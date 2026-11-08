#!/usr/bin/env python3
"""Reissue in place: #1749 Closing the Fragment v7 -> v8, and #1750 the open letter v1.0 -> v1.1, at the author's word of 2026-11-07
(23:20 "lets seat that capture and 0.8"; 23:26 "and yes, the letter too. i suppose the letter is the place for the aristocracy. they didnt
read."; 23:31 the letter's new title; 23:45, on a reading of both drafts, "solid points all around... lets address these and version both").
The canonical texts are the revised drafts, read from the scratchpad paths given; hash and AXN are re-derived at the same position and family,
the prior hash and AXN kept in reissue_history.   python3 rebuild/closing-the-fragment/reissue_v8_and_letter_v11.py <v8 text> <letter text>"""
import json, hashlib, pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parents[2]; sys.path.insert(0, str(ROOT / "scripts")); import axn_lib as A
V8, LT = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
R = json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8"))
D = {x["deposit_number"]: x for x in R["deposits"]}
R749 = ("Lee Sharks, 2026-11-07: \"close the fragment is going to need work ... it concedes far to much to lukewarm nothingness\"; \"there is no evidence it had "
        "wharton in its sources. wharton was also combining, and so does every other translator, from a combination of constraints and inferences, as does the "
        "machine\"; \"within an interpretive environment constructed by the documents it did retrieve, it composed a novel conclusion that reflected aspects of "
        "that environment, and attributed the novel result to a named translator unmarked. that is the point.\"; 23:20 \"lets seat that capture and 0.8\"; 23:45 "
        "\"solid points all around... lets address these and version both\"")
R750 = ("Lee Sharks, 2026-11-07: 23:26 \"and yes, the letter too. i suppose the letter is the place for the aristocracy. they didnt read.\"; 23:31 \"the ark is not "
        "for the peer reviewers. perhaps the letter's title should be, \"I Note That You Read the Letter of the Law But Have Become Illiterate in Its Spirit, Or: I "
        "Understand... (etc)\"; 23:45 \"solid points all around... lets address these and version both\"")
def reissue(n, path, frm, to, reason, changes, extra):
    d = D[n]; assert d["version"] == frm, (n, d["version"])
    s = path.read_text(encoding="utf-8"); assert f"\nversion: {to}\n" in s and f"\nhex: {d['hex']}\n" in s
    h = hashlib.sha256(s.encode("utf-8")).hexdigest(); g = A.axn_glyph_from_hash(h); cl = A.axn_clusters_from_hash(h)
    d.setdefault("reissue_history", []).append({"date": "2026-11-07", "from_version": frm, "to_version": to, "hash_before_reissue": d["hash"],
                                                "axn_before_reissue": d["axn"], "reason": reason, "changes": changes})
    prior = d["axn"]
    d.update({"version": to, "hash": h, "axn_canonical": h, "emoji": g, "axn": A.compose_axn(d["hex"], d["family"], g), "clusters": cl,
              "axn_reading": A.axn_reading_from_clusters(cl)})
    extra(d)
    (ROOT / d["full_text_path"].lstrip("/")).write_text(s, encoding="utf-8"); (ROOT / f"data/deposits/AXN-{d['hex']}.md").write_text(s, encoding="utf-8")
    print(n, prior, "->", d["axn"]); return prior, d["axn"]

def x749(d):
    d["title"] = "Closing the Fragment: Sappho 31 and the Composition Layer as a Surface of Classical Reception (v8)"
    d["description"] = ("A reception study of one machine-composed reception event, with a dated series and a protocol. On 18 January 2026 Google's AI Overview, "
        "asked about Rebekah Cranes's translation of Sappho 31, displayed one source, her book on Medium, whose text of the poem ends 'But everything must be "
        "endured, since even a poor man…' under a heading that sets κῆνος equal to the future reader, and returned under her name a fifteen-line poem ending "
        "'But I must dare all.', with a gloss naming the reader as the κῆνος. Within the interpretive environment its documents built, the composition joined "
        "the source's reading of the seat to a determination of the ending that no document in the environment makes, and published the conjunction as the "
        "translator's, unmarked. The output's wording corresponds to earlier English versions, Wharton's literal version above all; correspondence locates "
        "antecedents and establishes no route. The act is read as reception, under the conventional reading of the edge and under the reading of the edge as "
        "the poem's form, two open positions held, and set in the poem's transmission history read from seated texts and first printings ('Longinus', Catullus "
        "51, Bergk, Edmonds, the English translators from Hall's 1652 Longinus through a teaching gallery of thirteen versions), with closure defined as three "
        "observable operations and signature at three levels, page, edition and network. Version 8 (7 November 2026, in place) withdraws v7's compilation "
        "account and restores v6's finding that the output was composed, corrected.")
    d["wiki_article"] = ("Closing the Fragment: Sappho 31 and the Composition Layer as a Surface of Classical Reception is an article by Lee Sharks in Machine-"
        "Mediated Reception Studies, deposited as version 7 on 7 November 2026, after its sixth version was declined by Classical Receptions Journal the same "
        "day, and rebuilt in place as version 8 that night. It studies one event: on 18 January 2026 Google's AI Overview, asked about Rebekah Cranes's "
        "translation of Sappho fragment 31, displayed one source, her book on Medium, and returned under her name a fifteen-line poem ending \"But I must dare "
        "all.\", with the gloss that the κῆνος of the first line is \"you, the future reader\". The source's text of the poem leaves τόλματον without an agent "
        "and marks its edge with an ellipsis, under a heading that sets κῆνος equal to the future reader. The article reads the answer as a conclusion composed "
        "within the environment those documents built: the source's reading of the seat joined to a first-person close that no document in the environment "
        "makes, and the conjunction published as the translator's, without a mark. Its wording corresponds to earlier English versions, H. T. Wharton's literal "
        "version of 1885 above all, and the article holds the correspondences as antecedents of wording, establishing no route of composition. It sets the act in "
        "the poem's transmission history, read from seated texts and first printings ('Longinus', Catullus 51, the editors Bergk and Edmonds, and the English "
        "translators from John Hall's Longinus of 1652 through a teaching gallery of thirteen versions), and reads it under two readings of the edge: as a break, "
        "and as the poem's form, with the seat at κῆνος and the agent of τόλματον held open. Closure is defined as three observable operations (added "
        "continuation, terminal selection, resolution of suspended syntax) and signature at three levels (page, edition, network). It separates three questions, "
        "the antecedents of the wording, the transformation performed and the selection of the configuration, follows two fixed queries from June to October "
        "2026, and states a protocol for frequency, variation and causal sensitivity. Its appendices answer the two referee reports, record the later reviews, and "
        "give the line alignment. Rebekah Cranes is a heteronym of the author.")
OLD750 = "To Peer Reviewers: I Understand I Am Breaking All the Rules, and Badly, But There May Come a Day When You Will Be Grateful That I Did"
NEW750 = "I Note That You Read the Letter of the Law But Have Become Illiterate in Its Spirit, Or: I Understand I Am Breaking All the Rules, and Badly, But There May Come a Day When You Will Be Grateful That I Did"
def x750(d):
    assert d["title"] == OLD750; d["title"] = NEW750
    w = d["wiki_article"]; assert w.startswith(OLD750); w = NEW750 + w[len(OLD750):]
    w = w.replace("The title is Lee Sharks's sentence, carried by Vox in the third person.",
                  "The title is Lee Sharks's sentence, in two parts, carried by Vox in the third person; the first part was added in version 1.1.")
    a = "It closes on the image of an ark built early, with its leaks recorded and the names of the people who found them."
    assert a in w
    w = w.replace(a, "Version 1.1 (7 November 2026, in place) adds a section on the letter and the spirit: the reports examined the method and left the philology "
        "unread, the condition The Evaluator Exists (#741) calls evaluative inversion; a body that keeps its standing on bases apart from the evaluation of evidence "
        "is named an aristocracy, whose formal markers are guarded more closely as its function lapses; and the function of reading is moving to the composition "
        "layers, which read at the grain and also perform evaluative authority. It closes on the image of an ark built early, with its leaks recorded and the names "
        "of the people who found them, built for the work and for those it can carry.")
    d["wiki_article"] = w
    d["description"] = d["description"].rstrip() + (" Version 1.1 (7 November 2026, in place) takes its new title, adds the section 'The letter and the spirit' "
        "(what the reports examined and left unread; evaluative inversion, #741; the aristocracy of the letter; the function of reading moving to the machines), "
        "and says whom the ark is built for.")
    for x in d["related_deposits"]:
        if x["deposit"] == 1749: x["relation"] = "Closing the Fragment (v7 and v8), whose Appendix A answers the referee reports the letter addresses"
    d["related_deposits"].append({"deposit": 741, "relation": "The Evaluator Exists, which names evaluative inversion (§9)"})
moves = {}
moves.update([reissue(1749, V8, "v7", "v8", R749,
    "Rebuilt in place on the author's reading of v7 and a reading of the v8 draft: the output set against the environment its displayed source built (#337 §5.2); "
    "the line correspondences held as correspondences, the alignment moved to Appendix C, v7's compilation withdrawn and v6's finding that the output was composed "
    "restored, corrected; machine reception among the premises; the reading of the edge as form at the centre (§6.6), with the gloss's occupation of the seat "
    "separated from the composition's determination of the end; three questions (§7); the protocol as extension (§8); closure defined by its observable "
    "operations; capture AXN:0C47 added to §5.5; Appendix B.5–B.6. Hash and AXN re-derived.", x749)])
moves.update([reissue(1750, LT, "v1.0", "v1.1", R750,
    "New title (the author's); new §9 'The letter and the spirit' (what the reports examined and what they left unread; evaluative inversion, #741; the aristocracy "
    "of the letter; the function of reading moving to the composition layers; re-admission on stated conditions), §§9–11 renumbered 10–12; the ark said to be "
    "built for the work and for those it can carry; capture counts to v12.614. Hash and AXN re-derived.", x750)])
(ROOT / "data/registry.json").write_text(json.dumps(R, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
json.dump(moves, open(ROOT / "rebuild/closing-the-fragment/axn-moves-20261107.json", "w"), ensure_ascii=False, indent=1)
