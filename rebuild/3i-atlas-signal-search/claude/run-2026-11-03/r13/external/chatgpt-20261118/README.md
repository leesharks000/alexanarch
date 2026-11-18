# Two ChatGPT reports on the 3I/ATLAS voltages, 18 November 2026

Received from the author on 18 November 2026 (17:09 EST), as attachments. The author, 17:13: "chatgpt, yup". Kept verbatim, as received. The evidence bundles they describe (results/, PLAN.md, code, the saved subband archives) were not received with them and are not here.

- **REPORT-reading-the-original-thirteen.md.** The thirteen original coordinates read as filtered complex voltages from six saved subband products, each with 113 coordinates, two feeds and 214,528 samples per feed. The 113 coordinates match this investigation's delaymod set: C01–C13 plus K±01–50. Result: 0/13 pass its replication screen; C02 is a moving filter crossing a fixed receiver-frequency line complex near 1665.615 MHz; C03–C13 are noise-like; first-two-second power sits 0.8–2.8% above mid-scan in ON and OFF scans alike.
- **REPORT-what-the-boundary-search-can-recover.md.** Injected packets ("ATLAS TEST NN": on/off keying, BPSK, and intermittent keying absent from ON0015) were added to copies of the measured backgrounds. A joint amplitude and phase screen recovers what the earlier all-three-ON clock rule misses: at 0.30 of filtered background power, 12/12 of each family against 0/12 BPSK and 0/12 intermittent under the old rule. Nothing at 0.03 or below. Zero nominations in the measured C03–C13. One false nomination in twelve ON-and-OFF controls.

## Checked against this investigation

- **Agrees with r13 (RESULTS-r13.md):** the thirteen fall to the null once the scan starts are cut.
- **Header modes.** Its tracking states match telemetry.json: UNKNOWN then TRACK in 0013, 0014 and 0017; TRACK from the first header in 0015, 0016 and 0018.
- **Open check.** r13's V2 cut drops rows in 0015 (0–1), 0016 (0–2) and 0018 (0), whose headers already read TRACK. V2's criterion therefore included pointing offsets beyond the TRK_MODE flag. That must be stated exactly before the V2 null is cited.
- **For part K.** K1 also requires all three ON scans and would miss a transmitter absent from one of them; K2 and K3 are per scan. The boundary report's intermittent family is the test K lacks.
