# DEEPINIT-MAP — cafe24-agent-kit AI 구조 지도

- 기준일: 2026-07-10
- 기준 버전: `v2.10.0` (`VERSION` = 2026-07-09)
- 정본 루트: `C:\nookitokki\cafe24-agent-kit`
- 이 문서 위치: `C:\nookitokki\cafe24-agent-kit\agent-kit\brain\docs\DEEPINIT-MAP.md`
- 성격: `/deepinit` 스타일의 **AI-readable map**. `AGENTS.md` 계층을 생성하거나 수정하지 않는다.

## 0. 에이전트용 최상위 판단 규칙

### 먼저 읽을 순서

1. `C:\nookitokki\cafe24-agent-kit\README.md` — 저장소 진입점.
2. `C:\nookitokki\cafe24-agent-kit\agent-kit\README.md` — 키트 본체 지도.
3. 이 문서 — 어느 영역을 건드려도 되는지 확인.
4. 실제 작업 영역의 원문 문서/스크립트 — 이 지도만 보고 수정하지 말 것.

### Domain A / Domain B 경계

| 분류 | 의미 | 예시 | 에이전트 행동 |
|---|---|---|---|
| Domain A | 로컬 파일·되돌릴 수 있는 kit 빌드 작업 | 문서 갱신, evaluator/검증기, `_verified-template/src` in-place 개선, `.omc` scratch, source verify | 자율 실행 가능. 단, 수정 파일 범위를 좁히고 targeted verification만 수행 |
| Domain B | 외부 side-effect 또는 불가역 작업 | live Cafe24 SFTP upload, Cafe24 API write, OAuth 연결, live mall 설정 변경, `create_product`, git push, release/deploy, 공개 배포 | 즉시 HALT. 대표님 명시 승인 없이는 실행 금지 |

**핵심:** 이 repo에는 Domain B 기능을 호출할 수 있는 도구와 스크립트가 존재한다. 존재 자체가 실행 허가가 아니다. `put`, `cafe24_sftp_upload`, `product-create`, OAuth `auth-url/code`, `release-github.sh`, git push 계열은 모두 승인 게이트가 필요하다.

### 절대 혼동하지 말 것

- `C:\nookitokki\cafe24-agent-kit\agent-kit\clients\_verified-template\`는 검증 템플릿 정본이다. 일반 클라이언트 작업은 이 폴더를 직접 고치지 말고 복사본에서 해야 한다. ralplan Domain A의 P4처럼 명시된 승격 작업일 때만 `src` in-place 편집이 허용된다.
- `C:\nookitokki\cafe24-agent-kit\mcp\config\`에는 실제 토큰·SFTP JSON이 생길 수 있는 영역이다. example과 loader 외의 비밀 파일은 문서화·출력·커밋 대상이 아니다.
- `C:\nookitokki\cafe24-agent-kit\agent-kit\brain\_evidence\`는 근거 원본/캐시 성격이며 build script에서 dist 제외된다. 공개 배포 문서처럼 다루지 않는다.
- root `.claude/skills`와 `.claude/agents`가 현재 Claude Code 인식 위치다. `agent-kit/.claude`는 오래된 중첩 위치로 남아 있을 수 있으나 현재 배포 기준은 root `.claude`다.

---

## 1. Root files — 저장소 진입점과 배포 메타

**Purpose**

`C:\nookitokki\cafe24-agent-kit` 루트는 배포 키트의 실제 source root다. 비개발자 사용자는 root README에서 시작하고, 개발/배포 작업자는 root scripts와 mcp, agent-kit 본체를 함께 본다.

**Key files**

| 절대 경로 | 역할 |
|---|---|
| `C:\nookitokki\cafe24-agent-kit\README.md` | 사용자 진입점. `/키트시작`, 설치 안내, `agent-kit/`와 `mcp/`의 큰 구조를 안내 |
| `C:\nookitokki\cafe24-agent-kit\agent-kit\README.md` | 키트 본체 지도. 명령어, 폴더맵, `_verified-template` 사용법, v2.4+ 확장 자료 안내 |
| `C:\nookitokki\cafe24-agent-kit\CHANGELOG.md` | 릴리스/변경 이력. v2.10.0은 `nk-stock.css`와 `_verified-template` 32파일 확장 기록 |
| `C:\nookitokki\cafe24-agent-kit\VERSION` | 현재 버전/날짜. `kit-version`, build-dist가 참조 |
| `C:\nookitokki\cafe24-agent-kit\package.json` | devDependency로 Playwright만 보유. 시각/브라우저 검증 보조 성격 |
| `C:\nookitokki\cafe24-agent-kit\PURPOSE.md` | 개발 repo 전용 설계 원칙. 배포본에는 미포함이라고 README가 안내 |
| `C:\nookitokki\cafe24-agent-kit\.mcp.json.example`, `.mcp.json.mac.example` | Claude Code MCP 등록 템플릿 |
| `C:\nookitokki\cafe24-agent-kit\.cursor\mcp.json.example`, `.cursor\mcp.json.mac.example` | Cursor MCP 등록 템플릿 |

**Agent working notes**

- 사용자용 진입 문구는 root `README.md`, 키트 내부 안내는 `agent-kit/README.md`에 둔다.
- 배포본에 들어가는 안내를 바꾸면 `scripts/build-dist-kit.sh`의 copy 대상과 `scripts/verify-kit.sh`의 검증 기대를 함께 확인한다.
- 버전 변경은 `VERSION` + `CHANGELOG.md` + 관련 README의 상호 정합이 필요하다. 단, 이 문서 작성 업무에서는 버전 변경이 목표가 아니다.
- root `AGENTS.md`는 이 작업의 non-goal이다. 이 문서는 AGENTS hierarchy를 대신 생성하지 않는다.

**Verification notes**

- source 구조 검증: `bash agent-kit/connect/scripts/verify-kit.sh`
- dist 생성 후 검증: `bash scripts/build-dist-kit.sh` → `bash scripts/verify-kit.sh`
- root verify는 `dist/cafe24-agent-kit`이 없으면 실패/skip 안내가 난다. source만 확인할 때는 `agent-kit/connect/scripts/verify-kit.sh`가 맞다.

---

## 2. `mcp/` — Cafe24 연결 손발

**Purpose**

`C:\nookitokki\cafe24-agent-kit\mcp`는 카페24 Admin API, SFTP/FTP, OAuth, MCP 서버를 실제로 연결하는 손발 모듈이다. `agent-kit/`가 두뇌와 가이드라면 `mcp/`는 외부 몰을 읽고, 승인된 경우 파일을 백업/업로드할 수 있는 실행 계층이다.

**Key files and directories**

| 절대 경로 | 역할 |
|---|---|
| `C:\nookitokki\cafe24-agent-kit\mcp\README.md` | MCP 도구 8종+kit guide/preflight, CLI 사용법, OAuth/SFTP 보안 규칙 정리 |
| `C:\nookitokki\cafe24-agent-kit\mcp\server.py` | FastMCP stdio 서버 진입점. `.mcp.json`에서 호출되는 런타임 |
| `C:\nookitokki\cafe24-agent-kit\mcp\cli.py` | 로컬 손 테스트 CLI. `status`, `themes`, `page`, `ls`, `cat`, `get`, `backup`, `put`, `kit-*` 명령을 제공 |
| `C:\nookitokki\cafe24-agent-kit\mcp\kit_tools.py` | `diagnose`, `scaffold`, `kit-version`, `kit-update`, `kit-autoupdate` 등 kit 자체 관리 기능 |
| `C:\nookitokki\cafe24-agent-kit\mcp\smoke_test.py` | MCP 서버/도구 smoke test |
| `C:\nookitokki\cafe24-agent-kit\mcp\requirements.txt` | Python runtime dependency 목록 |
| `C:\nookitokki\cafe24-agent-kit\mcp\auth\oauth.py` | TokenManager, OAuth URL/code 교환, 토큰 만료/refresh 처리 |
| `C:\nookitokki\cafe24-agent-kit\mcp\backends\cafe24_api.py` | Admin API read/write wrapper. read-only 진단은 Domain A, write는 Domain B |
| `C:\nookitokki\cafe24-agent-kit\mcp\backends\cafe24_sftp.py` | SFTP list/read/download/backup/upload. upload는 Domain B 승인 게이트 |
| `C:\nookitokki\cafe24-agent-kit\mcp\backends\cafe24_ftp.py` | 파트너 웹 FTP port 21 backend |
| `C:\nookitokki\cafe24-agent-kit\mcp\config\cafe24_config.example.py` | 배포 가능한 설정 예시. 실제 `cafe24_config_{mall}.py`는 secret |
| `C:\nookitokki\cafe24-agent-kit\mcp\examples\products.example.json` | product API 테스트/예시 payload |
| `C:\nookitokki\cafe24-agent-kit\mcp\work\scripts\strip_ez.py` | EZ strip utility. dist에 포함되는 작업 보조 스크립트 |

**Agent working notes**

- CLI `product-create`는 실제 상품 생성 API를 호출한다. Domain B다. 자동 실행 금지.
- CLI `put` 및 MCP `cafe24_sftp_upload`는 운영 반영이다. 백업·화이트리스트가 있어도 Domain B다. 자동 실행 금지.
- `status`, `themes`, `page`, `ls`, `cat`, `get`, `backup`은 원칙적으로 진단/read/backup 성격이지만, OAuth 연결이 필요한 경우 token 발급 자체는 Domain B 승인 게이트다.
- `kit-*` 명령은 kit 로컬 관리 기능이다. `kit-update --from-github --apply`처럼 외부 다운로드/파일 갱신을 수반하면 범위를 명시하고 검증해야 한다.
- `mcp/config`의 실제 token/config/SFTP 파일명은 보고서나 채팅에 노출하지 않는다. example과 README만 공개 기준이다.

**Verification notes**

- dependency 설치 후 import: `cd mcp && python -c "import server"`
- 빠른 smoke: `cd mcp && python smoke_test.py`
- preflight 전체는 시간이 길 수 있다: `SMOKE_PREFLIGHT_ALL=1 python smoke_test.py`
- source verify는 `mcp/server.py`, `kit_tools.py`, `auth/oauth.py`, `backends/cafe24_sftp.py`, `config/cafe24_config.example.py` 존재와 import를 확인한다.

---

## 3. `scripts/` and `agent-kit/connect/scripts/` — build/verify/release 경계

**Purpose**

루트 `scripts/`는 개발 repo에서 dist bundle을 만들고 검사하는 도구다. `agent-kit/connect/scripts/`는 배포 키트 내부에서 source 구조와 연결 상태를 점검하는 사용자/에이전트용 verify 계층이다.

**Key files**

| 절대 경로 | 역할 | Domain |
|---|---|---|
| `C:\nookitokki\cafe24-agent-kit\scripts\build-dist-kit.sh` | `dist/cafe24-agent-kit` 생성. clients allowlist, mcp secret 제외, root `.claude` 포함, sanity check 수행 | Domain A, 로컬 build |
| `C:\nookitokki\cafe24-agent-kit\scripts\verify-kit.sh` | dist bundle 동작/보안 검증. Python import, JSON parse, secret leak, token vocab drift, `_verified-template` 중립성 검사 | Domain A, 로컬 verify |
| `C:\nookitokki\cafe24-agent-kit\scripts\release-github.sh` | GitHub release 보조 스크립트 | Domain B, 승인 전 실행 금지 |
| `C:\nookitokki\cafe24-agent-kit\agent-kit\connect\scripts\verify-kit.sh` | source kit 구조·보안·mcp import 검증. P0 hotfix 대상이었던 source verify | Domain A |
| `C:\nookitokki\cafe24-agent-kit\agent-kit\connect\scripts\verify-live.sh` | live 확인 계열로 보이는 스크립트. 실제 외부 호출 가능성 때문에 실행 전 범위 확인 필요 | Domain B 가능성 있음 |
| `C:\nookitokki\cafe24-agent-kit\agent-kit\connect\scripts\verify-partner-live.sh` | 파트너 live 확인 계열. 외부 호출 가능성 때문에 자동 실행 금지 | Domain B 가능성 있음 |

**Agent working notes**

- `build-dist-kit.sh`의 배포 clients allowlist는 `_template`, `demo000`, `_verified-template`이다. 실 클라이언트 폴더가 dist에 들어가면 실패다.
- `build-dist-kit.sh`는 `agent-kit/brain/_evidence`와 `_핸드오프_*`를 dist에서 제외한다.
- `scripts/verify-kit.sh`는 dist가 있어야 의미 있다. source만 고친 뒤 dist를 만들지 않았다면 `agent-kit/connect/scripts/verify-kit.sh`로 확인한다.
- release script, git push, deploy, public distribution은 Domain B다. 계획서에 있더라도 별도 승인 없이는 실행하지 않는다.

**Verification notes**

- 현재 Domain A 최저 검증: `bash agent-kit/connect/scripts/verify-kit.sh`
- dist artifact 변경까지 포함한 경우: `bash scripts/build-dist-kit.sh` 후 `bash scripts/verify-kit.sh`
- live verify류는 “검증”이라는 이름이어도 외부 몰에 접속할 수 있다. 자동 실행하지 말고 command 내용을 먼저 읽는다.

---

## 4. Root `.claude/skills/` — 슬래시 명령과 전문 지식

**Purpose**

`C:\nookitokki\cafe24-agent-kit\.claude\skills`는 Claude Code가 workspace root에서 인식하는 슬래시 스킬 정본이다. v2.6.0 이후 모든 slash command가 root `.claude/skills`로 이동했다.

**Major skill groups**

| 절대 경로 | 역할 |
|---|---|
| `C:\nookitokki\cafe24-agent-kit\.claude\skills\cafe24\SKILL.md` | 카페24 SmartDesign core guide. 변수, 모듈, 지시어, EZ/HTML 경계, 작업 전 준비물 3종 세트 |
| `C:\nookitokki\cafe24-agent-kit\.claude\skills\cafe24\references\` | `variables.md`, `modifiers.md`, `modules.md`, `module-remarkup.md`, `troubleshooting.md`, `skin-method-detect.md` 등 검증 기준/사전 |
| `C:\nookitokki\cafe24-agent-kit\.claude\skills\cafe24\snippets\` | `_nk` HTML/CSS/JS 조각. 검증된 `nk-` prefix 조각을 복사/적용하는 영역 |
| `C:\nookitokki\cafe24-agent-kit\.claude\skills\cafe24\design-tokens\` | Figma/레퍼런스 값을 `nk-tokens.css`로 정리하는 token pipeline |
| `C:\nookitokki\cafe24-agent-kit\.claude\skills\cafe24\component-gallery\` | 버튼·폼·카드 등 완성 부품 gallery |
| `C:\nookitokki\cafe24-agent-kit\.claude\skills\cafe24\brand-profile\` | 클라이언트별 tone/order sheet 성격의 JSON profile |
| `C:\nookitokki\cafe24-agent-kit\.claude\skills\cafe24\workflows\cafe24-automation.md` | `/카페24-자동화` 실험적 6단계 pipeline |
| `C:\nookitokki\cafe24-agent-kit\.claude\skills\cafe24-greenfield-skin\` | 신규 몰/전체 페이지 재구축 오케스트레이션, audit scripts, wave templates |
| `C:\nookitokki\cafe24-agent-kit\.claude\skills\키트시작\SKILL.md` | 첫 실행, auto-update check, Python/MCP smoke |
| `C:\nookitokki\cafe24-agent-kit\.claude\skills\새클라이언트\SKILL.md` | `clients/_template` scaffold 안내 |
| `C:\nookitokki\cafe24-agent-kit\.claude\skills\MCP연결\SKILL.md` | Cursor/Claude Code MCP 등록 안내 |
| `C:\nookitokki\cafe24-agent-kit\.claude\skills\API발급\SKILL.md` | OAuth 발급 대본. 실제 OAuth 연결은 Domain B 게이트 |
| `C:\nookitokki\cafe24-agent-kit\.claude\skills\접속세팅\SKILL.md` | 일반몰/파트너몰, 몰 ID, SFTP path 세팅 질문 대본 |
| `C:\nookitokki\cafe24-agent-kit\.claude\skills\레퍼런스인입\SKILL.md` | 레퍼런스 URL/Figma 인입 전 질문 흐름 |
| `C:\nookitokki\cafe24-agent-kit\.claude\skills\요소측정\SKILL.md` | 폰트·여백·구조 실측 진입 |
| `C:\nookitokki\cafe24-agent-kit\.claude\skills\토대정리\SKILL.md` | base 함정 scan, reset, token 준비 C단계 |
| `C:\nookitokki\cafe24-agent-kit\.claude\skills\디자인수정\SKILL.md` | 실제 수정 전 게이트와 작업 순서 |
| `C:\nookitokki\cafe24-agent-kit\.claude\skills\검증\SKILL.md`, `qa-loop\SKILL.md` | 검증/QA loop 진입 |
| `C:\nookitokki\cafe24-agent-kit\.claude\skills\EZ제거\SKILL.md` | EZ strip 관련 질문 대본 |
| `C:\nookitokki\cafe24-agent-kit\.claude\skills\캐시확인\SKILL.md` | 업로드 후 캐시/반영 지연 확인 |
| `C:\nookitokki\cafe24-agent-kit\.claude\skills\도움말\SKILL.md`, `프롬프트참고\SKILL.md`, `버전확인\SKILL.md` | 사용자 안내/링크/버전 진단 |

**Agent working notes**

- skill 문서는 “대본 + 규칙”이다. 실제 skin HTML/CSS/JS 수정을 시작하기 전에 관련 skill과 reference를 먼저 읽는다.
- `cafe24/references/variables.md`가 카페24 변수 단일 기준이다. 일반 웹 쇼핑몰 변수처럼 보이는 미검증 변수는 재유입 금지다.
- snippets는 안정/실험 상태가 섞여 있다. `agent-kit/README.md` 기준으로 즉시 사용 권장과 실험적 자료를 구분한다.
- `cafe24-greenfield-skin`은 대규모 신규/전 페이지 재구축 계열이다. 단일 quick fix에 끌어오면 과잉이다.
- `API발급`, `MCP연결`, `접속세팅`은 외부 계정/토큰으로 넘어갈 수 있다. 안내는 가능하지만 실제 OAuth 연결·토큰 발급은 Domain B 승인 필요.

**Verification notes**

- skill 구조가 배포본에 들어가는지는 `scripts/build-dist-kit.sh` required list와 `scripts/verify-kit.sh`에서 확인된다.
- snippets/variables 변경 시 `agent-kit/connect/scripts/verify-kit.sh`의 fake variable denylist와 `scripts/verify-kit.sh`의 drift guard를 통과해야 한다.
- skill frontmatter/trigger 변경은 root에서 slash command 인식이 깨질 수 있으므로 작은 수정 후 실제 workspace 인식 또는 dist verify가 필요하다.

---

## 5. Root `.claude/agents/` — 역할 분리 검증자와 지휘자

**Purpose**

`C:\nookitokki\cafe24-agent-kit\.claude\agents`는 카페24 작업 전용 subagent 정의다. code 작성, 시각 QA, 워크플로우 지휘, 초보자 안내를 분리해 자가승인과 역할 혼선을 줄인다.

**Agents**

| 절대 경로 | 역할 | 작업 노트 |
|---|---|---|
| `C:\nookitokki\cafe24-agent-kit\.claude\agents\카페24-도우미.md` | 처음/막힘 사용자용 친절 통역·진단. 직접 코드 작업 금지 | 5줄 이내 안내, F1~F5 중심, 본격 작업은 main/전문 agent로 넘김 |
| `C:\nookitokki\cafe24-agent-kit\.claude\agents\카페24-워크플로우.md` | workflow 지휘자. 단계 게이트, `.workflow.md`, 재진입 관리 | 직접 코드 작업보다 단계 순서와 검증 게이트 관리가 핵심 |
| `C:\nookitokki\cafe24-agent-kit\.claude\agents\qa-checker.md` | visual QA 전담. screenshot pixel만 평가 | 코드/클래스/line 추측 금지. PC+mobile, aggregate ≥ 0.85 기준 |
| `C:\nookitokki\cafe24-agent-kit\.claude\agents\code-reviewer.md` | 코드 규칙/함정 리뷰 전담 | `nk-`, scope, inline style, token, module/variable, `@css` path 등 code-level 검증 |

**Agent working notes**

- `qa-checker`와 `code-reviewer`는 서로 다른 축이다. 시각 PASS가 코드 PASS를 의미하지 않고, 코드 PASS가 시각 PASS를 의미하지 않는다.
- `카페24-워크플로우`는 “직접 작업자”가 아니라 gatekeeper다. 작업 본문은 main/executor 계열이 수행하고, 이 agent는 상태·검증·재진입을 관리한다.
- `카페24-도우미`는 초보자 UX를 위한 안내자다. 실제 파일 수정까지 맡기면 역할 위반이다.

**Verification notes**

- 코드 수정 직후: `code-reviewer` 관점의 규칙을 반드시 통과해야 한다.
- 디자인/레퍼런스 구현 직후: `qa-checker` 관점의 PC/mobile screenshot 비교가 필요하다.
- workflow 진행: `.workflow.md` 상태 기록과 단계별 완료 기준 충족이 verification evidence다.

---

## 6. `agent-kit/01_작업하기/workflows/` — 작업 순서의 정본

**Purpose**

`C:\nookitokki\cafe24-agent-kit\agent-kit\01_작업하기\workflows`는 작업 흐름을 강제하는 정의 모음이다. 비개발자 수강생이 “무엇부터, 어디서 멈추고, 어떻게 검증하는지”를 잃지 않게 하는 단계표다.

**Workflow files**

| 절대 경로 | 사용 시점 | 요약 |
|---|---|---|
| `C:\nookitokki\cafe24-agent-kit\agent-kit\01_작업하기\workflows\README.md` | workflow 진입 전 | 9종 workflow 목록과 권장 순서 |
| `C:\nookitokki\cafe24-agent-kit\agent-kit\01_작업하기\workflows\01-quick-fix.md` | 색·텍스트·이미지 등 단일 변경 | 3단계 빠른 수정 |
| `C:\nookitokki\cafe24-agent-kit\agent-kit\01_작업하기\workflows\02-skin-build-standard.md` | 메인 리뉴얼·스킨 빌드 | 6단계 표준 |
| `C:\nookitokki\cafe24-agent-kit\agent-kit\01_작업하기\workflows\03-reference-renewal.md` | 레퍼런스/시안 1:1 구현 | 8단계 reference renewal |
| `C:\nookitokki\cafe24-agent-kit\agent-kit\01_작업하기\workflows\04-measure-first.md` | 수정 전 실측 | 폰트·여백·구조를 먼저 재는 흐름 |
| `C:\nookitokki\cafe24-agent-kit\agent-kit\01_작업하기\workflows\05-reference-intake.md` | 구현 전 URL/Figma/시안 인입 | 레퍼런스와 타겟 구조 격차 기록 |
| `C:\nookitokki\cafe24-agent-kit\agent-kit\01_작업하기\workflows\06-verify-loop.md` | 구현 중 반복 검증 | Phase별 score=100 only 자기검증 루프 |
| `C:\nookitokki\cafe24-agent-kit\agent-kit\01_작업하기\workflows\07-ez-on-legacy-setup.md` | 레거시 SmartDesign + EZ 초기 세팅 | EZ/HTML 경계 판정과 초기 핑퐁 |
| `C:\nookitokki\cafe24-agent-kit\agent-kit\01_작업하기\workflows\08-ez-three-step-pingpong.md` | HTML → EZ overlay → 선별 제거 | 압축 3단계 핑퐁 |
| `C:\nookitokki\cafe24-agent-kit\agent-kit\01_작업하기\workflows\09-full-renewal.md` | A-to-Z 전체 페이지 개편 | 전체 페이지 유형별 재마크업/재스타일/JS재구축 |

**Agent working notes**

- 큰 작업은 바로 코드로 가지 말고 `05-reference-intake` → `04-measure-first` → 해당 구현 workflow → `06-verify-loop` 순서로 묶는다.
- `06-verify-loop`의 “100점 미만인데 완료 보고”는 F33 함정이다. 점수가 남으면 완료가 아니다.
- workflow 문서는 작업 순서의 정본이다. brain docs의 개념과 충돌하면 workflow README와 해당 workflow 원문을 우선 확인하고, 이후 brain docs를 정합화한다.
- `.workflow.md`는 클라이언트 작업 상태 파일이다. `_verified-template` 자체에는 일반 클라 작업 상태를 남기지 않는다.

**Verification notes**

- workflow 변경 시 최소한 `agent-kit/connect/scripts/verify-kit.sh`로 문서 존재/구조 검증을 통과해야 한다.
- 실제 skin 구현 workflow는 PC/mobile 시각 QA, code-reviewer 규칙 검증, Cafe24 module/variable 보존 검증이 별도로 필요하다.
- `verify-loop` 관련 변경은 관련 score script 또는 MCP `run_preflight` 문서와 용어가 맞아야 한다.

---

## 7. `agent-kit/02_막혔을때/` — troubleshooting hub

**Purpose**

`C:\nookitokki\cafe24-agent-kit\agent-kit\02_막혔을때`는 F코드 기반 문제 해결 허브다. 비개발자에게는 “증상→F번호→처방”을, 에이전트에게는 “원인→상세 문서→검증 루프”를 제공한다.

**Key files**

| 절대 경로 | 역할 |
|---|---|
| `C:\nookitokki\cafe24-agent-kit\agent-kit\02_막혔을때\F-상황-인덱스.md` | 작업자·에이전트 공용 허브. F27~F36, F3, F19 등 빠른 찾기와 관련 Q&A/프롬프트/상세 연결 |
| `C:\nookitokki\cafe24-agent-kit\agent-kit\02_막혔을때\함정-INDEX.md` | F1~F36 한 줄 인덱스. 등급과 공식 문서 링크 포함 |
| `C:\nookitokki\cafe24-agent-kit\agent-kit\02_막혔을때\common-pitfalls.md` | 실제 postmortem. EZ `#contents` 92%, PLP/PDP narrow 오판, basket/member/board/paginate 등 상세 |

**Agent working notes**

- 문제 보고를 받으면 먼저 증상을 F코드에 매핑한다. 원인을 모른 채 CSS를 덮어쓰지 않는다.
- F1~F26은 SmartDesign 문법/스킨 함정, F27~F34는 reference renewal/검증 postmortem, F35~F36은 Easy 타입 충돌·EZ 이식 함정이다.
- F27 `#container #contents` 92%는 모바일 full-bleed 실패의 대표 원인이다. 자식 `width:100vw`만 보면 안 되고 부모 computed width를 본다.
- F34는 관리자 모바일 전용 디자인 ON 문제다. 에이전트가 MCP로 끌 수 있는 문제가 아니다. 사용자/관리자 확인 게이트가 필요하다.

**Verification notes**

- troubleshooting 문서 수정 시 F번호가 `00_시작하기/QnA-쉬운말로.md`, `00_시작하기/프롬프트-템플릿.md`, `brain/rules/*`, workflow 문서의 링크와 일치해야 한다.
- `agent-kit/connect/scripts/verify-kit.sh`는 `common-pitfalls.md`, `F-상황-인덱스.md`, `함정-INDEX.md` 존재를 확인한다.
- F코드 추가/변경 시 “빠른 찾기”, “전체 마스터 표”, “초보자 Q&A/프롬프트”의 삼각 링크를 함께 점검한다.

---

## 8. `agent-kit/clients/_verified-template/` — 검증 템플릿 정본

**Purpose**

`C:\nookitokki\cafe24-agent-kit\agent-kit\clients\_verified-template`는 실제 카페24 데모몰 2곳에서 QA gate를 통과한 브랜드 중립 SmartDesign template이다. 새 몰을 빈 스킨에서 시작하지 않도록 검증된 토대(`src/` 45파일: HTML 27, CSS 16, JS 2)를 제공한다.

**Key files and structure**

| 절대 경로 | 역할 |
|---|---|
| `C:\nookitokki\cafe24-agent-kit\agent-kit\clients\_verified-template\README.md` | 비개발자용 설치 안내. FTP 업로드 순서, token 수정 위치, 주의사항 |
| `C:\nookitokki\cafe24-agent-kit\agent-kit\clients\_verified-template\CASE-STUDY.md` | 검증 근거. 데모몰 재현성, QA 통과, 중립화 요약 |
| `C:\nookitokki\cafe24-agent-kit\agent-kit\clients\_verified-template\src\index.html` | 스킨 root entry |
| `C:\nookitokki\cafe24-agent-kit\agent-kit\clients\_verified-template\src\layout\basic\layout.html` | 공용 layout. `@css`, `@import`, body class 등 핵심 spine |
| `C:\nookitokki\cafe24-agent-kit\agent-kit\clients\_verified-template\src\layout\basic\main.html` | main body |
| `C:\nookitokki\cafe24-agent-kit\agent-kit\clients\_verified-template\src\layout\basic\popup.html` | popup layout |
| `C:\nookitokki\cafe24-agent-kit\agent-kit\clients\_verified-template\src\product\list.html` | PLP |
| `C:\nookitokki\cafe24-agent-kit\agent-kit\clients\_verified-template\src\product\detail.html` | PDP |
| `C:\nookitokki\cafe24-agent-kit\agent-kit\clients\_verified-template\src\member\login.html`, `C:\nookitokki\cafe24-agent-kit\agent-kit\clients\_verified-template\src\member\join.html` | member pages |
| `C:\nookitokki\cafe24-agent-kit\agent-kit\clients\_verified-template\src\order\basket.html` | basket. 거래 흐름 보존 주의 |
| `C:\nookitokki\cafe24-agent-kit\agent-kit\clients\_verified-template\src\myshop\index.html` | myshop |
| `C:\nookitokki\cafe24-agent-kit\agent-kit\clients\_verified-template\src\board\free\list.html` | board list |
| `C:\nookitokki\cafe24-agent-kit\agent-kit\clients\_verified-template\src\_nk\css\nk-tokens.css` | 디자인 token 정본. 색·폰트·간격 변경의 1차 위치 |
| `C:\nookitokki\cafe24-agent-kit\agent-kit\clients\_verified-template\src\_nk\css\nk-cafe24-reset.css` | Cafe24 base 함정 완화 reset |
| `C:\nookitokki\cafe24-agent-kit\agent-kit\clients\_verified-template\src\_nk\css\nk-base.css`, `C:\nookitokki\cafe24-agent-kit\agent-kit\clients\_verified-template\src\_nk\css\nk-components.css` | 공용 base/component layer |
| `C:\nookitokki\cafe24-agent-kit\agent-kit\clients\_verified-template\src\_nk\css\nk-stock.css` | v2.10.0 stock page tone layer. HTML 무변경으로 stock 페이지 톤 통일 |
| `C:\nookitokki\cafe24-agent-kit\agent-kit\clients\_verified-template\src\_nk\css\nk-main.css`, `C:\nookitokki\cafe24-agent-kit\agent-kit\clients\_verified-template\src\_nk\css\nk-plp.css`, `C:\nookitokki\cafe24-agent-kit\agent-kit\clients\_verified-template\src\_nk\css\nk-pdp.css`, `C:\nookitokki\cafe24-agent-kit\agent-kit\clients\_verified-template\src\_nk\css\nk-member.css`, `C:\nookitokki\cafe24-agent-kit\agent-kit\clients\_verified-template\src\_nk\css\nk-order.css`, `C:\nookitokki\cafe24-agent-kit\agent-kit\clients\_verified-template\src\_nk\css\nk-board.css`, `C:\nookitokki\cafe24-agent-kit\agent-kit\clients\_verified-template\src\_nk\css\nk-myshop.css`, `C:\nookitokki\cafe24-agent-kit\agent-kit\clients\_verified-template\src\_nk\css\nk-popup.css`, `C:\nookitokki\cafe24-agent-kit\agent-kit\clients\_verified-template\src\_nk\css\nk-etc.css` | 페이지별 CSS |
| `C:\nookitokki\cafe24-agent-kit\agent-kit\clients\_verified-template\src\_nk\css\nk-orderform.css` | 미사용·보존 참고본. 주문서 HTML은 기본 stock 유지 |
| `C:\nookitokki\cafe24-agent-kit\agent-kit\clients\_verified-template\src\_nk\inc\nk-header.html`, `C:\nookitokki\cafe24-agent-kit\agent-kit\clients\_verified-template\src\_nk\inc\nk-footer.html`, `C:\nookitokki\cafe24-agent-kit\agent-kit\clients\_verified-template\src\_nk\inc\nk-layout-quick.html`, `C:\nookitokki\cafe24-agent-kit\agent-kit\clients\_verified-template\src\_nk\inc\nk-layout-overlays.html` | layout include fragments |
| `C:\nookitokki\cafe24-agent-kit\agent-kit\clients\_verified-template\src\_nk\js\nk-pdp-tabs.js`, `C:\nookitokki\cafe24-agent-kit\agent-kit\clients\_verified-template\src\_nk\js\nk-guide-tabs.js` | PDP tab script · 이용안내 tab script |

**Agent working notes**

- 기본 사용법은 “`_verified-template/src`를 `clients/{몰ID}/src`로 복사 후 작업”이다. 이 정본 폴더에서 직접 클라이언트 브랜드 작업을 하지 않는다.
- Domain A P4 같은 명시된 template 승격 작업에서는 `_verified-template/src` in-place 편집 가능. 이때도 새 client folder 생성은 금지다.
- 주문서/결제/PG C그룹은 기본 제외 원칙이다. `order/orderform.html`이 없는 것은 누락이 아니라 안전 설계다.
- `module="..."`, `{$...}` 변수, `xans-*`, `ec-base-*`, `@layout/@contents/@css/@js/@import` 지시어를 삭제하거나 이동하면 런타임이 깨질 수 있다.
- token 변경은 `nk-tokens.css` 우선. 페이지 CSS에 색을 하드코딩하면 drift guard와 유지보수성이 깨진다.
- `nk-stock.css`는 stock 페이지 톤 레이어다. cover page의 페이지별 CSS보다 앞/뒤 load 순서와 specificity 의도를 확인하고 수정한다.

**Verification notes**

- source verify: `_verified-template`은 `agent-kit/connect/scripts/verify-kit.sh` clients allowlist에 포함되어야 한다.
- dist verify: root `scripts/verify-kit.sh`는 `_verified-template` 중립성 drift를 검사한다.
- template 변경 검증 기준 8개: SmartDesign 지시어 보존, `{$변수}` 보존, `module` 보존, `xans/ec-base` 보존, 주문/결제/PG 기본 제외, backup/rollback 설명, 브랜드 흔적 제거, 비개발자 안전성 설명.
- 실제 브라우저 검증이 필요한 변경은 PC/mobile screenshot, module 바인딩, `{$` 노출 0, overflow 0, 핵심 URL smoke를 별도로 수행해야 한다.

---

## 9. `agent-kit/brain/docs/` — 두뇌 문서와 근거 지도

**Purpose**

`C:\nookitokki\cafe24-agent-kit\agent-kit\brain\docs`는 카페24 스킨 자동화의 판단 근거, 방법론, 검증 기록, 공식 대조표, 스니펫을 담은 brain layer다. workflow가 “순서”라면 brain docs는 “왜 그렇게 하는가”와 “무엇이 안전한가”를 설명한다.

**Key documents**

| 절대 경로 | 역할 |
|---|---|
| `C:\nookitokki\cafe24-agent-kit\agent-kit\brain\docs\CAFE24-SMARTDESIGN-AGENT.md` | SmartDesign 전문 에이전트 핵심 문서. 역할, 문법, 함정, 작업 원칙 |
| `C:\nookitokki\cafe24-agent-kit\agent-kit\brain\docs\WORK-GUIDE.md` | `_nk` template customization 작업지시서. HTML-native vs EZ-on-legacy 등 실무 기준 |
| `C:\nookitokki\cafe24-agent-kit\agent-kit\brain\docs\GOAL-AND-ROADMAP.md` | kit 목표, 목표 적합성, roadmap |
| `C:\nookitokki\cafe24-agent-kit\agent-kit\brain\docs\OFFICIAL-AUDIT.md` | Cafe24 공식 guide 대조표. 공식/실측 경계 확인 |
| `C:\nookitokki\cafe24-agent-kit\agent-kit\brain\docs\LEGACY-HUNTER.md` | 스킨 코드 고고학 prompt. layout 고아, CSS 부채, EZ 전략 분기 |
| `C:\nookitokki\cafe24-agent-kit\agent-kit\brain\docs\EZ-STRATEGY.md` | EZ 기본 전략. 기본은 strip, 예외는 명시적 파일럿 |
| `C:\nookitokki\cafe24-agent-kit\agent-kit\brain\docs\EZ-OVERLAY-FINDINGS.md` | EZ→HTML overlay 실측 발견 기록 |
| `C:\nookitokki\cafe24-agent-kit\agent-kit\brain\docs\BASE-CSS-MAP.md` | HTML-native base CSS 전역 지도 |
| `C:\nookitokki\cafe24-agent-kit\agent-kit\brain\docs\BASE-CSS-MAP-EZ.md` | SmartDesignEasy base CSS 전역 지도 |
| `C:\nookitokki\cafe24-agent-kit\agent-kit\brain\docs\SKIN1-AB-VALIDATION.md` | skin1 A/B 방식 검증 기록 |
| `C:\nookitokki\cafe24-agent-kit\agent-kit\brain\docs\SPINE-VALIDATION.md` | Phase 3 spine end-to-end 실증 기록 |
| `C:\nookitokki\cafe24-agent-kit\agent-kit\brain\docs\cafe24-skill-resources.md` | skill 확장 자료 index. snippets/references/design-token 연결 |
| `C:\nookitokki\cafe24-agent-kit\agent-kit\brain\docs\단계별-지시-프롬프트-플레이북.md` | 신규 몰 구축 단계별 지시 prompt playbook |
| `C:\nookitokki\cafe24-agent-kit\agent-kit\brain\docs\analysis\2026-07-05_스마트디자인-방법론\01_deep-dive_기본스킨-모듈유닛-구조와-잔존CSS.md` | 기본 스킨 페이지·모듈·유닛 구조 deep dive |
| `C:\nookitokki\cafe24-agent-kit\agent-kit\brain\docs\snippets\ez-contents-override.css` | F27 `#contents` 92% 대응 paste-ready CSS |
| `C:\nookitokki\cafe24-agent-kit\agent-kit\brain\docs\snippets\ec-paginate-override.css` | pagination override snippet |

**Agent working notes**

- `OFFICIAL-AUDIT.md`는 “공식 문장으로 확인된 것”과 “실측으로만 확인된 것”을 구분할 때 우선 확인한다.
- `CAFE24-SMARTDESIGN-AGENT.md`와 `.claude/skills/cafe24/SKILL.md`의 문법 설명이 어긋나면 둘 중 하나를 조용히 믿지 말고 official audit/evidence label을 확인한다.
- `BASE-CSS-MAP*`은 CSS로 이길지, HTML을 재마크업해야 할지 판단할 때 사용한다.
- `EZ-STRATEGY`와 `EZ-OVERLAY-FINDINGS`는 Easy 타입 작업에서 특히 중요하다. Easy GUI 메타와 FTP HTML을 동시에 깨지 않게 경계한다.
- brain docs의 스니펫은 근거/처방이다. 실제 배포 template에 반영하려면 `_verified-template/src` 또는 `.claude/skills/cafe24/snippets`의 대응 파일까지 확인한다.

**Verification notes**

- brain docs 변경 후에는 관련 workflow/troubleshooting/skill 링크가 stale 되지 않았는지 targeted grep/read로 확인한다.
- `agent-kit/connect/scripts/verify-kit.sh`는 `CAFE24-SMARTDESIGN-AGENT.md`, `common-pitfalls.md`, F index, workflow 07 존재를 확인한다.
- 공식/실측 라벨 변경은 `cafe24/references/evidence-labels.md`와 일치해야 한다.
- snippets 변경은 실제 CSS selector specificity와 Cafe24 runtime 구조(`#container #contents`, `xans-*`, `ec-base-*`)를 기준으로 검증한다.

---

## 10. `agent-kit/brain/rules/` and evidence — 규칙과 원본 근거

**Purpose**

`C:\nookitokki\cafe24-agent-kit\agent-kit\brain\rules`는 특정 함정/운영 규칙을 짧게 강제하는 rule layer다. `brain/_evidence`는 공식/실측 원본 캡처와 quote cache 성격이다.

**Key files**

| 절대 경로 | 역할 |
|---|---|
| `C:\nookitokki\cafe24-agent-kit\agent-kit\brain\rules\responsive-fullrange.md` | full-range responsive 관련 규칙 |
| `C:\nookitokki\cafe24-agent-kit\agent-kit\brain\rules\responsive-mobile.md` | 단일 반응형 스킨과 관리자 mobile OFF 관련 규칙 |
| `C:\nookitokki\cafe24-agent-kit\agent-kit\brain\rules\ez-contents-width.md` | EZ `#contents` 92% width trap 필수 override |
| `C:\nookitokki\cafe24-agent-kit\agent-kit\brain\rules\cafe24-admin-verify.md` | 관리자 설정 확인이 필요한 경우의 gate |
| `C:\nookitokki\cafe24-agent-kit\agent-kit\brain\_evidence\` | 공식/실측 원본 evidence. dist 제외 대상 |

**Agent working notes**

- rule 문서는 workflow/skill에서 “짧은 강제 규칙”으로 참조하기 좋다. 긴 설명은 docs에 두고, 반복 확인은 rules에 둔다.
- `_evidence`는 배포 표면이 아니다. 여기에 새 증거를 넣는 작업은 local research 성격이며 공개 bundle과 분리해야 한다.

**Verification notes**

- rule 변경 시 해당 F코드 문서와 workflow link를 맞춘다.
- `_evidence`는 build-dist에서 제외되므로 dist verification에는 들어가지 않는다. 공개 문서가 evidence 파일을 직접 링크하면 배포본 dead link가 될 수 있다.

---

## 11. `agent-kit/connect/` — 사용자 연결 가이드와 source verify

**Purpose**

`C:\nookitokki\cafe24-agent-kit\agent-kit\connect`는 배포 kit 사용자에게 MCP/OAuth/SFTP 연결을 설명하고, source verify script를 제공하는 연결 안내 계층이다.

**Key files**

| 절대 경로 | 역할 |
|---|---|
| `C:\nookitokki\cafe24-agent-kit\agent-kit\connect\DISTRIBUTION-KIT.md` | dist bundle build/포함/제외/첫 몰 세팅/검증 안내 |
| `C:\nookitokki\cafe24-agent-kit\agent-kit\connect\MCP-OAUTH-GUIDE.md` | 초보자용 OAuth 발급 튜토리얼. `mall.read_design` 최소 권한 권장 |
| `C:\nookitokki\cafe24-agent-kit\agent-kit\connect\OAUTH-BEGINNER-5MIN.md` | 빠른 OAuth 안내 |
| `C:\nookitokki\cafe24-agent-kit\agent-kit\connect\scripts\verify-kit.sh` | source verify |
| `C:\nookitokki\cafe24-agent-kit\agent-kit\connect\scripts\verify-live.sh` | live verify 가능 영역. 승인 전 주의 |
| `C:\nookitokki\cafe24-agent-kit\agent-kit\connect\scripts\verify-partner-live.sh` | partner live verify 가능 영역. 승인 전 주의 |

**Agent working notes**

- `MCP-OAUTH-GUIDE.md`는 사용자가 브라우저 주소창과 터미널을 오가야 하는 단계가 있다. URL/token/secret을 채팅에 붙이지 않게 설명해야 한다.
- OAuth 발급 자체는 외부 연결이므로 Domain B. 문서 수정은 Domain A, 실제 token 생성은 Domain B다.
- `DISTRIBUTION-KIT.md`의 포함/제외 표가 `build-dist-kit.sh`와 어긋나면 user-facing 배포 안전성이 깨진다.

**Verification notes**

- 연결 문서 변경 후 `agent-kit/connect/scripts/verify-kit.sh`가 통과해야 한다.
- OAuth/SFTP 설명 변경은 `mcp/README.md`, `agent-kit/00_시작하기/05b-MCP-등록.md`, root `.claude/skills/API발급`/`MCP연결`/`접속세팅`과 용어가 맞아야 한다.

---

## 12. `agent-kit/00_시작하기/`, `01_작업하기/examples/`, `clients/_template/` — 수강생 동선

**Purpose**

이 영역들은 비개발자 수강생이 실제로 따라가는 시작/연습/클라이언트 scaffold 동선이다. codebase cartography에서는 “설명력”을 검증하는 표면으로 본다.

**Key areas**

| 절대 경로 | 역할 |
|---|---|
| `C:\nookitokki\cafe24-agent-kit\agent-kit\00_시작하기\` | 아무것도 모를 때, 5분 컷, 몰 ID 찾기, WebFTP vs SFTP, MCP 등록, prompt template, Q&A, 실패복구 |
| `C:\nookitokki\cafe24-agent-kit\agent-kit\01_작업하기\examples\` | 헤더 로고 교체, 메인 배너, 상품 상세 레이아웃 등 첫 실습 예시 |
| `C:\nookitokki\cafe24-agent-kit\agent-kit\clients\_template\` | 신규 client scaffold 원본. 요청사항/수정사항/references/design/work-log/CLAUDE 템플릿 |
| `C:\nookitokki\cafe24-agent-kit\agent-kit\clients\demo000\` | 예시 workflow client |

**Agent working notes**

- 초보자 문서는 기술 정답보다 “따라 했을 때 어디서 막히지 않는가”가 중요하다.
- `clients/_template`은 scaffold 정본이다. 신규 클라이언트 실데이터를 이 폴더에 넣지 않는다.
- `demo000`은 예시로 배포 가능하지만, 실 클라이언트 폴더는 dist allowlist 밖이다.

**Verification notes**

- source verify는 `00_시작하기` markdown 최소 5개 이상을 확인한다.
- scaffold 변경은 `mcp/kit_tools.py::scaffold_client`와 `clients/_template` 구조가 맞는지 확인한다.
- onboarding 문서의 명령 이름은 root `.claude/skills` 실제 폴더명과 일치해야 한다.

---

## 13. 작업 유형별 “어디를 고칠까” 빠른 라우팅

| 작업 요청 | 먼저 볼 곳 | 수정 후보 | 건드리지 말 곳 |
|---|---|---|---|
| 초보자 시작 안내 개선 | `agent-kit/README.md`, `00_시작하기/` | root README, kit README, `키트-시작-가이드.md`, `QnA-쉬운말로.md` | MCP backend code |
| MCP 연결/토큰 안내 개선 | `agent-kit/connect/MCP-OAUTH-GUIDE.md`, `mcp/README.md` | connect docs, `MCP연결`, `API발급`, `접속세팅` skills | 실제 token/config 파일 |
| source verify 실패 | `agent-kit/connect/scripts/verify-kit.sh` | verify script, missing docs/files | live verify scripts, release script |
| dist build/packaging 문제 | `scripts/build-dist-kit.sh`, `scripts/verify-kit.sh` | build/verify scripts, README/changelog sync | git release/push |
| SmartDesign 문법 정정 | `.claude/skills/cafe24/SKILL.md`, `references/*`, `OFFICIAL-AUDIT.md` | skill reference, brain docs | `_verified-template` unless actual template behavior changes |
| F코드/troubleshooting 보강 | `02_막혔을때/F-상황-인덱스.md`, `함정-INDEX.md`, `common-pitfalls.md` | F hub, Q&A, prompt templates, brain rules | unrelated workflow stages |
| Workflow 단계 수정 | `01_작업하기/workflows/README.md` + target workflow | workflow markdown, `카페24-워크플로우` agent if trigger/state changes | MCP upload/write functions |
| `_verified-template` 품질 개선 | `_verified-template/README.md`, `CASE-STUDY.md`, `src/` | template src, install doc, case study | `clients/_template` or 실 client folders |
| Token/snippet 품질 개선 | `.claude/skills/cafe24/snippets`, `design-tokens`, `_verified-template/src/_nk/css` | snippets and/or template token CSS | unverified non-Cafe24 variable sources |
| Agent behavior 수정 | `.claude/agents/*.md` | relevant agent only | role-irrelevant agents |

---

## 14. 최소 검증 체크리스트

문서만 수정한 경우에도 다음을 기준으로 고른다.

1. **문서/지도/링크만 수정**
   - 대상 파일 read-back.
   - 관련 링크/파일명 존재 확인.
   - 가능하면 `bash agent-kit/connect/scripts/verify-kit.sh`.

2. **skill/reference/snippet 수정**
   - `bash agent-kit/connect/scripts/verify-kit.sh`.
   - fake variable, token drift, F-code link 정합 targeted check.

3. **template src 수정**
   - 8개 skin safety criteria 확인.
   - SmartDesign directive/module/variable preservation targeted grep.
   - PC/mobile smoke 또는 score/preflight가 필요한 경우 별도 실행.

4. **build/dist script 수정**
   - `bash scripts/build-dist-kit.sh`.
   - `bash scripts/verify-kit.sh`.

5. **MCP backend 수정**
   - `cd mcp && python -c "import server"`.
   - 관련 CLI command smoke.
   - 단, OAuth 연결/API write/SFTP upload는 Domain B 승인 전 실행 금지.

---

## 15. 현재 지도 작성 근거

이 문서는 다음 현재 repo 표면을 기준으로 작성되었다.

- root README: `C:\nookitokki\cafe24-agent-kit\README.md`
- kit README: `C:\nookitokki\cafe24-agent-kit\agent-kit\README.md`
- approved ralplan Domain boundary: `C:\nookitokki\cafe24-agent-kit\.omc\plans\cafe24-agent-kit-skin-safety-ralplan.md`
- MCP README/CLI: `C:\nookitokki\cafe24-agent-kit\mcp\README.md`, `C:\nookitokki\cafe24-agent-kit\mcp\cli.py`, `C:\nookitokki\cafe24-agent-kit\mcp\kit_tools.py`
- build/verify scripts: `C:\nookitokki\cafe24-agent-kit\scripts\build-dist-kit.sh`, `C:\nookitokki\cafe24-agent-kit\scripts\verify-kit.sh`, `C:\nookitokki\cafe24-agent-kit\agent-kit\connect\scripts\verify-kit.sh`
- root skills/agents: `C:\nookitokki\cafe24-agent-kit\.claude\skills\`, `C:\nookitokki\cafe24-agent-kit\.claude\agents\`
- workflow/troubleshooting/template/brain doc inventories under `C:\nookitokki\cafe24-agent-kit\agent-kit\`

이 문서 자체는 guide surface다. 실제 수정을 수행할 때는 반드시 해당 원문 파일을 다시 읽고, 파일별 최신 상태를 기준으로 작업한다.
