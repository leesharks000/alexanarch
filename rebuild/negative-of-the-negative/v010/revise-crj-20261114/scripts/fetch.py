"""Fetch the B_R sources #1769 §6.5.1 cites (and one retry of the journal's own pages) with the row's agent string.
One request per URL, no retry by another route. Saves <id>.txt (scripts/styles stripped) and, where small, <id>.html; a PDF is saved
as text only (pdftotext). Writes sources/fetch-records.json.   python3.12 fetch.py"""
import subprocess, json, hashlib, datetime, pathlib, re, html
from html.parser import HTMLParser

STAGE = pathlib.Path(__file__).resolve().parents[1]
OUT = STAGE / "sources"; OUT.mkdir(exist_ok=True)
AGENT = "Mozilla/5.0 (compatible; alexanarch-non)"
JOBS = [
    ("oup-ai-disclosure", "https://corp.oup.com/news/supporting-researchers-to-disclose-ai-use-with-confidence/"),
    ("camws-ajcr", "https://camws.org/ajcr"),
    ("newvoices", "https://fass.open.ac.uk/research/newvoices"),
    ("crsn-cfp", "https://classicalreception.org/cfp-literary-reception-and-human-creativity-in-the-age-of-ai/"),
    ("ijct-future-pasts", "https://doi.org/10.1007/s12138-026-00750-7"),
    ("ora-postcolonial-sparagmos", "https://ora.ox.ac.uk/objects/uuid%3Aa2e18976-942c-4f25-aae5-39ee9db0d5ba/files/rx633f145r"),
    ("crj-about", "https://academic.oup.com/crj/pages/About"),
    ("crj-general-instructions", "https://academic.oup.com/crj/pages/General_Instructions"),
]


class T(HTMLParser):
    def __init__(self):
        super().__init__(); self.skip = 0; self.out = []
    def handle_starttag(self, t, a):
        if t in ("script", "style", "noscript", "svg"): self.skip += 1
        if t in ("p", "div", "br", "li", "h1", "h2", "h3", "h4", "tr", "section", "article", "header", "footer"): self.out.append("\n")
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


recs = {}
for sid, url in JOBS:
    at = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    raw = OUT / (sid + ".raw")
    r = subprocess.run(["curl", "-sS", "-L", "--max-time", "60", "-A", AGENT, "-o", str(raw), "-w", "%{http_code} %{url_effective} %{content_type}", url],
                       capture_output=True, text=True)
    code, eff, ctype = (r.stdout.split(" ", 2) + ["", "", ""])[:3]
    rec = {"url": url, "at": at, "http": int(code) if code.isdigit() else None, "final_url": eff, "content_type": ctype,
           "agent": AGENT, "curl_err": r.stderr.strip() or None, "files": {}}
    b = raw.read_bytes() if raw.exists() else b""
    rec["bytes"] = len(b); rec["raw_sha256"] = sha(b) if b else None
    if b:
        if b[:4] == b"%PDF":
            txt = subprocess.run(["pdftotext", "-layout", str(raw), "-"], capture_output=True).stdout
            (OUT / (sid + ".txt")).write_bytes(txt); rec["files"][sid + ".txt"] = sha(txt); rec["kind"] = "pdf (raw not kept; text by pdftotext -layout)"
        else:
            txt = text_of(b).encode("utf-8")
            (OUT / (sid + ".txt")).write_bytes(txt); rec["files"][sid + ".txt"] = sha(txt)
            if len(b) <= 250_000:
                (OUT / (sid + ".html")).write_bytes(b); rec["files"][sid + ".html"] = sha(b)
            else:
                rec["kind"] = "html over 250 KB: raw not kept (disk), its sha256 recorded"
    raw.unlink(missing_ok=True)
    recs[sid] = rec
    print(sid, rec["http"], rec["bytes"], eff[:100])
(OUT / "fetch-records.json").write_text(json.dumps(recs, ensure_ascii=False, indent=1), encoding="utf-8")
