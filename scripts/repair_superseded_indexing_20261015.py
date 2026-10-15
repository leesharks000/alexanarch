#!/usr/bin/env python3
"""repair_superseded_indexing_20261015.py — superseded records are indexable; only stubs are not.

Lee, 2026-10-15: "superseded records are allowed to be indexed. it was only a specific class of
unrecoverable metadata stubs that was to be no indexed."

retire.py (2026-08-10) applied one head layer to two populations: noindex + a canonical repointed
to the successor, to SUPERSEDED records and to NON-CITABLE metadata stubs alike. The ruling it
implemented ("retire the metadata stubs and fold the superceded records into most recent") retires
the stubs; folding the superseded records forward is the banner's work ("Cite instead"), not
de-indexing. Search Console (2026-10-09) reported 152 pages "Excluded by 'noindex' tag".

This repair, on the page layer retire.py wrote (record pages are not bulk re-rendered; the layer
is post-render, see build_record_api.py):
  - axn:retired = superseded: drop the robots noindex; canonical back to the record itself.
    The banner and the axn:retired marker stay: the page still says what supersedes it.
  - #1398 (EA-WG-CAPTURES-01 v7.0, a metadata_capture stub) lost its stub layer when #1676 was
    minted on 2026-10-12. The stub layer is restored, resolving to #1676, the current edition.
Registry: body_status.retired on each repaired record is updated to say what the page now does,
via record_modification.touch (a change to declared state).

    python3 scripts/repair_superseded_indexing_20261015.py --plan
    python3 scripts/repair_superseded_indexing_20261015.py --apply
"""
import json, pathlib, re, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import record_modification as rm
import retire

ROOT = pathlib.Path(__file__).resolve().parents[1]
REGP = ROOT / "data/registry.json"
ON = "2026-10-15"
RULING = ("superseded records are allowed to be indexed. it was only a specific class of "
          "unrecoverable metadata stubs that was to be no indexed")
NOTE_SUP = ("Superseded, not a stub: indexable (ruling 2026-10-15). The page carries a banner before "
            "the body naming the current version to cite, and an axn:retired marker; its canonical is "
            "its own URL. The URL is kept; the record is not deleted.")
ROBOTS = re.compile(r'<meta name="robots" content="noindex, follow">\n?')
CANON = re.compile(r'<link rel="canonical" href="[^"]*">')


def main():
    apply = "--apply" in sys.argv
    reg = json.loads(REGP.read_text())
    D = {d["deposit_number"]: d for d in reg["deposits"] if d.get("deposit_number")}
    sup, stub_fix = [], []
    for n, d in sorted(D.items()):
        p = ROOT / f"s/records/{n}/index.html"
        if not p.exists():
            continue
        s = p.read_text(errors="replace")
        if '<meta name="axn:retired" content="superseded">' in s and ROBOTS.search(s):
            sup.append(n)
            if apply:
                self_url = f"https://www.alexanarch.org/s/records/{n}/"
                s = ROBOTS.sub("", s, count=1)
                s = CANON.sub(f'<link rel="canonical" href="{self_url}">', s, count=1)
                p.write_text(s)
                r = (d.get("body_status") or {}).get("retired") or {}
                was = dict(r)
                r.update({"indexable": True, "note": NOTE_SUP,
                          "indexing_ruled": {"on": ON, "ruling": RULING}})
                d.setdefault("body_status", {})["retired"] = r
                rm.touch(d, "body_status", "superseded record made indexable; canonical self "
                         "(ruling 2026-10-15: only metadata stubs are noindex)",
                         was=was, now=r, when=ON)
    # #1398: stub whose layer was lost at the #1676 mint
    p = ROOT / "s/records/1398/index.html"
    if "axn:retired" not in p.read_text(errors="replace"):
        stub_fix.append(1398)
        if apply:
            d = D[1398]
            was = (d.get("body_status") or {}).get("retired")
            retire.apply(reg, D, {1398: {"kind": "stub", "target": 1676, "reason": ""}})
            r = d["body_status"]["retired"]
            r["declared"] = "2026-08-10"
            r["restored"] = {"on": ON, "why": "stub layer lost when #1676 was minted (2026-10-12); "
                             "restored, resolving to #1676, the current edition"}
            rm.touch(d, "body_status", "metadata stub's retirement layer restored (lost at #1676 mint)",
                     was=was, now=r, when=ON)
    print(f"  superseded pages made indexable: {len(sup)}  {sup[:12]}{' …' if len(sup) > 12 else ''}")
    print(f"  stub layers restored: {stub_fix}")
    if apply:
        REGP.write_text(json.dumps(reg, ensure_ascii=False, indent=1))  # the registry's own serialization
        print("  applied; registry updated")


if __name__ == "__main__":
    main()
