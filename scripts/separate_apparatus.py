#!/usr/bin/env python3
"""separate_apparatus.py — the body is the WORK. Apparatus belongs to the record.

═══════════════════════════════════════════════════════════════════════════════
THE STANDING RULE THIS ENFORCES (MANUS, 2026-08-06)
═══════════════════════════════════════════════════════════════════════════════

  Recording of method or modification does not appear in body text.

The archive declares deposited text immutable. That rule was violated in the
direction nobody watches: not by deletion but by ACCRETION. Restoration notes,
body-head-gate language, severed-DOI lines, self-referential AXN headers, YAML
frontmatter and retained metadata-capture appendices were written INTO bodies
that then present themselves as faithfully restored text.

On deposit #1230 — an open letter — the work is 7,913 characters and the
apparatus around it is 4,659. A reader asking for the letter receives the letter
plus 59% again of prose describing how the letter was processed. That is not a
restored record; it is a record with a commentary fused to it.

WHAT THIS DOES
  · HEAD APPARATUS  — the generator block before the first horizontal rule,
    when it carries restoration/AXN/dead-DOI markers
  · TAIL APPENDIX   — "Appendix — metadata-capture body (superseded …)" to end
  are LIFTED OUT of the body and PRESERVED on the record, never deleted. The
  archive does not destroy; it relocates and declares. The record page renders
  them after the work, where apparatus belongs.

WHAT IT REFUSES TO TOUCH
  Authored sections named "Methodology" or "Falsification Conditions" are part
  of many EA papers and are NOT apparatus. 263 bodies carry such headings and
  the overwhelming majority are the author's own. Only structurally
  generator-inserted blocks are lifted — identified by position and by markers
  no author writes about their own work ("Body-head gate passed", "Restoration
  status:", "self-reference in root form by pre-hash necessity").

  A body that would lose more than 70% of itself is skipped and reported: that
  signature means the detector is wrong about which part is the work.

Usage:
    python3 scripts/separate_apparatus.py --dry-run      # report only
    python3 scripts/separate_apparatus.py --apply
    python3 scripts/separate_apparatus.py --apply --only AXN-04DF
"""
import re, json, sys, pathlib, argparse, datetime

ROOT = pathlib.Path(__file__).resolve().parents[1]
TEXTS = ROOT / "data/texts"
REG = ROOT / "data/registry.json"
STORE = ROOT / "data/restoration-apparatus"

HEAD_MARKERS = (
    r"\*\*Restoration status:\*\*", r"^\*\*AXN:\*\* AXN:[0-9A-F]{3,4} — Alexanarch deposit",
    r"\*\*Dead DOI\(s\):\*\*", r"[Bb]ody-head gate", r"pre-hash necessity",
)
APPENDIX_RX = r"^#{1,3} Appendix — metadata-capture body"
MIN_KEEP = 0.30   # a work must retain at least 30% of its bytes, else skip and report


def split(text):
    """Return (work, head_apparatus, tail_apparatus)."""
    head = tail = ""
    body = text

    m = re.search(APPENDIX_RX, body, re.M)
    if m:
        tail = body[m.start():]
        body = body[:m.start()].rstrip()

    # HEAD: lift apparatus LINES only. The work's own title and subtitle are
    # content, not apparatus — an earlier cut took them wholesale, which would
    # have quietly deleted a paper's subtitle from its own body. Headings and
    # prose stay; only lines that record method or modification are lifted.
    rule = re.search(r"^---\s*$", body, re.M)
    if rule and any(re.search(p, body[:rule.start()], re.M) for p in HEAD_MARKERS):
        zone, rest = body[:rule.start()], body[rule.end():]
        keep, lift = [], []
        for line in zone.split("\n"):
            if any(re.search(p, line) for p in HEAD_MARKERS) or re.match(r"^\*\*[^*]+\*\* · restored", line):
                lift.append(line)
            else:
                keep.append(line)
        if lift:
            head = "\n".join(lift).strip()
            body = ("\n".join(keep).rstrip() + "\n\n" + rest.lstrip("\n")).strip()

    return body.strip(), head.strip(), tail.strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--only")
    a = ap.parse_args()
    if not (a.apply or a.dry_run):
        a.dry_run = True

    reg = json.loads(REG.read_text())
    by_hex = {}
    for d in reg["deposits"]:
        if d.get("hex"):
            by_hex.setdefault(d["hex"].upper().zfill(4), d)

    changed, skipped, untouched = [], [], 0
    for p in sorted(TEXTS.glob("AXN-*-text.md")):
        if a.only and a.only not in p.stem:
            continue
        original = p.read_text(errors="replace")
        work, head, tail = split(original)
        if not head and not tail:
            untouched += 1
            continue
        ratio = len(work) / max(len(original), 1)
        if ratio < MIN_KEEP:
            skipped.append((p.stem, round(ratio * 100)))
            continue
        changed.append((p.stem, len(original), len(work), len(head), len(tail)))

        if a.apply:
            hexk = p.stem.split("-")[1].upper().zfill(4)
            STORE.mkdir(parents=True, exist_ok=True)
            (STORE / f"{hexk}.json").write_text(json.dumps({
                "hex": hexk,
                "lifted_at": datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
                "rule": "Recording of method or modification does not appear in body text "
                        "(MANUS standing rule, 2026-08-06). Nothing is destroyed: this file holds "
                        "what was lifted, and the record page renders it after the work.",
                "head_apparatus": head,
                "tail_apparatus": tail,
                "body_bytes_before": len(original),
                "body_bytes_after": len(work),
            }, ensure_ascii=False, indent=1) + "\n")
            p.write_text(work + "\n")
            d = by_hex.get(hexk)
            if d is not None:
                d["apparatus_separated"] = True
                d["apparatus_path"] = f"/data/restoration-apparatus/{hexk}.json"

    if a.apply and changed:
        REG.write_text(json.dumps(reg, ensure_ascii=False, indent=2))

    print(f"bodies examined : {untouched + len(changed) + len(skipped)}")
    print(f"apparatus lifted: {len(changed)}")
    print(f"skipped (work would drop below {int(MIN_KEEP*100)}%): {len(skipped)}")
    if changed:
        print(f"\n{'file':<20}{'before':>9}{'work':>9}{'head':>8}{'tail':>8}{'apparatus':>11}")
        for stem, b, w, h, t in sorted(changed, key=lambda x: -(x[3] + x[4]))[:15]:
            print(f"{stem:<20}{b:>9,}{w:>9,}{h:>8,}{t:>8,}{100*(h+t)//b:>10}%")
    for stem, pc in skipped:
        print(f"  SKIP {stem} — work would be {pc}% of body; detector is wrong here")
    if a.dry_run:
        print("\n(dry run — nothing written)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
