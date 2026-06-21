/*!
 * nk-scroll-animation — 스크롤 시 요소 페이드인 (IntersectionObserver 기반)
 * 사용처: 메인 페이지의 섹션 등장 애니메이션, 카드 그리드 페이드인
 * 의존성: 없음 (Vanilla JS, ES6+). 폴리필 없이 모든 현대 브라우저 동작.
 *
 * 비코더 사용법:
 *   1. SFTP로 _nk/js/ 폴더에 업로드
 *   2. layout.html 의 </body> 직전에 <script src="/_nk/js/nk-scroll-animation.js" defer></script>
 *   3. HTML에서 애니메이션할 요소에 클래스 추가:
 *      <section class="nk-fade-in">...</section>
 *      <div class="nk-fade-in" data-nk-delay="200">...</div>   ← 200ms 지연
 *      <div class="nk-fade-in" data-nk-direction="left">...</div>  ← 왼쪽에서 슬라이드인
 *
 *   4. CSS도 함께 (이미 있으면 생략):
 *      .nk-fade-in { opacity: 0; transform: translateY(20px); transition: opacity .6s, transform .6s; }
 *      .nk-fade-in.is-visible { opacity: 1; transform: translateY(0); }
 *      .nk-fade-in[data-nk-direction="left"] { transform: translateX(-30px); }
 *      .nk-fade-in[data-nk-direction="left"].is-visible { transform: translateX(0); }
 *
 * 접근성: prefers-reduced-motion 자동 감지 → 애니메이션 건너뛰고 즉시 표시
 */

(function () {
  'use strict';

  // 모션 줄이기 설정 감지
  const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // 타깃 요소 수집 (이미 표시된 것 포함 → CSS 의존 안 함)
  const targets = document.querySelectorAll('.nk-fade-in:not(.is-visible)');
  if (targets.length === 0) return;

  // 모션 줄이기: 모두 즉시 표시
  if (prefersReducedMotion) {
    targets.forEach((el) => el.classList.add('is-visible'));
    return;
  }

  // IntersectionObserver 미지원 브라우저 → 즉시 표시
  if (!('IntersectionObserver' in window)) {
    targets.forEach((el) => el.classList.add('is-visible'));
    return;
  }

  // 옵저버 설정
  const observer = new IntersectionObserver(
    (entries, obs) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        const el = entry.target;
        const delay = parseInt(el.dataset.nkDelay, 10) || 0;

        if (delay > 0) {
          setTimeout(() => el.classList.add('is-visible'), delay);
        } else {
          el.classList.add('is-visible');
        }

        // 한 번만 등장 (성능 + 자연스러운 UX)
        obs.unobserve(el);
      });
    },
    {
      root: null,
      // 화면 하단에서 80px 위로 들어오면 트리거 (너무 일찍 시작 방지)
      rootMargin: '0px 0px -80px 0px',
      threshold: 0,
    }
  );

  targets.forEach((el) => observer.observe(el));

  // 페이지 로드 후 늦게 삽입되는 요소 지원 (ajax 등)
  window.nkScrollAnimation = {
    observe(elements) {
      const els = elements instanceof NodeList ? elements : [elements];
      els.forEach((el) => {
        if (!el.classList.contains('is-visible')) observer.observe(el);
      });
    },
  };
})();
