# PDP 레퍼런스 격차 — RCA & 수정 (ecudemo400786)

> **일자:** 2026-06-19  
> **Ref:** https://ecudemo393674.cafe24.com/product/sample-product-01/11/category/24/display/1/  
> **Tgt:** https://ecudemo400786.cafe24.com/product/샘플상품-2/10/category/24/display/1/  
> **검증:** `ref393674-score-pdp.py` — **100/100 PASS**

---

## 초기 점수 (수정 전)

| viewport | score | 실패 추정 |
|----------|-------|-----------|
| PC 1440 | ~90 | container 풀폭·padding·2열 레이아웃 |
| MO 390 | 0–10 | `#contents` 92% trap → containerW ≈359 |
| **total** | **91** | 100/110 |

---

## 근본 원인 (4가지)

### 1. PDP가 `ref393674-sub-narrow` 로 분류됨

- 초기 `sub.css` 가 모든 서브에 `max-width:1200px` 적용
- `layout.js` `detectSubPageType()` 이 `product_detail` 미감지 시 `narrow` 반환
- **증상:** containerW ≈1200, padding `50px 20px 100px` (기대 PDP: 100% / `20px 20px 100px`)

### 2. EZ `#contents` 92% trap (MO)

- skin16 `layout.css` `@media (max-width:1024px)` → `#container #contents { width:92% }`
- PDP용 `#container #contents { width:100% !important }` 미적용
- **증상:** MO containerW ≈359 (score **M1** FAIL → total 91)

### 3. `detailArea` 2열·`infoArea` sticky 미적용

- EZ `detail.css` 기본 block 레이아웃
- `sub-product.css` 에 flex 2열·sticky·`btnSubmit` 다크 CTA 없음
- **증상:** L1 flex 2열, L2 sticky, L3 areaW &lt;1200, L4 btnSubmit 색상 FAIL

### 4. path breadcrumb 노출

- EZ 기본 `.path` 표시
- **증상:** S4 path 숨김 FAIL (ref는 `display:none`)

---

## 수정

| 파일 | 변경 |
|------|------|
| `_ref393674/js/layout.js` | `[module="product_detail"]` / `.xans-product-detail` → `ref393674-sub-pdp` |
| `_ref393674/css/sub.css` | `ref393674-sub-pdp` container 100%, padding `20px 20px 100px`, `#contents width:100% !important` |
| `_ref393674/css/sub-product.css` | `.detailArea` flex 2열, `.infoArea` sticky, `.btnSubmit` `#000`, h1 `var(--font-display)`, MO column stack |
| `product/detail.html` | ref 탭 마크업(`tabProduct_box`)·gallery 구조 유지 (skin16 EZ 템플릿) |
| `sub.css` (공통) | `.path` / `.section.path` `display:none` |

---

## 배포

| 경로 | 파일 |
|------|------|
| `/sde_design/base/` + `/sde_design/mobile/` | `product/detail.html`, `_ref393674/css/sub.css`, `_ref393674/css/sub-product.css`, `_ref393674/js/layout.js` |

FTP: `open_remote('ecudemo400786')` — 2026-06-19 18:06 KST

---

## 검증 (PASS 후)

```json
{
  "total_score": 100,
  "pass": true,
  "PC": { "containerW": 1440, "containerPad": "20px 20px 100px", "areaDisplay": "flex", "infoPos": "sticky", "areaW": 1280 },
  "MO": { "containerW": 390 }
}
```
