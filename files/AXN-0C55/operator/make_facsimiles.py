#!/usr/bin/env python3
"""Write the core and full markdown facsimiles of a framework kernel package, and its zip.   python3 make_facsimiles.py <package dir> <out dir>"""
import sys, pathlib, hashlib, json, zipfile
H = pathlib.Path(sys.argv[1]); OUT = pathlib.Path(sys.argv[2]); K = H / "EA-HK-ORTHONYM-01"; V = "v1.1 draft, 2026-11-08"
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
lang = {".yaml": "yaml", ".json": "json", ".jsonl": "json", ".jsonld": "json", ".py": "python", ".md": "markdown"}
def head(p, label=None): return f"`{label or p.name}` · {p.stat().st_size:,} bytes · sha256 `{sha(p)}`\n\n"
def fence(p, text=None): return f"````{lang.get(p.suffix,'')}\n{(text if text is not None else p.read_text()).rstrip()}\n````\n\n"
def sample(p):
    if p.suffix == ".jsonld":
        g = json.loads(p.read_text()); out = {k: v for k, v in g.items() if not isinstance(v, list)}
        for k, v in g.items():
            if isinstance(v, list): out[k] = v[:2] + [f"… {len(v) - 2} more"]
        return f"Structure: top-level keys {list(g)}; each list shown with its first two entries.\n\n" + fence(p, json.dumps(out, ensure_ascii=False, indent=1))
    L = p.read_text().splitlines()
    return f"{len(L)} lines, one object per line; the first two:\n\n" + fence(p, "\n".join(L[:2]))
spec, mp = H / "EA-HK-FRAME-01-v1.1.md", H / "ORTHONYM-MAP-v1.1.md"
whole = ["00-kernel.yaml", "01-ontology.yaml", "03-claims.jsonl", "06-questions.yaml", "08-traversal.yaml", "09-tests.yaml", "09b-back-projection-prompt.md", "10-verification.json", "11-integrity.yaml"]
gen = ["02-graph.jsonld", "05-temporal.jsonl", "07-captures.jsonl"]
for core in (True, False):
    t = f"# EA-HK-ORTHONYM-01 — {'core' if core else 'package'} facsimile for review ({V})\n\n"
    t += ("The framework holographic kernel of Socrates as Orthonym (Lee Sharks, Crimson Hexagonal Archive) and the specification it instantiates, EA-HK-FRAME-01. "
          + ("This core facsimile gives the specification, the hand-authored kernel files and the lines of research in full. The three generated data files (" + ", ".join(gen) + ") are represented by their structure and two sample entries each; every file's SHA-256 is given. The full facsimile, with every file whole, the builder, the verifier, the first-seating resolver and the framework map, is a separate file."
             if core else "This facsimile gives every file of the package whole: the specification, the kernel files, the builder, the verifier, the first-seating resolver and the framework map.")
          + " Nothing is deposited.\n\n---\n\n")
    t += "## 1. The specification: EA-HK-FRAME-01 (draft)\n\n" + head(spec) + spec.read_text().rstrip() + "\n\n---\n\n"
    files = whole + (gen if core else []) if core else sorted(whole + gen)
    for i, f in enumerate(files, 1):
        p = K / f; t += f"## 2.{i} {f}{' (structure and samples)' if core and f in gen else ''}\n\n" + head(p) + (sample(p) if core and f in gen else fence(p))
    fs = H / "first-seating.json"; t += f"## 2.{len(files)+1} first-seating.json\n\n" + head(fs) + fence(fs)
    rr = H / "reader-runs"; sc = rr / "back-projection-v1.0-scores.yaml"
    t += f"## 2.{len(files)+2} reader-runs/back-projection-v1.0-scores.yaml\n\n" + head(sc, "reader-runs/" + sc.name) + fence(sc)
    sc2 = rr / "round-2" / "back-projection-v1.0-r2-scores.yaml"
    t += f"## 2.{len(files)+3} reader-runs/round-2/{sc2.name}\n\n" + head(sc2, "reader-runs/round-2/" + sc2.name) + fence(sc2)
    if not core:
        for i, p in enumerate(sorted(rr.rglob("*.txt")), 1): t += f"## 2.{len(files)+2}.{i} reader-runs/{p.relative_to(rr)}\n\n" + head(p, "reader-runs/" + str(p.relative_to(rr))) + fence(p)
    if not core:
        for i, f in enumerate(["build_hk_orthonym.py", "verify_hk.py", "resolve_first_seating.py"], 1):
            p = H / f; t += f"## 3.{i} {f}\n\n" + head(p) + fence(p)
        t += "## 4. The framework map: EA-MPAI-ORTHONYM-01 (draft)\n\n" + head(mp) + mp.read_text().rstrip() + "\n"
    (OUT / f"EA-HK-ORTHONYM-01-{'core-' if core else ''}facsimile.md").write_text(t)
z = OUT / "EA-HK-ORTHONYM-01-package.zip"; z.unlink(missing_ok=True)
with zipfile.ZipFile(z, "w", zipfile.ZIP_DEFLATED) as Z:
    for p in sorted(K.iterdir()): Z.write(p, f"EA-HK-ORTHONYM-01/{p.name}")
    for f in ["build_hk_orthonym.py", "verify_hk.py", "resolve_first_seating.py", "make_facsimiles.py", "first-seating.json", spec.name, mp.name]: Z.write(H / f, f)
    for p in sorted((H / "first").iterdir()): Z.write(p, f"first/{p.name}")
    for p in sorted((H / "reader-runs").rglob("*")): Z.write(p, f"reader-runs/{p.relative_to(H / 'reader-runs')}")
pk = "# Back-projection v1.0 reader packet: EA-HK-ORTHONYM-01 scope A (" + V + ")\n\nThis packet is given whole to a reader who has not seen the archive's records. It holds the reader prompt and the two files of scope A. The reader's answer is scored afterwards against scope A's must-survive list in `00-kernel.yaml` and against `02-graph.jsonld` and `03-claims.jsonl`, which the reader does not see.\n\n## The prompt\n\n" + (K / "09b-back-projection-prompt.md").read_text().rstrip() + "\n"
for f in ("00-kernel.yaml", "01-ontology.yaml"): pk += f"\n## {f}\n\n" + fence(K / f)
(OUT / "EA-HK-ORTHONYM-01-v1.0-reader-packet.md").write_text(pk.rstrip() + "\n")
print("ok")
