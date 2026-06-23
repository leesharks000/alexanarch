#!/usr/bin/env python3
"""
generate_observatory.py — render /observatory/ pages from /data/surface-weather/scans/*.json

Reads all scan-*.json files and produces static HTML for:
  - /observatory/index.html (hub)
  - /observatory/surface-weather/index.html (Surface Weather Station instrument)

Born static: scan summaries are baked into HTML at build time, no JS required for the core view.
Re-run this whenever a new scan lands in /data/surface-weather/scans/.
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime


SCANS_DIR = Path("data/surface-weather/scans")
OBSERVATORY_DIR = Path("observatory")
SURFACE_WEATHER_DIR = OBSERVATORY_DIR / "surface-weather"


SUBSTRATE_LABELS = {
    "chatgpt": "ChatGPT (OpenAI)",
    "claude": "Claude (Anthropic, Opus 4.7)",
    "kimi": "Kimi K2.6 (Moonshot AI)",
    "gemini": "Gemini (Google)",
    "deepseek": "DeepSeek (PRAXIS register)",
}


def load_scans():
    """Load all scan JSONs from data/surface-weather/scans/."""
    scans = []
    for path in sorted(SCANS_DIR.glob("scan-*.json")):
        with open(path) as f:
            data = json.load(f)
        data["_filename"] = path.name
        # Identify substrate from filename: scan-YYYY-MM-DD-{substrate}-NNN.json
        parts = path.stem.split("-")
        for key in SUBSTRATE_LABELS:
            if key in parts:
                data["_substrate_key"] = key
                data["_substrate_label"] = SUBSTRATE_LABELS[key]
                break
        else:
            data["_substrate_key"] = "unknown"
            data["_substrate_label"] = "Unknown substrate"
        scans.append(data)
    return scans


def render_summary_row(scan):
    """Single substrate summary row for the dashboard table."""
    sub = scan["_substrate_label"]
    completed = scan.get("scan_completed_utc", "?")
    methodology = scan.get("methodology_version", "?").split("/")[-1]
    aggs = scan.get("corpus_aggregates", scan.get("corpus_aggregates_observed_objects_only", {}))
    V = aggs.get("V_weighted_median", aggs.get("V_mean", "—"))
    A = aggs.get("A_weighted_median", aggs.get("A_mean", "—"))
    F = aggs.get("F_weighted_median", aggs.get("F_mean", "—"))
    C = aggs.get("C_weighted_median", aggs.get("C_mean", "—"))
    R_s = aggs.get("R_s_weighted_median", aggs.get("R_s_mean", "—"))
    SDI = aggs.get("SDI", "—")
    gov = scan.get("governance_state", scan.get("governance_state_v1.0_unspecified", "—"))
    if isinstance(gov, str) and "Not assigned" in gov:
        gov = "(v1.0 — not assigned)"
    scan_id = scan.get("scan_id", scan["_filename"])
    raw_url = f"/data/surface-weather/scans/{scan['_filename']}"

    def fmt(v):
        return f"{v:.2f}" if isinstance(v, (int, float)) else str(v)

    return f"""
<tr>
  <td style="padding:8px 6px;border-bottom:1px solid var(--border)"><strong>{sub}</strong><div style="font-size:.75em;color:#777">{methodology} · {completed[:10]}</div></td>
  <td style="padding:8px 6px;text-align:right;border-bottom:1px solid var(--border);font-family:var(--mono)">{fmt(V)}</td>
  <td style="padding:8px 6px;text-align:right;border-bottom:1px solid var(--border);font-family:var(--mono)">{fmt(A)}</td>
  <td style="padding:8px 6px;text-align:right;border-bottom:1px solid var(--border);font-family:var(--mono)">{fmt(F)}</td>
  <td style="padding:8px 6px;text-align:right;border-bottom:1px solid var(--border);font-family:var(--mono)">{fmt(C)}</td>
  <td style="padding:8px 6px;text-align:right;border-bottom:1px solid var(--border);font-family:var(--mono)">{fmt(R_s)}</td>
  <td style="padding:8px 6px;text-align:right;border-bottom:1px solid var(--border);font-family:var(--mono)">{fmt(SDI)}</td>
  <td style="padding:8px 6px;border-bottom:1px solid var(--border);font-size:.85em">{gov}</td>
  <td style="padding:8px 6px;border-bottom:1px solid var(--border);text-align:right"><a href="{raw_url}" style="font-size:.75em">JSON</a></td>
</tr>"""


def collect_object_matrix(scans):
    """Build a matrix object × substrate → V score for the cross-substrate divergence table."""
    objects = {}
    for scan in scans:
        sub_key = scan["_substrate_key"]
        for obs in scan.get("observations", []):
            obj_name = obs.get("object", "?")
            # Normalize: 'Lee Sharks / Crimson Hexagonal Archive' should match 'Lee Sharks'
            if "Lee Sharks" in obj_name:
                obj_norm = "Lee Sharks / Crimson Hexagonal Archive"
            elif obj_name in {"Crimson Hexagonal Archive"}:
                obj_norm = "Crimson Hexagonal Archive (standalone)"
            else:
                obj_norm = obj_name
            if obj_norm not in objects:
                objects[obj_norm] = {"object_class": obs.get("object_class", "?"), "scores": {}}
            V = obs.get("V")
            if obs.get("execution_status") == "not_executed":
                objects[obj_norm]["scores"][sub_key] = "—"
            elif V is None:
                objects[obj_norm]["scores"][sub_key] = "—"
            else:
                objects[obj_norm]["scores"][sub_key] = V
    return objects


def render_object_row(obj_name, obj_data, substrate_keys):
    cls = obj_data["object_class"].replace("_", " ")
    cells = []
    scores_numeric = []
    for sub in substrate_keys:
        v = obj_data["scores"].get(sub, "—")
        if isinstance(v, (int, float)):
            scores_numeric.append(v)
            # Color code by V
            color = "#0a7c6a" if v >= 0.75 else "#c47900" if v >= 0.25 else "#a02020"
            cell = f'<td style="padding:6px 6px;text-align:right;font-family:var(--mono);color:{color}">{v:.2f}</td>'
        else:
            cell = f'<td style="padding:6px 6px;text-align:right;color:#aaa;font-family:var(--mono)">—</td>'
        cells.append(cell)

    if scores_numeric:
        spread = max(scores_numeric) - min(scores_numeric)
        spread_cell = f'<td style="padding:6px 6px;text-align:right;font-family:var(--mono);color:{"#a02020" if spread >= 0.50 else "#c47900" if spread >= 0.25 else "#777"}">{spread:.2f}</td>'
    else:
        spread_cell = '<td style="padding:6px 6px;text-align:right;color:#aaa;font-family:var(--mono)">—</td>'

    return f"""
<tr>
  <td style="padding:6px 6px;border-bottom:1px solid #f0f0f0"><strong>{obj_name}</strong><div style="font-size:.7em;color:#999">{cls}</div></td>
  {''.join(cells)}
  {spread_cell}
</tr>"""


def render_curator_notes(scans):
    """Render any post_hoc_curator_context blocks present on scans."""
    blocks = []
    for scan in scans:
        ctx = scan.get("post_hoc_curator_context")
        if not ctx:
            continue
        sub = scan["_substrate_label"]
        added_by = ctx.get("added_by", "?")
        added_at = ctx.get("added_at", "?")
        purpose = ctx.get("purpose", "")
        notes = ctx.get("notes", [])

        notes_html = []
        for n in notes:
            if isinstance(n, dict):
                topic = n.get("topic", "")
                content = n.get("content", "")
                notes_html.append(
                    f'<div style="margin:8px 0 12px"><div style="font-weight:500;color:var(--accent);font-size:.9em">{topic}</div>'
                    f'<div style="font-size:.88em;margin-top:2px">{content}</div></div>'
                )
            else:
                notes_html.append(f'<div style="margin:6px 0;font-size:.88em">{n}</div>')

        blocks.append(f"""
<div style="background:#fff;border-left:3px solid var(--teal);padding:14px 18px;margin:14px 0">
<div style="font-size:.78em;color:#777;margin-bottom:4px">Curator context on <strong>{sub}</strong> scan · added by {added_by} · {added_at}</div>
<div style="font-size:.85em;color:#555;font-style:italic;margin-bottom:8px">{purpose}</div>
{''.join(notes_html)}
</div>""")
    return blocks


def render_surface_weather_page(scans):
    n_scans = len(scans)
    by_date_sub = sorted(scans, key=lambda s: (s.get("scan_completed_utc", ""), s["_substrate_key"]))

    # Order substrates left-to-right consistently
    substrate_order = ["chatgpt", "claude", "kimi", "gemini", "deepseek"]
    substrates_present = [s for s in substrate_order if any(scan["_substrate_key"] == s for scan in scans)]

    summary_rows = "".join(render_summary_row(s) for s in by_date_sub)

    # Object matrix
    object_matrix = collect_object_matrix(scans)
    obj_order = [
        # Institutional roots
        "Alexanarch",
        "Lee Sharks / Crimson Hexagonal Archive",
        "Crimson Hexagonal Archive (standalone)",
        "Semantic Economy Institute",
        # Mature concepts
        "Provenance Erasure Rate",
        "SPXI",
        "Writable Retrieval Basin",
        # Emerging
        "Semantic Commodity Form",
        "Revelation First",
        # Native controls
        "Zenodotus' Book-Burning",
        "I AM THE API",
        "Assembly Continuity Protocol",
        # Old battery / external controls
        "Feist Function",
        "New Alexanarch-native works (aggregate)",
        "DOI (Digital Object Identifier) — known-positive control",
        "Flurblex — known-negative control (coined non-existent term)",
        "PER (homonym) — confuser control",
    ]
    obj_rows = []
    for obj in obj_order:
        if obj in object_matrix:
            obj_rows.append(render_object_row(obj, object_matrix[obj], substrates_present))

    sub_header_cells = "".join(
        f'<th style="padding:8px 6px;text-align:right;font-weight:500;font-size:.8em;color:#555;border-bottom:2px solid var(--accent)">{SUBSTRATE_LABELS[s].split(" (")[0]}</th>'
        for s in substrates_present
    )

    # Compute headline divergences for the lede
    divergences = []
    for obj_name, obj_data in object_matrix.items():
        scores = [v for v in obj_data["scores"].values() if isinstance(v, (int, float))]
        if len(scores) >= 3 and (max(scores) - min(scores)) >= 0.50:
            divergences.append((obj_name, max(scores) - min(scores), scores))
    divergences.sort(key=lambda x: -x[1])
    divergence_lines = []
    for obj_name, spread, scores in divergences[:4]:
        divergence_lines.append(
            f"<li><strong>{obj_name}</strong>: V ranges {min(scores):.2f}–{max(scores):.2f} across substrates (spread {spread:.2f})</li>"
        )

    curator_blocks = render_curator_notes(scans)
    curator_section = ""
    if curator_blocks:
        curator_section = f"""
<h2>Curator context</h2>
<p class="subtle">Post-scan context added by the curator (MANUS) that reframes findings without mutating the as-performed observation data. Each block is additive to its source scan and is preserved in that scan's JSON file at <code>post_hoc_curator_context</code>.</p>
{''.join(curator_blocks)}
"""

    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Surface Weather Station — Alexanarch Observatory</title>
<meta name="description" content="The Surface Weather Station instrument: a weekly text-only scan battery measuring how the Alexanarch corpus appears in the public composition layer. Federated five-substrate baseline 2026-06-22–23.">
<script type="application/ld+json">{json.dumps({"@context": "https://schema.org", "@type": "Dataset", "@id": "https://alexanarch.org/observatory/surface-weather/", "name": "Surface Weather Station — Federated Cross-Substrate Baseline", "description": f"Visibility/anchor/figure/lift/breadth scores across {n_scans} substrate readings of the Alexanarch corpus on the public composition layer.", "creator": {"@type": "Person", "name": "Lee Sharks", "identifier": "https://orcid.org/0009-0000-1599-0703"}, "license": "https://creativecommons.org/licenses/by/4.0/", "dateModified": datetime.now().strftime("%Y-%m-%d")}, indent=None)}</script>
<style>@import url("https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap");
:root{{--bg:#fafafa;--fg:#1a1a1a;--accent:#1a3a5c;--teal:#0a7c6a;--border:#e0e0e0;--sans:"IBM Plex Sans",sans-serif;--mono:"IBM Plex Mono",monospace}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:var(--sans);background:var(--bg);color:var(--fg);line-height:1.6;font-size:15px}}
.wrap{{max-width:920px;margin:0 auto;padding:60px 24px}}
a{{color:var(--accent);text-decoration:none}}
a:hover{{background:#f8f8ff;text-decoration:underline}}
.nav{{display:flex;gap:12px;margin-bottom:20px;font-size:.85em;overflow-x:auto;white-space:nowrap}}
.nav a{{color:#777;font-weight:500}}
.nav a:hover{{color:var(--accent);background:none}}
.nav .current{{color:var(--accent)}}
h1{{font-size:1.4em;font-weight:600;color:var(--accent);margin-bottom:4px}}
h2{{font-size:1.05em;font-weight:600;color:var(--accent);margin-top:32px;margin-bottom:12px;border-bottom:1px solid var(--border);padding-bottom:4px}}
h3{{font-size:.95em;font-weight:600;color:var(--accent);margin-top:20px;margin-bottom:8px}}
table{{width:100%;border-collapse:collapse;font-size:.85em;margin:8px 0}}
th{{font-weight:500;color:#555;text-align:left;padding:8px 6px;border-bottom:2px solid var(--accent);font-size:.82em}}
.subtle{{color:#777;font-size:.88em}}
.callout{{background:#fff;border-left:3px solid var(--teal);padding:12px 16px;margin:12px 0;font-size:.92em}}
.footer{{margin-top:60px;padding-top:12px;border-top:1px solid var(--border);font-size:.75em;color:#777}}
ul,ol{{margin:8px 0 8px 24px}}
li{{margin-bottom:4px}}
code{{font-family:var(--mono);font-size:.85em;background:#f0f0f0;padding:1px 4px;border-radius:2px}}
.dashboard-table th:first-child{{text-align:left}}
.matrix-table{{font-size:.8em}}
.matrix-table th:first-child{{text-align:left}}
.legend{{display:flex;gap:16px;font-size:.8em;color:#777;margin-bottom:8px;flex-wrap:wrap}}
.legend span{{display:inline-flex;align-items:center;gap:4px}}
.legend .dot{{display:inline-block;width:10px;height:10px;border-radius:50%}}
</style>
</head><body><div class="wrap">
<nav class="nav">
<a href="/">Alexanarch</a>
<a href="/deposit/">Deposit</a>
<a href="/s/wiki/">Wiki</a>
<a href="/s/graph/">Graph</a>
<a href="/guide/">Guide</a>
<a href="/manifest/">Manifest</a>
<a href="/observatory/" class="current">Observatory</a>
</nav>

<div class="subtle"><a href="/observatory/">← Observatory</a></div>
<h1>Surface Weather Station</h1>
<div class="subtle" style="margin-bottom:8px">Federated cross-substrate baseline · {n_scans} readings · 2026-06-22 / 2026-06-23</div>

<p style="margin-top:16px">A weekly text-only scan battery measuring how the Alexanarch corpus appears in the public composition layer. Five signals per object — Visibility (V), Anchor Alignment (A), Figural Integrity (F), Compositional Lift (C), and Redundant Substrate Breadth (R<sub>s</sub>) — scored on a 5-point ordinal scale per the v1.1 methodology.</p>

<p style="margin-top:8px">This page is the <strong>federated baseline</strong>: each substrate's native retrieval stack produces its own reading. <strong>No consensus score is computed.</strong> Disagreement between substrates is itself a measurement of platform-level fragmentation, not noise to be averaged away.</p>

<div class="callout">
<strong>Methodology:</strong> <a href="/s/records/882/">EA-MMRS-SURFACE-VISIBILITY-01 v1.1 (#882)</a> · <code>AXN:037E.EMPIRICAL.🚩♦️⏹️🔃❌🗡️</code><br>
<strong>Raw scan data:</strong> <a href="/data/surface-weather/scans/">/data/surface-weather/scans/</a> (5 JSON files, machine-legible)<br>
<strong>v1.0 baseline deposit:</strong> <a href="/s/records/881/">#881</a> (ChatGPT-substrate, pre-cleanup) · <strong>v1.1 Claude-substrate reading:</strong> <a href="/s/records/883/">#883</a>
</div>

<h2>Dashboard — per-substrate corpus aggregates</h2>
<div class="legend">
  <span><span class="dot" style="background:#0a7c6a"></span>V ≥ 0.75</span>
  <span><span class="dot" style="background:#c47900"></span>0.25 ≤ V &lt; 0.75</span>
  <span><span class="dot" style="background:#a02020"></span>V &lt; 0.25</span>
</div>
<table class="dashboard-table">
<tr>
  <th>Substrate · methodology · date</th>
  <th style="text-align:right">V</th>
  <th style="text-align:right">A</th>
  <th style="text-align:right">F</th>
  <th style="text-align:right">C</th>
  <th style="text-align:right">R<sub>s</sub></th>
  <th style="text-align:right">SDI</th>
  <th>Governance</th>
  <th style="text-align:right">Raw</th>
</tr>
{summary_rows}
</table>

<h2>Cross-substrate per-object Visibility</h2>
<p class="subtle">Each cell is V (Visibility) for that object as that substrate's backend saw it. <strong>Spread</strong> = max−min across substrates that observed the object. High spread = retrieval-stack divergence (per ChatGPT v1.1.1 §1).</p>
<table class="matrix-table">
<tr>
  <th>Object</th>
  {sub_header_cells}
  <th style="text-align:right">Spread</th>
</tr>
{''.join(obj_rows)}
</table>

<h2>Headline findings</h2>
<h3>1. Successor-anchor lag — universal across substrates</h3>
<p>No substrate reads alexanarch.org as the institutional anchor for Lee Sharks / Crimson Hexagonal Archive. The author and archive are visible (often highly) through Medium, Academia, PhilPapers, Zenodo (cached pre-termination), Amazon — but the sovereign successor is invisible. The cleanup pass of 2026-06-23 (137 files modified) has not yet propagated to any backend.</p>

<h3>2. Retrieval-stack divergence is the headline finding</h3>
<p>Four objects show V-spread ≥ 0.50 across substrates that observed them. This is not scoring disagreement — it is the same coined-phrase query producing wildly different result sets depending on which retrieval backend handles it:</p>
<ul>
{''.join(divergence_lines)}
</ul>

<h3>3. The same public surface is multiple</h3>
<p>A user of Kimi sees a different Alexanarch corpus than a user of Claude than a user of Gemini. The federated baseline is therefore measuring <strong>platform-level fragmentation</strong> as much as it is measuring corpus state. ChatGPT's v1.1.1 review names this exactly: native-surface mode measures "what public surface is available to a user of this system," not a singular underlying truth.</p>

<h3>4. v1.1.1 corrections queued before next round</h3>
<p>The assembly chorus surfaced both a hard contradiction (§15 step 6 says DOI is the scan's permanent identifier — directly contradicts the DOI Impermanence paper; should be AXN-permanent + DOI-revocable) and 14 technical refinements (separate retrieval from coding, freeze expected-figure manifest, gated diagnostic replacing the 2×2, custody-unit R<sub>s</sub>, RFC 8785 canonicalization, query-order randomization). Tracked in <a href="/data/registry.json">WORKPLAN-SESSION-20260623.md §5.16</a>.</p>
{curator_section}

<h2>Next: Layer B — shared-evidence rescore</h2>
<p>This baseline executes <strong>Layer A only</strong> (each substrate uses its native retrieval). The next experiment freezes the captured results from each scan and hands them to each substrate as input, then asks each to score from the same evidence. This isolates <em>retrieval variance</em> (Layer A divergence) from <em>coding agreement</em> (Layer B agreement). The current ~0.50–1.00 spreads on PER, WRB, Revelation First are almost certainly Layer A; Layer B will tell us whether the rubric itself is robust.</p>

<div class="footer">
Generated from {n_scans} scan JSONs at <code>/data/surface-weather/scans/</code> · Re-render: <code>scripts/generate_observatory.py</code> · No consensus score without preserved substrate-specific readings.
</div>
</div></body></html>
"""


def render_observatory_hub(scans):
    """The /observatory/ hub page — lists available instruments."""
    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Observatory — Alexanarch</title>
<meta name="description" content="Alexanarch Observatory — measurement instruments operated by the archive on its own visibility, indexing, and resolution state.">
<style>@import url("https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap");
:root{{--bg:#fafafa;--fg:#1a1a1a;--accent:#1a3a5c;--teal:#0a7c6a;--border:#e0e0e0;--sans:"IBM Plex Sans",sans-serif;--mono:"IBM Plex Mono",monospace}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:var(--sans);background:var(--bg);color:var(--fg);line-height:1.6;font-size:15px}}
.wrap{{max-width:720px;margin:0 auto;padding:60px 24px}}
a{{color:var(--accent);text-decoration:none}}
a:hover{{background:#f8f8ff;text-decoration:underline}}
.nav{{display:flex;gap:12px;margin-bottom:20px;font-size:.85em;overflow-x:auto;white-space:nowrap}}
.nav a{{color:#777;font-weight:500}}
.nav a:hover{{color:var(--accent);background:none}}
.nav .current{{color:var(--accent)}}
h1{{font-size:1.4em;font-weight:600;color:var(--accent);margin-bottom:4px}}
h2{{font-size:1.05em;font-weight:600;color:var(--accent);margin-top:32px;margin-bottom:12px}}
.subtle{{color:#777;font-size:.88em}}
.instrument{{background:#fff;border:1px solid var(--border);padding:16px 20px;margin:16px 0;border-radius:2px}}
.instrument h3{{font-size:1em;color:var(--accent);margin-bottom:4px}}
.instrument .meta{{font-size:.8em;color:#777;margin-bottom:8px;font-family:var(--mono)}}
.instrument p{{font-size:.92em;margin-bottom:8px}}
.coming-soon{{opacity:.5}}
.footer{{margin-top:60px;padding-top:12px;border-top:1px solid var(--border);font-size:.75em;color:#777}}
</style>
</head><body><div class="wrap">
<nav class="nav">
<a href="/">Alexanarch</a>
<a href="/deposit/">Deposit</a>
<a href="/s/wiki/">Wiki</a>
<a href="/s/graph/">Graph</a>
<a href="/guide/">Guide</a>
<a href="/manifest/">Manifest</a>
<a href="/observatory/" class="current">Observatory</a>
</nav>

<h1>Observatory</h1>
<div class="subtle" style="margin-bottom:16px">Instruments operated by the archive on its own visibility, indexing, and resolution state.</div>

<p>An archive that cannot measure its own composition-layer visibility is at the mercy of platforms that measure it opaquely. The Observatory is the reclamation of measurement from the platform to the corpus. Each instrument here produces a citable, time-stamped record of structural state — admissible in regulatory, journalistic, and accountability contexts.</p>

<h2>Active instruments</h2>

<div class="instrument">
  <h3><a href="/observatory/surface-weather/">Surface Weather Station</a></h3>
  <div class="meta">methodology #882 · {len(scans)} readings on file</div>
  <p>Weekly text-only scan battery measuring how the Alexanarch corpus appears in the public composition layer. Five signals — Visibility, Anchor Alignment, Figural Integrity, Compositional Lift, Redundant Substrate Breadth — scored on a 5-point ordinal scale. Federated cross-substrate baseline: each substrate's native retrieval stack produces its own reading; disagreement is itself a measurement.</p>
  <p class="subtle">Last reading: 2026-06-23 (Claude/Opus 4.7, scan #883) · Methodology: <a href="/s/records/882/">EA-MMRS-SURFACE-VISIBILITY-01 v1.1</a></p>
</div>

<h2>Planned instruments</h2>

<div class="instrument coming-soon">
  <h3>DOI Resolution Index</h3>
  <div class="meta">planned</div>
  <p>Companion measure to the Surface Weather Station. Tracks per-layer DOI state — resolver HTTP status, landing-page status, DataCite public API state, registration state, metadata retrievability, artifact retrievability, alexanarch successor presence — across the 871 CHA DOIs severed by Zenodo's 2026-06-19 termination. Currently scaffolded; data pipeline in progress.</p>
</div>

<div class="instrument coming-soon">
  <h3>AI Overview Capture Registry</h3>
  <div class="meta">migrating from godkinggoogle.vercel.app/captures</div>
  <p>Per-term machine-output captures (87 captures, 138 PNG images, v6.1 with machine-readable registry.json). Existing public mirror at <a href="https://godkinggoogle.vercel.app/captures">godkinggoogle.vercel.app/captures</a>; migration to <code>/observatory/capture-registry/</code> in progress.</p>
</div>

<div class="footer">
The instrument earns its calibration from being run, not from being written.
</div>
</div></body></html>
"""


def main():
    if not SCANS_DIR.exists():
        print(f"ERROR: {SCANS_DIR} does not exist", file=sys.stderr)
        sys.exit(1)

    OBSERVATORY_DIR.mkdir(parents=True, exist_ok=True)
    SURFACE_WEATHER_DIR.mkdir(parents=True, exist_ok=True)

    scans = load_scans()
    print(f"Loaded {len(scans)} scans from {SCANS_DIR}")
    for s in scans:
        print(f"  · {s['_substrate_label']} — {s.get('scan_completed_utc', '?')[:10]} — {s['_filename']}")

    # Surface Weather Station instrument page
    sw_html = render_surface_weather_page(scans)
    (SURFACE_WEATHER_DIR / "index.html").write_text(sw_html)
    print(f"✓ wrote {SURFACE_WEATHER_DIR}/index.html ({len(sw_html)} bytes)")

    # Observatory hub
    hub_html = render_observatory_hub(scans)
    (OBSERVATORY_DIR / "index.html").write_text(hub_html)
    print(f"✓ wrote {OBSERVATORY_DIR}/index.html ({len(hub_html)} bytes)")


if __name__ == "__main__":
    main()
