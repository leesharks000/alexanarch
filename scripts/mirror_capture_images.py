#!/usr/bin/env python3
"""mirror_capture_images.py — the archive holds its own evidence.

WHY
The capture registry is a record of visual evidence, and until 2026-08-07 that
evidence lived somewhere else. 257 of 268 image references pointed at
leesharks.com or machinemediation — surfaces the archive does not control, cannot
guarantee, and would lose without notice. A registry documenting platform erasure
whose exhibits are hosted on other platforms is making its own argument against
itself.

Worse, nothing resolved them: no gallery ever rendered the imgs field, so the
dependency was invisible. The links were dead in the way that shows no error.

WHAT THIS DOES
Fetches every externally hosted capture image into data/captures/{slug}/ and
rewrites the registry to archive-relative paths. **The original URL is preserved**
in `imgs_origin` per non-destruction: where an image came from is provenance, and
provenance is not replaced by custody.

Idempotent. Re-running fetches only what is missing.

Usage:
    python3 scripts/mirror_capture_images.py --dry-run
    python3 scripts/mirror_capture_images.py --apply [--limit N]
"""
import json, re, sys, pathlib, argparse, urllib.request, hashlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
REG = ROOT / "data/EA-WG-CAPTURES-01.json"
DEST = ROOT / "data/captures"
BARE_BASE = "https://leesharks.com/captures/"
UA = {"User-Agent": "Mozilla/5.0 (alexanarch capture mirror)"}


def resolve(u):
    if u.startswith("http"):
        return u
    if u.startswith("data/captures/"):
        return None            # already archive-local
    return BARE_BASE + u.lstrip("/")


def safe_name(u):
    name = u.split("/")[-1].split("?")[0]
    name = re.sub(r"[^A-Za-z0-9._-]", "-", name)
    return name or ("img-" + hashlib.sha256(u.encode()).hexdigest()[:12] + ".png")


def main():
    if not REG.exists():
        print("SKIP: the Capture Registry is withdrawn from publication (quarantine/capture-registry-20260812/) and under reconstruction; nothing to process.")
        return 0
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--limit", type=int, default=0)
    a = ap.parse_args()
    if not (a.apply or a.dry_run):
        a.dry_run = True

    r = json.loads(REG.read_text())
    fetched = skipped = failed = already = 0
    bytes_in = 0

    for e in r["entries"]:
        imgs = e.get("imgs") or e.get("images") or []
        if not imgs:
            continue
        slug = e.get("slug", "")
        newpaths, origins = [], list(e.get("imgs_origin") or [])
        changed = False
        for u in imgs:
            if not isinstance(u, str):
                continue
            if u.startswith("data/captures/"):
                newpaths.append(u); already += 1; continue
            full = resolve(u)
            if not full:
                newpaths.append(u); continue
            local = DEST / slug / safe_name(full)
            rel = str(local.relative_to(ROOT))
            if local.exists():
                newpaths.append(rel); already += 1
                if full not in origins: origins.append(full)
                changed = True
                continue
            if a.limit and fetched >= a.limit:
                newpaths.append(u); skipped += 1; continue
            if a.dry_run:
                newpaths.append(u); skipped += 1; continue
            try:
                req = urllib.request.Request(full, headers=UA)
                with urllib.request.urlopen(req, timeout=45) as resp:
                    data = resp.read()
                if len(data) < 500:
                    raise ValueError(f"suspiciously small: {len(data)} bytes")
                local.parent.mkdir(parents=True, exist_ok=True)
                local.write_bytes(data)
                bytes_in += len(data); fetched += 1
                newpaths.append(rel)
                if full not in origins: origins.append(full)
                changed = True
            except Exception as ex:
                print(f"  FAIL {slug}: {type(ex).__name__} {str(ex)[:60]}", file=sys.stderr)
                newpaths.append(u); failed += 1
        if changed and a.apply:
            e["imgs"] = newpaths
            e["imgs_origin"] = origins   # provenance is not replaced by custody

    if a.apply:
        REG.write_text(json.dumps(r, ensure_ascii=False, indent=1))

    print(f"fetched {fetched} ({bytes_in/1024/1024:.1f} MB) · already held {already} · "
          f"skipped {skipped} · failed {failed}")
    if a.dry_run:
        print("(dry run — nothing written)")
    return 1 if failed and not fetched else 0


if __name__ == "__main__":
    sys.exit(main())
