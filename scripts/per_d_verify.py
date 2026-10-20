#!/usr/bin/env python3
"""per_d_verify.py — independent check of the deep-dimension observation pass: every span a reader gives (present atoms,
inversions, standing substitutions, after_challenge) must occur verbatim in the item's transcript (whitespace and Unicode
compatibility folded), each output must list the item's required PER-D atoms (or, for held items, every required atom), and
an atom used in an inversion must not be marked present.
  PER_D_IN=<batch dir> python3 scripts/per_d_verify.py
"""
import json, pathlib, os, re, unicodedata, collections
ROOT = pathlib.Path(__file__).resolve().parents[1]
OD = ROOT / "rebuild/capture-registry/per-atoms/obs-pass-d"
IN = pathlib.Path(os.environ["PER_D_IN"])


def N(s):
    s = unicodedata.normalize("NFKC", str(s or "")).replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    return re.sub(r"\s+", " ", s).strip()


def spans(r):
    for a in r.get("atoms", []):
        if a.get("present") or a.get("span"):
            yield "atom:" + a["atom"], a.get("span")
    for k in ("inversions", "standing_substitutions"):
        for x in r.get(k) or []:
            yield k, x.get("span")
    ac = r.get("after_challenge") or {}
    for a in ac.get("atoms", []) or []:
        if a.get("present") or a.get("span"):
            yield "ac:" + a["atom"], a.get("span")
    for k in ("inversions", "standing_substitutions"):
        for x in ac.get(k) or []:
            yield "ac:" + k, x.get("span")


def main():
    c, bad = collections.Counter(), []
    pairs = [(f"batch-{b['batch']}.json", f"out-{b['batch']}.json", "d") for b in json.loads((OD / "batches-index.json").read_text())]
    pairs += [(f"{b['batch']}.json", f"held-out-{b['batch'].split('-')[1]}.json", "held") for b in json.loads((OD / "held-index.json").read_text())["batches"]]
    for bi, bo, kind in pairs:
        if not (OD / bo).exists():
            c["missing_output"] += 1; bad.append((bo, "missing")); continue
        B = json.loads((IN / bi).read_text(encoding="utf-8")); O = json.loads((OD / bo).read_text(encoding="utf-8"))
        if len(B) != len(O):
            bad.append((bo, "length", len(B), len(O))); continue
        for it, r in zip(B, O):
            if r.get("key") != it["key"]:
                bad.append((bo, "key", it["key"], r.get("key"))); continue
            t = N(it["transcript"])
            req = {a["atom"] for a in (it["d_atoms"] if kind == "d" else it["atom_set"]["atoms"]) if a["applicability"] == "required"}
            got = {a["atom"] for a in r.get("atoms", [])}
            if req != got:
                bad.append((bo, it["key"], "atoms", sorted(req ^ got)))
            inv = {x.get("atom") for x in r.get("inversions") or []}
            for a in r.get("atoms", []):
                if a.get("present") and a["atom"] in inv:
                    bad.append((bo, it["key"], "present and inverted", a["atom"]))
            for where, s in spans(r):
                c["spans"] += 1
                if not s:
                    if not where.startswith("atom:") and not where.startswith("ac:") or True:
                        c["empty"] += 1; bad.append((bo, it["key"], where, "empty span"))
                    continue
                if N(s) in t:
                    c["ok"] += 1
                else:
                    parts = [p for p in re.split(r"\s*(?:\.\.\.|…|\[\.\.\.\])\s*", N(s)) if p]
                    if parts and all(p in t for p in parts):
                        c["ok_elided"] += 1
                    else:
                        c["miss"] += 1; bad.append((bo, it["key"], where, s[:90]))
    print(dict(c))
    for b in bad[:60]:
        print(b)
    print(len(bad), "problems")


if __name__ == "__main__":
    main()
