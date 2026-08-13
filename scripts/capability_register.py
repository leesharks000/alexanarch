#!/usr/bin/env python3
"""capability_register.py — the archive remembers what it could do, and refuses less.

═══════════════════════════════════════════════════════════════════════════════
WHY THIS EXISTS
═══════════════════════════════════════════════════════════════════════════════

Two failure modes have repeatedly cost this archive hours of finished work, and
neither is caught by any validator that reads bytes off disk:

  1. SILENT REGRESSION — a fresh instance edits a file, a capability built over
     several sessions stops working, every existing check still passes because
     the bytes are well-formed, and the loss is discovered days later by a human.
     (2026-07-31: one added api/oai.js took 1,012 static files dark for six days.
     Search, the protocol catalog and the DOI resolver were all down the whole
     time while validate_deposit --strict reported zero failures.)

  2. FALSE ERASURE — an instance writes a verification that does not actually
     exercise the capability, reports its impoverished numbers as the whole
     picture, and declares working infrastructure broken. The operator then
     believes finished work has been destroyed.
     (2026-08-06: a "regression test" queried only the metadata tables and
     reported search as reset to zero, while 995 body shards were serving and
     returning 4x more hits than metadata. Nothing was broken. The test was.)

Both are the same disease: NOTHING WAS WATCHING THE CAPABILITY ITSELF.

═══════════════════════════════════════════════════════════════════════════════
THE MECHANISM — A RATCHET, NOT A CHECKLIST
═══════════════════════════════════════════════════════════════════════════════

Every capability declares a probe that measures it live, and a FLOOR: the
minimum measurement that still counts as working. Floors only ever go UP.

  · A run that measures BELOW its floor FAILS. Loudly, with the number, the
    floor, and the date the floor was set. This is the anti-regression gate.

  · A run that measures ABOVE its floor may raise it with --ratchet. The archive
    then refuses to accept less than it has already achieved, ever again.

  · Floors are NEVER lowered by a script. Lowering one is a human decision that
    must be made in a commit message with a reason, so a capability can never be
    quietly abandoned by an instance that found it inconvenient.

Crucially, several probes carry RELATIONAL assertions, not just counts — e.g.
body-search hits MUST exceed metadata-only hits for a known term. A probe that
tests only half a capability therefore fails as loudly as a broken capability,
which is the specific defense against failure mode 2. A test that does not
exercise the thing cannot pass.

Usage:
    python3 scripts/capability_register.py              # verify all, exit 1 on any loss
    python3 scripts/capability_register.py --ratchet    # verify, then raise floors met
    python3 scripts/capability_register.py --only search
"""
import sys, json, re, pathlib, argparse, datetime, urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[1]
BASE = "https://www.alexanarch.org"
REGISTER = ROOT / "data/api/capability-register.json"


def get(path, timeout=60):
    req = urllib.request.Request(BASE + path, headers={"User-Agent": "axn-capability-register"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.headers.get("Content-Type", ""), r.read()


def get_json(path, timeout=60):
    ct, raw = get(path, timeout)
    if "json" not in ct.lower():
        raise AssertionError(f"{path} served as '{ct or 'no content-type'}', expected JSON")
    return json.loads(raw.decode("utf-8", "replace"))


# ── PROBES ────────────────────────────────────────────────────────────────────
# Each returns dict(measure=<number>, detail=<str>) and raises on hard failure.

def probe_body_search():
    """Full-text search over sharded body postings. RELATIONAL: body must beat
    metadata, or the probe is only testing metadata and must fail."""
    man = get_json("/api/body-shards/manifest.json")
    shards = man.get("shard_count", 0)
    assert shards >= 900, f"body shard manifest reports {shards} shards"
    idx = get_json("/api/search-index.json")

    def meta(t):
        o = set()
        for tb in (idx.get("index"), idx.get("series_prefixes"), idx.get("keywords"),
                   idx.get("creators"), idx.get("content_types"), idx.get("hex_labels")):
            if tb and tb.get(t):
                o.update(tb[t])
        return o

    def body(t):
        p = (re.sub(r"[^a-z0-9]", "", t[:2].lower()) + "_")[:2] or "__"
        return set(get_json(f"/api/body-shards/{p}.json").get(t, []))

    total = 0
    for term in ("sappho", "symbolon", "tachyon"):
        m, b = meta(term), body(term)
        assert b, f"'{term}' returned ZERO body hits — full-text search is not working"
        assert len(b) > len(m), (
            f"'{term}': body {len(b)} <= metadata {len(m)}. Full-text search must return "
            f"MORE than metadata alone; if it does not, either the shards are degraded or "
            f"this probe is only exercising metadata — the 2026-08-06 false-erasure failure.")
        total += len(b)
    return {"measure": total, "detail": f"{shards} shards; body hits across 3 control terms"}


def probe_metadata_search():
    """All six metadata tables must be present and populated."""
    idx = get_json("/api/search-index.json")
    need = ["index", "series_prefixes", "keywords", "creators", "content_types", "hex_labels"]
    missing = [k for k in need if not idx.get(k)]
    assert not missing, f"search index missing populated tables: {missing}"
    return {"measure": len(idx["index"]), "detail": f"{len(need)} tables; generic tokens"}


def probe_doi_resolution():
    """The map standing in for severed Zenodo DOIs."""
    m = get_json("/api/doi-axn-map.json")["map"]
    sample = next(iter(m))
    assert m[sample], f"DOI {sample} maps to an empty record"
    return {"measure": len(m), "detail": "DOI to AXN mappings"}


def probe_oai():
    """OAI-PMH must be executing, not merely present in the repo."""
    ok = 0
    for verb in ("Identify", "ListMetadataFormats", "ListSets"):
        ct, raw = get(f"/oai?verb={verb}")
        s = raw.decode("utf-8", "replace")
        assert "xml" in ct.lower(), f"{verb} served as {ct}"
        assert "<OAI-PMH" in s and "<error" not in s, f"{verb} returned an OAI error envelope"
        ok += 1
    ct, raw = get("/oai?verb=ListIdentifiers&metadataPrefix=oai_dc")
    ids = len(re.findall(r"<identifier>", raw.decode("utf-8", "replace")))
    assert ids > 0, "ListIdentifiers returned no identifiers"
    return {"measure": ok * 1000 + ids, "detail": f"{ok} verbs valid; {ids} ids in first page"}


def probe_static_publication():
    """Every advertised machine endpoint returns parseable JSON."""
    eps = json.loads((ROOT / "data/api/endpoint-contract.json").read_text())["endpoints"]
    for ep in eps:
        doc = get_json(ep["path"])
        k = ep.get("must_contain_key")
        assert not k or k in doc, f"{ep['path']} missing required key '{k}'"
    return {"measure": len(eps), "detail": "contracted endpoints serving JSON"}


def probe_record_pages():
    """Human record surfaces render with their identifier.

    PROBES THE NEWEST *PUBLISHED* DEPOSIT, NOT deps[-1]. This gate runs BEFORE
    git push, so at commit time deps[-1] is the deposit being committed and its
    page cannot be live yet — the probe would 404 on a healthy archive and halt
    a correct commit. That is what happened on #1457.

    The gate exists to catch REGRESSION in capability that already existed.
    Verifying the NEW deposit's page is stage_verify's job, after the push and
    the deploy wait. So this asks the last deposit that had a chance to deploy.
    """
    reg = json.loads((ROOT / "data/registry.json").read_text())
    deps = reg["deposits"]
    published = deps[-2] if len(deps) > 1 else deps[-1]
    n = published["deposit_number"]
    axn = published["axn"]
    ct, raw = get(f"/s/records/{n}/")
    s = raw.decode("utf-8", "replace")
    assert axn.split(".")[0] in s, f"record #{n} does not carry its AXN"
    return {"measure": len(deps), "detail": f"registry deposits; #{n} verified rendering"}


def probe_symbolon_store():
    """Stored sealed cores verify against their kernels and are mirrorable."""
    man = get_json("/data/symbolon-registry/MANIFEST.json")
    cores = man.get("cores", [])
    assert man.get("integrity_alerts", 1) == 0, "symbolon store reports integrity alerts"
    for c in cores:
        assert c.get("sha256") and c.get("bytes"), f"core {c.get('position')} lacks hash or length"
    return {"measure": len(cores), "detail": "sealed cores with published hash and length"}


def probe_resourcesync():
    """Harvesters can find and verify content without asking."""
    ct, raw = get("/resourcesync/resourcelist.xml")
    s = raw.decode("utf-8", "replace")
    hashed = len(re.findall(r'hash="sha-256:', s))
    urls = len(re.findall(r"<url>", s))
    assert hashed > 0, "resourcelist publishes no verifiable hashes"
    return {"measure": urls, "detail": f"resources listed; {hashed} with verifiable hashes"}


def probe_browse_filter():
    """Browse: complete static list AND a working filter. Both, or neither counts.
    RELATIONAL: the static rows must survive the filter's presence — a filter that
    replaced the list would break crawlers and archival capture."""
    ct, raw = get("/s/browse/")
    s = raw.decode("utf-8", "replace")
    rows = len(re.findall(r'href="/s/records/\d+/"', s))
    assert rows > 1000, f"browse lists only {rows} records — the static list is the point"
    assert "axnflt" in s, "browse has no filter widget"
    assert "search every deposit" in s, "browse filter does not route onward to full-text search"
    # FUNCTION, not presence. The previous probe passed while the widget was
    # destroying the page: it assigned style.display='' on match, which strips the
    # inline display:block these rows carry, collapsing 1,434 stacked rows into one
    # inline run at load. A probe that only checks the widget EXISTS would have
    # reported this capability healthy forever.
    assert "__disp" in s, ("browse filter does not preserve each row's original display value "
                           "— assigning '' strips inline display:block and breaks the page")
    assert "display = ok ? ''" not in s, "browse filter reintroduces the display-stripping bug"
    return {"measure": rows, "detail": "static rows, with filter present"}


def probe_wiki():
    """Wiki: complete static entry list AND a filter, on the page the LAST
    generator writes. A filter here was once silently overwritten."""
    ct, raw = get("/s/wiki/")
    s = raw.decode("utf-8", "replace")
    rows = len(re.findall(r'class="entry-row"', s))
    assert rows > 1000, f"wiki lists only {rows} entries"
    assert "axnflt" in s, ("wiki has no filter widget — it was previously destroyed by "
                           "publish_wiki_entries.py rewriting the page after it was added")
    assert "__disp" in s, "wiki filter does not preserve each row's original display value"
    return {"measure": rows, "detail": "static entries, with filter present"}


def probe_stamp_page():
    """The instrument itself: client-side stamping and verification must be served."""
    ct, raw = get("/mint/stamp/")
    s = raw.decode("utf-8", "replace")
    for needle, why in [("AXN_GLYPHS", "the glyph table"),
                        ("crypto.subtle.digest", "client-side hashing"),
                        ("axn-central-registry.json", "the verify lookup"),
                        ("pdf-lib", "PDF stamping")]:
        assert needle in s, f"stamp page missing {why} ({needle})"
    return {"measure": len(s), "detail": "stamp+verify page bytes with all four capabilities"}


def probe_lexical():
    """The minted-term surface."""
    d = get_json("/data/lexical-minting-registry.json", timeout=90)
    terms = d.get("terms") or []
    assert len(terms) > 5000, f"lexical registry holds only {len(terms)} terms"
    return {"measure": len(terms), "detail": "minted lexical terms"}


def probe_axn_resolver():
    """Every hex position resolves to a page carrying its full AXN."""
    # Same reason as probe_record_pages: the newest deposit is not yet pushed
    # when this gate runs, so the resolver page for its hex cannot exist.
    reg = json.loads((ROOT / "data/registry.json").read_text())
    deps = reg["deposits"]
    d = deps[-2] if len(deps) > 1 else deps[-1]
    ct, raw = get(f"/s/axn/{d['hex']}/")
    s = raw.decode("utf-8", "replace")
    assert d["axn"] in s, f"resolver page for {d['hex']} does not carry the full AXN"
    return {"measure": 1, "detail": f"{d['hex']} resolves with full form"}


def probe_node_declaration():
    """The federation declaration must match live registry state. Generating it is
    not enough: a generator with a bug would automate the lie instead of ending it,
    so this compares PUBLISHED values against the PUBLISHED registry."""
    d = get_json("/.well-known/axn-node.json")
    reg = get_json("/data/registry.json", timeout=120)
    deps = reg["deposits"] if isinstance(reg, dict) else reg
    actual = len(deps)
    declared = d.get("deposit_count")
    assert declared == actual, (
        f"node declaration advertises {declared} deposits, registry holds {actual} "
        f"— divergence {abs(actual - (declared or 0))}. This is F1: a root node lying "
        f"about its own state is how a federation silently diverges.")
    assert d.get("registry_head"), "declaration carries no registry_head"
    return {"measure": actual, "detail": "declared deposit_count == live registry"}


PROBES = {
    "body-search": probe_body_search,
    "metadata-search": probe_metadata_search,
    "doi-resolution": probe_doi_resolution,
    "oai-pmh": probe_oai,
    "static-publication": probe_static_publication,
    "record-pages": probe_record_pages,
    "symbolon-store": probe_symbolon_store,
    "resourcesync": probe_resourcesync,
    "browse-filter": probe_browse_filter,
    "wiki": probe_wiki,
    "stamp-page": probe_stamp_page,
    "lexical": probe_lexical,
    "axn-resolver": probe_axn_resolver,
    "node-declaration": probe_node_declaration,
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ratchet", action="store_true",
                    help="raise floors to today's measurements where they were met")
    ap.add_argument("--only", help="run one capability")
    a = ap.parse_args()

    reg = json.loads(REGISTER.read_text()) if REGISTER.exists() else {
        "description": "Declared capabilities with measured floors. Floors only rise.",
        "capabilities": {}}
    caps = reg["capabilities"]
    today = datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d")
    lost, held, raised = [], [], []

    for name, probe in PROBES.items():
        if a.only and a.only != name:
            continue
        entry = caps.setdefault(name, {"floor": 0, "floor_set": today, "detail": ""})
        try:
            r = probe()
        except Exception as e:
            lost.append(f"{name}: PROBE FAILED — {type(e).__name__}: {e}")
            continue
        m, floor = r["measure"], entry.get("floor", 0)
        if m < floor:
            lost.append(f"{name}: MEASURED {m}, FLOOR {floor} (set {entry.get('floor_set')}) "
                        f"— {floor - m} LOST. {r['detail']}")
            continue
        held.append(f"{name}: {m} (floor {floor}) — {r['detail']}")
        if a.ratchet and m > floor:
            entry.update(floor=m, floor_set=today, detail=r["detail"])
            raised.append(f"{name}: {floor} → {m}")
        entry["last_measured"] = m
        entry["last_checked"] = today

    for h in held:
        print(f"  ok    {h}")
    for r in raised:
        print(f"  ↑     ratcheted {r}")
    for l in lost:
        print(f"  LOST  {l}", file=sys.stderr)

    if a.ratchet and not lost:
        reg["updated"] = today
        REGISTER.write_text(json.dumps(reg, ensure_ascii=False, indent=1))

    if lost:
        print("\n" + "=" * 76, file=sys.stderr)
        print("CAPABILITY LOSS. Work that existed no longer does.", file=sys.stderr)
        print("Do not commit through this. Restore the capability, or — if the loss is",
              file=sys.stderr)
        print("deliberate — lower the floor BY HAND in data/api/capability-register.json",
              file=sys.stderr)
        print("and say why in the commit message. No script may lower a floor.",
              file=sys.stderr)
        print("=" * 76, file=sys.stderr)
        return 1
    print(f"\nALL CAPABILITIES HELD ({len(held)} verified)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
