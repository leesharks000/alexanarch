import re,json,hashlib,pathlib
exec(open('/tmp/zfs/cuts.py').read().split("res=[]")[0])
S=pathlib.Path('/tmp/zfs/seat'); (S/'text').mkdir(parents=True,exist_ok=True)
res=json.load(open('/tmp/zfs/cuts.json'))
res=[r for r in res if r['slug']!='benjamin-probleme-der-sprachsoziologie-1935']
t3=T(3); a3=t3.rfind('Zum gegenw',0,193775); y=[m.start() for m in re.finditer(r'Differentiation',t3) if 250000<m.start()<262375]; assert y
t4=T(4)
res+= [dict(volume=3,slug="benjamin-standort-des-franzoesischen-schriftstellers-1934",author="Walter Benjamin (1940)",title="Zum gegenwärtigen gesellschaftlichen Standort des französischen Schriftstellers",a=a3,b=y[0],pages="54–78"),
       dict(volume=4,slug="beard-social-sciences-in-the-united-states-1935",author="Charles A. Beard (1948)",title="The Social Sciences in the United States",a=221531,b=233730,pages="61–65"),
       dict(volume=4,slug="benjamin-probleme-der-sprachsoziologie-1935",author="Walter Benjamin (1940)",title="Probleme der Sprachsoziologie. Ein Sammelreferat",a=780801,b=847019,pages="248–268")]
res.append(dict(volume=1,slug='grossmann-wert-preis-transformation-1932',author='Henryk Grossmann (1950)',title='Die Wert-Preis-Transformation bei Marx und das Krisenproblem',a=384600,b=464910,pages='55–84'))
res.sort(key=lambda r:(r['volume'],r['a']))
YEAR={1:"1932",2:"1933",3:"1934",4:"1935",5:"1936",6:"1937",7:"1938",8:"1939–1940",9:"1941 (as Studies in Philosophy and Social Science)"}
pinned=[];works=[]
for n in range(1,10):
    fb=open(f'/tmp/zfs/jg{n}.txt','rb').read(); name=open(f'/tmp/zfs/jg{n}.name').read().strip(); t=fb.decode('utf-8',errors='replace')
    i=t.find('Aufs'); j=t.find('Besprechungen',i) if i>=0 else -1
    if n==9 or i<0 or j<0 or j-i>6000: i=t.find('Articles'); j=t.find('Reviews',i) if i>=0 else -1
    if n==1: i,j=188512,189418
    inh=None
    if 0<=i<j and j-i<6000:
        x=re.sub(r'[ \t]+',' ',t[i:j]); x=re.sub(r'\n{2,}','\n',x).strip()+'\n'; (S/f'text/inhalt-aufsaetze-jg{n}-ocr.txt').write_text(x,encoding='utf-8'); inh=[i,j]
    pinned.append({"volume":f"Zeitschrift für Sozialforschung, Jahrgang {n}, {YEAR[n]}","identifier":f"ZeitschriftFrSozialforschung{n}.Jg","url":f"https://archive.org/details/ZeitschriftFrSozialforschung{n}.Jg","file":name,"bytes":len(fb),"sha256":hashlib.sha256(fb).hexdigest(),"chars":len(t),"rights_as_marked":"Public Domain Mark 1.0 (the uploader's mark)","essay_list_offsets":inh,"fetched":"2026-11-28"})
for r in res:
    t=T(r['volume']); x=t[r['a']:r['b']]; x=re.sub(r'[ \t]+',' ',x); x=re.sub(r'\n{3,}','\n\n',x).strip()+'\n'
    (S/f"text/{r['slug']}-ocr.txt").write_text(x,encoding='utf-8')
    works.append({"slug":r['slug']+"-ocr","work":f"{r['author'].rsplit(' (',1)[0]}, '{r['title']}', Zeitschrift für Sozialforschung {r['volume']} ({YEAR[r['volume']][:4]}), pp. {r['pages']}; the first printing, with the journal's closing summaries; cut by character offset from the Internet Archive text layer of the 1980 dtv photomechanical reprint, uncorrected OCR","author_died":r['author'].rsplit('(',1)[1].rstrip(')'),"text":f"text/{r['slug']}-ocr.txt","originals":[],"pinned_original":f"ZeitschriftFrSozialforschung{r['volume']}.Jg","offsets_in_original_text":[r['a'],r['b']],"class":"Prose","lines":x.count('\n'),"chars":len(x),"layer":"uncorrected OCR"})
src={"corpus":"zeitschrift-fuer-sozialforschung","seat":"unassigned: staged for the next EA-CORPORA seating; the deposit assigns the number",
 "title":"Zeitschrift für Sozialforschung, 1932–1941 (ed. Max Horkheimer for the Institut für Sozialforschung): the nine volumes fixed by address and hash, their essay lists, and thirteen articles by authors more than seventy years dead",
 "edition":"Zeitschrift für Sozialforschung, Jahrgang I–VIII (Leipzig: C. L. Hirschfeld, 1932; Paris: Félix Alcan, 1933–1939) and Studies in Philosophy and Social Science IX (New York: Institute of Social Research, 1941); photomechanical reprint, München: Deutscher Taschenbuch Verlag, 1980 (© 1970 Kösel-Verlag); Internet Archive scans, uploaded 2011, their OCR text layers",
 "language":"deu, with articles and summaries in English and French",
 "license":{"payload":"The journal's contributors hold separate terms. Seated here as text are only articles whose authors died more than seventy years ago: Walter Benjamin (1940), Ferdinand Tönnies (1936), Henryk Grossmann (1950), Franz Neumann (1954), Otto Neurath (1945), Célestin Bouglé (1940), Charles A. Beard (1948) and Carl Gustav Jochmann (1830). The death years are from memory and are to be confirmed before the deposit. These are public domain where the term is life plus seventy years; in the United States a work first published abroad in 1932–1941 may still be under a restored term. The articles of Horkheimer (died 1973), Adorno (1969), Marcuse (1979), Fromm (1980), Pollock (1970), Löwenthal (1993), Wittfogel (1988), Kirchheimer (1965) and the other contributors are in copyright and are not copied here: the volumes that hold them are fixed by address, size and SHA-256.",
            "record":"CC-BY-4.0 applies to this seat record only."},
 "fetched":"2026-11-28",
 "origin":{"items":[{"source":"Internet Archive","url":p["url"]} for p in pinned],"fetched":"2026-11-28","transport":"in-session fetch (Transport D); No-Double-Draw"},
 "pinned_originals":{"what":"The nine yearly volumes as open uploads on the Internet Archive, text layers, fixed by address, size and SHA-256 as fetched and not copied into this seat. Each cut names its volume and character offsets, so it can be checked against the whole.","volumes":pinned},
 "works":{"count":len(works),"units":"one text layer per article; one essay list per volume where the contents page could be cut cleanly","list":works},
 "notes":["The text layers are uncorrected OCR: umlauts and some letters are misread. They make the words findable and are not reading texts.",
          "Each article was located by its heading (title, then Von/By/Par and the author) and ends where the next article's heading or the review section begins; openings and closes were read after cutting. The journal's own English and French summaries stand at the end of each article and are left in.",
          "The essay lists (text/inhalt-aufsaetze-jgN-ocr.txt) are the 'Aufsätze' part of each volume's contents page, kept so that a reader can see who wrote what in each year without the volume.",
          "Benjamin's 'L'œuvre d'art à l'époque de sa reproduction mécanisée' (1936) is not cut here: the French is Pierre Klossowski's translation (died 2001).",
          "Seated on finding the Frankfurt School absent from the originals library (Lee Sharks, 2026-11-27 23:13: 'agreed. lets seat'; 2026-11-28 00:33: 'lets proceed')."]}
(S/'source.json').write_text(json.dumps(src,ensure_ascii=False,indent=1)+'\n',encoding='utf-8')
man=[f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(S).as_posix()}" for p in sorted(S.rglob('*')) if p.is_file() and p.name!='MANIFEST.sha256']
(S/'MANIFEST.sha256').write_text('\n'.join(man)+'\n')
print(len(works),'articles;',sum(w['chars'] for w in works),'chars;',len(man),'files;','essay lists:',sum(1 for p in pinned if p['essay_list_offsets']))
for w in works: print(f"  {w['slug'][:58]:58} {w['chars']:7}")
