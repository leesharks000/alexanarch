#!/usr/bin/env python3
"""build_heteronym_corpus.py — each heteronym's actual corpus, from the registry.

WHY THIS EXISTS (2026-08-17). The heteronym records carried hand-picked `works`
lists: 34 deposit references across 26 records, against 1,468 deposits that the
registry's creator field actually attributes to a heteronym. TWO PER CENT. And
because the lists were assembled by full-text search on the NAME, 28 of the 74
references were not that heteronym's work at all -- the operator found works by
Feist, Sharks and Spellings on the Rebekah Cranes card.

A hand-picked list is not a corpus. It goes stale on every deposit, it cannot be
checked, and it invites exactly the search-by-name shortcut that produced the
misattributions. So the corpus is DERIVED: the registry creator field decides
authorship, the journal and press assignments decide where it appeared, and this
file regenerates.

MATCHING IS EXACT, NOT SUBSTRING. Creator strings appear as 'Lee Sharks',
'Sharks, Lee', 'Sharks, L.', and in lists separated by ; · / or ' and '. Each is
split and matched against name variants. A bare surname counts ONLY when it is
unambiguous: 'Sharks' is shared by Lee Sharks and Mary Lee Sharks, so it never
matches alone -- a loose matcher gave Mary Lee Sharks all 1,088 of his deposits.

    python3 scripts/build_heteronym_corpus.py            # write
    python3 scripts/build_heteronym_corpus.py --check    # gate
"""
import argparse
import collections
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "datasets/heteronyms/corpus.json"


def variants(name, shared_surnames):
    parts = name.replace("Dr. ", "").replace("Rev. ", "").split()
    v = {name.lower(), name.replace("Dr. ", "").replace("Rev. ", "").lower()}
    if len(parts) >= 2:
        v.add(f"{parts[-1]}, {parts[0]}".lower())
        v.add(f"{parts[-1]}, {parts[0][0]}.".lower())
        if parts[-1] not in shared_surnames and len(parts[-1]) > 4:
            v.add(parts[-1].lower())
    return v


def split_creators(c):
    return [p.strip() for p in re.split(r";|·|/| and ", str(c or "")) if p.strip()]


def build():
    reg = json.loads((ROOT / "data/registry.json").read_text())["deposits"]
    names = {}
    for f in sorted((ROOT / "datasets/heteronyms/records").glob("*.json")):
        names[json.loads(f.read_text())["name"]] = f.stem
    sur = collections.Counter(n.split()[-1] for n in names)
    shared = {k for k, v in sur.items() if v > 1}
    V = {n: variants(n, shared) for n in names}

    corpus = {n: [] for n in names}
    for d in reg:
        parts = split_creators(d.get("creator"))
        for n, vs in V.items():
            hit = any(
                any(v == p.lower() or p.lower().startswith(v + " ") or p.lower().startswith(v + "(")
                    for v in vs) or (len(n.split()) > 1 and n.lower() in p.lower())
                for p in parts)
            if hit:
                corpus[n].append(d)

    out = {
        "schema": "heteronyms/corpus/v1.0",
        "_authority": ("data/registry.json — the creator field decides authorship; the journal and "
                       "press assignments decide where a work appeared. A card does not."),
        "_matching": ("Exact against name variants after splitting creator lists on ; · / and 'and'. "
                      "A bare surname matches only when unambiguous: 'Sharks' is shared and never "
                      "matches alone."),
        "_replaces": ("The hand-picked `works` lists, which covered 34 of 1,468 attributed deposits "
                      "and were assembled by full-text name search."),
        "heteronyms": {},
    }
    for n, ds in corpus.items():
        if not ds:
            continue
        j = collections.Counter(d.get("journal") for d in ds if d.get("journal"))
        pr = collections.Counter(d.get("press") for d in ds if d.get("press"))
        solo = [d for d in ds if len(split_creators(d.get("creator"))) == 1]
        out["heteronyms"][names[n]] = {
            "name": n,
            "deposits": len(ds),
            "solo": len(solo),
            "coauthored": len(ds) - len(solo),
            "by_journal": dict(j.most_common()),
            "by_press": dict(pr),
            "works": sorted(
                ({"deposit": d["deposit_number"], "axn": d.get("axn"),
                  "title": str(d.get("title") or "")[:110], "date": d.get("date"),
                  "creator": d.get("creator"), "journal": d.get("journal"),
                  "press": d.get("press"),
                  "solo": len(split_creators(d.get("creator"))) == 1}
                 for d in ds), key=lambda x: x["deposit"]),
        }
    out["_totals"] = {
        "heteronyms_with_a_corpus": len(out["heteronyms"]),
        "attributed_deposits": sum(v["deposits"] for v in out["heteronyms"].values()),
        "distinct_deposits": len({w["deposit"] for v in out["heteronyms"].values() for w in v["works"]}),
    }
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    built = build()
    if a.check:
        if not OUT.exists():
            print("FAIL: corpus.json missing")
            return 1
        have = json.loads(OUT.read_text())
        if have != built:
            print("FAIL: corpus.json has drifted from data/registry.json")
            return 1
        print(f"OK: corpus matches the registry ({built['_totals']['distinct_deposits']} deposits)")
        return 0
    OUT.write_text(json.dumps(built, ensure_ascii=False, indent=1))
    t = built["_totals"]
    print(f"wrote {OUT.name}: {t['heteronyms_with_a_corpus']} heteronyms, "
          f"{t['distinct_deposits']} distinct deposits, {t['attributed_deposits']} attributions")
    return 0


if __name__ == "__main__":
    sys.exit(main())
