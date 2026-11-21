"""Grey-body factors and Hawking power per degree of freedom, Schwarzschild, G = c = hbar = k_B = M = 1.

See DERIVATION.md for every step. Main route: integrate the master equation from a purely ingoing horizon
solution outwards (stage 1 in r*, stage 2 in r) and match at finite R to the exact asymptotic 1/r series of the
in/outgoing solutions; Gamma = 1/|A_in|^2 (flux identity).
"""
import math
import functools
import numpy as np
from scipy.integrate import solve_ivp
from scipy.special import lambertw

R_H = 2.0                    # horizon radius 2M (SPEC)
T_HAWKING = 1.0 / (8.0 * math.pi)   # SPEC section 3
RSTAR_MIN = -160.0           # start of integration in r*; f ~ e^{(r*-2)/2}, sqrt(f) ~ e^{-40.5} (DERIVATION 2)
R_A = 3.0                    # switch from r* to r integration
RTOL, ATOL = 1e-12, 1e-300

PROVENANCE = {
    "transmission": ("derived", "ingoing horizon BC, ODE integration, matched to exact asymptotic 1/r series; Gamma=1/|A_in|^2 (unclipped); fermion horizon BC to O(sqrt f); rel. accuracy 1e-9 claimed (DERIVATION 9)"),
    "absorption_sum": ("derived", "sum over j >= s of (2j+1) transmission until terms negligible"),
    "power_per_dof": ("derived", "SPEC 3 integral: Gauss-Legendre panels in w on [0, w_max], partial waves until negligible"),
}


def _is_fermion(s):
    return abs(s - 0.5) < 1e-12


def _rstar(r):
    return r + 2.0 * math.log(r / 2.0 - 1.0)


def _v_over_f(s, j, r, sign=+1):
    """V/f as a function of r."""
    f = 1.0 - 2.0 / r
    if _is_fermion(s):
        k = j + 0.5
        return k * k / r**2 - sign * k * (1.0 - 3.0 / r) / (r**2 * math.sqrt(f))
    return j * (j + 1.0) / r**2 + 2.0 * (1.0 - s * s) / r**3


def _potential_x(s, j, x, sign=+1):
    """V in terms of x = r - 2 (accurate near the horizon)."""
    r = 2.0 + x
    f = x / r
    if _is_fermion(s):
        k = j + 0.5
        return k * k * f / r**2 - sign * k * math.sqrt(f) * (1.0 - 3.0 / r) / r**2
    return f * (j * (j + 1.0) / r**2 + 2.0 * (1.0 - s * s) / r**3)


def _vp_coeffs(s, j, nmax, sign=+1):
    """Coefficients v_p of V/f = sum_p v_p r^{-p} (p = 0..nmax+2)."""
    v = np.zeros(nmax + 3)
    if _is_fermion(s):
        k = j + 0.5
        b = np.zeros(nmax + 3)            # f^{-1/2} = sum_m b_m r^{-m}, b_m = C(2m,m)/2^m
        b[0] = 1.0
        for m in range(1, nmax + 3):
            b[m] = b[m - 1] * (2 * m - 1) / m      # b_m/b_{m-1} = (2m-1)/m
        v[2] += k * k
        for p in range(2, nmax + 3):
            term = b[p - 2] - (3.0 * b[p - 3] if p >= 3 else 0.0)
            v[p] -= sign * k * term
    else:
        v[2] = j * (j + 1.0)
        v[3] = 2.0 * (1.0 - s * s)
    return v


def _asymptotic(s, j, w, R, eps, sign=+1, nmax=400):
    """u_eps(R), du/dr(R) for psi_eps = e^{i eps w r*} sum_n a_n r^{-n}, a_0 = 1.

    Works with the scaled coefficients b_n = a_n R^{-n} (no overflow); recursion of DERIVATION section 4
    divided by R^{n+1}:
      2 i eps w (n+1) R b_{n+1} = n(n+1) b_n - 2(n^2-1) b_{n-1}/R - sum_p v_p b_{n+2-p} R^{2-p}.
    Summed up to n ~ 2 w R (smallest term of the asymptotic series) or until terms are negligible.
    """
    v = _vp_coeffs(s, j, nmax, sign)
    pmax = 3 if not _is_fermion(s) else nmax + 2
    Rpow = R ** (-np.arange(0, nmax + 3, dtype=float))     # R^{-(p-2)} for p - 2 = 0, 1, ...
    b = [1.0 + 0j]
    u = 1.0 + 0j
    du = 0j
    nstop = min(nmax, max(4, int(2.0 * w * R)))
    small = 0
    for n in range(0, nstop):
        acc = n * (n + 1.0) * b[n]
        if n >= 1:
            acc -= 2.0 * (n * n - 1.0) * b[n - 1] / R
        for p in range(2, min(n + 2, pmax) + 1):
            acc -= v[p] * b[n + 2 - p] * Rpow[p - 2]
        bn1 = acc / (2j * eps * w * (n + 1.0) * R)
        b.append(bn1)
        u += bn1
        du += -(n + 1.0) * bn1 / R
        small = small + 1 if abs(bn1) < 1e-18 * abs(u) else 0
        if small >= 3:               # three consecutive negligible terms (exact zeros can occur singly)
            break
    return u, du


def _match_radius(s, j, w):
    leff = (j + 0.5)**2 if _is_fermion(s) else j * (j + 1.0)
    return max(60.0, (30.0 + leff) / w)


def _solve(s, j, w, sign=+1, rstar_min=RSTAR_MIN, R=None):
    """Return (A_in, A_out) for the solution psi -> e^{-i w r*} at the horizon."""
    if R is None:
        R = _match_radius(s, j, w)
    # stage 1: r* from rstar_min to r*(R_A); state x, Re/Im psi, Re/Im psi'
    x0 = 2.0 * float(lambertw(math.exp(rstar_min / 2.0 - 1.0)).real)
    f0 = x0 / (2.0 + x0)
    ph = np.exp(-1j * w * rstar_min)
    if _is_fermion(s):
        # u = 1 + c sqrt(f): V ~ sign k sqrt(f)/8, d sqrt(f)/dr* = sqrt(f) f_r / 2 (DERIVATION 2)
        k = j + 0.5
        z0 = math.sqrt(f0)
        c = sign * 2.0 * k / (1.0 - 8j * w)
        psi0 = ph * (1.0 + c * z0)
        dpsi0 = ph * (-1j * w * (1.0 + c * z0) + c * z0 * (1.0 / (2.0 + x0)**2))
    else:
        v1 = j * (j + 1.0) / 4.0 + 2.0 * (1.0 - s * s) / 8.0
        c = v1 / (0.25 - 1j * w)
        dfac = f0 * (2.0 / (2.0 + x0)**2)          # d f / d r* = f * f_r
        psi0 = ph * (1.0 + c * f0)
        dpsi0 = ph * (-1j * w * (1.0 + c * f0) + c * dfac)

    def rhs1(t, y):
        x = y[0]
        V = _potential_x(s, j, x, sign)
        k = V - w * w
        return [x / (2.0 + x), y[3], y[4], k * y[1], k * y[2]]

    ta = _rstar(R_A)
    sol1 = solve_ivp(rhs1, (rstar_min, ta), [x0, psi0.real, psi0.imag, dpsi0.real, dpsi0.imag],
                     method="DOP853", rtol=RTOL, atol=ATOL)
    y = sol1.y[:, -1]

    # stage 2: r from R_A to R; state Re/Im psi, Re/Im chi (chi = dpsi/dr*)
    def rhs2(r, z):
        f = 1.0 - 2.0 / r
        k = (_v_over_f(s, j, r, sign) * f - w * w) / f
        return [z[2] / f, z[3] / f, k * z[0], k * z[1]]

    sol2 = solve_ivp(rhs2, (R_A, R), [y[1], y[2], y[3], y[4]], method="DOP853", rtol=RTOL, atol=ATOL)
    z = sol2.y[:, -1]
    psi = z[0] + 1j * z[1]
    chi = z[2] + 1j * z[3]

    fR = 1.0 - 2.0 / R
    rsR = _rstar(R)
    cols = []
    for eps in (-1, +1):
        u, du = _asymptotic(s, j, w, R, eps, sign)
        e = np.exp(1j * eps * w * rsR)
        cols.append((e * u, e * (1j * eps * w * u + fR * du)))
    M = np.array([[cols[0][0], cols[1][0]], [cols[0][1], cols[1][1]]])
    A_in, A_out = np.linalg.solve(M, np.array([psi, chi]))
    return A_in, A_out, abs(y[0] - (R_A - 2.0))


@functools.lru_cache(maxsize=None)
def _transmission(s, j, w):
    A_in, _, _ = _solve(s, j, w)
    return float(1.0 / abs(A_in)**2)       # no clip: see DERIVATION section 1


def transmission(s, j, w):
    s = float(s)
    j = float(j)
    w = float(w)
    if w <= 0.0:
        return 0.0
    if j < s - 1e-12:
        return 0.0
    return _transmission(s, j, w)


def _lowest_j(s):
    return float(s)


def absorption_sum(s, w, rel=1e-12):
    s = float(s)
    j = _lowest_j(s)
    total = 0.0
    bc = 3.0 * math.sqrt(3.0)          # capture impact parameter, DERIVATION section 5
    while True:
        t = (2 * j + 1) * transmission(s, j, w)
        total += t
        if j + 0.5 > bc * w + 3 and t < rel * max(total, 1e-300):
            break
        j += 1.0
    return total


def _gl_nodes(n, a, b):
    x, wt = np.polynomial.legendre.leggauss(n)
    return 0.5 * (b - a) * x + 0.5 * (b + a), 0.5 * (b - a) * wt


def _occupation(s, w):
    x = w / T_HAWKING
    return 1.0 / math.expm1(x) if not _is_fermion(s) else 1.0 / (math.exp(x) + 1.0)


def _power(s, w_max=2.5, nodes=32, edges=(0.0, 0.1, 0.25, 0.5, 1.0), rel=1e-10):
    s = float(s)
    panels = list(edges) + [w_max] if w_max > edges[-1] else [e for e in edges if e < w_max] + [w_max]
    ws, wts = [], []
    for a, b in zip(panels, panels[1:]):
        xx, ww = _gl_nodes(nodes, a, b)
        ws.extend(xx)
        wts.extend(ww)
    ws = np.array(ws)
    wts = np.array(wts)
    occ = np.array([_occupation(s, w) for w in ws])
    total = 0.0
    j = _lowest_j(s)
    while True:
        # nodes whose largest possible contribution (Gamma <= 1) is negligible are skipped
        bound = (2 * j + 1) * wts * ws * occ / (2 * math.pi)
        g = np.array([transmission(s, j, w) if bnd > 1e-3 * rel * max(total, 1e-300) or total == 0.0 else 0.0
                      for w, bnd in zip(ws, bound)])
        contrib = (2 * j + 1) * np.sum(wts * ws * g * occ) / (2 * math.pi)
        total += contrib
        if contrib < rel * total:
            break
        j += 1.0
    return total


@functools.lru_cache(maxsize=None)
def power_per_dof(s):
    return _power(s)


if __name__ == "__main__":

    from scipy.integrate import quad

    # (a) flux identity and stage-1 consistency
    for s, j, w in ((0, 0, 0.3), (0.5, 0.5, 0.3), (1, 1, 0.5), (2, 2, 0.7), (0, 3, 1.0)):
        A_in, A_out, dx = _solve(float(s), float(j), w)
        print(f"flux s={s} j={j} w={w}: |Ain|^2-|Aout|^2 = {abs(A_in)**2 - abs(A_out)**2:.12f}, x(r*_a) err {dx:.1e}")
    # (b) fermion partner potential
    for j, w in ((0.5, 0.05), (0.5, 0.3), (1.5, 0.5), (2.5, 1.0)):
        a, _, _ = _solve(0.5, j, w, sign=+1)
        b, _, _ = _solve(0.5, j, w, sign=-1)
        print(f"fermion j={j} w={w}: Gamma(V+) = {1/abs(a)**2:.10e}, Gamma(V-) = {1/abs(b)**2:.10e}")
    # (c) matching radius and r*_min convergence
    for s, j, w in ((0, 0, 0.005), (2, 2, 0.01), (0.5, 0.5, 0.002), (0.5, 0.5, 0.01), (0.5, 1.5, 0.005),
                    (0.5, 2.5, 0.02), (0.5, 1.5, 0.3), (1, 2, 1.5)):
        s, j = float(s), float(j)
        g0 = 1 / abs(_solve(s, j, w)[0])**2
        g1 = 1 / abs(_solve(s, j, w, R=2 * _match_radius(s, j, w))[0])**2
        g2 = 1 / abs(_solve(s, j, w, rstar_min=2 * RSTAR_MIN)[0])**2
        g3 = 1 / abs(_solve(s, j, w, rstar_min=RSTAR_MIN / 2)[0])**2
        print(f"conv s={s} j={j} w={w}: {g0:.12e}  R*2: {g1/g0-1:.1e}  r*min*2: {g2/g0-1:.1e}  r*min/2: {g3/g0-1:.1e}")
    # (e) limits
    for w in (0.002, 0.005, 0.01):
        print(f"Gamma_00/w^2 at w={w}: {transmission(0, 0, w)/w**2:.5f}")
    for s in (0, 0.5, 1, 2):
        print(f"s={s}: sum(2j+1)Gamma/w^2 at w=1,2,3: " +
              ", ".join(f"{absorption_sum(s, w)/w**2:.4f}" for w in (1.0, 2.0, 3.0)))
    # (d) power: main route and convergence, plus scipy.quad second route
    for s in (0, 0.5, 1, 2):
        p = power_per_dof(s)
        p_wmax = _power(s, w_max=5.0)
        p_nodes = _power(s, nodes=64)
        p_rel = _power(s, rel=1e-13)
        q = 0.0
        j = _lowest_j(float(s))
        while True:
            val, _ = quad(lambda w: w * transmission(s, j, w) * _occupation(s, w) / (2 * math.pi),
                          0.0, 3.0, points=(0.1, 0.3, 0.6, 1.0), limit=200, epsabs=0, epsrel=1e-10)
            c = (2 * j + 1) * val
            q += c
            if c < 1e-11 * q:
                break
            j += 1.0
        print(f"P_{s} = {p:.10e}  w_max*2: {p_wmax/p-1:.1e}  nodes*2: {p_nodes/p-1:.1e}  "
              f"more j: {p_rel/p-1:.1e}  quad route: {q:.10e} ({q/p-1:.1e})")

