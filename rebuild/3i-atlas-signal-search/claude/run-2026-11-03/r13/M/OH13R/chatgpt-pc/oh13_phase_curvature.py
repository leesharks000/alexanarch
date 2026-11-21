#!/usr/bin/env python3
"""Original OH13, one phase-curvature representation, NOT general ET detection.
Requires networked Berkeley reader dm.py and original oh13_candidates.json.
"""
import argparse, json, sys, importlib.util
from pathlib import Path
import numpy as np
from scipy.fft import fft, fftshift
N=1<<20
FC=1666.9921875e6
DF=(1/3.41333333333333e-7)/N
LAGS=(1,2,4,8,16,32)
OFFSETS=(-96000,-48000,-24000,-12000,12000,24000,48000,96000)
BAND=(1665.52734375e6,1668.45703125e6)
def closure(x):
    u=x/np.maximum(abs(x),1e-12)
    return np.array([abs(np.mean(u[:-2*d]*u[2*d:]*np.conj(u[d:-d])**2)) for d in LAGS])
def trial(x,nsur=99,seed=1):
    rng=np.random.default_rng(seed); observed=closure(x)
    null=np.array([max(closure(abs(x)*np.exp(2j*np.pi*rng.random(len(x))))) for _ in range(nsur)])
    return {'winning_lag':LAGS[int(observed.argmax())], 'max':float(max(observed)),
            'p_family':float((1+(null>=max(observed)).sum())/(1+nsur)),
            'null_median':float(np.median(null))}
def self_test():
    rng=np.random.default_rng(7717);n=2048;t=np.arange(n)
    noise=(rng.normal(size=n)+1j*rng.normal(size=n))/np.sqrt(2)
    coded=noise+0.9*np.exp(1j*(.0013*t*t+.7*t+.23))
    tone=noise.copy();tone[n//2]+=50
    results={name:trial(a,99,4000+j) for j,(name,a) in enumerate(
            [('quadratic_phase',coded),('pure_noise',noise),('single_strong_tone',tone)])}
    assert results['quadratic_phase']['p_family']<=.05 and results['pure_noise']['p_family']>.05
    print(json.dumps({'status':'synthetic_only','results':results},indent=2))
def nulls(n,nsur,seed):
    rng=np.random.default_rng(seed);arr=[]
    for _ in range(nsur):
        val=np.zeros(6)
        for _ in range(n):
            val+=closure(np.exp(2j*np.pi*rng.random(2048)))
        arr.append(max(val/n))
    return np.array(arr)
def run(args):
    spec=importlib.util.spec_from_file_location('gbt_dm',str(Path(args.dm)/'dm.py'))
    dm=importlib.util.module_from_spec(spec);spec.loader.exec_module(dm)
    dm.CH=7;dm.FC=FC
    catalog=json.loads(Path(args.catalog).read_text())['candidates']
    assert len(catalog)==13
    result={'status':'phase-curvature-pilot','metadata':{
         'frames_per_scan':args.frames,'surrogates':args.surrogates,'lags':LAGS,
         'sideband_offsets_hz':OFFSETS},'candidates':{r['id']:{} for r in catalog}}
    for scan in ('0013','0014','0015','0016','0017','0018'):
        centers={r['id']:next(s for s in r['scans'] if s['scan']==scan)['f_topo_first_Hz']
                 for r in catalog}
        features={}
        print('acquiring',scan,flush=True,file=sys.stderr)
        for j,X,Y in dm.frames(scan,args.frames):
            arrays={'X':fftshift(fft(X)),'Y':fftshift(fft(Y))}
            for cid,f0 in centers.items():
                for key,f in [('target',f0)]+[(str(int(o)),f0+o) for o in OFFSETS
                    if BAND[0]+10000<f0+o<BAND[1]-10000]:
                    i=int(np.rint(N//2-(f-FC)/DF))
                    if not 1024<=i<N-1024:continue
                    for feed,F in arrays.items():
                        features.setdefault((cid,feed,key),[]).append(closure(F[i-1024:i+1024]))
        for (cid,feed,key),a in features.items():
            parts=np.array_split(np.array(a),2,axis=0)
            halves=[{'lag':LAGS[int(m.argmax())],'max':float(max(m)),
                    'all_lags':m.tolist()} for m in [h.mean(axis=0) for h in parts]]
            result['candidates'][cid].setdefault(scan,{}).setdefault(feed,{})[key]=halves
    n1=(args.frames+1)//2;n2=args.frames//2
    controls={n:nulls(n,args.surrogates,20261121+n) for n in (n1,n2)}
    for cid,scans in result['candidates'].items():
        for scan,feeds in scans.items():
            for feed,locations in feeds.items():
                for key,halves in locations.items():
                    for n,h in zip((n1,n2),halves):
                        null=controls[n];h['p_ideal_phase_null']=float(
                            (1+np.count_nonzero(null>=h['max']))/(len(null)+1))
    result['warning']=('Not yet receiver-calibrated. Requires matched sideband ranks, '
        'held-out ON replication, OFF comparisons, and multiple-testing control. '
        'These phase-only statistics cannot exclude unknown signal classes.')
    Path(args.output).write_text(json.dumps(result,indent=2))
    print('saved',args.output)
if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--self-test',action='store_true')
    ap.add_argument('--dm');ap.add_argument('--catalog')
    ap.add_argument('--frames',type=int,default=16)
    ap.add_argument('--surrogates',type=int,default=99)
    ap.add_argument('--output',default='oh13_curvature_features.json')
    a=ap.parse_args()
    if a.self_test:self_test()
    elif a.dm and a.catalog:run(a)
    else:ap.error('real-voltage run requires --dm and --catalog')
