#!/usr/bin/env python3
"""Write the EA-CORPORA-37 deposit issue body from the twelve seat records (the form of body35.py).
Edition lines, loci, licences and scopes are read from data/corpora/<seat>/source.json.
-> data/issue-bodies/EA-CORPORA-37-issue.md"""
import json, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[3]
A = ROOT / "data/corpora"
SEATS = [
 ("slavonic-josephus-meshcherskii-1958", "Seat 37/01 — Meshcherskii, История Иудейской войны Иосифа Флавия в древнерусском переводе (1958)", "The Old Russian Jewish War in seven books, in the language of the translation"),
 ("berendts-grass-slavonic-josephus-1924", "Seat 37/02 — Berendts and Grass, Flavius Josephus vom Jüdischen Kriege, Buch I–IV (Dorpat, 1924–1927)", "Books I–IV in German with the Greek compared, and the nineteen Überschüsse over the Greek"),
 ("thackeray-loeb-josephus-iii-1928", "Seat 37/03 — Thackeray, Loeb Josephus III (1928)", "The Jewish War IV–VII, and the twenty-two Slavonic additions in English"),
 ("eisler-iesous-basileus-1929", "Seat 37/04 — Eisler, ΙΗΣΟΥΣ ΒΑΣΙΛΕΥΣ ΟΥ ΒΑΣΙΛΕΥΣΑΣ (1929–1930)", "The case for Josephus's first draft, with the Slavonic passages rendered and argued"),
 ("berendts-zeugnisse-slavischen-josephus-1906", "Seat 37/05 — Berendts, Die Zeugnisse vom Christentum im slavischen De bello judaico (1906)", "The first statement of the case in the West: the Slavonic from Josephus's Aramaic first edition"),
 ("berendts-zacharias-johannes-apokryphen-1904", "Seat 37/06 — Berendts, Die handschriftliche Überlieferung der Zacharias- und Johannes-Apokryphen (1904)", "The John apocrypha in Greek and Slavonic: the road to the Slavonic John"),
 ("berendts-zacharias-studien-1895", "Seat 37/07 — Berendts, Studien über Zacharias-Apokryphen und Zacharias-Legenden (1895)", "Zechariah, father of John, and his murder in the Temple"),
 ("eisler-messiah-jesus-1931", "Seat 37/08 — Eisler, The Messiah Jesus and John the Baptist (1931)", "The Halōsis in English: the Slavonic passages, the Essenes, the Testimonium"),
 ("eisler-testimonium-flavianum-1938", "Seat 37/09 — Eisler, Flavius-Josephus-Studien I: Das Testimonium Flavianum (1938)", "The answer to Bienert: the polemic of the consensus years in Eisler's words"),
 ("eisler-orpheus-the-fisher-1921", "Seat 37/10 — Eisler, Orpheus the Fisher (1921)", "The fish and the fisher, Orphic to Christian"),
 ("eisler-enigma-fourth-gospel-1938", "Seat 37/11 — Eisler, The Enigma of the Fourth Gospel (1938)", "The gospel's author and its writer as two persons"),
 ("eisler-weltenmantel-1910", "Seat 37/12 — Eisler, Weltenmantel und Himmelszelt (1910)", "The high priest's robe as the cosmos, and the ancient world-picture"),
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
            f"- Research: {research(s['research'])}", f"- Why seated: {s['why_seated']}",
            f"- Files: [the seat](https://www.alexanarch.org/data/corpora/{corpus}/) — [source.json](https://www.alexanarch.org/data/corpora/{corpus}/source.json), "
            f"[MANIFEST.sha256](https://www.alexanarch.org/data/corpora/{corpus}/MANIFEST.sha256). Shelf: "
            f"[traininglayerliterature.org/originals/{corpus}](https://traininglayerliterature.org/originals/{corpus}/)", ""]
    return "\n".join(out), s


title = ("EA-CORPORA-37 — The Thirty-Seventh Seating: The Slavonic Josephus — the Old Russian Jewish War in Seven Books, "
         "Its Translations and Its First Challengers (Meshcherskii 1958; Berendts and Grass 1924–1927; Thackeray 1928; Berendts 1895–1906; Eisler 1910–1938)")
parts, tot = [], 0
for c, h, sub in SEATS:
    t, s = section(c, h, sub); parts.append(t); tot += s["lines_total"]
nfiles = sum(1 for c, _, _ in SEATS for p in (A / c).rglob("*") if p.is_file())

hdr = f"""# {title}

# EA-CORPORA-37 — The Thirty-Seventh Seating

The author asked for the seating on 2026-11-12: "we need to seat as much of slavonic josephus as possible, source language translation or both - we werent previously able to locate a full copy" (12:48 EST); "whos the guy who first made the challenge? his article shaped my reading - we should seat that with this and his other scholarship if its public domain" (13:16), the man named at 13:20 as "fiery. polemical. but disciplined.", Robert Eisler; and "lets do that as a versioned seating with the old russian josephus + they belong together. and no seating is final until it gets its tll spine and card" (13:28).

EA-CORPORA-01/12 (#1510) seated the Slavonic Josephus on 2026-08-19 as an index of the eight Jesus-and-John passages, after a documented negative search that found no openly served text of the recension. That seat stands, with its manifest and AXN unchanged; its record now points here. This seating holds what the search did not reach. The Old Russian of all seven books is in Meshcherskii's 1958 edition from the Vilna Chronograph, served by the Internet Archive (37/01). Books I–IV are in German, with the Greek compared at every phrase, in the four Lieferungen of Berendts and Grass, served by the University of Tartu (37/02). The twenty-two additions are in English in Thackeray's Loeb appendix of 1928, whose last three carry Books V–VI (37/03). The case for the Slavonic as Josephus's own first draft is made first by Alexander Berendts in 1906 (37/05) and argued at full force by Robert Eisler in 1929–1931 (37/04, 37/08) and again in 1938 against Bienert (37/09). Berendts's John and Zechariah apocrypha (37/06–37/07) and three further works of Eisler (37/10–37/12) complete the authors' public-domain scholarship on the question and around it.

The research occasion is The Josephus Thesis (#1759) and the challenge to the consensus reading of the Slavonic as spurious, opened 2026-11-12: "the case that these are later interpolations just stops making sense once we range beyond the john and jesus materials". The seated texts carry the ground of that challenge. Berendts and Grass count nineteen additions over the Greek in Books I–IV, of which four concern John or the wonder-worker. In the Essene chapter they record agreements of the Slavonic with Hippolytus, Refutatio IX 18–28, against the Greek: the sects as "eine dreifache Ordnung gesetzlicher Lebensweise", not three forms of philosophy; the novice lodged for his first year in another house, "eine der auffallendsten Übereinstimmungen zwischen beiden". The books of the Refutatio that hold the Essenes were lost from late antiquity until the Athos manuscript of 1842. And the initiate's oath in the Old Russian calls to witness "бога живаго, и десницю его всемощную, и духъ божии невмѣстимыи, серафим и херувим … и всю небесьную силу" (here cleaned of the OCR's note numbers and line breaks, with ѣ restored where it reads $), where the Greek has only fearful oaths.

Declared and not pursued (commons only): Meshcherskii's introduction and commentary (1958), held by reference at the Archive item, not copied; the edition of V. Istrin and P. Pascal, La prise de Jérusalem de Josèphe le Juif (Paris, 1934–1938), not located in an open text layer in session; the critical edition of A. A. Pichkhadze and others (Moscow, 2004), served behind a sign-in; Berendts, "Analecta zum slavischen Josephus" (ZNW 9, 1908), not located in an open text layer in session; H. and K. Leeming, Josephus' Jewish War and Its Slavonic Version (Brill, 2003), J. M. Creed (HTR 25, 1932), S. Zeitlin's studies, W. Bienert (1936) and A. Whealey's work, in copyright. The PDFs of the Internet Archive items are held by reference at their Archive URLs.
"""
tail = """## How the seats were made

Every seat was fetched in session and hashed into its MANIFEST.sha256, with a source.json recording edition, origin, licence, normalization, the loci verified in the text layer, and the research the seat was made for. The loci keep the OCR's readings: in 37/01 ѣ comes through as $, Ъ, З or Ф, and in 37/05 the Old Russian and Greek are damaged. Three seats are cut by line number from a larger text layer, each recording the full layer's SHA-256 and the lines kept: 37/01 the edition's TEXTS section, 37/05 and 37/06 their Hefte from bound volumes of Texte und Untersuchungen. The builders are under rebuild/corpora/ea-corpora-37/: build_seats37a.py builds 37/01–37/04, and 37/05–37/12 were built in session with its write_seat helper, as NOTE.md records, seat_axns37.py gives them their AXNs once deposited, and body37.py writes this body.
"""
body = hdr + "\n" + "\n".join(parts) + "\n" + tail
desc = ("The thirty-seventh seating of the originals shelf, twelve seats: the Slavonic Josephus in its own language and in translation, with the first challengers of the reading of it as spurious. "
        "The Old Russian Jewish War in seven books (Meshcherskii 1958); Books I–IV in German with the Greek compared (Berendts and Grass, Dorpat 1924–1927); the twenty-two additions in English (Thackeray, Loeb 1928); "
        "Berendts's Zeugnisse vom Christentum im slavischen De bello judaico (1906) and his John and Zechariah apocrypha (1895, 1904); Eisler's ΙΗΣΟΥΣ ΒΑΣΙΛΕΥΣ (1929–1930), The Messiah Jesus (1931), Das Testimonium Flavianum (1938) and three further works. "
        "The text layer the negative search of EA-CORPORA-01/12 (#1510) could not find, held for The Josephus Thesis (#1759).")
kw = ("EA-CORPORA, originals shelf, Slavonic Josephus, Old Russian Josephus, Halosis, Capture of Jerusalem, Jewish War, Bellum Judaicum, Vilna Chronograph, Meshcherskii, Berendts, Grass, Thackeray, Eisler, "
      "Testimonium Flavianum, wonder-worker, John the Baptist, Essenes, Hippolytus, Refutatio, Aramaic first edition, interpolation, Josephus Thesis, Revelation First")
related = "\n".join([
    "AXN deposit #1510 — EA-CORPORA-01/12: The Slavonic Josephus: Negative Search and the Contested Pericope Set, whose text layer this seating supplies",
    "AXN deposit #1759 — The Josephus Thesis: The Custody of the Name, the research this seating serves",
    "AXN deposit #1176 — The Word That Became Text: The Slavonic Josephus, the Grammar of Incarnation, and the Doctrine of the Logos, whose Appendix II defines the eight passages",
    "AXN deposit #1698 — EA-CORPORA-20: the Ethiopian canon in Ge'ez, with the Ethiopic Yosippon (Zena Ayhud)",
    "AXN deposit #1748 — EA-CORPORA-36: the thirty-sixth seating"]) + "\n"
issue = "\n".join([
    "### Protocol Version\n\nalexanarch-deposit-protocol/v1\n",
    f"### Title\n\n{title}\n", "### Creator\n\nCranes, Rebekah\n", "### ORCID\n\n0009-0000-1599-0703\n",
    "### Date\n\n2026-11-12\n", f"### Description\n\n{desc}\n", "### Content Type\n\nDataset\n", "### License\n\nCC-BY-4.0\n",
    "### Substrate Disclosure\n\nHuman–machine collaborative. Rebekah Cranes is a heteronym of Lee Sharks, the standing authority on the EA-CORPORA deposits (named by the author on 2026-11-04 and held at his word of 2026-11-05). The sources found, fetched, verified, hashed and indexed, and the records drafted, in session by TACHYON (Claude, Anthropic) under MANUS (Lee Sharks) direction. The request, the challenger named, and the research occasion are Lee Sharks's; the editions within each seat were chosen in session and are stated per seat. CC-BY-4.0 applies to this record and the seat records.\n",
    f"### Keywords\n\n{kw}\n", f"### Related Identifiers\n\n{related}", "### Version\n\nv1.0\n",
    "### Methodology\n\nEach seat fetched in session from the source its record names (the Internet Archive; the University of Tartu Library's OJS), kept as served, reduced to a text layer by code and hashed into its MANIFEST.sha256; licences read at the item; loci verified by substring in the text layer, in the OCR's own readings; public-domain status checked against first publication and the author's death, and stated per jurisdiction where it differs. No text corrected by hand. The builders and this body are under rebuild/corpora/ea-corpora-37/.\n",
    "### Falsification Conditions\n\nA seat is falsified if its files do not verify against its MANIFEST.sha256 at the canonical URL; if a verified locus is absent from the text layer it names; if a work is misattributed, misdated or assigned to the wrong edition; if a licence recorded for an item is not the one its source states; if a work seated as public domain is not, in the jurisdiction stated; if a seat cut from a larger text layer does not match the lines it records; or if the four surfaces (seat, index, deposit, shelf) disagree.\n",
    f"### Body\n\n{body}",
    "### Terms\n\n- [x] I read the deposit protocol at https://alexanarch.org/api/deposit-protocol.json\n- [x] I confirm this work is deposited under the stated license\n- [x] I confirm the substrate disclosure is accurate\n- [x] I understand that deposited content will NOT be used to train enforcement classifiers\n"])
out = ROOT / "data/issue-bodies/EA-CORPORA-37-issue.md"
out.write_text(issue, encoding="utf-8")
print(out, len(body.split()), "words in body;", len(desc), "chars in description;", tot, "lines;", nfiles, "files")
