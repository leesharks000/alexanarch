"""PLAN-K injection on synthetic noise only: a complementary comet-tracking pair at low amplitude must be found in the true frame, not in false ones."""
import numpy as np, json
from kcore import shift, relate, DSET
rng = np.random.default_rng(5); T, N = 47, 1 << 20
drift = np.rint(np.linspace(0, 300, T)).astype(int)            # true frame: 300 bins of drift over the scan
f0, d = 300000, 128
X0 = rng.standard_normal((T, N)).astype(np.float32)
sw = np.where((np.arange(T) // 4) % 2 == 0, 1.0, -1.0)          # period 8 switching
res = {}
for amp in (0.6, 0.9, 1.2):
  X = X0.copy()
  for k in range(T):
    X[k, f0 + drift[k]] += amp * sw[k]; X[k, f0 + d + drift[k]] -= amp * sw[k]
  for name, sh in (("true", drift), ("stationary", np.zeros(T, int)), ("false", np.rint(np.linspace(0, -500, T)).astype(int))):
    o = relate(shift(X, sh))
    z = o[d]["z"]; i = int(np.argmax(z))
    res[f"{amp} {name}"] = {"max_z_at_d": float(z.max()), "argmax": i, "z_at_injected": float(z[f0]),
                 "k2_mean_h2": float(o[d]["k2_h2"].mean()), "k3_best": float(o[d]["k3_s"].max()),
                 "k3_at_injected": [(float(s), int(p)) for f, s, p in zip(o[d]["k3_f"], o[d]["k3_s"], o[d]["k3_p"]) if f == f0]}
print(json.dumps(res, indent=1))
