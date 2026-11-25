import json, urllib.request, urllib.parse, numpy as np
C=299792.458
def H(q):
    q=dict(format="json",OBJ_DATA="NO",MAKE_EPHEM="YES",**q)
    return json.load(urllib.request.urlopen("https://ssd.jpl.nasa.gov/api/horizons.api?"+urllib.parse.urlencode(q),timeout=120))["result"]
def soe(t): return [[x.strip() for x in l.split(",") if x.strip()] for l in t.split("$$SOE")[1].split("$$EOE")[0].strip().splitlines()]
jd77=2443371.5+ (3+16/60+6/3600)/24   # 1977-08-16 03:16:06 UTC
r=soe(H(dict(COMMAND="'399'",EPHEM_TYPE="VECTORS",CENTER="'@0'",REF_PLANE="FRAME",START_TIME=f"'JD {jd77:.6f}'",STOP_TIME=f"'JD {jd77+0.001:.6f}'",STEP_SIZE="'1'",VEC_TABLE="'2'",CSV_FORMAT="YES",OUT_UNITS="KM-S",TIME_TYPE="UT")))[0]
vE=np.array([float(x) for x in r[5:8]])
# site rotation, Big Ear
lon=np.radians(-83.0489); lat=np.radians(40.2513)
T=(jd77-2451545.0)/36525; gmst=np.radians((280.46061837+360.98564736629*(jd77-2451545.0)+0.000387933*T*T)%360)
lst=gmst+lon; w=7.2921159e-5; R=6378.137*np.cos(lat)
vsite=w*R*np.array([-np.sin(lst),np.cos(lst),0.0])
def u(ra,dec): ra,dec=np.radians(ra),np.radians(dec); return np.array([np.cos(dec)*np.cos(ra),np.cos(dec)*np.sin(ra),np.sin(dec)])
dec=-(26+57/60); us=[u((19+25/60+31/3600)*15,dec),u((19+28/60+22/3600)*15,dec)]
vobs=vE+vsite; vlos=np.mean([vobs@x for x in us])   # observer velocity toward source
rr77=-vlos
F={"revised":1420.726,"ehman":1420.4556}
Femit={k:v/(1-rr77/C) for k,v in F.items()}
print("Big Ear 1977: observer velocity toward Wow %.3f km/s (rr %.3f); Sun-frame f: %s"%(vlos,rr77,{k:round(v,6) for k,v in Femit.items()}))
json.dump({"rr77":rr77,"Femit":Femit},open("freq2.json","w"))
