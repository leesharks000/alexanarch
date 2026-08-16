#!/usr/bin/env python3
"""build_journals_dataset.py — project registry + venue records into datasets/journals.

CANONICAL: datasets/venues/records/*.json (venue definitions) and data/registry.json
(per-deposit assignment). PROJECTION: datasets/journals/*.jsonl.

Same architecture as the heteronym substrate: a layer that looks like data says whether
it is data. Every row carries _derived_from.

Usage: build_journals_dataset.py [--check]
"""
import json, sys, pathlib, collections, argparse
ROOT=pathlib.Path(__file__).resolve().parent.parent
OUT=ROOT/"datasets/journals"; V=ROOT/"datasets/venues/records"

def build():
    reg=json.loads((ROOT/"data/registry.json").read_text()); D=reg["deposits"]
    venues={}
    for p in sorted(V.glob("*.json")):
        r=json.loads(p.read_text()); venues[r["venue_string"]]=r
    by=collections.defaultdict(list)
    for d in D: by[d.get("journal")].append(d)
    a=[]
    for d in sorted(D,key=lambda x:x["deposit_number"]):
        ja=d.get("journal_assignment") or {}
        a.append(json.dumps({"deposit":d["deposit_number"],"axn":d.get("axn"),"hex":d.get("hex"),
          "title":d.get("title"),"content_type":d.get("content_type"),"creator":d.get("creator"),
          "journal":d.get("journal"),"journal_secondary":d.get("journal_secondary"),"press":d.get("press"),
          "assigned":ja.get("assigned"),"pass":ja.get("pass"),"previous":ja.get("previous"),
          "record":f"https://alexanarch.org/s/records/{d['deposit_number']}/",
          "_derived_from":"data/registry.json"},ensure_ascii=False))
    v=[]
    for vs,r in venues.items():
        ds=sorted(x["deposit_number"] for x in by.get(vs,[]))
        v.append(json.dumps({"venue_id":r["venue_id"],"canonical":r["canonical"],"abbrev":r.get("abbrev"),
          "venue_string":vs,"class":r.get("class"),"status":r.get("status"),"press":r.get("imprint"),
          "scope":r.get("scope"),"editorial":r.get("editorial"),"charter":r.get("charter"),
          "location":r.get("location"),"inaugural_issue":r.get("inaugural_issue"),
          "deposit_count":len(ds),"deposits":ds,
          "_derived_from":f"datasets/venues/records/{r['venue_id']}.json + data/registry.json"},ensure_ascii=False))
    return "\n".join(a)+"\n", "\n".join(v)+"\n"

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--check",action="store_true"); ar=ap.parse_args()
    A,Vv=build()
    fa,fv=OUT/"assignments.jsonl",OUT/"venues.jsonl"
    if ar.check:
        if (fa.read_text() if fa.exists() else "")!=A or (fv.read_text() if fv.exists() else "")!=Vv:
            print("FAIL: datasets/journals has drifted from registry + venue records."); return 1
        print("OK: journals dataset matches its sources"); return 0
    OUT.mkdir(parents=True,exist_ok=True); fa.write_text(A); fv.write_text(Vv)
    print(f"wrote {fa.name} and {fv.name}")
    return 0

if __name__=="__main__": sys.exit(main())
