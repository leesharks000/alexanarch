#!/usr/bin/env python3
"""restore_sf_line.py — give the downstream galleries their surface line back.

THE REGRESSION. leesharks.com and godkinggoogle.com render a card meta row as
`${e.date} · ${e.sf}`. In v9.6 every entry carried `sf` — 204 of 204, e.g.
'AI Overview + AI Mode, 9+ sources'. The rebuild stopped emitting it: 0 of 315.
Every downstream card has since shown a date, a middot, and nothing.

That line is NOT reducible to the alexanarch card, which renders surface and
citation count as separate rows in a definition list. `sf` is a compact composite
belonging to the downstream galleries, and it is restored here rather than
replaced with something alexanarch happens to have.

THREE SOURCES, IN ORDER OF AUTHORITY:
  1. the v9.6 archive, by slug — the line as it was actually published (180 hits)
  2. canonical `sf_line_unparsed`, by slug — the operator's own surface note
  3. synthesis from surface + citation count, marked as derived

A synthesized line is flagged `sf_derived: true` so a reader can tell a recovered
line from a reconstructed one.
"""
import json, pathlib, datetime

ROOT = pathlib.Path(__file__).resolve().parents[1]
PROJ = ROOT / "data/EA-WG-CAPTURES-01.json"
V96 = ROOT / "data/EA-WG-CAPTURES-01-v9.6.json"
CANON = ROOT / "rebuild/capture-registry/EA-WG-CAPTURES-01-REBUILD.json"

SHORT = {"Google AI Overview": "AI Overview", "Google AI Mode (native)": "AI Mode",
         "Google Search results page (no AI surface)": "Google Search (no AI surface)",
         "Google Knowledge panel": "Knowledge panel", "Bing Copilot": "Bing Copilot",
         "ChatGPT": "ChatGPT", "Google Scholar": "Google Scholar",
         "SciLynk aggregator record page": "SciLynk record page",
         "TikTok Studio post analysis": "TikTok Studio",
         "UNRESOLVED": "surface unresolved", "UNDETERMINED": "surface undetermined"}


def main():
    p = json.loads(PROJ.read_text())
    v96 = {e["slug"]: e["sf"] for e in json.loads(V96.read_text())["entries"]
           if e.get("slug") and e.get("sf")}
    canon = {}
    for a in json.loads(CANON.read_text())["addresses"]:
        for o in a["observations"]:
            if o.get("legacy_slug") and o.get("sf_line_unparsed"):
                canon.setdefault(o["legacy_slug"], o["sf_line_unparsed"])

    src = {"v9.6": 0, "canonical": 0, "derived": 0}
    for e in p["entries"]:
        obs = e.get("observations") or [e]
        slugs = [o.get("slug") for o in obs if o.get("slug")] + [e.get("slug")]
        line = next((v96[s] for s in slugs if s in v96), None)
        if line:
            src["v9.6"] += 1
        else:
            line = next((canon[s] for s in slugs if s in canon), None)
            if line:
                src["canonical"] += 1
        if not line:
            surfaces = [SHORT.get(s, s) for s in (e.get("surfaces") or [e.get("surface")]) if s]
            n = max([o.get("cites") or 0 for o in obs] or [0])
            line = " + ".join(dict.fromkeys(surfaces)) or "surface undetermined"
            if n:
                line += f", {n} source{'s' if n != 1 else ''}"
            e["sf_derived"] = True
            src["derived"] += 1
        # a series says so, because the downstream card has no other way to show it
        if len(obs) > 1:
            line += f" · {len(obs)} observations"
        e["sf"] = line

    p["_sf_rule"] = ("`sf` is the compact surface line the DOWNSTREAM galleries render in their card meta row. It "
                     "is not reducible to the alexanarch card, which shows surface and citation count as separate "
                     "definition-list rows. Recovered from the v9.6 archive where it was published, from canonical "
                     "sf_line_unparsed where the operator wrote one, and synthesized otherwise — synthesis marked "
                     "`sf_derived: true`. Restored " + datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d") + ".")
    PROJ.write_text(json.dumps(p, indent=1, ensure_ascii=False))
    print("sf restored on %d entries" % len(p["entries"]))
    for k, v in src.items():
        print(f"   {v:>4}  from {k}")
    for e in p["entries"][:6]:
        print(f"     «{str(e.get('q'))[:34]:<34}» sf={e['sf'][:56]!r}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
