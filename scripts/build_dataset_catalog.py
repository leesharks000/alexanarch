#!/usr/bin/env python3
"""build_dataset_catalog.py — the dataset fleet inventory, generated from what builds it.

WHY GENERATED (2026-09-28). datasets/set.json is hand-maintained. On 2026-09-28 it was
still v1.4 of 2026-07-25: eleven members, and none of the September datasets — the
rhizomes, Negative of the Negative, The Final Time, Tiger Leap, the argument-as-dataset.
Meanwhile the Semantic Economy body had last been emitted on 2026-09-16 and did not
contain the deposits (#1631, #1634) that extended it. A hand-kept inventory drifts
silently; a conceptual dataset then looks live while it is a snapshot.

This catalog is read off the publishing workflows (.github/workflows/hf-*.yml), the
rhizome grammars, the dataset directories and git. Every field says where it came from.

FRESHNESS IS RECORDED, NOT ENFORCED. Each entry carries the date its source last changed
and, where the body has dated nodes, how far its latest node trails the registry's
latest deposit. Nothing here fails a build: a stale dataset is data about the fleet.

    python3 scripts/build_dataset_catalog.py        # writes datasets/catalog.json
"""
import json, pathlib, re, subprocess, datetime

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "datasets" / "catalog.json"
HUB = "https://huggingface.co/datasets/"


def git_last(path):
    try:
        out = subprocess.run(["git", "log", "-1", "--format=%H %cI", "--", str(path)], cwd=ROOT,
                             capture_output=True, text=True, check=True).stdout.strip()
        if not out:
            return None, None
        h, d = out.split(" ", 1)
        return h[:12], d[:10]
    except Exception:
        return None, None


def days(a, b):
    try:
        return (datetime.date.fromisoformat(a) - datetime.date.fromisoformat(b)).days
    except Exception:
        return None


def referenced(repo):
    """Is the Hub repo name referenced anywhere on the archive's own surfaces?"""
    try:
        r = subprocess.run(["git", "grep", "-l", "-F", f"huggingface.co/datasets/{repo}", "--", "*.md", "*.json", "*.html"],
                           cwd=ROOT, capture_output=True, text=True)
        return bool(r.stdout.strip())
    except Exception:
        return False


def main():
    reg = json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8"))["deposits"]
    reg_latest = max(str(d.get("date") or "")[:10] for d in reg)
    wf = {p.name: p.read_text(encoding="utf-8") for p in (ROOT / ".github/workflows").glob("hf-*.yml")}
    entries = []

    # the canonical projection
    h, d = git_last("data/registry.json")
    entries.append({
        "slug": "crimson-hexagonal-archive", "dataset_class": "canonical",
        "source_path": "data/ (registry, texts, captures, citations, lexicon)", "builder": "scripts/build_hf_dataset.py",
        "workflow": "hf-dataset.yml", "hub_repo_var": "HF_REPO", "hub_repo": "leesharks/crimson-hexagonal-archive",
        "hub_repo_basis": "referenced on archive surfaces" if referenced("leesharks/crimson-hexagonal-archive") else "workflow variable only",
        "update_trigger": "push touching data/registry.json, data/texts/**, captures, citations, datasets/**",
        "last_source_commit": h, "last_source_date": d, "parent_body": None, "status": "live",
    })

    # rhizomes: the matrix in hf-rhizomes.yml is the list
    rz = wf.get("hf-rhizomes.yml", "")
    for m in re.finditer(r"- slug: ([a-z0-9-]+)\s+grammar: (\S+)\s+repo_var: (\S+)", rz):
        slug, gram, var = m.groups()
        body = ROOT / "rhizomes" / slug
        g = json.loads((ROOT / gram).read_text(encoding="utf-8"))
        spore = json.loads((body / "spore.json").read_text(encoding="utf-8")) if (body / "spore.json").exists() else {}
        nodes = [json.loads(l) for l in (body / "nodes.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()] if (body / "nodes.jsonl").exists() else []
        stolons = [json.loads(l) for l in (body / "stolons.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()] if (body / "stolons.jsonl").exists() else []
        latest_node = max((str(n.get("date") or "")[:10] for n in nodes if n.get("date")), default=None)
        h, d = git_last(body)
        repo = f"leesharks/{slug}"
        entries.append({
            "slug": slug, "dataset_class": "rhizome", "source_path": f"rhizomes/{slug}/",
            "grammar": gram, "grammar_version": g.get("version"), "builder": "scripts/build_rhizome_mc.py",
            "workflow": "hf-rhizomes.yml", "hub_repo_var": var, "hub_repo": repo,
            "hub_repo_basis": "referenced on archive surfaces" if referenced(repo) else "workflow variable only",
            "update_trigger": "push touching the grammars, the graph layer or the registry (hf-rhizomes.yml paths)",
            "last_source_commit": h, "last_source_date": d, "generated": str(spore.get("generated") or "")[:10] or None,
            "row_count": len(nodes), "latest_node_date": latest_node,
            "trails_registry_by_days": days(reg_latest, latest_node) if latest_node else None,
            "parent_body": (g.get("body") or {}).get("parent"),
            "stolons": sorted({s.get("to_rhizome") for s in stolons if s.get("to_rhizome")}),
            "status": "live",
        })

    # experiments, interventions, arguments, problems: one workflow each
    singles = [
        ("negative-of-the-negative", "intervention", "datasets/negative-of-the-negative/", "scripts/build_negative_of_the_negative.py", "hf-negative-of-the-negative.yml", "HF_REPO_NON", "leesharks/negative-of-the-negative"),
        ("the-final-time", "experiment", "datasets/the-final-time/", "scripts/build_final_time_dataset.py", "hf-the-final-time.yml", "HF_REPO_FINAL_TIME", "leesharks/the-final-time"),
        ("spam-technicians", "argument", "datasets/argument-as-dataset/", "scripts/build_argument_as_dataset.py", "hf-spam-technicians.yml", "HF_REPO_SPAM", "leesharks/spam-technicians"),
        ("tiger-leap", "problem", "datasets/tiger-leap/", None, "hf-tiger-leap.yml", "HF_REPO_TIGER", "leesharks/tiger-leap"),
    ]
    for slug, cls, src, builder, wfn, var, repo in singles:
        h, d = git_last(ROOT / src)
        paths = re.search(r"paths:\s*\[([^\]]*)\]", wf.get(wfn, ""))
        entries.append({
            "slug": slug, "dataset_class": cls, "source_path": src, "builder": builder,
            "workflow": wfn, "hub_repo_var": var, "hub_repo": repo,
            "hub_repo_basis": "referenced on archive surfaces" if referenced(repo) else "workflow variable only; name as published",
            "update_trigger": ("push touching " + paths.group(1).replace("'", "")) if paths else "see workflow",
            "last_source_commit": h, "last_source_date": d, "parent_body": "crimson-hexagonal-archive", "status": "live",
        })

    # the on-site set (datasets/set.json): published on the archive, not as separate Hub repos
    try:
        st = json.loads((ROOT / "datasets/set.json").read_text(encoding="utf-8"))
        for m in st.get("members", []):
            p = str(m.get("path") or "").strip("/")
            h, d = git_last(ROOT / p) if p else (None, None)
            entries.append({
                "slug": m.get("name"), "dataset_class": "archive_set_member", "source_path": p + "/",
                "builder": None, "workflow": None, "hub_repo_var": None, "hub_repo": None,
                "hub_repo_basis": "on-site dataset; carried inside the canonical projection",
                "update_trigger": "manual", "last_source_commit": h, "last_source_date": d,
                "parent_body": "crimson-hexagonal-archive", "status": "live",
                "set_json": {"version": st.get("version"), "date": st.get("date")},
            })
    except Exception as e:
        entries.append({"slug": "set.json", "status": f"unreadable: {e}"})

    listed = {e.get("source_path", "").rstrip("/").split("/")[-1] for e in entries}
    unlisted = sorted(p.name for p in (ROOT / "datasets").iterdir()
                      if p.is_dir() and p.name not in listed)

    cat = {
        "catalog": "alexanarch-dataset-catalog", "generated": datetime.datetime.now(datetime.timezone.utc).isoformat()[:19] + "Z",
        "generator": "scripts/build_dataset_catalog.py", "registry_latest_deposit_date": reg_latest,
        "note": "Generated from the publishing workflows, the rhizome grammars, the dataset directories and git. "
                "Freshness is recorded, not enforced: trails_registry_by_days is the gap between the registry's latest "
                "deposit and a body's latest node, measured on the emission committed in this repository — the Hub copy is rebuilt in CI from source and may be newer or older. datasets/set.json (the hand-kept set of July) is carried as members "
                "of class archive_set_member; directories under datasets/ that no entry covers are listed in unlisted_directories.",
        "count": len(entries), "entries": entries, "unlisted_directories": unlisted,
    }
    OUT.write_text(json.dumps(cat, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"catalog: {len(entries)} entries, {len(unlisted)} unlisted directories → {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
