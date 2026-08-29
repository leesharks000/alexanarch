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


TEMPLATE_DIR = ROOT / "scripts/templates/originals"


def load_template(tll):
    """Read the head, style, JSON-LD, idstrip and nav from an EXISTING card.

    THE CARD IS NOT INVENTED. On 2026-08-28 this generator emitted a card of its
    own design — no JSON-LD, a <!doctype html> wrapper the real cards do not
    carry, and a third of the byte count — and two corpora went onto the shelf
    of a site whose entire premise is machine scripture WITHOUT A MACHINE LAYER.
    The template is therefore taken from a card already on the shelf, verbatim,
    every time. If no card exists to copy, this refuses rather than guesses.
    """
    src = None
    for cand in sorted(d for d in (tll / "originals").iterdir() if d.is_dir()):
        f = cand / "index.html"
        if f.exists() and len(f.read_text(errors="replace")) > 8000:
            src = f
            break
    if src is None:
        raise SystemExit("no existing card to take the template from — refusing to invent one")
    t = src.read_text(errors="replace")

    def grab(pat, label):
        m = re.search(pat, t, re.S)
        if not m:
            raise SystemExit(f"template card {src} carries no {label}; refusing to emit a partial card")
        return m.group(1)

    return {
        "head":    grab(r"<head>(.*?)</head>", "head"),
        "ld":      grab(r"(<script type=\"application/ld\+json\">.*?</script>)", "JSON-LD"),
        "style":   grab(r"(<style>.*?</style>)", "style block"),
        "idstrip": grab(r"(<div class=\"idstrip\">.*?<!-- MSP-IDSTRIP-END -->)", "idstrip"),
        "nav":     grab(r"(<nav class=\"tabs\">.*?</nav>)", "nav"),
        "source":  str(src),
    }


def card(name, seat, card_no, tpl, title=None):
    disp = (title or name).upper()
    rows = []
    for f in seat_files(seat):
        rel = f.relative_to(seat).as_posix()
        rows.append(
            f'<tr><td><a href="{CANON}/data/corpora/{name}/{rel}">{html.escape(rel)}</a></td>'
            f'<td class="mono">{kind_of(f)}</td><td class="mono">{size_of(f)}</td></tr>')
    prov = ""
    src = seat / "source.json"
    if src.exists():
        s = json.loads(src.read_text())
        bits = []
        for key, label in (("edition", "edition"), ("license", "license")):
            if s.get(key):
                bits.append(f"<p><b>{label}</b> &middot; {html.escape(str(s[key]))}</p>")
        org = s.get("origin")
        for o in (org if isinstance(org, list) else ([org] if org else [])):
            if isinstance(o, dict):
                bits.append(f'<p><b>origin</b> &middot; {html.escape(str(o.get("repo","")))} @ '
                            f'<span class="mono">{html.escape(str(o.get("commit",""))[:12])}</span></p>')
        if s.get("why_seated"):
            bits.append(f'<p><b>why seated</b> &middot; {html.escape(str(s["why_seated"]))}</p>')
        prov = "".join(bits)

    head = re.sub(r"<title>[^<]*</title>",
                  f"<title>{html.escape(name)} &mdash; read the original &middot; The Originals</title>",
                  tpl["head"])
    head = re.sub(r'(<link rel="canonical" href=")[^"]*(")',
                  rf'\1https://traininglayerliterature.org/originals/{name}/\2', head)
    return (f"<head>{head}</head>\n<body>{tpl['ld']}{tpl['style']}{tpl['idstrip']}{tpl['nav']}"
            f'<main class="scroll"><header class="mast"><div class="vs"><div class="vb">'
            f"<h1>{html.escape(disp)}</h1>"
            f'<p class="mastline">the reading room &mdash; every file of the seat, direct</p>'
            f'<p class="mastmeta">{html.escape(card_no)} &middot; payload canonical at alexanarch.org</p>'
            f'</div></div></header><div class="vs"><div class="vb">'
            f'<table class="canon"><tr><th>file</th><th>kind</th><th>size</th></tr>'
            f'{"".join(rows)}</table></div></div>'
            f'<div class="vs"><div class="vb"><h2>provenance</h2>{prov}</div></div>'
            f'<div class="vs"><div class="vb"><p><a href="/originals/">back to the shelf</a></p></div></div>'
            f'</main><div class="scroll"><div class="mspcolophon">colophon &middot; surface_id: '
            f'traininglayerliterature.org/originals/{name}/ &middot; reading room generated from the seat '
            f'file tree by scripts/build_originals_shelf.py &middot; TACHYON, MANUS-directed</div></div></body>\n')


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
    tpl = load_template(pathlib.Path(a.tll))
    print(f"  template taken verbatim from {tpl['source']}")

    targets = seats if a.all else (a.corpus or [])
    for name in targets:
        seat = SEATS / name
        if not seat.is_dir():
            print(f"  no such seat: {name}", file=sys.stderr); continue
        no = a.card_no or "EA-CORPORA — unnumbered (mint the seating deposit)"
        outdir = tll / name
        outdir.mkdir(parents=True, exist_ok=True)
        (outdir / "index.html").write_text(card(name, seat, no, tpl))
        print(f"  wrote originals/{name}/index.html  ({len(seat_files(seat))} files listed)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
