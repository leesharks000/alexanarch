# 3648–3688 MHz has public Parkes spectra

Metadata audit, 4 November 2026 (America/New_York). No signal powers were decoded or searched in this audit.

The quoted claim that 3648–3688 MHz has public data only from ATA July 3 is contradicted by the actual July 31 Parkes file headers. The public `blc27` source-pointing file contains the proposed strip. Two further nodes continue coverage to approximately 4032 MHz.

| July 31 Parkes node | First-channel frequency (MHz) | Channel increment (MHz) | Channels | Nominal span (MHz) |
|---|---:|---:|---:|---:|
| blc26 | 3648 | −0.000002 | 64,000,000 | 3520–3648 |
| blc27 | 3776 | −0.000002 | 64,000,000 | 3648–3776 |
| blc31 | 3904 | −0.000002 | 64,000,000 | 3776–3904 |
| blc32 | 4032 | −0.000002 | 64,000,000 | 3904–4032 |

These are on-source `3IATLAS_S` high spectral resolution files, with 2 Hz channels, 15-second sampling, one IF and 32-bit samples. The recorded file lengths accommodate 20 integrations per file. For example, the `blc27` channel centers are

`frequency[j] = 3776.0 − 0.000002*j MHz`, for `j = 0 … 63,999,999`.

The last center is 3648.000002 MHz. Nominal MHz endpoints in the table round the channel-center/edge convention; adjacent `blc26` supplies the immediate lower boundary.

## Scope and witnesses

I attempted one observed source file from each of the 26 node directories listed for July 31. Twenty-five headers were read and saved with their original 395-byte header, full source URL, HTTP range, parsed fields and SHA256. The `blc12` directory response supplied no matching source file link; that node remains unverified. This is not evidence that its data cannot exist elsewhere.

The verified nominal union is **704–1984 MHz and 2112–4032 MHz**. This audit therefore does not claim continuous verified Parkes coverage through the unresolved node. It does directly establish public recorded coverage of the proposed 3648–3688 MHz strip. Header presence and plausible payload length do not establish sensitivity, valid samples throughout a band or an already completed search.

The witness archive contains the raw headers, JSON records, aggregation and retrieval code, this note and a per-file SHA manifest. The verification uses the actual file links returned by public directory listings. Header reads requested only the first 4096 bytes; the parser stopped at `HEADER_END`, and only header bytes were retained. No bulk ATA download was started.

## Consequences for the proposed ranking

The coverage-first criterion improves my earlier ranking, which had not adequately joined all independent observing footprints. The particular replacement claim—an ATA-only 40 MHz gap—does not survive the Parkes headers.

If the prior Parkes reanalysis stopped at 3648 MHz, then 3648–3688 MHz may be a gap in that reanalysis. It is not the public Parkes archive's frequency ceiling. The distinction should be recorded explicitly. The July 3 ATA epoch remains valuable, and the Parkes July 31 epoch can supply an independent-instrument follow-up after ATA nominations are frozen. A July 31 null would not exclude a July 3 transient.

There is also a correction to the interference description. FCC 24-136, footnote 534, identifies 3600–3700 MHz as extended-C-band fixed-satellite service in the space-to-Earth direction. Calling the strip only ground-based LTE omits a relevant service category. Allocation is not a transmitter identification: this audit establishes no source for any interference on the observing night.

## Amendments before a new power search

1. Rebuild the usable-coverage map with date, actual header interval, resolution, sampling, flags/quality and search status as separate fields. Preserve the distinction between available data and analyzed data.
2. Use the signed `foff` for each file. Five of the verified Parkes nodes ascend in frequency and twenty descend; there is no single ordering for the whole Parkes dataset. Validate an injected physical comet-frame chirp through each reader and search before interpreting sign labels.
3. If proceeding with the 40 MHz strip, freeze the ATA nominations before inspecting the corresponding Parkes source powers. Convert frequencies with each telescope's observer ephemeris and preserve the different simultaneous-beam versus source/reference cadence.
4. Qualify the top of the ATA passband using calibration information where available and injection recovery at multiple positions. Noise comparison alone does not give a flux sensitivity; post-digitization injections do not measure frontend attenuation. Include source masks, chunk alignment and metadata overhead in the transfer estimate.
5. Record which scan/frequency cells the ongoing survey has already inspected before describing a half of the scans as untouched holdout data. Do not infer the survey's 64-channel completion from a clock estimate.

This audit does not rerun the original ATA pipeline or establish its full drift-sign convention. The May 2026 paper still documents a positive 0.05–1.5 Hz/s retained range; end-to-end sign tests and a header-coverage audit are separate pieces of evidence. Existing completed CH and 2694–2696 MHz results are unchanged.

## Primary sources

- [Parkes July 31 directory](https://bldata.berkeley.edu/ATLAS/PKS_Jul_31_2025/)
- [blc27 source file](https://bldata.berkeley.edu/ATLAS/PKS_Jul_31_2025/blc27/guppi_60887_50760_6690867462_3IATLAS_S_0001.0000.fil)
- [blc31 directory](https://bldata.berkeley.edu/ATLAS/PKS_Jul_31_2025/blc31/)
- [blc32 directory](https://bldata.berkeley.edu/ATLAS/PKS_Jul_31_2025/blc32/)
- [Breakthrough Listen campaign and data description](https://seti.berkeley.edu/atlas/)
- [FCC 24-136, footnote 534](https://docs.fcc.gov/public/attachments/FCC-24-136A1.pdf)
- [ATA paper, accepted revision v2, §3.2](https://arxiv.org/html/2512.18142v2)
