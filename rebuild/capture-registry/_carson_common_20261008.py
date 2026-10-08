"""Shared card parser for the 2026-10-08 13:52 intake (three Google AI Overview popups, expanded)."""
import re
def cards(raw, spec):
    """spec: list of (site_line, title_prefix, site_label, rel). Returns cite_list with the snippet line that follows."""
    L = raw.split("\n"); out = []
    for n, (site_line, tpre, label, rel) in enumerate(spec, 1):
        def nxt(i):  # skip a video duration line ('0:48') between the site and the title
            return i + 2 if i + 2 < len(L) and re.fullmatch(r"\d+:\d\d", L[i + 1].strip()) else i + 1
        idx = [i for i, l in enumerate(L) if l.strip() == site_line and nxt(i) < len(L) and L[nxt(i)].strip().startswith(tpre)]
        assert idx, (site_line, tpre)
        i = idx[0]; t = nxt(i); title = L[t].strip(); snip = L[t + 1].strip() if t + 1 < len(L) else None
        out.append({"n": n, "site": label, "title": title, "snip": snip, "rel": rel, "url": None, "note": "card"})
        L[i] = "\0"  # consume, so a repeated site line resolves to the next card
    return out
