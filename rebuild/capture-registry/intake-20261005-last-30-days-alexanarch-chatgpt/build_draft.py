#!/usr/bin/env python3
"""Author the capture 'walk me thru the last 30 days of deposits on alexanarch.org as an evolving body of thought', ChatGPT,
signed out, incognito, 2026-10-05, two answers.

Source: the operator's attachment of 2026-10-05 21:19 EDT, with the batch attestation "logged out. incognito." and the prompt as given.
NEW address; the nearest seated is 'the last month or so of deposits to alexanarch.org as an evolving system of living thought'
(ChatGPT and Claude, 2026-09-27).
"""
import json, re, pathlib, collections
HERE = pathlib.Path(__file__).resolve().parent
raw = (HERE / "paste-20261005-2119.txt").read_text(encoding="utf-8")
Q = "walk me thru the last 30 days of deposits on alexanarch.org as an evolving body of thought"
assert "\nLog in\n" in raw and raw.count("ChatGPT said:") == 2
JUNK = {"Log in for personalized, step-by-step guidance.", "Log in", "Sign up for free", "Airtop", "AI Agents That Use Websites",
        "Build one without writing automation code.", "Ad"}
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
        if re.fullmatch(r"\+\d", l) or l == "Sources" or re.fullmatch(r"([A-Z])\1", l) or l in JUNK:
            continue
        out.append(l)
    return "\n".join(out).strip()
segs = [clean(L[a:b]) for a, b in zip(st, en)]
assert len(segs) == 2
QUOTES = [(0, "I’m treating the window as roughly September 5–October 5, 2026."),
          (0, "The first important deposit in this window is “Aristotle and Theophrastus ≠ Two Distinct Authors” on September 6."),
          (0, "authorship → attribution → mediation → trust → provenance → inheritance → semantic capital"),
          (0, "A work has to be able to carry its own evidence through the systems that describe it."),
          (1, "October changes the trajectory of the project."),
          (1, "“The Seed in the Narrowing Cone: Retrocausal Canon Formation as Resolution-Dependent Convergence,” EA-RCF-02 v0.4, October 2."),
          (1, "So yes: I skipped the most theoretically consequential part of the month.")]
for i, q in QUOTES:
    assert q in segs[i], (i, q)
ROOT = HERE.parents[2]
reg = {x["deposit_number"]: x for x in json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8"))["deposits"]}
WIN = sorted((x["date"], x["deposit_number"]) for x in reg.values() if "2026-09-05" <= (x.get("date") or "") <= "2026-10-05")
assert len(WIN) == 88
CITED = {1587: "2026-09-06", 1638: "2026-09-26", 1643: "2026-09-27", 1644: "2026-09-28", 1647: "2026-09-28", 1651: "2026-09-29",
         1652: "2026-09-29", 1653: "2026-09-29", 1657: "2026-09-30", 1658: "2026-10-01", 1660: "2026-10-02"}
for n, dt in CITED.items():
    assert reg[n]["date"] == dt, (n, reg[n]["date"])
assert reg[1660]["version"] == "v0.4" and reg[1658]["version"] == "v0.2"
OCT = [n for d, n in WIN if d >= "2026-10-01"]
assert OCT == [1658, 1659, 1660, 1661, 1662, 1663, 1664, 1665]
cite_list = [{"n": i + 1, "site": s, "rel": "archive_controlled" if s == "Alexanarch" else "unresolved", "title": None, "snip": None, "url": None,
              "note": f"chip shown {k} time(s); site label only"} for i, (s, k) in enumerate(chips.most_common())]
PROMPTS = [Q, "[not in the paste; the answer opens on a correction: the first answer stopped at September]"]
parts = []
for n, (p, s) in enumerate(zip(PROMPTS, segs), 1):
    parts += [f"[QUERENT] {p}", f"[ANSWER {n}]\n\n{s}"]
tx = ("[ChatGPT (chatgpt.com), signed out, incognito. Two operator turns, blank in the paste; the first from the operator's message. "
      "Source chips (site label only), 'Sources', a sign-in prompt and an advertisement cut and counted.]\n\n" + "\n\n".join(parts))
SEAT = "Seated 2026-10-05 from the operator's attachment of 21:19 EDT, on the attestation in the same message (\"logged out. incognito.\")."
d = {
 "q": Q, "date": "2026-10-05", "surface": "ChatGPT",
 "surface_basis": "The paste: the chatgpt.com unauthenticated interface ('Log in', 'Sign up for free').",
 "auth": "signed out, incognito", "auth_basis": "'logged out. incognito.' — operator, 2026-10-05 21:19 EDT.",
 "ev": "paste", "s": "Archive", "slug": "last-30-days-alexanarch-chatgpt-20261005",
 "q_kind": "a request to read a dated window of the archive's deposits as one development, then a second turn not in the paste. NEW address; nearest seated the 2026-09-27 'last month or so' captures.",
 "originator": {"name": "Lee Sharks", "relation": "archive", "entity_type": "site", "spxi_treatment": "full",
                "basis": "alexanarch.org and its deposits are the archive's. Recorded 2026-10-05."},
 "related_deposits": [1587, 1638, 1643, 1644, 1647, 1651, 1652, 1653, 1657, 1658, 1660],
 "mt": "A MONTH READ AS ONE ARGUMENT, TO OCTOBER 2",
 "d": ("A MONTH READ AS ONE ARGUMENT, TO OCTOBER 2: asked to read the last 30 days of deposits as a body of thought, ChatGPT sets the window "
       "at September 5 to October 5. It builds a sequence from eleven of the window's 88 deposits, from authorship to semantic capital, all "
       "dated correctly: Aristotle and Theophrastus, the Trusted Intermediary, AI Fucking Lies, Phase X, the mantles, the Crown and the "
       "Practice. It stops at September 30. Corrected, it adds What Syllogizing Can Divide (October 1) and The Seed in the Narrowing Cone "
       "(October 2) and redraws the arc around division, recollection and escape cost. The window's last six deposits are not in it: two "
       "glyphic checksums, the poems 'words no good' and 'hush, dear hands —', and EA-NEGONT-02 v0.6 and v0.7."),
 "cites": sum(chips.values()), "cite_list": cite_list, "archive_controlled_cites": chips.get("Alexanarch", 0),
 "sf": "Source chips expose site labels only. Shown: " + "; ".join(f"{s} ×{k}" for s, k in chips.most_common()) + ".",
 "per": 0.25, "per_v": {"author": True, "inst": True, "id": False, "src": True},
 "per_note": "Retained: the author, the institution (alexanarch.org), the sources (Alexanarch chips throughout). Lost: the identifiers (no deposit number, AXN or DOI).",
 "transcript": tx, "transcript_raw": raw,
 "transcript_class": "CAPTURE-TIME VERBATIM RECORD (TWO ANSWERS; THE SECOND OPERATOR TURN NOT IN THE PASTE; CHIPS COUNTED)",
 "transcript_complete": "Two answers as supplied; the opening query from the operator's message; the second turn blank and not supplied.",
 "transcript_read": "READ IN FULL 2026-10-05",
 "rounds": [{"n": 1, "prompt": PROMPTS[0], "note": "September 6–30 as one sequence; stops at September 30."},
            {"n": 2, "prompt": PROMPTS[1], "note": "October 1–2 added; the arc redrawn; 'I skipped the most theoretically consequential part of the month.'"}],
 "reading": ("Checked against the registry: the window holds 88 deposits; every one the composer names is dated as it says (#1587 September 6, "
             "#1638 September 26, #1643 September 27, #1644 and #1647 September 28, #1651–#1653 September 29, #1657 September 30, #1658 "
             "October 1 at v0.2, #1660 October 2 at v0.4). The reading is a selection of eleven, all argumentative papers, arranged as a "
             "sequence of questions. It leaves out the window's poems ('words no good' and 'hush, dear hands —', #1662–#1663) and its "
             "checksums. The first answer ends a month early and is corrected on a turn not in the paste. The second still ends on October 2, "
             "three days short of the window it set, before EA-NEGONT-02 (#1664, October 4; #1665, October 5)."),
 "analysis": "A month of deposits composed as one argument at the grain of its papers; the window's end and its poems fall outside it. Companion to the 2026-09-27 'last month or so' captures. " + SEAT,
 "findings": ["THE WINDOW SET, THEN NOT REACHED. September 5–October 5 declared; the first answer ends on September 30, the second on October 2.",
              "ELEVEN OF 88, DATED CORRECTLY. Every named deposit's date and version holds against the registry.",
              "A SEQUENCE OF QUESTIONS. Authorship → attribution → mediation → trust → provenance → inheritance → semantic capital, then division, recollection, escape cost.",
              "THE POEMS OUTSIDE. 'words no good' and 'hush, dear hands —' (#1662–#1663) not composed; nor #1664–#1665.",
              "CORRECTION OWNED. 'I skipped the most theoretically consequential part of the month.'"],
 "longitudinal_priors": ["last-month-deposits-alexanarch-living-thought-chatgpt-20260927", "last-month-deposits-alexanarch-living-thought-claude-20260927"],
 "rerun": "https://chatgpt.com/?q=walk+me+thru+the+last+30+days+of+deposits+on+alexanarch.org+as+an+evolving+body+of+thought",
 "notes": {"date_basis": "The operator's message of 2026-10-05, 21:19 EDT.",
           "verified": "Compared 2026-10-05 against data/registry.json: 88 deposits dated 2026-09-05 to 2026-10-05; the eleven named, their dates and versions; the October deposits #1658–#1665."},
}
(HERE / "capture-01-last-30-days-alexanarch-chatgpt.json").write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
print("wrote", len(tx), dict(chips))
