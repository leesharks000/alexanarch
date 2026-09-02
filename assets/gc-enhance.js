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
  var CACHE_KEY = 'gc:snapshot:v3'; // v3 2026-09-02: bumped so browsers drop the cached 100-path, one-week snapshot
  var TTL = 6 * 3600 * 1000;  // 6h — matches the Action's cadence
  var snapshotPromise = null;

  function fmt(n) { return String(n).replace(/\B(?=(\d{3})+(?!\d))/g, ','); }
  function show(el, count, suffix) {
    el.textContent = fmt(count) + ' ' + (suffix || (count === 1 ? 'visitor' : 'visitors'));
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

  /* Trailing-slash normalisation (2026-08-12, found by external audit — LABOR).
   *
   * GoatCounter stores paths as it receives them: '/s/records/1039', without a
   * trailing slash. The browse enhancer below constructs '/s/records/1039/'
   * WITH one, because that is the canonical link form on the site. Those are
   * different object keys, so the lookup missed on 99 of 100 records and the
   * counter rendered an em-dash even though the snapshot held a perfectly good
   * count for that record.
   *
   * This is a display defect that MIMICS a data defect: it made the analytics
   * look far worse than the underlying dataset, which is exactly the kind of
   * instrument error this archive exists to document. Both sides are now
   * normalised to a single canonical form before comparison, and the lookup
   * tries the variants rather than assuming one convention won. */
  function normPath(p) {
    if (!p || p === 'TOTAL') return p;
    return p.length > 1 ? p.replace(/\/+$/, '') : p;
  }
  function lookup(snapshot, path) {
    var paths = snapshot && snapshot.paths;
    if (!paths) return null;
    if (paths[path]) return paths[path];              // exact, whichever form
    var bare = normPath(path);
    if (paths[bare]) return paths[bare];              // stored without slash
    if (bare !== path && paths[bare + '/']) return paths[bare + '/'];
    if (paths[path + '/']) return paths[path + '/'];  // stored with slash
    return null;
  }

  function renderOne(el, snapshot, suffix) {
    if (!snapshot) return showUnavailable(el);
    var path = el.getAttribute('data-gc');
    if (path === 'TOTAL') {
      if (typeof snapshot.total === 'number') show(el, snapshot.total, suffix || 'visitors site-wide');
      else showUnavailable(el);
      return;
    }
    var entry = lookup(snapshot, path);
    if (entry && typeof entry.count === 'number') show(el, entry.count, suffix);
    else showUnavailable(el);
  }

  function renderAll(snapshot) {
    document.querySelectorAll('.gc-v[data-gc]').forEach(function (el) {
      el.setAttribute('data-gc-done', '1');
      renderOne(el, snapshot);
    });
    var tot = document.getElementById('home-views') || document.getElementById('site-views');
    if (tot) {
      tot.setAttribute('data-gc', 'TOTAL');
      tot.classList.add('gc-v');
      renderOne(tot, snapshot, 'visitors site-wide');
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

      // TWO DATES, AND THEY ARE DIFFERENT FACTS. datetime is the WORK's date;
      // data-deposited is when it was minted. A paper written in July and
      // deposited in August sorts by July on any date sort — which put #1539 at
      // position 116 of 1,539 under "newest" on the day it landed, and would
      // bury every deposit of existing work by an external contributor.
      function key(row) {
        var t = row.querySelector('time[datetime]');
        var m2 = row.getAttribute('href').match(/(\d+)/);
        return {
          d: t ? t.getAttribute('datetime') : '',
          m: t ? (t.getAttribute('data-deposited') || '') : '',
          n: m2 ? parseInt(m2[1], 10) : 0
        };
      }
      function apply(mode) {
        var sorted = rows.slice().sort(function (a, b) {
          var ka = key(a), kb = key(b);
          if (mode === 'newest') return (kb.d > ka.d ? 1 : kb.d < ka.d ? -1 : kb.n - ka.n);
          if (mode === 'oldest') return (ka.d > kb.d ? 1 : ka.d < kb.d ? -1 : ka.n - kb.n);
          if (mode === 'deposited') return (kb.m > ka.m ? 1 : kb.m < ka.m ? -1 : kb.n - ka.n);
          return ka.n - kb.n;
        });
        var last = anchor;
        sorted.forEach(function (r) { parent.insertBefore(r, last.nextSibling); last = r; });
        if (hdr) {
          var label = {
            newest: 'sorted by the work\u2019s date, newest first',
            oldest: 'sorted by the work\u2019s date, oldest first',
            deposited: 'sorted by when deposited, most recent first',
            number: 'sorted by deposit number'
          }[mode];
          var totSpan = hdr.querySelector('#site-views');
          // Counts come from the header's data attributes, written from the
          // registry. rows.length is the number of TOP-LEVEL rows after series
          // folding — it read 1,391 and called them "deposits", while the same
          // page's header said 1,550. One source, or the page contradicts itself.
          var dsT = hdr.getAttribute('data-total'), dsR = hdr.getAttribute('data-rendered'),
              dsF = hdr.getAttribute('data-folded');
          var counts = dsT
            ? Number(dsT).toLocaleString() + ' deposits · ' + Number(dsR).toLocaleString() +
              ' shown, ' + Number(dsF).toLocaleString() + ' earlier versions folded under their series heads'
            : rows.length.toLocaleString() + ' rows';
          hdr.innerHTML = counts + ' · ' + label + ' · sort: ' +
            '<a href="#" data-sort="deposited" style="color:var(--teal)">recently deposited</a> · ' +
            '<a href="#" data-sort="newest" style="color:var(--teal)">newest work</a> · ' +
            '<a href="#" data-sort="oldest" style="color:var(--teal)">oldest work</a> · ' +
            '<a href="#" data-sort="number" style="color:var(--teal)">by №</a>' +
            ' · <span id="site-views">' + (totSpan ? totSpan.textContent : '\u2014') + '</span>';
          if (dsT) { hdr.setAttribute('data-total', dsT); hdr.setAttribute('data-rendered', dsR); hdr.setAttribute('data-folded', dsF); }
          hdr.querySelectorAll('a[data-sort]').forEach(function (a) {
            a.onclick = function (ev) { ev.preventDefault(); apply(a.getAttribute('data-sort')); };
          });
        }
      }
      apply('newest');
    }

    // One snapshot fetch, apply everywhere — including to cards that arrive
    // AFTER this ran. The home page renders its recent-deposit cards from an
    // async fetch of the registry, so at DOMContentLoaded there are no cards
    // yet; renderAll found nothing and the cards were born as em-dashes and
    // stayed that way (2026-09-02). A MutationObserver now renders any
    // .gc-v[data-gc] that appears later, from the same single snapshot.
    loadSnapshot().then(function (snapshot) {
      renderAll(snapshot);
      if (!window.MutationObserver || !document.body) return;
      var mo = new MutationObserver(function (muts) {
        for (var i = 0; i < muts.length; i++) {
          var added = muts[i].addedNodes;
          for (var j = 0; j < added.length; j++) {
            var n = added[j];
            if (n.nodeType !== 1) continue;
            if (n.matches && n.matches('.gc-v[data-gc]') && !n.hasAttribute('data-gc-done')) {
              n.setAttribute('data-gc-done', '1'); renderOne(n, snapshot);
            }
            var inner = n.querySelectorAll ? n.querySelectorAll('.gc-v[data-gc]:not([data-gc-done])') : [];
            for (var k = 0; k < inner.length; k++) {
              inner[k].setAttribute('data-gc-done', '1'); renderOne(inner[k], snapshot);
            }
          }
        }
      });
      mo.observe(document.body, { childList: true, subtree: true });
    });
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
