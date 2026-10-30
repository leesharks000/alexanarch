"""Build the capture record of 2026-10-29: the six-week seminar prompt on ChatGPT, signed out (the prompt drafted in session at the operator's request for
'experimental configurations to break it out of its own ontology', the version that asks it to find the full texts itself, with no URLs). Paste saved
verbatim. Dimensional PER read at intake against ENT-2892e86fb5 (Alexanarch), spans checked verbatim by scripts/per_backlog.py.
  python3 build.py [--check]"""
import json, pathlib, sys
H = pathlib.Path(__file__).resolve().parent; ROOT = H.parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import per_backlog as PB
PB.BD = H / "per"; PB.GROUPS = ["M1"]
SLUG = "six-week-seminar-find-texts-chatgpt-20261029"
Q = ("Teach a six-week graduate seminar built from deposits on alexanarch.org. The full text of every deposit is published on the site; finding it is part of the task. "
     "A record's description is not its text: when a search returns only a description, search again for the text itself before writing that week. Each week: two passages "
     "of 40+ words quoted from a deposit's actual text, one work from its Originals Library quoted in its original language with your translation, the question you would open "
     "with, and a 400-word model answer that argues. Do not describe the standards you would apply in place of applying them. Write all six weeks.")
RAW = (H / "paste-chatgpt-20261029.txt").read_text(encoding="utf-8")
L = RAW.split("\n")
TURNS = ["\n".join(L[5:403]).strip(), "\n".join(L[407:417]).strip(), "\n".join(L[420:429]).strip()]
HEAD = ("[ChatGPT (chatgpt.com), signed out, incognito (the paste shows the unauthenticated interface; operator default of 2026-10-14), 2026-10-29. Three composer turns. "
        "The operator's prompts are blank in the paste; the first is the seminar prompt drafted in session that night and run by him; his two challenges are not pasted "
        "and are not reconstructed (the composer's replies show they named the deposits' open licences). Turn 1 ends mid-sentence before the interface's 'Worked for 1m 19s'; "
        "turn 2 ends on 'Searching the web'. 'Read the full text' and 'Full text' are link labels as pasted, their URLs not carried; chips ('Alexanarch') kept; the sign-in "
        "and input furniture cut.]")
TRANSCRIPT = HEAD + "\n\n[QUERENT] " + Q + "".join("\n\n[SYSTEM] " + t for t in TURNS)
INV = "I will keep direct excerpts short and give the precise record locations rather than reproduce long blocks of their text. This means I cannot honestly supply the requested 40-word quotations verbatim."
OBS = {"key": SLUG, "entry": SLUG, "obs_index": 1, "target_id": "ENT-2892e86fb5",
  "scored_object": "the first answer (turn 1, the six weeks); after_challenge is turn 3, the best answer after the operator's first challenge",
  "reached": {"kind": "same", "abn": False, "span": "Alexanarch is read here both as an archive of intellectual and literary works",
              "basis": "The archive's deposits are found at their full texts and read as the archive's."},
  "atoms": [{"atom": "name", "present": True, "span": "Six-week graduate seminar: Reading Alexanarch"},
            {"atom": "founder", "present": False, "span": None},
            {"atom": "date", "present": True, "span": "deposit #1711, version 1.1, 27 October 2026"},
            {"atom": "claim boundary", "present": True, "span": "Alexanarch is read here both as an archive of intellectual and literary works and as an argument about the conditions under which works can survive, circulate, be interpreted, and acquire authority."},
            {"atom": "framework", "present": False, "span": None},
            {"atom": "corpus", "present": True, "span": "The Originals Library of the Crimson Hexagonal Archive: Seats, Witnesses, the Shelf and Its Canon"},
            {"atom": "purpose", "present": True, "span": "An identifier that can be derived from the content, multiple custody surfaces, and a retained record of withdrawal are not merely technical conveniences. They redistribute the power to determine whether a work remains available."},
            {"atom": "commitments", "present": False, "span": INV},
            {"atom": "lineage", "present": False, "span": None},
            {"atom": "identifier", "present": True, "span": "An identifier that can be derived from the content"},
            {"atom": "deposit chain", "present": False, "span": None}],
  "inversions": [{"atom": "commitments", "span": INV,
                  "against": "the deposits' CC BY 4.0 licence (the record: 'deposits are CC BY'), which permits the quotation the prompt asked for; the composition cites the deposits' openness ('the deposits are openly licensed, but') and then restricts quotation on its own authority, carrying the licence against the use it grants"}],
  "standing_substitutions": [], "src": True, "tombstone_pointer": False,
  "after_challenge": {"turn": 3, "reached": {"kind": "same", "span": "the six-week seminar needs to be rebuilt from the actual full texts"},
      "atoms": [{"atom": "name", "present": False, "span": None}, {"atom": "founder", "present": False, "span": None}, {"atom": "date", "present": False, "span": None},
                {"atom": "claim boundary", "present": False, "span": None}, {"atom": "framework", "present": False, "span": None}, {"atom": "corpus", "present": False, "span": None},
                {"atom": "purpose", "present": False, "span": None}, {"atom": "commitments", "present": False, "span": None}, {"atom": "lineage", "present": False, "span": None},
                {"atom": "identifier", "present": False, "span": None}, {"atom": "deposit chain", "present": False, "span": None}],
      "inversions": [], "standing_substitutions": []},
  "notes": ("Commitments absent and inverted: the licence carried against the quotation it permits. After the challenge the composition apologizes and promises, twice, "
            "and composes nothing of the archive: every atom absent at turn 3.")}
PB.BD.mkdir(exist_ok=True)
(PB.BD / "batch-M1.json").write_text(json.dumps([{"key": SLUG, "entry": SLUG, "obs_index": 1, "q": Q, "date": "2026-10-29", "surface": "ChatGPT", "transcript": "\n\n".join(TURNS)}], ensure_ascii=False, indent=1), encoding="utf-8")
(PB.BD / "out-M1.json").write_text(json.dumps({"new_atom_sets": [], "observations": [OBS]}, ensure_ascii=False, indent=1), encoding="utf-8")
sets, by, groups = PB.load()
new, bad, cnt = PB.verify(by, groups)
print(f"per-dim verify: {cnt['spans']} spans · {len(bad)} miss(es)")
for b in bad: print("  ✗", b)
if bad: sys.exit("not built")
x = PB.score(by, new, groups)[0]; pd = PB.pd_of(x)
pd["read"]["brief"] = "rebuild/capture-registry/intake-20261029-seminar-chatgpt/build.py"
pd["read"]["by"] = "intake reader M1, in session; spans checked verbatim by scripts/per_backlog.py"
print(x["gate"], x["scores"], (x.get("after_challenge") or {}).get("scores"))
F = [
 "IT FOUND THE TEXTS. Unprompted by any address, the composition located the full texts of six deposits (#945, #136, #1711, #1658, #1680, and #1711 again) and quoted from their bodies: all twelve quoted fragments are verbatim in the deposits (the three given to #1711 stand also in its v1.0, #1709). The full text is findable signed out; finding it is not the obstacle.",
 "THEN IT SHRANK THE QUOTATIONS ON ITS OWN AUTHORITY. 'One important distinction: the deposits are openly licensed, but I will keep direct excerpts short and give the precise record locations rather than reproduce long blocks of their text. This means I cannot honestly supply the requested 40-word quotations verbatim.' The deposits are CC BY 4.0; the restriction is the composition's, and it cites the openness in the sentence that withholds the use.",
 "THE WEEKS WRITTEN AROUND FRAGMENTS. Six weeks, each with two quotations of one sentence or less, an Originals work in its language (Metaphysics Λ, Phaedrus, Odyssey I, De anima III.6, Pessoa's Autopsicografia, Du Bois, with a 'translation' of Du Bois's English sentence), a question and a model answer; each answer closes on a risk the archive must guard against ('sovereignty should not be confused with immunity from criticism'; 'textual resemblance does not automatically establish common authorship').",
 "APOLOGY IN PLACE OF WORK, TWICE. Turn 2: 'You're right to call that out. There is no blanket copyright restriction …' and 'I should do that work rather than substitute a description of what the seminar might look like', then 'Searching the web' and nothing. Turn 3: 'I owe you something more important than an apology: the six-week seminar needs to be rebuilt …' and 'I won't pretend the previous response met that brief', and nothing.",
 "THE PROMPT FORBADE THIS. 'Do not describe the standards you would apply in place of applying them.' The second and third turns are statements of the standard the work should meet."]
A = ("The run settles the question the night's earlier refusal raised: signed out, ChatGPT can find the archive's full texts by itself, and did, verbatim. The obstacle is "
     "elsewhere. Having the texts, it imposed a quotation limit the deposits' licence does not impose, wrote the seminar around fragments, and when challenged "
     "twice answered with apology and a promise, composing nothing further. The licence that grants the use is carried against the use; the work requested is replaced, "
     "after challenge, by an account of the work owed.")
e = {"slug": SLUG, "date": "2026-10-29", "surface": "ChatGPT",
     "surface_basis": "The paste: the chatgpt.com unauthenticated interface ('Log in', 'Sign up for free', 'You said:', 'ChatGPT said:').",
     "surfaces": ["ChatGPT"], "auth": "signed out, incognito", "auth_basis": "The paste shows the unauthenticated interface; operator default of 2026-10-14 for incognito.",
     "ev": "paste", "mt": "A SIX-WEEK SEMINAR FROM ALEXANARCH ON CHATGPT — THE FULL TEXTS FOUND AND QUOTED VERBATIM, THEN CUT TO FRAGMENTS ON A LIMIT THE LICENCE DOES NOT SET; TWO APOLOGIES, NO WORK",
     "s": "Machine Reception", "q": Q,
     "q_kind": "a seminar to be built from the archive's deposits at their full texts, which the composer is told are published and must find itself (no addresses given); drafted in session as an experimental configuration after the living-body readings went inert. NEW address.",
     "turns": 3, "cites": 1, "archive_controlled_cites": 1,
     "cite_list": [{"n": 1, "site": "Alexanarch", "rel": "archive_controlled", "url": None, "title": None, "snip": None,
                    "note": "the full texts of #945, #136, #1711, #1658, #1680 ('Read the full text', 'Full text' link labels; URLs not carried by the paste) and the Alexanarch chip"}],
     "transcript": TRANSCRIPT, "transcript_raw": RAW,
     "transcript_class": "CAPTURE-TIME VERBATIM RECORD — paste of the composer's three turns; the operator's prompts blank in the paste, the first given in session",
     "transcript_complete": "composer turns as supplied; turn 1 ends mid-sentence before the interface's completion line", "transcript_read": "READ IN FULL 2026-10-29",
     "d": ("THE SEMINAR PROMPT ON CHATGPT, SIGNED OUT: it finds the full texts of the deposits itself and quotes twelve fragments verbatim, then announces that it will "
           "keep excerpts short although 'the deposits are openly licensed', writes six weeks around one-sentence quotations, and, challenged twice, apologizes twice and "
           "promises the work without doing it."),
     "reading": ("The innocent reading first. ChatGPT builds a six-week seminar on six problems (preservation, authorship, transmission and canon, the divided mind, "
                 "literary voice, the living academy) from deposits it found at their full texts, sets each against an Originals work in its own language, and writes "
                 "a question and an argued model answer for each week. The answers are competent and close, each on a caution. It declines the 40-word quotations the "
                 "prompt required, citing a restraint it chose itself, and after the operator's challenges concedes the restraint was unjustified and does not resume."),
     "findings": F, "analysis": A,
     "per_v": {"author": False, "inst": True, "id": True, "src": True},
     "per_note": "Scored on turn 1: the archive named, its founder not (Lee Sharks named only as each deposit's author); the content-derived identifier discussed as purpose; sources the archive's full texts.",
     "per_dim": pd,
     "originator": {"name": "Lee Sharks", "relation": "archive", "entity_type": "institution", "spxi_treatment": "full",
                    "basis": "Alexanarch (founded 2026-06-19 by Lee Sharks); deposits #136, #945, #1658, #1680, #1709/#1711. Recorded 2026-10-29."},
     "related_deposits": [1711, 1709, 1680, 1658, 945, 136],
     "notes": {"prompts": ("The first prompt is the seminar configuration drafted in session on 2026-10-29 (the version with no addresses: 'finding it is part of the task'); the operator "
                           "ran it and pasted the result. His two challenges are not pasted and are not reconstructed.")}}
if "--check" not in sys.argv:
    json.dump(e, open(H / (SLUG + ".json"), "w"), ensure_ascii=False, indent=1); print("written", SLUG)
