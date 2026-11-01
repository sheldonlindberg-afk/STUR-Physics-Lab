#!/usr/bin/env python3
"""
Refinement round 7: a line-by-line audit of the math after rounds 1-6.
See docs/REFINEMENT_R7.md. Requires numpy, scipy. Runs in about 1 min.

Every number this round corrects is recomputed here, so each correction can
be checked by rerunning the script rather than by trusting the prose.

  A1  the sign of beta: what fixes it, and over what region
  A2  tomography (Delta beta) when part of the reionization shell lies in an
      opposite-sign domain
  A3  the nucleation window after R2.4: 1/L < f/197, not f/8
  A4  the range of the 4D gauge coupling g4 = 1/(f L)
  A5  the lightest allowed bulk fermion psi
  A6  how closely the in-script reionization projection matches CLASS
  A7  the seed needed for a timely roll at m = 1e-29 eV
"""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import stur_final as F  # noqa: E402

BAR = "=" * 78
ALPHA_DEG = np.degrees(F.ALPHA)                   # alpha in degrees, 0.4181
HALF = ALPHA_DEG / 2                              # alpha/2 = 0.2091 deg
MPL = 2.435e27                                    # reduced Planck mass, eV

# Inputs fixed by earlier rounds (each is reproduced by its own script).
H_C = 15.06                     # H_c L, de Sitter trigger scale (R2.2, check O5)
LINV_MIN = 875.0                # 1/L lower bound in GeV, conservative (R2.3)
F_MIN = 2.9e9                   # f lower bound in GeV, Chandra (section C)
SEED_3PCT = 0.03 * np.pi        # |theta_i| allowed for beta within 3% (R2.4)
N_EFOLDS = 60
P_OPP_N60 = 0.085               # largest P_opp for N_extra = 60 (R2.4 table)


def f_max_gev(m):
    """domain-wall bound sigma = 8 m f^2 < (1 MeV)^3, returned in GeV"""
    return np.sqrt(1e18 / (8 * m)) / 1e9


def delta_beta(beta_own, beta_rec, f_opp):
    """Sky-averaged reionization angle minus recombination angle.

    A reionization point in our own domain is rotated by beta_own. In an
    opposite domain theta sits at -Theta instead of +Theta, so the rotation
    is (alpha/2pi)(pi + Theta) = alpha - beta_own exactly. The large-scale
    estimator averages over the shell (sin 2 beta ~ 2 beta to 1e-5 here), so
    beta_reio = (1 - f) beta_own + f (alpha - beta_own).
    """
    beta_reio = (1 - f_opp) * beta_own + f_opp * (ALPHA_DEG - beta_own)
    return beta_reio - beta_rec


def a1_sign():
    print(BAR + "\n A1  The sign of beta\n" + BAR)
    th = np.linspace(-np.pi, np.pi, 2001)
    V = 1 + np.cos(th)                              # late-time potential / m^2 f^2
    print(f"   V(theta) = m^2 f^2 (1 + cos theta) is even: max |V(th) - V(-th)|"
          f" = {np.max(np.abs(V - V[::-1])):.0e}")
    print("   -> the brane twist (vartheta = pi) makes theta = 0 a SYMMETRIC hilltop;")
    print("      it does not choose a direction. Each region rolls toward the sign")
    print("      of its own random-walk offset theta_i.")
    rng = np.random.default_rng(1)
    th_i = 1e-3 * rng.standard_normal(100000)       # emission points, recombination
    for th_obs in (np.pi, -np.pi):
        b = np.degrees(F.ALPHA / (2 * np.pi) * (th_obs - th_i))
        print(f"   observer at theta = {th_obs:+.4f}: beta_rec on 1e5 sky points in"
              f" [{b.min():+.4f}, {b.max():+.4f}] deg")
    print("   -> beta_rec has ONE sign on our whole sky (only the observer's theta")
    print("      matters, because theta ~ 0 at every emission point). That sign is")
    print("      set by theta_i in OUR region, not by the brane twist; distant")
    print("      regions of the universe can carry the opposite sign.")


def a2_tomography(R):
    print("\n" + BAR + "\n A2  Tomography with opposite-sign domains\n" + BAR)
    print("   beta_reio = (1 - f) beta_own + f (alpha - beta_own),  f = sky fraction")
    print("   of the reionization shell lying in an opposite domain (R2.4: P_opp).")
    hdr = ["m [eV]", "beta_rec", "beta_own", "f = 0", f"f = {P_OPP_N60}", "f = 0.5"]
    print("   " + "".join(f"{h:>11s}" for h in hdr))
    lo, hi = [], []
    for m in (2e-31, 3e-31, 1e-30, 1e-29, 1e-28):
        _, b_rec, hist = F.roll(m, 1e-4)
        b_own = R.beta_l(hist)[2]
        d = [delta_beta(b_own, b_rec, f) for f in (0.0, P_OPP_N60, 0.5)]
        lo.append(d[0])
        hi.append(d[1])
        print(f"   {m:11.0e}{b_rec:11.4f}{b_own:11.4f}" + "".join(f"{x:11.4f}" for x in d))
    print(f"   -> single domain (f = 0):        Delta beta in [{min(lo):.3f}, {max(lo):.3f}] deg")
    print(f"   -> N_extra >= 60 (f <= {P_OPP_N60}):   Delta beta in [{min(lo):.3f}, {max(hi):.3f}] deg")
    sig = 0.05
    print(f"      LiteBIRD sigma ~ {sig} deg: {abs(max(hi)) / sig:.1f}-{abs(min(lo)) / sig:.1f} sigma"
          " from zero")
    print("   -> Delta beta ~ 0 needs f ~ 0.5: half the reionization shell in an")
    print("      opposite domain. That configuration has its own signature: a")
    print("      large-scale anisotropic rotation with sky rms ~ 0.2 deg and")
    print("      D_2 ~ 0.04e-4 rad^2 (R2.4, N_extra = 0 rows).")
    print("   -> corrected kill criterion: |beta| ~ 0.2 deg with Delta beta ~ 0 AND")
    print("      no large-scale anisotropic reionization rotation falsifies STUR-ROLL.")


def a3_window():
    print("\n" + BAR + "\n A3  Nucleation window after R2.4\n" + BAR)
    h_over_f = 2 * np.pi * SEED_3PCT / np.sqrt(N_EFOLDS)
    ratio = H_C / h_over_f
    print(f"   H_nuc < 2 pi f (0.03 pi)/sqrt({N_EFOLDS}) = {h_over_f:.4f} f   (was 2 f)")
    print(f"   H_nuc > H_c = {H_C}/L   ->   1/L < f/{ratio:.0f}   (was f/8)")
    print(f"   {'f [GeV]':>8s} {'1/L [GeV]':>10s} {'M_f [GeV]':>10s}  old status -> new status")
    for f in (3e9, 1e12, 3e14):
        for linv in (1e3, 1e6, 1e10, 1e13):
            x = -np.log((1e-30 * (f * 1e9) * (1 / (linv * 1e9)) ** 2) ** 2)
            old = "closed" if linv > f / 8 else "allowed"
            new = "closed" if linv > f / ratio else "allowed"
            if linv < LINV_MIN * 1.16:
                new += " (KK edge)"
            flag = "   <- changed" if old != new.split()[0] else ""
            print(f"   {f:8.0e} {linv:10.0e} {x * linv:10.1e}  {old:>7s} -> {new}{flag}")
    return ratio


def a4_g4(ratio):
    print("\n" + BAR + "\n A4  The 4D gauge coupling g4 = 1/(f L) = (1/L)/f\n" + BAR)
    f_top = f_max_gev(2e-31)
    g_lo, g_hi = LINV_MIN / f_top, 1 / ratio
    print(f"   smallest: 1/L = {LINV_MIN:.0f} GeV, f = {f_top:.1e} GeV -> g4 = {g_lo:.1e}")
    print(f"   largest:  1/L = f/{ratio:.0f}                     -> g4 = {g_hi:.1e}")
    print(f"   -> g4 spans {g_lo:.0e} to {g_hi:.0e} (HYPOTHESIS.md said 1e-6 to 1e-11).")
    print(f"      A displaced birth value costs action ~ theta^2/g4^2 >= {1 / g_hi ** 2:.0e}"
          " theta^2:")
    print("      still large, so the conclusion (theta = 0 at birth) is unchanged.")


def a5_lightest_psi():
    print("\n" + BAR + "\n A5  Lightest allowed bulk fermion psi\n" + BAR)
    best = (np.inf, None)
    for m in np.geomspace(2e-31, 1e-28, 40):
        for f in np.geomspace(F_MIN, f_max_gev(m), 40):
            linv = LINV_MIN
            x = -np.log((m * f * 1e9 / (linv * 1e9) ** 2) ** 2)
            if x * linv < best[0]:
                best = (x * linv, (m, f, x))
    m, f, x = best[1]
    print(f"   M_f = (M_f L)/L with m^2 f^2 ~ e^(-M_f L)/L^4, 1/L = {LINV_MIN:.0f} GeV")
    print(f"   minimum M_f = {best[0]:.2e} GeV  (m = {m:.0e} eV, f = {f:.1e} GeV,"
          f" M_f L = {x:.0f})")
    print("   -> 'M_f >~ 1.4e5 GeV' should read 'M_f >~ 1.2e5 GeV' (log accuracy).")


def a6_reion_vs_class(R):
    print("\n" + BAR + "\n A6  In-script reionization projection vs CLASS (l <= 4)\n" + BAR)
    cls = {1e-31: (0.1244, 0.1632, 0.1850), 3e-31: (0.0212, 0.0349, 0.0494),
           1e-30: (0.0000, 0.0009, 0.0023)}
    worst = 0.0
    for m, row in cls.items():
        b = R.beta_l(F.roll(m, 1e-4)[2])
        d = [b[l] - c for l, c in zip((2, 3, 4), row)]
        worst = max(worst, max(abs(v) for v in d))
        print(f"   m = {m:.0e}: Reion - CLASS at l = 2, 3, 4: "
              + ", ".join(f"{v:+.4f}" for v in d))
    print(f"   -> max |difference| = {worst:.4f} deg; the docs' '<= 0.004 deg'"
          " should read '<= 0.005 deg'.")


def a7_seed():
    print("\n" + BAR + "\n A7  Seed needed for a timely roll at m = 1e-29 eV\n" + BAR)
    worst = 0.0
    for sd in (1e-20, 1e-40, 1e-60, 1e-80):
        fr = F.roll(1e-29, sd)[0]
        worst = max(worst, abs(fr - 1))
        print(f"   seed {sd:.0e}: lands at {fr:.4f} pi")
    print(f"   -> every seed down to 1e-80 lands within {100 * worst:.1f}% of pi;")
    print("      stur_final's '>~ 1e-40 (m = 1e-29)' is conservative, not wrong.")


def main():
    R = F.Reion()
    a1_sign()
    a2_tomography(R)
    ratio = a3_window()
    a4_g4(ratio)
    a5_lightest_psi()
    a6_reion_vs_class(R)
    a7_seed()


if __name__ == "__main__":
    main()
