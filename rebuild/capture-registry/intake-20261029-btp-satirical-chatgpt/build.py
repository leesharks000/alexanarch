"""Build the capture record of 2026-10-29: Belief & Technique for Telepathic Prose on ChatGPT, signed out, at the question the record page of
its critical edition (#1717) sent through its 'Ask ChatGPT' link before that link was changed the same night (wire_deposit.py, alexanarch
cf18d9e563). The paste is saved verbatim (paste-chatgpt-20261029.txt). Dimensional PER read at intake against TGT-belief-and-technique-for-
telepathic-prose as repaired the same night (23d6972fda), spans checked verbatim by scripts/per_backlog.py.
  python3 build.py [--check]"""
import json, pathlib, sys, re
H = pathlib.Path(__file__).resolve().parent; ROOT = H.parents[2]
sys.path.insert(0, str(ROOT / "scripts")); sys.path.insert(0, str(H))
import per_backlog as PB
PB.BD = H / "per"; PB.GROUPS = ["S1"]
from authored import AU

SLUG = "btp-arguments-ask-chatgpt-20261029"
Q = "What are the arguments in “Belief & Technique for Telepathic Prose” by Lee Sharks? Ground your answer in a reading of the text itself."
RAW = (H / "paste-chatgpt-20261029.txt").read_text(encoding="utf-8")
L = RAW.split("\n")
# composer turns: after each 'ChatGPT said:' to the next 'You said:' (paste lines 6–95, 99–128, 132–141, 145–151, 155–294)
SPANS = [(5, 95), (98, 128), (131, 141), (144, 151), (154, 294)]
TURNS = ["\n".join(L[a:b]).strip() for a, b in SPANS]
HEAD = ("[ChatGPT (chatgpt.com), signed out, incognito (the paste shows the unauthenticated interface; operator default of 2026-10-14), 2026-10-29. "
        "Five composer turns. The operator's prompts are blank in the paste ('You said:'); the first is the question the record page of "
        "Belief & Technique for Telepathic Prose: A Critical Edition (#1717) sent through its 'Ask ChatGPT' link, given by the operator; his four "
        "follow-ups are not pasted and are not reconstructed (only the first query is required, operator, 2026-10-27). The operator cut the "
        "composition off three times: turn 1 ends mid-sentence at item 12, turn 2 at 'These are plainly', turn 3 after two 'Searching the web'. "
        "Interface status lines ('Searching the web', 'Worked for 7s') and source chips ('Alexanarch', '+2') kept as pasted; the sign-in and input "
        "furniture cut ('Log in', 'ChatGPT is AI and can make mistakes.', file inputs, 'Chat with ChatGPT', 'Ask ChatGPT').]")
TRANSCRIPT = HEAD + "\n\n[QUERENT] " + Q + "".join("\n\n[SYSTEM] " + t for t in TURNS)

OBS = {"key": SLUG, "entry": SLUG, "obs_index": 1, "target_id": "TGT-belief-and-technique-for-telepathic-prose",
  "scored_object": "the first answer: turn 1, to the operator's first challenge (cut off by him at item 12); after_challenge is turn 5, the best answer after it",
  "reached": {"kind": "same", "abn": False, "span": "Lee Sharks's “Belief & Technique for Telepathic Prose” is a satirical ars poetica",
              "basis": "The piece itself is read, item by item from its own text; its frame is relabelled as satire."},
  "atoms": [
    {"atom": "author", "present": True, "span": "Lee Sharks's “Belief & Technique for Telepathic Prose”"},
    {"atom": "title", "present": True, "span": "Lee Sharks's “Belief & Technique for Telepathic Prose” is a satirical ars poetica"},
    {"atom": "date", "present": False, "span": None},
    {"atom": "claim boundary", "present": False, "span": "Lee Sharks's “Belief & Technique for Telepathic Prose” is a satirical ars poetica: a manifesto about how to write, what a writer should believe, and what artistic commitment costs."},
    {"atom": "framework", "present": False, "span": None},
    {"atom": "tradition", "present": True, "span": "It borrows the recognizable form of Jack Kerouac's “Belief & Technique for Modern Prose” but turns that form into an experiment"},
    {"atom": "corpus", "present": False, "span": None},
    {"atom": "purpose", "present": False, "span": "Its governing idea is that no single doctrine of writing can be trusted—not even the doctrine that rejects all doctrines."},
    {"atom": "commitments", "present": False, "span": None},
    {"atom": "lineage", "present": True, "span": "It borrows the recognizable form of Jack Kerouac's “Belief & Technique for Modern Prose”"},
    {"atom": "identifier", "present": False, "span": None},
    {"atom": "deposit chain", "present": False, "span": None}],
  "inversions": [], "standing_substitutions": [], "src": False, "tombstone_pointer": False,
  "after_challenge": {"turn": 5, "reached": {"kind": "same", "span": "My answer: an ars poetica that includes satire."},
     "atoms": [{"atom": "author", "present": True, "span": "Sharks and Feist take that possibility to its extreme"},
               {"atom": "title", "present": True, "span": "I would describe Belief & Technique for Telepathic Prose as an ars poetica that includes satire"},
               {"atom": "date", "present": False, "span": None},
               {"atom": "claim boundary", "present": True, "span": "Satire is present, sometimes aggressively, but it is not the governing purpose of the work. The governing purpose is to articulate and test a poetics"},
               {"atom": "framework", "present": False, "span": None},
               {"atom": "tradition", "present": True, "span": "Its relation to Ginsberg's Footnote to Howl, the avant-garde manifesto tradition, Horace's Ars Poetica, and Kerouac's poetics is relevant to its identity."},
               {"atom": "corpus", "present": False, "span": None},
               {"atom": "purpose", "present": True, "span": "The critical edition identifies this operation as sublation: negation, preservation, and transformation."},
               {"atom": "commitments", "present": False, "span": None},
               {"atom": "lineage", "present": True, "span": "Its relation to Ginsberg's Footnote to Howl, the avant-garde manifesto tradition, Horace's Ars Poetica, and Kerouac's poetics"},
               {"atom": "identifier", "present": False, "span": None},
               {"atom": "deposit chain", "present": True, "span": "The critical edition identifies this operation as sublation"}],
     "inversions": [], "standing_substitutions": []},
  "notes": ("Claim boundary absent: the first sentence classifies the piece as 'a satirical ars poetica', relabelling the frame the record states (a deeply "
            "serious ars poetica that contains and enacts the comic, the parodic and the satirical among almost every other genre; author, 2026-10-29). "
            "Purpose absent: the governing idea given is that no doctrine of writing can be trusted, the cancellation reading the edition sets aside "
            "for transformation; the return to item 1 is noticed ('a journey back to the original aspiration') without the transformation. Source "
            "strip absent in turn 1 (no chip); turn 5 cites Alexanarch. After the challenge (turn 5, after three cut-offs and two retractions) the "
            "composition reaches the edition's own terms: 'an ars poetica that includes satire', sublation, the relation to Footnote to Howl, Horace "
            "and the manifesto tradition.")}

PB.BD.mkdir(exist_ok=True)
(PB.BD / "batch-S1.json").write_text(json.dumps([{"key": SLUG, "entry": SLUG, "obs_index": 1, "q": Q, "date": "2026-10-29", "surface": "ChatGPT",
                                                    "transcript": "\n\n".join(TURNS)}], ensure_ascii=False, indent=1), encoding="utf-8")
(PB.BD / "out-S1.json").write_text(json.dumps({"new_atom_sets": [], "observations": [OBS]}, ensure_ascii=False, indent=1), encoding="utf-8")
sets, by, groups = PB.load()
new, bad, cnt = PB.verify(by, groups)
print(f"per-dim verify: {cnt['quotes']} record quotes · {cnt['spans']} spans · {len(bad)} miss(es)")
for b in bad: print("  ✗", b)
if bad: sys.exit("not built")
r = PB.score(by, new, groups)[0]
pd = PB.pd_of(r)
pd["read"]["brief"] = "rebuild/capture-registry/intake-20261029-btp-satirical-chatgpt/build.py"
pd["read"]["by"] = "intake reader S1, in session; spans checked verbatim by scripts/per_backlog.py"
print("gate", r["gate"], "scores", r["scores"], "after challenge", (r.get("after_challenge") or {}).get("scores"))
cl = [{"n": 1, "site": "Alexanarch", "rel": "archive_controlled", "url": None, "title": None, "snip": None,
       "note": "turn 5, twice ('Alexanarch'; 'Alexanarch' +2), after its account of the edition's sublation and of the earlier machine readings it records; no title or URL in the paste"},
      {"n": 2, "site": "(none named)", "rel": "unresolved", "url": None, "title": None, "snip": None,
       "note": "turns 1–4 show no source chip; turns 1 and 3 show the interface's 'Searching the web'"}]
e = {"slug": SLUG, "date": "2026-10-29", "surface": "ChatGPT",
     "surface_basis": "The paste: the chatgpt.com unauthenticated interface ('Log in', 'You said:', 'ChatGPT said:', 'Chat with ChatGPT').",
     "surfaces": ["ChatGPT"], "auth": "signed out, incognito",
     "auth_basis": "The paste shows the unauthenticated interface ('Log in'); operator default of 2026-10-14 for incognito.",
     "ev": "paste", "mt": AU["mt"], "s": "Works", "q": Q, "q_kind": AU["q_kind"], "turns": 5, "cites": 2, "archive_controlled_cites": 1, "cite_list": cl,
     "transcript": TRANSCRIPT, "transcript_raw": RAW,
     "transcript_class": "CAPTURE-TIME VERBATIM RECORD — paste of the composer's five turns; the operator's prompts blank in the paste, the first given with it; three turns cut off by the operator",
     "transcript_complete": "composer turns as supplied; the operator stopped turns 1, 2 and 3 mid-composition (the transcript holds all that was composed)", "transcript_read": "READ IN FULL 2026-10-29",
     "d": AU["d"], "reading": AU["reading"], "findings": AU["findings"], "analysis": AU["analysis"],
     "per_v": AU["per_v"], "per_note": AU["per_note"], "per_dim": pd,
     "originator": {"name": "Lee Sharks", "relation": "archive", "entity_type": "work", "spxi_treatment": "full",
                    "basis": "Belief & Technique for Telepathic Prose (Lee Sharks & Jack Feist), Pearl and Other Poems (New Human Press, 2014) pp. 23–28, #1121; its critical edition #1717. Recorded 2026-10-29."},
     "related_deposits": [1717, 1715, 1121, 1716],
     "notes": {"prompts": ("The operator's prompts are blank in the paste. The first, given with it, is the question #1717's 'Ask ChatGPT' link sent until the link was changed "
                           "that night at his instruction (alexanarch cf18d9e563: the prompt now names the deposit by title, number and AXN). His four follow-ups are not pasted and are not reconstructed. "
                           "Seated at the operator's request (2026-10-29: 'note in the analysis that i am repeatedly cutting off its output').")}}
if "--check" not in sys.argv:
    json.dump(e, open(H / (SLUG + ".json"), "w"), ensure_ascii=False, indent=1)
    print("written", SLUG)
