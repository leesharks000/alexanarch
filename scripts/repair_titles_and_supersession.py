#!/usr/bin/env python3
"""
repair_titles_and_supersession.py

Two registry defects found 2026-07-26 by inspection of a laborvector link to
deposit #1260, which displayed a title ending in the word "Description" and a
supersession notice pointing at its own ratification record.

DEFECT 1 — ABSORBED SECTION HEADER IN TITLE
At ingest, some titles absorbed the section heading that followed them, so the
registry title reads "... — Crimson Hexagon Archive Description". A word-list
alone cannot fix this: several legitimate titles genuinely end in these words
("An Executive Summary", "Exists Only as Metadata", "Read as Bibliography").
The repair is therefore SELF-VERIFYING — a candidate is only corrected when
BOTH of the following hold in the deposit's own body text:
  (a) the absorbed word appears as a standalone heading (#/##/### Word), and
  (b) the stripped title appears in the opening of the body.
227 candidates, 212 verified, 15 correctly rejected.

DEFECT 2 — KIND-MISMATCH SUPERSESSION
Seven deposits are marked SUPERSEDED by a document that is not a version of
them but a companion artifact: a ratification record, a metadata packet, a
Zenodo metadata record. The effect is worse than an absent relation — it
retires a live work and directs the reader to an accessory.

NOT touched: 24 supersessions whose successor predates its predecessor. That
is overwhelmingly an artifact of restoration, where recovered deposits carry
their original dates under new deposit numbers; #56 (v2.0) -> #1101 (v3.0)
looks reversed while being correct, at 0.98 title similarity. Clearing those
would break working relations. They are reported for review instead.

Also NOT touched: supersessions where predecessor AND successor are the same
kind of document (#1178 -> #645, metadata packet to metadata packet). That is
a genuine version relation and the kind-mismatch test is what preserves it.

Usage: python3 scripts/repair_titles_and_supersession.py [--apply]
"""
import json, re, os, argparse, datetime

REGISTRY = 'data/registry.json'

TRAIL = re.compile(r'\s+(Description|Abstract|Keywords?|Metadata|Summary|Contents?|'
                   r'Notes?|Overview|Introduction|Bibliography|References|Colophon|'
                   r'Appendix)\s*$')
COMPANION = re.compile(r'\b(ratification record|metadata packet|zenodo metadata|'
                       r'companion deposit|witness document|integrity lock certificate|'
                       r'provenance documentation)\b', re.I)


def verify_absorbed(deposit, word, stripped):
    """Both conditions must hold in the deposit's own body."""
    p = (deposit.get('full_text_path') or '').lstrip('/')
    if not p or not os.path.exists(p):
        return False
    head = open(p, encoding='utf-8', errors='replace').read(6000)
    heading = re.search(r'^#{1,3}\s*' + re.escape(word) + r'\s*$', head, re.M | re.I)
    in_body = re.sub(r'\s+', ' ', stripped[:60].lower()) in \
              re.sub(r'\s+', ' ', head[:2500].lower())
    return bool(heading and in_body)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--apply', action='store_true')
    a = ap.parse_args()

    reg = json.load(open(REGISTRY, encoding='utf-8'))
    deps = reg['deposits']
    byn = {d['deposit_number']: d for d in deps}
    stamp = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds').replace('+00:00', 'Z')

    # ---- DEFECT 1 ----
    fixed_titles, rejected = [], []
    for d in deps:
        t = str(d.get('title') or '')
        m = TRAIL.search(t)
        if not m:
            continue
        word, stripped = m.group(1), t[:m.start()].strip()
        if not verify_absorbed(d, word, stripped):
            rejected.append((d['deposit_number'], word, t))
            continue
        fixed_titles.append((d['deposit_number'], word, t, stripped))
        if a.apply:
            d.setdefault('title_repair_log', []).append({
                'at': stamp, 'defect': 'absorbed_section_header',
                'absorbed': word, 'was': t, 'now': stripped,
                'verified_by': 'standalone heading in body + stripped title in body opening',
            })
            d['title'] = stripped

    # ---- DEFECT 2 ----
    cleared, review = [], []
    for d in deps:
        tgt = d.get('superseded_by_deposit_number')
        if not tgt:
            continue
        s = byn.get(tgt)
        if not s:
            continue
        pre, suc = str(d.get('title') or ''), str(s.get('title') or '')
        if COMPANION.search(suc) and not COMPANION.search(pre):
            cleared.append((d['deposit_number'], tgt, pre[:50], suc[:50]))
            if a.apply:
                d.setdefault('supersession_repair_log', []).append({
                    'at': stamp, 'defect': 'kind_mismatch_supersession',
                    'was_superseded_by': tgt, 'successor_title': suc,
                    'reason': ('successor is a companion artifact (ratification record, '
                               'metadata packet, or metadata record), not a version of '
                               'this work; the relation retired a live deposit and '
                               'directed readers to an accessory'),
                })
                # preserve the relation rather than discarding it
                comp = d.setdefault('companion_deposits', [])
                if tgt not in comp:
                    comp.append(tgt)
                d.pop('superseded_by_deposit_number', None)
                if str(d.get('status', '')).upper() == 'SUPERSEDED':
                    d['status'] = 'ACTIVE'
        else:
            ds, dd = str(s.get('date', '')), str(d.get('date', ''))
            if ds and dd and ds < dd:
                review.append((d['deposit_number'], tgt, dd, ds))

    print("DEFECT 1 — absorbed section header in title")
    print("  corrected : %d" % len(fixed_titles))
    print("  rejected  : %d  (legitimate titles ending in those words)" % len(rejected))
    import collections
    print("  by word   :", dict(collections.Counter(w for _, w, _, _ in fixed_titles)))
    for n, w, was, now in fixed_titles[:5]:
        print("     #%-5s -%s" % (n, w)); print("        %s" % now[-70:])
    print()
    print("DEFECT 2 — kind-mismatch supersession")
    print("  cleared   : %d" % len(cleared))
    for n, t, pre, suc in cleared:
        print("     #%-5s was superseded_by #%-5s (%s)" % (n, t, suc[:44]))
    print("  flagged for review (successor predates; likely restoration artifact): %d"
          % len(review))
    for n, t, dd, ds in review[:6]:
        print("     #%-5s -> #%-5s   %s -> %s" % (n, t, dd, ds))

    if not a.apply:
        print("\n[dry-run] nothing written. re-run with --apply")
        return
    reg['deposits'] = deps
    json.dump(reg, open(REGISTRY, 'w', encoding='utf-8'), indent=2, ensure_ascii=False)
    print("\n[ok] wrote %s" % REGISTRY)


if __name__ == '__main__':
    main()
