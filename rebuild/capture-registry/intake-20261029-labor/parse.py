"""Split the operator's paste of 2026-10-29 (twelve Labor Vector captures inline, '$' between them, and three attached as files)
into query, answer and source cards. Nothing is reworded: the answer and the card lines are the paste's own lines.

The inline paste is saved verbatim from the session transcript (paste-inline-20261029-labor.txt); the harness prefixed it with a
time note and the three attachment paths, which are cut here at the first 'AI Mode Conversation'. The separator is a '$' (once
'$.') followed by 'AI Mode Conversation': the Microsoft answer itself contains '$100 billion'."""
import json, re, pathlib
H = pathlib.Path(__file__).resolve().parent
raw = (H / "paste-inline-20261029-labor.txt").read_text(encoding="utf-8")
raw = raw[raw.index("AI Mode Conversation"):]
parts = [p for p in re.split(r"\s\$\.?\s+(?=AI Mode Conversation)", raw)]
for f in ["paste-attach-dwi.txt", "paste-attach-ilo-index.txt", "paste-attach-negotiating-tech.txt"]:
    parts.append((H / f).read_text(encoding="utf-8").strip())
DUR = re.compile(r"^\d+m$|^\d+:\d+(:\d+)?$")
OFFER = ("Would you like", "Are you looking", "If you want", "If you would like", "If you'd like", "If you are looking", "To give you", "Do you want")


def rail(lines):
    offers = [i for i, l in enumerate(lines) if l.strip().startswith(OFFER)]
    # no closing offer (Turkopticon): the answer ends at its last line carrying an inline citation
    end = max(offers) if offers else max(i for i, l in enumerate(lines) if "](https://www.google.com/goto" in l)
    j = end + 1
    while j < len(lines) and (not lines[j].strip() or lines[j].strip().startswith("* ") or lines[j].strip().startswith("• ") or lines[j].strip().startswith("I can help")):
        j += 1
    return end, j


def cards(rest):
    out, i = [], 0
    while i < len(rest):
        site = rest[i]
        if i + 1 < len(rest) and DUR.match(rest[i + 1]):
            out.append({"site": site, "title": rest[i + 2] if i + 2 < len(rest) else None, "snip": None, "duration": rest[i + 1]}); i += 3; continue
        if i + 1 < len(rest) and re.match(r"^\[\d+(:\d+)*m?\]\(", rest[i + 1]):  # a video duration given as a link
            out.append({"site": site, "title": rest[i + 2] if i + 2 < len(rest) else None, "snip": None, "duration": rest[i + 1]}); i += 3; continue
        out.append({"site": site, "title": rest[i + 1] if i + 1 < len(rest) else None, "snip": rest[i + 2] if i + 2 < len(rest) else None}); i += 3
    return out


segs = []
for k, p in enumerate(parts, 1):
    p = p.strip()
    assert p.startswith("AI Mode Conversation"), p[:60]
    p = p[len("AI Mode Conversation"):].strip()
    first, body = p.split("\n", 1)
    assert first.startswith("You said: "), first
    qq = first[len("You said: "):].strip(); q = qq[:len(qq) // 2]; assert qq == q + q, qq
    lines = body.split("\n")
    end, j = rail(lines)
    ans = "\n".join(lines[:j]).strip()
    tail = [l.strip() for l in lines[j:] if l.strip() and not l.strip().startswith("AI responses may include mistakes")]
    disclaimer = any(l.strip().startswith("AI responses may include mistakes") for l in lines[j:])
    segs.append({"i": k, "q": q, "source": "inline" if k <= 12 else "attachment", "text": body.strip(), "answer": ans, "cards": cards(tail), "disclaimer": disclaimer})
json.dump({"segments": segs}, open(H / "segments.json", "w"), ensure_ascii=False, indent=1)
for s in segs:
    print(s["i"], repr(s["q"]), len(s["answer"]), "cards:", len(s["cards"]), s["source"])
    for c in s["cards"]: print("     ", c["site"][:40], "|", (c["title"] or "")[:60], "|", (c["snip"] or c.get("duration") or "")[:40])
