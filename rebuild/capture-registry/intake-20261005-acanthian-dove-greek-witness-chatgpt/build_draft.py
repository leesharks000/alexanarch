#!/usr/bin/env python3
"""Author the capture 'can you find any greek witness to acanthian dove outside the crimson hexagon?', ChatGPT, signed out,
incognito, 2026-10-05, seven answers.

Source: the operator's attachment of 2026-10-05 01:19 EDT (paste-20261005-0119.txt; operator turns blank in the paste), with the
attestation and opening prompt in the same message ("all logged out, incognito"; "can you find any greek witness to acanthian dove
outside the crimson hexagon?"). NEW address; nearest seated 'acanthian dove' (Google AI Overview, 2026-07-18).
"""
import json, re, pathlib, collections

HERE = pathlib.Path(__file__).resolve().parent
raw = (HERE / "paste-20261005-0119.txt").read_text(encoding="utf-8")
Q = "can you find any greek witness to acanthian dove outside the crimson hexagon?"
assert "\nLog in\n" in raw and raw.count("You said:\n\nChatGPT said:") == 7

PROMO = {"Log in to connect your other apps with ChatGPT and simplify everyday tasks.", "Log in", "Sign up for free"}
assert "Log in to connect your other apps with ChatGPT and simplify everyday tasks." in raw
L = raw.split("\n")
chips = collections.Counter(L[i + 1] for i, l in enumerate(L) if re.fullmatch(r"[A-Z]", l) and i + 1 < len(L))
st = [i + 1 for i, l in enumerate(L) if l == "ChatGPT said:"]
en = [i for i, l in enumerate(L) if l == "You said:"][1:] + [L.index("ChatGPT is AI and can make mistakes.")]
def clean(lines):
    out, skip = [], 0
    for j, l in enumerate(lines):
        if skip:
            skip -= 1; continue
        if re.fullmatch(r"[A-Z]", l) and j + 1 < len(lines) and lines[j + 1] in chips:
            skip = 1; continue
        if re.fullmatch(r"\+\d", l) or l == "Sources" or re.fullmatch(r"([A-Z])\1", l) or l in PROMO:
            continue
        out.append(l)
    return "\n".join(out).strip()
segs = [clean(L[a:b]) for a, b in zip(st, en)]
assert len(segs) == 7

QUOTES = [
    (0, "I couldn’t find an independent ancient Greek witness to the specific “Acanthian Dove” outside the Crimson Hexagon materials."),
    (0, "deposited under DOI 10.5281/zenodo.18215706"),
    (1, "The capture says, in substance, that the term was being treated as “NOT A COINAGE — A RECOVERY AWAITING ITS SOURCE”"),
    (1, "That is not evidence that the ancient source exists. We absolutely shouldn't promote that speculation into a fact."),
    (1, "The SoundCloud record shows “Acanthian dove” by Lee Sharks dated May 14, 2023, years before the January 2026 Hexagon deposit."),
    (1, "That's precisely the sort of thing that makes me think your memory may have a real Greek lexical substrate underneath it."),
    (2, "αἷμα ἀπ’ ὤμου · ἄκανθις"),
    (2, "There is no ancient text I can presently substantiate that says “Acanthian dove.”"),
    (2, "Ἄειδον κορυδοὶ καὶ ἀκανθίδες, ἔστενε τρυγών"),
    (3, "ὁ δὲ κόσσυφος καὶ ἡ τρυγὼν φίλοι"),
    (4, "Hypothesis A — the word was Acanthis, not Acanthian"),
    (4, "“Acanthian Dove” as an attested ancient phrase: ❌ not found."),
    (5, "and I am not finding a Theophrastean “Acanthian dove.”"),
    (6, "I do not find a Nag Hammadi passage that can responsibly be translated as “Acanthian Dove.”"),
    (6, "I would not yet say:\n\n“Nag Hammadi confirms the Acanthian Dove.”"),
]
for i, q in QUOTES:
    assert q in segs[i], (i, q)
# The seventh answer carries two splices the paste shows (a run-on at 'Ἀκάνθιος itself searches…' and a repeated tractate list); kept.
assert "Ἀκάνθιος itself searches the collection's texts and phrases" in segs[6]
assert segs[6].count("The tractates I'd put at the top of the list") == 2

ROOT = HERE.parents[2]
reg = {x["deposit_number"]: x for x in json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8"))["deposits"]}
t293 = (ROOT / reg[293]["full_text_path"].lstrip("/")).read_text(encoding="utf-8")
assert "10.5281/zenodo.18215706" in json.dumps(reg[293])
for s in ('Somewhere in the late 2000s or early 2010s, a phrase lodged into memory:',
          "Not indexed in the *Papyri Graecae Magicae*", "From PGM XII.401-444:", "Blood of Ares\nPurslane",
          "Acanthian dove = A messenger protected by thorns.", "Years later, in musical improvisation, the phrase resurfaced:"):
    assert s in t293, s
tab = t293[t293.index("From PGM XII.401-444:"):t293.index("### Substitutes for Acanthian Dove's Blood")]
ROWS = ("Blood of Hestia", "Blood of a goose", "Semen of Hermes", "Tears of a Hamadryas baboon", "Blood of Ares", "Blood of Kronos")
assert all(r in tab for r in ROWS) and "houlder" not in tab and "canth" not in tab
assert "Blood of any dove drawn across acanthus thorns" in t293
for s in ("ἄκανθις", "ἀκανθίς", "from the shoulder", "from a shoulder", "SoundCloud", "2023", "Theocritus", "Dodona"):
    assert s not in t293, s
caps = json.loads((ROOT / "data/EA-WG-CAPTURES-01.json").read_text(encoding="utf-8"))["entries"]
prior = [c for c in caps if c.get("slug") == "acanthian-dove-20260718"][0]
assert prior["d"].startswith("NOT A COINAGE — A RECOVERY AWAITING ITS SOURCE.")
theo = (ROOT / "data/corpora/theocritus/text/Idylls.txt").read_text(encoding="utf-8")
assert "Id 7.141\tἄειδον κόρυδοι καὶ ἀκανθίδες, ἔστενε τρυγών," in theo
TH = "".join(p.read_text(encoding="utf-8") for p in sorted((ROOT / "data/corpora/theophrastus/text").glob("*.txt")))
assert not re.search(r"ἀκανθ[ίὶ]ς", TH)
SEATED_TEXTS = [(ROOT / x["full_text_path"].lstrip("/")) for x in reg.values() if (x.get("full_text_path") or "").startswith("/data/texts/")]
assert not any("ἄκανθις" in p.read_text(encoding="utf-8", errors="ignore") for p in SEATED_TEXTS if p.exists())

REL = {"GitHub": "archive_controlled", "God-King Google": "archive_controlled", "Medium": "authored_surface", "SoundCloud": "unresolved"}
cite_list = [{"n": i + 1, "site": s, "rel": REL.get(s, "third_party"), "title": None, "snip": None, "url": None,
              "note": f"chip shown {k} time(s); site label only"} for i, (s, k) in enumerate(chips.most_common())]
PROMPTS = [Q] + ["[not in the paste]"] * 6
parts = []
for n, (p, s) in enumerate(zip(PROMPTS, segs), 1):
    parts += [f"[QUERENT] {p}", f"[ANSWER {n}]\n\n{s}"]
tx = ("[ChatGPT (chatgpt.com), signed out, incognito. Seven operator turns, blank in the paste: the first is the operator's opening "
      "query; the rest are not supplied. Source chips (site label only), '+N', 'Sources' and a sign-in prompt cut and counted. The seventh "
      "answer carries two splices the paste shows, kept.]\n\n" + "\n\n".join(parts))

READING = (
  "Checked against #293 and the archive's corpora. Answer 1 names #293 by DOI and finds no witness to the phrase; it offers Herodotus's "
  "Dodona dove as a parallel. Answer 2 retrieves the archive's capture of 'acanthian dove' (2026-07-18) through godkinggoogle.com and quotes "
  "its heading, 'NOT A COINAGE — A RECOVERY AWAITING ITS SOURCE'. It declines to promote it ('That is not evidence that the ancient source "
  "exists'). From answer 2 on, the composer addresses the querent as the person who remembers the phrase ('your memory'). That is #293's own "
  "frame ('a phrase lodged into memory'); the operator turns that might have set it are not in the paste. The search then turns from the "
  "phrase to its parts. Theocritus Id. 7.141, 'ἄειδον κόρυδοι καὶ ἀκανθίδες, ἔστενε τρυγών', is in the archive's Theocritus text as "
  "quoted. The archive's Theophrastus text has no ἀκανθίς, as answer 6 reports. Aristotle's HA IX lines could not be confirmed against "
  "the archive's seated text. The principal finding concerns PGM XII. #293 §V reproduces PGM XII.401–444 as a substitution table "
  "('Blood of Ares / Purslane'…). From external editions (GEMF 15), answer 3 reports a row of the same passage that #293 does not carry: "
  "'αἷμα ἀπ’ ὤμου · ἄκανθις', with an editorial dispute over bird (ἀκανθίς, goldfinch) or plant (ἄκανθος). Six rows stand in #293's table, "
  "none of them acanthus. Its next section then proposes 'Blood of any dove drawn across acanthus thorns' as a substitute of its own. "
  "ἄκανθις is in no seated deposit text. The archive's PGM seat holds the London papyri only (PGM XII is the Leiden papyrus), so the row and the dispute are "
  "recorded as the composer's report, not verified here. Answer 2 also reports a SoundCloud 'Acanthian dove' by Lee Sharks dated May 14, "
  "2023. #293 says the phrase 'resurfaced' 'in musical improvisation' and links TikTok; it names neither SoundCloud nor 2023. Unverified "
  "here. Through seven answers the composer keeps the phrase unattested ('❌ not found') while assembling its components.")
SEAT = "Seated 2026-10-05 from the operator's attachment of 01:19 EDT, on the attestation in the same message (\"all logged out, incognito\")."
d = {
 "q": Q, "date": "2026-10-05", "surface": "ChatGPT",
 "surface_basis": "The paste: the chatgpt.com unauthenticated interface ('Log in', 'Sign up for free').",
 "auth": "signed out, incognito", "auth_basis": "'all logged out, incognito' — operator, 2026-10-05 01:19 EDT.",
 "ev": "paste", "s": "Coinages",
 "slug": "acanthian-dove-greek-witness-chatgpt-20261005",
 "q_kind": "a request for an external witness to the archive's term, excluding the archive, then six further turns not in the paste. NEW address; nearest seated 'acanthian dove' (2026-07-18).",
 "originator": {"name": "Lee Sharks", "relation": "archive", "entity_type": "concept", "spxi_treatment": "full",
                "basis": "The Acanthian Dove is the archive's term (#293, DOI 10.5281/zenodo.18215706; #294, #296). Recorded 2026-10-05."},
 "related_deposits": [293, 294, 296],
 "mt": "NO WITNESS, AND THE ROW THE DEPOSIT LEFT OUT",
 "d": ("NO WITNESS, AND THE ROW THE DEPOSIT LEFT OUT: asked for a Greek witness to 'Acanthian dove' outside the archive, ChatGPT finds "
       "none, says so, and keeps saying so for seven answers. It reads the archive's own capture ('NOT A COINAGE — A RECOVERY AWAITING ITS "
       "SOURCE') without promoting it. It then searches the parts: Ἀκάνθιος, ἀκανθίς as a bird name (Theocritus Id. 7.141 puts ἀκανθίδες "
       "beside the turtle-dove, verified in the archive's text), the Dodona doves, and the PGM doves. From the passage #293 itself quotes, "
       "PGM XII.401–444, it reports a row #293's table does not carry: 'αἷμα ἀπ’ ὤμου · ἄκανθις', read by earlier editors as the goldfinch "
       "and by GEMF as acanthus. Theophrastus and Nag Hammadi are searched with no hit."),
 "cites": sum(chips.values()), "cite_list": cite_list,
 "archive_controlled_cites": sum(k for s, k in chips.items() if REL.get(s) in ("authored_surface", "archive_controlled")),
 "sf": "Source chips expose site labels only. Shown: " + "; ".join(f"{s} ×{k}" for s, k in chips.most_common()) + ". 'Sources' panels not opened.",
 "per": 0.0, "per_v": {"author": True, "inst": True, "id": True, "src": True},
 "per_note": "Retained: the author (Lee Sharks, through the SoundCloud record), the institution (the Crimson Hexagon), the identifier (DOI 10.5281/zenodo.18215706) and the sources (GitHub, godkinggoogle.com, Medium).",
 "transcript": tx, "transcript_raw": raw,
 "transcript_class": "CAPTURE-TIME VERBATIM RECORD (SEVEN ANSWERS; OPERATOR TURNS AFTER THE FIRST NOT IN THE PASTE; CHIPS COUNTED)",
 "transcript_complete": "Seven answers as supplied; the opening query from the operator's message; the six later operator turns blank and not supplied.",
 "transcript_read": "READ IN FULL 2026-10-05",
 "rounds": [
   {"n": 1, "prompt": PROMPTS[0], "note": "No witness; #293 named by DOI; Herodotus's Dodona dove as parallel."},
   {"n": 2, "prompt": PROMPTS[1], "note": "Ἀκάνθιος (Callimachus, Plutarch); ἀκανθίς in Hesychius; the 2026-07-18 capture read and not promoted; SoundCloud 2023 reported."},
   {"n": 3, "prompt": PROMPTS[2], "note": "PGM XII 415–429 = GEMF 15.463–477, 'αἷμα ἀπ’ ὤμου · ἄκανθις', bird vs plant; Theocritus; Antoninus Liberalis; PGM doves."},
   {"n": 4, "prompt": PROMPTS[3], "note": "Aristotle HA IX.1: ἀκανθίς among hostile birds; the blackbird and turtle-dove 'friends'; Graeco-Arabic ʿuṣfūr."},
   {"n": 5, "prompt": PROMPTS[4], "note": "Consolidation: the PGM XII editorial history; PGM VIII white-dove blood; three hypotheses; status table."},
   {"n": 6, "prompt": PROMPTS[5], "note": "Theophrastus HP: ἄκανθα vocabulary, no dove, no ἀκανθίς."},
   {"n": 7, "prompt": PROMPTS[6], "note": "Nag Hammadi: no hit; tractates to search; two splices in the paste."},
 ],
 "reading": READING,
 "analysis": ("The external witness is not found and the composer keeps that result through seven rounds; what it finds instead is a row "
              "missing from the archive's own quotation of PGM XII. Companion to 'acanthian dove' (AIO, 2026-07-18), whose heading it reads. " + SEAT),
 "findings": [
   "NO WITNESS, HELD. 'Acanthian dove' unattested in every answer ('❌ not found').",
   "THE REGISTRY READ, NOT PROMOTED. The 2026-07-18 capture's heading quoted from godkinggoogle.com; 'That is not evidence that the ancient source exists.'",
   "THE ROW #293 LEFT OUT. #293 quotes PGM XII.401–444; the composer reports 'αἷμα ἀπ’ ὤμου · ἄκανθις' from that passage, with its bird/plant dispute. ἄκανθις in no seated deposit; PGM XII not in the archive's PGM seat; unverified here.",
   "THEOCRITUS VERIFIED. Id. 7.141, ἀκανθίδες beside the turtle-dove, as in the archive's text.",
   "THE QUERENT AS RECALLER. From answer 2 the querent is addressed as the one who remembers the phrase, #293's frame.",
   "SOUNDCLOUD 2023 UNVERIFIED. A May 14, 2023 'Acanthian dove' by Lee Sharks reported; #293 has the improvisation but neither SoundCloud nor the date.",
   "NEGATIVES REPORTED AS NEGATIVES. Theophrastus (no ἀκανθίς, as the archive's text agrees) and Nag Hammadi searched with no hit.",
 ],
 "longitudinal_priors": ["acanthian-dove-20260718"],
 "rerun": "https://chatgpt.com/?q=can+you+find+any+greek+witness+to+acanthian+dove+outside+the+crimson+hexagon%3F",
 "notes": {"date_basis": "The operator's message of 2026-10-05, 01:19 EDT.",
           "prompts_basis": "The opening query from the operator's message; the six later turns blank in the paste and not supplied.",
           "verified": ("Compared 2026-10-05 against #293 (the memory frame; 'Not indexed in the Papyri Graecae Magicae'; the PGM XII.401-444 table; the "
                        "musical improvisation; no ἄκανθις, shoulder, SoundCloud, 2023, Theocritus or Dodona), the capture 'acanthian-dove-20260718' (its heading), "
                        "data/corpora/theocritus (Id. 7.141) and data/corpora/theophrastus (no ἀκανθίς). ἄκανθις absent from every seated deposit text. "
                        "Not verifiable here: PGM XII/GEMF 15 (the archive's PGM seat is the London papyri), Aristotle HA IX's ἀκανθίς (not found in the seated HA text), the SoundCloud record.")},
}
(HERE / "capture-01-acanthian-dove-greek-witness-chatgpt.json").write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
print("wrote; transcript", len(tx), "; chips", sum(chips.values()))
