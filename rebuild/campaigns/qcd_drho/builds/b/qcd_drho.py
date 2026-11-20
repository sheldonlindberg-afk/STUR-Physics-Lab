"""O(alpha_s) QCD correction to Delta rho of the (t, b = massless) doublet, from first principles.

Everything is computed: d-dimensional Dirac traces of the one- and two-loop diagrams of the vector
correlators at q = 0, Wick rotation, partial fractions, reduction to the one-loop tadpole and the two
two-loop vacuum masters (masses (m,m,0) and (m,0,0)), mass renormalisation (pole and MS-bar) from the
one-loop quark self-energy, and the Laurent expansion in eps.  See DERIVATION.md.

Units inside the engine: m = 1; the outer loop normalisation N_C/(16 pi^2) and the inner one
g_s^2 C_F/(16 pi^2) are factored out (they are restored analytically below).
"""
import math
import functools
import itertools
import sympy as sp

# ---------------------------------------------------------------- symbols
eps = sp.Symbol("eps")
d = 4 - 2 * eps
xi = sp.Symbol("xi")                 # covariant gauge parameter (xi = 1: Feynman gauge)
Lmu = sp.Symbol("Lmu")               # ln(mu_bar^2 / m^2)
KK, LL, GG = sp.symbols("KK LL GG")  # Euclidean K^2, L^2, (K-L)^2
DOT = {p: sp.Symbol(p) for p in ("kk", "kl", "ll", "kq", "lq", "qq")}
G1p, G1m, G2p, G2m = sp.symbols("G1p G1m G2p G2m")   # Gamma(1+eps), Gamma(1-eps), Gamma(1+2eps), Gamma(1-2eps)
BASE = {1: G1p, -1: G1m, 2: G2p, -2: G2m}
I = sp.I


def dot(a, b):
    return DOT["".join(sorted(a + b))]


# ---------------------------------------------------------------- d-dimensional Dirac trace
def _matchings(n):
    """All perfect matchings of range(n) with the sign of Tr(gamma ... gamma) recursion."""
    if n == 0:
        yield 1, []
        return
    def rec(items):
        if not items:
            yield 1, []
            return
        a = items[0]
        for j in range(1, len(items)):
            rest = items[1:j] + items[j + 1:]
            s = (-1) ** (j - 1)
            for s2, m in rec(rest):
                yield s * s2, [(a, items[j])] + m
    yield from rec(list(range(n)))


@functools.lru_cache(maxsize=None)
def trace(atoms):
    """Tr[a1 ... an] with Tr 1 = 4; atoms are momentum names ('k','l','q') or index names
    (every index name occurs exactly twice and is contracted)."""
    n = len(atoms)
    if n % 2:
        return sp.Integer(0)
    isidx = [len(a) > 1 for a in atoms]
    other = {}
    for i, a in enumerate(atoms):
        if isidx[i]:
            js = [j for j, b in enumerate(atoms) if b == a and j != i]
            other[i] = js[0]
    total = sp.Integer(0)
    for sign, match in _matchings(n):
        partner = {}
        for a, b in match:
            partner[a], partner[b] = b, a
        seen = set()
        val = sp.Integer(1)
        for s in range(n):
            if isidx[s] or s in seen:
                continue
            seen.add(s)
            nxt = partner[s]
            while isidx[nxt]:
                seen.add(nxt)
                j = other[nxt]
                seen.add(j)
                nxt = partner[j]
            seen.add(nxt)
            val *= dot(atoms[s], atoms[nxt])
        for s in range(n):
            if s in seen:
                continue
            cur = s
            while cur not in seen:           # index-only cycle -> g^a_a = d
                seen.add(cur)
                p = partner[cur]
                seen.add(p)
                cur = other[p]
            val *= d
        total += sign * val
    return 4 * total


def trace_slots(slots):
    """slots: list of lists of (coef, atom or None); returns Tr of the product (expanded)."""
    res = sp.Integer(0)
    for combo in itertools.product(*slots):
        c = sp.Integer(1)
        atoms = []
        for coef, at in combo:
            c *= coef
            if at is not None:
                atoms.append(at)
        if c != 0:
            res += c * trace(tuple(atoms))
    return sp.expand(res)


# ---------------------------------------------------------------- Gamma functions of n + k eps
def gam(n, k):
    """Gamma(n + k eps) for integer n, k in terms of the base Gamma(1 + k eps)."""
    n = int(n)
    if k == 0:
        if n <= 0:
            raise ZeroDivisionError("Gamma at a pole")
        return sp.factorial(n - 1)
    g = BASE[k]
    if n >= 1:
        return g * sp.prod([j + k * eps for j in range(1, n)])
    return g / sp.prod([j + k * eps for j in range(n, 1)])


def rgam(n, k):
    """1/Gamma(n + k eps); zero at the poles of Gamma (k = 0, n <= 0)."""
    if k == 0 and n <= 0:
        return sp.Integer(0)
    return 1 / gam(n, k)


# d = 4 - 2 eps: write each Gamma argument as integer + k*eps
def tad(a, a0):
    """\\int d^dK/pi^{d/2} (K^2)^{-a0} (K^2+1)^{-a}, a >= 1."""
    if a <= 0:
        return sp.Integer(0)
    # Gamma(d/2 - a0) Gamma(a + a0 - d/2) / (Gamma(d/2) Gamma(a))
    return gam(2 - a0, -1) * gam(a + a0 - 2, 1) * rgam(2, -1) * rgam(a, 0)


def master_mm0(a, b, c):
    """\\int\\int d^dK d^dL/pi^d 1/[(K^2+1)^a (L^2+1)^b ((K-L)^2)^c], a, b >= 1, c integer."""
    if a <= 0 or b <= 0:
        return sp.Integer(0)
    return (gam(a + b + c - 4, 2) * gam(a + c - 2, 1) * gam(b + c - 2, 1) * gam(2 - c, -1)
            * rgam(a, 0) * rgam(b, 0) * rgam(2, -1) * rgam(a + b + 2 * c - 4, 2))


def master_m00(a, b, c):
    """\\int\\int d^dK d^dL/pi^d 1/[(K^2+1)^a (L^2)^b ((K-L)^2)^c]."""
    if a <= 0 or b <= 0 or c <= 0:
        return sp.Integer(0)             # massless subloop with a polynomial line: scaleless
    G = gam(2 - b, -1) * gam(2 - c, -1) * gam(b + c - 2, 1) * rgam(b, 0) * rgam(c, 0) * rgam(4 - b - c, -2)
    return G * gam(4 - b - c, -2) * gam(a + b + c - 4, 2) * rgam(2, -1) * rgam(a, 0)


@functools.lru_cache(maxsize=None)
def pfrac(i, p0, p1):
    """x^i / (x^p0 (x+1)^p1) as a list of (kind, power, coef): kind 'M' -> (x+1)^-power, '0' -> x^-power."""
    x = sp.Symbol("x")
    if p1 == 0:
        return [("0", p0 - i, sp.Integer(1))]
    expr = sp.apart(x**i / (x**p0 * (x + 1)**p1), x)
    out = []
    for t in sp.Add.make_args(expr):
        pw = t.as_powers_dict()
        coef = sp.Integer(1)
        kind, power = "0", 0
        for base, e in pw.items():
            if base == x:
                kind, power = "0", -e
            elif base == x + 1:
                kind, power = "M", -e
            else:
                coef *= base**e
        out.append((kind, int(power), coef))
    return out


# ---------------------------------------------------------------- diagrams
def prop(mom, M):
    """Quark propagator i (pslash + M)/(p^2 - M^2): (factor, slot, den-key)."""
    slot = [(c, a) for a, c in mom.items()] + ([(M, None)] if M != 0 else [])
    return I, slot, (tuple(sorted(mom)), "M" if M != 0 else "0")


def build(kind, m1, m2, gauge_part, dm=None):
    """Minkowski integrand of a q = 0 diagram of L_V(m1, m2) (contracted with g_{mu nu}/d).
    Returns (numerator expression, dens dict, number of loops).  kind in R, S1, S2, CT1, CT2, ONE."""
    k, l = {"k": 1}, {"l": 1}
    V = [(1, "mu")]
    if gauge_part == "feyn":
        A, B, gfac, gden = [(1, "al")], [(1, "al")], -I, 1
    else:  # longitudinal part: -i * (-(1-xi)) G_al G_be / (G^2)^2 with G = k - l
        A = B = [(1, "k"), (-1, "l")]
        gfac, gden = -I * (-(1 - xi)), 2
    vtx = -I
    if kind == "ONE":
        P1, P2 = prop(k, m1), prop(k, m2)
        seq, facs, dens = [V, P1[1], V, P2[1]], [P1[0], P2[0]], [P1[2], P2[2]]
        loops = 1
    elif kind == "R":
        p1k, p1l, p2l, p2k = prop(k, m1), prop(l, m1), prop(l, m2), prop(k, m2)
        seq = [V, p1k[1], A, p1l[1], V, p2l[1], B, p2k[1]]
        facs = [p1k[0], p1l[0], p2l[0], p2k[0], vtx, vtx, gfac]
        dens = [p1k[2], p1l[2], p2l[2], p2k[2]] + [(("G",), "0")] * gden
        loops = 2
    elif kind == "S1":
        a, b, c, e = prop(k, m1), prop(l, m1), prop(k, m1), prop(k, m2)
        seq = [V, a[1], A, b[1], B, c[1], V, e[1]]
        facs = [a[0], b[0], c[0], e[0], vtx, vtx, gfac]
        dens = [a[2], b[2], c[2], e[2]] + [(("G",), "0")] * gden
        loops = 2
    elif kind == "S2":
        a, e, b, c = prop(k, m1), prop(k, m2), prop(l, m2), prop(k, m2)
        seq = [V, a[1], V, e[1], A, b[1], B, c[1]]
        facs = [a[0], e[0], b[0], c[0], vtx, vtx, gfac]
        dens = [a[2], e[2], b[2], c[2]] + [(("G",), "0")] * gden
        loops = 2
    elif kind == "CT1":
        a, b, e = prop(k, m1), prop(k, m1), prop(k, m2)
        seq, facs, dens = [V, a[1], b[1], V, e[1]], [a[0], b[0], e[0], -I * dm], [a[2], b[2], e[2]]
        loops = 1
    elif kind == "CT2":
        a, e, b = prop(k, m1), prop(k, m2), prop(k, m2)
        seq, facs, dens = [V, a[1], V, e[1], b[1]], [a[0], e[0], b[0], -I * dm], [a[2], e[2], b[2]]
        loops = 1
    num = -sp.prod(facs) * trace_slots(seq) / d          # fermion loop (-1), g_{mu nu}/d
    dd = {}
    for key in dens:
        dd[key] = dd.get(key, 0) + 1
    return sp.expand(num), dd, loops


def wick_reduce(num, dens, loops):
    """Wick-rotate a Minkowski integrand and reduce it to Gamma-function masters.
    Returns the value of \\int (d^dk/(2pi)^d)^loops [...] in units (1/(16 pi^2))^loops, outer (4pi)^eps dropped,
    inner loop carrying (e^{gamma} mu_bar^2/m^2)^eps."""
    sub = {DOT["kk"]: -KK, DOT["ll"]: -LL, DOT["kl"]: -(KK + LL - GG) / 2}
    num = sp.expand(num.subs(sub))
    sign = (-1) ** sum(dens.values())
    pK0, pK1 = dens.get((("k",), "0"), 0), dens.get((("k",), "M"), 0)
    pL0, pL1 = dens.get((("l",), "0"), 0), dens.get((("l",), "M"), 0)
    pG = dens.get((("G",), "0"), 0)
    poly = sp.Poly(num, KK, LL, GG)
    res = sp.Integer(0)
    for (i, j, g), coef in poly.terms():
        if loops == 1:
            for kind, pw, c1 in pfrac(i, pK0, pK1):
                if kind == "M":
                    res += coef * c1 * tad(pw, 0)
            continue
        for kk_, pk, ck in pfrac(i, pK0, pK1):
            for kl_, pl, cl in pfrac(j, pL0, pL1):
                c = pG - g
                if kk_ == "M" and kl_ == "M":
                    val = master_mm0(pk, pl, c)
                elif kk_ == "M":
                    val = master_m00(pk, pl, c)
                elif kl_ == "M":
                    val = master_m00(pl, pk, c)
                else:
                    val = 0
                if val != 0:
                    res += coef * ck * cl * val
    pref = sign * I**loops
    if loops == 2:
        pref *= sp.exp(eps * (sp.EulerGamma + Lmu))
    return pref * res


class Ser:
    """Truncated Laurent series in eps: {power: coef}, exact up to and including power `top`."""
    def __init__(self, c, top):
        self.c = {k: v for k, v in c.items() if k <= top and v != 0}
        self.top = top

    def vmin(self):
        return min(self.c) if self.c else self.top + 1

    def __add__(self, o):
        top = min(self.top, o.top)
        c = dict(self.c)
        for k, v in o.c.items():
            c[k] = c.get(k, 0) + v
        return Ser(c, top)

    def __mul__(self, o):
        if not self.c or not o.c:
            return Ser({}, min(self.top + o.vmin(), o.top + self.vmin()))
        top = min(self.top + o.vmin(), o.top + self.vmin())
        c = {}
        for k1, v1 in self.c.items():
            for k2, v2 in o.c.items():
                if k1 + k2 <= top:
                    c[k1 + k2] = c.get(k1 + k2, 0) + v1 * v2
        return Ser({k: sp.expand(v) for k, v in c.items()}, top)

    def inv(self):
        v = self.vmin()
        a = [sp.expand(self.c.get(v + i, 0)) for i in range(self.top - v + 1)]
        n = len(a)
        b = [1 / a[0]]
        for i in range(1, n):
            b.append(sp.expand(-sum(a[j] * b[i - j] for j in range(1, i + 1)) / a[0]))
        return Ser({-v + i: b[i] for i in range(n)}, -v + n - 1)


TOPDEF = 9


def _exp_ser(arg):
    """exp of a series with only positive powers."""
    out = Ser({0: sp.Integer(1)}, arg.top)
    term = Ser({0: sp.Integer(1)}, arg.top)
    for n in range(1, arg.top + 1):
        term = term * arg * Ser({0: sp.Rational(1, n)}, arg.top + 10)
        out = out + term
    return out


@functools.lru_cache(maxsize=None)
def _gamma_ser(k):
    """Gamma(1 + k eps) = exp(-gamma k eps + sum_n (-1)^n zeta(n) (k eps)^n / n)."""
    c = {1: -sp.EulerGamma * k}
    for n in range(2, TOPDEF + 1):
        c[n] = (-1)**n * sp.zeta(n) * sp.Integer(k)**n / n
    return _exp_ser(Ser(c, TOPDEF))


def to_ser(e):
    if e == eps:
        return Ser({1: sp.Integer(1)}, TOPDEF + 20)
    if e in (G1p, G1m, G2p, G2m):
        return _gamma_ser({G1p: 1, G1m: -1, G2p: 2, G2m: -2}[e])
    if not e.has(eps) and not e.has(G1p, G1m, G2p, G2m):
        return Ser({0: e}, TOPDEF + 20)
    if e.is_Add:
        out = None
        for t in e.args:
            s = to_ser(t)
            out = s if out is None else out + s
        return out
    if e.is_Mul:
        out = None
        for t in e.args:
            s = to_ser(t)
            out = s if out is None else out * s
        return out
    if e.is_Pow and e.exp.is_Integer:
        b = to_ser(e.base)
        n = int(e.exp)
        if n < 0:
            b, n = b.inv(), -n
        out = Ser({0: sp.Integer(1)}, TOPDEF + 20)
        for _ in range(n):
            out = out * b
        return out
    if isinstance(e, sp.exp):
        a = to_ser(e.args[0])
        assert a.vmin() >= 1
        a.top = min(a.top, TOPDEF)
        return _exp_ser(a)
    raise ValueError(f"cannot expand {e}")


def laurent(expr, order=1):
    """Laurent expansion in eps keeping powers < order (base Gammas expanded)."""
    s = to_ser(sp.expand(expr))
    assert s.top >= order - 1, (s.top, order)
    return sp.Add(*[sp.expand(v) * eps**k for k, v in s.c.items() if k < order])


# ---------------------------------------------------------------- mass counterterm
def sigma_onshell():
    """Sigma(pslash = m)/m in units g_s^2 C_F/(16 pi^2), with (e^gamma mu_bar^2/m^2)^eps; Feynman gauge.
    -i Sigma = (-i)(i)(-i)(-i) C_F \\int gamma^al (lslash+m) gamma_al /[(l^2-m^2)(p-l)^2]
             = -C_F \\int [...];  Wick: \\int d^dl/(2pi)^d -> i/(16 pi^2) Gamma(eps) \\int_0^1 dx Delta^-eps,
    Feynman parameter x on the massive line, Delta = x^2 m^2 on shell, l -> (1-x) p.  Hence
    Sigma(m)/m = Gamma(eps) e^{eps(gamma+L)} [ (2-d) B(1-2eps,2) + d B(1-2eps,1) ]."""
    # Dirac algebra gamma^al lslash gamma_al = (2-d) lslash, gamma^al gamma_al = d, from the trace engine:
    c_l = sp.simplify(trace(("al", "k", "al", "l")) / (4 * DOT["kl"]))
    c_1 = sp.simplify(trace(("al", "al")) / 4)
    assert sp.simplify(c_l - (2 - d)) == 0 and sp.simplify(c_1 - d) == 0
    B1 = gam(1, -2) * rgam(2, -2)                 # \\int_0^1 x^{-2eps} dx
    B2 = gam(1, -2) * gam(2, 0) * rgam(3, -2)     # \\int_0^1 x^{-2eps} (1-x) dx
    minus_i_sigma = (-I) * I * (-I) * (-I) * I * gam(0, 1) * (c_l * B2 + c_1 * B1) * sp.exp(eps * (sp.EulerGamma + Lmu))
    return sp.expand(minus_i_sigma / (-I))


@functools.lru_cache(maxsize=None)
def dm_hat(scheme):
    """dm / m in units g_s^2 C_F/(16 pi^2) (exact in eps for the pole scheme)."""
    s = sigma_onshell()
    if scheme == "pole":
        return -s
    pole = laurent(s, 0)          # terms with negative powers of eps
    pole = sp.expand(pole)
    pure = sum(pole.coeff(eps, -n) * eps**(-n) for n in (1, 2))
    return -sp.expand(pure)


# ---------------------------------------------------------------- the combination X
PAIRS = [((1, -1), 1), ((1, 0), -4)]     # X = L_V(m, -m) - 4 L_V(m, 0)


def correlator(m1, m2, order, scheme="pole", gauge="feyn", parts=None):
    """L_V(m1, m2)(0): order 1 -> one loop, order 2 -> O(g_s^2 C_F) part, exact in eps (Gamma basis)."""
    if order == 1:
        n, dd, lp = build("ONE", m1, m2, "feyn")
        return wick_reduce(n, dd, lp)
    tot = sp.Integer(0)
    kinds = parts or ("R", "S1", "S2", "CT1", "CT2")
    for kind in kinds:
        if kind in ("CT1", "CT2"):
            M = m1 if kind == "CT1" else m2
            if M == 0 or gauge != "feyn":
                continue
            n, dd, lp = build(kind, m1, m2, "feyn", dm=M * dm_hat(scheme))
            # counterterm: one loop integral; dm carries the inner-loop factor already
            tot += wick_reduce(n, dd, lp)
        else:
            tot += _diag(kind, m1, m2, gauge)
    return tot


@functools.lru_cache(maxsize=None)
def _diag(kind, m1, m2, gauge):
    n, dd, lp = build(kind, m1, m2, gauge)
    return wick_reduce(n, dd, lp)


@functools.lru_cache(maxsize=None)
def _x_one():
    return sum(w * correlator(a, b, 1) for (a, b), w in PAIRS)


@functools.lru_cache(maxsize=None)
def _x_two(scheme):
    return sum(w * correlator(a, b, 2, scheme) for (a, b), w in PAIRS)


def _num(z):
    return complex(sp.N(z, 30))


@functools.lru_cache(maxsize=None)
def oneloop_value():
    """v1 with X^(1) = (N_C/(16 pi^2)) m^2 v1 at eps -> 0."""
    return sp.nsimplify(sp.simplify(laurent(_x_one(), 1).subs(eps, 0)))


@functools.lru_cache(maxsize=None)
def coeff_unit(scheme):
    """c / C_F as an exact sympy expression in Lmu = ln(mu_bar^2/m^2); also checks pole cancellation."""
    x2 = sp.expand(laurent(_x_two(scheme), 1))
    for n in (1, 2, 3, 4):
        assert sp.simplify(x2.coeff(eps, -n)) == 0, f"uncancelled 1/eps^{n} pole in {scheme}"
    fin = sp.simplify(x2.coeff(eps, 0))
    assert not fin.has(sp.EulerGamma)
    v1 = oneloop_value()
    # X = (N_C/16pi^2) m^2 [v1 + (g^2 C_F/16 pi^2) v2],  g^2/(16 pi^2) = (alpha_s/pi)/4
    return sp.nsimplify(sp.simplify(sp.expand(fin / (4 * v1))))


# ---------------------------------------------------------------- exports
def delta_rho_oneloop(m, GF, NC):
    """Delta rho_0 = -(i/(4 v^2)) X^(1), X^(1) = (N_C/(16 pi^2)) m^2 v1, v^2 = 1/(sqrt2 G_F)."""
    v1 = _num(oneloop_value())
    val = -1j / 4 * v1 * NC * m**2 * math.sqrt(2) * GF / (16 * math.pi**2)
    return val.real


@functools.lru_cache(maxsize=None)
def _coeff_parts(scheme):
    e = sp.expand(coeff_unit(scheme))
    return float(e.coeff(Lmu, 0)), float(e.coeff(Lmu, 1))


def qcd_coeff(scheme, CF, mu_over_m):
    if scheme == "pole":
        a, _ = _coeff_parts("pole")
        return CF * a
    if scheme == "msbar":
        a, b = _coeff_parts("msbar")
        return CF * (a + b * 2 * math.log(mu_over_m))
    raise ValueError(scheme)


def delta_rho_qcd(m, GF, NC, CF, alphas, scheme, mu_over_m):
    return delta_rho_oneloop(m, GF, NC) * (1 + qcd_coeff(scheme, CF, mu_over_m) * alphas / math.pi)


PROVENANCE = {
    "delta_rho_oneloop": ("derived", "one-loop d-dim trace + tadpoles of X = L_V(m,-m) - 4 L_V(m,0); Delta rho = -(i/4v^2) X"),
    "qcd_coeff": ("derived", "two-loop q=0 diagrams (rung, self-energies) reduced to (m,m,0)/(m,0,0) vacuum masters + mass counterterm (pole / MS-bar) from one-loop Sigma"),
    "delta_rho_qcd": ("derived", "Delta rho_0 (1 + c alpha_s/pi)"),
}


# ---------------------------------------------------------------- second route: Ward identity / scalar correlator
def _prop_q(mom, M, qexp):
    """Propagator with the external q Taylor-expanded: list of (tpow, factor, slot, den-key, den-pow)."""
    key = (tuple(sorted(mom)), "M" if M != 0 else "0")
    base = [(c, a) for a, c in mom.items()] + ([(M, None)] if M != 0 else [])
    if not qexp:
        return [(0, I, base, key, 1)]
    p = list(mom)[0]
    pq = dot(p, "q")
    qq = DOT["qq"]
    return [(0, I, base, key, 1),
            (1, I, [(1, "q")], key, 1),
            (1, I * (-2 * pq), base, key, 2),
            (2, I * (-2 * pq), [(1, "q")], key, 2),
            (2, I * (-qq), base, key, 2),
            (2, I * (4 * pq**2), base, key, 3)]


def scalar_q2(kind, m1, m2, dm=None):
    """q^2-coefficient of L_S(q) = (-1) Tr[1 S1(k+q) 1 S2(k)] (+ gluon corrections), q routed on line 1."""
    k, l = {"k": 1}, {"l": 1}
    A = [(1, "al")]
    if kind == "ONE":
        props = [(_prop_q(k, m1, True), None), (_prop_q(k, m2, False), None)]
        extra, loops, gl = sp.Integer(1), 1, 0
        order = ["P0", "P1"]
    elif kind == "R":
        props = [(_prop_q(k, m1, True), None), (_prop_q(l, m1, True), None), (_prop_q(l, m2, False), None), (_prop_q(k, m2, False), None)]
        order = ["P0", "A", "P1", "P2", "A", "P3"]
        extra, loops, gl = (-I) * (-I) * (-I), 2, 1
    elif kind == "S1":
        props = [(_prop_q(k, m1, True), None), (_prop_q(l, m1, True), None), (_prop_q(k, m1, True), None), (_prop_q(k, m2, False), None)]
        order = ["P0", "A", "P1", "A", "P2", "P3"]
        extra, loops, gl = (-I) * (-I) * (-I), 2, 1
    elif kind == "S2":
        props = [(_prop_q(k, m1, True), None), (_prop_q(k, m2, False), None), (_prop_q(l, m2, False), None), (_prop_q(k, m2, False), None)]
        order = ["P0", "P1", "A", "P2", "A", "P3"]
        extra, loops, gl = (-I) * (-I) * (-I), 2, 1
    elif kind == "CT1":
        props = [(_prop_q(k, m1, True), None), (_prop_q(k, m1, True), None), (_prop_q(k, m2, False), None)]
        order = ["P0", "P1", "P2"]
        extra, loops, gl = -I * dm, 1, 0
    elif kind == "CT2":
        props = [(_prop_q(k, m1, True), None), (_prop_q(k, m2, False), None), (_prop_q(k, m2, False), None)]
        order = ["P0", "P1", "P2"]
        extra, loops, gl = -I * dm, 1, 0
    groups = {}
    for choice in itertools.product(*[p[0] for p in props]):
        tp = sum(c[0] for c in choice)
        if tp != 2:
            continue
        fac = extra
        dens = {}
        slots = []
        pi = 0
        for o in order:
            if o == "A":
                slots.append(A)
            else:
                c = choice[int(o[1])]
                slots.append(c[2])
        for c in choice:
            fac = fac * c[1]
            dens[c[3]] = dens.get(c[3], 0) + c[4]
        if gl:
            dens[(("G",), "0")] = 1
        key = tuple(sorted(dens.items()))
        num = -fac * trace_slots(slots)
        groups[key] = groups.get(key, 0) + num
    tot = sp.Integer(0)
    for key, num in groups.items():
        pq = sp.Poly(sp.expand(num), DOT["kq"], DOT["lq"], DOT["qq"])
        avg = {(2, 0, 0): DOT["kk"] / d, (1, 1, 0): DOT["kl"] / d, (0, 2, 0): DOT["ll"] / d, (0, 0, 1): 1}
        num = sp.Integer(0)
        for mon, cf in pq.terms():
            if cf != 0:
                num += cf * avg[mon]      # q^al q^be -> q^2 g^{al be}/d ; coefficient of q^2
        num = sp.expand(num)
        tot += wick_reduce(num, dict(key), loops)
    return tot


def x_ward(order, scheme="pole"):
    """X through the Ward identity: L_V(m1,m2)(0) = (m01 - m02)^2 * [q^2 coefficient of L_S]."""
    tot = sp.Integer(0)
    for (a, b), w in PAIRS:
        D = a - b
        if order == 1:
            tot += w * D**2 * scalar_q2("ONE", a, b)
            continue
        s2 = sum(scalar_q2(kd, a, b) for kd in ("R", "S1", "S2"))
        if a:
            s2 += scalar_q2("CT1", a, b, dm=a * dm_hat(scheme))
        if b:
            s2 += scalar_q2("CT2", a, b, dm=b * dm_hat(scheme))
        dD = (a - b) * dm_hat(scheme)       # dm1 - dm2 = (m1 - m2) * dm_hat
        tot += w * (D**2 * s2 + 2 * D * dD * scalar_q2("ONE", a, b))
    return tot


def _formula_general_d(kind, a, b, c, dd):
    """The two masters with general-d Gamma functions (mpmath), as written in DERIVATION.md."""
    import mpmath as mp
    G = mp.gamma
    if kind == "mm0":
        return G(a + b + c - dd) * G(a + c - dd / 2) * G(b + c - dd / 2) * G(dd / 2 - c) / (
            G(a) * G(b) * G(dd / 2) * G(a + b + 2 * c - dd))
    Gb = G(dd / 2 - b) * G(dd / 2 - c) * G(b + c - dd / 2) / (G(b) * G(c) * G(dd - b - c))
    return Gb * G(dd - b - c) * G(a + b + c - dd) / (G(dd / 2) * G(a))


def check_masters_numerically():
    """Second route for the masters.
    (i) direct numerical integration by a different method: radial integrals with the exact angular average
        of 1/(K-L)^2  (d = 4: 1/max(K^2,L^2);  d = 3: ln((K+L)/|K-L|)/(2 K L)), compared with the general-d formula;
    (ii) the eps-reduced Gamma basis used by the engine, evaluated at eps = 0.3, against the general-d formula."""
    import mpmath as mp
    mp.mp.dps = 20
    out = []
    # d = 4, measure d^4K/pi^2 = x dx (x = K^2)
    for (a, b) in ((2, 2), (3, 2)):
        f = lambda x, y: x * y / ((x + 1)**a * (y + 1)**b * max(x, y))
        num = mp.quad(lambda x: mp.quad(lambda y: f(x, y), [0, x, mp.inf]), [0, 1, mp.inf])
        out.append((f"I({a},{b},1) d=4", float(num), float(_formula_general_d("mm0", a, b, 1, 4))))
    # d = 3, measure d^3K/pi^{3/2} = 4 K^2 dK / sqrt(pi)
    w = 4 / mp.sqrt(mp.pi)
    ang = lambda K, L: mp.log((K + L) / abs(K - L)) / (2 * K * L) if K != L else 0   # integrable log singularity
    num = mp.quad(lambda K: mp.quad(lambda L: w * w * K**2 * L**2 * ang(K, L) / ((K**2 + 1)**2 * (L**2 + 1)), [0, K, mp.inf]), [0, 1, mp.inf])
    out.append(("I(2,1,1) d=3", float(num), float(_formula_general_d("mm0", 2, 1, 1, 3))))
    num = mp.quad(lambda K: mp.quad(lambda L: w * w * K**2 * L**2 * ang(K, L) / ((K**2 + 1)**2 * L**2), [0, K, mp.inf]), [0, 1, mp.inf])
    out.append(("J(2;1,1) d=3", float(num), float(_formula_general_d("m00", 2, 1, 1, 3))))
    # (ii) engine's Gamma reduction at eps = 0.3 (d = 3.4)
    e0 = sp.Rational(3, 10)
    vals = {eps: e0, G1p: sp.gamma(1 + e0), G1m: sp.gamma(1 - e0), G2p: sp.gamma(1 + 2 * e0), G2m: sp.gamma(1 - 2 * e0)}
    for (a, b, c) in ((1, 1, 1), (2, 1, 1), (1, 2, -1), (3, 1, 2), (2, 2, 0)):
        out.append((f"I({a},{b},{c}) eps=0.3", float(master_mm0(a, b, c).subs(vals)), float(_formula_general_d("mm0", a, b, c, 4 - 2 * 0.3))))
    for (a, b, c) in ((1, 1, 1), (2, 1, 1), (3, 1, 2), (2, 2, 1)):
        out.append((f"J({a};{b},{c}) eps=0.3", float(master_m00(a, b, c).subs(vals)), float(_formula_general_d("m00", a, b, c, 4 - 2 * 0.3))))
    # (iii) negative gluon power: (K-L)^2 = K^2 + L^2 - 2K.L, K.L averages to 0 -> products of tadpoles
    direct = tad(1, -1) * tad(2, 0) + tad(1, 0) * tad(2, -1)
    out.append(("I(1,2,-1) vs tadpoles", float(master_mm0(1, 2, -1).subs(vals)), float(direct.subs(vals))))
    return out


def gauge_xi_terms():
    """(1 - xi) part of R + S1 + S2 for each correlator, exact in eps (must vanish)."""
    return {pr: sp.simplify(laurent(sum(_diag(kd, pr[0], pr[1], "long") for kd in ("R", "S1", "S2")), 1))
            for pr in ((1, 1), (1, -1), (1, 0))}


if __name__ == "__main__":
    print("one loop: X^(1) = (N_C/16pi^2) m^2 *", oneloop_value(), "  Ward route:", sp.simplify(laurent(x_ward(1), 1)))
    print("Delta rho_0(172, GF, 3) =", delta_rho_oneloop(172.0, 1.1663788e-5, 3))
    print("mass relation: Sigma(m)/m =", laurent(sigma_onshell(), 1), "   dm_MS/m =", dm_hat("msbar"))
    print("Ward identity at two loops, L_V(m,m)(0) =", sp.simplify(laurent(correlator(1, 1, 2, "pole"), 1)))
    for sch in ("pole", "msbar"):
        print(f"main route   c/C_F [{sch}] =", coeff_unit(sch))
    shift = sp.simplify(coeff_unit("msbar") - coeff_unit("pole"))
    print("scheme shift (c_MS - c_pole)/C_F =", shift, "  [(m_pole^2/mbar^2 - 1)/(C_F alpha_s/pi) = 2*finite(Sigma)/m/4:",
          sp.expand(2 * (laurent(sigma_onshell(), 1) - laurent(sigma_onshell(), 0)) / 4), "]")
    print("gauge (1-xi) terms of R+S1+S2:", gauge_xi_terms())
    for row in check_masters_numerically():
        print("master check (case, numeric-or-engine value, general-d formula):", row)
    for sch in ("pole", "msbar"):
        x2w = sp.expand(laurent(x_ward(2, sch), 1))
        print(f"second route (Ward identity / scalar correlator) [{sch}]: 1/eps, 1/eps^2 coefficients",
              [sp.simplify(x2w.coeff(eps, -n)) for n in (1, 2)], " c/C_F =",
              sp.nsimplify(sp.simplify(x2w.coeff(eps, 0) / (4 * oneloop_value()))), "   main route:", coeff_unit(sch))
    print("qcd_coeff pole, C_F=4/3:", qcd_coeff("pole", 4 / 3, 1.0), " msbar mu=m:", qcd_coeff("msbar", 4 / 3, 1.0))
