#!/usr/bin/env python3
"""#1770 Who Speaks for the Classics, and on What Basis (MMRS) reissued in place v1.0 -> v1.1 (2026-11-14), at the author's words: 21:37 "if the classical object
are fixed then they are not studying the reception of the classics they are administering the classics as sovereign objects in their control"; 21:40 "this is often the
monetary shear, my guess would be more so when dealing with more subaltern literature - the alignment with the classical object is not a fixed quality of the receiver but a
primary operation of the journal"; 21:41 "adopted. lets reissue". The body gains §2.7 (alignment as the journal's operation, read through the monetary shear of #1631) and
the version line moves to v1.1. Hash and AXN re-derived at the same position and family; the prior hash, AXN and title kept in reissue_history.
   python3 rebuild/hk-frameworks/reissue_who_speaks_v11.py"""
import json, hashlib, pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parents[2]; sys.path.insert(0, str(ROOT / "scripts")); import axn_lib as AX
N = 1770; R = json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8")); d = {x["deposit_number"]: x for x in R["deposits"]}[N]
assert d["version"] == "v1.0", d["version"]
WORD = ('Lee Sharks, 2026-11-14: 21:37 "if the classical object are fixed then they are not studying the reception of the classics they are administering the classics as '
        'sovereign objects in their control"; 21:40 "this is often the monetary shear, my guess would be more so when dealing with more subaltern literature - the alignment with '
        'the classical object is not a fixed quality of the receiver but a primary operation of the journal"; 21:41 "adopted. lets reissue".')
P27 = ('2.7 **Alignment as the journal\'s operation.** The author (14 November, 21:37): "if the classical object are fixed then they are not studying the reception of the classics '
       'they are administering the classics as sovereign objects in their control". And at 21:40: "the alignment with the classical object is not a fixed quality of the receiver '
       'but a primary operation of the journal". A receiving work arrives as a whole field: its own tradition, its own account of how the classics were made, its own readers. The '
       'journal shears it into the form its grammar admits, a reception of a fixed classical object (153 of 185; 141 from source to later work). In the terms of #1631, the relation '
       'of alignment retains operative standing, and the rest of the work\'s field goes dark to the journal\'s form while remaining in the work. The shear is productive: the darker '
       'the work\'s own claims, the more cleanly it reads as classical reception. The editor\'s article shows it at its loci: Soyinka\'s dispute over the origin of drama redirected '
       'to his authenticity, Ogun measured as "a more developed, more complex kind of Dionysus", four of six points of contact absent (§4.6–4.8). The more subaltern the literature, '
       'the less of its field the classical grammar already holds, and the more the shear takes. What it yields, the article, its citations and its standing, is recorded at the '
       'centre and sold back behind the subscription (§3.4.1).\n\n')
fp = ROOT / d["full_text_path"].lstrip("/"); cur = fp.read_text(encoding="utf-8")
fm_end = cur.index("\n---\n", 4) + 5; fm, body = cur[:fm_end], cur[fm_end:]
assert "\nversion: v1.0\n" in fm and body.count("## 3. The object was made") == 1 and "2.7 **Alignment" not in body
fm = fm.replace("\nversion: v1.0\n", "\nversion: v1.1\n")
body = body.replace("Lee Sharks · v1.0 · 14 November 2026", "Lee Sharks · v1.1 · 14 November 2026", 1).replace("## 3. The object was made", P27 + "## 3. The object was made", 1)
s = fm + body
h = hashlib.sha256(s.encode("utf-8")).hexdigest(); g = AX.axn_glyph_from_hash(h); cl = AX.axn_clusters_from_hash(h)
d.setdefault("reissue_history", []).append({"date": "2026-11-14", "from_version": "v1.0", "to_version": "v1.1", "hash_before_reissue": d["hash"], "axn_before_reissue": d["axn"],
    "title_before_reissue": d["title"], "reason": WORD, "changes": "§2.7 added: alignment with the classical object as the journal's operation on the receiving work, read through the monetary shear (#1631); byline v1.1."})
prior = d["axn"]
d.update({"version": "v1.1", "hash": h, "axn_canonical": h, "emoji": g, "axn": AX.compose_axn(d["hex"], d["family"], g), "clusters": cl, "axn_reading": AX.axn_reading_from_clusters(cl), "full_text_chars": len(s)})
d["description"] = d["description"].rstrip() + (" Version 1.1 (the same day, in place) adds §2.7: alignment with the classical object is the journal's operation on the receiving work, a "
    "productive shear (#1631) in which the work's own claims go dark to the journal's form, taking most from the most subaltern literature.")
d["wiki_article"] = d["wiki_article"].rstrip() + (" Version 1.1 adds that alignment with the classical object is an operation the journal performs on the receiving work: in the terms of "
    "the archive's monetary shear (#1631), the relation of alignment keeps operative standing while the work's own tradition and its claims about the making of the classics go dark, "
    "and the shear takes most from the most subaltern literature.")
if 1631 not in d.setdefault("related_deposits", []): d["related_deposits"].append(1631)
fp.write_text(s, encoding="utf-8")
dp = ROOT / f"data/deposits/AXN-{d['hex']}.md"
if dp.exists(): dp.write_text(s, encoding="utf-8")
(ROOT / "data/registry.json").write_text(json.dumps(R, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
json.dump({prior: d["axn"]}, open(pathlib.Path(__file__).parent / "axn-moves-20261114-who-speaks-v11.json", "w"), ensure_ascii=False, indent=1)
print(N, prior, "->", d["axn"])
