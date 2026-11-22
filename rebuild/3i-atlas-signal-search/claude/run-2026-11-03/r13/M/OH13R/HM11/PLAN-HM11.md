# PLAN-HM11: the conditions as characters

Frozen 22 November 2026, before any HM11 statistic is computed, at the author's word (16:58 EST): "and keep the rh experiments." It follows the proposal of 16:46: carry one move from the Riemann proof into the search.

**The move.** The proof extracts its signal with a signed combination of four character channels, Re(G₀ + G_ψ − G_χ − G_χψ). The signs cancel everything except the term wanted, and every other channel becomes part of the error budget. The search's controls have the same structure. They are three binary conditions:
- scan (ON +1, OFF −1);
- feed (X +1, Y −1);
- track (the comet's drift c +1, the mirrored drift f −1).

Their eight sign patterns are the characters of the group of conditions. Every account of the excess predicts its own character. Projecting each cohort onto all eight at once gives each account its own channel, read against the 379 false cohorts on the same channel.

**What each account predicts, stated now.**

| account | characters it predicts |
|---|---|
| a comet-borne source seen by both feeds | s·t (ON − OFF on the comet's drift but not the mirror), with s and t |
| a comet-borne source polarized along X | s·p·t as well |
| the X chain in ON acting on drifting windows, either direction | s·p and s, not t |
| a drift-direction effect of the session (HM6 item 4: false cohorts biased on c, not f) | s·t in the false cohorts too, so in their mean, not in the comet's rank |
| a feature fixed at the dish | the contrast outside the cube: (ON − OFF) on d minus the mean of c and f |

**Data.**
- The kept cohort products, read without recomputation: HM6's for 0013/0014 and HM8's for 0015–0018. Each holds per-scan power (P) and D3 for 11,452 windows (380 cohorts, each with 11 coordinates and their sidebands) on tracks c, d and f, in X and Y.
- These products were read before, at cohort level per track, by HM6 and HM8. The characters below have not been computed. The code check printed one number, a reproduction of an existing figure (HM8's first-pair X power on track c, 1.093), and nothing else.

## 1. The statistic

- Per scan, measure, feed and track, each coordinate's rank among its sidebands (as HM6 and HM8), centred at 0.
- Per pair (0013/0014, 0015/0016, 0017/0018), per coordinate, the eight characters are the mean over the eight cells (scan × feed × track c/f) of the centred rank times the character's sign. The cohort score is the mean over its coordinates × √n, as HM6.
- **Pooled** is the sum of the three pairs' scores over √3.
- The comet's rank among the 380 is reported in both directions, for every character, pair, measure (P and D3) and the dish contrast.

## 2. Rule

- **The comet's character stands out** if, pooled, the comet cohort ranks first of 380, above every false cohort, on s·t or on s·p·t, in P or in D3. That is four statistics, at p ≤ 1/380 each.
- Every other character is reported, not ruled. The false cohorts' mean on each character is the session's own bias on that channel, reported beside the comet's rank.
- The per-pair ranks are reported. The first pair is known from HM6 to carry the strongest contrast, so a pooled result is read with its per-pair breakdown.

## 3. What a result means, stated now

- s·t or s·p·t standing out says the comet's coordinates carry the comet's own sign pattern beyond what any false cohort shows.
- Neither standing out, with the false cohorts' mean carrying s·t or s·p, says the excess is the session's channel bias, read in its proper character.
- None of this is meaning by itself, and none of it, alone, separates a sender from a natural or instrumental cause.

## 4. What stays fixed

No other character, rank method, cohort set or threshold, and nothing tuned after the score. Failing a frozen test bars nothing.

FROZEN-HM11.sha256 hashes this plan and hm11.py.
