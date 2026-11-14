"""Compare the third route (third_route.json) with build a, build b and src/. Run from anywhere."""
import json, os, sys, importlib, math
from fractions import Fraction as F
HERE=os.path.dirname(os.path.abspath(__file__)); REPO=os.path.abspath(os.path.join(HERE,"..",".."))
T=json.load(open(os.path.join(HERE,"third_route.json")))
def load_build(bid):
    for k in [k for k in sys.modules if k in ("inputs","toolkit","gauge331","weak","chiral","running","links","blackholes","graviton","casimir","desitter")]:
        del sys.modules[k]
    sys.path[:0]=[os.path.join(REPO,"rebuild","builds",bid), os.path.join(REPO,"rebuild")]
    m={n:importlib.import_module(n) for n in ("weak","running","chiral","links")}
    del sys.path[:2]
    return m
def vals(m):
    W,R,C,L=m["weak"],m["running"],m["chiral"],m["links"]
    d={"fpi":W.fpi_from_pion_decay(),"pi0":L.pi0_width_from_rungs(),"chpt":C.chpt_mpi_from_rungs()}
    d["sm"]=tuple(R.sm_coefficients())
    for v in ("-1/sqrt3","+1/sqrt3"):
        for Nc in (1,3,5,7,9): d[f"b|{v}|{Nc}"]=tuple(R.b_331(Nc,v))
        for Nc in (1,3,5,7): d[f"pole|{v}|{Nc}"]=R.landau_pole(Nc,v)
        d[f"gw|{v}"]=L.g_window_from_rungs(v)
        d[f"aX|{v}"]=R.matching_331(4e3,v)[0]
    return d
A=vals(load_build("2026-11-a")); B=vals(load_build("2026-11-b"))
sys.path.insert(0,os.path.join(REPO,"src"))
import ladder_links as LL, m331_exact as E, m331_three_loop as T3, m331_margin as MM
S={"fpi":LL.fpi_from_weak()[1]}
G_new,pull,m4=LL.rung2_with_weak_fpi(); S["pi0"]=G_new; S["chpt"]=m4
a,_=E.sm_check(); S["sm"]=(a[0]*F(5,3),a[1])
for v in ("-1/sqrt3","+1/sqrt3"):
    for Nc in (1,3,5,7,9):
        a,_=E.coefficients(*E.MODELS[v](Nc)[:3]); S[f"b|{v}|{Nc}"]=(a[0],a[1]); S[f"bc|{v}|{Nc}"]=a[2]
    for Nc in (3,5):
        S[f"pole|{v}|{Nc}"]=float(T3.pole(Nc,v,MV=4e3,loops=1,thresholds=False,yukawas=False,gmax=MM.ALPHA1))
    mpl=float(T["mpl"]); S[f"gw|{v}"]=((mpl/S[f"pole|{v}|3"])**2,(mpl/S[f"pole|{v}|5"])**2)
rel=lambda x,y: abs(x/y-1)
def row(name,t,key,idx=None):
    g=lambda D: (D.get(key) if idx is None else (D[key][idx] if key in D else None))
    a,b,s=g(A),g(B),g(S)
    f=lambda x: "n/a" if x is None else f"{x:.13g}"
    r=lambda x: "n/a" if x is None else f"{rel(x,t):.1e}"
    print(f"| {name} | {t:.13g} | {f(a)} | {f(b)} | {f(s)} | {r(a)} / {r(b)} / {r(s)} |")
print("| quantity | third route | build a | build b | src | rel diff a / b / src vs third |")
row("f_pi (GeV)",float(T["fpi"]),"fpi"); row("pi0 width (eV)",float(T["pi0_width"]),"pi0"); row("O(p^4) m_pi (GeV)",float(T["chpt_mpi"]),"chpt")
for v in ("-1/sqrt3","+1/sqrt3"):
    row(f"1/alpha_X(4 TeV) {v}",float(T["boundary"][2]),f"aX|{v}")
    for Nc in (1,3,5,7): row(f"pole {v} Nc={Nc} (GeV)",float(T["poles"][f"{v}|{Nc}"]),f"pole|{v}|{Nc}")
    row(f"G window lo {v}",float(T[f"g_window|{v}"][0]),f"gw|{v}",0); row(f"G window hi {v}",float(T[f"g_window|{v}"][1]),f"gw|{v}",1)
print("exact b comparisons:")
ok=True
print(" SM third",T["sm"],"a",A["sm"],"b",B["sm"],"src",S["sm"])
for v in ("-1/sqrt3","+1/sqrt3"):
    for Nc in (1,3,5,7,9):
        t=tuple(F(x) for x in T["b_331"][f"{v}|{Nc}"])
        e=(t[:2]==A[f"b|{v}|{Nc}"]==B[f"b|{v}|{Nc}"]==S[f"b|{v}|{Nc}"]) and t[2]==S[f"bc|{v}|{Nc}"]
        ok&=e; print(f" {v} Nc={Nc}: third (bX,bL,bc)={[str(x) for x in t]} a={[str(x) for x in A[f'b|{v}|{Nc}']]} src bc={S[f'bc|{v}|{Nc}']} all equal: {e}")
print("ALL b EXACTLY EQUAL:",ok)
print("src pi0 pull",pull,"src fpi tuple",LL.fpi_from_weak())
