"""Nucleon polarizabilities from the pion cloud, LO heavy-baryon ChPT, derived in builds/b/DERIVATION.md.

Method: the static nucleon is a source; to O(gA^2) its energy in static fields is
  dE = -(gA^2/(4 f^2)) <0| D_i G D_i^dagger |0>,  G = (m^2 - D^2 - V^2)^-1  (charged-pion zero-frequency operator),
dE = -2 pi alpha_E E^2 - 2 pi beta_M B^2.  Position-space radial integrals are done symbolically (units m_pi = 1).
"""
import math
import functools
import sympy as sp

PROVENANCE = {
    "alpha_E": ("derived", "second order in the pi-N vertex, charged pion in static potential V=eE.x: G0 V^2 G0 term, radial integral"),
    "beta_M": ("derived", "same functional, symmetric gauge A=B x r/2: -G0 e^2A^2 G0 + G0 (eB.L) G0 (eB.L) G0 terms"),
    "to_fm3": ("input", "(hbar c)^3 with hbar c = 197.3269804 MeV fm from SPEC"),
}
HBARC = 197.3269804


@functools.lru_cache(maxsize=1)
def _coefficients():
    """Return (cE, cB): dE_charged = -(gA^2/4f^2) * [cE e^2 E^2 or cB e^2 B^2] / m, exact rationals times 1/pi."""
    r = sp.symbols("r", positive=True)
    p = sp.symbols("p", positive=True)
    G0 = sp.exp(-r) / (4 * sp.pi * r)                      # static Yukawa propagator 1/(p^2+1)
    dG = sp.diff(G0, r)
    # electric: (1/3) int d^3z r^2 G0'^2   (angular average of (E.z)^2 = r^2/3)
    I2 = sp.integrate(4 * sp.pi * r**2 * r**2 * dG**2, (r, 0, sp.oo))
    cE = sp.simplify(I2 / 3)
    # magnetic term 1: -(1/6) int d^3z r^2 G0'^2  (A^2 = B^2 r^2 sin^2/4 -> avg B^2 r^2/6)
    t1 = -I2 / 6
    # magnetic term 2: (<(B.L)^2> summed over the l=1 multiplet = 2 B^2) / 3 * int d^3p/(2pi)^3 p^2/(p^2+1)^3
    P3 = sp.integrate(4 * sp.pi * p**2 * p**2 / (p**2 + 1)**3, (p, 0, sp.oo)) / (2 * sp.pi)**3
    t2 = sp.Rational(2, 3) * P3
    cB = sp.simplify(t1 + t2)
    return float(cE), float(cB)


def _dE_coeff(which, gA, fpi, mpi, alpha):
    c = _coefficients()[0 if which == "E" else 1]
    e2 = 4 * math.pi * alpha
    # dE = -(gA^2/4f^2) c e^2 F^2 / m = -2 pi X F^2
    return gA**2 * c * e2 / (4 * fpi**2 * mpi) / (2 * math.pi)


def alpha_E(gA, fpi, mpi, alpha):
    return _dE_coeff("E", gA, fpi, mpi, alpha)


def beta_M(gA, fpi, mpi, alpha):
    return _dE_coeff("B", gA, fpi, mpi, alpha)


def to_fm3(x):
    return x * HBARC**3


if __name__ == "__main__":
    import numpy as np
    from scipy import integrate
    gA, f, m, al = 1.27, 92.4, 139.57, 1 / 137.035999
    a, b = alpha_E(gA, f, m, al), beta_M(gA, f, m, al)
    print("main  (position space, symmetric gauge): alpha_E = %.4e fm^3, beta_M = %.4e fm^3, ratio %.6f" % (to_fm3(a), to_fm3(b), b / a))
    # route 2: momentum space, Landau gauge A=(0,Bx,0), numeric quadrature, m=1
    def sph(fun):
        # p = tan(u) maps the radial range to a finite interval
        v, _ = integrate.tplquad(lambda ph, th, u: fun(math.tan(u) * math.sin(th) * math.cos(ph), math.tan(u) * math.sin(th) * math.sin(ph), math.tan(u) * math.cos(th)) * math.tan(u)**2 * math.sin(th) / math.cos(u)**2,
                                 0, math.pi / 2, 0, math.pi, 0, 2 * math.pi, epsabs=1e-8, epsrel=1e-8)
        return v / (2 * math.pi)**3
    def dchi(x, y, z, k):      # d/dp_k of chi_i = p_i/(p^2+1), summed squared over i
        q = (x, y, z); D = x * x + y * y + z * z + 1
        return sum(((1.0 if i == k else 0.0) / D - 2 * q[i] * q[k] / D**2)**2 for i in range(3))
    cE2 = sph(lambda x, y, z: dchi(x, y, z, 2))
    cB2 = sph(lambda x, y, z: -dchi(x, y, z, 0) + sum((2 * y * ((1.0 if i == 0 else 0.0) / (x*x+y*y+z*z+1) - 2 * (x, y, z)[i] * x / (x*x+y*y+z*z+1)**2))**2 for i in range(3)) / (x*x+y*y+z*z+1))
    rE = cE2 / _coefficients()[0]; rB = cB2 / _coefficients()[1]
    print("route2 / main coefficient ratios (should be 1): electric %.6f, magnetic %.6f" % (rE, rB))
