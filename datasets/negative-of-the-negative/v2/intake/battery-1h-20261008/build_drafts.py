#!/usr/bin/env python3
"""Author the /non drafts for battery 1h, run by the operator 2026-10-08 (message of 10:53 EDT): the five watch
addresses of the anne-carson entry, entered that morning. Operator: "signed out. incognito. all but anne carson
sappho give a google books knowledge panel, so theyre all ai mode compositions except anne carson sappho, which is
an aio popup." The four AI Mode pages show "Sign in"; their sources appear as chips (site name, +N undisclosed). The
knowledge panels are attested by the operator and are not in the pastes.
"""
import json, pathlib, re
HERE = pathlib.Path(__file__).resolve().parent
NOTE = "signed out. incognito. all but anne carson sappho give a google books knowledge panel, so theyre all ai mode compositions except anne carson sappho, which is an aio popup."


def chips(raw, lines):
    out = []
    for i, ln in enumerate(lines, 1):
        assert "\n" + ln + "\n" in raw, ln
        m = re.match(r"(.*?)(?: \+(\d+))?$", ln)
        site, extra = m.group(1), m.group(2)
        out.append(dict(n=i, site=site, title=None, snip=None, rel="third_party", url=None,
                        note=f"chip '{ln}': one site shown" + (f", {extra} undisclosed" if extra else "")))
    return out


AIMODE = {
 "autobiography-of-red": ("autobiography of red", ["Literary Hub", "eclass UoA +1", "Michelle Bailat-Jones +2", "Wikipedia +1", "Amazon.com +2", "Amazon.com +1", "Graceful | Substack·Graceful +2"]),
 "nox-anne-carson": ("nox anne carson", ["Poetry Foundation +1", "New Directions Publishing +1", "National Book Critics Circle +1", "YouTube +1", "PopMatters +1"]),
 "eros-the-bittersweet": ("eros the bittersweet", ["Wikipedia +2", "The University of Chicago Department of Mathematics +3", "Nancy Ann Roth +3", "Nancy Ann Roth", "Wikipedia +2"]),
 "if-not-winter": ("if not, winter", ["Goodreads +1", "Wikipedia +2"]),
}
for slug, (q, cl) in AIMODE.items():
    raw = (HERE / f"paste-{slug}.txt").read_text(encoding="utf-8")
    assert ("q%3D" + q.replace(" ", "%2B")) in raw, q
    c = chips(raw, cl)
    d = {"q": q, "entity": "anne-carson", "cites": len(c), "cite_list": c, "transcript": raw,
         "transcript_complete": "complete as pasted: Sign in, the tab row, the AI Mode body with its source chips and offer menu; the Google Books knowledge panel the operator reports is not in the paste",
         "sf": f"Google AI Mode at the address (Google Books knowledge panel, operator); {len(c)} source chips.",
         "date": "2026-10-08", "surface": "Google AI Mode",
         "surface_basis": f"'{NOTE}' — operator, 2026-10-08 10:53 EDT.",
         "auth": "signed out, incognito", "auth_basis": "'Sign in' shown on the page; 'signed out. incognito.' — operator, 2026-10-08 10:53 EDT.", "ev": "paste",
         "transcript_class": "CAPTURE-TIME VERBATIM RECORD — composition and sources as pasted", "transcript_read": "READ IN FULL 2026-10-08",
         "notes": {"seated_from": f"paste-{slug}.txt, the operator's message of 2026-10-08 10:53 EDT", "seat": "Seated 2026-10-08 (battery 1h), a watch address of the anne-carson entry.",
                   "watch": "entered 2026-10-08 as a watch on the Nobel motivation's compression (#1459 L1–L8 at the address); day zero"}}
    (HERE / f"draft-{slug}-aimode.json").write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    print("wrote", slug, len(c), "chips")

# anne carson sappho: an AI Overview popup, expanded; six cards after the body
slug, q = "anne-carson-sappho", "anne carson sappho"
raw = (HERE / f"paste-{slug}.txt").read_text(encoding="utf-8")
assert raw.startswith("AI Mode Conversation\nYou said: anne carson sappho")
cards = [("Poetry Foundation", "31 [\"He seems to me equal to gods\"] | The Poetry Foundation"),
         ("Wikipedia", "If Not, Winter"),
         ("Goodreads", "If Not, Winter: Fragments of Sappho"),
         ("Poetry Foundation", "1 [\"Deathless Aphrodite of the spangled mind\"]"),
         ("Internet Archive", "If not, winter : fragments of Sappho"),
         ("Google", "If Not Winter Fragments of Sappho")]
cl = []
for i, (site, title) in enumerate(cards, 1):
    k = raw.find("\n" + site + "\n" + title + "\n")
    assert k >= 0, title
    snip = raw[k + len(site) + len(title) + 3:].split("\n", 1)[0]
    cl.append(dict(n=i, site=site, title=title, snip=snip, rel="third_party", url=None, note="card"))
d = {"q": q, "entity": "anne-carson", "cites": len(cl), "cite_list": cl, "transcript": raw,
     "transcript_complete": "complete as pasted: the expanded AI Overview (headed 'AI Mode Conversation' as expanded), its body with inline markers, and six cards",
     "sf": "Google AI Overview popup, expanded; six cards (Poetry Foundation ×2, Wikipedia, Goodreads, Internet Archive, Google).",
     "date": "2026-10-08", "surface": "Google AI Overview (expanded)",
     "surface_basis": f"'{NOTE}' — operator, 2026-10-08 10:53 EDT.",
     "auth": "signed out, incognito", "auth_basis": "'signed out. incognito.' — operator, 2026-10-08 10:53 EDT.", "ev": "paste",
     "transcript_class": "CAPTURE-TIME VERBATIM RECORD — composition and sources as pasted", "transcript_read": "READ IN FULL 2026-10-08",
     "notes": {"seated_from": f"paste-{slug}.txt, the operator's message of 2026-10-08 10:53 EDT", "seat": "Seated 2026-10-08 (battery 1h), a watch address of the anne-carson entry.",
               "watch": "entered 2026-10-08 as a watch on the Nobel motivation's compression (#1459 L1–L8 at the address); day zero"}}
(HERE / f"draft-{slug}-aio.json").write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
print("wrote", slug, len(cl), "cards")
