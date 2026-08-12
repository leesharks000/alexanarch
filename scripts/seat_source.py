#!/usr/bin/env python3
"""seat_source.py — seat one source's data into the rebuilt registry, with a ledger.

Every value is routed to a named slot by an EXPLICIT map below. Nothing is
merged, overwritten, or preferred: a value already present from another source
is recorded as an additional provenanced variant. Text whose class is not yet
established (is this the machine's output, or a reading of it?) goes to
unclassified_text and is NEVER placed in machine_output by this script.
"""
import sqlite3,json,sys,collections,re

DB='/home/claude/palette/capture-palette.sqlite'
REG='/home/claude/palette/EA-WG-CAPTURES-01-REBUILD.json'
SKEL='/home/claude/palette/EA-WG-CAPTURES-01-EMPTY-v3.3.json'

# field -> (block, slot). 'UNCLASSIFIED' text is text of undetermined class.
FIELD_MAP={
 # ANALYSIS BY DEFINITION. A description that quotes the machine is analysis containing
 # quoted text, not an undetermined object and not a transcript. Measured over the 130
 # leesharks descriptions: 99 are an analyst frame around quoted spans, 24 mix analyst
 # prose with quotations, 4 carry no quotation at all, 3 are almost entirely quotation.
 # In every case the field is the analyst's record OF a capture. Quoted spans inside it
 # are marked as quotations, with completeness explicitly unknown, and are never promoted.
 'd':('analysis','records'), 'description_html':('analysis','records'),
 'overview_at_capture':('analysis','records'),
 # `transcript` is NOT routed here. Only a value whose provenance establishes it as a
 # capture-time verbatim record may enter machine_output, and that is decided per record.
 'transcript':('_HOLD_TRANSCRIPT',None),
 'mt':('classification','match_or_finding'), 'match_type':('measurement_flags','match_type'),
 's':('classification','section'), 'section':('classification','section'),
 'entity_type':('classification','entity_type'), 'failure_modes':('classification','failure_modes'),
 'stability_status':('classification','stability_status'), 'has_correction':('classification','has_correction'),
 'has_recapture':('classification','has_recapture'), 'auto_derived':('classification','auto_derived'),
 'entry_status':('classification','entry_status'), 'finding':('classification','finding'),
 'author_retained':('measurement_flags','author_retained'),
 'institution_retained':('measurement_flags','institution_retained'),
 'doi_retained':('measurement_flags','doi_retained'),
 'composition_source_included':('measurement_flags','composition_source_included'),
 'per_score':('measurement_flags','per_score'),
 'organic_rank':('citations_and_sources','organic_rank'),
 'source_count':('citations_and_sources','source_count'),
 'citations_shown':('citations_and_sources','citations_shown'),
 'citations':('citations_and_sources','citations_legacy'),
 'citations_note':('citations_and_sources','citations_note'),
 'sources':('citations_and_sources','sources'), 'links':('citations_and_sources','links'),
 'related':('citations_and_sources','related'), 'cite':('citations_and_sources','cite'),
 'images':('evidence','images'), 'imgs':('evidence','images'),
 'image_filenames':('evidence','image_filenames'), 'image_count':('evidence','image_count'),
 'imgs_origin':('evidence','imgs_origin'), 'image_status':('evidence','image_status'),
 'image_lacuna':('evidence','image_lacuna'), 'ocr_text':('evidence','ocr'),
 'ocr_provenance':('evidence','ocr_provenance'), 'evidence':('evidence','evidence_statements'),
 'manifest_ref':('evidence','manifest_ref'), 'verify':('evidence','verify'),
 'note_image':('evidence','note_image'),
 'surface':('query_and_surface','surface'), 'surface_raw':('query_and_surface','surface_raw'),
 'search_url':('query_and_surface','search_url'), 'exact':('query_and_surface','exact_field'),
 'capture_method':('query_and_surface','capture_method'), 'capture_class':('query_and_surface','capture_class'),
 'auth_state':('query_and_surface','auth_state_recorded'),
 'id':('identity','aliases'), 'slug':('identity','aliases'), 'slug_history':('identity','slug_history'),
 'axn':('identity','axn'), 'axn_note':('identity','axn_note'),
 'supersedes':('identity','supersedes'), 'superseded_by':('identity','superseded_by'), 'prior':('identity','prior'),
 'notes':('record_history','notes'), 'recovered':('record_history','recovered'),
 'restored_note':('record_history','restored_note'), 'record_note':('record_history','record_note'),
 'interface_observation':('record_history','interface_observation'),
 'divergence':('record_history','divergence'), 'available_readings':('record_history','available_readings'),
 'analysis':('unclassified_text','records'), 'artifact':('record_history','artifact'),
 'transcript_status':('record_history','transcript_status'),
 # address components already seated in the skeleton; recorded as consumed, not re-seated
 'q':('_ADDRESS',None), 'date':('_ADDRESS',None), 'query':('_ADDRESS',None),
 'capture_date':('_ADDRESS',None), 'sf':('_ADDRESS',None),
 # assistant-generated in the withdrawn passes; quarantined, never seated
 'meta':('_QUARANTINE',None),
}
SKIP_VALUES={'','null','[]','{}','-','none','None'}

def load():
    import os
    if os.path.exists(REG): return json.load(open(REG))
    d=json.load(open(SKEL))
    d['build']='rebuild-v0.1'
    d['status']='UNDER RECONSTRUCTION. Values seated source by source from the palette, each with provenance. Nothing merged or preferred.'
    d['seating_ledger']={'sources_consumed':[],'notes':[]}
    for a in d['addresses']:
        for o in a['observations']:
            o['analysis'].setdefault('records',[])
            o['analysis']['_rule']=('The analyst record OF a capture. A description that quotes the machine is analysis containing quoted text — by definition analysis, not an undetermined object. '
              'Quotations inside it are marked in quoted_machine_text with completeness UNKNOWN and are never promoted to machine_output. '
              'Only a value whose provenance establishes it as a capture-time verbatim record may enter machine_output.')
    return d

def seat(source_name, alias_map=None, dry_run=False):
    alias_map=alias_map or {}
    db=sqlite3.connect(DB); q=lambda s,*a: db.execute(s,a).fetchall()
    doc=load()
    by_slug={}
    for a in doc['addresses']:
        for o in a['observations']:
            by_slug.setdefault(o['legacy_slug'],[]).append((a,o))
    exclude=set()
    QUARANTINE_FIELDS=set()
    if source_name=='alexanarch':
        # MANUS ruling 2026-08-12: seat alexanarch MINUS the batch-mangled transcripts.
        # `transcript` and `meta` in this source were written by the assistant's withdrawn
        # repair passes of 11-12 August: 119 of 207 transcripts are verbatim substrings of
        # their own record's description, and all 207 meta blocks assert a per-entry read
        # that was never performed. Neither is seated. They remain in the palette and in
        # quarantine/capture-registry-20260812/ for audit.
        QUARANTINE_FIELDS={'transcript','meta','transcript_status'}
    if source_name=='machinemediation':
        # v9.42 and v9.55 are the copy the assistant synced FROM alexanarch on 2026-08-12
        # and carry the withdrawn batch-mangled content. Earlier shared blobs are the
        # ordinary upstream relationship and are excluded here only to avoid double-seating
        # alexanarch's bytes under another source's name; alexanarch is consumed separately.
        exclude={b for b, in q("SELECT blob FROM versions WHERE source='alexanarch'")}
    VER={vid:(dv,blob,fd) for vid,dv,blob,fd in q("SELECT id,doc_version,blob,first_date FROM versions WHERE source=?",source_name)
         if blob not in exclude}
    led=collections.Counter(); unmapped=collections.Counter(); nohome=collections.Counter()
    rows=q("""SELECT capture_key, field, value, version_id FROM observations
              WHERE source=? ORDER BY capture_key, field""",source_name)
    for key,field,value,vid in rows:
        if vid not in VER: continue
        dv,blob,fd=VER[vid]
        if value is None or str(value).strip() in SKIP_VALUES: led['empty_skipped']+=1; continue
        tgt=alias_map.get(key,key)
        if tgt not in by_slug: unmapped[key]+=1; continue
        if field in QUARANTINE_FIELDS:
            led['batch_mangled_field_not_seated']+=1; continue
        block_slot=FIELD_MAP.get(field)
        if not block_slot: nohome[field]+=1; continue
        block,slot=block_slot
        if block=='_ADDRESS': led['address_component_already_seated']+=1; continue
        if block=='_QUARANTINE': led['quarantined_not_seated']+=1; continue
        if block=='_HOLD_TRANSCRIPT': led['transcript_held_for_per_record_ruling']+=1; continue
        for a,o in by_slug[tgt]:
            cont=o.setdefault(block,{})
            cur=cont.get(slot)
            entry={'value':value,'source':source_name,'registry_version':dv,'blob':blob[:12],
                   'version_date':fd,'from_field':field}
            if block=='analysis':
                spans=re.findall(r"'([^']{40,})'", value)
                entry['quoted_machine_text']=[{'text':x,'completeness':'UNKNOWN — this is what the analyst quoted, not necessarily the full answer','status':'quotation inside an analyst record; NOT a transcript and never promoted to machine_output without independent capture-time evidence'} for x in spans]
                entry['analysis_shape']=('no quotation' if not spans else
                    ('predominantly quotation with an analyst frame' if sum(len(x) for x in spans)/max(1,len(value))>0.5 else 'analyst prose with quotations'))
            if isinstance(cur,list) or cur is None or cur==[]:
                lst=cur if isinstance(cur,list) else []
                if any(isinstance(x,dict) and x.get('value')==value and x.get('source')==source_name for x in lst):
                    led['redundant_same_source']+=1; continue
                if any(isinstance(x,dict) and x.get('value')==value for x in lst):
                    entry['note']='identical value already seated from another source; retained as an independent attestation'
                    led['redundant_cross_source_recorded']+=1
                else: led['seated']+=1
                lst.append(entry); cont[slot]=lst
            else:
                cont[slot]=[cur,entry] if not isinstance(cur,list) else cur+[entry]
                led['seated']+=1
    doc['seating_ledger']['sources_consumed'].append({
      'source':source_name,'seated':led['seated'],
      'redundant_cross_source_recorded':led['redundant_cross_source_recorded'],
      'redundant_same_source_skipped':led['redundant_same_source'],
      'empty_skipped':led['empty_skipped'],
      'address_components_already_seated':led['address_component_already_seated'],
      'quarantined_not_seated':led['quarantined_not_seated'],
      'fields_with_no_slot':dict(nohome),
      'capture_keys_with_no_address':dict(unmapped),
      'alias_map_applied':alias_map})
    if not dry_run: json.dump(doc,open(REG,'w'),ensure_ascii=False,indent=1)
    return led,unmapped,nohome

if __name__=='__main__':
    src=sys.argv[1]
    am=json.loads(sys.argv[2]) if len(sys.argv)>2 else {}
    led,un,nh=seat(src,am)
    print('SOURCE:',src)
    for k,v in led.items(): print('   %-38s %d'%(k,v))
    if nh: print('   fields with NO SLOT:',dict(nh))
    if un: print('   keys with NO ADDRESS:',dict(un))
