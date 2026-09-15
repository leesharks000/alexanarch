import json,re,time,collections,urllib.parse,sys
import requests
from html.parser import HTMLParser
H={'User-Agent':'Mozilla/5.0 (compatible; cha-topology-audit/0.1; research; alexanarch.org)'}
A=['en.wikipedia.org','www.reddit.com','www.youtube.com','arxiv.org','github.com','medium.com','www.academia.edu','figshare.com','www.sciencedirect.com','www.semanticscholar.org','www.linkedin.com','www.quora.com','stackoverflow.com','www.facebook.com','www.forbes.com']
FAM={'wikipedia':('wikipedia','wikimedia','wiktionary','wikidata'),'reddit':('reddit','redd.it'),'youtube':('youtube','youtu.be','google'),'arxiv':('arxiv',),'github':('github',),'medium':('medium',),'academia':('academia',),'figshare':('figshare',),'sciencedirect':('sciencedirect','elsevier'),'semanticscholar':('semanticscholar','allenai'),'linkedin':('linkedin',),'quora':('quora',),'stackoverflow':('stackoverflow','stackexchange'),'facebook':('facebook','fb.com','meta.com','instagram'),'forbes':('forbes',)}
def fam(h):
    h=h.lower()
    for f,keys in FAM.items():
        if any(k in h for k in keys): return f
    return None
class LP(HTMLParser):
    def __init__(s): super().__init__(); s.links=[]
    def handle_starttag(s,tag,attrs):
        if tag=='a':
            for k,v in attrs:
                if k=='href' and v: s.links.append(v)
def host(u):
    try: return urllib.parse.urlparse(u).netloc.lower().replace('www.','')
    except: return ''
def fetch(u,limit=400000):
    try:
        r=requests.get(u,headers=H,timeout=20,allow_redirects=True); return r.status_code,r.text[:limit]
    except Exception: return None,''
def sitemap(d):
    for u in [f'https://{d}/sitemap.xml',f'https://{d}/sitemaps/sitemap.xml',f'https://{d}/sitemap_index.xml']:
        st,t=fetch(u,1500000)
        if st==200 and '<loc>' in t:
            urls=re.findall(r'<loc>\s*([^<\s]+)\s*</loc>',t)
            if urls and all(x.endswith('.xml') or x.endswith('.gz') for x in urls[:3]):
                sub=[]
                for sm in [x for x in urls if x.endswith('.xml')][:2]:
                    st2,t2=fetch(sm,1500000); sub+=re.findall(r'<loc>\s*([^<\s]+)\s*</loc>',t2)
                urls=sub
            return urls
    return []
out={}
start=int(sys.argv[1]); end=int(sys.argv[2])
for d in A[start:end]:
    t0=time.time(); st,home=fetch(f'https://{d}/')
    urls=sitemap(d) if st==200 else []
    sample=[f'https://{d}/']+[u for u in urls if host(u).replace('www.','')==d.replace('www.','') or fam(host(u))==fam(d)][:10]
    pages=[]
    for u in sample:
        s2,t=fetch(u)
        if s2!=200: continue
        p=LP()
        try: p.feed(t)
        except Exception: pass
        hosts=collections.Counter()
        for l in p.links:
            if l.startswith('#') or l.startswith('mailto:') or l.startswith('javascript:'): continue
            hh=host(l) or d.replace('www.','')
            hosts[hh]+=1
        pages.append({'url':u,'bytes':len(t),'links':sum(hosts.values()),'hosts':dict(hosts)})
    out[d]={'home_status':st,'sitemap_urls':len(urls),'pages_sampled':len(pages),'pages':pages,'secs':round(time.time()-t0,1)}
    print(d,st,'sitemap',len(urls),'sampled',len(pages),round(time.time()-t0,1),'s',flush=True)
json.dump(out,open(f'admitted_crawl_{start}_{end}.json','w'),indent=1)
