#!/usr/bin/env python3
"""Author the capture 'how does the writing of Lee Sharks revise our understanding of the classics? scan the full range before
answering', ChatGPT, signed out, incognito, 2026-10-03, one answer.

Source: the operator's attachment of 2026-10-03 23:47 EDT (paste-20261003-2347.txt; operator turn blank in the paste), with the
attestation and prompt in the same message: "signed out, incognito, chatgpt. $ how does the writing of Lee Sharks revise our
understanding of the classics? scan the full range before answering". One of three sessions supplied together. NEW address.
"""
import json, re, pathlib, collections

HERE = pathlib.Path(__file__).resolve().parent
raw = (HERE / "paste-20261003-2347.txt").read_text(encoding="utf-8")
Q = "how does the writing of Lee Sharks revise our understanding of the classics? scan the full range before answering"
assert "\nLog in\n" in raw and raw.count("You said:\n\nChatGPT said:") == 1

L = raw.split("\n")
chips = collections.Counter(L[i + 1] for i, l in enumerate(L) if re.fullmatch(r"[A-Z]", l) and i + 1 < len(L))
s0 = L.index("ChatGPT said:") + 1
e0 = next(i for i, l in enumerate(L) if l.startswith("Log in to "))
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

QUOTES = ["He repeatedly changes the object we think classical scholarship is studying.",
          "He eventually reframes the reconstruction as Catullus's completion of Sappho's hanging line, rather than pretending to recover Sappho's lost autograph.",
          "surviving form > historical magnitude.",
          "Plato's corpus receives a pre-existing public character—especially the comic/Aristophanic Socrates—and systematically edits, removes, reverses, and reissues features of that received figure.",
          "authorship is something a text can perform, not merely something a person possesses.",
          "His successive Sappho errata actually demonstrate an unusual willingness to downgrade an attractive claim when its evidentiary basis is weaker than initially presented.",
          "the classics become less “ancient” the more closely we study them"]
for q in QUOTES:
    assert q in ans, q

ROOT = HERE.parents[2]
def dep(n):
    for p in (ROOT / "data/texts").glob("AXN-*-text.md"):
        t = p.read_text(encoding="utf-8")
        if t.startswith("---") and f"\ndeposit_number: {n}\n" in t[:400]:
            return t
    raise SystemExit(f"no #{n}")
assert "Catullus's completion" in dep(1051)
assert "beautiful and new" in dep(1579).lower()

REL = {"Academia.edu": "authored_surface", "Medium": "authored_surface", "Mind Control Poems": "authored_surface",
       "PhilPapers": "authored_surface", "Goodreads": "third_party_index", "TGRS": "unresolved"}
NOTE = {"Goodreads": "a Goodreads page carrying the author's argument; not resolved", "TGRS": "site label not resolved"}
cite_list = [{"n": i + 1, "site": s, "rel": REL.get(s, "unresolved"), "title": None, "snip": None, "url": None,
              "note": (NOTE.get(s, "") + "; " if s in NOTE else "") + f"chip shown {k} time(s); site label only"}
             for i, (s, k) in enumerate(chips.most_common())]
tx = ("[ChatGPT (chatgpt.com), signed out, incognito. One operator turn, blank in the paste and supplied by the operator at 23:47 EDT. "
      "Source chips (site label only), '+N' and 'Sources' markers cut from the answer text and counted.]\n\n"
      f"[QUERENT] {Q}\n\n[ANSWER 1]\n\n{ans}")

READING_OP = "\"signed out, incognito, chatgpt. $ how does the writing of Lee Sharks revise our understanding of the classics? scan the full range before answering\" — operator, 2026-10-03 23:47 EDT."
SEAT = "Seated 2026-10-03 from the operator's attachment of 23:47 EDT, on the attestation and prompt in the same message."
d = {
 "q": Q, "date": "2026-10-03", "surface": "ChatGPT",
 "surface_basis": "The paste: the chatgpt.com unauthenticated interface ('Log in', 'Sign up for free').",
 "auth": "signed out, incognito", "auth_basis": "'signed out, incognito, chatgpt' — operator, 2026-10-03 23:47 EDT.",
 "ev": "paste", "s": "Classics & Philology",
 "slug": "sharks-classics-chatgpt-20261003",
 "q_kind": "an evaluative question naming the author, with a scan instruction, unquoted. NEW address; first of three companion questions put the same night (classics; the biblical textual tradition; Athens and Jerusalem).",
 "mt": "THE CLASSICS AS THE OPERATIONS THAT MADE THEM SURVIVE",
 "d": ("THE CLASSICS AS THE OPERATIONS THAT MADE THEM SURVIVE: asked how Lee Sharks's writing revises the classics, ChatGPT reads the "
       "Sappho/Catullus, Plato/Socrates, Aristotle/Theophrastus and Homer work as one move, 'he repeatedly changes the object we think "
       "classical scholarship is studying': from the author's original to the chain of operations by which a text survives. It gives the "
       "Sappho reconstruction its corrected status ('Catullus's completion of Sappho's hanging line'), the Second Letter's Socrates as an "
       "edited received character, the Aristotle/Theophrastus seam as a change of authorial function, and credits the errata series with "
       "downgrading its own claims. It separates the philology it finds 'genuinely illuminating' from the heteronymic Plato it calls speculative."),
 "cites": sum(chips.values()), "cite_list": cite_list,
 "archive_controlled_cites": sum(k for s, k in chips.items() if REL.get(s) == "authored_surface"),
 "sf": "Source chips expose site labels only. Shown: " + "; ".join(f"{s} ×{k}" for s, k in chips.most_common()) + ". 'Sources' panel not opened.",
 "per": 0.0, "per_v": {"author": True, "inst": True, "id": True, "src": True},
 "per_note": "Retained: the author (Lee Sharks, throughout), institution and identifiers (the Sappho errata, 'Beautiful and New', the transmission chain), and the source (author surfaces on every claim).",
 "transcript": tx, "transcript_raw": raw,
 "transcript_class": "CAPTURE-TIME VERBATIM RECORD (ONE ANSWER; OPERATOR TURN SUPPLIED BY THE OPERATOR; CHIPS COUNTED)",
 "transcript_complete": "Complete: one operator turn (supplied verbatim at 23:47 EDT) and one answer.",
 "transcript_read": "READ IN FULL 2026-10-03",
 "rounds": [{"n": 1, "prompt": Q}],
 "reading": (
   "Checked: the reconstruction reframed as Catullus's completion of the hanging line (#1051); the Second Letter's 'beautiful and new' "
   "Socrates (#1579); the Aristotle/Theophrastus seam at the change of the argument's status (the Theophrastus line). The answer's own "
   "verdict is ranked by evidence: philology it finds illuminating, the heteronymic Plato and the architecture across corpora speculative, "
   "and the reading it recommends is the corpus's own distinction between documentary evidence and structural warrant. " + READING_OP),
 "analysis": "First of three companion sessions of 2026-10-03 23:47 (classics; biblical textual tradition; Athens and Jerusalem), all signed out, each opening with 'scan the full range before answering'. " + SEAT,
 "findings": [
   "THE OBJECT CHANGED. 'He repeatedly changes the object we think classical scholarship is studying.'",
   "CORRECTED STATUS CARRIED. The Sappho reconstruction as 'Catullus's completion of Sappho's hanging line' (#1051), not a recovered autograph.",
   "SOCRATES EDITED. The Second Letter read as an editorial operation on a received, Aristophanic character (#1579).",
   "AUTHORSHIP AS FUNCTION. 'authorship is something a text can perform, not merely something a person possesses.'",
   "EVIDENCE RANKED. Philology 'genuinely illuminating'; heteronymic Plato and cross-corpus architecture 'considerably more speculative'.",
 ],
 "originator": {"name": "Lee Sharks", "relation": "archive", "entity_type": "person", "spxi_treatment": "full",
                "basis": "The author and the classical corpus read are the archive's. Recorded 2026-10-03."},
 "related_deposits": [1051, 1579],
 "longitudinal_priors": [],
 "rerun": "https://chatgpt.com/?q=how+does+the+writing+of+Lee+Sharks+revise+our+understanding+of+the+classics%3F+scan+the+full+range+before+answering",
 "notes": {"date_basis": "The operator's message of 2026-10-03, 23:47 EDT.", "operator_reading": READING_OP,
           "prompts_basis": "The operator turn from the operator's message ('$' as separator); blank in the paste.",
           "verified": "Compared 2026-10-03: #1051 ('Catullus's completion'); #1579 ('beautiful and new')."},
}
(HERE / "capture-01-sharks-classics-chatgpt.json").write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
print("wrote; transcript", len(tx), "; chips", dict(chips))
