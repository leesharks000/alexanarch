#!/usr/bin/env python3
"""Shared head (copied from intake-20261012-ask-chatgpt-five-1324, from -five, -six, -seven). Author ChatGPT captures at the record pages' Ask ChatGPT prompts, 2026-10-12, from the operator's attachments of
12:32, 13:03, 13:24 and 14:14 EDT ("captures. signed out. incognito. testing the new links. dont need to paste the initial prompt because its the
link to search prompt from the chatgpt button in the corresponding deposit · 12:32: they should have landed, and here are a few more · 13:03: might as well stay in the roll · 13:24: chatgpt has a difficult time finding records on oddly specific subtopics, namely dealing with or especially representing suppression · 14:14: the stones is perhaps one of the more important pieces... easy to miss"). Each issued string is the record page's Ask
ChatGPT prompt for its deposit (wire_deposit.chatgpt_prompt_of), on the operator's statement. Signed out and incognito, both
attested. Operator turns blank in the pastes; later turns are not given. Every quotation and figure the findings rest on is
asserted against the deposit's seated text before anything is written. NEW addresses."""
import json, re, pathlib, sys, unicodedata
HERE = pathlib.Path(__file__).resolve().parent; ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE.parent)); sys.path.insert(0, str(ROOT))
from _chatgpt_common_20261008 import parse, transcript, cite_list
import wire_deposit as w

N = lambda s: unicodedata.normalize("NFC", re.sub(r"\s+", " ", s))
reg = {x["deposit_number"]: x for x in json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8"))["deposits"]}
caps = json.loads((ROOT / "data/EA-WG-CAPTURES-01.json").read_text(encoding="utf-8"))
def text(n): return N((ROOT / reg[n]["full_text_path"].lstrip("/")).read_text(encoding="utf-8"))
def inall(strings, *hay):
    for s in strings:
        for h in hay: assert N(s) in N(h), (s[:60], hay.index(h))
OPR = ("12:08: captures. signed out. incognito. testing the new links. dont need to paste the initial prompt because its the link "
       "to search prompt from the chatgpt button in the corresponding deposit · 12:32: they should have landed, and here are a few more · 13:03: might as well stay in the roll · 13:24: chatgpt has a difficult time finding records on oddly specific subtopics, namely dealing with or especially representing suppression · 14:14: the stones is perhaps one of the more important pieces... easy to miss")
SEAT = "Seated 2026-10-12 from the operator's attachments of 14:14 EDT."
FURNITURE = ["You’ll get smarter responses and can upload files, images, and more.", "Sign up for free",
             "You’re using our basic model. Log in or sign up for more intelligence.", "Worked for 19s"]
REL = {"Alexanarch": "archive_controlled", "mindcontrolpoems.blogspot.com": "authored_surface", "Goodreads": "authored_surface",
       "Plato Online": "third_party", "Stanford Encyclopedia of Philosophy": "third_party"}
CHIPS = set(REL)
NOTE = {"Goodreads": "a Goodreads page; the answer's quotations are the deposit's text, so the page carries it; not resolved",
        "mindcontrolpoems.blogspot.com": "the author's blog; not resolved",
        "Alexanarch": "the archive; which page is not shown"}

def load(name, captions=(), merge=()):
    raw = (HERE / name).read_text(encoding="utf-8")
    body = raw
    for a, b in merge: assert a in body, a; body = body.replace(a, b)
    cut = [f for f in FURNITURE if f in body]
    for f in cut: body = body.replace(f, "")
    for c in captions: assert c in body, c
    turns, seen = parse(body, CHIPS, captions)
    return raw, turns, seen, cut

def head(n, k, extra=""):
    later = (f" Turns 2–{k} blank in the paste and not given." if k > 1 else "")
    return (f"[ChatGPT (chatgpt.com), signed out, incognito, 2026-10-12 (operator: signed out, incognito, 12:08 EDT; sent 14:14). The operator turn blank in the paste; the "
            f"issued string is the record page's Ask ChatGPT prompt for #{n}.{later} Source chips rendered inline as [chip: site +N]; "
            f"image-card captions as [image card: …]; the sign-in furniture cut.{extra}]")

def cl_for(seen):
    cl = cite_list(seen, REL)
    for c in cl: c["note"] += "; " + NOTE.get(c["site"], "not resolved")
    return cl

def base(n, slug, mt, d, turns, seen, raw, cut, per_v, per_note, reading, analysis, findings, related, priors, reached, reached_basis,
         q_kind_extra="", query_basis=None, transcript_extra="", originator=None):
    x = reg[n]; Q = w.chatgpt_prompt_of(x)
    assert not any(e["q"] == Q for e in caps["entries"]), "address already seated: " + Q
    b, ex = w.search_title_urls(x)
    k = len(turns)
    lost = 4 - sum(per_v.values())
    qs = [Q] + ["[blank in the paste]"] * (k - 1)
    tc = ("ONE ANSWER; QUERY FROM THE RECORD PAGE'S LINK; CHIPS INLINE" if k == 1 else
          f"{['','','TWO','THREE','FOUR','FIVE'][k]} ANSWERS; FIRST QUERY FROM THE RECORD PAGE'S LINK; LATER TURNS BLANK; CHIPS INLINE")
    complete = ("One answer, complete as pasted; the operator turn blank, the query taken from the link." if k == 1 else
                f"{k} answers, complete as pasted; the first operator turn blank and taken from the link, turns 2–{k} blank and not given.")
    notes = {"date_basis": "The operator's message of 2026-10-12, 14:14 EDT.", "operator_reading": OPR,
             "query_basis": query_basis or (f"The operator turn is blank in the paste. The string is the record page's Ask ChatGPT prompt for #{n}, "
                                            "on the operator's statement that the initial prompt is the link from the deposit's ChatGPT button."),
             "reached_basis": reached_basis, "verified": f"Compared 2026-10-12 against the seated text of #{n}" + (" and the deposits named in the reading." if related else ".")}
    if cut: notes["furniture_cut"] = "; ".join(cut)
    return {"q": Q, "date": "2026-10-12", "surface": "ChatGPT",
        "surface_basis": "The paste: the chatgpt.com unauthenticated interface ('Log in', 'ChatGPT said:', 'Chat with ChatGPT').",
        "auth": "signed out, incognito", "auth_basis": "'signed out. incognito.' — operator, 2026-10-12 12:08 EDT, for this run of the record-page links; these seven sent at 14:14, after the seven of 12:08, the six of 12:32 and the fives of 13:03 and 13:24. The interface's 'Log in' corroborates signed out.",
        "ev": "paste", "s": "Machine Reception", "slug": slug,
        "q_kind": ("the record page's Ask ChatGPT prompt for #" + str(n) + " (" + ("a work read closely, its title quoted, its author named, grounded in the text"
                   if Q.startswith("Tell me about") else "a paper's arguments, its title quoted, its author named, grounded in the text")
                   + "); the operator turn blank in the paste, the string taken from the link. NEW address." + q_kind_extra),
        "originator": originator or {"name": "Lee Sharks", "relation": "archive", "entity_type": "work", "spxi_treatment": "full",
                       "basis": f"#{n} ({x['axn']}) is {x['creator']}'s. Recorded 2026-10-12."},
        "related_deposits": [n] + list(related), "longitudinal_priors": list(priors),
        "intended": {"deposit": n, "axn": x["axn"], "title": x["title"], "record": f"https://www.alexanarch.org/s/records/{n}/", "search": b, "search_exact": ex, "reached": reached},
        "mt": mt, "d": mt + ": " + d,
        "cites": sum(seen.values()), "cite_list": cl_for(seen), "archive_controlled_cites": seen.get("Alexanarch", 0),
        "sf": "Source chips expose site labels only: " + "; ".join(f"{s} ×{c}" for s, c in seen.most_common()) + ".",
        "per": lost / 4, "per_v": per_v, "per_note": per_note,
        "transcript": transcript(head(n, k, transcript_extra), qs, turns), "transcript_raw": raw,
        "transcript_class": "CAPTURE-TIME VERBATIM RECORD (" + tc + ")", "transcript_complete": complete, "transcript_read": "READ IN FULL 2026-10-12",
        "reading": reading, "analysis": analysis + " " + SEAT, "findings": findings, "rerun": w.chatgpt_url_of(x), "notes": notes}

