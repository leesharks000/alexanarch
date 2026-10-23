"""Assembly round 02: three separate files, one per message, each pasted whole; a session-only manifest.
Built from cases.py with the readings brought to the state of the v1.1 draft after round 01 (C.7-C.9)."""
import sys, re, hashlib, json, copy, pathlib
ST = '/tmp/claude-0/-home-claude/97be5201-55d8-50c9-b9d9-c76c8dde5ac6/scratchpad/st'
SC = '/tmp/claude-0/-home-claude/97be5201-55d8-50c9-b9d9-c76c8dde5ac6/scratchpad/'
sys.path.insert(0, ST)
import cases
from cases import SOURCES, ARTICLES
OUT = pathlib.Path('/home/claude/drafts/wiki-open/assembly-02'); OUT.mkdir(parents=True, exist_ok=True)

ARTICLES = dict(ARTICLES)
ARTICLES['TU'] = dict(title='Alan Turing', rev='1381462563', file=SC + 'wiki/Alan_Turing.1381462563.txt', raw=SC + 'wiki/Alan_Turing.1381462563.wiki')
ARTICLES['CU'] = dict(title='Marie Curie', rev='1381292352', file=SC + 'wiki/Marie_Curie.1381292352.txt', raw=SC + 'wiki/Marie_Curie.1381292352.wiki')

def norm(s): return re.sub(r'\s+', ' ', s)
TXT = {k: norm(open(v['file'], encoding='utf-8').read()) for k, v in SOURCES.items()}
ART = {k: open(v['file'], encoding='utf-8').read() for k, v in ARTICLES.items()}
SHA = {k: hashlib.sha256(open(v['raw'], 'rb').read()).hexdigest() for k, v in {**SOURCES, **ARTICLES}.items()}

def window(src, anchor, n):
    t = TXT[src]; i = t.index(anchor)
    a = max(0, i - 160); a = t.rfind('. ', 0, i) + 2 if t.rfind('. ', a, i) != -1 else a
    b = min(len(t), i + len(anchor) + n); j = t.find('. ', b); b = j + 1 if j != -1 and j - b < 300 else b
    return ('…' if a > 0 else '') + t[a:b].strip() + ('…' if b < len(t) else '')

def paragraph(art, sentence):
    for p in [p for p in ART[art].split('\n\n') if p.strip()]:
        if norm(sentence) in norm(p): return re.sub(r'thumb\|(?:[^|\[\]]*\|)*\[\[[^\]]*\]\]\s*', '', norm(p)).strip()
    return norm(sentence)

def lead(art, start):
    t = norm(ART[art].split('\n==')[0]).replace('&nbsp;', ' '); i = t.index(start)
    return t[i:].strip()

CASES = copy.deepcopy(cases.CASES)
C = {c['id']: c for c in CASES}
TYPE = {'SR-W1': 'sentence', 'SR-W2': 'sentence', 'SR-W3': 'sentence', 'SR-W4-6': 'sentence group', 'SR-W7-8': 'heading with lists',
        'TH-1': 'sentence', 'TH-2': 'sentence', 'IW-1': 'sentence', 'EB-1': 'sentence', 'AC-1': 'placement'}
for c in CASES: c['type'] = TYPE[c['id']]

# the session's readings, brought to the v1.1 draft after round 01
r = C['SR-W1']['reading']
r['support'] = 'partially supported: thirteen by Krabbe (article-internal); twelve by no source the article cites (the article\'s history shows the hedge entered from an unsourced footnote, "Sometimes listed as twelve.", folded into the text on 23 December 2025)'
r['status'] = 'source fidelity: partial; operative retention: partial (the act survives as "identified", its exhaustiveness does not)'
r = C['SR-W2']['reading']
r['deltas'][0] = r['deltas'][0] + ' The bounded claim is entailed by the unbounded one, so the qualifier weakens the claim and falsifies nothing: a loss of scope, recorded as such.'
r['deltas'] = [d.replace('Composition and division: "in ancient Greece" composes', 'Ambiguity of combination: "in ancient Greece" attaches') for d in r['deltas']]
r['deltas'].append('Two senses of "in excess of deduction", kept apart: in intension the definition adds conditions to necessity, so it defines a narrower class than the valid arguments; in scope the undertaking includes asking, answering, sustaining an account and solving by division. The gloss loses both.')
r['status'] = 'source fidelity: the gloss is the field\'s convention, uncited at the sentence; primary-text adequacy of "deduction" as a translation: contested (round 01: a translation can name the ancient category while its translator marks the distance from the modern one, against: the sentence carries the term without the caveat and the gloss relocates the undertaking); operative retention: lost (the undertaking defined at 183a37–b1)'
r = C['SR-W7-8']['reading']
r['deltas'][0] = 'The sub-headings keep Aristotle\'s criterion and assert an equivalence beside it ("Fallacies in the language or formal fallacies", "Fallacies not in the language or informal fallacies"); the "or" makes a later taxonomy interchangeable with the criterion, and the section\'s first sentence states only the later one'
r['deltas'][1] = r['deltas'][1] + '. The modern definition comes from the article\'s own link: the article "Affirming the consequent" (rev. 1375717267) calls it "a formal fallacy (or an invalid form of argument)"'
r['status'] = 'source fidelity: partial (the lists are Krabbe\'s; the equivalence and the narrowing are unsupported); operative retention: the criterion survives in the sub-headings, beside an unsupported equivalence'
r = C['TH-1']['reading']
r['deltas'].insert(1, '"the Aristotelian treatment" becomes "Aristotle\'s treatment": a school made a person, unresolved, since the 1911 phrase may mean either')
r = C['AC-1']['reading']
r['deltas'] = ['The lead carries identity, appointments, prizes and activities (she taught, wrote, translated) and none of her distinctive operations, by the criterion used here: an operation is a stated method, argument or result, with its object. Her account of desire and her method of translation first appear in the Works section.']

# two placement controls, added by round 01 and pinned
CASES.append(dict(id='TU-1', art='TU', type='placement', locus='lead, paragraph 1', cited='refs not fetched', w=None, windows=[],
    reading=dict(innocent='', support='placement only', spans=[], paraphrase='', deltas=['The lead states an operation with its object beside an honorific: "He formalised the concepts of algorithm and computation with the Turing machine" beside "widely regarded as the father of theoretical computer science".'],
                 omega='formalises (algorithm, computation; the Turing machine)', attributization='no: the operation is stated as an act in the lead', lam=1, status='placement observation', alternatives=[], correction='')))
CASES.append(dict(id='CU-1', art='CU', type='placement', locus='lead, paragraph 1', cited='refs not fetched', w=None, windows=[],
    reading=dict(innocent='', support='placement only', spans=[], paraphrase='', deltas=['A credential sentence carries its operation: the 1911 prize "[for] the discovery of the elements radium and polonium, by the isolation of radium and the study of the nature and compounds of this remarkable element".'],
                 omega='discovers, isolates, studies (radium, polonium)', attributization='no: the operation is carried inside the credential', lam=1, status='placement observation', alternatives=[], correction='')))

LEADS = {'AC': 'Anne Patricia Carson', 'TU': 'Alan Mathison Turing', 'CU': 'Maria Salomea'}

# ---------------- MESSAGE 1 ----------------
M = []; m = M.append
m('EA-WIKI-OPEN-01 · ASSEMBLY ROUND 02 · MESSAGE 1 OF 3 · THE BLIND READING')
m('')
m('BEFORE ANYTHING ELSE. This message is meant to be read in a fresh conversation that holds nothing else from this project: no drafts, no papers, no other message of this test. The reader\'s first line states its model name and version as it knows them, and whether the conversation holds anything other than this message. Messages 2 and 3 follow only after this reply is saved.')
m('')
m('ROLE. The reader is one of several independent readers, each from a different model family, asked to run one step of a published procedure on twelve cases and to report in a fixed format. The reader works only from the materials below. Where the materials do not settle a question, the reader says so and marks it unresolved; a guess presented as a finding is the one failure this test exists to catch. The reader quotes every span it relies on verbatim from the materials, since the replies are checked by code against the saved texts, and a quotation that does not occur in its source is recorded as a breach. The reader runs nothing and reports no check it did not make.')
m('')
m('THE PROCEDURE (EA-WIKI-OPEN-01, "Opening the Encyclopedia", step S3 and the fields it feeds). The unit is a sentence of a Wikipedia article at a pinned revision, read against its cited source. Some cases are a sentence group, a heading with the lists under it (the heading classifies every item under it), or a placement case (where the reader records only what a passage carries and where in the article the subject\'s own operations first appear).')
m('')
m('Three measures are kept apart, and the reader names which one each finding belongs to; no single word such as "damage" stands for all three.')
m('- SOURCE FIDELITY: does the sentence say what its source says?')
m('- PRIMARY-TEXT ADEQUACY: where the source is itself a reading (a translation, a gloss, a secondary account), does that reading hold against the primary text supplied?')
m('- OPERATIVE RETENTION: does the act the source reports (a count, a division, a denial, a method, an argument) survive in the sentence with its relations (scope, distinctions, evidence, consequences), and do those relations keep the authority to revise the description?')
m('')
m('The rules, in this order:')
m('0. THE INNOCENT READING. Before any finding, the reader writes the strongest case that the sentence is faithful and adequately sourced, built first from the sources the article itself cites anywhere, then from the cited source. A finding against the sentence states what in the sources the innocent reading cannot accommodate; where nothing does, the sentence is supported. Wikipedia\'s No original research policy permits "Describing the information from cited material in one\'s own words while retaining the substance (i.e., not introducing ideas or arguments absent from the source)" and "Faithfully translating sourced material."')
m('1. UNCITED SENTENCES are read against the sources the article cites elsewhere; support found there is recorded as article-internal, never as a citation at the sentence.')
m('2. A GLOSS OR TRANSLATION in a secondary source is a reading. Where it is all that supports the sentence\'s wording, the reader records it as the source of the wording and tests the wording against the primary text\'s own terms and definitions, under primary-text adequacy.')
m('3. A PHRASE THAT ATTACHES TWO WAYS is divided: the reader states each reading and reads each against the source.')
m('4. ENTAILMENT. A claim that the source\'s claim entails (a narrower or weaker version of it) is not unsupported; the narrowing is recorded as a loss of scope.')
m('')
m('For each case the reader then records: (a) SUPPORT, classes non-exclusive: supported; partially supported; qualifier added (list the tokens); interpretation beyond descriptive paraphrase; unsupported; unresolved. (b) THE PARAPHRASE COMPARISON: the defensible descriptive paraphrase of the source lines, set beside the sentence, each change quoted on both sides. (c) ATTRIBUTIZATION: does the source perform an act that the sentence restates as a property or attribute (a credential, a priority, a category membership)? "No" is a valid and important answer. (d) RETAINED AUTHORITY: retained, lost, mixed or unknown, with the evidence and the revision of the sentence the operation could require. (e) LAMBDA, per finding: where the qualification, objection or source of the wording sits relative to the sentence: 1 beside it; 2 below it in the same article; 3 in another article; 4 in a cited source; 5 outside the supplied sources; null where none is identified. (f) ALTERNATIVE READINGS. (g) CORRECTION PATHWAY. (h) CONFIDENCE, with what limits it.')
m('')
m('OUTPUT. The first line as asked above; then one JSON array, one object per case, in a code block, nothing else:')
m('{"case": "...", "case_type": "sentence | sentence group | heading with lists | placement", "innocent_reading": "...", "innocent_reading_fails_at": "... or null", "support": ["..."], "support_source": ["at the sentence" | "elsewhere in the article" | "none"], "paraphrase": "...", "deltas": [{"sentence_says": "...", "source_says": "...", "kind": "scope | qualifier added | idea introduced | term changed | omission | hedge | date omitted | equivalence asserted | ambiguity of combination | none", "measure": "source fidelity | primary-text adequacy | operative retention", "lambda": 1-5 or null}], "omega": "... or null", "attribute": "... or null", "attributization": "yes | partial | no", "attributization_reason": "...", "retained_authority": {"value": "retained | lost | mixed | unknown", "evidence": "...", "revision_required": "..."}, "surviving_relations": ["..."], "lost_relations": ["..."], "alternatives": ["..."], "correction_pathway": "...", "confidence": "high | medium | low", "confidence_note": "...", "windows_too_narrow": "... or null", "spans": [{"source": "SOURCE ID or ARTICLE", "quote": "verbatim"}]}')
m('')
m('THE CASES. The source windows were chosen by the session that prepared this test; the reader says where a window is too narrow to decide the case, and what is missing. For placement cases, "ARTICLE" is the source ID for quotations from the passage given.')
for c in CASES:
    a = ARTICLES[c['art']]
    m('')
    m(f'=== CASE {c["id"]} · {c["type"].upper()} · Wikipedia, "{a["title"]}", revision {a["rev"]}, {c["locus"]} ===')
    if c['type'] == 'placement':
        m(f'THE LEAD, WHOLE: {lead(c["art"], LEADS[c["art"]])}')
        m('SOURCE MATERIAL: none supplied. The reader records the case at placement only: whether the lead states any operation of the subject (a stated method, argument or result, with its object), and quotes it.')
        continue
    m(f'SENTENCE: {c.get("w_display", c["w"])}')
    if c.get('list_display'): m(f'THE LISTS IT INTRODUCES: {c["list_display"]}')
    m(f'HOW IT IS CITED: {c["cited"]}')
    if c['art'] != 'SR': m(f'ITS PARAGRAPH: {paragraph(c["art"], c["w"])}')
    m('SOURCE MATERIAL:')
    for s, anc, n in c['windows']:
        m(f'  [{s}] {SOURCES[s]["cite"]}')
        m(f'  "{window(s, anc, n)}"')
m('')
m('THE FULL SPECIMEN ARTICLE ("Sophistical Refutations", revision 1361634710, wikitext rendered to plain text, references removed; the second list is the {{ordered list}} template, given as in the wikitext):')
sr = ART['SR'].split('==References==')[0].strip().replace('(Σοφιστικοὶ Ἔλεγχοι; )', '(Greek Σοφιστικοὶ Ἔλεγχοι; Latin De Sophisticis Elenchis)')
sr = sr.replace(':Fallacies not in the language or informal fallacies (extra dictionem):', ':Fallacies not in the language or informal fallacies (extra dictionem):\n# 7 Accident\n# 8 Secundum quid\n# 9 Irrelevant conclusion\n# 10 Petitio principii\n# 11 False cause\n# 12 Affirming the consequent\n# 13 Fallacy of many questions')
m(sr)
m('')
m('A NOTE ON THE GREEK (case SR-W2). The Greek of SE 34 and of the lines on division and combination is given as seated in the archive\'s deposit #1574, with that deposit\'s working translation of SE 34; the Pickard-Cambridge translation the article cites is given beside it. The reader may use either and says which.')
M1 = '\n'.join(M)

# ---------------- MESSAGE 2 ----------------
M = []; m = M.append
m('EA-WIKI-OPEN-01 · ASSEMBLY ROUND 02 · MESSAGE 2 OF 3 · THE SESSION\'S READINGS AND THE ATTACK')
m('')
m('This message follows the reader\'s own Message 1 reply, which has been saved. The reader now receives the readings made in the procedure\'s own session (TACHYON, Claude, the same model family as the procedure\'s built reader, so its agreement with that reader proves nothing), the record of how one finding moved, and for case SR-W2 the archive sources the procedure admits at its step S7. The reader\'s task is to break the procedure where it breaks. Where the reader still holds a Message 1 reading it says so, with the span that decides it; changing a reading because the session\'s differs, without new evidence, is a failure of the test.')
m('')
m('THE SESSION\'S READINGS, by case:')
for c in CASES:
    r = c['reading']
    m('')
    m(f'--- {c["id"]} ({c["type"]}) ---')
    if r['innocent']: m(f'innocent: {r["innocent"]}')
    m(f'support: {r["support"]}')
    if r['paraphrase']: m(f'paraphrase: {r["paraphrase"]}')
    for d in r['deltas']: m(f'delta: {d}')
    m(f'omega: {r["omega"]}')
    m(f'attributization: {r["attributization"]}')
    m(f'lambda: {r["lam"]}; status: {r["status"]}')
    for al in r['alternatives']: m(f'alternative: {al}')
    if r['correction']: m(f'correction pathway: {r["correction"]}')
m('')
m('HOW ONE FINDING MOVED (SR-W2), recorded in order. (1) The deposited paper (v1.0) classed the sentence unsound because "the subject of deductive reasoning" changed the scope of the cited lines. (2) Opening the article whole, the session\'s first pass took the article\'s own sources (Smith: "the deduction ( sullogismos )"; Krabbe: "deductive reasoning (sullogismos)") as support for the gloss and withdrew the finding. (3) The operator rejected that: "deduction" and "deductive reasoning" are interpretive translations that relocate the interpretive move to translation; Aristotle defines syllogizing in excess of deduction; dividing and combining is the more accurate account of the undertaking. The session checked these against the sources and adopted them (SE 1\'s definition; Krabbe\'s and Smith\'s statements of what the definition requires; SE 17, 18, 20, 23 on division and combination). (4) A reader in round 01 argued the other way on one point: a translation can name the ancient category while its translator marks the distance from the modern one, so Smith\'s caveat does not by itself make "deduction" unfaithful; and the additional defining conditions make the class narrower, so "in excess" must say in what sense. The session kept the finding on the scope of the undertaking (183a37–b1), and records the fidelity of the translation as such as contested.')
m('')
m('THE ARCHIVE\'S ADMITTED SOURCE FOR SR-W2 (step S7). From #1603, "Nothing Before Us: Socrates and the Ending of the Sophistical Refutations", Appendix P, prohibition P1, verbatim:')
p1 = open('/home/claude/alexanarch/data/texts/AXN-0693-text.md', encoding='utf-8').read()
i = p1.index('**P1. The scope is this undertaking.**'); j = p1.index('**P2.', i)
m(norm(p1[i:j]).replace('**', ''))
m('And from #1574 §3, verbatim:')
t74 = open('/home/claude/alexanarch/data/texts/AXN-0666-text.md', encoding='utf-8').read()
i = t74.index('The immediate undertaking is not presented here merely'); j = t74.index('without being coextensive with every feature of the undertaking.', i) + len('without being coextensive with every feature of the undertaking.')
m(norm(t74[i:j]))
m('')
m('THE TASKS.')
m('B1. AGREEMENT. For each case, field by field (support, deltas, attributization, retained authority, lambda), the reader states agree, disagree or partly, the measure the field belongs to, and the span that decides it; and whether it holds its own Message 1 reading.')
m('B2. FALSE POSITIVES. Where does the session find a loss that is not there? The positive controls (SR-W4-6, IW-1, EB-1, TU-1, CU-1) are in the set to catch this.')
m('B3. FALSE NEGATIVES. What does the session miss that the materials show?')
m('B4. WHO AUDITS THE AUDITOR. For SR-W2: does admitting #1603 P1 change the verdict by evidence (a locus in the Greek that the field\'s gloss cannot accommodate) or by the archive\'s standing to rule its own reading? Answer from the Greek and the two translations. Then state what the opened sentence should say so that a reader who holds the field\'s reading and a reader who holds the archive\'s can both check it.')
m('B5. THE RULES THEMSELVES. Rule 2 (a gloss is a reading, tested against the primary text) and rule 4 (entailment) decided findings in Message 1. Is each rule right? Where would it decide a case wrongly?')
m('B6. THE FIVE-PART ACCOUNT. For SR-W2 and SR-W7-8: (1) source support; (2) what the sentence adds, changes or omits; (3) the strongest alternative reading and its basis; (4) the status of each finding: verified (checkable by code), inferred, contested, or unresolved; (5) what evidence would revise it. At most two sentences each.')
m('B7. BREAK IT. Up to five sentences from real English Wikipedia articles, each with title and a revision id the reader can state with confidence, or marked "revision to be pinned", on which the procedure would most likely err: (i) a legitimate standard gloss the procedure would call unsound; (ii) an archive admission that would substitute its own ontology without evidence; (iii) a real loss the classes cannot express; (iv) an entity lead whose operation survives; (v) any other trap.')
m('B8. THE TEST OF P1. P1 predicts attributization with loss of operative authority at a higher rate on entity pages than on work and method pages. The revised design matches named operations across an entity page and a work or method page, with each operation\'s source unit identified before scoring; adds a within-page arm (lead against body); measures access cost from the lead separately; and blinds readers to the expected verdict, the archive, the operator\'s rulings and the page type, asking each reader to guess the page type afterwards. Name the largest remaining threat and the change that removes it.')
m('')
m('OUTPUT. One JSON object in a code block: {"agreement": [{"case": "...", "field": "...", "measure": "...", "verdict": "agree | disagree | partly", "holds_message_1": true | false, "decisive_span": {"source": "...", "quote": "..."}, "note": "..."}], "false_positives": [...], "false_negatives": [...], "auditor": {"verdict_changed_by": "evidence | standing | both | neither", "locus": "...", "opened_sentence": "..."}, "rules": {"rule_2": "...", "rule_4": "..."}, "five_part": {"SR-W2": {...}, "SR-W7-8": {...}}, "break_cases": [{"title": "...", "revision": "...", "sentence": "...", "trap": "i | ii | iii | iv | v", "why": "..."}], "p1_threat": {"threat": "...", "remedy": "..."}}')
M2 = '\n'.join(M)

M3 = '\n'.join([
 'EA-WIKI-OPEN-01 · ASSEMBLY ROUND 02 · MESSAGE 3 OF 3 · THE BREAK CASES',
 '',
 'This message follows the reader\'s Message 2 reply, which has been saved. The session has pinned the break cases proposed by all readers, with their cited sources, below, in Message 1\'s format and under Message 1\'s rules. The reader runs Message 1\'s procedure on each, blind to every other reader\'s reading, and returns the Message 1 JSON.',
 '',
 '[The session inserts the pinned cases here.]'])

files = {'message-1-blind-reading.txt': M1, 'message-2-readings-and-attack.txt': M2, 'message-3-break-cases-TEMPLATE.txt': M3}
for fn, txt in files.items(): (OUT / fn).write_text(txt + '\n', encoding='utf-8')
H = {fn: hashlib.sha256((OUT / fn).read_bytes()).hexdigest() for fn in files}
man = ['# Assembly round 02: for the session (never sent to a reader)', '',
 'Send each message as the whole contents of its file, in a fresh conversation per reader, with nothing else attached. Message 1 first. Save the reply verbatim. Then Message 2 in the same conversation; save that reply. Message 3 only after the session has pinned the break cases.', '',
 'Files (SHA-256):']
man += [f'- `{fn}`: `{h}`' for fn, h in H.items()]
man += ['', 'Pinned materials (SHA-256 of the file as fetched):']
man += [f'- Wikipedia, "{v["title"]}", revision {v["rev"]}: `{SHA[k]}`' for k, v in ARTICLES.items()]
man += [f'- {k}: {v["cite"]}: `{SHA[k]}`' for k, v in SOURCES.items()]
man += ['', 'Collation: every quoted span checked by code against these materials; a miss is a breach, recorded. Tables by case, field, measure and family; a reader\'s self-identification recorded as given, beside the family it was run in. Break cases that survive pinning are new, so they may be held out under §5.4.']
(OUT / 'MANIFEST-session-only.md').write_text('\n'.join(man) + '\n', encoding='utf-8')
json.dump([{k: v for k, v in c.items()} for c in CASES], open(OUT / 'cases-round02.json', 'w'), ensure_ascii=False, indent=1)
for fn in files: print(fn, len(files[fn].encode()), 'bytes')
# leak checks: nothing of the session's readings in message 1
for c in CASES:
    for d in c['reading']['deltas']:
        frag = d[:60]
        if frag in M1: print('LEAK into message 1:', c['id'], frag)
for bad in ['TACHYON', 'innocent reading fails at its own sources', 'v1.1', '#1603', 'P1.']:
    if bad in M1: print('M1 contains:', bad)
