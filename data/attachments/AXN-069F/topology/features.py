import json,re,collections,statistics,glob,os,itertools,math
from html.parser import HTMLParser
C=json.load(open('fleet_crawl.json')); fleet=set(C['fleet']); H=C['hosts']
def hostnorm(h): return h.lower().replace('www.','')
# ---- host graph from crawl (sampled pages)
G=collections.defaultdict(collections.Counter)   # src host -> dst host -> link count
pages_per_host={}
for d,info in H.items():
    n=0
    for p in info['pages']:
        n+=1
        for hh,c in p['hosts'].items():
            hh=hostnorm(hh)
            if hh and hh!=d: G[d][hh]+=c
    pages_per_host[d]=n
hosts=[d for d in H if pages_per_host.get(d,0)>0]
def out_stats(d):
    tot=sum(G[d].values()); infleet=sum(c for h,c in G[d].items() if h in fleet); ext=tot-infleet
    ext_hosts={h for h in G[d] if h not in fleet}
    return tot,infleet,ext,ext_hosts
rows=[]
for d in hosts:
    tot,inf,ext,exth=out_stats(d)
    inlinks_from_fleet=sum(1 for s in hosts if s!=d and G[s].get(d,0)>0)
    reciprocal=sum(1 for s in hosts if s!=d and G[s].get(d,0)>0 and G[d].get(s,0)>0)
    rows.append({'host':d,'section':H[d]['section'],'sitemap_urls':H[d]['sitemap_urls'],'pages_sampled':pages_per_host[d],'out_links_total':tot,'out_links_in_fleet':inf,'out_links_external':ext,'in_fleet_share':round(inf/tot,3) if tot else None,'distinct_external_hosts':len(exth),'fleet_hosts_linking_in':inlinks_from_fleet,'reciprocal_fleet_hosts':reciprocal,'reciprocity':round(reciprocal/inlinks_from_fleet,3) if inlinks_from_fleet else None,'links_per_page':round(tot/pages_per_host[d],1)})
# component density
n=len(hosts); edges=sum(1 for s in hosts for t in hosts if s!=t and G[s].get(t,0)>0)
density=edges/(n*(n-1)) if n>1 else None
# external hosts most linked by the fleet
ext=collections.Counter()
for d in hosts:
    for h,c in G[d].items():
        if h not in fleet: ext[h]+=c
# ---- alexanarch internal structure from disk
root='/home/claude/alexanarch/s/records'
recs=glob.glob(root+'/*/index.html')
class LP(HTMLParser):
    def __init__(s): super().__init__(); s.links=[]
    def handle_starttag(s,tag,attrs):
        if tag=='a':
            for k,v in attrs:
                if k=='href' and v: s.links.append(v)
import random; random.seed(1)
samp=random.sample(recs,min(200,len(recs)))
per=[]
for f in samp:
    t=open(f,encoding='utf-8',errors='ignore').read(); p=LP()
    try: p.feed(t)
    except Exception: pass
    rec=len([l for l in p.links if re.match(r'^(https?://(www\.)?alexanarch\.org)?/s/records/\d+/',l)])
    fl=len([l for l in p.links if any(h in l for h in fleet) and 'alexanarch.org' not in l])
    ext_=len([l for l in p.links if l.startswith('http') and not any(h in l for h in fleet)])
    per.append((len(p.links),rec,fl,ext_,len(t)))
def med(i): return statistics.median(x[i] for x in per)
alexa={'rendered_record_pages':len(recs),'sample':len(samp),'median_links_per_record_page':med(0),'median_record_to_record':med(1),'median_links_to_other_fleet_hosts':med(2),'median_external_links':med(3),'median_bytes':med(4)}
# page generation: sitemap lastmod distribution and registry dates
reg=json.load(open('/home/claude/alexanarch/data/registry.json'))
bym=collections.Counter((x.get('date') or '')[:7] for x in reg['deposits'])
# self-citation share
cg=json.load(open('/home/claude/alexanarch/data/citation-graph.json'))
cge=json.load(open('/home/claude/alexanarch/data/citation-graph-external.json'))
def count_edges(j):
    for k in ('edges','links'):
        if isinstance(j,dict) and isinstance(j.get(k),list): return len(j[k])
    return len(j) if isinstance(j,list) else None
internal=count_edges(cg); external=count_edges(cge)
# templated share on alexanarch: generated surfaces
gen=sum(len(glob.glob(f'/home/claude/alexanarch/{p}')) for p in ['s/records/*/index.html','s/axn/*/index.html','s/wiki/*/index.html','s/browse/*/*/index.html','s/doi/*/index.html','s/graph/*/index.html'])
allpages=len(glob.glob('/home/claude/alexanarch/**/index.html',recursive=True))
out={'hosts':rows,'fleet_size':len(fleet),'hosts_crawled':n,'fleet_host_graph_edges':edges,'fleet_host_graph_density':round(density,3),'top_external_hosts_linked':ext.most_common(25),'alexanarch_pages':alexa,'deposits_per_month':dict(sorted(bym.items())),'citation_edges_internal':internal,'citation_edges_external':external,'alexanarch_generated_pages':gen,'alexanarch_index_pages':allpages}
json.dump(out,open('fleet_features.json','w'),indent=1)
print('hosts',n,'edges',edges,'density',round(density,3))
print('median in-fleet share of outlinks',statistics.median([r['in_fleet_share'] for r in rows if r['in_fleet_share'] is not None]))
print('median reciprocity',statistics.median([r['reciprocity'] for r in rows if r['reciprocity'] is not None]))
print('median distinct external hosts per host',statistics.median([r['distinct_external_hosts'] for r in rows]))
print('alexanarch',alexa)
print('citations internal',internal,'external',external,'generated pages',gen,'of',allpages)
print('top external:',ext.most_common(15))
print('deposits/month',dict(sorted(bym.items())))
