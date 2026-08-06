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
      r.style.display = ok ? '' : 'none';
      if (ok) shown++;
    }}
    count.textContent = q
      ? shown.toLocaleString() + ' of ' + rows.length.toLocaleString() + ' {noun}'
      : rows.length.toLocaleString() + ' {noun}';
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
  if (init) box.value = init;
  apply();
}})();
</script>
"""
