# 06 — 외부 디자인 시스템·코드 → 카페24 적응

> 사용자가 **디자인 시스템(DS) + HTML/CSS/JS 코드**를 제공하면, 그대로 붙이지 않고 **카페24 SmartDesign HTML 규칙**에 맞게 변환한다.  
> 인입 절차: `agent-kit/01_작업하기/workflows/05-reference-intake.md` · 구현: 본 문서 + `05-module-shell-rebuild.md`.

---

## 0. 입력물 (사용자가 줄 것)

| 입력 | 저장 위치 | 용도 |
|------|-----------|------|
| DS 토큰 (색·타이포·간격·radius) | `clients/{몰}/04_design/design.md` + `src/_nk/css/nk-tokens.css` | `:root` 변수 — **하드코딩 금지** |
| 컴포넌트 HTML/CSS | `clients/{몰}/03_references/source/` | 변환 원본 (git OK, 비밀 X) |
| 레퍼런스 URL (선택) | `03_references/links.md` | 실측 교차검증 |
| Figma (선택) | MCP Figma | 토큰·spacing 실측 |

**에이전트는 제공 코드를 Read한 뒤** `design.md`에 「원본 → 카페24 매핑표」를 먼저 쓰고, 사용자 **「예」** 후 HTML/CSS 생성.

---

## 1. 변환 파이프라인 (순서 고정)

```
① Read  사용자 DS + 코드 + (레퍼런스)
  ↓
② Map   design.md — 토큰·컴포넌트·페이지 타입 표
  ↓
③ Stock  css/module + layout/basic/css 인벤토리 (05 §1)
  ↓
④ Adapt  Layer1 module KEEP + Layer2 nk-* (05 §2–3)
  ↓
⑤ Verify parity + 4-tier + visual (08)
```

---

## 2. DS 토큰 → `nk-tokens.css`

| 원본 (예: Tailwind/Figma) | 카페24 |
|---------------------------|--------|
| `--color-primary` | `--nk-theme` |
| `--color-accent` | `--nk-accent` |
| `--font-sans` | Pretendard (한글) — 클라 지시 우선 |
| `--spacing-4` | `--nk-gap` / `--nk-padding-x` |
| `--radius-md` | `--nk-radius` |

규칙:

- **italic/oblique 금지** (전역 룰)
- hex는 `:root`에만 — 컴포넌트 CSS에 `#fff` 반복 금지
- Phosphor Icons CDN — 다른 아이콘 라이브러리 혼용 금지

```css
/* clients/{몰}/src/_nk/css/nk-tokens.css — design.md 와 1:1 */
:root {
  --nk-theme: /* DS primary */;
  --nk-accent: /* DS accent */;
  /* … */
}
```

---

## 3. 컴포넌트 코드 → 카페24 조각

### 3-A. 변환 체크리스트 (컴포넌트 1개마다)

| 원본 | 카페24 적응 |
|------|-------------|
| `<div class="card">` | `.nk-prd` / `.nk-card` — `nk-` 접두사 |
| React/Vue 컴포넌트 | 정적 HTML + `<!--@import-->` 조각 |
| `onClick` / SPA 라우터 | 카페24 링크 `{$param}` · `{$link_product_detail}` |
| `<img src="fixed">` | 상품: `{$image_medium}` · 배너: `/web/upload/…` 또는 관리자 |
| Grid/Flex 레이아웃 | 유지 — 단 **ec-base-product width%** 와 충돌 시 `width:100%` (F-grid) |
| inline `style=""` | **금지** → 클래스 |
| `<section>` 풀블리드 | `margin:0!important` (section 120px 함정) |

### 3-B. 페이지 조립 구조

```
layout/basic/layout.html     ← @css custom.css · nk-cafe24-reset · nk-tokens
layout/basic/main.html       ← @layout + 섹션 @import 만
_nk/inc/header.html          ← module="Layout_*" + nk-header
_nk/inc/prd.html             ← listmain anchorBoxId 내부 (변수 scope)
_nk/css/nk-header.css        ← 조각 첫 줄 @css 자기완결
```

index/main = **마크업 0** — 섹션 나열 + import만.

### 3-C. DS 컴포넌트 ↔ 카페24 module 매핑표 (design.md §)

| DS 컴포넌트 | 카페24 위치 | module | 비고 |
|-------------|-------------|--------|------|
| ProductCard | `_nk/inc/prd.html` | listmain 내부 | `{$image_medium}` `{$link_product_detail}` |
| SiteHeader | `_nk/inc/header.html` | Layout_LogoTop 등 | logotop.css 오버라이드 필수 |
| PrimaryButton | `.nk-btn` | member/order | `.nk-btn--accent` 1종만 골드 |

---

## 4. 제공 CSS 처리 원칙

1. **전역 utility class** (`.flex`, `.gap-4`) → `nk-base.css` 또는 도메인 CSS로 **이름 nk-화**
2. **stock과 같은 속성** (border, color on `.ec-base-*`) → 병행 셀렉터 (`04-html-css-parity.md`)
3. **`css/module` 직접 수정** — greenfield·재판매 템플릿만. **클라 운영 스킨**은 `_nk` 오버라이드 우선 (AGENT §12)
4. body 끝 로드 CSS (`sub_style.css` 등) — specificity 한 단계 올려 이김

---

## 5. 사용자 코드 인계 시 에이전트 Read Order

1. `clients/{몰}/04_design/design.md` (없으면 템플릿 생성)
2. `03_references/source/**` — 사용자 제공 코드 **전부 Read**
3. `05-module-shell-rebuild.md` §1 — stock CSS 인벤토리
4. 변환 매핑표 초안 → **사용자 승인**
5. Wave 순 (`blank-slate-rebuild-queue.md`) — **한 페이지 타입 PASS 후 다음**

---

## 6. 산출물 체크리스트

- [ ] `design.md` — 토큰표 + 컴포넌트↔module 매핑 + 페이지 타입
- [ ] `nk-tokens.css` — DS 숫자 반영
- [ ] `03_references/source/` — 원본 보존 (diff 추적)
- [ ] `blank-slate-rebuild-queue.md` — module 유닛 표
- [ ] `css-module-inventory.md` — stock CSS 분석
- [ ] 변환본은 `_nk/` 만 — system `layout/basic` 직접 수정 최소

---

## 7. Human gates

- DS에서 **브랜드 폰트·팔레트 변경** — 사용자 확인
- EZ 제거 — 사용자 명시
- FTP upload — 사용자 OK
- 레퍼런스 1:1 주장 — `visual-verdict` + agy/codex (워크스페이스 룰)
