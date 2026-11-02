#!/usr/bin/env python3
"""EA-CORPORA-32 seat builder (a session tool, kept beside the seating it built). The 31st seating's builder
(rebuild/corpora/ea-corpora-31/build31.py) with its session OCR read from this seating's own ocr/, one kind added, and
the research field written into every seat:

  page_images  leaves of an Internet Archive scan held as images by URL and the sha256 of the bytes served (the images
               are not copied), with a transcription of named passages made by eye in session (transcriptions/<file>),
               for prints whose fount no OCR reads (the Aldine Greek)
  research     the study the seat was made for (the operator's rule of 2026-11-02: a seating conducted in the course of
               active research names that research), copied from the spec into source.json

    python3 build32.py <spec.json> <stage> [--loci]"""
import json, pathlib, sys
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "ea-corpora-31"))
import build31 as B31
B31.HERE = HERE            # ocr_pages reads ocr/<prefix>-n<leaf>.txt from this seating's folder
S = B31.S
_extra = B31.build_extra


def build_extra(it, seat):
    if it["kind"] != "page_images":
        return _extra(it, seat)
    ident = it["identifier"]
    (seat / "text").mkdir(parents=True, exist_ok=True)
    src = HERE / "transcriptions" / it["transcription"]
    dest = seat / "original" / ident / "transcription" / it["transcription"]
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(src.read_bytes())
    tr = f"text/{it['slug']}-transcription.txt"
    (seat / tr).write_bytes(src.read_bytes())
    pages = []
    for n in it["pages"]:
        img = pathlib.Path(it["images_dir"]) / f"n{n}.jpg"
        pages.append({"leaf": n, "url": f"https://archive.org/download/{ident}/page/n{n}.jpg", "sha256_as_served": B31.sha_bytes(img) if img.exists() else None})
    oi = {"source": "Internet Archive", "identifier": ident, "url": f"https://archive.org/details/{ident}", "pages_by_reference": pages,
          "transcription": {"file": dest.relative_to(seat).as_posix(), "made": "2026-11-02, by eye in session from the page images", "sha256": S.sha(dest)},
          "why": "the fount is read by no OCR available; the leaves are held by reference and the passages the study cites are transcribed"}
    return {"slug": it["slug"], "work": it["work"], "text": tr, "originals": [dest.relative_to(seat).as_posix()],
            "lines": sum(1 for _ in open(seat / tr, encoding="utf-8"))}, oi


B31.build_extra = build_extra
_orig_build = B31.build


def build(spec, stage):
    kinds = ("ocr_pages", "dfhg", "page_images")
    seat = pathlib.Path(stage) / spec["corpus"]
    # build31.build routes ocr_pages and dfhg to build_extra; page_images is routed the same way by relabelling it for the call
    sp = json.loads(json.dumps(spec))
    for it in sp["items"]:
        if it["kind"] == "page_images":
            it["kind"] = "dfhg"; it["_pi"] = True
    def route(it, seat_):
        if it.pop("_pi", False):
            it = dict(it, kind="page_images")
        return build_extra(it, seat_)
    B31.build_extra = route
    try:
        src = _orig_build(sp, stage)
    finally:
        B31.build_extra = build_extra
    return finish(spec, seat, src)


def finish(spec, seat, src):
    if spec.get("research"):
        src["research"] = spec["research"]
    (seat / "source.json").write_text(json.dumps(src, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return src


if __name__ == "__main__":
    spec = json.load(open(sys.argv[1]))
    if "--loci" in sys.argv:
        s = B31.B.reloci(spec, sys.argv[2])
        s = finish(spec, pathlib.Path(sys.argv[2]) / spec["corpus"], s)
    else:
        s = build(spec, sys.argv[2])
    print(spec["corpus"], "works", s["works"]["count"], "lines", s["lines_total"], "loci ok", len(s["verified_loci"]), "missing", s["loci_not_found"])
