# 카페24 변수 사전 (상세·장바구니·주문서·회원 보강)

> 본문 SKILL.md는 상품 목록 변수 위주. 이 파일은 **상품 상세 / 장바구니 / 주문서 / 회원 / 게시판** 변수를 보강한다.
> 출처: kimyoungwopo/cafe24-smart-design (MIT) + 공식문서. 변수는 해당 모듈 scope 안에서만 치환됨.

---

## 1. 상품 상세 변수

| 변수 | 설명 |
|------|------|
| `{$name}` | 상품명(상세 페이지) |
| `{$product_code}` | 상품 코드 |
| `{$product_custom}` | 자체 상품코드 |
| `{$big_img}` | 상세 대표 이미지 |
| `{$image_big}` | 대표 이미지(큰 사이즈) |
| `{$image_small}` | 작은 이미지(상세 하단) |
| `{$zoom_param}` | 이미지 확대 파라미터 |
| `{$product_detail}` | 상품 상세 설명 |
| `{$mileage_value}` | 적립금/마일리지 |
| `{$dc_price}` | 회원 할인가 |
| `{$dc_min_price}` | 최소 할인가 |
| `{$supply_info}` | 공급사 정보 |
| `{$payment_info}` | 결제 정보 |
| `{$shipping_method}` | 배송 방법 |
| `{$shipping_area}` | 배송 지역 |
| `{$shipping}` / `{$delivery}` | 배송비 / 배송 정보 |
| `{$delivery_price}` | 배송 가격 |

### 옵션 변수
| 변수 | 설명 |
|------|------|
| `{$option_name}` / `{$option_value}` | 옵션명 / 옵션값 |
| `{$option_maxlength}` | 옵션 최대 글자수 |
| `{$add_option_name}` | 추가 옵션명 |
| `{$file_option_name}` | 파일 옵션명 |
| `{$form.option}` | 기본 옵션 폼 |
| `{$form.add_option}` | 추가 옵션 폼 |
| `{$quantity}` | 수량 |
| `{$color}` | 컬러칩 색상값 |
| `{$option_str}` | 옵션 문자열 |

### 구매 액션 변수
| 변수 | 설명 |
|------|------|
| `{$action_buy}` | 바로구매 |
| `{$action_basket}` | 장바구니 담기 |
| `{$action_wishlist}` | 관심상품 담기 |
| `{$action_recommend}` | 추천하기 |

---

## 2. 장바구니 변수

| 변수 | 설명 |
|------|------|
| `{$basket_count}` | 장바구니 상품 수 |
| `{$item_total}` | 아이템 합계 |
| `{$img}` | 상품 이미지 |
| `{$form.quantity}` | 수량 입력 |
| `{$option_str}` | 옵션 문자열 |
| `{$mileage}` | 적립금 |
| `{$discount}` | 할인 금액 |
| `{$delv_price_front}` / `{$delv_price_back}` | 배송비(기준통화/보조통화) |
| `{$delv_type}` | 배송 유형 |
| `{$sum_price_front}` / `{$sum_price_back}` | 소계(기준/보조 통화) |
| `{$total_product_price}` | 총 상품 금액 |
| `{$total_option_price}` | 총 옵션 금액 |
| `{$total_delv_price}` | 총 배송비 |
| `{$total_sum_price_front}` / `{$total_sum_price_back}` | 최종 합계(기준/보조 통화) |
| `{$action_modify}` | 수정 |
| `{$action_option_change}` | 옵션 변경 |
| `{$action_wish_item}` | 관심상품으로 이동 |
| `{$action_buy_item}` | 선택 상품 구매 |
| `{$display_product_sale_price}` | 판매가 표시 토글 |

---

## 3. 주문서 변수

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
| `{$coupon_cnt}` | 사용가능 쿠폰 수 |
| `{$total_avail_mileage}` | 사용가능 적립금 |
| `{$total_deposit}` | 사용가능 예치금 |
| `{$addr_paymethod}` | 결제 수단 |
| `{$pname}` / `{$bankaccount}` | 은행명 / 계좌번호 |
| `{$item_count}` | 아이템 수 |
| `{$price_unit_head}` | 통화 단위 |
| `{$mileage_name}` | 적립금 명칭 |

---

## 4. 회원 변수

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

(가입 폼 `{$form.*}` 전체 분류는 modules.md의 member_join 상세 변수 표 참고)

---

## 5. 게시판 변수 (본문 보강)

| 변수 | 설명 |
|------|------|
| `{$board_name}` / `{$board_title}` / `{$board_info}` | 게시판명 / 타이틀 / 정보 |
| `{$board_top_image}` | 게시판 상단 이미지 |
| `{$subject}` / `{$content}` | 글 제목 / 내용 |
| `{$writer}` / `{$write_date}` | 작성자 / 작성일 |
| `{$hit_count}` / `{$vote}` / `{$point_count}` / `{$comment_count}` | 조회수 / 추천 / 점수 / 댓글수 |
| `{$notice_icon}` / `{$fixed_icon}` | 공지 / 고정 아이콘 |
| `{$icon_re}` / `{$icon_new}` / `{$icon_hit}` / `{$icon_file}` / `{$icon_lock}` | 답글/신규/인기/첨부/비밀 아이콘 |
| `{$list_bg_color}` / `{$list_char_color}` / `{$link_color}` | 목록 배경/글자/링크 색상 |
| `{$param_read}` / `{$param_write}` / `{$param_prev}` / `{$param_next}` | 읽기/쓰기/이전/다음 파라미터 |
| `{$form.board_category}` | 카테고리 선택 폼 |
| `{$form.search_key}` / `{$form.search}` / `{$form.search_date}` | 검색 키/텍스트/날짜 폼 |
| `{$action_search}` | 검색 액션 |
| `{$action_category_move}` / `{$action_article_move}` / `{$action_article_copy}` | 카테고리이동/글이동/글복사 액션 |

### 게시판 config 조건 변수 (`|display`)
| 변수 | 설명 |
|------|------|
| `{$config.is_category\|display}` | 카테고리 사용 토글 |
| `{$config.use_date\|display}` | 날짜 표시 토글 |
| `{$config.use_cnt\|display}` | 조회수 표시 토글 |
| `{$config.is_use_recom\|display}` | 추천 사용 토글 |
| `{$config.is_use_point\|display}` | 점수 사용 토글 |
| `{$write_display\|display}` | 글쓰기 버튼 표시 |
| `{$category_display\|display}` / `{$date_display\|display}` / `{$hit_display\|display}` | 카테고리/날짜/조회수 컬럼 표시 |
