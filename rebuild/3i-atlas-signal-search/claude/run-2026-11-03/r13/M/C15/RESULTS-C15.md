# RESULTS-C15: the cc15 hit is an image of the cc14 burst

Plan: PLAN-C15.md, frozen before any product (PLAN-C15.sha256). Products: z.json and v_0013.npz … v_0018.npz.

## 1. Uncapped z (z.json)

ON0013 z 14.53 at both predictions (3 of 100 false stacks reach it in the window). Every other scan is below z 2.8 at both predictions, at levels false stacks also reach (OFF0016 2.1 at the comet prediction, 29 false stacks; ON0017 2.3 fixed, 7; OFF0018 2.7 fixed, 1).

## 2. The voltages

1. In cc15 the wide view (5.72 kHz) exceeds 1.5× its median only in ON0013, at frames 664 and 665: the same two frames as the cc14 burst (RESULTS-C14 §2). No other scan has a frame above 1.3×.
2. Frame 664 holds a narrow peak at the predicted bin: 17.3× (feed X) and 42.8× (feed Y). The rest of the view is near noise: median group 1.1× and 1.2×. Frame 665: peak 1.2× and 2.0×, view 1.2× and 1.5×.
3. Against cc14 in frame 664, the peak is 0.0075 (X) and 0.0094 (Y) of cc14's peak, about −21 dB in both feeds. The broad part, which stands at 15–28× across cc14's view, is near absent in cc15. The cc15/cc14 ratio across the view runs from 0.008 at the peak to 0.03–0.40 elsewhere: not flat.

## 3. Reading, by the plan's fixed rule

Rule 1 holds: cc15's excess is only at frames 664–665 of ON0013, so the event is shared. Its shape is a narrow peak at the same bin, at a nearly fixed fraction of cc14's peak in both feeds (−21 dB), without cc14's broad part. The plan reads that as an instrumental image, not a burst wider than 2.9 MHz. The cc15 nomination is closed as an image of the cc14 burst.

What it adds to RESULTS-C14: the burst's broad part is confined to cc14 (it does not spill into cc15 at that level), and its peak, at 1645.270 MHz, is strong enough to print a −21 dB image at the same position one coarse channel down. An image of that kind is a property of the receiver chain. Its mechanism (the channelizer, the sampler, or a mixing product) is not established here. Its coordinate (the same fine-bin position in the adjacent channel) is recorded as a known image path for strong signals.
