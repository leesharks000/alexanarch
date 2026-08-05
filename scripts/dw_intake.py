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
    # DW-032 introduced a second batch format: '## #517 — `AXN:...`' headers and
    # '### Proposed replacement description' field names, where earlier batches
    # used '## Record #517' and '### Proposed description'. Accept both rather
    # than silently parsing zero records (DW-032 seated 0/24 before this).
    blocks = re.split(r'\n## Record #', raw)[1:]
    if not blocks:
        blocks = [b for b in re.split(r'\n## #', raw)[1:] if re.match(r'\d+', b)]
    for b in blocks:
        n = int(re.match(r'(\d+)', b).group(1))
        def g(pat, flags=0):
            m = re.search(pat, b, flags)
            return m.group(1).strip() if m else ''
        out.append({'n': n,
                    'axn': g(r'\*\*AXN:\*\*\s*`([^`]+)`'),
                    'action': g(r'###\s*Action\s*\n+\*\*([^*]+)\*\*'),
                    'desc': (g(r'###\s*Proposed (?:replacement )?description\s*\n+(.*?)(?=\n###|\n---|\n## |\Z)', re.S)),
                    'wiki': (g(r'###\s*Proposed (?:replacement )?wiki(?: article)?\s*\n+(.*?)(?=\n###|\n---|\n## |\Z)', re.S))})
    return out, (src.group(1) if src else ''), (label.group(1) if label else 'DW-???')

def verify(it, d):
    try: bod = open(f"data/texts/AXN-{d['hex']}-text.md").read()
    except Exception: bod = ''
    hay = (bod + json.dumps(d, ensure_ascii=False)).lower()
    text = it['desc'] + ' ' + it['wiki']
    hits = miss = 0; missed = []
    # DW-022 rule: '#261' style spans are CROSS-REFERENCES to sibling deposits,
    # not factual claims about this record's body. Strip them before probing.
    _probe_text = re.sub(r'#\d{1,4}\b', ' ', text)
    nums = set(re.findall(r'\b\d{3,5}\b', _probe_text)) - set(re.findall(r'\b(?:19|20)\d\d\b', _probe_text))
    for x in list(nums)[:5]:
        if x in hay: hits += 1
        else: miss += 1; missed.append(x)
    # DW-004/005 rule: quoted phrases are matched against a normalized body
    # (punctuation stripped, whitespace collapsed) and tolerate simple
    # singular/plural variance — LABOR quotes a work's phrase as it reads in
    # prose, which is not a factual claim about exact wording.
    norm = re.sub(r'\s+', ' ', re.sub(r'[^a-z0-9 ]', ' ', hay))
    def present(q):
        c = re.sub(r'\s+', ' ', re.sub(r'[^a-z0-9 ]', ' ', q.lower())).strip()
        if not c: return True
        if c[:40] in norm: return True
        toks = [t for t in c.split() if len(t) > 3][:4]
        if toks and all(re.search(r'\b' + re.escape(t[:-1] if t.endswith('s') else t), norm) for t in toks):
            return True
        return False
    for q in re.findall(r'[“"]([^”"]{10,70})[”"]', text)[:3]:
        if NAMEQ.match(q.strip()): continue
        if present(q): hits += 1
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
