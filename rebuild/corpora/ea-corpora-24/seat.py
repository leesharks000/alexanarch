#!/usr/bin/env python3
"""Seat builder for EA-CORPORA-20 onward (session tool; not part of the archive). EA-CORPORA-24 adds the
"pages" kind (every image an index page links, in file-name order; the scan is the witness, no text layer),
"wikisource" items (pre-harvested wikitext and rendered HTML, the text layer derived from the HTML), and
"scan_loci" (loci read by eye from a page of a scan, recorded with the page).

A spec (JSON) names the seat, its items and its loci. The builder fetches each item into
<stage>/<corpus>/original/..., derives text/<slug>.* (IA OCR layers as fetched; TEI reduced to
plain text by code, chapter and verse kept), finds every locus in the seated text, and writes
source.json and MANIFEST.sha256 (original/ and text/, as the seats before it do).
"""
import hashlib, json, pathlib, re, sys, urllib.parse, urllib.request, xml.etree.ElementTree as ET

TEI = "{http://www.tei-c.org/ns/1.0}"
UA = {"User-Agent": "alexanarch-seating/1.0 (https://www.alexanarch.org)"}


def fetch(url, dest):
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists() and dest.stat().st_size > 0:
        return dest
    import time
    for k in range(6):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=600) as r, open(dest, "wb") as f:
                while True:
                    b = r.read(1 << 20)
                    if not b:
                        break
                    f.write(b)
            return dest
        except Exception:
            if dest.exists():
                dest.unlink()
            if k == 5:
                raise
            time.sleep(10 * (k + 1))


def tei_text(path):
    """The edition divisions of a TEI file as plain text: a heading line per textpart
    ('=== chapter 3 ==='), one line per <l>/<ab>/<p> with its n where given."""
    root = ET.parse(path).getroot()
    out = []

    def walk(el, depth):
        tag = el.tag.replace(TEI, "")
        if tag == "div" and el.get("type") == "textpart":
            out.append(f"=== {el.get('subtype') or 'part'} {el.get('n') or el.get('{http://www.w3.org/XML/1998/namespace}id') or ''} ===".replace("  ", " "))
        if tag in ("l", "p") or (tag == "ab" and not el.findall(f"{TEI}l")):
            t = " ".join("".join(el.itertext()).split())
            if t:
                out.append(f"{el.get('n')} {t}" if el.get("n") else t)
            return
        if tag in ("note", "label") and depth > 0:
            if tag == "label":
                t = " ".join("".join(el.itertext()).split())
                if t:
                    out.append(f"[{t}]")
            return
        for c in el:
            walk(c, depth + 1)

    eds = [d for d in root.iter(f"{TEI}div") if d.get("type") == "edition"]
    for d in eds:
        note = d.find(f"{TEI}note")
        out.append(f"##### edition {d.get('{http://www.w3.org/XML/1998/namespace}id') or ''} ({d.get('{http://www.w3.org/XML/1998/namespace}lang') or ''})"
                   + (f" — {' '.join(''.join(note.itertext()).split())}" if note is not None else ""))
        for c in d:
            walk(c, 1)
    return "\n".join(out) + "\n"


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def norm(s):
    return " ".join(s.split())


def build(spec, stage):
    seat = pathlib.Path(stage) / spec["corpus"]
    works, origin_items = [], []
    for it in spec["items"]:
        if it["kind"] == "ia":
            ident = it["identifier"]
            files = []
            for fn in it["files"]:
                fetch(f"https://archive.org/download/{ident}/{urllib.parse.quote(fn)}", seat / "original" / ident / fn)
                files.append(fn)
            djvu = [f for f in files if f.endswith("_djvu.txt")]
            text_rel = f"text/{it['slug']}.ocr.txt"
            if djvu:
                (seat / "text").mkdir(parents=True, exist_ok=True)
                (seat / text_rel).write_bytes((seat / "original" / ident / djvu[0]).read_bytes().replace(b"\r\n", b"\n"))
            origin_items.append({"source": "Internet Archive", "identifier": ident, "url": f"https://archive.org/details/{ident}", "files": files})
            originals = [f"original/{ident}/{f}" for f in files]
        elif it["kind"] == "tei":
            dest = seat / "original" / it["path"]
            fetch(it["url"], dest)
            text_rel = f"text/{it['slug']}.txt"
            (seat / "text").mkdir(parents=True, exist_ok=True)
            (seat / text_rel).write_text(tei_text(dest), encoding="utf-8")
            origin_items.append({k: v for k, v in it.items() if k in ("source", "url", "repository", "commit", "file")} | {"source": it.get("source", "")})
            originals = [f"original/{it['path']}"]
        elif it["kind"] == "file":
            dest = seat / "original" / it["path"]
            fetch(it["url"], dest)
            text_rel = it.get("text")
            if it.get("as_text"):
                (seat / "text").mkdir(parents=True, exist_ok=True)
                text_rel = f"text/{it['slug']}.txt"
                (seat / text_rel).write_bytes(dest.read_bytes().replace(b"\r\n", b"\n"))
            origin_items.append({"source": it.get("source", ""), "url": it["url"]})
            originals = [f"original/{it['path']}"]
        elif it["kind"] == "pages":
            import re as _re
            html = urllib.request.urlopen(urllib.request.Request(it["dir"], headers=UA), timeout=120).read().decode("utf-8", "replace")
            imgs = sorted({h for h in _re.findall(r'href="([^"/?]+\.(?:gif|jpg|png))"', html, _re.I)})
            for im in imgs:
                fetch(it["dir"] + im, seat / "original" / it["path"] / im)
            text_rel = None
            origin_items.append({"source": it.get("source", ""), "url": it["dir"], "pages": len(imgs)})
            originals = [f"original/{it['path']}/{im}" for im in imgs]
        elif it["kind"] == "wikisource":
            text_rel = it["text"]
            origin_items.append({"source": "Wikisource (zh)", "url": it["url"], "revisions": it["revisions"]})
            originals = it["originals"]
        w = {"slug": it["slug"], "work": it["work"], "text": text_rel, "originals": originals}
        if it.get("class"):
            w["class"] = it["class"]
        if text_rel and (seat / text_rel).exists():
            w["lines"] = sum(1 for _ in open(seat / text_rel, encoding="utf-8", errors="replace"))
        works.append(w)

    # Loci: each string looked up, whitespace-normalized, in the text the locus names.
    verified, missing = [], []
    for lo in spec.get("loci", []):
        t = norm((seat / lo["text"]).read_text(encoding="utf-8", errors="replace"))
        (verified if norm(lo["find"]) in t else missing).append(f"{lo['label']} — '{lo['find']}'" + (f" ({lo['note']})" if lo.get("note") else ""))

    verified += [f"{lo['label']} — '{lo['reads']}' (read from the scan, {lo['where']})" for lo in spec.get("scan_loci", [])]
    src = {
        "corpus": spec["corpus"], "seat": spec["seat"], "title": spec["title"],
        "edition": "; ".join(w["work"] for w in works) if not spec.get("edition") else spec["edition"],
        "language": spec["language"], "license": spec["license"], "fetched": spec["fetched"],
        "origin": {"items": origin_items, "fetched": spec["fetched"], "transport": "in-session fetch (Transport D); No-Double-Draw"},
        "works": {"count": len(works), "units": spec.get("units", "one text file per work"), "list": works},
        "normalization": spec["normalization"], "scope": spec["scope"],
        "verified_loci": verified, "loci_not_found": missing,
        "lines_total": sum(w.get("lines", 0) for w in works),
        "why_seated": spec["why_seated"], "spine": spec["spine"], "ruling": spec["ruling"],
    }
    for k in ("classes", "queued", "witness_note", "not_seated", "contested"):
        if spec.get(k):
            src[k] = spec[k]
    (seat / "source.json").write_text(json.dumps(src, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    lines = []
    for p in sorted(seat.rglob("*")):
        if p.is_file() and p.name not in ("MANIFEST.sha256", "source.json"):
            lines.append(f"{sha(p)}  {p.relative_to(seat).as_posix()}")
    (seat / "MANIFEST.sha256").write_text("\n".join(lines) + "\n")
    return src


if __name__ == "__main__":
    spec = json.load(open(sys.argv[1]))
    s = build(spec, sys.argv[2])
    print(spec["corpus"], "works", s["works"]["count"], "lines", s["lines_total"], "loci ok", len(s["verified_loci"]), "missing", s["loci_not_found"])
