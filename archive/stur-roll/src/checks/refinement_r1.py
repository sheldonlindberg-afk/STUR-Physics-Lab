#!/usr/bin/env python3
"""
Refinement round 1: independent checks of the STUR-ROLL chain.
See docs/REFINEMENT_R1.md for the discussion and references.
Requires numpy. Runs in < 2 s.

  R1.1  closed form for the KK-tower coupling c_g(theta, M r)
  R1.2  normalisation chain  L = (k alpha/4 pi) theta F Ftilde  ->  beta
  R1.3  comparison with the hilltop domain-wall prediction of
        Lee, Murai, Takahashi & Yin (PRD 112, 043538, 2025)
  R1.4  bulk-photon constraint on 1/L (the charged bulk fermion needs a
        bulk U(1)_EM), applied to the section E table of stur_final.py
  R1.5  weak-gravity-conjecture check of the U(1)_B sector
"""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from stur_final import ALPHA  # noqa: E402

BAR = "=" * 78


def cg_sum(theta, Mr, N):
    """d/dtheta of sum_n arg(M + i (n + theta/2pi)/r), |n| <= N (as in stur_final)"""
    n = np.arange(-N, N + 1)
    x = theta / (2 * np.pi)
    return np.sum(Mr / (Mr ** 2 + (n + x) ** 2)) / (2 * np.pi)


def cg_exact(theta, Mr):
    """closed form: sum_n a/(a^2 + (n+x)^2) = pi sinh(2 pi a)/(cosh(2 pi a) - cos 2 pi x)"""
    a = 2 * np.pi * Mr
    return 0.5 * np.sinh(a) / (np.cosh(a) - np.cos(theta))


def r1_1():
    print(BAR + "\n R1.1  KK-tower coupling: closed form\n" + BAR)
    print("   c_g(theta) = 1/2 * sinh(2 pi M r) / (cosh(2 pi M r) - cos theta)")
    print("              = 1/2 [1 + 2 e^(-2 pi M r) cos theta + O(e^(-4 pi M r))]")
    print(f"   {'M r':>5s} {'exact':>12s} {'sum N=2e5':>12s} {'sum N=2e7':>12s}"
          f" {'trunc. est.':>12s}")
    for Mr in (0.2, 2.0, 10.0):
        ex = cg_exact(1.0, Mr)
        s5, s7 = cg_sum(1.0, Mr, 200000), cg_sum(1.0, Mr, 20000000)
        tr = Mr / (np.pi * 200000)          # tail of the sum: 2 * Mr / N / (2 pi)
        print(f"   {Mr:5.1f} {ex:12.8f} {s5:12.8f} {s7:12.8f} {ex - tr:12.8f}")
    print("   -> stur_final's 0.49998 at M r = 10 is truncation of the KK sum")
    print("      (tail ~ M r / (pi N)), not physics; the exact value is 1/2 to e^-63.")
    per = np.trapezoid([cg_exact(t, 0.3) for t in np.linspace(0, 2 * np.pi, 20001)],
                       np.linspace(0, 2 * np.pi, 20001))
    print(f"   integral of c_g over one period of theta (M r = 0.3): {per / np.pi:.6f} pi")
    print("   -> exactly pi for ANY M r: the fermion tower shifts the theta-term")
    print("      by pi, not 2 pi, per period; invariance under theta -> theta + 2 pi")
    print("      needs a bare level in Z + 1/2. k_eff = k0 + sgn(M)/2.")
    print("      With one fermion and k0 = +1/2: k_eff = 1 (M > 0) or 0 (M < 0).")
    print("      So 'k = 1 minimal' is equivalently a choice of sign of the bulk mass")
    print("      relative to the bare term; k_eff = 0 (no birefringence) is equally")
    print("      allowed. This is a discrete input, as stur_final states.")


def r1_2():
    print("\n" + BAR + "\n R1.2  Normalisation chain\n" + BAR)
    print("   L = (k alpha / 4 pi) theta F Ftilde,  Ftilde^{mu nu} = 1/2 eps F")
    print("   compare L = -(1/4) g a F Ftilde  ->  g a = -(k alpha / pi) theta")
    print("   rotation of linear polarisation: Delta psi = (g/2) Delta a")
    print("   (Carroll-Field-Jackiw 1990; Harari-Sikivie 1992)")
    print("   -> beta = (k alpha / 2 pi) Delta theta")
    b = np.degrees(ALPHA / (2 * np.pi) * np.pi)
    print(f"   Delta theta = pi, k = 1:  beta = alpha/2 = {b:.5f} deg")
    print("   photon coupling for theta = a/f:  |g| = k alpha / (pi f)  [section C]")


def r1_3():
    print("\n" + BAR + "\n R1.3  Prior art: hilltop domain walls (Lee, Murai, Takahashi, Yin 2025)\n"
          + BAR)
    b = np.degrees(ALPHA) / 2
    print(f"   LMTY abstract: beta ~ 0.21 c_gamma deg, c_gamma ~ 1, hilltop start,")
    print(f"   walls form after recombination.   STUR-ROLL: beta = k alpha/2 = {b:.4f} k deg.")
    print("   Same Lagrangian normalisation, same Delta theta = pi, same number.")
    print("   -> The observable prediction (amplitude, isotropy at recombination,")
    print("      patchy late-time rotation) is NOT new. STUR-ROLL's candidate")
    print("      contribution is a UV origin for the two inputs LMTY assume:")
    print("        (i)  c_gamma = 1 from the 5D parity anomaly (R1.1), and")
    print("        (ii) the hilltop initial condition from the Wilson-line")
    print("             potential flipping sign as the universe cools (step 4).")


def r1_4():
    print("\n" + BAR + "\n R1.4  Bulk photon: the charged bulk fermion needs a bulk U(1)_EM\n"
          + BAR)
    print("   psi is a 5D bulk field with electric charge 1, so the photon (U(1)_Y)")
    print("   must propagate in the bulk. Its KK modes (mass ~ n/L, up to O(1)")
    print("   convention factors) couple to the brane-localised SM fermions with")
    print("   strength ~sqrt(2) e. Literature bounds for gauge KK modes with")
    print("   brane fermions: M_c >~ 4-5 TeV (electroweak precision) and 6.8 TeV")
    print("   (combined fit incl. Tevatron/HERA); LHC dilepton searches are")
    print("   stronger still and must be re-derived for this model.")
    LMIN = 5e3        # GeV, conservative placeholder until a dedicated recast
    print(f"   Applying 1/L > {LMIN:.0e} GeV (placeholder) to the section E grid:")
    print(f"   {'f [GeV]':>8s} {'1/L [GeV]':>10s} {'M_f [GeV]':>10s}  status")
    for f in (3e9, 1e12, 3e14):
        for linv in (1e3, 1e6, 1e10, 1e13):
            x = -np.log((1e-30 * (f * 1e9) * (1 / (linv * 1e9)) ** 2) ** 2)
            st = []
            if linv > f / 8:
                st.append("H_nuc window closed")
            if linv < LMIN:
                st.append("KK photon")
            print(f"   {f:8.0e} {linv:10.0e} {x * linv:10.1e}  "
                  + (", ".join(st) if st else "allowed"))
    print("   -> the stur_final statement 'allowed from 1/L ~ 10 GeV' must be")
    print("      replaced by 1/L >~ few TeV; then M_f >~ 1e5-1e6 GeV and psi is")
    print("      beyond colliders in every allowed row.")


def r1_5():
    print("\n" + BAR + "\n R1.5  Weak gravity conjecture for U(1)_B\n" + BAR)
    print("   Wilson-line axion: theta = g4 L B5,  f = 1 / (g4 L)   (extranatural")
    print("   inflation convention; O(2 pi) factors depend on the circle length).")
    print("   Electric WGC: some state with m <= sqrt(2) g4 q M_Pl  (psi, q = 1).")
    print("   Magnetic WGC: cutoff Lambda <~ g4 M_Pl, must exceed 1/L.")
    mpl = 2.435e18
    print(f"   {'f':>8s} {'1/L':>8s} {'g4':>9s} {'g4 M_Pl':>9s} {'M_f':>9s}  electric magnetic")
    for f in (3e9, 1e12, 3e14):
        for linv in (1e6, 1e10, 1e13):
            if linv > f / 8:
                continue
            g = linv / f
            x = -np.log((1e-30 * (f * 1e9) * (1 / (linv * 1e9)) ** 2) ** 2)
            mf = x * linv
            e_ok = mf <= np.sqrt(2) * g * mpl
            m_ok = g * mpl > linv
            print(f"   {f:8.0e} {linv:8.0e} {g:9.1e} {g * mpl:9.1e} {mf:9.1e}"
                  f"  {'ok' if e_ok else 'FAILS':>8s} {'ok' if m_ok else 'FAILS':>8s}")
    print("   -> g4 M_Pl / M_f = M_Pl / (f x) with x = M_f L ~ 150-250: the electric")
    print("      WGC holds whenever f <~ M_Pl / 250 ~ 1e16 GeV, i.e. throughout the")
    print("      section C window. Not a new constraint, but now checked.")


if __name__ == "__main__":
    r1_1()
    r1_2()
    r1_3()
    r1_4()
    r1_5()
