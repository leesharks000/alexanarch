#!/usr/bin/env python3
"""Write the EA-CORPORA-44 deposit issue body and packet from the two seat records (the form of body43.py).
    python3 rebuild/corpora/ea-corpora-44/body44.py
-> data/issue-bodies/EA-CORPORA-44-issue.md, data/issue-bodies/EA-CORPORA-44-packet.json"""
import json, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[3]; A = ROOT / "data/corpora"
SEATS = [("benjamin", "Walter Benjamin in German: first printings, and the seven volumes cut to his text"),
         ("zeitschrift-fuer-sozialforschung", "The Institute's journal: nine volumes pinned, their essay lists, thirteen articles")]
DECLARED = [
    ("The articles of Max Horkheimer (died 1973), Theodor W. Adorno (1969), Herbert Marcuse (1979), Erich Fromm (1980), Friedrich Pollock (1970), Leo Löwenthal (1993), Karl August Wittfogel (1988), Otto Kirchheimer (1965) and the other contributors to the Zeitschrift still in copyright", "in copyright: not copied. The volumes that hold them are fixed by Internet Archive address, size and SHA-256 in seat 44/02, and each volume's essay list is seated so that who wrote what is readable without the volume"),
    ("The editors' reports and notes of the Gesammelte Schriften (Rolf Tiedemann, Hermann Schweppenhäuser, Hella Tiedemann-Bartels, Tillman Rexroth and others; Suhrkamp Verlag)", "in copyright: not copied. The seven volumes are fixed by address, size and SHA-256 in seat 44/01, with the offsets at which the editors' sections begin"),
    ("Eight pieces printed inside the volumes: 'Neapel' (with Asja Lacis, died 1979), 'Gehaltserhöhung?! Wo denken Sie hin!' (with Wolf Zucker, died 1983), 'Revue oder Theater' (with Bernhard Reich, died 1972), 'Vom Weltbürger zum Großbürger' (with Willy Haas, died 1973), 'Das kalte Herz' (with Ernst Schoen, died 1960), 'Allemands de quatre-vingt-neuf' (in Marcel Stora's French), and the two records of the January 1928 hashish experiment headed as Ernst Bloch's (died 1977)", "co-signed with, written by or translated by an author not seventy years dead: left out of the cuts and marked in place with their volume offsets"),
    ("'L'œuvre d'art à l'époque de sa reproduction mécanisée' (Zeitschrift 5, 1936)", "the French is Pierre Klossowski's (died 2001): not cut from the volume"),
    ("'Die Waffen von morgen' (Vossische Zeitung, 29 June 1925)", "German Wikisource attributes it to Dora Sophie Benjamin (died 1964): not seated"),
    ("Adorno, Horkheimer, Marcuse and the rest of the school in their own books", "in copyright: not seated. This is a first gathering, and what it holds of the school is Benjamin and the journal's address"),
]
lic = lambda l: l["payload"] if isinstance(l, dict) else str(l)

def section(i, corpus, sub):
    s = json.loads((A / corpus / "source.json").read_text(encoding="utf-8"))
    o = [f"## Seat 44/{i:02d}: {s['title']}", "", f"*{sub}*", "", f"- Edition: {s['edition']}", f"- Licence: {lic(s['license'])}",
         f"- Record licence: {s['license']['record']}", f"- Works: {s['works']['count']} ({s['works']['units']})"]
    o += [f"- Verified locus: {v}" for v in s["verified_loci"]] + [f"- Locus not found: {v}" for v in s.get("loci_not_found") or []]
    o += [f"- Scope: {s['scope']}", f"- Pinned, not carried: {len(s['pinned_originals']['volumes'])} volumes, each by Internet Archive address, size and SHA-256 (source.json, pinned_originals)"]
    o += [f"- Note: {n}" for n in s.get("notes", [])]
    o += [f"- Files: [the seat](https://www.alexanarch.org/data/corpora/{corpus}/) ({len(s['files'])} files; MANIFEST.sha256). "
          f"Shelf: [traininglayerliterature.org/originals/{corpus}/](https://traininglayerliterature.org/originals/{corpus}/)", ""]
    return o

TITLE = "EA-CORPORA-44: The Forty-Fourth Seating: The Frankfurt School, First Gathering (Walter Benjamin in German, the Gesammelte Schriften cut to his text; the Zeitschrift für Sozialforschung, 1932–1941, pinned, with thirteen articles)"
body = ["### Protocol Version", "", "alexanarch-deposit-protocol/v1", "", "### Title", "", TITLE, "",
        "### Creator", "", "Cranes, Rebekah", "", "### ORCID", "", "0009-0000-1599-0703", "", "### Date", "", "2026-11-28", "",
        "### Description", "",
        "The forty-fourth seating of the originals shelf, two seats. On 27 November 2026 the Frankfurt School was found absent from the library: "
        "no seat for Benjamin, Adorno, Horkheimer, Marcuse or the Institute's journal. This is the first gathering. Seat 44/01 holds Walter "
        "Benjamin in German: thirteen first printings as German Wikisource transcribes them, three scans of printings from 1921, 1923 and 1936, "
        "and the seven volumes of the Gesammelte Schriften cut to his text, without the editors' reports and notes. Seat 44/02 holds the "
        "Zeitschrift für Sozialforschung, 1932–1941: the nine yearly volumes fixed by address and hash, the essay list of each, and thirteen "
        "articles by contributors more than seventy years dead (Benjamin, Grossmann, Bouglé, Tönnies, Beard, Neurath, Neumann). The seating "
        "copies what is in the commons and pins what is only free to read: the core of the school (Horkheimer, Adorno, Marcuse, Fromm, "
        "Pollock, Löwenthal) is in copyright and is held here by address and hash, not as text. What is not seated is declared below with its reason.", "",
        "### Content Type", "", "Dataset", "", "### License", "",
        "CC-BY-4.0 (the deposit and seat records; the seated texts are public domain where the term is the author's life plus seventy years, and the layers taken from German Wikisource carry its CC BY-SA 4.0)", "",
        "### Substrate Disclosure", "",
        "Human–machine collaborative. Rebekah Cranes is a heteronym of Lee Sharks, the standing authority on the EA-CORPORA deposits. The "
        "sources were found, fetched, hashed, cut by character offset, checked at named loci and recorded by Claude (TACHYON) in a claude.ai "
        "session (01NyzQpk) at the author's direction (2026-11-27 23:13 to 2026-11-28 02:34 EST).", "",
        "### Keywords", "",
        "EA-CORPORA, originals shelf, Frankfurt School, Walter Benjamin, Gesammelte Schriften, Passagen-Werk, Über den Begriff der Geschichte, "
        "Ursprung des deutschen Trauerspiels, Einbahnstraße, Kunstwerk essay, Zeitschrift für Sozialforschung, Institut für Sozialforschung, "
        "Henryk Grossmann, Franz Neumann, Otto Neurath, Ferdinand Tönnies, Célestin Bouglé, Charles A. Beard, Carl Gustav Jochmann, commons, pinned originals", "",
        "### Related Identifiers", "", "AXN deposit #1801 — EA-CORPORA-43: the forty-third seating", "",
        "### Version", "", "v1.0", "",
        "### Methodology", "",
        "Wikisource pages fetched once each at a pinned revision and reduced to text by code, each layer checked against its page by character "
        "count. Internet Archive text layers fetched on 2026-11-27 and 2026-11-28, hashed as fetched, and cut by character offset to the "
        "author's text; every cut records its volume and offsets so it can be checked against the whole. Authors' death years checked on "
        "2026-11-28 against German Wikipedia and, for two, the Deutsches Literaturarchiv Marbach authority records. Other hands inside the "
        "volumes were searched for by co-author name in all volumes and by reading every heading in the last part of volume IV; what was found "
        "is left out and marked in place. Loci verified (missing 0 in both seats); manifests verified.", "",
        "### Falsification Conditions", "",
        "A seat is falsified if its files do not verify against its MANIFEST.sha256 at the canonical URL; if a verified locus is absent from "
        "the text it names; if a cut does not match the pinned volume at the offsets it records; if a pinned volume's SHA-256 does not match "
        "the file at the address given as fetched; if a text seated here as an author's is another's; or if an author treated as more than "
        "seventy years dead is not.", "",
        "### Body", "",
        "# EA-CORPORA-44 — The Forty-Fourth Seating: The Frankfurt School, First Gathering", "",
        "The author found the gap on 2026-11-27 at 23:10: \"i think we legitimate havent seated the frankfurt school - if so thats a large "
        "whoops\". The library was checked and held no seat for the school. At 23:13: \"agreed. lets seat\". At 23:39, of the Suhrkamp "
        "volumes: \"both. the versions with the editors notes and the versions without\"; the editors' apparatus is in copyright and was "
        "pinned and not copied, and at 23:59: \"ok. so lets seat all volumes without notes\". On 2026-11-28 at 00:54: \"yup lets cut the "
        "non-commons bits\". At 02:34: \"go\".", "",
        "The seating keeps apart two things that the word free runs together. A text in the commons may be copied and reissued by anyone; "
        "a text that is only free to read has an owner whose word is still needed. What is in the commons is copied in. What is only free "
        "is fixed by address, size and SHA-256, so that a reader can reach it and check it, and is not reissued here.", "",
        "The text layers cut from scans are uncorrected OCR. Umlauts and some letters are misread. They make the words findable and are not reading texts.", ""]
for i, (c, sub) in enumerate(SEATS, 1): body += section(i, c, sub)
body += ["## Declared, not seated", ""] + [f"- {a}: {b}." for a, b in DECLARED] + ["",
         "## Owed", "",
         "- Volumes II to VII of the Gesammelte Schriften are each one cut; cutting them work by work, as volume I is, is owed, and with it a heading-by-heading reading of volumes II, III, V, VI and VII for other hands.",
         "- The rest of the school, as public copies are found.", "",
         "## How the seats were made", "",
         "By the scripts in rebuild/corpora/ea-corpora-44/: build_benjamin_seat.py and build_zfs_seat.py make the seats from the fetched pages "
         "and text layers; finish44.py verifies the loci and writes the manifests; index44.py enters the seats in the two corpora indexes.", "",
         "### Terms", "", "- [x] I read the deposit protocol at https://alexanarch.org/api/deposit-protocol.json",
         "- [x] I confirm this work is deposited under the stated license", "- [x] I confirm the substrate disclosure is accurate",
         "- [x] I understand that deposited content will NOT be used to train enforcement classifiers", ""]
(ROOT / "data/issue-bodies/EA-CORPORA-44-issue.md").write_text("\n".join(body), encoding="utf-8")
packet = {"schema": "alexanarch-internal-session-packet/v1", "registry_patch": {
    "wiki_article": "EA-CORPORA-44 is the forty-fourth seating of the Crimson Hexagonal Archive's originals shelf, prepared under Rebekah Cranes, the standing authority on the EA-CORPORA deposits, on 28 November 2026, after the Frankfurt School was found absent from the library. It is a first gathering in two seats. Seat 44/01 holds Walter Benjamin in German: thirteen first printings from German Wikisource, three scans of printings of 1921, 1923 and 1936, and the seven volumes of the Gesammelte Schriften cut by character offset to Benjamin's text, without the editors' reports and notes, which are in copyright; eight pieces co-signed with, written by or translated by authors not seventy years dead are left out and marked in place. Seat 44/02 holds the Zeitschrift für Sozialforschung, 1932–1941: nine yearly volumes fixed by Internet Archive address, size and SHA-256, the essay list of each volume, and thirteen articles by contributors more than seventy years dead (Benjamin, Henryk Grossmann, Célestin Bouglé, Ferdinand Tönnies, Charles A. Beard, Otto Neurath, Franz Neumann). The articles of Horkheimer, Adorno, Marcuse, Fromm, Pollock and Löwenthal are in copyright and are pinned, not copied. The seating distinguishes what is in the commons, which it copies, from what is only free to read, which it fixes by address and hash. The text layers cut from scans are uncorrected OCR.",
    "concepts_attested_none": True, "lexical_attested_none": True,
    "related_deposits": [{"deposit": 1801, "relation": "EA-CORPORA-43, the preceding seating"}]}, "lexical_mints": []}
(ROOT / "data/issue-bodies/EA-CORPORA-44-packet.json").write_text(json.dumps(packet, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("body", len(body), "lines", sum(len(x) for x in body), "chars")
