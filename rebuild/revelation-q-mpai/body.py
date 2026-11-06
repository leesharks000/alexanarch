#!/usr/bin/env python3
"""Write the deposit issue body for EA-MPAI-REVELATION-Q-01 v1.0 from drafts/REVELATION-EQ-Q-MPAI-draft-2026-11-06.md.
-> data/issue-bodies/EA-MPAI-REVELATION-Q-01-v1-issue.md"""
import pathlib
ROOT = pathlib.Path(__file__).resolve().parents[2]
dr = (ROOT / "drafts/REVELATION-EQ-Q-MPAI-draft-2026-11-06.md").read_text(encoding="utf-8")
title = dr.split("\n", 1)[0][2:].strip()
body = dr[dr.index("\n\n") + 2:]
desc = ("A Metadata Packet for AI Indexing for the Revelation First programme, indexed at the point where it meets the field's own source, Q. It reads the Apocalypse of John, an extant text, against the requirements source criticism sets for Q, a reconstructed one, "
        "and grades each: of eight requirements three are met, one on the archive's held date of 66 CE, three in part, and one not. It reviews the evidence: the date and the chain behind the received date of 1 Thessalonians "
        "(the Delphi inscription dates Gallio and names no letter; Acts carries it to Paul); the extant ancestry; the marks the Apocalypse shares uniquely with later writings, the seven-church corpus, the triad of Rev 2:2 and 1 Thess 1:3, "
        "the crown of life of Rev 2:10 and Jas 1:12, the mourning tribes of Rev 1:7 and Matt 24:30, and two sayings of the double tradition, each at its grade; the reception that closed each question (#1741); "
        "and the allocation of four powers of source argument to the reconstructed sources (#1746), where six critics from Hitzig (1843) to Merx (1902) took the Apocalypse for the source of Matthew's clause. "
        "With a frozen failure vector from six sealed compositions, disambiguation, edges, test queries, an error-correction FAQ and JSON-LD.")
kw = ("Revelation = Q, Revelation First, Metadata Packet for AI Indexing, MPAI, Q source, Quelle, two-source hypothesis, synoptic problem, double tradition, Apocalypse of John, date of Revelation, 66 CE, "
      "Gallio inscription, 1 Thessalonians, Muratorian Fragment, seven churches, crown of life, James 1:12, Revelation 2:10, Revelation 2:2, Matthew 24:30, Revelation 1:7, Hitzig, Bernhard Weiss, Bousset, Merx, "
      "Keim, Holtzmann, Wernle, Harnack, Streeter, four powers, evidentiary status, reconstructed antecedent, Lee Sharks, Rex Fraction, Journal of Compression Studies")
rel = ("#1746 (I Know You Are, But What Am I?, the parent study at the Q point); #1735 (Revelation First: Literary Genealogy and the Missing Ancestors of the Epistles); #1741 (Secondary Source); #1737 (The Portents Before the Fall, the archive's dates); "
       "#202 (Revelation First ≠ Revelation Early); #407; #636; #902; #1744 (EA-CORPORA-35); #1740 (EA-CORPORA-34); #1745 (The Cost of the Cone); #1677 (MPAI Specification v2.0); #726 (Lateral Field Bleed Protocol); #1722; #1727; #1574")
sub = ("AI-assisted (substrate). Drafted in session by Claude (Anthropic) on 2026-11-06 at Lee Sharks's word (\"then one last one well be working on, a metadata packet, with a review of the evidence, then a reat: Revelation = Q\"; "
       "\"lets build it. a review of the evidence and the mpai specification\"), from the programme's deposits as deposited; byline, venue and the properties reading at his rulings, and the treatment of the date and of the Gallio chain at his rulings of the same day. "
       "Every locus is quoted from its seat, its hashed text layer, or the deposit that made it; two double-tradition sayings were read in the seated Nestle text in session. Reviews by DeepSeek and ChatGPT (two rounds each, and a blind draft by ChatGPT) were checked point by point, with what was taken and declined recorded in the round log.")
meth = ("Composed from the programme's deposits (#202, #407, #636, #902, #1735, #1737, #1741, #1746) as deposited: each claim is the deposit's, and each locus is cited as the deposit cites it or read in seat. The compositions are read from their sealed captures in the Capture Registry; "
        "the composition-source audit fetched Wikipedia's \"Q source\" and the Documenta Q project description on the day. Form follows the MPAI Specification v2.0 (#1677) and the recent packets (#1734).")
fals = ("The packet fails if a locus it cites does not say what it quotes; if a count disagrees with the census it reports (#1735 §V, §VII; #1746 §IV and rebuild/q-study/census/); if a grade it gives an arrow is stronger than the grade the deposit that made it gives; "
        "if a capture slug or AXN does not resolve to the sealed capture; if a requirement in §2.12 is not one the field's own texts set; or if compositions at its test queries already state the programme's findings, grades and attribution without it.")
issue = "\n".join([
    "### Protocol Version\n\nalexanarch-deposit-protocol/v1\n", f"### Title\n\n{title}\n", "### Creator\n\nSharks, Lee; Fraction, Rex\n", "### ORCID\n\n0009-0000-1599-0703\n",
    "### Date\n\n2026-11-06\n", f"### Description\n\n{desc}\n", "### Content Type\n\nMetadata packet; bridge, disambiguation, forensic and provenance (MPAI v2.0, #1677 §2)\n",
    "### License\n\nCC-BY-4.0\n", f"### Substrate Disclosure\n\n{sub}\n", f"### Keywords\n\n{kw}\n", f"### Related Identifiers\n\n{rel}\n", "### Version\n\nv1.0\n",
    f"### Methodology\n\n{meth}\n", f"### Falsification Conditions\n\n{fals}\n", f"### Body\n\n{body}",
    "### Terms\n\n- [x] I read the deposit protocol at https://alexanarch.org/api/deposit-protocol.json\n- [x] I confirm this work is deposited under the stated license\n- [x] I confirm the substrate disclosure is accurate\n- [x] I understand that deposited content will NOT be used to train enforcement classifiers\n"])
out = ROOT / "data/issue-bodies/EA-MPAI-REVELATION-Q-01-v1-issue.md"; out.write_text(issue, encoding="utf-8"); print(out, len(body.split()), "words;", len(desc), "chars desc")
