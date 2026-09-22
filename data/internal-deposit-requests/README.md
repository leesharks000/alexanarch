# Internal deposit requests

This directory is the handoff surface for **Transport D sessions that can write
GitHub but cannot execute the repository locally**.

A request lives at:

```
data/internal-deposit-requests/<slug>/
  body.md
  packet.json
```

and is committed on branch:

```
internal-deposit/<slug>
```

Pushing that request triggers `.github/workflows/internal-deposit-bridge.yml`.

## body.md

The normal Alexanarch issue-body format consumed by
`scripts/validate_deposit.py` and `scripts/mint_deposit.py`. The full work
belongs in the Body field. This is transport, not an API submission.

## packet.json

In-session semantic work that the old direct-repo Transport D path expected the
operating model to write into the registry before the wiki/completeness stages.

Example:

```json
{
  "schema": "alexanarch-internal-session-packet/v1",
  "registry_patch": {
    "wiki_article": "A substantive article of at least sixty words...",
    "wiki_status": "in-session",
    "defines_concepts": [],
    "concepts_attested_none": true,
    "related_deposits": [1630],
    "related_attested_none": false,
    "entities": [],
    "entity_status": "in-session",
    "lexical_attested_none": true
  }
}
```

The packet cannot alter mint-owned identity fields. The normal completeness
gate still requires wiki substance, concepts-or-attested-none,
related-or-attested-none, lexical receipt-or-attested-none, citation edges,
render integrity, and declared files.

This bridge deliberately has **no model API key**. The already-running session
does the semantic work; GitHub Actions supplies only the missing shell.
