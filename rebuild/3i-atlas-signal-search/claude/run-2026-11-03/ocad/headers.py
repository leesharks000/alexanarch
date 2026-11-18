"""Header pass for the cadences outside L band (2025-12-18): fch1, foff, nfpc, shape, tsamp, tstart of every node's rawspec.0000 for every scan. Metadata only."""
import re, json, urllib.request, concurrent.futures as CF, fsspec, h5py, hdf5plugin
B = "https://bldata.berkeley.edu/ATLAS/GB_ATLAS/"
idx = urllib.request.urlopen(B, timeout=60).read().decode()
F = sorted(set(re.findall(r'(blc\d+_guppi_\d+_\d+_DIAG_3I_ATLAS(?:_OFF)?_00(?:29|3[0-4]|4[5-9]|50|6[1-6])\.rawspec\.0000\.h5)', idx)))
def hd(f):
    for a in range(3):
        try:
            h = h5py.File(fsspec.open(B + f, "rb", block_size=1 << 20).open(), "r")["data"]; t = h.attrs
            return f, {"node": f[:5], "scan": f[-20:-16], "fch1": float(t["fch1"]), "foff": float(t["foff"]), "nfpc": int(t["nfpc"]), "shape": list(h.shape), "tsamp": float(t["tsamp"]), "tstart": float(t["tstart"])}
        except Exception as e: err = e
    return f, {"error": str(err)}
with CF.ThreadPoolExecutor(8) as ex: R = dict(ex.map(hd, F))
json.dump(R, open("headers.json", "w"), indent=0); print(len(R), sum("error" in v for v in R.values()))
