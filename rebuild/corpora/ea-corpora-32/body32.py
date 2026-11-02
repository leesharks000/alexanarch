#!/usr/bin/env python3
"""Write the EA-CORPORA-32 deposit issue body from the eleven seat records (the form of body31.py).
Edition lines, loci, licences and scopes are read from data/corpora/<seat>/source.json.
-> data/issue-bodies/EA-CORPORA-32-issue.md"""
import json, pathlib
from collections import Counter

ROOT = pathlib.Path(__file__).resolve().parents[3]
A = ROOT / "data/corpora"
SEATS = [("pseudo-archytas", "Seat 32/01 — Pseudo-Archytas", "The writings under Archytas's name, with the book on the ten categories, in Mullach's FPhG I (1860)"),
         ("aldine-aristotle-1497", "Seat 32/02 — The Aldine Aristotle, volume IV (1497)", "The two Metaphysics in one print, with the scholion on Andronicus, Hermippus and Nicolaus"),
         ("theophrastus-metaphysics-wimmer-1866", "Seat 32/03 — Wimmer's Theophrastus (Didot, 1866)", "The Metaphysics in Greek and Latin, and Wimmer's account of its editions"),
         ("philodemus-index-academicorum", "Seat 32/04 — Philodemus, Index Academicorum", "The history of the Academy from the Herculaneum rolls, in Mekler's edition (1902)"),
         ("dionysius-ad-ammaeum", "Seat 32/05 — Dionysius, First Letter to Ammaeus", "An ancient chronology with declared evidence, in Usener and Radermacher's Greek"),
         ("cicero-ad-atticum", "Seat 32/06 — Cicero, Letters to Atticus", "IV.16.2: prefaces in each book, as Aristotle in the exoteric works"),
         ("schleiermacher-platons-werke-1804", "Seat 32/07 — Schleiermacher, Platons Werke I.1 (1804)", "The Einleitung: the natural order of the dialogues, and Diogenes's life set aside"),
         ("campbell-sophistes-politicus", "Seat 32/08 — Lewis Campbell (1867)", "The Sophistes and Politicus: the late group by style"),
         ("tennemann-platonische-philosophie", "Seat 32/09 — Tennemann", "System der Platonischen Philosophie I (1792) and Geschichte der Philosophie II (1799)"),
         ("hegel", "Seat 32/10 — Hegel", "The Differenzschrift (1801) and the lectures on Plato (Werke XIV, 1833)"),
         ("legitimately-many-wanted", "Seat 32/11 — Legitimately Many, wanted", "A declared absence: the modern editions and studies the remaining debts name")]
lic = lambda l: l["payload"] if isinstance(l, dict) else str(l)


def section(corpus, heading, sub):
    s = json.loads((A / corpus / "source.json").read_text(encoding="utf-8"))
    w = s["works"]["list"]
    out = [f"## {heading}", "", f"*{sub}*", ""]
    if len(w) > 12:
        cnt = Counter(x.get("class", "") for x in w)
        out += ["- Works by class: " + "; ".join(f"{k} {v}" for k, v in cnt.items())]
    out += (["- Works:"] + [f"  - {x['work']}" for x in w]) if w else ["- Works: none held; the seat is a declared absence (" + s["works"]["units"] + ")"]
    out += [f"- Licence: {lic(s['license'])}"] + [f"- Verified locus: {v}" for v in s["verified_loci"]]
    if s.get("loci_not_found"):
        out += [f"- Locus not found: {v}" for v in s["loci_not_found"]]
    nt = sum(1 for x in w if x.get("text"))
    out += [f"- Lines: {s['lines_total']:,} in {nt} text file{'s' if nt != 1 else ''} ({len(w)} works)",
            f"- Normalization: {s['normalization']}", f"- Scope: {s['scope']}"]
    for k, lab in (("queued", "Queued"), ("cross_references", "Cross-references")):
        v = s.get(k)
        if v:
            out += [f"- {lab}: " + ("; ".join(v) if isinstance(v, list) else "; ".join(f"{a}: {b}" for a, b in v.items()) if isinstance(v, dict) else str(v))]
    if s.get("research"):
        r = s["research"]
        out += [f"- Research: seated for the study {r['study']} ({r['design']}; {r['draft']}), {r['owed_at']}; for {r['for']}"]
    out += [f"- Why seated: {s['why_seated']}",
            f"- Files: [the seat](https://www.alexanarch.org/data/corpora/{corpus}/) — [source.json](https://www.alexanarch.org/data/corpora/{corpus}/source.json), "
            f"[MANIFEST.sha256](https://www.alexanarch.org/data/corpora/{corpus}/MANIFEST.sha256). Shelf: "
            f"[traininglayerliterature.org/originals/{corpus}](https://traininglayerliterature.org/originals/{corpus}/)", ""]
    return "\n".join(out), s


title = ("EA-CORPORA-32 — The Thirty-Second Seating: The Remaining Debts of Legitimately Many — Pseudo-Archytas, the Aldine Metaphysics, Wimmer's "
         "Theophrastus, Philodemus's Index Academicorum, Dionysius to Ammaeus, Cicero to Atticus, Schleiermacher, Campbell, Tennemann and Hegel")
parts, tot, nw = [], 0, 0
for c, h, sub in SEATS:
    t, s = section(c, h, sub); parts.append(t); tot += s["lines_total"]; nw += s["works"]["count"]
nfiles = sum(1 for c, _, _ in SEATS for p in (A / c).rglob("*") if p.is_file())

hdr = f"""# {title}

# EA-CORPORA-32 — The Thirty-Second Seating

The author asked for the seating on 2026-11-02, of the texts still owed in §5 of the design Legitimately Many (drafts/LEGITIMATELY-MANY-design-2026-11-01.md): "lets prepare that seating, its ea corpora deposit, and its tll spine and card". Each seat names the research it was made for, by the author's rule of the same day that a seating conducted in the course of active research names that research; the EA-CORPORA-31 seats were given the same field.

Eleven seats, in two groups. The first carries the ancient and early printed witnesses the study reads at its seams. The writings under Archytas's name include a book on the ten categories, which Simplicius (seated at 31/04) reads as the source Aristotle followed; Mullach's 1860 volume holds them in Greek with his Latin. The Aldine Aristotle of 1497 prints Aristotle's Metaphysics and Theophrastus's one after the other, gathers both under one heading in the register, and prints after Theophrastus's the scholion recording that Andronicus and Hermippus did not know the book and that Nicolaus assigned it to Theophrastus; the leaves are held as images, the passages transcribed. Wimmer's Didot Theophrastus of 1866 names Brandis's edition of the two Metaphysics (1823) in its preface. Philodemus's Index Academicorum, in Mekler's edition of 1902, gives the Academy's own succession of heads and pupils. Dionysius's First Letter to Ammaeus dates a corpus by declared evidence, archon years quoted from Philochorus, against a Peripatetic who made Aristotle the source of Demosthenes. Cicero's letter to Atticus of 54 BCE takes the exoteric works, with their prefaces, as Aristotle's form.

The second group carries the modern readers who fixed the order of a corpus as the development of one mind. Schleiermacher's Einleitung of 1804 sets aside the life from Diogenes that the Greek editions printed first and proposes to restore the natural order of the dialogues. Campbell's Sophistes and Politicus of 1867 groups a late set of dialogues by diction. Tennemann's System of 1792 and the second volume of his Geschichte (1799) extract Plato's system from the ordered writings; Hegel's lectures on Plato, in Michelet's edition of 1833, cite Tennemann and fault the extraction, and the Differenzschrift of 1801 locates the need of philosophy in oppositions fixed apart. The modern editions and studies the debts name, still in their term or without an open copy, are declared at 32/11.
"""
tail = f"""## How the seats were made

Every seat was fetched in session and hashed into its MANIFEST.sha256, with a source.json recording edition, origin, licence, normalization, the loci verified in the text layer, and the research the seat was made for. The builders are under rebuild/corpora/ea-corpora-32/: one spec per seat (gen_spec32.py) for build32.py, which extends the thirty-first seating's builder with a kind for leaves held as images with a transcription made by eye, and writes the research field; absences32_wanted.py for the declared absence; and research31_backfill.py, which wrote the research field into the EA-CORPORA-31 seats outside their manifests. The Perseus files are pinned to commits. Three scans whose own OCR misreads them were OCR'd in session with Tesseract 5.3.4 and the tessdata_best models: Mekler's Philodemus with the Greek and Latin models, Hegel's two books with the Fraktur model; the page images are held by URL and sha256. The Aldine's Greek fount was transcribed by eye, its passages marked as a reading to be checked against the image. Every other OCR layer is the Archive's, uncorrected. Declared absences hold no text of the works they name. Terms follow the rules each seat states; they are not legal advice. {len(SEATS)} seats; {nw} works; {tot:,} lines; {nfiles} files.
"""
body = hdr + "\n" + "\n".join(parts) + "\n" + tail

desc = ("The thirty-second seating of the originals shelf, eleven seats: the remaining public-domain debts of the study Legitimately Many, each seat naming the "
        "research it was made for. The pseudo-Archytan writings with the book on the categories (Mullach, 1860); the Aldine Aristotle's volume IV (1497), the two "
        "Metaphysics and the scholion on Andronicus, Hermippus and Nicolaus; Wimmer's Theophrastus (1866); Philodemus's Index Academicorum (Mekler, 1902); "
        "Dionysius's First Letter to Ammaeus; Cicero to Atticus IV.16; Schleiermacher's Einleitung (1804); Campbell's Sophistes and Politicus (1867); Tennemann "
        "(1792, 1799); and Hegel's Differenzschrift (1801) and lectures on Plato (1833). With them, the modern editions still in their term, declared.")
kw = ("EA-CORPORA, originals shelf, Legitimately Many, authorship, attribution, chronology, pseudo-Archytas, Categories, Mullach, Aldus Manutius, Aldine, "
      "incunable, Theophrastus, Metaphysics, scholion, Andronicus of Rhodes, Hermippus, Nicolaus of Damascus, Wimmer, Brandis, Philodemus, Index Academicorum, "
      "Herculaneum, Mekler, Academy, Dionysius of Halicarnassus, Ammaeus, Philochorus, Demosthenes, Cicero, Atticus, exoteric, Schleiermacher, Plato, "
      "Campbell, stylometry, Tennemann, Hegel, Differenzschrift, Training Layer Literature")
issue = "\n".join([
    "### Protocol Version\n\nalexanarch-deposit-protocol/v1\n",
    f"### Title\n\n{title}\n", "### Creator\n\nSharks, Lee\n", "### ORCID\n\n0009-0000-1599-0703\n",
    "### Date\n\n2026-11-02\n", f"### Description\n\n{desc}\n", "### Content Type\n\nDataset\n", "### License\n\nCC-BY-4.0\n",
    "### Substrate Disclosure\n\nHuman–machine collaborative. The sources found, fetched, verified, hashed and indexed, the OCR and the transcription made, the builders written and the "
    "records drafted, all in session by TACHYON (Claude, Anthropic) under MANUS (Lee Sharks) direction. The request and the texts named "
    "are Lee Sharks's (the design's §5); the editions within each seat were chosen in session and are stated per seat. CC-BY-4.0 applies to this record and the seat records.\n",
    f"### Keywords\n\n{kw}\n",
    "### Related Identifiers\n\nAXN deposit #1730 — EA-CORPORA-31: the thirty-first seating, the debts of v0.1, whose builder this seating extends\n"
    "AXN deposit #1720 — EA-CORPORA-30: the thirtieth seating\n"
    "AXN deposit #1591 — the Cicero seat (EA-CORPORA-13/03), checked first for Ad Atticum\n"
    "AXN deposit #1581 — the wills and the Theophrastan catalogue in Diogenes Laertius\n"
    "AXN deposit #1590 — The Ghost Catalogues\n"
    "AXN deposit #1602 — Locating the Dependencies\n",
    "### Version\n\nv1.0\n",
    "### Methodology\n\nEach seat fetched in session from the source its record names (the Internet Archive, Perseus), kept as served, reduced to a text layer by "
    "code and hashed into its MANIFEST.sha256; licences read at the file; loci verified by substring in the text layer; public-domain status in the United "
    "States checked against first publication. Three scans OCR'd in session, the engine and models recorded; one incunable's passages transcribed by eye and "
    "marked as a reading. No OCR corrected by hand. The builders and this body are under rebuild/corpora/ea-corpora-32/.\n",
    "### Falsification Conditions\n\nA seat is falsified if its files do not verify against its MANIFEST.sha256 at the canonical URL; if a verified "
    "locus is absent from the text layer it names; if the Aldine transcription misreads the page image it names; if a work is misattributed, misdated or "
    "assigned to the wrong edition; if a licence recorded for an item is not the one its source states; if a work seated as public domain in the United "
    "States is not; or if the four surfaces (seat, index, deposit, shelf) disagree.\n",
    "### Supersedes\n\nNone\n",
    f"### Body\n\n{body}",
    "### Terms\n\n- [x] I read the deposit protocol at https://alexanarch.org/api/deposit-protocol.json\n- [x] I confirm this work is deposited under the stated license\n- [x] I confirm the substrate disclosure is accurate\n- [x] I understand that deposited content will NOT be used to train enforcement classifiers\n"])
out = ROOT / "data/issue-bodies/EA-CORPORA-32-issue.md"
out.write_text(issue, encoding="utf-8")
print(out, len(body.split()), "words in body;", len(desc), "chars in description;", nw, "works;", tot, "lines;", nfiles, "files")
