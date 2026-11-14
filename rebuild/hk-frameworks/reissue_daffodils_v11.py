#!/usr/bin/env python3
"""#1769 Daffodils (EA-HK-DAFFODILS-01) reissued in place v1.0 -> v1.1 (2026-11-14), at the author's words: 17:38 "this is about who gets to speak
for the classics, and on what basis"; 17:40 "the received reading if what healthy flagship means is whats being contested. i wouldnt contest that it
meets that definition; i would contest that that definition defines something healthy"; 17:41 "more of the same is what it tends to mean". The map gains
§1.6 (what is contested) and the kernel restates the rival with its common ground and contested point, extends the ledger's reading instruction and adds
the flag DEFINITION_ASSUMED. The attached package is replaced by the v1.1 build and the file list re-hashed; hash and AXN re-derived at the same
position and family, the prior hash, AXN and title kept in reissue_history.
   python3 rebuild/hk-frameworks/reissue_daffodils_v11.py <staged daffodils-hk dir>"""
import json, hashlib, pathlib, shutil, sys, mimetypes
ROOT = pathlib.Path(__file__).resolve().parents[2]; sys.path.insert(0, str(ROOT / "scripts")); import axn_lib as AX
ST = pathlib.Path(sys.argv[1]); N = 1769
R = json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8")); D = {x["deposit_number"]: x for x in R["deposits"]}
d = D[N]; assert d["version"] == "v1.0", d["version"]
FD = ROOT / f"files/AXN-{d['hex']}"
WORD = ('Lee Sharks, 2026-11-14: 17:38 "this is about who gets to speak for the classics, and on what basis"; 17:40 "the received reading if what healthy '
        'flagship means is whats being contested. i wouldnt contest that it meets that definition; i would contest that that definition defines something healthy"; '
        '17:41 "more of the same is what it tends to mean".')
CHANGES = ("Map §1.6, what is contested: the received definition of a healthy flagship stated with its criteria; the journal meets it; the frame contests that it "
           "defines health, since its criteria reward more of the same (153 of 185 abstracts hold the object fixed; 141 read a later work against a fixed source) and "
           "leave unasked who gets to speak for the classics, and on what basis. §0.5 and the frame table restated to match. Kernel v1.1: the rival's common ground "
           "and contested point, the ledger's reading instruction, the flag DEFINITION_ASSUMED, three author statements. Attached package replaced and re-hashed.")
# 1. the package: kernel, operator, surfaces, sources, data and reader runs replaced from the v1.1 build; reviews kept; map and packet at v1.1
for sub in ("kernel", "operator", "surfaces", "sources", "data", "reader-runs"):
    if (FD / sub).exists(): shutil.rmtree(FD / sub)
    shutil.copytree(ST / sub, FD / sub, ignore=shutil.ignore_patterns("__pycache__"))
for old in ("Daffodils-map-v1.0.md", "reader-packet-scopeA-v1.0.md"):
    if (FD / old).exists(): (FD / old).unlink()
for new in ("Daffodils-map-v1.1.md", "reader-packet-scopeA-v1.1.md"):
    shutil.copy2(ST / new, FD / new)
old_roles = {f["filename"]: f["role"] for f in d["files"]}
MT = {".yaml": "application/yaml", ".jsonl": "application/x-ndjson", ".jsonld": "application/ld+json", ".json": "application/json", ".md": "text/markdown",
      ".py": "text/x-python", ".txt": "text/plain", ".tsv": "text/tab-separated-values", ".zip": "application/zip", ".desc": "text/plain"}
def role(rel):
    if rel in old_roles: return old_roles[rel]
    if rel == "Daffodils-map-v1.1.md": return "attached file — the map as the kernel binds it (this record's body, with its H1)"
    if rel == "reader-packet-scopeA-v1.1.md": return "attached file — the scope-A reader packet: prompt, 00-kernel.yaml and 01-ontology.yaml"
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
title = d["title"].replace("(EA-HK-DAFFODILS-01 v1.0)", "(EA-HK-DAFFODILS-01 v1.1)"); assert title != d["title"]
m = (ST / "Daffodils-map-v1.1.md").read_text(encoding="utf-8"); assert m.startswith("# Daffodils\n\n"); body = m[len("# Daffodils\n\n"):]
cur = (ROOT / d["full_text_path"].lstrip("/")).read_text(encoding="utf-8")
fm_end = cur.index("\n---\n", 4) + 5
fm = cur[:fm_end].replace(f'title: "{d["title"]}"', f'title: "{title}"').replace("\nversion: v1.0\n", "\nversion: v1.1\n")
assert f'title: "{title}"' in fm and "\nversion: v1.1\n" in fm
s = fm + "\n# " + title + "\n\n" + body
h = hashlib.sha256(s.encode("utf-8")).hexdigest(); g = AX.axn_glyph_from_hash(h); cl = AX.axn_clusters_from_hash(h)
d.setdefault("reissue_history", []).append({"date": "2026-11-14", "from_version": "v1.0", "to_version": "v1.1", "hash_before_reissue": d["hash"],
    "axn_before_reissue": d["axn"], "title_before_reissue": d["title"], "reason": WORD, "changes": CHANGES + f" ({len(changed)} files new or re-hashed.)"})
prior = d["axn"]
d.update({"title": title, "version": "v1.1", "hash": h, "axn_canonical": h, "emoji": g, "axn": AX.compose_axn(d["hex"], d["family"], g), "clusters": cl,
          "axn_reading": AX.axn_reading_from_clusters(cl), "files": files, "full_text_chars": len(s)})
d["description"] = d["description"].rstrip() + (" Version 1.1 (14 November 2026, in place) states what is contested: the journal meets the received definition of a healthy "
    "flagship, and the frame contests that the definition defines health, since its criteria reward more of the same and leave unasked who gets to speak for the classics, and on what basis.")
d["wiki_article"] = d["wiki_article"].rstrip() + (" Version 1.1, the same day, states what is contested. The audit concedes that the journal meets the received definition of a "
    "healthy flagship, its range, self-examination, standing and uptake, and contests that the definition defines health: its criteria reward more of the same, more receivers "
    "read against a fixed source, and leave unasked who gets to speak for the classics, and on what basis.")
(ROOT / d["full_text_path"].lstrip("/")).write_text(s, encoding="utf-8")
dp = ROOT / f"data/deposits/AXN-{d['hex']}.md"
if dp.exists(): dp.write_text(s, encoding="utf-8")
(ROOT / "data/registry.json").write_text(json.dumps(R, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
json.dump({prior: d["axn"]}, open(pathlib.Path(__file__).parent / "axn-moves-20261114-daffodils-v11.json", "w"), ensure_ascii=False, indent=1)
print(N, prior, "->", d["axn"], "| files:", len(files), "| changed:", len(changed))
