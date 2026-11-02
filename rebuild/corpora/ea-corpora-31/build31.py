#!/usr/bin/env python3
"""EA-CORPORA-31 seat builder (a session tool, kept beside the seating it built). The 29th seating's builder
(rebuild/corpora/ea-corpora-29/build29.py) with two kinds added for the transmission seating:

  ocr_pages  pages of an Internet Archive scan whose own OCR layer cannot be read (Greek read as Latin), OCR'd in
             session with Tesseract 5.3.4 and the tessdata_best models named in the item; the OCR of each page is
             kept under original/<identifier>/ocr/, the text layer joins the pages under '=== n<leaf> ===' headings,
             and each page image is recorded by URL and the sha256 of the bytes served (the images are not copied)
  dfhg       one author of the Digital Fragmenta Historicorum Graecorum (Müller's FHG), fetched from the DFHG API as
             served (JSON); the text layer is each fragment's number, FHG page, work and book, witness and Greek text

Every other kind is built by build29.py's own code. Loci are looked up whitespace-normalized, as before.
    python3 build31.py <spec.json> <stage> [--loci]"""
import hashlib, json, pathlib, sys
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "ea-corpora-29")); sys.path.insert(0, str(HERE.parent / "ea-corpora-27"))
import build29 as B
import seat as S


def sha_bytes(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def build_extra(it, seat):
    k = it["kind"]
    (seat / "text").mkdir(parents=True, exist_ok=True)
    if k == "ocr_pages":
        ident = it["identifier"]
        parts, originals, pages = [], [], []
        for n in it["pages"]:
            src = HERE / "ocr" / f"{it['ocr_prefix']}-n{n}.txt"
            dest = seat / "original" / ident / "ocr" / f"n{n:04d}.txt"
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(src.read_bytes())
            originals.append(dest.relative_to(seat).as_posix())
            parts.append(f"=== n{n} ===\n" + src.read_text(encoding="utf-8").strip("\n"))
            img = pathlib.Path(it["images_dir"]) / f"n{n}.jpg"
            pages.append({"leaf": n, "url": f"https://archive.org/download/{ident}/page/n{n}.jpg",
                          "sha256_as_served": sha_bytes(img) if img.exists() else None})
        tr = f"text/{it['slug']}.ocr.txt"
        (seat / tr).write_text("\n\n".join(parts) + "\n", encoding="utf-8")
        oi = {"source": "Internet Archive", "identifier": ident, "url": f"https://archive.org/details/{ident}",
              "ocr": it["ocr_engine"], "pages_by_reference": pages,
              "why": it.get("why", "the Archive's own OCR layer reads the Greek as Latin; the pages were OCR'd in session and the images are held by reference")}
        return {"slug": it["slug"], "work": it["work"], "text": tr, "originals": originals,
                "lines": sum(1 for _ in open(seat / tr, encoding="utf-8"))}, oi
    if k == "dfhg":
        dest = seat / "original" / it["path"]
        S.fetch(it["url"], dest)
        frs = json.loads(dest.read_bytes().decode("utf-8"))
        out = []
        for f in frs:
            head = f"=== fr. {f.get('fragment_number','')}{f.get('fragment_letter','') or ''} · FHG {f.get('volume','')} p. {f.get('page','')} · {f.get('work','')}" + (f" · {f['book']}" if f.get("book") else "") + " ==="
            out.append(head)
            if f.get("witness"):
                out.append(" ".join(f["witness"].split()))
            out.append(" ".join((f.get("text") or "").split()))
            out.append("")
        tr = f"text/{it['slug']}.txt"
        (seat / tr).write_text("\n".join(out).strip() + "\n", encoding="utf-8")
        oi = {"source": "Digital Fragmenta Historicorum Graecorum (DFHG), Leipzig", "url": it["url"], "fragments": len(frs),
              "sha256": S.sha(dest)}
        return {"slug": it["slug"], "work": it["work"], "text": tr, "originals": [f"original/{it['path']}"],
                "lines": sum(1 for _ in open(seat / tr, encoding="utf-8"))}, oi
    raise SystemExit(f"unknown kind {k}")


def build(spec, stage):
    seat = pathlib.Path(stage) / spec["corpus"]
    extra = [it for it in spec["items"] if it["kind"] in ("ocr_pages", "dfhg")]
    rest = dict(spec); rest["items"] = [it for it in spec["items"] if it["kind"] not in ("ocr_pages", "dfhg")]
    rest["loci"] = []
    works, origin = [], []
    if rest["items"]:
        s0 = B.build(rest, stage)
        works, origin = s0["works"]["list"], s0["origin"]["items"]
    for it in extra:
        w, oi = build_extra(it, seat)
        if it.get("class"):
            w["class"] = it["class"]
        works.append(w); origin.append(oi)
    order = {it["slug"]: i for i, it in enumerate(spec["items"])}
    pairs = sorted(zip(works, origin), key=lambda p: order.get(p[0]["slug"], 99)) if len(works) == len(origin) else None
    if pairs:
        works, origin = [p[0] for p in pairs], [p[1] for p in pairs]
    verified, missing = [], []
    for lo in spec.get("loci", []):
        t = S.norm((seat / lo["text"]).read_text(encoding="utf-8", errors="replace"))
        (verified if S.norm(lo["find"]) in t else missing).append(f"{lo['label']} — '{lo['find']}'" + (f" ({lo['note']})" if lo.get("note") else ""))
    src = {"corpus": spec["corpus"], "seat": spec["seat"], "title": spec["title"],
           "edition": spec.get("edition") or "; ".join(w["work"] for w in works),
           "language": spec["language"], "license": spec["license"], "fetched": spec["fetched"],
           "origin": {"items": origin, "fetched": spec["fetched"], "transport": "in-session fetch (Transport D); No-Double-Draw"},
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


if __name__ == "__main__":
    spec = json.load(open(sys.argv[1]))
    s = B.reloci(spec, sys.argv[2]) if "--loci" in sys.argv else build(spec, sys.argv[2])
    print(spec["corpus"], "works", s["works"]["count"], "lines", s["lines_total"], "loci ok", len(s["verified_loci"]), "missing", s["loci_not_found"])
