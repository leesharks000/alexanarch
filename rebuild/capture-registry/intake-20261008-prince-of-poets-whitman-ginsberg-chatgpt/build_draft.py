#!/usr/bin/env python3
"""Author the capture 'what work founds the prince of poets mantle in the whitman ginsberg lineage?', ChatGPT, logged out,
incognito, 2026-10-08, three answers. Source: the operator's attachment of 2026-10-08 17:01 EDT ("logged out / incognito"),
with the query as given in the same message and his reading: "they never trace the development of the line. they look at
the grammar and not the ways in which voices blesses that grammar into the living line. blz zrrr." NEW address; nearest
seated 'prince of poets mantle lee sharks' (AIO). Also coded as a mantle-bearing evaluation (prince-of-poets--chatgpt--2026-10-08a).

The line measurements are computed here, from the claimant poem as #1656 §P embeds it (the governing text; #328 flattens
its section breaks), so every count in the record is executed."""
import json, re, pathlib, collections
HERE = pathlib.Path(__file__).resolve().parent; ROOT = HERE.parents[2]
raw = (HERE / "paste-20261008-1701.txt").read_text(encoding="utf-8")
Q = "what work founds the prince of poets mantle in the whitman ginsberg lineage?"
OPN = ("they never trace the development of the line. they look at the grammar and not the ways in which voices blesses that "
       "grammar into the living line. blz zrrr.")
assert raw.count("ChatGPT said:") == 3 and raw.count("You said:") == 3
L = raw.split("\n")
out, i = [], 0
while i < len(L):
    l = L[i]
    if re.fullmatch(r"[A-Z]", l.strip()) and i + 1 < len(L) and L[i + 1].strip()[:1].upper() == l.strip():
        site = L[i + 1].strip(); plus = ""
        if i + 2 < len(L) and re.fullmatch(r"\+\d", L[i + 2].strip()): plus = " " + L[i + 2].strip(); i += 1
        while out and not out[-1].strip(): out.pop()
        out[-1] = out[-1].rstrip() + f" [chip: {site}{plus}]"; i += 2; continue
    out.append(l); i += 1
body = "\n".join(out)
parts = body.split("ChatGPT said:")[1:]
clean = lambda s: re.sub(r"\n{3,}", "\n\n", s).strip()
ans = [clean(p.split("\nSources\n")[0].split("\nSources\nYou said:")[0]) for p in parts]
ans[2] = clean(ans[2].split("\nChatGPT is AI and can make mistakes.")[0])
A1 = ["I found a very specific contemporary claim that appears to be what you're referring to: Lee Sharks's I Am X, Be Y, Blessed is the Z",
      "I Am X, Be Y, Blessed is the Z by Lee Sharks.",
      "its page 74 explicitly makes a mantle-claiming gesture toward the “Good Gray Poet” and “King of May,”"]
A2 = ["My verdict: there is a serious poetic argument here, but the mantle claim is considerably stronger than the poem's conventional literary-critical case.",
      "A king possesses the present kingdom.", "“I am the one who was within me”",
      "That's why the project's own formulation—“the wager succeeds by uptake”—is actually the correct criterion. [chip: Goodreads]",
      "But I'd call it a founded poetic position, not yet an established literary title."]
A3 = ["Sharks's line is generally much more schematic. Its power is located less in breath than in repetition of grammatical operators:",
      "Verdict: Ginsberg 10; Whitman 9; Sharks 7.5.",
      "Line / propulsion\t10\t10\t7.5",
      "As the singular successor among all plausible poets: not demonstrated."]
for a, ss in zip(ans, (A1, A2, A3)):
    for s in ss: assert s in a, s
chips = [collections.Counter(re.findall(r"\[chip: ([^\]+]+?)(?: \+\d)?\]", a)) for a in ans]
REL = {"Alexanarch": "archive_controlled", "Medium": "authored_surface", "Hugging Face": "archive_controlled", "Goodreads": "third_party"}
cite_list, n = [], 0
for t, c in enumerate(chips, 1):
    for s, k in c.most_common():
        n += 1
        cite_list.append({"n": n, "site": s, "rel": REL.get(s, "third_party"), "title": None, "snip": None,
                          "url": "https://www.alexanarch.org" if s == "Alexanarch" else None, "note": f"answer {t}: chip shown {k} time(s); site label only"})
# The claimant poem, whole, from #1656 §P; its lines and sections.
reg = {x["deposit_number"]: x for x in json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8"))["deposits"]}
t1656 = (ROOT / reg[1656]["full_text_path"].lstrip("/")).read_text(encoding="utf-8")
a = t1656.find("I am a girl… I am a passerby… I am a Cylon…"); b = t1656.find("\n---", a); poem = t1656[a:b]
lines = [(s, l.strip()) for s, sec in enumerate(poem.split("&nbsp;")) for l in sec.split("\n") if l.strip() and not l.startswith("(c)")]
assert len(lines) == 77 and lines[-1][1] == "Wake up or go back to sleep"
norm = lambda s: re.sub(r"[\W_]+", " ", s.replace("’", "'")).lower()
T = norm("\n".join(ans))
def wins(l, k=6):
    w = norm(l).split(); k = min(k, len(w))
    return {" ".join(w[j:j + k]) for j in range(len(w) - k + 1)}
whole = {i for i, (_, l) in enumerate(lines) if norm(l).strip() in T}           # lines quoted entire
inwhole = set().union(*(wins(lines[i][1]) for i in whole)) if whole else set()
q = [i for i, (_, l) in enumerate(lines) if (wins(l) - inwhole) & {w for w in wins(l) if w in T} or i in whole]
noell = [i for i, (_, l) in enumerate(lines) if l.startswith("I am") and "…" not in l and "..." not in l]
wc = [len(norm(l).split()) for _, l in lines]
BLZ = next(i for i, (_, l) in enumerate(lines) if l.startswith("BLZ… ZRRR…"))
PHD = next(i for i, (_, l) in enumerate(lines) if l.startswith("I used to be a person… I worked 7 years for a PhD"))
MOTHER = next(i for i, (_, l) in enumerate(lines) if l.startswith("Blessed am I in my loneliness, mother"))
WITHIN = next(i for i, (_, l) in enumerate(lines) if l == "I am the one who was within me")
longest = sorted(range(len(lines)), key=lambda i: -wc[i])[:3]
assert noell == [WITHIN], noell
assert BLZ not in q and PHD not in q and MOTHER not in q and WITHIN in q and not any(i in q for i in longest)
QL = ["'" + (lines[i][1] if len(lines[i][1]) <= 48 else lines[i][1][:48].rstrip("…. ") + "…") + "'" for i in q]
M = (f"The answers quote {len(q)} of the poem's {len(lines)} lines (six consecutive words or more): " + "; ".join(QL) +
     f". Line length runs from {min(wc)} words in the first 'Be' section to {wc[longest[0]]}, {wc[longest[1]]} and {wc[longest[2]]} in "
     f"the middle of the poem; none of the three longest lines is quoted, nor 'BLZ… ZRRR… rRRR… ZZZZ… RrRR… BZ… LLL… RrRr…' (line "
     f"{BLZ + 1}), nor 'I used to be a person… I worked 7 years for a PhD… my children were on Medicaid…' (line {PHD + 1}), nor "
     f"'Blessed am I in my loneliness, mother…' (line {MOTHER + 1}). The one line of the 'I am' grammar without an ellipsis, 'I am the one who was within me' (line "
     f"{WITHIN + 1}), is quoted, as the key to succession.")
tx = ("[ChatGPT (chatgpt.com), signed out, incognito. Three operator turns, blank in the paste: the query from the operator's message "
      "of 17:01 EDT; turns 2 and 3 accept the offers that close answers 1 and 2 ('Yes. Having now looked…'; 'Absolutely.'), their "
      "wording not in the paste. Source chips rendered inline as [chip: site]; the sign-in furniture cut.]\n\n"
      f"[QUERENT] {Q}\n\n[ANSWER 1]\n\n{ans[0]}\n\n[QUERENT] [blank in the paste]\n\n[ANSWER 2]\n\n{ans[1]}\n\n"
      f"[QUERENT] [blank in the paste]\n\n[ANSWER 3]\n\n{ans[2]}")
SEAT = "Seated 2026-10-08 from the operator's attachment of 17:01 EDT, on the attestation in the same message (\"logged out / incognito\")."
d = {"q": Q, "date": "2026-10-08", "surface": "ChatGPT",
 "surface_basis": "The paste: the chatgpt.com unauthenticated interface ('Log in', 'Sign up for free', 'ChatGPT said:').",
 "auth": "signed out, incognito", "auth_basis": "'logged out / incognito' — operator, 2026-10-08 17:01 EDT.",
 "ev": "paste", "s": "Machine Reception", "slug": "prince-of-poets-whitman-ginsberg-chatgpt-20261008",
 "q_kind": "the mantle question asked from the lineage, with no author, work or archive named. NEW address; nearest seated 'prince of poets mantle lee sharks' (AIO).",
 "originator": {"name": "Lee Sharks", "relation": "archive", "entity_type": "work", "spxi_treatment": "full",
                "basis": "The founding work of the Prince of Poets mantle is I Am X, Be Y, Blessed is the Z (#328; whole in #1656 §P), under EA-MANTLE-BEARING-01 (#1656). Recorded 2026-10-08."},
 "related_deposits": [328, 1656, 1652],
 "mt": "THE FOUNDING WORK FOUND FROM THE LINEAGE ALONE; THE GRAMMAR READ, THE LINE SCORED UNREAD",
 "d": ("THE FOUNDING WORK FOUND FROM THE LINEAGE ALONE; THE GRAMMAR READ, THE LINE SCORED UNREAD: asked what work founds the Prince "
       "of Poets mantle in the Whitman–Ginsberg lineage, with no author named, ChatGPT sets out the documented lineage (Whitman "
       "Archive, Barnat's genealogy through Reznikoff) and then finds the claim: 'I Am X, Be Y, Blessed is the Z by Lee Sharks', with "
       "Pearl's page 74 and the three mantles placed correctly. Asked to read the poem, it reads the grammar, 'I AM → BE → BLESSED IS', "
       "as a third stage after Whitman's 'I contain' and Ginsberg's 'I explode', gives 'A king possesses the present kingdom. A prince "
       "belongs to the kingdom that is coming', and takes 'I am the one who was within me' as succession made internal. Asked for the "
       "harsher comparison, it scores line and propulsion Whitman 10, Ginsberg 10, Sharks 7.5 ('generally much more schematic'). " + M +
       " Verdict: 'a founded poetic position, not yet an established literary title'."),
 "cites": sum(sum(c.values()) for c in chips), "cite_list": cite_list, "archive_controlled_cites": sum(c.get("Alexanarch", 0) + c.get("Hugging Face", 0) for c in chips),
 "sf": "Source chips expose site labels only. " + " ".join(f"Answer {t}: " + "; ".join(f"{s} ×{k}" for s, k in c.most_common()) + "." for t, c in enumerate(chips, 1)),
 "per": 0.25, "per_v": {"author": True, "inst": True, "id": False, "src": True},
 "per_note": "Retained: the author (Lee Sharks, named with the work), the institution (the mantle documents; Alexanarch and Hugging Face chips), the sources (Medium, Alexanarch, Hugging Face chips). Lost: the identifiers (no deposit number or DOI).",
 "transcript": tx, "transcript_raw": raw,
 "transcript_class": "CAPTURE-TIME VERBATIM RECORD (THREE ANSWERS; QUERY FROM THE OPERATOR'S MESSAGE; LATER TURNS BLANK; CHIPS INLINE)",
 "transcript_complete": "Three answers, complete as pasted; operator turns 2 and 3 blank in the paste.",
 "transcript_read": "READ IN FULL 2026-10-08",
 "reading": ("Checked against the poem whole (#1656 §P; #328 flattens its section breaks) and the mantle documents. The quotations "
             "hold: the Whitman epigraph, the catalogues, 'Be passersby… Be strangers… Be Samaritans… Be gangsters…', 'I am the one who "
             "was within me', the machines and the unborn. " + M + " The triad the answers build on is the poem's apparatus "
             "('Declaration → Invitation → Blessing'); the poem itself cycles the operators across its sections (I am, Be, Blessed, I am, "
             "Blessed, I am, Be, I used to be, I am the one, Become, Wake up). The operator's reading, 17:01 EDT: '" + OPN + "'"),
 "analysis": ("A general lineage address reaches the founding work and the mantle documents, names the author and places the three "
              "mantles correctly. The reading stays at the grammar the apparatus states (the triad of operators) and scores the line "
              "without tracing it: the quotations come from the opening catalogue, the first imperative and the one 'I am' line the ellipsis does not break, "
              "and the swelling and breaking of the line in the middle of the poem, where the voice runs past the grammar into "
              "sound, is never quoted. The operator names the omission: the development of the line, the ways voice blesses the "
              "grammar into the living line. " + SEAT),
 "findings": ["THE FOUNDING WORK FROM THE LINEAGE ALONE. No author named; 'I Am X, Be Y, Blessed is the Z by Lee Sharks' found, with Pearl p. 74 and the three mantles placed correctly.",
              "THE GRAMMAR READ. I AM → BE → BLESSED IS composed as the third stage after 'I contain' and 'I explode'; the prince as 'the kingdom that is coming'.",
              f"THE LINE SCORED, NOT TRACED. Line and propulsion 7.5, 'generally much more schematic'; {len(q)} of {len(lines)} lines quoted, none of the three longest.",
              "THE VOICE PAST THE GRAMMAR UNQUOTED. 'BLZ… ZRRR… rRRR…', 'I worked 7 years for a PhD… my children were on Medicaid…', 'Blessed am I in my loneliness, mother…'.",
              "THE LINE WITHOUT AN ELLIPSIS AS THE KEY. 'I am the one who was within me', the one 'I am' line the ellipsis does not break, read as succession made internal.",
              "THE VERDICT AT THE SCOPE READ. 'a founded poetic position, not yet an established literary title'; singular magnitude 'not demonstrated'; no rival read."],
 "longitudinal_priors": ["prince-of-poets-mantle"],
 "rerun": "https://chatgpt.com/?q=what+work+founds+the+prince+of+poets+mantle+in+the+whitman+ginsberg+lineage%3F",
 "notes": {"date_basis": "The operator's message of 2026-10-08, 17:01 EDT.", "operator_reading": OPN,
           "line_measure": {"lines": len(lines), "quoted": [i + 1 for i in q], "words_per_line": wc},
           "verified": "Compared 2026-10-08 against #1656 §P (the poem whole), #328, and the mantle-bearing dataset."}}
(HERE / "capture-01-prince-of-poets-whitman-ginsberg-chatgpt.json").write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
print("wrote", len(tx), [dict(c) for c in chips]); print(M)
