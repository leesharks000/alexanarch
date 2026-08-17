#!/usr/bin/env python3
"""check_heteronym_works.py — is every claimed work actually by that heteronym?

Written 2026-08-17, after the operator read the Rebekah Cranes identity card and
found works belonging to Feist, Sharks and Spellings listed as hers.

HOW THEY GOT THERE. A full-text search on the heteronym's NAME. The field was
called `works_recovered_by_full_text_search`, and every deposit mentioning the
name was attached as that heteronym's work -- conflating AUTHORSHIP with
COMPILATION, WITNESS, SUBJECT and MERE MENTION. Deposit #435 is titled 'Compiled,
Woven, and Witnessed by Rebekah Cranes' and its creator is Lee Sharks: she is the
witness, he is the author, and a name search cannot tell the difference.

The archive already forbids this. Every heteronym record carries claims.terms,
whose own note reads: 'the practices, frameworks, concepts this heteronym OWNS.
Capture attribution runs on THESE, not on the name.' The captures obey it --
they are joined by claim, many-to-many, and the name-matched set is kept
separately with every entry marked relation: mention. Works did not obey it.

AUTHORITY: data/registry.json. The creator field, and the journal and press
assignments, decide who a work belongs to. A card does not.

An entry may sit in a works field against the registry ONLY if it carries an
explicit override recording who ruled and why -- because there are real
heteronymic questions here (Operative Semiotics is Sigil's Great Work while its
deposits name Sharks) and those must be RULED, not searched.
"""
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
WORKFIELDS = ('works', 'corpus', 'major_work', 'creative_work', 'catalogue',
              'primary_work', 'book', 'works_of_record', 'corpus_verified',
              'works_recovered_by_full_text_search')


def names(creator, heteronym):
    c = str(creator or '').lower()
    return heteronym.lower() in c or heteronym.split()[-1].lower() in c


def walk(node, path=""):
    if isinstance(node, dict):
        if 'deposit' in node and isinstance(node['deposit'], int):
            yield path, node
        for k, v in node.items():
            yield from walk(v, f"{path}.{k}" if path else k)
    elif isinstance(node, list):
        for v in node:
            yield from walk(v, path)


def main():
    reg = {x['deposit_number']: x for x in
           json.loads((ROOT / 'data/registry.json').read_text())['deposits']}
    fails = []
    checked = 0
    for f in sorted((ROOT / 'datasets/heteronyms/records').glob('*.json')):
        d = json.loads(f.read_text())
        het = d['name']
        for k in WORKFIELDS:
            if k not in d:
                continue
            for path, node in walk(d[k], k):
                dep = node['deposit']
                r = reg.get(dep)
                if not r:
                    continue
                checked += 1
                if names(r.get('creator'), het):
                    continue
                if node.get('attribution_override'):
                    continue           # ruled, and the ruling is recorded
                fails.append(
                    f"{f.stem}: #{dep} is listed under {path} but the registry creator is "
                    f"{str(r.get('creator'))[:44]!r} — reattribute, or add attribution_override "
                    f"naming who ruled and why")
    if fails:
        print(f"FAIL: {len(fails)} work(s) attributed against the registry:")
        for x in fails:
            print("  " + x)
        return 1
    print(f"OK: {checked} claimed works all match the registry creator field")
    return 0


if __name__ == '__main__':
    sys.exit(main())
