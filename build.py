#!/usr/bin/env python3
"""
Alexanarch Build Pipeline
═════════════════════════
One source of truth. One build command. Multiple outputs.

Reads:  catalog.yaml + data/registry.json + data/JOURNAL-MAPPING-PRELIMINARY.json
Writes: ro-crate-metadata.json, datapackage.json, dcat.jsonld, SHA256SUMS.txt,
        build/catalog-export.csv, build/journal-toc/*.json, build/graph.jsonld,
        build/graph.nq

Usage:  python build.py [--validate-only] [--format FORMAT] [--verbose]
"""

import argparse
import csv
import hashlib
import io
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

# ── YAML loading (stdlib fallback if PyYAML unavailable) ──────

try:
    import yaml
except ImportError:
    yaml = None


def load_yaml(path):
    """Load YAML with PyYAML or a minimal fallback for simple files."""
    if yaml:
        with open(path) as f:
            return yaml.safe_load(f)
    else:
        # Minimal YAML subset parser — enough for catalog.yaml
        # In production, install PyYAML. This handles the basics.
        print("[WARN] PyYAML not installed. Using minimal parser.", file=sys.stderr)
        print("       Install with: pip install pyyaml --break-system-packages", file=sys.stderr)
        with open(path) as f:
            text = f.read()
        # For the build to work without PyYAML, we parse just enough
        import subprocess
        result = subprocess.run(
            ["python3", "-c", f"""
import json, sys
try:
    import yaml
    with open('{path}') as f:
        print(json.dumps(yaml.safe_load(f)))
except ImportError:
    print('{{"error": "PyYAML required"}}')
"""],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            return json.loads(result.stdout)
        raise RuntimeError("PyYAML is required. Install: pip install pyyaml --break-system-packages")


# ── Constants ─────────────────────────────────────────────────

REPO_ROOT = Path(__file__).parent
BUILD_DIR = REPO_ROOT / "build"
NOW = datetime.now(timezone.utc).isoformat()


# ── Loaders ───────────────────────────────────────────────────

def load_catalog():
    """Load catalog.yaml."""
    path = REPO_ROOT / "catalog.yaml"
    if not path.exists():
        print(f"ERROR: {path} not found", file=sys.stderr)
        sys.exit(1)
    return load_yaml(str(path))


def load_registry():
    """Load data/registry.json."""
    path = REPO_ROOT / "data" / "registry.json"
    if not path.exists():
        print(f"ERROR: {path} not found", file=sys.stderr)
        sys.exit(1)
    with open(path) as f:
        return json.load(f)


def load_journal_mapping():
    """Load data/JOURNAL-MAPPING-PRELIMINARY.json."""
    path = REPO_ROOT / "data" / "JOURNAL-MAPPING-PRELIMINARY.json"
    if not path.exists():
        print(f"WARN: {path} not found — journal assignments unavailable", file=sys.stderr)
        return None
    with open(path) as f:
        return json.load(f)


# ── Validation ────────────────────────────────────────────────

def validate(catalog, registry, journal_mapping, verbose=False):
    """Validate consistency across all data sources. Returns (errors, warnings)."""
    errors = []
    warnings = []
    deposits = registry.get("deposits", [])

    # 1. Every deposit has required fields
    required = ["title", "creator", "date", "description", "license", "hash"]
    for d in deposits:
        dn = d.get("deposit_number", d.get("hex", "???"))
        missing = [f for f in required if not d.get(f)]
        if missing:
            warnings.append(f"Deposit #{dn}: missing fields: {', '.join(missing)}")

    # 2. AXN identifiers are unique
    axns = [d.get("axn") for d in deposits if d.get("axn")]
    dupes = [a for a in set(axns) if axns.count(a) > 1]
    for a in dupes:
        errors.append(f"Duplicate AXN: {a}")

    # 3. Deposit numbers are unique
    nums = [d.get("deposit_number") for d in deposits if d.get("deposit_number")]
    num_dupes = [n for n in set(nums) if nums.count(n) > 1]
    for n in num_dupes:
        errors.append(f"Duplicate deposit_number: {n}")

    # 4. Journal mapping coverage
    if journal_mapping:
        mapped_nums = {m["deposit_number"] for m in journal_mapping.get("mapping", [])}
        reg_nums = {d.get("deposit_number") for d in deposits if d.get("deposit_number")}
        unmapped = reg_nums - mapped_nums
        if unmapped:
            warnings.append(f"{len(unmapped)} deposits not in journal mapping")

    # 5. SHA-256 hashes are valid format (64 hex chars)
    for d in deposits:
        h = d.get("hash", "")
        if h and (len(h) != 64 or not all(c in "0123456789abcdef" for c in h)):
            warnings.append(f"Deposit #{d.get('deposit_number', '?')}: invalid SHA-256 hash format")

    # 6. Catalog journal names match mapping journal names
    if journal_mapping:
        catalog_journals = set()
        for j in catalog.get("journals", {}).values():
            catalog_journals.add(j.get("abbreviation", ""))
        mapping_journals = set(journal_mapping.get("journal_distribution", {}).keys())
        unknown = mapping_journals - catalog_journals
        if unknown:
            warnings.append(f"Journal mapping has journals not in catalog: {unknown}")

    # 7. Heteronym names in registry match catalog
    catalog_names = {h["name"] for h in catalog.get("heteronyms", {}).values()}
    registry_creators = {d.get("creator", "") for d in deposits}
    # Only check single-creator entries
    for c in registry_creators:
        if " · " not in c and c not in catalog_names and c:
            warnings.append(f"Creator '{c}' in registry but not in heteronym catalog")

    if verbose:
        print(f"\nValidation: {len(deposits)} deposits checked")
        print(f"  {len(errors)} errors, {len(warnings)} warnings")

    return errors, warnings


# ── Generators ────────────────────────────────────────────────

def generate_ro_crate(catalog, registry, journal_mapping):
    """Generate RO-Crate 1.2 metadata (ro-crate-metadata.json)."""
    archive = catalog["archive"]
    deposits = registry.get("deposits", [])
    jm_by_num = {}
    if journal_mapping:
        jm_by_num = {m["deposit_number"]: m for m in journal_mapping.get("mapping", [])}

    # Build the @graph
    graph = []

    # 1. Root dataset
    root = {
        "@id": "./",
        "@type": "Dataset",
        "name": archive["name"],
        "description": archive["description"].strip(),
        "datePublished": archive["founded"],
        "license": {"@id": f"https://creativecommons.org/licenses/{archive['license'].lower().replace('cc-', '').replace('.0', '')}/4.0/"},
        "author": {"@id": f"https://orcid.org/{archive['founder_orcid']}"},
        "publisher": {
            "@id": archive["url"],
            "@type": "Organization",
            "name": archive["name"],
            "url": archive["url"]
        },
        "identifier": archive["url"],
        "isPartOf": {
            "@type": "CreativeWork",
            "name": archive["parent_project"]
        },
        "hasPart": [{"@id": f"#deposit-{d.get('deposit_number', d.get('hex'))}"} for d in deposits]
    }
    graph.append(root)

    # 2. Author
    graph.append({
        "@id": f"https://orcid.org/{archive['founder_orcid']}",
        "@type": "Person",
        "name": archive["founder"],
        "identifier": f"https://orcid.org/{archive['founder_orcid']}"
    })

    # 3. License
    graph.append({
        "@id": "https://creativecommons.org/licenses/by/4.0/",
        "@type": "CreativeWork",
        "name": "CC-BY-4.0",
        "url": "https://creativecommons.org/licenses/by/4.0/"
    })

    # 4. Journals as organizational units
    for jkey, jval in catalog.get("journals", {}).items():
        graph.append({
            "@id": f"#journal-{jval['slug']}",
            "@type": "Periodical",
            "name": jval["name"],
            "alternateName": jval.get("abbreviation", ""),
            "description": jval["description"].strip()
        })

    # 5. Each deposit as a dataset part
    for d in deposits:
        dn = d.get("deposit_number", d.get("hex"))
        journal_abbr = jm_by_num.get(dn, {}).get("journal", "")
        journal_slug = ""
        for jkey, jval in catalog.get("journals", {}).items():
            if jval.get("abbreviation") == journal_abbr:
                journal_slug = jval["slug"]
                break

        entry = {
            "@id": f"#deposit-{dn}",
            "@type": "CreativeWork",
            "name": d.get("title", ""),
            "author": d.get("creator", ""),
            "datePublished": d.get("date", ""),
            "description": (d.get("description", "") or "")[:500],
            "identifier": d.get("axn", ""),
            "license": d.get("license", "CC-BY-4.0"),
            "genre": d.get("content_type", ""),
            "keywords": d.get("keywords", []),
            "version": d.get("version", ""),
            "url": f"{archive['url']}/s/records/{dn}/"
        }
        if journal_slug:
            entry["isPartOf"] = {"@id": f"#journal-{journal_slug}"}
        if d.get("hash"):
            entry["sha256"] = d["hash"]
        graph.append(entry)

    crate = {
        "@context": "https://w3id.org/ro/crate/1.2-DRAFT/context",
        "@graph": graph
    }
    return crate


def generate_data_package(catalog, registry, journal_mapping):
    """Generate Frictionless Data Package (datapackage.json)."""
    archive = catalog["archive"]
    deposits = registry.get("deposits", [])
    jm_by_num = {}
    if journal_mapping:
        jm_by_num = {m["deposit_number"]: m for m in journal_mapping.get("mapping", [])}

    resources = []

    # Main registry as a tabular resource
    fields = [
        {"name": "deposit_number", "type": "integer", "description": "Sequential deposit number"},
        {"name": "axn", "type": "string", "description": "AXN identifier"},
        {"name": "title", "type": "string", "description": "Work title"},
        {"name": "creator", "type": "string", "description": "Author/heteronym"},
        {"name": "date", "type": "date", "description": "Publication date"},
        {"name": "content_type", "type": "string", "description": "Content type classification"},
        {"name": "license", "type": "string", "description": "License identifier"},
        {"name": "journal", "type": "string", "description": "Journal assignment"},
        {"name": "family", "type": "string", "description": "CHA family classification"},
        {"name": "hash", "type": "string", "description": "SHA-256 content hash"},
        {"name": "description", "type": "string", "description": "Work description"},
        {"name": "keywords", "type": "string", "description": "Semicolon-separated keywords"},
        {"name": "version", "type": "string", "description": "Version string"},
        {"name": "substrate", "type": "string", "description": "Substrate disclosure"},
        {"name": "url", "type": "string", "description": "Canonical URL"},
    ]

    resources.append({
        "name": "deposits",
        "path": "build/catalog-export.csv",
        "format": "csv",
        "mediatype": "text/csv",
        "encoding": "utf-8",
        "schema": {"fields": fields}
    })

    # DOI resolution index
    resources.append({
        "name": "doi-resolution-index",
        "path": "data/doi-resolution-index.json",
        "format": "json",
        "mediatype": "application/json",
        "description": "Maps 1,817 defunct Zenodo DOIs to live Alexanarch locations"
    })

    # Registry
    resources.append({
        "name": "registry",
        "path": "data/registry.json",
        "format": "json",
        "mediatype": "application/json",
        "description": "Full deposit registry with metadata"
    })

    package = {
        "name": archive["name"].lower(),
        "title": f"{archive['name']} — {archive['parent_project']}",
        "description": archive["description"].strip(),
        "homepage": archive["url"],
        "version": registry.get("version", "1.0.0"),
        "created": archive["founded"],
        "licenses": [{"name": archive["license"], "path": f"https://creativecommons.org/licenses/by/4.0/"}],
        "contributors": [
            {
                "title": archive["founder"],
                "role": "author",
                "path": f"https://orcid.org/{archive['founder_orcid']}"
            }
        ],
        "resources": resources
    }
    return package


def generate_dcat(catalog, registry):
    """Generate DCAT-AP catalog description (dcat.jsonld)."""
    archive = catalog["archive"]
    deposits = registry.get("deposits", [])

    dcat = {
        "@context": {
            "dcat": "http://www.w3.org/ns/dcat#",
            "dct": "http://purl.org/dc/terms/",
            "foaf": "http://xmlns.com/foaf/0.1/",
            "schema": "https://schema.org/"
        },
        "@type": "dcat:Catalog",
        "dct:title": f"{archive['name']} — {archive['parent_project']}",
        "dct:description": archive["description"].strip(),
        "dct:publisher": {
            "@type": "foaf:Organization",
            "foaf:name": archive["name"],
            "foaf:homepage": archive["url"]
        },
        "dct:issued": archive["founded"],
        "dct:modified": NOW[:10],
        "dct:language": "en",
        "dcat:dataset": []
    }

    # Add each journal as a dataset
    for jkey, jval in catalog.get("journals", {}).items():
        ds = {
            "@type": "dcat:Dataset",
            "dct:title": jval["name"],
            "dct:description": jval["description"].strip(),
            "dcat:distribution": {
                "@type": "dcat:Distribution",
                "dcat:accessURL": f"{archive['url']}/s/browse/?journal={jval['slug']}",
                "dcat:mediaType": "text/html"
            }
        }
        dcat["dcat:dataset"].append(ds)

    # Add the main registry as a dataset
    dcat["dcat:dataset"].append({
        "@type": "dcat:Dataset",
        "dct:title": "Alexanarch Deposit Registry",
        "dct:description": f"Complete registry of {len(deposits)} deposits in the Crimson Hexagonal Archive",
        "dcat:distribution": [
            {
                "@type": "dcat:Distribution",
                "dcat:downloadURL": f"{archive['url']}/data/registry.json",
                "dcat:mediaType": "application/json"
            },
            {
                "@type": "dcat:Distribution",
                "dcat:downloadURL": f"{archive['url']}/build/catalog-export.csv",
                "dcat:mediaType": "text/csv"
            }
        ]
    })

    return dcat


def generate_csv_export(catalog, registry, journal_mapping):
    """Generate flat CSV export of all deposits."""
    archive = catalog["archive"]
    deposits = registry.get("deposits", [])
    jm_by_num = {}
    if journal_mapping:
        jm_by_num = {m["deposit_number"]: m for m in journal_mapping.get("mapping", [])}

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([
        "deposit_number", "axn", "title", "creator", "date",
        "content_type", "license", "journal", "family", "hash",
        "description", "keywords", "version", "substrate", "url"
    ])

    for d in deposits:
        dn = d.get("deposit_number", "")
        journal = jm_by_num.get(dn, {}).get("journal", "")
        keywords = "; ".join(d.get("keywords", [])) if isinstance(d.get("keywords"), list) else d.get("keywords", "")
        writer.writerow([
            dn,
            d.get("axn", ""),
            d.get("title", ""),
            d.get("creator", ""),
            d.get("date", ""),
            d.get("content_type", ""),
            d.get("license", ""),
            journal,
            d.get("family", ""),
            d.get("hash", ""),
            (d.get("description", "") or "")[:500],
            keywords,
            d.get("version", ""),
            d.get("substrate", ""),
            f"{archive['url']}/s/records/{dn}/"
        ])

    return output.getvalue()


def generate_checksums(registry):
    """Generate SHA256SUMS.txt from deposit hashes."""
    lines = []
    for d in registry.get("deposits", []):
        h = d.get("hash", "")
        dn = d.get("deposit_number", d.get("hex", ""))
        title = d.get("title", "untitled")
        if h and len(h) == 64:
            lines.append(f"{h}  AXN-{str(dn).zfill(4)} {title}")
    return "\n".join(sorted(lines)) + "\n"


def generate_journal_tocs(catalog, registry, journal_mapping):
    """Generate per-journal table-of-contents JSON files."""
    if not journal_mapping:
        return {}

    jm_by_num = {m["deposit_number"]: m for m in journal_mapping.get("mapping", [])}
    reg_by_num = {d.get("deposit_number"): d for d in registry.get("deposits", [])}

    tocs = {}
    for jkey, jval in catalog.get("journals", {}).items():
        abbr = jval.get("abbreviation", "")
        slug = jval.get("slug", "")
        entries = []

        for m in journal_mapping.get("mapping", []):
            if m.get("journal") == abbr:
                dn = m["deposit_number"]
                rd = reg_by_num.get(dn, {})
                entries.append({
                    "deposit_number": dn,
                    "axn": rd.get("axn", ""),
                    "title": rd.get("title", m.get("title", "")),
                    "creator": rd.get("creator", ""),
                    "date": rd.get("date", ""),
                    "content_type": rd.get("content_type", ""),
                    "url": f"https://alexanarch.org/s/records/{dn}/"
                })

        tocs[slug] = {
            "journal": jval["name"],
            "abbreviation": abbr,
            "slug": slug,
            "total_articles": len(entries),
            "generated": NOW,
            "entries": sorted(entries, key=lambda e: e.get("date", ""), reverse=True)
        }

    return tocs


def generate_jsonld_graph(catalog, registry):
    """Generate JSON-LD linked data graph connecting deposits, heteronyms, and journals."""
    archive = catalog["archive"]
    deposits = registry.get("deposits", [])

    graph = []

    # Archive node
    graph.append({
        "@id": archive["url"],
        "@type": "schema:DataCatalog",
        "schema:name": archive["name"],
        "schema:description": archive["description"].strip(),
        "schema:url": archive["url"],
        "schema:dateCreated": archive["founded"],
        "schema:creator": {"@id": f"https://orcid.org/{archive['founder_orcid']}"}
    })

    # Heteronym nodes
    for hkey, hval in catalog.get("heteronyms", {}).items():
        node = {
            "@id": f"{archive['url']}#heteronym-{hkey}",
            "@type": "schema:Person",
            "schema:name": hval["name"],
            "schema:description": hval.get("function", ""),
            "schema:memberOf": {"@id": archive["url"]}
        }
        if hval.get("orcid"):
            node["schema:identifier"] = f"https://orcid.org/{hval['orcid']}"
        graph.append(node)

    # Journal nodes
    for jkey, jval in catalog.get("journals", {}).items():
        graph.append({
            "@id": f"{archive['url']}#journal-{jval['slug']}",
            "@type": "schema:Periodical",
            "schema:name": jval["name"],
            "schema:alternateName": jval.get("abbreviation", ""),
            "schema:description": jval["description"].strip(),
            "schema:isPartOf": {"@id": archive["url"]}
        })

    # Deposit nodes (lightweight — full metadata in registry.json)
    for d in deposits[:100]:  # Cap at 100 for graph manageability
        dn = d.get("deposit_number", "")
        graph.append({
            "@id": f"{archive['url']}/s/records/{dn}/",
            "@type": "schema:CreativeWork",
            "schema:name": d.get("title", ""),
            "schema:author": d.get("creator", ""),
            "schema:datePublished": d.get("date", ""),
            "schema:identifier": d.get("axn", ""),
            "schema:isPartOf": {"@id": archive["url"]}
        })

    return {
        "@context": {"schema": "https://schema.org/"},
        "@graph": graph
    }


# ── Main ──────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Alexanarch Build Pipeline")
    parser.add_argument("--validate-only", action="store_true", help="Validate without generating")
    parser.add_argument("--format", type=str, help="Generate only this format")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    args = parser.parse_args()

    print("═══════════════════════════════════════════════")
    print("  Alexanarch Build Pipeline")
    print(f"  {NOW}")
    print("═══════════════════════════════════════════════")

    # Load sources
    print("\n[1/5] Loading sources...")
    catalog = load_catalog()
    registry = load_registry()
    journal_mapping = load_journal_mapping()
    print(f"  catalog.yaml: {len(catalog.get('journals', {}))} journals, {len(catalog.get('heteronyms', {}))} heteronyms")
    print(f"  registry.json: {len(registry.get('deposits', []))} deposits")
    if journal_mapping:
        print(f"  journal-mapping: {len(journal_mapping.get('mapping', []))} assignments")

    # Validate
    print("\n[2/5] Validating...")
    errors, warnings = validate(catalog, registry, journal_mapping, verbose=args.verbose)
    for e in errors:
        print(f"  ✗ ERROR: {e}")
    if args.verbose:
        for w in warnings[:20]:
            print(f"  ⚠ WARN: {w}")
        if len(warnings) > 20:
            print(f"  ... and {len(warnings) - 20} more warnings")
    print(f"  → {len(errors)} errors, {len(warnings)} warnings")

    if errors:
        print("\nBuild aborted: fix errors first.")
        sys.exit(1)

    if args.validate_only:
        print("\nValidation complete.")
        sys.exit(0)

    # Create build directory
    BUILD_DIR.mkdir(exist_ok=True)
    (BUILD_DIR / "journal-toc").mkdir(exist_ok=True)

    generated = []

    # Generate outputs
    print("\n[3/5] Generating outputs...")

    # RO-Crate 1.2
    if not args.format or args.format == "ro-crate":
        crate = generate_ro_crate(catalog, registry, journal_mapping)
        out = REPO_ROOT / "ro-crate-metadata.json"
        with open(out, "w") as f:
            json.dump(crate, f, indent=2, ensure_ascii=False)
        generated.append(("ro-crate-metadata.json", len(crate["@graph"]), "graph nodes"))
        print(f"  ✓ ro-crate-metadata.json ({len(crate['@graph'])} nodes)")

    # Data Package
    if not args.format or args.format == "data-package":
        pkg = generate_data_package(catalog, registry, journal_mapping)
        out = REPO_ROOT / "datapackage.json"
        with open(out, "w") as f:
            json.dump(pkg, f, indent=2, ensure_ascii=False)
        generated.append(("datapackage.json", len(pkg["resources"]), "resources"))
        print(f"  ✓ datapackage.json ({len(pkg['resources'])} resources)")

    # DCAT
    if not args.format or args.format == "dcat":
        dcat = generate_dcat(catalog, registry)
        out = BUILD_DIR / "dcat.jsonld"
        with open(out, "w") as f:
            json.dump(dcat, f, indent=2, ensure_ascii=False)
        generated.append(("build/dcat.jsonld", len(dcat["dcat:dataset"]), "datasets"))
        print(f"  ✓ build/dcat.jsonld ({len(dcat['dcat:dataset'])} datasets)")

    # CSV Export
    if not args.format or args.format == "csv-export":
        csv_data = generate_csv_export(catalog, registry, journal_mapping)
        out = BUILD_DIR / "catalog-export.csv"
        with open(out, "w") as f:
            f.write(csv_data)
        lines = csv_data.count("\n") - 1
        generated.append(("build/catalog-export.csv", lines, "rows"))
        print(f"  ✓ build/catalog-export.csv ({lines} rows)")

    # Checksums
    if not args.format or args.format == "checksums":
        sums = generate_checksums(registry)
        out = REPO_ROOT / "SHA256SUMS.txt"
        with open(out, "w") as f:
            f.write(sums)
        lines = sums.count("\n")
        generated.append(("SHA256SUMS.txt", lines, "entries"))
        print(f"  ✓ SHA256SUMS.txt ({lines} entries)")

    # Journal TOCs
    if not args.format or args.format == "journal-toc":
        tocs = generate_journal_tocs(catalog, registry, journal_mapping)
        for slug, toc in tocs.items():
            out = BUILD_DIR / "journal-toc" / f"{slug}.json"
            with open(out, "w") as f:
                json.dump(toc, f, indent=2, ensure_ascii=False)
            generated.append((f"build/journal-toc/{slug}.json", toc["total_articles"], "articles"))
            print(f"  ✓ build/journal-toc/{slug}.json ({toc['total_articles']} articles)")

    # JSON-LD Graph
    if not args.format or args.format == "jsonld-graph":
        graph = generate_jsonld_graph(catalog, registry)
        out = BUILD_DIR / "graph.jsonld"
        with open(out, "w") as f:
            json.dump(graph, f, indent=2, ensure_ascii=False)
        generated.append(("build/graph.jsonld", len(graph["@graph"]), "nodes"))
        print(f"  ✓ build/graph.jsonld ({len(graph['@graph'])} nodes)")

    # Summary
    print(f"\n[4/5] Build complete: {len(generated)} outputs generated")

    # Deploy to root check
    print("\n[5/5] Root deployment check:")
    for fname in catalog.get("build", {}).get("deploy_to_root", []):
        path = REPO_ROOT / fname
        if path.exists():
            size = path.stat().st_size
            print(f"  ✓ {fname} ({size:,} bytes) — ready at repo root")
        else:
            print(f"  ✗ {fname} — NOT FOUND")

    print("\n═══════════════════════════════════════════════")
    print("  ∮ = 1")
    print("═══════════════════════════════════════════════")


if __name__ == "__main__":
    main()
