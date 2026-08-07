#!/usr/bin/env python3
"""audit_capture_pairings.py — a pairing score cannot tell a sibling from a parent.

WHY THIS EXISTS
On 2026-08-04 a strict-pairing pass linked semi-restored metadata captures to the
complete works held elsewhere in the archive, matching on title overlap and a
content probe. It was a good pass and it closed a real defect — hundreds of
records pointing nowhere when the work existed.

But on 2026-08-07 MANUS found #1346 pointing at the wrong Caesura. That record
captures a COMBINED Zenodo deposit whose own description states it is a
three-document fulfillment pair. The pass matched it to one of the three at title
overlap 0.67 and declared that its complete version. The match was real. The
label was wrong.

**Siblings resemble each other — that is what makes them siblings.** A similarity
score therefore cannot distinguish:

    this capture IS a fragment of that complete work      (correct pairing)
    this capture is a COMPANION to that work              (sibling mislabelled)
    this capture is one part of a COMBINED deposit        (parent mislabelled)

The lower the title overlap, the more likely the target is a relative rather than
the work itself. This script ranks every pairing by that suspicion so each can be
read by a human, which is the only thing that can actually settle it.

Usage:  python3 scripts/audit_capture_pairings.py [--md]
"""
import json, re, sys, pathlib, argparse

ROOT = pathlib.Path(__file__).resolve().parents[1]
REG = ROOT / "data/registry.json"


def tokens(t):
    return {w for w in re.findall(r"[a-z0-9]+", (t or "").lower()) if len(w) > 2}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--md", action="store_true", help="emit a markdown review sheet")
    a = ap.parse_args()

    reg = json.loads(REG.read_text())["deposits"]
    D = {d["deposit_number"]: d for d in reg}
    rows = []

    for d in reg:
        bs = d.get("body_status") or {}
        fv = bs.get("full_version")
        if not isinstance(fv, dict):
            continue
        tgt = fv.get("deposit_number")
        basis = fv.get("basis", "")
        ov = re.search(r"title overlap ([\d.]+)", basis)
        pr = re.search(r"content probe ([\d.]+)", basis)
        sz = re.search(r"full body ([\d,]+)c vs capture ([\d,]+)c", basis)
        t = D.get(tgt) or {}

        a_tok, b_tok = tokens(d.get("title")), tokens(t.get("title"))
        shared = a_tok & b_tok
        only_capture = a_tok - b_tok
        only_target = b_tok - a_tok

        # A capture is a FRAGMENT of its target: the target's title should contain
        # most of the capture's distinctive words. Words the capture has and the
        # target lacks are the tell — they name something the target is not about.
        rows.append({
            "n": d["deposit_number"], "axn": d.get("axn", ""),
            "title": d.get("title", ""), "target": tgt,
            "target_title": t.get("title", ""),
            "overlap": float(ov.group(1)) if ov else None,
            "probe": float(pr.group(1)) if pr else None,
            "full_c": int(sz.group(1).replace(",", "")) if sz else None,
            "cap_c": int(sz.group(2).replace(",", "")) if sz else None,
            "unmatched_in_capture": sorted(only_capture)[:6],
            "unmatched_in_target": sorted(only_target)[:6],
        })

    for r in rows:
        risk = 0
        if (r["overlap"] or 1) < 0.70: risk += 2
        elif (r["overlap"] or 1) < 0.80: risk += 1
        if len(r["unmatched_in_capture"]) >= 3: risk += 2
        elif len(r["unmatched_in_capture"]) >= 1: risk += 1
        if r["full_c"] and r["cap_c"] and r["full_c"] < r["cap_c"] * 1.5: risk += 1
        r["risk"] = risk
    rows.sort(key=lambda r: (-r["risk"], r["overlap"] or 1))

    if a.md:
        out = ["# Capture pairings — sibling review sheet", "",
               f"**{len(rows)} paired records.** Ranked by the likelihood that the target is a "
               "relative rather than the work itself.", "",
               "A capture should be a FRAGMENT of its target. Words present in the capture's "
               "title and absent from the target's are the strongest tell: they name something "
               "the target is not about. Confirmed wrong so far: **#1346**.", ""]
        for r in rows:
            flag = "🔴" if r["risk"] >= 4 else ("🟠" if r["risk"] >= 2 else "🟢")
            out += [f"## {flag} #{r['n']} → #{r['target']}  ·  risk {r['risk']}",
                    f"- **capture:** {r['title'][:110]}",
                    f"- **target :** {r['target_title'][:110]}",
                    f"- overlap {r['overlap']} · probe {r['probe']} · "
                    f"target {r['full_c']:,}c vs capture {r['cap_c']:,}c"
                    if r["full_c"] else f"- overlap {r['overlap']} · probe {r['probe']}",
                    f"- **in capture, not in target:** {', '.join(r['unmatched_in_capture']) or '—'}",
                    f"- in target, not in capture: {', '.join(r['unmatched_in_target']) or '—'}",
                    f"- read: https://www.alexanarch.org/s/records/{r['n']}/ · "
                    f"https://www.alexanarch.org/s/records/{r['target']}/", ""]
        print("\n".join(out))
    else:
        print(f"{len(rows)} paired records · ranked by sibling risk\n")
        print(f"{'risk':<5}{'record':<8}{'→ target':<10}{'ovl':<6}{'in capture not in target'}")
        for r in rows:
            print(f"{r['risk']:<5}#{r['n']:<7}#{r['target']:<9}{str(r['overlap']):<6}"
                  f"{', '.join(r['unmatched_in_capture'])[:52]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
