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
    # decade breakpoints 10, 100, ... up to T = 1/rho: without them quad under-samples the 1/t^4 region of a single
    # panel [10, T] and loses ~1e-3 of J for rho <= 1e-7 (found in audit; now within 2e-16 of mpmath for 1e-12 <= rho <= 1e5)
    decades = [10.0**j for j in range(1, int(math.log10(T)) + 1)] if T > 10 else [10.0]
    pts = [0.0, 1.0] + decades + ([T, 20 * T] if T > 10 else [])
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



# ---------------------------------------------------------------- SPEC 3b intermediate exports

def denominator_sum(k, q, a, b):
    """SPEC 3b: sum over the 24 orderings of the vertex events (A,k),(A,q),(B,k),(B,q) of 1/(E1 E2 E3), / 2.
    Each event toggles its atom (energy a or b) and its photon (energy k or q); E_n = energy after n events."""
    W = {'A': a, 'B': b}
    E = {'k': k, 'q': q}
    tot = 0.0
    for perm in itertools.permutations((('A', 'k'), ('A', 'q'), ('B', 'k'), ('B', 'q'))):
        ex = {'A': False, 'B': False}
        ph = {'k': False, 'q': False}
        prod = 1.0
        for at, pp in perm[:3]:
            ex[at] = not ex[at]
            ph[pp] = not ph[pp]
            prod *= sum(W[z] for z in ex if ex[z]) + sum(E[z] for z in ph if ph[z])
        tot += 1.0 / prod
    return tot / 2


def _kgrid(r, eps, a, b, refine=1):
    """Gauss-Legendre nodes/weights on [0, K]: graded panels near k = 0, then panels of width <= pi/(2r),
    <= 1/(2 eps) and <= min(a,b)/2; K chosen so that k^6 e^{-eps k} has fallen below 1e-30 of its peak."""
    K = (80.0 + 6 * math.log(1 + 6 / (eps * min(a, b)))) / eps * (1 + 0.25 * (refine - 1))
    h = min(math.pi / (2 * r), 0.5 / eps, 0.5 * min(a, b)) / refine
    edges = [0.0] + [h * 2.0**(-j) for j in range(40, 0, -1)]
    edges += list(np.arange(h, K, h)) + [K]
    edges = np.unique(np.array(edges))
    xg, wg = np.polynomial.legendre.leggauss(16)
    mid, half = (edges[:-1] + edges[1:]) / 2, (edges[1:] - edges[:-1]) / 2
    return (mid[:, None] + half[:, None] * xg).ravel(), (half[:, None] * wg).ravel()


def _PQ(x):
    """tau_ij(x) = P delta_ij + Q rhat_i rhat_j with P = (2 j0 - j2)/3, Q = j2 (stable form of DERIVATION sec 2)."""
    from scipy.special import spherical_jn
    j0, j2 = spherical_jn(0, x), spherical_jn(2, x)
    return (2 * j0 - j2) / 3, j2


def _tr(G1, G2):
    """Tr[(P1 d + Q1 rr)(P2 d + Q2 rr)] = 3 P1 P2 + P1 Q2 + Q1 P2 + Q1 Q2."""
    return 3 * G1[0] * G2[0] + G1[0] * G2[1] + G1[1] * G2[0] + G1[1] * G2[1]


def damped_energy(r, w0, alpha0, eps, _refine=1):
    """SPEC 3b: eq.(1) of DERIVATION.md with the factor e^{-eps(k+q)}, evaluated without identity (2).
    Sigma_12 = 4/[(a+k)(a+q)(b+k)(b+q)] [ab/(k+q) + (a+b) + (k+q) + kq/(a+b)] (exact algebra, DERIVATION sec 8);
    the separable pieces are products of 1D k-integrals, and the 1/(k+q) piece uses 1/(k+q) = int_0^inf ds e^{-s(k+q)}
    (a real Laplace variable), giving an s-integral of products of 1D k-integrals. All integrals converge absolutely."""
    a = b = w0
    d4 = alpha0**2 * w0**2 / 4
    k, w = _kgrid(r, eps, a, b, _refine)
    P, Q = _PQ(k * r)
    g = w * k**3 * np.exp(-eps * k) / ((a + k) * (b + k))
    G = lambda f: (np.dot(g * f, P), np.dot(g * f, Q))
    G0, G1 = G(1.0), G(k)
    sep = (a + b) * _tr(G0, G0) + 2 * _tr(G1, G0) + _tr(G1, G1) / (a + b)

    def lap(s):
        Gs = G(np.exp(-np.minimum(s * k, 200.0)))   # cap keeps products out of slow subnormal floats; e^-200 is negligible
        return _tr(Gs, Gs)

    # s-integral: integrand ~ s^-8 for s >> 1/r, eps; panels on a log scale
    sc = 1.0 / (r + eps)
    pts = [0.0] + [sc * 2.0**j for j in range(-6, 30)]
    # absolute floor relative to the size of the s-integral (~ lap(0) * sc); a pure relative target cannot be met
    # on far-tail panels where the integrand is ~1e-40 of its peak
    opts = dict(epsabs=1e-13 * abs(lap(0.0)) * sc / _refine**2, epsrel=1e-11 / _refine**2, limit=200)
    L = sum(quad(lap, lo, hi, **opts)[0] for lo, hi in zip(pts, pts[1:]))
    return -(d4 / math.pi**2) * 4 * (a * b * L + sep)

PROVENANCE = {
    "cp_energy": ("derived", "runtime: scipy quad of the 1D imaginary-frequency integral U = -(1/pi r^6) int du "
                             "alpha(iu)^2 e^{-2ur} p(ur) (eq. 3), in dimensionless form J(rho); eq. 3 itself is derived "
                             "in DERIVATION secs 1-4 from 4th-order RS over the 12 two-photon exchange diagrams "
                             "(denominator identity (2), posited and proved by residues, + closed-form k-integrals); "
                             "valid and checked against mpmath for 1e-12 <= r*w0 <= 1e5"),
    "far_coefficient": ("derived", "rho -> infinity limit of J(rho): sum c_n n!/2^{n+1}/pi (DERIVATION sec 5)"),
    "near_coefficient": ("derived", "rho -> 0 limit of J(rho): (1/pi) int 3/(1+t^2)^2; cross-checked by London route"),
    "denominator_sum": ("derived", "literal SPEC 3b enumeration (24 orderings / 2) of the 4th-order RS energy denominators; "
                                   "equals Sigma_12 of DERIVATION sec 3 (checked symbolically in __main__)"),
    "damped_energy": ("derived", "eq.(1) (12-diagram RS sum) with e^{-eps(k+q)}: exact split of Sigma_12 + real Laplace "
                                 "variable for 1/(k+q), Gauss-Legendre in k, quad in s; no identity (2), no imaginary "
                                 "frequency (DERIVATION sec 8); ~1e-10 relative, tested for 0.25 <= eps*w0 <= 1 at "
                                 "0.3 <= r*w0 <= 3 (grid refinement + brute force), and down to eps*w0 = 0.003"),
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
    rng = np.random.default_rng(1)
    worst = 0.0
    for _ in range(5):
        av, bv, kv, qv = rng.uniform(0.3, 3.0, 4)
        lhs = Sf(av, bv, kv, qv)
        rhs = 8 / math.pi * quad(lambda u: av * bv * kv * qv / ((av**2 + u**2) * (bv**2 + u**2) * (kv**2 + u**2)
                                 * (qv**2 + u**2)), 0, np.inf, epsabs=0, epsrel=1e-13)[0]
        worst = max(worst, abs(rhs / lhs - 1))
    print(f"identity (2) numerically at 5 random (a,b,k,q): max relative deviation {worst:.2e}")
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
    # ---- SPEC 3b exports
    fS = sp.lambdify(syms, S)                     # Sigma_12(a, b, k, q) from the 12 ordered paths
    rng = np.random.default_rng(7)
    worst = 0.0
    for _ in range(20):
        av, bv, kv, qv = rng.uniform(0.05, 5.0, 4)
        worst = max(worst, abs(denominator_sum(kv, qv, av, bv) / fS(av, bv, kv, qv) - 1))
    print(f"denominator_sum (24/2 rule) vs 12-path Sigma_12 at 20 random points, a != b: max rel. dev. {worst:.2e}")
    a_, b_, k_, q_ = syms
    split = 4 / ((a_ + k_) * (a_ + q_) * (b_ + k_) * (b_ + q_)) * (a_ * b_ / (k_ + q_) + (a_ + b_) + (k_ + q_) + k_ * q_ / (a_ + b_))
    print(f"exact split of Sigma_12 used by damped_energy (DERIVATION sec 8): residual {sp.simplify(split - S)}")
    for r, e in ((1.0, 0.5), (3.0, 1.0), (0.3, 0.25), (2.0, 0.25)):
        dm, dr = damped_energy(r, 1.0, 1.0, e), damped_energy(r, 1.0, 1.0, e, _refine=2)
        bf = _U_double(r, e, Sf)
        print(f"damped_energy(r={r}, eps={e}) = {dm:.12e}; refined grid {dr / dm - 1:+.1e}; "
              f"brute-force eq.(1) grid {bf / dm - 1:+.1e}")
    for r in (0.3, 1.0, 3.0):
        U = cp_energy(r, 1.0, 1.0)
        es = (0.1, 0.03, 0.01, 0.003)
        dev = [damped_energy(r, 1.0, 1.0, e) / U - 1 for e in es]
        lin = (dev[-1] - dev[-2]) / (es[-1] - es[-2])
        print(f"r w0={r}: damped/cp_energy - 1 at eps={es}: " + ", ".join(f"{d:+.3e}" for d in dev)
              + f"; linear in eps, intercept {dev[-1] - lin * es[-1]:+.1e} (test only)")
    # numerical stability: t-form vs s-form at rho = 1 boundary region
    import mpmath as mp
    mp.mp.dps = 30
    worst = 0.0
    for rho in (1e-12, 1e-9, 1e-7, 1e-5, 1e-2, 0.5, 1.0, 3.0, 1e2, 1e4, 1e5):
        rm = mp.mpf(rho)
        g = lambda t: mp.e**(-2 * rm * t) * sum(c * (rm * t)**n for n, c in enumerate(_C)) / (1 + t * t)**2
        ref = mp.quad(g, [0, 1, 10, 1 / rm, 20 / rm, mp.inf])
        worst = max(worst, abs(_J(rho) / float(ref) - 1))
    print(f"J(rho) vs 30-digit mpmath reference, rho in [1e-12, 1e5]: max relative deviation {worst:.2e}")
    rho = 1.0
    gt = lambda t: math.exp(-2 * rho * t) * _p(rho * t) / (1 + t * t)**2
    print(f"J(1): s-form {_J(1.0):.14f}, t-form {quad(gt, 0, np.inf, epsrel=1e-13, limit=400)[0]:.14f}")
