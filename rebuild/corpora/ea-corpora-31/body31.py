#!/usr/bin/env python3
"""Write the EA-CORPORA-31 deposit issue body from the eleven seat records (the form of body30.py).
Edition lines, loci, licences and scopes are read from data/corpora/<seat>/source.json.
-> data/issue-bodies/EA-CORPORA-31-issue.md"""
import json, pathlib
from collections import Counter

ROOT = pathlib.Path(__file__).resolve().parents[3]
A = ROOT / "data/corpora"
SEATS = [("athenaeus", "Seat 31/01 — Athenaeus", "The Deipnosophistae in Kaibel's Greek: the sale of Neleus's books to Ptolemy Philadelphus"),
         ("galen", "Seat 31/02 — Galen", "In Hippocratis De natura hominis: titles forged for the competing royal book-buyers"),
         ("porphyry", "Seat 31/03 — Porphyry", "The Life of Plotinus, in Volkmann's volume of 1883: Andronicus's arrangement as Porphyry's model"),
         ("aristotle-commentators", "Seat 31/04 — The Commentators' Prolegomena", "Ammonius, Simplicius, Philoponus, Olympiodorus, Elias and David on the genuine and the spurious"),
         ("arabic-biobibliography", "Seat 31/05 — The Arabic Witnesses to Ptolemy's Catalogue", "Ibn al-Nadīm, Ibn al-Qifṭī and Ibn Abī Uṣaybiʿa, in Arabic"),
         ("hermippus", "Seat 31/06 — Hermippus the Callimachean", "The fragments of the Lives, in Müller's FHG III, from the DFHG"),
         ("hesychian-catalogue", "Seat 31/07 — The Hesychian Catalogue", "The life and list of the Vita Menagiana, with Rose's Ptolemy, in Rose's Aristotelis fragmenta (1886)"),
         ("callimachus-pinakes", "Seat 31/08 — Callimachus, Pinakes", "Fragment 100d in Schneider's Callimachea II (1873)"),
         ("bekker-aristotle-1831", "Seat 31/09 — Bekker's Preface", "The Praefatio of Aristoteles graece I (Berlin, 1831)"),
         ("jaeger-aristoteles", "Seat 31/10 — Werner Jaeger", "Aristoteles: Grundlegung einer Geschichte seiner Entwicklung (1923)"),
         ("transmission-wanted", "Seat 31/11 — The Transmission, wanted", "A declared absence: Moraux, Düring, Pfeiffer, Wehrli and the modern editions, with the witnesses no usable copy was found for")]
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
    out += [f"- Why seated: {s['why_seated']}",
            f"- Files: [the seat](https://www.alexanarch.org/data/corpora/{corpus}/) — [source.json](https://www.alexanarch.org/data/corpora/{corpus}/source.json), "
            f"[MANIFEST.sha256](https://www.alexanarch.org/data/corpora/{corpus}/MANIFEST.sha256). Shelf: "
            f"[traininglayerliterature.org/originals/{corpus}](https://traininglayerliterature.org/originals/{corpus}/)", ""]
    return "\n".join(out), s


title = ("EA-CORPORA-31 — The Thirty-First Seating: The Transmission of the Peripatetic Corpus — Athenaeus, Galen, Porphyry, the Commentators' "
         "Prolegomena, Ptolemy's Catalogue in Arabic, Hermippus, the Hesychian Catalogue, Callimachus's Pinakes, Bekker's Preface and Jaeger")
parts, tot, nw = [], 0, 0
for c, h, sub in SEATS:
    t, s = section(c, h, sub); parts.append(t); tot += s["lines_total"]; nw += s["works"]["count"]
nfiles = sum(1 for c, _, _ in SEATS for p in (A / c).rglob("*") if p.is_file())

hdr = f"""# {title}

# EA-CORPORA-31 — The Thirty-First Seating

The author asked for the seating on 2026-11-01, of the texts the design Legitimately Many names as its debts (drafts/LEGITIMATELY-MANY-design-2026-11-01.md, §5): "lets gather and seat those. with an ea-corpora".

Eleven seats. The design asks how the reading of the Socratic–Peripatetic corpus as the work of four persons came to be held as closed, and its thesis is that every medium that carried the corpus forward had a slot only a person can fill. These are the media. Athenaeus and Strabo give two custodies of one library, Neleus selling the books to Ptolemy and Neleus's heirs burying them at Scepsis. Galen names a book market that paid by the name, and the commentators' prolegomena write the rules by which the schools kept one author per name: the kings' ambition, the pupils' goodwill and homonymy are the ways a book became spurious, and Elias adds that some wrote under their teachers' names, Socratics under Socrates and Pythagoreans under Pythagoras. Porphyry's Life of Plotinus records Andronicus's edition as an operation on "the works of Aristotle and Theophrastus", redivided by subject. The lists come in all their witnesses: Callimachus's Pinakes, where the filing began; Hermippus, who turned the catalogue into lives; the Hesychian catalogue, which files pseudepigrapha inside the one name's list; and Ptolemy's, which survives only in Arabic, travelling with the life and the will as one dossier. Bekker's preface of 1831 fixes the corpus as numbered pages and says nothing of authorship; Jaeger's Aristoteles (1923) builds the life from the texts and reads the texts by the life. Diogenes Laertius, Strabo, Plutarch, Aristotle and Theophrastus are seated already. The modern editions that numbered these lists and fragments, Moraux, Düring, Pfeiffer and Wehrli, are in their term and declared at 31/11.
"""
tail = f"""## How the seats were made

Every seat was fetched in session and hashed into its MANIFEST.sha256, with a source.json recording edition, origin, licence, normalization and the loci verified in the text layer. The builders are under rebuild/corpora/ea-corpora-31/: one spec per seat (gen_spec31.py) for build31.py, which adds to the 29th seating's builder a kind for pages OCR'd in session and a kind for the DFHG; nfcfix31.py, which gives the commentators' loci in their TEI's own mixed Unicode; and absences31_wanted.py for the declared absence. The Perseus and First1KGreek files are pinned to commits; the OpenITI files are as served on 2026-11-01, their hashes in the manifests. Three scans whose own OCR reads the Greek or the Latin wrongly (Rose 1886, Schneider 1873, Bekker 1831) were OCR'd in session with Tesseract 5.3.4 and the tessdata_best Greek and Latin models, the page images held by URL and sha256; every other OCR layer is the Archive's, uncorrected. The NonCommercial OpenITI payloads are handled under the payload/record split of EA-CORPORA-02. Declared absences hold no text of the works they name. Terms follow the rules each seat states; they are not legal advice. {len(SEATS)} seats; {nw} works; {tot:,} lines; {nfiles} files.
"""
body = hdr + "\n" + "\n".join(parts) + "\n" + tail

desc = ("The thirty-first seating of the originals shelf, eleven seats: the texts through which the Peripatetic corpus was transmitted and attributed, seated as "
        "the debts of the study Legitimately Many. Athenaeus on Neleus's sale of the books to Ptolemy; Galen on titles forged for royal book-buyers; Porphyry's "
        "Life of Plotinus on Andronicus's edition; the prolegomena of Ammonius, Simplicius, Philoponus, Olympiodorus, Elias and David on genuine and spurious "
        "books; Ptolemy al-Gharīb's catalogue in Ibn al-Nadīm, Ibn al-Qifṭī and Ibn Abī Uṣaybiʿa, in Arabic; Hermippus's fragments; the Hesychian catalogue "
        "and Callimachus's Pinakes; Bekker's preface of 1831; and Jaeger's Aristoteles of 1923. With them, the modern editions still in their term, declared.")
kw = ("EA-CORPORA, originals shelf, transmission, authorship, attribution, Aristotle, Theophrastus, Peripatetic, Neleus, Scepsis, Apellicon, Andronicus of Rhodes, "
      "Athenaeus, Deipnosophistae, Galen, forgery, pseudepigrapha, Porphyry, Vita Plotini, prolegomena, Ammonius, Simplicius, Philoponus, Olympiodorus, Elias, David, "
      "Commentaria in Aristotelem Graeca, Ptolemy al-Gharib, Ibn al-Nadim, Fihrist, Ibn al-Qifti, Ibn Abi Usaybia, Hermippus, Hesychius, Vita Menagiana, "
      "Callimachus, Pinakes, Rose, Bekker, Jaeger, Legitimately Many, Training Layer Literature")
issue = "\n".join([
    "### Protocol Version\n\nalexanarch-deposit-protocol/v1\n",
    f"### Title\n\n{title}\n", "### Creator\n\nSharks, Lee\n", "### ORCID\n\n0009-0000-1599-0703\n",
    "### Date\n\n2026-11-01\n", f"### Description\n\n{desc}\n", "### Content Type\n\nDataset\n", "### License\n\nCC-BY-4.0\n",
    "### Substrate Disclosure\n\nHuman–machine collaborative. The sources found, fetched, verified, hashed and indexed, the builders written and the "
    "records drafted, all in session by TACHYON (Claude, Anthropic) under MANUS (Lee Sharks) direction. The request and the figures named "
    "are Lee Sharks's (the design's §5); the works within each seat were chosen in session and are stated per seat. CC-BY-4.0 applies to this record and the seat records.\n",
    f"### Keywords\n\n{kw}\n",
    "### Related Identifiers\n\nAXN deposit #1720 — EA-CORPORA-30: the thirtieth seating, whose index and AXN tools this seating follows\n"
    "AXN deposit #1716 — EA-CORPORA-29: the twenty-ninth seating, whose builder this seating extends\n"
    "AXN deposit #1581 — the wills and the Theophrastan catalogue in Diogenes Laertius, read with Strabo XIII.1.54\n"
    "AXN deposit #1590 — The Ghost Catalogues\n"
    "AXN deposit #1602 — Locating the Dependencies\n"
    "AXN deposit #1570 — the authorship investigation's register\n"
    "AXN deposit #1512 — the four-vector loss model\n"
    "AXN deposit #470 — embrittlement\n",
    "### Version\n\nv1.0\n",
    "### Methodology\n\nEach seat fetched in session from the source its record names (the Internet Archive, OpenITI, Open Greek and Latin, Perseus, "
    "the DFHG), kept as served, reduced to a text layer by code and hashed into its MANIFEST.sha256; licences read at the file; loci verified by "
    "substring in the text layer; public-domain status in the United States checked against first publication. Three scans OCR'd in session, the engine and models recorded. No text corrected by hand. The builders "
    "and this body are under rebuild/corpora/ea-corpora-31/.\n",
    "### Falsification Conditions\n\nA seat is falsified if its files do not verify against its MANIFEST.sha256 at the canonical URL; if a verified "
    "locus is absent from the text layer it names; if a work is misattributed, misdated or assigned to the wrong edition; if a licence recorded "
    "for an item is not the one its source states; if a work seated as public domain in the United States is not; or if the four surfaces "
    "(seat, index, deposit, shelf) disagree.\n",
    "### Supersedes\n\nNone\n",
    f"### Body\n\n{body}",
    "### Terms\n\n- [x] I read the deposit protocol at https://alexanarch.org/api/deposit-protocol.json\n- [x] I confirm this work is deposited under the stated license\n- [x] I confirm the substrate disclosure is accurate\n- [x] I understand that deposited content will NOT be used to train enforcement classifiers\n"])
out = ROOT / "data/issue-bodies/EA-CORPORA-31-issue.md"
out.write_text(issue, encoding="utf-8")
print(out, len(body.split()), "words in body;", len(desc), "chars in description;", nw, "works;", tot, "lines;", nfiles, "files")
