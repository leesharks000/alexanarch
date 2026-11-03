import json, numpy as np, sys, os
sys.argv=['x','raw/HI']; import importlib.util
spec=importlib.util.spec_from_file_location('cf','cometframe_raw.py'); cf=importlib.util.module_from_spec(spec); spec.loader.exec_module(cf)
F_REST=1421.0e6; AMP=float(os.environ.get('AMP','0.02'))
for s in cf.ON+cf.OFF:
    h=json.load(open(f'raw/HI_{s}.json')); json.dump(h,open(f'raw/INJ_{s}.json','w'))
    if s in cf.OFF:
        if not os.path.exists(f'raw/INJ_{s}.npy'): os.symlink(os.path.abspath(f'raw/HI_{s}.npy'),f'raw/INJ_{s}.npy')
        continue
    x=np.load(f'raw/HI_{s}.npy').copy(); nt,nc=x.shape
    t=h['tstart']+(np.arange(nt)+0.5)*h['tsamp']/86400; v=cf.deldot(t)
    fobs=F_REST*(1-v/cf.C); ch=np.rint((fobs-h['fch1_cc']*1e6)/(h['foff']*1e6)).astype(int)
    med=np.median(x,axis=0)
    for k in range(nt): x[k,ch[k]]+=AMP*med[ch[k]]
    np.save(f'raw/INJ_{s}.npy',x)
print('injected at',F_REST/1e6,'MHz rest, amp',AMP)
