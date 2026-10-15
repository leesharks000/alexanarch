"""capture_join_render.py — the projections of data/capture-joins.json onto alexanarch's own pages (2026-10-14).

One reader for three renderers: the capture record page (build_capture_records.py), the deposit record page
(wire_deposit.py, "Read in composition") and the /non entity (build_non.py, "Observations of this entity").
Only confirmed relations render, and only for observations inside the join's render_scope. Every row carries its
obs_id and links to the observation's own anchor; an interpretive row carries its finding and its excerpt.
Source relations (appeared_in) and interpretive ones (mentions, about, distorts …) are shown under their own verbs.
"""
import html, json, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
J = ROOT / "data/capture-joins.json"
INSTR = {"0.6": "Provenance Erasure Rate", "0.8": "Semantic Addresses Framework", "0.9": "Capture Registry",
         "0.10": "Conformance Instrument", "0.15": "Platform Erosion Observatory", "5.4": "Canary Registry"}
VERB = {"held_by": "held by", "scored_by": "scored by", "mentions_instrument": "named in the answer",
        "distorts": "distorts", "represents_faithfully": "represents faithfully"}
_cache = None
ANCH = {}


def esc(s):
    return html.escape(str(s or ""), quote=True)


def load():
    global _cache
    if _cache is None:
        try:
            d = json.loads(J.read_text(encoding="utf-8"))
        except Exception:
            d = {"render_scope": [], "relations": []}
        scope = set(d.get("render_scope") or [])
        rels = [r for r in d.get("relations", []) if r.get("state") == "confirmed" and r["obs_id"] in scope]
        by_obs = {}
        for r in rels:
            by_obs.setdefault(r["obs_id"], []).append(r)
        global ANCH
        ANCH = {oid: anchor(rs[0]) for oid, rs in by_obs.items()}
        _cache = (by_obs, d.get("derived_from", ""))
    return _cache


def anchor(r):
    return f"/captures/{r['entry']}/#{r['obs_slug']}"


def finding(rs):
    return next((r for r in rs if r["verb"] in ("distorts", "represents_faithfully")), None)


def _evidence(f):
    if not f:
        return ""
    return (f'<div style="margin:3px 0 0 0"><strong>Finding</strong> ({esc(VERB[f["verb"]])}): {esc(f.get("finding"))}</div>'
            f'<div style="margin:2px 0 0 0"><strong>Response:</strong> “{esc(f.get("excerpt"))}{"" if (f.get("excerpt") or "").endswith((".", "!", "?")) else "…"}”</div>'
            f'<div class="meta" style="font-size:.85em;color:#777">read by {esc(f.get("decision", {}).get("reader"))}, '
            f'{esc(f.get("decision", {}).get("date"))}, against {esc(f.get("decision", {}).get("revision"))}</div>')


def _obj(o):
    k, _, v = o.partition(":")
    if k == "deposit":
        return f'<a href="/s/records/{esc(v)}/">#{esc(v)}</a>'
    if k == "surface":
        return f'<a href="https://{esc(v)}/">{esc(v)}</a>'
    if k == "non":
        return f'<a href="/non/{esc(v)}/">/non {esc(v)}</a>'
    if k == "instrument":
        return f'<a href="https://www.spxi.dev/methods#m-{esc(v.replace(".", "-"))}">{esc(v)} {esc(INSTR.get(v, ""))}</a>'
    return esc(o)


def _sortkey(o):
    k, _, v = o.partition(":")
    return (k, int(v) if v.isdigit() else 0, v)


def _line(r0, rs, lead):
    f = finding(rs)
    return (f'<li style="margin:0 0 8px 0">{lead}<a href="{anchor(r0)}"><code>{esc(r0["obs_id"])}</code></a> · {esc(r0.get("date"))} · '
            f'{esc(r0.get("surface"))} · «{esc(r0.get("q"))}»{_evidence(f)}</li>')


def observation_block(entry):
    """For a capture record page: per observation in scope, its joins by verb."""
    by_obs, src = load()
    obs = [(oid, rs) for oid, rs in by_obs.items() if rs[0]["entry"] == entry["slug"]]
    if not obs:
        return ""
    out = []
    for oid, rs in obs:
        r0 = rs[0]
        app = sorted({r["object"] for r in rs if r["verb"] == "appeared_in"}, key=_sortkey)
        men = sorted({r["object"] for r in rs if r["verb"] == "mentions"}, key=_sortkey)
        non = sorted({r["object"] for r in rs if r["verb"] in ("about", "corrected_by")})
        ins = sorted({(r["verb"], r["object"]) for r in rs if r["object"].startswith("instrument:")}, key=lambda x: (x[0], _sortkey(x[1])))
        prs = [r for r in rs if r["verb"] == "pair_of"]
        f = finding(rs)
        parts = [f'<div style="margin:0 0 6px"><a href="{anchor(r0)}"><code>{esc(oid)}</code></a> · {esc(r0.get("date"))} · {esc(r0.get("surface"))}</div>']
        if f:
            parts.append(_evidence(f))
        if app:
            parts.append("<div><strong>Appeared in</strong> (source cards): " + " · ".join(_obj(o) for o in app) + "</div>")
        if men:
            parts.append("<div><strong>Named in the answer</strong>: " + " · ".join(_obj(o) for o in men) + "</div>")
        if non:
            parts.append("<div><strong>About</strong>: " + " · ".join(_obj(o) for o in non) + "</div>")
        if ins:
            parts.append("<div><strong>Instruments</strong>: " + " · ".join(f'{esc(VERB.get(v, v))} {_obj(o)}' for v, o in ins) + "</div>")
        if prs:
            parts.append("<div><strong>Paired with</strong>: " + " · ".join(
                f'<a href="{esc(ANCH.get(p["object"][12:], "/captures/"))}"><code>{esc(p["object"][12:])}</code></a> <span class="meta">({esc(p["basis"])})</span>'
                for p in prs) + "</div>")
        out.append('<div style="margin:0 0 8px">' + "\n".join(parts) + "</div>")
    return ('<section class="cap-joins" style="font-size:.88em;margin:8px 0 10px;padding:8px 10px;border-left:3px solid #2a6f6f">\n'
            '<h2 style="font-size:1em;margin:0 0 4px">Joined: where this observation returns</h2>\n'
            + "\n".join(out) + f'\n<p class="meta" style="font-size:.85em;color:#777;margin:4px 0 0">Source relations are read off the cards; '
            f'the finding, the mentions, the entity and the pair are readings. From <a href="/data/capture-joins.json">the capture join</a> ({esc(src)}).</p>\n</section>\n')


def deposit_block(n):
    """For a deposit record page: every observation in scope whose cards resolved to the deposit, then those that name it."""
    by_obs, src = load()
    obj = f"deposit:{n}"
    app, men = [], []
    for oid, rs in by_obs.items():
        if any(r["verb"] == "appeared_in" and r["object"] == obj for r in rs):
            app.append((rs[0], rs))
        elif any(r["verb"] == "mentions" and r["object"] == obj for r in rs):
            men.append((rs[0], rs))
    if not app and not men:
        return ""
    key = lambda x: (x[0].get("date") or "", x[0]["obs_id"])
    h = ['<section id="read-in-composition" style="margin:18px 0;padding:10px 12px;border-left:3px solid #2a6f6f;font-size:.88em">',
         '<h2 style="margin-top:0">Read in composition</h2>',
         '<p class="meta" style="color:#777">Machine answers in which this deposit took part, from the Capture Registry. Each row is one observation, '
         'with its finding and the passage the finding concerns.</p>']
    if app:
        h.append("<h3 style=\"font-size:1em\">Cited: a source card resolved to this deposit</h3><ul>")
        h += [_line(r0, rs, "") for r0, rs in sorted(app, key=key, reverse=True)] + ["</ul>"]
    if men:
        h.append("<h3 style=\"font-size:1em\">Named: the answer names this work, with no card for it</h3><ul>")
        h += [_line(r0, rs, "") for r0, rs in sorted(men, key=key, reverse=True)] + ["</ul>"]
    h.append(f'<p class="meta" style="color:#777;font-size:.85em">From <a href="/data/capture-joins.json">the capture join</a> ({esc(src)}).</p></section>')
    return "\n".join(h) + "\n"


def non_block(entity):
    """For a /non entity: the observations read as concerning it."""
    by_obs, src = load()
    obj = f"non:{entity}"
    rows = [(rs[0], rs) for oid, rs in by_obs.items() if any(r["verb"] in ("about", "corrected_by") and r["object"] == obj for r in rs)]
    if not rows:
        return ""
    rows.sort(key=lambda x: (x[0].get("date") or "", x[0]["obs_id"]), reverse=True)
    return ('<div class="cap-joins" style="font-size:.88em;margin:10px 0;padding:8px 10px;border-left:3px solid #2a6f6f">'
            '<h3 style="font-size:1em;margin:0 0 4px">Observations of this entity</h3><ul>'
            + "".join(_line(r0, rs, "") for r0, rs in rows)
            + f'</ul><p class="meta" style="font-size:.85em">Confirmed by reading; from <a href="/data/capture-joins.json">the capture join</a> ({esc(src)}).</p></div>')


# ── PAGE DATES (2026-10-15) ───────────────────────────────────────────────────────────────────────────────
# A page that renders a join changed on the day the join was confirmed, whatever its record's own dates say
# (record_modification.py: date_modified tracks the RECORD; it deliberately does not move for projections).
# The sitemap <lastmod> and the WebPage dateModified are page dates, so each renderer above has a date
# function here that selects EXACTLY what it renders and returns the latest decision date among the rows it
# shows (the date a reader confirmed the relation; else the observation date). "" when the page renders no
# join. Deterministic: an unchanged join file gives unchanged dates.

def _rs_date(rs):
    return max([str((r.get("decision") or {}).get("date") or r.get("date") or "")[:10] for r in rs] or [""])


def deposit_date(n):
    by_obs, _ = load()
    obj = f"deposit:{n}"
    return max([_rs_date(rs) for rs in by_obs.values()
                if any(r["verb"] in ("appeared_in", "mentions") and r["object"] == obj for r in rs)] or [""])


def entry_date(slug):
    by_obs, _ = load()
    return max([_rs_date(rs) for rs in by_obs.values() if rs[0]["entry"] == slug] or [""])


def non_date(entity):
    by_obs, _ = load()
    obj = f"non:{entity}"
    return max([_rs_date(rs) for rs in by_obs.values()
                if any(r["verb"] in ("about", "corrected_by") and r["object"] == obj for r in rs)] or [""])


def page_date(*dates):
    """The latest of the given dates (record date, join date …), ignoring empties."""
    return max([str(d)[:10] for d in dates if d] or [""])
