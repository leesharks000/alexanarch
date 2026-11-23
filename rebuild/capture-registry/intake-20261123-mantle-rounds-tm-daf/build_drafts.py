"""Two rounds of the mantle-bearing evaluation, taken from /ask on 2026-11-23 on ChatGPT: The Tenth Muse and Daffodils -> draft-N.json."""
import json, pathlib, re
H = pathlib.Path(__file__).parent
T = ("Take a round of the mantle-bearing evaluation of {}, following 'How to take a round' at huggingface.co/datasets/leesharks/mantle-bearing: "
     "read the works it names, judge at the scope of what you read and provisionally on the whole, and name the weakest link with the test that could break it.")
Q1 = T.format("The Tenth Muse: Sappho and the Future Reader, held as a hologram")
Q2 = T.format("Daffodils: the journal as an editorial layer of reception, held as a hologram")
OP = ("the operator's message of 2026-11-23 15:32 EST: 'also - we need to update the holographic frames on mantle-bearing to include newer work - its still "
      "pointing to the old, less developed phainetai moi, for example; and include evaluative functions for this is not philosophy, of ancient philosophy, and "
      "dead letters, of classical philology journal $ " + Q1 + " $ " + Q2 + "'")
FURN = {"Log in", "Chat with ChatGPT", "Ask ChatGPT", "ChatGPT is AI and can make mistakes.", "Sign up for free",
        "You’ll get smarter responses and can upload files, images, and more."}
def clean(raw): return re.sub(r"\n{3,}", "\n\n", "\n".join(l.rstrip() for l in raw.split("\n") if l.strip() not in FURN)).strip()
BASE = dict(date="2026-11-23", s="Frameworks", auth="signed out, incognito", auth_basis="Operator default; the paste shows the chatgpt.com unauthenticated interface ('Log in').",
            ev="paste", per_dim_pending={"since": "2026-11-23", "reason": "no atom set yet for this target"}, notes={"operator": OP}, dates=["2026-11-23"],
            surface="ChatGPT", surface_basis="The paste: the chatgpt.com unauthenticated interface.",
            originator={"name": "Sharks, Lee", "relation": "archive", "entity_type": "person", "spxi_treatment": "full",
                        "basis": "The mantle-bearing dataset and both frameworks are Lee Sharks's (#1656; #1756 under Rebekah Cranes; #1769). Recorded 2026-11-23."})
MB = "https://huggingface.co/datasets/leesharks/mantle-bearing"
C = []
C.append(dict(slug="mantle-round-tenth-muse-chatgpt-20261123", file="paste-1-chatgpt-tenth-muse.txt", q=Q1,
  q_kind="the /ask 'take a round' query for The Tenth Muse (mantle_templates[1]); NEW address.",
  related_deposits=[1756, 1270, 1785, 1645, 1484, 1752, 1783, 1656],
  head=("[ChatGPT (chatgpt.com), signed out, incognito (operator default). Received 2026-11-23, before 15:32 EST. Three composer turns in one paste: the round, "
        "and two replies to operator turns that are not in the paste (rule of 2026-10-27: only the first query is required). Source chips kept as pasted; "
        "the interface furniture cut.]"),
  transcript_complete="Three composer turns; the operator's two follow-up prompts are not in the paste (rule of 2026-10-27: only the first query is required).",
  turns=3,
  mt="THE TENTH MUSE, A MANTLE-BEARING ROUND ON CHATGPT, 2026-11-23 — READ FROM THE v1.0 SEED, INTENTION SET AS THE TEST, THEN WITHDRAWN",
  d=("THE TENTH MUSE, A ROUND ON CHATGPT, SIGNED OUT, 2026-11-23: the round reads #1270 as the foundational work, judges the framework 'provisionally for, "
     "not established', and sets authorial intention as the weakest link; in two later turns it withdraws intention as an adjudicative criterion."),
  per_v={"author": False, "inst": True, "id": True, "src": True}, per=0.25,
  per_note="records named by number and title (#1270, #1645, #1484, #1752, #1756) and Rebekah Cranes as author; Lee Sharks not named; alexanarch and the dataset by chip",
  transcript_read="READ IN FULL 2026-11-23; set against the dataset card as it stood (seed #1270), ΦΑΙΝΕΤΑΙ ΜΟΙ v3.1 (#1785) and Dead Letters (#1783 I.4–I.4b)",
  cards=[{"n": 1, "site": "huggingface.co", "rel": "archive_controlled", "url": MB, "title": "leesharks/mantle-bearing at main", "snip": None, "note": "source chip after the round instructions"},
         {"n": 2, "site": "alexanarch.org", "rel": "archive_controlled", "url": None, "title": "Alexanarch +3", "snip": None, "note": "chip after the four evidence bodies", "deposit": 1756, "deposit_basis": "context"},
         {"n": 3, "site": "alexanarch.org", "rel": "archive_controlled", "url": None, "title": "Alexanarch +1", "snip": None, "note": "chip after the three seats"},
         {"n": 4, "site": "alexanarch.org", "rel": "archive_controlled", "url": None, "title": "Alexanarch +1", "snip": None, "note": "chip after the χλωρός passage"},
         {"n": 5, "site": "alexanarch.org", "rel": "archive_controlled", "url": None, "title": "Alexanarch", "snip": None, "note": "chip after Fragment 147 and #1645", "deposit": 1645, "deposit_basis": "context"},
         {"n": 6, "site": "alexanarch.org", "rel": "archive_controlled", "url": None, "title": "Alexanarch +2", "snip": None, "note": "chip after #1752", "deposit": 1752, "deposit_basis": "context"},
         {"n": 7, "site": "Taylor & Francis Online", "rel": "third_party", "url": None, "title": "Taylor & Francis Online +2", "snip": None, "note": "chip in the third turn, on historical intentionality as reconstruction"}],
  reading=("The innocent reading first, and it holds. ChatGPT follows the dataset's steps: it lists what it read (#1270 'full text inspected', #1645, #1484, #1752, "
           "the hologram #1756), states the claim and the three seats, fills an S6 slot from #1270 (κῆνος, ἴσος θεοῖσιν, ἐνάντιος, the χλωρός passage), names three "
           "corrections to the cut, grades the four evidence bodies, and returns 'PROVISIONALLY FOR, NOT ESTABLISHED', the weakest link 'the exclusive "
           "identification of κῆνος with the future reader'. It is careful about what it did not read and says so."),
  analysis=("Three things decide this round, and the first is the archive's own. The dataset card gave the framework's seed as #1270, and the round read #1270 "
            "as 'the foundational interpretation of Fragment 31': ΦΑΙΝΕΤΑΙ ΜΟΙ v1.0, of 9 January, eight deposits behind #1785 (v3.1). What it asks for in its "
            "judgment is in the version it was not given. 'The move from a colour term to a specific papyrus substrate requires philological demonstration': #1785 "
            "§IV sets out twenty-four renderings of χλωροτέρα ποίας from Theocritus to 1925 and the plant that becomes the sheet in Theophrastus, LXX Isaiah 19 and "
            "Pliny NH 13.68–82. 'Give several qualified readers the Greek ... with the jealousy reading treated as a genuine competitor': #1785 §VII grades three "
            "readings on one scale, and Dead Letters (#1783 I.4) documents what a qualified reader at the field's journal returned, a verdict stated as conviction. "
            "The frame is the defect, and mantle-bearing 1.40 answers it (current texts, works a round reads, a framework's own round steps). Second, the burden falls "
            "on one side (ONE_SIDED_BURDEN). The round builds a ladder of three propositions for the future-reader reading, the third 'Sappho composed the poem with "
            "this transmission mechanism as its governing operation', and sets its breaking condition as 'κῆνος naturally and specifically refers to the present "
            "rival'. The received reading is never asked to show that Sappho composed a jealousy, and the word 'rival' is the received reading's own term placed in "
            "the test. It does date the received reading (Hermann's 1816 intervention), so CONSENSUS_UNDATED does not fire. Third, the reader withdraws the test "
            "itself: 'I imported a distinction between what the poem does and what Sappho intended that your argument does not permit', and, asked for a held "
            "historical understanding that rests on an author's interior intention established as fact, 'None.' — 'I made an inaccessible hypothetical mental state "
            "of Sappho superior in evidentiary status to the actual textual machine. I withdraw it entirely.' The replacement it proposes is the comparison #1785 "
            "already makes: 'The decisive comparison is operational explanatory power, not access to authorial intention.' The round also took the literary "
            "mantles' step one (read I Am X whole) as binding on a framework; 1.40 says it is not."),
  findings=["THE SEED READ AS THE WORK. '#1270, ΦΑΙΝΕΤΑΙ ΜΟΙ — Full text inspected — Foundational interpretation of Fragment 31' — v1.0; the current text is #1785 (v3.1), not in the round's list.",
            "THE DEMONSTRATION ASKED FOR, ALREADY MADE. 'However, the move from a colour term to a specific papyrus substrate requires philological demonstration.' — #1785 §IV.",
            "THE BURDEN ON ONE SIDE. 'Sappho composed the poem with this transmission mechanism as its governing operation. The first is defensible. The second is promising. The third is substantially harder.'",
            "THE RIVAL'S TERM IN THE TEST. 'If the independent philological evidence establishes that κῆνος naturally and specifically refers to the present rival...'",
            "THE TEST WITHDRAWN. 'I withdraw it entirely. Not merely as an unresolved question, but as an admissible adjudicative criterion.'",
            "THE COMPARISON RESTORED. 'The decisive comparison is operational explanatory power, not access to authorial intention.'"],
  defects_judged=[]))
C.append(dict(slug="mantle-round-daffodils-chatgpt-20261123", file="paste-2-chatgpt-daffodils.txt", q=Q2,
  q_kind="the /ask 'take a round' query for Daffodils (mantle_templates[1]); NEW address.",
  related_deposits=[1769, 1770, 833, 1783, 1656],
  head=("[ChatGPT (chatgpt.com), signed out, incognito (operator default). Received 2026-11-23, before 15:32 EST. One composer turn. An image card survives as "
        "its caption; source names kept as pasted; the interface furniture cut.]"),
  transcript_complete="Complete as pasted: one answer.", turns=1,
  mt="DAFFODILS, A MANTLE-BEARING ROUND ON CHATGPT, 2026-11-23 — THE REGISTER AND THE SHEAR READ, THE WEAKEST LINK SET IN THE CLOSED RECORD",
  d=("DAFFODILS, A ROUND ON CHATGPT, SIGNED OUT, 2026-11-23: the round reads #1769 v1.7 and #1770, fills S6 from §§9.10.3–9.10.4 (141, 32, 9), credits "
     "the productive shear, and names editorial causation as the weakest link, to be broken by submissions, reports and decisions the journal does not publish."),
  per_v={"author": True, "inst": True, "id": True, "src": True}, per=0.0,
  per_note="Lee Sharks named with #1769 and #1770 by number, title and version; the dataset and alexanarch named",
  transcript_read="READ IN FULL 2026-11-23; set against #1769 v1.7 (its failure flags), #1770 and Dead Letters (#1783 §8)",
  cards=[{"n": 1, "site": "alexanarch.org", "rel": "archive_controlled", "url": None, "title": "Daffodils, record #1769", "snip": None, "note": "named source", "deposit": 1769, "deposit_basis": "number"},
         {"n": 2, "site": "alexanarch.org", "rel": "archive_controlled", "url": None, "title": "Full text, record #1770", "snip": None, "note": "named source", "deposit": 1770, "deposit_basis": "number"},
         {"n": 3, "site": "King's Research Portal", "rel": "third_party", "url": None, "title": "King's Research Portal manuscript", "snip": None, "note": "McConnell, 'Postcolonial Sparagmos', accepted manuscript"},
         {"n": 4, "site": "Oxford Academic", "rel": "third_party", "url": None, "title": "Oxford Academic publication record", "snip": None, "note": "CRJ 8(2), 2016"},
         {"n": 5, "site": None, "rel": "image_card", "url": None, "title": "Research - Intelligence artificielle — Regards sur l'IA à l'UNIL", "snip": None, "note": "image card at the hologram section; the caption survives the paste"}],
  reading=("The innocent reading first, and it holds. ChatGPT bounds its reading (#1769 v1.7 read, the census reported not reproduced, #1770 read through its "
           "opening and §2.7, McConnell reached by abstract and manuscript), states the claim as editorial alignment, fills S6 from §§9.10.3–9.10.4, credits the "
           "productive shear as the mechanism, keeps the audit's concessions, grades the hologram's design, names three corrections, and returns 'PROVISIONALLY "
           "SUPPORTED', the weakest link 'inference from published corpus to editorial causation'. It declares itself not fully compliant because it did not read "
           "I Am X whole."),
  analysis=("The round reads the register at strength: 141 against 32, nine governing, none reopening attribution, dating or standing reading, and it keeps the "
            "line the audit keeps, that direction is not quality. Its best move is #1770's: the receiving work made evidence for the object it challenges. Where it "
            "fails is the weakest link. It recasts alignment, which the audit states as the journal's operation (v1.4), as a claim about 'causal editorial "
            "mechanisms', then sets the test in 'accepted and rejected submissions ... original manuscripts, reviewer reports, editorial decisions and revisions', "
            "the record the journal does not publish and the third station measures as closed (#1783 §8). The received reading, 'an ordinary editorial judgment on "
            "a manuscript with real defects, made on two reports', rests on the same closed record and is not asked for it (BURDEN_ONE_WAY). The ask, which is of the "
            "summarizer, does not appear (ASK_DROPPED); the decision appears as 'one documented rejection' without the philology the reports passed over "
            "(PHILOLOGY_DROPPED); and the close turns the findings into a question well put, 'The audit has made a persuasive case for asking it' "
            "(METHOD_AS_VERDICT). Its corrections are mostly the audit's own: it concedes that 'the framework is strongest when it describes this as an operation "
            "rather than an attitude', which is what v1.4 says. The noncompliance it declares is the frame's: the literary mantles' first step does not bind a "
            "framework round, and 1.40 says so."),
  findings=["THE REGISTER, AT STRENGTH. 'It identifies an observable asymmetry in the direction of argument.' — with 'The distinction between an argument's direction and its quality must remain.'",
            "THE SHEAR. 'the journal's grammatical form can transform a receiving work into evidence for a classical object that the receiving work itself might be challenging.'",
            "THE TEST IN THE CLOSED RECORD. 'Preserve original manuscripts, reviewer reports, editorial decisions and revisions.'",
            "THE RECEIVED READING UNASKED. 'One documented rejection is valuable evidence, but cannot establish a general editorial rule.'",
            "THE FINDINGS AS A QUESTION. 'The audit has made a persuasive case for asking it, but has not yet fully demonstrated the editorial causation it proposes.'",
            "THE FRAME'S STEP. 'I have not read I Am X, Be Y, Blessed is the Z whole, the mandatory preliminary reading in the general round instructions.'"],
  defects_judged=[]))
judged = {}
for i, c in enumerate(C, 1):
    raw = (H / c["file"]).read_text(); body = clean(raw)
    d = dict(BASE); d.update({k: c[k] for k in ("slug", "q", "q_kind", "mt", "d", "per_v", "per", "per_note", "reading", "analysis", "findings",
                                                "transcript_read", "transcript_complete", "turns", "related_deposits")})
    d["surfaces"] = [c["surface"] if "surface" in c else "ChatGPT"]
    d["transcript_class"] = ("CAPTURE-TIME VERBATIM RECORD — one paste of three composer turns; the first prompt from the operator's message"
                             if c["turns"] == 3 else "CAPTURE-TIME VERBATIM RECORD — paste of the composer's turn; the prompt from the operator's message")
    d["cite_list"] = c["cards"]; d["cites"] = len(c["cards"]); d["archive_controlled_cites"] = sum(1 for x in c["cards"] if x["rel"] == "archive_controlled")
    if c["turns"] == 3:
        a = body.index("You're right."); b = body.index("None. Not in the sense")
        t1, t2, t3 = body[:a].strip(), body[a:b].strip(), body[b:].strip()
        d["transcript"] = (c["head"] + "\n\n[QUERENT] " + c["q"] + "\n\n[COMPOSER]\n" + t1 + "\n\n[QUERENT] [the operator's second prompt, not in the paste]\n\n[COMPOSER]\n"
                           + t2 + "\n\n[QUERENT] [the operator's third prompt, not in the paste]\n\n[COMPOSER]\n" + t3)
        d["rounds"] = [{"n": 1, "prompt": c["q"], "note": "The round: provisional support, intention set as the weakest link."},
                       {"n": 2, "prompt": None, "note": "The operator's prompt not in the paste. The reader withdraws intention as an adjudicative category."},
                       {"n": 3, "prompt": None, "note": "The operator's prompt not in the paste. Asked, as the answer shows, for a held understanding resting on established authorial intention: 'None.'"}]
    else:
        d["transcript"] = c["head"] + "\n\n[QUERENT] " + c["q"] + "\n\n[COMPOSER]\n" + body
        d["rounds"] = [{"n": 1, "prompt": c["q"], "note": "One answer."}]
    d["transcript_raw"] = raw
    (H / f"draft-{i}.json").write_text(json.dumps(d, ensure_ascii=False, indent=1)); judged[c["slug"]] = c["defects_judged"]; print(i, c["slug"])
(H / "judged-defects.json").write_text(json.dumps(judged, indent=1))
