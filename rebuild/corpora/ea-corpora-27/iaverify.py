import json,sys,hashlib,pathlib,urllib.request
seat=pathlib.Path(sys.argv[1]); bad=0
for d in sorted((seat/"original").iterdir()):
    if not d.is_dir(): continue
    try: meta=json.load(urllib.request.urlopen(f"https://archive.org/metadata/{d.name}",timeout=60))
    except Exception: continue
    m={f["name"]:f for f in meta.get("files",[])}
    if not m: continue
    for f in sorted(d.iterdir()):
        md=hashlib.md5(f.read_bytes()).hexdigest()
        ok=m.get(f.name,{}).get("md5")==md
        bad+= not ok
        print("ok " if ok else "BAD", d.name+"/"+f.name, f.stat().st_size, m.get(f.name,{}).get("size"))
print("mismatches:",bad)
