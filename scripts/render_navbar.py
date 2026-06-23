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
    """
    try:
        nav = _load_nav()
        items = nav['items']
    except (FileNotFoundError, KeyError, json.JSONDecodeError):
        # Fallback: minimal core nav
        items = [
            {"path": "/", "label": "Alexanarch"},
            {"path": "/s/browse/", "label": "Browse"},
            {"path": "/deposit/", "label": "Deposit"},
            {"path": "/guide/", "label": "Guide"},
            {"path": "/manifest/", "label": "Manifest"},
        ]

    parts = ['<nav class="nav">']
    for item in items:
        path = item['path']
        label = item['label']
        style = ''
        if active and path == active:
            style = ' style="font-weight:600"'
        parts.append(f'<a href="{path}"{style}>{label}</a>')
    parts.append('</nav>')
    return ' '.join(parts)


if __name__ == '__main__':
    # CLI usage: python3 scripts/render_navbar.py [active-path]
    active = sys.argv[1] if len(sys.argv) > 1 else None
    print(render_navbar(active=active))
