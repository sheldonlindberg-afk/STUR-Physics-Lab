"""O(alpha_s) QCD correction to Delta rho of the (t, b = massless) doublet, derived from scratch.

Pipeline (see DERIVATION.md):
  * Delta rho = sqrt2 G_F [Pi_V(m,0) - Pi_V(m,-m)/4]   (q = 0 transverse current correlators, eq. 2.2)
  * Pi_V at one and two loops from Feynman rules: a d-dimensional Dirac-trace engine, reduction of the
    numerators to scalar two-loop vacuum integrals with lines (m,m,0) and (m,0,0), closed Gamma-function
    forms for those, exact in d = 4 - 2 eps
  * top-mass renormalization from the one-loop self-energy on shell (pole) or its 1/eps pole (MS-bar)
  * eps expansion with sympy; the finite remainder divided by the one-loop term gives c.
A general covariant gauge parameter xi is carried; the result must not depend on it.
"""
import math
from functools import lru_cache

import sympy as sp

EPS = sp.Symbol("eps")
XI = sp.Symbol("xi")
LMU = sp.Symbol("Lmu")            # ln(mu^2/m^2), m = the renormalized top mass of the chosen scheme
D = 4 - 2 * EPS


# ---------------------------------------------------------------- Dirac algebra in d dimensions
# A gamma string is a tuple of elements: a vector name ('k', 'l', 'p') stands for its slash, a name starting
# with '_' stands for gamma^index. A "spinor polynomial" is a list of (coefficient, string).

def _dot(a, b):
    a, b = sorted((a, b))
    return sp.Symbol(f"{a}{b}")


def _mul(*factors):
    out = [(sp.Integer(1), ())]
    for f in factors:
        out = [(c1 * c2, s1 + s2) for c1, s1 in out for c2, s2 in f]
    return out


def _sandwich(S):
    """gamma^a S gamma_a for a string S without the index a:  g^a S' x g_a = 2 x S' - (g^a S' g_a) x."""
    if not S:
        return [(D, ())]
    head, x = S[:-1], S[-1]
    res = [(sp.Integer(2), (x,) + head)]
    res += [(-c, s + (x,)) for c, s in _sandwich(head)]
    return res


def _eliminate(c, s):
    """Remove every contracted index pair from a string (all indices here are contracted inside the trace)."""
    for i, e in enumerate(s):
        if e.startswith("_"):
            j = s.index(e, i + 1)
            out = []
            for c2, mid in _sandwich(s[i + 1:j]):
                out += _eliminate(c * c2, s[:i] + mid + s[j + 1:])
            return out
    return [(c, s)]


@lru_cache(maxsize=None)
def _trace(s):
    """Tr of a product of slashed vectors, normalized Tr 1 = 4 (cancels in every ratio used)."""
    if len(s) % 2:
        return sp.Integer(0)
    if not s:
        return sp.Integer(4)
    a, rest = s[0], s[1:]
    tot = sp.Integer(0)
    for j, b in enumerate(rest):
        tot += (-1) ** j * _dot(a, b) * _trace(rest[:j] + rest[j + 1:])
    return sp.expand(tot)


def _tr(poly):
    tot = sp.Integer(0)
    for c, s in poly:
        if c == 0:
            continue
        for c2, s2 in _eliminate(c, s):
            tot += c2 * _trace(s2)
    return sp.expand(tot)


def _slash(**coef):
    return [(sp.Integer(v), (k,)) for k, v in coef.items() if v]


def _N(p, m):
    """numerator of the quark propagator, pslash + m."""
    return [(sp.Integer(1), (p,))] + ([(sp.sympify(m), ())] if m != 0 else [])


def _G(name):
    return [(sp.Integer(1), (name,))]


# ---------------------------------------------------------------- scalar integrals (Euclidean, measure d^dk/pi^{d/2})

@lru_cache(maxsize=None)
def _G1(c):
    """symbol standing for Gamma(1 + c eps); expanded in eps only at the very end."""
    return sp.Symbol(f"G[{c}]")


def _gam(z):
    """Gamma(n + c eps) = Gamma(1 + c eps) x rational(eps), n integer (exact recursion Gamma(z+1) = z Gamma(z))."""
    z = sp.expand(sp.sympify(z))
    c = z.coeff(EPS, 1)
    n = z - c * EPS
    assert n.is_integer, z
    if c == 0:
        assert n >= 1, z
        return sp.factorial(n - 1)
    x = c * EPS
    if n >= 1:
        return sp.Mul(*[(j + x) for j in range(1, int(n))]) * _G1(c)
    return _G1(c) / sp.Mul(*[(j + x) for j in range(int(n), 1)])


def _rgamma(z):
    """1/Gamma(z), exactly 0 at non-positive integers (scaleless / vanishing integrals)."""
    z = sp.expand(sp.sympify(z))
    if z.is_integer and z <= 0:
        return sp.Integer(0)
    return 1 / _gam(z)


def J_m00(a, b, c):
    """\\int\\int 1/[(k^2+1)^a (l^2)^b ((k-l)^2)^c]."""
    return (_gam(a + b + c - D) * _gam(D / 2 - b) * _gam(D / 2 - c) * _gam(b + c - D / 2)
            * _rgamma(a) * _rgamma(b) * _rgamma(c) / _gam(D / 2))


def J_mm0(a, b, c):
    """\\int\\int 1/[(k^2+1)^a (l^2+1)^b ((k-l)^2)^c]."""
    if a <= 0 or b <= 0:
        return sp.Integer(0)
    return (_gam(a + c - D / 2) * _gam(b + c - D / 2) * _gam(D / 2 - c) * _gam(a + b + c - D)
            * _rgamma(a) * _rgamma(b) / _gam(D / 2) * _rgamma(a + b + 2 * c - D))


def T1(a):
    """one-loop tadpole \\int 1/(k^2+1)^a."""
    return _gam(a - D / 2) * _rgamma(a)


def O1(a, b):
    """on-shell \\int 1/[(k^2+1)^a ((k-p)^2)^b], p_E^2 = -1."""
    return _gam(a + b - D / 2) * _gam(D - a - 2 * b) * _rgamma(a) * _rgamma(D - a - b)


@lru_cache(maxsize=None)
def _pf(e, a):
    """1/(K^e (K+1)^a) as {(M2, n): coef} meaning sum coef (K+M2)^(-n); e, a may be <= 0 in one slot."""
    if a <= 0:
        # K^-e (K+1)^|a|
        n = -a
        if e <= 0:   # polynomial K^|e| (K+1)^n  -> expand (K+1)^n in powers of K: massless lines with negative index
            return {(0, e - j): sp.binomial(n, j) for j in range(n + 1)}
        return {(0, e - j): sp.binomial(n, j) for j in range(n + 1)}
    if e <= 0:
        # K^|e| / (K+1)^a, K = (K+1) - 1
        n = -e
        return {(1, a - j): sp.binomial(n, j) * (-1) ** (n - j) for j in range(n + 1)}
    out = {}
    for key, v in _pf(e, a - 1).items():
        out[key] = out.get(key, 0) + v
    for key, v in _pf(e - 1, a).items():
        out[key] = out.get(key, 0) - v
    return {k: v for k, v in out.items() if v != 0}


def _line(p, dens):
    """K^p / prod (K + M2)^n for dens = {M2: n}, M2 in {0, 1}."""
    e = dens.get(0, 0) - p
    a = dens.get(1, 0)
    return _pf(e, a)


def _two_loop_scalar(kform, lform, nq):
    tot = sp.Integer(0)
    for (Mk, nk), ck in kform.items():
        for (Ml, nl), cl in lform.items():
            if Mk == 1 and Ml == 1:
                v = J_mm0(nk, nl, nq)
            elif Mk == 1:
                v = J_m00(nk, nl, nq)
            elif Ml == 1:
                v = J_m00(nl, nk, nq)
            else:
                v = 0
            tot += ck * cl * v
    return tot


K, L, Q = sp.symbols("K L Q")


def _euclid_two(num):
    """Minkowski dot products -> Euclidean squares: k.k = -K, l.l = -L, k.l = -(K+L-Q)/2."""
    return sp.expand(num.subs({_dot("k", "k"): -K, _dot("l", "l"): -L, _dot("k", "l"): -(K + L - Q) / 2}))


def _reduce_two(num, kd, ld, qd):
    """\\int\\int num(K,L,Q) / [prod_k (K+M2)^n  prod_l (L+M2)^n  Q^qd] -> Gamma functions."""
    poly = sp.Poly(num, K, L, Q)
    tot = sp.Integer(0)
    for (pk, pl, pq), coef in poly.terms():
        tot += coef * _two_loop_scalar(_line(pk, kd), _line(pl, ld), qd - pq)
    return tot


def _dens(*pairs):
    out = {}
    for m2, n in pairs:
        out[m2] = out.get(m2, 0) + n
    return out


def _gluon(left, middle, right):
    """returns [(weight, poly), ...] implementing gamma^a X gamma_a + (1-xi) qslash X qslash / Q,
    where the extra 1/Q is signalled by weight power 1."""
    feyn = _mul(left, _G("_a"), middle, _G("_a"), right)
    q = _slash(k=1, l=-1)
    gauge = _mul(left, q, middle, q, right)
    return [(0, sp.Integer(1), feyn), (1, 1 - XI, gauge)]


@lru_cache(maxsize=None)
def pi_v_two_loop(m1, m2):
    """Two-loop Pi_V(m1, m2)(0) in units g0^2 C_F N_C / (4 pi)^d, m_i in {0, +-1}. Includes 1/d of Pi_T."""
    s1, s2 = m1 * m1, m2 * m2
    mu, al = _G("_mu"), _G("_al")
    tot = sp.Integer(0)
    # SE on line 1:  Tr[g^mu N2(k) g_mu N1(k) g^a N1(l) g_a N1(k)]
    for extra, w, poly in _gluon(_mul(mu, _N("k", m2), mu, _N("k", m1)), _N("l", m1), _N("k", m1)):
        num = _euclid_two(_tr(poly))
        tot += w * _reduce_two(num, _dens((s2, 1), (s1, 2)), _dens((s1, 1)), 1 + extra)
    # SE on line 2:  Tr[g^mu N2(k) g^a N2(l) g_a N2(k) g_mu N1(k)]
    for extra, w, poly in _gluon(_mul(mu, _N("k", m2)), _N("l", m2), _mul(_N("k", m2), mu, _N("k", m1))):
        num = _euclid_two(_tr(poly))
        tot += w * _reduce_two(num, _dens((s2, 2), (s1, 1)), _dens((s2, 1)), 1 + extra)
    # vertex:  Tr[g^mu N2(k) g^a N2(l) g_mu N1(l) g_a N1(k)]
    for extra, w, poly in _gluon(_mul(mu, _N("k", m2)), _mul(_N("l", m2), mu, _N("l", m1)), _N("k", m1)):
        num = _euclid_two(_tr(poly))
        tot += w * _reduce_two(num, _dens((s2, 1), (s1, 1)), _dens((s2, 1), (s1, 1)), 1 + extra)
    return tot / D   # prefactor +g^2 C_F N_C (section 3)


@lru_cache(maxsize=None)
def pi_v_one_loop(m1, m2):
    """One-loop Pi_V(m1, m2)(0) in units N_C/(4 pi)^{d/2}: -Tr[g^mu N2 g_mu N1]/(d D1 D2)."""
    num = _tr(_mul(_G("_mu"), _N("k", m2), _G("_mu"), _N("k", m1)))
    num = sp.expand(num.subs({_dot("k", "k"): -K}))
    tot = sp.Integer(0)
    for (pk,), coef in sp.Poly(num, K).terms():
        for (M, n), c in _line(pk, _dens((m1 * m1, 1), (m2 * m2, 1))).items():
            tot += coef * c * (T1(n) if M == 1 else 0)
    return -tot / D


@lru_cache(maxsize=None)
def sigma_onshell():
    """Sigma(pslash = m)/m for m = 1 in units g0^2 C_F/(4 pi)^{d/2}, from Tr[(pslash+m) Sigma]/(4 m)."""
    q = _slash(p=1, k=-1)
    proj = _mul(_N("p", 1))
    feyn = _tr(_mul(proj, _G("_a"), _N("k", 1), _G("_a")))
    gauge = _tr(_mul(proj, q, _N("k", 1), q))
    # Euclidean: p.p = -P = +1 (on shell P = -1), k.k = -K, k.p = -(K + P - Q)/2 with Q = (k-p)^2
    sub = {_dot("p", "p"): 1, _dot("k", "k"): -K, _dot("k", "p"): -(K - 1 - Q) / 2}
    tot = sp.Integer(0)
    for w, num, qd in ((1, feyn, 1), (1 - XI, gauge, 2)):
        num = sp.expand(num.subs(sub))
        for (pk, pq), coef in sp.Poly(num, K, Q).terms():
            for (M, n), c in _line(pk, {1: 1}).items():
                tot += w * coef * c * (O1(n, qd - pq) if M == 1 else 0)
    return tot / 4


EX = sp.Symbol("EX")              # stands for e^{gamma eps} (mu^2/m^2)^eps, the MS-bar coupling factor


@lru_cache(maxsize=None)
def _taylor_factor(name, order):
    """Taylor coefficients [a_0..a_order] of Gamma(1 + c eps) or of EX = exp(eps (gamma + Lmu))."""
    if name == "EX":
        arg = EPS * (sp.EulerGamma + LMU)
    else:
        x = int(sp.Rational(name[2:-1])) * EPS     # Gamma(1+x) = exp(-gamma x + sum_k zeta(k) (-x)^k / k)
        arg = -sp.EulerGamma * x + sum(sp.zeta(k) * (-x) ** k / k for k in range(2, order + 1))
    ser = sp.expand(sp.series(sp.exp(arg), EPS, 0, order + 1).removeO())
    return tuple(sp.expand(ser.coeff(EPS, k)) for k in range(order + 1))


def _series0(expr, order=1, depth=6):
    """Laurent expansion in eps, terms eps^n with n < order. expr is a polynomial in the symbols G[c], EX with
    coefficients rational in eps; each rational coefficient is expanded once, the factors by their Taylor series."""
    expr = sp.expand(expr)
    syms = sorted((x for x in expr.free_symbols if x.name.startswith("G[") or x.name == "EX"), key=lambda x: x.name)
    terms = sp.Poly(expr, *syms).terms() if syms else [((), expr)]
    tot = sp.Integer(0)
    for powers, coef in terms:
        coef = sp.cancel(sp.together(coef))
        num, den = sp.fraction(coef)
        low = 0
        while den.subs(EPS, 0) == 0:
            den = sp.cancel(den / EPS)
            low += 1
        # coef = eps^-low num/den, den(0) != 0; need eps^n, n < order -> Taylor to order + low - 1
        n_need = order + low
        rat = sp.expand(sp.series(num / den, EPS, 0, n_need).removeO()) if n_need > 0 else sp.Integer(0)
        prod = [sp.expand(rat.coeff(EPS, k)) for k in range(max(n_need, 0))]
        for x, pw in zip(syms, powers):
            t = _taylor_factor(x.name, depth)
            for _ in range(pw):
                prod = [sp.expand(sum(prod[i] * t[k - i] for i in range(k + 1) if k - i < len(t))) for k in range(len(prod))]
        tot += sum(prod[k] * EPS ** (k - low) for k in range(len(prod)))
    return sp.expand(tot)


@lru_cache(maxsize=None)
def _assembled(xi_value=1):
    """Returns (leading, c_pole, c_msbar(Lmu)) with c in units C_F alpha_s/pi.

    leading: lim Delta rho^(1) / (sqrt2 G_F m^2 N_C/(4 pi)^2).
    """
    sub = {XI: xi_value}
    # combination (2.2): Pi_V(m,0) - Pi_V(m,-m)/4
    P1 = pi_v_one_loop(1, 0) - pi_v_one_loop(1, -1) / 4
    P2 = (pi_v_two_loop(1, 0) - pi_v_two_loop(1, -1) / 4).subs(sub)
    S = sigma_onshell().subs(sub)
    # units: Pi^(1) = N_C/(4pi)^{d/2} P1 ;  Pi^(2) = N_C/(4pi)^{d/2} (alpha_s/4pi) e^{gamma eps} mu^{2eps} C_F P2
    #        sigma = (alpha_s/4pi) C_F e^{gamma eps} mu^{2eps} S  (pole) ; m d/dm Pi^(1) = (2-2eps) Pi^(1)
    E = EX
    lead = _series0(P1, 1).subs(EPS, 0)
    pole_expr = E * (P2 - S * (2 - 2 * EPS) * P1)
    ser_pole = sp.expand(_series0(pole_expr, 1))
    s_m1 = sp.expand(_series0(EPS * S * E, 1)).subs(EPS, 0)          # residue of the on-shell self-energy
    ms_expr = E * P2 - (s_m1 / EPS) * (2 - 2 * EPS) * P1
    ser_ms = sp.expand(_series0(ms_expr, 1))
    out = {}
    for name, ser in (("pole", ser_pole), ("msbar", ser_ms)):
        poles = [sp.simplify(ser.coeff(EPS, -k)) for k in (1, 2, 3)]
        fin = sp.expand(ser.coeff(EPS, 0))
        # Delta rho = Delta rho_0 [1 + (alpha_s/4pi) C_F fin/lead]  ->  c / C_F = fin/(4 lead)
        out[name] = (None, poles, sp.expand(fin / (4 * lead)))
    return lead, out, s_m1, ser_pole, ser_ms


@lru_cache(maxsize=None)
def _numbers():
    lead, out, s_m1, _, _ = _assembled(1)
    cp = sp.expand(out["pole"][2])
    cm = sp.expand(out["msbar"][2])
    return float(lead), float(cp.subs(LMU, 0)), float(cm.coeff(LMU, 0)), float(cm.coeff(LMU, 1))


# ---------------------------------------------------------------- exports

def delta_rho_oneloop(m, GF, NC):
    """Delta rho_0 = sqrt2 G_F N_C m^2 lead/(16 pi^2) (derived; lead from the one-loop trace + tadpoles)."""
    lead = _numbers()[0]
    return math.sqrt(2) * GF * NC * m * m * lead / (16 * math.pi ** 2)


def qcd_coeff(scheme, CF, mu_over_m):
    _, cpole, cms0, cms1 = _numbers()
    if scheme == "pole":
        return CF * cpole
    if scheme == "msbar":
        return CF * (cms0 + cms1 * math.log(mu_over_m ** 2))
    raise ValueError(f"unknown scheme {scheme!r}")


def delta_rho_qcd(m, GF, NC, CF, alphas, scheme, mu_over_m):
    return delta_rho_oneloop(m, GF, NC) * (1 + qcd_coeff(scheme, CF, mu_over_m) * alphas / math.pi)


PROVENANCE = {
    "delta_rho_oneloop": ("derived", "q=0 current correlators, d-dim trace + tadpoles, eq. (2.2)"),
    "qcd_coeff": ("derived", "two-loop vacuum diagrams (m,m,0),(m,0,0) in closed Gamma form + on-shell/MSbar mass CT"),
    "delta_rho_qcd": ("derived", "Delta rho_0 (1 + c alpha_s/pi)"),
}


def _second_route():
    """Independent checks (DERIVATION section 8)."""
    res = {}
    # 1. general covariant gauge: keep xi symbolic all the way
    lead, out, s_m1, ser_pole, ser_ms = _assembled(XI)
    res["c_pole/C_F, xi symbolic"] = out["pole"][2]
    res["c_MSbar/C_F, xi symbolic"] = out["msbar"][2]
    res["poles (xi symbolic)"] = out["pole"][1] + out["msbar"][1]
    res["Sigma_OS finite part (xi symbolic)"] = sp.expand(_series0(EX * sigma_onshell(), 1).coeff(EPS, 0))
    # 2. vector Ward identity at two loops, bare, any xi, exact in d
    res["Pi_V^(2)(m,m) through eps^1"] = _series0(pi_v_two_loop(1, 1), 2)
    # 3. mu independence of the pole coefficient
    res["d c_pole/d Lmu"] = sp.diff(out["pole"][2], LMU)
    # 4. RG: d c_MSbar / d ln mu^2 vs 2 x (Z_m residue)/4 (units alpha_s/pi)
    res["d c_MSbar/d Lmu  vs  2*s_-1/4"] = (sp.diff(out["msbar"][2], LMU), 2 * s_m1 / 4)
    # 5. scheme shift = m_pole^2/mbar^2 - 1 at O(alpha_s): 2 x finite part of Sigma_OS/m (units alpha_s/pi)
    fin = sp.expand(_series0(EX * sigma_onshell(), 1).coeff(EPS, 0)).subs(XI, 1)
    res["(c_MSbar - c_pole)/C_F  vs  2*finite(Sigma_OS)/4"] = (sp.expand(out["msbar"][2] - out["pole"][2]), sp.expand(2 * fin / 4))
    # 6. master integral J_mm0(2,2,1) at d = 4 by direct 2D quadrature (angular average 1/(k-l)^2 -> 1/max)
    from scipy import integrate
    # symmetric in K <-> L: 2 x region K < L, where max(K, L) = L
    f = lambda K, L: 2 * K / ((K + 1) ** 2 * (L + 1) ** 2)
    numv = integrate.dblquad(f, 0, math.inf, 0, lambda L: L)[0]
    G = math.gamma
    res["J_mm0(2,2,1), d=4: quadrature vs Gamma formula"] = (numv, G(1) ** 4 / (G(2) ** 3 * G(2)))
    return res


if __name__ == "__main__":
    lead, out, s_m1, ser_pole, ser_ms = _assembled(1)
    print("MAIN ROUTE (Feynman gauge)")
    print("  one-loop lead (units sqrt2 GF NC m^2/16pi^2):", lead)
    print("  Z_m residue s_-1 (Sigma_OS/m = alpha_s/4pi C_F (s_-1/eps + ...)):", s_m1)
    for k, v in out.items():
        print(" ", k, "poles 1/eps,1/eps^2,1/eps^3:", v[1], " c/C_F =", v[2], "=", sp.N(v[2].subs(LMU, 0)))
    print("  c_pole(C_F=4/3) =", qcd_coeff("pole", sp.Rational(4, 3), 1.0),
          " c_MSbar(C_F=4/3, mu=mbar) =", qcd_coeff("msbar", 4 / 3, 1.0))
    print("SECOND ROUTE (general gauge xi, Ward identity, RG, scheme shift, master-integral quadrature)")
    for k, v in _second_route().items():
        print(" ", k, ":", v)
