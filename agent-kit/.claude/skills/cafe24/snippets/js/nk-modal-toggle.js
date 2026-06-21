/*!
 * nk-modal-toggle — 모달 열기/닫기 (ESC 키 + 오버레이 클릭 + 닫기 버튼)
 * 사용처: nk-modal-system.css 와 함께 사용 (모든 모달·팝업)
 * 의존성: 없음 (Vanilla JS, ES6+)
 *
 * 비코더 사용법:
 *   1. SFTP로 _nk/js/ 폴더에 업로드
 *   2. layout.html 의 </body> 직전에 <script src="/_nk/js/nk-modal-toggle.js" defer></script>
 *   3. 모달 HTML 구조 (자세한 건 nk-modal-system.css 참고):
 *      <div class="nk-modal" id="my-modal" role="dialog" aria-modal="true" hidden>...</div>
 *
 *   4. 열기 버튼:
 *      <button data-nk-modal-open="my-modal">상품 보기</button>
 *
 *   5. 닫기 (자동 처리):
 *      - 닫기 버튼: data-nk-modal-close 속성
 *      - 오버레이 클릭: .nk-modal-overlay 또는 data-nk-modal-close
 *      - ESC 키: 자동 처리
 *
 *   6. JS에서 직접 제어:
 *      nkModal.open('my-modal');
 *      nkModal.close('my-modal');
 *      nkModal.closeAll();
 *
 * 접근성:
 *   - 모달 열릴 때 첫 포커스 가능 요소로 자동 포커스
 *   - 모달 닫힐 때 열기 버튼으로 포커스 복귀
 *   - Tab 키 트랩 (모달 안에서만 순환)
 */

(function () {
  'use strict';

  let lastTrigger = null; // 모달 닫힐 때 복귀할 요소

  function getFocusable(modal) {
    return modal.querySelectorAll(
      'button:not(:disabled), [href], input:not(:disabled), select:not(:disabled), textarea:not(:disabled), [tabindex]:not([tabindex="-1"])'
    );
  }

  function openModal(id) {
    const modal = document.getElementById(id);
    if (!modal || !modal.classList.contains('nk-modal')) return;

    lastTrigger = document.activeElement;
    modal.hidden = false;
    document.body.classList.add('nk-modal-open');

    // 첫 포커스 가능 요소로 포커스
    const focusable = getFocusable(modal);
    if (focusable.length > 0) {
      // 닫기 버튼 말고 본문의 첫 요소로 (UX 좋음)
      const closeBtn = modal.querySelector('.nk-modal-close');
      const first = Array.from(focusable).find((el) => el !== closeBtn) || focusable[0];
      first.focus({ preventScroll: true });
    }

    modal.dispatchEvent(new CustomEvent('nk:modal:open', { bubbles: true }));
  }

  function closeModal(id) {
    const modal = id ? document.getElementById(id) : document.querySelector('.nk-modal:not([hidden])');
    if (!modal || !modal.classList.contains('nk-modal')) return;

    modal.hidden = true;

    // 다른 열린 모달이 없으면 body 스크롤 잠금 해제
    if (!document.querySelector('.nk-modal:not([hidden])')) {
      document.body.classList.remove('nk-modal-open');
    }

    // 트리거 버튼으로 포커스 복귀
    if (lastTrigger && typeof lastTrigger.focus === 'function') {
      lastTrigger.focus({ preventScroll: true });
      lastTrigger = null;
    }

    modal.dispatchEvent(new CustomEvent('nk:modal:close', { bubbles: true }));
  }

  function closeAll() {
    document.querySelectorAll('.nk-modal:not([hidden])').forEach((m) => closeModal(m.id));
  }

  // 클릭 이벤트 위임
  document.addEventListener('click', (e) => {
    // 열기 버튼
    const openBtn = e.target.closest('[data-nk-modal-open]');
    if (openBtn) {
      e.preventDefault();
      openModal(openBtn.dataset.nkModalOpen);
      return;
    }

    // 닫기 (버튼 + 오버레이)
    const closeBtn = e.target.closest('[data-nk-modal-close]');
    if (closeBtn) {
      e.preventDefault();
      const modal = closeBtn.closest('.nk-modal');
      closeModal(modal ? modal.id : null);
    }
  });

  // ESC 키 닫기 + Tab 트랩
  document.addEventListener('keydown', (e) => {
    const openModalEl = document.querySelector('.nk-modal:not([hidden])');
    if (!openModalEl) return;

    if (e.key === 'Escape') {
      e.preventDefault();
      closeModal(openModalEl.id);
      return;
    }

    if (e.key === 'Tab') {
      const focusable = getFocusable(openModalEl);
      if (focusable.length === 0) return;
      const first = focusable[0];
      const last = focusable[focusable.length - 1];

      if (e.shiftKey && document.activeElement === first) {
        e.preventDefault();
        last.focus();
      } else if (!e.shiftKey && document.activeElement === last) {
        e.preventDefault();
        first.focus();
      }
    }
  });

  // 전역 API
  window.nkModal = {
    open: openModal,
    close: closeModal,
    closeAll: closeAll,
  };
})();
