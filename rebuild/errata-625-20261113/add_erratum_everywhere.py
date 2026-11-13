"""2026-11-13 14:59 EST, the operator: "lets add that note everywhere the phrase appears." The erratum entered on #625 and #902 is entered on every
record that gives *ei exestin* / εἰ ἔξεστιν as the Greek of the Slavonic Josephus or quotes a finding that does. Records whose text is itself the
correction are left as they stand, because the note would contradict nothing in them: #1761, #1763, #1764, #1765 (The Word That Became Text v2.x, which
withdraw the phrase), #1762 (The Crossing of Names, which traces it to Whiston), #3 (a capture reporting that correction), and #626, which already
carries the erratum ('unattested quotation'). Each locus is the section heading over the occurrences.   python3 add_erratum_everywhere.py"""
import json, pathlib, re
ROOT = pathlib.Path(__file__).resolve().parents[2]; P = ROOT / "data/registry.json"
reg = json.loads(P.read_text(encoding="utf-8")); D = {d["deposit_number"]: d for d in reg["deposits"]}
BASE = next(e for e in D[625]["errata"] if e["kind"] == "reconstruction given as attested text")
PAT = re.compile(r"(?i)ei exestin|εἰ ἔξεστιν")
KIND = {1755: "quoted finding rests on a reconstruction", 1757: "quoted finding rests on a reconstruction",
        1458: "reconstruction: attested forms supplied", 1468: "reconstruction: attested forms supplied"}
TARGETS = [56, 65, 639, 969, 970, 971, 978, 1101, 1176, 1458, 1468, 1755, 1757]
SKIP = [3, 626, 1761, 1762, 1763, 1764, 1765]
done = []
for n in TARGETS:
    t = (ROOT / D[n]["full_text_path"].lstrip("/")).read_text(encoding="utf-8")
    occ = [m.start() for m in PAT.finditer(t)]; assert occ, n
    heads = [(m.start(), m.group(1).strip()) for m in re.finditer(r"(?m)^#{1,4} (.+)$", t)]
    loci = []
    for o in occ:
        h = [x for x in heads if x[0] < o]
        name = h[-1][1] if h else "front matter"
        if name not in loci: loci.append(name)
    body_occ = [o for o in occ if not t[t.rfind("\n", 0, o) + 1:o].lstrip().startswith("#")]
    first = (body_occ or occ)[0]; s = t.rfind("\n", 0, first) + 1; e = t.find("\n", first); line = re.sub(r"\s+", " ", t[s:e if e > 0 else len(t)]).strip()
    i = line.lower().find("ei exestin") if "ei exestin" in line.lower() else line.find("εἰ ἔξεστιν")
    snip = line[max(0, i - 120):i + 120].strip()
    k = KIND.get(n, BASE["kind"])
    E = dict(BASE, kind=k, locus="; ".join(loci[:6]) + (f" (and {len(loci) - 6} more)" if len(loci) > 6 else "") + f" — {len(occ)} occurrence(s)",
             was=("'" + snip + "'" + (" — quoted as a finding of #625/#626/#1101" if n in (1755, 1757) else "")))
    if n in (1458, 1468):
        E["was"] = "'" + snip + "' — the phrase marked as a retroversion, without the attested forms"
    d = D[n]; d.setdefault("errata", [])
    d["errata"] = [x for x in d["errata"] if x.get("reason") != BASE["reason"]]
    d["errata"].append(E); done.append(n)
P.write_text(json.dumps(reg, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
print("entered", done, "skipped (text is the correction)", SKIP)
