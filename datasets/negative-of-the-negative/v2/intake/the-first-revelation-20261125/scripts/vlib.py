"""Verification helpers for the /non row the-first-revelation (2026-11-25); after the longinus-on-the-sublime row's vlib.py,
with the /non register's entries, the seated originals (OpenITI '~~' wraps joined) and the 404 fetch bodies added."""
import json, re, pathlib, unicodedata

ROOT = pathlib.Path(__file__).resolve().parents[6]
REG = ROOT / "data/EA-WG-CAPTURES-01.json"
NONREG = ROOT / "datasets/negative-of-the-negative/v2/register.json"
INTAKE = pathlib.Path(__file__).resolve().parents[1]


def norm(s):
    s = unicodedata.normalize("NFC", s)
    for a, b in ((" ", " "), (" ", " "), (" ", " "), ("​", ""), ("­", ""),
                 ("‘", "'"), ("’", "'"), ("“", '"'), ("”", '"'), ("ʼ", "'")):
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
    return [p for p in re.split(r"\s…\s", q) if p.strip()]


def found(quote, hay):
    H = norm(hay)
    return all(norm(p) in H for p in parts(quote))


def seat_text(path):
    """A seated original as text: OpenITI's '~~' line-wrap marks joined into the running line."""
    t = (ROOT / path).read_text(encoding="utf-8")
    return re.sub(r"\n~~", " ", t)


_reg = None
_nonreg = None


def registry():
    global _reg
    if _reg is None:
        _reg = json.loads(REG.read_text(encoding="utf-8"))
    return _reg


def nonregister():
    global _nonreg
    if _nonreg is None:
        _nonreg = json.loads(NONREG.read_text(encoding="utf-8"))
    return _nonreg


def entry(slug):
    for e in registry()["entries"]:
        if e["slug"] == slug:
            return e
    raise KeyError(slug)


def nonreg_entry(slug):
    for e in nonregister()["entries"]:
        if e["slug"] == slug:
            return e
    raise KeyError(slug)


def _flat(e, keys):
    bits = []
    for k in keys:
        v = e.get(k)
        if isinstance(v, str):
            bits.append(v)
        elif isinstance(v, list):
            bits += [x if isinstance(x, str) else json.dumps(x, ensure_ascii=False) for x in v]
        elif isinstance(v, dict):
            bits += [x for x in v.values() if isinstance(x, str)]
            if isinstance(v.get("basis"), str):
                bits.append(v["basis"])
    return "\n".join(bits)


def entry_text(slug):
    return _flat(entry(slug), ("reading", "analysis", "q", "q_kind", "mt", "d", "surface_basis", "findings", "per_note",
                               "per_dim", "originator", "notes"))


def nonreg_text(slug):
    return _flat(nonreg_entry(slug), ("archive_basis", "notes", "transcript_complete", "surface_basis", "auth_basis", "sf"))


def deposit_text(path):
    return strip_md((ROOT / path).read_text(encoding="utf-8"))
