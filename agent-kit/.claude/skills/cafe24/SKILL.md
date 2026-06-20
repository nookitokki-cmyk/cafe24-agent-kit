---
name: cafe24-smartdesign
description: 카페24 스마트디자인(HTML 방식) + 스마트디자인Easy(비주얼 에디터) 양쪽 개발 가이드. 변수/모듈/지시어 문법, IDIO→NK 템플릿 구조, EZ 속성 시스템, 구버전 스킨에 신버전 스타일 차용법, SFTP 배포 포함. Use when: 카페24 스킨 HTML/CSS/JS 편집, 모듈 커스터마이징, 스마트디자인Easy 블록 편집, SFTP 배포 작업.
---

# 카페24 스마트디자인 개발 가이드

> **출처**: 이 스킬은 실제 프로젝트 코드 분석(reference-case 클라이언트) + 공식 문서(sdsupport.cafe24.com) 기반.
> 직접 사용해보며 틀린 내용을 발견하면 즉시 수정할 것.

---

## 0. 두 시스템 비교 (작업 전 먼저 확인)

> **출처 등급:** ✅ Admin API `editor_type` · ⚠️ 아래 표 중 SFTP/경로/호환 — [`OFFICIAL-AUDIT.md`](../../../brain/docs/OFFICIAL-AUDIT.md) · `VERIFICATION-EVIDENCE.md`

| 구분 | 스마트디자인 (HTML, **H**) | 스마트디자인Easy (**E**) |
|-----|------------------------|-----------------|
| API 구분 | `editor_type` **H** ✅ | `editor_type` **E** ✅ |
| 편집 방식 | HTML/CSS/JS + SFTP ⚠️ | 비주얼 블록 + 관리자 편집 ⚠️ |
| SFTP (demo000 실측 2026-06-19) | `/{skin_code}` 접근 OK ⚠️ | **동일** — E 스킨도 `/skin14`, `/base` list OK ⚠️. 「Easy=SFTP 불가」는 **과장** |
| 스킨 경로 (키트 주장) | `/skin1/`, `/mobile/` 등 ⚠️ | `/sde_design/base/` ⚠️ — **해당 몰 SFTP 루트에 sde_design 없음** |
| 전용 속성 | `module="..."` ✅ basic | `data-ez-*` ⚠️ (base layout에 실측 존재) |
| 상호 호환 | ⚠️ 공식 동일 문장 없음 | ⚠️ |

**작업 전 필수:** `cafe24_list_themes` → `editor_type` 확인. **E라도 SFTP 폴더가 있을 수 있음** — EZ 제거·HTML 전환은 사용자 명시 시만.

### 실제 스킨 3개 비교 (reference-case 프로젝트 기준)

| 항목 | skin1 (IDIO 템플릿) | skin2 ★ 작업 베이스 | skin5 (경량 참고) |
|------|-------------------|-------------------|-----------------|
| 파일 수 | 777 | 612 | 458 |
| 커스텀 레이어 | `_idio/` | `layout/basic/header·footer.html` | `_nk/` |
| EZ 속성 위치 | `ez/ez-module.html` | `layout/basic/header·footer.html` 내부 | 없음 (레거시) |
| skin1과 교집합 | — | 584개 (34.25% 동일) | 450개 (14% 동일) |
| 고유 파일 수 | 188개 | 26개 | 10개 |

**결론**: skin2가 skin1과 가장 유사한 구조. skin2 위에 `_nk/` 레이어를 얹으면 skin1과 동일한 아키텍처가 된다.

### IDIO/NK 템플릿과 EZ 시스템 관계 (자주 혼동)

IDIO/NK 구매 템플릿은 **스마트디자인(HTML 방식)** 기반이며 SmartDesignEasy가 아님.
단, 각 스킨마다 EZ 속성이 포함된 위치가 다름.

```
skin1/
├── layout.html, index.html       → data-ez-* 없음 (표준 SmartDesign)
├── _idio/ 또는 _nk/              → 커스텀 에셋 — 여기서만 작업
└── ez/ez-module.html             → data-ez-* 있음 (관리자 편집 연동 전용)

skin2/ ← 현재 작업 베이스
├── layout/basic/layout.html      → data-ez-* 없음
├── layout/basic/header.html      → data-ez-* 있음 (레이아웃 선택 6종)
├── layout/basic/footer.html      → data-ez-* 있음 (레이아웃 선택 3종)
├── ez/ez-settings.json           → EZ 설정 (절대 수정 금지)
└── _nk/                          → 커스텀 에셋 추가 위치
```

**skin2 작업 원칙**: `layout/basic/header.html`과 `footer.html`에 있는 `data-ez-*`, `<ez-prop>`, `<ez-var>`, `<ez-item>` 속성을 **절대 건드리지 않음**. 이 파일들에 CSS 클래스만 추가하거나, `_nk/inc/header.html`로 오버라이드하는 방식 사용.

**올바른 개발 방식**: `_nk/` 폴더에 커스텀 파일 추가, EZ 속성 건드리지 않음, CSS/JS만 오버라이드.

---

## 1. 공통 — 지시어 (두 시스템 동일)

카페24 엔진이 빌드 시 실제 태그로 치환하는 HTML 주석 형태 지시어.

```html
<!--@layout(/layout/basic/layout.html)-->  <!-- 파일 첫 줄: 이 페이지의 레이아웃 -->
<!--@contents-->                           <!-- layout.html 안: 페이지 본문 삽입 위치 -->
<!--@import(/_nk/inc/header.html)-->       <!-- 외부 HTML 인클루드 -->
<!--@css(/_nk/css/color.css)-->            <!-- CSS 로드 → <link> 태그로 치환 -->
<!--@js(/_nk/js/nk.js)-->                  <!-- JS 로드 → <script> 태그로 치환 -->
```

**주의**: LSP/linter가 이 경로를 파일 참조로 인식 못함. 경로 오타 = 육안 검증 필수.

---

## 2. 공통 — 변수 문법

### 기본 출력

```html
{$mall_name}           <!-- 쇼핑몰 이름 -->
{$product_name}        <!-- 상품명 -->
{$product_sale_price}  <!-- 판매가 -->
{$image_medium}        <!-- 상품 목록 이미지 URL -->
{$param}               <!-- 상품 상세 링크 파라미터 (?product_no=...) -->
```

변수는 해당 모듈 scope 안에서만 동작. 모듈 밖에서 쓰면 빈 값 출력됨.

### 모디파이어 (필터)

```html
{$변수명|모디파이어}
{$변수명|모디파이어:옵션}
```

| 모디파이어 | 용도 | 예시 |
|-----------|------|------|
| `\|display` | false면 `display:none` 인라인 적용 | `class="{$use_sale\|display}"` |
| `\|cut:N,...` | N글자 자르기 | `{$product_name\|cut:20,...}` |
| `\|numberformat` | 천 단위 콤마 | `{$product_price\|numberformat}` |
| `\|date:형식` | 날짜 포맷 | `{$write_date\|date:Y-m-d}` |
| `\|nl2br` | 줄바꿈 → `<br>` | `{$content\|nl2br}` |
| `\|striptag` | HTML 태그 제거 | `{$content\|striptag}` |
| `\|replace:찾을것,바꿀것` | 문자열 치환 | `{$icon\|replace:공지,📌}` |
| `\|cover:앞,뒤` | 값 있을 때만 앞뒤 감싸기 | `{$subject\|cover:(,)}` |
| `\|imgconv:경로` | 값 있을 때 `<img>` 태그로 치환 | `{$new_icon\|imgconv:'/img/new.gif'}` |
| `\|strconv:텍스트` | 값 있을 때 지정 텍스트로 치환 | `{$new_icon\|strconv:NEW}` |
| `\|timetodate:형식` | 타임스탬프 → 날짜 변환 | `{$write_date\|timetodate:Y-m-d}` |
| `\|upper` / `\|lower` | 영문 대소문자 변환 | |

---

## 3. 공통 — 모듈 시스템

### 기본 사용법

```html
<div module="모듈명">
  <!--
  $설정변수 = 값
  $설정변수2 = 값2
  -->
  {$변수명}
</div>
```

**설정 변수 규칙**: 각 변수 반드시 별도 줄에 작성. 한 줄에 몰아쓰면 인식 실패.

```html
<!-- ✅ 올바름 -->
<div module="product_listnormal">
  <!--
  $count = 12
  $basket_result = /product/add_basket.html
  -->
</div>

<!-- ❌ 잘못됨 — 인식 안 됨 -->
<div module="product_listnormal">
  <!-- $count = 12 $basket_result = /product/add_basket.html -->
</div>
```

### 반복 렌더링

`foreach` 태그 없음. 모듈 안의 HTML(li 등)을 `$count`만큼 자동 반복.

```html
<ul module="product_listnormal">
  <!--
  $count = 12
  -->
  <!-- 이 li 1개 = 상품 1개 → 12번 반복됨 -->
  <li id="anchorBoxId_{$product_no}">
    <a href="/product/detail.html{$param}">
      <img src="{$image_medium}" alt="{$product_name}">
    </a>
    <p class="nk-product-name">{$product_name}</p>
    <p class="nk-product-price">{$product_sale_price}</p>
  </li>
</ul>
```

`$only_html = yes` → DB 무시, HTML에 작성된 li 개수 그대로.

### 주요 모듈 목록

**레이아웃**

| 모듈명 | 용도 |
|-------|------|
| `Layout_LogoTop` | 로고 |
| `Layout_category` | 카테고리 메뉴 |
| `Layout_statelogoff` | 비로그인 전용 영역 |
| `Layout_statelogon` | 로그인 전용 영역 |
| `Layout_SearchHeader` | 검색창 |
| `Layout_shoppingInfo` | 적립금/장바구니/관심상품 |
| `Layout_orderBasketcount` | 장바구니 개수 |

**상품**

| 모듈명 | 용도 |
|-------|------|
| `product_listnormal` | 일반 상품 목록 |
| `product_listnew` | 신상품 목록 |
| `product_listrecommend` | 추천상품 목록 |
| `product_listmain_1~5` | 메인 상품 목록 1~5번 |
| `product_headcategory` | 카테고리 브레드크럼 |
| `product_normalpaging` | 상품 목록 페이징 |

**상품 목록 주요 변수**

| 변수 | 용도 |
|-----|------|
| `{$product_no}` | 상품 고유 번호 |
| `{$param}` | 상세 링크 파라미터 |
| `{$product_name}` | 상품명 |
| `{$product_price}` | 정가 |
| `{$product_sale_price}` | 판매가 |
| `{$image_medium}` | 목록 이미지 |
| `{$image_big}` | 상세 이미지 |
| `{$soldout_icon}` | 품절 아이콘 |
| `{$new_icon}` | 신상품 아이콘 |
| `{$basket_icon}` | 장바구니 버튼 |

**게시판** (번호는 게시판마다 다름, 예: 1002)

| 모듈명 | 용도 |
|-------|------|
| `Board_ListPackage_번호` | 게시판 전체 패키지 |
| `board_title_번호` | 게시판 타이틀 |
| `board_list_번호` | 일반 글 목록 |
| `board_notice_번호` | 공지사항 목록 |
| `board_paging_번호` | 페이징 |
| `board_search_번호` | 검색 폼 |

### xans- 자동 클래스

모듈에 카페24가 자동으로 CSS 클래스 부여: `xans-` + 모듈명 소문자.

```
module="product_listnormal"  →  .xans-product-listnormal
module="Layout_category"     →  .xans-layout-category
module="Layout_statelogon"   →  .xans-layout-statelogon
```

커스텀 스타일 작성 시 xans 클래스 기반으로 덮어쓰거나, 모듈에 커스텀 클래스 추가.

---

## 4. 스마트디자인 (HTML 방식) 전용

### 폴더 구조

```
/ (SFTP 루트)                        ← 실제 서버 확인 완료
├── base/            ← 시스템 기본 (수정 불가, fallback용)
├── skin1/           ← PC 스킨 1 (운영)
│   ├── layout/basic/
│   │   ├── layout.html       ← 전체 레이아웃 (헤더+본문+푸터)
│   │   ├── layout_wide.html  ← 와이드 레이아웃 (상품상세 등)
│   │   ├── main.html         ← 메인 전용 레이아웃
│   │   └── main_supply.html  ← 공급사 전용 메인
│   ├── product/ / board/ / member/ / myshop/ / order/
│   ├── _idio/ 또는 _nk/   ← 커스텀 에셋 (CSS/JS/inc)
│   │   ├── css/
│   │   ├── js/               ← 핵심 JS: idio.js 또는 nk.js
│   │   └── inc/              ← 공통 HTML 조각 (header, footer 등)
│   ├── css/module/           ← 카페24 모듈 자동 주입 CSS (수정 불가)
│   └── setup.js              ← NK['키'] 설정 제어 파일 (루트에 위치)
├── skin2/  /  mobile/  /  mobile2/  /  web/
```

파일이 skin1에 없으면 base에서 자동 fallback. 커스텀 파일만 skin1에 배치하면 됨.

### skin2 고유 파일 목록 (EZ 속성 포함 — 수정 주의)

skin2에만 있는 고유 파일 26개 중 핵심:

| 파일 | EZ 속성 여부 | 처리 방법 |
|------|------------|----------|
| `layout/basic/header.html` | `data-ez-module`, `data-ez-layout`, `<ez-prop>`, `<ez-var>` 대거 포함 | CSS로 스타일 오버라이드 또는 `_nk/inc/header.html`로 교체 (EZ 속성 유지) |
| `layout/basic/footer.html` | `data-ez-group`, `data-ez-role`, `data-ez-item` 포함 | 동일 |
| `layout/basic/navigation.html` | EZ 속성 포함 가능 | 구조 확인 후 CSS만 수정 |
| `ez/ez-settings.json` | EZ 시스템 설정 | **절대 수정 금지** |

**skin2 header.html 레이아웃 옵션** (data-ez-layout 값):
- layout1: 2단 중앙형 (아이콘 하단)
- layout2: 2단 좌측형
- layout3: 1단 기본형
- layout4: 2단 혼합형
- layout5: 2단 중앙형 (아이콘 상단)
- layout6: 2단 슬라이딩 메뉴 노출형

**skin2 footer.html 레이아웃 옵션**:
- layout1: 기본형
- layout2: 좌우반전형
- layout3: 중앙형

### SFTP 연결 주의사항

- 서버: SSH 기반 SFTP (SFTPGo 2.4.4), paramiko 사용
- **연속 접속 시 rate-limit 걸림** — 접속 후 최소 30초 간격 유지
- 한 번 접속해서 필요한 작업을 모두 처리한 후 연결 종료하는 방식 권장
- 복수 경로 확인이 필요하면 하나의 transport 안에서 처리

### IDIO → NK 리네이밍 (이 프로젝트의 관례)

| 구버전 (IDIO) | 신버전 (NK) |
|--------------|------------|
| `/_idio/` | `/_nk/` |
| `--idio-theme-color` | `--nk-theme-color` |
| `IDIO['key']` (JS) | `NK['key']` |
| `idio.js` | `nk.js` |

리네이밍은 에셋 명칭 변경일 뿐, 카페24 문법 자체는 동일함.

**신버전(_nk)에서 추가된 CSS 파일**

| 파일 | 내용 |
|------|------|
| `_nk/css/color.css` | 확장 색상 토큰 (Figma DS, 30+ 토큰) |
| `_nk/css/motion.css` | 애니메이션 토큰 |
| `_nk/css/zindex.css` | z-index 관리 |
| `_nk/css/layout.css` | 레이아웃 그리드/spacing |
| `_nk/css/font.css` | Pretendard + Phosphor Icons |

### JS 제어 시스템 (setup.js)

```javascript
// 구버전 (IDIO)
IDIO['class-popup-idio'] = 'on';          // 팝업 표시
IDIO['text-cstime-1'] = '평일 09:00~18:00'; // 고객센터 시간 텍스트
IDIO['href-ic-talk'] = 'https://...';     // 카카오톡 링크

// 신버전 (NK) — 동일 패턴, 변수명만 교체
NK['class-popup-nk'] = 'on';
NK['text-cstime-1'] = '평일 09:00~18:00';
```

### SFTP 배포

```bash
# 원격 폴더 보기
python3 sftp_util.py ls /skin1 2

# 파일 업로드
python3 sftp_util.py upload ./deploy/_nk /skin1/_nk

# 파일 다운로드 (수정 전 백업 필수)
python3 sftp_util.py download /skin1/_nk/css/color.css ./backup/color.css
```

---

## 5. 스마트디자인Easy 전용

### 폴더 구조

```
/sde_design/
├── base/          ← PC 스킨
│   ├── layout/basic/layout.html
│   ├── product/ / board/ / member/ ...
│   ├── css/ / js/ / img/
│   └── config/settings_data.json
└── mobile/        ← 모바일 스킨
```

Easy는 SFTP 직접 접근 불가. 관리자 패널 코드 편집 탭에서만 수정.

### EZ 시스템 — 관리자 디자인 편집 연동

Easy 스킨 전용. 관리자 패널 "디자인 편집"과 연동되는 속성.

```html
<div data-ez-theme="header">
  <div data-ez-module="logo" data-ez-group="branding">
    ...
  </div>
</div>

<!-- ez-prop/ez-var: 관리자 패널에서 바꿀 수 있는 옵션/변수 -->
<section ez-prop="backgroundColor" ez-var="mainBg">
  ...
</section>
```

| EZ 속성 | 역할 |
|---------|------|
| `data-ez-theme` | 테마 레벨 식별 |
| `data-ez-module` | 모듈 식별자 |
| `data-ez-group` | 그룹핑 |
| `ez-prop` | 관리자 패널 옵션 파라미터 |
| `ez-var` | 관리자 패널 변수 파라미터 |

**절대 금지**: `data-ez-*`, `ez-prop`, `ez-var` 임의 제거. 제거 시 관리자 패널 편집 불가.

### settings_data.json

```json
{
  "jquery": {
    "use_latest_jquery": true
  }
}
```

---

## 6. 구버전 스킨에 신버전 스타일 차용하기

카페24 모듈 문법은 구/신버전 동일. 차이는 에셋(CSS/JS)만.

### 안전한 방법

```html
<!-- 1. 신규 CSS 파일 추가 (common.html 또는 layout.html에) -->
<!--@css(/_nk/css/color.css)-->
<!--@css(/_nk/css/motion.css)-->

<!-- 2. 외부 라이브러리 교체 -->
<!-- Pretendard, Phosphor Icons, AOS, Swiper 등 -->

<!-- 3. 커스텀 클래스 추가 (모듈 기능은 유지) -->
<div module="product_listnormal" class="nk-product-grid">
```

### 권장 마이그레이션 순서

1. `color.css` 교체 (색상 토큰만 먼저)
2. `font.css` 교체 (Pretendard + Phosphor)
3. `motion.css`, `zindex.css` 추가
4. `setup.js` 변수명 교체 (`IDIO` → `NK`)
5. HTML 클래스명 `idio-*` → `nk-*` 일괄 교체

---

## 7. 렌더링 흐름

```
브라우저 요청 /product/list.html
  ↓ 첫 줄 <!--@layout(/layout/basic/layout.html)-->
layout.html 래핑
  ↓ <!--@import(/_nk/inc/header.html)-->
  ↓ <!--@contents-->  ← list.html 본문 삽입
  ↓ <!--@import(/_nk/inc/footer.html)-->
카페24 엔진 서버사이드 처리: {$변수} 치환 + module 데이터 바인딩
  ↓
완성된 HTML → 브라우저 (변수 코드 노출 없음)
```

JS 동적 생성 영역은 카페24 치환 대상 아님.

---

## 8. 함정 & 실수 방지

### `<section>` 태그 120px margin 함정

`_nk/css/common.css`에 전역 규칙:
```css
section { margin-top: 120px !important; margin-bottom: 120px !important; }
```

히어로/배너 등 풀블리드 섹션에서 반드시 오버라이드:
```css
.nk-hero { margin-top: 0 !important; margin-bottom: 0 !important; }
```

### 풀블리드 이미지 섹션 — 텍스트+이미지 2단 그리드 패턴

이미지가 섹션 경계까지 여백 없이 꽉 차야 할 때 (brand-intro 등), inner wrapper 없이 section을 직접 grid로 만들고 왼쪽 패딩만 container 기준으로 계산하는 방식:

```html
<section class="nk-brand-intro">
  <div class="nk-brand-intro__text">...</div>
  <div class="nk-brand-intro__image">
    <img src="..." alt="...">
  </div>
</section>
```

```css
.nk-brand-intro {
  display: grid;
  grid-template-columns: 1fr 1fr;
  min-height: 600px;
  /* section 전역 margin 오버라이드 */
  margin: 0 !important;
}

/* 텍스트 영역: container 중앙 기준으로 왼쪽 padding 계산 */
.nk-brand-intro__text {
  padding: 80px var(--nk-padding-x) 80px
    calc((100vw - var(--nk-container-max)) / 2 + var(--nk-padding-x));
}

/* 이미지 영역: 섹션 오른쪽 끝까지 풀블리드 */
.nk-brand-intro__image {
  width: 100%;
  height: 100%;
  overflow: hidden;
}

.nk-brand-intro__image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
```

핵심: `inner` wrapper를 쓰지 않고 section에 직접 grid → 이미지가 뷰포트 끝까지 확장됨.
왼쪽 텍스트 padding은 `calc((100vw - max-width) / 2 + padding-x)`로 container 안쪽에 맞춤.

### `#category` 모듈 자동 margin

`/css/module/layout/번호/category.css`가 `margin: 0 0 30px` 자동 주입.
헤더 메뉴에 사용 시: `#category { margin: 0 !important; }`

### 카페24 모듈 CSS 우선순위

`/css/module/layout/<번호>/` CSS는 수정 불가, 우선순위 높음. 충돌 시 selector specificity 높여서 오버라이드.

### skin2 header/footer EZ 속성 삭제 금지

skin2의 `layout/basic/header.html`, `footer.html`에는 `data-ez-*`, `<ez-prop>`, `<ez-var>`, `<ez-item>` 속성이 대거 포함되어 있음. 이 속성들을 제거하면:
- 카페24 관리자 "레이아웃 편집" 패널에서 헤더/푸터 레이아웃 선택 불가
- EZ 초기화 실패로 헤더가 렌더링 깨질 수 있음

**올바른 수정 방법:**
```html
<!-- ❌ 잘못 — EZ 속성 제거 -->
<header id="header">...</header>

<!-- ✅ 올바름 — EZ 속성 유지하면서 클래스만 추가 -->
<header id="header" class="layout1 nk-header" data-ez-layout="layout1" data-ez="contents-...">
  ...
</header>
```

### 변수가 그대로 노출될 때

브라우저 소스에 `{$변수}`가 그대로 보이면 → 모듈 scope 밖에서 변수 사용 중. 모듈 안으로 이동.

### CSS/JS 중복 로드 방지

같은 파일을 여러 템플릿에서 각각 `<!--@css-->` 로드하면 중복 적용됨. 공통 CSS/JS는 `common.html` 한 곳에서만 로드하고 모든 페이지가 `<!--@import(/_nk/inc/common.html)-->` 으로 불러오는 방식 권장.

### IDE 자동 포맷팅 주의

VSCode 등에서 HTML 파일을 저장할 때 auto-format이 들여쓰기/줄바꿈을 바꾸면 카페24 엔진이 파싱 실패하는 경우 있음. `<!--@-->` 지시어 주변은 포맷터가 건드리지 않도록 설정 필요.

### 모듈 JS 비동기 타이밍

카페24 모듈은 비동기로 DOM에 삽입됨. 모듈 안의 요소를 JS로 제어할 때 `document.ready` 이후에도 존재하지 않을 수 있음.

```javascript
// 방어적 접근 패턴
const src = element?.getAttribute("ec-data-src") || 
            element?.getAttribute("data-src") ||
            element?.currentSrc || "";
```

### 헤더 커스텀 시 반드시 포함해야 할 오버라이드

카페24는 헤더를 렌더링할 때 `/css/module/layout/` 하위의 CSS 파일들을 자동으로 주입한다. 이 파일들은 수정 불가이고 우선순위가 높다. 커스텀 헤더를 만들 때 이 오버라이드를 **처음부터 포함하지 않으면** 예상과 다른 레이아웃이 나온다. 문제가 생긴 후 고치는 게 아니라, 헤더 CSS 파일 작성 시 처음부터 포함시켜야 한다.

**`Layout_LogoTop` 모듈**: `logotop.css`가 자동 주입되어 로고 컨테이너에 `margin: auto`, `text-align: center`, 고정 width 등을 강제 적용함. 이 오버라이드 없이 flex 헤더를 만들면 로고가 중앙으로 밀리거나 컨테이너 너비를 과도하게 점유함.

**헤더 CSS에 처음부터 포함할 것**:
```css
div.xans-layout-logotop.nk-header__logo {
  padding: 0 !important;
  width: auto !important;
  min-width: 0 !important;
  max-width: none !important;
  margin: 0 auto 0 0 !important;  /* 로고 좌측 고정 + 우측 공간 밀어내기 */
  text-align: left !important;
}

@media (min-width: 1025px) {
  div.xans-layout-logotop.nk-header__logo {
    margin: 0 auto 0 0 !important;
    text-align: left !important;
  }
}

@media (max-width: 1024px) {
  div.xans-layout-logotop.nk-header__logo {
    text-align: left !important;
  }
}
```

`margin: 0 auto 0 0` = top:0 / right:auto / bottom:0 / left:0. 이것이 핵심 — auto right margin이 로고를 좌측에 고정시키고 나머지 요소를 우측으로 밀어냄.

### GNB 절대 중앙 정렬

헤더 3단 구조(로고 | GNB | util)에서 GNB를 중앙에 배치할 때 `flex: 1` 방식을 쓰면 로고/util 너비가 달라질 때마다 GNB가 시각적으로 치우친다. 처음 구조를 짤 때부터 절대 중앙 방식을 쓸 것.

```css
/* 헤더 inner에 position: relative 필수 */
.nk-header__inner { position: relative; }

/* GNB는 absolute로 헤더 너비 기준 정중앙 */
.nk-gnb {
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
}
```

로고나 util 너비가 달라져도 GNB는 항상 헤더의 정확한 중앙에 위치함.

### 드로어 내 `{$mall_name}` 미렌더링

카페24 변수 `{$변수명}`은 `module=""` 속성이 있는 요소 **안에서만** 치환됨. 드로어 헤더 브랜드명 등 module 바깥에 `{$mall_name}`을 쓰면 브라우저에 `{$mall_name}` 텍스트가 그대로 노출됨.

**해결책**: module 밖에서는 반드시 하드코딩
```html
<!-- ❌ 안 됨 — module 밖 -->
<span class="nk-drawer__brand">{$mall_name}</span>

<!-- ✅ 올바름 — 하드코딩 -->
<span class="nk-drawer__brand">내쇼핑몰</span>
```

### SFTP IP 단위 차단 — 수동 업로드 우회 (오직 IP 차단 시 최후 수단)

> ❗ **범위 주의 — 파트너센터와 혼동 금지.** 이 항목은 *자동 접속이 IP로 막혔을 때만* 쓰는 최후 우회다. **"파트너센터 = 웹 FTP"** 는 차단된 게 아니라 *다른 프로토콜*이며, `sftp_{몰ID}.json` 에 `"protocol":"ftp"` 만 넣으면 MCP `cafe24_sftp_upload` 가 **Python(ftplib)으로 자동 업로드**한다. 파트너 작업을 "SFTP 차단이라 수동 업로드"라고 안내하지 말 것.

카페24 SFTP는 paramiko, OpenSSH 등 자동화 라이브러리 접속을 IP 기반으로 차단하는 경우 있음. 증상: `Connection reset by peer`, `SSH handshake failed` 등.

**해결책**: 위 증상이 **실제로 떴을 때만** 카페24 관리자 패널 → 파일관리에서 직접 업로드. 평상시 업로드는 `cafe24_sftp_upload` 자동 경로(FTP·SFTP 공용)가 기본이다.

### 모바일 드로어 — 풀스크린 fade-in 패턴

좌측 슬라이드 드로어보다 풀스크린 fade-in이 UX에서 더 자연스러울 때의 CSS 패턴:

```css
/* 드로어 — 풀스크린 fade-in */
.nk-drawer {
  position: fixed;
  inset: 0;           /* top/right/bottom/left: 0 전체 차지 */
  width: 100%;
  height: 100%;
  background: var(--nk-bg-white);
  z-index: calc(var(--nk-z-header) + 10);  /* 헤더 위 */
  opacity: 0;
  visibility: hidden;
  pointer-events: none;
  transition: opacity 0.25s ease, visibility 0.25s ease;
}

.nk-drawer.is-open {
  opacity: 1;
  visibility: visible;
  pointer-events: auto;
}

/* 드로어 열릴 때 배경 스크롤 잠금 */
body.nk-drawer-open { overflow: hidden; }
```

햄버거 ↔ X 아이콘 토글은 CSS만으로 처리:
```css
.nk-hamburger .nk-hamburger__icon--close { display: none; }
.nk-hamburger[aria-expanded="true"] .nk-hamburger__icon--open  { display: none; }
.nk-hamburger[aria-expanded="true"] .nk-hamburger__icon--close { display: block; }
```

JS에서 `aria-expanded` 속성을 true/false로 토글하면 됨.

### product_listmain_N — 올바른 구조 패턴 (skin1 실증)

module을 ul/li에 직접 붙이거나 anchorBoxId 안에 커스텀 콘텐츠를 직접 넣으면 1개만 출력되거나 콘텐츠가 2배 중복 렌더링됨.

**올바른 구조**:
```html
<div module="product_listmain_1" class="ec-base-product">
  <!--
    $count = 12
    $basket_result = /product/add_basket.html
    $moreview = no
    $cache = no
  -->
  <ul class="nk-best-products__grid">
    <li class="nk-product-card" id="anchorBoxId_{$product_no}">
      <!--@import(/_nk/inc/prd.html)-->
    </li>
    <li class="nk-product-card" id="anchorBoxId_{$product_no}">
      <!--@import(/_nk/inc/prd.html)-->
    </li>
  </ul>
</div>
```

> ⚠️ **anchorBoxId 요소는 반드시 2개 이상** — 1개만 있으면 상품이 1개만 출력됨.  
> 카페24 엔진이 반복 패턴을 인식하려면 동일한 `id="anchorBoxId_{$product_no}"` 블록이 최소 2개 나란히 있어야 한다. (skin1 `prdArea1.html` 실증)

**prd.html 구조**:
```html
<a href="{$link_product_detail}" class="nk-prd-link"></a>
<div class="nk-product-card__thumb">
  <img src="{$image_medium}" alt="{$product_name}">
</div>
<div class="nk-product-card__info">
  <p class="nk-product-card__name">{$product_name}</p>
  <span class="nk-product-card__sale-price">{$product_sale_price}</span>
  <span class="nk-product-card__origin-price">{$product_price}</span>
</div>
```

핵심 규칙:
- `module`은 반드시 `<div class="ec-base-product">`에
- `anchorBoxId` 블록은 **2개 이상** 나란히 선언 (1개 → 상품 1개만 출력)
- `anchorBoxId` 내부에 커스텀 콘텐츠 직접 작성 금지 → 2배 중복 렌더링 발생
- 실제 콘텐츠는 `<!--@import-->` 로 별도 파일 분리
- 카드 링크는 CSS 오버레이 방식 (`position: absolute; inset: 0`)
- 이미지 변수: `{$image_medium}` (❌ `{$product_image}` 아님)
- 링크 변수: `{$link_product_detail}` (❌ `/product/detail.html{$param}` 아님)

---

## 9. 디버깅

```
크롬 시크릿(비로그인) vs 일반 크롬(로그인)
→ Layout_statelogoff / Layout_statelogon 상태 비교

Ctrl+U 브라우저 소스 보기
→ {$변수} 치환됐는지 확인
→ 치환 안 됐으면 모듈 scope 밖에서 사용 중

카페24 모듈 CSS 충돌
→ 브라우저 개발자도구 스타일 패널 → /css/module/... 파일 확인
```

---

## 10. 체크리스트

### 공통

- [ ] 스마트디자인(HTML)인지 스마트디자인Easy인지 확인
- [ ] `<!--@css/js/import-->` 경로 오타 육안 확인
- [ ] module 설정 변수 각 줄 분리 확인

### 스마트디자인 (HTML)

- [ ] SFTP 업로드 전 기존 파일 백업
- [ ] `<section>` 태그 사용 시 margin 0 오버라이드
- [ ] 비로그인/로그인 상태 양쪽 테스트
- [ ] 모바일(/mobile) 별도 대응 여부 확인

### 스마트디자인Easy

- [ ] `data-ez-*`, `ez-prop`, `ez-var` 속성 보존 확인
- [ ] 관리자 패널 디자인 편집 정상 동작 확인

---

## 11. 공식 레퍼런스

- 스마트디자인 서포트: `https://sdsupport.cafe24.com`
- 전체 모듈 목록: `https://sdsupport.cafe24.com/product/list.html?cate_no=61`
- 상품 모듈: `https://sdsupport.cafe24.com/module/product/list.html`
- 레이아웃 모듈: `https://sdsupport.cafe24.com/module/layout/index.html`

---

## 12. 상세 사전 (references/) — 필요할 때만 읽기

본문은 메인/목록 작업 위주. **상품 상세 / 장바구니 / 주문서 / 회원가입 / 게시판** 페이지를 작업할 때는
아래 사전 파일에서 정확한 모듈 ID·변수명을 찾아 쓸 것. (토큰 절약 위해 전체 로드 말고 필요한 항목만 검색)

- `references/modules.md` — 상품 상세·장바구니·주문서·회원·게시판 모듈 ID 전체
- `references/variables.md` — 상세/장바구니/주문서/회원/게시판 변수 전체 + `member_join` 폼 변수
- `references/modifiers.md` — 수정자 13종(`|cut`·`|numberformat`·`|display`·`|date` 등) + 조건/반복 제어 문법

> 출처: 본문은 reference-case 실프로젝트 분석 기반. references/ 사전 항목은 kimyoungwopo/cafe24-smart-design(MIT) + 공식문서에서 보강.
