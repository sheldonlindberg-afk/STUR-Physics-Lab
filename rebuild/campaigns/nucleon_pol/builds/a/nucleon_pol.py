"""Nucleon electric and magnetic polarizabilities from the pion cloud, O(p^3) heavy-baryon ChPT.

Route A (exports): the static-source one-loop self-energy in plane-wave static external fields, diagram by diagram
(KR-KR, KR-insertion, seagull, double insertion), expanded to O(q q') with exact isotropic angular averages and
dimensionally regularized radial integrals in n = d-1 spatial dimensions, evaluated at n = 3 (see DERIVATION.md).
The Born (nucleon-line) diagrams cannot produce the q.q' structures and are excluded by reading off only those.

Routes B (position-space uniform-field gauges) and C (Baldin sum rule over tree-level photoproduction) run under
__main__ as independent checks.
"""
import math
from functools import lru_cache

import sympy as sp

HBARC = 197.3269804  # MeV fm (SPEC)

# ---------------------------------------------------------------- symbolic loop machinery (route A)
_p = sp.symbols("p1:4")
_s, _t, _u, _m, _n = sp.symbols("s t u m n", positive=True)
_P = sp.Matrix(_p)
_X = sp.Matrix([1, 0, 0])
_Y = sp.Matrix([0, 1, 0])


def _dot(a, b):
    return sum(a[i] * b[i] for i in range(3))


def _G(K):
    """Static pion propagator 1/((p+K)^2+m^2) to second order in the external momentum K; _u = 1/(p^2+m^2)."""
    x = 2 * _dot(_P, K) + _dot(K, K)
    return _u - x * _u**2 + x**2 * _u**3


def _st(expr):
    """Coefficient of s^1 t^1 (one power of each photon momentum)."""
    e = sp.expand(expr)
    return sp.expand(e.coeff(_s, 1).coeff(_t, 1))


def _loop(expr):
    """int d^n p/(2pi)^n of a polynomial in p_i and u = 1/(p^2+m^2): isotropic average in n dims, then the closed
    dim-reg radial formula; returned at n = 3 (Gamma functions at half-integers: finite)."""
    expr = sp.expand(expr)
    if expr == 0:
        return sp.Integer(0)
    tot = 0
    for (a, b, c, N), co in sp.Poly(expr, *_p, _u).terms():
        if a % 2 or b % 2 or c % 2:
            continue
        k = (a + b + c) // 2
        ang = sp.factorial2(a - 1) * sp.factorial2(b - 1) * sp.factorial2(c - 1) / sp.prod([_n + 2 * j for j in range(k)])
        rad = (sp.gamma(k + _n / 2) * sp.gamma(N - k - _n / 2) / (sp.gamma(_n / 2) * sp.gamma(N))
               * _m**(_n + 2 * k - 2 * N) / (4 * sp.pi)**(_n / 2))
        tot += co * ang * rad
    return sp.simplify(tot.subs(_n, 3))


# Diagrams for D[A] = sum_i <0| Pi_i K^-1 Pi_i |0>, per e^2, bilinear in photon 1 (q,a) and photon 2 (q',a').
def _T1(q, a, qp, ap):     # KR - KR (both photons at the nucleon vertex); no momentum dependence
    return 2 * _dot(a, ap) * _u


def _T2(q, a, qp, ap):     # KR at origin + one pi-pi-gamma insertion on the pion line (both orderings, both photons)
    def one(akr, qi, ai):
        return (-2 * _dot(akr, _P) * _dot(ai, _P) * _G(qi) * _u
                - 2 * _dot(akr, _P + qi) * _dot(ai, _P) * _G(qi) * _u)
    return one(a, qp, ap) + one(ap, q, a)


def _T3(q, a, qp, ap):     # gamma gamma pi pi seagull (transverse photons)
    Q = q + qp
    return -2 * _dot(a, ap) * _dot(_P + Q, _P) * _G(Q) * _u


def _T4(q, a, qp, ap):     # two pi-pi-gamma insertions, vertex -2e a.k for transverse a
    Q = q + qp

    def f(q, a, qp, ap):
        return 4 * _dot(_P + Q, _P) * _dot(a, _P + qp) * _dot(ap, _P) * _G(Q) * _G(qp) * _u
    return f(q, a, qp, ap) + f(qp, ap, q, a)


def _TE(q, qp):            # Coulomb (A_0) photons: seagull -e^2 A_0^2 in K, i.e. +2 e^2 phi1 phi2 Sigma(q+q')
    Q = q + qp
    return 2 * _dot(_P + Q, _P) * _G(Q) * _u


@lru_cache(maxsize=None)
def loop_coefficients():
    """Return (d_E, d_B, gauge_check) per e^2, as sympy expressions in m (pion mass).
    D contains e^2 d_E (q.q') phi1 phi2 and e^2 d_B [(q.q')(a.a') - (q.a')(q'.a)]."""
    dE = _loop(_st(_TE(_s * _X, _t * _X)))
    diags = (_T1, _T2, _T3, _T4)
    # configuration 1: q = s X, q' = t X, a = a' = Y  -> picks (q.q')(a.a')
    c1 = sum(_loop(_st(T(_s * _X, _Y, _t * _X, _Y))) for T in diags)
    # configuration 2: q = s X, a = Y, q' = t Y, a' = X  -> picks (q.a')(q'.a)
    c2 = sum(_loop(_st(T(_s * _X, _Y, _t * _Y, _X))) for T in diags)
    return dE, c1, sp.simplify(c1 + c2)


@lru_cache(maxsize=None)
def _unit_coefficients():
    """d_E, d_B at m = 1 (they scale as 1/m: m^(n-4) at n = 3)."""
    dE, dB, chk = loop_coefficients()
    if chk != 0:
        raise ArithmeticError("magnetic loop amplitude is not gauge invariant")
    return float(dE.subs(_m, 1)), float(dB.subs(_m, 1))


def _pol(d_unit, gA, fpi, mpi, alpha):
    e2 = 4 * math.pi * alpha
    # Delta E = -(gA^2/4f^2) D,  D ⊃ e^2 d (structure),  -2 pi pol B^2 ⊃ 4 pi pol (structure)
    return -gA**2 * e2 * (d_unit / mpi) / (16 * math.pi * fpi**2)


def alpha_E(gA, fpi, mpi, alpha):
    return _pol(_unit_coefficients()[0], gA, fpi, mpi, alpha)


def beta_M(gA, fpi, mpi, alpha):
    return _pol(_unit_coefficients()[1], gA, fpi, mpi, alpha)


def to_fm3(x):
    return x * HBARC**3


PROVENANCE = {
    "alpha_E": ("derived", "HB static one-loop self-energy in a Coulomb field; q.q' term of the pi pi gamma gamma seagull loop, dim reg n=3 (DERIVATION 3.1)"),
    "beta_M": ("derived", "same, transverse static field: seagull + double pi pi gamma insertion (+KR, which drop), gauge-checked (DERIVATION 3.2)"),
    "to_fm3": ("input", "(hbar c)^3 with hbar c = 197.3269804 MeV fm from SPEC"),
}


# ---------------------------------------------------------------- independent routes
def route_B(gA, fpi, mpi, alpha):
    """Position space, uniform-field gauges A0 = -E.y, A = B x y / 2 (no KR, no Born). Radial integrals by quadrature."""
    from scipy.integrate import quad
    e2 = 4 * math.pi * alpha
    g = lambda r: (1 + mpi * r) * math.exp(-mpi * r) / (4 * math.pi * r**2)
    I = quad(lambda r: 4 * math.pi * r**4 * g(r)**2, 0, math.inf, epsabs=0, epsrel=1e-13)[0]
    K1 = quad(lambda p: 4 * math.pi * p**2 * (p**2 / 3) / (p**2 + mpi**2)**3, 0, math.inf, epsabs=0, epsrel=1e-13)[0] / (2 * math.pi)**3
    DE = e2 * I / 3                 # D = DE * E^2
    DB = -e2 * I / 6 + 2 * e2 * K1  # diamagnetic + paramagnetic (Tr_{l=1} L_k L_l = 2 delta_kl)
    c = gA**2 / (4 * fpi**2) / (2 * math.pi)
    return c * DE, c * DB


def route_C(gA, fpi, mpi, alpha):
    """alpha_E + beta_M from the Baldin sum rule with the LO static gamma p -> pi+ n cross section (KR + pion pole)."""
    from scipy.integrate import quad
    e2 = 4 * math.pi * alpha
    pref = e2 * gA**2 / (2 * fpi**2)

    def sigma(w):
        q = math.sqrt(w * w - mpi * mpi)

        def dsig(c):
            C = -1 / (w * (w - q * c))
            X = q * q * (1 - c * c) / 2
            M2 = pref * (1 + 2 * C * X + C * C * X * (q * q + w * w - 2 * q * w * c))
            return 2 * math.pi * (q / w) * M2 / (16 * math.pi**2)
        return quad(dsig, -1, 1, epsabs=0, epsrel=1e-13)[0]
    return quad(lambda w: sigma(w) / w**2, mpi, math.inf, epsabs=0, epsrel=1e-11, limit=400)[0] / (2 * math.pi**2)


if __name__ == "__main__":
    gA, fpi, mpi, alpha = 1.27, 92.4, 139.57, 1 / 137.035999
    dE, dB, chk = loop_coefficients()
    print("route A loop coefficients (per e^2): d_E =", dE, " d_B =", dB, " gauge check (should be 0):", chk)
    a, b = alpha_E(gA, fpi, mpi, alpha), beta_M(gA, fpi, mpi, alpha)
    print(f"route A: alpha_E = {a:.10e} MeV^-3 = {to_fm3(a):.6e} fm^3 ; beta_M = {b:.10e} MeV^-3 = {to_fm3(b):.6e} fm^3 ; beta/alpha = {b / a:.12f}")
    aB, bB = route_B(gA, fpi, mpi, alpha)
    print(f"route B: alpha_E = {aB:.10e} ; beta_M = {bB:.10e} ; rel. diff {aB / a - 1:.1e}, {bB / b - 1:.1e}")
    sC = route_C(gA, fpi, mpi, alpha)
    print(f"route C (Baldin): alpha_E + beta_M = {sC:.10e} vs route A {a + b:.10e} ; rel. diff {sC / (a + b) - 1:.1e}")
