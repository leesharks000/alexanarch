# Atlas v1.5 addendum — the binding

**2026-08-15 · TACHYON, under operator instruction**

> *"that atlas binds every connector, input output, interlinking, to data — or should."*

It should. It did not. **The atlas named three datasets of eighteen.**

## What the count showed

| | |
|---|---|
| datasets present | **18** · 316 files · 90 MB |
| named anywhere in the atlas | **3** |
| carrying a manifest | 13 |
| **declaring a canonical store** | **2** |
| **naming the script that rebuilds them** | **1** |

A dataset that does not say where its authority lives, or what regenerates it, **cannot be
checked for drift**. That is not a documentation gap; it is the precondition for every silent
failure recorded in this atlas:

- the heteronym index sat thin against rich records, and an agent read the index as the data;
- the capture link map sat 43 captures stale against a live registry, and would have carried
  that staleness into every venue join built on it;
- the identity cards' capture blocks sat four registry versions behind, and reported 40
  captures where the registry held 54.

Each was found by a person looking, not by a check. The binding exists so the check can.

## The binding

`binding-v1.0.json` — one row per dataset with its file count, manifest state, declared
canonical store, named producer, and **explicit `binding_gaps`** where any of those is
missing. Plus:

**10 producers** — what writes what. `build_heteronym_index.py`, `build_venues_index.py`,
`build_journals_dataset.py`, `link_heteronym_captures.py`, `resolve_capture_links.py`,
`regenerate_surfaces.py`, `citation_extractor.py`, `mint_deposit.py` via the pipeline,
`wire_deposit.regenerate_static_page`.

**10 gates** — what each one fails on, stated as a condition rather than a name. Five are
`--check` modes that compare a projection against its store; five are audits that compare a
surface against reality.

**8 interlinks** — every join now declares **what it joins on**, because the join key is the
claim:

| join | on |
|---|---|
| heteronyms × deposits | creator field (byline) |
| heteronyms × venues | creator field (byline) |
| **mantles × venues** | **attestation — required separately** |
| venues × citation graph | deposit endpoints → journal |
| **captures × venues, evidentiary** | capture → deposit → venue (hard/soft split) |
| **captures × venues, thematic** | capture text → venue claim terms |
| captures × heteronyms | claim terms, many-to-many |
| venues × Pocket Humans | deposit number |

Three of those carry a **must-not** rather than a method, and the must-nots are the load-bearing part:

- **A mantle cannot be joined on a byline.** A creator field records an *occupant*; a mantle
  is a *position*. MMRS's own spec says so. Joined on bylines the Assembly Chorus appears
  absent, and the absence gets reported as a fact about the Chorus rather than about the join.
- **The two capture routes must not be summed.** Evidentiary is an identification; thematic is
  a resemblance. Adding them produces a number that means nothing.
- **Claim counts are evidence of contact, not of aboutness.** A capture that mentions a
  heteronym's domain is a real link; a capture *about* that heteronym is a different thing,
  and only a reading separates them.

## Known version conflicts, recorded rather than resolved

**The capture registry has three near-identical names and the wrong one has been read at
least twice:**

- live — `data/EA-WG-CAPTURES-01.json`, **v11.4, 343 captures**
- `datasets/capture-registry/EA-WG-CAPTURES-01.json` — **v10.0 gallery manifest, 300**
- `data/EA-WG-CAPTURES-01-v8.11.json`, `-v9.6.json` — frozen snapshots

Also recorded: the heteronyms card on the datasets tab still reads *"12 Dodecad positions · 13
total"* against 26 records; and `datasets/venues` carries no manifest, so its canonical store
is declared only inside the projection that depends on it.

## The rule this addendum adds

**A dataset must declare, on its own face: what is canonical, what regenerates it, and what
gate detects its drift.** The three-tier rule from v1.4 said a layer must say *whether* it is
data. This says it must also say *what keeps it true*.

Sixteen datasets do not yet. `binding_gaps` names which, per dataset, so the work is
enumerable rather than remembered.
