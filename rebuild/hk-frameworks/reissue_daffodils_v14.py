#!/usr/bin/env python3
"""#1769 Daffodils (EA-HK-DAFFODILS-01) reissued in place v1.3 -> v1.4 (2026-11-14), at the author's words of 21:37, 21:40 and 21:41 ("adopted. lets reissue"): map §7.10.1,
alignment with the classical object as the journal's operation on the receiving work (the monetary shear of #1631); kernel v1.4 with the flag ALIGNMENT_AS_QUALITY. Package
replaced and re-hashed; hash and AXN re-derived at the same position and family, the prior hash, AXN and title kept in reissue_history.
   python3 rebuild/hk-frameworks/reissue_daffodils_v14.py <staged daffodils-hk dir>"""
import json, hashlib, pathlib, shutil, sys, mimetypes
ROOT = pathlib.Path(__file__).resolve().parents[2]; sys.path.insert(0, str(ROOT / "scripts")); import axn_lib as AX
ST = pathlib.Path(sys.argv[1]); N = 1769
R = json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8")); D = {x["deposit_number"]: x for x in R["deposits"]}
d = D[N]; assert d["version"] == "v1.3", d["version"]
FD = ROOT / f"files/AXN-{d['hex']}"
WORD = ('Lee Sharks, 2026-11-14: 21:37 "if the classical object are fixed then they are not studying the reception of the classics they are administering the classics as sovereign objects in their control"; '
        '21:40 "the alignment with the classical object is not a fixed quality of the receiver but a primary operation of the journal"; 21:41 "adopted. lets reissue".')
CHANGES = ("Map v1.4: §7.10.1, alignment with the classical object as the journal's operation on the receiving work, read through the monetary shear (#1631); §4.2.1 and the ask's first "
           "address carry it. Kernel v1.4: the alignment block, the claim df-alignment, the flag ALIGNMENT_AS_QUALITY, one adversarial query, two author statements; 11 of 11 tests offline. Package replaced and re-hashed.")
# 1. the package: kernel, operator, surfaces, sources, data and reader runs replaced from the v1.1 build; reviews kept; map and packet at v1.1
for sub in ("kernel", "operator", "surfaces", "sources", "data", "reader-runs"):
    if (FD / sub).exists(): shutil.rmtree(FD / sub)
    shutil.copytree(ST / sub, FD / sub, ignore=shutil.ignore_patterns("__pycache__"))
for old in ("Daffodils-map-v1.3.md", "reader-packet-scopeA-v1.3.md"):
    if (FD / old).exists(): (FD / old).unlink()
for new in ("Daffodils-map-v1.4.md", "reader-packet-scopeA-v1.4.md"):
    shutil.copy2(ST / new, FD / new)
old_roles = {f["filename"]: f["role"] for f in d["files"]}
MT = {".yaml": "application/yaml", ".jsonl": "application/x-ndjson", ".jsonld": "application/ld+json", ".json": "application/json", ".md": "text/markdown",
      ".py": "text/x-python", ".txt": "text/plain", ".tsv": "text/tab-separated-values", ".zip": "application/zip", ".desc": "text/plain"}
def role(rel):
    if rel in old_roles: return old_roles[rel]
    if rel == "Daffodils-map-v1.4.md": return "attached file — the map as the kernel binds it (this record's body, with its H1)"
    if rel == "reader-packet-scopeA-v1.4.md": return "attached file — the scope-A reader packet: prompt, 00-kernel.yaml and 01-ontology.yaml"
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
title = d["title"].replace("(EA-HK-DAFFODILS-01 v1.3)", "(EA-HK-DAFFODILS-01 v1.4)"); assert title != d["title"]
m = (ST / "Daffodils-map-v1.4.md").read_text(encoding="utf-8"); assert m.startswith("# Daffodils\n\n"); body = m[len("# Daffodils\n\n"):]
cur = (ROOT / d["full_text_path"].lstrip("/")).read_text(encoding="utf-8")
fm_end = cur.index("\n---\n", 4) + 5
fm = cur[:fm_end].replace(f'title: "{d["title"]}"', f'title: "{title}"').replace("\nversion: v1.3\n", "\nversion: v1.4\n")
assert f'title: "{title}"' in fm and "\nversion: v1.4\n" in fm
s = fm + "\n# " + title + "\n\n" + body
h = hashlib.sha256(s.encode("utf-8")).hexdigest(); g = AX.axn_glyph_from_hash(h); cl = AX.axn_clusters_from_hash(h)
d.setdefault("reissue_history", []).append({"date": "2026-11-14", "from_version": "v1.3", "to_version": "v1.4", "hash_before_reissue": d["hash"],
    "axn_before_reissue": d["axn"], "title_before_reissue": d["title"], "reason": WORD, "changes": CHANGES + f" ({len(changed)} files new or re-hashed.)"})
prior = d["axn"]
d.update({"title": title, "version": "v1.4", "hash": h, "axn_canonical": h, "emoji": g, "axn": AX.compose_axn(d["hex"], d["family"], g), "clusters": cl,
          "axn_reading": AX.axn_reading_from_clusters(cl), "files": files, "full_text_chars": len(s)})
d["description"] = d["description"].rstrip() + (" Version 1.4 (the same day, in place) states alignment with the classical object as the journal's operation on the receiving work, a productive shear (#1631) in which the work's own claims go dark.")
d["wiki_article"] = d["wiki_article"].rstrip() + (" Version 1.4 adds that the journal administers the classics as fixed objects and performs their alignment on each receiving work, which keeps only the relation of alignment in operative standing.")
d.setdefault("related_deposits", [])
for x in (1770, 1631):
    if x not in d["related_deposits"]: d["related_deposits"].append(x)
(ROOT / d["full_text_path"].lstrip("/")).write_text(s, encoding="utf-8")
dp = ROOT / f"data/deposits/AXN-{d['hex']}.md"
if dp.exists(): dp.write_text(s, encoding="utf-8")
(ROOT / "data/registry.json").write_text(json.dumps(R, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
json.dump({prior: d["axn"]}, open(pathlib.Path(__file__).parent / "axn-moves-20261114-daffodils-v14.json", "w"), ensure_ascii=False, indent=1)
print(N, prior, "->", d["axn"], "| files:", len(files), "| changed:", len(changed))
