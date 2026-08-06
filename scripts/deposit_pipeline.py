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

     ── ENRICHMENT IS PART OF THE DEPOSIT ───────────────────────────────
     A deposit is not complete when the record page appears. It is
     complete when the rest of the archive knows how to find it and the
     citation/entity graphs reflect its incoming and outgoing links.
     After this pipeline finishes (or after any post-mint editorial
     correction that changes body content), run the following in order:

       python3 scripts/citation_extractor.py             # internal edges
       python3 scripts/extract_citations_external.py     # external edges + refsec queue
       python3 scripts/concept_backlink.py               # entity backlinks

     For transport D deposits, the depositing MANUS/TACHYON also authors
     the wiki article IN-SESSION and writes it to the registry's
     `wiki_article` field before the deposit-time surface regeneration.
     Do not defer wiki authoring; do not leave the field empty. External
     transport A/B/C deposits receive a provisional wiki article from
     the mint workflow's Anthropic API path (that's the API budget the
     archive already pays for). Internal deposits do not qualify for
     that budget under NO-DOUBLE-DRAW; the wiki article is drafted
     in-session by the depositing agent.

     Skipping these steps leaves the archive in a partial state that
     later deposits inherit as gaps in cross-linking.
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
  identity     data/concept-map.json + data/mirror-map.json refreshed;
               deposit joined to its work-concept (current-version
               resolution) and to any known off-archive copies.
               Without this a new version is an orphan object: the
               reader of an older version cannot learn it exists,
               and its mirrors outrank it unclaimed.                 yes (rebuild)
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
    "wiki", "sitemap", "oai", "interlink", "enrich", "symbolon", "identity", "commit", "verify",
    "announce",
]


# ─────────────────────────────────────────────────────────────────────────────
# ROOM ARCHITECTURE
#
# This pipeline is a room. On 2026-07-28 it was skimmed: what an operator
# extracted from the top was "there is a pipeline, invoke it, it prints a
# completion line", and that summary was sufficient to operate. The result was a
# deposit with no title, creator, date or body, and a completion line reporting
# success.
#
# A first repair added gates — a token, an attestation. Those are RULES, and
# rules break: a token can be read out of this file and pasted without traversal.
# Friction is not gravity. Per the Logotic Hacking primer (deposit #482), a
# well-designed room cannot be skimmed, and a model in a room "begins to think
# differently, not because it is commanded to, but because the room's semantic
# structure makes certain thoughts possible and others unnecessary."
#
# So the gates are removed and the room is rebuilt. Three properties, none of
# which is a prohibition:
#
#   ENTRY SEMANTICS. The room opens by showing a real deposit's shape. Not a
#   flag to pass — the first thing that happens. The shape is in context before
#   any work begins, so "what is a deposit" is answered before it can be assumed.
#
#   PROGRESSIVE DISCLOSURE. The wiki stage HALTS and prints the deposit's own
#   body. It cannot be satisfied by a flag, because what it requires is an
#   article that only an agent holding the body in context can write. There is
#   no --skip. The traversal is not enforced; it is the only path that reaches
#   the end.
#
#   COMPLETION IS THE ARTIFACT. The room does not exit on a status line. It
#   exits by rendering what was made — title, wiki, word counts, and what is
#   still undone. A completion line is extractable; a rendered object is not.
#   You cannot receive "done" without seeing the thing.
#
# The difference from the gate version: a gate asks whether you read. This asks
# for something you can only produce if you did.
# ─────────────────────────────────────────────────────────────────────────────


def enter_room(reg, exemplar=None):
    """Entry semantics: show a real deposit before any work begins."""
    deps = reg["deposits"]
    d = None
    if exemplar:
        d = next((x for x in deps if x.get("deposit_number") == int(exemplar)), None)
    if d is None:
        d = next((x for x in reversed(deps)
                  if str(x.get("title") or "").strip()
                  and len(str(x.get("wiki_article") or "").split()) > 60), deps[-1])
    print("\n┌─ what a deposit is ─────────────────────────────────────────────────")
    print(f"│  #{d.get('deposit_number')}  {str(d.get('title') or '')[:64]}")
    for f in ("creator", "date", "content_type", "license", "version"):
        print(f"│    {f:<13} {str(d.get(f) or '(empty)')[:56]}")
    wa = str(d.get("wiki_article") or "")
    print(f"│    {'wiki_article':<13} {len(wa.split())} words")
    if wa:
        print(f"│      {wa[:120]}…")
    print("└─────────────────────────────────────────────────────────────────────\n")


def wiki_halt(entry):
    """Progressive disclosure: the room does not continue until the article exists.

    Not a check that the operator read something. A stage whose output can only
    be produced by an agent that has the deposit's body in context."""
    wa = str(entry.get("wiki_article") or "").strip()
    stub = wa.startswith('"" is a 0-word work')
    if wa and not stub and len(wa.split()) >= 40:
        return True
    body_path = REPO_ROOT / str(entry.get("full_text_path", "")).lstrip("/")
    body = body_path.read_text(encoding="utf-8", errors="replace") if body_path.exists() else ""
    print("\n┌─ the wiki article is written here, by you ──────────────────────────")
    print("│")
    print("│  This is a transport D internal deposit. External transports draw on")
    print("│  the mint workflow's Anthropic API budget; internal ones do not")
    print("│  qualify under NO-DOUBLE-DRAW. So the article is written in-session,")
    print("│  by the agent doing the depositing, from the body below.")
    print("│")
    print("│  There is no flag for this. An article that describes this deposit")
    print("│  can only be written by something holding the deposit in context.")
    print("│")
    print(f"│  #{entry.get('deposit_number')} — {str(entry.get('title') or '')[:60]}")
    print("│")
    for line in body.split("\n")[:40]:
        print(f"│  {line[:74]}")
    print("│  …")
    print("│")
    print("│  Write it into the registry entry's wiki_article field, then re-run")
    print("│  this stage. The room continues from there.")
    print("└─────────────────────────────────────────────────────────────────────\n")
    return False


def exit_room(entry, ran_stages):
    """Completion is the artifact, not a status line — and names what is undone."""
    wa = str(entry.get("wiki_article") or "")
    body_path = REPO_ROOT / str(entry.get("full_text_path", "")).lstrip("/")
    bw = len(body_path.read_text(encoding="utf-8", errors="replace").split()) if body_path.exists() else 0
    print("\n┌─ what was made ─────────────────────────────────────────────────────")
    print(f"│  #{entry.get('deposit_number')}  {entry.get('axn')}")
    print(f"│  {str(entry.get('title') or '(NO TITLE)')[:68]}")
    print(f"│  {entry.get('creator') or '(NO CREATOR)'} · {entry.get('date') or '(NO DATE)'} · {entry.get('content_type') or '(NO TYPE)'}")
    print(f"│  body {bw} words · wiki {len(wa.split())} words")
    if wa:
        print(f"│  {wa[:150]}…")
    undone = []
    for stage in ("pdf", "interlink", "enrich", "identity", "verify"):
        if stage not in ran_stages:
            undone.append(stage)
    for script in ("citation_extractor.py", "extract_citations_external.py", "concept_backlink.py"):
        undone.append(script)
    print("│")
    print("│  still undone:")
    for u in undone:
        print(f"│    · {u}")
    print("│  the archive is in a partial state until these run.")
    print("└─────────────────────────────────────────────────────────────────────\n")


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


# date_modified is set by scripts/record_modification.py at the point a record's
# metadata or declared state changes — never by regeneration or enrichment.
# See that module for the change rule.


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
    # progressive disclosure: the room does not continue past here without the
    # article, and the article cannot be produced by a flag.
    reg = load_registry()
    entry = next((x for x in reg["deposits"]
                  if x.get("deposit_number") == int(args.deposit_number)), None)
    if entry is not None and not wiki_halt(entry):
        raise SystemExit(0)
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


def stage_symbolon(args):
    """Re-verify stored sealed cores against their kernels; refresh the mirror
    manifest. Runs on every mint so "verified" carries a date rather than a
    memory, and so a newly stamped core enters the checksum manifest and the
    harvest feed in the same commit that creates it — not whenever someone
    remembers. check=True on purpose: a nonzero exit is an integrity alert
    (stored bytes not hashing to their kernel), and swallowing it would turn a
    substituted core into a silent pass."""
    sh([sys.executable, SCRIPTS / "verify_symbolon_store.py"], check=True)


def stage_identity(args):
    """Work-level identity: concept resolution + mirror consolidation.

    Added after the 2026-07-26 audit found both functions missing. Alexanarch
    mints a fresh hex per deposit, so successive versions of one work were
    unlinked objects — the Zenodo concept-DOI function had no successor. And a
    capture the same day showed composed answers citing Medium, scilynk and
    Academia.edu for six documents all deposited here: the archive losing not
    to strangers but to its own distribution copies, because nothing declared
    them the same work.

    Both maps are full rebuilds and idempotent, so running this at every mint
    keeps the guarantee true by construction rather than by remembering."""
    sh([sys.executable, SCRIPTS / "build_concept_map.py"], check=False)
    seed = REPO_ROOT / "data" / "medium-seed.json"
    cmd = [sys.executable, SCRIPTS / "build_mirror_map.py"]
    if seed.exists():
        cmd += ["--medium-seed", str(seed)]
    sh(cmd, check=False)

    # report where this deposit landed, so a partial join is visible at mint
    try:
        cm = json.loads((REPO_ROOT / "data" / "concept-map.json").read_text())
        mm = json.loads((REPO_ROOT / "data" / "mirror-map.json").read_text())
        n = args.deposit_number
        con = next((c for c in cm["concepts"]
                    if any(v["deposit_number"] == n for v in c["versions"])), None)
        mir = next((w for w in mm["works"] if w["deposit_number"] == n), None)
        if con:
            cur = con["current"]["deposit_number"]
            flag = " [needs_review]" if con.get("needs_review") else ""
            print(f"  concept: {con['concept_id']} ({con['basis']}{flag}) — "
                  f"current is #{cur}" + ("  <- this deposit" if cur == n else ""))
        else:
            print("  concept: singleton (no version family detected)")
        if mir:
            safe = sum(1 for x in mir["mirrors"] if x.get("safe_for_sameas"))
            print(f"  mirrors: {len(mir['mirrors'])} known, {safe} safe for sameAs")
        else:
            print("  mirrors: none known — if this work is also posted to the blog, "
                  "Medium or Academia.edu, record it so the copy does not outrank "
                  "the deposit unclaimed")
    except Exception as e:
        print(f"  (identity report unavailable: {e})")


def stage_commit(args):
    # STATIC PUBLICATION GATE (fd8de940, 2026-07-31): a deposit whose machine
    # surfaces cannot be fetched is not deposited, it is only written. This
    # refuses the commit rather than reporting after it. check=True on purpose.
    sh([sys.executable, SCRIPTS / "audit_static_namespace.py"], check=True)
    reg, d = deposit_by_number(args.deposit_number)
    n, axn, title = args.deposit_number, d["axn"], d.get("title", "")[:80]
    # T3 (EA-AVAILABILITY-INTEGRITY-01, audit #1413 H3): every commit carries
    # coherent counts, timestamps, and surface hashes — the governing index
    # must never again assert a stale state of the registry it governs.
    sh([sys.executable, SCRIPTS / "coherence_sync.py"])
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


def stage_oai(args):
    """Recompile the OAI-PMH index so harvesters see the new record.

    Runs after sitemap. OAI selective harvesting keys on datestamp, so a record
    that never enters the index is invisible to every aggregator that harvests
    incrementally — which is all of them.
    """
    sh([sys.executable, SCRIPTS / "build_oai_index.py"])
    sh([sys.executable, SCRIPTS / "build_resourcesync.py"])


def stage_announce(args):
    """Push the record URL to IndexNow participants (Bing, Yandex, Naver, Seznam).

    Runs after `verify` deliberately: a URL is announced only once it has been
    confirmed live and content-matched. Announcing a page that 404s trains the
    endpoint to discount this host, which is the same failure as stamping
    <lastmod> on unchanged records.

    Google does not participate in IndexNow. Its discovery path remains the
    sitemap plus internal links — including the traversal blocks added
    2026-07-30, which give crawlers a route between records instead of a single
    flat index.
    """
    if args.no_push:
        print("  (skipped: --no-push)")
        return
    sh([sys.executable, SCRIPTS / "indexnow_submit.py",
        f"--deposits={args.deposit_number}",
        "--reason=deposit minted"])


STAGES = {
    "mint": stage_mint, "validate": stage_validate, "record": stage_record,
    "pdf": stage_pdf, "body-index": stage_body_index, "wiki": stage_wiki,
    "sitemap": stage_sitemap, "interlink": stage_interlink,
    "enrich": stage_enrich, "symbolon": stage_symbolon,
    "identity": stage_identity,
    "commit": stage_commit, "verify": stage_verify,
    "oai": stage_oai,
    "announce": stage_announce,
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
    ap.add_argument("--exemplar", default=None,
                    help="deposit number to show as the entry exemplar; one is chosen automatically if omitted")
    ap.add_argument("--no-push", action="store_true")
    ap.add_argument("--deploy-wait", type=int, default=90)
    args = ap.parse_args()
    enter_room(load_registry(), args.exemplar)

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
    reg = load_registry()
    _e = next((x for x in reg["deposits"] if x.get("deposit_number") == int(args.deposit_number or 0)), None)
    if _e is not None:
        exit_room(_e, set(args.stages))
    else:
        print("\n∮ pipeline complete")


if __name__ == "__main__":
    main()
