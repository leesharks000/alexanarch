import sys, fsspec, h5py, hdf5plugin
B="https://bldata.berkeley.edu/ATLAS/GB_ATLAS/"
for n in sys.argv[1:]:
    f=fsspec.open(B+n,"rb",block_size=1<<20).open(); d=h5py.File(f,"r")["data"]; a=d.attrs
    fch1,foff,nchan=float(a["fch1"]),float(a["foff"]),d.shape[2]
    print(n.split('_guppi')[0], round(fch1,3), round(fch1+foff*nchan,3))
