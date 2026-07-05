# /skin14 다운로드 및 base 의존성 점검

## 다운로드 결과
- 원격 경로: `/skin14`
- 로컬 저장 경로: `C:\nookitokki\cafe24-kit-작업본\web\cafe24\.Codex\clients\paransky97\src\skin14`
- 다운로드 결과: 598개 성공 / 51개 실패
- 로컬 폴더 수: 82개
- 로컬 파일 수: 598개

## 다운로드 실패 항목 성격
실패 51개는 대부분 아래 계열이다.

- `/skin14/order/ec_orderform/...`
- `/skin14/css/module/order/ec_orderform/...`
- `/skin14/js/module/order/ec_orderform/...`
- `/skin14/preference/product/product_category.ini`

확인 결과, 이 항목들은 SFTP 목록에는 보이지만 `read/cat` 시 `no such file`이 나는 항목이다. 카페24 SFTP에서 주문서 시스템 파일이 유령 항목처럼 보이는 케이스로 판단한다.

## 지시어 의존성 검사
검사 대상 지시어:

- `<!--@layout(...)-->`
- `<!--@import(...)-->`
- `<!--@css(...)-->`
- `<!--@js(...)-->`

검사 결과:

- 전체 지시어 수: 771개
- 고유 대상 파일 수: 299개
- `/skin14` 안에 없는 고유 대상: 20개
- `<!--@...(/base...)-->` 직접 참조: 0개

## `/skin14` 안에 없는 지시어 대상

```text
/css/module/order/ec_orderform/form_onetouch.css
/css/module/order/ec_orderform/form_onetouch_layer.css
/css/module/order/ec_orderform/form_onetouch_popup.css
/css/module/order/ec_orderform/form_onetouch_v2.css
/css/module/product/listrecommend.css
/js/module/order/ec_orderform/orders.js
/js/module/order/ec_orderform/orders_v2.js
/layout/intro/layout.html
/order/ec_orderform/additionalInput.html
/order/ec_orderform/agreement_v2.html
/order/ec_orderform/benefit.html
/order/ec_orderform/billingNshipping_v2.html
/order/ec_orderform/confirm.html
/order/ec_orderform/discount.html
/order/ec_orderform/gift.html
/order/ec_orderform/header.html
/order/ec_orderform/orderProduct_v2.html
/order/ec_orderform/payment_v2.html
/order/ec_orderform/paymethod_v2.html
/order/ec_orderform/product_detail.html
```

## base 연결 없이 동작 여부
판정:

- 메인/공통 레이아웃 기준으로는 `/base`를 직접 호출하는 지시어가 없다.
- `layout/basic/layout.html`, `layout/basic/main.html`의 주요 CSS/JS/import는 `/skin14` 안에 존재한다.
- 따라서 일반 디자인 작업 영역은 `/skin14` 기준으로 분석/수정 가능하다.
- 다만 주문서 `ec_orderform` 계열과 `member/adminFail.html`의 `/layout/intro/layout.html`, `supply/index.html`의 `listrecommend.css`는 완전 독립 복제 기준에서는 누락 상태다.
- 누락 항목은 `/base`에서도 SFTP read가 되지 않는 항목이 섞여 있어, 단순한 `/base` fallback 의존이라기보다 카페24 시스템 파일/유령 스텁으로 봐야 한다.

## 별도 외부 의존
- `//img.echosting.cafe24.com/skin/base...` 이미지/CDN 참조: 199건
- 이는 SFTP `/base` 폴더가 아니라 카페24 공통 이미지 CDN 참조다.

## 실무 결론
- `/skin14`는 로컬에 내려받아 분석 가능한 상태다.
- 일반 페이지 수정은 이 로컬 스킨을 기준으로 진행해도 된다.
- 단, 주문서/결제/관리자 실패 페이지까지 완전한 독립 동작을 보장하려면 라이브 페이지에서 별도 검증이 필요하다.
- 업로드 허용 경로는 아직 열지 않았다.
