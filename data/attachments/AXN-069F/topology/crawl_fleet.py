import json,re,sys,time,collections,urllib.parse
import requests
from html.parser import HTMLParser
H={'User-Agent':'cha-topology-audit/0.1 (alexanarch.org; research)'}
f=json.load(open('/home/claude/alexanarch/data/api/fleet.json'))
doms=[]
for s in f['sections']:
    for it in s['sites']:
        d=it.get('d')
        if d: doms.append((s['name'],d))
fleet=set(d for _,d in doms)
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
        r=requests.get(u,headers=H,timeout=25,allow_redirects=True); return r.status_code,r.text[:limit],r.url
    except Exception as e: return None,'',u
def sitemap_urls(d):
    urls=[]
    for u in [f'https://{d}/sitemap.xml',f'https://www.{d}/sitemap.xml']:
        st,t,_=fetch(u,2000000)
        if st==200 and '<loc>' in t:
            urls=re.findall(r'<loc>\s*([^<\s]+)\s*</loc>',t)
            # sitemap index?
            if urls and all(x.endswith('.xml') for x in urls[:3]):
                sub=[]
                for sm in urls[:3]:
                    st2,t2,_=fetch(sm,2000000)
                    sub+=re.findall(r'<loc>\s*([^<\s]+)\s*</loc>',t2)
                urls=sub
            break
    return urls
out={}
for sec,d in doms:
    t0=time.time()
    home_st,home,final=fetch(f'https://{d}/')
    urls=sitemap_urls(d) if home_st==200 else []
    sample=[f'https://{d}/']+[u for u in urls if host(u)==d][:12]
    pages=[]
    for u in sample:
        st,t,_=fetch(u)
        if st!=200: continue
        p=LP(); 
        try: p.feed(t)
        except Exception: pass
        hosts=collections.Counter()
        for l in p.links:
            if l.startswith('#') or l.startswith('mailto:') or l.startswith('javascript:'): continue
            hh=host(l) or d
            hosts[hh]+=1
        pages.append({'url':u,'bytes':len(t),'links':sum(hosts.values()),'hosts':dict(hosts)})
    out[d]={'section':sec,'home_status':home_st,'sitemap_urls':len(urls),'pages_sampled':len(pages),'pages':pages,'secs':round(time.time()-t0,1)}
    print(d,sec,home_st,'sitemap',len(urls),'sampled',len(pages),flush=True)
json.dump({'fleet':sorted(fleet),'hosts':out},open('fleet_crawl.json','w'),indent=1)
