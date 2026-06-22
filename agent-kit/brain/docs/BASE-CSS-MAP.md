# 카페24 base CSS 전역 지도 (skin1 HTML 네이티브 실측, 2026-06-22)

> 목적: 카페24 기본(base) CSS·모듈 CSS가 우리 `#nk-skin1` 커스텀 스킨에 거는 규칙을 **전수 정독으로 매핑**.
> 방법론 전환: 화면 보고 깨진 것 패치하는 **런타임 함정 진단(reactive)** → 전역 CSS를 먼저 다 읽고 지도를 만드는 **전수 정독(proactive)**.
> 근거: `~/Downloads/cafe24-400919-backup_2026-06-22/skin1/layout/basic/css/*.css`(13개) + `css/module/**/*.css`. 줄 번호는 해당 몰 실측(스킨 버전마다 다를 수 있으니 재확인).
> 실증: 헤더 가로선 2줄(`#header:before/:after`)은 가상요소라 런타임 border 검사로 **안 잡혔고**, 전역 CSS 정독으로만 발견됨 → 정공법의 가치.

---

## 0. 왜 런타임 진단만으로 부족한가
| 못 잡는 유형 | 예 | 이유 |
|---|---|---|
| 가상요소 장식선 | `#header:before/:after`, `#footer:before`, `.ec-base-table table:before`, category 화살표 | `getBoundingClientRect`에 안 잡힘 |
| 숨은 고정폭 | `.prdList{min-width:756px}` | 상품 미등록 시 화면에 안 드러남 |
| 가려진 색 | `.ec-base-table table{color:#fff}` | 셀(th/td)이 덮어서 평소 안 보임 |
| !important 함정 | `ec-base-ui.css` 폼 5종 | 스코프로 못 이김 → 클래스명 회피만 답 |

→ **전역 CSS를 읽어야 "왜 이렇게 되는지"를 안다.** 이 문서가 그 지도.

---

## 1. TOP 위험 (nk 반응형/디자인을 실제로 깨는 순서)
| 순위 | 파일:줄 | 셀렉터 | 무엇을 깨나 | 처방 |
|---|---|---|---|---|
| 1 | common.css:10 | `body{min-width:1480px}` | 모바일 가로 스크롤·반응형 붕괴 | `body#nk-skin1{min-width:0!important}` |
| 2 | layout.css:22/23 | `#wrap{1460}`·`#container{1218}` | 컨테이너 고정폭 | `#nk-skin1 #wrap,#container{width:auto!important}` |
| 3 | layout.css:36/25 | `#contents{float:right;1014}`·`#sidebar{float:left}` | float 레이아웃 | `float:none!important` |
| 4 | layout.css:5,6,43 | `#header:before/:after`·`#footer:before` | 가상요소 가로선 3개 | `display:none;content:none` |
| 5 | footer.css:1 | `.xans-layout-footer{float:right;width:1000px}` | 푸터 정렬·폭 깨짐 | `float:none!important;width:auto!important` |
| 6 | ec-base-product.css:8 | `.prdList{min-width:756px}` | 상품 그리드 최소폭 | `min-width:0` |
| 7 | common.css:9 | `body{font:굴림/돋움;color:#353535}` | Pretendard 무력화 | `#nk-skin1{font-family:Pretendard…}` |
| 8 | ec-base-ui.css:49 | `input,select,textarea{font:돋움}` | 폼 폰트 | `#nk-skin1 input…{font-family:Pretendard}` |
| 9 | ec-base-table.css:1 | `table{color:#fff}` | 표 흰 글자 | `#nk-skin1 .ec-base-table table{color:inherit}` |
| 10 | logobottom.css:1 / logotop.css:1-2 | 푸터·헤더 로고 float·고정폭·파란 폰트 | 로고 깨짐 | float:none;font:inherit |

**!important 함정(스코프로 못 이김 → HTML에서 클래스 회피):**
- `ec-base-ui.css:63` `table tr.radioType input`, `span.noBorder input` — border/width/height/margin/background 전부 !important → nk 폼에 `radioType`/`noBorder` 클래스 쓰지 말 것
- `ec-base-button.css:2~5` `[class^='btnNormal|Submit|Em|Basic']` — 첫 클래스가 btn으로 시작하면 굴림+배경 → nk 요소에 base btn 클래스 혼용 금지(`nk-btn` 단독은 안전)

---

## 2. 영역별 지도 (요약)

### 전역 (common.css / layout.css)
- `body` min-width:1480 / font 굴림 / color #353535 — common.css:9,10
- `a{color:#000}` `a:hover{underline}` — common.css:19,20
- `#wrap/#container/#contents/#sidebar` 고정폭·float — layout.css:22,23,36,25
- `#header/#footer` border + `:before/:after` 가상요소선 — layout.css:4,5,6,42,43
- `.inner{width:1218px}` — layout.css:7,44 (우리는 `.nk-inner` 사용이라 무관)
- ★ `ec-base-layer.css:1~5`는 파일명과 달리 전역 reset(`li`,`table`,`caption`,`h1,h3`) 재선언 — 놓치기 쉬움

### 헤더 모듈 (css/module/layout/)
- `logotop.css` — `.xans-layout-logotop{width:800;text-align:center}` + `a{verdana 40px #008bcc bold}`
- `searchHeader.css` — `.xans-layout-searchheader{float:right;margin:-50px}`
- `statelogoff/logon.css` — `{float:right;height:45px}` + `a{background:ico_bar.gif}`
- `category.css` — `a{padding;font 14px bold}` + `.selected/.on/:hover{#008bcc}` + `.sub-category ul:before/:after{가상요소 화살표}`
- `shoppingInfo.css` — `{position:absolute}` + `li{float:left}` + `:before{세로선}`

### 푸터 모듈
- `footer.css` — `.xans-layout-footer{float:right;width:1000;height:234}` + `.utilMenu li{float:left;ico_bar2.gif}` + `.copyright/.pageTop/.hosting{position:absolute}`
- `info.css` — `.xans-layout-info{border-bottom:1px}` + `li.tel{25px Tahoma #495164}`
- `logobottom.css` — `{float:left;width:189;padding:64px}` + `a{verdana 28px #8c8c8c bold}`

### 상품 진열 (★ ec-base-product.css 가 보스 — listmain.css 없음)
- `.ec-base-product .prdList{min-width:756;font-size:0;margin:-20px}` — :8
- `a[href^='/product/detail.html']>img{border:1px #ececec}` — :6 (썸네일 테두리)
- `.thumbnail .icon{border-bottom:1px}` — :17
- `ul.grid2~5>li{width:50%/33%/25%/20%}` + `grid2 .thumbnail/.description{float;width 220/247}`

---

## 3. 일괄 차단 규칙
실 적용본은 **`snippets/css/nk-ez-override.css`** (§11 "전수분석 일괄 차단") 참조.
skin1 라이브에는 `_nk/css/nk-main.css` §8에 동일 처방 반영 완료(2026-06-22).

## 4. 적용 전 확인 (추측 금지)
1. `#header/#footer/#wrap/#container/body`가 우리 `#nk-skin1`(보통 body) 안인가 — body면 `body#nk-skin1`로, 바깥이면 비스코프 처리.
2. nk 스코프가 ID(`#nk-skin1`)인가 class(`.nk-skin1`)인가 — class면 명시도 낮아 일부 base를 못 이겨 `!important` 필요.

## 5. 재사용 지침
새 카페24 몰 작업 시: ① 이 지도로 TOP 위험 선제 차단 → ② `diagnose-overrides.js`로 런타임 확인 → ③ 남는 것만 개별 처방. "전수 정독 → 일괄 차단 → 런타임 검증" 순서.
