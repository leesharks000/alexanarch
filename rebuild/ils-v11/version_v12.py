"""version_v12.py — Ils ne sont pas marxistes v1.2 from v1.1 (#1728), on the operator's ruling of 2026-11-01 16:19 EST ("adopted."), adopting
the session's proposal after his point (16:14): "my point about critique was not only that marx critiqued himself, and that was sustaiend,
and now it is not, but also that marx took down others, and now critique is smoothed over". Exact replacements, each required to match once.
Reads data/texts/AXN-0BDD-text.md and the registry; writes data/issue-bodies/ILS-NE-SONT-PAS-MARXISTES-v1.2-issue.md."""
import json, pathlib, sys
R = pathlib.Path(__file__).resolve().parents[2]
txt = (R / "data/texts/AXN-0BDD-text.md").read_text()
out = txt.split("\n---\n", 1)[1].lstrip("\n")
d = next(x for x in json.loads((R / "data/registry.json").read_text())["deposits"] if int(x["deposit_number"]) == 1728)
def rep(old, new, count=1):
    global out
    n = out.count(old)
    if n != count: sys.exit(f"expected {count} of: {old[:90]!r}, found {n}")
    out = out.replace(old, new)
rep("## Marx ripped his own apart, and the parties kept the verdicts\n",
    "## Marx ripped his own apart and took down others; the parties kept the verdicts, and the present smooths the polemic\n")
rep("a commission of inquiry ([Hague Congress](https://en.wikipedia.org/wiki/Hague_Congress_(1872))).",
    "a commission of inquiry ([Hague Congress](https://en.wikipedia.org/wiki/Hague_Congress_(1872))). Those are the organizational outcomes. The polemic itself is another product, and its texts outlived the splits: the Gotha critique is at once a critique of the party's own programme and a takedown of \"the Lassallean articles of faith\", and the circular against Kriege ruled that his line \"is not communist\", in writing and on a recorded vote. The Ruge letter states the two turns as one practice: criticism that \"will shrink neither from its own discoveries, nor from conflict with the powers that be\". Turned on its own results and turned on named others, it is one criticism.")
rep("\"Greatest\" is a valuation the evidence can support without proving.",
    "\"Greatest\" is a valuation the evidence can support without proving. The present loses both turns, in two forms. The turn on one's own programme lost its carriers, as above. The turn on others is smoothed. A polemic that takes a named position apart at full strength is reclassified as infighting, bad faith or flamewar, and the composing layer balances it into perspectives. The charge this report opens with, \"the left infights\", is one instrument of that smoothing. It counts the polemic as conflict and offers quiet as the remedy. r/LeftistsForAI's sidebar sets the pair out as rules: Rule 6, \"Bad Faith\", and Rule 8, \"No factional flamewar\". #517 took the subreddit's removal apart by name, and Rule 6 removed it (§ The analysis posted, and the ban).")
rep("and the critique kept its organ only because the archive held it.",
    "and the critique kept its organ only because the archive held it. Both turns of Marx's criticism are what the record loses: the turn on his own programme to the absence of carriers, the turn on named others to smoothing.")
F = lambda k, v: f"### {k}\n\n{v}\n\n"
desc = d["description"] + " Version 1.2 (2026-11-01) states the second half of the lost legacy: Marx's criticism turned both on his own programme and on named others, the Ruge letter's one practice; the present loses the first to the absence of carriers and the second to smoothing, in which a polemic at full strength is reclassified as infighting, bad faith or flamewar and the composing layer balances it into perspectives."
sub = d["substrate"] + " Version 1.2 transformed in place on 2026-11-01 by Claude (Anthropic) in session on the operator's point and his adoption of the proposed text."
rel = "#1728 (version 1.1, superseded by this version); " + (d.get("related_identifiers_raw") or "").replace("#1725 (version 1.0, superseded by this version)", "#1725 (version 1.0)")
kw = d["keywords"] if isinstance(d["keywords"], list) else json.loads(d["keywords"])
kw = kw + ["polemic", "smoothing", "Ruge letter", "Circular against Kriege"]
ib = (F("Protocol Version", "alexanarch-deposit-protocol/v1") + F("Title", d["title"]) + F("Creator", "Sharks, Lee") + F("ORCID", "0009-0000-1599-0703")
      + F("Date", "2026-11-01") + F("Description", desc) + F("Content Type", d["content_type"]) + F("License", "CC-BY-4.0")
      + F("Substrate Disclosure", sub) + F("Keywords", ", ".join(kw)) + F("Related Identifiers", rel) + F("Version", "v1.2")
      + F("Methodology", d["methodology"] + " Version 1.2: the two turns from texts the report already cites (the Gotha covering letter, the Kriege circular, the Ruge letter, the r/LeftistsForAI sidebar).")
      + F("Falsification Conditions", d["falsification_conditions"]) + F("Supersedes", "1728") + "### Body\n\n" + out.rstrip("\n") + "\n\n"
      + "### Terms\n\n- [x] I read the deposit protocol at https://alexanarch.org/api/deposit-protocol.json\n- [x] I confirm this work is deposited under the stated license\n- [x] I confirm the substrate disclosure is accurate\n- [x] I understand that deposited content will NOT be used to train enforcement classifiers\n")
(R / "data/issue-bodies/ILS-NE-SONT-PAS-MARXISTES-v1.2-issue.md").write_text(ib)
print("written", len(ib))
