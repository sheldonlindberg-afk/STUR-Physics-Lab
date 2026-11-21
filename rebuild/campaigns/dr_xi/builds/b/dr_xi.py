"""Bosonic one-loop Delta r of muon decay in the general R_xi gauge, derived from the SU(2)xU(1) Lagrangian.

See DERIVATION.md.  Everything below is built from the Lagrangian of SPEC section 1:
  * the Feynman rules are generated numerically in a real field basis (generators T^a, structure constants C^{abc},
    vev v) and rotated to mass eigenstates; no vertex is typed in by hand;
  * the Lorentz algebra of the gauge-boson self-energies is done symbolically (sympy) with one Feynman parameter;
  * the lepton vertex, self-energy and box diagrams at zero external momenta are reduced symbolically (d-dimensional
    Dirac algebra, angular averaging of the loop momentum) to vacuum integrals evaluated by partial fractions;
  * all numerics in mpmath at 90 digits (local to the exports).
Conventions: 1PI two-point sum = -i Sigma_T (g - pp/p^2) + ..., delta M^2 = Re Sigma_T(M^2);  MS-bar at mu.
"""
import functools
import itertools
import math

import mpmath as mp
import numpy as np
import sympy as sp

_DPS = 90
_LAMBDAS = ('1e-14', '1e-17')     # photon-mass IR regulator values (lambda -> 0 extrapolation, see DERIVATION 5)

# =====================================================================================================
# 1. symbolic Lorentz algebra for the gauge-boson self-energies
# =====================================================================================================
_d = sp.Symbol('d')
_kk, _kp, _pp = sp.symbols('kk kp pp')
_x, _ll, _lp, _m1, _m2, _L = sp.symbols('x ll lp m1 m2 L')


def _dot(a, b):
    tab = {('k', 'k'): _kk, ('k', 'p'): _kp, ('p', 'k'): _kp, ('p', 'p'): _pp}
    return sp.expand(sum(ca * cb * tab[(u, w)] for u, ca in a.items() for w, cb in b.items()))


class _T:
    """sum of terms coef * prod(factors); factor = ('g', i, j) metric or ('v', vector, i)."""

    def __init__(self, terms):
        self.terms = terms

    def __mul__(self, o):
        if not isinstance(o, _T):
            return _T([(c * o, f) for c, f in self.terms])
        return _T([(c1 * c2, f1 + f2) for c1, f1 in self.terms for c2, f2 in o.terms])

    __rmul__ = __mul__

    def __add__(self, o):
        return _T(self.terms + o.terms)


def _G(i, j):
    return _T([(1, [('g', i, j)])])


def _V(vec, i):
    return _T([(1, [('v', vec, i)])])


def _contract(c, fs):
    fs = list(fs)
    changed = True
    while changed:
        changed = False
        for n, f in enumerate(fs):
            if f[0] != 'g':
                continue
            i, j = f[1], f[2]
            if i == j:
                c = c * _d
                fs.pop(n)
                changed = True
                break
            for m, h in enumerate(fs):
                if m == n:
                    continue
                idx = [h[1], h[2]] if h[0] == 'g' else [h[2]]
                if j in idx or i in idx:
                    a, b = (j, i) if j in idx else (i, j)
                    if h[0] == 'g':
                        fs[m] = ('g', b if h[1] == a else h[1], b if h[2] == a else h[2])
                    else:
                        fs[m] = ('v', h[1], b)
                    fs.pop(n)
                    changed = True
                    break
            if changed:
                break
        if not changed:
            for n, f in enumerate(fs):
                if f[0] != 'v':
                    continue
                for m in range(n + 1, len(fs)):
                    h = fs[m]
                    if h[0] == 'v' and h[2] == f[2]:
                        c = c * _dot(f[1], h[1])
                        fs.pop(m)
                        fs.pop(n)
                        changed = True
                        break
                if changed:
                    break
    return c, fs


def _scalar(t):
    out = 0
    for c, fs in t.terms:
        c2, rest = _contract(c, fs)
        assert not rest
        out += c2
    return sp.expand(out)


def _lin(a, b, sa=1, sb=1):
    out = dict()
    for u, c in a.items():
        out[u] = out.get(u, 0) + sa * c
    for u, c in b.items():
        out[u] = out.get(u, 0) + sb * c
    return out


_K = {'k': 1}
_P = {'p': 1}
_Q = {'k': -1, 'p': -1}          # momentum of the second loop line, k2 = -p - k


def _V3(i1, q1, i2, q2, i3, q3):
    """triple-gauge vertex without C^{abc}: all momenta incoming"""
    return (_G(i1, i2) * _V(_lin(q1, q2, 1, -1), i3) + _G(i2, i3) * _V(_lin(q2, q3, 1, -1), i1)
            + _G(i3, i1) * _V(_lin(q3, q1, 1, -1), i2))


def _line(t, mom, i, j):
    return _G(i, j) if t == 'g' else _V(mom, i) * _V(mom, j)


def _transverse(Nmn):
    """(g_{mu nu} - p_mu p_nu/p^2) N^{mu nu}, the 1/(d-1) is returned separately"""
    Ng = _scalar(Nmn * _G('mu', 'nu'))
    Np = _scalar(Nmn * _V(_P, 'mu') * _V(_P, 'nu'))
    return sp.expand(Ng - sp.cancel(Np / _pp)), 1 / (_d - 1)


def _dfact2(j):
    r = 1
    for i in range(1, 2 * j, 2):
        r *= i
    return r


def _avg(j):
    a = sp.Integer(_dfact2(j))
    for i in range(j):
        a = a / (_d + 2 * i)
    return a


def _bubble(expr, dfac):
    """int d^dk N/[(k^2-m1)((k+p)^2-m2)] = i/16pi^2 int_0^1 dx [pole/epsbar + fin], L = ln Delta (mu = 1)"""
    e = sp.expand(expr.subs({_kk: _ll - 2 * _x * _lp + _x**2 * _pp, _kp: _lp - _x * _pp}, simultaneous=True))
    poly = sp.Poly(e, _lp, _ll)
    Delta = _x * _m2 + (1 - _x) * _m1 - _x * (1 - _x) * _pp
    pole = 0
    fin = 0
    for (a, n), c in poly.terms():
        if a % 2:
            continue
        j = a // 2
        C = sp.together(c * _avg(j) * dfac) * _pp**j
        nn = n + j
        C4 = C.subs(_d, 4)
        C1 = sp.diff(C, _d).subs(_d, 4)
        pole += C4 * (nn + 1) * Delta**nn
        fin += C4 * (nn + 1) * Delta**nn * (-_L + sp.Rational(nn, nn + 1)) - 2 * C1 * (nn + 1) * Delta**nn
    return sp.expand(pole), sp.expand(fin)


def _tadpole(expr, dfac):
    """int d^dk N/(k^2-m1) = i/16pi^2 [pole/epsbar + fin], L = ln m1"""
    poly = sp.Poly(sp.expand(expr), _kp, _kk)
    pole = 0
    fin = 0
    for (a, n), c in poly.terms():
        if a % 2:
            continue
        j = a // 2
        C = sp.together(c * _avg(j) * dfac) * _pp**j
        nn = n + j
        C4 = C.subs(_d, 4)
        C1 = sp.diff(C, _d).subs(_d, 4)
        pole += C4 * _m1**(nn + 1)
        fin += C4 * _m1**(nn + 1) * (1 - _L) - 2 * C1 * _m1**(nn + 1)
    return sp.expand(pole), sp.expand(fin)


def _poly_eval_factory(e, vars_):
    """sympy polynomial in vars_ -> list of (mpf-able rational, exponents)"""
    e = sp.expand(e)
    if e == 0:
        return []
    P = sp.Poly(e, *vars_)
    return [(sp.Rational(c), mon) for mon, c in P.terms()]


def _peval(terms, vals):
    s = mp.mpf(0)
    for c, mon in terms:
        t = mp.mpf(c.p) / c.q
        for v, k in zip(vals, mon):
            if k:
                t *= v**k
        s += t
    return s


@functools.lru_cache(maxsize=None)
def _se_kernels():
    raw = {}
    for t1 in 'gk':
        for t2 in 'gk':
            N = _V3('mu', _P, 'a', _K, 'b', _Q) * _line(t1, _K, 'a', 'A') * _line(t2, _Q, 'b', 'B') \
                * _V3('nu', {'p': -1}, 'A', {'k': -1}, 'B', {'k': 1, 'p': 1})
            raw['VV' + t1 + t2] = _bubble(*_transverse(N))
    for t in 'gk':
        raw['VS' + t] = _bubble(*_transverse(_G('mu', 'a') * _line(t, _K, 'a', 'A') * _G('nu', 'A')))
    two = {'k': 2, 'p': 1}
    raw['SS'] = _bubble(*_transverse(_V(two, 'mu') * _V(two, 'nu')))
    raw['GH'] = _bubble(*_transverse(_V(_K, 'mu') * _V({'k': 1, 'p': 1}, 'nu')))
    for t in 'gk':
        raw['VT' + t] = _tadpole(*_transverse(_G('mu', 'nu') * _line(t, _K, 'r', 'r') + _line(t, _K, 'mu', 'nu') * (-1)))
    raw['ST'] = _tadpole(*_transverse(_G('mu', 'nu')))
    out = {}
    for name, (pole, fin) in raw.items():
        tad = name in ('VTg', 'VTk', 'ST')
        finA = sp.expand(fin.subs(_L, 0))
        finB = sp.expand(sp.diff(fin, _L))
        pieces = {'P': pole, 'A': finA, 'B': finB}
        if not tad:
            pieces['dP'] = sp.diff(pole, _pp).subs(_pp, 0)
            pieces['dA'] = sp.diff(finA, _pp).subs(_pp, 0)
            pieces['dB'] = sp.diff(finB, _pp).subs(_pp, 0)
            pieces['dR'] = sp.expand(-_x * (1 - _x) * finB.subs(_pp, 0))   # from d ln Delta/dp^2 = -x(1-x)/Delta
        comp = {}
        for key, e in pieces.items():
            e = sp.expand(e)
            if tad:
                comp[key] = _poly_eval_factory(e, (_pp, _m1))
            else:
                if e == 0:
                    comp[key] = [[]]
                    continue
                poly = sp.Poly(e, _x)
                comp[key] = [_poly_eval_factory(poly.coeff_monomial(_x**j), (_pp, _m1, _m2)) for j in range(poly.degree() + 1)]
        out[name] = (tad, comp)
    return out


# =====================================================================================================
# 2. Feynman-parameter integrals in closed form (real part, ln|Delta|)
# =====================================================================================================
def _eps():
    return mp.mpf(10) ** (-mp.mp.dps - 5)


def _J(j, r):
    """int_0^1 x^j ln(x - r) dx, principal branch"""
    r = mp.mpc(r)
    if abs(r) > 4:
        s = mp.log(-r) / (j + 1)
        n, rn = 1, r
        while True:
            t = 1 / (n * rn * (j + n + 1))
            s -= t
            if abs(t) < _eps() * (1 + abs(s)):
                return s
            n += 1
            rn *= r
    s = (((1 - r ** (j + 1)) * mp.log(1 - r) if r != 1 else 0) + (r ** (j + 1) * mp.log(-r) if r != 0 else 0)) / (j + 1)
    return s - sum(r ** (j - i) / (i + 1) for i in range(j + 1)) / (j + 1)


def _Jinv(j, r):
    """int_0^1 x^j/(x - r) dx for real r outside [0, 1]"""
    if abs(r) > 4:
        s, n, rn = mp.mpf(0), 0, r
        while True:
            t = -1 / (rn * (j + n + 1))
            s += t
            if abs(t) < _eps() * (1 + abs(s)):
                return s
            n += 1
            rn *= r
    return sum(r ** (j - 1 - i) / (i + 1) for i in range(j)) + r ** j * mp.log(abs((1 - r) / r))


def _int_poly(poly):
    return sum(c / (j + 1) for j, c in enumerate(poly))


def _int_log(poly, A, a1, a2):
    """int_0^1 poly(x) ln|Delta|, Delta = A x^2 + (a2 - a1 - A) x + a1"""
    if all(c == 0 for c in poly):
        return mp.mpf(0)
    B, Cc = a2 - a1 - A, a1
    if A == 0:
        if B == 0:
            return mp.log(abs(Cc)) * _int_poly(poly)
        r = -Cc / B
        return sum(c * (mp.re(_J(j, r)) + mp.log(abs(B)) / (j + 1)) for j, c in enumerate(poly))
    disc = B * B - 4 * A * Cc
    if disc >= 0:
        sq = mp.sqrt(disc)
        q = -(B + (sq if B >= 0 else -sq)) / 2
        r1 = q / A
        r2 = Cc / q if q != 0 else mp.mpf(0)
    else:
        sq = mp.sqrt(-disc) * 1j
        r1, r2 = (-B + sq) / (2 * A), (-B - sq) / (2 * A)
    return sum(c * (mp.re(_J(j, r1) + _J(j, r2)) + mp.log(abs(A)) / (j + 1)) for j, c in enumerate(poly))


def _int_inv(poly, a1, a2):
    """int_0^1 poly(x)/Delta0, Delta0 = (a2 - a1) x + a1  (p^2 = 0)"""
    if all(c == 0 for c in poly):
        return mp.mpf(0)
    B = a2 - a1
    if B == 0:
        return _int_poly(poly) / a1
    r = -a1 / B
    if r == 0 or r == 1:                       # a massless line: Delta0 vanishes at an end point; divide exactly
        n = len(poly) - 1
        q = [0] * n
        acc = 0
        for j in range(n, 0, -1):
            acc = poly[n] if j == n else poly[j] + acc * r
            q[j - 1] = acc
        rem = poly[0] + q[0] * r
        assert abs(rem) <= mp.mpf(10) ** (-30) * (1 + max(abs(c) for c in poly)), 'infrared divergent dSigma/dp^2'
        return _int_poly(q) / B
    return sum(c * _Jinv(j, r) for j, c in enumerate(poly) if c != 0) / B


# =====================================================================================================
# 3. the model: Lagrangian parameters -> mass-basis couplings
# =====================================================================================================
_TAU = [[[0, 1], [1, 0]], [[0, -1j], [1j, 0]], [[1, 0], [0, -1]]]


def _real4(Mc):
    """complex 2x2 acting on Phi -> real 4x4 acting on (x1, y1, x2, y2), Phi_k = (x_k + i y_k)/sqrt2"""
    R = mp.zeros(4, 4)
    for k in range(2):
        for l in range(2):
            a, b = mp.re(Mc[k][l]), mp.im(Mc[k][l])
            R[2 * k, 2 * l] = a
            R[2 * k, 2 * l + 1] = -b
            R[2 * k + 1, 2 * l] = b
            R[2 * k + 1, 2 * l + 1] = a
    return R


def _eps3(a, b, c):
    return {(0, 1, 2): 1, (1, 2, 0): 1, (2, 0, 1): 1, (0, 2, 1): -1, (2, 1, 0): -1, (1, 0, 2): -1}.get((a, b, c), 0)


class _Model:
    """fields in the mass basis: gauge (W1, W2, Z, A), scalars (G_W1, G_W2, G_Z, H), ghosts like the gauge fields"""

    def __init__(self, MW, MZ, MH, alpha, xi, lam):
        MW, MZ, MH, alpha, xi, lam = [mp.mpf(t) for t in (MW, MZ, MH, alpha, xi, lam)]
        self.MW, self.MZ, self.MH, self.alpha, self.xi, self.lam = MW, MZ, MH, alpha, xi, lam
        e = mp.sqrt(4 * mp.pi * alpha)
        c = MW / MZ
        s = mp.sqrt(1 - c * c)
        g, gp = e / s, e / c
        v = 2 * MW / g
        self.e, self.c, self.s, self.g = e, c, s, g
        tiny = mp.mpf(10) ** (-35)
        # real-basis generators T^a (couplings included), a = W1 W2 W3 B; Higgs doublet Y = 1/2
        Ta = [_real4([[-1j * g * _TAU[a][k][l] / 2 for l in range(2)] for k in range(2)]) for a in range(3)]
        Ta.append(_real4([[(-0.5j * gp if k == l else 0) for l in range(2)] for k in range(2)]))
        Cr = [[[(g * _eps3(a, b, cc) if max(a, b, cc) < 3 else 0) for cc in range(4)] for b in range(4)] for a in range(4)]
        for a in range(4):
            for b in range(4):
                rhs = mp.zeros(4, 4)
                for cc in range(4):
                    rhs += Cr[a][b][cc] * Ta[cc]
                assert mp.mnorm(Ta[a] * Ta[b] - Ta[b] * Ta[a] - rhs) < tiny          # [T^a, T^b] = C^{abc} T^c
        # mass basis of the gauge fields: W3 = c Z + s A, B = -s Z + c A
        R = mp.zeros(4, 4)
        R[0, 0] = R[1, 1] = 1
        R[2, 2], R[2, 3], R[3, 2], R[3, 3] = c, s, -s, c
        TF = []
        for F in range(4):
            mt = mp.zeros(4, 4)
            for a in range(4):
                mt += R[a, F] * Ta[a]
            TF.append(mt)
        self.C = [[[sum(R[a, F] * R[b, G] * R[cc, H] * Cr[a][b][cc] for a in range(4) for b in range(4) for cc in range(4))
                    for H in range(4)] for G in range(4)] for F in range(4)]
        vev = mp.matrix([0, 0, v, 0])
        Fv = [TF[F] * vev for F in range(4)]                                       # F_a = T^a v
        M2 = [[sum(Fv[a][i] * Fv[b][i] for i in range(4)) for b in range(4)] for a in range(4)]
        for a in range(4):
            for b in range(4):
                tgt = [MW**2, MW**2, MZ**2, 0][a] if a == b else 0
                assert abs(M2[a][b] - tgt) < tiny * MZ**2                           # M_W = g v/2, M_Z, massless photon
        O = mp.zeros(4, 4)                                                         # Goldstones along F_a, Higgs along phi3
        for S in range(3):
            nrm = mp.sqrt(M2[S][S])
            for i in range(4):
                O[i, S] = Fv[S][i] / nrm
        O[2, 3] = 1
        assert mp.mnorm(O.T * O - mp.eye(4)) < tiny
        self.That = [O.T * TF[F] * O for F in range(4)]                            # V S S couplings
        self.cvvs = [[[sum(Fv[F][i] * (TF[V] * O.column(S))[i] + Fv[V][i] * (TF[F] * O.column(S))[i] for i in range(4))
                       for S in range(4)] for V in range(4)] for F in range(4)]  # V V S couplings
        self.M2 = [MW**2, MW**2, MZ**2, lam**2]
        self.Ms2 = [xi * MW**2, xi * MW**2, xi * MZ**2, MH**2]
        self.Mgh2 = [xi * MW**2, xi * MW**2, xi * MZ**2, xi * lam**2]
        # left-handed lepton doublet (nu, l), Y = -1/2: G^F = sum_a R_aF g_a t^a
        t = [mp.matrix([[_TAU[a][k][l] / 2 for l in range(2)] for k in range(2)]) for a in range(3)]
        Gr = [g * t[0], g * t[1], g * t[2], gp * mp.matrix([[-0.5, 0], [0, -0.5]])]
        self.Gf = []
        for F in range(4):
            mt = mp.zeros(2, 2)
            for a in range(4):
                mt += R[a, F] * Gr[a]
            self.Gf.append(mt)
        Qm = mp.matrix([[0, 0], [0, -1]])
        assert mp.mnorm(self.Gf[3] - e * Qm) < tiny and mp.mnorm(self.Gf[2] - (g / c) * (t[2] - s * s * Qm)) < tiny
        for a in range(4):
            for b in range(4):
                rhs = mp.zeros(2, 2)
                for cc in range(4):
                    rhs += 1j * self.C[a][b][cc] * self.Gf[cc]
                assert mp.mnorm(self.Gf[a] * self.Gf[b] - self.Gf[b] * self.Gf[a] - rhs) < tiny   # [G^a,G^b] = i C G

    def line_terms(self, V):
        """gauge propagator = sum of (numerator type, mass^2, coefficient)/(k^2 - mass^2)"""
        M2 = self.M2[V]
        return [('g', M2, -1j), ('k', M2, 1j / M2), ('k', self.xi * M2, -1j / M2)]


# =====================================================================================================
# 4. gauge-boson self-energies
# =====================================================================================================
class _Acc:
    def __init__(self, mode, ppv):
        self.mode, self.pp = mode, ppv
        self.groups = dict()
        self.tad = dict()

    def add(self, name, pref, a1, a2=None):
        tad, comp = _se_kernels()[name]
        ppv = self.pp if self.mode == 'val' else mp.mpf(0)
        if tad:
            if self.mode == 'deriv':
                return                                 # tadpoles do not depend on p^2
            acc = self.tad.setdefault(a1, [0, 0, 0])
            for n, key in enumerate(('P', 'A', 'B')):
                acc[n] += pref * _peval(comp[key], (ppv, a1))
            return
        acc = self.groups.setdefault((a1, a2), dict())
        for pc in (('P', 'A', 'B') if self.mode != 'deriv' else ('dP', 'dA', 'dB', 'dR')):
            cs = [_peval(cf, (ppv, a1, a2)) for cf in comp[pc]]
            lst = acc.setdefault(pc, [])
            while len(lst) < len(cs):
                lst.append(0)
            for j, cv in enumerate(cs):
                lst[j] += pref * cv

    def result(self):
        tol = mp.mpf(10) ** (-30)
        fin, pole = 0, 0
        cx = lambda f, poly, *a: f([mp.re(c) for c in poly], *a) + 1j * f([mp.im(c) for c in poly], *a)
        for a1, (P, A, B) in self.tad.items():
            pole += P
            fin += A
            if a1 != 0:
                fin += B * mp.log(a1)
            else:
                assert abs(B) < tol * (1 + abs(A))
        for (a1, a2), acc in self.groups.items():
            if self.mode != 'deriv':
                ppv = self.pp if self.mode == 'val' else mp.mpf(0)
                pole += _int_poly(acc['P'])
                fin += _int_poly(acc['A'])
                if ppv == 0 and a1 == 0 and a2 == 0:
                    assert all(abs(c) < tol for c in acc['B'])
                else:
                    fin += cx(_int_log, acc['B'], ppv, a1, a2)
            else:
                pole += _int_poly(acc['dP'])
                fin += _int_poly(acc['dA'])
                if a1 == 0 and a2 == 0:
                    assert all(abs(c) < tol for c in acc['dB'] + acc['dR']), 'infrared divergent dSigma/dp^2'
                else:
                    fin += cx(_int_log, acc['dB'], 0, a1, a2) + cx(_int_inv, acc['dR'], a1, a2)
        return fin, pole


def _sigma(m, F, G, mode='val', ppv=0):
    """Sigma_T^{FG}(p^2 = ppv) (mode 'val') or dSigma_T/dp^2 at 0 (mode 'deriv').  returns (finite at mu = 1, pole)"""
    acc = _Acc(mode, mp.mpf(ppv))
    N = range(4)
    C = m.C
    for V1 in N:                                                     # (1) gauge loop, symmetry 1/2
        for V2 in N:
            cf, cg = C[F][V1][V2], C[G][V1][V2]
            if cf == 0 or cg == 0:
                continue
            for t1, a1, c1 in m.line_terms(V1):
                for t2, a2, c2 in m.line_terms(V2):
                    acc.add('VV' + t1 + t2, mp.mpf(1) / 2 * cf * cg * c1 * c2, a1, a2)
    for V in N:                                                      # (2) gauge-scalar loop
        for S in N:
            cf, cg = m.cvvs[F][V][S], m.cvvs[G][V][S]
            if abs(cf) < 1e-40 or abs(cg) < 1e-40:
                continue
            for t, a1, c1 in m.line_terms(V):
                acc.add('VS' + t, 1j * 1j * 1j * c1 * cf * cg, a1, m.Ms2[S])
    for i in N:                                                      # (3) scalar loop, 1/2
        for j in N:
            tf, tg = m.That[F][i, j], m.That[G][i, j]
            if abs(tf) < 1e-40 or abs(tg) < 1e-40:
                continue
            acc.add('SS', mp.mpf(1) / 2 * tf * (-tg) * 1j * 1j, m.Ms2[i], m.Ms2[j])
    for a in N:                                                      # (4) ghost loop, -1
        for b in N:
            pr = C[F][b][a] * C[G][a][b]
            if pr != 0:
                acc.add('GH', -1 * 1j * 1j * pr, m.Mgh2[a], m.Mgh2[b])
    for V in N:                                                      # (5) quartic gauge tadpole
        for e_ in N:
            pr = C[F][V][e_] * C[G][V][e_]
            if pr == 0:
                continue
            for t, a1, c1 in m.line_terms(V):
                acc.add('VT' + t, -1j * pr * c1, a1)
    for S in N:                                                      # (6) V V S S tadpole
        pr = -sum(m.That[F][j, S] * m.That[G][j, S] for j in N)
        if abs(pr) > 1e-40:
            acc.add('ST', pr, m.Ms2[S])
    fin, pole = acc.result()
    k = -1 / (16 * mp.pi**2)          # Pi = pref/16pi^2 * K, Sigma_T = -Pi_T
    return mp.re(k * fin), mp.re(k * pole)


# =====================================================================================================
# 5. lepton diagrams at zero external momenta: d-dim Dirac algebra, vacuum integrals
# =====================================================================================================
class _DT:
    __slots__ = ('c', 'g', 'v', 's', 'kpow')

    def __init__(self, c, g, v, s, kpow=0):
        self.c, self.g, self.v, self.s, self.kpow = c, list(g), list(v), [list(q) for q in s], kpow


def _pairings(lst):
    if not lst:
        yield []
        return
    for i in range(1, len(lst)):
        for p in _pairings(lst[1:i] + lst[i + 1:]):
            yield [(lst[0], lst[i])] + p


def _average_k(t):
    """k^{a1}..k^{a2n} -> (k^2)^n/(d(d+2)..(d+2n-2)) sum over pairings of metrics"""
    ks = [i for (vec, i) in t.v if vec == 'k']
    others = [(vec, i) for (vec, i) in t.v if vec != 'k']
    if len(ks) % 2:
        return []
    n = len(ks) // 2
    fac = _avg(n) / _dfact2(n)            # each of the (2n-1)!! pairings carries 1/(d(d+2)..(d+2n-2))
    return [_DT(t.c * fac, t.g + list(pr), others, t.s, t.kpow + n) for pr in _pairings(ks)]


def _rename(t, a, b):
    t.g = [(b if i == a else i, b if j == a else j) for (i, j) in t.g]
    t.v = [(vec, b if i == a else i) for (vec, i) in t.v]
    t.s = [[b if i == a else i for i in st] for st in t.s]


def _contract_metrics(t):
    changed = True
    while changed:
        changed = False
        for n, (i, j) in enumerate(t.g):
            if i == j:
                t.g.pop(n)
                t.c = t.c * _d
                changed = True
                break

            def occ(idx):
                return (any(idx in (a, b) for m, (a, b) in enumerate(t.g) if m != n) or any(idx == ii for _, ii in t.v)
                        or any(idx in st for st in t.s))
            if occ(j):
                t.g.pop(n)
                _rename(t, j, i)
                changed = True
                break
            if occ(i):
                t.g.pop(n)
                _rename(t, i, j)
                changed = True
                break
    return t


def _reduce_string(st):
    """d-dimensional reduction of a gamma string with contracted index pairs (anticommutation only)"""
    pos = dict()
    for n, i in enumerate(st):
        if i in pos:
            a, b = pos[i], n
            break
        pos[i] = n
    else:
        return [(sp.Integer(1), tuple(st))]
    if b == a + 1:                                                   # gamma^a gamma_a = d
        return [(c * _d, s2) for c, s2 in _reduce_string(st[:a] + st[b + 1:])]
    x_, y_ = st[b - 1], st[b]                                        # gamma^x gamma^y = 2 g^{xy} - gamma^y gamma^x
    s1 = st[:b - 1] + st[b + 1:]
    s1 = [x_ if k == a else s1[k] for k in range(len(s1))]
    out = [(2 * c, s2) for c, s2 in _reduce_string(s1)]
    out += [(-c, s3) for c, s3 in _reduce_string(st[:b - 1] + [y_, x_] + st[b + 1:])]
    return out


def _reduce_single(t):
    res = []
    for t1 in _average_k(t):
        _contract_metrics(t1)
        for c, s2 in _reduce_string(t1.s[0]):
            t2 = _DT(t1.c * c, t1.g, t1.v, [s2], t1.kpow)
            _contract_metrics(t2)
            assert not t2.g and len(t2.s[0]) == 1                   # result proportional to gamma^alpha or pslash
            res.append(t2)
    return res


def _by_kpow(terms):
    out = dict()
    for t in terms:
        out[t.kpow] = out.get(t.kpow, 0) + t.c
    return {kp: (sp.Rational(sp.simplify(R).subs(_d, 4)), sp.Rational(sp.simplify(sp.diff(R, _d)).subs(_d, 4)))
            for kp, R in out.items() if sp.simplify(R) != 0}


def _dline(t, i, j):
    return ([(i, j)], []) if t == 'g' else ([], [('k', i), ('k', j)])


_GAM = None


def _gammas():
    global _GAM
    if _GAM is None:
        I2, Z2 = np.eye(2), np.zeros((2, 2))
        sig = [np.array([[0, 1], [1, 0]]), np.array([[0, -1j], [1j, 0]]), np.array([[1, 0], [0, -1]])]
        gam = [np.block([[Z2, I2], [I2, Z2]]).astype(complex)] + [np.block([[Z2, q], [-q, Z2]]).astype(complex) for q in sig]
        g5 = 1j * gam[0] @ gam[1] @ gam[2] @ gam[3]
        _GAM = (gam, (np.eye(4) - g5) / 2, [1, -1, -1, -1])
    return _GAM


def _box_struct(tx, ty, topo):
    """(line 1: gamma^b (-kslash) gamma^a) x (line 2), reduced in 4 dimensions to r gamma P_L x gamma P_L"""
    gam, PL, eta = _gammas()
    gx, vx = _dline(tx, 'a', 'A')
    gy, vy = _dline(ty, 'b', 'B')
    s2, sign = (['B', 'K2', 'A'], -1) if topo == 1 else (['A', 'K2', 'B'], 1)
    T = _DT(sp.Integer(sign), gx + gy, vx + vy + [('k', 'K1'), ('k', 'K2')], [['b', 'K1', 'a'], s2])
    E = sum(eta[m] * np.kron(gam[m] @ PL, gam[m] @ PL) for m in range(4))
    out = dict()
    for t1 in _average_k(T):
        _contract_metrics(t1)
        assert not t1.v and not t1.g
        idx = sorted(set(t1.s[0] + t1.s[1]))
        M = np.zeros((16, 16), complex)
        for vals in itertools.product(range(4), repeat=len(idx)):
            asg = dict(zip(idx, vals))
            w = 1
            for i in idx:
                w *= eta[asg[i]]
            A1 = np.eye(4, dtype=complex)
            for i in t1.s[0]:
                A1 = A1 @ gam[asg[i]]
            A2 = np.eye(4, dtype=complex)
            for i in t1.s[1]:
                A2 = A2 @ gam[asg[i]]
            M += w * np.kron(A1 @ PL, A2 @ PL)
        r = complex(np.vdot(E, M) / np.vdot(E, E))
        assert np.abs(M - r * E).max() < 1e-9 and abs(r.imag) < 1e-12 and abs(r.real - round(r.real)) < 1e-9
        out[t1.kpow] = out.get(t1.kpow, 0) + t1.c * int(round(r.real))
    return {kp: (sp.Rational(sp.simplify(R).subs(_d, 4)), sp.Rational(sp.simplify(sp.diff(R, _d)).subs(_d, 4)))
            for kp, R in out.items() if sp.simplify(R) != 0}


@functools.lru_cache(maxsize=None)
def _lep_structs():
    st = dict()
    for t in 'gk':
        g, v = _dline(t, 's', 'r')
        # vertex (A): gamma^s (-k) gamma^alpha (-k) gamma^r L_sr
        st['A' + t] = _by_kpow(_reduce_single(_DT(sp.Integer(1), g, v + [('k', 'K1'), ('k', 'K2')], [['s', 'K1', 'alpha', 'K2', 'r']])))
        # self-energy to O(p): gamma^s [pslash/k^2 - 2 kslash (k.p)/k^4] gamma^r L_sr
        st['W1' + t] = _by_kpow(_reduce_single(_DT(sp.Integer(1), g, v + [('p', 'P1')], [['s', 'P1', 'r']])))
        st['W2' + t] = _by_kpow(_reduce_single(_DT(sp.Integer(-2), g, v + [('k', 'K1'), ('k', 'Q1'), ('p', 'Q1')], [['s', 'K1', 'r']])))
        for t2 in 'gk':
            # vertex (B): gamma^s (-k) gamma^r L1_rb L2_sc V3_{alpha b c}(0, k, -k)
            g1, v1 = _dline(t, 'r', 'b')
            g2, v2 = _dline(t2, 's', 'c')
            terms = []
            for coef, gg, vv in ((-1, [('alpha', 'b')], [('k', 'c')]), (2, [('b', 'c')], [('k', 'alpha')]), (-1, [('c', 'alpha')], [('k', 'b')])):
                terms += _reduce_single(_DT(sp.Integer(-coef), g1 + g2 + gg, v1 + v2 + vv + [('k', 'K1')], [['s', 'K1', 'r']]))
            st['B' + t + t2] = _by_kpow(terms)
            for topo in (1, 2):
                st['X%s%s%d' % (t, t2, topo)] = _box_struct(t, t2, topo)
    return st


def _vac(n, poles):
    """int d^dk/(2pi)^d (k^2)^n / prod (k^2 - m)^a  = i/16pi^2 (P/epsbar + F) at mu = 1  (partial fractions in k^2)"""
    P, F = mp.mpf(0), mp.mpf(0)
    ms = list(poles.items())
    for idx, (m, a) in enumerate(ms):
        ser = [mp.mpf(0)] * a
        for s in range(min(n, a - 1) + 1):
            ser[s] = mp.binomial(n, s) * (m ** (n - s) if n - s > 0 else 1)
        for jdx, (mo, ao) in enumerate(ms):
            if jdx == idx:
                continue
            dl = m - mo
            fs = [mp.binomial(-ao, s) * dl ** (-ao - s) for s in range(a)]
            ser = [sum(ser[i] * fs[s - i] for i in range(s + 1)) for s in range(a)]
        for s in range(a):
            q, cq = a - s, ser[s]
            if cq == 0:
                continue
            if m == 0:
                if q >= 2:
                    raise ValueError('infrared divergent vacuum integral')
                continue                                              # scaleless
            if q == 1:
                P += cq * m
                F += cq * m * (1 - mp.log(m))
            elif q == 2:
                P += cq
                F -= cq * mp.log(m)
            else:
                F += cq * (-1) ** q / ((q - 1) * (q - 2)) * m ** (2 - q)
    return P, F


def _integ(name, ferm, masses):
    """sum_structures R(d) int (k^2)^kpow / ((k^2)^ferm prod (k^2 - m)); O(eps) of R(d) kept against the pole"""
    P, F = mp.mpf(0), mp.mpf(0)
    for kp, (R4, R1) in _lep_structs()[name].items():
        R4 = mp.mpf(R4.p) / R4.q
        R1 = mp.mpf(R1.p) / R1.q
        n, a0 = kp, ferm
        cut = min(n, a0)
        n, a0 = n - cut, a0 - cut
        poles = dict()
        if a0:
            poles[mp.mpf(0)] = a0
        for mm in masses:
            poles[mp.mpf(mm)] = poles.get(mp.mpf(mm), 0) + 1
        p, f = _vac(n, poles)
        P += R4 * p
        F += R4 * f - 2 * R1 * p
    return P, F


def _lepton_parts(m):
    """K: lepton self-energy matrix (1PI = i pslash K P_L); dLam[X]: vertex correction (1PI = i gamma^alpha dLam P_L);
    box: coefficient of gamma P_L x gamma P_L.  each as [finite at mu = 1, pole]"""
    N = range(4)
    Gf, C = m.Gf, m.C
    I = mp.mpc(0, 1)
    k16 = I / (16 * mp.pi**2)
    K = [mp.zeros(2, 2), mp.zeros(2, 2)]
    for V in N:
        for t, a, ct in m.line_terms(V):
            for nm, ferm in (('W1' + t, 1), ('W2' + t, 2)):
                P, F = _integ(nm, ferm, [a])
                val = I**3 * ct * k16 / I
                K[0] += val * F * (Gf[V] * Gf[V])
                K[1] += val * P * (Gf[V] * Gf[V])
    dLam = dict()
    for X in N:
        Lm = [mp.zeros(2, 2), mp.zeros(2, 2)]
        for V in N:                                                  # (A)
            for t, a, ct in m.line_terms(V):
                P, F = _integ('A' + t, 2, [a])
                Mx = Gf[V] * Gf[X] * Gf[V]
                val = I**5 * ct * k16 / I
                Lm[0] += val * F * Mx
                Lm[1] += val * P * Mx
        for V1 in N:                                                 # (B)
            for V2 in N:
                cc = C[X][V1][V2]
                if cc == 0:
                    continue
                Mx = Gf[V2] * Gf[V1]
                for t1, a1, c1 in m.line_terms(V1):
                    for t2, a2, c2 in m.line_terms(V2):
                        P, F = _integ('B' + t1 + t2, 1, [a1, a2])
                        val = I**3 * c1 * c2 * cc * k16 / I
                        Lm[0] += val * F * Mx
                        Lm[1] += val * P * Mx
        dLam[X] = Lm
    box = [mp.mpc(0), mp.mpc(0)]
    for X in N:
        for Y in N:
            l1 = (Gf[Y] * Gf[X])[0, 1]
            if l1 == 0:
                continue
            for topo in (1, 2):
                l2 = (Gf[Y] * Gf[X])[1, 0] if topo == 1 else (Gf[X] * Gf[Y])[1, 0]
                if l2 == 0:
                    continue
                for tx, ax, cx in m.line_terms(X):
                    for ty, ay, cy in m.line_terms(Y):
                        P, F = _integ('X%s%s%d' % (tx, ty, topo), 2, [ax, ay])
                        pref = I**6 * cx * cy * l1 * l2 * k16
                        box[0] += pref * F
                        box[1] += pref * P
    return K, dLam, box


# =====================================================================================================
# 6. assembly
# =====================================================================================================
def _classes_at(MW, MZ, MH, alpha, xi, lam):
    """returns dict of (finite at mu = 1, pole) for the pieces"""
    m = _Model(MW, MZ, MH, alpha, xi, lam)
    W, Z, A = 0, 2, 3
    s, c = m.s, m.c
    aad = _sigma(m, A, A, 'deriv')
    az = _sigma(m, A, Z, 'val', 0)
    w0 = _sigma(m, W, W, 'val', 0)
    wm = _sigma(m, W, W, 'val', m.MW**2)
    zm = _sigma(m, Z, Z, 'val', m.MZ**2)
    K, dLam, box = _lepton_parts(m)
    Gf = m.Gf
    tree = sum(Gf[a][0, 1] * Gf[a][1, 0] for a in (0, 1))
    Ttree = -1j / m.MW**2 * tree
    out = dict()
    for k in (0, 1):
        dZe = aad[k] / 2 + s / c * az[k] / m.MZ**2                       # Thomson charge (Ward identity, checked)
        ds2 = c * c / (s * s) * (zm[k] / m.MZ**2 - wm[k] / m.MW**2)     # delta s^2 / s^2
        se = 2 * dZe - ds2 + (w0[k] - wm[k]) / m.MW**2
        vert = sum(dLam[a][k][0, 1] * Gf[a][1, 0] + Gf[a][0, 1] * dLam[a][k][1, 0] for a in (0, 1)) / tree
        wfc = -(K[k][0, 0] + K[k][1, 1])
        bx = box[k] / Ttree
        fermi = 0                                                          # charge-retention Fermi QED at q = 0: Ward identity
        parts = dict(SE=se, VBW=vert + wfc + bx - fermi, AAp=aad[k], AZ0=az[k] / m.MZ**2, W0=w0[k] / m.MW**2,
                     WM=wm[k] / m.MW**2, ZM=zm[k] / m.MZ**2, dZe=dZe, vertex=vert, wf=wfc, box=bx)
        for key, val in parts.items():
            out.setdefault(key, [0, 0])[k] = mp.re(val)
    return out


@functools.lru_cache(maxsize=256)
def _classes_unit(MW, MZ, MH, xi):
    """pieces per unit alpha: (finite at mu = 1, pole, IR log coefficient b) with the photon-mass dependence
    a + b ln lambda^2 extracted from two tiny lambda; the IR pole is subtracted in MS-bar (ln lambda^2 -> ln mu^2 + 1)"""
    with mp.workdps(_DPS):
        l1, l2 = mp.mpf(_LAMBDAS[0]), mp.mpf(_LAMBDAS[1])
        r1 = _classes_at(MW, MZ, MH, 1, xi, l1)
        r2 = _classes_at(MW, MZ, MH, 1, xi, l2)
        out = dict()
        for key in r1:
            b = (r1[key][0] - r2[key][0]) / (2 * mp.log(l1) - 2 * mp.log(l2))
            a = r1[key][0] - b * 2 * mp.log(l1)
            out[key] = (a + b, r1[key][1], b)          # value at mu = 1 after ln lambda^2 -> ln mu^2 + 1
        return out


def _piece(key, MW, MZ, MH, alpha, xi, mu):
    with mp.workdps(_DPS):
        fin, pole, b = _classes_unit(float(MW), float(MZ), float(MH), float(xi))[key]
        lmu = 2 * mp.log(mp.mpf(mu))
        return float(mp.mpf(alpha) * (fin + (pole + b) * lmu))


def delta_r_se(MW, MZ, MH, alpha, xi, mu):
    """class SE: 2 dZ_e - delta s^2/s^2 + (Sigma^W(0) - Sigma^W(M_W^2))/M_W^2, MS-bar at mu"""
    return _piece('SE', MW, MZ, MH, alpha, xi, mu)


def delta_r_vbw(MW, MZ, alpha, xi, mu):
    """class VBW: W-lepton vertices + boxes + lepton legs - Fermi photonic correction, MS-bar at mu (no M_H dependence)"""
    return _piece('VBW', MW, MZ, 125.0, alpha, xi, mu)


def delta_r_bos_xi(MW, MZ, MH, alpha, xi):
    """total bosonic one-loop Delta r (UV finite, mu and xi independent)"""
    with mp.workdps(_DPS):
        se = _classes_unit(float(MW), float(MZ), float(MH), float(xi))['SE']
        vb = _classes_unit(float(MW), float(MZ), 125.0, float(xi))['VBW']
        return float(mp.mpf(alpha) * (se[0] + vb[0] + (se[1] + vb[1] + se[2] + vb[2]) * 2 * mp.log(mp.mpf(MW))))


PROVENANCE = {
    'delta_r_se': ('derived', 'gauge-boson self-energies in R_xi from the Lagrangian (real-basis generators rotated to mass '
                              'eigenstates), Feynman-parameter integrals in closed form; on-shell masses, mixing angle, Thomson '
                              'charge dZ_e = Sigma_AA\'(0)/2 + (s/c) Sigma_AZ(0)/M_Z^2 (verified by the direct q=0 vertex); MS-bar'),
    'delta_r_vbw': ('derived', 'W-lepton vertices (abelian + non-abelian), W-Z and W-photon boxes, lepton legs at zero momenta; '
                               'd-dim Dirac algebra, vacuum integrals by partial fractions; charge-retention Fermi QED subtraction '
                               '(zero at q = 0 by the Ward identity); MS-bar'),
    'delta_r_bos_xi': ('derived', 'SE + VBW; UV poles, mu and xi dependence cancel'),
}


if __name__ == '__main__':
    MW, MZ, MH, AL = 80.38, 91.19, 125.0, 1 / 128.0
    print('main route: total Delta r_bos for several xi')
    for xi in (0.0, 0.3, 1.0, 4.0, 25.0, 1000.0):
        se, vb = delta_r_se(MW, MZ, MH, AL, xi, MW), delta_r_vbw(MW, MZ, AL, xi, MW)
        print('  xi = %-7g  SE = % .12f  VBW = % .12f  total = % .15f' % (xi, se, vb, delta_r_bos_xi(MW, MZ, MH, AL, xi)))
    with mp.workdps(_DPS):
        print('second route (a): direct Thomson-limit photon-lepton vertex vs dZ_e of the Ward identity')
        for xi in (0.0, 1.0, 7.0):
            m = _Model(MW, MZ, MH, AL, xi, mp.mpf('1e-12'))
            K, dLam, box = _lepton_parts(m)
            aad, az = _sigma(m, 3, 3, 'deriv'), _sigma(m, 3, 2, 'val', 0)
            G = m.Gf
            for k, lab in ((0, 'finite'), (1, 'pole')):
                eff = dLam[3][k] - (K[k] * G[3] + G[3] * K[k]) / 2 + az[k] / m.MZ**2 * G[2] - aad[k] / 2 * G[3]
                dze_direct = -eff[1, 1] / G[3][1, 1]
                dze_ward = aad[k] / 2 + m.s / m.c * az[k] / m.MZ**2
                print('  xi = %-4g %-6s neutrino charge shift = %.1e   dZe direct = %.15f   Ward = %.15f'
                      % (xi, lab, abs(eff[0, 0]), float(mp.re(dze_direct)), float(dze_ward)))
        print('second route (b): xi = 1 VBW from the hand-reduced closed form (DERIVATION 9)')
        m = _Model(MW, MZ, MH, AL, 1, mp.mpf('1e-12'))
        e, g, s, c, lam = m.e, m.g, m.s, m.c, m.lam
        gn, gl = g / c / 2, g / c * (s * s - mp.mpf(1) / 2)
        Sx = lambda M2: -mp.mpf(1) / 2 - mp.log(M2 / mp.mpf(MW) ** 2)
        B0 = lambda a, b: 1 - (a * mp.log(a / MW**2) - b * mp.log(b / MW**2)) / (a - b) if b != 0 else 1 - mp.log(a / MW**2)
        W2, Z2 = mp.mpf(MW)**2, mp.mpf(MZ)**2
        tot = (2 * (gn * gl * Sx(Z2) + g**2 * (c**2 * (3 * B0(W2, Z2) - mp.mpf(1) / 2) + s**2 * (3 * B0(W2, 0) - mp.mpf(1) / 2)))
               - (Sx(Z2) * (gn**2 + gl**2) + e**2 * Sx(lam**2) + g**2 * Sx(W2))
               - W2 * mp.log(Z2 / W2) / (W2 - Z2) * (gn**2 + gl**2 - 8 * gn * gl) + e**2 * mp.log(W2 / lam**2)) / (16 * mp.pi**2)
        print('  closed form VBW(xi=1, mu=MW) = %.15f   code = %.15f' % (float(tot), delta_r_vbw(MW, MZ, AL, 1.0, MW)))
        s2 = s * s
        print('  closed form VBW = alpha/(4 pi s^2) [6 + (7-4s^2)/(2 s^2) ln c^2] at mu = M_W: %.15f'
              % float(AL / (4 * mp.pi * s2) * (6 + (7 - 4 * s2) / (2 * s2) * mp.log(c * c))))
