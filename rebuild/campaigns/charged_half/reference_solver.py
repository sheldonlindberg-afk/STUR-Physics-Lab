"""Orchestrator's independent reference for the charged spin-1/2 emission campaign (HIDDEN: never exported).

Massless Dirac field of charge q e on Schwarzschild (M = 1) in the Coulomb potential of the hole's charge Q = n e: with g = alpha q n (potential energy g/r), the
Chandrasekhar-Page radial system (d/dr* -+ i (w - g/r)) R_-+ = W R_+- , W = (j + 1/2) sqrt(f)/r.  Amplitude variables R_+ = a e^{-i phi}, R_- = b e^{+i phi},
phi = w r* - g ln(r - 2); |a|^2 - |b|^2 is conserved, the regular horizon solution has a = 1, b = 0, so Gamma = 1/(1 + |b_inf|^2).
Variable x = ln(r - 2): da/dx = kappa b e^{2 i phi}, db/dx = kappa a e^{-2 i phi}, kappa = (j + 1/2) e^{x/2} / sqrt(2 + e^x), phi(x) = w e^x + (2 w - g) x + const.
"""
import math
import numpy as np
from scipy.integrate import solve_ivp


def gamma(j, w, g, rmax_w=3000.0, rtol=1e-12):
    """Transmission probability of partial wave j (half-integer) at energy w (units 1/M) for coupling g = alpha q n."""
    jj = j + 0.5
    x0 = -40.0
    kap = lambda x: jj * math.exp(x / 2) / math.sqrt(2 + math.exp(x))
    ph = lambda x: w * math.exp(x) + (2 * w - g) * x
    dph = lambda x: w * math.exp(x) + (2 * w - g)
    b0 = kap(x0) * np.exp(-2j * ph(x0)) / (-2j * dph(x0))             # adiabatic first correction at the horizon (a = 1)
    x1 = math.log(max(rmax_w / w, 50.0))

    def rhs(x, y):
        a, b = y
        e = np.exp(2j * ph(x))
        k = kap(x)
        return [k * b * e, k * a / e]

    sol = solve_ivp(rhs, [x0, x1], [1.0 + 0j, b0], method="DOP853", rtol=rtol, atol=1e-14)
    a, b = sol.y[0, -1], sol.y[1, -1]
    # first-order asymptotic tail correction (phi' = (w r - g)/(r - 2) in r, = dph in x)
    k, d, e = kap(x1), dph(x1), np.exp(2j * ph(x1))
    bi = b + k * a / e / (2j * d)
    ai = a - k * b * e / (2j * d)
    return float(1.0 / (abs(ai) ** 2)) if False else float((abs(ai) ** 2 - abs(bi) ** 2) / abs(ai) ** 2 * 0 + 1.0 / (1.0 + abs(bi) ** 2))
