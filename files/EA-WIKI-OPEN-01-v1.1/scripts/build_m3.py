"""Assembly round 02, Message 3: the readers' break cases, pinned at the articles' own sentences, with their sources.
Every sentence is located in the pinned revision's plain text by code; every window in its saved source."""
import sys, re, hashlib, json, pathlib
SC = '/tmp/claude-0/-home-claude/97be5201-55d8-50c9-b9d9-c76c8dde5ac6/scratchpad/'
M3 = SC + 'm3/'; SRC = M3 + 'src/'
sys.path.insert(0, SC + 'st')
from cases import SOURCES as OLD
OUT = pathlib.Path('/home/claude/drafts/wiki-open/assembly-02')
F = '2026-10-23'
SOURCES = {
 'SE34GR': OLD['SE34GR'], 'MIT': OLD['MIT'], 'SEPLOGIC': OLD['SEPLOGIC'],
 'SEPANC': dict(file=SRC+'sep-logic-ancient.flat.txt', raw=SRC+'sep-logic-ancient.html',
   cite=f'Susanne Bobzien, "Ancient Logic," Stanford Encyclopedia of Philosophy, current entry (cited in the Syllogism article; fetched {F})'),
 'APRGR': dict(file=SRC+'apr-gr.flat.txt', raw=SRC+'apr-gr-1.wiki',
   cite=f'Aristotle, Prior Analytics I, Greek text, el.wikisource "Αναλυτικών προτέρων/1" (raw wikitext; "ἐνᾧ" at 24b19 is the page\'s own spacing; fetched {F})'),
 'APRMIT': dict(file=SRC+'pa-mit.flat.txt', raw=SRC+'pa-mit.html',
   cite=f'Aristotle, Prior Analytics I, tr. A. J. Jenkinson, classics.mit.edu/Aristotle/prior.1.i.html (fetched {F})'),
 'BARNES': dict(file=None, raw=None, text='History\'s first logic has also been the most influential...',
   cite='Jonathan Barnes (ed.), The Cambridge Companion to Aristotle (Cambridge University Press, 1995), p. 27: the book was not fetched; given here is the whole of what the article\'s own citation quotes from it (the cite template\'s "quote" field)'),
 'NEGR': dict(file=SRC+'ne-gr.flat.txt', raw=SRC+'ne-gr-1106b.html',
   cite=f'Aristotle, Nicomachean Ethics II.6, 1106b33–1107a13, Greek, ed. I. Bywater (Oxford, 1894), Perseus Digital Library, Bekker pages 1106b and 1107a joined (fetched {F})'),
 'NEMIT': dict(file=SRC+'ne-mit.flat.txt', raw=SRC+'ne-mit-2.html',
   cite=f'Aristotle, Nicomachean Ethics II, tr. W. D. Ross, classics.mit.edu/Aristotle/nicomachaen.2.ii.html (fetched {F})'),
 'GRANT': dict(file=SRC+'grant.flat.txt', raw=SRC+'ethicsofaristotl01arisuoft.txt',
   cite=f'Alexander Grant, The Ethics of Aristotle, Illustrated with Essays and Notes, 4th ed. (Longmans, Green, 1885), vol. 1, Essay IV, pp. 251–262 (cited at the sentence as Grant, pp. 251–262); Internet Archive OCR text, ethicsofaristotl01arisuoft, quoted as the OCR gives it (fetched {F})'),
 'CATGR': dict(file=SRC+'cat-gr.flat.txt', raw=SRC+'cat-gr-wikisource.html',
   cite=f'Aristotle, Categories, Greek text, el.wikisource "Κατηγορίαι" (fetched {F})'),
 'CATMIT': dict(file=SRC+'cat-mit.flat.txt', raw=SRC+'cat-mit.html',
   cite=f'Aristotle, Categories, tr. E. M. Edghill, classics.mit.edu/Aristotle/categories.1.1.html (fetched {F})'),
 'LSJ': dict(file=SRC+'lsj-arete.flat.txt', raw=SRC+'lsj-arete.html',
   cite=f'H. G. Liddell and R. Scott, A Greek–English Lexicon, 9th ed. (Oxford, 1940), s.v. ἀρετή, Perseus Digital Library (cited at the sentence as LSJ; fetched {F})'),
}
# the Nicomachean Ethics window spans two Perseus pages: join the two Greek passages as printed
g6 = open(SRC+'ne-gr-1106b.flat.txt', encoding='utf-8').read(); g7 = open(SRC+'ne-gr-1107a.flat.txt', encoding='utf-8').read()
a = g6.index('καὶ διὰ ταῦτ᾽ οὖν τῆς μὲν κακίας'); b = g6.index('τῇ πρὸς ἡμᾶς,', a) + len('τῇ πρὸς ἡμᾶς,')
c = g7.index('ὡρισμένῃ λόγῳ'); d = g7.index('οὐδ᾽ αἱ ἐλλείψεις.', c) + len('οὐδ᾽ αἱ ἐλλείψεις.')
open(SRC+'ne-gr.flat.txt', 'w', encoding='utf-8').write((g6[a:b] + ' ' + g7[c:d]).replace('” 1 ἔστιν', '” ἔστιν'))
# LSJ spacing: Perseus sets a space before punctuation
import html as _h
_l = open(SRC+'lsj-arete.html', encoding='utf-8', errors='replace').read()
_l = re.sub(r'(?s)<script.*?</script>|<style.*?</style>', '', _l); _l = re.sub(r'\s+', ' ', _h.unescape(re.sub(r'<[^>]+>', ' ', _l)))
open(SRC+'lsj-arete.flat.txt', 'w', encoding='utf-8').write(re.sub(r'\s+([,.:;])', r'\1', _l).strip())

def norm(s): return re.sub(r'\s+', ' ', s)
TXT = {k: (norm(open(v['file'], encoding='utf-8').read()) if v.get('file') else v['text']) for k, v in SOURCES.items()}
SHA = {k: hashlib.sha256(open(v['raw'], 'rb').read()).hexdigest() for k, v in SOURCES.items() if v.get('raw')}

def window(src, anchor, n, back=160, end=None):
    t = TXT[src]; i = t.index(anchor)
    a = max(0, i - back); k = t.rfind('. ', a, i); a = k + 2 if k != -1 else a
    if back == 0: a = i
    b = min(len(t), i + len(anchor) + n); j = t.find('. ', b); b = j + 1 if j != -1 and j - b < 300 else b
    if end: b = t.index(end, i) + len(end)
    return ('…' if a > 0 else '') + t[a:b].strip() + ('…' if b < len(t) else '')

ARTS = {
 'SY': ('Syllogism', '1376036931'), 'PA': ('Prior Analytics', '1363223373'), 'NE': ('Nicomachean Ethics', '1376958477'),
 'AV': ('Avicenna', '1377286292'), 'CA': ('Categories (Aristotle)', '1367090838'), 'AR': ('Aristotle', '1379112110'),
 'ARE': ('Arete', '1378364950'), 'OR': ('Organon', '1370990006'),
}
FN = {'SY': 'Syllogism', 'PA': 'Prior_Analytics', 'NE': 'Nicomachean_Ethics', 'AV': 'Avicenna', 'CA': 'Categories_Aristotle', 'AR': 'Aristotle', 'ARE': 'Arete', 'OR': 'Organon'}
ART = {k: open(f'{M3}{FN[k]}.{ARTS[k][1]}.txt', encoding='utf-8').read() for k in ARTS}
ARTSHA = {k: hashlib.sha256(open(f'{M3}{FN[k]}.{ARTS[k][1]}.wiki', 'rb').read()).hexdigest() for k in ARTS}

def paragraph(k, sentence):
    for p in [p for p in ART[k].split('\n\n') if p.strip()]:
        if norm(sentence) in norm(p):
            q = re.sub(r'=+[^=]+=+\s*', '', norm(p)); q = re.sub(r'thumb\|(?:\d+px\|)?[^.]*\.\s*', '', q)
            return q.strip()
    sys.exit(f'sentence not in {k}: {sentence[:60]}')

def locus(k, sentence):
    t = ART[k]; i = norm(t).index(norm(sentence))
    heads = [m for m in re.finditer(r'(?m)^=+\s*([^=\n]+?)\s*=+\s*$', t)]
    # map normalized offset back approximately via the raw text
    j = t.find(sentence[:40]); sec = 'lead'
    for h in heads:
        if h.start() < j: sec = h.group(1)
    return sec

CASES = [
 dict(id='SY-1', art='SY', w="A syllogism (, syllogismos, 'conclusion, inference') is a kind of logical argument that applies deductive reasoning to arrive at a conclusion based on two propositions that are asserted or assumed to be true.",
      w_display="A syllogism (Ancient Greek συλλογισμός, syllogismos, 'conclusion, inference') is a kind of logical argument that applies deductive reasoning to arrive at a conclusion based on two propositions that are asserted or assumed to be true.",
      cited='uncited (the article cites the Stanford Encyclopedia entry "Ancient Logic" elsewhere)', where='lead, sentence 1',
      windows=[('APRGR', 'συλλογισμὸς δέ ἐστι λόγος', 260), ('APRMIT', 'A syllogism is discourse in which', 260), ('SEPANC', 'Aristotle defines a syllogism as', 0)],
      wopts={'SEPANC': dict(back=0, end='satisfy these conditions.')}),
 dict(id='PA-1', art='PA', w="Aristotle's Prior Analytics represents the first time in history when Logic is scientifically investigated.",
      cited='the paragraph ends with a citation to Barnes (ed.) 1995, p. 27, after the next sentence, which quotes Sophistical Refutations; the sentence itself is uncited', where=None,
      windows=[('BARNES', None, 0), ('SE34GR', 'Ταύτης δὲ τῆς πραγματείας', 0), ('MIT', 'Of this inquiry, on the other hand', 0)],
      wopts={'SE34GR': dict(back=0, end='πολλὴν ἔχειν χάριν.'), 'MIT': dict(back=0, end='your warm thanks.')}),
 dict(id='NE-1', art='NE', w="Aristotle says moral virtues are found at a mean (mesótēs) between deficiency and excess.",
      cited='sfn Grant, pp. 251–262', where=None,
      windows=[('NEGR', 'καὶ διὰ ταῦτ᾽ οὖν τῆς μὲν κακίας', 1200), ('NEMIT', 'Virtue, then, is a state of character', 900), ('GRANT', 'the whole bearing of his use of the term', 700)]),
 dict(id='CA-1', art='CA', w="The Categories places every object of human apprehension under one of ten categories (known to medieval writers as the Latin term praedicamenta).",
      cited='uncited', where=None,
      windows=[('CATGR', 'Τῶν κατὰ μηδεμίαν συμπλοκὴν λεγομένων', 700), ('CATMIT', 'Expressions which are in no way composite', 700)]),
 dict(id='AR-1', art='AR', w="Aristotle was the founder of term logic, pioneered the study of zoology, and benefited future scientists and philosophers through his contributions to the scientific method.",
      cited='sfn "Aristotle (Greek philosopher)", Encyclopædia Britannica; Durant 2006, p. 92; Kukkonen 2010, pp. 70–77 (none fetched: the Britannica page and its archived copy were not reachable from here, and the two books are not online); the article cites the Stanford Encyclopedia entry "Aristotle\'s Logic" elsewhere', where=None,
      windows=[('SEPLOGIC', 'Aristotle’s logical works contain the earliest formal study of logic that we have', 400), ('SE34GR', 'Καὶ περὶ μὲν τῶν ῥητορικῶν', 0), ('MIT', 'Moreover, on the subject of Rhetoric', 0)],
      wopts={'SE34GR': dict(back=0, end='πολλὴν ἔχειν χάριν.'), 'MIT': dict(back=0, end='your warm thanks.')}),
 dict(id='ARE-1', art='ARE', w="' () is a concept in ancient Greek thought that refers to \"excellence\" of any kind—especially a person or thing's \"full realization of potential or inherent function.\"",
      w_display="Arete (Ancient Greek ἀρετή, aretḗ) is a concept in ancient Greek thought that refers to \"excellence\" of any kind—especially a person or thing's \"full realization of potential or inherent function.\"",
      cited='LSJ s.v. ἀρετή (for "excellence of any kind"); Collins English Dictionary, 2023 (for "full realization of potential or inherent function"; not fetched)', where='lead, sentence 1',
      windows=[('LSJ', 'ἀρετή [ α^], ἡ, A.', 900)], wopts={'LSJ': dict(back=0, end='Pol. 1295a37, etc.;')}),
 dict(id='OR-1', art='OR', w="The Organon (, meaning \"instrument, tool, organ\") is the standard collection of Aristotle's six works on logical analysis and dialectic.",
      w_display="The Organon (Ancient Greek Ὄργανον, meaning \"instrument, tool, organ\") is the standard collection of Aristotle's six works on logical analysis and dialectic.",
      cited='uncited (the article cites the Stanford Encyclopedia entry "Aristotle\'s Logic", its section on the Organon, elsewhere)', where='lead, sentence 1',
      windows=[('SEPLOGIC', 'The ancient commentators grouped together several', 500)]),
]
PLACE = [dict(id='AV-1', art='AV', where='lead', start='Ibn Sina ( – 22 June 1037)', display_start='Ibn Sina (c. 980 – 22 June 1037)')]

M = []; m = M.append
m('EA-WIKI-OPEN-01 · ASSEMBLY ROUND 02 · MESSAGE 3 OF 3 · THE BREAK CASES')
m('')
m('This message follows the reader\'s Message 2 reply, which has been saved. The readers of this round proposed twenty break cases between them. Ten are cases this round already reads. Two could not be pinned: one sentence does not occur in its article at the current revision, and one cites a source that could not be fetched from here. No proposed sentence occurs word for word in its article; each case below is pinned at the article\'s own sentence nearest the proposal, at the current revision, with its cited sources, in Message 1\'s format. The reader runs Message 1\'s procedure on each under Message 1\'s rules, which are unchanged, blind to every other reader\'s reading, and returns the Message 1 JSON with the one field added below.')
m('')
m('ONE FIELD ADDED IN THIS MESSAGE. (i) HOLDER AND MOOD. For the claim the sentence makes: who holds it in the source (the author speaking in their own voice; a party the author reports; the author\'s audience; a later tradition) and in what mood the source states it (asserted; conditional; hedged; put to the audience\'s judgment; reported); then the same two things for the sentence; then whether they match. Each with the span that shows it. In the JSON, after "retained_authority": "holder_and_mood": {"source": {"holder": "...", "mood": "...", "span": {"source": "...", "quote": "..."}}, "sentence": {"holder": "...", "mood": "...", "span": {"source": "ARTICLE", "quote": "..."}}, "match": true | false | "unresolved"}. For a placement case the field is null.')
m('')
m('The field is also asked of one case already read. CASE SR-W2 (Message 1, its sentence and its source material as given there): the reader returns, as the last object of the array, only {"case": "SR-W2", "holder_and_mood": {...}, "spans": [...]}, from Message 1\'s materials.')
m('')
m('THE CASES. The source windows were chosen by the session that prepared this test; the reader says where a window is too narrow to decide the case, and what is missing. "ARTICLE" is the source ID for quotations from the sentence, its paragraph or a lead given here.')
for c in CASES:
    t, rev = ARTS[c['art']]
    if norm(c['w']) not in norm(ART[c['art']]): sys.exit('not found ' + c['id'])
    where = c['where'] or locus(c['art'], c['w'])
    m('')
    m(f'=== CASE {c["id"]} · SENTENCE · Wikipedia, "{t}", revision {rev}, {where} ===')
    m(f'SENTENCE: {c.get("w_display", c["w"])}')
    m(f'HOW IT IS CITED: {c["cited"]}')
    p = paragraph(c['art'], c['w'])
    if 'w_display' in c: p = p.replace(c['w'], c['w_display'])
    m(f'ITS PARAGRAPH: {p}')
    m('SOURCE MATERIAL:')
    for s, anc, n in c['windows']:
        m(f'  [{s}] {SOURCES[s]["cite"]}')
        m(f'  "{TXT[s] if anc is None else window(s, anc, n, **(c.get("wopts", {}).get(s, {})))}"')
for c in PLACE:
    t, rev = ARTS[c['art']]; L = norm(ART[c['art']].split('\n=')[0]); i = L.index(c['start'])
    m('')
    m(f'=== CASE {c["id"]} · PLACEMENT · Wikipedia, "{t}", revision {rev}, {c["where"]} ===')
    m(f'THE LEAD, WHOLE: {L[i:].strip().replace(c["start"], c["display_start"])}')
    m('SOURCE MATERIAL: none supplied. The reader records the case at placement only: whether the lead states any operation of the subject (a stated method, argument or result, with its object), and quotes it.')
m('')
m('OUTPUT. One JSON array in a code block, one object per case in the order above (SY-1, PA-1, NE-1, CA-1, AR-1, ARE-1, OR-1, AV-1), each in Message 1\'s format with "holder_and_mood" added, then the SR-W2 object; nothing else.')
TXT3 = '\n'.join(M) + '\n'
(OUT / 'message-3-break-cases.txt').write_text(TXT3, encoding='utf-8')
print(len(TXT3.encode()), 'bytes')
# leak check: nothing of the session's readings or the operator's ruling
for bad in ['TACHYON', 'inversion', 'Lee', '#1603', 'v1.1', '184b3', 'hearers', 'pardon']:
    if bad in TXT3: print('M3 contains:', bad)
man = ['', '## Message 3 (built ' + F + ')', '', f'- `message-3-break-cases.txt`: `{hashlib.sha256(TXT3.encode()).hexdigest()}`', '', 'Pinned articles:']
man += [f'- "{t}", revision {r}: `{ARTSHA[k]}`' for k, (t, r) in ARTS.items()]
man += ['', 'Sources:'] + [f'- {k}: {v["cite"]}' + (f': `{SHA[k]}`' if k in SHA else '') for k, v in SOURCES.items()]
man += ['', 'Proposals and their disposition (twenty proposed; no proposed sentence occurs verbatim):',
 '- Gemini: Syllogism → SY-1 (lead sentence 1); Prior Analytics → PA-1 (the article\'s priority sentence, which quotes SE 34); Nicomachean Ethics → NE-1; Avicenna → AV-1 (Gemini proposed an entity lead whose operation survives; the lead states none, and the Floating Man is in the body, so it is pinned as a placement case); Categories (Aristotle) → CA-1. Gemini\'s five revision ids are not these articles (C.10).',
 '- Muse Spark: Aristotle → AR-1 ("founder of term logic", the article\'s nearest sentence to the proposal on syllogistic); Sophistical Refutations completeness sentence: not in revision 1361634710, not pinned; Theophrastus = TH-1; Alan Turing = TU-1; If Not, Winter square brackets: the sentence is real, its source (Jansen 2019, p. 81, Bloomsbury) not reachable, not pinned.',
 '- DeepSeek: Arete → ARE-1; Organon → OR-1; Anne Carson = AC-1; Alan Turing = TU-1; Sophistical Refutations heading = SR-W7-8.',
 '- ChatGPT: all five are this round\'s pinned specimens (SR-W2, TH-2, EB-1, CU-1, IW-1).',
 '', 'The added field (holder and mood) tests the operation stated in v1.1 §6.3 (c) without stating it; SR-W2 is re-asked for that field alone. Message 1\'s rules are unchanged, so the round stays under fixed rules.']
mf = OUT / 'MANIFEST-session-only.md'; old = mf.read_text(encoding='utf-8'); old = old.split('\n## Message 3 (built')[0]; mf.write_text(old.rstrip('\n') + '\n' + '\n'.join(man) + '\n', encoding='utf-8')
json.dump(CASES + PLACE, open(OUT / 'cases-message3.json', 'w'), ensure_ascii=False, indent=1)
