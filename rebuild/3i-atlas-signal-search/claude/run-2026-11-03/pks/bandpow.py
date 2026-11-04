import sys,os,re,urllib.request,numpy as np,concurrent.futures as cf
sys.path.insert(0,'pks');_a=sys.argv;sys.argv=[_a[0]]
from fullband import get,header,R
sys.argv=_a
node=_a[1];fl=[float(x) for x in _a[2:]]
idx=urllib.request.urlopen(R+node+"/",timeout=60).read().decode()
F=sorted(set(re.findall(r'href="([^"]+_[SR]_0001\.0000\.fil)"',idx)))
H=[header(R+node+"/"+f) for f in F]
EX=cf.ThreadPoolExecutor(24)
for f0 in fl:
  out=[]
  for i,h in enumerate(F):
    hh=H[i];c0=int(round((f0-hh['fch1'])/hh['foff']));n=50000
    def one(k):
      a=hh['hdr_len']+(k*hh['nchans']+c0)*4;return k,np.frombuffer(get(R+node+"/"+h,a,a+n*4-1),'<f4').astype(float)
    X=np.zeros((20,n))
    for k,r in EX.map(one,range(20)):X[k]=r
    out.append(X.mean(1))
  allm=np.median(np.concatenate(out))
  print(f0,' | '.join(('S' if '_S_' in F[i] else 'R')+' '+' '.join('%+.0f'%(100*(v/allm-1)) for v in o) for i,o in enumerate(out)),flush=True)
