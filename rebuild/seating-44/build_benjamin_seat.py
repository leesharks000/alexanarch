import json,re,hashlib,pathlib,shutil,datetime
from bs4 import BeautifulSoup, NavigableString, Comment
S=pathlib.Path('/tmp/benj/seat'); 
for d in ('original/wikisource','original/archive-org','text'): (S/d).mkdir(parents=True,exist_ok=True)
revs=json.load(open('/tmp/benj/ws/revs.json'))
META={ # title -> slug, work description, class
 "Einbahnstraße":("einbahnstrasse-1928","Walter Benjamin, Einbahnstraße (Berlin: Ernst Rowohlt, 1928), the first edition; German Wikisource transcription from the scan, proofread ('fertig')"),
 "Das Dornröschen":("dornroeschen-1911","'Das Dornröschen', Der Anfang. Vereinigte Zeitschriften der Jugend, Heft 3 (1911), pp. 51–54; German Wikisource transcription"),
 "Das Leben der Studenten":("leben-der-studenten-1915","'Das Leben der Studenten', Der Neue Merkur 2 (1915), pp. 727–737; German Wikisource transcription"),
 "Die Kaktushecke":("kaktushecke-1933","'Die Kaktushecke', Das Unterhaltungsblatt der Vossischen Zeitung, Nr. 8, 8 January 1933, pp. 1–2; German Wikisource transcription"),
 "Kierkegaard (Benjamin)":("kierkegaard-1933","'Kierkegaard. Das Ende des philosophischen Idealismus', Literarische Umschau, Nr. 14, Beilage der Vossischen Zeitung, 2 April 1933, p. 1 (review of Adorno's Kierkegaard book); German Wikisource transcription"),
 "Ein Weihnachtsengel":("bk-weihnachtsengel-1932","Berliner Kindheit um neunzehnhundert: 'Ein Weihnachtsengel', Vossische Zeitung, Nr. 357, 24 December 1932; German Wikisource transcription"),
 "Das Fieber":("bk-fieber-1933","Berliner Kindheit um neunzehnhundert: 'Das Fieber', Vossische Zeitung, Nr. 76, 17 March 1933; German Wikisource transcription"),
 "Die Mummerehlen":("bk-mummerehlen-1933","Berliner Kindheit um neunzehnhundert: 'Die Mummerehlen' (as Detlef Holz), Vossische Zeitung, Nr. 123, 5 May 1933; German Wikisource transcription"),
 "Zwei Rätselbilder":("bk-raetselbilder-1933","Berliner Kindheit um neunzehnhundert: 'Zwei Rätselbilder' (as Detlef Holz), Vossische Zeitung, Nr. 164, 16 June 1933; German Wikisource transcription"),
 "Loggien":("bk-loggien-1933","Berliner Kindheit um neunzehnhundert: 'Loggien' (as Detlef Holz), Vossische Zeitung, Nr. 210, 1 August 1933; German Wikisource transcription"),
 "Der Mond (Benjamin)":("bk-mond-1933","Berliner Kindheit um neunzehnhundert: 'Der Mond' (as Detlef Holz), Vossische Zeitung, Nr. 248, 8 September 1933; German Wikisource transcription"),
 "Schmöker":("bk-schmoeker-1933","Berliner Kindheit um neunzehnhundert: 'Schmöker' (as Detlef Holz), Vossische Zeitung, Nr. 257, 17 September 1933; German Wikisource transcription"),
 "Das Kunstwerk im Zeitalter seiner technischen Reproduzierbarkeit (Dritte Fassung)":("kunstwerk-dritte-fassung","Das Kunstwerk im Zeitalter seiner technischen Reproduzierbarkeit, third version (written 1935–1939), as printed in Gesammelte Schriften I.2, ed. Rolf Tiedemann and Hermann Schweppenhäuser (Frankfurt am Main: Suhrkamp, 1980), pp. 471–508; German Wikisource transcription, proofread ('fertig')"),
}
def html2text(b):
    s=BeautifulSoup(b,'lxml'); c=s.select_one('div.mw-parser-output')
    for sel in ('div.ws-noexport','div.noprint','style','script','table.hiddenStructure','span.mw-editsection','figure','span.mw-cite-backlink','div.mw-references-wrap > h2','link','meta'):
        for e in c.select(sel): e.decompose()
    for e in c.select('span.PageNumber, span.pagenum, span.seitennummer'):
        t=re.sub(r'\s+',' ',e.get_text()).strip().strip('[]'); e.replace_with(NavigableString(f' [S. {t}] ' if t else ' '))
    for e in c.select('sup.reference'):
        t=re.sub(r'[\[\]\s]','',e.get_text()); e.replace_with(NavigableString(f'[{t}]'))
    for br in c.find_all('br'): br.replace_with(NavigableString('\n'))
    out=[]; BL={'p','h1','h2','h3','h4','li','dd','dt','div','blockquote','td','th','center','section','ol','ul','dl','table','tr','tbody'}
    def flush(buf,head=False):
        t=''.join(buf); t='\n'.join(re.sub(r'[ \t\u00a0]+',' ',x).strip() for x in t.split('\n')); t=re.sub(r'\n{2,}','\n',t).strip()
        if t: out.append('# '+t if head else t)
        buf.clear()
    def walk(node):
        buf=[]
        for ch in node.children:
            if isinstance(ch,Comment): continue
            if isinstance(ch,NavigableString): buf.append(str(ch))
            elif ch.name in BL: flush(buf); walk(ch)
            elif ch.find(list(BL)): flush(buf); walk(ch)
            else: buf.append(ch.get_text())
        flush(buf, node.name in ('h1','h2','h3','h4'))
    walk(c)
    return '\n\n'.join(out)+'\n'
works=[]; items=[]
for title,(slug,desc) in META.items():
    o=revs[title]; n=o['n']; rev=o['revid']
    hb=open(f'/tmp/benj/ws/{n:02d}.html','rb').read(); wb=open(f'/tmp/benj/ws/{n:02d}.wiki','rb').read()
    assert b'Wikimedia Error' not in hb[:300] and b'Wikimedia Error' not in wb[:300], title
    (S/f'original/wikisource/{slug}.rev{rev}.html').write_bytes(hb); (S/f'original/wikisource/{slug}.rev{rev}.wiki').write_bytes(wb)
    t=html2text(hb); (S/f'text/{slug}.txt').write_text(t,encoding='utf-8')
    url='https://de.wikisource.org/w/index.php?title='+title.replace(' ','_')+f'&oldid={rev}'
    items.append({"source":"German Wikisource (de.wikisource.org)","url":url,"revision":int(rev)})
    works.append({"slug":slug,"work":desc,"text":f"text/{slug}.txt","originals":[f"original/wikisource/{slug}.rev{rev}.html",f"original/wikisource/{slug}.rev{rev}.wiki"],"class":"Prose","lines":t.count('\n'),"chars":len(t)})
# the Werkverzeichnis, as a finding aid only
o=revs["Walter Benjamin/Werkverzeichnis"]; (S/f"original/wikisource/werkverzeichnis.rev{o['revid']}.wiki").write_bytes(open(f"/tmp/benj/ws/{o['n']:02d}.wiki",'rb').read())
# Internet Archive OCR
IA=[("deutsche-menschen-1936","BenjaminDeutscheMenschen_djvu.txt","DeutscheMenschen-EineFolgeVonBriefen","Deutsche Menschen. Eine Folge von Briefen. Auswahl und Einleitungen von Detlef Holz [Walter Benjamin] (Luzern: Vita Nova Verlag, 1936), the first edition; Internet Archive scan, its OCR text layer, uncorrected"),
    ("tableaux-parisiens-1923","BenjaminTableauxParisien_djvu.txt","CharlesBaudelaireTableauxParisiens","Charles Baudelaire, Tableaux Parisiens. Deutsche Übertragung mit einem Vorwort über die Aufgabe des Übersetzers von Walter Benjamin (Heidelberg: Richard Weißbach, 1923), French and German, with 'Die Aufgabe des Übersetzers'; Internet Archive scan, its OCR text layer, uncorrected")]
for slug,f,ident,desc in IA:
    b=open(f'/tmp/benj/ia/{f}','rb').read(); (S/f'original/archive-org/{f}').write_bytes(b); t=b.decode('utf-8',errors='replace'); t=re.sub(r'[ \t]+',' ',t); t=re.sub(r'\n{3,}','\n\n',t).strip()+'\n'
    (S/f'text/{slug}-ocr.txt').write_text(t,encoding='utf-8')
    items.append({"source":"Internet Archive","url":f"https://archive.org/details/{ident}","file":f"https://archive.org/download/{ident}/{f}","rights_as_marked":"Public Domain Mark 1.0"})
    works.append({"slug":slug+"-ocr","work":desc,"text":f"text/{slug}-ocr.txt","originals":[f"original/archive-org/{f}"],"class":"Prose","lines":t.count('\n'),"chars":len(t),"layer":"uncorrected OCR"})
# Zur Kritik der Gewalt from the journal volume
f="Archiv_fuer_Sozialwissenschaft_und_Sozialpolitik_47.1920-21_djvu.txt"; b=open(f'/tmp/benj/ia/{f}','rb').read(); (S/f'original/archive-org/{f}').write_bytes(b); a=b.decode('utf-8',errors='replace')
i=a.index('809 \n\n\nZur Kritik der Gewalt.'); 
json.dump({'start':i},open('/tmp/benj/kg.json','w'))
open('/tmp/benj/kg_tail.txt','w',encoding='utf-8').write(a[i+95000:i+125000])
print(len(works),'works so far;',sum(w['chars'] for w in works),'chars'); 
for w in works: print(f"  {w['slug']:34} {w['chars']:7}")
json.dump({'works':works,'items':items},open('/tmp/benj/partial.json','w'),ensure_ascii=False,indent=1)
j=a.index('mag die waltende heißen.',i)+len('mag die waltende heißen.')
kg=a[i:j]; kg=re.sub(r'[ \t]+',' ',kg); kg=re.sub(r'\n{3,}','\n\n',kg).strip()+'\n'
(S/'text/zur-kritik-der-gewalt-1921-ocr.txt').write_text(kg,encoding='utf-8')
items.append({"source":"Internet Archive","url":"https://archive.org/details/archiv-fur-sozialwissenschaft-und-sozialpolitik-47","file":"https://archive.org/download/archiv-fur-sozialwissenschaft-und-sozialpolitik-47/Archiv%20f%C3%BCr%20Sozialwissenschaft%20und%20Sozialpolitik%2047.1920-21_djvu.txt","rights_as_marked":"none marked on the item; the volume was printed in 1920/1921"})
works.append({"slug":"zur-kritik-der-gewalt-1921-ocr","work":"'Zur Kritik der Gewalt', Archiv für Sozialwissenschaft und Sozialpolitik 47 (Tübingen: J. C. B. Mohr (Paul Siebeck), 1920/1921), pp. 809–832, the first printing; Internet Archive scan of the volume, its OCR text layer, uncorrected, the essay cut out by character offset","text":"text/zur-kritik-der-gewalt-1921-ocr.txt","originals":[f"original/archive-org/{f}"],"class":"Prose","lines":kg.count('\n'),"chars":len(kg),"layer":"uncorrected OCR","offsets_in_original_text":[i,j]})
# ---- Gesammelte Schriften (Suhrkamp), Internet Archive open uploads: text-only cuts; the whole volumes pinned by hash, not rehosted
GS='/tmp/benj/gs/'; pinned=[]
EDS={1:[("Editorischer Bericht",1683148),("Anmerkungen der Herausgeber",1796913)],2:[("Anmerkungen der Herausgeber",1850412)],3:[],4:[("Anmerkungen des Herausgebers",1844425)],5:[("Anmerkungen des Herausgebers",2513634)],6:[("Anmerkungen der Herausgeber",1392418)],7:[]}
for v in range(1,8):
    fb=open(GS+f'BenjaminGs{v}_djvu.txt','rb').read()
    pinned.append({"volume":f"Gesammelte Schriften Bd. {v}","identifier":f"GesammelteSchriftenBd.{v}","url":f"https://archive.org/details/GesammelteSchriftenBd.{v}","file":f"https://archive.org/download/GesammelteSchriftenBd.{v}/BenjaminGs{v}_djvu.txt","bytes":len(fb),"sha256":hashlib.sha256(fb).hexdigest(),"chars":len(fb.decode('utf-8',errors='replace')),"editors_sections_begin_at_char":[{"heading":h,"offset":o} for h,o in EDS[v]],"fetched":"2026-11-27"})
g=open(GS+'BenjaminGs1_djvu.txt','rb').read().decode('utf-8',errors='replace')
A=g.index('Der Begriff \n\nder Kunstkritik in der \n\ndeutschen Romantik'); B=273685; C=459804; D=g.index('\nErster Band. Erster Teil \n\nDer Begriff der Kunstkritik in der deutsdien'); E=g.index('Das Kunstwerk im Zeitalter seiner \ntechnischen Reproduzierbarkeit \n\n\n\n(Erste Fassung)'); F=g.index('Charles Baudelaire \n\nEin Lyriker im Zeitalter.des'); G=1532662; H=1562054; I_=1584808; J=1683148
CUTS=[("gs1-begriff-der-kunstkritik","Der Begriff der Kunstkritik in der deutschen Romantik (1920)",A,B,"7–122"),
      ("gs1-goethes-wahlverwandtschaften","Goethes Wahlverwandtschaften (1924–25)",B,C,"123–201"),
      ("gs1-ursprung-des-deutschen-trauerspiels","Ursprung des deutschen Trauerspiels (1928)",C,D,"203–430"),
      ("gs1-kunstwerk-erste-und-dritte-fassung","Das Kunstwerk im Zeitalter seiner technischen Reproduzierbarkeit, first and third versions",E,F,"431–508"),
      ("gs1-baudelaire-second-empire-und-motive","Charles Baudelaire. Ein Lyriker im Zeitalter des Hochkapitalismus: Das Paris des Second Empire bei Baudelaire; Über einige Motive bei Baudelaire",F,G,"509–653"),
      ("gs1-zentralpark","Zentralpark",G,H,"655–690"),
      ("gs1-ueber-den-begriff-der-geschichte","Über den Begriff der Geschichte (1940), the eighteen theses with A and B",H,I_,"691–704"),
      ("gs1-anhang","Anhang: Selbstanzeige der Dissertation; L'œuvre d'art à l'époque de sa reproduction mécanisée (1936, French); Notes sur les Tableaux parisiens de Baudelaire",I_,J,"705–748")]
for slug,desc,a0,a1,pp in CUTS:
    assert a0<a1,(slug,a0,a1)
    x=g[a0:a1]; x=re.sub(r'[ \t]+',' ',x); x=re.sub(r'\n{3,}','\n\n',x).strip()+'\n'
    (S/f'text/{slug}-ocr.txt').write_text(x,encoding='utf-8')
    works.append({"slug":slug+"-ocr","work":desc+f"; Benjamin's text only, cut by character offset from Gesammelte Schriften I, ed. Rolf Tiedemann and Hermann Schweppenhäuser (Frankfurt am Main: Suhrkamp, 1974; Taschenbuch 1991), pp. {pp}; Internet Archive OCR text layer, uncorrected, umlauts largely lost in the OCR","text":f"text/{slug}-ocr.txt","originals":[],"pinned_original":"GesammelteSchriftenBd.1/BenjaminGs1_djvu.txt","offsets_in_original_text":[a0,a1],"class":"Prose","lines":x.count('\n'),"chars":len(x),"layer":"uncorrected OCR"})

VOLS=[(2,2093,1848631,"gs2-aufsaetze-essays-vortraege","Gesammelte Schriften II: Aufsätze, Essays, Vorträge (early writings; metaphysical and historical-philosophical studies, with 'Über Sprache überhaupt und über die Sprache des Menschen', 'Zur Kritik der Gewalt', 'Theologisch-politisches Fragment'; the literary and aesthetic essays, with Kafka, Kraus, Proust, the Surrealism essay, 'Der Erzähler', 'Der Autor als Produzent', 'Eduard Fuchs'; lectures; encyclopaedia articles)","7–813"),
      (3,1790,1352849,"gs3-kritiken-und-rezensionen","Gesammelte Schriften III: Kritiken und Rezensionen, 1912–1940, with the appendix","9–602"),
      (4,2037,1844425,"gs4-kleine-prosa-baudelaire-uebertragungen","Gesammelte Schriften IV: the Baudelaire translations with 'Die Aufgabe des Übersetzers', Einbahnstraße, Deutsche Menschen, Berliner Kindheit um Neunzehnhundert, Denkbilder, satires and glosses, reports, illustrated essays, Hörmodelle, stories, miscellanies","7–880"),
      (5,80867,2513634,"gs5-das-passagen-werk","Gesammelte Schriften V: Das Passagen-Werk (the two exposés, German and French; Aufzeichnungen und Materialien, convolutes A–r; Erste Notizen; Frühe Entwürfe), without the editor's introduction","45–1063"),
      (6,2127,1392418,"gs6-fragmente-autobiographische-schriften","Gesammelte Schriften VI: Fragmente vermischten Inhalts; Autobiographische Schriften (Lebensläufe, notebooks, Moskauer Tagebuch, Berliner Chronik); appendix with the Protokolle zu Drogenversuchen","7–621"),
      (7,2419,1193898,"gs7-nachtraege","Gesammelte Schriften VII: Nachträge (early writings, sonnets, the radio pieces for children, literary radio talks, stories and riddles, 'Das kalte Herz', the Kunstwerk essay's second version, Berliner Kindheit in the Fassung letzter Hand, Verzeichnis der gelesenen Schriften), without the editors' bibliography","9–476")]
EDN={1:"Rolf Tiedemann and Hermann Schweppenhäuser",2:"Rolf Tiedemann and Hermann Schweppenhäuser",3:"Hella Tiedemann-Bartels",4:"Tillman Rexroth",5:"Rolf Tiedemann",6:"Rolf Tiedemann and Hermann Schweppenhäuser",7:"Rolf Tiedemann and Hermann Schweppenhäuser, with Christoph Gödde, Henri Lonitz and Gary Smith"}
for v,a0,a1,slug,desc,pp in VOLS:
    gv=open(GS+f'BenjaminGs{v}_djvu.txt','rb').read().decode('utf-8',errors='replace'); assert 0<a0<a1<len(gv)
    x=gv[a0:a1]; x=re.sub(r'[ \t]+',' ',x); x=re.sub(r'\n{3,}','\n\n',x).strip()+'\n'
    (S/f'text/{slug}-ocr.txt').write_text(x,encoding='utf-8')
    works.append({"slug":slug+"-ocr","work":desc+f"; Benjamin's text only, one cut by character offset from the volume (ed. {EDN[v]}; Frankfurt am Main: Suhrkamp), pp. {pp}; Internet Archive OCR text layer, uncorrected","text":f"text/{slug}-ocr.txt","originals":[],"pinned_original":f"GesammelteSchriftenBd.{v}/BenjaminGs{v}_djvu.txt","offsets_in_original_text":[a0,a1],"class":"Prose","lines":x.count('\n'),"chars":len(x),"layer":"uncorrected OCR"})
for p_ in pinned:
    v=int(p_["identifier"][-1])
    if v==3: p_["editors_sections_begin_at_char"]=[{"heading":"Anmerkungen der Herausgeberin","offset":1352849}]
    if v==5: p_["editors_sections_begin_at_char"]=[{"heading":"Einleitung des Herausgebers (front, to offset 80867)","offset":2056},{"heading":"Anmerkungen des Herausgebers","offset":2513634}]
    if v==7: p_["editors_sections_begin_at_char"]=[{"heading":"Bibliographie der zu Lebzeiten gedruckten Arbeiten","offset":1193898},{"heading":"Anmerkungen der Herausgeber","offset":1305810}]
src={"corpus":"benjamin","seat":"unassigned: staged for the next EA-CORPORA seating; the deposit assigns the number",
 "title":"Walter Benjamin in German, 1911–1940: Über den Begriff der Geschichte, Ursprung des deutschen Trauerspiels, the Baudelaire studies, Einbahnstraße, Zur Kritik der Gewalt, Die Aufgabe des Übersetzers with the Tableaux Parisiens, Deutsche Menschen, Das Kunstwerk im Zeitalter seiner technischen Reproduzierbarkeit (third version), Das Leben der Studenten, and ten pieces from periodicals, seven of them from Berliner Kindheit um neunzehnhundert",
 "edition":"; ".join(w["work"] for w in works),
 "language":"deu (the Tableaux Parisiens volume also carries Baudelaire's French)",
 "license":{"payload":"Walter Benjamin died on 26 September 1940; his writings are in the public domain where the term is the author's life plus seventy years. Fourteen of the sixteen items were first printed between 1911 and 1936. The third version of the Kunstwerk essay was first printed after his death; it is held here as German Wikisource transcribes it from Gesammelte Schriften I.2 (Suhrkamp, 1980), text only, with the editors' additions marked there in square brackets. German Wikisource transcriptions are offered under CC BY-SA 4.0. The Internet Archive items for Deutsche Menschen and the Tableaux Parisiens carry the Public Domain Mark 1.0; the Archiv volume carries no mark and was printed in 1920/1921. Each original is held as fetched.",
            "record":"CC-BY-4.0 applies to this seat record only. Text layers derived from German Wikisource pages carry that source's CC BY-SA 4.0."},
 "fetched":"2026-11-27",
 "origin":{"items":items,"fetched":"2026-11-27","transport":"in-session fetch (Transport D); No-Double-Draw. Wikisource pages fetched once each through the ordinary page route at a pinned revision, three seconds apart; the API was rate-limited and was not used."},
 "works":{"count":len(works),"units":"one text layer per item, beside the page or scan text it was made from","list":works},
 "pinned_originals":{"what":"The seven volumes of Gesammelte Schriften as open uploads on the Internet Archive (uploaded 2011), text layers. They carry the editors' reports and notes, which are in copyright (Suhrkamp Verlag; Rolf Tiedemann, Hermann Schweppenhäuser and the other editors). They are fixed here by address, size and SHA-256 as fetched, and are not copied into this seat. Each cut in this seat names its volume and its character offsets, so a cut can be checked against the whole.","volumes":pinned},
 "notes":["Text layers from Wikisource are the rendered page with the header box, images and edit links removed; page breaks of the printed source are kept as [S. n] and footnote calls as [n], with the notes at the end. Each layer was checked against its page by character count.",
          "The three Internet Archive layers are uncorrected OCR and are marked so. They are seated so the words can be found; they are not reading texts.",
          "Not seated here, with the reason: 'Die Waffen von morgen' (Vossische Zeitung, 29 June 1925), which the Wikisource author page lists and whose own page attributes to Dora Sophie Benjamin (died 1964). Volume I of the Gesammelte Schriften is cut into eight text layers of Benjamin's words (the theses on history, the Baudelaire studies, Zentralpark, the Trauerspiel book, the Wahlverwandtschaften essay, the dissertation, the Kunstwerk essay's first and third versions, and the appendix). Volumes II to VII are each one cut of Benjamin's text, from the first work to the start of the editors' section; volume V leaves out the editor's introduction at the front, and volume VII stops before the editors' bibliography. Part-title and contents pages that fall inside a cut are left in. Two things inside the cuts are other hands: the Passagen-Werk is in large part Benjamin's excerpts from other authors, and the drug protocols in volume VI include records written by Ernst Joël, Fritz Fränkel and Ernst Bloch. Cutting volumes II to VII work by work, as volume I is, is owed.",
          "original/wikisource/werkverzeichnis.rev%s.wiki is German Wikisource's list of Benjamin's works after the Gesammelte Schriften, kept as a finding aid." % revs["Walter Benjamin/Werkverzeichnis"]["revid"],
          "Seated during the Revelation First and Critique of Pure Inference work of November 2026, on finding the Frankfurt School absent from the originals library (Lee Sharks, 2026-11-27 23:10: 'i think we legitimate havent seated the frankfurt school - if so thats a large whoops'; 23:13: 'agreed. lets seat')."]}

(S/'source.json').write_text(json.dumps(src,ensure_ascii=False,indent=1)+'\n',encoding='utf-8')
man=[]
for p in sorted(S.rglob('*')):
    if p.is_file() and p.name!='MANIFEST.sha256': man.append(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(S).as_posix()}")
(S/'MANIFEST.sha256').write_text('\n'.join(man)+'\n')
print(len(works),'works;',sum(w['chars'] for w in works),'chars;',len(man),'files')
