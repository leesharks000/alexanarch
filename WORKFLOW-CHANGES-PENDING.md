# Pending Workflow Changes

The schema-correction commit `2b586d5` landed all code, data, docs, and surface regeneration for the AXN v2 + protocol enforcement work. Two `.github/workflows/` changes were prepared but could not be pushed because the PAT in use does not have the `workflow` scope.

You need to apply these two workflow changes with a PAT that has `workflow` scope (settings → tokens → Generate new token (classic) → check `workflow`), or via the GitHub web UI / Codespaces.

After these workflows are applied, the enforcement layer is fully active: new deposits that don't conform to `api/deposit-protocol.json` are mechanically rejected, and the consistency invariants are checked on every push/PR.

---

## Change 1: Update `.github/workflows/mint-axn.yml`

Three edits to the existing file. The full updated file is also saved at `/tmp/workflow-changes/mint-axn.yml.new` in the working environment. Diff summary:

### Edit 1.A — 4-emoji → 6-emoji glyph derivation

Find:
```javascript
const emoji = [AXN_GLYPHS[hash[0]], AXN_GLYPHS[hash[1]], AXN_GLYPHS[hash[2]], AXN_GLYPHS[hash[3]]].join('');
const clusters = [CLUSTERS[hash[0]], CLUSTERS[hash[1]], CLUSTERS[hash[2]], CLUSTERS[hash[3]]];
```

Replace with:
```javascript
const emoji = [AXN_GLYPHS[hash[0]], AXN_GLYPHS[hash[1]], AXN_GLYPHS[hash[2]], AXN_GLYPHS[hash[3]], AXN_GLYPHS[hash[4]], AXN_GLYPHS[hash[5]]].join('');
const clusters = [CLUSTERS[hash[0]], CLUSTERS[hash[1]], CLUSTERS[hash[2]], CLUSTERS[hash[3]], CLUSTERS[hash[4]], CLUSTERS[hash[5]]];
```

### Edit 1.B — Add schema/protocol version fields to mint output

Find:
```javascript
wiki_article: null,
wiki_status: 'provisional',
entities: [],
entity_status: 'provisional'
};
```

Replace with:
```javascript
wiki_article: null,
wiki_status: 'provisional',
entities: [],
entity_status: 'provisional',
axn_schema_version: 'v2',
protocol_version: 'alexanarch-deposit-protocol/v1',
};
```

### Edit 1.C — Run regenerate_surfaces.py and commit all surfaces atomically

Find (the final step):
```yaml
      - name: Commit registry update
        run: |
          git config user.name "Alexanarch Bot"
          git config user.email "bot@alexanarch.org"
          git pull --rebase || true
          git add data/registry.json data/deposits/ s/records/
          if git diff --cached --quiet; then
            echo "Registry already up to date"
          else
            git commit -m "Mint AXN - deposit #$(cat data/registry.json | python3 -c 'import sys,json; print(json.load(sys.stdin)["total_deposits"])')"
            git push
          fi
```

Replace with:
```yaml
      - name: Regenerate derived surfaces (browse, browse-index, chunks, sitemap, SHA256SUMS)
        if: success()
        run: |
          # Bring every derived surface into agreement with the updated registry.
          # See DEPOSIT-FLOW.md for the full surface inventory.
          python3 scripts/regenerate_surfaces.py

      - name: Commit registry update + derived surfaces
        run: |
          git config user.name "Alexanarch Bot"
          git config user.email "bot@alexanarch.org"
          git pull --rebase || true
          git add data/registry.json data/deposits/ s/records/ \
                  s/browse/ data/browse-index.json data/chunks/registry/ \
                  sitemap.xml SHA256SUMS.txt
          if git diff --cached --quiet; then
            echo "Registry already up to date"
          else
            git commit -m "Mint AXN - deposit #$(cat data/registry.json | python3 -c 'import sys,json; print(json.load(sys.stdin)["total_deposits"])')"
            git push
          fi
```

---

## Change 2: Create `.github/workflows/validate-registry.yml` (NEW)

This is the CI enforcement layer. Create the file with this content:

```yaml
name: Validate Registry & Deposit Protocol

on:
  push:
    branches: [main]
    paths:
      - 'data/registry.json'
      - 'api/deposit-protocol.json'
      - 'api/deposit-schema.json'
      - 'scripts/**'
      - 'data/texts/**'
  pull_request:
    branches: [main]
    paths:
      - 'data/registry.json'
      - 'api/deposit-protocol.json'
      - 'api/deposit-schema.json'
      - 'scripts/**'
      - 'data/texts/**'
  workflow_dispatch:

jobs:
  validate-protocol:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      pull-requests: write
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Validate api/deposit-protocol.json is valid JSON
        run: python3 -m json.tool api/deposit-protocol.json > /dev/null

      - name: Validate api/deposit-schema.json is valid JSON
        run: python3 -m json.tool api/deposit-schema.json > /dev/null

      - name: Validate registry against current protocol (strict)
        id: validate
        run: |
          python3 scripts/validate_deposit.py --registry data/registry.json --strict

      - name: Run DEPOSIT-FLOW.md consistency invariants
        run: |
          python3 << 'PY'
          import json, glob, sys
          ok = True
          def check(cond, msg):
              global ok
              if not cond:
                  print(f"FAIL: {msg}")
                  ok = False
              else:
                  print(f"  ok: {msg}")

          reg = json.load(open('data/registry.json'))
          n = reg['total_deposits']
          deposit_numbers = [d['deposit_number'] for d in reg['deposits']]
          check(n == len(reg['deposits']), f"total_deposits ({n}) == len(deposits) ({len(reg['deposits'])})")
          check(deposit_numbers == sorted(deposit_numbers), "deposit numbers in ascending order")
          check(min(deposit_numbers) == 1, "first deposit is #1")
          check(max(deposit_numbers) == n, f"deposit numbers contiguous 1..{n}")

          bi = json.load(open('data/browse-index.json'))
          check(bi['total'] == n, f"browse-index.total ({bi['total']}) == registry.total ({n})")
          check(len(bi['deposits']) == n, f"browse-index list length ({len(bi['deposits'])}) == {n}")

          cidx = json.load(open('data/chunks/registry/_index.json'))
          check(cidx['total_deposits'] == n, f"chunks-index.total_deposits == {n}")
          chunk_count = len(glob.glob('data/chunks/registry/chunk-*.json'))
          check(cidx['total_chunks'] == chunk_count, f"chunks-index.total_chunks ({cidx['total_chunks']}) == file count ({chunk_count})")

          browse = open('s/browse/index.html').read()
          check(f'registry of {n} deposits' in browse, f"browse page total claim matches registry")
          missing = [num for num in deposit_numbers if f'/s/records/{num}/' not in browse]
          check(not missing, f"browse contains all record URLs (missing: {missing[:5]}...)" if missing else "browse contains all record URLs")

          sitemap = open('sitemap.xml').read()
          missing = [num for num in deposit_numbers if f'/s/records/{num}/' not in sitemap]
          check(not missing, f"sitemap contains all record URLs (missing: {missing[:5]}...)" if missing else "sitemap contains all record URLs")

          if not ok:
              print("\nRegistry/surface inconsistency detected. Run: python3 scripts/regenerate_surfaces.py")
              sys.exit(1)
          print("\nAll consistency invariants pass.")
          PY

      - name: Comment on PR with failure details
        if: failure() && github.event_name == 'pull_request'
        uses: actions/github-script@v7
        with:
          script: |
            github.rest.issues.createComment({
              owner: context.repo.owner,
              repo: context.repo.repo,
              issue_number: context.issue.number,
              body: [
                '## ❌ Deposit protocol validation failed',
                '',
                'This PR introduces a state that does not conform to the canonical protocol at `api/deposit-protocol.json`.',
                '',
                'See the workflow logs for the specific rule IDs that failed.',
                '',
                'Common fixes:',
                '- Run `python3 scripts/regenerate_surfaces.py` to bring derived surfaces back into agreement with `data/registry.json`.',
                '- Re-read [DEPOSIT-FLOW.md](https://github.com/leesharks000/alexanarch/blob/main/DEPOSIT-FLOW.md) for the canonical pipeline.',
                '- If your deposit uses an AXN with the wrong emoji count, run `python3 scripts/backfill_axn_compliance.py`.',
                '',
                '*This is automated enforcement, not a polite reminder. Submissions that do not validate are not merged.*'
              ].join('\n')
            });
```

---

## Fastest application path

1. Generate a new PAT at https://github.com/settings/tokens with both `public_repo` and `workflow` scopes.
2. Replace the PAT in the local clone:
   ```
   git remote set-url origin https://NEW_PAT@github.com/leesharks000/alexanarch.git
   ```
3. The prepared workflow files are saved at `/tmp/workflow-changes/` in the session environment. To re-apply them:
   ```
   cp /tmp/workflow-changes/mint-axn.yml.new .github/workflows/mint-axn.yml
   cp /tmp/workflow-changes/validate-registry.yml.new .github/workflows/validate-registry.yml
   git add .github/workflows/
   git commit -m "AXN v2 enforcement: workflow changes (part 2)"
   git push origin main
   ```

Alternatively, paste the contents above directly into the GitHub web UI editor for each file.

---

## What works without these workflow changes

- All Path B (canonical rich deposit) work, including `scripts/validate_deposit.py` for pre-push validation.
- Backfill (`scripts/backfill_axn_compliance.py`) is one-shot and complete.
- Protocol JSON, schema JSON, docs are all live.

## What does NOT work without these workflow changes

- New auto-minted deposits (Path A via GitHub Issue) will still produce 4-emoji AXNs because the mint workflow hasn't been updated.
- The CI enforcement layer (validate-registry.yml) isn't running, so non-conforming commits to the registry can land on main without triggering a block.

This is the gap. Apply the workflow changes to close it.

---

*Schema correction commit: `2b586d5`. Workflow changes prepared, pending workflow-scope PAT.*
