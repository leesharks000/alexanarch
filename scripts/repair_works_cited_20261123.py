#!/usr/bin/env python3
"""repair_works_cited_20261123.py — a standard References list added in place to recent papers that lacked one.

The author, 2026-11-23 20:40: "we have to keep standard works cited lists alongside axn citations - aggregators read
citations as authority. full stop. google scholar wont index without it. lets please look over recent deposits and see
whats been getting that or not." The audit of #1700–#1804 (scripts/check_works_cited.py, data/works-cited-ledger.json)
found papers giving their sources as prose, as footnotes or not at all. Adopted at 20:48: "adopted on all three, but
modified in place, not bumped to the top of the list."

Repair scope as ruled 2026-10-15 (broken, missing and mislabelled files and citations): the text keeps every word it
had; a section headed References is added at its end, in two parts:
  - the outside works the text cites, one per line in author-date form, read out of the text by readers who recorded,
    for each entry, the lines that cite it and a verbatim snippet (scratchpad refs/N.json, checked here: every snippet
    must occur on one of its lines);
  - the archive records the text cites as #N, each in the same form from the registry (creator, date, title, number,
    record URL).
Nothing is added that the text does not cite. Each record is rehashed with a new AXN at the same hex and family; the
prior AXN and hash are kept in axn_prior and works_cited_added; record_modification logs the change. The record's date
and its place in the registry are unchanged, so nothing moves on the front page or in the feed.

    python3 scripts/repair_works_cited_20261123.py REFS_DIR N [N ...] [--apply]"""
import hashlib, json, pathlib, re, sys
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import record_modification as rm
import references_lib as R
from axn_lib import axn_glyph_from_hash, axn_clusters_from_hash, axn_reading_from_clusters, compose_axn

ON = "2026-11-23"
RULING = ("Lee Sharks, 2026-11-23 20:40 ('we have to keep standard works cited lists alongside axn citations') and 20:48 "
          "('adopted on all three, but modified in place, not bumped to the top of the list')")
NOTE = ("*The works this text cites, set out as a standard list beside its record citations: first the outside works, then "
        "the records of the archive it cites by number. Added in place at the author's word; the text above is unchanged.*")
RECNUM = re.compile(r'(?<![\w&/#])#(\d{1,4})\b(?![\w-])')


def archive_entry(d):
    yr = str(d.get("date") or "")[:4] or "n.d."
    title = re.sub(r"\s+", " ", str(d.get("title") or "")).strip().rstrip(".")
    n = d["deposit_number"]
    return f'{d.get("creator") or "Crimson Hexagonal Archive"}. {yr}. *{title}*. Crimson Hexagonal Archive, #{n}. https://www.alexanarch.org/s/records/{n}/.'


def section(n, text, refs, reg):
    lines = text.split("\n")
    ext = []
    for e in refs["entries"]:
        ok = any(e["snippet"].strip()[:60] in lines[i - 1] for i in e["lines"] if 0 < i <= len(lines))
        if not ok:
            raise SystemExit(f"#{n}: snippet not found on its lines: {e['ref'][:80]} {e['lines']}")
        ext.append(e["ref"].strip())
    ext = sorted(dict.fromkeys(ext), key=lambda s: re.sub(r'^[\W_]+|^The ', '', s).lower())
    nums = sorted({int(m) for m in RECNUM.findall(text) if int(m) in reg and int(m) != n})
    arch = [archive_entry(reg[m]) for m in nums]
    parts = ["", "## References", "", NOTE, ""]
    if ext:
        parts += ["### Outside works", ""] + [f"- {x}" for x in ext] + [""]
    if arch:
        parts += ["### Archive records", ""] + [f"- {x}" for x in arch] + [""]
    return "\n".join(parts), len(ext), len(arch)


def main(argv):
    apply = "--apply" in argv
    args = [a for a in argv if a != "--apply"]
    refs_dir = pathlib.Path(args[0]); ns = [int(a) for a in args[1:]]
    reg_p = ROOT / "data/registry.json"; raw = reg_p.read_text(encoding="utf-8"); regj = json.loads(raw)
    reg = {d["deposit_number"]: d for d in regj["deposits"]}
    log = []
    for n in ns:
        d = reg[n]
        tp = ROOT / d["full_text_path"].lstrip("/")
        text = tp.read_text(encoding="utf-8")
        if "\n## References\n\n" + NOTE in text:
            print(f"#{n}: already repaired"); continue
        refs = json.loads((refs_dir / f"{n}.json").read_text(encoding="utf-8"))
        sec, ne, na = section(n, text, refs, reg)
        new = text.rstrip("\n") + "\n" + sec
        got = len(R.entries(new))
        print(f"#{n}: {ne} outside works, {na} records; standard-list entries read back: {got}")
        log.append({"n": n, "outside_works": ne, "records": na, "entries_read_back": got})
        if not apply:
            continue
        tp.write_text(new, encoding="utf-8")
        dp = ROOT / f"data/deposits/AXN-{d['hex']}.md"
        if dp.exists() and dp != tp:
            dt = dp.read_text(encoding="utf-8")
            if "\n## References\n\n" + NOTE not in dt:
                dp.write_text(dt.rstrip("\n") + "\n" + sec, encoding="utf-8")
        h = hashlib.sha256(new.encode("utf-8")).hexdigest(); g = axn_glyph_from_hash(h)
        before = {"axn": d["axn"], "hash": d["hash"]}
        d.setdefault("axn_prior", []).append({"axn": d["axn"], "hash": d["hash"], "until": ON,
                                              "why": "standard References list added in place (repair_works_cited_20261123.py)"})
        d["hash"] = h; d["axn_canonical"] = h; d["emoji"] = g
        d["axn"] = compose_axn(d["hex"], d.get("family", "ARCHIVAL"), g)
        d["clusters"] = axn_clusters_from_hash(h); d["reading"] = axn_reading_from_clusters(d["clusters"])
        if "axn_reading" in d: d["axn_reading"] = d["reading"]
        if "full_text_chars" in d: d["full_text_chars"] = len(new)
        if isinstance(d.get("body_status"), dict) and "residual_chars" in d["body_status"]:
            d["body_status"]["residual_chars"] = len(new)
        d["works_cited_added"] = {"on": ON, "outside_works": ne, "records": na, "hash_before": before["hash"],
                                  "axn_before": before["axn"], "ruled_by": RULING,
                                  "method": "outside works read from the text with line provenance; records from the text's #N citations and the registry"}
        rm.touch(d, "full_text", "standard References list added in place", was={"axn": before["axn"]}, now={"axn": d["axn"]}, when=ON)
        print(f"   applied: {before['axn']} -> {d['axn']}")
    if apply:
        indent = 2 if raw.startswith('{\n  "') else (1 if raw.startswith('{\n "') else None)
        s = json.dumps(regj, ensure_ascii=False, indent=indent) if indent else json.dumps(regj, ensure_ascii=False, separators=(",", ":"))
        reg_p.write_text(s + ("\n" if raw.endswith("\n") else ""), encoding="utf-8")
        mp = ROOT / "data/repair-maps/works-cited-2026-11-23.json"
        old = json.loads(mp.read_text(encoding="utf-8"))["records"] if mp.exists() else []
        keep = [r for r in old if r["n"] not in {x["n"] for x in log}]
        mp.write_text(json.dumps({"generated": ON, "ruling": RULING, "records": sorted(keep + log, key=lambda r: r["n"])},
                                 ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
