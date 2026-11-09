"""Check that every quotation a framework definition binds occurs in its record's seated text (or a surface page as cloned)."""
import json, pathlib, re, sys, yaml
ROOT = pathlib.Path("/home/claude/alexanarch"); SITE = pathlib.Path("/tmp/claude-0/-home-claude/97be5201-55d8-50c9-b9d9-c76c8dde5ac6/scratchpad/rf")
REG = {r["deposit_number"]: r for r in json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8"))["deposits"]}
def norm(s): return re.sub(r"\s+", " ", s.replace("*", "").replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"'))
def src(ref):
    if str(ref).startswith("site:"): return (SITE / (ref[5:] + ".txt")).read_text(encoding="utf-8", errors="replace")
    r = REG[int(ref)]; return (ROOT / r["full_text_path"].lstrip("/")).read_text(encoding="utf-8")
d = yaml.safe_load(open(sys.argv[1], encoding="utf-8")); bad = 0; n = 0
def walk(x, path=""):
    # a plain YAML scalar is cut at " #" (a comment); an unbalanced parenthesis marks the cut
    global bad
    if isinstance(x, dict): [walk(v, f"{path}.{k}") for k, v in x.items()]
    elif isinstance(x, list): [walk(v, f"{path}[{i}]") for i, v in enumerate(x)]
    elif isinstance(x, str) and x.count("(") != x.count(")"): print("TRUNCATED?", path, x[-60:]); bad += 1
walk(d)
for c in d["claims"]:
    n += 1
    if norm(c["quote"]) not in norm(src(c["record"])):
        bad += 1; print("MISSING", c["id"], c["record"], c["quote"][:90])
print(f"{n} claims, {bad} missing")
