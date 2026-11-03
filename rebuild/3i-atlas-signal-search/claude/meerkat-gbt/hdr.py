import sys, fsspec, h5py, hdf5plugin
B="https://bldata.berkeley.edu/ATLAS/GB_ATLAS/"
for name in sys.argv[1:]:
    with fsspec.open(B+name, "rb", block_size=1<<20) as f:
        h=h5py.File(f,"r"); d=h["data"]; a=dict(d.attrs)
        fch1=float(a["fch1"]); foff=float(a["foff"]); n=d.shape[-1]
        lo,hi=sorted([fch1, fch1+foff*n])
        print(name.split("_DIAG")[0][:24], name.split("ATLAS")[1][:10], d.shape, d.chunks, d.compression, "%.3f-%.3f MHz foff=%.4g Hz tsamp=%.3g"%(lo,hi,foff*1e6,float(a["tsamp"])))
