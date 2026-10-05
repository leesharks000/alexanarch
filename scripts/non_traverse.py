#!/usr/bin/env python3
"""non_traverse.py — D/R/O candidate traversal for a /non row (EA-NEGONT-02 v0.7 §3.4, ruled 2026-10-05).

The ruling: S1–S3 are replaced by three strata of the archive's bearing on an address.

  D  direct      the archive names the entity (by its string or an alias) and says something about it.
  R  relational  the archive states a relation between the entity and an archive object (a heteronym, a mantle,
                 a work of the archive, the archive itself), whether or not the entity is the text's topic.
  O  ontological the archive applies one of its own categories (a defined concept or lexical mint) to the entity
                 (O-direct), or to a class the entity belongs to (O-class). Guard: O counts only where the archive
                 applies the category itself. Class membership must be sourced: from the disclosed field B or
                 from the archive, by locus, given in the address config. The composer never applies an archive
                 category on its own judgment.

This script finds CANDIDATES only, by string. Admission is by reading (§3.4: a candidate is admitted when the
sentence or its paragraph makes a claim of the stratum's kind), recorded with its reason in the row's reading
file. Volume is never a ground for removal (S4 stands). Integrity (S5) is checked here: a deposit whose
text path is missing is reported and skipped.

Usage:  python3.12 scripts/non_traverse.py <address-config.json> [--out DIR]
Config: {"row": "howl", "address": "howl", "entity": "Howl (Ginsberg, 1956)",
         "aliases": [{"pattern": "\\bHowl\\b", "flags": ""}, ...],
         "classes": [{"term": "Beat", "pattern": "\\bBeat\\b", "basis": "field: B1 ... or archive: #N locus"}],
         "exclude_deposits": [], "notes": "..."}
Outputs (in DIR, default datasets/negative-of-the-negative/v2/traversal/<row>/):
  candidates-D.jsonl, candidates-R.jsonl, candidates-O.jsonl, summary.json; and, on the second pass (config
  "hop_from": the deposits admitted by reading), candidates-H.jsonl: one citation hop forward and back.
Deterministic: same config, same registry, same texts -> same files (sorted, no timestamps in candidates).
"""
import json, re, sys, pathlib, argparse, hashlib, collections

ROOT = pathlib.Path(__file__).resolve().parent.parent

def load_registry():
    return json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8"))["deposits"]

def sentences(text):
    """Paragraph-first split; sentences inside paragraphs. Returns (para_index, sentence)."""
    out = []
    paras = re.split(r"\n\s*\n", text)
    for pi, p in enumerate(paras):
        p = re.sub(r"\s+", " ", p).strip()
        if not p:
            continue
        for s in re.split(r"(?<=[.!?])\s+(?=[A-Z“\"'(\[*#])", p):
            s = s.strip()
            if s:
                out.append((pi, s[:900]))
    return out

def heteronym_names():
    names = set()
    p = ROOT / "datasets/heteronyms/heteronyms.jsonl"
    for line in p.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        r = json.loads(line)
        n = (r.get("name") or "").strip()
        if n and len(n) > 3:
            names.add(n)
    return names

ARCHIVE_OBJECTS_FIXED = ["Crimson Hexagon", "Crimson Hexagonal", "the archive", "Alexanarch", "New Human",
                         "King of May", "Good Gray Poet", "Prince of Poets", "mantle", "Dodecad", "heteronym"]

def archive_categories(reg):
    """The archive's own categories: registry defines_concepts plus lexical mints, multiword or >= 8 chars,
    with generic English filtered by requiring the term to be defined in a deposit."""
    cats = {}
    for x in reg:
        for c in (x.get("defines_concepts") or []):
            if isinstance(c, str):
                t = c.strip()
                if len(t) >= 8 and (" " in t or "-" in t):
                    cats.setdefault(t, x["deposit_number"])
    lx = json.loads((ROOT / "data/lexical-minting-registry.json").read_text(encoding="utf-8"))
    for t in (lx.get("terms") if isinstance(lx, dict) else lx) or []:
        term = (t.get("term") or "").strip().strip('"').strip()
        if len(term) >= 8 and " " in term and len(term) <= 60 and not re.search(r"[\":;]", term):
            cats.setdefault(term, t.get("defined_in_deposit"))
    return cats

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("config")
    ap.add_argument("--out")
    a = ap.parse_args()
    cfg = json.loads(pathlib.Path(a.config).read_text(encoding="utf-8"))
    row = cfg["row"]
    out = pathlib.Path(a.out) if a.out else ROOT / f"datasets/negative-of-the-negative/v2/traversal/{row}"
    out.mkdir(parents=True, exist_ok=True)

    reg = load_registry()
    aliases = [re.compile(al["pattern"], re.I if "i" in al.get("flags", "") else 0) for al in cfg["aliases"]]
    classes = [(c["term"], re.compile(c["pattern"], re.I if "i" in c.get("flags", "") else 0), c["basis"]) for c in cfg.get("classes", [])]
    objects = sorted(set(ARCHIVE_OBJECTS_FIXED) | heteronym_names(), key=lambda s: (-len(s), s))
    obj_re = re.compile(r"\b(" + "|".join(re.escape(o) for o in objects) + r")\b", re.I)
    cats = archive_categories(reg)
    # compile categories in chunks (python re handles a few thousand alternatives)
    cat_terms = sorted(cats, key=lambda s: (-len(s), s))
    cat_res = [re.compile(r"\b(" + "|".join(re.escape(t) for t in cat_terms[i:i + 1500]) + r")\b", re.I)
               for i in range(0, len(cat_terms), 1500)]
    excl = set(cfg.get("exclude_deposits", []))

    D, R, O = [], [], []
    integrity = []
    entity_triples = []
    scanned = 0
    for x in sorted(reg, key=lambda r: r["deposit_number"]):
        n = x["deposit_number"]
        if n in excl:
            continue
        for e in (x.get("entities") or []):
            s = json.dumps(e, ensure_ascii=False)
            if any(al.search(s) for al in aliases):
                entity_triples.append({"dep": n, "triple": e})
        fp = (x.get("full_text_path") or "").strip()
        if not fp or not re.search(r"\.(md|txt)$", fp):
            continue          # non-text records (JSON stores, PDFs) are excluded by type, as S2 excluded them
        path = ROOT / fp.lstrip("/")
        if not path.exists():
            integrity.append({"dep": n, "path": fp, "defect": "text path missing"})
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        scanned += 1
        cls_hit = [c for c in classes if c[1].search(text)]
        if not any(al.search(text) for al in aliases) and not cls_hit:
            continue
        sents = sentences(text)
        for si, (pi, s) in enumerate(sents):
            hit_alias = [al.pattern for al in aliases if al.search(s)]
            hit_class = [c[0] for c in classes if c[1].search(s)]
            if not hit_alias and not hit_class:
                continue
            base = {"dep": n, "title": (x.get("title") or "")[:160], "date": x.get("date"), "para": pi, "sent": si,
                    "sentence": s}
            catm = sorted({m.group(1) for cr in cat_res for m in cr.finditer(s)}, key=str.lower)
            if hit_alias:
                D.append(dict(base, alias=hit_alias))
                objm = sorted({m.group(1) for m in obj_re.finditer(s)}, key=str.lower)
                if objm:
                    R.append(dict(base, alias=hit_alias, objects=objm))
                if catm:
                    O.append(dict(base, alias=hit_alias, kind="O-direct", categories=catm))
            if hit_class and catm and not hit_alias:
                O.append(dict(base, classes=hit_class, kind="O-class", categories=catm,
                              class_basis={c[0]: c[2] for c in classes if c[0] in hit_class}))

    def write(name, rows, prefix):
        for i, r in enumerate(rows, 1):
            r["cand_id"] = f"{prefix}{i:04d}"
        p = out / name
        p.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")
        return hashlib.sha256(p.read_bytes()).hexdigest()

    hD, hR, hO = write("candidates-D.jsonl", D, "D"), write("candidates-R.jsonl", R, "R"), write("candidates-O.jsonl", O, "O")

    # H, the hop (second pass). One citation hop, forward and back, from deposits ALREADY ADMITTED by reading at
    # D, R or O (config "hop_from"), over the archive's internal citation graph. Each hop candidate is read into
    # a stratum or rejected; the hop finds term-absent sources that string matching cannot.
    H = []
    hop_from = set(cfg.get("hop_from") or [])
    if hop_from:
        g = json.loads((ROOT / "data/citation-graph.json").read_text(encoding="utf-8"))["edges"]
        byn = {x["deposit_number"]: x for x in reg}
        seen = {}
        for e in g:
            s_, t_ = e.get("source_deposit"), e.get("target_deposit")
            if s_ in hop_from and t_ not in hop_from and t_ in byn and t_ not in excl:
                seen.setdefault((t_, "forward"), set()).add(s_)
            if t_ in hop_from and s_ not in hop_from and s_ in byn and s_ not in excl:
                seen.setdefault((s_, "reverse"), set()).add(t_)
        for (n_, d_), via in sorted(seen.items()):
            H.append({"dep": n_, "title": (byn[n_].get("title") or "")[:160], "date": byn[n_].get("date"),
                      "direction": d_, "via_admitted": sorted(via)})
    hH = write("candidates-H.jsonl", H, "H") if hop_from else None
    per = lambda rows: dict(sorted(collections.Counter(r["dep"] for r in rows).items()))
    summary = {
        "row": row, "address": cfg["address"], "entity": cfg.get("entity"), "procedure": "EA-NEGONT-02 v0.7 §3.4 (D/R/O), working; not frozen",
        "config": cfg, "texts_scanned": scanned,
        "counts": {"D_sentences": len(D), "D_deposits": len(per(D)), "R_sentences": len(R), "R_deposits": len(per(R)),
                   "O_direct": sum(1 for r in O if r["kind"] == "O-direct"), "O_class": sum(1 for r in O if r["kind"] == "O-class"),
                   "O_deposits": len(per(O)), "H_candidates": len(H)},
        "per_deposit": {"D": per(D), "R": per(R), "O": per(O)},
        "registry_entity_triples": entity_triples,
        "integrity_S5": integrity,
        "sha256": {"candidates-D.jsonl": hD, "candidates-R.jsonl": hR, "candidates-O.jsonl": hO, "candidates-H.jsonl": hH},
        "category_vocabulary": {"defines_concepts_and_lexical_mints": len(cats)},
        "note": "Candidates by string only. Admission by reading, recorded in the row's reading file; nothing here is admitted.",
    }
    (out / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(summary["counts"]), "→", out.relative_to(ROOT))

if __name__ == "__main__":
    main()
