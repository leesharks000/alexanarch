"""The argument layer of a framework kernel (v1.1, at the author's word of 2026-11-09 09:55: "the hologram needs deeper density of compressed
evidentiary claims and argumentation. it is supposed to be a hologram of the whole").

Moves are read by parallel readers, one range of records each, every quotation extracted from the seated text and asserted verbatim
(check_args.py), in the form of the calibration exemplar (#1735, argument_1735.jsonl). This module takes the moves of a kernel's records,
re-asserts each quotation against the record as it now stands, binds the current hash, and writes 04-arguments.jsonl. An edge to a move of a
record outside the kernel is kept, typed external, with that kernel-free id."""
import json, pathlib, hashlib, collections

HERE = pathlib.Path(__file__).parent
KINDS = ["test", "method", "datum", "count", "inference", "finding", "price", "rival", "reply", "defeat", "hypothesis", "state"]
RELS = {"supports": "the move is evidence or ground for its target", "infers_from": "the move is concluded from its target",
        "answers": "a reply to a rival position", "prices": "a cost the record names against its own target claim",
        "defeats_if": "a stated condition under which the target falls", "applies": "the move applies a method or test to its target",
        "qualifies": "the move limits or grades its target", "bounds": "the move sets the strength or scope of its target, leaving it held",
        "develops": "the move extends its target", "revises": "the move replaces its target in a later state of the record or of the archive"}


def all_moves():
    rows = []
    for f in sorted((HERE / "args").glob("*.jsonl")) + [HERE / "argument_1735.jsonl"]:
        rows += [json.loads(l) for l in f.read_text(encoding="utf-8").splitlines() if l.strip()]
    return rows


def build(root, records, out_dir, readers_note):
    """records: the kernel's deposit numbers. Returns (moves written, summary for 00-kernel.yaml)."""
    root = pathlib.Path(root); REG = {r["deposit_number"]: r for r in json.loads((root / "data/registry.json").read_text(encoding="utf-8"))["deposits"]}
    texts = {}
    for n in records:
        p = root / REG[n]["full_text_path"].lstrip("/"); texts[n] = (p.read_text(encoding="utf-8"), hashlib.sha256(p.read_bytes()).hexdigest())
    mine = [m for m in all_moves() if m["record"] in records]
    ids = {m["id"] for m in mine}; out, stale = [], []
    for m in mine:
        t, h = texts[m["record"]]
        if m["exact"] not in t: stale.append(m["id"]); continue
        o = {"@id": f"arg:{m['id']}", "@type": "Move", "move": m["move"], "record": f"rec:{m['record']}", "axn": REG[m["record"]]["axn"],
             "record_sha256": h, "section": m.get("section"), "exact": m["exact"],
             "edges": [{"rel": e["rel"], "to": f"arg:{e['to']}"} if e["to"] in ids else {"rel": e["rel"], "to_external": e["to"]} for e in m.get("edges", [])]}
        if m.get("notes"): o["notes"] = m["notes"]
        out.append(o)
    (pathlib.Path(out_dir) / "04-arguments.jsonl").write_text("".join(json.dumps(o, ensure_ascii=False) + "\n" for o in out), encoding="utf-8")
    by_rec = collections.Counter(int(o["record"].split(":")[1]) for o in out)
    summary = {"file": "04-arguments.jsonl", "moves": len(out), "edges": sum(len(o["edges"]) for o in out),
               "records_with_moves": len(by_rec), "records_without_moves": sorted(set(records) - set(by_rec)),
               "by_kind": {k: sum(1 for o in out if o["move"] == k) for k in KINDS if any(o["move"] == k for o in out)},
               "kinds": KINDS, "relations": RELS, "quotations_stale_at_build": stale,
               "how_read": readers_note,
               "reading_instruction": ("A reader reconstructing a record's argument reads its moves in 04-arguments.jsonl in order with their edges: data and counts "
                                       "support inferences and findings; prices, rivals, replies and defeat conditions stand beside the claims they bear on; "
                                       "hypotheses and states keep the strength the record gives them. Each quotation is verbatim, bound to the record's hash.")}
    return out, summary


def verify(root, KD):
    """T20–T22: each move verbatim in its record at the bound hash; each edge resolved or typed external, its relation in the vocabulary;
    the kernel's records with and without moves. Recorded, not blocking."""
    root = pathlib.Path(root); KD = pathlib.Path(KD)
    REG = {r["deposit_number"]: r for r in json.loads((root / "data/registry.json").read_text(encoding="utf-8"))["deposits"]}
    A = [json.loads(l) for l in (KD / "04-arguments.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
    ids = {a["@id"] for a in A}; cache = {}; bad, badh, bade, badr = [], [], [], []
    for a in A:
        n = int(a["record"].split(":")[1])
        if n not in cache:
            p = root / REG[n]["full_text_path"].lstrip("/"); cache[n] = (p.read_text(encoding="utf-8"), hashlib.sha256(p.read_bytes()).hexdigest())
        t, h = cache[n]
        if a["exact"] not in t: bad.append(a["@id"])
        if a["record_sha256"] != h or h != REG[n]["hash"]: badh.append(a["@id"])
        for e in a["edges"]:
            if e["rel"] not in RELS: badr.append((a["@id"], e["rel"]))
            if "to" in e and e["to"] not in ids: bade.append((a["@id"], e["to"]))
    ext = sum(1 for a in A for e in a["edges"] if "to_external" in e)
    return {"T20 every move verbatim in its record, at the record's current hash": {"pass": not bad and not badh, "detail": {"moves": len(A), "not_verbatim": bad[:6], "hash_stale": badh[:6]}},
            "T21 every move edge resolves, or is typed external; every relation in the vocabulary": {"pass": not bade and not badr, "detail": {"edges": sum(len(a['edges']) for a in A), "external": ext, "unresolved": bade[:6], "bad_relation": badr[:6]}}}
