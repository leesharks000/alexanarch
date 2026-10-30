"""Fleet sitemap audit, 2026-10-29. For each surface: the sitemap(s) at origin/main against the indexable HTML pages at origin/main,
and the live sitemap against the repository's. Reads only; writes a JSON report.
  python3 sitemap_audit.py OUT.json"""
import json, re, subprocess, sys, urllib.request, collections, xml.etree.ElementTree as ET
FLEET = "/home/claude/fleet"
MAP = {"alexanarch.org": "/home/claude/alexanarch", "axnidentifiers.org": "axn-identifiers", "chatgptpsychosis.org": "chatgptpsychosis-site",
       "crimsonhexagonal.org": "crimson-hexagonal-interface", "godkinggoogle.com": "godkinggoogle", "holographickernel.org": "holographic-kernel",
       "laborvector.org": "laborvector", "lagrangeobservatory.org": "lagrange-observatory", "leesharks.com": "leesharks.com",
       "livingarchitecturelab.org": "living-architecture-lab", "machinemediation.org": "machinemediation-org", "maryleelabor.org": "maryleelabor-org",
       "metadatapacket.dev": "metadatapacket-dev", "persistentidentifiers.org": "platform-erosion-observatory", "pessoagraph.org": "pessoa-knowledge-graph",
       "provenanceerasure.org": "provenance-erasure", "restoredacademy.org": "restoredacademy", "revelationfirst.com": "revelationfirst-com",
       "secretbookofwalt.org": "secret-book-of-walt", "semanticeconomy.org": "lee-sharks-corporate", "semanticphysics.org": "semanticphysics-site",
       "spxi.dev": "spxi-dev", "surfacemap.org": "surface-map", "survivethedeletion.vercel.app": "survivethedeletion", "themandalaoracle.com": "the-mandala-oracle",
       "traininglayerliterature.org": "traininglayerliterature-org", "vpcor.org": "vpcor-org", "watergiraffe.org": "watergiraffe-org",
       "operativesemiotics.org": "operative-semiotics"}
PREFIX = {"metadatapacket.dev": "public/", "crimsonhexagonal.org": "public/", "secretbookofwalt.org": "public/", "livingarchitecturelab.org": "public/"}
UA = "Mozilla/5.0 (compatible; Crimson-Hexagonal-fleet-audit)"


def git(repo, *a):
    return subprocess.run(["git", "-C", repo, *a], capture_output=True, text=True).stdout


def show(repo, path):
    r = subprocess.run(["git", "-C", repo, "show", f"origin/main:{path}"], capture_output=True)
    return r.stdout if r.returncode == 0 else None


def locs(xml_bytes):
    out, kids = [], []
    try:
        root = ET.fromstring(xml_bytes)
    except Exception as ex:
        return None, None, str(ex)
    ns = re.match(r"\{.*\}", root.tag); ns = ns.group(0) if ns else ""
    if root.tag.endswith("sitemapindex"):
        kids = [e.findtext(f"{ns}loc").strip() for e in root.findall(f"{ns}sitemap")]
    for u in root.findall(f"{ns}url"):
        out.append((u.findtext(f"{ns}loc", "").strip(), (u.findtext(f"{ns}lastmod") or "").strip()))
    return out, kids, None


def norm(u):
    u = re.sub(r"^https?://(www\.)?[^/]+", "", u.strip())
    u = re.sub(r"(index)?\.html$", "", u)
    u = u.rstrip("/")
    return u or "/"


def page_of(path):
    if not path.endswith(".html"): return None
    if path in ("404.html",) or path.startswith(("node_modules/", ".", "templates/", "_", "scripts/", "rebuild/", "drafts/", "snapshots/", "src/", "dist/")): return None
    return norm("/" + path)


def fetch(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=25) as r:
            return r.status, r.read()
    except urllib.error.HTTPError as e:
        return e.code, b""
    except Exception as e:
        return str(e)[:80], b""


rep = {}
for dom, repo in MAP.items():
    repo = repo if repo.startswith("/") else f"{FLEET}/{repo}"
    subprocess.run(["git", "-C", repo, "fetch", "-q", "origin"], capture_output=True)
    head = git(repo, "rev-parse", "--short", "origin/main").strip()
    PRE = PREFIX.get(dom, "")
    files_all = git(repo, "ls-tree", "-r", "--name-only", "origin/main").split("\n")
    files = [f[len(PRE):] for f in files_all if f.startswith(PRE)]
    fileset = set(files)
    # last commit date per file, one pass
    last = {}
    cur = None
    for line in git(repo, "log", "origin/main", "--format=@%cs", "--name-only").split("\n"):
        if line.startswith("@"): cur = line[1:]
        elif line and line not in last: last[line] = cur
    sm_files = [f for f in files if re.fullmatch(r"(sitemap[^/]*\.xml)", f)]
    entries, kids_all, errs = [], [], []
    for f in sm_files:
        b = show(repo, PRE + f); e, k, err = locs(b)
        if err: errs.append(f"{f}: {err}"); continue
        entries += e; kids_all += k
    # child sitemaps referenced by an index, if they live in subfolders
    for k in kids_all:
        p = norm(k).lstrip("/")
        for cand in (p, p + ".xml"):
            if cand in fileset and cand not in sm_files:
                b = show(repo, PRE + cand); e, _, err = locs(b)
                if not err: entries += e
    pages = {}
    for f in files:
        p = page_of(f)
        if p is None: continue
        pages[p] = f
    # indexable: drop noindex and meta-refresh redirects (read each page once; large repos sample-free but capped)
    noindex = set()
    for p, f in pages.items():
        b = show(repo, PRE + f) or b""
        h = b[:6000].decode("utf-8", "ignore").lower()
        if re.search(r'<meta[^>]+name=["\']robots["\'][^>]+noindex', h) or 'http-equiv="refresh"' in h or "http-equiv='refresh'" in h:
            noindex.add(p)
    idx = {p for p in pages if p not in noindex}
    sm = {}
    for u, lm in entries:
        sm[norm(u)] = lm
    missing = sorted(idx - set(sm))
    dangling = sorted(p for p in sm if p not in pages and not any(norm("/" + x) == p for x in fileset))
    stale = []
    for p, lm in sm.items():
        f = pages.get(p)
        if f and lm and last.get(PRE + f) and lm[:10] < last[PRE + f]:
            stale.append((p, lm[:10], last[PRE + f]))
    st, live = fetch(f"https://{'www.' if dom not in ('survivethedeletion.vercel.app', 'spxi.dev', 'metadatapacket.dev') else ''}{dom}/sitemap.xml")
    le, lk, lerr = locs(live) if live else (None, None, "no body")
    repo_sm = show(repo, PRE + "sitemap.xml")
    rep[dom] = {"repo": repo.split("/")[-1], "head": head, "sitemaps": sm_files, "index_children": kids_all, "parse_errors": errs,
                "sitemap_urls": len(sm), "html_pages": len(pages), "indexable": len(idx), "noindex_or_redirect": len(noindex),
                "missing": len(missing), "missing_sample": missing[:25], "dangling": len(dangling), "dangling_sample": dangling[:25],
                "lastmod_older_than_file": len(stale), "stale_sample": stale[:10],
                "live_status": st, "live_urls": (len(le) if le is not None else None), "live_children": lk,
                "live_matches_repo": (live == repo_sm) if live and repo_sm else None}
    r = rep[dom]
    print(f"{dom:32} {r['repo'][:26]:26} sm={r['sitemap_urls']:5} idx={r['indexable']:5} miss={r['missing']:4} dang={r['dangling']:3} stale={r['lastmod_older_than_file']:4} live={st} {'=' if r['live_matches_repo'] else '≠' if r['live_matches_repo'] is False else '?'}")
json.dump(rep, open(sys.argv[1], "w"), indent=1, ensure_ascii=False)
