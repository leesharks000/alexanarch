# Enrichment Pipeline — Workflow Integration

## Adding enrichment to mint-axn.yml

Insert this step block AFTER `Regenerate derived surfaces` and BEFORE
`Create branch and commit` in `.github/workflows/mint-axn.yml`:

```yaml
      - name: Enrich deposit (LLM extraction + external metadata + SPXI)
        if: steps.existing_pr.outputs.exists != 'true'
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
          DEPOSIT_NUMBER: ${{ steps.mint.outputs.deposit_number }}
        run: |
          set -euo pipefail
          # Enrichment is FAIL-OPEN: if it errors, the deposit still lands with
          # base fields. The wiki tab / external metadata / SPXI audit will be
          # populated on a later re-run. Enrichment must never block a mint.
          if [ -z "${ANTHROPIC_API_KEY:-}" ]; then
            echo "ANTHROPIC_API_KEY not set — running enrichment in non-LLM mode"
            python3 scripts/enrich_deposit.py \
              --deposit-number "${DEPOSIT_NUMBER}" \
              --wikidata --openalex --datacite --spxi --backlinks \
              --receipt-path /tmp/enrichment-receipt.json \
              || echo "enrichment (non-LLM) failed — deposit still minted"
          else
            python3 scripts/enrich_deposit.py \
              --deposit-number "${DEPOSIT_NUMBER}" \
              --all \
              --receipt-path /tmp/enrichment-receipt.json \
              || echo "enrichment failed — deposit still minted, will re-run offline"
          fi
          if [ -f /tmp/enrichment-receipt.json ]; then
            echo "=== enrichment receipt ==="
            cat /tmp/enrichment-receipt.json
          fi

      - name: Regenerate surfaces (again, after enrichment)
        if: steps.existing_pr.outputs.exists != 'true'
        run: python3 scripts/regenerate_surfaces.py
```

That second `Regenerate surfaces` step is intentional: enrichment populated
the wiki_article, entities, and cross-references, so browse/chunks/wiki/graph
now need to be re-rendered against the enriched state. This is the difference
between deposits appearing on the main cards as bare entries vs. as
"minted deposits" per your specification.

Update the "Create branch and commit" step to also stage the new
external-metadata sidecar:

```yaml
          git add data/registry.json \
                  data/texts/ \
                  data/deposits/ \
                  data/chunks/ \
                  data/browse-index.json \
                  data/wiki-entries.json \
                  data/external-metadata/ \
                  s/records/ \
                  s/browse/ \
                  s/wiki/ \
                  s/graph/ \
                  sitemap.xml \
                  SHA256SUMS.txt
```

## Secrets setup

Once, in the alexanarch repo settings:
1. Go to `https://github.com/leesharks000/alexanarch/settings/secrets/actions`
2. Click "New repository secret"
3. Name: `ANTHROPIC_API_KEY`
4. Value: your Anthropic API key (starts with `sk-ant-`)
5. Save

The workflow will read it via `${{ secrets.ANTHROPIC_API_KEY }}`.
The secret is never visible in workflow logs — GitHub masks it automatically.

## Manual enrichment (retroactive)

To enrich a deposit AFTER the fact (e.g., #935 the manifesto that just
landed without enrichment):

```bash
export ANTHROPIC_API_KEY='sk-ant-...'
python3 scripts/enrich_deposit.py --deposit-number 935 --all
python3 scripts/regenerate_surfaces.py
git add -A && git commit -m "Enrich AXN:03B2 (#935) retroactively"
git push
```

To enrich in non-LLM mode (SPXI audit + Wikidata + OpenAlex + DataCite +
backlinks only, no concept/citation extraction) — free, no API key needed:

```bash
python3 scripts/enrich_deposit.py --deposit-number 935 \
    --wikidata --openalex --datacite --spxi --backlinks
```

## Cost verification

The extraction step will print an actual usage receipt on each run:

```
[enrich] extracted concepts=12, citations=8, wikidata_candidates=6,
         cha_xrefs=3 (usage: 15234in / 2891out)
```

Sonnet 4.6 pricing (as of June 2026): $3 input / $15 output per MTok.
That run cost = 15234 × $3/M + 2891 × $15/M = $0.046 + $0.043 = **$0.089**

Haiku 4.5 ($1/$5) same run: $0.015 + $0.014 = **$0.029**

Set `ANTHROPIC_MODEL=claude-haiku-4-5-20251001` in env or workflow to
switch models. Sonnet recommended for concept/citation extraction where
nuance matters (Sophia's first deposit is a good case for Sonnet); Haiku
is fine for high-volume retroactive backfill.

## What each enrichment step produces

| Step | Populates in registry | Also writes |
|------|-----------------------|-------------|
| `--extract` (LLM) | `wiki_article`, `entities`, `defines_concepts`, `citations`, `wikidata_candidates`, `cha_cross_references` | — |
| `--wikidata` | Adds `wikidata_qid` etc. to `wikidata_candidates` entries | — |
| `--openalex` | `openalex_ids` (for the deposit itself) | Sidecar with cited work IDs |
| `--datacite` | `datacite_severance` status | Sidecar with per-DOI status |
| `--spxi` | `spxi_audit` full 5-layer audit report | — |
| `--backlinks` | Updates `cited_by` on other deposits | — |
| always | `references_concepts`, `references_concept_count` (lexical scan) | — |
| always | `external_metadata_path` pointing to sidecar | `data/external-metadata/AXN-XXXX.json` |

### SPXI Layer 1 anchor detection

Layer 1 counts as present when at least 3 of these anchor types appear in
body prose:

- ORCID string
- Creator name
- AXN prefix (e.g., `AXN:03B2`)
- Hex identifier as full AXN
- Sovereign ID (e.g., `EA-TACHYON-20260630`)
- Deposit date
- Deposit number phrase (`deposit #935`)
- Authorial position phrase (`authorial position`, `MANUS`, `operating as`)

This is more forgiving than a strict ORCID+creator gate, matching the
SPXI v0.2 spec that anchors should be redundant, prose-embedded, and
survive standard preprocessing.

### Wiki article inscription

The wiki_article template now inscribes AXN and deposit number visibly:

    "[title]" is a X-word [type] by [creator], dated [date]. It is
    registered as [AXN] (deposit #[N]) in the Crimson Hexagonal Archive
    under the [FAMILY] semantic family. [description]. [concepts].

This means Sigil surfaces AXN + basic metadata whenever it retrieves the
wiki entry — the reader gets the archival coordinates automatically.

## What each enrichment step produces (summary)

## Behavior with Sophia's deposit

When Sophia submits her first deposit through the form, the workflow will:

1. Validate + mint the base entry (as before)
2. Extract concepts + citations + Wikidata candidates + CHA cross-references
   via Sonnet 4.6 (~$0.05-0.10 spent from your key)
3. Resolve Wikidata QIDs for named entities
4. Fetch OpenAlex work IDs for her deposit and its citations
5. Check DataCite severance for cited DOIs
6. Audit her deposit against the SPXI 5-layer protocol
7. Populate cross-references (SPXI Layer 4) prospectively; update
   `cited_by` on referenced deposits retrospectively
8. Regenerate the wiki, graph, browse, and record pages
9. Commit + auto-merge

Her deposit appears on the main page cards as a fully-enriched entry
with wiki article, entity graph, cross-references, and external metadata
sidecar — the "minted deposit" state you specified.
