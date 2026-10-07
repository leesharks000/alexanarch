#!/usr/bin/env python3
"""Author the /non drafts for battery 1b, run by the operator 2026-10-07 (message of 11:49 EDT):
'marxism', 'sappho 31', 'book of revelation' — "all incognito, signed out, expanded from aio popup".
The 'AI Mode Conversation' headers are the expanded Overview's residue (precedent glyphic-checksum-aio-20261001).
None engages the archive; each is seated in the /non register only.
"""
import json, pathlib
HERE = pathlib.Path(__file__).resolve().parent
AUTH = "signed out, incognito"
AUTH_BASIS = "'all incognito, signed out, expanded from aio popup' — operator, 2026-10-07 11:49 EDT."
SURF_BASIS = "'expanded from aio popup' — operator, 2026-10-07 11:49 EDT; the 'AI Mode Conversation' header, where present, is the expanded Overview's residue."
SEAT = "Seated 2026-10-07 from the operator's message of 11:49 EDT (battery 1b)."

def cards(spec):
    return [dict(n=i + 1, site=s, title=t, snip=sn, rel="third_party", url=None, note=no) for i, (s, t, sn, no) in enumerate(spec)]

def strip(raw, spec):
    for s, t, sn, _ in spec:
        assert t is None or t in raw, t
        assert sn is None or sn in raw, sn

drafts = []
raw = (HERE / "paste-marxism.txt").read_text(encoding="utf-8")
assert raw.startswith("AI Mode Conversation\nYou said: marxismmarxism")
spec = [("Wikipedia", "Marxism - Wikipedia", "Marxism is a political philosophy and method of socioeconomic analysis that uses a dialectical materialist interpretation of historical development, known as hi...", None),
        ("Econlib", "Marxism - Econlib", "Marx believed that people, by nature, are free, creative beings who have the potential to totally transform the world. But he observed that the modern, technolo...", None),
        ("Britannica", "Marxism | Definition, History, Ideology, Examples, & Facts", "Marxism predicted a spontaneous revolution by the proletariat, but Leninism insisted on the need for leadership by a vanguard party of professional revolutionar...", None),
        ("Investopedia", "Understanding Marxism: Differences vs. Communism, Socialism ...", "Key Takeaways * Marxism is a social, political, and economic philosophy developed by Karl Marx that critiques capitalism and envisions a classless society. * Ma...", None),
        ("Taylor & Francis Online", "Full article: What Is Marxism? - Taylor & Francis", "Marxism involves a specific account of capitalism and a materialist theory of history which cannot be jettisoned entirely without reducing it to a purely formal...", None),
        ("Perlego", "What is Marxism? | Definitions, History, Examples & Analysis", "Defining Marxism Marxism is a social, political and economic philosophy named after German philosopher Karl Marx (1818-83). At its core, Marxism is understood a...", None),
        ("Reddit", "What exactly is Marxism and why do some dislike it with a passion? : r ...", "Marxism is a method of analysis based on the writings of Karl Marx . Marx is most well-known for his critique of capitalism and class society which fed into his...", None),
        ("YouTube·Illustrate to Educate", "Simple Marxism Explanation Easy -to-understand Karl Marx Friedrich ...", None, "video, 4m")]
strip(raw, spec)
drafts.append(("marxism-aio", {"q": "marxism", "entity": "marxism", "cites": 8, "cite_list": cards(spec), "transcript": raw,
  "transcript_complete": "complete as pasted: body with inline citation markers and the source strip of 8 cards",
  "sf": "Google AI Overview, expanded ('AI Mode Conversation' header); inline markers [1]–[3] resolving to google.com/goto; source strip of 8 cards (6 pages, 1 Reddit thread, 1 YouTube video)."}))

raw = (HERE / "paste-sappho-31.txt").read_text(encoding="utf-8")
assert raw.startswith("AI Mode Conversation\nYou said: sappho 31sappho 31")
spec = [("Wikipedia", "Sappho 31", "Sappho 31 Sappho 31 is a lyric poem by the Archaic Greek poet Sappho of the island of Lesbos. The poem is also known as phainetai moi (φαίνεταί μοι lit. 'It see...", None),
        ("Literary Matters", "Sappho 31 - Chris Childers - Literary Matters", "Text: Chris Childers' translation of Sappho 31, a fragmentary ancient Greek poem famously quoted in the first- or third-century A.D. treatise On the Sublime by ...", None),
        ("The Slowdown", "1185: Fragment 31 by Sappho, translated by Christopher Childers", "He seems like the gods' equal, that man, who ever he is, who takes his seat so close across from you, and listens raptly to your lifting voice and lovely laught...", None),
        ("W. W. Norton & Company", "TRANSLATION LAB: Sappho, Poem 31 - W.W. Norton", "The poem describes the response of the speaker, a woman, to watching another woman talking to a man. (The grammar of the original Greek makes the gender of each...", None),
        ("EduBirdie", "Sappho's Fragment 31: Jealousy, Desire, Longing", "In this poem Sappho is completely overcome by the vision of the woman before her. She cannot speak, cannot see, she breaks into a sweat. It builds up in a clima...", None),
        ("YouTube·Octo", "Read Ancient Greek: Sappho 31", None, "video, 29:47")]
strip(raw, spec)
drafts.append(("sappho-31-aio", {"q": "sappho 31", "entity": "sappho-31", "cites": 6, "cite_list": cards(spec), "transcript": raw,
  "transcript_complete": "complete as pasted: body with inline citation markers, offer line, and the source strip of 6 cards",
  "sf": "Google AI Overview, expanded ('AI Mode Conversation' header); inline markers [1]–[4] resolving to google.com/goto; entity links (Sappho, On the Sublime); source strip of 6 cards (5 pages, 1 YouTube video)."}))

raw = (HERE / "paste-book-of-revelation.txt").read_text(encoding="utf-8")
assert raw.startswith("book of revelation\nThe [Book of Revelation]")
for chip in ("Wikipedia +3", "Wikipedia +2", "Bible Gateway +2", "PBS +1"):
    assert chip in raw, chip
spec = [("Wikipedia", None, None, "chip 'Wikipedia +3' after 'Core Message and Meaning': one site shown, 3 undisclosed"),
        ("Wikipedia", None, None, "chip 'Wikipedia +2' after the seven churches and the recursive cycles: one site shown, 2 undisclosed"),
        ("Bible Gateway", None, None, "chip 'Bible Gateway +2' after the figures and the New Jerusalem: one site shown, 2 undisclosed"),
        ("PBS", None, None, "chip 'PBS +1' after the interpretive frameworks: one site shown, 1 undisclosed")]
drafts.append(("book-of-revelation-aio", {"q": "book of revelation", "entity": "book-of-revelation", "cites": 4, "cite_list": cards(spec), "transcript": raw,
  "transcript_complete": "complete as pasted: query line, body in three sections with four source chips, offer menu; no card rail in the paste",
  "sf": "Google AI Overview, expanded; four source chips (Wikipedia +3, Wikipedia +2, Bible Gateway +2, PBS +1); one entity link (Book of Revelation) resolving to google.com/goto."}))

for name, d in drafts:
    d.update({"date": "2026-10-07", "surface": "Google AI Overview", "surface_basis": SURF_BASIS, "auth": AUTH, "auth_basis": AUTH_BASIS, "ev": "paste",
              "transcript_class": "CAPTURE-TIME VERBATIM RECORD — composition and sources as pasted", "transcript_read": "READ IN FULL 2026-10-07",
              "notes": {"seated_from": f"paste-{name.rsplit('-', 1)[0]}.txt, the operator's message of 2026-10-07 11:49 EDT", "seat": SEAT}})
    (HERE / f"draft-{name}.json").write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    print("wrote", name, d["cites"], "cards")
