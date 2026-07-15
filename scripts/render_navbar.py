"""Render the canonical Alexanarch navigation bar from data/navigation.json.

Single source of truth: data/navigation.json. All generators import this
function instead of hardcoding nav HTML. Authored static pages get synced
by scripts/sync_navbars.py.

Usage:
    from scripts.render_navbar import render_navbar
    nav_html = render_navbar(active='/s/wiki/')  # or active=None
"""
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NAV_FILE = ROOT / 'data' / 'navigation.json'

_CACHE = None


def _load_nav():
    """Load navigation.json, with a small in-process cache."""
    global _CACHE
    if _CACHE is None:
        with open(NAV_FILE) as f:
            _CACHE = json.load(f)
    return _CACHE


def render_navbar(active=None):
    """Return the canonical navigation HTML as a single string.

    active: optional path string (e.g. '/s/wiki/'). If given, that link
            gets style='font-weight:600' for visual emphasis.

    Returns: '<nav class="nav">...</nav>' as a single string with no
             trailing newline. Callers wrap as they need.

    Rendering (schema v1.1+):
      Items without a `cluster` field are rendered first, ungrouped. Items
      with a `cluster` field are rendered grouped, in the order given by
      `clusters_order`. Each cluster is preceded by a subtle inline label
      (`<span class="nav-cluster" ...>`) with monospace typography and a
      light left-border divider. Inline styles are used so the cluster
      labels look correct regardless of whether the host page has
      .nav-cluster CSS defined.
    """
    try:
        nav = _load_nav()
        items = nav['items']
        clusters_order = nav.get('clusters_order', [])
    except (FileNotFoundError, KeyError, json.JSONDecodeError):
        # Fallback: minimal core nav
        items = [
            {"path": "/", "label": "Alexanarch"},
            {"path": "/s/browse/", "label": "Browse"},
            {"path": "/deposit/", "label": "Deposit"},
            {"path": "/guide/", "label": "Guide"},
            {"path": "/manifest/", "label": "Manifest"},
        ]
        clusters_order = []

    # Cluster label style (kept minimal so it degrades gracefully anywhere
    # the host page's .nav CSS applies). font-size relative to nav .85em.
    _CLUSTER_STYLE = (
        'color:#a0a0a0;'
        'font-family:ui-monospace,SFMono-Regular,Menlo,monospace;'
        'font-size:0.78em;'
        'letter-spacing:0.09em;'
        'text-transform:uppercase;'
        'padding:0 2px 0 10px;'
        'margin-left:6px;'
        'border-left:1px solid #d9d9d0;'
    )
    _CLUSTER_STYLE_FIRST = _CLUSTER_STYLE.replace('border-left:1px solid #d9d9d0;', 'border-left:none;padding-left:0;margin-left:2px;')

    # Group items
    ungrouped = [it for it in items if not it.get('cluster')]
    by_cluster = {}
    for it in items:
        c = it.get('cluster')
        if c:
            by_cluster.setdefault(c, []).append(it)

    def _link(item):
        path = item['path']
        label = item['label']
        style = ' style="font-weight:600"' if active and path == active else ''
        return f'<a href="{path}"{style}>{label}</a>'

    parts = ['<nav class="nav">']
    for it in ungrouped:
        parts.append(_link(it))

    first_cluster = True
    for cluster_name in clusters_order:
        cluster_items = by_cluster.get(cluster_name, [])
        if not cluster_items:
            continue
        style = _CLUSTER_STYLE_FIRST if first_cluster and not ungrouped else _CLUSTER_STYLE
        parts.append(f'<span class="nav-cluster" style="{style}">{cluster_name}</span>')
        for it in cluster_items:
            parts.append(_link(it))
        first_cluster = False

    # Any cluster present in items but missing from clusters_order — render at end.
    trailing = [c for c in by_cluster if c not in clusters_order]
    for c in trailing:
        parts.append(f'<span class="nav-cluster" style="{_CLUSTER_STYLE}">{c}</span>')
        for it in by_cluster[c]:
            parts.append(_link(it))

    parts.append('</nav>')
    return ' '.join(parts)


if __name__ == '__main__':
    # CLI usage: python3 scripts/render_navbar.py [active-path]
    active = sys.argv[1] if len(sys.argv) > 1 else None
    print(render_navbar(active=active))
