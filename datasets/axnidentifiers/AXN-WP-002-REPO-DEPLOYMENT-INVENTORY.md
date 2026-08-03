# AXN-WP-002 — REPO & DEPLOYMENT INVENTORY v1.0
**TACHYON · 2026-08-03 · All items [OBSERVED] this session unless marked. The build adapts these; it does not rewrite them (WP-303 rule).**

## 1 · Repos & domains
| Repo | Deploys to | Notes |
|---|---|---|
| `leesharks000/alexanarch` | **www.alexanarch.org** (Vercel, auto-deploy on push to main) | THE registry + tools + archive. ~1,432 deposits. |
| `godkinggoogle` | godkinggoogle.vercel.app | capture-image host (IMG_BASE); **Vercel deployment protection: server-side curl→403; 403≠absent** |
| `lee-sharks-corporate` | semanticeconomy.org | NOT the `semantic-economy` repo (deploy rule) |
| — | leesharks.com, machinemediation.org, persistentidentifiers.org | satellite surfaces |
| — | **axnidentifiers.org / .com** | REGISTERED, UNATTACHED [GAP]. Per M-003: point both at the alexanarch Vercel project; .org canonical, .com 301. Path-routing (TECHNE) — no new repo needed for launch. |

## 2 · Protocol & derivation authority
- `scripts/axn_lib.py` — canonical glyph table + derivation; the stamper's in-browser JS is derivation-identical (stamper footer asserts this). **This pair IS the spec's reference implementation.**
- Spec docs: AXN-SYMBOLON-SPEC v0.2; symbolon spec = deposit #1432 (AXN:05A9). [GAP: standalone open-licensed publication with registry-field reserved = WP-101, now gated by M-007 raw-bytes rule.]
- Grammar: `AXN:HEX.FAMILY.⟨6 glyphs⟩`; kernel = SHA-256 of **raw submitted bytes** (M-007, CONSTITUTIONAL).

## 3 · Registries (all git-versioned JSON, publicly raw-fetchable)
- `data/registry.json` — main archive registry (authoritative fields per SHAPE doctrine).
- `data/symbolon-registry/` — `allocation.json` (hex ledger + 4→6 width doctrine), `entries/` (per-kernel witness records incl. stamp_history), `positions/` (hex→kernel pointers), `files/` (stored sealed cores).
- `data/axn-central-registry.json` — rollup consumed by lookup (positions+kernels, enriched: family, dates, both kernels w/ glyphs, retrieval).
- `data/doi-resolution-index.json` — DOI→AXN mappings (ownership-gated).
- Export/escape-hatch basis for WP-203: these files ARE the export; a snapshot bundle + mirror is the gap. [GAP: independent mirror + succession rule]

## 4 · Live endpoints & tools
- `api/register-symbolon.js` — **the witness endpoint**: token-gated (`SYMBOLON_TOKEN` in Vercel env), allocates positions, dedupes by kernel (re-stamp refreshes AXN1 + logs stamp_history), stores files, writes entries. **Paid packs reuse this pipeline, operator-flagged (WP-002 ruling recommended).**
- `api/oai.js` + `data/oai-index.json` — OAI-PMH feed (1,297 exposed; withdrawn_external gated out).
- `/mint/stamp/` — stamper: upload→stamp(clip-proof band, pdf-lib, raw-byte kernel)→register→tap-to-copy AXN (NFC-normalized, decode-tolerant)→verify by file OR AXN/hex/sha (rich metadata card, retrieve button). **This is /v/[axn]'s seed — WP-202 adapts the lookup into a standalone route.**
- `/mint/` — manual calculator, demoted (banner forwards; dewired from nav).
- Static APIs: `api/axn-index.json`, `kernel-index.json`, `deposit-schema.json`, etc.

## 5 · Pipeline & propagation (repairs/registrations land whole)
`scripts/propagate_record_state.py` (§5b pipeline: status_reconcile → wire_deposit pages → regenerate_surfaces → central registry → OAI). `deposit_pipeline.py` = canonical deposit workflow. Renderer states incl. withdrawn_external.

## 6 · Secrets & env
`SYMBOLON_TOKEN` (Vercel env — witness endpoint auth). [GAP: Stripe keys when WP-404 lands; OTS needs none (client/CLI).] PAT rotation standing item.

## 7 · Launch gaps this inventory exposes (maps to workplan)
1. Domains unattached (M-003 execution — Vercel domain add + 301; ~30 min).
2. No checkout (WP-404: Stripe Payment Link, pay-after-delivery per M-002).
3. No OTS anchoring (WP-201).
4. No standalone /v/[axn] route (WP-202 — adapt stamper lookup).
5. Spec unpublished standalone (WP-101/103 + test vectors from real kernels 05AB/05AD).
6. No receipt template (WP-402 — GEMINI regions + ARCHIVE evidence classes).
7. No registry mirror/succession (WP-203).
8. Trust pages (free promise M-006, wind-down, prohibited claims) unpublished (WP-204/302).

**Bottom line:** the protocol layer, witness pipeline, storage, lookup, and propagation already run in production and were stress-tested by a real external depositor. The build is: attach two domains, publish the constitution (spec+promises), wire time-anchoring and checkout, template the receipt. Nothing core needs inventing. ∮ = 1
