#!/usr/bin/env python3
"""repair_scholar_meta.py — bring every record page's Google Scholar tags to the renderer's current form, in place.

Scholar's inclusion guidelines (read 2026-11-10): "Put each author name in a separate tag and omit all affiliations,
degrees, certifications, etc., from this field", and citation_pdf_url "must refer to a file in the same subdirectory
as the HTML abstract". The record pages carried the creator string whole in one citation_author tag, and pointed
citation_pdf_url and the PDF button at /papers/AXN-<hex>.pdf, outside the record's folder /s/records/<n>/. The renderer
(wire_deposit.py) now writes one tag per author (scholar_authors) and the PDF at /s/records/<n>/AXN-<hex>.pdf, which a
vercel.json rewrite serves from /papers/. This repairs the pages already rendered, touching only those three things,
so no other layer of a page (banners, retirement apparatus, injected scripts) moves. Idempotent; prints what changed.

    python3 scripts/repair_scholar_meta.py [--check]"""
import html, json, pathlib, re, sys
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "scripts"))
import wire_deposit as W

AUTH = re.compile(r'(?:<meta name="citation_author" content="[^"]*">\n?)+')
PDF = re.compile(r'<meta name="citation_pdf_url" content="https://www\.alexanarch\.org/papers/(AXN-[0-9A-Fa-f]{4}\.pdf)">')
BTN = re.compile(r'href="/papers/(AXN-[0-9A-Fa-f]{4}\.pdf)">↓ PDF</a>')


def main(check=False):
    reg = {d["deposit_number"]: d for d in json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8"))["deposits"]}
    changed = 0
    for n, d in sorted(reg.items()):
        p = ROOT / f"s/records/{n}/index.html"
        if not p.exists():
            continue
        s = p.read_text(encoding="utf-8")
        t = s
        names = W.scholar_authors(d.get("creator"))
        tags = "".join(f'<meta name="citation_author" content="{W.esc(a) if hasattr(W, "esc") else html.escape(a, quote=True)}">\n' for a in names)
        m = AUTH.search(t)
        if m and m.group(0) != tags:
            t = t[:m.start()] + tags + t[m.end():]
        t = PDF.sub(lambda m: f'<meta name="citation_pdf_url" content="https://www.alexanarch.org/s/records/{n}/{m.group(1)}">', t)
        t = BTN.sub(lambda m: f'href="/s/records/{n}/{m.group(1)}">↓ PDF</a>', t)
        if t != s:
            changed += 1
            if not check:
                p.write_text(t, encoding="utf-8")
    print(f"record pages {'to change' if check else 'changed'}: {changed}")
    return 0


if __name__ == "__main__":
    sys.exit(main("--check" in sys.argv))
