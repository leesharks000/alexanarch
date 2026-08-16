# Atlas v1.7 addendum — external dependencies, and a description for every dataset

**2026-08-15 · TACHYON, under operator instruction**

> *"the data atlas should reflect external dependencies, too… and should include descriptions
> of every dataset — including perseus etc, even if its not yet interlinked."*

## The archive's data does not live only in this repository

**Twelve heteronym identity cards are rendered on twelve different domains.** Each is a render
of a record in `datasets/heteronyms/records/`, on a site this repo does not build:

| | |
|---|---|
| Johannes Sigil | restoredacademy.com/who/sigil/ |
| Rex Fraction | spxi.dev/who/fraction/ |
| Damascus Dancings | revelationfirst.com/who/dancings/ |
| Rebekah Cranes | axnidentifiers.org/who/cranes/ |
| Talos Morrow | godkinggoogle.com/who/morrow/ |
| **Sen Kuro** | **holographickernel.org/who/kuro/** |
| Sparrow Wells | surfacemap.org/who/wells/ |
| Rev. Ayanna Vox | vpcor.org/ayanna/who/ |
| Ichabod Spellings | survivethedeletion.vercel.app/who/spellings/ |
| Nobel Glas | lagrangeobservatory.org/who/glas/ |
| Dr. Orin Trace | provenanceerasure.org/who/trace/ |
| Jack Feist | chatgptpsychosis.org/who/feist/ |

**The dependency runs outward.** `records/` produces; the site consumes. A record change does
not propagate until that site is rebuilt and deployed — which is the same class of silence as
the six fleet sites found serving builds older than their own repos.

## What the check found on its first run

**Sen Kuro's card was a 404.** The dataset pointed at `leesharks.com/who/kuro/`. He had been
reseated at `holographickernel.org` by a MANUS ruling — and the fleet commit for that ruling
says it plainly: *"the ruling reached the network-block attribution map and never reached the
page or the grids."* It never reached this dataset either.

**A dataset pointing at a dead surface is a dataset asserting something false**, and no
internal gate could see it, because no gate looked outside the repository.
`scripts/check_external_surfaces.py` now does. All fourteen declared surfaces resolve.

## Capture galleries — and one that is not declared

The registry declares two galleries: `www.godkinggoogle.com/captures` and
`leesharks.com/captures`.

**`machinemediation.org/captures/` exists, resolves, and is not in the list** — and MMRS is
the journal whose founding dataset the capture registry *is*. The venue displaying the data is
absent from the data's own record of where it is displayed.

Also recorded: **host drift.** The v10.0 manifest names `godkinggoogle.vercel.app`; v11.4
names `www.godkinggoogle.com`. A gallery moved and only the newer file knows.

## Other external dependencies now bound

- **data-rhizome releases** — `generated-corpus-v1` (15.1 MB, mined) and `v1` (47.6 MB, the raw
  account export, unmined). Bytes are in neither repo; locators point at releases.
- **Corpora upstreams** — First1KGreek, Perseus, Gutenberg. Mirrored into `datasets/`;
  upstream can change and the mirror does not track it.
- **Resolvers** — the OAI endpoint, the AXN resolver, DataCite (severed 2026-06-19), OpenAIRE.

## Every dataset now has a description

All **eighteen**, including the four that are not interlinked and were therefore invisible in
every crosswalk: **perseus-classical** (1,161 works, 764 aligned — the Greek and Latin
substrate behind the philological work), **gutenberg-classical**, **new-human-primary**, and
**deletion-conformance-fixture**.

An `interlinked` flag marks which five participate in a crosswalk. **Not being interlinked is
not a defect** — Perseus is a mirrored upstream, not archive-native — but it should be legible
rather than inferred from absence. The largest dataset by size is **registry-audit** at 41 MB:
the archive's memory of its own corrections.

## The rule this adds

**An atlas that maps only what a repository contains is not a map of the system.** Bind the
surfaces the data is rendered on, the upstreams it is mirrored from, and the releases its
bytes actually live in — and check them, because those are the dependencies no internal gate
can see.
