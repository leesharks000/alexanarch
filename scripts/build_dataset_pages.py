#!/usr/bin/env python3
"""build_dataset_pages.py — every dataset gets a reachable page.

MANUS: "on datasets, that data is sparse. you should be able to access the
fuller data that is available elsewhere. where are the transcripts, the
analysis?"

They were on disk and unreachable. Nine dataset directories were absent from
/datasets/ entirely, including the two richest: registry-audit, which holds 47
files of batch findings and the record-shape specification, and dataflow-atlas,
which holds eleven successive versions of the archive's own map.

This generates an index page for any dataset directory that lacks one, listing
every file with its size, and — where a MANIFEST.json exists — its description.
Markdown files are linked as raw text; JSON as raw JSON. Nothing is summarised
away: the page is a door, not a précis.

    python3 scripts/build_dataset_pages.py            # report
    python3 scripts/build_dataset_pages.py --write
"""
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
DS = ROOT / 'datasets'

BLURB = {
    'registry-audit': ("The archive auditing itself. Batch findings across the full deposit "
                       "range, the content-fingerprint scan, the verified register, and "
                       "RECORD-SHAPE-AND-PROPAGATION — the specification of the nine "
                       "declaration sites and the seven-step propagator pipeline."),
    'dataflow-atlas': ("Eleven successive versions of the archive's own map: where data enters, "
                       "what transforms it, where it is published, and which instruments watch "
                       "the map itself. Read v1.1 for the current head; the superseded versions "
                       "are kept because the map's own history is evidence."),
    'capture-registry': ("The capture registry as data: dated reception events with query, "
                         "section, attribution state and finding."),
    'doi-work-identity': ("Which DOI resolves to which work, graded by truth source. Built after "
                          "1,817 Zenodo DOIs were tombstoned."),
    'erosion-empirical-audit-01': ("Programmed bibliographic suppression documented at commit "
                                   "level."),
    'deletion-conformance-fixture': ("A fixture for testing whether a system's deletion behaviour "
                                     "conforms to what it claims."),
    'axnidentifiers': "The AXN identifier system as data.",
    'peo-case-001-florence-fup': "A provenance-erasure case file.",
    'venues': "Publication venues.",
}

CSS = """<style>
.dsx{max-width:52rem;margin:0 auto;padding:1rem 1.4rem 5rem}
.dsx h1{font-size:1.6rem;margin:.4rem 0 .2rem}
.dsx .sub{font-family:ui-monospace,Menlo,monospace;font-size:11px;letter-spacing:.12em;
text-transform:uppercase;color:#6d6f66;margin-bottom:1.2rem}
.dsx .lede{font-size:1.05rem;line-height:1.55;max-width:38rem;margin-bottom:1.4rem}
.fl{border-top:1px solid #d9d9d0}
.fl a.row{display:grid;grid-template-columns:minmax(0,1fr) 90px;gap:12px;padding:10px 2px;
border-bottom:1px solid #ececE4;text-decoration:none;color:inherit;align-items:baseline}
.fl a.row:hover{background:rgba(26,58,92,.04)}
.fl .nm{font-family:ui-monospace,Menlo,monospace;font-size:12.5px;color:#1a3a5c;
overflow-wrap:anywhere}
.fl .sz{font-family:ui-monospace,Menlo,monospace;font-size:11px;color:#8a8a80;text-align:right}
.fl .ds{grid-column:1/-1;font-size:12.5px;color:#55564e;line-height:1.5;margin-top:2px}
</style>"""


def human(n):
    for u in ('B', 'KB', 'MB'):
        if n < 1024 or u == 'MB':
            return f'{n:.0f} {u}' if u == 'B' else f'{n:.1f} {u}'
        n /= 1024


def page(name, files, nav, blurb, desc):
    rows = []
    for f, sz in files:
        d = desc.get(f, '')
        rows.append(f'<a class="row" href="./{f}"><span class="nm">{f}</span>'
                    f'<span class="sz">{human(sz)}</span>'
                    + (f'<span class="ds">{d}</span>' if d else '') + '</a>')
    return (f'<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">'
            f'<meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>datasets/{name}/ — Alexanarch</title>'
            f'<meta name="description" content="{blurb[:180]}">'
            f'<link rel="canonical" href="https://www.alexanarch.org/datasets/{name}/">'
            f'<link rel="icon" href="/favicon.ico" sizes="any">'
            f'{CSS}</head><body>{nav}'
            f'<div class="dsx"><div class="sub">Alexanarch &middot; datasets</div>'
            f'<h1>datasets/{name}/</h1>'
            f'<div class="sub">{len(files)} files &middot; '
            f'{human(sum(s for _, s in files))}</div>'
            f'<p class="lede">{blurb}</p>'
            f'<div class="fl">' + ''.join(rows) + '</div>'
            f'<p class="sub" style="margin-top:2rem">'
            f'<a href="/datasets/">all datasets</a> &middot; '
            f'<a href="/">the archive</a></p></div></body></html>')


if __name__ == '__main__':
    import re
    nav = re.search(r'<nav[^>]*>.*?</nav>',
                    (ROOT / 'datasets/index.html').read_text(), re.S).group(0)
    made = []
    for d in sorted(DS.iterdir()):
        if not d.is_dir() or (d / 'index.html').exists():
            continue
        files = sorted((f.name, f.stat().st_size) for f in d.iterdir() if f.is_file())
        if not files:
            continue
        desc = {}
        mf = d / 'MANIFEST.json'
        if mf.exists():
            try:
                m = json.loads(mf.read_text())
                for e in (m.get('files') or []):
                    if isinstance(e, dict) and e.get('name'):
                        desc[e['name']] = e.get('description', '')
            except Exception:
                pass
        blurb = BLURB.get(d.name, f'{len(files)} files.')
        made.append((d.name, len(files)))
        if '--write' in sys.argv:
            (d / 'index.html').write_text(page(d.name, files, nav, blurb, desc))
    for n, c in made:
        print(f'  datasets/{n}/  {c} files  → index.html')
    print(f'\n  {len(made)} page(s)' + ('' if '--write' in sys.argv else ' (dry run)'))
