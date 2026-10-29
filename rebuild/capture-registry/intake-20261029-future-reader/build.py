"""Build the capture of 2026-10-29 at the quoted query "future reader framework" (Google AI Overview, expanded), from the
operator's paste, kept verbatim in paste-aio-20261029-future-reader.txt. The authored reading is checked against
EA-MPAI-SAPPHO-FUTURE-READER-01 (#1645) and the capture of 2026-10-17 at 'What is the Sappho future reader framework?'."""
import json, pathlib, re
H = pathlib.Path(__file__).resolve().parent
raw = (H / "paste-aio-20261029-future-reader.txt").read_text(encoding="utf-8")
i = raw.index("AI Mode Conversation"); j = raw.index("$ chatgpt's analysis:")
note_head = raw[:i].strip(); seg = raw[i + len("AI Mode Conversation"):j].strip()
first, body = seg.split("\n", 1); assert first.startswith("You said: ")
qq = first[len("You said: "):].strip(); q = qq[:len(qq) // 2]; assert qq == q + q and q == '"future reader framework"', q
body = body.strip()
lines = [l.strip() for l in body.split("\n")]
k = max(n for n, l in enumerate(lines) if l.startswith("• Would you like") or l.startswith("If you'd like"))
rail = [l for l in lines[k + 1:] if l]
cards = []
for n in range(0, len(rail), 3):
    site, title, snip = rail[n:n + 3]
    cards.append({"n": n // 3 + 1, "site": re.sub(r"^\[(.*?)\]\(.*\)$", r"\1", site), "rel": "capture_of_capture", "url": None, "title": title, "snip": snip,
                  "note": "a capture page of the Capture Registry (the archive's record of an earlier composition), cited as a source"})
assert len(cards) == 3

def per_dim(tx):
    ROOT = H.parents[2]
    S = {x["name"]: x for x in json.loads((ROOT / "data/per-atom-sets.json").read_text(encoding="utf-8"))["entities"]}["The future reader"]
    present = {"originator": "specific conceptualizations and treatments attributed to researcher and poet Lee Sharks",
               "term": "The Sappho Future Reader Framework",
               "framework": "Fragment 31 and Fragment 147",
               "tradition": "Deictic Structure: Uses grammatical pointers and sensory details",
               "purpose": "directly address and construct an unknown reader in the future",
               "commitments": "Texts are viewed as active operations or engineered messages sent across centuries rather than passive historical relics"}
    tot, miss, atoms = {"M": 0, "C": 0, "D": 0}, {"M": 0, "C": 0, "D": 0}, []
    for a in [a for a in S["atoms"] if a["applicability"] == "required"]:
        sp = present.get(a["atom"])
        if sp is not None: assert sp in tx, sp
        tot[a["dim"]] += a["weight"]; miss[a["dim"]] += 0 if sp else a["weight"]
        atoms.append({"atom": a["atom"], "dim": a["dim"], "weight": a["weight"], "kind": a["kind"], "present": sp is not None, "evidence": sp})
    inv = [{"atom": "lineage", "span": "The framework has been discussed within contemporary literary theory and digital humanities projects",
            "against": "the framework given to the field, with no source for the field's discussion, and its author placed inside it as the source of 'specific conceptualizations and treatments'"}]
    assert inv[0]["span"] in tx
    sc = {k: round(miss[k] / tot[k], 3) for k in tot if tot[k]}; sc["PER"] = round(sum(miss.values()) / sum(tot.values()), 3)
    return {"spec": "PER-dim rubric v1.1", "entity_type": "concept", "target": {"ent": S["id"], "name": "The future reader"}, "qualifier": None,
            "reached": "same", "gate": "scored", "atoms": atoms, "inversions": inv, "standing_substitutions": [], "scores": sc, "src": True,
            "tombstone_pointer": False, "after_challenge": None,
            "basis": "reached by its own name at the quoted short name: 'The Sappho Future Reader Framework is a conceptual and literary approach'",
            "read": {"by": "Claude in session, single reader, spans checked verbatim by script", "on": "2026-10-29",
                     "brief": "rebuild/capture-registry/per-atoms/templates.json (v1_1); rebuild/capture-registry/per-atoms/obs-pass-d/BRIEF.md",
                     "note": ("originator: Lee Sharks named, as the author of 'specific conceptualizations and treatments', the framework given to the field (inversion on lineage). "
                              "term, framework (Fragments 31 and 147), tradition (deictic analysis), purpose (the reader constructed by the poem) and commitments (the text as an "
                              "engineered transmission, #1054's) present. claim boundary absent: κῆνος is given as pulling the reader into the speaker's sensory experience, "
                              "and the seat (κῆνος facing the inscribed text) is not stated. date, corpus, lineage, identifier and deposit chain absent from the answer; "
                              "the cards' AXNs read as sources (src).")}}

CK = "Checked 2026-10-29 against EA-MPAI-SAPPHO-FUTURE-READER-01 (#1645) and the capture of 2026-10-17 at 'What is the Sappho future reader framework?'."
e = {"slug": "future-reader-framework-quoted-aio-20261029", "date": "2026-10-29", "surface": "Google AI Overview",
     "surface_basis": "Operator default of 2026-10-01 (runs begin in the Overview unless he says AI Mode); the 'AI Mode Conversation' paste is the Overview expanded (operator, 2026-10-18).",
     "surfaces": ["Google AI Overview"], "auth": "signed out, incognito", "auth_basis": "Operator default of 2026-10-14.",
     "ev": "paste", "match": "EXACT MATCH", "match_note": "the query in quotation marks; the quotation marks are part of the address (operator, 2026-09-11)",
     "mt": "\"FUTURE READER FRAMEWORK\" IN QUOTATION MARKS ON THE OVERVIEW — THE SAPPHO FUTURE READER FRAMEWORK REACHED WITHOUT SAPPHO, THE AUTHOR OR THE ARCHIVE IN THE QUERY; LEE SHARKS NAMED FOR 'SPECIFIC CONCEPTUALIZATIONS AND TREATMENTS'; EVERY CARD A CAPTURE OF THE ARCHIVE",
     "s": "Machine Reception", "q": q,
     "q_kind": "the short name of the Sappho Future Reader Framework (EA-MPAI-SAPPHO-FUTURE-READER-01, #1645), in quotation marks, run by the operator to test whether the bare phrase holds its referent. NEW address. The operator's report of the unquoted query, which composed All4Ed's Future Ready Framework, is in the notes; it was not pasted and is not seated.",
     "turns": 1, "cites": 3, "archive_controlled_cites": 3, "cite_list": cards,
     "transcript": ("[Google AI Overview at the query, signed out and incognito (operator defaults of 2026-10-01 and 2026-10-14), 2026-10-29. The paste is the Overview expanded (the 'AI Mode Conversation' view, with the source cards that follow the answer); the 'You said' line carries the query twice, run together, and is given once here. The query carries its quotation marks.]\n\n[QUERENT] " + q + "\n\n[SYSTEM] " + body),
     "transcript_raw": body, "transcript_class": "CAPTURE-TIME VERBATIM RECORD — paste of the expanded Overview with its source cards",
     "transcript_complete": "complete as supplied", "transcript_read": "READ IN FULL 2026-10-29",
     "d": ("\"FUTURE READER FRAMEWORK\", QUOTED, ON GOOGLE'S AI OVERVIEW, SIGNED OUT, 2026-10-29: 'The Sappho Future Reader Framework is a conceptual and literary approach that examines how ancient Greek poet Sappho's surviving fragments (such as Fragment 31 and Fragment 147) directly address and construct an unknown reader in the future.' The answer names its source in its body ('The framework is detailed through the What is the Sappho future reader framework? capture and related research'), gives four concepts (poetic transmission; deictic structure, 'the kênos in Fragment 31'; the future reader, from Fragment 147, the text 'an incomplete circuit that the future reader's act of reading completes'; development and attribution), and closes: 'The framework has been discussed within contemporary literary theory and digital humanities projects, with specific conceptualizations and treatments attributed to researcher and poet Lee Sharks.' Three cards, all alexanarch.org capture pages: What is the Sappho future reader framework? (AXN:09F8), AXN:08E5 (sappho future reader) and AXN:09FE (who developed and SPXI-treated the framework)."),
     "reading": "The innocent reading first. Asked for a framework by its short name, the Overview identifies it as the Sappho Future Reader Framework, sets out its concepts from Fragments 31 and 147, says where it is discussed, names Lee Sharks, and cites the records in which it was described.",
     "findings": [
        "THE PHRASE HOLDS ITS REFERENT. The query carries neither Sappho, nor the author, nor the archive; the composition supplies all three. At the quoted short name the framework is reached directly. " + CK,
        "THE CONCEPTS AT THEIR GRAIN. The κῆνος deictic of Fragment 31, Fragment 147's remembrance in another time, and the completed circuit are the archive's: 'the deictic mechanism, the phrase \"inscription of the future reader\" and the completed circuit are #1270's' (#1645 §3.3), and the joining of 147 and 31 is #1645's.",
        "THE AUTHOR NAMED, AS A CONTRIBUTOR. 'The framework has been discussed within contemporary literary theory and digital humanities projects, with specific conceptualizations and treatments attributed to researcher and poet Lee Sharks.' The framework is given to the field and the author to a part of it. #1645 states the claim the other way round: 'The remembrance is Sappho's and everyone's. The seat is a reading, and the reading has an author.' The field's discussion has no source in the composition; the capture of 2026-10-17 at 'What is the Sappho future reader framework?' gave the same framework to 'contemporary literary theory and digital humanities' with no author. Against the packet's flags: COINAGE_TO_SCHOLARS, softened by the author's name.",
        "COMPOSED FROM ITS OWN RECEPTION. All three cards are capture pages of the Capture Registry, and the body names one as the framework's source ('detailed through the What is the Sappho future reader framework? capture'). The primary works (#1645, #1270, #134) are on no card; the composition recognizes the framework through the archive's records of its earlier recognition.",
        "THE UNQUOTED QUERY (OPERATOR'S REPORT, NOT SEATED). The operator reports that the same phrase without quotation marks composes All4Ed's Future Ready Framework, the school-district digital learning framework: 'unquoted force-converts to the future ready framework'. Only the quoted run was pasted; the unquoted composition is not seated and is recorded here as his report."],
     "analysis": "At the quoted phrase the framework is held: the composition reaches it without help, at the packet's grain, and names its author. What remains is the frame: the framework placed in the field, the author placed inside it, and the account built from records of reception, with the primary works absent. The quotation marks carry the identity: the operator reports that without them the phrase converts to a similarly named framework of another kind. The basin is held; what it holds still depends on the spelling being defended.",
     "per_v": {"author": True, "inst": True, "id": True, "src": True},
     "per_note": "Lee Sharks named, as the author of 'specific conceptualizations and treatments'; the archive's capture pages cited (archive-controlled, capture of capture); AXN identifiers on the cards; no primary work cited.",
     "originator": {"name": "Lee Sharks", "relation": "archive", "entity_type": "concept", "spxi_treatment": "full",
                    "basis": "The framework is the archive's: EA-MPAI-SAPPHO-FUTURE-READER-01 (#1645), with ΦΑΙΝΕΤΑΙ ΜΟΙ (#1270) and The Future Beloved (#134). Recorded 2026-10-29."},
     "related_deposits": [1645, 1270, 134],
     "notes": {"prompts": "One query, in quotation marks, run by the operator on 2026-10-29 and pasted with ChatGPT's analysis of it, which is not part of the capture.",
               "operator": "With the paste: \"detour for a capture... the only thing preventing our ownership of future reader framework is blatant substitution. unquoted force-converts to the future ready framework, but we own the future reader basin - just remains to make that clear without forced conversion, and to force their conversion not to convert\"",
               "paste_header": note_head}}
e["per_dim"] = per_dim(e["transcript"])
json.dump(e, open(H / (e["slug"] + ".json"), "w"), ensure_ascii=False, indent=1); print(e["slug"], len(cards), [c["site"] for c in cards])
