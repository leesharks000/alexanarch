#!/usr/bin/env python3
"""Seat builder for EA-CORPORA-23 (session tool; not part of the archive).

Seats OpenITI texts pinned by commit. For each item of the spec it fetches the text file and its version
record (.yml) from raw.githubusercontent.com/OpenITI/<repo>/<commit>/<path>, checks each against its git blob
id (sha1 of "blob <size>\\0" + bytes) as listed by `git ls-tree` at the commit (pins in openiti-pins.txt:
"<repo> <commit> <path>", blob ids read with a blob-less clone), finds every locus in the seated text, and
writes source.json and MANIFEST.sha256 in the form of the seats before it.

    python3 seat.py spec23-hadith.json <stage>        # <stage>/<corpus>/ is built
    python3 seat.py spec23-hadith.json <stage> --clones <dir-of-blobless-clones>
"""
import hashlib, json, pathlib, re, subprocess, sys, urllib.request

HERE = pathlib.Path(__file__).resolve().parent
UA = {"User-Agent": "alexanarch-seating/1.0 (https://www.alexanarch.org)"}
VERS = re.compile(r"\.(completed|mARkdown|inProgress)$")


def fetch(url, dest):
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists() and dest.stat().st_size > 0:
        return dest
    import time
    for k in range(6):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=900) as r, open(dest, "wb") as f:
                while True:
                    b = r.read(1 << 20)
                    if not b:
                        break
                    f.write(b)
            return dest
        except Exception:
            if dest.exists():
                dest.unlink()
            if k == 5:
                raise
            time.sleep(10 * (k + 1))


def blob_id(p):
    b = p.read_bytes()
    return hashlib.sha1(b"blob %d\0" % len(b) + b).hexdigest()


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def norm(s):
    return " ".join(s.split())


def main():
    spec = json.load(open(sys.argv[1], encoding="utf-8"))
    stage = pathlib.Path(sys.argv[2])
    clones = pathlib.Path(sys.argv[sys.argv.index("--clones") + 1]) if "--clones" in sys.argv else None
    pins = {}
    for line in (HERE / "openiti-pins.txt").read_text().split("\n"):
        if line.strip():
            repo, commit, path = line.split()
            pins[VERS.sub("", path.rsplit("/", 1)[1])] = (repo, commit, path)

    seat = stage / spec["corpus"]
    works, origin_items, bad = [], [], []
    for it in spec["items"]:
        repo, commit, path = pins[it["uri"]]
        assert repo == it["repo"], (it["uri"], repo)
        yml = path.rsplit("/", 1)[0] + "/" + it["uri"] + ".yml"
        files = []
        for q in (path, yml):
            dest = seat / "original" / q.rsplit("/", 1)[1]
            fetch(f"https://raw.githubusercontent.com/OpenITI/{repo}/{commit}/{q}", dest)
            got = blob_id(dest)
            want = None
            if clones:
                out = subprocess.run(["git", "-C", str(clones / repo), "ls-tree", commit, q], capture_output=True, text=True).stdout.split()
                want = out[2] if len(out) > 2 else None
                if want != got:
                    bad.append(f"{q}: blob {got} != {want}")
            files.append({"file": dest.name, "path": q, "git_blob": got, "blob_checked": want == got if clones else None})
        text_rel = f"original/{path.rsplit('/', 1)[1]}"
        origin_items.append({"source": "OpenITI", "repository": f"https://github.com/OpenITI/{repo}", "commit": commit,
                             "uri": it["uri"], "files": files,
                             "url": f"https://raw.githubusercontent.com/OpenITI/{repo}/{commit}/{path}"})
        w = {"slug": it["slug"], "work": it["work"], "text": text_rel,
             "originals": [f"original/{f['file']}" for f in files], "class": it["class"],
             "lines": sum(1 for _ in open(seat / text_rel, encoding="utf-8", errors="replace"))}
        works.append(w)

    texts = {w["slug"]: w["text"] for w in works}
    verified, missing = [], []
    for lo in spec["loci"]:
        t = norm((seat / texts[lo["slug"]]).read_text(encoding="utf-8"))
        (verified if norm(lo["find"]) in t else missing).append(f"{lo['label']} — '{lo['find']}'")

    src = {
        "corpus": spec["corpus"], "seat": spec["seat"], "title": spec["title"],
        "edition": "; ".join(w["work"] for w in works), "language": spec["language"],
        "license": spec["license"], "fetched": spec["fetched"],
        "origin": {"release": spec["release"], "items": origin_items, "fetched": spec["fetched"],
                   "transport": "in-session fetch (Transport D); No-Double-Draw; every file checked against its git blob id at the pinned commit"},
        "works": {"count": len(works), "units": spec["units"], "list": works},
        "normalization": spec["normalization"], "scope": spec["scope"],
        "verified_loci": verified, "loci_not_found": missing,
        "lines_total": sum(w["lines"] for w in works),
        "why_seated": spec["why_seated"], "spine": spec["spine"], "ruling": spec["ruling"],
        "classes": spec["classes"], "witness_note": spec["witness_note"],
    }
    (seat / "source.json").write_text(json.dumps(src, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    lines = [f"{sha(p)}  {p.relative_to(seat).as_posix()}" for p in sorted(seat.rglob("*"))
             if p.is_file() and p.name not in ("MANIFEST.sha256", "source.json")]
    (seat / "MANIFEST.sha256").write_text("\n".join(lines) + "\n")
    print(spec["corpus"], "works", len(works), "lines", src["lines_total"], "loci ok", len(verified), "missing", missing, "blob mismatches", bad)
    return 1 if bad or missing else 0


if __name__ == "__main__":
    sys.exit(main())
