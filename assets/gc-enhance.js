/* Alexanarch view-count + browse enhancement v2 (TACHYON, 2026-07-16).
 *
 * v1 fetched a per-record GoatCounter API call from the browser on every
 * page load and thundering-herd'd the public counter endpoint, producing
 * em-dashes under load. v2 fetches ONE static snapshot per session
 * (data/view-counts.json, refreshed every 6 hours by the goatcounter-snapshot
 * GitHub Action) and does O(1) local lookups per record.
 *
 * The tracker script (count.js on every page) is unchanged; GoatCounter
 * keeps accumulating the underlying data. Only the display path was
 * broken; only the display path is replaced.
 *
 * Epistemics of a counter, snapshot edition:
 *   Snapshot has a path with a numeric count -> display the count.
 *   Snapshot is missing the path -> display em-dash. In the snapshot
 *     pattern, "missing" collapses three prior states — no observations
 *     yet, snapshot lag, path never tracked — into one honest uncertainty
 *     signal. The v1 200/404 distinction bought a display of "0 views"
 *     for genuine zeros at the cost of the thundering-herd; the snapshot
 *     buys reliability at the cost of that specific distinction. A record
 *     that has been tracked for months and legitimately has zero views
 *     will show em-dash; that is the trade.
 *   Snapshot fetch fails at runtime -> display em-dash; fall back to any
 *     cached snapshot from localStorage. Never displays 0 under uncertainty.
 *   Special path 'TOTAL' -> snapshot.total (all-time site total from
 *     goatcounter /api/v0/stats/total).
 */
(function () {
  'use strict';
  var SNAPSHOT_URL = '/data/view-counts.json';
  var CACHE_KEY = 'gc:snapshot:v2';
  var TTL = 6 * 3600 * 1000;  // 6h — matches the Action's cadence
  var snapshotPromise = null;

  function fmt(n) { return String(n).replace(/\B(?=(\d{3})+(?!\d))/g, ','); }
  function show(el, count, suffix) {
    el.textContent = fmt(count) + ' ' + (suffix || (count === 1 ? 'view' : 'views'));
    el.removeAttribute('title');
  }
  function showUnavailable(el) {
    if (!/^\d/.test(el.textContent)) {
      el.textContent = '\u2014';
      el.title = 'view count temporarily unavailable';
    }
  }

  function loadSnapshot() {
    if (snapshotPromise) return snapshotPromise;
    snapshotPromise = new Promise(function (resolve) {
      // 1. Try localStorage cache
      var cached = null;
      try {
        var raw = localStorage.getItem(CACHE_KEY);
        if (raw) {
          var c = JSON.parse(raw);
          if (c && c.d && (Date.now() - c.t) < TTL) cached = c.d;
        }
      } catch (e) {}
      if (cached) { resolve(cached); return; }

      // 2. Fetch fresh
      var x = new XMLHttpRequest();
      x.open('GET', SNAPSHOT_URL);
      x.timeout = 10000;
      x.onload = function () {
        if (x.status === 200) {
          try {
            var d = JSON.parse(x.responseText);
            try { localStorage.setItem(CACHE_KEY, JSON.stringify({ d: d, t: Date.now() })); } catch (e) {}
            resolve(d);
          } catch (e) { resolve(null); }
        } else {
          // Try stale localStorage as last resort before giving up
          try {
            var stale = localStorage.getItem(CACHE_KEY);
            if (stale) { var s = JSON.parse(stale); if (s && s.d) return resolve(s.d); }
          } catch (e) {}
          resolve(null);
        }
      };
      x.onerror = x.ontimeout = function () {
        try {
          var stale = localStorage.getItem(CACHE_KEY);
          if (stale) { var s = JSON.parse(stale); if (s && s.d) return resolve(s.d); }
        } catch (e) {}
        resolve(null);
      };
      x.send();
    });
    return snapshotPromise;
  }

  function renderOne(el, snapshot, suffix) {
    if (!snapshot) return showUnavailable(el);
    var path = el.getAttribute('data-gc');
    if (path === 'TOTAL') {
      if (typeof snapshot.total === 'number') show(el, snapshot.total, suffix || 'views site-wide');
      else showUnavailable(el);
      return;
    }
    var entry = snapshot.paths && snapshot.paths[path];
    if (entry && typeof entry.count === 'number') show(el, entry.count, suffix);
    else showUnavailable(el);
  }

  function renderAll(snapshot) {
    document.querySelectorAll('.gc-v[data-gc]').forEach(function (el) {
      renderOne(el, snapshot);
    });
    var tot = document.getElementById('home-views') || document.getElementById('site-views');
    if (tot) {
      tot.setAttribute('data-gc', 'TOTAL');
      tot.classList.add('gc-v');
      renderOne(tot, snapshot, 'views site-wide');
    }
  }

  function init() {
    // Pre-mark any elements that don't have counts yet with em-dash rather
    // than "0 views" or empty text; renderAll will replace with real value
    // once the snapshot loads.
    document.querySelectorAll('.gc-v[data-gc]').forEach(function (el) {
      if (!/\d/.test(el.textContent) || el.textContent.trim() === '0 views') {
        el.textContent = '\u2014';
      }
    });

    // Browse-surface enhancement: add counter spans to record rows + wire
    // date sort. Same logic as v1; only the count SOURCE changed.
    var rows = Array.prototype.slice.call(
      document.querySelectorAll('a[itemscope][href^="/s/records/"]'));
    if (rows.length >= 10) {
      rows.forEach(function (row) {
        var line = row.querySelector('div');
        var m = row.getAttribute('href').match(/\/s\/records\/(\d+)\//);
        if (!line || !m) return;
        var sp = document.createElement('span');
        sp.className = 'gc-v';
        sp.setAttribute('data-gc', '/s/records/' + m[1] + '/');
        sp.style.cssText = 'font-size:.72em;color:var(--teal);white-space:nowrap;min-width:52px;text-align:right';
        sp.textContent = '\u2014';
        line.appendChild(sp);
      });

      var hdr = document.getElementById('browse-meta') ||
        (function () {
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
          return ka.n - kb.n;
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
        }
      }
      apply('newest');
    }

    // One snapshot fetch, apply everywhere.
    loadSnapshot().then(renderAll);
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
