#!/usr/bin/env python3
"""Write the EA-CORPORA-42 deposit issue body from the ten seat records (the form of body41.py).
Edition lines, loci, licences and scopes are read from <seats>/<seat>/source.json (default data/corpora).
    python3 rebuild/corpora/ea-corpora-42/body42.py [seats-dir]
-> data/issue-bodies/EA-CORPORA-42-issue.md"""
import json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from names42 import SEATS
A = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "data/corpora"
SUB = {
 "plutarch-platonic-questions-de-facie-numa": "Plato's repentance, the central fire, and Aristarchus charged with impiety",
 "pseudo-plutarch-placita": "The doxography Copernicus quoted",
 "cicero-lucullus": "Hicetas, as Theophrastus says",
 "archimedes-arenarius": "Aristarchus's hypotheses",
 "simplicius-in-de-caelo": "Heraclides saves the phenomena",
 "diels-doxographi-graeci": "Aëtius, with Stobaeus: Aristarchus the hearer of Strato",
 "aquinas-in-de-caelo": "The school commentary holding the centre",
 "copernicus-de-revolutionibus": "Cicero first, Plutarch after",
 "bacon-novum-organum": "Blaming the name",
 "galileo-dialogo": "Aristotle against the Peripatetics",
}
lic = lambda l: l["payload"] if isinstance(l, dict) else str(l)


def research(r):
    if isinstance(r, dict):
        return "; ".join(f"{k.replace('_', ' ')}: {v}" for k, v in r.items())
    return str(r)


def section(n, corpus, title):
    s = json.loads((A / corpus / "source.json").read_text(encoding="utf-8"))
    w = s["works"]["list"]
    out = [f"## Seat 42/{n:02d} — {title.replace(' — ', ', ', 1)}", "", f"*{SUB[corpus]}*", ""]
    out += ["- Works:"] + [f"  - {x.get('title') or x.get('work')}" for x in w]
    out += [f"- Licence: {lic(s['license'])}"] + [f"- Verified locus: {v}" for v in s["verified_loci"]]
    out += [f"- Locus not found: {v}" for v in s.get("loci_not_found") or []]
    nt = sum(1 for x in w if x.get("text"))
    out += [f"- Lines: {s['lines_total']:,} in {nt} text file{'s' if nt != 1 else ''}",
            f"- Normalization: {s['normalization']}", f"- Scope: {s['scope']}",
            f"- Research: {research(s['research'])}", f"- Why seated: {s['why_seated']}"]
    for k in ("held_out", "duplicate_not_seated"):
        if s.get(k):
            out.append(f"- {k.replace('_', ' ').capitalize()}: {s[k]}")
    out += [f"- Files: [the seat](https://www.alexanarch.org/data/corpora/{corpus}/) — [source.json](https://www.alexanarch.org/data/corpora/{corpus}/source.json), "
            f"[MANIFEST.sha256](https://www.alexanarch.org/data/corpora/{corpus}/MANIFEST.sha256). Shelf: "
            f"[traininglayerliterature.org/originals/{corpus}](https://traininglayerliterature.org/originals/{corpus}/)", ""]
    return "\n".join(out), s


title = ("EA-CORPORA-42 — The Forty-Second Seating: Contra Geocentrism — Plutarch's Platonic Questions, De facie and Numa, the Placita, "
         "Cicero's Lucullus, Archimedes's Sand-Reckoner, Simplicius and Aquinas on De caelo, Diels's Doxographi, Copernicus, Bacon and Galileo")
parts, tot = [], 0
for n, (c, _, t) in enumerate(SEATS, 1):
    x, s = section(n, c, t); parts.append(x); tot += s["lines_total"]
nfiles = sum(1 for c, _, _ in SEATS for p in (A / c).rglob("*") if p.is_file())

hdr = f"""# {title}

# EA-CORPORA-42 — The Forty-Second Seating

The author asked for the gathering on 2026-11-22. At 00:04, to the offer to seat the Academica and the Plutarch the study had read in Perseus: "yup. lers write it up. the socratic-peripatetic corpus contra geocentrism". At 00:33: "rebekah cranes gets ea corpora deposits. lets expand the scope there, deposit, and close debts on the contea geocentrism so that were ready to deposit when the ea corpora lands". The study is Contra Geocentrism: The Socratic–Peripatetic Corpus Against Its Own Conversion (draft, not deposited): the corpus under the names of Aristotle and Theophrastus states the resting central earth in De caelo II 14 and carries the case against it in II 13, in the Metaphysics and in its reports; the reports reach Copernicus by way of Cicero and the Placita. The seating holds the texts the study reads that the shelf did not already hold, in the language each was written in.

The reports (42/01–42/03): Plutarch's Platonic Questions 8.1, where Theophrastus reports Plato's repentance of the central earth, with Numa 11 and De facie 923A, where Cleanthes would indict Aristarchus for moving the hearth of the cosmos; the Placita, whose III 13 Copernicus copies in Greek; Cicero's Lucullus 123, Hicetas ut ait Theophrastus. Aristarchus and the school (42/04–42/06): the Sand-Reckoner; Simplicius on De caelo, Heraclides saving the phenomena; Diels's Doxographi Graeci, with Aëtius I 15 giving Aristarchus as the hearer of Strato. The commentary and the turn (42/07–42/10): Aquinas on De caelo, the school commentary that concedes the astronomers' suppositions need not be true and holds the centre; Copernicus's dedication, Cicero first and Plutarch after; Bacon's Novum Organum I.63, the charge laid on the name; Galileo's Dialogo, Aristotle set against the Peripatetics.

Already seated and not reseated: Aristotle, De caelo among the corpus (EA-CORPORA-04/01, #1559); Theophrastus, the Metaphysics in First1KGreek (Wimmer, Teubner 1862; 09/01) and in Wimmer's Didot of 1866 (32/03, #1731); Plato, the Timaeus among the corpus (01/08, #1522); Cicero's Academica posteriora (13/03, #1591); Simplicius on the Physics (41/11, #1792); Diogenes Laertius (12/01, #1580).

## Pointers to the rest

Declared and not pursued, or held for a later seating, with what is known of each:

- Nicole Oresme, Le Livre du ciel et du monde (1377), II.25: the edition (Menut and Denomy, 1968) is in copyright; no open text found.
- John Buridan, Quaestiones super libris quattuor De caelo et mundo, II q. 22: the edition (Moody, 1942) not found open.
- Theophrastus, Metaphysics, ed. Ross and Fobes (Oxford, 1929): public domain in the United States, no open copy found (the Internet Archive holds a 1967 reprint for lending); Gutas (2010) is paywalled.
- Bertrand Russell, A History of Western Philosophy (1945): in copyright.
- Peter Ramus, Aristotelicae animadversiones (1543); the 1536 thesis is reported, its historicity doubted: for a later seating.
- Copernicus, De revolutionibus II–VI: not transcribed at Wikisource; for a later seating.
- Modern studies: Tupikova, "Cosmology and Epistemology" (Edition Open Access, 2016), open and cited in the study; Meister, Theophrastus on First Principles (Cambridge Elements, 2026), paywalled, declared.
"""
tail = f"""## How the seats were made

Every seat was fetched in session from the source its record names (the Perseus Digital Library's canonical-greekLit and canonical-latinLit TEI and the First1KGreek TEI at GitHub; the Internet Archive for Diels; the Corpus Thomisticum for Aquinas; Latin and Italian Wikisource for Copernicus, Bacon and Galileo) and hashed into its MANIFEST.sha256, with a source.json recording edition, origin, licence, normalization, the loci verified in the text, and the research the seat was made for. The TEI files are held under original/ as fetched; under text/, a reading text reduced from each, with the TEI's own book, chapter and section numbers kept as markers, speakers marked [speaker], and numbered verse lines marked |N. The HTML pages are held as served under original/, with a text reduced from each by code; Diels's OCR layer is held as served. Loci are verified by substring, with whitespace collapsed, in the editions' own readings. No text corrected by hand. The builders are under rebuild/corpora/ea-corpora-42/ (prepare_texts42.py, build_seats42.py, index42.py, seat_axns42.py, and body42.py, which writes this body); NOTE.md records the order.

In all: ten seats, {nfiles:,} files, {tot:,} lines of text.
"""
body = hdr + "\n" + "\n".join(parts) + "\n" + tail
desc = ("The forty-second seating of the originals shelf, ten seats, gathered for the study Contra Geocentrism (2026-11-22). Plutarch's Platonic Questions, De facie and Numa; "
        "the Placita of Pseudo-Plutarch; Cicero's Lucullus; Archimedes's Sand-Reckoner; Simplicius on De caelo; Diels's Doxographi Graeci; Aquinas on De caelo; "
        "Copernicus's prefaces and Book I; Bacon's Novum Organum; Galileo's Dialogo. Each in the language it was written in. Pointers to what is not seated, Oresme and Buridan first.")
kw = ("EA-CORPORA, originals shelf, geocentrism, De caelo, Aristotle, Theophrastus, Plato, Timaeus, Plutarch, Platonic Questions, De facie, Numa, Placita, Aëtius, "
      "Diels, Doxographi Graeci, Cicero, Lucullus, Hicetas, Heraclides of Pontus, Ecphantus, Philolaus, Aristarchus, Archimedes, Sand-Reckoner, Simplicius, "
      "Thomas Aquinas, Copernicus, De revolutionibus, Francis Bacon, Novum Organum, Galileo, Dialogo, Cleanthes, impiety, Perseus Digital Library, First1KGreek, Wikisource")
related = "\n".join([
    "AXN deposit #1792 — EA-CORPORA-41: the forty-first seating",
    "AXN deposit #1559 — EA-CORPORA-04: Aristotle undivided",
    "AXN deposit #1591 — EA-CORPORA-13: the Alexander seam, with Cicero's De finibus and Academica",
    "AXN deposit #1731 — EA-CORPORA-32: the Wimmer Theophrastus",
    "AXN deposit #1575 — Many and One",
    "AXN deposit #1794 — The Thinkery and the Lyceum"]) + "\n"
issue = "\n".join([
    "### Protocol Version\n\nalexanarch-deposit-protocol/v1\n",
    f"### Title\n\n{title}\n", "### Creator\n\nCranes, Rebekah\n", "### ORCID\n\n0009-0000-1599-0703\n",
    "### Date\n\n2026-11-22\n", f"### Description\n\n{desc}\n", "### Content Type\n\nDataset\n", "### License\n\nCC-BY-4.0\n",
    "### Substrate Disclosure\n\nHuman–machine collaborative. Rebekah Cranes is a heteronym of Lee Sharks, the standing authority on the EA-CORPORA deposits (named by the author on 2026-11-04 and held at his word of 2026-11-05). The sources found, fetched, reduced to reading texts, verified, hashed and indexed, and the records drafted, in session by TACHYON (Claude, Anthropic) under MANUS (Lee Sharks) direction. The gathering, its object and its scope are Lee Sharks's (the study Contra Geocentrism); the editions within each seat were chosen in session and are stated per seat. CC-BY-4.0 applies to this record and the seat records.\n",
    f"### Keywords\n\n{kw}\n", f"### Related Identifiers\n\n{related}", "### Version\n\nv1.0\n",
    "### Methodology\n\nEach seat fetched in session from the source its record names (Perseus canonical-greekLit and canonical-latinLit and First1KGreek at GitHub; the Internet Archive; the Corpus Thomisticum; Latin and Italian Wikisource); the TEI held as fetched and reduced to a reading text keeping the edition's own reference markers; licences read in each file's teiHeader or the serving site's statement; loci verified by substring with whitespace collapsed, in the editions' own readings; public-domain status checked against the underlying edition. No text corrected by hand. The builders and this body are under rebuild/corpora/ea-corpora-42/.\n",
    "### Falsification Conditions\n\nA seat is falsified if its files do not verify against its MANIFEST.sha256 at the canonical URL; if a verified locus is absent from the text it names; if a work is misattributed or assigned to the wrong edition; if a licence recorded for an item is not the one its source states; if a reading text drops or alters a line of the TEI it is reduced from, beyond the markup; or if the four surfaces (seat, index, deposit, shelf) disagree.\n",
    f"### Body\n\n{body}",
    "### Terms\n\n- [x] I read the deposit protocol at https://alexanarch.org/api/deposit-protocol.json\n- [x] I confirm this work is deposited under the stated license\n- [x] I confirm the substrate disclosure is accurate\n- [x] I understand that deposited content will NOT be used to train enforcement classifiers\n"])
out = ROOT / "data/issue-bodies/EA-CORPORA-42-issue.md"
out.write_text(issue, encoding="utf-8")
print(out, len(body.split()), "words in body;", len(desc), "chars in description;", tot, "lines;", nfiles, "files")
