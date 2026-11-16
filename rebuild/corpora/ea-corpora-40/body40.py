#!/usr/bin/env python3
"""Write the EA-CORPORA-40 deposit issue body from the sixteen seat records (the form of body38.py).
Edition lines, loci, licences and scopes are read from data/corpora/<seat>/source.json.
-> data/issue-bodies/EA-CORPORA-40-issue.md"""
import json, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[3]
A = ROOT / "data/corpora"
SEATS = [
 ("classical-philology-1906-1922", "Seat 40/01 — Classical Philology I–XVII (1906–1922), whole", "The census's journal on the page, item by item"),
 ("wolf-prolegomena-1795", "Seat 40/02 — F. A. Wolf, Prolegomena ad Homerum I (1795)", "One name into many"),
 ("wolf-darstellung-altertumswissenschaft-1807", "Seat 40/03 — F. A. Wolf, Darstellung der Alterthums-Wissenschaft (1807; ed. 1833)", "The discipline defined, and its object bounded"),
 ("boeckh-encyklopaedie-1877", "Seat 40/04 — August Boeckh, Encyklopädie und Methodologie der philologischen Wissenschaften (1877)", "Erkenntniss des Erkannten"),
 ("usener-philologie-geschichtswissenschaft-1882", "Seat 40/05 — Hermann Usener, Philologie und Geschichtswissenschaft (1882)", "Philology among the historical sciences"),
 ("lachmann-lucretius-1850", "Seat 40/06 — Karl Lachmann, In T. Lucretii Cari De rerum natura libros commentarius (1850)", "The method named for him"),
 ("madvig-adversaria-critica-1871-1873", "Seat 40/07 — J. N. Madvig, Adversaria critica I–II (1871–1873)", "The locus grain as a body of work"),
 ("housman-manilius-ii-1912", "Seat 40/08 — A. E. Housman, Manilius, Astronomicon II (1912)", "The method at its most exacting"),
 ("nietzsche-philologica-1869-1910", "Seat 40/09 — Friedrich Nietzsche, the philological writings (1869, 1870; eds. 1896, 1910)", "The philologist the field refused"),
 ("rohde-afterphilologie-1872", "Seat 40/10 — Erwin Rohde, Afterphilologie (1872)", "The boundary drawn, and answered"),
 ("valla-donatio-schwahn-1928", "Seat 40/11 — Lorenzo Valla, De falso credita et ementita Constantini donatione (ed. Schwahn, 1928)", "A received document shown not to be what it was received as"),
 ("casaubon-exercitationes-1614", "Seat 40/12 — Isaac Casaubon, De rebus sacris et ecclesiasticis exercitationes XVI (1614)", "An ancient author dissolved"),
 ("bentley-phalaris-1699", "Seat 40/13 — Richard Bentley, A Dissertation upon the Epistles of Phalaris (1699)", "A forgery shown by language and chronology"),
 ("diels-doxographi-graeci-1879", "Seat 40/14 — Hermann Diels, Doxographi Graeci (1879)", "The construction behind the reports 'from Theophrastus'"),
 ("sandys-history-classical-scholarship-1903-1908", "Seat 40/15 — J. E. Sandys, A History of Classical Scholarship I–III (1903–1908)", "The field's history of itself"),
 ("philology-census-classical-philology", "Seat 40/16 — The census of Classical Philology", "The Crossref records, the items, the samples, the corpus-grain candidates, the script and the notebook"),
]
lic = lambda l: l["payload"] if isinstance(l, dict) else str(l)


def research(r):
    if isinstance(r, dict):
        return "; ".join(f"{k.replace('_', ' ')}: {v}" for k, v in r.items())
    return str(r)


def section(corpus, heading, sub):
    s = json.loads((A / corpus / "source.json").read_text(encoding="utf-8"))
    w = s["works"]["list"]
    out = [f"## {heading}", "", f"*{sub}*", ""]
    if len(w) <= 40:
        out += ["- Works:"] + [f"  - {x['work']}" for x in w]
    else:
        out += [f"- Works: {len(w)} volumes and files, listed in the seat's source.json"]
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


title = ("EA-CORPORA-40 — The Fortieth Seating: Philology Constituted — Classical Philology 1906–1922 Whole, the Discipline Defined from Wolf to Usener, "
         "the Method from Lachmann to Housman, the Quarrel over the Geburt der Tragödie, the Standing Question from Valla to Bentley, Diels, Sandys, and the Census of Classical Philology")
parts, tot = [], 0
for c, h, sub in SEATS:
    t, s = section(c, h, sub); parts.append(t); tot += s["lines_total"]
nfiles = sum(1 for c, _, _ in SEATS for p in (A / c).rglob("*") if p.is_file())

hdr = f"""# {title}

# EA-CORPORA-40 — The Fortieth Seating

The author asked for the gathering on 2026-11-16, while the census of the philology journals began with Classical Philology: "oh - and we need an ea-corpora. what can and should be gathered up? philology is a rich historical field". He asked first for an inventory ("first we check what we have"), then for the gathering ("lets begin gathering for the ea corpora"; "certainly we can locate wilamowitz elsewhere... and Nietzsche - there must be copies"), and at 14:48 EST for the deposit: "and then yes lets build the ea-corpora deposit". The census is in its working notebook (v0.1, seated here as 40/16) and is not deposited; this seating precedes it. Biblical criticism is the census's next station and is kept apart from this seating, at the author's word ("keep biblical separate from the current question, and after we've done both separately we'll look at the combine").

The archive held philology's applications (the authenticity criticism of Plato, the editing of Sappho) and not its constitution. These sixteen seats hold the constitution. Classical Philology I–XVII is seated whole, item by item (40/01), so that the census, which Crossref allows only from titles, can read the text question on the page at each grain. The discipline defined: Wolf's Prolegomena (40/02), one name into many; Wolf's Darstellung (40/03), which bounds the object and sets the Egyptians, Hebrews and Persians apart, "nicht ... auf Einer Linie mit den Griechen und Römern"; Boeckh's Erkenntniss des Erkannten (40/04); Usener (40/05). The method: Lachmann's Lucretius (40/06), Madvig's Adversaria (40/07), Housman's Manilius II (40/08). The boundary drawn: Nietzsche's philological writings (40/09) and Rohde's Afterphilologie (40/10), the quarrel in which the field refused a book as not philology. The standing question's canon: Valla (40/11), Casaubon (40/12), Bentley (40/13), the three demonstrations that a received author or document was not what it was received as. Diels's Doxographi Graeci (40/14), behind every report of the Presocratics from Theophrastus. Sandys (40/15), the field's history of itself, where Wolf's matriculation as Studiosus Philologiae on 8 April 1777 is told as an epoch. The census itself, with its samples for the blind parallel run (40/16).

Already seated and not reseated: Nietzsche, Die Geburt der Tragödie, new edition of 1886 (EA-CORPORA-27/03, #1712); Philologus, the cited volumes, and the Classical Quarterly, 1914 and 1926–1929 (39/10, 39/11, #1771); Bergk's Poetae Lyrici Graeci III (33/04); Hermann, Elementa doctrinae metricae (36/33, #1748); Theophrastus's Characteres ed. Diels (38/04).

## Pointers to the rest

Held for a later seating, with what is known of each:

- Wilamowitz, Zukunftsphilologie! (1872) and its second part (1873): located at Google Books (PtVXAAAAcAAJ, i1NbAAAAcAAJ); not fetchable from the session; the author is to supply the copies. The first edition of the Geburt der Tragödie (1872), likewise.
- Wilamowitz, Geschichte der Philologie (1921): public domain in the United States; not yet located in an open scan.
- Housman, Manilius I (1903), with the preface, and "The Application of Thought to Textual Criticism" (1921): not at the Internet Archive in an open scan.
- Madvig, Adversaria critica III (1884): not yet located.
- Classical Philology 1923–1928: in the United States public domain, not in JSTOR's Early Journal Content at the Archive.
- The other journals, for later stations: American Journal of Philology, Transactions of the American Philological Association, The Classical Review, Hermes, Rheinisches Museum and Mnemosyne, through 1930.
- Declared, not pursued (in copyright, or behind paywalls): Pfeiffer, History of Classical Scholarship (1968, 1976); Timpanaro, La genesi del metodo del Lachmann (1963); Reynolds and Wilson, Scribes and Scholars; Grafton, Defenders of the Text and Forgers and Critics; Maas, Textkritik (1927).
"""
tail = f"""## How the seats were made

Every seat was fetched in session from the Internet Archive or Crossref and hashed into its MANIFEST.sha256, with a source.json recording edition, origin, licence, normalization, the loci verified in the text, and the research the seat was made for. The Archive's text layers are held once, under text/, exactly as served: the builder checks the SHA-256 of each file against the fetch log before seating it. Loci are verified with all whitespace collapsed and keep the scans' readings (Casaubon's long s read as f; Housman's title page in capitals with V for U). Classical Philology is seated from JSTOR's Early Journal Content, whose items mostly carry no title in the Archive's metadata ("[untitled]"); each item is held under its identifier, with its date and pages. The census (40/16) holds no abstract: Crossref has none for the journal, and the builder refuses a census file in which an abstract holds text. Where the Archive's catalogue date was wrong, the seat says so (Housman's Book II is 1912, not 1903). The builders are under rebuild/corpora/ea-corpora-40/ (build_seats40.py, index40.py, seat_axns40.py, and body40.py, which writes this body); NOTE.md records the order.

In all: sixteen seats, {nfiles:,} files, {tot:,} lines of text.
"""
body = hdr + "\n" + "\n".join(parts) + "\n" + tail
desc = ("The fortieth seating of the originals shelf, sixteen seats, gathered for the census of the philology journals, which began with Classical Philology, and seated before it. "
        "Classical Philology I–XVII (1906–1922) whole, as JSTOR's Early Journal Content; the discipline defined: Wolf's Prolegomena ad Homerum (1795) and Darstellung der Alterthums-Wissenschaft (1807), Boeckh's Encyklopädie (1877), Usener (1882); "
        "the method: Lachmann's Lucretius (1850), Madvig's Adversaria critica (1871–1873), Housman's Manilius II (1912); the boundary drawn: Nietzsche's philological writings and Rohde's Afterphilologie (1872); "
        "the standing question: Valla, Casaubon (1614), Bentley (1699); Diels's Doxographi Graeci (1879); Sandys's History of Classical Scholarship (1903–1908); and the census of Classical Philology, without abstracts. Pointers to what is not seated, Wilamowitz's Zukunftsphilologie! first.")
kw = ("EA-CORPORA, originals shelf, philology census, Classical Philology, history of classical scholarship, Altertumswissenschaft, F. A. Wolf, Prolegomena ad Homerum, Homeric question, Boeckh, Usener, "
      "Lachmann, textual criticism, recension, Madvig, conjectural criticism, Housman, Manilius, Nietzsche, Rohde, Afterphilologie, Wilamowitz, Zukunftsphilologie, Geburt der Tragödie, "
      "Valla, Donation of Constantine, Casaubon, Hermetica, Bentley, Phalaris, forgery, authenticity, Diels, Doxographi Graeci, Sandys, Crossref census, JSTOR Early Journal Content")
related = "\n".join([
    "AXN deposit #1773 — This Is Not Philosophy, the combined audit's second station, whose instrument the census carries",
    "AXN deposit #1770 — Who Speaks for the Classics, and on What Basis, the first station",
    "AXN deposit #1775 — ΦΑΙΝΕΤΑΙ ΜΟΙ v2.4, the submission whose decline at Classical Philology opened the census",
    "AXN deposit #1771 — EA-CORPORA-39: the field before the flattening, with Philologus and the Classical Quarterly",
    "AXN deposit #1712 — EA-CORPORA-27: Nietzsche in German, with the Geburt der Tragödie of 1886",
    "AXN deposit #1580 — EA-CORPORA-12: the transmission texts, Diogenes Laertius whole"]) + "\n"
issue = "\n".join([
    "### Protocol Version\n\nalexanarch-deposit-protocol/v1\n",
    f"### Title\n\n{title}\n", "### Creator\n\nCranes, Rebekah\n", "### ORCID\n\n0009-0000-1599-0703\n",
    "### Date\n\n2026-11-16\n", f"### Description\n\n{desc}\n", "### Content Type\n\nDataset\n", "### License\n\nCC-BY-4.0\n",
    "### Substrate Disclosure\n\nHuman–machine collaborative. Rebekah Cranes is a heteronym of Lee Sharks, the standing authority on the EA-CORPORA deposits (named by the author on 2026-11-04 and held at his word of 2026-11-05). The sources found, fetched, verified against their fetch logs, hashed and indexed, the census staged, and the records drafted, in session by TACHYON (Claude, Anthropic) under MANUS (Lee Sharks) direction. The gathering, its object, its form and its rulings are Lee Sharks's; the scans within each seat were chosen in session and are stated per seat. CC-BY-4.0 applies to this record and the seat records.\n",
    f"### Keywords\n\n{kw}\n", f"### Related Identifiers\n\n{related}", "### Version\n\nv1.0\n",
    "### Methodology\n\nEach seat fetched in session from the source its record names (the Internet Archive; JSTOR Early Journal Content at the Archive; Crossref); the Archive's text layers held as served, checked against the fetch logs and hashed into each MANIFEST.sha256; licences read at the item; loci verified by substring with whitespace collapsed, in the scans' own readings; public-domain status checked against first publication; catalogue dates checked against title pages. No text corrected by hand. The builders and this body are under rebuild/corpora/ea-corpora-40/.\n",
    "### Falsification Conditions\n\nA seat is falsified if its files do not verify against its MANIFEST.sha256 at the canonical URL; if a verified locus is absent from the text it names; if a work is misattributed, misdated or assigned to the wrong scan; if a licence recorded for an item is not the one its source states; if a work seated as public domain is not, in the jurisdiction stated; if any file of the census holds an abstract; if an item of Classical Philology seated under an identifier is not that identifier's served text; or if the four surfaces (seat, index, deposit, shelf) disagree.\n",
    f"### Body\n\n{body}",
    "### Terms\n\n- [x] I read the deposit protocol at https://alexanarch.org/api/deposit-protocol.json\n- [x] I confirm this work is deposited under the stated license\n- [x] I confirm the substrate disclosure is accurate\n- [x] I understand that deposited content will NOT be used to train enforcement classifiers\n"])
out = ROOT / "data/issue-bodies/EA-CORPORA-40-issue.md"
out.write_text(issue, encoding="utf-8")
print(out, len(body.split()), "words in body;", len(desc), "chars in description;", tot, "lines;", nfiles, "files")
