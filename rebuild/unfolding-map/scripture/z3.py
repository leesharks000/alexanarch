src=open('x1.py',encoding='utf-8').read(); exec(src.split("# kind, matt")[0])
RE=NT['RE']
ex=[k for k in ORDER['Exod'] if k[0]<=4]; rv=[k for k in RE if k[0]==12]
eh=rh=0
for v in range(1,24):
    ms=stems(text('MT',(2,v)))
    be=max(((len(ms&stems(LX['Exod'][k])),k,sorted(ms&stems(LX['Exod'][k]))) for k in ex)); br=max(((len(ms&stems(text('RE',k))),k,sorted(ms&stems(text('RE',k)))) for k in rv))
    eh+=be[0]>=2; rh+=br[0]>=2
    print(f'Mt 2:{v:<2d} Exod {be[1][0]}:{be[1][1]:<2d} {be[0]} {" ".join(be[2]) if be[0]>=2 else "":40s} | Rev 12:{br[1][1]:<2d} {br[0]} {" ".join(br[2]) if br[0]>=2 else ""}')
print('verses of Matthew 2 with a hit: Exodus',eh,'| Revelation 12',rh)
print(LX['Exod'][(4,19)][:160]); print(text('MT',(2,20)))
