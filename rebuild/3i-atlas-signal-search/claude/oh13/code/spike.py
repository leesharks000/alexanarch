import sys, json, numpy as np, importlib.util
sys.argv=['x','raw/OH','2.5','2.0']
spec=importlib.util.spec_from_file_location('cf','cometframe_raw.py'); cf=importlib.util.module_from_spec(spec); spec.loader.exec_module(cf)
for s in cf.ON+cf.OFF:
    x=np.load(f'raw/OH_{s}.npy',mmap_mode='r'); h=cf.H[s]; nt=x.shape[0]
    f0=h['fch1_cc']*1e6; fo=cf.foff_hz
    lo=int((1665.640e6-f0)/fo); hi=int((1665.585e6-f0)/fo); a,b=min(lo,hi),max(lo,hi)
    blk=np.asarray(x[:,a:b],float); med=np.median(np.asarray(x[:,a-3000:a],float)); 
    sd=1.4826*np.median(np.abs(np.asarray(x[:,a-3000:a],float)-med))
    z=(blk-med)/sd
    pk=z.argmax(1); pv=z.max(1)
    fr=(f0+(a+pk)*fo)/1e6
    t=h['tstart']+(np.arange(nt)+0.5)*h['tsamp']/86400; v=cf.deldot(t)
    exp=1665.6046e6*(1-v/cf.C)/1e6
    strong=pv>20
    if strong.sum()>3:
        k=np.where(strong)[0]; slope=np.polyfit(k*h['tsamp'],fr[k]*1e6,1)[0]
        ce=np.polyfit(np.arange(nt)*h['tsamp'],exp*1e6,1)[0]
        print(s,'strong steps',int(strong.sum()),'of',nt,' f %.6f..%.6f'%(fr[k].min(),fr[k].max()),' drift %.3f Hz/s  comet-path drift %.3f Hz/s'%(slope,ce),' offset from comet path at mid %.1f Hz'%((fr[k]-exp[k]).mean()*1e6))
    else:
        print(s,'no strong tone in 1665.585-1665.640 (max z %.1f)'%pv.max())
