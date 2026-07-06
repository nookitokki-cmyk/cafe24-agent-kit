# Cafe24 Agent Kit — Changelog

## v2.8.0 (2026-07-06) — 재마크업 방법론 표면화 + 카트 JS재구축 + A-to-Z 전체 개편 워크플로우

> **호환성:** non-breaking(파일 삭제·이동·이름변경 **없음**, 순수 신규 추가 + 문서 내용 정합). 기존 v2.7.x 설치 위에 그대로 업데이트 가능.

### Added
- **재마크업 방법론 1급 문서화** — `references/module-remarkup.md`: "색·폰트·여백=CSS 오버라이드 / 레이아웃·구조=HTML 재작성" 결정트리, 되는·제약 모듈 등급표(✅완전재작성/🟡주의/🔴표 골격보존), 반복단위(`anchorBoxId_{$product_no}`) 보존 규칙, 반복단위 계층 규칙.
- **카트 JS재구축 방법** — `references/cart-js-rebuild.md` + `snippets/_nk-cart-app/`: 거래 표를 완전 커스텀해야 할 때 카페24 카트를 화면 밖으로 숨기고 JS로 데이터를 읽어 커스텀 UI 렌더 + 숨긴 원본에 배선 연결. **프로토타입 단계(옵션·품절·배송그룹 하드닝 미완) — 실전 적용 전 검증 필수 경고 포함.**
- **A-to-Z 전체 개편 워크플로우** — `01_작업하기/workflows/09-full-renewal.md`: 레퍼런스 인입 → 토대정리 → 페이지 유형별 재마크업/재스타일/JS재구축 자동 배분 → verify-loop/qa-loop.
- **디자인 프리셋 3종** — `design-tokens/presets/`(minimal·luxury·soft).
- **모듈 안전등급표·페이지맵 편입** — `references/module-safety.json` + P0 실측 맵. 근거 라벨(`[공식]`/`[실측]`/`[검증됨]`/`[검증필요]`) 정합.

### Fixed — 카페24 문법 정합화 (2026-07-06 skin2 라이브 검증 반영, QA 3라운드)
- **조건문**: `<!--[if]-->`는 미작동 → `|display` 필터로 정정.
- **변수 스코프**: 모듈 밖/미지원 변수는 `{$var}` 글자 그대로가 아니라 **빈 값**으로 렌더됨(중괄호·`$` 누락 오타일 때만 글자 그대로). authoritative 문서 + 초보자 문서(용어집·실패복구·자주막히는5가지) + troubleshooting 전면 정합.
- **지시어**: 실제 지시어는 `@layout`·`@contents`·`@css`·`@js`·`@import` **괄호 단일태그**뿐. 쌍태그(`<!--/@css-->`)·`@module`·`@section`·`@placeholder`는 실제 지시어 아님 → `troubleshooting.md` 예시 코드의 가짜 `<!--@module()-->` 표기를 실제 `<div module="...">` 속성 형태로 전면 교정.
- **span 함정**: `{$product_name}`은 카페24가 `<span>`으로 감싸므로 `alt=`/`aria-label=`/`|cut`에 직접 쓰면 마크업 깨짐 → 회피 가이드.
- `product_action`(구매 버튼) 재마크업 가능(onclick·link 1:1 이식) / 거래 표 de-table 금지 — 라이브 실증 반영.
- (내부) stale `dist/` 추적 해제 — 릴리스는 `build-dist-kit.sh` 재빌드본만 사용.
- **문서 정합**: 명령 개수 문서 간 불일치(9·6·16 혼재 → 14개로 통일, 정본 `commands/COMMANDS.md`), 죽은 stub `05b-MCP-Cursor-등록.md` 제거, 루트 README 진입 문서 안내(PURPOSE는 배포본 미포함 명시), 배포 대상 전체 **죽은 링크 0건**(v2.6.0 스킬 이동 후 `../.claude`→`../../.claude` 경로 잔존 교정).

## v2.7.1 (2026-07-04) — 준비물 3종 세트(컴포넌트 갤러리) + Claude Code MCP 지원

### Added
- **컴포넌트 갤러리** 하위 스킬(`.claude/skills/cafe24/component-gallery/`) 신설 — 디자인 토큰(값)으로 버튼·폼·카드 등 부품을 미리 조립해 진열대(`example-gallery.html`)로 확정. 토대정리 C단계에 **"4. 컴포넌트 갤러리"** 단계 + 완료기준 추가.
- **Claude Code MCP 등록 지원** — `.mcp.json.example` / `.mcp.json.mac.example` 템플릿(`${CLAUDE_PROJECT_DIR:-.}` 기반) + 빌드 스크립트·설치안내 반영.
- `cafe24/SKILL.md`에 **"작업 전 준비물"** 섹션(디자인 3종 세트), `design-tokens/examples/` 분석문서 예시(JSON·MD 역할 구분).

### Changed
- MCP 등록 안내 간소화 — 새 세션에서 **"카페24 연결됐는지 확인해줘"** 한마디로 확인, 신뢰 승인 안내 추가(`MCP연결`·`05b-MCP-등록.md`).
- 백업 존재확인을 `list`/`download`와 동일한 **MLSD 목록조회**로 통일(폴더·파일 일관 처리). 배포본에 슬래시 스킬 전체 + MCP 템플릿 포함.
- `references/input-pipeline.md`에 컴포넌트 갤러리 생성 단계 삽입.

## v2.7.0 (2026-06-25) — 미검증(비-카페24 출처) recipes·templates 제거 + 변수 가드 (Step 8)

### Removed
- **`recipes/`(7) · `templates/`(5) 제거** — 비-카페24 출처 `APapeIsName/web-uiux-design-from-reference`(일반 웹 디자인 레포)에서 유입돼 변수의 **67~100%가 카페24에 없는 가짜**(`{$thumbnail_url}`·`{$product_url}`·`{$sale_price}` 등). "진짜처럼 보이는 가짜 코드"라 오히려 위험 → 제거. (git 히스토리 보존, 복구 가능)

### Fixed
- **`references/troubleshooting.md`** — "올바른 가격 변수명" 섹션이 정작 가짜 변수(`{$price}`·`{$retail_price}`·`{$discount_price}`)를 안내하던 것을 **검증본**(`{$product_sale_price}`·`{$product_price}`)으로 정정.

### Added
- **변수 재유입 가드** — `verify-kit`에 비-카페24 가짜 변수 denylist 검사(FAIL) 추가. 미검증 변수 재유입 자동 차단.

### Changed
- `SKILL.md`·`CLAUDE.md`·`README.md` 인덱스에서 recipes/templates 제거 + 출처 표기에서 비-카페24 `APapeIsName` 제거. **카페24 변수 단일 기준 = `references/variables.md`(검증본).**

> 팩트체크 감사(STATUS Step 8) 결과. 유지: SKILL.md 본문·`references/`·`snippets/`(components·css·js)·`design-tokens/`·`module-browser.html`(검증·카페24 변수 무관).

## v2.6.3 (2026-06-25) — 상품 마우스오버 롤오버: 틀린 변수 정정 + 공식 방법 반영

### Fixed
- **`snippets/js/nk-product-hover.js` · `snippets/components/nk-product-card.html`** — 존재하지 않는 변수 `{$product_image2}`(검증 안 된 추측)를 **카페24 공식 방법**으로 정정. 카페24엔 롤오버 전용 변수가 없고, **'축소 이미지' 칸(`{$image_small}`)**을 마우스오버 이미지로 활용. (출처: 카페24 Help Center "상품 이미지에 마우스오버 시 다른 이미지 노출시키는 방법")

### Added
- **`recipes/02_상품목록-그리드.md`** — "마우스오버 롤오버(PC 전용)" 섹션: 목록·축소 이미지 등록 + `onmouseover="this.src='{$image_small}'" onmouseout="this.src='{$image_medium}'"` + 두 이미지 사이즈 동일 주의.
- **`references/variables.md`** — `{$image_small}`이 목록 롤오버에도 쓰임 명시(기존 '상세' 단독 표기 보강).

> ⚠️ 이 정정은 v2.4.0 실험적(🧪) 자료의 미검증 코드를 잡은 첫 건. 동일 묶음(snippets·recipes·templates) 전체 팩트체크 감사(STATUS Step 8) 후속 진행 예정.

## v2.6.2 (2026-06-24) — /토대정리 스킬 신설 (워크플로우 C단계)

### Added
- **`/토대정리` 스킬** — 시안/레퍼런스 구현의 **C단계**(섹션 제작 직전 1회)를 한 스킬로: ① base 함정 전수 스캔 → `BASE-CSS-MAP.md` ② `nk-cafe24-reset.css` 적용 ③ 디자인 토큰 세팅(`--nk-point`·Pretendard·Phosphor). 상세는 기존 문서(reset 가이드·`CAFE24-SMARTDESIGN-AGENT.md` STEP 2·design-tokens)를 가리켜 **중복 없음**.
- `03-reference-renewal.md`에 **2.5단계(토대 정리)** 연결, `commands/COMMANDS.md`에 `/토대정리` 등록.

> A→Z 파이프라인(`/카페24-워크플로우`→`03-reference-renewal`)에서 유일하게 빠져 있던 C(토대) 단계 보완. A·B·D·E·F는 기존 스킬로 이미 커버.

## v2.6.1 (2026-06-24) — nk-cafe24-reset.css 사용 가이드 신설

### Added
- **`snippets/css/nk-cafe24-reset-사용가이드.md`** — base 함정 중화 레이어의 독립 사용 가이드(비개발자용). 적용 3단계(업로드→`@css` 맨 위 로드→`<body class="nk-skin">`), 안 먹을 때(`body#main.nk-skin`로 명시도 보강), 색 위임(`--nk-point`), 10개 섹션이 막는 함정 표, 3형제 구분(reset/ez-override/일반 reset), Step 0 base 스캔 연계, 적용 체크리스트.

### Fixed
- `SKILL.md` snippets 목록에 누락돼 있던 `nk-cafe24-reset.css`를 등록 + 가이드 링크 연결(기존엔 파일만 있고 문서화 X라 못 찾던 문제).

## v2.6.0 (2026-06-24) — 명령→스킬 통합 + 진입점 정상화

### Changed
- **슬래시 명령 19개 → 스킬 통합** — 모든 슬래시 명령을 스킬로 전환해 워크스페이스 **루트 `.claude/skills/`** 로 이동(16개 정규 + 기존 `cafe24`·`qa-loop`). 키트 **최상위 폴더를 열면 `/키트시작` 등이 바로 인식**됨. (기존엔 `agent-kit/.claude/commands/` 중첩이라 루트를 열면 명령이 안 떴음 — Claude Code는 워크스페이스 루트 `.claude/`만 스캔.)
- **에이전트 4개 루트 이동** — `code-reviewer`·`qa-checker`·`카페24-워크플로우`·`카페24-도우미` → 루트 `.claude/agents/` (스킬 전환 없이 에이전트로 유지).
- **구 별칭 3개 폐기** — `/카페24-시작`·`/카페24-도와줘`·`/카페24-새작업` 제거. 각각 `/도움말`·`/도움말`+함정·`/디자인수정`(신규 몰 `/새클라이언트`) 직접 사용.

### Fixed
- **진입점 깨짐 해결** — `/키트시작` 등이 최상위 폴더에서 인식 안 되던 문제. 스킬은 루트에서 prefix 없이 `/명령` 호출 + 관련 상황에 자동 트리거.

### Internal
- `UPDATE_PATHS` `agent-kit/.claude`→`.claude`(루트) / `build-dist-kit.sh` 루트 `.claude/{skills,agents}` dist 포함(worktrees 제외) / `mcp/server.py` 워크플로 경로 루트 기준 보정 / verify·문서·`PURPOSE.md` 동기화.

## v2.5.1 (2026-06-24) — 벤더 브랜드 실명 제거

### Fixed
- **실명 누출 제거** — 유료 구매 템플릿 벤더의 브랜드 실명을 전체 문서·코드 예시에서 제거(12개 파일·202회). 본문은 `구매템플릿`, 코드 토큰(폴더·JS 파일·CSS 변수·JS 객체)은 `_ext_` 계열로 중립화. 의미와 `→NK` 마이그레이션 가이드는 그대로 보존.
- **재발 방지 가드** — `verify-kit`(소스·dist) 양쪽에 벤더 실명 재유입 검사 추가.

## v2.5.0 (2026-06-24) — 레포 구조 개편 + 카페24 함정 대응 강화

### Added
- **`snippets/css/nk-cafe24-reset.css` 신설** — `body.nk-skin` opt-in 방식의 **카페24 base 7대 함정 범용 중화 레이어**(고정폭·가짜선·a밑줄·상품 회색테두리·카페24 블루·gif/PNG 폼컨트롤·푸터 고정폭). 기존 `nk-ez-override.css`(#nk-skinN, base 소스 토큰화 보완)와 달리 **base를 못 고치는 클라이언트 운영 스킨에서 오버라이드 레이어로 쓰는 휴대용 버전**. 색은 `--nk-point` 등 변수 위임, 체크박스 체크표시는 `<input>` 자체 background SVG(pseudo-element 미렌더 회피), select caret 중립색 고정. (code-reviewer 2회 + 크로스브라우저 검증)
- **base 전수 스캔 명령 세트 추가** (`CAFE24-SMARTDESIGN-AGENT.md` STEP 2) — 새 클라 base CSS를 7종 grep(고정폭·파란색·강제폰트·가상요소선·echosting 이미지·!important·태그누수)으로 전수 스캔해 `BASE-CSS-MAP.md`를 생성·검증. 함정을 사람이 하나씩 발견하지 않고 기계가 색출 → 게시판·주문·회원 등 안 본 페이지 함정도 사전 포착. (계기: 클라마다 base가 달라 두더지잡기가 반복되던 문제)
- **`brain/rules/responsive-fullrange.md` 신설** — 전체 해상도 대응 규칙(모바일 375 ~ 울트라와이드 2560). 콘텐츠 `max-width` 상한 함정(와이드 좁은 밴드)·카드 이미지 미충전(체인 inline) 함정 + copy-paste 처방. (계기: ecudemo400125 — 1440에서만 검증해 와이드 전용 버그를 놓친 사고)
- **`capture-pair.mjs` 와이드 캡처 추가** — 기본 뷰포트에 `wide(1920)`·`ultrawide(2560)` 추가(기존 pc 1440·mobile 390). lazy 이미지 로딩용 자동 스크롤 추가 → 1600 초과 전용 버그를 검증 단계에서 포착.
- **`accuracy-gate.md` visual 축 폭 확장** — PC·모바일 → 모바일·PC·와이드·울트라와이드 전 구간. 풀블리드 레퍼는 1600 초과 폭 생략 불가.

### Changed
- **`PURPOSE.md` 신설** — 목적·3층 분리·자동업데이트 불변식 헌장 (개편 기준)
- **진입점 단일화** — 루트 `README.md`를 유일 시작점으로 재작성, `agent-kit/README.md`는 "본체 지도"로 역할 정정 (구 v2.3 Step4b의 "단일 진입점 = agent-kit/README" 서술을 갱신)
- **개발 메타 격리** — `__THE-ONE_단일기준`·`__지금상태_STATUS`·`MANIFEST` → `_dev/meta/`
- **배포 진입점 통일** — dist 진입점을 루트 `README.md`로 통일(구 `README-DIST` 대체) + `_dev`/`brain/_evidence` build 제외

## v2.4.0 (2026-06-21)

### Added — 카페24 스킨 작업 풀스택 자동화 (대규모 추가)

**비코더가 막히는 지점 3가지(레시피·에러·시각 미리보기) 해소 + Figma→CSS 토큰 파이프라인 + 클라이언트 통합 프로필 + 원클릭 자동화 명령. 총 28개 신규 파일, 1개 갱신.**

#### `agent-kit/.claude/skills/cafe24/` 대폭 확장
- `recipes/` (7) — 모듈 조합 레시피북 (메인-히어로 / 상품목록-그리드 / 상품상세 / 장바구니-결제 / 게시판-공지사항 / 로그인-회원가입 / 검색결과). "내가 원하는 화면 → 어떤 모듈 어떻게 조합" 매핑 사전
- `templates/` (5) — 페이지 타입 스타터 (hero-main / plp-full / pdp-full / narrow / board). SFTP 업로드 → EZ로 텍스트만 바꾸면 끝나는 완성형
- `snippets/` (20) — HTML 컴포넌트 6개 (header / product-card / banner-slider / footer / breadcrumb / quick-view) + CSS 시스템 8개 (reset / typography / responsive-grid / ez-override / button / form / modal / toast) + JavaScript 6개 (sticky-header / product-hover / scroll-animation / modal-toggle / tab-switcher / form-validator). 전부 Vanilla, nk- prefix, Pretendard / Phosphor 준수
- `design-tokens/` (4) — Figma URL → JSON → CSS 토큰 자동 파이프라인 (README / schema / example / builder-guide)
- `brand-profile/` (3) — 클라이언트 통합 프로필 (메타·연락처·프로젝트·브랜드·페이지 구성) JSON 스키마 + 예시
- `workflows/` (1) — `/카페24-자동화` 6단계 파이프라인 문서
- `module-browser.html` (1) — 19개 모듈 시각 카탈로그 단일 HTML (검색·다크모드·복사 버튼)
- `references/troubleshooting.md` (1) — 비코더 마주치는 5대 에러 + 수정 템플릿 (21KB)
- `references/variables.md` (확장) — 6.4KB → 13.6KB. 15개 섹션 마스터 사전 (상품 기본/가격/이미지/상태·아이콘/옵션/상세·배송/구매 액션/카테고리/정렬·페이지네이션/쇼핑 전역/장바구니/주문서/회원/게시판/Config 조건) + 비코더 빠른 가이드
- `references/modifiers.md` (확장) — 13개 모디파이어(`|cut`·`|display`·`|number_format` 등) + Foreach·If 문법 상세 (17KB)
- `SKILL.md` (갱신) — 12번 섹션을 신규 자료 통합 인덱스로 재편

#### 부속 인프라
- `agent-kit/.claude/agents/qa-checker.md` — 카페24 비주얼 검증 에이전트 (Haiku)
- `agent-kit/.claude/skills/qa-loop/SKILL.md` — 합격 점수 0.85 자동 수정 루프 스킬
- `agent-kit/.claude/commands/카페24-자동화.md` — 원클릭 파이프라인 슬래시 명령 (토큰 빌드 → HTML → 리뷰 → QA → SFTP)

### Added — 시작 시 자동 업데이트 (배달 메커니즘)
**이미 설치한 사용자가 앞으로의 업데이트를 조건부 자동으로 받게 하는 핵심 기능.** 이 버전으로 한 번 올린 뒤부터 시작 시 자동 반영.
- **시작 시 자동 업데이트 체크** — `python cli.py kit-autoupdate`. `/키트시작` 0단계로 실행되어, 로컬 `VERSION` vs 원격(GitHub Release)을 비교하고 새 버전이면 안내/적용
  - **채널 감지**(`detect_install_channel`): `git` clone / GitHub Release `zip` / 향후 `npm` 을 구분해 알맞은 업데이트 명령 제시 (env `CAFE24_KIT_CHANNEL` 로 강제 지정 가능)
  - **조건부 자동 적용** `--apply`: Release 채널은 `kit-update --from-github` 자동 실행, git 채널은 **클린 트리일 때만** `git pull --ff-only`. config/*·clients/{몰} 은 항상 보존
  - **스로틀**(기본 12h) + **오프라인 안전**: 매 시작마다 네트워크를 때리지 않고, 원격 확인 실패 시에도 시작을 막지 않음. `--force` 로 즉시 재확인
  - backend(paramiko 등) 미설치 상태에서도 `kit-*` 명령 동작 — pip 설치 전 fresh 설치자 0단계 크래시 방지
  - 스로틀 상태 파일 `mcp/config/.autoupdate_check.json` 은 gitignore 처리(로컬 전용)
  - 문서: `/키트시작` Q0 + `/버전확인` 채널표

### Stability — 자료별 검증 상태

**✅ 즉시 사용 권장 (Stable)** — 글 정리·공식 문서·MIT 출처 기반, 검증 완료
- `references/troubleshooting.md` (21KB, 비코더 5대 에러 + 해법)
- `references/variables.md` 확장 (6.4KB → 13.6KB, 15섹션 250+ 변수)
- `references/modifiers.md` 확장 (13개 모디파이어 + Foreach/If 문법)
- `recipes/01~07.md` (모듈 조합 매핑 사전)
- `module-browser.html` (의존성 없는 단일 HTML, 브라우저 더블클릭)

**🧪 실험적 (Experimental)** — 카페24 라이브 환경 검증 부족, 실 클라이언트 작업 검증 후 v2.4.1에서 안정화 예정
- `templates/{hero-main,plp-full,pdp-full,narrow,board}.html` — 페이지 타입 스타터 5종
- `snippets/components/` — HTML 컴포넌트 6개
- `snippets/css/` 추가분 (button/form/modal/toast) — 4개
- `snippets/js/` 추가분 (scroll-anim/modal/tabs/form-validator) — 4개
- `design-tokens/` — Figma → CSS 토큰 파이프라인
- `brand-profile/` — 클라이언트 통합 프로필 JSON
- `workflows/cafe24-automation.md` + `/카페24-자동화` 명령
- `agents/qa-checker.md` + `skills/qa-loop/`

**실험적 자료 사용 시 주의:** 백업 + 소규모 테스트 후 라이브 검증 → 본격 사용. 문제 발생 시 GitHub Issue 환영.

### Notes
- 출처 명시: kimyoungwopo/cafe24-smart-design (MIT) + APapeIsName/web-uiux-design-from-reference (MIT) 분석 + 누끼토끼 실무 정리
- 표준 준수: `nk-` 접두사 / Pretendard / Phosphor / italic 금지 / WCAG AA / 모바일 터치 타겟 44px
- 예시 클라이언트 `demo-brand` 사용 (실제 클라이언트 정보 미포함)
- 사전 처리: 절대 경로 `/Users/{user}/...` → `~/.claude/...` 치환 (개인정보 보호)
- 파일명 통일: `modifiers-and-syntax.md` → `modifiers.md` (기존 GitHub 파일명 유지)

---


## v2.3.6 (2026-06-20)

### Added
- `00_시작하기/프롬프트-템플릿.md` **#13 — EZ 템플릿 overlay**(테마조회→FTP→엎기): `/카페24-워크플로우` 08 Phase A→B 복붙 프롬프트 (F35·F36 가드 + `cafe24_list_themes`·`cafe24_sftp_upload` 명시). `/프롬프트참고`로 호출

### Fixed
- `/디자인수정` 게이트 재구성 — **공통 필수 / 작업종류별(1:1 vs quick-fix)** 분기 명시. 레퍼런스인입 조건이 괄호에 묻혀 quick-fix에도 레퍼런스를 요구하던 모호함 해소
- `설치-안내.md` 릴리스 zip 이름 실제와 일치: `cafe24-agent-kit-v*.zip` → `cafe24-agent-kit.zip`
- `build-dist-kit.sh` 클라이언트 **allowlist** 화 — `_template`·`demo000`만 배포. `ecudemo400864` 등 실/테스트 클라 폴더가 배포 zip에 섞이던 것 차단 (기존 denylist는 신규 폴더를 놓침)

---

## v2.3.5 (2026-06-20)

### Fixed — 파트너센터 웹 FTP = 자동 업로드 (수동 오안내 차단)
- 에이전트가 "파트너센터 웹 FTP는 수동 업로드 (SFTP 차단)" 라고 오안내하던 문제 수정. `sftp_{몰}.json` 에 `"protocol":"ftp"` 가 있으면 `cafe24_sftp_upload` 가 **Python(ftplib)으로 자동 업로드**함을 지침에 명시 (CLAUDE.md §6 · SKILL.md SFTP-차단 항목 · `/접속세팅` · `03-접속-웹FTP-vs-SFTP`)
- "수동 업로드(관리자 파일관리)"의 범위를 **IP 일시 차단 시 최후 우회**로 한정 — 파트너센터의 기본 경로가 아님을 명문화

---

## v2.3.4 (2026-06-20)

### Added
- `references/modifiers.md` — 수정자 13종(`|cut`·`|numberformat`·`|display`·`|date` 등) + 조건/반복 제어 문법 (SKILL.md·CLAUDE.md 레퍼런스 연결)

### Fixed
- 파트너센터 **웹 FTP** 설정법 명시 — `sftp_{몰}.json`에 `"protocol":"ftp"`(port 21·`/sde_design` 경로). `/접속세팅`·`03-접속` 문서 분기 보강 (SFTP만 묻던 혼란 해소)
- `.gitignore`: `agent-kit/clients/*` 일괄 제외(+`_template`·`demo000`만 허용) · `.mcp.json` 제외 — 새 클라 폴더 실수 커밋 방지

---

## v2.3.3 (2026-06-20)

### Added — Mac/Linux 지원 보강
- `.cursor/mcp.json.mac.example` (command=`python3`) 추가 — 배포물 포함. Mac 사용자는 이걸 복사
- 설치 문서(`05b-MCP-등록.md`·`설치-안내.md`)에 Windows(`py -3`)/Mac(`python3`) 분기 명시
- build-dist: `.cursor/mcp.json*.example` 전부 배포물에 포함

---

## v2.3.2 (2026-06-20)

### Changed
- `설치-안내.md` 핑퐁 우선 재작성 — "채팅에 `/키트시작`" 중심(하나씩 물어봄), 수동 단계는 참고로 강등
- `/키트시작` 완료 시 `/API발급`(OAuth)로 자연스럽게 연결

---

## v2.3.1 (2026-06-20)

### Added
- 루트 `설치-안내.md` — 경로 무관 설치·사용·새 클라이언트 안내 (배포물 zip에도 포함)
- 범용 클라이언트 온보딩: "새 클라이언트" 한마디 → 몰 ID 하나만 묻고 `clients/{몰ID}/` 자동 생성·누적 (Tally·Notion 등 외부 폼 안 물음)

### Fixed
- 배포물에서 `__pycache__/*.pyc`(빌드 PC 경로·잉여 파일) 제외 — 빌드 시 `PYTHONDONTWRITEBYTECODE` + 사후 정리

---

## v2.3.0 (2026-06-20)

### Changed — 구조 재편 (Step 4b)
- **사람용/기계용 폴더 재편**: `getting-started`→`00_시작하기`, `examples`·`workflows`→`01_작업하기`, `traps/INDEX`·`common-pitfalls`·`F-상황-인덱스`→`02_막혔을때`, `rules`·지식 `docs`·`_evidence`→`brain`, 접속 `docs`·`scripts`→`connect` (git rename 이력 보존)
- 내부 마크다운 링크·MCP 코드(`server.py`·`kit_tools.py`)·셸 스크립트(`verify-kit.sh`·`build-dist-kit.sh`) 전부 새 구조로 갱신
- 중복 진입점 6→1 통합 (단일 진입점 = `agent-kit/README.md`)

### Added — 입문자료 (Step 4c)
- `00_시작하기/`: `0-이-키트가-뭔가요` · `용어집` · `첫수정-1건-성공` · `실패복구-가이드`

### Fixed — 익명화·범위 보강
- 배포 문서 잔존 실 클라이언트 식별자 제거 + 깨진 링크 19곳 수리
- 문서 범위 정정: 강의/수강생 맥락 단어 제거 → 독자 = "이 키트를 쓰는 비개발자 누구나"

---

## v2.2.3 (2026-06-20)

### Fix
- `kit-update --from-github` — temp dir leak: extract under zip parent, single cleanup in `finally`
- `kit-update` — empty `CAFE24_KIT_UPDATE_SOURCE` no longer resolves to home dir
- `scaffold_client` — single `your_mall_id` replace (REDIRECT_URI derived from template)
- `kit_update` — reject source == workspace root (self-update guard)

---

## v2.2.2 (2026-06-20)

### Fix
- `kit-update --from-github` — private Release zip via API asset URL + `gh auth token` fallback
- `kit-update` no longer wipes entire `mcp/work/` (only `strip_ez.py`)

---

## v2.2.1 (2026-06-20)

### Fix
- `kit-update --from-github` — private repo Release zip via GitHub API asset URL (`application/octet-stream`)
- Auto `gh auth token` when `GITHUB_TOKEN` unset

---

## v2.2.0 (2026-06-19)

### Commands (onboarding + robustness)
- **`/키트시작`** — first install: pip, `import server`, MCP, smoke 5/9
- **`/새클라이언트`** — scaffold `clients/{mall_id}` from `_template`
- **`/MCP연결`** — Cursor + Claude Code MCP registration
- **`/검증`** — `run_preflight` ping-pong with F34 interpretation
- **`/캐시확인`** — `?v=N`, live URL vs SFTP path
- **`/EZ제거`** — Phase C strip (`strip_ez.py`) with user gate
- **`/버전확인`** — local VERSION + remote compare (v3 channel)

### MCP tools
- `get_kit_guides`: `kit_version`, `changelog_path`, `onboarding_commands`
- **`diagnose_kit_setup`** — structured install diagnostic
- **`scaffold_client(mall_id)`** — same logic as `/새클라이언트`

### CLI (`mcp/cli.py`)
- `diagnose`, `scaffold --mall`, `kit-version [--check-remote]`, `kit-update [--source] [--dry-run]`

### Docs & dist
- `05b-MCP-등록.md` — Cursor + Claude Code (replaces Cursor-only title)
- `OMC-명령어-매칭가이드.md`, `COMMANDS.md`, `/도움말` updated
- `smoke_test.py`: **no credentials → exit 0, 5/9 partial OK**
- `build-dist-kit.sh`: REQUIRED includes `05b`, `kit_tools.py`, `CHANGELOG.md`; version **v2.2.0**

### Release channel (v2.2.0+)
- GitHub: `nookitokki-cmyk/cafe24-agent-kit` — tag `v2.2.0` + zip asset
- `cli.py kit-update --from-github` — Release zip 자동 다운로드·적용
- `CAFE24_KIT_GITHUB_REPO` 기본값 · `kit-version --check-remote` via Releases API

---

## v2.0.1 (2026-06-18)

### Fix (critical dist regression)
- Bundle `mcp/auth/`, `mcp/backends/`, `mcp/config/__init__.py` — fixes `No module named auth`
- Windows Git Bash `cp --parents` → `copy_mcp_pkg()` with `cp -R`
- Dist includes `.cursor/mcp.json.example`, `cafe24_config.example.py`, `requirements.txt`
- Exclude `clients/nookitokki002` from dist; no secrets in `mcp/config/`

### Docs
- `05b-MCP-Cursor-등록.md` (later generalized in v2.2)
- Post-build gate: `python -c "import server"` from dist

---

## v2.0.0

- Initial distribution kit: agent-kit + MCP stdio server + score scripts
- 10 MCP tools, 8 workflows, OMC slash commands
