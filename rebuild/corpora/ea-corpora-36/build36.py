#!/usr/bin/env python3
"""EA-CORPORA-36 seat builder (a session tool, kept beside the seating it built). The thirty-fourth seating's builder
(rebuild/corpora/ea-corpora-34/build34.py) with one kind added:

  tcp  a Text Creation Partnership (EEBO-TCP) TEI file fetched as served from the Partnership's GitHub repository and
       kept under original/; the text layer is the <text> element reduced to lines (one per <head>, <p>, <l>, <q>-free
       block), original spelling and long s kept, the Partnership's end-of-line hyphen marks (<g ref="char:EOLhyphen"/>)
       removed so that the word they divide is joined, <gap> recorded as [gap]. The licence is read from the file's
       <availability>.

Every other kind is built by build34.py and the builders it extends.   python3 build36.py <spec.json> <stage> [--loci]"""
import json, pathlib, re, sys, xml.etree.ElementTree as ET
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "ea-corpora-34"))
import build34 as B34
B32, B31, S = B34.B32, B34.B31, B34.S
T = "{http://www.tei-c.org/ns/1.0}"
_route34 = B34.route


def tcp_text(path):
    raw = path.read_text(encoding="utf-8")
    raw = re.sub(r'<g ref="char:EOLhyphen"/>\s*', "", raw)
    root = ET.fromstring(raw)
    avail = " ".join("".join(root.find(f".//{T}availability").itertext()).split())
    out = []

    def walk(el):
        tag = el.tag.replace(T, "")
        if tag in ("note",):
            return
        if tag == "gap":
            out.append("[gap]"); return
        if tag in ("head", "p", "l", "salute", "label", "closer", "signed", "trailer"):
            t = " ".join("".join(x if isinstance(x, str) else "" for x in el.itertext()).split())
            if t:
                out.append(t)
            return
        if tag == "lg":
            out.append("")
        for c in el:
            walk(c)
        if tag in ("lg", "div"):
            out.append("")

    walk(root.find(f"{T}text"))
    return re.sub(r"\n{3,}", "\n\n", "\n".join(out)).strip() + "\n", avail


def tcp(it, seat):
    dest = seat / "original" / it["path"]
    S.fetch(it["url"], dest)
    txt, avail = tcp_text(dest)
    tr = f"text/{it['slug']}.txt"
    (seat / "text").mkdir(parents=True, exist_ok=True)
    (seat / tr).write_text(txt, encoding="utf-8")
    oi = {"source": "Text Creation Partnership (EEBO-TCP Phase I), GitHub textcreationpartnership", "url": it["url"],
          "tcp_id": it["tcp_id"], "stc": it.get("stc", ""), "licence_at_file": avail, "sha256": S.sha(dest)}
    return {"slug": it["slug"], "work": it["work"], "text": tr, "originals": [f"original/{it['path']}"],
            "lines": sum(1 for _ in open(seat / tr, encoding="utf-8"))}, oi


def route(it, seat):
    if it.get("_tcp"):
        it = dict(it); it.pop("_tcp"); it["kind"] = "tcp"
        return tcp(it, seat)
    return _route34(it, seat)


def build(spec, stage):
    sp = json.loads(json.dumps(spec))
    for it in sp["items"]:
        if it["kind"] == "pdf_ocr":
            it["kind"] = "dfhg"; it["_pdf"] = True
        if it["kind"] == "tcp":
            it["kind"] = "dfhg"; it["_tcp"] = True      # build31.build routes dfhg to build_extra
    B31.build_extra = route
    seat = pathlib.Path(stage) / spec["corpus"]
    src = B32._orig_build(sp, stage)
    return B32.finish(spec, seat, src)


if __name__ == "__main__":
    spec = json.load(open(sys.argv[1]))
    if "--loci" in sys.argv:
        s = B31.B.reloci(spec, sys.argv[2])
        s = B32.finish(spec, pathlib.Path(sys.argv[2]) / spec["corpus"], s)
    else:
        s = build(spec, sys.argv[2])
    print(spec["corpus"], "works", s["works"]["count"], "lines", s["lines_total"], "loci ok", len(s["verified_loci"]), "missing", s["loci_not_found"])
