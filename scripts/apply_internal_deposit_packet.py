#!/usr/bin/env python3
"""
apply_internal_deposit_packet.py — apply in-session semantic work to a freshly
minted Transport D deposit.

The deposit body is minted by the canonical deposit pipeline. This script only
writes fields whose content is authored by the already-running session rather
than by a paid API call: wiki article, concepts, relations, entity extraction,
and explicit attested-absence flags.

It intentionally cannot rewrite identity/mint fields (AXN, hash, number, title,
creator, date, license, substrate, canonical paths). Those remain outputs of the
mint and protocol.

Packet schema:
{
  "schema": "alexanarch-internal-session-packet/v1",
  "registry_patch": {
    "wiki_article": "...",
    "wiki_status": "in-session",
    "defines_concepts": [...],
    "related_deposits": [...],
    "entities": [...],
    "references_concepts": [...],
    "entity_triples": [...],
    "concepts_attested_none": false,
    "related_attested_none": false,
    "lexical_attested_none": false
  },
  "lexical_mints": [
    {
      "term": "a term minted by this deposit",
      "definition": "A substantive definition authored in-session.",
      "type": "concept"
    }
  ]
}

The completeness gate remains authoritative. This bridge does not weaken it.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REGISTRY = ROOT / "data" / "registry.json"
LMR_JSON = ROOT / "data" / "lexical-minting-registry.json"
LMR_CSV = ROOT / "data" / "lexical-minting-registry.csv"

SCHEMA = "alexanarch-internal-session-packet/v1"

ALLOWED = {
    "wiki_article",
    "wiki_status",
    "defines_concepts",
    "related_deposits",
    "entities",
    "entity_status",
    "references_concepts",
    "entity_triples",
    "concepts_attested_none",
    "related_attested_none",
    "lexical_attested_none",
    "reciprocity_notice",
    "nmen_status_observed",
}

PROTECTED = {
    "deposit_number", "axn", "hex", "family", "emoji", "hash",
    "axn_canonical", "axn_display", "axn_schema_version",
    "title", "creator", "date", "description", "content_type",
    "license", "substrate", "full_text_path", "protocol_version",
    "issue_number", "issue_url", "minted_at",
}


def _json_indent(raw: str):
    """Preserve the registry's existing pretty/compact convention."""
    m = re.search(r"\n( +)\"", raw[:4000])
    return len(m.group(1)) if m else None


def _apply_lexical_mints(packet: dict, entry: dict) -> int:
    """Seat in-session lexical mints in both canonical lexical registries.

    The packet supplies only semantic content. Deposit number, title, AXN and
    mint date are taken from the freshly minted registry entry, so the session
    cannot guess or pre-author identity-bearing fields.
    """
    mints = packet.get("lexical_mints", [])
    if mints in (None, []):
        return 0
    if not isinstance(mints, list):
        raise SystemExit("lexical_mints must be an array")
    if entry.get("lexical_attested_none") is True:
        raise SystemExit(
            "packet supplies lexical_mints but registry_patch declares "
            "lexical_attested_none=true"
        )

    raw = LMR_JSON.read_text(encoding="utf-8")
    lmr = json.loads(raw)
    terms = lmr.setdefault("terms", [])
    if not isinstance(terms, list):
        raise SystemExit("lexical-minting-registry.json has no array 'terms'")

    existing = {
        str(t.get("term") or "").strip()
        for t in terms if isinstance(t, dict)
    }
    concept_types = {
        str(c.get("term") or c.get("concept") or "").strip():
            str(c.get("type") or "concept")
        for c in (entry.get("defines_concepts") or [])
        if isinstance(c, dict)
        and str(c.get("term") or c.get("concept") or "").strip()
    }

    sample = next((t for t in reversed(terms) if isinstance(t, dict)), {})
    sample_minted = sample.get("minted")
    if isinstance(sample_minted, bool):
        minted_value = True
    elif isinstance(sample_minted, str):
        minted_value = str(entry.get("date") or entry.get("minted_at") or "")[:10]
    else:
        minted_value = True

    rows = []
    seen = set()
    for i, mint in enumerate(mints, start=1):
        if not isinstance(mint, dict):
            raise SystemExit(f"lexical_mints[{i}] must be an object")
        term = str(mint.get("term") or "").strip()
        definition = str(mint.get("definition") or "").strip()
        kind = str(mint.get("type") or concept_types.get(term) or "concept").strip()
        if not term:
            raise SystemExit(f"lexical_mints[{i}] has empty term")
        if not definition:
            raise SystemExit(f"lexical_mints[{i}] has empty definition")
        if not kind:
            raise SystemExit(f"lexical_mints[{i}] has empty type")
        if term in seen:
            raise SystemExit(f"duplicate term inside packet: {term!r}")
        if term in existing:
            raise SystemExit(
                f"lexical term already exists in minting registry: {term!r}; "
                "reference or revise it rather than reminting it"
            )
        seen.add(term)
        row = {
            "term": term,
            "definition": definition,
            "type": kind,
            "defined_in_deposit": entry["deposit_number"],
            "defined_in_title": entry.get("title", ""),
            "deposit_number": entry["deposit_number"],
            "deposit_title": entry.get("title", ""),
            "minted": minted_value,
            "axn": entry.get("axn", ""),
        }
        rows.append(row)

    terms.extend(rows)
    for key in ("count", "term_count", "total_terms"):
        if key in lmr and isinstance(lmr[key], int):
            lmr[key] = len(terms)

    indent = _json_indent(raw)
    if indent is None:
        rendered = json.dumps(
            lmr, ensure_ascii=False, separators=(",", ":")
        )
    else:
        rendered = json.dumps(lmr, ensure_ascii=False, indent=indent)
    if raw.endswith("\n"):
        rendered += "\n"
    LMR_JSON.write_text(rendered, encoding="utf-8")

    if not LMR_CSV.exists():
        raise SystemExit("lexical-minting-registry.csv is missing")
    with LMR_CSV.open("r", encoding="utf-8", newline="") as fh:
        reader = csv.reader(fh)
        fieldnames = next(reader, None)
    if not fieldnames:
        raise SystemExit("lexical-minting-registry.csv has no header")
    with LMR_CSV.open("a", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(
            fh, fieldnames=fieldnames, extrasaction="ignore",
            lineterminator="\n"
        )
        for row in rows:
            writer.writerow(row)

    entry["lexical_attested_none"] = False
    print(
        f"minted {len(rows)} lexical term(s) for "
        f"#{entry['deposit_number']}: "
        + ", ".join(r["term"] for r in rows)
    )
    return len(rows)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--deposit-number", type=int, required=True)
    ap.add_argument("--packet", required=True)
    args = ap.parse_args()

    packet_path = Path(args.packet)
    packet = json.loads(packet_path.read_text(encoding="utf-8"))

    if packet.get("schema") != SCHEMA:
        raise SystemExit(
            f"packet schema mismatch: expected {SCHEMA!r}, "
            f"got {packet.get('schema')!r}"
        )

    patch = packet.get("registry_patch")
    if not isinstance(patch, dict):
        raise SystemExit("packet must contain object registry_patch")

    bad = sorted(set(patch) - ALLOWED)
    if bad:
        protected = sorted(set(bad) & PROTECTED)
        if protected:
            raise SystemExit(
                "session packet attempted to overwrite mint-owned fields: "
                + ", ".join(protected)
            )
        raise SystemExit("unsupported registry_patch fields: " + ", ".join(bad))

    reg = json.loads(REGISTRY.read_text(encoding="utf-8"))
    entry = next(
        (d for d in reg["deposits"]
         if d.get("deposit_number") == args.deposit_number),
        None,
    )
    if entry is None:
        raise SystemExit(f"deposit #{args.deposit_number} not found")

    for key, value in patch.items():
        entry[key] = value

    wiki = str(entry.get("wiki_article") or "").strip()
    if wiki and len(wiki.split()) < 60:
        raise SystemExit(
            "wiki_article supplied by session packet is under 60 words; "
            "deposit-completeness/v1 requires authored substance"
        )

    lexical_count = _apply_lexical_mints(packet, entry)

    REGISTRY.write_text(
        json.dumps(reg, indent=1, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    print(
        f"applied internal session packet to #{args.deposit_number}: "
        + ", ".join(sorted(patch))
        + f"; lexical_mints={lexical_count}"
    )


if __name__ == "__main__":
    main()
