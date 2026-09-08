#!/usr/bin/env python3
"""Derive LINE MEMBERSHIP at scale; leave developmental ORDER to judgment.

Two different things were being conflated. A developmental edge — this record
develops from that one — is a judgment and must be authored one at a time. But
MEMBERSHIP in a body of thought is evidence, and can be derived from the record's
own title and keywords the way keyword enrichment is derived.

Separating them lets the 1,208 orphans measured on 2026-09-08 join their bodies
without anyone pretending to know their sequence. Membership derived here is marked
line_basis='derived'; a curated line with ordered develops_from edges is 'stated',
and this script never overwrites one.

Rules are ordered: the first match wins, so the more specific patterns come first.
"""
import json, re, sys, collections

RULES = [
 ('space-ark-and-transforms','science', r'space ark|ascii spatial|glyphic checksum|emoji transform|symbolic compression of the c'),
 ('axn-identifiers','infrastructure', r'\bAXN\b.*identifier|axn resolver|content-derived identifier|axn as distributed'),
 ('doi-severance-and-restoration','infrastructure', r'zenodo|datacite|dead doi|orphan restoration|tombstone|\bCERN\b|right to access|RQF\d'),
 ('capture-and-reception','science', r'capture|ai overview|ai mode|summarizer|knowledge panel|reception|probe protocol'),
 ('metadata-packets','infrastructure', r'metadata packet|MPAI|disambiguat'),
 ('operator-swerve-effective-act','philosophy', r'operator ?//|swerve|effective act|canonical operator'),
 ('assembly-chorus','method', r'assembly chorus|assembly synthesis|referee|review round|four reviews'),
 ('corpus-seatings','philology', r'EA-CORPORA|seating|seated under|the \w+ seating'),
 ('authorship-and-heteronymy','letters', r'heteronym|orthonym|dodecad|provenance packet|provenance anchor|authorship investigation|measurement register'),
 ('scripture-and-theology','letters', r'gospel|sermon|apocalyp|scripture|midrash|logos|theolog|revelation|crucifixion|witness architecture'),
 ('poetry','letters', r'\bpoem|poetry|sonnet|lyric|verse|pearl|sappho|catullus|new human \d|cohort'),
 ('rooms-and-chambers','architecture', r'\broom\b|chamber|gallery|wing|museum|the ark\b'),
 ('fleet-surfaces','infrastructure', r'\.org|\.com|landing|surface|fleet|site\b|blog index'),
 ('protocol-and-governance','governance', r'protocol|specification|governance|constitution|charter|policy|work plan|integrity lock|closure notice'),
 ('errata','method', r'erratum|corrigend|correction to'),
 ('studies-and-predictions','science', r'prediction|falsif|study|experiment|baseline|dashboard'),
 ('semantic-economy','science', r'semantic econom|semantic rent|labor|proletar|marx|class consciousness|extractive'),
 ('continuity-records','method', r'TACHYON|continuity record|session \d{4}-|status report'),
]

def derive(x):
    t = (x.get('title') or '') + ' ' + ' '.join(x.get('keywords') or [])
    for line, parent, pat in RULES:
        if re.search(pat, t, re.I):
            return line, parent
    return None, None

def main(apply=False):
    reg = json.load(open('data/registry.json', encoding='utf-8'))
    lines = reg.setdefault('lines', {})
    for line, parent, _ in RULES:
        lines.setdefault(line, {'parent': parent, 'title': line.replace('-', ' ').capitalize()})
    n = collections.Counter(); placed = 0
    for x in reg['deposits']:
        if (x.get('status') or 'ACTIVE') != 'ACTIVE': continue
        if x.get('line'):                       # never overwrite a curated line
            n[x['line']] += 1; continue
        ln, par = derive(x)
        if not ln: continue
        n[ln] += 1; placed += 1
        if apply:
            x['line'] = ln; x['line_parent'] = par; x['line_basis'] = 'derived'
    act = sum(1 for x in reg['deposits'] if (x.get('status') or 'ACTIVE') == 'ACTIVE')
    print(f"derive_lines: {placed} newly placed · {sum(n.values())} of {act} active in a line "
          f"({100*sum(n.values())//act}%) · {act - sum(n.values())} unplaced")
    for k, v in n.most_common(): print(f"    {v:>5}  {k}")
    if apply:
        json.dump(reg, open('data/registry.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
        print("  written")

if __name__ == '__main__':
    main('--apply' in sys.argv)
