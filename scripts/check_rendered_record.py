#!/usr/bin/env python3
"""check_rendered_record.py — validate a record AS A READER SEES IT.

Every other gate reads the registry or the files. This one reads the rendered
HTML and strips it to text, because the failures that reach readers are the
ones no data-level check catches:

  #1486 (2026-08-15) passed BODY-001/002/003, RENDER-001, completeness and
  validate while its live page showed a stale AXN glyph, the [DEPOSIT] issue
  prefix in two places, the description printed twice, metadata fields as body
  sections, and the literal string "full_text_path" where a path belonged.
  It was reported by the operator, not by any gate, because the depositor had
  verified a <title> tag and a raw file and called it done.

  A raw file on GitHub is not a rendered page. A registry entry is not a
  rendered page. Only the rendered page is the rendered page.

Usage: check_rendered_record.py <deposit_number> [...]
"""
import json, re, sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent

def plain(html: str) -> str:
    t = re.sub(r'<script.*?</script>', ' ', html, flags=re.S)
    t = re.sub(r'<style.*?</style>', ' ', t, flags=re.S)
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', t))

def check(n: int):
    reg = json.loads((ROOT/"data/registry.json").read_text())
    d = next((x for x in reg["deposits"] if x.get("deposit_number") == n), None)
    if d is None: return [("EXIST", f"#{n} not in registry")]
    page = ROOT/f"s/records/{n}/index.html"
    if not page.exists(): return [("RENDERED-000", "no record page")]
    t = plain(page.read_text(encoding="utf-8", errors="replace"))
    f = []
    if d.get("axn") and d["axn"] not in t:
        f.append(("RENDERED-001", f"page does not show the registry AXN {d['axn']} "
                                 f"(stale render: the identifier a reader copies is wrong)"))
    if "[DEPOSIT]" in t and n != 885:
        f.append(("RENDERED-002", "issue-title prefix visible to readers"))
    for leak in ("full_text_path", "{title}", "{description}", "None", "PLACEHOLDER"):
        if leak in ("None",) and f" None " not in t: continue
        if leak in t and leak != "None":
            f.append(("RENDERED-003", f"unsubstituted template token rendered: {leak!r}"))
    desc = (d.get("description") or "")[:80]
    if desc and t.count(desc) > 1:
        f.append(("RENDERED-004", f"description rendered {t.count(desc)}x; it is metadata and belongs once"))
    for meta in ("Methodology", "Falsification Conditions"):
        if f"{meta} " in t and t.count(meta) > 2:
            f.append(("RENDERED-005", f"{meta} appears {t.count(meta)}x — metadata rendered as body?"))
    return f

if __name__ == "__main__":
    ns = [int(a) for a in sys.argv[1:]] or []
    if not ns:
        print(__doc__); sys.exit(2)
    bad = 0
    for n in ns:
        fails = check(n)
        if fails:
            bad += 1
            print(f"Record #{n}: {len(fails)} failure(s)\n")
            for c, m in fails: print(f"  [{c}] {m}")
        else:
            print(f"✓ Record #{n}: renders clean (axn, prefix, tokens, description, metadata)")
    sys.exit(1 if bad else 0)
