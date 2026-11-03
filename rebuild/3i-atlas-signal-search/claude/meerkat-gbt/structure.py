"""Structure in a set of rest frequencies, each statistic compared with uniform random sets of the same size in the same
band and, when available, with the false-drift candidate sets. Statistics:
 comb   : best regular spacing s (1-300 kHz): max over s of Rayleigh power |sum exp(2 pi i f/s)|^2/n  (free phase)
 anchored comb: same, phase fixed so the comb passes through the OH rest line 1667.359 MHz
 mirror : pairs symmetric about 1667.359 MHz within 20 Hz
 integer-kHz offsets from 1667.359 MHz: mean distance to the nearest whole kHz"""
import json, sys, numpy as np
OH=1667.359e6
F=np.array(json.load(open('raw/OH_excess_freqs.json')))
F=F[~((F>1665.60e6)&(F<1665.61e6))] if '--drop-spike' in sys.argv else F
lo,hi=1665.50e6,1668.43e6
S=np.exp(np.linspace(np.log(1e3),np.log(3e5),6000))
def stats(f):
    n=len(f); ph=2j*np.pi*np.outer(1/S,f)
    comb=(np.abs(np.exp(ph).sum(1))**2/n).max()
    anch=(np.abs(np.exp(2j*np.pi*np.outer(1/S,f-OH)).sum(1))**2/n)
    anch=np.max(np.real(np.exp(2j*np.pi*np.outer(1/S,f-OH)).sum(1))/np.sqrt(n))
    d=f[:,None]+f[None,:]-2*OH; mir=int(((np.abs(d)<20)&np.triu(np.ones((n,n),bool),1)).sum())
    k=(f-OH)/1e3; ik=float(np.abs(k-np.rint(k)).mean())
    return dict(comb=float(comb),anchored=float(anch),mirror=mir,int_kHz=ik)
t=stats(F); print('n',len(F),{k:round(v,3) for k,v in t.items()})
rng=np.random.default_rng(3); M=[stats(rng.uniform(lo,hi,len(F))) for _ in range(1000)]
for k in t:
    arr=np.array([m[k] for m in M]); p=(arr<=t[k]).mean() if k=='int_kHz' else (arr>=t[k]).mean()
    print(f'  {k:9s} true {t[k]:.3f}   uniform-null median {np.median(arr):.3f}   p={p:.3f}')
try:
    sets=json.load(open('raw/OH_excess_sets.json'))
    for d,fs in sets.items():
        if d!='0.0' and len(fs)>=4: print('  false',d,len(fs),{k:round(v,3) for k,v in stats(np.array(fs)).items()})
except FileNotFoundError: pass
