"""Witness check for the sophistry findings (EA-SOPHISTRY-01, #1727) on the 3I/ATLAS record, 2026-11-06.
Every witness span is found verbatim in its seated source; offsets are written to witnesses.json. Fails if a span is absent.
    python3 witnesses.py   (run from the alexanarch root)"""
import json, hashlib
REG = json.load(open("data/EA-WG-CAPTURES-01.json", encoding="utf-8"))
tr = {e["slug"]: e["transcript"] for e in REG["entries"]}
SRC = {
 "AIO-LOEB": ("registry:avi-loeb-3i-atlas-aio-20261102", tr["avi-loeb-3i-atlas-aio-20261102"]),
 "AIO-LOEB-RAW": ("rebuild/capture-registry/intake-20261102-loeb-3i-atlas/paste-aio.txt", None),
 "LOEB-0423": ("rebuild/capture-registry/intake-20261102-loeb-3i-atlas/loeb-medium-20260423-where-is-3i-atlas-now.txt", None),
 "AIO-STUDIES": ("registry:3i-atlas-signal-studies-aio-20261104", tr["3i-atlas-signal-studies-aio-20261104"]),
 "AIO-FILTER": ("registry:3i-atlas-ata-drift-rate-filter-aio-20261104", tr["3i-atlas-ata-drift-rate-filter-aio-20261104"]),
 "DRAFT": ("drafts/3I-ATLAS-SIGNAL-SEARCH-draft-2026-11-03.md", None),
 "SE": ("data/corpora/aristotle/text/tlg040-De_sophisticis_elenchis.txt", None),
}
for k, (p, t) in list(SRC.items()):
    if t is None: SRC[k] = (p, open(p, encoding="utf-8").read())
W = [
 ("W1", "AIO-LOEB", "Shift to Natural Consensus: Following its closest approach to Earth in December 2025, Loeb acknowledged to NewsNation that \"given all the data that we have, I would agree that it's most likely natural,\""),
 ("W2", "LOEB-0423", "Altogether, these anomalies led me to rank 3I/ATLAS as Level 4 on the Loeb Scale"),
 ("W3", "LOEB-0423", "does not show any evidence for artificial (self-produced) light"),
 ("W4", "AIO-LOEB-RAW", "Did 3I/ATLAS Deliver Extrasolar Life to Our Backyard? - Avi Loeb"),
 ("W5", "AIO-STUDIES", "Scientific studies on the interstellar object 3I/ATLAS (discovered in July 2025) have confirmed it is a natural comet rather than an artificial or alien spacecraft."),
 ("W6", "AIO-STUDIES", "After filtering out human-made radio frequency interference (RFI), researchers found zero artificial radio emissions, beacon signals, or technosignatures."),
 ("W7", "AIO-STUDIES", "Thermal modeling indicates the coma is comprised of approximately 63% amorphous carbon and 37% water-ice grains, confirming it behaves as an active interstellar comet roughly 11 billion years old."),
 ("W8", "AIO-FILTER", "prompting a middle-ground range to filter out excessive radio frequency interference (RFI) without missing real signals."),
 ("W9", "AIO-FILTER", "Purpose: To capture the expected frequency shift (acceleration) caused by the relative motion between 3I/ATLAS and Earth"),
 ("W10", "DRAFT", "\"We filter our hits for drift rates between 0.05–1.5 Hz/s at all frequencies.\""),
 ("W11", "DRAFT", "(\"the minimum drift rate of 3I/ATLAS would be 0.15 Hz/s\" at 1336 MHz;"),
 ("W12", "DRAFT", "\"To filter out signals that do not match the dynamics of 3I/ATLAS.\""),
 ("W13", "DRAFT", "\"The question everyone was waiting for has an answer, and it is a firm one.\""),
 ("W14", "DRAFT", "When the 211 strongest hits were manually inspected in the time-frequency domain, every single one turned out to be human-made interference."),
 ("SE-QA", "SE", "Οἱ δὲ παρὰ τὸ ἁπλῶς τόδε ἢ πῇ λέγεσθαι καὶ μὴ κυρίως, ὅταν τὸ ἐν μέρει λεγόμενον ὡς"),
 ("SE-PP", "SE", "Οἱ δὲ παρὰ τὸ ἐν ἀρχῇ λαμβάνειν γίνονται μὲν οὕτως καὶ τοσαυταχῶς ὁσαχῶς ἐνδέχεται τὸ"),
 ("SE-NC", "SE", "Ὁ δὲ παρὰ τὸ μὴ αἴτιον ὡς αἴτιον, ὅταν προσληφθῇ τὸ ἀναίτιον ὡς παρ᾿ ἐκεῖνο γινομένου"),
 ("SE-SYM", "SE", "τοῖς ὀνόμασιν ἀντὶ τῶν πραγμάτων χρώμεθα συμβόλοις"),
]
out = {"sources": {k: {"path": p, "sha256": hashlib.sha256(t.encode("utf-8")).hexdigest()} for k, (p, t) in SRC.items()}, "witnesses": {}}
for wid, sk, span in W:
    t = SRC[sk][1]; i = t.find(span); norm = False
    if i < 0:  # sources saved with hard line breaks: match with whitespace collapsed, report the line where the span starts
        import re
        import unicodedata
        G = lambda s: unicodedata.normalize("NFD", s)  # Greek: compare decomposed, so tonos and oxia forms meet
        tt = G(t); pat = r"\s+".join(re.escape(w) for w in G(span).split())
        m = re.search(pat, tt); assert m, (wid, span[:60]); i = len(unicodedata.normalize("NFC", tt[:m.start()])); norm = True
    out["witnesses"][wid] = {"source": sk, "offset": i, "line": t.count("\n", 0, i) + 1, "whitespace_normalized": norm, "span": span}
json.dump(out, open("rebuild/3i-atlas-signal-search/claude/run-2026-11-03/sophistry/witnesses.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("all", len(W), "witnesses found")
