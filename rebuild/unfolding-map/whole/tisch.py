import re,collections,unicodedata
D='/tmp/fetch/tischendorf-data/word-per-line/2.8/Unicode/'
def load(code):
    V=collections.OrderedDict()
    for l in open(D+code+'.txt',encoding='utf8'):
        f=l.split()
        if len(f)<8: continue
        m=re.match(r'(\d+):(\d+)\.',f[1]); 
        if not m: continue
        key=(int(m.group(1)),int(m.group(2)))
        # fields: book ref brk word1 word2 tag strong lemma ! lemma
        tag=f[5]; lemma=unicodedata.normalize('NFC',f[7])
        V.setdefault(key,[]).append((lemma,tag,f[3]))
    return V
