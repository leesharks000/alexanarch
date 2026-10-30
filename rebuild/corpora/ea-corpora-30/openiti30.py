#!/usr/bin/env python3
"""EA-CORPORA-30 (session tool): build29.py with one reducer added, for OpenITI mARkdown files.

An item of kind "file" that carries "openiti" ({repository, commit, file, licence}) is fetched from
raw.githubusercontent.com pinned to the commit and kept under original/ as fetched. Its text layer
text/<slug>.txt is derived by code:
  - the #META# header, up to and including '#META#Header#End#', is dropped (it stays in the original);
  - '### | heading' lines (any number of '|') become '=== heading ===';
  - a line opening '# ' starts a paragraph; a line opening '~~' continues the line before it, joined with a space;
  - page markers 'PageV01P023' become '[V01P023]' on a line of their own;
  - milestones 'ms123' are dropped.
Nothing else is changed: OCR errors in the files stay as OpenITI has them.
All other items, and --loci, go to build29.py unchanged.
    python3 openiti30.py <spec.json> <stage> [--loci]"""
import json, pathlib, re, sys
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "ea-corpora-29"))
import build29 as B

S = B.S
_orig_build = S.build


def reduce_markdown(raw):
    t = raw.replace("\r\n", "\n")
    k = t.find("#META#Header#End#")
    if k >= 0:
        t = t[k + len("#META#Header#End#"):]
    out = []
    for line in t.split("\n"):
        line = re.sub(r"\bms\d+\b", "", line)
        pages = re.findall(r"PageV(\d+)P(\d+)", line)
        line = re.sub(r"PageV\d+P\d+", "", line)
        s = line.strip()
        if s.startswith("###"):
            h = s.lstrip("#").strip().strip("|").strip()
            h = re.sub(r"^\|+\s*", "", h)
            out.append(f"=== {h} ===" if h else "")
        elif s.startswith("~~"):
            c = s[2:].strip()
            if out and out[-1] and not out[-1].startswith(("===", "[V")):
                out[-1] = (out[-1] + " " + c).strip()
            else:
                out.append(c)
        elif s.startswith("# "):
            out.append(s[2:].strip())
        elif s == "#":
            out.append("")
        else:
            out.append(s)
        for v, p in pages:
            out.append(f"[V{v}P{p}]")
    txt = "\n".join(out)
    txt = re.sub(r"[ \t]+", " ", txt)
    txt = re.sub(r"\n{3,}", "\n\n", txt)
    return txt.strip() + "\n"


def build(sub, stage):
    it = sub["items"][0]
    if not it.get("openiti"):
        return _orig_build(sub, stage)
    seat = pathlib.Path(stage) / sub["corpus"]
    o = it["openiti"]
    url = f"https://raw.githubusercontent.com/OpenITI/{o['repository']}/{o['commit']}/{o['file']}"
    dest = seat / "original" / it["path"]
    S.fetch(url, dest)
    tr = f"text/{it['slug']}.txt"
    (seat / "text").mkdir(parents=True, exist_ok=True)
    (seat / tr).write_text(reduce_markdown(dest.read_bytes().decode("utf-8")), encoding="utf-8")
    origin = {"source": "OpenITI", "url": url, "repository": f"https://github.com/OpenITI/{o['repository']}", "commit": o["commit"],
              "file": o["file"], "sha256": S.sha(dest), "licence_at_file": o.get("licence", "CC BY-NC-SA 4.0 (OpenITI corpus licence)")}
    for k in ("edition_at_file", "openiti_status"):
        if o.get(k):
            origin[k] = o[k]
    w = {"slug": it["slug"], "work": it["work"], "text": tr, "originals": [f"original/{it['path']}"],
         "lines": sum(1 for _ in open(seat / tr, encoding="utf-8"))}
    if it.get("class"):
        w["class"] = it["class"]
    return {"works": {"list": [w]}, "origin": {"items": [origin]}}


S.build = build

if __name__ == "__main__":
    spec = json.load(open(sys.argv[1]))
    s = B.reloci(spec, sys.argv[2]) if "--loci" in sys.argv else B.build(spec, sys.argv[2])
    print(spec["corpus"], "works", s["works"]["count"], "lines", s["lines_total"], "loci ok", len(s["verified_loci"]), "missing", s["loci_not_found"])
