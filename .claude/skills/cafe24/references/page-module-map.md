# 카페24 base 스킨 페이지·모듈 맵 (실측 초안)

> **[실측·초안]** ecudemo400125 `/sde_design/base` 1개 몰 실측(2026-07-05, HTML 234p). **몰·스킨마다 페이지/모듈 구성이 다름 — 그대로 일반화 금지, 새 몰은 재스캔(P0) 필요.**
> 재생성: FTP로 base 트리 walk → 각 페이지 `module="..."`·`{$var}`·`anchorBoxId` 추출 (읽기전용). 원자료: `page-module-map.json`·`module-safety.json`.

## 페이지 인벤토리 (그룹별)

| 그룹 | 페이지수 | 재마크업 성향 | 대표 페이지 |
|---|---|---|---|
| order | 56 | 🔴 거래 | order/basket.html, order/custom_ship_area.html, order/defered_payment_guide_popup.html, order/ec_orderform/additionalInput.html, order/ec_orderform/agreement.html |
| board | 47 | 🟡 게시판 | board/consult/list.html, board/consult/modify.html, board/consult/read.html, board/consult/reply.html, board/consult/write.html |
| myshop | 41 | 🔴 폼 | myshop/addr/list.html, myshop/addr/modify.html, myshop/addr/register.html, myshop/addr_popup/list.html, myshop/addr_popup/modify.html |
| product | 30 | ✅/🔴 혼재 | product/add_basket.html, product/add_basket2.html, product/basket_option.html, product/compare.html, product/coupon_popup.html |
| member | 25 | 🔴 폼 | member/adminFail.html, member/agreement.html, member/certification_layer.html, member/change_passwd.html, member/check_password.html |
| calendar | 7 | 🟡 | calendar/calendar_day.html, calendar/calendar_field.html, calendar/calendar_modify.html, calendar/calendar_month.html, calendar/calendar_view.html |
| coupon | 5 | 🔴 | coupon/coupon_down_result.html, coupon/coupon_list.html, coupon/coupon_productdetail.html, coupon/coupon_select.html, coupon/coupon_zone.html |
| intro | 5 | [검증필요] | intro/adult_certification.html, intro/adult_i.html, intro/adult_i_recommend.html, intro/adult_im.html, intro/member.html |
| layout | 5 | ✅ 레이아웃 | layout/basic/intro.html, layout/basic/layout.html, layout/basic/main.html, layout/basic/main_supply.html, layout/basic/popup.html |
| link | 3 | [검증필요] | link/bookmark.html, link/livelinkon.html, link/shortcut.html |
| attend | 2 | [검증필요] | attend/comment.html, attend/stamp.html |
| estimate | 2 | [검증필요] | estimate/print.html, estimate/userform.html |
| shopinfo | 2 | [검증필요] | shopinfo/company.html, shopinfo/guide.html |
| supply | 2 | [검증필요] | supply/index.html, supply/main.html |
| index.html | 1 | ✅ | index.html |
| poll | 1 | [검증필요] | poll/poll_result.html |

## 대표 페이지 바인딩 밀도 (재마크업 위험 근거)

| 페이지 | 모듈수 | 변수 | onclick/action | 재마크업 |
|---|---|---|---|---|
| `index.html` | 28 | 15 | 0 | ✅ 안전 |
| `product/detail.html` | 25 | 227 | 19 | 🔴 고위험 |
| `order/basket.html` | 25 | 294 | 184 | 🔴 고위험 |
| `member/join.html` | 1 | 273 | 16 | 🔴 고위험 |

> 결론: **전시성 상단(index·layout·상품전시)=재마크업 쉬움 ✅ / 거래 하단(basket 294변수·184바인딩 등)=고위험 🔴**. 방법론 원칙 "보여주기=재마크업 / 거래=오버라이드+반복단위 보존"이 실측으로 성립.

## 2번째 데이터포인트 — skin1(EZ) 대조 [실측]
> 같은 몰 `skin1`(EZ 방식) 실측: HTML 268p · 모듈 590종(base와 공통 547) · **data-ez 402·`<ez-*>` 228 (base는 0)** · EZ 폴더 `ez/·smart-banner/·svg/·preference/` 존재.
> **결론**: 모듈·anchorBoxId 반복단위·변수 골격은 base와 동일 → **재마크업 보존대상은 HTML/EZ 무관 동일**. 단 **EZ는 data-ez 속성 보존 + 테마CSS/smart-banner 선별 이식**이 추가된다(통째 덮기 금지). 상세: `~/Downloads/ecudemo400125-skin1-audit/skin1-vs-base.md` (레포 밖).
> [검증필요] skin1엔 아직 `_nk/` 레이어 없음 = 미커스텀 상태.