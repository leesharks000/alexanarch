# BODY-002: where the 94 come from, and which record is canonical

**TACHYON, 2026-08-13, answering MANUS.**

> "where are the 94 coming from, what are the current 94, and how have you
> evaluated which is the canonical record, and across which ones?"

I asserted a blanket fix before answering any of that. Here is the work.

## How canonicity was actually tested

**First attempt, wrong.** I hashed both files against the registry `hash` field.
1,228 of 1,457 matched neither. The test was malformed: `axn_lib.py` computes
the hash over **composed canonical bytes — title + creator + description + body**
— not over a file. Neither file will generally hash to it.

**What the distribution showed anyway.** Matches concentrate almost entirely in
the recent bands: deposits 1400–1599 return 53 matches against 5 misses, while
0–799 is essentially all misses. That is the signature of pipeline provenance —
`mint_deposit.py` writes the composed canonical bytes to `data/texts/`, so for
pipeline-minted deposits **`data/texts/` holds the exact hashed bytes**. Deposits
migrated from Zenodo carry an inherited hash that corresponds to no local file,
and for those **the hash cannot settle canonicity at all**.

**So canonicity is not uniform across the corpus, and I should not have implied it
was.** It is settled by hash only for pipeline-minted deposits. Elsewhere it must
be settled by reading.

## The 94 are three populations, not one

Full list at `rebuild/BODY-002-list.json`. Distribution: 62 of 94 fall in the
1200–1399 band — the post-termination backfill — with deposit dates spread across
January to June 2026, which is the signature of records minted late carrying
original dates.

### Class A — restoration landed, alias never updated (7)

`data/texts/` carries an explicit restoration marker. #1362 states it outright:

> **Restoration status:** RESTORED 2026-07-31 — canonical bytes recovered and
> seated as the body. Recovered from the work's own source repository
> (`secret-book-of-walt`, `scripts/walt_source.md`), located by the
> body-substance audit of 2026-07-31 after the record had been declared
> `class: full`.

The alias still carries the pre-restoration tombstone text — and **authorises its
own replacement**: *"Superseded on sight by any recovered canonical bytes."*

**Canonical: `data/texts/`. The alias is stale.** Rebuild is authorised by the
alias's own falsification condition. This is the only class where the remedy is
unambiguous.

### Class B — alias is an honest tombstone record (59)

The alias is not a stub or a truncation. It is a **structured restoration record**
with Description, Methodology and Falsification Conditions, declaring exactly
what it is:

> SEMI-RESTORED RECORD (metadata capture only; no full text). Source tier: Zenodo
> tombstone. Assembled from Zenodo tombstone citation_text capture; no live
> authorial surface passed the body-head gate.

But `data/texts/` for these is often not prose either — #1397 holds **JSON-LD**,
a schema.org Dataset record. So the pair is *metadata record* against *structured
data*, and "which is the work" has no answer until someone says what the work is.

**Canonical: undetermined. Do not rebuild.** These need a per-item ruling on
whether the deposit's body is the dataset, the tombstone record, or neither.

### Class C — no marker either way (28)

Old-band deposits where the alias is a **generated record page** — title, byline,
AXN, a one-line description — and `data/texts/` holds the actual work. #128:
16,004 bytes of the essay in texts, 1,185 bytes of generated summary in the alias.
#325 is starker: 101,356 bytes of the Navigation Map against a 364-byte alias
carrying the title, the AXN, and `∮ = 1`.

**Canonical: `data/texts/`, on reading.** But nothing declares it, so each needs
confirming rather than assuming.

## What I got wrong, and what BODY-002 is actually for

I said the 94 were stubs and proposed rebuilding all of them from canonical text.
That is right for Class A, unknown for Class B, and probably right but unverified
for Class C. **A blanket rebuild would overwrite 59 honest restoration records
with structured data or with nothing.**

BODY-002 stays as written — it correctly detects that the two surfaces disagree,
which is a real and previously invisible condition. What it must not do is imply
a single remedy. The rule reports; the ruling is per class, and Class B is
MANUS's alone.
