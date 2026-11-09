"""Check an argument-layer file against the seated texts.   python3 check_args.py <alexanarch root> <file.jsonl> [more.jsonl ...]
Each line: {"id","record","section","move","exact","edges":[{"rel","to"}], optional "notes"}.
Checks: record exists; exact occurs verbatim in the record's seated text (data/registry.json full_text_path); ids unique and prefixed a<record>-;
move in KINDS; rel in RELS; every edge target resolves to an id in the files checked together, or to an id in argument_1735.jsonl.
Writes record_sha256 into each line on success (same file, rewritten)."""
import json, pathlib, sys, hashlib
KINDS = {"test", "method", "datum", "count", "inference", "finding", "price", "rival", "reply", "defeat", "hypothesis", "state"}
RELS = {"supports", "infers_from", "answers", "prices", "defeats_if", "applies", "qualifies", "bounds", "develops", "revises"}
ROOT = pathlib.Path(sys.argv[1]); files = [pathlib.Path(f) for f in sys.argv[2:]]
REG = {r["deposit_number"]: r for r in json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8"))["deposits"]}
here = pathlib.Path(__file__).parent
known = {json.loads(l)["id"] for l in (here / "argument_1735.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()}
rows = {f: [json.loads(l) for l in f.read_text(encoding="utf-8").splitlines() if l.strip()] for f in files}
ids = [r["id"] for rs in rows.values() for r in rs]; allids = set(ids) | known
errs = []
if len(ids) != len(set(ids)): errs.append(("duplicate ids", sorted({i for i in ids if ids.count(i) > 1})))
texts = {}
for f, rs in rows.items():
    for r in rs:
        n = r.get("record")
        if n not in REG: errs.append((r["id"], "no record", n)); continue
        if n not in texts:
            p = ROOT / REG[n]["full_text_path"].lstrip("/"); texts[n] = (p.read_text(encoding="utf-8"), hashlib.sha256(p.read_bytes()).hexdigest())
        t, h = texts[n]
        if not r["id"].startswith(f"a{n}-"): errs.append((r["id"], "id prefix"))
        if r.get("move") not in KINDS: errs.append((r["id"], "move", r.get("move")))
        if not r.get("exact") or r["exact"] not in t: errs.append((r["id"], "quote not verbatim", (r.get("exact") or "")[:80]))
        for e in r.get("edges", []):
            if e.get("rel") not in RELS: errs.append((r["id"], "rel", e.get("rel")))
            if e.get("to") not in allids: errs.append((r["id"], "dangling", e.get("to")))
        r["record_sha256"] = h
from collections import Counter
for f, rs in rows.items():
    print(f.name, len(rs), "moves", dict(Counter(r["move"] for r in rs)), "records", sorted({r["record"] for r in rs}))
if errs:
    print("ERRORS", len(errs)); [print(" ", e) for e in errs[:60]]; sys.exit(1)
for f, rs in rows.items(): f.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rs), encoding="utf-8")
print("OK")
