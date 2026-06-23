# Alexanarch recovery procedure

This document explains how to reconstruct a functioning Alexanarch deployment from the public repository contents, in the event the canonical deployment becomes unavailable. The goal is **byte-identical reconstruction** of the static surfaces and **functional reconstruction** of the dynamic ones from a fresh operator account.

The repository is the source of truth. Everything below assumes you have a clone of `github.com/leesharks000/alexanarch` (or a complete mirror — see §6 below).

## 1. What you need

**Minimum** (for a read-only mirror):
- A clone of the repository
- A static-file web server (Nginx, Caddy, GitHub Pages, Vercel, Cloudflare Pages)
- Python 3.10+ to regenerate any derived surfaces
- About 200 MB of disk

**Recommended** (for a fully operational mirror with deposit capability):
- A GitHub account with Actions enabled
- Vercel or equivalent serverless host
- A domain name (or use the host's default subdomain)

## 2. Verify what you have

Before deploying anything, verify the bytes:

```bash
cd alexanarch/
sha256sum -c SHA256SUMS.txt
```

This should report `OK` for every entry. `SHA256SUMS.txt` lists real file paths under `data/texts/` (one line per deposit). If any entry fails, the corresponding deposit text file has drifted from its recorded hash — investigate before publishing.

Then verify the registry matches its declared count:

```bash
python3 -c "import json; r=json.load(open('data/registry.json')); print(f'{len(r[\"deposits\"])} deposits, total_deposits field says {r[\"total_deposits\"]}')"
```

These should agree.

## 3. Regenerate derived surfaces

The repository ships with the derived surfaces already generated. If you want to verify they match the registry, regenerate from scratch:

```bash
python3 scripts/regenerate_surfaces.py
```

This regenerates: `data/state.json`, `s/browse/index.html`, `data/browse-index.json`, `data/chunks/registry/*`, `sitemap.xml`, `SHA256SUMS.txt`, `RECORD-SHA256-MANIFEST.txt`, `s/wiki/index.html` and the 9 wiki chunks, `s/graph/index.html`, `index.html` noscript fallback, and `api/index.json` (drift corrections).

Then regenerate the record pages and the observatory:

```bash
python3 -c "
import json, sys
sys.path.insert(0, '.')
import wire_deposit
reg = json.load(open('data/registry.json'))
eidx = json.load(open('data/entity-index.json'))
for d in reg['deposits']:
    wire_deposit.regenerate_static_page(d, eidx, registry=reg)
"
python3 scripts/generate_observatory.py
```

You can compare your regenerated output against the repository copy with `git diff`; non-zero diff means your registry has drifted from the canonical state.

## 4. Deploy as static

Point any static-file host at the repository root. Examples:

**Vercel**: connect the repository as a project; Vercel auto-deploys on every push. The `vercel.json` in the repo configures redirects (e.g. `/observatory/surface-weather/` → `/observatory/`), security headers (CSP, frame-options, etc.), and CORS for `/data/` and `/api/` JSON.

**GitHub Pages**: enable Pages on the repository, set the source to the root branch. Note: GitHub Pages doesn't honor `vercel.json`; you'd need to translate the redirects to `_redirects` (Cloudflare/Netlify format) or rely on the static `<noscript>` and meta-refresh fallbacks.

**Nginx**: serve the repository root directly. Apply the security headers from `vercel.json` in your `nginx.conf`. Redirects in `vercel.json` translate to `rewrite` directives.

After deploy, smoke-test:
- `/` should render the home page with 16-link nav
- `/s/browse/` should list all 884 deposits
- `/s/records/1/` should render Zenodotus' Book-Burning
- `/data/registry.json` should serve as JSON
- `/api/index.json` should serve as JSON
- `/observatory/` should render the Surface Weather Station

## 5. Restore deposit capability (optional)

The mint workflow at `.github/workflows/mint-axn.yml` listens for `[DEPOSIT]`-prefixed issues, validates them against `api/deposit-protocol.json` and `api/deposit-schema.json`, mints an AXN, regenerates surfaces, and opens a PR for auto-merge.

To enable on a new repository:
1. Push the repository to your own GitHub remote
2. In repository Settings → Actions → General: allow workflow permissions to read+write, allow workflow to create PRs
3. In Settings → General: enable "Allow auto-merge"
4. In Settings → Branches: protect `main`, require the `validate-registry / validate-protocol` status check before merging, disallow direct push and force-push
5. Open a test deposit via Issues → New Issue → Deposit a Work; the workflow should mint + PR + auto-merge end to end

If you skip this, you have a read-only mirror — which is still valuable.

## 6. Mirror sources

If the canonical repository is also unavailable, complete mirrors should exist at:

- `https://github.com/leesharks000/alexanarch` (canonical)
- `https://alexanarch.org/` (deployed)
- Any operator-declared mirror node (see `/rhizome/peers.json` if/when that surface ships)

A complete release should always carry:
- A release ID
- A source commit SHA
- The registry SHA-256
- A file checksum manifest (`SHA256SUMS.txt`)
- A semantic record manifest (`RECORD-SHA256-MANIFEST.txt`)
- The chunk index with per-chunk hashes (`data/chunks/registry/_index.json`)

If you have these, byte-identical reconstruction is possible.

## 7. Identity continuity

The corpus's identity is its content hashes, not its hosting. An AXN identifier like `AXN:01.GOVERNANCE.♍🜁🏴⌛🍃💫` is verifiable from any complete mirror by re-deriving from the canonical bytes. The domain `alexanarch.org` is a convenience surface, not the institution.

If you reconstruct under a different domain, the AXNs are still valid; the resolution surface changes but the identifier doesn't. This is a constitutional property: identifiers are derived from content, not granted by hosts.

---

*Last updated 2026-06-23.*
