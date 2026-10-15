#!/usr/bin/env python3
"""build_seats.py — assemble the ten EA-CORPORA-18 seats from the fetched files.

    python3 rebuild/corpora/ea-corpora-18/build_seats.py --dl <download dir> [--dry]

Reads seats.json beside it. For each seat writes data/corpora/<corpus>/:
  original/   the files as fetched — Gutenberg plain text (gutenberg-<id>.txt); Internet Archive scan and
              OCR text (original/<identifier>/...); Wikisource rendered text with its page list
              (original/wikisource-<lang>-<slug>.txt, .pages.json)
  text/       one file per work: Gutenberg stripped at the START/END markers, CRLF to LF; Internet Archive
              OCR as fetched (<slug>.ocr.txt — uncorrected, the scan is the witness); Wikisource text as fetched
  source.json the seat record (seats.json entry + origin, fetched date, works, lines, verified loci)
  MANIFEST.sha256  sha256 of every file under original/ and text/
A locus is kept only if its string occurs in the named work's text; every miss is printed and recorded
under loci_not_found (laws record; they do not block). Deterministic given the same downloads.
"""
import argparse, hashlib, json, os, pathlib, re, shutil, sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
SPEC = pathlib.Path(__file__).with_name("seats.json")
FETCHED = "2026-10-15"


def pg_strip(raw):
    t = raw.replace("\r\n", "\n").replace("\r", "\n")
    s = re.search(r"^\*\*\* ?START OF (THE|THIS) PROJECT GUTENBERG EBOOK[^\n]*\n", t, re.M)
    e = re.search(r"^\*\*\* ?END OF (THE|THIS) PROJECT GUTENBERG EBOOK", t, re.M)
    return t[s.end() if s else 0:e.start() if e else len(t)].strip("\n") + "\n"


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dl", required=True)
    ap.add_argument("--dry", action="store_true")
    ap.add_argument("--show-front", action="store_true", help="print each Gutenberg text's first lines")
    a = ap.parse_args()
    dl = pathlib.Path(a.dl)
    spec = json.loads(SPEC.read_text(encoding="utf-8"))
    report = {}
    for S in spec["seats"]:
        name = S["corpus"]
        seat = ROOT / "data/corpora" / name
        if seat.exists() and not a.dry:
            shutil.rmtree(seat)  # this builder owns these ten seats outright; rebuilt whole each run
        (seat / "original").mkdir(parents=True, exist_ok=True) if not a.dry else None
        (seat / "text").mkdir(parents=True, exist_ok=True) if not a.dry else None
        works, origin, texts = [], [], {}
        for it in S["items"]:
            kind, ref = it["src"].split(":", 1)
            slug = it["slug"]
            if kind == "pg":
                src = dl / "pg" / f"gutenberg-{ref}.txt"
                raw = src.read_text(encoding="utf-8", errors="replace")
                body = pg_strip(raw)
                origs = [(src, f"original/gutenberg-{ref}.txt")]
                tname = f"text/{slug}.txt"
                origin.append({"source": "Project Gutenberg", "ebook": ref, "url": f"https://www.gutenberg.org/ebooks/{ref}"})
                if a.show_front:
                    print(f"\n--- {name} / {slug} (PG {ref})\n" + "\n".join(l for l in body.splitlines()[:40] if l.strip())[:900])
            elif kind == "ia":
                d = dl / "ia" / ref
                files = sorted(p for p in d.iterdir() if p.is_file())
                ocr = [p for p in files if p.name.endswith("_djvu.txt")]
                body = "".join((f"\n\n=== {p.name} ===\n\n" if len(ocr) > 1 else "") + p.read_text(encoding="utf-8", errors="replace").replace("\r\n", "\n") for p in ocr) if ocr else ""
                origs = [(p, f"original/{ref}/{p.name}") for p in files]
                tname = f"text/{slug}.ocr.txt" if body else None
                origin.append({"source": "Internet Archive", "identifier": ref, "url": f"https://archive.org/details/{ref}",
                               "files": [p.name for p in files]})
            elif kind.startswith("ws-"):
                lang = kind[3:]
                d = dl / f"ws-{'jarry' if lang == 'fr' else lang}"
                src = d / f"{ref}.txt"; pj = d / f"{ref}.pages.json"
                body = src.read_text(encoding="utf-8")
                pages = json.loads(pj.read_text(encoding="utf-8"))
                origs = [(src, f"original/wikisource-{lang}-{ref}.txt"), (pj, f"original/wikisource-{lang}-{ref}.pages.json")]
                tname = f"text/{slug}.txt"
                origin.append({"source": f"Wikisource ({lang})", "page": pages["source"], "pages": pages["pages"]})
            else:
                raise SystemExit(f"unknown source kind {kind}")
            if not a.dry:
                for p, rel in origs:
                    (seat / rel).parent.mkdir(parents=True, exist_ok=True)
                    shutil.copyfile(p, seat / rel)
                if tname:
                    (seat / tname).write_text(body, encoding="utf-8")
            texts[slug] = body
            works.append({"slug": slug, "work": it["work"], "text": tname, "originals": [rel for _, rel in origs],
                          "lines": body.count("\n") if body else 0})
        found, missed = [], []
        for slug, needle, label in S["loci"]:
            t = texts.get(slug, "")
            norm = lambda x: re.sub(r"\s+", " ", x.replace("’", "'"))
            (found if (needle in t or norm(needle) in norm(t)) else missed).append(label if needle in t or norm(needle) in norm(t) else f"{label} [string not found: {needle!r}]")
        lines = sum(w["lines"] for w in works)
        rec = {"corpus": name, "seat": f"EA-CORPORA-{S['card']}", "title": S["title"], "edition": "; ".join(w["work"] for w in works),
               "language": S["language"], "license": S["license"], "fetched": FETCHED,
               "origin": {"items": origin, "fetched": FETCHED, "transport": "in-session fetch (Transport D); No-Double-Draw"},
               "works": {"count": len(works), "units": "one text file per work", "list": works},
               "normalization": ("Project Gutenberg texts stripped at the START/END markers, CRLF to LF, otherwise unaltered; "
                                 "Internet Archive OCR text layers as fetched, uncorrected (text/<slug>.ocr.txt) — the scan under "
                                 "original/<identifier>/ is the witness; Wikisource texts as rendered from the proofread "
                                 "transcription, page headings marked '=== title ==='."),
               "scope": S["scope"], "verified_loci": found, "loci_not_found": missed, "lines_total": lines,
               "why_seated": S["why_seated"], "spine": S["spine"],
               "ruling": spec["_ruling"]}
        if not a.dry:
            (seat / "source.json").write_text(json.dumps(rec, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
            man = [f"{sha(p)}  {p.relative_to(seat).as_posix()}" for p in sorted(seat.rglob("*"))
                   if p.is_file() and p.name != "MANIFEST.sha256" and p.name != "source.json"]
            (seat / "MANIFEST.sha256").write_text("\n".join(man) + "\n", encoding="utf-8")
        size = sum(p.stat().st_size for p in seat.rglob("*") if p.is_file()) if seat.exists() else 0
        report[name] = {"card": S["card"], "works": len(works), "lines": lines, "loci": f"{len(found)}/{len(S['loci'])}",
                        "missed": missed, "MB": round(size / 1048576, 1)}
    for k, v in report.items():
        print(f"{v['card']} {k:26} works {v['works']:3}  lines {v['lines']:7}  loci {v['loci']}  {v['MB']:6} MB")
        for m in v["missed"]:
            print("      MISSED:", m)


if __name__ == "__main__":
    sys.exit(main())
