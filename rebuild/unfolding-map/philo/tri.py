import re,glob,unicodedata as U,sys
C='/home/claude/repos/alexanarch/data/corpora/'
def N(t):
    t=U.normalize('NFD',t); return ''.join(c for c in t if not U.combining(c)).lower().replace('ς','σ')
def load(pat):
    out=[]
    for f in sorted(glob.glob(C+pat)):
        prev=None; book=1
        for i,l in enumerate(open(f,encoding='utf-8'),1):
            if '\t' not in l: continue
            r,t=l.rstrip('\n').split('\t',1)
            m=re.search(r'(\d+)$',r)
            if m:
                k=int(m.group(1))
                if prev is not None and k<prev-20: book+=1
                prev=k
            # cut the edition's apparatus where it is run into the line: keep text up to first ' \d+ ' followed by latin-letter sigla is unreliable; keep whole, flag latin
            out.append((r,book,t,N(t)))
    return out
PH=load('philo/text/*.txt'); JO=load('josephus/text/*.txt'); LX=load('lxx-swete/text/*.txt'); NT=load('gnt-nestle1904/text/*.txt')
def find(us,*rx):
    return [(r,b,t) for r,b,t,x in us if all(re.search(p,x) for p in rx)]
def snip(t,rx,w=110):
    x=N(t); m=re.search(rx,x)
    if not m: return t[:2*w]
    return t[max(0,m.start()-w):m.end()+w].replace('\n',' ')
def rep(name,*rx,show=4,key=None):
    p=find(PH,*rx); j=find(JO,*rx); l=find(LX,*rx); n=find(NT,*rx)
    print(f'\n## {name}: Philo {len(p)} | Josephus {len(j)} | LXX {len(l)} {[r for r,_,_ in l][:5]} | NT {len(n)} {[r for r,_,_ in n][:6]}')
    for r,b,t in p[:show]: print(f'   {r} (book {b}): …{snip(t,key or rx[0])}…')
rep('M1 Jerusalem = vision of peace', r'ορασισ[^.]{0,20}ειρηνησ|ειρηνησ[^.]{0,20}ορασισ')
rep('M1 city of God', r'θεου πολισ|πολισ[^.]{0,12}του θεου|πολιν[^.]{0,12}θεου',show=6)
rep('M2 blind wealth', r'πλουτ', r'τυφλ', show=5, key=r'τυφλ[^.]{0,40}πλουτ|πλουτ[^.]{0,40}τυφλ')
rep('M3a beginning and end', r'αρχη[ν]? (τε )?και τελοσ|αρχη[^.]{0,6}και[^.]{0,6}τελοσ',show=6)
rep('M3b equal + first + last', r'\bισο', r'πρωτ', r'εσχατ|υστατ|τελευται', show=5, key=r'\bισο')
rep('M3b isotes sections in Quis heres', r'ισοτητ')
rep('M3c wage same day', r'μισθ', r'αυθημερ', show=4, key=r'αυθημερ')
rep('M4 eleven/twelve stars, zodiac', r'αστερ', r'ενδεκα|δωδεκατ|ζωδια', show=6, key=r'ενδεκα|δωδεκατ|ζωδια')
rep('M5 mother wisdom of the Logos', r'μητροσ[^.]{0,40}σοφιασ|σοφιασ[^.]{0,40}μητροσ', show=4)
rep('M5 conceive from God, virgin', r'παρθεν', r'κυοφορ|εγκυμον|τικτ|σπειρ', r'θεο', show=5, key=r'παρθεν')
rep('M6 coin + image/stamp', r'νομισμα', r'εικον|εικων|χαρακτηρ|σφραγι', show=6, key=r'νομισμα')
rep('M7 Prov 3:11-12', r'παιδειασ', r'ελεγχ|μαστιγοι', show=3, key=r'ον γαρ')
rep('M8 Sodom + Egypt', r'σοδομ', r'αιγυπτ', show=4, key=r'σοδομ')
rep('M8 Egypt = body', r'αιγυπτ[^.]{0,60}σωμα|σωμα[^.]{0,60}αιγυπτ', show=3)
rep('M8 Sodom = blindness/barrenness', r'σοδομ[^.]{0,120}(τυφλωσ|στειρωσ)|(τυφλωσ|στειρωσ)[^.]{0,120}σοδομ', show=3)
rep('M9 God swears by himself', r'κατ εμαυτου ωμοσα|καθ εαυτου ωμοσ|ομνυσι[^.]{0,30}καθ εαυτου', show=3)
