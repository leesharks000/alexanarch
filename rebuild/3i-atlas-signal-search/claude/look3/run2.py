import json, re, urllib.request, urllib.parse, numpy as np, h5py, hdf5plugin, fsspec, concurrent.futures as cf, sys
import look2_parkes_lib as L
C=299792.458; B="https://bldata.berkeley.edu/ATLAS/"; HALF=3000
FE=json.load(open("freq2.json"))["Femit"]
SESS=["PKS_Jul_31_2025","PKS_Sep_12_2025","PKS_Oct_05_2025"]
def H(q):
    q=dict(format="json",OBJ_DATA="NO",MAKE_EPHEM="YES",**q)
    t=json.load(urllib.request.urlopen("https://ssd.jpl.nasa.gov/api/horizons.api?"+urllib.parse.urlencode(q),timeout=120))["result"]
    return [[x.strip() for x in l.split(",") if x.strip()] for l in t.split("$$SOE")[1].split("$$EOE")[0].strip().splitlines()]
def rr_fixed(t0,t1):
    a=f"'JD {t0+2400000.5-0.003:.6f}'"; b=f"'JD {t1+2400000.5+0.02:.6f}'"
    o=H(dict(COMMAND="'C/2025 N1'",EPHEM_TYPE="OBSERVER",CENTER="'coord@399'",COORD_TYPE="GEODETIC",SITE_COORD="'148.2635,-32.9984,0.415'",START_TIME=a,STOP_TIME=b,STEP_SIZE="'1 m'",QUANTITIES="'1,20'",CSV_FORMAT="YES",CAL_FORMAT="JD",ANG_FORMAT="DEG"))
    v=H(dict(COMMAND="'C/2025 N1'",EPHEM_TYPE="VECTORS",CENTER="'@0'",REF_PLANE="FRAME",START_TIME=a,STOP_TIME=b,STEP_SIZE="'1 m'",VEC_TABLE="'2'",CSV_FORMAT="YES",OUT_UNITS="KM-S",TIME_TYPE="UT"))
    tj=np.array([float(r[0])-2400000.5 for r in o]); ra=np.radians([float(r[-4]) for r in o]); de=np.radians([float(r[-3]) for r in o]); dd=np.array([float(r[-1]) for r in o])
    V=np.array([[float(x) for x in r[5:8]] for r in v])[:len(tj)]
    U=np.stack([np.cos(de)*np.cos(ra),np.cos(de)*np.sin(ra),np.sin(de)],1)
    rr=dd-(V*U).sum(1); return (lambda t: np.interp(t,tj,rr)),(lambda t: np.interp(t,tj,dd))
def scans_of(s):
    names=sorted(set(re.findall(r'href="([^"]*\.0000\.(?:fil|h5))"',urllib.request.urlopen(B+s+"/blc05/",timeout=60).read().decode()))); out=[]
    for n in names:
        u=B+s+"/blc05/"+n
        if n.endswith(".fil"):
            h=L.filhdr(u); size=int(urllib.request.urlopen(urllib.request.Request(u,method="HEAD"),timeout=60).headers["Content-Length"]); nt=(size-h['hdr_len'])//(4*h['nchans']); out.append([n,"fil",h,nt,u])
        else:
            d=h5py.File(fsspec.open(u,"rb",block_size=4<<20).open(),"r")["data"]; a=d.attrs
            h={k:float(a[k]) for k in ("fch1","foff","tsamp","tstart")}; h["nchans"]=d.shape[2]; out.append([n,"h5",h,d.shape[0],u])
    return [x for x in out if x[3]>0]
res={"plan_sha256":"89f844ca95615786115ea7fdd6a8ebca5bfee68caf80788dcfac6b47295927f5","Femit":FE,"sessions":{}}
for s in SESS:
    sc=scans_of(s); fr,dd=rr_fixed(min(x[2]["tstart"] for x in sc),max(x[2]["tstart"] for x in sc))
    def win(x,f0):
        n,kind,h,nt,u=x; t=h["tstart"]+(np.arange(nt)+0.5)*h["tsamp"]/86400; ch=np.rint((f0*(1-fr(t)/C)-h["fch1"])/h["foff"]).astype(int)
        W=np.empty((nt,2*HALF+1),np.float32)
        if kind=="h5": d=h5py.File(fsspec.open(u,"rb",block_size=1<<20).open(),"r")["data"]
        for k in range(nt):
            lo=ch[k]-HALF
            if kind=="fil": a0=h['hdr_len']+(k*h['nchans']+lo)*4; W[k]=np.frombuffer(L.get(u,a0,a0+(2*HALF+1)*4-1),'<f4')
            else: W[k]=d[k,0,lo:lo+2*HALF+1]
        Z=L.zmap(W); return Z.mean(0)*np.sqrt(nt), int((Z>=5).sum())
    S=[x for x in sc if "_S_" in x[0]]; R=[x for x in sc if "_R_" in x[0]]
    rec={"nS":len(S),"nR":len(R),"rr_kms":[float(fr(S[0][2]["tstart"])),float(dd(S[0][2]["tstart"]))],"freq":{}}
    for name,f in FE.items():
        def unit(k):
            f0=f+k*0.001; lS=[win(x,f0) for x in S]; lR=[win(x,f0) for x in R]
            st=lambda l: sum(a for a,_ in l)/np.sqrt(max(len(l),1))
            return k,st(lS),st(lR),sum(p for _,p in lS),sum(p for _,p in lR)
        ks=[0]+[s_*(15+15*k) for k in range(20) for s_ in (1,-1)]
        with cf.ThreadPoolExecutor(4) as ex: out=list(ex.map(unit,ks))
        mid=slice(HALF-500,HALF+501)
        pk={k:(float(Sx[mid].max()),int(np.argmax(Sx[mid]))-500,float(Rx[mid][int(np.argmax(Sx[mid]))]),pS,pR) for k,Sx,Rx,pS,pR in out}
        t0=pk[0]; ctrl=[pk[k][0] for k in ks[1:]]
        rec["freq"][name]={"target":{"peak":t0[0],"offset_Hz":t0[1]*2,"R_at_peak":t0[2],"pixS":t0[3],"pixR":t0[4]},
             "ctrl_peaks":ctrl,"rank":1+int(sum(c>=t0[0] for c in ctrl)),"lead":bool(t0[0]>max(ctrl) and t0[2]<3)}
        print(s,name,"peak %.2f at %+d Hz, R %.2f | ctrl median %.2f max %.2f | rank %d/41 | pix S %d R %d"%(t0[0],t0[1]*2,t0[2],np.median(ctrl),max(ctrl),rec["freq"][name]["rank"],t0[3],t0[4]),flush=True)
    res["sessions"][s]=rec
    json.dump(res,open("look3-2.json","w"),indent=1)
