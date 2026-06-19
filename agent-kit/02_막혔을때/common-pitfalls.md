# 공통 함정 — 서브페이지 narrow 레이아웃 사례 (postmortem)

> **사건:** ecudemo400786 초기 구현에서 PLP·PDP까지 **max-width 1200px** 로 잘못 좁혀짐.  
> **교훈:** 「서브페이지 = narrow」 가정은 EZ skin16에서 치명적이다.

---

## 증상

- PLP `product/list.html` 에서 `prdList` 폭이 ~1160px (기대 ~1420px)
- `body` 에 `ref393674-sub-narrow` 가 붙고 `#container` max-width 1200px
- 레퍼런스는 PLP container 100% + padding 50px 20px 100px

---

## 근본 원인 (4가지)

### 1. EZ skin16 `#contents` 92% trap (반복 사고)

skin16 `layout.html` 은 `#container` > `#contents` > `@contents` 구조.  
MO `@media (max-width:1024px)` 에 EZ `layout.css` 가 **`#container #contents { width:92%; margin:0 auto }`** (specificity **512**) 를 건다.

**흔한 실수:** `body.layout #contents { margin:0 }` 만 추가 (specificity **305**) → margin은 0이지만 **width 92% 유지** → 히어로·배너 좌우 흰 gap.

**필수 규칙:** [`brain/rules/ez-contents-width.md`](../brain/rules/ez-contents-width.md) — **`#container #contents` + `width:100% !important`**. 스니펫: [`brain/docs/snippets/ez-contents-override.css`](../brain/docs/snippets/ez-contents-override.css).

**예방:** 인입 단계 HTML 구조 격차표에 `#contents` 유무·**390px computed width** 기록.

### 2. 모든 서브페이지에 동일 container 규칙 적용

초기 `sub.css` 가 `body.layout.ref393674-sub #container` 에만 1200px 를 걸어, PLP·PDP까지 narrow 처리.

**예방:** 페이지 타입 표에서 **plp-full / pdp-full / narrow** 를 Phase 0 이전에 확정 (`05-reference-intake.md`).

### 3. CSS 오버레이만으로 HTML 구조 불일치 해결 시도

`list.html`·`list_product.html` 구조(banner, menupackage, sortby ul) 없이 `sub-product.css` 만 추가 → menupackage·배너·4열 grid FAIL.

**예방:** 레퍼런스 DOM 스냅샷과 타겟 module 마크업 대조 후 CSS.

### 4. `layout.js` page-type 감지 누락

`detectSubPageType()` 이 main/plp/pdp 외 전부 `narrow` 반환 → PLP도 `ref393674-sub-narrow`.

**예방:** module 셀렉터(`product_normalpackage`, `product_detail`) 로 타입 분기 후 body class 분리.

---

## 올바른 타입별 container (maeve 실측)

| 타입 | body class | container max-width | padding (PC) |
|------|------------|---------------------|--------------|
| hero-main | `ref393674-main` | 100% | 0 |
| plp-full | `ref393674-sub-plp` | 100% | 50px 20px 100px |
| pdp-full | `ref393674-sub-pdp` | 100% | 20px 20px 100px |
| narrow | `ref393674-sub-narrow` | 1200px | 50px 20px 100px |

---

## 예방 체크리스트 (구현 전)

- [ ] 페이지 타입 표 작성 완료 (PLP ≠ narrow 명시)
- [ ] 타입별 대표 URL 에서 ref `getComputedStyle` 실측
- [ ] `#contents` · `titleArea` · sort UI (ul vs select) 구조 격차 기록
- [ ] **`#container #contents` width override** — override CSS 첫 블록 (`brain/rules/ez-contents-width.md`)
- [ ] DevTools 390px: `#contents` width = viewport (359px ≈ 92% trap **FAIL**)
- [ ] `layout.js` 에 plp/pdp/narrow 분기 존재 확인
- [ ] Phase 1 PLP score 스크립트로 containerW ≥ 1400 검증
- [ ] `ref393674-score-mobile-full.py` **C1** `#contents` viewport width PASS

---

## 관련 파일 (ecudemo400786)

- `work/deploy-ec400786/_ref393674/css/sub.css` — 타입별 container
- `work/deploy-ec400786/_ref393674/js/layout.js` — `detectSubPageType()`
- `work/scripts/ref393674-score-plp.py` — PLP 회귀 방지

---

## EZ #contents 92% trap — full-bleed 실패 (postmortem)

> **사건:** ecudemo400786 모바일 히어로·배너 좌우 gap — **`margin:0`만 적용**, width 92% 잔존.  
> **교훈:** full-bleed = **부모 `#contents` width** 먼저. 자식 100vw·overflow 검사만으로는 부족.

### 증상 (MO 390px)

- `#contents` computed width ≈ **359** (viewport 390의 92%)
- `.main-sec1` 등 자식이 viewport에 닿아도 **좌우 body 배경(흰색) gap**
- PC는 92% 룰이 `@media (max-width:1024px)` 안에만 있어 덜 눈에 띔

### 근본 원인 (요약)

| # | 원인 |
|---|------|
| 1 | EZ `#container #contents { width:92% }` — specificity **512** |
| 2 | 에이전트가 `body #contents { margin:0 }` 만 복사 — **305**, width 속성 미충돌 |
| 3 | full-bleed CSS를 **자식**에만 적용, **부모 width** 미해제 |
| 4 | score 스크립트가 hero rect만 검사 — **`#contents` width** 미검사 (→ C1 추가) |

### 예방 체크리스트

- [ ] **필수 규칙:** [`brain/rules/ez-contents-width.md`](../brain/rules/ez-contents-width.md)
- [ ] override CSS **첫 블록:** `#container #contents { width:100% !important; margin:0 !important; }`
- [ ] 메인 + PLP + (해당 시) PDP/narrow 타입별 블록 (`brain/docs/snippets/ez-contents-override.css`)
- [ ] DevTools 390px: `#contents`.width === `document.documentElement.clientWidth` (±4px)
- [ ] verify-loop Phase 0 pre-flight + `ref393674-score-mobile-full.py` **C1** PASS
- [ ] R1 hero full-bleed — C1 통과 **후**에도 `.main-sec1` x ≤ 2 확인

### 관련 파일

- `brain/rules/ez-contents-width.md` — mandatory rule
- `brain/docs/snippets/ez-contents-override.css` — paste-ready
- `work/deploy-ec400786/_ref393674/css/base.css` — 메인 `#container #contents`
- `work/deploy-ec400786/_ref393674/css/sub.css` — 서브 타입별 (→ `#container #contents`로 강화 권장)

---

## PDP layout — body class·container 타입 (postmortem)

> **사건:** ecudemo400786 PDP 91점 — 2열 flex·sticky·풀폭 container FAIL.  
> **교훈:** PDP는 PLP와 동일하게 **pdp-full** 타입. `body.layout` 공통 셀렉터만으로는 `ref393674-sub-narrow` 오분류를 막지 못한다.

### 증상 (`ref393674-score-pdp.py`)

| 체크 | 기대 | 실패 시 |
|------|------|---------|
| S1 | `layout` + `ref393674-sub-pdp` | narrow class 붙음 |
| S2/S3 | container pad `20px 20px 100px`, width ≈1440 | 1200px narrow |
| L1 | `detailArea` flex, img/info 각 >300px | block·단열 |
| L2 | `infoArea` `position:sticky` | static/relative |
| L4 | `btnSubmit` 배경 `#000` | EZ theme 색 |

### 근본 원인

| # | 원인 |
|---|------|
| 1 | `layout.js` 가 PDP를 `narrow`로 분류 → `ref393674-sub-narrow` + max-width 1200px (**F29**) |
| 2 | `sub.css` 에 `ref393674-sub-pdp` 전용 `#container #contents` 블록 누락 (**F27**) |
| 3 | `sub-product.css` PDP 규칙이 `body.layout` 만 사용 — narrow class 시 container 규칙이 우선 |
| 4 | EZ `detail.css` / theme `btnSubmit` 이 `_ref` CTA 색 덮음 |

### 수정 패턴

- `layout.js`: `[module="product_detail"]` / `.xans-product-detail` → `ref393674-sub-pdp`
- `sub.css`: PDP container `max-width:100%`, pad `20px 20px 100px`, `#container #contents { width:100% !important }`
- `sub-product.css`: `.detailArea` flex 2열, `.infoArea` sticky, `.btnSubmit { background:#000 }`
- 배포: **base + mobile** 동시 (`F28`)

### 예방

- [ ] 인입 시 페이지 타입 표에 **pdp-full** 명시 (`05-reference-intake.md`)
- [ ] `ref393674-score-pdp.py` — 구현·배포 후 **100점**까지 루프
- [ ] DevTools: `body` class에 `ref393674-sub-pdp` 확인 (narrow 아님)

### 관련 파일

- `work/deploy-ec400786/_ref393674/js/layout.js`
- `work/deploy-ec400786/_ref393674/css/sub.css` (§PDP)
- `work/deploy-ec400786/_ref393674/css/sub-product.css`
- `work/scripts/ref393674-score-pdp.py`

---

## 모바일 별도 스킨 vs 반응형 (postmortem)

> **사건:** ecudemo400786 — PC는 maeve `_ref393674`, 실제 모바일(`/m/`)은 카페24 기본 EZ mobile 스킨.  
> **교훈:** `base/` 만 FTP 업로드하면 MO는 **완전히 다른 템플릿**이 서빙된다.

### 증상

- PC: `#header.a-header`, Women/Men GNB, hero 슬라이드
- `/m/`: 「카테고리펼침」, `mobile_ko_KR` 기본 UI, `_ref393674` 없음
- score 스크립트 MO 390 (메인 URL)은 PASS인데, 실제 `/m/` 방문 시 디자인 불일치

### 근본 원인 (4가지)

1. **Cafe24 EZ skin16 기본:** `/sde_design/mobile/` 별도 트리 존재
2. **관리자 「모바일 전용 디자인 사용」 ON** — `CAFE24.MOBILE_WEB=true` (레퍼런스 393674는 `false`)
3. **에이전트가 `/sde_design/base/` 만 배포** — mobile `layout.html`에 CSS 링크 없음
4. **검증이 `/m/` 이 아닌 메인 URL viewport만 사용** — mobile 스킨 불일치 미탐지 가능

### 예방

- [ ] `brain/rules/responsive-mobile.md` — MO = base `@media`, upload base only (mobile sync는 예외)
- [ ] **작업 시작 전·배포 후** 사용자에게 「모바일 전용 디자인 사용설정」**사용안함** 확인 요청 (관리자 수동 — MCP 불가)
- [ ] 인입 Q4: PC 1440 + MO 390 **동일 템플릿** 확정
- [ ] FTP 배포 후 `/sde_design/mobile/_ref393674` 존재 또는 관리자 mobile OFF 확인
- [ ] score 스크립트: 390×844 on **메인 URL** (not `/m/` unless unavoidable)
- [ ] 관리자: **쇼핑몰 설정 → 사이트 설정 → 쇼핑몰 환경 설정 → 모바일 → 기본설정 → 「모바일 전용 디자인 사용설정」 사용안함** ([Help](https://support.cafe24.com/hc/ko/articles/8466336842009))

### ecudemo400786 조치 (2026-06-19)

- `work/deploy-ec400786/` → base + mobile 동기화 (layout, `_ref393674`, pages, PLP)
- 상세: `work/clients/ecudemo400786/mobile-responsive-fix.md`

---

## MO 장바구니 가격·수량 줄바꿈 (postmortem)

> **사건:** ecudemo400786 MO 장바구니에서 `10,000` / `원` / `12,500원` 숫자가 줄바꿈.  
> **교훈:** EZ skin16 basket = **ec-base-prdInfo card** — `sub-order.css` table 규칙만으로는 부족.

### 증상 (390px, item≥1)

- `.sumPrice` innerText 3줄: `주문금액` / `10,000` / `원`
- `.totalSummary .total` 2줄: `결제예정금액` / `12,500원`
- `#contents` w≈331 (84.9%) — narrow 페이지 `#container #contents` override 누락

### 근본 원인

| # | 원인 |
|---|------|
| 1 | `basketPackage.css` `.paymentPrice strong { word-break:break-all }` |
| 2 | `.sumPrice` flex + `white-space:normal` — strong·통화 텍스트 노드 분리 |
| 3 | `sub-order.css`가 `.ec-base-table.typeList`만 타깃 (skin16 card 미적용) |
| 4 | `ref393674-sub-narrow`에 `#container #contents { width:100% !important }` 미배포 |
| 5 | MO `#orderFixArea` sticky CTA 중복 노출 |

### 수정 패턴 (`sub-order.css` @media max-width 1023px)

```css
.xans-order-basketpackage .ec-base-prdInfo.gCheck .sumPrice {
  flex-wrap: nowrap;
  white-space: nowrap;
}
.xans-order-basketpackage .totalSummary .paymentPrice strong {
  white-space: nowrap;
  word-break: normal;
}
.xans-order-basketpackage #orderFixArea { display: none !important; }
```

### 예방

- [ ] 장바구니 score: 상품 1개 담은 뒤 MO `sumPriceLines`·`totalLines` 검사 (`ref393674-score-basket.py` M3/M4)
- [ ] narrow 서브에 `#container #contents` 100% (`sub.css` + snippet)
- [ ] empty basket만 검사하지 말 것

### 관련 파일

- `work/deploy-ec400786/_ref393674/css/sub-order.css`
- `work/clients/ecudemo400786/mobile-hidden-bugs-confession.md`

---

## §전역 페이징 `ec-base-paginate` (postmortem)

> **사건:** ecudemo400786 **전 페이지**에서 `typeList` 페이징 깨짐 — 게시판·상품목록·검색·마이페이지 등 **동일 클래스** 20곳+.  
> **교훈:** EZ `font-size:0` 숨김 + body 끝 `sub_style.css` PNG 화살표는 **`#contents` 스코프 + body 끝 로드** 없이는 항상 깨진다.

### 증상

```html
<div class="ec-base-paginate typeList section">
  <a>이전 페이지</a>
  <ol><li><a class="this">1</a></li></ol>
  <a>다음 페이지</a>
</div>
```

- `이전 페이지` / `다음 페이지` 한글 노출 (`prevFontSize: 13px`)
- 번호 `border:1px` 박스, `.section` 시 좌우 margin 비대칭

### 근본 원인

| # | 원인 |
|---|------|
| 1 | EZ `ec-base-paginate.css` — `font-size:0` + `li a` border 박스 |
| 2 | head `sub.css`가 `.typeList a`에 font-size 복원 → `> a` 숨김 무력화 |
| 3 | **body 끝** `sub_style` / `sub_theme` / `add_layout` 이 head 커스텀보다 나중 |
| 4 | `add_layout.css` `#contents > .section` — 페이징 92% width trap |
| 5 | 게시판만 `sub-board.css` 수정 시 PLP·검색·typeSub 누락 |

### 수정 패턴

**`sub-paginate.css` — `layout.html` body 끝 `add_layout.css` 직후**

스니펫: [`brain/docs/snippets/ec-paginate-override.css`](../brain/docs/snippets/ec-paginate-override.css)

### 예방

- [ ] 페이징은 **`sub-paginate.css` 한 파일** — `sub.css`·`sub-board.css` 분산 금지
- [ ] `python work/scripts/ref393674-score-paginate.py` — board @390·1440

### 관련 파일

- `work/deploy-ec400786/_ref393674/css/sub-paginate.css`
- `work/clients/ecudemo400786/paginate-global-rca.md`
- `work/scripts/ref393674-score-paginate.py`

---

## PDP narrow trap + MO #contents 92% (postmortem)

> **사건:** ecudemo400786 PDP `ref393674-score-pdp.py` **91** — PC container 좁음 + MO `#contents` 92%.  
> **교훈:** PDP는 **plp-full과 별도 타입** (`ref393674-sub-pdp`). PLP 수정만으로 PDP가 자동 해결되지 않는다.

### 증상

| viewport | 측정 | 기대 |
|----------|------|------|
| PC | `body` = `ref393674-sub-narrow`, containerW ≈1200 | `ref393674-sub-pdp`, containerW ≈1440, pad `20px 20px 100px` |
| PC | `.detailArea` block, infoArea `relative` | flex 2열, infoArea `sticky` |
| PC | btnSubmit 밝은 EZ 테마색 | `#000` / `rgb(0,0,0)` |
| MO 390 | containerW ≈359 (`#contents` 92%) | containerW = viewport (390) |

### 근본 원인

| # | 원인 |
|---|------|
| 1 | `detectSubPageType()` 이 PDP 미감지 → `ref393674-sub-narrow` (1200px) |
| 2 | `sub.css`에 `ref393674-sub-pdp` 블록 없음 — padding·max-width PLP/narrow와 혼용 |
| 3 | `sub-product.css` PDP 레이아웃(flex·sticky·CTA) 미작성 |
| 4 | MO: PDP에 `#container #contents { width:100% !important }` 미배포 (F27 동일 패턴) |

### 수정 패턴

```css
/* sub.css — PDP 전용 */
body.layout.ref393674-sub-pdp #container.a-container {
  max-width: 100%;
  padding: 20px 20px 100px;
}
body.layout.ref393674-sub-pdp #container #contents {
  width: 100% !important;
  max-width: none !important;
  margin: 0 !important;
}

/* sub-product.css — 2열 + sticky + CTA */
body.layout .xans-product-detail .detailArea { display: flex; gap: 40px; }
body.layout .xans-product-detail .infoArea { position: sticky; top: calc(var(--header) + 30px); }
body.layout .xans-product-detail .xans-product-action .btnSubmit { background: #000; }
```

```js
// layout.js — product_detail 감지
if (document.querySelector('[module="product_detail"]')) return "pdp";
```

### 예방

- [ ] 페이지 타입 표: **pdp-full** ≠ plp-full ≠ narrow (`padding 20/20/100`)
- [ ] `layout.js` 에 `product_detail` / `.xans-product-detail` 분기
- [ ] Phase 1: `ref393674-score-pdp.py` — PC S1–L4 + MO M1
- [ ] MO 390: PDP `#contents` width = viewport (PLP F27과 동일 trap)

### 관련 파일

- `work/deploy-ec400786/_ref393674/css/sub.css` — `ref393674-sub-pdp`
- `work/deploy-ec400786/_ref393674/css/sub-product.css` — gallery·options·tabs·CTA
- `work/deploy-ec400786/_ref393674/js/layout.js`
- `work/clients/ecudemo400786/pdp-ref-gap-fix.md`
- `work/scripts/ref393674-score-pdp.py`

---

## §F35 · EZ GUI ↔ HTML 편집 충돌

> **한 줄:** Easy **타입** 디자인 + FTP/HTML 대량 수정 = 섹션 GUI 메타와 소스 불일치 → 초기화 오류. **FTP 주력 EZ-on-legacy는 HTML 타입 skin + EZ 코드 이식** (실증: ecudemo400786 — HTML 타입, EZ FTP on `/sde_design/base` + `_ref393674`).

### 공식 근거

| 출처 | 내용 |
|------|------|
| [HTML 수정 FAQ](https://support.cafe24.com/hc/ko/articles/9131045034777) | Easy에서 HTML 수정 시 **Easy 종료** → SD 편집창. 구조 훼손 시 Easy 재진입 **오류 가능** |
| [HTML 수정 후 오류](https://support.cafe24.com/hc/ko/articles/9131291835161) | 백업 복구 권장 |
| [Easy 초기화 오류](https://support.cafe24.com/hc/ko/articles/9131043889945) | 편집 오류 시 새 디자인 추가 권장 |
| [Easy ↔ SD 상호 편집](https://support.cafe24.com/hc/ko/articles/9130954167065) | Easy 타입 ↔ HTML 타입 **교차 편집 불가** |

### 처방

- **FTP·에이전트 작업:** 관리자 **HTML 타입** skin 복사본 + EZ 마크업 선별 이식 — [`01_작업하기/workflows/07-ez-on-legacy-setup.md`](../01_작업하기/workflows/07-ez-on-legacy-setup.md) **Phase 0-D**
- **EZ 마크업 in HTML skin** ≠ **Easy 타입 등록** (코드에 `data-ez-*`만 있는 IDIO/아키테이블 패턴은 HTML 타입에서 가능)
- **하지 말 것:** Easy 대표 + 파트너 FTP 전면 개편 동시 약속 · 「GUI 끄고 HTML만」을 기본 기능처럼 안내

---

## §F36 · EZ 이식·통째 덮기 / ez-settings 무분별 삭제 / strip_ez

> **한 줄:** Easy/EZ 파일을 HTML skin에 **통째 덮어쓰기**하거나 `ez-settings.json`·`@js(/ez/init.js)`를 **역할 확인 없이 삭제**하면 스마트배너·EZST·module·MO 레이아웃이 불일치한다. **선별 이식** + 필요 시에만 `strip_ez.py`.

### 증상

- `layout.html`만 EZ로 교체했는데 module·CSS·MO `#contents` 규칙이 어긋남 (F27·F28 동반)
- `ez-settings.json`·`ez/init.js` 삭제 후 레이아웃 옵션·EZST 런타임 붕괴
- `strip_ez.py` 전량 적용 후 스마트배너·슬라이더 멈춤 (`EZST.register` 순서)

### 근본 원인 (brain §6 F36)

| # | 원인 |
|---|------|
| 1 | EZ base를 작업 skin에 **통째 FTP 덮기** → 스마트배너·EZST·카페24 core module 경로 불일치 |
| 2 | `layout.html`만 교체 — 필수 `css/ec-base-*`·`product/`·`js/` 미동기 |
| 3 | `ez-settings.json`·`@js(/ez/init.js)` **무분별 삭제** — 관리자 레이아웃 옵션·런타임 의존 |
| 4 | **전량 EZ 제거**를 기본값으로 가정 — IDIO/아키테이블은 `data-ez-*`를 header/footer 옵션용으로 **남기는** 패턴도 있음 |
| 5 | `strip_ez.py` 후 `main.js`에서 `EZST.register`가 `new Swiper`보다 **앞**이면 슬라이더 깨짐 |

### 처방

- **권장:** EZ base는 **`layout+필수 module+css` 선별 이식** — [`01_작업하기/workflows/08-ez-three-step-pingpong.md`](../01_작업하기/workflows/08-ez-three-step-pingpong.md) Phase B · [`07-ez-on-legacy-setup.md`](../01_작업하기/workflows/07-ez-on-legacy-setup.md)
- **커스텀 레이어:** `_ref{id}/` 만 수정 · EZ core·`skin1` 읽기 전용
- **전량 제거:** 사용자가 **HTML 전환**을 명시했을 때만 — [`WORK-GUIDE.md` §15](../brain/docs/WORK-GUIDE.md) + `strip_ez.py` (미리보기 → `--write`)
- **삭제 전 확인:** `ez/ez-module.html`·`smart-banner/init/` 등 시스템 파일은 유지 ([WORK-GUIDE §15](../brain/docs/WORK-GUIDE.md) 표)
- **검증:** `data-ez` 잔여 0 + 카페24 코어 `module=` 생존 · Pre-flight C1 PASS ([`06-verify-loop.md`](../01_작업하기/workflows/06-verify-loop.md))

### 예방 체크리스트

- [ ] Phase B에서 **통째 vs 선별** 사용자 확인 (기본: 선별)
- [ ] 업로드 전 diff·파일 목록 제시
- [ ] `strip_ez.py` 미리보기로 `module=`·`@import` 보존 확인
- [ ] EZST 제거 시 Swiper 초기화 순서 점검

### 관련 파일

- [`CAFE24-SMARTDESIGN-AGENT.md`](../brain/docs/CAFE24-SMARTDESIGN-AGENT.md) §6 F36
- [`WORK-GUIDE.md`](../brain/docs/WORK-GUIDE.md) §15 (`strip_ez.py`)
- [`01_작업하기/workflows/08-ez-three-step-pingpong.md`](../01_작업하기/workflows/08-ez-three-step-pingpong.md) Phase B·C
