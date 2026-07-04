# EZ→HTML 엎기(overlay) 실측 발견 — ecudemo400919 skin1(HTML) vs skin2(EZ)

> 작성: 2026-06-22 · 방법: skin1=HTML 스마트디자인 / skin2=Easy(EZ) 스킨 실파일 다운로드 후 정밀 비교 (FTP 읽기)
> 목적: 카페24 작업 2방식(① HTML 네이티브 시작 / ② EZ를 HTML에 엎어서 시작) 중 ②의 함정을 정량 근거로 기록.
> 베이스라인(이미 키트에 있음): `EZ-STRATEGY.md`, `01_작업하기/workflows/07·08`, `common-pitfalls F35/F36`.
> 이 문서는 그 위에 **실측 증분**만 기록.

---

## 0. 스킨 판별 (실측)

| | skin1 = **HTML** | skin2 = **EZ** |
|---|---|---|
| `ez/` 폴더 | 없음 | **있음** (`ez-module.html`, `init.js`) |
| `smart-banner/`·`svg/`·`preference/` | 없음 | **있음** |
| layout.html `data-ez` | 0 | 1 (body) |
| layout.html `module=` | **37** | **4** |
| layout.html `@css` | **35** | 22 |
| index.html `data-ez` | 0 | **102** |
| index.html `ez-prop` | 0 | **44** |

---

## 1. ★ 핵심 발견 (엎기가 실제로 깨뜨리는 것)

### EZ-1. EZ layout은 "기능 module CSS"를 안 싣는다 → 통째 엎으면 20개 CSS 증발
HTML(skin1) layout.html이 직접 `@css`로 부르는데 EZ(skin2) layout.html엔 **없는** css (= EZ를 통째로 엎으면 사라지는 것):
```
css/module/layout/  category · logotop · logobottom · searchHeader · searchSide
                    login · statelogoff · statelogon · orderBasketcount · myshop
                    footer · info · boardInfo · shoppingInfo · productRecent
                    multiCurrency · multishopList · conversionpc · poll · project
```
→ **헤더 카테고리/로고/검색/로그인상태/장바구니수/푸터 스타일이 통째로 빠진다.** (F36 #2의 정량 증거 — "layout.html만 교체 시 필수 module 미동기")

### EZ-2. EZ는 테마 CSS를 `</body>` 직전에 로드 → custom.css보다 늦음 → override 전쟁
EZ(skin2)에만 있는 `@css` (엎으면 새로 들어오고, **우리 nk보다 나중 로드**됨):
```
layout/basic/css/  sub_style.css · sub_theme.css · add_theme01.css · add_theme02.css · add_layout.css
```
→ EZ-STRATEGY 1.2의 "detail.css late-load → override 전쟁"의 **실증**. **`#nk-skinN` ID 스코프가 필수인 결정적 이유** (로드 순서로는 절대 못 이김 — base가 뒤에 또 로드).

### EZ-3. ★ 골드(#d0ac88)의 근원 = EZ 테마 시스템
skin2 layout.html `<ez-prop>` 안:
```
theme01 "WARM"      data-background-color:#d0ac88   (body class="theme01" 기본)
theme02 "COZY"      data-background-color:#9fa581
theme03 "SENSITIVE" data-background-color:#beacc4
```
→ traps.json `F9`(골드 잔존)의 **출처가 EZ 테마**임이 확정. `<body class="theme01" data-ez-theme="theme01">` 가 색·폰트를 주입한다. **strip(Phase C) 안 하면 body.theme01이 계속 골드/테마폰트를 먹임.**

### EZ-4. EZST 폴리필 inline + ez/init.js → strip 시 순서 주의
skin2 layout.html `<head>`:
```html
<script>try{window.EZST={q:[],register:function(a,b){this.push([a,(b.init||b)(),arguments])}}}catch(e){}</script>
<!--@js(/ez/init.js)-->
```
→ strip 시 EZST 제거하면 smart-banner/슬라이더 깨짐 (F36 #5). `EZST.register` 순서 점검 필수.

### EZ-5. body 식별자 충돌 — EZ는 `class="theme01" data-ez-theme`, 우리는 `id="nk-skinN"`
엎으면 body가 `theme01`로 바뀌어 EZ 테마 CSS가 활성화된다. 우리 `#nk-skinN` 스코프와 **공존**시킬지(파일럿) **strip**할지가 갈림.

### EZ-6. EZ는 테마별 웹폰트를 자동 로드 → Pretendard와 충돌/중복
skin2가 부르는 폰트: `Noto Sans KR · Nanum Myeongjo · Nanum Gothic · Jost · Lora · Roboto` (theme01/02/03 각각).
→ 엎으면 이 link들이 추가 로드돼 Pretendard/Bricolage와 섞임. (traps `FONT`/`BASEFONT`의 EZ판 근원)

### EZ-7. EZ index = data-ez 102 + ez-prop 44 (비주얼에디터 콘텐츠 덩어리)
엎으면 이 마크업이 유입되는데 `ez/init.js`+EZST 없으면 **렌더 안 됨**. → 우리 식으로 가려면 strip 대상(102개 data-ez 제거).

### EZ-8. EZ는 svg 아이콘을 `@import`로 — HTML skin엔 `svg/` 폴더 없음
skin2: `<a ...>{$go_back}<!--@import(/svg/icon-go-back.html)-->뒤로가기</a>` (`Layout_MobileAction` RTMB).
→ 엎을 때 `svg/` 폴더를 같이 안 가져오면 `@import` 깨짐 (F25 유형).

### EZ-9. @css 의존 세트가 상호 배타 — "어느 세트를 살릴지"가 핵심 결정
- HTML skin = `css/module/layout/*` (기능별 모듈 CSS)
- EZ skin = `layout/basic/css/ec-base-*` (공통 UI) + 테마 CSS
→ 단순 덮어쓰기가 아니라 **두 세트를 병합**해야 함 (선별 이식의 구체적 의미).

### EZ-10. module 수 격차 37→4 = 헤더/푸터 기능 바인딩 손실
EZ layout은 구조를 `@import(header/sidebar/footer)`와 EZ 컴포넌트에 위임 → layout.html 자체 module은 4개뿐.
→ 통째 엎으면 헤더 유틸·로그인상태·장바구니수·검색·푸터 **모듈 바인딩 손실**.

---

## 2. 결론 — 2방식 차이 (키트 규칙에 반영 제안)

| 축 | ① HTML 네이티브 | ② EZ→HTML 엎기 |
|---|---|---|
| 시작 골격 | module CSS 37개 + 기능 CSS 직결 | module 4개 + 테마 CSS late-load + data-ez 102 |
| base가 이기는 주경로 | css/module/* 명시도 | **sub_theme/add_theme late-load + body.theme01** |
| 골드/테마색 | 잔존(드묾) | **body.theme01 → #d0ac88 상시 주입** |
| 필수 후처리 | 토큰화 | **strip(data-ez 제거) + 테마 CSS 차단 + 모듈/CSS 병합** |
| 진단 추가점 | 색/폰트/레이아웃 스윕 | **body[data-ez-theme] 감지 · sub_theme.css 로드 감지 · data-ez 잔존 카운트** |

→ **traps.json 에 `method: html-native | ez-on-legacy | both` 축 추가** + 위 EZ 함정을 `ez-on-legacy`로 태깅 제안.
→ **diagnose-overrides.js 에 EZ 감지 블록 추가**: `document.body.dataset.ezTheme` 존재 / `sub_theme.css`·`add_theme*.css` 로드 여부 / `[data-ez]` 잔존 수 / EZST 존재.

---

### EZ-11. ★ 부분 엎기 = dangling 참조 다발 (실제 FTP 엎기로 실증)
skin2(EZ) `layout.html`·`index.html`·`ez/`만 skin1(HTML)에 엎었더니, 엎은 layout이 부르는 EZ 의존 파일들이 skin1에 **없어서 죽은 링크**가 됨 (skin2엔 다 있음):
```
sub_theme.css ❌ · add_theme01.css ❌ · add_layout.css ❌ · svg/icon-go-back.html ❌ · swiper.min.css ❌
```
→ **"통째 덮기 ❌ → 선별 이식 ✅"(F36)의 결정적 실증.** EZ를 엎을 땐 `layout/index`만이 아니라 **테마 CSS(sub_theme·add_theme*·add_layout) + `svg/` + `ez/` + `smart-banner/` + swiper**까지 같이 가져와야 dangling 0. (테스트 후 skin1 원복 완료)

---

## 3. 작업 방식 판별 게이트 (이 발견의 결론 → 키트 반영)
지시 받으면 **코드 만지기 전에 방식부터 판별**한다. → `references/skin-method-detect.md` (판별 마커·분기·함정).
- 판별 마커(가장 확실): `ez/` 폴더 / `body[data-ez-theme]` / `sub_theme·add_theme*.css` 로드 / `data-ez-*` / EZST.
- `diagnose-overrides.js` 상단이 **방식(HTML-native / EZ-on-legacy)을 자동 판정**해 출력.
- traps.json 각 항목에 `method` 축(`html-native`/`ez-on-legacy`/`both`) 부여.
