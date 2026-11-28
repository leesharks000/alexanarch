"""Repair of #1812's description and wiki article, 2026-11-28 (run once; kept as the record of what was changed)."""
import json,sys
p='data/registry.json'; r=json.load(open(p,encoding='utf-8')); d=[x for x in r['deposits'] if x['deposit_number']==1812][0]
was={'description':d['description'],'wiki_article':d['wiki_article']}
def rep(k,o,n):
    assert d[k].count(o)==1,(k,o[:50],d[k].count(o)); d[k]=d[k].replace(o,n)
rep('description',"HOW TO WRITE MATTHEW FROM REVELATION. The paper asks","HOW TO WRITE MATTHEW FROM REVELATION. Current version v2.1 (27 November 2026), which superseded v1.1 and v1.0 in place the same day; what each version added is stated at the end of this description. The paper asks")
rep('description',"Its evidence is a ledger of 86 relations, each checked for shared lemmas in a tagged text, reaching 178 of Matthew's 1,067 verses.","Its evidence is a ledger of 158 relations, each checked for shared lemmas in a tagged text, reaching 305 of Matthew's 1,067 verses (86 and 178 at v1.0).")
rep('description',"321 Greek quotations verified by machine against the seated texts (221 at v1.0).","321 Greek quotations verified by machine against the seated texts at v1.1 (221 at v1.0); the count was not rerun for v2.1.")
rep('wiki_article',"deposited in the Crimson Hexagonal Archive on 27 November 2026, with","deposited in the Crimson Hexagonal Archive on 27 November 2026 and reissued in place twice that day (the current version is v2.1), with")
rep('wiki_article',"Its evidence is a ledger of 86 relations, each checked for shared lemmas in a tagged Greek text, reaching 178 of Matthew's 1,067 verses.","Its evidence is a ledger of 158 relations, each checked for shared lemmas in a tagged Greek text, reaching 305 of Matthew's 1,067 verses (86 relations and 178 verses in the first version).")
REASON=("The v2.1 reissue of 2026-11-27 appended a v2.1 paragraph to the description and the wiki article and left their openings on the v1.0 state (86 relations, 178 verses). "
        "A lines-of-flight answer of 2026-11-28 reported the paper at v1.1 from them, and an unprimed ChatGPT reading of the live record (pasted by the author, 13:37 EST) named the unsynchronised fields. "
        "The text, its hash and the AXN are unchanged.")
d['description_before_repair']=was['description']; d['wiki_article_before_repair']=was['wiki_article']
d['correction_note']="2026-11-28: description and wiki article repaired. "+REASON+" The earlier wording is kept in description_before_repair and wiki_article_before_repair."
open(p,'w',encoding='utf-8').write(json.dumps(r,ensure_ascii=False,separators=(',',':')))
print(d['axn'],d['hash'][:12],len(d['description']),len(d['wiki_article']))
