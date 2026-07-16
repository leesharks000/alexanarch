#!/usr/bin/env python3
"""
scripts/build_semantic_addresses.py

Reference implementation of the Semantic Addresses framework
(EA-SEMANTIC-ADDRESSES-01 v1.0). Produces the canonical
data/semantic-addresses.json from six tributary sources.

Determinism guarantee: given the same tributary file contents at the
same commit SHA, this regenerator produces byte-identical output (modulo
the regenerated_at timestamp field, which is set to the argument
--pinned-timestamp if provided for hash-reproducible builds).

Framework spec: specs/EA-SEMANTIC-ADDRESSES-01.md
Machine schema: data/semantic-addresses.schema.json

Usage:
    python3 scripts/build_semantic_addresses.py                # normal run
    python3 scripts/build_semantic_addresses.py --dry-run      # no write
    python3 scripts/build_semantic_addresses.py --verify       # rebuild
                                                                # and diff
                                                                # against
                                                                # existing
"""

from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import os
import re
import sys
from collections import defaultdict
from typing import Dict, List, Tuple

# --------------------------------------------------------------------------- #
# Configuration
# --------------------------------------------------------------------------- #

FRAMEWORK_VERSION = "1.1"
REGENERATOR_PATH = "scripts/build_semantic_addresses.py"

# Observation tributaries — produce actual observation events
OBSERVATION_TRIBUTARIES = {
    "mm-main-capture": {
        "path": "data/EA-WG-CAPTURES-01.json",
        "description": "AI Overview / AI Mode Capture Registry",
        "extractor": "extract_main_capture",
    },
    "mm-rf-reception": {
        "path": "data/trackers/mm-revfirst-registry.json",
        "description": "Revelation First Reception Registry",
        "extractor": "extract_rf_reception",
    },
}

# Subjunctive tributaries — catalogue candidate addresses without observation events
SUBJUNCTIVE_TRIBUTARIES = {
    "mm-termindex": {
        "path": "data/trackers/mm-termindex.json",
        "description": "Archive term index — subjunctive-source (catalogued terms)",
        "extractor": "extract_termindex",
    },
    "mm-mint": {
        "path": "data/trackers/mm-mint.json",
        "description": "Sémantique Potentielle — subjunctive-source (minted families)",
        "extractor": "extract_mint",
    },
}

# Positive statuses → observed_address; negative → verified_non_address
# Status classification uses prefix normalization: "ADOPTION (dual-lineage)"
# → normalizes to "ADOPTION" for classification. Variants preserved in raw form
# on the observation record for downstream fine-grained filtering.
POSITIVE_PREFIXES = (
    "EXACT_MATCH", "EXACT MATCH",
    "BROAD_MATCH", "BROAD MATCH",
    "ADOPTION",              # covers "ADOPTION (dual-lineage)", etc.
    "WOUND_GAUGE", "WOUND GAUGE",
    "FAIR_TREATMENT", "FAIR TREATMENT",
    "PARTIAL",               # partial reception is still reception
    "DEMAND SIGNAL",
    "MANTLE CONSOLIDATION",
    "FUNCTIONAL ADDRESS",
)
NEGATIVE_PREFIXES = (
    "ZERO_RESULT", "ZERO RESULT",
    "ZERO_INDEX", "ZERO INDEX",
    "BASIN_MISS", "BASIN MISS",
    "DISPLACEMENT",
    "DISSOLUTION",
    "CORRECTION",            # AI corrected the query rather than answering
)

def _status_class(status: str) -> str:
    """Return 'positive' | 'negative' | 'unrated'."""
    if not status:
        return "unrated"
    s = status.upper().strip()
    for p in POSITIVE_PREFIXES:
        if s.startswith(p.upper()):
            return "positive"
    for p in NEGATIVE_PREFIXES:
        if s.startswith(p.upper()):
            return "negative"
    return "unrated"

GALLERIES = [
    "https://godkinggoogle.vercel.app/captures",
    "https://leesharks.com/captures",
]


# --------------------------------------------------------------------------- #
# Canonicalization (framework §3.1)
# --------------------------------------------------------------------------- #

_WHITESPACE = re.compile(r"\s+")
_CURLY_QUOTES = str.maketrans({
    "\u201C": '"', "\u201D": '"', "\u2018": "'", "\u2019": "'",
})


def canonicalize(q: str, is_quoted: bool = False) -> str:
    """Return the canonical form of a query per §3.1."""
    if q is None:
        return ""
    s = q.translate(_CURLY_QUOTES)
    s = _WHITESPACE.sub(" ", s).strip()
    s = s.lower()
    if is_quoted and not (s.startswith('"') and s.endswith('"')):
        s = f'"{s}"'
    return s


# --------------------------------------------------------------------------- #
# Extractors — one per tributary
# --------------------------------------------------------------------------- #

def extract_main_capture(data: dict) -> List[dict]:
    """
    EA-WG-CAPTURES-01.json — each entry is a capture event.
    Compressed keys: s=section, q=query, sf=source_format, mt=match_type/status, d=details.
    """
    out = []
    for e in data.get("entries", []):
        query = e.get("q") or e.get("query") or ""
        if not query:
            continue
        slug = e.get("slug", "")
        gallery = f"https://godkinggoogle.vercel.app/captures/#{slug}" if slug else None
        mirror = f"https://leesharks.com/captures/#{slug}" if slug else None
        obs = {
            "source": "mm-main-capture",
            "date": e.get("date") or "",
            "status": e.get("mt") or e.get("status"),
            "source_format": e.get("sf") or e.get("source_format"),
            "section": e.get("s") or e.get("section"),
            "slug": slug,
            "gallery_url": gallery,
            "mirror_gallery_url": mirror,
            "details_excerpt": (e.get("d") or "")[:220] or None,
        }
        # detect is_quoted from surrounding quotes
        is_q = query.startswith('"') and query.endswith('"')
        out.append({
            "raw_query": query,
            "is_quoted": is_q,
            "refers_to": [],
            "type": None,
            "battery_membership": [],
            "observation": obs,
        })
    return out


def extract_rf_reception(data: dict) -> List[dict]:
    """
    mm-revfirst-registry.json — each entry is a reception observation.
    Keys: id, q, date, surface, framing, response_summary, battery_key.
    'framing' is the observation status (CORRECTION, ADOPTION, etc.)
    """
    out = []
    for e in data.get("entries", []):
        query = e.get("q") or e.get("query") or ""
        if not query:
            continue
        obs = {
            "source": "mm-rf-reception",
            "date": e.get("date") or "",
            "status": e.get("framing") or e.get("status"),
            "source_format": e.get("surface") or e.get("source_format"),
            "section": e.get("battery_key") or e.get("workstream"),
            "details_excerpt": (e.get("response_summary") or "")[:220] or None,
        }
        is_q = query.startswith('"') and query.endswith('"')
        out.append({
            "raw_query": query,
            "is_quoted": is_q,
            "refers_to": [],
            "type": None,
            "battery_membership": [e["battery_key"]] if e.get("battery_key") else [],
            "observation": obs,
        })
    return out


def extract_termindex(data: dict) -> List[dict]:
    """
    mm-termindex.json — 1400 terms; each is a subjunctive candidate.
    Keys: term, key, count, tier, category, first_date, first_doi, tested, variants, source.
    """
    out = []
    for e in data.get("entries", []):
        term = e.get("term") or e.get("key") or ""
        if not term:
            continue
        ti = {
            "tier": e.get("tier"),
            "count": e.get("count"),
            "category": e.get("category"),
            "first_date": e.get("first_date"),
            "first_doi": e.get("first_doi"),
            "tested_flag_in_termindex": bool(e.get("tested")),
            "variants": e.get("variants") or [],
            "extraction_source": e.get("source"),
        }
        out.append({
            "raw_query": term,
            "is_quoted": False,
            "refers_to": [],
            "type": None,
            "battery_membership": [],
            "observation": None,
            "termindex": ti,
        })
    return out


def extract_mint(data: dict) -> List[dict]:
    """
    mm-mint.json — Sémantique Potentielle families across releases.
    Each family's canonical + variants are subjunctive addresses.
    """
    out = []
    for release in data.get("releases", []):
        rel_id = release.get("id") or release.get("title")
        for fam in release.get("families", []):
            canonical = fam.get("canonical")
            if canonical:
                out.append({
                    "raw_query": canonical,
                    "is_quoted": False,
                    "refers_to": [fam.get("gloss")] if fam.get("gloss") else [],
                    "type": None,
                    "battery_membership": [str(rel_id)] if rel_id else [],
                    "observation": None,
                    "mint": {
                        "release": rel_id,
                        "coord": fam.get("coord"),
                        "family_id": fam.get("id"),
                        "category": fam.get("category"),
                        "forensic": fam.get("forensic"),
                    },
                })
            for variant in (fam.get("family") or []):
                out.append({
                    "raw_query": variant,
                    "is_quoted": False,
                    "refers_to": [canonical] if canonical else [],
                    "type": None,
                    "battery_membership": [str(rel_id)] if rel_id else [],
                    "observation": None,
                    "mint": {
                        "release": rel_id,
                        "coord": fam.get("coord"),
                        "family_id": fam.get("id"),
                        "variant_of_canonical": canonical,
                    },
                })
    return out


EXTRACTORS = {
    "extract_main_capture": extract_main_capture,
    "extract_rf_reception": extract_rf_reception,
    "extract_termindex": extract_termindex,
    "extract_mint": extract_mint,
}


# --------------------------------------------------------------------------- #
# Union algorithm (framework §5)
# --------------------------------------------------------------------------- #

def classify(observations: List[dict]) -> str:
    """
    §2.1 — deterministic class assignment (framework v1.1):
      subjunctive           — no observations at all
      verified_non_address  — has observations but ALL are negative
      observed_address      — has any observation (positive or unrated)
    An observation event is itself evidence the address exists at the
    reception surface; positive/negative/unrated are ratings within the
    observed class, surfaced via `latest_status`.
    """
    if not observations:
        return "subjunctive"
    classes = [_status_class(o.get("status")) for o in observations]
    has_any_positive_or_unrated = any(c in ("positive", "unrated") for c in classes)
    if has_any_positive_or_unrated:
        return "observed_address"
    return "verified_non_address"


def infer_type(refers_to: List[str], termindex: dict, existing: str = None) -> str:
    """Best-effort type inference. Preserves existing type if provided."""
    if existing:
        return existing
    if not refers_to:
        return "unmatched"
    if len(refers_to) == 1:
        return "single_concept"
    return "multi_concept"


def build_addresses(repo_root: str) -> Tuple[dict, dict]:
    """
    Load all tributaries, apply canonicalization, merge, classify.
    Returns (addresses_dict, input_hashes).
    """
    all_tributaries = {**OBSERVATION_TRIBUTARIES, **SUBJUNCTIVE_TRIBUTARIES}
    input_hashes = {}
    accumulator: Dict[str, dict] = defaultdict(lambda: {
        "canonical_query": None,
        "is_quoted": False,
        "refers_to": [],
        "type": None,
        "battery_membership": [],
        "sources": [],
        "observations": [],
        "termindex": None,
        "mint": None,
    })

    for tid, cfg in all_tributaries.items():
        path = os.path.join(repo_root, cfg["path"])
        if not os.path.exists(path):
            print(f"[warn] tributary {tid} missing at {path}; skipping", file=sys.stderr)
            continue
        with open(path, "rb") as fh:
            raw = fh.read()
            input_hashes[tid] = hashlib.sha256(raw).hexdigest()
        data = json.loads(raw.decode("utf-8"))
        extractor = EXTRACTORS[cfg["extractor"]]
        candidates = extractor(data)

        for c in candidates:
            key = canonicalize(c["raw_query"], c.get("is_quoted", False))
            if not key:
                continue
            a = accumulator[key]
            a["canonical_query"] = key
            a["is_quoted"] = a["is_quoted"] or c.get("is_quoted", False)
            for r in (c.get("refers_to") or []):
                if r and r not in a["refers_to"]:
                    a["refers_to"].append(r)
            if c.get("type") and not a["type"]:
                a["type"] = c["type"]
            for b in (c.get("battery_membership") or []):
                if b and b not in a["battery_membership"]:
                    a["battery_membership"].append(b)
            if tid not in a["sources"]:
                a["sources"].append(tid)
            if c.get("observation"):
                a["observations"].append(c["observation"])
            if c.get("termindex") and not a["termindex"]:
                a["termindex"] = c["termindex"]
            if c.get("mint") and not a["mint"]:
                a["mint"] = c["mint"]

    # Second pass — classify and finalize
    out = {}
    for key, a in sorted(accumulator.items()):
        a["observation_class"] = classify(a["observations"])
        a["type"] = infer_type(a["refers_to"], a.get("termindex"), a["type"])
        if a["observations"]:
            latest = max(a["observations"], key=lambda o: (o.get("date") or ""))
            a["latest_observation_date"] = latest.get("date")
            a["latest_status"] = latest.get("status")
        else:
            a["latest_observation_date"] = None
            a["latest_status"] = None
        # Drop mint field if empty (not part of published schema)
        if a.get("mint") is None:
            a.pop("mint", None)
        if a.get("termindex") is None:
            a.pop("termindex", None)
        out[key] = a

    return out, input_hashes


# --------------------------------------------------------------------------- #
# Emit
# --------------------------------------------------------------------------- #

def emit(addresses: dict, input_hashes: dict, timestamp: str = None) -> dict:
    from collections import Counter
    class_counts = Counter(a["observation_class"] for a in addresses.values())
    type_counts = Counter(a["type"] for a in addresses.values())
    total_obs = sum(len(a["observations"]) for a in addresses.values())

    all_tributaries = {**OBSERVATION_TRIBUTARIES, **SUBJUNCTIVE_TRIBUTARIES}
    sources_readable = {
        tid: f'{cfg["path"]} — {cfg["description"]}'
        for tid, cfg in all_tributaries.items()
    }

    return {
        "version": FRAMEWORK_VERSION,
        "description": (
            "Unified semantic-addresses dataset produced by the reference "
            "regenerator per EA-SEMANTIC-ADDRESSES-01 v1.0. Determinism "
            "guarantee: given the same tributary contents, output is "
            "byte-identical."
        ),
        "regenerated_at": timestamp or datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "regenerator": REGENERATOR_PATH,
        "framework_spec": "specs/EA-SEMANTIC-ADDRESSES-01.md",
        "schema": "data/semantic-addresses.schema.json",
        "input_hashes": input_hashes,
        "sources": sources_readable,
        "observation_classes": {
            "observed_address": (
                "Query has been observed at least once with a positive status "
                "(EXACT_MATCH, BROAD_MATCH, ADOPTION, WOUND_GAUGE)."
            ),
            "verified_non_address": (
                "Query has been observed at least once with a negative status "
                "(ZERO_RESULT, ZERO_INDEX, BASIN_MISS, DISPLACEMENT) and no positive observations."
            ),
            "subjunctive": (
                "Query catalogued from an authoring tributary but never observed "
                "— hypothesized address pending test."
            ),
        },
        "galleries": GALLERIES,
        "total_addresses": len(addresses),
        "total_observations": total_obs,
        "class_counts": dict(class_counts),
        "type_counts": dict(type_counts),
        "addresses": addresses,
    }


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--repo-root", default=".", help="repo root (default cwd)")
    p.add_argument("--dry-run", action="store_true", help="no write")
    p.add_argument("--verify", action="store_true", help="rebuild and diff against existing")
    p.add_argument("--pinned-timestamp", default=None, help="ISO timestamp for hash-reproducible builds")
    p.add_argument("--out", default="data/semantic-addresses.json")
    args = p.parse_args()

    addresses, input_hashes = build_addresses(args.repo_root)
    payload = emit(addresses, input_hashes, args.pinned_timestamp)

    out_path = os.path.join(args.repo_root, args.out)

    if args.verify:
        existing = json.load(open(out_path))
        # Compare essential fields excluding timestamp
        for k in ("total_addresses", "total_observations", "class_counts", "type_counts"):
            e = existing.get(k)
            n = payload.get(k)
            match = "==" if e == n else "!="
            print(f"  {k:20s}  existing={e}  new={n}  {match}")
        return

    if args.dry_run:
        print(f"[dry-run] would write {len(addresses)} addresses to {out_path}")
        print(f"  class_counts: {payload['class_counts']}")
        print(f"  type_counts:  {payload['type_counts']}")
        print(f"  input_hashes:")
        for tid, h in input_hashes.items():
            print(f"    {tid:20s}  {h[:16]}...")
        return

    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2, ensure_ascii=False)
    print(f"[ok] wrote {len(addresses)} addresses ({payload['total_observations']} observations) to {out_path}")
    print(f"  class_counts: {payload['class_counts']}")


if __name__ == "__main__":
    main()
