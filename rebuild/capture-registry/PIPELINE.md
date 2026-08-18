# Capture intake — the pipeline, and the two modes

One path from a screenshot to a visible, citable entry. Everything here is a
committed script; nothing depends on a session container.

**Read `reading_canon` in `data/EA-WG-CAPTURES-01.json` before writing anything.**
Six seated records, each teaching one thing a new instance otherwise gets wrong.
They are not a template to fill. They are records to read.

---

## THERE ARE TWO MODES AND ONLY ONE OF THEM IS DANGEROUS

**INTAKE** adds an observation that did not exist. On 2026-08-13, forty captures
were seated across four sittings and intake broke nothing, twice.

**REPAIR** touches a record that already exists. On the same day, four repairs
broke the dataset — a projector that reintroduced doubling the projection had
already fixed, a schema reseat in a shape 406 records do not use, six cards
rendered blank, and a correct citation note destroyed by a "correction."

*Every destructive act was a fix.* If you are about to improve something, you are
in the dangerous mode. The posture below is not optional there.

### Before touching an existing record

1. **State what you believe is broken, and the evidence for it.** In the commit
   message, before the change. "The doubling is structural" was written in commit
   `3674bca6` and quoted back four rounds before it was reintroduced — stating
   the belief out loud is what surfaces the contradiction.
2. **Search the archive against that belief.** `data/registry.json` is on disk.
   A relation asserted without checking is a guess wearing a finding's clothes —
   and so is a relation *retracted* without checking. Both happened on
   2026-08-13, in the same week, over the same SoundCloud card.
3. **One operation per commit.** Never mix intake with repair. This is the only
   property that saved the dataset when a revert was called: the revert was clean
   because the commits were separable.
4. **Verify against the artifact a person sees**, not the data. Two of the four
   failures existed only in the rendered page; the JSON looked correct at every
   level checked. Then state what you did *not* verify.

---

## 0. Capture

**One image: the collapsed AI Overview popup.** Expansion adds only text already
in the transcript, the citation card row is a sideways scroller no frame can
hold, and the collapsed frame is the *only* artifact that positively establishes
Overview.

**Surface discriminator (operator finding, 2026-08-13):** AI Mode **selects the
AI Mode tab**. An expanded Overview adopts AI Mode chrome *without* selecting it.
Every AI Mode determination made before this rested on an `AI Mode Conversation`
paste marker, which is copy-paste residue and not a surface signal — 150
observations were mislabelled that way.

## 1. Author the capture record

`rebuild/capture-registry/intake-YYYYMMDD/capture-NN.json`.

**Authored, per capture** — transcript cleaning and presentation, analysis,
finding. This registry collects data *and* curates artifacts.

**Mechanical, with a refusal gate** — citations, routing, slug, ids, defects, PER
proposal, fingerprint. `scripts/extract_cards.py` **proposes** the citation
cards; the count is authored against the frame. Unknown site names refuse rather
than drop.

## 2. Gate

    python3 scripts/capture_intake.py rebuild/capture-registry/intake-*/capture-NN.json

ADMIT (transcript, date, surface, both auth dimensions) → ROUTE (exact issued
string, **quotation marks significant**) → NORMALISE → EMIT.

## 3. Seat

Append to `data/EA-WG-CAPTURES-01.json` in the shape the corpus already uses.
Recaptures append to an existing entry's `observations`; they do not mint a
second card. See `scripts/seat_20260813_2248.py` for the form.

**Ratified as doctrine, 2026-08-17 (MANUS):** this step names the canonical
store. `data/EA-WG-CAPTURES-01.json` is the single writable authority; the
rebuild store is sealed as the rebuild-era source. See `_authority` in the
canonical file.

## 4. Render and gate

    python3 scripts/build_capture_gallery.py
    node   scripts/check_gallery_js.js          # executes the page scripts
    python3 scripts/check_render_determinism.py # two builds, byte-identical

`node --check` is a syntax check and passed for a full day while the page was
broken. The runtime gate exists because of that day.

## 5. Commit ONCE

One commit, one push, one deploy. Vercel deploy limits are real.

**Attach the familiarization receipt** from
`python3 scripts/bootstrap_familiarization.py --strict --instance "<label>"`.
It was not attached to any of the eleven commits made on 2026-08-13, and the
gate that would have caught the drift was walked past because nothing in the
path made the instance meet it.

---

## Rules that cost something to learn

**The address is the exact issued string.** Quoted and unquoted are different
addresses, and the difference is measurable in both directions: `"the network is
the poem"` quoted returns Zenodo and CERN and no author, unquoted names Sharks;
but `"composition layer" "entity substitution"` fully quoted names nobody, and
loosening one pair of quotes names both parties. The effect is not a property of
quotation — it is which basin the exact string lands in.

**Auth is two dimensions and is never inferred.** A blanket date rule assigned
"signed in" to 161 observations and destroyed the only authentication-controlled
pair in the corpus. Frames can corroborate authentication; **no frame can show
incognito** — that half rests on attestation, and the record says so.

**Surface is not read off the paste.** See the discriminator above.

**NULL is never zero.** An apparatus not captured has an unknown count. A
transcript that returned without its sources is a *false positive*, not a
citations-null observation — see `_excluded_20260813_2248`.

**A filename is not an image.** Six addresses looked promotable because a bare
filename sat in the record; no file existed anywhere in the fleet.

**A section of one is not a section.** A capture carried section `Archive`, the
only card of 300 in it, and vanished under every filter state but one.

**Conservation is a partition test, not a concatenation compare.** Extraction
reorders. And conservation proves nothing was *lost* — never that boundaries were
placed right. A card split in two conserves every character.

**One capture, counted once.** Fifteen observations were byte-identical
transcripts on the same date, seated twice. Withdrawn, not deleted.

**OCR is retroactive cleanup, not a forward-looking concern.** No future capture
will be OCR-read. 122 transcripts still carry OCR chrome.
