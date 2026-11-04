"""Fetch one coarse channel (1,048,576 fine channels, 2.79 Hz) across all time steps from a remote GBT
rawspec .0000.h5 by HTTP range reads; save float32 .npy plus a small header JSON.
    python3 fetch_cc.py <file name> <freq MHz inside the wanted coarse channel> <out stem>"""
import sys, json, time, fsspec, h5py, hdf5plugin, numpy as np
B = "https://bldata.berkeley.edu/ATLAS/GB_ATLAS/"
name, fmhz, out = sys.argv[1], float(sys.argv[2]), sys.argv[3]
t0 = time.time()
f = fsspec.open(B + name, "rb", block_size=8 << 20).open()
d = h5py.File(f, "r")["data"]; a = d.attrs
fch1, foff, nfpc = float(a["fch1"]), float(a["foff"]), int(a["nfpc"])
i = int((fmhz - fch1) / foff); cc = i // nfpc; lo = cc * nfpc
x = d[:, 0, lo:lo + nfpc].astype(np.float32)
np.save(out + ".npy", x)
hdr = {"file": name, "fch1_cc": fch1 + foff * lo, "foff": foff, "nchan": nfpc, "coarse_channel": cc,
       "tsamp": float(a["tsamp"]), "tstart": float(a["tstart"]), "src_raj": float(a["src_raj"]), "src_dej": float(a["src_dej"]),
       "source": a["source_name"].decode() if isinstance(a["source_name"], bytes) else str(a["source_name"]), "shape": list(x.shape)}
json.dump(hdr, open(out + ".json", "w"), indent=1)
print(out, x.shape, "cc", cc, "%.1fs" % (time.time() - t0))
