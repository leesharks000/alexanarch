import json,re,unicodedata,collections,itertools,glob,os
from tisch import load
nf=lambda s:unicodedata.normalize('NFC',s)
D='/tmp/fetch/tischendorf-data/word-per-line/2.8/Unicode/'
books=[os.path.basename(f)[:-4] for f in sorted(glob.glob(D+'*.txt'))]
NT={b:load(b) for b in books}; RE=NT['RE']; MT=NT['MT']
def span(V,s):
    """'3:17-18' or '27:6-8' or '20:1-16' or '13:14-17; 18:3' -> list of keys"""
    out=[]
    for part in re.split(r'\s*[;+]\s*',s):
        m=re.match(r'(\d+):(\d+)(?:-(\d+))?$',part.strip()); c=int(m.group(1)); a=int(m.group(2)); b=int(m.group(3) or a)
        out+=[(c,v) for v in range(a,b+1) if (c,v) in V]
    return out
def lem(V,keys): return {l for k in keys for l,_,_ in V[k]}
# hand rows: (rev, matt, lemmas required in both, lemmas required in Revelation only, in Matthew only, relation in Revelation, relation in Matthew, move, strand/bearer, standing)
H=[
("22:12-13","20:1-16",["μισθός","ἀποδίδωμι","πρῶτος","ἔσχατος"],[],[],"the speaker comes with his wage, to give to each as his work is; he is first and last","a householder pays the last as the first, beginning from the last","STAGE the collision; ENACT the title","wage","held under seal: together 6 of 6, apart 0 of 6 (2AG, 2AH)"),
("6:6","20:2",["δηνάριον"],[],[],"a measure of wheat for a denarius","a denarius for the day","KEEP the price; the bearer exchanged (rider, householder)","3 rider","read; δηνάριον outside Revelation in the Gospels only (2AO)"),
("6:5","11:29-30",["ζυγός"],[],[],"the rider holds a balance","take my yoke; my yoke is kind","the bearer exchanged (rider, teacher); the sign turned (dearth, rest)","3 rider","read; ζυγός in the Gospels in Matthew only (2AO)"),
("3:17-18","19:21-23",["πλούσιος"],["ἀγοράζω"],["πωλέω","θησαυρός"],"to the rich one who is poor: buy from me, to be rich","to the rich one: sell, give to the poor, have treasure","OPPOSE the act (buy, sell)","3 speaker","read; list complete (2AO)"),
("3:21","19:28",["καθίζω","θρόνος"],[],[],"I will give the conqueror to sit with me on my throne","you who followed shall sit on twelve thrones","KEEP; the promise said to followers","1 speaker","read (2X, 2AO)"),
("3:21","20:23",["καθίζω","δίδωμι"],[],[],"I will give to sit","to sit is not mine to give","TURN the sign","1 speaker","read; construction exclusive (2AK)"),
("3:19","26:48",["φιλέω"],["ἐλέγχω"],["κρατέω"],"as many as I love I reprove and chasten","whomever I kiss, he it is: seize him","MOVE the line to the adversary's mouth; its object the teacher","speaker","read; construction exclusive (2AK)"),
("5:9","27:6-8",["ἀγοράζω","αἷμα"],[],[],"the Lamb bought for God by his blood","the chief priests bought a field with the price of blood","EXCHANGE the buyer across the sides","3 Lamb","read; the only two places (2AO)"),
("13:17","21:12",["ἀγοράζω","πωλέω"],[],[],"none may buy or sell but who has the mark","he cast out all who sold and bought in the temple","OPPOSE (the market closed to all but its own; the market cast out)","3 adversary","read; list complete (2AO)"),
("13:14-17","22:19-21",["εἰκών"],[],["δηνάριον"],"the image all must bow to, and the mark for buying","whose image is this, on the coin","KEEP the image and the coin; the claim divided (Caesar's, God's)","3 adversary","read; list complete (2AO)"),
("18:11-12","13:45-46",["ἔμπορος","μαργαρίτης"],[],[],"the merchants weep: no one buys their pearls","a merchant sells all and buys one pearl","TURN the sign","3 adversary","read; exclusive (2AO)"),
("20:2","26:50",["κρατέω"],[],[],"the angel seized the dragon","they laid hands on Jesus and seized him","EXCHANGE the patient (adversary, teacher)","custody","2AI.3 held on one instrument, not repeated (2AM)"),
("20:2","27:2",["δέω"],[],[],"and bound him","having bound him they led him away","EXCHANGE the patient","custody","as above"),
("13:10","26:52",["μάχαιρα"],["ἀποκτείνω"],["ἀπόλλυμι"],"who kills by the sword must by the sword be killed","all who take the sword shall perish by the sword","KEEP, as the teacher's saying","2","read tonight"),
("6:4","10:34",["εἰρήνη","μάχαιρα"],[],[],"it was given him to take peace from the earth; a great sword was given","I came not to cast peace on the earth but a sword","the bearer exchanged (rider, teacher, in the first person)","2 rider","read (3.4, 2AN)"),
("1:18","16:18-19",["ᾅδης","κλείς"],[],["δέω","λύω"],"I have the keys of death and of Hades","the gates of Hades; I will give you the keys; bind and loose","EXCHANGE the holder (speaker, follower)","4 speaker","read tonight"),
("3:9","4:9-10",["προσκυνέω","Σατανᾶς"],[],[],"those of Satan's synagogue made to bow before the faithful","Satan asks to be bowed to; begone, Satan","EXCHANGE (who bows to whom)","letters","read (2AL.2)"),
("2:10","4:1",["διάβολος","πειράζω"],[],[],"the devil will throw some of you into prison to be tried","led up to be tried by the devil","EXCHANGE the patient (faithful, teacher)","letters","read (2AL.2)"),
("6:2","27:29",["στέφανος"],[],[],"a crown was given him, and he went out conquering","they plaited a crown of thorns and set it on his head","TURN the sign; the patient the teacher","1 rider","read tonight"),
("14:15","13:39",["θερισμός","ἄγγελος"],[],[],"an angel cries: reap, the harvest of the earth is ripe","the harvest is the end of the age; the reapers are angels","KEEP, as a likeness explained","harvest","read tonight"),
("22:12","16:27",["ἀποδίδωμι","ἕκαστος"],[],[],"to give to each as his work is","he will give to each according to his doing","KEEP, as the teacher's saying of the Son of Man","wage","read tonight"),
("20:11-12","25:31-32",["θρόνος"],[],[],"a great white throne; the dead judged by their works","he will sit on the throne of his glory; the nations gathered and parted","KEEP; told as a scene of sheep and goats","judgment","read tonight"),
("1:16-17","17:2-7",["ἥλιος","πίπτω","φοβέω"],[],[],"his face as the sun; I fell as dead; he laid his hand on me: fear not","his face shone as the sun; they fell; he touched them: fear not","the seer's part given to three followers","epiphany","read tonight; with engine rev1.17→matt28.4-5"),
("12:4-6","2:13-16",["φεύγω"],["τίκτω","δράκων"],["παιδίον","ἀπόλλυμι"],"the dragon stands to devour the child when she bears; she fled to the wilderness","Herod seeks the child to destroy it; flee to Egypt","KEEP; the adversary named in the land","woman and dragon","read (2L)"),
("12:5","2:6",["ποιμαίνω"],[],[],"a son who is to shepherd all the nations","a ruler who shall shepherd my people","KEEP, as scripture cited","woman and dragon","read tonight"),
("21:14","10:2",["δώδεκα","ἀπόστολος","ὄνομα"],[],[],"twelve foundations, on them the twelve names of the twelve apostles","the names of the twelve apostles are these","ENACT (the names on the stones told as a list)","city","read tonight"),
("7:16","5:6",["πεινάω","διψάω"],[],[],"they shall hunger no more nor thirst","blessed those who hunger and thirst","KEEP, as a beatitude","multitude","read tonight"),
("6:12-13","24:29",["ἥλιος","σελήνη","ἀστήρ","πίπτω"],[],[],"the sun black, the moon as blood, the stars fell","the sun darkened, the moon not giving light, the stars shall fall","KEEP, as prophecy","sixth seal","read tonight"),
("19:7-9","25:10",["γάμος"],[],[],"the wedding of the Lamb is come; blessed those called","those ready went in with him to the wedding, and the door was shut","KEEP; with the door of 3:20","wedding","read tonight"),
("12:9","25:41",["διάβολος","ἄγγελος"],[],[],"the devil was thrown down, and his angels with him","the fire prepared for the devil and his angels","KEEP","woman and dragon","read tonight"),
("18:21","18:6",["θάλασσα"],[],[],"a stone like a great millstone thrown into the sea: so Babylon","a millstone hung on him and he sunk in the sea","EXCHANGE the patient (Babylon, the one who makes a little one stumble)","Babylon","read tonight"),
("2:7","13:9",["οὖς","ἀκούω"],[],[],"who has an ear, let him hear","who has ears, let him hear","KEEP, the letters' formula","letters","read tonight"),
("20:14-15","13:41-42",["βάλλω","πῦρ"],[],[],"death and Hades, and whoever is not found written, thrown into the lake of fire","the angels gather the lawless and throw them into the furnace of fire","EXCHANGE the patient (the adversary and the unwritten; those within the kingdom who do lawlessness)","judgment","found by the machine map (2AP.4); βάλλω with πῦρ in Revelation and the Gospels only"),
("8:7","3:10",["βάλλω","πῦρ","δένδρον"],[],[],"fire thrown to the earth, and a third of the trees burnt","every tree not bearing good fruit is cut down and thrown into the fire","the direction of the throwing turned (fire onto trees; the tree into fire)","trumpets","found by the machine map (2AP.4)"),
]
rows=[]; bad=[]
for rv,mt,both,ro,mo,rr,mr,move,strand,stand in H:
    rk=span(RE,rv); mk=span(MT,mt); rl=lem(RE,rk); ml=lem(MT,mk)
    miss=[x for x in both if nf(x) not in rl]+[x for x in ro if nf(x) not in rl]; missm=[x for x in both if nf(x) not in ml]+[x for x in mo if nf(x) not in ml]
    if miss or missm: bad.append((rv,mt,miss,missm))
    rows.append(dict(rev=rv,matt=mt,lemmas=both,rev_only=ro,matt_only=mo,rev_relation=rr,matt_relation=mr,move=move,strand=strand,standing=stand,source='hand, verified in the tagged text' if not (miss or missm) else 'hand, lemma check FAILED'))
print('hand rows',len(rows),'| lemma check failures:',bad or 'none')
# engine rows
E_=json.load(open('../engine/derivations.json'))['derivations']; runs={x['id']:x for x in json.load(open('../engine/runs.json'))['runs']}
for x in E_:
    if 'Matt' in x['target']:
        rows.append(dict(rev=x['seed'].replace('gnt:Rev ','').replace(' + Rev ','; '),matt=x['target'].replace('gnt:Matt ','').replace(' + Matt ','; '),lemmas=[m['greek'] for m in x['members']][:6],rev_relation=x['title'],matt_relation='',move=', '.join(s['op'] for s in x['steps']),strand=x['family'],standing='engine: '+runs[x['id']]['verdict'] if x['id'] in runs else 'engine',source='engine '+x['id']))
# exclusivity checks for tonight's new pairs
def near(A,B,w):
    A={nf(x) for x in A}; B={nf(x) for x in B}; out=[]
    for b in books:
        ks=list(NT[b])
        for i,k in enumerate(ks):
            if {l for l,_,_ in NT[b][k]}&A and any({l for l,_,_ in NT[b][kk]}&B for kk in ks[max(0,i-w):i+w+1]): out.append(f'{b} {k[0]}:{k[1]}')
    return out
chk={'ᾅδης within one verse of κλείς':near(['ᾅδης'],['κλείς'],1),'εἰρήνη with μάχαιρα in one verse':near(['εἰρήνη'],['μάχαιρα'],0),'διάβολος with ἄγγελος in one verse':near(['διάβολος'],['ἄγγελος'],0),'δώδεκα, ἀπόστολος with ὄνομα in one verse':[x for x in near(['ἀπόστολος'],['ὄνομα'],0) if x in near(['ἀπόστολος'],['δώδεκα'],0)],'ποιμαίνω':near(['ποιμαίνω'],['ποιμαίνω'],0),'πεινάω with διψάω':near(['πεινάω'],['διψάω'],0),'θερισμός with ἄγγελος':near(['θερισμός'],['ἄγγελος'],0),'ἀποδίδωμι with ἕκαστος':near(['ἀποδίδωμι'],['ἕκαστος'],0),'μάχαιρα twice in a verse':[f'{b} {k[0]}:{k[1]}' for b in books for k,t in NT[b].items() if sum(1 for l,_,_ in t if l==nf('μάχαιρα'))>=2],'στέφανος':near(['στέφανος'],['στέφανος'],0),'μύλος family with θάλασσα':near(['μύλος','μύλινος','μυλικός'],['θάλασσα'],0)}
for k,v in chk.items(): print(' ',k,':',v)
json.dump(dict(rows=rows,checks=chk,bad=bad),open('rev-matthew-ledger.json','w'),ensure_ascii=False,indent=1)
