#!/usr/bin/env python3
"""harvest_gallery_html.py — recover capture entries from the gallery HTML history.

Before registry.json existed, capture entries lived as JavaScript object literals
inside captures/index.html. Those versions (v4.0 onward) are not in any JSON and
were never harvested. This walks every distinct blob of captures/index.html in all
four repositories and extracts the entries.
"""
import json,os,re,subprocess,sqlite3,collections
HOME='/home/claude'
REPOS={'leesharks.com':'src-leesharks.com','godkinggoogle':'src-godkinggoogle',
       'machinemediation':'src-machinemediation-org','alexanarch':'src-alexanarch'}
def git(repo,*a):
    return subprocess.run(['git','-C',os.path.join(HOME,repo)]+list(a),capture_output=True,text=True,errors='replace').stdout
# JS object literal with the known field set, tolerant of order and extra fields
ENTRY=re.compile(r'\{(?=[^{}]*slug:)([^{}]*?)\}',re.S)
FIELD=re.compile(r'(\w+)\s*:\s*"((?:[^"\\]|\\.)*)"')
def parse(html):
    out=[]
    for m in ENTRY.finditer(html):
        d={k:v for k,v in FIELD.findall(m.group(1))}
        if 'slug' in d and ('q' in d or 'date' in d):
            out.append({k:bytes(v,'utf-8').decode('unicode_escape') if '\\' in v else v for k,v in d.items()})
    return out
rows=[]
for src,repo in REPOS.items():
    log=[l.split() for l in git(repo,'log','--all','--format=%H|%ad','--date=short','--','captures/index.html').replace('|',' ').strip().split('\n') if l.strip()]
    seen={}
    for commit,date in log:
        sha=subprocess.run(['git','-C',os.path.join(HOME,repo),'rev-parse','%s:captures/index.html'%commit],
                           capture_output=True,text=True).stdout.strip()
        if not sha or sha in seen: 
            if sha: seen[sha]['dates'].append(date)
            continue
        html=git(repo,'cat-file','-p',sha)
        ents=parse(html)
        ver=re.search(r'v(\d+\.\d+(?:\.\d+)?)',html[:4000])
        seen[sha]={'dates':[date],'n':len(ents),'ents':ents,'ver':ver.group(1) if ver else None,'bytes':len(html)}
    for sha,info in seen.items():
        rows.append({'source':src,'blob':sha,'first_date':min(info['dates']),'last_date':max(info['dates']),
                     'declared_version':info['ver'],'n_entries':info['n'],'bytes':info['bytes'],'entries':info['ents']})
    print('%-18s %2d distinct gallery blobs, %d with entries'%(src,len(seen),sum(1 for v in seen.values() if v['n'])))
json.dump(rows,open(os.path.join(HOME,'palette','gallery-html-harvest.json'),'w'),ensure_ascii=False)
tot=sum(r['n_entries'] for r in rows)
keys=set(e['slug'] for r in rows for e in r['entries'])
print('\nblobs: %d | entry instances: %d | distinct slugs: %d'%(len(rows),tot,len(keys)))
print('entry counts observed:',sorted({r['n_entries'] for r in rows if r['n_entries']}))
