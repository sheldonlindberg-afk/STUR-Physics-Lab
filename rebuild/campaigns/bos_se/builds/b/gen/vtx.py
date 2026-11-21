"""Feynman-rule generator: multilinear plane-wave extraction of vertex functions from the Lagrangian.

All momenta incoming, fields ~ exp(-i p x).  A vertex function is the coefficient of the product of the
slot amplitudes in L (without the factor i), fitted onto a basis of Lorentz structures.
"""
import itertools, random
import sympy as sp

I = sp.I
ETA = [1, -1, -1, -1]
g, gp, c, s, v, lam = sp.symbols('g gp c s v lam')
mw, mz = sp.symbols('mw mz')
R2 = sp.sqrt(2)

# operator table: name -> kind ('v' vector, 's' scalar, 'gh' ghost scalar)
OPS = {
    'A': 'v', 'Z': 'v', 'Wp': 'v', 'Wm': 'v',
    'php': 's', 'phm': 's', 'chi': 's', 'H': 's',
    'cp': 'g', 'cm': 'g', 'cZ': 'g', 'cA': 'g',
    'cbp': 'g', 'cbm': 'g', 'cbZ': 'g', 'cbA': 'g',
}
CHARGE = {'A': 0, 'Z': 0, 'Wp': 1, 'Wm': -1, 'php': 1, 'phm': -1, 'chi': 0, 'H': 0,
          'cp': 1, 'cm': -1, 'cZ': 0, 'cA': 0, 'cbp': 1, 'cbm': -1, 'cbZ': 0, 'cbA': 0}
# sign choices of the gauge fixing (fixed after checking the cancellation of the mixing)
GF_A = -1     # F^+ = d.W^+ + GF_A i mw phi^+
GF_B = -1     # F_Z = d.Z + GF_B mz chi


class F:
    """multilinear polynomial in slot amplitudes: {mask: value}"""
    __slots__ = ('d',)

    def __init__(self, d=None):
        self.d = d if d is not None else {}

    def __add__(self, o):
        if not isinstance(o, F):
            o = F({0: sp.sympify(o)})
        r = dict(self.d)
        for m, x in o.d.items():
            r[m] = r.get(m, 0) + x
        return F(r)
    __radd__ = __add__

    def __neg__(self):
        return F({m: -x for m, x in self.d.items()})

    def __sub__(self, o):
        return self + (-o if isinstance(o, F) else -sp.sympify(o))

    def __rsub__(self, o):
        return (-self) + o

    def __mul__(self, o):
        if not isinstance(o, F):
            o = sp.sympify(o)
            return F({m: x * o for m, x in self.d.items()})
        r = {}
        for ma, xa in self.d.items():
            for mb, xb in o.d.items():
                if ma & mb:
                    continue
                r[ma | mb] = r.get(ma | mb, 0) + xa * xb
        return F(r)
    __rmul__ = __mul__


class Kin:
    """numeric kinematics of one sample"""

    def __init__(self, ops, rng):
        n = len(ops)
        self.ops = ops
        self.e = [[rng.randint(-5, 5) for _ in range(4)] for _ in range(n)]
        p = [[rng.randint(-5, 5) for _ in range(4)] for _ in range(n - 1)]
        p.append([-sum(pp[mu] for pp in p) for mu in range(4)])
        self.p = p

    def P(self, mask):
        return [sum(self.p[i][mu] for i in range(len(self.ops)) if mask >> i & 1) for mu in range(4)]


def dot(a, b):
    return sum(ETA[m] * a[m] * b[m] for m in range(4))


class Fields:
    def __init__(self, kin):
        self.kin = kin
        self.cache = {}

    def sc(self, name):
        d = {}
        for i, o in enumerate(self.kin.ops):
            if o == name:
                d[1 << i] = sp.Integer(1)
        return F(d)

    def vec(self, name):  # upper components
        out = []
        for mu in range(4):
            d = {}
            for i, o in enumerate(self.kin.ops):
                if o == name and self.kin.e[i][mu] != 0:
                    d[1 << i] = sp.Integer(self.kin.e[i][mu])
            out.append(F(d))
        return out

    def dup(self, f, mu):   # d^mu
        return F({m: x * (-I) * self.kin.P(m)[mu] for m, x in f.d.items()})

    def dlow(self, f, mu):  # d_mu
        return F({m: x * (-I) * ETA[mu] * self.kin.P(m)[mu] for m, x in f.d.items()})


def lagrangian(fl, ghosts=True, gf=True, ym=True, higgs=True):
    sc, vec, dup, dlow = fl.sc, fl.vec, fl.dup, fl.dlow
    A, Z, Wp, Wm = vec('A'), vec('Z'), vec('Wp'), vec('Wm')
    W1 = [(Wp[m] + Wm[m]) * (1 / R2) for m in range(4)]
    W2 = [(Wp[m] - Wm[m]) * (I / R2) for m in range(4)]
    W3 = [Z[m] * c + A[m] * s for m in range(4)]
    B = [Z[m] * (-s) + A[m] * c for m in range(4)]
    W = [W1, W2, W3]
    L = F()
    if ym:
        eps = {(0, 1, 2): 1, (1, 2, 0): 1, (2, 0, 1): 1, (0, 2, 1): -1, (2, 1, 0): -1, (1, 0, 2): -1}
        for a in range(3):
            for mu in range(4):
                for nu in range(4):
                    Fa = dup(W[a][nu], mu) - dup(W[a][mu], nu)
                    for (aa, b, cc), sg in eps.items():
                        if aa == a:
                            Fa = Fa + W[b][mu] * W[cc][nu] * (g * sg)
                    L = L + Fa * Fa * (-sp.Rational(1, 4) * ETA[mu] * ETA[nu])
        for mu in range(4):
            for nu in range(4):
                Fb = dup(B[nu], mu) - dup(B[mu], nu)
                L = L + Fb * Fb * (-sp.Rational(1, 4) * ETA[mu] * ETA[nu])
    if higgs:
        php, phm, chi, H = sc('php'), sc('phm'), sc('chi'), sc('H')
        Phi = [php, (H + chi * I + v) * (1 / R2)]
        Phd = [phm, (H - chi * I + v) * (1 / R2)]
        for mu in range(4):
            # tau.W Phi
            tw0 = W[2][mu] * Phi[0] + (W[0][mu] - W[1][mu] * I) * Phi[1]
            tw1 = (W[0][mu] + W[1][mu] * I) * Phi[0] - W[2][mu] * Phi[1]
            D0 = dup(Phi[0], mu) - (tw0 * (g / 2) + B[mu] * Phi[0] * (gp / 2)) * I
            D1 = dup(Phi[1], mu) - (tw1 * (g / 2) + B[mu] * Phi[1] * (gp / 2)) * I
            wt0 = Phd[0] * W[2][mu] + Phd[1] * (W[0][mu] + W[1][mu] * I)
            wt1 = Phd[0] * (W[0][mu] - W[1][mu] * I) - Phd[1] * W[2][mu]
            E0 = dup(Phd[0], mu) + (wt0 * (g / 2) + B[mu] * Phd[0] * (gp / 2)) * I
            E1 = dup(Phd[1], mu) + (wt1 * (g / 2) + B[mu] * Phd[1] * (gp / 2)) * I
            L = L + (E0 * D0 + E1 * D1) * ETA[mu]
        pp = Phd[0] * Phi[0] + Phd[1] * Phi[1]
        L = L + pp * (lam * v * v) + pp * pp * (-lam)   # V = -mu^2 Phi^dag Phi + lam (Phi^dag Phi)^2, mu^2 = lam v^2
    if gf:
        php, phm, chi = sc('php'), sc('phm'), sc('chi')
        divp = F(); divm = F(); divz = F(); diva = F()
        for mu in range(4):
            divp = divp + dlow(Wp[mu], mu); divm = divm + dlow(Wm[mu], mu)
            divz = divz + dlow(Z[mu], mu); diva = diva + dlow(A[mu], mu)
        Fp = divp + php * (I * GF_A * mw)
        Fm = divm + phm * (-I * GF_A * mw)
        Fz = divz + chi * (GF_B * mz)
        L = L - Fp * Fm - Fz * Fz * sp.Rational(1, 2) - diva * diva * sp.Rational(1, 2)
    if ghosts:
        cp, cm, cZ, cA = sc('cp'), sc('cm'), sc('cZ'), sc('cA')
        cbp, cbm, cbZ, cbA = sc('cbp'), sc('cbm'), sc('cbZ'), sc('cbA')
        th = [(cp + cm) * (1 / R2), (cp - cm) * (I / R2), cZ * c + cA * s]   # theta^1,2,3 ; theta^0 below
        th0 = cZ * (-s) + cA * c
        eps3 = [(0, 1, 2, 1), (1, 2, 0, 1), (2, 0, 1, 1), (0, 2, 1, -1), (2, 1, 0, -1), (1, 0, 2, -1)]
        # delta W^a_mu = d_mu th^a + g eps^{abc} W^b_mu th^c ; contract with d^mu (upper d on upper W -> use dlow on upper comps)
        def dW(a):
            tot = F()
            for mu in range(4):
                x = dup(th[a], mu)
                for (aa, b, cc, sg) in eps3:
                    if aa == a:
                        x = x + W[b][mu] * th[cc] * (g * sg)
                tot = tot + dlow(x, mu)
            return tot  # = d_mu (delta W^{a mu})
        d1, d2, d3 = dW(0), dW(1), dW(2)
        d0 = F()
        for mu in range(4):
            d0 = d0 + dlow(dup(th0, mu), mu)
        # scalar variations: delta Phi = i [ (g/2) theta.tau + (gp/2) theta0 ] Phi
        php, phm, chi, H = sc('php'), sc('phm'), sc('chi'), sc('H')
        P1, P2 = php, (H + chi * I + v) * (1 / R2)
        Q1, Q2 = phm, (H - chi * I + v) * (1 / R2)
        t12m = th[0] - th[1] * I      # theta1 - i theta2
        t12p = th[0] + th[1] * I
        dP1 = ((th[2] * P1 + t12m * P2) * (g / 2) + th0 * P1 * (gp / 2)) * I
        dP2 = ((t12p * P1 - th[2] * P2) * (g / 2) + th0 * P2 * (gp / 2)) * I
        dQ1 = ((th[2] * Q1 + t12p * Q2) * (g / 2) + th0 * Q1 * (gp / 2)) * (-I)
        dQ2 = ((t12m * Q1 - th[2] * Q2) * (g / 2) + th0 * Q2 * (gp / 2)) * (-I)
        dchi = (dP2 - dQ2) * (1 / (I * R2))
        dFp = (d1 - d2 * I) * (1 / R2) + dP1 * (I * GF_A * mw)     # delta F^+ , W^+ = (W1 - i W2)/sqrt2
        dFm = (d1 + d2 * I) * (1 / R2) + dQ1 * (-I * GF_A * mw)
        dFz = d3 * c - d0 * s + dchi * (GF_B * mz)
        dFa = d3 * s + d0 * c
        L = L - (cbp * dFm + cbm * dFp + cbZ * dFz + cbA * dFa)
    return L


def basis(ops):
    """list of (descriptor, numeric function(kin)) ; descriptor items: ('g',i,j) or ('p',l,k) = p_l . e_k"""
    kinds = ['v' if OPS[o] == 'v' else 's' for o in ops]
    vs = [i for i, k in enumerate(kinds) if k == 'v']
    ss = [i for i, k in enumerate(kinds) if k == 's']
    n = len(ops)
    out = []
    if n == 2:
        if len(vs) == 2:
            out = [(('g', 0, 1),), (('g', 0, 1), ('pp', 0, 0)), (('p', 0, 1), ('p', 1, 0))]
        elif len(vs) == 0:
            out = [(), (('pp', 0, 0),)]
        else:
            out = [(('p', ss[0], vs[0]),)]
    elif n == 3:
        if len(vs) == 3:
            for (i, j, k) in [(0, 1, 2), (1, 2, 0), (2, 0, 1)]:
                for l in (i, j):
                    out.append((('g', i, j), ('p', l, k)))
        elif len(vs) == 2:
            out = [(('g', vs[0], vs[1]),)]
        elif len(vs) == 1:
            out = [(('p', l, vs[0]),) for l in ss]
        else:
            out = [()]
    elif n == 4:
        if len(vs) == 4:
            out = [(('g', 0, 1), ('g', 2, 3)), (('g', 0, 2), ('g', 1, 3)), (('g', 0, 3), ('g', 1, 2))]
        elif len(vs) == 2:
            out = [(('g', vs[0], vs[1]),)]
        elif len(vs) == 0:
            out = [()]
    return out


def evalstruct(desc, kin):
    val = 1
    for it in desc:
        if it[0] == 'g':
            val *= dot(kin.e[it[1]], kin.e[it[2]])
        elif it[0] == 'p':
            val *= dot(kin.p[it[1]], kin.e[it[2]])
        elif it[0] == 'pp':
            val *= dot(kin.p[it[1]], kin.p[it[2]])
    return val


_cache = {}


def vertex(ops, **kw):
    """vertex function (coefficient in L) for the ordered operator tuple, as {descriptor: coefficient}"""
    key = (tuple(ops), tuple(sorted(kw.items())))
    if key in _cache:
        return _cache[key]
    ops = list(ops)
    if sum(CHARGE[o] for o in ops) != 0:
        _cache[key] = {}
        return {}
    B = basis(ops)
    rng = random.Random(12345)
    nsamp = len(B) + 6
    rows, rhs = [], []
    for _ in range(nsamp):
        kin = Kin(ops, rng)
        fl = Fields(kin)
        L = lagrangian(fl, **kw)
        val = sp.expand(L.d.get((1 << len(ops)) - 1, 0))
        rows.append([evalstruct(d, kin) for d in B])
        rhs.append(val)
    if all(x == 0 for x in rhs):
        _cache[key] = {}
        return {}
    M = sp.Matrix(rows)
    Rv = sp.Matrix(rhs)
    sol = (M.T * M).LUsolve(M.T * Rv)
    sol = sol.applyfunc(sp.expand)
    res = (M * sol - Rv).applyfunc(sp.expand)
    assert all(x == 0 for x in res), ("basis incomplete", ops, res.T)
    out = {B[i]: sol[i] for i in range(len(B)) if sol[i] != 0}
    _cache[key] = out
    return out
