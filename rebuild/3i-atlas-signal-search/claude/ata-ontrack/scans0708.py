import fsspec,h5py,json,re,urllib.request,concurrent.futures as cf
B="https://bldata.berkeley.edu/ATLAS/ATA_ATLAS/2025-07-08-04%3A52%3A40/"
fs=fsspec.filesystem("https")
scans=[h.strip("/") for h in re.findall(r'href="([^"]*)"',urllib.request.urlopen(B).read().decode()) if h.startswith("fil_")]
def hdr(sc,b):
    u=f"{B}{sc}/LoD.C1504/{sc}-beam000{b}.fbh5"
    with fs.open(u,block_size=2**16) as f:
        d=h5py.File(f,"r")["data"]; return {k:(v.item() if hasattr(v,"item") else str(v)) for k,v in d.attrs.items() if k!="DIMENSION_LABELS"}|{"shape":list(d.shape),"url":u}
with cf.ThreadPoolExecutor(8) as ex:
    R={(sc,b):ex.submit(hdr,sc,b) for sc in scans for b in (0,1)}
    out=[{"scan":sc,"beam":b,**R[(sc,b)].result()} for sc in scans for b in (0,1)]
json.dump(out,open("scans-20250708.json","w"),indent=1,default=lambda o:o.decode() if isinstance(o,bytes) else str(o))
for x in out: print(x["scan"][4:20],x["beam"],round(x["tstart"],6),x["src_raj"],round(x["src_dej"],4),x["shape"][0],x["source_name"] if isinstance(x["source_name"],str) else x["source_name"].decode())
