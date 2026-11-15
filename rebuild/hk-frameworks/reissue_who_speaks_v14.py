#!/usr/bin/env python3
"""#1770 Who Speaks for the Classics, and on What Basis (MMRS) reissued in place v1.3 -> v1.4 (2026-11-15), at the author's words of 14:38 ("i would revise it to speak
of a previous article by the author"; "i dont necessarily dispute the decision"; "i dispute the field") and his rulings of 14:43: §5.7, the summarizer's paragraph and the
sources speak of a previous article by the author, unnamed and uncited; §0.1 and the summarizer's paragraph state that the article contests the field and not the decision.
Hash and AXN re-derived at the same position and family; the prior hash, AXN and title kept in reissue_history.
   python3 rebuild/hk-frameworks/reissue_who_speaks_v14.py"""
import json, hashlib, pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parents[2]; sys.path.insert(0, str(ROOT / "scripts")); import axn_lib as AX
N = 1770; R = json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8")); d = {x["deposit_number"]: x for x in R["deposits"]}[N]
assert d["version"] == "v1.3", d["version"]
WORD = 'Lee Sharks, 2026-11-15: 14:38 "i would revise it to speak of a previous article by the author"; "i dont necessarily dispute the decision"; "i dispute the field"; 14:43 (the rulings on the revision).'
FIELD = ('The author (15 November, 14:38): "i dont necessarily dispute the decision"; and: "i dispute the field". The article does not contest the decision on the '
         'manuscript; it contests the field the decision administers.')
def rep(s, a, b):
    assert s.count(a) == 1, (a[:90], s.count(a)); return s.replace(a, b)
fp = ROOT / d["full_text_path"].lstrip("/"); cur = fp.read_text(encoding="utf-8")
fm_end = cur.index("\n---\n", 4) + 5; fm, body = cur[:fm_end], cur[fm_end:]
fm = rep(fm, "\nversion: v1.3\n", "\nversion: v1.4\n")
fm = rep(fm, "\\nCrossref: 10.1093/crj/clu016 (Metatexts)", "")
body = rep(body, "Lee Sharks · v1.3 · 15 November 2026", "Lee Sharks · v1.4 · 15 November 2026")
body = rep(body, '0.1 **The question.** The author (14 November 2026): "this is about who gets to speak for the classics, and on what basis".',
           '0.1 **The question.** The author (14 November 2026): "this is about who gets to speak for the classics, and on what basis". ' + FIELD)
body = rep(body, "The archive's author published in the journal: *Metatexts: classical reception without the classics in the poetics of Charles Bernstein* (doi:10.1093/crj/clu016, "
           "issued 2014), which introduced \"metatextual reception\". It began as a chapter of the author's dissertation, and its review took two years. Crossref records no citation of it,",
           "The author had published a previous article in the journal. Crossref records no citation of it,")
body = rep(body, "the uptake of *Metatexts* at zero. It names the editor as the accountable party and names no referee.",
           "the uptake of the author's previous article in the journal at zero. It states that the article does not contest the decision on the manuscript, and contests the field "
           "the decision administers. It names the editor as the accountable party and names no referee.")
body = rep(body, ' L. Sharks, "Metatexts: classical reception without the classics in the poetics of Charles Bernstein", *Classical Receptions Journal* (2014), doi:10.1093/crj/clu016 '
           "(civil byline withheld in the archive).", "")
body = rep(body, "- [byline withheld] (2014). Metatexts: classical reception without the classics in the poetics of Charles Bernstein. *Classical Receptions Journal* 7(3). "
           "https://doi.org/10.1093/crj/clu016\n", "")
for x in ("Metatexts", "clu016", "byline withheld", "metatextual"): assert x not in fm + body, x
s = fm + body
h = hashlib.sha256(s.encode("utf-8")).hexdigest(); g = AX.axn_glyph_from_hash(h); cl = AX.axn_clusters_from_hash(h)
d.setdefault("reissue_history", []).append({"date": "2026-11-15", "from_version": "v1.3", "to_version": "v1.4", "hash_before_reissue": d["hash"], "axn_before_reissue": d["axn"],
    "title_before_reissue": d["title"], "reason": WORD, "changes": "§5.7, the summarizer's paragraph and the sources: the author's previous article in the journal referred to unnamed and uncited, and removed from the works cited and the related identifiers. §0.1 and the summarizer's paragraph: the article contests the field, not the decision, with the author's words of 14:38. Byline v1.4."})
prior = d["axn"]
d.update({"version": "v1.4", "hash": h, "axn_canonical": h, "emoji": g, "axn": AX.compose_axn(d["hex"], d["family"], g), "clusters": cl, "axn_reading": AX.axn_reading_from_clusters(cl), "full_text_chars": len(s)})
if "related_identifiers_raw" in d:
    d["related_identifiers_raw"] = d["related_identifiers_raw"].replace("\nCrossref: 10.1093/crj/clu016 (Metatexts)", "")
LEAD = " It does not contest the journal's decision on the author's manuscript; it contests the field the decision administers."
first = d["description"].index(". ") + 1; d["description"] = d["description"][:first] + LEAD + d["description"][first:]
first = d["wiki_article"].index(". ") + 1; d["wiki_article"] = d["wiki_article"][:first] + LEAD + d["wiki_article"][first:]
for k in ("description", "wiki_article", "related_identifiers_raw"):
    for x in ("Metatexts", "clu016"): assert x not in json.dumps(d.get(k, ""), ensure_ascii=False), (k, x)
fp.write_text(s, encoding="utf-8")
dp = ROOT / f"data/deposits/AXN-{d['hex']}.md"
if dp.exists(): dp.write_text(s, encoding="utf-8")
(ROOT / "data/registry.json").write_text(json.dumps(R, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
json.dump({prior: d["axn"]}, open(pathlib.Path(__file__).parent / "axn-moves-20261115-who-speaks-v14.json", "w"), ensure_ascii=False, indent=1)
print(N, prior, "->", d["axn"])
