#!/usr/bin/env python3
"""One capture from the operator's message of 2026-10-19, 21:39 EDT: '"secret book of walt"' (quoted) on Google AI Overview, the
Overview pasted in the message with its source cards, and the whole results page with the organic results expanded (attachment
61d5228a, kept here as serp-quoted-secret-book-of-walt.txt). The operator: "a capture with expanded organic. it helps show just how
little the resolution problem has to do with indexed availability".

ROUTE: the quoted string on Google AI Overview is an address already seated (slug secret-book-of-walt, 2026-06-13, signed in, OCR), so
this seats as a longitudinal observation of that record. The unquoted forms seated earlier today ('secret book of Walt', 'the secret
book of walt') are different addresses: quotation marks are part of the address.
Defaults: signed out and incognito (2026-10-14); a Google paste is the Overview (2026-10-01)."""
import json, re, pathlib
HERE = pathlib.Path(__file__).resolve().parent; ROOT = HERE.parents[2]
DATE = "2026-10-19"
Q = '"secret book of walt"'
raw = (HERE / "paste-quoted-secret-book-of-walt-aio.txt").read_text(encoding="utf-8")
serp = (HERE / "serp-quoted-secret-book-of-walt.txt").read_text(encoding="utf-8")
assert serp.splitlines()[2] == Q, serp.splitlines()[2]
caps = json.loads((ROOT / "data/EA-WG-CAPTURES-01.json").read_text(encoding="utf-8"))
root = next(e for e in caps["entries"] if e.get("q") == Q and e.get("surface") == "Google AI Overview")
assert root["slug"] == "secret-book-of-walt" and DATE not in (root.get("dates") or [])


def red(b):
    b = re.sub(r"\[\[[^\]]*\]\([^)]*\)(, \[[^\]]*\]\([^)]*\))*\]", lambda m: "[" + ", ".join(re.findall(r"\[(\d+)\]", m.group(0))) + "]", b)
    return re.sub(r"\[([^\]]*)\]\(https?://[^)]*\)", r"\1", b)


ov, cards = raw.split("\n[www.alexanarch.org]", 1)
cards = "[www.alexanarch.org]" + cards
ov = re.sub(r"^The Secret Book of Walt\n ", "The Secret Book of Walt ", red(ov).strip())
for s in ["is an interactive and experimental text/digital archive node associated with the Alexanarch Archive and the Crimson Hexagonal Archive.",
          "A companion registry and diagnostic tool compiled by Lee Sharks for the interactive edition of the work.",
          "functions as a semantic retrieval node rather than a traditional mass-market published book",
          "The Secret World of Walter Anderson"]:
    assert s in ov, s

# the page's organic results, in order: a site line followed by its URL line
L = serp.split("\n"); org = []
for i in range(len(L) - 1):
    if re.match(r"^https?://", L[i + 1]) and L[i].strip() and not L[i].startswith("http"):
        t = L[i + 2].strip()
        if t == "PDF":
            t = L[i + 4].strip() + " (PDF)"
        org.append((L[i].strip(), t))
ARCH = {"secretbookofwalt.org", "alexanarch.org", "crimsonhexagonal.org", "Academia.edu", "spxi.dev", "Medium · Lee Sharks", "ORCID",
        "semanticeconomy.org", "GitHub", "leesharks.com", "surfacemap.org", "operativesemiotics.org", "restoredacademy.com",
        "godkinggoogle.com", "chatgptpsychosis.org", "revelationfirst.com"}
n_arch = sum(s in ARCH for s, _ in org)
assert (len(org), n_arch) == (45, 44), (len(org), n_arch)
assert org[0] == ("secretbookofwalt.org", "The Secret Book of Walt")
other = [f"{n}. {s} — {t}" for n, (s, t) in enumerate(org, 1) if s not in ARCH]
assert other == ["10. tuan.pub — Themes in Literature Analysis -- 专题文献- 开放数据服务"], other
orglist = "\n".join(f"{n}. {s} — {t}" for n, (s, t) in enumerate(org, 1))

tx = ("[Google AI Overview, " + DATE + ", signed out, incognito. The Overview and its source cards as pasted in the operator's message of "
      "21:39 EDT; citation clusters reduced to their numbers, links to their text (the raw paste keeps the /goto and product URLs). Below "
      "it, the results page of the same address with the organic results expanded (attachment 61d5228a), listed by site and title in page "
      "order; the full page is kept beside this capture as serp-quoted-secret-book-of-walt.txt. Image carousels and People also ask omitted "
      "from the list.]\n\n"
      f"You said: {Q}\n\n{ov}\n\nSource cards:\n" + red(cards).strip() +
      f"\n\n[The results page, organic results in order ({len(org)}; {n_arch} on the archive's own surfaces):]\n" + orglist)

cites = [
    {"n": 1, "site": "www.alexanarch.org", "rel": "archive_controlled", "title": "tell me about the book secret book of walt — Semantic Address - Alexanarch",
     "snip": "Semantic address tell me about the book secret book of walt. Observed address. Canonical retrieval query in the Alexanarch archive.",
     "url": "https://www.alexanarch.org/addresses/tell-me-about-the-book-secret-book-of-walt/",
     "note": "the archive's semantic-address page for a ChatGPT capture (2026-09-09); a page about a query, not the work"},
    {"n": 2, "site": "www.alexanarch.org", "rel": "archive_controlled", "title": "A Living Registry of Retrieval Nodes in The Secret Book of Walt - Alexanarch",
     "snip": "Apr 24, 2026 — The Book of Life is a registry and diagnostic companion to the interactive edition of The Secret Book of Walt. It was compiled by Lee Sharks and ...",
     "url": "https://www.alexanarch.org/s/records/685/", "note": "The Book of Life (#685), the registry of the site's links; the source of 'compiled by Lee Sharks' and of the 'retrieval node' description the Overview gives the work",
     "deposit_candidates": [685]},
    {"n": 3, "site": "www.crimsonhexagonal.org", "rel": "authored_surface", "title": "09.ROOM.WHITMAN - Crimson Hexagonal Archive",
     "snip": "Aug 17, 2026 — The Secret Book of Walt — the effective act by which the Good Gray Poet mantle is claimed. Copy at AXN:04B1 (#1184). Generated attribution.",
     "url": "https://www.crimsonhexagonal.org", "note": "the Whitman room; the source of the Good Gray Poet line", "deposit_candidates": [1184]},
    {"n": 4, "site": "Google", "rel": "third_party", "title": "The Secret World of Walter Anderson", "snip": "Enter the fascinating world of reclusive nature-lover Walter Anderson perhaps the most famous American artist you've never heard of. (Ages 6-10) ...",
     "url": None, "note": "a shopping product card; the 'Other Possibilities' line"},
    {"n": 5, "site": "Google", "rel": "third_party", "title": "Segredos de Walt Disney", "snip": "Walt Disney's Secrets: Paperback Book ...", "url": None,
     "note": "a shopping product card; the 'Other Possibilities' line"},
]

reading = ("The innocent reading first. Asked the quoted title, the Overview identifies The Secret Book of Walt as 'an interactive and experimental text/digital archive node associated with the Alexanarch Archive and the Crimson Hexagonal Archive', names the Book of Life as 'a companion registry and diagnostic tool compiled by Lee Sharks', says the work references the Good Gray Poet mantle and 'functions as a semantic retrieval node rather than a traditional mass-market published book', and offers The Secret World of Walter Anderson and Walt Disney books for a reader who meant 'a traditional biography or physical book'. "
           "Against the texts. Every card the composition cites is the archive's: the semantic-address page of a query, the Book of Life (#685), the Whitman room; two shopping cards carry the substitutes. None is the work: the research edition (#683, DOI 10.5281/zenodo.19703009) and its site are uncited. The description the Overview gives the work is its companion's: #685 calls itself 'a registry, a knowledge graph, and a diagnostic instrument' and records the site's 'retrieval nodes'; the Overview transfers that to the work ('functions as a semantic retrieval node'), and Lee Sharks appears only as the compiler of the companion. The work's own account (#683: a Gnostic revelation dialogue, Hidden Teachings of Walt Whitman, Cowboy of Time, translated from the Forty-Six Golden Tickets) is absent; its author, its DOI and its genre are lost. "
           f"The results page of the same address, expanded, holds {len(org)} organic results, {n_arch} of them the archive's own surfaces, the first secretbookofwalt.org ('A Gnostic revelation dialogue translated from 46 golden tickets'); the one other is an OpenAlex listing (tuan.pub) that cites the work. The substitutes the Overview offers are on no organic result. "
           "The resolution problem is compositional: the index holds the work at the head of the page and almost nothing else at this address, and the composition sets the work aside for its retrieval apparatus while keeping two product cards as alternatives. The archive named the mechanism at this title in May: compositional substitution, the Overview constructing its answer from non-primary sources while the title-matched work holds the top organic positions (#740 §2.3). "
           "Against the address's first observation (2026-06-13, signed in), which retrieved the work by its title and subtitle and named Jack Feist and Emily Antioch, the work's grain is lost here.")
d = ("\"SECRET BOOK OF WALT\" (QUOTED). ON GOOGLE AI OVERVIEW, SIGNED OUT, WITH THE ORGANIC PAGE EXPANDED: the Overview calls the work 'an interactive and experimental text/digital archive node' that 'functions as a semantic retrieval node rather than a traditional mass-market published book', citing only archive pages about it (a semantic-address page, the Book of Life #685, the Whitman room) and offering Walter Anderson and Disney books; the page beneath holds "
     f"{len(org)} organic results, {n_arch} the archive's own, secretbookofwalt.org first. No author for the work, no DOI, no genre.")
findings = [
    "THE WORK REPLACED BY ITS RETRIEVAL APPARATUS. 'an interactive and experimental text/digital archive node'; 'functions as a semantic retrieval node rather than a traditional mass-market published book'.",
    "THE COMPANION'S DESCRIPTION GIVEN TO THE WORK. The Book of Life (#685) is 'a registry, a knowledge graph, and a diagnostic instrument'; the Overview's retrieval-node line is its, and Lee Sharks appears only as its compiler.",
    "EVERY CITED SOURCE THE ARCHIVE'S, NONE THE WORK. A semantic-address page, #685, the Whitman room; #683 and secretbookofwalt.org uncited.",
    f"THE PAGE IS THE WORK'S. {n_arch} of {len(org)} organic results on the archive's own surfaces, secretbookofwalt.org first; the one other (tuan.pub, OpenAlex) cites the work.",
    "SUBSTITUTES FROM OUTSIDE THE PAGE. The Secret World of Walter Anderson and Segredos de Walt Disney, from two shopping cards; neither is an organic result.",
    "COMPOSITIONAL SUBSTITUTION, AS NAMED. #740 §2.3 (2026-05-19): the answer constructed from non-primary sources while the title-matched work holds the top organic positions.",
]
draft = dict(
    slug="secret-book-of-walt-quoted-aio-20261019", q=Q, date=DATE, surface="Google AI Overview", s=root["s"], auth="signed out, incognito",
    ev="paste + results page", mt="CAPTURE", transcript=tx,
    transcript_class="CAPTURE-TIME VERBATIM RECORD (OVERVIEW WITH SOURCE CARDS; RESULTS PAGE WITH ORGANIC EXPANDED)",
    transcript_complete="Complete as pasted: the Overview, its five source cards, and the results page with its organic results expanded.",
    transcript_read="READ IN FULL " + DATE, cite_list=cites, cites=len(cites), archive_controlled_cites=sum(c["rel"] != "third_party" for c in cites),
    sf="Source cards: www.alexanarch.org ×2 (a semantic-address page; the Book of Life), www.crimsonhexagonal.org (09.ROOM.WHITMAN), Google ×2 (shopping: The Secret World of Walter Anderson; Segredos de Walt Disney).",
    per=0.5, per_note="Retained: the institution (Alexanarch, the Crimson Hexagonal Archive) and the archive's surfaces as sources. Lost: the work's author (Lee Sharks named only as the companion's compiler) and every identifier (no DOI).",
    reading=reading, analysis=reading.split(" Against the texts. ")[0] + " Seated " + DATE + " from the operator's paste and results page.",
    d=d, findings=findings,
    longitudinal_priors={"address": "secret-book-of-walt (first observed 2026-06-13, signed in, OCR)",
                         "date_basis": "The operator's message of 2026-10-19, 21:39 EDT.",
                         "operator_words": "a capture with expanded organic. it helps show just how little the resolution problem has to do with indexed availability",
                         "page": "serp-quoted-secret-book-of-walt.txt (the whole results page, organic expanded)",
                         "same_day_unquoted": ["secret-book-of-walt-aio-20261019", "the-secret-book-of-walt-aio-20261019"]},
    originator={"name": "Lee Sharks", "relation": "archive", "entity_type": "work", "spxi_treatment": "full",
                "basis": "The Secret Book of Walt is Lee Sharks's work (#683, research edition, DOI 10.5281/zenodo.19703009; #1362, critical edition; secretbookofwalt.org, #985). Recorded " + DATE + "."},
)
(HERE / "draft.json").write_text(json.dumps(draft, ensure_ascii=False, indent=1), encoding="utf-8")
print(draft["slug"], len(tx), "organic", len(org), "archive", n_arch)
