/**
 * nk-product-hover.js — 상품 카드 hover 시 두 번째 이미지 전환 기능
 * 사용법: 카페24 관리자 → 디자인 → HTML/CSS 편집 → 레이아웃 HTML의 </body> 바로 위에 붙여넣기
 *         또는 EZ 에디터 → 공통 영역 → <body> 끝 부분에 <script> 태그로 감싸서 붙여넣기
 *
 * 사전 준비 (카페24 공식 방법): 카페24엔 "롤오버 전용 이미지 칸"이 없습니다.
 *   "축소 이미지" 칸을 마우스오버용으로 빌려 씁니다.
 *   관리자 [상품 > 상품목록 > 수정 > 이미지 정보 > 이미지 등록 > '개별 이미지 등록']에서
 *   - 목록 이미지 = 평소 이미지  ({$image_medium})
 *   - 축소 이미지 = 마우스오버 시 이미지  ({$image_small})   ← 여기에 두 번째 사진 등록
 *   ⚠️ 두 이미지 사이즈를 동일하게 (안 맞으면 hover 시 깨짐).
 *
 * HTML 적용 방법:
 *   상품 진열 모듈(anchorBoxId 카드) 안의 상품 이미지 <img> 태그에
 *   data-hover-src 로 "축소 이미지 변수"를 지정하세요.
 *
 *   카페24 변수 예시:
 *   <img src="{$image_medium}" data-hover-src="{$image_small}" alt="{$seo_alt_tag}">
 *
 *   ※ 더 간단한 카페24 공식 방법(JS 없이 인라인):
 *   <img src="{$image_medium}" onmouseover="this.src='{$image_small}'" onmouseout="this.src='{$image_medium}'" alt="{$seo_alt_tag}">
 *
 * 주의: data-hover-src 속성이 없는 이미지는 hover 효과가 적용되지 않습니다.
 *       모바일/터치 환경에서는 동작하지 않습니다 (의도된 동작).
 */

(function () {
  'use strict';

  /* ── 설정 ── 여기만 바꾸세요 ───────────────────────── */
  var PRODUCT_IMG_SELECTOR = '.xans-product-listitem img[data-hover-src]';
  // 설명: 카페24 상품 목록 안에 있고 data-hover-src 속성이 있는 img만 선택
  // 카페24 상품 목록 클래스가 다를 경우 .xans-product-listitem 부분을 변경하세요.
  // 예: '.prd-list img[data-hover-src]' 또는 '.item-list img[data-hover-src]'

  var TRANSITION_DURATION = 200; // 이미지 전환 시 페이드 효과 시간 (ms, 0이면 즉시 전환)
  /* ─────────────────────────────────────────────────── */

  // 터치 기기 감지 (모바일에서는 hover 효과 비활성화)
  var isTouchDevice = (
    'ontouchstart' in window ||
    navigator.maxTouchPoints > 0 ||
    navigator.msMaxTouchPoints > 0
  );

  // 터치 기기면 아무것도 하지 않습니다
  if (isTouchDevice) {
    return;
  }

  // 페이지에 있는 모든 해당 이미지에 이벤트를 달아주는 함수
  function bindHoverEvents(imgElement) {
    var originalSrc = imgElement.getAttribute('src');     // 원래 이미지 URL 저장
    var hoverSrc    = imgElement.getAttribute('data-hover-src'); // hover 이미지 URL

    // hover 이미지가 없거나, 원본과 같으면 건너뜁니다
    if (!hoverSrc || hoverSrc === originalSrc) {
      return;
    }

    // CSS 전환 효과 설정 (부드러운 전환을 위해)
    if (TRANSITION_DURATION > 0) {
      imgElement.style.transition = 'opacity ' + TRANSITION_DURATION + 'ms ease';
    }

    // hover 이미지를 미리 불러옵니다 (실제 hover 시 느린 로딩 방지)
    var preloadImg   = new Image();
    preloadImg.src   = hoverSrc;
    var isPreloaded  = false; // 사전 로딩 완료 여부
    preloadImg.onload = function () {
      isPreloaded = true;
    };

    // 마우스가 이미지 위로 들어올 때
    imgElement.addEventListener('mouseenter', function () {
      if (!isPreloaded) {
        // 아직 로드 중이면 기다렸다가 교체
        preloadImg.onload = function () {
          isPreloaded = true;
          imgElement.src = hoverSrc;
        };
      } else {
        imgElement.src = hoverSrc; // 즉시 교체
      }
    });

    // 마우스가 이미지 밖으로 나올 때
    imgElement.addEventListener('mouseleave', function () {
      imgElement.src = originalSrc; // 원래 이미지로 복원
    });
  }

  // ── 초기 실행 ──────────────────────────────────────
  // DOM이 준비된 후 실행 (DOMContentLoaded)
  function init() {
    var images = document.querySelectorAll(PRODUCT_IMG_SELECTOR);

    // 찾은 이미지 개수 콘솔에 출력 (개발 확인용, 배포 시 삭제 가능)
    // console.log('[nk-product-hover] 감지된 이미지:', images.length);

    // 각 이미지에 hover 이벤트 부착
    for (var i = 0; i < images.length; i++) {
      bindHoverEvents(images[i]);
    }
  }

  // DOM 로드 상태 확인 후 실행
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    // 이미 DOM이 준비된 경우 (스크립트가 defer/async로 늦게 실행된 경우)
    init();
  }

  // ── 동적 상품 로딩 대응 (무한스크롤·AJAX 상품 추가 시) ──
  // 카페24 AJAX 상품 로딩 후 새로 추가된 이미지에도 이벤트를 달아줍니다.
  // MutationObserver: DOM 변화를 감지하는 브라우저 내장 기능
  if (typeof MutationObserver !== 'undefined') {
    var observer = new MutationObserver(function (mutations) {
      mutations.forEach(function (mutation) {
        // 새로 추가된 노드만 검사합니다
        mutation.addedNodes.forEach(function (node) {
          if (node.nodeType !== 1) return; // 텍스트 노드는 건너뜁니다

          // 새로 추가된 요소 자체가 해당 이미지인 경우
          if (node.matches && node.matches(PRODUCT_IMG_SELECTOR)) {
            bindHoverEvents(node);
          }

          // 새로 추가된 요소 안에 해당 이미지가 있는 경우
          var childImages = node.querySelectorAll ? node.querySelectorAll(PRODUCT_IMG_SELECTOR) : [];
          for (var i = 0; i < childImages.length; i++) {
            bindHoverEvents(childImages[i]);
          }
        });
      });
    });

    // 상품 목록이 있는 영역을 감시 대상으로 등록
    // (더 넓은 범위를 감시할수록 성능에 영향 → 가능하면 상품 목록 컨테이너만 지정)
    var productListContainer = document.querySelector('.xans-product-listitem')
                            || document.getElementById('contents')
                            || document.body;

    observer.observe(productListContainer, {
      childList: true,   // 직접 자식 노드 추가/삭제 감시
      subtree:   true    // 모든 하위 노드 변화 감시
    });
  }

})();
