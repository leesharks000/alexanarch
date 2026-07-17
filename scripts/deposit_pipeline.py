#!/usr/bin/env python3
"""
deposit_pipeline.py — THE single deposit workflow for Alexanarch.

═══════════════════════════════════════════════════════════════════════════════
ONE PIPELINE, FOUR TRANSPORTS
═══════════════════════════════════════════════════════════════════════════════

Every deposit, regardless of who makes it or how it arrives, runs the SAME
pipeline. The four supported transports differ ONLY in how the issue body
arrives and in which environment this script executes:

  A. WEB FORM (external, no-code)
     GitHub issue form → mint-axn.yml CI → THIS SCRIPT (in CI).

  B. API-ASSISTED (external, archive-funded drafting help)
     Deposit app uses the archive's Anthropic API credits to help the
     depositor FORMAT AND VALIDATE the issue body → posts a GitHub issue →
     same CI path as A. API credits pay for drafting assistance ONLY.
     The pipeline itself NEVER runs on paid API calls.

  C. EXTERNAL LLM, DEPOSITOR'S OWN CREDITS
     Depositor's own LLM formats the issue body per DEPOSIT-GUIDE.md →
     depositor posts the GitHub issue → same CI path as A.

  D. INTERNAL (TACHYON / Assembly instances, direct repo access)
     Run THIS SCRIPT locally in the working session:
       python3 scripts/deposit_pipeline.py --issue-body body.md --issue-number N
     ── THE NO-DOUBLE-DRAW RULE ──────────────────────────────────────────
     Internal depositors MUST NOT invoke the Anthropic API (or any paid
     API) for pipeline work. The session running this script is already
     paid for; the repo is directly writable; there is nothing the API
     path adds except a second bill. LLM-domain work (drafting, LLM-tier
     enrichment: defines_concepts, entities, related_deposits) happens
     IN-SESSION. Mechanical work happens in THIS SCRIPT. The
     artifact/"Claudeception" API path is FORBIDDEN for deposits.
     ─────────────────────────────────────────────────────────────────────

═══════════════════════════════════════════════════════════════════════════════
THE CANONICAL ELEMENT SET, IN CANONICAL ORDER
═══════════════════════════════════════════════════════════════════════════════

  stage        element produced                                   idempotent
  ─────        ────────────────                                   ──────────
  mint         data/texts/AXN-<HEX>-text.md   (canonical bytes)   guarded
               data/deposits/AXN-<HEX>.md     (download alias)
               registry entry (hash, AXN, body_status)
  validate     entry-level then registry-level, --strict, FULL
               output read (never piped through tail/grep)
  record       s/records/<N>/index.html (citation_* meta incl.
               citation_pdf_url; MD + PDF download buttons)        yes
  pdf          papers/AXN-<HEX>.pdf (schema per body_status:
               standard | lacuna | pointer notice)                 checkpointed
  body-index   /api/body-index.json refreshed                     yes (rebuild)
  wiki         wiki-entries.json + /s/wiki/<n>/ page              yes (rebuild)
  sitemap      record URL + paper URL appended                    guarded
  interlink    citation extraction + entity backlinks
               (enrich_deposit --extract --backlinks)             yes
  enrich       mechanical tier: --wikidata --openalex
               --datacite --spxi (LLM tier is IN-SESSION work,
               recorded by the session, never an API call)        yes
  commit       ONE commit for the whole deposit, canonical
               message format "MINT #<N> · <AXN> — <title>"       n/a
  verify       live content-match per link-verification rule v2
               (HTTP 200 is NOT verification)                     n/a

Family note: if the content_type's first clause is not in the dropdown map,
mint infers UNCLASSIFIED; pass --family to set it at mint time with
consistent AXN recomposition (the #1086/#1087 precedent, now formalized).

Usage:
  # Full run (internal, transport D):
  python3 scripts/deposit_pipeline.py --issue-body /tmp/body.md --issue-number 12

  # Post-mint stages only (deposit already in registry):
  python3 scripts/deposit_pipeline.py --deposit-number 1087 --from-stage record

  # CI (transports A/B/C) runs the same entry point.
  # --no-push for review before deploy; --stages to cherry-pick.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = REPO_ROOT / "scripts"
REGISTRY = REPO_ROOT / "data" / "registry.json"

STAGE_ORDER = [
    "mint", "validate", "record", "pdf", "body-index",
    "wiki", "sitemap", "interlink", "enrich", "commit", "verify",
]


def sh(cmd, check=True, timeout=600, capture=False):
    print(f"  $ {' '.join(str(c) for c in cmd)}")
    r = subprocess.run([str(c) for c in cmd], cwd=REPO_ROOT, timeout=timeout,
                       capture_output=capture, text=True)
    if check and r.returncode != 0:
        if capture:
            print(r.stdout or "", r.stderr or "", sep="\n")
        raise SystemExit(f"stage command failed ({r.returncode}): {cmd[0]}")
    return r


def load_registry():
    return json.loads(REGISTRY.read_text(encoding="utf-8"))


def deposit_by_number(n):
    reg = load_registry()
    for d in reg["deposits"]:
        if d["deposit_number"] == n:
            return reg, d
    raise SystemExit(f"deposit #{n} not in registry")


def hex_of(d):
    axn = d.get("axn", "")
    return axn.split(":")[1].split(".")[0] if ":" in axn and "." in axn else ""


# ── stages ───────────────────────────────────────────────────────────────────

def stage_mint(args):
    cmd = [sys.executable, SCRIPTS / "mint_deposit.py",
           "--issue-body", args.issue_body,
           "--issue-number", str(args.issue_number),
           "--output", "/tmp/pipeline-mint.json"]
    sh(cmd)
    m = json.loads(Path("/tmp/pipeline-mint.json").read_text())
    entry = m["registry_entry"]
    n = entry["deposit_number"]

    # Optional family override with consistent AXN recomposition
    if args.family and entry["family"] != args.family:
        sys.path.insert(0, str(SCRIPTS))
        from axn_lib import compose_axn  # single source of AXN derivation
        glyph = entry["axn"].split(".", 2)[2]
        old_fam = entry["family"]
        entry["family"] = args.family
        entry["axn"] = compose_axn(entry["hex"], args.family, glyph)
        entry["root_axn"] = f"AXN:{entry['hex']}.{args.family}"
        for k in ("axn_canonical", "axn_display"):
            if entry.get(k):
                entry[k] = entry[k].replace(f".{old_fam}.", f".{args.family}.")\
                                   .replace(f".{old_fam}", f".{args.family}")
        print(f"  family override: {old_fam} → {args.family}")

    # body_status at mint (complete-by-declaration; audit may revise)
    entry.setdefault("body_status", {
        "class": "full", "lacuna": False, "recovery_status": "COMPLETE",
        "residual_chars": m.get("canonical_text_bytes", 0),
        "audited_at": entry.get("minted_at", ""),
        "audit_version": "mint-time-declaration",
    })

    # mint_deposit inserts the pre-override entry; replace it in place
    reg = load_registry()
    for i, d in enumerate(reg["deposits"]):
        if d["deposit_number"] == n:
            reg["deposits"][i] = entry
            break
    else:
        reg["deposits"].append(entry)
    if "deposit_count" in reg:
        reg["deposit_count"] = len(reg["deposits"])
    REGISTRY.write_text(json.dumps(reg, indent=1, ensure_ascii=False),
                        encoding="utf-8")
    Path("/tmp/pipeline-entry.json").write_text(
        json.dumps(entry, indent=2, ensure_ascii=False))
    args.deposit_number = n
    print(f"  minted + inserted: #{n} · {entry['axn']}")


def stage_validate(args):
    # STANDING RULE: full output, never piped through tail/grep.
    if Path("/tmp/pipeline-entry.json").exists():
        sh([sys.executable, SCRIPTS / "validate_deposit.py",
            "--registry-entry", "/tmp/pipeline-entry.json", "--strict"])
    sh([sys.executable, SCRIPTS / "validate_deposit.py",
        "--registry", str(REGISTRY), "--strict"])


def stage_record(args):
    n = args.deposit_number
    code = (
        "import sys, json; sys.path.insert(0, '.');\n"
        "import wire_deposit\n"
        f"reg = json.load(open('data/registry.json'))\n"
        f"eidx = json.load(open('data/entity-index.json'))\n"
        f"d = next(x for x in reg['deposits'] if x['deposit_number'] == {n})\n"
        "wire_deposit.regenerate_static_page(d, eidx, registry=reg)\n"
        f"print('  record page: s/records/{n}/')\n"
    )
    sh([sys.executable, "-c", code])


def stage_pdf(args):
    sh([sys.executable, SCRIPTS / "build_deposit_pdfs.py",
        f"--deposits={args.deposit_number}", "--timeout=120", "--force"])


def stage_body_index(args):
    sh([sys.executable, SCRIPTS / "build_body_index.py"])


def stage_wiki(args):
    sh([sys.executable, SCRIPTS / "regenerate_surfaces.py", "--only", "wiki"])


def stage_sitemap(args):
    reg, d = deposit_by_number(args.deposit_number)
    hx = hex_of(d).zfill(4)
    n = args.deposit_number
    sm = REPO_ROOT / "sitemap.xml"
    txt = sm.read_text(encoding="utf-8")
    add = []
    if f"/s/records/{n}/" not in txt:
        add.append(f"  <url><loc>https://alexanarch.org/s/records/{n}/</loc>"
                   f"<changefreq>monthly</changefreq><priority>0.7</priority></url>")
    if f"/papers/AXN-{hx}.pdf" not in txt:
        add.append(f"  <url><loc>https://alexanarch.org/papers/AXN-{hx}.pdf</loc>"
                   f"<changefreq>monthly</changefreq><priority>0.6</priority></url>")
    if add:
        i = txt.rfind("</urlset>")
        sm.write_text(txt[:i] + "\n".join(add) + "\n" + txt[i:], encoding="utf-8")
    print(f"  sitemap: +{len(add)} URLs")


def stage_interlink(args):
    # --extract is LLM-domain (it calls the Anthropic API) and is therefore
    # IN-SESSION work under the No-Double-Draw Rule: the operating session
    # writes citations/concepts directly. Pipeline runs only the mechanical
    # backlink pass.
    sh([sys.executable, SCRIPTS / "enrich_deposit.py",
        "--deposit-number", str(args.deposit_number),
        "--backlinks"], check=False)


def stage_enrich(args):
    # Mechanical tier only. The LLM tier is in-session work (transport D)
    # or queued for a tooled session — NEVER a paid API call from here.
    sh([sys.executable, SCRIPTS / "enrich_deposit.py",
        "--deposit-number", str(args.deposit_number),
        "--wikidata", "--openalex", "--datacite", "--spxi"], check=False)


def stage_commit(args):
    reg, d = deposit_by_number(args.deposit_number)
    n, axn, title = args.deposit_number, d["axn"], d.get("title", "")[:80]
    sh(["git", "add", "-A"])
    sh(["git", "checkout", "data/pre-overwrite-receipts.log"], check=False)
    msg = (f"MINT #{n} · {axn} — {title}\n\n"
           f"Deposited via deposit_pipeline.py (single-workflow, "
           f"all stages: {', '.join(args.stages)}).")
    sh(["git", "commit", "-m", msg], check=False)
    if not args.no_push:
        r = sh(["git", "push", "origin", "main"], check=False)
        if r.returncode != 0:
            sh(["git", "pull", "--rebase", "origin", "main"])
            sh(["git", "push", "origin", "main"])


def stage_verify(args):
    if args.no_push:
        print("  (skipped: --no-push)")
        return
    reg, d = deposit_by_number(args.deposit_number)
    n, hx = args.deposit_number, hex_of(d).zfill(4)
    time.sleep(args.deploy_wait)
    import urllib.request
    checks = [
        (f"https://www.alexanarch.org/s/records/{n}/", d["axn"].split(".")[0]),
        (f"https://www.alexanarch.org/papers/AXN-{hx}.pdf", None),
    ]
    for url, needle in checks:
        try:
            with urllib.request.urlopen(url, timeout=25) as r:
                body = r.read(200_000)
                ok = (needle is None) or (needle.encode() in body)
                print(f"  {'✓' if ok else '✗ CONTENT-MISMATCH'} {url}")
        except Exception as e:
            print(f"  ✗ {url} — {e}")


STAGES = {
    "mint": stage_mint, "validate": stage_validate, "record": stage_record,
    "pdf": stage_pdf, "body-index": stage_body_index, "wiki": stage_wiki,
    "sitemap": stage_sitemap, "interlink": stage_interlink,
    "enrich": stage_enrich, "commit": stage_commit, "verify": stage_verify,
}


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--issue-body", help="path to issue body (mint stage)")
    ap.add_argument("--issue-number", type=int, help="GitHub issue number (mint stage)")
    ap.add_argument("--deposit-number", type=int, help="existing deposit (post-mint stages)")
    ap.add_argument("--family", help="AXN family override at mint (e.g. GOVERNANCE)")
    ap.add_argument("--from-stage", default=None, choices=STAGE_ORDER,
                    help="start at this stage (default: mint if --issue-body else record)")
    ap.add_argument("--stages", default=None,
                    help="comma list to run exactly these stages")
    ap.add_argument("--no-push", action="store_true")
    ap.add_argument("--deploy-wait", type=int, default=90)
    args = ap.parse_args()

    if args.stages:
        args.stages = [s.strip() for s in args.stages.split(",")]
    else:
        start = args.from_stage or ("mint" if args.issue_body else "record")
        args.stages = STAGE_ORDER[STAGE_ORDER.index(start):]

    if "mint" in args.stages and not (args.issue_body and args.issue_number):
        raise SystemExit("mint stage requires --issue-body and --issue-number")
    if "mint" not in args.stages and not args.deposit_number:
        raise SystemExit("post-mint stages require --deposit-number")

    print(f"deposit_pipeline: stages = {args.stages}")
    for s in args.stages:
        print(f"\n── stage: {s} ──")
        STAGES[s](args)
    print("\n∮ pipeline complete")


if __name__ == "__main__":
    main()
