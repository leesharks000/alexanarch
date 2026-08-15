#!/usr/bin/env python3
"""Sappho-31 fingerprint scan with random-window baselines.

Method. Eleven feature families are drawn from Sappho 31 (nine somatic,
two structural). Windows of +/-700 normalized chars are taken around every
INSPIRATION ANCHOR in each work; the score is how many families fire in the
window. Baseline: 150 random windows per work, fixed seed.

The finding is NOT the aggregate ratio; it is the DECOMPOSITION. Operator
families (mania, hearing, alienation, voice, tongue, sight) travel; flesh
families (sweat, tremor, pallor, fire) go to zero. That asymmetry is the
decay law, and it is what the transform's dissipation rule (D) predicts.

Usage: fingerprint_scan.py <corpus_dir> [--window 700] [--baseline 150]
"""
import argparse, pathlib, random, statistics, collections, json
from normalize import strip, tei_text, wiki_text
from census import load

FAMILIES = {
 "voice-fail":    ["αφων", "ισχνοφων", "φωνητηριον"],
 "tongue":        ["γλωσσ", "γλωττ", "βραδυγλωσσ", "επιστομιζ"],
 "hearing":       ["ακου", "ενηχ", "ηχε", "ωσιν"],
 "sight-fail":    ["ομμα", "αορασ", "τυφλ", "σκοτοδιν", "αμαυρ"],
 "fire-heat":     ["πυρ ", "φλογ", "θερμ", "διακαι", "αναφλεγ"],
 "sweat":         ["ιδρω"],
 "tremble":       ["τρομ", "τρεμ", "φρικ"],
 "pallor-green":  ["χλωρ", "ωχρ"],
 "near-death":    ["τεθν", "θανατ", "ημιθαν"],
 "mania-ecstasy": ["μανι", "εκστα", "βακχ", "κορυβαντ", "ενθουσι", "κατοκωχ", "επιθειασμ"],
 "alienation":    ["αλλοτρι", "οικειον ουδεν", "εξοικιζ", "ουκετ", "εκδημ"],
}
FLESH = {"fire-heat", "sweat", "tremble", "pallor-green"}
ANCHORS = ["προφητ", "θεοφορ", "ενθουσι", "κατοκωχ", "εκστα", "επιθειασμ", "θεοληπτ", "θεσπιζ"]

def fired(window):
    return [f for f, pats in FAMILIES.items() if any(p in window for p in pats)]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('corpus_dir'); ap.add_argument('--window', type=int, default=700)
    ap.add_argument('--baseline', type=int, default=150); ap.add_argument('--seed', type=int, default=31)
    a = ap.parse_args(); random.seed(a.seed)
    works = load(a.corpus_dir); W = a.window
    rows, fam_counts, anchors_total = [], collections.Counter(), 0
    for name, raw in sorted(works.items()):
        norm = strip(raw)
        pos = set()
        for anc in ANCHORS:
            i = 0
            while (j := norm.find(anc, i)) >= 0: pos.add(j); i = j + 1
        if not pos: continue
        scores = []
        for p in sorted(pos):
            f = fired(norm[max(0, p - W): p + W]); scores.append(len(f))
            for x in f: fam_counts[x] += 1
        anchors_total += len(pos)
        base = ([len(fired(norm[max(0, r - W): r + W]))
                 for r in (random.randrange(W, max(W + 1, len(norm) - W)) for _ in range(a.baseline))]
                if len(norm) > 3 * W else [0])
        rows.append((name, len(pos), statistics.mean(scores), statistics.mean(base), max(scores)))
    rows.sort(key=lambda r: -(r[2] - r[3]))
    print(f"{'work':<10}{'anchors':>8}{'mu_anchor':>11}{'mu_random':>11}{'max':>5}")
    for n, c, ma, mb, mx in rows: print(f"{n:<10}{c:>8}{ma:>11.2f}{mb:>11.2f}{mx:>5}")
    print(f"\nCORPUS  anchor {statistics.mean(r[2] for r in rows):.2f}  "
          f"vs random {statistics.mean(r[3] for r in rows):.2f}")
    print(f"\nFAMILY FIRE-RATE across {anchors_total} anchor windows  "
          f"(flesh families marked *):")
    for f, n in fam_counts.most_common():
        print(f"  {n:>4}/{anchors_total}  {f}{'  *FLESH' if f in FLESH else ''}")
    for f in FAMILIES:
        if f not in fam_counts: print(f"     0/{anchors_total}  {f}{'  *FLESH' if f in FLESH else ''}")

if __name__ == '__main__':
    main()
