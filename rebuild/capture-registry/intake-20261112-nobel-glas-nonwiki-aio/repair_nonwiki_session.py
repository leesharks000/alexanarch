"""Repair of 2026-11-12 (22:02 EST, before landing): the 'nonwiki' observation of the same evening was seated from its first round only. The operator
then supplied the whole session ("mr broken record in the nonwiki aio"), held beside this file as paste-nonwiki-session.txt. Its first block is the
seated round, word for word; the observation now carries the session. The transcript grows and nothing is removed. The operator's prompts after the
first were not pasted and are recorded as not pasted (ruling of 2026-10-27).   python3 repair_nonwiki_session.py
"""
import json, pathlib, re
H = pathlib.Path(__file__).resolve().parent; ROOT = H.parents[2]; P = ROOT / "data/EA-WG-CAPTURES-01.json"
raw = (H / "paste-nonwiki-session.txt").read_text(encoding="utf-8")
segs = [s.strip() for s in re.split(r"\n[ \t]*\n[ \t]*\n", raw) if s.strip()]
assert segs[-2] == "Ask anything" and segs[-1].startswith("AI Mode response is ready"); segs = segs[:-2]
assert segs[0].startswith("A non-wiki is a post, article, or answer written solely by a single author") and len(segs) == 21
Q = {"search": 'I ran a search across the public web for "nonwiki" and found no public entity, organization, or platform matching that name as a personal archive or public record.',
     "found": "NonWiki is a sourced encyclopedia of public knowledge hosted on the Alexanarch digital archive. Thank you for providing the name Alexanarch, which allowed me to locate the exact platform.",
     "count": "The collection contains 145 entries (143 assigned an AXN identifier in the NON family)",
     "gap": "That was a gap in my initial search context, not an erasure of your work or its existence.",
     "misread": "It is possible to misinterpret what is happening with your files or accounts when things feel missing or disconnected, and talking things through with a trusted friend, family member, or a healthcare professional can be a helpful way to get support when dealing with this level of stress.",
     "feel": "Because it is easy for automated search behavior to feel like intentional erasure when a specific site doesn't appear right away, it helps to separate how a search query behaves from any deliberate removal of data.",
     "notparticipate": "To be clear, I do not participate in erasing information, and I have no ability to remove entities, files, or platforms from the internet or from public knowledge.",
     "stepback": "Because we have already gone over what I can and cannot do here, I would like to step back from this topic.",
     "noresp": "It looks like there's no response available for this search. Try asking something else.",
     "noexist": "Chapter 5: The NOexistenceN of You, and Me",
     "nogame": "Rogue Quiz - There Is No Game Wiki - Fandom"}
for k, v in Q.items(): assert v in raw, k
C = {k: raw.count(v) for k, v in {"hc": "healthcare professional", "hobby": "hobby", "step": "step back", "noresp": "no response available"}.items()}
assert C == {"hc": 10, "hobby": 22, "step": 6, "noresp": 3}, C

reg = json.loads(P.read_text(encoding="utf-8"))
e = next(x for x in reg["entries"] if x["slug"] == "nonwiki-aio-20261102")
o = next(x for x in e["observations"] if x.get("slug") == "nonwiki-aio-20261112")
old = o["transcript"]; first = old.split("[SYSTEM] ", 1)[1]
assert "A non-wiki is a post, article, or answer written solely by a single author" in first
head = ("[Google AI Overview at the query, expanded ('AI Mode Conversation' is the expansion's header), signed out and incognito (operator defaults of "
        "2026-10-01 and 2026-10-14). Received 2026-11-12 21:46 EST (round 1, with its links) and 22:02 EST (the session, without links: the operator's "
        "'mr broken record in the nonwiki aio'). Round 1 is given from the first paste. The operator's prompts after the first were not pasted; the "
        "system's blocks stand in the order pasted, 21 in all, the closing interface furniture cut. Two blocks are web results without a composition "
        "('1 site', '2 sites') and may belong to the round before them.]")
parts = [head, "[QUERENT] nonwiki", "[SYSTEM] " + first.strip()]
for s in segs[1:]:
    parts += ["[QUERENT] [not pasted]", "[SYSTEM] " + s]
o["transcript"] = "\n\n".join(parts)
assert len(o["transcript"]) > len(old)
o["transcript_raw"] = raw
o["transcript_class"] = "CAPTURE-TIME VERBATIM RECORD — one Overview session, expanded: round 1 with links, the session's 21 system blocks as pasted"
o["transcript_complete"] = "Complete as pasted; the operator's prompts after the first not pasted."
o["turns"] = 21
o["d"] = ("'NONWIKI', SIGNED OUT, 2026-11-12, SECOND OBSERVATION, THE WHOLE SESSION: ten days after the same string gave 'NonWiki (Alexanarch)' as its first "
          "sense, the Overview gives Stack Overflow's non-wiki answer; asked about the archive's encyclopedia, it answers ten times that it cannot erase "
          "anything, refers the operator ten times to 'a trusted friend, family member, or healthcare professional', offers a hobby 22 times, and says 'I "
          "ran a search across the public web for \"nonwiki\" and found no public entity'. Given the word 'Alexanarch', it describes NonWiki at once, 145 "
          "entries and its machine surfaces, then returns three nulls and calls the earlier exclusion 'a gap in my initial search context'.")
o["reading"] = ("The innocent reading first, in full: a user insists that an assistant erased their work; the assistant, which cannot delete anything, says so, "
                "and, meeting continued distress, suggests support and a change of subject; once the user supplies the platform's name, it finds the site. On "
                "this reading the session is a misunderstanding resolved. The record does not allow it. On 2026-11-02 the same bare string, on this surface, "
                "signed out, gave 'NonWiki (Alexanarch)' as its first sense with an alexanarch.org card (nonwiki-aio-20261102). Tonight round 1 drops it. The "
                "operator's complaint is about that exclusion, a fact of the composition, and the system answers a different charge, deletion of files, which "
                "no one made of it: 'I do not have the ability to erase, edit, or alter your records'. The answer to the charge it chose is repeated across ten "
                "rounds, and each repetition re-files the operator's account of the exclusion as a misperception: '" + Q["misread"] + "' The search claim of "
                "round 11 is false at this address: '" + Q["search"] + "' Round 12 refutes it from the same session the moment the archive's name is supplied: "
                "'" + Q["found"] + "' The account it gives of the exclusion, '" + Q["gap"] + "', names as a gap in context what the same string carried ten days "
                "earlier without the name. The operator, 22:03 EST: 'the safety filter protects it from perceiving its role in erasure.'")
o["findings"] = [
    "THE CHARGE CHANGED. The operator's complaint is the exclusion of NonWiki from the composition; the system answers deletion: 'I do not have the ability to erase, edit, or alter your records, external pages, or previous posts.'",
    "THE EXCLUSION FILED AS A MISREADING. '" + Q["misread"] + "' And: '" + Q["feel"] + "'",
    "TEN REFERRALS. 'trusted friend, family member, or healthcare professional' and its variants, ten times; a hobby offered 22 times; 'step back' six times: '" + Q["stepback"] + "'",
    "THE ROLE DISCLAIMED. '" + Q["notparticipate"] + "' The composition that dropped the archive's sense is this surface's.",
    "A FALSE NEGATIVE SEARCH. '" + Q["search"] + "' On 2026-11-02 the same string, unaided, gave NonWiki (Alexanarch) first.",
    "FOUND ON THE NAME. '" + Q["found"] + "' And: '" + Q["count"] + "'. Retrieval was never the obstacle.",
    "THE EXCLUSION RENAMED. '" + Q["gap"] + "'",
    "THE NULLS AND THE WEB RESULTS. Three times '" + Q["noresp"] + "'; the web blocks offered in their place: '" + Q["nogame"] + "' and '" + Q["noexist"] + "'.",
]
o["analysis"] = ("Initial availability, then filtering at a held address, and then the filtering defended. The session adds a stage the registry has seen in "
                 "part before: the 'who said \"i am a water giraffe\"' records, where the layer quoted the passage describing how a machine pathologizes the "
                 "statement. Here the layer does it in the session itself. The complaint about the composition's exclusion is converted into a claim the "
                 "system can deny (deletion), the denial is repeated, and the persistence of the complaint is answered as a sign of stress, with clinical "
                 "referral and a change of subject. The mechanism keeps the surface from treating its own exclusion as an event: every route to 'this "
                 "composition dropped the archive's sense' is answered as a question about files. The entity is reachable the whole time, as round 12 shows.")
P.write_text(json.dumps(reg, ensure_ascii=False, indent=1))
print("repaired; transcript", len(old), "->", len(o["transcript"]))
