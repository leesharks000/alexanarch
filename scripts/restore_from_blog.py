#!/usr/bin/env python3
"""
restore_from_blog.py — batch restoration of queue works from live blog surfaces.

Reads datasets/doi-work-identity/restoration-queue.json (class: restorable).
For each work, IN ORDER: fetch candidate blog URL(s) → extract Blogger post body →
TITLE-VERIFICATION GATE (the candidate URL is only the post the DOI was FOUND IN;
mint only if the fetched post's title matches this work's DOI-keyed truth title;
mismatches are skipped and logged, never minted) → legal-name hygiene scan →
html2text canonical markdown + SHA-256 of raw fetch → issue body → deposit_pipeline
(transport D, full stages, --no-push; commits are local until the operator pushes).

Creator is taken from the OpenAlex snapshot authorships for the work's DOI when
present (creators as recorded), else 'Lee Sharks' with a note — per the standing
batch-restoration authorization pattern (MANUS 2026-07-03; renewed 2026-07-19).

USAGE: python3 scripts/restore_from_blog.py --limit 8 [--offset 0] [--dry-run]
Progress is tracked in the queue file itself: each restored entry gains
restored: {deposit_number, axn, date}; each skip gains skip: {reason, date}.
Re-runs resume past entries carrying either marker.
"""
import argparse, hashlib, json, re, subprocess, sys, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
QUEUE = ROOT / 'datasets' / 'doi-work-identity' / 'restoration-queue.json'

def norm(t):
    t = re.sub(r'\[SUPERSEDED[^\]]*\]', '', t or '')
    return ' '.join(re.sub(r'[^0-9a-z ]', '', t.lower().replace('\u00a0', ' ')).split())

def jacc(a, b):
    sa, sb = set(a.split()), set(b.split())
    return len(sa & sb) / max(1, len(sa | sb))

def contain(a, b):
    sa, sb = set(a.split()), set(b.split())
    return len(sa & sb) / max(1, min(len(sa), len(sb)))

def fetch(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'alexanarch-restoration/1.0'})
    return urllib.request.urlopen(req, timeout=30).read()

def extract_post(html):
    m = re.search(r"<title>(?:Mind Control Poems:?\s*)?([^<]+)</title>", html)
    page_title = (m.group(1).strip() if m else '')
    b = re.search(r"<div class='post-body entry-content[^']*'[^>]*>(.*?)<div class='post-footer'>", html, re.S) \
        or re.search(r'<div class="post-body entry-content[^"]*"[^>]*>(.*?)<div class="post-footer">', html, re.S)
    return page_title, (b.group(1) if b else None)

STOP = {'the','a','an','of','and','or','in','on','for','to','as','with','by','from','at','crimson','hexagon','archive'}

def load_inventory():
    p = ROOT/'datasets'/'doi-work-identity'/'blog-post-inventory.txt'
    urls = [u.strip() for u in open(p) if u.strip()] if p.exists() else []
    out = []
    for u in urls:
        slug = u.rsplit('/',1)[-1].replace('.html','')
        out.append((u, set(t for t in slug.split('-') if t and t not in STOP)))
    return out

def slug_candidates(title, inventory, k=3, min_ov=3):
    tt = set(t for t in norm(title).split() if t not in STOP)
    scored = []
    for u, stoks in inventory:
        ov = len(tt & stoks)
        if ov >= min_ov or (stoks and ov >= max(2, len(stoks)-1)):
            scored.append((ov, u))
    scored.sort(reverse=True)
    return [u for _, u in scored[:k]]

def body_gate(tt, md):
    """Post body is the source of truth (authorial practice: in-place version overwrites;
    post <title>/slug may be stale). Match truth-title tokens against the BODY HEAD only
    (first ~800 normalized chars) so catalog posts that merely cite the title deeper in
    the body do not false-match."""
    head = norm(md[:1200])[:800]
    return contain(tt, head) >= 0.75

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--limit', type=int, default=5)
    ap.add_argument('--offset', type=int, default=0)
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--batch', action='store_true',
                    help='mint-only per work (fast); shared stages deferred to --finish; queue saved after EVERY work')
    ap.add_argument('--deep', action='store_true', help='wider candidate search: 10 slug candidates, overlap>=2')
    ap.add_argument('--finish', action='store_true',
                    help='run shared stages once for all stages_pending mints, then single commit')
    args = ap.parse_args()
    if args.finish:
        return finish(args)
    import html2text
    global INVENTORY
    INVENTORY = load_inventory()
    q = json.load(open(QUEUE))
    snap = json.load(open(ROOT/'data'/'openalex-severed-recovery.json'))
    recs = next(v for v in snap.values() if isinstance(v, list) and len(v) > 500)
    oa_auth = {}
    for r in recs:
        doi = (r.get('doi') or '').replace('https://doi.org/', '').lower()
        au = [a.get('author', {}).get('display_name') for a in (r.get('authorships') or []) if a.get('author')]
        if doi and au: oa_auth[doi] = au
    reg = json.load(open(ROOT/'data'/'registry.json'))
    next_issue = max(d['deposit_number'] for d in reg['deposits']) + 1
    done = 0
    pending = [e for e in q['restorable'] if not e.get('restored') and not e.get('skip')][args.offset:]
    for e in pending:
        if done >= args.limit: break
        tt = norm(e['title'])
        matched = None
        h2 = html2text.HTML2Text(); h2.body_width = 0
        candidates = slug_candidates(e['title'], INVENTORY, k=(10 if args.deep else 3), min_ov=(2 if args.deep else 3)) + [u for u in e['candidate_blog_urls'] if u]
        seen = set()
        for url in candidates:
            if url in seen: continue
            seen.add(url)
            try:
                raw = fetch(url)
            except Exception:
                continue
            html = raw.decode('utf-8', 'replace')
            ptitle, body = extract_post(html)
            if not body: continue
            md_probe = h2.handle(body).strip()
            if body_gate(tt, md_probe):
                matched = (url, raw, html, ptitle, body); break
        if not matched:
            e['skip'] = {'reason': 'body_gate_no_matching_post', 'date': '2026-07-19'}
            print(f"SKIP  {e['dois'][0]} | {e['title'][:55]} | gate: no candidate post matched")
            continue
        url, raw, html, ptitle, body = matched
        if re.search(r'(?i)pfaff', html):
            e['skip'] = {'reason': 'legal_name_hygiene', 'date': '2026-07-19'}
            print(f"SKIP  {e['dois'][0]} | LEGAL-NAME HYGIENE FLAG — manual review")
            continue
        h = html2text.HTML2Text(); h.body_width = 0
        md = h.handle(body).strip()
        raw_sha = hashlib.sha256(raw).hexdigest()
        md_sha = hashlib.sha256(md.encode()).hexdigest()
        doi = e['dois'][0]
        creators = oa_auth.get(doi.lower()) or ['Lee Sharks']
        desc = (f"Canonical bytes recovered 2026-07-19 from the authorial blog surface ({url}); "
                f"work severed at Zenodo 2026-06-19 (DOI(s): {', '.join(e['dois'])}). Batch restoration under the "
                f"queue at /datasets/doi-work-identity/restoration-queue.json; title verified against the DOI-keyed "
                f"truth title at fetch time. Opening of the work: " + re.sub(r'\s+', ' ', md)[:400])
        rel = '; '.join(f"https://doi.org/{d} (severed)" for d in e['dois'])
        body_md = f"""### Protocol Version

alexanarch-deposit-protocol/v1

### Title

{e['title']}

### Creator

{'; '.join(creators)}

### ORCID

0009-0000-1599-0703

### Date

{e['date'] if e['date'] != '9999' else '2026-01-01'}

### Description

{desc}

### Content Type

Recovered blog-canonical work (full text; queue restoration 2026-07-19)

### License

CC-BY-4.0

### Substrate Disclosure

Human-only (original composition; creators as recorded by OpenAlex/DataCite capture); 2026-07-19 recovery, title-gate verification, and framing by TACHYON in-session under MANUS authorization (queue restoration). No paid API calls (No-Double-Draw, transport D).

### Keywords

Crimson Hexagonal Archive, restoration, blog canonical bytes, severed DOI, Zenodo termination, {', '.join(re.findall(r'[A-Za-z]{4,}', e['title'])[:5])}

### Related Identifiers

{rel}; recovery source: {url}

### Version

v1.0

### Methodology

Fetched {url} (raw SHA-256 {raw_sha}); Blogger post-body extracted; BODY-HEAD gate passed against the DOI-keyed truth title (post body is the source of truth per authorial practice: versioned posts were often overwritten in place without updating post title or slug). Converted via html2text body_width=0 (canonical MD SHA-256 {md_sha}). Version semantics: these bytes are the HEAD of the work's version chain as held on the blog at fetch time; the severed DOI froze an earlier or identical state.

### Falsification Conditions

Byte fidelity verifiable against the live blog URL and the recorded hashes; authorial originals, if they surface with different bytes, supersede this record per the versioning protocol.

### Files

_No response_

### Body

## Recovery note (TACHYON, 2026-07-19)

Restored from {url} under the grade-none restoration queue; DOI(s) {', '.join(e['dois'])} severed 2026-06-19. Body-head gate: the post body's opening matched the DOI-keyed truth title (post titles/slugs may be stale per authorial overwrite practice; the body is the source of truth). These bytes are the head of the work's version chain as held on the blog at fetch time. Canonical bytes below the rule.

---

{md}

### Terms

- [x] I have read and agree to the deposit protocol.
"""
        if args.dry_run:
            print(f"DRY   {doi} | would mint #{next_issue} | {e['title'][:55]}")
            next_issue += 1; done += 1; continue
        bp = Path(f"/tmp/restore-{next_issue}.md"); bp.write_text(body_md)
        stages = ['--stages', 'mint'] if args.batch else []
        r = subprocess.run([sys.executable, 'scripts/deposit_pipeline.py', '--issue-body', str(bp),
                            '--issue-number', str(next_issue), '--no-push'] + stages,
                           cwd=ROOT, capture_output=True, text=True)
        mm = re.search(r'minted \+ inserted: #(\d+) · (AXN:\S+)', r.stdout)
        ok = mm and ('pipeline complete' in r.stdout or args.batch)
        if ok:
            e['restored'] = {'deposit_number': int(mm.group(1)), 'axn': mm.group(2), 'date': '2026-07-19'}
            if args.batch: e['restored']['stages_pending'] = True
            print(f"MINT  {doi} → #{mm.group(1)} {mm.group(2)} | {e['title'][:50]}")
        else:
            e['skip'] = {'reason': 'pipeline_failure', 'date': '2026-07-19'}
            print(f"FAIL  {doi} | pipeline error; tail: {r.stdout[-300:]}{r.stderr[-200:]}")
        next_issue += 1; done += 1
        json.dump(q, open(QUEUE, 'w'), ensure_ascii=False, indent=1)  # save after EVERY work
    json.dump(q, open(QUEUE, 'w'), ensure_ascii=False, indent=1)
    print('tranche complete:', done)

def finish(args):
    """Shared stages, once, for every stages_pending mint; then one commit."""
    import json as J
    q = J.load(open(QUEUE))
    pend = [e for e in q['restorable'] if (e.get('restored') or {}).get('stages_pending')]
    nums = sorted(e['restored']['deposit_number'] for e in pend)
    if not nums:
        print('nothing pending'); return
    print('finishing shared stages for:', nums)
    def sh(cmd, check=True):
        r = subprocess.run([str(c) for c in cmd], cwd=ROOT, capture_output=True, text=True)
        if check and r.returncode != 0:
            print('STAGE FAIL:', ' '.join(str(c) for c in cmd), r.stdout[-300:], r.stderr[-200:]); sys.exit(1)
        return r
    py = sys.executable
    sh([py, 'scripts/validate_deposit.py', '--registry', 'data/registry.json', '--strict'])
    # record pages (in-process, cheap)
    sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT/'scripts'))
    import wire_deposit
    reg = J.load(open(ROOT/'data'/'registry.json'))
    eidx = J.load(open(ROOT/'data'/'entity-index.json'))
    for n in nums:
        d = next(x for x in reg['deposits'] if x['deposit_number'] == n)
        wire_deposit.regenerate_static_page(d, eidx, registry=reg)
    print('record pages:', len(nums))
    sh([py, 'scripts/build_deposit_pdfs.py', f"--deposits={','.join(map(str,nums))}", '--timeout=120', '--force'], check=False)
    sh([py, 'scripts/build_body_index.py'])
    sh([py, 'scripts/regenerate_surfaces.py'])
    for n in nums:  # mechanical enrich, per pipeline doctrine (No-Double-Draw: mechanical flags only)
        sh([py, 'scripts/enrich_deposit.py', '--deposit-number', str(n), '--backlinks'], check=False)
        sh([py, 'scripts/enrich_deposit.py', '--deposit-number', str(n),
            '--wikidata', '--openalex', '--datacite', '--spxi'], check=False)
    sh([py, 'scripts/validate_deposit.py', '--registry', 'data/registry.json', '--strict'])
    for e in pend:
        e['restored'].pop('stages_pending', None)
    J.dump(q, open(QUEUE, 'w'), ensure_ascii=False, indent=1)
    subprocess.run(['git', 'add', '-A'], cwd=ROOT)
    subprocess.run(['git', 'checkout', 'data/pre-overwrite-receipts.log'], cwd=ROOT, capture_output=True)
    msg = (f"RESTORE BATCH · #{nums[0]}–#{nums[-1]} ({len(nums)} works) via restore_from_blog.py --batch/--finish. "
           f"Body-head gate; version-head semantics; shared stages run once per batch; queue markers saved per-work. "
           f"validate --strict clean.")
    subprocess.run(['git', 'commit', '-q', '-m', msg], cwd=ROOT)
    print('batch committed:', len(nums), 'works')

if __name__ == '__main__':
    main()
