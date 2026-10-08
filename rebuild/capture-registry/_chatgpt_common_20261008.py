"""Shared parser for the 2026-10-08 19:26 intake (three ChatGPT sessions, signed out, incognito).

The pastes carry: source chips as standalone lines (site label, optionally followed by a '+N' line); image-strip captions
between paragraphs; an ad block; the sign-in furniture. Chips are rendered inline as [chip: site +N] at the sentence they
followed, captions as [image card: caption], the ad cut and returned for the notes. Operator turns are blank in the paste."""
import re, collections

JUNK = {"Log in", "ChatGPT is AI and can make mistakes.", "No file chosenNo file chosenNo file chosen", "Chat with ChatGPT", "Ask ChatGPT", "Sources"}

def parse(raw, chips, captions=(), ad=None):
    if ad:
        assert ad in raw, "ad block"
        raw = raw.replace(ad, "")
    L = raw.split("\n")
    out, i, seen = [], 0, collections.Counter()
    while i < len(L):
        l = L[i].strip()
        if l in chips:
            plus = ""
            if i + 1 < len(L) and re.fullmatch(r"\+\d", L[i + 1].strip()):
                plus = " " + L[i + 1].strip(); i += 1
            while out and not out[-1].strip(): out.pop()
            out[-1] = out[-1].rstrip() + f" [chip: {l}{plus}]"; seen[l] += 1; i += 1; continue
        if l in captions:
            out.append(f"[image card: {l}]"); i += 1; continue
        if l in JUNK:
            i += 1; continue
        out.append(L[i]); i += 1
    body = "\n".join(out)
    turns = body.split("ChatGPT said:")[1:]
    turns = [re.sub(r"\n{3,}", "\n\n", t.split("\nYou said:")[0]).strip() for t in turns]
    return turns, seen

def transcript(head, queries, answers):
    parts = [head, ""]
    for n, (q, a) in enumerate(zip(queries, answers), 1):
        parts += [f"[QUERENT] {q}", "", f"[ANSWER {n}]", "", a, ""]
    return "\n".join(parts).strip()

def cite_list(seen, rel):
    return [{"n": n, "site": s, "rel": rel.get(s, "third_party"), "title": None, "snip": None,
             "url": "https://www.alexanarch.org" if s == "Alexanarch" else None, "note": f"chip shown {k} time(s); site label only"}
            for n, (s, k) in enumerate(seen.most_common(), 1)]
