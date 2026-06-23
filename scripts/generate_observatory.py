#!/usr/bin/env python3
"""
generate_observatory.py — render /observatory/index.html from /data/surface-weather/scans/*.json

The Observatory IS the Surface Weather Station instrument (collapsed structure;
no nested subpath). Companion measurements live at their existing surfaces
(/captures/ for the AI Overview Capture Registry, /resolve/ for DOI Resolution).

Born static: scan summaries are baked into HTML at build time, no JS required for the core view.
Re-run this whenever a new scan lands in /data/surface-weather/scans/.
"""

import json
import os
import sys
from pathlib import Path

# Import canonical navbar renderer
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from scripts.render_navbar import render_navbar
from datetime import datetime


SCANS_DIR = Path("data/surface-weather/scans")
OBSERVATORY_DIR = Path("observatory")


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
<title>Observatory — Alexanarch</title>
<meta name="description" content="The Alexanarch Observatory: the Surface Weather Station instrument measuring how the corpus appears in the public composition layer. Federated five-substrate baseline 2026-06-22–23, v1.1.1 methodology stable across several scan rounds.">
<script type="application/ld+json">{json.dumps({"@context": "https://schema.org", "@type": "Dataset", "@id": "https://alexanarch.org/observatory/", "name": "Alexanarch Observatory — Surface Weather Station", "description": f"Visibility/anchor/figure/lift/breadth scores across {n_scans} substrate readings of the Alexanarch corpus on the public composition layer.", "creator": {"@type": "Person", "name": "Lee Sharks", "identifier": "https://orcid.org/0009-0000-1599-0703"}, "license": "https://creativecommons.org/licenses/by/4.0/", "dateModified": datetime.now().strftime("%Y-%m-%d")}, indent=None)}</script>
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
{render_navbar(active='/observatory/')}

<div class="subtle"><a href="/">Alexanarch</a> · Observatory</div>
<h1>Surface Weather Station</h1>
<div class="subtle" style="margin-bottom:8px">Federated cross-substrate baseline · {n_scans} readings · 2026-06-22 / 2026-06-23</div>

<p style="margin-top:16px">The Observatory's measuring instrument for how the Alexanarch corpus appears in the public composition layer. A weekly text-only scan battery scoring five signals per object — Visibility (V), Anchor Alignment (A), Figural Integrity (F), Compositional Lift (C), and Redundant Substrate Breadth (R<sub>s</sub>) — on a 5-point ordinal scale.</p>

<p style="margin-top:8px">This page is the <strong>federated baseline</strong>: each substrate's native retrieval stack produces its own reading. <strong>No consensus score is computed.</strong> Disagreement between substrates is itself a measurement of platform-level fragmentation, not noise to be averaged away.</p>

<div class="callout">
<strong>Current methodology:</strong> <a href="/s/records/884/">EA-MMRS-SURFACE-VISIBILITY-01 v1.1.1 (#884)</a> · <code>AXN:0380.EMPIRICAL.🧱🕙🪞🏛️💚🔃</code> — stable across several scan rounds<br>
<strong>Scans on file:</strong> performed under v1.1 (#882, <code>AXN:037E.EMPIRICAL.🚩♦️⏹️🔃❌🗡️</code>); v1.1.1 introduces the two-layer protocol, substrate-properties table, and gated diagnostic that will govern the next round<br>
<strong>Raw scan data:</strong> <a href="/data/surface-weather/scans/">/data/surface-weather/scans/</a> ({n_scans} JSON files, machine-legible) · <strong>Predecessor baseline:</strong> <a href="/s/records/881/">#881</a> · <strong>Claude/Brave Layer A:</strong> <a href="/s/records/883/">#883</a>
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
<p>The assembly chorus surfaced both a hard contradiction (§15 step 6 said DOI was the scan's permanent identifier — directly contradicting the DOI Impermanence paper; v1.1.1 corrects to AXN-permanent + DOI-revocable) and 14 technical refinements (separate retrieval from coding, freeze expected-figure manifest, gated diagnostic replacing the 2×2, custody-unit R<sub>s</sub>, RFC 8785 canonicalization, query-order randomization). All landed in <a href="/s/records/884/">v1.1.1 (#884)</a>.</p>
{curator_section}

<h2>Next: Layer B — shared-evidence rescore</h2>
<p>This baseline executes <strong>Layer A only</strong> (each substrate uses its native retrieval). The next experiment freezes the captured results from each scan and hands them to each substrate as input, then asks each to score from the same evidence. This isolates <em>retrieval variance</em> (Layer A divergence) from <em>coding agreement</em> (Layer B agreement). The current ~0.50–1.00 spreads on PER, WRB, Revelation First are almost certainly Layer A; Layer B will tell us whether the rubric itself is robust.</p>

<h2>Companion measurements</h2>
<p>This instrument measures the <em>composition layer</em> — how the corpus appears in search, summaries, and AI-mediated answers. Two related measurements operate as separate surfaces:</p>
<ul>
<li><strong><a href="/captures/">AI Overview Capture Registry</a></strong> — per-term machine-output captures recording what specific generative-search systems return for specific queries. The composition layer captured as evidence, not as score.</li>
<li><strong><a href="/resolve/">DOI Resolution Index</a></strong> — per-layer DOI state (resolver, landing, DataCite API, registration, metadata, artifact, successor anchor) across the 871 CHA DOIs severed in the 2026-06-19 Zenodo termination. The address-survival axis that pairs with this instrument's visibility axis in the §14 gated diagnostic.</li>
</ul>

<div class="footer">
Generated from {n_scans} scan JSONs at <code>/data/surface-weather/scans/</code> · Re-render: <code>scripts/generate_observatory.py</code> · No consensus score without preserved substrate-specific readings.
</div>
</div></body></html>
"""


def render_observatory_hub(scans):
    """DEPRECATED. The Observatory IS the Surface Weather Station now; no hub-vs-instrument split. Kept as a stub for older callers; will be removed in a future cleanup."""
    raise NotImplementedError("Observatory hub removed in collapsed-structure refactor. Use render_surface_weather_page(scans) and write to OBSERVATORY_DIR/index.html directly.")


def main():
    if not SCANS_DIR.exists():
        print(f"ERROR: {SCANS_DIR} does not exist", file=sys.stderr)
        sys.exit(1)

    OBSERVATORY_DIR.mkdir(parents=True, exist_ok=True)

    scans = load_scans()
    print(f"Loaded {len(scans)} scans from {SCANS_DIR}")
    for s in scans:
        print(f"  · {s['_substrate_label']} — {s.get('scan_completed_utc', '?')[:10]} — {s['_filename']}")

    # Observatory IS the Surface Weather Station — single page, no nested subpath
    page_html = render_surface_weather_page(scans)
    (OBSERVATORY_DIR / "index.html").write_text(page_html)
    print(f"✓ wrote {OBSERVATORY_DIR}/index.html ({len(page_html)} bytes)")


if __name__ == "__main__":
    main()
