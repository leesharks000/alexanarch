exec(open('s1.py').read().split("print('rows',len(rows)")[0])
import statistics
ri={k:i for i,k in enumerate(RE)}; mi={k:i for i,k in enumerate(MT)}
def test(rs,N=4000):
    pts=[(mi[r['pos']],statistics.median(ri[k] for k in r['rk'])) for r in rs]
    def stat(p):
        d=[abs(a[1]-b[1]) for a,b in itertools.combinations(p,2) if 0<abs(a[0]-b[0])<=10]
        return statistics.median(d),len(d)
    obs,n=stat(pts); allm=statistics.median(abs(a[1]-b[1]) for a,b in itertools.combinations(pts,2))
    random.seed(3); rv=[p[1] for p in pts]; le=0
    for _ in range(N):
        random.shuffle(rv); s,_=stat([(p[0],v) for p,v in zip(pts,rv)]); le+= s<=obs
    return dict(median_near=obs,pairs=n,median_all=allm,ratio=round(obs/allm,2),p=round((le+1)/(N+1),4))
print('S7 all',test(rows)); print('S7 unchosen',test([r for r in rows if r['unch']])); print('S7 chosen only',test([r for r in rows if not r['unch']]))
