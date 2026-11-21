"""Charged massless spin-1/2 emission from a Schwarzschild hole with a fluctuating charge (SPEC.md).

See DERIVATION.md. Units G = c = hbar = k_B = 1, M = 1, r_h = 2, T = 1/(8 pi).
"""
import math
import functools

import numpy as np
from scipy.integrate import solve_ivp, ode

T_H = 1.0 / (8.0 * math.pi)          # SPEC: Hawking temperature, M = 1
EPS_H = 1e-10                         # start at r0 = 2 + EPS_H
RTOL = 1e-11
NSER = 60                             # max order of the asymptotic series

# ---------------------------------------------------------------- series of sqrt(1 - 2x)
_S = np.empty(NSER + 2)
_S[0] = 1.0
for _n in range(1, NSER + 2):
    # binom(1/2, n) (-2)^n recursively: c_n = c_{n-1} * (1/2 - (n-1))/n * (-2)
    _S[_n] = _S[_n - 1] * (0.5 - (_n - 1)) / _n * (-2.0)


def _series(w, ks, gs, x):
    """In-mode (A, B) at x = 1/r for R_+ = e^{-i Phi} A, R_- = e^{-i Phi} B (DERIVATION section 2),
    summed to the smallest term.  Vectorised over components (ks, gs)."""
    K = len(ks)
    a = np.zeros((NSER + 1, K), complex)
    b = np.zeros((NSER + 1, K), complex)
    a[0] = 1.0
    A = np.ones(K, complex)
    B = np.zeros(K, complex)
    xn = 1.0
    last = np.full(K, np.inf)
    active = np.ones(K, bool)
    for n in range(1, NSER + 1):
        sa = np.zeros(K, complex)
        for m in range(n):
            sa += _S[n - 1 - m] * a[m]
        bn = (-(n - 1) * b[n - 1] + 2j * gs * b[n - 1] - ks * sa) / (2j * w)
        if n >= 2:
            bn += 2 * (n - 2) * b[n - 2] / (2j * w)
        b[n] = bn
        sb = np.zeros(K, complex)
        for m in range(n + 1):
            sb += _S[n - m] * b[m]
        a[n] = (2 * (n - 1) * a[n - 1] - ks * sb) / n
        xn *= x
        ta, tb = a[n] * xn, b[n] * xn
        size = np.abs(ta) + np.abs(tb)
        active &= size < last          # stop at the smallest term (asymptotic series)
        A = A + np.where(active, ta, 0)
        B = B + np.where(active, tb, 0)
        last = np.where(active, size, last)
        if not active.any() or (last < 1e-18).all():
            break
    return A, B


def _rmax(w, kmax, gmax):
    return max(40.0, (20.0 + kmax * kmax) / w, 40.0 * gmax / w)


def _solve(w, ks, gs, rmax=None):
    """Gamma for every component (k, g) at frequency w; returns (Gamma, Gamma_flux_check)."""
    ks = np.asarray(ks, float)
    gs = np.asarray(gs, float)
    K = len(ks)
    if rmax is None:
        rmax = _rmax(w, ks.max(), np.abs(gs).max())
    y0 = math.log(EPS_H)
    r0 = 2.0 + EPS_H
    t0 = r0 + 2.0 * math.log(EPS_H / 2.0)
    t1 = rmax + 2.0 * math.log(rmax / 2.0 - 1.0)
    f0 = EPS_H / r0
    W0 = ks * math.sqrt(f0) / r0
    Phi0 = w * t0 - gs * y0
    wH = w - gs / 2.0
    v0 = W0 * np.exp(-2j * Phi0) / (0.25 - 2j * wH)
    # real state [y, Re u, Im u, Re v, Im v]; Fortran DOP853 (scipy.integrate.ode) -- no BLAS calls in the stepper
    z0 = np.concatenate([[y0], np.ones(K), np.zeros(K), v0.real, v0.imag])

    def rhs(t, z):
        y = z[0]
        ey = math.exp(y)
        r = 2.0 + ey
        f = ey / r
        Wk = ks * (math.sqrt(f) / r)
        a = 2.0 * (w * t - gs * y)
        c, s_ = Wk * np.cos(a), Wk * np.sin(a)
        ur, ui = z[1:K + 1], z[K + 1:2 * K + 1]
        vr, vi = z[2 * K + 1:3 * K + 1], z[3 * K + 1:]
        out = np.empty_like(z)
        out[0] = 1.0 / r
        out[1:K + 1] = c * vr - s_ * vi            # u' = W e^{+ia} v
        out[K + 1:2 * K + 1] = c * vi + s_ * vr
        out[2 * K + 1:3 * K + 1] = c * ur + s_ * ui  # v' = W e^{-ia} u
        out[3 * K + 1:] = c * ui - s_ * ur
        return out

    solver = ode(rhs).set_integrator("dop853", rtol=RTOL, atol=1e-16, nsteps=10 ** 7)
    solver.set_initial_value(z0, t0)
    z = solver.integrate(t1)
    if not solver.successful():
        raise RuntimeError(f"ODE integration failed at w = {w}")
    y = z[0]
    r = 2.0 + math.exp(y)
    u = z[1:K + 1] + 1j * z[K + 1:2 * K + 1]
    v = z[2 * K + 1:3 * K + 1] + 1j * z[3 * K + 1:]
    Phi = w * t1 - gs * y
    x = 1.0 / r
    Ain, Bin = _series(w, ks, gs, x)            # in-mode (A, B)
    Eout, Cout = _series(-w, ks, -gs, x)        # out-mode (E, C): in-mode with (w, g) -> (-w, -g)
    e2 = np.exp(2j * Phi)
    # u = Ai*A + Ao*e2*C ;  v = Ai*conj(e2)*B + Ao*E
    m11, m12 = Ain, e2 * Cout
    m21, m22 = np.conj(e2) * Bin, Eout
    det = m11 * m22 - m12 * m21
    Ai = (u * m22 - m12 * v) / det
    Ao = (m11 * v - m21 * u) / det
    gam = 1.0 / np.abs(Ai) ** 2
    gam2 = 1.0 - np.abs(Ao) ** 2 / np.abs(Ai) ** 2
    return gam, gam2


@functools.lru_cache(maxsize=4096)
def _transmission_cached(k, w, g):
    gam, _ = _solve(w, [float(k)], [g])
    return float(min(max(gam[0], 0.0), 1.0))


def transmission(j, w, g):
    """Gamma_j(w; g), SPEC section 2."""
    k = int(round(j + 0.5))
    return _transmission_cached(k, round(float(w), 15), round(float(g), 15))


# ---------------------------------------------------------------- tables for the rates
KMAX = 10
PANEL_BREAKS = (0.0, 0.05, 0.15, 0.3, 0.5, 0.8, 1.2, 1.8, 2.6)
NGL = 16
NCHEB = 25
G0 = 0.25


def _omega_nodes(breaks=PANEL_BREAKS, ngl=NGL):
    xg, wg = np.polynomial.legendre.leggauss(ngl)
    om, wt = [], []
    for a, b in zip(breaks[:-1], breaks[1:]):
        om.append(0.5 * (b - a) * xg + 0.5 * (a + b))
        wt.append(0.5 * (b - a) * wg)
    return np.concatenate(om), np.concatenate(wt)


def _cheb_nodes(G, n):
    j = np.arange(n)
    return G * np.cos(math.pi * j / (n - 1))           # Chebyshev-Lobatto, barycentric weights (-1)^j, halved at ends


@functools.lru_cache(maxsize=8)
def _table(G, ncheb, kmax, breaks, ngl):
    om, wt = _omega_nodes(breaks, ngl)
    gn = _cheb_nodes(G, ncheb)
    kk, gg = np.meshgrid(np.arange(1, kmax + 1, dtype=float), gn, indexing="ij")
    ks, gs = kk.ravel(), gg.ravel()
    lnG = np.empty((len(om), kmax, ncheb))
    for i, w in enumerate(om):
        gam, _ = _solve(w, ks, gs)
        lnG[i] = np.log(np.maximum(gam, 1e-300)).reshape(kmax, ncheb)
    return om, wt, gn, lnG


def _bary_weights(gn, g):
    n = len(gn)
    lam = (-1.0) ** np.arange(n)
    lam[0] *= 0.5
    lam[-1] *= 0.5
    d = g - gn
    hit = np.abs(d) < 1e-15
    if hit.any():
        out = np.zeros(n)
        out[np.argmax(hit)] = 1.0
        return out
    c = lam / d
    return c / c.sum()


def _config_for(g):
    G, n = G0, NCHEB
    while abs(g) > G:
        G *= 2.0
        n = 2 * n - 1
    return G, n


def _rates_impl(g_gb, g_mu, kmax=None, breaks=None, ngl=None, ncheb=None, G=None):
    kmax = KMAX if kmax is None else kmax
    breaks = PANEL_BREAKS if breaks is None else breaks
    ngl = NGL if ngl is None else ngl
    if G is None:
        G, ncheb = _config_for(g_gb)
    om, wt, gn, lnG = _table(G, ncheb, kmax, breaks, ngl)
    bw = _bary_weights(gn, g_gb)
    gam = np.exp(lnG @ bw)                                   # (n_omega, kmax)
    deg = 2.0 * np.arange(1, kmax + 1)                       # 2j + 1 = 2k
    xarg = (om - 0.5 * g_mu) / T_H
    nF = 0.5 * (1.0 - np.tanh(0.5 * xarg))                   # 1/(e^x + 1), overflow-safe
    s = (gam @ deg) * nF * wt / (2.0 * math.pi)
    return float(s.sum()), float((s * om).sum())


@functools.lru_cache(maxsize=100000)
def _rates_cached(g_gb, g_mu):
    return _rates_impl(g_gb, g_mu)


def rates(g_gb, g_mu):
    """(N, P) per helicity state, SPEC section 3."""
    return _rates_cached(round(float(g_gb), 15), round(float(g_mu), 15))


# ---------------------------------------------------------------- charge process
_NSEL = {"before": lambda q, n: n, "mid": lambda q, n: n - q / 2.0, "after": lambda q, n: n - q}


def _couplings(alpha, rule, q, n):
    r_gb, r_mu = rule
    return alpha * q * _NSEL[r_gb](q, n), alpha * q * _NSEL[r_mu](q, n)


def _up(alpha, rule, n):
    return rates(*_couplings(alpha, rule, -1, n))


def _down(alpha, rule, n):
    return rates(*_couplings(alpha, rule, +1, n))


@functools.lru_cache(maxsize=256)
def _distribution(alpha, rule):
    lnp = {0: 0.0}
    n = 0
    while True:                               # pi(n+1)/pi(n) = up(n)/down(n+1)
        lnp[n + 1] = lnp[n] + math.log(_up(alpha, rule, n)[0]) - math.log(_down(alpha, rule, n + 1)[0])
        n += 1
        if lnp[n] < math.log(1e-17) or n > 100000:
            break
    m = 0
    while True:                               # pi(m-1)/pi(m) = down(m)/up(m-1)
        lnp[m - 1] = lnp[m] + math.log(_down(alpha, rule, m)[0]) - math.log(_up(alpha, rule, m - 1)[0])
        m -= 1
        if lnp[m] < math.log(1e-17) or m < -100000:
            break
    mx = max(lnp.values())
    p = {k: math.exp(v - mx) for k, v in lnp.items()}
    z = math.fsum(p.values())
    p = {k: v / z for k, v in p.items()}
    p = {k: v for k, v in p.items() if v >= 1e-14}
    z = math.fsum(p.values())
    return tuple(sorted((k, v / z) for k, v in p.items()))


def charge_distribution(alpha, rule=("after", "after")):
    return dict(_distribution(float(alpha), tuple(rule)))


def _averages(alpha, rule):
    pi = charge_distribution(alpha, rule)
    Nm = Pm = 0.0
    for n, p in pi.items():
        Ne, Pe = _up(alpha, rule, n)
        Np, Pp = _down(alpha, rule, n)
        Nm += p * 0.5 * (Ne + Np)
        Pm += p * 0.5 * (Pe + Pp)
    return Nm, Pm


def weight_ratio(alpha, rule=("after", "after")):
    N0, P0 = rates(0.0, 0.0)
    return _averages(float(alpha), tuple(rule))[1] / P0


def energy_ratio(alpha, rule=("after", "after")):
    N0, P0 = rates(0.0, 0.0)
    Nm, Pm = _averages(float(alpha), tuple(rule))
    return (Pm / Nm) / (P0 / N0)


PROVENANCE = {
    "transmission": ("derived", "phase-factored Dirac system, exact Coulomb phase, horizon series start, asymptotic-series matching; Gamma = 1/|A_in|^2"),
    "rates": ("derived", "Gauss-Legendre panels in omega, k = 1..10, Chebyshev interpolation of ln Gamma in g_gb, Fermi-Dirac with mu = g_mu/2"),
    "charge_distribution": ("derived", "detailed balance of the nearest-neighbour birth-death chain, up = N(electron), down = N(positron)"),
    "weight_ratio": ("derived", "<P>/P(0,0) from the stationary distribution"),
    "energy_ratio": ("derived", "(<P>/<N>)/(P0/N0)"),
}


# ---------------------------------------------------------------- independent second routes
def _gamma_schrodinger(k, w, rmax_factor=2.0e3):
    """g = 0 only: psi = R_+ + R_- obeys psi'' + (w^2 - V)psi = 0 (' = d/dr*), V = W^2 + dW/dr*.
    Integrated in y = ln(r - 2) (d/dr* = (1/r) d/dy) from r - 2 = 1e-20, horizon psi = e^{-i w r*};
    plain plane-wave projection at large r, no asymptotic series.  Gamma = 1/|a|^2."""
    y0 = math.log(1e-20)
    rs0 = 2.0 + 1e-20 + 2.0 * (y0 - math.log(2.0))
    rmax = max(200.0, rmax_factor / w)
    y1 = math.log(rmax - 2.0)

    def rhs(y, z):
        ey = math.exp(y)
        r = 2.0 + ey
        f = ey / r
        sf = math.sqrt(f)
        W = k * sf / r
        dWdr = k * (1.0 / (r ** 3 * sf) - sf / (r * r))
        V = W * W + f * dWdr
        return np.array([r * z[1], r * (V - w * w) * z[0]])

    z0 = np.array([np.exp(-1j * w * rs0), -1j * w * np.exp(-1j * w * rs0)])
    sol = solve_ivp(rhs, (y0, y1), z0, method="DOP853", rtol=1e-12, atol=1e-16)
    psi, dpsi = sol.y[0, -1], sol.y[1, -1]
    rs = rmax + 2.0 * math.log(rmax / 2.0 - 1.0)
    a = (1j * w * psi - dpsi) * np.exp(1j * w * rs) / (2j * w)   # coefficient of e^{-i w r*}
    return 1.0 / abs(a) ** 2


def _gamma_leading_match(k, w, g, rmax):
    """Any g: same horizon start, matching only to the leading Coulomb plane waves (u ~ A_in, v ~ A_out) at a large rmax."""
    ks, gs = np.array([float(k)]), np.array([float(g)])
    old = _series

    def lead(w_, ks_, gs_, x):
        return np.ones(len(ks_), complex), np.zeros(len(ks_), complex)

    globals()["_series"] = lead
    try:
        gam, _ = _solve(w, ks, gs, rmax=rmax)
    finally:
        globals()["_series"] = old
    return float(gam[0])


if __name__ == "__main__":
    alpha = 1 / 137.035999084
    print("Gamma checks (main | flux form | Schrodinger route (g=0) | leading-order match at large r):")
    for k, w, g in ((1, 0.05, 0.0), (1, 0.3, 0.0), (2, 0.2, 0.0), (3, 0.6, 0.0), (1, 0.1, 0.1), (2, 0.3, -0.1), (1, 0.03, 0.2)):
        a, b = _solve(w, [k], [g])
        s = _gamma_schrodinger(k, w) if g == 0 else float("nan")
        l = _gamma_leading_match(k, w, g, rmax=4000.0 * k / w)
        print(f"  k={k} w={w} g={g}: {a[0]:.12e} | {b[0]:.12e} | {s:.12e} | {l:.12e}")
    print("rmax x2 check:", _solve(0.3, [1, 2], [0.0, 0.05])[0], _solve(0.3, [1, 2], [0.0, 0.05], rmax=2 * _rmax(0.3, 2, 0.05))[0])
    N0, P0 = rates(0.0, 0.0)
    print(f"neutral N0 = {N0:.10e}  P0 = {P0:.10e}")
    for rule in [(a_, b_) for a_ in ("before", "mid", "after") for b_ in ("before", "mid", "after")]:
        print(rule, "weight_ratio =", f"{weight_ratio(alpha, rule):.10f}", " energy_ratio =", f"{energy_ratio(alpha, rule):.10f}",
              " n_max =", max(charge_distribution(alpha, rule)))

    # second route for pi: null vector of the generator (linear algebra), principal rule
    import scipy.linalg as sla
    rule = ("after", "after")
    pi = charge_distribution(alpha, rule)
    ns = sorted(pi)
    Q = np.zeros((len(ns), len(ns)))
    for i, n in enumerate(ns):
        if i + 1 < len(ns):
            Q[i, i + 1] = _up(alpha, rule, n)[0]
        if i > 0:
            Q[i, i - 1] = _down(alpha, rule, n)[0]
    Q -= np.diag(Q.sum(1))
    nv = sla.null_space(Q.T)[:, 0]
    nv /= nv.sum()
    print("pi: null space vs detailed balance, max diff", np.max(np.abs(nv - np.array([pi[n] for n in ns]))))
    print("<n^2> =", sum(p * n * n for n, p in pi.items()))
    # small-alpha behaviour: (ratio - 1)/alpha should tend to a constant
    for fac in (1.0, 0.5, 0.25):
        wr = weight_ratio(alpha * fac)
        print(f"alpha*{fac}: weight_ratio = {wr:.10f}, (wr - 1)/alpha = {(wr - 1) / (alpha * fac):.6f}, energy_ratio = {energy_ratio(alpha * fac):.10f}")
    # second route for the principal rule at small alpha: expand in g (DERIVATION section 5.5)
    h = 1e-3
    Np_, Pp_ = rates(h, h)
    Nm_, Pm_ = rates(-h, -h)
    Lg = (math.log(Np_) - math.log(Nm_)) / (2 * h)
    cP = -(Pp_ - Pm_) / (2 * h) / P0 + (Pp_ - 2 * P0 + Pm_) / h ** 2 / (4 * Lg * P0)
    cN = -(Np_ - Nm_) / (2 * h) / N0 + (Np_ - 2 * N0 + Nm_) / h ** 2 / (4 * Lg * N0)
    print(f"perturbative: weight_ratio ~ 1 + {cP:.5f} alpha = {1 + cP * alpha:.6f}; energy_ratio ~ 1 + {cP - cN:.5f} alpha = {1 + (cP - cN) * alpha:.6f}")
    # numerical-parameter convergence of the principal results (each parameter changed by ~2x)
    base = (weight_ratio(alpha), energy_ratio(alpha))
    for name, val in (("KMAX", 5), ("NGL", 32), ("NCHEB", 49)):
        old = globals()[name]
        globals()[name] = val
        _rates_cached.cache_clear(); _distribution.cache_clear()
        alt = (weight_ratio(alpha), energy_ratio(alpha))
        print(f"{name} {old} -> {val}: d weight_ratio = {alt[0] - base[0]:.2e}, d energy_ratio = {alt[1] - base[1]:.2e}")
        globals()[name] = old
        _rates_cached.cache_clear(); _distribution.cache_clear()
