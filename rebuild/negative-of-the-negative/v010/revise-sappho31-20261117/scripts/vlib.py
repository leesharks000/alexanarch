"""Shared verification helpers for the Sappho 31 row revision of 2026-11-17 (stage scripts only); after the CRJ stage's vlib.py."""
import json, re, pathlib, unicodedata

ROOT = pathlib.Path(__file__).resolve().parents[5]
REG = ROOT / "data/EA-WG-CAPTURES-01.json"
STAGE = pathlib.Path(__file__).resolve().parents[1]
LIVE_ROW = ROOT / "datasets/negative-of-the-negative/v2/rows/sappho-31.json"
LIVE_LEDGERS = ROOT / "datasets/negative-of-the-negative/v2/ledgers/sappho-31"


def norm(s):
    s = unicodedata.normalize("NFC", s)
    for a, b in ((" ", " "), (" ", " "), (" ", " "), ("​", ""), ("­", ""),
                 ("‘", "'"), ("’", "'"), ("“", '"'), ("”", '"'), ("ʼ", "'"), ("᾽", "'"), ("᾿", "'")):
        s = s.replace(a, b)
    s = re.sub(r"\s+", " ", s)
    return s.strip()


def strip_md(s):
    s = re.sub(r"\*\*?|__", "", s)
    s = re.sub(r"(?<![A-Za-z0-9])_([^_]+)_(?![A-Za-z0-9])", r"\1", s)
    s = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", s)
    s = s.replace("`", "")
    return s


def parts(q):
    return [p for p in re.split(r"\s…\s|\s\.\.\.\s", q) if p.strip()]


def unquote(q):
    q = q.strip()
    if len(q) > 1 and q[0] == '"' and q[-1] == '"':
        q = q[1:-1]
    return q


def found(quote, hay):
    H = norm(hay)
    return all(norm(p) in H for p in parts(quote))


_reg = None


def registry():
    global _reg
    if _reg is None:
        _reg = json.loads(REG.read_text(encoding="utf-8"))
    return _reg


def entry(slug):
    for e in registry()["entries"]:
        if e["slug"] == slug:
            return e
        for o in e.get("observations") or []:
            if o.get("slug") == slug and slug != e["slug"]:
                return o
    raise KeyError(slug)


def entry_text(slug):
    e = entry(slug)
    bits = []
    for k in ("reading", "analysis", "q", "mt", "d", "transcript"):
        v = e.get(k)
        if isinstance(v, str):
            bits.append(v)
    for f in e.get("findings") or []:
        bits.append(f if isinstance(f, str) else json.dumps(f, ensure_ascii=False))
    for c in e.get("cite_list") or []:
        bits.append(" ".join(str(c.get(k) or "") for k in ("site", "title", "snip")))
    return "\n".join(bits)


def deposit_text(path):
    return strip_md((ROOT / path).read_text(encoding="utf-8"))
