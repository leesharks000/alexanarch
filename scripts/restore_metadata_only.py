#!/usr/bin/env python3
"""
restore_metadata_only.py — semi-restored mints for queue works with no live source.

For each metadata_only queue entry: pull the richest available capture
(tier 1: DataCite full backup; tier 2: tombstone-mirror citation_text + removal
forensics) and mint a SEMI-RESTORED record: all captured metadata rendered, no
full text, provenance and removal evidence preserved in the body. Precedent:
the #969–#971 semi-restored class. Queue entries gain
restored: {deposit_number, axn, date, semi: true}.

USAGE: python3 scripts/restore_metadata_only.py [--dry-run] [--limit N]
Mint-only (fast); run shared stages via restore_from_blog.py --finish
(it collects every stages_pending marker regardless of harness).
"""
import argparse, json, re, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
QUEUE = ROOT / 'datasets' / 'doi-work-identity' / 'restoration-queue.json'

def load_sources():
    dc = json.load(open(ROOT/'data'/'datacite-full-backup.json'))
    dcrecs = dc['records'] if isinstance(dc, dict) and 'records' in dc else dc
    bydoi = {}
    for r in dcrecs:
        a = r.get('attributes', r)
        d = (a.get('doi') or '').lower()
        if d: bydoi[d if d.startswith('10.') else '10.5281/zenodo.'+d] = a
    tomb = {}
    for line in open(ROOT/'datasets'/'tombstone-mirror'/'tombstone-api.jsonl'):
        try: r = json.loads(line)
        except Exception: continue
        rid = str(r.get('record_id') or '')
        if rid: tomb['10.5281/zenodo.'+rid] = r
    return bydoi, tomb

def parse_citation(ct):
    m = re.match(r'^(?P<au>.+?)\s+\((?P<yr>\d{4})(?:,[^)]*)?\)\.\s+(?P<rest>.+?)\.\s+Zenodo\.', ct or '')
    if not m: return None
    rest = m.group('rest')
    ver = None
    vm = re.search(r'\s+\(([^()]{1,20})\)$', rest)
    if vm: ver = vm.group(1); rest = rest[:vm.start()]
    return {'creators': m.group('au'), 'year': m.group('yr'), 'title': rest, 'version': ver}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--limit', type=int, default=100)
    args = ap.parse_args()
    bydoi, tomb = load_sources()
    q = json.load(open(QUEUE))
    reg = json.load(open(ROOT/'data'/'registry.json'))
    next_issue = max(d['deposit_number'] for d in reg['deposits']) + 1
    done = 0
    for e in q['metadata_only']:
        if e.get('restored') or e.get('skip') or done >= args.limit: continue
        ds = [d.lower() for d in e['dois']]
        a = next((bydoi[d] for d in ds if d in bydoi), None)
        tb = next((tomb[d] for d in ds if d in tomb), None)
        ts = ((tb or {}).get('api') or {}).get('tombstone') or {}
        cit = parse_citation(ts.get('citation_text'))
        if a:
            tier = 'DataCite full-metadata capture'
            title = (a.get('titles') or [{}])[0].get('title') or e['title']
            creators = '; '.join(c.get('name','') for c in (a.get('creators') or [])) or 'Sharks, Lee'
            descs = ' '.join(d.get('description','') for d in (a.get('descriptions') or []))
            subjects = ', '.join(s.get('subject','') for s in (a.get('subjects') or []))
            year = str(a.get('publicationYear') or '')
        elif cit:
            tier = 'Zenodo tombstone citation_text capture'
            title, creators, year = cit['title'], cit['creators'], cit['year']
            descs, subjects = '', ''
        else:
            e['skip'] = {'reason': 'no_metadata_source', 'date': '2026-07-19'}
            print(f"SKIP  {e['dois'][0]} | no metadata source | {e['title'][:50]}")
            continue
        date = e['date'] if e.get('date') and e['date'] != '9999' else (year + '-01-01' if year else '2026-01-01')
        removal = ''
        if ts:
            removal = (f"Zenodo removal forensics: removal_date {ts.get('removal_date','?')}, "
                       f"removal_reason {((ts.get('removal_reason') or {}).get('id','?'))}, "
                       f"removed_by user {((ts.get('removed_by') or {}).get('user','?'))}. ")
        desc_body = (descs or f"Metadata-only capture of a work severed at Zenodo; full text not yet recovered from any surviving surface.")
        desc = (f"SEMI-RESTORED RECORD (metadata capture only; no full text). Source tier: {tier}. "
                f"DOI(s): {', '.join(e['dois'])}. {removal}" + re.sub(r'\s+',' ', desc_body)[:600] +
                " Restored under the metadata_only class of /datasets/doi-work-identity/restoration-queue.json; "
                "if canonical bytes surface, a full-text version supersedes this record per the versioning protocol.")
        kw = 'Crimson Hexagonal Archive, semi-restored, metadata-only, severed DOI, Zenodo termination'
        if subjects: kw += ', ' + subjects[:200]
        rel = '; '.join(f"https://doi.org/{d} (severed)" for d in e['dois'])
        cite_line = ('Captured citation: ' + ts.get('citation_text','')) if ts.get('citation_text') else ''
        body_md = f"""### Protocol Version

alexanarch-deposit-protocol/v1

### Title

{title}

### Creator

{creators}

### ORCID

0009-0000-1599-0703

### Date

{date}

### Description

{desc}

### Content Type

Semi-restored record (metadata-only; {tier})

### License

CC-BY-4.0

### Substrate Disclosure

Human-only original; metadata capture assembled and framed by TACHYON in-session (transport D, No-Double-Draw).

### Keywords

{kw}

### Related Identifiers

{rel}

### Version

semi-restored v1.0

### Methodology

Assembled from {tier}; no live authorial surface passed the body-head gate or existed for this work at restoration time. All captured fields rendered verbatim in the body.

### Falsification Conditions

Superseded on sight by any recovered canonical bytes; the captured metadata is verifiable against the DataCite API historical record and the Zenodo tombstone.

### Files

_No response_

### Body

## SEMI-RESTORED RECORD — metadata capture only

**Work:** {title}
**Severed DOI(s):** {', '.join(e['dois'])}
**Source tier:** {tier}
**Creators (as captured):** {creators}
{cite_line}

{('**Removal forensics:** ' + removal) if removal else ''}

{('**Captured description:** ' + desc_body) if descs else 'No abstract survived in the capture; the title, creators, date, and DOIs above are the recovered identity of the work.'}

{('**Captured subjects:** ' + subjects) if subjects else ''}

---

*Full text not yet recovered. If the canonical bytes surface on any authorial surface, a full-text version supersedes this record in-series per the versioning protocol. This record exists so the DOI resolves to the work's true identity rather than to silence.*

### Terms

- [x] I have read and agree to the deposit protocol.
"""
        if args.dry_run:
            print(f"DRY   {e['dois'][0]} | {tier[:20]} | would mint #{next_issue} | {title[:45]}")
            next_issue += 1; done += 1; continue
        bp = Path(f"/tmp/semi-{next_issue}.md"); bp.write_text(body_md)
        r = subprocess.run([sys.executable, 'scripts/deposit_pipeline.py', '--issue-body', str(bp),
                            '--issue-number', str(next_issue), '--stages', 'mint'],
                           cwd=ROOT, capture_output=True, text=True)
        mm = re.search(r'minted \+ inserted: #(\d+) · (AXN:\S+)', r.stdout)
        if mm:
            e['restored'] = {'deposit_number': int(mm.group(1)), 'axn': mm.group(2),
                             'date': '2026-07-19', 'semi': True, 'stages_pending': True}
            print(f"MINT  {e['dois'][0]} → #{mm.group(1)} ({tier.split()[0]}) | {title[:45]}")
        else:
            e['skip'] = {'reason': 'pipeline_failure', 'date': '2026-07-19'}
            print(f"FAIL  {e['dois'][0]} | {r.stdout[-200:]}{r.stderr[-150:]}")
        next_issue += 1; done += 1
        json.dump(q, open(QUEUE, 'w'), ensure_ascii=False, indent=1)
    json.dump(q, open(QUEUE, 'w'), ensure_ascii=False, indent=1)
    print('metadata-only pass complete:', done)

if __name__ == '__main__':
    main()
