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

    # ── BODY-001 / BODY-002 ────────────────────────────────────────────────
    # Added 2026-08-13 after TACHYON asserted "31 bodiless deposits" on the
    # strength of checking ONE path convention, and proposed a remedy that
    # would have cut 104KB from AXN-0434 and collapsed three versions of
    # Machine-Mediated Resistance Literature into one file.
    #
    # THE ARCHIVE STORES EVERY BODY TWICE, ON PURPOSE:
    #   data/texts/AXN-<HEX>-text.md   canonical text; the AXN hash is over this
    #   data/deposits/AXN-<HEX>.md     download alias; YAML frontmatter + body
    # A deposit is not complete until BOTH resolve, and the alias is not an
    # alias if it carries only frontmatter.
    #
    # ABSENCE IS A CLAIM, AND A CLAIM NEEDS EVERY PLACE THE THING COULD BE.
    text_p = ROOT / f"data/texts/AXN-{hexid}-text.md"
    depo_p = ROOT / f"data/deposits/AXN-{hexid}.md"
    have_text, have_depo = text_p.exists(), depo_p.exists()

    if not (have_text and have_depo):
        missing = " and ".join(
            p for p, ok in ((str(text_p), have_text), (str(depo_p), have_depo)) if not ok)
        fails.append(("BODY-001",
                      f"body absent at {missing}; a deposit must resolve under BOTH "
                      f"path conventions, never one"))
    else:
        # BODY-002 — the alias must carry the work, not just its metadata.
        # Frontmatter runs to the second '---'. What follows must be substantial
        # relative to the canonical text, or the alias is a stub that serves a
        # header to anyone who fetches the deposit.
        def _strip_frontmatter(raw: str) -> str:
            if raw.lstrip().startswith("---"):
                parts = raw.lstrip().split("---", 2)
                if len(parts) == 3:
                    return parts[2]
            return raw

        # BOTH sides are stripped before comparison. Comparing an alias BODY
        # against a canonical file INCLUDING its frontmatter made #1095 a false
        # positive: its body is 1,057 bytes on both sides, and only the 1,068
        # bytes of YAML on the canonical side tripped the threshold.
        body = _strip_frontmatter(depo_p.read_text(encoding="utf-8", errors="replace"))
        canon = len(_strip_frontmatter(
            text_p.read_text(encoding="utf-8", errors="replace")).strip())
        if canon > 2000 and len(body.strip()) < canon * 0.5:
            fails.append(("BODY-002",
                          f"download alias is a STUB: {len(body.strip())} bytes of body "
                          f"against {canon} bytes of canonical text. Rebuild the alias as "
                          f"frontmatter + full canonical text."))

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

    # ── BODY-003 ───────────────────────────────────────────────────────────
    # Added 2026-08-15 after #1486 and #1487 minted with a canonical text made
    # ENTIRELY of metadata sections -- Description, Methodology, Falsification,
    # Files -- and no work in it at all. Both passed every gate then in force:
    # the files existed, the alias resolved, the byte counts matched, because
    # the same emptiness was faithfully written to both paths.
    #
    # BODY-001 asks whether a body exists. BODY-002 asks whether the two copies
    # agree. NEITHER ASKS WHETHER THE THING IS THE WORK. A deposit whose text is
    # its own metadata re-rendered is a deposit of its own catalogue card.
    #
    # The depositor supplies the work through the Body field. If a deposit is
    # genuinely metadata-only -- a pointer record, a tether stub -- that is a
    # decision, and it is declared, not defaulted into by omission.
    if have_text:
        raw = text_p.read_text(encoding="utf-8", errors="replace")
        after_fm = raw.split("---", 2)[2] if raw.lstrip().startswith("---") and len(raw.split("---", 2)) == 3 else raw
        META_HEADS = ("## Description", "## Methodology", "## Falsification Conditions",
                      "## Files", "## Keywords", "## Terms", "## Related Identifiers")
        substantive = []
        for block in after_fm.split("\n## "):
            head = ("## " + block.split("\n", 1)[0].strip()) if not block.startswith("#") else block.split("\n", 1)[0].strip()
            if any(head.startswith(m) for m in META_HEADS):
                continue
            substantive.append(block)
        body_chars = sum(len(b) for b in substantive)
        title_only = body_chars < 400
        if title_only and not entry.get("metadata_only_attested"):
            fails.append(("BODY-003",
                          f"canonical text carries {body_chars} chars outside metadata sections "
                          f"(Description/Methodology/Falsification/Files): the work is absent from "
                          f"its own deposit. Supply it via the Body field, or set "
                          f"metadata_only_attested: true to declare a pointer record."))

    # RENDER-001 — the record as a reader sees it
    rec = ROOT / f"s/records/{n}/index.html"
    if not rec.exists():
        fails.append(("RENDER-001", "record page missing"))
    else:
        h = rec.read_text(encoding="utf-8")
        # A markdown heading is "# " — hash, SPACE, text. A paragraph opening
        # "#NewHuman" is a hashtag and one opening "#1287's truth title" is a
        # deposit reference in a sentence. Both are correct prose and neither is
        # an unconverted heading. Requiring the space removes 5 false positives
        # found on 2026-08-09 across #1442 (four hashtag lines quoted verbatim
        # from the source posts) and #1445 (a sentence beginning with a record
        # number). Checking for the literal marker rather than the syntax would
        # push an editor to alter deposited text to satisfy a checker.
        import re as _re3
        arts = (len(_re3.findall(r"<p>#{1,6} ", h))
                + h.count("<p>---</p>")
                + h.count("<p>&gt; "))
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
