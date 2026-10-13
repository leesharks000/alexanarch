#!/usr/bin/env python3
"""build_axn_derivation_ledger.py — AXN protocol v2.2 applied to the 2026-06-20 batch.

MANUS ruling 2026-10-13: "lets go ahead and adopt the solution for those batched axns."
The solution, as corrected by the reviewer report of the same morning, records three independent
dimensions on each batch record and changes no AXN, no hash and no text:

  mint_derivation   the stored hash; the recipe; whether its input was retained; whether the stored
                    hash equals the SHA-256 of any bytes this archive holds (served now, or earlier)
  founding_event    2026-06-20 batch assignment (data/batch-axn-assignment.json), the day after the
                    2026-06-19 Zenodo account termination; the batch AXN and hash; the former DOIs
                    that now resolve to the record; MANUS's attestation, kept as attestation —
                    "what the batch axns were minting over was the absence of the deleted records
                    themselves" — and not as derivation evidence
  manifestations    every distinct body the record has held in git, in order: the batch placeholder
                    (data/deposits/AXN-<HEX>.md as first written) where it predates the first
                    canonical body, then each version of the canonical text file; SHA-256, computed
                    SWHID, Software Heritage retention (checked through /api/1/known/), the commit

Rules the ledger keeps (reviewer report, verified and adopted):
  * the preimage of a hash is bytes; none of the retained bytes is asserted to be it unless it hashes to it
  * a later body differing from an earlier one is recorded as an unaccounted byte difference; a cause is
    not assigned, and the commit subject is carried only as what the commit said
  * a byte change does not establish that two bodies are the same edition: same_edition is
    "undetermined" unless an editorial determination is recorded
  * a computed SWHID is not retention; swh_known is checked separately and dated
  * "∅" on a first canonical body means no canonical body was seated in this archive at the preceding
    recorded state; it asserts nothing about the work or about the old hash's input

Outputs: data/axn-derivation-ledger.json (full chains) and compact fields on each batch registry entry
(mint_derivation, founding_event, manifestations: {ledger, count, first_retained, current}).
Idempotent: re-running recomputes everything from git, the registry and Software Heritage.

Usage: python3 scripts/build_axn_derivation_ledger.py [--no-swh] [--date YYYY-MM-DD]
"""
import argparse, collections, hashlib, json, pathlib, subprocess, sys, urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[1]
REG = ROOT / "data/registry.json"
BATCH = ROOT / "data/batch-axn-assignment.json"
DOIMAP = ROOT / "data/api/doi-axn-map.json"
OUT = ROOT / "data/axn-derivation-ledger.json"
ATTESTATION = {"by": "Lee Sharks (MANUS)", "date": "2026-10-13",
               "statement": "what the batch axns were minting over was the absence of the deleted records themselves",
               "standing": "attestation of the founding event; not derivation evidence"}
RECIPE = ("2026-06-20 batch assignment (871 works, hex 0005–036B). The assigning procedure and its input bytes "
          "are not in the repository; data/batch-axn-assignment.json records its outputs only. No version of any "
          "file under data/texts/ or data/deposits/ in git history hashes to the stored value.")
EMPTY_PRIOR = "∅ — no canonical body was seated in this archive at the preceding recorded state"


def git(*a):
    return subprocess.run(["git", *a], cwd=ROOT, capture_output=True, text=True, check=True).stdout


def history():
    """path -> [(commit, iso_date, new_oid, subject)] for A/M events under data/texts and data/deposits."""
    out = git("log", "--reverse", "--format=C %H %aI %s", "--raw", "--no-abbrev", "--no-renames",
              "--", "data/texts", "data/deposits")
    h = collections.defaultdict(list); cur = None
    for line in out.splitlines():
        if line.startswith("C "):
            parts = line.split(" ", 3); cur = (parts[1], parts[2], parts[3] if len(parts) > 3 else "")
        elif line.startswith(":") and cur:
            meta, path = line.split("\t", 1)
            f = meta.split()
            if f[4] in ("A", "M"):
                h[path].append((cur[0], cur[1], f[3], cur[2]))
    return h


def _t(iso):
    import datetime
    return datetime.datetime.fromisoformat(iso)


def blob_sha256(oids):
    p = subprocess.Popen(["git", "cat-file", "--batch"], cwd=ROOT, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    res = {}
    for o in oids:
        p.stdin.write((o + "\n").encode()); p.stdin.flush()
        hdr = p.stdout.readline().split()
        if len(hdr) < 3 or hdr[1] == b"missing":
            res[o] = None; continue
        n = int(hdr[2]); data = p.stdout.read(n); p.stdout.read(1)
        res[o] = hashlib.sha256(data).hexdigest()
    p.stdin.close(); p.wait()
    return res


def swh_known(swhids):
    known = {}
    ids = sorted(set(swhids))
    for i in range(0, len(ids), 900):
        chunk = ids[i:i + 900]
        req = urllib.request.Request("https://archive.softwareheritage.org/api/1/known/",
                                     data=json.dumps(chunk).encode(), headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=120) as r:
            for k, v in json.loads(r.read()).items():
                known[k] = bool(v.get("known"))
    return known


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--no-swh", action="store_true")
    ap.add_argument("--date", default="2026-10-13"); a = ap.parse_args()
    raw = REG.read_text(encoding="utf-8"); reg = json.loads(raw)
    by_hex = {d["hex"]: d for d in reg["deposits"]}
    batch = json.loads(BATCH.read_text(encoding="utf-8"))["assignments"]
    doimap = json.loads(DOIMAP.read_text(encoding="utf-8"))["map"]
    dois_by_rec = collections.defaultdict(list)
    for doi, v in doimap.items():
        try:
            n = int(str(v[1]).rstrip("/").rsplit("/", 1)[1])
        except Exception:
            continue
        dois_by_rec[n].append(doi)
    hist = history()
    head_tree = {l.split("\t")[1]: l.split()[2] for l in git("ls-tree", "-r", "HEAD", "--", "data/texts", "data/deposits").splitlines()}

    plans, unregistered = [], []
    for asg in batch:
        d = by_hex.get(asg["hex"])
        if not d:
            unregistered.append({"sovereign_id": asg["sovereign_id"], "batch_axn": asg["axn"], "hex": asg["hex"],
                                 "title_at_assignment": asg.get("title"), "note": "assigned in the batch, never entered the registry"})
            continue
        tpath = (d.get("full_text_path") or f"/data/texts/AXN-{d['hex']}-text.md").lstrip("/")
        alias = f"data/deposits/AXN-{d['hex']}.md"
        plans.append((asg, d, tpath, alias))

    oids = set()
    for asg, d, tpath, alias in plans:
        for c in hist.get(tpath, []) + hist.get(alias, [])[:1]: oids.add(c[2])
        if tpath in head_tree: oids.add(head_tree[tpath])
    sha = blob_sha256(sorted(oids))
    known = {} if a.no_swh else swh_known([f"swh:1:cnt:{o}" for o in oids])

    def man(seq, kind, path, ev):
        commit, date, oid, subj = ev
        sw = f"swh:1:cnt:{oid}"
        return {"seq": seq, "kind": kind, "path": path, "commit": commit, "date": date, "sha256": sha.get(oid),
                "swhid": sw, "swh_known": known.get(sw) if known else None, "commit_subject": subj[:200]}

    entries, counts = {}, collections.Counter()
    for asg, d, tpath, alias in plans:
        n = d["deposit_number"]
        tev = hist.get(tpath, [])
        aev = hist.get(alias, [])[:1]
        chain = []
        if aev and (not tev or _t(aev[0][1]) < _t(tev[0][1])) and (not tev or aev[0][2] != tev[0][2]):
            chain.append(man(0, "placeholder", alias, aev[0]))
        seen = None
        for ev in tev:
            if ev[2] == seen: continue
            seen = ev[2]
            m = man(len(chain), "canonical_body", tpath, ev)
            if not any(x["kind"] == "first_retained_canonical_body" for x in chain):
                m["kind"] = "first_retained_canonical_body"
                m["prior_state"] = (f"placeholder (seq {chain[0]['seq']})" if chain else EMPTY_PRIOR)
            else:
                m["change"] = "unaccounted_byte_difference"; m["same_edition"] = "undetermined"
            chain.append(m)
        cur_oid = head_tree.get(tpath)
        cur_sw = f"swh:1:cnt:{cur_oid}" if cur_oid else None
        declared = bool(d.get("full_text_path"))
        current = ({"path": tpath, "sha256": sha.get(cur_oid), "swhid": cur_sw,
                    "swh_known": known.get(cur_sw) if known else None, "swh_checked": a.date if known else None,
                    "observed": a.date} if cur_oid else {"path": tpath, "missing": True, "observed": a.date})
        if not declared:
            current["full_text_path_declared"] = False
        if cur_oid and chain and chain[-1]["sha256"] != current["sha256"]:
            current["note"] = "served bytes differ from the last committed manifestation"
        h = d.get("hash")
        hits = [m["seq"] for m in chain if m["sha256"] == h]
        if cur_oid and current.get("sha256") == h:
            status, against = "verifies_against_served_bytes", "current"
        elif hits:
            status, against = "verifies_against_retained_bytes", hits[0]
        else:
            status, against = "unverified_input_not_retained", None
        batch_current = d.get("axn") == asg["axn"]
        md = {"hash": h, "status": status, "verified_against": against,
              "input_retained": status != "unverified_input_not_retained",
              "recipe": RECIPE if batch_current else
                        "restoration mint: hash recomputed over the seated body and the glyph recomposed under the same hex "
                        "(restoration protocol of 2026-07-04 / restore_in_place.py); the batch AXN is kept in founding_event",
              "checked": a.date}
        fe = {"date": "2026-06-20", "kind": "batch_assignment", "basis": "data/batch-axn-assignment.json",
              "upstream_deletion": "2026-06-19 Zenodo account termination (862 deposits, 1,817 DOIs)",
              "sovereign_id": asg["sovereign_id"], "batch_axn": asg["axn"], "batch_hash": asg["hash"],
              "batch_axn_current": batch_current,
              "batch_derivation": ("as mint_derivation" if batch_current else
                                   ("unverified_input_not_retained" if not any(m["sha256"] == asg["hash"] for m in chain)
                                    else "verifies_against_retained_bytes")),
              "former_dois": sorted(dois_by_rec.get(n, [])), "attestation": ATTESTATION}
        if not batch_current:
            fe["superseded_by_restoration_mint"] = d.get("axn")
        unacc = sum(1 for m in chain if m.get("change") == "unaccounted_byte_difference")
        first = next((m for m in chain if m["kind"] == "first_retained_canonical_body"), None)
        entries[str(n)] = {"deposit_number": n, "axn": d.get("axn"), "mint_derivation": md, "founding_event": fe,
                           "manifestations": chain, "current": current}
        d["mint_derivation"] = md
        d["founding_event"] = {k: v for k, v in fe.items() if k != "former_dois"} | {"former_doi_count": len(fe["former_dois"])}
        d["manifestations"] = {"ledger": f"/data/axn-derivation-ledger.json#{n}", "count": len(chain),
                               "first_retained": ({k: first[k] for k in ("seq", "commit", "date", "sha256", "swhid", "swh_known")} if first else None),
                               "current": current, "unaccounted_byte_differences": unacc}
        counts[status] += 1; counts["placeholder_retained"] += any(m["kind"] == "placeholder" for m in chain)
        counts["batch_axn_current"] += batch_current; counts["unaccounted_byte_differences"] += unacc
        counts["current_swh_known"] += bool(current.get("swh_known"))
        counts["no_canonical_file"] += bool(current.get("missing"))
        counts["full_text_path_undeclared"] += not declared

    ledger = {
        "maxim": "all things are now lawful to you in christ jesus",
        "name": "AXN derivation ledger — the 2026-06-20 batch",
        "protocol": "axn/v2.2 (data/api/axn-protocol.json → record_dimensions)",
        "ruling": {"by": "Lee Sharks (MANUS)", "date": "2026-10-13",
                   "text": "lets go ahead and adopt the solution for those batched axns"},
        "generated": a.date, "generator": "scripts/build_axn_derivation_ledger.py",
        "scope": f"{len(entries)} registry records whose hex appears in data/batch-axn-assignment.json; "
                 f"{len(unregistered)} assignments never entered the registry and are listed, not created",
        "definitions": {
            "mint_derivation.status": {"verifies_against_served_bytes": "stored hash = SHA-256 of the file served now",
                                       "verifies_against_retained_bytes": "stored hash = SHA-256 of an earlier manifestation held in git",
                                       "unverified_input_not_retained": "no bytes this archive holds hash to the stored value; the derivation cannot be re-checked"},
            "∅": EMPTY_PRIOR,
            "unaccounted_byte_difference": "the body differs from the preceding manifestation; no cause is assigned by this ledger",
            "same_edition": "undetermined unless an editorial determination with its reason is recorded",
            "swhid": "computed from the bytes (sha1_git); swh_known records separately whether Software Heritage holds them, as checked on the date given",
            "attestation": "MANUS's statement of the founding event, kept as attestation and not as derivation evidence"},
        "counts": dict(counts), "unregistered_assignments": unregistered, "entries": entries}
    OUT.write_text(json.dumps(ledger, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    compact = "\n" not in raw.strip()
    REG.write_text(json.dumps(reg, ensure_ascii=False, separators=(",", ":")) if compact
                   else json.dumps(reg, ensure_ascii=False, indent=2) + ("\n" if raw.endswith("\n") else ""), encoding="utf-8")
    print(json.dumps(ledger["counts"]), len(entries), "records;", len(unregistered), "unregistered assignments")


if __name__ == "__main__":
    main()
