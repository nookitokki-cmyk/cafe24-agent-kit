// Default UltraQA sweep URLs — per-key override: audit-overrides.json ultraqaPages
const DEFAULT_ULTRAQA_PAGES = [
  ['index', '/'],
  ['plp', '/product/list.html?cate_no=24'],
  ['pdp', '/product/샘플상품-2/10/category/1/display/1/'],
  ['basket', '/order/basket.html'],
  ['login', '/member/login.html'],
  ['join', '/member/join.html'],
  ['find-id', '/member/id/find_id.html'],
  ['find-pw', '/member/passwd/find_passwd_info.html'],
  ['search', '/product/search.html?keyword=sample'],
  ['board-free', '/board/free/list.html?board_no=1'],
  ['recent', '/product/recent_view_product.html'],
  ['board-gallery', '/board/gallery/list.html?board_no=8'],
  ['guide', '/shopinfo/guide.html'],
  ['company', '/shopinfo/company.html'],
  ['coupon-zone', '/coupon/coupon_zone.html'],
  ['attend', '/attend/stamp.html'],
  ['gift-list', '/order/gift_list.html'],
  ['modify', '/member/modify.html'],
  ['agreement', '/member/agreement.html'],
  ['board-memo', '/board/memo/list.html?board_no=5'],
  ['myshop-index', '/myshop/index.html'],
  ['myshop-order', '/myshop/order/list.html'],
];

module.exports = { DEFAULT_ULTRAQA_PAGES };
