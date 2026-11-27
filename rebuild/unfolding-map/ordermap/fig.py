exec(open('u2.py').read().split("name=lambda V,i")[0])
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
C={'sealed':'#257de0','engine':'#00b894','counted':'#f2a600','read':'#9aa3ad'}; LAB={'sealed':'written down before counting, or produced blind','engine':'engine','counted':'counted','read':'read'}
fig,ax=plt.subplots(figsize=(11,9.2),dpi=150); fig.patch.set_facecolor('white')
mch=[mi[(c,1)] for c in range(1,29)]; rch=[ri[(c,1)] for c in range(1,23)]
for x in mch: ax.axvline(x,color='#eef0f2',lw=0.8,zorder=0)
for y in rch: ax.axhline(y,color='#eef0f2',lw=0.8,zorder=0)
ax.axvspan(mi[(11,1)],mi[(13,1)],color='#f6f1e6',zorder=0); ax.text((mi[(11,1)]+mi[(13,1)])/2,len(RE)-6,'held out',ha='center',va='top',fontsize=8,color='#8a7a55')
for k in ['read','counted','engine','sealed']:
    pts=[(m,r) for m,r,row in Q if ('sealed' if cls(L[row]['standing']) in('sealed','blind') else cls(L[row]['standing']))==k]
    ax.scatter([p[0] for p in pts],[p[1] for p in pts],s=46,color=C[k],edgecolor='white',linewidth=1.2,label=f'{LAB[k]} ({len(pts)})',zorder=3)
for run in [[(26,35),(26,40),(26,41),(26,48)],[(26,52),(26,56),(26,64)]]:
    pp=[(m,r) for m,r,row in Q if mk_[m] in run]; pp=sorted(pp); ax.plot([p[0] for p in pp],[p[1] for p in pp],color='#3b4350',lw=1.4,zorder=2)
ax.set_xticks(mch); ax.set_xticklabels([str(c) for c in range(1,29)],fontsize=8); ax.set_yticks(rch); ax.set_yticklabels([str(c) for c in range(1,23)],fontsize=8)
ax.set_xlim(-8,len(MT)+8); ax.set_ylim(-6,len(RE)+6)
ax.set_xlabel('Matthew, by chapter (where the row begins)',fontsize=10,color='#3b4350'); ax.set_ylabel('Revelation, by chapter (the median of the places the row draws on)',fontsize=10,color='#3b4350')
ax.set_title('The 149 rows: order in Matthew against order in Revelation',fontsize=13,loc='left',color='#1f2530',pad=26)
ax.text(0,1.012,'One point per row. Rank correlation −0.09 (p = 0.13). No rotation of Revelation does better. The two lines are the only runs of three or more.',transform=ax.transAxes,fontsize=8.5,color='#5b6470')
for s in ['top','right']: ax.spines[s].set_visible(False)
for s in ['left','bottom']: ax.spines[s].set_color('#c9ced4')
ax.tick_params(colors='#5b6470',length=0)
ax.legend(loc='upper center',bbox_to_anchor=(0.5,-0.07),ncol=4,frameon=False,fontsize=9)
plt.tight_layout(); plt.savefig('/mnt/user-data/outputs/REV-MATTHEW-ORDER-MAP.png',facecolor='white'); print('ok')
