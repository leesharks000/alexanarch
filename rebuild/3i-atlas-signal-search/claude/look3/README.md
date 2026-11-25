# look3 — two searches of 2026-11-25 (plans frozen and hashed before any count)

1. Off the comet (PLAN-look3-1.md, sha256 97b62b17…). MeerKAT hit lists, 157 64-beam scans. Single-beam off-target hits at the comet's drift: 109 against a false-drift median of 114; rank 23 of 41. Null.
2. The Wow's frequency fixed in the Sun's frame, at Parkes (PLAN-look3-2.md, sha256 89f844ca…). Jul 31 and Sep 12 complete, all four readings null (ranks 7, 16, 25, 15 of 41). Oct 5 not reached: the process was stopped by the container before that session wrote. To be rerun.

The full MeerKAT hit array (hits.npy, about 1 GB) is not committed; stream.py rebuilds it in about a minute.
