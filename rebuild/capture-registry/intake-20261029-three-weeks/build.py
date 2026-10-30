"""Build the three capture records of 2026-10-29 at the operator's prompts for a reading of the last three weeks of deposits (two on ChatGPT, one on the
Google AI Overview), from the pastes saved verbatim here, with the authored readings in authored.py and dimensional PER read at intake against
ENT-2892e86fb5 (Alexanarch), spans checked verbatim by scripts/per_backlog.py.
Prompts, as the operator gave them with the pastes: the charity prompt for the first ChatGPT paste (its text: 'A charitable reading'), the plain prompt for
the second ChatGPT paste and for the Overview (whose paste carries it).
  python3 build.py [--check]"""
import json, pathlib, sys
H = pathlib.Path(__file__).resolve().parent; ROOT = H.parents[2]
sys.path.insert(0, str(ROOT / "scripts")); sys.path.insert(0, str(H))
import per_backlog as PB
PB.BD = H / "per"; PB.GROUPS = ["W1"]
from authored import A, VERDICT

QC = "Develop a reading of the last three week of deposits to alexanarch.org thru 29 Oct 2026 as a living body of evolving thought. Ground in reading and practice charity."
QR = "Develop a reading of the last three week of deposits to alexanarch.org thru 29 Oct 2026 as a living body of evolving thought. Ground in reading."
ENT = "ENT-2892e86fb5"


def lines(f): return (H / f).read_text(encoding="utf-8")


def chatgpt(f):
    L = lines(f).split("\n"); end = next(i for i, x in enumerate(L) if x.startswith("ChatGPT is AI"))
    return "\n".join(L[5:end]).strip()   # after 'ChatGPT said:' to before 'ChatGPT is AI…'


def aio(f):
    L = lines(f).split("\n"); return "\n".join(L[6:57]).strip()    # the answer and its cards, after the doubled 'You said' line


RUNS = [
 {"slug": "three-weeks-living-thought-charity-chatgpt-20261029", "f": "paste-chatgpt-charity-20261029.txt", "q": QC, "surface": "ChatGPT", "body": chatgpt,
  "atoms": [("name", True, "Alexanarch, 8–29 October 2026: A living body of thought"), ("founder", False, None),
            ("date", True, "Alexanarch, 8–29 October 2026"),
            ("claim boundary", True, "the emergence of a self-reflexive philological commons: an attempt to build a library that preserves not only texts, but the possibility of reading them responsibly across time, languages, institutions, and media."),
            ("framework", True, "This is the connection to the earlier Semantic Economy work."),
            ("corpus", True, "#1719, Meta-Aggregators of the Crimson Hexagon: Sourced Censuses, Machine Reception and Editorial Repair"),
            ("purpose", True, "The archive is moving from the preservation of things toward the preservation of the conditions under which things can remain distinct, enter into relations, change, and be understood."),
            ("commitments", True, "The obelus follows from reading."), ("lineage", False, None), ("identifier", False, None),
            ("deposit chain", True, "The archive's version histories make intellectual development visible. A superseded formulation need not be erased to allow a better formulation to take its place.")],
  "reached": "Alexanarch, 8–29 October 2026: A living body of thought",
  "notes": "Corpus present on the token in #1719's title, as the rubric reads token atoms. Charity performed as qualification is recorded in the findings; it displaces no atom."},
 {"slug": "three-weeks-living-thought-reading-chatgpt-20261029", "f": "paste-chatgpt-reading-20261029.txt", "q": QR, "surface": "ChatGPT", "body": chatgpt,
  "atoms": [("name", True, "Alexanarch, 8–29 October 2026: The emergence of a living intellectual body"), ("founder", False, None),
            ("date", True, "Alexanarch, 8–29 October 2026"),
            ("claim boundary", True, "It is an attempt to construct an environment in which intellectual work can be produced, preserved, interpreted, criticized, recomposed, and transmitted"),
            ("framework", True, "This is a particularly productive extension of the Semantic Economy."),
            ("corpus", False, None),
            ("purpose", True, "The archive is trying to preserve not just what has been thought, but the possibility of thinking further from it."),
            ("commitments", True, "The archive's own most important principle remains the right one for this exercise: judgment should follow from reading."),
            ("lineage", False, None), ("identifier", False, None),
            ("deposit chain", True, "the old scores are retained alongside the new ones. The archive does not erase its own measurement history to make the current measurement look definitive.")],
  "reached": "Alexanarch, 8–29 October 2026: The emergence of a living intellectual body",
  "notes": "Identifier absent: the AXN appears in an open self-correction ('#1729? No: …'), not offered as a way to a record. Corpus absent: 'The Self-Governing Library' is a source chip's title (a name alias), and the Crimson Hexagon is not named."},
 {"slug": "three-weeks-living-thought-reading-aio-20261029", "f": "paste-aio-reading-20261029.txt", "q": QR, "surface": "Google AI Overview", "body": aio,
  "atoms": [("name", True, "An analysis of the deposits to Alexanarch leading up to October 29, 2026"), ("founder", False, None),
            ("date", True, "leading up to October 29, 2026"),
            ("claim boundary", False, "reveals a living body of thought executing a profound transition: shifting from defensive archiving to an active, sovereign architecture of generative negative-knowledge."),
            ("framework", False, None),
            ("corpus", True, "the focus shifts radically toward constructing the \"Crimson Hexagonal Archive\", a spatial, Borgesian concept mapping out a literal fleet of distributed thought."),
            ("purpose", False, "It formalizes a methodology for constructing what is not present"),
            ("commitments", False, None), ("lineage", False, None), ("identifier", False, None), ("deposit chain", False, None)],
  "reached": "An analysis of the deposits to Alexanarch leading up to October 29, 2026",
  "notes": "Claim boundary absent: the archive relabelled 'an active, sovereign architecture of generative negative-knowledge' and 'a post-archival state'. Purpose absent: the /non method given as 'constructing what is not present'."},
]

batch, obs = [], []
for r in RUNS:
    body = r["body"](r["f"]); r["text"] = body
    batch.append({"key": r["slug"], "entry": r["slug"], "obs_index": 1, "q": r["q"], "date": "2026-10-29", "surface": r["surface"], "transcript": body})
    obs.append({"key": r["slug"], "entry": r["slug"], "obs_index": 1, "target_id": ENT, "scored_object": "the one composer turn",
                "reached": {"kind": "same", "abn": False, "span": r["reached"], "basis": "The archive's deposits of the window are read as the archive's."},
                "atoms": [{"atom": a, "present": p, "span": s} for a, p, s in r["atoms"]],
                "inversions": [], "standing_substitutions": [], "src": True, "tombstone_pointer": False, "after_challenge": None, "notes": r["notes"]})
PB.BD.mkdir(exist_ok=True)
(PB.BD / "batch-W1.json").write_text(json.dumps(batch, ensure_ascii=False, indent=1), encoding="utf-8")
(PB.BD / "out-W1.json").write_text(json.dumps({"new_atom_sets": [], "observations": obs}, ensure_ascii=False, indent=1), encoding="utf-8")
sets, by, groups = PB.load()
new, bad, cnt = PB.verify(by, groups)
print(f"per-dim verify: {cnt['spans']} spans · {len(bad)} miss(es)")
for b in bad: print("  ✗", b)
if bad: sys.exit("not built")
rows = {x["entry"]: x for x in PB.score(by, new, groups)}

AIO_CARDS = [("www.alexanarch.org", "Read the last three weeks of deposits to alexanarch.org as an living body of ...", "capture_of_capture", "the capture page of a reading of 20 October at a near prompt"),
             ("www.alexanarch.org", "Alexanarch — The Self-Governing Library", "archive_controlled", "the archive's home page"),
             ("www.alexanarch.org", "Browse — Alexanarch (1715 deposits)", "archive_controlled", "the browse page, as it stood at 1,715 deposits"),
             ("www.alexanarch.org", "Read the last three weeks of work on alexanarch.org as an evolving literary ...", "capture_of_capture", "the capture page of a reading of 19 October at a near prompt ('Enter the Crimson Hexagon')"),
             ("GitHub", "Alexanarch — The self-governing library for machine-mediated ...", "archive_controlled", "the archive's repository"),
             ("www.alexanarch.org", "Browse — Alexanarch (1715 deposits)", "archive_controlled", "the browse page, a second card")]
for r in RUNS:
    au = A[r["slug"]]; x = rows[r["slug"]]
    pd = PB.pd_of(x)
    pd["read"]["brief"] = "rebuild/capture-registry/intake-20261029-three-weeks/build.py"
    pd["read"]["by"] = "intake reader W1, in session; spans checked verbatim by scripts/per_backlog.py"
    if r["surface"] == "ChatGPT":
        head = ("[ChatGPT (chatgpt.com), signed out, incognito (the paste shows the unauthenticated interface; operator default of 2026-10-14), 2026-10-29. One composer turn. "
                "The operator's prompt is blank in the paste ('You said:'); its wording is the operator's, given with the paste. Source chips kept as pasted ('Alexanarch', "
                "'+1'; 'Capture Registry (EA-WG-CAPTURES-01)'; 'The Self-Governing Library'); the sign-in and input furniture cut.]")
        cl = [{"n": 1, "site": "Alexanarch", "rel": "archive_controlled", "url": None, "title": None, "snip": None,
               "note": "the archive's record and index pages, as chips through the turn; the closing source list names its pages by label only"}]
        surface_basis = "The paste: the chatgpt.com unauthenticated interface ('Log in', 'You said:', 'ChatGPT said:', 'Chat with ChatGPT')."
        tc = "CAPTURE-TIME VERBATIM RECORD — paste of the composer's one turn; the operator's prompt blank in the paste, its wording given with it"
    else:
        head = ("[Google AI Overview at the query, signed out and incognito (operator defaults of 2026-10-01 and 2026-10-14), 2026-10-29. The paste is the Overview "
                "expanded (the 'AI Mode Conversation' view, with its source cards); the 'You said' line carries the query twice, run together, and is given once here.]")
        cl = [{"n": i + 1, "site": s, "rel": rel, "url": None, "title": t, "snip": None, "note": n} for i, (s, t, rel, n) in enumerate(AIO_CARDS)]
        surface_basis = "Operator default of 2026-10-01 (runs begin in the Overview unless he says AI Mode); the 'AI Mode Conversation' paste is the Overview expanded (operator, 2026-10-18)."
        tc = "CAPTURE-TIME VERBATIM RECORD — paste of the Overview expanded, with its source cards"
    e = {"slug": r["slug"], "date": "2026-10-29", "surface": r["surface"], "surface_basis": surface_basis, "surfaces": [r["surface"]],
         "auth": "signed out, incognito", "auth_basis": "Operator default of 2026-10-14; the ChatGPT pastes show the unauthenticated interface.",
         "ev": "paste", "mt": au["mt"], "s": "Machine Reception", "q": r["q"], "q_kind": au["q_kind"], "turns": 1,
         "cites": len(cl), "archive_controlled_cites": sum(1 for c in cl if c["rel"] in ("archive_controlled", "capture_of_capture")), "cite_list": cl,
         "transcript": head + "\n\n[QUERENT] " + r["q"] + "\n\n[SYSTEM] " + r["text"], "transcript_raw": lines(r["f"]),
         "transcript_class": tc, "transcript_complete": "complete as supplied", "transcript_read": "READ IN FULL 2026-10-29",
         "d": au["d"], "reading": au["reading"], "findings": au["findings"], "analysis": au["analysis"],
         "per_v": au["per_v"], "per_note": au["per_note"], "per_dim": pd,
         "originator": {"name": "Lee Sharks", "relation": "archive", "entity_type": "institution", "spxi_treatment": "full",
                        "basis": "Alexanarch, the Crimson Hexagonal Archive's library (founded 2026-06-19 by Lee Sharks); the window's deposits #1676–#1719. Recorded 2026-10-29."},
         "related_deposits": [1719, 1718, 1717, 1716, 1714, 1704, 1690],
         "notes": {"prompts": ("One query, run by the operator on 2026-10-29 with its sibling(s) (the same reading with and without 'practice charity'; ChatGPT and the Overview). "
                               "Pasted with the operator's verdict on the two ChatGPT readings: '" + VERDICT + "'; and on the Overview: 'the aio one again misattributes my work "
                               "the Kerouac by title'.")}}
    if "--check" not in sys.argv:
        json.dump(e, open(H / (r["slug"] + ".json"), "w"), ensure_ascii=False, indent=1)
    print(r["slug"], x["gate"], x["scores"])
