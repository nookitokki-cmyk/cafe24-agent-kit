# 카페24 스마트디자인 작업용 MCP 에이전트 — 설계서 (v0.1)

> 코딩 전 "그림 맞추기" 문서. 검증된 사실 + 아키텍처 + 도구 목록 + 인증 처리 + 로드맵.
> 작성: 2026-06-09 · 대상 몰: paransky97 (template-02) · 상태: 설계 단계

---

## 1. 목표

카페24 **스마트디자인(HTML 방식)** 스킨을, 에이전트가
- **읽고 분석**(현재 구조·규칙·시스템 파악)하고
- **설계·생성**한 코드를
- **실제 스킨에 반영**

하는 작업을, 사람이 매번 FTP·관리자창을 오가지 않아도 되게 만드는 MCP 서버.

> 기존 `web/cafe24/agent-kit/`(에이전트의 "두뇌": 규칙·교훈·문법)는 그대로 두고,
> 이 MCP는 그 두뇌가 **실제 몰에 손을 뻗는 "손발"** 역할을 한다.

---

## 2. 검증된 사실 (2026-06-09 PoC 결과)

| 항목 | 결과 | 근거 |
|---|---|---|
| Admin API OAuth 인증 | ✅ 성공 | `read_skins.py` 토큰 발급 |
| 디자인 목록 조회 `GET /themes` | ✅ 200 | skin_no 17·16·4·1 (H/E 타입 식별) |
| 스킨 소스 읽기 `GET /themes/{skin_no}/pages?path=` | ✅ 200 | layout.html 21,437자 정본 수신 |
| 스킨 소스 쓰기 `PUT /themes/{skin_no}/pages` | ⚠️ **제한 API** | 문서: "특정 클라이언트만 사용 가능, 카페24 문의" |
| access_token 수명 | 2시간 | `expires_at` |
| refresh_token 수명 | 2주(슬라이딩) | `refresh_token_expires_at` |
| 부여된 권한 | `mall.read_design` | `scopes` |

**핵심 제약**: API "읽기"는 자유롭지만, **API "쓰기(소스 수정)"는 카페24 승인을 받은 앱만** 가능.
→ 승인 전까지 **업로드(쓰기)는 SFTP로** 한다.

**API 읽기의 구조적 한계**:
- `GET pages`는 **`path`를 알아야 1건씩** 읽음 → 파일트리 "목록 조회" 기능 없음.
- 호출 제한 **40건** → 수백 개 CSS/JS 에셋 일괄 수집엔 부적합.
- 정적 에셋(이미지 등) 전부를 노출하는지 불확실.
→ **전체 탐색·대량 읽기는 SFTP가 우위.**

---

## 3. 아키텍처 — 역할 분담 (하이브리드)

```
┌─────────────────────────────────────────────┐
│        에이전트 (agent-kit 규칙으로 사고)        │
└───────────────┬─────────────────────────────┘
                │  MCP 도구 호출
        ┌───────┴────────┐
        ▼                ▼
┌──────────────┐  ┌──────────────────┐
│  API 백엔드    │  │   SFTP 백엔드      │
│ (읽기·메타)    │  │ (탐색·대량·쓰기)   │
├──────────────┤  ├──────────────────┤
│ 디자인 목록     │  │ 파일트리 listing   │
│ 정본 1건 읽기   │  │ 대량 다운로드      │
│ 인증 안정       │  │ 업로드(쓰기) ★     │
└──────────────┘  └──────────────────┘
```

| 용도 | 백엔드 | 이유 |
|---|---|---|
| 디자인 목록·타입(H/E) 파악 | **API** | 메타데이터, JSON |
| 특정 템플릿 **정본** 읽기·진단 | **API** | 카페24 보관 원본, 인증 안정 |
| 전체 파일트리 탐색 | **SFTP** | API엔 listing 없음 |
| CSS/JS 대량 읽기·초기 동기화 | **SFTP** | 40건 제한 회피 |
| 모든 쓰기(업로드) | **SFTP** | API 쓰기 미승인 |

> 한 MCP 서버 안에 두 백엔드 도구를 모두 넣어, 에이전트가 상황별로 자동 선택.

---

## 4. MCP 서버 도구 목록 (제안)

### 4-1. API 백엔드 (읽기)
| 도구 | 입력 | 출력 | 비고 |
|---|---|---|---|
| `cafe24_list_themes` | (없음) | skin_no/이름/editor_type/usage 목록 | H=스마트디자인 식별 |
| `cafe24_read_page` | `skin_no`, `path` | 해당 파일 소스(정본) | 1건 |
| `cafe24_auth_status` | (없음) | 토큰 유효시간·scope | 진단용 |

### 4-2. SFTP 백엔드 (탐색·대량·쓰기)

> 구현 시 도구명에 `cafe24_` 접두사 통일 (타 MCP 의 generic 이름과 충돌 방지 — MCP 베스트 프랙티스).

| 도구 (구현명) | 입력 | 출력 | 안전장치 |
|---|---|---|---|
| `cafe24_sftp_list` | `remote_path`, `depth` | 파일/폴더 트리 | 읽기 |
| `cafe24_sftp_read` | `remote_path` | 파일 내용 | 읽기 |
| `cafe24_sftp_download` | `remote_path`, `local_path` | 저장 결과 | 읽기 |
| `cafe24_sftp_backup` | `remote_path` | 백업본 경로 | 쓰기 전 자동 호출 (upload 가 기본 수행) |
| `cafe24_sftp_upload` ★ | `local_path`/`content`, `remote_path` | 업로드 결과 | **운영 반영 — 실행 전 사용자 확인 + write_allowed 화이트리스트** |

> ★ 쓰기 도구는 "되돌리기 어려운 운영 반영"이라, 에이전트가 호출 전 반드시 사용자에게 확인.
> (누끼토끼 절대룰: 운영 업로드/배포 전 컨펌)

---

## 5. 인증 처리 (OAuth 토큰 수명 관리)

```
access_token (2h) 만료 → refresh_token 으로 자동 재발급
refresh_token (2주, 쓸 때마다 갱신) 만료 → 사용자 1회 재동의(브라우저 '허용')
```

- 토큰은 `cafe24.token.json`(**git 제외**)에 저장, MCP 서버가 매 호출 전 만료 검사 → 필요 시 `grant_type=refresh_token`으로 갱신.
- 비밀키(`CLIENT_SECRET`)·토큰은 절대 git/로그에 노출 금지.
- 멀티 클라이언트(slowagings 등) 확장 시: 몰별 `cafe24_config_{mall}.py` + `*.token.json` 분리.

---

## 6. 폴더 구조 (제안)

```
web/cafe24/
├── agent-kit/                 ← (기존) 에이전트 두뇌: 규칙·문법·교훈
└── mcp/                       ← (신규) 손발: MCP 서버
    ├── server.py              ← MCP 엔트리 (도구 등록)
    ├── backends/
    │   ├── cafe24_api.py       ← OAuth + themes/pages 읽기 (PoC read_skins.py 승격)
    │   └── cafe24_sftp.py      ← paramiko 기반 list/read/upload (기존 sftp_util 통합)
    ├── auth/
    │   └── oauth.py            ← 토큰 발급·자동갱신
    ├── config/                 ← 몰별 설정 (git 제외)
    └── README.md
```

> 현재 `api-poc/`의 `read_skins.py`·`cafe24_config.py`가 `mcp/backends/cafe24_api.py`의 원형.

---

## 7. 에이전트 연동 흐름 (예: "헤더를 레퍼런스처럼 바꿔줘")

```
1. cafe24_list_themes        → 작업 대상 skin_no 확정 (H 타입)
2. sftp_list /skinNN         → 파일트리 파악 (전체 구조)
3. cafe24_read_page (정본) + sftp_read (에셋)  → 현재 코드 분석
4. agent-kit 규칙으로 새 코드 설계·생성 (F1~F20 함정 회피)
5. sftp_backup → sftp_upload  → 운영 반영 (사용자 확인 후)
6. 라이브 ?v=N 스크린샷(PC+모바일) 검증  → "완료"
```

---

## 8. 구현 로드맵 (단계)

- [x] **0. 읽기 PoC** — OAuth + themes/pages 읽기 검증 (완료)
- [x] **1. API 백엔드 모듈화** — `read_skins.py` → 토큰 자동갱신 포함 함수화 (완료 2026-06-10, `web/cafe24/mcp/` — list_themes/read_page/auth_status 라이브 검증, 토큰은 `mcp/config/{mall}.token.json`으로 이전)
- [x] **2. SFTP 백엔드 통합** — 완료 (2026-06-10, `mcp/backends/cafe24_sftp.py`). 라이브 검증: ls/cat/get/backup + 업로드 왕복(업로드→재읽기→삭제) + 화이트리스트 거부 전부 통과. write_allowed=`/skin14`,`/mobile` (대표님 확정). ★추가 확정 사실: ①themes API `skin_code` = SFTP 폴더명 (두 백엔드의 다리) ②API pages 는 HTML만 — CSS 등 에셋 422 → 에셋은 SFTP 전담 (§2 가설 확정) ③SFTP 비번 만료 이력 — 재개설로 해결, 인증 거부 시 1순위 의심
- [x] **3. MCP 서버 골격** — 완료 (2026-06-10, `mcp/server.py`). FastMCP(mcp 1.27.2) stdio 서버에 도구 8종 등록. `smoke_test.py` 로 실제 MCP 클라이언트 왕복 검증 5/5 통과 (도구 목록 + auth_status/list_themes/sftp_list/sftp_read 실호출 + 보호슬롯 업로드 거부 확인)
- [x] **4. Cursor/Claude 등록** — 완료 (2026-06-10). 워크스페이스 `.mcp.json` 에 `cafe24` 서버 등록 (command=python, 절대경로, env 불필요 — 비밀키는 mcp/config/ 파일에서 읽음). 등록된 명령 그대로 핸드셰이크 + 도구 8종 노출 + 실호출 검증 통과. **Claude Code 재시작 후 `mcp__cafe24__*` 도구 사용 가능**
- [ ] **5. (선택) API 쓰기 승인 신청** — `mall.write_design` 풀리면 SFTP 의존 축소

---

## 9. 미해결·리스크

- **API 쓰기 승인** 가능 여부·소요기간 미확인 (카페24 개발자센터 문의 필요).
- **Client Secret 평문 노출** — 채팅에 입력된 이력 → **재발급 권장**(후속 조치).
- SFTP FTP 비번 **만료/IP 차단** 리스크 상존(slowagings는 이미 만료 이력).
- API "pages"의 정적 에셋 커버리지 미확인 — SFTP로 보완 전제.

---

_이 설계서는 코딩 시작 전 합의용 초안(v0.1)이다. 합의되면 §8 로드맵 1단계부터 착수._
