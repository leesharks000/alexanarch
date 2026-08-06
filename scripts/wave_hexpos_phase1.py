#!/usr/bin/env python3
"""WAVE-HEXPOS-01 · Phase 1 — hex-width normalization of the three founding
records (#1, #2, #3: 01/02/03 -> 0001/0002/0003).

Ruling-free scope only. Does NOT touch #913 (391), #869, or #901 — those are
Phase 2, blocked on the MANUS allocation ruling for the 0365 and 0391
contested positions.

Acts, all idempotent:
  1. data/registry.json — for #1/#2/#3: hex padded to 4 chars; axn string
     rewritten with the padded label; prior form appended to axn_history
     (pattern of the 2026-06-22 v1->v2 schema backfill).
  2. s/axn/0001|0002|0003/index.html — canonical resolver pages written
     from record data (template of the current generation, cf. s/axn/05AF/).
  3. s/axn/01|02|03/index.html — rewritten as superseded-label alias pages
     that state the normalization and point to the canonical page. The URLs
     keep resolving forever (non-destruction).
Run from repo root or scripts/. After running: python3 scripts/build_central_registry.py
then the standard page/OAI regeneration + nine-site propagation for #1-#3.
"""
import json, pathlib, datetime, re, sys, html

ROOT = pathlib.Path(__file__).resolve().parent
if not (ROOT/"data/registry.json").exists(): ROOT = ROOT.parent
assert (ROOT/"data/registry.json").exists(), "run from repo root or scripts/"

TODAY = datetime.date.today().isoformat()
REASON = "hex_width_normalization_4char (WAVE-HEXPOS-01 Phase 1)"
TARGETS = {1: ("01","0001"), 2: ("02","0002"), 3: ("03","0003")}

reg_path = ROOT/"data/registry.json"
reg = json.loads(reg_path.read_text())
deps = reg["deposits"]
changed = 0
for d in deps:
    n = d.get("deposit_number")
    if n not in TARGETS: continue
    old_hx, new_hx = TARGETS[n]
    if d.get("hex") == new_hx:
        print(f"#{n}: already {new_hx} — skip"); continue
    assert d.get("hex") == old_hx, f"#{n}: unexpected hex {d.get('hex')!r}"
    old_axn = d["axn"]
    new_axn = old_axn.replace(f"AXN:{old_hx}.", f"AXN:{new_hx}.", 1)
    assert new_axn != old_axn and f"AXN:{new_hx}." in new_axn
    hist = d.setdefault("axn_history", [])
    if not any(h.get("axn") == old_axn for h in hist):
        hist.append({"axn": old_axn, "schema_version": d.get("axn_schema_version","v2"),
                     "retired_at": TODAY, "reason": REASON})
    d["hex"], d["axn"] = new_hx, new_axn
    changed += 1
    print(f"#{n}: {old_axn}  ->  {new_axn}")

# collision guard: after edit, no padded key may collide beyond the two known contested ones
from collections import Counter
c = Counter((d.get("hex") or "").upper().zfill(4) for d in deps if d.get("hex"))
new_coll = {k:v for k,v in c.items() if v > 1 and k not in ("0365","0391")}
assert not new_coll, f"UNEXPECTED COLLISIONS after edit: {new_coll} — aborting, nothing written"

if changed:
    reg_path.write_text(json.dumps(reg, ensure_ascii=False, indent=1))
    print(f"registry.json written ({changed} records normalized)")

# ---- resolver pages ----
def canonical_page(d):
    hx, axn, n = d["hex"], d["axn"], d["deposit_number"]
    fam = d.get("family",""); sha = d.get("axn_canonical","")
    glyph = axn.split(".",2)[2] if axn.count(".")>=2 else ""
    title = html.escape(d.get("title",""))
    ld = {"@context":"https://schema.org","@type":"DefinedTerm",
      "@id":f"https://www.alexanarch.org/s/axn/{hx}/","url":f"https://www.alexanarch.org/s/axn/{hx}/",
      "name":axn,"termCode":axn,
      "identifier":[{"@type":"PropertyValue","propertyID":"AXN","value":axn},
        {"@type":"PropertyValue","propertyID":"AXN-hex","value":hx},
        {"@type":"PropertyValue","propertyID":"sha256","value":sha}],
      "inDefinedTermSet":{"@type":"DefinedTermSet","@id":"https://www.alexanarch.org/s/axn/",
        "name":"AXN — Alexanarch content-derived identifiers","url":"https://www.alexanarch.org/s/axn/"},
      "description":f"AXN {hx} is the content-derived identifier of Alexanarch deposit #{n}. The hex marks position in the archive; the six-glyph suffix is a display hash of the canonical text's SHA-256, so the identifier is derived from the work rather than assigned to it. Family: {fam}.",
      "about":{"@type":"ScholarlyArticle","@id":f"https://www.alexanarch.org/s/records/{n}/",
        "url":f"https://www.alexanarch.org/s/records/{n}/","name":d.get("title","")},
      "subjectOf":{"@type":"WebPage","@id":f"https://www.alexanarch.org/s/records/{n}/","url":f"https://www.alexanarch.org/s/records/{n}/"},
      "sameAs":[f"https://www.alexanarch.org/s/records/{n}/"],
      "additionalProperty":[{"@type":"PropertyValue","name":"family","value":fam},
        {"@type":"PropertyValue","name":"glyph_hash","value":glyph}]}
    hist_html = ""
    for h in (d.get("axn_history") or []):
        hist_html += f'<dt>Retired form</dt><dd><code>{html.escape(h.get("axn",""))}</code> — retired {html.escape(h.get("retired_at",""))} ({html.escape(h.get("reason",""))})</dd>\n'
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<title>{axn} — Alexanarch AXN resolver</title>
<link rel="canonical" href="https://www.alexanarch.org/s/axn/{hx}/">
<meta name="robots" content="index,follow,max-snippet:-1,max-image-preview:large">
<meta name="description" content="AXN {hx} — content-derived identifier of Alexanarch deposit #{n}. Hex position {hx}; family {fam}; six-glyph display hash of the canonical text SHA-256.">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
</head><body>
<h1>{axn}</h1>
<p><strong>AXN {hx}</strong> is the content-derived identifier of Alexanarch deposit
<a href="https://www.alexanarch.org/s/records/{n}/">#{n}</a>. It is an identifier, not a copy of the work: the hex marks
position in the archive, and the six-glyph suffix is a display hash of the canonical
text&rsquo;s SHA-256, so the identifier is derived from the work rather than assigned to it.</p>
<dl>
<dt>Identifies</dt><dd><a href="https://www.alexanarch.org/s/records/{n}/">{title}</a></dd>
<dt>Hex position</dt><dd><code>{hx}</code></dd>
<dt>Family</dt><dd><code>{fam}</code></dd>
<dt>Glyph hash</dt><dd>{glyph}</dd>
<dt>Canonical-text SHA-256</dt><dd><code>{sha}</code></dd>
<dt>Record</dt><dd><a href="https://www.alexanarch.org/s/records/{n}/">https://www.alexanarch.org/s/records/{n}/</a></dd>
{hist_html}</dl>
<p>Resolver rule: <code>alexanarch.org/axn/&lt;HEX&gt;</code> &middot;
term set: <a href="/s/axn/">AXN identifier set</a> &middot;
machine index: <a href="/api/axn-index.json">/api/axn-index.json</a></p>
</body></html>"""

def alias_page(old_hx, d):
    hx, axn, n = d["hex"], d["axn"], d["deposit_number"]
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<title>AXN {old_hx} — superseded label — Alexanarch AXN resolver</title>
<link rel="canonical" href="https://www.alexanarch.org/s/axn/{hx}/">
<meta name="robots" content="noindex,follow">
<meta http-equiv="refresh" content="4; url=/s/axn/{hx}/">
</head><body>
<h1>AXN {old_hx} &rarr; <a href="/s/axn/{hx}/">AXN {hx}</a></h1>
<p><strong>{old_hx}</strong> is a superseded label of the same position, retired {TODAY}
under hex-width normalization (WAVE-HEXPOS-01): all AXN hex labels are four
characters. The identifier it named — deposit <a href="/s/records/{n}/">#{n}</a> —
is unchanged; its canonical form is <code>{html.escape(axn)}</code>.
This URL resolves permanently; nothing published against it is broken.</p>
<p>Continuing to <a href="/s/axn/{hx}/">/s/axn/{hx}/</a>&hellip;</p>
</body></html>"""

for d in deps:
    n = d.get("deposit_number")
    if n not in TARGETS: continue
    old_hx, new_hx = TARGETS[n]
    pc = ROOT/f"s/axn/{new_hx}"; pc.mkdir(parents=True, exist_ok=True)
    (pc/"index.html").write_text(canonical_page(d))
    pa = ROOT/f"s/axn/{old_hx}"; pa.mkdir(parents=True, exist_ok=True)
    (pa/"index.html").write_text(alias_page(old_hx, d))
    print(f"#{n}: wrote s/axn/{new_hx}/ (canonical) + s/axn/{old_hx}/ (alias)")

print("Phase 1 complete. Next: python3 scripts/build_central_registry.py, then standard regeneration + propagation for #1-#3.")
