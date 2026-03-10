#!/usr/bin/env python3
"""
Seesaw Scale M_R from Hosotani Mechanism on S^1/Z_3
=====================================================

STUR Framework -- Deriving M_R from first principles

PROBLEM:
  In the existing STUR code, M_R is effectively FITTED:
    M_R = lambda_hol * inv_LX_UV
  where lambda_hol ~ 20 is assembled from ad-hoc factors (f_base=3,
  f_loc=1.5, f_Wilson=2.08, f_inf=2.1) and inv_LX_UV = 10^13 GeV
  is assumed. This gives M_R ~ 2e14 GeV, which is then fed into the
  seesaw formula with Dirac masses reverse-engineered from the desired
  neutrino masses. That is circular.

GOAL:
  Derive M_R from the Hosotani mechanism: the Wilson line on S^1/Z_3
  breaks a symmetry protecting the right-handed neutrino mass, generating
  M_R at one loop through the Hosotani effective potential.

PHYSICS:
  1. On S^1/Z_3, the Wilson line P exp(i oint A_X dX) has Z_3 holonomy
  2. The one-loop effective potential for the Wilson line phase theta is:
       V(theta) = -(1/(64 pi^2 L^4)) sum_fields N_dof sum_n 1/(theta+2pi*n)^4
     More precisely, the standard Hosotani/Casimir potential on S^1:
       V(theta) = -(3/(2 pi^2 L^4)) sum_rep d_rep B_4({q*theta/(2pi)})
     where B_4(x) = x^4 - 2x^3 + x^2 - 1/30 is the 4th Bernoulli polynomial
  3. The minimum determines <A_X> = theta_min / L
  4. M_R = g_2 * <A_X> = g_2 * theta_min / L
  5. Compare with seesaw: m_nu ~ v^2 / M_R

HONEST ASSESSMENT: This script will show whether the Hosotani mechanism
gives the right scale for M_R, or whether there is a fundamental problem.

Author: Computed for STUR framework
"""

import numpy as np
from scipy.optimize import minimize_scalar, minimize
from scipy.special import bernoulli as scipy_bernoulli

# =========================================================================
# CONSTANTS
# =========================================================================

M_Pl = 1.22e19           # Planck mass (GeV) -- full, not reduced
M_Pl_red = 2.435e18      # Reduced Planck mass (GeV)
v_EW = 246.22            # Electroweak VEV (GeV)
sin2_thetaW = 0.23121    # Weinberg angle
g_2 = 0.652              # SU(2)_L coupling at M_Z
g_Y = 0.357              # U(1)_Y coupling at M_Z
alpha_s_MZ = 0.1179      # Strong coupling at M_Z
hbar_c_m = 1.9733e-16    # hbar*c in m*GeV

# NuFIT 5.2 (2022) best-fit values (normal ordering)
Dm2_21_exp = 7.53e-5     # eV^2  (solar)
Dm2_31_exp = 2.453e-3    # eV^2  (atmospheric, NO)

# From STUR: v*L_X = 3 quantization
# L_X = 3 / v_EW = 0.01219 GeV^{-1} (the UV/fundamental scale)
L_X_fund = 3.0 / v_EW    # GeV^{-1}
M_KK_fund = 2 * np.pi / L_X_fund  # KK mass scale


def header(title):
    w = 76
    print(f"\n{'=' * w}")
    print(f"  {title}")
    print(f"{'=' * w}\n")


def B4(x):
    """4th Bernoulli polynomial B_4(x) = x^4 - 2x^3 + x^2 - 1/30.
    Evaluated for {x} = x mod 1 (periodic extension)."""
    xp = x - np.floor(x)  # fractional part
    return xp**4 - 2*xp**3 + xp**2 - 1.0/30


# =========================================================================
# PART 1: THE HOSOTANI EFFECTIVE POTENTIAL ON S^1/Z_3
# =========================================================================

header("PART 1: Hosotani Effective Potential on S^1/Z_3")

print("""  The Hosotani mechanism: on a compact space with nontrivial pi_1,
  the Wilson line <A_X> = theta / (g * L) is a physical degree of freedom.
  Its value is determined by minimizing the one-loop effective potential.

  On S^1 of circumference L, for a gauge field with coupling g, the
  one-loop potential from a field of spin s, charge q under the gauge
  group, and mass m is:

    V(theta) = -C * sum_rep N_dof * sum_{n=-inf}^{inf} 1/|n + q*theta/(2pi)|^5

  The standard result (Hosotani 1983, Hatanaka-Inami-Lim 1999) in terms
  of Bernoulli polynomials:

    V(theta) = -(3 / (2 pi^2 L^4)) * sum_rep d_rep * B_4({q*theta/(2pi)})

  For PERIODIC bosons and ANTIPERIODIC fermions on S^1:
    Bosons:  contribute -d_B * B_4({q*theta/(2pi)})
    Fermions: contribute +d_F * B_4({q*theta/(2pi) + 1/2})

  On S^1/Z_3: the orbifold projects out 2/3 of the KK modes.
  The surviving modes have n = 0 mod 3 (untwisted) plus twisted sector
  contributions at the fixed points.
""")


def hosotani_potential_S1(theta, L, field_content):
    """
    Compute the one-loop Hosotani effective potential on S^1.

    Parameters:
        theta: Wilson line phase (dimensionless, in [0, 2pi])
        L: circumference of S^1 (GeV^{-1})
        field_content: list of (N_dof, charge_q, is_fermion, label)

    Returns:
        V(theta) in GeV^4
    """
    prefactor = 3.0 / (2 * np.pi**2 * L**4)
    V = 0.0
    for N_dof, q, is_fermion, label in field_content:
        x = q * theta / (2 * np.pi)
        if is_fermion:
            # Antiperiodic fermions: shift by 1/2
            V += N_dof * B4(x + 0.5)
        else:
            # Periodic bosons
            V -= N_dof * B4(x)
    return -prefactor * V


def hosotani_potential_Z3(theta, L, field_content):
    """
    Hosotani potential on S^1/Z_3.

    On the orbifold, the potential is modified:
    1. Untwisted sector: KK modes with n = 0 mod 3 survive
       This replaces B_4({x}) -> B_4({3x})/3^4 (rescaled sum)
       Actually: the proper orbifold result is V_Z3 = (1/3)*V_S1(theta)
       because 1/3 of modes survive, but with the SAME theta
       (the Wilson line wraps the full circle, not 1/3 of it).
    2. Twisted sectors at fixed points: add localized contributions.

    More carefully (see e.g. Scrucca-Serone 2003):
    On S^1/Z_N, the effective potential is:
      V_orb(theta) = (1/N) * sum_{k=0}^{N-1} V_S1(theta + 2*pi*k/N * twist_phases)

    For Z_3 with the standard embedding:
      V_Z3(theta) = (1/3)[V_S1(theta) + V_S1(theta + 2pi/3) + V_S1(theta + 4pi/3)]
    """
    V = 0.0
    for k in range(3):
        shift = 2 * np.pi * k / 3.0
        V += hosotani_potential_S1(theta + shift, L, field_content)
    return V / 3.0


# =========================================================================
# PART 2: FIELD CONTENT FOR THE WILSON LINE POTENTIAL
# =========================================================================

header("PART 2: SM Field Content Charges under SU(2)_L Wilson Line")

print("""  For the SU(2)_L Wilson line, the relevant charge is the T_3 eigenvalue.
  The Wilson line phase theta parametrizes: W = exp(i*theta*T_3).

  SU(2)_L doublets feel the Wilson line with charges q = +/- 1/2.
  SU(2)_L singlets are neutral (q = 0).

  SM field content (charges under SU(2)_L T_3):
""")

# SM fields: (N_dof, T_3 charge, is_fermion, label)
# For SU(2)_L Wilson line: doublets have T_3 = +/- 1/2
# Count complex d.o.f. -> real d.o.f.

# Fermion doublets (each is a Weyl fermion doublet = 2 Weyl fermions):
# Q_L = (u_L, d_L): 3 colors x 3 generations x 2 (Weyl d.o.f. in 5D)
# L_L = (nu_L, e_L): 3 generations x 2

# For the Hosotani potential, what matters is:
# - Each LEFT-HANDED doublet contributes 2 Weyl fermions with T_3 = +1/2, -1/2
# - In 5D, a Dirac fermion = 2 Weyl fermions, so we count 4 real d.o.f. per Dirac
# - SU(2) doublet: each component is a Dirac fermion (in 5D) with charge q = +/-1/2

# Standard counting for Hosotani potential (5D on S^1):
# Each 5D Dirac fermion with charge q contributes N_dof = 4 (real d.o.f.)

sm_fields_su2 = [
    # Fermion SU(2) doublets: q = +1/2 and q = -1/2 components
    # Quarks: 3 colors x 3 generations = 9 doublets
    (4, +0.5, True, "u_L (3c x 3g)"),   # 9 copies
    (4, -0.5, True, "d_L (3c x 3g)"),   # 9 copies
    # Leptons: 3 generations = 3 doublets
    (4, +0.5, True, "nu_L (3g)"),        # 3 copies
    (4, -0.5, True, "e_L (3g)"),         # 3 copies

    # Fermion SU(2) singlets: q = 0 (don't contribute to SU(2) potential)
    # u_R, d_R, e_R, (nu_R): charge 0 under SU(2), so they drop out

    # Gauge bosons: W^+, W^-, W^3 have charges +1, -1, 0
    (2, +1.0, False, "W^+"),    # 2 polarizations in 5D (transverse)
    (2, -1.0, False, "W^-"),
    (2, 0.0, False, "W^3"),
    # The A_X component (5th component) is the Wilson line itself -- excluded

    # Higgs doublet: 2 complex = 4 real d.o.f., charges +1/2, -1/2
    (1, +0.5, False, "H^+"),
    (1, -0.5, False, "H^0"),
]

# Multiply fermion contributions by the number of copies
sm_fields_full = [
    # 9 quark doublets: each has T_3 = +1/2 and -1/2 components
    (4 * 9, +0.5, True, "Q_L upper (9 doublets)"),
    (4 * 9, -0.5, True, "Q_L lower (9 doublets)"),
    # 3 lepton doublets
    (4 * 3, +0.5, True, "L_L upper (3 doublets)"),
    (4 * 3, -0.5, True, "L_L lower (3 doublets)"),
    # W bosons (5D: 3 physical polarizations, but on S^1 the A_5 is the modulus)
    (3, +1.0, False, "W^+"),
    (3, -1.0, False, "W^-"),
    (3, 0.0, False, "W^3"),
    # Higgs doublet (4 real scalars)
    (2, +0.5, False, "H^+"),
    (2, -0.5, False, "H^0"),
]

for N, q, is_f, label in sm_fields_full:
    ftype = "fermion" if is_f else "boson"
    print(f"    N_dof = {N:3d}, T_3 = {q:+.1f}, {ftype:7s}  ({label})")

total_fermion_dof = sum(N for N, q, is_f, _ in sm_fields_full if is_f)
total_boson_dof = sum(N for N, q, is_f, _ in sm_fields_full if not is_f)
print(f"\n  Total: {total_fermion_dof} fermion d.o.f., {total_boson_dof} boson d.o.f.")


# =========================================================================
# PART 3: MINIMIZE THE HOSOTANI POTENTIAL
# =========================================================================

header("PART 3: Minimizing V(theta) on S^1 and S^1/Z_3")

# Scan theta from 0 to 2*pi
N_theta = 1000
theta_arr = np.linspace(0, 2*np.pi, N_theta)

# Use the fundamental STUR scale: L = L_X_fund = 3/v_EW
L = L_X_fund

V_S1 = np.array([hosotani_potential_S1(th, L, sm_fields_full) for th in theta_arr])
V_Z3 = np.array([hosotani_potential_Z3(th, L, sm_fields_full) for th in theta_arr])

# Find minima
idx_min_S1 = np.argmin(V_S1)
idx_min_Z3 = np.argmin(V_Z3)

print(f"  Compactification scale: L = 3/v_EW = {L:.5f} GeV^{{-1}}")
print(f"  Corresponding M_KK = 2pi/L = {M_KK_fund:.1f} GeV")
print(f"")
print(f"  --- On S^1 (no orbifold) ---")
print(f"  V(theta) minimum at theta_min = {theta_arr[idx_min_S1]:.4f} rad")
print(f"                                 = {theta_arr[idx_min_S1]/np.pi:.4f} pi")
print(f"  V(theta_min) = {V_S1[idx_min_S1]:.6e} GeV^4")
print(f"")
print(f"  --- On S^1/Z_3 ---")
print(f"  V(theta) minimum at theta_min = {theta_arr[idx_min_Z3]:.4f} rad")
print(f"                                 = {theta_arr[idx_min_Z3]/np.pi:.4f} pi")
print(f"  V(theta_min) = {V_Z3[idx_min_Z3]:.6e} GeV^4")

# Refine the S^1/Z_3 minimum
result_Z3 = minimize_scalar(
    lambda th: hosotani_potential_Z3(th, L, sm_fields_full),
    bounds=(0.01, np.pi),
    method='bounded'
)
theta_min_Z3 = result_Z3.x

# Also check near pi and 2pi/3
candidates = []
for th0 in [0.1, np.pi/3, 2*np.pi/3, np.pi, 4*np.pi/3, 5*np.pi/3]:
    res = minimize_scalar(
        lambda th: hosotani_potential_Z3(th, L, sm_fields_full),
        bounds=(max(0.001, th0 - 0.5), min(2*np.pi - 0.001, th0 + 0.5)),
        method='bounded'
    )
    candidates.append((res.fun, res.x))

candidates.sort()
theta_min_Z3 = candidates[0][1]
V_min_Z3 = candidates[0][0]

print(f"\n  Refined Z_3 minimum:")
print(f"    theta_min = {theta_min_Z3:.6f} rad = {theta_min_Z3/np.pi:.6f} pi")
print(f"    V(theta_min) = {V_min_Z3:.6e} GeV^4")

# Also print all local minima found
print(f"\n  All extrema found on S^1/Z_3:")
for V_val, th_val in candidates[:6]:
    print(f"    theta = {th_val:.4f} ({th_val/np.pi:.4f} pi), V = {V_val:.6e} GeV^4")


# =========================================================================
# PART 4: COMPUTE M_R FROM THE WILSON LINE VEV
# =========================================================================

header("PART 4: Right-Handed Neutrino Mass from Wilson Line VEV")

print("""  The Wilson line VEV gives a gauge field background:
    <A_X> = theta_min / (g_2 * L)

  For a right-handed neutrino (SU(2) singlet, but it can couple to
  the Wilson line through higher-dimensional operators or through
  a Majorana mass term that involves the Wilson line):

  MECHANISM: The right-handed neutrino has zero SU(2)_L charge,
  so it does NOT directly couple to the SU(2)_L Wilson line.

  For M_R to come from the Hosotani mechanism, we need EITHER:
    (a) A separate U(1)_{B-L} gauge symmetry in the bulk, whose
        Wilson line gives mass to nu_R, OR
    (b) The nu_R mass arises at SECOND order: the SU(2)_L Wilson line
        breaks SU(2) -> U(1), and the resulting symmetry-breaking
        pattern generates M_R through loops, OR
    (c) M_R = <A_X> directly if nu_R carries charge under the 5D gauge
        group (e.g., in an SU(3)_W or SO(10) embedding).

  Let us compute M_R for each scenario.
""")

# Scenario A: M_R = g * <A_X> (direct coupling)
# This would apply if nu_R has charge 1 under some U(1) in the bulk
A_X_vev = theta_min_Z3 / L  # GeV (mass dimension 1)
M_R_direct = g_2 * A_X_vev

print(f"  Wilson line VEV: <A_X> = theta_min / L = {A_X_vev:.4f} GeV")
print(f"")
print(f"  Scenario A: M_R = g_2 * <A_X> (direct, charge-1 coupling)")
print(f"    M_R = {g_2:.3f} x {A_X_vev:.2f} = {M_R_direct:.2f} GeV")
print(f"    This is ~ M_KK scale = {M_KK_fund:.1f} GeV")
print(f"    >> PROBLEM: This is WAY too low for seesaw!")
print(f"       Need M_R ~ 10^14 GeV, got M_R ~ {M_R_direct:.0f} GeV")
print(f"")

# Scenario B: M_R from one-loop with the Wilson line
# At one loop, the Wilson line can generate a Majorana mass through
# a diagram where two Higgs doublets connect to the neutrino line
# via the Wilson line background. This gives:
# M_R ~ (g^2 / (16 pi^2)) * (theta / L) * (v^2 / M_KK)
M_R_oneloop = (g_2**2 / (16 * np.pi**2)) * theta_min_Z3 / L
print(f"  Scenario B: M_R from one-loop (suppressed by 1/(16 pi^2))")
print(f"    M_R = (g_2^2 / 16pi^2) * theta/L = {M_R_oneloop:.4f} GeV")
print(f"    >> EVEN WORSE: loop-suppressed, ~{M_R_oneloop:.2f} GeV")
print(f"")

# Scenario C: M_R = M_KK (the KK scale itself)
# If the right-handed neutrino is a KK mode, its mass IS M_KK
M_R_KK = M_KK_fund
print(f"  Scenario C: M_R = M_KK (nu_R as zero-mode with KK-scale mass)")
print(f"    M_R = 2pi/L = {M_R_KK:.1f} GeV")
print(f"    >> SAME PROBLEM: M_KK = {M_R_KK:.0f} GeV << 10^14 GeV")


# =========================================================================
# PART 5: THE FUNDAMENTAL SCALE PROBLEM
# =========================================================================

header("PART 5: The Scale Problem -- Why Hosotani Cannot Give M_R ~ 10^14 GeV")

print(f"""  THE ROOT ISSUE:

  The Hosotani mechanism generates masses of order:
    M_Hosotani ~ theta / L ~ 1 / L

  In STUR, the fundamental compactification scale is:
    L = 3 / v_EW = {L_X_fund:.5f} GeV^{{-1}}
    => 1/L = v_EW/3 = {v_EW/3:.1f} GeV
    => M_KK = 2pi/L = {M_KK_fund:.0f} GeV

  So ANY mass generated by the Hosotani mechanism is bounded by:
    M_R <~ M_KK ~ {M_KK_fund:.0f} GeV

  To get M_R ~ 10^14 GeV, we would need:
    L ~ 1 / (10^14 GeV) = 10^{{-14}} GeV^{{-1}}
    which is ~{1e-14/L_X_fund:.1e} times SMALLER than L_X_fund.

  This is a factor of ~10^12 discrepancy.

  POSSIBLE RESOLUTIONS:
  1. L_X is NOT 3/v_EW but much smaller (different v in v*L=3)
  2. M_R comes from a mechanism OTHER than the Hosotani Wilson line
  3. There is an enhancement factor (the "lambda_hol ~ 20" approach)
     but this provides at most O(10) enhancement, not 10^12
""")


# =========================================================================
# PART 6: WHAT IF L_X IS AT THE GUT SCALE?
# =========================================================================

header("PART 6: Hosotani M_R with L_X at Various Scales")

print("""  Let's honestly compute M_R for different compactification scales
  and see what neutrino masses result from the seesaw formula.

  Seesaw: m_nu = m_D^2 / M_R
  We take m_D = y_nu * v_EW / sqrt(2) with y_nu ranging from
  y_e ~ 3e-6 to y_t ~ 1 (different possibilities).
""")

# Table: L_X -> M_R -> m_nu for various Dirac Yukawa assumptions
scales = [
    ("v*L=3 (fund.)", L_X_fund),
    ("M_KK = 10^4 GeV", 2*np.pi/1e4),
    ("M_KK = 10^6 GeV", 2*np.pi/1e6),
    ("M_KK = 10^10 GeV", 2*np.pi/1e10),
    ("M_KK = 10^13 GeV", 2*np.pi/1e13),
    ("M_KK = 10^14 GeV", 2*np.pi/1e14),
    ("M_KK = 10^15 GeV", 2*np.pi/1e15),
    ("M_KK = M_GUT", 2*np.pi/2e16),
]

# Dirac mass assumptions
m_D_values = {
    "y~y_e (3e-6)": 3e-6 * v_EW / np.sqrt(2),
    "y~y_mu (6e-4)": 6e-4 * v_EW / np.sqrt(2),
    "y~y_tau (0.01)": 0.01 * v_EW / np.sqrt(2),
    "y~y_b (0.024)": 0.024 * v_EW / np.sqrt(2),
    "y~y_t (1.0)": 1.0 * v_EW / np.sqrt(2),
}

print(f"  {'Scale':20s}  {'M_KK (GeV)':>14s}  {'M_R (GeV)':>14s}  ", end="")
print(f"{'m_nu(y~y_t)':>14s}  {'m_nu(y~y_tau)':>14s}")
print(f"  {'':20s}  {'':>14s}  {'':>14s}  {'(eV)':>14s}  {'(eV)':>14s}")
print(f"  {'-'*20}  {'-'*14}  {'-'*14}  {'-'*14}  {'-'*14}")

for label, L_val in scales:
    M_KK_val = 2 * np.pi / L_val

    # Hosotani M_R: minimize V on S^1/Z_3 at this scale
    res = minimize_scalar(
        lambda th: hosotani_potential_Z3(th, L_val, sm_fields_full),
        bounds=(0.01, np.pi),
        method='bounded'
    )
    theta_min = res.x
    M_R_val = g_2 * theta_min / L_val

    # Seesaw masses
    m_D_t = 1.0 * v_EW / np.sqrt(2)
    m_D_tau = 0.01 * v_EW / np.sqrt(2)

    if M_R_val > 0:
        m_nu_t = m_D_t**2 / M_R_val  # GeV
        m_nu_tau = m_D_tau**2 / M_R_val  # GeV
    else:
        m_nu_t = float('inf')
        m_nu_tau = float('inf')

    print(f"  {label:20s}  {M_KK_val:14.2e}  {M_R_val:14.2e}  "
          f"{m_nu_t*1e9:14.2e}  {m_nu_tau*1e9:14.2e}")


# =========================================================================
# PART 7: REQUIRED L_X FOR CORRECT NEUTRINO MASSES
# =========================================================================

header("PART 7: What L_X Is Required for Correct Neutrino Masses?")

print("""  Working backwards from the observed neutrino mass splittings:

  Target: m_nu3 ~ 0.05 eV (from Dm^2_31 ~ 2.5e-3 eV^2)
  Seesaw: m_nu3 = m_D3^2 / M_R

  If m_D3 ~ m_t ~ 173 GeV (maximal, y~1):
    M_R = m_t^2 / m_nu3 = (173)^2 / (0.05e-9) = 6.0e14 GeV

  If m_D3 ~ v_EW/sqrt(2) ~ 174 GeV:
    M_R = (174)^2 / (0.05e-9) = 6.1e14 GeV

  If m_D3 ~ 10 GeV (y ~ 0.06, comparable to y_b):
    M_R = (10)^2 / (0.05e-9) = 2.0e12 GeV

  For Hosotani: M_R ~ g_2 * theta_min / L ~ g_2 / L
  So: L ~ g_2 / M_R
""")

m_nu3_target = 0.05e-9  # GeV (0.05 eV)

for m_D_label, m_D_val in [
    ("m_D = m_t = 173 GeV", 173.0),
    ("m_D = v/sqrt(2) = 174 GeV", v_EW/np.sqrt(2)),
    ("m_D = 10 GeV (y~0.06)", 10.0),
    ("m_D = 1 GeV (y~0.006)", 1.0),
]:
    M_R_needed = m_D_val**2 / m_nu3_target
    L_needed = g_2 * np.pi / M_R_needed  # theta_min ~ pi for fermion-dominated
    M_KK_needed = 2 * np.pi / L_needed

    print(f"  {m_D_label}:")
    print(f"    M_R needed = {M_R_needed:.2e} GeV")
    print(f"    L needed   = {L_needed:.2e} GeV^-1 = {L_needed*hbar_c_m:.2e} m")
    print(f"    M_KK       = {M_KK_needed:.2e} GeV")
    print(f"    v from v*L=3: v = {3.0/L_needed:.2e} GeV")
    print()


# =========================================================================
# PART 8: FULL SEESAW CALCULATION AT THE "CORRECT" SCALE
# =========================================================================

header("PART 8: Seesaw with Hosotani-Determined M_R at Various L_X")

print("""  We now compute the full seesaw prediction: given L_X, the Hosotani
  mechanism determines theta_min and hence M_R. We then predict all
  three neutrino masses using the STUR generation hierarchy (Cabibbo
  angle suppression for lighter generations).

  Dirac mass pattern (from STUR wavefunction overlaps):
    m_D3 ~ y_3 * v_EW / sqrt(2)
    m_D2 ~ m_D3 * lambda_C^2   (lambda_C = Cabibbo angle ~ 0.225)
    m_D1 ~ m_D3 * lambda_C^4
""")

lambda_C = 0.2253  # Cabibbo angle

# Try the scale that gives M_R ~ 2e14 GeV (the "standard" seesaw scale)
# At this scale, theta_min should be ~ pi (typical for fermion-dominated)
M_R_target = 2e14  # GeV
L_target = g_2 * np.pi / M_R_target
print(f"  For target M_R = {M_R_target:.1e} GeV:")
print(f"    Required L = {L_target:.2e} GeV^-1")

# Compute Hosotani potential at this scale
res_target = minimize_scalar(
    lambda th: hosotani_potential_Z3(th, L_target, sm_fields_full),
    bounds=(0.01, 2*np.pi - 0.01),
    method='bounded'
)
theta_min_target = res_target.x
M_R_hosotani = g_2 * theta_min_target / L_target

print(f"    Hosotani theta_min = {theta_min_target:.4f} rad = {theta_min_target/np.pi:.4f} pi")
print(f"    M_R (Hosotani) = {M_R_hosotani:.4e} GeV")
print()

# Now compute neutrino masses with this M_R
# Use y_D3 such that seesaw works
y_D3 = 1.0  # O(1) Yukawa (top-like)
m_D3 = y_D3 * v_EW / np.sqrt(2)
m_D2 = m_D3 * lambda_C**2
m_D1 = m_D3 * lambda_C**4

m_nu3 = m_D3**2 / M_R_hosotani  # GeV
m_nu2 = m_D2**2 / M_R_hosotani
m_nu1 = m_D1**2 / M_R_hosotani

# Convert to eV
m_nu3_eV = m_nu3 * 1e9
m_nu2_eV = m_nu2 * 1e9
m_nu1_eV = m_nu1 * 1e9

Dm2_31 = m_nu3_eV**2 - m_nu1_eV**2
Dm2_21 = m_nu2_eV**2 - m_nu1_eV**2

print(f"  Dirac masses (y_3 = {y_D3}):")
print(f"    m_D3 = {m_D3:.1f} GeV")
print(f"    m_D2 = {m_D2:.2f} GeV  (m_D3 * lambda_C^2)")
print(f"    m_D1 = {m_D1:.4f} GeV  (m_D3 * lambda_C^4)")
print()
print(f"  Neutrino masses (seesaw with M_R = {M_R_hosotani:.2e} GeV):")
print(f"    m_nu1 = {m_nu1_eV:.6e} eV")
print(f"    m_nu2 = {m_nu2_eV:.6e} eV")
print(f"    m_nu3 = {m_nu3_eV:.6e} eV")
print()
print(f"  Mass-squared differences:")
print(f"    Dm^2_31 = {Dm2_31:.4e} eV^2   (NuFIT: {Dm2_31_exp:.3e} eV^2)")
print(f"    Dm^2_21 = {Dm2_21:.4e} eV^2   (NuFIT: {Dm2_21_exp:.3e} eV^2)")
print()

# Compare
ratio_31 = Dm2_31 / Dm2_31_exp
ratio_21 = Dm2_21 / Dm2_21_exp
r_3121 = Dm2_31 / Dm2_21 if Dm2_21 > 0 else float('inf')
r_3121_exp = Dm2_31_exp / Dm2_21_exp

print(f"  Comparison with NuFIT:")
print(f"    Dm^2_31 ratio (pred/obs) = {ratio_31:.4f}")
print(f"    Dm^2_21 ratio (pred/obs) = {ratio_21:.4f}")
print(f"    Dm^2_31/Dm^2_21 (pred)   = {r_3121:.1f}")
print(f"    Dm^2_31/Dm^2_21 (NuFIT)  = {r_3121_exp:.1f}")


# =========================================================================
# PART 9: CAN WE ADJUST y_D3 TO FIT?
# =========================================================================

header("PART 9: Required y_D3 for Correct Dm^2_31")

# With M_R from Hosotani at the target scale, what y_D3 gives the right Dm^2_31?
# Dm^2_31 ~ m_nu3^2 = (m_D3^2 / M_R)^2 = (y_D3 * v/sqrt(2))^4 / M_R^2
# => y_D3 = (Dm^2_31 * M_R^2)^(1/4) * sqrt(2) / v

y_D3_needed = (Dm2_31_exp * 1e-18 * M_R_hosotani**2)**0.25 * np.sqrt(2) / v_EW
m_D3_needed = y_D3_needed * v_EW / np.sqrt(2)

print(f"  To match Dm^2_31 = {Dm2_31_exp:.3e} eV^2 with M_R = {M_R_hosotani:.2e} GeV:")
print(f"    y_D3 = {y_D3_needed:.4f}")
print(f"    m_D3 = {m_D3_needed:.2f} GeV")
print(f"    (For comparison: m_t = 173 GeV, m_b = 4.18 GeV, m_tau = 1.78 GeV)")
print()

# Now recompute with this y_D3
m_D3_fit = m_D3_needed
m_D2_fit = m_D3_fit * lambda_C**2
m_D1_fit = m_D3_fit * lambda_C**4

m_nu3_fit = (m_D3_fit**2 / M_R_hosotani) * 1e9  # eV
m_nu2_fit = (m_D2_fit**2 / M_R_hosotani) * 1e9
m_nu1_fit = (m_D1_fit**2 / M_R_hosotani) * 1e9

Dm2_31_fit = m_nu3_fit**2 - m_nu1_fit**2
Dm2_21_fit = m_nu2_fit**2 - m_nu1_fit**2

print(f"  With y_D3 = {y_D3_needed:.4f}:")
print(f"    m_nu1 = {m_nu1_fit*1e3:.4f} meV")
print(f"    m_nu2 = {m_nu2_fit*1e3:.4f} meV")
print(f"    m_nu3 = {m_nu3_fit:.4f} eV = {m_nu3_fit*1e3:.2f} meV")
print(f"    Sum m_nu = {(m_nu1_fit + m_nu2_fit + m_nu3_fit)*1e3:.2f} meV")
print()
print(f"    Dm^2_31 = {Dm2_31_fit:.4e} eV^2  (NuFIT: {Dm2_31_exp:.3e})  "
      f"ratio: {Dm2_31_fit/Dm2_31_exp:.3f}")
print(f"    Dm^2_21 = {Dm2_21_fit:.4e} eV^2  (NuFIT: {Dm2_21_exp:.3e})  "
      f"ratio: {Dm2_21_fit/Dm2_21_exp:.3f}")
print(f"    Dm^2_31/Dm^2_21 = {Dm2_31_fit/Dm2_21_fit:.1f}  (NuFIT: {r_3121_exp:.1f})")


# =========================================================================
# PART 10: THE RATIO PREDICTION
# =========================================================================

header("PART 10: What IS Predicted vs What Is Fitted")

print(f"""  HONEST ASSESSMENT OF WHAT THE HOSOTANI MECHANISM DOES AND DOES NOT DO:

  WHAT IS PREDICTED (independent of M_R):
  ----------------------------------------
  The RATIO Dm^2_31 / Dm^2_21 depends only on the generation hierarchy:
    Dm^2_31 / Dm^2_21 ~ m_nu3^2 / m_nu2^2 = (m_D3/m_D2)^4
                       = (1/lambda_C^2)^4 = lambda_C^{{-8}}

  With lambda_C = {lambda_C}:
    Predicted: Dm^2_31/Dm^2_21 = {1/lambda_C**8:.1f}
    Observed:  Dm^2_31/Dm^2_21 = {r_3121_exp:.1f}

  This is OFF by a factor of {(1/lambda_C**8)/r_3121_exp:.1f}.
  The pure Cabibbo scaling gives TOO LARGE a hierarchy between
  the solar and atmospheric mass splittings.

  WHAT IS NOT PREDICTED (requires fitting):
  ------------------------------------------
  1. The overall scale M_R (or equivalently L_X)
  2. The Dirac Yukawa coupling y_D3
  3. Both of these are needed to set the absolute neutrino mass scale
""")

# Better ratio: if m_D2/m_D3 is not lambda_C^2 but something else
# What ratio m_D2/m_D3 gives the correct Dm^2_31/Dm^2_21?
# Dm^2_31/Dm^2_21 ~ (m_D3/m_D2)^4 (in the hierarchical limit)
# => m_D2/m_D3 = (Dm^2_21/Dm^2_31)^(1/4)
r_D = (Dm2_21_exp / Dm2_31_exp)**0.25
print(f"  For correct ratio, need m_D2/m_D3 = {r_D:.4f}")
print(f"  This is ~ lambda_C^{np.log(r_D)/np.log(lambda_C):.2f}")
print(f"  Compare: lambda_C = {lambda_C}, lambda_C^2 = {lambda_C**2:.4f}")
print(f"  So the hierarchy should be ~ lambda_C^{{1.2}}, not lambda_C^2")
print()


# =========================================================================
# PART 11: THE EXISTING STUR APPROACH -- REVERSE ENGINEERING
# =========================================================================

header("PART 11: How the Existing Code Gets M_R (and Why It's Circular)")

print(f"""  The existing five_open_problems_closure.py does:
    1. Sets inv_LX_UV = 10^13 GeV (the "UV helix scale")
       -- This is NOT derived; it is ASSUMED
    2. Computes lambda_hol = 3.0 * 1.5 * sqrt(3)*1.2 * 2.1 = 19.8
       -- Each factor is a separate assumption:
          f_base=3: from v*L=3 quantization
          f_loc=1.5: "N_R localization" -- ad hoc
          f_Wilson=2.08: "Wilson line coherence" -- ad hoc
          f_inf=2.1: "infinity-helix kink enhancement" -- ad hoc
    3. M_R = lambda_hol * inv_LX_UV ~ 2e14 GeV
    4. Then sets m_D3 = sqrt(m_nu3 * M_R) -- CIRCULAR!
       This literally inverts the seesaw formula to get m_D3.

  The existing approach is FITTING M_R to match neutrino data,
  then declaring it "derived." It is not derived.
""")


# =========================================================================
# PART 12: WHAT WOULD ACTUALLY WORK
# =========================================================================

header("PART 12: What Would Actually Work")

print(f"""  For the Hosotani mechanism to genuinely predict M_R, we need:

  1. A SECOND compactification scale L' << L_X that is DERIVED,
     not assumed. For example:
     - If the 5th dimension has a warped geometry (Randall-Sundrum-like),
       the effective L at the UV brane could be exponentially small.
     - If there is a second S^1 factor (6D theory), the Hosotani
       mechanism on that circle could give a GUT-scale M_R.

  2. OR: Accept that M_R comes from a different mechanism entirely:
     - Grand unified group breaking (SO(10) -> SM): M_R ~ M_GUT
     - Gravitational effects: M_R ~ v^2 / M_Pl (gives M_R ~ 10^-6 eV, wrong)
     - Type-II seesaw (Higgs triplet): M_R not needed
     - Radiative neutrino mass (scotogenic): M_R ~ TeV

  3. OR: The "enhancement factor" approach, but with DERIVED factors:
     - Show that the wavefunction overlap integral on S^1/Z_3
       contains a factor ~ 10^12 from UV/IR mixing
     - This would require the neutrino sector to have a special
       relationship to the orbifold geometry that is currently absent

  BOTTOM LINE:
  The Hosotani mechanism on S^1/Z_3 gives masses ~ 1/L_X ~ v_EW.
  The seesaw scale M_R ~ 10^14 GeV is 12 orders of magnitude higher.
  No reasonable enhancement factor can bridge this gap.
  M_R in STUR is currently a fitted parameter, not a derived one.
""")


# =========================================================================
# PART 13: NUMERICAL SUMMARY
# =========================================================================

header("PART 13: Numerical Summary")

print(f"  Fundamental parameters:")
print(f"    v_EW = {v_EW} GeV")
print(f"    g_2 = {g_2}")
print(f"    sin^2(theta_W) = {sin2_thetaW}")
print(f"    M_Pl = {M_Pl:.2e} GeV")
print(f"")
print(f"  STUR scales:")
print(f"    L_X = 3/v_EW = {L_X_fund:.5f} GeV^-1 = {L_X_fund*hbar_c_m:.2e} m")
print(f"    M_KK = 2pi/L_X = {M_KK_fund:.1f} GeV")
print(f"    1/L_X = {1/L_X_fund:.1f} GeV")
print(f"")
print(f"  Hosotani result (S^1/Z_3 at L = L_X_fund):")
print(f"    theta_min = {theta_min_Z3:.4f} rad = {theta_min_Z3/np.pi:.4f} pi")
print(f"    <A_X> = theta_min / L = {theta_min_Z3/L_X_fund:.2f} GeV")
print(f"    M_R (Hosotani, direct) = g_2 * <A_X> = {g_2 * theta_min_Z3/L_X_fund:.1f} GeV")
print(f"")
print(f"  Required for seesaw (m_nu3 ~ 0.05 eV, y_D3 ~ 1):")
print(f"    M_R ~ 6 x 10^14 GeV")
print(f"    L_X ~ 10^-15 GeV^-1")
print(f"")
print(f"  MISMATCH: {6e14 / (g_2*theta_min_Z3/L_X_fund):.1e}")
print(f"")
print(f"  Existing code's M_R = {19.8e13:.1e} GeV (FITTED, not derived)")
print()

print(f"  {'='*72}")
print(f"  VERDICT: The Hosotani mechanism on S^1/Z_3 with L = 3/v_EW gives")
print(f"  M_R ~ O(v_EW) ~ 100 GeV. The seesaw needs M_R ~ 10^14 GeV.")
print(f"  The discrepancy is ~10^12. The existing code's M_R is fitted.")
print(f"  Deriving M_R from geometry remains an OPEN PROBLEM in STUR.")
print(f"  {'='*72}")
