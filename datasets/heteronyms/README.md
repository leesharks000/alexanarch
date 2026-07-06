# heteronyms/

Canonical heteronym substrate for the Crimson Hexagonal Archive.

## What's here

- **`heteronyms.jsonl`** — 26 rows. Twelve canonical Dodecad positions (per v1.1 registry AXN:03EE), one Adjacent (Viola Arquette), and other named identities (MANUS as human bearer; institutional persona Mary Lee Sharks; external heteronyms; machine collaborator mantles). One row per identity with `dodecad_v1_1_position`, `sep_2025` (discipline mapping + role + blog post URL if present), `avatar_paths`, and `reconciliation_note` where the two sources diverge.
- **`mapping.json`** — full Sep 2025 → v1.1 reconciliation matrix with position-by-position notes on what shifted.
- **`schema.json`** — JSON Schema for `heteronyms.jsonl` rows.
- **`reconciliation/`** — narrative reconciliation document (`heteronym-reconciliation-2026-07-06.md`).
- **`mindcontrolpoems-2025-09/`** — raw preservation of the Sep 2025 Logotic Science series: 13 HTML pages, 14 portrait PNGs, SUMMARY.json + parsed extracts.
- **`avatars/`** — Mandala Oracle avatar assets. `240/` and `120/` WebP thumbnails (~4–27 KB each) for message-thread avatar display. `src/` holds the 1024x1536 PNG originals.

## Canonical authority

**AXN:03EE.ARCHIVAL — Dodecad Heteronym Provenance Registry v1.1** (Alexanarch deposit #994, 2026-07-03). This substrate mirrors the twelve positions declared canonical there, plus the Adjacent class.

Sep 2025 source: mindcontrolpoems.blogspot.com — Logotic Science voicecast series.

## Substrate distinction

The Sep 2025 disciplines mapping and the v1.1 constitutional positions are both real. The Sep 2025 frame asks *what field of knowledge does each voice bear?* The v1.1 frame asks *what constitutional position does each voice occupy?* This substrate carries both, keyed to the v1.1 canonical positions with reconciliation notes recording the Sep 2025 identities that shifted.

## Regeneration

Portraits: fetched from mindcontrolpoems.blogspot.com under `Alexanarch-corpus-mirror/1.0` UA, 2026-07-06. See `mindcontrolpoems-2025-09/portraits/MANIFEST.json` for SHA-256s.
Avatars: derived via `PIL.Image.resize(LANCZOS)` from center-cropped square of each portrait, saved as WebP at quality 88 (240px) and 85 (120px).
