/**
 * nk-sticky-header.js — 스크롤 시 헤더 상단 고정 기능
 * 사용법: 카페24 관리자 → 디자인 → HTML/CSS 편집 → 레이아웃 HTML의 </body> 바로 위에 붙여넣기
 *         또는 EZ 에디터 → 공통 영역 → <body> 끝 부분에 <script> 태그로 감싸서 붙여넣기
 *
 * 필요한 CSS 추가:
 *   .nk-header { transition: all 0.3s ease; }
 *   .nk-header.is-sticky { position: fixed; top: 0; left: 0; width: 100%;
 *                           background: #ffffff; box-shadow: 0 2px 8px rgba(0,0,0,0.08);
 *                           z-index: 1000; }
 *
 * 주의: 헤더 HTML에 class="nk-header" 가 있어야 동작합니다.
 *       EZ 헤더를 사용하는 경우 .xans-layout-header 선택자도 함께 적용 가능.
 */

(function () {
  'use strict';

  /* ── 설정 ── 여기만 바꾸세요 ───────────────────────── */
  var STICKY_THRESHOLD = 100;   // 스크롤이 몇 px 넘으면 sticky가 될지 (기본 100px)
  var HEADER_SELECTOR  = '.nk-header'; // 헤더 CSS 선택자 (카페24 EZ 헤더면 '.xans-layout-header' 로 변경)
  /* ─────────────────────────────────────────────────── */

  // 헤더 요소를 찾습니다
  var header = document.querySelector(HEADER_SELECTOR);

  // 헤더를 찾지 못하면 아무것도 하지 않습니다 (에러 방지)
  if (!header) {
    console.warn('[nk-sticky-header] 헤더 요소를 찾을 수 없습니다:', HEADER_SELECTOR);
    return;
  }

  // sticky가 될 때 헤더 높이만큼 아래 콘텐츠가 올라오는 것을 막기 위한 placeholder
  // (sticky 전환 시 레이아웃이 튀는 현상 방지)
  var placeholder = document.createElement('div');
  placeholder.setAttribute('aria-hidden', 'true'); // 스크린리더가 읽지 않도록
  placeholder.style.cssText = 'display:none; visibility:hidden;';
  header.parentNode.insertBefore(placeholder, header.nextSibling);

  var isSticky       = false;  // 현재 sticky 상태 여부
  var headerHeight   = 0;      // 헤더 높이 (px)
  var ticking        = false;  // requestAnimationFrame 중복 방지 플래그

  // 헤더 높이를 다시 잽니다 (리사이즈 시 재측정용)
  function measureHeader() {
    headerHeight = header.offsetHeight;
  }

  // 스크롤 위치에 따라 sticky 클래스를 추가/제거합니다
  function updateStickyState() {
    var scrollY = window.pageYOffset || document.documentElement.scrollTop;

    if (scrollY > STICKY_THRESHOLD && !isSticky) {
      // 스크롤이 기준값을 넘었고 아직 sticky 아닌 경우 → sticky 적용
      measureHeader();
      header.classList.add('is-sticky');
      placeholder.style.display  = 'block';
      placeholder.style.height   = headerHeight + 'px';
      isSticky = true;

    } else if (scrollY <= STICKY_THRESHOLD && isSticky) {
      // 스크롤이 기준값 이하로 돌아온 경우 → sticky 해제
      header.classList.remove('is-sticky');
      placeholder.style.display = 'none';
      isSticky = false;
    }

    ticking = false; // 다음 스크롤 이벤트를 받을 준비 완료
  }

  // 스크롤 이벤트 (성능 최적화: requestAnimationFrame 사용)
  function onScroll() {
    if (!ticking) {
      requestAnimationFrame(updateStickyState);
      ticking = true;
    }
  }

  // 화면 크기가 바뀔 때 헤더 높이 재측정 + placeholder 높이 업데이트
  function onResize() {
    if (isSticky) {
      measureHeader();
      placeholder.style.height = headerHeight + 'px';
    }
  }

  // 이벤트 등록
  window.addEventListener('scroll',  onScroll,  { passive: true }); // passive: 스크롤 성능 향상
  window.addEventListener('resize',  onResize,  { passive: true });

  // 페이지 로드 시 초기 상태 확인 (새로고침 후 스크롤 위치가 유지되는 경우 대비)
  updateStickyState();

})();
