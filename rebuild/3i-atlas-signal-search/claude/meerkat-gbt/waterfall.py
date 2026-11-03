import sys, json, numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
sys.argv=['x','raw/OH']
import importlib.util
spec=importlib.util.spec_from_file_location('cf','cometframe_raw.py'); cf=importlib.util.module_from_spec(spec); spec.loader.exec_module(cf)
cands=[1667.686516,1666.512829,1667.994976,1667.138772]
scans=['0013','0014','0015','0016','0017','0018']
fig,axes=plt.subplots(len(cands),6,figsize=(14,2.6*len(cands)))
for r,F in enumerate(cands):
    for c,s in enumerate(scans):
        h=json.load(open(f'raw/OH_{s}.json')); x=np.load(f'raw/OH_{s}.npy',mmap_mode='r')
        t=h['tstart']+(np.arange(49)+0.5)*h['tsamp']/86400; v=cf.deldot(t)
        fobs=F*1e6*(1-v/cf.C); ch=np.rint((fobs-h['fch1_cc']*1e6)/(h['foff']*1e6)).astype(int)
        lo=ch.min()-40; hi=ch.max()+40
        w=np.asarray(x[:,lo:hi],np.float64); med=np.median(np.asarray(x[:,lo-500:hi+500],np.float64),axis=0)[500:500+(hi-lo)]
        w=w/np.median(w,axis=0)-1
        ax=axes[r,c]; ax.imshow(w,aspect='auto',cmap='viridis',vmin=-0.4,vmax=0.6,extent=[0,hi-lo,49,0])
        ax.plot(ch-lo+0.5,np.arange(49)+0.5,'r-',lw=0.6,alpha=0.6)
        ax.set_title(f"{F:.6f} {'ON' if s in cf.ON else 'OFF'} {s}",fontsize=7); ax.set_xticks([]); ax.set_yticks([])
plt.tight_layout(); plt.savefig('raw/oh_candidates_waterfall.png',dpi=110)
print('ok')
