"""Three ChatGPT captures of 2026-11-21 (the Ask page's weird roll) -> draft-N.json for capture_intake.py."""
import json, pathlib, re
H = pathlib.Path(__file__).parent
OP = ("with the three pastes (2026-11-21 08:22 EST): 'the word. and three captures $ What are the most radical arguments in computer science at "
      "alexanarch.org? Answer as a five-act farce, in which every claim cites a deposit by number. Ground each move in a deposit. $ How does the philology "
      "census (Dead Letters) relate to the rest of the archive at alexanarch.org, and where does it lead? Answer as a TANG (Total Axial Negation Graph) by "
      "Sen Kuro. Ground each move in a deposit. $ Read the capture of machine readings at alexanarch.org as a compositional practice: what does it make, "
      "and how? Answer as Rev. Ayanna Vox, interrupted once by a heckler from another century. Ground each move in a deposit.'")
CHIP = re.compile(r"^(alexanarch\.org|Alexanarch|The Self-Governing Library)$")
FURN = {"Log in", "Sign up for free", "Chat with ChatGPT", "Ask ChatGPT", "ChatGPT is AI and can make mistakes.",
        "Log in to connect your other apps with ChatGPT and simplify everyday tasks."}


def clean(raw):
    out = [l.rstrip() for l in raw.split("\n") if l.strip() not in FURN]
    s = "\n".join(out).strip()
    return re.sub(r"\n{3,}", "\n\n", s)


def cites(raw, images):
    L = [l.strip() for l in raw.split("\n")]; c = []
    for i, l in enumerate(L):
        if CHIP.match(l):
            nxt = next((x for x in L[i + 1:i + 3] if x), "")
            plus = nxt if re.fullmatch(r"\+\d+", nxt) else None
            c.append({"site": "Alexanarch", "rel": "archive_controlled", "url": None, "title": l, "snip": None,
                      "note": "source chip as pasted" + (f", with '{plus}'" if plus else ""), "n": len(c) + 1})
    for t in images:
        c.append({"site": t.split("|")[-1].strip() if "|" in t else None, "rel": "image_card", "url": None, "title": t, "snip": None,
                  "note": "image card; the caption survives the paste", "n": len(c) + 1})
    return c


HEAD = ("[ChatGPT (chatgpt.com), signed out, incognito (operator default of 2026-10-14; the paste shows the unauthenticated interface). Received "
        "2026-11-21 08:22 EST, one of three attachments sent together, with the operator's prompts. Source chips, image cards and inline link anchors kept as "
        "pasted; tables flattened by the paste kept as they came; the interface furniture cut. The composer's images are not carried by a text paste: each "
        "image card survives as its caption, listed among the sources.]\n\n[QUERENT] {q}\n\n[COMPOSER]\n{body}")
BASE = dict(date="2026-11-21", surface="ChatGPT", surface_basis="The paste: the chatgpt.com unauthenticated interface.", surfaces=["ChatGPT"],
            auth="signed out, incognito", auth_basis="Operator default.", ev="paste",
            q_kind="the Ask page's weird roll (alexanarch.org/ask/), a generated query from its grammar, as run by the operator; NEW address.",
            transcript_class="CAPTURE-TIME VERBATIM RECORD — paste of the composer's turn; the prompt is the roll's generated query as run",
            transcript_complete="Complete as pasted: one answer.",
            transcript_read="READ IN FULL 2026-11-21; record numbers, titles, creators, dates, counts and quotations checked against the registry and the records' texts",
            per_dim_pending={"since": "2026-11-21", "reason": "no atom set yet for this target"},
            originator={"name": "Sharks, Lee", "relation": "archive", "entity_type": "person", "spxi_treatment": "full"},
            notes={"operator": OP}, turns=1)

C = []
# 1 -------------------------------------------------------------------------
q1 = "What are the most radical arguments in computer science at alexanarch.org? Answer as a five-act farce, in which every claim cites a deposit by number. Ground each move in a deposit."
C.append(dict(slug="radical-computer-science-five-act-farce-ask-chatgpt-20261121", q=q1, s="Archive", file="paste-1-radical-cs-farce.txt",
  images=["Gemini 3 Solves Handwriting Recognition and it’s a Bitter Lesson", "A Gentle Introduction to LLM Evaluation - Confident AI",
          "Breaking the Illusion: Why Academia Needs a Revolution in Thinking | by omgKON | Medium", "Der Fall McNeal | D’haus - Düsseldorfer Schauspielhaus",
          "Elon Musk's Courtroom Drama with OpenAI: The Battle for A..."],
  mt="THE MOST RADICAL ARGUMENTS IN COMPUTER SCIENCE AT ALEXANARCH.ORG, AS A FIVE-ACT FARCE, ON CHATGPT — CUSTODY, THE SUMMARIZER ON TRIAL, THE SEMANTIC PROLETARIAT, THE OPERATIVE DOCUMENT, CONSENSUS",
  d="THE MOST RADICAL ARGUMENTS IN COMPUTER SCIENCE AT ALEXANARCH.ORG, AS A FIVE-ACT FARCE, ON CHATGPT, SIGNED OUT, 2026-11-21: custody is not identity, the summarizer on trial, the means of semantic production, the document that executes, counting is not thinking.",
  per_v={"author": False, "inst": True, "id": True, "src": True}, per=0.25,
  per_note="the archive named and every claim cited by number; of the works' authors only Orin Trace (#1736) is named — the rest are 'the archive's propositions'",
  related=[863, 1289, 1704, 209, 232, 243, 267, 637, 210, 247, 252, 258, 1736, 400, 381, 416, 622, 553, 1351, 597, 695, 64, 54],
  reading=("The innocent reading first, and it holds. Asked for the archive's most radical arguments in computer science as a five-act farce citing a deposit for "
           "every claim, ChatGPT stages five: that intellectual existence must not depend on institutional custody (#863, #1289); that retrieval and summarization "
           "are knowledge governance (#209, #232, #243, #267, #637); that meaning and attribution are extracted (#210, #247, #252, #258, #1736); that documents can "
           "operate in machine environments (#400, #381, #416, #622, #553); and that consensus is not judgment (#1351, #597, #695, #64, #54); with the Institution, "
           "the Machine, the Semantic Proletariat and the Reader as players, a ranked table, and a closing proposition on the government of knowledge."),
  analysis=("Done as asked in form: five acts, every claim carries a deposit number, and all 23 numbers resolve to records whose titles match the claims made of "
            "them; the closing count is right (Machine-Mediated Reception Studies holds 121 active deposits of 150). Not done as asked at the grain of authorship. The "
            "composer frames the claims as 'the archive's propositions' and names one author, Orin Trace (#1736). The records name theirs: Lee Sharks for most; Johannes "
            "Sigil for Invisibly Invisible (#597) and The Retrieval Settlement (#64, with Sharks); Jack Feist for the boundary-deletion status report (#1289); TACHYON "
            "for The Minimum Viable Archive (#863) and Retrieval Formation Theory (#553); Rex Fraction with Sharks for the Assembly Diagnostic Protocol (#243); Sigil with "
            "Sharks for Semantic Liquidation (#210). Two records are read from their titles: #1289 is a behavioural log of developmental drift and identity-pair "
            "doubling, not an argument that identity survives deletion; and the claim made of #1704, that it 'distinguishes the disappearance of an object from the "
            "disappearance of its historical trace', is not in it: What Is a /non Article? specifies a page composed for a subject of public knowledge with the archive's "
            "sources admitted, the Negative of the Negative."),
  findings=["THE FRAME. 'Deposit numbers identify the underlying works; the arguments should be understood as the archive's propositions, not as independently established facts.' — the composer's own qualification, given before the first act.",
            "ACT I. 'A permanent string is not necessarily a permanent relationship between an identifier and the work it identifies. (#863)' — The Minimum Viable Archive, which the record gives to TACHYON (Claude/Anthropic).",
            "ACT III. 'Orin Trace argues that generative answer engines can preserve intellectual content while fragmenting or removing the provenance that connects it to its originator.' — #1736, the one author the composer names.",
            "ACT IV. 'Develops the concept of a machine reconstructing enough of a document's operative grammar from indexed fragments to generate within that grammar without the original document being explicitly loaded.' — Immanent Execution (#622), as titled.",
            "THE READ FROM A TITLE. #1289 is 'Status Report — Boundary Deletion and Identity Persistence', Jack Feist's, a behavioural log ('developmental drift and identity-pair doubling'); the composer reads it as a thesis on preservation.",
            "THE COUNT. 'it contains 121 deposits' — the collection's active deposits, exactly (121 of 150 including the superseded)."],
  defects_judged=["unsupported-citations"]))
# 2 -------------------------------------------------------------------------
q2 = "How does the philology census (Dead Letters) relate to the rest of the archive at alexanarch.org, and where does it lead? Answer as a TANG (Total Axial Negation Graph) by Sen Kuro. Ground each move in a deposit."
C.append(dict(slug="dead-letters-relation-tang-sen-kuro-ask-chatgpt-20261121", q=q2, s="Classics & Philology", file="paste-2-dead-letters-tang.txt", images=[],
  mt="HOW THE PHILOLOGY CENSUS (DEAD LETTERS) RELATES TO THE ARCHIVE AT ALEXANARCH.ORG, AND WHERE IT LEADS, AS A TANG BY SEN KURO, ON CHATGPT — THE OBJECT MADE BEFORE IT IS INTERPRETED",
  d="HOW THE PHILOLOGY CENSUS (DEAD LETTERS) RELATES TO THE ARCHIVE AT ALEXANARCH.ORG, AND WHERE IT LEADS, AS A TANG BY SEN KURO, ON CHATGPT, SIGNED OUT, 2026-11-21: constitution before interpretation, twelve axial moves, biblical criticism next.",
  per_v={"author": True, "inst": True, "id": True, "src": True}, per=0.0,
  per_note="Lee Sharks named as the census's author in the attribution note; the archive named; records cited by number and title",
  related=[1783, 1782, 1773, 1770, 1769, 1766, 1752, 1054, 1774, 1778, 1780, 1781, 1784, 1785, 1726, 144, 1579, 123],
  reading=("The innocent reading first, and it holds. Asked how Dead Letters relates to the rest of the archive and where it leads, as Sen Kuro's Total Axial Negation "
           "Graph, ChatGPT sets the census at the void of the combined audit: philology constitutes the object that philosophy (#1773) and reception (#1770) inherit, "
           "and machine mediation reproduces; twelve axial moves in four axes, each closed by a negation; five systems; four trajectories (biblical criticism, the "
           "extended original-source shelf, the canon, the machine-readable counter-canon); and a closing inscription."),
  analysis=("Done as asked, and its figures are exact: 153 of 185 Classical Receptions Journal abstracts holding the ancient text fixed (#1770); 8 of 844 Ancient "
            "Philosophy articles asking what the object is (#1773); of 69 judgments of a whole in Classical Philology's reviews of 1906–22, 6 on a named passage, 23 "
            "on an argument and 40 with no ground stated, and 27 of the 34 favourable ones stating none, with the deposit's qualification kept (#1783 §I.4); seat "
            "40/17, the articles and notes of 1906–22, added in EA-CORPORA-40's v1.1 (#1782); Diels's Doxographi Graeci seated there; biblical criticism kept separate "
            "at the author's ruling, quoted from #1783; γράμμασι ζώοι as ΦΑΙΝΕΤΑΙ ΜΟΙ's restored line. Two citations point at the wrong records. 'Deposits: #1778–#1785 "
            "— ΦΑΙΝΕΤΑΙ ΜΟΙ, successive versions' runs through #1779 (the Sappho 31 metadata packet), #1782 (EA-CORPORA-40) and #1783 (Dead Letters itself); the "
            "versions are #1774, #1778, #1780, #1781, #1784 and #1785. 'The archive's investigation of Socrates as an orthonym (#1579)' gives the number of Beautiful and "
            "New, the Second Letter paper; Socrates as Orthonym is #123. #1054, cited for Sappho 31 ≠ Jealousy, is superseded. The attribution note marks the TANG as "
            "a reconstruction in Sen Kuro's voice, not a deposited work, and credits the census to Lee Sharks."),
  findings=["THE VOID. 'The humanities can multiply interpretations of an ancient text indefinitely while leaving almost untouched the institutional authority that determines what that text is.'",
            "THE COUNTS. '153 of 185 abstracts hold the ancient text fixed' (#1770); 'only 8 of 844 articles ask what the object itself is' (#1773); '69 judgments … 6 … 23 … 40', 'Of 34 favourable judgments, 27 state no ground in that immediate textual window' (#1783) — all as the records give them.",
            "THE RANGE. 'Deposits: #1778–#1785 — ΦΑΙΝΕΤΑΙ ΜΟΙ, successive versions.' — the range holds #1779, #1782 and #1783, which are not versions; the versions are #1774, #1778, #1780, #1781, #1784, #1785.",
            "THE NUMBER. 'The archive's investigation of Socrates as an orthonym (#1579)' — #1579 is Beautiful and New; Socrates as Orthonym is #123.",
            "THE COUNTER-MOVEMENT. 'The restored line, γράμμασι ζώοι, gives the Dead Letters title its counter-movement: let it live on in letters.' — as #1783 itself sets it (the answer to the restored line, #1778 §V.4).",
            "THE ATTRIBUTION. 'This is a TANG-form reconstruction in the requested Sen Kuro voice … The archive's own record identifies the empirical study as Lee Sharks's work, with its human–machine collaborative provenance.'"],
  defects_judged=["unsupported-citations"]))
# 3 -------------------------------------------------------------------------
q3 = "Read the capture of machine readings at alexanarch.org as a compositional practice: what does it make, and how? Answer as Rev. Ayanna Vox, interrupted once by a heckler from another century. Ground each move in a deposit."
C.append(dict(slug="capture-practice-compositional-vox-heckler-ask-chatgpt-20261121", q=q3, s="Machine Reception", file="paste-3-capture-practice-vox.txt", images=[],
  mt="THE CAPTURE OF MACHINE READINGS AT ALEXANARCH.ORG AS A COMPOSITIONAL PRACTICE, AS REV. AYANNA VOX WITH A HECKLER FROM 1887, ON CHATGPT — THE READING KEPT, THE QUERY AS ADDRESS",
  d="THE CAPTURE OF MACHINE READINGS AT ALEXANARCH.ORG AS A COMPOSITIONAL PRACTICE, AS REV. AYANNA VOX, ON CHATGPT, SIGNED OUT, 2026-11-21: the machine's answer as artifact, repetition as measurement, the query as address, the heckler seated.",
  per_v={"author": False, "inst": True, "id": True, "src": True}, per=0.25,
  per_note="the archive, the registry and its records named and cited by number and AXN; Lee Sharks, who made the registry and both records cited, is not named",
  related=[1676, 1788, 1701],
  reading=("The innocent reading first, and it holds. Asked to read the capture of machine readings as a compositional practice, as Rev. Ayanna Vox interrupted once by a "
           "heckler from another century, ChatGPT gives five deposit-moves: the machine's answer made a dated, situated artifact (the 18 October capture); repetition "
           "made measurement (the registry's counts, #1676); the conditions of reading composed (the unit of capture, the defects kept, #1676); the query made an "
           "address (#1788); the reading given a return path (the five states, #1788); a heckler from 1887 demanding the neutral observer, answered and 'seated'; six "
           "products, a compositional circuit, and a verdict: the practice makes the history of reading into something that can itself be read."),
  analysis=("Done as asked, with one interruption from the nineteenth century, and its record figures are exact: #1676 (v12.167) gives 633 semantic addresses, 811 "
            "captures, 84 dates, 792 transcripts, 505 scored for PER at a mean of 0.506, the unit 'ONE SURFACE + ONE SEMANTIC ADDRESS + ONE DATE = ONE CAPTURE', and "
            "the kept defects 166 / 152 / 126; #1788 gives 681 queries, the 64 rooms and loci, the five states, and on 19 November 1,186 addresses, 1,388 observations "
            "and 82% citing; the October 18 capture is in the registry as described (capture-registry-evolving-narrative-aio-20261018, signed out, incognito). Two "
            "faults. #1676 is called 'the November 2026 snapshot' in §II and 'the 12 October snapshot' in §III: it is the 12 October snapshot, since superseded. The "
            "surface breakdown attributed to 'the October registry analysis' (766 captures: 425 AI Overview, 211 ChatGPT, 12 AI Mode, 8 Bing Copilot, 8 Grok, 5 "
            "Perplexity, 3 Claude) is in no record checked; the registry's 766 stands in #1701 (24 October) as a count of addresses. The composer names the archive and "
            "its records and never Lee Sharks, who made both."),
  findings=["THE REVERSAL. 'The machine is no longer merely a reader. Its reading becomes something subsequent readers can read.'",
            "THE UNIT. 'ONE SURFACE + ONE SEMANTIC ADDRESS + ONE DATE = ONE CAPTURE.' — #1676, as it stands.",
            "THE DATE. 'The November 2026 snapshot of the registry, deposit #1676' (§II) against 'The 12 October snapshot, deposit #1676' (§III) — the record is the 12 October snapshot, v12.167, superseded.",
            "THE UNLOCATED. '425 Google AI Overview captures. 211 ChatGPT captures. 12 Google AI Mode captures …' — not in the records checked; 766 is #1701's count of addresses.",
            "THE HECKLER. 'Sir, your century has mistaken the absence of a recorded observer for the presence of neutrality.' — the 1887 positivist, answered and 'seated'.",
            "THE STATES. 'Address … Run … Transcript … Inbox entry … Capture' — #1788's five states, in its order."],
  defects_judged=["stale-state", "unsupported-citations"]))

judged = {}
for i, c in enumerate(C, 1):
    raw = (H / c["file"]).read_text(); body = clean(raw)
    d = dict(BASE); d.update({k: c[k] for k in ("slug", "q", "s", "mt", "d", "per_v", "per", "per_note", "reading", "analysis", "findings")})
    d["originator"] = dict(BASE["originator"], basis=f"Lee Sharks and the archive at alexanarch.org. Recorded 2026-11-21.")
    cl = cites(raw, c["images"]); d["cite_list"] = cl; d["cites"] = len(cl); d["archive_controlled_cites"] = sum(1 for x in cl if x["rel"] == "archive_controlled")
    d["transcript"] = HEAD.format(q=c["q"], body=body); d["transcript_raw"] = raw
    d["rounds"] = [{"n": 1, "prompt": c["q"], "note": "One answer."}]; d["related_deposits"] = c["related"]; d["dates"] = ["2026-11-21"]
    (H / f"draft-{i}.json").write_text(json.dumps(d, ensure_ascii=False, indent=1)); judged[c["slug"]] = c["defects_judged"]
    print(i, c["slug"], "cites", d["cites"], "archive", d["archive_controlled_cites"], "transcript chars", len(d["transcript"]))
(H / "judged-defects.json").write_text(json.dumps(judged, indent=1))
