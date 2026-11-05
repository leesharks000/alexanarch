#!/usr/bin/env python3
"""Write the EA-CORPORA-34 deposit issue body from the eleven seat records (the form of body33.py).
Edition lines, loci, licences and scopes are read from data/corpora/<seat>/source.json.
-> data/issue-bodies/EA-CORPORA-34-issue.md"""
import json, pathlib
from collections import Counter

ROOT = pathlib.Path(__file__).resolve().parents[3]
A = ROOT / "data/corpora"
SEATS = [("eusebius-historia-ecclesiastica", "Seat 34/01 — Eusebius, Historia ecclesiastica (Dindorf, 1871)", "The ten books in Greek: the ledger of the books, Gaius, Papias's two Johns, Irenaeus's sentence, Dionysius on Nepos"),
         ("irenaeus-adversus-haereses", "Seat 34/02 — Irenaeus, Adversus haereses (Harvey, 1857)", "The Greek of the TEI and both volumes of the Latin: 4.20.11 and 5.30.3"),
         ("justin-dialogus", "Seat 34/03 — Justin, Dialogue with Trypho (Archambault, 1909)", "Dialogue 81.4: John, one of the apostles, in a revelation made to him"),
         ("muratorian-fragment-tregelles", "Seat 34/04 — The Muratorian fragment (Tregelles, 1867)", "Paul, following the order of his predecessor John, writes to seven churches"),
         ("epiphanius-panarion", "Seat 34/05 — Epiphanius, Panarion (Holl)", "Heresy 51, the Alogi, who rejected the Gospel and the Apocalypse of John"),
         ("westcott-canon-1896", "Seat 34/06 — Westcott, General Survey of the History of the Canon (1896)", "The catalogues of the first eight centuries in their original languages (Appendix D)"),
         ("collectio-hispana-1808", "Seat 34/07 — Collectio canonum Ecclesiae Hispanae (1808)", "The Fourth Council of Toledo (633), canon 17, on receiving and reading the Apocalypse"),
         ("september-testament-1522", "Seat 34/08 — Luther's September Testament (1522), facsimile of 1883", "The table of books and the 1522 preface to the Apocalypse; the scan is the witness"),
         ("erasmus-annotationes-1535", "Seat 34/09 — Erasmus, Annotationes (Basel, 1535)", "The annotations on the Apocalypse"),
         ("revelation-criticism-1886-1920", "Seat 34/10 — The critics, 1886–1920", "Vischer, Spitta, Gunkel, Bousset (1896, 1913) and Charles (1920)"),
         ("gregory-textkritik-1900", "Seat 34/11 — Gregory, Textkritik des Neuen Testamentes I (1900)", "The manuscripts that carry the Apocalypse, and the lectionaries"),
         ("scrivener-plain-introduction-1894", "Seat 34/12 — Scrivener, A Plain Introduction, 4th ed. (1894)", "The manuscripts of the Apocalypse and the printed editions (added at v1.1)"),
         ("delitzsch-handschriftliche-funde-1861", "Seat 34/13 — Delitzsch, Handschriftliche Funde (1861)", "Reuchlin's codex, the one exemplar of the first printed Apocalypse (added at v1.1)"),
         ("tregelles-printed-text-1854", "Seat 34/14 — Tregelles, An Account of the Printed Text (1854)", "The succession from Erasmus to the received text (added at v1.1)"),
         ("erasmus-novum-instrumentum-1516", "Seat 34/15 — Erasmus, Novum Instrumentum (1516)", "The first printed Greek New Testament, its Apocalypse; the scan is the witness (added at v1.1)")]
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



title = "EA-CORPORA-34 — The Thirty-Fourth Seating: Secondary Source — the Reception of the Apocalypse, from the Fathers to the Critics (Eusebius, Irenaeus, Justin, the Muratorian Fragment, Epiphanius, the Catalogues, Toledo IV, Luther 1522, Erasmus, the Critics 1886–1920, Gregory; and the Carriage: Scrivener, Delitzsch, Tregelles, Erasmus 1516)"
parts, tot, nw = [], 0, 0
for c, h, sub in SEATS:
    t, s = section(c, h, sub); parts.append(t); tot += s["lines_total"]; nw += s["works"]["count"]
nfiles = sum(1 for c, _, _ in SEATS for p in (A / c).rglob("*") if p.is_file())
hdr = f"""# {title}

# EA-CORPORA-34 — The Thirty-Fourth Seating

The author asked for the seating on 2026-11-05: "also - lets gather up and seat the sources we'll need for this one prior to writing. still under rebekah cranes for the ea-corpora, and with reference to the research occasion"

The research occasion is Secondary Source, the reception study of how the Apocalypse came to be received as derivative, secondary and marginal (design v0.3, drafts/SECONDARY-SOURCE-design-2026-11-05.md, not deposited). Its §5 lists the debts the study must read in seat before drafting; these eleven seats carry them, in the languages the texts were written in. The fathers come from the First1KGreek TEI and from public editions on the Internet Archive; the catalogues of the fourth century are read in Westcott's appendix of the original texts; the Western counter-witness to the Byzantine lectionary is the Fourth Council of Toledo in the Collectio Hispana; the Reformation is held in the 1522 September Testament and Erasmus's Annotationes; the critics run from Vischer (1886) to Charles (1920).

Version 1.1 adds four seats (34/12–34/15), at the operator's words of 2026-11-05: "we should also be tracking material manuscript transmission and succession, that seems particularly important with revelation and less-often and -critically studied than pure reception" (11:02 EST), and "lets bundle the 35 sources with 34 and version in place - theyre of a piece" (11:11 EST). They carry the study's fifth count, carriage: what materially carries the book and from what each carrier descends. Erasmus made the Apocalypse of 1516 from one manuscript lent by Reuchlin, in which text and commentary were mixed; its last verses were wanting, and he supplied them from the Latin. Delitzsch found that manuscript again in 1861; Tregelles and Scrivener trace what it became in the printed text; Erasmus's 1516 printing is seated as the witness.

Declared and not pursued (commons only): Metzger 1987, Hahneman 1992 and the Weimar Ausgabe Deutsche Bibel 7 (in copyright); Zwingli's Sämtliche Werke (access-restricted at the Archive); Hoskier, Concerning the Text of the Apocalypse (1929), its term unclear. The Greek of Cyril's Catecheses, of Gregory of Nazianzus's Carmina and of Amphilochius's Iambi is read in Westcott's appendix, no public TEI of them being reachable in session.
"""
tail2 = """## How the seats were made

Every seat was fetched in session and hashed into its MANIFEST.sha256, with a source.json recording edition, origin, licence, normalization, the loci verified in the text layer, and the research the seat was made for. The builders are under rebuild/corpora/ea-corpora-34/: gen_spec34.py writes the specs of 34/01–34/11 and gen_spec34_carriage.py those of 34/12–34/15, build34.py builds each seat, fix_loci34.py gives the Greek loci in the code points of the seated TEI (which is not in NFC), index_seats34.py enters the seats in the index, and body34.py writes this body.
"""
body = hdr + "\n" + "\n".join(parts) + "\n" + tail2
desc = ("The thirty-fourth seating of the originals shelf, eleven seats, the sources of Secondary Source, the reception study of how the Apocalypse came to be "
        "received as derivative, secondary and marginal, seated before drafting: Eusebius's Historia ecclesiastica in Greek (Dindorf); Irenaeus in Harvey's Greek and Latin; "
        "Justin's Dialogue; the Muratorian fragment in Tregelles's edition; Epiphanius's Panarion (Holl); Westcott's survey with the catalogues of the first eight centuries; "
        "the Collectio Hispana with the Fourth Council of Toledo; Luther's September Testament of 1522; Erasmus's Annotationes; Vischer, Spitta, Gunkel, Bousset and Charles; "
        "and Gregory's Textkritik for the manuscripts and lectionaries; and, at v1.1, the carriage of the book: Scrivener's Plain Introduction (1894), Delitzsch's Handschriftliche Funde (1861) on Reuchlin's codex, Tregelles's Account of the Printed Text (1854) on the last six verses supplied from the Latin, and Erasmus's Novum Instrumentum of 1516.")
kw = ("EA-CORPORA, originals shelf, Secondary Source, Apocalypse, Revelation, reception history, canon, Eusebius, Historia ecclesiastica, Irenaeus, Justin Martyr, "
      "Muratorian fragment, Epiphanius, Alogi, Gaius, Dionysius of Alexandria, Laodicea, Cyril of Jerusalem, Athanasius, Toledo IV, lectionary, Luther, September Testament, "
      "Erasmus, Vischer, Spitta, Gunkel, Bousset, Kyrios Christos, Charles, Gregory, Textkritik, Revelation First, manuscripts, carriage, succession, Reuchlin, Andreas of Caesarea, Novum Instrumentum, Delitzsch, Tregelles, Scrivener, Textus Receptus")
issue = "\n".join([
    "### Protocol Version\n\nalexanarch-deposit-protocol/v1\n",
    f"### Title\n\n{title}\n", "### Creator\n\nCranes, Rebekah\n", "### ORCID\n\n0009-0000-1599-0703\n",
    "### Date\n\n2026-11-05\n", f"### Description\n\n{desc}\n", "### Content Type\n\nDataset\n", "### License\n\nCC-BY-4.0\n",
    "### Substrate Disclosure\n\nHuman–machine collaborative. Rebekah Cranes is a heteronym of Lee Sharks, the standing authority on the EA-CORPORA deposits (named by the author on 2026-11-04 and held at his word of 2026-11-05). The sources found, fetched, verified, hashed and indexed, and the records drafted, in session by TACHYON (Claude, Anthropic) under MANUS (Lee Sharks) direction. The request and the research occasion are Lee Sharks's; the editions within each seat were chosen in session and are stated per seat. CC-BY-4.0 applies to this record and the seat records.\n",
    f"### Keywords\n\n{kw}\n",
    "### Related Identifiers\n\nAXN deposit #1735 — Revelation First: Literary Genealogy and the Missing Ancestors of the Epistles, whose dating record and Muratorian premise the study takes as given\n"
    "AXN deposit #1420 — The Argument of the Bookshelf, whose mechanism the study tests\n"
    "AXN deposit #1738 — EA-CORPORA-33: the thirty-third seating, whose builder this seating uses\n"
    "AXN deposit #1733 — Legitimately Many, the companion reception study\n",
    "### Version\n\nv1.1\n",
    "### Methodology\n\nEach seat fetched in session from the source its record names (First1KGreek, the Internet Archive), kept as served, reduced to a text layer by code and hashed into its MANIFEST.sha256; licences read at the file; loci verified by substring in the text layer, the Greek loci in the TEI's own code points; public-domain status checked against first publication and the editor's death. No text corrected by hand. The builders and this body are under rebuild/corpora/ea-corpora-34/.\n",
    "### Falsification Conditions\n\nA seat is falsified if its files do not verify against its MANIFEST.sha256 at the canonical URL; if a verified locus is absent from the text layer it names; if a work is misattributed, misdated or assigned to the wrong edition; if a licence recorded for an item is not the one its source states; if a work seated as public domain is not, in the jurisdiction stated; or if the four surfaces (seat, index, deposit, shelf) disagree.\n",
    f"### Body\n\n{body}",
    "### Terms\n\n- [x] I read the deposit protocol at https://alexanarch.org/api/deposit-protocol.json\n- [x] I confirm this work is deposited under the stated license\n- [x] I confirm the substrate disclosure is accurate\n- [x] I understand that deposited content will NOT be used to train enforcement classifiers\n"])
out = ROOT / "data/issue-bodies/EA-CORPORA-34-issue.md"
out.write_text(issue, encoding="utf-8")
print(out, len(body.split()), "words in body;", len(desc), "chars in description;", nw, "works;", tot, "lines;", nfiles, "files")
