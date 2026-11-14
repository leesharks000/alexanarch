#!/usr/bin/env python3
"""Write the EA-CORPORA-38 deposit issue body from the sixteen seat records (the form of body37.py).
Edition lines, loci, licences and scopes are read from data/corpora/<seat>/source.json.
-> data/issue-bodies/EA-CORPORA-38-issue.md"""
import json, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[3]
A = ROOT / "data/corpora"
SEATS = [
 ("kant-akademie-ausgabe", "Seat 38/01 — Kant's gesammelte Schriften, Akademie-Ausgabe I–XVIII (1910–1928)", "The Werke, the Briefwechsel and the Nachlass through Metaphysik II, XVI the Reflexionen zur Logik"),
 ("alexander-in-apr-wallies-1883", "Seat 38/02 — Alexander of Aphrodisias, In Analytica priora I (Wallies, CAG II.1, 1883)", "The first surviving commentary, with Aristotle's companions against him at 124.8"),
 ("philoponus-in-apr-wallies-1905", "Seat 38/03 — John Philoponus, In Analytica priora (Wallies, CAG XIII.2, 1905)", "ὁ φιλόσοφος against οἱ ἑταῖροι αὐτοῦ"),
 ("theophrastus-characteres-diels-1909", "Seat 38/04 — Theophrastus, Characteres (Diels, 1909)", "The draft position: from the Peripatetic definition to the drawn person"),
 ("epictetus-dissertationes-schenkl-1916", "Seat 38/05 — Epictetus, Dissertationes (Schenkl, 1916)", "The Stoic line, the Master Argument at 2.19"),
 ("cicero-topica-wilkins-1902", "Seat 38/06 — Cicero, Topica (Wilkins, 1902)", "The Latin door: inveniendi and iudicandi"),
 ("bacon-novum-organum-1620", "Seat 38/07 — Bacon, Novum Organum I–II (1620)", "The syllogism refused as an instrument of discovery"),
 ("hume-treatise-enquiry", "Seat 38/08 — Hume, A Treatise of Human Nature and An Enquiry concerning Human Understanding", "The inference from cause to effect taken apart"),
 ("carroll-symbolic-logic-1897", "Seat 38/09 — Lewis Carroll, Symbolic Logic, Part I (4th ed., 1897)", "The syllogism as a method for puzzles"),
 ("hegel-wissenschaft-der-logik", "Seat 38/10 — Hegel, Wissenschaft der Logik", "The syllogism taken into the concept: Der Schluß"),
 ("frege-begriffsschrift-1879", "Seat 38/11 — Frege, Begriffsschrift (1879)", "Inference rebuilt from the judgment-stroke"),
 ("peirce-logic-papers-1867-1878", "Seat 38/12 — Peirce, the logic papers of 1867 and the Illustrations of the Logic of Science (1877–1878)", "Deduction, induction and hypothesis"),
 ("boethius-logica-migne-pl64", "Seat 38/13 — Boethius, the logical works (Migne, PL 64, 1847)", "The Latin Organon as the schools received it"),
 ("nyaya-sutra-vatsyayana-1896", "Seat 38/14 — Nyāyasūtra with Vātsyāyana's Bhāṣya (Vizianagram, 1896)", "Anumāna without the Organon"),
 ("ibn-sina-isharat-forget-1892", "Seat 38/15 — Ibn Sīnā, al-Ishārāt wa-l-tanbīhāt I (Forget, 1892)", "Qiyās, istiqrāʾ, tamthīl"),
 ("buridan-sophismata-c1489", "Seat 38/16 — John Buridan, Sophismata ([Paris, c. 1489])", "The commons witness to Buridan's logic"),
]
lic = lambda l: l["payload"] if isinstance(l, dict) else str(l)


def research(r):
    if isinstance(r, dict):
        return "; ".join(f"{k.replace('_', ' ')}: {v}" for k, v in r.items())
    return str(r)


def section(corpus, heading, sub):
    s = json.loads((A / corpus / "source.json").read_text(encoding="utf-8"))
    w = s["works"]["list"]
    out = [f"## {heading}", "", f"*{sub}*", "", "- Works:"] + [f"  - {x['work']}" for x in w]
    out += [f"- Licence: {lic(s['license'])}"] + [f"- Verified locus: {v}" for v in s["verified_loci"]]
    out += [f"- Locus not found: {v}" for v in s.get("loci_not_found") or []]
    nt = sum(1 for x in w if x.get("text"))
    out += [f"- Lines: {s['lines_total']:,} in {nt} text file{'s' if nt != 1 else ''} ({len(w)} works)",
            f"- Normalization: {s['normalization']}", f"- Scope: {s['scope']}",
            f"- Research: {research(s['research'])}", f"- Why seated: {s['why_seated']}"]
    for k in ("held_out", "duplicate_not_seated"):
        if s.get(k):
            out.append(f"- {k.replace('_', ' ').capitalize()}: {s[k]}")
    out += [f"- Files: [the seat](https://www.alexanarch.org/data/corpora/{corpus}/) — [source.json](https://www.alexanarch.org/data/corpora/{corpus}/source.json), "
            f"[MANIFEST.sha256](https://www.alexanarch.org/data/corpora/{corpus}/MANIFEST.sha256). Shelf: "
            f"[traininglayerliterature.org/originals/{corpus}](https://traininglayerliterature.org/originals/{corpus}/)", ""]
    return "\n".join(out), s


title = ("EA-CORPORA-38 — The Thirty-Eighth Seating: The Reception History of Inference — Kant Whole (Akademie-Ausgabe I–XVIII), "
         "the Commentators, the Latin Handbooks, the Early-Modern Refusals, the Nineteenth-Century Rebuilds, and the Traditions beside the Organon")
parts, tot = [], 0
for c, h, sub in SEATS:
    t, s = section(c, h, sub); parts.append(t); tot += s["lines_total"]
nfiles = sum(1 for c, _, _ in SEATS for p in (A / c).rglob("*") if p.is_file())

hdr = f"""# {title}

# EA-CORPORA-38 — The Thirty-Eighth Seating

The author asked for the gathering on 2026-11-13, for the construction and reception history of inference that is now part of Critique of Pure Inference: "what we're trying to trace is the history of how bad inference came to be operative", with Kant seated whole, and Alexander's commentary on the Prior Analytics ruled into the package ("needs to be in the corpora package"). On 2026-11-14 he set the form: "lets continue to assemble and we'll deposit and seat the whole thing as a massive batch" (01:25 EST), and then "lets deposit with what we have and leave pointers to the rest" (08:57).

The sixteen seats run the line the reception history reads. Kant's verdict in the preface to the second Critique of Pure Reason, that logic "auch bis jetzt keinen Schritt vorwärts hat thun können" since Aristotle (B viii; AA III 7), is held in the whole Akademie-Ausgabe through XVIII (38/01), so the verdict can be read beside the Logik Jäsche made from Kant's copy of Meier's Auszug, which Jäsche's preface calls "das Materialien-Magazin" of the lectures (AA IX), and beside the Reflexionen zur Logik in XVI, where the history of logic is drafted as a list: "2. Aristotelici: Theophrast, Demetrius Phalereus". Behind the verdict stand the commentators who read the Prior Analytics with its school beside it: Alexander (38/02), whose ἑταῖροι of Aristotle, Theophrastus and Eudemus, dissent on the mixtures at In APr 124.8, and Philoponus (38/03), who names the school as ὁ φιλόσοφος against οἱ ἑταῖροι αὐτοῦ; and Theophrastus's Characters (38/04), the draft position of The Production of Readers (#1767). The Stoic line (Epictetus, 38/05) and the Latin door (Cicero's Topica, 38/06; Boethius in Migne PL 64, 38/13) carry the syllogism into the schools; Buridan (38/16) stands for the late-medieval logic whose Consequentiae the commons does not hold. Bacon (38/07) and Hume (38/08) refuse it as an instrument of discovery and of matter of fact; Hegel (38/10) takes it into the concept; Carroll (38/09) makes it a method for puzzles; Frege (38/11) rebuilds inference from the judgment-stroke; Peirce (38/12) names the third kind, hypothesis, with a bag of beans. Two traditions reason about inference without the Organon at their centre and are seated in their own languages: the Nyāyasūtra with Vātsyāyana's Bhāṣya in Sanskrit (38/14), and Ibn Sīnā's Ishārāt in Arabic (38/15), whose logic divides argument into «القياس والاستقراء والتمثيل».

Already seated and not reseated: the Prior and Posterior Analytics, the Topics and the Sophistical Refutations, in the Aristotle seat (EA-CORPORA-04/01; its text file tlg001, labelled Analytica priora, holds Bekker's text of both Analytics — a label to be repaired, recorded here); Theophrastus's other works (EA-CORPORA-09/01); Hegel's Differenz and the Plato lectures (EA-CORPORA-32/10); Cicero (EA-CORPORA-13/03); Gödel and the exact sciences (EA-CORPORA-30, #1720).

## Pointers to the rest

Held for a later seating, with what is known of each:

- Kant, AA XIX–XXIII (printed 1934, 1942, 1936, 1938, 1955): the Reflexionen zur Moralphilosophie and Rechtsphilosophie, the Bemerkungen and Vorarbeiten, the Opus postumum. Internet Archive items kantsgesammeltes19imma–kantsgesammeltes23imma (Gumberg Library); the Archive's text layers were fetched in session and are not seated. They are later than the 1931 line the seated volumes stand on, and whether they are seated is the author's ruling. The Bonn Kant-Korpus (korpora.org) serves AA I–XXIII as text and is named as a route, not used.
- Hegel, Encyklopädie der philosophischen Wissenschaften im Grundrisse §§181–193 (der Schluß): the first edition (Heidelberg, 1817; Internet Archive 10045975, bub_gb_hL8IAAAAQAAJ), the second (1827; 11759980, 10045976) and the Werke text (1840–1845; georgwilhelmfri00henngoog, georgwilhelmfri01henngoog). Fraktur scans; to be read by the OCR made for 38/01.
- Ibn Sīnā, al-Shifāʾ, al-Manṭiq, al-Qiyās: the edition of S. Zayed (Cairo, 1964) is the only edition and is not in the commons. Declared absent.
- John Buridan, Tractatus de consequentiis: no commons scan of a print or a manuscript was found in session (the Internet Archive, e-rara and the MDZ searched on 2026-11-14; Gallica refused the session); the edition of H. Hubien (Louvain, 1976) is in copyright. Declared absent.
- Theophrastus's logical fragments: the edition of Fortenbaugh, Huby, Sharples and Gutas (Brill, 1992) is in copyright; the fragments are read in the commentators seated here (38/02, 38/03). Declared absent as an edition.
"""
tail = f"""## How the seats were made

Every seat was fetched in session and hashed into its MANIFEST.sha256, with a source.json recording edition, origin, licence, normalization, the loci verified in the text layer, and the research the seat was made for. Two seats carry an OCR made for them because the Internet Archive's own layer cannot read the type: 38/01, Fraktur, by tesseract 5 with the deu_latf model, page by page from the Archive's images, about 9,800 pages and none failed; 38/15, Arabic, by tesseract 5 with the ara model, 232 pages. In both the Archive's own layer is held beside the new one for comparison. The commentaries (38/02, 38/03) carry Wallies's pages as [p. N] and his numbered lines as |L from the First1KGreek TEI, so a locus can be cited by page and line from the text layer; the TEI also marks manuscript folios (|40r) and some line numbers out of sequence, so a citation gives the page and the line numbers on either side. Three volumes of Peirce (38/12) are held whole because their text layers drop the running heads; each paper is located by the line of its heading. The loci keep the OCR's readings. The builders are under rebuild/corpora/ea-corpora-38/ (prepare_texts38.py, build_seats38.py, build_kant38.py, index38.py, seat_axns38.py, and body38.py, which writes this body); NOTE.md records the order.

In all: sixteen seats, {nfiles:,} files, {tot:,} lines of text.
"""
body = hdr + "\n" + "\n".join(parts) + "\n" + tail
desc = ("The thirty-eighth seating of the originals shelf, sixteen seats: the reception history of inference, gathered for Critique of Pure Inference. "
        "Kant's gesammelte Schriften whole through AA XVIII, with a Fraktur OCR made for the seat; Alexander and Philoponus on the Prior Analytics (Wallies), with Aristotle's companions against him; "
        "Theophrastus's Characters; Epictetus; Cicero's Topica; Boethius's logical works (PL 64); Buridan's Sophismata; Bacon's Novum Organum; Hume; Hegel's Wissenschaft der Logik; Carroll's Symbolic Logic; "
        "Frege's Begriffsschrift (1879); Peirce's logic papers of 1867–1878; the Nyāyasūtra with Vātsyāyana's Bhāṣya in Sanskrit; and Ibn Sīnā's Ishārāt in Arabic, with an Arabic OCR made for the seat. "
        "Pointers to Kant AA XIX–XXIII, Hegel's Encyklopädie, and the declared absences.")
kw = ("EA-CORPORA, originals shelf, inference, syllogism, reception history of logic, Critique of Pure Inference, Kant, Akademie-Ausgabe, Jäsche Logik, Reflexionen zur Logik, Alexander of Aphrodisias, Philoponus, "
      "Prior Analytics, Theophrastus, Eudemus, Characters, Epictetus, Master Argument, Cicero Topica, Boethius, Buridan, Bacon, Novum Organum, Hume, Hegel, Wissenschaft der Logik, Carroll, Frege, Begriffsschrift, "
      "Peirce, abduction, hypothesis, Nyāya, anumāna, Vātsyāyana, Ibn Sīnā, Avicenna, Ishārāt, qiyās")
related = "\n".join([
    "AXN deposit #1766 — Critique of Pure Inference, the research this seating serves",
    "AXN deposit #1767 — The Production of Readers, whose draft position the Characters seat holds",
    "AXN deposit #1733 — Legitimately Many, the reception history of the many-author reading",
    "AXN deposit #1720 — EA-CORPORA-30: the exact sciences, with Gödel",
    "AXN deposit #1731 — EA-CORPORA-32: the remaining debts of Legitimately Many, with Hegel's seat",
    "AXN deposit #1591 — EA-CORPORA-13: the Alexander seam",
    "AXN deposit #1760 — EA-CORPORA-37: the thirty-seventh seating"]) + "\n"
issue = "\n".join([
    "### Protocol Version\n\nalexanarch-deposit-protocol/v1\n",
    f"### Title\n\n{title}\n", "### Creator\n\nCranes, Rebekah\n", "### ORCID\n\n0009-0000-1599-0703\n",
    "### Date\n\n2026-11-14\n", f"### Description\n\n{desc}\n", "### Content Type\n\nDataset\n", "### License\n\nCC-BY-4.0\n",
    "### Substrate Disclosure\n\nHuman–machine collaborative. Rebekah Cranes is a heteronym of Lee Sharks, the standing authority on the EA-CORPORA deposits (named by the author on 2026-11-04 and held at his word of 2026-11-05). The sources found, fetched, OCR'd where the served text layer could not read the type, verified, hashed and indexed, and the records drafted, in session by TACHYON (Claude, Anthropic) under MANUS (Lee Sharks) direction. The gathering, its object and its form are Lee Sharks's; the editions within each seat were chosen in session and are stated per seat. CC-BY-4.0 applies to this record and the seat records.\n",
    f"### Keywords\n\n{kw}\n", f"### Related Identifiers\n\n{related}", "### Version\n\nv1.0\n",
    "### Methodology\n\nEach seat fetched in session from the source its record names (First1KGreek and Perseus on GitHub; the Latin Library; Project Gutenberg; the Internet Archive), kept as served, reduced to a text layer by code and hashed into its MANIFEST.sha256; where the served text layer could not read the type (Fraktur, Arabic), an OCR made from the source's page images by tesseract 5, page by page, recorded as the seat's and not corrected; licences read at the item; loci verified by substring in the text layer, in the OCR's own readings; public-domain status checked against first publication and the author's death. No text corrected by hand. The builders and this body are under rebuild/corpora/ea-corpora-38/.\n",
    "### Falsification Conditions\n\nA seat is falsified if its files do not verify against its MANIFEST.sha256 at the canonical URL; if a verified locus is absent from the text layer it names; if a work is misattributed, misdated or assigned to the wrong edition; if a licence recorded for an item is not the one its source states; if a work seated as public domain is not, in the jurisdiction stated; if an OCR said to be made from a source's page images is not reproducible from them by the stated model; or if the four surfaces (seat, index, deposit, shelf) disagree.\n",
    f"### Body\n\n{body}",
    "### Terms\n\n- [x] I read the deposit protocol at https://alexanarch.org/api/deposit-protocol.json\n- [x] I confirm this work is deposited under the stated license\n- [x] I confirm the substrate disclosure is accurate\n- [x] I understand that deposited content will NOT be used to train enforcement classifiers\n"])
out = ROOT / "data/issue-bodies/EA-CORPORA-38-issue.md"
out.write_text(issue, encoding="utf-8")
print(out, len(body.split()), "words in body;", len(desc), "chars in description;", tot, "lines;", nfiles, "files")
