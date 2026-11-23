# PLAN-HM13-B2b, amendment 1 (before run 2)

Run 1 of B2b (streams of 09:14–09:25 EST) is void. hm13b2b.py stored the per-frame windows as float16, whose largest value is 65,504. Per-bin powers here run to about 10⁶, so 72.6% of the stored values overflowed to inf (checked in b2b_0013.npz). Every peak-over-median ratio was then inf/inf, every frame read as off, and the reader returned duty 0 for all 21 events. That was the storage failing, not a measurement. Run 1's products are hashed in B2b-RUN1-VOID.sha256 and its json and logs kept in b2b_run1_void/; the npz files are deleted.

The one change: the windows are stored as float32 (`W=Wn`). Nothing else in the plan, the rule or the code changes. Hashes of the amended code in FROZEN-HM13-B2b-AMEND-1.sha256, committed before run 2.

A second error in the frozen plan, recorded here: rule 1 says 20,000 simulated noise frames gave "none" above 12. The simulation run just before the freeze gave 1 (5 × 10⁻⁵). The bound "below 10⁻⁴" holds.
