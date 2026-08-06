#!/usr/bin/env python3
"""
build_body_index.py — build /api/body-index.json, an inverted index over the
body text of every deposit.

Task 1 of EA-RETRIEVAL-DENSITY-01. Complements /api/search-index.json (which
tokenizes metadata only: title, description, creator, content_type, keywords,
axn, hex). This index tokenizes the full body of each deposit's source md.

Tokenization matches the primary index for consistency:
  - regex \\w-style extraction: [a-zA-Z0-9]{3,}
  - case-folded
  - stopwords stripped (same set as primary)
  - series prefixes captured with structure preserved

Additionally, distinctive multi-word capitalized noun phrases (2-4 consecutive
capitalized words) are extracted as keyword_phrases, since body text carries
many named entities the metadata does not.

Output at /api/body-index.json. Size estimate ~5-15 MB depending on corpus.
Design intent: additive, does not alter /api/search-index.json semantics.

Callers:
  - Direct fetch by AI systems and any code wanting deep phrase-in-body search.
  - The archive's /search/ page can optionally extend to also query this index
    (follow-on task, not part of build).
"""
from __future__ import annotations

import json
import re
import sys
import argparse
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
REGISTRY_PATH = REPO_ROOT / "data" / "registry.json"
DEPOSITS_DIR = REPO_ROOT / "data" / "deposits"
OUTPUT_PATH = REPO_ROOT / "data" / "api" / "body-index.json"

# Reuse the primary index's tokenization discipline verbatim
_STOPWORDS = frozenset({
    "a", "an", "the", "and", "or", "of", "in", "on", "at", "to", "for",
    "with", "by", "from", "as", "is", "are", "was", "were", "be", "been",
    "being", "has", "have", "had", "it", "its", "this", "that", "these",
    "those", "which", "who", "whom", "whose", "what", "when", "where",
    "why", "how", "not", "no", "so", "if", "than", "then", "into", "out",
    "via", "per", "over", "vs",
})

_SERIES_PATTERNS = [
    (re.compile(r"\bgw\.tachyon(?:\.[a-z]+)?", re.IGNORECASE), True),
    (re.compile(r"\bgw\.[a-z]+(?:\.[a-z]+)?", re.IGNORECASE), True),
    (re.compile(r"\bEA-[A-Z0-9]+(?:-[A-Z0-9]+)*"), False),
    (re.compile(r"\bMPAI(?:-[A-Z0-9]+)*"), False),
    (re.compile(r"\bOCTANG(?:-\d+)?"), False),
    (re.compile(r"\bPVE-\d+"), False),
    (re.compile(r"\bEB-\d+"), False),
    (re.compile(r"\bSPXI(?:-[A-Z0-9]+)*"), False),
    (re.compile(r"\bCHA(?:-[A-Z0-9-]+)?"), False),
    (re.compile(r"\bNEGSHAPE(?:-\d+)?"), False),
    (re.compile(r"\bAXN:[0-9A-F]{3,4}", re.IGNORECASE), False),
]

# Capitalized multi-word noun phrases: 2-4 consecutive capitalized words,
# excluding sentence-starts (heuristic: preceded by a period or line-start
# with next word capitalized is dropped later via frequency thresholds).
_CAP_PHRASE = re.compile(r"\b([A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+){1,3})\b")

# Skip markdown fenced code blocks and inline code — that content is machine-
# generated (code, JSON, YAML) and its tokens are noise, not body.
_FENCED = re.compile(r"```.*?```", re.DOTALL)
_INLINE_CODE = re.compile(r"`[^`\n]+`")
# Strip HTML comments and raw HTML blocks (some deposits embed HTML)
_HTML_COMMENT = re.compile(r"<!--.*?-->", re.DOTALL)
_HTML_TAG = re.compile(r"<[^>]+>")


def _strip_markdown(text: str) -> str:
    """Remove content that shouldn't be tokenized as body."""
    text = _FENCED.sub(" ", text)
    text = _INLINE_CODE.sub(" ", text)
    text = _HTML_COMMENT.sub(" ", text)
    text = _HTML_TAG.sub(" ", text)
    return text


def _tokenize(text: str) -> list[str]:
    """Extract case-folded generic tokens, ≥3 chars, stopwords removed.
    Matches primary search-index tokenization exactly."""
    if not text:
        return []
    words = re.findall(r"[a-zA-Z0-9]{3,}", text.lower())
    return [w for w in words if w not in _STOPWORDS]


def _extract_series(text: str) -> list[str]:
    if not text:
        return []
    out = []
    for cre, fold in _SERIES_PATTERNS:
        for m in cre.findall(text):
            if isinstance(m, tuple):
                m = m[0] if m else ""
            if m:
                out.append(m.lower() if fold else m)
    return out


def _extract_capitalized_phrases(text: str) -> list[str]:
    """Extract 2-4-word capitalized noun phrases, case-preserved.

    Filters common false positives (sentence-initial single caps get folded
    into 2-word phrases occasionally; we accept some noise here — the
    frequency-threshold in the roll-up drops singletons that only appear once
    across the corpus, which culls most noise)."""
    if not text:
        return []
    matches = _CAP_PHRASE.findall(text)
    # Skip phrases that are all short function-words after lowering (unlikely
    # but possible). No stopword filtering on phrases — they're multi-word
    # units, distinctiveness is preserved.
    return [m.strip() for m in matches if m.strip()]


TEXTS_DIR = REPO_ROOT / "data" / "texts"

def _load_body(hex_id: str, dep_num: int, ftp: str | None = None) -> tuple[str, str]:
    """Return (body_text, path_used) from the LONGEST body across BOTH stores.

    v2 fix (2026-07-17): data/texts/AXN-{hex}-text.md is the canonical
    full-text store (registry full_text_path); data/deposits/AXN-{hex}.md is
    the wire_deposit store. Reading only deposits/ under-indexed the corpus
    (104 deposits appeared body-less). Longest-wins across both stores."""
    candidates = []
    if hex_id:
        hz = hex_id.zfill(4)
        candidates += [DEPOSITS_DIR / f"AXN-{hex_id}.md", TEXTS_DIR / f"AXN-{hex_id}-text.md"]
        if hz != hex_id:
            candidates += [DEPOSITS_DIR / f"AXN-{hz}.md", TEXTS_DIR / f"AXN-{hz}-text.md"]
        if hex_id != hex_id.upper():
            candidates.append(DEPOSITS_DIR / f"AXN-{hex_id.upper()}.md")
    candidates.append(DEPOSITS_DIR / f"AXN-{dep_num}.md")
    if ftp:  # registry full_text_path is authoritative; stored with leading slash = repo-relative.
        # Text formats only (binary pointers like PDFs fall back to the conventional stores),
        # capped at 2MB so index-scale data files cannot masquerade as bodies.
        _p = REPO_ROOT / ftp.lstrip('/')
        if _p.suffix.lower() in ('.md', '.txt', '.json') and _p.exists() and _p.stat().st_size < 2_000_000:
            candidates.append(_p)

    best_text, best_path = "", ""
    for candidate in candidates:
        if candidate.exists():
            try:
                t = candidate.read_text(encoding="utf-8", errors="replace")
                if len(t) > len(best_text):
                    best_text = t
                    best_path = str(candidate.relative_to(REPO_ROOT))
            except (OSError, UnicodeDecodeError):
                pass
    return best_text, best_path


def build(dry_run: bool = False, min_phrase_freq: int = 2) -> int:
    reg = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    deposits = reg.get("deposits", [])

    inverted: dict[str, set[int]] = {}
    series_ix: dict[str, set[int]] = {}
    phrase_ix: dict[str, set[int]] = {}

    body_bytes_total = 0
    body_found = 0
    body_missing: list[int] = []

    for d in deposits:
        n = d.get("deposit_number")
        if not n:
            continue
        # Extract hex from AXN string
        axn = d.get("axn", "") or ""
        hex_id = ""
        if axn.startswith("AXN:") and "." in axn:
            hex_id = axn.split(":")[1].split(".")[0]
        hex_id = hex_id or d.get("hex", "") or ""

        body_text, used_path = _load_body(hex_id, n, d.get('full_text_path'))
        if not body_text:
            body_missing.append(n)
            continue

        body_bytes_total += len(body_text)
        body_found += 1

        stripped = _strip_markdown(body_text)

        for tok in _tokenize(stripped):
            inverted.setdefault(tok, set()).add(n)
        for s in _extract_series(stripped):
            series_ix.setdefault(s, set()).add(n)
        for p in _extract_capitalized_phrases(stripped):
            phrase_ix.setdefault(p, set()).add(n)

    # Frequency-threshold phrases: drop phrases that appear in only 1 deposit's
    # body AND with just one occurrence (they're likely noise). But keep any
    # phrase that appears in 2+ deposits (real cross-corpus term) or that has
    # multiple occurrences within one deposit's body (real term for that work).
    # Simpler heuristic: keep phrases appearing in ≥ min_phrase_freq distinct
    # deposit sets OR containing a proper-name marker (all uppercase word).
    def phrase_kept(phrase: str, deps: set[int]) -> bool:
        if len(deps) >= min_phrase_freq:
            return True
        # Retain single-deposit phrases that look genuinely proper — e.g. mixed
        # capitalization with 3+ words (likely a title or proper name).
        words = phrase.split()
        if len(words) >= 3:
            return True
        return False

    phrase_ix_filtered = {p: v for p, v in phrase_ix.items() if phrase_kept(p, v)}

    def to_sorted(d: dict) -> dict:
        return {k: sorted(v) for k, v in sorted(d.items())}

    output = {
        "$schema": "https://alexanarch.org/api/schemas/body-index.schema.json",
        "$id": "https://alexanarch.org/api/body-index.json",
        "index_version": "v1",
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "purpose": (
            "Inverted index over the BODY text of every deposit. Complements "
            "/api/search-index.json which tokenizes metadata only. Fetch once; "
            "look up any term as a key. For phrase search, intersect the deposit "
            "lists for each token."
        ),
        "companion_index": "/api/search-index.json",
        "total_deposits": len(deposits),
        "deposits_with_body": body_found,
        "deposits_missing_body": len(body_missing),
        "body_bytes_indexed": body_bytes_total,
        "tokenization": {
            "sources": ["body"],
            "min_length": 3,
            "case_folded": True,
            "stopwords_stripped": True,
            "series_prefixes_regex_captured": True,
            "capitalized_multiword_phrases_extracted": True,
            "min_phrase_deposit_frequency": min_phrase_freq,
            "phrase_length_range": [2, 4],
            "content_stripped_before_tokenization": [
                "markdown fenced code blocks (```...```)",
                "inline code (`...`)",
                "HTML comments and HTML tags",
            ],
        },
        "series_prefixes": to_sorted(series_ix),
        "keyword_phrases": to_sorted(phrase_ix_filtered),
        "index": to_sorted(inverted),
        "counts": {
            "generic_tokens": len(inverted),
            "series_prefix_terms": len(series_ix),
            "keyword_phrases_raw": len(phrase_ix),
            "keyword_phrases_kept": len(phrase_ix_filtered),
        },
    }

    payload = json.dumps(output, ensure_ascii=False, indent=2)
    if dry_run:
        print(f"[DRY] would write {OUTPUT_PATH} ({len(payload):,} bytes)")
    else:
        OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT_PATH.write_text(payload, encoding="utf-8")
        print(f"  ✓ api/body-index.json ({len(payload):,} bytes)")
        # --- Sharded postings for client-side body search (Canonical Record Convergence P0.3) ---
        # The monolith is ~39MB and cannot be client-fetched; /search/ fetches only the
        # 2-char-prefix shards for the query's tokens (median shard: tens of KB).
        import shutil as _sh
        shard_dir = OUTPUT_PATH.parent / "body-shards"
        if shard_dir.exists():
            _sh.rmtree(shard_dir)
        shard_dir.mkdir()
        tokens = output.get("index", {})
        shards = {}
        for tok, posts in tokens.items():
            pref = "".join(c for c in tok[:2].lower() if c.isalnum()) or "_"
            if len(pref) < 2: pref = (pref + "_")[:2]
            shards.setdefault(pref, {})[tok] = posts
        for pref, block in shards.items():
            (shard_dir / f"{pref}.json").write_text(
                json.dumps(block, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
        manifest = {"shard_count": len(shards), "prefix_length": 2,
                    "lookup": "lowercase token -> first two alphanumeric chars -> /api/body-shards/{prefix}.json",
                    "generated_at": output.get("generated_at")}
        (shard_dir / "manifest.json").write_text(json.dumps(manifest, indent=1), encoding="utf-8")
        print(f"  ✓ api/body-shards/ ({len(shards)} shards)")

    print(f"  deposits indexed: {body_found}/{len(deposits)}")
    if body_missing:
        print(f"  deposits missing body md: {len(body_missing)} — sample: {body_missing[:10]}")
    print(f"  generic body tokens:   {len(inverted):,}")
    print(f"  series prefix terms:   {len(series_ix):,}")
    print(f"  capitalized phrases:   {len(phrase_ix_filtered):,} kept of {len(phrase_ix):,} raw")
    print(f"  body bytes indexed:    {body_bytes_total:,}")

    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Build /api/body-index.json")
    ap.add_argument("--dry-run", action="store_true", help="Do not write output")
    ap.add_argument("--min-phrase-freq", type=int, default=2,
                    help="Minimum deposit-set size for a phrase to be kept (default 2)")
    args = ap.parse_args()
    return build(dry_run=args.dry_run, min_phrase_freq=args.min_phrase_freq)


if __name__ == "__main__":
    sys.exit(main())
