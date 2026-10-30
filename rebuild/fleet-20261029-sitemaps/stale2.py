import json,subprocess,re,sys,collections
exec(open('sitemap_audit.py').read().split('rep = {}')[0])
MECH=re.compile(r'(?i)fleet refresh|network block|fleet block|allied sites|spxi instrument line|instrument line|count fallback|fleet-wide|sync.*fleet|regenerat')
out={}
for dom,repo in MAP.items():
    if dom=='alexanarch.org': continue
    repo=f"{FLEET}/{repo}"; PRE=PREFIX.get(dom,"")
    files=git(repo,'ls-tree','-r','--name-only','origin/main').split('\n')
    sms=[f for f in files if f.startswith(PRE) and re.fullmatch(r'sitemap[^/]*\.xml',f[len(PRE):])]
    ent=[]
    for s in sms:
        e,k,err=locs(show(repo,s)); ent+=e or []
    res=[]
    for u,lm in ent:
        p=norm(u).lstrip('/')
        cands=[PRE+p+'/index.html',PRE+p+'.html',PRE+p] if p else [PRE+'index.html']
        f=next((c for c in cands if c in files),None)
        if not f or not lm: continue
        log=git(repo,'log','origin/main',f'--since={lm[:10]}T23:59:59','--format=%cs\t%s','--',f).strip().split('\n')
        log=[l for l in log if l]
        content=[l for l in log if not MECH.search(l.split('\t',1)[1])]
        if content: res.append((norm(u),lm[:10],content[0]))
    out[dom]={'entries':len(ent),'content_stale':len(res),'sample':res[:6]}
    print(f"{dom:30} entries={len(ent):4} content-changed-after-lastmod={len(res)}")
json.dump(out,open('stale2.json','w'),indent=1)
