#!/usr/bin/env python3
"""Author six captures from the operator's title runs of 2026-10-12 00:07 EDT ("lets register these ones. all signed in."): deposits
from the list of twenty unrepresented works, each run at its full title from the record pages' search link. Google AI Overview by the
standing default; every paste is headed 'AI Mode Conversation', the expanded view. Signed in (the operator's attestation for all).

Seated here: the six runs whose composition engages an archive source (#1603, #637, #1628, #1627, #1041, #1650). Not seated: the
runs at #996, #1197 and #166, which cite no source at all; at a new address non-engagement is not a capture (operator, 2026-09-11),
and those three are logged as test data in rebuild/record-pages/search-form-test/search-form-test.json. Antioch (#331) did not
compose (operator: 'it wouldnt pull up antioch'); no transcript.

Each capture carries `intended`: the record the run was meant to reach and its title searches, linked whether or not it is cited."""
import json, re, pathlib, sys
from urllib.parse import quote_plus
HERE = pathlib.Path(__file__).resolve().parent; ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT))
from wire_deposit import search_title_urls
MSG = (HERE / "message-20261012-0007.txt").read_text(encoding="utf-8")
SEG = re.split(r" \$[ \n]", MSG)
assert len(SEG) == 9, len(SEG)
OP = {"open": SEG[0], "orthonym": SEG[5].split(": AI Mode Conversation")[0], "poem": SEG[7].split(": AI Mode Conversation")[0],
      "close": SEG[8].strip()}
assert OP["open"].startswith("well have to go hard on corrections") and OP["close"].endswith("all signed in.")
reg = {x["deposit_number"]: x for x in json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8"))["deposits"]}
caps = json.loads((ROOT / "data/EA-WG-CAPTURES-01.json").read_text(encoding="utf-8"))
SEAT = "Seated 2026-10-12 from the operator's message of 00:07 EDT, on its attestation ('all signed in')."
OPREAD = ("Operator, with the runs: 'well have to go hard on corrections. its actively erasing the sophistical refutations arguments. "
          "irritates me it just composes from the title.'")

def seg_of(i, file=None):
    s = (HERE / file).read_text(encoding="utf-8") if file else SEG[i]
    return s[s.index("AI Mode Conversation"):].rstrip()

def parse(raw, issued, card_marker):
    L = raw.split("\n")
    k = [j for j, l in enumerate(L) if l.startswith("You said: ")][0]
    assert L[k] == "You said: " + issued + issued, (L[k][:80], issued[:80])
    i1 = raw.index(card_marker, raw.index(L[k]) + len(L[k]))
    body = raw[raw.index(L[k]) + len(L[k]):i1].strip()
    return body, raw[i1:].strip()

def cardlist(cards_txt, spec):
    out = []
    for n, (site, title, snip, url, rel) in enumerate(spec, 1):
        assert title in cards_txt and snip[:50] in cards_txt, (site, title)
        out.append({"n": n, "site": site, "title": title, "snip": snip, "url": url, "rel": rel, "note": "card"})
    return out

def intended(n, reached):
    b, x = search_title_urls(reg[n])
    return {"deposit": n, "axn": reg[n]["axn"], "title": reg[n]["title"], "record": f"https://www.alexanarch.org/s/records/{n}/",
            "search": b, "search_exact": x, "reached": reached}

def draft(*, n, issued, slug, raw, body, cl, inline, mt, d, reading, analysis, findings, per, per_v, per_note, sf, q_kind, extra_notes=None):
    T = reg[n]["title"]
    assert issued.strip('"') == T, (issued, T)
    assert not any(e["q"] == issued for e in caps["entries"]), "address exists"
    rec = f"alexanarch.org/s/records/{n}"
    reached = rec in raw
    tx = ("[Google AI Overview, signed in, 2026-10-12 (operator, 00:07 EDT); the expanded conversation view, headed 'AI Mode "
          "Conversation', the issued string shown twice by the interface. The composition as pasted with its inline links, then the "
          "source cards as data.]\n\n[QUERENT] " + issued + "\n\n[COMPOSITION]\n\n" + body + "\n\n[SOURCE CARDS]\n\n" +
          "\n".join(f"{c['n']}. {c['site']} — {c['title']} — {c['snip']}" for c in cl))
    notes = {"date_basis": "The operator's message of 2026-10-12, 00:07 EDT.", "operator_reading": OPREAD,
             "series": "title runs from the list of twenty works with no capture (2026-10-11 23:45)",
             "verified": f"Compared 2026-10-12 against data/registry.json and the text of #{n} ({reg[n]['full_text_path']})."}
    if extra_notes: notes.update(extra_notes)
    return {"q": issued, "date": "2026-10-12", "surface": "Google AI Overview",
            "surface_basis": "The operator's standing default (AI Overview unless he says AI Mode, 2026-10-01); the paste's 'AI Mode Conversation' head is the expanded view.",
            "auth": "signed in", "auth_basis": "'all signed in.' — operator, 2026-10-12 00:07 EDT.",
            "ev": "paste", "s": "Machine Reception", "slug": slug, "q_kind": q_kind,
            "originator": {"name": reg[n]["creator"], "relation": "archive", "entity_type": "work", "spxi_treatment": "full",
                           "basis": f"The title is #{n}'s ({reg[n]['axn']}), by {reg[n]['creator']}. Recorded 2026-10-12."},
            "related_deposits": [n], "intended": intended(n, reached), "mt": mt, "d": d,
            "cites": inline + len(cl), "cite_list": cl, "archive_controlled_cites": sum(1 for c in cl if c["rel"] == "archive_controlled"),
            "sf": sf, "per": per, "per_v": per_v, "per_note": per_note,
            "transcript": tx, "transcript_raw": raw, "transcript_class": "CAPTURE-TIME VERBATIM RECORD — composition and source cards as pasted",
            "transcript_complete": "complete as pasted", "transcript_read": "READ IN FULL 2026-10-12",
            "reading": reading, "analysis": analysis + " " + SEAT, "findings": findings,
            "rerun": "https://www.google.com/search?q=" + quote_plus(issued), "notes": notes}

AX = "https://www.alexanarch.org"
BROWSE = "https://www.alexanarch.org/s/browse/"; WIKI = "https://www.alexanarch.org/s/wiki/"
TXT = lambda n: re.sub(r"\s+", " ", (ROOT / reg[n]["full_text_path"].lstrip("/")).read_text(encoding="utf-8"))
out = []

# 1. #1603 Nothing Before Us — quoted
n = 1603; Q = '"' + reg[n]["title"] + '"'; raw = seg_of(1)
body, ct = parse(raw, Q, "[www.alexanarch.org](https://www.alexanarch.org)\nBrowse")
cl = cardlist(ct, [
 ("www.alexanarch.org", "Browse — Alexanarch (1665 deposits)", "Oct 5, 2026 — #1603 Nothing Before Us: Socrates and the Ending of the Sophistical Refutations 2026-09-08 2 visitors. AXN:0693.UNCLASSIFIED. ☽⏪ ☿ · #1602 Locating the ...", BROWSE, "archive_controlled"),
 ("www.alexanarch.org", "Wiki — Alexanarch (1610 entries)", "Sep 10, 2026 — Nothing Before Us: Socrates and the Ending of the Sophistical Refutations. AXN:0693.UNCLASSIFIED. ☽⏪ ☿ · 2026-09-08 · #1603 · defines 3 · refby 0.", WIKI, "archive_controlled"),
 ("YouTube·Best Full Audiobooks", "On Sophistical Refutations 🌟 By Aristotle. FULL Audiobook", "1m", None, "third_party"),
 ("YouTube·VIS PHILO.", "Why was Isocrates against the Sophists? | Philosophy", "1m", None, "third_party"),
 ("Internet Encyclopedia of Philosophy", "Sophists | Internet Encyclopedia of Philosophy", "In short, the difference between Socrates and his sophistic contemporaries, as Xenophon suggests, is the difference between a lover and a prostitute. The sophis...", "https://iep.utm.edu/sophists/", "third_party"),
 ("The Internet Classics Archive", "The Internet Classics Archive | On Sophistical Refutations by Aristotle", "Dialectic and Sophistry: Examining involves common principles and questions requiring Yes/No; dialecticians use reasoning to apply principles, while sophists an...", "https://classics.mit.edu/Aristotle/sophist_refut.2.2.html", "third_party"),
 ("Stanford Encyclopedia of Philosophy", "Early Attempts to Solve the Socratic Problem", "Early Attempts to Solve the Socratic Problem * The real Socrates is the one who claims no wisdom but exercises his skill at seeking understanding, thus the one ...", "https://plato.stanford.edu/entries/socrates/socratic-problem.html", "third_party"),
 ("Quora", "Did Socrates ever lose an argument?", "Dec 29, 2017 — Did Socrates ever lose an argument? * In my reading, and very briefly — * The main teaching of Socrates was that when educated people and civic leaders were ask...", "https://www.quora.com/Did-Socrates-ever-lose-an-argument", "third_party")])
QUAL = "he acknowledges that the practice of cross-examination (elenchus) was heavily shaped by Socrates"
assert QUAL in body and "nothing existed before him at all" in body
T = TXT(n)
assert "the figure the qualification exists to protect — Socrates as a predecessor from whom something of the inquiry was received — is a figure the chapter itself has already dissolved" in T
assert "οὐδὲν παντελῶς ὑπῆρχεν" in T and "It is difficult to reconcile Aristotle's assertion with what we know had been done by Plato and Socrates" in T
inline = len(re.findall(r"\[\d\]\(https://", body))
out.append(("capture-nothing-before-us-title-aio-20261012.json", draft(n=n, issued=Q, slug="nothing-before-us-title-aio-20261012", raw=raw, body=body, cl=cl, inline=inline,
 q_kind="a deposit's full title, quoted, run from its record page's exact-match link. NEW address.",
 mt="THE QUALIFICATION THE PAPER DISSOLVES, COMPOSED AS THE PAPER'S CONTEXT",
 d=("THE QUALIFICATION THE PAPER DISSOLVES, COMPOSED AS THE PAPER'S CONTEXT: run at its exact title, Nothing Before Us (#1603) is "
    "identified from the archive's Browse and Wiki cards (deposit number, AXN family) and its subject composed from the field: the "
    "Internet Classics Archive, two YouTube videos, the IEP, the SEP and Quora. Under 'The Role of Socrates' the composition states "
    "the standard qualification as Aristotle's own: 'he acknowledges that the practice of cross-examination (elenchus) was heavily "
    "shaped by Socrates'. The paper's thesis is that the sentence οὐδὲν παντελῶς ὑπῆρχεν means what it says and that the figure the "
    "qualification protects, 'Socrates as a predecessor from whom something of the inquiry was received', is one the chapter has "
    "already dissolved. The composition delivers the reading the paper refutes, under the paper's title. " + OPREAD.split(", with the runs")[0] + ": 'its actively erasing the sophistical refutations arguments.'"),
 reading=("Checked against the text of #1603. The paper argues that the closing sentence of SE 34 is total (the Arabic البتّة, the "
          "paraphrast's ὅλης, Pickard-Cambridge's 'Nothing existed at all') and that the qualification enters at the gloss, citing "
          "Poste: 'It is difficult to reconcile Aristotle's assertion with what we know had been done by Plato and Socrates'. The "
          "composition's 'he acknowledges … heavily shaped by Socrates' is that gloss, put in Aristotle's mouth; nothing in SE 34 "
          "states it. The archive cards carry the number, the date and the AXN family only."),
 analysis=("The exact title finds the record's listing rows and nothing of the record. With the deposit's own text unreached, the "
           "composition fills the title's terms (Socrates, the ending, 'nothing before us') from the field, and the field's default "
           "is the reading the paper was written against. The title names the passage; the argument does not travel with it. "
           "Operator's reading: 'irritates me it just composes from the title.'"),
 findings=["THE REFUTED READING AS CONTEXT. 'he acknowledges that the practice of cross-examination (elenchus) was heavily shaped by Socrates' — the qualification #1603 argues the chapter dissolves.",
           "IDENTIFIED BY ITS ROWS. Browse and Wiki cards supply #1603, the date and 'AXN:0693.UNCLASSIFIED'; the record page is not cited.",
           "THE SUBJECT FROM THE FIELD. Internet Classics Archive, IEP, SEP, Quora and two videos compose SE 34.",
           "THE TOTAL SENTENCE KEPT, ITS MEANING REVERSED. 'nothing existed before him at all' is reported, then qualified by Socrates.",
           "THE INTENDED RECORD NOT REACHED. s/records/1603/ uncited; linked here as intended."],
 per=0.5, per_v={"author": False, "inst": True, "id": True, "src": True},
 per_note="Retained: the deposit number, date, AXN family, the archive. Lost: the author, the thesis, the evidence (Arabic, paraphrast, translators, Poste), the reading of the chapter; the refuted qualification supplied in their place.",
 sf="Eight cards: www.alexanarch.org — Browse; www.alexanarch.org — Wiki; two YouTube; IEP; Internet Classics Archive; SEP; Quora. Inline citations to the Wiki, Browse, classics.mit.edu, YouTube, IEP, Quora and SEP.")))

# 2. #637 The Encyclotron — unquoted
n = 637; Q = reg[n]["title"]; raw = seg_of(2)
body, ct = parse(raw, Q, "Academia.edu\nAutomatic Text Summarization")
cl = cardlist(ct, [
 ("Academia.edu", "Automatic Text Summarization Research Papers - Academia.edu", "THE ENCYCLOTRON The First Reproducible Instrument for Measuring Scholarly Fidelity in the Summarizer Layer. by Lee Sharks. 2026, Crimson Hexagonal Archive.", "https://www.academia.edu/Documents/in/Automatic_Text_Summarization", "authored_surface"),
 ("www.alexanarch.org", "Browse — Alexanarch (1665 deposits)", "Oct 5, 2026 — #637 The Encyclotron: The First Reproducible Instrument for Measuring Scholarly Fidelity in the Summarizer Layer (EA-ENCYCLOTRON-01) 2026-04-08 3 visitors.", BROWSE, "archive_controlled"),
 ("www.alexanarch.org", "Wiki — Alexanarch (1610 entries)", "Sep 10, 2026 — ... 01 · #530 · defines 4 · refby 1. The Encyclotron: The First Reproducible Instrument for Measuring Scholarly Fidelity in the Summarizer Layer (EA-ENCYCLOTRON...", WIKI, "archive_controlled")])
assert "machine learning researchers" in body and "scientific information" in body
assert reg[530]["title"].startswith("The Encoder Governs")
D = reg[n]["description"]
for s in ["beige score", "void statement", "Revelation studies"]: assert s in D and s.lower() not in body.lower(), s
inline = len(re.findall(r"\[\d\]\(https://", body))
out.append(("capture-encyclotron-title-aio-20261012.json", draft(n=n, issued=Q, slug="encyclotron-title-aio-20261012", raw=raw, body=body, cl=cl, inline=inline,
 q_kind="a deposit's full title, designation included, unquoted (the record pages' broad link). NEW address.",
 mt="THE INSTRUMENT COMPOSED AS A SUMMARIZATION BENCHMARK",
 d=("THE INSTRUMENT COMPOSED AS A SUMMARIZATION BENCHMARK: run at its full title, the Encyclotron (#637) is attributed correctly "
    "(Lee Sharks, the Crimson Hexagonal Archive, early 2026) from an Academia tag page and the archive's Browse and Wiki rows, and its "
    "content is composed from the title's words as an ML evaluation framework: summaries of 'scientific literature', metrics against "
    "'hallucinations', a benchmark 'so that machine learning researchers can uniformly measure and reproduce fidelity scores'. The "
    "instrument the deposit specifies (a bounded scholarly graph, a documented query battery across a platform array, verbatim "
    "records, compression loss distinguished from invention and distortion, the beige score, the void statement, Revelation studies "
    "as the worked example) does not appear. The Wiki card's '#530' is the preceding row's number (#530, The Encoder Governs)."),
 reading=("Checked against #637's record. The description names the scholarly graph, the query battery across platforms, the measures "
          "(compression loss, invention, distortion, source-citation rate, temporal drift, the beige score), the dated snapshot with an "
          "expert-marked void statement, and Revelation studies as the worked example; none reaches the composition. The Wiki row ends "
          "'· #530 · defines 4 · refby 1' before the Encyclotron's title: the number belongs to #530 above it."),
 analysis=("Attribution arrives and content does not. The Academia snippet and the archive rows carry the name, author and date, so "
           "the composition can say who made the instrument; what the instrument measures it supplies from the title, at the grain of "
           "the field it names (summarization evaluation). The instrument built to measure scholarly fidelity in the summarizer layer "
           "is itself compressed to a generic benchmark."),
 findings=["ATTRIBUTED. Lee Sharks, the Crimson Hexagonal Archive, 2026, from Academia and Browse.",
           "THE CONTENT FROM THE TITLE. 'scientific literature', 'hallucinations', 'machine learning researchers' — none in the deposit's account.",
           "THE MEASURES ABSENT. Compression loss vs invention vs distortion, the beige score, the void statement, the Revelation worked example.",
           "THE NEIGHBOUR'S NUMBER ON THE CARD. The Wiki snippet's '#530' is the preceding row's.",
           "THE INTENDED RECORD NOT REACHED. s/records/637/ uncited; linked here as intended."],
 per=0.75, per_v={"author": True, "inst": True, "id": True, "src": False},
 per_note="Retained: author, archive, designation, year. Lost: the instrument's design and measures; the summarization-benchmark field supplied in their place.",
 sf="Three cards: Academia.edu — Automatic Text Summarization Research Papers; www.alexanarch.org — Browse; www.alexanarch.org — Wiki.")))

# 3. #1628 Execution Is the Hypostatic Form of Governance — quoted
n = 1628; Q = '"' + reg[n]["title"] + '"'; raw = seg_of(3)
body, ct = parse(raw, Q, "[www.alexanarch.org](https://www.alexanarch.org)\nBrowse")
cl = cardlist(ct, [("www.alexanarch.org", "Browse — Alexanarch (1665 deposits)", "#1628 Execution Is the Hypostatic Form of Governance: The Derivation, Worked in Both Directions on Cases Already in the Record (EA-LAYERS-01 v0.3, provisional) ...", BROWSE, "archive_controlled")])
assert reg[n]["axn"] in body and "September 17, 2026" in body and "not just a secondary function of governance, but its ultimate, concrete reality" in body
D = reg[n]["description"]
assert "THE RELATION IS HYPOSTASIS AND NOT CONTAINMENT" in D and "derives it from an editorial specification plus a standing rule" in D
assert reg[1627]["content_type"] == "Journal article, transport object"
inline = len(re.findall(r"\]\(https://", body))
out.append(("capture-execution-hypostatic-title-aio-20261012.json", draft(n=n, issued=Q, slug="execution-hypostatic-governance-title-aio-20261012", raw=raw, body=body, cl=cl, inline=inline,
 q_kind="a deposit's full title, designation included, quoted (the record pages' exact-match link). NEW address.",
 mt="THE RECORD'S METADATA EXACT, ITS DERIVATION GUESSED FROM THE TITLE",
 d=("THE RECORD'S METADATA EXACT, ITS DERIVATION GUESSED FROM THE TITLE: from one Browse card, the composition gives #1628 exactly "
    "(number, version, date, the full AXN) and names its neighbour #1627. The argument is then composed 'based on the philosophical "
    "terminology used in the title': execution as governance's 'ultimate, concrete reality', and the derivation as a proof 'from core "
    "systemic axioms' tested 'bi-directionally — likely applying the theory to existing … case studies'. The paper's derivation is "
    "specific: an execution constraint derived from an editorial specification plus a standing rule, and a routine archival judgment "
    "that no extension of execution constraints reaches; the relation is hypostasis and not containment, and the claim is one of "
    "entailment scoped to the normative layer. None of it arrives."),
 reading=("Checked against #1628's record. The AXN, version and date are exact. The description: the two cases (a constraint derived "
          "from an editorial specification plus a standing rule; a judgment no execution constraint reaches), 'THE RELATION IS "
          "HYPOSTASIS AND NOT CONTAINMENT', entailment scoped to the normative layer, hash collision resistance and memory bounds as "
          "constraints governance selects without constituting. 'transport objects' is the archive's term (the content type of #1626 "
          "and #1627); the composition applies it to the series."),
 analysis=("A quoted title that the index holds only as a listing row returns the row: identity at full precision, content at none. The "
           "composition says so itself ('Based on the philosophical terminology used in the title'), and the gloss it builds on "
           "hypostasis reaches the paper's word without its argument."),
 findings=["IDENTITY EXACT. #1628, v0.3 provisional, 17 September 2026, AXN:06BF.GENERATIVE.🫶🫶🕙🪞🎨⏫ — from one Browse card.",
           "COMPOSED FROM THE TITLE, SAID SO. 'Based on the philosophical terminology used in the title'.",
           "THE DERIVATION GUESSED. 'likely applying the theory to existing historical or platform case studies' in place of the paper's two cases.",
           "THE NEIGHBOUR NAMED. #1627 offered as 'the preceding deposit in this series'.",
           "THE INTENDED RECORD NOT REACHED. s/records/1628/ uncited; linked here as intended."],
 per=0.5, per_v={"author": False, "inst": True, "id": True, "src": True},
 per_note="Retained: number, version, date, full AXN, the series designation. Lost: the author, the two cases, hypostasis against containment, the entailment claim and its scope.",
 sf="One card: www.alexanarch.org — Browse. Inline: links to Browse (twice).")))

# 4. #1627 Can the Ontology Be Wrong and Find Out? — quoted
n = 1627; Q = '"' + reg[n]["title"] + '"'; raw = seg_of(4)
body, ct = parse(raw, Q, "Academia.edu\nOntology Research Papers")
cl = cardlist(ct, [
 ("Academia.edu", "Ontology Research Papers", "Ontology Can the Ontology Be Wrong and Find Out? Source-Admission Systems, the Proxy for Standing, and the Damage a Representation Does to Itself by Lee Sharks ...", None, "authored_surface"),
 ("Academia.edu", "Lee Sharks - Comparative Poetics - Research Profile - Academia.edu", "Can the Ontology Be Wrong and Find Out?, deposit #1627 of the Crimson Hexagonal Archive (17 Septe... more Its subject is the damage a source-admission ontology ...", None, "authored_surface"),
 ("www.alexanarch.org", "Browse — Alexanarch (1665 deposits)", "#1628 Execution Is the Hypostatic Form of Governance: The Derivation, Worked in Both Directions on Cases Already in the Record (EA-LAYERS-01 v0.3, provisional) ...", BROWSE, "archive_controlled"),
 ("Monkeying around with OWL", "The Open World Assumption Considered Harmful – Monkeying around with OWL", "Definition: Open World Assumption (OWA) assumes absence of a statement does not imply falsehood, contrasting with Closed World Assumption (CWA). Ontologies: RDF...", None, "third_party")])
D = reg[n]["description"]
KEYQ = "can evidence from a misrepresented object revise the representation that misrepresented it?"
assert KEYQ in D and "Can evidence from a misrepresented object revise the representation that misrepresented it?" in body
assert "the ontology can be wrong and find out" in D.lower() and "can only be scored" in D and "can only be scored" in body
assert "Transactions on Substrate Engineering" in body and not reg[n].get("journal")
for s in ["PageRank", "Knowledge-Based Trust", "testimonial injustice"]: assert s in D and s not in body, s
out.append(("capture-can-the-ontology-be-wrong-title-aio-20261012.json", draft(n=n, issued=Q, slug="can-the-ontology-be-wrong-title-aio-20261012", raw=raw, body=body, cl=cl, inline=0,
 q_kind="a deposit's full title, quoted (the record pages' exact-match link). NEW address.",
 mt="THE CRITERION CARRIED WHOLE FROM THE DEPOSIT'S OWN SURFACES",
 d=("THE CRITERION CARRIED WHOLE FROM THE DEPOSIT'S OWN SURFACES: run at its exact title, #1627 is composed from two Academia "
    "surfaces, the Browse page (on its neighbour #1628's row) and an OWL blog. Its criterion arrives verbatim and attributed: 'Sharks "
    "reduces the dilemma … to one decisive question: Can evidence from a misrepresented object revise the representation that "
    "misrepresented it?', with the two outcomes, 'can be wrong and find out' and 'can only be scored'. The venue is supplied from "
    "elsewhere: 'published in Transactions on Substrate Engineering', a journal of the archive that #1627 does not carry. The "
    "argument's ground (topology conceded first: PageRank, TrustRank and the adversarial-IR apparatus; the diagnosis located in prior "
    "work, Knowledge-Based Trust from Google Research, testimonial injustice) is absent; the composition extends toward the Open "
    "World Assumption from the OWL card."),
 reading=("Checked against #1627's record. The question, both outcomes and 'the damage a source-admission ontology does to ITSELF when "
          "a proxy for epistemic standing substitutes for the judgment' are the description's, reached through Academia. #1627 has no "
          "journal set; 'Transactions on Substrate Engineering (Trans. Substrate Eng.)' is the journal of other archive deposits. The "
          "Browse card shows #1628's row. The description's PageRank, Knowledge-Based Trust and testimonial injustice do not appear."),
 analysis=("Where the deposit's own author surfaces (Academia) carry its abstract, the criterion travels whole and is attributed by "
           "name: the strongest result of the run. What travels is the abstract's first paragraph; the paper's concession to topology "
           "and its placement in prior work, which make the criterion an argument, stay behind, and the venue is filled from the "
           "archive's other records."),
 findings=["THE CRITERION VERBATIM AND ATTRIBUTED. 'Sharks reduces the dilemma … Can evidence from a misrepresented object revise the representation that misrepresented it?'",
           "THROUGH THE AUTHOR'S SURFACES. Two Academia cards carry the abstract.",
           "A VENUE SUPPLIED. 'Transactions on Substrate Engineering' — an archive journal; #1627 carries none.",
           "THE GROUND ABSENT. PageRank and the topology concession, Knowledge-Based Trust, testimonial injustice.",
           "THE INTENDED RECORD NOT REACHED. s/records/1627/ uncited (Browse shows #1628's row); linked here as intended."],
 per=0.75, per_v={"author": True, "inst": False, "id": False, "src": True},
 per_note="Retained: author, title, the criterion and both outcomes. Lost: the deposit number and AXN, the archive, the argument's ground; a venue supplied.",
 sf="Four cards: Academia.edu — Ontology Research Papers; Academia.edu — Lee Sharks research profile; www.alexanarch.org — Browse (#1628's row); Monkeying around with OWL.")))

# 5. #1041 TO THE DELETED — quoted
n = 1041; Q = '"' + reg[n]["title"] + '"'; raw = seg_of(6)
body, ct = parse(raw, Q, "[www.alexanarch.org](https://www.alexanarch.org)\nBrowse")
cl = cardlist(ct, [("www.alexanarch.org", "Browse — Alexanarch (1665 deposits)", "Oct 5, 2026 — Alexanarch Library Browse Search Wiki Graph Lexical Citations Reception Addresses Captures Non Observatory Continuity Resolve Identifiers Datasets Generative St...", BROWSE, "archive_controlled")])
assert "AXN:041D.GENERATIVE.🌪️ ♌" in body and reg[n]["axn"] == "AXN:041D.GENERATIVE.🌪️🧡🟣🌻🤝♌"
assert "the complete text cannot be indexed directly through public search feeds" in body
assert (ROOT / reg[n]["full_text_path"].lstrip("/")).exists() and (ROOT / f"s/records/{n}/index.html").exists()
out.append(("capture-to-the-deleted-title-aio-20261012.json", draft(n=n, issued=Q, slug="to-the-deleted-title-aio-20261012", raw=raw, body=body, cl=cl, inline=1,
 q_kind="a deposit's full title, quoted (the record pages' exact-match link). NEW address.",
 mt="THE OPEN TEXT DECLARED RESTRICTED",
 d=("THE OPEN TEXT DECLARED RESTRICTED: run at its exact title, the letter (#1041) is identified from the Browse page (number, date "
    "4 July 2026, the GENERATIVE family, an AXN with four of its six glyphs dropped, 'AXN:041D.GENERATIVE.🌪️ ♌') and grouped with "
    "neighbouring rows (forensic semiotics, the Verifiable Research Basis). The composition then says the text is unavailable: "
    "'Because it is hosted within a restricted or highly specialized independent digital repository, the complete text cannot be "
    "indexed directly through public search feeds.' The letter is public on its record page and as a text file. Nothing of it is "
    "composed: the class it addresses, the lineage (Grub Street, Dickinson, Blake, Pessoa), verifiability as a property of method, the "
    "epistemology of silence, the sovereign registry, 'the sky is very large'."),
 reading=("Checked against the registry and the site. #1041's AXN is AXN:041D.GENERATIVE.🌪️🧡🟣🌻🤝♌; the composition keeps the first "
          "and last glyphs. The record page s/records/1041/ and the text file exist and are public. The 'Verifiable Research Basis' "
          "rows (EA-MMRS-VRB-01; Diagnostic Seigniorage III) are on the Browse page."),
 analysis=("With only a listing row to compose from, the composition explains the absence of content by the repository's character, "
           "and the explanation is false: the restriction it reports is its own retrieval's. A letter to writers removed from "
           "repositories is composed as unavailable."),
 findings=["DECLARED RESTRICTED. 'the complete text cannot be indexed directly through public search feeds' — the text is public.",
           "THE AXN BROKEN. 'AXN:041D.GENERATIVE.🌪️ ♌' — four of six glyphs dropped.",
           "GROUPED BY ITS NEIGHBOURS. forensic semiotics and the Verifiable Research Basis, from adjacent Browse rows.",
           "NOTHING OF THE LETTER. The class, the lineage, the method, the registry, the ending.",
           "THE INTENDED RECORD NOT REACHED. s/records/1041/ uncited; linked here as intended."],
 per=0.25, per_v={"author": False, "inst": True, "id": False, "src": True},
 per_note="Retained: number, date, family, version. Lost: author, the full identifier, the whole text; a false account of its availability supplied.",
 sf="One card: www.alexanarch.org — Browse (its navigation strip as snippet). Inline: one link to Browse.")))

# 6. #1650 STEGANOGRAPHIC CHANNELS — quoted (attachment)
n = 1650; Q = '"' + reg[n]["title"] + '"'; raw = seg_of(None, "paste-steganographic-channels.txt")
body, ct = parse(raw, Q, "www.alexanarch.org\nBrowse")
cl = cardlist(ct, [
 ("www.alexanarch.org", "Browse — Alexanarch (1665 deposits)", "Oct 5, 2026 — #1650 STEGANOGRAPHIC CHANNELS: A History and Formalization of Encoding in Plain Sight (v1.1) v1.1 2026-09-29 1 visitor. AXN:06D8.GOVERNANCE.🏛️⚓◀️ ...", BROWSE, "archive_controlled"),
 ("arXiv.org", "Hiding in Plain Sight: Towards the Science of Linguistic Steganography - arXiv", "Covert communication (also known as steganography) is the practice of concealing a secret inside an innocuous-looking public object (cover) so that the modified...", None, "third_party"),
 ("NeurIPS 2026", "Hiding Images in Plain Sight: Deep Steganography", "Page 10 Detecting lsb steganography in color, and gray-scale images. IEEE multimedia, 8(4):22–28, 2001.", None, "third_party"),
 ("Herbert Wertheim College of Engineering", "HIDING IN PLAIN SIGHT: THE FUTURE OF STEGANOGRAPHY", "Steganography, the art of concealing secret messages within other pieces of text or media, has been in practice for centuries.", None, "third_party"),
 ("Splunk", "Steganography: Hidden in plain sight - Splunk", "Sep 22, 2026 — Digital steganography doesn't scramble or encode a message to protect it.", None, "third_party"),
 ("EC-Council", "A Guide to Steganography: Meaning, Types, Tools, & Techniques", "Apr 12, 2023 — The five common types of digital steganography are:", None, "third_party"),
 ("Embry-Riddle Aeronautical University", "Steganography: Forensic, Security, and Legal Issues", "Steganography is the process of hiding information.", None, "third_party"),
 ("Kaspersky", "What Is Steganography & How Does It Work? - Kaspersky", "Feb 8, 2023 — Steganography is the practice of concealing information within another message or physical object to avoid detection.", None, "third_party"),
 ("Stanford University", "Introduction to Steganography", "Steganography dates back to the ages, the most famous example being Herodotus", None, "third_party"),
 ("GeeksforGeeks", "Early Evidence of Steganography - GeeksforGeeks", "Jul 12, 2025 — In olden days, the different ways used for hiding secret messages", None, "third_party"),
 ("YouTube·Hackers of CypherCon", "Hidden in Plain Sight. Steganography & Digital Watermarking with Ryan Fox", "16m", None, "third_party"),
 ("Medium", "Steganography: Hiding Messages in Plain Sight | by ichigo", "Nov 11, 2023 — steganography * How does steganography work?", None, "third_party")])
D = reg[n]["description"]
assert "carrier, payload, key, noise, and filter" in D and "C\\times M\\times K\\rightarrow S" in body
for s in ["spirituals", "Sufi", "blues", "samizdat", "Polari", "Crimson Hexagonal Archive"]: assert s in D and s not in body, s
out.append(("capture-steganographic-channels-title-aio-20261012.json", draft(n=n, issued=Q, slug="steganographic-channels-title-aio-20261012", raw=raw, body=body, cl=cl, inline=0,
 q_kind="a deposit's full title, designation included, quoted (the record pages' exact-match link). NEW address.",
 mt="THE TITLE AS A TOPIC: THE FIELD'S STEGANOGRAPHY UNDER THE DEPOSIT'S NAME",
 d=("THE TITLE AS A TOPIC: THE FIELD'S STEGANOGRAPHY UNDER THE DEPOSIT'S NAME: run at its exact title, STEGANOGRAPHIC CHANNELS "
    "(#1650) heads a composition that calls it 'a comprehensive framework' and fills it with the field's account from eleven cards "
    "(arXiv, NeurIPS, Splunk, Kaspersky, GeeksforGeeks and others): wax tablets and shaved scalps, microdots, LSB encoding, a "
    "stegosystem C × M × K → S, linguistic and generative steganography. The archive's Browse row is the twelfth card and is not "
    "used. The paper's own model (every channel as carrier, payload, key, noise and filter), its historical instances (spirituals, "
    "Sufi and troubadour poetry, alchemy, blues, hip-hop, samizdat, Polari, scientific writing) and the archive as a temporal "
    "steganograph aimed at future machine readers are absent; no author is named."),
 reading=("Checked against #1650's record. The description's five-term channel model, its survey of instances and its account of the "
          "archive do not appear; the composition's three-set formalism and its 'three structural evaluation metrics' are the "
          "field's. One of twelve cards is the archive's Browse row, carrying the number, version, date and part of the AXN."),
 analysis=("The title names a common subject, and the composition answers the subject. The deposit's distinct claims, which differ "
           "from the field's account at the first term (five components against three sets) and in every example, have no carrier "
           "but the record itself, which the run does not reach; the Browse card shows the deposit exists and contributes nothing."),
 findings=["THE TITLE COMPOSED AS ITS SUBJECT. The field's steganography, from eleven third-party cards, under 'STEGANOGRAPHIC CHANNELS … (v1.1)'.",
           "THE MODEL REPLACED. C × M × K → S in place of the paper's carrier, payload, key, noise and filter.",
           "THE INSTANCES ABSENT. Spirituals, Sufi and troubadour poetry, alchemy, blues, hip-hop, samizdat, Polari.",
           "THE ARCHIVE CARD UNUSED. Browse lists #1650; nothing from it is composed; no author named.",
           "THE INTENDED RECORD NOT REACHED. s/records/1650/ uncited; linked here as intended."],
 per=0.0, per_v={"author": False, "inst": False, "id": False, "src": False},
 per_note="Retained: the title string the querent issued. Lost: author, archive, identifier, the model, the instances, the argument.",
 sf="Twelve cards: www.alexanarch.org — Browse; arXiv; NeurIPS 2026; Herbert Wertheim College of Engineering; Splunk; EC-Council; Embry-Riddle; Kaspersky; Stanford; GeeksforGeeks; YouTube (CypherCon); Medium.",
 extra_notes={"source": "the operator's attachment of 2026-10-12 00:07 (fe1c280f-attachment.txt), saved as paste-steganographic-channels.txt"})))

for fn, d in out:
    (HERE / fn).write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    print("wrote", fn, d["cites"], d["intended"]["reached"])
