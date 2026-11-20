# Verification of the ChatGPT handoff (Claude, 2026-11-19)

The handoff (HANDOFF-mandala-guided-2026-11-19.md) was received in thread from Lee Sharks at 20:00 EST, because the ChatGPT environment cannot download files. Its code blocks are extracted verbatim into views.py, consts.py, payload.py and recon.py. recon.py adds one line, `center_index = 63733`, which the RF-convention block uses without defining. Python 3.12.3, numpy 2.5.4, scipy 1.18.1.

1. **The D19 payload decodes to its stated hash.** The sha256 is e16488f0…6e86ca. The fixed-pair (groups 7, 15) correlations for scans 13–18 match the handoff's expected values to about 10⁻⁸.
2. **The blind-spot arithmetic recomputes from the stated scales.**
   - July BRIDE: the maximum possible contrast is 1/0.0548 = 18.249, against the pooled cutoff of 100.
   - July INVERSION: the maximum is 12.925, against 100.
   - December long/narrow BRIDE: the maximum is 13.213, against 20.
   - D19: the contrast is 2.894, against its per-view limit of 1.973.
3. **D19 reproduces from public voltages.** reconstruct_d19 was run live on GB_ATLAS_raw by bounded range reads, 16 MiB per scan. Every range came back as HTTP 206, and the first block's sha256 matched the handoff's for both scans.
   - Scan 13: BRIDE 0.42468361 (handoff 0.42468362), groups 7 and 15.
   - Scan 14: BRIDE 0.29514844 (handoff 0.29514843), groups 2 and 15.
   - The differences are at float32 precision.
4. **The rest is unrun here.** Scans 15–18, the additional-time window, the July branch and the controls were not rerun. Their numbers stand on the handoff's record.
5. **Read in M4b's terms.** D19's window centre, 1668.279 MHz, lies in coarse channel 7. M4b found no class-A event in cc07 (A 0, B 3 | control A 0, B 3). The handoff's own repeat test also fails: its fixed relation does not recur in the other ON scans.
