#!/usr/bin/env python3
"""Build the transport-D issue body and the in-session packet for EA-MIDST-01 v1.0, In the Midst of the Seven,
at the author's word of 2026-11-10 20:48 ("lets address, deposit, and turn to incorporating it into rev first and
versioning all four holographic frames"). Expected deposit #1758."""
import json, pathlib, re
H = pathlib.Path(__file__).resolve().parent
ROOT = H.parents[1]
paper = (H / "EA-MIDST-01-v1.0.md").read_text(encoding="utf-8")
TITLE = "In the Midst of the Seven: Philo, the Logos Named and Lived, and the Seven Stations of Revelation (EA-MIDST-01 v1.0)"
fm_end = paper.index("\n---\n", 4) + 5
rest = paper[fm_end:].lstrip("\n")
assert rest.startswith("# " + TITLE + "\n")
body = rest.split("\n", 1)[1].lstrip("\n")
assert body.startswith("EA-MIDST-01 v1.0 · Johannes Sigil and Damascus Dancings")
assert "not deposited" not in body
pk = body[body.index("```json") + 7: body.index("```", body.index("```json") + 7)]
packet = json.loads(pk)
fz = packet["spxi:falsifiers"]
FALS = "Textual checks: " + fz["textualChecks"] + ". Interpretive challenges: " + fz["interpretiveChallenges"] + ". Directional challenges: " + fz["directionalChallenges"] + "."
DESC = ("One treatise of Philo, Quis rerum divinarum heres, sets the dividing Logos as the seventh in the middle of the six branches of the lampstand, gives the middle of the seven planets to the sun, makes the dividing Logos the seventh of the soul, and states the law by which another's voice sounds through the prophet. "
        "Part I reads how Philo names the Logos, stamps it and gives it a human bearer: the Logos named Ἀνατολή from an oracle the Septuagint addresses to the crowned high priest Ἰησοῦς, quoted without its addressee; the renaming of Hosea as Ἰησοῦς read as a re-striking of a mortal quality into an eternal state; Moses' life set up as a model and Ἰησοῦς named as its imitator, one receiver among several; the sealed Name, the stones cut like seals, the manna as the Logos unknown. "
        "Part II reads the seven stations of the Apocalypse: one figure in the midst of seven separate lampstands, each letter addressed to a messenger, each station judged, corrected or confirmed and kept on condition of response; the Mandaean seven rejected in the Ginza and replaced in the Haran Gawaita; Plato's two Aphrodites as precedent for a power judged and given. "
        "Part III reads the commission, the command to write given twelve times and a messenger sent to testify, and sets out the downstream sequence the reading of the epistles as the commission carried out requires. "
        "Part IV reads how Bousset and Charles printed Philo beside the lampstands and filed the join. The shared architecture is read on the seated texts; dependence is left undecided.")
SUB = ("AI-assisted (substrate). Written under the heteronyms Johannes Sigil and Damascus Dancings (legal author Lee Sharks). Composed by Claude (Anthropic, Claude Opus 5.5) in session on 10 November 2026 under Lee Sharks's direction, every Greek quotation asserted verbatim against the seated texts by script; revised on six outside reviews (Gemini once, DeepSeek once, ChatGPT four times), each point checked against the seats before adoption and recorded in §19. "
       "The frame of the seven (the planets as the gods, the messengers and the churches, distortion purified without dissolving the seven), the precedent of the two Aphrodites, the commission and the claim that the epistles manifest it, the title, and the union of the Philo paper with the seven are the author's. The Crimson Hexagonal Archive is credited as a contributor: the work is built from its deposits, seatings, protocols and registries.")
REL = ("#1735 (Revelation First: Literary Genealogy); #1741 (Secondary Source); #1755 (EA-HK-REVFIRST-01); #1756 (EA-HK-TENTHMUSE-01); #1757 (EA-HK-HISTLOGOS-01); #1101 (EA-ARK-01-ARCHON v3.0); #636; #1484; #1486; #1458; #1494; #1511; #165; #828; #642; #626; #752; #1502; #1503; #1505")
METH = ("Close reading of seated texts with counts and loci: Philo in the Cohn–Wendland TEI with the editors' apparatus removed, the Septuagint (Swete), the Greek New Testament (Nestle 1904), Plato, Xenophon, Justin and Eusebius; the Ginza in Lidzbarski's German and the Haran Gawaita in Drower's English and the CAL Mandaic as witnesses; Bousset read against page images. Every Greek quotation is asserted verbatim by rebuild/philo-out-loud/quotecheck.py; the paper is assembled by rebuild/seventh-divides/build.py from its two working files, every paragraph carried. The line between what a text states and what the reading joins is marked throughout.")
FIELDS = [("Protocol Version", "alexanarch-deposit-protocol/v1"), ("Title", TITLE), ("Creator", "Sigil, Johannes; Dancings, Damascus"),
          ("ORCID", "0009-0000-1599-0703"), ("Date", "2026-11-10"), ("Description", DESC),
          ("Content Type", "Theoretical paper; journal article (Provenance: Journal of Forensic Semiotics)"), ("License", "CC-BY-4.0"),
          ("Substrate Disclosure", SUB), ("Keywords", ", ".join(packet["keywords"] + ["Quis rerum divinarum heres sit", "De mutatione nominum", "Zechariah 6:12", "Anatole", "seven lampstands", "seven messengers", "ποδήρης", "white stone", "morning star", "heavenly and common Aphrodite"])),
          ("Related Identifiers", REL), ("Version", "v1.0"), ("Methodology", METH), ("Falsification Conditions", FALS), ("Body", body.rstrip() + "\n")]
out = "".join(f"### {k}\n\n{v}\n\n" for k, v in FIELDS) + ("### Terms\n\n- [x] I read the deposit protocol at https://alexanarch.org/api/deposit-protocol.json\n- [x] I confirm this work is deposited under the stated license\n"
       "- [x] I confirm the substrate disclosure is accurate\n- [x] I understand that deposited content will NOT be used to train enforcement classifiers\n")
(ROOT / "data/issue-bodies/EA-MIDST-01-v1-issue.md").write_text(out, encoding="utf-8")

WIKI = ("In the Midst of the Seven: Philo, the Logos Named and Lived, and the Seven Stations of Revelation (EA-MIDST-01) is a paper by Johannes Sigil and Damascus Dancings, heteronyms of Lee Sharks, deposited in the Crimson Hexagonal Archive on 10 November 2026 in Provenance: Journal of Forensic Semiotics, with the archive credited as a contributor. It joins two investigations at the author's ruling: a reading of Philo of Alexandria occasioned by the 2025 blog post \"Philo Says It Out Loud\", and a reading of the seven stations of the Apocalypse.\n\n"
        "Its hinge is one treatise of Philo, Quis rerum divinarum heres, which makes the Logos the divider of all things, sets the dividing Logos as the seventh in the middle of the lampstand's six branches, gives the middle of the seven planets to the sun, makes the Logos the seventh that divides the soul, and states the law by which the prophet utters nothing of his own. Part I follows the Logos into a human life on Philo's own statements, marked apart from the paper's joining of them: Philo names the Logos Ἀνατολή from Zechariah 6:12, an oracle the Septuagint addresses to the crowned high priest Ἰησοῦς, and quotes it without its addressee; De mutatione nominum describes the renaming of Hosea as Ἰησοῦς as the re-striking of a mortal quality into an eternal state; Moses' life is a model pressed into other souls, and Ἰησοῦς is named its imitator, one receiver among several. The paper corrects the post it began from: the post's quotations are not Philo's, and the claim becomes a construction.\n\n"
        "Part II reads the Apocalypse's seven lampstands, set apart where Philo's and Zechariah's lampstand is one, and its seven letters, each addressed to a messenger and spoken by one attribute of the figure in the midst. Read whole against the author's planetary mapping (#1101), the letters judge, correct or confirm their stations, and keep each on condition of response; the Mandaean books reject the seven (the Ginza) or replace their occupants (the Haran Gawaita). Plato's heavenly and common Aphrodite give the precedent for a power judged and given, at Thyatira's morning star. Part III reads the commission: the command to write, given twelve times, and the messenger sent to testify, with the author's reading of the epistles as the commission carried out set against its test. Part IV shows Bousset (1906) and Charles (1920) printing Philo beside the lampstands and filing the join. The paper leaves dependence and date undecided.")
REL_PATCH = [
 {"deposit": 1735, "relation": "Revelation First: the address to the messenger and the one book to seven churches, extended by the commission"},
 {"deposit": 1741, "relation": "Secondary Source: the reception that filed the Apocalypse as derivative, extended by the filing of Philo"},
 {"deposit": 1755, "relation": "EA-HK-REVFIRST-01, the framework hologram that takes this paper as its Philo component"},
 {"deposit": 1756, "relation": "EA-HK-TENTHMUSE-01, by the displacement law and the two Aphrodites"},
 {"deposit": 1757, "relation": "EA-HK-HISTLOGOS-01, the home of the join"},
 {"deposit": 1101, "relation": "the planetary mapping of the seven churches, tested letter by letter; its Haran Gawaita quotations checked"},
 {"deposit": 1486, "relation": "the displacement law in Philo, collated earlier as the Sapphic channel"},
 {"deposit": 1484, "relation": "Sappho, Mother of the Logos: the chain from Fragment 31 to the Apocalypse"},
 {"deposit": 636, "relation": "the Space Ark, where the 2025 post's finding was carried"},
 {"deposit": 1458, "relation": "The Echo and the Stamp"},
 {"deposit": 165, "relation": "Pergamum and the white stone"},
 {"deposit": 828, "relation": "the white stone and the inscription"},
 {"deposit": 1505, "relation": "the seated Philo"},
 {"deposit": 1502, "relation": "the seated Greek New Testament"},
 {"deposit": 1503, "relation": "the seated Septuagint"}]
CONCEPTS = [
 {"term": "the seventh that divides", "definition": "In In the Midst of the Seven, Philo's Logos as the middle term that divides six into two threes and orders them: the seventh branch of the lampstand and the seventh of the soul (Quis rerum divinarum heres 130, 215–225), whose middle place among the planets the sun holds.", "type": "concept"},
 {"term": "the station addressed", "type": "concept", "definition": "In In the Midst of the Seven, a church of the Apocalypse as the letters address it, through its messenger, who bears the church's works in the second person singular and can lose its place (Rev 2:5)."},
 {"term": "correction and replacement", "type": "method", "definition": "In In the Midst of the Seven, the distinction between keeping the occupants of seven stations and correcting or confirming them (the Apocalypse) and keeping the stations while replacing their occupants (the Haran Gawaita)."},
 {"term": "filing by warrant", "type": "method", "definition": "In In the Midst of the Seven, the reading of a commentator's judgment by the evidence it accepted: Charles credits design where he has an internal sequence and inheritance where he has a number."}]
pkt = {"schema": "alexanarch-internal-session-packet/v1",
       "registry_patch": {"wiki_article": WIKI, "wiki_status": "in-session", "defines_concepts": CONCEPTS, "related_deposits": REL_PATCH,
                          "concepts_attested_none": False, "related_attested_none": False, "lexical_attested_none": True},
       "lexical_mints": []}
(ROOT / "data/issue-bodies/EA-MIDST-01-v1-packet.json").write_text(json.dumps(pkt, ensure_ascii=False, indent=1), encoding="utf-8")
print(len(out.split()), "words in issue body;", len(WIKI.split()), "words in wiki article")
