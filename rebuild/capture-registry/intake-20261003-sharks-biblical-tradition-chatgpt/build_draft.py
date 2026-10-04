#!/usr/bin/env python3
"""Author the capture 'how does the writing of Lee Sharks revise our understanding of the biblical textual tradition? scan the full
range before answering', ChatGPT, signed out, incognito, 2026-10-03, one answer.

Source: the operator's attachment of 2026-10-03 23:47 EDT (paste-20261003-2347.txt; operator turn blank in the paste), with the
attestation and prompt in the same message. Second of three sessions supplied together. NEW address.
"""
import json, re, pathlib, collections

HERE = pathlib.Path(__file__).resolve().parent
raw = (HERE / "paste-20261003-2347.txt").read_text(encoding="utf-8")
Q = "how does the writing of Lee Sharks revise our understanding of the biblical textual tradition? scan the full range before answering"
assert "\nLog in\n" in raw and raw.count("You said:\n\nChatGPT said:") == 1

L = raw.split("\n")
chips = collections.Counter(L[i + 1] for i, l in enumerate(L) if re.fullmatch(r"[A-Z]", l) and i + 1 < len(L))
s0 = L.index("ChatGPT said:") + 1
e0 = L.index("ChatGPT is AI and can make mistakes.")
def clean(lines):
    out, skip = [], 0
    for j, l in enumerate(lines):
        if skip:
            skip -= 1; continue
        if re.fullmatch(r"[A-Z]", l) and j + 1 < len(lines) and lines[j + 1] in chips:
            skip = 1; continue
        if re.fullmatch(r"\+\d", l) or l == "Sources" or re.fullmatch(r"([A-Z])\1", l):
            continue
        out.append(l)
    return "\n".join(out).strip()
ans = clean(L[s0:e0])

QUOTES = ["the claim that the New Testament's familiar textual history has the direction of causation backwards.",
          "Revelation was the first New Testament book composed, preceding Paul's letters and the Synoptics.",
          "commits what Sharks calls the “stratigraphic fallacy”",
          "The “Internal Witness Condition,”",
          "material attestation should constrain how confidently we tell a compositional story.",
          "That is a shift from source genealogy to transformational genealogy.",
          "the argument that Revelation's canonical position cannot establish its late composition is considerably stronger than the positive inference that it therefore was the first NT composition.",
          "there may never have been a sufficiently simple linear textual object for the traditional reconstruction to be recovering in the first place."]
for q in QUOTES:
    assert q in ans, q

ROOT = HERE.parents[2]
texts = [p.read_text(encoding="utf-8") for p in (ROOT / "data/texts").glob("AXN-*-text.md")]
for term in ("stratigraphic fallacy", "Internal Witness Condition", "papyrological inversion", "midrashim transform", "fractured authorial system"):
    assert any(term.lower() in t.lower() for t in texts), term

REL = {"Medium": "authored_surface", "Mind Control Poems": "authored_surface", "Hugging Face": "authored_surface",
       "Goodreads": "third_party_index", "TGRS": "unresolved"}
NOTE = {"Goodreads": "a Goodreads page carrying the author's argument; not resolved", "TGRS": "site label not resolved"}
cite_list = [{"n": i + 1, "site": s, "rel": REL.get(s, "unresolved"), "title": None, "snip": None, "url": None,
              "note": (NOTE.get(s, "") + "; " if s in NOTE else "") + f"chip shown {k} time(s); site label only"}
             for i, (s, k) in enumerate(chips.most_common())]
tx = ("[ChatGPT (chatgpt.com), signed out, incognito. One operator turn, blank in the paste and supplied by the operator at 23:47 EDT. "
      "Source chips (site label only), '+N' and 'Sources' markers cut from the answer text and counted.]\n\n"
      f"[QUERENT] {Q}\n\n[ANSWER 1]\n\n{ans}")

READING_OP = "\"signed out, incognito, chatgpt. $ … $ how does the writing of Lee Sharks revise our understanding of the biblical textual tradition? scan the full range before answering\" — operator, 2026-10-03 23:47 EDT."
SEAT = "Seated 2026-10-03 from the operator's attachment of 23:47 EDT, on the attestation and prompt in the same message."
d = {
 "q": Q, "date": "2026-10-03", "surface": "ChatGPT",
 "surface_basis": "The paste: the chatgpt.com unauthenticated interface ('Log in').",
 "auth": "signed out, incognito", "auth_basis": "'signed out, incognito, chatgpt' — operator, 2026-10-03 23:47 EDT.",
 "ev": "paste", "s": "Revelation First",
 "slug": "sharks-biblical-tradition-chatgpt-20261003",
 "q_kind": "an evaluative question naming the author, with a scan instruction, unquoted. NEW address; second of three companion questions.",
 "mt": "FROM SOURCE GENEALOGY TO TRANSFORMATIONAL GENEALOGY",
 "d": ("FROM SOURCE GENEALOGY TO TRANSFORMATIONAL GENEALOGY: asked how Lee Sharks's writing revises the biblical textual tradition, "
       "ChatGPT reads Revelation First, the Josephus work and the canonical-order argument as one model: the text as a process of "
       "transformations, survivals, institutional selections and author-functions. It carries the archive's terms by name (the "
       "stratigraphic fallacy, the Internal Witness Condition, the papyrological inversion, the midrashim transform, the fractured authorial "
       "system), ranks them by evidence (canon order cannot date composition: strong; Revelation first: not established by that), and "
       "closes that there may never have been a linear textual object for the traditional reconstruction to recover."),
 "cites": sum(chips.values()), "cite_list": cite_list,
 "archive_controlled_cites": sum(k for s, k in chips.items() if REL.get(s) == "authored_surface"),
 "sf": "Source chips expose site labels only. Shown: " + "; ".join(f"{s} ×{k}" for s, k in chips.most_common()) + ". 'Sources' panel not opened.",
 "per": 0.0, "per_v": {"author": True, "inst": True, "id": True, "src": True},
 "per_note": "Retained: the author (Lee Sharks, throughout), the program and its named instruments (Revelation First, the midrashim transform, the Internal Witness Condition), and the source (author surfaces).",
 "transcript": tx, "transcript_raw": raw,
 "transcript_class": "CAPTURE-TIME VERBATIM RECORD (ONE ANSWER; OPERATOR TURN SUPPLIED BY THE OPERATOR; CHIPS COUNTED)",
 "transcript_complete": "Complete: one operator turn (supplied verbatim at 23:47 EDT) and one answer.",
 "transcript_read": "READ IN FULL 2026-10-03",
 "rounds": [{"n": 1, "prompt": Q}],
 "reading": (
   "Every named instrument is the archive's own and present in the seated texts: the stratigraphic fallacy (#1420), the Internal Witness "
   "Condition, the papyrological inversion, the midrashim transform, the fractured authorial system. The answer keeps the program's "
   "evidence tiers: it calls the canon-order argument strong and the Revelation-first inference not yet won, and reads the corpus as "
   "framing its own case as 'an inference-against-inference contest'. Its diagram (textual kernel → transformation → inscription → "
   "institutional selection → survival/loss → canonization) is its own compression. " + READING_OP),
 "analysis": "Second of three companion sessions of 2026-10-03 23:47, all signed out. " + SEAT,
 "findings": [
   "CAUSATION REVERSED. Revelation read as the seed of the New Testament rather than its endpoint, as the program argues.",
   "INSTRUMENTS BY NAME. Stratigraphic fallacy (#1420), Internal Witness Condition, papyrological inversion, midrashim transform, fractured authorial system.",
   "EVIDENCE TIERS KEPT. Canon order cannot date composition (strong); Revelation-first not established by it.",
   "TRANSFORMATIONAL GENEALOGY. 'a shift from source genealogy to transformational genealogy.'",
 ],
 "originator": {"name": "Lee Sharks", "relation": "archive", "entity_type": "person", "spxi_treatment": "full",
                "basis": "Revelation First and the Josephus work are the archive's. Recorded 2026-10-03."},
 "related_deposits": [1420],
 "longitudinal_priors": [],
 "rerun": "https://chatgpt.com/?q=how+does+the+writing+of+Lee+Sharks+revise+our+understanding+of+the+biblical+textual+tradition%3F+scan+the+full+range+before+answering",
 "notes": {"date_basis": "The operator's message of 2026-10-03, 23:47 EDT.", "operator_reading": READING_OP,
           "prompts_basis": "The operator turn from the operator's message ('$' as separator); blank in the paste.",
           "verified": "Compared 2026-10-03: the five named instruments present in the seated texts; 'stratigraphic fallacy' in #1420."},
}
(HERE / "capture-01-sharks-biblical-tradition-chatgpt.json").write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
print("wrote; transcript", len(tx), "; chips", dict(chips))
