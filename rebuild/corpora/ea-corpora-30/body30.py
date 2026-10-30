#!/usr/bin/env python3
"""Write the EA-CORPORA-30 deposit issue body from the twelve seat records (the form of body29.py).
Edition lines, loci, licences and scopes are read from data/corpora/<seat>/source.json.
-> data/issue-bodies/EA-CORPORA-30-issue.md"""
import json, pathlib
from collections import Counter

ROOT = pathlib.Path(__file__).resolve().parents[3]
A = ROOT / "data/corpora"
SEATS = [("einstein", "Seat 30/01 — Albert Einstein", "The 1905 papers, the 1915 field equations, the 1916 foundation, the 1917 cosmology and the popular exposition, in the Annalen and the Academy's volumes"),
         ("goedel", "Seat 30/02 — Kurt Gödel", "The Königsberg abstract of 1930, in Naturwissenschaften; the completeness paper wanted, the incompleteness paper opening 2027"),
         ("tesla", "Seat 30/03 — Nikola Tesla", "My Inventions, the lectures of 1891–1893, The Problem of Increasing Human Energy and the canonical patents"),
         ("copernicus", "Seat 30/04 — Nicolaus Copernicus", "De revolutionibus orbium coelestium, Nuremberg, 1543"),
         ("galileo", "Seat 30/05 — Galileo Galilei", "Sidereus nuncius, Il Saggiatore, the Dialogo, the Discorsi and the letter to Christina, in their first printings and in Favaro"),
         ("kepler", "Seat 30/06 — Johannes Kepler", "Mysterium cosmographicum, Astronomia nova and Harmonices mundi"),
         ("newton", "Seat 30/07 — Isaac Newton", "The Principia of 1687 and the Opticks of 1704"),
         ("arabic-mathematics", "Seat 30/08 — Classical Arabic Mathematics", "al-Khwārizmī, al-Kindī, Thābit ibn Qurra, Ibn al-Haytham, al-Bīrūnī and ʿUmar al-Khayyām, in Arabic"),
         ("paul-klee", "Seat 30/09 — Paul Klee", "The Pädagogisches Skizzenbuch of 1925 and the Schöpferische Konfession of 1920: the seat the twenty-eighth seating promised"),
         ("quantum-founders", "Seat 30/10 — The Founders of Quantum Mechanics", "Heisenberg, Born and Jordan, Pauli, Schrödinger, Dirac and Bohr, 1925–1928"),
         ("archimedes-ptolemy", "Seat 30/11 — Archimedes and Ptolemy", "Archimedes and the Syntaxis in Heiberg's Greek"),
         ("exact-wanted", "Seat 30/12 — The Exact Sciences, wanted", "A declared absence: Gödel 1931, the Königsberg discussion, Turing, EPR and the Tetrabiblos as they open, with the witnesses no copy was found for")]
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


title = ("EA-CORPORA-30 — The Thirtieth Seating: The Exact Sciences — Einstein, Gödel, Tesla, Copernicus, Galileo, Kepler, Newton, "
         "Classical Arabic Mathematics, the Founders of Quantum Mechanics, Archimedes and Ptolemy — and Klee's Bauhaus Notebook")
parts, tot, nw = [], 0, 0
for c, h, sub in SEATS:
    t, s = section(c, h, sub); parts.append(t); tot += s["lines_total"]; nw += s["works"]["count"]
nfiles = sum(1 for c, _, _ in SEATS for p in (A / c).rglob("*") if p.is_file())

hdr = f"""# {title}

# EA-CORPORA-30 — The Thirtieth Seating

The author asked for the seating on 2026-10-30: "and then an ea-corpora seating... Einstein, Gödel, Tesla, Copernicus, Galileo, classical Arabic mathematicians... what is in the public domain, and what else? and just to be perverse lets seat the promised Klee notebooks with them". To the twelve seats proposed he answered: "yes, thats a good set".

Twelve seats. The exact sciences come in their original languages and, where a copy could be found, in their first printings: Archimedes and the Syntaxis in Heiberg's Greek; al-Khwārizmī's Algebra, Thābit, Ibn al-Haytham's Optics, al-Bīrūnī and Khayyām in Arabic; De revolutionibus of 1543; Galileo's Sidereus nuncius, Dialogo and Discorsi; Kepler's three books of the world's harmony and motion; the Principia of 1687 and the Opticks of 1704; Tesla's lectures, patents and My Inventions; Einstein's papers in the Annalen and the Academy's Sitzungsberichte, as their issues and volumes printed them; the founders of quantum mechanics, 1925–1928; and Gödel, of whom the United States term leaves this seating only the Königsberg abstract of 1930, since the incompleteness paper opens on 2027-01-01. "What else" is answered in 30/12, the wanted list, which names each work still held by its term or not yet found, and when each opens. And Klee, declared wanted in the twenty-eighth seating (28/06), is seated with them: the Pädagogisches Skizzenbuch in the Bauhausbücher printing of 1925, its drawings in the book he made of them, and the Schöpferische Konfession of 1920 in the volume that first printed it. Seated beside Euclid (20/04), the line that walks for its own sake stands next to the line defined as breadthless length.
"""
tail = f"""## How the seats were made

Every seat was fetched in session and hashed into its MANIFEST.sha256, with a source.json recording edition, origin, licence, normalization and the loci verified in the text layer. The builders are under rebuild/corpora/ea-corpora-30/: one spec per seat for the 29th seating's build29.py, openiti30.py for the OpenITI mARkdown files, merge_klee.py for the promised Klee seat, and absences30_wanted.py for the declared absence. Internet Archive scans over about 60 MB are held by reference, with the Archive's md5; the OCR text layers are the Archive's, uncorrected. Wikisource pages are kept as served, with their revision ids. The NonCommercial OpenITI payloads are handled under the payload/record split of EA-CORPORA-02. Hosts that refused the seating's agent are named in the seats' scopes; the agent was not changed. Declared absences hold no text of the works they name. Terms follow the rules each seat states; they are not legal advice. {len(SEATS)} seats; {nw} works; {tot:,} lines; {nfiles} files.
"""
body = hdr + "\n" + "\n".join(parts) + "\n" + tail

desc = ("The thirtieth seating of the originals shelf, twelve seats: the exact sciences in their original languages and first printings. "
        "Einstein's papers of 1905–1917 in the Annalen and the Sitzungsberichte; Gödel's Königsberg abstract of 1930; Tesla's lectures, patents and My Inventions; "
        "De revolutionibus (1543); Galileo's Sidereus nuncius, Saggiatore, Dialogo and Discorsi; Kepler's Mysterium, Astronomia nova and Harmonices mundi; "
        "Newton's Principia (1687) and Opticks (1704); al-Khwārizmī, al-Kindī, Thābit ibn Qurra, Ibn al-Haytham, al-Bīrūnī and Khayyām in Arabic; "
        "Heisenberg, Born, Jordan, Pauli, Schrödinger, Dirac and Bohr, 1925–1928; Archimedes and Ptolemy in Heiberg's Greek. With them, the Klee seat "
        "the twenty-eighth seating promised: the Pädagogisches Skizzenbuch (1925) and the Schöpferische Konfession (1920). And the exact sciences still wanted, "
        "Gödel 1931 first among them, with their opening dates.")
kw = ("EA-CORPORA, originals shelf, exact sciences, history of science, Einstein, relativity, Annalen der Physik, Gödel, completeness, incompleteness, Tesla, "
      "Copernicus, De revolutionibus, Galileo, Sidereus nuncius, Dialogo, Kepler, Astronomia nova, Harmonices mundi, Newton, Principia, Opticks, al-Khwārizmī, "
      "algebra, al-Kindī, Thābit ibn Qurra, Ibn al-Haytham, Kitāb al-Manāẓir, al-Bīrūnī, Khayyām, OpenITI, Heisenberg, Schrödinger, Dirac, Pauli, Bohr, quantum "
      "mechanics, Archimedes, Ptolemy, Almagest, Heiberg, Paul Klee, Pädagogisches Skizzenbuch, Bauhaus, Schöpferische Konfession, Training Layer Literature")
issue = "\n".join([
    "### Protocol Version\n\nalexanarch-deposit-protocol/v1\n",
    f"### Title\n\n{title}\n", "### Creator\n\nSharks, Lee\n", "### ORCID\n\n0009-0000-1599-0703\n",
    "### Date\n\n2026-10-30\n", f"### Description\n\n{desc}\n", "### Content Type\n\nDataset\n", "### License\n\nCC-BY-4.0\n",
    "### Substrate Disclosure\n\nHuman–machine collaborative. The sources found, fetched, verified, hashed and indexed, the builders written and the "
    "records drafted, all in session by TACHYON (Claude, Anthropic) under MANUS (Lee Sharks) direction. The request and the figures named "
    "are Lee Sharks's; the works within each seat were chosen in session and are stated per seat. CC-BY-4.0 applies to this record and the seat records.\n",
    f"### Keywords\n\n{kw}\n",
    "### Related Identifiers\n\nAXN deposit #1713 — EA-CORPORA-28: the wanted, whose declared Klee seat (28/06) this seating fulfils\n"
    "AXN deposit #1716 — EA-CORPORA-29: the twenty-ninth seating, whose builder this seating uses\n"
    "AXN deposit #1698 — EA-CORPORA-20: the seating that holds Euclid (20/04), cross-referenced from 30/11\n"
    "AXN deposit #1711 — EA-MPAI-ORIGINALS-01 v1.1: the inspection packet of the originals library\n",
    "### Version\n\nv1.0\n",
    "### Methodology\n\nEach seat fetched in session from the source its record names (the Internet Archive, OpenITI, Open Greek and Latin, Wikisource, "
    "Project Gutenberg), kept as served, reduced to a text layer by code and hashed into its MANIFEST.sha256; licences read at the file; loci verified by "
    "substring in the text layer; public-domain status in the United States checked against first publication. No text corrected by hand. The builders "
    "and this body are under rebuild/corpora/ea-corpora-30/.\n",
    "### Falsification Conditions\n\nA seat is falsified if its files do not verify against its MANIFEST.sha256 at the canonical URL; if a verified "
    "locus is absent from the text layer it names; if a work is misattributed, misdated or assigned to the wrong edition; if a licence recorded "
    "for an item is not the one its source states; if a work seated as public domain in the United States is not; or if the four surfaces "
    "(seat, index, deposit, shelf) disagree.\n",
    f"### Body\n\n{body}"])
out = ROOT / "data/issue-bodies/EA-CORPORA-30-issue.md"
out.write_text(issue, encoding="utf-8")
print(out, len(body.split()), "words in body;", len(desc), "chars in description;", nw, "works;", tot, "lines;", nfiles, "files")
