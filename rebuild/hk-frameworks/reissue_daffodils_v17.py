#!/usr/bin/env python3
"""#1769 Daffodils (EA-HK-DAFFODILS-01) reissued in place v1.6 -> v1.7 (2026-11-15), at the author's words of 14:38 ("i would revise it to speak of a previous article
by the author"; "i dont necessarily dispute the decision"; "i dispute the field") and his rulings of 14:39-14:43: the author's previous article in the journal referred to
unnamed (§5.1, §6.2); every work of the register with Crossref's byline (census.json restored to Crossref's data); §1.6 states, in the author's words, that the audit
contests the field and not the decision. Package rebuilt from map v1.7 against the revised entity row; hash and AXN re-derived, the prior kept in reissue_history.
   python3 rebuild/hk-frameworks/reissue_daffodils_v17.py <staged daffodils-hk dir>"""
import json, hashlib, pathlib, shutil, sys, mimetypes
ROOT = pathlib.Path(__file__).resolve().parents[2]; sys.path.insert(0, str(ROOT / "scripts")); import axn_lib as AX
ST = pathlib.Path(sys.argv[1]); N = 1769
R = json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8")); D = {x["deposit_number"]: x for x in R["deposits"]}
d = D[N]; assert d["version"] == "v1.6", d["version"]
FD = ROOT / f"files/AXN-{d['hex']}"
WORD = ('Lee Sharks, 2026-11-15: 14:38 "i would revise it to speak of a previous article by the author"; "i dont necessarily dispute the decision"; "i dispute the field"; 14:43 (the rulings on the revision).')
CHANGES = ("Map v1.7: the author's previous article in the journal referred to unnamed (§5.1, §6.2); every work in the register with Crossref's byline, and census.json with Crossref's data; "
           "§1.6: the audit contests the field and not the decision, in the author's words of 14:38. Kernel v1.7, bound to the revised entity row; 11 of 11 tests offline.")
# 1. the package: kernel, operator, surfaces, sources, data and reader runs replaced from the v1.1 build; reviews kept; map and packet at v1.1
for sub in ("kernel", "operator", "surfaces", "sources", "data", "reader-runs"):
    if (FD / sub).exists(): shutil.rmtree(FD / sub)
    shutil.copytree(ST / sub, FD / sub, ignore=shutil.ignore_patterns("__pycache__"))
for old in ("Daffodils-map-v1.6.md", "reader-packet-scopeA-v1.6.md"):
    if (FD / old).exists(): (FD / old).unlink()
for new in ("Daffodils-map-v1.7.md", "reader-packet-scopeA-v1.7.md"):
    shutil.copy2(ST / new, FD / new)
old_roles = {f["filename"]: f["role"] for f in d["files"]}
MT = {".yaml": "application/yaml", ".jsonl": "application/x-ndjson", ".jsonld": "application/ld+json", ".json": "application/json", ".md": "text/markdown",
      ".py": "text/x-python", ".txt": "text/plain", ".tsv": "text/tab-separated-values", ".zip": "application/zip", ".desc": "text/plain"}
def role(rel):
    if rel in old_roles: return old_roles[rel]
    if rel == "Daffodils-map-v1.7.md": return "attached file — the map as the kernel binds it (this record's body, with its H1)"
    if rel == "reader-packet-scopeA-v1.7.md": return "attached file — the scope-A reader packet: prompt, 00-kernel.yaml and 01-ontology.yaml"
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
title = d["title"].replace("(EA-HK-DAFFODILS-01 v1.6)", "(EA-HK-DAFFODILS-01 v1.7)"); assert title != d["title"]
m = (ST / "Daffodils-map-v1.7.md").read_text(encoding="utf-8"); assert m.startswith("# Daffodils\n\n"); body = m[len("# Daffodils\n\n"):]
cur = (ROOT / d["full_text_path"].lstrip("/")).read_text(encoding="utf-8")
fm_end = cur.index("\n---\n", 4) + 5
fm = cur[:fm_end].replace(f'title: "{d["title"]}"', f'title: "{title}"').replace("\nversion: v1.6\n", "\nversion: v1.7\n")
assert f'title: "{title}"' in fm and "\nversion: v1.7\n" in fm
s = fm + "\n# " + title + "\n\n" + body
h = hashlib.sha256(s.encode("utf-8")).hexdigest(); g = AX.axn_glyph_from_hash(h); cl = AX.axn_clusters_from_hash(h)
d.setdefault("reissue_history", []).append({"date": "2026-11-15", "from_version": "v1.6", "to_version": "v1.7", "hash_before_reissue": d["hash"],
    "axn_before_reissue": d["axn"], "title_before_reissue": d["title"], "reason": WORD, "changes": CHANGES + f" ({len(changed)} files new or re-hashed.)"})
prior = d["axn"]
d.update({"title": title, "version": "v1.7", "hash": h, "axn_canonical": h, "emoji": g, "axn": AX.compose_axn(d["hex"], d["family"], g), "clusters": cl,
          "axn_reading": AX.axn_reading_from_clusters(cl), "files": files, "full_text_chars": len(s)})
LEAD = " It does not contest the journal's decision on the author's manuscript; it contests the field the decision administers."
def rep1(t, a, b):
    assert t.count(a) == 1, a[:70]; return t.replace(a, b)
d["description"] = rep1(d["description"], "the article Metatexts (2014), with no recorded uptake,", "the author's previous article in the journal, with no recorded uptake,")
d["wiki_article"] = rep1(d["wiki_article"], "its author's article in the journal, Metatexts (2014), has no recorded citation", "its author's previous article in the journal has no recorded citation")
first = d["description"].index(". ") + 1; d["description"] = d["description"][:first] + LEAD + d["description"][first:]
first = d["wiki_article"].index(". ") + 1; d["wiki_article"] = d["wiki_article"][:first] + LEAD + d["wiki_article"][first:]
for k in ("description", "wiki_article"):
    assert "Metatexts" not in d[k] and "clu016" not in d[k], k
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
json.dump({prior: d["axn"]}, open(pathlib.Path(__file__).parent / "axn-moves-20261115-daffodils-v17.json", "w"), ensure_ascii=False, indent=1)
print(N, prior, "->", d["axn"], "| files:", len(files), "| changed:", len(changed))
