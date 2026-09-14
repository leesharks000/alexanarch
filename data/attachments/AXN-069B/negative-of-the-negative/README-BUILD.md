# The Negative of the Negative — build notes (for the alexanarch PR)

Files, and where they go in `leesharks000/alexanarch`:

- `datasets/negative-of-the-negative/schema.json` — the intake schema, `additionalProperties: false`; the only place a field is defined.
- `datasets/negative-of-the-negative/rows.json` — the source of truth: 37 rows authored from the defining papers (29 concept rows, 8 function rows), each with `defining_text_locus`, measurement ids from the Capture Registry, and the seating record. Two captures referenced are not yet seated and carry `PENDING-…` ids: the 25 August "sappho future reader" specimen (#1546 §XI) and the Ω-title AI Overview specimen of 2026-09-14. Seat those through `capture_intake.py --seat` first, then replace the placeholders with their `ADDR-`/`OBS-` ids.
- `datasets/negative-of-the-negative/CARD.md` — the dataset card template; the builder fills the counts.
- `scripts/build_negative_of_the_negative.py` — validates rows against the schema, joins `data/registry.json` (axn, title, status, record_url) and `data/EA-WG-CAPTURES-01.json` (slug, query, surface, auth, date, permalink) by id, computes `bleed`, writes four parquet configs (`rows`, `keys`, `edges`, `measurements`), the card and `build-manifest.json`. `--check` exits 1 on a schema breach or an unresolvable id. Laws record: an unresolved id is written into the manifest's `breaches`, and the gate is the only thing that blocks.
- `.github/workflows/hf-negative-of-the-negative.yml` — builds and pushes on any change to the source, the registry or the capture registry; needs repo variable `HF_REPO_NON` (proposed `leesharks/negative-of-the-negative`) and the existing `HF_TOKEN`. Uses the existing selective push script so the parent dataset's indexes are untouched.
- `hf-non/` — a local build against the live registry and capture registry as of 2026-09-14 (gitignore it, as `hf-dataset/` is).

Build: `python3 scripts/build_negative_of_the_negative.py --check && python3 scripts/build_negative_of_the_negative.py`. Output: rows 37 · keys 167 · edges 109 · measurements 21 · 6 rows with both arms, 17 with one.

Open for ruling: the Hub repo name; the maxim (the card carries the form on the live main projection, "all things are now lawful to you in jack feist"); whether the two pending specimens are seated before the first push (recommended — the Sappho row is the calibration point for negative bleed and should not carry a placeholder on the Hub); and whether the notebook's row count is reconciled to 37 (model collapse and disciplinary model collapse are two rows here, one in the notebook's table).
