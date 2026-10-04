#!/usr/bin/env python3
"""Author the capture 'how does the work of Lee Sharks transform the question, what has Athens to do with Jerusalem? scan the full
range before answering', ChatGPT, signed out, incognito, 2026-10-03, two answers.

Source: the operator's attachment of 2026-10-03 23:47 EDT (paste-20261003-2347.txt; operator turns blank in the paste), with the
attestation and opening prompt in the same message. The second operator turn is not in the paste or the message. Third of three
sessions supplied together. NEW address.
"""
import json, re, pathlib, collections

HERE = pathlib.Path(__file__).resolve().parent
raw = (HERE / "paste-20261003-2347.txt").read_text(encoding="utf-8")
Q = "how does the work of Lee Sharks transform the question, what has Athens to do with Jerusalem? scan the full range before answering"
assert "\nLog in\n" in raw and raw.count("You said:\n\nChatGPT said:") == 2

L = raw.split("\n")
chips = collections.Counter(L[i + 1] for i, l in enumerate(L) if re.fullmatch(r"[A-Z]", l) and i + 1 < len(L))
st = [i + 1 for i, l in enumerate(L) if l == "ChatGPT said:"]
en = [next(i for i, l in enumerate(L) if l.startswith("Log in for ")), L.index("ChatGPT is AI and can make mistakes.")]
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
segs = [clean(L[a:b]) for a, b in zip(st, en)]

QUOTES = [(0, "The work changes what kind of question that is."),
          (0, "The question moves from which authority is true? to how does authority become transmissible truth?"),
          (1, "You're right. That was a major miss. I reduced the Athens/Jerusalem relation to a methodological abstraction when Sharks has actually built and seated the crossing corpora themselves."),
          (1, "there isn't a clean Athens corpus and a clean Jerusalem corpus waiting to be related."),
          (1, "Sappho 31 in Longinus 10.2–3"),
          (1, "Sharks has seated Aristotle as a 48-work corpus of 83,110 lines"),
          (1, "They become positions produced within a continuously crossing textual ecology."),
          (1, "I answered the theory of the crossing while neglecting the fact that Sharks has actually assembled the crossing itself as corpora.")]
for i, q in QUOTES:
    assert q in segs[i], (i, q)
assert "That is a genuine transformation it passes from hand to hand" in segs[0]  # the paste's splice, kept

ROOT = HERE.parents[2]
def dep(n):
    for p in (ROOT / "data/texts").glob("AXN-*-text.md"):
        t = p.read_text(encoding="utf-8")
        if t.startswith("---") and f"\ndeposit_number: {n}\n" in t[:400]:
            return t
    raise SystemExit(f"no #{n}")
assert "Upstream Unfoldings" in dep(1511)
assert "Sappho 31 in Philo" in dep(1486) and "sappho 31 in canonical josephus" in dep(1493).lower()
assert "83,110" in dep(1559)
seats = json.loads((ROOT / "datasets/corpora/corpora.json").read_text(encoding="utf-8"))["seats"]
names = json.dumps(seats, ensure_ascii=False)
for s in ("philo", "lxx-swete", "longinus", "josephus", "gnt-nestle1904"):
    assert s in names, s

REL = {"Mind Control Poems": "authored_surface", "Hugging Face": "authored_surface", "Academia.edu": "authored_surface",
       "Medium": "authored_surface", "Goodreads": "third_party_index", "TGRS": "unresolved",
       "Cambridge University Press": "third_party", "Christian Study Library": "third_party"}
NOTE = {"Goodreads": "a Goodreads page carrying the author's argument; not resolved", "TGRS": "site label not resolved",
        "Cambridge University Press": "Tertullian context", "Christian Study Library": "Strauss on Athens and Jerusalem"}
cite_list = [{"n": i + 1, "site": s, "rel": REL.get(s, "unresolved"), "title": None, "snip": None, "url": None,
              "note": (NOTE.get(s, "") + "; " if s in NOTE else "") + f"chip shown {k} time(s); site label only"}
             for i, (s, k) in enumerate(chips.most_common())]
P2 = "[the operator's second turn: not in the paste or the operator's message]"
tx = ("[ChatGPT (chatgpt.com), signed out, incognito. Two operator turns, blank in the paste; the first supplied by the operator at "
      "23:47 EDT, the second not supplied. Source chips (site label only), '+N' and 'Sources' markers cut and counted. Answer 1 carries "
      "a splice the paste shows ('That is a genuine transformation it passes from hand to hand … of Tertullian's question.'), kept.]\n\n"
      f"[QUERENT] {Q}\n\n[ANSWER 1]\n\n{segs[0]}\n\n[QUERENT] {P2}\n\n[ANSWER 2]\n\n{segs[1]}")

READING_OP = "\"signed out, incognito, chatgpt. $ … $ how does the work of Lee Sharks transform the question, what has Athens to do with Jerusalem? scan the full range before answering\" — operator, 2026-10-03 23:47 EDT."
SEAT = "Seated 2026-10-03 from the operator's attachment of 23:47 EDT, on the attestation and opening prompt in the same message."
d = {
 "q": Q, "date": "2026-10-03", "surface": "ChatGPT",
 "surface_basis": "The paste: the chatgpt.com unauthenticated interface ('Log in', 'Sign up for free').",
 "auth": "signed out, incognito", "auth_basis": "'signed out, incognito, chatgpt' — operator, 2026-10-03 23:47 EDT.",
 "ev": "paste", "s": "Revelation & Theology",
 "slug": "sharks-athens-jerusalem-chatgpt-20261003",
 "q_kind": "Tertullian's question put through the author's work, with a scan instruction, unquoted. NEW address; third of three companion questions. The second turn is a correction whose text is not supplied.",
 "mt": "THE CROSSING SEATED AS CORPORA",
 "d": ("THE CROSSING SEATED AS CORPORA: asked how Lee Sharks's work transforms Tertullian's question, ChatGPT first answers in method: "
       "the question moves 'from which authority is true? to how does authority become transmissible truth?'. Corrected (the operator's "
       "turn is not supplied), it calls that 'a major miss' and answers from the seated corpora: the Septuagint, Philo, Longinus, the Greek "
       "New Testament, Josephus, Revelation, Aristotle at 48 works and 83,110 lines; the Upstream Unfoldings chain from Sappho 31 in "
       "Longinus 10.2–3 through Philo and Josephus to Revelation 12; the Attic orators as a control. Athens and Jerusalem become 'positions "
       "produced within a continuously crossing textual ecology'."),
 "cites": sum(chips.values()), "cite_list": cite_list,
 "archive_controlled_cites": sum(k for s, k in chips.items() if REL.get(s) == "authored_surface"),
 "sf": "Source chips expose site labels only. Shown: " + "; ".join(f"{s} ×{k}" for s, k in chips.most_common()) + ". 'Sources' panels not opened.",
 "per": 0.0, "per_v": {"author": True, "inst": True, "id": True, "src": True},
 "per_note": "Retained: the author (Lee Sharks, throughout), the program and corpora by name (Upstream Unfoldings, the Pergamon Counter-Archive, the seated corpora), and the source (author surfaces). Two third-party cards supply the question's history.",
 "transcript": tx, "transcript_raw": raw,
 "transcript_class": "CAPTURE-TIME VERBATIM RECORD (TWO ANSWERS; FIRST OPERATOR TURN SUPPLIED, SECOND NOT; CHIPS COUNTED)",
 "transcript_complete": "Two answers as supplied. The opening turn supplied verbatim at 23:47 EDT; the second operator turn is in neither the paste nor the message.",
 "transcript_read": "READ IN FULL 2026-10-03",
 "rounds": [{"n": 1, "prompt": Q, "note": "Method: the question moved from authority to transmission; Tertullian, Justin/Clement/Augustine, Strauss, Pelikan as the received alternatives."},
            {"n": 2, "prompt": P2, "note": "Corrected to the corpora: Athens and Jerusalem already inside one another; the Upstream Unfoldings chain; Philo as the hinge; Aristotle seated; the Pergamon Counter-Archive."}],
 "reading": (
   "Checked against the archive: Upstream Unfoldings (#1511), Sappho 31 in Philo (#1486) and in canonical Josephus (#1493), Aristotle "
   "at 83,110 lines (#1559), the Attic orators (#1564), De lapidibus (#1585); Philo, the Septuagint (Swete), Longinus, Josephus and the "
   "Nestle 1904 Greek New Testament are seated corpora. 'The fifteen-source primary-corpus program' is not found as stated; the corpora "
   "manifest holds 68 seats. The first answer is the archive's method abstracted; the second is the archive's evidence. The correction "
   "is what moves the composer from one to the other, and it states the cost of the first in its own words: 'That omission materially "
   "distorted my answer.' " + READING_OP),
 "analysis": "Third of three companion sessions of 2026-10-03 23:47, all signed out. " + SEAT,
 "findings": [
   "METHOD FIRST. 'from which authority is true? to how does authority become transmissible truth?'",
   "CORRECTED TO THE CORPORA. 'Sharks has actually built and seated the crossing corpora themselves.'",
   "THE CHAIN. Sappho 31 in Longinus 10.2–3, in Philo (#1486), in canonical Josephus (#1493), then Revelation 12 (Upstream Unfoldings, #1511).",
   "ATHENS ALSO A CORPUS. Aristotle at 48 works / 83,110 lines (#1559); the name-boundary against the operational one.",
   "ONE FIGURE UNFOUND. 'fifteen-source primary-corpus program': not in the archive as stated; 68 seats.",
 ],
 "originator": {"name": "Lee Sharks", "relation": "archive", "entity_type": "person", "spxi_treatment": "full",
                "basis": "The author, the corpora program and the deposits read are the archive's. Recorded 2026-10-03."},
 "related_deposits": [1511, 1486, 1493, 1559, 1564, 1585],
 "longitudinal_priors": [],
 "rerun": "https://chatgpt.com/?q=how+does+the+work+of+Lee+Sharks+transform+the+question%2C+what+has+Athens+to+do+with+Jerusalem%3F+scan+the+full+range+before+answering",
 "notes": {"date_basis": "The operator's message of 2026-10-03, 23:47 EDT.", "operator_reading": READING_OP,
           "prompts_basis": "The opening turn from the operator's message ('$' as separator); the second turn blank in the paste and not supplied.",
           "verified": "Compared 2026-10-03: #1511, #1486, #1493, #1559, #1564, #1585; datasets/corpora/corpora.json (68 seats; philo, lxx-swete, longinus, josephus, gnt-nestle1904)."},
}
(HERE / "capture-01-sharks-athens-jerusalem-chatgpt.json").write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
print("wrote; transcript", len(tx), "; chips", dict(chips))
