# The WHERE tab — build specification

**Status: one of twelve built.** `axnidentifiers.org/where/` is live and is the reference.

## What it is

A `/where/` page on each heteronym's own site, complementing that site's `/who/` card:
**the heteronym lives there, so their journal should too.** It shows the venue that
heteronym edits — not all eight.

## The binding rule, learned the hard way

**Build from the host site's own stylesheet and add no class it does not already use.**
The first attempt put journals and presses on alexanarch in Georgia serif on `#faf9f4`
with a crimson accent, against alexanarch's `--sans` on `#fafafa` with `--accent:#1a3a5c`
— and duplicated `datasets/journals/`, which already existed. Reverted the same day.

The reference page declares **zero inline `<style>`** and uses only classes present on
`who/cranes/index.html`: `body.flat`, `zone surface`, `rail`, `seal`, `wm`, `stations`,
`calib`, `plate d1/d2`, `plate-head`, `plate-no`, `plate-title`, `plate-state`,
`plate-sub`, `overview`, `eco`, `ecorow`, `name`, `what`, `axn-chip`.

## The four plates

| plate | carries |
|---|---|
| **Journal** | canonical name, abbrev, press, deposit count, scope, charter as an AXN-chipped ecorow |
| **Editors** | the duoviri, each linked to their card **wherever it lives**, plus the board |
| **Issue** | the inaugural issue, contents in order, each with section and editor's note |
| **Elsewhere** | back to this site's `/who/` card; out to the archive's canonical venue records |

## Nav

Follow the host site's existing convention. Five sites carry the card in a nav bar, six
have a nav bar without it, seven have no nav at all — so `Where` goes in the nav where
there is one, and beside the card link where there is not. On axnidentifiers it sits
directly after `Who` in the `.stations` bar, with `.here` on the current page.

## Data sources — read, never retyped

- `datasets/venues/records/<vid>.json` — scope, abbrev, editorial slate, charter
- `datasets/venues/issues/<vid>-1.json` — the issue and its ordered contents
- `data/registry.json` — deposit counts, joined on **`registry_string`** and never on
  `canonical` (five of eight venues differ, and a canonical join drops them silently)
- `data/editor-cards.json` — where each editor's card lives; paths are **not uniform**
  (vpcor.org uses `/ayanna/`) and were verified, not guessed
- `data/where-links.json` — which venue each site's heteronym edits

## Remaining eleven

restoredacademy (Sigil → nh2) · spxi.dev (Fraction → tsei) · godkinggoogle (Morrow → tse) ·
provenanceerasure (Trace → pjfs) · lagrangeobservatory (Glas → tse) · holographickernel
(Kuro → jcs) · surfacemap (Wells → jcs) · chatgptpsychosis (Feist → nh2) · revelationfirst
(Dancings → mmrs) · vpcor (Vox → pjfs) · machinemediation (the Seven → mmrs).

**Deploys are at the ceiling as of 2026-08-17.** machinemediation and watergiraffe are each
one commit behind on the network-block de-duplication and will catch up when the queue clears.
