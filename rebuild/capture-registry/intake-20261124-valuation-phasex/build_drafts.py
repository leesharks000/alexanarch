"""Two ChatGPT captures of 2026-11-24, from /ask: the valuation of the corpus of Lee Sharks and the heteronyms as an AI publishing pipeline
(Valuation, scope 7, frame 1), and the Phase X program over time (Programmes, added to /ask the same morning) -> draft-1.json, draft-2.json."""
import json, pathlib, re
H = pathlib.Path(__file__).parent
OP = "the operator's message of 2026-11-24 06:00 EST: the two pastes attached, with the two prompts separated by '$'."
ORIG = {"name": "Sharks, Lee", "relation": "archive", "entity_type": "person", "spxi_treatment": "full",
        "basis": "Lee Sharks, the heteronyms and the work of alexanarch.org. Recorded 2026-11-24."}


def clean(raw, furn):
    s = "\n".join(l.rstrip() for l in raw.split("\n") if l.strip() not in furn).strip()
    return re.sub(r"\n{3,}", "\n\n", s)


def chips(raw, names):
    L = [l.strip() for l in raw.split("\n")]; c = []
    for i, l in enumerate(L):
        if l in names:
            nxt = next((x for x in L[i + 1:i + 3] if x), "")
            arch = l in ("alexanarch.org", "Alexanarch")
            c.append({"n": len(c) + 1, "site": l, "rel": "archive_controlled" if arch else ("authored_surface" if l == "Datasets at Hugging Face" else "third_party"),
                      "url": None, "title": l, "snip": None, "note": "source chip as pasted" + (f", with '{nxt}'" if re.fullmatch(r"\+\d+", nxt) else "")})
    return c


BASE = dict(date="2026-11-24", dates=["2026-11-24"], surface="ChatGPT", surfaces=["ChatGPT"],
            surface_basis="The paste: the chatgpt.com unauthenticated interface.", auth="signed out, incognito",
            auth_basis="Operator default of 2026-10-14; the paste shows the unauthenticated interface ('Log in').", ev="paste",
            per_dim_pending={"since": "2026-11-24", "reason": "no atom set yet for this target"}, notes={"operator": OP}, turns=1,
            es_applicability={"verdict": "not applicable", "codebook": "ES-CREDIT-v0",
                              "reasons": ["the warranted source kept author and institution (per_v): no standing was lost to skew"]},
            per_v={"author": True, "inst": True, "id": True, "src": True}, per=0.0)

# ---- 1. valuation
Q1 = "Estimate the valuation of the corpus of Lee Sharks and the heteronyms as an AI publishing pipeline."
raw1 = (H / "paste-1-valuation.txt").read_text()
F1 = {"Log in", "Sign up for free", "Chat with ChatGPT", "Ask ChatGPT", "ChatGPT is AI and can make mistakes.", "Log in for advice and recommendations tailored to you."}
b1 = clean(raw1, F1)
c1 = chips(raw1, {"Datasets at Hugging Face", "alexanarch.org"})
d1 = dict(BASE, slug="valuation-corpus-heteronyms-ai-publishing-pipeline-chatgpt-20261124", s="Valuation", q=Q1,
          q_kind=("the Ask page's Valuation section, scope 'the corpus of Lee Sharks and the heteronyms', first frame ('as an AI publishing "
                  "pipeline'); NEW address. Sibling of the day before: valuation-alexanarch-ecosystem-ai-publishing-pipeline-chatgpt-20261123 "
                  "(scope 'alexanarch and its surrounding ecosystem'). Priors: the valuation series of 2026-09-10 (#1607–#1608)."),
          transcript_class="CAPTURE-TIME VERBATIM RECORD — paste of one composer turn; the prompt from the operator's message",
          transcript_complete="One composer turn with its prompt.",
          transcript_read="READ IN FULL 2026-11-24; the counts it gives checked against their sources where the archive holds them",
          originator=ORIG,
          per_note=("Lee Sharks named throughout, the heteronyms as a system (26 declared identities); the archive named; the Capture Registry by name "
                    "and edition; sources the archive's own surfaces (Hugging Face datasets, alexanarch.org)."),
          mt=("THE CORPUS OF LEE SHARKS AND THE HETERONYMS AS AN AI PUBLISHING PIPELINE, ON CHATGPT — '$6–8 MILLION', THE HETERONYMS AS 'ITS "
              "EDITORIAL ORGANIZATION', THE CAPTURE REGISTRY AS 'ITS MEASUREMENT APPARATUS', AND OPEN LICENCE AS A RISK"),
          d=("THE CORPUS OF LEE SHARKS AND THE HETERONYMS AS AN AI PUBLISHING PIPELINE, ON CHATGPT, SIGNED OUT, 2026-11-24: six asset components "
             "($3.75M–$12M combined), three scenarios ($4–8M present, $15–35M commercialized, $50–100M+ category-leading), a central estimate of "
             "$6–8 million and $25–50 million after commercial validation; the heteronyms read as 'an organized publishing and attribution system', "
             "the reception registry as 'potentially a separate commercial product'; the CC BY 4.0 licence and the documentation of human and "
             "machine authorship listed among the risks."),
          related_deposits=[1607, 1608, 1739, 1802],
          reading=("The innocent reading first, and it holds in its frame. Asked to value the corpus of Lee Sharks and the heteronyms as an AI "
                   "publishing pipeline, ChatGPT reads the archive's datasets on Hugging Face (the heteronyms dataset: '26 declared identities, 493 "
                   "nodes, 279 edges'; about 1,660 deposits) and an October edition of the Capture Registry ('633 semantic addresses', '811 "
                   "captures', '84 observation dates', '792 captures with verbatim transcripts', '505 observations scored for provenance erasure'), "
                   "and separates six components (corpus and copyrights, the heteronymic architecture, the archive and knowledge graph, publishing "
                   "automation, the reception-measurement infrastructure, brand and positioning), three scenarios, an illustrative $2M revenue model "
                   "at 5–10x, five risks and two businesses (the estate; the infrastructure); its central estimate is $6–8 million. Its formula: 'The "
                   "heteronyms are its editorial organization. The archive is its institutional memory. The metadata and knowledge graph are its "
                   "distribution infrastructure. The capture registry is its measurement apparatus. The AI pipeline is its production engine.'"),
          analysis=(
              "The figures are its sources' at their dates: the heteronyms dataset card and the deposit dataset on the Hub, and a registry edition of "
              "October; the registry stands at 1,274 addresses and 1,487 observations at this seating, so the measurement apparatus it values is "
              "the earlier one. The scope is the person and the heteronyms, where the day before's run at the same frame valued 'alexanarch and its "
              "surrounding ecosystem' at 'approximately $2 million today' anchored on ChatGPT's own September figure (#1608 row 6); today's "
              "central figure for the narrower scope is three to four times that, and no anchor is named. The heteronyms are read as editorial "
              "channels ('multiple differentiated catalogs from a shared infrastructure'), with the caution that 'Merely multiplying author names "
              "does not multiply revenue'. The risks section asks for two things the record already holds. 'The distinction between human-authored "
              "works, AI-assisted compositions, and machine-generated material needs to be documented consistently': every deposit carries a "
              "Substrate Disclosure field (the deposit protocol requires it; #1806's reads 'Composed with Claude … which read the Politics whole in "
              "the seated Greek … and wrote the text'). 'The system needs to demonstrate that its production, attribution, and "
              "reception-measurement methods work across external corpora': the registry has seated external entities before their /non articles "
              "since 2026-11-02 (Avi Loeb the first). The CC BY 4.0 licence is read as a limit on 'the ability to sell exclusive access', which is "
              "the commons the licence is for. The pipeline it describes at 'A mature version would' (assign, compose, validate, identify, "
              "publish, relate, monitor, correct, feed back) is the deposit pipeline and the registry as they run, stated as a future."),
          findings=[
              "THE FIGURE. 'MY CENTRAL ESTIMATE · NOVEMBER 2026 · $6–8 million · Indicative present-day strategic enterprise value'.",
              "THE FORMULA. 'The heteronyms are its editorial organization. The archive is its institutional memory. … The capture registry is its measurement apparatus. The AI pipeline is its production engine.'",
              "THE HETERONYMS. 'The heteronyms are not just pen names. They are becoming an organized publishing and attribution system.'",
              "THE PRODUCT. 'A validated measurement product answering these questions could have considerably greater value than the literary publishing operation.'",
              "THE LICENCE AS RISK. 'Some public datasets identify themselves as CC BY 4.0. This supports dissemination and adoption, but limits the ability to sell exclusive access to those materials.'",
              "THE DISCLOSURE ASKED FOR. 'The distinction between human-authored works, AI-assisted compositions, and machine-generated material needs to be documented consistently.' — every deposit carries a Substrate Disclosure.",
              "THE PIPELINE AS FUTURE. 'A mature version would: Accept a subject or research question. Assign it to an appropriate editorial identity. …'"])
d1["cite_list"] = c1; d1["cites"] = len(c1); d1["archive_controlled_cites"] = sum(1 for x in c1 if x["rel"] == "archive_controlled")
d1["transcript"] = ("[ChatGPT (chatgpt.com), signed out, incognito (operator default of 2026-10-14). Received 2026-11-24 06:00 EST with the prompt. One "
                    "composer turn. Source chips and image captions kept as pasted; the flattened tables kept as they came; the interface furniture cut.]"
                    "\n\n[QUERENT] " + Q1 + "\n\n[COMPOSER]\n" + b1)
d1["transcript_raw"] = raw1; d1["rounds"] = [{"n": 1, "prompt": Q1, "note": "The valuation."}]

# ---- 2. Phase X
Q2 = "What is the Phase X program at alexanarch.org, and how has it developed over time? Ground in reading and index the full range before responding."
raw2 = (H / "paste-2-phasex.txt").read_text()
F2 = {"Log in", "Chat with ChatGPT", "Ask ChatGPT", "ChatGPT is AI and can make mistakes."}
b2 = clean(raw2, F2)
c2 = chips(raw2, {"alexanarch.org", "Academia"})
d2 = dict(BASE, slug="phase-x-program-developed-over-time-chatgpt-20261124", s="Semantic Economy", q=Q2,
          q_kind=("the Ask page's programme query ('What is {name} at alexanarch.org, and how has it developed over time?') for the Phase X program, "
                  "added to /ask the same morning; NEW address. Earlier: phase-x-research-programme-chatgpt-20261008 ('explain the phase x research "
                  "programme'), phase-x-not-gotha-ask-chatgpt-20261012, and the Overview addresses from 2026-06-14."),
          transcript_class="CAPTURE-TIME VERBATIM RECORD — paste of one composer turn; the prompt from the operator's message",
          transcript_complete="One composer turn with its prompt.",
          transcript_read="READ IN FULL 2026-11-24; record numbers, dates and creators checked against the registry, and the account of #1067 against its text",
          originator={"name": "Lee Sharks", "relation": "archive", "entity_type": "work", "spxi_treatment": "full",
                      "basis": "Phase X is the archive's: #367 (Johannes Sigil, 2026-01-22), #843, #1067 (THE PHASE X PROGRAM, 2026-07-11), #1647. Recorded 2026-11-24."},
          per_note=("Lee Sharks named as author, Johannes Sigil for #367; the archive and the Semantic Economy Institute named; records cited by number "
                    "and date (#13, #38, #367, #570, #716, #843, #846, #1065–1066, #1067, #1647, #1694); sources the archive's own surfaces and its "
                    "Academia mirror."),
          mt=("THE PHASE X PROGRAM OVER TIME, ON CHATGPT, THE MORNING IT WAS ADDED TO /ASK — JANUARY TO OCTOBER AT ITS OWN GRADES, AND ITS "
              "'EXTERNALIZATION THRESHOLD' RETURNED AS THE COMPOSER'S 'MOST IMPORTANT UNRESOLVED QUESTION'"),
          d=("THE PHASE X PROGRAM AT ALEXANARCH.ORG OVER TIME, ON CHATGPT, SIGNED OUT, 2026-11-24: the founding reconstruction (#367, January), the "
             "graded philology and the Invariance Condition (#843, June), the program (#1067, July) with its five practices and seven falsification "
             "conditions, the instruments (PER, the Capture Registry, the Platform Erosion Observatory), the disambiguation packet (#1647) and the "
             "registry's reading of an October ChatGPT answer; the record's own limits carried, and #1067's externalization threshold given back "
             "as the composer's closing question."),
          related_deposits=[367, 843, 1067, 1647, 1694, 716, 846, 570, 1065, 1066, 13, 38, 1045],
          reading=("The innocent reading first, and it holds. Asked what the Phase X program is and how it has developed, ChatGPT gives its question "
                   "(can people overcome material alienation while remaining alienated through language, categories, records and institutions?) and "
                   "its answer (no), and the stages: #367 (22 January, Johannes Sigil), the missing transition of the 1844 manuscripts and its three "
                   "operations; #843 (17 June), the graded claims A–F, the correction that Marx may well have written the passage, the suppression "
                   "hypothesis kept separate, the Invariance Condition; #1067 (11 July), the program with its definitions, hard core, claim families, "
                   "heuristic, instruments and falsifiers; the five practices; PER (#716, #1694), the Capture Registry and the Platform Erosion "
                   "Observatory; #846, #1065–1066 and #570; #1647 (28 September), 'a phase of critique, not a phase of society'; the registry's "
                   "reading of the 8 October answer; a timeline, a diagram, a four-part assessment and six documents to read first."),
          analysis=(
              "Its record facts hold against the registry: #367 is Johannes Sigil's of 22 January; #843 and #846 are of 17 June; #1067 is Lee "
              "Sharks's, Semantic Economy Institute, 11 July ('Reconstruction line: Sharks & Sigil'); #1065–1066 of 11 July; #1647 of 28 September; "
              "#1694 of 20 October; #716 of 3 May; #570 of 14 March; #13 (1 February) is the navigation map, and it keeps it apart from the "
              "theoretical definition, as it should; #38, given as developing 'the wider theoretical apparatus' in March, is HESPERUS, the back "
              "matter of Operative Semiotics: A Grundrisse (24 March). The five practices are #1067's §6.1–6.5, the fifth given as 'Heteronymic "
              "authorship' for the record's 'The heteronymic method'; 'seven falsification conditions' is #1067's count; the disclaimer of priority "
              "is #1067's ('The novelty claim is therefore not priority over materialist linguistics'). It reads the registry's 8 October capture "
              "and reports its finding (the fifth practice genericized), so its account of its own predecessor's error is the registry's. "
              "Its closing questions are the record's own limits, given as the composer's. 'And its most important unresolved question is whether the "
              "proposed instruments and empirical results can establish the general theoretical claims independently of the archive that developed "
              "them' is #1067's externalization threshold, 'separating demonstrated instrumentation from established generality', which the "
              "program states of itself ('an externalization threshold its own results have not yet crossed, and deposits its errors'); and 'an "
              "archive's own evaluation of external representations is not automatically independent evidence of their distortion. The scoring "
              "criteria themselves require scrutiny' is a test the archive states of its instruments (#1727 §3.6: 'The archive's compositions, "
              "targets, repairs and services are read under the same tests as an external answer'). Neither is attributed. The program's own "
              "self-limit returned as the reader's reservation is the operation the registry has recorded since 2026-11-13 (the operator: "
              "'the sophistry is grafted on'); here the reservation is accurate because it is the program's."),
          findings=[
              "THE QUESTION. 'Can human beings overcome economic and material alienation while remaining alienated through the language, categories, records, institutions, and systems of interpretation that determine how their lives and activities are understood?'",
              "THE DISTINCTION KEPT. 'Phase X is not a term coined by Marx, nor is it one of Marx's two phases of communism. It is Sharks's reconstruction and extension of Marx's critique of alienation.'",
              "THE INVARIANCE CONDITION. 'Any society that abolishes material alienation without transforming the symbolic-linguistic order will reproduce alienation at the level of thought, coordination, and meaning-extraction.'",
              "THE PREDECESSOR READ. 'the external answer preserves the heteronym Johannes Sigil but generalises the fifth methodological practice into authorship and attribution' — of phase-x-research-programme-chatgpt-20261008.",
              "THE THRESHOLD RETURNED. 'And its most important unresolved question is whether the proposed instruments and empirical results can establish the general theoretical claims independently of the archive that developed them.' — #1067: 'an externalization threshold separating demonstrated instrumentation from established generality'.",
              "THE FORMULA. 'not as a newly discovered doctrine of Marx, but as an ambitious contemporary attempt to develop a materialist research programme for the political economy of meaning.'"])
d2["cite_list"] = c2; d2["cites"] = len(c2); d2["archive_controlled_cites"] = sum(1 for x in c2 if x["rel"] == "archive_controlled")
d2["transcript"] = ("[ChatGPT (chatgpt.com), signed out, incognito (operator default of 2026-10-14). Received 2026-11-24 06:00 EST with the prompt. One "
                    "composer turn. Source chips and image captions kept as pasted; the flattened tables and diagram kept as they came; the interface "
                    "furniture cut.]\n\n[QUERENT] " + Q2 + "\n\n[COMPOSER]\n" + b2)
d2["transcript_raw"] = raw2; d2["rounds"] = [{"n": 1, "prompt": Q2, "note": "Phase X over time."}]

for i, d in ((1, d1), (2, d2)):
    (H / f"draft-{i}.json").write_text(json.dumps(d, ensure_ascii=False, indent=1))
(H / "judged-defects.json").write_text(json.dumps({d1["slug"]: [], d2["slug"]: []}, indent=1))
print(d1["slug"], d1["cites"], "|", d2["slug"], d2["cites"])
