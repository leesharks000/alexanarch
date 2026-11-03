import sys, json, numpy as np
sys.argv=['x','raw/OH','2.5','2.0']
import importlib.util
spec=importlib.util.spec_from_file_location('cf','cometframe_raw.py'); cf=importlib.util.module_from_spec(spec); spec.loader.exec_module(cf)
def clusters(rows, tol_hz=10.0):
    f=sorted(r['f_rest_MHz']*1e6 for r in rows); n=0; last=None
    for x in f:
        if last is None or x-last>tol_hz: n+=1
        last=x
    return n
if __name__=="__main__":
  pass
real=None if __name__!="__main__" else cf.coincidences(0.0,keep=True)
rng=np.random.default_rng(11); offs=rng.uniform(0.03,1.0,40)*rng.choice([-1,1],40)*cf.C/1.42e9
nulls=[clusters(cf.coincidences(a,keep=True)) for a in offs]
print('true-frame clusters:',clusters(real),' null clusters mean %.2f sd %.2f max %d  frac>=true %.3f'%(np.mean(nulls),np.std(nulls),max(nulls),np.mean([n>=clusters(real) for n in nulls])))
seen=[]
for r in sorted(real,key=lambda r:r['f_rest_MHz']):
    if seen and abs(r['f_rest_MHz']-seen[-1]['f_rest_MHz'])*1e6<10: continue
    seen.append(r); print('%.6f'%r['f_rest_MHz'],{k:round(v,1) for k,v in r.items() if k.startswith('z_')})
