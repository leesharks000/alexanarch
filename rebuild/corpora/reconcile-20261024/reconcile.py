#!/usr/bin/env python3
"""Reconcile the two EA-CORPORA indexes after the twentieth to twenty-second seatings (2026-10-24).

What was broken, and the evidence (2026-10-24):
  - datasets/corpora/corpora.json (the manifest the Hugging Face `corpora` config is built from) held 83 seats and
    was last generated 2026-10-18; the seatings of 20, 21 and 22 (#1698-#1700) entered data/api/corpora.json and
    never this file, so the Hub served 83 rows while 97 seats are on disk.
  - data/api/corpora.json carried `seats: 93` and `lines_total: 2627851` while its `corpora` array holds 97 objects
    whose lines sum to 2633059; `count` was 97.
  - the Enoch seat gained its Beta masahft text layer in EA-CORPORA-20; its manifest row still carried the earlier
    file count, bytes, MANIFEST digest and licence class.
This writes the missing rows in the form of rebuild/corpora/ea-corpora-19/index_seats.py, re-derives the Enoch row,
recomputes every count from the rows, and sets the index's header from its own array. No seat is changed.
Licence class follows the indexer's rule, most restrictive packaging first: a seat that redistributes CC BY-SA
packaging (Wikisource, Perseus, Beta masahft, the TLA) is cc-by-sa; Project Gutenberg next; otherwise public domain."""
import json, hashlib, pathlib, datetime, collections

ROOT = pathlib.Path(__file__).resolve().parents[3]
I = ROOT / "data/api/corpora.json"; d = json.loads(I.read_text(encoding="utf-8"))
M = ROOT / "datasets/corpora/corpora.json"; m = json.loads(M.read_text(encoding="utf-8"))
now = datetime.datetime.now(datetime.timezone.utc)
NEW = ["ethiopic-canon", "kebra-nagast", "second-temple-pseudepigrapha", "euclid", "maya-codices", "popol-vuh",
       "maya-colonial-texts", "florentine-codex", "book-of-the-dead", "earlier-egyptian", "corpus-hermeticum",
       "mesopotamian-epics", "avesta", "rig-veda", "ethiopic-enoch"]


def lclass(s):
    pay = s["license"]["payload"] if isinstance(s["license"], dict) else str(s["license"])
    carried = pay + " " + str(s.get("scope", "")) + " " + str(s.get("text_layer", ""))  # a text layer added later (Enoch) carries its own packaging
    kinds = " ".join(str(i.get("source", "")) if isinstance(i, dict) else str(i) for i in s["origin"]["items"])
    if "CC BY-SA" in carried or "Wikisource" in kinds:
        return "cc-by-sa"
    if "Gutenberg" in kinds:
        return "gutenberg"
    return "public-domain"


def row(name):
    seat = ROOT / "data/corpora" / name
    s = json.loads((seat / "source.json").read_text(encoding="utf-8"))
    files = [p for p in seat.rglob("*") if p.is_file()]
    lic = s["license"]["payload"] if isinstance(s["license"], dict) else str(s["license"])
    works = s.get("works") or {}
    return {
        "corpus": name, "seat": s["seat"], "title": s.get("title", name), "edition": s["edition"],
        "origin": json.dumps(s["origin"], ensure_ascii=False), "language": s["language"],
        "license_verbatim": lic, "license_class": lclass(s), "fetched": s.get("fetched", ""),
        "normalization": s.get("normalization", ""), "scope": s.get("scope", ""), "status": "seated",
        "verified_loci": json.dumps(s.get("verified_loci", []), ensure_ascii=False),
        "works": json.dumps({"count": works.get("count"), "units": works.get("units")}, ensure_ascii=False),
        "why_seated": s.get("why_seated", ""),
        "manifest_sha256": hashlib.sha256((seat / "MANIFEST.sha256").read_bytes()).hexdigest(),
        "file_count": len(files), "bytes": sum(p.stat().st_size for p in files)}


# Existing rows keep their place (the Enoch row is re-derived where it stands); the new seats follow in seating order.
rows = [row(x["corpus"]) if x["corpus"] in NEW else x for x in m["seats"]]
rows += [row(n) for n in NEW if n not in {x["corpus"] for x in m["seats"]}]
assert sorted(x["corpus"] for x in rows) == sorted(c["corpus"] for c in d["corpora"]), "manifest and index disagree on membership"
m["seats"] = rows
m["counts"] = {"seats": len(rows), "files": sum(x["file_count"] for x in rows), "bytes": sum(x["bytes"] for x in rows),
               "with_manifest_sha": sum(1 for x in rows if x["manifest_sha256"]),
               "with_verified_loci": sum(1 for x in rows if x["verified_loci"] not in ("", "[]"))}
m["by_license_class"] = dict(collections.Counter(x["license_class"] for x in rows))
m["generated"] = now.date().isoformat()
d["seats"] = d["count"] = len(d["corpora"])
d["lines_total"] = sum(c.get("lines") or 0 for c in d["corpora"])
d["_generated"] = now.isoformat().replace("+00:00", "Z")
I.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
M.write_text(json.dumps(m, ensure_ascii=False, indent=1), encoding="utf-8")
print("index:", d["seats"], "seats,", d["lines_total"], "lines · manifest:", m["counts"], m["by_license_class"])
