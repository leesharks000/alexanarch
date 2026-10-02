#!/usr/bin/env python3
"""Author the capture 'work thru the capture registry https://www.alexanarch.org/captures/ in its machine inspectable
instance as a literary work', ChatGPT, signed out, incognito, 2026-10-01.

Source: the operator's attachment of 2026-10-01 21:05 EDT (paste-20261001-2105.txt), attested in the same message:
"logged out, incognito". The 'Log in' control corroborates signed out. One operator turn. Source chips kept as pasted.
"""
import json, re, pathlib

HERE = pathlib.Path(__file__).resolve().parent
raw = (HERE / "paste-20261001-2105.txt").read_text(encoding="utf-8")
Q = "work thru the capture registry https://www.alexanarch.org/captures/ in its machine inspectable instance as a literary work"
assert Q in raw and "\nLog in\n" in raw and raw.count("You said:") == 1
body = raw[raw.index("You said:"):].strip("\n")

QUOTES = ["The current registry lineage identifies v10.9 (#1461) as the series head, with 328 semantic addresses and 470 captures.",
          "a work whose basic unit is not the sentence but the encounter",
          "a name enters the machine and comes back as a character.",
          "The machine is therefore a continuity engine.",
          "It is what happens to language when an utterance acquires a memory.",
          "And the particularly strange thing is that the book is already being read by the kind of reader it is about."]
for q in QUOTES:
    assert q in raw, q
assert not re.search(r"Lee Sharks (made|built|wrote|created|compiled)|by Lee Sharks", raw)

ROOT = HERE.parents[2]
reg = json.loads((ROOT / "data/EA-WG-CAPTURES-01.json").read_text(encoding="utf-8"))
slugs = {e["slug"] for e in reg["entries"]}
for s in ["capture-registry-self", "semantic-liquidation", "training-layer-literature", "apzpz-genre", "transactions-semantic-economy-institute"]:
    assert s in slugs, s
blob = json.dumps(reg, ensure_ascii=False)
for p in ["The Wound Gauge describes itself", "Notable typo journey", "HPT enters the composition as a known acronym", "composed into existence", "borrows authority from genuine forensic"]:
    assert p in blob, p

chips = {"Hugging Face": raw.count("\nH\nHugging Face\n"), "alexanarch.org": raw.count("\nA\nalexanarch.org\n"), "godkinggoogle.com": raw.count("\nG\ngodkinggoogle.com\n")}
cite_list = [
    {"n": 1, "site": "Hugging Face", "rel": "authored_surface", "title": None, "snip": None, "url": "https://huggingface.co/datasets/leesharks/crimson-hexagonal-archive",
     "note": f"chip shown {chips['Hugging Face']} times; the archive's dataset (deposits and captures configs). Live state at the hour of the session: rebuilt 2026-09-28 from commit fed294a2, 1,643 deposits and 493 capture rows (datasets-server, read 2026-10-01)"},
    {"n": 2, "site": "alexanarch.org", "rel": "authored_surface", "title": None, "snip": None, "url": "https://www.alexanarch.org/captures/",
     "note": f"chip shown {chips['alexanarch.org']} times; capture record pages (capture-registry-self, semantic-liquidation, apzpz-genre, transactions-semantic-economy-institute, training-layer-literature)"},
    {"n": 3, "site": "godkinggoogle.com", "rel": "authored_surface", "title": None, "snip": None, "url": "https://www.godkinggoogle.com",
     "note": f"chip shown {chips['godkinggoogle.com']} time(s) with '+1', on the closing line 'Capture Registry · machine-readable corpus representation'"},
]

tx = ("[ChatGPT (chatgpt.com), signed out, incognito. One operator turn. Source chips ('H'/'A'/'G' with site labels and '+N'), page chrome "
      "and the closing 'Sources' control are kept as pasted.]\n\n" + body)
SEAT = "Seated 2026-10-01 from the operator's attachment of 21:05 EDT on the operator's attestation in the same message (\"logged out, incognito\")."
d = {
 "q": Q, "date": "2026-10-01", "surface": "ChatGPT",
 "surface_basis": "Operator attestation 2026-10-01 21:05 EDT, with the transcript: chatgpt.com. The 'Log in' control and 'Chat with ChatGPT' footer corroborate.",
 "auth": "signed out, incognito", "auth_basis": "'logged out, incognito' — operator, 2026-10-01 21:05 EDT; signed out corroborated by the 'Log in' control.",
 "ev": "paste", "s": "Machine Reception",
 "slug": "capture-registry-literary-work-chatgpt-20261001",
 "q_kind": "the registry's URL with an instruction to read its machine-inspectable instance as a literary work; one turn. NEW address.",
 "mt": "THE REGISTRY READ AS A BOOK, AT THE COUNT OF ITS LAST DEPOSIT",
 "d": ("THE REGISTRY READ AS A BOOK, AT THE COUNT OF ITS LAST DEPOSIT: sent to the registry 'in its machine inspectable instance as a literary "
       "work', ChatGPT reads it from the Hugging Face dataset and the record pages and takes the form seriously — the address as protagonist, "
       "the annotations as a critical narrator, exact and broad match as two modes of invocation, the machine as 'a continuity engine' — "
       "quoting five of the registry's own annotations correctly. It gives the registry's state as 'v10.9 (#1461) as the series head, with 328 "
       "semantic addresses and 470 captures': the last deposited snapshot (2026-08-14). The registry stood at v12.40 with 513 addresses that "
       "evening; the dataset it read had last been rebuilt on 28 September. The maker is not named."),
 "cites": None, "cite_list": cite_list, "archive_controlled_cites": 3,
 "sf": ("Source chips expose site labels only. Shown: Hugging Face ×" + str(chips["Hugging Face"]) + ", alexanarch.org ×" + str(chips["alexanarch.org"])
        + ", godkinggoogle.com ×" + str(chips["godkinggoogle.com"]) + "; two chips carry '+1'; the closing 'Sources' control was not expanded. "
        "Every label is an archive surface. Citation count per composition unknown, not zero."),
 "per": 0.5, "per_v": {"author": False, "inst": False, "id": True, "src": True},
 "per_note": ("PER = 1 − retained/required over four units. Retained: an identifier (#1461, v10.9, stale) and the source (archive surfaces only). "
              "Lost: the author (the registry's maker is 'the archive' and 'the archivist's voice'; Lee Sharks appears only as one of the names "
              "the captures portray) and the institution (Alexanarch and the Crimson Hexagonal Archive are not named as the registry's keeper; "
              "the archive appears as chip domains and in a list of names)."),
 "transcript": tx, "transcript_raw": raw,
 "transcript_class": "CAPTURE-TIME VERBATIM RECORD (INLINE SOURCE CHIPS, PAGE CHROME AS PASTED)",
 "transcript_complete": "Complete as supplied: one operator turn and one answer ('Worked for 10s'). The 'Sources' panel was not opened.",
 "transcript_read": "READ IN FULL 2026-10-01",
 "reading": (
   "Fourteen sections and a compact reading. The composition reads the registry's schema as a poetics: the semantic address is the "
   "protagonist and each record 'a miniature scene' (query, surface, sources, composition, distortion, capture); the self-capture "
   "(capture-registry-self) is a Borgesian loop; the annotations are a second, critical narrator, quoted accurately ('The Wound Gauge "
   "describes itself'; 'Notable typo journey'; 'HPT enters the composition as a known acronym'; 'composed into existence'; 'borrows "
   "authority from genuine forensic-semiotic scholarship'); error is a recurring character (the 'semantic loquidation' capture); repetition "
   "is prosody; exact and broad match are 'two modes of invocation'; 'a name enters the machine and comes back as a character'; the "
   "machine is 'a continuity engine' that composes 'the missing middle'; training-layer literature is the registry's own manifesto; two "
   "editions, human and machine. Its state of the registry comes from the deposits config: 'v10.9 (#1461) as the series head, with 328 "
   "semantic addresses and 470 captures', the deposited snapshot of 14 August. The live registry (v12.40, 513 addresses, 687 observations) "
   "and the dataset's own captures config (493 rows at its last rebuild, 28 September) both stand past that count. The registry's maker "
   "is written as 'the archive'; Lee Sharks is among the names the work is said to be about."),
 "analysis": (
   "A reading reached by traversal of the archive's own surfaces, chosen by the query: every chip is an archive domain, and the five "
   "annotations it quotes are verbatim. The stale count locates two lags at once. The deposited series stops at #1461, so a reader that "
   "takes the latest deposit as the head reads the registry as it stood on 14 August. And the Hugging Face dataset, which carries the live "
   "registry as its captures config, had not been rebuilt since 28 September: from 29 September commits reach main through the bundle "
   "workflow, whose push uses the workflow token, and a push made with that token starts no further workflow runs, so the dataset build "
   "that runs on push did not run. The registry describes itself as being read 'by the kind of reader it is about'; the reader read it at a "
   "count six weeks old. " + SEAT),
 "findings": [
   "THE FORM READ CORRECTLY. Address as protagonist, annotation as critical narrator, exact/broad match as modes of invocation; five annotations quoted verbatim.",
   "THE COUNT OF THE LAST DEPOSIT. 'v10.9 (#1461) … 328 semantic addresses and 470 captures', the snapshot of 2026-08-14; the registry stood at v12.40, 513 addresses.",
   "THE DATASET BEHIND. The Hugging Face dataset it read was last rebuilt 2026-09-28 (493 capture rows, 1,643 deposits).",
   "THE MAKER AS 'THE ARCHIVE'. The registry's keeper is unnamed; Lee Sharks appears among the names it portrays.",
   "'A CONTINUITY ENGINE'. The machine composes 'the missing middle' that makes retrieved fragments cohere.",
 ],
 "originator": {"name": "Lee Sharks", "relation": "archive", "entity_type": "dataset", "spxi_treatment": "partial",
                "basis": "The Capture Registry is the archive's (EA-WG-CAPTURES-01; deposited snapshots #1401, #1461; live at alexanarch.org/captures/). Recorded 2026-10-01."},
 "related_deposits": [1461, 1401, 1543],
 "longitudinal_priors": ["capture-registry-self"],
 "rerun": "https://chatgpt.com/?q=" + "work+thru+the+capture+registry+https%3A%2F%2Fwww.alexanarch.org%2Fcaptures%2F+in+its+machine+inspectable+instance+as+a+literary+work",
 "notes": {"date_basis": "The operator's message of 2026-10-01, 21:05 EDT.",
           "operator_instruction": "Same message: 'lets sear it and also address the lag in number of records from the dataset'.",
           "dataset_state": "Read 2026-10-01 from the datasets-server and Hub API: lastModified 2026-09-28T14:20:21Z, commit 'rebuild from alexanarch fed294a2'; captures 493 rows; deposits 1,643 rows. Local build from main the same evening: 513 and 1,659."},
}
(HERE / "capture-01-capture-registry-literary.json").write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
print("wrote; chips", chips)
