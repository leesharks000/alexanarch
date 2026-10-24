#!/usr/bin/env python3
"""reissue_1527_1529.py — The Lucente Extension (#1527) as v9.6 and the Claim Status Packet (#1529) as v0.7, in place.

Ruling (Lee Sharks, 2026-10-24), on ChatGPT's notes on both records, each checked at its locus first:
"probably a version in place for both"; on the review history, the option to remove it, as with #1409 on 2026-10-22;
and of the §1 provenance passage, whose source (Paper 208 or her letters) he does not know: "lets just remove it".

The ground: her notice of 2026-10-22 invokes §3 of the signed approval instrument, "Your correspondence remains
private and enters no publication, deposit, or public record." The reviews of v2.0–v6.0 came by correspondence.

What changes, and nothing else:
  1. The consent clause dated (#1527 substrate and §9; #1529 A.1 `consent`): consent given at deposit, withdrawn
     2026-10-22; the attribution to Paper 208 stands; the title is the author's naming of his own work.
  2. Statements of what she reviewed, returned, confirmed or flagged are removed (#1527 §§0.1–0.5, 0.9, 1, 4.5, 4.6,
     5, 5.3, 7; #1529 A.1 `selected_by`, `authorized_by`, the deposit_condition note). Each correction stays, as the
     author's change. Paper 208, its quotations and their translation provenance are untouched.
  3. The stale sentences saying transcription she supplied "is being incorporated" (#1527 §7, twice) are removed.
  4. #1529's `deposit_condition` and the §6.3 stagnation example's "observer confirmation pending" are marked
     withdrawn, after #1527 v9.2, which withdrew that invented condition.
  5. Hard-coded line breaks inside prose paragraphs are joined (both records), and two earlier join artifacts are
     repaired ("No-Double- Draw"; a stray space inside the quoted Japanese 「…経た上で提示すること」).
  6. Each record gets a change-log entry for the new version; the AXN is re-derived from the new bytes, with the prior
     hash and AXN kept in `reissue_history` (the convention of #1409's reissues).
"""
import datetime, hashlib, json, pathlib, re, sys
ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts'))
import record_modification as rm
from axn_lib import axn_glyph_from_hash, axn_clusters_from_hash, axn_reading_from_clusters, compose_axn

ON = '2026-10-24'
RULING = ('Lee Sharks, 2026-10-24: "probably a version in place for both"; the review history removed, as with #1409 '
          'on 2026-10-22 (her notice invokes §3 of the approval instrument: "Your correspondence remains private and '
          'enters no publication, deposit, or public record"); of the §1 provenance passage, "lets just remove it"')
CONSENT = ('named at deposit with her consent, which she withdrew on 2026-10-22; the attribution stands')

E1527 = [
 ('version: v9.5', 'version: v9.6'),
 ('"version": "v9.5",', '"version": "v9.6",'),
 ('named with her standing consent, ORCID', CONSENT + ', ORCID'),
 ('## 0.1 CHANGES AT v3.0 — ON REVIEW BY THE OBSERVER\n\nEnli Lucente reviewed v2.0 and returned four corrections. All four are applied. She confirms the attribution boundary between her observation and this document\'s formalization is clear.',
  '## 0.1 CHANGES AT v3.0\n\nFour corrections, all applied.'),
 ('**Also corrected, not from this review:**', '**Also corrected:**'),
 ('No-Double- Draw', 'No-Double-Draw'),
 ('## 0.2 CHANGES AT v4.0 — SECOND REVIEW BY THE OBSERVER\n\nEnli Lucente reviewed v3.0 and returned ten corrections. All ten are applied. She\nconfirms the attribution boundary remains clear.\n\n**They share the cause of her previous set.**',
  '## 0.2 CHANGES AT v4.0\n\nTen corrections, all applied.\n\n**They share the cause of the previous set.**'),
 ('recorded here because it is now the second consecutive review to find the same failure in the revision method rather than in the argument.',
  'recorded here because this is the second consecutive set to find the same failure in the revision method rather than in the argument.'),
 ('## 0.3 CHANGES AT v5.0 — THIRD REVIEW BY THE OBSERVER\n\nThree corrections returned on v4.0. All applied.',
  '## 0.3 CHANGES AT v5.0\n\nThree corrections, all applied.'),
 ('**Two were more than copyediting** and are flagged for the observer.', '**Two were more than copyediting.**'),
 ('**The deposit condition was already satisfied and therefore idle.** The observer has reviewed v2.0 through v6.0. The real condition is narrower:',
  '**The deposit condition was already satisfied and therefore idle.** The real condition is narrower:'),
 ('*(Superseded at v9.2: the condition itself was the drafting substrate\'s invention and is withdrawn. The observer set no condition.)*',
  '*(Superseded at v9.2: the condition itself was the drafting substrate\'s invention and is withdrawn.)*'),
 ('**v9.0 stated a deposit condition the observer never set**, and v9.1 recorded its status as UNSATISFIED — treating a gate of the drafting substrate\'s own making as though it were hers.\n\n**She never withheld anything.** Three review passes, corrections at each, the\nattribution boundary confirmed clear, no condition attached.\n\n',
  '**v9.0 stated a deposit condition the observer never set**, and v9.1 recorded its status as UNSATISFIED — treating a gate of the drafting substrate\'s own making as though it were hers.\n\n'),
 ('\n\n**And the archive has paid this cost before:** a handwritten SPXI withdrawn from the full and versioned without its author\'s section, over a consent that never arrived. **A gate nobody asked for produces a gap nobody wanted.**', ''),
 ('経た上で 提示', '経た上で提示'),
 # §1: the provenance passage, source unknown (Paper 208 or her letters)
 ('**Provenance of the record.** Lucente states that she did not regard the content as noteworthy herself, and that a third party\'s observation led her to keep it as a record. That third party is the present author. **The observation is hers; the prompting to preserve it was external.** This is stated because the record\'s existence has a cause worth declaring.\n\n', ''),
 ('*Correction due to review of v6.0. Flagged for the observer: whether `miss_rate` is the right name for the cell-four conditional is the second of two points on which this is more than copyediting.*',
  '*Correction due to review of v6.0. Whether `miss_rate` is the right name for the cell-four conditional is the second of two points on which this is more than copyediting.*'),
 ('\n\n*Correction due to Enli Lucente, on review of v2.0.*\n\n**`miss_rate` is the quantity of interest**', '\n\n**`miss_rate` is the quantity of interest**'),
 ('\n\n*Correction due to Enli Lucente, on review of v2.0.*\n\n### 4.7 Protocol', '\n\n### 4.7 Protocol'),
 ('*Correction due to Enli Lucente, on review of v2.0, and independently to the\nreview of the Four Interfaces map.*', '*Correction due to the review of the Four Interfaces map.*'),
 ('\n\n*Correction due to Enli Lucente, on review of v4.0.*\n\n', '\n\n'),
 # §7
 (' The Japanese is quoted at every load-bearing point so the reading can be checked against the pages. Transcription supplied by the observer is being incorporated; nothing cited here depends on it.',
  ' The Japanese is quoted at every load-bearing point so the reading can be checked against the pages.'),
 ('**The observer has now reviewed v2.0 through v6.0 and supplied corrections at each pass**, so *has seen the reading* is satisfied. **Nothing remains pending. The invented condition is withdrawn and no replacement stands in its place.**',
  '**Nothing remains pending. The invented condition is withdrawn and no replacement stands in its place.**'),
 ('\n\nShe reviewed v2.0 through v6.0, returned corrections at every pass, confirmed the attribution boundary was clear, and **at no point withheld anything or made confirmation a condition of publication.**', ''),
 ('The observer reviewed v2.0 through v6.0 and supplied corrections at each pass.\n**v7.0 through v9.5 are internal**', '**v7.0 through v9.6 are internal**'),
 ('\n\nSubstantial transcription has since been supplied by the observer and is being\nincorporated; the citations above do not depend on it.', ''),
 # §9
 ('ORCID 0009-0006-2822-8359. Named with her standing consent.',
  'ORCID 0009-0006-2822-8359. Named at deposit with her consent, which she withdrew on 2026-10-22; the attribution stands. The title, *The Lucente Extension*, is the author\'s naming of his own work.'),
]
LOG1527 = ('\n## 0.13 CHANGES AT v9.6 — REISSUED IN PLACE\n\n'
 '**The consent clause is dated.** The substrate disclosure and §9 said the observations were named *with her standing consent*, a present state. The naming was made with her consent at deposit, and she withdrew it on 2026-10-22. The attribution stands, and the title is the author\'s naming of his own work.\n\n'
 '**Her correspondence enters no public record.** Her notice of 2026-10-22 invokes §3 of the signed approval instrument: *"Your correspondence remains private and enters no publication, deposit, or public record."* The reviews of v2.0 through v6.0 came by correspondence, so the change log and the correction notes no longer report what was reviewed, returned or confirmed. Each correction stays, as the author\'s change. One passage of §1 on the record\'s provenance, whose source could not be fixed as Paper 208 or the correspondence, is removed. Paper 208, its quotations and the declared translation provenance are unchanged.\n\n'
 '**Two stale sentences are removed** from §7, each saying that transcription supplied by the observer *is being incorporated*.\n\n'
 '**Line breaks.** Hard-coded breaks inside prose paragraphs are joined, and two earlier join artifacts are repaired: *No-Double- Draw*, and a stray space inside the quoted rebuttal standard.\n\n---\n')

E1529 = [
 ('version: v0.6', 'version: v0.7'),
 ('> **STATUS — SCHEMA DRAFT v0.6.**', '> **STATUS — SCHEMA DRAFT v0.7.**'),
 ('"consent": "named attribution, standing consent"', '"consent": "named attribution; consent given at deposit, withdrawn 2026-10-22; attribution stands"'),
 ('"deposit_condition": {\n   "state": "UNSATISFIED",\n   "requires": "observer confirmation of the quoted Japanese and the English renderings at load-bearing points",\n   "note": "Observer reviewed v2.0-v6.0. v7.0-v9.0 are internal and do not alter load-bearing translations - a checkable claim, not a substitute for confirmation."\n  }',
  '"deposit_condition": {\n   "state": "WITHDRAWN",\n   "was": "observer confirmation of the quoted Japanese and the English renderings at load-bearing points",\n   "note": "Withdrawn at EA-PER-LUCENTE-01 v9.2 (#1527 §0.9): the condition was the drafting substrate\'s invention. This packet was authored against v9.0 and keeps the field as its historical state."\n  }'),
 ('"selected_by": "observer, on review of v6.0"', '"selected_by": "author, on revision of v6.0"'),
 ('"authorized_by": "observer-review-v2.0",', '"authorized_by": "revision-v3.0",'),
 ('  "blocked_by": "observer confirmation pending"\n}', '  "blocked_by": "observer confirmation pending",\n  "_note": "Historical example, from EA-PER-LUCENTE-01 v9.0. The confirmation condition was withdrawn at v9.2 (#1527 §0.9)."\n}'),
]
LOG1529 = ('## 0.6 CHANGES AT v0.7 — REISSUED IN PLACE\n\n'
 '**The worked packet at A.1 brought into line with EA-PER-LUCENTE-01 v9.6 (#1527).** `contributing_observation.consent` is dated: consent given at deposit, withdrawn on 2026-10-22, attribution standing. `deposit_condition` is marked WITHDRAWN, after #1527 v9.2 withdrew the invented condition; the packet was authored against v9.0 and keeps the field as its historical state. The §6.3 stagnation example, which shows that condition as pending, is marked historical. Two provenance fields that attributed a constraint selection and a weakening to review by the observer now name the author\'s revision, since her correspondence enters no public record (her notice of 2026-10-22, invoking §3 of the approval instrument).\n\n'
 '**Line breaks.** Hard-coded breaks inside prose paragraphs are joined.\n\n---\n\n')

BLOCK = re.compile(r'^(#|\||-{3}|- |\* |\+ |\d+\.\s|```|<|!\[|\[\^|\$\$)')
CJK = re.compile(r'[　-ヿ㐀-鿿＀-￯]')


def join_breaks(text):
    head, body = (text.split('\n---\n', 1) if text.startswith('---\n') else ('', text))
    L = body.split('\n'); out = []; fence = False; joined = 0
    for ln in L:
        if ln.startswith('```'):
            fence = not fence; out.append(ln); continue
        prev = out[-1] if out else ''
        if not fence and out and prev.strip() and re.match(r'^ {2,8}\S', ln) and (re.match(r'^\d+\.\s', prev) or prev.startswith('<!--')):
            out[-1] = prev.rstrip() + ' ' + ln.strip(); joined += 1; continue      # a list item's indented continuation; a comment's lines
        ok = (not fence and out and prev.strip() and ln.strip() and not prev.endswith('  ')
              and not BLOCK.match(prev) and not BLOCK.match(ln) and not prev.startswith('    ') and not ln.startswith('    '))
        whole_italic = lambda x: x.strip().startswith('*') and x.strip().endswith('*')
        if ok and whole_italic(prev) and whole_italic(ln):           # two italic lines (a footer pair): kept apart
            ok = False
        if ok and prev.startswith('>') and ln.startswith('>') and prev[1:].strip() and ln[1:].strip():
            q = ln[1:].strip()
            if q.startswith(('*', '「')) or prev.rstrip().endswith(('*', '」')):   # a translation under its original, or a new statement
                out.append(ln); continue
            a, b = prev.rstrip(), q
        elif ok and not prev.startswith('>') and not ln.startswith('>'):
            a, b = prev.rstrip(), ln.strip()
        else:
            out.append(ln); continue
        sep = '' if (CJK.search(a[-1:]) and CJK.search(b[:1])) else ' '
        out[-1] = a + sep + b; joined += 1
    body2 = '\n'.join(out)
    return (head + '\n---\n' + body2 if head else body2), joined


def apply(text, edits):
    for a, b in edits:
        assert text.count(a) == 1, (a[:80], text.count(a))
        text = text.replace(a, b)
    return text


def main():
    reg = json.loads((ROOT / 'data/registry.json').read_text()); D = {d['deposit_number']: d for d in reg['deposits']}
    plan = {1527: (E1527, LOG1527, '\n## 1. THE ORIGINATING OBSERVATION', 'v9.5', 'v9.6'),
            1529: (E1529, LOG1529, '## 1. THE PROBLEM, WITH EVIDENCE', 'v0.6', 'v0.7')}
    for n, (edits, log, anchor, vfrom, vto) in plan.items():
        d = D[n]; tp = ROOT / d['full_text_path'].lstrip('/')
        old = tp.read_text(encoding='utf-8'); old_hash = hashlib.sha256(old.encode()).hexdigest()
        assert old_hash == d['hash'], n
        t = apply(old, edits)
        t, joined = join_breaks(t)
        assert t.count(anchor) == 1, anchor
        t = t.replace(anchor, (log + anchor) if n == 1529 else ('\n' + log.lstrip('\n') + anchor))
        if n == 1527:
            for bad in ('standing consent', 'is being incorporated', 'is being\nincorporated', 'returned four corrections', 'She never withheld'):
                assert bad not in t.replace(log, ''), (n, bad)
        else:
            assert 'standing consent' not in t and 'observer-review' not in t and 'observer, on review' not in t
        h = hashlib.sha256(t.encode()).hexdigest(); glyph = axn_glyph_from_hash(h)
        hist = d.get('reissue_history') if isinstance(d.get('reissue_history'), list) else []
        hist.append({'date': ON, 'from_version': vfrom, 'to_version': vto, 'hash_before_reissue': old_hash,
                     'axn_before_reissue': d['axn'], 'reason': RULING, 'lines_joined': joined,
                     'note': 'The deposit number and hex position are addresses and do not move. The AXN is re-derived from the new bytes; the prior AXN and hash are kept here.'})
        d['reissue_history'] = hist
        was_axn = d['axn']
        d['hash'] = h; d['axn_canonical'] = h; d['emoji'] = glyph
        d['axn'] = compose_axn(d['hex'], d.get('family', 'ARCHIVAL'), glyph)
        d['clusters'] = axn_clusters_from_hash(h); d['reading'] = axn_reading_from_clusters(d['clusters'])
        d['version'] = vto
        rm.touch(d, 'version', f'reissued in place as {vto} ({RULING})', was=vfrom, now=vto, when=ON)
        rm.touch(d, 'axn', 'AXN re-derived from the reissued bytes', was=was_axn, now=d['axn'], when=ON)
        if n == 1527:
            was = d['substrate']; assert 'named with her standing consent' in was
            d['substrate'] = was.replace('named with her standing consent', CONSENT)
            rm.touch(d, 'substrate', 'consent clause dated, in the text and the registry alike', was=was, now=d['substrate'], when=ON)
            for e in d.get('errata') or []:
                if e.get('date') == ON and 'standing consent' in e.get('locus', ''):
                    e['status'] = 'folded into the text at v9.6'
        tp.write_text(t, encoding='utf-8')
        dep = ROOT / 'data/deposits' / f"AXN-{d['hex']}.md"
        if dep.exists() and hashlib.sha256(dep.read_bytes()).hexdigest() == old_hash:
            dep.write_text(t, encoding='utf-8')
        print(n, vfrom, '->', vto, '| joined', joined, '|', was_axn, '->', d['axn'])
    reg['last_updated'] = datetime.datetime.now(datetime.UTC).strftime('%Y-%m-%dT%H:%M:%SZ')
    (ROOT / 'data/registry.json').write_text(json.dumps(reg, ensure_ascii=False, indent=1))


if __name__ == '__main__':
    main()
