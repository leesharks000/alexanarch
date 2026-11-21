"""PLAN-P3W-D3: stream cc21 scan 0015, ctrl25k and hidrift slices, all 833 frames, both feeds; then gate 4 at (422, 440), Y+.
python3 p3wd3.py stream | gate"""
import json, os, sys, time
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "../../../../../voltages/delaymod")); import dm
dm.CH = 21; dm.FC = 1595.21484375e6 + 93.75e6 - 21.5 * 2.9296875e6
N, DF, FC = dm.N, dm.DF, dm.FC; WD = 65536; F0 = 1625.2936106175184e6
SL = {"ctrl25k": F0 + 25e3, "hidrift": 1625.120423734188e6}                  # as N1625's n1625s.py
b = lambda f: int(np.rint(N // 2 + (FC - f) / DF - 0.5)); S = "0015"; NF = 833


def stream():
    out = {k: np.lib.format.open_memmap(os.path.join(HERE, f"ser_{S}_{k}.npy.part"), mode="w+", dtype=np.float16, shape=(2, NF * WD, 2)) for k in SL}
    T0 = time.time(); n = 0
    for j, X, Y in dm.frames(S, NF):
        for q, Z in enumerate((X, Y)):
            F = dm.fft(Z)
            for k, f in SL.items():
                c0 = b(f); z = np.fft.ifft(np.fft.ifftshift(F[c0 - WD // 2:c0 + WD // 2].astype(np.complex128)))
                out[k][q, j * WD:(j + 1) * WD, 0] = z.real; out[k][q, j * WD:(j + 1) * WD, 1] = z.imag
        n += 1
        if n % 100 == 0: print(n, round(time.time() - T0), flush=True)
    assert n == NF
    for k in SL:
        out[k].flush(); del out[k]
    for k in SL: os.replace(os.path.join(HERE, f"ser_{S}_{k}.npy.part"), os.path.join(HERE, f"ser_{S}_{k}.npy"))
    print("done", round(time.time() - T0))


def gate():
    import lean
    res = {}
    for k in SL:
        def chunks(q, nchunk=64):
            a = np.load(os.path.join(HERE, f"ser_{S}_{k}.npy"), mmap_mode="r")[q]; n = (len(a) // 512) * 512; step = (n // nchunk // 512) * 512
            for i in range(0, n, step):
                x = a[i:min(n, i + step)]; yield x[:, 0].astype(np.float32) + 1j * x[:, 1].astype(np.float32)
        PX, _ = lean.phasors_c64(chunks(0)); PY, _ = lean.phasors_c64(chunks(1))
        res[k] = lean.at_pair_lean(PX, PY, "Y+", 422, 440, 556); del PX, PY
        print(k, res[k], flush=True)
    res["gate4_passes"] = bool(all(res[k]["A"] <= res[k]["sur_max"] for k in SL))
    json.dump(res, open(os.path.join(HERE, "p3wd3_gate.json"), "w"), indent=1); print("gate 4 passes at full length:", res["gate4_passes"])


if __name__ == "__main__":
    stream() if sys.argv[1] == "stream" else gate()
