# reference-intake — ecudemo393674 → ecudemo400786

> 승인: 사용자 「다시 작업」= 인입 후 구현 진행  
> 소스: A 레퍼런스 URL · 타겟: ecudemo400786 · 범위: 전 페이지 · 데이터: 디자인만

## 페이지 인벤토리 (31 URLs, GNB·푸터 기준)

| 구분 | URL |
|---|---|
| main | `/` |
| plp | cate 23,24 + Women/Men 하위 14개 |
| order | `/order/basket.html` |
| member | login, agreement, privacy |
| pages | about, contact, guide, collection |
| board | free/1, faq/3, product/6, review/4 |
| other | wish_list, search, myshop (로그인 화면만 1:1) |

## 페이지 타입표

| 타입 | 페이지 | container |
|---|---|---|
| hero-main | `/` | 100%, pad 0 |
| plp-full | product/list* | 100%, pad 50px 20px 100px, banner+menupackage |
| pdp-full | product/detail* | 100%, pad 20px 20px 100px |
| narrow | pages/*, member/login, order/basket | max 1200px |
| board | board/* | narrow |

## HTML 구조 격차 (PLP)

| ref | tgt(수정 전) | 조치 |
|---|---|---|
| #container 직계 6모듈 | #contents 래퍼 + EZ section | list.html ref 구조 교체 + #contents CSS |
| headcategory.banner | product_top_image 빈块 | banner 모듈 |
| menupackage.menuCategory | ec-base-tab 숨김 | menupackage 마크업 |
| sortby ul + count | function+select | normalmenu ref 마크업 |
| item+effect+icon-wish | prdList__item EZ | list_product.html 교체 |

## 구현 순서

1. PLP list.html + list_product.html + sub-product.css
2. layout #contents PLP flatten
3. FTP 업로드 → 실측 PASS
4. PDP → order → member → board → pages (순차)

## 자기검증 루프 (90점 PASS)

- Phase별 채점: `work/scripts/ref393674-score-*.py`
- **90점 미만 → 수정·재업로드·재실측 반복**
- 로그: `work/clients/ecudemo400786/verify-loop.md`
