#!/usr/bin/env python3
"""EA-CORPORA-29 (session tool): Wikisource by its HTML pages (the API answers 429 to this session's address).

    ws.py search <lang> <query>            titles from the site's own search page
    ws.py fetch <lang> <title> <dest_dir>  the page as served (HTML), its revision id, and a text layer

The fetch keeps the served HTML as the original (<slug>.html), records the page's revision id (wgCurRevisionId)
and its permanent link, and derives text/<slug>.txt from the parser output by code: paragraphs, verse lines and
headings kept, navigation, edit links, references and page-number markers dropped."""
import html, json, re, sys, time, urllib.parse, urllib.request, pathlib, hashlib

UA = {"User-Agent": "alexanarch-seating/1.0 (https://www.alexanarch.org; leesharks000@users.noreply.github.com)"}


def get(url, tries=6):
    for k in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=120) as r:
                return r.read()
        except Exception as e:
            if k == tries - 1:
                raise
            time.sleep(8 * (k + 1))


def search(lang, q, n=20):
    u = f"https://{lang}.wikisource.org/w/index.php?" + urllib.parse.urlencode({"search": q, "fulltext": "1", "limit": n, "ns0": "1"})
    h = get(u).decode("utf-8", "replace")
    return [html.unescape(t) for t in re.findall(r'mw-search-result-heading"><a href="[^"]*" title="([^"]*)"', h)]


def text_of(page_html):
    m = re.search(r'<div class="mw-content-ltr mw-parser-output"[^>]*>(.*)<div class="printfooter"', page_html, re.S) or \
        re.search(r'<div class="mw-parser-output"[^>]*>(.*?)<div class="printfooter"', page_html, re.S) or \
        re.search(r'id="mw-content-text"[^>]*>(.*?)<div id="catlinks"', page_html, re.S)
    body = m.group(1) if m else page_html
    for pat in (r'<style.*?</style>', r'<script.*?</script>', r'<span class="mw-editsection">.*?</span></span>',
                r'<span[^>]*class="[^"]*pagenum[^"]*"[^>]*>.*?</span>', r'<div[^>]*class="[^"]*(?:ws-noexport|noprint|navigation|header-template|ws-header|licenseContainer|reflist|references)[^"]*"[^>]*>.*?</div>',
                r'<sup[^>]*class="reference"[^>]*>.*?</sup>', r'<table[^>]*class="[^"]*(?:headertemplate|ws-header)[^"]*".*?</table>'):
        body = re.sub(pat, " ", body, flags=re.S | re.I)
    body = re.sub(r'<br\s*/?>', "\n", body)
    body = re.sub(r'</(p|div|h[1-6]|li|tr|dd|dt|blockquote)>', "\n", body)
    body = re.sub(r'<(?:[^>"\']|"[^"]*"|\'[^\']*\')*>', "", body)  # attribute-aware: data-mw attributes carry '>'
    body = html.unescape(body)
    lines = [re.sub(r'[ \t ]+', ' ', l).strip() for l in body.split("\n")]
    out, blank = [], False
    for l in lines:
        if not l:
            if not blank and out:
                out.append("")
            blank = True
            continue
        out.append(l); blank = False
    return "\n".join(out).strip() + "\n"


def fetch(lang, title, dest, slug):
    dest = pathlib.Path(dest)
    (dest / "original").mkdir(parents=True, exist_ok=True); (dest / "text").mkdir(parents=True, exist_ok=True)
    u = f"https://{lang}.wikisource.org/w/index.php?" + urllib.parse.urlencode({"title": title})
    have = dest / "original" / f"{slug}.html"
    raw = have.read_bytes() if have.exists() and have.stat().st_size else get(u)
    h = raw.decode("utf-8", "replace")
    rev = re.search(r'"wgCurRevisionId":(\d+)', h) or re.search(r'"wgRevisionId":(\d+)', h)
    rev = rev.group(1) if rev else None
    (dest / "original" / f"{slug}.html").write_bytes(raw)
    t = text_of(h)
    (dest / "text" / f"{slug}.txt").write_text(t, encoding="utf-8")
    if not (have.exists() and raw is not None and have.stat().st_mtime < time.time() - 5):
        time.sleep(2)
    return {"source": f"Wikisource ({lang})", "title": title, "url": f"https://{lang}.wikisource.org/wiki/" + urllib.parse.quote(title.replace(' ', '_')),
            "revision": rev, "permalink": f"https://{lang}.wikisource.org/w/index.php?oldid={rev}" if rev else None,
            "file": f"original/{slug}.html", "text": f"text/{slug}.txt", "lines": t.count("\n"),
            "sha256": hashlib.sha256(raw).hexdigest()}


if __name__ == "__main__":
    if sys.argv[1] == "search":
        for t in search(sys.argv[2], " ".join(sys.argv[3:])):
            print(t)
    else:
        print(json.dumps(fetch(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5]), ensure_ascii=False))
