# Full-cadence voltage pass v1

16 November 2026, America/New_York. Authorized by the user's "lets proceed", carried forward after compute returned. This amends the completed first-pass PLAN.md without changing it. Same GBT observations, not an independent observing epoch. Existing total-power spectra and three sampled windows per scan have already been inspected.

## Fixed acquisition and validation

Acquire coarse channel 7 for all 1,676 blocks in each of scans 0013–0018: 10,056 blocks, 21,088,960,512 voltage bytes, about 299.932 seconds per scan. Reuse saved first-pass blocks. Verify HTTP byte ranges, header geometry, per-block PKTIDX, source sizes and SHA256s. Retrieve headers alongside payloads. Complete header progression, recorded tracking and drop diagnostics are part of the result. Decode with the validated rawspec signed-int8 normalization and FFT orientation. Reproduce the three independent fine-reference rows and conserve Parseval energy. No numerical or gap failure is silently filled or treated as a physical null.

## Primary measurement

C03 is the primary previously selected coordinate, rest 1665633776.6172388 Hz. The other twelve original coordinates are descriptive secondary measurements. Preserve the original candidate table. No per-scan frequency maximization. Use saved GBT ephemeris and exact native times. Reconstruct total and separate receiver-polarization fine powers, both at individual 0.357913941-second FFTs and at the inherited 17-FFT integrations. Compare comet-tracked and receiver-fixed paths. Receiver anchor for C03 is inherited 1665644304.702512 Hz. Keep 100 local frequency controls at C03 rest offsets +/-1 through +/-50 kHz; apply the same processing to each control. Original known interference complex around 1665.615 MHz is an explicit positive processing control. Uncalibrated X/Y differences are not sky polarization.

Primary full-scan line-power summaries use the inherited physical Gaussian template (rest sigma 1.6763806343 Hz), including exposure averaging, with the previously defined local-background exclusion and control normalization where the retained frequency support permits exact reuse. Fixed receiver and comet summaries are both reported. The old tolerance-dependent detector result is preserved separately.

## Phase-sensitive exploratory extension

Retain a phase-preserving narrow-band stream for C03 and its 100 frequency controls, plus the twelve secondary coordinates, from contiguous FFT subbands. Use a fixed receiver-frequency center for each subband over all scans. A 256-bin subband gives about 715.256 complex samples/second and approximately +/-357.6 Hz bandwidth. Validate its modulation, time and frequency conventions with numerical tone injections before source interpretation. Include the full observed Doppler displacement within each selected band.

For C03 and controls compare matched comet Doppler phase with a receiver-fixed phase model. Do not phase-connect separate ON/OFF scans. Within each scan measure coherent powers using fixed non-overlapping lengths of 1,4,16,64 native FFT frames (0.3579,1.4317,5.7266,22.9065 seconds). Use the same finite residual-frequency bank for target and controls: -8 through +8 Hz, spacing 1/(64 native FFT durations). Maxima over that bank/length family are explicitly multiple-trial exploratory quantities, not a new single-bin significance. Report each control's family maximum, ON/OFF behavior and failures. A coherent null is conditional on coherence and phase-model assumptions. No readable content or emitter identity is inferred from raw availability.

Inject equal-complex-amplitude tones, single-polarization and shared-polarization, at C03 and a fixed subset of ten control coordinates. Include zero-amplitude identity and test frequency orientation, conserved power, phase continuity across raw blocks and FFT boundaries, and recovery at fixed strength steps. Injection scale is in measured receiver-power units; no new calibrated EIRP bound is claimed. If reconstruction validation fails, report the failure and stop phase interpretation rather than tune on the candidate.

## Retention and scope

Save acquisition ledgers/hashes, native channel payloads or scientifically sufficient phase-preserving extracts, decoder/analysis code, checks, controls, injections and results. Save completed acquisition stages before long follow-ups. Report unread or incomplete blocks as incomplete work. Preserve existing findings and raw evidence. No external email, public deposit or automation is authorized or needed. This plan is saved before new full-cadence source powers or phase statistics are decoded.