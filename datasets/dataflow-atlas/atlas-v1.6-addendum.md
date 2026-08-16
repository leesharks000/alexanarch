# Atlas v1.6 addendum — every producer bound, and a collision I caused

**2026-08-15 · TACHYON**

v1.5 bound eighteen datasets. It bound **ten producers**. There are **174 scripts**, and
`script-dependency-graph.json` named **fourteen**.

## The count

| | |
|---|---|
| scripts on disk | **174** |
| named in the dependency graph | 14 |
| **unbound** | **160** |
| writing a known artifact | 42 |
| **carrying a `--check` gate** | **14** |

Most producers cannot be verified against their own output. `binding-v2.0.json` now carries
every script with its docstring, its writes, its reads, and its gate state.

## Contested artifacts — the finding that matters

An artifact with more than one producer has **no single writer, no ordering, and no lock**.
Whichever script ran last wins, and nothing records which did.

| artifact | producers |
|---|---|
| `data/EA-WG-CAPTURES-01.json` | **15** |
| `data/registry.json` | **11** |

The capture registry has fifteen scripts writing it — which is how three near-identical files
came to exist, and why the wrong one has been read at least twice. And the corpus's canonical
store has eleven writers, while `DEPLOY-FLOW.md` names `deposit_pipeline.py` as *the single
deposit workflow*. Ten of the eleven are not routed through it.

This is not a bug to fix in one pass. It is a standing condition that should be **declared**,
so that the next agent reading `data/registry.json` knows it is contested rather than assuming
a single author.

## A collision I caused, and how it is reconciled

**Two captures-to-heteronyms linkers exist, over two stores, both dated today.**

| | |
|---|---|
| `link_captures_to_heteronyms.py` → `data/dodecad.json` | **name match**, 12 Dodecad positions, MANUS wiring rule |
| `link_heteronym_captures.py` → `datasets/heteronyms/records/` | **claim match**, 26 identities, written tonight |

They disagree substantially — Fraction 16 by name against 95 by claim; Sigil 56 by name
against 46 by claim. **I built the second without finding the first**, which is precisely the
failure this atlas exists to prevent, and I committed it while writing the document that
forbids it.

**Resolution: both kept, neither summed.** The records are canonical and now carry both
routes as separate fields — `captures_by_name` (narrow, precise: the capture names the
heteronym) and `captures` (broad, thematic: the capture hits the heteronym's claims).
`data/dodecad.json` is marked a **projection**, not a competing store. Where the two disagree,
**the name count is the floor and the claim count is the ceiling.**

The gaps turn out to be informative rather than noise:

- **Fraction +79.** SPXI surfacing without his name — exactly the case the claim method exists
  for, and invisible to name matching.
- **Sigil −10.** The inverse: he is *named* in captures whose concepts he does not claim.
  Which is what a critic's byline does — it appears beside work that is not his subject.

Two routes, kept separate, never summed. The same discipline as evidentiary-versus-thematic in
the venue crosswalk, and as byline-versus-attestation for the mantles. **Three times now the
right answer has been two joins rather than one**, and each time the wrong answer was to pick
the method I had already built.

## The rule this adds

**Before writing a producer, search for the one that already exists.** The atlas cannot say
what a script does if the script was written without reading the atlas. `binding-v2.0.json`
makes that search possible for the first time: 174 scripts, what each writes, what each reads,
and which artifacts are contested.
