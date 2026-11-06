#!/usr/bin/env python3
"""Reissue #1746 as v1.1 in place from drafts/Q-draft-2026-11-06.md (on ChatGPT's review); the AXN keeps 0C29 and GENERATIVE, its glyphs from the new hash; prior hash and AXN to reissue_history."""
import json, hashlib, pathlib, re, sys
ROOT = pathlib.Path(__file__).resolve().parents[2]; sys.path.insert(0, str(ROOT / "scripts")); import axn_lib as A
R = json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8")); d = next(x for x in R["deposits"] if x["deposit_number"] == 1746)
assert d["version"] == "v1.0"
T = ROOT / d["full_text_path"].lstrip("/"); old = T.read_text(encoding="utf-8"); fm = old[:old.index("\n---\n", 4) + 5]
fm2 = re.sub(r"^version: v1\.0$", "version: v1.1", fm, count=1, flags=re.M); assert fm2 != fm
dr = (ROOT / "drafts/Q-draft-2026-11-06.md").read_text(encoding="utf-8"); title = dr.split("\n", 1)[0][2:].strip(); body = dr[dr.index("\n\n") + 2:]
new = fm2 + "\n# " + title + "\n\n" + body
h = hashlib.sha256(new.encode("utf-8")).hexdigest(); g = A.axn_glyph_from_hash(h); cl = A.axn_clusters_from_hash(h)
d.setdefault("reissue_history", None)
if not d["reissue_history"]: d["reissue_history"] = []
d["reissue_history"].append({"date": "2026-11-06", "from_version": "v1.0", "to_version": "v1.1", "hash_before_reissue": d["hash"], "axn_before_reissue": d["axn"],
    "reason": "ChatGPT's review of v0.2/v1.0, supplied by Lee Sharks 2026-11-06 12:58, each point checked before it was taken",
    "changes": "Allen's ICC Matthew (1907) entered with Merx's gloss proposal and the Sinaitic Syriac omission; the four-power claim restated (after 1843; Hitzig's grant withdrawn by the stratum); objects kept distinct; Weiss's result kept with Markan priority; Holtzmann's rule and Harnack's selection rule shown at their loci; reception events tabulated; composition-layer finding restated with Documenta Q's own statement; census method and links given; conditions separated by claim; Feist comparison restated. Hash and AXN re-derived from the new bytes."})
prior = d["axn"]
d.update({"version": "v1.1", "hash": h, "axn_canonical": h, "emoji": g, "axn": A.compose_axn(d["hex"], d["family"], g), "clusters": cl, "axn_reading": A.axn_reading_from_clusters(cl)})
d["wiki_article"] = d["wiki_article"].replace("Read in thirteen works from Lachmann (1835) to Streeter (1924), seven of them seated in the original languages as EA-CORPORA-35 (#1744) and six read by reference,", "Read in fourteen works from Lachmann (1835) to Streeter (1924), seven of them seated in the original languages as EA-CORPORA-35 (#1744) and seven read by reference,")
d["wiki_article"] = d["wiki_article"].replace("the reconstructed sources (Holtzmann's A and Λ, Wernle's Q, the apocalypse reconstructed beneath Mark 13) hold all four, and the extant Apocalypse of John holds none:", "the reconstructed sources (Holtzmann's A and Λ, Wernle's Q, the apocalypse reconstructed beneath Mark 13) hold all four at every locus read after 1843, and the extant Apocalypse of John holds none there:")
d["wiki_article"] += " Version 1.1, the same day, takes ChatGPT's review: it enters W. C. Allen's International Critical Commentary on Matthew (1907), which calls the agreement of Matt 24:30 and Rev 1:7 \"certainly curious\", reports Merx's proposal that Matthew's clause is a gloss from Rev 1:7, and supplies a commonplace of Christian apocalyptic study in place of either book; it keeps the reconstructed objects distinct and separates the paper's three claims and their conditions."
T.write_text(new, encoding="utf-8"); (ROOT / f"data/deposits/AXN-{d['hex']}.md").write_text(new, encoding="utf-8")
(ROOT / "data/registry.json").write_text(json.dumps(R, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
print(prior, "->", d["axn"])
