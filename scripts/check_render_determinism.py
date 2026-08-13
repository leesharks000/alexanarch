#!/usr/bin/env python3
"""check_render_determinism.py — the same record must render the same every time.

MANUS: "locked in populating to render & machine-facing — those records appear
the same every time."

Builds the gallery TWICE from unchanged inputs and compares the bytes. Any
difference means something non-deterministic is leaking into the render — a dict
iteration order, a timestamp, a set, a hash seed — and a registry whose public
surface changes without its data changing cannot support a longitudinal claim.
The whole instrument rests on being able to say a thing was different ON A DATE,
not different on a rebuild.
"""
import subprocess, hashlib, pathlib, sys, shutil

ROOT = pathlib.Path(__file__).resolve().parents[1]
PAGE = ROOT / "captures/index.html"


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def build():
    r = subprocess.run([sys.executable, "scripts/build_capture_gallery.py"],
                       cwd=ROOT, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stdout + r.stderr)
        raise SystemExit("build failed")


build(); a = sha(PAGE); shutil.copy(PAGE, "/tmp/_det_a.html")
build(); b = sha(PAGE)
if a != b:
    subprocess.run(["diff", "/tmp/_det_a.html", str(PAGE)], capture_output=True, text=True)
    print("NON-DETERMINISTIC RENDER")
    print("  build 1: %s" % a)
    print("  build 2: %s" % b)
    raise SystemExit(1)
print("render determinism: two builds byte-identical")
print("  sha256 %s" % a)
