import sys, json, numpy as np
zon=float(sys.argv[1]) if len(sys.argv)>1 else 2.5
sys.argv_stem='raw/OH2'
sys.argv=['x',sys.argv_stem,str(zon),'2.0']
import importlib.util
spec=importlib.util.spec_from_file_location('cf','cometframe_raw.py'); cf=importlib.util.module_from_spec(spec); spec.loader.exec_module(cf)
def clusters(rows, tol_hz=10.0):
    f=sorted(r['f_rest_MHz']*1e6 for r in rows); n=0; last=None
    for x in f:
        if last is None or x-last>tol_hz: n+=1
        last=x
    return n
out=[]
for d in np.round(np.arange(-0.2,0.2001,0.01),3):
    n=clusters(cf.coincidences(d*cf.C/1.6654e9,keep=True)); out.append((float(d),n)); print(d,n,flush=True)
json.dump(out,open(f'raw/OH2_driftscan_z{zon}.json','w'))
