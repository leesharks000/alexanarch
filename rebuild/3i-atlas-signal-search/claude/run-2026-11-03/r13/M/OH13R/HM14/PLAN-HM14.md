# PLAN-HM14 — the Parkes pattern against false drifts

23 November 2026. Frozen before any product of this plan exists (FROZEN-HM14.sha256, committed before the run). The operator, 14:20: "lets run them".

## The question

HM7 found the twelve Green Bank coordinates' mean S−R contrast D positive at Parkes in all three sessions (0.107, 0.125, 0.330; family p 0.074, 0.311, 0.026 against random draws of controls), and C09 above all its own controls in all three. Controls in HM7 sit at fixed offsets on the comet's own drift. At Green Bank, windows tracked along any drift ran high in ON against OFF (HM6: false mean 0.44), and the comet fell into the false cohorts once they were read on the same tracks (HM8). This plan reads the Parkes pattern against cohorts on false drifts, the test HM8 gave Green Bank.

## Data

HM7's kept products, hm7_<session>_<scan>.npz: for each of 84 windows (12 candidates, 72 controls) and each 15 s integration, the ±2.5 kHz strip (2,501 channels, 2 Hz) aligned on the comet track. No network. Only the three S/R pairs of each session are used, as in HM7.

## Cohorts

381 cohorts: the comet (Δd = 0) and 380 false drifts Δd drawn once, numpy default_rng(20261123), |Δd| uniform in 0.02–0.20 Hz/s, sign ±1 with equal probability. The same 380 values are used in every session. A cohort re-tracks every window by shifting integration k by round(Δd·(t_k − t_ref)/Δν) channels, t_ref the mean mid-time of the session's six scans, Δν the channel width. Over a session's ~1,800 s the largest shift is about 100 channels.

## Statistic

As HM7: each row divided by its median; S(j) the sum over integrations of channels j−1..j+1; Z of S(0) against S(j) for 30 ≤ |j| ≤ 999 and more than 30 channels from every other window's centre ((S(0) − median)/(1.4826·MAD)); per window D = mean Z over the three S scans − mean Z over the three R scans. The reference range is ±999 channels in place of HM7's ±1249, so that every shift stays inside the strip; the comet cohort is computed the same way.

- family(c, s) = mean D over the twelve candidates not flagged dc by HM7, in session s, cohort c.
- C09(c, s) = D of C09.
- Combined(c) = mean over the three sessions of (family(c, s) − mean of the 380 false)/sd of the 380 false.

## Gate

Before any cohort: the comet cohort computed with HM7's own reference range (±1249) must reproduce HM7's stored D for all twelve candidates in all three sessions to 1e-3. If not, nothing else is written.

## Rule

The Parkes pattern survives only if the comet cohort's family ranks in the top 5% (rank ≤ 19 of 381) in at least two of three sessions **and** its Combined ranks ≤ 4 of 381 (top 1%). Otherwise it is the drifting-window property and retires. C09 is read under the same rule on its own D, and reported.

A survivor goes to a request for another session on the comet; it is not a claim.
