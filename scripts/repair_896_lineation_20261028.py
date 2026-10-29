#!/usr/bin/env python3
"""repair_896_lineation_20261028.py — #896 HUMS &ITY: the description field's lines restored, the provenance unwrapped.

Lee Sharks, 2026-10-28: "the deposit page for hums &ity is blob text that erases all line break of the poem followed by
hard-coded prose linebreaks" ... "lets fix those other records as well". Repair scope as ruled 2026-10-15: broken,
missing and mislabelled files; standard, the text as published.

The body of #896 is the Zenodo description field of 22 February 2026 (10.5281/zenodo.18729800), an APZPZ: the poem lived
in the field. It was recovered from OpenAlex, which flattens the field to one line, so the poem's lineation and the
field's parts (deposit instructions, the poem, the situating note, keywords, related identifiers) ran together.

  THE POEM: lineated from the same work's first Zenodo version, 2 February 2026 (concept 10.5281/zenodo.18459863,
            resolved to #896), whose description DataCite preserved with its breaks (data/datacite-full-backup.json):
            couplets, a blank line between each, the closing "?" alone. The words are asserted equal, token for token,
            to the poem's words in #896's body before any line is broken.
  THE FIELD: broken into its parts at the headings and items it already carries; every token kept, in order (asserted).
  THE PROVENANCE: the mint note's paragraphs were wrapped at a fixed width; each paragraph is joined to one line.

Rehashed with a new AXN at the same hex and family; axn_prior and modifications record the change.
    python3 scripts/repair_896_lineation_20261028.py [--apply]"""
import hashlib, json, pathlib, re, sys
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import record_modification as rm
from axn_lib import axn_glyph_from_hash, axn_clusters_from_hash, axn_reading_from_clusters, compose_axn

ON = "2026-10-28"
RULING = ('Lee Sharks, 2026-10-28: "the deposit page for hums &ity is blob text that erases all line break of the poem followed by '
          'hard-coded prose linebreaks"; "lets fix those other records as well"')
TP = ROOT / "data/texts/AXN-038C-text.md"
DP = ROOT / "data/deposits/AXN-038C.md"
toks = lambda s: s.replace("\xa0", " ").split()
norm = lambda s: toks(re.sub(r"(?m)^\s*- ", "", s).replace("**", "").replace("---", " "))

t = TP.read_text(encoding="utf-8")
assert DP.read_text(encoding="utf-8") == t
lines = t.split("\n")
bi = lines.index("## Body") + 2
blob = lines[bi]
assert blob.startswith("ZENODO DESCRIPTION FIELD CONTENT For: HUMS & ITY") and "\n" not in blob

# the first version's description, with its breaks
d = json.loads((ROOT / "data/datacite-full-backup.json").read_text(encoding="utf-8"))


def walk(o):
    if isinstance(o, dict):
        if o.get("id") == "10.5281/zenodo.18459863" and (o.get("attributes") or {}).get("descriptions"):
            yield o
        for v in o.values():
            yield from walk(v)
    elif isinstance(o, list):
        for v in o:
            yield from walk(v)


v1 = next(walk(d))["attributes"]["descriptions"][0]["description"]
# stanzas: groups of non-empty lines separated by the NBSP paragraphs; the title and byline come first
paras = [l for l in v1.replace("\xa0", "\x00").split("\n\n")]
stanzas, cur = [], []
for p in paras:
    p = p.strip()
    if p in ("", "\x00"):
        if cur:
            stanzas.append(cur); cur = []
        continue
    cur.append(p.replace("\x00", "").strip())
if cur:
    stanzas.append(cur)
assert stanzas[0] == ["HUMS &ITY", "Lee Sharks"], stanzas[0]
poem = stanzas[1:]

A = blob.index("Hark these, my tongue-formed")
B = blob.index(" Situating Note.")
assert toks(blob[A:B]) == [w for s in poem for l in s for w in toks(l)], "poem words differ"

pre, post = blob[:A].strip(), blob[B:].strip()


def split_at(s, marks):
    """Break s before each mark, in order; every mark must occur once, after the previous."""
    out, pos = [], 0
    for m in marks:
        i = s.index(m, pos)
        out.append(s[pos:i].strip()); pos = i
    out.append(s[pos:].strip())
    return [x for x in out if x]


note_part, rest = post.split(" KEYWORDS ", 1)
kw, rel = rest.split(" RELATED IDENTIFIERS ", 1)
rels = split_at(rel, ["IsSupplementTo:", "References:", "10.5281/zenodo.14025488", "10.5281/zenodo.14538914"])
nb, close = note_part.split(" ∮ = 1 + δ_Sapphic")
note_body = nb.strip()
sit, after = note_body.split("The uploaded file contains only:", 1)

# rebuild the head precisely from tokens so nothing is lost or added
out = []
out.append("ZENODO DESCRIPTION FIELD CONTENT For: HUMS & ITY")
out.append("")
rest_head = pre[len("ZENODO DESCRIPTION FIELD CONTENT For: HUMS & ITY"):].strip()
parts = split_at(rest_head, ["PASTE THE FOLLOWING", "DEPOSIT INSTRUCTIONS", "Reserve DOI at Zenodo", "Title: HUMS & ITY", "Attach: SAPPHIC_SUBSTRATE_ZENODO_UPLOAD.md Paste",
                             "Paste everything", "Add keywords", "Add related identifiers", "Author: Lee Sharks", "License: CC BY 4.0", "Resource type:", "Publish ",
                             "DESCRIPTION FIELD CONTENT — PASTE", "HUMS & ITY Lee Sharks", "Lee Sharks Crimson", "∮ = 1", "HUMS & ITY"])
# parts: DOI line, PASTE…, DEPOSIT INSTRUCTIONS, 9 instruction items, Publish, DESCRIPTION FIELD CONTENT — PASTE BELOW THIS LINE, HUMS & ITY, Lee Sharks…, ∮ = 1, HUMS & ITY
doi, paste, dep = parts[0], parts[1], parts[2]
instr = parts[3:12]
publish, below, ftitle, fbyline, fseal, ptitle = parts[12:18]
assert fbyline.startswith("Lee Sharks Crimson")
assert dep == "DEPOSIT INSTRUCTIONS" and publish == "Publish" and ptitle == "HUMS & ITY", parts
out += [doi, "", paste, "", "**DEPOSIT INSTRUCTIONS**", ""] + ["- " + x for x in instr] + ["- " + publish, "", "---", "",
        "**" + below + "**", "", ftitle, "", "Lee Sharks", fbyline[len("Lee Sharks "):], "", fseal, "", "**" + ptitle + "**", ""]
for i, s in enumerate(poem):
    out += s + [""]
out += ["**Situating Note.** " + sit[len("Situating Note."):].strip(), "", "The uploaded file contains only:" + after.rstrip(), "", "∮ = 1 + δ_Sapphic" + close, "",
        "**KEYWORDS**", "", kw.strip(), "", "**RELATED IDENTIFIERS**", ""]
out += ["- " + r for r in rels[:2]] + ["- " + rels[2]] + ["  - " + r for r in rels[3:]]
new_body = "\n".join(out).rstrip()
assert norm(new_body) == norm(blob), "field tokens differ"

# provenance: join wrapped paragraphs
pi = lines.index("## Provenance")
prov = lines[pi + 1:]
pj, buf = [], []
for l in prov:
    if l.strip():
        buf.append(l.strip())
    else:
        if buf:
            pj.append(" ".join(buf)); buf = []
        pj.append("")
if buf:
    pj.append(" ".join(buf))
new_lines = lines[:bi] + new_body.split("\n") + lines[bi + 1:pi + 1] + pj
new = "\n".join(new_lines)
assert norm(new) == norm(t), "document tokens differ"
print(new[new.index("## Body"):new.index("## Provenance") + 900])

if "--apply" in sys.argv:
    TP.write_text(new, encoding="utf-8"); DP.write_text(new, encoding="utf-8")
    regp = ROOT / "data/registry.json"
    reg = json.loads(regp.read_text(encoding="utf-8"))
    x = next(r for r in reg["deposits"] if r["deposit_number"] in (896, "896"))
    h = hashlib.sha256(new.encode("utf-8")).hexdigest(); g = axn_glyph_from_hash(h)
    before = {"axn": x["axn"], "hash": x["hash"]}
    x.setdefault("axn_prior", []).append({"axn": x["axn"], "hash": x["hash"], "until": ON, "why": "lineation and layout repaired (repair_896_lineation_20261028.py)"})
    x["hash"] = h; x["axn_canonical"] = h; x["emoji"] = g
    x["axn"] = compose_axn(x["hex"], x.get("family", "ARCHIVAL"), g)
    x["clusters"] = axn_clusters_from_hash(h); x["reading"] = axn_reading_from_clusters(x["clusters"]); x["axn_reading"] = x["reading"]
    x["full_text_chars"] = len(new)
    x["lineation_repaired"] = {"on": ON, "poem_lineation_from": "10.5281/zenodo.18459863 (the work's first Zenodo version, 2026-02-02; description preserved by DataCite, data/datacite-full-backup.json)",
                               "field_parts": "deposit instructions, the poem, situating note, keywords and related identifiers set on their own lines; every token kept in order",
                               "provenance": "wrapped paragraphs joined", "hash_before": before["hash"], "axn_before": before["axn"], "ruled_by": RULING}
    rm.touch(x, "axn", "lineation repaired: the poem set in its couplets from the work's first Zenodo version; the description field's parts on their own lines; "
             "the provenance's wrapped paragraphs joined", was=before["axn"], now=x["axn"], when=ON)
    regp.write_text(json.dumps(reg, ensure_ascii=False, indent=1), encoding="utf-8")
    print("applied", x["axn"])
