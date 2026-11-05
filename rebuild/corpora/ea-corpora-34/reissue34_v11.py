#!/usr/bin/env python3
"""Reissue #1740 (EA-CORPORA-34) as v1.1, in place, at the operator's word of 2026-11-05 11:11 EST ("lets bundle the 35 sources with 34 and version
in place - theyre of a piece"). The canonical text is rewritten from the regenerated issue body (title, version, keywords and body); its sha256 is the
new hash; the AXN keeps its position (0C12) and family (DATASET) and takes its glyphs from the new hash; the prior hash and AXN go into reissue_history.
    python3 rebuild/corpora/ea-corpora-34/reissue34_v11.py"""
import json, hashlib, pathlib, re, sys
ROOT = pathlib.Path(__file__).resolve().parents[3]; sys.path.insert(0, str(ROOT / "scripts")); import axn_lib as A
issue = (ROOT / "data/issue-bodies/EA-CORPORA-34-issue.md").read_text(encoding="utf-8")
def field(name):
    m = re.search(r"^### " + re.escape(name) + r"\n\n(.*?)(?=\n### |\Z)", issue, re.S | re.M); return m.group(1).strip()
title, desc, kw, body = field("Title"), field("Description"), [k.strip() for k in field("Keywords").split(",")], field("Body")
T = ROOT / "data/texts/AXN-0C12-text.md"; old = T.read_text(encoding="utf-8")
fm_end = old.index("\n---\n", 4) + 5; fm = old[:fm_end]
fm = re.sub(r'^title: ".*"$', 'title: ' + json.dumps(title, ensure_ascii=False), fm, count=1, flags=re.M)
fm = re.sub(r"^version: v1\.0$", "version: v1.1", fm, count=1, flags=re.M)
fm = re.sub(r"^keywords:\n(?:  - .*\n)+", "keywords:\n" + "".join(f"  - {k}\n" for k in kw), fm, count=1, flags=re.M)
new = fm + "\n# " + title + "\n\n" + body.rstrip("\n") + "\n"
h = hashlib.sha256(new.encode("utf-8")).hexdigest()
R = json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8"))
d = next(x for x in R["deposits"] if x["deposit_number"] == 1740)
prior = {"hash": d["hash"], "axn": d["axn"]}
glyph = A.axn_glyph_from_hash(h); cl = A.axn_clusters_from_hash(h)
d.setdefault("reissue_history", []).append({"date": "2026-11-05", "from_version": "v1.0", "to_version": "v1.1", "hash_before_reissue": prior["hash"],
    "axn_before_reissue": prior["axn"], "reason": "Lee Sharks, 2026-11-05: \"we should also be tracking material manuscript transmission and succession, that seems particularly important with revelation and less-often and -critically studied than pure reception\" (11:02 EST); \"lets bundle the 35 sources with 34 and version in place - theyre of a piece\" (11:11 EST)",
    "changes": "Four seats added, 34/12–34/15 (Scrivener 1894, Delitzsch 1861, Tregelles 1854, Erasmus 1516): the carriage of the Apocalypse, seated first as EA-CORPORA-35 (not deposited) and folded into this seating; title, description, keywords, body and wiki article to v1.1. The eleven seats of v1.0 are unchanged."})
d.update({"title": title, "description": desc, "keywords": kw, "version": "v1.1", "hash": h, "axn_canonical": h, "emoji": glyph,
          "axn": A.compose_axn("0C12", "DATASET", glyph), "clusters": cl, "axn_reading": A.axn_reading_from_clusters(cl)})
d["wiki_article"] = d["wiki_article"].replace("Its eleven seats, 19 works and some 601,000 lines of text layer carry", "Its fifteen seats, 24 works and some 819,000 lines of text layer carry")
d["wiki_article"] += (" Version 1.1 (5 November 2026) adds the carriage of the book (34/12–34/15): Scrivener's Plain Introduction (1894), Delitzsch's Handschriftliche Funde (1861), "
    "Tregelles's Account of the Printed Text (1854) and Erasmus's Novum Instrumentum of 1516, for the one manuscript from which the first printed Apocalypse was made and the last six verses supplied from the Latin.")
T.write_text(new, encoding="utf-8"); (ROOT / "data/deposits/AXN-0C12.md").write_text(new, encoding="utf-8")
(ROOT / "data/registry.json").write_text(json.dumps(R, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
print("prior", prior["axn"], prior["hash"][:12], "→", d["axn"], h[:12])
