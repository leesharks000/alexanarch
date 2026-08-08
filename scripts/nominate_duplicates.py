#!/usr/bin/env python3
"""nominate_duplicates.py - find capture records whose work may already be held in full.

ROUND 1 OF THE RESTORATION-STATE PASS. Scope: records that render a metadata-capture
state and carry NO forward pointer. The question for this round, and only this one:
does the full work already exist elsewhere in the archive?

THE DISCIPLINE, which is the whole point of the round:

    A SCORE NOMINATES. ONLY READING CONFIRMS.

On 2026-08-07 a strict-pairing pass matched #1346 to #629 at title overlap 0.67 and
declared it the complete version. The match was real and the label was wrong: #629 is
one of three sibling components of a combined deposit, and the component the title
actually names is #630. Siblings resemble each other - that is what makes them
siblings - so similarity cannot distinguish a fragment from a companion.

This script therefore emits EVIDENCE, not verdicts. For each nomination it prints
what a reader needs to decide: the words present in the capture's title and absent
from the candidate's (the strongest tell that the candidate is about something else),
the body sizes, and the record links. Nothing is written to the registry.

Usage:
    python3 scripts/nominate_duplicates.py                 # all unpointed captures
    python3 scripts/nominate_duplicates.py --limit 12      # first N
    python3 scripts/nominate_duplicates.py --md            # review sheet
"""
import argparse, html, json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
STOP = {"the", "and", "for", "with", "from", "that", "this", "not", "are", "was",
        "its", "their", "into", "onto", "than", "then", "when", "what", "which",
        "v10", "v11", "v20", "v01", "v02"}


def toks(t):
    return {w for w in re.findall(r"[a-z0-9]+", (t or "").lower())
            if len(w) > 2 and w not in STOP}


def rendered_state(n):
    p = ROOT / f"s/records/{n}/index.html"
    if not p.exists():
        return "", 0
    t = p.read_text(errors="replace")
    head = t[:t.find(">Full Text<")] if ">Full Text<" in t else t
    txt = html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", head)))
    body = len(t) - len(head)
    return txt, body


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--md", action="store_true")
    a = ap.parse_args()

    reg = json.loads((ROOT / "data/registry.json").read_text())["deposits"]
    D = {d["deposit_number"]: d for d in reg}
    unpointed = json.loads(pathlib.Path("/tmp/unpointed.json").read_text())
    if a.limit:
        unpointed = unpointed[:a.limit]

    def bodylen(n):
        fp = (D.get(n) or {}).get("full_text_path")
        if not fp:
            return 0
        p = ROOT / fp.lstrip("/")
        return len(p.read_text(errors="replace")) if p.exists() else 0

    rows = []
    for n in unpointed:
        d = D.get(n)
        if not d:
            continue
        ct = toks(d.get("title"))
        if not ct:
            continue
        cands = []
        for o in reg:
            m = o["deposit_number"]
            if m == n:
                continue
            ot = toks(o.get("title"))
            if not ot:
                continue
            shared = ct & ot
            if len(shared) < 3:
                continue
            jac = len(shared) / len(ct | ot)
            cov = len(shared) / len(ct)          # how much of the capture the candidate covers
            if cov < 0.55:
                continue
            cands.append({
                "n": m, "title": o.get("title", ""),
                "cov": round(cov, 2), "jac": round(jac, 2),
                "only_in_capture": sorted(ct - ot)[:6],
                "only_in_candidate": sorted(ot - ct)[:6],
                "body": bodylen(m),
            })
        if not cands:
            continue
        cands.sort(key=lambda c: (-c["cov"], -c["body"]))
        rows.append({"n": n, "title": d.get("title", ""), "axn": d.get("axn", ""),
                     "body": bodylen(n), "cands": cands[:3]})

    if a.md:
        out = ["# Round 1 - duplicate nominations", "",
               f"**{len(rows)} of {len(unpointed)} unpointed capture records have a plausible "
               "full-text candidate.** Nothing below is a finding. Each is a pair to be read.",
               "",
               "The decisive field is **in capture, not in candidate**: words the capture's "
               "title carries and the candidate's does not name something the candidate may "
               "not be about. On #1346 that field read *derived, from, luke* and the pairing "
               "was wrong.", ""]
        for r in rows:
            out += [f"## #{r['n']} - {r['title'][:96]}",
                    f"`{r['axn']}` - capture body {r['body']:,}c - "
                    f"https://www.alexanarch.org/s/records/{r['n']}/", ""]
            for c in r["cands"]:
                flag = "*" if c["only_in_capture"] else " "
                out += [f"- {flag} **#{c['n']}** cov {c['cov']} - body {c['body']:,}c - "
                        f"{c['title'][:78]}",
                        f"  - in capture, not in candidate: "
                        f"`{', '.join(c['only_in_capture']) or '-'}`",
                        f"  - read: https://www.alexanarch.org/s/records/{c['n']}/"]
            out.append("")
        print("\n".join(out))
    else:
        print(f"{len(rows)} of {len(unpointed)} unpointed captures have a candidate\n")
        for r in rows:
            print(f"#{r['n']:>5} {r['title'][:52]}")
            for c in r["cands"]:
                print(f"      -> #{c['n']:>5} cov {c['cov']} body {c['body']:>7,}c  "
                      f"gap: {', '.join(c['only_in_capture'])[:44] or '-'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
