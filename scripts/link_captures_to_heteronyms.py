#!/usr/bin/env python3
"""link_captures_to_heteronyms.py — wire capture intake to the Dodecad dataset.

THE WIRING RULE (MANUS, 2026-08-15): "wire up capture intake to the heteronyms
dataset now." A capture whose composition concerns a heteronym belongs on that
heteronym's reception record, and the link must be COMPUTED, not remembered —
three of the archive's own findings sat unassembled in three papers because
linkage lived in memory instead of in a script.

Idempotent and rerunnable: scans every registry entry, matches heteronym names
(and an explicit `heteronym` field where the entry carries one), and rewrites
each heteronym's reception_captures from scratch. Run it after every seating.
"""
import json, pathlib, re, sys, datetime

ROOT = pathlib.Path(__file__).resolve().parents[1]

def main():
    reg = json.loads((ROOT / "data/EA-WG-CAPTURES-01.json").read_text())
    dp = ROOT / "data/dodecad.json"
    dd = json.loads(dp.read_text())
    for h in dd["heteronyms"]:
        name = h["name"]
        pats = [re.escape(name)]
        if name.startswith("Dr. "):
            pats.append(re.escape(name[4:]))
        pat = re.compile("|".join(pats), re.I)
        hits = []
        for e in reg["entries"]:
            # subject match: case-insensitive, honorific-stripped, suffix-tolerant
            # (entries store the name as issued in the query: "johannes sigil",
            #  "Sparrow Wells, Patacinematics")
            canon = name.replace("Dr. ", "").strip().lower()
            ent = str(e.get("heteronym") or "").replace("Dr. ", "").strip().lower()
            subj = bool(ent) and (ent == canon or ent.startswith(canon + ",") or ent.startswith(canon + " "))
            hay = " ".join(str(e.get(k) or "") for k in ("q", "slug", "d", "transcript"))
            if not subj and not pat.search(hay):
                continue
            rel = ((e.get("composed_as") or {}).get("binding_relation") or "")
            # NOTE the substring trap: "UNBOUND" contains "BOUND". Prefix test only.
            bound = (rel.startswith("BOUND") if (subj and rel) else None)
            hits.append({"slug": e["slug"], "date": e.get("date"), "surface": e.get("surface"),
                         "per": e.get("per") if subj else None,
                         "relation": "subject" if subj else "mention",
                         "bound": bound})
        h["reception_captures"] = sorted(hits, key=lambda x: (str(x["date"]), x["slug"]))
    dd["updated"] = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    dp.write_text(json.dumps(dd, indent=1, ensure_ascii=False), encoding="utf-8")
    print("heteronym            captures  bound/unbound (where scored)")
    for h in dd["heteronyms"]:
        rc = h["reception_captures"]
        s = sum(1 for x in rc if x["relation"]=="subject"); b = sum(1 for x in rc if x["bound"] is True); u = sum(1 for x in rc if x["bound"] is False)
        print(f"  {h['name']:<19} {len(rc):>3}   subj {s:>2}   {b}B/{u}U")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
