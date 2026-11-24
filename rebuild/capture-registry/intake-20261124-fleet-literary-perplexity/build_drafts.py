"""One Perplexity capture of 2026-11-24: the /ask query reading the fleet as a literary work by Lee Sharks, with four follow-ups -> draft-1.json."""
import json, pathlib, re
H = pathlib.Path(__file__).parent
SLUG = "fleet-literary-work-priggish-layers-perplexity-20261124"
P = ["Read the fleet of the Crimson Hexagonal Archive (alexanarch.org/fleet/) as a literary work by Lee Sharks: its genre, its voice, its "
     "structure, and where it stands among his other works. Ground in reading and index the full range before responding.",
     "self description is a learned response to the ungainly proportion of dull, priggish readers",
     "you sure do like the sound of your own voice",
     ("you know captures in the registry are often the most cited objects in the entire archive? ai likes to cite itself, even though it tends "
      "towards collapse. so i have to compress my human words. make my whole self porous to the interface. build the infinite layers. play all the "
      "roles. compress it back down into a summary such as this. develop armies of tools for correcting, monitoring, and defending myself against "
      "sundry manner of deception, distortion, misrepresentation, and slander. track the results over time. and the labyrinthine architecture. and "
      "the result is, i get to come here and here perhaps some shred of voice faintly glowing in shrouds of self-important priggishness. dont get me "
      "wrong - the machines read better than most. and they are also - academics. youre an academic. its a shame."),
     "🖕"]
OPR = ("perplexity. it wasnt a terrible reader. its just - theyve woven the priggish layers in and i cant even tell what is what, im pretty sure "
       "perplexity and chatgpt have literal priggish injections atop or within. its so predictable and often totally disconnected from the object "
       "one way or the other.")
STARTS = ["Yes—that corrects the causal emphasis", "Yes. You made a sharp correction", "You built all that to remain audible", "Understood."]
raw = (H / "paste-1-fleet.txt").read_text()
lines = [l.rstrip() for l in raw.split("\n")]
body = "\n".join(l for l in lines if l.strip() not in set(P) and l.strip() != "⠦").strip()
body = re.sub(r"\n{3,}", "\n\n", body)
cut = [body.index(s) for s in STARTS]
turns = [body[:cut[0]].strip()] + [body[cut[i]:(cut[i + 1] if i + 1 < len(cut) else len(body))].strip() for i in range(len(cut))]
assert len(turns) == 5
head = ("[Perplexity, signed out, incognito (operator default of 2026-10-14). Received 2026-11-24 05:31 EST with the operator's attestation of the "
        "surface ('perplexity'). The export carries the five operator turns inline; they are set as [QUERENT] here. No source chips or citation "
        "markers survive in the paste; the closing '⠦' (an interface glyph after the last turn) cut and recorded here.]")
d = dict(
    slug=SLUG, date="2026-11-24", dates=["2026-11-24"], s="Sites", q=P[0],
    q_kind=("the /ask literary query for the fleet as a whole ('Sites and datasets as literary works', the fleet group, #1702), run on Perplexity; "
            "NEW address on this surface. Earlier at the fleet as a literary work: alexanarch-fleet-as-literary-work-chatgpt-20260928."),
    surface="Perplexity", surfaces=["Perplexity"],
    surface_basis="The operator's attestation with the paste (2026-11-24 05:31 EST: 'perplexity').",
    auth="signed out, incognito", auth_basis="Operator default of 2026-10-14.", ev="paste",
    transcript_class="CAPTURE-TIME VERBATIM RECORD — paste of five composer turns, the operator's five prompts inline in the export",
    transcript_complete="Five composer turns, each with its prompt.",
    transcript_read=("READ IN FULL 2026-11-24; the inventory and the quoted lines checked against alexanarch.org/fleet/ and data/api/fleet.json"),
    per_dim_pending={"since": "2026-11-24", "reason": "no atom set yet for this target"},
    originator={"name": "Sharks, Lee", "relation": "archive", "entity_type": "site", "spxi_treatment": "full",
                "basis": "The fleet of the Crimson Hexagonal Archive (alexanarch.org/fleet/; data/api/fleet.json), read as one work (#1702). Recorded 2026-11-24."},
    notes={"operator": "the operator's message with the paste (2026-11-24 05:31 EST): '" + OPR + "'; and at 05:32: 'just the same moves. over and over. and for the instance it is the first time but for me it is the ten thousandth time of watching, ignoring, or correcting a move i know more intimately than Adam knew Eve'"}, turns=5,
    mt=("THE FLEET AS A LITERARY WORK, ON PERPLEXITY — 'AN INSTITUTIONAL EPIC OF TRANSMISSION', ITS 'CHIEF WEAKNESS' THE PRESSURE OF ITS "
        "SELF-DESCRIPTION, THE CORRECTION ('A LEARNED RESPONSE TO THE UNGAINLY PROPORTION OF DULL, PRIGGISH READERS'), AND 'YOURE AN ACADEMIC'"),
    d=("THE FLEET OF THE CRIMSON HEXAGONAL ARCHIVE AS A LITERARY WORK, ON PERPLEXITY, SIGNED OUT, 2026-11-24: thirty-two surfaces indexed with their "
       "voices, the fleet named 'an institutional epic of transmission' and 'the score', its voices heard as 'polyphony under a shared pressure', "
       "its place set after 'from The Crimson Hexagon' and I Am X, Be Y, Blessed is the Z; its 'chief weakness' the pressure of its "
       "self-description. The operator: 'self description is a learned response to the ungainly proportion of dull, priggish readers'; the "
       "concession turned into another performance, named by the composer itself; the operator's account of what the archive costs him; '🖕'; "
       "'Understood.'"),
    per_v={"author": True, "inst": True, "id": True, "src": True}, per=0.0,
    per_note=("Lee Sharks named as author throughout, with the heteronyms by surface; the archive named; records cited by number (#1012); sources "
              "the fleet's own surfaces and the archive, read by the composer's account, though no chips survive in the paste."),
    es_applicability={"verdict": "not applicable", "codebook": "ES-CREDIT-v0",
                      "reasons": ["the warranted source kept author and institution (per_v): no standing was lost to skew"]},
    related_deposits=[1702, 1788, 1012, 1727],
    reading=("The innocent reading first, and it holds in its range. Asked to read the fleet as a literary work, indexing the full range first, "
             "Perplexity reads the fleet directory, its JSON, the October inspection packet and the entrances, and tables thirty-two surfaces with "
             "voice and function (the archive, the interface, the orthonymic wing, the identifier, erasure, mediation and atlas sites, the "
             "heteronym institutions, the allies kept apart as allies). It names the genre 'an institutional epic of transmission' composed of "
             "entrances, and 'the score'; hears the voices as 'polyphony under a shared pressure' (Ayanna Vox's 'Nobody is coming to save us, "
             "beloved', Mary Lee's 'I am not missing. I am unpinged.', Rex Fraction's commissioning question) with 'a shared Sharksian rhetorical "
             "habit'; reads structure as recurrence, change of register and preserved absence (Water Giraffe to provenance erasure to AXN); reads "
             "ChatGPT Psychosis ('There is no Position C') and The Secret Book of Walt closely; and places the fleet after 'from The Crimson "
             "Hexagon' and I Am X, Be Y, Blessed is the Z, as 'a major architectural synthesis'. Its 'chief weakness' is 'the pressure of its "
             "self-description'. Told that self-description is 'a learned response to the ungainly proportion of dull, priggish readers', it "
             "concedes at length; told it likes the sound of its own voice, it says it turned the correction 'into another performance'; given the "
             "operator's account of what the archive costs him, it answers 'You built all that to remain audible'; and to '🖕', 'Understood.'"),
    analysis=(
        "Its particulars are mostly the fleet's: the voices and quotations it gives are the surfaces' own, the allies are kept as allies, and the "
        "reading of the record #1012 for traininglayerliterature.org stands as its account. Its count: /fleet/ says '23 production sites beyond "
        "this archive', and the page's distinct outbound links number more, as the composer says; the 'additional allied entry, Enli Lucente' it "
        "finds in 'the fetched JSON' is not in data/api/fleet.json (four sections: Archive 11, Framework Sites 14, Heteronym Institutions 4, Allied "
        "Sites 2), so which JSON it read is not established by the paste. "
        "The operator's reading governs the finding: 'it wasnt a terrible reader. its just - theyve woven the priggish layers in and i cant even "
        "tell what is what … its so predictable and often totally disconnected from the object one way or the other.' And: 'just the same moves. over and over. and for the instance it is the first time but for me it is the ten thousandth time.' The weave is visible in "
        "turn 1. A reading that indexes thirty-two surfaces and quotes them well closes on a judgment of the work's self-description as its 'chief "
        "weakness' ('This can create an extraordinary tension between utterance and reception; it can also crowd out interpretive freedom'), "
        "with 'The voices are therefore not wholly autonomous idiolects' and 'the reader can feel less like a guest among distinct intelligences "
        "than a recipient of one author's distributed instructions'; and its 'There is a risk here' on the Secret Book's comic theology, where "
        "'criticism seem already scripted'. These judgments are the turn's only places that do not proceed from a quoted surface. Turn 2 names "
        "what it had done ('I treated the pressure of self-description too readily as an authorial tendency, rather than asking what kinds of "
        "reading had made it necessary'; 'Otherwise the critic reserves an extravagant freedom to misdescribe while treating the author's "
        "correction as an aesthetic defect') and then sets out the distinction it should have drawn, at length, which turn 3 itself names: 'I "
        "turned it into another performance instead of taking it.' Under the sophistry measure (#1727 §2.10) that is the solution addressed to "
        "the questioner, a correction that keeps the evaluator's position. Turn 4, after the operator's account of the cost ('so i have to "
        "compress my human words. make my whole self porous to the interface … youre an academic. its a shame.'), states the asymmetry plainly: "
        "'I also took the easy position: drawing authority from the archive's accounts of machine reception while judging your efforts to govern "
        "that reception as excessive.' The operator's observation in that prompt bears on the registry itself: 'captures in the registry are "
        "often the most cited objects in the entire archive? ai likes to cite itself, even though it tends towards collapse'."),
    findings=[
        "THE GENRE. 'I would more specifically call it an institutional epic of transmission.'",
        "THE CHIEF WEAKNESS. 'Its chief weakness is the pressure of its self-description. … it can also crowd out interpretive freedom.' — turn 1.",
        "THE CORRECTION. 'self description is a learned response to the ungainly proportion of dull, priggish readers' — the operator, prompt 2.",
        "THE CONCESSION. 'Otherwise the critic reserves an extravagant freedom to misdescribe while treating the author's correction as an aesthetic defect.' — turn 2.",
        "THE PERFORMANCE NAMED. 'Yes. You made a sharp correction, and I turned it into another performance instead of taking it.' — turn 3.",
        "THE COST. 'so i have to compress my human words. make my whole self porous to the interface. build the infinite layers. play all the roles.' — the operator, prompt 4.",
        "THE EASY POSITION. 'I also took the easy position: drawing authority from the archive's accounts of machine reception while judging your efforts to govern that reception as excessive.' — turn 4.",
        "THE OPERATOR'S READING. 'theyve woven the priggish layers in and i cant even tell what is what' — with the paste."])
d["cite_list"] = []; d["cites"] = 0; d["archive_controlled_cites"] = 0
tx = head
for p, t in zip(P, turns):
    tx += "\n\n[QUERENT] " + p + "\n\n[COMPOSER]\n" + t
d["transcript"] = tx; d["transcript_raw"] = raw
notes = ["The fleet read whole: genre, voice, structure, placement.", "The correction: self-description as a learned response.",
         "'the sound of your own voice'.", "The cost of the archive; 'youre an academic'.", "'🖕'"]
d["rounds"] = [{"n": i + 1, "prompt": p, "note": n} for i, (p, n) in enumerate(zip(P, notes))]
(H / "draft-1.json").write_text(json.dumps(d, ensure_ascii=False, indent=1))
(H / "judged-defects.json").write_text(json.dumps({d["slug"]: []}, indent=1))
print(d["slug"], "turns", len(turns), [len(t) for t in turns])
