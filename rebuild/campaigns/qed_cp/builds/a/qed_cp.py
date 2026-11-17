"""Casimir-Polder energy from fourth-order RS perturbation theory (12 two-photon exchange diagrams).

See DERIVATION.md. Main chain: eq.(1) double photon integral -> identity (2) for the 12 energy denominators
-> photon k-integrals done in closed form (sec. 4) -> eq.(3), a single positive u-integral.
"""
import itertools
import math

import numpy as np
import sympy as sp
from scipy.integrate import quad

# polynomial p(x) = sum c_n x^n from Tr[M(u)^2] (DERIVATION sec. 4); obtained symbolically below, not typed in.


def _p_coeffs():
    """Derive p(x) from M = A delta + B rr: r^2 A = -(x^2+x+1), r^2 B = x^2+3x+3, Tr M^2 ~ 3A^2+2AB+B^2."""
    x, r, u = sp.symbols('x r u', positive=True)
    f = sp.exp(-u * r) / r
    fp, fpp = sp.diff(f, r), sp.diff(f, r, 2)
    lap = sp.simplify(fpp + 2 * fp / r)                # = u^2 f
    A = sp.simplify(-lap + fp / r)                      # coefficient of delta_ij (times 2/pi)
    B = sp.simplify(fpp - fp / r)                       # coefficient of rhat_i rhat_j
    tr = sp.simplify((3 * A**2 + 2 * A * B + B**2) / (f**2) * r**4)   # 2 p(ur)
    poly = sp.Poly(sp.expand(tr.subs(u, x / r) / 2), x)
    return [float(c) for c in reversed(poly.all_coeffs())]   # c_0, c_1, ...


_C = _p_coeffs()


def _p(x):
    return sum(c * x**n for n, c in enumerate(_C))


def _J(rho):
    """J(rho) = int_0^inf dt e^{-2 rho t} p(rho t)/(1+t^2)^2;  U = -(alpha0^2 w0 / pi r^6) J(rho)."""
    opts = dict(epsabs=1e-15, epsrel=1e-13, limit=400)   # J is O(0.1-1); absolute floor 1e-15
    if rho >= 1.0:   # s = rho t form
        g = lambda s: math.exp(-2 * s) * _p(s) / (1 + (s / rho)**2)**2
        pts = [0.0, 1.0, 5.0, 20.0, 60.0]
        val = sum(quad(g, lo, hi, **opts)[0] for lo, hi in zip(pts, pts[1:]))
        val += quad(g, pts[-1], np.inf, **opts)[0]
        return val / rho
    g = lambda t: math.exp(-2 * rho * t) * _p(rho * t) / (1 + t * t)**2
    T = 1.0 / rho
    pts = [0.0, 1.0, 10.0] + ([T, 20 * T] if T > 10 else [])
    pts = sorted(set(pts))
    val = sum(quad(g, lo, hi, **opts)[0] for lo, hi in zip(pts, pts[1:]))
    val += quad(g, pts[-1], np.inf, **opts)[0]
    return val


def cp_energy(r, w0, alpha0):
    """U(r) for two identical atoms, all separations (eq. 3 of DERIVATION.md)."""
    return -(alpha0**2 * w0 / (math.pi * r**6)) * _J(w0 * r)


def far_coefficient():
    """C: J -> (1/rho) int e^{-2s} p(s) ds = (1/rho) sum c_n n!/2^{n+1};  U -> -C alpha0^2/r^7, C = that / pi."""
    return sum(c * math.factorial(n) / 2**(n + 1) for n, c in enumerate(_C)) / math.pi


def near_coefficient():
    """D: J -> int_0^inf p(0)/(1+t^2)^2 dt;  U -> -D w0 alpha0^2/r^6."""
    t = sp.symbols('t', positive=True)
    return float(sp.integrate(sp.Float(_C[0]) / (1 + t**2)**2, (t, 0, sp.oo)) / sp.pi)


PROVENANCE = {
    "cp_energy": ("derived", "4th-order RS over 12 two-photon exchange diagrams; denominator identity (2) + closed-form "
                             "photon k-integrals -> 1D u-integral (DERIVATION secs 1-4)"),
    "far_coefficient": ("derived", "rho -> infinity limit of J(rho): sum c_n n!/2^{n+1}/pi (DERIVATION sec 5)"),
    "near_coefficient": ("derived", "rho -> 0 limit of J(rho): (1/pi) int 3/(1+t^2)^2; cross-checked by London route"),
}


# ---------------------------------------------------------------- second routes (DERIVATION sec. 6)

def _sigma12_symbolic():
    a, b, k, q = sp.symbols('a b k q', positive=True)
    ev = [('A', 'p'), ('A', 'q'), ('B', 'p'), ('B', 'q')]
    E, W = {'p': k, 'q': q}, {'A': a, 'B': b}
    tot, n = 0, 0
    for perm in itertools.permutations(ev):
        if perm.index(('A', 'p')) > perm.index(('A', 'q')):
            continue
        n += 1
        ex, ph, den = {'A': False, 'B': False}, {'p': False, 'q': False}, 1
        for at, pp in perm[:3]:
            ex[at] = not ex[at]
            ph[pp] = not ph[pp]
            den *= sum(W[z] for z in ex if ex[z]) + sum(E[z] for z in ph if ph[z])
        tot += 1 / den
    return n, (a, b, k, q), sp.factor(sp.together(tot))


def _check_identity():
    n, (a, b, k, q), S = _sigma12_symbolic()
    u = sp.symbols('u')
    integrand = a * b * k * q / ((a**2 + u**2) * (b**2 + u**2) * (k**2 + u**2) * (q**2 + u**2))
    res = sum(sp.residue(integrand, u, sp.I * z) for z in (a, b, k, q))
    rhs = sp.Rational(8) / sp.pi * (sp.pi * sp.I * res)      # int_0^inf = (1/2) 2 pi i sum Res
    return n, sp.simplify(sp.together(rhs - S)), S, (a, b, k, q)


def _U_double(r, eps, S, w0=1.0, alpha0=1.0):
    """Eq.(1) directly, Abel factor exp(-eps(k+q)), Gauss-Legendre grid."""
    d4 = alpha0**2 * w0**2 / 4
    kmax = 40 / eps
    xg, wg = np.polynomial.legendre.leggauss(8)
    edges = np.linspace(0, kmax, int(kmax * r) + 51)
    mid, half = (edges[:-1] + edges[1:]) / 2, (edges[1:] - edges[:-1]) / 2
    k = (mid[:, None] + half[:, None] * xg).ravel()
    w = (half[:, None] * wg).ravel()
    x = k * r
    s, c = np.sin(x), np.cos(x)
    P = s / x + c / x**2 - s / x**3
    Q = -s / x - 3 * c / x**2 + 3 * s / x**3
    f = k**3 * np.exp(-eps * k) * w
    tot = 0.0
    for i in range(0, len(k), 400):
        K = k[i:i + 400, None]
        T = 3 * P[i:i + 400, None] * P + P[i:i + 400, None] * Q + Q[i:i + 400, None] * P + Q[i:i + 400, None] * Q
        tot += np.sum(f[i:i + 400, None] * f * T * S(w0, w0, K, k[None, :]))
    return -d4 / math.pi**2 * tot


if __name__ == "__main__":
    n, diff, S, syms = _check_identity()
    print(f"number of time orderings: {n}; identity (2) residual: {diff}")
    Sf = sp.lambdify(syms, S, 'numpy')
    print("p(x) coefficients:", _C)
    print(f"far  C = {far_coefficient():.12f}   cp_energy*r^7 at r w0=1e5: {-cp_energy(1e5, 1, 1) * 1e35:.12f}")
    print(f"near D = {near_coefficient():.12f}   cp_energy*r^6 at r w0=1e-5: {-cp_energy(1e-5, 1, 1) * 1e-30:.12f}")
    # London route: U = -sum_ij d^4 (delta_ij - 3 rr)^2 / (2 w0 r^6), d^4 = alpha0^2 w0^2/4
    rh = np.array([0.0, 0.0, 1.0])
    Tdd = np.eye(3) - 3 * np.outer(rh, rh)
    print(f"London (electrostatic 2nd order) D = {np.sum(Tdd**2) / 4 / 2:.12f}")
    # direction average check of tau at one point
    kr = 2.3
    zz = quad(lambda th: (1 - math.cos(th)**2) * math.cos(kr * math.cos(th)) * math.sin(th) / 2, 0, math.pi)[0]
    s, c = math.sin(kr), math.cos(kr)
    print(f"tau_zz: angular quadrature {zz:.8f} vs P+Q {(s/kr+c/kr**2-s/kr**3)+(-s/kr-3*c/kr**2+3*s/kr**3):.8f}")
    # direct double integral, Richardson in eps
    for r in (2.0,):   # (slow: ~4 min)
        es = np.array([0.4, 0.2, 0.1, 0.05]) / r
        v = np.array([_U_double(r, e, Sf) for e in es])
        ext = np.polyfit(es, v, 2)[-1]
        print(f"r w0={r}: eq.(3) U = {cp_energy(r, 1, 1):.6e}; direct eq.(1) extrapolated eps->0: {ext:.6e}  (raw {v})")
    # numerical stability: t-form vs s-form at rho = 1 boundary region
    rho = 1.0
    gt = lambda t: math.exp(-2 * rho * t) * _p(rho * t) / (1 + t * t)**2
    print(f"J(1): s-form {_J(1.0):.14f}, t-form {quad(gt, 0, np.inf, epsrel=1e-13, limit=400)[0]:.14f}")
