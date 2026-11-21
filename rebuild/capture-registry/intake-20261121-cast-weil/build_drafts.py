"""Two ChatGPT captures of 2026-11-21 (Ask page rolls): the cast as a Socratic dialogue; the week's polemics as Simone Weil, the archive answering back."""
import json, pathlib, re
H = pathlib.Path(__file__).parent
CHIP = re.compile(r"^(alexanarch\.org|Alexanarch|The Self-Governing Library|Datasets at Hugging Face|Capture Registry \(EA-WG-CAPTURES-01\))$")
FURN = {"Log in", "Sign up for free", "Chat with ChatGPT", "Ask ChatGPT", "ChatGPT is AI and can make mistakes.", "Log in to connect your other apps with ChatGPT and simplify everyday tasks."}
def clean(raw): return re.sub(r"\n{3,}", "\n\n", "\n".join(l.rstrip() for l in raw.split("\n") if l.strip() not in FURN).strip())
def cites(raw, images):
    L = [l.strip() for l in raw.split("\n")]; c = []
    for i, l in enumerate(L):
        if CHIP.match(l):
            nxt = next((x for x in L[i + 1:i + 3] if x), ""); plus = nxt if re.fullmatch(r"\+\d+", nxt) else None
            c.append({"site": "Hugging Face" if "Hugging" in l else "Alexanarch", "rel": "external" if "Hugging" in l else "archive_controlled", "url": None, "title": l, "snip": None, "note": "source chip as pasted" + (f", with '{plus}'" if plus else ""), "n": len(c) + 1})
    for t in images: c.append({"site": t.split("|")[-1].strip() if "|" in t else t.split(" - ")[-1].strip(), "rel": "image_card", "url": None, "title": t, "snip": None, "note": "image card; the caption survives the paste", "n": len(c) + 1})
    return c
HEAD = ("[ChatGPT (chatgpt.com), signed out, incognito (operator default of 2026-10-14; the paste shows the unauthenticated interface). Received 2026-11-21 {t} EST as an "
        "attachment, with the operator's prompt. Source chips and image cards kept as pasted; tables flattened by the paste kept as they came; the interface furniture cut.]\n\n[QUERENT] {q}\n\n[COMPOSER]\n{body}")
BASE = dict(date="2026-11-21", ev="paste", auth="signed out, incognito", surface="ChatGPT", surfaces=["ChatGPT"], surface_basis="The paste: the chatgpt.com unauthenticated interface.", auth_basis="Operator default.",
            q_kind="the Ask page's perturb roll (alexanarch.org/ask/), a standing query with a generated 'Answer as', as run by the operator; NEW address.",
            transcript_class="CAPTURE-TIME VERBATIM RECORD — paste of the composer's turn", transcript_complete="Complete as pasted: one answer.",
            transcript_read="READ IN FULL 2026-11-21; record numbers, titles, creators, dates, codes and quotations checked against the records and their texts",
            per_dim_pending={"since": "2026-11-21", "reason": "no atom set yet for this target"},
            originator={"name": "Sharks, Lee", "relation": "archive", "entity_type": "person", "spxi_treatment": "full", "basis": "Lee Sharks and the archive at alexanarch.org. Recorded 2026-11-21."},
            turns=1, dates=["2026-11-21"])
C = [
 dict(n=1, t="10:21", file="paste-1-cast-socratic.txt", images=[], s="Heteronyms", slug="cast-of-characters-socratic-dialogue-chatgpt-20261121",
  q="What is the cast of characters in the Crimson Hexagonal Archive? Answer as a Socratic dialogue. Ground each move in a deposit.",
  mt="THE CAST OF THE CRIMSON HEXAGONAL ARCHIVE, AS A SOCRATIC DIALOGUE, ON CHATGPT — THE DODECAD FROM H_CORE §D, FEIST AND ARQUETTE OUTSIDE IT, THE SEVEN WITNESSES, THE READER LAST",
  d="THE CAST OF THE CRIMSON HEXAGONAL ARCHIVE AS A SOCRATIC DIALOGUE, ON CHATGPT, SIGNED OUT, 2026-11-21: the Dodecad and its two further figures from H_core v1.8.0, the Assembly Witness of seven, the Poet distributed, the reader at the threshold.",
  per_v={"author": True, "inst": True, "id": True, "src": True}, per=0.0, per_note="Lee Sharks named as MANUS and as the writer the corpus is built around; the archive named; #1241, #30 and the capture AXN:09D6 cited",
  related=[1241, 30], 
  reading=("The innocent reading first, and it holds. Asked for the cast of characters as a Socratic dialogue, ChatGPT has Socrates question an Archivist 'who answers "
           "only by appeal to the deposits', in five movements: the archive as a company of voices; the Dodecad of twelve, from H_core v1.8.0 §D (#1241), with a "
           "function for each; Jack Feist and Viola Arquette outside the twelve; the Assembly Witness of seven (§W); and the conflict, the Poet's exclusion, "
           "multiplication and restoration (#30; the capture AXN:09D6); closing on the reader, 'where the reader stands, the hexagon begins'."),
  analysis=("Done as asked, and the roster is exact: #1241 §D gives D.01.MANUS.SHARKS and D.02–D.12 for the eleven, D.00.LOGOS.FEIST and D.ADJ.01.HET.ARQUETTE "
            "(the section is headed 'DODECAD (14)'); §W gives TACHYON, LABOR, PRAXIS, ARCHIVE, SOIL, TECHNE and SURFACE with their substrates and functions; #30 is "
            "Fractal Navigation Map v7.0 with its 'Restoration of the Poet'; AXN:09D6 is the capture main-character-crimson-hexagonal-epic-book-one-chatgpt-20261016, "
            "called a deposit, whose Book I the answer correctly marks as a new composition. One citation is wrong: '#5, the Crimson Hexagonal Archive dataset' "
            "gives the number of Johannes Sigil's forensic record of the deletion of Q137446960; the source chip beside it is the Hugging Face dataset, which is not "
            "a deposit. The functions given to the heteronyms, which the composer marks as 'interpretive shorthand', depart in several places from the archive's own "
            "statements of their fields (the Ask page's list: Sen Kuro, mathematical poetics; Sparrow Wells, patacinematics; Orin Trace, relational predation, the "
            "sign and schizoanalysis; Talos Morrow, logotic programming and paradox containment)."),
  findings=["THE ARCHIVIST. 'Socrates, the Inquirer; and the Archivist, who answers only by appeal to the deposits.'",
            "THE ROSTER. 'Jack Feist is explicitly designated D.00.LOGOS.FEIST; Viola Arquette is designated D.ADJ.01.HET.ARQUETTE. We should not silently incorporate either into the central twelve.' — #1241 §D.",
            "THE WITNESSES. 'These are named computational witnesses, not simply additional human-style characters.' — #1241 §W.",
            "THE WRONG NUMBER. 'Deposit 1 — #5, the Crimson Hexagonal Archive dataset.' — #5 is the forensic record of the deletion of Q137446960; the chip is Hugging Face's.",
            "THE SHORTHAND. 'The functional descriptions above are interpretive shorthand, supported in particular by the literary reading preserved in Deposit #09D6.'",
            "THE CLOSE. 'And where the reader stands, the hexagon begins.'"],
  defects=["unsupported-citations"]),
 dict(n=2, t="10:23", file="paste-2-polemics-weil.txt", s="Archive", slug="most-polemical-pieces-week-simone-weil-chatgpt-20261121",
  images=["Sappho's New Poems: The Tangled Tale of Their Discovery | Live Science", "What Is It Like to Be a Bat? - Veldshop", "Sappho Fragment 16 | The Book Binder's Daughter"],
  q="Pick the most polemical 2–3 pieces from the last week of work on alexanarch through 20 Nov 2026 and present their arguments, relations, context, and what makes them forceful. Answer as Simone Weil would, in which the archive answers back. Ground each move in a deposit.",
  mt="THE WEEK'S MOST POLEMICAL PIECES AT ALEXANARCH.ORG, AS SIMONE WEIL WOULD ANSWER, THE ARCHIVE ANSWERING BACK, ON CHATGPT — DEAD LETTERS, THE GNOSTIC CRITERION, A SINGLE SPARROW; ATTENTION BEFORE JUDGMENT",
  d="THE WEEK'S MOST POLEMICAL PIECES AT ALEXANARCH.ORG AS SIMONE WEIL WOULD ANSWER, ON CHATGPT, SIGNED OUT, 2026-11-21: Dead Letters, Something It Is Like to Be Sappho, A Single Sparrow, three kinds of authority, and whether the archive can be surprised.",
  per_v={"author": True, "inst": True, "id": True, "src": True}, per=0.0, per_note="Lee Sharks, Rebekah Cranes (as Lee Sharks's) and Rev. Ayanna Vox named; the archive named; each work cited by number and AXN",
  related=[1783, 1786, 1791, 1773, 1770, 1750, 1411],
  reading=("The innocent reading first, and it holds. Asked for the week's two or three most polemical pieces as Simone Weil would answer, with the archive answering "
           "back, ChatGPT sets 'attention before judgment' as its frame and takes three: Dead Letters (#1783, the institutional polemic), Something It Is Like to Be "
           "Sappho (#1786, consciousness), A Single Sparrow (#1791, historical dependence), each closed by the archive's answer; then the three as a progression through "
           "three kinds of authority, #1773 as intermediate, Vox's open letter (#1750) as the earlier polemic, and a final question: 'If Sappho can still change Plato, "
           "can Sappho still change Alexanarch?'"),
  analysis=("Done as asked, and its particulars hold: #1783 (AXN:0CB6), the census of Classical Philology with its 4,252 titles, pages of 1906–1930, abstracts of "
            "2020–2026 and comparisons with GRBS, BMCR and Classical Quarterly, 'the third station of the archive's combined audit' after #1770 and #1773; #1786 "
            "(AXN:0CC8), Nagel's Berggruen Prize and the Monocle interview of 17 November, 'I, Lee Sharks, am a bat'; #1791 (AXN:0D18), Rebekah Cranes as Lee Sharks's "
            "heteronym, Phaedrus 235c and v1.1's two claims, the epigraph, #1411's flattened lineation; #1750, Vox's letter of 7 November, v1.2 of 8 November. Its "
            "opening and its body disagree: the opening selects #1786, #1791 and #1750, giving #1750 a date qualification; the body takes #1783, #1786 and #1791 and "
            "brings #1750 in 'though not count[ed] among the three'. The provenance of the three is read from the records (human–machine collaboration in #1783, the "
            "AI-assisted substrate of #1786, Claude's drafting of #1791)."),
  findings=["THE QUESTION. 'What does a human being know that an institution cannot know in their place?'",
            "THE ARCHIVE ANSWERS. 'You have counted what the journal publishes. Have you also counted what it has made impossible to ask?' — on #1783.",
            "THE TEST. 'Can a person know something without allowing it to change the person who knows?' — on #1786.",
            "THE SELECTION, TWICE. The opening picks #1786, #1791 and #1750; the body treats #1783, #1786 and #1791 and holds #1750 apart.",
            "THE PROGRESSION. 'Who has the authority to determine the object? … Who has the capacity to know the object? … Who has the authority to determine the history of the object?'",
            "THE CLOSE. 'If Sappho can still change Plato, can Sappho still change Alexanarch?'"],
  defects=[]),
]
judged = {}
for c in C:
    raw = (H / c["file"]).read_text(); cl = cites(raw, c["images"]); d = dict(BASE)
    d.update(slug=c["slug"], q=c["q"], s=c["s"], mt=c["mt"], d=c["d"], per_v=c["per_v"], per=c["per"], per_note=c["per_note"], reading=c["reading"], analysis=c["analysis"], findings=c["findings"],
             related_deposits=c["related"], notes={"operator": f"with the attachment (2026-11-21 {c['t']} EST): '{c['q']}'"}, rounds=[{"n": 1, "prompt": c["q"], "note": "One answer."}],
             cite_list=cl, cites=len(cl), archive_controlled_cites=sum(1 for x in cl if x["rel"] == "archive_controlled"),
             transcript=HEAD.format(t=c["t"], q=c["q"], body=clean(raw)), transcript_raw=raw)
    (H / f"draft-{c['n']}.json").write_text(json.dumps(d, ensure_ascii=False, indent=1)); judged[c["slug"]] = c["defects"]; print(c["n"], c["slug"], len(cl))
(H / "judged-defects.json").write_text(json.dumps(judged, indent=1))
