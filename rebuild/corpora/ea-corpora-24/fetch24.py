#!/usr/bin/env python3
"""Stage the files a spec names (session tool). ia: Internet Archive files; file: one URL; pages: every image
an index page links, in the order of its file names.  python3 fetch24.py spec.json <stage>"""
import json, re, sys, pathlib, urllib.parse, urllib.request, time
sys.path.insert(0, str(pathlib.Path(__file__).parent)); from seat import fetch, UA
spec = json.load(open(sys.argv[1])); seat = pathlib.Path(sys.argv[2]) / spec["corpus"]
for it in spec["items"]:
    if it["kind"] == "ia":
        for fn in it["files"]:
            fetch(f"https://archive.org/download/{it['identifier']}/{urllib.parse.quote(fn)}", seat / "original" / it["identifier"] / fn)
    elif it["kind"] == "file":
        fetch(it["url"], seat / "original" / it["path"])
    elif it["kind"] == "pages":
        html = urllib.request.urlopen(urllib.request.Request(it["dir"], headers=UA), timeout=120).read().decode("utf-8", "replace")
        imgs = sorted({h for h in re.findall(r'href="([^"/?]+\.(?:gif|jpg|png))"', html, re.I)})
        for im in imgs:
            fetch(it["dir"] + im, seat / "original" / it["path"] / im)
        print(it["slug"], len(imgs), "pages")
    print("staged", it["slug"], flush=True)
