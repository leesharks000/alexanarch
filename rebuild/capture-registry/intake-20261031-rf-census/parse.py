"""Split the operator's paste of 2026-10-31 00:04 EDT (eight Revelation First census captures inline, '$' between them, and two attached
as files) into query, answer and source cards. Nothing is reworded: the answer and the card lines are the paste's own lines.

The inline paste is saved verbatim from the session transcript (paste-inline-raw.txt); the harness prefixed it with the three attachment
paths, which are cut here at the first 'AI Mode Conversation'. The separator is a '$' standing alone (' $ ' or a closing ' $'): the
Early Christian Writings answer itself carries '$17.00' and '$10.99'. That capture alone has no 'AI Mode Conversation' header and no
'You said' line; its query is its first line. Two of the three attachments are byte-identical (sha1 cc738be5…, the Vesuvius Challenge),
so one is kept."""
import json, re, pathlib
H = pathlib.Path(__file__).resolve().parent
raw = (H / "paste-inline-raw.txt").read_text(encoding="utf-8")
raw = raw[raw.index("AI Mode Conversation"):]
parts = [p for p in re.split(r" \$(?= |\n|$)", raw) if p.strip()]
src = ["inline"] * len(parts)
for f in ["paste-attach-vesuvius.txt", "paste-attach-ai-and-faith.txt"]:
    parts.append((H / f).read_text(encoding="utf-8").strip()); src.append("attachment")
DUR = re.compile(r"^\d+m$|^\d+:\d+(:\d+)?$")
OFFER = ("Would you like", "Which of these", "If you'd like", "If you want", "Do you want")


def rail(lines):
    offers = [i for i, l in enumerate(lines) if l.strip().startswith(OFFER)]
    end = max(offers)
    j = end + 1
    while j < len(lines) and (not lines[j].strip() or lines[j].strip().startswith("* ") or lines[j].strip().startswith("• ")):
        j += 1
    return end, j


def cards(rest):
    out, i = [], 0
    while i < len(rest):
        site = rest[i]
        if i + 1 < len(rest) and (DUR.match(rest[i + 1]) or re.match(r"^\[\d+(:\d+)*m?\]\(", rest[i + 1])):
            out.append({"site": site, "title": rest[i + 2] if i + 2 < len(rest) else None, "snip": None, "duration": rest[i + 1]}); i += 3; continue
        out.append({"site": site, "title": rest[i + 1] if i + 1 < len(rest) else None, "snip": rest[i + 2] if i + 2 < len(rest) else None}); i += 3
    return out


segs = []
for k, (p, s) in enumerate(zip(parts, src), 1):
    p = p.strip()
    if p.startswith("AI Mode Conversation"):
        p = p[len("AI Mode Conversation"):].strip()
        first, body = p.split("\n", 1)
        assert first.startswith("You said: "), first
        qq = first[len("You said: "):].strip(); q = qq[:len(qq) // 2]; assert qq == q + q, qq
        header = True
    else:
        q, body = p.split("\n", 1); q = q.strip(); header = False
    lines = body.split("\n")
    end, j = rail(lines)
    ans = "\n".join(lines[:j]).strip()
    tail = [l.strip() for l in lines[j:] if l.strip() and not l.strip().startswith("AI responses may include mistakes")]
    disclaimer = any(l.strip().startswith("AI responses may include mistakes") for l in lines[j:])
    segs.append({"i": k, "q": q, "source": s, "header": header, "text": body.strip(), "answer": ans, "cards": cards(tail), "disclaimer": disclaimer})
json.dump({"segments": segs}, open(H / "segments.json", "w"), ensure_ascii=False, indent=1)
for s in segs:
    print(s["i"], repr(s["q"]), len(s["answer"]), "cards:", len(s["cards"]), s["source"], "header" if s["header"] else "NO HEADER")
    for c in s["cards"]:
        print("     ", c["site"][:40], "|", (c["title"] or "")[:60], "|", (c["snip"] or c.get("duration") or "")[:40])
