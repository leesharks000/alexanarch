#!/usr/bin/env python3
"""Diacritic-blind stem census across a corpus directory.

Reports per-stem totals and per-work distribution. Used for:
  - the name-census (Σαπφ- -> 0; all string-hits are σάπφειρος)
  - the transmission-vocabulary families (σφραγ-, χαρακτηρ-, εκμαγει-, ...)
  - the rare-word bridges (δυσεξαλειπτ-, υψηγορ-, απηχ-, ενηχ-)

Usage: census.py <corpus_dir> [--stems a,b,c]
A null result here is a POSITIVE FINDING and must be reported with the
corpus name, the work count, and the character count. Absence asserted
without a stated corpus is not evidence.
"""
import sys, json, pathlib, argparse
from normalize import strip, tei_text, wiki_text

DEFAULT_STEMS = {
 "σαπφ": "Σαπφ- (the name; expect σάπφειρος collisions)",
 "αποτυπ": "ἀποτυπ- (Longinus's stamp-noun)",
 "δυσεξαλειπτ": "δυσεξάλειπτ- (hard-to-efface; the hard bridge)",
 "υψηγορ": "ὑψηγορ- (high-speech)",
 "απηχ": "ἀπηχ- (echo-off)", "ενηχ": "ἐνηχ- (echo-into)", "υπηχ": "ὑπηχ- (under-sound)",
 "σφραγ": "σφραγ- (seal)", "χαρακτηρ": "χαρακτηρ- (stamp)",
 "εκμαγει": "ἐκμαγει- (Theaetetus wax)", "απαυγασμ": "ἀπαύγασμ- (effulgence)",
 "αποσπασμ": "ἀπόσπασμ- (fragment)", "απορρο": "ἀπορρο- (effluence)",
 "κορυβαντ": "κορυβαντ-", "ενθουσι": "ἐνθουσι-", "θεοφορ": "θεοφορ-",
 "κατοκωχ": "κατοκωχ-", "κατοχ": "κατοχ-", "οργανον": "ὄργανον",
 "ιεροφαντ": "ἱεροφαντ-", "μυστ": "μυστ-", "τελετ": "τελετ-", "εποπτ": "ἐποπτ-",
}

def load(corpus_dir):
    d = pathlib.Path(corpus_dir); out = {}
    for p in sorted(d.rglob('*')):
        if p.suffix == '.xml':   out[p.stem] = tei_text(p.read_text(encoding='utf-8', errors='replace'))
        elif p.suffix == '.html': out[p.stem] = wiki_text(p.read_text(encoding='utf-8', errors='replace'))
        elif p.suffix == '.txt':  out[p.stem] = p.read_text(encoding='utf-8', errors='replace')
    return {k: v for k, v in out.items() if len(v) > 3000}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('corpus_dir'); ap.add_argument('--stems', default=None)
    ap.add_argument('--json', action='store_true')
    a = ap.parse_args()
    stems = ({s: s for s in a.stems.split(',')} if a.stems else DEFAULT_STEMS)
    works = load(a.corpus_dir)
    norm = {k: strip(v) for k, v in works.items()}
    total_chars = sum(len(v) for v in norm.values())
    print(f"CORPUS: {a.corpus_dir}  |  {len(works)} works  |  {total_chars:,} normalized chars\n")
    rows = {}
    for stem, label in stems.items():
        hits = {k: v.count(stem) for k, v in norm.items() if stem in v}
        rows[stem] = {'total': sum(hits.values()), 'by_work': hits}
        dist = " ".join(f"{k}:{n}" for k, n in sorted(hits.items(), key=lambda x: -x[1])) or "—"
        print(f"{rows[stem]['total']:>5}  {label:<44} {dist}")
    if a.json:
        pathlib.Path('census.json').write_text(json.dumps(
            {'corpus': a.corpus_dir, 'works': len(works), 'chars': total_chars, 'stems': rows},
            ensure_ascii=False, indent=1))
        print("\n-> census.json")

if __name__ == '__main__':
    main()
