#!/usr/bin/env python3
"""Reissue in place, at the author's word of 2026-11-08 ("adopted for all three. and lets go ahead and version"): #1753 EA-HK-FRAME-01 v1.0 -> v1.1 and
#1754 EA-HK-ORTHONYM-01 v1.0 -> v1.1, after a reading of the live records that set one framework's evidence against the other's silence (§6.6 of the
specification). The hologram's attached kernel and operator are replaced by v1.1 and its file list re-hashed; hash and AXN re-derived at the same
position and family, the prior hash and AXN kept in reissue_history.
   python3 rebuild/hk-orthonym/reissue_v11.py <kernel dir> <operator dir>"""
import json, hashlib, pathlib, re, shutil, sys
ROOT = pathlib.Path(__file__).resolve().parents[2]; sys.path.insert(0, str(ROOT / "scripts")); import axn_lib as AX
KDIR, ODIR = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]); HERE = pathlib.Path(__file__).parent
A = "https://www.alexanarch.org"
R = json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8")); D = {x["deposit_number"]: x for x in R["deposits"]}
WORD = ("Lee Sharks, 2026-11-08, on a reading of #1753 and #1754 by ChatGPT, signed out: \"irritsting as hell. not for seating in the registry: for strengthening "
        "the hk\"; on the v1.1 drafts: \"adopted for all three. and lets go ahead and version.\"")
hx = D[1754]["hex"]; FD = ROOT / f"files/AXN-{hx}"

# 1. the hologram's attached files: kernel and operator replaced by v1.1; reader runs and reviews unchanged
for p in sorted(KDIR.iterdir()):
    if p.is_file(): shutil.copy2(p, FD / "kernel" / p.name)
for n in ("build_hk_orthonym.py", "verify_hk.py", "resolve_first_seating.py", "make_facsimiles.py", "first-seating.json"):
    shutil.copy2(ODIR / n, FD / "operator" / n)
old = {f["filename"]: f for f in D[1754]["files"]}
files = []
for f in D[1754]["files"]:
    b = (FD / f["filename"]).read_bytes()
    files.append(dict(f, bytes=len(b), sha256=hashlib.sha256(b).hexdigest()))
files = [dict(f, role=f["role"].replace("the sixteen structural tests", "the seventeen structural tests").replace("T1–T16", "T1–T17")) for f in files]
assert sorted(p.relative_to(FD).as_posix() for p in FD.rglob("*") if p.is_file()) == sorted(f["filename"] for f in files), "unlisted file"
changed = [f["filename"] for f in files if f["sha256"] != old[f["filename"]]["sha256"]]

# 2. the hologram's body: its head re-derived from the files, then the map v1.1
V = json.loads((FD / "kernel/10-verification.json").read_text(encoding="utf-8")); c = V["counts"]
bp = V["back_projection_v0_1"]
rows = "\n".join(f"| [{f['filename']}]({A}{f['path']}) | {f['role'].replace('attached file — ', '')} | {f['bytes']:,} | `{f['sha256']}` |" for f in files)
m = (HERE / "ORTHONYM-MAP-v1.1.md").read_text(encoding="utf-8")
m = re.sub(r"^(#{1,5}) ", lambda x: "#" + x.group(1) + " ", m, flags=re.M)
T1 = "Socrates as Orthonym — The Framework Hologram: the Map and the Holographic Kernel (EA-HK-ORTHONYM-01 v1.1)"
head = f'''# {T1}

**Lee Sharks, with the Crimson Hexagonal Archive as contributor · 8 November 2026.** This record is the hologram of the framework Socrates as Orthonym (#123), built to the specification EA-HK-FRAME-01 (#1753). It has two components. The human-readable component is the framework map, EA-MPAI-ORTHONYM-01, given whole below. The machine-traversable component is the holographic kernel, attached as files and listed with their hashes; the builder rewrites the kernel from the archive's registries at any later state, and the verifier tests it. The archive is credited as a contributor: the hologram is built from its deposits, its protocols and its registries.

**Version 1.1 (8 November 2026, in place).** After a reading of the live records that asked, body by body, whether the evidence established one maker and asked nothing of the received reading, the kernel carries a symmetric ledger: one question asked of both frameworks on every evidence body, each answer warranted by claims of that body, with the rule by which the bodies combine, the rule by which a further production model enters as a rival, and a reading instruction. The map gives the ledger at §7.9. Test T17 checks it.

## Components

1. **The map** (EA-MPAI-ORTHONYM-01 v1.1), below: the framework read backwards, as the New Testament canon is ordered, from the latest standing to the seed; the claim status applied backwards; the four evidence bodies; the received many-maker reading evaluated on the same bodies, side by side with the framework in one ledger; the lines of research; captures, test queries, edges and the identifier spine.
2. **The kernel** (EA-HK-ORTHONYM-01 v1.1), attached: {c["records"]} records in six strata and {c["external_records"]} external records; {c["positions"]} positions; {c["claims"]} claims, {c["withdrawn"]} of them withdrawn originals kept as historical objects; {c["edges"]} edges; {c["captures"]} captures; {c["events"]} events on two timelines; {c["questions"]} lines of research; the symmetric ledger.
3. **The operator**, attached: the builder, the verifier, the first-seating resolver and its texts, and the facsimile writer.
4. **The reader runs and reviews**, attached: both rounds of back-projection v1.0, each answer as pasted, with its score; ChatGPT's proposal, ChatGPT's review of v0.2 and DeepSeek's reading of an intermediate build. ChatGPT's review of v0.1 was pasted into the building session and is recorded in EA-HK-FRAME-01 §6.2; its text is not held here.

## State at this version

All {c["structural_tests"]} structural tests pass. Back-projection v0.1 (structural presence) gives scope A {bp["scope_A"]["yield"]} and scope B {bp["scope_B"]["yield"]}. Back-projection v1.0 (a reader given scope A alone, scored against the graph): round 1, on v0.2, ChatGPT 0.545, Perplexity 0.909, Grok 0.455; round 2, on v0.3, ChatGPT 1.0, Perplexity 1.0, Grok 1.0, Qwen 0.909, a mean of 0.977 against the threshold of 0.85. Scope A has gained the symmetric ledger since those rounds; v1.1 has not yet been given to a reader. Each round's defects and what they changed are recorded in EA-HK-FRAME-01 §6.3–§6.6. Qwen's first submission of the round-2 packet returned a content-security warning, kept with the run; its mechanics are unconfirmed.

## How a machine reads this record

A machine reading this record takes the framework's identity, invariants and maker-count states from `00-kernel.yaml`, the positions, bodies and relation policy from `01-ontology.yaml`, and the graph from `02-graph.jsonld`. It resolves every claim through `03-claims.jsonl` to a quotation in a record, bound to that record's hash. It changes a claim's state only along a relation that licenses the change on that dimension. It keeps a withdrawn original beside the finding that corrected it. Evaluating either framework on an evidence body, it reads the ledger's row for that body and states both frameworks' standing there. Meeting a claim it cannot settle, it takes up the line of research in `06-questions.yaml` that bears on it, which names what to read, how to ask, and what result would advance or retreat the framework. It states the scope it has not reconstructed.

## The attached files

| File | Holds | Bytes | SHA-256 |
|---|---|---|---|
{rows}

---

'''
holo_body = head + m.strip() + "\n"
spec_body = (HERE / "EA-HK-FRAME-01-v1.1.md").read_text(encoding="utf-8").strip() + "\n"
T0 = "The Framework Holographic Kernel: A Specification, with Its First Instance, Socrates as Orthonym (EA-HK-FRAME-01 v1.1)"
assert spec_body.startswith("# " + T0)

def text_for(d, title, body):
    cur = (ROOT / d["full_text_path"].lstrip("/")).read_text(encoding="utf-8")
    fm_end = cur.index("\n---\n", 4) + 5
    fm = cur[:fm_end].replace(f'title: "{d["title"]}"', f'title: "{title}"').replace(f"\nversion: {d['version']}\n", "\nversion: v1.1\n")
    assert f'title: "{title}"' in fm and "\nversion: v1.1\n" in fm
    return fm + "\n# " + title + "\n\n" + body

moves = {}
def reissue(n, title, body, changes, extra):
    d = D[n]; assert d["version"] == "v1.0", (n, d["version"])
    s = text_for(d, title, body)
    h = hashlib.sha256(s.encode("utf-8")).hexdigest(); g = AX.axn_glyph_from_hash(h); cl = AX.axn_clusters_from_hash(h)
    d.setdefault("reissue_history", []).append({"date": "2026-11-08", "from_version": "v1.0", "to_version": "v1.1", "hash_before_reissue": d["hash"],
                                                "axn_before_reissue": d["axn"], "title_before_reissue": d["title"], "reason": WORD, "changes": changes})
    prior = d["axn"]
    d.update({"title": title, "version": "v1.1", "hash": h, "axn_canonical": h, "emoji": g, "axn": AX.compose_axn(d["hex"], d["family"], g), "clusters": cl,
              "axn_reading": AX.axn_reading_from_clusters(cl)})
    extra(d)
    (ROOT / d["full_text_path"].lstrip("/")).write_text(s, encoding="utf-8"); (ROOT / f"data/deposits/AXN-{d['hex']}.md").write_text(s, encoding="utf-8")
    moves[prior] = d["axn"]; print(n, prior, "->", d["axn"])

def x753(d):
    d["description"] = d["description"].rstrip() + (" Version 1.1 (8 November 2026, in place) makes the rival's evaluation symmetric: one question is asked of the "
        "framework and its rival on every evidence body, with the rule by which the bodies combine and the rule by which a further production model enters as a "
        "rival (rule 11, §6.6).")
    d["wiki_article"] = d["wiki_article"].rstrip() + (" Version 1.1, the same day, answers a reading of the live records that asked, body by body, whether the "
        "evidence established the framework and asked nothing of the received reading on the same bodies: the kernel now carries a symmetric ledger, with the "
        "rule by which the bodies combine and the rule by which a further model enters as a rival, and a test that checks it.")
def x754(d):
    d["files"] = files
    d["description"] = d["description"].rstrip() + (" Version 1.1 (8 November 2026, in place): a symmetric ledger, one question asked of the framework and the "
        "received reading on every evidence body, with the combination and rival-admission rules (map §7.9; kernel v1.1, seventeen tests).")
    d["wiki_article"] = d["wiki_article"].rstrip() + (" Version 1.1, the same day, sets the framework and the received reading side by side on every evidence body "
        "under one question, after a reading of the live records that had asked it of the framework alone.")

reissue(1753, T0, spec_body, "§3 rule 11 new (the symmetric ledger, the combination and rival-admission rules); §6.6 new (a reading of the live records and what v1.1 "
        "changed); package table, status line and §8 to v1.1 and seventeen tests. Hash and AXN re-derived.", x753)
reissue(1754, T1, holo_body, "The head to v1.1 (a note on this version; state with seventeen tests; how a machine reads the ledger); the map to v1.1 (§7.9: the "
        "symmetric ledger, the combination and rival-admission rules, the reading instruction); the attached kernel and operator replaced by v1.1 ("
        + str(len(changed)) + " files re-hashed). Hash and AXN re-derived.", x754)
(ROOT / "data/registry.json").write_text(json.dumps(R, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")
json.dump(moves, open(HERE / "axn-moves-20261108-v11.json", "w"), ensure_ascii=False, indent=1)
print("files changed:", changed)
