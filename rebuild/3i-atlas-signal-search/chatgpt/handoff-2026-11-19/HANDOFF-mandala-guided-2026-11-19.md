Yes. **Copy the handoff below to Claude.** It includes the measurement code, calibration values, results, actual BRIDE time-series data, and a recipe for retrieving the corresponding original voltages.

The embedded data are **derived measurements from real recordings**. They are not synthetic insertions. Full spectrograms and voltages require the public-source retrieval described below.

---

**Handoff for Claude — Lee Sharks’s Mandala-guided 3I/ATLAS experiment**

This is a private exploratory radio-data analysis. The Mandala supplies experimental measurement views and sampling permutations. No evidence establishes that a transmitter used the Mandala, and no convincing comet-associated signal has emerged.

Preserve these distinctions:

- December 18, 2025 GBT voltages are the primary branch.
- July 8, 2025 ATA saved intensities are the secondary branch.
- A proposed matched July 3/July 9 comparison **has not executed**. July 9’s session index was readable, but tested scan directories and the selected file returned HTTP 403.
- The first Mandala experiment was frozen before its feature measurements.
- The subsequent beam-rule audit was **retrospective**, using already known targets.
- The correction to use separate limits for each measurement was motivated after seeing failures of a pooled limit. It has not received independent validation on fresh sky data.
- Original primary assignments remain fixed. Secondary views are not promoted retrospectively.
- Scores below are **not conventional SNR**, calibrated flux, EIRP, or extraterrestrial probabilities. We have not established their relation to the published survey’s SNR-15 threshold.
- No publication, external message, or deposit is authorized by this handoff.

The reported Mandala genesis is July 7, 2025, retrospectively registered in February 2026. The November 29, 2025 blog testimony describes a working eight-operator engine. These dates motivate observing strata; they do not establish physical communication.

The operator-to-radio mappings were proposed in this experiment. They are not algorithms specified by the original literary texts, nor a proof of their complete semantic algebra.

**The data layout is as follows.**

| Property | December GBT | July ATA |
|---|---|---|
| Observing date | December 18, 2025 UTC | July 8, 2025 UTC |
| Recordings per tile | Six sequential scans | Two simultaneous beams |
| Target indices | 0, 2, 4: scans 13, 15, 17 | Beam 0, provisionally |
| Reference indices | 1, 3, 5: scans 14, 16, 18 | Beam 1, provisionally |
| Available product | Two-feed complex voltages | Saved Stokes-I intensity |
| Power-raster orientation | Ascending RF × time | Ascending RF × time |
| Raster shape | 256 × 64 | 256 × 16 |
| Voltage-phase analysis | Available | Unavailable |
| Selected tiles | 48 | 48 |
| Roles | 24 target, 12 calibration, 12 reserved | Same |

December has two resolutions:

```text
D_short_wide:
  duration_s = 1.431655765333332
  bandwidth_hz = 11444.091796875011
  raster_frequency_bin_hz = 44.70348358154301
  raster_time_row_s = 0.02236962133333331

D_long_narrow:
  duration_s = 5.726623061333328
  bandwidth_hz = 2861.0229492187527
  raster_frequency_bin_hz = 11.175870895385753
  raster_time_row_s = 0.08947848533333325

J_intensity:
  duration_s = 268.435456
  bandwidth_hz = 488.28125
  raster_frequency_bin_hz = 1.9073486328125
  raster_time_row_s = 16.777216
```

December coordinates came from archived coarse channel 7 and three short raw windows beginning at raw blocks 0, 816 and 1632. These are selected excerpts, not continuous coverage of the scans.

July used three native chunks, indices `[99, 163, 176]`, in subband `LoC.C0736/`, approximately covering:

```text
7961.25–7961.75 MHz
7993.25–7993.75 MHz
7999.75–8000.25 MHz
```

The July source scan has 19 native time integrations. Selected tiles contain 16. Both data and mask arrays were acquired. All selected tiles were valid; masked or invalid draws were not replaced.

The provisional July beam assignment is consistent with the header pointing offset and published observing strategy, but this work did not independently reconstruct beamformer calibration.

**The measurements have these meanings.**

| Name | Implemented measurement |
|---|---|
| BRIDE | Strongest positive temporal correlation between nonadjacent frequency groups |
| BEAST | Fourier concentration of unit-voltage phasors raised to orders 2, 4 or 8 |
| MIRROR | Maximum overlap-normalized recurrence under time delay and RF translation |
| SHADOW | Strongest rectangular negative residual |
| FLAME | Strongest rectangular positive residual |
| THUNDER | Strongest temporal step, preserving direction |
| INVERSION | Magnitude of signed third-moment asymmetry of temporal increments |
| SILENCE | Longest consecutive below-baseline run |
| TS | Temporal difference after extracting deficits |
| ST | Deficit extraction after temporal difference |

“SILENCE” means a deficit relative to a declared baseline. It does not mean zero received energy. Missing or masked measurements cannot count as silence.

Each tile received a reproducible permutation of the eight operators—seven for July, where BEAST is unavailable. The first three were primary. If THUNDER and SILENCE both occurred among those three, their drawn order also selected TS or ST.

```text
Root seed:
99937588011255287591726421231676650532

Hexadecimal:
4b2f47824e7e437bd86f31fd4b9f7424

seed modulo 2**32:
1268741156

Original operator order:
BRIDE, BEAST, MIRROR, SHADOW, FLAME, THUNDER, INVERSION, SILENCE
```

The seed came from a curated operator/chronology manifest plus a fresh nonce. It was not a hash of the entire blog.

**This is the measurement implementation.** Formatting is expanded for transfer; operations follow the executed core. Inputs to `views` should be positive, finite, unmasked float64 power rasters. `x`, when available, has shape `(2, 16384)`.

```python
import numpy as np
from scipy import fft, signal

OPS = [
    "BRIDE", "BEAST", "MIRROR", "SHADOW", "FLAME",
    "THUNDER", "INVERSION", "SILENCE", "TS", "ST"
]

def prefix(a):
    return np.pad(a.cumsum(0).cumsum(1), ((1, 0), (1, 0)))

def boxes(a, wf, wt):
    I = prefix(a)
    return (
        I[wf:, wt:] - I[:-wf, wt:]
        - I[wf:, :-wt] + I[:-wf, :-wt]
    ) / (wf * wt)

def boxmax(a, timewidths=(1, 4, 16)):
    best = (-np.inf, {})
    for wf in [8, 32, 128]:
        if wf > a.shape[0]:
            continue
        for wt in timewidths:
            if wt > a.shape[1]:
                continue
            b = boxes(a, wf, wt)
            ij = np.unravel_index(np.argmax(b), b.shape)
            value = float(b[ij])
            if value > best[0]:
                best = (
                    value,
                    {
                        "f_start": int(ij[0]),
                        "t_start": int(ij[1]),
                        "f_width": wf,
                        "t_width": wt,
                    },
                )
    return {"score": max(0, best[0]), **best[1]}

def voltage_power(x):
    # Two feeds; 64 nonoverlapping windows of 256 samples.
    z = fft.fftshift(
        fft.fft(
            np.asarray(x).reshape(2, 64, 256)
            * signal.windows.hann(256, sym=False)[None, None, :],
            axis=-1,
        ),
        axes=-1,
    )
    # Reverse FFT frequency order because source channel bandwidth is negative.
    return (abs(z) ** 2).sum(0).T[::-1]

def fields(P):
    L = np.log(np.maximum(P, np.finfo(float).tiny))
    out = []
    for axis in [0, 1]:
        a = L - np.median(L, axis=axis, keepdims=True)
        center = np.median(a)
        scale = 1.4826 * np.median(abs(a - center))
        out.append(a / max(scale, 1e-12))
    return out

# A = frequency-median subtraction at each time:
#     retains persistent narrow spectral peaks/deficits.
# B = time-median subtraction at each frequency:
#     retains temporal change.
# Scaling is global MAD for each field, not Gaussian sigma.

def phase_grain(x):
    seg = np.asarray(x).reshape(2, 4, 4096)
    u = seg / np.maximum(abs(seg), np.finfo(float).tiny)
    best = (-1, {})
    for q in [2, 4, 8]:
        z = abs(fft.fft(u ** q, axis=-1)) / 4096
        ij = np.unravel_index(np.argmax(z), z.shape)
        value = float(z[ij])
        if value > best[0]:
            best = (
                value,
                {
                    "order": q,
                    "feed": int(ij[0]),
                    "segment": int(ij[1]),
                    "powered_bin": int(ij[2]),
                },
            )
    return {"score": best[0], **best[1]}

def views(P, x=None):
    P = np.asarray(P, dtype=float)
    A, B = fields(P)
    F, T = A.shape
    result = {}

    # BRIDE: 16 frequency groups; exclude adjacent pairs.
    groups = B.reshape(16, F // 16, T).mean(1)
    groups -= groups.mean(1, keepdims=True)
    norm = np.sqrt((groups ** 2).sum(1))
    C = groups @ groups.T / np.maximum(
        norm[:, None] * norm[None, :], 1e-20
    )
    ii, jj = np.triu_indices(16, k=2)
    j = int(np.argmax(C[ii, jj]))
    result["BRIDE"] = {
        "score": float(max(0, C[ii[j], jj[j]])),
        "group_a": int(ii[j]),
        "group_b": int(jj[j]),
    }

    result["BEAST"] = phase_grain(x) if x is not None else None

    # MIRROR: double-median log contrast, then translated recurrence.
    M = np.log(np.maximum(P, np.finfo(float).tiny))
    M -= np.median(M, axis=1, keepdims=True)
    M -= np.median(M, axis=0, keepdims=True)
    C = signal.fftconvolve(M, M[::-1, ::-1], mode="full")
    E = prefix(M * M)
    ds = np.arange(-64, 65)[:, None]
    dt = np.arange(1, min(24, T // 2) + 1)[None, :]

    def rect(f0, f1, t0, t1):
        return E[f1, t1] - E[f0, t1] - E[f1, t0] + E[f0, t0]

    e0 = rect(np.maximum(ds, 0), np.minimum(F, F + ds), dt, T)
    e1 = rect(np.maximum(-ds, 0), np.minimum(F, F - ds), 0, T - dt)
    corr = C[F - 1 + ds, T - 1 + dt] / np.maximum(
        np.sqrt(e0 * e1), 1e-30
    )
    ij = np.unravel_index(np.argmax(corr), corr.shape)
    result["MIRROR"] = {
        "score": float(corr[ij]),
        "f_shift_bins": int(ds[ij[0], 0]),
        "t_shift_rows": int(dt[0, ij[1]]),
    }

    for name, sign in [("SHADOW", -1), ("FLAME", 1)]:
        candidates = [
            {**boxmax(sign * field), "normalization": i}
            for i, field in enumerate([A, B])
        ]
        result[name] = max(candidates, key=lambda v: v["score"])

    # THUNDER: every split with >=2 rows on each side.
    I = np.pad(np.cumsum(B, axis=1), ((0, 0), (1, 0)))
    best = (-1, {})
    for split in range(2, T - 1):
        d = (
            (I[:, -1] - I[:, split]) / (T - split)
            - I[:, split] / split
        ) * np.sqrt(split * (T - split) / T)
        for wf in [8, 32, 128]:
            v = np.convolve(d, np.ones(wf) / wf, mode="valid")
            k = int(np.argmax(abs(v)))
            score = float(abs(v[k]))
            if score > best[0]:
                best = (
                    score,
                    {
                        "split": split,
                        "f_start": k,
                        "f_width": wf,
                        "direction": int(np.sign(v[k])),
                    },
                )
    result["THUNDER"] = {"score": best[0], **best[1]}

    # INVERSION: signed increment asymmetry.
    best = (-1, {})
    for wf in [8, 32, 128]:
        g = boxes(B, wf, 1)
        d = np.diff(g, axis=1)
        ratio = (d ** 3).sum(1) / np.maximum(
            (abs(d) ** 3).sum(1), 1e-30
        )
        k = int(np.argmax(abs(ratio)))
        if abs(ratio[k]) > best[0]:
            best = (
                float(abs(ratio[k])),
                {
                    "f_start": k,
                    "f_width": wf,
                    "signed_asymmetry": float(ratio[k]),
                },
            )
    result["INVERSION"] = {"score": best[0], **best[1]}

    # SILENCE: longest run below -1 robust unit, in either baseline.
    best = (-1, {})
    for mode, field in enumerate([A, B]):
        for wf in [8, 32]:
            g = boxes(field, wf, 1)
            low = g < -1
            runs = np.zeros(g.shape[0], int)
            for t in range(T):
                runs = np.where(low[:, t], runs + 1, 0)
                k = int(np.argmax(runs))
                value = float(runs[k] / np.sqrt(T))
                if value > best[0]:
                    best = (
                        value,
                        {
                            "f_start": k,
                            "f_width": wf,
                            "end_row": t,
                            "run_rows": int(runs[k]),
                            "threshold_robust_unit": -1,
                            "normalization": mode,
                        },
                    )
    result["SILENCE"] = {"score": best[0], **best[1]}

    result["TS"] = boxmax(
        np.diff(np.maximum(-B, 0), axis=1), (1, 4)
    )
    result["ST"] = boxmax(
        np.maximum(-np.diff(B, axis=1), 0), (1, 4)
    )
    return result
```

**The original nomination rule and the later audit rule must remain separate.**

For each measurement:

```python
on = max(target_recording_scores)
off = max(reference_recording_scores)

old_nomination = (
    on > original_cutoff
    and on > 1.25 * off
)
```

The original cutoff is the 95th percentile of pooled calibration-recording scores within the applicable stratum.

The audit defines:

```python
score_scale = max(
    1.4826 * MAD(calibration_recording_scores),
    0.05 * median(abs(calibration_recording_scores)),
    0.001,
)

contrast = (on - off) / score_scale
```

A **per-view stress-envelope pass** requires:

```python
pass_this_view = (
    old_nomination
    and contrast > envelope_cutoff_for_this_view
)

primary_pass = any(
    pass_this_view
    for view in preassigned_primary_views
)
```

Envelope cutoffs are maxima over finite shared-pattern, zero-addition and swapped-zero training controls. They do not establish a universal false-alarm rate.

Here are the numerical calibration values. Arrays follow the listed intensity-operator order:

```python
INTENSITY_OPS = [
    "BRIDE", "MIRROR", "SHADOW", "FLAME", "THUNDER",
    "INVERSION", "SILENCE", "TS", "ST"
]

ORIGINAL_CUTOFF = {
    "D_short_wide": [
        0.38469500631874554,
        0.05652247210191197,
        2.919625033443001,
        1.6733592223146623,
        2.158286596907836,
        0.5279962782637866,
        0.40625,
        2.2624335939311857,
        3.19763741142153,
    ],
    "D_long_narrow": [
        0.44327235230631157,
        0.05598523586453802,
        2.7546463310265086,
        1.7408131517808405,
        2.21937813003504,
        0.5574020423517977,
        0.375,
        2.5391384321344175,
        3.284890102532298,
    ],
    "J_intensity": [
        0.7955910495756379,
        0.0864314364858965,
        1.537804924619676,
        1.4866416819449104,
        1.5900201496557596,
        0.9033023801707849,
        0.25,
        1.502677047142389,
        2.5643977211756344,
    ],
}

SCORE_SCALE = {
    "D_short_wide": [
        0.04476377188899714,
        0.004103238014189982,
        0.1542271860347247,
        0.07588186767532715,
        0.13980233135692233,
        0.04483515553503896,
        0.185325,
        0.15041667223053024,
        0.21218074739879833,
    ],
    "D_long_narrow": [
        0.07568044080365044,
        0.0038383709814450435,
        0.2431942341337368,
        0.10845995161027432,
        0.1979316555127188,
        0.04994572689389832,
        0.018750000000000003,
        0.26392058291381,
        0.3017504843904751,
    ],
    "J_intensity": [
        0.05479813057279881,
        0.012433743346631889,
        0.12387574523162001,
        0.1050650984075806,
        0.13887242694205687,
        0.07737081734105167,
        0.0125,
        0.1476953353191091,
        0.21209971803965796,
    ],
}

ENVELOPE_CUTOFF = {
    "D_short_wide": [
        1.9729156984766547,
        2.845629305619798,
        7.518274925222702,
        3.4960711600972627,
        4.5018575622041075,
        3.590618930715488,
        2.023472278429786,
        9.197772959096065,
        5.386990666843413,
    ],
    "D_long_narrow": [
        1.8384043989575463,
        4.0991904339809,
        2.146473395615006,
        3.0536327966829475,
        7.367958935032967,
        3.407442140485045,
        19.999999999999996,
        2.4480464175084964,
        2.2369715788451616,
    ],
    "J_intensity": [
        4.034003166268455,
        3.7773171236959127,
        8.649571033873356,
        14.03003643997898,
        14.404571766413731,
        2.767658216628756,
        100.0,
        4.945918839382391,
        3.9168591032348856,
    ],
}

BEAST_ORIGINAL_CUTOFF = {
    "D_short_wide": 0.05902494506407352,
    "D_long_narrow": 0.05819143671405881,
}
```

BEAST was excluded from this intensity-only beam audit.

The unsuccessful pooled audit instead required every view to exceed a single contrast cutoff:

```python
POOLED_CUTOFF = {
    "D_short_wide": 9.197772959096065,
    "D_long_narrow": 19.999999999999996,
    "J_intensity": 100.0,
}
```

This created provable blind spots:

```text
July BRIDE:
  score bounded [0,1]
  maximum possible contrast = 1 / 0.05479813057279881
                            = 18.2487977153
  pooled cutoff = 100
  therefore impossible to pass through BRIDE.

July INVERSION:
  maximum possible contrast = 12.9247697564
  pooled cutoff = 100
  therefore impossible to pass through INVERSION.

December long-window BRIDE:
  maximum possible contrast = 13.2134536927
  pooled cutoff = 20
  therefore impossible to pass through BRIDE.
```

This establishes defects in our proposed pooled rule. It does not establish defects in every SETI pipeline.

**D19 is the retained BRIDE example. These are its coordinates and observed results.**

```python
D19 = {
    "dataset": "December18_GBT",
    "role": "target",
    "scale": "short_wide",
    "M": 4096,
    "frames": 4,
    "center_index": 63733,
    "window": 2,
    "first_frame": 1,
    "raw_block_start": 1634,
    "rf_center_hz": 1668278963.305056,
    "bandwidth_hz": 11444.091796875011,
    "duration_s": 1.431655765333332,
    "start_in_scan_s": 292.41569006933304,
    "operator_permutation": [
        "BRIDE", "SHADOW", "FLAME", "INVERSION",
        "BEAST", "THUNDER", "MIRROR", "SILENCE"
    ],
    "primary_views": ["BRIDE", "SHADOW", "FLAME"],
}
```

The RF center identifies the analyzed window, not a detected transmitter frequency.

Original BRIDE maxima:

| Scan | Pointing | Maximum BRIDE score | Winning groups |
|---:|---|---:|---|
| 13 | ON | 0.42468361501242713 | 7, 15 |
| 14 | OFF | 0.2951484342809225 | 2, 15 |
| 15 | ON | 0.33883159479535674 | 3, 13 |
| 16 | OFF | 0.28750540378017403 | 5, 15 |
| 17 | ON | 0.2877469875522553 | 0, 15 |
| 18 | OFF | 0.2759581108912088 | 2, 6 |

**Those maxima do not identify the same relation in every scan.** Each recording independently selects its strongest eligible pair.

For D19:

```text
ON maximum     = 0.42468361501242713
OFF maximum    = 0.2951484342809225
Original cut   = 0.38469500631874554
Score scale    = 0.04476377188899714
Contrast       = 2.893750353583232
Per-view limit = 1.9729156984766547

Original nomination: PASS
Per-view stress envelope: PASS
Repeated fixed relation: NOT DEMONSTRATED
```

Holding the original winning groups **7 and 15** fixed gives:

```python
# Order: scans 13,14,15,16,17,18.
original_fixed_pair_correlations = [
     0.4246836150124272,
    -0.24228638477591996,
    -0.007210347068977389,
    -0.1265863457753575,
    -0.27192629087502884,
     0.06964021426682021,
]

# Same frequency groups, preselected additional time window.
# New start within each scan: 0.357913941333333 seconds.
additional_time_fixed_pair_correlations = [
     0.08724322589972937,
     0.23309582276723925,
    -0.13683944731193382,
    -0.011779703064592086,
     0.0895950522491814,
     0.1085021632413962,
]
```

Thus the initially positive relation is absent in the other two original ON recordings and does not pass the additional-time check. No Doppler-track localization or transmitter identification was established by this test.

**The following payload contains actual D19 measurements, sufficient to inspect that fixed pair without downloading anything.**

It contains the time-centered BRIDE group traces for groups 7 and 15:

```text
shape = (6 recordings, 2 frequency groups, 64 time rows)
recording order = scans 13,14,15,16,17,18
group order = 7,15
dtype = little-endian float32
uncompressed bytes = 3072

Construction:
  B = time-median-subtracted, globally MAD-scaled log power
  groups = B.reshape(16,16,64).mean(axis=1)
  groups -= groups.mean(axis=1, keepdims=True)
  retain groups [7,15]
  cast derived traces to float32

Group 7 occupies raster bins 112:128.
Group 15 occupies raster bins 240:256.
```

This is a small precision-reduced copy of derived traces, not raw voltage. Float32 quantization changes the reported correlations by approximately \(10^{-8}\) or less.

Copy this executable block intact:

```python
import base64
import hashlib
import zlib
import numpy as np

D19_PAIR_B64 = """
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
mnPIHw==
"""

raw = zlib.decompress(base64.b64decode(D19_PAIR_B64))
assert len(raw) == 3072
assert hashlib.sha256(raw).hexdigest() == (
    "e16488f0b6d62f31402309f816e44328918d94c948cf55804888ad221a6e86ca"
)

traces = np.frombuffer(raw, dtype="<f4").reshape(6, 2, 64)

for scan, pair in zip(range(13, 19), traces):
    print(scan, np.corrcoef(pair)[0, 1])

# Expected approximately:
# 13   0.4246836157042849
# 14  -0.24228639083191764
# 15  -0.00721034249888216
# 16  -0.12658634393884863
# 17  -0.271926290185296
# 18   0.0696402176656476
```

Those traces permit fixed-pair correlation, lag, robustness and waveform-shape work. They cannot reproduce the search over all 105 nonadjacent group pairs or the other measurements. For that, reconstruct the full excerpt.

**The original D19 voltage excerpt can be reconstructed from bounded public reads.**

The source root is [GB_ATLAS_raw](https://bldata.berkeley.edu/ATLAS/GB_ATLAS_raw/). A fresh 64-byte probe to the relevant scan-13 file returned HTTP 206 with the expected byte range.

Recorded layout:

```text
Raw sample interval TB = 3.41333333333333e-7 seconds
Raw FFT length N       = 1048576
Raw FFT duration       = N*TB = approximately 0.357913941333333 seconds

Raw blocks per source file = 128
Whole raw-block payload    = 134217728 bytes
Padded header              = 7168 bytes
Whole block stride         = 134224896 bytes

Selected coarse channel    = 7
Bytes per selected channel = 2097152
Channel offset within whole block payload = 7*2097152

Selected bytes are int8:
  [feed0_real, feed0_imag, feed1_real, feed1_imag]
repeated in time.

Frozen normalization:
  clip -128 to -127, then divide by 127.

D19 uses global raw blocks 1634 through 1641 inclusive.
These lie in source file index 12, local blocks 98 through 105.

First selected byte:
  98*134224896 + 7168 + 7*2097152
  = 13168727040
```

The following recipe reconstructs one scan by default, requiring 16 MiB of payload. Calling it for all six scans requires 96 MiB. The full live retrieval has not been rerun in this handoff; the layout and decoder reproduce the recorded method.

```python
import hashlib
import urllib.request
import numpy as np
from scipy import fft

RAW_ROOT = "https://bldata.berkeley.edu/ATLAS/GB_ATLAS_raw/"

SMJD = {
    13: 17226, 14: 17543, 15: 17861,
    16: 18179, 17: 18497, 18: 18814,
}

FIRST_D19_BLOCK_SHA256 = {
    13: "bca4d54ed4008a646c9c7d1735f2dbe433f1678722132f4658baf81bdbe0d899",
    14: "0b58a5f78b9ac272f56c81b9392314f14c142bf1970d5d5c561b8a9ec7889930",
    15: "715962ce43ac6476fb18ca5cabaa9e14daa611a4fe67b59f9f859986112fcb49",
    16: "68e305dc9ce1e7da2614c2e654b1e7b628b2a44a4465f2639cfdb3d40eb38129",
    17: "db21aa987905d991a545af018e9e02c5d2b895a8bcfd17e9eb7e988e1fc90963",
    18: "d1acf0056e4f07efb2909ec4ad7199e35750eb1823769bced8157bfc10f256a8",
}

def fetch_channel_block(scan, block):
    file_index, local_block = divmod(block, 128)
    name = (
        f"blc23_guppi_61027_{SMJD[scan]}_DIAG_3I_ATLAS_"
        f"{scan:04d}.{file_index:04d}.raw"
    )
    count = 2097152
    start = local_block * 134224896 + 7168 + 7 * count
    stop = start + count - 1

    req = urllib.request.Request(
        RAW_ROOT + name,
        headers={"Range": f"bytes={start}-{stop}"}
    )

    with urllib.request.urlopen(req, timeout=60) as response:
        # Refuse a full-file fallback.
        assert response.status == 206
        assert response.headers["Content-Range"].startswith(
            f"bytes {start}-{stop}/"
        )
        payload = response.read(count + 1)

    assert len(payload) == count
    if block == 1634:
        assert hashlib.sha256(payload).hexdigest() == (
            FIRST_D19_BLOCK_SHA256[scan]
        )
    return payload

def reconstruct_d19(scan=13, first_block=1634):
    N = 1048576
    M = 4096
    center = 63733
    x = np.empty((2, 16384), dtype=np.complex64)

    for frame in range(4):
        pieces = [
            np.frombuffer(
                fetch_channel_block(scan, first_block + 2*frame + j),
                dtype=np.int8
            ).reshape(-1, 4)
            for j in [0, 1]
        ]
        raw = (
            np.maximum(np.concatenate(pieces).astype(np.float32), -127)
            / np.float32(127)
        )

        for feed in [0, 1]:
            v = raw[:, 2*feed] + 1j*raw[:, 2*feed + 1]
            X = fft.fftshift(fft.fft(v))
            selected = X[center-M//2:center+M//2]
            y = fft.ifft(fft.ifftshift(selected)) * np.float32(M/N)
            x[feed, frame*M:(frame+1)*M] = y

    # Match the original search's power-product precision:
    P = voltage_power(x.astype(np.complex128)).astype(np.float32)
    return x, P

# Uses voltage_power(), views() and fields() defined above:
# x13, P13 = reconstruct_d19(13)
# result13 = views(P13.astype(float), x13.astype(np.complex128))
# print(result13["BRIDE"])
#
# Expected: score approximately 0.42468361501242713,
#           groups 7 and 15.
#
# Additional-time excerpt at the same RF:
# x13_extra, P13_extra = reconstruct_d19(13, first_block=2)
```

The frozen RF convention is:

```python
N = 1048576
TB = 3.41333333333333e-7
TF = N * TB
F0 = 1668457031.25  # Hz

rf_center_hz = F0 - center_index / TF
```

The negative RF sign was independently checked in the original decoder.

**The remaining original primary flags are summarized here.**

| Tile | Window center MHz | Primary feature | ON max | OFF max | Outcome after per-view audit |
|---|---:|---|---:|---:|---|
| D7 | 1665.633299 | SILENCE | 0.5 | 0.375 | Fails |
| D13 | 1666.518266 | SILENCE | 0.5 | 0.375 | Fails |
| D19 | 1668.278963 | BRIDE | 0.424684 | 0.295148 | Passes envelope; repeat test fails |
| D27 | 1667.765751 | THUNDER | 2.488272 | 1.927965 | Fails |
| D40 | 1665.668006 | SILENCE | 0.5 | 0.375 | Fails |
| J32 | 7999.861586 | FLAME | 1.508116 | 1.176100 | Fails |
| J47 | 7999.813866 | SILENCE | 0.5 | 0.25 | Fails |

All five December primary features failed their fixed-feature check in a preselected additional time window.

For the December SILENCE examples:

```text
D7:
  winning scan = 17
  normalization = B
  f_start = 21
  f_width = 8
  end_row = 39
  run_rows = 4
  duration approximately 89.48 ms

D13:
  winning scan = 15
  normalization = B
  f_start = 229
  f_width = 8
  end_row = 30
  run_rows = 4
  duration approximately 89.48 ms

D40:
  winning scan = 15
  normalization = A
  f_start = 157
  f_width = 8
  end_row = 31
  run_rows = 4
  duration approximately 357.91 ms

Each threshold is below -1 robust unit in the frequency-averaged field.
```

For July:

```text
J32 / FLAME:
  native_start_channel = 46195719
  first_time_row = 3
  power slice = data[3:19, 0, 46195719:46195975]
  winning target feature:
    normalization = A
    f_start = 202
    f_width = 8
    t_start = 0
    t_width = 1

J47 / SILENCE:
  native_start_channel = 46170700
  first_time_row = 3
  power slice = data[3:19, 0, 46170700:46170956]
  winning target feature:
    normalization = B
    f_start = 24
    f_width = 8
    end_row = 14
    run_rows = 2
  duration = 33.554432 seconds
```

The July source files are obtained from:

```python
JULY_FOLDER = (
    "https://bldata.berkeley.edu/ATLAS/ATA_ATLAS/"
    "2025-07-08-04%3A52%3A40/"
    "fil_60864_17864_64385681_JPLH_ATLAS_0001/"
    "LoC.C0736/"
)

JULY_FILENAME = (
    "fil_60864_17864_64385681_JPLH_ATLAS_0001-"
    "beam{beam:04d}.fbh5"
)

JULY_HEADER = {
    "shape": [19, 1, 50331648],
    "chunks": [1, 1, 262144],
    "dtype": "float32",
    "compression": "gzip",
    "compression_level": 0,
    "fch1_MHz": 7911.750000953674,
    "foff_MHz": 1.9073486328125e-6,
    "tsamp_s": 16.777216,
    "tstart_MJD": 60864.20675925926,
}
```

Frequency increases with channel index. Read the corresponding `mask` slice as well as `data`. Data slices are time × frequency; transpose them before passing to `views`.

Two secondary December diagnostics survive per-view envelopes but were **not primary**:

```text
D39 / SHADOW:
  target cohort
  center = 1667.1532429754734 MHz
  long_narrow
  start_in_scan_s = 146.02888806399986
  primary views = INVERSION, BEAST, THUNDER
  SHADOW was secondary
  contrast = 2.561203057278626
  envelope cutoff = 2.146473395615006

D23 / MIRROR:
  reserved cohort
  center = 1666.2932932376862 MHz
  short_wide
  start_in_scan_s = 293.48943189333306
  primary views = FLAME, BEAST, THUNDER
  MIRROR was secondary
  contrast = 3.5095118355828236
  envelope cutoff = 2.845629305619798
```

Promoting D39 after inspecting its secondary results would require acknowledging the same selection latitude that surfaces the reserved D23.

**The controls used these exact pattern families.**

These are additions to power rasters after voltage projection. They are not end-to-end electromagnetic transmitter simulations.

```python
def pattern(family, seed, F, T):
    rng = np.random.default_rng(seed)
    f = np.arange(F)[:, None]
    time = np.arange(T)[None, :]

    if family == "burst":
        c = rng.uniform(32, F-32)
        epoch = rng.uniform(2, T-3)
        width = rng.uniform(0.6, max(0.7, T/16))
        p = (
            np.exp(-0.5*((f-c)/1.4)**2)
            * np.exp(-0.5*((time-epoch)/width)**2)
        )

    elif family == "linked":
        c1 = rng.uniform(25, 85)
        c2 = rng.uniform(F-85, F-25)
        shape = 0.15 + (rng.random(T) > 0.45).astype(float)
        p = (
            np.exp(-0.5*((f-c1)/1.3)**2)
            + np.exp(-0.5*((f-c2)/1.3)**2)
        ) * shape[None, :]

    elif family == "gaps":
        c = rng.uniform(32, F-32)
        gate = np.ones(T)
        period = int(rng.integers(5, 9))
        phase = int(rng.integers(period))
        gate[(np.arange(T)+phase) % period < 2] = 0
        p = np.exp(-0.5*((f-c)/1.5)**2) * gate[None, :]

    else:
        raise ValueError(family)

    return p / p.mean()

# For each active recording:
#
# changed_power = original_power + (
#     pattern(family, seed, F, T)
#     * rho
#     * original_power.mean()
# )
#
# Target-only challenge:
#   active = scans 13,15,17, or July beam 0.
#
# Shared challenge:
#   active = every target and reference recording.
#
# rho is added mean power / background mean power.
# Compact additions can have much greater peak power.
```

Calibration tile IDs:

```python
DECEMBER_CALIBRATION_IDS = [
    0, 1, 10, 14, 15, 22,       # short/wide
    28, 31, 34, 36, 37, 43,    # long/narrow
]

JULY_CALIBRATION_IDS = [
    0, 6, 10, 12, 16, 19, 24, 27, 34, 41, 42, 46
]
```

Audit training used:

```text
Per calibration tile:
  3 families × 3 rho values [.03, .3, 1]
  added to every recording
  plus zero and target/reference-swapped zero contrasts

D_short_wide: 66 null-training trials
D_long_narrow: 66
J_intensity: 132
Total: 264

Training seeds:
  seed32 + 500000 + 1000*family_index + j
  family_index: burst=0, linked=1, gaps=2
  j: index within the stratum's calibration-tile list
```

A further 240 controls used different pattern seeds:

```text
For each dataset and family:
  12 target-only trials at rho=.03
  12 target-only trials at rho=.3
  12 shared trials at rho=.3

Plus:
  12 zero-addition trials per dataset

Control seeds:
  seed32 + 600000 + 1000*family_index + j

Calibration backgrounds are reused.
These are different inserted patterns, not independent sky realizations.
```

Expected measurement views:

```python
EXPECTED_VIEWS = {
    "burst": ["FLAME", "THUNDER"],
    "linked": ["BRIDE"],
    "gaps": ["SHADOW", "SILENCE", "TS", "ST"],
}
```

Selected control results, each out of 12 target-only insertions:

| Dataset | Family | Added mean fraction | Pooled expected-view flags | Per-view expected-view flags | Per-view primary flags |
|---|---|---:|---:|---:|---:|
| December | Burst | .03 | 10 | 12 | 8 |
| December | Burst | .3 | 12 | 12 | 8 |
| December | Linked | .03 | 0 | 2 | 0 |
| December | Linked | .3 | 3 | 11 | 10 |
| December | Gaps | .03 | 1 | 1 | 1 |
| December | Gaps | .3 | 6 | 12 | 12 |
| July | Burst | .03 | 12 | 12 | 10 |
| July | Burst | .3 | 12 | 12 | 10 |
| July | Linked | .03 | 0 | 11 | 11 |
| July | Linked | .3 | 0 | 12 | 12 |
| July | Gaps | .03 | 0 | 12 | 12 |
| July | Gaps | .3 | 12 | 12 | 12 |

“Expected-view flag” means one of the designated measurement views passed. It does not mean exact injection coordinates or a message were recovered.

For the per-view rule:

```text
Shared-pattern primary flags: 0 / 72
Shared-pattern all-view flags: 3 / 72
Zero-addition primary flags: 0 / 24
```

These finite, dependent controls do not establish a universal false-alarm guarantee. The difference between expected-view recovery and primary recovery measures the cost of the random routing.

**The current sky-result counts and validation state are:**

| Dataset/cohort | Tiles | Original primary flags | Pooled-rule flags | Per-view-rule flags |
|---|---:|---:|---:|---:|
| December target | 24 | 5 | 0 | 1 |
| December reserved | 12 | 0 | 0 | 0 |
| July target | 24 | 2 | 0 | 0 |
| July reserved | 12 | 2 | 0 | 0 |

The one retained primary is the old D19/BRIDE fluctuation. Its fixed relation does not repeat.

Recorded implementation checks:

```text
Original voltage decoding:
  6 source archives hash-verified
  612 source blocks hash-verified
  612 Parseval checks
  maximum relative Parseval error: 1.023e-7
  36 independent inverse-sample checks
  maximum absolute inverse error: 5.274e-9
  RF sign/gain checks passed at both resolutions

July acquisition:
  36 bitwise comparisons against native HDF5 slice reads
  data and masks included
  149435988 payload bytes fetched
  conservative payload-plus-metadata count: 160970324 bytes
  acquisition cap: 192 MiB

Measurement checks:
  direct rectangle means verified
  MIRROR winning overlap independently summed
  INVERSION time reversal preserved magnitude and reversed sign

Retrospective audit:
  648 legacy intensity-view score/cutoff/flag rules reproduced exactly
  103 frozen source files unchanged
  6 control configurations independently replayed with exact score matches
```

For further development, retain the numerical ranges of each measurement, separate primary routing from exploratory inspection, and test the same relation across recordings rather than comparing independently selected maxima. A fresh sky test should freeze the chosen reference rule before scoring its targets.

**End of handoff.**