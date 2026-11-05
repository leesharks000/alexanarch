#!/usr/bin/env python3
"""EA-CORPORA-34 seat builder (the 33rd seating's builder, unchanged; no pdf_ocr item is used) (a session tool, kept beside the seating it built). The 32nd seating's builder
(rebuild/corpora/ea-corpora-32/build32.py) with one kind added:

  pdf_ocr  pages of an Internet Archive PDF, rasterized in session at 300 dpi (pdftoppm -r 300 -gray) and OCR'd with
           Tesseract; the PDF is held by reference with the Archive's md5 and the sha256 of the bytes as fetched; each
           page's OCR is copied under original/<identifier>/ocr/p<NNNN>.txt and joined into text/<slug>.ocr.txt with a
           '=== p<N> ===' line before each page. Used where the Archive's own OCR layer reads the Greek as Latin, and
           where the page images endpoint was too slow to fetch leaf by leaf (2026-11-04).

    python3 build33.py <spec.json> <stage> [--loci]"""
import json, pathlib, sys
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "ea-corpora-32"))
import build32 as B32
B31 = B32.B31
S = B31.S
OCR = pathlib.Path("/tmp/claude-0/-home-claude/97be5201-55d8-50c9-b9d9-c76c8dde5ac6/scratchpad/ea33/ocr")
_b32_extra = B32.build_extra


def pdf_ocr(it, seat):
    ident = it["identifier"]
    (seat / "text").mkdir(parents=True, exist_ok=True)
    parts, originals = [], []
    for p in it["pages"]:
        src = OCR / f"{it['ocr_prefix']}-p{p}.txt"
        dest = seat / "original" / ident / "ocr" / f"p{p:04d}.txt"
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(src.read_bytes())
        originals.append(dest.relative_to(seat).as_posix())
        parts.append(f"=== p{p} ===\n" + src.read_text(encoding="utf-8").strip("\n"))
    tr = f"text/{it['slug']}.ocr.txt"
    (seat / tr).write_text("\n\n".join(parts) + "\n", encoding="utf-8")
    oi = {"source": "Internet Archive", "identifier": ident, "url": f"https://archive.org/details/{ident}",
          "pdf_by_reference": {"file": it["pdf"], "url": f"https://archive.org/download/{ident}/{it['pdf']}", "md5": it["pdf_md5"],
                               "sha256_as_fetched": it["pdf_sha256"], "pages": f"{it['pages'][0]}–{it['pages'][-1]} of {it['pdf_pages']}"},
          "ocr": it["ocr_engine"],
          "why": it.get("why", "the Archive's own OCR layer reads the Greek as Latin; the PDF pages were rasterized and OCR'd in session")}
    return {"slug": it["slug"], "work": it["work"], "text": tr, "originals": originals,
            "lines": sum(1 for _ in open(seat / tr, encoding="utf-8"))}, oi


def route(it, seat):
    if it.get("_pdf"):
        it = dict(it); it.pop("_pdf"); it["kind"] = "pdf_ocr"
        return pdf_ocr(it, seat)
    return _b32_extra(it, seat)


def build(spec, stage):
    sp = json.loads(json.dumps(spec))
    for it in sp["items"]:
        if it["kind"] == "pdf_ocr":
            it["kind"] = "dfhg"; it["_pdf"] = True      # build31.build routes dfhg to build_extra
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
