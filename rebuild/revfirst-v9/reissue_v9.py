#!/usr/bin/env python3
"""Reissue in place: #1735 Revelation First, v8 -> v9, at the author's word of 2026-11-11 04:37 ("its live..lets go ahead and version"), #1758 v1.1
being live. The text is rebuild/revfirst-v9/REVFIRST-v9-draft.md (draft_v9.py). Hash and AXN re-derived at the same position and family; the prior
hash, AXN and title kept in reissue_history.   python3 rebuild/revfirst-v9/reissue_v9.py"""
import json, hashlib, pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parents[2]; sys.path.insert(0, str(ROOT / "scripts")); import axn_lib as A
raw = (ROOT / "data/registry.json").read_text(encoding="utf-8"); R = json.loads(raw); D = {x["deposit_number"]: x for x in R["deposits"]}
n = 1735; d = D[n]; assert d["version"] == "v8", d["version"]
H = pathlib.Path(__file__).parent; s = (H / "REVFIRST-v9-draft.md").read_text(encoding="utf-8")
for chk in ("\nversion: v9\n", "v9 (11 November 2026, in place)", '"version": "9"', "A second arrow runs from the same scene"): assert chk in s, chk
h = hashlib.sha256(s.encode("utf-8")).hexdigest(); g = A.axn_glyph_from_hash(h); cl = A.axn_clusters_from_hash(h)
d.setdefault("reissue_history", []).append({"date": "2026-11-11", "from_version": "v8", "to_version": "v9", "hash_before_reissue": d["hash"], "axn_before_reissue": d["axn"],
    "title_before_reissue": d["title"], "reason": 'Lee Sharks, 2026-11-11: "this is a new folding in, separate from the sappho chain, for revfirst"; "yes, lets start the draft"; "its live..lets go ahead and version"',
    "changes": "From In the Midst of the Seven v1.1 (#1758): in VI.1 the dependence on the Philonic organization with the richer alternatives counted (Wisdom 18.15-16, 18.24; Isaiah 49.2; Judges 5.31; Ezekiel 9.2), Zechariah 3 and the withheld name as a second extant antecedent, Justin's apocalypse of the high priest (Dial. 115.4, 116.1); in IV.1 the Haran Gawaita as a late witness; in VI.3 the arrow to Hebrews 4.8-14, drawn and not run; their conditions in VIII; IX; abstract; five bibliography entries; SPXI packet. Nothing in v8 removed. Hash and AXN re-derived."})
prior = d["axn"]
d.update({"version": "v9", "hash": h, "axn_canonical": h, "emoji": g, "axn": A.compose_axn(d["hex"], d["family"], g), "clusters": cl,
          "axn_reading": A.axn_reading_from_clusters(cl), "full_text_chars": len(s), "date_modified": "2026-11-11"})
d["description"] = d["description"].rstrip() + (" Version 9 (11 November 2026, in place) traces the figure in the midst to Zechariah's vision of Ἰησοῦς the high priest, robed in the ποδήρης and twice given the name Ἀνατολή, "
    "which Philo takes for the Logos while withholding its addressee, and sets the Philonic organization of the scene as its antecedent against the richer alternatives (#1758 v1.1); "
    "it draws a second arrow, not yet run, to Hebrews 4.8–14, which gathers the two Joshuas, the two-edged word and the great high priest named Jesus.")
if d.get("wiki_article"):
    d["wiki_article"] = d["wiki_article"].rstrip() + (" Version 9 (11 November 2026) adds, from the second version of In the Midst of the Seven, Zechariah's vision of Joshua the high priest and Philo's "
        "organization of the lampstand as antecedents of the figure in the midst, and an arrow toward Hebrews 4.8–14, left unrun.")
if isinstance(d.get("keywords"), list):
    for k in ["Zechariah 3", "Joshua the high priest", "Hebrews 4", "Justin Martyr", "Haran Gawaita"]:
        if k not in d["keywords"]: d["keywords"].append(k)
(ROOT / d["full_text_path"].lstrip("/")).write_text(s, encoding="utf-8"); dp = ROOT / f"data/deposits/AXN-{d['hex']}.md"
if dp.exists(): dp.write_text(s, encoding="utf-8")
ind = 1 if raw.startswith('{\n "') else (2 if raw.startswith('{\n  "') else None)
(ROOT / "data/registry.json").write_text(json.dumps(R, ensure_ascii=False, indent=ind) + ("\n" if raw.endswith("\n") else ""), encoding="utf-8")
json.dump({prior: d["axn"]}, open(H / "axn-moves-20261111-v9.json", "w"), ensure_ascii=False, indent=1)
print(n, prior, "->", d["axn"])
