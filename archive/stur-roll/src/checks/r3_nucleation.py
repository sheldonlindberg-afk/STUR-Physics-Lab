#!/usr/bin/env python3
"""
Refinement round 3, item 3: constraints on the nucleation (de Sitter) phase.
See docs/REFINEMENT_R3.md. Requires numpy. Runs in < 1 s.

Inputs used (all from earlier rounds or stur_final.py):
  H_c = 15.06 / L                    scalar dominates on dS above this (R2.2)
  1/L >= 0.88 TeV                     KK hypercharge bound (R2.3, Run 2+3)
  f   >= 2.9e9 GeV                    Chandra NGC 1275 (section C)
  f   <= sqrt(1e18 eV^3 / (8 m))      domain-wall bound (section C)
  |theta_i| ~ s0 sqrt(N), s0 = H/(2 pi f); beta within 3% of alpha/2
        -> s0 sqrt(N) <= 0.03 pi      (R2.4)
  tensor modes: r = 2 H^2 / (pi^2 M_Pl^2 A_s);  r < 0.036 (BICEP/Keck 2021)
"""
import numpy as np

MPL = 2.435e18          # reduced Planck mass, GeV
AS = 2.1e-9             # scalar amplitude (Planck 2018)
HC_L = 15.06            # H_c * L  (R2.2)
LINV_MIN = 875.0        # GeV, 1/L lower bound (R2.3, conservative Run 2+3)
F_MIN = 2.9e9           # GeV
TOL = 0.03 * np.pi      # max |theta_i| for 3 % accuracy
BAR = "=" * 78


def f_max(m_ev):
    return np.sqrt(1e18 / (8 * m_ev)) / 1e9      # GeV


def h_from_r(r):
    return np.pi * MPL * np.sqrt(AS * r / 2)


def r_from_h(h):
    return 2 * h ** 2 / (np.pi ** 2 * MPL ** 2 * AS)


def window(f, linv, n_efold):
    lo = HC_L * linv                             # H_nuc > H_c
    hi = 2 * np.pi * f * TOL / np.sqrt(n_efold)  # seed accuracy
    return lo, hi


def main():
    print(BAR + "\n R3.3  The nucleation phase: allowed H_nuc\n" + BAR)
    print("   H_nuc > H_c = 15.06/L            (theta held at 0 when it starts)")
    print("   H_nuc < 2 pi f (0.03 pi)/sqrt(N)  (beta within 3% after N e-folds)")
    print(f"   r < 0.036 (BICEP/Keck)  ->  H_inf < {h_from_r(0.036):.2e} GeV")
    print(f"\n   {'f [GeV]':>9s} {'N':>5s} {'H_min [GeV]':>12s} {'H_max [GeV]':>12s}"
          f" {'r_max':>9s}  status")
    for f in (F_MIN, 1e12, 1e14, 3.5e14):
        for n in (60, 1e3, 1e6):
            lo, hi = window(f, LINV_MIN, n)
            hi = min(hi, h_from_r(0.036))
            st = "open" if hi > lo else "CLOSED"
            print(f"   {f:9.1e} {n:5.0e} {lo:12.2e} {hi:12.2e} {r_from_h(hi):9.1e}  {st}")
    print("\n   -> the window is open for every allowed f, even with 1e6 e-folds.")
    print("   -> a STUR-ROLL nucleation phase predicts r <~ r_max above; for f below")
    print("      ~1e14 GeV this is r <~ 1e-3, i.e. BELOW LiteBIRD's design sensitivity.")
    print("      An r detection by LiteBIRD (r >~ 2e-3) would force f >~ 1e14 GeV.")

    print("\n" + BAR + "\n R3.3b  If the nucleation phase is R^2 (Starobinsky) inflation\n" + BAR)
    for nstar, r in ((55, 0.0035), (60, 0.0030)):
        h = h_from_r(r)
        f_need = h * np.sqrt(60) / (2 * np.pi * TOL)
        m_max = 1e18 / (8 * (f_need * 1e9) ** 2)
        print(f"   N* = {nstar}: r = {r}, H = {h:.2e} GeV -> f > {f_need:.2e} GeV"
              f" (N = 60) -> m < {m_max:.1e} eV")
    print("   -> R^2 inflation as the nucleation phase confines theta's mass to")
    print("      2e-31 <~ m <~ 3e-30 eV (lower end from the alpha/2 window, R2.1),")
    print("      and f to ~2e14-8e14 GeV: a narrow, testable corner. Longer")
    print("      inflation (N > 60) tightens it further: f ~ sqrt(N).")
    for n in (60, 100, 200):
        h = h_from_r(0.0035)
        f_need = h * np.sqrt(n) / (2 * np.pi * TOL)
        print(f"     N = {n:3d}: f > {f_need:.2e} GeV, m < {1e18 / (8 * (f_need * 1e9) ** 2):.1e} eV"
              f"  (needs m > 2e-31: {'ok' if 1e18 / (8 * (f_need * 1e9) ** 2) > 2e-31 else 'CLOSED'})")


if __name__ == "__main__":
    main()
