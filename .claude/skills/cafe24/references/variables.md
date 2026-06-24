# 카페24 변수 사전 (전 영역 250+)

> 카페24 스마트디자인의 핵심 치환 변수를 영역별로 망라한 사전입니다.
> 본문 `SKILL.md`는 상품 목록 변수 위주, 이 파일은 **전체 변수 마스터**입니다.
> 출처: kimyoungwopo/cafe24-smart-design (MIT) + 카페24 공식 개발자센터 + 누끼토끼 실무 정리.
> 변수는 **해당 모듈 scope 안에서만** 치환됩니다. 모듈 바깥에서 쓰면 `{$변수명}` 그대로 출력됩니다.

---

## 1. 상품 기본 정보

목록·상세 어디서나 자주 쓰는 식별·이름·링크 변수.

| 변수 | 설명 | 주 사용처 |
|------|------|-----------|
| `{$product_no}` | 상품 번호 (고유 ID) | 목록·상세 |
| `{$product_name}` | 상품명 (목록에서 표시되는 이름) | 목록 |
| `{$product_name_title}` | 상품명 (title 속성용) | 목록 |
| `{$product_name_title_display}` | 상품명 title 표시 토글 | 목록 |
| `{$name}` | 상품명 (상세 페이지) | 상세 |
| `{$product_code}` | 상품 코드 (관리 코드) | 상세 |
| `{$product_custom}` | 자체 상품 코드 | 상세 |
| `{$param}` | 상품 파라미터 (링크용) | 목록 |
| `{$link_product_detail}` | 상품 상세 페이지 링크 | 목록 |
| `{$link_product_list}` | 카테고리 상품 목록 링크 | 카테고리 |

---

## 2. 상품 가격

가격 표기와 할인·모바일 가격 변수.

| 변수 | 설명 | 주 사용처 |
|------|------|-----------|
| `{$product_price}` | 정가 (소비자가) | 목록·상세 |
| `{$product_sale_price}` | 판매가 (할인 적용) | 목록·상세 |
| `{$product_price_mobile}` | 모바일 상품가 | 모바일 상세 |
| `{$mobile_dc_price}` | 모바일 할인가 | 모바일 상세 |
| `{$mileage_value}` | 적립금/마일리지 | 상세 |
| `{$dc_price}` | 회원 할인가 | 상세 |
| `{$dc_min_price}` | 최소 할인가 | 상세 |
| `{$display_product_sale_price}` | 판매가 표시 토글 | 장바구니 |

---

## 3. 상품 이미지

목록 썸네일·상세 대표·서브 이미지 변수.

| 변수 | 설명 | 주 사용처 |
|------|------|-----------|
| `{$image_medium}` | 목록 이미지 (가장 많이 씀) | 목록 |
| `{$image_big}` | 대표 이미지 (큰 사이즈) | 상세 |
| `{$big_img}` | 상세 대표 이미지 | 상세 |
| `{$image_small}` | 작은 이미지 (상세 하단) | 상세 |
| `{$image_tiny}` | 아주 작은 목록 이미지 | 최근 본 상품 |
| `{$zoom_param}` | 이미지 확대 파라미터 | 상세 |
| `{$top_image1_tag}` | 카테고리 상단 이미지 1 | 목록 |
| `{$top_image2_tag}` | 카테고리 상단 이미지 2 | 목록 |
| `{$top_image3_tag}` | 카테고리 상단 이미지 3 | 목록 |

---

## 4. 상품 상태·아이콘

신상품·품절·세일 등 상태 표시 아이콘.

| 변수 | 설명 |
|------|------|
| `{$soldout_icon}` | 품절 아이콘 |
| `{$recommend_icon}` | 추천 아이콘 |
| `{$new_icon}` | 신상품 아이콘 |
| `{$sale_icon}` | 세일 아이콘 |
| `{$product_icons}` | 상품 아이콘 묶음 (전체 모음) |
| `{$option_preview_icon}` | 옵션 미리보기 아이콘 |
| `{$basket_icon}` | 장바구니 아이콘 |
| `{$zoom_icon}` | 확대 아이콘 |
| `{$delvtype_display}` | 배송 유형 표시 |

---

## 5. 상품 옵션

색상·사이즈·수량·추가 옵션·파일 옵션 변수.

| 변수 | 설명 |
|------|------|
| `{$option_name}` | 옵션명 (예: 컬러, 사이즈) |
| `{$option_value}` | 옵션값 |
| `{$option_maxlength}` | 옵션 최대 글자수 |
| `{$add_option_name}` | 추가 옵션명 |
| `{$file_option_name}` | 파일 옵션명 |
| `{$form.option}` | 기본 옵션 폼 |
| `{$form.add_option}` | 추가 옵션 폼 |
| `{$form.option_value}` | 옵션값 폼 |
| `{$quantity}` | 수량 |
| `{$color}` | 컬러칩 색상값 |
| `{$option_str}` | 옵션 문자열 (요약 표시용) |

---

## 6. 상품 상세 설명·배송

상세 본문·공급사·배송 정보.

| 변수 | 설명 |
|------|------|
| `{$product_detail}` | 상품 상세 설명 |
| `{$item_display}` | 아이템 표시 토글 |
| `{$item_title}` | 아이템 제목 |
| `{$item_title_display}` | 아이템 제목 표시 토글 |
| `{$item_content}` | 아이템 내용 |
| `{$supply_info}` | 공급사 정보 |
| `{$payment_info}` | 결제 정보 |
| `{$shipping_method}` | 배송 방법 |
| `{$shipping_area}` | 배송 지역 |
| `{$shipping}` | 배송비 |
| `{$delivery}` | 배송 정보 |
| `{$delivery_price}` | 배송 가격 |

---

## 7. 구매 액션

구매·장바구니·관심상품·추천 액션.

| 변수 | 설명 |
|------|------|
| `{$action_buy}` | 바로구매 |
| `{$action_basket}` | 장바구니 담기 |
| `{$action_wishlist}` | 관심상품 담기 |
| `{$action_recommend}` | 추천하기 |

---

## 8. 카테고리

카테고리명·이미지·뎁스(1~4단)·서브 카테고리.

| 변수 | 설명 |
|------|------|
| `{$category_name}` | 카테고리명 |
| `{$category_title_text}` | 카테고리 타이틀 텍스트 |
| `{$category_title_text_display}` | 타이틀 텍스트 표시 토글 |
| `{$category_title_img}` | 카테고리 타이틀 이미지 |
| `{$category_title_img_display}` | 타이틀 이미지 표시 토글 |
| `{$title_text_or_image}` | 텍스트/이미지 자동 선택 타이틀 |
| `{$name_or_img_tag}` | 카테고리명 또는 이미지 |
| `{$product_count}` | 카테고리 내 상품 수 |
| `{$product_count_display}` | 상품 수 표시 토글 |
| `{$children_icon}` | 하위 카테고리 아이콘 |
| `{$disp_cate_1}` ~ `{$disp_cate_4}` | 1~4단 카테고리 표시 |
| `{$name_1}` ~ `{$name_4}` | 1~4단 카테고리명 |
| `{$param_1}` ~ `{$param_4}` | 1~4단 카테고리 파라미터 |
| `{$param_cate_no}` | 카테고리 번호 파라미터 |

---

## 9. 정렬·페이지네이션

상품 목록 정렬·페이징 변수.

| 변수 | 설명 |
|------|------|
| `{$total_count}` | 전체 상품 수 |
| `{$param_first}` | 첫 페이지 링크 |
| `{$param_before}` | 이전 페이지 링크 |
| `{$param_next}` | 다음 페이지 링크 |
| `{$param_last}` | 마지막 페이지 링크 |
| `{$param_class}` | 현재 페이지 클래스 |
| `{$no}` | 페이지 번호 |
| `{$param_num}` | 페이지 번호 파라미터 |
| `{$selected}` | 선택 상태 |
| `{$value}` | 옵션값 (정렬 select용) |
| `{$title}` | 옵션 타이틀 (정렬 select용) |

---

## 10. 쇼핑 전역 정보

헤더·푸터에서 자주 쓰는 전역 변수.

| 변수 | 설명 |
|------|------|
| `{$basket_cnt}` | 장바구니 담긴 상품 수 (헤더 뱃지용) |
| `{$mylikeprd_total_cnt}` | 좋아요한 상품 수 |
| `{$interest_prd_cnt}` | 관심상품 수 |
| `{$mall_name}` | 쇼핑몰명 (사이트 제목) |
| `{$mobile_title}` | 모바일 페이지 타이틀 |

---

## 11. 장바구니

장바구니 페이지의 상품·금액·액션 변수.

| 변수 | 설명 |
|------|------|
| `{$basket_count}` | 장바구니 상품 수 |
| `{$item_total}` | 아이템 합계 |
| `{$img}` | 상품 이미지 |
| `{$form.quantity}` | 수량 입력 |
| `{$option_str}` | 옵션 문자열 |
| `{$mileage}` | 적립금 |
| `{$discount}` | 할인 금액 |
| `{$delv_price_front}` | 배송비 (기준통화) |
| `{$delv_price_back}` | 배송비 (보조통화) |
| `{$delv_type}` | 배송 유형 |
| `{$sum_price_front}` | 소계 (기준통화) |
| `{$sum_price_back}` | 소계 (보조통화) |
| `{$total_product_price}` | 총 상품 금액 |
| `{$total_option_price}` | 총 옵션 금액 |
| `{$total_delv_price}` | 총 배송비 |
| `{$total_sum_price_front}` | 최종 합계 (기준통화) |
| `{$total_sum_price_back}` | 최종 합계 (보조통화) |
| `{$action_modify}` | 수정 액션 |
| `{$action_option_change}` | 옵션 변경 액션 |
| `{$action_wish_item}` | 관심상품으로 이동 |
| `{$action_buy_item}` | 선택 상품 구매 |

---

## 12. 주문서

주문자·받는이·결제 수단·쿠폰·적립금 변수.

| 변수 | 설명 |
|------|------|
| `{$product_image}` | 상품 이미지 |
| `{$product_price_front}` | 상품 가격 |
| `{$product_quantity_text}` | 수량 텍스트 |
| `{$product_total_price_front}` | 상품 소계 |
| `{$form.oname}` | 주문자명 |
| `{$form.ozipcode1}` | 주문자 우편번호 |
| `{$form.oaddr1}` | 주문자 주소 |
| `{$form.ophone1_}` | 주문자 전화 |
| `{$form.oemail}` | 주문자 이메일 |
| `{$form.rname}` | 받는사람명 |
| `{$form.rzipcode1}` | 받는사람 우편번호 |
| `{$form.raddr1}` | 받는사람 주소 |
| `{$total_price}` | 총 결제 금액 |
| `{$total_order_price_front}` | 총 주문 금액 |
| `{$coupon_cnt}` | 사용 가능 쿠폰 수 |
| `{$total_avail_mileage}` | 사용 가능 적립금 |
| `{$total_deposit}` | 사용 가능 예치금 |
| `{$addr_paymethod}` | 결제 수단 |
| `{$pname}` | 은행명 |
| `{$bankaccount}` | 계좌번호 |
| `{$item_count}` | 아이템 수 |
| `{$price_unit_head}` | 통화 단위 |
| `{$mileage_name}` | 적립금 명칭 |

---

## 13. 회원

로그인·가입·등급·복귀 URL 변수.

| 변수 | 설명 |
|------|------|
| `{$member_name}` | 회원명 |
| `{$group_name}` | 회원 등급명 |
| `{$member_login_module_id}` | 로그인 모듈 ID |
| `{$member_login_tab_display}` | 로그인 탭 표시 |
| `{$form.member_id}` | 회원 ID 입력 |
| `{$form.member_passwd}` | 비밀번호 입력 |
| `{$form.use_login_keeping}` | 로그인 유지 |
| `{$form.check_save_id}` | 아이디 저장 |
| `{$action_func_login}` | 로그인 액션 |
| `{$returnUrl}` | 로그인 후 복귀 URL |
| `{$display_nomember}` | 비회원 주문 표시 토글 |
| `{$action_nomember_order}` | 비회원 주문 액션 |

(가입 폼 `{$form.*}` 전체 분류는 `modules.md`의 member_join 상세 변수 표 참고)

---

## 14. 게시판

게시판명·글 정보·아이콘·검색·액션 변수.

| 변수 | 설명 |
|------|------|
| `{$board_name}` | 게시판명 |
| `{$board_title}` | 게시판 타이틀 |
| `{$board_info}` | 게시판 안내 |
| `{$board_adult_icon}` | 성인 인증 아이콘 |
| `{$board_top_image}` | 게시판 상단 이미지 |
| `{$subject}` | 글 제목 |
| `{$content}` | 글 내용 |
| `{$writer}` | 작성자 |
| `{$write_date}` | 작성일 |
| `{$hit_count}` | 조회수 |
| `{$vote}` | 추천수 |
| `{$point_count}` | 점수 |
| `{$comment_count}` | 댓글수 |
| `{$no}` | 글 번호 |
| `{$notice_icon}` | 공지 아이콘 |
| `{$fixed_icon}` | 고정 아이콘 |
| `{$icon_re}` | 답글 아이콘 |
| `{$icon_new}` | NEW 아이콘 |
| `{$icon_hit}` | 인기 아이콘 |
| `{$icon_file}` | 첨부파일 아이콘 |
| `{$icon_lock}` | 비밀글 아이콘 |
| `{$member_icon}` | 회원 등급 아이콘 |
| `{$category_name}` | 카테고리명 |
| `{$list_bg_color}` | 목록 배경색 |
| `{$list_char_color}` | 목록 글자색 |
| `{$link_color}` | 링크색 |
| `{$checkbox}` | 체크박스 |
| `{$param_read}` | 읽기 파라미터 |
| `{$param_write}` | 쓰기 파라미터 |
| `{$param_prev}` | 이전 페이지 |
| `{$param_next}` | 다음 페이지 |
| `{$form.board_category}` | 카테고리 선택 폼 |
| `{$form.search_key}` | 검색 키 폼 |
| `{$form.search}` | 검색 텍스트 폼 |
| `{$form.search_date}` | 검색 날짜 폼 |
| `{$action_search}` | 검색 액션 |
| `{$action_category_move}` | 카테고리 이동 액션 |
| `{$action_article_move}` | 글 이동 액션 |
| `{$action_article_copy}` | 글 복사 액션 |
| `{$reply_sort}` | 댓글 정렬 |

---

## 15. Config 조건 변수 (`|display`)

`|display` 모디파이어로 토글 가능한 설정 변수.

| 변수 | 설명 |
|------|------|
| `{$config.is_category\|display}` | 카테고리 사용 토글 |
| `{$config.use_date\|display}` | 날짜 표시 토글 |
| `{$config.use_cnt\|display}` | 조회수 표시 토글 |
| `{$config.is_use_recom\|display}` | 추천 사용 토글 |
| `{$config.is_use_point\|display}` | 점수 사용 토글 |
| `{$write_display\|display}` | 글쓰기 버튼 표시 |
| `{$category_display\|display}` | 카테고리 컬럼 표시 |
| `{$date_display\|display}` | 날짜 컬럼 표시 |
| `{$hit_display\|display}` | 조회수 컬럼 표시 |
| `{$vote_display\|display}` | 추천 컬럼 표시 |
| `{$point_display\|display}` | 점수 컬럼 표시 |

---

## 비코더용 빠른 가이드

### 변수가 `{$변수명}` 그대로 출력될 때
1. **모듈 scope 확인** — 그 변수는 어떤 모듈 안에서만 작동합니다. 예: `{$basket_cnt}`는 `<!--@layout(/layout/basic/layout.html)-->` 또는 `Module=...basket_count` 안에서만 작동
2. **오타 확인** — 예: `product_name` ≠ `prdouct_name`
3. **페이지 종류 확인** — 상세 페이지 변수(`{$name}`)를 목록 페이지에 쓰면 빈 값

### 자주 헷갈리는 변수 페어
- `{$product_name}` (목록) vs `{$name}` (상세) — 같은 상품명이지만 페이지마다 다른 변수
- `{$product_price}` (정가) vs `{$product_sale_price}` (할인가)
- `{$image_medium}` (목록) vs `{$image_big}` / `{$big_img}` (상세)
- `{$mileage_value}` (적립금 금액) vs `{$mileage_name}` (적립금 명칭) vs `{$total_avail_mileage}` (사용 가능 적립금)

### 모디파이어와 함께 자주 쓰는 패턴
```html
<!-- 가격: 콤마 포함 표시 -->
{$product_price|number_format}원

<!-- 상품명: 20자 초과 시 ... 처리 -->
{$product_name|cut:20:"..."}

<!-- 토글 변수: HTML 자동 노출/숨김 -->
{$config.use_date|display}

<!-- HTML 이스케이프 해제 (위험: 신뢰된 데이터만) -->
{$content|noescape}
```

자세한 모디파이어 사용법은 `modifiers.md` 참고.
