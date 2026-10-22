#!/usr/bin/env python3
"""add_text_pointers.py — point machine readers of every record page to its plain text (2026-10-22).

Record pages carry their Full Text after the description, wiki article and concepts; on the long ones it begins
hundreds of kilobytes in (#683: byte ~256,000 of 617 KB). A fetcher reading only the head of the page found no
text, judged the record unreadable and stopped, while /data/texts/AXN-XXXX-text.md sat unlinked. The renderer
(wire_deposit.text_pointer_html) now writes a <link rel="alternate" type="text/markdown"> in the head and a
first-screen line under the byline (the head link first in the head, ahead of the JSON-LD). This script writes the same two into the pages already built, in place,
leaving everything else on them as it is; a full re-render is not needed for this and would touch far more.

Idempotent: a page that already carries the head link is skipped.

    python3 scripts/add_text_pointers.py            # every record in the registry
    python3 scripts/add_text_pointers.py 683 1690   # these
"""
import json, os, pathlib, re, sys
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
os.chdir(ROOT)
from wire_deposit import text_pointer_html

VIEWPORT = re.compile(r'(<meta name="viewport" content="[^"]*">)')
BYLINE = re.compile(r'(</h1>\s*<div style="font-size:\.85em;color:#777;margin-bottom:10px">.*?</div>)', re.S)


def main(nums):
    reg = json.load(open('data/registry.json'))
    by = {d['deposit_number']: d for d in reg['deposits']}
    nums = nums or sorted(by)
    done = skipped = no_text = no_page = unplaced = 0
    misses = []
    for n in nums:
        d = by.get(n)
        p = ROOT / f's/records/{n}/index.html'
        if not d or not p.exists():
            no_page += 1; continue
        s = p.read_text(encoding='utf-8')
        if 'type="text/markdown" title="Full text (plain)"' in s:
            skipped += 1; continue
        head, line = text_pointer_html(d)
        if not head:
            no_text += 1; continue
        # First in the head: the JSON-LD after it carries the whole text as articleBody, and on long records the
        # head alone runs past 250 KB.
        s2, k1 = VIEWPORT.subn(lambda m: m.group(1) + head, s, count=1)
        s3, k2 = BYLINE.subn(lambda m: m.group(1) + '\n' + line, s2, count=1)
        if not (k1 and k2):
            unplaced += 1; misses.append(n); continue
        p.write_text(s3, encoding='utf-8')
        done += 1
    print(json.dumps({"written": done, "already": skipped, "no_plain_text": no_text, "no_page": no_page,
                      "not_placed": unplaced, "not_placed_records": misses[:40]}))


if __name__ == '__main__':
    main([int(a) for a in sys.argv[1:]])
