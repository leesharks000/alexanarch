import re,json
def T(n): return open(f'/tmp/zfs/jg{n}.txt',encoding='utf-8',errors='replace').read()
def starts(t,pat):
    # an article opens with its title, then "Von" / "By" / "Par" and the author, within 260 characters
    out=[]
    for m in re.finditer(pat,t):
        if m.start()<15000: continue
        if re.search(r'\n\s*(Von|By|Par|von)\s*\n',t[m.end():m.end()+260]): out.append(m.start())
    return out
B=r'\n\s*Besprechungen\.?\s*\n'
SPEC=[ # volume, slug, author (death year, from memory), title, start pattern, end patterns, pages
 (3,"benjamin-standort-des-franzoesischen-schriftstellers-1934","Walter Benjamin (1940)","Zum gegenwärtigen gesellschaftlichen Standort des französischen Schriftstellers",r'Zum gegenw\S+rtigen gesellschaftlichen Standort',[r'Differentiation of Delinquent'],"54–78"),
 (3,"bougle-sociologie-economique-en-france-1934","Célestin Bouglé (1940)","La sociologie économique en France",r'La sociologie \S+conomique en France',[r'Taine, Bergson et Nietzsche',B],"383–408"),
 (4,"beard-social-sciences-in-the-united-states-1935","Charles A. Beard (1948)","The Social Sciences in the United States",r'The Social Sciences in the United States',[r'Das Recht auf Arbeit'],"61–65"),
 (4,"toennies-das-recht-auf-arbeit-1935","Ferdinand Tönnies (1936)","Das Recht auf Arbeit",r'Das Recht auf Arbeit',[r'Neue Literatur zur Planwirtschaft'],"66–80"),
 (4,"grossmann-mechanistische-philosophie-und-manufaktur-1935","Henryk Grossmann (1950)","Die gesellschaftlichen Grundlagen der mechanistischen Philosophie und die Manufaktur",r'Die gesellschaftlichen Grundlagen der mechanistischen',[r'Collective Autism'],"161–231"),
 (4,"benjamin-probleme-der-sprachsoziologie-1935","Walter Benjamin (1940)","Probleme der Sprachsoziologie. Ein Sammelreferat",r'Probleme der Sprachsoziologie',[B,r'Zum Problem der Wahrheit'],"248–268"),
 (6,"neurath-inventory-of-the-standard-of-living-1937","Otto Neurath (1945)","Inventory of the Standard of Living",r'Inventory of the Standard of Living',[r'Gestural Behavior and Social Setting'],"140–151"),
 (6,"benjamin-eduard-fuchs-1937","Walter Benjamin (1940)","Eduard Fuchs, der Sammler und der Historiker",r'Eduard Fuchs, der Sammler und der Historiker',[r'Sociological Remarks on Greek Poetry'],"346–381"),
 (6,"bougle-les-sciences-sociales-en-france-1937","Célestin Bouglé (1940)","Les sciences sociales en France",r'Les [Ss]ciences sociales en France',[B,r'La Sociologie de Pare'],"400–"),
 (6,"neumann-funktionswandel-des-gesetzes-1937","Franz Neumann (1954)","Der Funktionswandel des Gesetzes im Recht der bürgerlichen Gesellschaft",r'Der Funktionswandel des Gesetzes',[r'Zum Begriff und zur Diagnose'],"542–596"),
 (8,"benjamin-ueber-einige-motive-bei-baudelaire-1939","Walter Benjamin (1940)","Über einige Motive bei Baudelaire, the first printing",r'[UÜ]ber einige Motive bei Baudelaire',[r'Die R\S+ckschritte der Poesie'],"50–91"),
 (8,"jochmann-die-rueckschritte-der-poesie-1939","Carl Gustav Jochmann (1830), introduced by Walter Benjamin (1940)","Die Rückschritte der Poesie",r'Die R\S+ckschritte der Poesie',[r'Die Juden und Europa'],"92–114"),
]
res=[]
for n,slug,auth,title,sp,eps,pp in SPEC:
    t=T(n); st=starts(t,sp)
    if not st: print('NO START',n,slug,[m.start() for m in re.finditer(sp,t)][:6]); continue
    a=st[0]; ends=[]
    for ep in eps:
        e=[x for x in (starts(t,ep) if ep!=B else [m.start() for m in re.finditer(ep,t)]) if x>a+2000]
        if e: ends.append(e[0])
    if not ends: print('NO END',n,slug); continue
    b=min(ends); x=t[a:b]
    print(f"{n} {slug[:44]:44} {a:8}-{b:8} {len(x):7} | {re.sub(chr(10)+'+',' ',x[:70])!r} … {re.sub(chr(10)+'+',' ',x[-90:])!r}")
    res.append(dict(volume=n,slug=slug,author=auth,title=title,a=a,b=b,pages=pp))
json.dump(res,open('/tmp/zfs/cuts.json','w'),ensure_ascii=False,indent=1)
