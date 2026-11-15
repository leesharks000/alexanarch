#!/usr/bin/env python3
"""#1769 Daffodils (EA-HK-DAFFODILS-01) reissued in place v1.5 -> v1.6 (2026-11-15), at the author's words: 13:19 "we can correct a typo that emerges from the keyboard,
yes, and still achieve that effect"; 13:20 "we can broaden it to 18th and 19th centuries"; 13:21 "18th-19th centuries, but the fetishized philological object does more
consolidating in the 19th"; 14:02 "point of contact as an abstract noun phrase, leave as is; the received reading *of". The settlement of which the classical object is the
residue is dated to the eighteenth and nineteenth centuries (§7.11.4, §7.11.5, the table), with the 13:21 words; keyboard slips corrected in three quoted messages (17:40
"if" -> "of", 21:37 "object are" -> "objects are", 16:14 "evalautor" -> "evaluator"), the words otherwise as typed, including in the reason of v1.4 in reissue_history.
Package rebuilt from map v1.6; hash and AXN re-derived at the same position and family, the prior kept in reissue_history.
   python3 rebuild/hk-frameworks/reissue_daffodils_v16.py <staged daffodils-hk dir>"""
import json, hashlib, pathlib, shutil, sys, mimetypes
ROOT = pathlib.Path(__file__).resolve().parents[2]; sys.path.insert(0, str(ROOT / "scripts")); import axn_lib as AX
ST = pathlib.Path(sys.argv[1]); N = 1769
R = json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8")); D = {x["deposit_number"]: x for x in R["deposits"]}
d = D[N]; assert d["version"] == "v1.5", d["version"]
FD = ROOT / f"files/AXN-{d['hex']}"
WORD = ('Lee Sharks, 2026-11-15: 13:19 "we can correct a typo that emerges from the keyboard, yes, and still achieve that effect"; 13:20 "we can broaden it to 18th and 19th centuries"; 13:21 "18th-19th centuries, but the fetishized philological object does more consolidating in the 19th"; 14:02 "point of contact as an abstract noun phrase, leave as is; the received reading *of".')
CHANGES = ("Map v1.6: the settlement of which the classical object is the residue dated to the eighteenth and nineteenth centuries (§7.11.4, §7.11.5, the table of §8), with the author's words of 13:21 (§7.11.4); "
           "keyboard slips corrected in the author's quoted words of 17:40 (§1.6), 21:37 (§7.10.1) and 16:14 (kernel), his words otherwise as typed. Kernel v1.6; 11 of 11 tests offline.")
# 1. the package: kernel, operator, surfaces, sources, data and reader runs replaced from the v1.1 build; reviews kept; map and packet at v1.1
for sub in ("kernel", "operator", "surfaces", "sources", "data", "reader-runs"):
    if (FD / sub).exists(): shutil.rmtree(FD / sub)
    shutil.copytree(ST / sub, FD / sub, ignore=shutil.ignore_patterns("__pycache__"))
for old in ("Daffodils-map-v1.5.md", "reader-packet-scopeA-v1.5.md"):
    if (FD / old).exists(): (FD / old).unlink()
for new in ("Daffodils-map-v1.6.md", "reader-packet-scopeA-v1.6.md"):
    shutil.copy2(ST / new, FD / new)
old_roles = {f["filename"]: f["role"] for f in d["files"]}
MT = {".yaml": "application/yaml", ".jsonl": "application/x-ndjson", ".jsonld": "application/ld+json", ".json": "application/json", ".md": "text/markdown",
      ".py": "text/x-python", ".txt": "text/plain", ".tsv": "text/tab-separated-values", ".zip": "application/zip", ".desc": "text/plain"}
def role(rel):
    if rel in old_roles: return old_roles[rel]
    if rel == "Daffodils-map-v1.6.md": return "attached file — the map as the kernel binds it (this record's body, with its H1)"
    if rel == "reader-packet-scopeA-v1.6.md": return "attached file — the scope-A reader packet: prompt, 00-kernel.yaml and 01-ontology.yaml"
    for pre, r in (("kernel/", "kernel component"), ("operator/", "operator: builder, verifier, first seatings and registry extract"), ("surfaces/", "capture transcript or entity row as bound by the kernel"),
                   ("sources/", "current text of a cited record, for offline verification"), ("data/", "the audit's tables"), ("reader-runs/", "round-1 reader run, as pasted")):
        if rel.startswith(pre): return "attached file — " + r
    return "attached file"
files = []
for p in sorted(FD.rglob("*")):
    if not p.is_file(): continue
    rel = p.relative_to(FD).as_posix(); b = p.read_bytes()
    files.append({"filename": rel, "path": f"/files/AXN-{d['hex']}/{rel}", "bytes": len(b), "sha256": hashlib.sha256(b).hexdigest(),
                  "media_type": MT.get(p.suffix, mimetypes.guess_type(p.name)[0] or "application/octet-stream"), "role": role(rel)})
changed = [f["filename"] for f in files if {x["filename"]: x["sha256"] for x in d["files"]}.get(f["filename"]) != f["sha256"]]
# 2. the body: map v1.1 with its H1 replaced by the record's title
title = d["title"].replace("(EA-HK-DAFFODILS-01 v1.5)", "(EA-HK-DAFFODILS-01 v1.6)"); assert title != d["title"]
m = (ST / "Daffodils-map-v1.6.md").read_text(encoding="utf-8"); assert m.startswith("# Daffodils\n\n"); body = m[len("# Daffodils\n\n"):]
cur = (ROOT / d["full_text_path"].lstrip("/")).read_text(encoding="utf-8")
fm_end = cur.index("\n---\n", 4) + 5
fm = cur[:fm_end].replace(f'title: "{d["title"]}"', f'title: "{title}"').replace("\nversion: v1.5\n", "\nversion: v1.6\n")
assert f'title: "{title}"' in fm and "\nversion: v1.6\n" in fm
s = fm + "\n# " + title + "\n\n" + body
h = hashlib.sha256(s.encode("utf-8")).hexdigest(); g = AX.axn_glyph_from_hash(h); cl = AX.axn_clusters_from_hash(h)
d.setdefault("reissue_history", []).append({"date": "2026-11-15", "from_version": "v1.5", "to_version": "v1.6", "hash_before_reissue": d["hash"],
    "axn_before_reissue": d["axn"], "title_before_reissue": d["title"], "reason": WORD, "changes": CHANGES + f" ({len(changed)} files new or re-hashed.)"})
prior = d["axn"]
d.update({"title": title, "version": "v1.6", "hash": h, "axn_canonical": h, "emoji": g, "axn": AX.compose_axn(d["hex"], d["family"], g), "clusters": cl,
          "axn_reading": AX.axn_reading_from_clusters(cl), "files": files, "full_text_chars": len(s)})
d["description"] = d["description"].rstrip() + (" Version 1.6 (15 November, in place) dates the settlement of which the classical object is the residue to the eighteenth and nineteenth centuries, the nineteenth doing the most consolidating.")
d["wiki_article"] = d["wiki_article"].rstrip() + (" Version 1.6 dates the settlement whose residue the field keeps as its object to the eighteenth and nineteenth centuries; in the author's words, 'the fetishized philological object does more consolidating in the 19th'.")
# the author's quoted words in earlier reasons, keyboard slips corrected (13:19)
for r in d["reissue_history"]:
    r["reason"] = r["reason"].replace("if the classical object are fixed", "if the classical objects are fixed").replace("the received reading if what", "the received reading of what").replace("the evalautor exists", "the evaluator exists")
d.setdefault("related_deposits", [])
for x in (1770, 1631):
    if x not in d["related_deposits"]: d["related_deposits"].append(x)
(ROOT / d["full_text_path"].lstrip("/")).write_text(s, encoding="utf-8")
dp = ROOT / f"data/deposits/AXN-{d['hex']}.md"
if dp.exists(): dp.write_text(s, encoding="utf-8")
(ROOT / "data/registry.json").write_text(json.dumps(R, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
json.dump({prior: d["axn"]}, open(pathlib.Path(__file__).parent / "axn-moves-20261115-daffodils-v16.json", "w"), ensure_ascii=False, indent=1)
print(N, prior, "->", d["axn"], "| files:", len(files), "| changed:", len(changed))
