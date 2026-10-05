#!/usr/bin/env python3
"""Apply the operator's rulings of 2026-10-05 to the worked example's archive ledger (EA-NEGONT-02 v0.7).

Ruling 2 (constitutive flags): "for now, lets do both. i am not viewing this as something we have fixed, but as
something we will need to iterate over and adjust." Both readings are carried: `const` (the first pass, kept
under its name) and `const_x2` (the second extraction, §3.8), with the matched claim. Neither is used to cut.

Ruling 3: "recode under 4.2". §4.2: self-definition is not self-description; self-description lowers force only
where a source assesses itself (its status, its success, its limits). Every claim the first pass coded
self-description is re-read under that rule. A source's definition of its own term or subject becomes
`stipulation` (v0.7 §3.3); a falsifier becomes `hypothesis` (the condition belongs to the claim it would refute);
a claim about the world becomes the modality its content carries. Self-assessment stays self-description. The
prior coding is kept in `modality_v06`.

Idempotent: re-running from the v0.6 ledger state gives the same output.
"""
import json, re, pathlib, hashlib

HERE = pathlib.Path(__file__).resolve().parent
LP = HERE / "ledger-archive.json"
L = json.loads(LP.read_text(encoding="utf-8"))

RECODE = {  # id: (new modality, reason)
 "P001-01": ("stipulation", "defines its own term, classifier model collapse"),
 "P001-08": ("stipulation", "defines its term's relation to strict generative collapse"),
 "P001-12": ("hypothesis", "falsifier of the paper's hypothesis"),
 "C46-02": ("stipulation", "the mint's gloss of a term it lists"),
 "C46-03": ("stipulation", "the mint's variant family"),
 "C46-06": ("stipulation", "states the mint's own procedure (priority test)"),
 "C46-01": ("attributed", "gloss of the conventional sense of model collapse, not the source's own term"),
 "C199-01": ("interpretation", "a claim about three literatures, not about the source"),
 "C199-07": ("stipulation", "defines correlated vulnerability"),
 "C199-09": ("stipulation", "defines SSDI"),
 "C199-12": ("hypothesis", "falsifier"),
 "A745-04": ("interpretation", "a claim about experimental method"),
 "A783-04": ("interpretation", "a claim about a corrective"),
 "L855-10": ("hypothesis", "falsifiers per substrate"),
 "L856-04": ("hypothesis", "falsifier F1"),
 "L856-05": ("hypothesis", "falsifier F2"),
 "B931-01": ("hypothesis", "the claim is about classifiers (foreclosure present); the 'defensible' framing rides as a limit"),
 "B931-05": ("stipulation", "defines what the replay bank measures and the collapse-inference criterion"),
 "B931-07": ("hypothesis", "falsifier with thresholds"),
 "P932-10": ("stipulation", "defines the proposed metric (OAR)"),
 "P932-12": ("hypothesis", "falsifier"),
 "B933-01": ("stipulation", "defines what a correcting architecture is"),
 "B933-02": ("interpretation", "a formal argument about foreclosure, not an assessment of the source"),
 "B933-04": ("stipulation", "defines the anchor caveat and inference criterion"),
 "B933-05": ("hypothesis", "architecture falsifiers"),
 "B947-06": ("hypothesis", "falsifier of P8"),
 "B1081-04": ("stipulation", "defines the P4 bridge experiment"),
 "B1147-07": ("hypothesis", "a claim about the loop's dynamics ('can be interrupted'), not a self-assessment"),
 "B1200-07": ("hypothesis", "falsifier"),
 "D1540-03": ("stipulation", "defines the relation in two stages"),
 "D1540-04": ("stipulation", "defines what collapses (admissible variance)"),
 "D1540-11": ("hypothesis", "falsifier"),
 "C1554-06": ("interpretation", "a claim about the relation of two works"),
 "D1574-01": ("stipulation", "defines its own term, disciplinary model collapse"),
 "D1574-06": ("stipulation", "states its method"),
 "D1616-01": ("stipulation", "states the extension its term makes (genealogy/definition)"),
 "D1616-02": ("stipulation", "operational definitions of flattening and collapse"),
 "D1616-03": ("stipulation", "operational definition of reality"),
 "D1616-12": ("hypothesis", "pre-registered falsification"),
}
# Everything else coded self-description is self-assessment (status, success, limits) and stays.

def toks(s):
    return set(re.findall(r"\w+", (s or "").lower()))

X = []
for f in "XYZ":
    for c in json.loads((HERE / f"audit/extract-{f}.json").read_text(encoding="utf-8")):
        c["_ext"] = f
        X.append(c)
def depnum(c):
    s = str(c.get("source", "")).lstrip("#")
    return int(s) if s.isdigit() else None

stay = []
for c in L:
    m = c.get("modality_v06", c.get("modality")) or ""
    c["modality_v06"] = m
    if "self-description" in m:
        if c["id"] in RECODE:
            c["modality"], why = RECODE[c["id"]]
            c["recode"] = {"rule": "§4.2", "ruled": "2026-10-05", "reason": why}
        else:
            c["modality"] = m
            c.pop("recode", None)
            stay.append(c["id"])
    # ruling 2: carry the second extraction's constitutive reading beside the first
    qa = toks(c.get("quote"))
    best, bs = None, 0.0
    for x in X:
        if depnum(x) != c["dep"]:
            continue
        qb = toks(x.get("quote"))
        if qa and qb:
            ov = len(qa & qb) / min(len(qa), len(qb))
            if ov > bs:
                bs, best = ov, x
    if best is not None and bs >= 0.6:
        c["const_x2"] = bool(best.get("constitutive"))
        c["const_x2_match"] = {"extractor": best["_ext"], "claim_id": best["claim_id"], "quote_overlap": round(bs, 2)}
    else:
        c["const_x2"] = None
        c["const_x2_match"] = None

missing = sorted(set(RECODE) - {c["id"] for c in L})
assert not missing, missing
LP.write_text(json.dumps(L, ensure_ascii=False, indent=1), encoding="utf-8")
n_re = sum(1 for c in L if c.get("recode"))
n_x1 = sum(1 for c in L if c.get("const"))
n_x2 = sum(1 for c in L if c.get("const_x2"))
n_m = sum(1 for c in L if c.get("const_x2_match"))
print(f"recoded {n_re}; self-description kept {len(stay)}; const x1 {n_x1} of {len(L)}; const x2 {n_x2} of {n_m} matched; "
      f"sha256 {hashlib.sha256(LP.read_bytes()).hexdigest()[:16]}")
