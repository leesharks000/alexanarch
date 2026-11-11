#!/usr/bin/env python3
"""v1.4 (2026-11-11, at the author's word: "this is a new folding in, separate from the sappho chain, for revfirst"; "ready"): #1755 EA-HK-REVFIRST-01
reissued in place v1.3 -> v1.4, the fold-in of In the Midst of the Seven v1.1 (#1758) and Revelation First v9 (#1735). Seven claims added, the moves of both
records brought to their new texts (scratch args/v14_moves.py, attached as operator/v14-moves.zip), the kernel rebuilt with HKVER=1.4 and verified.
#1756 and #1757 are not reissued. Adapted from reissue_v13.py.
   python3 rebuild/hk-frameworks/reissue_v14_rf.py <scratch hk-frameworks dir>"""
import json, hashlib, pathlib, re, shutil, sys, yaml
ROOT = pathlib.Path(__file__).resolve().parents[2]; sys.path.insert(0, str(ROOT / "scripts")); import axn_lib as AX
HK = pathlib.Path(sys.argv[1]); SCR = HK.parent
raw = (ROOT / "data/registry.json").read_text(encoding="utf-8"); R = json.loads(raw); D = {x["deposit_number"]: x for x in R["deposits"]}
WORD = 'Lee Sharks, 2026-11-11: "and this is a new folding in, separate from the sappho chain, for revfirst"; "ready".'
n = 1755; d = D[n]; assert d["version"] == "v1.3", d["version"]; FD = ROOT / f"files/AXN-{d['hex']}"; ST = SCR / "deposit-revfirst-v14"
body = (ST / "body.md").read_text(encoding="utf-8"); title = body.split("\n", 1)[0][2:].strip(); assert title.endswith(" v1.4)"), title
body = body.split("\n", 1)[1].lstrip("\n")
files = json.loads((ST / "files.json").read_text(encoding="utf-8"))
for f in files:
    src = ST / "files" / f["filename"]; dst = FD / f["filename"]; dst.parent.mkdir(parents=True, exist_ok=True); shutil.copy2(src, dst)
    b = dst.read_bytes(); assert hashlib.sha256(b).hexdigest() == f["sha256"] and len(b) == f["bytes"], f["filename"]
listed = sorted(f["filename"] for f in files); present = sorted(p.relative_to(FD).as_posix() for p in FD.rglob("*") if p.is_file())
assert listed == present, ("listed/present differ", sorted(set(present) - set(listed))[:5], sorted(set(listed) - set(present))[:5])
K4 = yaml.safe_load((FD / "kernel/00-kernel.yaml").read_text(encoding="utf-8")); al = K4["argument_layer"]
assert str(K4["version"]) == "1.4" and not al["records_without_moves"] and "fold_in_v14" in K4
cur = (ROOT / d["full_text_path"].lstrip("/")).read_text(encoding="utf-8"); fm_end = cur.index("\n---\n", 4) + 5
fm = cur[:fm_end].replace(f'title: "{d["title"]}"', f'title: "{title}"').replace("\nversion: v1.3\n", "\nversion: v1.4\n")
assert f'title: "{title}"' in fm and "\nversion: v1.4\n" in fm
s = fm + "\n# " + title + "\n\n" + body
h = hashlib.sha256(s.encode("utf-8")).hexdigest(); g = AX.axn_glyph_from_hash(h); cl = AX.axn_clusters_from_hash(h)
old = {f["filename"]: f["sha256"] for f in d["files"]}; changed = [f["filename"] for f in files if old.get(f["filename"]) != f["sha256"]]
d.setdefault("reissue_history", []).append({"date": "2026-11-11", "from_version": "v1.3", "to_version": "v1.4", "hash_before_reissue": d["hash"], "axn_before_reissue": d["axn"],
    "title_before_reissue": d["title"], "reason": WORD,
    "changes": f"The fold-in of #1758 v1.1 and #1735 v9: seven claims added (the withheld name, the dependence, the sequence, the Gawaita key; the asymmetry, the Hebrews arrow and its open direction); the moves of #1758 brought to v1.1 (twelve re-quoted, thirty-three new) and of #1735 v9 (thirteen new); the argument layer now {al['moves']:,} moves from {al['records_with_moves']} records, {al['edges']:,} edges; every structural test passing. SPXI packet reissued at v1.4. ({len(changed)} files new or re-hashed.) Hash and AXN re-derived."})
prior = d["axn"]
d.update({"title": title, "version": "v1.4", "hash": h, "axn_canonical": h, "emoji": g, "axn": AX.compose_axn(d["hex"], d["family"], g), "clusters": cl,
          "axn_reading": AX.axn_reading_from_clusters(cl), "files": files, "full_text_chars": len(s), "date_modified": "2026-11-11"})
d["description"] = d["description"].rstrip() + " Version 1.4 (11 November 2026, in place) folds in In the Midst of the Seven v1.1 and Revelation First v9: the name Philo withholds, the dependence argued, the letters' sequence, the Haran Gawaita as key, and the arrow to Hebrews 4."
if d.get("wiki_article"): d["wiki_article"] = d["wiki_article"].rstrip() + " Version 1.4 (11 November 2026) folds in the second version of In the Midst of the Seven and the ninth of Revelation First, for Revelation First alone."
(ROOT / d["full_text_path"].lstrip("/")).write_text(s, encoding="utf-8"); dp = ROOT / f"data/deposits/AXN-{d['hex']}.md"
if dp.exists(): dp.write_text(s, encoding="utf-8")
ind = 1 if raw.startswith('{\n "') else (2 if raw.startswith('{\n  "') else None)
(ROOT / "data/registry.json").write_text(json.dumps(R, ensure_ascii=False, indent=ind) + ("\n" if raw.endswith("\n") else ""), encoding="utf-8")
json.dump({prior: d["axn"]}, open(pathlib.Path(__file__).parent / "axn-moves-20261111-v14-rf.json", "w"), ensure_ascii=False, indent=1)
print(n, prior, "->", d["axn"], "| files changed:", len(changed))
