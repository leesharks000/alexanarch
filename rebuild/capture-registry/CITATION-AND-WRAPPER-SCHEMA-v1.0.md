# Citation layer, formal wrapper, and intake division of labour — v1.0

Drafted 2026-08-13 against the twenty-capture batch of the same date. Every rule
is either a defect this registry sustained or a constraint one of the four
downstream consumers imposes.

## Ruling this implements

> "clean lineation, formatting, and citation structure can absolutely be
> retroactively granted without demoting canonical status. that's a formal
> wrapper for care-attendance and beauty of object. faithful semantic content
> is canonical." — MANUS, 2026-08-13

The clipboard is lossy in **form**, not in semantic content. `transcript` holds
the cleaned text and remains canonical. The raw paste is retained beside it as
`source_transcription`, so what was cut stays answerable.

## Division of labour

This registry collects data **and** curates artifacts. The second is not
decoration; it is why a reader can attend to the object at all. But authoring
must be spent where judgment is required and nowhere else.

**Authored, per capture** — transcript cleaning and presentation, analysis,
finding.

**Mechanical, with a refusal gate** — citation extraction, routing, slug and
ids, defect vector, PER proposal, fingerprint, emit. A script that meets input
it cannot classify **refuses the capture**; it never swallows it.

PER is proposed by string test against controlled lists — Sharks and the twelve
heteronyms; CHA / Alexanarch / SEI; AXN and DOI patterns; archive-controlled
domains — and confirmed or overridden by hand. Proposal is mechanical;
adjudication is not.

## Capture protocol (2026-08-13 forward)

**One image: the collapsed Overview popup.** Expansion adds only text already in
the transcript, and the citation card row is a sideways scroller no single frame
can hold. The collapsed frame is also the *only* artifact that positively
establishes Overview — nothing in an expanded frame does.

## Additive only

Three of four nodes render the projection they fetch; only alexanarch builds it.
A changed key breaks whoever lags; an added key is ignored. `cite_list` keeps
`n, site, rel, title, snip, url, note`; `cites` stays the integer count and must
equal `len(cite_list)`; `rel` keeps its closed four-value **provenance**
vocabulary — `third_party`, `authored_surface`, `archive_controlled`,
`authority_transfer` — and is not overloaded with a support relation, a
different axis. Added: `date_shown`, and `display.overflow_label` for the `+N`
chip, recorded rather than discarded.

## No inline citation layer

Withdrawn. Inline chips are clickable popups, so position is unrecoverable from
a frame; and the paste collapses every chip to the tail block regardless. In all
twenty captures of 2026-08-13 not one chip sits mid-prose. **Cards only.** No
`layer`, `anchored`, or `anchor` field exists — an apparatus that can never be
populated is worse than absent, because it implies the corpus measured something
it did not.

## The formal wrapper

```
transcript_wrapper: {
  status:     "granted" | "pending",
  granted:    "YYYY-MM-DD",  granted_by: "TACHYON",
  operations: ["lineation restored", "cards extracted",
               "query echo removed", "chrome discarded"],
  conservation: { ... }
}
```

`pending` is a work queue, not a demotion. The 386 seated transcripts await a
wrapper; they are not disqualified for lacking one.

## Conservation — how the wrapper proves it took nothing

**A partition test, not a concatenation compare.** The first draft concatenated
cleaned + citations + discards and compared to source; it failed on a capture
that conserved every character, because extraction *reorders* — the card layer
leaves the prose run and arrives in a list. Two tests, both required:

1. **Partition** — each cleaned, citation and discard span is located in the
   source and consumed once. What remains unconsumed is residue.
2. **Multiset** — word-character counts of source and of all parts are equal.

`residue_unclassified > 0` **refuses the capture**. Closed vocabulary, not a
regex that eats what it does not recognise — *twelve failure modes, not extended
by invention*.

## Discard vocabulary (closed)

| class | what it is |
|---|---|
| `chrome.query_echo` | `AI Mode Conversation` / `You said:` and the duplicated query |
| `chrome.show_more` | the expansion control |
| `chrome.disclaimer` | *AI can make mistakes, so double-check responses* |
| `chrome.followup_prompt` | *Ask anything* |
| `chrome.separator` | `$` and stray run-together glyphs |
| `chrome.overflow_chip` | `+3`, `+12` — moved to `display.overflow_label`, not lost |
| `serp.organic_result` | **see below — post-change captures only** |

Cards are **moved**, never discarded: they leave the transcript, arrive in
`cite_list`, and their characters count as `citation_chars`.

`AI Mode Conversation` is discardable chrome and **not a surface signal**. All
twenty captures of 2026-08-13 carry it; all twenty are confirmed Overview.

## The render change — a dated hazard

Google altered the Overview render after this batch. Two effects:

**Expansion no longer converts to AI Mode.** The confound that produced 150
mislabelled observations ends at the change date. Captures after it are
unambiguous.

**Select-all now takes organic results with it.** Future pastes will carry SERP
text that is *not composition-layer output*, run together with text that is.
Seated unchallenged, the registry would begin measuring Google's organic index
as though it were the summarizer. `serp.organic_result` must be detected and
discarded, and **a parser tuned for pre-change pastes will silently admit
post-change contamination** — so the class is dated, not universal.

**Boundary: after 2026-08-13 16:48 EDT.** Established on `alexanarch:classics`,
whose frame shows `alexanderclassiccars.com` as the top organic result while the
paste's source list contains no such entry. Organic results were not being taken
as of that minute. This batch is the last clean set under the old behaviour and
is therefore the calibration corpus. Resolution of the new constraint is
deferred to the rerun batch.

## Display image

Inherited from the **address**, not from whichever observation the entry was
built on; most recent imaged observation wins. `alexanarch` displays "no image"
while holding three observations — the address-level display never looks down.

**A filename is not an image.** Six addresses appeared promotable without a
rerun; every one carries `resolved: false`, `repo_path: null`, and a bare
filename matching no file in any of the four repositories. The count of
promotable-today is **zero**, and all 115 image-less entries are rerun
candidates. Verification is content-match, never the presence of a reference.

## Downstream contract

`mark_inline_cites()` needs no change — with the inline layer withdrawn it finds
nothing and is idempotent by construction.

`split_source_strip()` must be **skipped where the wrapper is granted**. Against
cleaned text it normally finds nothing, but its guard 3 protects only titles
occurring in the first 40%, so a body quoting a cited title late remains
cuttable — `"the network is the poem"` is exactly that shape.

```python
if (e.get("transcript_wrapper") or {}).get("status") == "granted":
    answer, strip = tr, ""
else:
    answer, strip = split_source_strip(tr, cites)
```

Degradation is safe: a lagging node renders cleaned text through the old path
and, but for the quoted-title case, gets the same output.

`check_fleet_sync.py` compares `version` and `address_count`; both move when the
campaign changes either.

## Order of operations

Canonical is the only writable authority. The wrapper is applied at intake. The
projector carries and reshapes; **it never cleans**. That keeps reproduction-diff
a valid test of the projector, because nothing downstream may alter content.
