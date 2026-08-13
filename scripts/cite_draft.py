"""cite_draft.py — DRAFT ONLY. The parser proposes; TACHYON reads and rules.

This exists to remove TYPING from the loop, not reading. It emits a candidate
citation structure beside the record tail so a reader can correct it rather than
transcribe from scratch. Nothing it produces is authoritative: every draft is
read against the source text before it is seated, and the reading overrules the
draft wherever they disagree — which, on this material, has been often.
"""
import json, re, sys

def draft(text):
    tail = text[int(len(text)*0.45):]
    out = []
    # inline citations that kept a URL
    for m in re.finditer(r'\[\[?(\d+)\]\((https?://[^\)\s]+)\)', text):
        u = m.group(2).rstrip('.,);')
        dom = re.match(r'https?://([^/]+)', u)
        out.append({'pos':'inline','url':u,'domain':dom.group(1).replace('www.','') if dom else None})
    # card blocks: SITE / TITLE / DATE — SNIPPET  or  TITLE / DATE — SNIPPET / SITE
    lines = [l.strip() for l in tail.split('\n') if l.strip()]
    for i,l in enumerate(lines):
        if re.match(r'^(Zenodo|Wikipedia|Medium|Academia\.edu|GitHub|Reddit|YouTube|arXiv|PhilPapers|SciLynk|Britannica|Instagram|Substack|Quora|LinkedIn|Scribd|[a-z0-9.-]+\.(com|org|net|edu|gov|io))', l, re.I) and len(l) < 70:
            nxt = lines[i+1] if i+1 < len(lines) else ''
            prv = lines[i-1] if i else ''
            out.append({'pos':'card','site':l,'title_after':nxt[:90],'title_before':prv[:90]})
    return out

if __name__ == '__main__':
    Q = json.load(open('/tmp/citeq.json'))
    d = json.load(open('/home/claude/palette/EA-WG-CAPTURES-01-REBUILD.json'))
    done = {(a['semantic_address'].get('q_as_issued'), o['observed_on'])
            for a in d['addresses'] for o in a['observations']
            if 'citations' in o['citations_and_sources']}
    left = [x for x in Q if (x['q'], x['date']) not in done]
    seen, uniq = set(), []
    for x in left:
        k = (x['q'], x['date'])
        if k in seen: continue
        seen.add(k); uniq.append(x)
    a, b = int(sys.argv[1]), int(sys.argv[2])
    for i, x in enumerate(uniq[a:b], a):
        print('='*74)
        print('[%d] «%s» %s | %s | %d ch' % (i, x['q'], x['date'], x['surface'], x['chars']))
        print('--- TAIL '.ljust(74,'-'))
        print(x['text'][-1100:])
        print('--- DRAFT (to be read against the tail, not trusted) ---')
        for c in draft(x['text'])[:14]:
            print('   ', c)
        print()
