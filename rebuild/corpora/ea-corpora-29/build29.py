#!/usr/bin/env python3
"""EA-CORPORA-29 seat builder (a session tool, kept beside the seating it built). The 27th seating's builder
(rebuild/corpora/ea-corpora-27/seat.py) with three kinds added for the pluriform seating:

  ws      a Wikisource page fetched as served (ws.py), its revision recorded, the text layer derived by code
  gretil  a GRETIL TEI file; the text layer is the TEI <body> reduced to lines (one per <l>, <p> or <lg>)
  text    a plain-text file fetched as served (Project Gutenberg), kept as text
  aozora  an Aozora Bunko XHTML file (Shift_JIS) kept as served; the text layer is its main_text, ruby kept as base
          text with the reading in 《》 after it, tags dropped
  ia_ref  an Internet Archive scan too large to copy: the OCR text layer (_djvu.txt) is copied, the scan is recorded
          by identifier, file name, size and the md5 the Archive publishes for it
  extract a line range of a text already seated in this library, copied with the source's path and sha256
A ws item may carry "titles" (several pages of one work): each page is kept, and the text layer joins them under
'=== <title> ===' headings.

Items of the older kinds (tei, ia, file) are built by seat.py's own code. Loci are looked up whitespace-normalized in
the text the locus names, as before.
    python3 build29.py <spec.json> <stage>"""
import hashlib, json, pathlib, re, sys, html, urllib.parse, urllib.request
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "ea-corpora-27")); sys.path.insert(0, str(HERE))
import seat as S
import ws as W
import xml.etree.ElementTree as ET

# Resume: a stage file already fetched in this session is reused (its bytes are the ones the manifest will record).
_sfetch, _wget = S.fetch, W.get
def _fetch_once(url, dest):
    dest = pathlib.Path(dest)
    if dest.exists() and dest.stat().st_size:
        return
    _sfetch(url, dest)
S.fetch = _fetch_once


def gretil_text(path):
    root = ET.parse(path).getroot()
    T = "{http://www.tei-c.org/ns/1.0}"
    body = root.find(f".//{T}body")
    out = []
    def walk(el):
        tag = el.tag.replace(T, "")
        if tag in ("l", "p"):
            t = " ".join("".join(el.itertext()).split())
            if t:
                out.append(t)
            return
        if tag == "head":
            t = " ".join("".join(el.itertext()).split())
            if t:
                out.append(f"=== {t} ===")
            return
        if tag in ("note",):
            return
        for c in el:
            walk(c)
        if tag == "lg":
            out.append("")
    walk(body if body is not None else root)
    return re.sub(r"\n{3,}", "\n\n", "\n".join(out)).strip() + "\n"


def build(spec, stage):
    seat = pathlib.Path(stage) / spec["corpus"]
    works, origin_items = [], []
    for it in spec["items"]:
        k = it["kind"]
        if k in ("tei", "ia", "file"):
            sub = dict(spec); sub["items"] = [it]; sub["loci"] = []
            s0 = S.build(sub, stage)
            works += s0["works"]["list"]; origin_items += s0["origin"]["items"]
            continue
        if k == "ws" and it.get("titles"):
            parts, origs = [], []
            for n, ti in enumerate(it["titles"], 1):
                r = W.fetch(it["lang"], ti, seat, f"{it['slug']}-{n:02d}")
                origin_items.append({kk: r[kk] for kk in ("source", "title", "url", "revision", "permalink", "sha256")})
                parts.append(f"=== {ti} ===\n" + (seat / r["text"]).read_text(encoding="utf-8"))
                (seat / r["text"]).unlink(); origs.append(r["file"])
            tr = f"text/{it['slug']}.txt"
            (seat / tr).write_text("\n".join(parts), encoding="utf-8")
            w = {"slug": it["slug"], "work": it["work"], "text": tr, "originals": origs,
                 "lines": sum(1 for _ in open(seat / tr, encoding="utf-8"))}
        elif k == "ws":
            r = W.fetch(it["lang"], it["title"], seat, it["slug"])
            origin_items.append({kk: r[kk] for kk in ("source", "title", "url", "revision", "permalink", "sha256")})
            w = {"slug": it["slug"], "work": it["work"], "text": r["text"], "originals": [r["file"]], "lines": r["lines"]}
        elif k == "aozora":
            dest = seat / "original" / it["path"]
            S.fetch(it["url"], dest)
            h = dest.read_bytes().decode("shift_jis", "replace")
            m = re.search(r'<div class="main_text">(.*?)<div class="bibliographical_information">', h, re.S)
            b = m.group(1) if m else h
            b = re.sub(r'<rp>.*?</rp>', '', b, flags=re.S)
            b = re.sub(r'<rt>(.*?)</rt>', r'《\1》', b, flags=re.S)
            b = re.sub(r'<br\s*/?>', '\n', b)
            b = html.unescape(re.sub(r'<[^>]+>', '', b))
            tr = f"text/{it['slug']}.txt"
            (seat / "text").mkdir(parents=True, exist_ok=True)
            (seat / tr).write_text(re.sub(r'\n{3,}', '\n\n', b).strip() + "\n", encoding="utf-8")
            origin_items.append({"source": "Aozora Bunko", "url": it["url"], "card": it.get("card", ""), "base_text": it.get("base_text", "")})
            w = {"slug": it["slug"], "work": it["work"], "text": tr, "originals": [f"original/{it['path']}"],
                 "lines": sum(1 for _ in open(seat / tr, encoding="utf-8"))}
        elif k == "ia_ref":
            ident, md = it["identifier"], json.load(urllib.request.urlopen(urllib.request.Request(f"https://archive.org/metadata/{it['identifier']}", headers=S.UA), timeout=120))
            fl = {f["name"]: f for f in md["files"]}
            djvu = it.get("ocr") or f"{ident}_djvu.txt"
            S.fetch(f"https://archive.org/download/{ident}/{urllib.parse.quote(djvu)}", seat / "original" / ident / djvu)
            tr = f"text/{it['slug']}.ocr.txt"
            (seat / "text").mkdir(parents=True, exist_ok=True)
            (seat / tr).write_bytes((seat / "original" / ident / djvu).read_bytes().replace(b"\r\n", b"\n"))
            scan = it["scan"]
            origin_items.append({"source": "Internet Archive", "identifier": ident, "url": f"https://archive.org/details/{ident}", "files": [djvu],
                                 "scan_by_reference": {"file": scan, "url": f"https://archive.org/download/{ident}/{urllib.parse.quote(scan)}",
                                                       "size": int(fl[scan]["size"]), "md5": fl[scan]["md5"],
                                                       "why": "too large to carry in a bundle; the Archive's md5 identifies the scan the OCR layer was made from"}})
            w = {"slug": it["slug"], "work": it["work"], "text": tr, "originals": [f"original/{ident}/{djvu}"],
                 "lines": sum(1 for _ in open(seat / tr, encoding="utf-8", errors="replace"))}
        elif k == "blogger":
            dest = seat / "original" / it["path"]
            S.fetch(it["url"], dest)
            h = dest.read_bytes().decode("utf-8", "replace")
            m = re.search(r"<div class='post-body entry-content'[^>]*>(.*?)<div class='post-footer'>", h, re.S)
            tr = f"text/{it['slug']}.txt"
            (seat / "text").mkdir(parents=True, exist_ok=True)
            (seat / tr).write_text(W.text_of('<div class="mw-parser-output">' + (m.group(1) if m else h) + '<div class="printfooter">'), encoding="utf-8")
            origin_items.append({"source": "Blogger (mindcontrolpoems.blogspot.com)", "url": it["url"], "published": it.get("published", ""), "sha256": S.sha(dest)})
            w = {"slug": it["slug"], "work": it["work"], "text": tr, "originals": [f"original/{it['path']}"],
                 "lines": sum(1 for _ in open(seat / tr, encoding="utf-8"))}
        elif k == "extract":
            src_path = pathlib.Path(it["from"])
            L = src_path.read_text(encoding="utf-8").splitlines()
            a, b = it["lines"]
            tr = f"text/{it['slug']}.txt"
            (seat / "text").mkdir(parents=True, exist_ok=True)
            (seat / tr).write_text("\n".join(L[a - 1:b]).strip("\n") + "\n", encoding="utf-8")
            origin_items.append({"source": "this library", "from": it["from_rel"], "lines": [a, b], "sha256_of_source": S.sha(src_path), "seat": it.get("seat_of_source", "")})
            w = {"slug": it["slug"], "work": it["work"], "text": tr, "originals": [it["from_rel"]],
                 "lines": sum(1 for _ in open(seat / tr, encoding="utf-8"))}
        elif k in ("gretil", "text"):
            dest = seat / "original" / it["path"]
            S.fetch(it["url"], dest)
            (seat / "text").mkdir(parents=True, exist_ok=True)
            tr = f"text/{it['slug']}.txt"
            if k == "gretil":
                (seat / tr).write_text(gretil_text(dest), encoding="utf-8")
            else:
                (seat / tr).write_bytes(dest.read_bytes().replace(b"\r\n", b"\n"))
            origin_items.append({"source": it.get("source", ""), "url": it["url"]} | ({"licence_at_file": it["licence"]} if it.get("licence") else {}))
            w = {"slug": it["slug"], "work": it["work"], "text": tr, "originals": [f"original/{it['path']}"],
                 "lines": sum(1 for _ in open(seat / tr, encoding="utf-8", errors="replace"))}
        else:
            raise SystemExit(f"unknown kind {k}")
        if it.get("class"):
            w["class"] = it["class"]
        works.append(w)
    verified, missing = [], []
    for lo in spec.get("loci", []):
        t = S.norm((seat / lo["text"]).read_text(encoding="utf-8", errors="replace"))
        (verified if S.norm(lo["find"]) in t else missing).append(f"{lo['label']} — '{lo['find']}'" + (f" ({lo['note']})" if lo.get("note") else ""))
    verified += [f"{lo['label']} — '{lo['reads']}' (read from the scan, {lo['where']})" for lo in spec.get("scan_loci", [])]
    src = {"corpus": spec["corpus"], "seat": spec["seat"], "title": spec["title"],
           "edition": spec.get("edition") or "; ".join(w["work"] for w in works),
           "language": spec["language"], "license": spec["license"], "fetched": spec["fetched"],
           "origin": {"items": origin_items, "fetched": spec["fetched"], "transport": "in-session fetch (Transport D); No-Double-Draw"},
           "works": {"count": len(works), "units": spec.get("units", "one text file per work"), "list": works},
           "normalization": spec["normalization"], "scope": spec["scope"], "verified_loci": verified, "loci_not_found": missing,
           "lines_total": sum(w.get("lines", 0) for w in works), "why_seated": spec["why_seated"], "spine": spec["spine"],
           "ruling": spec["ruling"], "seating": spec.get("seating", "")}
    for kk in ("classes", "queued", "witness_note", "not_seated", "contested", "cross_references"):
        if spec.get(kk):
            src[kk] = spec[kk]
    (seat / "source.json").write_text(json.dumps(src, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    lines = [f"{S.sha(p)}  {p.relative_to(seat).as_posix()}" for p in sorted(seat.rglob("*")) if p.is_file() and p.name not in ("MANIFEST.sha256", "source.json")]
    (seat / "MANIFEST.sha256").write_text("\n".join(lines) + "\n")
    return src


def reloci(spec, stage):
    """Re-verify the spec's loci against an already-built seat and rewrite source.json (the MANIFEST does not cover it)."""
    seat = pathlib.Path(stage) / spec["corpus"]
    src = json.load(open(seat / "source.json"))
    verified, missing = [], []
    for lo in spec.get("loci", []):
        t = S.norm((seat / lo["text"]).read_text(encoding="utf-8", errors="replace"))
        (verified if S.norm(lo["find"]) in t else missing).append(f"{lo['label']} — '{lo['find']}'" + (f" ({lo['note']})" if lo.get("note") else ""))
    verified += [f"{lo['label']} — '{lo['reads']}' (read from the scan, {lo['where']})" for lo in spec.get("scan_loci", [])]
    src["verified_loci"], src["loci_not_found"] = verified, missing
    for kk in ("edition", "license", "normalization", "scope", "why_seated", "spine", "ruling", "seating", "title", "classes", "queued", "witness_note", "not_seated", "contested", "cross_references"):
        if spec.get(kk):
            src[kk] = spec[kk]
    for w in src["works"]["list"]:
        it = next((i for i in spec["items"] if i["slug"] == w["slug"]), None)
        if it:
            w["work"] = it["work"]
            if it.get("class"):
                w["class"] = it["class"]
    (seat / "source.json").write_text(json.dumps(src, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return src


if __name__ == "__main__":
    spec = json.load(open(sys.argv[1]))
    s = reloci(spec, sys.argv[2]) if "--loci" in sys.argv else build(spec, sys.argv[2])
    print(spec["corpus"], "works", s["works"]["count"], "lines", s["lines_total"], "loci ok", len(s["verified_loci"]), "missing", s["loci_not_found"])
