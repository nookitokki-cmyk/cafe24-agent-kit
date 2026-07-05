# Blank-slate rebuild queue — {몰ID}

> **정본 순서**: 메인 → PLP → PDP → auth-order → board → myshop → member → etc  
> **한 페이지 타입 전 module PASS** 전 다음 타입 착수 금지.  
> **방법론**: `references/05-module-shell-rebuild.md` · **DS 적응**: `references/06-design-system-adaptation.md`

**갱신**: {YYYY-MM-DD} · **design.md**: `04_design/design.md` · **DS 소스**: `03_references/source/`

**상태**: `—` · `WIP` · `분석완료` · `구현완료` · `4tier-PASS` · `FAIL` · `수용`

---

## §0 Wave0 선행 (타입 작업 전 1회)

| # | 작업 | 산출물 | 상태 |
|---|------|--------|:---:|
| W0-1 | SFTP pull `css/module` + `layout/basic/css` | `src/css/module/` | — |
| W0-2 | css/module 7종 grep | `css-module-inventory.md` | — |
| W0-3 | DS·코드 Read → 토큰 | `nk-tokens.css` + `design.md` | — |
| W0-4 | `nk-cafe24-reset.css` + Foundation | body `#main.nk-skin` | — |

---

## §1 메인 (`/`)

**소스**: `layout/basic/main.html` · `_nk/inc/header.html` · `_nk/inc/footer.html`

### §1-A 페이지 게이트

| URL | css/module 분석 | 유닛 표 | nk HTML | nk CSS | module tier | page tier | 상태 |
|-----|:---:|:---:|:---:|:---:|:---:|:---:|---|
| `/` | — | — | — | — | — | — | — |

### §1-B 모듈 유닛 표

#### `Layout_LogoTop` · `css/module/layout/logotop.css`

| # | 유닛 DOM | KEEP (변수·id·name) | NEW nk-* | stock CSS 셀렉터 | parity 병행 | 상태 |
|---|----------|---------------------|----------|------------------|-------------|:---:|
| 1 | `.xans-layout-logotop` | module 래퍼 | `.nk-header__logo` | `.xans-layout-logotop` margin/width | §header logotop | — |

#### `product_listmain_1` · `css/module/product/listmain*.css`

| # | 유닛 DOM | KEEP | NEW nk-* | stock CSS | parity | 상태 |
|---|----------|------|----------|-----------|--------|:---:|
| 1 | `div[module]` | `$count` 등 주석 | `.nk-sec` | `.ec-base-product` | `.nk-sec .ec-base-product` | — |
| 2 | `li#anchorBoxId_{$product_no}` | **≥2블록** | `.nk-prd` | `.prdList > li{width:25%}` | grid width 100% | — |
| 3 | 카드 내부 | `{$image_medium}` … | `@import prd.html` | `.description` margin | nk-prd desc | — |

<!-- 모듈마다 §1-B 블록 복제 — wave4-page-queue §1-B 인벤토리와 1:1 -->

### §1-C module 밖 섹션

| 섹션 | module | 파일 | nk CSS | 상태 |
|------|--------|------|--------|:---:|
| `.nk-hero` | 없음 | `_nk/inc/hero.html` | `nk-hero.css` | — |
| `.nk-topbar` | 없음 | `_nk/inc/topbar.html` | `nk-base.css` | — |

---

## §2 PLP

**소스**: `product/list.html`

### §2-A 페이지 게이트

| URL | css/module 분석 | 유닛 표 | nk HTML | nk CSS | module tier | page tier | 상태 |
|-----|:---:|:---:|:---:|:---:|:---:|:---:|---|
| `/product/list.html?cate_no={N}` | — | — | — | — | — | — | — |

### §2-B 모듈 유닛 표

#### `product_listnormal` · `css/module/product/listnormal.css`

| # | 유닛 DOM | KEEP | NEW nk-* | stock CSS | parity | 상태 |
|---|----------|------|----------|-----------|--------|:---:|
| 1 | | | | | | — |

---

## §3 PDP

**소스**: `product/detail.html`

### §3-A 페이지 게이트

| URL | … | 상태 |
|-----|---|:---:|
| `/product/…/{product_no}/` | — | — |

### §3-B 모듈 유닛 표

#### `product_detail` · `product_image` · `product_option` …

(submodule: `image_zoom2.html` · `recommend_mail.html` — **submodule tier** 별도 행)

---

## §4 auth-order · §5 board · §6 myshop · §7 member · §8 etc

> 타입 착수 시 위 §1 패턴으로 **페이지 게이트 + 모듈 유닛 표** 섹션 추가.  
> 전체 URL 목록: `wave4-page-queue.md`

---

## §9 진행 요약

| 타입 | module 수 | 분석완료 | 4tier-PASS | 비고 |
|------|:---:|:---:|:---:|---|
| 1 메인 | | 0 | 0 | |
| 2 PLP | | 0 | 0 | |
| 3 PDP | | 0 | 0 | |
| … | | | | |

**다음 액션**: Wave0 W0-1 SFTP pull → `css-module-inventory.md` 초안
