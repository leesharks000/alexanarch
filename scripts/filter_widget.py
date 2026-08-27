#!/usr/bin/env python3
"""filter_widget.py — one filter implementation, injected by whichever generator
writes last.

WHY ONE IMPLEMENTATION
A filter was once added to the wiki page by regenerate_surfaces.py and then
silently destroyed by publish_wiki_entries.py, which runs afterwards and rewrites
the same file. The feature was never rejected; it was overwritten. Copying the
widget into each generator would reproduce that class of loss and let the copies
drift. This module is the single source, and the LAST writer of each surface
injects it.

PROGRESSIVE ENHANCEMENT, NOT REPLACEMENT
The complete static list stays in the HTML. Crawlers, no-JavaScript readers and
archival captures see every row exactly as before. The filter hides rows that do
not match; it never fetches, never re-renders, and cannot empty the page if it
fails. It also carries an explicit route to full-text search, because filtering a
rendered list and searching every body are different acts and the reader should
be told which one they are doing.
"""

def filter_widget(row_selector: str, noun: str, total: int,
                  search_href: str = "/search/") -> str:
    """Return the filter bar + behaviour for a static list surface.

    row_selector — CSS selector matching one row per item
    noun         — what a row is, for the count line ("deposits", "entries")
    total        — the rendered row count, for the resting label
    """
    return f"""
<div class="filterbar" style="margin:14px 0 18px">
  <label for="axnflt" style="position:absolute;left:-9999px">Filter {noun}</label>
  <input id="axnflt" type="search" autocomplete="off"
         placeholder="Filter {total:,} {noun} — title, AXN, number, creator"
         style="width:100%;font-family:var(--sans,sans-serif);font-size:.95em;padding:9px 12px;
                border:1px solid var(--border,#e0e0e0);border-radius:6px;background:var(--surface,#fff);color:inherit">
  <div style="display:flex;gap:10px;align-items:baseline;flex-wrap:wrap;margin-top:6px;
              font-size:.78em;color:var(--dim,#777)">
    <span id="axnfltcount" aria-live="polite">{total:,} {noun}</span>
    <span>·</span>
    <span>filters this page only —
      <a id="axnfltfull" href="{search_href}">search every deposit's full text</a></span>
  </div>
</div>
<script>
(function(){{
  // WAIT FOR THE ROWS. This widget renders ABOVE the list it filters, because
  // that is where a filter bar belongs — so at parse time NOT ONE ROW EXISTS.
  // Querying here returned an empty list, the length guard below fired, and the
  // filter silently never bound: 1,460 rows present, filter inert, no error
  // anywhere. The guard written to protect the page was what disabled it.
  // Found 2026-08-14 on /s/browse/ and /s/wiki/, where the script sat at byte
  // 4,939 and the first row at 7,007.
  function ready(fn) {{
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', fn);
    else fn();
  }}
  ready(function(){{
  var box = document.getElementById('axnflt');
  if (!box) return;                                  // no widget, no behaviour
  var rows = Array.prototype.slice.call(document.querySelectorAll({row_selector!r}));
  if (!rows.length) return;                          // never blank a page we cannot see
  var count = document.getElementById('axnfltcount');
  var full  = document.getElementById('axnfltfull');
  var timer = null;

  function apply() {{
    var q = box.value.trim().toLowerCase();
    var toks = q.split(/\\s+/).filter(Boolean);
    var shown = 0;
    for (var i = 0; i < rows.length; i++) {{
      var r = rows[i];
      if (!r.__hay) r.__hay = (r.textContent || '').toLowerCase();
      var ok = true;
      for (var j = 0; j < toks.length; j++) {{
        if (r.__hay.indexOf(toks[j]) === -1) {{ ok = false; break; }}
      }}
      // Restore the row's ORIGINAL display value, never ''. Browse rows carry an
      // inline style="display:block", and assigning '' strips it — which turned
      // 1,434 stacked rows into one inline run the moment the page loaded,
      // because apply() runs once at init even with an empty query.
      if (r.__disp === undefined) r.__disp = r.style.display || '';
      r.style.display = ok ? r.__disp : 'none';
      if (ok) shown++;
    }}
    // Idle shows NOTHING. The page's count belongs to one place — the header,
    // drawn from the registry. This label restated it from a DOM row count, which
    // is a different number whenever any row is folded or dropped: browse read
    // 1,550 in the header, 1,542 here, and 1,391 after the sorter rewrote it.
    count.textContent = q
      ? shown.toLocaleString() + ' of ' + rows.length.toLocaleString() + ' matching'
      : '';
    full.href = q ? '{search_href}?q=' + encodeURIComponent(q) : '{search_href}';
    // shareable: the filtered view survives a copied URL and the back button
    try {{
      var u = new URL(location);
      q ? u.searchParams.set('f', q) : u.searchParams.delete('f');
      history.replaceState(null, '', u);
    }} catch (e) {{}}
  }}

  box.addEventListener('input', function () {{
    clearTimeout(timer); timer = setTimeout(apply, 90);
  }});
  var init = new URLSearchParams(location.search).get('f');
  if (init) {{ box.value = init; apply(); }}
  else {{ count.textContent = ''; }}
  }});
}})();
</script>
"""
