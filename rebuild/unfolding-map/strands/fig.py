exec(open('v6.py').read().split("random.seed(6)")[0])
P=json.load(open('/home/claude/unfold/rev3/matt-proxy-classes.json'))
allv=set(); nonrel=set()
for r in Lr:
    mk=set(segs(MT,r['matt'])); allv|=mk
    if 'relational' not in r.get('standing',''): nonrel|=mk
print('rows',len(Lr),'reach',len(allv),'of',len(MT),round(100*len(allv)/len(MT),1),'| without relational rows',len(nonrel),'| ch11-12',len([k for k in allv if k[0] in(11,12)]))
print(collections.Counter(P.get('%d:%d'%k) for k in allv))
for u in list(U): U[u]=[x for x in U[u] if x[3] not in ('2:9','26:58','20:25-28','11:2-3','11:15','11:27','11:28-29','12:29','11:20-21')]
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
ink='#1f2530'; mut='#5b6470'; blue='#257de0'; grey='#9aa3ad'
fig,(a,b)=plt.subplots(1,2,figsize=(12.5,6.8),dpi=150,gridspec_kw={'width_ratios':[1.05,1]}); fig.patch.set_facecolor('white')
order=[l[0] for l in LET]+sorted(k for k in U if k.startswith('ch'))
order=[u for u in order if len(U[u])>=5]; names=[u if not u.startswith('ch') else 'ch. '+str(int(u[2:])) for u in order]
ys=list(range(len(order)))[::-1]
a.axvline(50,color='#c9ced4',lw=1)
for u,n,y in zip(order,names,ys):
    c,d=conc(U[u]); sh=100*c/max(1,c+d); col=blue if u=='ch12' else grey
    a.plot([50,sh],[y,y],color=col,lw=2,solid_capstyle='round'); a.scatter([sh],[y],s=70,color=col,edgecolor='white',linewidth=1.2,zorder=3)
    a.text(103,y,f'{len(U[u])} rows',va='center',fontsize=8,color=mut)
    if u=='ch12': a.text(sh-3,y+0.5,'81%, p = 0.003 (about 0.13 corrected for 22 units)',va='center',ha='right',fontsize=8,color=ink)
a.set_yticks(ys); a.set_yticklabels(names,fontsize=9); a.set_xlim(0,120); a.set_xticks([0,25,50,75,100]); a.set_xticklabels(['0','25','50%','75','100'],fontsize=8)
a.set_xlabel('pairs of rows standing in the same order in both books',fontsize=9,color=mut)
a.set_title('Order inside each letter and chapter of Revelation',fontsize=12,loc='left',color=ink,pad=22)
a.text(0,1.02,'Units with five rows or more, as sealed. All units together: 50% (p = 0.55).',transform=a.transAxes,fontsize=8.5,color=mut)
mch=[mi[(c,1)] for c in range(1,29)]
for x in mch: b.axvline(x,color='#eef0f2',lw=0.8,zorder=0)
rows=[(m,list(RE)[int(r)][1],rv,mt) for m,r,rv,mt in U['ch12']]
head=[p for p in rows if p[0]<=mi[(3,17)]]; rest=[p for p in rows if p[0]>mi[(3,17)]]
b.scatter([p[0] for p in rest],[p[1] for p in rest],s=60,color=grey,edgecolor='white',linewidth=1.2,zorder=3,label='the eight rows outside Matthew 2–3 (p = 0.45)')
b.scatter([p[0] for p in head],[p[1] for p in head],s=60,color=blue,edgecolor='white',linewidth=1.2,zorder=3,label='rows landing in Matthew 2–3')
b.scatter([mi[(2,9)]],[4],s=90,facecolor='white',edgecolor=blue,linewidth=2,zorder=4,label='predicted from the order, then found: Rev 12:4 → Matt 2:9')
off={'2:2':-6,'2:9':-2,'2:13-16':4,'2:6':-5,'3:3':5}
for p in head+[(mi[(2,9)],4,'12:4','2:9')]: b.annotate(f'{p[2]} → {p[3]}',(p[0],p[1]),xytext=(11,off.get(p[3],0)),textcoords='offset points',fontsize=7.5,color=ink,va='center')
b.set_xticks(mch[::3]); b.set_xticklabels([str(c) for c in range(1,29,3)],fontsize=8); b.set_yticks(range(1,18,2)); b.set_yticklabels([str(v) for v in range(1,18,2)],fontsize=8); b.set_ylim(0,18.5); b.set_xlim(-25,len(MT)+10)
b.set_xlabel('Matthew, by chapter',fontsize=9,color=mut); b.set_ylabel('Revelation 12, by verse',fontsize=9,color=mut)
b.set_title('Revelation 12 in Matthew',fontsize=12,loc='left',color=ink,pad=22)
b.text(0,1.02,'The forward run is the infancy. Outside it the chapter is scattered like the rest.',transform=b.transAxes,fontsize=8.5,color=mut)
b.legend(loc='upper center',bbox_to_anchor=(0.5,-0.11),ncol=1,frameon=False,fontsize=8.5)
for ax in (a,b):
    for s in ['top','right']: ax.spines[s].set_visible(False)
    for s in ['left','bottom']: ax.spines[s].set_color('#c9ced4')
    ax.tick_params(colors=mut,length=0)
plt.tight_layout(); plt.savefig('/mnt/user-data/outputs/REV-MATTHEW-ORDER-BY-UNIT.png',facecolor='white'); print('fig ok')
