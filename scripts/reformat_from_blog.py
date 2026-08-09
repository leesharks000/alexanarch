#!/usr/bin/env python3
"""reformat_from_blog.py — restore lost structure from the authorial original.

THE DEFECT
122 of 181 records with a recorded blog source hold LESS structure than the post
they were recovered from. #1013 went from 99 headings, 13 tables, 233 list items
and 15 code blocks to 3 / 0 / 0 / 1. The bytes were right; the shape was thrown
away by whatever converter ran at recovery time.

Structure is not decoration in this corpus. A CSV export whose columns collapse
into prose stops being an export; a comparison table rendered as a run of pipe
characters stops being a comparison; a numbered protocol rendered as a paragraph
stops being executable.

THE GUARD, which is the whole reason this is a script and not a loop
Reformatting rewrites canonical text in bulk, so it must be impossible for this to
seat the WRONG work. Two conditions, both required:

  1. SAME-WORK: at least 80% of the seated body's own sentences must be present in
     the reconverted text. If the blog post has drifted, been rewritten, or is a
     different version, coverage collapses and the record is skipped.

  2. STRICTLY BETTER: the reconversion must add structure and must not lose more
     than 5% of the character count.

A record failing either is reported, not touched. Nothing is deleted: the prior
body is written to data/restoration-apparatus/ before replacement.

    python3 scripts/reformat_from_blog.py --dry-run
    python3 scripts/reformat_from_blog.py --apply --limit 20
"""
import argparse, hashlib, html, json, pathlib, re, sys, time, urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from restore_caesura import convert  # noqa: E402


def struct(md):
    return {"h": len(re.findall(r"^#+ ", md, re.M)),
            "tbl": md.count("|---"),
            "li": len(re.findall(r"^\s*(?:[-*]\s|\d+\.\s)", md, re.M)),
            "pre": md.count("```") // 2}


def sentences(t):
    t = re.sub(r"[#*`|>]", "", t)
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", re.sub(r"\s+", " ", t))
            if len(s.split()) >= 7]


def fetch_body(url):
    raw = urllib.request.urlopen(
        urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}),
        timeout=40).read().decode("utf-8", "replace")
    m = re.search(r"<div class=['\"]post-body[^>]*>(.*?)</div>\s*<div class=['\"]post-footer",
                  raw, re.S)
    return m.group(1) if m else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--only", type=int)
    a = ap.parse_args()
    if not (a.apply or a.dry_run):
        a.dry_run = True

    targets = json.loads(pathlib.Path("/tmp/fmtloss.json").read_text())
    if a.only:
        targets = [t for t in targets if t[0] == a.only]
    if a.limit:
        targets = targets[:a.limit]

    reg_p = ROOT / "data/registry.json"
    reg = json.loads(reg_p.read_text())
    D = {d["deposit_number"]: d for d in reg["deposits"]}
    store = ROOT / "data/restoration-apparatus"
    store.mkdir(exist_ok=True)

    applied, skipped = [], []
    for n, url, _loss in targets:
        d = D.get(n)
        if not d or not d.get("full_text_path"):
            continue
        fp = ROOT / d["full_text_path"].lstrip("/")
        old = fp.read_text(errors="replace")
        try:
            h = fetch_body(url)
        except Exception as e:
            skipped.append((n, f"fetch failed: {e}"))
            continue
        if not h:
            skipped.append((n, "no post-body in source"))
            continue
        new = convert(h)

        old_body = re.sub(r"^---.*?^---", "", old, flags=re.S | re.M)
        so, sn = struct(old_body), struct(new)
        gain = sum(max(0, sn[k] - so[k]) for k in so)
        if gain == 0:
            skipped.append((n, "reconversion adds no structure"))
            continue

        # GUARD 1 — same work
        sents = sentences(old_body)
        flat = re.sub(r"\s+", " ", re.sub(r"[#*`|>]", "", new)).lower()
        cov = (sum(1 for s in sents if s[:55].lower() in flat) / len(sents)) if sents else 0.0
        if sents and cov < 0.80:
            skipped.append((n, f"same-work guard: only {cov:.0%} of seated sentences "
                               f"present in the source — the post may be a different "
                               f"version or a different work"))
            continue
        # GUARD 2 — strictly better
        if len(new) < len(old_body) * 0.95:
            skipped.append((n, f"would lose {100 - len(new) * 100 // max(1, len(old_body))}% "
                               f"of the text"))
            continue

        print(f"  #{n:<6} h{so['h']}->{sn['h']} tbl{so['tbl']}->{sn['tbl']} "
              f"li{so['li']}->{sn['li']} pre{so['pre']}->{sn['pre']}  "
              f"cov {cov:.0%}  {len(old_body):,}c -> {len(new):,}c")
        if a.apply:
            hexid = d["axn"].split(":")[1].split(".")[0]
            f = store / f"{hexid}.json"
            rec = json.loads(f.read_text()) if f.exists() else {}
            rec.setdefault("lifted", []).append({
                "at": "2026-08-08",
                "reason": ("Body replaced by a structure-preserving reconversion of the same "
                           "authorial source. The prior text was correct in its words and had "
                           "lost its headings, tables, lists and code blocks at recovery time."),
                "text": old})
            f.write_text(json.dumps(rec, ensure_ascii=False, indent=1))
            fp.write_text(new)
            bs = d.setdefault("body_status", {})
            bs["work_sha256"] = hashlib.sha256(new.encode()).hexdigest()
            bs["structure_repair"] = {
                "at": "2026-08-08", "source": url,
                "was": f"{so['h']} headings, {so['tbl']} tables, {so['li']} list items, "
                       f"{so['pre']} code blocks",
                "now": f"{sn['h']} headings, {sn['tbl']} tables, {sn['li']} list items, "
                       f"{sn['pre']} code blocks",
                "same_work_coverage": round(cov, 3)}
            d.setdefault("record_modifications", []).append({
                "date": "2026-08-08", "field": "canonical_text",
                "note": (f"STRUCTURE RESTORED from the authorial source: {so['h']}/{so['tbl']}/"
                         f"{so['li']}/{so['pre']} headings/tables/list-items/code-blocks became "
                         f"{sn['h']}/{sn['tbl']}/{sn['li']}/{sn['pre']}. The words were already "
                         f"right; the shape had been discarded at recovery. Verified as the same "
                         f"work at {cov:.0%} sentence coverage before replacement.")})
            applied.append(n)
        time.sleep(0.15)

    if a.apply:
        reg_p.write_text(json.dumps(reg, ensure_ascii=False, indent=2))
    print(f"\n{'applied' if a.apply else 'dry run'}: {len(applied) if a.apply else '—'} changed · "
          f"{len(skipped)} skipped")
    for n, why in skipped[:14]:
        print(f"  skip #{n}: {why}")
    if a.apply:
        json.dump(applied, open("/tmp/reformatted.json", "w"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
