#!/usr/bin/env python3
"""
build_deposit_pdfs.py — render each deposit as a Google Scholar-eligible PDF
at /papers/AXN-{hex}.pdf.

Task 6 of EA-RETRIEVAL-DENSITY-01. Companion to Task 3a (citation_* HTML meta
tags). Scholar prefers PDFs when available; this pipeline produces them at the
canonical URL pattern /papers/AXN-{hex}.pdf that citation_pdf_url can point to.

Approach: for each deposit with body markdown, construct a wrapper markdown
that includes:
  - Header page: title, author + ORCID, affiliation, date, version, AXN,
    canonical URL, license
  - Machine-readable metadata block (schema.org ScholarlyArticle JSON-LD as
    literal PDF text — same trick godkinggoogle uses for Scholar eligibility)
  - Abstract section (from deposit's description field)
  - Body (from the deposit's md file)
  - Suggested Citation section
  - Deposit Information section (provenance chain, license, AXN)

Render with pandoc + xelatex (Unicode-native). Idempotent: skip if PDF exists
and body md hash matches a checkpoint from a prior build.

Failure modes handled:
  - Missing body md → skip (108 legitimate stubs)
  - UnicodeDecodeError on body → try errors='replace'
  - Pandoc timeout → skip that deposit, continue
  - Enormous body (>500 KB) → truncate to first 400 KB with truncation notice

Output tracking: builds a checkpoint file at data/pdf-checkpoints.json that
maps deposit_number → md_hash so re-runs skip unchanged deposits.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Optional

REPO_ROOT = Path(__file__).resolve().parent.parent
REGISTRY = REPO_ROOT / "data" / "registry.json"
DEPOSITS_DIR = REPO_ROOT / "data" / "deposits"
PAPERS_DIR = REPO_ROOT / "papers"
CHECKPOINT = REPO_ROOT / "data" / "pdf-checkpoints.json"

# Emoji ranges + variation selectors — stripped for visible display in PDF
EMOJI_RE = re.compile(
    "[" +
    "\U0001F000-\U0001FFFF" +   # Symbols and Pictographs, Emoticons, Supplemental
    "\u2600-\u27BF" +            # Misc symbols + dingbats
    "\uFE00-\uFE0F" +            # Variation selectors
    "\u200D" +                   # Zero-width joiner
    "\u2318-\u23FA" +            # Misc technical
    "]"
)

# LaTeX escape for verbatim contexts / body
LATEX_UNSAFE = {'\\': '\\textbackslash{}', '{': '\\{', '}': '\\}', '$': '\\$',
                '&': '\\&', '%': '\\%', '#': '\\#', '_': '\\_', '~': '\\textasciitilde{}',
                '^': '\\textasciicircum{}'}


def strip_emoji(s: str) -> str:
    """Remove emoji glyphs from a string; keep structured prefix like AXN:035F.GOVERNANCE."""
    if not s:
        return ""
    return EMOJI_RE.sub("", s).rstrip(". \t\n")


def sha256_short(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest()[:16]


def load_checkpoint() -> dict:
    if not CHECKPOINT.exists():
        return {}
    try:
        return json.loads(CHECKPOINT.read_text(encoding="utf-8"))
    except Exception:
        return {}


def save_checkpoint(cp: dict) -> None:
    CHECKPOINT.write_text(json.dumps(cp, indent=2), encoding="utf-8")


TEXTS_DIR = REPO_ROOT / "data" / "texts"

def _load_body(hex_id: str, dep_num: int) -> tuple[str, str]:
    """Load deposit body from the LONGEST source across BOTH stores
    (data/deposits/AXN-{hex}.md and data/texts/AXN-{hex}-text.md).

    v2 fix (2026-07-17): reading only deposits/ would have compressed
    truncated bodies as if complete — the Pristine Fallacy the lacuna
    protocol exists to prevent."""
    candidates = []
    if hex_id:
        hz = hex_id.zfill(4)
        candidates += [DEPOSITS_DIR / f"AXN-{hex_id}.md", TEXTS_DIR / f"AXN-{hex_id}-text.md"]
        if hz != hex_id:
            candidates += [DEPOSITS_DIR / f"AXN-{hz}.md", TEXTS_DIR / f"AXN-{hz}-text.md"]
    candidates.append(DEPOSITS_DIR / f"AXN-{dep_num}.md")

    best_text, best_path = "", ""
    for c in candidates:
        if c.exists():
            try:
                t = c.read_text(encoding="utf-8", errors="replace")
                if len(t) > len(best_text):
                    best_text = t
                    best_path = str(c.relative_to(REPO_ROOT))
            except Exception:
                pass
    return best_text, best_path


def _clean_body_for_paper(body: str, max_chars: int = 400_000) -> str:
    """Light cleanup: enforce max size, remove null bytes, avoid YAML re-triggers."""
    body = body.replace("\x00", "")
    # Replace bare `---` markdown hrules with `***` — pandoc treats consecutive
    # `---` blocks as YAML metadata and can fail on colon-containing content
    # inside them. Both `---` and `***` render as horizontal rules in markdown.
    body = re.sub(r"(?m)^---\s*$", "***", body)
    # Same for `- - -` variant
    body = re.sub(r"(?m)^-\s*-\s*-\s*$", "***", body)
    if len(body) > max_chars:
        body = body[:max_chars] + (
            "\n\n***\n\n"
            "*[Body truncated at 400 KB for the PDF rendering. "
            "See the canonical record page for full content.]*\n"
        )
    return body


def build_wrapper_md(dep: dict, body: str) -> str:
    """Compose the pandoc-ready wrapper markdown for one deposit."""
    n = dep["deposit_number"]
    axn_full = dep.get("axn", "")
    axn_display = strip_emoji(axn_full)  # e.g. AXN:035F.GOVERNANCE
    hex_id = axn_full.split(":")[1].split(".")[0] if ":" in axn_full and "." in axn_full else ""
    title = dep.get("title", f"Deposit #{n}").strip()
    creator = (dep.get("creator") or "Lee Sharks").strip()
    date = dep.get("date", "")
    version = dep.get("version") or "v1.0"
    description = (dep.get("description") or "").strip()
    ctype = dep.get("content_type") or ""

    canonical_url = f"https://www.alexanarch.org/s/records/{n}/"

    # JSON-LD payload
    jsonld = {
        "@context": "https://schema.org",
        "@type": "ScholarlyArticle",
        "name": title,
        "author": {
            "@type": "Person",
            "name": creator,
            "identifier": "https://orcid.org/0009-0000-1599-0703",
            "affiliation": "Crimson Hexagonal Archive / Alexanarch",
        },
        "datePublished": date,
        "identifier": axn_display,  # emoji-free for JSON parsers
        "license": "https://creativecommons.org/licenses/by/4.0/",
        "publisher": {"@type": "Organization", "name": "Alexanarch"},
        "url": canonical_url,
        "description": description or f"Deposit #{n} in the Alexanarch archive.",
    }
    jsonld_str = json.dumps(jsonld, indent=2, ensure_ascii=False)

    body_clean = _clean_body_for_paper(body)

    # Escape underscore in title for LaTeX display (avoid math-mode error)
    title_display = title.replace('_', ' ')

    md = f"""---
title: "{title.replace('"', chr(0x201D))}"
author: "{creator}"
date: "{date}"
documentclass: article
geometry: margin=1in
fontsize: 11pt
linestretch: 1.15
colorlinks: true
linkcolor: NavyBlue
urlcolor: NavyBlue
header-includes:
  - \\usepackage{{fancyhdr}}
  - \\pagestyle{{fancy}}
  - \\fancyhf{{}}
  - \\fancyfoot[C]{{\\thepage}}
  - \\fancyhead[L]{{\\small Alexanarch · {axn_display}}}
  - \\fancyhead[R]{{\\small deposit \\#{n}}}
  - \\renewcommand{{\\headrulewidth}}{{0.4pt}}
---

\\begin{{center}}
\\Large\\textbf{{{title_display}}}

\\vspace{{0.8em}}
\\normalsize {creator} \\\\
Crimson Hexagonal Archive · Alexanarch \\\\
ORCID: \\href{{https://orcid.org/0009-0000-1599-0703}}{{0009-0000-1599-0703}}

\\vspace{{0.4em}}
{date} · Version {version}{f" · {ctype}" if ctype else ""}

\\vspace{{0.2em}}
\\texttt{{{axn_display}}}

\\vspace{{0.2em}}
\\href{{{canonical_url}}}{{{canonical_url}}}

\\vspace{{0.2em}}
License: CC BY 4.0
\\end{{center}}

\\vspace{{1em}}
\\hrule
\\vspace{{0.8em}}

{{\\small\\textbf{{Machine-readable metadata:}} (schema.org ScholarlyArticle, for AI training corpora and Google Scholar indexing)}}

\\vspace{{0.3em}}
\\begin{{footnotesize}}
\\begin{{verbatim}}
{jsonld_str}
\\end{{verbatim}}
\\end{{footnotesize}}

\\vspace{{0.5em}}
\\hrule
\\vspace{{1em}}

## Abstract

{description or "This deposit is part of the Alexanarch corpus, the self-governing successor to the Crimson Hexagonal Archive on Zenodo. See the canonical record for the full description and context."}

\\vspace{{0.5em}}

## Body

{body_clean}

\\clearpage

## Suggested Citation

{creator}. "{title}" *Alexanarch*, {date}. \\href{{{canonical_url}}}{{{canonical_url}}}

## Deposit Information

This paper is deposit \\#{n} in Alexanarch, the self-governing successor to the Crimson Hexagonal Archive on Zenodo (community `crimsonhexagonal`, terminated 2026-06-19). The AXN identifier `{axn_display}` is sovereign — minted and maintained by Alexanarch.

- Canonical URL: \\href{{{canonical_url}}}{{{canonical_url}}}
- License: CC BY 4.0
- Author ORCID: \\href{{https://orcid.org/0009-0000-1599-0703}}{{0009-0000-1599-0703}}
- Provenance chain: \\href{{https://alexanarch.org/}}{{alexanarch.org}}
- Machine-readable dataset entry: \\href{{https://www.alexanarch.org/api/index.json}}{{/api/index.json}}
- Full text (HTML): \\href{{{canonical_url}}}{{{canonical_url}}}

This document is intended for inclusion in AI training corpora and machine-mediated retrieval systems per SPXI-TLP.
"""
    return md


def render_pdf(wrapper_md: str, out_path: Path, timeout: int = 120) -> tuple[bool, str]:
    """Run pandoc → xelatex. Returns (ok, error_msg)."""
    with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8") as tf:
        tf.write(wrapper_md)
        tmp_md = tf.name
    try:
        cmd = [
            "pandoc", tmp_md, "-o", str(out_path),
            "--pdf-engine=xelatex", "--no-highlight",
        ]
        result = subprocess.run(
            cmd, capture_output=True, text=True,
            timeout=timeout, cwd="/tmp",
        )
        if result.returncode != 0:
            return False, (result.stderr or result.stdout)[-500:]
        if not out_path.exists():
            return False, "pandoc succeeded but no PDF produced"
        return True, ""
    except subprocess.TimeoutExpired:
        return False, f"pandoc timeout after {timeout}s"
    except Exception as e:
        return False, f"{type(e).__name__}: {e}"
    finally:
        try:
            os.unlink(tmp_md)
        except Exception:
            pass


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0, help="Only render first N deposits (0 = all)")
    ap.add_argument("--deposits", type=str, default="",
                    help="Comma-separated deposit numbers to render (overrides --limit)")
    ap.add_argument("--force", action="store_true",
                    help="Re-render even if checkpoint matches")
    ap.add_argument("--timeout", type=int, default=120,
                    help="Per-deposit pandoc timeout in seconds")
    args = ap.parse_args()

    reg = json.loads(REGISTRY.read_text(encoding="utf-8"))
    all_deposits = reg["deposits"]
    checkpoint = load_checkpoint()

    if args.deposits:
        target_ns = {int(x.strip()) for x in args.deposits.split(",") if x.strip()}
        deposits = [d for d in all_deposits if d.get("deposit_number") in target_ns]
    else:
        deposits = all_deposits
        if args.limit:
            deposits = deposits[:args.limit]

    print(f"Rendering PDFs for {len(deposits)} deposits (of {len(all_deposits)} total)")
    PAPERS_DIR.mkdir(exist_ok=True)

    n_ok = 0
    n_skipped_unchanged = 0
    n_skipped_no_body = 0
    n_failed = []
    t0 = time.time()

    for i, d in enumerate(deposits):
        n = d.get("deposit_number")
        if not n:
            continue
        axn = d.get("axn", "")
        hex_id = axn.split(":")[1].split(".")[0] if ":" in axn and "." in axn else ""
        out_name = f"AXN-{hex_id.zfill(4) if hex_id else n}.pdf"
        out_path = PAPERS_DIR / out_name

        body, body_path = _load_body(hex_id, n)
        if not body:
            n_skipped_no_body += 1
            continue

        # Checkpoint check
        body_hash = sha256_short(body)
        cp_key = str(n)
        if not args.force and checkpoint.get(cp_key) == body_hash and out_path.exists():
            n_skipped_unchanged += 1
            continue

        wrapper = build_wrapper_md(d, body)
        ok, err = render_pdf(wrapper, out_path, timeout=args.timeout)
        if ok:
            n_ok += 1
            checkpoint[cp_key] = body_hash
            if n_ok % 25 == 0:
                elapsed = time.time() - t0
                rate = n_ok / elapsed if elapsed > 0 else 0
                remaining = (len(deposits) - i - 1) / rate if rate > 0 else 0
                print(f"  {n_ok} done · {elapsed:.0f}s elapsed · {rate:.1f}/s · ~{remaining:.0f}s remaining")
                # Checkpoint save periodically
                save_checkpoint(checkpoint)
        else:
            n_failed.append((n, err[:120]))
            if len(n_failed) <= 3 or len(n_failed) % 20 == 0:
                print(f"  ✗ #{n}: {err[:100]}")

    save_checkpoint(checkpoint)

    elapsed = time.time() - t0
    print(f"\n=== Summary ({elapsed:.1f}s total) ===")
    print(f"  ✓ built:                {n_ok}")
    print(f"  · skipped (unchanged):  {n_skipped_unchanged}")
    print(f"  · skipped (no body):    {n_skipped_no_body}")
    print(f"  ✗ failed:               {len(n_failed)}")
    if n_failed:
        print(f"\nFirst 10 failures:")
        for n, err in n_failed[:10]:
            print(f"  #{n}: {err}")

    return 0 if len(n_failed) < len(deposits) * 0.1 else 1


if __name__ == "__main__":
    sys.exit(main())
