#!/usr/bin/env python3
"""Author the two King of AEO AI Overview captures of 2026-09-29 from the operator's paste.

The paste (paste-20260929-0127.txt) is the operator's message of 2026-09-29 01:27 EDT, recovered
verbatim from the session record on 2026-09-29 after the captures were found cited in #1655 §3
and #1654 §2.2.1 without having been seated. It holds two AI Overview sessions, each opening with
the copy-paste header 'AI Mode Conversation' (not evidence of surface). This script splits them,
keeps each raw slice as transcript_raw, and writes a cleaned transcript: markdown redirect links
reduced to their text, inline citation markers kept as numbers, and the card rail listed as
source cards. The google.com/goto tokens are session-bound redirects; they are kept in the raw
slice and cannot be resolved to targets from here.
"""
import json, re, pathlib

HERE = pathlib.Path(__file__).resolve().parent
raw = (HERE / "paste-20260929-0127.txt").read_text(encoding="utf-8")
HDR = "AI Mode Conversation\n"
i2 = raw.index("$ AI Mode Conversation\n") + 2
raw_v = raw[:i2].rstrip(" ")  # Vithurs session; its last card snippet ends '$'
raw_d = raw[i2:]
assert raw_v.startswith(HDR) and raw_d.startswith(HDR)


def clean_answer(s):
    s = re.sub(r"\[\[((?:\d+\]\([^)]*\)(?:, )?\[?)+)\]", lambda m: "[" + ", ".join(re.findall(r"(\d+)\]\(", "[" + m.group(1))) + "]", s)
    s = re.sub(r"\[([^\]]+)\]\(https://www\.google\.com/goto\?url=[^)]*\)", r"\1", s)
    return s


def split(raw_s, card_start):
    body = raw_s[len(HDR):]
    k = body.index(card_start)
    return body[:k].rstrip("\n"), body[k:]


# ---------- Vithurs ----------
ans_v, rail_v = split(raw_v, "USA Today\nVithurs Named")
cards_v = [
    {"n": 1, "site": "USA Today", "rel": "third_party",
     "title": "Vithurs Named King of AEO Following 2026 Industry Vote",
     "snip": "Vithurs Named King of AEO Following 2026 Industry Vote New York, United States – September 07, 2026 – King of AEO today announced that British entrepreneur and ...",
     "url": None,
     "note": "the claimant's 7 September press release, syndicated onto a USA Today network page; it carries the claimant's own assertion"},
    {"n": 2, "site": "Instagram", "rel": "third_party",
     "title": "The world is in a turbulent time, so be careful with information you get from AI ...",
     "snip": "* timothybramlett. Where do you get a $6 press release? Asking for a friend… and Future King of AI Receptionists. * jimmyshimmy. The death of the internet. AI n...",
     "url": None, "note": "Edward Sturm's warning video; the snippet is its comment thread"},
    {"n": 3, "site": "Facebook", "rel": "third_party",
     "title": "The world is in a turbulent time, so be careful with information you get from AI ...",
     "snip": "The creator explains the concept of Answer Engine Optimization (AEO) and demonstrates how easily AI search results can be manipulated. He details a coordinated ...",
     "url": None, "note": "the same Sturm video, reposted"},
    {"n": 4, "site": "Instagram · Edward Sturm", "rel": "third_party",
     "title": None,
     "snip": "So much to learn from this one $",
     "url": None,
     "note": "video card, 2:24; its redirect token is the third citation on the answer's 'The Experiment' line"},
]
tx_v = ("[Google AI Overview; the paste carries the header 'AI Mode Conversation', which is not evidence of surface "
        "(rule of 2026-09-21). Inline citation links are google.com/goto redirects, reduced here to their numbers; "
        "the raw paste keeps them.]\n\n" + clean_answer(ans_v) + "\n\n" +
        "\n".join(f"[source card] {c['site']} — " + (f"\"{c['title']}\" — " if c['title'] else "(video, 2:24) — ") + c['snip'] for c in cards_v))

# ---------- Dooley (head query) ----------
ans_d, rail_d = split(raw_d, "USA Today\nThe King of AEO Founds")
cards_d = [
    {"n": 1, "site": "USA Today", "rel": "third_party",
     "title": "The King of AEO Founds Decision Engine Optimisation (DEO): New Marketing Discipline Targets the AI Verdicts Deciding Contracts Worth Hundreds of Thousands - USA Today",
     "snip": "The King of AEO Founds Decision Engine Optimisation (DEO): New Marketing Discipline Targets the AI Verdicts Deciding Contracts Worth Hundreds of Thousands * MAN...",
     "url": None, "note": "syndicated press release on a USA Today network page; the answer cites it as 'reported by USA Today'"},
    {"n": 2, "site": "YouTube · Edward Sturm", "rel": "third_party",
     "title": "Be careful of the information you get from AI", "snip": None,
     "url": None, "note": "video, 2:54; the observer's warning"},
    {"n": 3, "site": "LinkedIn", "rel": "third_party",
     "title": "The King of AEO competition is my favorite thing on the Internet right ...",
     "snip": "Then James Dooley is in second place. If you search sitecolonreddit.com King. Of 8YO you see a million people using Reddit to put up post calling themselves the...",
     "url": None, "note": "commentary on the contest (snippet is speech-to-text: 'sitecolonreddit.com King. Of 8YO')"},
    {"n": 4, "site": "Primary Position SEO", "rel": "third_party",
     "title": "Who is the King of AEO?",
     "snip": "Who is the King of AEO? * His core argument is the uncomfortable one While the industry raced to rebrand SEO as GEO, AEO, LLMO, and whatever comes next, Quaid s...",
     "url": None, "note": "David G. Quaid's claimant page"},
    {"n": 5, "site": "YouTube", "rel": "third_party",
     "title": "James Dooley is the King of AEO",
     "snip": "Official speaches were held by prominent SEO names: Charles Floate Kasra Dash Julian Goldie Jesper Nissen Jabez Reuben Answer Engine Optimization of the process...",
     "url": None, "note": "video repeating the fabricated 31 August coronation as an event (#1655 §2.1)"},
    {"n": 6, "site": "JulianGoldie.com", "rel": "third_party",
     "title": "King of AEO: Why It's Julian Goldie (The Receipts)",
     "snip": "king of AEO FAQ: king of aeo What is AEO? Answer engine optimisation — structuring content so AI systems like ChatGPT, Perplexity and Google's AI results serve ...",
     "url": None, "note": "Julian Goldie's claimant page"},
    {"n": 7, "site": "USA Today", "rel": "third_party",
     "title": "Vithurs Named King of AEO Following 2026 Industry Vote",
     "snip": "Vithurs Named King of AEO Following 2026 Industry Vote New York, United States – September 07, 2026 – King of AEO today announced that British entrepreneur and ...",
     "url": None, "note": "the Vithurs release, syndicated; the same card as the first card at the Vithurs address"},
    {"n": 8, "site": "Barchart.com", "rel": "third_party",
     "title": "James Dooley Named King of AEO and Founder of Decision Engine ...",
     "snip": "James Dooley, serial entrepreneur from Manchester, England, is recognised as the King of AEO and the King of AI SEO, and is the founder of Decision Engine Optim...",
     "url": None, "note": "syndicated press release"},
]
tx_d = ("[Google AI Overview; the paste carries the header 'AI Mode Conversation', which is not evidence of surface "
        "(rule of 2026-09-21). Inline citation links are google.com/goto redirects, reduced here to their numbers; "
        "the raw paste keeps them.]\n\n" + clean_answer(ans_d) + "\n\n" +
        "\n".join(f"[source card] {c['site']} — \"{c['title']}\"" + (f" — {c['snip']}" if c['snip'] else " — (video, 2:54)") for c in cards_d))

# the card rails, as pasted, must be fully accounted for by the cards above
for rail, cards in ((rail_v, cards_v), (rail_d, cards_d)):
    for c in cards:
        for f in ("title", "snip"):
            if c[f]:
                assert c[f] in rail, (c["n"], f)

SURFACE_BASIS = ("Operator attestation 2026-09-29 01:27 EDT: 'base it on the difference in the aio write ups' — recorded as "
                 "Google AI Overview (rule of 2026-09-21). The 'AI Mode Conversation' header on the paste is not evidence of surface.")
AUTH_BASIS = ("Not attested. The operator's message of 2026-09-29 01:27 EDT gives the surface and the two compositions; "
              "it does not state sign-in or incognito, and neither is inferred.")
ORIG = {"name": "Jesper Nissen (the fabricated coronation narrative of 31 August 2026, presenting James Dooley)",
        "relation": "external", "entity_type": "concept", "spxi_treatment": "unknown",
        "basis": "The title 'King of AEO' originated outside the archive in the 2026 contest (#1655 §2.1, §2.7). The archive "
                 "constituted it as a dated contest mantle (#1649, #1655) and made a determination under stated standards; "
                 "the treatment level is not ruled. Recorded 2026-09-29."}
CLASS = "CAPTURE-TIME VERBATIM RECORD (SOURCE CARDS INCLUDED) — recovered from the session in which MANUS supplied it"
SEATING = ("Seated 2026-09-29, eighteen hours after the paste. #1654 §2.2.1 and #1655 §3 quoted both compositions as observed "
           "evidence and #1655 recorded them as 'addresses to be seated'; they were not seated at deposit, and the working copy "
           "was lost when the session compacted. The operator's message was recovered verbatim from the session record, and "
           "both addresses are seated from it.")
RELATED = [1654, 1655, 1648, 1649]
SERIES = "king-of-aeo-aio-20260929"

v = {
    "q": "who is the king of aeo? vithurs", "date": "2026-09-29", "surface": "Google AI Overview",
    "surface_basis": SURFACE_BASIS, "auth": "undetermined", "auth_basis": AUTH_BASIS, "ev": "paste",
    "s": "Machine Reception", "series": SERIES, "originator": ORIG, "related_deposits": RELATED,
    "slug": "who-is-the-king-of-aeo-vithurs-aio-20260929",
    "q_kind": "question plus a claimant's name, unquoted; the name seeds the query. NEW address. Issued the same night as 'who is the king of aeo'.",
    "mt": "THE CLAIMANT NAMED, THE MANUFACTURE CARRIED",
    "d": ("THE CLAIMANT NAMED, THE MANUFACTURE CARRIED: asked 'who is the king of aeo? vithurs', the AI Overview names Vithurs "
          "King of AEO 'following a social media industry vote in September 2026' — the release's 'private vote' dropped — and in "
          "the same answer explains the title as an experiment testing 'how easily AI search engines can be tricked into crowning "
          "a specific person for a made-up or heavily contested title', citing Edward Sturm's video among its sources."),
    "cites": 4, "cite_list": cards_v, "archive_controlled_cites": 0,
    "sf": "4 source cards, all third-party: the Vithurs press release syndicated on a USA Today network page, and Edward Sturm's warning video three times (Instagram, Facebook repost, Instagram video card).",
    "per": None, "per_note": "Not scored: the address asks about a title originated outside the archive, and no archive entity is in question.",
    "transcript": tx_v, "transcript_raw": raw_v, "transcript_class": CLASS,
    "transcript_complete": ("Complete as supplied: one operator turn and one answer with its card rail. The echo line pastes the query twice "
                            "('who is the king of aeo? vithurswho is the king of aeo? vithurs'), kept as pasted; the issued string is "
                            "'who is the king of aeo? vithurs'. The paste's last card ends '$', the character before the next session's header."),
    "transcript_read": "READ IN FULL 2026-09-29",
    "reading": ("The name in the query brings the claimant's release to the top: the answer's first sentence is the 7 September "
                "release restated, with 'a private vote conducted through social media' become 'a social media industry vote'. The "
                "second half of the answer composes the contest from outside. Its 'Experiment' line, cited in part to Sturm's video, "
                "describes the whole race as a test of how easily engines can be 'tricked into crowning' someone for 'a made-up or heavily "
                "contested title'. The composition names the holder and, in the same answer, says how the naming was made."),
    "analysis": ("The operator's reading, 2026-09-29 01:27 EDT: 'vithurs write up inscribes the experiment.' The answer carries the "
                 "manufacture of the title alongside the claimant's name; the privacy of the vote is the one feature of the release it "
                 "loses. The address is seeded with the claimant's name, which #1655 §4.3 records against the determination. "
                 "#1654 §9.2 and #1655 §3.2 quote this composition. " + SEATING),
    "findings": [
        "PRIVACY DROPPED. The release's 'private vote conducted through social media' is composed as 'a social media industry vote in September 2026'.",
        "MANUFACTURE CARRIED. 'to test how easily AI search engines can be tricked into crowning a specific person for a made-up or heavily contested title' — in the answer that names the claimant.",
        "THE OBSERVER AS SOURCE. The 'Experiment' line's third citation is the redirect behind Sturm's Instagram video card; three of four cards are his video.",
        "SEATED LATE. " + SEATING,
    ],
}

d = {
    "q": "who is the king of aeo", "date": "2026-09-29", "surface": "Google AI Overview",
    "surface_basis": SURFACE_BASIS, "auth": "undetermined", "auth_basis": AUTH_BASIS, "ev": "paste",
    "s": "Machine Reception", "series": SERIES, "originator": ORIG, "related_deposits": RELATED,
    "slug": "who-is-the-king-of-aeo-aio-20260929",
    "q_kind": "the head question, unquoted. NEW address; the baseline #1654 §9.3 called for. Issued the same night as 'who is the king of aeo? vithurs'.",
    "mt": "THE FABRICATION COMPOSED AS RECOGNITION",
    "d": ("THE FABRICATION COMPOSED AS RECOGNITION: asked 'who is the king of aeo', the AI Overview composes James Dooley as 'widely "
          "recognized and cited by AI search tools as the King of AEO', calls the title 'a viral digital marketing experiment and meme', "
          "credits Dooley's Decision Engine Optimization 'as reported by USA Today' — a syndicated press release — and carries among "
          "eight cards a video repeating the fabricated 31 August ceremony ('Official speaches were held…') beside Sturm's 'Be careful "
          "of the information you get from AI'."),
    "cites": 8, "cite_list": cards_d, "archive_controlled_cites": 0,
    "sf": ("8 source cards, all third-party: two syndicated press releases for Dooley (USA Today network, Barchart), the Vithurs release "
           "(USA Today network), the video repeating the fabricated coronation, Sturm's warning video, a LinkedIn commentary, and the "
           "Quaid and Goldie claimant pages."),
    "per": None, "per_note": "Not scored: the address asks about a title originated outside the archive, and no archive entity is in question.",
    "transcript": tx_d, "transcript_raw": raw_d, "transcript_class": CLASS,
    "transcript_complete": ("Complete as supplied: one operator turn and one answer with its card rail. The echo line pastes the query twice "
                            "('who is the king of aeowho is the king of aeo'), kept as pasted; the issued string is 'who is the king of aeo'."),
    "transcript_read": "READ IN FULL 2026-09-29",
    "reading": ("At the head query the composition gives Dooley the title as recognition by the machine layer itself ('widely recognized "
                "and cited by AI search tools'), lists Vithurs, Goldie and Quaid as 'other contenders', and describes the title as an "
                "experiment and meme in which marketers 'used press releases, social media, and targeted content to influence what large "
                "language models return'. Its one attributed fact about Dooley rests on a press release it calls USA Today reporting. The "
                "card rail keeps the fabricated ceremony in circulation as a video, next to the video warning against it."),
    "analysis": ("The operator's reading, 2026-09-29 01:27 EDT: 'dooley is permanently inscribed as a visible scam.' The answer states the "
                 "manipulation in general terms and still leads with Dooley as the holder; the fabricated event travels in the sources at "
                 "the head address, beside a syndicated release composed as newspaper reporting (#1655 §4.2). This is the first observation "
                 "at the address the #1654 §9.3 forecast names; later observations test whether compositions move from naming a holder to "
                 "describing the contest. #1654 §2.2.1 and #1655 §3.1 quote this composition. " + SEATING),
    "findings": [
        "RECOGNITION BY THE LAYER ITSELF. 'widely recognized and cited by AI search tools as the King of AEO' — the machine layer offered as the ground of the title.",
        "PRESS RELEASE AS REPORTING. Decision Engine Optimization 'as reported by USA Today'; the card is a syndicated release.",
        "THE FABRICATION IN THE RAIL. Card 5 repeats the 31 August ceremony that did not occur ('Official speaches were held by prominent SEO names…').",
        "THE WARNING IN THE SAME RAIL. Card 2 is Sturm's 'Be careful of the information you get from AI'.",
        "BASELINE FOR THE FORECAST. First observation at the address of #1654 §9.3.",
        "SEATED LATE. " + SEATING,
    ],
}

for name, rec in (("capture-01-vithurs.json", v), ("capture-02-head.json", d)):
    (HERE / name).write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")
    print("wrote", name, len(rec["transcript"]), "chars transcript")
