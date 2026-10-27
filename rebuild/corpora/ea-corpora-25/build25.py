#!/usr/bin/env python3
"""Seat builder for EA-CORPORA-25 (session tool; not part of the archive): the archive's own critical
editions of the Waltian canon, seated as 03/02 (Pearl and Other Poems) was: deposited in the archive that
seats them, no external fetch. Each seat holds (1) the canonical bytes of the edition's record, copied
from data/texts/ and checked against the registry's hash, and (2) the files of the edition as published
at secretbookofwalt.org, copied from the repository `secret-book-of-walt` at a pinned commit and checked
against `git ls-tree` there. Loci are strings found in the seated text.
    python3 build25.py <alexanarch> <secret-book-of-walt checkout>"""
import hashlib, json, pathlib, shutil, subprocess, sys

ROOT = pathlib.Path(sys.argv[1]); SITE = pathlib.Path(sys.argv[2])
SPEC = json.loads((pathlib.Path(__file__).with_name("spec25.json")).read_text(encoding="utf-8"))
COMMIT = subprocess.run(["git", "-C", str(SITE), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
REG = {d["deposit_number"]: d for d in json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8"))["deposits"]}
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
blob = lambda p: hashlib.sha1(b"blob %d\0" % p.stat().st_size + p.read_bytes()).hexdigest()
norm = lambda s: " ".join(s.split())

for st in SPEC["seats"]:
    seat = ROOT / "data/corpora" / st["corpus"]
    if seat.exists():
        shutil.rmtree(seat)
    (seat / "original/record").mkdir(parents=True); (seat / "original/site").mkdir(parents=True)
    works, origin = [], []
    for n in st["records"]:
        d = REG[n]; src = ROOT / d["full_text_path"].lstrip("/"); dst = seat / "original/record" / src.name
        shutil.copyfile(src, dst)
        h = sha(dst)
        origin.append({"source": "Alexanarch deposit", "deposit": n, "axn": d["axn"], "title": d["title"],
                       "file": f"original/record/{src.name}", "sha256": h, "registry_hash": d["hash"],
                       "hash_agrees": h == d["hash"],
                       **({"body_status_note": st["hash_notes"][str(n)]} if str(n) in st.get("hash_notes", {}) else {})})
        works.append({"slug": f"record-{n}", "work": f"#{n} · {d['axn']} — {d['title']}", "text": f"original/record/{src.name}",
                      "originals": [f"original/record/{src.name}"], "class": "the edition's record",
                      "lines": sum(1 for _ in open(dst, encoding="utf-8"))})
    for rel in st["site_files"]:
        src = SITE / rel; dst = seat / "original/site" / rel
        dst.parent.mkdir(parents=True, exist_ok=True); shutil.copyfile(src, dst)
        ls = subprocess.run(["git", "-C", str(SITE), "ls-tree", COMMIT, rel], capture_output=True, text=True).stdout.split()
        origin.append({"source": "secret-book-of-walt repository (secretbookofwalt.org)", "repository": "https://github.com/leesharks000/secret-book-of-walt",
                       "commit": COMMIT, "path": rel, "git_blob": blob(dst), "blob_agrees": len(ls) > 2 and ls[2] == blob(dst)})
        w = {"slug": "site-" + rel.replace("/", "-"), "work": f"secretbookofwalt.org, {rel}", "text": None,
             "originals": [f"original/site/{rel}"], "class": "the edition as published on the site"}
        if rel.endswith((".md", ".json")):
            w["text"] = f"original/site/{rel}"; w["lines"] = sum(1 for _ in open(dst, encoding="utf-8"))
        works.append(w)
    texts = {w["slug"]: w["text"] for w in works}
    verified, missing = [], []
    for lo in st["loci"]:
        t = norm((seat / texts[lo["in"]]).read_text(encoding="utf-8"))
        (verified if norm(lo["find"]) in t else missing).append(f"{lo['label']} — '{lo['find']}'")
    src = {"corpus": st["corpus"], "seat": st["seat"], "title": st["title"], "edition": st["edition"],
           "language": st.get("language", "eng"), "license": SPEC["license"], "fetched": SPEC["fetched"],
           "origin": {"items": origin, "provenance": SPEC["provenance"], "fetched": SPEC["fetched"],
                      "transport": "local copy from the archive and the site repository (Transport D); No-Double-Draw"},
           "works": {"count": len(works), "units": "the record's canonical bytes, and the site's files of the edition", "list": works},
           "normalization": SPEC["normalization"], "scope": st["scope"], "verified_loci": verified, "loci_not_found": missing,
           "lines_total": sum(w.get("lines", 0) for w in works), "why_seated": st["why_seated"], "spine": st["spine"],
           "ruling": SPEC["ruling"]}
    for k in ("binds", "declared_absences"):
        if st.get(k):
            src[k] = st[k]
    (seat / "source.json").write_text(json.dumps(src, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    lines = [f"{sha(p)}  {p.relative_to(seat).as_posix()}" for p in sorted(seat.rglob("*"))
             if p.is_file() and p.name not in ("MANIFEST.sha256", "source.json")]
    (seat / "MANIFEST.sha256").write_text("\n".join(lines) + "\n")
    bad = [o for o in origin if o.get("hash_agrees") is False or o.get("blob_agrees") is False]
    print(st["corpus"], len(works), "works", src["lines_total"], "lines; loci", len(verified), "missing", missing,
          "; disagreements:", [o.get("deposit") or o.get("path") for o in bad])
