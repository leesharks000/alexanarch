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
    "lexical_attested_none": true
  }
}

The completeness gate remains authoritative. This bridge does not weaken it.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REGISTRY = ROOT / "data" / "registry.json"

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

    REGISTRY.write_text(
        json.dumps(reg, indent=1, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    print(
        f"applied internal session packet to #{args.deposit_number}: "
        + ", ".join(sorted(patch))
    )


if __name__ == "__main__":
    main()
