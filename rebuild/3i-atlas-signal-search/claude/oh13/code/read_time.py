"""Along-track time series of each 1667 comet-frame candidate: per 6.08 s step, the normalised power in the 3 channels
the comet path passes through, for the three ON scans (147 steps) and three OFF scans. Tests: per-step SNR, on/off keying
(bimodality), periodicity (FFT of the stacked ON series), and agreement of the time pattern across candidates."""
import sys, json, numpy as np, importlib.util
sys.argv=['x','raw/OH','2.5','2.0']
spec=importlib.util.spec_from_file_location('cf','cometframe_raw.py'); cf=importlib.util.module_from_spec(spec); spec.loader.exec_module(cf)
rows=cf.coincidences(0.0,keep=True)
F=[]; 
for x in sorted(r['f_rest_MHz']*1e6 for r in rows):
    if not F or x-F[-1][-1]>10: F.append([x])
    else: F[-1].append(x)
F=[float(np.mean(c)) for c in F]
def series(s,Fr):
    x=np.load(f'raw/OH_{s}.npy',mmap_mode='r'); h=cf.H[s]; nt,nc=x.shape
    t=h['tstart']+(np.arange(nt)+0.5)*h['tsamp']/86400.0; v=cf.deldot(t); f0=h['fch1_cc']*1e6
    med=np.median(x,axis=0); out=[]
    for k in range(nt):
        ch=int(np.rint((Fr*(1-v[k]/cf.C)-f0)/cf.foff_hz))
        seg=np.asarray(x[k,ch-1:ch+2],float)/med[ch-1:ch+2]-1; out.append(seg.sum())
    # per-step noise from neighbouring channels away from the path
    k=nt//2; ch=int(np.rint((Fr*(1-v[k]/cf.C)-f0)/cf.foff_hz))
    nb=np.asarray(x[:,ch+20:ch+620],float)/med[ch+20:ch+620]-1
    nb3=nb[:,:-2]+nb[:,1:-1]+nb[:,2:]; sd=nb3.std()
    return np.array(out)/sd
R={}
for Fr in F:
    on=np.concatenate([series(s,Fr) for s in cf.ON]); off=np.concatenate([series(s,Fr) for s in cf.OFF])
    R[Fr]=(on,off)
    print(f"{Fr/1e6:.6f} MHz  ON mean/step {on.mean():+.2f}  OFF {off.mean():+.2f}  ON max {on.max():.1f}  steps>2σ ON {int((on>2).sum())}/147 OFF {int((off>2).sum())}/147")
ON=np.array([R[f][0] for f in F]); OFF=np.array([R[f][1] for f in F])
# cross-candidate agreement of time pattern: mean pairwise correlation, ON vs OFF
def mpc(A):
    c=np.corrcoef(A); return float(c[np.triu_indices(len(A),1)].mean())
print('mean pairwise corr of time pattern: ON %.3f  OFF %.3f  (n=%d)'%(mpc(ON),mpc(OFF),len(F)))
# periodicity of the stacked ON series within each scan (49 steps)
st=ON.mean(0); P=np.abs(np.fft.rfft(st-st.mean()))**2; Po=np.abs(np.fft.rfft(OFF.mean(0)-OFF.mean(0).mean()))**2
i=int(np.argmax(P[1:]))+1; print('stacked ON: peak power at period %.1f s, ratio to median %.1f; OFF max ratio %.1f'%(147*6.08/i,P[i]/np.median(P[1:]),Po[1:].max()/np.median(Po[1:])))
np.save('raw/OH_excess_timeseries.npy',np.stack([ON,OFF]))
json.dump(F,open('raw/OH_excess_freqs.json','w'))
