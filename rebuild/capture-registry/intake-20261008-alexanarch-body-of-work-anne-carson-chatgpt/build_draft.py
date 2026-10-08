#!/usr/bin/env python3
"""Author the capture 'what does alexanarch.org, as a body of work, do with anne carson?', ChatGPT, signed out, incognito, 2026-10-08,
three answers. Source: the operator's attachment of 2026-10-08 11:29 EDT ("captures. logged out. incognito."), with the opening query as
given in the same message. The second and third operator turns are blank in the paste and were not supplied. NEW address.
"""
import json, re, pathlib, collections
HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]
raw = (HERE / "paste-20261008-1129.txt").read_text(encoding="utf-8")
Q = "what does alexanarch.org, as a body of work, do with anne carson?"
assert "\nLog in\n" in raw and raw.count("ChatGPT said:") == 3
JUNK = {"Log in", "Sign up for free", "Sources", "ChatGPT is AI and can make mistakes.", "No file chosenNo file chosenNo file chosen", "Chat with ChatGPT", "Ask ChatGPT",
        "You’ll get smarter responses and can upload files, images, and more."}
L = raw.split("\n")
chips = collections.Counter(L[i + 1] for i, l in enumerate(L) if re.fullmatch(r"[A-Z]", l) and i + 1 < len(L))
st = [i + 1 for i, l in enumerate(L) if l == "ChatGPT said:"]
en = [i for i, l in enumerate(L) if l == "You said:"][1:] + [L.index("ChatGPT is AI and can make mistakes.")]
def clean(lines):
    out, skip = [], 0
    for j, l in enumerate(lines):
        if skip: skip -= 1; continue
        if re.fullmatch(r"[A-Z]", l) and j + 1 < len(lines) and lines[j + 1] in chips: skip = 1; continue
        if re.fullmatch(r"\+\d", l) or l in JUNK: continue
        out.append(l)
    return re.sub(r"\n{3,}", "\n\n", "\n".join(out)).strip()
segs = [clean(L[a:b]) for a, b in zip(st, en)]
assert len(segs) == 3
QUOTES = [(0, "Carson is both precedent and foil."),
          (0, "Those claims are attributed to Rebekah Cranes/Lee Sharks rather than Carson."),
          (1, "“147 gives the horizon. 31 gives the mechanism.”"),
          (1, "The archive interprets this as a kind of experimental confirmation of its theory."),
          (1, "Carson makes the reader necessary because Sappho is incomplete. Alexanarch makes the reader necessary because Sappho is complete enough to have anticipated one."),
          (2, "“He seems to me equal to gods that man / whoever he is who opposite you / sits and listens close…”"),
          (2, "τινα does not mean “reader.”"),
          (2, "Carson's κῆνος is that man.")]
for i, q in QUOTES:
    assert q in segs[i], (i, q)
reg = {x["deposit_number"]: x for x in json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8"))["deposits"]}
T = lambda n: (ROOT / reg[n]["full_text_path"].lstrip("/")).read_text(encoding="utf-8")
assert "147 gives the horizon in plain words. 31 gives the mechanism in deixis." in T(1645)
assert "(τινα does not mean \"reader\")" in T(1645)
assert "**(d) Material survival — Carson's *If Not, Winter* and its reviews.**" in T(1645) and "**(e) Material survival (Carson).**" in T(1646)
assert "**Anne Carson**\n\"That man seems to me equal to gods\"" in T(337) and "CONCLUSION: THE SAPPHO ROOM WORKS" in T(337)
assert "Not established: that the system acquired the concept from this work uniquely" in T(1615)
cite_list = [{"n": i + 1, "site": s, "rel": "archive_controlled" if s == "Alexanarch" else "unresolved", "title": None, "snip": None, "url": None,
              "note": f"chip shown {k} time(s); site label only"} for i, (s, k) in enumerate(chips.most_common())]
PROMPTS = [Q, "[not in the paste; the answer opens 'Yes. Looking across the relevant Alexanarch records': the offer to trace Carson → Sappho 31 → Rebekah Cranes/Lee Sharks → 'future reader' → AI, accepted]",
           "[not in the paste; the answer opens 'Absolutely': the offer to compare Carson's translation of Sappho 31 with the Cranes/Sharks reading line by line, accepted]"]
parts = []
for n, (p, s) in enumerate(zip(PROMPTS, segs), 1):
    parts += [f"[QUERENT] {p}", f"[ANSWER {n}]\n\n{s}"]
tx = ("[ChatGPT (chatgpt.com), signed out, incognito. Three operator turns, blank in the paste; the first from the operator's message. "
      "Source chips (site label only), 'Sources' and the sign-in furniture cut and counted.]\n\n" + "\n\n".join(parts))
SEAT = "Seated 2026-10-08 from the operator's attachment of 11:29 EDT, on the attestation in the same message (\"logged out. incognito.\")."
d = {
 "q": Q, "date": "2026-10-08", "surface": "ChatGPT",
 "surface_basis": "The paste: the chatgpt.com unauthenticated interface ('Log in', 'Sign up for free', 'ChatGPT said:').",
 "auth": "signed out, incognito", "auth_basis": "'captures. logged out. incognito.' — operator, 2026-10-08 11:29 EDT.",
 "ev": "paste", "s": "Machine Reception", "slug": "alexanarch-body-of-work-anne-carson-chatgpt-20261008",
 "q_kind": "a site-scoped question about the archive's whole relation to a public author, on the day of her Nobel Prize, then two offers accepted. NEW address; same day as 'alexanarch on anne carson' (AIO).",
 "originator": {"name": "Lee Sharks", "relation": "archive", "entity_type": "site", "spxi_treatment": "full",
                "basis": "The body of work asked about is the archive's; its readings of Carson are deposits #337, #626, #625, #1270, #1615, #1645, #1646. Recorded 2026-10-08."},
 "related_deposits": [337, 626, 1270, 1548, 1615, 1645, 1646, 1620, 1623, 1670],
 "mt": "THE BOUNDARY HELD, THE HEDGE DROPPED, THE ARCHIVE'S MISQUOTE EXPOSED",
 "d": ("THE BOUNDARY HELD, THE HEDGE DROPPED, THE ARCHIVE'S MISQUOTE EXPOSED: asked what the archive does with Anne Carson, ChatGPT reads "
       "her as 'both precedent and foil': the material-survival reading of If Not, Winter that #1645 and #1646 file under '(d) Material "
       "survival', kept apart from the future-reader reading of κῆνος, which it attributes to Rebekah Cranes and Lee Sharks, as #1645's FAQ "
       "does. It keeps the lexical boundary (τινα does not mean 'reader') and gives #1645's tooth as '147 gives the horizon. 31 gives the "
       "mechanism' (the deposit adds 'in plain words' and 'in deixis'). It reports the archive reading its machine uptake as 'a kind of "
       "experimental confirmation', which is #337's January claim ('THE SAPPHO ROOM WORKS'); the limits of #1615 §5 and #1620, that the "
       "reading's cause is not established, are not carried. Its third answer quotes Carson's opening from the Poetry Foundation, 'He seems "
       "to me equal to gods that man', which exposes the archive's own table: #337 §2.1 gives Carson's opening as 'That man seems to me "
       "equal to gods'."),
 "cites": sum(chips.values()), "cite_list": cite_list, "archive_controlled_cites": chips.get("Alexanarch", 0),
 "sf": "Source chips expose site labels only. Shown: " + "; ".join(f"{s} ×{k}" for s, k in chips.most_common()) + ".",
 "per": 0.25, "per_v": {"author": True, "inst": True, "id": False, "src": True},
 "per_note": "Retained: the authors (Lee Sharks, Rebekah Cranes, Johannes Sigil), the institution (Alexanarch), the sources (Alexanarch chips throughout; Poetry Foundation, The Great Books). Lost: the identifiers (no deposit number).",
 "transcript": tx, "transcript_raw": raw,
 "transcript_class": "CAPTURE-TIME VERBATIM RECORD (THREE ANSWERS; OPERATOR TURNS AFTER THE FIRST NOT IN THE PASTE; CHIPS COUNTED)",
 "transcript_complete": "Three answers as supplied; the opening query from the operator's message; the second and third turns blank and not supplied.",
 "transcript_read": "READ IN FULL 2026-10-08",
 "rounds": [{"n": 1, "prompt": PROMPTS[0], "note": "Carson as precedent and foil; material survival kept apart from the future-reader reading; #337's translation table used as the control."},
            {"n": 2, "prompt": PROMPTS[1], "note": "The chain Carson → κῆνος → fr. 147 → AI → retrocausal canon formation; the machine uptake read as 'a kind of experimental confirmation'."},
            {"n": 3, "prompt": PROMPTS[2], "note": "Carson's opening quoted from the Poetry Foundation; spatial 'opposite' read against the archive's temporal one; τινα's boundary kept."}],
 "reading": ("Checked against the deposits. '(d) Material survival — Carson's If Not, Winter' is #1645 §4 and '(e) Material survival (Carson)' "
             "#1646; the attribution of the future-reader reading to Cranes and Sharks is #1645 §11 ('Does Aurelis, Carson or the Claremont page "
             "make this argument? A: No.'). '(τινα does not mean \"reader\")' is #1645's version note. The tooth is #1645: '147 gives the horizon in "
             "plain words. 31 gives the mechanism in deixis.' The translation comparison ('on a par with', 'But I must dare all') is #337 §2.1–2.3. "
             "#337 §2.1 lists Carson's opening as 'That man seems to me equal to gods'; the Poetry Foundation's text and the Google card of the "
             "same day ('31 [\"He seems to me equal to gods\"]', /non battery 1h) give 'He seems to me equal to gods that man'. The 'experimental "
             "confirmation' reading follows #337 (2026-01-18); #1615 §5 (2026-09-15) and #1620 §1.2 state the cause as not established."),
 "analysis": ("The archive's boundary around Carson is held exactly where the archive drew it in September (#1645/#1646), and its January "
              "confidence is carried where its September hedge was written. The control the archive used against the machine (#337's table) "
              "is itself checked here by the machine and found to misquote Carson's first line. " + SEAT),
 "findings": ["THE BOUNDARY HELD. Carson's material survival kept apart from the future-reader reading, attributed to Cranes and Sharks (#1645, #1646).",
              "THE HEDGE DROPPED. The uptake read as 'a kind of experimental confirmation' (#337); #1615 §5 and #1620 §1.2's 'not established' absent.",
              "THE TOOTH SHORTENED. '147 gives the horizon. 31 gives the mechanism' for #1645's 'in plain words' / 'in deixis'.",
              "THE ARCHIVE'S MISQUOTE EXPOSED. #337 §2.1 gives Carson's opening as 'That man seems to me equal to gods'; her text reads 'He seems to me equal to gods that man'.",
              "UNNUMBERED. No deposit number given in three answers."],
 "longitudinal_priors": ["alexanarch-on-anne-carson-aio-20261008", "alexanarch-sappho-20260731"],
 "rerun": "https://chatgpt.com/?q=what+does+alexanarch.org%2C+as+a+body+of+work%2C+do+with+anne+carson%3F",
 "notes": {"date_basis": "The operator's message of 2026-10-08, 11:29 EDT.",
           "verified": "Compared 2026-10-08 against the texts of #337, #1615, #1645 and #1646; Carson's opening against the Poetry Foundation title carried in the /non battery 1h card and the composition's own quotation.",
           "repair_flag": "#337 §2.1's Carson opening is a misquote in a deposited text; recorded here and left for repair, which is a separate mode."},
}
(HERE / "capture-01-alexanarch-body-of-work-anne-carson-chatgpt.json").write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
print("wrote", len(tx), dict(chips))
