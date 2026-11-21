"""Auditor's independent grey-body solver (different far-field route from both builds).

Near horizon: t = ln(r-2) variable, ingoing BC with the auditor's own leading correction
  bosons  u = 1 + c f,      c = V1/(1/4 - i w),  V1 = L/4 + kappa/8
  fermions u = 1 + d sqrt f, d = sigma k/(8 (1/16 - i w/2))   (V ~ sigma k sqrt(f)/8 at r = 2, sqrt f ~ e^{r*/4})
Far field: NO asymptotic series. Local WKB projection at radius R with k(r) = sqrt(w^2 - V):
  |A_in|^2 = k |psi - psi'/(i k) + (k'/(2 i k^2)) psi|^2 / (4 w)    (first-order adiabatic projection)
and Richardson-free convergence check by R -> 2R. Gamma = 1/|A_in|^2.
"""
import math, cmath
import numpy as np
from scipy.integrate import solve_ivp


def V_and_dV(s, j, r, sigma=+1):
    """V(r) and dV/dr* (analytic)."""
    f = 1 - 2 / r
    fr = 2 / r**2
    if abs(s - 0.5) < 1e-12:
        k = j + 0.5
        sf = math.sqrt(f)
        # V = k^2 f / r^2 + sigma k sqrt(f) (3/r^3 - 1/r^2)
        V = k * k * f / r**2 + sigma * k * sf * (3 / r**3 - 1 / r**2)
        dVdr = k * k * (fr / r**2 - 2 * f / r**3) + sigma * k * (fr / (2 * sf) * (3 / r**3 - 1 / r**2) + sf * (-9 / r**4 + 2 / r**3))
    else:
        L = j * (j + 1)
        kap = 2 * (1 - s * s)
        U = L / r**2 + kap / r**3
        dU = -2 * L / r**3 - 3 * kap / r**4
        V = f * U
        dVdr = fr * U + f * dU
    return V, f * dVdr


def gamma(s, j, w, R=None, x0=1e-12, sigma=+1, rtol=1e-12):
    fermion = abs(s - 0.5) < 1e-12
    if R is None:
        leff = (j + 0.5) ** 2 if fermion else j * (j + 1)
        R = max(400.0 / w, 40.0 * math.sqrt(leff + 1) / w, 100.0)
    r0 = 2 + x0
    f0 = x0 / r0
    rs0 = r0 + 2 * math.log(x0 / 2)
    e = cmath.exp(-1j * w * rs0)
    if fermion:
        k = j + 0.5
        d = sigma * k / (8 * (1 / 16 - 0.5j * w))
        sf = math.sqrt(f0)
        u, du = 1 + d * sf, d * sf / 4          # d(sqrt f)/dr* = sqrt f * f_r/2 -> sqrt f /4 at horizon
    else:
        L = j * (j + 1); kap = 2 * (1 - s * s)
        c = (L / 4 + kap / 8) / (0.25 - 1j * w)
        u, du = 1 + c * f0, c * f0 / 2
    psi0 = e * u
    dpsi0 = e * (-1j * w * u + du)

    # t = ln(r - 2): d psi/dt = (r/1) * psi_{r*} * (dr*/dr * dr/dt) ... dr/dt = x, dr*/dr = 1/f = r/x -> dr*/dt = r
    def rhs(t, y):
        x = math.exp(t); r = 2 + x
        V, _ = V_and_dV(s, j, r, sigma) if r > 2.5 else (_Vx(s, j, x, sigma), 0)
        return [r * y[1], r * (V - w * w) * y[0]]

    sol = solve_ivp(rhs, (math.log(x0), math.log(R - 2)), [psi0, dpsi0], method="DOP853", rtol=rtol, atol=1e-16)
    psi, dpsi = sol.y[0, -1], sol.y[1, -1]
    V, dV = V_and_dV(s, j, R, sigma)
    kk = math.sqrt(w * w - V)
    kp = dV / (2 * kk)          # dk/dr*
    # WKB: psi = a e^{-iS}/sqrt(k) + b e^{+iS}/sqrt(k); psi' = (-ik - k'/2k) a.. + (ik - k'/2k) b..
    # => a-part = [ (ik - k'/2k) psi - psi' ] / (2ik)
    am = ((1j * kk - kp / (2 * kk)) * psi - dpsi) / (2j * kk)
    Ain2 = abs(am) ** 2 * kk / w
    return 1 / Ain2


def _Vx(s, j, x, sigma):
    r = 2 + x; f = x / r
    if abs(s - 0.5) < 1e-12:
        k = j + 0.5
        return k * k * f / r**2 + sigma * k * math.sqrt(f) * (3 / r**3 - 1 / r**2)
    return f * (j * (j + 1) / r**2 + 2 * (1 - s * s) / r**3)


if __name__ == "__main__":
    for s, j, w in ((0, 0, 0.2), (1, 1, 0.2), (2, 2, 0.4), (0.5, 0.5, 0.1)):
        g1 = gamma(s, j, w); g2 = gamma(s, j, w, R=2 * max(400 / w, 100)); g3 = gamma(s, j, w, sigma=-1) if s == 0.5 else g1
        print(s, j, w, g1, g2 / g1 - 1, g3 / g1 - 1)
