#!/usr/bin/env python3
"""mret.py — Machine Retrieval Eligibility Test: an executable gate, not a description.

ORIGIN (2026-08-15). An external audit distinguished SCHEMA eligibility (the
archive defines the right fields) from POPULATED-RECORD eligibility (this
record, today, carries what an agent needs). The distinction is the defect
class the completeness gate was built for, generalized to retrieval. This
scorer makes it executable: every deposit, six axes, checkable properties
only, read-only over data/registry.json plus filesystem facts.

AXES (each averages its checks to 0..1):
  identity        axn + six-glyph checksum + hex + hash + title
  bibliography    creator + date + content_type + license + version
  description     non-trivial description + keywords
  machine_read    staged text file exists + body_status + data/records/<n>.json
  human_read      record page exists + wiki_article (the LLM tier)
  retrieval       retrieval_summary field present (the audit's item 3;
                  absence is a MEASURED BACKLOG, which is the point)
Supersession clarity is a cross-cutting check: a SUPERSEDED record must name
its successor, or identity is docked — a record that is retired without saying
so misleads every agent that retrieves it.

Deterministic: registry bytes in → identical report out (git supplies dating).
Writes datasets/mret/mret-report.json + mret-report.md. Mutates nothing else.
"""
import json, pathlib, statistics, collections

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUTD = ROOT / "datasets" / "mret"
EMOJI_MIN = 6  # six-glyph checksum


def score_one(d):
    n = d["deposit_number"]
    ax = {}
    emoji = d.get("emoji") or ""
    ax["identity"] = statistics.mean([
        bool(d.get("axn")), len(emoji) >= EMOJI_MIN or len(list(emoji)) >= 6,
        bool(d.get("hex")), bool(d.get("hash")), bool(d.get("title")),
        (d.get("status") != "SUPERSEDED") or bool(d.get("superseded_by_deposit_number")),
    ])
    ax["bibliography"] = statistics.mean([
        bool(d.get("creator")), bool(d.get("date")), bool(d.get("content_type")),
        bool(d.get("license")), bool(d.get("version")),
    ])
    desc = (d.get("description") or "").strip()
    kw = d.get("keywords") or []
    ax["description"] = statistics.mean([len(desc) >= 40, bool(kw)])
    ax["machine_read"] = statistics.mean([
        (ROOT / "data/texts" / f"AXN-{d['hex']}-text.md").exists(),
        bool(d.get("body_status")),
        (ROOT / "data/records" / f"{n}.json").exists(),
    ])
    ax["human_read"] = statistics.mean([
        (ROOT / "s/records" / str(n) / "index.html").exists(),
        bool((d.get("wiki_article") or "").strip()),
    ])
    ax["retrieval"] = 1.0 if (d.get("retrieval_summary") or "").strip() else 0.0
    return ax


def main():
    reg = json.loads((ROOT / "data/registry.json").read_text())
    OUTD.mkdir(parents=True, exist_ok=True)
    rows, axis_sums = [], collections.defaultdict(float)
    for d in reg["deposits"]:
        ax = score_one(d)
        total = round(statistics.mean(ax.values()), 4)
        for k, v in ax.items():
            axis_sums[k] += v
        rows.append({"n": d["deposit_number"], "axn": d["axn"], "mret": total,
                     **{k: round(v, 3) for k, v in ax.items()}})
    N = len(rows)
    rows.sort(key=lambda r: (r["mret"], r["n"]))
    dist = collections.Counter()
    for r in rows:
        dist["1.00" if r["mret"] == 1 else "0.90+" if r["mret"] >= .9 else
             "0.80+" if r["mret"] >= .8 else "0.70+" if r["mret"] >= .7 else "<0.70"] += 1
    report = {
        "instrument": "MRET v1.0 — Machine Retrieval Eligibility Test (executable gate)",
        "deposits": N,
        "mean": round(statistics.mean(r["mret"] for r in rows), 4),
        "median": round(statistics.median(r["mret"] for r in rows), 4),
        "distribution": dict(sorted(dist.items(), reverse=True)),
        "axis_fill": {k: round(v / N, 4) for k, v in sorted(axis_sums.items())},
        "note_on_retrieval_axis": ("retrieval_summary is a new field; its fill rate IS the backlog. "
                                   "Scoring absence, rather than not scoring, is what makes the "
                                   "backlog a measurement instead of a silence."),
        "worst_20": rows[:20],
        "records": rows,
    }
    (OUTD / "mret-report.json").write_text(json.dumps(report, indent=1, ensure_ascii=False) + "\n")
    md = ["# MRET v1.0 — distribution report", "",
          f"**{N} deposits.** Mean {report['mean']} · median {report['median']}.", "",
          "| band | records |", "|---|---|"]
    md += [f"| {k} | {v} |" for k, v in report["distribution"].items()]
    md += ["", "## Per-axis fill", "", "| axis | mean |", "|---|---|"]
    md += [f"| {k} | {v} |" for k, v in report["axis_fill"].items()]
    md += ["", report["note_on_retrieval_axis"], "",
           "## Lowest 20", "", "| # | MRET | weakest axes |", "|---|---|---|"]
    for r in rows[:20]:
        weak = ", ".join(k for k in ("identity", "bibliography", "description",
                                     "machine_read", "human_read", "retrieval") if r[k] < 1)
        md.append(f"| {r['n']} | {r['mret']} | {weak} |")
    (OUTD / "mret-report.md").write_text("\n".join(md) + "\n")
    print(f"MRET: {N} scored · mean {report['mean']} · median {report['median']}")
    for k, v in report["distribution"].items():
        print(f"  {k:<6} {v}")
    print("axis fill:", {k: v for k, v in report["axis_fill"].items()})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
