"""Split the operator's paste of 2026-10-29 into its captures: query, answer, source cards, operator notes. Nothing is reworded."""
import json, re, pathlib
H = pathlib.Path(__file__).resolve().parent
raw = (H / "paste-aio-20261029.txt").read_text(encoding="utf-8")
raw = re.sub(r"^<system-reminder>.*?</system-reminder>", "", raw, flags=re.S)
raw = raw.replace('@"/mnt/user-data/attachments/97be5201-55d8-50c9-b9d9-c76c8dde5ac6/bddfeb27-attachment.txt" ', "", 1)
raw += "\n\n" + (H / "paste-pwc-active-aio-20261029.txt").read_text(encoding="utf-8")
parts = re.split(r"AI Mode Conversation\s*\n+\s*You said: ", raw)
segs = []
notes = []
for p in parts[1:]:
    note = None
    m = re.search(r"\s\$\s*(.*?)\s*$", p, flags=re.S)
    body = p
    if m and p.rstrip().endswith((":", "$")) or (m and len(m.group(1)) < 200 and "$" in p[-220:]):
        idx = p.rfind("$")
        tail = p[idx + 1:].strip()
        body = p[:idx]
        note = tail or None
    segs.append({"body": body.strip(), "note_after": note})
out = []
for i, s in enumerate(segs):
    b = s["body"]; first, rest = b.split("\n", 1)
    first = first.strip()
    q = first[:len(first) // 2]
    assert first == q + q, (i, first)
    out.append({"i": i, "q": q, "text": rest.strip(), "operator_note_before": segs[i - 1]["note_after"] if i else None})
json.dump(out, open(H / "segments.json", "w"), ensure_ascii=False, indent=1)
for o in out: print(o["i"], repr(o["q"]), len(o["text"]), "| note:", o["operator_note_before"])
