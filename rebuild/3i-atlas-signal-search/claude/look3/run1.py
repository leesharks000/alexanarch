import numpy as np, json, urllib.request, urllib.parse
C=299792.458
A=np.load('hits.npy',mmap_mode='r')
t=A[:,0]; f=A[:,1]; dr=A[:,2]; beam=A[:,4].astype(int); tsamp=A[:,7]; nt=A[:,10]
ts,inv=np.unique(t,return_inverse=True)
nb=np.array([len(np.unique(beam[inv==i])) for i in range(len(ts))])
keep=nb[inv]>1
idx=np.where(keep)[0]
def horizons(t0,t1):
    q={"format":"json","COMMAND":"'C/2025 N1'","OBJ_DATA":"NO","MAKE_EPHEM":"YES","EPHEM_TYPE":"OBSERVER","CENTER":"'coord@399'",
       "COORD_TYPE":"GEODETIC","SITE_COORD":"'21.4430,-30.7110,1.038'","START_TIME":f"'JD {t0+2400000.5:.6f}'",
       "STOP_TIME":f"'JD {t1+2400000.5:.6f}'","STEP_SIZE":"'10 m'","QUANTITIES":"'20'","CSV_FORMAT":"YES","CAL_FORMAT":"JD"}
    txt=json.load(urllib.request.urlopen("https://ssd.jpl.nasa.gov/api/horizons.api?"+urllib.parse.urlencode(q),timeout=120))["result"]
    rows=[[x.strip() for x in l.split(",") if x.strip()] for l in txt.split("$$SOE")[1].split("$$EOE")[0].strip().splitlines()]
    return np.array([(float(r[0])-2400000.5,float(r[-1])) for r in rows])
E_=[]
for d in np.unique(t[idx].astype(int)):
    m=t[idx].astype(int)==d; E_.append(horizons(t[idx][m].min()-0.02,t[idx][m].max()+0.05))
E_=np.concatenate(E_); E_=E_[np.argsort(E_[:,0])]
acc=np.gradient(E_[:,1],E_[:,0]*86400.0)   # km/s^2, finite difference within each day's block
# guard: recompute per block to avoid cross-day gradients
blk=np.r_[0,np.where(np.diff(E_[:,0])>0.1)[0]+1,len(E_)]
for a,b in zip(blk[:-1],blk[1:]): acc[a:b]=np.gradient(E_[a:b,1],E_[a:b,0]*86400.0)
tmid=t[idx]+nt[idx]*tsamp[idx]/2/86400
a_hit=np.interp(tmid,E_[:,0],acc)
pred=-f[idx]*1e6*a_hit/C          # Hz/s
step=1.5944242477416992/(nt[idx]*tsamp[idx])
# singletons: per scan, sort by freq, check other beams within 2 kHz
sing=np.zeros(len(idx),bool)
sc=inv[idx]
order=np.lexsort((f[idx],sc))
fs=f[idx][order]; ss=sc[order]; bs=beam[idx][order]
w=0.002
lo=np.searchsorted(ss*1e5+fs, ss*1e5+fs-w, 'left'); hi=np.searchsorted(ss*1e5+fs, ss*1e5+fs+w, 'right')
for k in range(len(fs)):
    seg=bs[lo[k]:hi[k]]
    sing[order[k]] = np.all(seg==bs[k])
off=beam[idx]!=0
def count(fac,mask):
    return int(np.sum(mask & (np.abs(dr[idx]-fac*pred)<=1.5*step)))
facs=np.r_[np.linspace(-1.5,-0.5,20),np.linspace(0.5,0.9,10),np.linspace(1.1,1.5,10)]
res={"plan_sha256":"97b62b17c0ed31f774a47ca4908d8fd132ff9a385009cad097a681b371871faa",
     "hits_in_64beam_scans":int(len(idx)),"off_target":int(off.sum()),"off_singletons":int((off&sing).sum()),
     "target_singletons":int((~off&sing).sum()),
     "N_true_off":count(1.0,off&sing),"N_false_off":[count(x,off&sing) for x in facs],
     "N_true_target":count(1.0,(~off)&sing),"N_false_target":[count(x,(~off)&sing) for x in facs],
     "pred_range_Hz_s":[float(pred.min()),float(pred.max())],"factors":facs.tolist()}
m=off&sing&(np.abs(dr[idx]-pred)<=1.5*step)
sel=idx[m]
res["true_off_hits"]=[{"t":float(t[i]),"f":float(f[i]),"drift":float(dr[i]),"pred":float(p),"snr":float(A[i,3]),"beam":int(beam[i])} for i,p in zip(sel,pred[m])]
json.dump(res,open('look3-1.json','w'),indent=1)
nf=np.array(res["N_false_off"])
print("off-target singletons",res["off_singletons"],"| N_true",res["N_true_off"],"| false: median",np.median(nf),"max",nf.max(),"rank",1+int((nf>=res["N_true_off"]).sum()),"of 41")
nt_=np.array(res["N_false_target"]); print("target beam: N_true",res["N_true_target"],"false median",np.median(nt_),"max",nt_.max())
print("pred drift range",res["pred_range_Hz_s"])
