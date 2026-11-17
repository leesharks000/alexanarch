"""Verification helpers for the /non row longinus-on-the-sublime (2026-11-17); after the Sappho 31 and CRJ stages' vlib.py."""
import json, re, pathlib, unicodedata

ROOT = pathlib.Path(__file__).resolve().parents[6]
REG = ROOT / "data/EA-WG-CAPTURES-01.json"
INTAKE = pathlib.Path(__file__).resolve().parents[1]


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
    return [p for p in re.split(r"\s…\s|\s\.\.\.\s(?=\S)", q) if p.strip()]


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
    raise KeyError(slug)


def entry_text(slug):
    e = entry(slug)
    bits = []
    for k in ("reading", "analysis", "q", "q_kind", "mt", "d", "surface_basis"):
        v = e.get(k)
        if isinstance(v, str):
            bits.append(v)
    for f in e.get("findings") or []:
        bits.append(f if isinstance(f, str) else json.dumps(f, ensure_ascii=False))
    for k in ("originator", "per_dim"):
        v = e.get(k)
        if isinstance(v, dict):
            bits.append(v.get("basis") or "")
    return "\n".join(bits)


def deposit_text(path):
    return strip_md((ROOT / path).read_text(encoding="utf-8"))
