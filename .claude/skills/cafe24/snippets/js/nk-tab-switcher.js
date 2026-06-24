/*!
 * nk-tab-switcher — 탭 메뉴 전환 (접근성 준수, 키보드 화살표 네비게이션)
 * 사용처: 상품 상세 페이지의 "상세정보·리뷰·Q&A·배송", 마이페이지 카테고리 등
 * 의존성: 없음 (Vanilla JS, ES6+)
 *
 * 비코더 사용법:
 *   1. SFTP로 _nk/js/ 폴더에 업로드
 *   2. layout.html 의 </body> 직전에 <script src="/_nk/js/nk-tab-switcher.js" defer></script>
 *   3. HTML 구조 (WAI-ARIA 탭 패턴):
 *      <div class="nk-tabs" data-nk-tabs>
 *        <div class="nk-tab-list" role="tablist">
 *          <button role="tab" class="nk-tab is-active" aria-controls="panel-1" aria-selected="true" id="tab-1">상세정보</button>
 *          <button role="tab" class="nk-tab"           aria-controls="panel-2" aria-selected="false" id="tab-2" tabindex="-1">리뷰</button>
 *          <button role="tab" class="nk-tab"           aria-controls="panel-3" aria-selected="false" id="tab-3" tabindex="-1">Q&A</button>
 *        </div>
 *        <div role="tabpanel" id="panel-1" aria-labelledby="tab-1">상세정보 내용...</div>
 *        <div role="tabpanel" id="panel-2" aria-labelledby="tab-2" hidden>리뷰 내용...</div>
 *        <div role="tabpanel" id="panel-3" aria-labelledby="tab-3" hidden>Q&A 내용...</div>
 *      </div>
 *
 *   4. CSS도 함께 (간단 버전):
 *      .nk-tab-list { display:flex; border-bottom:1px solid var(--nk-color-border); }
 *      .nk-tab { padding:12px 20px; background:transparent; border:0; cursor:pointer;
 *                color:var(--nk-color-text-sub); font-family:inherit; font-size:14px; }
 *      .nk-tab.is-active { color:var(--nk-color-text); font-weight:700;
 *                          border-bottom:2px solid var(--nk-color-accent); }
 *
 * 키보드 단축키:
 *   - ←/→ : 이전/다음 탭
 *   - Home/End : 첫/마지막 탭
 *   - Enter/Space : 활성화 (포커스 시 자동 활성화도 옵션)
 */

(function () {
  'use strict';

  function initTabs(root) {
    const list = root.querySelector('[role="tablist"]');
    if (!list) return;
    const tabs = Array.from(list.querySelectorAll('[role="tab"]'));
    if (tabs.length === 0) return;

    function activate(tab, setFocus = true) {
      tabs.forEach((t) => {
        const isActive = t === tab;
        t.classList.toggle('is-active', isActive);
        t.setAttribute('aria-selected', isActive ? 'true' : 'false');
        t.setAttribute('tabindex', isActive ? '0' : '-1');

        const panelId = t.getAttribute('aria-controls');
        if (panelId) {
          const panel = document.getElementById(panelId);
          if (panel) panel.hidden = !isActive;
        }
      });
      if (setFocus) tab.focus();

      root.dispatchEvent(new CustomEvent('nk:tab:change', {
        bubbles: true,
        detail: { tab, id: tab.id },
      }));
    }

    // 클릭으로 활성화
    tabs.forEach((tab) => {
      tab.addEventListener('click', (e) => {
        e.preventDefault();
        activate(tab, false);
      });
    });

    // 키보드 네비게이션
    list.addEventListener('keydown', (e) => {
      const currentIdx = tabs.indexOf(document.activeElement);
      if (currentIdx === -1) return;

      let targetIdx = -1;
      switch (e.key) {
        case 'ArrowRight':
          targetIdx = (currentIdx + 1) % tabs.length;
          break;
        case 'ArrowLeft':
          targetIdx = (currentIdx - 1 + tabs.length) % tabs.length;
          break;
        case 'Home':
          targetIdx = 0;
          break;
        case 'End':
          targetIdx = tabs.length - 1;
          break;
        default:
          return;
      }
      e.preventDefault();
      activate(tabs[targetIdx], true);
    });
  }

  // 초기화
  document.querySelectorAll('[data-nk-tabs]').forEach(initTabs);

  // 동적으로 추가되는 탭 지원
  window.nkTabs = {
    init: initTabs,
  };
})();
