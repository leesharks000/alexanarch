/* Network-wide witness counter for the Alexanarch site network.
 *
 * Any site in the network can render the network-wide view total by:
 *   1. Including this script from alexanarch.org:
 *      <script src="https://www.alexanarch.org/assets/network-witness.js" async></script>
 *   2. Placing an empty element with the trigger attribute:
 *      <span data-alexanarch-network-total></span>
 *
 * The element's text is set to the formatted network total (e.g. "1,234,567
 * network views") or em-dash under uncertainty. Prefix/suffix strings can be
 * customized via attributes:
 *      <span data-alexanarch-network-total
 *            data-suffix="witnesses across the network"
 *            data-prefix=""></span>
 *
 * Source of truth: https://www.alexanarch.org/data/network-witness.json,
 * refreshed every 6 hours by the goatcounter-snapshot GitHub Action. This
 * module fetches once per session with a 6-hour localStorage cache.
 *
 * Never displays 0 under uncertainty. Fetch failure or missing data ->
 * em-dash. Stale cache is preferred over em-dash if fresh fetch fails.
 */
(function () {
  'use strict';
  var URL = 'https://www.alexanarch.org/data/network-witness.json';
  var CACHE_KEY = 'nw:witness:v1';
  var TTL = 6 * 3600 * 1000;

  function fmt(n) { return String(n).replace(/\B(?=(\d{3})+(?!\d))/g, ','); }

  function render(el, data) {
    var n = data && data.network_total;
    var suffix = el.getAttribute('data-suffix') || 'network views';
    var prefix = el.getAttribute('data-prefix') || '';
    if (typeof n === 'number' && !isNaN(n)) {
      el.textContent = prefix + fmt(n) + ' ' + suffix;
      el.removeAttribute('title');
    } else {
      el.textContent = '\u2014';
      el.title = 'network view count temporarily unavailable';
    }
  }

  function targets() {
    return Array.prototype.slice.call(
      document.querySelectorAll('[data-alexanarch-network-total]'));
  }

  function readCache() {
    try {
      var raw = localStorage.getItem(CACHE_KEY);
      if (!raw) return null;
      var c = JSON.parse(raw);
      if (!c || !c.d) return null;
      c.fresh = (Date.now() - c.t) < TTL;
      return c;
    } catch (e) { return null; }
  }
  function writeCache(d) {
    try { localStorage.setItem(CACHE_KEY, JSON.stringify({ d: d, t: Date.now() })); } catch (e) {}
  }

  function loadAndRender() {
    var els = targets();
    if (!els.length) return;

    var cache = readCache();
    if (cache && cache.fresh) {
      els.forEach(function (el) { render(el, cache.d); });
      return;
    }

    var x = new XMLHttpRequest();
    x.open('GET', URL);
    x.timeout = 10000;
    x.onload = function () {
      if (x.status === 200) {
        try {
          var d = JSON.parse(x.responseText);
          writeCache(d);
          els.forEach(function (el) { render(el, d); });
          return;
        } catch (e) { /* fall through to stale/null */ }
      }
      // Fetch failed / non-200: use stale cache if we have it, else null
      els.forEach(function (el) { render(el, cache ? cache.d : null); });
    };
    x.onerror = x.ontimeout = function () {
      els.forEach(function (el) { render(el, cache ? cache.d : null); });
    };
    x.send();
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', loadAndRender);
  else loadAndRender();
})();
