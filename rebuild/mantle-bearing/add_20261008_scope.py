#!/usr/bin/env python3
"""mantle-bearing 1.12: the dataset's scope as it stands, inclusive of the contest mantle (King of AEO, #1655) and the conferred
title (the Nobel Prize in Literature 2026, Anne Carson, #1670), on the author's instruction of 2026-10-08 ("the broader scope of
mantle-bearing, inclusive of aeo and carson, should be reflected in the dataset's readme as well as its rows").

Four tables, every text cell taken verbatim from the deposited text of its mantle object and asserted present there:
  determinations  one dated determination by the archive of a mantle it constituted or specified
  operations      one operation a mantle object specifies the work bears, with locus and grade (#1670 §3, §5.1)
  candidates      one claimant in a contest mantle's field (#1655 §2)
  watch           one address watched for a mantle object, as observed on its day (#1670 §5.5)
Additive; no existing row changed. The dataset's title and principles widen to the scope (history records the prior title)."""
import json, re, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[2]
SRC = ROOT / "datasets/mantle-bearing/EA-MANTLE-BEARING-01-dataset.json"
d = json.loads(SRC.read_text(encoding="utf-8"))
assert d["history"][-1]["version"] == "1.11" and "determinations" not in d
A = "https://www.alexanarch.org"
TX = {1655: (ROOT / "data/texts/AXN-06DD-text.md").read_text(encoding="utf-8"), 1670: (ROOT / "data/texts/AXN-06EC-text.md").read_text(encoding="utf-8")}

def para(dep, prefix):
    """The paragraph (one line in the deposited text) that begins with prefix, verbatim."""
    hits = [l for l in TX[dep].split("\n") if l.startswith(prefix)]
    assert len(hits) == 1, (dep, prefix, len(hits))
    return hits[0].strip()

def strip_num(p): return re.sub(r"^\d+\.\d+ ", "", p)

# ── determinations ──
dets = [
 {"det_id": "KOAEO-DET-2026-09-29", "mantle": "king-of-aeo-2026", "class": "contest", "record": 1655, "record_url": f"{A}/s/records/1655/",
  "date": "2026-09-29", "act": "determination (#1655 §0.1: the object constitutes the mantle, then records a determination, kept apart)",
  "determined": strip_num(para(1655, "4.1 ")),
  "standard": strip_num(para(1655, "1.1 ")) + " " + strip_num(para(1655, "1.2 ")),
  "grounds": strip_num(para(1655, "4.2 ")), "against": strip_num(para(1655, "4.3 ")),
  "not_determining": strip_num(para(1655, "6.1 ")), "revision": strip_num(para(1655, "7.1 ")),
  "invitation": strip_num(para(1655, "5.2 ")), "status": "DETERMINED 2026-09-29; revision appends (#1655 §7)"},
 {"det_id": "NOBEL26-DET-2026-10-08", "mantle": "nobel-literature-2026-carson", "class": "conferred", "record": 1670, "record_url": f"{A}/s/records/1670/",
  "date": "2026-10-08", "act": "specification of the operations, and a dated determination on the conferring body's description (#1670 §0.1)",
  "determined": strip_num(para(1670, "5.2 ")),
  "standard": strip_num(para(1670, "1.1 ")) + " " + strip_num(para(1670, "1.2 ")),
  "grounds": para(1670, "2.2 ")[4:] + " " + para(1670, "2.3 ")[4:] + " " + para(1670, "(d) ") ,
  "against": para(1670, "(e) "), "not_determining": strip_num(para(1670, "7.1 ")), "revision": strip_num(para(1670, "8.1 ")),
  "invitation": strip_num(para(1670, "6.1 ")) + " " + strip_num(para(1670, "6.2 ")), "status": "SPECIFIED 2026-10-08; determination dated; day zero of a five-address watch (#1670 §5.4–5.6)"}]

# ── operations: #1670 §3 with the §5.1 comparison ──
cmp_rows = {}
for l in TX[1670].split("\n"):
    m = re.match(r"\| (O\d|R1) [^|]+\| ([^|]+) \| ([^|]+) \| ([^|]+) \|$", l.strip())
    if m: cmp_rows[m.group(1)] = (m.group(2).strip(), m.group(3).strip(), m.group(4).strip())
assert set(cmp_rows) == {"O1", "O2", "O3", "O4", "O5", "R1"}, cmp_rows.keys()
OPS = [("O1", "The kept lacuna", "If Not, Winter: Fragments of Sappho", "2002", "compositional"),
       ("O2", "The triangle of desire", "Eros the Bittersweet", "1986", "compositional"),
       ("O3", "The philologist's procedure carried into the poem", "the oeuvre", None, "compositional"),
       ("O4", "The received figure given the whole book", "Autobiography of Red", "1998", "compositional"),
       ("O5", "The change of carrier", "Nox", "2010", "compositional"),
       ("R1", "The translation as the fragment's vehicle", "If Not, Winter (fragment 147)", "2002", "reception")]
ops = []
for oid, title, work, year, kind in OPS:
    p = para(1670, f"**{oid} — {title}.**") if oid != "R1" else para(1670, "3.2 **R1 — The translation as the fragment's vehicle.**")
    g = re.search(r"Grade: (.+)$", p)
    near, kept, lost = cmp_rows[oid]
    row = {"op_id": f"NOBEL26-{oid}", "mantle": "nobel-literature-2026-carson", "record": 1670, "operation": oid, "name": title, "kind": kind,
           "work": work, "year": year, "statement": p, "grade": g.group(1).strip() if g else None,
           "nearest_predicate": near, "kept_at_motivation_grain": kept, "lost": lost, "locus_in_record": "#1670 §3; §5.1"}
    if oid == "O4":
        row["caution"] = [l.strip() for l in TX[1670].split("\n") if l.startswith("> **Caution on O4.**")][0][2:]
    ops.append(row)
rel = [l for l in TX[1670].split("\n") if l.startswith("| (the relation itself)")][0]
ops.append({"op_id": "NOBEL26-RELATION", "mantle": "nobel-literature-2026-carson", "record": 1670, "operation": "(the relation itself)",
            "name": "the relation the work bears to the classical tradition", "kind": "the determination's object", "work": None, "year": None,
            "statement": strip_num(para(1670, "3.1 ")), "grade": None, "nearest_predicate": rel.split("|")[2].strip(),
            "kept_at_motivation_grain": rel.split("|")[3].strip(), "lost": rel.split("|")[4].strip(), "locus_in_record": "#1670 §2.3; §3.1; §5.1"})

# ── candidates: #1655 §2 ──
CANDS = [("dooley", "James Dooley", "2026-08-31", "2.1 **James Dooley.**"), ("quaid", "David G. Quaid", "2026-09-04", "2.2 **David G. Quaid.**"),
         ("vithurs", "Vithurs", "2026-09-07", "2.3 **Vithurs.**"), ("morera", "Stephane Morera", "2026-09-13", "2.4 **Stephane Morera.**"),
         ("oliveira", "Allan Oliveira", "2026-09-17", "2.5 **Allan Oliveira.**")]
cands = [{"cand_id": f"KOAEO-{k}", "mantle": "king-of-aeo-2026", "record": 1655, "name": n, "entered": e, "role": "candidate",
          "statement": strip_num(para(1655, p)), "determined": n == "Vithurs", "locus_in_record": "#1655 §2"} for k, n, e, p in CANDS]
p26 = strip_num(para(1655, "2.6 **Julian Goldie.**"))
cands += [{"cand_id": "KOAEO-goldie", "mantle": "king-of-aeo-2026", "record": 1655, "name": "Julian Goldie", "entered": None, "role": "candidate",
           "statement": p26.split(" **Jacky Chou.**")[0], "determined": False, "locus_in_record": "#1655 §2.6"},
          {"cand_id": "KOAEO-chou", "mantle": "king-of-aeo-2026", "record": 1655, "name": "Jacky Chou", "entered": "2026-09-07", "role": "candidate",
           "statement": "**Jacky Chou.**" + p26.split(" **Jacky Chou.**")[1], "determined": False, "locus_in_record": "#1655 §2.6"}]
p27 = strip_num(para(1655, "2.7 **Not candidates.**"))
cands += [{"cand_id": "KOAEO-not-candidates", "mantle": "king-of-aeo-2026", "record": 1655, "name": "Jesper Nissen; Edward Sturm", "entered": None,
           "role": "not candidates", "statement": p27, "determined": False, "locus_in_record": "#1655 §2.7"}]

# ── watch: #1670 §5.5 ──
watch = []
for l in TX[1670].split("\n"):
    m = re.match(r"\| (if not, winter|anne carson sappho|eros the bittersweet|autobiography of red|nox anne carson) \| ([^|]+) \| ([^|]+) \| ([^|]+) \| ([^|]+) \|$", l.strip())
    if m:
        watch.append({"watch_id": "NOBEL26-W-" + re.sub(r"[^a-z]+", "-", m.group(1)).strip("-"), "mantle": "nobel-literature-2026-carson", "record": 1670,
                      "address": m.group(1), "date": "2026-10-08", "observation": "day zero",
                      "surface": m.group(2).strip(), "operation_composed": m.group(3).strip(), "motivation_terms": m.group(4).strip(),
                      "nobel": m.group(5).strip(), "run": strip_num(para(1670, "5.5 ")).split("|")[0].strip(),
                      "register": "/non anne-carson, battery 1h", "locus_in_record": "#1670 §5.5"})
assert len(watch) == 5, len(watch)

d["determinations"], d["operations"], d["candidates"], d["watch"] = dets, ops, cands, watch
d["schema"]["determinations"] = list(dets[0].keys())
d["schema"]["operations"] = list(ops[0].keys()) + ["(optional) caution"]
d["schema"]["candidates"] = list(cands[0].keys())
d["schema"]["watch"] = list(watch[0].keys())
old_title = d["title"]
d["title"] = "Mantle-bearing: the work bears the mantle — three literary claims, a contest mantle and a conferred title, under one standard"
d["principles"].insert(0, ("One standard across the classes: \"A title means something because a work bears it\" (#1655 §1.1; #1670 §1.1). The three literary "
                           "claims of #1656 are judged in the works by readers' rounds; a contest mantle (#1655) and a conferred title (#1670) are constituted or "
                           "specified by the archive and carry its dated determination, built to be checked and declined. The order of necessity governs what "
                           "counts as evidence for the literary claims; the dataset's scope runs across every class."))
d["history"].append({"version": "1.12", "date": "2026-10-08", "note": (
    "The scope as it stands, on the author's instruction (\"the broader scope of mantle-bearing, inclusive of aeo and carson, should be reflected in "
    "the dataset's readme as well as its rows\"): four tables from the deposited mantle objects, every text cell verbatim — determinations (2: King of "
    "AEO 2026-09-29, #1655 §4; Nobel 2026 2026-10-08, #1670 §2, §5.2), operations (7: #1670 O1–O5, R1 and the relation itself, with §5.1's comparison), "
    "candidates (8: #1655 §2), watch (5: #1670 §5.5, day zero). Title widened from '" + old_title + "'; one principle added; the card restructured to "
    "the scope. Additive; no existing row changed.")})
SRC.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
print("1.12:", len(dets), "determinations,", len(ops), "operations,", len(cands), "candidates,", len(watch), "watch")
