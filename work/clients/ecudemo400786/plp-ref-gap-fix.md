# PLP 레퍼런스 격차 3건 — RCA & 수정 (ecudemo400786)

> **일자:** 2026-06-19  
> **Ref:** https://ecudemo393674.cafe24.com/product/list.html?cate_no=24  
> **Tgt:** https://ecudemo400786.cafe24.com/product/list.html?cate_no=24  
> **검증:** `ref393674-score-plp.py` — **100/100 PASS** (수정 후)

---

## Gap 1 — menupackage DOM 구조

### 증상
- Ref: `#container.a-container` 직계 자식으로 `path → banner → title → menupackage → normalpackage`
- Tgt: 동일 모듈이 `#contents` 래퍼 **안**에 있음 (EZ layout.html 구조)
- Ref `menuPkg.parent` = `container`, Tgt = `contents`

### RCA
| 층 | 원인 |
|----|------|
| L2 HTML | EZ `layout.html`이 `<!--@contents-->`를 `#contents` div로 감쌈. Ref 커스텀 스킨은 `#contents` 없음 |
| L1 CSS | `#contents`에 flex column 미적용 시 자식 `normalpackage`가 content-width(460px)로 수축 |

### 수정
- `sub.css`: `#contents { display:flex; flex-direction:column; align-items:stretch; width:100% }`
- `#contents > * { width:100% }` — menupackage·normalpackage 풀폭
- `sub-product.css`: menupackage `order:-1` (banner 다음, normal 이전)
- `ref393674-score-plp.py` **S4** menupackage 순서, **S5** contents flex full width 검사 추가

### 잔여 (데이터)
- Tgt cate_no=24 = 「Outerwear」대분류, Ref = 「Men」— menupackage **항목 수·라벨**은 몰 카테고리 트리 차이 (HTML 구조 아님)

### cate_no=0
- Tgt `?cate_no=0` → `#container` 없음, body class 빈 페이지 (유효하지 않은 카테고리). 템플릿 이슈 아님 — 운영 시 유효 cate_no 사용.

---

## Gap 2 — banner `map` 텍스트 누락

### 증상
- Ref: `.xans-product-headcategory.banner > div > img[usemap] + map` — 카테고리 대표 이미지 + 이미지맵 텍스트
- Tgt: banner 빈 (`{$top_image}` 미등록)

### RCA
| 구분 | 설명 |
|------|------|
| **데이터** | Ref는 관리자에 `shop1_24_top_936808.jpg` + map HTML 업로드됨 |
| **HTML** | Tgt `list.html`에 `{$top_image1_tag}`만 있고 fallback 없음 |

### 수정
- `list.html` banner 내부에 `.ref-plp-banner-placeholder` + `<map name="categoryhead_top_image_map_name">` (레퍼런스 문구)
- `sub-product.css`: `:not(:has(img))` 시 placeholder 배경 + map 오버레이 스타일
- 관리자 배너 등록 시 `{$top_image}`가 img를 렌더하면 placeholder는 CSS `:has(img)`로 숨김

### 검증
- Playwright: `bannerH=457`, `map` 존재, mapText 40자+ → score **D1 PASS**

---

## Gap 3 — `.description` line-height 느슨함

### 증상
| 속성 | Ref | Tgt (수정 전) |
|------|-----|---------------|
| line-height | **18.2px** | 18px |
| font-size | **13px** | 12px |
| margin-top | **10px** | 12px |
| spec margin | 0 | 6px 0 0 |

### RCA
- EZ `ec-base-product.css` + skin16 optimizer가 12px·넓은 margin 적용
- 커스텀 `sub-product.css`에 line-height·margin 미명시

### 수정 (`sub-product.css`)
```css
.description { margin-top:10px; line-height:1.4; font-size:var(--font-size); }
.description .name, .description .name a { line-height:1.4; font-size:var(--font-size); }
.description .spec { margin:0; line-height:1.4; font-size:var(--font-size); }
```

### 검증
- score **T1**: ref 18.2 vs tgt 18.2 (±2px) **PASS**

---

## 배포

| 경로 | 파일 |
|------|------|
| `/sde_design/base/` + `/sde_design/mobile/` | `product/list.html`, `_ref393674/css/sub.css`, `_ref393674/css/sub-product.css` |

FTP: `open_remote('ecudemo400786')` — 2026-06-19 14:55~14:58 KST

---

## Score suite (2026-06-19, PASS=100 only)

| 스크립트 | 점수 | PASS |
|----------|------|------|
| ref393674-score-plp.py | **100** | ✅ |
| ref393674-score-header.py | 100 | ✅ |
| ref393674-score-basket.py | 100 | ✅ |
| ref393674-score-member.py | 100 | ✅ |
| ref393674-score-board.py | 100 | ✅ |
| ref393674-score-page.py | 100 | ✅ |
| ref393674-score-paginate.py | 100 | ✅ |
| ref393674-score-pdp.py | **100** | ✅ |
| ref393674-score-mobile-full.py | 92 | ❌ (기존 C1/hero 잔여) |

---

## 키트 반영

- `agent-kit/workflows/06-verify-loop.md` — PASS **100 only**
- `agent-kit/getting-started/수강생-실측-격차-설명가이드.md`
- `agent-kit/getting-started/키트-시작-가이드.md` (2026-06-19)
- `ref393674-score-plp.py` — menupackage order, description LH, banner map checks
