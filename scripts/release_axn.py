#!/usr/bin/env python3
"""release_axn.py — AXNs for frozen releases: datasets, instruments, sites (adopted 2026-10-27).

MANUS, 2026-10-27, adopting the proposal of that day ("adopted. lets proceed"): dataset releases first, starting with the
Capture Registry; then instrument and protocol versions; then typed relations; then site releases, beginning with an
alexanarch freeze. The rule adopted with it: mint when preserving the distinction will matter later, hash when integrity
matters, locate when pointing is enough. Regenerated pages, the gallery, the addresses and dashboards are projections;
the release that produces them is the identified state.

THREE DISTINCTIONS. Continuity: the continuing object takes one position in the shared allocation ledger
(data/symbolon-registry/allocation.json, rule max(registry hex, ledger) + 1) and its root AXN:<HEX>.<FAMILY> names it
across its releases. Version: each release is AXN:<HEX>.<FAMILY>.<glyphs>, the glyphs derived (table v2.1) from the
SHA-256 of what the release freezes. Location: where the release's bytes can be had (the site path, the git commit that
records the release, a hub copy); a location can change and the release keeps its identity.

    family    object                                   what a release freezes
    RELEASE   a dataset (datasets/catalog.json, the    a manifest: every constituent file of the release with the
              Capture Registry with its held earlier    SHA-256 of its bytes (sha256sum format, paths from the repository
              copies v8.11 and v9.6)                    root, sorted; HTML pages left out, being projections)
    INSTRUMENT a protocol, schema, grammar or rubric    one file: the release's AXN derives from the file's own bytes, and
              (data/api/index.json, rhizomes/_grammars, a frozen copy is kept (data/releases/frozen/); several files: a
              the Capture Registry's intake instrument, manifest, as for datasets
              the PER-dim rubric)
    SITE      a site (alexanarch first)                a manifest of the tree of one commit (base_commit), read from git:
                                                       every file except its HTML pages and sitemaps (projections),
                                                       SHA256SUMS.txt and the release ledger. The release is that commit's
                                                       tree, verifiable by checking it out and running sha256sum -c

A release is frozen when --apply finds an object whose current state differs from its last release. Its label is the
version the object declares (the Capture Registry's version, a protocol's current_version, a grammar's version), else the
date. A state already released is not released again. Manifests: data/releases/manifests/<object>/<label>.sha256 —
verify from the repository root with `sha256sum -c`. Ledger: data/releases/axn.json.

    python3 scripts/release_axn.py --check [--only KEY ...]     # what has moved since its last release; writes nothing
    python3 scripts/release_axn.py --apply [--only KEY ...] [--kinds dataset,instrument,site]
"""
import datetime, hashlib, json, pathlib, re, shutil, subprocess, sys
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import axn_lib as A

LEDGER = ROOT / "data/releases/axn.json"
MANI = ROOT / "data/releases/manifests"
FROZEN = ROOT / "data/releases/frozen"
ALLOC = ROOT / "data/symbolon-registry/allocation.json"
SITE = "https://www.alexanarch.org"
GH = "https://github.com/leesharks000/alexanarch"
SKIP_NAME = re.compile(r"(\.html?$|^\.DS_Store$|\.pyc$)")


def sha_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def tree(rel):
    """Every file under rel (a directory or a file), repository-relative, HTML and caches left out."""
    p = ROOT / rel
    if p.is_file():
        return [rel]
    out = []
    for f in sorted(p.rglob("*")):
        if f.is_file() and not SKIP_NAME.search(f.name) and "__pycache__" not in f.parts:
            out.append(str(f.relative_to(ROOT)))
    return out


def site_tree(commit="HEAD"):
    """The site at a commit, read from git: (path, sha256, size) for every file of the commit's tree except HTML pages,
    sitemaps, SHA256SUMS.txt and the release ledger. Read from the commit's blobs, so the release is exactly that tree
    whatever the working tree holds."""
    r = subprocess.run(["git", "ls-tree", "-r", "-z", commit], cwd=ROOT, capture_output=True, check=True)
    ents = []
    for line in r.stdout.decode("utf-8").split("\0"):
        if not line:
            continue
        meta, path = line.split("\t", 1)
        mode, typ, oid = meta.split()
        n = path.rsplit("/", 1)[-1]
        if typ != "blob" or mode == "120000" or SKIP_NAME.search(n) or path.startswith("data/releases/") or n == "SHA256SUMS.txt" \
                or re.match(r"sitemap[^/]*\.xml$", path):
            continue
        ents.append((path, oid))
    ents.sort()
    out = []
    pr = subprocess.Popen(["git", "cat-file", "--batch"], cwd=ROOT, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    for path, oid in ents:
        pr.stdin.write((oid + "\n").encode()); pr.stdin.flush()
        hdr = pr.stdout.readline().split()
        size = int(hdr[2]); h = hashlib.sha256(); left = size
        while left:
            b = pr.stdout.read(min(left, 1 << 20)); h.update(b); left -= len(b)
        pr.stdout.read(1)
        out.append((path, h.hexdigest(), size))
    pr.stdin.close(); pr.wait()
    return out


def manifest(paths):
    return "".join(f"{sha_file(ROOT / p)}  {p}\n" for p in sorted(set(paths))).encode("utf-8")


def ver_of(path, *keys):
    try:
        d = json.loads((ROOT / path).read_text(encoding="utf-8"))
        for k in keys:
            if d.get(k):
                return str(d[k])
    except Exception:
        pass
    return None


# the stores scripts/build_hf_dataset.py reads (2026-10-28)
HF_SOURCES = ["data/registry.json", "data/texts", "data/EA-WG-CAPTURES-01.json", "data/citation-graph.json",
              "data/lexical-minting-registry.json", "data/named-entities.json", "data/hexagon-seats.json",
              "data/nodes.jsonl", "data/relations.jsonl", "data/assertions.jsonl", "data/blog-index.json"]
WIKIS = ROOT / "data/releases/wikis.json"


def objects():
    """The continuing objects and, for each, how to read its current state."""
    objs = []
    cat = json.loads((ROOT / "datasets/catalog.json").read_text(encoding="utf-8"))["entries"]
    seen = set()
    for e in cat:
        src = str(e.get("source_path") or "")
        if e.get("slug") == "crimson-hexagonal-archive":
            # 2026-10-28 (MANUS: "lets fill the gaps"): the canonical Hub dataset takes its own position. Its release
            # freezes the stores scripts/build_hf_dataset.py builds it from, so a Hub build can be checked against them.
            objs.append({"key": "crimson-hexagonal-archive", "kind": "dataset", "family": "RELEASE", "name": "crimson-hexagonal-archive",
                         "class": e.get("dataset_class"), "source": [x for x in HF_SOURCES if (ROOT / x).exists()],
                         "locations": [f"https://huggingface.co/datasets/{e.get('hub_repo') or 'leesharks/crimson-hexagonal-archive'}", f"{SITE}/datasets/"],
                         "label": None, "basis": "manifest", "builder": e.get("builder"), "instrument": None})
            seen.add("crimson-hexagonal-archive")
            continue
        if not src.startswith(("datasets/", "rhizomes/")):
            continue
        src = src.rstrip("/")
        key = ("rhizome-" if src.startswith("rhizomes/") else "") + e["slug"].lower().replace(" ", "-").replace("–", "-")
        key = re.sub(r"[^a-z0-9-]+", "-", key).strip("-")
        if key in seen:
            continue
        seen.add(key)
        paths = [src] + ([e["grammar"]] if e.get("grammar") else [])
        locs = [f"{SITE}/{src}/"]
        if e.get("hub_repo") and e["hub_repo"] != "None":
            locs.append(f"https://huggingface.co/datasets/{e['hub_repo']}")
        label = None
        if key == "capture-registry":
            # the registry, its sealed observations and their AXN ledger: the identified state. datasets/capture-registry/
            # is a copy carrying run timestamps, a location of the release (a check must not compare a field that changes
            # every run).
            label = ver_of("data/EA-WG-CAPTURES-01.json", "version")
            paths = ["data/EA-WG-CAPTURES-01.json", "data/captures/axn.json", "data/captures/sealed"]
        objs.append({"key": key, "kind": "dataset", "family": "RELEASE", "name": e["slug"], "class": e.get("dataset_class"),
                     "source": paths, "locations": locs, "label": label, "basis": "manifest",
                     "builder": e.get("builder") if e.get("builder") not in (None, "None") else None,
                     "instrument": ("grammar-" + pathlib.Path(e["grammar"]).stem) if e.get("grammar") else None})
    idx = json.loads((ROOT / "data/api/index.json").read_text(encoding="utf-8"))
    for sec in ("protocols", "schemas"):
        for k, x in idx[sec].items():
            path = "data" + x["canonical_path"]
            if not (ROOT / path).is_file():
                continue
            objs.append({"key": f"{sec[:-1]}-{k.replace('_', '-')}", "kind": "instrument", "family": "INSTRUMENT",
                         "name": x.get("name") or k, "source": [path], "locations": [f"{SITE}{x['canonical_path']}"],
                         "label": x.get("current_version"), "basis": "file", "governs": x.get("governs") or x.get("validates")})
    for g in sorted((ROOT / "rhizomes/_grammars").glob("*.json")):
        rel = str(g.relative_to(ROOT))
        objs.append({"key": f"grammar-{g.stem}", "kind": "instrument", "family": "INSTRUMENT", "name": f"rhizome grammar {g.stem}",
                     "source": [rel], "locations": [f"{SITE}/{rel}"], "label": ver_of(rel, "version", "grammar_version"), "basis": "file"})
    objs.append({"key": "capture-intake", "kind": "instrument", "family": "INSTRUMENT",
                 "name": "Capture Registry intake instrument (schema, contract, pipeline, intake and scalar code)",
                 "source": ["rebuild/capture-registry/EA-WG-CAPTURES-01.schema.json", "rebuild/capture-registry/INTAKE-CONTRACT.md",
                            "rebuild/capture-registry/PIPELINE.md", "scripts/capture_intake.py", "scripts/per_scalar.py", "scripts/capture_axn.py"],
                 "locations": [f"{SITE}/rebuild/capture-registry/"], "label": None, "basis": "manifest"})
    objs.append({"key": "per-dim-rubric", "kind": "instrument", "family": "INSTRUMENT",
                 "name": "PER-dim rubric (atom sets, templates and scorers)", "documented_in": 1694,
                 "source": ["data/per-atom-sets.json", "rebuild/capture-registry/per-atoms/templates.json", "scripts/per_dim_score.py", "scripts/per_d_score.py", "scripts/per_dim_write.py", "scripts/per_d_write.py"],
                 "locations": [f"{SITE}/data/per-atom-sets.json"], "label": ver_of("data/per-atom-sets.json", "rubric"), "basis": "manifest"})
    objs.append({"key": "alexanarch", "kind": "site", "family": "SITE", "name": "alexanarch.org",
                 "source": None, "locations": [SITE + "/", GH, "https://huggingface.co/datasets/leesharks/crimson-hexagonal-archive"],
                 "label": None, "basis": "manifest"})
    # the Capture Registry first: the first dataset release (ruled 2026-10-27, "starting with the Capture Registry")
    objs.sort(key=lambda o: 0 if o["key"] == "capture-registry" else 1)
    return objs


HISTORICAL = {"capture-registry": [("data/EA-WG-CAPTURES-01-v8.11.json", "8.11", "2026-07-06"),
                                   ("data/EA-WG-CAPTURES-01-v9.6.json", "9.6", "2026-07-14")]}


def state(o):
    """(sha256, bytes to write as manifest or None, file count, total bytes)"""
    if o["kind"] == "site":
        t = site_tree()
        m = "".join(f"{h}  {p}\n" for p, h, _ in t).encode("utf-8")
        return hashlib.sha256(m).hexdigest(), m, len(t), sum(z for *_, z in t), [p for p, *_ in t]
    paths = [p for s in o["source"] for p in tree(s)]
    if o["basis"] == "file":
        p = paths[0]
        return sha_file(ROOT / p), None, 1, (ROOT / p).stat().st_size, paths
    m = manifest(paths)
    return hashlib.sha256(m).hexdigest(), m, len(set(paths)), sum((ROOT / p).stat().st_size for p in set(paths)), paths


def main():
    apply = "--apply" in sys.argv
    only = set(sys.argv[sys.argv.index("--only") + 1:]) if "--only" in sys.argv else None
    kinds = set(sys.argv[sys.argv.index("--kinds") + 1].split(",")) if "--kinds" in sys.argv else None
    today = datetime.date.today().isoformat()
    led = json.loads(LEDGER.read_text(encoding="utf-8")) if LEDGER.exists() else {
        "_what_this_is": ("The AXN ledger of releases: one position per continuing object (a dataset, an instrument, a site), root "
                          "AXN:<HEX>.<FAMILY>; one AXN per frozen release, AXN:<HEX>.<FAMILY>.<glyphs>, the glyphs derived from the SHA-256 "
                          "of the release's manifest (data/releases/manifests/) or, for a one-file instrument, of the file itself (a copy "
                          "kept in data/releases/frozen/). Continuity is the position, version the release, location where its bytes are had."),
        "ruling": 'Lee Sharks, 2026-10-27: "adopted. lets proceed" — dataset releases, instrument versions, typed relations, site releases.',
        "minted_by": "scripts/release_axn.py", "glyph_table": A.AXN_GLYPH_TABLE, "objects": {}}
    alloc = json.loads(ALLOC.read_text(encoding="utf-8"))
    deps = json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8"))["deposits"]
    nxt = max(int(alloc["next_hex"], 16), max(int(d["hex"], 16) for d in deps if d.get("hex")) + 1, __import__('axn_positions').next_free())  # 2026-10-28: the floor includes origin/main
    new_pos, made, writes = 0, [], []
    for o in objects():
        if only and o["key"] not in only:
            continue
        if kinds and o["kind"] not in kinds:
            continue
        L = led["objects"].get(o["key"])
        if not L:
            hx = f"{nxt:04X}"; nxt += 1; new_pos += 1
            L = led["objects"][o["key"]] = {"hex": hx, "root": f"AXN:{hx}.{o['family']}", "kind": o["kind"], "family": o["family"],
                                            "allocated": today, "releases": []}
        for k in ("name", "class", "source", "locations", "builder", "instrument", "governs", "documented_in"):
            if o.get(k) is not None:
                L[k] = o[k]
        # 2026-10-28: the dataset's wiki (data/releases/wikis.json) travels with its position; the resolver renders it
        _w = (json.loads(WIKIS.read_text(encoding="utf-8")).get("wikis") or {}).get(o["key"]) if WIKIS.exists() else None
        if _w:
            L["wiki"] = _w
        todo = []
        for path, label, date in HISTORICAL.get(o["key"], []):
            m = manifest([path]); h = hashlib.sha256(m).hexdigest()
            todo.append((h, m, 1, (ROOT / path).stat().st_size, [path], label, date, "a copy of this version held in the archive"))
        h, m, n, size, paths = state(o)
        todo.append((h, m, n, size, paths, o.get("label") or today, today, None))
        for h, m, n, size, paths, label, date, note in todo:
            if any(r["sha256"] == h for r in L["releases"]):
                continue
            if any(r["label"] == label for r in L["releases"]):
                # a declared version whose bytes moved without the version moving keeps the version and takes the date;
                # a date label already used that day takes a running number
                label = f"{label}.{sum(1 for r in L['releases'] if r['label'].startswith(label))+1}" if label == today else f"{label}+{today}"
            if any(r["label"] == label for r in L["releases"]):
                label = f"{label}.{len(L['releases'])}"
            slab = re.sub(r"[^A-Za-z0-9._+-]+", "_", label)
            r = {"axn": A.derive_axn(h, L["hex"], o["family"]), "label": label, "date": date, "sha256": h, "basis": o["basis"],
                 "files": n, "bytes": size}
            if m is not None:
                r["manifest"] = f"/data/releases/manifests/{o['key']}/{slab}.sha256"
                writes.append((MANI / o["key"] / f"{slab}.sha256", m))
            else:
                r["file"] = paths[0]
                r["frozen"] = f"/data/releases/frozen/{o['key']}/{slab}/{pathlib.Path(paths[0]).name}"
                writes.append((FROZEN / o["key"] / slab / pathlib.Path(paths[0]).name, (ROOT / paths[0]).read_bytes()))
            if o["kind"] == "site":
                r["base_commit"] = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True).stdout.strip()
            if note:
                r["note"] = note
            L["releases"].append(r); made.append((o["key"], r["axn"], label, n))
        L["releases"].sort(key=lambda r: (r["date"], r["label"]))
    for k, axn, label, n in made:
        print(f"  {k}: {axn}  [{label}]  {n} file(s)")
    print(f"releases: {len(made)} new; {new_pos} new positions (next position {alloc['next_hex']} -> {nxt:04X})")
    if not apply:
        return
    for p, b in writes:
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(b)
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    LEDGER.write_text(json.dumps(led, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    if new_pos:
        alloc["next_hex"] = f"{nxt:04X}"; alloc["last_allocated"] = f"{nxt - 1:04X}"
        alloc["last_allocated_at"] = datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z")
        alloc["last_allocator"] = "releases (scripts/release_axn.py)"
        ALLOC.write_text(json.dumps(alloc, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print("applied")


if __name__ == "__main__":
    main()
