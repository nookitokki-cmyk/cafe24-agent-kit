/**
 * nk-guide-tabs.js — shopinfo/guide.html 탭 전환 (vanilla, mall_faq module 보존)
 * .nk-tabs__nav [data-nk-tab] 클릭 → .nk-tabs__panel 단일 노출 · hash(#payment 등) 딥링크 지원
 */
(function () {
  var root = document.querySelector('.nk-etc-guide__tabs');
  if (!root) return;

  var nav = root.querySelector('.nk-tabs__nav');
  if (!nav) return;

  var tabs = nav.querySelectorAll('[data-nk-tab]');
  var panels = root.querySelectorAll('.nk-tabs__panel');
  var tabIds = ['member', 'order', 'payment', 'delivery', 'change', 'refund', 'etc'];

  function activate(id) {
    if (tabIds.indexOf(id) === -1) id = 'member';

    tabs.forEach(function (tab) {
      var active = tab.getAttribute('data-nk-tab') === id;
      var item = tab.parentElement;
      if (item) item.classList.toggle('is-active', active);
      tab.setAttribute('aria-selected', active ? 'true' : 'false');
      tab.tabIndex = active ? 0 : -1;
    });

    panels.forEach(function (panel) {
      var active = panel.id === id;
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
    var idx = tabIds.indexOf(current.getAttribute('data-nk-tab'));
    if (idx === -1) return;

    var next = -1;
    if (e.key === 'ArrowRight') next = (idx + 1) % tabIds.length;
    else if (e.key === 'ArrowLeft') next = (idx - 1 + tabIds.length) % tabIds.length;
    else if (e.key === 'Home') next = 0;
    else if (e.key === 'End') next = tabIds.length - 1;
    else return;

    e.preventDefault();
    var target = nav.querySelector('[data-nk-tab="' + tabIds[next] + '"]');
    if (target) {
      target.focus();
      activate(tabIds[next]);
      if (history.replaceState) {
        history.replaceState(null, '', '#' + tabIds[next]);
      }
    }
  });

  var hash = (location.hash || '').replace(/^#/, '');
  activate(tabIds.indexOf(hash) !== -1 ? hash : 'member');
})();
