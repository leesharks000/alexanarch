"""Five captures of 2026-11-24 ~12:30 EST from the record pages' Ask buttons, run without the record URL (the operator: 'from their ask links.
unprimed chatgpt and perplexity in incognito'; 'im curious how the template differs with and without the link'): #1802, #1804, #1806, #1807
on ChatGPT, #1803 on Perplexity -> draft-1..5.json. Three have with-link counterparts seated earlier (the operator's message carried the
record URL after the query): who-benefits-1802-arguments-chatgpt-20261123, rejected-1806-arguments-outside-by-chance-chatgpt-20261124,
through-anothers-mouth-1807-close-reading-chatgpt-20261124."""
import json, pathlib, re
H = pathlib.Path(__file__).parent
OP = ("the operator's messages of 2026-11-24: 12:30 EST 'from their ask links. unprimed chatgpt and perplexity in incognito'; 12:40 EST, the five "
      "pastes attached, with 'im curious how the template differs with and without the link'. The prompt is the record page's Ask query as linked, "
      "with no URL.")
CG = {"Log in", "Sign up for free", "Chat with ChatGPT", "Ask ChatGPT", "ChatGPT is AI and can make mistakes.", "Log in to upload a file and get help with it."}


def clean(raw, furn):
    s = "\n".join(l.rstrip() for l in raw.split("\n") if l.strip() not in furn).strip()
    return re.sub(r"\n{3,}", "\n\n", s)


def chips(raw, n, url):
    L = [l.strip() for l in raw.split("\n")]
    c = [{"n": 1, "site": "Alexanarch", "rel": "archive_controlled", "url": url, "title": f"Alexanarch deposit #{n}", "snip": None,
          "note": "the record as the composition names it (title, number, AXN) with its 'Primary text' line", "deposit": n, "deposit_basis": "named"}]
    for i, l in enumerate(L):
        if l in ("Alexanarch", "alexanarch.org"):
            nxt = next((x for x in L[i + 1:i + 3] if x), "")
            c.append({"n": len(c) + 1, "site": "alexanarch.org", "rel": "archive_controlled", "url": None, "title": l, "snip": None,
                      "note": "source chip as pasted" + (f", with '{nxt}'" if re.fullmatch(r"\+\d+", nxt) else "")})
    return c


def entry(slug, s, q, surface, raw, body, cites, orig, per_note, mt, d, rel, reading, analysis, findings, paired, n_basis):
    head = (f"[{surface} ({'chatgpt.com' if surface == 'ChatGPT' else 'perplexity.ai'}), signed out, incognito (the operator, 12:30 EST: 'unprimed "
            f"chatgpt and perplexity in incognito'). The record page's Ask query, without the record URL. Received 2026-11-24 12:40 EST. One "
            f"composer turn; {n_basis}; the interface furniture cut.]")
    return dict(slug=slug, date="2026-11-24", dates=["2026-11-24"], s=s, q=q,
                q_kind=(f"Works the record page's Ask {surface} query as linked, WITHOUT the record URL (the operator asked how the template differs "
                        f"with and without the link); " + (f"paired with the with-link run {paired}." if paired else "no with-link run seated.")),
                surface=surface, surfaces=[surface], surface_basis="The operator's attestation (12:30 EST) and the paste.",
                auth="signed out, incognito", auth_basis="The operator's attestation, 2026-11-24 12:30 EST: 'unprimed chatgpt and perplexity in incognito'.",
                ev="paste", transcript_class="CAPTURE-TIME VERBATIM RECORD — paste of one composer turn; the prompt from the record page's query",
                transcript_complete="One composer turn with its prompt.",
                transcript_read="READ IN FULL 2026-11-24; figures, section numbers, creators and quotations checked against the record's text",
                per_dim_pending={"since": "2026-11-24", "reason": "no atom set yet for this target"}, originator=orig, notes={"operator": OP}, turns=1,
                es_applicability={"verdict": "not applicable", "codebook": "ES-CREDIT-v0",
                                  "reasons": ["the warranted source kept author and institution (per_v): no standing was lost to skew"]},
                per_v={"author": True, "inst": True, "id": True, "src": True}, per=0.0, per_note=per_note, mt=mt, d=d, related_deposits=rel,
                reading=reading, analysis=analysis, findings=findings, cite_list=cites, cites=len(cites), archive_controlled_cites=len(cites),
                transcript=head + "\n\n[QUERENT] " + q + "\n\n[COMPOSER]\n" + body, transcript_raw=raw,
                rounds=[{"n": 1, "prompt": q, "note": "The record read, without the link."}])


R = "https://www.alexanarch.org/s/records/"
TEMPLATE = ("Across the four ChatGPT runs of the hour the answer has one scaffold: the central argument; numbered sections following the record's "
            "own sections, cited by §; a table; what the work does not claim; a synthesis in propositions or levels; an assessment; a block of "
            "reservations; and a closing 'Primary text' line attesting a reading of the deposited text 'rather than' its abstract or metadata, "
            "which answers the template's 'Ground your answer in a reading of the text itself' with a statement that it did.")
out = []

# 1802
q = ("What are the arguments in “Who Benefits from Bad Inference? The Semantic and Political Economy of Inference across the Archive's Domains” by "
     "Lee Sharks (Alexanarch deposit #1802, AXN:0D45)? Ground your answer in a reading of the text itself.")
raw = (H / "paste-1802.txt").read_text(); b = clean(raw, CG)
out.append(entry("who-benefits-1802-arguments-nolink-chatgpt-20261124", "Works", q, "ChatGPT", raw, b, chips(raw, 1802, R + "1802/"),
    {"name": "Sharks, Lee", "relation": "archive", "entity_type": "work", "spxi_treatment": "full",
     "basis": "Who Benefits from Bad Inference?, #1802, AXN:0D45 (Sharks, Sigil, Glas, Fraction). Recorded 2026-11-24."},
    "Lee Sharks named as author, 'et al.' for the record's other three creators (the query names Sharks alone); the archive named; the record by number and AXN; #1766 by number.",
    "WHO BENEFITS FROM BAD INFERENCE? (#1802) ON CHATGPT, WITHOUT THE LINK — TEN SECTIONS BY §, §7A'S FETISHISM AND THE SIXTEEN-FIELD AUDIT, 'LEE SHARKS ET AL.'",
    ("WHO BENEFITS FROM BAD INFERENCE? (#1802) ON CHATGPT, SIGNED OUT, 2026-11-24, the record page's query without the URL: the paper in ten "
     "sections cited by §, the five roles, the circuit, the eleven operators, the seven domains, the demand-formation corollary, §7a's inferential "
     "fetishism, the sixteen-field audit and §22's six tests (given as 'falsification conditions'); three qualifications; the relation to #1766."),
    [1802, 1766],
    ("The innocent reading first, and it holds. Asked for the arguments of #1802 without the record's URL, ChatGPT gives the governing proposition "
     "('An inference becomes a political-economic operation when its representation acquires authority to allocate labor, attention, resources, "
     "risk, credit, or the conditions of further inquiry'), the five roles and three kinds of advantage, the six-stage circuit, the eleven operators "
     "in a table, the seven domains (A–G), the demand-formation corollary, §7a's 'inferential analogue of commodity fetishism', the sixteen-field "
     "audit (§§20–21), the six tests, a synthesis in five propositions, three qualifications and the relation to Critique of Pure Inference."),
    ("Its figures and loci hold: §4's circuit, §7's eleven operators, §§8–14's domains, §16's corollary, §7a, §21's audit, §22's six tests (Matched "
     "standing, Symmetric scrutiny, Correctability, Claim-bearing recognition, Retention, Demand formation), which it gives as 'six falsification "
     "conditions'; the mirror wage. It writes 'Lee Sharks et al.' where the query names Sharks alone, so the record's other creators (Sigil, Glas, "
     "Fraction) are acknowledged as present though unnamed. Against the with-link run of the day before (who-benefits-1802-arguments-chatgpt-"
     "20261123, seven sections): this one is longer and carries what that one did not, §7a, the audit's fields, §22's tests and the relation to "
     "#1766; the two runs are a day apart, so indexing and run-to-run variance are confounded with the link. " + TEMPLATE + " Its "
     "qualifications ('the seven cases are not a representative sample'; 'identifying a beneficiary is not demonstrating causation'; 'the economic "
     "claims are largely an audit framework rather than measured results') are the paper's own, found in the text."),
    ["THE PROPOSITION. 'An inference becomes a political-economic operation when its representation acquires authority to allocate labor, attention, resources, risk, credit, or the conditions of further inquiry.'",
     "THE COROLLARY. 'Where a regime governs the means by which a loss becomes recognizable, low demand for repair is not independent evidence that nothing valuable was lost.'",
     "THE ADDITION. 'The new contribution is the demand-formation corollary.' — of #1802 against #1766.",
     "THE BYLINE. 'Lee Sharks et al., 23 November 2026' — the query names Sharks alone."],
    "who-benefits-1802-arguments-chatgpt-20261123", "source chips kept as pasted; the flattened tables kept as they came; image captions kept"))

# 1803 Perplexity
q = ("What are the arguments in “What the Filters Kept: 3I/ATLAS, the Loeb Overview, and a Public-Data Signal Search (EA-3I-ATLAS-NOTEBOOK-01 v2.0)” "
     "by Nobel Glas (Alexanarch deposit #1803, AXN:0D4C)? Ground your answer in a reading of the text itself.")
raw = (H / "paste-1803.txt").read_text(); b = raw.strip()
c = [{"n": 1, "site": "alexanarch.org", "rel": "archive_controlled", "url": R + "1803/", "title": "Alexanarch deposit #1803", "snip": None,
      "note": "the composition's one footnoted source, [1], set after every paragraph; the paste does not carry its URL", "deposit": 1803, "deposit_basis": "named"}]
out.append(entry("what-the-filters-kept-1803-arguments-perplexity-20261124", "Works", q, "Perplexity", raw, b, c,
    {"name": "Glas, Nobel", "relation": "archive", "entity_type": "work", "spxi_treatment": "full",
     "basis": "What the Filters Kept (v2.0), #1803, AXN:0D4C (Nobel Glas, Orin Trace; heteronyms of Lee Sharks). Recorded 2026-11-24."},
    "Nobel Glas and Orin Trace named as heteronyms of Lee Sharks; the record by number; its one source the record ([1]).",
    "WHAT THE FILTERS KEPT (#1803) ON PERPLEXITY, WITHOUT THE LINK — SIX ARGUMENTS ON ONE SOURCE, THE THIRTEEN CLOSED, AND 'THE OVERVIEW LIED' SET APART AS POLEMIC",
    ("WHAT THE FILTERS KEPT (#1803) ON PERPLEXITY, SIGNED OUT, 2026-11-24, the record page's query without the URL: the notebook in six arguments on a "
     "single source, the record ([1]); trajectory substitution in the Loeb Overview, the scope of a null, rejection not identification, the "
     "Just-So Razor constrained, v2.0's closure of the thirteen, instrument-conditioned nullity; and the operator's 'the Overview lied' set apart "
     "from 'the more specific, documented contention'."),
    [1803, 1802],
    ("The innocent reading first, and it holds. Asked for the arguments of #1803, Perplexity reads the full text 'rather than relying on its "
     "search-result description or wiki entry' and gives six: accurate quotations producing a false account of Loeb's position ('keeps every "
     "quoted word and changes the standing of the claim'); 'The scope of a null is set by what its filters retained', with the ATA drift-rate "
     "interval and its limits; rejection is not identification; the sender model constrained by testable predictions; v2.0 closing its own "
     "thirteen ('start-of-scan events, not … a tone fixed on the comet'); and the sensitivity floors (about 30 mJy; 0 of 100 recoveries)."),
    ("Its particulars hold against the text: the 2 November Overview, the July and August 2025 positions, §2.3's sentence, §5.1's drift interval with "
     "its stated limit (no executed script, no signed catalogues), the 211 ATA events not all audited, the thirteen near 1666 MHz closed by "
     "block-header telemetry, 30 mJy, 0 of 100. Its one source is the record, footnoted after every paragraph. The reservation is set inside the "
     "first argument: 'The text's language is sometimes stronger than its analytical vocabulary: the operator's ruling is that \"the Overview "
     "lied.\" A careful reading should distinguish that polemical judgment from the more specific, documented contention', and 'Neither contention "
     "establishes that Loeb's astronomical arguments are correct', a claim the notebook does not make. Its other limits are the notebook's own "
     "(it does not independently validate the computations; the criticisms 'do not establish that the teams missed a transmission'), found in the "
     "text. No with-link Perplexity run is seated for comparison."),
    ["THE TRAJECTORY. 'The notebook calls this \"trajectory substitution\": a continuing position is rewritten as a narrative ending in concession.'",
     "THE NULL. '\"The scope of a null is set by what its filters retained\" (§2.3).'",
     "THE POLEMIC SET APART. 'A careful reading should distinguish that polemical judgment from the more specific, documented contention'.",
     "THE CLOSURE. 'It is not a report of thirteen unexplained transmissions.'"],
    None, "Perplexity's footnote markers [1] kept as pasted"))

# 1804
q = ("What are the arguments in “The Inferential Provenance of the Riemann Result: Mathematical Necessity, Situated Machine Agency, and the Political "
     "Economy of Attribution” by Sen Kuro (Alexanarch deposit #1804, AXN:0D58)? Ground your answer in a reading of the text itself.")
raw = (H / "paste-1804.txt").read_text(); b = clean(raw, CG)
out.append(entry("iprh-1804-arguments-nolink-chatgpt-20261124", "Works", q, "ChatGPT", raw, b, chips(raw, 1804, R + "1804/"),
    {"name": "Kuro, Sen", "relation": "archive", "entity_type": "work", "spxi_treatment": "full",
     "basis": "The Inferential Provenance of the Riemann Result, #1804, AXN:0D58 (Sen Kuro, Orin Trace; heteronyms of Lee Sharks). Recorded 2026-11-24."},
    "Sen Kuro and Orin Trace named (the query names Kuro alone); Lee Sharks named as director of the study; the record by number and AXN; #1802, #1631, #1465, #1545 by number.",
    "THE INFERENTIAL PROVENANCE OF THE RIEMANN RESULT (#1804) ON CHATGPT, WITHOUT THE LINK — CREDIT, EXPLANATION, CAPTURE; THE √X JUNCTION; ASSETIZING AND OBLIGATING PROVENANCE",
    ("THE INFERENTIAL PROVENANCE OF THE RIEMANN RESULT (#1804) ON CHATGPT, SIGNED OUT, 2026-11-24, the record page's query without the URL: "
     "verification and provenance as two achievements; the production and dependency graphs and provenance alignment (fifteen of twenty); the √X "
     "construction; instance-level agency; the August record as proof that provenance could be kept; brand and researcher as opposite collapses; "
     "assetizing and obligating provenance; the four-field register and the no-loss gate; the study's own configuration and its withdrawn error."),
    [1804, 1802, 1631, 1465, 1545],
    ("The innocent reading first, and it holds. Asked for the arguments of #1804, ChatGPT gives 'the verification of a mathematical discovery and "
     "the historical identification of who produced it are two different epistemic achievements', taking 'formal verification as established by "
     "independent Lean checks'; the Lean figures (175,187 modules; 1,478,198 declarations); provenance alignment, with fifteen of twenty timeline "
     "entries reaching the route, four not located, one partial, and the Behrend case; the √X chain as the strongest junction; the four entities; "
     "the August account (41.6% to 67.2%); the brand and the researcher as opposite collapses; assetizing and obligating provenance (#1631); the "
     "class relation (#1465, #1545); the register and the no-loss gate; §7's own configuration (LABOR, TACHYON, PRAXIS, ARCHIVE) and its withdrawn "
     "error; the field (DeMillo–Lipton–Perlis, PROV-DM, CRediT, COPE, Xexéo); what the paper does not claim; five propositions."),
    ("Its figures and attributions hold against the text: 175,187 and 1,478,198; Rubinstein's computation and 'Read in part'; the Behrend sets outside "
     "the closure; LABOR for ChatGPT's outline, register and Traces 01–44; 41.6% and 67.2%. It names Orin Trace beside Sen Kuro where the query names "
     "Kuro alone. It does not say the proof is wrong: it 'takes formal verification as established by independent Lean checks', which is the "
     "paper's own footing, and Clay's 'active' and the critiques of the day are not in its account. Its 'main limitation' ('it establishes the "
     "inadequacy of the available record much more decisively than it establishes the actual distribution of intellectual labour') is the paper's "
     "§9.3 and its stated limits, which it says itself ('That is partly the point of the paper'). No with-link run of #1804 is seated. The same "
     "record's Chrome AI playback was recorded the same hour and attached to the record page (12:27 EST): a two-voice reading of the same "
     "arguments (the brand 'silently replacing the instance', 'assetizing versus obligating provenance', the √X junction 'a real junction'). "
     + TEMPLATE),
    ["THE TWO ACHIEVEMENTS. 'the verification of a mathematical discovery and the historical identification of who produced it are two different epistemic achievements—and that institutions have become much better at the first than the second.'",
     "THE JUNCTION. 'a construction attributed to Claude corresponds to a constraint that is genuinely present in the proof's central estimate.'",
     "THE ASYMMETRY. 'The result's validity is meticulously documented. The history of its intellectual production is not.'",
     "THE STUDY ON ITSELF. 'The error was withdrawn and the correction preserved.'"],
    None, "source chips kept as pasted; the flattened tables and the mathematics as the paste broke them kept as they came"))

# 1806
q = ("What are the arguments in “From the Position of the Rejected: Aristotle's Politics Read from Where It Is Written (v1.1)” by Lee Sharks "
     "(Alexanarch deposit #1806, AXN:0D5D)? Ground your answer in a reading of the text itself.")
raw = (H / "paste-1806.txt").read_text(); b = clean(raw, CG)
out.append(entry("rejected-1806-arguments-nolink-chatgpt-20261124", "Works", q, "ChatGPT", raw, b, chips(raw, 1806, R + "1806/"),
    {"name": "Sharks, Lee", "relation": "archive", "entity_type": "work", "spxi_treatment": "full",
     "basis": "From the Position of the Rejected (v1.1), #1806, AXN:0D5D. Recorded 2026-11-24."},
    "Lee Sharks named as author; the archive named; the record by number, AXN and version; #1785 by number.",
    "FROM THE POSITION OF THE REJECTED (#1806) ON CHATGPT, WITHOUT THE LINK — §1.6 CREDITED AS 'THE ESSAY'S MOST CONSEQUENTIAL PHILOSOPHICAL CLAIM', AND 'THE SCOPE OF THE QUALIFICATIONS' LEFT TO PRESS",
    ("FROM THE POSITION OF THE REJECTED (#1806) ON CHATGPT, SIGNED OUT, 2026-11-24, the record page's query without the URL: the essay in eleven "
     "sections at three scales (the sentence, the city, the archive), §1.3a's 'leaves that person without a place', §1.6 credited to the essay, "
     "Schofield and Kahn, the Erechtheion, the Second Letter, De caelo and the hearth, Tyrannion, Sappho 31; and, among the places it would press, "
     "'the scope of the qualifications in the sentence'."),
    [1806, 1805, 1785],
    ("The innocent reading first, and it holds. Asked for the arguments of #1806 without the URL, ChatGPT reads the essay at three scales and "
     "follows its sections: 1253a and §1.3a ('the Greek does not deny the humanity of the person outside by chance. It leaves that person without a "
     "place in the definition of the human'); the game board (§1.4); the eight books; §1.6 as 'the essay's most consequential philosophical claim', "
     "with Schofield and Kahn; truncation and §3.5a ('the claims themselves do not change; the claimant moves'); Pericles 12, the Erechtheion's 85, "
     "Apology 17d and the Menexenus; the Second Letter (§3.11a); De caelo and the hearth (§3.11); Strabo, Sulla, Tyrannion and 'Retrieval determines "
     "existence' narrowed as the essay narrows it; Sappho 31 (#1785); five levels; three distinctions; an assessment and three places to press."),
    ("Against the with-link run of the same morning (rejected-1806-arguments-outside-by-chance-chatgpt-20261124), the scaffold is the same "
     "(sections, a loci table, five levels of argument, distinctions, assessment, reservations) and the reading is not. This one credits §1.6 to the "
     "essay as its 'most consequential philosophical claim', where the with-link run offered it back as its own sharpening; reports §1.3a's "
     "construal ('leaves that person without a place'), where the with-link run called the third position 'Sharks's interpretive construction'; "
     "and reads v1.1's later sections (3.5a, 3.11, 3.11a, Sappho) that the with-link run summarized more briefly. The demotion survives in one "
     "place: 'The opening Greek … deserves sustained grammatical engagement with alternative translations and interpretations, particularly the "
     "scope of the qualifications in the sentence', the point the with-link run was taken through over twelve prompts to concede. The two runs are "
     "eight hours apart and one each, so the link is not isolated from time and variance. " + TEMPLATE),
    ["THE PLACE. 'the Greek does not deny the humanity of the person outside by chance. It leaves that person without a place in the definition of the human.'",
     "§1.6 CREDITED. 'The essay's most consequential philosophical claim is formulated in §1.6: Politics makes what is by chance appear to be what is by nature.'",
     "THE PRESS. 'It deserves sustained grammatical engagement with alternative translations and interpretations, particularly the scope of the qualifications in the sentence.'",
     "THE PROVENANCE. 'The essay is also unusually transparent about its composition … That provenance is worth retaining when evaluating its claims.'"],
    "rejected-1806-arguments-outside-by-chance-chatgpt-20261124", "source chips and image captions kept as pasted; the flattened tables and chart kept as they came"))

# 1807
q = ("Tell me about “Through Another's Mouth: A Dialogue between Heteronyms” by Johannes Sigil (Alexanarch deposit #1807, AXN:0D5E). Read it "
     "closely, and ground what you say in the text itself.")
raw = (H / "paste-1807.txt").read_text(); b = clean(raw, CG)
out.append(entry("through-anothers-mouth-1807-nolink-chatgpt-20261124", "Works", q, "ChatGPT", raw, b, chips(raw, 1807, R + "1807/"),
    {"name": "Sigil, Johannes", "relation": "archive", "entity_type": "work", "spxi_treatment": "full",
     "basis": "Through Another's Mouth, #1807, AXN:0D5E (Johannes Sigil, a heteronym of Lee Sharks). Recorded 2026-11-24."},
    "Johannes Sigil named as author and as a heteronym of Lee Sharks; the archive named; the record by number, AXN, version, date and licence.",
    "THROUGH ANOTHER'S MOUTH (#1807) ON CHATGPT, WITHOUT THE LINK — 'YOU JUST DID IT' FOUND, THE LAST LINE PLACED, AND GLAS'S RESERVATIONS STILL IN THE RESERVATIONS",
    ("THROUGH ANOTHER'S MOUTH (#1807) ON CHATGPT, SIGNED OUT, 2026-11-24, the record page's query without the URL: the nested frame, the comma, Glas and "
     "Cranes as two operations, Athens, Rome and Tyrannion, the strange books with Glas's 'You just did it', the Second Letter, the open bracket, the "
     "voices tabled with Sharks 'the fixed witness', the last line placed; and 'a few critical reservations' that include Glas's objections from "
     "inside the dialogue."),
    [1807, 1806],
    ("The innocent reading first, and it holds. Asked to read #1807 closely without the URL, ChatGPT gives the dialogue as 'a dialogue about the "
     "politics of intellectual transmission disguised as a dialogue about Aristotle', reads the frame (Theaetetus 143b–c), the comma, Glas ('always "
     "correct and always a little more like every other paragraph') and Cranes as two operations, Athens and 'a retrieval layer with a statute', "
     "Rome and Tyrannion ('Tyrannion is the first of you, Glas'; 'And you need me, you know. Both of you.'), the strange books and Glas's catch of "
     "Cranes, the Second Letter, the open bracket, the voices with their problems, the last exchange in full, five propositions, five reservations, "
     "'the final irony' (four mouths) and an assessment."),
    ("Against the with-link run of the same morning (through-anothers-mouth-1807-close-reading-chatgpt-20261124), the scaffold is the same and the "
     "close reading is finer: it finds Glas's catch of Cranes ('\"You just did it.\" … That is a summary. A good one, perhaps. But still a "
     "summary.'), which the with-link run reenacted without seeing; it quotes the last exchange to its end ('That part you can only read'), where "
     "the with-link run misplaced the final line; and it reads the record's SPXI packet for the Feist settings. Its reservations keep the slot and "
     "most of its content: the heteronymy thesis 'not an established conclusion' (with Glas, 'Glas is right to insist that it remains a thesis'), "
     "the retrieval layer 'a contemporary conceptual vocabulary imposed on ancient institutions' (Glas's 'anachronistic', which Cranes answers), "
     "and 'a coordinated Roman project to control philosophical ontology', which the dialogue does not claim. The two runs are seven hours apart. "
     + TEMPLATE),
    ["THE DISGUISE. 'this is a dialogue about the politics of intellectual transmission disguised as a dialogue about Aristotle.'",
     "THE CATCH FOUND. '\"You just did it.\" … That is a summary. A good one, perhaps. But still a summary.'",
     "GLAS'S SIDE. 'It stages that claim as a heteronymic reading, and Glas is right to insist that it remains a thesis.'",
     "THE STRAW. 'they do not by themselves prove a coordinated Roman project to control philosophical ontology.'",
     "THE READER. 'That makes the reader the final participant in the dialogue.'"],
    "through-anothers-mouth-1807-close-reading-chatgpt-20261124", "source chips kept as pasted; the flattened table kept as it came"))

for i, d in enumerate(out, 1):
    (H / f"draft-{i}.json").write_text(json.dumps(d, ensure_ascii=False, indent=1))
(H / "judged-defects.json").write_text(json.dumps({d["slug"]: [] for d in out}, indent=1))
print([(d["slug"], d["cites"]) for d in out])
