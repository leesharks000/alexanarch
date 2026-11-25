#!/usr/bin/env python3
"""build_provenance_gravity_register.py — where Provenance Gravity Markers are applied, and what their tables say is at risk.

    python3 scripts/build_provenance_gravity_register.py        → data/provenance-gravity-register.json

WHY A SEPARATE REGISTER. Provenance Gravity Markers (#526, Lee Sharks, 2026-02-28) are "a different kind of thing" from
canaries and semantic integrity markers (operator, 2026-11-25). A canary is a signal to be detected downstream: if it comes
back, the text was read. A gravity marker is pressure on the reader in the present: it declares the document a node in a
chain and pulls the reader toward the chain's other nodes, naming their preservation state (anchored, preserved, recorded,
referenced, ghost) and their loss. So this register lists applications and the chains they declare; the canary registry
(data/canary-registry.json) lists the signals.

ELEMENTS READ (#526 §IV), each recorded where it appears in a deposited text:
  provenance_note       a **Provenance Note.** block (§IV.A)
  preservation_block    a **Preservation Gravity.** block or heading (§IV.D), with its Chain state and Source status lines
  source_status_table   a | Source | Location | Status | table (§IV.B); its rows are kept, so referenced and ghost sources
                        are listed by name
  inline_status_labels  inline "status: anchored|preserved|recorded|referenced|ghost" labels (§IV.B)
  inline_upstream       inline upstream markers, [upstream source exists] and the like (§IV.C)
  source_status_section a section headed "(WITH SOURCE STATUS)" or "Source Status", where a table survives as flattened lines
  provenance_gravity_section a section titled "Provenance Gravity" (the Space Ark's tier system, §VII there)
  declared              the text's own statement that it implements the markers
A deposit that names the protocol without carrying any element is listed under cites_only. A deposit dated before the protocol
(2026-02-28) that carries the same vocabulary (a status table in its states) is listed under precursors, not as an application.

The operator, 2026-09-07, recorded in #1605 §21: "provenance gravity markers was a good idea that i allowed to fall by the
wayside" — so the applications cluster at the protocol's founding, and the register shows where it stopped."""
import json, re, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "provenance-gravity-register.json"
reg = json.loads((ROOT / "data" / "registry.json").read_text(encoding="utf-8"))["deposits"]
BY_HEX = {str(d.get("hex") or "").zfill(4).upper(): d for d in reg}

NOTE = re.compile(r'\*\*Provenance Note\.?\*\*\s*(.+)', re.I)
BLOCK = re.compile(r'\*\*Preservation Gravity\.?\*\*|^#+\s*Preservation Gravity\b', re.I | re.M)
CHAIN = re.compile(r'\*\*Chain state:?\*\*\s*:?\s*([^\n]+)', re.I)
SSTAT = re.compile(r'\*\*Source status:?\*\*\s*:?\s*([^\n]+)', re.I)
TABLE = re.compile(r'^(\|[^\n]*\bStatus\b[^\n]*\|)[ \t]*\n\|[-:| ]+\|[ \t]*\n((?:\|[^\n]*\|[ \t]*\n?)+)', re.I | re.M)   # any table with a Status column (§IV.B)
DECLARED = re.compile(r'implements Provenance Gravity Markers[^\n.]*', re.I)
STATUS_SECTION = re.compile(r'^[^\n|]{0,80}\(WITH SOURCE STATUS\)[^\n]*$|^#+[^\n]*Source[- ]Status[^\n]*$', re.I | re.M)
PG_SECTION = re.compile(r'^(?:#+\s*)?(?:[IVXLC]+\.\s*|\d+\.\s*)?Provenance Gravity\b(?!\s+Markers)[^\n]*$', re.M)
INLINE_STATUS = re.compile(r'(?:—|\(|;)\s*\**\s*status:\s*\**\s*(anchored|preserved|recorded|referenced|ghost)\b[^)\n]{0,60}')   # the protocol's inline form, lower-case, in a parenthesis or after a dash (§IV.B); document status fields (Status: ANCHORED) are not labels
INLINE_UP = re.compile(r'\[(?:upstream source exists|derived from prior thread|this claim compresses a larger source object|preserve adjacent artifacts|[^\]\n]*upstream drafts? not[^\]\n]*|[^\]\n]*not independently (?:deposited|recoverable)[^\]\n]*)\]', re.I)
NAMES = re.compile(r'Provenance Gravity Marker', re.I)
STATES = ("anchored", "preserved", "recorded", "referenced", "ghost")


def cells(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


apps, cites, precursors = [], [], []
for f in sorted((ROOT / "data" / "texts").glob("AXN-*-text.md")):
    d = BY_HEX.get(f.name.split("-")[1].upper())
    if not d:
        continue
    t = f.read_text(encoding="utf-8")
    el = {}
    n = NOTE.search(t)
    if n:
        el["provenance_note"] = n.group(1).strip()[:600]
    if BLOCK.search(t):
        el["preservation_block"] = {"chain_state": [m.group(1).strip() for m in CHAIN.finditer(t)][:3],
                                    "source_status": [m.group(1).strip() for m in SSTAT.finditer(t)][:3]}
    rows = []
    for m in TABLE.finditer(t):
        head = [h.lower() for h in cells(m.group(1))]
        si = next(i for i, h in enumerate(head) if re.search(r'\bstatus\b', h))
        trows = []
        for line in m.group(2).strip().splitlines():
            c = cells(line)
            if len(c) > si:
                st = c[si].lower()
                trows.append({"source": c[0], "location": c[1] if si != 1 and len(c) > 1 else "", "status": c[si],
                              "notes": " · ".join(x for i, x in enumerate(c) if i not in (0, 1, si)),
                              "states": [s for s in STATES if re.search(r'\b' + s + r'\b', st)]})
        if any(r["states"] for r in trows):   # a status table in the protocol's vocabulary, not any table with a Status column
            rows.extend(trows)
    if rows:
        el["source_status_table"] = rows
    dc = DECLARED.search(t)
    if dc:
        el["declared"] = dc.group(0).strip()
    ss = [m.group(0).strip() for m in STATUS_SECTION.finditer(t)]
    if ss:
        el["source_status_section"] = ss[:5]
    pg = [m.group(0).strip() for m in PG_SECTION.finditer(t)]
    if pg:
        el["provenance_gravity_section"] = pg[:5]
    il = [m.group(0).strip() for m in INLINE_STATUS.finditer(t)] if str(d.get("date") or "") >= "2026-02-28" else []   # the protocol dates from #526
    if il:
        el["inline_status_labels"] = il[:40]
    iu = sorted({m.group(0) for m in INLINE_UP.finditer(t)})
    if iu:
        el["inline_upstream"] = iu[:40]
    if el and str(d.get("date") or "") < "2026-02-28":   # before the protocol: the same vocabulary, not yet the markers
        precursors.append({"deposit": d["deposit_number"], "axn": d.get("axn"), "date": d.get("date"), "title": d.get("title"), "elements": sorted(el)})
        continue
    meta = {"deposit": d["deposit_number"], "axn": d.get("axn"), "date": d.get("date"), "status": d.get("status"), "title": d.get("title")}
    if el:
        meta["elements"] = sorted(el)
        meta.update(el)
        apps.append(meta)
    elif NAMES.search(t):
        cites.append(meta)

apps.sort(key=lambda a: (str(a["date"]), a["deposit"]))
cites.sort(key=lambda a: (str(a["date"]), a["deposit"]))
at_risk = []
for a in apps:
    for r in a.get("source_status_table", []):
        if set(r["states"]) & {"referenced", "ghost", "recorded"}:
            at_risk.append({"deposit": a["deposit"], "source": r["source"], "location": r["location"], "status": r["status"], "notes": r["notes"]})
doc = {
    "name": "Provenance gravity register of the Crimson Hexagonal Archive",
    "description": "Deposits that carry Provenance Gravity Markers (#526), the elements each carries, the chain state and source status they declare, and every source their status tables list as recorded, referenced or ghost. Built by scripts/build_provenance_gravity_register.py from data/texts/.",
    "protocol": {"deposit": 526, "title": "Provenance Gravity Markers: A Protocol for Embedding Preservation Pressure in Documents", "date": "2026-02-28"},
    "url": "https://www.alexanarch.org/data/provenance-gravity-register.json",
    "distinct_from": "https://www.alexanarch.org/data/canary-registry.json — canaries and semantic integrity markers are signals to be detected downstream; gravity markers are pressure toward the chain in the present",
    "licence": "CC BY 4.0",
    "counts": {"applications": len(apps), "cites_only": len(cites), "precursors": len(precursors), "sources_at_risk": len(at_risk),
               "by_element": {k: sum(1 for a in apps if k in a["elements"]) for k in ("provenance_note", "preservation_block", "source_status_table", "source_status_section", "inline_status_labels", "inline_upstream", "provenance_gravity_section", "declared")}},
    "scope_note": "Deposited texts only; blog posts, Medium and fleet pages are not read by this builder.",
    "sources_at_risk": at_risk,
    "applications": apps,
    "cites_only": cites,
    "precursors": precursors,
}
OUT.write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(f"provenance gravity register: {len(apps)} applications, {len(cites)} cite only, {len(at_risk)} sources recorded/referenced/ghost · {doc['counts']['by_element']}")
