"""Grey-body factors and Hawking power of Schwarzschild (G=c=hbar=M=1). See DERIVATION.md."""
import math
import cmath
import functools
import numpy as np
from scipy.integrate import solve_ivp

PROVENANCE = {
    "transmission": ("derived", "ODE from horizon (ingoing) to far field, matched to asymptotic series; Gamma=1/|A_in|^2"),
    "absorption_sum": ("derived", "sum (2j+1) Gamma over j until Gamma negligible"),
    "power_per_dof": ("derived", "Gauss-Legendre in w of sum_j (2j+1) w Gamma/(2 pi (e^{w/T} -+ 1)), T=1/(8 pi)"),
}

T_H = 1.0 / (8.0 * math.pi)
_SIGMA = -1


def _gcoef(s, j, N, sigma):
    """Taylor coefficients g_p of V/f in x=1/r, p=0..N."""
    g = np.zeros(N + 2)
    if s == 0.5:
        k = j + 0.5
        inv = [math.comb(2 * n, n) / 2.0 ** n for n in range(N + 2)]
        g[2] += k * k
        for n in range(N + 2):
            if n + 2 <= N + 1:
                g[n + 2] -= sigma * k * inv[n]
            if n + 3 <= N + 1:
                g[n + 3] += sigma * k * 3.0 * inv[n]
    else:
        g[2] = j * (j + 1.0)
        g[3] += 2.0 * (1.0 - s * s)
    return g


def _series(g, w, x, N):
    """u(x), du/dr for u=sum c_n x^n, solving 2iw u_r+(f u_r)_r - g u=0. Returns (u, u_r)."""
    c = [1.0 + 0j]
    mags = [1.0]
    for m in range(1, N + 1):
        t = (m - 1) * m * c[m - 1]
        if m >= 2:
            t -= 2.0 * (m - 2) * m * c[m - 2]
        for p in range(2, m + 2):
            t -= g[p] * c[m + 1 - p]
        cm = t / (2j * w * m)
        c.append(cm)
        mags.append(abs(cm) * x ** m)
        if max(mags[-1], mags[-2]) < 1e-19 or mags[-1] > 1e30:   # converged, or clearly past the smallest term
            break
    # asymptotic series: truncate at the smallest term (pairwise max, since a coefficient can vanish identically)
    pm = [max(mags[i], mags[i + 1]) for i in range(len(mags) - 1)]
    last = (int(np.argmin(pm)) + 1) if pm else 0
    u = sum(c[n] * x ** n for n in range(last + 1))
    du_dx = sum(n * c[n] * x ** (n - 1) for n in range(1, last + 1))
    return u, -x * x * du_dx


def _potential(s, j, d, sigma):
    r = 2.0 + d
    f = d / r
    if s == 0.5:
        k = j + 0.5
        return k * k * f / r ** 2 + sigma * k * math.sqrt(f) * (3.0 / r ** 3 - 1.0 / r ** 2)
    return f * (j * (j + 1.0) / r ** 2 + 2.0 * (1.0 - s * s) / r ** 3)


def _amplitudes(s, j, w, R=None, d0fac=1e-22, rtol=1e-12, sigma=None, N=80):
    sigma = _SIGMA if sigma is None else sigma
    if R is None:
        L = j * (j + 1.0) + 2
        R = max(70.0 / w, 80.0 + 12.0 * L / (1.0 + w))
    d0 = d0fac * min(1.0, w) ** 2
    t0, t1 = math.log(d0), math.log(R - 2.0)
    rs0 = 2.0 + d0 + 2.0 * math.log(d0 / 2.0)
    psi0 = cmath.exp(-1j * w * rs0)
    y0 = np.array([psi0, -1j * w * psi0], dtype=complex)

    def rhs(t, y):
        d = math.exp(t)
        r = 2.0 + d
        V = _potential(s, j, d, sigma)
        return [r * y[1], -(w * w - V) * r * y[0]]

    sol = solve_ivp(rhs, (t0, t1), y0, method="DOP853", rtol=rtol, atol=1e-14, dense_output=False)
    psi, Phi = sol.y[0, -1], sol.y[1, -1]
    g = _gcoef(s, j, N, sigma)
    x = 1.0 / R
    f = 1.0 - 2.0 * x
    rs = R + 2.0 * math.log(R / 2.0 - 1.0)
    up, upr = _series(g, w, x, N)
    um, umr = _series(g, -w, x, N)
    pp = cmath.exp(1j * w * rs) * up
    ppd = cmath.exp(1j * w * rs) * (1j * w * up + f * upr)
    pm = cmath.exp(-1j * w * rs) * um
    pmd = cmath.exp(-1j * w * rs) * (-1j * w * um + f * umr)
    # psi = Ain*pm + Aout*pp
    det = pm * ppd - pp * pmd
    Ain = (psi * ppd - pp * Phi) / det
    Aout = (pm * Phi - psi * pmd) / det
    return Ain, Aout


@functools.lru_cache(maxsize=None)
def _gamma(s, j, w):
    Ain, _ = _amplitudes(s, j, w)
    return 1.0 / abs(Ain) ** 2


def transmission(s, j, w):
    s = float(s)
    j = float(j)
    w = float(w)
    if s == 0.5:
        pass
    elif s == int(s):
        s = float(int(s))
    return _gamma(s, j, w)


def _jmin(s):
    return 0.5 if s == 0.5 else float(max(0, int(s)))


def absorption_sum(s, w, cut=1e-15):
    s = float(s)
    j = _jmin(s)
    tot = 0.0
    while True:
        g = transmission(s, j, w)
        tot += (2 * j + 1) * g
        if g < cut and j > _jmin(s) + 1 or j > 200:
            break
        j += 1.0
    return tot


def _panels(wmax):
    edges = [0.0, 0.1, 0.3, 0.6, 1.0, 1.6, wmax]
    return [(a, b) for a, b in zip(edges, edges[1:]) if b > a]


def _power(s, nodes=12, wmax=2.4, cut=1e-15):
    s = float(s)
    sign = 1.0 if s == 0.5 else -1.0
    x, wt = np.polynomial.legendre.leggauss(nodes)
    tot = 0.0
    for a, b in _panels(wmax):
        for xi, wi in zip(x, wt):
            w = 0.5 * (b - a) * xi + 0.5 * (a + b)
            occ = 1.0 / math.expm1(w / T_H) if sign < 0 else 1.0 / (math.exp(w / T_H) + 1.0)
            tot += 0.5 * (b - a) * wi * w * occ * absorption_sum(s, w, cut) / (2 * math.pi)
    return tot


@functools.lru_cache(maxsize=None)
def _power_cached(s):
    return _power(s)


def power_per_dof(s):
    return _power_cached(float(s))


if __name__ == "__main__":
    print("second route (a): flux conservation 1-|Aout/Ain|^2 vs 1/|Ain|^2")
    for s, j, w in ((0, 0, 0.3), (0.5, 1.5, 0.7), (1, 1, 1.2), (2, 2, 0.5), (0, 5, 2.0)):
        Ain, Aout = _amplitudes(float(s), float(j), w)
        print(s, j, w, 1 / abs(Ain) ** 2, 1 - abs(Aout / Ain) ** 2)
    print("(c) sigma +-: Gamma", [1 / abs(_amplitudes(0.5, 1.5, 0.7, sigma=sg)[0]) ** 2 for sg in (1, -1)])
    print("(b) vary R, d0, rtol:", 1 / abs(_amplitudes(2.0, 2.0, 0.05)[0]) ** 2,
          1 / abs(_amplitudes(2.0, 2.0, 0.05, R=4000.0, d0fac=1e-10, rtol=1e-12)[0]) ** 2)
    print("(d) Gamma_00/w^2 at 0.005:", transmission(0, 0, 0.005) / 0.005 ** 2)
    for s in (0, 0.5, 1, 2):
        p1 = _power(s, 12)
        p2 = _power(s, 16, wmax=2.8, cut=1e-17)
        print("P", s, p1, p2, abs(p1 / p2 - 1))
