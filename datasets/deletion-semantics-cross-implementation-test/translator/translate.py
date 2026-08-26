#!/usr/bin/env python3
"""okf-shape-translator — render the 111-case deletion-conformance corpus into the
remember/0.2 emitted shape (log.md + store records + .manifest.json), recording every
place the translation must invent a key the emitter does not define.

Promised on knowledge-catalog#207: "run its shape against these cases and send you
what breaks." STRICT mode refuses to invent; FORCED mode translates everything, to
show what a permissive translator would produce. MIT, stdlib only.
"""
import json, re, sys, hashlib
from pathlib import Path
from collections import Counter, defaultdict

# Keys the remember/0.2 emitter actually defines, read off its published bundle.
EMITTER_RECORD_KEYS = {"id","summary","type","generated","verified","status",
    "reliability","confidence","provenance","block","tags","timestamps","basis","validity"}
EMITTER_MANIFEST_KEYS = {"lessonId","outputPath","sourceHash","compiledAt","summary","block","tags","status"}

def slug(s, n=60):
    return re.sub(r"-+","-", re.sub(r"[^a-z0-9]+","-", s.lower())).strip("-")[:n] or "x"

def translate(case, mode):
    """Return (log_entry|None, record|None, breaks[]). A break is a corpus field with
    no home in the emitter's shape."""
    breaks = []
    ident = case.get("identifier","")
    kind  = case.get("identifier_kind","")
    axes  = case.get("axes") or {}
    rec   = case.get("recorded") or {}

    # --- BREAK 1: identity semantics -----------------------------------------
    # The emitter's `id` is a producer-controlled lesson key. A DOI is a handle to a
    # foreign resolver. Putting one in the other conflates "I wrote this here" with
    # "that identifier resolves" — the exact distinction never_landed depends on.
    producer_controlled = kind in ("declared_path",) or (case.get("axis_subject") or {}).get("kind") == "registry_assertion"
    if not producer_controlled:
        breaks.append(("identity", kind, "foreign identifier has no producer-controlled `id` slot"))
        if mode == "strict":
            return None, None, breaks

    rid = slug(ident if producer_controlled else f"{kind}-{ident}")

    # --- remaining fields, each seeking a home -------------------------------
    if case.get("successor"):
        breaks.append(("successor", case.get("successor_kind"), "no emitter key for succession; tombstones.md has no manifest schema"))
    if case.get("reason"):
        breaks.append(("reason", (case["reason"] or {}).get("actor"), "no emitter key for removal actor/reason"))
    if axes.get("presence"):
        breaks.append(("presence", axes["presence"], "`status` carries compile state, not presence"))
    obs = [k for k in case if k.startswith("observed")]
    if obs:
        breaks.append(("observation", obs[0], "no observation-boundary key; timestamps are producer-side"))
    if kind:
        breaks.append(("identifier_kind", kind, "no emitter key"))

    record = {
        "id": rid,
        "summary": (case.get("work_title") or ident)[:120],
        "type": "fact",
        "generated": {"by":"okf-shape-translator/0.1","at":"2026-08-26T00:00:00.000Z"},
        "verified": case.get("evidence", []),          # the one partial fit
        "status": "stable",
        "reliability": {"confidence":"established"},
        "confidence": "established",
        "provenance": "observed",
        "block": "deletion-conformance",
        "tags": ["okf","deletion", case.get("case_class","")],
        "timestamps": {"created":"2026-07-28T00:00:00.000Z","updated":"2026-07-28T00:00:00.000Z"},
        "basis": "live-source",
        "validity": None,
    }
    assert set(record) <= EMITTER_RECORD_KEYS, set(record) - EMITTER_RECORD_KEYS

    # A write-claim is only truthful where the record asserted a body at a place the
    # producer controls. In forced mode we emit one anyway, which is the point.
    declared = (kind == "declared_path" or "declared_state" in rec
                or (case.get("axis_subject") or {}).get("kind") == "registry_assertion")
    log_entry = None
    if declared or mode == "forced":
        noun = "Record" if declared else "Lesson"
        log_entry = f"* **{noun} created**: lesson {rid} `__row__`"
        if not declared:
            breaks.append(("claim", case.get("case_class"), "forced: emitting a write-claim for an assertion the producer never made"))
    # did the thing land?
    observed = " ".join(str(v) for k,v in case.items() if k.startswith("observed")).lower()
    landed = not any(w in observed for w in ("absent","missing","not present","no body"))
    return log_entry, (record if landed else None), breaks

def run(cases, mode, out):
    out = Path(out); (out/"store"/"facts").mkdir(parents=True, exist_ok=True)
    log = ["# Directory Update Log", "", "## 2026-07-28", ""]
    manifest, allbreaks, emitted, skipped = {"version":1,"entries":{}}, [], 0, 0
    refusals = []
    for c in cases:
        entry, record, breaks = translate(c, mode)
        if entry is None and record is None:
            # Case not emitted: its breaks are REFUSALS (why it was untranslatable),
            # not coercions. Conflating the two makes strict mode look lossy when it
            # was in fact honest — a receipt that flatters itself is worse than none.
            for b in breaks: refusals.append((c.get("case_class"),)+b)
            skipped += 1; continue
        for b in breaks: allbreaks.append((c.get("case_class"),)+b)
        if entry: log.append(entry); emitted += 1
        if record:
            p = out/"store"/"facts"/f"{record['id']}.md"
            fm = json.dumps(record, indent=1)  # frontmatter-equivalent; id_key readable
            body = "---\n" + "\n".join(
                f"{k}: {json.dumps(v) if isinstance(v,(dict,list)) else (v if v is not None else '')}"
                for k,v in record.items()) + "\n---\n"
            p.write_text(body)
            manifest["entries"][record["id"]] = {"lessonId":record["id"],
                "outputPath":f"facts/{p.name}", "sourceHash":hashlib.sha256(body.encode()).hexdigest(),
                "compiledAt":"2026-08-26T00:00:00.000Z","summary":record["summary"],
                "block":record["block"],"tags":record["tags"],"status":"compiled"}
    (out/"log.md").write_text("\n".join(log)+"\n")
    (out/"store"/".manifest.json").write_text(json.dumps(manifest, indent=1))
    return {"mode":mode,"log_claims":emitted,"records":len(manifest["entries"]),
            "skipped_untranslatable":skipped,"breaks":allbreaks,"refusals":refusals}

if __name__ == "__main__":
    data = json.loads(Path("cases.json").read_text())
    cases = data["cases"] if isinstance(data, dict) else data
    print(f"corpus: {len(cases)} cases\n")
    for mode in ("strict","forced"):
        r = run(cases, mode, f"out-{mode}")
        print(f"── {mode.upper()} ──")
        print(f"  log claims emitted : {r['log_claims']}")
        print(f"  store records      : {r['records']}")
        print(f"  untranslatable     : {r['skipped_untranslatable']}")
        bk = Counter(b[1] for b in r["breaks"])
        print(f"  breaks by class    : {dict(bk)}")
        json.dump([list(b) for b in r["breaks"]], open(f"breaks-{mode}.json","w"), indent=1)
        print()
