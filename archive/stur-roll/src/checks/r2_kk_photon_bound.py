#!/usr/bin/env python3
"""
Refinement round 2, item 3: bound on the KK hypercharge boson B_Y^(1).
See docs/R2_KK_PHOTON_BOUND.md. Requires numpy. Runs in < 1 s.

Model: only U(1)_Y propagates in the bulk of S^1/Z2 (psi is an SU(2)-singlet
vectorlike lepton, Y = -1); SM fermions and the Higgs live on a fixed point.
KK modes B^(n), n >= 1, couple to brane fields with sqrt(2) g_Y Y.

Approximations (stated, not hidden):
  * narrow width, tree level, massless final states (incl. top);
  * B^(1)-Z mass mixing O(v^2/M^2) ~ 1e-3 neglected;
  * Drell-Yan rate ~ w_u C_u + w_d C_d with the u-ubar : d-dbar luminosity
    ratio w = w_u/w_d scanned over 2-5 (no PDF set is used);
  * no brane-localised kinetic terms (they can soften the couplings).
"""
import numpy as np

S2W = 0.231                     # sin^2 theta_W (MSbar, m_Z)
ALPHA_MZ = 1 / 127.95
E2 = 4 * np.pi * ALPHA_MZ
GY2 = E2 / (1 - S2W)            # g_Y^2 = g'^2
GZ2 = E2 / (S2W * (1 - S2W))    # (g / cos theta_W)^2
BAR = "=" * 78

# hypercharges (Q = T3 + Y) per chirality; (Y_L, Y_R, N_c)
HYP = {"u": (1 / 6, 2 / 3, 3), "d": (1 / 6, -1 / 3, 3),
       "e": (-1 / 2, -1, 1), "nu": (-1 / 2, None, 1)}
# (T3_L, Q) for the SSM Z' (Z-like couplings)
SSM = {"u": (0.5, 2 / 3, 3), "d": (-0.5, -1 / 3, 3),
       "e": (-0.5, -1, 1), "nu": (0.5, 0, 1)}


def c_kk(f):
    yl, yr, _ = HYP[f]
    return 2 * GY2 * (yl ** 2 + (yr ** 2 if yr is not None else 0))


def c_ssm(f):
    t3, q, _ = SSM[f]
    gl, gr = t3 - q * S2W, -q * S2W
    return GZ2 * (gl ** 2 + (gr ** 2 if f != "nu" else 0))


def widths():
    """sum of N_c * (g_L^2 + g_R^2) over 3 generations (+ Higgs doublet for KK)"""
    tot_kk = 3 * sum(HYP[f][2] * c_kk(f) for f in HYP)
    tot_kk += 2 * GY2 * 0.25          # brane Higgs doublet, Y = 1/2 (equiv. thm)
    tot_ssm = 3 * sum(SSM[f][2] * c_ssm(f) for f in SSM)
    return tot_kk, tot_ssm


def ratio(w):
    """sigma x BR(ll) of B^(1) relative to Z'_SSM at the same mass"""
    tk, ts = widths()
    prod = (w * c_kk("u") + c_kk("d")) / (w * c_ssm("u") + c_ssm("d"))
    br = (c_kk("e") / tk) / (c_ssm("e") / ts)
    return prod * br


def main():
    tk, ts = widths()
    print(BAR + "\n R2.3  KK hypercharge boson vs Z'_SSM (narrow width, tree level)\n"
          + BAR)
    print(f"   g_Y^2 = {GY2:.4f}, g_Z^2 = {GZ2:.4f}  (at m_Z; running to 5 TeV ~ few %)")
    print(f"   Gamma/M:  B^(1) = {tk / (24 * np.pi):.3f}   Z'_SSM = {ts / (24 * np.pi):.3f}"
          "   (SSM check: ATLAS/CMS quote ~3%)")
    print(f"   BR(ee):   B^(1) = {c_kk('e') / tk:.3f}   Z'_SSM = {c_ssm('e') / ts:.4f}")
    print(f"   {'w = uu/dd lumi':>16s} {'sigma*BR ratio r':>17s}")
    rs = []
    for w in (2, 3, 4, 5):
        r = ratio(w)
        rs.append(r)
        print(f"   {w:16d} {r:17.2f}")
    rmin = min(rs)
    print(f"   -> r >= {rmin:.1f} > 1 for any w in [2, 5]: at every mass B^(1) gives MORE")
    print("      dilepton signal than Z'_SSM, so the published Z'_SSM limits are")
    print("      conservative lower bounds on M_1 (the limit on sigma*BR is ~flat at")
    print("      high mass: ~0.014 fb at 6 TeV, ATLAS 139 fb^-1).")

    print("\n   Published Z'_SSM limits (95% CL):")
    lims = [("ATLAS Run 2, 139 fb^-1 [N1]", 5.1), ("CMS Run 2, 140 fb^-1 [N2]", 5.15),
            ("ATLAS Run 2+3, 140 + 165 fb^-1 [N3] (preprint)", 5.5)]
    for name, m in lims:
        print(f"     {name:46s} {m:4.2f} TeV")
    print("\n   Estimated gain from r > 1. Empirical slope of the reach: going from")
    print("   Run 2 to Run 2+3 (sensitivity x ~2-3) moved the SSM limit 5.1 -> 5.5 TeV,")
    print("   i.e. d ln(sigma) / dM ~ ln(2-3) / 0.4 TeV ~ 1.7-2.7 per TeV.")
    print(f"   {'slope [1/TeV]':>14s} {'Delta M (r=' + f'{rmin:.1f}' + ')':>16s} {'M_1 estimate':>14s}")
    for s in (1.7, 2.2, 2.7):
        dm = np.log(rmin) / s
        print(f"   {s:14.1f} {dm:13.2f} TeV {5.5 + dm:11.2f} TeV")
    print("   (estimate only: replace with the HEPData sigma*BR limit curve.)")

    print("\n" + BAR + "\n Contact interactions from the whole KK tower\n" + BAR)
    print("   L_eff = -sum_n (2 g_Y^2 / M_n^2) Y_i Y_j (fbar_i g f_i)(fbar_j g f_j),")
    print("   M_n = n M_1, sum 1/n^2 = pi^2/6.  Matching to 4 pi / Lambda^2:")
    print("   Lambda / M_1 = sqrt(12 / (pi g_Y^2 |Y_i Y_j|))")
    for lab, yy in (("u_R e_R", 2 / 3), ("e_R mu_R (LEP RR)", 1.0),
                    ("d_R e_R", 1 / 3), ("e_L mu_L (LEP LL)", 0.25)):
        print(f"     {lab:20s} |Y Y| = {yy:5.3f}   Lambda / M_1 = "
              f"{np.sqrt(12 / (np.pi * GY2 * yy)):5.2f}")
    k = np.sqrt(12 / (np.pi * GY2 * 2 / 3))
    print(f"   ATLAS 139 fb^-1 non-resonant: Lambda up to 35.8 TeV [N4]; applied to the")
    print(f"   strongest channel (u_R e_R) -> M_1 >~ {35.8 / k:.1f} TeV (indicative: ATLAS")
    print("   benchmarks assume u = d universal couplings, B^(1) does not).")
    k2 = np.sqrt(12 / (np.pi * GY2))
    print(f"   LEP-II ll, RR: Lambda > 9.6 / 15.3 TeV (prelim. combination [N5]) ->"
          f" M_1 > {9.6 / k2:.1f} / {15.3 / k2:.1f} TeV")

    print("\n" + BAR + "\n Convention: L in stur_final.py is the covering-circle circumference\n"
          + BAR)
    print("   g_mass(x = M L) carries e^(-M L): the first winding of a mass-M field around")
    print("   a circle of length L. th_ratio uses the same L. So L = 2 pi R and the")
    print("   Z2-even photon tower has M_n = n / R = 2 pi n / L:   1/L = M_1 / (2 pi).")
    best_cons, best_est = 5.5, 5.5 + np.log(rmin) / 1.7
    for name, m in (("conservative (Z'_SSM, Run 2)", 5.1),
                    ("conservative (Z'_SSM, Run 2+3)", best_cons),
                    ("estimate incl. r > 1", best_est)):
        print(f"   {name:32s} M_1 > {m:4.2f} TeV  ->  1/L > {m / (2 * np.pi):.2f} TeV")

    print("\n" + BAR + "\n Section E grid with the sourced bound\n" + BAR)
    lmin = best_est * 1e3 / (2 * np.pi)      # GeV, upper end of the estimate
    print(f"   using 1/L > {lmin:.0f} GeV (estimate; conservative: "
          f"{best_cons * 1e3 / (2 * np.pi):.0f} GeV)")
    print(f"   {'f [GeV]':>8s} {'1/L [GeV]':>10s} {'M_f [GeV]':>10s}  status")
    for f in (3e9, 1e12, 3e14):
        for linv in (1e3, 1e6, 1e10, 1e13):
            x = -np.log((1e-30 * (f * 1e9) * (1 / (linv * 1e9)) ** 2) ** 2)
            st = []
            if linv > f / 8:
                st.append("H_nuc window closed")
            lcons = best_cons * 1e3 / (2 * np.pi)
            if linv < lcons:
                st.append("KK photon")
            elif linv < lmin:
                st.append("edge: allowed (conservative), excluded (estimate)")
            print(f"   {f:8.0e} {linv:10.0e} {x * linv:10.1e}  "
                  + (", ".join(st) if st else "allowed"))
    print("   -> the 1/L = 1 TeV rows sit at the edge (allowed under the conservative")
    print("      bound, excluded if r > 1 buys >~ 0.8 TeV). R1.4's 5 TeV placeholder")
    print("      applied to 1/L was too strong by 2 pi. Lightest psi: M_f ~ 1.4e5 GeV.")


if __name__ == "__main__":
    main()
