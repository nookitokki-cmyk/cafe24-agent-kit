# Wave 4 — 페이지 타입 큐 ({몰ID})

> **정본 순서**: 메인 → PLP → PDP → 로그인/장바구니 → 게시판 → myshop → member → etc → popup  
> **193 일괄 금지** — 현재 타입 **PASS** 전 다음 타입 착수 불가.  
> **갱신**: {YYYY-MM-DD} · **정본 디자인**: `04_design/design.md`

**상태 범례**: `—` 미착수 · `WIP` 진행 · `PASS` 4-tier+interaction · `FAIL` · `수용`/`제외`(사유 필수)

**연관 문서**: `wave4-status.md` · `wave4-defects.md` · `blank-slate-rebuild-queue.md` · `rerun-audit-spec.md`

---

## §0 진행 요약

| 타입 | 페이지(예상) | 완료 | 상태 | 다음 액션 |
|---|:---:|:---:|---|---|
| 1 메인 | 1 | 0 | — | Wave0 foundation 후 착수 |
| 2 PLP | 3+ | 0 | — | §1 PASS 후 |
| 3 PDP | 1+ | 0 | — | §2 PASS 후 |
| 4 auth-order | 2+ | 0 | — | login + basket empty/filled |
| 5 board | 28+ | 0 | — | list/read/write/modify/reply × 유형 |
| 6 myshop | 21 | 0 | — | login=test 계정 필수 |
| 7 member | 8 | 0 | — | join/modify/find passwd |
| 8 etc | 7 | 0 | — | guide 탭 interaction |
| 9 popup/fragment | 45+ / 19 | 0 | — | G7 — popup 4-tier |
| G8 Final | status 193행 | 0 | — | ultraqa 8/8 · defects 0 |

---

## §1 메인 — `—`

**라우트**: `/` · **소스**: `layout/basic/main.html` + `nk-header.html` · `nk-footer.html`

### §1-A 페이지 행

| URL | 소스 파일 | module | submodule | section | page | interaction | 상태 | 비고 |
|---|---|:---:|:---:|:---:|:---:|:---:|---|---|
| `/` | layout/basic/main.html | — | — | — | — | — | — | |

### §1-B 모듈 인벤토리

| # | module | 위치 | inner rebuild | module tier | click-test | 비고 |
|:---:|---|---|:---:|:---:|:---:|---|
| 1 | `Layout_LogoTop` | nk-header | Wave1 | — | 로고→홈 | |
| 2 | `Layout_category` | GNB + drawer | Wave1 | — | PLP 링크 | |
| 3 | `Layout_statelogoff` / `Layout_stateLogon` | header | Wave1 | — | LOGIN·CART | |
| 4 | `Layout_SearchHeader` | search overlay | Wave1 | — | open/close/submit | |
| 5 | `product_listmain_*` | hero sections | Wave2 | — | card→PDP | anchorBoxId ×≥2 |
| 6 | `product_ListItem` | listmain 서브 | Wave2 | — | 가격 | |
| 7 | `Layout_Info` / `Layout_footer` / `Layout_LogoBottom` | nk-footer | Wave1 | — | 소셜 hover | parity §footer |
| 8 | `Layout_orderBasketcount` | #quick | stock | — | basket | |
| 9 | `Layout_productRecent` | #quick | stock | — | prev/next | |

**module 밖 섹션**: `.nk-hero` · `.nk-split-banner` · `#quick` · `.nk-topbar`

**Interaction checklist**: topbar · burger/drawer · search · scroll header · product card · quick basket · **footer social hover (PC)**

---

## §2 PLP — `—`

### §2-A 페이지 행

| URL | 소스 | module | submodule | section | page | interaction | 상태 | 비고 |
|---|---|:---:|:---:|:---:|:---:|:---:|---|---|
| `/product/list.html?cate_no={N}` | product/list.html | — | — | — | — | — | — | 대표 카테고리 |
| `/product/search.html` | product/search.html | — | — | — | — | — | — | |
| `/product/recent_view_product.html` | product/recent_view_product.html | — | — | — | — | — | — | empty state |

**Interaction**: card→PDP · sort · paginate · search · recent empty · MO390 overflow 0

---

## §3 PDP — `—`

| URL | 소스 | module | submodule | section | page | interaction | 상태 | 비고 |
|---|---|:---:|:---:|:---:|:---:|:---:|---|---|
| `/product/{slug}/{product_no}/` | product/detail.html | — | — | — | — | — | — | |

**Open-state submodule**: `image_zoom2.html` · `recommend_mail.html` — submodule tier 별도

**Interaction**: zoom · recommend popup · option/CTA · guest asyncbenefit · MO390

---

## §4 로그인/장바구니 — `—`

| URL | 소스 | module | submodule | section | page | interaction | 상태 | 비고 |
|---|---|:---:|:---:|:---:|:---:|:---:|---|---|
| `/member/login.html` | member/login.html | — | — | — | — | — | — | |
| `/order/basket.html` | order/basket.html | — | — | — | — | — | — | empty + filled |

**Parity 포인트**: `nk-empty` 이중 border · `nk-qty` DOM order · 타이틀 `var(--nk-ls-page-title)`

**Blockers**: `CAFE24_TEST_PW` · `MyShop_OrderHistoryNologin` 몰 설정

---

## §5 게시판 — `—`

> 28 URL 템플릿: index · consult/free/gallery/inquiry/memo/opdiary/product × list/read/write/modify/reply

| URL 패턴 | module tier | interaction | 상태 |
|---|---|:---:|---|
| `/board/index.html` | — | — | — |
| `/board/{type}/list.html?board_no={N}` | — | list→read | — |
| `/board/{type}/read.html?...` | — | — | — |
| `/board/{type}/write.html?...` | — | guest→login | — |

**잔존 watch**: `btnBasicFix` stock 버튼 · paginate gif · `nk-tabs` parity

---

## §6 myshop — `—`

> login 필수 · `--batch myshop` 4-tier strict

| HTML | module | submodule | section | page | 상태 | 비고 |
|---|---|:---:|:---:|:---:|---|---|
| myshop/index.html | — | — | — | — | — | em stock blue |
| myshop/order/list.html | — | — | — | — | — | |
| myshop/order/detail.html | — | — | — | — | — | |
| myshop/wish_list.html | — | — | — | — | — | |
| … (21 URL) | | | | | | `wave4-group-matrix.md` 참조 |

---

## §7 member — `—`

| HTML | module | submodule | section | page | 상태 | 비고 |
|---|---|:---:|:---:|:---:|---|---|
| member/join.html | — | — | — | — | — | |
| member/login.html | — | — | — | — | — | §4와 중복 — 재break 금지 |
| member/modify.html | — | — | — | — | — | login 후 |
| member/id/find_id.html | — | — | — | — | — | |
| member/passwd/find_passwd_*.html | — | — | — | — | — | flow |

---

## §8 etc — `—`

| HTML | module | submodule | section | page | 상태 | 비고 |
|---|---|:---:|:---:|:---:|---|---|
| coupon/coupon_zone.html | — | — | — | — | — | |
| shopinfo/company.html | — | — | — | — | — | |
| shopinfo/guide.html | — | — | — | — | — | `ul.menu` hide · nk-guide-tabs.js |
| attend/comment.html · stamp.html | — | — | — | — | — | |

---

## §9 popup/조각 — `—`

> popup 45 URL · fragment 19 URL · 제외: `pg_success` · popup layout (사유 문서화)

---

## G8 Final — `—`

- [ ] `wave4-status.md` 193행 4-tier sync
- [ ] `ultraqa-wave4-report.md` 8/8 PASS
- [ ] `wave4-defects.md` 열림 0
- [ ] parity 수동 sweep (`references/04-html-css-parity.md` §실전 패턴)
- [ ] 로그인 게이트 URL 수동 스크린샷
- [ ] 라이브 `?v={N}` PC1440 + MO390

---

## 스캔 명령 (몰ID·BASE 치환)

```bash
cd clients/{몰ID}/04_design/shots/wave4
node _stock-scan-tier.js --tier page --batch default
node _stock-scan-tier.js --tier module --batch board
node _ultraqa-wave4-sweep.js
```

Windows 상세: `references/08-full-audit-pipeline.md` §run-audit
