# 카페24 모듈 사전 (상세·주문·회원·게시판 보강)

> 본문 SKILL.md는 메인/목록 모듈 위주. 이 파일은 **상품 상세 / 장바구니·주문서 / 회원 / 게시판** 모듈을 보강한다.
> 출처: kimyoungwopo/cafe24-smart-design (MIT) + 공식문서 sdsupport.cafe24.com. 실사용 중 틀린 내용 발견 시 즉시 수정.

---

## 1. 상품 상세 페이지 모듈 (detail.html)

| 모듈 ID | 용도 |
|---------|------|
| `product_detail` | 상품 핵심 정보(상품명·가격·배송) + 구매 영역 |
| `product_image` | 대표 이미지 + 확대(zoom) |
| `Product_mobileImage` | 모바일 상품 이미지 |
| `product_addimage` | 추가 이미지(썸네일 목록) |
| `product_Colorchip` | 컬러 옵션 칩 미리보기 |
| `product_option` | 기본 옵션(색상·사이즈 등) |
| `product_addoption` | 추가 입력 옵션 |
| `product_fileoption` | 파일 업로드 옵션 |
| `product_noneoption` | 무옵션 상품 수량 선택 |
| `product_action` | 구매하기 / 장바구니 / 관심상품 버튼 |
| `product_setproduct` | 세트상품 진열 |
| `product_addproduct` | 추가상품 진열 |
| `product_additional` | 상품 추가 정보 |
| `product_detaildesign` | 상세 설명(에디터 입력 영역) |
| `product_relation` | 관련상품 영역 |
| `product_relationlist` | 관련상품 목록 |
| `product_review` | 상품 후기 목록 |
| `product_reviewpaging` | 후기 페이징 |
| `product_qna` | 상품 Q&A 목록 |
| `product_qnapaging` | Q&A 페이징 |
| `coupon_productdetail` | 상세 페이지 쿠폰 표시 |
| `myshop_benefit` | 회원 할인/적립 혜택 정보 |

---

## 2. 목록/카테고리 페이지 모듈 (본문 보강)

| 모듈 ID | 용도 |
|---------|------|
| `product_headcategory` | 카테고리 브레드크럼 + 타이틀/배너 |
| `product_displaycategory` | 하위 카테고리 메뉴 |
| `product_children` | 카테고리 자식 메뉴 |
| `product_ListItem` | 상품 목록 진열 아이템(공통) |
| `product_normalmenu` | 상품 정렬/검색/비교 메뉴 |
| `product_FirstSelect` | 조건검색 1차 선택 |
| `product_SecondSelect` | 조건검색 2차 선택 |
| `product_Orderby` | 상품 정렬 기능 |

---

## 3. 장바구니 모듈 (basket.html)

| 모듈 ID | 용도 |
|---------|------|
| `Order_TabInfo` | 국내/해외배송 상품 탭 |
| `Order_Empty` | 빈 장바구니 안내 |
| `Order_EmptyItem` | 장바구니 상품 정보 |
| `Order_BasketOption` | 할인 금액 정보 |
| `Order_NormTitle` | 일반 상품 타이틀 |
| `Order_NormNormal` | 일반 상품(기본 배송) |
| `Order_list` | 상품 목록 |
| `Order_optionAll` | 전체 옵션 |
| `Order_optionList` | 옵션 목록 |
| `Order_optionAddList` | 추가 옵션 목록 |
| `Order_SuppNormal` | 일반 상품(공급사 배송) |
| `Order_NormIndividual` | 일반 상품(개별 배송) |
| `Order_NormOverseaTitle` | 해외배송 타이틀 |
| `Order_NormOversea` | 일반 상품(해외 배송) |
| `Order_InstTitle` | 무이자 상품 타이틀 |
| `Order_InstNormal` | 무이자 상품(기본 배송) |

## 4. 주문서 모듈 (orderform.html)

| 모듈 ID | 용도 |
|---------|------|
| `Order_form` | 주문서 메인 모듈 |
| `Order_normallist` | 기본 배송 상품 목록 |
| `Order_optionSet` | 상품 옵션 설정 |
| `Order_individuallist` | 개별 배송 상품 목록 |
| `Order_oversealist` | 해외 배송 상품 목록 |
| `Order_DeliveryList` | 배송지 선택 목록 |
| `Order_ordadd` | 추가 정보 입력 |

---

## 5. 회원 모듈

| 모듈 ID | 용도 | 핵심 변수 |
|---------|------|-----------|
| `member_login` | 로그인 폼(전체화면) | `{$form.member_id}`, `{$form.member_passwd}`, `{$action_func_login}`, `{$returnUrl}` |
| `member_join` | 회원가입 폼 | `{$form.member_id}`, `{$form.passwd}`, `{$form.name}`, `{$form.email}`, `{$action_func_join}` |
| `member_modify` | 회원정보 수정 | 가입 변수와 유사 |
| `member_find` | 아이디/비밀번호 찾기 | `{$form.name}`, `{$form.email}` |
| `MyShop_OrderHistoryNologin` | 비회원 주문 조회 | `{$form.order_name}`, `{$form.order_id}`, `{$form.order_password}` |

### member_join 상세 변수 (영역별)

| 영역 | 변수 |
|------|------|
| 인증 | `{$form.member_id}`, `{$form.passwd}`, `{$form.user_passwd_confirm}`, `{$form.hint}`, `{$form.hint_answer}` |
| 개인 | `{$form.name}`, `{$form.name_en}`, `{$form.email}`, `{$form.is_news_mail}` |
| 연락처 | `{$form.phone}`, `{$form.mobile}`, `{$form.is_sms}` |
| 주소 | `{$form.postcode1}`, `{$form.postcode2}`, `{$form.addr1}`, `{$form.addr2}` |
| 추가 | `{$form.nick_name}`, `{$form.is_sex}`, `{$form.birth_year}`, `{$form.birth_month}`, `{$form.birth_day}` |
| 직업 | `{$form.job_class}`, `{$form.job}`, `{$form.earning}`, `{$form.region}`, `{$form.reco_id}` |
| 환불계좌 | `{$form.bank_account_owner}`, `{$form.refund_bank_code}`, `{$form.bank_account_no}` |
| 본인확인 | `{$action_ipin_open}`, `{$action_mobile_open}`, `{$action_check_id}`, `{$action_find_address}` |
| 사업자 | `{$form.member_type}`, `{$form.company_type}`, `{$form.bname}`, `{$form.bssn1}`, `{$form.bssn2}`, `{$form.cname}`, `{$form.cssn}` |
| 외국인 | `{$form.foreigner_name}`, `{$form.foreigner_type}`, `{$form.foreigner_ssn}`, `{$form.citizenship}` |

---

## 6. 게시판 모듈 (본문 보강)

게시판 번호(`_1002` 등)는 게시판마다 다름.

| 모듈 ID | 용도 |
|---------|------|
| `board_title_{no}` | 게시판 타이틀/정보 |
| `board_category` | 게시판 카테고리 분류 |
| `board_ReplySort` | 댓글 정렬 |
| `board_listheader_{no}` | 목록 헤더(제목·작성자·날짜 컬럼) |
| `board_notice_{no}` | 공지 목록 |
| `board_fixed_{no}` | 고정(상단) 게시글 |
| `board_list_{no}` | 일반 글 목록 |
| `board_ButtonList_{no}` | 글쓰기 버튼 등 |
| `board_paging_{no}` | 페이징 |
| `board_catemove_{no}` | 카테고리/게시판 이동 |
| `board_function_{no}` | 게시판 기능(이동·복사) |
| `board_search_{no}` | 게시판 검색 |
| `board_listpackage_5` | 자유게시판 패키지 |
| `board_listpackage_6` | 상품 Q&A 패키지 |
