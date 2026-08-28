#!/usr/bin/env python3
"""build_errata_surface.py — generate /errata/ from the registry.

An archive that corrects itself in public needs one place where the
corrections can be read together. Errata are otherwise scattered across the
deposit sequence at the point they were minted, which is the least useful place
to look for them: a reader arrives at the CORRECTED work, not at the correction.

Detection is deliberately conservative and declared, not guessed:
  - content_type matching /erratum|errata|correction/i, OR
  - title beginning with ERRATUM/Erratum/Errata
An entry whose corrected target cannot be resolved is listed with the target
marked UNRESOLVED rather than omitted or invented. Absence is a claim.

Target resolution, in order:
  1. related_deposits[] with a relation containing "correct"
  2. an AXN hex in the title ("ERRATUM to AXN:044A")
  3. a deposit number in the title ("in Deposit #1081")
  4. the body's front-matter "corrects:" line
  5. UNRESOLVED

Chains are detected transitively: where an erratum corrects another erratum,
the surface renders the whole descent (the Sappho 31 series runs six deep).

Usage:  python3 scripts/build_errata_surface.py [--dry-run]
"""
import json, re, sys, html, datetime, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
ERRATUM_TYPE = re.compile(r'\berrat(?:um|a)\b|\b(?:record|classifier|philological|mathematical|technical)\s+correction\b', re.I)
ERRATUM_TITLE = re.compile(r'^\s*(erratum|errata)\b', re.I)
AXN_HEX = re.compile(r'AXN:([0-9A-F]{4})')
DEP_NUM = re.compile(r'[Dd]eposit\s*#(\d+)')


def load_registry():
    return json.load(open(ROOT / 'data' / 'registry.json'))


def is_erratum(d):
    return bool(ERRATUM_TYPE.search(d.get('content_type') or '')) or \
           bool(ERRATUM_TITLE.match(d.get('title') or ''))


def body_corrects_line(d):
    p = (d.get('full_text_path') or '').lstrip('/')
    if not p:
        return None
    f = ROOT / p
    if not f.exists():
        return None
    head = f.read_text(errors='replace')[:6000]
    m = re.search(r'^corrects:\s*(.+)$', head, re.M)
    return m.group(1).strip() if m else None


def resolve_target(d, by_hex, by_num):
    """Return (target|None, evidence, candidates[]).

    Resolution is DECLARED only. Where the record does not declare a target we
    return None and surface the AXN references the deposit does carry, as
    candidates a reader can follow — never as an asserted correction. Most of
    the archive's errata predate the declared form and name no target
    machine-readably; that gap is shown rather than filled by inference.
    """
    for r in (d.get('related_deposits') or []):
        if isinstance(r, dict) and 'correct' in str(r.get('relation', '')).lower():
            return r.get('deposit_number'), 'declared: related_deposits relation', []
    title = d.get('title') or ''
    m = AXN_HEX.search(title)
    if m and m.group(1) in by_hex:
        return by_hex[m.group(1)], f'declared: AXN:{m.group(1)} in title', []
    m = DEP_NUM.search(title)
    if m and int(m.group(1)) in by_num:
        return int(m.group(1)), 'declared: deposit number in title', []
    line = body_corrects_line(d)
    if line:
        m = AXN_HEX.search(line)
        if m and m.group(1) in by_hex:
            return by_hex[m.group(1)], 'declared: corrects: line in body', []
        m = DEP_NUM.search(line)
        if m and int(m.group(1)) in by_num:
            return int(m.group(1)), 'declared: corrects: line in body', []
    # not declared — collect candidates without asserting any of them
    cands = []
    for hx in AXN_HEX.findall(str(d.get('related_ids') or '')):
        if hx in by_hex and by_hex[hx] != d['deposit_number']:
            cands.append(by_hex[hx])
    return None, 'not declared in the record', cands[:4]


def build():
    reg = load_registry()
    by_num = {d['deposit_number']: d for d in reg['deposits']}
    by_hex = {d.get('hex'): d['deposit_number'] for d in reg['deposits'] if d.get('hex')}
    errata = sorted([d for d in reg['deposits'] if is_erratum(d)],
                    key=lambda x: (x.get('date') or '', x['deposit_number']))
    rows = []
    for d in errata:
        tgt, ev, cands = resolve_target(d, by_hex, by_num)
        rows.append({'d': d, 'target': tgt, 'evidence': ev, 'candidates': cands})
    # chain depth: how many hops back to a non-erratum
    err_nums = {r['d']['deposit_number'] for r in rows}
    def depth(n, seen=None):
        seen = seen or set()
        r = next((x for x in rows if x['d']['deposit_number'] == n), None)
        if not r or not r['target'] or r['target'] in seen or r['target'] not in err_nums:
            return 0
        return 1 + depth(r['target'], seen | {n})
    for r in rows:
        r['depth'] = depth(r['d']['deposit_number'])
    return rows, by_num


CSS = """*{box-sizing:border-box}body{margin:0;background:#fbfbf9;color:#16181d;
font-family:'IBM Plex Sans',system-ui,sans-serif;font-size:17px;line-height:1.6}
.wrap{max-width:900px;margin:0 auto;padding:56px 24px 90px}
h1{font-size:34px;margin:0 0 6px;letter-spacing:-.01em}
.tag{font-size:18px;color:#123a5e;margin:0 0 14px}
.crumb{font-family:'IBM Plex Mono',monospace;font-size:12px;color:#6d6f66;margin:0 0 8px}
.principle{font-size:15px;background:#f1f1ec;border:1px solid #d9d9d0;border-left:3px solid #123a5e;
border-radius:4px;padding:14px 18px;margin:0 0 26px;color:#3c3e37}
.e{border:1px solid #d9d9d0;border-radius:6px;background:#fff;padding:20px 24px;margin:0 0 16px}
.e h3{font-size:17px;margin:0 0 6px;font-weight:600}
.e h3 a{color:#16181d;text-decoration:none}.e h3 a:hover{text-decoration:underline}
.meta{display:grid;grid-template-columns:auto 1fr;column-gap:14px;row-gap:5px;font-size:14px;margin:10px 0 0}
.k{font-family:'IBM Plex Mono',monospace;font-size:11px;text-transform:uppercase;letter-spacing:.06em;color:#6d6f66;padding-top:3px}
.v{color:#3c3e37}.v a{color:#123a5e}
.mono{font-family:'IBM Plex Mono',monospace;font-size:12.5px}
.chain{display:inline-block;background:#f1f1ec;border:1px solid #d9d9d0;border-radius:3px;
padding:1px 7px;font-family:'IBM Plex Mono',monospace;font-size:11px;color:#123a5e;margin-left:6px}
.unres{color:#a41623}
.sev{font-size:13.5px;color:#3c3e37;margin:10px 0 0;font-style:italic}
footer{margin-top:46px;font-size:13px;color:#6d6f66;border-top:1px solid #d9d9d0;padding-top:18px}
"""


def render(rows, by_num):
    n = len(rows)
    unres = sum(1 for r in rows if not r['target'])
    chains = sum(1 for r in rows if r['depth'] > 0)
    out = [f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Errata — Crimson Hexagonal Archive</title>
<meta name="description" content="Every correction the archive has issued against its own deposits, collected in one place.">
<style>{CSS}</style></head><body><div class="wrap">
<p class="crumb"><a href="/">alexanarch.org</a> / errata</p>
<h1>Errata</h1>
<p class="tag">Every correction the archive has issued against its own record.</p>
<div class="principle"><b>Why this surface exists.</b> An erratum minted into the deposit
sequence sits at the point it was written, which is the least useful place to look for it:
a reader arrives at the corrected work, not at the correction. This page collects them so
that the archive's errors can be read as a series rather than found by accident.
<b>Corrections are registry-level.</b> The canonical bytes of a corrected deposit are not
rewritten — the erratum is a separate deposit, cross-referenced, and any citation of the
corrected claim carries it. An entry whose target could not be resolved from the record is
listed as <span class="unres">UNRESOLVED</span> rather than omitted or guessed.</div>
<p class="mono">{n} errata &middot; {chains} correcting other errata &middot; {unres} target unresolved
&middot; generated {datetime.date.today().isoformat()}</p>
"""]
    for r in rows:
        d = r['d']; t = r['target']
        if not t:
            if r['candidates']:
                tgt_html = ('<span class="unres">not declared</span> — candidates from related_ids: ' +
                            ', '.join(f'<a href="/s/records/{c}/">#{c}</a>' for c in r['candidates']))
            else:
                tgt_html = '<span class="unres">not declared in the record</span>'
        tgt_html = (tgt_html if not t else
                    f'<a href="/s/records/{t}/">#{t}</a> — ' +
                    html.escape((by_num[t].get('title') or '')[:88]) +
                    f' <span class="mono">({html.escape(by_num[t].get("axn","")[:24])})</span>')
        chain = f'<span class="chain">chain depth {r["depth"]+1}</span>' if r['depth'] else ''
        sev = body_corrects_line(d)
        out.append(f"""<div class="e">
<h3><a href="/s/records/{d['deposit_number']}/">#{d['deposit_number']} — {html.escape((d.get('title') or '')[:150])}</a>{chain}</h3>
<div class="meta">
<div class="k">corrects</div><div class="v">{tgt_html}</div>
<div class="k">identifier</div><div class="v mono">{html.escape(d.get('axn',''))}</div>
<div class="k">date</div><div class="v mono">{html.escape(d.get('date') or '')}</div>
<div class="k">type</div><div class="v">{html.escape(d.get('content_type') or '')}</div>
<div class="k">resolved by</div><div class="v mono">{html.escape(r['evidence'])}</div>
</div></div>""")
    out.append("""<footer>Generated from <span class="mono">data/registry.json</span> by
<span class="mono">scripts/build_errata_surface.py</span>. Detection is by declared
content type or title, never inferred from content. Re-run after any erratum mint.
</footer></div></body></html>""")
    return '\n'.join(out)


if __name__ == '__main__':
    rows, by_num = build()
    page = render(rows, by_num)
    if '--dry-run' in sys.argv:
        print(f'{len(rows)} errata; {sum(1 for r in rows if not r["target"])} unresolved')
        for r in rows:
            print(f'  #{r["d"]["deposit_number"]:>5} -> {r["target"] or "UNRESOLVED"}  ({r["evidence"]})')
        sys.exit(0)
    out = ROOT / 'errata'
    out.mkdir(exist_ok=True)
    (out / 'index.html').write_text(page)
    print(f'errata/index.html written — {len(rows)} errata, '
          f'{sum(1 for r in rows if r["depth"]>0)} in chains, '
          f'{sum(1 for r in rows if not r["target"])} unresolved')
