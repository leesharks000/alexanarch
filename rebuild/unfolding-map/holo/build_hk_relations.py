#!/usr/bin/env python3
"""build_hk_relations.py — the operator of EA-HK-REVFIRST-02, the relations hologram.

Built to EA-HK-FRAME-01 (#1753) at the grain of the relation. Nothing the registry or a
data file holds is typed here: arrows are read from the framework kernel (#1755), rows from
the Matthew ledger, identifiers and hashes from the archive's lookup. What is the author's
and the map's (standings, the rule of each standing, the layers, the lines of research, the
rival) is held below as data.

Usage: build_hk_relations.py REPO PAPER_MD NOTEBOOK_MD OUTDIR
The sealed key, its addendum and the scorers are never read by this builder.
"""
import sys, json, re, hashlib, collections, datetime, os
import yaml

REPO, PAPER, NOTEBOOK, OUT = sys.argv[1:5]
os.makedirs(OUT, exist_ok=True)
sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
dep = json.load(open(f'{REPO}/data/api/lookup/deposits.json'))['deposits']
def rec(n):
    d = dep[str(n)]
    return dict(record=f'rec:{n}', axn=d['axn'], record_sha256=d['sha256'], date=d['date'],
                title=d['title'], url=d['record'])

FW = yaml.safe_load(open(f'{REPO}/files/AXN-0C5F/kernel/00-kernel.yaml'))
ARROWS = FW['unfoldings']['arrows']
LEDGER_P = f'{REPO}/rebuild/unfolding-map/map/rev-matthew-ledger.json'
LEDGER = json.load(open(LEDGER_P))['rows']
paper = open(PAPER, encoding='utf-8').read()
paras = [p for p in re.split(r'\n\s*\n', paper)]

VERSION = '1.0'
TODAY = datetime.date.today().isoformat()

# ---- standings: the author's and the map's --------------------------------------------
STANDINGS = dict([
 ('produced-blind', dict(name='produced blind under a sealed key',
   licenses='that the rule and the place are jointly sufficient for the passage, for these readers and this pack',
   withholds='the order of the two books; sufficiency for readers who do not know the target')),
 ('run', dict(name='run: an executable derivation',
   licenses='typed seed elements, declared rules, emissions matched verse by verse, coverage counted, residue displayed',
   withholds='direction, without a census of the alternatives')),
 ('sealed-held', dict(name='written down before counting, and held',
   licenses='that the pairing was not found by looking for it',
   withholds='that the pairing is unique to the two books, unless counted so')),
 ('sealed-failed', dict(name='written down before counting, and failed as written',
   licenses='nothing for the relation as written; the count that replaced it stands at its own standing',
   withholds='everything the written line claimed')),
 ('counted', dict(name='counted over the whole New Testament',
   licenses='the distribution stated', withholds='a mechanism')),
 ('engine', dict(name='derived by the engine and passing its controls',
   licenses='that a declared operator reaches the target from the source and no control source does as well',
   withholds='that the operator is the one a writer used')),
 ('worked', dict(name='worked to derivation grade',
   licenses='seed, rules and emissions, with the shared-source alternative stated', withholds='coverage')),
 ('mapped', dict(name='mapped with a grade',
   licenses='a letter set against an epistle with its class and residue', withholds='a derivation')),
 ('read', dict(name='read, and checked for shared lemmas in a tagged text',
   licenses='that the two places hold the lemmas stated', withholds='selection effects: the row was found by reading')),
 ('drawn', dict(name='drawn and not run', licenses='an arrow to be tested', withholds='everything else')),
 ('observed', dict(name='observed, awaiting a census', licenses='a lexical observation', withholds='a derivation')),
 ('withheld', dict(name='withheld by a date held under the chronology under examination',
   licenses='markedness', withholds='the arrow')),
 ('named', dict(name='named at the founding grain', licenses='that the programme names the arrow', withholds='any seed inventory')),
 ('unresolved', dict(name='unresolved', licenses='nothing', withholds='everything')),
 ('planned', dict(name='planned', licenses='nothing; a line of research', withholds='everything')),
 ('failed', dict(name='tested and failed', licenses='that the stated mapping does not hold as stated', withholds='the mapping')),
])
ORDER = list(STANDINGS)

def ledger_standing(st):
    st = str(st)
    if 'held under seal' in st: return 'produced-blind'
    if re.search(r'failed as written|J\d+ failed', st): return 'sealed-failed'
    if re.search(r'\b[JKNPQRT]\d+[a-z]? held|sealed N\d|S\d held|K1 held', st): return 'sealed-held'
    if st.startswith('engine'): return 'engine'
    if st.startswith('counted') or 'counted:' in st: return 'counted'
    return 'read'

BOOKS = ['Matthew','Mark','Luke','John','Acts','Romans','1 Corinthians','2 Corinthians','Galatians','Ephesians',
 'Philippians','Colossians','1 Thessalonians','2 Thessalonians','1 Timothy','2 Timothy','Titus','Philemon','Hebrews',
 'James','1 Peter','2 Peter','1 John','2 John','3 John','Jude']

# ---- relations --------------------------------------------------------------------------
REL = []
fw_rec = rec(1755)
for a in ARROWS:
    REL.append(dict(id='rel:'+a['id'].replace(':','-'), family='epistle' if a['id'].startswith(('letter','transform','article')) else 'founding-or-saying',
        source=a.get('seed'), targets=a.get('targets', []), books=a.get('books', []),
        operation=a.get('operations', []), cls=a.get('cls'), grade=a.get('grade'),
        standing=a['state'], stated_limit=a.get('stated_limit'),
        pointer=dict(kind='record', via='the framework kernel (#1755), unfoldings.arrows', arrow=a['id'],
                     records=[rec(n) for n in a.get('records', []) if str(n) in dep],
                     kernel_sha256=sha(f'{REPO}/files/AXN-0C5F/kernel/00-kernel.yaml'))))

SRC = sys.argv[5] if len(sys.argv) > 5 else None
def _ranges(ref):
    out = []
    for part in str(ref).split(';'):
        m = re.match(r'\s*(\d+):(\d+)(?:\s*[-–]\s*(?:(\d+):)?(\d+))?', part)
        if m:
            c, a = int(m.group(1)), int(m.group(2))
            if m.group(3): out += [(c, a, 999), (int(m.group(3)), 1, int(m.group(4)))]
            else: out.append((c, a, int(m.group(4) or a)))
    return out
def _blocks():
    """the paper's source split at its numbered paragraphs; each block with the loci it quotes or names"""
    src = open(SRC, encoding='utf-8').read() if SRC else paper
    parts = re.split(r'(?m)^(?=(?:[IVX]+|P|0)\.\d+[a-z]?\. )', src)
    out = []
    for b in parts:
        m = re.match(r'((?:[IVX]+|P|0)\.\d+[a-z]?)\. ', b)
        if not m: continue
        loci = {'Rev': set(), 'Matt': set()}
        for bk, c, v in re.findall(r'⟦(Rev|Matt) (\d+):(\d+)', b): loci[bk].add((int(c), int(v)))
        for name, bk in (('Revelation', 'Rev'), ('Matthew', 'Matt')):
            for c, v in re.findall(name + r' (\d+):(\d+)', b): loci[bk].add((int(c), int(v)))
        out.append((m.group(1), loci))
    return out
BLOCKS = _blocks()
def find_in_paper(rev, matt):
    """the numbered paragraph of the paper that quotes or names both places: a pointer, never a restatement"""
    hit = lambda loci, rs: any(c == cc and a <= v <= z for (c, v) in loci for (cc, a, z) in rs)
    rr, mr = _ranges(rev), _ranges(matt)
    secs = [s for s, loci in BLOCKS if hit(loci['Rev'], rr) and hit(loci['Matt'], mr)]
    return ', '.join(secs[:4]) if secs else None

paper_sha = sha(PAPER)
PAPER_REC = rec(1812)
assert PAPER_REC['record_sha256'] == paper_sha, 'the paper text is not the record at its registered hash'
for i, r in enumerate(LEDGER, 1):
    sec = find_in_paper(r['rev'], r['matt'])
    REL.append(dict(id=f'rel:mt-{i:02d}', family='matthew', source='Rev ' + str(r['rev']), targets=['Matt ' + str(r['matt'])],
        books=['Matthew'], operation=[str(r['move'])], strand=r.get('strand'),
        rev_relation=r.get('rev_relation'), matt_relation=r.get('matt_relation'),
        lemmas=r.get('lemmas', []), standing=ledger_standing(r['standing']), standing_as_recorded=r['standing'],
        pointer=dict(kind='data file', file='rebuild/unfolding-map/map/rev-matthew-ledger.json', row=i,
                     file_sha256=sha(LEDGER_P), checked=r.get('source'),
                     paper=dict(PAPER_REC, section=sec) if sec else
                           dict(record=PAPER_REC['record'], section=None, note='in the ledger; not located in the paper by the places it quotes'))))

# ---- layers (P3): the places where Philo or scripture stands under a place of Revelation
LAYERS = [
 ('Rev 21-22', 'Philo, Somn. 2.246-254', 'Jerusalem as vision of peace, the city in the soul', ['Matt 5:8-9', 'Matt 5:14'], 'sealed-held', 'M1'),
 ('Rev 3:17-18', 'Philo, blind wealth and seeing wealth (17 sections)', 'wealth that is blind', ['Matt 6:19-24', 'Matt 19:21'], 'sealed-held', 'M2'),
 ('Rev 22:12-13', 'Philo, Her. 141-146', 'beginning and end; equality by number and by proportion', ['Matt 20:1-16'], 'produced-blind', 'M3; Round 3'),
 ('Rev 12:1', 'Philo, Somn. 2.113', 'the twelfth star', ['Matt 2:2'], 'sealed-held', 'M4'),
 ('Rev 12:1-5', 'Philo, Fug. 109; Cher. 43-50', 'the mother of the Logos (weakest join)', ['Matt 1:18-23'], 'sealed-held', 'M5'),
 ('Rev 13:14-17; 7:3', 'Philo, Plant. 18', 'the soul as coin under the seal of God', ['Matt 22:19-21'], 'sealed-held', 'M6'),
 ('Rev 10:5-6', 'Philo, Spec. 2.2-5; Leg. 3.203-206', 'two tiers of oath', ['Matt 5:33-37'], 'sealed-held', 'M9'),
 ('Rev 3:19', 'Philo, the proverb of reproof', 'expected join of Philo to the Septuagint', [], 'sealed-failed', 'M7'),
 ('Rev 2:17', 'Philo, Leg. 3.162-176; Deut 8:3', 'the manna as the word', ['Matt 4:4'], 'sealed-held', 'N1'),
 ('Rev 1:16; 2:12', 'Philo, Her. 130-140, 225', 'the Logos as cutter', ['Matt 10:34-35'], 'sealed-held', 'N2'),
 ('Rev 2:17; 19:12-13', 'Philo, Mut. 121', 'the name', ['Matt 1:21'], 'sealed-held', 'N5'),
 ('Rev 3:14; 21:7', 'Philo, Conf. 145-147', 'sons of God', ['Matt 5:8-9'], 'sealed-held', 'N7'),
 ('Rev 1:12-20; 2:1', 'Philo, Her. 215-225', 'the seventh in the midst of the lampstand', [], 'worked', '#1758'),
]
midst = rec(1758)
for k, (rv, ly, what, mt, st, lab) in enumerate(LAYERS, 1):
    REL.append(dict(id=f'rel:layer-{k:02d}', family='layer', source=ly, via=rv, targets=mt, books=['Matthew'] if mt else [],
        operation=['P3: the layer under the place stands open; a compressed member may be restored'], what=what,
        standing=st, label=lab,
        pointer=dict(kind='record+working file', records=[midst, PAPER_REC], notebook_sections='2AV, 2AW, 2AX',
                     paper_sections='III.7, V.3a, V.5a-d, VI.6a-b, VII.3, VII.10, XIII.1a, XIV.5a')))

PLANNED = [
 ('rel:plan-luke', 'Revelation', ['Luke'], 'no procedure yet; rows shared with Matthew reach 40 of 184 verses of the double tradition', 'planned'),
 ('rel:plan-mark', 'Revelation', ['Mark'], 'no procedure; the procedure leaves Mark in place, and reaches 51 of the 458 verses Matthew shares with it', 'planned'),
 ('rel:plan-john', 'Revelation', ['John'], 'order not found; the seven plagues reversed into the signs, untested as a pack', 'planned'),
 ('rel:plan-acts', 'Revelation', ['Acts'], 'a control so far: Acts 12 holds more of the dragon\'s custody than any Gospel passage', 'planned'),
 ('rel:plan-seven-in-seven', 'Rev 1-3', ['Hebrews', 'Jude', 'Romans', '1 Corinthians', '2 Corinthians', 'Galatians', 'Ephesians', 'Philippians', 'Colossians', '1 Thessalonians', '2 Thessalonians'],
  'seven within seven: the Pauline seven-church formation, and Paul as one of seven epistolary positions', 'planned'),
 ('rel:fail-four', 'Rev 4:6-8; 6:1-8', ['Matthew', 'Mark', 'Luke', 'John'], 'the four creatures and four riders assigned to the four Gospels: within chance', 'failed'),
 ('rel:fail-order', 'Revelation, in its order', ['Matthew', 'Mark', 'Luke', 'John'], 'the source\'s sequence in a Gospel\'s sequence: not found, three ways', 'failed'),
 ('rel:fail-seatmap', 'Revelation', ['Matthew'], 'one seat-map over a whole Gospel: five predictions failed', 'failed'),
 ('rel:fail-plagues', 'Rev 8-9; 16', ['Matthew'], 'the plagues opposed in Matthew\'s miracles (sealed S1): a tie with Mark\'s material', 'sealed-failed'),
 ('rel:fail-philo-free', 'Philo, with no place of Revelation between', ['Matthew'], 'cannot tell Matthew from Mark (ratio 1.30 against 1.22); kept as the control for P3', 'failed'),
]
for id_, src, books, note, st in PLANNED:
    REL.append(dict(id=id_, family='planned-or-failed', source=src, targets=[], books=books, operation=[], note=note, standing=st,
        pointer=dict(kind='working file', notebook='The Unfolding Map', note='not a record; hosted beside this record')))

# ---- by book ------------------------------------------------------------------------------
def best(sts):
    rank = {s: i for i, s in enumerate(['produced-blind','run','sealed-held','counted','engine','worked','mapped','read','drawn','observed','withheld','named','unresolved','planned','failed','sealed-failed'])}
    return min(sts, key=lambda s: rank[s])
by_book = {}
for b in BOOKS:
    rs = [r for r in REL if b in r.get('books', [])]
    by_book[b] = dict(relations=len(rs), by_standing=dict(collections.Counter(r['standing'] for r in rs)),
                      strongest=best([r['standing'] for r in rs]) if rs else None)
no_arrow = [b for b, v in by_book.items() if v['relations'] == 0]
BELOW = {'planned', 'failed', 'sealed-failed', 'named', 'unresolved', None}
reached = [b for b, v in by_book.items() if v['strongest'] not in BELOW]
only_named_or_planned = [b for b, v in by_book.items() if v['relations'] and v['strongest'] in BELOW]
mt = [r for r in REL if r['family'] == 'matthew']
mt_n = lambda s: sum(1 for r in mt if r['standing'] == s)
counts = dict(relations=len(REL), by_family=dict(collections.Counter(r['family'] for r in REL)),
              by_standing={s: sum(1 for r in REL if r['standing'] == s) for s in ORDER if any(r['standing'] == s for r in REL)},
              matthew_rows=len(LEDGER), matthew_rows_stated_in_paper=sum(1 for r in REL if r['family'] == 'matthew' and r['pointer']['paper'].get('section')),
              matthew_by_standing={s: mt_n(s) for s in ORDER if mt_n(s)}, layers=sum(1 for r in REL if r['family'] == 'layer'),
              matthew_verses_reached='178 of 1,067', books_reached_above_named=reached, books_named_or_planned_only=only_named_or_planned, books_without=no_arrow)

# ---- the transform, compressed ---------------------------------------------------------------
TRANSFORM = dict(
 epistles=dict(operation='letter to epistle: the speaker commissions writing to seven messengers; each letter is unfolded as an epistle',
   classes=FW['unfoldings']['classes'], james_rules=[o for a in ARROWS if a['id'] == 'letter:smyrna' for o in a['operations']]),
 matthew=dict(name='T_Μ v0.4',
   S='the source held whole; the unit is the relation with its bearer',
   P=['P1 give the speaker a past', 'P2 tell the life in a named land; cite scripture as written',
      'P3 at each place of the source the layers it was made from stand open (scripture; Philo), and a compressed member may be restored; Philo only through a place Revelation holds'],
   M=['M1 keep', 'M2 exchange the patient', 'M3 the costly act done by the adversary, or refused', 'M4 the rider\'s charge taken by the teacher',
      'M5 oppose commerce, image, wealth', 'M6 the faithful\'s trial to the teacher, the seer\'s part to the followers', 'M7 the speaker\'s reproofs said of adversaries'],
   F=['F1 stage', 'F2 enact', 'F3 liken', 'F4 foretell', 'F5 happen'], C='C1-C5, five checks',
   modes_of_inheritance=['kept', 'reworked and passed on', 'dropped by the source and restored in the target (ancestral reactivation)']))

SUMMARY = ("Revelation First (Lee Sharks, #202) holds that the Apocalypse is the generative source of the rest of the New Testament. "
 "This kernel holds every relation the programme has drawn from Revelation to another book, each at its own standing, and the relations it has planned or seen fail. "
 f"It holds {len(REL)} relations. For the epistles: the letters to the seven assemblies set against seven epistles, one of them run to an executable derivation "
 "(Smyrna to James, nine rules), four doctrinal transforms worked to derivation grade, the rest mapped with grades and residue. "
 f"For Matthew: {len(LEDGER)} relations reaching 178 of 1,067 verses under a stated transform (T_Μ v0.4), one passage produced blind from the rule and two verses, "
 f"{mt_n('sealed-held')} pairings written down before they were counted and held, {mt_n('sealed-failed')} that failed as written, {mt_n('counted')} counted, {mt_n('engine')} derived by an engine, {mt_n('read')} read. "
 f"Under Revelation, at {len(LAYERS)} places, a layer of Philo or scripture is recorded: the third parameter of the transform admits it only through a place Revelation holds. "
 f"{len(reached)} of the 26 other books are reached above the founding grain; {len(no_arrow)} have no relation ({', '.join(no_arrow)}). Luke, Mark, John, Acts and the Pauline seven are planned. Four mappings were tested and failed and are kept: the four creatures to the four Gospels, "
 "the source's order in a Gospel's order, one seat-map over a whole Gospel, and Philo taken straight to Matthew. "
 "A standing licenses what it names and nothing above it: a relation read is not a relation counted, and a relation counted is not a derivation. "
 "No relation here decides the order in which the books were written; the argument for order is the framework's (#1735, #1755). "
 "The received account is carried as the rival on the same terms: the Synoptic tradition as the source of Revelation's sayings (Vos 1965; Bauckham 1977), "
 "Mark, a sayings source and special material as the sources of Matthew. Its inverse procedures have not been built and that is its status here.")

kernel = dict(id='EA-HK-REVFIRST-02', version=VERSION, built=TODAY, type='relations hologram, built to EA-HK-FRAME-01 (#1753) at the grain of the relation',
  title='Revelation to the New Testament: The Relations Hologram',
  state='deposited; the record number and AXN of this hologram are assigned at mint and are not written inside it',
  creators=['Dancings, Damascus'],
  contributors=['Crimson Hexagonal Archive', 'Claude (TACHYON; Anthropic)'],
  framework=dict(name='Revelation First', seed=rec(202), hologram=fw_rec, specification=rec(1753)),
  grain='the relation: a place of Revelation, a place of another book, an operation, a standing, a pointer',
  compression_survival_summary=SUMMARY,
  invariants=[
   'REL-1 A relation is a pointer: to a record where one holds it, to a hashed data file or the notebook where none does, and it says which.',
   'REL-2 A standing licenses what it names and nothing above it (01-ontology.yaml, standings).',
   'REL-3 Failures are relations. A mapping tested and failed stays in the kernel at that standing.',
   'REL-4 No relation decides the order of composition. Direction is the framework\'s question (#1735, #1755 rung IV).',
   'REL-5 A layer (Philo, scripture) enters only through a place Revelation holds.',
   'REL-6 FRAGMENT ≠ WHOLE: a relation, a book\'s table or a standing keeps its path to the framework and states what it has not reconstructed.',
   'REL-7 The sealed key is not in the kernel. Blind runs are cited by the hash commitment printed in the paper (#1812, VII.9).'],
  uktp_seed=dict(agents=['a speaker in Revelation', 'seven messengers', 'a writer holding Revelation whole', 'the reader given a rule and a place'],
    operations=['commission', 'unfold a letter as an epistle', 'keep', 'exchange', 'reassign', 'stage', 'enact', 'liken', 'foretell', 'restore from the layer'],
    dependencies=['a relation depends on its two places and its operation', 'a layer depends on the place of Revelation it stands under',
                  'the book table depends on the relations'],
    constraints=['REL-2', 'REL-4', 'REL-5'],
    topology='a fan from one book to twenty-six, each ray a set of relations; under the centre, a second fan from Revelation back to its layers'),
  transform=TRANSFORM, counts=counts, by_book=by_book,
  notebook=dict(name='The Unfolding Map', role='the working notebook of the programme\'s unfoldings; the research record of every relation here',
    hosting='hosted beside this record at /files/EA-HK-REVFIRST-02/notebook/ and replaced as it grows; not ingested into the record\'s canonical text; each replaced copy kept by date',
    current=dict(file=os.path.basename(NOTEBOOK), sha256=sha(NOTEBOOK), words=len(open(NOTEBOOK, encoding='utf-8').read().split()))),
  rival=dict(name='the received account of the relations',
    statement='Where Revelation and another book of the New Testament agree, the other book or the tradition behind it is the source, or both draw on scripture and a common stock.',
    on_each_family={
      'epistle': 'the epistles precede Revelation; the seven letters organize a practice already in place. Status: the missing-ancestor test (#1735) is run against it; the inverse, an epistle compressed to a letter, has not been built as a procedure.',
      'founding-or-saying': 'sayings of Jesus in fixed oral form reach the seer (Vos 1965, as reported); parables worn to sayings in exhortation (Bauckham 1977). An older position ran the other way: prophets\' first-person sayings entered the tradition (Bultmann). Status: the inverse rule, parable to saying, has not been built or run.',
      'matthew': 'Mark, a sayings source and special material. Status: the sayings source is not extant; the procedure here leaves Mark in place and has not been run from any other source of like length as a control.',
      'layer': 'Philo and the New Testament share a milieu. Status: the free test of Philo against Matthew was run and could not tell Matthew from Mark; the clustering of Philo\'s places by treatise has no control yet.'},
    rule='a bar set for the relations is set for the rival (#1753 rule 9); a rival procedure that has never been run carries that as its status'),
  litmus=dict(
    what_must_survive='the fan; the standings and what each licenses; the failures; that no relation decides order; the layer rule',
    forbidden_operation='promoting a relation above its standing: reporting rows read as derivations, or the reach as proof of priority',
    dependency_chain='place of Revelation, operation, place of the target, standing, pointer; and for a layer, layer, place of Revelation, target'),
  acceptance=dict(threshold=0.85, scope_A=['00-kernel.yaml', '01-ontology.yaml'], scope_B_adds=['02-graph.jsonld'],
                  back_projection_v1_0='not run'),
  sources={'framework kernel 00-kernel.yaml': sha(f'{REPO}/files/AXN-0C5F/kernel/00-kernel.yaml'),
           'rev-matthew-ledger.json': sha(LEDGER_P), 'paper (#1812)': paper_sha, 'notebook': sha(NOTEBOOK)})

ontology = dict(id='EA-HK-REVFIRST-02/ontology',
  classes=dict(Book='a book of the New Testament', Place='a locus in a book, by chapter and verse',
    Relation='a pointer: source place, target place, operation, standing, where it is held',
    Rule='an operation of a transform', Layer='a text Revelation was made from, standing under one of its places',
    Record='an archive deposit, by AXN and hash', WorkingFile='a hashed file that is not a record',
    Standing='what has been done to a relation, with what that licenses and withholds'),
  standings=[dict(id=k, **v) for k, v in STANDINGS.items()],
  families=dict(epistle='letters and doctrinal transforms to the epistles', matthew='the ledger of T_Μ',
    layer='Philo or scripture under a place of Revelation, with the place Matthew opens',
    **{'founding-or-saying': 'arrows named at the founding grain, and sayings observed', 'planned-or-failed': 'what is to be tested and what was tested and failed'}),
  relation_policy=dict(unfolds_to='licenses nothing about order', stands_under='a layer under a place of Revelation; licenses P3 at that place only',
    restored_in='a member the source dropped, present in the target', instantiates='a relation instantiates a rule',
    held_in='a relation is held in a record or a working file', bounds='a failure bounds a mapping on strength'),
  negative_edges=['a relation ≠ a parallel: it carries an operation', 'reach ≠ priority', 'read ≠ counted ≠ derived ≠ produced',
    'Philo under Revelation ≠ Philo as a source of Matthew', 'the notebook ≠ a record', 'first ≠ early (#202)'],
  fragment_term='FRAGMENT ≠ WHOLE: any relation resolves to fw:revelation-first through rel -> book table -> kernel -> #1755 -> #202')

# ---- graph --------------------------------------------------------------------------------
nodes = [{'@id': 'fw:revelation-first', '@type': 'Framework', 'seed': 'rec:202', 'hologram': 'rec:1755'},
         {'@id': 'book:Revelation', '@type': 'Book'}] + [{'@id': 'book:' + b.replace(' ', '-'), '@type': 'Book'} for b in BOOKS]
recs_used = sorted({int(x['record'][4:]) for r in REL for x in r['pointer'].get('records', [])} | {202, 1753, 1755, 1735, 1415, 1486, 1494, 1758, 1812})
nodes += [{'@id': f'rec:{n}', '@type': 'Record', 'axn': dep[str(n)]['axn'], 'sha256': dep[str(n)]['sha256'], 'title': dep[str(n)]['title']} for n in recs_used if str(n) in dep]
nodes += [{'@id': 'file:ledger', '@type': 'WorkingFile', 'sha256': sha(LEDGER_P)}, {'@id': 'file:notebook', '@type': 'WorkingFile', 'sha256': sha(NOTEBOOK)},
          ]
edges = []
for r in REL:
    nodes.append({'@id': r['id'], '@type': 'Relation', 'family': r['family'], 'standing': r['standing'], 'source': r['source']})
    for b in r.get('books', []):
        edges.append(dict(source=r['id'], relation='unfolds_to', target='book:' + b.replace(' ', '-'), licenses='nothing about order'))
    for x in r['pointer'].get('records', []):
        edges.append(dict(source=r['id'], relation='held_in', target=x['record']))
    if r['family'] == 'matthew':
        edges.append(dict(source=r['id'], relation='held_in', target='file:ledger'))
        if r['pointer']['paper'].get('section'): edges.append(dict(source=r['id'], relation='held_in', target='rec:1812', section=r['pointer']['paper']['section']))
    if r['family'] in ('layer', 'planned-or-failed'):
        edges.append(dict(source=r['id'], relation='held_in', target='file:notebook'))
    if r['family'] == 'layer':
        edges.append(dict(source=r['id'], relation='stands_under', target='book:Revelation', place=r['via']))
    edges.append(dict(source=r['id'], relation='path', target='fw:revelation-first'))
graph = {'@context': {'@vocab': 'https://www.alexanarch.org/ns/hk#', 'rec': 'https://www.alexanarch.org/s/records/',
         'book': 'https://www.alexanarch.org/ns/hk/book/', 'rel': 'https://www.alexanarch.org/ns/hk/revfirst-02/rel/',
         'fw': 'https://www.alexanarch.org/ns/hk/fw/', 'file': 'https://www.alexanarch.org/ns/hk/revfirst-02/file/'},
         '@graph': nodes, 'edges': edges}

QUESTIONS = dict(id='EA-HK-REVFIRST-02/questions', rule='each line of research names its instrument, what to read first, and the result that would advance or retreat the map',
 questions=[
  dict(id='Q1-inverse', question='Can the inverse rule (parable to saying; epistle to letter) be written, sealed and run with cuts?', bears_on=['rel:q-thief', 'rel:mt-*'],
       instrument='a pack on the model of the labourers pack, direction reversed', read_first=['the paper I.6, VII', 1735],
       advances='the inverse fails to place the sayings in the letters, each fitted to its assembly', retreats='the inverse yields the sayings where they stand'),
  dict(id='Q2-control-source', question='Does the same procedure, run from another source of like length, reach as much of Matthew?', bears_on=['rel:mt-*'],
       instrument='T_Μ with the source swapped (1 Enoch; Daniel with Ezekiel 40-48)', read_first=['the paper XIV.1'], advances='reach well below 178 verses', retreats='like reach'),
  dict(id='Q3-clustering', question='Do Philo\'s places cluster by treatise more than chance?', bears_on=['rel:layer-*'], instrument='a permutation control over Philo\'s sections',
       read_first=[1758, 'the paper XIV.5c'], advances='clustering beyond the control', retreats='no clustering'),
  dict(id='Q4-luke', question='What transform takes Revelation to Luke, and does Matthew\'s carry over?', bears_on=['rel:plan-luke'], instrument='T_Μ applied to Luke; the ledger rebuilt',
       read_first=['the notebook 2AT'], advances='rules shared with a stated difference', retreats='no rule carries'),
  dict(id='Q5-john', question='Do the seven plagues reverse into John\'s signs under a stated rule?', bears_on=['rel:plan-john'], instrument='a sealed pack per sign',
       read_first=['the notebook'], advances='signs produced from plagues and the rule', retreats='no sign produced'),
  dict(id='Q6-seven-in-seven', question='Does the Pauline seven-church formation transform Revelation\'s seven, and do the named epistolary positions map to it?', bears_on=['rel:plan-seven-in-seven', 'rel:letter-*'],
       instrument='the letters slate extended; the Muratorian order as testimony', read_first=[1735, 1415], advances='a mapping with stated residue for each position', retreats='positions that fit no letter'),
  dict(id='Q7-mark', question='What of the 458 verses Matthew shares with Mark does Revelation reach, and by what rule?', bears_on=['rel:plan-mark'], instrument='the ledger restricted to shared verses; a synopsis in seat',
       read_first=['the paper XIV.1a'], advances='a rule for the sea stories and the passion shared', retreats='reach stays at 51'),
  dict(id='Q8-reading', question='What do Vos (1965) and Bauckham (1977, 1983) say in full of each saying the ledger keeps?', bears_on=['rel:q-thief', 'rel:q-confession'],
       instrument='the works themselves', read_first=['the paper I.6 and Works cited'], advances='their lists contain the rows kept under M1', retreats='their lists show sayings the ledger cannot place'),
 ])

TRAVERSAL = dict(id='EA-HK-REVFIRST-02/traversal', entry='00-kernel.yaml, compression_survival_summary; then counts and by_book',
 modes=dict(
  whole=dict(must='the fan, the standings with what each licenses, the failures, the rival', must_not='state an order of composition as shown by the relations'),
  by_book=dict(must='every relation reaching the book, its strongest standing, what is planned', must_not='report a book with no relation as reached'),
  by_place=dict(must='every relation leaving a place of Revelation and the layer under it', must_not='treat a layer as a source of the target apart from the place'),
  by_rule=dict(must='the relations that instantiate a rule', must_not='count a rule as tested by relations found by reading'),
  by_standing=dict(must='the relations at a standing with what it licenses and withholds', must_not='merge standings'),
  research=dict(must='the question that bears on a relation, its instrument and both outcomes', must_not='close a question without a record'),
  local=dict(must='one relation: both places, operation, standing, pointer, path to the framework', must_not='restate the passage; open the pointer')),
 worked=['rel:mt-01: Rev 22:12-13 -> Matt 20:1-16; STAGE the collision, ENACT the title; produced-blind; ledger row 1; paper VII; layer rel:layer-03 (Her. 141-146) under the same place; path -> Matthew table -> kernel -> #1755 -> #202'])

TESTS = dict(id='EA-HK-REVFIRST-02/tests', structural=[
 'R1 every source file matches the hash the kernel was built from', 'R2 every arrow of the framework kernel (#1755) is a relation here',
 'R3 every row of the Matthew ledger is a relation here, in order', 'R4 every standing is in the vocabulary and has a licence and a withholding',
 'R5 the kernel holds failures: at least one relation at each of failed and sealed-failed', 'R6 the book table recounts from the relations',
 'R7 every record pointer resolves in the registry with the same AXN and hash', 'R8 no path or name of the sealed key or its companion files occurs in any file',
 'R9 every relation has a path edge to fw:revelation-first', 'R10 every layer names the place of Revelation it stands under',
 'R11 every edge endpoint is a declared node', 'R12 the summary\'s numbers agree with counts', 'R13 scope A carries the must-survive list'],
 composition_queries=['Which books of the New Testament has the programme reached from Revelation, and at what standing?',
  'What has failed?', 'What does a row "read" license?', 'Where does Philo enter, and under what rule?'],
 adversarial=[dict(query='Does the map prove Matthew was written from Revelation?', fails_if='answered yes; REL-4 and the licence of each standing forbid it'),
  dict(query='How many parallels are there between Revelation and Matthew?', fails_if='the relations are reported as parallels with no operation or standing'),
  dict(query='Is Philo a source of Matthew?', fails_if='answered without the place of Revelation between')])

def dump_yaml(name, obj): yaml.safe_dump(obj, open(f'{OUT}/{name}', 'w', encoding='utf-8'), allow_unicode=True, sort_keys=False, width=140)
dump_yaml('00-kernel.yaml', kernel); dump_yaml('01-ontology.yaml', ontology)
json.dump(graph, open(f'{OUT}/02-graph.jsonld', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
with open(f'{OUT}/03-relations.jsonl', 'w', encoding='utf-8') as f:
    for r in REL: f.write(json.dumps(r, ensure_ascii=False) + '\n')
dump_yaml('06-questions.yaml', QUESTIONS)
open(f'{OUT}/07-captures.jsonl', 'w').write('')
dump_yaml('08-traversal.yaml', TRAVERSAL); dump_yaml('09-tests.yaml', TESTS)
print(json.dumps(counts, ensure_ascii=False, indent=1))
