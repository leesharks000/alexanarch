#!/usr/bin/env python3
"""reflow_structure.py — give the deposit's words the blog's structure, and nothing else.

THE FAILURE THIS REPLACES
The previous attempt reconverted the blog post and seated the result. Nine of ten
records were thereby replaced with a LATER OR DIFFERENT VERSION of the work: #1241
arrived with 81% of its vocabulary absent from the deposit, #1319 with 67%, and
three retained fewer of the deposit's own words than they replaced. The whole pass
was reverted. The cause was structural, not a bug: THE BLOG IS A LIVING SURFACE THE
AUTHOR REVISES, so its current text is not the deposited text and never will be.

THE INVARIANT
This script never takes a word from the blog. It takes only markup — where a
heading begins, where a table's cells divide, where a list item starts, where a
code block opens. Every character of prose in the output comes from the deposited
body.

    OUTPUT.words() == DEPOSIT.words()   exactly, in order, with multiplicity.

That is checked after every transformation and the record is refused if it does not
hold. Not approximately, not at 99%: exactly. A structural repair that alters one
word is a version substitution wearing a repair's name, which is what happened last
time and what this equality exists to make impossible.

HOW IT WORKS
The blog post is parsed into an ordered list of blocks. For each block, its word
sequence is located in the deposit's own word stream, moving forward only. When
found, the block's markup is emitted around THE DEPOSIT'S characters for that span.
Blog blocks absent from the deposit are dropped — they are the author's revisions.
Deposit spans no blog block claims are emitted verbatim as plain paragraphs, so
nothing is lost. Then the equality is checked.

    python3 scripts/reflow_structure.py --test 1319
    python3 scripts/reflow_structure.py --apply --limit 10
"""
import argparse, difflib, hashlib, html, json, pathlib, re, sys, time, urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[1]
WORD = re.compile(r"\S+")


def words(t):
    """The comparison unit. Markup characters are not words; prose is."""
    t = re.sub(r"[|`*_#>]", " ", t)
    return [w for w in re.findall(r"[0-9A-Za-z\u00c0-\u024f']+", t)]


def blog_blocks(post_html):
    """Ordered (kind, level, cells|text) from the post body."""
    out = []
    pat = re.compile(r"<(h[1-6]|p|pre|table|ul|ol)\b[^>]*>(.*?)</\1>", re.S | re.I)
    for m in pat.finditer(post_html):
        tag = m.group(1).lower()
        inner = m.group(2)
        if tag == "table":
            rows = []
            for r in re.findall(r"<tr\b[^>]*>(.*?)</tr>", inner, re.S | re.I):
                cells = [html.unescape(re.sub(r"<[^>]+>", " ", c)).strip()
                         for c in re.findall(r"<t[hd]\b[^>]*>(.*?)</t[hd]>", r, re.S | re.I)]
                if cells:
                    rows.append(cells)
            if rows:
                out.append(("table", 0, rows))
        elif tag in ("ul", "ol"):
            items = [html.unescape(re.sub(r"<[^>]+>", " ", li)).strip()
                     for li in re.findall(r"<li\b[^>]*>(.*?)</li>", inner, re.S | re.I)]
            items = [i for i in items if i]
            if items:
                out.append(("list", 1 if tag == "ol" else 0, items))
        elif tag == "pre":
            t = html.unescape(re.sub(r"<[^>]+>", "", inner)).strip("\n")
            if t.strip():
                out.append(("pre", 0, t))
        elif tag.startswith("h"):
            t = html.unescape(re.sub(r"<[^>]+>", " ", inner)).strip()
            if t:
                out.append(("head", int(tag[1]), t))
        else:
            t = html.unescape(re.sub(r"<[^>]+>", " ", inner)).strip()
            if t:
                out.append(("para", 0, t))
    return out


class Stream:
    """The deposit's words, consumed strictly forward. Nothing else may be emitted."""

    def __init__(self, text):
        self.raw = text
        self.spans = [(m.start(), m.end()) for m in WORD.finditer(text)]
        self.w = [re.sub(r"[|`*_#>]", "", text[s:e]) for s, e in self.spans]
        self.wn = [re.sub(r"[^0-9A-Za-z\u00c0-\u024f']", "", x).lower() for x in self.w]
        self.i = 0

    def find(self, target, window=400):
        """Locate target's words at or ahead of the cursor. Returns (start,end) or None."""
        tw = [w.lower() for w in words(target)]
        if not tw:
            return None
        n = len(tw)
        hi = min(len(self.wn), self.i + window + n)
        for st in range(self.i, max(self.i, hi - n) + 1):
            if self.wn[st:st + n] == tw:
                return st, st + n
        return None

    def text_of(self, st, en):
        return self.raw[self.spans[st][0]:self.spans[en - 1][1]]

    def tail(self):
        if self.i >= len(self.spans):
            return ""
        return self.raw[self.spans[self.i][0]:]


def reflow(deposit_text, post_html):
    body = re.sub(r"^---\n.*?\n---\n", "", deposit_text, count=1, flags=re.S)
    front = deposit_text[:len(deposit_text) - len(body)]
    S = Stream(body)
    out, dropped = [], 0

    for kind, lvl, payload in blog_blocks(post_html):
        if kind == "table":
            located = []
            probe = Stream(body)
            probe.i = S.i
            ok = True
            for row in payload:
                rowspans = []
                for c in row:
                    hit = probe.find(c, window=60)
                    if not hit:
                        ok = False
                        break
                    rowspans.append(hit)
                    probe.i = hit[1]
                if not ok:
                    break
                located.append(rowspans)
            if ok and located:
                md = []
                for ri, rowspans in enumerate(located):
                    md.append("| " + " | ".join(
                        S_text(body, S, sp).replace("|", "\\|") for sp in rowspans) + " |")
                    if ri == 0:
                        md.append("|" + "|".join(["---"] * len(rowspans)) + "|")
                out.append("\n".join(md))
                S.i = located[-1][-1][1]
                continue
            dropped += 1
            continue

        if kind == "list":
            spans = []
            probe_i = S.i
            ok = True
            for it in payload:
                save = S.i
                S.i = probe_i
                hit = S.find(it, window=80)
                S.i = save
                if not hit:
                    ok = False
                    break
                spans.append(hit)
                probe_i = hit[1]
            if ok and spans:
                # THE MARKER MUST NOT REPLACE A WORD. An ordered-list marker "1."
                # is markup, but the deposit may itself begin that item with the
                # numeral — in which case emitting both duplicates a word, and
                # emitting only the marker DELETES one. #589 failed the invariant
                # here: six words of a heading were replaced by "1.". Bullets are
                # always safe because "-" is not a word; numerals never are, so
                # ordered lists are emitted as bullets and their numbering is left
                # to the deposit's own text.
                out.append("\n".join("- " + S.text_of(*sp).strip() for sp in spans))
                S.i = spans[-1][1]
                continue
            dropped += 1
            continue

        hit = S.find(payload, window=600 if kind == "para" else 300)
        if not hit:
            dropped += 1
            continue
        if hit[0] > S.i:                       # deposit text no blog block claims
            out.append(S.text_of(S.i, hit[0]).strip())
        seg = S.text_of(*hit).strip()
        if kind == "head":
            out.append("#" * min(6, max(1, lvl)) + " " + seg)
        elif kind == "pre":
            out.append("```\n" + seg + "\n```")
        else:
            out.append(seg)
        S.i = hit[1]

    tail = S.tail().strip()
    if tail:
        out.append(tail)
    return front + re.sub(r"\n{3,}", "\n\n", "\n\n".join(x for x in out if x.strip())) + "\n", dropped


def S_text(body, S, sp):
    return S.text_of(*sp).strip()


def verify(before, after):
    """THE INVARIANT. Exact word equality, in order, with multiplicity."""
    a, b = words(before), words(after)
    if a == b:
        return True, "identical word sequence"
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    diffs = [(tag, a[i1:i2][:6], b[j1:j2][:6])
             for tag, i1, i2, j1, j2 in sm.get_opcodes() if tag != "equal"]
    return False, (f"{len(a)} words in, {len(b)} out; {len(diffs)} divergence(s); "
                   f"first: {diffs[0] if diffs else '-'}")


def fetch(url):
    raw = urllib.request.urlopen(
        urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}),
        timeout=40).read().decode("utf-8", "replace")
    m = re.search(r"<div class=['\"]post-body[^>]*>(.*?)</div>\s*<div class=['\"]post-footer",
                  raw, re.S)
    return m.group(1) if m else None


def struct(md):
    return (len(re.findall(r"^#+ ", md, re.M)), md.count("|---"),
            len(re.findall(r"^\s*(?:[-*]\s|\d+\.\s)", md, re.M)), md.count("```") // 2)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--test", type=int)
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--limit", type=int, default=0)
    a = ap.parse_args()

    reg_p = ROOT / "data/registry.json"
    reg = json.loads(reg_p.read_text())
    D = {d["deposit_number"]: d for d in reg["deposits"]}
    m = json.loads((ROOT / "data/blog-deposit-map.json").read_text())
    pairs = [(e["deposit_number"], e["post_url"], e["title_coverage"])
             for e in m["entries"] if e["confidence_band"] == "strong"]

    if a.test:
        pairs = [p for p in pairs if p[0] == a.test]
        if not pairs:
            print(f"#{a.test} is not a strong pairing in the map", file=sys.stderr)
            return 2
    if a.limit:
        pairs = pairs[:a.limit]

    changed = []
    for n, url, cov in pairs:
        d = D.get(n)
        if not d or not d.get("full_text_path"):
            continue
        fp = ROOT / d["full_text_path"].lstrip("/")
        if not fp.exists():
            continue
        old = fp.read_text(errors="replace")
        try:
            h = fetch(url)
        except Exception as e:
            print(f"  #{n}: fetch failed ({e})")
            continue
        if not h:
            continue
        new, dropped = reflow(old, h)
        ok, why = verify(old, new)
        so, sn = struct(old), struct(new)
        gain = sum(max(0, sn[k] - so[k]) for k in range(4))
        if not ok:
            print(f"  #{n}: REFUSED — {why}")
            continue
        if gain == 0:
            print(f"  #{n}: no structural gain; left alone")
            continue
        print(f"  #{n}: h{so[0]}->{sn[0]} tbl{so[1]}->{sn[1]} li{so[2]}->{sn[2]} "
              f"pre{so[3]}->{sn[3]}  · {dropped} blog block(s) dropped as revisions "
              f"· WORDS IDENTICAL")
        if a.apply:
            store = ROOT / "data/restoration-apparatus"
            store.mkdir(exist_ok=True)
            hexid = d["axn"].split(":")[1].split(".")[0]
            f = store / f"{hexid}.json"
            rec = json.loads(f.read_text()) if f.exists() else {}
            rec.setdefault("lifted", []).append({
                "at": "2026-08-08",
                "reason": ("Pre-reflow body. Structure was transplanted from the authorial "
                           "post; the words are unchanged and verified identical."),
                "text": old})
            f.write_text(json.dumps(rec, ensure_ascii=False, indent=1))
            fp.write_text(new)
            bs = d.setdefault("body_status", {})
            bs["work_sha256"] = hashlib.sha256(new.encode()).hexdigest()
            bs["structure_reflow"] = {
                "at": "2026-08-08", "source": url,
                "invariant": "output word sequence identical to the deposited body, verified",
                "was": f"{so[0]} headings, {so[1]} tables, {so[2]} list items, {so[3]} code blocks",
                "now": f"{sn[0]} headings, {sn[1]} tables, {sn[2]} list items, {sn[3]} code blocks",
                "blog_blocks_dropped_as_revisions": dropped,
                "pairing_status": "provisional \u2014 the blog/deposit pairing has not been read"}
            d.setdefault("record_modifications", []).append({
                "date": "2026-08-08", "field": "canonical_text",
                "note": ("STRUCTURE REFLOWED from the authorial post. NO WORD OF THE DEPOSITED "
                         "TEXT CHANGED: the output's word sequence was verified identical to the "
                         "input's, in order and with multiplicity, before writing. Only markup "
                         f"was added. {dropped} block(s) present on the blog but absent from the "
                         "deposit were dropped as authorial revisions rather than seated.")})
            changed.append(n)
        time.sleep(0.15)

    if a.apply and changed:
        reg_p.write_text(json.dumps(reg, ensure_ascii=False, indent=2))
        json.dump(changed, open("/tmp/reflowed.json", "w"))
    print(f"\n{len(changed)} record(s) reflowed" if a.apply else "\n(no --apply; nothing written)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
