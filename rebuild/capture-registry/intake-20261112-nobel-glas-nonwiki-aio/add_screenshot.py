"""2026-11-12 22:10 EST, before landing: the operator's screenshot of the results page for 'nonwiki' (signed out: 'Sign in' shown), attached to the
observation of the same evening. NonWiki — a sourced encyclopedia - Alexanarch is the first organic result, above the AI Overview, which gives
Stack Overflow's non-wiki. The operator: "nonwiki is still number one organic, above the overview."   python3 add_screenshot.py"""
import json, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[3]; P = ROOT / "data/EA-WG-CAPTURES-01.json"
IMG = "data/captures-images/nonwiki-aio-20261112-1.png"; assert (ROOT / IMG).exists()
reg = json.loads(P.read_text(encoding="utf-8"))
e = next(x for x in reg["entries"] if x["slug"] == "nonwiki-aio-20261102")
o = next(x for x in e["observations"] if x.get("slug") == "nonwiki-aio-20261112")
o["imgs"] = [IMG]; o["img_urls"] = ["https://www.alexanarch.org/" + IMG]
o["findings"].insert(0, "NUMBER ONE ORGANIC, BELOW IT THE ERASURE. The operator's screenshot of the results page (signed out, 'Sign in' shown): the first "
    "result is alexanarch.org, 'NonWiki — a sourced encyclopedia - Alexanarch', with its own description, 'NonWiki is an encyclopedia of public knowledge "
    "with its sources open. Each article states what is known of one entity, a poem, a person, a text, a tool, a field ...'. The AI Overview beneath it "
    "begins 'A non-wiki is a post, article, or answer written solely by a single author rather than a collaborative community', carded to Meta Stack "
    "Overflow. Retrieval ranks the entity first; the composition directly under it excludes it.")
o["d"] = o["d"].replace("the Overview gives Stack Overflow's non-wiki answer;", "the Overview gives Stack Overflow's non-wiki answer, beneath NonWiki at number one organic (screenshot);")
assert "number one organic" in o["d"]
o["transcript"] = o["transcript"].replace("[QUERENT] nonwiki", "[QUERENT] nonwiki\n\n[RESULTS PAGE, operator's screenshot, data/captures-images/nonwiki-aio-20261112-1.png: first organic result alexanarch.org, 'NonWiki — a sourced encyclopedia - Alexanarch'; the AI Overview below it.]", 1)
o["analysis"] += (" The screenshot fixes the point beyond argument: the encyclopedia is the first organic result for the string, and the composition set "
                  "directly beneath that result gives a different entity and, asked about the first, says no such entity was found.")
P.write_text(json.dumps(reg, ensure_ascii=False, indent=1)); print("ok")
