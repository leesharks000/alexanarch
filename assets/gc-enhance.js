/* Alexanarch view-count + browse enhancement (TACHYON, 2026-07-12).
 *
 * Epistemics of a counter (the whole reason this file exists):
 *   HTTP 200  -> a count. Display it, cache it.
 *   HTTP 404  -> a true zero (GoatCounter has no pageviews for the path).
 *                Display "0 views" honestly.
 *   429/5xx/network -> NOT AN ANSWER. Never display 0. Show the cached
 *                value if one exists, else an em dash. A rate limit must
 *                never testify that a record is unread.
 *
 * Also: localStorage cache (6h fresh, stale-while-revalidate), a fetch
 * queue throttled under GoatCounter's public counter rate limit, lazy
 * loading via IntersectionObserver, client-side date sorting for the
 * static browse surface, and the site-wide TOTAL counter.
 */
(function () {
  'use strict';
  var HOST = 'https://alexanarch.goatcounter.com';
  var TTL = 6 * 3600 * 1000;           // cache freshness window
  var GAP = 340;                        // ms between counter fetches (~3/s)

  function cacheGet(path) {
    try { var v = JSON.parse(localStorage.getItem('gcv:' + path)); return v && typeof v.c !== 'undefined' ? v : null; }
    catch (e) { return null; }
  }
  function cacheSet(path, count) {
    try { localStorage.setItem('gcv:' + path, JSON.stringify({ c: count, t: Date.now() })); } catch (e) {}
  }
  function fmt(n) { return String(n).replace(/\B(?=(\d{3})+(?!\d))/g, ','); }
  function show(el, count, suffix) {
    el.textContent = fmt(count) + ' ' + (suffix || (count === 1 || count === '1' ? 'view' : 'views'));
    el.removeAttribute('title');
  }
  function showUnavailable(el) {
    if (!el.textContent || el.textContent === '\u2014' || /^0 views$/.test(el.textContent)) {
      el.textContent = '\u2014';
      el.title = 'view count temporarily unavailable';
    } // else: keep whatever (cached) value is already displayed
  }

  // ── throttled fetch queue ──────────────────────────────────────────────
  var queue = [], draining = false, seen = {};
  function enqueue(path, el, suffix) {
    var key = path + '|' + (suffix || '');
    if (seen[key]) return; seen[key] = 1;
    var c = cacheGet(path);
    if (c) { show(el, c.c, suffix); if (Date.now() - c.t < TTL) return; } // fresh: done; stale: revalidate below
    queue.push({ path: path, el: el, suffix: suffix });
    drain();
  }
  function drain() {
    if (draining) return; draining = true;
    (function step() {
      var job = queue.shift();
      if (!job) { draining = false; return; }
      var x = new XMLHttpRequest();
      x.open('GET', HOST + '/counter/' + encodeURIComponent(job.path) + '.json');
      x.timeout = 8000;
      x.onload = function () {
        if (x.status === 200) {
          try {
            var d = JSON.parse(x.responseText);
            var n = parseInt(String(d.count).replace(/[^\d]/g, ''), 10);
            if (!isNaN(n)) { cacheSet(job.path, n); show(job.el, n, job.suffix); }
            else showUnavailable(job.el);
          } catch (e) { showUnavailable(job.el); }
        } else if (x.status === 404) {
          cacheSet(job.path, 0); show(job.el, 0, job.suffix);   // true zero
        } else {
          showUnavailable(job.el);                               // 429/5xx: not an answer
        }
        setTimeout(step, GAP);
      };
      x.onerror = x.ontimeout = function () { showUnavailable(job.el); setTimeout(step, GAP); };
      x.send();
    })();
  }

  // ── lazy loading: fetch only when visible ─────────────────────────────
  var io = ('IntersectionObserver' in window) ? new IntersectionObserver(function (entries) {
    entries.forEach(function (en) {
      if (en.isIntersecting) {
        io.unobserve(en.target);
        enqueue(en.target.getAttribute('data-gc'), en.target);
      }
    });
  }, { rootMargin: '200px' }) : null;
  function watch(el) { if (io) io.observe(el); else enqueue(el.getAttribute('data-gc'), el); }

  function init() {
    // 1. Upgrade any pre-existing counter elements (homepage cards).
    document.querySelectorAll('.gc-v[data-gc]').forEach(function (el) {
      if (!/\d/.test(el.textContent) || el.textContent.trim() === '0 views') el.textContent = '\u2014';
      watch(el);
    });

    // 2. Site-wide total (GoatCounter special TOTAL path).
    var tot = document.getElementById('home-views') || document.getElementById('site-views');
    if (tot) enqueue('TOTAL', tot, 'views site-wide');

    // 3. Browse surface: per-record counters + date sorting.
    var rows = Array.prototype.slice.call(
      document.querySelectorAll('a[itemscope][href^="/s/records/"]'));
    if (rows.length < 10) return;                      // not the browse page

    rows.forEach(function (row) {
      var line = row.querySelector('div');             // the flex line
      var m = row.getAttribute('href').match(/\/s\/records\/(\d+)\//);
      if (!line || !m) return;
      var sp = document.createElement('span');
      sp.className = 'gc-v';
      sp.setAttribute('data-gc', '/s/records/' + m[1] + '/');
      sp.style.cssText = 'font-size:.72em;color:var(--teal);white-space:nowrap;min-width:52px;text-align:right';
      sp.textContent = '';
      line.appendChild(sp);
      watch(sp);
    });

    var hdr = document.getElementById('browse-meta') ||
      (function () {                                   // fallback: the "deposits · sorted by" line
        var ds = document.querySelectorAll('div');
        for (var i = 0; i < ds.length; i++)
          if (/deposits\s*·\s*sorted/.test(ds[i].textContent) && ds[i].children.length < 3) return ds[i];
        return null;
      })();

    var parent = rows[0].parentNode;
    var anchor = document.createComment('gc-rows');
    parent.insertBefore(anchor, rows[0]);

    function key(row) {
      var t = row.querySelector('time[datetime]');
      var m2 = row.getAttribute('href').match(/(\d+)/);
      return { d: t ? t.getAttribute('datetime') : '', n: m2 ? parseInt(m2[1], 10) : 0 };
    }
    function apply(mode) {
      var sorted = rows.slice().sort(function (a, b) {
        var ka = key(a), kb = key(b);
        if (mode === 'newest') return (kb.d > ka.d ? 1 : kb.d < ka.d ? -1 : kb.n - ka.n);
        if (mode === 'oldest') return (ka.d > kb.d ? 1 : ka.d < kb.d ? -1 : ka.n - kb.n);
        return ka.n - kb.n;                            // by number
      });
      var last = anchor;
      sorted.forEach(function (r) { parent.insertBefore(r, last.nextSibling); last = r; });
      if (hdr) {
        var label = { newest: 'sorted by date, newest first', oldest: 'sorted by date, oldest first', number: 'sorted by deposit number' }[mode];
        var totSpan = hdr.querySelector('#site-views');
        hdr.innerHTML = rows.length + ' deposits · ' + label + ' · sort: ' +
          '<a href="#" data-sort="newest" style="color:var(--teal)">newest</a> · ' +
          '<a href="#" data-sort="oldest" style="color:var(--teal)">oldest</a> · ' +
          '<a href="#" data-sort="number" style="color:var(--teal)">by №</a>' +
          ' · <span id="site-views">' + (totSpan ? totSpan.textContent : '\u2014') + '</span>';
        hdr.querySelectorAll('a[data-sort]').forEach(function (a) {
          a.onclick = function (ev) { ev.preventDefault(); apply(a.getAttribute('data-sort')); };
        });
        enqueue('TOTAL', hdr.querySelector('#site-views'), 'views site-wide');
      }
    }
    apply('newest');                                   // date order by default
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
