#!/usr/bin/env python3
"""
deposit_completeness.py — per-deposit completeness gate (deposit-completeness/v1).

The capability register guards what the ARCHIVE can do; this guards what a
DEPOSIT carries. Doctrine that is not a machine check degrades to whatever the
tiredest instance ships — the 2026-08-09 MINT #1443/#1444 session shipped both
deposits with empty defines_concepts, empty related_deposits, no lexical
receipt, and records rendered before the citation graph existed, and nothing
refused. This gate refuses.

Runs as pipeline stage `completeness` (before commit) and standalone:
    python3 scripts/deposit_completeness.py --deposit-number N
Contract: data/api/deposit-completeness.json (registered in /api/index.json).
Attested absence is allowed and explicit: a deposit that genuinely coins no
terms sets `lexical_attested_none: true` in its registry entry — absence must
be a decision, never a default. Same for concepts and related deposits.
"""
from __future__ import annotations
import argparse, hashlib, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

def _load(p):
    return json.load(open(ROOT / p, encoding="utf-8"))

def check_deposit(n: int):
    reg = _load("data/registry.json")
    entry = next((d for d in reg["deposits"] if d.get("deposit_number") == n), None)
    fails = []
    if entry is None:
        return [("EXIST-001", f"deposit #{n} not in registry")]
    hexid = entry.get("hex", "")

    # WIKI-002 — authored substance, not merely non-empty
    if len(str(entry.get("wiki_article") or "").split()) < 60:
        fails.append(("WIKI-002", "wiki_article under 60 words; author it in-session"))

    # CONCEPTS-001
    if not entry.get("defines_concepts") and not entry.get("concepts_attested_none"):
        fails.append(("CONCEPTS-001",
                      "defines_concepts empty and not attested-none; author in-session "
                      "or set concepts_attested_none: true"))

    # RELATED-001
    if not entry.get("related_deposits") and not entry.get("related_attested_none"):
        fails.append(("RELATED-001",
                      "related_deposits empty and not attested-none"))

    # LEX-001 — the minting registry grows or consciously declines with every mint
    lmr = _load("data/lexical-minting-registry.json")
    mine = [t for t in lmr.get("terms", []) if t.get("defined_in_deposit") == n]
    if not mine and not entry.get("lexical_attested_none"):
        fails.append(("LEX-001",
                      "no lexical-minting-registry rows for this deposit and not "
                      "attested-none; mint the deposit's coinages or set "
                      "lexical_attested_none: true"))

    # CITE-001 — body AXN references must be in the citation graph
    txt_path = entry.get("full_text_path", f"/data/texts/AXN-{hexid}-text.md")
    body = ""
    fp = ROOT / txt_path.lstrip("/")
    if fp.exists():
        body = fp.read_text(encoding="utf-8")
    # Citation grammar alignment (2026-08-09): the checker counts what the
    # extractor's grammar recognizes — full-form references OUTSIDE code
    # fences and inline backtick spans. #1443's R·14 table wraps its thirty
    # archive citations in backticks (glyph-preserving typography); whether
    # such display references should also mint edges is a flagged policy
    # question for MANUS, not a unilateral corpus-wide re-extraction.
    _scan = re.sub(r"```.*?```", " ", body, flags=re.S)
    _scan = re.sub(r"`[^`\n]*`", " ", _scan)
    targets = {h for h in re.findall(r"AXN:([0-9A-F]{4})\.", _scan) if h != hexid}
    if targets:
        cg = _load("data/citation-graph.json")
        edges = cg.get("edges", cg if isinstance(cg, list) else [])
        mine_e = {e.get("target_axn", "")[4:8]
                  for e in edges if e.get("source_deposit") == n}
        missing = targets - mine_e
        if missing:
            fails.append(("CITE-001",
                          f"body references AXN hex(es) {sorted(missing)} absent from "
                          "citation-graph edges for this deposit; run "
                          "scripts/citation_extractor.py"))

    # RENDER-001 — the record as a reader sees it
    rec = ROOT / f"s/records/{n}/index.html"
    if not rec.exists():
        fails.append(("RENDER-001", "record page missing"))
    else:
        h = rec.read_text(encoding="utf-8")
        arts = h.count("<p>#") + h.count("<p>---</p>") + h.count("<p>&gt;")
        if arts:
            fails.append(("RENDER-001",
                          f"record page carries {arts} literal-markdown artifact(s) "
                          "(<p>#… / <p>--- / <p>&gt;…); re-render with current "
                          "wire_deposit"))
        if entry.get("axn", "").split(".")[0] not in h:
            fails.append(("RENDER-001", "record page does not carry its own AXN"))

    # FILES-001 — declared files exist and match
    for f in entry.get("files") or []:
        p = ROOT / f["path"].lstrip("/")
        if not p.exists():
            fails.append(("FILES-001", f"declared file missing on disk: {f['path']}"))
            continue
        data = p.read_bytes()
        if len(data) != f.get("bytes") or hashlib.sha256(data).hexdigest() != f.get("sha256"):
            fails.append(("FILES-001", f"sha/bytes mismatch: {f['path']}"))

    return fails

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--deposit-number", type=int, required=True)
    args = ap.parse_args()
    fails = check_deposit(args.deposit_number)
    if fails:
        print(f"Deposit #{args.deposit_number}: {len(fails)} completeness failure(s)\n")
        for rid, msg in fails:
            print(f"  [{rid}] {msg}")
        print("\nContract: data/api/deposit-completeness.json (deposit-completeness/v1)")
        sys.exit(1)
    print(f"✓ Deposit #{args.deposit_number}: complete "
          f"(wiki, concepts, related, lexical, citations, render, files)")

if __name__ == "__main__":
    main()
