"""Sync the navbar across all authored static HTML pages.

Reads data/navigation.json (via scripts.render_navbar) and rewrites the
content between <!-- NAV-START --> and <!-- NAV-END --> markers in each
listed page. Pages without markers get them added around their first
<nav class="nav">...</nav>.

Run after editing data/navigation.json. Idempotent.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from scripts.render_navbar import render_navbar

ROOT = Path(__file__).resolve().parent.parent

# All authored static pages with hand-written nav. Generators (wire_deposit,
# regenerate_surfaces, generate_observatory) read render_navbar directly,
# so their output doesn't need syncing here.
AUTHORED_PAGES = [
    'index.html',
    'deposit/index.html',
    'guide/index.html',
    'manifest/index.html',
    'captures/index.html',
    'resolve/index.html',
    'principles/index.html',
    'identifiers/index.html',
    'lexical/index.html',
    'citations/index.html',
    'addresses/index.html',
    'datasets/index.html',
]


def sync_one(page_path: Path) -> str:
    """Return one of: 'updated', 'unchanged', 'added-markers', 'no-nav', 'missing'."""
    if not page_path.exists():
        return 'missing'

    html = page_path.read_text()
    new_nav = render_navbar()

    # Path A: page has markers — replace content between them
    marker_pattern = re.compile(
        r'(<!--\s*NAV-START\s*-->)(.*?)(<!--\s*NAV-END\s*-->)',
        re.DOTALL,
    )
    m = marker_pattern.search(html)
    if m:
        existing_content = m.group(2).strip()
        if existing_content == new_nav:
            return 'unchanged'
        new_html = marker_pattern.sub(
            lambda mm: f'{mm.group(1)}\n{new_nav}\n{mm.group(3)}',
            html,
        )
        page_path.write_text(new_html)
        return 'updated'

    # Path B: no markers — find the first <nav class="nav">...</nav> and wrap with markers
    nav_pattern = re.compile(
        r'<nav[^>]*class=["\']nav["\'][^>]*>.*?</nav>',
        re.DOTALL,
    )
    m = nav_pattern.search(html)
    if m:
        wrapped = f'<!-- NAV-START -->\n{new_nav}\n<!-- NAV-END -->'
        new_html = html[:m.start()] + wrapped + html[m.end():]
        page_path.write_text(new_html)
        return 'added-markers'

    return 'no-nav'


def main():
    results = {}
    for rel in AUTHORED_PAGES:
        page = ROOT / rel
        status = sync_one(page)
        results.setdefault(status, []).append(rel)

    width = max((len(s) for s in results), default=0)
    for status in sorted(results):
        for rel in results[status]:
            print(f'  {status.rjust(width)}  {rel}')
    print(f'\n  {sum(len(v) for v in results.values())} page(s) processed.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
