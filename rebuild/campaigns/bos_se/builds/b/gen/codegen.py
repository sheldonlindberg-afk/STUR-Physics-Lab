import sys, pickle; sys.path.insert(0,'tmp')
import sympy as sp
from sympy.printing.str import StrPrinter
from phys import e, mh
from vtx import c, s, mw
kk=sp.Symbol('kk')
class P(StrPrinter):
    def _print_Integer(self, n): return str(int(n))
    def _print_Rational(self, r): return f"(mpf({r.p})/{r.q})"
pr=P()
res=pickle.load(open('tmp/res.pkl','rb'))
def code(x):
    x=sp.factor(sp.simplify(x/e**2))
    return pr.doprint(x)
lines=[]
for name in ('AA','AZ','ZZ','W'):
    per,fin,pole,rest=res[name][False]
    lines.append(f"def _terms_{name}(kk, mw, mh, c, s):")
    lines.append("    # returns (coefficients of the finite loop functions {name: coeff}, rational rest, UV-pole coefficient); units alpha/(4 pi)")
    lines.append("    co = {}")
    for k,vv in sorted(fin.items()):
        lines.append(f"    co['{k}'] = {code(vv)}")
    lines.append(f"    rest = {code(rest)}")
    lines.append(f"    pole = {code(pole)}")
    lines.append("    return co, rest, pole")
    lines.append("")
open('tmp/gen_part.py','w').write("\n".join(lines))
print("\n".join(lines))
