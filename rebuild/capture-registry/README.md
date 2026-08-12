# Capture Registry — rebuild in progress

The published registry was withdrawn 2026-08-12 (see `quarantine/capture-registry-20260812/`).
This directory holds the reconstruction. Everything here is permanent and in git; nothing
depends on a session container.

## Files

| file | what it is |
|---|---|
| `EA-WG-CAPTURES-01-REBUILD.json` | THE WORKING REBUILD. 289 addresses, 303 observations. Every value provenanced to its source, version and blob. |
| `EA-WG-CAPTURES-UNIFIED-SCHEMA-v1.0-draft.json` | The schema: all 74 fields ever observed across every registry version, mapped, with eight reconciliation problems flagged. |
| `EA-WG-CAPTURES-01-EMPTY-v3.3.json` | The empty skeleton the rebuild was seated into — addresses only, no content. |
| `PALETTE-SURVEY.json` | What the four-source harvest found, before any repair. |
| `gallery-html-harvest.json` | The pre-JSON registry versions recovered from `captures/index.html` history (galleries of 21→80 entries). |
| `RECOVERED-PASTE-20260811-batch.txt` | The 62,508-character MANUS paste of the 19-capture batch, recovered from a session transcript. Source of 18 seated transcripts. |

## Scripts (in `scripts/`)

- `harvest_palette.py` — rebuilds the palette database from the four repositories' full histories.
- `harvest_gallery_html.py` — recovers capture entries from the gallery HTML era.
- `seat_source.py` — seats one source into the rebuild, with a ledger. Carries the routing rules in its own source.

## The palette database

`palette/capture-palette.sqlite` (151 MB) is NOT committed — it is rebuildable in minutes by
running `scripts/harvest_palette.py` against clones of the four repositories:
alexanarch, leesharks.com, godkinggoogle, machinemediation-org. It holds every version of every
capture-bearing file: 138 registry versions, 330,530 field observations, 316 capture keys,
55 companion/manifest file versions, across 3,235 commits.

## Where the images are

Images are locatable addresses, never embedded data. The registry stores a path or URL; the
files live in the repositories:

    alexanarch            data/captures/{slug}/          442 images, 187 directories
    godkinggoogle         captures/                      261 images
    leesharks.com         captures/                      263 images
    machinemediation-org  data/captures/{dir}/            37 images

## State as of 2026-08-12

- 289 addresses, 303 observations, seated by semantic address = (query as issued, surface), longitudinal across time.
- 61 transcripts in `machine_output`, EVERY ONE read in full before seating.
- 241 observations have no machine output. Their text does not exist in any registry field, in any
  version, in any of the four sources. It survives only in the capture images, in the Claude threads
  where MANUS pasted it, or nowhere.
- The registry's own text fields are exhausted: a sweep of all 242 transcript-less captures against
  nine transcript signals returned two candidates, and reading both showed neither qualified.

## Standing rules

1. NO TRANSCRIPT IS SEATED WITHOUT BEING FULLY READ. (MANUS, 2026-08-12)
2. MARKER-DATE GATE: a transcript declared by a marker may only be seated where the marker's date
   matches the capture date. Eight records failed this and were unseated.
3. Analysis containing quoted text is ANALYSIS. Quotations are marked inside it and never promoted.
4. Only a value whose provenance establishes a capture-time verbatim record may enter `machine_output`.
5. The withdrawn passes' `transcript`, `meta` and `transcript_status` fields are never seated.

## Marker conventions found (five)

    Full AI Mode transcript (DATE):
    FULL AI MODE TRANSCRIPT (DATE), as supplied by MANUS:
    **TRANSCRIPT (surface, DATE, authentication state)**
    FULL AI MODE SEQUENCE (DATE), N turns, as supplied by MANUS
    raw paste — "AI Mode Conversation" / "You said:" echo
