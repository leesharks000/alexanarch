"""PLAN-HM13-B2: cc21's envelope at Iridium's 90 ms frame.
python3 hm13b2.py SCAN            -> b2_SCAN.npz   (streams coarse channel 21 of the scan, all 833 frames)
python3 hm13b2.py synth SEED A RATE -> b2_synth_SEED.npz (Gaussian noise, a gated tone of amplitude A (x sigma) drifting RATE Hz/s in tile 300; A = 0 is noise only)"""
import json, os, sys, time
import numpy as np, scipy.fft as sf
HERE = os.path.dirname(os.path.abspath(__file__)); M = os.path.normpath(os.path.join(HERE, "../.."))
sys.path.insert(0, os.path.join(M, "../../../voltages/delaymod")); import dm
cc = 21; FC = 1595.21484375e6 + 93.75e6 - (cc + 0.5) * 2.9296875e6; dm.CH = cc; dm.FC = FC
N, C, DF, TBIN = dm.N, dm.C, dm.DF, dm.TBIN
NF = 833; NT = 1024; W = N // NT; DEC = 16; SPF = W // DEC           # 1024 tiles of 1024 bins; 64 envelope samples per frame
FS_E = SPF / (N * TBIN); NE = NF * SPF                                # envelope rate 178.8 Hz, 53,312 samples
FI = 1 / 0.090; FR = 1 / (N * TBIN); K = 4                            # Iridium's frame rate; the frame rate of our own FFT frames (= DF)
rngc = np.random.default_rng(2121); CTRL = []
def clear(b):
    for k in range(1, K + 1):
        f = k * b
        if abs(f - FI * round(f / FI)) < 0.05 or abs(f - FR * round(f / FR)) < 0.05: return False
    return True
while len(CTRL) < 20:
    b = rngc.uniform(9.0, 13.0)
    if clear(b) and all(abs(b - c) > 0.1 for c in CTRL): CTRL.append(b)
CTRL = np.array(CTRL)
fE = np.fft.rfftfreq(NE, 1 / FS_E); KEEP = fE <= 60.0
def avoid(f):
    m = np.ones_like(f, bool)
    for base in (FI, FR):
        h = np.arange(1, int(60 / base) + 2) * base; m &= np.min(np.abs(f[:, None] - h[None, :]), 1) > 0.05
    return m
CLEAN = avoid(fE)
def scores(env):
    """env: (2, NT, NE) -> envelope spectra, r at k*FI, H_I, H_c."""
    e = env - env.mean(-1, keepdims=True); E = np.empty((2, NT, int(KEEP.sum())), np.float32)
    for q in range(2):
        for a in range(0, NT, 64): E[q, a:a + 64] = (np.abs(np.fft.rfft(e[q, a:a + 64], axis=-1)) ** 2)[:, KEEP]
    global fE_k; fE_k = fE[KEEP]
    rI = np.stack([ratio_k(E, k * FI) for k in range(1, K + 1)], -1); HI = rI.sum(-1)
    HC = np.stack([sum(ratio_k(E, k * c) for k in range(1, K + 1)) for c in CTRL], -1)
    return E, rI, HI, HC
def ratio_k(E, nu):
    """Peak within 0.01 Hz of nu over the median of 0.2-1.0 Hz around it, away from both frame families."""
    f = fE_k; cl = CLEAN[KEEP]; pk = (np.abs(f - nu) <= 0.01); bg = (np.abs(f - nu) >= 0.2) & (np.abs(f - nu) <= 1.0) & cl
    return E[..., pk].max(-1) / np.median(E[..., bg], -1)
def gen_synth(seed, A, rate):
    rng = np.random.default_rng(seed); kt = 300; b0 = kt * W + W // 2 + 300; ph = rng.uniform(0, 0.09)
    f0 = (b0 - N // 2) * DF                                                         # baseband frequency of bin b0 after dm.fft's fftshift
    n = np.arange(N)
    for j in range(NF):
        t = (j * N + n) * TBIN; ph_t = 2 * np.pi * (f0 * t + 0.5 * rate * t ** 2)
        g = ((t + ph) % 0.09) < 0.00828
        out = []
        for q in range(2):
            z = (rng.standard_normal(N) + 1j * rng.standard_normal(N)).astype(np.complex64) / np.sqrt(2)
            if A > 0: z = z + (A * g * np.exp(1j * ph_t)).astype(np.complex64)
            out.append(z)
        yield j, out[0], out[1]
if __name__ == "__main__":
    synth = sys.argv[1] == "synth"
    if synth: seed, A, rate = int(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]); src = gen_synth(seed, A, rate); tag = f"synth_{seed}"; s = None
    else: s = sys.argv[1]; src = dm.frames(s, NF); tag = s
    env = np.zeros((2, NT, NE), np.float32); S = np.zeros((2, N)); Sc = np.zeros((2, N))
    if not synth:
        Eph = dm.ephem(); vel = lambda t: np.interp(t, Eph[:, 0], Eph[:, 1]); t0s = 61027 + int(dm.SCANS[s][0]) / 86400.0; v0 = vel(t0s + 0.5 * N * TBIN / 86400.0)
    n = 0; T0 = time.time()
    for j, X, Y in src:
        sh = 0 if synth else int(np.rint(FC * (vel(t0s + (j + 0.5) * N * TBIN / 86400.0) - v0) / C / DF))
        for q, Z in enumerate((X, Y)):
            F = dm.fft(Z); p = (F.real ** 2 + F.imag ** 2); S[q] += p; Sc[q] += np.roll(p, -sh)
            x = sf.ifft(sf.ifftshift(F.reshape(NT, W), axes=1), axis=1, workers=2)
            env[q, :, j * SPF:(j + 1) * SPF] = (x.real ** 2 + x.imag ** 2).reshape(NT, SPF, DEC).mean(-1)
        n += 1
        if n % 100 == 0: print(tag, n, round(time.time() - T0), flush=True)
    assert n == NF, n
    E, rI, HI, HC = scores(env)
    TG = json.load(open(os.path.join(HERE, "targets_hm13b2.json"))); keep = sorted({t for x in TG["targets"] for t in x["tiles"]} | ({299, 300, 301} if synth else set()))
    np.savez_compressed(os.path.join(HERE, f"b2_{tag}.npz"), S=(S / n).astype(np.float32), Sc=(Sc / n).astype(np.float32), rI=rI.astype(np.float32),
                        HI=HI.astype(np.float32), HC=HC.astype(np.float32), ctrl=CTRL, tiles_kept=np.array(keep), Ekept=E[:, keep].astype(np.float32),
                        fE=fE[KEEP].astype(np.float32), nframes=n, v0=(0.0 if synth else v0))
    print(tag, "done", n, round(time.time() - T0), flush=True)
