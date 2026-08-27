# Capture Registry — intake and normalization contract

Set by MANUS, 2026-08-13. Every rule below is a defect this registry actually
sustained, not a precaution against a hypothetical one.

## Data in

A new capture is **not seated** unless it carries all four:

| field | why |
|---|---|
| `transcript` | 20 observations carried claims with **no evidence at all**. A capture without machine text is an assertion. |
| `date` | 5 carried the **string `"null"`** as a date, breaking every longitudinal comparison silently. `YYYY-MM-DD`, Michigan local. |
| `surface` | 60 sat at `UNRESOLVED` and could not be re-run, compared across surfaces, or counted by layer. |
| `auth.authenticated` **and** `auth.incognito` | A blanket date rule assigned "signed in" to 161 observations and **destroyed the corpus's only authentication-controlled pair**. Two independent dimensions; never inferred. |

## Routing

The address key is the **exact issued string**, NFC-normalised and trimmed, and
nothing else. Case preserved, punctuation preserved, **quotation marks preserved**.

- **Exact match** → the capture is an **observation of that record**, not a new capture.
- **No match** → a **new record**.

**Quoted and unquoted are different addresses.** `«operative semiotics»` held 5 of
5 archive cards quoted and 1 of 8 unquoted, and by 13 August resolved *only* under
the exact-phrase operator. Folding the two forms together would erase the
decisive measured variable in the corpus.

Sub-rounds are never captures. A round is a turn within one sitting where the
operator changed the query and said so — *"I modified to"*, *"I retired with"*. A
bare label naming the next query is a **separator between captures**, not a pivot.

## Normalization

The same derivations, by the same functions, on every capture: defects from the
controlled list; PER as a **four-unit vector** with the scalar as its projection;
citations relation-typed; the source strip split only under three guards; OCR
reflowed for reading with **every word character preserved**.

Twelve failure modes. **Not extended by invention.**

## Data out

One writable authority: `rebuild/capture-registry/EA-WG-CAPTURES-01-REBUILD.json`.
Everything else — the public projection, the gallery, the links file, the semantic
addresses, the mirror — is **derived and says so**. Nothing writes back.

Three gates run on every build:

- `check_gallery_js.js` — executes the page's scripts against a stub DOM. `node --check` is a *syntax* check and passed for a full day while the page was broken.
- `check_render_determinism.py` — builds twice and compares bytes. A registry whose public surface changes without its data changing cannot support a longitudinal claim.
- `capture_intake.py` — refuses a capture that cannot be read.

**NULL is never zero.** An apparatus not captured has an unknown count.
**Absence is a claim**, and a claim needs every place the thing could be.

## The mirror rule (added 2026-08-18, after the who-said half-seating)

An entry mirrors its primary observation at the top level, and THE GALLERY
RENDERS THE TOP. Every seating and every repair must therefore write BOTH
sides: the observation's fields and the entry-level mirror of the primary
observation (imgs, transcript fields, attestations, all of them). A seating
that updates one side of the mirror is half a seating; the files serve, the
audits pass, and the card shows nothing. Until the mirror-audit gate exists,
the closing step of any intake is to open the rebuilt gallery page and see
the images with your own eyes. Anchored is not shown.

---

## RULING — THE SEAT IS THE TAB (MANUS, 2026-08-27)

The canonical rendered surface of the Capture Registry is the captures tab:
https://www.alexanarch.org/captures/. A capture is seated when, and only when,
that page carries its card. Authoring the entry into data/EA-WG-CAPTURES-01.json
and syncing datasets/capture-registry/ is authoring, not seating — the tab is a
baked static page and does not follow the data file.

SPLITBRAIN RECORD (2026-08-27, third occurrence of the 2026-08-15 shape):
entry authored, projection synced, pushed, projection verified live — tab stale
at 371/372. Contributing drift found and repaired in the same session:
cite_list authored as strings where the renderer requires {site,title,snip}
dicts (the bake crashed invisibly and kept its previous bytes); entry lacked
the section field `s`; top-level address_count stale at 360 for twelve seats.

CLOSURE: scripts/seat_capture_postflight.py chains BAKE → GATE → SYNC and
refuses at the first failure. It runs after every registry write. Exit 0 is
the definition of seated; a non-zero exit is a seat that must not be pushed.

SECOND DRIFT VECTOR FOUND (2026-08-27, on the v11.6 seat): the registry carries
TWO declared counts — `address_count` and `total_captures` — and
sync_capture_dataset.py prefers the latter over len(entries). address_count was
updated on the seat and total_captures was not, so the chain passed its gate and
the projection still announced 372 for a 373-entry registry. Both declared counts
are now checked by check_capture_page_current.py. A count that some consumer
prefers is a count the gate must hold.
