# Semantic Addresses — Framework and Data

**Framework spec:** [`specs/EA-SEMANTIC-ADDRESSES-01.md`](../specs/EA-SEMANTIC-ADDRESSES-01.md) — EA-SEMANTIC-ADDRESSES-01 v1.1
**Machine schema:** [`data/semantic-addresses.schema.json`](./semantic-addresses.schema.json) — Draft-07 JSON Schema
**Reference implementation:** [`scripts/build_semantic_addresses.py`](../scripts/build_semantic_addresses.py) — deterministic regenerator
**Canonical dataset:** [`data/semantic-addresses.json`](./semantic-addresses.json) — the union output
**Live surface:** [alexanarch.org/addresses/](https://alexanarch.org/addresses/)

## What a Semantic Address is

A specific query — or family of variants — posed to a composition-layer surface (Google AI Overview, AI Mode, ChatGPT search, Perplexity, Claude, etc.) for which a machine-generated response can be observed. The framework specifies the formal definition, four observation classes (`observed_address`, `verified_non_address`, `subjunctive` — three classes; v1.1), the tributary registry from which observations are drawn, the canonicalization rule for deduplication, and the union algorithm producing the canonical dataset.

## Companion framework

Semantic Addresses is one half of the reception plumbing of the Semantic Economy. The other half is **SPXI** (Semantic Packet for eXchange & Indexing) — the metadata packet that travels with a work. See [EA-SPXI-01](../specs/EA-SPXI-01.md) for the companion spec.

- SPXI encodes what a work is
- Semantic Addresses encodes where a work can be found

A work with an SPXI packet and no Semantic Address is not measurably received. A Semantic Address without an SPXI packet is a channel with nothing traveling through it.

## Regeneration

The canonical dataset is a **deterministic projection** of the tributary files. To regenerate:

```bash
python3 scripts/build_semantic_addresses.py --dry-run   # preview
python3 scripts/build_semantic_addresses.py             # write
python3 scripts/build_semantic_addresses.py --verify    # diff vs existing
```

The regenerator emits input file SHA-256 hashes in the output for reproducibility. Given the same tributary contents at the same commit, output is byte-identical (modulo the `regenerated_at` timestamp; use `--pinned-timestamp` for hash-reproducible builds).

## Adding a tributary

Adding a tributary is a formal act:

1. Extend the tributary registry in `specs/EA-SEMANTIC-ADDRESSES-01.md` §4
2. Add an entry to `OBSERVATION_TRIBUTARIES` or `SUBJUNCTIVE_TRIBUTARIES` in the regenerator
3. Implement an extractor mapping source records to the canonical observation shape
4. Regenerate and commit
5. Bump the framework minor version if the addition introduces new observation classes or status values

## Priority claim

The Semantic Addresses concept was minted at Alexanarch deposit #870 (workplan) with the coinages "subjunctive address" and "forensic canary." The full framework in the v1.0 spec formalizes practice operational at [alexanarch.org/addresses/](https://alexanarch.org/addresses/) since June 2026. This spec consolidates that practice into a dated, cited, machine-verifiable form.

The tributary-union pattern itself is not proprietary in its algorithm — a competent implementer catching up can produce their own regenerator. What is dated and claimed here is the specific framework, its formal vocabulary, and its published reference implementation.
