#!/usr/bin/env python3
"""#1770 Who Speaks for the Classics, and on What Basis (MMRS) reissued in place v1.2 -> v1.3 (2026-11-15), at the author's words: 13:19 "we can correct a typo that
emerges from the keyboard, yes, and still achieve that effect"; 13:20 "we can broaden it to 18th and 19th centuries"; 13:21 "18th-19th centuries, but the fetishized
philological object does more consolidating in the 19th". The settlement of which the classical object is the residue is dated to the eighteenth and nineteenth centuries
(§3.5, §3.6), with the 13:21 words in §3.5; the keyboard slip in the quoted words of 21:37 ("object are" -> "objects are") corrected in §2.7 and in the reason of v1.1 in
reissue_history, the words otherwise as typed. Hash and AXN re-derived at the same position and family; the prior hash, AXN and title kept in reissue_history.
   python3 rebuild/hk-frameworks/reissue_who_speaks_v13.py"""
import json, hashlib, pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parents[2]; sys.path.insert(0, str(ROOT / "scripts")); import axn_lib as AX
N = 1770; R = json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8")); d = {x["deposit_number"]: x for x in R["deposits"]}[N]
assert d["version"] == "v1.2", d["version"]
WORD = ('Lee Sharks, 2026-11-15: 13:19 "we can correct a typo that emerges from the keyboard, yes, and still achieve that effect"; 13:20 "we can broaden it to 18th and '
        '19th centuries"; 13:21 "18th-19th centuries, but the fetishized philological object does more consolidating in the 19th".')
Q1321 = 'The author (15 November, 13:21): "the fetishized philological object does more consolidating in the 19th".'
def rep(s, a, b):
    assert s.count(a) == 1, (a[:80], s.count(a)); return s.replace(a, b)
fp = ROOT / d["full_text_path"].lstrip("/"); cur = fp.read_text(encoding="utf-8")
fm_end = cur.index("\n---\n", 4) + 5; fm, body = cur[:fm_end], cur[fm_end:]
fm = rep(fm, "\nversion: v1.2\n", "\nversion: v1.3\n")
body = rep(body, "Lee Sharks · v1.2 · 14 November 2026", "Lee Sharks · v1.3 · 15 November 2026")
body = rep(body, '"if the classical object are fixed', '"if the classical objects are fixed')
body = rep(body, "the residue of a reception, the eighteenth century's, and to read the canon at the centre as that residue. The field holds the instruments for the move",
           "the residue of a reception, that of the eighteenth and nineteenth centuries, and to read the canon at the centre as that residue. " + Q1321 + " The field holds the instruments for the move")
body = rep(body, "from outside the eighteenth-century settlement:", "from outside the settlement of the eighteenth and nineteenth centuries:")
assert "eighteenth century's" not in body and "eighteenth-century settlement" not in body and "classical object are" not in body
s = fm + body
h = hashlib.sha256(s.encode("utf-8")).hexdigest(); g = AX.axn_glyph_from_hash(h); cl = AX.axn_clusters_from_hash(h)
for r in d.get("reissue_history", []):
    r["reason"] = r["reason"].replace("if the classical object are fixed", "if the classical objects are fixed")
d.setdefault("reissue_history", []).append({"date": "2026-11-15", "from_version": "v1.2", "to_version": "v1.3", "hash_before_reissue": d["hash"], "axn_before_reissue": d["axn"],
    "title_before_reissue": d["title"], "reason": WORD, "changes": "§3.5 and §3.6: the settlement of which the classical object is the residue dated to the eighteenth and nineteenth "
    "centuries, with the author's words of 13:21 in §3.5; §2.7 and the reason of v1.1: a keyboard slip corrected in the author's quoted words of 21:37; byline v1.3."})
prior = d["axn"]
d.update({"version": "v1.3", "hash": h, "axn_canonical": h, "emoji": g, "axn": AX.compose_axn(d["hex"], d["family"], g), "clusters": cl, "axn_reading": AX.axn_reading_from_clusters(cl), "full_text_chars": len(s)})
d["description"] = d["description"].rstrip() + (" Version 1.3 (15 November, in place) dates the settlement of which the classical object is the residue to the eighteenth and "
    "nineteenth centuries, the nineteenth doing the most consolidating.")
d["wiki_article"] = d["wiki_article"].rstrip() + (" Version 1.3 dates the settlement whose residue the field keeps as its object to the eighteenth and nineteenth centuries; in "
    "the author's words, 'the fetishized philological object does more consolidating in the 19th'.")
fp.write_text(s, encoding="utf-8")
dp = ROOT / f"data/deposits/AXN-{d['hex']}.md"
if dp.exists(): dp.write_text(s, encoding="utf-8")
(ROOT / "data/registry.json").write_text(json.dumps(R, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
json.dump({prior: d["axn"]}, open(pathlib.Path(__file__).parent / "axn-moves-20261115-who-speaks-v13.json", "w"), ensure_ascii=False, indent=1)
print(N, prior, "->", d["axn"])
