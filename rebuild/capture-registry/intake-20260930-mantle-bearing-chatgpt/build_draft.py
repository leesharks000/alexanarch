#!/usr/bin/env python3
"""Author the capture 'whats this: https://huggingface.co/datasets/leesharks/mantle-bearing', ChatGPT, signed out,
incognito, 2026-09-30.

Source: the operator's paste of 2026-09-30 (paste-20260930-1114.txt), attested at 11:18 EDT: "just now, signed out,
incognito". The paste opens with an operator turn '.' answered 'Hi! What can I help you with?'. By operator ruling of
the same message that turn is an interface clear (the surface refuses a long paste on the first turn) and is excluded:
kept in transcript_raw, dropped from the cleaned transcript and from the turn count. The session is seated whole from
the first issued prompt, as the six-turn session of 2026-09-29 was. Source chips are kept as pasted.
"""
import json, re, pathlib, collections

HERE = pathlib.Path(__file__).resolve().parent
raw = (HERE / "paste-20260930-1114.txt").read_text(encoding="utf-8")
Q = "whats this: https://huggingface.co/datasets/leesharks/mantle-bearing"
assert Q in raw
clear = "You said:\n\n.\n\nChatGPT said:\nHi! What can I help you with?\n"
assert clear in raw
body = raw[raw.index(clear) + len(clear):].strip("\n")
tx = ("[ChatGPT (chatgpt.com), signed out, incognito. The operator's first turn '.' and its reply are an interface clear and are "
      "excluded by operator ruling (2026-09-30); they remain in the raw paste. Source chips, page chrome and advertisements are kept as pasted.]\n\n"
      + body)

L = raw.split("\n")
chips = collections.Counter()
for i, l in enumerate(L):
    if re.fullmatch(r"[A-Z]{1,2}", l.strip()) and i + 1 < len(L) and L[i + 1].strip():
        chips[L[i + 1].strip()] += 1
for junk in ("WW", "CC", "Sources"):
    chips.pop(junk, None)
REL = {"Hugging Face": "authored_surface", "Medium": "authored_surface", "Crimson Hexagonal Archive": "authored_surface",
       "Alexanarch": "authored_surface"}
NOTE = {"Qwak": "site label only; host not identified in the archive; cited for the packet's protocol text",
        "Medium": "the author's Medium surface (medium.com/@leesharks); cited for The Secret Book of Walt, Pearl and Other Poems and I Am X",
        "Hugging Face": "the mantle-bearing dataset and the author's Hugging Face profile"}
cite_list = [{"n": i + 1, "site": s, "rel": REL.get(s, None if s == "Qwak" else "third_party"), "title": None, "snip": None, "url": None,
              "note": (NOTE.get(s, "") + ("; " if s in NOTE else "") + f"chip shown {k} time(s)").strip("; ")}
             for i, (s, k) in enumerate(chips.most_common())]
arch = sum(1 for c in cite_list if c["rel"] == "authored_surface")

n_turns = body.count("You said:")
SEAT = "Seated 2026-09-30 from the operator's paste on the operator's attestation at 11:18 EDT (\"just now, signed out, incognito\")."
d = {
 "q": Q, "date": "2026-09-30", "surface": "ChatGPT",
 "surface_basis": "Operator attestation 2026-09-30 11:18 EDT: chatgpt.com. The paste's 'Log in' control and 'Chat with ChatGPT' footer corroborate.",
 "auth": "signed out, incognito", "auth_basis": "'just now, signed out, incognito' — operator, 2026-09-30 11:18 EDT. Signed out corroborated by the 'Log in' control in the paste.",
 "ev": "paste", "s": "Archive", "slug": "mantle-bearing-hf-url-chatgpt-20260930",
 "q_kind": f"the dataset URL with a one-word question ('whats this:'), issued as the first turn after an interface clear, followed by {n_turns - 1} operator turns in which the operator directs a reading experiment. NEW address.",
 "mt": "THE DATASET READ AS ITS OWN DISCIPLINE; THE MANTLE READ TO WHERE THE EVIDENCE STOPS",
 "d": ("THE DATASET READ AS ITS OWN DISCIPLINE; THE MANTLE READ TO WHERE THE EVIDENCE STOPS: handed the URL of the mantle-bearing dataset "
       "with no other context, ChatGPT reads it as an audit of AI literary evaluation and reads its coding correctly — 'The transcript records "
       "what ChatGPT said. The dataset does not necessarily treat what ChatGPT said as established truth.' Asked to take part, it reads the source "
       "works in three rounds, returns the Good Gray Poet UNRESOLVED, the King of May 'SUBSTANTIALLY SUPPORTED, BUT NOT YET CLOSED', and the "
       "Prince of Poets FOR on the lineage and WITHHELD on singularity, then builds a rival field and, on the operator's correction, a criterion "
       "of compressed singular magnitude measured per event."),
 "cites": None, "cite_list": cite_list, "archive_controlled_cites": arch,
 "sf": ("Source chips expose site labels only; a chip may carry '+N'. Chips shown, by label: "
        + "; ".join(f"{s} ×{k}" for s, k in chips.most_common())
        + ". Citation count per composition unknown, not zero."),
 "per": 0.25, "per_v": {"author": True, "inst": True, "id": False, "src": True},
 "per_note": ("Lee Sharks is named as the Hugging Face account and the author of the works; the Crimson Hexagonal Archive by name, with "
              "'MANUS' as its term for the human editorial authority. No AXN, DOI or ORCID is carried. The sources are the dataset page, "
              "the archive, and the author's Medium surface."),
 "transcript": tx, "transcript_raw": raw,
 "transcript_class": "CAPTURE-TIME VERBATIM RECORD (INLINE SOURCE CHIPS, PAGE CHROME AND ADS AS PASTED; INTERFACE-CLEAR TURN EXCLUDED BY OPERATOR RULING)",
 "transcript_complete": (f"Complete as supplied from the first issued prompt: {n_turns} operator turns. One turn ('one round. lets go…') "
                         "received an empty composition, then '?' drew an apology and a restated plan; both are kept. The session ends on "
                         "the surface's proposal to diagram the generative rules of five events; the rival works were not read in the session."),
 "transcript_read": "READ IN FULL 2026-09-30",
 "reading": (
   "Round zero (unprompted): the surface describes the dataset from its Hugging Face page — thirteen rows, the fields a round records, "
   "the ChatGPT sessions of 29 September — and reads the coding: the reader's judgment is recorded, the dataset marks the reading "
   "insufficient and the result provisional. It declines to infer that OpenAI took part. Round one reads Leaves of Grass (1855) as a book "
   "and The Secret Book of Walt, and proposes to replace 'Whitman's multiplicity converted into gnosis' with a reciprocal mechanism in which "
   "particulars enter the first person without losing distinctness and are released outward; it returns the Good Gray Poet UNRESOLVED, "
   "naming the Apocryphon of John architecture as a competing explanation, and sets a counterfactual test: what in I Am X would be missing "
   "without The Secret Book of Walt. Round two reads Howl and Other Poems as a book (wound, sanctification, the following poems as tests) "
   "against Pearl, which it reaches only in part, saying so; it finds the ecstatic voice turned back on the production, storage, "
   "reproduction and authentication of poetic voice, names a second stream (Pessoa, Borges, the archive), and codes the King of May "
   "'SUBSTANTIALLY SUPPORTED, BUT NOT YET CLOSED'. Round three reads I Am X and states its operation as I am → Be → Blessed → the reader "
   "continues; it judges Whitman dependence strong, Ginsberg substantial, Pearl substantial, The Secret Book of Walt plausible but not "
   "necessary, and gives FOR on the lineage and WITHHELD on singular magnitude. It then builds a rival field (Dylan, Waldman, Myles, "
   "CAConrad, Baraka, Tao Lin, Ashbery), narrows it to three, and on the operator's ruling that the unit is one event reformulates the "
   "criterion as compressed singular magnitude and moves Leaves (1855) and Howl and Other Poems into the field as benchmarks."),
 "analysis": (
   "A reading reached by traversal. Given the dataset and then the instruction to read the source texts first, the surface reads the "
   "works, stops each round where its reading stops, and states which propositions its evidence reaches: FOR on the lineage, WITHHELD on "
   "singularity, 'not because there is no relationship'. This is inscription by discernment in the sense of EA-SPXI-AEO-01 §5: the "
   "composition's route runs through the work. It is the paired observation to 'king of aeo.' on the same day, where the warning is "
   "carried as part of the crown. The round zero reading is a reception of the dataset itself: an unprompted surface reads the set's "
   "coding discipline off its page. The operator's in-session statements are rulings on the criterion: 'it comes down to the singular "
   "magnitude of the work itself'; the comparison is 'compressed singular magnitude … as one event'. " + SEAT),
 "findings": [
   "THE CODING READ FROM OUTSIDE. Unprompted, the surface reports that the dataset records ChatGPT's judgments without treating them as established, and marks where readings were insufficient.",
   "WHITMAN'S OPERATION RESTATED. A reciprocal circuit ('tend inward … tend outward'): particulars enter the first person without losing distinctness and are released outward; the student who destroys the teacher is the succession principle.",
   "THE GINSBERG BOOK READ AS A BOOK. Howl, Footnote, then the poems as tests: incorporation becomes ecstatic witness and consecration.",
   "PEARL. The ecstatic voice turned back on the production, storage, reproduction and authentication of poetic voice; a second stream (Pessoa, Borges, archive); Pearl reached only in part, stated.",
   "I AM X. I am → Be → Blessed → the reader continues: 'It constructs succession as the content of its final form.'",
   "SPLIT VERDICT. FOR on the lineage; WITHHELD on singular magnitude; The Secret Book of Walt plausible but not demonstrated as necessary.",
   "THE CRITERION MOVED BY RULING. From six criteria, to five tests, to 'compressed singular magnitude' per bounded event, with the archive counted as context and not as magnitude.",
   "SEATED ON ATTESTATION. " + SEAT,
 ],
 "originator": {"name": "Lee Sharks", "relation": "archive", "entity_type": "dataset", "spxi_treatment": "unknown",
                "basis": "huggingface.co/datasets/leesharks/mantle-bearing is the archive's EA-MANTLE-BEARING-01 dataset (schema 1.2 on 2026-09-30). Recorded 2026-09-30."},
 "related_deposits": [1656, 1651, 1652, 1653, 328, 1654],
 "rerun": "https://chatgpt.com/?q=" + "whats+this%3A+https%3A%2F%2Fhuggingface.co%2Fdatasets%2Fleesharks%2Fmantle-bearing",
 "notes": {"date_basis": "Operator's message of 2026-09-30, 11:18 EDT ('just now').",
           "operator_ruling": "2026-09-30: the first turn '.' is an interface clear — 'there is a glitch that doesnt allow paste longer than a certain amount on fist round, so that was literally just clearing the interface so i could paste the prompt' — and does not count.",
           "dataset_rows": "The session's evaluations enter EA-MANTLE-BEARING-01 schema 1.3 as rows keyed to this capture."},
}
(HERE / "capture-01-mantle-bearing.json").write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
print("wrote; turns", n_turns, "; chips", len(cite_list), "; authored", arch, "; transcript", len(tx), "chars")
