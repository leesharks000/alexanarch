#!/usr/bin/env python3
"""resolve_doi_axn.py — DOI to AXN, from the resolver, verified against the registry.

WHY THIS EXISTS. Asked to put AXNs beside the DOIs in pessoagraph, I opened
data/doi-resolution-index.json, saw @context and @type at the top, assumed it was
a schema.org wrapper with no payload, and fell back to SCANNING EVERY DEPOSIT FOR
DOI STRINGS. That attaches the AXN of any deposit that MENTIONS a DOI rather than
the one the DOI belongs to. 28 of 32 were wrong, and they shipped.

The resolver holds 1,935 mappings, 1,926 with an AXN. It is the purpose-built
index and should have been the first thing read.

BUT IT IS NOT SELF-SUFFICIENT EITHER. Its own authority block says:

    "DATED — NOT A SOURCE OF TRUTH FOR RECORD IDENTITY" (MANUS, 2026-08-10)
    "Where the index and a record disagree, THE ALEXANARCH RECORD IS AUTHORITATIVE."

So this resolves from the index and then CONTENT-MATCHES the title against the
registry, per the standing rule that HTTP 200 is not verification. On the
pessoagraph pass that caught three DOIs collapsing onto one AXN with unrelated
titles — the index's own `membership_rejected_collision` category, visible only
because the titles were compared.

    python3 scripts/resolve_doi_axn.py 10.5281/zenodo.20343987 [...]
    python3 scripts/resolve_doi_axn.py --file path/with/dois
"""
import difflib
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]


def norm(s):
    return re.sub(r"[^a-z0-9 ]", " ", str(s).lower())


def load():
    idx = json.loads((ROOT / "data/doi-resolution-index.json").read_text())
    res = {m["dead_doi"]: m for m in idx["mappings"]}
    reg = {d["axn"]: d for d in json.loads((ROOT / "data/registry.json").read_text())["deposits"]
           if d.get("axn")}
    return res, reg


def resolve(doi, res, reg, threshold=0.55):
    """Returns (axn, deposit, confidence) or (None, None, reason)."""
    m = res.get(doi)
    if not m:
        return None, None, "not in the resolver"
    ax = m.get("axn")
    if not ax:
        return None, None, f"resolver has no AXN (mapping_type={m.get('mapping_type')})"
    dep = reg.get(ax)
    if not dep:
        return None, None, f"resolver gives {ax}, which is not in the registry"
    r = difflib.SequenceMatcher(None, norm(m.get("title"))[:110],
                                norm(dep.get("title"))[:110]).ratio()
    if r < threshold:
        return None, None, (f"TITLE MISMATCH ({r:.2f}) — index says "
                            f"{norm(m.get('title'))[:44]!r}, registry says "
                            f"{norm(dep.get('title'))[:44]!r}")
    return ax, dep.get("deposit_number"), round(r, 2)


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return 0
    if args[0] == "--file":
        dois = sorted(set(re.findall(r"10\.\d{4,}/[^\s\"'<>,)]+",
                                     pathlib.Path(args[1]).read_text(errors="replace"))))
    else:
        dois = args
    res, reg = load()
    good = 0
    for d in dois:
        ax, dep, why = resolve(d, res, reg)
        if ax:
            good += 1
            print(f"  {d:<32}#{dep:<6}{ax}   (title match {why})")
        else:
            print(f"  {d:<32}UNRESOLVED — {why}")
    print(f"\n{good}/{len(dois)} verified. An unresolved DOI is left BARE, never guessed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
