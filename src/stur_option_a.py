#!/usr/bin/env python3
"""
Option A: spacetime records which-path information - the minimal STUR model.

STUR POSTULATE (the only new structure): the gravitational potential (per unit
mass) carries Gaussian noise, white in time, whose spatial variogram follows
STUR's area law (linear 'string-like' growth), regularised at a scale xi:

    <Phi(x,t) Phi(y,t')> = delta(t-t') C(x-y),
    V(dx) = 2[C(0) - C(dx)] = 2 kappa ( sqrt(dx^2 + xi^2) - xi )

FOLLOWS (Gaussian Wilson loop of the connection A_0 = m Phi / hbar):
    Gamma = -ln(V/V0) = (1/2)(m/hbar)^2 Int V(dx(t)) dt
          -> (m/hbar)^2 kappa A_st      for dx >> xi,   A_st = Int dx(t) dt
    i.e. STUR line 1 + line 6 with A_mu = gravitational potential: visibility loss
    = tension x enclosed SPACETIME AREA x mass^2 (no saturation in dx, unlike
    Diosi-Penrose / CSL, whose rates saturate for dx >> their length scale).

FOLLOWS (same noise kicks matter): force noise F = -m grad Phi gives momentum
diffusion d<p^2>/dt = m^2 kappa / xi per axis, so heating per unit MASS
    P/M = 3 kappa / (2 xi)       (independent of how matter is grouped)

Constraints (LIT inputs, not recomputed):
  Kovachy et al., Nature 528, 530 (2015): Rb-87, arm separation 0.54 m, T = 1.04 s
     -> require Gamma <= 1 (conservative: interference was observed).
  Earth's internal heat flow 47 TW (Davies & Davies 2010), M_E = 5.97e24 kg
     -> require P/M below the total, i.e. 3 kappa/(2 xi) < 47 TW / M_E.
"""
import numpy as np

hbar = 1.054571817e-34
amu = 1.66053906660e-27


def banner(s):
    print("\n" + "=" * 78 + "\n" + s + "\n" + "=" * 78)


def gamma(m_amu, kappa, A_st):
    return (m_amu * amu / hbar) ** 2 * kappa * A_st


def A_mz(dx_max, T):
    """Enclosed spacetime area of a symmetric Mach-Zehnder: arms separate linearly
    for T and recombine over T -> triangle of base 2T, height dx_max."""
    return dx_max * T


def check_profile():
    """Numerical check of the dx >> xi limit against the full variogram."""
    xi, kappa, T, dxm = 1e-6, 1.0, 1.0, 0.5
    t = np.linspace(0, 2 * T, 200001)
    dx = dxm * (1 - abs(t - T) / T)
    full = 0.5 * np.trapezoid(2 * kappa * (np.sqrt(dx**2 + xi**2) - xi), t)
    return full / (kappa * A_mz(dxm, T))


def main():
    banner("A1  Model check: area law of the gravitational Wilson loop")
    print(f"   full variogram integral / (kappa A_st) for xi = 1 um, dx_max = 0.5 m: {check_profile():.6f}")

    banner("A2  Constraint 1: interference at half-metre separation (Kovachy et al. 2015)")
    A_K = A_mz(0.54, 1.04)
    kappa_max = 1.0 / ((87 * amu / hbar) ** 2 * A_K)
    print(f"   A_st = {A_K:.3f} m s,  Gamma <= 1  =>  kappa <= {kappa_max:.3e} m^3/s^3")
    print(f"   equivalently Gamma per amu^2 per (m s) <= {1/(87**2*A_K):.3e}")

    banner("A3  Constraint 2: heating of matter (Earth's heat flow)")
    pm = 47e12 / 5.97e24
    print(f"   Earth heat flow per kg = {pm:.3e} W/kg")
    xi_min = 1.5 * kappa_max / pm
    print(f"   3 kappa/(2 xi) < {pm:.2e}  =>  at kappa = kappa_max:  xi > {xi_min:.3e} m")
    print("   (xi >> atom size, so the noise acts coherently on each atom: Gamma ~ m^2 holds)")

    banner("A4  Predicted signal at the largest still-allowed kappa (illustrative geometries)")
    print("   NOT instrument specifications: arm separation dx_max and time T are illustrative.")
    for name, m, dxm, T in [("Kovachy 2015 (bound, Rb-87)", 87, 0.54, 1.04),
                            ("MAGIS/AION-class, Sr-87", 87, 1.0, 2.0),
                            ("MAGIS/AION-class, Sr-87", 87, 3.0, 4.0),
                            ("km-scale (AION-km class), Sr-87", 87, 10.0, 10.0)]:
        A = A_mz(dxm, T)
        G = gamma(m, kappa_max, A)
        print(f"   {name:34s} dx={dxm:5.2f} m T={T:5.1f} s  A_st={A:7.2f} m s  Gamma={G:8.2f}"
              f"  contrast factor {np.exp(-G):.2e}")
    print("\n   Reach: a contrast measured to dV at area A bounds kappa <= dV / ((m/hbar)^2 A):")
    for dV, A in [(1e-2, 2.0), (1e-3, 12.0)]:
        print(f"     dV = {dV:.0e}, A = {A:5.1f} m s  ->  kappa <= {dV/((87*amu/hbar)**2*A):.2e}"
              f"  ({dV/((87*amu/hbar)**2*A)/kappa_max:.1e} x today's bound)")

    banner("A4b  Does any natural scale put kappa in the window? (dimensional benchmarks only)")
    c, G = 2.99792458e8, 6.67430e-11
    lP = np.sqrt(hbar * G / c**3)
    RH = c / (67.4e3 / 3.0857e22)
    for name, k in [("c^3 (Planck-scale tension, no suppression)", c**3),
                    ("c^3 lP / R_Hubble (holographic suppression)", c**3 * lP / RH),
                    ("c^3 (lP / R_Hubble)^(1/2)", c**3 * np.sqrt(lP / RH))]:
        print(f"   {name:46s} kappa = {k:9.2e}   / today's bound = {k/kappa_max:9.2e}")
    print("   -> none is derived; kappa is a FREE parameter of option A, as any collapse-model rate is.")

    banner("A5  Signatures that separate this from standard decoherence and collapse models")
    print("   (1) Gamma linear in enclosed spacetime area: doubling dx_max at fixed T doubles Gamma.")
    print("       Gas collisions, blackbody scattering, CSL and Diosi-Penrose all SATURATE in dx.")
    print("   (2) Gamma ~ m^2 across species at equal geometry:")
    for sp, m in [("Rb-87", 87), ("Sr-88", 88), ("Cs-133", 133), ("Yb-174", 174)]:
        print(f"       {sp:7s} Gamma / Gamma(Sr-87) = {(m/87)**2:.3f}")
    print("   (3) Independent of internal state, temperature and vacuum pressure.")
    print("   (4) Heats all matter at 3 kappa/(2 xi) per kg - a second, independent test.")
    print("   (5) If xi > dx_max the area law degrades to Gamma = (m/hbar)^2 kappa Int dx^2 dt / (2 xi):")
    xi = 10.0
    t = np.linspace(0, 4.0, 400001); dx = 1.0 * (1 - abs(t - 2.0) / 2.0)
    full = 0.5 * (87 * amu / hbar) ** 2 * kappa_max * np.trapezoid(2 * (np.sqrt(dx**2 + xi**2) - xi), t)
    print(f"       e.g. xi = {xi} m, dx_max = 1 m, T = 2 s: Gamma = {full:.3f} (vs {gamma(87, kappa_max, 2.0):.2f} for xi << dx)")


if __name__ == "__main__":
    main()
