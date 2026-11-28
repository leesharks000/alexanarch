#!/usr/bin/env python3
"""build_work_atom_set.py — build a work's PER atom set from its deposit record, automatically (2026-11-28).

Operator, 2026-11-28 13:39: "there is no reason atoms cant be created for works automatically, its highly repetitive and now there is a
350 record backlog"; 13:40: "the atoms could be created at time of a work's deposit, in anticipation of its search and scoring - i search
and score at least one capture for every new deposit"; 13:41: "that could just be standard deposit intake, so that dimensional scoring can
be standard capture intake".

The set is the 'work' template of rebuild/capture-registry/per-atoms/templates.json under PER-dim rubric v1.1 (EA-PER-RECALC-01, #1694, §3.4 and §3.9): twelve atoms,
PER-M author 3, title 3, date 1, claim boundary 2; PER-C framework 2, tradition 2, corpus 2; PER-D purpose 3, commitments 2, lineage 2, identifier 1, deposit chain 1. Every token,
reference and record quote is taken from the deposit's registry entry; every quote is checked at its locus by per_backlog.quote_ok before
anything is written (Measurement Sovereignty, #1530 §2.3). Where the record does not state an atom, the atom is 'unknown': not scored,
listed as the record's gap, never charged to a composition (templates.json, applicability).

  author         creator of record, each name in both orders                                  quote: the creator field
  title          the title, its main clause, the document id in its parentheses                quote: the title
  date           the record's date, ISO and written                                            quote: the date
  claim boundary the Falsification Conditions the deposit states                               quote: their first sentence     else unknown
  framework      the line and journal the record is placed in                                  quote: those fields             else unknown
  tradition      the genre the record names, its content type                                  quote: the content type         else unknown
  corpus         the archive's name as the record gives it                                     quote: that name                else unknown
  purpose        the opening of the description                                                quote: its first sentence
  commitments    the licence and the substrate disclosure                                      quote: both
  lineage        the records the deposit names as related, by number and main title           quote: each '#N' the record prints   else unknown
  identifier     #N, AXN:HEX, DOIs                                                             quote: the AXN
  deposit chain  the version and the versions it supersedes                                    quote: the version              else unknown

The three reading atoms (claim boundary, purpose, commitments) take the sources proposed in session on 2026-11-28 and continued by the
operator at 14:26 ("lets continue"). A set built here is marked state 'deposit intake (automatic, rubric v1.1)'; a reader may later replace
a reference with a closer one, as a versioned change. A deposit that already has a set (any set whose records name it) is left alone.

    python3 scripts/build_work_atom_set.py 1810 1812            # print, verify, do not write
    python3 scripts/build_work_atom_set.py 1810 1812 --merge    # verify and append to data/per-atom-sets.json
    python3 scripts/build_work_atom_set.py --backlog --merge    # every deposit a pending capture names as its work
"""
import datetime, json, pathlib, re, sys
ROOT = pathlib.Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "scripts"))
import per_backlog as PB
PS = ROOT / "data/per-atom-sets.json"; CAP = ROOT / "data/EA-WG-CAPTURES-01.json"
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
ARCHIVE_NAMES = ["Crimson Hexagonal Archive", "Alexanarch", "alexanarch.org"]
W = {"author": ("M", 3, "role"), "title": ("M", 3, "token"), "date": ("M", 1, "token"), "claim boundary": ("M", 2, "reading"), "framework": ("C", 2, "token"),
     "tradition": ("C", 2, "reading"),
     "corpus": ("C", 2, "token"), "purpose": ("D", 3, "reading"), "commitments": ("D", 2, "reading"), "lineage": ("D", 2, "role"), "identifier": ("D", 1, "role"),
     "deposit chain": ("D", 1, "role")}

def first_sentence(s, cap=260):
    s = re.sub(r"\s+", " ", str(s or "")).strip()
    m = re.search(r"^(.{20,%d}?[.!?])(?=\s|$)" % cap, s)
    if m: return m.group(1)
    return s if len(s) <= cap else s[:cap].rsplit(" ", 1)[0]

def names(creator):
    out = []
    for part in re.split(r";", str(creator or "")):
        part = re.sub(r"\([^)]*\)", "", part).strip(" .,")
        if not part: continue
        m = re.fullmatch(r"([^,]+), (.+)", part)
        out += [f"{m.group(2).strip()} {m.group(1).strip()}", part] if m else [part]
    return list(dict.fromkeys(out))

def main_title(t):
    t = re.sub(r"\s*\([^)]*\)\s*$", "", str(t)).strip()
    return re.split(r":| — | – ", t, 1)[0].strip()

def slug_of(d):
    s = re.sub(r"[^a-z0-9]+", "-", main_title(d["title"]).lower()).strip("-")[:48].strip("-")
    return f"dep-{d['deposit_number']}-{s}"

def build(d, reg):
    n = d["deposit_number"]; loc = f"data/registry.json #{n}"; atoms = []; gaps = []
    def add(atom, tokens, reference, quotes):
        dim, w, kind = W[atom]; ev = [{"record_quote": q, "locus": loc} for q in quotes if q and PB.quote_ok(q, loc)]
        app = "required" if ev else "unknown"
        if not ev: gaps.append(atom)
        atoms.append({"atom": atom, "dim": dim, "weight": w, "kind": kind, "applicability": app, "tokens": [t for t in dict.fromkeys(tokens) if t], "reference": reference, "evidence": ev})
    nm = names(d.get("creator"))
    add("author", nm, " and ".join(nm[0::2]) if nm else None, [d.get("creator")])
    doc = re.findall(r"\(([A-Z]{2,}[A-Z0-9-]*-\d+[A-Za-z0-9-]*)[^)]*\)", d["title"])
    add("title", [main_title(d["title"]), d["title"]] + doc, None, [d["title"]])
    iso = str(d.get("date") or "")[:10]; wr = []
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", iso):
        y, m, dd = iso.split("-"); wr = [f"{int(dd)} {MONTHS[int(m)-1]} {y}", f"{MONTHS[int(m)-1]} {int(dd)}, {y}"]
    add("date", [iso] + wr, None, [iso])
    fc = d.get("falsification_conditions")
    add("claim boundary", [], re.sub(r"\s+", " ", str(fc)).strip()[:600] if fc else None, [first_sentence(fc)] if fc else [])
    fw = [str(d.get(k)) for k in ("line", "journal") if d.get(k) and isinstance(d.get(k), str)]
    # Where line and journal are empty the framework is UNKNOWN. A journal named inside the content type was tried as the framework on
    # 2026-11-28 and set aside the same day: the readers' sets give frameworks as programmes and series (Semantic Economy, Machine-Mediated
    # Reception Studies), and a journal no composition names would be charged as an erasure on the builder's guess.
    add("framework", fw, None, fw)
    ct = str(d.get("content_type") or "").strip()   # the genre the record names (EA-PER-RECALC-01 §3.4; the existing work sets quote content_type for it)
    add("tradition", [], ct or None, [ct] if ct else [])
    blob = PB.N(" ‖ ".join(PB.strings(d)))
    add("corpus", ARCHIVE_NAMES, None, [a for a in ARCHIVE_NAMES if PB.N(a) in blob][:1])
    desc = re.sub(r"\s+", " ", str(d.get("description") or "")).strip()
    while desc:   # a description often opens by repeating the title in capitals: that sentence states no purpose and is passed over
        fs = first_sentence(desc)
        if fs and fs.upper() == fs and len(desc) > len(fs) + 20: desc = desc[len(fs):].strip()
        else: break
    add("purpose", [], first_sentence(desc, 420) if desc else None, [first_sentence(desc)] if desc else [])
    lic, sub = d.get("license"), d.get("substrate")
    add("commitments", [], "; ".join(x for x in [f"licence {lic}" if lic else "", ("substrate disclosure: " + first_sentence(sub, 300)) if sub else ""] if x) or None,
        [q for q in [lic, first_sentence(sub) if sub else None] if q])
    rel = [int(x) for x in (d.get("related_deposits") or []) if str(x).isdigit()]
    if not rel:   # the record names its relations in prose only (related_identifiers_raw, related_ids): take the numbers it prints, its own excluded
        rel = [int(x) for x in dict.fromkeys(re.findall(r"#(\d{1,4})\b", " ".join(str(d.get(k) or "") for k in ("related_identifiers_raw", "related_ids")))) if int(x) != n]
    printed = [f"#{x}" for x in rel if re.search(r"#%d\b" % x, " ".join(s for s in PB.strings(d)))]
    by = {x["deposit_number"]: x for x in reg}
    ltok = []
    for x in rel[:24]:
        ltok += [f"#{x}"] + ([main_title(by[x]["title"])] if x in by else [])
    add("lineage", ltok, ", ".join(f"{main_title(by[x]['title'])} (#{x})" for x in rel[:24] if x in by) or None, printed[:6])
    dois = [z for z in (d.get("zenodo_dois") or []) if isinstance(z, str)]
    add("identifier", [f"#{n}", f"AXN:{d['hex']}", f"deposit {n}", d["hex"]] + dois, None, [d["axn"]])
    ver = str(d.get("version") or ""); prior = [h.get("from_version") for h in d.get("reissue_history") or [] if h.get("from_version")]
    vt = re.findall(r"v\d+(?:\.\d+)+", ver) + prior
    add("deposit chain", vt, None, [ver] if ver else [])
    return {"new": slug_of(d), "name": d["title"], "template": "work", "external": False,
            "type_basis": f"The defining record's content_type is {d.get('content_type')!r}: read on the work template. Built automatically from the deposit record.",
            "records": [{"deposit": n, "title_quote": d["title"]}], "atoms": atoms,
            "notes": "Built automatically at deposit intake from the registry entry of #%d (scripts/build_work_atom_set.py). %s" % (n, ("Not stated by the record, so unknown and not scored: " + ", ".join(gaps) + ".") if gaps else "Every atom is stated by the record.")}, gaps

def have(sets):
    return {r.get("deposit") for e in sets["entities"] for r in (e.get("records") or []) if isinstance(r, dict)}

def backlog_targets():
    E = json.loads(CAP.read_text(encoding="utf-8"))["entries"]; out = []
    for e in E:
        if e.get("per_dim") or not e.get("per_dim_pending"): continue
        if (e.get("originator") or {}).get("entity_type") != "work": continue
        m = re.search(r"#(\d{1,4})\b", str(e.get("q") or "")); n = int(m.group(1)) if m else ((e.get("related_deposits") or [None])[0])
        if n: out.append(int(n))
    return sorted(set(out))

def main(argv):
    reg = json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8"))["deposits"]; by = {d["deposit_number"]: d for d in reg}
    sets = json.loads(PS.read_text(encoding="utf-8")); got = have(sets)
    nums = backlog_targets() if "--backlog" in argv else [int(a) for a in argv if a.isdigit()]
    if "--refresh" in argv:   # rebuild, in place, the sets this script built itself (a change to the builder); sets made by readers are never touched
        mine = [e for e in sets["entities"] if str(e.get("state", "")).startswith("deposit intake (automatic")]; k = 0
        for e in mine:
            n = e["records"][0]["deposit"]; s, gaps = build(by[n], reg)
            if s["atoms"] != e["atoms"]:
                e["atoms"] = s["atoms"]; e["required"] = [a["atom"] for a in s["atoms"] if a["applicability"] == "required"]; e["notes"] = s["notes"]; k += 1
        print(f"refreshed {k} of {len(mine)} automatic sets")
        if "--merge" in argv:
            PS.write_text(json.dumps(sets, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        return 0
    today = datetime.date.today().isoformat(); made = []; skipped = []; missing = []
    for n in nums:
        if n not in by: missing.append(n); continue
        if n in got: skipped.append(n); continue
        if re.search(r"dataset", str(by[n].get("content_type") or ""), re.I) and "--force" not in argv:
            print(f"#{n}: content_type {by[n].get('content_type')!r} is a dataset, not read on the work template; left alone (--force to build anyway)"); continue
        s, gaps = build(by[n], reg); req = [a["atom"] for a in s["atoms"] if a["applicability"] == "required"]
        made.append((n, s, gaps))
        print(f"#{n} TGT-{s['new']}: {len(req)} required, unknown {gaps or 'none'}")
    print(f"built {len(made)}; already had a set {len(skipped)} {skipped[:12]}; not in the registry {missing}")
    if "--merge" in argv and made:
        ids = {e["id"] for e in sets["entities"]}
        for n, s, gaps in made:
            sid = "TGT-" + s["new"]
            if sid in ids: continue
            sets["entities"].append({"id": sid, "name": s["name"], "template": "work", "type_basis": s["type_basis"], "records": s["records"], "atoms": s["atoms"],
                "required": [a["atom"] for a in s["atoms"] if a["applicability"] == "required"], "inversion_guidance": None, "notes": s["notes"], "external": False,
                "state": f"deposit intake (automatic, rubric v1.1) {today}", "state_d": f"deposit intake (automatic, rubric v1.1) {today}"})
        sets["count"] = len(sets["entities"]); sets["with_atom_set"] = sum(1 for e in sets["entities"] if e.get("atoms"))
        sets.setdefault("deposit_intake_pass", []).append({"date": today, "brief": "scripts/build_work_atom_set.py (automatic, from the registry entry)",
            "new_sets": ["TGT-" + s["new"] for _, s, _ in made], "checked_by": "per_backlog.quote_ok (every record quote at its locus before writing)"})
        PS.write_text(json.dumps(sets, ensure_ascii=False, indent=1) + "\n", encoding="utf-8"); print("merged into data/per-atom-sets.json:", len(made))
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
