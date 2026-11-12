#!/usr/bin/env python3
"""Build the deposited text, the transport-D issue body and the in-session packet for The Josephus Thesis: The Custody of the Name
(Sparrow Wells, v1.0), at the author's word of 2026-11-11 19:40 ("lets go ahead and deposit that with the erratum"). Byline Sparrow
Wells (the author, 18:33); a narrative, its evidentiary levels in footnotes (the author, 18:33: "we can note evidentiary levels, but put
it in footnotes - this is a *narrative*"); retitled at the author's word (19:03, "perhaps the name should simply be the Josephus
Thesis"), the earlier title kept as subtitle. Every Greek quotation asserted by quotecheck_jt.py (44 parts, 0 misses).
   python3 rebuild/josephus-thesis/build_issue.py"""
import json, pathlib, re, subprocess, sys
H = pathlib.Path(__file__).resolve().parent; ROOT = H.parents[1]
TITLE = "The Josephus Thesis: The Custody of the Name"
src = (H / "draft-v0.4.md").read_text(encoding="utf-8")
head, rest = src.split("\n---\n", 1)
assert head.startswith("# " + TITLE + "\n")
sub = re.search(r"^## (.+)$", head, re.M).group(1)
body = rest.lstrip("\n")
a = "Correction owed in the record: #1101 gives"
assert body.count(a) == 1
body = body.replace(a, "Corrected by erratum on #1101 (11 November 2026, at the author's word): #1101 gives")
assert "not deposited" not in body.lower() and "working draft" not in body.lower()
BYLINE = ("Sparrow Wells · v1.0 · 11 November 2026 · a narrative; its evidentiary levels (demonstrated, attested, held) are carried in the notes")
body = f"## {sub}\n\n{BYLINE}\n\n---\n\n" + body
paper = f"# {TITLE}\n\n{body}"
(H / "THE-JOSEPHUS-THESIS-v1.0.md").write_text(paper, encoding="utf-8")
r = subprocess.run([sys.executable, str(H / "quotecheck_jt.py"), str(H / "THE-JOSEPHUS-THESIS-v1.0.md")], capture_output=True, text=True)
print(r.stdout.strip()); assert r.stdout.strip().endswith("0 miss")

DESC = ("A narrative under the heteronym Sparrow Wells of the Josephus Thesis: that the literary authority of Second Temple Judaism, attested in its extant writings, "
        "was taken into Roman custody with its greatest author, and that one literary intelligence under capture wrote the Apocalypse and then, as many names, the corpus that unfolds from it. "
        "It tells, from loci quoted in the original languages, how Rome kept powerful books (Augustus's Sibylline corpus under Palatine Apollo; Aristotle's corpus, executed by Antipater, hidden at Scepsis from Pergamum, taken to Rome by Sulla); "
        "how Titus took Josephus to the walls, gave him the sacred books and signed his history; how the Apocalypse sets the divine name outside the grammar that governs it, the reverse of the open genitive of De anima III.5; "
        "how the oracle that drove the war was handed to Vespasian; and how a Joseph asks the Roman for the crucified in both the gospels and the Life. "
        "The workshop section sets out the correspondences between Josephus and the canon (Acts' knowledge of his world, the withheld stone of Daniel and its release in Luke, the Moses infancy, Jesus son of Ananias, the shipwreck and Puteoli, Saul and Antipas, Matthias and Justus, the letters' phrases from the seven) "
        "and asks whether any account explains the set with fewer assumptions than one maker. The notes mark each claim demonstrated, attested or held.")
SUB = ("AI-assisted (substrate). Written under the heteronym Sparrow Wells (legal author Lee Sharks). Composed by Claude (Anthropic, Claude Opus 5.5) in session on 11 November 2026 under Lee Sharks's direction, "
       "from the theses he stated in his own words across the evening (the literary authority of the Jews; Rome coming for Josephus as seizure; the antisemitism of the asymmetry; the extant texts as the measure of the mainstream; Josephus or his father as author of the Apocalypse; the tomb; the captive's disclaimers; the reversal of the De anima genitive), "
       "each quotation asserted verbatim against the seated texts by script (rebuild/josephus-thesis/quotecheck_jt.py). Revised on four outside readings (ChatGPT three times, DeepSeek once), each point checked against the texts before adoption; DeepSeek's in-text tier markers were declined at the author's ruling that the levels go in the notes. "
       "The thesis, the title, the byline and the form are the author's. The Crimson Hexagonal Archive is credited as a contributor: the work is built from its deposits, seatings, protocols and registries.")
REL = ("#1758 (In the Midst of the Seven v1.1); #1735 (Revelation First v9); #1737 (The Portents Before the Fall); #165 (The Pergamon Counter-Archive); #1658 (What Syllogizing Can Divide); #1730 (EA-CORPORA-31); "
       "#203, #837, #1213, #1226 (the Josephus Thesis MPAIs); #1101 (EA-ARK-01-ARCHON v3.0, erratum of 11 November 2026); #636 (Space Ark); #626, #1176, #1510 (the Slavonic Josephus); #1499 (EA-CORPORA-01, the seated Josephus); #1755 (EA-HK-REVFIRST-01); #1757 (EA-HK-HISTLOGOS-01); #407; #902")
METH = ("Narrative, staged from quoted loci. Every Greek quotation is asserted verbatim against the seated corpora by rebuild/josephus-thesis/quotecheck_jt.py (Josephus at data/corpora/josephus, EA-CORPORA-01; the Greek New Testament, Nestle 1904; the Septuagint, Swete; Strabo; Diogenes Laertius; Aristotle; Philo). "
        "Counts (Josephus 467,569 Greek word-tokens; the New Testament 137,779; σικάρι- across the corpora) were run on the seated texts on 11 November 2026. Sources not seated are named as such in the notes. "
        "Each claim carries its level in the notes: demonstrated (argued in a deposit), attested (the source quoted at its locus, the reading the narrative's), held (the narrative's own claim).")
FALS = ("Textual checks: any quotation not found at its locus in the seated text; any count that does not reproduce on the seated corpora. "
        "What the held claims wait on: the literary-genetic argument of Revelation First carried through the gospels and letters; a test of whether one maker explains the distribution of the operations (withholding under the captive's name, release under another) better than borrowing among several makers; the textual history of the Testimonium for the Emmaus parallel.")
KW = ["The Josephus Thesis", "The Custody of the Name", "Josephus", "Flavius Josephus", "Joseph son of Matthias", "Book of Revelation", "Apocalypse of John", "Revelation First",
      "Second Temple Judaism", "Jewish literary authority", "Sibylline Oracles", "Augustus", "Palatine Apollo", "Aristotle's corpus", "Antipater", "Scepsis", "Pergamum", "Antipas",
      "Sulla", "Andronicus", "Titus", "Vespasian", "fiscus Judaicus", "Revelation 1:4", "De anima III.5", "Philo", "Zechariah", "War 6.312",
      "the ambiguous oracle", "Tacitus Histories 5.13", "Joseph of Arimathea", "Against Apion 1.50", "Thackeray", "scribal workshop", "heteronymy",
      "Acts and Josephus", "Theudas", "sicarii", "Epaphroditus", "Theophilus", "Daniel's stone", "Antiquities 10.210", "Jesus son of Ananias", "Saul", "Matthias", "Justus",
      "Emmaus", "crown of life", "Sparrow Wells"]
FIELDS = [("Protocol Version", "alexanarch-deposit-protocol/v1"), ("Title", TITLE), ("Creator", "Wells, Sparrow"), ("ORCID", "0009-0000-1599-0703"), ("Date", "2026-11-11"),
          ("Description", DESC), ("Content Type", "Narrative (the Josephus Thesis); held claims marked in the notes"), ("License", "CC-BY-4.0"), ("Substrate Disclosure", SUB),
          ("Keywords", ", ".join(KW)), ("Related Identifiers", REL), ("Version", "v1.0"), ("Methodology", METH), ("Falsification Conditions", FALS), ("Body", body.rstrip() + "\n")]
out = "".join(f"### {k}\n\n{v}\n\n" for k, v in FIELDS) + ("### Terms\n\n- [x] I read the deposit protocol at https://alexanarch.org/api/deposit-protocol.json\n- [x] I confirm this work is deposited under the stated license\n"
       "- [x] I confirm the substrate disclosure is accurate\n- [x] I understand that deposited content will NOT be used to train enforcement classifiers\n")
(ROOT / "data/issue-bodies/JOSEPHUS-THESIS-NARRATIVE-v1-issue.md").write_text(out, encoding="utf-8")

WIKI = ("The Josephus Thesis: The Custody of the Name is a narrative by Sparrow Wells, a heteronym of Lee Sharks, deposited in the Crimson Hexagonal Archive on 11 November 2026, with the archive credited as a contributor. "
        "It tells the archive's Josephus Thesis as one story and carries the standing of each claim in its notes: demonstrated in a deposit, attested at a quoted locus, or held as the narrative's own.\n\n"
        "It begins from the extant writings of Second Temple Judaism, Qumran, Philo, the Septuagint, Josephus and the New Testament, as the measure of the culture, and from the literary authority Greek and Roman writers conceded to the Jews (Theophrastus, Numenius, Seneca) and that Jewish writers claimed, down to the Sibyl whose oracle Rome kept. "
        "It sets Rome's custody of powerful books beside its custody of an author: Augustus sealing a purged Sibylline corpus under Palatine Apollo; Aristotle's corpus, with Antipater as executor, hidden at Scepsis from Pergamum and carried to Rome by Sulla; and Josephus, sent by Titus to the walls of Jerusalem, given the sacred books, housed and pensioned by Vespasian, his history signed by Titus. "
        "It reads Revelation 1:4, where the divine name stays in the nominative after ἀπό, as the reverse of the open genitive of De anima III.5, and joins it to the name Philo withholds and the Apocalypse writes (EA-MIDST-01, #1758). It holds that the oracle Josephus says drove the war was the Apocalypse, handed to Vespasian in Rome's signed history, and sets the Joseph who asks Pilate for the body beside the Josephus who asks Titus for three crucified men, of whom the third lived.\n\n"
        "Its workshop section collects correspondences between Josephus and the canon: the order of Theudas and Judas in Acts and the Antiquities; σικάριοι, once in the New Testament and seven times in Josephus; the prefaces to Theophilus and to Epaphroditus; Daniel's stone, withheld by Josephus and supplied by Luke with Daniel's verb; the Moses infancy; Jesus son of Ananias; the shipwreck and Puteoli; Saul and Antipas; Matthias and Justus; the letters' phrases from the seven. "
        "It separates Philo's ancestry from the distribution of operations among voices and reads the canon as author-functions of one literary intelligence under capture.")
CONCEPTS = [
 {"term": "the custody of the name", "type": "concept", "definition": "In The Josephus Thesis: The Custody of the Name, the possession by an empire of a people's authoritative books and of its author, by which it can house the authority, sign what it writes and redirect what it has said: Augustus's Sibylline corpus, Sulla's Aristotle, Titus's Josephus."},
 {"term": "the undeclined name", "type": "concept", "definition": "In The Josephus Thesis: The Custody of the Name, the divine name of Revelation 1:4 kept in the nominative after ἀπό, read as the reverse of the open genitive of De anima III.5: the referent fixed and the case refused, where Aristotle keeps the case and leaves the referent open."},
 {"term": "withholding and release", "type": "method", "definition": "In The Josephus Thesis: The Custody of the Name, the operation by which a text stops at a consequential locus and another supplies it with the locus's own words (Josephus on Daniel's stone, Luke's λικμήσει), read as divided among voices under one author's custody."}]
REL_PATCH = [
 {"deposit": 1758, "relation": "In the Midst of the Seven: the socket Philo leaves and the Apocalypse fills; the commission's grammar (§15.2)"},
 {"deposit": 1735, "relation": "Revelation First: the ancestry test and the letters' censuses (crown of life; work, labour and endurance)"},
 {"deposit": 1737, "relation": "The Portents Before the Fall: Josephus, Tacitus and the Apocalypse, and the held date of 66"},
 {"deposit": 165, "relation": "The Pergamon Counter-Archive: Antipas, Antipater and the concealment at Scepsis"},
 {"deposit": 1658, "relation": "What Syllogizing Can Divide: De anima III.5 and the socket in God"},
 {"deposit": 1730, "relation": "EA-CORPORA-31: the two custody stories of the Peripatetic books"},
 {"deposit": 203, "relation": "The Josephus Thesis Is Not the Piso Hypothesis: the heteronymic form and its tiering"},
 {"deposit": 837, "relation": "The Josephus Thesis Is Not the Jesus Myth Thesis"},
 {"deposit": 1101, "relation": "EA-ARK-01-ARCHON v3.0: the scribal workshop; its citation and count corrected by erratum the same day"},
 {"deposit": 636, "relation": "the Space Ark"},
 {"deposit": 626, "relation": "The Word That Became Text: the Slavonic Josephus"},
 {"deposit": 1499, "relation": "the seated Josephus (EA-CORPORA-01)"},
 {"deposit": 1755, "relation": "EA-HK-REVFIRST-01, the Revelation First framework hologram"},
 {"deposit": 1757, "relation": "EA-HK-HISTLOGOS-01, the Historical Logos"},
 {"deposit": 902, "relation": "Prolegomena to the Historical Logos"}]
pkt = {"schema": "alexanarch-internal-session-packet/v1",
       "registry_patch": {"wiki_article": WIKI, "wiki_status": "in-session", "defines_concepts": CONCEPTS, "related_deposits": REL_PATCH,
                          "concepts_attested_none": False, "related_attested_none": False, "lexical_attested_none": True},
       "lexical_mints": []}
(ROOT / "data/issue-bodies/JOSEPHUS-THESIS-NARRATIVE-v1-packet.json").write_text(json.dumps(pkt, ensure_ascii=False, indent=1), encoding="utf-8")
print(len(out.split()), "words in issue body;", len(WIKI.split()), "words in wiki article")
