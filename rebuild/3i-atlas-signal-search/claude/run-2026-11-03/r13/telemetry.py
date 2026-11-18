"""PLAN-r13 part A: per-block pointing from the GUPPI raw headers of blc23 scans 0013-0018 (metadata only).
Every 4th block of file 0000, every 32nd block after. Writes telemetry.json."""
import json, urllib.request, concurrent.futures as CF
SC = {"0013": "17226", "0014": "17543", "0015": "17861", "0016": "18179", "0017": "18497", "0018": "18814"}
B = "https://bldata.berkeley.edu/ATLAS/GB_ATLAS_raw/blc23_guppi_61027_{}_DIAG_3I_ATLAS_{}.{:04d}.raw"
S = 7168 + 134217728; NB = 1676
def hd(a):
    sc, g = a; f, b = divmod(g, 128); o = b * S
    for t in range(4):
        try:
            h = urllib.request.urlopen(urllib.request.Request(B.format(SC[sc], sc, f), headers={"Range": f"bytes={o}-{o + 6799}"}), timeout=60).read().decode("ascii", "replace")
            c = {h[i:i + 8].strip(): h[i + 9:i + 80].strip().strip("'").strip() for i in range(0, len(h), 80)}
            return sc, g, {k: c.get(k) for k in ("RA", "DEC", "AZ", "ZA", "TRK_MODE", "PKTIDX", "STT_IMJD", "STT_SMJD", "STT_OFFS", "TBIN", "PIPERBLK", "DAQPULSE")}
        except Exception as e: err = str(e)
    return sc, g, {"error": err}
jobs = [(sc, g) for sc in SC for g in sorted(set(list(range(0, 128, 4)) + list(range(128, NB, 32)) + [NB - 1]))]
with CF.ThreadPoolExecutor(8) as ex: R = list(ex.map(hd, jobs))
out = {}
for sc, g, d in R: out.setdefault(sc, {})[g] = d
json.dump(out, open("telemetry.json", "w"), indent=0); print(len(R), sum("error" in d for _, _, d in R))
