#!/usr/bin/env python3
"""Derives the TEGR torsion scalar for a static spherical metric with the rotated
("good") tetrad, used by fp_black_hole_exterior.py.  Slow (about a minute): not run by tests.
T = 1/4 T^rmn T_rmn + 1/2 T^rmn T_nmr - T^r_rm T^n_n^m  (Weitzenboeck torsion)."""
import sympy as sp
t,r,th,ph,M=sp.symbols('t r theta phi M',positive=True)
X=[t,r,th,ph]
A=sp.Function('A')(r); B=sp.Function('B')(r)
s,cth,sph,cph=sp.sin(th),sp.cos(th),sp.sin(ph),sp.cos(ph)
# "good" (rotated) tetrad for ds^2 = A dt^2 - B dr^2 - r^2 dOmega^2
e=sp.Matrix([[sp.sqrt(A),0,0,0],
 [0,sp.sqrt(B)*s*cph, r*cth*cph, -r*s*sph],
 [0,sp.sqrt(B)*s*sph, r*cth*sph,  r*s*cph],
 [0,sp.sqrt(B)*cth,  -r*s, 0]])          # e[a,mu]
eta=sp.diag(1,-1,-1,-1)
g=sp.simplify(e.T*eta*e); gi=g.inv()
E=sp.simplify(e.inv())                    # E[mu,a]  inverse tetrad
Tor=[[[sp.simplify(sum(E[rho,a]*(sp.diff(e[a,nu],X[mu])-sp.diff(e[a,mu],X[nu])) for a in range(4)))
       for nu in range(4)] for mu in range(4)] for rho in range(4)]
# full scalar: 1/4 T^{rmn}T_{rmn} + 1/2 T^{rmn}T_{nmr} - T_{rm}^{r} T^{nm}_{n}
Tup=[[[sp.simplify(sum(gi[rho,a]*gi[mu,b]*gi[nu,c]*sum(g[a,l]*Tor[l][b][c] for l in range(4)) for a in range(4) for b in range(4) for c in range(4))) for nu in range(4)] for mu in range(4)] for rho in range(4)]
Tlow=[[[sp.simplify(sum(g[rho,l]*Tor[l][mu][nu] for l in range(4))) for nu in range(4)] for mu in range(4)] for rho in range(4)]
S1=sum(Tup[a][b][c]*Tlow[a][b][c] for a in range(4) for b in range(4) for c in range(4))/4
S2=sum(Tup[a][b][c]*Tlow[c][b][a] for a in range(4) for b in range(4) for c in range(4))/2
vec=[sp.simplify(sum(Tor[rh][rh][m] for rh in range(4))) for m in range(4)]   # T^rho_{rho mu}
S3=sum(gi[m,n]*vec[m]*vec[n] for m in range(4) for n in range(4))
Tsc=sp.simplify(S1+S2-S3)
print('T(A,B) =',Tsc)
Ts=sp.simplify(Tsc.subs({A:1-2*M/r,B:1/(1-2*M/r)}).doit())
print('Schwarzschild T(r) =',sp.simplify(Ts))
print('at r=2M:',sp.simplify(Ts.subs(r,2*M)),'  large r:',sp.series(Ts,r,sp.oo,6))
