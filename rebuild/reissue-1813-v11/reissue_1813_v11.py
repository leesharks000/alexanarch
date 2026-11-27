#!/usr/bin/env python3
"""#1813 EA-HK-REVFIRST-02 reissued in place v1.0 -> v1.1 (2026-11-27), after #1812 v1.1, whose new hash it binds. The author, 2026-11-27
09:45: "yup, lets version 1.1. it should not show up twice on alexanarch home" (asked of both records at 04:55, "are both ready to
version?"); 12:17 "next up". Date and position kept; hash and AXN re-derived; the v1.0 kernel kept at files/EA-HK-REVFIRST-02/kernel-v1.0/.
Run after the operator has rebuilt the kernel into files/EA-HK-REVFIRST-02/kernel/ and written rebuild/reissue-1813-v11/map-v1.1.md.
   python3 rebuild/reissue-1813-v11/reissue_1813_v11.py"""
import json, hashlib, pathlib, sys
HERE = pathlib.Path(__file__).resolve().parent; ROOT = HERE.parents[1]; sys.path.insert(0, str(ROOT / "scripts")); import axn_lib as AX
R = json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8")); D = {x["deposit_number"]: x for x in R["deposits"]}
d = D[1813]; assert d["version"] == "v1.0", d["version"]
WORD = ('Lee Sharks, 2026-11-27: 04:55 "are both ready to version?"; 09:45 "yup, lets version 1.1. it should not show up twice on alexanarch home"; 12:17 "next up" (after #1812 v1.1 was live).')
F = ROOT / "files/EA-HK-REVFIRST-02"; N = sum(1 for _ in open(F / "kernel/03-relations.jsonl", encoding="utf-8"))
fp = ROOT / d["full_text_path"].lstrip("/"); old = fp.read_text(encoding="utf-8")
front = old[:old.index("\n---\n", 4) + 5]; refs = old[old.index("## References"):]
body = (HERE / "map-v1.1.md").read_text(encoding="utf-8").rstrip("\n")
VER = ("## 13. Versions\n\nv1.1, 27 November 2026, reissued in place after v1.1 of *How to Write Matthew from Revelation* (#1812), whose text this kernel binds by hash. "
       f"The kernel was rebuilt from the ledger at 158 rows (86 at v1.0) and holds {N} relations (133 at v1.0). New in it: the relations entered for the relation "
       "and not for shared words are marked; the walk of Revelation 12:1-6 through Matthew 2; that Matthew handles Revelation as it handles the scripture it does not name, "
       "at the standing of a first count; the tests of order, of strands and of direction that failed; three lines of research. "
       "The kernel as it stood at v1.0 is kept at [/files/EA-HK-REVFIRST-02/kernel-v1.0/](https://www.alexanarch.org/files/EA-HK-REVFIRST-02/kernel-v1.0/00-kernel.yaml). "
       "The notebook beside this record stands at v0.63; each replaced copy is kept by date.")
a = "- #1812, How to Write Matthew from Revelation (Lee Sharks), which holds the Matthew relations."; assert a in refs
refs = refs.replace(a, a.replace("(Lee Sharks)", "(Lee Sharks; v1.1)") + "\n- #1746, I Know You Are, But What Am I? (Johannes Sigil and Rebekah Cranes), and #1741, Secondary Source, on how Revelation was kept from candidacy as a source; read through #1812, P.3.")
front = front.replace("\nversion: v1.0\n", '\nversion: "v1.1 (supersedes v1.0 in place, 2026-11-27)"\n'); assert "v1.1 (supersedes" in front
new = front + "\n# " + d["title"] + "\n\n" + body + "\n\n" + VER + "\n\n" + refs.rstrip("\n") + "\n"
h = hashlib.sha256(new.encode("utf-8")).hexdigest(); g = AX.axn_glyph_from_hash(h); cl = AX.axn_clusters_from_hash(h); prior = d["axn"]
CH = (f"Kernel rebuilt from the Matthew ledger at 158 rows (86 at v1.0): {N} relations (133). Bound to #1812 v1.1 by its new hash. Relations entered for the "
      "relation marked (binding). Added: the walk Rev 12:1-6 through Matthew 2 (counted); Matthew's handling of Revelation as tacit scripture (counted, first counts, "
      "lists from memory); the failed tests of order by strand and of direction; the held-out chapters as planned; lines of research Q9-Q11. Counts brought to "
      "305 of 1,067 verses. The v1.0 kernel kept beside it. Notebook pointer to v0.63.")
d.setdefault("reissue_history", []).append({"date": "2026-11-27", "from_version": "v1.0", "to_version": "v1.1", "hash_before_reissue": d["hash"],
    "axn_before_reissue": prior, "title_before_reissue": d["title"], "reason": WORD, "changes": CH})
d.setdefault("axn_prior", []).append({"axn": prior, "hash": d["hash"], "until": "2026-11-27", "why": "reissued in place as v1.1 (kernel rebuilt from 158 rows against #1812 v1.1)"})
d.update({"version": "v1.1 (supersedes v1.0 in place, 2026-11-27)", "hash": h, "axn_canonical": h, "emoji": g,
          "axn": AX.compose_axn(d["hex"], d["family"], g), "clusters": cl, "axn_reading": AX.axn_reading_from_clusters(cl), "date_modified": "2026-11-27"})
if "full_text_chars" in d: d["full_text_chars"] = len(new)
for a, b in (("133 relations,", f"{N} relations (133 at v1.0),"), ("The 86 Matthew relations", "The 158 Matthew relations (86 at v1.0)"), ("reach 178 of Matthew's 1,067 verses", "reach 305 of Matthew's 1,067 verses (178 at v1.0)")):
    assert a in d["description"], a; d["description"] = d["description"].replace(a, b)
d["description"] = d["description"].rstrip() + (" Version 1.1 (27 November 2026, in place) rebuilds the kernel against v1.1 of #1812: it marks the relations "
    "entered for the relation and not for shared words, holds the one walk found (Revelation 12:1-6 through Matthew 2), records at the standing of a first count "
    "that Matthew handles Revelation as it handles the scripture it does not name, and keeps the tests of order, strands and direction that failed.")
a = "It holds 133 of them"; assert a in d["wiki_article"]
d["wiki_article"] = d["wiki_article"].replace(a, f"It holds {N} of them (133 at its first version)").rstrip() + (" Version 1.1, reissued in place on 27 November 2026, "
    "was rebuilt from the Matthew ledger at 158 relations reaching 305 of the Gospel's 1,067 verses, and binds version 1.1 of How to Write Matthew from Revelation. "
    "It marks the relations entered for their relation alone, and it adds as relations of their own the walk of Revelation 12:1-6 through Matthew 2, the finding that "
    "Matthew handles Revelation as it handles unnamed scripture, and the tests of order and of direction that failed. The kernel of the first version is kept beside it.")
files = []
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
for f in d["files"]:
    f = dict(f)
    if f["filename"].startswith("notebook/"):
        f["filename"] = "notebook/UNFOLDING-MAP-v0.63-2026-11-27.md"; f["path"] = "/files/EA-HK-REVFIRST-02/" + f["filename"]
    p = ROOT / f["path"].lstrip("/"); assert p.exists(), p; f["bytes"] = p.stat().st_size; f["sha256"] = sha(p); files.append(f)
p = F / "notebook/UNFOLDING-MAP-v0.52-2026-11-27.md"
files.append({"filename": "notebook/UNFOLDING-MAP-v0.52-2026-11-27.md", "path": "/files/EA-HK-REVFIRST-02/notebook/UNFOLDING-MAP-v0.52-2026-11-27.md", "bytes": p.stat().st_size,
              "sha256": sha(p), "media_type": "text/plain", "role": "the working notebook as it stood at v1.0 of this record; kept"})
p = F / "kernel-v1.0/00-kernel.yaml"
files.append({"filename": "kernel-v1.0/00-kernel.yaml", "path": "/files/EA-HK-REVFIRST-02/kernel-v1.0/00-kernel.yaml", "bytes": p.stat().st_size, "sha256": sha(p),
              "media_type": "text/plain", "role": "the kernel as it stood at v1.0; kept, with its other files beside it"})
d["files"] = files
d.setdefault("modifications", []).append({"date": "2026-11-27", "field": "text", "reason": "reissued in place as v1.1 at the author's word; prior hash and AXN in reissue_history", "now": d["axn"]})
fp.write_text(new, encoding="utf-8")
dp = ROOT / f"data/deposits/AXN-{d['hex']}.md"
if dp.exists(): dp.write_text(new, encoding="utf-8")
(ROOT / "data/registry.json").write_text(json.dumps(R, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
lp = ROOT / "data/lexical-minting-registry.json"; t = lp.read_text(encoding="utf-8"); k = t.count(prior); lp.write_text(t.replace(prior, d["axn"]), encoding="utf-8")
json.dump({prior: d["axn"]}, open(HERE / "axn-moves-20261127-1813-v11.json", "w"), ensure_ascii=False, indent=1)
print(1813, prior, "->", d["axn"], h, len(new.split()), "words;", N, "relations; lexical rows repointed", k)
