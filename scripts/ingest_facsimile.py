#!/usr/bin/env python3
"""Take custody of a deposit's attachments and, for PDF-only work, build its body.

  python3 scripts/ingest_facsimile.py --deposit N

WHAT THIS FIXES, and it is one defect wearing three faces.

Deposit #1539 arrived as a handwritten paper: eleven photographed pages, no text.
The mint recorded the attachment's URL and moved on. The record then said
"Binary attachment preserved at deposit time" while THE ARCHIVE HELD NOTHING —
the work lived on a third party's CDN behind a five-minute signed credential.
The Full Text section described the work instead of being it. And /papers/ 404'd,
because the renderer builds from body text and there was none.

An archive founded because a platform deleted 862 works cannot accept a deposit
and leave the work on someone else's server. Custody is the first obligation, not
a later enrichment.

WHAT IT DOES

  1. CUSTODY. Downloads each attachment to data/attachments/AXN-{hex}/, hashes it,
     records archive_path + sha256 + size on the registry entry, and writes
     MANIFEST.sha256. Filenames are preserved as submitted — the mint's sanitiser
     reduced 手書き論文197-多層切替による中心秘匿構造2026.07.30.pdf to
     "197-.2026.07.30.pdf", stripping the title from a Japanese author's file.

  2. BODY. If the deposit has no text body and its only content is a PDF, rasterises
     the pages into data/attachments/AXN-{hex}/pages/ and writes a canonical body of
     image references. THE FULL TEXT FIELD THEN CONTAINS THE FULL TEXT — the pages —
     rather than a description of where to find it.

  3. READER. Calls build_facsimile_reader.py for page-at-a-time navigation.

WHAT IT REFUSES TO DO

  It does not transcribe. A transcription of an author's handwriting is an editorial
  act on their work and is not the archive's to make. The facsimile is the primary
  source and is presented as deposited: un-OCR'd, untranscribed, unreflowed.

  It does not overwrite an existing body. If a deposit already has text, the text is
  the body and this touches only custody.
"""
import argparse, hashlib, json, os, re, shutil, subprocess, sys, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
UA = {"User-Agent": "alexanarch-ingest/1.0 (+https://alexanarch.org)"}
FACSIMILE_CLASS = "primary-source-facsimile"


def _fetch(url: str, token: str | None = None) -> bytes:
    h = dict(UA)
    if token and "github.com" in url:
        h["Authorization"] = f"Bearer {token}"
    return urllib.request.urlopen(urllib.request.Request(url, headers=h), timeout=300).read()


def _clean_name(name: str, fallback: str) -> str:
    """Keep the author's filename. Strip only path separators and control bytes."""
    name = os.path.basename(name or "").strip()
    name = re.sub(r'[\x00-\x1f/\\]', "", name)
    return name or fallback


def ingest(n: int, token: str | None = None, dpi: int = 150) -> None:
    reg_path = ROOT / "data/registry.json"
    reg = json.loads(reg_path.read_text(encoding="utf-8"))
    dep = next(d for d in reg["deposits"] if d["deposit_number"] == n)
    hex_id = str(dep.get("hex") or dep["axn"].split(":")[1].split(".")[0]).zfill(4)
    atts = dep.get("attachments") or []
    if not atts:
        print(f"#{n}: no attachments")
        return

    outdir = ROOT / "data/attachments" / f"AXN-{hex_id}"
    outdir.mkdir(parents=True, exist_ok=True)
    changed = False

    for att in atts:
        if att.get("archive_path") and (ROOT / str(att["archive_path"]).lstrip("/")).exists():
            print(f"#{n}: already held — {att.get('filename')}")
            continue
        url = att.get("url")
        if not url:
            continue
        fname = _clean_name(att.get("filename", ""), f"AXN-{hex_id}-attachment")
        try:
            blob = _fetch(url, token)
        except Exception as e:
            att["ingestion_error"] = f"{type(e).__name__}: {e}"
            att["ingested_inline"] = False
            print(f"#{n}: FETCH FAILED for {fname} — {e}")
            print("      The deposit stands; custody does not. Recorded as an error "
                  "rather than a claim of preservation.")
            changed = True
            continue
        (outdir / fname).write_bytes(blob)
        sha = hashlib.sha256(blob).hexdigest()
        att.update({
            "filename": fname,
            "archive_path": f"/data/attachments/AXN-{hex_id}/{fname}",
            "size": len(blob),
            "sha256": sha,
            "md5": hashlib.md5(blob).hexdigest(),
            "ingested_inline": True,
            "ingestion_error": None,
        })
        changed = True
        print(f"#{n}: custody taken — {fname} ({len(blob):,} bytes, sha256 {sha[:16]}…)")

    lines = []
    for f in sorted(outdir.iterdir()):
        if f.is_file() and f.name != "MANIFEST.sha256":
            lines.append(f"{hashlib.sha256(f.read_bytes()).hexdigest()}  {f.name}")
    if lines:
        (outdir / "MANIFEST.sha256").write_text("\n".join(lines) + "\n", encoding="utf-8")

    # ── body, only when there is none and the work is a PDF
    body_path = ROOT / f"data/texts/AXN-{hex_id}-text.md"
    existing = body_path.read_text(encoding="utf-8") if body_path.exists() else ""
    stripped = re.sub(r"^---\n.*?\n---\n", "", existing, count=1, flags=re.S).strip()
    has_text = len(re.sub(r"!\[[^\]]*\]\([^)]*\)", "", stripped).split()) > 60

    pdfs = [a for a in atts if str(a.get("archive_path", "")).lower().endswith(".pdf")]
    if pdfs and not has_text:
        src = ROOT / str(pdfs[0]["archive_path"]).lstrip("/")
        pages = outdir / "pages"
        if pages.exists():
            shutil.rmtree(pages)
        pages.mkdir(parents=True, exist_ok=True)
        subprocess.run(["pdftoppm", "-jpeg", "-r", str(dpi), "-jpegopt", "quality=88",
                        str(src), str(pages / "p")], check=True,
                       stderr=subprocess.DEVNULL)
        for f in sorted(pages.glob("p-*.jpg")):
            f.rename(pages / f"p-{int(f.stem.split('-')[1]):03d}.jpg")
        n_pages = len(list(pages.glob("*.jpg")))

        fm = re.match(r"^---\n.*?\n---\n", existing, flags=re.S)
        front = fm.group(0) if fm else (
            f"---\ndeposit_number: {n}\nhex: {hex_id}\n"
            f"title: {dep.get('title','')}\ncreator: {dep.get('creator','')}\n"
            f"body_status: {FACSIMILE_CLASS}\n---\n")
        imgs = "\n\n".join(
            f"![{dep.get('title','')} — page {i} of {n_pages}]"
            f"(/data/attachments/AXN-{hex_id}/pages/p-{i:03d}.jpg)"
            for i in range(1, n_pages + 1))
        att0 = pdfs[0]
        body = (f"{front}\n{imgs}\n\n---\n\nPresented as deposited — un-OCR'd, "
                f"untranscribed, unreflowed. The document is the work.\n\n"
                f"[Page reader](/read/{n}/) · "
                f"[original PDF]({att0['archive_path']}) · "
                f"{n_pages} pages · {att0['size']:,} bytes · "
                f"SHA-256 `{att0['sha256']}`\n")
        body_path.write_text(body, encoding="utf-8")
        dep["body_status"] = {
            "class": FACSIMILE_CLASS,
            "note": ("The work is a document, not text. Page images are the canonical "
                     "body; no transcription is made, and none is implied."),
        }
        dep["full_text_path"] = f"/data/texts/AXN-{hex_id}-text.md"
        changed = True
        print(f"#{n}: body built — {n_pages} page images, no transcription")

        subprocess.run([sys.executable, str(ROOT / "scripts/build_facsimile_reader.py"),
                        "--deposit", str(n)], check=False)

    if changed:
        reg_path.write_text(json.dumps(reg, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"#{n}: registry updated")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--deposit", type=int, required=True)
    ap.add_argument("--dpi", type=int, default=150)
    args = ap.parse_args()
    ingest(args.deposit, os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN"), args.dpi)
