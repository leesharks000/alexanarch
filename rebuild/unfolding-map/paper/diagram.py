import json,re,sys,html
sys.path.insert(0,'/home/claude/unfold/seats'); import tisch
RE=tisch.load('RE'); MT=tisch.load('MT')
rows=json.load(open('/home/claude/unfold/map/rev-matthew-ledger.json'))['rows']
def axis(V):
    ks=list(V); pos={k:i for i,k in enumerate(ks)}; ch={}
    for k in ks: ch.setdefault(k[0],[pos[k],pos[k]]); ch[k[0]][1]=pos[k]
    return pos,ch,len(ks)
rp,rc,rn=axis(RE); mp,mc,mn=axis(MT)
def first(V,pos,s):
    out=[]
    for part in str(s).split(';'):
        m=re.match(r'(\d+):(\d+)(?:-(\d+))?$',part.strip())
        if not m: continue
        c,a,b=int(m.group(1)),int(m.group(2)),int(m.group(3) or m.group(2))
        ks=[(c,v) for v in range(a,b+1) if (c,v) in pos]
        if ks: out.append((pos[ks[0]]+pos[ks[-1]])/2)
    return out
FAM=[('keep','Kept: the speaker’s saying is the teacher’s','#257de0'),
     ('exch','Exchanged: who does it, or to whom','#f47230'),
     ('opp','Opposed or turned','#00b894'),
     ('form','Given a form: it happens, is foretold, likened, enacted, staged, or named in the land','#f2a600'),
     ('eng','Divided and gathered (the engine’s derivations)','#ee7fac')]
def fam(m):
    if re.match(r'PARTITION|SUBSTITUTE|EVENT',m): return 'eng'
    if re.search(r'OPPOSE|TURN|turned',m): return 'opp'
    if re.search(r'EXCHANGE|exchanged|MOVE|given to|said of|passive charge',m): return 'exch'
    if re.search(r'STAGE|ENACT|HAPPEN|FORETELL|LIKEN|P2',m): return 'form'
    return 'keep'
W,H=1200,800; L,R=40,1160; yR,yM=170,610; bh=26
xr=lambda p:L+(R-L)*(p+0.5)/rn; xm=lambda p:L+(R-L)*(p+0.5)/mn
col={k:c for k,_,c in FAM}
o=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="Georgia, \'Times New Roman\', serif" role="img" aria-labelledby="t d">',
'<title id="t">From Revelation to Matthew: the ledger of relations</title>',
f'<desc id="d">Each line joins a place in Revelation (top, chapters 1 to 22) to the place in Matthew (bottom, chapters 1 to 28) that holds the same relation with a stated change. {len(rows)} rows of the ledger. Lines cross because the source is held open and not followed in order.</desc>',
f'<rect width="{W}" height="{H}" fill="#ffffff"/>',
f'<text x="{L}" y="38" font-size="24" fill="#1a1a1a">From Revelation to Matthew</text>',
f'<text x="{L}" y="62" font-size="14" fill="#555">Each line is one checked relation of the ledger ({len(rows)} rows): a place in the Apocalypse, the move, the place in the Gospel. The lines cross because a writer holds the source open.</text>']
def band(ch,n,y,label,marks,above):
    o.append(f'<text x="{L}" y="{y-58 if above else y+bh+66}" font-size="17" fill="#1a1a1a" font-weight="bold">{label}</text>')
    for c,(a,b) in ch.items():
        x0=L+(R-L)*a/n; x1=L+(R-L)*(b+1)/n
        o.append(f'<rect x="{x0+1:.1f}" y="{y}" width="{x1-x0-2:.1f}" height="{bh}" rx="3" fill="#f1efe9" stroke="#b9b4a8" stroke-width="0.8"/>')
        o.append(f'<text x="{(x0+x1)/2:.1f}" y="{y+18}" font-size="12" text-anchor="middle" fill="#333">{c}</text>')
    for i,(c0,c1,t) in enumerate(marks):
        x0=L+(R-L)*ch[c0][0]/n; x1=L+(R-L)*(ch[c1][1]+1)/n; yy=y-8 if above else y+bh+8; tier=16*(i%2)
        o.append(f'<line x1="{x0+3:.1f}" x2="{x1-3:.1f}" y1="{yy}" y2="{yy}" stroke="#8a857a" stroke-width="1"/>')
        o.append(f'<text x="{(x0+x1)/2:.1f}" y="{yy-5-tier if above else yy+15+tier}" font-size="11.5" text-anchor="middle" fill="#555" font-style="italic">{t}</text>')
band(rc,rn,yR,'REVELATION',[(1,1,'the speaker'),(2,3,'seven letters'),(4,5,'throne, Lamb'),(6,6,'seals, riders'),(8,9,'trumpets'),(11,11,'witnesses'),(12,12,'woman, dragon'),(13,13,'beast, mark'),(14,14,'harvest'),(16,16,'bowls'),(17,18,'Babylon'),(19,19,'wedding'),(20,20,'custody, judgment'),(21,22,'the city; “I come”')],True)
band(mc,mn,yM,'MATTHEW',[(1,2,'birth, flight'),(3,4,'trial'),(5,7,'the Sermon'),(8,9,'healings, sea'),(10,10,'mission'),(11,12,'yoke; adversaries'),(13,13,'parables'),(14,15,'feeding, sea'),(16,17,'keys; mountain'),(18,20,'the rich one; labourers'),(21,22,'temple; wedding'),(23,23,'woes'),(24,25,'the end'),(26,27,'passion'),(28,28,'tomb')],False)
n=0; cnt={k:0 for k in col}
order={'eng':0,'keep':1,'form':2,'exch':3,'opp':4}
links=[]
for r in rows:
    f=fam(str(r['move'])); ms=first(MT,mp,r['matt']); rs=first(RE,rp,r['rev'])
    if not ms or not rs: print('no pos',r['rev'],r['matt']); continue
    cnt[f]+=1
    m=sum(ms)/len(ms)
    for a in rs: links.append((order[f],f,a,m,r))
for _,f,a,m,r in sorted(links,key=lambda t:t[0]):
    x0,x1=xr(a),xm(m); y0,y1=yR+bh,yM
    tip=html.escape(f"Rev {r['rev']} → Matt {r['matt']}: {r['move']}")
    o.append(f'<path d="M{x0:.1f},{y0} C{x0:.1f},{y0+190} {x1:.1f},{y1-190} {x1:.1f},{y1}" fill="none" stroke="{col[f]}" stroke-width="1.8" stroke-opacity="0.62" stroke-linecap="round"><title>{tip}</title></path>')
    o.append(f'<circle cx="{x0:.1f}" cy="{y0}" r="2.6" fill="{col[f]}"/><circle cx="{x1:.1f}" cy="{y1}" r="2.6" fill="{col[f]}"/>'); n+=1
y=738; x=L
for k,t,c in FAM:
    lab=f'{t} ({cnt[k]})'
    o.append(f'<line x1="{x}" x2="{x+26}" y1="{y-4}" y2="{y-4}" stroke="{c}" stroke-width="3" stroke-linecap="round"/><text x="{x+32}" y="{y}" font-size="12.5" fill="#333">{html.escape(lab)}</text>')
    x+=32+len(lab)*6.6+22
    if x>R-330: x=L; y+=24
o.append(f'<text x="{R}" y="{H-12}" font-size="11" text-anchor="end" fill="#777">Widths are in verses. Data: rev-matthew-ledger.json, 27 November 2026. A draft figure.</text>')
o.append('</svg>')
open('/mnt/user-data/outputs/REV-TO-MATTHEW-MAP.svg','w',encoding='utf-8').write('\n'.join(o))
print(n,'links',cnt)
