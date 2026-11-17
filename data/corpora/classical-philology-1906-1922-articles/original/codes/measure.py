#!/usr/bin/env python3
"""measure.py — the conviction lexicon over reviews and articles (Dead Letters §8.2).
For each text: every sentence that judges by conviction (convinc-, persua-, compelling, cogent, plausib-,
'carry conviction', überzeug-, convainc-, convinc(ente), persuasiv-), whether it is negative, whether it names
an atom (a locus reference in the sentence), and whether it falls in the text's last fifth (the verdict).
Lexicon instrument only: it finds the sentences; it does not read them."""
import re
POS=re.compile(r"\b(convinc\w*|persua\w*|compelling\w*|cogent\w*|plausib\w*|implausib\w*|carr(?:y|ies|ied)\s+conviction|überzeug\w*|convainc\w*|convincent\w*|convincente\w*|persuasiv\w*|persuasion)\b",re.I)
NEG=re.compile(r"\b(not|no|nor|never|un\w*convinc\w*|unpersua\w*|unconvinc\w*|implausib\w*|fail\w*|less|hardly|scarcely|doubt\w*|nicht|kaum|keineswegs|wenig|pas|guère|non|poco|nessun\w*|un[- ]?)\b|\bun(convinc|persua)",re.I)
ATOM=re.compile(r"(\b\d{1,4}\.\d{1,4}\b|\b\d{1,4}[a-e]\d*\b|\bl{1,2}\.\s*\d|\blines?\s+\d|\bvv?\.\s*\d|\bverses?\s+\d|\bfr(?:ag)?\.\s*\d|\bfrr\.\s*\d|\bpp?\.\s*\d|§\s*\d|\bch(?:ap)?\.\s*\d|\bcol\.\s*\d|\bn\.\s*\d|[Ͱ-Ͽἀ-῿]{3,})")
SPLIT=re.compile(r'(?<=[.!?;])\s+(?=[A-ZÀ-ÖØ-Þ“"(\[])')
def judge(text):
    t=re.sub(r'\s+',' ',text or '').strip(); n=len(t)
    if not n: return {'chars':0,'hits':[]}
    hits=[]; pos=0; S=SPLIT.split(t)
    for k,s in enumerate(S):
        i=t.find(s,pos); pos=i+len(s) if i>=0 else pos
        if POS.search(s):
            hits.append({'s':s[:600],'prev':(S[k-1][-400:] if k else ''),'next':(S[k+1][:400] if k+1<len(S) else ''),
                         'neg':bool(NEG.search(s)),'atom':bool(ATOM.search(s)),'pos':round(i/n,3) if i>=0 else None,'verdict':(i/n)>=0.8 if i>=0 else None})
    return {'chars':n,'hits':hits}
