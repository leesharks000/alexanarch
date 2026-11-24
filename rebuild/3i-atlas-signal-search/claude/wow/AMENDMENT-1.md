# PLAN-WOW, amendment 1 (2026-11-24 ~03:20 UTC, after stage 1's first products)

Stage 1's controls were the Wow's values in random order and random six-value sequences. Any smooth transient (a satellite crossing a
sidelobe, a radar sweep) correlates better with a single rise-and-fall than with a jagged sequence, so beating those controls shows only
that the detections are smooth bumps, not that the Wow's particular profile instructs. Added, before reading it: 200 smooth controls,
each a sampled Gaussian on the same six steps with centre drawn from 1.5–3.5 and width from 0.6–2.5 samples, skewed by a factor from
0.6–1.6 on the falling side (the Wow itself is a rise to step 4 and a faster fall). The Wow's rank against these is the test of whether its
shape, among single-peaked shapes, picks out anything. Same data, same detection rule. Code: wow_s1b.py.
