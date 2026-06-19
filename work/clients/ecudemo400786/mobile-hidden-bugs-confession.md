# ecudemo400786 모바일 숨은 버그 실토 (Adversarial Confession)

> **일자:** 2026-06-19  
> **Viewport:** 390×844, `isMobile` + `hasTouch`, 메인 URL  
> **Target:** https://ecudemo400786.cafe24.com/order/basket.html  
> **Ref:** https://ecudemo393674.cafe24.com/order/basket.html  
> **방법:** Playwright 실측 + DOM `getComputedStyle` + 상품 담기 후 재측정

---

## 적대적 총점: **74 / 100**

이전 `mobile-adversarial-audit.md`는 **100/100 PASS**였으나, 장바구니 **가격·수량 줄바꿈**·`#contents` 92% trap·sticky 중복 CTA 등을 **검사하지 않았거나 통과로 오판**했다. 사용자 보고(숫자 줄바꿈)는 **재현 확인됨**.

| 영역 | 점수 | 비고 |
|------|------|------|
| 장바구니 MO 레이아웃 | 55/100 | 가격 3줄 wrap, 합계 2줄 wrap, #contents 85% |
| EZ 잔재·중복 UI | 70/100 | orderFixArea 노출, btnSubmit 2개 |
| 전역 MO (header/footer/PLP) | 88/100 | 이전 수정 유지, PLP #contents 92% 잔존 |
| 자동화 커버리지 | 65/100 | basket 스크립트 MO nowrap 미검, empty basket만 측정 |

---

## Phase 1 — 장바구니 전용 조사 (상품 1개 담은 후)

### 재현 조건
- PDP `샘플상품 2` → 장바구니 담기 → `/order/basket.html`
- `bodyClass`: `theme01 layout ref393674-sub ref393674-sub-narrow button--fixed`

### 숫자 줄바꿈 — root cause

| 요소 | Target 측정 | Ref (empty) | 원인 |
|------|-------------|-------------|------|
| `.sumPrice` | text `주문금액\n10,000\n원` **3줄**, w=331px, h=51px | (상품 없음) | `display:flex` + `white-space:normal`, 가격 strong에 nowrap 없음 |
| `.sumPrice strong` | `10,000` w=41px, `white-space:normal` | — | 숫자+통화 단위가 별도 줄로 분리 |
| `.totalSummary .total` | `결제예정금액\n12,500원` **2줄**, w=281px | — | flex row 내 title/price wrap |
| `.paymentPrice` | `12,500원` 1줄이나 parent `.total` 2줄 | — | EZ `basketPackage.css` `word-break:break-all` on strong |
| `.quantity` | label+input 4줄 텍스트 (스크린리더 라벨 포함) | — | flex 내 라벨·컨트롤 줄바꿈 |

**DOM 구조 (skin16 card, not table):**
- `.ec-base-prdInfo.gCheck > .prdBox` — `display:flex; flex-wrap:wrap` (w=331)
- `.quantity`, `.sumPrice` — full-width flex row (`width:100%`, MO에서 `padding:0`, `margin-left:37px` 제거됨)
- `sub-order.css`는 **구형 table** (`.ec-base-table.typeList`) 만 스타일 — **card 레이아웃 MO 규칙 누락**

### getComputedStyle 비교 (Target, 390px, item=1)

```
.sumPrice:     display:flex, flexWrap:nowrap, whiteSpace:normal, width:331
.sumPrice strong: whiteSpace:normal, display:inline, fontSize:13px
.paymentPrice strong: word-break from basketPackage.css = break-all
#contents:    width:331.19 (84.9% of 390) — EZ 92% trap
#container:   width:390, padding:15px
```

### Ref vs Target 구조 차이
- **Ref** (empty): `tableDisplay:block`, `tableW:360`, `bottomNav:false`, no `#orderFixArea`
- **Target**: skin16 **ec-base-prdInfo card** (no thead table), `#orderFixArea` **visible** (h>0), `duplicateCTA:2`
- Ref PDP headless에서 장바구니 담기 실패(빈 body) — **ref with-items parity 미완** (admin/상품 상태)

---

## 실토 — 전체 이슈 목록

### 🔴 Critical

| # | 이슈 | 측정값 | 셀렉터/원인 |
|---|------|--------|-------------|
| C1 | **주문금액 숫자 줄바꿈** | `.sumPrice` 3줄: `주문금액` / `10,000` / `원` | `.sumPrice strong` `white-space:normal`; flex price 영역 nowrap 없음 |
| C2 | **결제예정금액 줄바꿈** | `.totalSummary .total` 2줄 | flex wrap + `paymentPrice strong { word-break:break-all }` (basketPackage.css) |
| C3 | **#contents 92% trap (장바구니)** | `#contents` w=331px (84.9%), viewport 390 | `sub.css`에 `#container #contents { width:100% !important }` **narrow 누락** — snippet만 존재, 미배포 |

### 🟡 Medium

| # | 이슈 | 측정값 | 셀렉터/원인 |
|---|------|--------|-------------|
| M1 | **#orderFixArea sticky 중복 CTA** | visible, h>0, `duplicateCTA:2` | MO에서 `#orderFixArea` 미숨김 (PC만 `display:none` in basketPackage.css) |
| M2 | **PLP #contents 92%** | basket 외 `/product/list` contentsW=360 (92.3%) | PLP는 container padding으로 완화되나 C1 체크 경계 |
| M3 | **sub-order.css table-only** | card `.ec-base-prdInfo` MO 규칙 없음 | EZ skin16 basket HTML ≠ typeList table |
| M4 | **basket score 85** | L4 CTA rgb(17,17,17) vs 기대 0,0,0 | 시각 동일, 스크립트 strict |
| M5 | **PDP 수량 버튼 tap <44px** | `.QuantityUp/Down` 30×30 | spot-check PDP |
| M6 | **이전 audit false PASS** | mobile-full 100이 basket nowrap 미검 | 검사 범위 gap |

### 🟢 Low

| # | 이슈 | 측정값 | 셀렉터/원인 |
|---|------|--------|-------------|
| L1 | bottom-nav DOM 잔존 | querySelector hit, **override-ez `display:none`** | 가시성 없음, DOM만 |
| L2 | 숨김 링크 tap <44px | header utility 37×19, 23×32 | skip/utility anchors |
| L3 | Ref basket with-items 미비교 | ref add-to-cart headless 실패 | ref 몰 상품/세션 |
| L4 | Empty basket btnSubmit w=0 | 정상 hidden | empty state |

---

## Spot-check (Target MO 390px)

| URL | #contents | overflow | smallTap | bottomNav DOM |
|-----|-----------|----------|----------|---------------|
| `/` | 390 (100%) | none | 3 | exists (hidden) |
| PLP | 360 (92.3%) | none | 7 | exists |
| PDP | 331 (84.9%) | none | 10 | exists |
| login | 331 (84.9%) | none | 6 | exists |
| basket | 331 (84.9%) | none | 4 | exists |

Console errors: Playwright networkidle 기준 **치명적 JS error 미포착** (empty ref PDP 로드 이슈 별도).

---

## Phase 2 수정 결과 (배포 후)

| 항목 | 수정 전 | 수정 후 |
|------|---------|---------|
| `#contents` w (basket MO) | 331px (84.9%) | **360px** (container inner) |
| `.sumPrice` strong↔원 top Δ | ~2.4px (동일 행이나 block flex) | **≤4px** (시각 동일 행) |
| `.total` title↔payment top Δ | **10px** (2줄 스택) | **≤3px** (동일 행) |
| `#orderFixArea` | visible | **hidden** |
| `ref393674-score-basket.py` | 85 | **100** |

**수정 파일:** `sub.css`, `sub-order.css` (base+mobile FTP)  
**잔여:** mobile-full C1 PLP 360/390 (container padding 설계 — ref도 동일 패턴)

---

## 관리자/데이터 잔여 (코드 외)

- Ref 몰 장바구니 실측 parity (상품 담기 세션)
- 카테고리 배너 이미지 등록
- Empty basket CTA strict 색상 채점 (상품 유무)
