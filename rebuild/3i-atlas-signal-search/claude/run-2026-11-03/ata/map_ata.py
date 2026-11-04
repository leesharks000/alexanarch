"""Access audit and frequency map of the public ATA 3I/ATLAS archive: every directory listed, every .fbh5 header read (fch1, foff, nchans, tsamp, tstart, shape).
  python3 ata/map_ata.py -> ata/ata_map.json (resumable), ata/ata_access.log"""
import urllib.request, urllib.error, re, json, os, concurrent.futures as cf
import fsspec, h5py, hdf5plugin
B = "https://bldata.berkeley.edu/ATLAS/ATA_ATLAS/"; OUT = "ata/ata_map.json"
st = json.load(open(OUT)) if os.path.exists(OUT) else {"files": {}, "denied": []}
log = open("ata/ata_access.log", "a")
def ls(u):
    try: t = urllib.request.urlopen(u, timeout=90).read().decode()
    except urllib.error.HTTPError as e:
        st["denied"].append([u, e.code]); log.write(f"{e.code} {u}\n"); log.flush(); return []
    return [h for h in re.findall(r'href="([^"?][^"]*)"', t) if not h.startswith("..")]
def walk(u, d=0):
    out = []
    for h in ls(u):
        if h.endswith("/") and d < 3: out += walk(u + h, d + 1)
        elif h.endswith(".fbh5"): out.append(u + h)
    return out
files = []
with cf.ThreadPoolExecutor(6) as ex:
    for r in ex.map(lambda s: walk(B + s, 1), [h for h in ls(B) if h.startswith("2025")]): files += r
log.write(f"listed {len(files)} fbh5\n"); log.flush()
fs = fsspec.filesystem("https", block_size=1 << 20)
def head(u):
    if u in st["files"]: return u, st["files"][u]
    try:
        d = h5py.File(fs.open(u))["data"]; a = d.attrs
        return u, {k: float(a[k]) for k in ("fch1", "foff", "tsamp", "tstart")} | {"nchans": int(a["nchans"]), "shape": list(d.shape), "src_raj": float(a["src_raj"]), "src_dej": float(a["src_dej"])}
    except Exception as e:
        log.write(f"ERR {u} {e!r}\n"); log.flush(); return u, {"error": repr(e)[:200]}
with cf.ThreadPoolExecutor(16) as ex:
    for i, (u, h) in enumerate(ex.map(head, files)):
        st["files"][u] = h
        if i % 50 == 0: json.dump(st, open(OUT, "w"))
json.dump(st, open(OUT, "w"), indent=0)
print("files", len(st["files"]), "errors", sum("error" in v for v in st["files"].values()), "denied dirs", len(st["denied"]), flush=True)
