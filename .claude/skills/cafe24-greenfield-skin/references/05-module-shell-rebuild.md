# 05 — css/module 전수분석 · 모듈 유닛 분해 · 껍데기 재구성

> HTML/CSS를 짜기 **전**에 stock CSS·모듈 내부 DOM을 전부 파악하고, **Layer 1(KEEP) + Layer 2(NEW nk-*)** 로 재구성한다.  
> 검증은 `08-full-audit-pipeline.md` · `04-html-css-parity.md` · `stock-scan-tier.js` (module→submodule→section→page).

---

## 0. 황금 규칙

```
css/module 을 안 읽고 HTML/CSS 짜면 → stock border·파란색·float CTA 잔존 (grep도 놓침)
module 껍데기만 바꾸고 유닛 안 건드리면 → 바인딩 깨짐 · 1개만 출력 · 2배 렌더
```

| Layer | 유지/신규 | 내용 |
|-------|-----------|------|
| **Layer 1 KEEP** | 유지 | `module="..."` · `{$vars}` · `anchorBoxId_{$product_no}` ×≥2 · 설정 주석(줄 분리) · `id`/`name` 카페24 필수 속성 |
| **Layer 2 NEW** | 신규 | inner wrapper `nk-*` · 타입별 `nk-{domain}.css` · `@import` 조각 |

**금지**: Layer 1 안의 `data-ez-*` 임의 제거(EZ 몰) · module 밖 `{$mall_name}` · module 설정 한 줄에 몰아쓰기.

---

## 1. Wave0 — css/module 전수분석 (구현 전 필수)

### 1-A. Pull & 인벤토리

```powershell
# 파트너 FTP 예: /sde_design/base
python cli.py get /sde_design/base/css/module ./clients/{몰}/src/css/module --mall {몰ID}
python cli.py get /sde_design/base/layout/basic/css ./clients/{몰}/src/layout/basic/css --mall {몰ID}
```

산출물: `clients/{몰}/04_design/css-module-inventory.md`

| 컬럼 | 설명 |
|------|------|
| 경로 | `css/module/product/listnormal.css` 등 |
| 연관 module ID | `product_listnormal` → `.xans-product-listnormal` |
| 주요 stock 클래스 | `.ec-base-product` `.prdList` `.description` … |
| 위험 속성 | border 5px · `#008bcc` · float · `font-style:italic` · 고정 width% |
| 대응 nk CSS | `nk-plp.css` §… · 병행 셀렉터 필요 여부 |

### 1-B. 7종 grep (토대정리 연동)

`brain/docs/BASE-CSS-MAP.md` 생성 — `/토대정리` 스킬과 동일:

- 고정폭 · 파란색 · 강제폰트 · 가상요소 border · echosting 이미지 · `!important` · 태그 누수

**두 레이어 모두** 대상: `layout/basic/css/**` + **`css/module/**/*.css`** (AGENT §4 D3).

### 1-C. 페이지 ↔ module CSS 매핑

각 페이지 HTML의 `module=""` 목록 → grep `css/module` 해당 파일 → **영향 셀렉터 표** 작성.

예: `product/list.html` → `product_listnormal` → `css/module/product/listnormal.css` + `css/module/product/listitem.css`

---

## 2. 모듈 유닛 분해 (구현 전 체크리스트)

페이지 타입 하나 착수 시, 해당 페이지 **모든 module** 에 대해 아래 표를 `blank-slate-rebuild-queue.md`에 채운다.

### 2-A. 유닛 유형 (stock-scan-tier SUBUNIT_SELECTORS 기준)

| 유닛 | 예 | 분석 시 확인 |
|------|-----|-------------|
| `form[id]` | 로그인·주문 | action·hidden input·submit name 유지 |
| `fieldset` | 회원가입 동의 | legend·checkbox name |
| `tr[id]` / `li[id$="_wrap"]` | 옵션·주문 행 | JS 바인딩 id |
| `.ec-base-table` | 게시판·myshop | thead/tbody 구조 |
| `.ec-base-box` | 빈 상태·안내 | inner 텍스트만 nk-* 래핑 |
| `.ec-base-button` | CTA 묶음 | float 제거용 nk-actions |
| `anchorBoxId_{$product_no}` | listmain | **블록 ≥2개** 나란히 |
| submodule `@import` | PDP zoom·mail | 별도 HTML 파일 tier |

### 2-B. 모듈 1개 분석 표 (복붙 템플릿)

```markdown
### module: `{모듈명}` · 파일: `{경로}`

| # | 유닛 (DOM) | KEEP 속성/변수 | NEW nk 클래스 | stock CSS 파일 | parity 병행 |
|---|------------|----------------|---------------|----------------|---------------|
| 1 | `.xans-… > ul.prdList > li` | `id="anchorBoxId_{$product_no}"` | `.nk-prd` | listnormal.css | `.nk-prd, .prdList > li` |
| 2 | … | … | … | … | … |
```

### 2-C. 껍데기 재구성 패턴

```html
<!-- Layer 1: module 래퍼 유지 -->
<div module="product_listmain_1" class="nk-sec nk-best">
  <!--
  $count = 12
  $basket_result = /product/add_basket.html
  -->
  <ul class="nk-prd-grid">
    <!-- Layer 2: 반복 블록 ≥2 · 콘텐츠는 @import -->
    <li class="nk-prd" id="anchorBoxId_{$product_no}">
      <!--@import(/_nk/inc/prd.html)-->
    </li>
    <li class="nk-prd" id="anchorBoxId_{$product_no}">
      <!--@import(/_nk/inc/prd.html)-->
    </li>
  </ul>
</div>
```

**module 밖** 히어로·배너: `module=""` 없음 → `{$vars}` 사용 불가 → 텍스트 하드코딩 또는 별도 module scope.

---

## 3. CSS 작성 순서 (페이지 타입당)

1. **HTML 유닛 표** 확정 (§2)
2. **stock CSS** 해당 파일 Read — 덮어쓸 속성 목록
3. **`nk-{type}.css`** — 병행 셀렉터 (`04-html-css-parity.md`)
4. **`nk-cafe24-reset.css`** — 전역 stock 무력화 (이미 Foundation)
5. 페이지 첫 줄 `<!--@css(/_nk/css/nk-{type}.css)-->`
6. FTP 업로드 → `?v=N` → **module tier** 스캔 → submodule → section → page

```powershell
node .claude/skills/cafe24-greenfield-skin/scripts/stock-scan-tier.js --mall-id {몰} --tier module --batch main
node .claude/skills/cafe24-greenfield-skin/scripts/stock-scan-tier.js --mall-id {몰} --tier page --url "/"
```

---

## 4. 완료 기준 (타입 1개)

- [ ] `css-module-inventory.md` 해당 module 행 **분석완료**
- [ ] `blank-slate-rebuild-queue.md` 해당 페이지 **전 module 유닛 표** 작성
- [ ] Layer 1 KEEP 항목 diff 0 (module·변수·anchorBoxId)
- [ ] Layer 2 모든 `nk-*`에 CSS 셀렉터 존재 (parity FAIL 0)
- [ ] 4-tier module·page PASS
- [ ] PC1440 + MO390 스크린샷

---

## 5. 연관 SSOT

| 문서 | 역할 |
|------|------|
| `CAFE24-SMARTDESIGN-AGENT.md` §4 D3 | css/module 2레이어 |
| `04-html-css-parity.md` | nk vs stock 병행 |
| `templates/blank-slate-rebuild-queue.md` | 행 단위 진행표 |
| `06-design-system-adaptation.md` | 외부 DS·코드 → 카페24 변환 |
| `.claude/skills/cafe24/SKILL.md` | 변수·모듈 문법 |
