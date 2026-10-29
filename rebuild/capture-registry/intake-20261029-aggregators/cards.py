"""Source cards of an expanded Overview paste, proposed from the lines after the answer's closing offer. Kept as pasted."""
import re
DUR = re.compile(r"^\[?(\d+:\d+(:\d+)?|\d+m)(\]\(.*\))?$")
OFFER = ("Would you like", "Are you looking", "Are you trying", "If you'd like", "Do you want")
def split_answer(text):
    lines = text.split("\n")
    end = next(i for i, l in enumerate(lines) if l.strip().startswith(OFFER))
    for j in range(end + 1, min(end + 8, len(lines))):
        if lines[j].strip().startswith("Let me know"): end = j
    ans = "\n".join(lines[:end + 1]).strip()
    rest = [l.strip() for l in lines[end + 1:] if l.strip()]
    rest = [l for l in rest if not l.startswith("AI responses may include mistakes") and not l.startswith("[Show thread]")]
    return ans, rest
def cards(rest):
    out, i = [], 0
    while i < len(rest):
        site = rest[i]
        if i + 1 < len(rest) and DUR.match(rest[i + 1]):
            title = rest[i + 2] if i + 2 < len(rest) else None
            out.append({"site": site, "title": title, "snip": None, "kind": "video", "duration": rest[i + 1]}); i += 3; continue
        title = rest[i + 1] if i + 1 < len(rest) else None
        snip = rest[i + 2] if i + 2 < len(rest) else None
        if snip and (len(snip) < 60 and not snip.endswith("...")) and not re.match(r"^[A-Z][a-z]{2} \d", snip):
            out.append({"site": site, "title": title, "snip": None}); i += 2; continue
        out.append({"site": site, "title": title, "snip": snip}); i += 3
    return out
def inline_links(ans):
    return [m.group(1) for m in re.finditer(r"\[([^\]\d][^\]]*)\]\(https://www\.google\.com/goto", ans)]
