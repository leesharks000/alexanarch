"""DW intake harness: parse a LABOR batch, verify against each record's own body, seat."""
import json, re, sys, copy
sys.path.insert(0,'scripts')
from record_modification import diff_touch

NAMEQ = re.compile(r"^[A-Z][\w'’-]*(?:\s+[A-Z][\w'’-]*){0,3}\.?$")  # proper-name scare-quote (DW-002 rule)

def parse(path):
    raw = open(path).read()
    src = re.search(r'\*\*Source commit:\*\*\s*`([0-9a-f]+)`', raw)
    label = re.search(r'Batch (DW-\d+)', raw)
    out = []
    for b in re.split(r'\n## Record #', raw)[1:]:
        n = int(re.match(r'(\d+)', b).group(1))
        def g(pat, flags=0):
            m = re.search(pat, b, flags)
            return m.group(1).strip() if m else ''
        out.append({'n': n,
                    'axn': g(r'\*\*AXN:\*\*\s*`([^`]+)`'),
                    'action': g(r'###\s*Action\s*\n+\*\*([^*]+)\*\*'),
                    'desc': g(r'###\s*Proposed description\s*\n+(.*?)(?=\n###|\n---|\Z)', re.S),
                    'wiki': g(r'###\s*Proposed wiki\s*\n+(.*?)(?=\n###|\n---|\Z)', re.S)})
    return out, (src.group(1) if src else ''), (label.group(1) if label else 'DW-???')

def verify(it, d):
    try: bod = open(f"data/texts/AXN-{d['hex']}-text.md").read()
    except Exception: bod = ''
    hay = (bod + json.dumps(d, ensure_ascii=False)).lower()
    text = it['desc'] + ' ' + it['wiki']
    hits = miss = 0; missed = []
    nums = set(re.findall(r'\b\d{3,5}\b', text)) - set(re.findall(r'\b(?:19|20)\d\d\b', text))
    for x in list(nums)[:5]:
        if x in hay: hits += 1
        else: miss += 1; missed.append(x)
    for q in re.findall(r'[“"]([^”"]{10,70})[”"]', text)[:3]:
        if NAMEQ.match(q.strip()): continue
        if q[:25].lower() in hay: hits += 1
        else: miss += 1; missed.append(q[:30])
    return hits, miss, missed

def run(path):
    reg = json.load(open('data/registry.json'))
    deps = {d['deposit_number']: d for d in reg['deposits']}
    items, src, label = parse(path)
    seated, flagged = [], []
    for it in items:
        n = it['n']; d = deps.get(n)
        if not d: flagged.append((n, 'no such record')); continue
        if it['action'].upper().startswith('NO CHANGE'):
            seated.append({'n': n, 'h': 0, 'm': 0, 'mode': 'no-change'}); continue
        if it['axn'] and it['axn'] != d.get('axn'):
            flagged.append((n, 'AXN mismatch')); continue
        h, m, missed = verify(it, d)
        if m > h:
            flagged.append((n, f'probes {h}/{h+m}; missed {missed}')); continue
        before = copy.deepcopy(d)
        if it['desc']: d['description'] = it['desc']
        if it['wiki']: d['wiki_article'] = it['wiki']
        diff_touch(d, before, f'{label} intake (LABOR-prepared, TACHYON-verified: AXN match + factual probes vs record body)')
        seated.append({'n': n, 'h': h, 'm': m, 'mode': 'seated'})
    json.dump(reg, open('data/registry.json', 'w'), ensure_ascii=False, indent=2)
    return seated, flagged, src, label

if __name__ == '__main__':
    s, f, src, label = run(sys.argv[1])
    for x in s: print('  ✓', x)
    for x in f: print('  ⚑', x)
    json.dump({'seated': s, 'flagged': f, 'src': src, 'label': label}, open('/home/claude/dw_last.json', 'w'))
    print(f"{label}: {len(s)} seated/no-change, {len(f)} flagged")
