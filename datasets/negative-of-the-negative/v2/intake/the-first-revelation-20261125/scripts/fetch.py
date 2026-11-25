"""Fetch the field sources of the /non row longinus-on-the-sublime with the row's agent string. One request per URL,
no retry by another route. Text only (the brief: text only, nothing over 2 MB): scripts and styles stripped; the raw response is not kept,
its sha256 recorded; nothing over 2 MB. Writes sources/fetch-records.json.
   /home/claude/shim/python3 -I fetch.py [id=url ...]"""
import subprocess, json, hashlib, datetime, pathlib, re, sys
from html.parser import HTMLParser

INTAKE = pathlib.Path(__file__).resolve().parents[1]
OUT = INTAKE / "sources"; OUT.mkdir(exist_ok=True)
AGENT = "alexanarch-seating/1.0 (https://www.alexanarch.org)"
MAXB = 2_000_000
SCR = pathlib.Path("/tmp/the-first-revelation-scratch"); SCR.mkdir(exist_ok=True)


class T(HTMLParser):
    def __init__(self):
        super().__init__(); self.skip = 0; self.out = []
    def handle_starttag(self, t, a):
        if t in ("script", "style", "noscript", "svg"): self.skip += 1
        if t in ("p", "div", "br", "li", "h1", "h2", "h3", "h4", "h5", "tr", "td", "th", "section", "article", "header",
                 "footer", "blockquote", "dd", "dt", "table", "ul", "ol"): self.out.append("\n")
    def handle_endtag(self, t):
        if t in ("script", "style", "noscript", "svg") and self.skip: self.skip -= 1
        if t in ("p", "div", "li", "h1", "h2", "h3", "h4", "h5", "tr", "td", "th", "blockquote"): self.out.append("\n")
    def handle_data(self, d):
        if not self.skip: self.out.append(d)


def text_of(b, ctype):
    s = b.decode("utf-8", "replace")
    if "html" in (ctype or "") or s.lstrip()[:200].lower().find("<html") >= 0 or "<!doctype" in s[:200].lower():
        p = T(); p.feed(s); s = "".join(p.out)
    lines = [re.sub(r"[ \t\r\f\v]+", " ", l).strip() for l in s.split("\n")]
    return "\n".join(l for l in lines if l)


def sha(b): return hashlib.sha256(b).hexdigest()


def run(jobs):
    p = OUT / "fetch-records.json"
    recs = json.loads(p.read_text()) if p.exists() else {}
    for sid, url in jobs:
        at = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        raw = SCR / ("the-first-revelation-" + sid + ".raw")
        r = subprocess.run(["curl", "-sS", "-L", "--max-time", "60", "--max-filesize", str(MAXB), "-A", AGENT, "-o", str(raw),
                            "-w", "%{http_code} %{url_effective} %{content_type}", url], capture_output=True, text=True)
        code, eff, ctype = (r.stdout.split(" ", 2) + ["", "", ""])[:3]
        rec = {"url": url, "at": at, "http": int(code) if code.isdigit() else None, "final_url": eff, "content_type": ctype,
               "agent": AGENT, "curl_err": r.stderr.strip() or None, "files": {},
               "kind": "text only (raw not kept: disk); raw sha256 recorded; one request, no retry by another route"}
        b = raw.read_bytes() if raw.exists() else b""
        rec["bytes"] = len(b); rec["raw_sha256"] = sha(b) if b else None
        if b and rec["http"] == 200:
            txt = text_of(b, ctype).encode("utf-8")
            (OUT / (sid + ".txt")).write_bytes(txt); rec["files"][sid + ".txt"] = sha(txt)
            rec["text_bytes"] = len(txt)
        elif b:
            rec["body_head"] = text_of(b, ctype)[:300]
        raw.unlink(missing_ok=True)
        recs[sid] = rec
        print(sid, rec["http"], rec["bytes"], eff[:110])
    p.write_text(json.dumps(recs, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    run([tuple(a.split("=", 1)) for a in sys.argv[1:]])
