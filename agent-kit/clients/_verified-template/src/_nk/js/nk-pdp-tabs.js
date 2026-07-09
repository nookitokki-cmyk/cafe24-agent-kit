/**
 * nk-pdp-tabs.js — PDP 상세정보 탭 전환 (앵커 점프 → 단일 패널 노출)
 * .nk-pdp__tabs-bar [data-nk-tab] 클릭 → #prdDetail/#prdInfo/#prdReview/#prdQnA/#prdRelated 단일 노출
 */
(function () {
  var root = document.querySelector('.nk-pdp');
  if (!root) return;

  var nav = root.querySelector('.nk-pdp__tabs-bar .nk-tabs__nav');
  if (!nav) return;

  var tabIds = ['prdDetail', 'prdInfo', 'prdReview', 'prdQnA', 'prdRelated'];

  function panelFor(id) {
    return document.getElementById(id);
  }

  function isTabAvailable(id) {
    var tab = nav.querySelector('[data-nk-tab="' + id + '"]');
    if (!tab) return false;
    var item = tab.parentElement;
    if (item && item.classList.contains('displaynone')) return false;
    var panel = panelFor(id);
    if (!panel) return false;
    return !panel.classList.contains('displaynone');
  }

  function visibleTabIds() {
    return tabIds.filter(isTabAvailable);
  }

  function activate(id) {
    var visible = visibleTabIds();
    if (visible.indexOf(id) === -1) id = visible[0] || 'prdDetail';

    nav.querySelectorAll('[data-nk-tab]').forEach(function (tab) {
      var tid = tab.getAttribute('data-nk-tab');
      var active = tid === id;
      var item = tab.parentElement;
      if (item) item.classList.toggle('is-active', active);
      tab.setAttribute('aria-selected', active ? 'true' : 'false');
      tab.tabIndex = active ? 0 : -1;
    });

    tabIds.forEach(function (pid) {
      var panel = panelFor(pid);
      if (!panel) return;
      var active = pid === id;
      panel.classList.toggle('is-active', active);
      if (active) {
        panel.removeAttribute('hidden');
      } else {
        panel.setAttribute('hidden', '');
      }
    });
  }

  nav.addEventListener('click', function (e) {
    var tab = e.target.closest('[data-nk-tab]');
    if (!tab) return;
    e.preventDefault();
    var id = tab.getAttribute('data-nk-tab');
    activate(id);
    if (history.replaceState) {
      history.replaceState(null, '', '#' + id);
    } else {
      location.hash = id;
    }
  });

  nav.addEventListener('keydown', function (e) {
    var current = nav.querySelector('[data-nk-tab][aria-selected="true"]');
    if (!current) return;
    var visible = visibleTabIds();
    var idx = visible.indexOf(current.getAttribute('data-nk-tab'));
    if (idx === -1) return;

    var next = -1;
    if (e.key === 'ArrowRight') next = (idx + 1) % visible.length;
    else if (e.key === 'ArrowLeft') next = (idx - 1 + visible.length) % visible.length;
    else if (e.key === 'Home') next = 0;
    else if (e.key === 'End') next = visible.length - 1;
    else return;

    e.preventDefault();
    var targetId = visible[next];
    var target = nav.querySelector('[data-nk-tab="' + targetId + '"]');
    if (target) {
      target.focus();
      activate(targetId);
      if (history.replaceState) {
        history.replaceState(null, '', '#' + targetId);
      }
    }
  });

  var hash = (location.hash || '').replace(/^#/, '');
  activate(tabIds.indexOf(hash) !== -1 && isTabAvailable(hash) ? hash : 'prdDetail');
})();
