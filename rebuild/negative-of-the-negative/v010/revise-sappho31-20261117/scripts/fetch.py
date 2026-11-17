"""Fetch the field sources of the Sappho 31 row (B1-B5) with the row's agent string, to verify the field ledger's quotes
by script against saved text. One request per URL, no retry by another route. Text only (disk): scripts and styles
stripped; the raw response is not kept, its sha256 recorded. Writes sources/fetch-records.json.
   /tmp/py312/python3 fetch.py"""
import subprocess, json, hashlib, datetime, pathlib, re
from html.parser import HTMLParser

STAGE = pathlib.Path(__file__).resolve().parents[1]
OUT = STAGE / "sources"; OUT.mkdir(exist_ok=True)
AGENT = "Mozilla/5.0 (compatible; alexanarch-non)"
JOBS = [
    ("B1-wikipedia-sappho-31", "https://en.wikipedia.org/wiki/Sappho_31"),
    ("B2-literary-matters", "https://www.literarymatters.org/1-1-sappho-31/"),
    ("B3-slowdown", "https://www.slowdownshow.org/episode/2024/08/16/1185-fragment-31-by-sappho-translated-by-christopher-childers"),
    ("B4-norton", "https://nerd.wwnorton.com/ebooks/epub/worldlit5/EPUB/content/1.2.3.0.0.0-chapter04.xhtml"),
    ("B5-edubirdie", "https://hub.edubirdie.com/examples/analysis-of-sapphos-fragment-31-in-the-light-of-jealousy-the-triangle-of-desire-and-erotic-longing/"),
]
MAXB = 2_000_000


class T(HTMLParser):
    def __init__(self):
        super().__init__(); self.skip = 0; self.out = []
    def handle_starttag(self, t, a):
        if t in ("script", "style", "noscript", "svg"): self.skip += 1
        if t in ("p", "div", "br", "li", "h1", "h2", "h3", "h4", "tr", "section", "article", "header", "footer", "blockquote", "dd", "dt"): self.out.append("\n")
    def handle_endtag(self, t):
        if t in ("script", "style", "noscript", "svg") and self.skip: self.skip -= 1
    def handle_data(self, d):
        if not self.skip: self.out.append(d)


def text_of(b):
    p = T(); p.feed(b.decode("utf-8", "replace"))
    s = "".join(p.out)
    lines = [re.sub(r"[ \t\r\f\v]+", " ", l).strip() for l in s.split("\n")]
    return "\n".join(l for l in lines if l)


def sha(b): return hashlib.sha256(b).hexdigest()


def run(jobs):
    recs = {}
    p = OUT / "fetch-records.json"
    if p.exists(): recs = json.loads(p.read_text())
    for sid, url in jobs:
        at = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        raw = OUT / (sid + ".raw")
        r = subprocess.run(["curl", "-sS", "-L", "--max-time", "60", "--max-filesize", str(MAXB), "-A", AGENT, "-o", str(raw),
                            "-w", "%{http_code} %{url_effective} %{content_type}", url], capture_output=True, text=True)
        code, eff, ctype = (r.stdout.split(" ", 2) + ["", "", ""])[:3]
        rec = {"url": url, "at": at, "http": int(code) if code.isdigit() else None, "final_url": eff, "content_type": ctype,
               "agent": AGENT, "curl_err": r.stderr.strip() or None, "files": {}, "kind": "text only (raw not kept: disk); raw sha256 recorded"}
        b = raw.read_bytes() if raw.exists() else b""
        rec["bytes"] = len(b); rec["raw_sha256"] = sha(b) if b else None
        if b and rec["http"] == 200:
            txt = text_of(b).encode("utf-8")
            (OUT / (sid + ".txt")).write_bytes(txt); rec["files"][sid + ".txt"] = sha(txt)
        raw.unlink(missing_ok=True)
        recs[sid] = rec
        print(sid, rec["http"], rec["bytes"], eff[:100])
    p.write_text(json.dumps(recs, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    import sys
    run(JOBS if len(sys.argv) == 1 else [tuple(a.split("=", 1)) for a in sys.argv[1:]])
