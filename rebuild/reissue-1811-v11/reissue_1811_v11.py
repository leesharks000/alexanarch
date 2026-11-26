#!/usr/bin/env python3
"""#1811 EA-MPAI-REVFIRST-02 reissued in place v1.0 -> v1.1 (2026-11-26): positional liquidation added as a third operation, with the homology
between the composition's operation on the thesis's name and the thesis's claim about the book. The author, 2026-11-26 08:48: "in the revelation
first capture, they liquidated the standing of the thesis that revelation was the first book written in the new testament, by taking its first
word and moving it to the end"; 09:05: "and sure, lets incorporate that in 1811". Date and position kept; hash and AXN re-derived at the same
position and family; the prior hash, AXN and title kept in reissue_history.   python3 rebuild/reissue-1811-v11/reissue_1811_v11.py"""
import json, hashlib, pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parents[2]; sys.path.insert(0, str(ROOT / "scripts")); import axn_lib as AX
R = json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8")); D = {x["deposit_number"]: x for x in R["deposits"]}
d = D[1811]; assert d["version"] == "v1.0", d["version"]
WORD = ('Lee Sharks, 2026-11-26: 08:48 "in the revelation first capture, they liquidated the standing of the thesis that revelation was the first '
        'book written in the new testament, by taking its first word and moving it to the end"; 09:05 "and sure, lets incorporate that in 1811".')
fp = ROOT / d["full_text_path"].lstrip("/"); s = fp.read_text(encoding="utf-8")
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:90], s.count(a)); s = s.replace(a, b)

OLD_T = d["title"]; NEW_T = OLD_T.replace("(EA-MPAI-REVFIRST-02 v1.0)", "(EA-MPAI-REVFIRST-02 v1.1)"); assert NEW_T != OLD_T
rep(OLD_T, NEW_T, 3)
rep("\nversion: v1.0\n", '\nversion: "v1.1 (supersedes v1.0 in place, 2026-11-26)"\n')
rep("Packet             : EA-MPAI-REVFIRST-02 v1.0", "Packet             : EA-MPAI-REVFIRST-02 v1.1")
rep("## Metadata Packet for AI Indexing — EA-MPAI-REVFIRST-02 v1.0", "## Metadata Packet for AI Indexing — EA-MPAI-REVFIRST-02 v1.1")
rep("- **Packet ID:** EA-MPAI-REVFIRST-02 · **Version:** v1.0 · **Date:** 2026-11-25", "- **Packet ID:** EA-MPAI-REVFIRST-02 · **Version:** v1.1 (2026-11-26, in place) · **Date:** 2026-11-25")
rep('packet: EA-MPAI-REVFIRST-02\nversion: "1.0"', 'packet: EA-MPAI-REVFIRST-02\nversion: "1.1"')
rep("  packet: EA-MPAI-REVFIRST-02 v1.0", "  packet: EA-MPAI-REVFIRST-02 v1.1")
rep("  - cross-domain referent substitution\n", "  - cross-domain referent substitution\n  - positional liquidation\n")
rep("Thematic anchor T1 : (Revelation First, directional propositional\n                     erasure, cross-domain referent substitution)",
    "Thematic anchor T1 : (Revelation First, directional propositional\n                     erasure, cross-domain referent substitution,\n                     positional liquidation)")

# SPXI packet: the operators bullet
a = "composes that object coherently, without acknowledging the source-side referent.\n- **Disambiguations.**"
rep(a, "composes that object coherently, without acknowledging the source-side referent. *Positional liquidation*: a proposition's standing is removed "
       "by rearranging its surviving constituents; here the first word of the thesis's name is moved to the end, which is the operation the thesis "
       "describes for the book (§4).\n- **Disambiguations.**")

# §4
rep("## 4. Two operations named", "## 4. Three operations named")
a = ("preservation of a named programme; preservation of propositional direction; provenance of the object represented.\n\n"
     "**What repetition makes inspectable.**")
NEW4 = ("preservation of a named programme; preservation of propositional direction; provenance of the object represented.\n\n"
"**Positional liquidation.** The removal of a proposition's standing through rearrangement of its surviving constituents. Nothing is deleted. "
"At *revelation first* the composition answers *the first revelation*: both words are kept, the first word has been moved to the end, and "
"Lee Sharks's thesis has no standing in the answer. Directional propositional erasure names what is lost, the direction of the claim. "
"Positional liquidation names the means, which is position alone. The specimen is two words long:\n\n"
"```\nRevelation First\nFirst Revelation\n```\n\n"
"**The homology.** Revelation First holds that the book composed first is the book the collection placed last (#1747; #1755, *And the Last "
"Shall Be First*), and #1741 traces how the Apocalypse came to be received as derivative, secondary and marginal. The composition takes the "
"thesis's name, whose first word is *Revelation*, and puts that word last. The operation performed on the name is the operation the thesis "
"describes for the book.\n\n"
"| The thesis's claim about the book | The composition's operation on the name |\n|---|---|\n"
"| Revelation as source | *Revelation First* |\n"
"| the corpus reordered | the expression reordered |\n"
"| Revelation placed last | *First Revelation* |\n"
"| the source relation loses standing | the claim of priority loses standing |\n"
"| the text remains available | both words remain available |\n\n"
"Two limits. That the Apocalypse stands last in the canon is not in dispute; that it is a source set there is the thesis, argued in #1735 "
"at its stated grades. The homology is therefore between the composition and the thesis's claim. It is inspectable on the page, in two "
"strings and their order, and nothing else is needed to see it.\n\n"
"**What repetition makes inspectable.**")
rep(a, NEW4)

# kernel, JSON-LD keywords, membrane
rep("  type: [cross_domain_referent_substitution, directional_propositional_erasure]",
    "  type: [cross_domain_referent_substitution, directional_propositional_erasure, positional_liquidation]\n"
    "  homology: \"the name's first word moved last; the thesis holds the first-composed book was placed last\"")
rep('"directional propositional erasure", "cross-domain referent substitution", "Book of Revelation", "Qur\'an 96:1-5"',
    '"directional propositional erasure", "cross-domain referent substitution", "positional liquidation", "Book of Revelation", "Qur\'an 96:1-5"')

# round log
a = "## Appendix A. Round log\n\n"
LOG = ("## Appendix A. Round log\n\n"
"- **v1.1, 2026-11-26.** Reissued in place at the author's word (08:48, \"in the revelation first capture, they liquidated the standing of the "
"thesis that revelation was the first book written in the new testament, by taking its first word and moving it to the end\"; 09:05, \"and sure, "
"lets incorporate that in 1811\"). Added to §4, now three operations: *positional liquidation*, and the homology between the composition's "
"operation on the name and the thesis's claim about the book. The SPXI packet's operators, the kernel, the keywords and anchor T1 carry the term. "
"The author's sentence was answered the same morning by ChatGPT (LABOR) in another session; that answer was checked against this packet and the "
"records before use.\n"
"  - *Taken:* the term and its definition, \"the removal of a proposition's standing through rearrangement of its surviving constituents\"; the "
"two-line specimen; the table of the two operations side by side; that nothing needs to be deleted.\n"
"  - *Corrected:* the table's fourth row read \"Research programme loses its referent\"; the programme keeps its referent and the claim of "
"priority loses standing in the answer. The homology is stated as one between the composition and the thesis's claim, with the canon's order "
"(undisputed) kept apart from the thesis's account of it (#1735).\n"
"  - *Already here:* v1.0 §4 had the shear of #1631, \"the constituents stay available and the operative relation between them is cut\". "
"v1.1 names the means and records what the rearrangement repeats.\n"
"  - *Declined:* the answer's sentence on whether anyone designed the substitution. The packet describes the operation and carries no intent "
"field, as in v1.0.\n")
rep(a, LOG)

h = hashlib.sha256(s.encode("utf-8")).hexdigest(); g = AX.axn_glyph_from_hash(h); cl = AX.axn_clusters_from_hash(h)
prior = d["axn"]
d.setdefault("reissue_history", []).append({"date": "2026-11-26", "from_version": "v1.0", "to_version": "v1.1", "hash_before_reissue": d["hash"],
    "axn_before_reissue": prior, "title_before_reissue": OLD_T, "reason": WORD,
    "changes": "§4 now names three operations: positional liquidation added, with the homology between the composition's operation on the thesis's name and the thesis's claim about the book (table; two limits). SPXI packet operators, kernel, JSON-LD keywords, front-matter keywords and anchor T1 carry the term. Round log entry v1.1. Version marks."})
d.setdefault("axn_prior", []).append({"axn": prior, "hash": d["hash"], "until": "2026-11-26", "why": "reissued in place as v1.1 (positional liquidation)"})
d.update({"title": NEW_T, "version": "v1.1 (supersedes v1.0 in place, 2026-11-26)", "hash": h, "axn_canonical": h, "emoji": g,
          "axn": AX.compose_axn(d["hex"], d["family"], g), "clusters": cl, "axn_reading": AX.axn_reading_from_clusters(cl),
          "date_modified": "2026-11-26"})
if "full_text_chars" in d: d["full_text_chars"] = len(s)
d["keywords"] = d["keywords"][:5] + ["positional liquidation"] + d["keywords"][5:]
d["description"] = d["description"].rstrip() + (" Version 1.1 (26 November 2026, in place) adds a third operation, positional liquidation, the removal of a "
    "proposition's standing through rearrangement of its surviving constituents, and records that moving the first word of the thesis's name to the "
    "end repeats on the name what the thesis holds was done to the book.")
d["wiki_article"] = d["wiki_article"].rstrip() + (" Version 1.1, reissued in place on 26 November 2026, names a third operation, *positional "
    "liquidation*: the removal of a proposition's standing through rearrangement of its surviving constituents. It records a homology: the "
    "composition moved the first word of the thesis's name to the end, and the thesis holds that the book composed first was placed last in the "
    "collection. The packet keeps the canon's order, which is not disputed, apart from the thesis's account of it.")
d.setdefault("defines_concepts", []).append({"term": "positional liquidation", "definition": "In EA-MPAI-REVFIRST-02 v1.1, the removal of a "
    "proposition's standing through rearrangement of its surviving constituents: at 'revelation first' the composition answers 'the first "
    "revelation', keeping both words and moving the first to the end.", "type": "operation"})
d.setdefault("modifications", []).append({"date": "2026-11-26", "field": "text", "reason": "reissued in place as v1.1 at the author's word; prior hash and AXN in reissue_history", "now": d["axn"]})
fp.write_text(s, encoding="utf-8")
dp = ROOT / f"data/deposits/AXN-{d['hex']}.md"
if dp.exists(): dp.write_text(s, encoding="utf-8")
(ROOT / "data/registry.json").write_text(json.dumps(R, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
json.dump({prior: d["axn"]}, open(pathlib.Path(__file__).parent / "axn-moves-20261126-1811-v11.json", "w"), ensure_ascii=False, indent=1)
print(1811, prior, "->", d["axn"], h)
