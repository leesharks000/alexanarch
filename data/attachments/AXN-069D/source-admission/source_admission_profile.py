#!/usr/bin/env python3
"""source_admission_profile.py — what enters composition through the cards, by source class, over time.

Unit: one observation (an entry, and each item of its `observations`) that carries a
`cite_list`. Each cited source is classed twice: by the registry's own `rel`
(authored_surface · archive_controlled · third_party · authority_transfer ·
external_attestation · other) and by platform (the host family). Output: per month ×
surface, the admitted set's composition; per address with ≥2 observations, the diff;
per observation, whether the archive-side material was admitted to the cards (C) and,
where the record says so, used in the answer (A). Organic sets (O) are recorded only
where a capture noted them; that is the gap this profile makes visible.
Read-only. Writes JSON + a markdown report to the given --out.
"""
import json, re, collections, argparse, pathlib, datetime
ap=argparse.ArgumentParser(); ap.add_argument('--captures',required=True); ap.add_argument('--out',required=True); a=ap.parse_args()
c=json.load(open(a.captures,encoding='utf-8')); E=c['entries']
ARCHIVE_HOSTS=('alexanarch','leesharks','machinemediation','provenanceerasure','operativesemiotics','semanticeconomy','semanticphysics','axnidentifiers','spxi','lagrangeobservatory','godkinggoogle','revelationfirst','crimsonhexagonal','traininglayerliterature','metadatapacket','restoredacademy','vpcor','watergiraffe','secretbookofwalt','laborvector','surfacemap','mindcontrolpoems','mind control poems','chatgptpsychosis','pessoa','encyclotron','concordance','holographic','negentropic','themandalaoracle','lee-sharks','crimson hexagon')
AUTHORED_3P=('medium','academia','zenodo','github','scilynk','substack','hugging face','huggingface','figshare','scribd','google scholar','orcid','wikidata','goodreads','amazon','archive.org','researchgate','philarchive','philpapers','ssrn','wikiversity')
def platform(site):
    s=(site or '').lower()
    if any(h in s for h in ARCHIVE_HOSTS): return 'archive-owned'
    if 'wikipedia' in s: return 'wikipedia'
    if 'youtube' in s: return 'youtube'
    if any(h in s for h in ('reddit','facebook','quora','twitter','x.com','linkedin','tiktok','instagram')): return 'social'
    if any(h in s for h in ('medium','substack')): return 'medium/substack'
    if any(h in s for h in ('academia','zenodo','figshare','researchgate','philarchive','philpapers','ssrn','arxiv','scholar','orcid','wikidata','scilynk')): return 'scholarly platform'
    if any(h in s for h in ('sciencedirect','mdpi','springer','wiley','nature','tandfonline','jstor','cambridge','oxford','sage','de gruyter','brill','frontiers','plos','pubmed','acm','ieee')): return 'publisher'
    if any(h in s for h in ('github','hugging','stackoverflow','npm','pypi')): return 'code/data platform'
    if any(h in s for h in ('.edu','university','toronto','harvard','mit ','stanford','college')): return 'university'
    if any(h in s for h in ('collins','merriam','dictionary','britannica','wiktionary','vocabulary')): return 'reference'
    return 'other web'
def relclass(x):
    # The registry's `rel` vocabulary drifted across seatings: June–August used authored_surface /
    # archive_controlled for the archive's own surfaces; the 11 September re-measurements used
    # authority_transfer for alexanarch.org and Medium. So archive-side is decided by host and
    # by rel together, and the drift is recorded as a finding rather than hidden.
    r=(x.get('rel') or '').lower(); site=(x.get('site') or '').lower()
    if platform(x.get('site'))=='archive-owned' or r in ('authored_surface','archive_controlled','archive_lineage','identifier_record','authority_transfer') or any(k in site for k in ('lee sharks','johannes sigil','crimson','rebekah cranes','sigil')): return 'archive-side'
    if r in ('third_party','third_party_index','external_attestation'): return 'third-party'
    if r in ('capture_of_capture',): return 'capture-of-capture'
    return 'unclassed'
units=[]
for e in E:
    obs=[o for o in (e.get('observations') or []) if isinstance(o,dict)]
    # An entry that carries observations is a container: its own top-level cite_list mirrors
    # observation 1 (the 2026-08-27 format). Counting both double-counted 113 observations in
    # the first run. Units are observations where they exist, else the entry.
    srcs=obs if obs else [e]
    for o in srcs:
        cl=o.get('cite_list') if isinstance(o.get('cite_list'),list) and o.get('cite_list') else (e.get('cite_list') if (o is e or (obs and o is obs[0])) else None)
        if not cl: continue
        date=o.get('date') or e.get('date'); surface=o.get('surface') or e.get('surface'); auth=o.get('auth') or e.get('auth')
        text=(str(o.get('transcript') or '')+' '+str(o.get('d') or '')+' '+str(e.get('sf') or '')+' '+str(e.get('reading') or ''))
        organic=bool(re.search(r'organic',text,re.I)); organic_first=re.search(r'(?:first organic result|ORGANIC #1)[^\n]{0,200}',text)
        uncited=bool(re.search(r'uncited|not cited|not among the cited|cited nowhere',text,re.I))
        rows=[]
        for x in cl:
            if not isinstance(x,dict): continue
            rows.append({'site':x.get('site'),'rel':x.get('rel'),'relclass':relclass(x),'platform':platform(x.get('site')),'title':(x.get('title') or '')[:80]})
        n=len(rows); arch=sum(1 for r in rows if r['relclass']=='archive-side')
        units.append({'slug':e['slug'],'obs_slug':o.get('slug') if o is not e else None,'addr_id':e.get('addr_id'),'q':e.get('q'),'section':e.get('s'),'date':date,'month':(date or '')[:7],'surface':surface,'auth':auth,'n_sources':n,'archive_side':arch,'archive_share':round(arch/n,3) if n else None,'platforms':collections.Counter(r['platform'] for r in rows),'relclasses':collections.Counter(r['relclass'] for r in rows),'organic_noted':organic,'organic_first':organic_first.group(0) if organic_first else None,'archive_ranked_uncited':uncited and organic,'sources':rows})
# aggregates
def agg(key):
    g=collections.defaultdict(lambda:{'obs':0,'sources':0,'archive':0,'platforms':collections.Counter(),'relclasses':collections.Counter(),'organic_noted':0,'ranked_uncited':0})
    for u in units:
        k=key(u); d=g[k]; d['obs']+=1; d['sources']+=u['n_sources']; d['archive']+=u['archive_side']; d['platforms'].update(u['platforms']); d['relclasses'].update(u['relclasses']); d['organic_noted']+=u['organic_noted']; d['ranked_uncited']+=u['archive_ranked_uncited']
    out={}
    for k,d in g.items():
        out[k]={'observations':d['obs'],'sources':d['sources'],'archive_side_share':round(d['archive']/d['sources'],3) if d['sources'] else None,'platforms':dict(d['platforms'].most_common()),'relclasses':dict(d['relclasses']),'organic_noted':d['organic_noted'],'archive_ranked_uncited':d['ranked_uncited']}
    return dict(sorted(out.items(),key=lambda kv:str(kv[0])))
by_month=agg(lambda u:u['month']); by_surface=agg(lambda u:(u['surface'] or '').split('(')[0].strip()); by_month_surface=agg(lambda u:f"{u['month']} | {(u['surface'] or '').split('(')[0].strip()}")
# longitudinal diffs per address
byaddr=collections.defaultdict(list)
for u in units: byaddr[u['addr_id'] or u['slug']].append(u)
diffs=[]; replication=0
for k,us in byaddr.items():
    if len(us)<2: continue
    us=sorted(us,key=lambda u:u['date'] or '')
    # WITHIN-SESSION REPLICATION vs CROSS-DATE STATE CHANGE. Same-date observations with the
    # same card set are replications and do not count as transitions.
    seen={}; kept=[]
    for u in us:
        sig=(u['date'],tuple(sorted((x['site'] or '') for x in u['sources'])))
        if sig in seen: replication+=1; continue
        seen[sig]=1; kept.append(u)
    us=kept
    if len({u['date'] for u in us})<2: continue
    first,last=us[0],us[-1]
    diffs.append({'addr_id':k,'q':first['q'],'surface':first['surface'],'dates':[u['date'] for u in us],'archive_share':[u['archive_share'] for u in us],'n_sources':[u['n_sources'] for u in us],'platforms_first':dict(first['platforms']),'platforms_last':dict(last['platforms']),'sites_lost':sorted({s['site'] for s in first['sources']}-{s['site'] for s in last['sources']}),'sites_gained':sorted({s['site'] for s in last['sources']}-{s['site'] for s in first['sources']})})
out=pathlib.Path(a.out); out.mkdir(parents=True,exist_ok=True)
json.dump({'built':datetime.date.today().isoformat(),'units':len(units),'by_month':by_month,'by_surface':by_surface,'by_month_surface':by_month_surface,'longitudinal':diffs,'within_session_replications_dropped':replication,'observations':[{k:(dict(v) if isinstance(v,collections.Counter) else v) for k,v in u.items()} for u in units]},open(out/'source-admission-profile.json','w'),ensure_ascii=False,indent=1)
L=[]; L.append(f"# Source admission profile — what enters composition through the cards\n\nBuilt {datetime.date.today()} from the Capture Registry: {len(units)} observations carry a cite_list (of 428 entries / 588 observations). Organic sets are noted in prose on {sum(1 for u in units if u['organic_noted'])} of them and are not structured anywhere — the gap this profile exists to show.\n")
L.append("## By month\n\n| month | obs | sources | archive-side share | top platforms | organic noted | archive ranked & uncited |\n|---|---|---|---|---|---|---|")
for m,d in by_month.items(): L.append(f"| {m} | {d['observations']} | {d['sources']} | {d['archive_side_share']} | {', '.join(f'{k} {v}' for k,v in list(d['platforms'].items())[:5])} | {d['organic_noted']} | {d['archive_ranked_uncited']} |")
L.append("\n## By surface\n\n| surface | obs | sources | archive-side share | top platforms |\n|---|---|---|---|---|")
for s,d in by_surface.items(): L.append(f"| {s} | {d['observations']} | {d['sources']} | {d['archive_side_share']} | {', '.join(f'{k} {v}' for k,v in list(d['platforms'].items())[:5])} |")
L.append("\n## By month × surface (Google AI Overview and ChatGPT only)\n\n| month · surface | obs | sources | archive-side share | platforms |\n|---|---|---|---|---|")
for k,d in by_month_surface.items():
    if 'AI Overview' in k or 'ChatGPT' in k or 'AI Mode' in k: L.append(f"| {k} | {d['observations']} | {d['sources']} | {d['archive_side_share']} | {', '.join(f'{k2} {v}' for k2,v in list(d['platforms'].items())[:6])} |")
L.append(f"\n## Longitudinal — addresses with cross-date carded observations ({len(diffs)}; {replication} same-date replications dropped)\n\n| address | surface | dates | archive share per obs | sources per obs | lost | gained |\n|---|---|---|---|---|---|---|")
for d in sorted(diffs,key=lambda d:d['dates'][0]): L.append(f"| {d['q'][:50]} | {(d['surface'] or '')[:22]} | {' → '.join(d['dates'])} | {' → '.join(str(x) for x in d['archive_share'])} | {' → '.join(str(x) for x in d['n_sources'])} | {', '.join(d['sites_lost'])[:80]} | {', '.join(d['sites_gained'])[:80]} |")
open(out/'source-admission-profile.md','w',encoding='utf-8').write('\n'.join(L)+'\n')
print('units',len(units),'diffs',len(diffs)); print('\n'.join(L[:20]))
