"""Mechanics check of run_ata36.block (not part of the plan's counts): a small real-data block, a tone injected in beam 0 of all eight
discovery scans along the true comet path at a fixed reference-grid channel; the true frame must recover it, false frames should not."""
import os, sys, numpy as np
src = open("run_ata36.py").read().split("for a in SCAT:")[0]
src = src.replace('st = json.load(open(OUT)) if os.path.exists(OUT) else', 'st =')
exec(src)
NBt = 16384; a = ch(3670.0); b = a + NBt; lo = a - OV; cref = a + 5000
_read = read
def read(u, A, B, _r=_read):
    x = _r(u, A, B)
    if u.endswith("beam0000.fbh5"):
        i = [d[0] for d in DISC].index(u); t = TS[u]; v = deldot(t); f0 = (FCH1 + FOFF * (A + B) / 2) * 1e6
        sh = np.rint(f0 * (deldot(T0) - v) / C / FOFF_HZ).astype(int)
        for k in range(NT): x[k, cref + sh[k] - A] *= 1.0 + float(sys.argv[1])
    return x
globals()["read"] = read
r, scb = block(a, b)
print("frame0 on", [h for h in r[0]["on"] if abs(h[0] - cref) <= 2], "n", len(r[0]["on"]), "swap n", len(r[0]["swap"]))
print("false frames recovering it:", sum(any(abs(h[0] - cref) <= 2 for h in f["on"]) for f in r[1:]), "of 40")
print("scatter", list(scb.values())[:4])
