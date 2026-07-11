# NK Esthe-style Easy Compatible Skin System 설계

## 목적

`cafe24-agent-kit`의 기본 검증 템플릿을 Esthe/IDIO식 작업 방식으로 재설계한다.

목표는 Esthe 원본 코드, 이미지, 문구, 브랜드 자산을 복제하는 것이 아니다. 목표는 Esthe가 제공하는 작업 방식, 즉 `inc` 기반 섹션 분리, 설정 파일 기반 on/off 제어, 전용 CSS/JS 레이어, SmartDesignEasy용 `data-ez-*` 메타데이터, `ez-prop`/`ez-var`/`ez-item` 레이아웃 옵션, 카페24 DOM 보정 adapter를 `NK` 네임스페이스와 누끼토끼 제작 규칙으로 재구현하는 것이다.

## 적용 범위

### 포함

- `clients/_verified-template/src`의 템플릿 구조를 Esthe-style 구조로 확장
- `_nk/inc` 섹션 조각 시스템 도입
- `_nk/css` 디자인 토큰, 공통 스타일, 섹션 스타일, Easy 호환 스타일 분리
- `_nk/js` 설정 적용, DOM 보정, 상품/리뷰/상세 페이지 보정 모듈 분리
- `setup.html` 기반 비개발자용 on/off 설정 파일 도입
- `ez/ez-module.html`에 SmartDesignEasy 호환 메타데이터 포함
- `data-ez-module`, `data-ez-layout`, `data-ez-role`, `data-ez-holder` 표준화
- `ez-prop`, `ez-var`, `ez-item` 기반 레이아웃 옵션 정의
- 검증 스크립트에서 `NK` 규칙, Easy 속성, 금지 자산 검사

### 제외

- Esthe/IDIO 원본 코드의 직접 복사
- Esthe 이미지, 문구, 브랜드명, 클래스명, CSS 변수명 복사
- `idio`, `_idio`, `IDIO`, `--idio-*` 네임스페이스 사용
- Font Awesome 사용
- Pretendard 외 폰트 임의 사용
- `font-style: italic` 또는 `font-style: oblique` 사용
- 카페24 기본 `css/module` 파일 대량 수정

## 핵심 원칙

1. **작업 방식은 Esthe처럼, 산출물은 NK로 만든다.**
   - Esthe의 `inc`/CSS/JS/setup/Easy 구조를 차용한다.
   - 원본 코드와 자산은 복붙하지 않는다.

2. **디자인 기준은 `nk-*` 클래스가 담당한다.**
   - 모든 커스텀 클래스는 `nk-` 접두사를 사용한다.
   - CSS와 JS는 `data-ez-*`에 의존하지 않는다.

3. **Easy 속성은 편집기 호환 메타데이터로만 사용한다.**
   - `data-ez-*`가 없어도 화면은 정상 작동해야 한다.
   - `data-ez-*`가 있으면 SmartDesignEasy 편집기가 영역을 인식할 수 있다.

4. **비개발자 수정 지점은 `setup.html`로 모은다.**
   - 상단 배너, 팝업, 메인 섹션, SNS, 카카오 링크, 유튜브 링크를 설정 파일에서 제어한다.

5. **카페24 기본 CSS는 직접 대량 수정하지 않는다.**
   - 기본 CSS 위에 `_nk/css` override layer를 얹는다.

## 목표 폴더 구조

```text
src/
├─ index.html
├─ root.html
├─ setup.html
├─ ez/
│  └─ ez-module.html
├─ _nk/
│  ├─ inc/
│  │  ├─ common.html
│  │  ├─ header.html
│  │  ├─ footer.html
│  │  ├─ top-banner.html
│  │  ├─ popup.html
│  │  ├─ main-hero.html
│  │  ├─ product-list.html
│  │  ├─ product-slide.html
│  │  ├─ category-tabs.html
│  │  ├─ image-gallery.html
│  │  ├─ video.html
│  │  ├─ map.html
│  │  ├─ review.html
│  │  └─ quick-menu.html
│  ├─ css/
│  │  ├─ nk-tokens.css
│  │  ├─ nk-reset.css
│  │  ├─ nk-common.css
│  │  ├─ nk-header.css
│  │  ├─ nk-footer.css
│  │  ├─ nk-main.css
│  │  ├─ nk-product.css
│  │  ├─ nk-review.css
│  │  ├─ nk-ez.css
│  │  ├─ nk-responsive.css
│  │  └─ nk-custom.css
│  ├─ js/
│  │  ├─ nk-config.js
│  │  ├─ nk-core.js
│  │  ├─ nk-header.js
│  │  ├─ nk-slider.js
│  │  ├─ nk-product.js
│  │  ├─ nk-review.js
│  │  ├─ nk-detail.js
│  │  └─ nk-ez-adapter.js
│  └─ img/
├─ product/
│  ├─ detail.html
│  ├─ list.html
│  └─ search.html
└─ layout/basic/
   ├─ layout.html
   └─ main.html
```

## 구성 요소 설계

### 1. `setup.html`

역할: 비개발자용 전역 설정 파일.

포함 설정:

- 상단 배너 표시 여부
- 팝업 표시 여부
- 메인 히어로 표시 여부
- 신상품 영역 표시 여부
- 베스트 상품 영역 표시 여부
- 카테고리 탭 표시 여부
- 이미지 갤러리 표시 여부
- 동영상 영역 표시 여부
- 지도 영역 표시 여부
- 리뷰 영역 표시 여부
- 인스타그램 표시 여부
- 카카오 채널 URL
- 네이버 톡톡 URL
- 유튜브 URL
- 에스크로 URL

표준 전역 객체:

```html
<script>
window.NK_CONFIG = {
  showTopBanner: true,
  showPopup: false,
  showMainHero: true,
  showNewProducts: true,
  showBestProducts: true,
  showCategoryTabs: true,
  showImageGallery: true,
  showVideo: false,
  showMap: false,
  showReview: true,
  showInstagram: false,
  kakaoChannelUrl: "",
  naverTalkUrl: "",
  youtubeUrl: "",
  escrowUrl: ""
};
</script>
```

### 2. `_nk/inc/common.html`

역할: 공통 CSS/JS 로딩.

포함:

- Pretendard 로드
- Phosphor Icons CDN 로드
- Swiper CSS/JS 로드
- `_nk/css` 공통 파일 로드
- `_nk/js` 공통 파일 로드
- `setup.html` import

금지:

- Font Awesome 로드
- Google Fonts 임의 로드
- `_idio` 경로 참조

### 3. `_nk/inc` 섹션 파일

각 섹션은 단일 책임을 가진다.

예:

- `main-hero.html`: 메인 배너
- `product-list.html`: 일반 상품 리스트
- `product-slide.html`: 상품 슬라이드
- `category-tabs.html`: 카테고리 탭 상품 영역
- `image-gallery.html`: 이미지 갤러리
- `review.html`: 리뷰 영역

각 섹션의 공통 규칙:

- 최상위 class는 `nk-section`과 섹션별 class를 함께 사용한다.
- Easy 호환 대상이면 `data-ez-module`을 붙인다.
- 제목은 `data-ez-role="title"`을 붙인다.
- 설명은 `data-ez-role="subtitle"` 또는 `data-ez-role="desc"`를 붙인다.
- 링크는 `data-ez-role="a"`를 붙인다.
- 이미지는 `data-ez-role="img-pc"`, `data-ez-role="img-mobile"`를 구분한다.

### 4. `ez/ez-module.html`

역할: SmartDesignEasy 호환 블록 정의.

포함 대상:

- 상품 리스트 블록
- 상품 슬라이드 블록
- 이미지 갤러리 블록
- 비디오 블록
- 지도 블록
- 텍스트 배너 블록
- 카테고리 탭 상품 블록

필수 속성:

- `data-ez-module`
- `data-ez-layout`
- `data-ez-role`
- `data-ez-holder`
- `ez-prop`
- `ez-var`
- `ez-item`

예시:

```html
<section class="nk-section nk-main-product" data-ez-module="product-list/1" data-ez-layout="grid4">
  <ez-prop data-version="1.0.0">
    <ez-var data-prop="layout" data-namespace="ez.module.product-list.layout" data-type="array">
      <ez-item data-id="grid3" data-name="3단 상품 진열"></ez-item>
      <ez-item data-id="grid4" data-name="4단 상품 진열"></ez-item>
      <ez-item data-id="grid5" data-name="5단 상품 진열"></ez-item>
    </ez-var>
  </ez-prop>
</section>
```

### 5. `_nk/css`

역할별 분리:

- `nk-tokens.css`: 색상, 폰트, 간격, 반응형 기준
- `nk-reset.css`: 카페24 기본 여백/폭 충돌 최소화
- `nk-common.css`: 공통 레이아웃과 유틸리티
- `nk-header.css`: 헤더
- `nk-footer.css`: 푸터
- `nk-main.css`: 메인 섹션
- `nk-product.css`: 상품 카드, 가격, 배지
- `nk-review.css`: 리뷰 UI
- `nk-ez.css`: Easy 편집기 호환 보정
- `nk-responsive.css`: 390/768/1440/1920 기준 반응형
- `nk-custom.css`: 클라이언트별 추가 수정

토큰 규칙:

```css
:root {
  --nk-color-primary: #222222;
  --nk-color-bg: #ffffff;
  --nk-color-surface: #f8f8f8;
  --nk-color-text: #1a1a1a;
  --nk-color-muted: #666666;
  --nk-color-border: #e6e6e6;
  --nk-font-family: "Pretendard", sans-serif;
}
```

### 6. `_nk/js`

역할별 분리:

- `nk-config.js`: 설정 기본값과 안전한 읽기 함수
- `nk-core.js`: `NK_CONFIG` 적용, 영역 on/off
- `nk-header.js`: 헤더 fixed, 검색, 모바일 메뉴
- `nk-slider.js`: Swiper 초기화
- `nk-product.js`: 상품 카드 가격/할인/아이콘 정리
- `nk-review.js`: 리뷰 목록, 포토리뷰, 베스트리뷰, 빈 상태 처리
- `nk-detail.js`: 상세 페이지 가격, 리뷰 점수, 구매 영역 보정
- `nk-ez-adapter.js`: Easy 속성 기반 레이아웃 보정

JS 원칙:

- 요소가 없으면 조용히 종료한다.
- 전역 오류를 만들지 않는다.
- `data-ez-*`가 없어도 작동한다.
- jQuery 의존은 카페24 기본 환경에 한정하고, 새 모듈은 가능한 한 Vanilla JavaScript로 작성한다.

## 데이터 흐름

```text
setup.html
→ window.NK_CONFIG
→ nk-config.js
→ nk-core.js
→ 각 섹션 on/off, 링크, 텍스트, class 적용

index.html/root.html
→ _nk/inc/*.html import
→ _nk/css/*.css 로 스타일 적용
→ _nk/js/*.js 로 카페24 DOM 보정

SmartDesignEasy 편집기
→ ez/ez-module.html 또는 data-ez-* 속성 인식
→ 제목/이미지/링크/레이아웃 편집 가능
```

## 검증 기준

### 구조 검증

- `src/setup.html` 존재
- `src/ez/ez-module.html` 존재
- `src/_nk/inc/common.html` 존재
- `src/_nk/css/nk-tokens.css` 존재
- `src/_nk/js/nk-core.js` 존재

### 네임스페이스 검증

금지 문자열:

- `_idio`
- `IDIO[`
- `--idio-`
- `Font Awesome`
- `fontawesome`
- `fa-regular`
- `fa-solid`
- `font-style: italic`
- `font-style: oblique`

필수 문자열:

- `_nk`
- `NK_CONFIG`
- `--nk-`
- `nk-`
- `Pretendard`
- `phosphor`

### Easy 호환 검증

필수 문자열:

- `data-ez-module`
- `data-ez-role`
- `data-ez-holder`
- `ez-prop`
- `ez-var`
- `ez-item`

### 반응형 검증

필수 viewport:

- 390px 모바일
- 768px 태블릿
- 1440px PC
- 1920px 와이드

### 기존 키트 검증

- `bash scripts/build-dist-kit.sh`
- `bash scripts/verify-kit.sh`
- `python -m unittest discover -s mcp/tests -p "test*.py" -v`
- `python mcp/cli.py skin-audit agent-kit/clients/_verified-template/src --json-out tmp/skin-audit.json`

## 위험과 대응

### 위험 1. Easy 속성만 붙이고 실제 Easy 편집기에서 동작하지 않을 수 있음

대응:

- `data-ez-*`는 화면 기능의 필수 조건으로 쓰지 않는다.
- Easy 호환은 별도 검증 항목으로 둔다.
- 초기 구현은 로컬 구조 검증과 카페24 HTML 안전성 검증을 우선한다.

### 위험 2. Esthe 원본 복제와 NK 재구현 경계가 흐려질 수 있음

대응:

- `_idio`, `IDIO`, `--idio-*` 금지 검사를 추가한다.
- 원본 이미지와 문구를 사용하지 않는다.
- 파일명과 class를 `nk-*` 기준으로 재설계한다.

### 위험 3. 카페24 기본 CSS와 충돌할 수 있음

대응:

- 기본 `css/module` 대량 수정 대신 `_nk/css/nk-reset.css`, `nk-ez.css`, `nk-responsive.css`로 보정한다.
- `skin-audit` 기준을 통과해야 한다.

### 위험 4. 비개발자가 수정할 파일이 많아질 수 있음

대응:

- 비개발자 수정 지점은 `setup.html`과 `nk-tokens.css`로 제한한다.
- 각 파일 상단에 한국어 주석을 넣는다.

## 구현 우선순위

1. 구조 scaffold 추가
2. `setup.html`과 `NK_CONFIG` 도입
3. `_nk/inc/common.html` 공통 로더 정리
4. 핵심 CSS 토큰과 reset layer 작성
5. 메인 섹션 4종 구현
   - hero
   - product-list
   - product-slide
   - image-gallery
6. `ez/ez-module.html` 작성
7. JS adapter 최소 구현
8. 검증 스크립트에 금지/필수 문자열 검사 추가
9. 빌드 dist 반영
10. 문서와 비개발자 안내 업데이트

## 완료 정의

이 설계의 구현은 다음 조건을 모두 만족해야 완료로 본다.

- 검증 템플릿이 Esthe-style 구조를 가진다.
- `setup.html`에서 주요 영역 on/off가 가능하다.
- `ez/ez-module.html`에 Easy 호환 속성이 포함된다.
- 모든 커스텀 클래스가 `nk-` 접두사를 사용한다.
- Pretendard와 Phosphor Icons 기준을 지킨다.
- `_idio`, `IDIO`, `--idio-*`, Font Awesome이 남지 않는다.
- 빌드, 검증, 단위 테스트, skin-audit가 통과한다.
- 비개발자용 안내 문서가 업데이트된다.
