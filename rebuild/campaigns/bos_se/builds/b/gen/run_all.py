import sys, pickle; sys.path.insert(0,'tmp')
from engine import *
res={}
for name,XY in [('AA',('A','A')),('AZ',('A','Z')),('ZZ',('Z','Z')),('W',('Wp','Wm'))]:
    out={}
    for proj in (False,True):
        ds=diagrams(*XY,proj=proj)
        per=[]
        for lab,x in ds:
            fin,pole,rest=finalize(x)
            per.append((lab,{str(k):phys(vv) for k,vv in fin.items() if phys(vv)!=0},phys(pole),phys(rest)))
        tot=sum(x for _,x in ds)
        fin,pole,rest=finalize(tot)
        out[proj]=(per,{str(k):phys(vv) for k,vv in fin.items() if phys(vv)!=0},phys(pole),phys(rest))
    a,b=out[False],out[True]
    ok=all(sp.simplify(a[1].get(k,0)-b[1].get(k,0))==0 for k in set(a[1])|set(b[1])) and sp.simplify(a[2]-b[2])==0 and sp.simplify(a[3]-b[3])==0
    print(name,'methods agree:',ok)
    print(' pole',a[2]); print(' rest',a[3])
    for k,vv in a[1].items(): print(' ',k,vv)
    res[name]=out
pickle.dump(res,open('tmp/res.pkl','wb'))
