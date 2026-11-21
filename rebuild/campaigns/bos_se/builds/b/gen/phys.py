import sympy as sp
from vtx import g,gp,c,s,v,lam,mw,mz
e,mh=sp.symbols('e mh')
SUB={g:e/s, gp:e/c, v:2*mw*s/e, lam:mh**2*e**2/(8*mw**2*s**2), mz:mw/c}
def phys(x):
    x=sp.sympify(x).subs(SUB)
    x=sp.together(sp.expand(x))
    n,d=sp.fraction(x)
    # reduce s^2 -> 1-c^2
    n=sp.expand(n); d=sp.expand(d)
    def red(p):
        p=sp.Poly(p,s)
        out=0
        for (k,),co in p.terms():
            out+=co*(1-c**2)**(k//2)*s**(k%2)
        return sp.expand(out)
    return sp.factor(sp.cancel(red(n)/red(d)))
