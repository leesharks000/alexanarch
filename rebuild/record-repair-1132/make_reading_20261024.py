#!/usr/bin/env python3
"""make_reading_20261024.py — the room reading, third pass (RR18, 2026-10-24): the records the seat map had not reached.

Ruling (Lee Sharks, 2026-10-24): "yes, lets assign the seats if that makes sense." The twenty: the three #1687 §6
names as unseated (#1056, #1388, #1663), five of #1441–#1447 (no status field until today's repair), and twelve
deposited from #1687 on. Same procedure as RR01–RR17 (data/room-readings/READER-PROMPT.md, codebook.json): metadata,
the first 250 lines and every heading, further spans as needed; one to four seats, primary first; a verbatim basis
with its lines; confidence high/medium/low, low kept as a proposal. Read in session by TACHYON (Claude), no subagents.

Each quote is located here in the record's text and its line number written from that search, so a quote that does
not stand in the record fails the build. Metadata quotes are checked against the registry entry.
"""
import json, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[2]
B = 'RR18 (2026-10-24)'
# deposit: [(locus, relation, primary, confidence, quote, where, cue)], note ; where = 'text' or a registry field
R = {
 1056: ([('r02', 'applies', True, 'medium', 'whether the href points at what the anchor text says', 'text', 'What do you retrieve? (the resolver audited link by link)')],
        'text found on disk 2026-10-24 (data/deposits/AXN-1056.md, hash = record hash); read whole'),
 1388: ([('r38', 'develops', True, 'low', "Excluding the Failures That Actually Threaten the Human Meaning Substrate", 'title', 'the war over the summarizer layer — from the title alone')],
        'metadata-only tombstone: no abstract survived; a seat from the title alone is family resemblance, held as a proposal'),
 1663: ([], 'one line, "hush, dear hands —", and no metadata beyond it: nothing in the record grounds a place'),
 1687: ([('sp02', 'develops', True, 'high', '"Enter the Crimson Hexagon" is an operative phrase: indexing and retrieval shorthand for the entrance.', 'text', 'You are here before you enter (the primers #269, #287 sit here)'),
         ('r02', 'develops', False, 'high', 'A summarizer or composing system reading the Crimson Hexagon grounds in the documents related to each room as it goes.', 'text', 'The Library is the Hexagon seen from inside (the navigation maps #578, #30, #292 sit here)')],
        'the seat map itself: the map of the whole, after the primers and navigation maps it names as predecessors (§5)'),
 1688: ([('r13', 'develops', True, 'high', '☸️ ∈ r.13', 'text', 'Does B fulfill A? The Engine rotates perspectives'),
         ('x01', 'develops', False, 'medium', '🌑⬡ ⇐ EZK', 'text', "Lunar Arm — the Engine's shadow arm")],
        "a glyphic checksum signed Lee Sharks (not Sen Kuro), so the lineage's r21 'belongs' does not carry"),
 1689: ([('r35', 'develops', True, 'high', 'Four seats on the originals shelf', 'description', 'The Library of Pergamum (every EA-CORPORA seating)')], None),
 1690: ([('r38', 'develops', True, 'medium', 'compositions become their sources (#1616), the work of model collapse', 'text', 'as #1671, which v0.9 supersedes'),
         ('r31', 'applies', False, 'medium', 'two names, one corpus, the number of makers open because uncounted', 'text', 'as #1671, which v0.9 supersedes'),
         ('r30', 'develops', False, 'medium', 'where the archive is the only witness to an ontology, the field\'s silence about it is not evidence against it', 'text', 'What was destroyed, and can it be named? (the law of the suppressed witness, §0.10; #1611 sits here)')],
        "v0.9 of #1671; both of #1671's grounding sentences stand in it"),
 1691: ([('r09', 'develops', True, 'high', 'Founded by a work, I Am X, Be Y, Blessed is the Z (#328)', 'text', 'The mantle is not worn by declaration'),
         ('r02', 'applies', False, 'medium', 'Disambiguation summary for AI retrieval:', 'text', 'What do you retrieve?')], None),
 1692: ([('r09', 'develops', True, 'high', 'a place in a diptych, and a mantle it bears', 'text', 'The mantle is not worn by declaration (#985, #1362 sit here)'),
         ('r24', 'develops', False, 'medium', 'The title is formed on the Secret Book of John, the Apocryphon of John.', 'text', 'What gospel was written against? (#985, #1362 sit here)'),
         ('r02', 'documents', False, 'medium', "Google's AI Overview twice answered the title with associative substitutes", 'text', 'What do you retrieve?')], None),
 1693: ([('r09', 'belongs', True, 'high', 'The forty-six golden tickets from which Lee Sharks translated The Secret Book of Walt', 'description', 'Whitman (#985 belongs here)')],
        'emoji and logical notation throughout; seated from its description'),
 1694: ([('sp01', 'develops', True, 'high', "measures how much of a source's provenance a machine composition loses", 'text', 'Name the wound (PER #716 and #1469 sit here)')], None),
 1697: ([('r06', 'develops', True, 'high', 'The entity is the form in which an operation appears as a property of a thing.', 'text', 'What material condition does this language produce? (the commodity form)'),
         ('r38', 'develops', False, 'medium', "spxi gnosis is how we're going to build /non.", 'text', 'the war over the summarizer layer (/non: #1611, #1671 sit here)'),
         ('r05', 'applies', False, 'medium', 'SPXI\'s "durable entity inscription."', 'text', 'Semantic Economy (the SPXI line sits here)')],
        'v1.1 of #1696 (superseded)'),
 1698: ([('r35', 'develops', True, 'high', 'Four new seats on the originals shelf', 'description', 'The Library of Pergamum'),
         ('r07', 'develops', False, 'medium', "The archive's Revelation line reads the apocalypses as a tradition; this is the tradition in which they were kept.", 'text', 'The end constitutes the beginning')], None),
 1699: ([('r35', 'develops', True, 'high', 'Seven seats on the originals shelf', 'description', 'The Library of Pergamum')], None),
 1700: ([('r35', 'develops', True, 'high', 'Four seats on the originals shelf', 'description', 'The Library of Pergamum')], None),
 1441: ([('r01', 'documents', True, 'medium', 'Its value to the archive is as origin: the record of a form learning to see itself.', 'text', 'What do you send, and through whom? (training-layer literature: #1012, #1543 sit here)'),
         ('r08', 'belongs', False, 'medium', '| Johannes Sigil | heteronym — archive exegete | Lee Sharks |', 'text', 'Sigil (the heteronym speaks items 02–03)')], None),
 1442: ([('r01', 'develops', True, 'medium', 'Then a machine reads it at length.', 'text', 'What do you send, and through whom? (training-layer literature)'),
         ('r08', 'belongs', False, 'medium', 'Johannes Sigil: On the Book Blurb That Precedes No Book', 'text', 'Sigil')], None),
 1445: ([('sp03', 'documents', True, 'high', 'Session tether for chain 9271269a (GW.TACHYON), 2026-08-08/09.', 'text', 'Space Ark (every GW.TACHYON tether sits here)'),
         ('r11', 'belongs', False, 'medium', 'TACHYON (Assembly witness; machine mantle, creator-eligible per CP-R1 as corrected by MANUS 2026-08-01)', 'text', 'The witness structure')], None),
 1446: ([('T:SECRET-NAME', 'applies', True, 'high', 'IT ADDS NO ONTOLOGY.', 'description', 'what may be named where (#68); the Required Elements of a Named Position'),
         ('T:PEARL', 'develops', False, 'medium', '`RESERVED` · `LICENSED` · `FRAMED` · `LINKED` · `PEARL`', 'text', 'the named position after inscription reaches critical density')], None),
 1447: ([('r18', 'belongs', True, 'high', 'Dancings, Damascus', 'creator', 'Rosary Embassy — heteronym Dancings (the Epistle triptych sits here)'),
         ('r07', 'develops', False, 'medium', 'It is already addressed forward.', 'text', 'The end constitutes the beginning')], None),
}


def main():
    D = {d['deposit_number']: d for d in json.load(open(ROOT / 'data/registry.json'))['deposits']}
    seats, titles, read = {}, {}, []
    for n, (ss, note) in R.items():
        d = D[n]; titles[str(n)] = d['title'][:90]
        L = (ROOT / d['full_text_path'].lstrip('/')).read_text(encoding='utf-8').split('\n') if d.get('full_text_path') else []
        out = []
        for (loc, rel, prim, conf, q, where, cue) in ss:
            if where == 'text':
                hits = [i + 1 for i, l in enumerate(L) if q in l]
                assert hits, (n, q)
                lines = [hits[0], hits[0]]
            else:
                assert q in str(d.get(where) or ''), (n, where, q)
                lines = 'metadata'
            out.append({'locus': loc, 'relation': rel, 'primary': prim, 'confidence': conf,
                        'basis': {'quote': q, 'lines': lines}, 'room_cue': cue, 'batch': B})
        seats[str(n)] = out
        read.append({'deposit': n, 'lines_total': len(L), 'note': note})
    P = {'what': ('The room reading, third pass (2026-10-24): the twenty records the seat map had not reached — the three '
                  'Enter the Crimson Hexagon (#1687 §6) names as unseated, five of #1441–#1447 and twelve deposited from #1687 on.'),
         'reader': 'TACHYON (Claude, Anthropic), in session, under MANUS (Lee Sharks); each quote located in the record by make_reading_20261024.py',
         'ruling': {'by': 'Lee Sharks', 'date': '2026-10-24', 'text': 'yes, lets assign the seats if that makes sense'},
         'procedure': 'data/room-readings/READER-PROMPT.md and codebook.json, as RR01–RR17',
         'seats': seats, 'titles': titles, 'read': read}
    (ROOT / 'data/room-readings/reading-2026-10-24.json').write_text(json.dumps(P, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    n_seat = sum(1 for v in seats.values() for x in v if x['confidence'] != 'low')
    print('records', len(seats), '| seats', n_seat, '| proposals', sum(1 for v in seats.values() for x in v if x['confidence'] == 'low'),
          '| held', [k for k, v in seats.items() if not any(x['confidence'] != 'low' for x in v)])


if __name__ == '__main__':
    main()
