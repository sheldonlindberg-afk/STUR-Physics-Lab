"""dr_xi: bosonic one-loop Delta r in the general R_xi gauge, derived from the Lagrangian (see DERIVATION.md).

Everything below is generated: Feynman rules from the Lagrangian, diagrams, tensor/Dirac reduction,
scalar integrals. No numerical result is typed in."""
import itertools
import functools
import math
import sympy as sp
import mpmath as mp
import numpy as np


# ====================================================================================================
# Lorentz algebra (d-dimensional metric, vectors q and p)
# ====================================================================================================

d = sp.Symbol('d')
Q2, QP, P2 = sp.symbols('Q2 QP P2')
DOT = {('q', 'q'): Q2, ('p', 'q'): QP, ('q', 'p'): QP, ('p', 'p'): P2}

_cnt = itertools.count()


def fresh(base='i'):
    return f"{base}{next(_cnt)}"


# ---------------------------------------------------------------- Lorentz expressions
# term: tuple of factors; factor ('g', i, j) (i<j) or ('v', name, i)
def _contract(factors):
    coef = sp.Integer(1)
    fs = list(factors)
    while True:
        pos = {}
        hit = None
        for n, f in enumerate(fs):
            idxs = (f[1], f[2]) if f[0] == 'g' else (f[2],)
            for i in idxs:
                if i in pos:
                    hit = (pos[i], n, i)
                    break
                pos[i] = n
            if hit:
                break
        if hit is None:
            break
        a, b, i = hit
        if a == b:                      # g(i,i)
            fs.pop(a)
            coef *= d
            continue
        fa, fb = fs[a], fs[b]
        for n in sorted((a, b), reverse=True):
            fs.pop(n)
        if fa[0] == 'g' and fb[0] == 'g':
            oa = fa[2] if fa[1] == i else fa[1]
            ob = fb[2] if fb[1] == i else fb[1]
            if oa == ob:
                coef *= d
            else:
                fs.append(('g',) + tuple(sorted((oa, ob))))
        elif fa[0] == 'g' or fb[0] == 'g':
            g_, v_ = (fa, fb) if fa[0] == 'g' else (fb, fa)
            o = g_[2] if g_[1] == i else g_[1]
            fs.append(('v', v_[1], o))
        else:
            coef *= DOT[(fa[1], fb[1])]
    fs.sort()
    return coef, tuple(fs)


class L:
    __slots__ = ('t',)

    def __init__(self, t=None):
        self.t = t if t is not None else {}

    @staticmethod
    def scalar(c):
        return L({(): sp.sympify(c)}) if c != 0 else L()

    def __add__(self, o):
        r = dict(self.t)
        for k, v in o.t.items():
            r[k] = r.get(k, 0) + v
        return L(r)

    def __mul__(self, o):
        if not isinstance(o, L):
            o = sp.sympify(o)
            return L({k: v * o for k, v in self.t.items()})
        r = {}
        for k1, v1 in self.t.items():
            for k2, v2 in o.t.items():
                c, k = _contract(k1 + k2)
                r[k] = r.get(k, 0) + c * v1 * v2
        return L(r)

    __rmul__ = __mul__

    def simplify(self):
        r = {}
        for k, v in self.t.items():
            v = sp.expand(v)
            if v != 0:
                r[k] = v
        return L(r)


def g(i, j):
    return L({(('g',) + tuple(sorted((i, j))),): sp.Integer(1)})


def vec(mom, i):
    """mom: dict {'q': a, 'p': b}"""
    r = {}
    for n, c in mom.items():
        if c != 0:
            r[(('v', n, i),)] = sp.sympify(c)
    return L(r)


def mom_sq(mom):
    a, b = mom.get('q', 0), mom.get('p', 0)
    return sp.expand(a * a * Q2 + 2 * a * b * QP + b * b * P2)


# ====================================================================================================
# The Lagrangian (SPEC 1): scalar kinetic term, potential, Yang-Mills, gauge fixing, Faddeev-Popov, leptons
# ====================================================================================================

I = sp.I
gg, gp, v, lam, xi = sp.symbols('g gp v lam xi', positive=True)
cw, sw = sp.symbols('c s', positive=True)
r2 = sp.sqrt(2)

VEC = ['A', 'Z', 'Wp', 'Wm']
SCA = ['H', 'chi', 'php', 'phm']
GH = ['uA', 'uZ', 'up', 'um']
AGH = ['bA', 'bZ', 'bp', 'bm']

# real gauge basis (W1, W2, W3, B) in terms of mass fields
U = {0: {'Wp': 1 / r2, 'Wm': 1 / r2},
     1: {'Wp': I / r2, 'Wm': -I / r2},
     2: {'Z': cw, 'A': sw},
     3: {'Z': -sw, 'A': cw}}
GA = [gg, gg, gg, gp]
sig = [sp.Matrix([[0, 1], [1, 0]]), sp.Matrix([[0, -I], [I, 0]]), sp.Matrix([[1, 0], [0, -1]])]
tdoub = [s_ / 2 for s_ in sig] + [sp.Rational(1, 2) * sp.eye(2)]   # Higgs: Y = 1/2


def eps3(a, b, c):
    return sp.LeviCivita(a, b, c)


# ---------------------------------------------------------------- scalar sector, as commuting symbols
fsym = {n: sp.Symbol(n) for n in VEC + SCA}
dsym = {n: sp.Symbol('d_' + n) for n in SCA}
Vreal = [sum(cf * fsym[f] for f, cf in U[A].items()) for A in range(4)]


def kinetic_poly(Vr):
    Phi = sp.Matrix([fsym['php'], (v + fsym['H'] + I * fsym['chi']) / r2])
    Phid = sp.Matrix([[fsym['phm'], (v + fsym['H'] - I * fsym['chi']) / r2]])
    dPhi = sp.Matrix([dsym['php'], (dsym['H'] + I * dsym['chi']) / r2])
    dPhid = sp.Matrix([[dsym['phm'], (dsym['H'] - I * dsym['chi']) / r2]])
    M = sp.zeros(2, 2)
    for A in range(4):
        M += GA[A] * Vr[A] * tdoub[A]
    X = dPhi - I * M * Phi
    Xd = dPhid + I * Phid * M
    return sp.expand((Xd * X)[0, 0])


def potential_poly():
    Phi2 = fsym['phm'] * fsym['php'] + ((v + fsym['H']) ** 2 + fsym['chi'] ** 2) / 2
    mu2 = lam * v ** 2
    return sp.expand(mu2 * Phi2 - lam * Phi2 ** 2)      # = -V


def poly_to_monomials(poly, vecobjs):
    """Split a polynomial in field symbols into monomials with Lorentz slots.
    vecobjs: symbols carrying a Lorentz index (vector fields and derivatives of scalars).
    Each monomial has 0 or 2 vector objects, contracted with each other."""
    out = []
    P = sp.Poly(poly, *(list(fsym.values()) + list(dsym.values())))
    gens = P.gens
    for powers, coef in P.terms():
        slots = []
        nvec = 0
        idx = 'a'
        for gsym, pw in zip(gens, powers):
            name = str(gsym)
            for _ in range(pw):
                if name.startswith('d_'):
                    slots.append((name[2:], idx, None)); nvec += 1
                elif name in VEC:
                    slots.append((name, None, idx)); nvec += 1
                else:
                    slots.append((name, None, None))
        assert nvec in (0, 2), (powers, nvec)
        out.append((sp.nsimplify(coef) if coef.is_number else coef, tuple(slots)))
    return out


# ---------------------------------------------------------------- Yang-Mills
def ym_monomials():
    out = []
    # cubic: -g eps^{abc} (d_al W^a_be) W^b_al W^c_be
    for a, b, c in itertools.permutations(range(3)):
        e = eps3(a, b, c)
        for X, ux in U[a].items():
            for Y, uy in U[b].items():
                for Z_, uz in U[c].items():
                    out.append((-gg * e * ux * uy * uz, ((X, 'a', 'b'), (Y, None, 'a'), (Z_, None, 'b'))))
    # quartic: -(1/4) g^2 eps^{abe} eps^{cde} W^a_al W^b_be W^c_al W^d_be
    for a, b, c, dd in itertools.product(range(3), repeat=4):
        cf = sum(eps3(a, b, e_) * eps3(c, dd, e_) for e_ in range(3))
        if cf == 0:
            continue
        for X, ux in U[a].items():
            for Y, uy in U[b].items():
                for Z_, uz in U[c].items():
                    for W_, uw in U[dd].items():
                        out.append((-gg ** 2 / 4 * cf * ux * uy * uz * uw,
                                    ((X, None, 'a'), (Y, None, 'b'), (Z_, None, 'a'), (W_, None, 'b'))))
    return out


def collect(monos):
    """merge identical (sorted-slot) monomials"""
    acc = {}
    for cf, slots in monos:
        key = tuple(sorted(slots, key=lambda s_: (s_[0], str(s_[1]), str(s_[2]))))
        # canonical index renaming
        ren = {}
        def rn(x):
            if x is None:
                return None
            if x not in ren:
                ren[x] = 'l%d' % len(ren)
            return ren[x]
        key = tuple((f, rn(a), rn(b)) for f, a, b in key)
        acc[key] = acc.get(key, 0) + cf
    return [(sp.simplify(v_), k) for k, v_ in acc.items() if sp.simplify(v_) != 0]


# ---------------------------------------------------------------- gauge fixing / ghosts
def mixing_and_ghost():
    Vr = sp.symbols('V0:4')
    kin = kinetic_poly(list(Vr))
    # K_{A r}: coefficient of V^A * dS_r (v-linear, no other field)
    K = {}
    for A in range(4):
        for r in SCA:
            cf = sp.expand(kin).coeff(Vr[A], 1).coeff(dsym[r], 1)
            cf = cf.subs({fsym[n]: 0 for n in SCA})
            K[(A, r)] = sp.simplify(cf)
    GS = [sum(K[(A, r)] * fsym[r] for r in SCA) for A in range(4)]     # G_A . S
    # gauge variation of scalars: dPhi = i sum_B gB th^B t^B Phi
    th = sp.symbols('th0:4')
    Phi = sp.Matrix([fsym['php'], (v + fsym['H'] + I * fsym['chi']) / r2])
    Phid = sp.Matrix([[fsym['phm'], (v + fsym['H'] - I * fsym['chi']) / r2]])
    dP = sp.zeros(2, 1); dPd = sp.zeros(1, 2)
    for B in range(4):
        dP += I * GA[B] * th[B] * tdoub[B] * Phi
        dPd += -I * GA[B] * th[B] * Phid * tdoub[B]
    dS = {'php': dP[0], 'phm': dPd[0],
          'H': (dP[1] + dPd[1]) / r2, 'chi': (dP[1] - dPd[1]) / (r2 * I)}
    R = {(r, B): sp.expand(dS[r]).coeff(th[B]) for r in SCA for B in range(4)}
    return K, GS, R


def ghost_monomials(K, R):
    """L_FP = (d cbar^A).(g f^{ABC} V^B c^C) + xi cbar^A G_{Ar} R_{rB}(S) c^B (field part); quadratic part returned separately"""
    out = []
    GN = {'A': 'A', 'Z': 'Z', 'Wp': 'p', 'Wm': 'm'}
    ub = {A: {'b' + GN[f]: cf for f, cf in U[A].items()} for A in range(4)}
    uc = {A: {'u' + GN[f]: cf for f, cf in U[A].items()} for A in range(4)}
    for A, B, C in itertools.permutations(range(3)):
        e = eps3(A, B, C)
        for X, ux in ub[A].items():
            for Y, uy in U[B].items():
                for Z_, uz in uc[C].items():
                    out.append((gg * e * ux * uy * uz, ((X, 'a', None), (Y, None, 'a'), (Z_, None, None))))
    quad = []
    for A in range(4):
        for B in range(4):
            GR = sp.expand(sum(K[(A, r)] * R[(r, B)] for r in SCA))
            GRv = GR.subs({fsym[n]: 0 for n in SCA})
            GRf = sp.expand(GR - GRv)
            for X, ux in ub[A].items():
                for Z_, uz in uc[B].items():
                    if GRv != 0:
                        quad.append((xi * GRv * ux * uz, X, Z_))
                    for sname in SCA:
                        cf = GRf.coeff(fsym[sname])
                        if cf != 0:
                            out.append((xi * cf * ux * uz, ((X, None, None), (sname, None, None), (Z_, None, None))))
    return out, quad


def fermion_couplings():
    """returns dict (fbar, f, V) -> (cL, cR): vertex i gamma^mu (cL P_L + cR P_R)"""
    tl = [s_ / 2 for s_ in sig] + [-sp.Rational(1, 2) * sp.eye(2)]
    names = ['nu', 'l']
    out = {}
    for X in VEC:
        M = sp.zeros(2, 2)
        for A in range(4):
            M += GA[A] * U[A].get(X, 0) * tl[A]
        for i in range(2):
            for j in range(2):
                cL = sp.simplify(M[i, j])
                cR = sp.simplify(gp * (-1) * U[3].get(X, 0)) if (i == 1 and j == 1) else 0
                if cL != 0 or cR != 0:
                    out[(names[i], names[j], X)] = (cL, cR)
    return out


# ====================================================================================================
# Mass-basis vertices (i x functional derivative), propagators
# ====================================================================================================

e, MW, MH, L2 = sp.symbols('e MW MH L2', positive=True)
MZ = MW / cw
SUBS1 = {gp: gg * sw / cw, lam: MH ** 2 * gg ** 2 / (8 * MW ** 2)}
SUBS2 = {v: 2 * MW / gg}
SUBS3 = {gg: e / sw}


def scred(x):
    """reduce modulo s^2 + c^2 - 1"""
    x = sp.together(sp.expand(x))
    nu, de = sp.fraction(x)
    G = [sw ** 2 + cw ** 2 - 1]
    nu = sp.reduced(sp.expand(nu), G, sw, cw)[1]
    de = sp.reduced(sp.expand(de), G, sw, cw)[1]
    return sp.factor(nu) / sp.factor(de)


def phys(x):
    return scred(sp.sympify(x).subs(SUBS1).subs(SUBS2).subs(SUBS3))


def build():
    monos = []
    kin = kinetic_poly(Vreal)
    pot = potential_poly()
    for cf, sl in poly_to_monomials(kin, None) + poly_to_monomials(pot, None):
        if len(sl) >= 3:
            monos.append((cf, sl))
    monos += ym_monomials()
    K, GS, R = mixing_and_ghost()
    gm, quad = ghost_monomials(K, R)
    monos += gm
    monos = collect(monos)
    out = {}
    for cf, sl in monos:
        cfp = phys(cf)
        if cfp == 0:
            continue
        key = tuple(sorted(s_[0] for s_ in sl))
        out.setdefault(key, []).append((cfp, sl))
    # ghost mass matrix
    gq = {}
    for cf, X, Y in quad:
        gq[(X, Y)] = gq.get((X, Y), 0) + cf
    gq = {k: phys(v_) for k, v_ in gq.items() if phys(v_) != 0}
    ferm = {k: (phys(a), phys(b)) for k, (a, b) in fermion_couplings().items()}
    return out, gq, ferm


MONOS, GHOSTQ, FERM = build()


def vertex(legs):
    """legs: list of (field, mom dict, index or None); returns L expression (i * sum)."""
    key = tuple(sorted(l_[0] for l_ in legs))
    tot = L()
    for cf, slots in MONOS.get(key, []):
        n = len(slots)
        for perm in itertools.permutations(range(n)):
            if any(legs[perm[k]][0] != slots[k][0] for k in range(n)):
                continue
            ren = {}
            def rn(x):
                if x not in ren:
                    ren[x] = fresh('z')
                return ren[x]
            ex = L.scalar(sp.I * cf)
            for k in range(n):
                f, didx, vidx = slots[k]
                _, mom, lidx = legs[perm[k]]
                if didx is not None:
                    ex = ex * (vec(mom, rn(didx)) * (-sp.I))
                if vidx is not None:
                    ex = ex * g(rn(vidx), lidx)
            tot = tot + ex
    return tot.simplify()


CONJ = {'A': 'A', 'Z': 'Z', 'Wp': 'Wm', 'Wm': 'Wp', 'H': 'H', 'chi': 'chi', 'php': 'phm', 'phm': 'php'}
GCONJ = {'uA': 'bA', 'uZ': 'bZ', 'up': 'bm', 'um': 'bp'}      # <u_Y b_X> nonzero
BG = {v_: k for k, v_ in GCONJ.items()}
VMASS = {'A': None, 'Z': MZ ** 2, 'Wp': MW ** 2, 'Wm': MW ** 2}
SMASS = {'H': MH ** 2, 'chi': xi * MZ ** 2, 'php': xi * MW ** 2, 'phm': xi * MW ** 2}
GMASS = {'uA': 0, 'uZ': xi * MZ ** 2, 'up': xi * MW ** 2, 'um': xi * MW ** 2}


def vprop(f, k, a, b, photon='massless'):
    """list of (L numerator, coef, mass2, power) for vector field f with momentum k"""
    M2 = VMASS[f]
    if M2 is None:
        if photon == 'massless':
            return [(g(a, b), -sp.I, 0, 1), (vec(k, a) * vec(k, b), sp.I * (1 - xi), 0, 2)]
        M2 = L2
    return [(g(a, b), -sp.I, M2, 1), (vec(k, a) * vec(k, b), sp.I / M2, M2, 1), (vec(k, a) * vec(k, b), -sp.I / M2, xi * M2, 1)]


def prop(f, k, a, b, photon='massless'):
    if f in VMASS:
        return vprop(f, k, a, b, photon)
    if f in SMASS:
        return [(L.scalar(1), sp.I, SMASS[f], 1)]
    raise KeyError(f)


# ====================================================================================================
# Gauge-boson self-energy integrands (bubbles, ghost loops, seagulls; no tadpoles)
# ====================================================================================================

BOSONS = ['A', 'Z', 'Wp', 'Wm', 'H', 'chi', 'php', 'phm']
qv = {'q': 1}; pv = {'p': 1}
mq = {'q': -1}; mp_ = {'p': -1}
mqp = {'q': -1, 'p': -1}; qpv = {'q': 1, 'p': 1}


def _idx(f):
    return fresh('x') if f in VMASS else None


def add(acc, key, val):
    acc[key] = acc.get(key, 0) + val


def se_integrand(E1, E2, proj, photon='massless'):
    """1PI two-point (legs E1 momentum p index mu, E2 momentum -p index nu), contracted with proj in {'g','pp'}.
    Returns dict (m1,n1,m2,n2) -> numerator (the integrand is numerator/(D1^n1 D2^n2), measure d^dq/(2pi)^d)."""
    mu, nu = fresh('mu'), fresh('nu')
    P = g(mu, nu) if proj == 'g' else vec(pv, mu) * vec(pv, nu)
    acc = {}
    # bubbles
    for a in BOSONS:
        for b in BOSONS:
            ia, ib = _idx(a), _idx(b)
            V1 = vertex([(E1, pv, mu), (a, qv, ia), (b, mqp, ib)])
            if not V1.t:
                continue
            c_, d_ = CONJ[a], CONJ[b]
            ic, id_ = _idx(c_), _idx(d_)
            V2 = vertex([(E2, mp_, nu), (c_, mq, ic), (d_, qpv, id_)])
            if not V2.t:
                continue
            X = (V1 * P) * V2
            for (Na, ca, ma, na) in prop(a, qv, ia, ic, photon):
                XA = X * Na
                for (Nb, cb, mb, nb) in prop(b, qpv, ib, id_, photon):
                    Y = XA * Nb
                    assert set(Y.t) <= {()}, Y.t.keys()
                    add(acc, (ma, na, mb, nb), sp.Rational(1, 2) * ca * cb * Y.t.get((), 0))
    # ghost loops
    for X_ in AGH:
        for Y_ in GH:
            V1 = vertex([(E1, pv, mu), (X_, qv, None), (Y_, mqp, None)])
            if not V1.t:
                continue
            Yb = GCONJ[Y_]                 # antighost at v2 receiving ghost Y
            Xu = BG[X_]                    # ghost at v2 going to antighost X
            V2 = vertex([(E2, mp_, nu), (Yb, qpv, None), (Xu, mq, None)])
            if not V2.t:
                continue
            Z_ = (V1 * P) * V2
            add(acc, (GMASS[Xu], 1, GMASS[Y_], 1), -1 * sp.I * sp.I * Z_.t.get((), 0))
    # seagulls
    for a in BOSONS:
        ia = _idx(a); c_ = CONJ[a]; ic = _idx(c_)
        V4 = vertex([(E1, pv, mu), (E2, mp_, nu), (a, qv, ia), (c_, mq, ic)])
        if not V4.t:
            continue
        X = V4 * P
        for (Na, ca, ma, na) in prop(a, qv, ia, ic, photon):
            Y = X * Na
            add(acc, (ma, na, None, 0), sp.Rational(1, 2) * ca * Y.t.get((), 0))
    return {k: sp.expand(v_) for k, v_ in acc.items() if sp.expand(v_) != 0}


# ====================================================================================================
# Reduction: Passarino-Veltman + integration by parts (bubbles), Taylor expansion in p (p -> 0)
# ====================================================================================================
D1, D2 = sp.symbols('D1 D2')


def sym_fac(n):
    """<(q.p)^n> -> sym_fac * (Q2 P2)^(n/2) for even n"""
    if n % 2:
        return 0
    l = n // 2
    num = sp.Integer(1)
    for k in range(1, 2 * l, 2):
        num *= k
    den = sp.Integer(1)
    for i in range(l):
        den *= (d + 2 * i)
    return num / den


def r_T(n):
    """T_n = r_T(n) * A0 / m^(n-1)"""
    r = sp.Integer(1)
    for j in range(1, n):
        r *= (d - 2 * j) / (2 * j)
    return r


def add(acc, k, v):
    if v != 0:
        acc[k] = acc.get(k, 0) + v


def tadpole(N, m, n, acc, pref=1):
    """int N(Q2,QP)/(Q2-m)^n  (m = mass^2) into acc[('A', m)]"""
    if m == 0:
        return
    Pn = sp.Poly(sp.expand(N), Q2, QP)
    for (r, j), cf in Pn.terms():
        sf = sym_fac(j)
        if sf == 0:
            continue
        R = r + j // 2
        base = cf * sf * P2 ** (j // 2) * pref
        for s_ in range(R + 1):
            k = n - s_
            if k < 1:
                continue
            add(acc, ('A', m), base * sp.binomial(R, s_) * m ** (R - s_) * r_T(k) / m ** (k - 1))


def ibp_21_12(m1, m2):
    """return (B21, B12) as dicts over basis, from IBP"""
    T2 = lambda m: {} if m == 0 else {('A', m): r_T(2) / m}
    b21, b12 = sp.symbols('b21 b12')
    rhs1 = {('B', m1, m2): -(d - 3)}
    rhs2 = {('B', m1, m2): -(d - 3)}
    for k, v in T2(m2).items():
        rhs1[k] = rhs1.get(k, 0) + v
    for k, v in T2(m1).items():
        rhs2[k] = rhs2.get(k, 0) + v
    a11, a12 = -2 * m1, -(m1 + m2 - P2)
    a21, a22 = -(m1 + m2 - P2), -2 * m2
    det = a11 * a22 - a12 * a21
    keys = set(rhs1) | set(rhs2)
    B21 = {k: (rhs1.get(k, 0) * a22 - a12 * rhs2.get(k, 0)) / det for k in keys}
    B12 = {k: (a11 * rhs2.get(k, 0) - a21 * rhs1.get(k, 0)) / det for k in keys}
    return B21, B12


def bubble(N, m1, n1, m2, n2, acc):
    if m2 is None:
        tadpole(N, m1, n1, acc)
        return
    expr = sp.expand(sp.sympify(N).subs({QP: (D2 - D1 - P2 - m1 + m2) / 2}).subs({Q2: D1 + m1}))
    Pn = sp.Poly(expr, D1, D2)
    for (a, b), cf in Pn.terms():
        e1, e2 = n1 - a, n2 - b
        if e1 <= 0 and e2 <= 0:
            continue
        if e1 <= 0:
            # int D1^k / D2^e2 ; shift q -> q - p: D1 = Q2 - 2QP + P2 - m1, D2 = Q2 - m2
            tadpole(cf * (Q2 - 2 * QP + P2 - m1) ** (-e1), m2, e2, acc)
        elif e2 <= 0:
            tadpole(cf * (Q2 + 2 * QP + P2 - m2) ** (-e2), m1, e1, acc)
        elif (e1, e2) == (1, 1):
            add(acc, ('B', m1, m2), cf)
        else:
            assert (e1, e2) in ((2, 1), (1, 2)), (e1, e2)
            B21, B12 = ibp_21_12(m1, m2)
            for k, v in (B21 if (e1, e2) == (2, 1) else B12).items():
                add(acc, k, cf * v)


def reduce_se(integrand):
    acc = {}
    for (m1, n1, m2, n2), N in integrand.items():
        bubble(N, m1, n1, m2, n2, acc)
    return acc


# ------------------------------------------------------------------ Taylor (p -> 0) route
def taylor_vac(integrand, order):
    """expand integrand in p to total order `order` (QP ~ p, P2 ~ p^2), symmetric-integrate.
    returns dict (j, r, ((m,a),(m,b))) -> coef  meaning P2^j * <Q2^r / prod (Q2-m)^a>"""
    t = sp.Symbol('t')
    acc = {}
    for (m1, n1, m2, n2), N in integrand.items():
        Nt = sp.expand(sp.sympify(N).subs({QP: t * QP, P2: t ** 2 * P2}))
        dens = [(m1, n1)]
        if m2 is not None:
            # 1/(Q2 - m2 + t(2QP + t P2))^n2
            u = t * (2 * QP + t * P2)
            ser = 0
            for k in range(order + 1):
                ser += sp.binomial(-n2, k) * u ** k * sp.Symbol('Dm_%d' % (n2 + k))
            Nt = sp.expand(Nt * ser)
        Pn = sp.Poly(Nt, t)
        for (k,), cf in Pn.terms():
            if k > order:
                continue
            cf = sp.expand(cf)
            # split by Dm powers
            terms = sp.Add.make_args(cf)
            for term in terms:
                pw2 = 0
                c0 = term
                for s_ in term.free_symbols:
                    if s_.name.startswith('Dm_'):
                        pw2 = int(s_.name[3:]); c0 = c0.subs(s_, 1)
                if m2 is not None and pw2 == 0:
                    raise RuntimeError
                Pq = sp.Poly(c0, Q2, QP, P2)
                for (r, j, l), c1 in Pq.terms():
                    sf = sym_fac(j)
                    if sf == 0:
                        continue
                    key = (l + j // 2, r + j // 2, tuple(sorted(((m1, n1),) + (((m2, pw2),) if m2 is not None else ()), key=str)))
                    acc[key] = acc.get(key, 0) + c1 * sf
    return acc


# ====================================================================================================
# Numerical scalar integrals (MS-bar), partial fractions of vacuum integrals
# ====================================================================================================

eps = sp.Symbol('eps')
_RT = {}


def rT_eps(n):
    if n not in _RT:
        r = sp.Integer(1)
        for j in range(1, n):
            r *= (d - 2 * j) / (2 * j)
        r = r.subs(d, 4 - 2 * eps)
        _RT[n] = (sp.Rational(r.subs(eps, 0)), sp.Rational(sp.diff(r, eps).subs(eps, 0)))
    return _RT[n]


def T_num(n, a, mu2):
    """(pole, finite) of T_n(a) = <1/(q^2-a)^n>, a = mass^2 > 0"""
    r0, r1 = rT_eps(n)
    A0p = a
    A0f = a * (1 - mp.log(a / mu2))
    s = a ** (n - 1)
    return (r0 * A0p / s, (r0 * A0f + r1 * A0p) / s)


def _f(r):
    # (1-r) ln(1-r) + r ln(-r) - 1, real part
    t1 = 0 if r == 1 else (1 - r) * mp.log(1 - r)
    t2 = 0 if r == 0 else r * mp.log(-r)
    return mp.re(t1 + t2) - 1


def B0_num(p2, m1, m2, mu2):
    """(pole, Re finite) of B0(p2; m1, m2) (masses squared)"""
    p2, m1, m2 = mp.mpf(p2), mp.mpf(m1), mp.mpf(m2)
    if p2 == 0:
        if m1 == m2:
            if m1 == 0:
                return (0, 0)                  # B0(0;0,0) is scaleless: zero in dimensional regularization
            I = mp.log(m1 / mu2)
        elif m1 == 0:
            I = mp.log(m2 / mu2) - 1
        elif m2 == 0:
            I = mp.log(m1 / mu2) - 1
        else:
            I = (m1 * mp.log(m1 / mu2) - m2 * mp.log(m2 / mu2)) / (m1 - m2) - 1
        return (1, -I)
    a, b, c = p2, m1 - m2 - p2, m2
    disc = b * b - 4 * a * c
    sq = mp.sqrt(mp.mpc(disc)) if disc < 0 else mp.sqrt(disc)
    if disc >= 0:
        qq = -(b + (sq if b >= 0 else -sq)) / 2
        x1 = qq / a
        x2 = c / qq if qq != 0 else mp.mpf(0)
    else:
        x1 = (-b + sq) / (2 * a); x2 = (-b - sq) / (2 * a)
    I = mp.log(abs(a) / mu2) + _f(x1) + _f(x2)
    return (1, -I)


def B0_quad(p2, m1, m2, mu2):
    """independent: Feynman-parameter quadrature of Re B0 finite part"""
    f = lambda x: mp.log(abs(x * m1 + (1 - x) * m2 - x * (1 - x) * p2) / mu2)
    pts = [0, 1]
    a, b, c = p2, m1 - m2 - p2, m2
    if p2 != 0:
        disc = b * b - 4 * a * c
        if disc > 0:
            for x in ((-b + mp.sqrt(disc)) / (2 * a), (-b - mp.sqrt(disc)) / (2 * a)):
                if 0 < x < 1:
                    pts.append(x)
    pts = sorted(pts)
    return -mp.quad(f, pts)


def partial_fractions(r, dens):
    """x^r / prod (x - a)^n  -> list of (a, j, coef) for nonzero a; dens list of (a, n) numeric"""
    grp = []
    for a, n in dens:
        a = mp.mpf(a)
        for gi in grp:
            if gi[0] == a or (a != 0 and abs(gi[0] - a) <= mp.mpf(10) ** (-mp.mp.dps + 8) * abs(a)):
                gi[1] += n; break
        else:
            grp.append([a, n])
    out = []
    for i, (a, n) in enumerate(grp):
        if a == 0:
            continue
        # series in t around x = a, up to t^(n-1)
        N = n
        ser = [mp.mpf(0)] * N
        # x^r
        for k in range(min(r, N - 1) + 1):
            ser[k] = mp.binomial(r, k) * a ** (r - k)
        for j, (b, nb) in enumerate(grp):
            if j == i:
                continue
            dlt = a - b
            fac = [mp.binomial(-nb, k) * dlt ** (-nb - k) for k in range(N)]
            new = [mp.mpf(0)] * N
            for k1 in range(N):
                if ser[k1] == 0:
                    continue
                for k2 in range(N - k1):
                    new[k1 + k2] += ser[k1] * fac[k2]
            ser = new
        for jj in range(1, n + 1):
            out.append((a, jj, ser[n - jj]))
    return out


def vac_num(r, dens, mu2):
    """(pole, finite) of <x^r / prod (x-a)^n>"""
    P = mp.mpf(0); F = mp.mpf(0)
    for a, j, cf in partial_fractions(r, dens):
        p_, f_ = T_num(j, a, mu2)
        P += cf * p_; F += cf * f_
    return P, F


# ====================================================================================================
# Fermion lines: d-dim traces (single line), 4d Fierz projection (boxes)
# ====================================================================================================


class F:
    """sum of terms: key (gam tuple, lor tuple, dens tuple) -> coef.
    gam entries: ('i', name) | ('s', 'q') | ('s', 'p'); for two lines gam = (line1, line2)."""
    def __init__(self, t=None):
        self.t = t or {}

    def __add__(self, o):
        r = dict(self.t)
        for k, v in o.t.items():
            r[k] = r.get(k, 0) + v
        return F(r)


def mk(coef, gam=(), lor=None, dens=()):
    """lor: an L expression (sum) -> expand into terms"""
    out = {}
    if lor is None:
        lor = L.scalar(1)
    for lk, lc in lor.t.items():
        key = (tuple(gam), lk, tuple(dens))
        out[key] = out.get(key, 0) + coef * lc
    return F(out)


def fmul(a, b, two_lines=False):
    """product; gam concatenated (single line: a.gam + b.gam)"""
    r = {}
    for (ga, la, da), ca in a.t.items():
        for (gb, lb, db), cb in b.t.items():
            c, lk = _contract(la + lb)
            if ga and gb:
                assert len(ga) == len(gb)
                gk = tuple(x + y for x, y in zip(ga, gb))
            else:
                gk = ga or gb
            key = (gk, lk, da + db)
            r[key] = r.get(key, 0) + c * ca * cb
    return F(r)


def _absorb(gam, lor):
    """contract Lorentz factors into gamma entries. gam: tuple of lines (tuple of tuples)."""
    gam = [list(l_) for l_ in gam]
    lor = list(lor)
    changed = True
    while changed:
        changed = False
        for n, f in enumerate(lor):
            if f[0] == 'g':
                for line in gam:
                    for k, ge in enumerate(line):
                        if ge[0] == 'i' and ge[1] in (f[1], f[2]):
                            other = f[2] if ge[1] == f[1] else f[1]
                            line[k] = ('i', other)
                            lor.pop(n); changed = True
                            break
                    if changed: break
            elif f[0] == 'v':
                for line in gam:
                    for k, ge in enumerate(line):
                        if ge[0] == 'i' and ge[1] == f[2]:
                            line[k] = ('s', f[1])
                            lor.pop(n); changed = True
                            break
                    if changed: break
            if changed:
                break
    return tuple(tuple(l_) for l_ in gam), tuple(lor)


def pairings(lst):
    if not lst:
        yield []
        return
    a = lst[0]
    for k in range(1, len(lst)):
        rest = lst[1:k] + lst[k + 1:]
        for p in pairings(rest):
            yield [(a, lst[k])] + p


def sym_integrate(Fx, dim):
    """symmetric integration over q (zero external momenta, possibly p for WF): replaces q-slashes, v(q,i), QP.
    Q2 stays as scalar.  dim: d (symbol) or 4."""
    out = {}
    for (gam, lor, dens), c in Fx.t.items():
        c = sp.expand(c)
        for term in sp.Add.make_args(c):
            pw_qp = sp.degree(term, QP) if term.has(QP) else 0
            cterm = term / QP ** pw_qp
            lines = [list(l_) for l_ in gam]
            lorl = list(lor)
            qidx = []
            for line in lines:
                for k, ge in enumerate(line):
                    if ge == ('s', 'q'):
                        nm = fresh('s'); line[k] = ('i', nm); qidx.append(nm)
            newlor = []
            for f in lorl:
                if f[0] == 'v' and f[1] == 'q':
                    qidx.append(f[2])
                else:
                    newlor.append(f)
            for _ in range(pw_qp):
                nm = fresh('t'); qidx.append(nm); newlor.append(('v', 'p', nm))
            n = len(qidx)
            if n % 2:
                continue
            l_ = n // 2
            den = sp.Integer(1)
            for i in range(l_):
                den *= (dim + 2 * i)
            pref = cterm * Q2 ** l_ / den
            for P in pairings(qidx):
                lf = newlor + [('g',) + tuple(sorted(pp)) for pp in P]
                cc, lk = _contract(tuple(lf))
                if dim == 4:
                    cc = cc.subs(d, 4)
                g2, lk2 = _absorb(tuple(tuple(x) for x in lines), lk)
                key = (g2, lk2, dens)
                out[key] = out.get(key, 0) + pref * cc
    return F({k: v for k, v in out.items() if v != 0})


@functools.lru_cache(maxsize=None)
def trace_d(names):
    """Tr of gamma string with index names, every name exactly twice: polynomial in d"""
    n = len(names)
    tot = sp.Integer(0)
    pos = list(range(n))
    # name partner
    where = {}
    for i, nm in enumerate(names):
        where.setdefault(nm, []).append(i)
    partner = {}
    for nm, ps in where.items():
        assert len(ps) == 2, names
        partner[ps[0]] = ps[1]; partner[ps[1]] = ps[0]

    def rec(lst):
        if not lst:
            yield 1, []
            return
        a = lst[0]
        for k in range(1, len(lst)):
            sgn = (-1) ** (k - 1)
            rest = lst[1:k] + lst[k + 1:]
            for s2, p in rec(rest):
                yield sgn * s2, [(a, lst[k])] + p
    for sgn, P in rec(pos):
        m = {}
        for a, b in P:
            m[a] = b; m[b] = a
        seen = set(); cyc = 0
        for st in range(n):
            if st in seen:
                continue
            cyc += 1
            x = st
            while True:
                seen.add(x)
                y = m[x]; seen.add(y)
                x = partner[y]
                if x == st:
                    break
        tot += sgn * d ** cyc
    return 4 * tot


def canon(names):
    ren = {}
    out = []
    for nm in names:
        if nm not in ren:
            ren[nm] = 'n%d' % len(ren)
        out.append(ren[nm])
    return tuple(out)


def project_line(Fx, ext):
    """single line: coefficient of gamma^{ext} (ext = index name) or of pslash (ext='p'),
    returned per denominator key: dict dens -> coef (scalar in Q2, d, params)"""
    out = {}
    for (gam, lor, dens), c in Fx.t.items():
        line = list(gam[0])
        assert not lor, lor
        if ext == 'p':
            k = [i for i, ge in enumerate(line) if ge == ('s', 'p')]
            assert len(k) == 1
            line[k[0]] = ('i', '_rho'); tag = '_rho'
        else:
            tag = ext
        names = (tag,) + tuple(ge[1] for ge in line)
        assert all(ge[0] == 'i' for ge in line), line
        tr = trace_d(canon(names))
        val = c * tr / (4 * d)
        out[dens] = out.get(dens, 0) + val
    return {k: sp.expand(v) for k, v in out.items() if sp.expand(v) != 0}


# ---------------------------------------------- 4d two-line Fierz projection
_G = None


def _gammas():
    global _G
    if _G is None:
        I2 = np.eye(2); Z2 = np.zeros((2, 2))
        sx = np.array([[0, 1], [1, 0]], complex); sy = np.array([[0, -1j], [1j, 0]]); sz = np.array([[1, 0], [0, -1]], complex)
        g0 = np.block([[I2, Z2], [Z2, -I2]]).astype(complex)
        gs = [np.block([[Z2, s_], [-s_, Z2]]) for s_ in (sx, sy, sz)]
        G = [g0] + gs
        g5 = 1j * G[0] @ G[1] @ G[2] @ G[3]
        PL = (np.eye(4) - g5) / 2
        _G = (G, PL)
    return _G


ETA = [1, -1, -1, -1]


@functools.lru_cache(maxsize=None)
def fierz4(l1, l2):
    """l1, l2: tuples of index names (each name twice overall). Returns c with
    sum (l1 P_L) x (l2 P_L) = c * (gamma^a P_L) x (gamma_a P_L)  in 4d."""
    G, PL = _gammas()
    names = sorted(set(l1 + l2))
    X = np.zeros((16, 16), complex)
    for vals in itertools.product(range(4), repeat=len(names)):
        asg = dict(zip(names, vals))
        sg = 1
        for v_ in vals:
            sg *= ETA[v_]
        M1 = np.eye(4, dtype=complex)
        for nm in l1:
            M1 = M1 @ G[asg[nm]]
        M2 = np.eye(4, dtype=complex)
        for nm in l2:
            M2 = M2 @ G[asg[nm]]
        X += sg * np.kron(M1 @ PL, M2 @ PL)
    T = sum(ETA[a] * np.kron(G[a] @ PL, G[a] @ PL) for a in range(4))
    c = np.vdot(T, X) / np.vdot(T, T)
    res = np.abs(X - c * T).max()
    assert res < 1e-9, (l1, l2, res)
    cr = complex(c)
    assert abs(cr.imag) < 1e-12
    return sp.nsimplify(round(cr.real, 9))


def project_box(Fx):
    out = {}
    for (gam, lor, dens), c in Fx.t.items():
        assert not lor, lor
        l1, l2 = gam
        assert all(ge[0] == 'i' for ge in l1 + l2)
        names = canon(tuple(ge[1] for ge in l1) + tuple(ge[1] for ge in l2))
        n1 = len(l1)
        f = fierz4(names[:n1], names[n1:])
        out[dens] = out.get(dens, 0) + c * f
    return {k: sp.expand(v) for k, v in out.items() if sp.expand(v) != 0}


def absorb_reduce(Fx):
    """absorb Lorentz factors into the gamma lines, then use qslash qslash = q^2 for adjacent pairs"""
    out = {}
    for (gam, lor, dens), c in Fx.t.items():
        g2, l2 = _absorb(gam, lor)
        lines = []
        for line in g2:
            line = list(line)
            k = 0
            while k < len(line) - 1:
                if line[k] == ('s', 'q') and line[k + 1] == ('s', 'q'):
                    del line[k:k + 2]; c = c * Q2
                    k = max(k - 1, 0)
                else:
                    k += 1
            lines.append(tuple(line))
        key = (tuple(lines), l2, dens)
        out[key] = out.get(key, 0) + c
    return F(out)


def project_box_mixed(Fx):
    """d-dim where the two-line structure is gamma^a x gamma_a (exact in any d), 4d Fierz otherwise"""
    out = {}
    for (gam, lor, dens), c in Fx.t.items():
        assert not lor, lor
        l1, l2 = gam
        if len(l1) == 1 and len(l2) == 1:
            assert l1[0][1] == l2[0][1]
            f = 1
            cc = c
        else:
            names = canon(tuple(ge[1] for ge in l1) + tuple(ge[1] for ge in l2))
            f = fierz4(names[:len(l1)], names[len(l1):])
            cc = sp.sympify(c).subs(d, 4)
        out[dens] = out.get(dens, 0) + cc * f
    return {k: sp.expand(v) for k, v in out.items() if sp.expand(v) != 0}


# ====================================================================================================
# Lepton diagrams at zero external momenta: W l nu vertex, lepton self-energies, boxes, Ward-identity vertices
# ====================================================================================================

q = {'q': 1}; mq = {'q': -1}; zero = {}


def fv(fb, f, V, idx):
    cL = FERM[(fb, f, V)][0]
    return mk(sp.I * cL, ((('i', idx),),))


def S(sign):
    return mk(sp.I * sign, ((('s', 'q'),),), dens=((0, 1),))


def S_p():
    """first-order-in-p part of S(p+q) = i(p+q)/(p+q)^2"""
    return mk(sp.I, ((('s', 'p'),),), dens=((0, 1),)) + mk(-2 * sp.I * QP, ((('s', 'q'),),), dens=((0, 2),))


PHOTON = 'lambda'


def B(f, k, a, b):
    out = F()
    for (N, c, m, n) in prop(f, k, a, b, photon=PHOTON):
        out = out + mk(c, (), N, dens=((m, n),))
    return out


def V3(legs):
    return mk(1, (), vertex(legs))


def chain(*fs):
    r = fs[0]
    for x in fs[1:]:
        r = fmul(r, x)
    return r


def vertex_W():
    """1PI (nubar l Wp) vertex: returns dict dens -> coefficient of gamma^mu (times i/16pi^2 <...>)"""
    mu = 'MU'
    tot = F()
    a, b = fresh('a'), fresh('b')
    tot = tot + chain(fv('nu', 'nu', 'Z', b), S(-1), fv('nu', 'l', 'Wp', mu), S(-1), fv('l', 'l', 'Z', a), B('Z', q, a, b))
    for V in ('A', 'Z'):
        a, a2, b, b2 = fresh('a'), fresh('a'), fresh('b'), fresh('b')
        tot = tot + chain(fv('nu', 'l', 'Wp', b), S(-1), fv('l', 'l', V, a), B(V, q, a, a2), B('Wp', mq, b, b2),
                          V3([(V, q, a2), ('Wm', mq, b2), ('Wp', zero, mu)]))
    a, a2, b, b2 = fresh('a'), fresh('a'), fresh('b'), fresh('b')
    tot = tot + chain(fv('nu', 'nu', 'Z', a), S(+1), fv('nu', 'l', 'Wp', b), B('Z', q, a, a2), B('Wp', mq, b, b2),
                      V3([('Z', q, a2), ('Wm', mq, b2), ('Wp', zero, mu)]))
    return project_line(sym_integrate(tot, d), mu)


def wf(f, only=None):
    """lepton self-energy, coefficient of pslash P_L (times i/16pi^2 <...>)"""
    tot = F()
    if f == 'l':
        loops = [('l', 'A', 'A'), ('l', 'Z', 'Z'), ('nu', 'Wp', 'Wm')]
    else:
        loops = [('nu', 'Z', 'Z'), ('l', 'Wm', 'Wp')]
    for fi, B1, B2 in loops:
        if only is not None and B1 not in only:
            continue
        a, b = fresh('a'), fresh('b')
        # f(p) -> fi + boson (vertex fi_bar f B1-leg) ; fi -> f (vertex f_bar fi B2-leg)
        tot = tot + chain(fv(f, fi, B2, b), S_p(), fv(fi, f, B1, a), B(B1, q, a, b))
    return project_line(sym_integrate(tot, d), 'p')


BOXMODE = 'mixed'


def Bparts(f, k, a, b, photon):
    return [mk(c, (), N, dens=((m, n),)) for (N, c, m, n) in prop(f, k, a, b, photon=photon)]


def boxes():
    if BOXMODE == 'mixed':
        return boxes_mixed()
    return boxes_4d()


def boxes_mixed():
    """photon x (W xi-pole part) terms with a massless photon (dim reg; IR finite for xi>0);
    gamma^a x gamma_a structures in d dims, the rest (W g x V g, UV finite) in 4d"""
    tot = F()
    for V in ('A', 'Z'):
        a1, a2, b1, b2 = fresh('a'), fresh('a'), fresh('b'), fresh('b')
        L1 = {'a': chain(fv('nu', 'l', 'Wp', b1), S(-1), fv('l', 'l', V, a1)),
              'b': chain(fv('nu', 'nu', V, a1), S(+1), fv('nu', 'l', 'Wp', b1)) if V == 'Z' else None}
        L2_ = {'a': chain(fv('l', 'l', V, a2), S(-1), fv('l', 'nu', 'Wm', b2)),
               'b': chain(fv('l', 'nu', 'Wm', b2), S(+1), fv('nu', 'nu', V, a2)) if V == 'Z' else None}
        Wp_parts = Bparts('Wp', q, b1, b2, 'lambda')
        for k1, x1 in L1.items():
            for k2, x2 in L2_.items():
                if x1 is None or x2 is None:
                    continue
                y1 = F({((k[0][0], ()), k[1], k[2]): c for k, c in x1.t.items()})
                y2 = F({(((), k[0][0]), k[1], k[2]): c for k, c in x2.t.items()})
                for iw, wpart in enumerate(Wp_parts):
                    ph = 'massless' if (V == 'A' and iw == 2) else 'lambda'
                    for vpart in Bparts(V, q, a1, a2, ph):
                        tot = tot + chain(y1, y2, vpart, wpart)
    return project_box_mixed(sym_integrate(absorb_reduce(tot), d))


def boxes_4d():
    tot = F()
    for V in ('A', 'Z'):
        a1, a2, b1, b2 = fresh('a'), fresh('a'), fresh('b'), fresh('b')
        L1 = {'a': chain(fv('nu', 'l', 'Wp', b1), S(-1), fv('l', 'l', V, a1)),
              'b': chain(fv('nu', 'nu', V, a1), S(+1), fv('nu', 'l', 'Wp', b1)) if V == 'Z' else None}
        L2_ = {'a': chain(fv('l', 'l', V, a2), S(-1), fv('l', 'nu', 'Wm', b2)),
               'b': chain(fv('l', 'nu', 'Wm', b2), S(+1), fv('nu', 'nu', V, a2)) if V == 'Z' else None}
        for k1, x1 in L1.items():
            for k2, x2 in L2_.items():
                if x1 is None or x2 is None:
                    continue
                # two lines: wrap
                y1 = F({((k[0][0], ()), k[1], k[2]): c for k, c in x1.t.items()})
                y2 = F({(((), k[0][0]), k[1], k[2]): c for k, c in x2.t.items()})
                tot = tot + chain(y1, y2, B(V, q, a1, a2), B('Wp', q, b1, b2))
    return project_box(sym_integrate(tot, 4))


def ward_vertices():
    """1PI photon vertices at zero momentum (W loops) for e_L and nu: coefficient of gamma^mu"""
    mu = 'MU'
    # e_L
    a, a2, b, b2 = fresh('a'), fresh('a'), fresh('b'), fresh('b')
    eL = chain(fv('l', 'nu', 'Wm', b), S(+1), fv('nu', 'l', 'Wp', a), B('Wp', q, a, a2), B('Wm', q, b, b2),
               V3([('A', zero, mu), ('Wm', mq, a2), ('Wp', q, b2)]))
    # nu (a): photon on W
    a, a2, b, b2 = fresh('a'), fresh('a'), fresh('b'), fresh('b')
    nu = chain(fv('nu', 'l', 'Wp', b), S(+1), fv('l', 'nu', 'Wm', a), B('Wm', q, a, a2), B('Wp', q, b, b2),
               V3([('A', zero, mu), ('Wp', mq, a2), ('Wm', q, b2)]))
    # nu (b): photon on internal lepton
    a, b = fresh('a'), fresh('b')
    nu = nu + chain(fv('nu', 'l', 'Wp', b), S(-1), fv('l', 'l', 'A', mu), S(-1), fv('l', 'nu', 'Wm', a), B('Wm', q, a, b))
    return project_line(sym_integrate(eL, d), mu), project_line(sym_integrate(nu, d), mu)


# ====================================================================================================
# Assembly (SPEC 2): classes SE and VBW, the total
# ====================================================================================================
DPS = 60                       # working precision (local to the exports, via mp.workdps)
LAMBDA2_REL = mp.mpf(10) ** -30   # photon mass^2 / M_W^2 used as IR regulator in the lepton diagrams (lambda -> 0)
PARAMS = (e, cw, sw, MW, MH, xi, L2)


def _compile(expr):
    """c(d) -> (c(4), c1) with c(4 - 2 eps) = c(4) + c1 eps + ..., as mpmath functions of PARAMS"""
    expr = sp.sympify(expr)
    c0 = sp.expand(expr.subs(d, 4))
    c1 = sp.expand((-2 * sp.diff(expr, d)).subs(d, 4))
    return (sp.lambdify(PARAMS, c0, modules='mpmath'), sp.lambdify(PARAMS, c1, modules='mpmath'))


def _cmass(m):
    return sp.lambdify(PARAMS, sp.sympify(m), modules='mpmath')


def _taylor_A(E1, E2, j):
    """coefficient of P2^j in A(P2) = (G - P/P2)/(d-1), Taylor route: dict (r, dens) -> c(d)"""
    ig = se_integrand(E1, E2, 'g'); ip = se_integrand(E1, E2, 'pp')
    tg = taylor_vac(ig, 2 * j); tp = taylor_vac(ip, 2 * j + 2)
    out = {}
    for (jj, r, dens), c in tg.items():
        if jj == j:
            out[(r, dens)] = out.get((r, dens), 0) + c
    for (jj, r, dens), c in tp.items():
        if jj == j + 1:
            out[(r, dens)] = out.get((r, dens), 0) - c
    return {k: sp.expand(v_ / (d - 1)) for k, v_ in out.items() if sp.expand(v_) != 0}


def _onshell(E1, E2, M2):
    """Passarino-Veltman route at p^2 = M2: dict basis -> coefficient"""
    ig = se_integrand(E1, E2, 'g'); ip = se_integrand(E1, E2, 'pp')
    G = reduce_se(ig); Pp = reduce_se(ip)
    out = {}
    for k in set(G) | set(Pp):
        c = sp.cancel(sp.together((G.get(k, 0) - Pp.get(k, 0) / P2) / (d - 1)))
        c = sp.expand(c.subs(P2, M2))
        if c != 0:
            out[k] = c
    return out


def _lepton(acc):
    """dens -> polynomial in Q2  ->  dict (r, dens) -> c(d)"""
    out = {}
    for dens, c in acc.items():
        for (r,), cr in sp.Poly(c, Q2).terms():
            out[(r, dens)] = out.get((r, dens), 0) + cr
    return out


def _cvac(dct):
    return [(r, tuple((_cmass(m), n) for m, n in dens), _compile(c)) for (r, dens), c in dct.items()]


def _cbasis(dct):
    out = []
    for k, c in dct.items():
        if k[0] == 'A':
            out.append(('A', (_cmass(k[1]),), _compile(c)))
        else:
            out.append(('B', (_cmass(k[1]), _cmass(k[2])), _compile(c)))
    return out


@functools.lru_cache(maxsize=None)
def _derived():
    """the symbolic derivation (done once), compiled to numerical functions"""
    D = {}
    D['AA1'] = _cvac(_taylor_A('A', 'A', 1))      # Sigma'_AA(0)
    D['AA0'] = _cvac(_taylor_A('A', 'A', 0))      # Sigma_AA(0) (must vanish)
    D['AZ0'] = _cvac(_taylor_A('A', 'Z', 0))      # Sigma_AZ(0)
    D['WW0'] = _cvac(_taylor_A('Wp', 'Wm', 0))    # Sigma_W(0)
    D['WWM'] = _cbasis(_onshell('Wp', 'Wm', MW ** 2))        # Sigma_W(M_W^2)
    D['ZZM'] = _cbasis(_onshell('Z', 'Z', MW ** 2 / cw ** 2))  # Sigma_Z(M_Z^2)
    D['VW'] = _cvac(_lepton(vertex_W()))
    D['WL'] = _cvac(_lepton(wf('l')))
    D['WN'] = _cvac(_lepton(wf('nu')))
    D['BX'] = _cvac(_lepton(boxes()))
    D['ctree'] = sp.lambdify(PARAMS, FERM[('nu', 'l', 'Wp')][0], modules='mpmath')
    return D


def _ev_vac(terms, pv, mu2):
    P = mp.mpf(0); Fv = mp.mpf(0)
    for r, dens, (f0, f1) in terms:
        c0, c1 = mp.re(f0(*pv)), mp.re(f1(*pv))
        if c0 == 0 and c1 == 0:
            continue
        vp, vf = vac_num(r, [(mp.re(fm(*pv)), n) for fm, n in dens], mu2)
        P += c0 * vp; Fv += c0 * vf + c1 * vp
    return P, Fv


def _ev_basis(terms, p2, pv, mu2):
    P = mp.mpf(0); Fv = mp.mpf(0)
    for kind, ms, (f0, f1) in terms:
        if kind == 'A':
            m = mp.re(ms[0](*pv))
            if m == 0:
                continue                       # A0(0) = 0 (scaleless)
            bp, bf = T_num(1, m, mu2)
        else:
            bp, bf = B0_num(p2, mp.re(ms[0](*pv)), mp.re(ms[1](*pv)), mu2)
        c0, c1 = mp.re(f0(*pv)), mp.re(f1(*pv))
        P += c0 * bp; Fv += c0 * bf + c1 * bp
    return P, Fv


def _params(MWv, MZv, MHv, alpha, xiv):
    MWv, MZv, MHv = mp.mpf(MWv), mp.mpf(MZv), mp.mpf(MHv)
    c_ = MWv / MZv
    return (mp.sqrt(4 * mp.pi * mp.mpf(alpha)), c_, mp.sqrt(1 - c_ ** 2), MWv, MHv, mp.mpf(xiv), LAMBDA2_REL * MWv ** 2)


def pieces(MWv, MZv, MHv, alpha, xiv, mu, which=('SE', 'VBW')):
    """(pole, finite) pairs of the building blocks and of the two classes (MS-bar at mu)"""
    D = _derived()
    pv = _params(MWv, MZv, MHv, alpha, xiv)
    MWv, MZv = pv[3], mp.mpf(MZv)
    s_, c_ = pv[2], pv[1]
    mu2 = mp.mpf(mu) ** 2
    k16 = 16 * mp.pi ** 2
    out = {}
    lin = lambda *ts: tuple(sum(cf * t[i] for cf, t in ts) for i in (0, 1))
    if 'SE' in which:
        S = lambda x: (-x[0] / k16, -x[1] / k16)                  # Sigma_T = -A / 16 pi^2
        div = lambda x: x                                          # (d-1) already divided symbolically
        out['SigAAp0'] = S(_ev_vac(D['AA1'], pv, mu2))
        out['SigAZ0'] = S(_ev_vac(D['AZ0'], pv, mu2))
        out['SigW0'] = S(_ev_vac(D['WW0'], pv, mu2))
        out['SigWM'] = S(_ev_basis(D['WWM'], MWv ** 2, pv, mu2))
        out['SigZM'] = S(_ev_basis(D['ZZM'], MZv ** 2, pv, mu2))
        dZe = lin((mp.mpf(1) / 2, out['SigAAp0']), (s_ / c_ / MZv ** 2, out['SigAZ0']))
        out['dZe'] = dZe
        out['SE'] = lin((2, dZe), (-c_ ** 2 / s_ ** 2 / MZv ** 2, out['SigZM']), (c_ ** 2 / s_ ** 2 / MWv ** 2, out['SigWM']),
                        (1 / MWv ** 2, out['SigW0']), (-1 / MWv ** 2, out['SigWM']))
    if 'VBW' in which:
        ct = mp.re(D['ctree'](*pv))
        out['dv'] = tuple(x / (k16 * ct) for x in _ev_vac(D['VW'], pv, mu2))
        out['XL'] = tuple(x / k16 for x in _ev_vac(D['WL'], pv, mu2))
        out['XN'] = tuple(x / k16 for x in _ev_vac(D['WN'], pv, mu2))
        out['box'] = tuple(-MWv ** 2 * x / (k16 * ct ** 2) for x in _ev_vac(D['BX'], pv, mu2))
        out['VBW'] = lin((2, out['dv']), (1, out['box']), (-1, out['XL']), (-1, out['XN']))
    return out


def _dps(MWv, MHv):
    """precision: the M_H^2 (and M_H^4) pieces cancel between the W and Z self-energies"""
    r = max(abs(float(MHv) / float(MWv)), 1.0)
    return DPS + int(4 * math.log10(r)) + 2


def delta_r_se(MW, MZ, MH, alpha, xi, mu):
    with mp.workdps(_dps(MW, MH)):
        return float(pieces(MW, MZ, MH, alpha, xi, mu, which=('SE',))['SE'][1])


def delta_r_vbw(MW, MZ, alpha, xi, mu):
    with mp.workdps(DPS):
        return float(pieces(MW, MZ, MW, alpha, xi, mu, which=('VBW',))['VBW'][1])


def delta_r_bos_xi(MW, MZ, MH, alpha, xi):
    with mp.workdps(_dps(MW, MH)):
        p = pieces(MW, MZ, MH, alpha, xi, MW)
        return float(p['SE'][1] + p['VBW'][1])


PROVENANCE = {
    'delta_r_se': ('derived', 'class SE: 2 dZe - (c2/s2)(SigZ(MZ2)/MZ2 - SigW(MW2)/MW2) + (SigW(0)-SigW(MW2))/MW2, '
                              'self-energies generated from the R_xi Lagrangian, PV/IBP and Taylor reductions, MS-bar'),
    'delta_r_vbw': ('derived', 'class VBW: 2 x 1PI W l nu vertex + boxes - lepton wave functions (Fermi subtraction = 0 by '
                               'the Ward identity), zero external momenta, photon mass lambda -> 0, MS-bar'),
    'delta_r_bos_xi': ('derived', 'SE + VBW (mu independent, xi independent); inputs MW, MZ, MH, alpha from the caller'),
}


# ====================================================================================================
# Second route and checks (run: python3 dr_xi.py)
# ====================================================================================================
def _ward_checks(MWv, MZv, alpha, xiv, mu):
    """(1) Sigma_AA(0) = 0; (2) neutrino charge = 0:  X_nu + (e/2sc) Sigma_AZ(0)/MZ^2 = 0;
    (3) charge universality L vs R:  X_eW - eQ X_Sigma^W(l) - (e/2sc) Sigma_AZ(0)/MZ^2 = 0  (W loops)."""
    D = _derived()
    if 'WEL' not in D:
        eL, nu = ward_vertices()
        D['WEL'] = _cvac(_lepton(eL)); D['WNU'] = _cvac(_lepton(nu))
        D['WLW'] = _cvac(_lepton(wf('l', only=('Wp', 'Wm'))))
        D['eQ'] = sp.lambdify(PARAMS, FERM[('l', 'l', 'A')][0], modules='mpmath')
        D['ev'] = sp.lambdify(PARAMS, e, modules='mpmath')
    pv = _params(MWv, MZv, MWv, alpha, xiv)
    mu2 = mp.mpf(mu) ** 2; k16 = 16 * mp.pi ** 2
    s_, c_ = pv[2], pv[1]; MZv = mp.mpf(MZv)
    AA0 = _ev_vac(D['AA0'], pv, mu2)
    SAZ = tuple(-x / k16 for x in _ev_vac(D['AZ0'], pv, mu2))
    Xe = tuple(x / k16 for x in _ev_vac(D['WEL'], pv, mu2))
    Xn = tuple(x / k16 for x in _ev_vac(D['WNU'], pv, mu2))
    XLW = tuple(x / k16 for x in _ev_vac(D['WLW'], pv, mu2))
    eQ, ev = mp.re(D['eQ'](*pv)), mp.re(D['ev'](*pv))
    nu = [Xn[i] + ev / (2 * s_ * c_) * SAZ[i] / MZv ** 2 for i in (0, 1)]
    el = [Xe[i] - eQ * XLW[i] - ev / (2 * s_ * c_) * SAZ[i] / MZv ** 2 for i in (0, 1)]
    return max(abs(x) for x in AA0), max(abs(x) for x in nu), max(abs(x) for x in el)


def _taylor_vs_pv(E1, E2, p2, MWv, MZv, MHv, alpha, xiv, mu):
    """A(p^2) of the 1PI function from the PV/IBP route at small p^2 versus A(0) + p^2 A'(0) from the Taylor route"""
    ig = se_integrand(E1, E2, 'g'); ip = se_integrand(E1, E2, 'pp')
    G = reduce_se(ig); Pp = reduce_se(ip)
    pvr = {k: sp.cancel(sp.together((G.get(k, 0) - Pp.get(k, 0) / P2) / (d - 1))) for k in set(G) | set(Pp)}
    pv = _params(MWv, MZv, MHv, alpha, xiv); mu2 = mp.mpf(mu) ** 2
    terms = _cbasis({k: c.subs(P2, p2) for k, c in pvr.items()})
    a_pv = _ev_basis(terms, p2, pv, mu2)
    a0 = _ev_vac(_cvac(_taylor_A(E1, E2, 0)), pv, mu2)
    a1 = _ev_vac(_cvac(_taylor_A(E1, E2, 1)), pv, mu2)
    return a_pv[1], a0[1] + p2 * a1[1]


def _mass_check():
    """quadratic part of the Lagrangian: vector masses, Higgs mass, Goldstone masses from L_GF, ghost masses"""
    kin = kinetic_poly(Vreal); pot = potential_poly()
    quad = {}
    for cf, sl in poly_to_monomials(kin, None) + poly_to_monomials(pot, None):
        if len(sl) == 2 and all(x[1] is None for x in sl):
            quad[tuple(x[0] for x in sl)] = phys(cf)
    K, GS, R = mixing_and_ghost()
    gf = sp.expand(-xi / 2 * sum(G_ ** 2 for G_ in GS))
    gold = {str(k): phys(v_) for k, v_ in sp.Poly(gf, *[fsym[n] for n in SCA]).as_dict().items()}
    return quad, gold, GHOSTQ


if __name__ == '__main__':
    mp.mp.dps = DPS
    q_, g_, gh_ = _mass_check()
    print('quadratic terms (vector: coefficient of V.V, i.e. M^2/2 for real, M^2 for W+W-; scalars: -m^2/2):', q_)
    print('gauge-fixing scalar mass terms (monomial exponents in H, chi, php, phm):', g_)
    print('ghost mass terms (cbar u coefficient = -xi M^2):', gh_)
    MWv, MZv, MHv, AL = mp.mpf('80.38'), mp.mpf('91.19'), mp.mpf(125), 1 / mp.mpf(128)
    print('main result: Delta r_bos (M_W=80.38, M_Z=91.19, M_H=125, alpha=1/128)')
    for x in (0, 0.3, 1, 4, 25, 1000):
        p = pieces(MWv, MZv, MHv, AL, x, MWv)
        print('  xi=%-6s SE=% .12e  VBW=% .12e  total=% .15e  (total 1/eps pole % .1e)' % (
            x, p['SE'][1], p['VBW'][1], p['SE'][1] + p['VBW'][1], p['SE'][0] + p['VBW'][0]))
    print('mu independence of the total (xi = 0.3):', [mp.nstr(sum(pieces(MWv, MZv, MHv, AL, 0.3, m_)[k][1] for k in ('SE', 'VBW')), 15) for m_ in (30, 80.38, 900)])
    print('structure of the xi dependence (mu = M_W): building blocks')
    keys = ('SigAAp0', 'SigAZ0', 'SigW0', 'SigWM', 'SigZM', 'dZe', 'dv', 'box', 'XL', 'XN', 'SE', 'VBW')
    for x in (0, 1, 25):
        p = pieces(MWv, MZv, MHv, AL, x, MWv)
        print('  xi=%-4s ' % x + '  '.join('%s=% .6e' % (k, p[k][1]) for k in keys))
    print('second route 1: Ward identities |Sigma_AA(0)|, neutrino charge, L/R charge universality (poles and finite parts):')
    for x in (0, 0.3, 1, 7, 1000):
        print('  xi=%-5s' % x, ['%.1e' % float(v_) for v_ in _ward_checks(MWv, MZv, AL, x, 50)])
    print('second route 2: p^2 -> 0 Taylor route vs PV/IBP route at p^2 = 1e-3 GeV^2 (xi = 0.3):')
    for E in (('A', 'A'), ('A', 'Z'), ('Wp', 'Wm')):
        a, b = _taylor_vs_pv(E[0], E[1], mp.mpf('1e-3'), MWv, MZv, MHv, AL, 0.3, 50)
        print('   ', E, mp.nstr(a, 15), mp.nstr(b, 15))
    print('second route 3: B0 closed form vs Feynman-parameter quadrature:')
    for (p2, m1, m2) in ((MWv ** 2, 0, MWv ** 2), (MZv ** 2, MWv ** 2, MWv ** 2), (MWv ** 2, 0.3 * MWv ** 2, MHv ** 2), (MZv ** 2, 0.01 * MZv ** 2, 0.01 * MZv ** 2)):
        print('   ', mp.nstr(B0_num(p2, m1, m2, MWv ** 2)[1], 15), mp.nstr(B0_quad(mp.mpf(p2), mp.mpf(m1), mp.mpf(m2), MWv ** 2), 15))
    print('second route 4: photon-mass independence of VBW (lambda^2/M_W^2 = 1e-30 vs 1e-22), xi = 0, 1, 7:')
    for l_ in (mp.mpf(10) ** -30, mp.mpf(10) ** -22):
        LAMBDA2_REL = l_
        print('   ', [mp.nstr(pieces(MWv, MZv, MHv, AL, x, MWv, which=('VBW',))['VBW'][1], 15) for x in (0, 1, 7)])
    LAMBDA2_REL = mp.mpf(10) ** -30
    print('second route 5: boxes fully in 4 dimensions (alternative bookkeeping, valid for xi > 0) vs the mixed treatment:')
    bx4 = _cvac(_lepton(boxes_4d()))
    for x in (0.3, 1, 25):
        pv = _params(MWv, MZv, MHv, AL, x)
        ct = mp.re(_derived()['ctree'](*pv))
        b4 = -MWv ** 2 * _ev_vac(bx4, pv, MWv ** 2)[1] / (16 * mp.pi ** 2 * ct ** 2)
        print('    xi=%s  4d: %s  mixed: %s' % (x, mp.nstr(b4, 15), mp.nstr(pieces(MWv, MZv, MHv, AL, x, MWv, which=('VBW',))['box'][1], 15)))
    print('second route 6: Feynman gauge, VBW + (2/sc) Sigma_AZ(0)/M_Z^2 against the closed form a/(4 pi s^2)[6 + (7-4s^2)/(2s^2) ln c^2]')
    for m_ in (30, 300):
        p = pieces(MWv, MZv, MHv, AL, 1, m_)
        c_ = MWv / MZv; s_ = mp.sqrt(1 - c_ ** 2)
        print('    mu=%s:' % m_, mp.nstr(p['VBW'][1] + 2 / (s_ * c_) * p['SigAZ0'][1] / MZv ** 2, 15),
              mp.nstr(AL / (4 * mp.pi * s_ ** 2) * (6 + (7 - 4 * s_ ** 2) / (2 * s_ ** 2) * mp.log(c_ ** 2)), 15))
    print('second route 7: large-M_H slope d Delta r/d ln M_H^2 vs 11 alpha/(48 pi s^2):')
    s2 = 1 - (MWv / MZv) ** 2
    for x in (0, 1, 9):
        h1, h2 = 1e5 * float(MWv), 1e6 * float(MWv)
        sl = (delta_r_bos_xi(MWv, MZv, h2, AL, x) - delta_r_bos_xi(MWv, MZv, h1, AL, x)) / mp.log(h2 ** 2 / h1 ** 2)
        print('    xi=%s  slope/(11 alpha/48 pi s^2) = %s' % (x, mp.nstr(sl / (11 * AL / (48 * mp.pi * s2)), 12)))
