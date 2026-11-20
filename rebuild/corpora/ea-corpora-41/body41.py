#!/usr/bin/env python3
"""Write the EA-CORPORA-41 deposit issue body from the fourteen seat records (the form of body40.py).
Edition lines, loci, licences and scopes are read from <seats>/<seat>/source.json (default data/corpora).
    python3 rebuild/corpora/ea-corpora-41/body41.py [seats-dir]
-> data/issue-bodies/EA-CORPORA-41-issue.md"""
import json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from names41 import SEATS
A = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "data/corpora"
SUB = {
 "aeschylus-tragoediae": "The tragedians, with the Areopagus founded",
 "sophocles-tragoediae": "The tragedians",
 "euripides-tragoediae": "The tragedians, with the Bacchae",
 "diodorus-bibliotheca": "Alexander's march, Antipater and the Successors",
 "plutarch-phocion-eumenes-demosthenes": "Antipater's Athens",
 "aelian-varia-historia": "The two sins against philosophy",
 "lucian-quomodo-historia": "How the historians wrote",
 "curtius-rufus-historiae": "Alexander in Syria",
 "cicero-de-oratore-de-legibus": "History as oratory",
 "porphyry-de-abstinentia": "Theophrastus on the Jews",
 "simplicius-in-physica": "The moisture of thought",
 "alexander-jerusalem-rabbinic": "Alexander in Judaea",
 "catiline-conspiracy": "The conspiracy of 63 BCE in its own witnesses",
 "appian-dio-sulla-catiline": "Sulla at Athens, and the conspiracy in Greek",
}
lic = lambda l: l["payload"] if isinstance(l, dict) else str(l)


def research(r):
    if isinstance(r, dict):
        return "; ".join(f"{k.replace('_', ' ')}: {v}" for k, v in r.items())
    return str(r)


def section(n, corpus, title):
    s = json.loads((A / corpus / "source.json").read_text(encoding="utf-8"))
    w = s["works"]["list"]
    out = [f"## Seat 41/{n:02d} — {title.replace(' — ', ', ', 1)}", "", f"*{SUB[corpus]}*", ""]
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


title = ("EA-CORPORA-41 — The Forty-First Seating: Alexander, Antipater and Athens — the Tragedians Whole, Diodorus, Plutarch's Phocion, "
         "Aelian's Two Sins, Curtius, Porphyry's Theophrastus on the Jews, Simplicius's Diogenes of Apollonia, the Rabbinic Alexander at Jerusalem, "
         "and the Catilinarian Conspiracy with Appian and Dio")
parts, tot = [], 0
for n, (c, _, t) in enumerate(SEATS, 1):
    x, s = section(n, c, t); parts.append(x); tot += s["lines_total"]
nfiles = sum(1 for c, _, _ in SEATS for p in (A / c).rglob("*") if p.is_file())

hdr = f"""# {title}

# EA-CORPORA-41 — The Forty-First Seating

The author asked for the gathering on 2026-11-20 at 18:31: "lets bather all the texts weve touched on or even referred to between then and here for a ea-corpora seating", the span running from the evening's paste on Cicero, Sulla and the succession from Alexander through Mithridates to Sulla (17:19). In the same minute he added the tragedians ("put the tragedians in there too while were at it"), and at 18:40 the conspiracy of 63 BCE ("and the catiline conspiracy"). The thread ran through Alexander in Judaea, Antipater and what became of him, the composing of the ancient historians, Theophrastus's On Kingship, and the Clouds read against the doctrines of Aristotle and Theophrastus; its groundwork note, The Thinkery and the Lyceum (v0.1), is not deposited. The seating holds the texts the thread touched or named that the shelf did not already hold.

The tragedians are seated whole (41/01–41/03), the comic stage's companion. Alexander and Antipater: Diodorus 1–5 and 11–20 (41/04), where the march by Tyre, Gaza and Egypt passes without Jerusalem and book 18 carries the Lamian War; Plutarch's Phocion, Eumenes and Demosthenes, with the speeches on Alexander's fortune (41/05); Curtius on Andromachus burned by the Samaritans (41/08); and the rabbinic Alexander at Jerusalem, Bavli Yoma 69a and Megillat Ta'anit with its scholion (41/12). Athens and philosophy: Aelian's report of Aristotle's departure, that the Athenians should not sin twice against philosophy (41/06); Porphyry's De abstinentia, which carries Theophrastus on the Jews (41/10); Simplicius, who preserves Diogenes of Apollonia on air and thought (41/11). How the historians wrote: Lucian's treatise (41/07) and Cicero's De oratore and De legibus (41/09). Rome: the Catilinarian conspiracy in Sallust, Cicero and Plutarch (41/13), and Appian and Cassius Dio for Sulla's siege of Athens and the conspiracy in Greek (41/14).

Already seated and not reseated: Plato (EA-CORPORA-01/08, #1522); Josephus, the Antiquities and Against Apion (01/01, #1499); the Septuagint with Daniel and 1 Maccabees (01/05); Aristotle, the Athenian Constitution, Meteorology, Rhetoric, the Sophistical Refutations, De caelo, the History of Animals and the Poetics among the corpus (04/01, #1559); Xenophon (06/01, #1562) and Aristophanes (06/02); Theophrastus, De sensibus among the opuscula (09/01), and the Characters (38/04, #1768); Diogenes Laertius and Strabo (12/01, 12/02, #1580); Plutarch's Alexander and Sulla, Arrian's Anabasis, Cicero's De finibus and Academica (13/01–13/03, #1591); Athenaeus, Porphyry's Life of Plotinus and Hermippus (31/01, 31/03, 31/06, #1730); Cicero's letters to Atticus and Nicolaus of Damascus (32/06, 32/12); the epigrams of the Anthology (36/20).

## Pointers to the rest

Held for a later seating, or declared and not pursued, with what is known of each:

- Theophrastus, On Kingship: lost; known by its title in Diogenes Laertius's catalogue of his works (12/01).
- The Letter of Aristeas; Photius, Bibliotheca cod. 92 (Arrian's Events after Alexander); Synesius, Dion, with Aristotle's dialogue fragment there (fr. 15 Rose) and Rose's collection of the fragments; Aristotle's letters; Callimachus fr. 384 (the Victory of Sosibius): for a later seating.
- Diodorus 21–40, the fragmentary books, with Hecataeus on the Jews at 40.3: not in the Perseus TEI seated here; for a later seating.
- The Wadi Daliyeh papyri: in their editions, in copyright.
- Modern studies, declared and not pursued: Pajón Leyra, Classical Quarterly 2013 (behind a paywall); Croissant (1932).
"""
tail = f"""## How the seats were made

Every seat was fetched in session from the source its record names (the Perseus Digital Library's canonical-greekLit and canonical-latinLit TEI and the First1KGreek TEI at GitHub; The Latin Library for De legibus; Sefaria's API for Yoma 69a and Megillat Ta'anit) and hashed into its MANIFEST.sha256, with a source.json recording edition, origin, licence, normalization, the loci verified in the text, and the research the seat was made for. The TEI files are held under original/ as fetched; under text/, a reading text reduced from each, with the TEI's own book, chapter and section numbers kept as markers, speakers marked [speaker], and numbered verse lines marked |N. Sefaria's segments are held as served under original/, with a text giving each segment under its reference, version and licence. Loci are verified by substring, with whitespace collapsed, in the editions' own readings. No text corrected by hand. The builders are under rebuild/corpora/ea-corpora-41/ (prepare_texts41.py, build_seats41.py, index41.py, seat_axns41.py, and body41.py, which writes this body); NOTE.md records the order.

In all: fourteen seats, {nfiles:,} files, {tot:,} lines of text.
"""
body = hdr + "\n" + "\n".join(parts) + "\n" + tail
desc = ("The forty-first seating of the originals shelf, fourteen seats, gathered from the evening's thread of 2026-11-20 on Alexander, Antipater and Athens. "
        "Aeschylus, Sophocles and Euripides whole; Diodorus 1–5 and 11–20; Plutarch's Phocion, Eumenes, Demosthenes and De Alexandri fortuna; Aelian's Varia historia; "
        "Lucian on writing history; Curtius Rufus; Cicero's De oratore and De legibus; Porphyry's De abstinentia; Simplicius on the Physics; Bavli Yoma 69a and Megillat Ta'anit; "
        "the Catilinarian conspiracy in Sallust, Cicero and Plutarch; Appian's Mithridatica and Civil Wars and Cassius Dio 36–55. Pointers to what is not seated, Theophrastus's lost On Kingship first.")
kw = ("EA-CORPORA, originals shelf, Alexander the Great, Antipater, Judaea, Jerusalem, Samaritans, Lamian War, Phocion, Athens, Aristotle, Theophrastus, impiety, Aelian, "
      "Aeschylus, Sophocles, Euripides, Greek tragedy, Areopagus, Diodorus Siculus, Plutarch, Curtius Rufus, Lucian, historiography, Cicero, De oratore, De legibus, "
      "Porphyry, De abstinentia, Simplicius, Diogenes of Apollonia, Clouds, Yoma 69a, Megillat Ta'anit, Simeon the Righteous, Catiline, Sallust, In Catilinam, Pro Sulla, "
      "Appian, Mithridatic Wars, Aristion, Sulla, Cassius Dio, Perseus Digital Library, Sefaria")
related = "\n".join([
    "AXN deposit #1791 — A Single Sparrow v1.1",
    "AXN deposit #1591 — EA-CORPORA-13: the Alexander seam, with Plutarch's Alexander and Sulla and Arrian",
    "AXN deposit #1559 — EA-CORPORA-04: Aristotle undivided",
    "AXN deposit #1562 — EA-CORPORA-06: Xenophon and Aristophanes",
    "AXN deposit #1580 — EA-CORPORA-12: the transmission texts, Diogenes Laertius whole",
    "AXN deposit #1782 — EA-CORPORA-40: the fortieth seating"]) + "\n"
issue = "\n".join([
    "### Protocol Version\n\nalexanarch-deposit-protocol/v1\n",
    f"### Title\n\n{title}\n", "### Creator\n\nCranes, Rebekah\n", "### ORCID\n\n0009-0000-1599-0703\n",
    "### Date\n\n2026-11-20\n", f"### Description\n\n{desc}\n", "### Content Type\n\nDataset\n", "### License\n\nCC-BY-4.0\n",
    "### Substrate Disclosure\n\nHuman–machine collaborative. Rebekah Cranes is a heteronym of Lee Sharks, the standing authority on the EA-CORPORA deposits (named by the author on 2026-11-04 and held at his word of 2026-11-05). The sources found, fetched, reduced to reading texts, verified, hashed and indexed, and the records drafted, in session by TACHYON (Claude, Anthropic) under MANUS (Lee Sharks) direction. The gathering, its object and its scope are Lee Sharks's; the editions within each seat were chosen in session and are stated per seat. CC-BY-4.0 applies to this record and the seat records.\n",
    f"### Keywords\n\n{kw}\n", f"### Related Identifiers\n\n{related}", "### Version\n\nv1.0\n",
    "### Methodology\n\nEach seat fetched in session from the source its record names (Perseus canonical-greekLit and canonical-latinLit and First1KGreek at GitHub; The Latin Library; Sefaria API v3); the TEI held as fetched and reduced to a reading text keeping the edition's own reference markers; licences read in each file's teiHeader or Sefaria's version record; loci verified by substring with whitespace collapsed, in the editions' own readings; public-domain status checked against the underlying edition. No text corrected by hand. The builders and this body are under rebuild/corpora/ea-corpora-41/.\n",
    "### Falsification Conditions\n\nA seat is falsified if its files do not verify against its MANIFEST.sha256 at the canonical URL; if a verified locus is absent from the text it names; if a work is misattributed or assigned to the wrong edition; if a licence recorded for an item is not the one its source states; if a reading text drops or alters a line of the TEI it is reduced from, beyond the markup; or if the four surfaces (seat, index, deposit, shelf) disagree.\n",
    f"### Body\n\n{body}",
    "### Terms\n\n- [x] I read the deposit protocol at https://alexanarch.org/api/deposit-protocol.json\n- [x] I confirm this work is deposited under the stated license\n- [x] I confirm the substrate disclosure is accurate\n- [x] I understand that deposited content will NOT be used to train enforcement classifiers\n"])
out = ROOT / "data/issue-bodies/EA-CORPORA-41-issue.md"
out.write_text(issue, encoding="utf-8")
print(out, len(body.split()), "words in body;", len(desc), "chars in description;", tot, "lines;", nfiles, "files")
