#!/usr/bin/env python3
"""Write the EA-CORPORA-39 deposit issue body from the thirteen seat records (the form of body38.py).
Edition lines, loci, licences and scopes are read from data/corpora/<seat>/source.json.
-> data/issue-bodies/EA-CORPORA-39-issue.md"""
import json, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[3]
A = ROOT / "data/corpora"
SEATS = [
 ("agph-archiv-1888-1923", "Seat 39/01 — Archiv für Geschichte der Philosophie I–XXXVI (1888–1923)", "The field before the flattening: a work's standing as an ordinary article in a philosophy journal"),
 ("brucker-historia-critica-1742", "Seat 39/02 — Jacob Brucker, Historia critica philosophiae I (1742)", "The ancients narrated as systems"),
 ("brucker-historia-critica-iv-1743", "Seat 39/03 — Jacob Brucker, Historia critica philosophiae IV.1 (1743)", "The Platonists brought into the order of a system"),
 ("hermann-geschichte-system-1839", "Seat 39/04 — Karl Friedrich Hermann, Geschichte und System der platonischen Philosophie I (1839)", "The dialogues as stages of a development"),
 ("zeller-philosophie-griechen-1865", "Seat 39/05 — Eduard Zeller, Die Philosophie der Griechen I (1856/1865)", "The handbook that fixed the received order"),
 ("ueberweg-echtheit-zeitfolge-1861", "Seat 39/06 — Friedrich Ueberweg, Untersuchungen über die Echtheit und Zeitfolge platonischer Schriften (1861)", "Genuineness and order as the subject of a book"),
 ("schaarschmidt-sammlung-1866", "Seat 39/07 — Carl Schaarschmidt, Die Sammlung der platonischen Schriften (1866)", "The athetesis at its height, with an OCR made for the seat"),
 ("grote-plato-1865", "Seat 39/08 — George Grote, Plato, and the Other Companions of Sokrates I (1865)", "The canon defended against the athetizers"),
 ("lutoslawski-plato-logic-1897", "Seat 39/09 — Wincenty Lutosławski, The Origin and Growth of Plato's Logic (1897)", "Stylometry named and turned on the order of the dialogues"),
 ("philologus-cited-1858-1916", "Seat 39/10 — Philologus, the cited volumes (1858–1916)", "The philology journal where the question held its rate"),
 ("classical-quarterly-1914-1929", "Seat 39/11 — The Classical Quarterly, 1914 and 1926–1929", "The interim question in English"),
 ("this-is-not-philosophy-census", "Seat 39/12 — The census of This Is Not Philosophy", "The journals in Crossref and Persée, the codes with their spans, the logs and the scripts; the abstracts reached by DOI"),
 ("this-is-not-philosophy-gates", "Seat 39/13 — The gates of This Is Not Philosophy", "The editor's responses to the submissions and the policies on AI, as dated excerpts"),
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


title = ("EA-CORPORA-39 — The Thirty-Ninth Seating: The Field before the Flattening — the Archiv für Geschichte der Philosophie 1888–1923, "
         "the Construction of the Object from Brucker to Lutosławski, the Philology Journals, and the Census and Gates of This Is Not Philosophy")
parts, tot = [], 0
for c, h, sub in SEATS:
    t, s = section(c, h, sub); parts.append(t); tot += s["lines_total"]
nfiles = sum(1 for c, _, _ in SEATS for p in (A / c).rglob("*") if p.is_file())

hdr = f"""# {title}

# EA-CORPORA-39 — The Thirty-Ninth Seating

The author asked for the gathering on 2026-11-15, for the study now titled This Is Not Philosophy: How Disciplinarity Murdered Philosophy — The Shape of the Field: "i suppose we need to gather up materials for an ea-corpora seating for this one, and that that will help the case substantially, especially as we increase holdings beyond the recent, where the flattening is already largely accomplished" (22:43 EST). At 22:56 he adopted the three rulings on its form (the census without the publishers' abstracts, the philology journals by their cited volumes, the gates as dated excerpts) and asked for the interim: "adopted on all. lets build the seating. but we need to find more accessible interim journals before the 2000s". At 23:51 he ruled the order: "the seating goes first - we have more analysis to run from it". The study is not yet deposited; this seating precedes it, so that its analysis can be run from what is seated.

The study measures what the journals of ancient philosophy now publish: in Ancient Philosophy, 8 of 844 articles open the question of what the object is (a work's authenticity, authorship, date, order, unity), and since 2021, 4 of 283 Plato/Aristotle abstracts across the sister journals. The thirteen seats hold what that measure is read against. The field before the flattening is the Archiv für Geschichte der Philosophie in its first thirty-six volumes (39/01), where one ancient title in five in the 1890s puts a work's standing in question as an ordinary article: Appel on the authenticity of the Sophistes (V, 1892), the latest athetesis of the Philebus (IX, 1896), the authenticity of the De interpretatione (XIII, 1900), the order of the Metaphysics (XX, 1907/08). The construction of the object runs from Brucker (39/02, 39/03), who narrates the ancients as systems, "enarratione fyftematum veterum", through Hermann's genetic reading (39/04), Zeller's handbook (39/05), Ueberweg on genuineness and order (39/06), Schaarschmidt's athetesis at its height (39/07), "Unechtheit des Sophista und Politikus nachgewiesen", and Grote's defence of the Thrasyllan canon (39/08), to Lutosławski's stylometry (39/09), the instrument that fixed the received early, middle and late. The philology journals (39/10, 39/11) are held by the volumes the study cites, where the question of a work's standing persisted after the philosophy journal had let it go: the date of the Theaetetus in Philologus (1890), the authenticity and authorship of the Hippias Major in the Classical Quarterly (1926, 1927). The census (39/12) holds every figure the study's tables are built from (the journals in Crossref and two series in Persée, the object codes, the reach codes each with its 6–30-word span of the abstract it rests on, the adjudication logs, the stylometry, the scripts) and reaches each abstract by its DOI rather than reseating it. The gates (39/13) hold, as dated excerpts, the specification of the unit in the editor's own responses to the submissions, under the author's ruling that correspondence with the editor of Ancient Philosophy in his official capacity, on the substance of his field, is institutional; and the policies on AI-authored submissions at the journals and publishers where the template is strongest.

Already seated and not reseated: Schleiermacher, Platons Werke I.1 with the Einleitung (EA-CORPORA-32/07, #1731); Campbell, The Sophistes and Politicus (32/08); Tennemann, System der Platonischen Philosophie I (32/09); Jaeger, Aristoteles (EA-CORPORA-31/10, #1730). A second OCR of Tennemann's System I, from another scan (bub_gb_uuk9AAAAcAAJ), was made in session and is not seated. Plato and Aristotle are in EA-CORPORA-04.

## Pointers to the rest

Held for a later seating, with what is known of each:

- Archiv für Geschichte der Philosophie XIV (1901), XXIX (1916), XXXII (1919): not in the Toronto run at the Internet Archive; to be sought in another scan.
- Philologus and the Classical Quarterly beyond the cited volumes: the Internet Archive holds Philologus in the Toronto and Google scans, and the Classical Quarterly in full issues to 1961 (sim_classical-quarterly). The Crossref census of both whole runs is in 39/12.
- The interim journals with open full text before 2000: the Revue philosophique de Louvain (Persée, 1894–2019) and the Revue des Études Grecques (Persée, 1888–), whose full metadata (12,649 and 14,668 records) is in 39/12 with the title baselines built from it; and Museum Helveticum (e-periodica, ETH). Their texts are for a later seating.
- The publishers' abstracts of the census: reached by DOI at the publishers' pages and in Crossref, and not reseated (the author's ruling of 22:56).
"""
tail = f"""## How the seats were made

Every seat was fetched in session and hashed into its MANIFEST.sha256, with a source.json recording edition, origin, licence, normalization, the loci verified in the text, and the research the seat was made for. The Internet Archive's text layers are held once, under text/, exactly as served: the SHA-256 of each file is the hash of the served layer, checked against the fetch log, and no second normalized copy is held (the author's ruling of 23:51). Loci are verified with all whitespace collapsed, so that a passage broken across the scan's lines is still found, and keep the scans' readings (Brucker's long s read as f; Tarrant's title as the scan reads it). One seat carries an OCR made for it because the Archive's layer reads the scan poorly: 39/07, by tesseract 5 with the tessdata_fast deu model, page by page from the Archive's images, 445 pages and none failed, with the Archive's own layer held beside it. The census (39/12) was staged by stage_census39.py, which drops every abstract and reference list and refuses to stage a data file in which a key "abstract" holds running text. The builders are under rebuild/corpora/ea-corpora-39/ (stage_census39.py, build_seats39.py, index39.py, seat_axns39.py, and body39.py, which writes this body); NOTE.md records the order.

In all: thirteen seats, {nfiles:,} files, {tot:,} lines of text.
"""
body = hdr + "\n" + "\n".join(parts) + "\n" + tail
desc = ("The thirty-ninth seating of the originals shelf, thirteen seats, gathered for This Is Not Philosophy: How Disciplinarity Murdered Philosophy — The Shape of the Field, and seated before it. "
        "The Archiv für Geschichte der Philosophie I–XXXVI (1888–1923), the field before the flattening; the construction of the object: Brucker's Historia critica (1742, 1743), Hermann (1839), Zeller (1856/1865), Ueberweg (1861), "
        "Schaarschmidt (1866, with an OCR made for the seat), Grote (1865) and Lutosławski (1897); the cited volumes of Philologus and the Classical Quarterly; the census of the study, with its codes, spans, logs and scripts and without the publishers' abstracts; "
        "and the gates, as dated excerpts. Pointers to the volumes and the interim journals not seated.")
kw = ("EA-CORPORA, originals shelf, This Is Not Philosophy, disciplinarity, ontological flattening, history of philosophy, Archiv für Geschichte der Philosophie, authenticity, athetesis, Echtheitsfrage, chronology of the dialogues, "
      "stylometry, Brucker, Historia critica philosophiae, system of philosophy, Hermann, Zeller, Ueberweg, Schaarschmidt, Grote, Thrasyllan canon, Lutosławski, Philologus, Classical Quarterly, Hippias Major, "
      "Ancient Philosophy, Phronesis, Elenchos, Revue philosophique de Louvain, Revue des Études Grecques, Crossref census, reach coding, AI policy, journal gates")
related = "\n".join([
    "AXN deposit #123 — Socrates as Orthonym, the paper whose submission the gates record",
    "AXN deposit #1733 — Legitimately Many, the reception history of the many-author reading",
    "AXN deposit #1730 — EA-CORPORA-31: the transmission of the Peripatetic corpus, with Jaeger's seat",
    "AXN deposit #1731 — EA-CORPORA-32: the remaining debts of Legitimately Many, with Schleiermacher, Campbell and Tennemann",
    "AXN deposit #1769 — Daffodils: Classical Receptions Journal, 2009–2026, the sibling audit of a journal",
    "AXN deposit #1768 — EA-CORPORA-38: the thirty-eighth seating"]) + "\n"
issue = "\n".join([
    "### Protocol Version\n\nalexanarch-deposit-protocol/v1\n",
    f"### Title\n\n{title}\n", "### Creator\n\nCranes, Rebekah\n", "### ORCID\n\n0009-0000-1599-0703\n",
    "### Date\n\n2026-11-16\n", f"### Description\n\n{desc}\n", "### Content Type\n\nDataset\n", "### License\n\nCC-BY-4.0\n",
    "### Substrate Disclosure\n\nHuman–machine collaborative. Rebekah Cranes is a heteronym of Lee Sharks, the standing authority on the EA-CORPORA deposits (named by the author on 2026-11-04 and held at his word of 2026-11-05). The sources found, fetched, OCR'd where the served text layer read the scan poorly, verified, hashed and indexed, the census staged without the publishers' abstracts, the gate excerpts drawn, and the records drafted, in session by TACHYON (Claude, Anthropic) under MANUS (Lee Sharks) direction. The gathering, its object, its form and its rulings are Lee Sharks's; the scans within each seat were chosen in session and are stated per seat. CC-BY-4.0 applies to this record and the seat records.\n",
    f"### Keywords\n\n{kw}\n", f"### Related Identifiers\n\n{related}", "### Version\n\nv1.0\n",
    "### Methodology\n\nEach seat fetched in session from the source its record names (the Internet Archive; Crossref; Persée OAI-PMH); the Archive's text layers held as served and hashed into each MANIFEST.sha256; where the served layer read the scan poorly, an OCR made from the source's page images by tesseract 5, page by page, recorded as the seat's and not corrected; the census staged by code, without the publishers' abstracts; licences read at the item; loci verified by substring with whitespace collapsed, in the scans' own readings; public-domain status checked against first publication. No text corrected by hand. The builders and this body are under rebuild/corpora/ea-corpora-39/.\n",
    "### Falsification Conditions\n\nA seat is falsified if its files do not verify against its MANIFEST.sha256 at the canonical URL; if a verified locus is absent from the text it names; if a work is misattributed, misdated or assigned to the wrong scan; if a licence recorded for an item is not the one its source states; if a work seated as public domain is not, in the jurisdiction stated; if an OCR said to be made from a source's page images is not reproducible from them by the stated model; if any file of the census holds a publisher's abstract; if a gate excerpt is not exact to its source; or if the four surfaces (seat, index, deposit, shelf) disagree.\n",
    f"### Body\n\n{body}",
    "### Terms\n\n- [x] I read the deposit protocol at https://alexanarch.org/api/deposit-protocol.json\n- [x] I confirm this work is deposited under the stated license\n- [x] I confirm the substrate disclosure is accurate\n- [x] I understand that deposited content will NOT be used to train enforcement classifiers\n"])
out = ROOT / "data/issue-bodies/EA-CORPORA-39-issue.md"
out.write_text(issue, encoding="utf-8")
print(out, len(body.split()), "words in body;", len(desc), "chars in description;", tot, "lines;", nfiles, "files")
