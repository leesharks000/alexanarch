#!/usr/bin/env python3
"""build_review_report.py — export the link inventory to reviewable artifacts.

Outputs:
  /mnt/user-data/outputs/LINK-REVIEW-2026-07-08-summary.md
  /mnt/user-data/outputs/LINK-REVIEW-2026-07-08-actionable.csv
  /mnt/user-data/outputs/LINK-REVIEW-2026-07-08-ambiguous.csv
"""
import sqlite3, csv, json, re
from pathlib import Path

DB = Path('/tmp/linkscan/links_review.db')
OUT = Path('/mnt/user-data/outputs')
OUT.mkdir(parents=True, exist_ok=True)

conn = sqlite3.connect(DB)
cur = conn.cursor()

def q(sql, args=()):
    return cur.execute(sql, args).fetchall()

# ---- Summary MD ------------------------------------------------------

total = q('SELECT COUNT(*) FROM links')[0][0]
by_verdict = q('SELECT verdict, COUNT(*) FROM links GROUP BY verdict ORDER BY COUNT(*) DESC')
by_repo = q('''
    SELECT repo, COUNT(*) FROM links GROUP BY repo ORDER BY COUNT(*) DESC
''')
n_with_doi = q('SELECT COUNT(*) FROM links WHERE doi_in_text IS NOT NULL OR doi_in_href IS NOT NULL')[0][0]
mismatch_verdicts = ('href_wrong_target', 'href_disagrees_resolver', 'href_disagrees_text', 'likely_prose_mismatch')
n_mismatch = q(f'''
    SELECT COUNT(*) FROM links WHERE verdict IN ({",".join("?"*len(mismatch_verdicts))})
''', mismatch_verdicts)[0][0]
n_ambig = q('SELECT COUNT(*) FROM links WHERE verdict="ambiguous"')[0][0]

# Concentrated repos
by_repo_mismatch = q(f'''
    SELECT repo, COUNT(*) FROM links WHERE verdict IN ({",".join("?"*len(mismatch_verdicts))})
    GROUP BY repo ORDER BY COUNT(*) DESC
''', mismatch_verdicts)

# Ambiguous with high-value alt suggestions
n_ambig_promising = q('''
    SELECT COUNT(*) FROM links WHERE verdict="ambiguous"
    AND doi_in_text IS NOT NULL
    AND best_alt_jaccard >= 0.15
    AND (prose_vs_resolver_jaccard IS NULL OR prose_vs_resolver_jaccard < best_alt_jaccard)
''')[0][0]

md = f'''# Link Review Database — 2026-07-08

**Total anchored links scanned across the network:** {total:,} (across 34 repos)
**Links carrying a DOI:** {n_with_doi:,}
**Links with actionable mismatch verdict:** {n_mismatch:,}
**Links flagged ambiguous:** {n_ambig:,} (of which {n_ambig_promising:,} have a promising alternative record suggestion)

The full per-link inventory is in `/tmp/linkscan/links_review.db` (SQLite, 81 MB).
Two exportable CSVs accompany this MD for offline review:

- `LINK-REVIEW-2026-07-08-actionable.csv` — {n_mismatch:,} rows, high-confidence mismatches
- `LINK-REVIEW-2026-07-08-ambiguous.csv` — {n_ambig_promising:,} rows, DOI-carrying ambiguous links with a promising alt

## Verdict distribution

| verdict | count | meaning |
|---|---:|---|
'''

verdict_meanings = {
    'no_id': 'no DOI/AXN anywhere; navigation or other non-citation link',
    'ambiguous': 'DOI present but prose context matches resolver title only weakly; may or may not be a mismatch',
    'consistent': 'DOI in text matches DOI in href; or link is internally consistent',
    'href_disagrees_resolver': 'href points at record N; resolver says DOI in text should go to record M ≠ N',
    'external_ok': 'link points at external resource (doi.org, zenodo.org, non-network site) — passthrough, not checked',
    'href_wrong_target': 'href points at `/s/records/0/` sentinel — always wrong, needs the DOI to resolve elsewhere',
    'unknown': 'edge case, unclassified',
    'likely_prose_mismatch': 'prose context very different from what resolver says the DOI is, AND a much better alt record exists — probable wrong DOI or wrong mapping',
    'ok': 'strong jaccard match between prose and resolver title',
}
for v, n in by_verdict:
    md += f'| `{v}` | {n:,} | {verdict_meanings.get(v,"")} |\n'

md += f'''
## Mismatches concentrated in these repos

| repo | actionable mismatches |
|---|---:|
'''
for r, n in by_repo_mismatch:
    md += f'| `{r}` | {n} |\n'

# ---- The Generative Monoculture worked example ---------------------
md += '''
## Worked example — the "Generative Monoculture goes to Meaning Caste" case

MANUS flagged `lagrange-observatory/index.html:250` — anchor text `DOI 10.5281/zenodo.20675438` next to prose about "Generative Monoculture: Model Collapse in Code" — but that DOI resolves to record #198 "The Self-Audit Module Dissolved". The actual "Generative Monoculture" work is at record #199 (Talos Morrow, June 13 2026) or the re-mint at #1023 (EA-UMBML-MONOCULTURE-01).

**Two possible root causes:**

1. **DOI in the lagrange source HTML is wrong for the work described** — someone hardcoded `20675438` in the anchor text when the actual DOI for "Generative Monoculture" is different (potentially `20675440` version-later, or a distinct mint entirely).
2. **Resolver's `20675438 → #198` mapping is wrong** — Phase 6/7 fuzzy title matching may have landed the wrong record for this DOI.

The inventory can't decide between (1) and (2) mechanically — it needs a human judgment about whether the DOI in text is authoritative or whether the descriptive prose is. Both need a MANUS-level decision.

## Recommended review process

1. **Start with `actionable.csv`** — {n_mismatch:,} rows sorted by repo. Each row has file:line, anchor text, prose context, current href, extracted DOI, resolver's title, best alternative record, jaccard scores.
2. **Then `ambiguous.csv`** — {n_ambig_promising:,} rows filtered to cases with a promising alt.
3. Mark each row as: `keep_href` / `use_alt_record` / `update_resolver_mapping` / `remove_link` / `investigate`.
4. Report the corrections back and I apply them in a single controlled pass (fixing the source repos AND, where needed, the resolver map at the source of truth) — rather than another blanket rewrite.

## Rollback status of the last rewrite pass

The 2,377-rewrite anchor-text pass I ran before this inventory was built is still live on origin/main across 23 repos. Recommended before further deploys:

- **Deployed already** (per MANUS): `alexanarch` (link rewrites v1, /go/, v3.11.0), `lagrange-observatory` (semantic pass)
- **Not yet deployed**: everything else in the 23-repo pass

If MANUS wants a rollback pass across the 23 repos to restore pre-Phase-10-semantic state pending review, I can do that in a single script call. Otherwise, since the /go/ endpoint faithfully preserves whatever DOI was in the anchor text at rewrite time, the current state is a lateral move (no new mismatches introduced, just the pre-existing DOI-in-text mismatches now route through /go/ instead of pointing at sentinel 0 or stale records).
'''

# Try to render the "Two possible root causes" numbers correctly (Python f-strings don't work here)
md = md.replace('{n_mismatch:,}', f'{n_mismatch:,}').replace('{n_ambig_promising:,}', f'{n_ambig_promising:,}')

(OUT / 'LINK-REVIEW-2026-07-08-summary.md').write_text(md)
print(f'wrote {OUT / "LINK-REVIEW-2026-07-08-summary.md"}')

# ---- Actionable CSV -------------------------------------------------
COLS_ACTIONABLE = ('repo', 'file_path', 'line_no', 'link_form',
                   'anchor_text', 'href', 'context_before', 'context_after',
                   'doi_in_text', 'doi_in_href', 'href_record_num',
                   'resolver_doi', 'resolver_target', 'resolver_record', 'resolver_title',
                   'best_alt_record', 'best_alt_title',
                   'prose_vs_resolver_jaccard', 'best_alt_jaccard',
                   'verdict', 'verdict_confidence')

with open(OUT / 'LINK-REVIEW-2026-07-08-actionable.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(COLS_ACTIONABLE)
    rows = q(f'''
        SELECT {",".join(COLS_ACTIONABLE)}
        FROM links WHERE verdict IN ({",".join("?"*len(mismatch_verdicts))})
        ORDER BY repo, file_path, line_no
    ''', mismatch_verdicts)
    for r in rows:
        # Trim context / anchor to CSV-friendly lengths
        r = list(r)
        for i in (4, 5):     # anchor, href
            if r[i]: r[i] = r[i][:200]
        for i in (6, 7):     # context
            if r[i]: r[i] = r[i][:150]
        w.writerow(r)
print(f'wrote {OUT / "LINK-REVIEW-2026-07-08-actionable.csv"} ({len(rows):,} rows)')

# ---- Ambiguous-with-promising-alt CSV --------------------------------
with open(OUT / 'LINK-REVIEW-2026-07-08-ambiguous.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(COLS_ACTIONABLE)
    rows = q(f'''
        SELECT {",".join(COLS_ACTIONABLE)}
        FROM links WHERE verdict="ambiguous"
          AND doi_in_text IS NOT NULL
          AND best_alt_jaccard >= 0.15
          AND (prose_vs_resolver_jaccard IS NULL OR prose_vs_resolver_jaccard < best_alt_jaccard)
        ORDER BY best_alt_jaccard DESC, repo
        LIMIT 2000
    ''')
    for r in rows:
        r = list(r)
        for i in (4, 5):
            if r[i]: r[i] = r[i][:200]
        for i in (6, 7):
            if r[i]: r[i] = r[i][:150]
        w.writerow(r)
print(f'wrote {OUT / "LINK-REVIEW-2026-07-08-ambiguous.csv"} ({len(rows):,} rows)')
print('\ndone.')
