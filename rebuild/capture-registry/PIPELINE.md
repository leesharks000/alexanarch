# Capture intake — the pipeline, end to end

One path from a screenshot to a visible, citable entry. Every step is a
committed script; nothing depends on a session container. Run them in order.

## 0. Capture

**One image: the collapsed AI Overview popup.** Expansion adds only text already
in the transcript, the citation card row is a sideways scroller no frame can
hold, and the collapsed frame is the *only* artifact that positively establishes
Overview — nothing in an expanded frame does. Expanding used to convert the
surface to AI Mode chrome, which is how 150 observations came to carry a surface
label no image supports.

Commit the image, then paste the text.

## 1. Author the capture record

`rebuild/capture-registry/intake-YYYYMMDD/capture-NN.json`, built with
`author.py` in that directory.

**Authored, per capture** — transcript cleaning and presentation, analysis,
finding. This registry collects data *and* curates artifacts; the second is why
a reader can attend to the object at all.

**Mechanical, with a refusal gate** — citations, routing, slug, ids, defects,
PER proposal, fingerprint. `scripts/extract_cards.py` proposes the citation
cards; **the count is authored against the frame.** Four segmentation schemes
were tried and each fixed the failure in front of it while breaking one behind.
Conservation passed throughout — which is the point: it proves nothing was
*lost*, never that boundaries were placed right. A card split in two conserves
every character.

Unknown site names **refuse** rather than drop. Add them to
`intake-YYYYMMDD/lexicon-additions.json` with the capture that surfaced them.

## 2. Gate

    python3 scripts/capture_intake.py rebuild/capture-registry/intake-*/capture-NN.json

ADMIT (transcript, date, surface, both auth dimensions) → ROUTE (exact issued
string, **quotation marks significant**) → NORMALISE → EMIT. Refuses rather than
seating a record that cannot be read.

## 3. Seat into canonical

Canonical is `rebuild/capture-registry/EA-WG-CAPTURES-01-REBUILD.json` and is the
**only** writable authority. See `scripts/seat_batch_20260813.py` for the form.

## 4. Project

    python3 scripts/project_captures.py --verify    # carry-layer diff, writes nothing
    python3 scripts/project_captures.py --write

Carry, reshape, emit. **It never cleans.** The previous builder collapsed
whitespace in transcripts at projection time — a cleaning step invisible until a
reproduction diff went looking for it. Cleaning belongs at intake, by hand.

`--verify` rebuilds the *published* projection from canonical and compares only
carried fields. Every difference is a known reclassification or a bug.

## 5. Render and gate

    python3 scripts/build_capture_gallery.py
    node   scripts/check_gallery_js.js          # executes the page scripts
    python3 scripts/check_render_determinism.py # two builds, byte-identical
    python3 scripts/check_fleet_sync.py         # no node may diverge from canonical

`node --check` is a syntax check and passed for a full day while the page was
broken. The runtime gate exists because of that day.

## 6. Commit ONCE

One commit, one push, one deploy. Vercel deploy limits are real and every push
spends one.

---

## Rules that cost something to learn

**The address is the exact issued string.** NFC-normalised, trimmed, nothing
else. Quoted and unquoted are different addresses: `"the network is the poem"`
returns Zenodo, CERN and no author; unquoted names Lee Sharks. Fold them
together and the corpus's decisive measured variable is gone.

**Auth is two dimensions and is never inferred.** A blanket date rule assigned
"signed in" to 161 observations and destroyed the only authentication-controlled
pair in the corpus.

**Surface is not inferred from the paste.** The `AI Mode Conversation` header is
copy-paste residue from an expanded Overview, not a surface signal.

**NULL is never zero.** An apparatus not captured has an unknown count. Absence
is a claim, and a claim needs every place the thing could be.

**A filename is not an image.** Six addresses looked promotable because a bare
filename sat in the record; no file existed in any of the four repositories.

**A section of one is not a section.** A capture carried section `Archive`, the
only card of 300 in it, and was invisible under every filter state but one. The
projector will not mint a section outside the gallery's vocabulary.

**Conservation is a partition test, not a concatenation compare.** Extraction
reorders: the card layer leaves the prose run and arrives in a list. Locate each
span in the source, consume it once, then compare word-character multisets.
