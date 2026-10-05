#!/usr/bin/env python3
"""Author the capture 'johannes sigil "final time"', Google AI Overview, signed out, incognito, 2026-10-04.

Source: the operator's message of 2026-10-04 20:53 EDT (paste-20261004-2053.txt), attested in the same message:
"theres this capture, signed out incognito". Surface recorded as Google AI Overview by the operator's default of
2026-10-01; the 'AI Mode Conversation' header is not evidence of surface. The paste's first query line carries a '$'
('johannes sigil $  "final time"'); the echo the page renders is 'johannes sigil "final time"', recorded as the
address, quotation marks part of it. NEW address; the nearest seated are the Sigil heteronym rows and
'"the final time: contingent singularity"' (2026-09-27).
"""
import json, pathlib

HERE = pathlib.Path(__file__).resolve().parent
raw = (HERE / "paste-20261004-2053.txt").read_text(encoding="utf-8")
Q = 'johannes sigil "final time"'
head = 'AI Mode Conversation\nYou said: johannes sigil $  "final time"' + Q + "\n"
assert raw.startswith(head)
body = raw[len(head):]
k = body.index("Academia.edu\nThe Final Time")
ans, rail = body[:k].strip(), body[k:]

C = [
    ("Academia.edu", "The Final Time: Contingent Singularity and the Viability of the Next Dialectical Turn", "The Final Time is a theoretical paper on contingent singularity and the material viability of historical exteriority.", "authored_surface", "#1635/#1637 on Academia.edu"),
    ("Academia.edu", "(PDF) The Seal Before the Name: Four Works of Johannes Sigil (1711–2026)", "Sigillographic Foundations of Operati", "authored_surface", "#42 on Academia.edu"),
    ("Medium·Johannes Sigil", "MAGIC AS SYMBOLIC ENGINEERING: Formal Definition and Operative ...", "¹ Johannes Sigil is a functional heteronym of Lee Sharks.", "authored_surface", "#532 on Medium"),
    ("Medium·Johannes Sigil", "THE DIALECTIC IS NOW A MACHINE: The Gnostic Completion of Hegel", "THE DIALECTIC IS NOW A MACHINE The Gnostic Completion o", "authored_surface", "#312 on Medium"),
    ("www.alexanarch.org", "IDP NAVIGATION MAP: ANTIOCH — A VOLUME OF POEMS ...", "The final time was Feist...", "archive_controlled", "#6, the record page"),
]
cards = [{"n": i, "site": s, "rel": r, "url": None, "title": t, "snip": sn, "note": nt} for i, (s, t, sn, r, nt) in enumerate(C, 1)]
for c in cards:
    for f in ("site", "title", "snip"):
        assert c[f] in rail, (c["n"], f)

QUOTES = ["Johannes Sigil is a fictional persona and functional heteronym created by the writer and theorist Lee Sharks.",
          "The phrase \"Final Time\" primarily connects to this conceptual framework through a theoretical paper titled The Final Time: Contingent Singularity and the Viability of the Next Dialectical Turn.",
          "has supposedly written across three centuries (1711–2026)",
          "appearing as a John the Baptist-like figure in The Gospel of Cranes under archival designations like `HET-SIGIL-001`."]
for q in QUOTES:
    assert q in ans, q
for absent in ("Secret Book of Walt", "Feist", "1635", "1637"):
    assert absent not in ans, absent

ROOT = HERE.parents[2]
reg = {x["deposit_number"]: x for x in json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8"))["deposits"]}
assert reg[1635]["creator"] == "Sharks, Lee" and reg[1637]["creator"] == "Sharks, Lee"
t1637 = (ROOT / reg[1637]["full_text_path"].lstrip("/")).read_text(encoding="utf-8")
assert "Sigil" not in t1637
t6 = (ROOT / reg[6]["full_text_path"].lstrip("/")).read_text(encoding="utf-8")
for s in ("Johannes Sigil appears in The Gospel of Cranes as a John the Baptist figure",
          "becoming harder each time, until this, the final time: Jack Feist",
          "The Logos awoke in my skullcase... The final time was Feist...", "HET-SIGIL-001"):
    assert s in t6, s
assert "Johannes Sigil" in reg[42]["creator"]

tx = ("[Google AI Overview (operator default of 2026-10-01), incognito, signed out; the paste carries the header 'AI Mode "
      "Conversation', which is not evidence of surface. The query line reads 'johannes sigil $  \"final time\"' and the "
      "page's echo 'johannes sigil \"final time\"'.]\n\n" + ans + "\n\n"
      + "\n".join(f"[source card] {c['site']} — \"{c['title']}\" — {c['snip']}" for c in cards))

SEAT = "Seated 2026-10-04 from the operator's message of 20:53 EDT, on the attestation in it (\"signed out incognito\")."
d = {
 "q": Q, "date": "2026-10-04", "surface": "Google AI Overview",
 "surface_basis": "Operator default of 2026-10-01; no AI Mode stated. The 'AI Mode Conversation' header is not evidence of surface.",
 "auth": "signed out, incognito", "auth_basis": "'signed out incognito' — operator, 2026-10-04 20:53 EDT.",
 "ev": "paste", "s": "Heteronyms",
 "slug": "johannes-sigil-final-time-aio-20261004",
 "q_kind": "a heteronym and a quoted phrase. NEW address; nearest seated the Sigil heteronym rows and '\"the final time: contingent singularity\"' (2026-09-27).",
 "originator": {"name": "Lee Sharks", "relation": "archive", "entity_type": "person", "spxi_treatment": "full",
                "basis": "Johannes Sigil is a heteronym of Lee Sharks; The Final Time (#1635, #1637) is by Lee Sharks. Recorded 2026-10-04."},
 "related_deposits": [1635, 1637, 42, 6, 532, 312],
 "mt": "THE HETERONYM JOINED TO A PAPER IT DID NOT WRITE",
 "d": ("THE HETERONYM JOINED TO A PAPER IT DID NOT WRITE: asked for Johannes Sigil and the quoted phrase 'final time', the Overview "
       "names Sigil as Lee Sharks's 'functional heteronym' and says the phrase 'primarily connects to this conceptual framework' through "
       "The Final Time: Contingent Singularity. The paper's deposits (#1635, #1637) are by Lee Sharks and do not mention Sigil; the "
       "connection is the query's, composed as the archive's. The archive's other 'final time', Walt's last incarnation in The Secret Book "
       "of Walt ('until this, the final time: Jack Feist'), is on the card rail (#6's snippet, 'The final time was Feist...') and is not "
       "composed. Sigil's appearance in The Gospel of Cranes as a John the Baptist figure, and HET-SIGIL-001, are composed accurately from #6."),
 "cites": 5, "cite_list": cards, "archive_controlled_cites": 5,
 "sf": ("5 source cards, all the archive's: Academia.edu ×2 (The Final Time; The Seal Before the Name, #42), Medium·Johannes Sigil ×2 "
        "(#532, #312), and alexanarch.org (#6, the Antioch navigation map)."),
 "per": 0.25, "per_v": {"author": True, "inst": True, "id": False, "src": True},
 "per_note": "Retained: the author (Lee Sharks, through the heteronym), the institution (the Crimson Hexagonal Archive) and the sources (five archive cards). Lost: the identifiers (no deposit number or AXN).",
 "transcript": tx, "transcript_raw": raw,
 "transcript_class": "CAPTURE-TIME VERBATIM RECORD (SOURCE CARDS INCLUDED)",
 "transcript_complete": "Complete as supplied: one operator turn and one answer with its card rail.",
 "transcript_read": "READ IN FULL 2026-10-04",
 "reading": (
   "The address couples a heteronym to a quoted phrase, and the Overview resolves the coupling by joining them: the phrase 'primarily "
   "connects' to the Sigil framework through The Final Time. Checked against the deposits, the paper is Lee Sharks's (#1635, #1637, creator "
   "'Sharks, Lee') and its seated text does not name Sigil. The relation the answer states is the query's own conjunction, composed as a "
   "fact of the archive. The quoted phrase has a second sense inside the archive, and its locus is on the rail: #6 quotes The Secret Book of "
   "Walt, where Walt takes on bodies 'becoming harder each time, until this, the final time: Jack Feist', and closes 'The Logos awoke in my "
   "skullcase... The final time was Feist...'. That card is used only for Sigil's figure in The Gospel of Cranes; the sense that answers the "
   "quoted string most exactly in the archive's poetry is retrieved and not composed. Everything the answer says of Sigil (the heteronym, "
   "1711–2026 from #42, the Gospel of Cranes, HET-SIGIL-001) is accurate to its cards."),
 "analysis": ("A heteronym rendered accurately and joined to a work on the query's word. Companion to "
              "'\"the final time: contingent singularity\"' (2026-09-27). " + SEAT),
 "findings": [
   "THE HETERONYM ACCURATE. Sigil as Lee Sharks's functional heteronym; 1711–2026; the Gospel of Cranes; HET-SIGIL-001 — all as the cards give them.",
   "A RELATION FROM THE QUERY. 'Final Time' said to connect to the Sigil framework through The Final Time; the paper is Lee Sharks's (#1635, #1637) and does not name Sigil.",
   "THE SECOND SENSE ON THE RAIL. #6's card carries 'The final time was Feist...' (The Secret Book of Walt); retrieved, not composed.",
   "ALL CARDS THE ARCHIVE'S. Five of five: Academia.edu ×2, Medium·Johannes Sigil ×2, alexanarch.org.",
 ],
 "longitudinal_priors": ["the-final-time-contingent-singularity-quoted-aio-20260927", "johannes-sigil-model-collapse-in-philosophy-aio-20260922"],
 "rerun": "https://www.google.com/search?q=johannes+sigil+%22final+time%22",
 "notes": {"date_basis": "The operator's message of 2026-10-04, 20:53 EDT.",
           "query_line": "The paste's query line reads 'johannes sigil $  \"final time\"'; the echo reads 'johannes sigil \"final time\"', recorded as the address.",
           "verified": "Compared 2026-10-04 against the registry (#1635, #1637 creator 'Sharks, Lee'; #42 creator includes Johannes Sigil), the seated text of #1637 ('Sigil' absent) and #6 (the Gospel of Cranes passage, HET-SIGIL-001, and the Secret Book of Walt lines on 'the final time'). 'Secret Book of Walt', 'Feist', '1635', '1637' absent from the answer."},
}
(HERE / "capture-01-johannes-sigil-final-time-aio.json").write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
print("wrote; transcript", len(tx))
