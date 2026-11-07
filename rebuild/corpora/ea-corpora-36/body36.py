#!/usr/bin/env python3
"""Write the EA-CORPORA-36 deposit issue body from the thirty-two seat records, the cross-references (xref36.json), the open scholarship held by
reference (refs36.json) and the declared absences (absences36.json), in the form of body35.py. Edition lines, loci, licences and scopes are read from data/corpora/<seat>/source.json.
-> data/issue-bodies/EA-CORPORA-36-issue.md"""
import json, pathlib, glob
from collections import Counter

H = pathlib.Path(__file__).resolve().parent; ROOT = H.parents[2]
A = ROOT / "data/corpora"
SPECS = sorted((json.load(open(f, encoding="utf-8")) for f in glob.glob(str(H / "spec36-*.json"))), key=lambda s: s["seat"])
XREF = json.loads((H / "xref36.json").read_text(encoding="utf-8"))
ABS = json.loads((H / "absences36.json").read_text(encoding="utf-8"))
REFS = json.loads((H / "refs36.json").read_text(encoding="utf-8"))
lic = lambda l: l["payload"] if isinstance(l, dict) else str(l)
WALL = {"rights": "in copyright", "pay": "behind a subscription", "access": "open in law and unlocated or unfetched in session", "private": "held privately"}


def section(spec):
    corpus = spec["corpus"]
    s = json.loads((A / corpus / "source.json").read_text(encoding="utf-8"))
    w = s["works"]["list"]
    out = [f"## Seat {s['seat'].split('/')[1] if '/' in s['seat'] else s['seat']} — {s['title']}", ""]
    out += ["- Works:"] + [f"  - {x['work']}" for x in w]
    out += [f"- Language: {s['language']}", f"- Licence: {lic(s['license'])}"] + [f"- Verified locus: {v}" for v in s["verified_loci"]]
    if s.get("loci_not_found"):
        out += [f"- Locus not found: {v}" for v in s["loci_not_found"]]
    nt = sum(1 for x in w if x.get("text"))
    out += [f"- Lines: {s['lines_total']:,} in {nt} text file{'s' if nt != 1 else ''}", f"- Scope: {s['scope']}", f"- Why seated: {s['why_seated']}",
            f"- Files: [the seat](https://www.alexanarch.org/data/corpora/{corpus}/) — [source.json](https://www.alexanarch.org/data/corpora/{corpus}/source.json), "
            f"[MANIFEST.sha256](https://www.alexanarch.org/data/corpora/{corpus}/MANIFEST.sha256). Shelf: "
            f"[traininglayerliterature.org/originals/{corpus}](https://traininglayerliterature.org/originals/{corpus}/)", ""]
    return "\n".join(out), s


title = ("EA-CORPORA-36 — The Thirty-Sixth Seating: Sappho's Reception and the Future Reader — the Translators, Editors and Critics from "
         "Hall's Longinus (1652) to Cox (1925), the Ancient Dossier of Remembrance, the Scholarship Open and Walled, the Future-Reader Strata "
         "from Dante to the WIPP Markers, and the Jealousy Reading from Lucretius to Hermann")
pa, pb, pf, tot, nw = [], [], [], 0, 0
for sp in SPECS:
    t, s = section(sp); n_ = int(sp["seat"].split("/")[1]); (pa if n_ <= 23 else pb if n_ <= 32 else pf).append(t); tot += s["lines_total"]; nw += s["works"]["count"]
nfiles = sum(1 for sp in SPECS for p in (A / sp["corpus"]).rglob("*") if p.is_file())
nloci = sum(len(sp["loci"]) for sp in SPECS)

xr = ["# Part C — Cross-references: the strata already seated", "",
      "The library already held these texts when the seating was asked for; they are entered here by reference to the seat that holds them, "
      "with the locus asserted present in the seated text and the text's SHA-256 at the time of this seating. Nothing is re-seated.", "",
      "| Stratum | Locus | Seat | Text | Found |", "|---|---|---|---|---|"]
for x in XREF:
    xr.append(f"| {x['stratum']} | {x['label']} | {x['seat']} ({x['corpus']}) | [{x['text']}]({x['url']}) | {x['find']} |")
xr += ["", "Also seated and read with this seating: the melic poets with Sappho whole, Bergk's Poetae Melici (EA-CORPORA-33/04, poetae-melici-bergk) "
       "and Edmonds's Lyra Graeca I (33/05, lyra-graeca-edmonds-i), with Pindar and Bacchylides (33/01, 33/02); Dickinson's manuscripts and the "
       "1894 Letters (EA-CORPORA-02/14, dickinson-mss); the Walt Whitman Archive's editions of Leaves of Grass (EA-CORPORA-03/01, whitman).", ""]

rf = ["# Part D — The open scholarship, held by reference", "",
      "The modern scholarship on Sappho and the future reader that is free to read and in copyright, or licensed for reading in a form the seating "
      "could not fetch. Each work held by reference was fetched in session: its URL, the SHA-256 and size of the bytes as fetched, the rights "
      "statement as the source gives it, and short loci asserted present in the text read from those bytes are recorded; nothing is copied into "
      "the library. The pointers name what could be reached and what could not.", "", "## Held by reference", ""]
for r in REFS:
    if r["held"] == "by reference":
        rf += [f"- {r['work']}. [{r['url']}]({r['url']}) — fetched {r['fetched']}, {r['bytes']:,} bytes, sha256 {r['sha256_as_fetched']}. {r['rights']}"]
        rf += [f"  - Verified locus: {v}" for v in r["verified_loci"]]
rf += ["", "## Pointers", ""] + [f"- {r['work']}. [{r['url']}]({r['url']}) — {r['rights']} {r['status']}" for r in REFS if r["held"] == "pointer"] + [""]

ab = ["# Part E — Declared absences", "",
      "Commons only: works behind pay-, access- and rights-walls are declared, with the wall and, where one was verified, a pointer. "
      f"{len(ABS)} entries: " + "; ".join(f"{v} {WALL[k]}" for k, v in Counter(a['wall'] for a in ABS).items()) + ".", ""]
for part, head in (("A", "## The reception"), ("B", "## The future reader"), ("F", "## The jealousy reading (v1.1)")):
    ab += [head, ""] + [f"- {a['work']} — {WALL[a['wall']]}. {a['status']}" for a in ABS if a["part"] == part] + [""]

hdr = f"""# {title}

# EA-CORPORA-36 — The Thirty-Sixth Seating

The author asked for the seating on 2026-11-07: "i think we need a sappho reception history ea-corpora, whatever's public. translators, scholars. theres some ground work in the archive, notes towards a future reader i believe. the seating can include everything thats publicly available as well as declared absences and pointers for material behind pay- and access- and rights-walls"; and then: "sappho reception history + future reader frameworks and related". Of the first draft, which held the translators and left the scholarship among the absences, he wrote: "this seems light on scholarly material related to the future reader proposition or sappho... and that is the focus of notes towards a future reader, is it not?" The scholarship that could be fetched has been brought in (Parts A and D).

The research occasion is twofold. The revision of Closing the Fragment (v7, a draft of 2026-11-07 for Alexanarch) controls a public composition's closure of fragment 31 against the translators who closed it before: Hall's Longinus ends its four stanzas on "Yet ſince I'me wretched I muſt dare." (1652); Boileau ends his three quatrains on the fifth stanza's opening, that all must be hazarded (in the 1683 printing of the Traité, first published 1674); Philips's version in the Spectator ends on "I fainted, sunk, and dy'd away." (1711); Merivale ends at the failing of "Both sight and sound" (1813); Vivien's prose carries "Mais il faut oser tout..." (1903); Wharton's literal version carries "But I must dare all, since one so poor ..." (1908), the line the January composition's closing aligns with. The Sappho Future Reader framework, whose groundwork is Research Notes Towards the Future Reader (#1548), maps the future reader as a position with a history in twelve strata, from the epigraphic address through Thucydides' possession for all time, Ovid's legar, the scriptural writing for a generation to come, Dante's lettor and Shakespeare's eyes not yet created, the Romantic culture of posterity, Whitman's and Baratynsky's readers in posterity, to the WIPP marker studies' message for readers ten thousand years out.

The seating holds what is public. Part A (seats 36/01–36/23) holds the reception of Sappho and its scholarship. Seats 36/01–36/18 run from 1652 to 1925: the Longinian translators (Hall, Boileau), the eighteenth century's English Sappho (the Spectator, Pope's Ovid, Fawkes), the nineteenth century's question of her character (Welcker, Mure) and its poets and critics (Merivale, Swinburne, Higginson, Symonds), and the editions and renderings of the twentieth century's first quarter (Vivien, Carman, Wharton, O'Hara and Stacpoole, Wilamowitz, Robinson, Cox). Seats 36/19–36/23 hold the ground the future-reader question is argued on: the remembrance fragments in the books that carry them (Dio's Corinthian oration with fr. 147; Plutarch with fr. 55 and Sappho's pride in the καλλιγραφία of her songs; Stobaeus; the Oxyrhynchus volume with her fourth book and Ibycus's promise of imperishable fame to Polycrates), the epigrams of the Greek Anthology in which the stranger at Sappho's tomb is the reader addressed, Smyth's commentary printing fr. 147 under Horace's "non omnis moriar", Jebb's lectures, and the Wikipedia sentence that names the written-futurity view and cites for it the chapter written against it. Part B (36/24–36/32) holds the future-reader strata the library did not hold: Ennius in Cicero, Dante, Chaucer, Shakespeare's sonnets, Milton, the Romantic sentences (Wordsworth, Keats, Shelley, Stendhal), Dickinson as Todd and Higginson printed her, Baratynsky with Mandelstam's bottle quoted beside him, and the Sandia report of 1993. Part C enters by reference the strata the library already held (Homer, Herodotus, Thucydides, the Phaedrus, Horace, Ovid, the Hebrew Bible, Nietzsche, Whitman) and the witnesses of fragment 31 (Longinus, Catullus, the diplomatic layer). Part D holds the modern scholarship that is free to read and in copyright by reference, each work fetched, hashed and its loci verified: D'Angour's chapter of 2013 and his note of 2023, Finglass on the New College manuscript (2025), Garner on oral tradition (2011), and the Bryn Mawr reviews of Svenbro, of the volume carrying Lardinois 2008, and of Yatromanolakis; with pointers to Lardinois 2008 in the Radboud repository and to the open editions of Yatromanolakis, Greene–Skinner, Calame and The Newest Sappho, whose texts did not reach the session. Part E declares the rest: {len(ABS)} works, each with the wall that keeps it out.

Version 1.1 (7 November 2026) adds Part F (36/33–36/40) at the author's word of 14:42 EST, "lets expand it to include all materials well need for the reception study in one bundle", the study being his question of 14:13 EST: "im particularly interested in how sappho became a jealous woman rather than a writer, which i believe begins with lucretius". Part F seats the jealousy reading's sources that the library lacked: Hermann's Elementa doctrinae metricae (1816), where the jealousy reading is stated as the sense of the poem's last line, "invidens Sappho viro illi, omnia sibi audenda dicit", in the same year Welcker (36/06) answers it by name; Plutarch's Demetrius and Amatorius, the physician's reading of "the things of Sappho" in Antiochus and the poem quoted as what happens at the beloved's appearing; the Erasistratus story's other carriers, Valerius Maximus and Appian; Gellius with Valerius Aedituus's Latin version before Catullus; Maximus of Tyre, who sets Sappho's rivals beside Socrates's; Racine's Phèdre; Smollett's Roderick Random, with the added stanza Wharton reprints; and Wikipedia's "Sappho 31" at the revision current when the study opened. Part C adds fourteen cross-references for the study: Lucretius's division of the poem's symptoms into fear (DRN 3.155–58) and the lover's suspicion (4.1139–40), Theocritus's Simaetha, Apollonius's Medea, Horace and Ovid on Sappho, Herodotus and Athenaeus on her brother's Doricha, Welcker's refusal of the jealousy reading, Smyth's, Wilamowitz's jealousy in fr. 130, and the Spectator on jealousy. Part E adds the walled scholarship of the jealousy reading.

{len(SPECS)} seats, {nw} works, {tot:,} lines, {nfiles} files, {nloci} loci verified in the text layers; {len(XREF)} cross-references verified in seated texts; {sum(1 for r in REFS if r['held'] == 'by reference')} works of scholarship held by reference and {sum(1 for r in REFS if r['held'] == 'pointer')} pointers; {len(ABS)} declared absences.
"""
tail = """## How the seats were made

Every seat was fetched in session and hashed into its MANIFEST.sha256, with a source.json recording edition, origin, licence, normalization, the loci verified in the text layer, and the research the seat was made for. The loci keep their sources' readings: long s in the TCP transcription of Hall, and the OCR's readings in the Archive's text layers (Boileau's long s read as f, Welcker's Fraktur, Higginson's Aegean read as -^gean). Welcker's seat is the Bayerische Staatsbibliothek copy; the Google scan of the same book was fetched first and set aside because its OCR reads the Fraktur as noise. The builders are under rebuild/corpora/ea-corpora-36/: gen_spec36.py writes the specs; build36.py builds each seat (the thirty-fourth seating's builder with one kind added, the Text Creation Partnership's TEI); add_loci36.py enters the loci, each asserted present in its text layer; xref36.py verifies the cross-references in the seats that hold them; refs36.py fetches, hashes and verifies the scholarship held by reference; absences36.py writes the declared absences; index_seats36.py enters the seats in the index; seat_axns36.py gives them their AXNs once deposited; and body36.py writes this body.
"""
body = (hdr + "\n# Part A — Sappho's reception, 1652–1925, and the ground of the future-reader question\n\n" + "\n".join(pa) + "\n# Part B — The future reader\n\n" + "\n".join(pb) + "\n# Part F — The jealousy reading (v1.1)\n\n" + "\n".join(pf)
        + "\n" + "\n".join(xr) + "\n" + "\n".join(rf) + "\n" + "\n".join(ab) + "\n" + tail)
desc = ("The thirty-sixth seating of the originals shelf: Sappho's reception and the future reader, seated for the revision of Closing the Fragment "
        "and the Sappho Future Reader framework (#1548). Part A, twenty-three seats: the translators, editors and critics of Sappho from Hall's Longinus "
        "(1652) and Boileau through the Spectator, Pope, Fawkes, Welcker, Merivale, Mure, Swinburne, Higginson, Symonds, Vivien, Carman, Wharton, "
        "O'Hara, Stacpoole, Wilamowitz and Robinson to Cox (1925); the remembrance fragments in their carriers (Dio, Plutarch, Stobaeus, P.Oxy. XV); the "
        "Anthology's epigrams on Sappho; Smyth and Jebb; and the Wikipedia sentence on writing for future readers. Part B, nine seats, the future-reader "
        "strata the library lacked, from Ennius in Cicero and Dante to Baratynsky and the Sandia WIPP marker report of 1993. Part C, the strata already "
        "seated, by reference; Part D, the open scholarship in copyright (D'Angour, Finglass, Garner, the BMCR reviews) fetched, hashed and held by "
        "reference, with pointers to the CHS and Brill open editions; Part E, the works behind pay-, access- and rights-walls, declared. Version 1.1 adds "
        "Part F, eight seats for the reception study of the jealousy reading: Hermann 1816, Plutarch's Demetrius and Amatorius, Valerius Maximus and Appian, "
        "Gellius, Maximus of Tyre, Racine's Phèdre, Smollett, and Wikipedia's 'Sappho 31', with the ancient and modern witnesses already seated "
        "(Lucretius, Theocritus, Apollonius, Welcker, Smyth) entered by reference. Each seat in its original language, hashed, with its loci verified in the text layer.")
kw = ("EA-CORPORA, originals shelf, Sappho, Sappho 31, fragment 31, fr. 147, fr. 55, reception history, classical reception, translation history, "
      "Longinus, On the Sublime, John Hall, Boileau, Spectator 229, Ambrose Philips, Pope, Heroides 15, Fawkes, Welcker, Mure, Swinburne, Symonds, "
      "Renée Vivien, Bliss Carman, Wharton, Wilamowitz, Smyth, Dio Chrysostom, Plutarch, Oxyrhynchus Papyri, Greek Anthology, tenth Muse, "
      "Lardinois, Svenbro, D'Angour, Finglass, written futurity, future reader, posterity, monumentum, Dante, "
      "Baratynsky, WIPP, declared absences, Closing the Fragment, jealousy reading, Hermann, Lucretius, Erasistratus")
issue = "\n".join([
    "### Protocol Version\n\nalexanarch-deposit-protocol/v1\n",
    f"### Title\n\n{title}\n", "### Creator\n\nCranes, Rebekah\n", "### ORCID\n\n0009-0000-1599-0703\n",
    "### Date\n\n2026-11-07\n", f"### Description\n\n{desc}\n", "### Content Type\n\nDataset\n", "### License\n\nCC-BY-4.0\n",
    "### Substrate Disclosure\n\nHuman–machine collaborative. Rebekah Cranes is a heteronym of Lee Sharks, the standing authority on the EA-CORPORA deposits. The sources found, fetched, verified, hashed and indexed, the cross-references verified, the absences declared, and the records drafted, in session by TACHYON (Claude, Anthropic) under MANUS (Lee Sharks) direction. The request and the research occasion are Lee Sharks's; the editions within each seat were chosen in session and are stated per seat. CC-BY-4.0 applies to this record and the seat records.\n",
    f"### Keywords\n\n{kw}\n",
    "### Related Identifiers\n\nAXN deposit #1548 — Research Notes Towards the Future Reader, the groundwork of the seating\n"
    "AXN deposit #1270 — ΦΑΙΝΕΤΑΙ ΜΟΙ: Sappho 31 and the Inscription of the Future Reader\n"
    "AXN deposit #1532 — The Transforming Body of Sappho 31: A Survey of Ancient Reception\n"
    "AXN deposit #1476 — φωνῆς δίχα: The Hanging Line as the Complete Poem — Sappho 31 in Longinus\n"
    "AXN deposit #1478 — The Socket and the Stamp: Sappho 31.17 as Completed Composition\n"
    "AXN deposit #1508 — EA-CORPORA-01/10: Sappho, Fragment 31, the diplomatic layer\n"
    "AXN deposit #1504 — EA-CORPORA-01/06: Longinus, De Sublimitate\n"
    "AXN deposit #1500 — EA-CORPORA-01/02: Catullus\n"
    "AXN deposit #1738 — EA-CORPORA-33: Sappho whole with the melic poets\n"
    "AXN deposit #1744 — EA-CORPORA-35: the thirty-fifth seating, whose form this seating follows\n",
    "### Version\n\nv1.1\n",
    "### Methodology\n\nEach seat fetched in session from the source its record names (the Internet Archive, Project Gutenberg, the Text Creation Partnership, Perseus, Wikisource), kept as served, reduced to a text layer by code and hashed into its MANIFEST.sha256; licences read at the file; loci verified by substring in the text layer, in the source's own readings; public-domain status checked against first publication and the author's death, and stated per jurisdiction where it differs. The strata the library already held were verified in their seats and entered by reference. Works not open were declared with their walls. No text corrected by hand. The builders and this body are under rebuild/corpora/ea-corpora-36/.\n",
    "### Falsification Conditions\n\nA seat is falsified if its files do not verify against its MANIFEST.sha256 at the canonical URL; if a verified locus is absent from the text layer it names; if a work is misattributed, misdated or assigned to the wrong edition; if a licence recorded for an item is not the one its source states; if a work seated as public domain is not, in the jurisdiction stated; if a cross-reference's locus is absent from the seated text it names; if a declared absence is in fact open in law and in an open text layer the seating names as not located; or if the four surfaces (seat, index, deposit, shelf) disagree.\n",
    f"### Body\n\n{body}",
    "### Terms\n\n- [x] I read the deposit protocol at https://alexanarch.org/api/deposit-protocol.json\n- [x] I confirm this work is deposited under the stated license\n- [x] I confirm the substrate disclosure is accurate\n- [x] I understand that deposited content will NOT be used to train enforcement classifiers\n"])
out = ROOT / "data/issue-bodies/EA-CORPORA-36-issue.md"
out.write_text(issue, encoding="utf-8")
print(out, len(body.split()), "words in body;", len(desc), "chars in description;", len(SPECS), "seats;", nw, "works;", tot, "lines;", nfiles, "files;", nloci, "loci")
