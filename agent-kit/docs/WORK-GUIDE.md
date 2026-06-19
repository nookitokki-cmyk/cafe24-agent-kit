# 카페24 _nk 템플릿 커스터마이징 작업지시서

> 이 문서는 카페24 스킨을 `_nk/` 폴더 기반으로 커스터마이징할 때 적용하는 표준 가이드다.
> IDIO 템플릿(skin2) 분석을 통해 도출한 방법론을 정리한 것.

---

## 0. 핵심 결론 (반드시 먼저 읽을 것)

### 결론 1 — 카페24 스킨은 두 종류, 작업 방식이 완전히 다르다

| | 일반 스마트디자인 | 스마트디자인 Easy(EZ) |
|---|---|---|
| 대표 | skin2 (IDIO) | skin10 |
| HTML 자유 제작 | **가능** (헤더/푸터/배너 직접 작성) | 제약 많음 (`data-ez-*` 틀에 갇힘) |
| 카테고리 GNB | `module="Layout_category"` | `data-ez-module="menu-main/1"` |
| 우리 작업 적합도 | ✅ 적합 | ❌ 부적합 |

### 결론 2 — IDIO(skin2)의 정체 = "EZ 테마를 걷어내고 _idio 독립 레이어로 재구축" (심층 분석 확정)

> 상세 근거: `web/cafe24/clients/template-02/IDIO-ANALYSIS.md` (CSS·HTML·JS 3영역 심층 분석)

- IDIO는 카페24 **"아키테이블" EZ 테마**를 베이스로 가져왔다 (CSS 계보가 EZ 테마와 동일 — `layout.css:1` `아키테이블_style` 주석, `.ez-align`·CSS변수 등)
- 그 위에서 **EZ 기능을 전부 걷어냈다**: `ez-settings.json` 삭제, EZST 초기화 제거, `@js(/ez/init.js)` 제거, `data-ez-*` 제거, `body` max-width 제거(풀와이드화)
- **`ez/` 폴더는 죽은 껍데기** — skin2 어디서도 `@js(/ez/init.js)`·`@import(ez-module.html)` 안 함 (로드 0건). "ez 폴더 있다=EZ 쓴다"가 **아님**
- 헤더·푸터·메인을 `_idio/inc/`로 외부화 + `idio.js`(jQuery 설정 주입 엔진, EZST와 무관) 독자 시스템
- **즉 "IDIO는 EZ를 걷어냈다"가 정답.** (단순 구형도, EZ 활용도 아닌 = EZ 출신 + 완전 비활성화 + 독립 재구축)

### 결론 3 — skin15(순수 구형)는 IDIO와 다른 계보라 베이스 부적합

- skin15는 구형 XHTML·`@media` 0개(고정폭)·`main.css` 없음·`min-width:1480px` 구형 마커 = **IDIO(아키테이블 EZ)와 완전히 다른 종(種)**
- skin15로 작업하면 IDIO의 디자인·반응형을 재현할 수 없음 → **베이스로 쓰지 말 것**

### 결론 4 — 우리 베이스: IDIO와 같은 "아키테이블 EZ 출신"을 깊이 걷어낸다

- **skin14**가 IDIO(skin2)와 **같은 아키테이블 EZ 출신** (`layout.css:1` 주석 동일). → IDIO 방식 재현에 적합
- EZ 잔재(body max-width·EZST·ez-settings)를 **IDIO 수준으로 마저 걷어내면** skin2와 거의 같아짐
- 우리가 좌측 쏠림·아이콘 빠짐으로 헤맨 이유 = **걷어내기가 IDIO보다 얕았기 때문** (EZ 잔재가 함정 유발)

> ⚠️ 아래 본문 중 "skin10"=공식 EZ 스킨, "skin14/skin12"=EZ 걷어낸 작업 베이스, "skin15"=부적합 구형.
> EZ테마를 걷어내 작업할 때는 §15 "EZ 걷어내기" + 잔재 제거(body max-width 등)를 IDIO 수준까지 한다.

---

## 1. 스킨 유형 파악 — 가장 먼저 해야 할 것

카페24 스킨은 크게 두 종류가 있고, 유형에 따라 카테고리 모듈 문법이 완전히 달라진다.
**작업 시작 전 반드시 어떤 유형인지 먼저 파악한다.**

### 유형 확인 방법

```bash
grep "data-ez-module\|ez-prop\|ez-var" layout/basic/layout.html | head -5
```

결과가 나오면 EZ 스킨, 아무것도 없으면 일반 스마트디자인.

### 두 유형 비교

| 항목 | 일반 스마트디자인 | 스마트디자인 Easy (EZ) |
|---|---|---|
| 대표 스킨 | skin2 (IDIO 템플릿) | skin10 |
| 헤더/카테고리 | `module="Layout_category"` | `data-ez-module="menu-main/1"` |
| 메인 콘텐츠 | `module="product_listmain_1"` | `data-ez-module="product-list/1"` |
| 장바구니 수량 | `module="Layout_orderBasketcount"` | 동일 (이건 두 유형 모두 같음) |
| 로그인 분기 | `module="Layout_statelogoff/on"` | 동일 (이건 두 유형 모두 같음) |
| FTP 직접 수정 | 가능 | 가능 (단, EZ 속성 건드리면 관리자 패널 깨짐) |

### 하이브리드 구조 — EZ 스킨도 일부는 일반 문법을 쓴다

EZ 스킨이라고 해서 모든 것이 EZ 방식은 아니다.
**영역에 따라 혼용된다.**

| 영역 | skin2 (일반) | skin10 (EZ) |
|---|---|---|
| 카테고리 GNB | `module="Layout_category"` | `data-ez-module="menu-main/1"` |
| 메인 상품 진열 | `module="product_listmain_1"` | `data-ez-module="product-list/1"` |
| 장바구니 수량 뱃지 | `module="Layout_orderBasketcount"` | **동일** |
| 로그인/로그아웃 분기 | `module="Layout_statelogoff/on"` | **동일** |
| 검색창 | `module="Layout_SearchHeader"` | **동일** |
| 푸터 쇼핑몰명 | `module="Layout_footer"` | **동일** |

**핵심**: 장바구니, 로그인 분기, 검색창, 푸터 정보처럼 **데이터 치환이 필요한 모듈은 EZ 스킨에서도 일반 문법(`module=""`)이 그대로 작동한다.**
카테고리 GNB와 메인 콘텐츠 섹션만 EZ 전용 방식으로 바꿔야 한다.

### EZ 스킨의 파일 구조

```
skin10/
├── layout/basic/
│   ├── layout.html         ← 헤더/푸터 @import 등록
│   └── header.html         ← data-ez-module 포함 (수정 시 주의)
├── ez/
│   └── ez-module.html      ← 메인 EZ 모듈만 모아둔 파일 (없는 경우도 있음)
└── index.html              ← 메인 페이지 (EZ 섹션 직접 포함)
```

skin2처럼 `ez/ez-module.html`이 별도로 있으면 메인 콘텐츠 EZ 모듈이 거기에 분리된 것.
skin10처럼 없으면 `index.html`에 직접 EZ 섹션이 포함된 것.

### EZST 엔진 — EZ 기능의 실체

`data-ez-module` 속성이 작동하려면 **EZST 런타임 엔진**이 페이지에 로드되어 있어야 한다.

| | 공식 EZ 스킨 (skin10) | 일반 스마트디자인 (skin2 IDIO) |
|---|---|---|
| EZST 엔진 출처 | 카페24 서버가 자동 주입 | `ez/init.js` 파일을 스킨 안에 직접 포함 |
| 카테고리 GNB | `data-ez-module="menu-main/1"` | 일반 `module="Layout_category"` |
| 메인 콘텐츠 | `data-ez-module="product-list/1"` 등 | `data-ez-module` (EZST 엔진이 직접 해석) |
| 관리자 패널 편집 | 완전 지원 | 콘텐츠 섹션만 제한적 지원 |

skin10 `layout.html` 50번째 줄에 카페24가 자동 주입하는 EZST 초기화 코드:
```html
<script>try{window.EZST={q:[],register:function(a,b){this.push([a,(b.init||b)(),arguments])}}}</script>
```

IDIO(skin2)는 이 엔진을 `ez/init.js`로 직접 스킨에 복사해 탑재한 것.
**카페24 EZ API를 쓰는 게 아니라 엔진 파일 자체를 심은 것이다.**

### data-ez-module 번호 규칙

같은 페이지에 동일한 모듈을 2개 이상 쓸 때는 번호를 다르게 해야 한다.

```html
<!-- PC GNB -->
<div data-ez-module="menu-main/1" data-ez-mode="manual">...</div>

<!-- 모바일 드로어 — 번호 /2로 분리 -->
<div data-ez-module="menu-main/2" data-ez-mode="manual">...</div>
```

같은 번호를 쓰면 두 번째 모듈이 첫 번째를 덮어써서 한쪽만 렌더링된다.

### 👉 EZ테마로 생성한 스킨이라면

EZ테마(`data-ez-*` 속성이 있는 스킨)를 IDIO 방식으로 자유롭게 작업하려면,
먼저 **EZ 속성을 걷어내** 일반 스마트디자인으로 되돌린다. → **15장 참고**
(IDIO가 base(EZ 정품테마)를 가져와서 했던 방식과 동일)

---

## 2. 작업 전 반드시 확인할 것

### 이 스킨의 고유 ID 확인

> 📌 **표기 규칙**: 이 문서의 CSS 예시는 `#nk-skinN`으로 표기한다.
> `N`은 이번 작업 스킨의 실제 번호다 (skin12면 `#nk-skin12`, skin15면 `#nk-skin15`).
> 작업 시작 시 아래 절차로 실제 body ID를 확인하고, 문서의 `#nk-skinN`을 그 값으로 바꿔 쓴다.

모든 CSS 셀렉터의 시작점이 되는 `<body>` ID를 먼저 확인한다.

```bash
# layout.html에서 body 태그 확인
grep "<body" layout/basic/layout.html
```

- 예) 결과가 `<body id="nk-skin12" ...>` 이면 → 모든 CSS는 `#nk-skinN .셀렉터` 형태로 작성
- body에 `id`가 없으면 → `layout.html`의 `<body>`에 `id="nk-skin{번호}"`를 직접 추가한다
  (페이지마다 body id가 다를 수 있으므로, 없으면 부여해야 전 페이지 통일 가능)

### 현재 로드 순서 확인

```bash
grep "@css\|@js\|@import" layout/basic/layout.html
```

커스텀 CSS가 카페24 원본보다 **나중에** 로드되는지 확인.
나중에 로드되어야 오버라이드가 가능하다.

---

## 3. 작업 방식 2트랙 전략

영역에 따라 두 가지 방식으로 나뉜다.

| 영역 | 방식 | 이유 |
|---|---|---|
| 헤더 / 푸터 / GNB 메뉴 / 배너 | **HTML 직접 제작 → `@import`** | 레이아웃 자유도 필요, 카페24 데이터만 꽂으면 됨 |
| 상품목록 / 게시판 / 마이페이지 / 주문 | **CSS 오버라이드** | 카페24가 HTML 자동 생성 → 건드릴 수 없음 |

---

## 4. 폴더 구조 및 파일 배치

### 전체 구조

```
skin폴더/
├── layout/basic/               ← 원본 (수정 금지)
│   ├── layout.html             ← CSS/JS/HTML 등록 위치
│   ├── header.html             ← 카페24 기본 헤더 (교체 대상)
│   ├── footer.html             ← 카페24 기본 푸터 (교체 대상)
│   └── css/                    ← 원본 CSS (수정 금지)
│       ├── common.css
│       ├── layout.css
│       └── ec-base-*.css
│
└── _nk/                        ← 모든 커스텀 작업은 여기에만
    ├── css/
    │   ├── custom.css          ← xans- 오버라이드 전용 (전역)
    │   ├── header.css          ← 헤더 전용
    │   ├── footer.css          ← 푸터 전용
    │   └── [컴포넌트명].css    ← 컴포넌트별 (선택)
    ├── js/
    │   └── nk.js               ← 커스텀 JS
    ├── img/                    ← 커스텀 이미지
    └── inc/                    ← 직접 제작 HTML 파일
        ├── header.html
        ├── footer.html
        ├── menu.html
        └── banner/
            └── main-banner.html
```

### 파일 종류별 배치 원칙

| 파일 종류 | 위치 | 등록 방법 |
|---|---|---|
| 전역 CSS 오버라이드 | `_nk/css/custom.css` | `layout.html`에 `@css` 등록 |
| 컴포넌트 CSS | `_nk/css/[이름].css` | 해당 HTML 파일 **맨 첫 줄**에 `@css` 선언 |
| 직접 제작 HTML | `_nk/inc/[이름].html` | `layout.html` 또는 상위 HTML에서 `@import` |
| 커스텀 JS | `_nk/js/nk.js` | `layout.html`에 `@js` 등록 |
| SVG 아이콘 | `/svg/[이름].html` | 사용하는 HTML에서 `@import` |
| 커스텀 이미지 | `/_nk/img/` | 직접 경로 참조 |

---

## 5. CSS 파일 구성 — 몇 개를 어떻게 만드나

### 핵심 원칙: HTML 파일 1개 = CSS 파일 1개

```
_nk/inc/header.html       →  _nk/css/header.css
_nk/inc/footer.html       →  _nk/css/footer.css
_nk/inc/banner/main.html  →  _nk/css/main-banner.css
```

새 HTML 파일을 만들 때 CSS 파일도 반드시 함께 만들고,
해당 HTML 파일 **맨 첫 줄**에 `@css`를 선언한다.

```html
<!-- _nk/inc/header.html — 첫 줄 필수 -->
<!--@css(/_nk/css/header.css)-->

<header id="header">
  ...
</header>
```

이렇게 하면 header.html이 `@import`될 때 header.css도 자동으로 함께 로드된다.

### 작업 시작 시 만들어야 할 파일 수

```
필수 (처음부터 생성):
  ① custom.css    — layout.html에 이미 등록됨 (전역 오버라이드)
  ② header.css    — header.html 만들 때 함께 생성
  ③ footer.css    — footer.html 만들 때 함께 생성

선택 (컴포넌트 추가할 때마다):
  ④ main-banner.css
  ⑤ menu.css
  ⑥ gototop.css
  ... (HTML 파일 추가할 때마다 +1개)
```

### CSS 로드 방식 2가지

**방법 A. 전역 로드** — `layout.html`에 직접 등록
- `custom.css`처럼 모든 페이지에 항상 필요한 파일

**방법 B. 컴포넌트 로드** — 해당 HTML 파일 맨 위에 선언
- `header.css`, `footer.css`처럼 특정 컴포넌트에만 필요한 파일
- 그 컴포넌트가 없는 페이지에서는 로드되지 않음

---

## 6. layout.html 파일 등록 구조

### 실제 로드 순서 (CSS → JS → HTML 순)

```
[CSS — <head> 안]
① /layout/basic/css/common.css        카페24 기본
② /layout/basic/css/layout.css        카페24 기본
③ /layout/basic/css/ec-base-*.css     카페24 기본 (9개)
④ /_nk/css/custom.css                 ← 우리 파일 (나중에 로드 → 오버라이드 가능)

[JS — <head> 안]
⑤ /layout/basic/js/swiper-bundle.min.js
⑥ /layout/basic/js/basic.js
⑦ /layout/basic/js/layout.js
⑧ /_nk/js/nk.js                       ← 우리 파일 (카페24 JS 다음에)

[HTML — <body> 안]
⑨ <!--@import(/_nk/inc/header.html)-->   헤더 (기본 header.html 대체)
⑩ <!--@contents-->                       페이지 본문
⑪ <!--@import(/_nk/inc/footer.html)-->   푸터 (기본 footer.html 대체)
```

### 새 파일 추가 시 등록 위치

```html
<!-- CSS 추가: custom.css 바로 아래 -->
<!--@css(/_nk/css/custom.css)-->
<!--@css(/_nk/css/추가파일.css)-->  ← 여기

<!-- JS 추가: 카페24 JS 다음 -->
<!--@js(/layout/basic/js/layout.js)-->
<!--@js(/_nk/js/nk.js)-->          ← 여기

<!-- HTML 교체: 기존 @import 경로를 _nk/inc/ 로 변경 -->
<!--@import(/_nk/inc/header.html)-->
<!--@contents-->
<!--@import(/_nk/inc/footer.html)-->
```

> ⚠️ **경로 오타 주의**: `<!--@경로-->` 형식은 IDE가 파일 참조로 인식 못함.
> 오타가 나도 에러 없이 조용히 로드 실패함. 반드시 육안으로 직접 확인.

---

## 7. HTML 직접 제작 시 구조 규칙

### HTML 파일 구조 순서

모든 `_nk/inc/` HTML 파일은 아래 순서로 작성한다.

```html
<!-- 1. 작업 안내 주석 (수정 가이드) -->
<!--
  ■ 로고는 /_nk/inc/header-logo.html 에서 변경
  ■ SNS 링크는 nk.js 또는 setup.js 에서 변경
-->

<!-- 2. CSS 로드 — 반드시 첫 번째 -->
<!--@css(/_nk/css/header.css)-->

<!-- 3. JS 로드 (필요한 경우만) -->
<!--@js(/_nk/js/nk-header.js)-->

<!-- 4. HTML 본문 -->
<header id="header">
  ...
</header>
```

### 반복 렌더링이 필요한 module — li를 반드시 2개 작성

카페24 엔진은 module 안의 `<li>` 패턴을 반복 렌더링한다.
**`<li>`가 1개만 있으면 1개만 출력된다.** 반드시 2개 이상 나란히 작성한다.

```html
<!-- ❌ 1개만 있으면 1개만 출력됨 -->
<ul module="Layout_category">
  <li class="d1"><a href="/product/list.html{$param}">{$name}</a></li>
</ul>

<!-- ✅ 2개 이상 나란히 작성 — 카페24가 반복 패턴 인식 -->
<ul module="Layout_category">
  <li class="d1"><a href="/product/list.html{$param}">{$name}</a></li>
  <li class="d1"><a href="/product/list.html{$param}">{$name}</a></li>
</ul>
```

### module은 가장 바깥 감싸는 태그에만 붙인다

```html
<!-- ❌ 잘못 — 안쪽 태그에 module -->
<ul>
  <li module="Layout_category">
    <a href="/product/list.html{$param}">{$name}</a>
  </li>
</ul>

<!-- ✅ 올바름 — 감싸는 태그에 module -->
<ul module="Layout_category">
  <li class="d1"><a href="/product/list.html{$param}">{$name}</a></li>
  <li class="d1"><a href="/product/list.html{$param}">{$name}</a></li>
</ul>
```

### 수정이 잦은 영역은 별도 파일로 분리

로고, SNS 링크, 배너 이미지처럼 클라이언트가 자주 바꾸는 부분은
별도 파일로 쪼개서 `@import`로 불러온다.
파일 하나만 열면 수정이 끝나도록 설계한다.

```html
<!-- header.html 안 -->
<!--@import(/_nk/inc/header-logo.html)-->   ← 로고만 따로
<!--@import(/_nk/inc/menu.html)-->          ← 메뉴만 따로

<!-- footer.html 안 -->
<!--@import(/_nk/inc/footer-logo.html)-->   ← 푸터 로고만 따로
```

### 카페24 모듈 영역과 커스텀 영역을 HTML 주석으로 구분

```html
<!--상품분류-->
<ul module="Layout_category">
  <li class="d1"><a href="/product/list.html{$param}">{$name}</a></li>
  <li class="d1"><a href="/product/list.html{$param}">{$name}</a></li>
</ul>
<!--//상품분류-->

<!--게시판-->
<ul module="Layout_BoardInfo">
  <li class="d1"><a href="{$link_board_list}">{$board_name}</a></li>
  <li class="d1"><a href="{$link_board_list}">{$board_name}</a></li>
</ul>
<!--//게시판-->
```

### 멀티샵 언어 선택 — li 2개 패턴 고정

```html
<div class="bt_mshop" module="Layout_multishopList">
  <button type="button" class="toggle">
    <span>{$current_language}</span>
  </button>
  <ul module="Layout_multishopListitem">
    <li class="{$selected_class}">
      <a href="//{$shop_domain}/">
        <span>{$locale_language}</span>
        <span>{$currency_code}</span>
      </a>
    </li>
    <li class="{$selected_class}">
      <a href="//{$shop_domain}/">
        <span>{$locale_language}</span>
        <span>{$currency_code}</span>
      </a>
    </li>
  </ul>
</div>
```

---

## 8. 카페24 문법 — HTML 직접 제작 시 준수 규칙

### 규칙 1. 변수는 반드시 `module=""` 안에서만 사용

`{$변수명}`은 `module=""` 속성이 있는 요소 안에서만 치환된다.
밖에서 쓰면 `{$변수명}` 텍스트가 그대로 화면에 노출된다.

```html
<!-- ❌ 안 됨 — module 밖 -->
<span>{$mall_name}</span>

<!-- ✅ 됨 — module 안 -->
<div module="Layout_footer">
  Copyright © {$mall_name}
</div>
```

단, 쇼핑몰명처럼 변하지 않는 값은 하드코딩이 더 안전하다.

```html
<!-- 하드코딩 권장 (module 오염 방지) -->
<span class="nk-brand">SHOP NAME</span>
```

### 규칙 2. 로그인 상태 분기 — module로 블록 자체를 on/off

```html
<!-- 로그아웃 상태일 때만 노출 -->
<li module="Layout_statelogoff">
  <a href="/member/login.html">로그인</a>
  <a href="/member/agreement.html">회원가입</a>
</li>

<!-- 로그인 상태일 때만 노출 -->
<li module="Layout_statelogon">
  <a href="/myshop/index.html">마이페이지</a>
  <a href="{$action_logout}">로그아웃</a>
</li>
```

> ⚠️ `statelogoff` / `statelogon` 오타 주의.
> 오타 시 두 블록이 동시에 보이거나 동시에 안 보임.

### 규칙 3. 장바구니 수량

```html
<a href="/order/basket.html" module="Layout_orderBasketcount">
  <span class="nk-icon-cart">장바구니</span>
  <span class="count {$basket_count_display|display}">
    <span class="{$basket_count_class}">{$basket_count}</span>
  </span>
</a>
```

`|display` 모디파이어: 수량이 0이면 `display:none` 자동 처리.

### 규칙 4. 검색창

```html
<div module="Layout_SearchHeader" id="{$search_box_id}">
  <!--
    $search_page = /product/search.html
    $product_page = /product/detail.html
  -->
  {$form.keyword}
  <button type="button" onclick="{$action_search_submit}">검색</button>
</div>
```

### 규칙 5. GNB 카테고리 메뉴 — ⚠️ EZ 스킨 전용 주의

> **skin10은 스마트디자인 Easy(EZ) 스킨이다.**
> EZ 스킨에서 `module="Layout_category"` 방식은 카테고리가 렌더링되지 않는다.
> 반드시 `data-ez-module="menu-main/1"` 방식을 사용해야 한다.

```html
<!-- ❌ 작동 안 됨 — 일반 스마트디자인 방식 (EZ에서 카테고리 미출력) -->
<nav module="Layout_category">
  <!--
    $depth = 2
  -->
</nav>

<!-- ✅ EZ 스킨 전용 방식 — 원본 header.html 구조 그대로 유지 -->
<div data-ez-module="menu-main/1" data-ez-mode="manual">
  <div class="xans-element- xans-layout xans-layout-category top_category">
    <ul>
      <li><a href="/category/카테고리명/번호/">카테고리명</a></li>
      <li><a href="/category/카테고리명/번호/">카테고리명</a></li>
    </ul>
  </div>
</div>
```

`data-ez-mode="manual"` 안의 카테고리 HTML은 카페24 관리자에서 카테고리를 추가/수정하면 자동으로 갱신된다. 직접 수정하지 않아도 됨.

HTML을 직접 제작할 때는 원본 `layout/basic/header.html`의 `data-ez-module="menu-main/1"` 블록을 통째로 복사해서 구조를 유지한 채로 감싸는 클래스명만 교체한다.

**일반 스마트디자인 스킨(EZ 아닌 경우)** 에서는 기존 방식 사용 가능:

```html
<nav module="Layout_category">
  <!--
    $depth = 2
  -->
</nav>
```

### 규칙 6. module 설정 변수는 반드시 줄 분리

```html
<!-- ❌ 한 줄 몰아쓰기 — 설정 전체 무시됨 -->
<!-- $search_page = /product/search.html $product_page = /product/detail.html -->

<!-- ✅ 반드시 줄 분리 -->
<!--
  $search_page = /product/search.html
  $product_page = /product/detail.html
-->
```

### 규칙 7. 파일 분리는 `@import`로

```html
<!-- 메뉴, 로고, 아이콘 등 수정이 잦은 부분은 별도 파일로 분리 -->
<!--@import(/_nk/inc/menu.html)-->
<!--@import(/_nk/inc/header-logo.html)-->
<!--@import(/svg/icon-search.html)-->
<!--@import(/svg/icon-cart.html)-->
```

### 헤더에서 사용 가능한 module 전체 목록

| 용도 | module 값 |
|---|---|
| 로고 | `Layout_LogoTop` |
| GNB 카테고리 | `Layout_category` |
| 로그아웃 상태 영역 | `Layout_statelogoff` |
| 로그인 상태 영역 | `Layout_statelogon` |
| 검색창 | `Layout_SearchHeader` |
| 장바구니 수량 | `Layout_orderBasketcount` |
| 적립금/장바구니 요약 | `Layout_shoppingInfo` |
| 푸터 (mall_name 등) | `Layout_footer` |
| 출석체크 | `Layout_attendBanner` |

---

## 9. CSS 오버라이드 규칙

### body ID 래퍼 — 모든 셀렉터의 시작점

`layout.html`의 `<body id="nk-skinN">` ID를 앞에 붙여 명시도를 압도적으로 높인다.

```css
/* ✅ 올바른 방식 */
#nk-skinN .xans-board-title > .titleArea { padding: 60px 0; }

/* ❌ 잘못된 방식 — ID 없이 단독 타겟팅 */
.xans-board-title > .titleArea { padding: 60px 0; }
```

**이유 — CSS 명시도 점수:**

| 셀렉터 | 명시도 |
|---|---|
| 카페24 코어 `.xans-어쩌고.저쩌고 fieldset input` | ~22점 (클래스+태그 중첩) |
| ID 없이 단독: `.xans-board-title .titleArea` | ~20점 → 질 수 있음 |
| **ID 래퍼: `#nk-skinN .xans-board-title`** | **110점 → 무조건 이김** |

ID 하나가 클래스 10개보다 강하다. `!important` 없이도 카페24 코어를 제압한다.

### `!important` 금지

ID 래퍼가 이미 충분한 명시도를 확보하므로 불필요.
불가피할 경우 반드시 주석으로 사유 명시.

```css
/* ⚠️ 불가피한 경우에만 — 사유 명시 필수 */
#nk-skinN .xans-product-listitem .name {
  font-size: 14px !important; /* ec-base-product.css 인라인 스타일 충돌 */
}
```

### xans- 클래스 동작 원리

카페24는 `module=""` 속성을 가진 요소에 `xans-` 클래스를 자동 부여한다.

```
module="product_listnormal"   →   .xans-product-listnormal
module="Layout_category"      →   .xans-layout-category
module="Layout_statelogon"    →   .xans-layout-statelogon
```

이 클래스를 CSS 셀렉터로 잡아서 스타일을 덮어씌운다.

### 자주 쓰는 xans- 셀렉터 목록

| 영역 | xans- 클래스 |
|---|---|
| 헤더 장바구니 수량 | `.xans-layout-statebasket` |
| 헤더 GNB | `.xans-layout-category` |
| 상품 목록 | `.xans-product-listnormal` |
| 상품 목록 아이템 | `.xans-product-listitem` |
| 상품 더보기 버튼 | `.xans-product-listmore` |
| 상품 상세 | `.xans-product-detail` |
| 게시판 타이틀 | `.xans-board-title` |
| 게시판 카테고리 | `.xans-board-category` |
| 로그인 SNS 버튼 | `.xans-member-login` |
| 마이페이지 주문 탭 | `.xans-myshop-orderhistorytab` |

### 풀블리드 vs 여백 — `.inner` 유무로 제어

`section` 자체는 항상 풀폭. 좌우 여백이 필요한 콘텐츠만 `.inner`로 감싼다.

```
section                  →  풀폭 (배경·이미지가 화면 끝까지, padding 0)
  └── .inner             →  여백 있음 (max-width 1440px + padding 50px)
```

```html
<!-- 풀블리드 배너 — .inner 없음 -->
<section class="nk-main-banner">
  <img src="banner.jpg" style="width:100%">
</section>

<!-- 여백 있는 콘텐츠 — .inner로 감쌈 -->
<section class="nk-product-section">
  <div class="inner">
    상품 목록...
  </div>
</section>
```

### ⚠️ `.inner`는 반드시 `#[body-id] .inner`로 통합 선언 (페이지별 분산 금지)

IDIO 원본은 `.inner`를 페이지별로 쪼개서 선언한다.
이 방식은 **서브 페이지에서 max-width가 안 먹히는 함정**이 있다.

```css
/* ❌ IDIO 원본 — 페이지별 분산 (서브 페이지 누락) */
#main .inner { max-width: 1440px; ... }      /* body#main 일 때만 = 메인 페이지만 */
#footer .inner { max-width: 1440px; ... }    /* 푸터만 */
#layout #container.inner { ... }             /* container에 inner 클래스 붙어야 함 */
```

**문제점:**
- `body#main`은 메인 페이지에서만 body에 `id="main"`이 붙음 → 서브 페이지(상품목록·게시판)는 누락
- 그 결과 서브 페이지 `<section>` 안의 `<div class="inner">`에는 max-width가 안 먹혀 좌우로 퍼짐

```css
/* ✅ 통합 선언 — 전 페이지 동일 적용 */
section {
  width: 100%;
  padding: 0;   /* 전역 리셋에 의존하지 말고 명시 */
}

#nk-skinN .inner {
  max-width: 1440px;
  margin-left: auto;
  margin-right: auto;
  padding-left: 50px;
  padding-right: 50px;
  box-sizing: border-box;
}

/* 풀블리드가 필요한 섹션은 inner 없이 width 100% */
#nk-skinN #contents > section { max-width: 100% !important; }
```

### ⚠️ 헤더/푸터와 본문 max-width 불일치 함정 (실전 핵심)

헤더·푸터는 `.inner`로 1440px인데, **카페24 본문 섹션은 다른 기준폭**이라 좌우가 어긋난다.

| 스킨 사례 | 본문 기본 max-width | 헤더와 차이 |
|---|---|---|
| (구) 다른 스킨 | 1230px | 좌우 105px씩 |
| skin14 (실측) | **1480px** + `width:92%` | 좌우 40px씩 |

**중요 1 — 카페24 본문은 `<section>` 태그가 아니라 `<div class="section">`이다.**
셀렉터는 태그(`section`)가 아닌 클래스(`.section`)로 잡아야 한다.

```css
/* ❌ 태그로 잡으면 div.section을 놓침 */
#nk-skinN #contents > section { ... }

/* ✅ 클래스로 잡아야 div.section / section.section 둘 다 커버 */
#nk-skinN #contents > .section { ... }
```

**중요 2 — 카페24 원본이 `!important` + `width:92%`로 박아둔다.**
`/layout/basic/css/main.css`, `add_layout.css`가
`#contents > .section { max-width:1480px }`, `.main_xxx { max-width:1480px !important; width:92% }`
처럼 선언해서, 단순 max-width로는 안 먹힌다. **`!important`로 맞받아야 한다.**

```css
/* 헤더·푸터·본문 전부 동일 규칙으로 통일 */
#nk-skinN .inner,
#header .header-inner,
#nk-skinN #contents > .section {
  max-width: 1440px;
  margin-left: auto; margin-right: auto;
  padding-left: 50px; padding-right: 50px;
  box-sizing: border-box;
}

/* 원본이 1480 !important / width:92% 로 박은 메인 섹션 강제 통일 */
#nk-skinN #contents > .section,
#nk-skinN .main_product_list,
#nk-skinN .main_image_text_gallery,
#nk-skinN .main_product_slide,
#nk-skinN .main_text,
#nk-skinN .main_product_category,
#nk-skinN .main_map {
  max-width: 1440px !important;  /* 원본 1480 !important 오버라이드 */
  width: 100% !important;        /* 원본 width:92% 제거 → padding 정합 */
  margin-left: auto !important;  /* ⚠️ margin도 !important 필수 (아래 함정 참고) */
  margin-right: auto !important;
}

/* 풀블리드 예외: 화면 끝까지 (배너 등). 안의 .inner가 여백 담당 */
#nk-skinN #contents > .section.nk-full {
  max-width: 100% !important;
  padding-left: 0; padding-right: 0;
}
```

> 메인 섹션 클래스(`.main_product_list` 등)는 스킨마다 다르다.
> `grep "max-width.*!important\|width:92%" layout/basic/css/main.css`로 실제 클래스명을 먼저 확인할 것.

### ⚠️⚠️⚠️ 폭은 1440인데 본문이 좌측으로 쏠리는 함정 (EZ 걷어낸 스킨 1순위 범인)

**증상**: `max-width: 1440px`로 폭은 제한됐는데, 가운데가 아니라 **좌측으로 치우친다.**

#### 🔴 1순위 진짜 범인 — `body`에 박힌 `max-width` (실측 확정)

**EZ테마는 `body`에 `max-width: 1480px`(또는 1920px)를 박아둔다.** EZ를 걷어내도 이 규칙은
테마 CSS(`sub_theme.css`, `add_theme*.css`)에 남아서, **`body` 전체가 화면 좌측에 붙는다**
(`body { max-width:1480px; margin-left:0 }`). 그러면 그 안의 컨테이너·본문 정렬이 아무리
정상이어도 **body째로 좌측으로 쏠려 보인다.**

> 실측 사례(skin14): 화면 1646px인데 `body`가 `max-width:1480` + `margin-left:0` →
> body가 좌측 0에 붙음 → 컨테이너(1440)는 body 안에서 가운데(20px씩)인데도 전체가 왼쪽 쏠림.

```css
/* ✅ 해결 — body 자체 max-width 해제 + 가운데 정렬 */
body#nk-skinN { max-width: none !important; margin-left: auto !important; margin-right: auto !important; }
```

> **진단 1순위**: F12 Console에 `getComputedStyle(document.body).maxWidth` 입력.
> `1480px`/`1920px` 등이 나오면 이 함정. `none`이어야 정상.
> 또는 `document.body.getBoundingClientRect()`의 left/right가 비대칭이면 body가 쏠린 것.

**그동안 margin·명시도·캐시를 의심했지만 실제 범인은 거의 항상 `body max-width`였다.**
좌측 쏠림이면 **body부터 확인**한다.

#### 2순위 — `margin: auto`가 `!important` 누락으로 밀림

위 body 문제를 잡고도 본문 섹션만 따로 쏠리면 아래를 본다.
`max-width`·`width`는 `!important`로 줬는데 **`margin: auto`를 `!important` 없이** 주면,
카페24 원본 `main.css`가 본문보다 나중에 로드되거나 동일 명시도라
`margin: auto`가 밀려서 `margin-left: 0`처럼 계산된다 → 폭은 줄었는데 왼쪽 정렬.

```css
/* ❌ width만 important, margin은 일반 → 좌측 쏠림 */
#nk-skinN #contents > .section {
  max-width: 1440px !important;
  width: 100% !important;
  margin-left: auto;          /* ← 원본에 밀려 무시됨 */
  margin-right: auto;
}

/* ✅ margin도 !important → 무조건 가운데 */
#nk-skinN #contents > .section {
  max-width: 1440px !important;
  width: 100% !important;
  margin-left: auto !important;
  margin-right: auto !important;
}
```

> **규칙**: 본문 섹션 폭을 `!important`로 통일할 때는 **`max-width`·`width`·`margin`을 한 세트로 전부 `!important`** 처리한다. 폭만 important로 주고 margin을 빠뜨리면 100% 좌측 쏠린다.
> **점검**: F12 → 쏠린 섹션 클릭 → Computed의 `margin-left` 값 확인. `0`이면 이 함정.

### ⚠️⚠️⚠️ 그래도 안 먹을 때 — 명시도 동점 + 캐시 (실전 추적 기록)

`margin: auto !important`까지 줬는데도 좌측 쏠림이 안 풀리면 아래 2가지를 의심한다.

**① 명시도 동점** — 카페24 원본이 `#container #contents > .section`(ID 2 + class = **210점**)로
선언했는데, 내 셀렉터도 `#nk-skinN #contents > .section`(**210점**)이면 **동점**이다.
동점에서 `!important`끼리 붙으면 로드 순서 싸움이 되어 불안정하다.
→ **셀렉터에 `#container`를 더해 명시도를 확실히 위로** 올린다.

```css
/* ❌ 원본과 동점 (210) — 불안정 */
#nk-skinN #contents > .section { ... !important; }

/* ✅ #container 추가로 명시도 310 — 확실히 우위 */
body#nk-skinN #container #contents > .section { ... !important; }
```

**② 카페24 `optimizer.php` 캐시** — CSS는 정확한데 옛 버전이 서빙되는 경우.
업로드해도 화면이 안 바뀌면 코드를 더 고치기 전에 **반드시 캐시부터 비운다.**
- 브라우저: `Ctrl + Shift + R` (강력 새로고침)
- 그래도 안 되면: 카페24 관리자 → 디자인 → **캐시 초기화**
- `optimizer.php`가 CSS를 병합·압축해 서빙하므로, 수정 즉시 반영이 안 될 수 있음

> **카페24는 CSS가 맞아도 캐시 때문에 "안 먹는 것처럼" 보이는 일이 흔하다.**
> 코드를 의심하기 전에 캐시부터 비우는 게 순서다.

### ✅ 폭 정합 최종 정답 — skin2(IDIO) 방식 그대로 (실측 확정)

개별 `.section`과 명시도 싸움하지 말고, **헤더·푸터·본문 inner를 한 규칙으로 묶어
동일 max-width + 반응형 패딩**으로 통일한다. 이게 skin2가 검증한 방식이다.

```css
/* skin2 실측 규칙 — 헤더(.inner)·푸터(.inner)·본문(#container.inner)을 한 그룹으로 */
#nk-skinN #container.inner,
body#nk-skinN #header .inner,
body#nk-skinN #footer .inner,
#nk-skinN .inner {
  max-width: 1920px !important;   /* 고정값 — 모든 화면 동일 */
  width: 100% !important;
  margin-left: auto !important; margin-right: auto !important;
  padding-left: 50px !important; padding-right: 50px !important;
  box-sizing: border-box;
}
/* max-width 는 고정, 패딩만 반응형으로 줄임 (skin2 기준 50→35→24→15) */
@media (max-width:1480px){ ... padding: 0 35px !important; }
@media (max-width:1024px){ ... padding: 0 24px !important; }
@media (max-width:540px) { ... padding: 0 15px !important; }
```
```html
<!-- #container 에 class="inner" 부여 (layout.html / main.html / detail_layout.html) -->
<div id="container" class="inner"> ... </div>
```

**핵심 3가지:**
1. 헤더·푸터·본문을 **하나의 셀렉터 그룹**으로 묶음 (따로따로 하면 어긋남)
2. **max-width 는 고정**(skin2=1920), **패딩만 반응형**으로 줄임 → 모든 화면서 끝선 일치
3. 카페24 원본 헤더/푸터 `.inner {max-width:1480; width:92%}`와 동점(110)이므로
   `body#nk-skinN` 접두로 명시도 210 + `!important` 로 확실히 이긴다

> **"큰 화면에서 헤더가 본문보다 길다"** 증상의 원인이 바로 이것 —
> 헤더 `.inner`(1480)와 본문(1440)을 따로 잡아 값이 달랐던 것.
> 한 그룹·한 값으로 묶으면 해결.

### 🔑 EZ 걷어낸 스킨 vs IDIO 베이스 — body max-width 차이 (중요)

| | skin2 (IDIO 베이스) | EZ 걷어낸 스킨 (skin14 등) |
|---|---|---|
| `body` max-width | **원래 없음** → 해제 불필요 | `common.css`·`layout.css`에 `1480/1920` 박힘 → **해제 필수** |

EZ테마 기반 스킨은 위 폭 통일과 **별개로** body max-width 해제를 반드시 추가해야 한다.
(IDIO 베이스엔 없던 EZ 특유 단계 — 안 풀면 body째 좌측 쏠림)

```css
body#nk-skinN { max-width: none !important; margin-left: auto !important; margin-right: auto !important; }
```

> **점검 방법**: F12 Console에 `getComputedStyle(document.body).maxWidth` → `none` 이어야 정상.
> 그리고 `#header .inner` / `#container` / `#footer .inner` 의 maxW·left·right 가 모두 같은지 확인.

### ⚠️ 헤더 우측 아이콘이 컨테이너 밖으로 빠져나가는 함정

**증상**: 헤더 컨테이너(`.inner`)는 정상인데, 우측 아이콘(검색·마이·장바구니)만 패딩 밖으로 더 나간다.

**원인**: 아이콘 영역(`.top_mypage` 등)이 `position:absolute; right:0` 인데, **직계 부모가 `static`**이라
absolute의 기준점(offsetParent)이 패딩 가진 상위 `.inner`가 된다. → `right:0`이 inner의 **padding box**(패딩 포함 바깥쪽) 기준이 되어 콘텐츠보다 패딩(50)만큼 더 빠져나간다.

```css
/* ✅ 해결 — 아이콘의 직계 부모를 relative 로 만들어 기준점을 콘텐츠 영역으로 */
body#nk-skinN #header .top_nav_box { position: relative !important; }
```

> **원리**: `position:absolute`의 `right:0`은 **가장 가까운 positioned 조상(offsetParent)의 padding edge** 기준이다.
> 직계 부모가 static이면 더 위의 relative 조상(보통 패딩 가진 `.inner`)이 기준이 되어 빠져나간다.
> **아이콘을 감싼 콘텐츠 래퍼를 `relative`로 만들면** 기준점이 콘텐츠 영역으로 들어와 정렬된다.
> **점검**: F12로 아이콘 영역의 `offsetParent`와 `right` 값 확인. offsetParent가 `.inner`면 이 함정.

### custom.css 섹션 구분 주석 형식

```css
/* ── 0. 폰트 ─────────────────────────────────────────────── */
/* ── 1. 레이아웃 최대폭 제어 ─────────────────────────────── */
/* ── 2. 헤더 ─────────────────────────────────────────────── */
/* ── 3. 메인 ─────────────────────────────────────────────── */
/* ── 4. 상품 목록 / 상품카드 ─────────────────────────────── */
/* ── 5. 상품 상세 ────────────────────────────────────────── */
/* ── 6. 게시판 ───────────────────────────────────────────── */
/* ── 7. 마이페이지 ───────────────────────────────────────── */
/* ── 8. 푸터 ─────────────────────────────────────────────── */
```

### 미디어쿼리 브레이크포인트

| 구간 | 기준 |
|---|---|
| PC | 1025px 이상 |
| 태블릿 | `max-width: 1024px` |
| 모바일 | `max-width: 767px` |

---

## 10. 작업 절차

### 새 스킨 작업 시작할 때 (최초 1회)

```
1. layout.html 열어서 <body id="?"> 확인 → CSS 셀렉터 기준점 파악
2. layout.html의 @css/@js/@import 로드 순서 확인
3. _nk/inc/ 폴더 없으면 생성
4. layout.html에서 기존 @import(/layout/basic/header.html) →
   /_nk/inc/header.html 로 경로 교체
5. layout.html에서 기존 @import(/layout/basic/footer.html) →
   /_nk/inc/footer.html 로 경로 교체
```

### HTML 직접 제작 시

```
1. _nk/inc/파일명.html 생성
2. 파일 맨 첫 줄에 <!--@css(/_nk/css/파일명.css)--> 선언
3. _nk/css/파일명.css 함께 생성
4. 카페24 문법 준수하여 HTML 작성 (8장 참고)
5. SFTP로 두 파일 모두 업로드
6. 브라우저 소스보기(Ctrl+U)로 {$변수} 텍스트 노출 여부 확인
7. 로그인 / 로그아웃 상태 양쪽 모두 테스트
```

### CSS 오버라이드 시

```
1. F12 → 수정할 요소 우클릭 → 검사
2. xans-* 클래스 확인
3. #[body-id] .xans-... 형태로 custom.css에 추가
4. SFTP로 custom.css 업로드
5. Ctrl+Shift+R 강력 새로고침으로 반영 확인
6. 안 되면 카페24 관리자 → 캐시 초기화 후 재확인
```

---

## 11. 절대 하면 안 되는 것

| 금지 항목 | 이유 |
|---|---|
| `module=""` 밖에서 `{$변수}` 사용 | 변수 텍스트가 그대로 화면에 노출됨 |
| `Layout_statelogoff` / `statelogon` 오타 | 로그인 상태 분기 전체 붕괴 |
| `/layout/basic/css/` 파일 직접 수정 | 스킨 업데이트 시 초기화됨 |
| `ec-base-*.css` 수정 | 카페24 기본 UI 전체에 영향 |
| 인라인 `style=""` 속성 삽입 | EZ 에디터가 덮어씌움 |
| `!important` 남발 | 명시도 꼬임, 유지보수 불가 |
| module 설정 변수 한 줄 몰아쓰기 | 설정 전체 무시됨 |
| `<nav module="Layout_category">` 안에 HTML 임의 작성 | 카테고리 렌더링 깨짐 |
| CSS/JS 파일 생성 후 layout.html 미등록 | 파일이 존재해도 로드 안 됨 |
| 파일명만 리네이밍하고 참조처 미수정 | `@import`·`<script src>` 경로 깨져서 로드 안 됨 |
| `.inner` 페이지별 분산 선언 (`#main .inner` 등) | 서브 페이지에서 max-width 누락 |

---

## 12. IDIO → NK 리네이밍 규칙 (skin2/IDIO 복제 시)

일반 스마트디자인 스킨을 복제하면 IDIO 명칭(`_idio`, `idio.js`, `--idio-*`)이 그대로 남는다.
리네이밍할 때 **파일명만 바꾸면 안 되고, 참조처도 반드시 함께 수정**해야 한다.

### 리네이밍 대응표

| IDIO | NK |
|---|---|
| `/_idio/` 폴더 | `/_nk/` |
| `idio.js` | `nk-core.js` (또는 유지) |
| `--idio-theme-color` 등 CSS 변수 | `--nk-theme-color` |
| `IDIO['key']` (setup.js) | `NK['key']` |

### 파일명 변경 시 — 참조처 동시 수정 필수

예: `idio.js`를 `nk-core.js`로 바꾸려면 아래 3곳을 **모두** 함께 수정해야 한다.

```bash
# 1. 어디서 참조하는지 먼저 검색
grep -rn "idio.js" --include="*.html"

# 결과 예시 (skin12 기준):
#   _nk/inc/common.html:25       <script src="/_nk/js/idio.js"></script>
#   board/review/read.html:61    <script src="/_nk/js/idio.js"></script>
#   board/review/modify.html:60  <script src="/_nk/js/idio.js"></script>

# 2. 파일명 변경 + 위 3곳의 src 경로 모두 교체
```

> ⚠️ 참조처를 빠뜨리면 해당 페이지에서 JS가 로드되지 않아 슬라이더·메뉴 동작이 멈춘다.
> **검색 → 파일명 변경 → 참조처 일괄 교체** 순서를 반드시 지킨다.

### skin12 현재 미해결 항목

- `_nk/js/idio.js` 가 IDIO 명칭으로 남아있음 (참조처 3곳: `_nk/inc/common.html`, `board/review/read.html`, `board/review/modify.html`)
- 정리하려면 위 절차대로 파일명 + 참조처 3곳 동시 수정

---

## 13. 디버깅

| 증상 | 원인 및 해결 |
|---|---|
| `{$변수명}` 텍스트가 화면에 그대로 보임 | module 밖에서 변수 사용 → module 안으로 이동 |
| 로그인/로그아웃 분기 안 됨 | `statelogoff` / `statelogon` 오타 확인 |
| CSS 수정이 반영 안 됨 | Ctrl+Shift+R → 그래도 안 되면 카페24 관리자 캐시 초기화 |
| `@import` 파일 로드 안 됨 | layout.html에 등록됐는지 확인, 경로 오타 확인 |
| CSS 오버라이드가 안 먹힘 | body ID 래퍼 없이 단독 타겟팅 중 → `#[id] .xans-...` 형태로 수정 |
| 컴포넌트 CSS가 로드 안 됨 | 해당 HTML 파일 맨 첫 줄 `@css` 선언 누락 확인 |
| 메뉴(GNB)가 아예 안 보임 | EZ 스킨에서 `module="Layout_category"` 사용 중 → `data-ez-module="menu-main/1"` 방식으로 교체 (규칙 5 참고) |
| 서브 페이지만 좌우 여백이 다름 | `.inner`가 `#main .inner`처럼 페이지별 분산 선언됨 → `#[body-id] .inner`로 통합 |
| 헤더/푸터와 본문 좌우 정렬 어긋남 | max-width 불일치 (헤더 1440 vs 본문 1230) → `#contents > section` max-width 통일 |
| JS 동작(슬라이더 등) 멈춤 | 리네이밍 후 `<script src>` 경로 미수정 → grep으로 참조처 확인 |
| 헤더 우측 아이콘이 컨테이너 밖으로 빠져나감 | `.top_mypage`가 `absolute`인데 부모 `.top_nav_box`가 `static` → 부모를 `relative`로 (offsetParent 교정) |
| 헤더 우측 아이콘만 로고/GNB보다 한 줄 아래 | 카페24 layout01이 `.top_mypage`에 `top:70px` 박음(GNB 다단 가정) → `#[id] #header .top_nav_box .top_mypage { top:50%; transform:translateY(-50%) }`로 수직 중앙 정렬 |
| EZST 제거 후 메인 슬라이더 멈춤 | `main.js`의 `EZST.register`가 Swiper보다 앞이면 깨짐 → EZST 초기화 1줄 복원 (§15 EZ 런타임 제거 참고) |

---

## 14. header.css 작성 가이드

> ⚠️ **[구버전 화석 — 폐기. §18-9가 현행 정답]** 이 §14는 **skin7/skin8 계보**의 헤더 아키텍처(`--nk-hd-pc-height`/`--nk-hd-m-height`, `#topMenu`/`.d1Box`/`.btn_drw`/`.hdlogo`/`.hdicons`)를 기준으로 작성된 옛 가이드다. **현행 skin10/skin14 에는 이 토큰·셀렉터가 존재하지 않는다**(실측 0건). 현재 헤더는 `_nk/inc/header.html` 마이그레이션(§18-9)으로 **`.nk-hd__inner`/`.nk-gnb`/`.nk-hd__burger`/`.nk-drawer`** 구조 + custom.css 의 **`--nk-header-h`(80px, toparea 제거)·`--nk-topbar-h`(36px / 모바일 30px)** 토큰을 쓴다. 모바일 띠↔헤더 gap(§18-10 B)·드로어 z-스택(§18-10 C·D)의 핵심이 이 토큰들이므로, **새 헤더 작업은 반드시 §18-9 + §18-10 을 기준으로 하고 이 §14는 참고만** 할 것. (배포용 자립본 `CAFE24-SMARTDESIGN-AGENT.md` §8-4·§9 가 현행 정답을 담는다.) 아래 내용은 skin7/8 계보 이력 보존용으로만 남긴다.

header.css는 헤더 HTML에서 직접 제작한 모든 요소의 스타일을 담당한다.
xans- 클래스는 장바구니 수량 뱃지 딱 1개만 쓰고, 나머지는 전부 자체 클래스로 제어한다.

### 섹션 구성 — 이 순서로 작성한다

```css
/* ── 0. 헤더 높이 변수 ───────────────────────────────────── */
:root {
  --nk-hd-pc-height: 80px;   /* PC 헤더 높이 */
  --nk-hd-m-height: 56px;    /* 모바일 헤더 높이 */
}

/* ── 1. 헤더 전체 (위치·크기·z-index) ───────────────────── */
#header { }
#header .header-inner { }
#header .header-inner.fixed { }   /* 스크롤 시 fixed 전환 */

/* ── 2. GNB — PC 가로 메뉴 ──────────────────────────────── */
#topMenu .d1Box { }      /* 1depth 메뉴 목록 */
#topMenu .d1 { }         /* 1depth 아이템 */
#topMenu .d2Box { }      /* 2depth 드롭다운 */
#topMenu .d2 { }         /* 2depth 아이템 */
#topMenu .d3 { }         /* 3depth 아이템 */

/* ── 3. 모바일 드로어 메뉴 ───────────────────────────────── */
.nav { }                 /* 드로어 패널 */
.nav_cover { }           /* 배경 딤 */
.nav #leftMenu .d1 { }
.nav #leftMenu .d2 { }
.nav #leftMenu .d3 { }

/* ── 4. 햄버거 버튼 ──────────────────────────────────────── */
#header .btn_drw { }
#header .btn_drw .line { }

/* ── 5. 로고 ─────────────────────────────────────────────── */
#header .hdlogo { }

/* ── 6. 아이콘 메뉴 (검색·마이·장바구니) ────────────────── */
#header .hdicons { }
#header .top_mypage { }
#header .top_mypage > li > a { }

/* ── 7. 장바구니 수량 뱃지 — 유일한 xans- 타겟팅 ─────────── */
#header .top_mypage > li > a.xans-layout-orderbasketcount .count { }

/* ── 8. 검색 레이어 ──────────────────────────────────────── */
.schArea { }
.schBox { }

/* ── 9. 반응형 ───────────────────────────────────────────── */
@media all and (max-width: 1024px) { }   /* 모바일: GNB 숨김, 드로어 표시 */
@media all and (min-width: 1025px) { }   /* PC: 드로어 숨김, GNB 표시 */
```

### 핵심 패턴 — 헤더 높이를 CSS 변수로 관리

헤더 높이를 `:root` 변수로 선언하면, 본문 상단 여백(`padding-top`)도 자동으로 연동된다.

```css
:root {
  --nk-hd-pc-height: 80px;
  --nk-hd-m-height: 56px;
}

/* 본문이 헤더 아래에서 시작하도록 */
@media all and (min-width: 1025px) {
  #contents { padding-top: var(--nk-hd-pc-height); }
}
@media all and (max-width: 1024px) {
  #contents { padding-top: var(--nk-hd-m-height); }
}
```

헤더 높이를 바꿀 때 변수 값 하나만 수정하면 된다.

### PC ↔ 모바일 전환 원칙

```css
/* PC: GNB 표시, 드로어 숨김 */
@media all and (min-width: 1025px) {
  #header .hdgnb { display: flex; }
  .nav { display: none; }
  #header .hddrw { display: none; }
}

/* 모바일: GNB 숨김, 드로어 + 햄버거 표시 */
@media all and (max-width: 1024px) {
  #header .hdgnb { display: none; }
  .nav { display: block; }
  #header .hddrw { display: block; }
}
```

---

## 15. EZ테마 → 일반 스마트디자인 변환 ("걷어내기")

> **언제 쓰나**: EZ테마로 생성한 스킨을 IDIO 방식(HTML 직접 제작 + CSS 오버라이드)으로
> 자유롭게 작업하고 싶을 때. EZ 전용 속성을 제거해 일반 스마트디자인으로 되돌린다.
> IDIO가 base(EZ 정품테마)를 가져와 했던 작업과 동일하다.

### 핵심 원칙

**EZ 전용 속성·태그만 제거하고, 카페24 코어는 100% 보존한다.**

| ❌ 제거 (EZ 전용) | ✅ 보존 (카페24 코어 + 일반) |
|---|---|
| `<ez-prop>...</ez-prop>` 블록 통째 | `module="..."` (상품·게시판·레이아웃 모듈) |
| `<ez-var>`, `<ez-item>` (위 블록 안에 포함) | `<!-- $count=4 ... -->` 모듈 설정 주석 |
| `<script type="text/ez-prop">...</script>` | `{$변수}` (치환 변수) |
| `data-ez-module`, `data-ez-role`, `data-ez-layout` | `@import`, `@css`, `@js` 지시어 |
| `data-ez-align`, `data-ez-holder`, `data-ez-item` 등 모든 `data-ez-*` 속성 | 일반 class (`section`, `ec-base-product`, `prdList grid4`) |
| `data-ez="contents-..."`, `data-ez-theme` | HTML 구조 전체 |

> ⚠️ **`ez-` 로 시작하는 class** (예: `ez-align-left`, `ez-column-3`)는 **걷어내기 단계에서 유지**한다.
> 제거하면 레이아웃이 깨질 수 있어, 나중에 `_nk` 커스텀 작업 시 자연스럽게 정리한다.
> (제거 대상은 `data-ez-*` **속성**과 `<ez-prop>` **태그**이지, `ez-` **클래스**가 아님)

### 걷어낼 EZ 속성 전체 목록 (skin14 실측 기준)

| 속성/태그 | skin14 전체 개수 | 비고 |
|---|---|---|
| `data-ez-role` | 205 | 가장 많음 (영역 역할 표시) |
| `<ez-item>` | 132 | ez-prop 블록 내부 |
| `<ez-var>` | 29 | ez-prop 블록 내부 |
| `data-ez-item` | 37 | |
| `data-ez-module` | 32 | 모듈 식별 (안에 `module=` 포함 주의) |
| `<ez-prop>` | 24 | 블록 시작 태그 |
| `data-ez-align` | 22 | 정렬 |
| `data-ez-holder` | 21 | 모듈 홀더 |
| `data-ez-layout` | 17 | 레이아웃 그리드 |
| `data-ez-group` | 8 | 그룹핑 |
| `data-ez-theme` | 2 | body 테마 (`<body data-ez-theme="theme01">`) |
| `data-ez-item-length` | 2 | |
| `data-ez-column` | 2 | |
| `data-ez-mobile-layout` | 2 | |
| `text/ez-prop` (script) | 2 | |
| `data-ez-display` | 1 | |

### 제거하면 안 되는 파일 (카페24 시스템 — 건드리지 말 것)

| 파일 | 이유 |
|---|---|
| `ez/ez-module.html` | EZ 관리자 연동 메타데이터 (IDIO도 남겨둠) |
| `ez/init.js` | EZST 엔진 (남겨도 무해) |
| `smart-banner/init/ez-initialize.html` | EZ 초기화 시스템 파일 |
| `supply/*` | 공급사몰 (보통 미사용) |

### 자동 변환 스크립트 (`strip_ez.py`)

`web/cafe24/clients/template-02/strip_ez.py` 에 변환 스크립트가 있다.

```bash
# 미리보기 (통계만, 파일 수정 안 함)
python3 strip_ez.py src/skinNN/index.html

# 실제 적용 (--write)
python3 strip_ez.py src/skinNN/index.html --write
```

제거 규칙 (정규식):
```python
# 1. <ez-prop> 블록 통째 (멀티라인)
re.sub(r'[ \t]*<ez-prop\b.*?</ez-prop>\s*\n?', '', html, flags=re.DOTALL)
# 2. <script type="text/ez-prop"> 블록
re.sub(r'[ \t]*<script[^>]*type="text/ez-prop".*?</script>\s*\n?', '', html, flags=re.DOTALL)
# 3. data-ez-xxx="값" 속성
re.sub(r'\s+data-ez-[a-zA-Z-]+="[^"]*"', '', html)
# 4. data-ez="값" 속성
re.sub(r'\s+data-ez="[^"]*"', '', html)
# 5. 값 없는 data-ez-xxx 속성
re.sub(r'\s+data-ez-[a-zA-Z-]+(?=[\s>])', '', html)
```

### 걷어내기 작업 절차

```
1. 백업 — 걷어낼 파일을 _ez-backup/ 폴더에 복사 (SFTP 원본도 안전망)
2. 미리보기 — strip_ez.py로 통계 확인 (module=/@import 보존되는지)
3. 적용 — --write로 실제 변환
4. 검증 — data-ez 잔여 0개 확인 + 카페24 코어 module 살아있는지 확인
5. 대상 파일 (보통): index.html, layout/basic/{header,footer,layout,main,sidebar}.html,
   product/{detail,list}.html
```

> 💡 `module=` 카운트가 줄어드는 건 정상이다. `data-ez-module="..."` 안에 `module=`
> 문자열이 포함돼 있어, EZ 속성이 빠지면서 함께 빠지는 것일 뿐. 진짜 카페24 코어
> `module="product_listnormal"` 같은 건 그대로 보존된다 (검증 4단계에서 확인).

### EZ 런타임(EZST 엔진) 제거 — data-ez 걷어낸 다음 단계 (skin14 실증)

`data-ez` 속성을 다 걷어내도 `layout.html`/`main.html`의 `<head>`에 EZ **런타임**이 남는다.
IDIO(skin2)는 이것들이 전부 없다. 제거 대상 4종 (보통 `@js(/js/common.js)` 다음에 몰려 있음):

```html
<script>try{window.EZST={q:[],register:...}}catch(e){}</script>  <!-- EZST 초기화 -->
<!--ez-favicon[-->                                                <!-- EZ 파비콘 마커 -->
<!--ez-favicon]-->
<!--@js(/ez/init.js)-->                                           <!-- EZST 큐 처리 엔진 -->
```

> ⚠️ **제거 전 의존성 확인 필수**: `layout/basic/js/main.js`가 `EZST.register(...)`를 호출하면
> (카페24 기본 메인 JS), EZST 초기화를 지웠을 때 `EZST is not defined` 에러로 **메인 슬라이더가
> 깨질 수 있다.** 단, `EZST.register` 호출이 슬라이더(`new Swiper`)보다 **뒤**에 있으면 슬라이더는
> 이미 실행된 뒤라 살아남는다 (skin14 실증: main.js 5번 줄 Swiper, 79번 줄 EZST.register).

**안전 절차:**
```
1. main.js에서 EZST 사용 위치 확인: grep -n "EZST" layout/basic/js/main.js
   → EZST.register가 Swiper 초기화보다 뒤면 제거해도 슬라이더 안전
2. layout.html / main.html 백업
3. 위 4줄(<head>) 제거 → 업로드
4. 브라우저 검증 (필수):
   - F12 Console: EZST/ReferenceError 에러 없는지
   - window.EZST === undefined 확인
   - 슬라이더 작동: document.querySelectorAll('.swiper-slide-active').length > 0
   - body scrollHeight 정상(수천px)
5. 깨지면 EZST 초기화 1줄만 복원 (@js(/ez/init.js)·ez-favicon은 죽은 코드라 안전)
```

> **ez/ 폴더 자체(init.js, ez-module.html, ez-settings.json)는 삭제 불필요.** IDIO도 ez/ 폴더는
> 죽은 채로 남겨뒀다. `@js`/`@import`로 로드만 안 하면 프론트엔 무관. ez-settings.json은 카페24
> 관리자 EZ 편집 패널용이라 프론트 렌더링에 영향 0 → 남겨도 무해(삭제 리스크가 더 큼).

---

## 16. 프로젝트별 설정값 (스킨 시작 시 채울 것)

> 아래는 skin10 기준 값. 새 스킨 작업 시 실제 값으로 교체한다.

| 항목 | skin10 값 | 새 스킨 값 |
|---|---|---|
| body ID | `nk-skin10` | |
| 콘텐츠 최대폭 | `1440px` | |
| PC 좌우 패딩 | `50px` | |
| 태블릿 패딩 | `24px` | |
| 모바일 패딩 | `16px` | |
| PC 헤더 높이 | `80px` | |
| 모바일 헤더 높이 | `56px` | |
| custom.css 등록 위치 | `layout.html` 30번째 줄 | |
| 헤더 @import 등록 위치 | `layout.html` 71번째 줄 | |
| 푸터 @import 등록 위치 | `layout.html` 81번째 줄 | |

---

## 17. 메인 페이지 재구성 (skin14 실증 — 자기완결형 섹션 + 럭셔리 디자인시스템)

> skin14(아키테이블 EZ 걷어낸 베이스)의 메인을 skin2(IDIO) 순서를 차용해 럭셔리 재판매 템플릿으로
> 재구성하면서 실측한 함정·해법 모음. **이 절만 읽어도 다른 스킨 메인 재구성에 그대로 적용 가능.**

### 17-1. index.html = `@layout` + `@import` 나열 (마크업 0)

메인 `index.html` 첫 줄 `<!--@layout(/layout/basic/layout.html)-->` 뒤에 섹션 조각 `@import`만 나열.
각 조각은 `_nk/inc/<섹션>.html`, 첫 줄에서 자기 CSS `<!--@css(/_nk/css/<섹션>.css)-->` 로드 = 자기완결형.

```
<!--@layout(/layout/basic/layout.html)-->
<!--@import(/_nk/inc/mainBnr.html)-->   ← 히어로(풀블리드)
<!--@import(/_nk/inc/bnrArea1.html)-->  ← 카피배너
<!--@import(/_nk/inc/prdTab.html)-->    ← 키워드 탭 상품
...12개
```

**DRY 절충**: 섹션마다 반복되는 공유 프리미티브(섹션 헤드 `.nk-sec`/`.nk-eyebrow`/`.nk-sec__title`,
링크·솔리드 버튼 `.nk-btn-link`/`.nk-btn-solid`, 스와이퍼 화살표 `.nk-arrow`, 상품 그리드 `.nk-prd-grid`,
상품카드 `.nk-prd`, 이미지+텍스트 스플릿 `.nk-split`)는 **`custom.css §3`(전역 1회 로드)**에 둔다.
per-section CSS에는 그 섹션 고유 스타일(히어로 오버레이, 영상 16:9, USP 아이콘 등)만.

### 17-2. ⚠️ 카페24 상품 변수 함정 (상품카드 `prd.html` 실측)

| 변수 | 실체 | 올바른 사용 |
|---|---|---|
| `{$product_name}` | **`<span>…이름…</span>` 태그를 반환** (plain 문자열 아님) | 요소 '내용'으로만. **속성(`alt=` 등)에 절대 넣지 말 것** → 따옴표 깨짐으로 카드 전체 마크업 붕괴 |
| `{$seo_alt_tag}` | plain 문자열(상품명) | `<img alt="{$seo_alt_tag}">` 에 사용 |
| `{$image_medium}` | 이미지 URL | `<img src="{$image_medium}">` (그대로 src에) |
| `{$product_price}` | 숫자(예 `45000`) | 표시 시 `{$product_price|numberformat}원` → `45,000원` |

> 증상: 상품 썸네일 위에 `상품명" loading="lazy">` 같은 텍스트가 새어나오고 카드가 깨짐
> = `alt="{$product_name}"` 가 span의 `"` 때문에 속성을 깨뜨린 것. → alt는 `{$seo_alt_tag}`로.

상품 모듈은 `product_listmain_N` + `anchorBoxId` **2개 이상**(1개면 1개만 출력) 규칙 준수.
실제 콘텐츠는 `<!--@import(/_nk/inc/prd.html)-->`로 분리.

### 17-3. ⚠️ 카페24 Swiper는 구버전(v4/5) — 클래스·breakpoints 다름

- 초기화 클래스가 **`swiper-container-initialized`** (v6+의 `swiper-initialized` 아님). 검증 셀렉터 주의.
- v4/5는 `breakpoints`의 min/max 의미가 불안정 → `slidesPerView:숫자 + breakpoints`가 안 먹는다.
- **버전 무관 해법**: `slidesPerView:'auto'` + **CSS로 슬라이드 폭 직접 지정**(반응형).
  ```css
  .nk-prdslide__swiper .swiper-slide { width: calc(25% - 18px); } /* 데스크탑 4개 */
  @media(max-width:1024px){ ... width: calc(33.333% - 16px); }     /* 태블릿 3 */
  @media(max-width:767px){ ... width: calc(50% - 12px); }          /* 모바일 2 */
  ```
  (spaceBetween 만큼 슬라이드 우측 margin 이 붙으므로 폭에서 `gap*(n-1)/n` 차감)

### 17-4. ⚠️ 인라인 `new Swiper()` 는 파싱 시점에 실패한다 → 가드 필수

카페24 optimizer가 head의 `swiper-bundle.min.js`를 **지연 로드**할 수 있어, body 조각의
인라인 `<script>`가 실행될 때 `Swiper`가 아직 undefined → `ReferenceError: Swiper is not defined`.

```js
(function(){
  function init(){ new Swiper('.nk-xxx-swiper', { ... }); }
  if (window.Swiper) init();
  else window.addEventListener('load', init);   /* 로드 완료 후 보장 실행 */
})();
```

### 17-5. ⚠️ Phosphor Icons는 `custom.css @import` 로 넣지 말 것

카페24 optimizer가 `@import`한 외부 아이콘 CSS에서 **`@font-face`만 인라인하고 `.ph`/`.ph-*` 클래스
규칙을 누락**시킴 → 폰트는 로드되는데 아이콘이 안 보임(실측: `.ph` 계산 font-family가 Pretendard로 나옴).
(Pretendard는 전부 `@font-face`라 `@import`로도 정상 동작 → 아이콘 폰트와 다름)

**해법**: `layout/basic/layout.html`(과 main.html) `<head>`에 **정식 `<link>`**로 로드(구글폰트처럼 optimizer 미관여).
```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@phosphor-icons/web@2.1.1/src/regular/style.css">
```
사용: `<i class="ph ph-arrow-right"></i>`. IDIO 원본의 FontAwesome(`fa-*`)는 전부 Phosphor로 교체.

### 17-6. ⚠️ 카페24 컴파일 페이지 캐시 — TTL 약 2~3분

SFTP 업로드 후에도 라이브가 **즉시 갱신되지 않는다**(컴파일된 스킨 페이지를 캐시).
`?nkv=숫자` 같은 임의 쿼리로는 안 깨짐. **업로드 후 약 2~3분 기다린 뒤** 라이브 재검증할 것.
(원격 파일이 맞는지 먼저 SFTP로 확인하면 "업로드 누락"과 "캐시"를 구분 가능)

### 17-7. ⚠️ 데이터 의존 섹션 — 데이터 없으면 "빈 헤딩만 남는 버그" → 자동 숨김 필수

리뷰(`board_fixed_4`)·저널(`board_list_8`)·영상(유튜브) 섹션은 데이터/콘텐츠가 없으면
**모듈 안쪽(슬라이드)만 비고 섹션 셸(헤딩·View All·화살표)은 그대로 남아** "헤딩만 둥둥 뜬 빈 공간"
버그가 된다(실측: rvArea/journal 각각 빈 446px, vod 는 placeholder 유튜브 `00000000000` 가 '영상 사용 불가'로 표시).

**해법 — 각 조각에 self-hide 스크립트**(재판매 시 데이터 넣으면 자동 노출):
```js
/* 리뷰/저널: 실제 슬라이드 0이면 섹션 통째 숨김 */
function init(){
  var sec=document.querySelector('.nk-rv'), sw=document.querySelector('.nk-rv__swiper');
  var n = sw ? sw.querySelectorAll('.swiper-slide').length : 0;
  if(!sw || n===0){ if(sec) sec.style.display='none'; return; }  /* ← 빈 섹션 숨김 */
  new Swiper('.nk-rv__swiper', { ... });
}
if(window.Swiper) init(); else window.addEventListener('load', init);
```
```js
/* 영상: 유튜브 ID가 아직 placeholder(00000000000)면 깨진 임베드이므로 숨김 */
var sec=document.currentScript.closest('.nk-vod'), ifr=sec&&sec.querySelector('iframe');
if(sec&&ifr&&(ifr.getAttribute('src')||'').indexOf('00000000000')>-1){ sec.style.display='none'; }
```
- **재판매 시**: 조각 상단 주석대로 게시판 번호(4·8)·유튜브 ID·스냅위젯 코드를 실제 값으로 교체 → 섹션 자동 노출.
- 인스타(스냅위젯)는 샘플 위젯이 항상 로드되므로 빈 섹션 아님(교체만 안내).

### 17-11. ⚠️ `.inner` 이중 패딩 — `.inner` 섹션이 헤더보다 좌우가 한 단계 더 좁아지는 함정

**증상**: 메인에서 `.inner`를 쓰는 섹션(prdTab·bnr1·split 등)이 `.inner`가 없는 섹션·헤더보다
좌우가 한 번 더 안쪽으로 들어간다(라이브 실측: 헤더 콘텐츠 시작 50px vs `.inner` 섹션 100px, 폭 -100px).
**원인**: `layout.html`/`main.html`의 `<div id="container" class="inner">`가 좌우 패딩(50px)을 **1차**로 주는데,
그 안의 섹션 조각이 또 `<div class="inner">`를 쓰면 `#nk-skin14 .inner` 규칙이 패딩을 **2차**로 또 줘서 이중이 된다.
(헤더/푸터 `.inner`는 `#contents` 밖이라 단일이므로, 본문 `.inner`만 두 배가 됨 → 끝선 불일치)
**해결**: 컨테이너가 패딩을 책임지므로, `#contents` 안의 `.inner`는 패딩 0 + 폭 100%로 정리.
```css
/* 일반 섹션: 컨테이너가 이미 패딩 → 자체 패딩 제거(이중 방지). 헤더/푸터는 #contents 밖이라 무영향 */
#nk-skin14 #container.inner #contents .inner { max-width:100% !important; padding-left:0 !important; padding-right:0 !important; }
/* 풀블리드(.nk-full)는 100vw로 빠져나갔으니 그 안 .inner 는 단일 패딩 복구 (BP별로도) */
#nk-skin14 #container.inner #contents .nk-full .inner { max-width:var(--nk-container) !important; padding-left:var(--nk-pad-pc) !important; padding-right:var(--nk-pad-pc) !important; }
```
(확인: bnr1·prdTab 콘텐츠 시작 100px→50px 로 헤더와 끝선 일치, 폭 1531=헤더와 동일.)

### 17-12. ✅ 섹션을 풀블리드(배경 화면 끝까지)로 바꾸는 패턴

**원하는 모습**: 배경 띠는 화면 끝까지(100vw) 꽉 차고, 글자/콘텐츠는 가운데 좁게.
**핵심 2가지**:
1. 섹션에 `nk-full` 클래스 추가 → `#contents > .section.nk-full` 규칙이 `margin:calc(50% - 50vw); width:100vw` 로 컨테이너 패딩을 뚫고 화면 폭으로 빠져나감(배경 풀폭).
2. 콘텐츠를 `.inner`(반응형 좌우여백 공통박스) 안에 넣고, 좁은 칼럼이 필요하면 그 **안쪽에 별도 박스**(`.inner` 아님)를 둠.
```html
<section class="section nk-sec nk-full nk-bnr1">  <!-- nk-full = 배경 풀폭 -->
  <div class="inner">                              <!-- 반응형 좌우여백(공통) -->
    <div class="nk-bnr1__inner">…</div>            <!-- 가운데 820px 글자칼럼 -->
  </div>
</section>
```
**왜 안쪽 박스를 분리?** 글자칼럼에 `.inner`를 같이 붙이면 §17-11 의 `.nk-full .inner` 규칙(max-width:1920 복구)이 칼럼의 `max-width:820px`를 덮어써서 글자가 화면 전체로 퍼진다. 그래서 "바깥=`.inner`(반응형 패딩) / 안쪽=좁은 칼럼(`.inner` 아님)" 두 겹으로 분리.
**주의(100vw 스크롤바 오버플로)**: `width:100vw`는 세로 스크롤바 폭만큼 본문보다 넓어 가로 스크롤이 생길 수 있는데, 전역 `section { overflow:hidden }` 가 빠져나간 부분을 잘라줘서 이 스킨은 가로 스크롤 0(라이브 확인: scrollWidth==clientWidth).
**이미 `.inner` 안에 콘텐츠가 든 일반 띠배너**(좁은 칼럼 불필요)는 섹션에 `nk-full` 만 추가하면 끝.

### 17-13. ✅ 서브페이지 우리화 전략 + 카페24 기본 아이콘을 Phosphor로 교체(기능 보존)

**전제(라이브 실측으로 확인된 사실)**: custom.css 가 `#nk-skin14`(body id, 전 페이지 공통) 스코프라
**버튼/폼/타이포 전역 토큰은 로그인·상세·장바구니 등 서브페이지에 이미 자동 적용**된다(서브페이지 "전무"가 아님).
서브페이지 우리화는 "처음부터 다시"가 아니라 **(a) 전역 토큰이 안 닿는 페이지 고유 요소 + (b) 카페24 기본 아이콘 이미지** 두 가지만 보강하면 된다.
서브페이지 미리보기 URL: `?skin_no=skin14` 를 직접 붙여야 적용됨(내부 링크는 순정 경로라 컨텍스트 안 실림). 빈 카테고리(cate_no=1)는 다른 스킨이 떠 오판 주의 — 상품 있는 카테고리로 확인.

**핵심 기법 — 카페24 기본 아이콘 img 위에 Phosphor 글리프 깔기(클릭 기능 100% 보존)**:
상품목록 카드 hover 아이콘(`.icon__box .wish/.cart`)·플로팅 위젯 등은 카페24가 **클릭 핸들러를 가진 `<img>`** 로 렌더한다. img 를 지우면 기능이 죽으므로:
```css
/* 1) 카페24 img: 투명하게 + 원형 전체를 덮어 클릭만 보존 */
#nk-skin14 .icon__box .cart img { position:absolute; inset:0; width:100%; height:100%; opacity:0; cursor:pointer; z-index:1; }
/* 2) 부모 span 에 Phosphor 글리프(::before, pointer-events:none 로 클릭은 img 로 통과) */
#nk-skin14 .icon__box .cart { position:relative; display:flex; align-items:center; justify-content:center; width:40px; height:40px; background:var(--nk-theme); border-radius:50%; font-size:0; }
#nk-skin14 .icon__box .cart::before { font-family:"Phosphor"; content:"\e41e"; font-size:19px; color:#fff; pointer-events:none; }
```
- 글리프 코드는 **추측 금지** — 로드된 Phosphor 폰트에서 실측(probe `<i class="ph ph-xxx">` 만들어 `getComputedStyle(el,'::before').content` 읽기). 실측값 예: heart `\e2a8` / shopping-cart `\e41e` / sliders-horizontal `\e434` / caret-up `\e13c` / caret-down `\e136` / clock-counter-clockwise `\e1a0`.
- 텍스트 라벨(WISH/ADD)은 `font-size:0` 로 숨기되 DOM 유지(a11y). `::before` 는 자체 font-size 명시.
- **옵션 미리보기(.option)** 는 옵션상품일 때만 img 가 생기므로 `.option{display:none}` + `.option:has(img){display:flex}` 로 EZ 자동숨김 존중(빈 원 방지).
- **모바일 격리 필수**: 카페24 base 는 ≤1024px 에서 `.icon__box{display:none}` 인데 `#nk-skin14` 스코프가 이를 덮어 투명 클릭막이 남아 오탭 위험 → `@media(max-width:1024px){ #nk-skin14 .prdList__item .icon__box{display:none !important} }` 로 모바일 숨김 복원.
- **여분 검정 바 제거**: base EZ 는 `.icon__box` 에 `background:rgba(1,1,1,.5)` + `width:100%` 풀폭 띠를 깐다(버튼 뒤 어두운 막대). 원형 버튼만 남기려면 `.icon__box{ background:none !important; width:auto !important; height:auto !important; padding:0 !important }` 로 컨테이너를 지우고 우하단(`right/bottom`)에 콘텐츠폭으로 띄운다.
- **CSS 캐시 주의**: 페이지 `?nkv=N`은 HTML만 갱신하고 `<link>`의 `_nk/css/custom.css` URL은 그대로라 브라우저가 옛 CSS를 재사용한다. 변경이 안 보이면 하드 리로드(Cmd/Ctrl+Shift+R) 또는 `fetch('/_nk/css/custom.css',{cache:'no-store'})` 로 서버 반영 여부부터 확인.
- 카드 마크업이 우리 스킨 파일(`product/list_product.html`)이고 아이콘이 단순 `<img>`(링크/onclick 보유)면, **footer.html 의 #right_quick 처럼 마크업에서 직접 `<i class="ph">` 로 교체**하는 게 더 깔끔(이때 `<a href/onclick>` 은 보존). 어느 쪽이든 카페24 클릭 핸들러를 건드리지 않는 게 원칙.

(라이브 확인: 카드 hover → 차콜 원형+하트/카트 Phosphor, 클릭 보존 / 플로팅 위젯 탄색#d0ac88 → 흰 원+라인+Phosphor, onclick 보존 / 콘솔 에러 0.)

### 17-10. ⚠️ CSS Grid 상품목록인데 썸네일이 칸의 1/4로 작게 나오는 함정

**증상**: `.nk-prd-grid`(CSS grid, 4열)인데 상품 썸네일이 칸 폭을 안 채우고 작게(예: 340px 칸에 85px) 렌더.
**원인**: 카페24 상품모듈(`product_listmain_N`)이 상품 `<li>`에 자체 4단 **float 레이아웃용 `width:25%`**를
주입한다(+`.xans-record-` 클래스 자동 부여). 그리드 칸 안에서 이 `width:25%`가 **칸(340px)의 25%=85px**로
li 를 줄여버려 그 안의 썸네일·이미지가 같이 작아진다. (캐러셀(swiper-slide)은 슬라이드 폭을 직접 지정하므로 무영향 — **그리드 섹션에서만 발생**)
**해결**: 그리드의 상품 li 를 칸에 꽉 채우도록 강제.
```css
/* #[body-id] ID 스코프라 카페24 클래스 룰보다 우선 → !important 불필요 */
#nk-skin14 .nk-prd-grid > .nk-prd { width: 100%; min-width: 0; max-width: 100%; float: none; }
```
(확인: li 에 `width:100%` 강제 시 85px→341px 로 칸을 꽉 채움.) 더불어 카드 `img { display:block }` 로 인라인 여백 제거.

### 17-9. `product_listmore_N` 더보기 버튼이 안 보이는 건 정상일 수 있다

메인진열 그룹에 `$count` 이하의 상품만 진열돼 "다음 페이지"가 없으면 카페24가 `product_listmore_N`
모듈을 **출력하지 않는다**(래퍼 div째 사라짐). 버튼 부재 ≠ 버그. 더보기를 보려면 해당 메인진열에
`$count` 보다 많은 상품을 진열.

### 17-8. 버튼 디자인시스템 통일 (기능 페이지 전수 점검)

카페24 기본 버튼은 페이지마다 다른 색이 섞여 있다. 라이브 실측으로 이탈 요소를 찾아 토큰으로 통일.
- 실측: `.btnSubmit`/`.btnNormal`은 이미 차콜/라인 통일됨. **`.btnSubmitFix`만 테마 기본 탄색(#d0ac88)+radius0**으로 이탈 → 골드 액센트(`--nk-accent`)+radius2 로 통일.
- 매핑: 강조계열(`.btnStrong`/`.btnEmphasis`/`.btnSubmitFix`)=골드 / 라인계열(`.btnLine`/`.btnBasic`/`.btnNormalFix`)=라인 토큰.
- **색·테두리·라운드만 맞추고 높이·패딩은 건드리지 않는다** → 장바구니/주문 등 기능 페이지 레이아웃 안전.
- 제외: SNS 로그인(`.btnKakao`/`.btnNaver` 등 브랜드색), `.btnClose`(X), `.btnDelete`.

---

## 18. 재판매 템플릿 "우리화" 작업 지침서 (미래 에이전트 재현용)

> 목적: 새 카페24 EZ 스킨을 받아 "우리 디자인시스템(차콜·골드·Pretendard·Phosphor·박스버튼·라인토큰)"으로
> **메인+서브페이지 전체를 일관 통일**하는 작업을, 미래 에이전트가 이 절을 그대로 따라 재현하도록 정밀 기술한다.
> 단일 에이전트로 벅차면 **조사 단계를 3개 서브에이전트 병렬**로 띄운다(아래 18-2).

### 18-0. 대전제 (먼저 머리에 박아둘 사실)
1. **custom.css 는 `#nk-skin14`(body id, 전 페이지 공통) 스코프** → 버튼/폼/타이포 전역 토큰이 로그인·상세·장바구니 등 **서브페이지에 자동 적용**된다. "서브페이지는 손도 안 댔다"는 가정은 틀림. 이미 닿아 있다.
2. **CSS 로드 순서**: layout.html 에서 custom.css(앞) 이후 sub_style/sub_theme/add_theme*(뒤)가 로드된다 → "나중 로드라 이긴다"는 가정 금지. 우리가 이기는 건 **오직 `#nk-skin14` ID 스코프(우선순위)** 덕분. ID 없는 룰은 뒤 EZ룰에 진다.
3. **활성 테마 = `theme01`**(브라운 #d0ac88). 브라운 출처는 `sub_theme.css`(무스코프). ID스코프로 덮은 곳만 차콜이고, 안 덮은 곳(.sale_box 등)은 브라운 잔존.
4. **글로벌 룰 과침범 역설**: `#nk-skin14 h3`/`#nk-skin14 input` 같은 글로벌이 **너무 세서** 약관 라벨(h3)·수량칸(input)까지 침범해 버그를 만든다. 해결은 "EZ를 더 덮기"가 아니라 **더 구체적 셀렉터로 좁혀 되돌리기**(!important 불필요).
5. **CSS 캐시 함정**: 페이지 `?nkv=N`은 HTML만 갱신, `<link>`의 custom.css는 브라우저 캐시 재사용 → 변경이 안 보이면 하드리로드(Cmd/Ctrl+Shift+R) 또는 `fetch('/_nk/css/custom.css',{cache:'no-store'})`로 서버 반영부터 확인.
6. **서브페이지 프리뷰 URL**: `?skin_no=skin14` 직접 부착(내부 링크는 순정 경로라 컨텍스트 안 실림). **빈 카테고리(cate_no=1)는 다른 스킨이 떠 오판** → 상품 있는 카테고리로 확인. 마이페이지·담긴 장바구니는 로그인 필요(에이전트는 비번 입력 금지) → 로그아웃 가능 영역까지만.

### 18-1. 작업 순서 (Phase)
1. **조사(병렬)** → 2. **PRD 스토리화** → 3. **구현(순차, custom.css 단일파일이라 병렬편집 금지)** → 4. **전수 시각검증(라이브)** → 5. **리뷰어 승인(자가승인 금지)** → 6. **AA 대비 보정** → 7. **WORK-GUIDE 반영**.

### 18-2. 조사 단계 — 3개 서브에이전트 병렬 디스패치 (READ-ONLY)
동시에 한 번에 띄운다(독립 작업):
- **에이전트 A — skin2 토닝 추출**: `skin2/_idio/css/{custom,common}.css` + IDIO 개조 base(`layout/basic/css/sub_style.css`, `ec-base-button/table/ui/box.css`) + `css/module/{order,member,myshop}/*` 정독 → 영역별(버튼·테이블·폼·장바구니·회원·게시판·타이틀) `셀렉터{속성:값}` → 우리토큰 매핑표.
- **에이전트 B — skin14 잔존 EZ 전수 audit**: `_nk/css/custom.css`(덮은 범위) vs `layout/basic/css/*`(순정) 대조 → 우리 토큰 이탈 목록(P1~P3) + 2대 버그(회원가입 동의 h3 크기 / 상세 수량칸 높이) file:selector:현재값→필요값.
- **에이전트 C — 디자인시스템 일관성 + 박스버튼 스펙**: custom.css 버튼 인벤토리(링크형/박스형) + 박스버튼 통일 CSS 초안 + inc/*.html 전환목록 + 토큰 하드코딩 목록.

### 18-3. 핵심 구현 규칙
- **디자인 토큰**(:root): `--nk-theme #1a1a1a`(1차) / `--nk-accent #a68a64`(골드=결제·주문 확정 + 텍스트 악센트 전용) / `--nk-bg2 #f7f5f1` / `--nk-line rgba(0,0,0,.08)` / `--nk-line-strong rgba(0,0,0,.18)` / `--nk-on-theme #fff` / `--nk-radius 2px` / `--nk-control-h 50px`.
- **박스버튼 위계(전 CTA 박스형)**: `.nk-btn`=차콜 채움(1차) / `.nk-btn--line`=투명+차콜라인→hover 차콜채움(2차) / `.nk-btn--accent`=골드(전환 1종) / `.nk-btn--sm`(카드 내부) / `.nk-btn--block`(풀폭). 구 `.nk-btn-link`→라인, `.nk-btn-solid`→1차 **별칭 유지**(기존 마크업 자동 박스화 + 히어로 오버라이드 `.nk-hero .nk-btn-solid` specificity 보존). 화살표는 박스 안 + hover translateX(4px).
- **skin2 서브 토닝 공식 → 우리토큰**: 테이블 `border-top:2px var(--nk-theme)` + th `bg2` + 셀 `1px var(--nk-line)` / 합계·옵션 박스는 테두리 대신 `bg2` 면 + 구분만 `1px line` / 회원박스 `1px line` / 페이징 `border-radius:50%` + current 차콜채움 / 폼 focus `var(--nk-accent)` + `outline:1px`(제거 금지).
- **2대 버그 복원 패턴**(글로벌 과침범): `#nk-skin14 .xans-member-agreement .agreeAll h3, ... .title h3 { font-size:var(--nk-fs-body); font-weight:400 }` / `#nk-skin14 .xans-product-detail .quantity input[type=text] { height:30px; line-height:28px; padding:0; text-align:center }` (장바구니 `.gCheck .quantity` 40px 보존 위해 `.xans-product-detail` 스코프 필수).
- **카페24 기본 아이콘 → Phosphor**(§17-13): img `opacity:0`로 클릭 보존 + span `::before` Phosphor 글리프(코드는 실측). 모바일 `@media(max-width:1024px){.icon__box{display:none}}` 오탭 방지.
- **WCAG AA 필수**: 골드(#a68a64) 위 **흰 글씨는 3.26으로 미달** → 골드 버튼 글씨는 **차콜**(5.34 통과). 보조색(#8a8a8a)은 본문 대비 미달이니 큰글씨/보조정보에만.

### 18-4. 검증 프로토콜
- 업로드: 프로젝트 루트에서 `python3 sftp_push.py /skin14` → 카페24 컴파일 캐시 **2~3분 대기** → 하드리로드 후 라이브 측정.
- 페이지별 DOM 실측(getComputedStyle) + 스크린샷. PC + (가능하면)모바일 뷰 함께. 콘솔 에러 0 확인(단, `/skin-skin2/...` 출처 에러는 기본스킨 잔존물이라 우리 무관).
- **자가승인 금지**: 변경 후 `code-reviewer` 서브에이전트로 specificity·스코프 누수·규칙·AA 검증 → 지적 반영.

### 18-5. 함정 체크리스트 (반복 금지)
- [ ] custom.css 단일파일 → 서브에이전트 병렬 **편집** 금지(조사만 병렬, 구현 순차).
- [ ] 글로벌 h3/input 침범 → 좁은 셀렉터로 복원(!important 말고 specificity).
- [ ] 히어로 흰버튼 오버라이드(`.nk-hero .nk-btn-solid`) 별칭 유지로 보존됐는지.
- [ ] `.icon__box` 검정 바(`rgba(1,1,1,.5)`·풀폭) 제거(background:none/width:auto).
- [ ] 골드 버튼 글씨 차콜(AA).
- [ ] 빈 카테고리·CSS캐시로 인한 오판 주의(하드리로드/no-store fetch).
- [ ] 로그인 필요 페이지(마이페이지·담긴 장바구니)는 로그인 후(또는 장바구니 1건 담고) 검증 — `?skin_no` 빼고 순정 URL로.
- [ ] **글로벌 heading/input 침범 전수 점검(중요)**: `#nk-skin14 h2/h3/input` 같은 bare 태그 글로벌이 약관·상세수량 외에도 **마이페이지·장바구니·게시판 소제목 h3 / 검색·옵션 input** 까지 키운다. 우리 메인 타이틀은 `.nk-sec__title` 등 자체 클래스라 무관하므로, **카페24 콘텐츠 래퍼(.myshopArea/.xans-myshop/.xans-order/.xans-member/.xans-board/.ec-base-box/.ec-base-prdInfo) 안 h3 는 소제목 크기(var(--nk-fs-lead))로 리셋**. 한 군데(약관)만 고치고 끝내면 같은 버그가 다른 페이지에 잔존한다.
- [ ] **콘텐츠 래퍼 폭**: EZ `.myshopArea` 는 `width:calc(92% - 280px)` + `max-width` + `margin:auto` 3종으로 가운데 쪼그라든다. full-width 로 풀려면 **width·max-width·margin 3개 모두** 해제(`width:100%`), padding-left(사이드메뉴용)는 유지.
- [ ] 동일 셀렉터(input:focus 등) 중복 정의 금지 — 단일 소스로.

### 18-6. ★ 잔존 흰/회색/골드 박멸 = base CSS 직접 토큰화 (skin2/IDIO 방식, 2026-06-03 확립)

**대전제(가장 중요):** 카페24 스킨에는 하드코딩 색이 박힌 base CSS가 **두 레이어**다.
1. `layout/basic/css/*.css` (ec-base-*, sub_style 등)
2. **`css/module/**/*.css`** (188개, 카페24 모듈 자동주입) ← **이걸 빠뜨리면 `.totalPrice`·`.tabProduct`·골드 `#d0ac88` 가 영원히 잔존한다.** 그동안 whack-a-mole 한 진짜 원인.

**오버라이드(`#contents *` transparent !important)로 덮지 말고, skin2처럼 base CSS의 하드코딩 색을 우리 토큰 참조로 직접 치환한다.** 토큰 정의는 custom.css `:root` 에 이미 있음(skin2의 `_idio/color.css` 역할).

**속성별 안전 치환 (perl, `color:#fff` 흰글자는 절대 안 건드림):**
```bash
# 반드시 백업 먼저: cp -R css/module /tmp/backup
# find -exec 사용 ($FILES 변수에 188개 경로 담으면 "File name too long" 에러남)
find css/module layout/basic/css -name '*.css' -exec perl -pi -e \
  's/(background(?:-color)?\s*:\s*)#(?:ffffff|fff)\b/${1}var(--nk-bg)/gi' {} +      # 흰배경→bg
find ... -exec perl -pi -e 's/#(?:e5e5e5|e8e8e8|ebebeb|d7d7d7|ccc|ddd|cccccc|dddddd)\b/var(--nk-line)/gi' {} +  # 회색테두리→단일선색
find ... -exec perl -pi -e 's/#(?:f6f6f6|f9f9f9|f5f5f5|fafafa)\b/var(--nk-bg2)/gi' {} +   # 밝은회색배경→bg2
find ... -exec perl -pi -e 's/#(?:d0ac88|d8ac88)\b/var(--nk-accent)/gi' {} +              # 카페24 기본골드→accent(모노크롬)
```
- 핵심: `background...:#fff`만 토큰화, **`color:#fff`(다크버튼 위 흰글자)는 패턴에서 제외 → 안 깨짐.** 회색들은 전부 border 용도(color 사용 0)라 전역 치환 안전.
- 검증: `(?<!background-)\bcolor\s*:\s*#fff` 건수(흰글자)가 치환 전후 동일해야 함. `grep -P` 는 macOS BSD grep 에서 안 먹으니 GNU grep 또는 `background:#fff` 를 먼저 없앤 뒤 `color:#fff` 단순 카운트로 확인.

**치환 후:** custom.css 의 `#contents * { background:transparent !important }` 일괄 오버라이드는 **제거**한다(base 토큰이 솔리드 그레이지를 네이티브 제공 → fixed 바 등도 정상). 의도적 컴포넌트 재지정(.nk-btn 차콜·.nk-prd__thumb bg2·선택탭 강조)만 남김.

**검증 결과(라이브):** 홈·상세·장바구니·목록·로그인·게시판 6종 전수 — 잔존 흰배경 0 / 골드 0 / 흰글자깨짐 0. `.totalPrice`·`.tabProduct` 그레이지 확인.

**남는 의도적 색(잔존 아님, 둬도 됨):** 알림 뱃지 `#009ffa`(파랑)·`#9a9a9a`(회색 카운트), 본문 텍스트 회색(#999/#555/#333) — skin2도 그대로 둠. 완전 모노크롬 원하면 별도 지시 시 처리.

**⚠️ base CSS 직접 수정 규칙:** 원래 "base 수정 금지"였으나 — 재판매 템플릿(우리 소유, 우리가 업데이트 시점 통제)에서는 skin2/IDIO처럼 base 토큰화가 더 우월(오버라이드 해킹·!important 전쟁·캐시싸움 제거). 클라이언트 운영 스킨에서 카페24가 base 를 덮어쓸 위험이 있을 때만 오버라이드 방식 유지.

### 18-7. ★ 상세 sticky 구매정보 + 타이포(레퍼런스 maeve) + 토큰화 완결 (2026-06-03 2차)

**(A) 상세페이지 우측 구매정보 sticky — 실패 원인은 `overflow-x:hidden`이었다 (핵심).**
- 레퍼런스(maeve, ecudemo393674)는 **순수 CSS `position:sticky; top:81px`(헤더높이)** + 좌우 flex 50/50. JS 안 씀. (skin2 는 다름 — 상세 다 지난 뒤 우상단에 뜨는 JS 플로팅 카드라 "스크롤 내내 따라붙는" UX 아님. 따라붙길 원하면 레퍼런스의 CSS sticky 방식이 정답.)
- skin14 구조: `detail.html` 에서 [상세 + 쿠폰 + product_additional]을 `.nk-pdp` 로 감싸고, `@media(min-width:1025px)` 에서 `.nk-pdp{display:grid; grid-template-columns:1fr 460px}` + 중간 래퍼(`.xans-product-detail`,`.detailArea`) `display:contents` 로 녹여 `.imgArea`(좌)·`.infoArea`(우) 를 grid 아이템으로 끌어올림. `.infoArea{grid-column:2; grid-row:1/-1; position:sticky; top:calc(띠+헤더+여유)}`.
- **❗ 실패 진짜 원인**: `body`/`html` 에 걸린 **`overflow-x:hidden`** (가로 넘침 차단용). overflow:hidden 은 **스크롤 컨테이너를 만들어 자식 `position:sticky` 를 무력화**한다(유명한 함정). 증상: sticky 인데 스크롤하면 그냥 같이 밀려 사라짐.
- **✅ 해결**: `overflow-x: hidden` → **`overflow-x: clip`**. clip 은 가로 넘침은 동일하게 막으면서 스크롤 컨테이너를 **안 만들어서** sticky 가 정상 작동. (spec: overflow-x:clip + overflow-y:visible → overflow-y 가 auto 로 안 바뀜.)
- 검증법: 스크롤 0/150/300/450/600 에서 `.infoArea` 의 `getBoundingClientRect().top` 이 계속 top 값(예 206)으로 고정되면 성공. 단 **상세설명이 짧은 데모 상품은 좌측 컬럼이 낮아 sticky 이동 범위가 작다** → 긴 상품으로 확인하거나 좌측 높이>우측 높이 확인.

**(B) 타이포 = 레퍼런스 maeve + ORDINARY 디자인시스템.** 두 레퍼런스 모두 **본문=Bricolage Grotesque 13px/lh1.6/-0.25px/400**(동일). **차이점: ORDINARY(ecudemo392574)는 제목·GNB·영문 디스플레이에 `Marcellus`(우아한 세리프) 400 을 씀.** 팔레트(#f5f5f0/#222)는 양쪽 동일.
- 구현: layout.html·main.html `<head>` 에 Bricolage + **Marcellus** Google Fonts `<link>` 추가(@import 금지 — optimizer 함정).
- `body#nk-skin14{font-family:"Bricolage Grotesque","Pretendard",…; font-size:13px; line-height:1.6}`, `--nk-ls:-0.25px`.
- **디스플레이 토큰** `--nk-font-display:"Marcellus","Pretendard",…,serif` → `h1~h3 / .nk-sec__title / .nk-hero__title / .nk-journal__title / .nk-title* / #header .top_category>ul>li>a` 에 적용. **Marcellus 는 한글 글리프가 없어 한글 제목·GNB 는 자동으로 Pretendard 로 fallback** (영문만 세리프) — ORDINARY 와 동일 동작. 검증: 영문 제목 fontFamily=Marcellus / 한글 제목은 Pretendard 로 렌더.
- (※ 이전 "-1px 전역통일"·"Pretendard 유지" 결정은 사용자 재지시로 -0.25px·Bricolage+Marcellus 채용으로 변경됨 — 디자인 결정은 매번 확인할 것.)
- ⚠️ **번들 캐시**: custom.css 변경(토큰·규칙)은 optimizer 번들 재생성까지 2~5분 지연될 수 있음. 서버 raw 파일엔 즉시 반영되나(no-store fetch 로 확인), 렌더는 늦음 → 너무 일찍 검증하면 "미적용"으로 오판. `getComputedStyle(:root).--nk-font-display` 가 빈값이면 번들 아직 안 옴 → 더 대기.

**(C) 1차 토큰화가 불완전했다 — 회색 "변종" + 골드 누락.** 1차에서 `#e5e5e5/#e8e8e8/#ebebeb/#ccc/#ddd/#d7d7d7/#f6f6f6/#f9f9f9` 만 잡고, **`#fbfafa #d7d5d5 #e9e9e9 #e3e3e3 #d6d6d6 #e6e6e6 #e8e5e4` 등 변종 회색(134곳)과 `layout/basic/css` 의 골드 #d0ac88(30곳)·`#1a1a1a`(79곳)·italic(1곳)** 이 남아있었다. → **회색은 정확한 hex 목록을 전수 enumerate**(눈대중 금지), **골드 치환은 css/module·layout/basic 양쪽 모두** 돌릴 것. `#1a1a1a→var(--nk-theme)`(다크 통일), `font-style:italic→normal`(CLAUDE 금지). 배경/테두리 구분: `background:#xxx→bg2`, 나머지→line.

**(D) ⚠️ 셸 변수에 파일목록 담지 말 것.** `FILES=$(find …); perl … $FILES` → 경로가 한 덩어리로 전달돼 `find: File name too long` / `bfs: No such file or directory` 로 **조용히 실패**(편집 0, 검증 grep 도 0 으로 나와 "성공"처럼 착시). 반드시 **리터럴 경로** 또는 `find … -exec perl … {} +` 사용. 실패 의심 시 리터럴 경로 grep 으로 실제 잔존 재확인.

**(E) 장바구니 "이용안내"(.ec-base-help .inner) = skin2식 면채움 박스.** skin2: `padding:50px; background-color:면채움(--nk-bg2); 테두리 없음`. skin14 진원지 3곳: ① `ec-base-help.css` 의 `.inner` 가 `border+border-top:#000` 박스 → 배경+50px 로 교체·테두리 제거(+모바일 30px), ② `sub_style.css` 의 `border-top:2px` 그룹에서 `.inner` 분리, ③ **함정**: custom.css 의 "중첩 .inner 이중패딩 방지" 규칙 `#container.inner #contents .inner{padding-left/right:0!important}` 이 **도움말 박스 좌우 패딩까지 0** 으로 만듦 → `#contents .ec-base-help .inner` 예외 규칙으로 좌우 50px(모바일 30px) 복원. (레이아웃-폭 .inner 와 콘텐츠-박스 .inner 가 같은 클래스명이라 생기는 충돌.)

**(F) 타이포 크기 = ORDINARY 실측 스케일 그대로.** 폰트만 바꾸고 크기를 우리 큰 스케일(h2 최대 34px)로 두면 안 됨 — ORDINARY는 작고 절제됨. 토큰을 실측값으로:
`--nk-fs-h1:clamp(26px,3vw,33px)`(워드마크급 33) · `--nk-fs-h2:clamp(20px,2.2vw,23px)`(**섹션제목 23**) · `--nk-fs-h3:clamp(17px,1.8vw,20px)` · `--nk-fs-lead:clamp(14px,1.2vw,16px)` · `--nk-fs-body:14px`(상품명) · `--nk-fs-sm:13px`(가격/본문). body 기준 `font-size:13px`.
- ❗ **섹션 조각 CSS의 하드코딩 크기 주의**: 히어로 제목이 토큰이 아니라 `mainBnr.css` 에 `font-size:clamp(32px,5vw,64px)`(=64px) 하드코딩돼 있어 토큰을 내려도 64px로 떴음 → `var(--nk-fs-h1)`로 교체(weight도 300→400). 가격 `.nk-prd__price` 도 `--nk-fs-body(14)` → `--nk-fs-sm(13)`. **토큰만 바꾸지 말고 조각 CSS의 하드코딩 크기를 grep 으로 찾아 토큰화**(`grep -rniE 'font-size\s*:\s*[3-9][0-9]px' _nk/css/*.css | grep -v var`).

**(G) 상세 PDP 폭 — 좌우 빈공간 + 우측 좁음.** `.nk-pdp{max-width:1400px;grid-template-columns:minmax(0,1fr) 460px}` 이면 넓은 화면서 양옆 빈 공간 + 우측 구매영역 좁음. → **`max-width:none`**(콘텐츠 폭 #contents 와 동일하게 가득, 좌우 잔여 0) + **`grid-template-columns:minmax(0,1.4fr) minmax(440px,1fr)`**(우측 ~42%로 확대). 검증: `.nk-pdp` 의 left/right 가 `#contents` 와 동일하면 빈공간 0.

**(H) 상세 안내 아코디언(.detail_guide) 2열 flex → 상단 어긋남.** base 가 `.detail_guide{display:flex;flex-wrap:wrap}` 로 폴드(PAYMENT/DELIVERY/EXCHANGE/SERVICE INFO)를 **2열 배치** + `.ec-base-fold+.ec-base-fold{margin-top:30px}` 가 2번째 폴드를 30px 내려 **상단 정렬 깨짐**(PAYMENT top 381 vs DELIVERY top 411). → `#nk-skinN #prdInfo .detail_guide{display:block}` + `> .ec-base-fold{width:100%}` 로 **세로 풀폭 스택**(레퍼런스 아코디언 방식). 폴드 검정선(#000)은 `var(--nk-theme)`로 토큰화.

### 18-8. ★ 헤더 유틸바 제거 · 푸터 톤 · 폼컨트롤 전수 · 페이징 화살표 · 상세 infoArea (2026-06-03 3차)

**(I) 상단 유틸바(toparea) 제거** — skin2·ORDINARY 모두 헤더 상단 유틸바(`.toparea`: 회원가입/로그인/주문조회/최근본상품/고객센터) **없음**. skin14: `#nk-skinN #header .toparea{display:none!important}`(모듈 보존) + **`--nk-header-h` 150→80px**(toparea 70 제거분) 으로 fixed 헤더 오프셋·`#container` padding-top 재정합. 로그인/장바구니는 우측 아이콘으로.

**(J) 푸터 = ORDINARY 톤 (⚠️ 레이아웃 건드리지 말 것)** — ❌ `.inner_t/.info_left/.info_right` 에 `display:flex;gap` 강제 → **base 2단 구조와 충돌, 전부 깨짐**(기본정보 전폭 늘어짐·우측블록 아래로). ✅ **레이아웃(display/gap/width)은 base 그대로, 색·폰트·여백만**: `#footer{background:transparent;border-top:1px solid var(--nk-line)}` + `.bt_title{font-family:var(--nk-font-display);font-size:var(--nk-fs-lead);font-weight:400}` + 본문 `var(--nk-fs-sm)/color:var(--nk-sub)` + 링크 hover `var(--nk-font)`. IDIO 푸터는 구조 재배치보다 톤 입히기가 안전.

**(K) 폼 컨트롤 전수 정규화 (select 화살표 겹침)** — 공통 input 규칙에 select 를 섞고 `padding:0 14px`(대칭) 주면, base 가 우측 caret(PNG, padding-right:30px 전제) 깔아둬 **긴 옵션 텍스트가 caret 과 겹침**. ✅ select 전용: `padding:0 36px 0 14px; appearance:none; background-image:url(SVG caret); background-position:right 14px center; background-size:11px 7px`. checkbox/radio 는 `accent-color:var(--nk-theme)`. → 정렬·회원유형·주문폼 모든 select 한 번에. **공통 input 에 select 섞을 땐 우측 caret 자리(padding-right≥32px) 필수.**

**(L) 페이징 첫/이전/다음/끝 화살표 안 보임** — base 의 border-chevron(`::before` 7px rotate)이 transform 풀려 안 보임 → 텍스트 글리프로: `.typeList>a::after{content:none!important}` + `.typeList>a::before{border:0!important;transform:none!important;font-size:15px;line-height:40px}` + `:first-child‹«›/:nth-child(2)‹‹›/:nth-last-child(2)‹››/:last-child‹»›`. 박스 bg/border 도 제거(원형 미니멀).

**(M) 상세 .infoArea 노트북서 우측 잘림** — base detail.css 의 구 2단 float용 `.infoArea{margin-left:100px}`가 grid(이미 column-gap)에서 우측 컬럼을 100px 밀어 뷰포트 밖 잘림. ✅ `#nk-skinN .nk-pdp .infoArea{margin:0!important;padding-left:0!important}`. + PDP `max-width:none` + 컬럼 `minmax(0,1.4fr) minmax(440px,1fr)`.

**(N) 회원 페이지 ORDINARY 미니멀** — `.xans-member-login{max-width:460px;margin:0 auto}`, 찾기/재설정 `max-width:420px`, 찾기류 `.ec-base-box.typeMember{padding:0!important;border:0!important}`(박스 벗기기, 회원가입 제외), `.ec-base-desc.gVer>li{border:0}`(행 구분선 제거), 입력칸 `border:1px solid var(--nk-line)+focus var(--nk-theme)`, 하단버튼 `.gBottom{display:flex}a{flex:1}`. URL: `/member/id/find_id.html`, `/member/passwd/find_passwd_info.html`.

### 18-9. ★ 헤더·푸터 구조 마이그레이션 (base → _nk/inc, "우리 식") + 회원 플로우 (2026-06-03 4차)

**대전제(검증됨)**: 색·톤=CSS 오버라이드 / **레이아웃·구조=HTML 재작성**(`_nk/inc/`). skin2 가 `@import(/_idio/inc/header·footer.html)` 로 자기 마크업을 쓰는 방식을 차용.

**(A) 헤더 `_nk/inc/header.html` 마이그레이션 (완료)** — `_nk/inc/header.html`(로고 Layout_LogoTop / GNB `_nk/inc/menu.html` Layout_category / 아이콘 statelogon·off·orderBasketcount / 검색 Layout_SearchHeader / 모바일 드로어) + `_nk/css/header.css` 신규. **layout.html·main.html 둘 다** `@import(/layout/basic/header.html)` → `/_nk/inc/header.html` 교체. 원본은 `_nk/_backup_header_layoutbasic.html` 백업·보존. 자산 `/_nk/`.
- **3분할 정렬 검증 패턴**(시행착오 끝 확정): inner flex 인데 어딘가 `justify-content:center` 가 먹어 로고가 가운데 쏠림 → **로고 `margin: auto auto auto 0 !important`**(상하 auto=수직중앙, 우 auto=좌측고정, justify-content 무관). **GNB `position:absolute; left:50%; transform:translateX(-50%)`**(중앙). **아이콘 `position:absolute; right:var(--nk-pad-pc); top:50%; transform:translateY(-50%)`**(우측 — 검색 form 이 flex 흐름에 static 으로 남아 분배 망치므로 absolute 로 뺌, right 반응형 미디어쿼리). 검증: 로고 left<90·수직중앙 / GNB cx≈vw/2 / 아이콘 right<90.
- raw `{$logo}/{$name_or_img_tag}` 가 innerHTML 에 남아도 화면 노출 0 이면 모듈 반복 템플릿 잔여(정상).

**(B) 푸터 `_nk/inc/footer.html` 마이그레이션 (완료)** — `_nk/inc/footer.html`(`.nk-ft` 구조: 회사정보 Layout_footer / Menu / Customer Center Layout_Info / Follow) + `_nk/css/footer.css`(grid 4컬럼→1024 2컬럼→540 1컬럼). 카피라이트 `{$mall_name}` 은 **별도 `module="Layout_footer"` 컨테이너로 분리**해야 치환됨. import 교체(layout.html+main.html), 백업 보존. **레이아웃은 footer.css 의 grid 로 명확히**(base 중첩 안 씀 — CSS flex 로 base 푸터 덮으려다 깨진 §18-8(J) 교훈 적용).

**(C) 회원 플로우 4단계 (완료)** — 로그인/약관동의/정보입력/가입완료 전부 ORDINARY 미니멀 통일. 회원 CSS(§18-7E 류: 중앙 narrow·박스 벗기기·세로폼·균등버튼) + 커스텀 차콜 체크박스/라디오(§18-8K) + select caret + 새 헤더/푸터가 플로우 전체 커버. join 폼은 `.ec-base-table.typeWrite`(바인딩 자리) 구조 보존하고 라벨셀 면채움+상단 차콜선+CSS만.

**(D) 마이그레이션 일반 절차** — ① executor(opus)로 현재 base header/footer 의 module·{$변수} 전수 식별 → 클린 `_nk/inc` 마크업에 그대로 이식 ② `_nk/css/*.css` 신규(토큰 사용) ③ layout.html+**main.html 둘 다** import 교체 ④ 원본 `_nk/_backup_*` 백업·보존(삭제 X) ⑤ 라이브 검증(모듈 치환·정렬·모바일) ⑥ custom.css 옛 클래스 규칙은 죽은 CSS(무해, 정리 선택).

### 18-10. ★ PC·모바일 전수 QA + 띠배너↔헤더 간격 버그 (2026-06-03 5차)

**(A) 전수 QA 결과(라이브 demo000, PC 1440 / MO 390)** — 홈·목록·상세·장바구니·로그인·약관·정보입력·아이디찾기·게시판 전 페이지 × PC·모바일에서 **치명·중간 버그 0건**. 가로 오버플로 0 / 미치환 변수 0 / 골드 잔존 0 / 흰박스 잔존 0 / 콘솔 에러 0. 제목 폰트도 전 요소 Marcellus 정상(33/23/16px) — QA 1차의 "제목=Bricolage" 지적은 오판이었음(라이브 computed 재확인). 잔여 항목은 전부 스킨 코드 아님: 로고 placeholder·통신판매업번호·CS시간(=관리자 데이터 미입력), 빈 카트/게시글 0(=데이터 한계).

**(B) ★ 띠배너↔헤더 간격 버그 (모바일 한정, 스크롤 시 본문 비침)** — 띠배너(`#nk-topBnr`, fixed top:0)와 헤더(`#header`, fixed `top:var(--nk-topbar-h)`)는 둘 다 fixed 스택. **함정**: 띠배너 높이는 topBnr.css 가 **PC 36px / 모바일(≤1024) 30px**(`--nk-tb-pc-height`/`--nk-tb-m-height`)로 줄이는데, 헤더 오프셋 `--nk-topbar-h` 는 custom.css :root 에 **36px 단일 고정**. → 모바일에서 띠 바닥(30) vs 헤더 top(36) = **6px 빈틈**, 스크롤하면 그 슬릿으로 본문이 비쳐 선처럼 보임. 데스크톱은 36=36이라 무증상이라 PC만 보면 못 잡음.
- ✅ **수정**: custom.css §14 에 `@media (max-width:1024px){ #nk-skin14 { --nk-topbar-h: 30px; } }` 한 줄. `#nk-skin14`(body)가 `#header`·`#container`보다 가까운 조상이라 모바일에서 30px 우선 적용 → 헤더 top·본문 padding(`calc(--nk-topbar-h + --nk-header-h)`)·드로어·sticky 계산이 **변수 한 곳 동기화로 일괄 정합**. 검증: MO gap 0(스크롤 전·후), PC gap 0(회귀 없음).
- **교훈**: 띠/헤더 높이가 **다른 파일의 독립 변수**(topBnr.css 의 띠높이 vs custom.css 의 `--nk-topbar-h`)면 BP마다 드리프트 점검 필수. 반응형으로 한쪽 높이를 바꾸면 다른 쪽 오프셋 변수도 같은 BP에서 동기화. **PC만 보고 "고정 OK" 판정 금지 — fixed 스택 간격은 모바일 BP에서 별도 확인.**

**(C) 모바일 드로어 2버그 (header.css)** — ① **X(닫힘) 아이콘 안 보임**: 드로어(`.nk-drawer` z-index 950)가 헤더(`#header` z-index 900)를 덮어, 햄버거가 X 로 토글돼도(`aria-expanded=true` → `.nk-hd__burger-close` inline-block) 드로어 배경에 가려짐. ✅ `body#nk-skin14.nk-drawer-open #header { z-index: 960; }`(드로어 위로 헤더 올림 — 드로어 inner padding-top 이 헤더 높이만큼 비워둬 겹침 없음). 검증: elementFromPoint=X버튼(가림 없음), 클릭 시 닫힘. ② **하단 선 2개 중복**: 메뉴 마지막 항목 `border-bottom` + 유틸영역 `border-top` 이 28px 간격으로 2줄. ✅ `.nk-drawer__nav .nk-gnb__item:last-child { border-bottom: 0; }` → 구분선 1개로 정리. **교훈: 풀스크린 드로어가 헤더를 덮으면 햄버거=X 토글 패턴은 무용 — 드로어 열림 시 헤더 z-index 를 드로어보다 높여야 X 가 산다.** ③ **드로어 열려도 탑배너 유지**: 헤더만 올리면 탑배너(`.nk-topbnr` z901)는 여전히 드로어(950)에 가려 사라짐 → `body.nk-drawer-open .nk-topbnr { z-index:960 }` 추가(드로어 inner padding-top 에 띠 높이 이미 포함, 겹침 없음). ④ **버거 버튼 작게 보임**: `.nk-hd__burger` 에 크기 규칙이 없어 아이콘이 본문 상속(≈14px) → `.nk-hd__burger{width:40px;height:40px;display:inline-flex}` + `.nk-hd__burger i{font-size:26px}`(다른 헤더 아이콘과 동일 스케일). 검증 PASS(탑배너 elementFromPoint=띠 내부, 버거 40×40·26px). ⑤ **드로어 위로 좋아요(위시) 버튼 비침**: 상품 상세의 카페24 기본 위시 아이콘 `.ec-product-listwishicon`(부모 `.wish`)이 **기본 CSS z-index:997** 이라 드로어(950)를 뚫고 노출됨(메인 카드는 `@media ≤1024 .nk-prd__actions{display:none}` 이라 무증상, 상세에서만 발현). z-index 상향 경쟁은 X·탑배너(960)까지 깨지는 캐스케이드라 위험 → **드로어 열림 동안 위시/액션을 가리는 방식**: `body.nk-drawer-open .nk-prd__actions, .icon__box, .wish, .ec-product-listwishicon { visibility:hidden }`(닫으면 자동 복귀). 검증 PASS(상세 모바일: 드로어 열림 시 위시 자리 elementFromPoint=.nk-drawer__inner=가려짐, 닫으면 visible 복귀). **교훈: 풀스크린 드로어 위로 새는 요소는 대개 기본 CSS 의 고(高) z-index(여기선 997) — 드로어를 더 올리기보다 경쟁 요소를 드로어 열림 상태에서 숨기는 게 안전(헤더 X·탑배너 z 캐스케이드 안 깨짐).**

**(D) 전수 QA 6차 — 드로어 z-누수 색출 + 카페24 기본 모바일 요소 정리 (2026-06-04)** — ★ **드로어 위 비침 전수 색출법**: 드로어 열린 상태에서 JS 로 `document.querySelectorAll('body *')` 중 `position!=='static' && zIndex>=950 && 화면에 보임` 인 요소를 전부 열거 → 헤더(960)·탑배너(960)·드로어 외에 뜨면 버그(하나씩 찾지 말고 한 번에 색출). ① **상세 하단 주문바 `#orderFixArea`(기본 z990)** 드로어 위로 비침 → `body.nk-drawer-open #orderFixArea{visibility:hidden}`(위시 z997 과 동일 부류, 동일 처방). ② **카페24 기본 모바일 하단 탭바 `.bottom-nav`(z901, 메뉴/검색/홈/장바구니/마이)** — 커스텀 헤더+드로어와 기능 중복 + 검정 라인 톤 이질 + 주문바와 세로겹침 → `#nk-skin14 .bottom-nav{display:none!important}`(모바일 전용 요소라 PC 무영향). ③ **우측 퀵메뉴 `#right_quick`(기본 bottom:30/right:50)** 모바일에서 본문 폼 버튼 우측 가림 → `@media ≤1024 #right_quick{bottom:14px;right:12px}` 우하단 모서리로 위치보정(탭바 숨겨 모서리 공간 확보). 검증 PASS(주문바 드로어 열림 hidden·닫힘 복귀 / 탭바 전 페이지 none·상세 주문바는 유지 / 퀵메뉴 우하단). **잔여(경미)**: `#right_quick` 스택 높이 168px 라 짧은 폼 페이지(아이디찾기 등)에선 확인버튼 우측 모서리와 ~22px 세로겹침 잔존(텍스트·핵심 터치영역은 비가림). 완전제거 원하면 모바일에서 퀵메뉴 버튼 수 축소 필요(디자인 결정). **나머지(홈·목록·상세·장바구니·회원4단계·찾기·게시판·마이 × PC/모바일): 오버플로·미치환변수·골드·흰박스·콘솔에러·드로어·sticky·폼컨트롤·스택 gap 전부 PASS.**

**(E) 신상품 캐러셀 제목 가운데 정렬돼 보임 (specificity tie 함정)** — prdArea1(신상품) head 는 `.nk-prdslide__head`(flex space-between, 제목그룹 좌 + View All 우)라 좌측정렬이어야 하나, custom.css `#nk-skin14 .nk-sec__head{text-align:center}` 와 prdArea1.css `#nk-skin14 .nk-prdslide__head{text-align:left}` 가 **specificity 동일(id 1+class 1)** → 번들 로드순서로 center 가 이김. 제목그룹이 shrink-wrap 되며 eyebrow("What's New")보다 짧은 "신상품"이 가운데로 놓여 가운데정렬처럼 보임. ✅ `#nk-skin14 .nk-sec__head.nk-prdslide__head{text-align:left}`(두 클래스 동시 = id1+class2, 항상 우선) 추가 → eyebrow·제목 좌측 확정. 검증: title/eyebrow align=left, x=15. **참고**: prdArea2(스테디셀러)는 `.nk-sec__head`만 가진 그리드 섹션(가운데 정렬 + View More 하단중앙)이라 **가운데 정렬이 의도된 정상**. **교훈: 같은 요소에 두 컴포넌트 클래스(.nk-sec__head + .nk-prdslide__head)가 붙고 각각 다른 파일에서 같은 속성을 동일 specificity 로 지정하면 로드순서 의존 → 이기려면 두 클래스 동시 선택자로 specificity 를 올린다.**

---
> ★ **이 모든 규칙의 배포용 통합본 = `/Users/nookitokki/dev/web/cafe24/CAFE24-SMARTDESIGN-AGENT.md`** (그 자체로 카페24 SmartDesign 자동화 에이전트 시스템 프롬프트). 새 작업/새 환경에서는 그 문서를 단일 소스로 사용. 본 WORK-GUIDE 는 skin10~14 작업 상세 로그.
