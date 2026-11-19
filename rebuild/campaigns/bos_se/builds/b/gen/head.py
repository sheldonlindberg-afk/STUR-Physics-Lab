"""Bosonic one-loop gauge-boson self-energies (gauge, Goldstone, Higgs and ghost loops, no fermions) of the
SU(2)xU(1) electroweak theory in the 't Hooft-Feynman gauge, d = 4 - 2 eps, MS-bar at scale mu.

The loop coefficients below were generated (builds/bos_se-b/gen/*.py) from the Lagrangian: every Feynman rule is
extracted from L (Yang-Mills + Higgs + gauge fixing + ghost terms) by plane-wave multilinear differentiation, every
diagram (bubbles, ghost loops, seagulls) is contracted in d dimensions and reduced to A0, B0 (see DERIVATION.md).
Sigma_T = alpha/(4 pi) * [ sum_i coeff_i * (finite loop function_i) + rational rest ],
A0f(m) = m^2 (1 - ln m^2/mu^2),  B0f(k2; m1, m2) = - int_0^1 dx ln[(x m2^2 + (1-x) m1^2 - x(1-x) k2 - i0)/mu^2]  (real part).
"""
import math
from mpmath import mp, mpf, mpc, log, sqrt, pi, quad, fabs, floor, ceil, log10

PROVENANCE = {
    "sigma_AA": ("derived", "photon bosonic self-energy from the Lagrangian: W, phi, ghost bubbles and seagulls, MS-bar"),
    "sigma_AZ": ("derived", "photon-Z bosonic mixing from the Lagrangian: W, phi, ghost bubbles and seagulls, MS-bar"),
    "sigma_ZZ": ("derived", "Z bosonic self-energy from the Lagrangian: W, phi, H-Z, H-chi, ghost bubbles and seagulls, MS-bar"),
    "sigma_W": ("derived", "W bosonic self-energy from the Lagrangian: all gauge/scalar/ghost bubbles and seagulls, MS-bar"),
}

_TINY = mpf(10) ** (-30)     # k^2 = 0 is evaluated as the limit k^2 -> _TINY * MW^2 (analytic point, working precision raised)


def _J(r):
    """Re int_0^1 ln(x - r) dx = Re[(1-r) ln(1-r) + r ln(-r)] - 1 (r a root of the Feynman-parameter quadratic)."""
    r = mpc(r)
    t = mpf(0)
    if fabs(1 - r) > mpf(10) ** (-(mp.dps // 2)):
        t += ((1 - r) * log(1 - r)).real
    if fabs(r) > mpf(10) ** (-(mp.dps // 2)):
        t += (r * log(-r)).real
    return t - 1


def _A0f(m2, mu2):
    return mpf(0) if m2 == 0 else m2 * (1 - log(m2 / mu2))


def _B0f(k2, a, b, mu2):
    """finite part (Delta removed) of Re B0(k2; sqrt a, sqrt b); k2 != 0."""
    p = b - a - k2
    disc = p * p - 4 * k2 * a
    sq = sqrt(mpc(disc))
    r1 = (-p + sq) / (2 * k2)
    r2 = (-p - sq) / (2 * k2)
    return -(log(fabs(k2)) + _J(r1) + _J(r2)) + log(mu2)


def _prec(k2, mw, mz, mh, mu):
    big = max(mw * mw, mz * mz, mh * mh, fabs(k2), mu * mu)
    small = min(x for x in (mw * mw, mz * mz, mh * mh, fabs(k2), mu * mu) if x > 0)
    return int(70 + 4 * ceil(log10(big / small)))
