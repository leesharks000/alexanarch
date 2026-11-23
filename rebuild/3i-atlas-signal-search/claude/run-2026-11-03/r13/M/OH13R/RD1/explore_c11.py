"""Exploratory, after RD1's scores (not frozen): what carries C11's low phase-increment complexity in ON 0013 and 0015."""
import json, os, sys
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from common import *
import importlib.util
spec = importlib.util.spec_from_file_location("rd1", os.path.join(os.path.dirname(os.path.abspath(__file__)), "rd1.py")); rd1 = importlib.util.module_from_spec(spec); spec.loader.exec_module(rd1)
WIN = windows(); names = [w[0] for w in WIN]
def read(s, w, frames):
    A = load(s); st = json.load(open(os.path.join(HERE, f"win_{s}.json")))["starts"]
    name, kind, f, _ = WIN[w]
    Z = A[:, w, :, :, 0].astype(np.float32) + 1j * A[:, w, :, :, 1].astype(np.float32)
    med = np.median(np.abs(Z[51:]) ** 2, axis=0); med[med <= 0] = np.median(med); Zn = Z / np.sqrt(med)
    out = []
    for q in (0, 1):
        f0 = frames[0]; nf = len(frames)
        Phi = phase_track(s, f, nf=f0 + nf)[f0 * W:]
        D = dedop(Zn[frames, q, M:M + W], Phi); c = W // 2
        B = np.zeros_like(D); B[:, c - 1:c + 2] = D[:, c - 1:c + 2]
        z = np.fft.ifft(np.fft.ifftshift(B, axes=1), axis=1).ravel()
        seg = z[: (len(z) // 128) * 128].reshape(-1, 128).mean(1)
        dph = np.angle(seg[1:] * np.conj(seg[:-1])); sym = np.digitize(dph, [-np.pi / 2, 0, np.pi / 2])
        R = abs(np.exp(1j * dph).mean()); out.append((round(rd1.lz76(sym), 3), round(float(R), 3), round(float(np.angle(np.exp(1j * dph).mean())), 2), "".join(map(str, sym[:60]))))
    return out
w = names.index("C11"); ctl = [i for i, x in enumerate(WIN) if x[3] == "C11" and x[1] == "ctrl"]
for s in ["0013", "0015", "0017", "0014"]:
    for lab, fr in (("start 0-16", np.arange(0, 17)), ("next 17-33", np.arange(17, 34)), ("body 400-416", np.arange(400, 417))):
        r = read(s, w, fr)
        print(s, lab, "X", r[0][:3], "Y", r[1][:3])
    print("   X symbols 0-16:", read(s, w, np.arange(0, 17))[0][3])
print("C11 controls, 0013 start, (lzP, R):", [read("0013", i, np.arange(0, 17))[0][:2] for i in ctl])
