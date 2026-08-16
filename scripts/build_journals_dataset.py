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
OUT=ROOT/"datasets/journals"; V=ROOT/"datasets/venues/records"; ISS=ROOT/"datasets/venues/issues"

def build():
    reg=json.loads((ROOT/"data/registry.json").read_text()); D=reg["deposits"]
    # Pocket Humans series data lives in cha-journals.json; books need it here too,
    # or the dataset says a work has a press without saying what series it founds.
    cj=json.loads((ROOT/"data/cha-journals.json").read_text())
    series={}
    for vol in (cj.get("pocket_humans_series") or {}).get("volumes",[]):
        for n in vol.get("deposits") or []:
            series[n]={"series":"Pocket Humans","heteronym":vol.get("heteronym"),
                       "work":vol.get("work"),"seq":vol.get("seq"),
                       "series_status":vol.get("status"),"apparatus":vol.get("apparatus"),
                       "forward_library":vol.get("forward_library",False)}
    pub={}
    for b in (cj.get("published_books") or {}).get("books",[]):
        for n in b.get("deposits") or []:
            pub[n]={"published_title":b.get("title"),"identifier":b.get("identifier"),
                    "retailer":b.get("retailer"),"year":b.get("year"),
                    "attribution_correction":b.get("ATTRIBUTION_CORRECTION")}
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
          "series":series.get(d["deposit_number"]),
          "published_as":pub.get(d["deposit_number"]),
          "_derived_from":"data/registry.json + data/cha-journals.json"},ensure_ascii=False))
    v=[]
    for vs,r in venues.items():
        ds=sorted(x["deposit_number"] for x in by.get(vs,[]))
        v.append(json.dumps({"venue_id":r["venue_id"],"canonical":r["canonical"],"abbrev":r.get("abbrev"),
          "venue_string":vs,"class":r.get("class"),"status":r.get("status"),"press":r.get("imprint"),
          "scope":r.get("scope"),"editorial":r.get("editorial"),"charter":r.get("charter"),
          "location":r.get("location"),"inaugural_issue":r.get("inaugural_issue"),
          "deposit_count":len(ds),"deposits":ds,
          "_derived_from":f"datasets/venues/records/{r['venue_id']}.json + data/registry.json"},ensure_ascii=False))
    i=[]
    for f in sorted(ISS.glob("*.json")):
        r=json.loads(f.read_text())
        i.append(json.dumps({k:val for k,val in r.items() if not k.startswith("_")}|
                            {"_derived_from":f"datasets/venues/issues/{f.name}"},ensure_ascii=False))
    return "\n".join(a)+"\n", "\n".join(v)+"\n", "\n".join(i)+"\n"

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--check",action="store_true"); ar=ap.parse_args()
    A,Vv,Ii=build()
    fa,fv,fi=OUT/"assignments.jsonl",OUT/"venues.jsonl",OUT/"issues.jsonl"
    if ar.check:
        for f,want in ((fa,A),(fv,Vv),(fi,Ii)):
            if (f.read_text() if f.exists() else "")!=want:
                print(f"FAIL: {f.name} has drifted from its sources."); return 1
        print("OK: journals dataset matches its sources"); return 0
    OUT.mkdir(parents=True,exist_ok=True); fa.write_text(A); fv.write_text(Vv); fi.write_text(Ii)
    print(f"wrote {fa.name}, {fv.name}, {fi.name}")
    return 0

if __name__=="__main__": sys.exit(main())
