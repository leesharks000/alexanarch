"""Regenerate one fleet repository's sitemap from its tree, in the fleet's own semantics (scripts/url_grammar.py: pages from
the tree, lastmod from git, off-site-canonical pages unlisted), sitemap only: no page is rewritten. Kept from the existing
sitemap: host, trailing-slash style, priorities, and listed files of other extensions (pdf, md, json). Left out: pages that
declare noindex or redirect (a sitemap lists canonicals only), and the repository's own housekeeping pages.
  python3 sitemap_regen.py WORKTREE [--pages-dir public] [--out sitemap.xml] [--also-root]"""
import re, sys, pathlib, subprocess, argparse
ap = argparse.ArgumentParser(); ap.add_argument("root"); ap.add_argument("--pages-dir", default="."); ap.add_argument("--out", default=None)
ap.add_argument("--also-root", action="store_true"); ap.add_argument("--exclude-prefix", default=""); a = ap.parse_args()
ROOT = pathlib.Path(a.root).resolve(); PAGES = (ROOT / a.pages_dir).resolve()
OUT = ROOT / (a.out or (a.pages_dir.rstrip("/") + "/sitemap.xml" if a.pages_dir != "." else "sitemap.xml"))
cur = OUT.read_text(encoding="utf-8") if OUT.exists() else ""
entries = re.findall(r"<url>\s*<loc>\s*([^<]+?)\s*</loc>(.*?)</url>", cur, re.S)
hosts = [re.match(r"https?://[^/]+", u).group(0) for u, _ in entries if re.match(r"https?://[^/]+", u)]
HOST = max(set(hosts), key=hosts.count) if hosts else None
if not HOST: sys.exit(f"no host in {OUT}")
pagelocs = [u for u, _ in entries if not re.search(r"\.[a-z0-9]{2,5}$", u)]
slash = sum(1 for u in pagelocs if u.endswith("/") and u != HOST + "/") > len(pagelocs) / 2
prio = {}
for u, rest in entries:
    m = re.search(r"<priority>([^<]+)</priority>", rest)
    if m: prio[u.rstrip("/") or u] = m.group(1).strip()
exts = sorted({m.group(1) for u, _ in entries for m in [re.search(r"\.([a-z0-9]{2,5})$", u)] if m and m.group(1) != "html"})
SKIP = {"node_modules", ".git", "dist", ".vercel", ".astro", "snapshots", "src", "scripts", "_source", "templates", "drafts", "rebuild"}
SKIP_NAMES = {"404.html"}
NOT_PAGES = {"/privacy", "/subscribed", "/t", "/search"}   # signup housekeeping; the Oracle's shared-thread viewer (a template filled by query)


def lastmod(p):
    o = subprocess.run(["git", "log", "-1", "--format=%cs", "--", str(p)], cwd=ROOT, capture_output=True, text=True).stdout.strip()
    return o or None


def url(path):
    if path == "/": return HOST + "/"
    return HOST + path + ("/" if slash else "")


pages, dropped = {}, []
for p in sorted(PAGES.rglob("*.html")):
    rel = p.relative_to(PAGES)
    if any(s in rel.parts for s in SKIP) or any(x.startswith(".") for x in rel.parts) or p.name in SKIP_NAMES: continue
    path = "/" + (rel.as_posix()[:-len("index.html")].rstrip("/") if p.name == "index.html" else rel.as_posix()[:-5])
    path = path if path != "/" else "/"
    h = p.read_text(encoding="utf-8", errors="replace")
    head = h[:20000].lower()
    can = re.search(r'<link[^>]+rel="canonical"[^>]+href="([^"]+)"', h[:20000]) or re.search(r'<link[^>]+href="([^"]+)"[^>]+rel="canonical"', h[:20000])
    apex = HOST.replace("https://www.", "https://")
    if can and not (can.group(1).startswith(HOST) or can.group(1).startswith(apex)):
        dropped.append((path, "canonical off-site")); continue
    if re.search(r'<meta[^>]+name=["\']robots["\'][^>]+noindex', head) or re.search(r'<meta[^>]+content=["\'][^"\']*noindex[^>]+name=["\']robots', head):
        dropped.append((path, "noindex")); continue
    if re.search(r'http-equiv=["\']refresh', head):
        dropped.append((path, "redirect")); continue
    if a.exclude_prefix and (path == a.exclude_prefix or path.startswith(a.exclude_prefix + "/")):
        continue   # listed in its own generator-owned sitemap
    if path in NOT_PAGES:
        dropped.append((path, "housekeeping")); continue
    pages[path] = p
lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for path in sorted(pages, key=lambda x: (x != "/", x)):
    u = url(path); lm = lastmod(pages[path])
    pr = prio.get(u.rstrip("/") or u) or ("1.0" if path == "/" else "0.7")
    lines.append(f"  <url><loc>{u}</loc>" + (f"<lastmod>{lm}</lastmod>" if lm else "") + f"<priority>{pr}</priority></url>")
for ext in exts:
    for p in sorted(PAGES.rglob(f"*.{ext}")):
        rel = p.relative_to(PAGES)
        if any(s in rel.parts for s in SKIP) or any(x.startswith(".") for x in rel.parts): continue
        if p.name.upper() in ("README.MD", "LICENSE.MD", "CHANGELOG.MD", "AGENTS.MD", "CLAUDE.MD"): continue
        if p.name.startswith("sitemap") or p.name in ("package.json", "package-lock.json", "vercel.json", "tsconfig.json"): continue
        u = f"{HOST}/{rel.as_posix()}"
        if u not in {x for x, _ in entries}: continue   # other files only as the existing sitemap listed them
        lm = lastmod(p)
        pr = prio.get(u) or "0.5"
        lines.append(f"  <url><loc>{u}</loc>" + (f"<lastmod>{lm}</lastmod>" if lm else "") + f"<priority>{pr}</priority></url>")
lines.append("</urlset>")
xml = "\n".join(lines) + "\n"
old = {u.rstrip("/") for u, _ in entries}; new = set(re.findall(r"<loc>([^<]+)</loc>", xml)); newn = {u.rstrip("/") for u in new}
OUT.write_text(xml, encoding="utf-8")
if a.also_root and OUT != ROOT / "sitemap.xml": (ROOT / "sitemap.xml").write_text(xml, encoding="utf-8")
print(f"{ROOT.name}: {len(new)} urls (was {len(entries)}); added {sorted(newn - old)[:12]}{'…' if len(newn - old) > 12 else ''} ({len(newn - old)}); "
      f"removed {sorted(old - newn)[:12]} ({len(old - newn)}); dropped {[d for d in dropped][:8]} ({len(dropped)})")
