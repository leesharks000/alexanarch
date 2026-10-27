import json,pathlib
A=pathlib.Path("/home/claude/alexanarch/data/corpora")
lic=lambda l: l["payload"] if isinstance(l,dict) else str(l)
def section(corpus,heading,subtitle):
    s=json.loads((A/corpus/"source.json").read_text())
    w=s["works"]["list"]
    out=[f"## {heading}","",f"*{subtitle}*",""]
    if len(w)>12:
        from collections import Counter
        cnt=Counter(x.get("class","") for x in w)
        out+=["- Editions: "+s["edition"],"- Works by class: "+"; ".join(f"{k} {v}" for k,v in cnt.items()),
              "- Works: "+"; ".join(x["work"].split(" — ")[0] for x in w)]
    else:
        out+=["- Editions:"]+[f"  - {x['work']}" for x in w]
    out+=[f"- Licence: {lic(s['license'])}"]+[f"- Verified locus: {v}" for v in s["verified_loci"]]
    if s["loci_not_found"]: out+=[f"- Locus not found: {v}" for v in s["loci_not_found"]]
    out+=[f"- Lines: {s['lines_total']:,} in {s["works"]["count"]} text file{"s" if s["works"]["count"]!=1 else ""}",f"- Scope: {s['scope']}",f"- Why seated: {s['why_seated']}",
          f"- Files: [the seat](https://www.alexanarch.org/data/corpora/{corpus}/) — [source.json](https://www.alexanarch.org/data/corpora/{corpus}/source.json), [MANIFEST.sha256](https://www.alexanarch.org/data/corpora/{corpus}/MANIFEST.sha256). Shelf: [traininglayerliterature.org/originals/{corpus}](https://traininglayerliterature.org/originals/{corpus}/)",""]
    return "\n".join(out),s
parts=[]; tot=0; nw=0
title="EA-CORPORA-20 — The Twentieth Seating: The Ethiopian Canon in Ge'ez, the Kebra Nagast, the Apocalypses and Pseudepigrapha of the Second Temple, and Euclid, Each in Its Original Language"
hdr=f"""# {title}

# EA-CORPORA-20 — The Twentieth Seating

MANUS, 23 October 2026: "detour for an ea-corpora seating. lets see. whats available of mayan texts? and then i dont think we have much or any deuterocanonical second temple lit - all those apocalypses. and what about the ethiopian canon? and euclid. all in original language or as close to it as possible. what else?" — "and the Egyptian book of the dead" — "and what about the fragments of the book of balaam?" — "yes yes yes to all - what a meal."

The request is seated in three seatings. This, the twentieth, holds the Ethiopian canon, the Kebra Nagast, the Second Temple apocalypses and pseudepigrapha, and Euclid, and supplies the Ge'ez text layer that the 1 Enoch seat (EA-CORPORA-02/20) had queued since 25 August. The twenty-first holds Mesoamerica (the Maya codices, the Popol Vuh, the Chilam Balam, the Rabinal Achí, the Annals of the Cakchiquels) and Egypt (the Book of the Dead, the Pyramid Texts) with the Deir ʿAlla plaster text of Balaam son of Beor; the twenty-second, the Corpus Hermeticum, Gilgamesh and the Enuma Elish, the Avesta and the Rig Veda.
"""
specs=[("ethiopic-canon","Seat 20/01 — The Ethiopian Canon","The Old and New Testaments in Ge'ez, with Jubilees, the three books of Meqabyan, the Ethiopic Ezra, 4 Baruch and the Sinodos canons, from Beta maṣāḥǝft; Charles's Jubilees (1895) and Ascension of Isaiah (1900)"),
       ("kebra-nagast","Seat 20/02 — Kebra Nagast","The Glory of the Kings in Ge'ez, from Beta maṣāḥǝft"),
       ("second-temple-pseudepigrapha","Seat 20/03 — The Second Temple Apocalypses and Pseudepigrapha","Each in the original language of its earliest surviving witness, in the standard public-domain edition"),
       ("euclid","Seat 20/04 — Euclid","The Elements in Heiberg's Greek, with the Data, the Optics and the Phaenomena")]
for c,h,sub in specs:
    t,s=section(c,h,sub); parts.append(t); tot+=s["lines_total"]; nw+=s["works"]["count"]
e=json.loads((A/"ethiopic-enoch/source.json").read_text())["text_layer"]
parts.append(f"""## Seat 02/20 — 1 Enoch: the Ge'ez text layer supplied

*The seat of 25 August (Charles 1906, Dillmann 1851, as scans) queued its Unicode text layer. It is seated now from Beta maṣāḥǝft LIT1340EnochE: two edition divisions, 'ed1' and 'EOTCed' ('Text of the EOTC printed Bible').*

- Text: [text/1-enoch-geez.txt](https://www.alexanarch.org/data/corpora/ethiopic-enoch/{e['text']}), {e['lines']:,} lines, from [the TEI as fetched](https://www.alexanarch.org/data/corpora/ethiopic-enoch/{e['original']}) (commit {e['commit'][:8]})
- Licence: {e['license']}
- Verified locus: {e['verified_loci'][0]}
- The seat's record (source.json) is revised in place: status, scope and the text layer; its manifest re-hashed. Card number unchanged (02/20).
""")
tail=f"""## Not seated, and why

- 2 Enoch: it survives only in Slavonic. The open editions found are translations (Morfill and Charles, 1896); Sokolov's Slavonic text (Moscow, 1910) was not found in an open scan. QUEUED.
- Bezold's critical Kebra Nagast (1905): public domain, not found in an open scan in this pass. QUEUED.
- The Ethiopian Book of the Covenant, Didascalia and Clement of the broader canon: Beta maṣāḥǝft carries no edition text for them. QUEUED.
- Seventeen Beta maṣāḥǝft entries tagged Bible whose edition division holds under 200 Ethiopic characters (introductions, single prayers, catalogue stubs): named in 20/01's scope.
- Modern critical editions (Göttingen, de Jonge, Picard, Burchard; VanderKam's Jubilees as a book) are in copyright and are not seated; where Beta maṣāḥǝft's text rests on one, its own statement of the basis is recorded with the work.
- Euclid in translation (Heath, 1908), and the Elements volumes of the Opera omnia, which the Perseus TEI already gives.
- Everything marked QUEUED in a seat's scope.

## How the seats were made

Sources located in Beta maṣāḥǝft's Works repository (cloned at commit 3550dc59 of 23 October 2026; every file measured for the Ethiopic characters in its edition division), on the Internet Archive (advanced search; item metadata read for access restriction, volume and files) and in the Perseus Digital Library (PerseusDL/canonical-greekLit at commit 0189b9c8). Each item's front matter read against the edition claimed for it. Every Internet Archive file checked against the md5 the Archive publishes for it; none differed. TEI reduced to plain text by code with chapter and verse kept; OCR layers seated as fetched, uncorrected, the scan as witness. Every file hashed into its seat's MANIFEST.sha256; every verified locus is a string found in the seated text by the builder, rebuild/corpora/ea-corpora-20/seat.py, from the specifications beside it. {nw} works and {tot:,} lines in four new seats, and 1,502 lines added to a fifth.
"""
body=hdr+"\n"+"\n".join(parts)+"\n"+tail
pathlib.Path("body20.md").write_text(body,encoding="utf-8"); print(len(body.split()),"words;",nw,"works;",tot,"lines")
json.dump({"title":title,"works":nw,"lines":tot},open("body20-meta.json","w"))
