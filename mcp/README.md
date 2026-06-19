# 카페24 스마트디자인 MCP — 손발 모듈

> 설계서: 모노레po 전용 `../api-poc/MCP-DESIGN.md` (배포본에는 미포함)  
> 두뇌(규칙·문법·교훈)는 `../agent-kit/` — 이 폴더는 실제 몰에 손을 뻗는 "손발".

## 현재 상태 (로드맵 §8 기준)

- [x] 1단계 — API 백엔드 모듈화 (토큰 자동갱신 포함) ✅ 2026-06-10 검증
- [x] 2단계 — SFTP 백엔드 통합 ✅ 2026-06-10 라이브 검증 (ls/cat/get/backup + 업로드 왕복 + 화이트리스트 거부)
- [x] 2b단계 — **FTP 백엔드** (파트너 웹 FTP port 21) ✅ 2026-06-19 ecudemo400786 list/read/download/upload 검증
- [x] 3단계 — MCP 서버 골격 ✅ 2026-06-10 (`server.py`, FastMCP stdio, 도구 8종, `smoke_test.py` 5/5 통과)
- [x] 4단계 — 워크스페이스 `.mcp.json` 에 `cafe24` 등록 ✅ 2026-06-10 (등록 명령 그대로 핸드셰이크 검증. **Claude Code 재시작 후 활성화**)

> 남은 선택 항목: §8-5 카페24 API 쓰기(`mall.write_design`) 승인 신청 — 풀리면 SFTP 의존 축소.

## MCP 서버 (server.py)

```bash
python server.py        # stdio 서버 실행 (.mcp.json 등록용 — 직접 띄울 일은 거의 없음)
python smoke_test.py    # 실제 MCP 클라이언트로 왕복 검증 (도구 8종 + 실호출 5건)
```

등록 도구 8종 (요구사항: `pip install "mcp[cli]"` — 2026-06-10 mcp 1.27.2 설치됨):

| 도구 | 역할 | 비고 |
|---|---|---|
| `cafe24_list_themes` | 디자인 목록 + skin_code(SFTP 폴더명) | 작업 시작점 |
| `cafe24_read_page` | HTML 페이지 정본 읽기 (API) | 에셋은 422 → sftp_read |
| `cafe24_auth_status` | 토큰 진단 | |
| `cafe24_sftp_list` | 파일트리 | depth 1~5 |
| `cafe24_sftp_read` | 파일 내용 (에셋 포함) | 5MB 제한 |
| `cafe24_sftp_download` | 파일/폴더 재귀 다운로드 | 대량 동기화 |
| `cafe24_sftp_backup` | 쓰기 전 백업 → `backups/` | |
| `cafe24_sftp_upload` ★ | 운영 반영 | 사용자 컨펌 필수 + 화이트리스트 + 자동백업 |
| `get_kit_guides` | agent-kit 부트스트랩 | 작업 시작 시 1순위 |
| `run_preflight` | verify-loop Phase 0/0.5 채점 | score 스크립트 subprocess 래핑 |

### `run_preflight` (Phase 2 — verify-loop 자동 채점)

`work/scripts/ref393674-score-*.py` 를 subprocess로 실행해 JSON 점수·FAIL 항목·F-code 힌트를 반환합니다.

| `check` | score 스크립트 | 용도 |
|---------|----------------|------|
| `header` | `ref393674-score-header.py` | 헤더·로고 |
| `mobile_full` | `ref393674-score-mobile-full.py` | C1 #contents 92% + MOBILE_WEB (F34 안내) |
| `plp` / `pdp` / `basket` / `member` / `board` / `page` / `paginate` | 동명 `ref393674-score-*.py` | 페이지별 verify-loop |
| **`all`** | 위 9종 **순차 일괄** | batch 요약: `passed/9`, `failed_checks`, `mobile_web_hint` |

**MCP 호출 예 (Cursor):**

```json
{ "check": "mobile_full", "mall_id": "ecudemo400786" }
{ "check": "all", "mall_id": "ecudemo400786" }
```

**`check=all` 반환 필드 (요약):**

- `total_checks: 9`, `total_passed`, `pass` (9/9 전부 score 100)
- `checks` — check명 → `{ total_score, pass, fails, f_codes }` 맵
- `f34_message` — `mobile_full`에서 MOBILE_WEB=true 시 F34 (관리자 MO off + live `CAFE24.MOBILE_WEB=false` 확인)

**전제:** `pip install playwright && playwright install chromium` — 미설치 시 `error` 필드.

**로컬 검증:**

```bash
cd mcp
python smoke_test.py                         # invalid + header (빠름)
SMOKE_PREFLIGHT_ALL=1 python smoke_test.py   # check=all 9/9 (~15분)
```

### 핵심 발견

1. **API `skin_code` → SFTP `/{skin_code}`** ⚠️ 실측 (공식 문장 없음).

   **2026-06-19 demo000 라이브 (6/6 SFTP_OK):**

   | skin_code | skin_no | editor_type | skin_name |
   |-----------|---------|-------------|-----------|
   | skin17 | 19 | E | 테스트_스킨_엎는 용 |
   | skin16 | 18 | H | 테스트_스킨 |
   | skin15 | 17 | H | 베이직 |
   | skin14 | 16 | **E** | 아키테이블 |
   | skin2 | 4 | H | 에스테 반응형 |
   | base | 1 | E | 쇼핑몰 기본디자인 |

   **주의:** `skin_no`≠폴더 숫자. **E 스킨도 SFTP 접근 가능** (정책과 별개).

2. **API `pages` 는 HTML만.** CSS 등 → `cafe24_sftp_read`.
3. **smoke_test 5/5** — 2026-06-19 OneDrive·workspace 재검증. SFTP 연속 호출 시 30s+ 쿨다운.
4. 쓰기 허용 (demo000): `/skin14`, `/skin16`, `/mobile` (sftp json 기준).

## 폴더 구조

```
mcp/
├── cli.py                  ← 검증용 CLI (MCP 서버 올리기 전 손 테스트)
├── backends/
│   ├── cafe24_api.py       ← Admin API 읽기: list_themes / read_page / auth_status
│   └── cafe24_sftp.py      ← SFTP: list / read / download / backup / upload★
├── auth/
│   └── oauth.py            ← TokenManager: 토큰 저장·만료검사·자동갱신·재동의
├── backups/                ← upload 전 자동 백업본 (git 제외)
└── config/                 ← 몰별 설정·토큰 (git 제외)
    ├── __init__.py         ← load_mall_config() / load_sftp_config()
    ├── demo000.token.json   (자동 생성, git 제외)
    └── sftp_demo000.json    (자동 이전, git 제외 — write_allowed 포함)
```

## 사용법 (이 폴더에서 실행)

```bash
# API 백엔드 (읽기·메타)
python cli.py status                          # 토큰 상태 (만료시각·scope)
python cli.py themes                          # 디자인 목록 (H=스마트디자인, E=Easy)
python cli.py page 4 /layout/basic/layout.html  # 스킨 파일 1건 소스 읽기

# SFTP 백엔드 (탐색·대량·쓰기)
python cli.py ls /skin4 2                     # 파일트리 (깊이 2)
python cli.py cat /skin4/index.html           # 파일 내용
python cli.py get /skin4/_nk/css ./tmp/css    # 폴더 다운로드
python cli.py backup /skin4/index.html        # 백업본 생성 → backups/
python cli.py put ./로컬파일 /skin4/경로        # ★업로드 (사용자 컨펌 후에만)
```

### upload 안전장치 (운영 반영)

- `write_allowed` 화이트리스트(`config/sftp_{mall}.json`) 밖 경로는 **무조건 거부**
  — demo000: `/skin14`·`/mobile`만 허용, `/skin2`(IDIO원본)·`/skin15`·`/base` 보호 ✅ 검증 통과
- 업로드 전 원본을 `backups/{mall}/{시각}/`에 **자동 백업** (기본 ON)
- 에이전트는 upload 호출 전 반드시 사용자 확인 (누끼토끼 절대룰)

토큰은 호출 때마다 자동으로 만료 검사 → 만료면 refresh_token 으로 재발급.
refresh_token(2주)까지 만료된 경우에만:

```bash
python cli.py auth-url          # 브라우저에서 '허용' 클릭
python cli.py code "<이동된 URL>"  # 토큰 재발급
```

## 파이썬 코드에서 쓰기 (3단계 MCP 서버가 쓸 형태)

```python
from backends.cafe24_api import Cafe24API

api = Cafe24API("demo000")   # 몰 아이디
themes = api.list_themes()      # [{skin_no, skin_name, editor_type, ...}]
page = api.read_page(4, "/layout/basic/layout.html")  # {"path", "source", ...}
```

## 몰 추가 방법 (reference-case 등)

1. `config/cafe24_config_{mall_id}.py` 생성 (서식: `config/cafe24_config.example.py`)
2. `python cli.py auth-url --mall {mall_id}` → 브라우저 허용 → `code` 교환

## 보안 규칙

- `config/` 안의 `cafe24_config_*.py`·`*.token.json` 은 git 제외 (`config/.gitignore` + 루트 `.gitignore`).
- 비밀키·토큰 값은 로그/채팅에 출력하지 않는다 (`status`도 만료시각만 보여줌).
- API 쓰기(`PUT pages`)는 카페24 미승인 상태 — 업로드는 SFTP(2단계)로.
