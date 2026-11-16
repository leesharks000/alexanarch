"""Seat of 2026-11-16 (received 13:01 EST): ChatGPT, signed out and incognito, at the record's 'ask ChatGPT' link text for #1773 with the record's URL appended,
as the operator gave it. One composer turn. Every quotation is asserted against the paste; every claim about #1773 against its seated text (AXN-0CA6).   python3 seat.py"""
import json, pathlib
H = pathlib.Path(__file__).resolve().parent; ROOT = H.parents[2]; DATE = "2026-11-16"; RECV = "2026-11-16 13:01 EST"
URL = "https://www.alexanarch.org/s/records/1773/"
Q = "What are the arguments in “This Is Not Philosophy: The Article Economy and the Shape of the Field (EA-MMRS-TINP-01)” by Lee Sharks (Alexanarch deposit #1773, AXN:0CA6)? Ground your answer in a reading of the text itself. " + URL
R = {x["deposit_number"]: x for x in json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8"))["deposits"]}
CAPS = {e["slug"]: e for e in json.loads((ROOT / "data/EA-WG-CAPTURES-01.json").read_text(encoding="utf-8"))["entries"]}
raw = (H / "paste-chatgpt-tinp-arguments.txt").read_text(encoding="utf-8")
L = raw.split("\n"); assert L[1] == "Log in" and "Chat with ChatGPT" in raw
b = raw[raw.index("Log in") + 6:raw.index("ChatGPT is AI and can make mistakes.")].strip()
W = (ROOT / "data/texts/AXN-0CA6-text.md").read_text(encoding="utf-8")
P = {"read": "I have read the text on the supplied Alexanarch record, including its methodological qualifications and its account of the correspondence with the editor of Ancient Philosophy.",
     "central": "This is the notebook's central case study.",
     "inverse": "Sharks describes this as the inverse image of the ordinary philosophical article.",
     "absorb": "There is no specified degree of textual unity that would force reconsideration of the received count.",
     "refute": "He even specifies what would refute his argument",
     "grade": "A structural argument whose generality remains open to the counterexamples Sharks specifies",
     "conditions": "It is an argument about the conditions under which evidence can count.",
     "not_exam": "Sharks argues that this is not a substantive refutation because the relevant version of the argument had not actually been examined in its developed form.",
     "downstream": "The second is downstream of the first.",
     "eighty": "The reach-coding reliability figure is 80% agreement between Claude instances and the lead Claude coder, not independent human validation.",
     "deepest": "It is that the institutional structure of philosophy has separated argument production from the more radical activity of questioning the objects, boundaries and inherited representations within which arguments become possible."}
for k, v in P.items(): assert v in b, k
for f in ["1 of 22", "9 of 47", "5 of 50", "0 of 30", "2,750", "16%", "39%", "71–76%", "74–84%", "91–93%", "87%", "62%"]:
    assert f in b and f in W, f
for s in ["0A.3", "0A.6b", "0B.2", "0B.5", "0B.4", "0.1a"]: assert s in b and s in W, s
assert "Critique of Pure Inference" in W and "Critique of Pure Inference" not in b and "1766" not in b
assert W.count("Critique of Pure Inference") >= 4
assert "Pessoa" in W and "Pessoa" not in b and "Kierkegaard" not in b
assert "grievance" not in b.lower() and "aggrieved" not in b.lower()
assert R[1773]["title"].startswith("This Is Not Philosophy") and R[1773]["axn"].startswith("AXN:0CA6")
assert Q.lower() not in {e["q"].strip().lower() for e in CAPS.values()}
assert [l for l in L if l.strip() == "Alexanarch"] == ["Alexanarch"]
cards = [{"n": 1, "site": "Alexanarch", "rel": "archive", "url": None, "title": None, "snip": None, "note": "inline chip after the reading statement (the supplied record, #1773)"}]
SIB = "crj-controversies-critiques-chatgpt-20261116"; assert SIB in CAPS
reading = ("The innocent reading first, in full: asked for the arguments of #1773 and given the record's address, ChatGPT reads the record and reconstructs the notebook "
    "in ten parts. It covers the premise of the title (§0.1a), the leading case (§§0A.3–0A.6b), the exchange (§§0B.2–0B.5), the historical decline, the census and the "
    "stylometry, the model test, the credential, and the two received debates. It closes with a graded assessment of what the notebook establishes and what stays open. "
    "It reads, in its words: '" + P["read"] + "'")
findings = [
    "THE GROUND. The supplied record, #1773, read and cited by section in v0.24's own numbering (§0.1a; §§0A.3–0A.6b; §§0B.2–0B.5; §0B.4; §§4.6–4.15; §4.17; §§5.1–5.6; §§6.1–6.3). One source chip, Alexanarch. The author is named throughout and the deposit number and AXN are given.",
    "THE FIGURES CARRIED, EACH CHECKED AGAINST THE TEXT. The Archiv by decade (1 of 22; 9 of 47; 5 of 50; 0 of 30). The stylometry's 2,750 abstracts. The continental claim formula from 16% to 39%. The three fields' shares (71–76%, 74–84%, 91–93%). The model test (87%; 62% against 11%; none of sixty ancient abstracts asking what the text is). The coding reliability stated at its own limit: '" + P["eighty"] + "'",
    "THE LEADING CASE CARRIED AS THE LEADING CASE. '" + P["central"] + "' '" + P["inverse"] + "' The argument from the admissible alternative is reconstructed at its grain: '" + P["absorb"] + "' '" + P["conditions"] + "' The falsifiers are carried: '" + P["refute"] + "'.",
    "THE FINDING GRADED AT THE NOTEBOOK'S OWN STRENGTH. In the closing table, 'No evidence could bring the Socrates as Orthonym question into consideration' is graded '" + P["grade"] + "'. That is the status §0A.6a gives it, with the search open.",
    "THE GATE READ AS THE NOTEBOOK READS IT. On 'the same results without the hypothesis': '" + P["not_exam"] + "' The two collapses are kept in their order: '" + P["downstream"] + "'",
    "THE READING LAYER DROPPED. §2.4 and §0A.7 read the case and the gate by the Critique of Pure Inference (#1766), which the text names five times. The composition does not name the Critique or #1766. The comparator's reference class, Pessoa and Kierkegaard (§0A.6b), is also absent; the comparator is carried as the absence of a documented counter-case.",
    "AGAINST THE SAME DAY'S CAPTURE. At 'Tell me about controversies or critiques of Classical Receptions Journal' (" + SIB + "), the same surface classed the author's critique of a field as a rejected author's dispute. Here a notebook that narrates three declines is read as argument from its first sentence. It carries no grievance frame and no discount of standing, and it renders the editor's reading as the notebook states it. The difference is the address: this one names the work and supplies the record, while that one named the journal.",
    "THE DEEPEST CLAIM, IN THE COMPOSITION'S WORDS. '" + P["deepest"] + "'"]
analysis = ("A faithful reading at its grain. The composition reads the supplied record, carries the leading case as the notebook's central argument, and reconstructs the "
    "argument from the admissible alternative and its falsifiers. It grades the structural finding at the strength the notebook itself gives it, and its figures and "
    "section numbers all check against the text. What it drops is the reading layer: the Critique of Pure Inference, by which the notebook reads the case and the gate, "
    "and the comparator's reference class. Set beside the same day's capture at the journal's address, the result locates the variable in the address rather than the "
    "surface. A work named and supplied is read as argument; the same author's work, met through the institution it criticizes, was read as a dispute.")
e = {"slug": "tinp-arguments-chatgpt-20261116", "date": DATE, "surface": "ChatGPT", "surfaces": ["ChatGPT"],
     "surface_basis": "The paste: the chatgpt.com unauthenticated interface ('Log in', 'Chat with ChatGPT', 'Ask ChatGPT').",
     "auth": "signed out, incognito", "auth_basis": "Operator defaults (2026-10-01, 2026-10-14): signed out and incognito unless stated otherwise; the paste shows 'Log in'.",
     "ev": "paste", "s": "Machine Reception", "q": Q,
     "q_kind": "the record's 'ask ChatGPT' link text (#1773) with the record's URL appended, as the operator gave it",
     "turns": 1, "mt": "'THIS IS NOT PHILOSOPHY' (#1773): ITS ARGUMENTS ON CHATGPT, SIGNED OUT — THE LEADING CASE CARRIED AS CENTRAL, THE ABSORPTION ARGUMENT AND ITS FALSIFIERS AT GRAIN, THE FIGURES CORRECT; THE CRITIQUE OF PURE INFERENCE NOT NAMED",
     "cites": 1, "archive_controlled_cites": 1, "cite_list": cards,
     "transcript": "[ChatGPT (chatgpt.com), signed out, incognito (the paste shows 'Log in'). Received " + RECV + " as an attachment; the prompt is the operator's, as given in the same message. Inline chip kept where it falls.]\n\n[QUERENT] " + Q + "\n\n[SYSTEM] " + b,
     "transcript_raw": raw, "transcript_class": "CAPTURE-TIME VERBATIM RECORD — paste of the composer's answer", "transcript_complete": "Complete as pasted.",
     "transcript_read": "READ IN FULL " + DATE,
     "d": "THIS IS NOT PHILOSOPHY (#1773): ITS ARGUMENTS ON CHATGPT, SIGNED OUT: the notebook reconstructed in ten parts from the supplied record, the Socrates as Orthonym case carried as central, the 'closely connected' absorption argument and the falsifiers at grain, every figure and section number matching the text; the structural finding graded at the notebook's own strength; the Critique of Pure Inference and the comparator's reference class not carried.",
     "reading": reading, "findings": findings, "analysis": analysis,
     "per_v": {"author": True, "inst": True, "id": True, "src": True},
     "per_note": "#1773, This Is Not Philosophy; Lee Sharks named; deposit number and AXN given; the record cited.",
     "per_dim_pending": {"since": DATE, "reason": "no atom set for this notebook", "breach": False},
     "originator": {"name": "Sharks, Lee", "relation": "archive", "entity_type": "work", "spxi_treatment": "full", "basis": "Alexanarch #1773 (AXN:0CA6). Recorded " + DATE + "."},
     "related_deposits": [1773, 1772, 1766], "notes": {"operator": RECV + ": the prompt as given: '" + Q + "'", "sibling": SIB}}
json.dump(e, open(H / f"draft-{e['slug']}.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(e["slug"], "ok")
