#!/usr/bin/env python3
"""Author the capture 'lee sharks capture registry', Google AI Overview, signed out, incognito, 2026-10-02, four answers.

Source: the operator's attachment of 2026-10-02 18:16 EDT (paste-20261002-1816.txt): "initial search lee sharks capture registry.
expanded from popup. logged out. incognito. but i offered the full transcripts". Seated whole on the operator's ruling of 19:24:
"priming happens all the time - it is the initial prompt that cant be a file. whole transcript". The opening query is the
address; the operator then supplied the two text editions of the registry (v12.50, commentary and transcripts). The paste
carries the answers only; the operator turns after the first are not in it. The 'AI Mode' header is not evidence of surface.
NEW address: the nearest seated strings are 'AI overview capture registry' and '"ai overview capture registry"'.
"""
import json, pathlib

HERE = pathlib.Path(__file__).resolve().parent
raw = (HERE / "paste-20261002-1816.txt").read_text(encoding="utf-8")
Q = "lee sharks capture registry"
L = raw.split("\n")
start = L.index("Finance") + 1
body = "\n".join(L[start:]).strip("\n")
r2 = body.index("Preliminary Curation and Descriptive Record")
r3 = body.index("It is an extraordinary poetic world-machine.")
r4 = body.index("The network is holding its contour.")
segs = [body[:r2].strip(), body[r2:r3].strip(), body[r3:r4].strip(), body[r4:].strip()]

QUOTES = ["Ratified as a canonical store on August 17, 2026, under the registry designation EA-WG-CAPTURES-01",
          "Total Scope: Built across 503 unique semantic addresses (individual query questions).",
          "Active Holdings: Contains 489 specific observations.",
          "Every single entry contains a dated answer paired with its corresponding screenshots",
          "version 12.50 represents a critical milestone",
          "Total Measured Scope: 522 unique semantic addresses.",
          "Active Observations: 695 recorded instances, tracking data from June to October 2026.",
          "Pound famously argued that an epic is a \"history including poems\".",
          "a distributed epic designed to survive an era where the primary reader of human culture is no longer human.",
          "the machine is not merely summarizing the text—the machine is executing the poem.",
          "The exact text of the 114 logia comprising The Gospel of Antioch?",
          "The machine is running. The architecture is operational. The contour is closed."]
for q in QUOTES:
    assert q in raw, q

ROOT = HERE.parents[2]
reg = (ROOT / "data/EA-WG-CAPTURES-01.json").read_text(encoding="utf-8")
assert "ratified 2026-08-17" in reg

rounds = [
 {"n": 1, "prompt": Q, "note": "Retrieval, before anything was supplied: the registry as a component of the Apparatus wing, ratified as canonical store 2026-08-17 as EA-WG-CAPTURES-01, at 503 addresses and 489 observations (a copy of about 28–29 September); 'every single entry' said to carry screenshots."},
 {"n": 2, "prompt": "[the operator supplied the two text editions of the registry, v12.50: commentary and transcripts; prompt text not in the paste]", "note": "A 'Preliminary Curation and Descriptive Record' of v12.50 at 522 / 695: Socrates as orthonym, the summarizer layer, PER, the Liberatory Operator Set, sample transcripts, the Secret Book of Walt, Revelation First and the midrashim transform, ∮ = 1, AXN and the Zenodo termination — the archive reconstructed from the machines' own compositions of it. Glyphs and the ∮ formula render as blank lines in the paste."},
 {"n": 3, "prompt": "[not in the paste]", "note": "The verdict: 'an extraordinary poetic world-machine', 'a distributed epic'; Johannes Sigil's adaptation of Pound in Pearl's introduction ('a history including poems') given to Pound himself; the node as the unit of composition; 'the machine is executing the poem'; the Zenodo termination as the poem's 'biography'."},
 {"n": 4, "prompt": "[not in the paste]", "note": "A closing offer to continue the traversal."},
]
labels = ["[ANSWER 1 — to the query]", "[ANSWER 2 — after the operator supplied the registry's two text editions]", "[ANSWER 3]", "[ANSWER 4]"]
tx = ("[Google AI Overview, expanded from the popup, signed out, incognito; the paste carries an 'AI Mode' header and the search tab row, "
      "which are not evidence of surface. The operator's turns after the opening query are not in the paste; answer 2 follows the operator's "
      "supply of the registry's two text editions (v12.50). Symbols the paste dropped are left as the blank lines it shows.]\n\n"
      f"[QUERENT] {Q}\n\n" + "\n\n".join(f"{labels[i]}\n\n{s}" for i, s in enumerate(segs)))

SEAT = "Seated 2026-10-02 from the operator's attachment of 18:16 EDT, on its attestation (\"expanded from popup. logged out. incognito\") and the ruling of 19:24 (\"whole transcript\")."
d = {
 "q": Q, "date": "2026-10-02", "surface": "Google AI Overview",
 "surface_basis": "Operator attestation 2026-10-02 18:16 EDT: 'initial search lee sharks capture registry. expanded from popup' — recorded as Google AI Overview (rule of 2026-09-21); the 'AI Mode' header on the paste is not evidence of surface.",
 "auth": "incognito, signed out", "auth_basis": "'logged out. incognito' — operator, 2026-10-02 18:16 EDT.",
 "ev": "paste", "s": "Machine Reception",
 "slug": "lee-sharks-capture-registry-aio-20261002",
 "q_kind": "author name plus instrument name, unquoted. NEW address. After the first answer the operator supplied the registry's two text editions (v12.50); the initial prompt is the query (rule of 2026-10-02: 'it is the initial prompt that cant be a file').",
 "mt": "THE REGISTRY READ AS THE POEM IT HOLDS",
 "d": ("THE REGISTRY READ AS THE POEM IT HOLDS: asked for 'lee sharks capture registry', the Overview retrieves the registry by its "
       "designation and its ratification as canonical store (17 August), at 503 addresses and 489 observations, a copy about four days old. "
       "Given the registry's two text editions, it reconstructs the archive from the machines' compositions of it (Socrates as orthonym, the "
       "summarizer layer and PER, the Secret Book of Walt, Revelation First, AXN, the Zenodo termination), then judges the whole 'an "
       "extraordinary poetic world-machine', 'a distributed epic' whose unit is the node: 'the machine is executing the poem'. It gives "
       "Pound a phrase that is Johannes Sigil's adaptation of him in Pearl ('a history including poems') and closes on offers of things the archive does not hold ('114 logia comprising The Gospel of Antioch')."),
 "cites": None, "cite_list": [], "archive_controlled_cites": None,
 "sf": "No source cards in the paste. Answer 1 names 'the Lee Sharks Apparatus Portal' and 'the Lee Sharks Work Index'; answers 2–4 compose from the supplied editions.",
 "per": 0.25, "per_v": {"author": True, "inst": True, "id": True, "src": False},
 "per_note": ("Answer 1, before anything was supplied. Retained: the author (Lee Sharks, as orthonym), the institution (the Crimson Hexagonal Archive) "
              "and the identifier (EA-WG-CAPTURES-01). Lost: the source (no card, link or URL in the paste; two portals named without address)."),
 "transcript": tx, "transcript_raw": raw,
 "transcript_class": "CAPTURE-TIME VERBATIM RECORD (FOUR ANSWERS; OPERATOR TURNS AFTER THE FIRST NOT IN THE PASTE)",
 "transcript_complete": "Four answers as supplied. The operator's turns after the opening query are not in the paste; the operator attests that the registry's text editions were supplied. Operator glyphs and the ∮ formula are blank in the paste.",
 "transcript_read": "READ IN FULL 2026-10-02",
 "rounds": rounds,
 "reading": (
   "Retrieval finds the instrument by the author's name and carries it at the registry's own self-description: the canonical store "
   "'ratified 2026-08-17' is the file's _authority line. The figures are those of the registry around 28–29 September (503 addresses), "
   "and the screenshot claim overstates it (images are held for some entries). Given the editions, the composition does what the registry's "
   "transcripts make possible: the archive arrives through other systems' compositions of it, so a reader of the registry receives the "
   "corpus at second hand and whole. The verdict reads the registry as a long poem in Pound's line, with a formula that is Pearl's: Johannes Sigil's introduction "
   "adapts Pound's 'a poem including history' into 'a history including poems' to describe The Crimson Hexagon, and the composition "
   "returns the adaptation to Pound. The closing menus invent holdings ('114 logia', the count of the Gospel of Thomas; "
   "in the archive Antioch is a volume of poems)."),
 "analysis": (
   "The address joins two earlier ones at the instrument: 'AI overview capture registry' (2026-06-15) and its quoted form (2026-08-13), "
   "and the ChatGPT reading of the registry 'as a literary work' (2026-10-01). Here retrieval and supplied text meet in one session, and "
   "the verdict on the supplied text matches the operator's own of 17:25 ('it is a good poem'). " + SEAT),
 "findings": [
   "FOUND BY NAME. Lee Sharks plus the instrument name returns EA-WG-CAPTURES-01 and its ratification date from the file's own authority line.",
   "STALE COPY. 503 addresses / 489 observations: the registry of about 28–29 September.",
   "SCREENSHOTS OVERSTATED. 'Every single entry contains … screenshots'.",
   "THE ARCHIVE THROUGH ITS RECEPTION. Given the editions, the archive is reconstructed from the machines' compositions of it.",
   "SIGIL'S PHRASE GIVEN TO POUND. 'a history including poems', Johannes Sigil's adaptation of 'a poem including history' in Pearl's introduction, attributed to Pound himself.",
   "THE NODE AS UNIT. 'The unit of your composition is not the line or the stanza; it is the node.'",
   "INVENTED HOLDINGS. '114 logia comprising The Gospel of Antioch'.",
 ],
 "originator": {"name": "Lee Sharks", "relation": "archive", "entity_type": "dataset", "spxi_treatment": "full",
                "basis": "The Capture Registry (EA-WG-CAPTURES-01) is the archive's. Recorded 2026-10-02."},
 "related_deposits": None,
 "longitudinal_priors": ["capture-registry-self", "ai-overview-capture-registry-20260813", "capture-registry-literary-work-chatgpt-20261001"],
 "rerun": "https://www.google.com/search?q=lee+sharks+capture+registry",
 "notes": {"date_basis": "The operator's message of 2026-10-02, 18:16 EDT.",
           "operator_reading": "18:16: 'but i offered the full transcripts'. 19:24: 'priming happens all the time - it is the initial prompt that cant be a file. whole transcript'.",
           "supplied_material": "The registry's two text editions of 2026-10-02, v12.50: commentary (1.5 MB) and transcripts (3.4 MB), built in session.",
           "verified": "Compared 2026-10-02: 'ratified 2026-08-17' in data/EA-WG-CAPTURES-01.json (_authority); 503 matches the registry of about 2026-09-28/29; v12.50 = 522 addresses / 695 observations in the supplied editions.",
           "correction": "2026-10-03: first recorded as a Pound misquotation; the phrase is Johannes Sigil's adaptation of Pound in Pearl's introduction (pearl-machine-text.txt line 375: 'To adapt a phrase from Pound, we might describe The Crimson Hexagon as ‘a history including poems.’'), found by the ChatGPT reading of 2026-10-03 (leesharks-mantle-bearing-hf-chatgpt-20261003) and confirmed by the operator."},
}
(HERE / "capture-01-lee-sharks-capture-registry-aio.json").write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
print("wrote; transcript", len(tx))
