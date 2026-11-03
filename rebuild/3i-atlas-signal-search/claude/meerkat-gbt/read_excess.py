"""Read the 1667 MHz comet-frame excess: candidate rest frequencies (z_on 2.5, z_off 2.0), and the same sets for
false-drift frames, for structure tests run identically on both."""
import sys, json, numpy as np, importlib.util
sys.argv=['x','raw/OH','2.5','2.0']
spec=importlib.util.spec_from_file_location('cf','cometframe_raw.py'); cf=importlib.util.module_from_spec(spec); spec.loader.exec_module(cf)
def clusters(rows, tol=10.0):
    f=sorted(r['f_rest_MHz']*1e6 for r in rows); out=[]
    for x in f:
        if out and x-out[-1][-1]<=tol: out[-1].append(x)
        else: out.append([x])
    return [float(np.mean(c)) for c in out]
res={'0.0':clusters(cf.coincidences(0.0,keep=True))}
print('true',len(res['0.0']),flush=True)
for d in [-0.2,-0.17,-0.14,-0.11,-0.08,-0.05,0.05,0.08,0.11,0.14,0.17,0.2,-0.19,-0.13,0.13,0.19]:
    res[str(d)]=clusters(cf.coincidences(d*cf.C/1.667e9,keep=True)); print(d,len(res[str(d)]),flush=True)
json.dump(res,open('raw/OH_excess_sets.json','w'))
