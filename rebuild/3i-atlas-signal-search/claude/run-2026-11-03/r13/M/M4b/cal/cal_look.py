import sys,os,json,numpy as np
CCX,INJF=sys.argv[1],sys.argv[2]; sys.argv=['mdhits.py',CCX,'inj']
__file__=os.path.abspath('mdhits.py'); src=open('mdhits.py').read().split("real = events(ON, OFF)")[0]; exec(src)
fcm=fc/1e6; inj=json.load(open(INJF))
def cell(mhz,L): return int(((fc-mhz*1e6)/dm.DF+dm.N//2)/L)
rows=[]
for f0,rate,r,ab in inj:
    sky=fcm-f0/1e6; srate=-rate
    out=[]
    for s in SC:
        best=None
        for L in mdrift.LEVELS:
            t0=61027*86400.0+17226.0; mh=sky+(srate*(T0[s]-t0) if ab else 0.0)/1e6; c=cell(mh,L); w=slice(max(c-6,0),c+7); z=LZ[(s,L)][w]; i=int(np.argmax(z))
            v=(round(float(z[i]),1),L,int(DR[(s,L)][w][i]))
            if best is None or v[0]>best[0]: best=v
        out.append(f"{s}:{best[0]}@L{best[1]}")
    rows.append(f"{sky:.6f} rate {srate:+.2f} r {r} {'persistent' if ab else ''}  "+"  ".join(out))
print("\n".join(rows))
for g in ((1600.3095,1599.9620) if CCX=='30' else ()):
    print('GLONASS',g,["%s:%.1f"%(s,max(float(LZ[(s,L)][max(cell(g,L)-6,0):cell(g,L)+7].max()) for L in mdrift.LEVELS)) for s in SC])

ev=json.load(open(sys.argv[3])) if len(sys.argv)>3 else None
if ev:
    for f0,rate,r,ab in inj:
        sky=fcm-f0/1e6; m=[e for e in ev['events'] if abs(e['mhz_topo']-sky)<0.0006+abs(rate)*1600e-6]
        print(f"{sky:.6f} rate {-rate:+.2f} r {r}: events", sorted({(e['scan'],e['cls'],e['level']) for e in m}))
