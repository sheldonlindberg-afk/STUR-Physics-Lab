#!/usr/bin/env python3
"""
Options B and C, pushed until they stop.

B. A new field that couples to neutral atoms and carries STUR's area law (confinement).
   B1 (FOLLOWS): ordinary matter carries net charge under any candidate (B, B-L, ...): a
      confining field would need a string from every unpaired charge to an anti-charge.
      None exists within the Hubble volume, so the confinement length must exceed the
      Hubble radius:  sqrt(sigma_h) < hbar c / R_H.
   B2: inside that bound the field is unconfined (massless-like) in every lab ->
      ordinary fifth force, bounded by MICROSCOPE: |g_{B-L}| < 1.1e-25
      (LIT: Touboul et al. PRL 129, 121102 (2022); Fayet's analysis).
   B3: STUR's observable is VISIBILITY. A static field only shifts the phase (CHECK 2 of
      stur_verify.py: no visibility loss). Fluctuations from a thermal bath of the new
      bosons (FDT, Abraham-Lorentz damping, Markov):
         Gamma_rate = (4/3) alpha_g k_B T dx^2 / (hbar c^2),  alpha_g = (Q g)^2 / (4 pi)
      evaluated at the MICROSCOPE bound, T = 2.725 K (bath no hotter than the CMB), dx
      capped at the bath wavelength hbar c / k_B T (saturation beyond).
C. Modify the horizon row: STUR's 'scale-dependent tension' for horizons, using the KNOWN
   species running (U3): 1/4G(mu) = 1/4G0 + c N mu^2, evaluated at the horizon's own
   scale mu = hbar c / r_s.  Then delta S = c N A / r_s^2 = 4 pi c N: a CONSTANT.
"""
import numpy as np

hbar, c, kB, G, eV = 1.054571817e-34, 2.99792458e8, 1.380649e-23, 6.67430e-11, 1.602176634e-19
H0 = 67.4e3 / 3.0857e22


def banner(s):
    print("\n" + "=" * 78 + "\n" + s + "\n" + "=" * 78)


def main():
    banner("B1  A confining field coupled to ordinary matter's net charge")
    RH = c / H0
    sig = (hbar * c / RH) / eV
    MEarth, mn = 5.97e24, 1.67492749804e-27
    print(f"   Hubble radius {RH:.3e} m  ->  sqrt(sigma_h) < hbar c / R_H = {sig:.2e} eV")
    print(f"   (QCD: 0.44e9 eV.  Earth's net B-L charge ~ {0.5*MEarth/mn:.1e} neutrons, each would")
    print("    need a string; none can end within the Hubble volume.)")
    print("   -> any confinement that ordinary matter feels is longer than the universe:")
    print("      in every experiment the field acts as an UNCONFINED long-range field.")

    banner("B2-B3  The surviving long-range field: fifth-force bound and visibility signal")
    g = 1.1e-25
    Q = 49                                   # B-L charge of Sr-87 (49 neutrons)
    alpha = (Q * g) ** 2 / (4 * np.pi)
    T = 2.725
    lam = hbar * c / (kB * T)
    for dx, t in [(1.0, 4.0), (10.0, 10.0)]:
        dxe = min(dx, lam)
        G_ = (4 / 3) * alpha * kB * T * dxe**2 / (hbar * c**2) * 2 * t
        print(f"   Sr-87, dx = {dx} m (capped at {dxe:.2e} m), 2T = {2*t} s:  Gamma = {G_:.1e}")
    print(f"   alpha_g per atom at the MICROSCOPE bound = {alpha:.1e}")
    print("   Static part: fixed phase, no visibility loss (fringe shift only).")
    print("   -> B gives no STUR visibility signal. As a phase (fifth-force) signal it is the")
    print("      standard ultralight B-L boson search: known physics, nothing STUR-specific.")

    banner("C  Horizon row with STUR's scale-dependent tension (species running)")
    cs = 0.02424                              # per real scalar, computed in stur_unification.py U3
    for N in [1, 10, 100]:
        dS = 4 * np.pi * cs * N
        print(f"   N = {N:3d} scalar-equivalent species:  delta S = 4 pi c N = {dS:7.3f} k_B "
              "(independent of M)")
    Msun = 1.98847e30
    S_sun = 4 * np.pi * G * Msun**2 / (hbar * c)
    print(f"   compare S_BH(1 Msun) = {S_sun:.2e} k_B;  T_H = c^2 dM/dS unchanged since d(delta S)/dM = 0")
    print("   -> no observable: the 'running horizon tension' only shifts S by an M-independent")
    print("      constant. Other horizon corrections (log terms, area quantisation, echoes) are")
    print("      existing proposals from loop/string gravity, not STUR, and need GW data.")


if __name__ == "__main__":
    main()
