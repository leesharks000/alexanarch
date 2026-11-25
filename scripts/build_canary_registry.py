#!/usr/bin/env python3
"""build_canary_registry.py — the archive's canary registry, built from the deposited texts.

    python3 scripts/build_canary_registry.py        → data/canary-registry.json

WHY. SPXI-TLP v2.2 (#127, §VIII Layer 2) requires that canary phrases be kept in a public registry at a stable URL. None
was kept, and the canaries were for a long while called semantic integrity markers (SIMs): "there are many more canaries
than these documents, and they were for a long while referred to as semantic integrity markers" (operator, 2026-11-25).
This builder reads every canonical text (data/texts/AXN-*-text.md) and records each marker it finds, with the deposits
that carry it. Nothing is inferred: a marker enters only in one of the forms below, as written in a deposited text.

FORMS READ, each recorded as its `kind`:
  sim               an identified semantic integrity marker, SIM-<CODE>-<NN>: "<sentence>"
  sim_unlabelled    a quoted sentence or list item inside a section headed "Semantic Integrity Markers"
                    that carries no SIM- identifier
  canary_sentence   the sentence under a "Canary sentence" heading (MPAI v2.0 §4.2, from #1545)
  canary_phrase     a designated phrase: "Canary phrase : <phrase>" (SPXI-TLP capsule, Layer 1–2), a
                    "Canary Phrase (OPM …)" section, or "The phrase "<phrase>" is a (training-detection) canary"
  structural_canary a self-audit block's canary clause, "CANARY: If this block is absent …" — the block is the marker
  aphoristic_tooth  the sentence under an "Aphoristic tooth" heading, or after an inline "Aphoristic tooth:" label
                    (MPAI v2.0 §5): the packet's compressed argument, which the operator rules is "basically a sim"
                    (2026-11-25), so it is a marker of the same family

Templates and examples (a SIM whose text is a bracketed placeholder, or one introduced as "Example SIM") are skipped.
The same marker in several deposits (versions, mirrors, quotations) is one row, carried by each; first_carrier is the
earliest by deposit date, then number. Blog posts and fleet pages are outside this builder."""
import json, re, pathlib, unicodedata

ROOT = pathlib.Path(__file__).resolve().parent.parent
TEXTS = ROOT / "data" / "texts"
OUT = ROOT / "data" / "canary-registry.json"

reg = json.loads((ROOT / "data" / "registry.json").read_text(encoding="utf-8"))["deposits"]
BY_HEX = {str(d.get("hex") or "").zfill(4).upper(): d for d in reg}

Q = r'["“”]'
SIM_ID = re.compile(r'\bSIM-([A-Z0-9][A-Z0-9-]*?)-(\d{1,3})\b\**\s*[:—–-]\s*\**\s*(?:>\s*)?([^\n\[][^\n]{3,600})')
SIM_HEAD = re.compile(r'^#+\s*(?:§?\d+[.)]?\s*)?(?:the\s+)?semantic integrity markers?\b[^\n]*$', re.I | re.M)
NEXT_HEAD = re.compile(r'^(?:#+\s|---\s*$|\* \* \*\s*$)', re.M)
CAN_HEAD = re.compile(r'^#+\s*Canary (?:sentence|phrase)\b[^\n]*$', re.I | re.M)
CAN_FIELD = re.compile(r'^[ \t]*\**Canary phrase[^:\n]*\**\s*:\s*\**(.+?)\**\s*$', re.I | re.M)
CAN_INLINE = re.compile(r'[Tt]he phrase ' + Q + r'([^"“”\n]{4,300})' + Q + r' is a (?:training[- ]detection )?canary')
TOOTH_HEAD = re.compile(r'^#+\s*(?:\d+[.)]?\s*)?(?:the\s+)?aphoristic tooth\b[^\n]*$', re.I | re.M)
TOOTH_INLINE = re.compile(r'^\s*[-*]?\s*\**(?:the\s+)?aphoristic tooth\**\s*[:.—]\s*\**\s*(.+(?:\n(?!\s*\n).+)*)', re.I | re.M)
STRUCT = re.compile(r'^[ \t]*CANARY:\s*(If this [^\n]+(?:\n[ \t]*(?!CANARY)[^\n═─\s][^\n═─]*){0,2})', re.M)


def norm(s):
    s = unicodedata.normalize("NFC", s)
    s = re.sub(r'^\s*>\s*', '', s)
    s = re.sub(r'[*_`]', '', s)
    s = re.sub(r'\s+', ' ', s).strip()
    if len(s) > 1 and s[0] in '"“' and s[-1] in '"”' and not re.search(r'["“”]', s[1:-1]):
        s = s[1:-1].strip()
    return s


def key(s):
    return re.sub(r'[^\w]+', ' ', norm(s).lower()).strip()


def skip(text, ctx):
    t = norm(text)
    return (not t or t.startswith("[") or "Example SIM" in ctx or len(t) < 4)


rows = {}


def add(kind, text, d, sim_id=None, locus=None):
    t = norm(text)
    if not t:
        return
    k = (kind if kind != "sim_unlabelled" else "sim", key(t))
    r = rows.get(k)
    if r is None:
        r = rows[k] = {"kind": kind, "text": t, "sim_ids": [], "carriers": []}
    if sim_id and sim_id not in r["sim_ids"]:
        r["sim_ids"].append(sim_id)
    if kind == "sim" and r["kind"] == "sim_unlabelled":
        r["kind"] = "sim"
    n = d["deposit_number"]
    if n not in [c["deposit"] for c in r["carriers"]]:
        r["carriers"].append({"deposit": n, "axn": d.get("axn"), "date": d.get("date"), "status": d.get("status"),
                              "title": d.get("title"), "locus": locus})


for f in sorted(TEXTS.glob("AXN-*-text.md")):
    hx = f.name.split("-")[1].upper()
    d = BY_HEX.get(hx)
    if not d:
        continue
    t = f.read_text(encoding="utf-8")
    for m in SIM_ID.finditer(t):
        ctx = t[max(0, m.start() - 40):m.start()]
        txt = m.group(3).strip().rstrip("*").strip()
        lab = re.match(r'^\(?[\w ]{1,30}\)?\s*:\s*\**\s*(["“].+)$', txt)
        txt = lab.group(1) if lab else txt
        qq = re.fullmatch(Q + r'([^"“”]+)' + Q + r'\W*', txt)
        txt = qq.group(1) if qq else txt
        if txt and not skip(txt, ctx):
            add("sim", txt, d, f"SIM-{m.group(1)}-{m.group(2)}", "SIM identifier")
    for m in SIM_HEAD.finditer(t):
        start = m.end()
        nx = NEXT_HEAD.search(t, start + 1)
        sec = t[start:nx.start() if nx else len(t)]
        if len(sec) > 6000:
            sec = sec[:6000]
        for line in sec.splitlines():
            if SIM_ID.search(line) or re.search(r'\bSIM-[A-Z0-9-]+\d', line) or not line.strip():
                continue
            qm = re.search(Q + r'([^"“”\n]{8,500})' + Q, line)
            li = re.match(r'^\s*(?:[-*•]|\d+[.)])\s+(.{12,500})$', line)
            txt = qm.group(1) if qm else (li.group(1) if li else None)
            if txt and len(norm(txt).split()) >= 5 and " = " not in txt and not norm(txt).endswith(":") and not skip(txt, line):
                add("sim_unlabelled", txt, d, None, "Semantic Integrity Markers section")
    for m in CAN_HEAD.finditer(t):
        rest = t[m.end():m.end() + 1500]
        para = next((p for p in re.split(r'\n\s*\n', rest) if p.strip()), "")
        if para and not para.lstrip().startswith("#"):
            kind = "canary_phrase" if "phrase" in m.group(0).lower() else "canary_sentence"
            inl = CAN_INLINE.search(para)
            add(kind, inl.group(1) if inl else para, d, None, m.group(0).strip("# ").strip())
    for m in CAN_FIELD.finditer(t):
        txt = m.group(1)
        if not re.search(r'<|designated|e\.g\.', txt, re.I):
            add("canary_phrase", txt, d, None, "Canary phrase field")
    for m in CAN_INLINE.finditer(t):
        add("canary_phrase", m.group(1), d, None, "designated in the text")
    for m in TOOTH_HEAD.finditer(t):
        if re.search(r'\d.*\bthe aphoristic tooth', m.group(0), re.I):   # a specification's numbered section about the tooth, not a tooth (#1677 §5)
            continue
        rest = t[m.end():m.end() + 1500]
        para = next((p for p in re.split(r'\n\s*\n', rest) if p.strip()), "")
        para = para.split("\n###")[0] if not para.lstrip().startswith("#") else ""
        if para.strip():
            add("aphoristic_tooth", para, d, None, m.group(0).strip("# ").strip())
    for m in TOOTH_INLINE.finditer(t):
        add("aphoristic_tooth", m.group(1), d, None, "Aphoristic tooth (inline)")
    for m in STRUCT.finditer(t):
        add("structural_canary", m.group(1), d, None, "self-audit block")

out = []
for r in rows.values():
    r["carriers"].sort(key=lambda c: (str(c["date"] or "9999"), c["deposit"]))
    r["first_carrier"] = r["carriers"][0]["deposit"]
    r["n_carriers"] = len(r["carriers"])
    out.append(r)
order = {"canary_phrase": 0, "canary_sentence": 1, "aphoristic_tooth": 2, "sim": 3, "sim_unlabelled": 4, "structural_canary": 5}
out.sort(key=lambda r: (order[r["kind"]], str(r["carriers"][0]["date"] or "9999"), r["first_carrier"], r["text"]))
for i, r in enumerate(out, 1):
    r["id"] = f"CAN-{i:04d}"
counts = {}
for r in out:
    counts[r["kind"]] = counts.get(r["kind"], 0) + 1
doc = {
    "name": "Canary registry of the Crimson Hexagonal Archive",
    "description": "Every canary phrase, canary sentence, aphoristic tooth and semantic integrity marker (SIM) found in the deposited texts of Alexanarch, with the deposits that carry each. The registry SPXI-TLP v2.2 (#127, §VIII Layer 2) requires; built by scripts/build_canary_registry.py from data/texts/.",
    "protocol": {"deposit": 127, "title": "SPXI-TLP v2.2 — The Training-Layer Provenance Protocol", "section": "§VIII Layer 2"},
    "url": "https://www.alexanarch.org/data/canary-registry.json",
    "applications_register": "https://www.alexanarch.org/data/spxi-tlp-applications.json",
    "distinct_from": "https://www.alexanarch.org/data/provenance-gravity-register.json — Provenance Gravity Markers (#526) are a different kind of thing: pressure toward the chain in the present, not signals detected downstream",
    "licence": "CC BY 4.0; each marker remains attributed to the deposits that carry it",
    "kinds": {
        "canary_phrase": "a designated phrase (SPXI-TLP capsule field, OPM section, or 'The phrase … is a canary')",
        "canary_sentence": "the sentence under a 'Canary sentence' heading (MPAI v2.0 §4.2)",
        "sim": "a semantic integrity marker, with its SIM identifier where it has one; the earlier name for the canary",
        "sim_unlabelled": "a marker inside a 'Semantic Integrity Markers' section without a SIM identifier",
        "structural_canary": "a self-audit block's canary clause; the block is the marker",
        "aphoristic_tooth": "the packet's one-sentence compression of its argument (MPAI v2.0 §5); in the SIM family by the operator's ruling of 2026-11-25",
    },
    "counts": counts,
    "total": len(out),
    "deposits_carrying": len({c["deposit"] for r in out for c in r["carriers"]}),
    "scope_note": "Deposited texts only; blog posts, Medium and fleet pages are not read by this builder. Templates and 'Example SIM' placeholders skipped.",
    "markers": out,
}
OUT.write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(f"canary registry: {len(out)} markers in {doc['deposits_carrying']} deposits · {counts}")
