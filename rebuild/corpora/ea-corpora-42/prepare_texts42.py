#!/usr/bin/env python3
"""EA-CORPORA-42, step 1 (the TEI reduction of EA-CORPORA-41, unchanged): reduce each staged original to its text layer, by code.

    python3 -I prepare_texts42.py <stage-dir>

Writes <stage-dir>/_text/<slug>.txt. Nothing is corrected by hand.
- TEI (First1KGreek, Perseus): teiHeader, note, app, bibl and the like dropped; one line per <p> or <l>;
  each <div> that carries an n or a type gets a marker line [<subtype> <n>] so a locus can be found by its number;
  the edition's page breaks stand as [p. N] and its numbered lines as |L, so a commentary is cited by
  page and line of its edition (CAG: Wallies) straight from the text layer.
- The Latin Library HTML: tags dropped, entities decoded, one line per paragraph.
- Project Gutenberg plain text: the Gutenberg header and licence cut at the START/END markers.
- Internet Archive _djvu.txt and the OCR runs: copied as served, line endings normalized.
"""
import html, pathlib, re, sys, unicodedata
import xml.etree.ElementTree as ET

ST = pathlib.Path(sys.argv[1])
OUT = ST / "_text"
OUT.mkdir(exist_ok=True)
TEI = "{http://www.tei-c.org/ns/1.0}"
DROP = {"teiHeader", "note", "app", "bibl", "rdg", "foreign_note", "figure", "ref", "speaker"}
LINE = {"p", "l", "head", "ab"}


def local(t):
    return t.split("}", 1)[-1] if isinstance(t, str) else ""


def tei(path):
    root = ET.parse(path).getroot()
    out = []

    def text_of(e):
        parts = []

        def walk(x):
            if local(x.tag) in DROP:
                if x.tail:
                    parts.append(x.tail)
                return
            if local(x.tag) == "milestone" and x.get("n"):
                parts.append(f" [{x.get('unit') or 'm'} {x.get('n')}] ")
            elif local(x.tag) == "pb" and x.get("n"):
                parts.append(f" [p. {x.get('n')}] ")
            elif local(x.tag) == "lb" and x.get("n"):
                parts.append(f" |{x.get('n')} ")
            if x.text:
                parts.append(x.text)
            for c in x:
                walk(c)
            if x.tail and x is not e:
                parts.append(x.tail)

        walk(e)
        return re.sub(r"\s+", " ", "".join(parts)).strip()

    def walk_blocks(e):
        tag = local(e.tag)
        if tag in DROP:
            return
        if tag == "pb" and e.get("n"):
            out.append(f"[p. {e.get('n')}]")
            return
        if tag == "div" and (e.get("n") or e.get("subtype")):
            out.append(f"[{e.get('subtype') or e.get('type') or 'div'} {e.get('n') or ''}]".replace(" ]", "]"))
        if tag == "speaker":
            s = text_of(e)
            if s:
                out.append(f"[speaker] {s}")
            return
        if tag in LINE:
            s = text_of(e)
            if s:
                out.append(f"|{e.get('n')} {s}" if tag == "l" and e.get("n") else s)
            return
        for c in e:
            walk_blocks(c)

    b = root.find(f".//{TEI}text"); body = b if b is not None else root
    walk_blocks(body)
    return unicodedata.normalize("NFC", "\n".join(out) + "\n")


def latinlib(path):
    h = path.read_bytes().decode("latin-1")
    h = re.sub(r"(?is)<(script|style|head).*?</\1>", "", h)
    h = re.sub(r"(?i)<br\s*/?>|</p>|<p[^>]*>", "\n", h)
    h = re.sub(r"<[^>]+>", "", h)
    lines = [re.sub(r"\s+", " ", html.unescape(x)).strip() for x in h.split("\n")]
    return "\n".join(x for x in lines if x) + "\n"


def gutenberg(path, enc="utf-8"):
    t = path.read_bytes().decode(enc).replace("\r\n", "\n")
    a = re.search(r"\*\*\* ?START OF (THE|THIS) PROJECT GUTENBERG[^\n]*\n|\*END\*THE SMALL PRINT![^\n]*\n", t)
    b = re.search(r"\*\*\* ?END OF (THE|THIS) PROJECT GUTENBERG|End of (the )?Project Gutenberg", t)
    return t[a.end() if a else 0: b.start() if b else len(t)].strip("\n") + "\n"


def asserved(path):
    return path.read_bytes().decode("utf-8", errors="replace").replace("\r\n", "\n").replace("\r", "\n")


def ocrdir(d):
    pages = sorted(pathlib.Path(d).glob("n*.txt"))
    return "".join(f"[page n{p.stem[1:]}]\n" + p.read_text(encoding="utf-8").replace("\f", "") for p in pages)


def sefaria(path):
    """Sefaria API v3 JSON as fetched: the one version's segments, one per line, numbered [segment N]."""
    import json as _j
    d = _j.loads(pathlib.Path(path).read_text(encoding="utf-8"))
    v = d["versions"][0]
    t = v["text"]
    flat = []
    def walk(x):
        if isinstance(x, list):
            for y in x: walk(y)
        elif x: flat.append(re.sub(r"<[^>]+>", "", html.unescape(x)).strip())
    walk(t)
    head = f"[{d.get('ref')} · {v.get('versionTitle')} · {v.get('license')}]"
    return unicodedata.normalize("NFC", head + "\n" + "".join(f"[segment {k}] {x}\n" for k, x in enumerate(flat, 1)))


J = {}
for f in sorted(ST.glob("*.xml")):
    J[f.name.rsplit(".", 1)[0]] = tei(f)
for k, v in J.items():
    (OUT / f"{k}.txt").write_text(v, encoding="utf-8")
    print(f"{k:60} {v.count(chr(10)):>8} lines")
