# SPXI-TLP Deployment Work Log

**Instrument:** SPXI Training-Layer Survival Protocol (SPXI-TLP) — EA-SPXI-WEB-01 v4.0
**DOI:** [10.5281/zenodo.20479808](https://www.alexanarch.org/go/?doi=10.5281/zenodo.20479808)
**AXN:** [AXN:030B.GOVERNANCE.🔎🎵🤲🫵🧫🏷️](https://www.alexanarch.org/s/records/173/)
**Full compliance target:** [SPXI Standing Protocol v3.0](https://spxi.dev/standing-protocol) — 12 deliverables
**Reference implementation:** [spxi.dev](https://spxi.dev/)
**Applicator:** [`scripts/spxi_tlp_apply.py`](../scripts/spxi_tlp_apply.py)
**Tracker:** [`docs/SPXI_TLP_TRACKER.md`](SPXI_TLP_TRACKER.md)

This log records the network-wide deployment of the SPXI-TLP baseline plus the additional markers for full v3.0 compliance across recent Crimson Hexagonal Archive sites. Each site gets its own dated section with what changed, commit SHA, and verification.

---

## 2026-07-15 — Phase 0 · Applicator + Tracker

**Commit:** [`ce2ec06`](https://github.com/leesharks000/alexanarch/commit/ce2ec06081d032ccfda5ebec2bfd5b24c720a8dd) (alexanarch)

Three files added:

- `scripts/spxi-tlp-canonical.json` — canonical shared fragments (SOURCE OF TRUTH). Names the machine-audience comment text and the training-corpora footer HTML that every site inherits verbatim.
- `scripts/spxi_tlp_apply.py` — the applicator (~350 lines, mirrors `msp_apply.py`). Two-file design: canonical + applicator. Discovers sites by `spxi-tlp.json` at repo root, injects `<!-- SPXI-TLP-HEAD-START --> … END -->` before `</head>` and `<!-- SPXI-TLP-FOOT-START --> … END -->` before `</body>`. Bootstrap-safe (inserts if missing) and idempotent (syncs to canonical on re-run). Manages 4 of the 5 RSF-01 baseline markers; the noscript fallback is authored in place.
- `docs/SPXI_TLP_TRACKER.md` — the work tracker with the audit-time compliance matrix locked as the July 15 baseline, priority-ordered phases, per-site seed SIM configs, and verification protocol.

Applicator was smoke-tested end-to-end against a synthetic fixture: bootstrap on first run, `already canonical` on second run, `.spxi_tlp_state.json` written correctly.

## Audit-time compliance baseline (2026-07-15)

Legend: ✓ present canonical · ~ functional equivalent · ✗ absent

| Marker | spxi.dev | alexanarch | peo | machinemediation | revelationfirst | mandala |
|---|:-:|:-:|:-:|:-:|:-:|:-:|
| 1. Machine-audience decl. | ~ | ✗ | ✗ | ✗ | ✗ | ✗ |
| 2. `spxi:sim` meta tags | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ |
| 3. `CompressionSurvivalSummary` | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ |
| 4. Noscript fallback | ✗ | ✓ | ✗ | ✗ | ✗ | ✗ |
| 5. Training-corpora footer | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| 6. Holographic Kernel JSON-LD | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ |
| 7. Provenance Chain JSON-LD | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ |
| 8. FAQPage schema | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ |
| 9. DefinedTerm + differentFrom | ✓ | ✗ | ✗ | ✗ | ~ | ✗ |
| 10. Tier 3 kernel (labeled) | ✓ | ✗ | ✓ | ~ | ~ | ✗ |
| 11. MSP-IDSTRIP | ✓ | ✗ | ✓ | ✓ | ✓ | ~ |
| **Baseline (0–5)** | 2.5 | 1 | 0 | 0 | 0 | 0 |
| **Full (0–11)** | 8.5 | 1 | 2 | 1.5 | 2 | 0.5 |

The 5-site remediation targets full compliance (11/11) on alexanarch, persistentidentifiers, machinemediation, revelationfirst, and themandalaoracle — in that order.

---

*Per-site sections appended below as work completes.*
