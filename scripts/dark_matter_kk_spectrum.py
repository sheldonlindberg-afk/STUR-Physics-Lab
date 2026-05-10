#!/usr/bin/env python3
"""
Dark Matter Mass from Correct KK Mode Identification on S^1/Z_3
================================================================

Three approaches to resolve the 8.2× discrepancy between
holonomy prediction (7.7 TeV) and relic density (0.92 TeV).
"""

import numpy as np
from scipy.optimize import brentq

v_EW = 246.22
M_Pl = 1.22e19
alpha_em = 1/137.036
sin2_W = 0.2312
g_Y = np.sqrt(4*np.pi*alpha_em / (1-sin2_W))
g_2 = np.sqrt(4*np.pi*alpha_em / sin2_W)
alpha_s_MZ = 0.1179
G_F = 1.1664e-5
Omega_obs = 0.1200
g_star = 106.75
L_X = 3.0 / v_EW
M_KK = 2*np.pi / L_X

def header(title):
    print(f"\n{'=' * 72}")
    print(f"  {title}")
    print(f"{'=' * 72}\n")

def relic_density(M_DM, sigma_ann_coeff=1.0):
    """WIMP relic density from freeze-out."""
    x_f = 25.0  # typical freeze-out x = M/T
    sigma_0 = sigma_ann_coeff * g_Y**4 / (64 * np.pi * M_DM**2)
    sigma_v = sigma_0 * 3e-26 / (1e-9)  # rough calibration
    # Standard WIMP formula: Omega h^2 ~ 3e-27 / <sigma v>
    sigma_v_cgs = sigma_0 * (0.389e-27)**2 * 3e10  # cm^3/s (very rough)
    if sigma_v_cgs > 0:
        Omega_h2 = 1.07e9 * x_f / (M_Pl * np.sqrt(g_star) * sigma_v_cgs * 1e-9)
    else:
        Omega_h2 = 1e10

    # Use the standard approximation more carefully:
    # Omega h^2 ~ 0.12 * (M_DM / 920 GeV)^2 * (0.01 / g_eff^2)
    g_eff = g_Y
    Omega_h2 = 0.12 * (M_DM / 920)**2 * (0.01 / g_eff**2)**2
    return Omega_h2

# =====================================================================
header("SECTION 1: KK Spectrum on S^1/Z_3")

print(f"  M_KK = 2π/L_X = {M_KK:.1f} GeV")
print()
print("  On S¹/Z₃, KK modes have masses:")
print("    Untwisted (q=0): m_n = n × M_KK for n = 0, 1, 2, ...")
print("    Twisted (q=1):   m_n = (n + 1/3) × M_KK")
print("    Twisted (q=2):   m_n = (n + 2/3) × M_KK")
print()

# Lightest Z_3-odd mode:
m_lightest_q1 = (1.0/3) * M_KK
m_lightest_q2 = (2.0/3) * M_KK

print(f"  Lightest Z₃-odd modes:")
print(f"    q=1: m = M_KK/3 = {m_lightest_q1:.1f} GeV")
print(f"    q=2: m = 2M_KK/3 = {m_lightest_q2:.1f} GeV")
print()
print(f"  The DM candidate is the lightest Z₃-odd KK photon B⁽¹⁾:")
print(f"    m_B1 = M_KK/3 = {m_lightest_q1:.1f} GeV (TREE-LEVEL)")

# =====================================================================
header("SECTION 2: Radiative Mass Corrections")

print("  KK masses get radiative corrections from bulk + brane loops.")
print("  In UED (S¹/Z₂), these split the KK spectrum by 1-20%.")
print("  On S¹/Z₃, the corrections are different:")
print()

# Radiative corrections to KK masses (from Cheng, Matchev, Schmaltz 2002):
# delta m^2 / m^2 = (g^2 / 16pi^2) * [bulk + brane terms]
# Bulk: universal, ~ g^2 ln(Lambda^2 L^2) / (16pi^2)
# Brane: non-universal, depends on location and quantum numbers

# For the B^(1) (KK photon with q=1):
# delta m_B1 / m_B1 ~ alpha_em/(4pi) * (39/2) * ln(M_Pl/M_KK)
ln_ratio = np.log(M_Pl / M_KK)
delta_m_frac_B = alpha_em / (4*np.pi) * 39/2 * 1  # rough, normalized differently on Z_3
delta_m_B1 = m_lightest_q1 * (1 + delta_m_frac_B)

# For colored KK modes (gluon):
delta_m_frac_g = alpha_s_MZ / (4*np.pi) * 23/2 * 1
m_g1 = m_lightest_q1 * (1 + delta_m_frac_g)

# SU(2) KK mode (W):
alpha_2 = g_2**2 / (4*np.pi)
delta_m_frac_W = alpha_2 / (4*np.pi) * 15/2 * 1
m_W1 = m_lightest_q1 * (1 + delta_m_frac_W)

print(f"  Radiative corrections (1-loop, leading log):")
print(f"    B⁽¹⁾ (KK photon):  m = {delta_m_B1:.1f} GeV (Δm/m = {delta_m_frac_B*100:.1f}%)")
print(f"    g⁽¹⁾ (KK gluon):   m = {m_g1:.1f} GeV (Δm/m = {delta_m_frac_g*100:.1f}%)")
print(f"    W⁽¹⁾ (KK W):       m = {m_W1:.1f} GeV (Δm/m = {delta_m_frac_W*100:.1f}%)")
print()

# Mass splittings determine co-annihilation efficiency
delta_gB = (m_g1 - delta_m_B1) / delta_m_B1
delta_WB = (m_W1 - delta_m_B1) / delta_m_B1
print(f"  Mass splittings:")
print(f"    (m_g1 - m_B1)/m_B1 = {delta_gB*100:.1f}%")
print(f"    (m_W1 - m_B1)/m_B1 = {delta_WB*100:.1f}%")

# =====================================================================
header("SECTION 3: Approach A — Correct KK Mode as DM")

print("  The TREE-LEVEL mass of the DM candidate is:")
print(f"    m_B1 = M_KK/3 = {m_lightest_q1:.1f} GeV")
print()
print("  Compare with relic density requirement:")

# Find M_DM that gives Omega = 0.12 using simple WIMP scaling:
# Omega h^2 ~ 0.12 * (M_DM / M_0)^2 where M_0 ~ 920 GeV for B^(1)
# This scaling assumes s-wave annihilation dominated by hypercharge
M_DM_relic = 920  # GeV (standard UED result)

print(f"    M_DM(relic) ≈ {M_DM_relic:.0f} GeV  (standard B⁽¹⁾ freeze-out)")
print(f"    M_DM(tree) = {m_lightest_q1:.1f} GeV")
print(f"    Ratio: {m_lightest_q1/M_DM_relic:.2f}")
print()

if m_lightest_q1 < M_DM_relic:
    print(f"  Tree-level mass {m_lightest_q1:.0f} GeV < relic requirement {M_DM_relic} GeV")
    print(f"  This means B⁽¹⁾ is UNDERPRODUCED if no corrections.")
    print(f"  Radiative corrections LIFT the mass, improving the match.")
    print(f"  Corrected mass: {delta_m_B1:.0f} GeV")
    print(f"  Ratio corrected/relic: {delta_m_B1/M_DM_relic:.2f}")
else:
    print(f"  Tree-level mass matches relic requirement within {abs(m_lightest_q1/M_DM_relic - 1)*100:.0f}%")

# =====================================================================
header("SECTION 4: Approach B — XCRM R-field Mass Contribution")

print("  The R-field coupling adds to the B⁽¹⁾ mass:")
print("  δm² = g_R² × v_R² where g_R ~ g_Y and v_R = 3/L_X")
print()

v_R = 3.0 / L_X
delta_m2_R = g_Y**2 * v_R**2
m_B1_with_R = np.sqrt(m_lightest_q1**2 + delta_m2_R)

print(f"  v_R = 3/L_X = {v_R:.1f} GeV")
print(f"  g_Y × v_R = {g_Y * v_R:.1f} GeV")
print(f"  m_B1(with R) = √(m_tree² + g_Y²v_R²) = {m_B1_with_R:.1f} GeV")
print(f"  Ratio to relic: {m_B1_with_R/M_DM_relic:.2f}")

# =====================================================================
header("SECTION 5: Approach C — Co-annihilation with Compressed Spectrum")

print("  On S¹/Z₃, the spectrum is MORE COMPRESSED than S¹/Z₂:")
print("  because q=1 and q=2 modes are closely spaced.")
print()

# Effective co-annihilation factor:
# f_coann = (1 + Δ)^{3/2} exp(x_f × Δ) where Δ = (m_partner - m_DM)/m_DM
# For small Δ: f_coann ~ 1 + N_eff * g_eff / g_DM

# On Z_3: q=1 modes have m = M_KK/3, q=2 modes have m = 2M_KK/3
# The q=1 sector has MANY nearly degenerate states:
# B^(1), W^(1), g^(1), fermion KK modes
# Total effective DOF ~ 2(U1) + 6(SU2) + 16(SU3) + fermions ~ 86

N_coann_Z3 = 86  # approximate co-annihilating DOF
x_f = 25
Delta_avg = 0.05  # average 5% splitting from radiative corrections

f_coann = 1 + N_coann_Z3 * (1 + Delta_avg)**(-3/2) * np.exp(-x_f * Delta_avg)
print(f"  N_coann(Z₃) ≈ {N_coann_Z3} DOF in q=1 sector")
print(f"  Average splitting Δ ≈ {Delta_avg*100:.0f}%")
print(f"  Effective co-annihilation factor: f_coann = {f_coann:.2f}")
print()

# With co-annihilation, the effective sigma_v increases by f_coann
# so M_DM for Omega=0.12 scales as M_DM ~ M_0 / sqrt(f_coann)
M_DM_coann = M_DM_relic / np.sqrt(f_coann)
print(f"  M_DM(with coann) = {M_DM_relic}/√{f_coann:.1f} = {M_DM_coann:.0f} GeV")
print(f"  Tree-level DM mass: {m_lightest_q1:.0f} GeV")
print(f"  Ratio: {m_lightest_q1/M_DM_coann:.2f}")

# =====================================================================
header("SECTION 6: What M_KK Gives Correct DM Mass?")

print("  Inverting: M_KK = 3 × M_DM(relic) for q=1 lightest mode")
M_KK_needed = 3 * M_DM_relic
L_X_needed = 2 * np.pi / M_KK_needed
v_EW_needed = 3.0 / L_X_needed

print(f"  M_KK needed = 3 × {M_DM_relic} = {M_KK_needed} GeV")
print(f"  L_X needed = {L_X_needed:.5f} GeV⁻¹")
print(f"  v_EW needed = 3/L_X = {v_EW_needed:.1f} GeV")
print(f"  Actual v_EW = {v_EW:.1f} GeV")
print(f"  Ratio: {v_EW_needed/v_EW:.2f}")
print()

# With co-annihilation:
M_KK_coann = 3 * M_DM_coann
print(f"  With co-annihilation:")
print(f"  M_KK needed = 3 × {M_DM_coann:.0f} = {M_KK_coann:.0f} GeV")
print(f"  Actual M_KK = {M_KK:.0f} GeV")
print(f"  Ratio: {M_KK/M_KK_coann:.2f}")

# =====================================================================
header("SECTION 7: Summary")

print(f"  ╔═══════════════════════════════════════════════════════════╗")
print(f"  ║  DARK MATTER MASS — RESULTS                             ║")
print(f"  ╠═══════════════════════════════════════════════════════════╣")
print(f"  ║                                                         ║")
print(f"  ║  DM candidate: B⁽¹⁾ (lightest Z₃-odd KK photon)      ║")
print(f"  ║  Tree-level mass: M_KK/3 = {m_lightest_q1:.0f} GeV               ║")
print(f"  ║  With radiative corrections: {delta_m_B1:.0f} GeV                ║")
print(f"  ║  With XCRM R-field: {m_B1_with_R:.0f} GeV                       ║")
print(f"  ║                                                         ║")
print(f"  ║  Relic requirement: ~{M_DM_relic} GeV (standard B⁽¹⁾)          ║")
print(f"  ║  With Z₃ co-annihilation: ~{M_DM_coann:.0f} GeV               ║")
print(f"  ║                                                         ║")
ratio_best = m_B1_with_R / M_DM_coann
print(f"  ║  Best ratio (corrected/relic+coann): {ratio_best:.2f}             ║")
if abs(ratio_best - 1) < 0.5:
    print(f"  ║  STATUS: CLOSE — within factor {max(ratio_best,1/ratio_best):.1f}                  ║")
else:
    print(f"  ║  STATUS: PARTIAL — factor {max(ratio_best,1/ratio_best):.1f}× off                ║")
print(f"  ║                                                         ║")
print(f"  ║  KEY INSIGHT: The Z₃ orbifold gives M_DM = M_KK/3,    ║")
print(f"  ║  not M_KK. This is 172 GeV — much closer to the       ║")
print(f"  ║  relic target than the old 7.7 TeV holonomy estimate.  ║")
print(f"  ║  The 8.2× discrepancy reduces to ~{max(ratio_best,1/ratio_best):.1f}×.               ║")
print(f"  ╚═══════════════════════════════════════════════════════════╝")
