import html
W,H=1200,1170
o=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="Georgia, \'Times New Roman\', serif" role="img" aria-labelledby="t d">',
'<title id="t">How the Apocalypse produces the Gospel: who bears each relation</title>',
'<desc id="d">Left, the bearers of relations in Revelation. Middle, the two parameters and the move. Right, who bears the relation in Matthew, with one checked example for each line.</desc>',
f'<rect width="{W}" height="{H}" fill="#ffffff"/>',
'<text x="40" y="40" font-size="24" fill="#1a1a1a">How the Apocalypse produces the Gospel</text>',
'<text x="40" y="64" font-size="14" fill="#555">Give the heavenly speaker a past and a land. Then each relation of Revelation has somewhere to fall. One checked example on every line.</text>']
C={'keep':'#257de0','exch':'#f47230','opp':'#00b894','form':'#f2a600'}
def box(x,y,w,h,t,sub=None,fill='#f1efe9'):
    o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{fill}" stroke="#b9b4a8"/>')
    o.append(f'<text x="{x+w/2}" y="{y+(h/2 if sub else h/2+5)}" font-size="15" text-anchor="middle" fill="#1a1a1a" font-weight="bold">{html.escape(t)}</text>')
    if sub: o.append(f'<text x="{x+w/2}" y="{y+h/2+18}" font-size="11.5" text-anchor="middle" fill="#555" font-style="italic">{html.escape(sub)}</text>')
LX,LW,RX,RW=40,230,930,230
o.append(f'<text x="{LX}" y="104" font-size="16" font-weight="bold" fill="#1a1a1a">IN REVELATION</text><text x="{RX}" y="104" font-size="16" font-weight="bold" fill="#1a1a1a">IN MATTHEW</text>')
o.append(f'<text x="600" y="104" font-size="13" text-anchor="middle" fill="#555">P1: the speaker is given a past  ·  P2: the life is told in a named land</text>')
left=[('speaker','The speaker','“I”, from heaven, about to come',125),('lamb','The Lamb','slain; buys with blood',225),('riders','The four riders','crown, sword, balance, death',325),
      ('adv','The adversary','dragon, beast, Babylon',425),('faithful','The faithful and the seer','tried; sees and falls',545),('city','The city and the end','wedding, harvest, fire, gates',665),('signs','Signs in heaven','sun, stars, earthquake',775)]
right=[('teacher','The teacher','says it, does it, suffers it',160),('followers','The followers','the twelve; Peter; “you”',330),('advland','The adversaries in the land','Herod, priests, Pharisees, Judas',500),('hearers','The hearers at the judgment','the fruitless; the lawless',650),('story','The told world','parables, events, a map',790)]
LP={k:(LX+LW,y+30) for k,_,_,y in left}; RP={k:(RX,y+32) for k,_,_,y in right}
for k,t,s,y in left: box(LX,y,LW,60,t,s)
for k,t,s,y in right: box(RX,y,RW,64,t,s)
lines=[('speaker','teacher','keep','“I will confess his name before my Father” (3:5 → 10:32)',0),
 ('speaker','followers','exch','“I will keep you from the hour of trial” becomes “bring us not into trial” (3:10 → 6:13)',0),
 ('speaker','advland','exch','“as many as I love”: said by the betrayer, of the teacher (3:19 → 26:48)',0),
 ('lamb','advland','exch','the Lamb buys with blood; the priests buy a field with the price of blood (5:9 → 27:6–7)',0),
 ('riders','teacher','exch','the balance in the rider’s hand: “take my yoke”; the crown given: a crown of thorns (6:5 → 11:29; 6:2 → 27:29)',0),
 ('adv','teacher','exch','the dragon seized, bound, sealed over: the teacher seized, bound, sealed in (20:1–3 → 26:50; 27:66)',0),
 ('adv','teacher','opp','no one buys or sells without the mark: sellers and buyers cast out (13:17 → 21:12)',1),
 ('adv','advland','form','the dragon waits to devour the child: Herod seeks the child (12:4 → 2:13)',0),
 ('faithful','teacher','exch','“the devil will throw some of you into prison, to be tried”: led out to be tried by the devil (2:10 → 4:1)',0),
 ('faithful','followers','exch','“I fell at his feet as dead … fear not”: three fall on the mountain (1:17 → 17:6–7)',0),
 ('city','hearers','exch','thrown into the lake of fire: thrown into the furnace of fire (20:15 → 13:42)',0),
 ('city','story','form','the wedding of the Lamb: “the kingdom is like a king who made a wedding” (19:7–9 → 22:1–14)',0),
 ('speaker','story','form','“my wage with me … the first and the last”: the labourers paid last to first (22:12–13 → 20:1–16)',1),
 ('signs','story','form','“a great earthquake came”: at the tomb, in the same words (16:18 → 28:2)',0)]
used={}; KEY=[]
for a,b,f,t,off in lines:
    x0,y0=LP[a]; x1,y1=RP[b]
    i=used.get(('L',a),0); used[('L',a)]=i+1; j=used.get(('R',b),0); used[('R',b)]=j+1
    y0+= (i-1)*11; y1+= (j-2)*9
    pid=f'p{len(used)}{a}{b}{f}'
    o.append(f'<path id="{pid}" d="M{x0},{y0} C{x0+240},{y0} {x1-240},{y1} {x1},{y1}" fill="none" stroke="{C[f]}" stroke-width="2" stroke-opacity="0.8"/>')
    o.append(f'<circle cx="{x0}" cy="{y0}" r="3" fill="{C[f]}"/><path d="M{x1-8},{y1-4} L{x1},{y1} L{x1-8},{y1+4}" fill="none" stroke="{C[f]}" stroke-width="2"/>')
    n=len(KEY)+1; tt=0.30+0.045*((n*5)%9)
    bz=lambda p0,p1,p2,p3:((1-tt)**3*p0+3*(1-tt)**2*tt*p1+3*(1-tt)*tt**2*p2+tt**3*p3)
    bx=bz(x0,x0+240,x1-240,x1); by=bz(y0,y0,y1,y1)
    o.append(f'<circle cx="{bx:.1f}" cy="{by:.1f}" r="10" fill="#ffffff" stroke="{C[f]}" stroke-width="2"/><text x="{bx:.1f}" y="{by+4:.1f}" font-size="11.5" text-anchor="middle" fill="#1a1a1a" font-weight="bold">{n}</text>')
    KEY.append((n,f,t))
ky=900
o.append(f'<line x1="40" x2="1160" y1="{ky-22}" y2="{ky-22}" stroke="#d8d4ca"/>')
for n,f,t in KEY:
    col=0 if n<=7 else 1; yy=ky+((n-1)%7)*30; xx=40+col*570
    o.append(f'<circle cx="{xx+10}" cy="{yy-4}" r="10" fill="#ffffff" stroke="{C[f]}" stroke-width="2"/><text x="{xx+10}" y="{yy}" font-size="11.5" text-anchor="middle" fill="#1a1a1a" font-weight="bold">{n}</text>')
    a,_,b=t.rpartition(' (')
    words=a.split(); l1=''; l2=''
    for w in words:
        if len(l1)+len(w)<78 and not l2: l1+=(' ' if l1 else '')+w
        else: l2+=(' ' if l2 else '')+w
    o.append(f'<text x="{xx+28}" y="{yy-5 if l2 else yy}" font-size="11.5" fill="#333">{html.escape(l1)}</text>')
    if l2: o.append(f'<text x="{xx+28}" y="{yy+8}" font-size="11.5" fill="#333">{html.escape(l2)}</text>')
    o.append(f'<text x="{xx+545}" y="{yy}" font-size="10.5" fill="#777" text-anchor="end">{html.escape(b.rstrip(")"))}</text>')
x=40;y=H-24
for k,t in (('keep','Kept'),('exch','Exchanged: the bearer or the one it is done to'),('opp','Opposed'),('form','Given a form: happens, is likened, enacted, named in the land')):
    o.append(f'<line x1="{x}" x2="{x+26}" y1="{y-4}" y2="{y-4}" stroke="{C[k]}" stroke-width="3" stroke-linecap="round"/><text x="{x+32}" y="{y}" font-size="12.5" fill="#333">{t}</text>'); x+=32+len(t)*6.7+24
o.append('</svg>')
open('/mnt/user-data/outputs/REV-TO-MATTHEW-BEARERS.svg','w',encoding='utf-8').write('\n'.join(o))
