#!/usr/bin/env python3
"""Diacritic-blind concordance: find a stem, print the ACCENTED context.

Search is normalized; output is the original text with all diacritics intact,
via normalize.index_map. Every Greek passage quoted in the program's papers
was pulled with this, so quotations are verbatim from the edition, never
retyped from memory.

Usage: extract_context.py <file> <stem> [--width 700] [--max 3]
"""
import argparse, pathlib
from normalize import strip, index_map, tei_text, wiki_text

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('file'); ap.add_argument('stem')
    ap.add_argument('--width', type=int, default=700); ap.add_argument('--max', type=int, default=3)
    a = ap.parse_args(); p = pathlib.Path(a.file)
    raw = p.read_text(encoding='utf-8', errors='replace')
    if p.suffix == '.xml': raw = tei_text(raw)
    elif p.suffix == '.html': raw = wiki_text(raw)
    norm, im = index_map(raw); pat = strip(a.stem); s = 0; n = 0
    while n < a.max and (j := norm.find(pat, s)) >= 0:
        lo, hi = im[max(0, j - a.width // 2)], im[min(len(im) - 1, j + a.width // 2)]
        print(f"--- hit {n+1} @ normalized offset {j} ---\n{raw[lo:hi].replace(chr(10), ' ')}\n")
        s = j + 1; n += 1
    if n == 0: print(f"NO HIT for {a.stem!r} in {a.file} — report with corpus size before asserting absence.")

if __name__ == '__main__':
    main()
