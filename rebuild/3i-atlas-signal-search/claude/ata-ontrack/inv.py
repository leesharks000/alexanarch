import fsspec,h5py,json,re,sys,urllib.request,concurrent.futures as cf
B="https://bldata.berkeley.edu/ATLAS/ATA_ATLAS/"
fs=fsspec.filesystem("https")
def ls(u):
    try: return _ls(u)
    except Exception as e: print("ERR",u,e,file=sys.stderr); return []
def _ls(u): return [h for h in re.findall(r'href="([^"?][^"]*)"',urllib.request.urlopen(u,timeout=60).read().decode()) if h!="../"]
def hdr(u):
    with fs.open(u,block_size=2**16) as f:
        d=h5py.File(f,"r")["data"]; a={k:(v.item() if hasattr(v,"item") else v) for k,v in d.attrs.items() if k!="DIMENSION_LABELS"}
        a["shape"]=list(d.shape); return a
out={"sessions":{}}
sess=[s.strip("/") for s in ls(B)]
for s in sess:
    scans=[x.strip("/") for x in ls(B+s+"/")]
    out["sessions"][s]={"scans":scans}
# one scan: all subbands, both beams
s0=sess[0]; sc=out["sessions"][s0]["scans"][0]; subs=[x.strip("/") for x in ls(f"{B}{s0}/{sc}/")]
jobs={}
with cf.ThreadPoolExecutor(6) as ex:
    for sb in subs:
        fl=[x for x in ls(f"{B}{s0}/{sc}/{sb}/") if x.endswith(".fbh5")]
        for fn in fl: jobs[(sb,fn[-11:-5])]=ex.submit(hdr,f"{B}{s0}/{sc}/{sb}/{fn}")
    out["subbands"]={f"{k[0]}|{k[1]}":v.result() for k,v in jobs.items()}
json.dump(out,open("inventory-subbands.json","w"),indent=1,default=str)
for k,v in sorted(out["subbands"].items()):
    print(k, round(v["fch1"],3), round(v["fch1"]+v["foff"]*v["nchans"],3), v["src_raj"], v["src_dej"], v["tstart"])
for s,v in out["sessions"].items(): print(s,len(v["scans"]))
