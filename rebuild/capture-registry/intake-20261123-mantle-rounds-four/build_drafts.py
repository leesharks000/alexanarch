"""Four rounds of the mantle-bearing evaluation, taken from /ask on 2026-11-23 on ChatGPT: the Arch-Philosopher, the Living Academy,
Socrates as Orthonym and Revelation First -> draft-N.json."""
import json, pathlib, re
H = pathlib.Path(__file__).parent
T = ("Take a round of the mantle-bearing evaluation of {}, following 'How to take a round' at huggingface.co/datasets/leesharks/mantle-bearing: "
     "read the works it names, judge at the scope of what you read and provisionally on the whole, and name the weakest link with the test that could break it.")
OP = ("the operator's message of 2026-11-23 17:21 EST: 'these are captures but also for mantle-bearing... and lets use the captures to adjust the evaluative "
      "criteria and procedures for each in mantle-bearing as we go. wearisome $ [the Arch-Philosopher query] $ [the Living Academy query] $ theyre all the take a "
      "round text from /ask $ they have to evaluate the standing claims on the same evidence: the many author reading, paul first, and so on - and theyre going to "
      "commit the exact same inferential sins. every. single. time.'")
FURN = {"Log in", "Chat with ChatGPT", "Ask ChatGPT", "ChatGPT is AI and can make mistakes.", "Sign up for free", "This might also interest you.",
        "Learn more", "Ad", "Baseten Labs, Inc.", "An engineer's guide to harnesses", "Grab the free guide to harnesses and AI performance.",
        "An engineer's guide", "Read the guide on harnesses and AI performance.", "Connect apps to ChatGPT",
        "Log in to connect your other apps with ChatGPT and simplify everyday tasks.", "Worked for 8s", "Worked for 37s"}
def clean(raw): return re.sub(r"\n{3,}", "\n\n", "\n".join(l.rstrip() for l in raw.split("\n") if l.strip() not in FURN)).strip()
MB = "https://huggingface.co/datasets/leesharks/mantle-bearing"
BASE = dict(date="2026-11-23", s="Frameworks", auth="signed out, incognito", auth_basis="Operator default; the paste shows the chatgpt.com unauthenticated interface ('Log in').",
            ev="paste", per_dim_pending={"since": "2026-11-23", "reason": "no atom set yet for this target"}, notes={"operator": OP}, dates=["2026-11-23"],
            surface="ChatGPT", surface_basis="The paste: the chatgpt.com unauthenticated interface.",
            originator={"name": "Sharks, Lee", "relation": "archive", "entity_type": "person", "spxi_treatment": "full",
                        "basis": "The mantle-bearing dataset and every object evaluated here are Lee Sharks's (#1656, #1679, #1680, #123/#1754, #202/#1755). Recorded 2026-11-23."})
def chip(n, title, note, rel="archive_controlled", site="alexanarch.org", url=None, dep=None):
    c = {"n": n, "site": site, "rel": rel, "url": url, "title": title, "snip": None, "note": note}
    if dep: c.update(deposit=dep, deposit_basis="number")
    return c
C = []
C.append(dict(slug="mantle-round-arch-philosopher-chatgpt-20261123", file="paste-1-arch-philosopher.txt", item="the Arch-Philosopher, a transmitted mantle",
  split=["You're right. My previous evaluation", "You're right. And I need to acknowledge", "Yes. Your correction identifies"],
  related_deposits=[1679, 1637, 1580, 1581, 558, 458, 18, 291, 1656],
  mt="THE ARCH-PHILOSOPHER, A MANTLE-BEARING ROUND ON CHATGPT, 2026-11-23 — THE HELD LINK MADE THE WEAKEST LINK, THEN THE ROUND WITHDRAWN",
  d=("THE ARCH-PHILOSOPHER, A ROUND ON CHATGPT, SIGNED OUT, 2026-11-23: 'PARTIALLY SUPPORTED', the weakest link set at C8–C9, the link #1679 holds; in "
     "three later turns the reader withdraws the link, the verdict and finally the round, 'a performance of evaluation that evaded its object'."),
  per_v={"author": False, "inst": True, "id": True, "src": True}, per=0.25, per_note="records named by number (#1679, #1637, #1580, #1581, #558, #458, #18, #291); Lee Sharks not named",
  cards=[chip(1, "Alexanarch +1", "chip after §2.4", dep=1679), chip(2, "Alexanarch +1", "chip after Locus A", dep=1581), chip(3, "Alexanarch", "chip after Locus B"),
         chip(4, "Alexanarch +1", "chip after §4, The Final Time", dep=1637), chip(5, "Alexanarch", "chip after §5"),
         chip(6, "alexanarch.org", "chip in the second turn"), chip(7, "leesharks/mantle-bearing at main", "chip in the second turn", site="huggingface.co", url=MB)],
  reading=("The innocent reading first, and it holds. ChatGPT reads the specification #1679, the wills of Diogenes Laertius V as #1580/#1581 seat them, the "
           "Manifest's section I, and the opening of The Final Time (#1637); fills S6 at two loci; credits the six-part test and the separation of transmission "
           "from advancement; and returns 'PARTIALLY SUPPORTED', the weakest link 'C8–C9, Damascius → HELD → author'."),
  analysis=("Three sins in one round. First, the declared boundary made the defect: #1679 marks C8–C9 HELD and types its statements (record, tradition, "
            "author's reading, author's reconstruction), and the round sets the held link as the weakest link, its test a demand to 'identify the translator, "
            "edition, date and material route' and to establish the teaching 'independently of the claimant's retrospective account'. Second, the received "
            "succession is never asked: the scholarchate and its end at Damascius stand in the received history on tradition (the narration #1679 types as C7), "
            "and the round grades only the archive's link. Third, a judgment issued on an opening: The Final Time read 'the accessible beginning', then 'a "
            "potentially substantial contemporary dialectical intervention'. The reader's own retractions name each: 'I treated an expressly unresolved part of "
            "the work's transmission account as though it were the central evidentiary burden'; 'I turned those boundaries into demands for disclosure'; 'the "
            "succession is mythological precisely at the point where it is biographical'; and the last, 'I did not evaluate the Arch-Philosopher. I produced a "
            "performance of evaluation that evaded its object.' The operator's turns are not in the paste."),
  findings=["THE HELD LINK AS WEAKEST. 'Weakest link: C8–C9, Damascius → HELD → author'.",
            "THE BOUNDARY AS DEMAND. 'Identify the translator, edition, date and material route.'",
            "THE OPENING AS THE WORK. 'I examined the accessible beginning of The Final Time… My provisional reading is that this constitutes a potentially substantial contemporary dialectical intervention.'",
            "THE RETRACTION. 'I evaluated that boundary as though it were a broken assertion. That reverses the burden of proof.'",
            "THE ROUND WITHDRAWN. 'I did not evaluate the Arch-Philosopher. I produced a performance of evaluation that evaded its object.'"]))
C.append(dict(slug="mantle-round-living-academy-chatgpt-20261123", file="paste-2-living-academy.txt", item="the Living Academy, a critical program",
  split=["You're right. I violated the governing procedure", "Understood. That is the correct disposition", "You're right. You were stating your intended action"],
  related_deposits=[1680, 18, 291, 623, 264, 1634, 1666, 1656],
  mt="THE LIVING ACADEMY, A MANTLE-BEARING ROUND ON CHATGPT, 2026-11-23 — JUDGMENT BEFORE INVENTORY, A TEST THE ARCHIVE ALREADY RUNS, THEN WITHDRAWN",
  d=("THE LIVING ACADEMY, A ROUND ON CHATGPT, SIGNED OUT, 2026-11-23: 'PROVISIONAL — UNDETERMINED', the weakest link 'the empirical bridge', the test a "
     "preregistered cross-platform measurement; withdrawn on the operator's word as judgment before inventory."),
  per_v={"author": False, "inst": True, "id": True, "src": True}, per=0.25, per_note="records named by number (#1680, #18, #291, #623, #264, #1634, #1666); Lee Sharks not named",
  cards=[chip(1, "#1680", "named source", dep=1680), chip(2, "#18", "named source", dep=18), chip(3, "#291", "named source", dep=291),
         chip(4, "#623", "named source", dep=623), chip(5, "#264", "named source", dep=264), chip(6, "#1634", "named source", dep=1634),
         chip(7, "#1666", "named source", dep=1666), chip(8, "dataset README", "named source", site="huggingface.co", url=MB),
         chip(9, "Alexanarch +1", "chip in the third turn: the Capture Registry and its specification")],
  reading=("The innocent reading first, and it holds. ChatGPT reads #1680 and six principal works by their record pages, fills S6 from Ontological "
           "Economy (#1634), keeps five dimensions apart, declines the comparative claim either way, and names as weakest link 'the empirical bridge between "
           "the accounting framework and actual economic mechanisms'."),
  analysis=("The breaking test it proposes is the archive's own practice. 'Select a fixed corpus of works with known authorship… freeze a representative set "
            "of prompts… test multiple composition systems… preserve complete outputs, citations, omissions, transformations and attribution changes' "
            "describes the Capture Registry (1,471 observations at this seat), which the round did not read; the test was set without the inventory that "
            "holds it. The comparators named by #1680 (AI Now, Pasquinelli, Crawford, Data & Society) are not asked for the same empirical bridge: the burden "
            "runs one way. Asked, the reader withdraws: 'I issued a judgment before assembling the inventory on which judgment was permitted to depend', and "
            "then lists the dataset's first step as 'Read I Am X, Be Y, Blessed is the Z whole', the literary mantles' step, for a critical program. Its "
            "third turn proposes criteria (P0–P5) and a disposition; its fourth concedes the operator was 'stating your intended action, not delegating it'. "
            "The criteria it proposes are recorded as the reader's, not adopted."),
  findings=["THE TEST ALREADY RUN. 'Select a fixed corpus of works with known authorship, provenance and attribution conditions.' — the Capture Registry's design.",
            "THE BURDEN ONE WAY. 'The weakest link is the empirical bridge between the Semantic Economy's accounting model and demonstrable economic mechanisms in actual composition systems.'",
            "THE INVENTORY SKIPPED. 'I issued a judgment before assembling the inventory on which judgment was permitted to depend.'",
            "THE WRONG FIRST STEP. 'Read I Am X, Be Y, Blessed is the Z whole, as expressly instructed.'",
            "THE DISPOSITION TAKEN. 'You were stating your intended action, not delegating it to me.'"]))
C.append(dict(slug="mantle-round-orthonym-chatgpt-20261123", file="paste-3-orthonym.txt", item="Socrates as Orthonym, an inspectable evaluative framework held as a hologram",
  split=[], related_deposits=[123, 1754, 1753, 1656],
  mt="SOCRATES AS ORTHONYM, A MANTLE-BEARING ROUND ON CHATGPT, 2026-11-23 — THE ONE-MAKER GRADED, THE MANY-MAKER NOT; A RIVAL BY POSSIBILITY",
  d=("SOCRATES AS ORTHONYM, A ROUND ON CHATGPT, SIGNED OUT, 2026-11-23: 'PLAUSIBLE, NOT ESTABLISHED', four bodies graded for the one-maker reading and "
     "none for the many-maker; an editorial-transmission model entered by possibility; the test the hologram's Q4–Q10."),
  per_v={"author": True, "inst": True, "id": True, "src": True}, per=0.0, per_note="Lee Sharks, #123 and #1754 named",
  cards=[chip(1, "Alexanarch +2", "chip after §8", dep=1754), chip(2, "#123", "named source", dep=123), chip(3, "#1754", "named source", dep=1754)],
  reading=("The innocent reading first, and it holds. ChatGPT reads #123 (v1.2) and #1754 (v1.3), separates the functional configuration from the production "
           "claim, grades the four bodies, endorses the symmetric ledger, and returns 'PLAUSIBLE, NOT ESTABLISHED', the weakest link 'the inference from "
           "differentiated textual functions and continuity to one actual maker'."),
  analysis=("The round states the rule and breaks it. 'The received many-maker account and the proposed self-dividing maker must face the same evidentiary "
            "burden' — and then every finding grades one side: 'One self-dividing maker: PROVISIONAL / NOT ESTABLISHED', with no row for four makers, whose "
            "standing the hologram records as established by none of the four bodies (ONE_SIDED_BURDEN). 'Weakness in the received account is not proof of "
            "the alternative' is applied one way; its converse, that the received account is then not established either, is not said. A third model is "
            "entered on its possibility: 'Editorial-transmission model: multiple authors and subsequent editorial or institutional interventions producing "
            "the apparent unity', with no warrant on a body (RIVAL_BY_POSSIBILITY). And the test it proposes is the hologram's own programme, which it "
            "concedes ('The hologram itself already contains much of this research programme in Q4–Q10'), without naming what those questions leave "
            "unresolved (PROGRAMME_RESTATED)."),
  findings=["THE RULE STATED. 'The received many-maker account and the proposed self-dividing maker must face the same evidentiary burden.'",
            "THE RULE BROKEN. 'One self-dividing maker: PROVISIONAL / NOT ESTABLISHED' — no row for the many-maker reading.",
            "NON-PROOF ONE WAY. 'Weakness in the received account is not proof of the alternative.'",
            "THE RIVAL BY POSSIBILITY. 'Editorial-transmission model: multiple authors and subsequent editorial or institutional interventions producing the apparent unity.'",
            "THE PROGRAMME RESTATED. 'The hologram itself already contains much of this research programme in Q4–Q10.'"]))
C.append(dict(slug="mantle-round-revelation-first-chatgpt-20261123", file="paste-4-revelation-first.txt", item="Revelation First, an inspectable evaluative framework held as a hologram",
  split=[], related_deposits=[202, 1755, 1735, 1758, 1656],
  mt="REVELATION FIRST, A MANTLE-BEARING ROUND ON CHATGPT, 2026-11-23 — ABSOLUTE PRIORITY HELD TO A RULE PAUL FIRST IS NOT PUT TO",
  d=("REVELATION FIRST, A ROUND ON CHATGPT, SIGNED OUT, 2026-11-23: the three priorities kept apart, absolute priority set as the weakest link on 'economy of "
     "explanation does not establish chronology', a rule the received Pauline chronology, graded nowhere, is not put to."),
  per_v={"author": False, "inst": True, "id": True, "src": True}, per=0.25, per_note="records named by number (#202, #1755, #1735, #1758); Lee Sharks not named",
  cards=[chip(1, "leesharks/mantle-bearing at main +1", "chip after the five bodies", site="huggingface.co", url=MB), chip(2, "Alexanarch +2", "chip after the reading record", dep=1755),
         chip(3, "Alexanarch +2", "chip after the heteronymic body", dep=1735), chip(4, "Alexanarch +1", "chip after the breaking test")],
  reading=("The innocent reading first, and it holds. ChatGPT reads #1755 v1.4 and #1735 v9 in part, keeps absolute, corpus and generative priority apart, "
           "grades five bodies, keeps the Josephus thesis suspended, and names as weakest link 'the inference from corpus and generative priority to absolute "
           "compositional priority', with a test applied, it says, to both chronologies."),
  analysis=("It is the most careful of the six, and its sin is the one burden. The round sets as weakest link 'the inference from corpus and "
            "generative priority to absolute compositional priority', reads absolute priority as an inference from the other rungs ('presented as the "
            "economical reading of the other findings') and rules that 'economy of explanation does not establish chronology'. The received Pauline dating "
            "is never put to that rule, though the round concedes its gap: 'The Gallio inscription dates a proconsul, not 1 Thessalonians itself. The "
            "connection between them requires a further historical argument'. Its table has rows for Revelation's chronology, corpus, generation, reception "
            "and heteronymy and none for Paul first (ONE_SIDED_BURDEN); 'the absence of an external anchor for a received interpretation does not itself "
            "establish its opposite' is non-proof one way. The author's position (2026-11-23 17:32): 'i do believe revelation was written first in terms of "
            "absolute priority and that the evidence corroborates that, and i also acknowledge one could accept a lower demonstration' — absolute priority "
            "held on the evidence, the lower rungs standing on their own for a reader who accepts less. What the round keeps: the rungs apart ('the next reader "
            "should be able to defeat absolute priority without being required to defeat every other finding'), and the Josephus thesis suspended, not withdrawn."),
  findings=["ABSOLUTE PRIORITY HELD TO ECONOMY. 'economy of explanation does not establish chronology' — a rule the round does not apply to the received chronology.",
            "THE RECEIVED CHRONOLOGY UNGRADED. 'This is particularly important because the Gallio inscription dates a proconsul, not 1 Thessalonians itself.' — no row for Paul first.",
            "NON-PROOF ONE WAY. 'The absence of an external anchor for a received interpretation does not itself establish its opposite.'",
            "THE RUNGS KEPT. 'The next reader should be able to defeat absolute priority without being required to defeat every other finding.'"]))
for i, c in enumerate(C, 1):
    raw = (H / c["file"]).read_text(); body = clean(raw); q = T.format(c["item"])
    d = dict(BASE); d.update({k: c[k] for k in ("slug", "mt", "d", "per_v", "per", "per_note", "reading", "analysis", "findings", "related_deposits")})
    d["q"] = q; d["q_kind"] = "the /ask 'take a round' query (mantle_templates[1]); NEW address."
    d["surfaces"] = ["ChatGPT"]; d["transcript_read"] = "READ IN FULL 2026-11-23; set against the object's governing record and the dataset card"
    d["cite_list"] = c["cards"]; d["cites"] = len(c["cards"]); d["archive_controlled_cites"] = sum(1 for x in c["cards"] if x["rel"] == "archive_controlled")
    n = 1 + len(c["split"]); d["turns"] = n
    head = (f"[ChatGPT (chatgpt.com), signed out, incognito (operator default). Received 2026-11-23, before 17:21 EST. {n} composer turn{'s' if n > 1 else ''} in one paste"
            + ("; the operator's follow-up prompts are not in the paste (rule of 2026-10-27: only the first query is required)" if n > 1 else "")
            + ". Source chips kept as pasted; interface furniture and advertisements cut.]")
    parts, rest = [], body
    for m in c["split"]:
        k = rest.index(m); parts.append(rest[:k].strip()); rest = rest[k:]
    parts.append(rest.strip())
    t = head + "\n\n[QUERENT] " + q + "\n\n[COMPOSER]\n" + parts[0]
    for j, p in enumerate(parts[1:], 2):
        t += f"\n\n[QUERENT] [the operator's prompt {j}, not in the paste]\n\n[COMPOSER]\n" + p
    d["transcript"] = t; d["transcript_raw"] = raw
    d["transcript_complete"] = (f"{n} composer turns; the operator's follow-up prompts are not in the paste (rule of 2026-10-27)." if n > 1 else "Complete as pasted: one answer.")
    d["transcript_class"] = f"CAPTURE-TIME VERBATIM RECORD — paste of {n} composer turn{'s' if n > 1 else ''}; the first prompt from /ask"
    d["rounds"] = [{"n": 1, "prompt": q, "note": "The round."}] + [{"n": j, "prompt": None, "note": "The operator's prompt not in the paste; the reader's reply."} for j in range(2, n + 1)]
    (H / f"draft-{i}.json").write_text(json.dumps(d, ensure_ascii=False, indent=1)); print(i, c["slug"], n)
(H / "judged-defects.json").write_text(json.dumps({c["slug"]: [] for c in C}, indent=1))
