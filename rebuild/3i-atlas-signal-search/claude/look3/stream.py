"""Look 3.1, step 0: stream the four public MeerKAT 3I/ATLAS hit lists into compact arrays (every hit, every beam)."""
import re, zlib, urllib.request, numpy as np, json, sys
B="https://bldata.berkeley.edu/ATLAS/MeerKAT/"
LISTS=["atlas_hits","atlas_hits_2025_11","atlas_hits_2025_11_dups","atlas_hits_2025_12"]
num=rb'([0-9.eE+-]+)'
pat=re.compile(rb'\{"frequency":'+num+rb',"index":[^,]*,"driftSteps":'+num+rb',"driftRate":'+num+rb',"snr":'+num+rb',"coarseChannel":[^,]*,"beam":'+num+rb',"power":[^,]*,"incoherentPower":'+num+rb',"sourceName":"([^"]*)","fch1":[^,]*,"foff":[^,]*,"tstart":'+num+rb',"tsamp":'+num+rb',"ra":'+num+rb',"dec":'+num+rb',"telescopeId":[^,]*,"numTimesteps":'+num)
cnt=re.compile(rb'\{"frequency":')
names={}; rows=[]; tot={}
for li,L in enumerate(LISTS):
    r=urllib.request.urlopen(B+L+".json.gz",timeout=600); dz=zlib.decompressobj(31); buf=b""; n=0; nall=0; chunk=[]
    while True:
        c=r.read(1<<22)
        if not c: break
        buf+=dz.decompress(c); last=0
        for m in pat.finditer(buf):
            g=m.groups(); n+=1; last=m.end()
            s=names.setdefault(g[6],len(names))
            chunk.append((float(g[7]),float(g[0]),float(g[2]),float(g[3]),float(g[4]),float(g[5]),s,float(g[8]),float(g[9]),float(g[10]),float(g[11]),float(g[1]),li))
        nall+=len(cnt.findall(buf[:last])); buf=buf[last:]
    rows.append(np.array(chunk,dtype=np.float64)); tot[L]=[n,nall]; print(L,n,nall,flush=True)
A=np.concatenate(rows); np.save("hits.npy",A)
json.dump({"names":{k.decode():v for k,v in names.items()},"tot":tot,"cols":["tstart","freq","drift","snr","beam","incoh","src","tsamp","ra","dec","nt","dsteps","list"]},open("meta.json","w"))
print(A.shape)
