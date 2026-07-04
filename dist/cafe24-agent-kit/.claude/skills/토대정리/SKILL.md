---
name: 토대정리
description: 카페24 디자인 토대 세팅(워크플로우 C단계) — base 함정 전수 스캔 + nk-cafe24-reset.css 적용 + 디자인 토큰 세팅 + 컴포넌트 갤러리(부품 새로 조립). 시안/레퍼런스 구현 직전, 섹션 제작 전에 1회. "토대 정리", "밑칠 제거", "base 스캔", "reset 적용", "토큰 세팅", "컴포넌트 갤러리", "부품 세팅", "디자인 토대" 같은 요청 시 사용.
---

# 토대정리 — 디자인 짜기 전 base 함정 박멸 + 토큰 세팅 (C단계)

> 섹션을 만들기 **전에** 카페24 base 공통 함정을 한 번에 무력화하고, 색·폰트·간격을 변수로 깔아두는 단계.
> 순서: A(연결)·B(실측) 끝난 뒤 → **여기(C)** → D(섹션 제작). `03-reference-renewal` 2→3단계 사이.

## 선행 게이트 (먼저 확인)
- [ ] **작업 방식 판별됨?** HTML 네이티브 vs EZ 엎기 (`ez/` 폴더 유무). 안 됐으면 먼저 선언 — base가 이기는 경로가 달라짐.
- [ ] **접속·skin_code 확인됨?** (`/접속세팅`)
- [ ] **B단계 실측 끝남?** (`/요소측정` 또는 Figma MCP — 색·폰트·간격 숫자)

## 1. base 전수 스캔 (함정을 사람이 아닌 기계가 색출)
새 클라 base CSS를 7종 grep으로 훑어 `brain/docs/BASE-CSS-MAP.md` 생성·검증.
- 잡는 것: 고정폭 · 파란색 · 강제폰트 · 가상요소선 · echosting 이미지 · `!important` · 태그누수
- **상세 절차**: `brain/docs/CAFE24-SMARTDESIGN-AGENT.md` STEP 2
- → reset이 못 잡는 **이 클라 고유 함정**을 맵에 보강 (게시판·주문·회원 등 안 본 페이지까지 사전 포착)

## 2. nk-cafe24-reset.css 적용 (밑칠 제거)
- 업로드: `/_nk/css/nk-cafe24-reset.css`
- custom.css **맨 위**: `<!--@css(/_nk/css/nk-cafe24-reset.css)-->`
- 커스텀할 페이지: `<body id="main" class="nk-skin">`
- 안 먹으면 `body#main.nk-skin` 으로 명시도 보강
- **상세 사용법**: `.claude/skills/cafe24/snippets/css/nk-cafe24-reset-사용가이드.md`

## 3. 디자인 토큰 세팅 (실측값을 변수로 — 하드코딩 금지)
B단계 실측치(색·폰트·간격)를 CSS 변수로 박는다:
- 색: `:root { --nk-point: #브랜드색; }` (reset의 카페24 파란색 자리 위임)
- 폰트: **Pretendard**, 아이콘: **Phosphor** (CDN)
- 간격·타이포: 측정값을 토큰으로 (값 직접 박지 말 것 → 나중에 한 줄로 수정)
- Figma→토큰 자동 파이프라인: `.claude/skills/cafe24/design-tokens/`

## 4. 컴포넌트 갤러리 (부품 새로 짜기 — 준비물 ②)
토큰(값)만 깔고 D로 넘어가면 섹션마다 버튼·카드·폼을 **매번 새로 지어내** 톤이 들쭉날쭉해진다.
여기서 부품을 **토큰 기반으로 미리 조립해 확정**해두면, D단계는 재사용만 하면 된다.
- 3단계 토큰을 기반으로 `/_nk/css/nk-components.css` 작성 — 버튼(`.nk-btn`)·폼(`.nk-field`/`.nk-form-row`)·카드(`.nk-card`/`.nk-prd-card`)·배지·탭·페이지네이션·빈 상태 등
- `example-gallery.html` 진열대로 한 페이지에 모아 **로컬 QA**(깨짐·톤 확인)
- D단계 지시 문구: "이 몰의 갤러리 부품(`.nk-btn--primary`, `.nk-form-row`, `.nk-card`)을 **그대로 재사용**해. 새로 지어내지 마."
- **상세**: `.claude/skills/cafe24/component-gallery/` (README·example-gallery.html·gallery.schema.json)

> 준비물 3종: ① 토큰(3단계) → ② 컴포넌트 갤러리(4단계) → ③ 브랜드 프로필(`.claude/skills/cafe24/brand-profile/`).

## 완료 기준 (충족해야 D로)
- [ ] `BASE-CSS-MAP.md` 생성됨
- [ ] reset 로드 + `body.nk-skin` 적용 → 라이브에서 base 함정(고정폭·파란색·가짜선) 사라짐 (PC+모바일 스크린샷)
- [ ] `--nk-point` 등 토큰이 `:root`에 세팅됨
- [ ] `nk-components.css` 부품 세팅 + `example-gallery.html` 로컬 QA 통과 (버튼·폼·카드 등 렌더·톤 확인)
→ 충족되면 **D단계(`/디자인수정`)** 섹션 제작 진입 — 갤러리 부품을 재사용해 조립.

> 연계: 전체 흐름은 `/카페24-워크플로우` → `03-reference-renewal`. 이 단계는 그 2~3단계 사이의 "토대".
