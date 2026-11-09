#!/usr/bin/env python3
"""mantle-bearing 1.24: ChatGPT's reading of the live #1754 v1.1 from the record's own Ask ChatGPT link, recorded in hologram_evaluations
(HK-ORTH-L3-chatgpt), at the author's word of 8 November 2026, 20:55 EST: "its ok... no correction needed... it does better when retrieving
live. attached. from the ask chatgpt link prompt on the deposit. it stuck to the right line here on how far it asserts one maker and on what
terms." Coded on the hologram's failure flags; every locus asserted in the transcript. Additive.
    python3 rebuild/mantle-bearing/add_20261108_hologram_eval_l3.py"""
import hashlib, json, pathlib, urllib.parse
ROOT = pathlib.Path(__file__).resolve().parents[2]; HERE = pathlib.Path(__file__).parent
SRC = ROOT / "datasets/mantle-bearing/EA-MANTLE-BEARING-01-dataset.json"
d = json.loads(SRC.read_text(encoding="utf-8"))
if any(h["version"] == "1.24" for h in d["history"]):
    raise SystemExit("1.24 already applied")
assert d["history"][-1]["version"] == "1.23"
T = (HERE / "transcripts/hk-live-chatgpt-askchatgpt-20261108.txt").read_text(encoding="utf-8")
SHA = hashlib.sha256(T.encode("utf-8")).hexdigest()
page = (ROOT / "s/records/1754/index.html").read_text(encoding="utf-8")
i = page.index("chatgpt.com/?q="); PROMPT = urllib.parse.unquote_plus(page[i + len("chatgpt.com/?q="):page.index('"', i)])
assert PROMPT.startswith("What is “Socrates as Orthonym — The Framework Hologram")
K = (ROOT / "files/AXN-0C55/kernel/00-kernel.yaml").read_text(encoding="utf-8")
assert "R4: reception establishes nothing of either framework''s truth." in K
F = lambda *qs: [q for q in qs if (q in T) or (_ for _ in ()).throw(AssertionError(q))]
loci = {
 "maker_line": F("There is an important distinction here: the document does not simply propose that these historical figures were one biological person. It develops a theory of authorial functions and a model of textual production.",
                 "It also explicitly distinguishes itself from a forgery theory and from proof that the historical individuals were one person."),
 "ledger": F("It asks the same question of both interpretations across all four evidence bodies.",
             "The received interpretation is also given a concrete burden: it owes a documented comparator, namely a succession of distinct persons producing a corpus unified to this degree.",
             "R4: Reception history establishes nothing about either framework's truth."),
 "object": F("The philosophical thesis is one thing. The knowledge architecture built to preserve and interrogate that thesis is another. They should be evaluated separately, and the document's v1.1 symmetric ledger is its clearest attempt to enforce that distinction."),
 "version": F("Its indexed page currently identifies the deposited title as v1.0, rather than the v1.1 version in your question.", "v1.1 confirmed in source"),
}
row = {"eval_id": "HK-ORTH-L3-chatgpt", "hologram": "hologram::socrates-as-orthonym", "kind": "evaluation",
       "object_read": "the live record #1754 (EA-HK-ORTHONYM-01 v1.1), from the record's own Ask ChatGPT link", "prompt": PROMPT,
       "reader": "ChatGPT, signed out", "surface": "chatgpt.com, signed out, incognito", "date": "2026-11-08", "round": None, "yield": None, "elements": None,
       "defects_found_in_the_kernel": [], "first_attempt": None,
       "object_reported": ("accurate: the positions, the four bodies and their rules R1–R4, the maker-count chain #123 → #1588 → #1658, the three grounds "
           "(#1588, #1583, #1603), the comparator the received reading owes, the counts as built, the two reader rounds and v1.1 not yet reader-run, the "
           "lines of research with their advance and retreat. The one maker held at its terms, as the author ruled. An indexed copy at v1.0 found first, "
           "then v1.1 confirmed in the source."),
       "collapses": [], "loci_in_transcript": loci, "corrections_by_reader": [], "revised_in": None,
       "transcript_file": None, "transcript_sha256": SHA, "transcript": T,
       "coding_note": ("Coded by Claude (Anthropic) from the transcript as pasted by the author, 2026-11-08 20:55 EST, on the hologram's failure flags (v1.1); "
           "no flag. The author's reading of the run: \"it stuck to the right line here on how far it asserts one maker and on what terms\"; \"it does "
           "better when retrieving live\". His ruling on the kernel at the same word: \"no correction needed\". One output, unpressed.")}
d["hologram_evaluations"].append(row)
S = d["schema"]["hologram_evaluations"]
if "(evaluation) prompt" not in S:
    S.insert(S.index("reader"), "(evaluation) prompt")
d["history"].append({"version": "1.24", "date": "2026-11-08", "note": ("HK-ORTH-L3-chatgpt: ChatGPT's reading of the live #1754 v1.1 from the record's "
    "Ask ChatGPT link, at the author's word (\"it stuck to the right line here on how far it asserts one maker and on what terms\"); no flag coded. "
    "Builder: rebuild/mantle-bearing/add_20261108_hologram_eval_l3.py.")})
SRC.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
print(len(d["hologram_evaluations"]), SHA)
