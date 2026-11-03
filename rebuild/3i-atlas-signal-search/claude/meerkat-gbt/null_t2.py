import pandas as pd, numpy as np, sys
df=pd.read_parquet('hits_all.parquet', columns=['frequency','driftRate','sourceName','tstart'])
df=df[df.sourceName.str.contains('tlas',case=False) & (df.driftRate!=0)]
df['day']=df.tstart.astype(int)
# deldot per day (km/s), from the Horizons run (day means)
dd={60984:-20.714,60997:-22.13,60998:-22.74,61006:-20.8,61028:0.32}
C=299792.458
df['f_rest']=df.frequency/(1-df.day.map(dd)/C)
A=np.unique(np.rint(df[df.day==61006].f_rest*1e6/50).astype('int64'))
Bf=df[df.day==61028].f_rest.values*1e6
def count(off_hz):
    b=np.unique(np.rint((Bf+off_hz)/50).astype('int64'))
    return len(np.intersect1d(A,b))+len(np.intersect1d(A,b+1))
real=count(0)
rng=np.random.default_rng(1)
offs=rng.uniform(2000,200000,400)*rng.choice([-1,1],400)
null=np.array([count(o) for o in offs])
print('coincident bins, true comet frame:',real)
print('null (random frame offsets 2-200 kHz): mean %.1f sd %.1f max %d; fraction >= real: %.3f'%(null.mean(),null.std(),null.max(),(null>=real).mean()))
