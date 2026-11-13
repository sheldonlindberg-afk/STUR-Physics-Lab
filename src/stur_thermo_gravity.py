#!/usr/bin/env python3
"""
Gravity as an equation of state: the noise it must carry, and what that noise predicts.

D3 (Jacobson) obtains Einstein's equation as an equation of state of vacuum entanglement.
Read literally, gravity would then be a statistical, classical field sourced by the
quantum matter (lambda = 0). A classical field that responds to quantum matter without
breaking quantum mechanics has to carry noise, and that noise decoheres matter.

Q1  The minimum noise (FOLLOWS; LIT: Tilloy & Diosi, PRD 93,
    024026 (2016)). Matter's mass density m(x) is continuously monitored with strength
    k(q). The record has noise 1/(4k), so the potential inferred from it,
    Phi = -G K * m with K(q) = 4 pi / q^2, has noise S_Phi = G^2 K^2 / (4k). That
    noisy potential dephases matter as well. The total decoherence kernel is
          k(q) + S_Phi(q) / hbar^2  =  k + G^2 K^2 / (4 hbar^2 k)  >=  G K / hbar
    with equality at one k. The bound holds at every wavenumber, and its minimum is the
    Diosi-Penrose kernel 4 pi G / (hbar q^2). (Tilloy and Diosi, eqs. (41)-(42): the minimum
    is at kappa = 2, where back-action doubles the original DP decoherence. Whether this
    kernel is the original DP rate or the doubled one depends on the normalization of the
    decoherence term; not resolved here, see AUDIT.md.) So every Markovian statistical gravity
    decoheres at least as fast as Diosi-Penrose. The only freedom is R0, the length
    over which the mass density that sources the field is smeared:
          k_min(q) = (4 pi G / hbar q^2) exp(-q^2 R0^2)

Q2  What R0 is (an assumption of this argument). An equation of state is defined only above the scale at which
    its microscopic degrees of freedom are counted. In D1-D3 that scale is the cutoff a
    of the area law: a = sqrt(N c_s / pi) l_P, from 0.31 l_P (N = 1) to 9.8 l_P
    (N = 1000). The framework contains no other length.

Q3  The consequence. The same noise heats every nucleus (FOLLOWS):
          P / mass = hbar G / (4 sqrt(pi) R0^3)        (point nuclei; R0 >> 1 fm)
    Real nuclei are ~1e-15 m across, so for R0 below that the nucleus's own size sets
    the smearing: P / mass = 2 pi hbar G Int rho_hat^2, with rho_hat the normalised
    density of one nucleus smeared by R0 (src/stur_oppenheim.py P4). At R0 = a this is
    0.5 W per kilogram, not the point-nucleus 1e60 (an earlier version of this script
    quoted the latter). The Earth's internal heat flow is 7.9e-12 W/kg, so matter would
    still be heated 6e10 times faster than anything observed, and the radiation such
    heating produces bounds R0 >= 0.54 Angstrom (LIT: Donadi et al., Nature Physics 17,
    74 (2021)), which is 10^24 cutoff lengths. So a statistical gravity smeared at the
    framework's own cutoff is excluded, and within the framework, under that
    identification (R0 = a) and for Markovian dynamics, its field follows each branch
    (lambda = 1). D6 follows on those two conditions.

Q4  The prediction that remains for any statistical gravity with an R0 put in by hand,
    for the design-A diamond (1.5e-14 kg, R = 1.007 um, split 721 um, 3.2 s), and the
    smearing length it would need to survive.
"""
import numpy as np
from scipy.optimize import minimize_scalar, brentq
from scipy.special import erf

G, hbar, c = 6.67430e-11, 1.054571817e-34, 2.99792458e8
lP = np.sqrt(hbar * G / c**3)
c_s = 0.3046
u = 1.66053906660e-27

import stur_gravity_full as GF
_A = GF.design_a()
M_A, R_A, D_A, T_A = _A["m"], _A["R"], _A["dx"], _A["total"]   # design A, from src/stur_gravity_full.py
R0_DONADI = 0.54e-10          # LIT: Donadi et al. 2021
L_ISL = 52e-6                 # LIT: Lee et al., PRL 124, 101101 (2020): tested down to 52 um


def banner(s):
    print("\n" + "=" * 78 + "\n" + s + "\n" + "=" * 78)


def total_kernel(k, q):
    K = 4 * np.pi / q**2
    return k + (G * K) ** 2 / (4 * hbar**2 * k)


def min_total_kernel(q):
    """Numerically minimise the total decoherence kernel over the monitoring strength."""
    K = 4 * np.pi / q**2
    k0 = G * K / (2 * hbar)
    res = minimize_scalar(lambda lk: total_kernel(np.exp(lk), q),
                          bracket=(np.log(k0) - 3, np.log(k0) + 3), tol=1e-12)
    return res.fun, np.exp(res.x) / k0


def cutoff(N):
    return np.sqrt(N * c_s / np.pi) * lP


def heating_per_kg(R0):
    """Point nuclei smeared by a Gaussian R0 (valid for R0 >> 1 fm)."""
    return hbar * G / (4 * np.sqrt(np.pi) * R0**3)


EARTH_W_PER_KG = 47e12 / 5.972e24   # LIT: 47 +- 2 TW (Davies & Davies, Solid Earth 1, 5 (2010)); M = GM_E/G (IAU)


def heating_per_kg_nuclei(R0, A=12):
    """Carbon nuclei as uniform spheres of radius 1.2 A^(1/3) fm, smeared by R0."""
    from stur_oppenheim import int_rho2_sphere, nuclear_radius
    return 2 * np.pi * hbar * G * int_rho2_sphere(nuclear_radius(A), R0)


def sphere_ff(x):
    x = np.asarray(x, float)
    out = np.ones_like(x)
    s = x > 1e-4
    xs = x[s]
    out[s] = 3 * (np.sin(xs) - xs * np.cos(xs)) / xs**3
    out[~s] = 1 - x[~s] ** 2 / 10
    return out


def rate(R0, m=M_A, R=R_A, d=D_A, n=4_000_000):
    """Decoherence rate of two branches of a uniform sphere, kernel k_min (Q1)."""
    qmax = 40 / R if R0 < R else 12 / R0
    q = np.linspace(qmax / n, qmax, n)
    f = sphere_ff(q * R) ** 2 * np.exp(-(q * R0) ** 2) * (1 - np.sin(q * d) / (q * d))
    return 2 * G * m**2 / (np.pi * hbar) * np.trapezoid(f, q)


def rate_point_gauss(R0, m=M_A, d=D_A):
    """R0 >> R limit: two Gaussian-smeared points (analytic)."""
    return G * m**2 / hbar * (1 / (np.sqrt(np.pi) * R0) - erf(d / (2 * R0)) / d)


def main():
    banner("Q1  The minimum noise of a statistical gravity")
    print("   q (1/m)     min over k of total kernel / (4 pi G / hbar q^2)    k at minimum / (GK/2hbar)")
    worst = 0.0
    for q in (1e2, 1e6, 1e10, 1e14):
        val, kk = min_total_kernel(q)
        r = val / (4 * np.pi * G / (hbar * q**2))
        worst = max(worst, abs(r - 1))
        print(f"   {q:8.0e}    {r:.12f}                                     {kk:.6f}")
    print(f"   The minimum is the Diosi-Penrose kernel at every q (largest deviation {worst:.1e}).")
    r0 = rate(0.0)
    exact = G * M_A**2 / hbar * (6 / (5 * R_A) - 1 / D_A)
    print(f"   Design-A diamond, R0 -> 0: {r0:.2f} /s   (closed form (Gm^2/hbar)(6/5R - 1/d) = {exact:.2f} /s)")

    banner("Q2  The framework's only length: the entanglement cutoff a")
    for N in (1, 10, 100, 1000):
        print(f"   N = {N:5d} fields:  a = {cutoff(N)/lP:5.2f} l_P = {cutoff(N):.2e} m")

    banner("Q3  The heating that noise would cause, per kilogram of any matter")
    print("   R0                  point nuclei        carbon nuclei of finite size (2.75 fm)")
    for lab, R0 in (("a (N = 1)   ", cutoff(1)), ("a (N = 1000)", cutoff(1000)),
                    ("0.54 Angstrom", R0_DONADI)):
        print(f"   R0 = {lab:13s}  {heating_per_kg(R0):.1e} W/kg       {heating_per_kg_nuclei(R0):.2e} W/kg")
    print("   The point-nucleus figure (1e56-1e60 W/kg at R0 = a) ignores the nucleus's size. With")
    print(f"   it, smearing at R0 = a gives {heating_per_kg_nuclei(cutoff(1)):.2f} W/kg. At 0.54 Angstrom (the bound from radiation,")
    print("   LIT) the two formulas agree.")
    print(f"   Required R0 / a (N = 1000): {R0_DONADI / cutoff(1000):.1e}")
    print(f"   For scale: the Earth's internal heat flow is {EARTH_W_PER_KG:.1e} W/kg (LIT), so the")
    print(f"   cutoff-smeared noise would heat matter {heating_per_kg_nuclei(cutoff(1))/EARTH_W_PER_KG:.0e} times faster than anything observed.")
    print("   So gravity cannot be a Markovian statistical field coarse-grained at the framework's own")
    print("   cutoff. On those two conditions (R0 = a, Markovian) its field follows each branch:")
    print("   lambda = 1, and D6 follows from D1-D3. With R0 put in by hand, Q4 applies.")

    banner("Q4  Any statistical gravity with R0 put in by hand: the one-diamond prediction")
    print("   R0            rate (/s)    survival exp(-rate x 3.24 s)")
    for R0 in (R0_DONADI, 1e-7, 1e-6, 1e-5, L_ISL, 2e-4, 1e-3):
        g = rate(R0)
        print(f"   {R0:9.2e} m   {g:10.3e}   {np.exp(-g*T_A):.3e}")
    for R0 in (2e-4, 1e-3):
        print(f"   check, R0 = {R0:.0e} m, Gaussian-point formula: {rate_point_gauss(R0):.3e} /s")
    R_need = brentq(lambda r: rate(r) * T_A - 0.1, 1e-6, 1e-1)
    print(f"   To keep 90% coherence for 3.24 s, a statistical gravity needs R0 > {R_need*1e6:.0f} um.")
    print(f"   Smearing the source of gravity over R0 softens Newton's law at separations ~R0;")
    print(f"   the inverse-square law holds down to {L_ISL*1e6:.0f} um (LIT). So a design-A")
    print("   diamond that stays coherent for 3.24 s leaves no Markovian statistical gravity standing.")
    return R_need


if __name__ == "__main__":
    main()
