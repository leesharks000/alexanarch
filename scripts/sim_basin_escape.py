#!/usr/bin/env python3
"""sim_basin_escape.py — can a term leave its basin, and does attribution survive?

THE INVERSION THIS RESTS ON (measured, 2026-08-17, n=258 observations with PER):

    no citations shown at all   PER 0.69
    any citation shown          PER 0.54
    off-entity hosts present    PER 0.29 (heteronym named) / 0.44 (not)
    no off-entity hosts         PER 0.37 (heteronym named) / 0.67 (not)

A SEALED ANSWER IS THE ERASURE CASE. When the composition layer retrieves nothing
it composes from parametric memory and drops the author. When it reaches into
foreign basins it is in citation mode and attribution survives better. Bleed is
not dilution -- it is EVIDENCE THAT RETRIEVAL HAPPENED, and the leak is the only
bridge out of the basin.

So the objective is not to minimise bleed. It is to maximise ESCAPE = reach x
retention: attributed appearances in basins the archive does not own.

MODEL. A term is a compound of components. Each component has a basin. Escape
depends on:

  DECOMPOSABILITY  does the term split into ordinary words? A split is how the
                   term rides a component's basin outward. Measured inward as the
                   primary bleed driver (coined 28% vs uncoined 12%); the same
                   mechanism runs both ways.
  COLLISION        does the term hit an existing named thing? A collision imports
                   a fandom inward AND exposes the term to that fandom outward.
  ANCHOR           does a proper name travel with it? Naming a heteronym raised
                   retention in every stratum (0.29 vs 0.44, 0.37 vs 0.67).
  QUOTING          the exact-phrase operator halves bleed (9% vs 19%). It is a
                   DEFENCE THAT COSTS REACH, and under this objective it is a cost
                   rather than a benefit.

Monte Carlo over the lexical registry. Each trial issues a term into a basin drawn
from its component and collision profile, and records whether attribution survived
the crossing, using the retention rates measured above rather than assumed ones.

    python3 scripts/sim_basin_escape.py --trials 20000
"""
import argparse
import collections
import json
import pathlib
import random
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]

# Retention measured from the corpus, not posited.
RETENTION = {
    ("anchor", "reach"): 1 - 0.29,
    ("anchor", "sealed"): 1 - 0.37,
    ("bare", "reach"): 1 - 0.44,
    ("bare", "sealed"): 1 - 0.67,
}
# P(the answer reaches any off-entity basin), measured by segment.
P_REACH = {"coined": 0.28, "uncoined": 0.12, "quoted": 0.09, "unquoted": 0.19}

COMMON = None


def load_common():
    """Component-word commonness in ENGLISH, not in the archive.

    The first version of this counted word frequency across deposit titles, which
    is CIRCULAR: 'capture', 'metadata' and 'layer' are common inside the archive
    and that told us nothing about whether they carry a term outward. Every term
    scored decomposability 1.00 and the ranking was noise.

    Zipf frequency from wordfreq: log10(occurrences per billion words). 'economy'
    is 4.87, 'semiotics' 2.49, 'sophon' and 'heteronym' 0.00 -- the last two do
    not exist in English at all, which is exactly the property that matters.
    """
    from wordfreq import zipf_frequency
    return zipf_frequency


def profile(term, common, minted):
    """Decomposability and collision exposure for one term."""
    words = re.findall(r"[a-z]{4,}", term.lower())
    if not words:
        return None
    # a component is 'ordinary' if it appears widely in the corpus AND is not itself minted
    # A component carries the term outward in proportion to how much English
    # traffic it already has. Zipf 4.0 is roughly 'economy'; 2.5 is 'semiotics';
    # 0 is a coinage with no English basin to ride.
    z = [common(w, "en") for w in words]
    ordinary = [w for w, f in zip(words, z) if f >= 3.5]
    decomp = sum(min(f, 6.0) / 6.0 for f in z) / len(z)
    return {
        "term": term,
        "words": len(words),
        "ordinary_components": ordinary,
        "decomposability": round(decomp, 3),
        "max_component_zipf": round(max(z), 2),
        "zero_english_components": sum(1 for f in z if f == 0),
        "coined": term.lower() in minted or len(words) > 1,
    }


def simulate(prof, trials, rng, anchor=False, quoted=False):
    """One term, many issuances. Returns escape rate and attributed-escape rate."""
    base = P_REACH["coined"] if prof["coined"] else P_REACH["uncoined"]
    # decomposability scales reach: a term with no ordinary component has no bridge
    p_reach = base * (0.25 + 0.75 * prof["decomposability"])
    if quoted:
        p_reach *= P_REACH["quoted"] / P_REACH["unquoted"]
    reached = attributed = 0
    for _ in range(trials):
        r = rng.random() < p_reach
        state = "reach" if r else "sealed"
        keep = rng.random() < RETENTION[("anchor" if anchor else "bare", state)]
        if r:
            reached += 1
            if keep:
                attributed += 1
    return {"p_reach": round(p_reach, 4),
            "escape_rate": round(reached / trials, 4),
            "attributed_escape": round(attributed / trials, 4)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--trials", type=int, default=20000)
    ap.add_argument("--top", type=int, default=25)
    a = ap.parse_args()
    rng = random.Random(9271269)
    common = load_common()
    lex = json.loads((ROOT / "data/lexical-minting-registry.json").read_text())
    rows = lex if isinstance(lex, list) else lex.get("terms", lex)
    minted = {str(r.get("term", "")).lower() for r in rows}
    seen, out = set(), []
    for r in rows:
        t = str(r.get("term") or "").strip()
        if len(t) < 6 or t.lower() in seen:
            continue
        seen.add(t.lower())
        p = profile(t, common, minted)
        if not p or p["decomposability"] == 0:
            continue
        s = simulate(p, a.trials // 40, rng, anchor=True, quoted=False)
        out.append({**p, **s, "type": r.get("type")})
    out.sort(key=lambda x: -x["attributed_escape"])
    print(f"terms simulated: {len(out)}  ·  trials each: {a.trials // 40}\n")
    print(f"{'attributed':>11}{'reach':>8}{'decomp':>8}  term")
    print("-" * 74)
    for x in out[:a.top]:
        print(f"{x['attributed_escape']:>11.3f}{x['escape_rate']:>8.3f}"
              f"{x['decomposability']:>8.2f}  {x['term'][:44]}")
    pathlib.Path("/tmp/sim.json").write_text(json.dumps(out, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
