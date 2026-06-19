# 카페24 공식 가이드 대조표 (OFFICIAL-AUDIT)

> **품질 원칙:** 출처 없는 사실은 ✅로 표시하지 않는다.  
> **범례:** ✅ 공식 문서로 확인 | ⚠️ 미확인·부분 확인 | ❌ 키트와 공식 불일치 | 📎 근거 링크

**갱신:** Phase 1-A (2026-06-19) — FTP·몰 ID·접속 경로 분기  
**갱신:** Phase 1-C (2026-06-19) — 스마트디자인 문법·F1~F26 대조  
**갱신:** Phase 1-D (2026-06-19) — 스마트디자인Easy vs HTML 경계  
**갱신:** Phase 1-E (2026-06-19) — skin_no · skin_code · SFTP 폴더 매핑  
**다음 예정:** Phase 1-F 풀 감사 마무리, Phase 2 접속 가이드 …

---

## Phase 1-A. 몰 ID · FTP · 접속 경로

### A-1. 몰 ID (Mall ID)

| ID | 주장 | 키트 현재 | 공식/근거 | 판정 |
|----|------|-----------|-----------|------|
| A-1a | 쇼핑몰 URL `https://{몰ID}.cafe24.com/` 에서 앞부분이 몰 ID | `getting-started`·사용자 교정과 동일. **agent-kit `CLAUDE.md`는 몰 ID만 언급, URL 규칙은 없음** | Admin API OAuth 예시에 `{mallid}.cafe24api.com` 패턴 사용 → 몰 ID가 API 호스트에 쓰임은 **공식 확인** ([OAuth](https://developers.cafe24.com/docs/api/admin/#oauth2)). **쇼핑몰 프론트 URL `{id}.cafe24.com` 문장은 본 Phase에서 공식 HTML에서 직접 인용 못 함** | ⚠️ API 호스트 규칙 ✅ / 쇼핑 URL 규칙은 관례+실무, 공식 문장 추가 확인 필요 |
| A-1b | 파트너 샘플몰 예: `ecudemo400786` | 배포판 `getting-started`에 예시 있음. **workspace `agent-kit`에는 getting-started 없음** | 동일 | ⚠️ 예시는 실무 일치, 공식 샘플 URL 명칭 문서 미대조 |

### A-2. 계정 유형별 파일 접속 (핵심 분기)

| ID | 주장 | 키트 현재 | 공식/근거 | 판정 |
|----|------|-----------|-----------|------|
| A-2a | **파트너센터**에서 만든 샘플몰 → **웹 FTP** (디자인 FTP 아님) | 배포판 `getting-started/00` ✅. **`agent-kit/CLAUDE.md` 게이트는 「디자인 FTP 권한」만** → 파트너 분기 **없음** ❌ | Admin API 상품 이미지 업로드 옵션에 **「C : 웹FTP 등록」** 용어 존재 ([Admin API](https://developers.cafe24.com/docs/api/admin/)). **「파트너센터 샘플몰 = 웹 FTP만」 문장은 개발자센터 API 문서에서 직접 확인 못 함** | ⚠️ 웹FTP 용어 ✅ / 파트너→웹FTP 매핑은 내부 가이드+사용자 확정, **공식 파트너센터 문서 URL 필요 (Phase 1-A 보완)** |
| A-2b | 파트너 웹 FTP 호스트: `{몰ID}.ftp.cafe24.com` | 배포판 `getting-started` ✅ | **공식 문서 HTML에서 호스트 패턴 미확인.** 실측: `ecudemo400786.ftp.cafe24.com` (2026-06-19 FTP OK). 구 `ecudemo394381` (3822) — **2026-06-19 비활성** | ⚠️ 실측+내부 가이드 일치, **공식 호스트 문서 인용 0건** |
| A-2c | 파트너 웹 FTP 로그인 = 파트너센터 계정과 동일 | 배포판 `getting-started` | 공식 미확인 | ⚠️ |
| A-2d | **일반 운영 몰** → 관리자 **디자인 FTP 권한 신청** 후 SFTP 정보 발급 | `CLAUDE.md` 게이트 #2 ✅ (디자인 FTP만) | **관리자 메뉴 경로「디자인 → 디자인 FTP → 권한 신청」공식 HTML 미확인** (ecsupport/help 미수집) | ⚠️ 내부 가이드·실무, 공식 매뉴얼 링크 필요 |
| A-2e | 일반 몰 SFTP 호스트도 `{몰ID}.ftp.cafe24.com` | 키트는 호스트 형식 **명시 안 함** (MCP config에만 존재) | 실측 **반례:** 운영 몰 `paransky97` → `ecimg-ftp-c01.cafe24img.com:8008` (`clients/template-02/.vscode/sftp.json`) | ❌ **「항상 몰ID.ftp」는 틀릴 수 있음.** 호스트는 **발급된 SFTP 정보를 그대로** 써야 함 |
| A-2f | 포트는 22(SFTP 표준) | MCP 기본 `port` 22 (`config` 로더) | 파트너 실측 **21(FTP)**, 과거 **3822(SFTP)**, 운영 몰 **8008** | ❌ 키트/MCP 기본값만 믿으면 접속 실패. **발급 port·프로토콜 필수** |
| A-2g | 프로토콜: SFTP(SSH) | SKILL·MCP: paramiko SFTP ✅ | 파트너 `ecudemo400786` **FTP 21** (2026-06-19). 구 template-01 SFTP 3822 | ⚠️ **몰·시기별 FTP/SFTP 혼재** |
| A-2h | 파트너 편집 경로 `/sde_design/base` | getting-started §03 (2026-06-19 반영) | API·공식 문장 없음. 2몰 교차: paransky97 루트 `/skin14` vs partner `/sde_design/base` | ⚠️ **계정 유형별 경로 분기 필수** |

### A-3. API 메타와 SFTP 폴더 연결 (작업 시작 시)

| ID | 주장 | 키트/MCP | 공식/근거 | 판정 |
|----|------|----------|-----------|------|
| A-3a | `skin_no` = 디자인 번호 | MCP·AGENT ✅ | Themes API: `skin_no` 「디자인 번호」 ([Themes](https://developers.cafe24.com/docs/api/admin/#get-themes)) | ✅ |
| A-3b | `skin_code` = 디자인 코드 | MCP README: SFTP 폴더명과 같다고 기술 | API: `skin_code` 「디자인 코드」. **API 문서에 「SFTP 폴더명과 동일」 문장 없음** — 2026-06-10 라이브 검증 | ⚠️ API 필드 ✅ / 매핑 규칙은 **§E-2 실측** |
| A-3c | `editor_type` H=HTML 스마트디자인, E=Easy | SKILL ✅ | API: `H : 스마트 디자인 (HTML)`, `E : 스마트디자인Easy` 등 | ✅ |

### A-4. 키트 구조 결함 (공식과 무관하지만 Phase 3 차단 요소)

| ID | 문제 | 위치 | 판정 |
|----|------|------|------|
| A-4a | `getting-started/` 없는데 `CLAUDE.md`가 링크 | `agent-kit/CLAUDE.md` L26 | ❌ 깨진 참조 |
| A-4b | FTP 게이트가 일반 몰(디자인 FTP)만 가정 | `CLAUDE.md` L27 | ❌ 파트너 웹 FTP 사용자 오안내 |
| A-4c | SFTP 호스트·포트를 문서화하지 않음 | `CLAUDE.md` §6, SKILL | ⚠️ MCP config 의존 — **「발급 정보 그대로」 규칙 문서화 필요** |

---

## Phase 1-C. 스마트디자인 HTML 문법 · F1~F26

### C-1. 핵심 문법 (키트 vs 공식)

| ID | 키트 주장 | 공식 출처 | 판정 |
|----|-----------|-----------|------|
| C-1a | `<!--@layout(/path/layout.html)-->` 첫 줄 | basic: `<!--@layout(layout.html)-->` (경로 표기 예시는 상대) | ✅ 지시어 존재 확인. **풀경로 `/layout/basic/...` 는 SKILL·실무** |
| C-1b | `<!--@css-->`, `@import`, `@js` 지시어 | developers basic HTML **본문에서 @css/@import 미발견** | ⚠️ SKILL·AGENT에만 — **별도 공식 페이지 추가 수집 필요** |
| C-1c | `module="모듈아이디"` 로 엔진 구동 | basic: 「module="모듈아이디"에 따라 판단되고 구동」 | ✅ |
| C-1d | `{$변수}` 는 **module 안에서만** 치환 | basic: 「변수는 모듈에 상속되어 동작」「모듈마다 변수 정해짐」 | ✅ (module 밖 금지는 키트가 공식을 **보수적으로 해석**) |
| C-1e | `{$image_medium}` 등 상품 변수 | basic 예시 명시 | ✅ |
| C-1f | 반복: 주석변수 `$count`, 우선순위 `$only_html > $count > DB` | basic § 주석변수 활용 | ✅ |
| C-1g | 반복: **anchorBoxId 블록 2개 이상** 나란히 (getting-started 04) | 공식은 `$count` 등 **다른 문법**; anchorBoxId는 sdsupport **쇼핑몰 UI id**로만 확인 | ⚠️ 「2개 이상」규칙은 **실무·키트** — 공식 동일 문장 없음 |
| C-1h | `module="Layout_category"` 등 레이아웃 모듈명 | sdsupport cate_no=61 목록 307종 (예: product_no 3791 전체 상품분류) | ✅ 모듈명 카탈로그. **영문 ID는 상세 페이지·소스로 교차** |
| C-1i | `xans-{module}` 자동 클래스 | module 상세 렌더 예시 `xans-record-`, `xans-product-...` | 🟡 패턴 실측·상세페이지; **「xans- 규칙」한 줄 공식 문장 미수집** |
| C-1j | HTML 스마트디자인 vs Easy (`editor_type` H/E) | Admin API + SKILL §0 | ✅ (Phase 1-A·SKILL) |
| C-1k | Easy: `data-ez-*`, `/sde_design/base/` | SKILL §0 | ⚠️ **Phase 1-D: 공식 인용 0건** — 아래 §D-3 |

### C-2. F1~F26 함정 — 공식 대조 요약

| 구분 | 개수 | 설명 |
|------|------|------|
| ✅ 공식 직접 뒷받침 | **4** | C(변수·모듈), F25(@layout), F26(@layout 연계), 초보 #2·#5 |
| ⚠️ 실무·프로젝트 (공식 동일 문장 없음) | **22** | F1~F24 대부분, F3 캐시, F4 @css ? |
| ❌ 키트 내부 불일치 | **2** | AGENT 578줄·F전체 한 파일 / `traps/INDEX` 없었음 → **이번에 INDEX 생성** |

상세 한 줄 목록: [`traps/INDEX.md`](../traps/INDEX.md)

### C-3. 키트 구조 (문법 감사 부수 결과)

| ID | 문제 | 판정 |
|----|------|------|
| C-3a | F1~F26이 `CAFE24-SMARTDESIGN-AGENT.md` 한 파일에만 — 진입 시 과부하 | ⚠️ `traps/INDEX.md` 추가(Phase 1-C) · Phase 2에서 CLAUDE 링크 |
| C-3b | SKILL 「sdsupport 기반」이나 @css/@import **공식 인용 파일 없음** | ⚠️ P1C-1 보완 |
| C-3c | `references/modules.md`·`variables.md` vs sdsupport 307종 — 동기화 여부 미검 | ⚠️ Phase 1-E |
| C-3d | module-index.md (template-01) 307종 — workspace 키트에 **미포함** | ⚠️ 링크만 AUDIT에 기록 |

### C-4. 에이전트 규칙 초안 (문법 작업 시)

1. **공식 🟢만** 「카페24 공식」이라 말한다. F함정은 「실무에서 검증된 함정」.
2. 수정 전: `@layout` 참조 grep → 실사용 layout 확정 (F26).
3. 변수·모듈: [basic 가이드](https://developers.cafe24.com/design/front/smart/sdsupport/basic) + module 상세 URL.
4. 「상품 1개만」증상 → F3 캐시 먼저, 그다음 반복 블록(F4/getting-started) — **둘 다 확인**.

---

## Phase 1-B. OAuth · 앱 등록 · Admin API (MCP 손발)

### B-1. 공식 등록·설정 순서

| ID | 단계 | 공식 안내 | 판정 |
|----|------|-----------|------|
| B-1a | 개발사(자) 등록 | [개발가이드 > 개발사(자) 등록](https://developers.cafe24.com/app/front/app/develop/developedit) | ✅ 링크·메뉴 존재 (세부 클릭 경로는 UI 스크린샷 문서 — HTML에 단계 본문 일부만) |
| B-1b | 앱 생성 | 개발자센터 로그인 → **[Apps > App 관리]** → App 등록 ([createapps](https://developers.cafe24.com/app/front/app/develop/createapps)) | ✅ |
| B-1c | Redirect URI · Scope | **[개발자 어드민 > 상품관리 > App 관리 > STEP 1. 개발정보관리]** ([oauth/put](https://developers.cafe24.com/app/front/app/develop/oauth/put)) | ✅ |
| B-1d | Redirect URI 규칙 | **반드시 HTTPS**, **실제 서비스 도메인**, 인증 코드 수신용 | ✅ |
| B-1e | Scope 선택 | **[권한관리]** 에서 선택한 항목만 authorize `scope`에 넣을 수 있음 ([oauth/oauthcode](https://developers.cafe24.com/app/front/app/develop/oauth/oauthcode)) | ✅ |

### B-2. OAuth 흐름 (API 문서 + 개발 가이드 교차)

| ID | 주장 | 키트/MCP 현재 | 공식/근거 | 판정 |
|----|------|---------------|-----------|------|
| B-2a | 인가 URL `https://{mall_id}.cafe24api.com/api/v2/oauth/authorize?...` | `oauth.py` `auth_url()` ✅ | [oauthcode](https://developers.cafe24.com/app/front/app/develop/oauth/oauthcode), [Admin OAuth](https://developers.cafe24.com/docs/api/admin/#oauth2) | ✅ |
| B-2b | `client_id`, `redirect_uri`, `scope`는 앱 등록값과 **정확히 일치** | `cafe24_config.example.py` | oauthcode 파라미터 표 | ✅ |
| B-2c | 인증 코드 **1분 만료**, 재사용 불가 | PoC `read_skins.py` 주석 ✅ | oauthcode + Admin API | ✅ |
| B-2d | 토큰 교환 `POST .../oauth/token`, `grant_type=authorization_code`, Basic auth | `oauth.py` / `read_skins.py` ✅ | [oauth/token](https://developers.cafe24.com/app/front/app/develop/oauth/token) | ✅ |
| B-2e | access_token **2시간** | MCP-DESIGN·oauth.py ✅ | [oauth/retoken](https://developers.cafe24.com/app/front/app/develop/oauth/retoken) | ✅ |
| B-2f | refresh_token **14일** (발급 기준) | MCP 주석 「2주」·MCP-DESIGN 「2주 슬라이딩」 | 공식: 「발급으로부터 14일」— **사용 시 연장(슬라이딩) 문구 없음** | ⚠️ 14일=2주는 ✅ / 슬라이딩은 실측·미공식 |
| B-2g | refresh 만료 시 처음부터 재동의 | `TokenManager` ✅ | oauth/retoken | ✅ |
| B-2h | API 호출 시 `X-Cafe24-Api-Version` | `cafe24_config.example.py` `API_VERSION` ✅ | Admin API 문서 | ✅ |
| B-2i | 최초 실행 주체: **쇼핑몰 운영자** 권한 위임 | 키트에 명시 약함 | [oauth/process](https://developers.cafe24.com/app/front/app/develop/oauth/process) | ⚠️ 에이전트가 「관리자로 로그인한 뒤 허용」안내 필요 |

### B-3. Scope (스마트디자인 MCP 최소 권한)

| ID | Scope | 공식 설명 | MCP 권장 | 판정 |
|----|-------|-----------|----------|------|
| B-3a | `mall.read_design` | 디자인(Themes)·화면(Pages) **조회** | `SCOPE` 기본값 ✅ | ✅ |
| B-3b | `mall.write_design` | Themes/Pages **생성·수정·삭제** | MCP는 SFTP 쓰기, API PUT은 미사용 | ✅ scope 정의 / ⚠️ API PUT은 별도 승인(B-4b) |
| B-3c | `mall.write_design, mall.read_design` 묶음 동의 문구 | Scope 목록에 복합 형태 존재 | 읽기만 쓸 때는 **read만** 요청하는 게 맞음 | ✅ |

### B-4. API 쓰기 vs SFTP (MCP 설계 검증)

| ID | 주장 | MCP | 공식 | 판정 |
|----|------|-----|------|------|
| B-4a | Themes/Pages **읽기** API 사용 가능 | `cafe24_list_themes`, `cafe24_read_page` | `mall.read_design` | ✅ |
| B-4b | **PUT** `/themes/{skin_no}/pages` — 특정 클라이언트만, 개발자센터 문의 | SFTP 업로드로 우회 | Admin API + 1-A 인용 | ✅ MCP 전략 타당 |
| B-4c | 호출 제한 40건/… | MCP가 SFTP로 대량 읽기 | Themes read 섹션 | ✅ |

### B-5. 키트·예제와 공식 **불일치** (❌)

| ID | 문제 | 위치 | 공식 | 판정 |
|----|------|------|------|------|
| B-5a | `REDIRECT_URI = "http://localhost:8888/callback"` | `api-poc/cafe24_config.example.py` (원본 참조) | Redirect URI **HTTPS 필수** | ❌ 예제는 로컬 PoC 우회용; **공식 등록값으로 http 사용 불가** |
| B-5b | PoC 「브라우저 주소창 code 복사」우회 | `read_skins.py` | 공식은 Redirect URI로 code 전달 — **우회는 비공식 실무 해법** | ⚠️ 문서에 「공식=HTTPS 서버」와 「PoC 우회」분리 표기 필요 |
| B-5c | `/카페24-mcp` 핑퐁 명령 없음 | workspace agent-kit | Phase 5에서 구현 예정 | ❌ (기능 갭) |
| B-5d | MCP 연결 가이드가 키트에 없음 | agent-kit; `mcp/README`만 존재 | 모노레포 README 일부 | ⚠️ |

### B-6. `/카페24-mcp` 핑퐁 초안 (공식 순서만 — 구현 전 설계)

에이전트는 **한 번에 한 질문**, 답 없으면 다음 단계 금지.

| 순서 | 에이전트 질문 | 사용자 액션 | 공식 근거 |
|------|---------------|-------------|-----------|
| 1 | 개발자센터에 로그인할 수 있나요? | developers.cafe24.com 로그인 | createapps |
| 2 | 개발사(자) 등록을 마쳤나요? | developedit | developedit |
| 3 | [Apps > App 관리]에서 앱을 만들었나요? | App 등록 | createapps |
| 4 | STEP1에 **HTTPS** Redirect URI를 넣었나요? (값을 알려주세요 — secret 제외) | oauth/put | oauth/put |
| 5 | [권한관리]에서 `mall.read_design`을 켰나요? | scope | api/scope |
| 6 | 작업할 **몰 ID**는? (`https://____.cafe24.com`) | — | oauthcode `{mall_id}` |
| 7 | `client_id`는 준비됐나요? (`client_secret`은 **채팅에 붙이지 말 것**) | config 파일에만 저장 | oauthcode |
| 8 | `mcp/config/cafe24_config_{몰ID}.py` 만들까요? | example 복사 | MCP 로컬 |
| 9 | 브라우저에서 `python cli.py auth-url` URL 열고 **쇼핑몰 관리자**로 허용 | oauth/process | process |
| 10 | 리다이렉트된 URL에서 `code=` 복사 → `python cli.py auth-code "..."` | 1분 이내 | oauthcode |
| 11 | `python smoke_test.py` 결과 붙여주세요 | 5/5 확인 | MCP 로컬 |

---

## Phase 1-D. 스마트디자인Easy vs HTML (경계·폴더·편집 방식)

> **비유:** HTML 스마트디자인 = **레고 설명서대로 블록을 직접 조립**하는 방식. Easy = **미리 만들어진 방(블록)만 끼우는** 방식. API는 두 방의 **이름표(`editor_type`)**만 공식으로 붙여 준다. Easy 방의 **주소(`/sde_design`)·열쇠(SFTP)** 는 이번에 수집한 공식 문서에는 **아직 안 나온다**.

### D-1. API로 **확인된** 분류 (Themes)

| ID | 항목 | 공식 정의 | 판정 |
|----|------|-----------|------|
| D-1a | `editor_type` **H** | 스마트 디자인 **(HTML)** | ✅ [Themes property list](https://developers.cafe24.com/docs/api/admin/#themes-property-list) |
| D-1b | `editor_type` **E** | **스마트디자인Easy** | ✅ 동일 |
| D-1c | `editor_type` **D/W/C** | 에디봇(Drag&Drop) / 심플(WYSIWYG) / 콘텐츠스튜디오 | ✅ 동일 — **키트는 H·E만 강조, 나머지 3종 미문서화** |
| D-1d | `usage_type` S/C/I/M/N | PC·모바일 기본/복사/상속 스킨 구분 | ✅ 동일 |
| D-1e | `skin_code` | 디자인 코드 | ✅ 동일 — **SFTP·Easy 폴더명 규칙은 API에 없음** (Phase 1-E) |
| D-1f | Themes pages `path` | **파일 경로** (페이지 소스 조회·수정 시) | ✅ [Themes pages](https://developers.cafe24.com/docs/api/admin/#themes-pages-property-list) |

### D-2. 공식 **HTML 스마트디자인** 편집 UI (Easy 아님)

| ID | 공식 안내 | 출처 | 판정 |
|----|-----------|------|------|
| D-2a | 스마트 디자인 편집창에서 **HTML 직접 편집** + **모듈** 활용 | [sdsupport 소개](https://developers.cafe24.com/design/front/smart/sdsupport) | ✅ |
| D-2b | 편집창 = **화면 보기** + **HTML 보기** | [편집창 이해하기](https://developers.cafe24.com/design/front/smart/sdsupport/editor) | ✅ |
| D-2c | 모듈에 마우스오버 → **편집** 버튼으로 수정 | editor 가이드 | ✅ |
| D-2d | developers **스마트 디자인** 메뉴에 Easy 전용 하위 가이드 URL | HTML 스크랩 메뉴 | ⚠️ **Easy 전용 공식 가이드 링크 없음** (sdsupport·basic·editor·모듈몰만 확인) |

### D-3. 키트 주장 vs 공식 (Easy 경계)

| ID | 키트 주장 (SKILL·AGENT·MCP) | 공식 대조 (2026-06-19) | 판정 |
|----|----------------------------|------------------------|------|
| D-3a | HTML: `/skin1/`, `/mobile/` … | API: `skin_code`=디자인 코드, pages `path`=파일 경로. **`/skinN` 패턴 문장 없음** | ⚠️ 실무·MCP (`skin_code`→`/skin14`) — Phase 1-E |
| D-3b | Easy: `/sde_design/base/`, `mobile/` | developers·Admin API **본문 0건** | ⚠️ SKILL·프로젝트 실측만 — **공식 인용 없음** |
| D-3c | Easy: **SFTP 불가**, 관리자 에디터만 | 공식 **0건**. **2026-06-19 paransky97: E 스킨도 /{skin_code} SFTP OK** | ⚠️ 「불가」폐기 → 「API editor_type와 SFTP 접근 별개·실측 접근 가능」 |
| D-3d | HTML: SFTP 가능 | 공식 **0건** (디자인 SFTP와 `editor_type` 연결 문장 없음) | ⚠️ Phase 1-A 실측+내부 가이드와 합쳐서만 성립 |
| D-3e | `data-ez-*`, `ez-prop`, `ez-var` — Easy 전용 | sdsupport basic·editor·소개 페이지 **0건** | ⚠️ SKILL·AGENT 실무 |
| D-3f | HTML ↔ Easy **상호 편집 불가** | 공식 **0건** | ⚠️ |
| D-3g | EZ 스킨에서도 장바구니 등은 `module=""` **하이브리드** | 공식 **0건** | ⚠️ AGENT §0 실무 해석 |
| D-3h | 작업 전 `list_themes` → `editor_type` 확인 | API 필드 존재 + MCP `cafe24_list_themes` | ✅ API / ⚠️ 키트 **슬래시 명령으로 강제 안 함** |

### D-4. 키트·MCP 결함 (Easy 관련)

| ID | 문제 | 위치 | 판정 |
|----|------|------|------|
| D-4a | Easy 핵심 주장(SFTP·경로·data-ez)이 **공식 링크 없이** ✅처럼 읽힘 | `SKILL.md` §0·§5 | ⚠️ 「실무」라벨·AUDIT 링크 필요 |
| D-4b | MCP docstring: `E`=Easy, `H`=HTML **「FTP 가능」** | `mcp/server.py`, `cafe24_api.py` | ⚠️ **editor_type와 FTP 연결은 공식 미확인** |
| D-4c | `editor_type` D/W/C **무시** — 잘못된 스킨 유형 오판 위험 | SKILL·AGENT | ⚠️ |
| D-4d | CLAUDE 「EZ 걷어내기」가 기본 전략 — Easy 몰에 **무조건** 적용하면 위험 | `CLAUDE.md` L64·L82 | ⚠️ 사용자 의도·editor_type 확인 선행 필요 |
| D-4e | developers에 Easy 가이드 없음 → 에이전트가 SKILL만 「공식」처럼 인용할 위험 | 구조 | ❌ Phase 2에서 「공식/실무」게이트 강화 |

### D-5. 에이전트 규칙 초안 (Easy·HTML 작업 시)

1. **먼저 API:** `cafe24_list_themes` 또는 Themes API로 `editor_type`·`skin_code` 확인. **H가 아니면** HTML/SFTP 워크플로우를 **자동 적용하지 말 것**.
2. **말하기 규칙:** `data-ez-*`, `/sde_design`, Easy SFTP 불가, HTML↔Easy 호환 — **「카페24 실무·프로젝트 검증」**이라고만 말한다. 공식 URL 생기기 전까지 ✅ 금지.
3. **공식으로 할 수 있는 것:** HTML 스마트디자인은 [editor 가이드](https://developers.cafe24.com/design/front/smart/sdsupport/editor)대로 **관리자 편집창·HTML 보기·모듈** 안내.
4. **Easy 몰에서 EZ 제거:** 사용자가 **의도적으로 HTML 전환**을 요청했을 때만 — `strip_ez` 등 (Phase 4 워크플로우).

### D-6. Phase 1-D 보완 작업 (미해결)

- [ ] **P1D-1** 스마트디자인Easy 공식 매뉴얼 URL (관리자 도움말·ecsupport 본문 — 현재 검색 페이지만 수집)
- [ ] **P1D-2** `sde_design` 경로 공식 출처
- [ ] **P1D-3** `editor_type`별 디자인 FTP/SFTP 허용 여부 공식 표
- [ ] **P1D-4** `data-ez-module` 등 EZ 속성 레퍼런스 (Web Components 가이드와의 관계 여부)

---

## Phase 1-E. skin_no · skin_code · SFTP 폴더 매핑

> **비유:** 쇼핑몰 디자인에는 **주민등록번호(`skin_no`)** 와 **집 주소 이름(`skin_code`, 예: skin14)** 이 따로 있다. API 전화는 주민번호로 걸고, SFTP 택배는 **주소 이름**으로 보낸다. **14번 집 주소에 16번 주민이 사는 것처럼** 번호와 폴더 숫자가 안 맞을 수 있다 — 그래서 **항상 `list_themes`로 표를 먼저 본다.**

### E-1. 공식 필드 (Themes API)

| ID | 필드 | 공식 의미 | 판정 |
|----|------|-----------|------|
| E-1a | `skin_no` | 디자인 번호 (정수, API 경로에 사용) | ✅ |
| E-1b | `skin_code` | 디자인 코드 (문자열) | ✅ |
| E-1c | `skin_name` | 디자인명 | ✅ |
| E-1d | `usage_type` | S/C/I=PC, M/N=모바일 (기본·복사·상속) | ✅ |
| E-1e | `editor_type` | H/E/D/W/C (§D-1) | ✅ |
| E-1f | `published_in` | 대표디자인으로 쓰는 멀티쇼핑몰 번호 | ✅ |
| E-1g | `skin_lock` | T=잠금, F=해제 | ✅ |
| E-1h | `parent_skin_no` | 부모 디자인 번호 (복사·상속 추적) | ✅ |
| E-1i | GET `themes?type=` | `pc` \| `mobile` (기본 pc) | ✅ |
| E-1j | `design_type` | — | ❌ **MCP가 반환하지만 Themes property list에 없음** (`cafe24_api.py` L85) |

### E-2. API ↔ SFTP 연결 (핵심 다리)

| ID | 규칙 | 근거 | 판정 |
|----|------|------|------|
| E-2a | **`skin_code` → SFTP 루트 `/{skin_code}`** (예: `skin14` → `/skin14`) | 2026-06-10 paransky97 라이브: `list_themes` + `sftp ls` 교차 (`mcp/README.md`) | ⚠️ **실측 확정, 공식 문장 0건** |
| E-2b | **`skin_no` ≠ 폴더 이름의 숫자** (예: skin_no **16**, skin_code **skin14**, SFTP **/skin14**) | 동일 실측 표 | ⚠️ 함정 — 초보자가 「14번 스킨」이라고 skin_no=14로 착각하기 쉬움 |
| E-2c | API `read_page(skin_no, path)` 의 `path`는 **스킨 루트 기준** (예: `/layout/basic/layout.html`) | Themes pages: path=파일 경로; MCP `read_page` 구현 | ✅ API path 정의 / ⚠️ `skin_code`를 path에 넣지 않음 |
| E-2d | CSS·이미지 등 **에셋**은 API pages가 **422** → SFTP `read` 필요 | MCP README §핵심 발견 #2 (2026-06-10) | ⚠️ 실측 — 공식 「422」문장은 본 Phase 미인용 |
| E-2e | PC 목록 vs 모바일 목록 | `GET /themes?type=pc` / `type=mobile` | ✅ — 모바일 SFTP `/mobile` 과 **이름만으로 1:1 연결은 공식 없음** |

### E-3. 실측 SFTP 루트 구조 (HTML 몰, paransky97)

| SFTP 경로 | 대응 API (실측) | 키트 역할 주장 | 판정 |
|-----------|-----------------|----------------|------|
| `/skin14` | skin_no=16, skin_code=skin14 | 작업 스킨 (`_nk` 등) | ⚠️ 실측 1몰 |
| `/skin2` | skin_no=4 | IDIO 원본·보호 | ⚠️ |
| `/base` | skin_no=1 | fallback·**수정 금지** | ⚠️ SKILL §4 — **API·공식 폴더 문서 0건** |
| `/mobile` | (mobile type 목록 별도) | 모바일 스킨 | ⚠️ |
| `/skin15`, `/web` | README·SKILL에 언급 | 보호·업로드물 | ⚠️ 몰마다 다름 |

### E-4. 「지금 쇼핑몰에 켜진 디자인」찾기

| ID | 방법 | 판정 |
|----|------|------|
| E-4a | Shops API `skin_no` = **PC 대표 디자인 번호** (현재 사용 중) | ✅ |
| E-4b | Shops API `mobile_skin_no` = **모바일 대표 디자인 번호** | ✅ |
| E-4c | `published_in` + `skin_lock`으로 보관함·잠금 상태 교차 | ✅ 필드 / ⚠️ UI 경로는 관리자 매뉴 미수집 |

### E-5. editor_type 과 폴더 (Phase 1-D 연계)

| editor_type | SFTP 작업 (키트/MCP 가정) | 판정 |
|-------------|---------------------------|------|
| **H** (HTML) | `skin_code` 폴더 SFTP — 실측 다수 | ⚠️ H→SFTP 공식 연결 없음 |
| **E** (Easy) | `/sde_design/...` (SKILL) — SFTP 불가 주장 | ⚠️ §D — 공식 0건 |
| **D/W/C** | 키트 **미정의** | ❌ 오판 위험 |

### E-6. 키트·MCP 결함

| ID | 문제 | 위치 | 판정 |
|----|------|------|------|
| E-6a | `skin_code`=SFTP 폴더를 **공식처럼** 서술 | `mcp/README.md`, `server.py`, `cafe24_api.py` | ⚠️ → 「2026-06-10 실측」라벨·AUDIT 링크 필요 |
| E-6b | `design_type` 필드 노출 | `cafe24_api.py` | ✅ **제거됨** (2026-06-19) |
| E-6c | CLAUDE 게이트 #3은 맞지만 **확인 절차(핑퐁) 없음** | `CLAUDE.md` L28 | ⚠️ Phase 4 `/접속세팅`에서 대본화 |
| E-6d | `modules.md`·307종 모듈 인덱스와 skin 경로 동기화 미검 | `references/` | ⚠️ Phase 1-F 또는 별도 |

### E-7. 에이전트 작업 순서 (확정 초안)

```
1. cafe24_list_themes (또는 GET /themes?type=pc 와 mobile 각각)
2. 표 작성: skin_no | skin_code | skin_name | editor_type | usage_type
3. 작업 대상 skin_code 선택 → SFTP 경로 = "/" + skin_code
4. HTML 정본: cafe24_read_page(skin_no, "/layout/basic/layout.html")
5. CSS/JS/이미지: cafe24_sftp_read("/{skin_code}/...")
6. 쓰기 전: skin_no·skin_code·SFTP 경로 세 개를 사용자에게 읽어 확인
```

### E-8. Phase 1-E 보완 (미해결)

- [ ] **P1E-1** Admin API 응답 예시 JSON에 `skin_code` 실제 값 샘플 (공식 Response Copy 섹션)
- [ ] **P1E-2** `base/` fallback 규칙 공식 출처 (없으면 실무 라벨 유지)
- [ ] **P1E-3** Easy 스킨의 API `skin_code` 값과 SFTP 노출 여부 실측 1건
- [ ] **P1E-4** MCP `design_type` 필드 정리 — ✅ 제거 완료 (2026-06-19)

---

## Phase 1-F. 풀 감사 마무리 · 키트 인프라 갭 해소

**갱신:** Phase 2~7 (2026-06-19) — getting-started, MCP 가이드, OMC 명령, measure-first, CLAUDE 게이트

### F-1. 감사 Phase 완료 체크

| Phase | 주제 | 산출물 | 상태 |
|-------|------|--------|------|
| 1-A | FTP·몰ID | §A | ✅ |
| 1-B | OAuth | §B | ✅ |
| 1-C | HTML·F함정 | §C, traps/INDEX | ✅ |
| 1-D | Easy vs HTML | §D | ✅ |
| 1-E | skin 매핑 | §E | ✅ |
| 1-F | 마무리 | §F, phase-1f-summary | ✅ |

### F-2. 인프라 문서 (이번에 추가)

| ID | 산출물 | 역할 | 판정 |
|----|--------|------|------|
| F-2a | `getting-started/00`~`05` | 파트너/일반 분기, 몰ID, MCP 개요 | ✅ 구조 완료 — 파트너 호스트 등 ⚠️ 라벨 유지 |
| F-2b | `docs/MCP-OAUTH-GUIDE.md` | OAuth 핑퐁·read_design | ✅ 공식 순서 반영 |
| F-2c | `commands/COMMANDS.md` + `.claude/commands/` 5+4별칭 | OMC 대본 | ✅ |
| F-2d | `workflows/04-measure-first.md` | 실측 우선 | ✅ |
| F-2e | `CLAUDE.md` 게이트 0~6 | 파트너·editor_type·실측 | ✅ |
| F-2f | `scripts/verify-kit.sh` | 자동 검증 | ✅ |

### F-3. 미해결 백로그 (차단 아님)

- P1A-1~4, P1D-1~4, P1E-1~3 — 공식 URL·Easy SFTP 실측 추가 시 AUDIT 갱신
- P1E-4 MCP `design_type` — **제거 완료** (2026-06-19)

### F-4. 에이전트 진입 경로 (확정)

```
/도움말 → getting-started
/접속세팅 → 환경
/API발급 → MCP
/요소측정 → 실측
/디자인수정 → 코드
```

---

## Phase G. 라이브 검증 (2026-06-19, paransky97)

근거: [`docs/VERIFICATION-EVIDENCE.md`](VERIFICATION-EVIDENCE.md)

### G-1. smoke_test

| 환경 | 결과 |
|------|------|
| OneDrive `web/cafe24/mcp` | **5/5 PASS** |
| workspace `mcp/` (업graded code) | **5/5 PASS** (SFTP 35s 쿨다운 후) |

Scope: `mall.read_design` ✅

### G-2. skin_code ↔ SFTP (6/6)

| skin_no | skin_code | editor_type | SFTP |
|---------|-----------|-------------|------|
| 19 | skin17 | E | OK |
| 18 | skin16 | H | OK |
| 17 | skin15 | H | OK |
| 16 | skin14 | E | OK |
| 4 | skin2 | H | OK |
| 1 | base | E | OK |

### G-3. Easy 주장 수정 (라이브)

| ID | 이전 | 라이브 후 |
|----|------|-----------|
| G-3a | Easy SFTP 불가 | ⚠️ **E 스킨도 SFTP list/read 가능** (정책상 비권장일 수 있으나 기술적 차단 아님) |
| G-3b | `/sde_design` | paransky97 SFTP **루트에 없음** |
| G-3c | skin14=HTML 작업본 | **editor_type=E** (2026-06-19) — 매 작업 `list_themes` 필수 |

---

## Phase 1-A에서 확정한 에이전트 규칙 (문서 반영 전 초안)

1. **먼저 질문:** 「파트너센터 샘플몰인가요, 일반 운영 몰인가요?」
2. **몰 ID:** 사용자에게 쇼핑몰 URL 요청 → 앞부분 추출 (API는 `{몰ID}.cafe24api.com`으로 교차 확인).
3. **호스트·포트:** 문서에 적힌 예시를 **절대 기본값으로 쓰지 말 것.** 관리자/발급 SFTP 정보 또는 `sftp_{mall}.json`만 신뢰.
4. **파트너 웹 FTP vs 디자인 SFTP:** 배포판 getting-started 논리를 따르되, Phase 1-A 보완까지 공식 파트너 문서 링크를 AUDIT에 채운 뒤 `getting-started`에 옮긴다.

---

## 미해결 · Phase 1-A 보완 작업

- [ ] **P1A-1** 파트너센터 공식 문서에서 웹 FTP 호스트·계정 규칙 인용 확보 (`partners.cafe24.com` 또는 developers 파트너 가이드)
- [ ] **P1A-2** 관리자 「디자인 FTP 권한 신청」공식 매뉴얼 URL·스크린샷 경로
- [ ] **P1A-3** `{몰ID}.cafe24.com` 쇼핑 URL 규칙 공식 출처 (없으면 「관례」로 라벨 유지)
- [ ] **P1A-4** `ecimg-ftp-*.cafe24img.com` 호스트가 어떤 계정 유형인지 공식 분류

---

## 참고 파일 (이 워크스페이스)

| 파일 | 내용 |
|------|------|
| `docs/VERIFICATION-EVIDENCE.md` | smoke 5/5·skin 매핑 라이브 (2026-06-19) |
| `docs/_evidence/phase-1a-api-quotes.txt` | Admin API (FTP·Themes·OAuth) |
| `docs/_evidence/phase-1b-api-quotes.txt` | OAuth·앱 등록 |
| `docs/_evidence/phase-1c-api-quotes.txt` | 스마트디자인 basic·module 목록 인용 |
| `docs/_evidence/phase-1d-api-quotes.txt` | editor_type·HTML 편집창·Easy 미수집 목록 |
| `docs/_evidence/phase-1e-api-quotes.txt` | skin_no/skin_code·themes·shops·실측 매핑표 |
| `docs/_evidence/p1d_admin_api.html` | Admin API 전체 스크랩 (재검증) |
| `docs/_evidence/sds1d_design_front_smart_sdsupport_editor.html` | 편집창 가이드 원본 |
| `traps/INDEX.md` | F1~F26 한 줄 인덱스 + 출처 등급 |
| `docs/_evidence/dev_*.html` | Phase 1-B scrape 원본 (재검증용) |
| `../MANIFEST.txt` | 복제 정책 |
| (원본 참고) `키트-배포판/getting-started/00-아무것도-모를-때.md` | FTP 분기 초안 (공식 대조 전) |
