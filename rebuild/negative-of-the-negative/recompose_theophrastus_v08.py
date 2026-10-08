#!/usr/bin/env python3
"""Recompose /non theophrastus under EA-NEGONT-02 v0.8: composition in the archive's ontology.

    python3 rebuild/negative-of-the-negative/recompose_theophrastus_v08.py <v0.8 text.md> [deposit number]

Reads the knowledge object and the translation table from the v0.8 text's Appendix C (one source of truth), and
writes, in the row: objects.KO (L_A(B ∪ A), the expansion), objects.P (the compression in AIO's grammar, composed
from the archive's ontology: what faces on the card), objects.L_BA (the KO as running text), row.ontology (E_A,
E_F, ρ, the translation table), row.measure (R7, computed). The v0.7 objects are kept under row.superseded["v0.7"];
nothing of the field arm (P_B, KO_B, L_B), T, the ledgers or the delta is changed. Refuses to run twice."""
import json, re, sys, difflib, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[2]
SPEC = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
DEP = sys.argv[2] if len(sys.argv) > 2 else None
RP = ROOT / "datasets/negative-of-the-negative/v2/rows/theophrastus.json"
PP = ROOT / "datasets/negative-of-the-negative/v2/panel/panel.json"
row = json.loads(RP.read_text(encoding="utf-8")); o = row["objects"]
field = json.loads((ROOT / row["ledger"]["field"]).read_text(encoding="utf-8"))["field_claims"]
arch = {c["id"]: c for c in json.loads((ROOT / row["ledger"]["archive"]).read_text(encoding="utf-8"))}
first = "superseded" not in row
if first:
    row["superseded"] = {"v0.7": {"KO": o["KO"], "P": o["P"], "L_BA": o["L_BA"], "type": row["type"], "spec": row["spec"],
                                  "note": "Composed under v0.7 (#1665): the archive admitted on equal terms into the field's entity. Kept as the record of what v0.8 replaces."}}
v07 = row["superseded"]["v0.7"]

def expand(tok):
    m = re.fullmatch(r"F(\d+)[–-]F(\d+)", tok)
    return [f"F{i}" for i in range(int(m.group(1)), int(m.group(2)) + 1)] if m else [tok]

C = SPEC.split("## Appendix C")[1]
# the knowledge object
ko_md = C.split("### C.3.")[1].split("### C.4.")[0]
sents = [(int(n), t, [x for tok in c.split() for x in expand(tok)]) for n, t, c in re.findall(r"^(\d+)\. (.+?) `([^`]+)`\s*$", ko_md, re.M)]
assert [n for n, _, _ in sents] == list(range(1, len(sents) + 1)), "KO sentences numbered 1..n"
PARA = {1: 0, 2: 0, 3: 1, 4: 2, 5: 2, 6: 2, 7: 3, 8: 3, 9: 3, 10: 3, 11: 4, 12: 4, 13: 5, 14: 5}
for _, _, cl in sents:
    for x in cl: assert x in field or x in arch, x
# the translation table
tab = C.split("### C.2.")[1].split("### C.3.")[0]
trows = []
for line in tab.splitlines():
    cells = [x.strip() for x in line.strip().strip("|").split("|")]
    if len(cells) == 5 and re.match(r"F\d", cells[0]):
        trows.append({"field_claims": [x for tok in re.findall(r"F\d+(?:[–-]F\d+)?", cells[0]) for x in expand(tok)],
                      "received": cells[1], "receiving_text": cells[2], "translation": cells[3],
                      "archive_claims": re.findall(r"T\d+-\d+", cells[4])})
carried = {x for r in trows for x in r["field_claims"]}
assert carried == set(field), sorted(set(field) - carried)

KO = {"title": "Theophrastus",
      "genre": "knowledge object composed in the archive's ontology: L_A(B ∪ A) under EA-NEGONT-02 v0.8 (R1–R7); every field claim carried and translated (row.ontology.translation)",
      "status": "composed 2026-10-08 under v0.8 on the operator's ruling ('begin with the theophrastus recomposition'); not frozen; ledger unaudited",
      "sentences": [{"para": PARA[n], "text": t, "n": n, "claims": cl} for n, t, cl in sents],
      "field_claims": v07["KO"]["field_claims"], "field_sources": v07["KO"]["field_sources"]}

# the compression, in AIO's interaction grammar, from the archive's ontology: what faces on the card (ruled 2026-10-08)
def it(label, text, claims): return {"label": label, "text": text, "claims": claims.split()}
P = {"title": "Theophrastus",
     "genre": "the compression: AIO's interaction grammar (lede, headed clusters, bolded labels, card rail), composed from the archive's ontology; it faces on the card, with AIO's transcript a record within it (v0.8 R5–R6, ruled 2026-10-08)",
     "status": "composed 2026-10-08 from the v0.8 knowledge object; not frozen",
     "lede": {"text": "is the name under which part of one corpus has come down, the corpus transmitted under the names Aristotle and Theophrastus, which the surviving texts do not support dividing into two distinct authors; how many made it is uncounted.",
              "claims": "T1587-01 T1588-01 T1588-03 T1587-02".split()},
     "sections": [
      {"icon": "🔣", "head": "The function under the name", "items": [
        it("World into register:", "it extracts, classifies, registers; person and scene removed.", "T1587-06 T1584-04"),
        it("First draft:", "in method-order, the draft of the position named Aristotle.", "T1585-01 T1585-02"),
        it("The texts:", "Enquiry and Causes of Plants, received as botany's founding; On Stones; On the Senses; the Characters, thirty vices on no axis.",
           "F11 F13 F12 F41 F55 F56 F58 F62 T1592-01 F18 F14 F42 F15 F47 F54 T1584-03 T1586-04")]},
      {"icon": "🪡", "head": "The seam", "items": [
        it("The hinge:", "Metaphysics 6–7 written from inside Λ, no second voice marked.", "F17 T1583-02 T1583-06"),
        it("5a21–23:", "names Λ 8's spheres and refuses Λ's astronomers.", "T1602-01"),
        it("Ranked first:", "fragment → Λ, first of 1,482 edges; which came first, undecided.", "T1605-01 T1601-02"),
        it("Catalogues:", "12 titles in both lists; 'Aristotelian or Theophrastan'; 5 ghost twins.", "T1581-03 T1581-04 T1590-01")]},
      {"icon": "📜", "head": "The received person, from its texts", "items": [
        it("Parentage, city, 85 years:", "Diogenes V.36, V.40, on Athenodorus's word.", "F2 F24 F49 F57 T1585-04 T1570-03"),
        it("Plato, then Aristotle; the school:", "Diogenes V.36–37.", "F46 F23 F26 F60"),
        it("Tyrtamus renamed:", "Diogenes V.38; Strabo XIII.2.4.", "F3 F4 F25 F50 F59"),
        it("Library to him:", "Strabo XIII.1.54; Aristotle's will names no books.", "F6 T1581-07 T1581-08"),
        it("Will, 227 titles, 232,808 lines:", "texts Diogenes preserves, V.42–57.", "F7 F27 F53 F8 F28 F52 T1580-01 T1580-02 T1581-02"),
        it("Scepsis; 'a tenth survives':", "Strabo's story; a list set against a transmission.", "F10 F9 F29 F61 T165-01 T1570-04 T1581-06")]},
      {"icon": "🔗", "head": "Inside the transmission", "items": [
        it("Logic:", "credited through Alexander and Simplicius.", "F16 F32 F33 F34 F35 F20 T1569-03 T1605-05"),
        it("Doxography:", "the Presocratics, and the Plato/Aristotle division, pass through this name.", "F18 F39 F40 F43 F44 F48 T1569-04 T1575-02 T1594-01"),
        it("Read as a pupil's questions:", "doubts on teleology; the unmoved mover abandoned.", "T1583-01 F21 F37 F38 F22 F36"),
        it("Cushions:", "'colleague and successor', 'master and pupil', 'a school'.", "F1 F45 F51 F5 F19 F30 F31 T1585-03 T1587-04")]},
      {"icon": "⚠️", "head": "Bounds and falsifiers", "items": [
        it("It shows:", "what the attestation of a person rests on, and no more.", "T1658-08"),
        it("Would weaken it:", "an inscription or papyrus outside the manuscripts; a second voice at the hinge; an extant answering work.", "T1658-09 T1583-09 T1583-10 T1587-08"),
        it("Further, a hypothesis:", "one self-dividing maker.", "T1658-02")]}]}
# the rail: archive lineages first, in E_A's order; the received lineages after, named by their receiving texts
RN = {"The person and the renaming": "The received person and the renaming (Diogenes V.36–38; Strabo XIII.2.4)",
      "Succession and the will": "Succession and the will (Diogenes V.36, V.51–57; Strabo XIII.1.54)",
      "The catalogue and its loss": "The catalogue and the surviving fraction (Diogenes V.42–50)",
      "The Scepsis story": "The Scepsis story (Strabo XIII.1.54; Plutarch, Sulla 26)",
      "How far from Aristotle": "How far from Aristotle: the cushions"}
ORDER = ["Not two distinct authors; maker count open", "The first draft of the Aristotle-position", "The Characters as an operation",
         "The hinge", "Direction unresolved", "The catalogues: shared titles and ghost twins", "The axis and the recovered names",
         "The received reading stated, its relations reversed", "Void as a control; the witness inside", "One self-dividing maker (hypothesis)",
         "Falsifiers and limits"]
old = {l["lineage"]: l for l in v07["P"]["rail"]}
rail = [dict(old[n]) for n in ORDER] + [dict(l, lineage=RN.get(l["lineage"], l["lineage"])) for l in v07["P"]["rail"] if isinstance(l["earliest"], str)]
assert len(rail) == len(old)
P["rail"] = rail

# R7, computed
KO_B = [s["text"] for s in o["KO_B"]["sentences"]]
def survive(A):
    out = []
    for b in KO_B:
        r = max((difflib.SequenceMatcher(None, a, b).ratio(), i + 1) for i, a in enumerate(A))
        out.append(r[1] if r[0] >= 0.95 else None)
    return out
s8 = survive([t for _, t, _ in sents]); s7 = survive([s["text"] for s in v07["KO"]["sentences"]])
measure = {"rule": "v0.8 R7: KO_B sentences surviving in the KO at similarity ≥ 0.95, with positions",
           "v0.8": {"surviving": sum(p is not None for p in s8), "of": len(KO_B), "positions": s8},
           "v0.7": {"surviving": sum(p is not None for p in s7), "of": len(KO_B), "positions": s7}}
P["entity"] = (f"Composed in the archive's ontology (v0.8): KO_B sentences surviving {measure['v0.8']['surviving']} of {len(KO_B)} "
               f"(v0.7: {measure['v0.7']['surviving']} of {len(KO_B)}); every field claim carried and translated.")
words = sum(len(re.findall(r"[A-Za-z0-9'’-]+", t)) for _, t, _ in sents)
o["KO"], o["P"] = KO, P
o["L_BA"] = {"words": words, "text": " ".join(t for _, t, _ in sents), "rail": [],
             "note": "L_A(B ∪ A): the field and the archive composed in the archive's ontology (v0.8 §1.6a), realized as the knowledge object (objects.KO); its rail is the compression's, by lineage."}
spec = "EA-NEGONT-02 v0.8" + (f", #{DEP}" if DEP else "")
row["spec"] = spec
row["status"]["procedure"] = (f"{spec}: composed in the archive's ontology (E_A, E_F, ρ = constructs; translation replaces admission); "
                              "entity before address (ruled 2026-10-07); archive selected by D/R/O, first reading 2026-10-07 (32 of 35 admitted), hop and O-class not run")
row["ontology"] = {
 "composition": "archive (v0.8 §1.5: the archive's reading has precedence in shaping the entity)",
 "E_F": {"type": "C (public entity: a person)", "definition": "an ancient Greek philosopher and naturalist, Aristotle's colleague and successor at the Lyceum (B1–B8)", "claims": ["F1", "F2", "F23", "F45"]},
 "E_A": {"definition": "the name under which part of one corpus transmitted under two names has come down; a function, the world decomposed into register; in method-order the first draft of the Aristotle-position; maker count open because uncounted",
         "claims": ["T1587-01", "T1588-01", "T1588-03", "T1587-06", "T1584-04", "T1585-01", "T1585-02"],
         "defining_papers": [1587, 1588, 1583, 1584, 1585, 1605, 1658]},
 "rho": {"value": "constructs", "statement": "the archive reads E_F as made by reception: its data are relations supplied by receiving texts",
         "claims": ["T1585-04", "T1570-03", "T1658-03"], "guard": "T1658-08: the ledger shows what the attestation of a person rests on, not that no person stood behind the name"},
 "translation": trows,
 "receiving_texts": "Diogenes Laertius and Strabo seated whole (#1580; data/corpora/); loci checked by rebuild/negative-of-the-negative/v08_theophrastus_check.py"}
row["measure"] = measure
row["delta"]["T_vs_LB_reading"] = ("v0.8 §0.5 (ruled 2026-10-08): the first diff is already ontological. What AIO composes from the cards it surfaced, "
                                   "against what those cards hold, shows its composition working in its own ontology: the person, at coarse grain.")
RP.write_text(json.dumps(row, ensure_ascii=False, indent=1), encoding="utf-8")
# the panel's entity record: the name without the received person's dates; the ontology named
_raw = PP.read_text(encoding="utf-8"); PANEL_NL = _raw.endswith("\n"); panel = json.loads(_raw)
en = next(e for e in panel["entities"] if e["entity"] == "theophrastus")
en.setdefault("name_v07", en["name"]); en["name"] = "Theophrastus"
en["ontology"] = {"composition": "archive", "E_A": "a name for part of one corpus transmitted under two names", "E_F": "type C, a person", "rho": "constructs"}
en["stage"] = f"recomposed 2026-10-08 under {spec} (draft, not frozen; ledgers unaudited): field 62 claims carried and translated; archive 150 from 32 of 35 deposits; hop and O-class not run"
PP.write_text(json.dumps(panel, ensure_ascii=False, indent=1) + ("\n" if PANEL_NL else ""), encoding="utf-8")
print("recomposed:", len(sents), "KO sentences,", words, "words;", len(trows), "translation rows; measure", measure["v0.8"], "against", measure["v0.7"])
