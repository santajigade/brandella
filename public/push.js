// Brandella Journal: daily alerts opt in (max 1 notification per day)
// Non intrusive by design (Google Ad Experience Report safe):
// - nothing opens on its own; the prompt panel opens only after a click
// - a small bell sits in the empty page margin, only when the screen is wide
//   enough that it can never cover the article; otherwise only the footer link
// - closing (x or "No thanks") is remembered, so it never shows again
(function () {
  if (window.self !== window.top) return; // never inside the next-article iframes
  if (!('serviceWorker' in navigator) || !('PushManager' in window) || !('Notification' in window)) return;
  var store = {
    get: function (k) { try { return localStorage.getItem(k); } catch (e) { return null; } },
    set: function (k, v) { try { localStorage.setItem(k, v); } catch (e) {} },
  };
  function b64ToBytes(s) {
    s = s.trim(); var pad = '='.repeat((4 - s.length % 4) % 4);
    var raw = atob((s + pad).replace(/-/g, '+').replace(/_/g, '/'));
    var out = new Uint8Array(raw.length); for (var i = 0; i < raw.length; i++) out[i] = raw.charCodeAt(i); return out;
  }
  function subscribe() {
    return navigator.serviceWorker.register('/sw.js').then(function (reg) {
      return fetch('/push-key.txt', { cache: 'no-store' }).then(function (r) { return r.ok ? r.text() : Promise.reject('no key'); })
        .then(function (key) {
          return reg.pushManager.getSubscription().then(function (s) {
            return s || reg.pushManager.subscribe({ userVisibleOnly: true, applicationServerKey: b64ToBytes(key) });
          });
        });
    }).then(function (sub) {
      return fetch('/api/subscribe.php', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(sub) });
    }).then(function () { store.set('brj_push_sync', String(Date.now())); });
  }
  // Already allowed: re-save subscription once a week, show nothing
  if (Notification.permission === 'granted') {
    if (Date.now() - Number(store.get('brj_push_sync') || 0) > 7 * 864e5) subscribe().catch(function () {});
    return;
  }
  if (Notification.permission === 'denied') return;
  if (store.get('brj_push_off')) return; // visitor closed it once: remembered for good

  var BELL = '<svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true"><path fill="currentColor" d="M12 22a2.5 2.5 0 0 0 2.45-2h-4.9A2.5 2.5 0 0 0 12 22Zm7-6V11a7 7 0 0 0-5.5-6.84V3a1.5 1.5 0 0 0-3 0v1.16A7 7 0 0 0 5 11v5l-2 2v1h18v-1l-2-2Z"/></svg>';
  var dock, panel;
  function off() {
    store.set('brj_push_off', String(Date.now()));
    if (panel) panel.remove();
    if (dock) dock.remove();
    document.querySelectorAll('.push-open').forEach(function (b) { b.remove(); });
  }
  function closePanel() { if (panel) { panel.remove(); panel = null; } }
  function openPanel(anchor) {
    if (panel) return;
    panel = document.createElement('div');
    panel.className = 'push-panel';
    panel.setAttribute('role', 'dialog');
    panel.setAttribute('aria-label', 'Daily alerts');
    panel.innerHTML = '<strong>One top SEO and marketing update a day</strong><p>One alert a day. No spam. Turn off anytime.</p><div class="push-btns"><button type="button" class="push-later">No thanks</button><button type="button" class="push-allow">Allow</button></div>';
    // Opened from the footer link: show it inline in the footer, never over the page
    if (anchor && anchor.closest('.site-footer')) { panel.classList.add('inline'); anchor.insertAdjacentElement('afterend', panel); }
    else document.body.appendChild(panel);
    panel.querySelector('.push-later').onclick = off;
    panel.querySelector('.push-allow').onclick = function () {
      Notification.requestPermission().then(function (p) {
        if (p === 'granted') { subscribe().catch(function () {}); off(); }
        else if (p === 'denied') off();
        else closePanel();
      });
    };
  }
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') closePanel(); });

  function init() {
    // Footer link (all screen sizes): click only
    var slot = document.querySelector('.footer-bottom-in span:last-child');
    if (slot) {
      var link = document.createElement('button');
      link.type = 'button'; link.className = 'push-open'; link.textContent = 'Daily alerts';
      link.onclick = function () { openPanel(link); };
      slot.appendChild(link);
    }
    // Margin bell: only shown by CSS on wide screens with a free side margin
    dock = document.createElement('div');
    dock.className = 'push-dock';
    dock.innerHTML = '<button type="button" class="push-bell" aria-label="Get daily alerts" title="Get daily alerts">' + BELL + '</button><button type="button" class="push-x" aria-label="Hide alerts button">&times;</button>';
    dock.querySelector('.push-bell').onclick = function () { panel ? closePanel() : openPanel(null); };
    dock.querySelector('.push-x').onclick = off;
    document.body.appendChild(dock);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
