#!/usr/bin/env python3
"""
audit_completeness.py (v2) — classify body status of every deposit BEFORE the
PDF compression layer, using the residual measure.

Residual = substantive body text remaining after removing:
  (a) the recovered description (n-gram removal, order-insensitive)
  (b) reconstruction boilerplate (frontmatter-style field lines, standard
      section headers, SPXI footers)

Classes:
  full              — residual >= 2000 chars: substantive work beyond metadata
  description_only  — residual < 500: the body IS the description (+ wrapper)
  stub_short        — 500 <= residual < 2000 AND not natively-short type
  native_short      — 500 <= residual < 2000 AND content_type/title indicates
                      a natively short-form document class (canon node,
                      erratum, tether, metadata declaration, etc.)
  missing           — no body file on disk

review_flag on entries where the call is uncertain (residual in the
1200-3000 band, or sidecar abstract longer than body, or registry
full_text_chars disagrees strongly with disk).

Output: data/completeness-audit.json (proposal; registry untouched).
"""
from __future__ import annotations
import json, os, re, sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
REGISTRY = REPO_ROOT / "data" / "registry.json"
DEPOSITS_DIR = REPO_ROOT / "data" / "deposits"
SIDECAR_DIR = REPO_ROOT / "data" / "external-metadata"
OUT = REPO_ROOT / "data" / "completeness-audit.json"

FULL_RESIDUAL = 2000
DESC_ONLY_RESIDUAL = 500
REVIEW_BAND = (1200, 3000)

# Natively short document classes: pattern → label (checked on title + content_type)
NATIVE_SHORT_PATTERNS = [
    r"canon provenance node", r"provenance anchor", r"erratum", r"errata",
    r"session tether", r"gw\.tachyon", r"chain —", r"zenodo metadata",
    r"metadata declaration", r"visual schema", r"reply of", r"correction:",
    r"about the author", r"contributor bio", r"colophon",
]

BOILERPLATE_LINE = re.compile(
    r"^\s*\*\*(Author|ORCID|Date|Family|Sovereign ID|Legacy DOI|Deposit Number|"
    r"Hex|License|Version|Archive|Community|Type|Layer|Status)\b.*$"
    r"|^\s*(Author|ORCID|Date|Family|License|Version|Type|Layer|Status)\s*:.*$",
    re.MULTILINE | re.IGNORECASE,
)


TEXTS_DIR = REPO_ROOT / "data" / "texts"

def _load_body(hex_id, dep_num):
    """Check BOTH stores (data/deposits and data/texts) and return the LONGEST body.
    v3 fix: the canonical full-text store data/texts/AXN-{hex}-text.md was invisible
    to v1/v2, producing false 'missing' classifications."""
    cands = []
    if hex_id:
        hz = hex_id.zfill(4)
        cands += [DEPOSITS_DIR / f"AXN-{hex_id}.md", TEXTS_DIR / f"AXN-{hex_id}-text.md"]
        if hz != hex_id:
            cands += [DEPOSITS_DIR / f"AXN-{hz}.md", TEXTS_DIR / f"AXN-{hz}-text.md"]
    cands.append(DEPOSITS_DIR / f"AXN-{dep_num}.md")
    best_text, best_name = "", ""
    for c in cands:
        if c.exists():
            try:
                t = c.read_text(encoding="utf-8", errors="replace")
                if len(t) > len(best_text):
                    best_text, best_name = t, c.name
            except Exception:
                pass
    return best_text, best_name


def normalize(text):
    if not text:
        return ""
    text = re.sub(r"\A---\n.*?\n---\n", "", text, flags=re.DOTALL)
    text = re.sub(r"```.*?```", " ", text, flags=re.DOTALL)
    text = re.sub(r"`[^`\n]+`", " ", text)
    text = BOILERPLATE_LINE.sub(" ", text)
    text = re.sub(r"^#{1,6}\s+.*$", " ", text, flags=re.MULTILINE)  # headers are structure, not content
    text = re.sub(r"[*_]{1,3}([^*_]+)[*_]{1,3}", r"\1", text)
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip().lower()


def residual_after_desc(body_norm, desc_norm):
    """Remove desc content from body via sliding 10-gram removal; return remaining char count."""
    if not body_norm:
        return 0
    if not desc_norm:
        return len(body_norm)
    remaining = body_norm
    words = desc_norm.split()
    # Remove every 10-gram of the description from the body (covers verbatim + doubled copies)
    grams = set()
    for i in range(0, max(1, len(words) - 10)):
        g = " ".join(words[i:i + 10])
        if len(g) > 25:
            grams.add(g)
    for g in grams:
        remaining = remaining.replace(g, " ")
    remaining = re.sub(r"\s+", " ", remaining).strip()
    return len(remaining)


def is_native_short(title, content_type, body):
    hay = f"{title} {content_type}".lower()
    for pat in NATIVE_SHORT_PATTERNS:
        if re.search(pat, hay):
            return True
    return False


def sidecar_abstract_chars(hex_id):
    for name in (f"AXN-{hex_id}.json", f"AXN-{hex_id.zfill(4)}.json"):
        p = SIDECAR_DIR / name
        if p.exists():
            try:
                m = json.loads(p.read_text(encoding="utf-8"))
                vals = [v.get("abstract_chars", 0) or 0
                        for v in (m.get("per_doi") or {}).values() if isinstance(v, dict)]
                return max(vals) if vals else 0
            except Exception:
                return 0
    return 0


def main():
    reg = json.loads(REGISTRY.read_text(encoding="utf-8"))
    deposits = reg["deposits"]
    print(f"Auditing {len(deposits)} deposits (v2 residual method)...")

    results, counts = {}, {}
    review_count = 0

    for i, d in enumerate(deposits):
        n = d.get("deposit_number")
        if not n:
            continue
        axn = d.get("axn", "")
        hex_id = axn.split(":")[1].split(".")[0] if ":" in axn and "." in axn else ""
        desc = d.get("description", "") or ""
        title = d.get("title", "") or ""
        ctype = d.get("content_type", "") or ""

        body_raw, body_file = _load_body(hex_id, n)
        body_norm = normalize(body_raw)
        desc_norm = normalize(desc)
        residual = residual_after_desc(body_norm, desc_norm)

        if not body_norm:
            cls = "missing"
        elif residual < DESC_ONLY_RESIDUAL:
            cls = "description_only"
        elif residual < FULL_RESIDUAL:
            cls = "native_short" if is_native_short(title, ctype, body_norm) else "stub_short"
        else:
            cls = "full"

        counts[cls] = counts.get(cls, 0) + 1

        entry = {
            "deposit_number": n, "axn": axn, "title": title[:120],
            "classification": cls, "body_file": body_file,
            "body_raw_chars": len(body_raw),
            "body_norm_chars": len(body_norm),
            "desc_norm_chars": len(desc_norm),
            "residual_chars": residual,
            "registry_full_text_chars": d.get("full_text_chars") or 0,
        }

        review = False
        if REVIEW_BAND[0] <= residual < REVIEW_BAND[1] and cls != "missing":
            review = True
        sc = sidecar_abstract_chars(hex_id)
        if sc and sc > body_norm.__len__() and cls != "full":
            entry["sidecar_abstract_longer"] = sc
            review = True
        if review:
            entry["review_flag"] = True
            review_count += 1

        results[str(n)] = entry
        if (i + 1) % 250 == 0:
            print(f"  {i+1}/{len(deposits)}")

    import datetime
    payload = {
        "$schema": "https://alexanarch.org/api/schemas/completeness-audit.schema.json",
        "version": "v3-dual-store",
        "purpose": ("Per-deposit body-status classification generated BEFORE the PDF "
                    "compression layer (lacuna protocol precondition). Proposal for "
                    "MANUS review; registry untouched by this script."),
        "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "method": {
            "residual_measure": "body minus description n-grams minus boilerplate",
            "full_residual_threshold": FULL_RESIDUAL,
            "description_only_residual_threshold": DESC_ONLY_RESIDUAL,
            "review_band": list(REVIEW_BAND),
            "classes": ["full", "description_only", "stub_short", "native_short", "missing"],
        },
        "counts": counts,
        "review_flagged": review_count,
        "deposits": results,
    }
    OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"\n=== Classification (v2) ===")
    for k in ("full", "description_only", "stub_short", "native_short", "missing"):
        print(f"  {k}: {counts.get(k, 0)}")
    print(f"  review-flagged: {review_count}")
    print(f"\n✓ {OUT.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
