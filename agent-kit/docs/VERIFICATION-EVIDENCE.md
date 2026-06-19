# Live verification evidence (2026-06-19)

> 토큰·비밀값은 기록하지 않음. 실행 환경: Windows, paransky97.

## 1. MCP smoke_test — 5/5 PASS

### A. 운영 MCP (OneDrive, 토큰·SFTP 설정 있음)

```
경로: OneDrive/문서/개발/web/cafe24/mcp
명령: python smoke_test.py
결과: 5/5 통과, 도구 8종 등록
시각: 2026-06-19 (세션 내)
```

| # | 도구 | 결과 |
|---|------|------|
| 1 | cafe24_auth_status | OK (scope: mall.read_design, refresh 후 valid) |
| 2 | cafe24_list_themes | OK |
| 3 | cafe24_sftp_list /skin14 | OK |
| 4 | cafe24_sftp_read CSS | OK |
| 5 | cafe24_sftp_upload /skin2 | OK (쓰기 거부 = 정상) |

### B. 워크스페이스 MCP (업graded server.py, design_type 제거)

```
경로: {키트루트}/mcp
전제: config/{몰ID}.token.json, sftp_{몰ID}.json,
      cafe24_config_{몰ID}.py (example 복사 후 편집, gitignore)
명령: python smoke_test.py (SFTP 연속 호출 시 35s 쿨다운 후 재실행)
결과: 5/5 통과 (자격 있음) · 5/9 partial exit 0 (v2.2+, 자격 없음)
```

**교훈:** SFTP rate-limit — smoke 직후 연속 실행 시 SSH banner reset 가능. 30s+ 간격 권장.

---

## 2. skin_no ↔ skin_code ↔ SFTP (라이브 교차 검증)

`list_themes` + `sftp.list('/{skin_code}')` — **6/6 SFTP_OK**

| skin_no | skin_code | SFTP path | editor_type | skin_name |
|---------|-----------|-----------|-------------|-----------|
| 19 | skin17 | /skin17 | **E** | 테스트_스킨_엎는 용 |
| 18 | skin16 | /skin16 | H | 테스트_스킨 |
| 17 | skin15 | /skin15 | H | 베이직 |
| 16 | skin14 | /skin14 | **E** | 아키테이블 |
| 4 | skin2 | /skin2 | H | 에스테 반응형 |
| 1 | base | /base | **E** | 쇼핑몰 기본디자인 |

**확정 (⚠️ 실측, 공식 문장 없음):**
- `skin_code` → `/{skin_code}` SFTP 루트 **6/6 일치**
- `skin_no` 숫자 ≠ 폴더 숫자 (예: 16 → skin14)

**SFTP 루트 목록 (paransky97):** `/base`, `/mobile`, `/skin14`, `/skin15`, `/skin16`, `/skin17`, `/skin2`, `/web`  
**`/sde_design`:** 이 몰 SFTP 루트 목록에 **없음** (별도 list 시 0건)

---

## 3. Easy(editor_type E) 재검증 — 기존 키트 주장 수정

| 주장 | 라이브 결과 | 판정 |
|------|-------------|------|
| Easy 경로 `/sde_design/base/` | paransky97 SFTP에 **미노출** | ⚠️ 몰/계정별 다를 수 있음 |
| Easy SFTP 불가 | **E 스킨도 /skin14, /base SFTP list OK** | ❌→⚠️ **「불가」는 과장.** API `editor_type=E` 와 SFTP 접근은 **분리**. 공식 정책 문장 없음 |
| skin14 = HTML 작업본 | **editor_type=E** (2026-06-19) | ⚠️ 반드시 `list_themes` 재확인 |
| base layout data-ez | **True** (read_page skin_no=1) | ⚠️ 실측 |
| skin14 layout data-ez | **False** (EZ 제거·하이브리드 가능) | ⚠️ editor_type만으로 EZ 여부 판단 불가 |

---

## 4. 남은 위험 재점검

| 위험 | 재점검 결과 |
|------|-------------|
| smoke 미실행 | ✅ OneDrive + workspace **5/5** |
| skin 매핑 미검 | ✅ 6/6 교차 |
| Easy/SFTP/sde_design | ⚠️ **문서 수정 필요** (본 evidence 반영) |
| monorepo config 경로 | ⚠️ workspace 단독 시 `cafe24_config_{mall}.py` 필요 — README 보완 |
| 파트너 웹FTP 공식 URL | ❌ 여전히 미수집 (AUDIT P1A-1) |
| 원본 OneDrive agent-kit 미동기화 | ⚠️ 의도적 (복제본만 업그레이드) |
| SKILL §0 공식처럼 읽힘 | 🔧 §0 AUDIT 라벨 패치 예정 |

---

## 5. 재실행 명령

```bash
# 배포 키트 (자격 없음 — 5/9 partial 정상)
cd mcp && SMOKE_PREFLIGHT_ALL=0 python smoke_test.py

# 자격 있음 (전체 smoke)
cd mcp && python smoke_test.py
```

---

## 6. 파트너 데모몰 2차 실측 — ecudemo400786 (2026-06-19)

> 1차(paransky97)와 **계정 유형·프로토콜·루트 경로가 다름**. 비밀번호는 기록하지 않음.

### 6.1 접속

| 항목 | 값 | 판정 |
|------|-----|------|
| 몰 ID | `ecudemo400786` | ⚠️ 실측 |
| 쇼핑몰 URL | `https://ecudemo400786.cafe24.com/` | ✅ HTTP 200, 정상 쇼핑몰 |
| 프로토콜 | **FTP** (SFTP 아님) | ⚠️ 실측 |
| 호스트 | `ecudemo400786.ftp.cafe24.com` | ⚠️ `{몰ID}.ftp.cafe24.com` 패턴 일치 |
| 포트 | **21** | ⚠️ (22 TCP 타임아웃) |
| 포트 3822 | 미시도 — 이번 계정은 FTP 21 | — |

### 6.2 FTP 루트 vs paransky97 SFTP 루트

| 구분 | paransky97 (일반·디자인 SFTP) | ecudemo400786 (파트너·웹 FTP) |
|------|-------------------------------|-------------------------------|
| 프로토콜 | SFTP (paramiko) | **FTP** port 21 |
| 루트 폴더 | `/base`, `/skin14`, `/mobile`, `/web` … | **`/sde_design`**, `/web`, `/w3c` |
| `/sde_design` | **루트에 없음** | **있음** |
| `/{skin_code}` 루트 | ✅ `/skin14` 등 | ❌ `/skin1`, `/skin2`, `/base` **루트에 없음** |
| PC 스킨 경로 | `/skin14/…` 또는 `/base/…` | **`/sde_design/base/…`** |
| 모바일 | `/mobile/…` (루트) | **`/sde_design/mobile/…`** |

**확정 (⚠️ 실측 2몰 교차, 공식 문장 없음):** 파트너 샘플몰은 **`/sde_design/` 아래**에서 base/mobile을 편집한다. 일반 몰 가이드의 **`/{skin_code}`** 규칙을 그대로 쓰면 **경로 오류**.

### 6.3 HTML 샘플 (FTP 다운로드)

| 파일 | data-ez | module= | 비고 |
|------|---------|---------|------|
| `/sde_design/base/index.html` | 0 | 39 | `<!--@layout(/layout/basic/main.html)-->` |
| `/sde_design/base/layout/basic/layout.html` | 0 | 37 | XHTML 스마트디자인 HTML |

### 6.4 ecudemo394381 (구 template-01)

| 항목 | 2026-06-19 결과 |
|------|-----------------|
| 쇼핑몰 | ❌ 카페24 warn(계정 미연결) 페이지 |
| FTP 21/22/3822 | ❌ 전부 타임아웃 |
| 과거 실측 | 2026-05 scan: 동일 `/sde_design` 구조 — **몰 만료·비활성 추정** |

### 6.5 API/MCP

| 항목 | 결과 |
|------|------|
| OAuth / `list_themes` | **N/A** — ecudemo400786용 토큰 없음 |
| 파트너 실습 | **FTP 실측만**으로 충분. MCP는 일반 몰 OAuth 후 별도 |

### 6.6 에이전트 교훈

1. **파트너 vs 일반** 분기 후 **경로 규칙을 바꿀 것** (`/sde_design/base` vs `/{skin_code}`).
2. 파트너도 **포트·프로토콜 가정 금지** — 이번 몰은 FTP **21**, 과거 template-01 로그는 SFTP **3822**.
3. `editor_type` / API 없이 작업 시 **FTP에서 실제 폴더**를 먼저 list.

근거 파일: [`_evidence/partner-live-ecudemo400786-2026-06-19.txt`](./_evidence/partner-live-ecudemo400786-2026-06-19.txt)
