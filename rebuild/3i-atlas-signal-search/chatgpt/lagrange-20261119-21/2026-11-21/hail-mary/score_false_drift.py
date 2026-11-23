#!/usr/bin/env python3
"""OH13 final control: fixed D3 lag-2 X, comet cohort versus original false drifts.
No radio data included; scorer does not pretend to stream GBT voltages.

Input JSON {"cohorts": [{"drift_hz_s": 0.0, "candidates": [{"id":"C03", "scans":
  {"0013":{"X":{"q":0.13,"sidebands":[0.1,...]}}, ...}}]}]}
All candidates, including controls, must be selected using same original OH13 power criterion.
"""
import argparse,json, numpy as np
from pathlib import Path
ON=('0013','0015','0017'); OFF=('0014','0016','0018'); ALL=ON+OFF
DRIFTS=np.round(np.arange(-.2,.2001,.01),3)
DRIFTS=DRIFTS[np.abs(DRIFTS)>1e-9]

def phase_curvature(x,d=2):
    """Exactly invariant to an arbitrary phase offset and linear phase ramp."""
    u=x/np.maximum(abs(x),1e-30)
    return abs(np.mean(u[:-2*d]*u[2*d:]*np.conj(u[d:-d])**2))

def rank(record):
    controls=np.asarray(record['sidebands'],float)
    if controls.size<8 or not np.all(np.isfinite(controls)):raise ValueError('Need >=8 valid sidebands')
    q=float(record['q'])
    if not np.isfinite(q):raise ValueError('NaN source statistic')
    # Rank handles changing receiver distribution without assuming its shape.
    return float((np.count_nonzero(controls<q)+.5*np.count_nonzero(controls==q)+.5)/(len(controls)+1))

def cohort_score(c):
    rows=[]
    for candidate in c['candidates']:
        s=candidate['scans']
        if any(scan not in s or 'X' not in s[scan] for scan in ALL):
            raise ValueError('Missing six-scan X samples for '+candidate['id'])
        r={scan:rank(s[scan]['X']) for scan in ALL}
        diff=np.mean([r[t] for t in ON])-np.mean([r[t] for t in OFF])
        # Extra diagnostic, NOT part of primary statistic.
        strict=all(r[t]>.5 for t in ON) and all(r[t]<.5 for t in OFF)
        rows.append({'id':candidate['id'],'contrast':float(diff),'on_ranks':[r[t] for t in ON],
            'off_ranks':[r[t] for t in OFF],'strict':strict})
    return {'drift_hz_s':float(c['drift_hz_s']),'n':len(rows),
            'mean_ONminusOFF_X_D3':float(np.mean([r['contrast'] for r in rows])) if rows else None,
            'size_scaled_contrast':float(np.mean([r['contrast'] for r in rows])*np.sqrt(len(rows))) if rows else None,
            'candidate_diagnostics':rows}

def analyse(cohorts):
    assert len(cohorts)==41,'Require exactly true drift and 40 original false drifts'
    drifts=[float(c['drift_hz_s']) for c in cohorts]
    if len(set(np.round(drifts,3)))!=41:raise ValueError('Duplicate drift label')
    if set(np.round(drifts,3))!=set(np.round(np.r_[0,DRIFTS],3)):
        raise ValueError('Drift labels must match original OH13 0 and [-.2,.2] step .01 excluding 0')
    rows=[cohort_score(c) for c in cohorts]
    true=next(r for r in rows if abs(r['drift_hz_s'])<1e-9)
    controls=[r for r in rows if abs(r['drift_hz_s'])>=1e-9 and r['n']>0]
    if true['n']!=11:raise ValueError('True cohort must exclude C01 and C02 and contain C03-C13')
    if any(c['id'] not in ['C%02d'%n for n in range(3,14)] for c in next(x for x in cohorts if abs(x['drift_hz_s'])<1e-9)['candidates']):
        raise ValueError('Incorrect true cohort candidates')
    # Group sizes are variable: ranks give comparable per-candidate scales but
    # mean has larger variance for smaller controls. Empirical rank is descriptive.
    p=(1+sum(r['size_scaled_contrast']>=true['size_scaled_contrast'] for r in controls))/(1+len(controls))
    return {'status':'REAL_DATA_ONLY_IF_INPUT_MEASURED','primary':'sqrt(n) times mean ON-minus-OFF local percentile rank, phase curvature lag 2, X','true':true,
        'false_drift_groups_nonempty':len(controls),'empty_false_drift_groups':40-len(controls),
        'control_distribution':{'median':float(np.median([c['size_scaled_contrast'] for c in controls])) if controls else None,
        'max':max([c['size_scaled_contrast'] for c in controls],default=None)},
        'empirical_tail_p':p if controls else None,'p_resolution':1/(1+len(controls)) if controls else None,
        'interpretation':'Even p<=0.025 is NOT a comet confirmation without independent ON replication and systematics. Root-n scaling assumes weak between-candidate dependence and must be checked against frequency-matched empirical controls. If false cohorts also show D3 excess, reject any comet-specific reading.',
        'all_cohorts':[{k:v for k,v in row.items() if k!='candidate_diagnostics'} for row in rows]}

def make_fixture(rng, signal=False):
    groups=[]
    for drift in np.r_[0,DRIFTS]:
        n=11 if drift==0 else int(rng.integers(1,9))
        candidates=[]
        for j in range(n):
            scans={}
            for s in ALL:
                controls=rng.beta(3,10,size=16)
                q=float(rng.beta(3,10))
                if signal and drift==0 and s in ON:q=min(.999,q+.20)
                scans[s]={'X':{'q':q,'sidebands':controls.tolist()}}
            candidates.append({'id':'C%02d'%(j+3) if drift==0 else 'F_%s_%d'%(drift,j),'scans':scans})
        groups.append({'drift_hz_s':float(drift),'candidates':candidates})
    return groups

def selftest():
    rng=np.random.default_rng(20261121)
    n=4096;k=np.arange(n)
    x=np.exp(1j*(.0008*k*k+.031*k))
    y=x*np.exp(1j*(1.45+.3*k))
    assert abs(phase_curvature(x)-phase_curvature(y))<1e-12
    ps=[]
    for _ in range(200):ps.append(analyse(make_fixture(rng))['empirical_tail_p'])
    power=[]
    for _ in range(60):power.append(analyse(make_fixture(rng,True))['empirical_tail_p'])
    print(json.dumps({'validation':'synthetic only','phase_curvature_invariant_to_linear_phase':True,
        'H0_n':len(ps),'H0_p_le_0_05':sum(p<=.05 for p in ps),'H0_p_median':np.median(ps),
        'H1_n':len(power),'H1_p_le_0_05':sum(p<=.05 for p in power),
        'note':'Designed synthetic controls, not a receiver-calibrated null; this tests cohort scoring code only.'},indent=2))

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--self-test',action='store_true');ap.add_argument('--input');ap.add_argument('--output');a=ap.parse_args()
    if a.self_test:selftest()
    elif a.input:
        res=analyse(json.loads(Path(a.input).read_text())['cohorts']);txt=json.dumps(res,indent=2)
        if a.output:Path(a.output).write_text(txt)
        else:print(txt)
    else:ap.error('use --self-test or --input INPUT.json')
