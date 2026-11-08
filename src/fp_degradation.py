#!/usr/bin/env python3
"""
Fullness-phase theory, part 2: matter degrades with time itself (postulate P3).

Equation (one constant, tau; energy is conserved, rest mass becomes radiation):
        d rho_m/dt = -3 H rho_m        - rho_m / tau
        d rho_r/dt = -4 H rho_r        + rho_m / tau                              (D)
and gravity (part 1) responds to the total, phi = (rho_m + rho_r) / rho_max.

Bounds on tau computed here:
  D1  Earth's heat.  If degradation inside the Earth ends as heat, the power is M c^2 / tau,
      which cannot exceed the measured surface heat flow, 47 +- 2 TW (LIT, recalled:
      Davies & Davies 2010).  Model-independent apart from "ends as heat".
  D2  Proton decay.  No proton decay seen: tau(p -> e+ pi0) > 2.4e34 yr (LIT, recalled:
      Super-Kamiokande 2020).  Applies if degradation of a proton has a visible channel.
  D3  What that means: fraction of matter degraded since the Big Bang; when degradation
      wins the far-future race; and why it cannot empty a black hole.
"""
import numpy as np

c = 2.99792458e8
YR = 3.15576e7
M_EARTH = 5.972e24
P_EARTH = 47e12            # W, recalled
TAU_P = 2.4e34             # yr, recalled
T_UNIV = 1.38e10           # yr


def banner(s):
    print("\n" + "=" * 78 + "\n" + s + "\n" + "=" * 78)


def earth_bound():
    return M_EARTH * c ** 2 / P_EARTH / YR


def solve_static(tau, t, rho_m0=1.0):
    """CHECK of (D) with H = 0: rho_m = e^{-t/tau}, rho_r = 1 - e^{-t/tau}."""
    from scipy.integrate import solve_ivp
    s = solve_ivp(lambda t, y: [-y[0] / tau, y[0] / tau], [0, t], [rho_m0, 0.0],
                  rtol=1e-12, atol=1e-15)
    return s.y[0, -1], s.y[1, -1]


def main():
    banner("D1-D2  How slow must 'time itself' degrade matter?")
    tb = earth_bound()
    print(f"   Earth: M c^2 = {M_EARTH*c**2:.2e} J, heat flow {P_EARTH/1e12:.0f} TW  ->"
          f"  tau > {tb:.1e} yr")
    print(f"   Proton decay (Super-K, p -> e+ pi0): tau > {TAU_P:.1e} yr  "
          f"({TAU_P/tb:.0e} times stronger)")
    m, r = solve_static(2.0, 1.0)
    print(f"   CHECK (D) static: rho_m = {m:.10f} vs e^-1/2 = {np.exp(-0.5):.10f};"
          f" total = {m+r:.12f}")

    banner("D3  What the bound means")
    frac = T_UNIV / TAU_P
    print(f"   Matter degraded since the Big Bang: < t_U / tau = {frac:.1e}  (unobservable"
          " today).")
    print("   Far-future race (yr):  stars stop forming ~1e14 | degradation ~"
          f"{TAU_P:.0e}+ | solar-mass")
    G, hbar, Msun = 6.67430e-11, 1.054571817e-34, 1.98892e30
    t_hawk = 5120 * np.pi * G ** 2 * Msun ** 3 / (hbar * c ** 4) / YR
    print(f"   black hole evaporates (Hawking, 5120 pi G^2 M^3 / hbar c^4) ~{t_hawk:.0e}.")
    print("   FOLLOWS: degradation erases all free matter long before black holes evaporate.")
    print("   FOLLOWS: it cannot empty a black hole.  Inside the core, rest mass becomes")
    print("   radiation, but gravity counts all energy: phi stays 1 and the mass M is unchanged.")
    print("   Only the expansion of space dilutes radiation (rho_r ~ a^-4) towards 0.  So the")
    print("   user's arc 'to 1, then back to 0' needs BOTH: degradation turns matter into")
    print("   radiation, expansion takes radiation to 0.")
    print("   OPEN: the theory has not yet fixed tau.  If it predicts tau, Hyper-Kamiokande")
    print("   (sensitivity ~1e35 yr, recalled) can test it.")
    return dict(earth=tb, frac=frac)


if __name__ == "__main__":
    main()
