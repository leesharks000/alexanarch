#!/usr/bin/env python3
"""build_originals_shelf.py — render the TLL reading-room card for a seated corpus.

WHY THIS EXISTS

A corpus seat is finished only when four things agree:

    data/corpora/<name>/          the seat itself (originals, text, source.json, manifest)
    data/api/corpora.json         the archive's machine index
    an EA-CORPORA-0N deposit      the citable act of seating, which assigns the card number
    originals/<name>/ on TLL      the rendered shelf a reader actually reaches

Until 2026-08-28 the fourth was produced by hand, and there was no generator
anywhere in either repository. Predictably it drifted: Aristotle and Plotinus
were seated in data/, indexed, and never reached the shelf — the same splitbrain
the capture registry had, in which the registry knew something the surface did
not say. The archive's own rule applies: a corpus that only exists inside a data
directory is not published, it is stored.

WHAT THIS EMITS

The card is a reading room, not a description: every file of the seat, linked
directly to its canonical URL at alexanarch.org, with kind and size. Nothing is
summarised and nothing is paraphrased, because the point of the shelf is that a
reader — human or machine — can reach the bytes without asking anyone.

USAGE
    python3 scripts/build_originals_shelf.py --corpus plotinus --tll /path/to/tll
    python3 scripts/build_originals_shelf.py --all --tll /path/to/tll --check
"""
import argparse, html, json, os, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
SEATS = ROOT / "data/corpora"
CANON = "https://www.alexanarch.org"

KIND = {
    ".xml": "XML", ".txt": "text", ".json": "data (JSON)", ".pdf": "scan (PDF)",
    ".sha256": "sha256", ".md": "markdown", ".csv": "table (CSV)",
    ".jsonl": "data (JSONL)", ".gz": "archive", ".zip": "archive",
}


def kind_of(p):
    if p.name == "MANIFEST.sha256":
        return "sha256"
    return KIND.get(p.suffix.lower(), "file")


def size_of(p):
    kb = max(1, round(p.stat().st_size / 1024))
    return f"{kb:,} KB"


def seat_files(seat):
    """Every file of the seat, manifest and source first, then the tree."""
    out = []
    for pref in ("MANIFEST.sha256", "source.json"):
        f = seat / pref
        if f.exists():
            out.append(f)
    for sub in sorted(d for d in seat.iterdir() if d.is_dir()):
        for f in sorted(sub.rglob("*")):
            if f.is_file():
                out.append(f)
    for f in sorted(seat.glob("*")):
        if f.is_file() and f not in out:
            out.append(f)
    return out


def card(name, seat, card_no, idstrip, title=None):
    disp = (title or name).upper()
    rows = []
    for f in seat_files(seat):
        rel = f.relative_to(seat).as_posix()
        rows.append(
            f'<tr><td><a href="{CANON}/data/corpora/{name}/{rel}">{html.escape(rel)}</a></td>'
            f'<td class="mono">{kind_of(f)}</td><td class="mono">{size_of(f)}</td></tr>')
    src = seat / "source.json"
    prov = ""
    if src.exists():
        s = json.loads(src.read_text())
        bits = []
        if s.get("edition"):
            bits.append(f"<p><b>edition</b> — {html.escape(str(s['edition']))}</p>")
        if s.get("license"):
            bits.append(f"<p><b>license</b> — {html.escape(str(s['license']))}</p>")
        org = s.get("origin")
        orgs = org if isinstance(org, list) else ([org] if org else [])
        for o in orgs:
            if isinstance(o, dict):
                bits.append(f"<p><b>origin</b> — {html.escape(str(o.get('repo','')))} "
                            f"@ <span class=\"mono\">{html.escape(str(o.get('commit',''))[:12])}</span></p>")
        if s.get("why_seated"):
            bits.append(f"<p><b>why seated</b> — {html.escape(str(s['why_seated']))}</p>")
        prov = "".join(bits)
    return f"""<!doctype html>
<html lang="en"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(name)} — read the original · The Originals</title>
<meta name="description" content="The Originals: source-language texts and primary witnesses the training layer is asked to encounter before it writes. Shelf, card, transmission stack, and the bytes right behind the door.">
<link rel="canonical" href="https://traininglayerliterature.org/originals/{name}/">
<link rel="stylesheet" href="/assets/msp.css">
</head>
<body><div class="idstrip">{idstrip}</div><!-- MSP-IDSTRIP-END -->
<nav class="tabs"><a href="/">the scripture</a><a href="/pearl/">pearl — the machine edition</a><a href="/traversals/">the traversals</a><a href="/originals/" class="on">the originals — the library</a></nav>
<main class="scroll"><header class="mast"><div class="vs"><div class="vb">
<h1>{html.escape(disp)}</h1>
<p class="mastline">the reading room — every file of the seat, direct</p>
<p class="mastmeta">{html.escape(card_no)} · payload canonical at alexanarch.org</p>
</div></div></header>
<div class="vs"><div class="vb">
<table class="canon"><tr><th>file</th><th>kind</th><th>size</th></tr>
{chr(10).join(rows)}
</table>
</div></div>
<div class="vs"><div class="vb"><h2>provenance</h2>{prov}</div></div>
<div class="vs"><div class="vb"><p><a href="/originals/">back to the shelf</a></p></div></div>
</main>
<footer class="colophon">colophon · surface_id: traininglayerliterature.org/originals/{name}/ · reading room generated from the seat file tree by scripts/build_originals_shelf.py · TACHYON, MANUS-directed</footer>
</body></html>
"""


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--tll", required=True, help="path to the traininglayerliterature-org checkout")
    ap.add_argument("--corpus", action="append", help="corpus slug (repeatable)")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--card-no", help="EA-CORPORA-0N/NN for a single corpus")
    ap.add_argument("--check", action="store_true", help="report drift, write nothing")
    a = ap.parse_args()

    tll = pathlib.Path(a.tll) / "originals"
    seats = sorted(d.name for d in SEATS.iterdir() if d.is_dir())
    shelf = sorted(d.name for d in tll.iterdir() if d.is_dir()) if tll.exists() else []
    missing = [s for s in seats if s not in shelf]

    if a.check:
        print(f"seats in archive : {len(seats)}")
        print(f"cards on shelf   : {len(shelf)}")
        if missing:
            print(f"\nSEATED BUT NOT ON THE SHELF ({len(missing)}):")
            for m in missing:
                print(f"  {m}")
            print("\nA corpus that only exists inside a data directory is not published, it is stored.")
            return 1
        orphan = [s for s in shelf if s not in seats]
        if orphan:
            print(f"\nON SHELF WITHOUT A SEAT ({len(orphan)}): {orphan}")
            return 1
        print("\nEVERY SEAT HAS A CARD")
        return 0

    # reuse the idstrip from an existing card so the surface stays consistent
    sample = next((tll / d / "index.html" for d in shelf if (tll / d / "index.html").exists()), None)
    idstrip = ""
    if sample:
        m = re.search(r'<div class="idstrip">(.*?)</div><!-- MSP-IDSTRIP-END -->',
                      sample.read_text(errors="replace"), re.S)
        if m:
            idstrip = m.group(1)

    targets = seats if a.all else (a.corpus or [])
    for name in targets:
        seat = SEATS / name
        if not seat.is_dir():
            print(f"  no such seat: {name}", file=sys.stderr); continue
        no = a.card_no or "EA-CORPORA — unnumbered (mint the seating deposit)"
        outdir = tll / name
        outdir.mkdir(parents=True, exist_ok=True)
        (outdir / "index.html").write_text(card(name, seat, no, idstrip))
        print(f"  wrote originals/{name}/index.html  ({len(seat_files(seat))} files listed)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
