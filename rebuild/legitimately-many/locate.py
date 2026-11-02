#!/usr/bin/env python3
"""Locate a phrase in a seated TEI file and return its citation: the enclosing textpart path (book.chapter.section), the
last Stephanus-type milestone, and the printed page and line (<pb n> and the count of physical lines since it, which in the
First1KGreek CAG files follow the printed lines; the start-of-line <lb n> markers check it). Matching is done on NFD with
whitespace collapsed, so composed and decomposed Greek both match. Notes, the header and readings (<rdg>) are skipped.
    from locate import locate_tei, locate_text"""
import re, unicodedata, pathlib

TOK = re.compile(r"<[^>]+>|[^<]+", re.S)
SKIP = {"note", "teiHeader", "rdg", "bibl", "head"}


def _nfd(s):
    return unicodedata.normalize("NFD", s)


def _stream(xml):
    out, meta = [], []
    stack, skip = [], 0
    page, line, mile = None, 0, None
    bol = True   # at the beginning of a physical line (only whitespace since the last newline)
    for tok in TOK.findall(xml):
        if tok.startswith("<"):
            if tok.startswith("<!--") or tok.startswith("<?"):
                continue
            m = re.match(r"<(/?)([A-Za-z:]+)", tok)
            if not m:
                continue
            close, name = m.group(1) == "/", m.group(2).split(":")[-1]
            selfc = tok.endswith("/>")
            if name in SKIP:
                if close:
                    skip = max(0, skip - 1)
                elif not selfc:
                    skip += 1
                continue
            if name == "div":
                if close:
                    if stack:
                        stack.pop()
                elif not selfc:
                    n = re.search(r'\bn="([^"]*)"', tok)
                    tp = 'type="textpart"' in tok
                    stack.append(n.group(1) if (n and tp) else None)
            elif name == "lb" and not close and bol:
                n = re.search(r'\bn="(\d+)"', tok)
                if n:
                    line = int(n.group(1))   # a start-of-line <lb n> anchors the count to the printed line
            elif name == "pb" and not close:
                n = re.search(r'\bn="([^"]*)"', tok)
                page, line = (n.group(1) if n else page), 0
            elif name == "milestone" and not close:
                n = re.search(r'\bn="([^"]*)"', tok)
                if n and re.search(r'unit="(section|page)"', tok):
                    mile = n.group(1)
            continue
        if skip:
            continue
        for ch in tok:
            if ch == "\n":
                line += 1
                bol = True
            elif not ch.isspace():
                bol = False
            c = " " if ch.isspace() else ch
            if c == " " and out and out[-1] == " ":
                continue
            path = ".".join(x for x in stack if x)
            for d in _nfd(c):
                out.append(d)
                meta.append((path, page, line, mile))
    return "".join(out), meta


_cache = {}


def locate_tei(path, phrase):
    if path not in _cache:
        _cache[path] = _stream(pathlib.Path(path).read_text(encoding="utf-8"))
    s, meta = _cache[path]
    p = " ".join(_nfd(phrase).split())
    i = s.find(p)
    if i < 0:
        return None
    a, b = meta[i], meta[i + len(p) - 1]
    lines = f"{a[1]}.{a[2]}" + (f"–{b[2]}" if b[2] != a[2] and b[1] == a[1] else (f"–{b[1]}.{b[2]}" if b[1] != a[1] else ""))
    return {"textpart": a[0], "milestone": a[3], "page_line": lines if a[1] else None}


def locate_text(path, phrase, markers=(r"^=== (.+) ===$", r"(PageV\d+P\d+)")):
    """For seats without TEI: the line in the text layer and the last page marker before it."""
    raw = pathlib.Path(path).read_text(encoding="utf-8")
    flat, idx = [], []
    for ln, l in enumerate(raw.split("\n"), 1):
        for ch in l + " ":
            c = " " if ch.isspace() else ch
            if c == " " and flat and flat[-1] == " ":
                continue
            for d in _nfd(c):
                flat.append(d); idx.append(ln)
    s = "".join(flat)
    p = " ".join(_nfd(phrase).split())
    i = s.find(p)
    if i < 0:
        return None
    ln = idx[i]
    mark = None
    lines = raw.split("\n")[:ln]
    for l in reversed(lines):
        for m in markers:
            r = re.search(m, l)
            if r:
                mark = r.group(1)
                break
        if mark:
            break
    return {"text_line": ln, "marker": mark}


def line_agreement(path):
    """Share of start-of-line <lb n> markers that fall on the physical line the count gives (the check on page.line)."""
    import re as _re
    x = _re.sub(r"<teiHeader.*?</teiHeader>", "", pathlib.Path(path).read_text(encoding="utf-8"), flags=_re.S)
    ok = bad = 0; page = None; ln = 0; innote = 0
    for L in x.split("\n"):
        m = _re.search(r'<pb n="([^"]+)"', L)
        if m:
            page, ln = m.group(1), 0
            continue
        if innote == 0:
            ln += 1
        mm = _re.match(r'<lb n="(\d+)"/>', L.lstrip())
        if mm and page and innote == 0:
            if int(mm.group(1)) == ln:
                ok += 1
            else:
                bad += 1
        innote = max(0, innote + L.count("<note") - L.count("</note>"))
    return ok / (ok + bad) if ok + bad else 0.0

