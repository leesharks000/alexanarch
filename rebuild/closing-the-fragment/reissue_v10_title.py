#!/usr/bin/env python3
"""Reissue in place: #1749 v9 -> v10, the title only, at the author's word of 2026-11-10 (21:31: "i wonder why i changed the title of closing the fragment
from i must dare all? thats a better title"; 21:58: "adopted on all"). The title was never changed: on 27 July the author called Closing the Fragment
"bland", "but we'll worry about that later"; "But I Must Dare All" was proposed that evening as the strongest candidate, and the question stayed open in the
submission's provenance record ("Decide before the citation record forms"). The subtitle is kept as the article now has it. Former title kept as a keyword.
Hash and AXN re-derived at the same position and family, the prior hash, AXN and title kept in reissue_history.
   python3 rebuild/closing-the-fragment/reissue_v10_title.py"""
import json, hashlib, pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parents[2]; sys.path.insert(0, str(ROOT / "scripts")); import axn_lib as A
raw = (ROOT / "data/registry.json").read_text(encoding="utf-8"); R = json.loads(raw); D = {x["deposit_number"]: x for x in R["deposits"]}
d = D[1749]; assert d["version"] == "v9", d["version"]
OLD = "Closing the Fragment: Sappho 31 and the Composition Layer as a Surface of Classical Reception"
NEW = "“But I Must Dare All”: Sappho 31 and the Composition Layer as a Surface of Classical Reception"
p = ROOT / d["full_text_path"].lstrip("/"); s = p.read_text(encoding="utf-8")
s = s.replace(f'title: "{OLD} (v9)"', f'title: "{NEW} (v10)"', 1).replace("\nversion: v9\n", "\nversion: v10\n", 1)
s = s.replace("  - Closing the Fragment\n", "  - But I Must Dare All\n  - Closing the Fragment\n", 1)
s = s.replace(f"\n# {OLD} (v9)\n", f"\n# {NEW} (v10)\n", 1)
B9 = "Lee Sharks · v9 · 8 November 2026 · Machine-Mediated Reception Studies · reissued in place from v8 (#1749)"
assert B9 in s; s = s.replace(B9, "Lee Sharks · v10 · 10 November 2026 · Machine-Mediated Reception Studies · reissued in place from v9 (#1749), retitled; v9 reissued in place from v8", 1)
N0 = "### 0. Note on this version\n\n"
assert N0 in s
s = s.replace(N0, N0 + ("v10 (10 November 2026) changes the title and nothing else. The article was deposited as *Closing the Fragment*; on 27 July the author had called "
    "that title bland and left the question for later, and the line the composition supplied, “But I must dare all.”, was then put forward as the main title, "
    "with the argument in the subtitle. The author adopted it on 10 November. The subtitle is the one the article now carries.\n\n"), 1)
for chk in (f'title: "{NEW} (v10)"', "\nversion: v10\n", f"\n# {NEW} (v10)\n", "· v10 ·"): assert chk in s, chk
h = hashlib.sha256(s.encode("utf-8")).hexdigest(); g = A.axn_glyph_from_hash(h); cl = A.axn_clusters_from_hash(h)
d.setdefault("reissue_history", []).append({"date": "2026-11-10", "from_version": "v9", "to_version": "v10", "hash_before_reissue": d["hash"], "axn_before_reissue": d["axn"],
    "title_before_reissue": d["title"], "reason": 'Lee Sharks, 2026-11-10: "i wonder why i changed the title of closing the fragment from i must dare all? thats a better title"; "adopted on all"',
    "changes": "Retitled “But I Must Dare All”, subtitle kept; byline and the note on this version record the change; former title kept as a keyword. Nothing else changed. Hash and AXN re-derived."})
prior = d["axn"]
d.update({"title": f"{NEW} (v10)", "version": "v10", "hash": h, "axn_canonical": h, "emoji": g, "axn": A.compose_axn(d["hex"], d["family"], g), "clusters": cl,
          "axn_reading": A.axn_reading_from_clusters(cl), "full_text_chars": len(s), "date_modified": "2026-11-10"})
if isinstance(d.get("keywords"), list) and "But I Must Dare All" not in d["keywords"]: d["keywords"].insert(0, "But I Must Dare All")
d["description"] = d["description"].rstrip() + " Version 10 (10 November 2026, in place) retitles the article “But I Must Dare All”, the line the composition supplied; it was deposited as Closing the Fragment."
if d.get("wiki_article"): d["wiki_article"] = d["wiki_article"].rstrip() + " Version 10 (10 November 2026) retitled the article “But I Must Dare All”; versions 1 to 9 carry the title Closing the Fragment."
p.write_text(s, encoding="utf-8"); dp = ROOT / f"data/deposits/AXN-{d['hex']}.md"
if dp.exists(): dp.write_text(s, encoding="utf-8")
ind = 1 if raw.startswith('{\n "') else (2 if raw.startswith('{\n  "') else None)
(ROOT / "data/registry.json").write_text(json.dumps(R, ensure_ascii=False, indent=ind) + ("\n" if raw.endswith("\n") else ""), encoding="utf-8")
print(1749, prior, "->", d["axn"])
