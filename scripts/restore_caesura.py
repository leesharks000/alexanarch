#!/usr/bin/env python3
"""restore_caesura.py — restore the three Caesura documents from their blog originals.

WHY
The three records were seated at roughly 55-65% of their sources: #630 held 32 of 57
sentences, #629 held 10 of 24, #628 held 28 of 49. Whole sections were absent,
including the passage #630 is a reading OF. A record that carries two thirds of a
work and declares class=full is not a partial restoration; it is a complete-looking
one, which is worse, because nothing on its face says to go and check.

The blog is the authorial surface these documents name as their own publication
venue, and it carries structure the earlier restoration flattened away: headings,
definition tables, ordered procedures, code blocks.

Usage:
    python3 scripts/restore_caesura.py --dry-run
    python3 scripts/restore_caesura.py --apply
"""
import argparse, html, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]

SOURCES = {
    630: ("render-unto-caesar-hermeneutic-of",
          "https://mindcontrolpoems.blogspot.com/2026/04/render-unto-caesar-hermeneutic-of.html"),
    629: ("fc-caesura-protocol-sovereignty-audit",
          "https://mindcontrolpoems.blogspot.com/2026/04/fc-caesura-protocol-sovereignty-audit.html"),
    628: ("integrity-lock-caesura-fulfillment-pair",
          "https://mindcontrolpoems.blogspot.com/2026/04/integrity-lock-caesura-fulfillment-pair.html"),
}


def inline(s):
    """Inline markup, innermost first, so nesting survives."""
    s = re.sub(r"<code>(.*?)</code>", r"`\1`", s, flags=re.S)
    s = re.sub(r"<(?:strong|b)>(.*?)</(?:strong|b)>", r"**\1**", s, flags=re.S)
    s = re.sub(r"<(?:em|i)>(.*?)</(?:em|i)>", r"*\1*", s, flags=re.S)
    s = re.sub(r"<a [^>]*href=\"([^\"]+)\"[^>]*>(.*?)</a>", r"[\2](\1)", s, flags=re.S)
    s = re.sub(r"<br\s*/?>", "\n", s)
    s = re.sub(r"<[^>]+>", "", s)
    return html.unescape(s).strip()


def convert(body_html):
    out = []
    # walk block elements in document order so nothing is dropped or reordered
    pattern = re.compile(
        r"<(h1|h2|h3|h4|p|pre|table|ul|ol|hr)\b[^>]*>(.*?)</\1>|<hr\s*/?>",
        re.S | re.I)
    for m in pattern.finditer(body_html):
        tag = (m.group(1) or "hr").lower()
        inner = m.group(2) or ""
        if tag == "hr":
            out.append("---")
        elif tag in ("h1", "h2", "h3", "h4"):
            lvl = {"h1": "#", "h2": "##", "h3": "###", "h4": "####"}[tag]
            t = inline(inner)
            if t:
                out.append(f"{lvl} {t}")
        elif tag == "p":
            t = inline(inner)
            if t and t != "\xa0":
                out.append(t)
        elif tag == "pre":
            t = html.unescape(re.sub(r"<[^>]+>", "", inner)).strip("\n")
            out.append("```\n" + t + "\n```")
        elif tag in ("ul", "ol"):
            items = re.findall(r"<li\b[^>]*>(.*?)</li>", inner, re.S)
            for i, it in enumerate(items, 1):
                bullet = f"{i}." if tag == "ol" else "-"
                t = inline(it)
                if t:
                    out.append(f"{bullet} {t}")
        elif tag == "table":
            rows = re.findall(r"<tr\b[^>]*>(.*?)</tr>", inner, re.S)
            md = []
            for ri, row in enumerate(rows):
                cells = re.findall(r"<t[hd]\b[^>]*>(.*?)</t[hd]>", row, re.S)
                cells = [inline(c).replace("|", "\\|").replace("\n", " ") for c in cells]
                if not cells:
                    continue
                md.append("| " + " | ".join(cells) + " |")
                if ri == 0:
                    md.append("|" + "|".join(["---"] * len(cells)) + "|")
            if md:
                out.append("\n".join(md))
    # collapse the runs of rules the blog uses as section spacers
    text = "\n\n".join(out)
    text = re.sub(r"(\n\n---){2,}", "\n\n---", text)
    return re.sub(r"\n{3,}", "\n\n", text).strip() + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    if not (a.apply or a.dry_run):
        a.dry_run = True

    import json
    reg_p = ROOT / "data/registry.json"
    reg = json.loads(reg_p.read_text())
    D = {d["deposit_number"]: d for d in reg["deposits"]}

    for n, (slug, url) in SOURCES.items():
        raw = pathlib.Path(f"/tmp/{slug}.html").read_text(errors="replace")
        b = re.search(r"<div class=['\"]post-body[^>]*>(.*?)</div>\s*<div class=['\"]post-footer",
                      raw, re.S)
        if not b:
            print(f"  #{n}: post-body not found", file=sys.stderr)
            continue
        md = convert(b.group(1))
        d = D[n]
        cur = (ROOT / d["full_text_path"].lstrip("/")).read_text(errors="replace")
        cur_body = re.sub(r"^---.*?^---", "", cur, flags=re.S | re.M)

        flat = re.sub(r"\s+", " ", re.sub(r"[#*`|-]", "", md)).lower()
        sents = [s.strip() for s in re.split(r"(?<=[.!?])\s+",
                 re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", b.group(1)))))
                 if len(s.split()) >= 6]
        covered = sum(1 for s in sents if s[:60].lower() in flat)
        print(f"  #{n} {slug[:34]:<36} {len(cur_body):>6,}c -> {len(md):>6,}c · "
              f"{covered}/{len(sents)} source sentences present")
        if a.apply:
            (ROOT / d["full_text_path"].lstrip("/")).write_text(md)
    if a.dry_run:
        print("\n(dry run — nothing written)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
