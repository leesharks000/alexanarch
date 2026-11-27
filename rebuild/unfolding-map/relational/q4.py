exec(open('q3.py').read().split("P('Q5 στόμα+κοιλία")[0])
P('R1 Satan+σκάνδαλον ±2',cfg([anyl('σκάνδαλον'),anyl('Σατανᾶς')],2)); print('   MT 16:23',text('MT',(16,23))); print('   MR 8:33',text('MR',(8,33)))
import collections
c=collections.Counter(b for b in books for k in NT[b] for l,_,_ in NT[b][k] if l==N('ἄξιος')); print('R2 ἄξιος by book',dict(c)); P('R2 τίς+ἄξιος',has(lambda S:N('τίς') in S and N('ἄξιος') in S))
P('R3 τίς+ἐξουσία+δίδωμι',has(lambda S:N('τίς') in S and N('ἐξουσία') in S and N('δίδωμι') in S))
P('R4 ἀρνέομαι|ἀπαρνέομαι RE+MT',[x for x in has(anyl('ἀρνέομαι','ἀπαρνέομαι')) if x[0] in('RE','MT')])
P('R4 φεύγω MT26',[x for x in has(anyl('φεύγω')) if x[0]=='MT' and x[1][0]==26]); print('   MT 26:35',text('MT',(26,35))[:120]); print('   MT 26:56',text('MT',(26,56))[-70:])
P('R5 τυφλός+πτωχός',has(lambda S:N('τυφλός') in S and N('πτωχός') in S))
P('R6 ἀποκαλύπτω MT',[x for x in has(anyl('ἀποκαλύπτω')) if x[0]=='MT'])
