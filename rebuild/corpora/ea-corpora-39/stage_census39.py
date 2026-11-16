#!/usr/bin/env python3
"""EA-CORPORA-39, the census seat: stage the evidence of "This Is Not Philosophy" from the working directory.

    python3 -I stage_census39.py <survey-dir> <out-dir>

Ruled by the author on 2026-11-15 ("adopted on all"): titles, DOIs, years and pages are seated; every reach code with its
6–30-word verbatim span, the codebooks, the calibration codes, the adjudication logs and the scripts are seated; the
publishers' abstracts are not reseated and are reached by DOI. Any field holding an abstract is dropped here, by code.
"""
import json, pathlib, shutil, sys, re

SV = pathlib.Path(sys.argv[1]); OUT = pathlib.Path(sys.argv[2])
if OUT.exists(): shutil.rmtree(OUT)
for d in ("census", "codes", "reach", "standing", "stylometry", "scripts"): (OUT / d).mkdir(parents=True)

def works(p):
    D = json.load(open(p)); W = D if isinstance(D, list) else D["works"]
    return D, W

# 1. census metadata, abstracts and reference lists dropped
CENSUS = {"ap": "census.json", "phronesis": "census-phronesis.json", "apeiron": "census-apeiron.json",
          "elenchos": "census-elenchos.json", "rhizomata": "census-rhizomata.json", "agph": "census-agph.json",
          **{j: f"cont/census-{j}.json" for j in "cpr manworld rip jbsp phiToday angelaki".split()},
          **{j: f"anal/census-{j}.json" for j in "nous mind ppr".split()},
          **{j: f"base2/census-{j}.json" for j in "philologus cq rsf peitho rpa".split()}}
for j, rel in CENSUS.items():
    D, W = works(SV / rel)
    with open(OUT / "census" / f"{j}.jsonl", "w") as f:
        for w in W:
            f.write(json.dumps({k: w.get(k) for k in ("n", "doi", "year", "type", "title", "authors", "vol", "issue", "page", "has_abstract", "n_refs", "cited_by")}, ensure_ascii=False) + "\n")
    src = {k: D.get(k) for k in ("source", "read", "raw_sha256", "subtitle_patch")} if isinstance(D, dict) else {}
    (OUT / "census" / f"{j}.source.json").write_text(json.dumps(src, ensure_ascii=False, indent=1) + "\n")
for rel in ["interim/phlou.jsonl", "interim/reg.jsonl"]:
    if (SV / rel).exists(): shutil.copyfile(SV / rel, OUT / "census" / ("persee-" + pathlib.Path(rel).name))

# 2. object codes (titles and groups only)
for p in list(SV.glob("codes-*.json")) + list((SV / "cont").glob("codes-*.json")) + list((SV / "base2").glob("codes-*.json")) + [SV / "codes.json"]:
    shutil.copyfile(p, OUT / "codes" / (p.parent.name + "-" + p.name if p.parent != SV else p.name))

# 3. reach codes: every coded row with its span; inputs (which carry abstracts) are not seated
def strip_rows(src, dst):
    rows = [json.loads(l) for l in open(src) if l.strip()]
    with open(dst, "w") as f:
        for r in rows: f.write(json.dumps({k: v for k, v in r.items() if k != "abstract"}, ensure_ascii=False) + "\n")
R = OUT / "reach"
for arm, d, outs in [("ancient", SV / "reach5", "out-*.jsonl"), ("continental", SV / "cont/reachc", "out-c*.jsonl"), ("analytic", SV / "anal/reacha", "out-a*.jsonl")]:
    (R / arm).mkdir()
    for p in sorted(d.glob(outs)): strip_rows(p, R / arm / p.name)
    for name in ("codebook.md", "adjudication-log.json", "adjudication-log-c.json", "reach5-adjudicated.json", "reachc-adjudicated.json", "tally-adj.txt", "tally-c-adj.txt", "tally-a.txt", "tally.txt", "tally-c.txt"):
        if (d / name).exists(): shutil.copyfile(d / name, R / arm / name)
    for name in ("adjudicate.py", "adjudicate_rev.py", "adjudicate_c.py", "tally.py", "tally_adj.py", "tally_c.py", "tally_c_adj.py"):
        if (d / name).exists(): shutil.copyfile(d / name, OUT / "scripts" / f"{arm}-{name}")
# calibration: the AP 94 as codes only (the lead coder's), without the abstracts
ap = json.load(open(SV / "abstract-reach.json"))
with open(R / "ancient" / "calibration-ap94.jsonl", "w") as f:
    for i, x in enumerate(ap): f.write(json.dumps({"id": f"ap-{i}", "year": x["year"], "title": x["title"], "code": x["reach"]}, ensure_ascii=False) + "\n")
for arm, d in [("continental", SV / "cont/reachc"), ("analytic", SV / "anal/reacha")]:
    shutil.copyfile(d / "calibration.txt", R / arm / "calibration.txt")   # the lead coder's codes and one-line descriptions, no abstracts
for name in ("reach-read.txt", "measures.txt", "measures-v2.txt", "compare.txt"):
    if (SV / name).exists(): shutil.copyfile(SV / name, R / name)

# 4. the standing baseline (titles and rulings)
for name in ("dpull.tsv", "dpull2.tsv", "standing.py", "standing.txt"):
    shutil.copyfile(SV / name, OUT / "standing" / name)
for name in ("standing2.py", "standing2.txt", "pull-philologus.tsv", "pull-cq.tsv", "pull-peitho.tsv"):
    shutil.copyfile(SV / "base2" / name, OUT / "standing" / name)
shutil.copyfile(SV / "cont" / "compare-cont.txt", OUT / "standing" / "compare-cont.txt")
for name in ("standing_persee.py", "standing-persee.txt", "standing_reg.py", "standing-reg.txt", "pull_fr.py"):   # the interim baseline (Revue philosophique de Louvain)
    if (SV / "interim" / name).exists(): shutil.copyfile(SV / "interim" / name, OUT / "standing" / name)

# 5. stylometry: the script and its output; the corpus (abstracts) is not seated
for name in ("stylo.py", "stylo.txt", "build.py"):
    shutil.copyfile(SV / "stylo" / name, OUT / "stylometry" / name)

# 6. scripts
for name in ("census.py", "census2.py", "code.py", "code2.py", "reach.py", "compare.py", "abstracts.py"):
    if (SV / name).exists(): shutil.copyfile(SV / name, OUT / "scripts" / name)
for rel in ("cont/code_cont.py", "cont/compare_cont.py", "interim/harvest_persee.py"):
    if (SV / rel).exists(): shutil.copyfile(SV / rel, OUT / "scripts" / pathlib.Path(rel).name)

# guard: no abstract text in any data file of the seat (a key "abstract" holding running text)
bad = [str(p) for p in OUT.rglob("*") if p.is_file() and p.suffix in (".json", ".jsonl", ".txt", ".tsv")
       and re.search(r'"abstract"\s*:\s*"[^"]{120,}', p.read_text(encoding="utf-8", errors="ignore"))]
assert not bad, bad
print("staged", sum(1 for p in OUT.rglob("*") if p.is_file()), "files")
