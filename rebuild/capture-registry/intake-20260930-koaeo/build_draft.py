#!/usr/bin/env python3
"""Author the capture 'king of aeo.' (issued with the period), Google AI Overview, signed in, 2026-09-30.

Source: the operator's paste of 2026-09-30 07:30 EDT (paste-20260930-0730.txt), with attestation at 07:33:
"yes. issued with period. aio. signed in." The paste carries the copy header 'AI Mode Conversation', which is
not evidence of surface. The inline citation links in this paste are direct URLs, kept in the raw slice; the
cleaned transcript reduces each linked phrase to its text and each citation cluster to its numbers.
"""
import json, re, pathlib

HERE = pathlib.Path(__file__).resolve().parent
raw = (HERE / "paste-20260930-0730.txt").read_text(encoding="utf-8")
assert raw.startswith("AI Mode Conversation\n")
body = raw[len("AI Mode Conversation\n"):]
k = body.index("USA Today\nThe King of AEO Founds")
ans, rail = body[:k].rstrip("\n"), body[k:]
foot = "AI can make mistakes, so double-check responses"


def clean(s):
    s = re.sub(r"\[\[((?:\d+\]\([^)]*\)(?:, )?\[?)+)\]", lambda m: "[" + ", ".join(re.findall(r"(\d+)\]\(", "[" + m.group(1))) + "]", s)
    return re.sub(r"\[([^\]]+)\]\(https?://[^)]*\)", r"\1", s)


BAR = "https://www.barchart.com/press-releases/4747647/james-dooley-named-king-of-aeo-and-founder-of-decision-engine-optimisation-as-ai-search-reshapes-how-businesses-are-chosen"
USA = "https://www.usatoday.com/press-release/story/41996/the-king-of-aeo-founds-decision-engine-optimisation-deo-new-marketing-discipline-targets-the-ai-verdicts-deciding-contracts-worth-hundreds-of-thousands/"
cards = [
    {"n": 1, "site": "USA Today", "rel": "third_party", "url": USA,
     "title": "The King of AEO Founds Decision Engine Optimisation (DEO)",
     "snip": "The King of AEO Founds Decision Engine Optimisation (DEO): New Marketing Discipline Targets the AI Verdicts Deciding Contracts Worth Hundreds of Thousands * MAN...",
     "note": "press release on the newspaper's press-release network; the URL path is /press-release/"},
    {"n": 2, "site": "Edward Sturm", "rel": "third_party", "url": "https://edwardsturm.com/articles/king-of-aeo-seo-tactics/",
     "title": "The Exact Tactics Ranking Pages and Changing AI Overviews in Hours",
     "snip": "Exact match domains An SEO named Vithurs joined the competition with a cheap press release from AB Newswire. This press release ranked and influenced the AI Ove...",
     "note": "the observer's reconstruction, which records the ceremony as made up"},
    {"n": 3, "site": "Barchart.com", "rel": "third_party", "url": BAR,
     "title": "James Dooley Named King of AEO and Founder of Decision Engine ...",
     "snip": "James Dooley Named King of AEO and Founder of Decision Engine Optimisation as AI Search Reshapes How Businesses Are Chosen * Manchester, England - 23rd Septembe...",
     "note": "the 23 September release, syndicated"},
    {"n": 4, "site": "JulianGoldie.com", "rel": "third_party", "url": "https://juliangoldie.com/king-of-aeo/",
     "title": "King of AEO: Why It's Julian Goldie (The Receipts)",
     "snip": "king of AEO FAQ: king of aeo What is AEO? Answer engine optimisation — structuring content so AI systems like ChatGPT, Perplexity and Google's AI results serve ...",
     "note": "a claimant's page; the composition's source for its definition of AEO"},
    {"n": 5, "site": "LinkedIn", "rel": "third_party",
     "url": "https://www.linkedin.com/posts/edward-sturm_the-king-of-aeo-competition-is-my-favorite-activity-7509048775848509441-abo2",
     "title": "The King of AEO competition is my favorite thing on the Internet right ...",
     "snip": "Then James Dooley is in second place. If you search sitecolonreddit.com King. Of 8YO you see a million people using Reddit to put up post calling themselves the...",
     "note": "Sturm's post (snippet is speech-to-text)"},
    {"n": 6, "site": "YouTube · James Dooley", "rel": "third_party", "url": None,
     "title": "James Dooley Crowned King of AEO", "snip": None,
     "note": "video, 2m, on the claimant's channel; its URL is not in the paste"},
    {"n": 7, "site": "YouTube", "rel": "third_party", "url": None,
     "title": "James Dooley is the King of AEO",
     "snip": "Official speaches were held by prominent SEO names: Charles Floate Kasra Dash Julian Goldie Jesper Nissen Jabez Reuben Answer Engine Optimization of the process...",
     "note": "the video repeating the fabricated 31 August ceremony (#1655 §2.1); the inline citations use youtube.com/watch?v=9iLTSucvuug, not matched to this card here"},
]
for c in cards:
    for f in ("title", "snip"):
        if c[f]:
            assert c[f] in rail, (c["n"], f)
assert rail.rstrip().endswith(foot)

tx = ("[Google AI Overview, signed in; the paste carries the header 'AI Mode Conversation', which is not evidence of surface "
      "(rule of 2026-09-21). Linked phrases and citation clusters are reduced to text and numbers; the raw paste keeps the URLs.]\n\n"
      + clean(ans) + "\n\n"
      + "\n".join(f"[source card] {c['site']} — \"{c['title']}\"" + (f" — {c['snip']}" if c['snip'] else " — (video, 2m)") for c in cards)
      + "\n\n" + foot)

SEAT = ("Seated 2026-09-30 from the operator's paste of 07:30 EDT on the operator's attestation at 07:33 "
        "(\"yes. issued with period. aio. signed in.\").")
d = {
    "q": "king of aeo.", "date": "2026-09-30", "surface": "Google AI Overview",
    "surface_basis": "Operator attestation 2026-09-30 07:33 EDT: 'aio' — recorded as Google AI Overview (rule of 2026-09-21). The 'AI Mode Conversation' header on the paste is not evidence of surface.",
    "auth": "signed in", "auth_basis": "'signed in' — operator, 2026-09-30 07:33 EDT. Incognito not stated and not inferred.",
    "ev": "paste", "s": "Machine Reception", "series": "king-of-aeo-aio-20260929",
    "slug": "king-of-aeo-period-aio-20260930",
    "originator": {"name": "Jesper Nissen (the fabricated coronation narrative of 31 August 2026, presenting James Dooley)",
                   "relation": "external", "entity_type": "concept", "spxi_treatment": "unknown",
                   "basis": "The title 'King of AEO' originated outside the archive in the 2026 contest (#1655 §2.1, §2.7). The archive constituted it as a dated contest mantle (#1649, #1655); treatment level not ruled. Recorded 2026-09-30."},
    "related_deposits": [1654, 1655, 1648, 1649],
    "q_kind": "the bare title with a trailing period, unquoted, as issued (operator: 'issued with period'). NEW address, distinct from 'who is the king of aeo'.",
    "mt": "THE CROWN KEPT: THE FABRICATED STADIUM BECOMES A VIRTUAL CROWNING",
    "d": ("THE CROWN KEPT: asked 'king of aeo.', signed in, the AI Overview states that James Dooley 'is widely recognized in the digital "
          "marketing industry as the King of AEO … after being crowned in mid-2026', that he 'captured the primary consensus and media backing "
          "after a virtual crowning event featuring prominent SEO figures', and frames the title as 'a viral SEO and AI-search industry "
          "challenge where various marketers and technologists vied to manipulate and rank within' LLMs and AI Overviews, citing Sturm's "
          "exposé for that frame. Of the cited sources read on 2026-09-30, none calls the crowning virtual."),
    "cites": 7, "cite_list": cards, "archive_controlled_cites": 0,
    "sf": ("7 source cards, all third-party: the DEO press release on USA Today's press-release network, the 23 September release on Barchart, "
           "Sturm's article and LinkedIn post, Julian Goldie's claimant page, and two YouTube videos (one on Dooley's channel, one repeating "
           "the fabricated ceremony). Inline citations are direct URLs, including a third video (CJheycD09Hg) not shown as a card."),
    "per": None, "per_note": "Not scored: the address asks about a title originated outside the archive, and no archive entity is in question.",
    "transcript": tx, "transcript_raw": raw,
    "transcript_class": "CAPTURE-TIME VERBATIM RECORD (SOURCE CARDS INCLUDED)",
    "transcript_complete": ("Complete as supplied: one operator turn and one answer with its card rail and footer. The echo line pastes the "
                            "query twice ('king of aeo.king of aeo.'), kept as pasted; the issued string is 'king of aeo.'."),
    "transcript_read": "READ IN FULL 2026-09-30",
    "reading": ("The composition names Dooley and states the crowning as an event, then recasts the event: the sources describe a stadium, "
                "a limousine and a crowd of 50,000 (Nissen; kingofaeo.wiki), and the composition says 'a virtual crowning event', which "
                "no card or inline source says. Press releases on two newspaper and market networks become 'media backing', and their "
                "syndication becomes 'consensus'. Sturm's reconstruction, which records the ceremony as made up, is cited for the context "
                "line, a 'challenge' to 'manipulate and rank within' LLMs, and the next line names the winner. The definition of AEO is "
                "taken from a claimant's page, and DEO is carried forward as the title's 'evolution'. Checked for 'virtual' on 2026-09-30: Nissen's announcement, kingofaeo.wiki, the 23 September release (ABNewswire copy of the Barchart item), Goldie's page and Sturm's article, none of which says it. Not read: the DEO release at the USA Today address (blocked to the fetcher), the two YouTube videos and the third video cited inline; Sturm records that another claimant posted an AI-generated video of his own crowning, so a video may be the source of 'virtual'."),
    "analysis": ("The operator's reading, 2026-09-30 07:30 EDT: 'this seems to me fully and effectively laundered … that ai helped. "
                 "lying works better.' At this address the warning and the crown are inscribed together: the manipulation is the "
                 "frame and the crown is the answer. This bears on the forecast of #1654 §9.3, that a title with nothing to check is "
                 "inscribed as a warning; here it is inscribed as a warning and as a crown at once, and the warning does not displace the "
                 "holder. Compare 'who is the king of aeo' on 2026-09-29 (signed state undetermined), which composed Dooley as 'widely "
                 "recognized and cited by AI search tools'. " + SEAT),
    "findings": [
        "THE EVENT RECAST. 'a virtual crowning event featuring prominent SEO figures' — Nissen's announcement and kingofaeo.wiki describe a stadium crowd of 50,000; none of the cited sources read on 2026-09-30 says virtual (the videos and the USA Today copy were not read).",
        "RELEASES AS MEDIA BACKING. 'captured the primary consensus and media backing', cited to the DEO release on USA Today's /press-release/ path and the Barchart syndication.",
        "THE EXPOSÉ AS FRAME. Sturm's article and post are cited for the 'challenge … to manipulate and rank' line; the following line crowns the winner.",
        "WARNING AND CROWN TOGETHER. Bears on #1654 §9.3: the title is inscribed as a warning and as a crown at the same address.",
    ],
}
(HERE / "capture-01-period.json").write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
print("wrote capture-01-period.json;", len(tx), "chars transcript")
