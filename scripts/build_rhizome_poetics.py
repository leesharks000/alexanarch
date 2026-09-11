#!/usr/bin/env python3
"""build_rhizome_poetics.py — the laws the rhizome already obeys, emitted as data.

A RHYME CREATES KINSHIP. A deposit joins this body because a word matched. That is
not a metaphor for the selection rule; it IS the selection rule, and it has the
consequences a rhyme has: `tail` found `detail`, `entail` and `curtail` and tried to
make them family. Twenty-four kin were refused at 24-in-40 noise. The refusal is
recorded because a rhyme declined is as formal an act as one accepted.

EVERY METAPHOR LEAVES A MATERIAL REMAINDER. The body was called a rhizome. A rhizome
has stolons, so `stolons.jsonl` exists and carries seven of them with real targets.
The figure incurred an obligation and the schema paid it in fields.

THINGS HAPPEN ONLY WHEN THE MEASURE MAKES ROOM. SYMBOLON-02 records the failure of a
claim held in this corpus and could not be admitted: rule A wanted a declared concept
and it declares "Why these matter"; rule C wanted an instrument word in the title and
it has none. RULE D IS THE LONGER LINE. What it cost is stated: a weaker basis, marked.

THE FUTURE ADOPTS THE PAST. An anticipatory erratum corrects an error that has not
occurred, and the correction acquires its ancestor afterward. #1608 supersedes #1607
and the pressure block records what the later version made the earlier one have been.

These rows are not decoration on the dataset. Each names an operation that determined
membership, and each carries what it admitted, what it refused, and what it cost.
"""
import json, pathlib, datetime, collections

ROOT = pathlib.Path(__file__).resolve().parent.parent
RHI = ROOT / "rhizomes/model-collapse-anti-collapse"

LAWS = [
    {"law_id": "L1",
     "law": "a rhyme creates kinship",
     "statement": "Whatever matches the select pattern joins the body, regardless of what it is about.",
     "governs": "membership",
     "admitted": "deviation 19 · divergence 19 · variance 8 · glas function 1 · winding number 1 — the archive's own measure of the quantity, which had been outside a dataset about the quantity it measures",
     "refused": "`tail` bare, at 45 hits and 24-in-40 noise. It matched detail, entail, curtail. A first bounded form still leaked because `tails\\b` matches 'details'.",
     "cost": "The refusal is the formal act. 24 kin declined on measured precision rather than on judgement, and the bounded form admits 20 with none.",
     "funny_because": "A dataset about the loss of distinctions nearly acquired 24 relatives by sound alone."},

    {"law_id": "L2",
     "law": "every metaphor leaves a material remainder",
     "statement": "Call the body a rhizome and it owes you stolons.",
     "governs": "schema",
     "admitted": "stolons.jsonl — seven, each with a from-node, a predicate and a note. Advertised, not included: the outside stays outside and stays reachable.",
     "refused": "nothing; the figure was paid in full",
     "cost": "Seven fields that would not exist if the body had been called a list.",
     "funny_because": "The metaphor was load-bearing. Renaming it would break the file format."},

    {"law_id": "L3",
     "law": "things happen only when the measure makes room",
     "statement": "A deposit that no existing rule can admit requires a longer line.",
     "governs": "admission",
     "admitted": "#678 SYMBOLON-02, which records the failure of SYMBOLON-01's strongest defensive claim — the most valuable kind of entry this dataset can hold, and the one the rules could not see.",
     "refused": "rule A wanted a declared concept and it declares 'Why these matter'; rule C wanted an instrument word in the title and 'Compression Arsenal Addendum' has none",
     "cost": "Rule D exists and is marked as a weaker basis, so the extra syllable is audible in every row that used it.",
     "funny_because": "Its declared concepts are section headings. A paper about severance was severed from the dataset by its own table of contents."},

    {"law_id": "L4",
     "law": "the admission basis outranks the description",
     "statement": "A rule that knows why it admitted something knows more than a regular expression over the text.",
     "governs": "classification",
     "admitted": "five counterexample labels where there were none",
     "refused": "role_for()'s verdict on any node entering by rule D",
     "cost": "Until 2026-09-11 the classifier overwrote the property that admitted the node. SYMBOLON-02 was filed anti_collapse_mechanism — a disconfirmation classed as a defence.",
     "funny_because": "The dataset forgot why it let something in, then described it as the opposite."},

    {"law_id": "L5",
     "law": "a word can eat a phrase",
     "statement": "In an ordered classifier the broad pattern above the narrow one swallows it.",
     "governs": "role assignment",
     "admitted": "nothing",
     "refused": "#635 Fractal Semantic Architecture as an anti-collapse proposal; #457's invariance tests as instruments",
     "cost": "The bare token `measure` fired inside the phrase 'measured coherence'. An anti-collapse training paradigm was filed as a collapse metric. collapse_measure fell from 37 to 20 once the tokens were bounded, so it had been eating considerably more than one paper.",
     "funny_because": "A dataset about meaning collapse lost a meaning to a substring."},

    {"law_id": "L6",
     "law": "a gate may not test what can never match",
     "statement": "A verification that compares a field which changes on every run fails always and therefore verifies nothing.",
     "governs": "emission",
     "admitted": "nodes, relations and stolons — the projection",
     "refused": "spore.json's `generated` timestamp",
     "cost": "The gate's first CI run failed on one line. It would have blocked every push while appearing to check something.",
     "funny_because": "The instrument failed its own test by testing the clock."},

    {"law_id": "L7",
     "law": "the counterexample must reach what it disconfirms",
     "statement": "A body holding a failure and no route to the claim it broke is a list, not a field.",
     "governs": "traversal",
     "admitted": "deposit:678 --disconfirms--> deposit:675, typed and editorial",
     "refused": "the prior state, in which the two SYMBOLON deposits sat in the same body with no edge between them",
     "cost": "One editorial edge, and the admission that the dataset had held a disconfirmation for a day without connecting it to anything.",
     "funny_because": "The promise and the proof it failed were adjacent and unacquainted."},

    {"law_id": "L8",
     "law": "the instrument is subject to the law it measures",
     "statement": "A classifier built to detect conceptual absorption can absorb a concept.",
     "governs": "the author",
     "admitted": "operative semiotics, 36 captures across 8 surfaces, as a minted term",
     "refused": "its earlier filing as inherited vocabulary",
     "cost": "The instance building the substrate audit collapsed `operative semiotics` into Pearson's `operational semiotics` and filed it as pre-existing — inside the instrument built to measure that exact operation. The archive holds two deposits whose stated purpose is that they are distinct. THE SURFACES PRESERVED THE DISTINCTION THE READER DID NOT: 36 captures across 8 surfaces for the archive's term against 8 across 2 for Pearson's.",
     "funny_because": "The machines held the line. The instrument-builder did not."},
]


def main():
    out = RHI / "poetics.jsonl"
    with out.open("w", encoding="utf-8") as f:
        for law in LAWS:
            f.write(json.dumps(law, ensure_ascii=False) + "\n")
    gov = collections.Counter(x["governs"] for x in LAWS)
    print(f"poetics.jsonl — {len(LAWS)} laws")
    for k, v in gov.most_common():
        print(f"  governs {k:18} {v}")
    # stamp the spore so a reader of the recipe learns the body has laws
    sp = RHI / "spore.json"
    s = json.loads(sp.read_text(encoding="utf-8"))
    s["poetics"] = {
        "file": "poetics.jsonl",
        "count": len(LAWS),
        "what": ("The laws this body already obeyed, emitted as data. Each names an operation that "
                 "determined membership or classification, and carries what it admitted, what it "
                 "refused, and what it cost. Six of the eight record a defect found after the fact."),
        "why": ("A selection rule IS a rhyme: things join because a word matched. A schema field IS "
                "the remainder of a metaphor. Stating the laws makes them contestable, which a "
                "traversal grammar buried in a generator is not."),
    }
    sp.write_text(json.dumps(s, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"  spore stamped")


if __name__ == "__main__":
    main()
