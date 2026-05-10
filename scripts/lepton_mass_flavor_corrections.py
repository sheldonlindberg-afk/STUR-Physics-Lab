#!/usr/bin/env python3
"""
Lepton Mass Ratios with Flavor-Dependent Higgs Corrections
===========================================================

The key problem: m_tau/m_mu = 16.8 works (~2% off), but m_mu/m_e = 207
fails badly. This script investigates whether flavor-dependent Higgs
localization can close the gap.

Physics: The Higgs profile sigma_H differs for leptons vs quarks because
the CW potential gets different loop contributions (no QCD for leptons).
Additionally, the 3x3 Yukawa matrix structure matters — off-diagonal
elements must be suppressed for the 2nd/1st generation ratio to work.
"""

import numpy as np
from scipy.linalg import eigh
from scipy import integrate

v_EW = 246.22
M_TAU, M_MU, M_E = 1.77686, 0.10566, 0.000511
R_TAU_MU = M_TAU / M_MU   # 16.818
R_MU_E = M_MU / M_E       # 206.77
alpha_em = 1/137.036
L_X = 3.0 / v_EW

CENTERS = [0.0, 2*np.pi/3, 4*np.pi/3]
N = 200
THETA = np.linspace(-np.pi, np.pi, N, endpoint=False)
DTHETA = THETA[1] - THETA[0]

def header(title):
    print(f"\n{'=' * 72}")
    print(f"  {title}")
    print(f"{'=' * 72}\n")

def solve_mathieu(alpha_val, center=0.0):
    V = alpha_val * (1 - np.cos(THETA - center))
    diag = 2.0/DTHETA**2 + V
    off = -1.0/DTHETA**2 * np.ones(N-1)
    H = np.diag(diag) + np.diag(off, 1) + np.diag(off, -1)
    H[0, -1] = H[-1, 0] = -1.0/DTHETA**2  # periodic BC
    vals, vecs = eigh(H, subset_by_index=[0, 2])
    # Normalize
    for i in range(vecs.shape[1]):
        norm = np.sqrt(np.sum(vecs[:, i]**2) * DTHETA)
        vecs[:, i] /= norm
    return vals, vecs

def higgs_profile(sigma_H, center=0.0):
    h = np.exp(-(THETA - center)**2 / (2 * sigma_H**2))
    h /= np.sqrt(np.sum(h**2) * DTHETA)
    return h

def yukawa_matrix(alpha_val, sigma_H):
    """Compute 3x3 Yukawa matrix Y_gg' = int psi_g * H * psi_g' dtheta"""
    Y = np.zeros((3, 3))
    wavefunctions = []
    for c in CENTERS:
        _, vecs = solve_mathieu(alpha_val, c)
        wavefunctions.append(vecs[:, 0])

    H_profile = higgs_profile(sigma_H, 0.0)  # Higgs at first fixed point

    for g in range(3):
        for gp in range(3):
            Y[g, gp] = np.sum(wavefunctions[g] * H_profile * wavefunctions[gp]) * DTHETA

    return Y

# =====================================================================
header("SECTION 1: Quark Baseline (alpha_eff = 1.463)")

alpha_q = 1.463
sigma_H_q = 0.85  # from CW derivation

Y_quark = yukawa_matrix(alpha_q, sigma_H_q)
evals_q = np.sort(np.abs(np.linalg.eigvalsh(Y_quark @ Y_quark.T)))[::-1]
ratios_q = np.sqrt(evals_q)
r_32_q = ratios_q[0] / ratios_q[1] if ratios_q[1] > 0 else np.inf
r_21_q = ratios_q[1] / ratios_q[2] if ratios_q[2] > 0 else np.inf

print(f"  alpha_eff(quark) = {alpha_q}")
print(f"  sigma_H(quark)   = {sigma_H_q}")
print(f"  Eigenvalue ratios: y3/y2 = {r_32_q:.1f}, y2/y1 = {r_21_q:.1f}")
print(f"  Target (quarks):   m_t/m_c ~ 136, m_c/m_u ~ 590")

# =====================================================================
header("SECTION 2: Lepton alpha_eff = 1.381 (no QCD)")

alpha_l = 1.381

# Scan sigma_H to find what matches m_tau/m_mu
print(f"  Scanning sigma_H for lepton sector...")
print()
print(f"  sigma_H   m_tau/m_mu  m_mu/m_e   (targets: {R_TAU_MU:.1f}, {R_MU_E:.1f})")
print(f"  {'─'*60}")

best_err_tau_mu = 1e10
best_sigma = 0

for sigma_H in np.linspace(0.1, 2.0, 200):
    Y = yukawa_matrix(alpha_l, sigma_H)
    evals = np.sort(np.abs(np.linalg.eigvalsh(Y @ Y.T)))[::-1]
    r = np.sqrt(evals)
    if r[1] > 0 and r[2] > 0:
        r32 = r[0] / r[1]
        r21 = r[1] / r[2]
        err = abs(r32 - R_TAU_MU) / R_TAU_MU
        if err < best_err_tau_mu:
            best_err_tau_mu = err
            best_sigma = sigma_H
            best_r32 = r32
            best_r21 = r21
        if abs(sigma_H - 0.3) < 0.01 or abs(sigma_H - 0.5) < 0.01 or \
           abs(sigma_H - 0.85) < 0.01 or abs(sigma_H - 1.0) < 0.01 or \
           abs(sigma_H - 1.5) < 0.01:
            print(f"  {sigma_H:.2f}    {r32:.2f}       {r21:.2f}")

print(f"  ...")
print(f"  Best sigma_H for m_tau/m_mu = {R_TAU_MU:.1f}:")
print(f"    sigma_H = {best_sigma:.3f}")
print(f"    m_tau/m_mu = {best_r32:.2f}  (target: {R_TAU_MU:.2f})")
print(f"    m_mu/m_e   = {best_r21:.2f}  (target: {R_MU_E:.2f})")
print(f"    m_mu/m_e error: {abs(best_r21 - R_MU_E)/R_MU_E*100:.0f}%")

# =====================================================================
header("SECTION 3: Delta-Function Higgs Limit (Pairwise Overlap)")

kappa_l = np.sqrt(alpha_l)
kappa_q = np.sqrt(alpha_q)

# In delta-function limit: Y_gg' ~ psi_g(0) * psi_g'(0)
# Mass ratio from pairwise overlap:
# m_3/m_2 ~ exp(kappa^2 * (2pi/3)^2 / 2) / 1 = exp(kappa^2 * 2pi^2/9)

r_pairwise = np.exp(kappa_l**2 * (2*np.pi/3)**2 / 4)
# Actually: m_g/m_g' ~ exp((kappa * d_gg')^2 / 4) where d is distance between peaks

# More carefully: the overlap integral for Gaussians separated by d:
# Y_gg' = int exp(-(x-c_g)^2/(2sigma^2)) * delta(x) * exp(-(x-c_g')^2/(2sigma^2)) dx
# = exp(-c_g^2/(2sigma^2)) * exp(-c_g'^2/(2sigma^2))
# So Y_gg' = Y_g0 * Y_g'0

# For the mass matrix: Y is rank-1 in delta-function limit!
# This means only ONE eigenvalue is nonzero.
# The hierarchy comes from the FINITE width of both psi and H.

sigma_psi = 1.0 / kappa_l  # approximate width
d_12 = 2*np.pi/3  # distance between Z_3 fixed points

print(f"  kappa(lepton) = {kappa_l:.4f}")
print(f"  sigma_psi ~ 1/kappa = {sigma_psi:.4f} rad")
print(f"  d(Z_3 fixed points) = 2pi/3 = {d_12:.4f} rad")
print(f"  d/sigma = {d_12/sigma_psi:.2f}")
print()
print(f"  Overlap suppression: exp(-d^2/(4*sigma^2)) = exp(-kappa^2 * d^2/4)")
print(f"    = exp(-{kappa_l**2 * d_12**2/4:.4f}) = {np.exp(-kappa_l**2 * d_12**2/4):.6f}")
print()
print(f"  In delta-function H limit, Y is rank-1 → only 1 nonzero mass.")
print(f"  The hierarchy REQUIRES finite Higgs width sigma_H.")
print(f"  Smaller sigma_H → less overlap → larger hierarchy.")

# =====================================================================
header("SECTION 4: Two-Higgs Scenario (Different sigma_H per Generation)")

print("  What if each Z_3 fixed point has a slightly different Higgs profile?")
print("  This could arise from Wilson line corrections or brane tension.")
print()

# Try: sigma_H at fixed point 0 differs from sigma_H at fixed points 1,2
# due to the Hosotani mechanism breaking the Z_3 symmetry

def yukawa_matrix_split(alpha_val, sigma_H_0, sigma_H_12):
    """Different Higgs width at fixed point 0 vs 1,2"""
    wavefunctions = []
    for c in CENTERS:
        _, vecs = solve_mathieu(alpha_val, c)
        wavefunctions.append(vecs[:, 0])

    Y = np.zeros((3, 3))
    # Higgs profile is sum over fixed points with different widths
    H0 = higgs_profile(sigma_H_0, 0.0) * np.sqrt(sigma_H_0)
    H1 = higgs_profile(sigma_H_12, 2*np.pi/3) * np.sqrt(sigma_H_12)
    H2 = higgs_profile(sigma_H_12, 4*np.pi/3) * np.sqrt(sigma_H_12)
    H_total = H0 + H1 + H2
    H_total /= np.sqrt(np.sum(H_total**2) * DTHETA)

    for g in range(3):
        for gp in range(3):
            Y[g, gp] = np.sum(wavefunctions[g] * H_total * wavefunctions[gp]) * DTHETA

    return Y

print(f"  Scanning sigma_H_0 (1st fixed point) and sigma_H_12 (2nd/3rd)...")
print()

best_combined_err = 1e10
best_s0 = 0
best_s12 = 0

for s0 in np.linspace(0.2, 1.5, 20):
    for s12 in np.linspace(0.2, 1.5, 20):
        Y = yukawa_matrix_split(alpha_l, s0, s12)
        evals = np.sort(np.abs(np.linalg.eigvalsh(Y @ Y.T)))[::-1]
        r = np.sqrt(evals)
        if r[1] > 1e-15 and r[2] > 1e-15:
            r32 = r[0] / r[1]
            r21 = r[1] / r[2]
            err = (abs(r32 - R_TAU_MU)/R_TAU_MU)**2 + (abs(r21 - R_MU_E)/R_MU_E)**2
            if err < best_combined_err:
                best_combined_err = err
                best_s0 = s0
                best_s12 = s12
                best_r32_split = r32
                best_r21_split = r21

print(f"  Best fit (2-parameter scan):")
print(f"    sigma_H_0  = {best_s0:.3f}")
print(f"    sigma_H_12 = {best_s12:.3f}")
print(f"    m_tau/m_mu = {best_r32_split:.2f}  (target: {R_TAU_MU:.2f}, err: {abs(best_r32_split-R_TAU_MU)/R_TAU_MU*100:.1f}%)")
print(f"    m_mu/m_e   = {best_r21_split:.2f}  (target: {R_MU_E:.2f}, err: {abs(best_r21_split-R_MU_E)/R_MU_E*100:.1f}%)")

# =====================================================================
header("SECTION 5: Hypercharge Wilson Line Splitting")

print("  Leptons have different hypercharges than quarks:")
print("  e_R: Y = -1, mu_R: Y = -1, tau_R: Y = -1 (all same)")
print("  But L_L = (nu, e)_L: Y = -1/2")
print()
print("  The Wilson line phase at each Z_3 fixed point is:")
print("    theta_j = Y * g_Y * <A_X> * L_X/3")
print("  This displaces the wavefunction centers differently for different Y.")
print()

g_Y = np.sqrt(4*np.pi*alpha_em / (1 - 0.2312))
A_X_vev = 0.001  # small Wilson line VEV (from Hosotani at EW scale)

for Y_val, name in [(-1, "e_R/mu_R/tau_R"), (-1/2, "L_L"), (2/3, "u_R"), (-1/3, "d_R")]:
    delta = Y_val * g_Y * A_X_vev * L_X / 3
    print(f"    {name:20s}: Y={Y_val:+.2f}, delta_theta = {delta:.6f} rad")

print()
print("  The hypercharge Wilson line shifts are tiny (O(10^-6) rad)")
print("  because <A_X> ~ 0.001 GeV is small from Hosotani at L_X = 3/v_EW.")
print("  This cannot explain the m_mu/m_e discrepancy.")

# =====================================================================
header("SECTION 6: Z_3 Selection Rules for Leptons")

print("  For quarks, SU(3) color provides Z_3 charge assignments")
print("  that suppress off-diagonal Yukawa elements.")
print("  For leptons (color singlets), this mechanism is ABSENT.")
print()
print("  However, the SU(2)_L x U(1)_Y quantum numbers do provide")
print("  non-trivial Z_3 phases through the GAUGE holonomy:")
print("    P = exp(2pi*i*T_3/3) for SU(2) on Z_3")
print("  This acts as:")
print("    nu_L -> omega * nu_L  (T_3 = +1/2)")
print("    e_L  -> omega^2 * e_L (T_3 = -1/2)")
print("    e_R  -> e_R           (SU(2) singlet)")
print()

# The Z_3 phase from SU(2) gauge holonomy:
# P_SU2 = exp(2pi*i*T3/3)
# For lepton doublet: (nu, e)_L transform as (omega, omega^2)
# For e_R (singlet): trivial

# The overlap integral gets a phase:
# Y_{e_L, e_R} ~ int psi_L^* (omega^2)^g * H * psi_R dX
# This means generation g gets phase omega^{2g}

# For the Yukawa matrix:
# Y_gg' = sum_j Y_j * omega^{2g*j} (Z_3 Fourier transform)
# This IS a non-trivial selection rule!

# Compute with Z_3 phases:
def yukawa_with_z3_phases(alpha_val, sigma_H, z3_charge=2):
    """Include Z_3 phase from SU(2) holonomy"""
    omega = np.exp(2j * np.pi / 3)
    wavefunctions = []
    for c in CENTERS:
        _, vecs = solve_mathieu(alpha_val, c)
        wavefunctions.append(vecs[:, 0])

    H_prof = higgs_profile(sigma_H, 0.0)

    Y = np.zeros((3, 3), dtype=complex)
    for g in range(3):
        phase_g = omega**(z3_charge * g)
        for gp in range(3):
            overlap = np.sum(wavefunctions[g] * H_prof * wavefunctions[gp]) * DTHETA
            Y[g, gp] = phase_g * overlap

    return Y

for sigma_H in [0.5, 0.85]:
    Y_z3 = yukawa_with_z3_phases(alpha_l, sigma_H, z3_charge=2)
    YYd = Y_z3 @ Y_z3.conj().T
    evals = np.sort(np.abs(np.linalg.eigvalsh(YYd.real)))[::-1]
    r = np.sqrt(evals)
    if r[1] > 1e-15 and r[2] > 1e-15:
        r32 = r[0] / r[1]
        r21 = r[1] / r[2]
    else:
        r32 = r21 = np.inf
    print(f"  sigma_H={sigma_H:.2f}: m_3/m_2={r32:.1f}, m_2/m_1={r21:.1f}")

# =====================================================================
header("SECTION 7: Summary")

print(f"  ╔═══════════════════════════════════════════════════════════╗")
print(f"  ║  LEPTON MASS RATIOS — RESULTS                           ║")
print(f"  ╠═══════════════════════════════════════════════════════════╣")
print(f"  ║  m_tau/m_mu:                                            ║")
print(f"  ║    Observed:  {R_TAU_MU:.2f}                                    ║")
print(f"  ║    Best pred: {best_r32:.2f} (sigma_H={best_sigma:.2f})               ║")
print(f"  ║    Error:     {abs(best_r32-R_TAU_MU)/R_TAU_MU*100:.1f}%                                     ║")
print(f"  ║                                                         ║")
print(f"  ║  m_mu/m_e:                                              ║")
print(f"  ║    Observed:  {R_MU_E:.2f}                                   ║")
print(f"  ║    Best pred: {best_r21:.2f} (same sigma_H)                   ║")
print(f"  ║    Error:     {abs(best_r21-R_MU_E)/R_MU_E*100:.0f}%                                       ║")
print(f"  ║                                                         ║")
print(f"  ║  Split sigma scenario:                                  ║")
print(f"  ║    sigma_0={best_s0:.2f}, sigma_12={best_s12:.2f}                     ║")
print(f"  ║    m_tau/m_mu = {best_r32_split:.1f} ({abs(best_r32_split-R_TAU_MU)/R_TAU_MU*100:.0f}%)                          ║")
print(f"  ║    m_mu/m_e   = {best_r21_split:.1f} ({abs(best_r21_split-R_MU_E)/R_MU_E*100:.0f}%)                          ║")
print(f"  ║                                                         ║")
print(f"  ║  STATUS: PARTIAL                                        ║")
print(f"  ║  3rd/2nd gen ratio works; 2nd/1st gen requires either   ║")
print(f"  ║  Z_3 selection rules from SU(2) holonomy or split       ║")
print(f"  ║  Higgs widths at different fixed points.                ║")
print(f"  ╚═══════════════════════════════════════════════════════════╝")
