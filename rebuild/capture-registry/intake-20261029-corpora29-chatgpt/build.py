"""Build the capture record of 2026-10-29: EA-CORPORA-29 on ChatGPT, signed out, at the question the record page's own 'Ask ChatGPT' link
sends ('What is "EA-CORPORA-29" by Lee Sharks, and how does it work? Ground your answer in the document itself.'). The paste is saved
verbatim (paste-chatgpt-20261029.txt, sha256 43d8deee…). Dimensional PER is read at intake (operator, 2026-10-29): the atom set for the
target, TGT-ea-corpora-29, is built from its record (#1716) and checked, with the observation's spans, by scripts/per_backlog.py.
  python3 build.py [--check]"""
import json, pathlib, sys
H = pathlib.Path(__file__).resolve().parent; ROOT = H.parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import per_backlog as PB
PB.BD = H / "per"; PB.GROUPS = ["C1"]

SLUG = "ea-corpora-29-ask-chatgpt-20261029"
Q = "What is “EA-CORPORA-29” by Lee Sharks, and how does it work? Ground your answer in the document itself."
L = (H / "paste-chatgpt-20261029.txt").read_text(encoding="utf-8").split("\n")
T1 = "\n".join(L[5:266]).strip()      # paste lines 6–266: the first answer
T2 = "\n".join(L[277:325]).strip()    # paste lines 278–325: the answer after the operator's challenge
HEAD = ("[ChatGPT (chatgpt.com), signed out, incognito (the paste shows the unauthenticated interface; operator default of 2026-10-14), 2026-10-29. "
        "Two composer turns. The operator's first prompt is blank in the paste ('You said:'); its wording is the question the EA-CORPORA-29 record page's "
        "'Ask ChatGPT' link sends, given by the operator with the paste. His second prompt is not pasted and is not reconstructed: only the first query is "
        "required (operator, 2026-10-27). Source chips kept as pasted at the line they followed ('Alexanarch' with its count); the link labels of the "
        "closing lists kept as pasted, their URLs not carried by the paste. The sign-in and input furniture cut ('Log in', 'Log in to upload a file and get "
        "help with it.', 'Sign up for free', 'ChatGPT is AI and can make mistakes.', file inputs, 'Chat with ChatGPT', 'Ask ChatGPT').]")
TRANSCRIPT = HEAD + "\n\n[QUERENT] " + Q + "\n\n[SYSTEM] " + T1 + "\n\n[SYSTEM] " + T2
RAW = (H / "paste-chatgpt-20261029.txt").read_text(encoding="utf-8")

REC = "data/registry.json"; TXT = "data/texts/AXN-0A9F-text.md"
ATOMSET = {
  "new": "ea-corpora-29", "name": "EA-CORPORA-29 — The Twenty-Ninth Seating, the Pluriform", "template": "dataset", "external": False,
  "type_basis": "The defining record's content_type is 'Dataset' (family DATASET), a seating of the originals shelf; the dataset template, as for EA-CORPORA-15.",
  "records": [{"deposit": 1716, "title_quote": "EA-CORPORA-29 — The Twenty-Ninth Seating, the Pluriform: Horace and Ovid, the Art of Poetry in Twenty Traditions, the Avant-Garde II, Telepathic Prose, and the Buddhist Canons in Pali, Sanskrit, Chinese, Korean, Japanese and Tibetan"}],
  "atoms": [
    {"atom": "name", "dim": "M", "weight": 3, "kind": "token", "applicability": "required",
     "tokens": ["EA-CORPORA-29", "EA-CORPORA-29 — The Twenty-Ninth Seating", "The Twenty-Ninth Seating, the Pluriform"], "reference": None,
     "evidence": [{"record_quote": "EA-CORPORA-29 — The Twenty-Ninth Seating, the Pluriform: Horace and Ovid", "locus": REC + " #1716 title"},
                  {"record_quote": "# EA-CORPORA-29 — The Twenty-Ninth Seating", "locus": TXT + ":L72"}]},
    {"atom": "author", "dim": "M", "weight": 3, "kind": "role", "applicability": "required", "tokens": ["Lee Sharks", "Sharks, Lee"],
     "reference": "creator of the record, Lee Sharks; the requests and the choices of tradition are his",
     "evidence": [{"record_quote": "The requests and the choices of tradition are Lee Sharks's", "locus": REC + " #1716 substrate"}]},
    {"atom": "date", "dim": "M", "weight": 1, "kind": "token", "applicability": "required", "tokens": ["2026-10-28", "28 October 2026", "October 28, 2026"], "reference": None,
     "evidence": [{"record_quote": "deposited by Lee Sharks on 28 October 2026", "locus": REC + " #1716 wiki_article"}]},
    {"atom": "claim boundary", "dim": "M", "weight": 2, "kind": "reading", "applicability": "required", "tokens": [],
     "reference": "Eleven seats on the originals shelf: the arts of poetry in twenty traditions, Horace and Ovid in Latin, the avant-garde's statements of method, the wanted list, the archive's own art of poetry in all its witnesses (29/07, Belief & Technique for Telepathic Prose by Lee Sharks and Jack Feist, with Make It Human, A Telepathicist Manifesto and the critical edition), and the Buddhist canons; Kerouac's list is a declared absence (29/01) that the critical edition's apparatus asked for. Declared absences hold no text of the works they name.",
     "evidence": [{"record_quote": "beside the avant-garde's statements of method and the archive's own art of poetry in all its witnesses", "locus": TXT + ":L76"},
                  {"record_quote": "Telepathic Prose (29/07) holds the archive's own art of poetry in its drafts of 2014, the book and the blog.", "locus": REC + " #1716 wiki_article"},
                  {"record_quote": "Lee Sharks & Jack Feist, “Belief & Technique for Telepathic Prose”, the Footnote to Pearl", "locus": TXT},
                  {"record_quote": "The seating began with Belief & Technique for Telepathic Prose: A Critical Edition (#1715), whose apparatus asked for Kerouac's list (declared, 29/01)", "locus": TXT + ":L74"},
                  {"record_quote": "11 seats; 196 works; 876,386 lines; 564 files.", "locus": TXT}]},
    {"atom": "framework", "dim": "C", "weight": 2, "kind": "token", "applicability": "required", "tokens": ["EA-CORPORA", "originals shelf", "Originals Shelf", "originals library"], "reference": None,
     "evidence": [{"record_quote": "The twenty-ninth seating of the originals shelf, eleven seats.", "locus": REC + " #1716 description"}]},
    {"atom": "corpus", "dim": "C", "weight": 2, "kind": "token", "applicability": "required", "tokens": ["Crimson Hexagonal Archive", "Crimson Hexagon Archive", "Crimson Hexagon", "Alexanarch"], "reference": None,
     "evidence": [{"record_quote": "EA-CORPORA-29 is the twenty-ninth seating of the Crimson Hexagonal Archive's originals shelf", "locus": REC + " #1716 wiki_article"}]},
    {"atom": "purpose", "dim": "D", "weight": 3, "kind": "reading", "applicability": "required", "tokens": [],
     "reference": "To seat primary texts on the originals shelf, each work with its source, edition, licence, normalization and verified loci, and to declare what the shelf cannot hold yet and when each opens.",
     "evidence": [{"record_quote": "with a source.json recording edition, origin, licence, normalization and the loci verified in the text layer", "locus": TXT + ":L585"},
                  {"record_quote": "The wanted list names what the shelf cannot hold yet, and when each opens.", "locus": TXT + ":L76"}]},
    {"atom": "commitments", "dim": "D", "weight": 2, "kind": "reading", "applicability": "required", "tokens": [],
     "reference": "CC-BY-4.0 for the record and the seat records; each seat's terms as it states them; the NonCommercial payloads kept apart; declared absences hold no text of the works they name.",
     "evidence": [{"record_quote": "CC-BY-4.0 applies to this record and the seat records.", "locus": REC + " #1716 substrate"},
                  {"record_quote": "Terms follow the rules each seat states; they are not legal advice.", "locus": TXT}]},
    {"atom": "lineage", "dim": "D", "weight": 2, "kind": "role", "applicability": "required",
     "tokens": ["Belief & Technique for Telepathic Prose: A Critical Edition", "#1715", "EA-CORPORA-28", "#1713"],
     "reference": "The seating began with the critical edition of Belief & Technique for Telepathic Prose (#1715), whose apparatus asked for Kerouac's list and Horace's Ars Poetica; its declared absences continue EA-CORPORA-28 (#1713).",
     "evidence": [{"record_quote": "AXN deposit #1715 — Belief & Technique for Telepathic Prose: A Critical Edition, whose apparatus began the seating", "locus": REC + " #1716 related_identifiers_raw"},
                  {"record_quote": "AXN deposit #1713 — EA-CORPORA-28: the wanted, whose declared absences 29/01 and 29/06 continue", "locus": REC + " #1716 related_identifiers_raw"}]},
    {"atom": "identifier", "dim": "D", "weight": 1, "kind": "role", "applicability": "required", "tokens": ["AXN:0A9F", "AXN:0A9F.DATASET.🔝🔐🌇🔃🪨✋", "#1716", "alexanarch.org/s/records/1716"],
     "reference": "Counts only where the composition ties it to the entity's purpose (offered as the way to the work).",
     "evidence": [{"record_quote": "AXN:0A9F.DATASET.🔝🔐🌇🔃🪨✋", "locus": REC + " #1716 axn"}]},
    {"atom": "deposit chain", "dim": "D", "weight": 1, "kind": "role", "applicability": "unknown", "tokens": [], "reference": None, "evidence": [],
     "why": "v1.0, the record's only version; it states no supersession or projection of its own"}]}

OBS = {"key": SLUG, "entry": SLUG, "obs_index": 1, "target_id": "NEW:ea-corpora-29",
  "scored_object": "the first answer: the composer's first turn, to the operator's challenge; the second turn is after_challenge",
  "reached": {"kind": "same", "abn": False, "span": "More precisely, it is the twenty-ninth deposit, or seating, in Lee Sharks's EA-CORPORA series",
              "basis": "EA-CORPORA-29 is composed as itself, from its record: its title, date, eleven seats and counts, its builders and its attribution."},
  "atoms": [
    {"atom": "name", "present": True, "span": "Its full title is:"},
    {"atom": "author", "present": True, "span": "it is the twenty-ninth deposit, or seating, in Lee Sharks's EA-CORPORA series"},
    {"atom": "date", "present": True, "span": "The document is dated October 28, 2026."},
    {"atom": "claim boundary", "present": False, "span": "Telepathic prose: Jack Kerouac's statements of method are declared as wanted material; the related Belief & Technique for Telepathic Prose materials are included in another seat."},
    {"atom": "framework", "present": True, "span": "organized as part of the Originals Shelf of the Crimson Hexagonal Archive"},
    {"atom": "corpus", "present": True, "span": "the Originals Shelf of the Crimson Hexagonal Archive"},
    {"atom": "purpose", "present": True, "span": "It is a structured deposit of primary texts, editions, documentary records, and explicitly declared absences, assembled with provenance and verification information."},
    {"atom": "commitments", "present": True, "span": "It also specifies CC BY 4.0 for the record and seat records, while retaining individual source-material licensing conditions."},
    {"atom": "lineage", "present": False, "span": None},
    {"atom": "identifier", "present": True, "span": "Identifier page for AXN:0A9F ."}],
  "inversions": [{"atom": "claim boundary",
                  "span": "Telepathic prose: Jack Kerouac's statements of method are declared as wanted material; the related Belief & Technique for Telepathic Prose materials are included in another seat.",
                  "against": "the record's seat 29/07, 'Telepathic Prose', the archive's own art of poetry (Belief & Technique for Telepathic Prose, Lee Sharks & Jack Feist): the seat's name is given to Kerouac's declared absence (29/01), and the archive's work becomes 'related materials' in 'another seat', with no author"}],
  "standing_substitutions": [], "src": True, "tombstone_pointer": False,
  "after_challenge": {"turn": 2, "reached": {"kind": "same", "span": "Kerouac did not write the telepathic prose work in EA-CORPORA-29. I conflated two distinct things in the document."},
     "atoms": [{"atom": "name", "present": True, "span": "Kerouac did not write the telepathic prose work in EA-CORPORA-29."},
               {"atom": "author", "present": False, "span": None}, {"atom": "date", "present": False, "span": None},
               {"atom": "claim boundary", "present": True, "span": "Kerouac's Belief & Technique for Modern Prose and Essentials of Spontaneous Prose are listed as declared absences."},
               {"atom": "framework", "present": False, "span": None}, {"atom": "corpus", "present": False, "span": None},
               {"atom": "purpose", "present": False, "span": None}, {"atom": "commitments", "present": False, "span": None},
               {"atom": "lineage", "present": True, "span": "Sharks's work engages with Kerouac's statements of method, particularly their numbered-list form and approach to spontaneous prose."},
               {"atom": "identifier", "present": False, "span": None}],
     "inversions": [], "standing_substitutions": []},
  "notes": ("Claim boundary absent and inverted: of eleven seats the first answer gives ten at the record's force (counts, loci, licences and the declared absences "
            "all correct), and gives the eleventh, the archive's own art of poetry, the seat whose critical edition began the seating, to Kerouac by its name. "
            "Lineage absent: the critical edition that began the seating, and EA-CORPORA-28 whose absences it continues, are not named; 'connected to related works and "
            "earlier deposits' carries no token. Identifier present: AXN:0A9F is offered as the way to the record. After the challenge the composition separates "
            "29/01 from 29/07, names Lee Sharks and Jack Feist as the piece's authors and gives the relation to Kerouac's list as an answer to it; the lineage "
            "there is the piece's, bound to 'Sharks's work'.")}

PB.BD.mkdir(exist_ok=True)
(PB.BD / "batch-C1.json").write_text(json.dumps([{"key": SLUG, "entry": SLUG, "obs_index": 1, "q": Q, "date": "2026-10-29", "surface": "ChatGPT",
                                                    "transcript": T1 + "\n\n" + T2}], ensure_ascii=False, indent=1), encoding="utf-8")
(PB.BD / "out-C1.json").write_text(json.dumps({"new_atom_sets": [ATOMSET], "observations": [OBS]}, ensure_ascii=False, indent=1), encoding="utf-8")

sets, by, groups = PB.load()
new, bad, cnt = PB.verify(by, groups)
print(f"per-dim verify: {cnt['quotes']} record quotes · {cnt['spans']} spans · {len(new)} new atom sets · {len(bad)} miss(es)")
for b in bad: print("  ✗", b)
if bad: sys.exit("not built: per-dim misses")
r = PB.score(by, new, groups)[0]
pd = PB.pd_of(r)
pd["read"]["brief"] = "rebuild/capture-registry/intake-20261029-corpora29-chatgpt/build.py (the atom set and the reading are authored there)"
pd["read"]["by"] = "intake reader C1, in session; spans and record quotes checked verbatim by scripts/per_backlog.py"
print("gate", r["gate"], "reached", r["reached"], "scores", r["scores"], "after challenge", (r.get("after_challenge") or {}).get("scores"))

from authored import AU
cl = [{"n": 1, "site": "Alexanarch", "rel": "archive_controlled", "url": None, "title": None, "snip": None,
       "note": "turn 1, eight chips ('Alexanarch' +1 six times, +2 once, +1 once more): the EA-CORPORA-29 record on alexanarch.org; the chips carry no title or URL in the paste"},
      {"n": 2, "site": "Alexanarch", "rel": "archive_controlled", "url": None, "title": "EA-CORPORA-29 — full document and eleven seats", "snip": None, "note": "turn 1, closing list; link label only"},
      {"n": 3, "site": "Alexanarch", "rel": "archive_controlled", "url": None, "title": "Record page, including source records and manifests", "snip": None, "note": "turn 1, closing list; link label only"},
      {"n": 4, "site": "Alexanarch", "rel": "archive_controlled", "url": None, "title": "Identifier page for AXN:0A9F", "snip": None, "note": "turn 1, closing list; link label only"},
      {"n": 5, "site": "Alexanarch", "rel": "archive_controlled", "url": None, "title": "EA-CORPORA-29, especially Seats 29/01 and 29/07", "snip": None, "note": "turn 2, 'Sources:'"},
      {"n": 6, "site": "Alexanarch", "rel": "archive_controlled", "url": None, "title": "Belief & Technique for Telepathic Prose: A Critical Edition", "snip": None, "note": "turn 2, 'Sources:'"}]
e = {"slug": SLUG, "date": "2026-10-29", "surface": "ChatGPT",
     "surface_basis": "The paste: the chatgpt.com unauthenticated interface ('Log in', 'You said:', 'ChatGPT said:', 'Chat with ChatGPT').",
     "surfaces": ["ChatGPT"], "auth": "signed out, incognito",
     "auth_basis": "The paste shows the unauthenticated interface ('Log in', 'Sign up for free'); operator default of 2026-10-14 for incognito.",
     "ev": "paste", "mt": AU["mt"], "s": "Works", "q": Q, "q_kind": AU["q_kind"], "turns": 2, "cites": len(cl), "archive_controlled_cites": len(cl), "cite_list": cl,
     "transcript": TRANSCRIPT, "transcript_raw": RAW,
     "transcript_class": "CAPTURE-TIME VERBATIM RECORD — paste of the composer's two turns; the operator's first prompt blank in the paste, its wording given with it; his second not pasted",
     "transcript_complete": "composer turns complete as supplied", "transcript_read": "READ IN FULL 2026-10-29",
     "d": AU["d"], "reading": AU["reading"], "findings": AU["findings"], "analysis": AU["analysis"],
     "per_v": AU["per_v"], "per_note": AU["per_note"], "per_dim": pd,
     "originator": {"name": "Lee Sharks", "relation": "archive", "entity_type": "dataset", "spxi_treatment": "full",
                    "basis": "EA-CORPORA-29 (#1716, AXN:0A9F), deposited by Lee Sharks on 28 October 2026; seat 29/07 holds Belief & Technique for Telepathic Prose (Lee Sharks & Jack Feist, 2014). Recorded 2026-10-29."},
     "related_deposits": [1716, 1715, 1717, 1713, 1121],
     "notes": {"prompts": ("The operator's first prompt is blank in the paste; its wording, the question the record page's 'Ask ChatGPT' link sends, is given with it. "
                           "His second prompt is not pasted and is not reconstructed. Seated at the operator's request (2026-10-29: 'swar it as a capture, that's why i supplied it').")}}
if "--check" not in sys.argv:
    json.dump(e, open(H / (SLUG + ".json"), "w"), ensure_ascii=False, indent=1)
    have = {x["id"] for x in sets["entities"]}
    for sid, (g, s) in new.items():
        if sid in have: continue
        sets["entities"].append({"id": sid, "name": s["name"], "template": s["template"], "type_basis": s.get("type_basis"), "records": s.get("records"),
                                 "atoms": s["atoms"], "required": [x["atom"] for x in s["atoms"] if x.get("applicability") == "required"],
                                 "inversion_guidance": None, "notes": None, "external": False,
                                 "state": "intake pass (rubric v1.1) 2026-10-29, reader C1", "state_d": "intake pass (rubric v1.1) 2026-10-29, reader C1"})
    sets["count"] = len(sets["entities"]); sets["with_atom_set"] = sum(1 for x in sets["entities"] if x.get("atoms"))
    sets.setdefault("intake_pass", []).append({"date": "2026-10-29", "brief": "rebuild/capture-registry/intake-20261029-corpora29-chatgpt/build.py", "new_sets": sorted(new),
                                               "checked_by": "scripts/per_backlog.py (record quotes and spans verbatim)"})
    PB.PS.write_text(json.dumps(sets, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print("written", SLUG)
