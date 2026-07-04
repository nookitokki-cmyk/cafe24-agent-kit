# 카페24 EZ(스마트디자인Easy) base CSS 전역 지도 — skin2 실측 (2026-06-22)

> 목적: EZ 스킨이 우리 nk에 거는 규칙 + **HTML 방식(skin1)과 무엇이 다른지** 전수 정독 지도.
> HTML판 지도: [`BASE-CSS-MAP.md`](BASE-CSS-MAP.md) · EZ 함정 실측: [`EZ-OVERLAY-FINDINGS.md`](EZ-OVERLAY-FINDINGS.md)
> 근거: `~/Downloads/cafe24-400919-backup_2026-06-22/skin2/layout/basic/css/`(24) + `css/module/`(188) 전수 정독.

---

## 0. 한 줄 결론
**skin2 = EZ 표준 + "아키테이블(akitable)" 유료테마 하이브리드.** skin1(HTML)엔 아키테이블 흔적 0. EZ-on-legacy로 skin2 조각을 가져올 때 "왜 안 먹지"의 근원은 ① 클래스명 불일치(XANS↔BEM) ② 아키테이블 오버라이드 블록 ③ late-load ④ 무스코프 골드 — 이 4가지다.

## 1. HTML(skin1) vs EZ(skin2) 결정적 차이
| 영역 | skin1 (HTML) | skin2 (EZ+아키테이블) |
|---|---|---|
| **로드 순서** | head에서 base→`_nk`(nk가 마지막) | base(head) → 본문 → **`sub_style/sub_theme/add_theme/add_layout`가 `</body>` 직전 late-load** (layout.html:125~129) → **nk보다 나중, 동점이면 EZ 승** |
| **포인트색** | `_nk` 토큰 1곳 | **`#d0ac88`(theme01 WARM 골드)가 `.theme01` 클래스 없이 무스코프 전역** (sub_theme/main/layout/slideMenu 직박힘). theme02/03만 `.theme02/03` 스코프 |
| **폰트** | Pretendard 단일 | `layout.css:14` 전역 `"Jost"... !important` + theme02/03 `Lora`/`Roboto` `!important` (2중) |
| **헤더/푸터/카테고리 클래스** | `.xans-layout-footer .utilMenu`, `.xans-layout-category` (XANS 표준) | `.xans-layout-footer .util`, `.info__address`, **`.navigation__category`** (커스텀 BEM) — **이름 자체가 달라 skin1 셀렉터 재사용 불가** |
| **상품 진열 마크업** | `ul.prdList li.item`(고정 `width:189px;min-width:756px`, float) | `.prdList__item`(BEM) + flex + `calc()` 유동폭 |
| **레이아웃 분기** | 단일 | `#header.layout02~05`·`#footer.layout02/03` (PC 6/3종, body EZ 클래스 의존) |
| **!important 밀도** | 낮음 | sub_style 41 / layout 32 / main 23 / detail 17 / listnormal 9 (공격적) |
| **슬라이더** | 없음 | **Swiper JS + 자체 SVG 화살표**(`/SkinImg/img/slide_ar_*.svg`) 의존 — CSS만 바꾸면 죽음 |
| **EZ 후크** | 없음 | `body.theme01`·`data-ez-theme`·`.ez-align-*`·`.ez-discount-tag-off`·`[data-ez-image]`·`<ez-prop>` — EZ 엔진/JS가 제어, **건드리면 에디터·기능 깨짐** |

## 2. EZ 전용 TOP 위험 (skin1엔 없음)
1. **theme01 골드 `#d0ac88` 무스코프 전역** — sub_theme 전체 + main 11곳 + layout 6곳, 클래스 없이 항상 걸림 (최우선)
2. **`</body>` 직전 late-load** — nk보다 나중 → 동점 셀렉터면 EZ 승 → `#nk-skin1` 특이도 확실히 높이거나 사유 주석 `!important`
3. **폰트 2중 `!important`** (layout.css:14 + add_theme01/02)
4. **★ `sub_style.css:40` 상품 뱃지 `font-style:italic`** — **누끼토끼 절대금지** 속성을 base가 강제 → `font-style:normal !important` 필수
5. **아키테이블 오버라이드 블록** — detail/listnormal/detail_option/menupackage/restockSms/supplySearch 6파일에 `/** 아키테이블_style **/` (max-width:1280/1480 !important, 골드 다발)
6. **클래스명 BEM 불일치** — skin1 셀렉터 그대로 쓰면 안 먹음
7. **`.sale_box{...!important}`** 골드 원형 배지 (sub_theme:40, detail:353)
8. **Swiper + fixed 탭(z-index:997)** — JS 의존, CSS로 죽이면 깨짐
9. **`text-indent:150%`/`font-size:1px` 텍스트 숨김 트릭**(footer SNS) — 폰트만 덮으면 라벨 튀어나옴
10. **`#contents{width:100%!important}` vs `.section{max-width:1480px}`** 폭 충돌

## 3. EZ용 일괄 차단 초안 (참고 — 실제 적용 시 #nk-skin1 스코프)
```css
/* 폰트 재역전 (EZ !important 폰트 무력화) */
#nk-skin1, #nk-skin1 input,#nk-skin1 button { font-family:var(--nk-font,"Pretendard"),sans-serif !important; }
/* theme01 골드 → 토큰 */
#nk-skin1 [class^='btnSubmit'],#nk-skin1 .sale_box { background:var(--nk-accent) !important; }
/* ★ italic 금지(절대룰) */
#nk-skin1 .ec-base-product .prdList .thumbnail .badge { font-style:normal !important; color:var(--nk-accent); }
/* 아키테이블 고정폭 해제 */
#nk-skin1 .xans-product-detail,#nk-skin1 .product_top_image { max-width:none !important; width:100% !important; }
/* late-load 테마 타이틀 */
#nk-skin1 .titleArea h2 { font:inherit; color:var(--nk-text); }
/* 건드리지 말 것: body.theme0N, data-ez-*, .ez-*, .tabProduct.tab_fixed, #product_detail_option_layer, Swiper, 텍스트숨김트릭 */
```

## 4. nk 작업 행동 지침 (EZ 몰)
1. **헤더/푸터/카테고리/상품은 셀렉터 이름부터 확인** — skin2는 BEM(`.navigation__category`·`.prdList__item`). skin1 코드 복붙 금지.
2. **상품 detail/listnormal = 아키테이블 블록과의 싸움** — `detail.css:334`·`listnormal.css` 이후 블록이 base를 덮음 → 그 아래에서 `#nk-skin1` + 필요한 `!important`로만 대응.
3. **`#d0ac88` 골드를 `--nk-accent` 한 곳으로 토큰화.**
4. **`ez-*`·Swiper·fixed 탭·옵션레이어는 손대지 말 것** (EZ 엔진/JS 영역).
5. **late-load 전제** — nk CSS가 동점이면 짐. ID 스코프로 특이도를 확실히 높이거나, EZ `!important` 줄엔 사유 주석 후 `!important`.

## 5. EZ 결론 (방식 선택 함의)
이 분석은 **"HTML 네이티브(skin1)가 EZ-on-legacy(skin2)보다 우월"**을 재확인한다: EZ는 아키테이블 하이브리드라 클래스 불일치·late-load·무스코프 골드·!important 폭격·italic 강제까지 떠안는다. **EZ 몰이 출발점일 때만** EZ-on-legacy를 쓰고, 그때도 strip(HTML-clean)으로 수렴시키는 게 정공법.

## 6. 순정 skin4 교차검증 + 정정 (2026-06-22)
★ **skin4(순정 추가본) CSS = skin2(작업본) CSS 바이트 단위 100% 동일**(diff/md5 실측 212파일). 대표님 편집은 **CSS가 아니라 HTML 템플릿·EZ 블록(`layout/basic/*.html`, `ez/`) 레벨** → CSS 지도는 그대로 유효(편집 탓 오기록 없음).
기존 §1~3 검증: italic(`sub_style.css:40`)·late-load(`layout.html:125~129`, `</body>` 직전)·BEM(`.navigation__category`·`.info__*`)·골드·Swiper·아키테이블 6파일 전부 **정확**.

**정정 2건 (편집 탓 아닌 원래 오기록):**
1. **theme 파일번호 ≠ 테마번호 (1칸 밀림)**: `sub_theme.css`=theme01(골드 #d0ac88, **무스코프 base 디폴트**), `add_theme01.css`=**theme02**(#9fa581 + Lora, `.theme02` 스코프), `add_theme02.css`=**theme03**(Roboto, `.theme03`).
2. **상품 그리드 = `inline-block` + `ul.grid_N` 퍼센트**(ec-base-product.css:9,39-42), flex/calc 아님. 레거시 `li.item` 고정폭 float은 `basketAdd2.css`(레이어 장바구니)에만 잔존.

**신규**: `body{max-width:1480}`(layout.css:6) → 풀블리드는 `.section_full`(add_layout:84) 차용이 정석 / z-index 사다리(header 998·aside 1001·검색 1005·모달 10001) 회피 / detail.css !important 24개(지도 "17" 정정).
