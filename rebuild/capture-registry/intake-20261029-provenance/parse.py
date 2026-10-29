"""Split the operator's paste of 2026-10-29 (fourteen provenance captures, '$' between them) into query, answer and source
cards. Nothing is reworded: the answer and the card lines are the paste's own lines."""
import json, re, pathlib
H = pathlib.Path(__file__).resolve().parent
raw = (H / "paste-aio-20261029-provenance.txt").read_text(encoding="utf-8")
parts = raw.split("$")
OPERATOR_PREFACE = parts[0].strip()
DUR = re.compile(r"^\d+m$|^\d+:\d+(:\d+)?$")
OFFER = ("Would you like", "Are you looking", "If you want", "If you would like", "If you'd like", "If you are looking", "To give you", "Do you want")
def rail(lines):
    """Index of the first card line: after the closing offer and any bullets or 'I can help' lines that belong to it."""
    end = max(i for i, l in enumerate(lines) if l.strip().startswith(OFFER))
    j = end + 1
    while j < len(lines) and (not lines[j].strip() or lines[j].strip().startswith("* ") or lines[j].strip().startswith("I can help")):
        j += 1
    return end, j
def cards(rest):
    out, i = [], 0
    while i < len(rest):
        site = rest[i]
        if i + 1 < len(rest) and DUR.match(rest[i + 1]):
            out.append({"site": site, "title": rest[i + 2] if i + 2 < len(rest) else None, "snip": None, "duration": rest[i + 1]}); i += 3; continue
        out.append({"site": site, "title": rest[i + 1] if i + 1 < len(rest) else None, "snip": rest[i + 2] if i + 2 < len(rest) else None}); i += 3
    return out
segs = []
for k, p in enumerate(parts[1:], 1):
    p = p.strip()
    note = None
    if p.startswith("."): p = p[1:].strip()  # the operator's '$.' before the last capture
    if p.startswith("AI Mode Conversation"):
        p = p[len("AI Mode Conversation"):].strip()
        first, body = p.split("\n", 1)
        assert first.startswith("You said: "), first
        qq = first[len("You said: "):].strip(); q = qq[:len(qq) // 2]; assert qq == q + q, qq
        expanded = True
    else:  # the WikiWho capture: the operator's note, then the Overview as shown (query once, source chips inline, no card rail)
        note, rest = p.split("\n", 1)
        q, body = rest.split("\n", 1); q = q.strip()
        expanded = False
    lines = body.split("\n")
    if expanded:
        end, j = rail(lines)
        ans = "\n".join(lines[:j]).strip()
        cl = cards([l.strip() for l in lines[j:] if l.strip()])
    else:
        ans = body.strip(); cl = None
    segs.append({"i": k, "q": q, "expanded": expanded, "operator_note": note.strip() if note else None, "text": body.strip(), "answer": ans, "cards": cl})
json.dump({"operator_preface": OPERATOR_PREFACE, "segments": segs}, open(H / "segments.json", "w"), ensure_ascii=False, indent=1)
for s in segs:
    print(s["i"], repr(s["q"]), len(s["answer"]), "cards:", None if s["cards"] is None else len(s["cards"]), "| note:", s["operator_note"])
    for c in s["cards"] or []: print("     ", c["site"], "|", (c["title"] or "")[:60], "|", (c["snip"] or c.get("duration") or "")[:50])
