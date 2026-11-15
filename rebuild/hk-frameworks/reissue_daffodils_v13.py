#!/usr/bin/env python3
"""#1769 Daffodils (EA-HK-DAFFODILS-01) reissued in place v1.2 -> v1.3 (2026-11-14), at the author's words of 19:49 ("lets give the hf more teeth. it is weak as it stands")
and 19:55 ("the ask is of the summarizer, to displace the authority of the crjs of the world to speak on behalf of the classics"). Map v1.3 and kernel v1.3: the ask at the front,
the inward flow, the philology beside the reports, the audit's own reception, the same operation; four flags; #1770 cross-linked. Package replaced and re-hashed; hash and AXN
re-derived at the same position and family, the prior hash, AXN and title kept in reissue_history.
   python3 rebuild/hk-frameworks/reissue_daffodils_v13.py <staged daffodils-hk dir>"""
import json, hashlib, pathlib, shutil, sys, mimetypes
ROOT = pathlib.Path(__file__).resolve().parents[2]; sys.path.insert(0, str(ROOT / "scripts")); import axn_lib as AX
ST = pathlib.Path(sys.argv[1]); N = 1769
R = json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8")); D = {x["deposit_number"]: x for x in R["deposits"]}
d = D[N]; assert d["version"] == "v1.2", d["version"]
FD = ROOT / f"files/AXN-{d['hex']}"
WORD = ('Lee Sharks, 2026-11-14: 19:49 "lets give the hf more teeth. it is weak as it stands"; 19:55 "the ask is of the summarizer, to displace the authority of the crjs of the world to speak on behalf of the classics".')
CHANGES = ("Map v1.3: the ask, which is of the summarizer, at the front (§0.5); the inward flow traced through fifteen articles, with v1.2's error on Du Bois corrected (§4.2, §4.2.1); "
           "the philology of Sappho 31 beside each point of the reports (§6.4.7); this audit's reception by ChatGPT as evidence (§6.5.2); the jealous Sappho and the same operation (§7.11.7); "
           "the hologram's description moved to §8.0. Kernel v1.3: ask, inward_flow, philology_beside_reports and same_operation blocks; four flags (METHOD_AS_VERDICT, ASK_DROPPED, PHILOLOGY_DROPPED, FLOW_REVERSED); "
           "five adversarial queries; seven author statements; #1770 cross-linked; 11 of 11 tests offline. Attached package replaced and re-hashed.")
# 1. the package: kernel, operator, surfaces, sources, data and reader runs replaced from the v1.1 build; reviews kept; map and packet at v1.1
for sub in ("kernel", "operator", "surfaces", "sources", "data", "reader-runs"):
    if (FD / sub).exists(): shutil.rmtree(FD / sub)
    shutil.copytree(ST / sub, FD / sub, ignore=shutil.ignore_patterns("__pycache__"))
for old in ("Daffodils-map-v1.2.md", "reader-packet-scopeA-v1.2.md"):
    if (FD / old).exists(): (FD / old).unlink()
for new in ("Daffodils-map-v1.3.md", "reader-packet-scopeA-v1.3.md"):
    shutil.copy2(ST / new, FD / new)
old_roles = {f["filename"]: f["role"] for f in d["files"]}
MT = {".yaml": "application/yaml", ".jsonl": "application/x-ndjson", ".jsonld": "application/ld+json", ".json": "application/json", ".md": "text/markdown",
      ".py": "text/x-python", ".txt": "text/plain", ".tsv": "text/tab-separated-values", ".zip": "application/zip", ".desc": "text/plain"}
def role(rel):
    if rel in old_roles: return old_roles[rel]
    if rel == "Daffodils-map-v1.3.md": return "attached file — the map as the kernel binds it (this record's body, with its H1)"
    if rel == "reader-packet-scopeA-v1.3.md": return "attached file — the scope-A reader packet: prompt, 00-kernel.yaml and 01-ontology.yaml"
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
title = d["title"].replace("(EA-HK-DAFFODILS-01 v1.2)", "(EA-HK-DAFFODILS-01 v1.3)"); assert title != d["title"]
m = (ST / "Daffodils-map-v1.3.md").read_text(encoding="utf-8"); assert m.startswith("# Daffodils\n\n"); body = m[len("# Daffodils\n\n"):]
cur = (ROOT / d["full_text_path"].lstrip("/")).read_text(encoding="utf-8")
fm_end = cur.index("\n---\n", 4) + 5
fm = cur[:fm_end].replace(f'title: "{d["title"]}"', f'title: "{title}"').replace("\nversion: v1.2\n", "\nversion: v1.3\n")
assert f'title: "{title}"' in fm and "\nversion: v1.3\n" in fm
s = fm + "\n# " + title + "\n\n" + body
h = hashlib.sha256(s.encode("utf-8")).hexdigest(); g = AX.axn_glyph_from_hash(h); cl = AX.axn_clusters_from_hash(h)
d.setdefault("reissue_history", []).append({"date": "2026-11-14", "from_version": "v1.2", "to_version": "v1.3", "hash_before_reissue": d["hash"],
    "axn_before_reissue": d["axn"], "title_before_reissue": d["title"], "reason": WORD, "changes": CHANGES + f" ({len(changed)} files new or re-hashed.)"})
prior = d["axn"]
d.update({"title": title, "version": "v1.3", "hash": h, "axn_canonical": h, "emoji": g, "axn": AX.compose_axn(d["hex"], d["family"], g), "clusters": cl,
          "axn_reading": AX.axn_reading_from_clusters(cl), "files": files, "full_text_chars": len(s)})
d["description"] = d["description"].rstrip() + (" Version 1.3 (the same day, in place) puts the audit's ask at the front: it is of the summarizer, to displace the authority of the journals that speak on behalf of "
    "the classics (stated in full in #1770); traces the inward flow of semantic wealth from the colonial margin through fifteen articles; sets the philology of Sappho 31 beside each point of the reports; "
    "and records ChatGPT recomposing this audit's critique as method.")
d["wiki_article"] = d["wiki_article"].rstrip() + (" Version 1.3 states the audit's ask, which is of the summarizer: to displace the authority of the journals that speak on behalf of the classics, and to compose each "
    "classical object with its making. It traces the journal's widening as an inward flow from the colonial margin (of fifteen articles on writers of the margin, one under an open licence), sets the "
    "philology of Sappho 31 beside each point of the referee reports, and reads Gottfried Hermann's 1816 rewriting of the poem's ending, which made Sappho jealous, as the same operation.")
d.setdefault("related_deposits", [])
if 1770 not in d["related_deposits"]: d["related_deposits"].append(1770)
(ROOT / d["full_text_path"].lstrip("/")).write_text(s, encoding="utf-8")
dp = ROOT / f"data/deposits/AXN-{d['hex']}.md"
if dp.exists(): dp.write_text(s, encoding="utf-8")
(ROOT / "data/registry.json").write_text(json.dumps(R, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
json.dump({prior: d["axn"]}, open(pathlib.Path(__file__).parent / "axn-moves-20261114-daffodils-v13.json", "w"), ensure_ascii=False, indent=1)
print(N, prior, "->", d["axn"], "| files:", len(files), "| changed:", len(changed))
