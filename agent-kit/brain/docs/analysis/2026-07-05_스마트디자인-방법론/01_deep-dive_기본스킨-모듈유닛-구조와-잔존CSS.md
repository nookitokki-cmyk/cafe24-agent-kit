# [DEEP-DIVE] 카페24 스마트디자인 기본 스킨 — 페이지·모듈·유닛 구조와 "모듈 CSS가 남는" 원인 분석

> 작성: 2026-07-05 · 범위: **분석 전용** (스킨/파일 수정·FTP·배포 없음)
> 근거: cafe24-agent-kit 내부 지식 베이스(`SKILL.md`, `references/*`, `brain/docs/*`, `traps.json`, `_evidence/*`) 정독 + 공식 문서 인용분.
> 신뢰도 표기: **공식**(카페24 공식문서/API) · **실증**(누끼토끼 skin2~14 실작업 측정) · **추정** · **검증필요**(라이브 확인 전 단정 금지).

---

## 0. 세 줄 요약 (TL;DR)

1. **대표님이 느낀 "모듈 CSS가 자꾸 남는다"는 착각이 아니라 구조다.** 카페24는 모듈을 그릴 때 `xans-` 자동 클래스와 `/css/module/*.css`를 **강제로 주입**하고, 그 원본(base)은 **수정할 수 없다**. 그래서 마크업을 새로 짜도 base 모듈 CSS는 그대로 살아 있다.
2. **그러므로 "오버라이딩 대신 새 마크업"은 이분법이 아니다.** 새 마크업을 짜도 **reset/override 레이어는 반드시 병행**돼야 한다. 둘은 대체재가 아니라 **한 세트**다.
3. **모듈은 "얼마나 자유롭게 새로 짤 수 있느냐"에 따라 3등급으로 갈린다.** ①데이터만 뿌리는 모듈(진열·상세설명·헤더/푸터 레이아웃) = 자유 재작성 / ②폼·액션 모듈(회원·로그인·게시판) = 조건부(변수·id 보존) / ③JS 결합 모듈(옵션·장바구니 수량·주문서) = **구조 보존 + CSS만**. 방법론은 이 등급 분류 위에 세워야 한다.

---

## 0.5 먼저 용어 바로잡기 — "유닛(unit)"의 정체

대표님이 쓰신 "모듈의 유닛까지" 라는 표현을 소스 전수로 확인한 결과:

| 용어 | 공식 정의 존재? | 실제 정체 |
|---|---|---|
| **모듈(module)** | ✅ **공식** | 「1개 이상의 콘텐츠·기능의 묶음. 프로그램의 최소 단위로, HTML+변수 조합. `module="모듈아이디"`로 구동」 (OFFICIAL-AUDIT C-1c 인용) |
| **유닛(unit)** | ❌ **공식 정의 없음 (검증필요)** | 공식 스마트디자인 기본/에디터 문서에 "unit" 이라는 용어가 **명시돼 있지 않음**. 실무에서 "모듈이 만들어내는 반복 아이템 하나" 또는 "모듈이 렌더링한 DOM 조각"을 부르는 비공식 표현으로 추정 |
| **xans- 자동 클래스** | ⚠️ 패턴만 확인 | 모듈이 화면에 그려질 때 카페24 엔진이 **자동으로 붙이는 CSS 클래스**. `module="product_listnormal"` → `.xans-product-listnormal`. 이게 사실상 "유닛을 식별하는 유일한 손잡이"다 |

> **결론:** 실무에서 "유닛"이라 부를 만한 건 결국 **`xans-` 자동 클래스가 붙은 DOM 조각**이다. 이 문서에서는 "유닛 = 모듈이 뿌린 반복/구성 단위이며, `xans-` 클래스로 잡는다"로 통일한다.
> **검증필요:** 카페24 공식이 "unit"을 어떤 의미로 쓰는지(또는 안 쓰는지)는 개발자센터 확인 전까지 단정하지 않는다.

---

## 1. (a) 기본 스킨에 기본 제공되는 페이지 전수 + 페이지별 모듈·유닛 매핑

### 1-0. 중요한 한계 (추측 금지)

> 카페24 **공식 문서에는 "기본 스킨이 기본 제공하는 페이지 목록"이 하나의 표로 명시돼 있지 않다.**
> 아래 목록은 ①SFTP 폴더 구조(`/product/`, `/order/`, `/member/`, `/board/`) + ②`references/modules.md`·`SKILL.md`의 실무 검증 경로를 교차해 재구성한 것이다. 파일 경로 일부는 **실무 추정(⚠️)**이며, 실제 몰의 `skin_code` 폴더를 열어 확인해야 확정된다.

### 1-1. 기본 페이지 전수 목록 (카테고리별)

| 카테고리 | 페이지 | 파일 경로 | 신뢰도 |
|---|---|---|---|
| 메인 | 홈(메인) | `/index.html` | ✅ 실증 |
| 메인 | 공급사 전용 메인 | (공급사 계정) | ⚠️ 실무 |
| 상품목록(PLP) | 카테고리/상품 목록 | `/product/list.html` | ✅ 실증 |
| 상품상세(PDP) | 상품 상세 | `/product/detail.html` | ✅ 실증 |
| 장바구니 | 장바구니 | `/order/basket.html` | ✅ 실증 |
| 주문 | 주문서 | `/order/orderform.html` | ✅ 실증 |
| 주문 | 주문완료 | `/order/order_result.html` | ⚠️ 변수만 확인 |
| 회원 | 로그인 | `/member/login.html` | ✅ 실증 |
| 회원 | 회원가입 | `/member/join.html` | ✅ 실증 |
| 회원 | 정보수정 | `/member/modify.html` | ✅ 실증 |
| 회원 | 아이디·비번 찾기 | `/member/find.html` | ✅ 실증 |
| 마이페이지 | 비회원 주문조회 등 | `/myshop/...` | ⚠️ 경로 미확인(검증필요) |
| 게시판 | 목록/보기/쓰기 | `/board/list_{번호}.html` 등 | ✅ 실증 |

> **검증필요:** 마이페이지 계열(대시보드/적립금/관심상품/쿠폰)은 SFTP에 `myshop/` 폴더만 확인됐고 개별 파일명·모듈은 미확인. 팝업/약관/이용안내 등 시스템 부수 페이지도 이번 조사 범위 밖.

### 1-2. 페이지별 모듈 → 유닛(xans-) 매핑

각 페이지에 **기본으로 붙는 모듈**과 그 모듈이 만드는 **유닛 식별 클래스(xans-)**:

**메인 (`/index.html`)**

| 모듈 | 역할 | 유닛(xans-) |
|---|---|---|
| `product_listmain_1~5` | 메인 상품 진열 1~5 | `.xans-product-listmain-1~5` |
| `Layout_LogoTop` | 로고 | `.xans-layout-logotop` |
| `Layout_category` | 카테고리 GNB | `.xans-layout-category` |
| `Layout_statelogoff` / `Layout_statelogon` | 비로그인/로그인 분기 | `.xans-layout-statelogoff/-logon` |
| `Layout_SearchHeader` | 검색창 | `.xans-layout-searchheader` |
| `Layout_shoppingInfo` | 적립금·장바구니·관심 | `.xans-layout-shoppinginfo` |

**상품목록 (`/product/list.html`)**

| 모듈 | 역할 | 유닛(xans-) |
|---|---|---|
| `product_headcategory` | 브레드크럼·타이틀·배너 | `.xans-product-headcategory` |
| `product_displaycategory` | 하위 카테고리 메뉴 | `.xans-product-displaycategory` |
| `product_listnormal` / `_listnew` / `_listrecommend` | 상품 진열 | `.xans-product-listnormal` 등 |
| `product_normalmenu` | 정렬/검색/비교 | `.xans-product-normalmenu` |
| `product_normalpaging` | 페이징 | `.xans-product-normalpaging` |

**상품상세 (`/product/detail.html`)**

| 모듈 | 역할 | 유닛(xans-) |
|---|---|---|
| `product_detail` | 상품명·가격·배송·구매영역 | `.xans-product-detail` |
| `product_image` | 대표 이미지·확대 | `.xans-product-image` |
| `product_option` | 옵션(색/사이즈) | `.xans-product-option` |
| `product_action` | 구매/장바구니/관심 버튼 | `.xans-product-action` |
| `product_review` / `product_qna` | 후기 / Q&A | `.xans-product-review` / `-qna` |
| `product_relation(list)` | 관련상품 | `.xans-product-relation` |

**장바구니 (`/order/basket.html`)**

| 모듈 | 역할 | 유닛(xans-) |
|---|---|---|
| `Order_TabInfo` | 국내/해외 탭 | `.xans-order-tabinfo` |
| `Order_list` | 상품 목록 | `.xans-order-list` |
| `Order_optionList` | 옵션 목록 | `.xans-order-optionlist` |
| `Order_NormNormal` | 일반 상품(기본배송) | `.xans-order-normnormal` |

**주문서 (`/order/orderform.html`)**: `Order_form`, `Order_normallist`, `Order_DeliveryList`, `Order_ordadd` 등 → `.xans-order-*`
**회원 (`/member/*.html`)**: `member_login` / `member_join` / `member_modify` / `member_find` → `.xans-member-*`
**게시판 (`/board/list_{no}.html`)**: `board_title_{no}` / `board_list_{no}` / `board_notice_{no}` / `board_paging_{no}` / `board_search_{no}` → `.xans-board-*-{no}`

> 상세 모듈 ID·변수는 `references/modules.md`(상세·장바구니·주문·회원·게시판)와 `references/variables.md`(250+ 변수)에 이미 정리돼 있음. 이 문서는 "페이지 ↔ 모듈 ↔ 유닛" 연결만 정리.

---

## 2. (b) "기본 모듈 CSS가 남아 커스텀을 제약하는" 구조적 원인

대표님 표현대로 "모듈 CSS가 자꾸 남아서 제약이 많다"는 건 **정확한 관찰**이다. 원인은 4겹으로 쌓인다.

### 원인 ① base는 "수정 불가 + 자동 fallback"

- `/base/`(시스템 기본)와 `/css/module/**`(모듈 자동 주입 CSS)는 **직접 편집할 수 없다**. 파일이 내 스킨에 없으면 base에서 자동으로 끌어온다(fallback).
- 즉 **"삭제"라는 선택지가 없다.** 오직 위에 덮는(override) 것만 가능.

### 원인 ② 모듈을 그리면 `xans-` 클래스 + 모듈 CSS가 자동으로 딸려온다

- `module="product_listnormal"`을 쓰는 순간 → `.xans-product-listnormal`이 자동으로 붙고 → `/css/module/.../*.css`의 기본 스타일(회색 테두리·고정폭·가운데정렬·파란색 등)이 그 클래스에 걸린다.
- **핵심:** 내가 그 안의 HTML을 아무리 새로 짜도, **모듈을 쓰는 한 이 자동 CSS는 계속 주입된다.** → 대표님이 느낀 "제약"의 정체.

### 원인 ③ CSS 로드 순서 — 내 CSS가 나중에 와도 "명시도"로 져서 안 먹을 수 있다 (실증)

로드 순서(실측):

```
1) /layout/basic/css/*.css        (base 골격)
2) /css/module/**/*.css           (모듈 자동 CSS, 188개)
3) sub_theme.css / add_theme*.css (EZ 테마 — EZ 스킨일 때)
4) /custom.css 또는 /_nk/css/*    (내 커스텀 — 맨 나중)
```

- HTML 네이티브: 내 CSS가 나중이라도 base가 **명시도(specificity)**나 **`!important`**로 걸어놨으면 순서로는 못 이긴다 → `#nk-skinN` **ID 스코프**로 명시도를 올려야 이긴다.
- EZ 엎기: 테마 CSS(`sub_theme`/`add_theme*`)가 **`</body>` 직전 late-load** → 내 CSS보다 **나중에 로드** → 순서로도 지고, `body.theme01`이 색·폰트를 상시 주입 → **ID 스코프 필수 + 테마색 차단 필수**. (근거: EZ-OVERLAY-FINDINGS 실측)

### 원인 ④ `!important` 함정 — 명시도로도 못 이기는 구간

- `ec-base-ui.css`의 폼 5종(`radioType`, `noBorder` 등)과 `ec-base-button.css`의 `btnNormal/Submit/Em/Basic` 계열은 `!important`로 박혀 있어 **스코프로 못 이긴다** → 해법은 "이기기"가 아니라 **그 base 클래스명을 안 쓰기(회피)**. (근거: BASE-CSS-MAP §1)

### 원인 ⑤ 런타임 진단만으로는 안 보이는 함정

- 가상요소 장식선(`#header:before/:after`), 숨은 고정폭(`.prdList{min-width:756px}`), 가려진 색(`table{color:#fff}`) 등은 화면 검사(getBoundingClientRect)로 **안 잡힌다** → 전역 CSS **전수 정독**으로만 발견. (근거: BASE-CSS-MAP §0)

### 📌 이 장의 결정적 결론

> **"마크업을 새로 짜면 base 모듈 CSS에서 벗어난다"는 것은 사실이 아니다.**
> 모듈을 쓰는 한 `xans-` 클래스와 `/css/module/*.css`는 계속 붙는다.
> 따라서 **새 마크업을 짜든 안 짜든, base 함정을 무력화하는 reset/override 레이어(`nk-cafe24-reset.css` + `#nk-skinN` 스코프)는 반드시 병행**돼야 한다. 이게 대표님이 "제약이 많다"고 느낀 근본 이유이자, 방법론의 출발점이다.

이 키트는 이미 그 무력화 도구를 갖고 있다:
- **`snippets/css/nk-cafe24-reset.css`** — base 함정 10개 섹션 일괄 중화(`body.nk-skin` opt-in).
- **`references/traps.json`** — base가 이기는 함정 **47종** 머신리더블 카탈로그(증상·원인·detectJS·처방).
- **`scripts/diagnose-overrides.js`** — 라이브에서 "졌다/이겼다 + 원인 + 처방"을 콘솔로 자동 진단.
- **`brain/docs/BASE-CSS-MAP.md`** — base CSS 전역 지도(전수 정독).

---

## 3. (c) "기능 유지 + 새 마크업 + CSS" 방식이 실제로 가능한가 — 검증

**결론: 부분적으로 가능하다. 단, 모듈 유형에 따라 3등급으로 갈린다.** "무조건 새로 짜기"도, "무조건 오버라이드"도 아니다.

### 3-1. 모듈이 유지되는 대전제 (지키면 되는 최소 규칙) — 공식/실증

`module="..."`을 유지한 채 그 **안쪽 HTML을 새로 짜도** 데이터 바인딩·반복이 살아있으려면:

1. **`{$변수}`는 `module=""` 요소 안에서만 치환된다** (공식). 밖으로 빼면 빈 값(문자 그대로 아님 — [실측 2026-07-06]) → 모듈 밖은 하드코딩.
2. **반복 진열은 `id="anchorBoxId_{$product_no}"` 블록이 2개 이상 나란히** 있어야 인식된다 (실증). 1개면 상품 1개만 출력. 태그는 `<li>`든 `<div>`든 무관(id 기반 인식).
3. **모듈 설정변수(`$count` 등)는 각각 별도 줄**에 (실증). 한 줄에 몰아쓰면 전체 무시.
4. **옵션/폼은 `{$form.*}`·`{$action_*}`를 그대로** 둔다 (공식). select/input을 하드코딩하면 관리자 설정 미반영 + 계산 JS 붕괴.
5. **JS가 잡는 고정 id**(`anchorBoxId_*`, 회원가입 `name_view`/`ssn_view` 등)는 이름을 바꾸지 않는다.
6. **base CSS 무력화는 별도로**(2장 결론) — 새 마크업이 base를 없애주지 않는다.

### 3-2. 모듈 재작성 자유도 3등급 매트릭스 ★ 이 문서의 핵심

> 신뢰도: 대부분 실증/공식. 단 개별 모듈의 "완전 재작성 후 100% 정상"은 **라이브 검증 전 단정 금지(검증필요)** — 특히 옵션·주문서.

| 등급 | 성격 | 대표 모듈 | 새 마크업 | 권장 전략 |
|---|---|---|---|---|
| **A. 자유 재작성** | 데이터만 뿌림(로직 없음) | `product_listmain_N`, `product_listnormal`, `product_detaildesign`(상세설명), `coupon_productdetail`, **헤더/푸터 레이아웃**(`_nk/inc/`로 재작성 + `Layout_*` 모듈만 유지) | ✅ 내부 구조 자유 (규칙 3-1 준수) | **새 마크업 + nk- CSS** (오버라이드 최소) |
| **B. 조건부 재작성** | 폼·액션·페이징 결합 | `member_login`, `member_join`, `member_find`, `board_list_{no}`, `product_action`(버튼), `Order_list`(체크박스) | ⚠️ 레이아웃/섹션순서는 변경 가능, **변수·`{$action_*}`·고정 id는 보존** | 레이아웃만 새로, 폼 요소는 그대로 감싸기 |
| **C. 구조 보존(오버라이드가 정답)** | JS·계산에 DOM 구조 의존 | `product_option`/`product_addoption`(옵션), `Order_optionList`·장바구니 수량, `Order_form`(주문서), `Layout_category`(GNB depth), `Layout_statelogoff/logon`(분기) | ❌ 마크업 재작성 위험(선택·가격계산·POST 붕괴) | **원본 구조 유지 + CSS override + reset** |

**해석 (비유):**
- **A등급 = "빈 액자"** — 카페24가 사진(데이터)만 주고 액자 디자인은 내 맘대로. 마음껏 새로 짠다.
- **B등급 = "관공서 서류"** — 서식(변수·버튼 id)은 못 바꿔도, 종이 배치·여백·색은 다시 디자인 가능.
- **C등급 = "정밀기계 내부"** — 뚜껑(CSS)만 갈아끼운다. 안쪽 부품(DOM/JS) 건드리면 작동이 멈춘다.

### 3-3. "새 마크업" 방식이 실제로 채택된 실증 근거

- **헤더/푸터**: skin2(구매템플릿)·실작업에서 `_nk/inc/header.html`·`footer.html`에 **자기 마크업을 직접 작성**하고 `Layout_*` 모듈 블록만 원래대로 유지 → 성공. (실증)
- **메인 배너**: EZST 스마트배너 대신 `_nk/inc/banner/`에 Swiper로 독자 구현. (실증)
- **상품 진열**: `anchorBoxId` 2개 규칙만 지키면 카드 내부(`_nk/inc/prd.html`)를 원하는 구조로 재작성 → 성공. (실증)
- **반대로**: 옵션·장바구니 수량·주문서는 **CSS override로만** 다뤘고, 구조를 건드리면 계산/결제가 깨졌다는 함정(F* 계열)이 기록돼 있음. (실증)

### 3-4. 검증필요 (라이브 확인 전 단정 금지)

1. `product_option` 래퍼를 grid로 감싸되 `{$form.option}`만 유지했을 때 옵션·추가금액이 100% 정상인지 — **실물 검증 필요**.
2. 주문서 배송지/결제 영역 레이아웃 변경 후 POST/validation 유지 여부 — **미검증**.
3. EZ 속성 strip 후 카테고리·메인진열이 HTML 수정만으로 100% 복구되는지 — **미검증**.
4. 커스텀 JS 이벤트와 카페24 기본 옵션 JS의 타이밍 충돌 — **미검증**.

---

## 4. 신뢰도 종합 & 이번 분석의 한계

| 주제 | 신뢰도 | 근거 |
|---|---|---|
| 페이지→모듈→유닛(xans) 매핑 | ✅ 실증/공식 | `modules.md`·`SKILL.md` 교차 |
| "유닛" 공식 정의 | ❌ 검증필요 | 공식 문서 미명시 |
| base 모듈 CSS가 남는 원인(5겹) | ✅ 실증 | `BASE-CSS-MAP`·`EZ-OVERLAY-FINDINGS` 실측 |
| 새 마크업으로도 base CSS 안 사라짐 | ✅ 실증/논리 | 2장 결론 |
| 모듈 3등급 매트릭스 | ⚠️ 실증+추정 | A·헤더푸터=실증, C·옵션/주문서=함정기록, 개별 100% 정상은 검증필요 |
| 기본 페이지 파일 경로 일부 | ⚠️ 실무추정 | 실제 몰 `skin_code` 폴더로 확정 필요 |

**이번 분석이 안 한 것 (의도적):** 라이브 사이트·스킨 미접속, FTP·배포·커밋 없음. 위 "검증필요" 4종은 실제 몰에서 확인해야 함.

---

## 5. 이 분석이 계획서로 넘기는 3가지 씨앗

1. 방법론은 "오버라이드 vs 새 마크업"이 아니라 **"모듈 등급 분류 → 등급별 전략 + reset 병행"**으로 세운다.
2. 키트에 **"페이지 × 모듈 × 유닛 × 재작성 등급" 단일 인벤토리 문서**가 없다 → 신설이 최우선.
3. `traps.json`은 훌륭하나 **`method` 축 42/47 미채움**, 그리고 **모듈 재작성 등급(A/B/C)** 축이 아직 없다 → 보강 대상.

→ 계획서: `02_plan_초보자-카페24-커스텀-방법론과-키트보강.md`
