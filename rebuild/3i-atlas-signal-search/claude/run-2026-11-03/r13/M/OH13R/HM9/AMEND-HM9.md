# AMEND-HM9: stage 1 read, no amendment

Written 22 November 2026 after hm9_stage1.json (ON 0013, OFF 0014) was read, and before stage 2 is run. PLAN-HM9 §3.5 allows any structure seen in stage 1 that no reading names to be frozen here as a test for the hold-out.

**None is frozen.** What stage 1 shows is all within readings H1–H4 already name:

- **H4 at C04 passes in ON 0013 and not in OFF 0014.**
  - Its leading eigenvalue at lag 0 is 1.648. Its sidebands' highest is 1.617, and none of the 200 surrogates reaches it. In OFF 0014 the value is 1.617, below its sidebands' 1.636.
  - Its form is diffuse. The share is 0.36 in X and 0.64 in Y, and the largest single element carries 0.074 of it (Y+15), spread over both feeds and the whole ±16 bins.
  - The value sits at the edge expected from noise for 66 elements over 833 frames, (1 + √(66/833))² ≈ 1.64, and inside the range of the scan's other sidebands (up to 1.666 at C06's).
  - By §3.1–3.3 it goes to the hold-out with its form held fixed.
- **H3, X, comes nearest among the readings that do not pass.** The mean correlation among C08–C11 is 0.034 raw and 0.049 differenced. In 10,000 random four-sets of sidebands, 144 and 39 were as high (p ≈ 0.014 and 0.004), against the rule's 0. In OFF 0014 the same values are −0.001 and 0.000 (p ≈ 0.5), and in Y −0.03. H3 is computed on the hold-out in stage 2 as on every scan, so its values there are reported under the same reading. No new test is needed.
- No H1 or H2 value at any comet coordinate in ON 0013 has p below 0.04. The sidebands' base rate at p < 1e-4 is 0 of 84 for H1, H2X and H2Y in both scans.

Stage 2 runs hm9.py unchanged (its hash is in FROZEN-HM9.sha256).
