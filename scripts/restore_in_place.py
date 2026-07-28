#!/usr/bin/env python3
"""restore_in_place.py — seat recovered blog bodies into EXISTING deposits.

EA-RESTORATION in-place pass, 2026-07-28. Targets: deposits with
canonical_text_status == metadata_only whose truth title matches a live blog
URL in the DOI resolution index (plus slug candidates from the blog inventory).

This is NOT the mint harness (restore_from_blog.py mints queue works that were
never deposited). This instrument performs the recorded-correction protocol
established 2026-07-04 and refined 2026-07-19/21 on records that already exist:

  fetch → Blogger body extract → BODY-HEAD GATE (contain >= 0.75 against the
  deposit's truth title; the post body is the source of truth — titles/slugs
  go stale under authorial overwrite practice) → legal-name hygiene scan
  (regex reused from the mint harness at runtime; the literal never enters
  this file or any output) → seat canonical body with provenance header and
  the superseded capture retained as appendix → new hash, new glyph, AXN
  recomposed same-family, version v0.2-restored, restoration dict,
  remediation note → two-axis update: canonical_text_status =
  recovered_full_text, body_status = full / RESTORED-20260728.

Idempotent: records whose body_status.recovery_status starts with RESTORED
are skipped on re-run. Held cases (gate miss, fetch fail, hygiene flag) are
never written; they land in the report for MANUS reading-pass adjudication.

USAGE: python3 scripts/restore_in_place.py [--limit N] [--dry-run]
Report: data/restoration-inplace-2026-07-28.json
"""
import argparse, datetime, hashlib, json, re, sys, time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'scripts'))
from restore_from_blog import norm, fetch, extract_post, body_gate, slug_candidates, load_inventory
from axn_lib import axn_glyph_from_hash, axn_clusters_from_hash, axn_reading_from_clusters, compose_axn

try:
    import html2text
    _H = html2text.HTML2Text(); _H.body_width = 0
    to_md = lambda h: _H.handle(h)
except ImportError:
    to_md = lambda h: re.sub(r'<[^>]+>', '', h)

# Legal-name hygiene regex, reused from the mint harness at runtime.
_src = open(ROOT / 'scripts' / 'restore_from_blog.py').read()
_m = re.search(r"re\.search\(r'([^']+)',\s*html\):\s*\n\s*e\[[^\]]*\]\s*=\s*\{'reason':\s*'legal_name_hygiene'", _src)
if not _m:
    raise SystemExit("hygiene regex not found in harness; refusing to run without the scan")
LEGAL_RX = re.compile(_m.group(1))

REPORT = ROOT / 'data' / 'restoration-inplace-2026-07-28.json'
TODAY = '2026-07-28'


def build_targets(reg, dri):
    blogmap = {}
    for m in dri['mappings']:
        b = (m.get('live_urls') or {}).get('blog', '')
        t = norm(m.get('title', ''))
        if b and t:
            blogmap.setdefault(t, {'urls': [], 'alt': [], 'dois': []})
            lane = 'urls' if ('blogspot.com' in b or 'blogger.com' in b) else 'alt'
            if b not in blogmap[t][lane]:
                blogmap[t][lane].append(b)
            dd = m.get('dead_doi')
            if dd and dd not in blogmap[t]['dois']:
                blogmap[t]['dois'].append(dd)
    targets = []
    for d in reg['deposits']:
        if d.get('canonical_text_status') != 'metadata_only':
            continue
        bs = d.get('body_status') or {}
        if str(bs.get('recovery_status', '')).startswith('RESTORED'):
            continue
        hit = blogmap.get(norm(d.get('title', '')))
        if hit:
            targets.append((d, hit['urls'], hit['dois'], hit.get('alt', [])))
    return targets


def gate_extended(title, tt, md):
    """Base body-head gate, plus a stricter-bar test on the title CORE
    (decoration stripped at first parenthetical / em-dash tail): long
    registered titles carry apparatus their body heads never repeat.
    Core test requires >=4 tokens and contain >= 0.85 — higher precision
    on the shorter string, same body-is-truth doctrine."""
    if body_gate(tt, md):
        return True
    core = re.split(r'\s+\u2014\s+|\s*\(', title, 1)[0]
    ct = norm(core)
    head = norm(md[:1200])[:800]
    from restore_from_blog import contain
    return len(ct.split()) >= 4 and contain(ct, head) >= 0.85


def restore_one(d, urls, dois, alt, inventory, cache, dry):
    n = d['deposit_number']
    tp0 = (d.get('full_text_path') or f"/data/texts/AXN-{d['hex']}-text.md").lstrip('/')
    if (ROOT / tp0).exists():
        _existing = (ROOT / tp0).read_text(errors='replace')
        if 'Restoration status:** RESTORED (v0.2) — full text recovered and seated' in _existing[:1500] and 'restore_in_place' not in str((d.get('body_status') or {}).get('audit_version','')):
            # File restored by an interrupted run; registry not yet updated. Repair from file.
            _m = re.search(r'Recovered from (\S+) under', _existing)
            url = _m.group(1) if _m else '(interrupted-run source)'
            h = hashlib.sha256(_existing.encode('utf-8')).hexdigest()
            glyph = axn_glyph_from_hash(h)
            old_axn = d.get('axn')
            d['hash'] = h; d['axn_canonical'] = h; d['emoji'] = glyph
            d['axn'] = compose_axn(d['hex'], d.get('family','ARCHIVAL'), glyph)
            d['clusters'] = axn_clusters_from_hash(h)
            d['reading'] = axn_reading_from_clusters(d['clusters'])
            d['version'] = 'v0.2-restored'
            d['full_text_path'] = '/' + tp0
            r = d.get('restoration') if isinstance(d.get('restoration'), dict) else {}
            r.update({'fulltext':'restored','fulltext_source':url,'restored_at':TODAY,'axn_before_restoration':old_axn,'dead_dois':dois})
            d['restoration'] = r
            d['remediation_note'] = (f"{TODAY} FULL-TEXT RESTORATION (in-place): canonical body upgraded from metadata capture to recovered full text ({url}); new hash and glyph; capture body retained as appendix; v0.1 metadata body superseded by this recorded correction.")
            d['canonical_text_status'] = 'recovered_full_text'
            d['body_status'] = {'class':'full','lacuna':False,'recovery_status':'RESTORED-20260728','recovered_from':url,'residual_chars':len(_existing),'audited_at':datetime.datetime.now(datetime.UTC).isoformat(),'audit_version':'restore_in_place-20260728'}
            return ('restored', {'n': n, 'axn_old': old_axn, 'axn_new': d['axn'], 'url': url, 'chars': len(_existing), 'repaired_from_interrupt': True})
    tt = norm(d.get('title', ''))
    candidates = list(urls)
    for cand in slug_candidates(d.get('title', ''), inventory, k=10, min_ov=2):
        u = cand[0] if isinstance(cand, (list, tuple)) else cand
        if u not in candidates:
            candidates.append(u)
    matched = None
    for url in candidates[:12]:
        try:
            if url in cache:
                raw = cache[url]
            else:
                raw = fetch(url); cache[url] = raw; time.sleep(0.8)
            html = raw.decode('utf-8', 'replace')
        except Exception as ex:
            continue
        ptitle, body = extract_post(html)
        if not body:
            continue
        md = to_md(body).strip()
        if gate_extended(d.get('title', ''), tt, md):
            matched = (url, html, md)
            break
    if not matched:
        if not urls and alt:
            return ('held', {'n': n, 'reason': 'non_blog_source', 'lane': 'REPO-FETCH/OTHER-SUBSTRATE', 'detail': alt[0]})
        return ('held', {'n': n, 'reason': 'gate', 'detail': f'no candidate of {len(candidates[:12])} passed body-head gate'})
    url, html, md = matched
    if LEGAL_RX.search(html) or LEGAL_RX.search(md):
        return ('held', {'n': n, 'reason': 'legal_name_hygiene', 'detail': url})
    if dry:
        return ('would_restore', {'n': n, 'url': url, 'chars': len(md)})

    hex_id, family = d['hex'], d.get('family', 'ARCHIVAL')
    old_axn = d.get('axn')
    tp = (d.get('full_text_path') or f'/data/texts/AXN-{hex_id}-text.md').lstrip('/')
    old_body = ''
    if (ROOT / tp).exists():
        old_body = (ROOT / tp).read_text(errors='replace').strip()
    doiline = ', '.join(dois) if dois else '(none mapped)'
    header = (
        f"# {d.get('title')}\n\n"
        f"**{d.get('creator')}** · restored {TODAY}\n\n"
        f"**AXN:** AXN:{hex_id} — Alexanarch deposit #{n} (self-reference in root form by pre-hash necessity)\n"
        f"**Restoration status:** RESTORED (v0.2) — full text recovered and seated as the canonical body. "
        f"Recovered from {url} under the in-place restoration pass (EA-AVAILABILITY-INTEGRITY-01 follow-on). "
        f"Body-head gate passed against the truth title; the post body is the source of truth (titles/slugs may be "
        f"stale per authorial overwrite practice). These bytes are the head of the work's version chain as held on "
        f"the blog at fetch time.\n"
        f"**Dead DOI(s):** {doiline} — severed 2026-06-19.\n\n---\n\n"
    )
    appendix = ''
    if old_body:
        appendix = ("\n\n---\n\n## Appendix — metadata-capture body (superseded 2026-07-28, retained per non-destruction)\n\n"
                    + old_body + "\n")
    body_text = header + md + appendix
    (ROOT / tp).write_text(body_text, encoding='utf-8')

    h = hashlib.sha256(body_text.encode('utf-8')).hexdigest()
    glyph = axn_glyph_from_hash(h)
    d['hash'] = h
    d['axn_canonical'] = h
    d['emoji'] = glyph
    d['axn'] = compose_axn(hex_id, family, glyph)
    d['clusters'] = axn_clusters_from_hash(h)
    d['reading'] = axn_reading_from_clusters(d['clusters'])
    d['version'] = 'v0.2-restored'
    d['full_text_path'] = '/' + tp
    r = d.get('restoration') if isinstance(d.get('restoration'), dict) else {}
    r.update({'fulltext': 'restored', 'fulltext_source': url, 'restored_at': TODAY,
              'axn_before_restoration': old_axn,
              'dead_dois': dois})
    d['restoration'] = r
    d['remediation_note'] = (f"{TODAY} FULL-TEXT RESTORATION (in-place): canonical body upgraded from metadata capture "
                             f"to recovered full text ({url}); new hash and glyph; capture body retained as appendix; "
                             f"v0.1 metadata body superseded by this recorded correction.")
    d['canonical_text_status'] = 'recovered_full_text'
    d['body_status'] = {'class': 'full', 'lacuna': False,
                        'recovery_status': 'RESTORED-20260728',
                        'recovered_from': url,
                        'residual_chars': len(body_text),
                        'audited_at': datetime.datetime.now(datetime.UTC).isoformat(),
                        'audit_version': 'restore_in_place-20260728',
                        'class_before_restoration': (d.get('body_status') or {}).get('class') if isinstance(d.get('body_status'), dict) else None}
    return ('restored', {'n': n, 'axn_old': old_axn, 'axn_new': d['axn'], 'url': url, 'chars': len(md)})


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--limit', type=int, default=0)
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--retry-held', action='store_true')
    a = ap.parse_args()
    reg = json.load(open(ROOT / 'data' / 'registry.json'))
    dri = json.load(open(ROOT / 'data' / 'doi-resolution-index.json'))
    inventory = load_inventory()
    targets = build_targets(reg, dri)
    if not a.retry_held and REPORT.exists():
        prev = json.load(open(REPORT))
        held_ns = {h['n'] for h in prev.get('held', [])}
        targets = [t for t in targets if t[0]['deposit_number'] not in held_ns]
        print(f"skipping {len(held_ns)} previously-held (use --retry-held to include)")
    if a.limit:
        targets = targets[:a.limit]
    print(f"targets: {len(targets)} | dry_run={a.dry_run}")
    cache, out = {}, {'restored': [], 'held': [], 'would_restore': []}
    def _save():
        if not a.dry_run:
            reg['last_updated'] = datetime.datetime.now(datetime.UTC).strftime('%Y-%m-%dT%H:%M:%SZ')
            json.dump(reg, open(ROOT / 'data' / 'registry.json', 'w'), ensure_ascii=False, indent=2)
    for i, (d, urls, dois, alt) in enumerate(targets):
        kind, rec = restore_one(d, urls, dois, alt, inventory, cache, a.dry_run)
        if kind == 'restored' and len(out['restored']) % 5 == 4:
            _save()
        out[kind].append(rec)
        tag = {'restored': 'OK  ', 'would_restore': 'DRY ', 'held': 'HELD'}[kind]
        print(f"{tag} #{rec['n']:>4} {str(d.get('title'))[:58]}" + (f" | {rec.get('reason')}" if kind == 'held' else f" | {rec.get('chars','?')}ch"))
    if not a.dry_run:
        reg['last_updated'] = datetime.datetime.now(datetime.UTC).strftime('%Y-%m-%dT%H:%M:%SZ')
        json.dump(reg, open(ROOT / 'data' / 'registry.json', 'w'), ensure_ascii=False, indent=2)
    if REPORT.exists() and not a.retry_held:
        prev = json.load(open(REPORT))
        seen = {h['n'] for h in out['held']}
        out['held'] += [h for h in prev.get('held', []) if h['n'] not in seen]
        seenr = {r0['n'] for r0 in out['restored']}
        out['restored'] += [r0 for r0 in prev.get('restored', []) if r0['n'] not in seenr]
    json.dump({'run_at': datetime.datetime.now(datetime.UTC).isoformat(),
               'counts': {k: len(v) for k, v in out.items()}, **out},
              open(REPORT, 'w'), ensure_ascii=False, indent=1)
    print(f"\nrestored: {len(out['restored'])} | held: {len(out['held'])} | dry: {len(out['would_restore'])}")
    print(f"report: {REPORT.relative_to(ROOT)}")


if __name__ == '__main__':
    main()
