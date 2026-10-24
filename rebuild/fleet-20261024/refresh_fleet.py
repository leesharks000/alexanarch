#!/usr/bin/env python3
"""Fleet refresh of 2026-10-24, applied to local clones of the fleet repositories (one bundle per repository).

1. The network block, regenerated from data/api/fleet.json by scripts/build_network_block.py: gnosis.spxi.dev
   entered after spxi.dev; the OAI figure derived from data/oai-index.json (the blocks on the sites still said
   "1,400+").
2. The static fallbacks of live counts. A site's <span data-count="deposits.total">1,647</span> is filled at load
   from https://www.alexanarch.org/api/counts.json; a reader without script (a page extractor, a summarizer's fetch)
   sees the fallback, and on 2026-10-24 the fallbacks said 1,647 and 1,520 against 1,700. Only dotted keys that
   resolve in counts.json are rewritten; keys naming a site's own file (registry.json:..., schemas.json:...) are left.

    python3 refresh_fleet.py CLONE_DIR...
"""
import json, pathlib, re, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
C = json.loads((ROOT / "data/api/counts.json").read_text(encoding="utf-8"))
SPAN = re.compile(r'(<span[^>]*data-count="([a-z_]+(?:\.[a-z_]+)+)"[^>]*>)([\d,]+)(\+?)(</span>)')


def value(key):
    v = C
    for k in key.split("."):
        if not isinstance(v, dict) or k not in v:
            return None
        v = v[k]
    return v if isinstance(v, int) else None


for repo in sys.argv[1:]:
    repo = pathlib.Path(repo)
    subprocess.run([sys.executable, str(ROOT / "scripts/build_network_block.py"), "--apply", str(repo)], check=True,
                   capture_output=True)
    n = 0
    for p in repo.rglob("*.html"):
        if ".git" in p.parts:
            continue
        s = p.read_text(encoding="utf-8", errors="replace")
        def sub(m):
            global n
            v = value(m.group(2))
            if v is None:
                return m.group(0)
            new = f"{v:,}"
            if new != m.group(3):
                n += 1
            return m.group(1) + new + m.group(4) + m.group(5)
        s2 = SPAN.sub(sub, s)
        if s2 != s:
            p.write_text(s2, encoding="utf-8")
    print(f"{repo.name}: {n} fallback(s) refreshed")
