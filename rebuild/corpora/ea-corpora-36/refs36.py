#!/usr/bin/env python3
"""EA-CORPORA-36 open scholarship held by reference: the modern scholarship on Sappho and the future reader that is free to read and in
copyright (or licensed for reading, not for the seat to carry). Each was fetched in session; the record keeps its URL, the SHA-256 and size of
the bytes as fetched, the rights statement as the source gives it, and short loci asserted present (whitespace-normalized) in the text read
from those bytes. Nothing is copied into the library. Works whose pages could be reached but whose text could not be fetched from the
session are entered as pointers with what was read.
    python3 rebuild/corpora/ea-corpora-36/refs36.py  -> rebuild/corpora/ea-corpora-36/refs36.json"""
import hashlib, html, json, pathlib, re, subprocess
H = pathlib.Path(__file__).resolve().parent
W = pathlib.Path("/tmp/claude-0/-home-claude/97be5201-55d8-50c9-b9d9-c76c8dde5ac6/scratchpad/ea36/web")
FETCHED = "2026-11-07"
norm = lambda s: " ".join(s.split())


def text_of(p):
    if p.suffix == ".pdf":
        return subprocess.run(["pdftotext", "-layout", str(p), "-"], capture_output=True, text=True).stdout
    t = p.read_text(encoding="utf-8", errors="replace")
    t = re.sub(r"<script.*?</script>|<style.*?</style>", "", t, flags=re.S)
    return html.unescape(re.sub(r"<[^>]+>", " ", t))


R = [
 {"work": "A. D'Angour, 'Love's Battlefield: Rethinking Sappho Fragment 31', in E. Sanders, C. Thumiger, C. Carey and N. J. Lowe (eds.), Erôs in Ancient Greece (Oxford, 2013), 59–71: the author's corrected proof",
  "url": "https://www.armand-dangour.com/wp-content/uploads/2018/02/Loves-Battlefield-.pdf", "file": "dangour2013.pdf",
  "rights": "Oxford University Press; posted by the author ('OUP CORRECTED PROOF – FINAL, 11/1/2013' on each page). Held by reference.",
  "loci": [("the continuation proposed", "one might now envisage a continuation of the poem on the following lines:"),
           ("Fränkel on τόλματον", "Hermann Fränkel long ago noted that this is a mistranslation: ‘must be endured’ would be"),
           ("D'Angour beyond Fränkel: 'all can be dared'", "properly means something like ‘all can be dared’ (hence my translation, above, ‘all is worth the risk’)"),
           ("Catullus as witness to the lost stanza", "Catullus in fact preserves the last two lines of Sappho’s lost stanza with some degree of ﬁdelity")]},
 {"work": "A. D'Angour, 'Sappho 31 & Catullus', Antigone (January 2023)",
  "url": "https://antigonejournal.com/2023/01/sappho-31-catullus/", "file": "antigone.html",
  "rights": "Antigone (antigonejournal.com), free to read; the author's copyright. Held by reference.",
  "loci": [("the continuation conjectured for a general readership", "it might be possible to conjecture how the song continued, starting with the surviving words of the fifth stanza: But all is worth the risk, since…")]},
 {"work": "P. J. Finglass, 'Getting Sweaty with Sappho: New College MS 298', New College Notes 24.1 (2025)",
  "url": "https://www.new.ox.ac.uk/sites/default/files/2025-12/24NCN1%20%282025%29%20Finglass%20on%20Sappho.pdf", "file": "finglass2025.pdf",
  "rights": "New College, Oxford, free to read; the author's copyright. Held by reference.",
  "loci": [("the sole manuscript and its folios", "whose sole manuscript is Parisinus gr. 2036 (where the text appears at ff. 184r–184v), quotes the first four stanzas and the beginning of the fifth"),
           ("Finglass's translation of the line", "But everything is endurable, since †even a poor man†"),
           ("the obelus explained", "the obelus, †, indicates the extent of a phrase deemed impossibly corrupt")]},
 {"work": "R. S. Garner, 'Oral Tradition and Sappho', Oral Tradition 26.2 (2011), 413–44",
  "url": "https://journal.oraltradition.org/wp-content/uploads/files/articles/26ii/10_26.2.pdf", "file": "garner2011.pdf",
  "rights": "Oral Tradition (Center for Studies in Oral Tradition), free to read; no licence stated in the file. Held by reference.",
  "loci": [("the point at which writing entered", "now impossible to determine at exactly what point writing entered into the composition or transmission of Sappho’s poetry"),
           ("Gerber (1997: 3–4) on contemporary copies, as Garner quotes it", "it seems difficult to believe that contemporary copies of lyric poetry did not exist, especially for longer poems.")]},
 {"work": "J. J. O'Donnell, review of J. Svenbro, Phrasikleia: An Anthropology of Reading in Ancient Greece (Ithaca, 1993), BMCR 1994.02.03",
  "url": "https://bmcr.brynmawr.edu/1994/1994.02.03/", "file": "bmcr1.html",
  "rights": "Bryn Mawr Classical Review, free to read; no licence stated on the page. Held by reference.",
  "loci": [("Svenbro's fr. 31: the 'you' as the poem itself", "Svenbro reads Sappho frg. 31, for example, as evoking a “you” who is not some woman of whom S. is jealous but indeed the poem itself, the poem that speaks to the lover and endures the lover’s gaze.")]},
 {"work": "Review of E. A. Mackay (ed.), Orality, Literacy, Memory in the Ancient Greek and Roman World (Leiden, 2008), BMCR 2009.04.41",
  "url": "https://bmcr.brynmawr.edu/2009/2009.04.41/", "file": "bmcr2009.html",
  "rights": "Bryn Mawr Classical Review, free to read; no licence stated on the page. Held by reference.",
  "loci": [("the review's account of Lardinois 2008", "André Lardinois argues that Sappho’s main interest was to know of the performance of her poetry in the future and to imagine herself to be a singer-poet after death")]},
 {"work": "G. Liberman, review of D. Yatromanolakis, Sappho in the Making: The Early Reception (Washington, DC, 2007), BMCR 2008.12.13",
  "url": "https://bmcr.brynmawr.edu/2008/2008.12.13/", "file": "bmcr2008.html",
  "rights": "Bryn Mawr Classical Review, free to read; no licence stated on the page. Held by reference.",
  "loci": [("the review on the book's model of Sappho's company", "Yatromanolakis n’emploie jamais, certainement à dessein")]},
]
P = [
 {"work": "A. Lardinois, '\"Someone, I Say, Will Remember Us\": Oral Memory in Sappho's Poetry', in E. A. Mackay (ed.), Orality, Literacy, Memory in the Ancient Greek and Roman World (Leiden, 2008), 79–96",
  "url": "https://hdl.handle.net/2066/68171", "rights": "Brill; the publisher's version is open in the Radboud University repository.",
  "status": "The repository answered 403 to the session; the PDF was read and pinned on 2026-08-26 (#1548 §10), where pp. 79–80 and the closing sentence are quoted. The Wikipedia sentence seated at 36/23 cites it."},
 {"work": "D. Yatromanolakis, Sappho in the Making: The Early Reception, Hellenic Studies 28 (Washington, DC, 2007)",
  "url": "https://chs.harvard.edu/book/yatromanolakis-dimitrios-sappho-in-the-making-the-early-reception/",
  "rights": "Center for Hellenic Studies online edition; the page states 'This work is licensed under a Creative Commons 3.0 License' and links CC BY 3.0.",
  "status": "The book page was fetched in session and its licence read; the chapters are delivered by script and did not reach the session, so the text is not seated. Open to a later seating under its licence."},
 {"work": "E. Greene and M. B. Skinner (eds.), The New Sappho on Old Age: Textual and Philosophical Issues, Hellenic Studies 38 (Washington, DC, 2009), with E. Stehle's chapter on 'once' and 'now'",
  "url": "https://chs.harvard.edu/book/ellen-greene-and-marilyn-skinner-eds-the-new-sappho-on-old-age-textual-and-philosophical-issues/",
  "rights": "Center for Hellenic Studies online edition; the page states 'This work is licensed under a Creative Commons 3.0 License' and links CC BY 3.0.",
  "status": "The book page was fetched in session and its licence read; the chapters are delivered by script and did not reach the session. Open to a later seating under its licence."},
 {"work": "C. Calame, Choruses of Young Women in Ancient Greece, trans. D. Collins and J. Orion (Lanham, 1997; CHS online 2001)",
  "url": "https://chs.harvard.edu/book/calame-claude-choruses-of-young-women-in-ancient-greece/",
  "rights": "Center for Hellenic Studies online edition; the page states 'This work is licensed under a Creative Commons 3.0 License' and links CC BY 3.0.",
  "status": "The book page was fetched in session; the chapters did not reach the session. The choral reading Lardinois 2008 builds on (#1548 §2)."},
 {"work": "R. Travis, The Descent of the Goddess: Ritual and Difference in Sappho's Prayer to Aphrodite (1990; CHS online)",
  "url": "https://chs.harvard.edu/book/travis-roger-the-descent-of-the-goddess-ritual-and-difference-in-sapphos-prayer-to-aphrodite/",
  "rights": "The page states 'Copyright, Roger Travis. Published here with permission of the author.'",
  "status": "The book page was fetched in session; the text did not reach the session."},
 {"work": "A. Bierl and A. Lardinois (eds.), The Newest Sappho: P. Sapph. Obbink and P. GC inv. 105, frs. 1–4, Mnemosyne Supplements 392 (Leiden, 2016), with E. Bowie's chapter on sympotic reperformance",
  "url": "https://edoc.unibas.ch/52685/", "rights": "Open access; the University of Basel repository record gives its licence as CC_BY_NC.",
  "status": "The repository record was fetched in session; the PDF is served behind a script page and did not reach the session (the OAPEN and DOAB records answered 403). Open to a later seating under its licence, carried unmodified under the NC payload/record split of EA-CORPORA-02."},
]
out = []
for r in R:
    p = W / r["file"]; b = p.read_bytes(); t = norm(text_of(p))
    for lab, f in r["loci"]:
        assert norm(f) in t, (r["file"], f)
    out.append({"work": r["work"], "url": r["url"], "fetched": FETCHED, "sha256_as_fetched": hashlib.sha256(b).hexdigest(), "bytes": len(b),
                "rights": r["rights"], "verified_loci": [f"{lab} — '{f}'" for lab, f in r["loci"]], "held": "by reference"})
    print("ok", r["file"], len(r["loci"]))
for x in P:
    out.append(dict(x, held="pointer"))
(H / "refs36.json").write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(len(R), "held by reference;", len(P), "pointers")
