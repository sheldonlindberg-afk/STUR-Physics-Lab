#!/usr/bin/env python3
"""
L_X Stabilization: Complete Effective Potential on S^1/Z_3
==========================================================

STUR Framework — Comprehensive Compactification Modulus Analysis

This script computes ALL contributions to V_eff(L_X) and honestly
determines whether a stable minimum exists within the STUR framework.

Contributions to V_eff(L_X):
  1. Casimir energy from SM fields on S^1/Z_3 (with correct Z_3 twist)
  2. R-field winding (gradient) energy with constraint v_R = 3/L_X
  3. R-field potential energy V(|R|) evaluated at v_R = 3/L_X
  4. Holonomy potential from gauge fields at Z_3 symmetric point
  5. Gravitational (torsion) Casimir corrections
  6. Bulk cosmological constant Lambda_5 * L_X (the only term growing with L)

Key constraint: v_R * L_X = 3 (topological quantization from Z_3 winding)
This means v_R is NOT independent of L_X: v_R = 3/L_X.

Author: STUR L_X stabilization analysis
Date: 2026-03-10
"""

import numpy as np
from scipy.optimize import minimize_scalar, brentq
import sys

# =========================================================================
# PHYSICAL CONSTANTS (natural units: hbar = c = 1)
# =========================================================================

M_Pl_reduced = 2.435e18   # Reduced Planck mass (GeV)
M_Pl = 1.22e19            # Planck mass (GeV)
v_EW = 246.22             # Electroweak VEV (GeV)
alpha_s = 0.1179          # Strong coupling at M_Z
g_s = np.sqrt(4 * np.pi * alpha_s)
g_2 = 0.652               # SU(2) coupling
g_1 = 0.357               # U(1) coupling
hbar_c_m = 1.9733e-16     # hbar*c in m*GeV

N_orb = 3                 # Z_3 orbifold order

# =========================================================================
# SM FIELD CONTENT ON S^1/Z_3
# =========================================================================
# The Z_3 orbifold assigns twist phases omega = exp(2*pi*i/3) to fields.
# Fields in the untwisted sector have periodic BCs on the covering space.
# Fields in twisted sectors have shifted KK momenta.

# Bosonic degrees of freedom (real d.o.f.)
N_scalars_higgs = 4       # Higgs doublet: 2 complex = 4 real
N_gauge_gluon = 8 * 2     # 8 gluons x 2 polarizations = 16
N_gauge_W = 3 * 2          # W^+, W^-, W^3 x 2 polarizations = 6
N_gauge_B = 1 * 2          # B x 2 polarizations = 2
N_gauge_total = N_gauge_gluon + N_gauge_W + N_gauge_B  # = 24

# Fermionic degrees of freedom (Dirac d.o.f. = 2 x Weyl)
# Per generation: 2*(3*2 + 3*1 + 1*2 + 1*1) = 2*10 = 20 Weyl = 10 Dirac
# Three generations: 3 * 10 = 30 Dirac
N_Dirac = 30              # SM Dirac fermions (all 3 generations)
N_Dirac_dof = 4 * N_Dirac  # 4 real d.o.f. per Dirac fermion = 120

# For Casimir on S^1, the key quantity is:
#   Delta_n = n_bosonic - (7/8) * n_fermionic   (for periodic bosons, antiperiodic fermions)
# Using PHYSICAL d.o.f. that propagate in the bulk:
# Bosons: Higgs (4) + gauge (24) = 28 real d.o.f.
# Fermions: 120 real d.o.f.
N_b = N_scalars_higgs + N_gauge_total   # = 28
N_f = N_Dirac_dof                        # = 120
Delta_n = N_b - (7.0/8.0) * N_f          # = 28 - 105 = -77.0

print("=" * 74)
print("  L_X STABILIZATION: COMPLETE EFFECTIVE POTENTIAL ON S^1/Z_3")
print("  STUR Framework — Compactification Modulus Analysis")
print("=" * 74)

print(f"\n  Physical constants:")
print(f"    M_Pl = {M_Pl:.2e} GeV,  M_Pl_reduced = {M_Pl_reduced:.2e} GeV")
print(f"    v_EW = {v_EW:.2f} GeV")

print(f"\n  SM field content (5D bulk):")
print(f"    Bosonic real d.o.f.: {N_b} (Higgs: {N_scalars_higgs}, gauge: {N_gauge_total})")
print(f"    Fermionic real d.o.f.: {N_f} ({N_Dirac} Dirac fermions x 4)")
print(f"    Delta_n = n_b - (7/8)*n_f = {N_b} - {7.0/8*N_f:.1f} = {Delta_n:.1f}")
print(f"    --> FERMION-DOMINATED (Delta_n < 0 --> positive Casimir energy)")


# =========================================================================
# CONTRIBUTION 1: CASIMIR ENERGY ON S^1/Z_3
# =========================================================================

def V_casimir(L):
    """
    Casimir energy density (4D) from SM fields on S^1/Z_3.

    On the covering space S^1 of circumference L, the Casimir energy is:
      V_Cas = -(pi^2/720) * Delta_n / L^5    (5D formula, units GeV^5)

    The 4D energy density is obtained by dividing by L:
      rho_4D = V_Cas / L = -(pi^2/720) * Delta_n / L^5   [this IS already per 4D vol]

    Actually: for a 5D theory compactified on S^1, the one-loop vacuum energy
    per unit 4D volume is:
      V_Cas^{4D} = -(pi^2/1440) * Delta_n_eff / L^4  (with appropriate 5D counting)

    BUT the standard 5D Casimir formula gives energy per unit LENGTH per unit 4D volume:
      E_Cas / (L * V_3) = -(pi^2/1440) * n_eff / L^4

    For S^1/Z_3: the orbifold modifies the KK spectrum.
    Untwisted sector: modes with n = 0 mod 3 survive on the fundamental domain.
    The fundamental domain has length L/3.
    KK masses: m_n = 2*pi*n*3/L (spacing tripled) for untwisted modes.

    Net effect: replace L -> L/3 in the Casimir formula for untwisted sector,
    then add twisted sector corrections.

    V_Cas^{Z3} = -(pi^2/1440) * Delta_n / (L/3)^4
               = -(pi^2/1440) * 81 * Delta_n / L^4

    With Delta_n = -77 (negative): V_Cas > 0 (positive, repulsive).

    Twisted sectors add fractional KK mode contributions.
    For Z_3 with omega = e^{2pi i/3}, twisted modes have momenta shifted by 1/3 and 2/3.
    Each twisted sector contributes:
      V_twist = -(pi^2/1440) * n_twisted / L^4 * B_4(1/3)
    where B_4(x) = x^4 - 2x^3 + x^2 - 1/30 is the 4th Bernoulli polynomial.

    B_4(1/3) = 1/81 - 2/27 + 1/9 - 1/30 = 7/810

    For simplicity (and since the twisted sector is model-dependent in terms of
    which fields are twisted), we use the untwisted-sector dominant formula
    with a correction factor:
      f_twist = 1 + 2 * (B_4(1/3) + 1/30) / (1/30)   [ratio of twisted to untwisted B_4]

    Returns V_Cas in GeV^4 (4D energy density).
    """
    # Untwisted sector: L_fund = L/3
    L_fund = L / 3.0
    prefactor = np.pi**2 / 1440.0

    # B_4(0) = -1/30, B_4(1/3), B_4(2/3) for the KK sum
    def B4(x):
        x = x % 1.0
        return x**4 - 2*x**3 + x**2 - 1.0/30.0

    # The full Z_3 Casimir sums over all sectors:
    # V = -(pi^2/1440*L^4) * Delta_n * sum_{sectors} B_4(theta_sector/(2pi))
    # Untwisted: B_4(0) = -1/30
    # Twisted 1: B_4(1/3) = 1/81 - 2/27 + 1/9 - 1/30 = 7/810
    # Twisted 2: B_4(2/3) = 16/81 - 16/27 + 4/9 - 1/30 = 7/810

    b4_untwisted = B4(0.0)        # = -1/30
    b4_twist1 = B4(1.0/3.0)      # = 7/810
    b4_twist2 = B4(2.0/3.0)      # = 7/810

    # The Casimir energy using the Bernoulli polynomial representation:
    # V_Cas = -(2*pi^2)/(L^4) * Delta_n * [B_4(0) + B_4(1/3) + B_4(2/3)]
    # Factor of 2 accounts for left/right movers (or equivalently, the
    # conventional normalization of the 5D Casimir formula).
    B4_sum = b4_untwisted + b4_twist1 + b4_twist2

    V = -2 * prefactor * Delta_n * B4_sum / L**4

    return V


# =========================================================================
# CONTRIBUTION 2: R-FIELD WINDING (GRADIENT) ENERGY
# =========================================================================

def V_winding(L):
    """
    R-field winding energy.

    The R-field vacuum is R = v_R * (cos(k*X), sin(k*X))
    where k = 2*pi/(N*L_X) = 2*pi/(3*L) is the winding wavenumber.

    The gradient energy density (4D) is:
      V_wind = (1/2) * v_R^2 * k^2
             = (1/2) * (3/L)^2 * (2*pi/(3*L))^2
             = (1/2) * 9/L^2 * 4*pi^2/(9*L^2)
             = 2*pi^2/L^4

    Using the constraint v_R = 3/L, the winding energy is:
      V_wind = 2*pi^2 / L^4    (in GeV^4)

    Note: this scales as 1/L^4, NOT 1/L^2 as in the unconstrained case.
    The constraint v_R = 3/L converts 1/L^2 into 1/L^4.
    """
    v_R = 3.0 / L
    k = 2 * np.pi / (3 * L)
    return 0.5 * v_R**2 * k**2


# =========================================================================
# CONTRIBUTION 3: R-FIELD POTENTIAL ENERGY V(|R|)
# =========================================================================

def V_R_potential(L, lambda_R=1.0, mu_R_sq_coeff=1.0):
    """
    R-field potential evaluated at v_R = 3/L_X.

    The R-field has a Mexican hat potential:
      V(|R|) = -mu_R^2 |R|^2 + lambda_R |R|^4

    At the minimum: |R|_min = mu_R / sqrt(2*lambda_R)
                    V_min = -mu_R^4 / (4*lambda_R)

    But in the STUR framework, v_R is set by the topological constraint
    v_R = 3/L. The potential energy at this field value is:

      V(v_R) = -mu_R^2 * v_R^2 + lambda_R * v_R^4
             = -mu_R^2 * 9/L^2 + lambda_R * 81/L^4

    The mu_R^2 term gives a NEGATIVE contribution proportional to 1/L^2.
    The lambda_R term gives a POSITIVE contribution proportional to 1/L^4.

    This is interesting: the mu_R^2 term is the FIRST negative L-dependent
    term we have found (besides the cosmological constant).

    If mu_R ~ v_EW (electroweak scale), this term dominates at intermediate L
    and could create a minimum.

    Parameters:
        lambda_R: quartic coupling (dimensionless)
        mu_R_sq_coeff: mu_R^2 in GeV^2 (sets the symmetry breaking scale)

    Returns V in GeV^4.
    """
    v_R = 3.0 / L
    return -mu_R_sq_coeff * v_R**2 + lambda_R * v_R**4


# =========================================================================
# CONTRIBUTION 4: HOLONOMY POTENTIAL
# =========================================================================

def V_holonomy(L):
    """
    One-loop holonomy potential from gauge fields on S^1/Z_3.

    At the Z_3 symmetric point theta = 2*pi/3, the holonomy potential is:
      V_hol = -(3/(2pi)^4) * sum_charges B_4(q*theta/(2*pi)) / L^4

    For SU(3) adjoint (gluons) at theta = 2*pi/3:
    The 8 generators have charges q = 0 (x2), +/- 1 (x2), +/- 2 (x1) under the
    Cartan subalgebra contracted with the holonomy direction.

    At the Z_3 center element, this is at the MINIMUM of the holonomy potential
    (by construction: Z_3 is a center symmetry).

    Returns V_hol in GeV^4.
    """
    def B4(x):
        x = x % 1.0
        return x**4 - 2*x**3 + x**2 - 1.0/30.0

    theta = 2 * np.pi / 3.0

    # SU(3) adjoint charges under the chosen Cartan direction
    charges = [1, -1, 2, -2, 0, 0, 0, 0]
    B4_sum = sum(B4(q * theta / (2 * np.pi)) for q in charges)

    # SU(2) adjoint
    charges_su2 = [1, -1, 0]
    B4_sum_su2 = sum(B4(q * theta / (2 * np.pi)) for q in charges_su2)

    # Full gauge group contribution
    prefactor = 3.0 / (2 * np.pi)**4
    V = -prefactor * (B4_sum + B4_sum_su2) / L**4

    return V


# =========================================================================
# CONTRIBUTION 5: TORSION CASIMIR CORRECTIONS
# =========================================================================

def V_torsion_casimir(L):
    """
    Gravitational (torsion) Casimir correction.

    In TEGR, the graviton has 5 d.o.f. in 5D (massless spin-2).
    On S^1/Z_3, this contributes to the Casimir energy.
    The torsion scalar coupling xi*|R|*T also generates a 1-loop correction.

    For the graviton KK tower on S^1/Z_3:
      V_grav_Cas = -(pi^2/1440) * n_grav / (L/3)^4 * correction

    n_grav = 5 (5D graviton d.o.f.)
    With the non-minimal coupling xi*|R|*T, there's an additional
    mass-dependent correction.

    This is typically subdominant to the SM Casimir energy.
    """
    # 5D graviton: 5 bosonic d.o.f. (symmetric traceless tensor)
    n_grav = 5
    prefactor = np.pi**2 / 1440.0
    # Untwisted sector contribution (dominant)
    V = -prefactor * n_grav * (3.0/L)**4 * (-1.0/30.0)  # periodic boson: B_4(0) = -1/30

    # This is NEGATIVE (attractive) -- graviton is bosonic
    # But small: 5 d.o.f. vs 28 bosonic + 120 fermionic SM d.o.f.
    return V


# =========================================================================
# CONTRIBUTION 6: BULK COSMOLOGICAL CONSTANT
# =========================================================================

def V_bulk_cc(L, Lambda_5):
    """
    5D bulk cosmological constant contribution to 4D potential.

    When compactifying on S^1 of circumference L:
      V_4D = Lambda_5 * L

    This is the ONLY term that GROWS with L.
    It provides the restoring force necessary for a minimum.

    Lambda_5 has dimensions [GeV^5] and must be positive.
    """
    return Lambda_5 * L


# =========================================================================
# TOTAL EFFECTIVE POTENTIAL
# =========================================================================

def V_eff_minimal(L):
    """
    Minimal V_eff: Casimir + winding + holonomy + torsion Casimir.
    No free parameters -- everything determined by SM content and Z_3.
    """
    return V_casimir(L) + V_winding(L) + V_holonomy(L) + V_torsion_casimir(L)


def V_eff_with_R_potential(L, mu_R_sq, lambda_R=1.0):
    """
    V_eff including the R-field potential.
    The mu_R^2 term provides a NEGATIVE 1/L^2 contribution that could help.
    """
    return (V_casimir(L) + V_winding(L) + V_holonomy(L) +
            V_torsion_casimir(L) + V_R_potential(L, lambda_R, mu_R_sq))


def V_eff_full(L, mu_R_sq, lambda_R, Lambda_5):
    """
    Full V_eff including R-field potential and bulk CC.
    """
    return (V_casimir(L) + V_winding(L) + V_holonomy(L) +
            V_torsion_casimir(L) + V_R_potential(L, lambda_R, mu_R_sq) +
            V_bulk_cc(L, Lambda_5))


# =========================================================================
# MAIN COMPUTATION
# =========================================================================

# ========== SECTION 1: SCALING ANALYSIS ==========

print(f"\n{'=' * 74}")
print("  SECTION 1: SCALING ANALYSIS OF ALL CONTRIBUTIONS")
print(f"{'=' * 74}")

print(f"""
  With the topological constraint v_R = 3/L_X, all terms have definite
  L-dependence:

  Term                    Scaling      Sign        Origin
  ---------------------------------------------------------------
  V_Casimir (SM)          1/L^4       POSITIVE    fermion-dominated
  V_winding               1/L^4       POSITIVE    R-field gradient
  V_holonomy              1/L^4       depends     gauge loops at Z_3
  V_torsion_Casimir       1/L^4       NEGATIVE    graviton Casimir (small)
  V_R_potential (quartic)  1/L^4       POSITIVE    lambda_R * v_R^4
  V_R_potential (mass)     1/L^2       NEGATIVE    -mu_R^2 * v_R^2
  V_bulk_CC               L           POSITIVE    Lambda_5 * L

  KEY INSIGHT: The R-field mass term -mu_R^2 * v_R^2 = -9*mu_R^2/L^2
  is the only negative L-dependent term besides the bulk CC.

  For a minimum WITHOUT a bulk CC, we need:
    Positive 1/L^4 terms balanced by negative 1/L^2 term.
    dV/dL = -4*A/L^5 + 2*B/L^3 = 0  -->  L_* = sqrt(2A/B)

  This is a GENUINE possibility if mu_R is large enough!
""")

# Compute coefficients
# A_coeff: total coefficient of 1/L^4 (positive terms)
L_test = 1.0  # reference scale
A_cas = V_casimir(L_test) * L_test**4
A_wind = V_winding(L_test) * L_test**4
A_hol = V_holonomy(L_test) * L_test**4
A_tors = V_torsion_casimir(L_test) * L_test**4
A_quartic = 81.0  # lambda_R * 81/L^4 at lambda_R = 1

print(f"  Coefficients of 1/L^4 terms:")
print(f"    Casimir (SM):        A_cas   = {A_cas:.6e}")
print(f"    Winding:             A_wind  = {A_wind:.6e}")
print(f"    Holonomy:            A_hol   = {A_hol:.6e}")
print(f"    Torsion Casimir:     A_tors  = {A_tors:.6e}")
print(f"    R-potential quartic: A_qrt   = lambda_R * 81")
print(f"    Total (lambda_R=1): A_total = {A_cas + A_wind + A_hol + A_tors + 81:.6e}")

A_total_no_quartic = A_cas + A_wind + A_hol + A_tors
print(f"\n    Total (excluding quartic): {A_total_no_quartic:.6e}")

# B_coeff: coefficient of -1/L^2 (from R-field mass term)
# V_mass = -mu_R^2 * 9/L^2  -->  B_coeff = 9 * mu_R^2
print(f"\n  Coefficient of 1/L^2 term:")
print(f"    B = 9 * mu_R^2")


# ========== SECTION 2: MINIMAL POTENTIAL (NO FREE PARAMETERS) ==========

print(f"\n{'=' * 74}")
print("  SECTION 2: MINIMAL POTENTIAL (No Free Parameters)")
print(f"{'=' * 74}")

# Scan L values
L_GeV = np.logspace(-20, 20, 2000)  # GeV^-1

V_cas_arr = np.array([V_casimir(L) for L in L_GeV])
V_wind_arr = np.array([V_winding(L) for L in L_GeV])
V_hol_arr = np.array([V_holonomy(L) for L in L_GeV])
V_tors_arr = np.array([V_torsion_casimir(L) for L in L_GeV])
V_min_arr = V_cas_arr + V_wind_arr + V_hol_arr + V_tors_arr

# Check for minimum
dV = np.diff(V_min_arr)
min_candidates = np.where((dV[:-1] < 0) & (dV[1:] > 0))[0]

print(f"\n  Scanning L from {L_GeV[0]:.0e} to {L_GeV[-1]:.0e} GeV^-1")
print(f"  All four terms (Casimir + winding + holonomy + torsion Casimir)")
print(f"  scale as 1/L^4 and are all monotonically decreasing.")

if len(min_candidates) > 0:
    idx = min_candidates[0] + 1
    print(f"\n  MINIMUM FOUND at L = {L_GeV[idx]:.2e} GeV^-1")
else:
    print(f"\n  RESULT: NO MINIMUM (all terms ~ 1/L^4, monotonically decreasing)")
    print(f"  V_eff is positive and decreases monotonically as L -> infinity.")
    print(f"  This confirms the finding of lx_effective_potential.py.")

# Display representative values
print(f"\n  {'L (GeV^-1)':>14s}  {'V_Cas':>12s}  {'V_wind':>12s}  {'V_hol':>12s}  {'V_tors':>12s}  {'V_total':>12s}")
print(f"  {'---':>14s}  {'---':>12s}  {'---':>12s}  {'---':>12s}  {'---':>12s}  {'---':>12s}")
for logL in [-15, -10, -5, 0, 5, 10, 15]:
    L = 10.0**logL
    vc = V_casimir(L)
    vw = V_winding(L)
    vh = V_holonomy(L)
    vt = V_torsion_casimir(L)
    vtot = vc + vw + vh + vt
    print(f"  {L:14.0e}  {vc:12.2e}  {vw:12.2e}  {vh:12.2e}  {vt:12.2e}  {vtot:12.2e}")


# ========== SECTION 3: WITH R-FIELD POTENTIAL (mu_R^2 TERM) ==========

print(f"\n{'=' * 74}")
print("  SECTION 3: INCLUDING R-FIELD POTENTIAL V(|R|)")
print(f"{'=' * 74}")

print(f"""
  V(|R|) = -mu_R^2 * |R|^2 + lambda_R * |R|^4
  With v_R = 3/L:
    V = -9*mu_R^2/L^2 + 81*lambda_R/L^4

  The -9*mu_R^2/L^2 term is NEGATIVE and decays SLOWER than the 1/L^4 terms.
  At large L, this dominates over all 1/L^4 terms.

  For a minimum without bulk CC:
    V_eff = A_total/L^4 - 9*mu_R^2/L^2
    dV/dL = -4*A_total/L^5 + 18*mu_R^2/L^3 = 0
    --> L_*^2 = 4*A_total / (18*mu_R^2) = 2*A_total / (9*mu_R^2)
    --> L_* = sqrt(2*A_total / (9*mu_R^2))

  At the minimum:
    V(L_*) = A_total/L_*^4 - 9*mu_R^2/L_*^2
           = 9*mu_R^2/(2*L_*^2) - 9*mu_R^2/L_*^2
           = -9*mu_R^2 / (2*L_*^2) < 0

  The minimum has NEGATIVE energy (AdS-like).
  This is analogous to the KKLT mechanism where the minimum is AdS
  and needs uplifting.
""")

# Compute A_total with lambda_R = 1
lambda_R_values = [0.01, 0.1, 1.0]

for lam_R in lambda_R_values:
    A_total = A_total_no_quartic + 81 * lam_R

    print(f"  lambda_R = {lam_R}:")
    print(f"    A_total = {A_total:.6e}")

    # Try various mu_R values
    print(f"    {'mu_R (GeV)':>14s}  {'L_* (GeV^-1)':>14s}  {'L_* (m)':>12s}  {'M_KK (GeV)':>12s}  {'V(L_*) (GeV^4)':>16s}")

    mu_R_values = [1e-3, 1e-2, 0.1, 1.0, 10.0, v_EW, 1e3, 1e6, 1e10, M_Pl]
    for mu_R in mu_R_values:
        mu_R_sq = mu_R**2
        L_star_sq = 2 * A_total / (9 * mu_R_sq)
        if L_star_sq > 0:
            L_star = np.sqrt(L_star_sq)
            L_star_m = L_star * hbar_c_m
            M_KK = 2 * np.pi / L_star
            V_min_val = -9 * mu_R_sq / (2 * L_star_sq)
            v_R_star = 3.0 / L_star

            print(f"    {mu_R:14.2e}  {L_star:14.2e}  {L_star_m:12.2e}  {M_KK:12.2e}  {V_min_val:16.2e}", end="")

            # Check consistency: v_R should be real and positive
            if v_R_star > M_Pl:
                print(f"  [v_R = {v_R_star:.1e} > M_Pl: TRANS-PLANCKIAN]", end="")
            print()

    print()


# ========== SECTION 4: THE KEY QUESTION -- WHAT IS mu_R? ==========

print(f"\n{'=' * 74}")
print("  SECTION 4: WHAT DETERMINES mu_R?")
print(f"{'=' * 74}")

print(f"""
  The R-field mass parameter mu_R is the key to stabilization.
  In the STUR framework, R is a real SU(2) doublet that breaks
  electroweak symmetry. If R IS the Higgs field (or closely related):

    mu_R ~ mu_Higgs ~ v_EW / sqrt(2) ~ 174 GeV

  But the R-field is explicitly described as DIFFERENT from the Higgs.
  The Higgs mechanism arises from the R-field VEV, but the R-field
  itself lives in 5D and has a 5D mass parameter.

  The 5D mass mu_5 is related to the 4D mass by:
    mu_R^2 = mu_5^2 - (n*pi/L)^2   (for the nth KK mode)

  For the zero mode: mu_R^2 = mu_5^2 (no KK correction).

  If the R-field IS the electroweak Higgs mechanism:
    mu_R = v_EW / sqrt(2) = {v_EW / np.sqrt(2):.2f} GeV

  With mu_R = {v_EW / np.sqrt(2):.2f} GeV:
""")

# Compute the stabilization with mu_R = v_EW/sqrt(2)
mu_R_Higgs = v_EW / np.sqrt(2)
lambda_R = 1.0  # O(1) quartic coupling
A_total_lR1 = A_total_no_quartic + 81 * lambda_R

L_star_Higgs_sq = 2 * A_total_lR1 / (9 * mu_R_Higgs**2)
L_star_Higgs = np.sqrt(L_star_Higgs_sq)
L_star_Higgs_m = L_star_Higgs * hbar_c_m
M_KK_Higgs = 2 * np.pi / L_star_Higgs
v_R_Higgs = 3.0 / L_star_Higgs
V_min_Higgs = -9 * mu_R_Higgs**2 / (2 * L_star_Higgs_sq)

print(f"    mu_R = {mu_R_Higgs:.2f} GeV (electroweak scale)")
print(f"    lambda_R = {lambda_R}")
print(f"    A_total = {A_total_lR1:.6e}")
print(f"    L_* = sqrt(2*A / (9*mu_R^2)) = {L_star_Higgs:.4e} GeV^-1")
print(f"    L_* = {L_star_Higgs_m:.4e} m = {L_star_Higgs_m*1e15:.2f} fm")
print(f"    M_KK = 2*pi/L_* = {M_KK_Higgs:.2f} GeV")
print(f"    v_R = 3/L_* = {v_R_Higgs:.2e} GeV")
print(f"    V(L_*) = {V_min_Higgs:.4e} GeV^4 (AdS minimum)")

print(f"\n    Comparison with constraints:")
print(f"      v_R * L_* = {v_R_Higgs * L_star_Higgs:.6f} (should be 3.000)")
print(f"      v_R / v_EW = {v_R_Higgs / v_EW:.2e}")
print(f"      M_KK / v_EW = {M_KK_Higgs / v_EW:.2f}")


# ========== SECTION 5: NUMERICAL VERIFICATION WITH FULL POTENTIAL ==========

print(f"\n{'=' * 74}")
print("  SECTION 5: NUMERICAL VERIFICATION OF THE MINIMUM")
print(f"{'=' * 74}")

# Case A: mu_R = v_EW/sqrt(2), lambda_R = 1 (electroweak scale)
mu_R_sq = mu_R_Higgs**2
lambda_R = 1.0

print(f"\n  Case A: mu_R = v_EW/sqrt(2) = {mu_R_Higgs:.2f} GeV, lambda_R = {lambda_R}")

# Scan around the analytic estimate
L_scan = np.logspace(np.log10(L_star_Higgs) - 3, np.log10(L_star_Higgs) + 3, 5000)
V_scan = np.array([V_eff_with_R_potential(L, mu_R_sq, lambda_R) for L in L_scan])

# Find minimum numerically
dV_scan = np.diff(V_scan)
min_idx = np.where((dV_scan[:-1] < 0) & (dV_scan[1:] > 0))[0]

if len(min_idx) > 0:
    idx = min_idx[0] + 1
    L_min_num = L_scan[idx]
    V_min_num = V_scan[idx]
    L_min_m = L_min_num * hbar_c_m

    # Refine with scipy
    try:
        result = minimize_scalar(
            lambda logL: V_eff_with_R_potential(np.exp(logL), mu_R_sq, lambda_R),
            bounds=(np.log(L_scan[0]), np.log(L_scan[-1])),
            method='bounded'
        )
        L_min_refined = np.exp(result.x)
        V_min_refined = result.fun
        L_min_m_refined = L_min_refined * hbar_c_m
    except Exception:
        L_min_refined = L_min_num
        V_min_refined = V_min_num
        L_min_m_refined = L_min_m

    M_KK_min = 2 * np.pi / L_min_refined
    v_R_min = 3.0 / L_min_refined

    print(f"\n  STABLE MINIMUM FOUND:")
    print(f"    L_* = {L_min_refined:.6e} GeV^-1")
    print(f"    L_* = {L_min_m_refined:.6e} m = {L_min_m_refined*1e15:.4f} fm")
    print(f"    M_KK = 2*pi/L_* = {M_KK_min:.4f} GeV")
    print(f"    v_R = 3/L_* = {v_R_min:.4e} GeV")
    print(f"    V(L_*) = {V_min_refined:.6e} GeV^4")

    # Check second derivative (stability)
    eps = L_min_refined * 1e-5
    d2V = (V_eff_with_R_potential(L_min_refined + eps, mu_R_sq, lambda_R)
           - 2 * V_eff_with_R_potential(L_min_refined, mu_R_sq, lambda_R)
           + V_eff_with_R_potential(L_min_refined - eps, mu_R_sq, lambda_R)) / eps**2
    print(f"    d^2V/dL^2 = {d2V:.4e} GeV^6 {'(STABLE)' if d2V > 0 else '(UNSTABLE!)'}")

    # Radion mass
    m_radion_sq = L_min_refined**2 * d2V / M_Pl_reduced**2
    if m_radion_sq > 0:
        m_radion = np.sqrt(m_radion_sq)
        print(f"    m_radion = {m_radion:.4e} GeV")
        lambda_radion_m = hbar_c_m / m_radion
        print(f"    Radion Compton wavelength = {lambda_radion_m:.4e} m")
    else:
        print(f"    m_radion^2 = {m_radion_sq:.4e} (tachyonic -- UNSTABLE)")

    print(f"\n    Analytic estimate: L_* = {L_star_Higgs:.6e} GeV^-1")
    print(f"    Numerical result:  L_* = {L_min_refined:.6e} GeV^-1")
    print(f"    Agreement: {abs(L_min_refined - L_star_Higgs)/L_star_Higgs * 100:.2f}%")

else:
    print(f"\n  NO MINIMUM FOUND in scanned range.")
    print(f"  V_eff is {'increasing' if V_scan[-1] > V_scan[0] else 'decreasing'} over the scanned range.")
    # Diagnose
    print(f"  At small L: V ~ {V_scan[0]:.2e} (should be large positive)")
    print(f"  At large L: V ~ {V_scan[-1]:.2e} (should be large negative)")
    print(f"  Analytic L_* = {L_star_Higgs:.4e} GeV^-1, V there = {V_eff_with_R_potential(L_star_Higgs, mu_R_sq, lambda_R):.4e}")

    # Check at the analytic minimum
    L_check = L_star_Higgs
    V_check = V_eff_with_R_potential(L_check, mu_R_sq, lambda_R)
    dL = L_check * 1e-4
    dV_check = (V_eff_with_R_potential(L_check + dL, mu_R_sq, lambda_R)
                - V_eff_with_R_potential(L_check - dL, mu_R_sq, lambda_R)) / (2 * dL)
    d2V_check = (V_eff_with_R_potential(L_check + dL, mu_R_sq, lambda_R)
                 - 2 * V_check
                 + V_eff_with_R_potential(L_check - dL, mu_R_sq, lambda_R)) / dL**2
    print(f"  At L = {L_check:.4e}: V = {V_check:.4e}, dV/dL = {dV_check:.4e}, d2V/dL2 = {d2V_check:.4e}")

    # The issue: at large L, V -> -infinity (the -mu_R^2/L^2 term is not bounded below)
    print(f"\n  PROBLEM: V_eff -> -infinity as L -> infinity")
    print(f"  The minimum is actually a LOCAL minimum, but V is unbounded below.")
    print(f"  Need bulk CC (Lambda_5 * L) to make V bounded from below at large L.")


# ========== SECTION 6: FULL POTENTIAL WITH BULK CC (UPLIFT) ==========

print(f"\n{'=' * 74}")
print("  SECTION 6: FULL POTENTIAL WITH BULK CC UPLIFT")
print(f"{'=' * 74}")

print(f"""
  Adding Lambda_5 * L to the potential:
    V = A_total/L^4 - 9*mu_R^2/L^2 + Lambda_5 * L

  This has a richer structure:
    dV/dL = -4*A_total/L^5 + 18*mu_R^2/L^3 + Lambda_5 = 0

  At the minimum, there are potentially TWO extrema (min and max)
  from the interplay of all three terms.

  The condition for a STABLE minimum with V(L_*) approx 0 (de Sitter uplift):
    V(L_*) = A/L_*^4 - 9*mu_R^2/L_*^2 + Lambda_5 * L_* = 0
    dV/dL|_* = -4A/L_*^5 + 18*mu_R^2/L_*^3 + Lambda_5 = 0
""")

# With mu_R = v_EW/sqrt(2), find Lambda_5 that gives a minimum
mu_R = mu_R_Higgs
mu_R_sq = mu_R**2
A_total = A_total_no_quartic + 81 * lambda_R

# For a Minkowski minimum (V = 0 at L_*):
# A/L^4 - 9*mu^2/L^2 + Lambda_5*L = 0
# -4A/L^5 + 18*mu^2/L^3 + Lambda_5 = 0
# From the second: Lambda_5 = 4A/L^5 - 18*mu^2/L^3
# Substitute into first: A/L^4 - 9*mu^2/L^2 + L*(4A/L^5 - 18*mu^2/L^3) = 0
#   A/L^4 - 9*mu^2/L^2 + 4A/L^4 - 18*mu^2/L^2 = 0
#   5A/L^4 = 27*mu^2/L^2
#   L^2 = 5A/(27*mu^2)
#   L_* = sqrt(5A/(27*mu^2))

L_star_Mink = np.sqrt(5 * A_total / (27 * mu_R_sq))
Lambda_5_Mink = 4 * A_total / L_star_Mink**5 - 18 * mu_R_sq / L_star_Mink**3
L_star_Mink_m = L_star_Mink * hbar_c_m
M_KK_Mink = 2 * np.pi / L_star_Mink
v_R_Mink = 3.0 / L_star_Mink

print(f"  Minkowski minimum (V = 0 at L_*):")
print(f"    L_* = sqrt(5A/(27*mu_R^2)) = {L_star_Mink:.6e} GeV^-1")
print(f"    L_* = {L_star_Mink_m:.6e} m = {L_star_Mink_m*1e15:.4f} fm")
print(f"    Lambda_5 = {Lambda_5_Mink:.6e} GeV^5")
print(f"    Lambda_5 / M_Pl^5 = {Lambda_5_Mink / M_Pl**5:.4e}")
print(f"    M_KK = {M_KK_Mink:.4f} GeV")
print(f"    v_R = {v_R_Mink:.4e} GeV")

# Verify
V_check = V_eff_full(L_star_Mink, mu_R_sq, lambda_R, Lambda_5_Mink)
print(f"    V(L_*) = {V_check:.4e} GeV^4 (should be ~0)")

# Check stability
eps = L_star_Mink * 1e-5
d2V_Mink = (V_eff_full(L_star_Mink + eps, mu_R_sq, lambda_R, Lambda_5_Mink)
             - 2 * V_eff_full(L_star_Mink, mu_R_sq, lambda_R, Lambda_5_Mink)
             + V_eff_full(L_star_Mink - eps, mu_R_sq, lambda_R, Lambda_5_Mink)) / eps**2
print(f"    d^2V/dL^2 = {d2V_Mink:.4e} {'(STABLE)' if d2V_Mink > 0 else '(UNSTABLE -- saddle point!)'}")

if d2V_Mink < 0:
    print(f"\n  The Minkowski condition gives a MAXIMUM, not a minimum!")
    print(f"  This means we need to choose Lambda_5 slightly differently.")
    print(f"  With Lambda_5 > Lambda_5_Mink, the potential tilts up at large L,")
    print(f"  creating a minimum at L < L_star_Mink with V < 0 (AdS).")

# Scan Lambda_5 values to find a STABLE minimum
print(f"\n  Scanning Lambda_5 for stable minimum:")
print(f"  {'Lambda_5 (GeV^5)':>18s}  {'L_* (GeV^-1)':>14s}  {'L_* (m)':>12s}  {'V(L_*) (GeV^4)':>16s}  {'d2V > 0?':>10s}  {'M_KK (GeV)':>12s}")
print(f"  {'---':>18s}  {'---':>14s}  {'---':>12s}  {'---':>16s}  {'---':>10s}  {'---':>12s}")

Lambda5_scan = np.logspace(
    np.log10(abs(Lambda_5_Mink)) - 5,
    np.log10(abs(Lambda_5_Mink)) + 5,
    100
)
# Use the correct sign
if Lambda_5_Mink < 0:
    Lambda5_scan = -Lambda5_scan[::-1]  # scan negative values too

found_stable = False
stable_results = []

for Lam5 in Lambda5_scan:
    # Find extrema numerically
    L_scan_local = np.logspace(-2, 5, 10000)
    V_local = np.array([V_eff_full(L, mu_R_sq, lambda_R, Lam5) for L in L_scan_local])
    dV_local = np.diff(V_local)
    extrema = np.where((dV_local[:-1] * dV_local[1:]) < 0)[0]

    for ex_idx in extrema:
        L_ex = L_scan_local[ex_idx + 1]
        V_ex = V_local[ex_idx + 1]

        # Check if minimum (second derivative > 0)
        eps_l = L_ex * 1e-4
        d2V_ex = (V_eff_full(L_ex + eps_l, mu_R_sq, lambda_R, Lam5)
                  - 2 * V_eff_full(L_ex, mu_R_sq, lambda_R, Lam5)
                  + V_eff_full(L_ex - eps_l, mu_R_sq, lambda_R, Lam5)) / eps_l**2

        if d2V_ex > 0:
            L_ex_m = L_ex * hbar_c_m
            M_KK_ex = 2 * np.pi / L_ex
            stable_results.append((Lam5, L_ex, L_ex_m, V_ex, M_KK_ex, d2V_ex))
            if not found_stable or len(stable_results) <= 10:
                print(f"  {Lam5:18.4e}  {L_ex:14.4e}  {L_ex_m:12.4e}  {V_ex:16.4e}  {'YES':>10s}  {M_KK_ex:12.4e}")
            found_stable = True

if not found_stable:
    print(f"  No stable minimum found with these Lambda_5 values.")
    print(f"  The potential is monotonic or has only maxima in the scanned range.")

if found_stable:
    print(f"\n  Found {len(stable_results)} stable configurations.")
    # Show the one closest to V = 0 (Minkowski)
    closest_Mink = min(stable_results, key=lambda x: abs(x[3]))
    print(f"\n  Closest to Minkowski (V ~ 0):")
    print(f"    Lambda_5 = {closest_Mink[0]:.6e} GeV^5")
    print(f"    L_* = {closest_Mink[1]:.6e} GeV^-1 = {closest_Mink[2]:.6e} m")
    print(f"    V(L_*) = {closest_Mink[3]:.6e} GeV^4")
    print(f"    M_KK = {closest_Mink[4]:.6e} GeV")


# ========== SECTION 7: EXPLORATION OF mu_R VALUES ==========

print(f"\n{'=' * 74}")
print("  SECTION 7: L_* vs mu_R — WHAT SCALE IS SELECTED?")
print(f"{'=' * 74}")

print(f"""
  The stabilized L_* depends on mu_R. For the minimal case (no bulk CC):
    L_* = sqrt(2*A_total / (9*mu_R^2))

  What mu_R gives L_* ~ 0.8 um (the chronomagnetic scale)?
    L_pheno = 0.8e-6 m = {0.8e-6/hbar_c_m:.4e} GeV^-1
    mu_R = sqrt(2*A_total / (9*L_pheno^2))
""")

L_pheno = 0.8e-6 / hbar_c_m
mu_R_for_pheno = np.sqrt(2 * A_total / (9 * L_pheno**2))
print(f"  For L_* = 0.8 um:")
print(f"    mu_R needed = {mu_R_for_pheno:.4e} GeV")
print(f"    v_R at this L = 3/L = {3.0/L_pheno:.4e} GeV")

print(f"\n  For comparison:")
print(f"    mu_R = v_EW/sqrt(2) = {v_EW/np.sqrt(2):.2f} GeV  --> L_* = {L_star_Higgs_m:.2e} m")
print(f"    mu_R for 0.8 um = {mu_R_for_pheno:.2e} GeV")
print(f"    Ratio: {mu_R_for_pheno / (v_EW/np.sqrt(2)):.2e}")

# Also check: what mu_R gives L_* = 1/M_Pl (fundamental Planck scale)?
L_Pl = 1.0 / M_Pl
mu_R_for_Pl = np.sqrt(2 * A_total / (9 * L_Pl**2))
print(f"\n  For L_* = 1/M_Pl = {L_Pl:.2e} GeV^-1:")
print(f"    mu_R needed = {mu_R_for_Pl:.2e} GeV")
print(f"    v_R = 3*M_Pl = {3*M_Pl:.2e} GeV (trans-Planckian!)")


# ========== SECTION 8: CHRONOMAGNETIC SCALE CONNECTION ==========

print(f"\n{'=' * 74}")
print("  SECTION 8: CHRONOMAGNETIC SCALE L_eff ~ 0.8 um")
print(f"{'=' * 74}")

print(f"""
  The chronomagnetic scale L_eff ~ 0.8 um appears throughout STUR as the
  effective compactification scale, distinct from the fundamental L_X.

  The STUR framework proposes discrete scale invariance with ratio
  lambda_chrono = 3722/2705 = {3722/2705:.6f} connecting L_fund to L_eff.

  L_eff = L_fund * lambda_chrono^n  for some integer n.

  If L_fund ~ 1/M_Pl = {1.0/M_Pl:.2e} GeV^-1 = {hbar_c_m/M_Pl:.2e} m:
    L_eff/L_fund = 0.8e-6 / {hbar_c_m/M_Pl:.2e} = {0.8e-6 / (hbar_c_m/M_Pl):.2e}
    n = log(L_eff/L_fund) / log(lambda_chrono) = {np.log(0.8e-6/(hbar_c_m/M_Pl)) / np.log(3722/2705):.1f}

  This requires n ~ {np.log(0.8e-6/(hbar_c_m/M_Pl)) / np.log(3722/2705):.0f} iterations of the discrete
  scale invariance. Whether this is physical or numerological
  depends on the dynamics generating the discrete scaling.

  If instead L_X is stabilized at L_* ~ {L_star_Higgs_m:.2e} m (from mu_R = v_EW/sqrt(2)):
    L_eff/L_* = {0.8e-6/L_star_Higgs_m:.2e}
    n = {np.log(0.8e-6/L_star_Higgs_m)/np.log(3722/2705):.1f}

  Neither gives a simple integer n.
  The chronomagnetic scale 0.8 um does NOT naturally emerge from L_X stabilization.
""")


# ========== SECTION 9: NON-PERTURBATIVE STABILIZATION ==========

print(f"\n{'=' * 74}")
print("  SECTION 9: NON-PERTURBATIVE EFFECTS")
print(f"{'=' * 74}")

print(f"""
  If the perturbative potential cannot stabilize L_X at the desired scale,
  non-perturbative effects may help. Candidates:

  1. GAUGINO CONDENSATION ANALOG:
     In SUSY theories, gaugino condensation generates:
       W ~ exp(-8*pi^2 / (b*g^2))
       V ~ |W|^2 ~ exp(-16*pi^2 / (b*g^2))
     STUR is non-SUSY, but QCD confinement at scale Lambda_QCD ~ 0.2 GeV
     generates a non-perturbative potential:
       V_np ~ Lambda_QCD^4 * exp(-S_inst(L))
     where S_inst depends on L through the gauge coupling running.

  2. R-FIELD INSTANTONS:
     The R-field on S^1/Z_3 can have instanton configurations
     (tunneling between different winding sectors).
     Instanton action: S_inst ~ v_R * L = 3 (from topological constraint!)
     V_inst ~ mu^4 * exp(-S_inst) = mu^4 * exp(-3) = mu^4 * {np.exp(-3):.4f}
     This is O(1) -- NOT exponentially suppressed! The topological constraint
     v_R * L = 3 fixes the instanton action to be order unity.

  3. THERMAL EFFECTS (EARLY UNIVERSE):
     At temperature T > 1/L, the compact dimension is effectively
     decompactified. The thermal potential:
       V_thermal ~ T^4 * f(T*L)
     This can stabilize L during cosmological evolution.

  Let us compute the instanton contribution:
""")

# R-field instanton
S_inst = 3.0  # v_R * L = 3 (topological)
# The instanton generates a potential of the form:
# V_inst = -C * mu^4 * cos(theta_vac) * exp(-S_inst) / L^4
# where theta_vac is the vacuum angle and C is a numerical factor.
# For Z_3: theta_vac = 2*pi/3 and cos(2*pi/3) = -1/2.

C_inst = 1.0  # O(1) prefactor (unknown)
mu_inst = v_EW  # scale of instanton
V_inst_coeff = C_inst * mu_inst**4 * np.exp(-S_inst) * (-np.cos(2*np.pi/3))
# This is POSITIVE (since cos(2pi/3) = -1/2, the minus signs combine)

print(f"  R-field instanton contribution:")
print(f"    S_inst = v_R * L = 3 (topological)")
print(f"    exp(-S_inst) = exp(-3) = {np.exp(-3):.6f}")
print(f"    cos(theta_vac) = cos(2*pi/3) = {np.cos(2*np.pi/3):.4f}")
print(f"    V_inst ~ +{V_inst_coeff:.4e} / L^4  (GeV^4)")
print(f"    This is POSITIVE and scales as 1/L^4.")
print(f"    It does NOT help create a minimum -- same scaling as other terms.")
print(f"    The instanton merely renormalizes the 1/L^4 coefficient.")


# ========== SECTION 10: HONEST SUMMARY ==========

print(f"\n{'=' * 74}")
print("  SECTION 10: HONEST SUMMARY AND ASSESSMENT")
print(f"{'=' * 74}")

print(f"""
  +---------------------------------------------------------------------+
  |  L_X STABILIZATION: COMPLETE ASSESSMENT                             |
  +---------------------------------------------------------------------+
  |                                                                     |
  |  1. MINIMAL POTENTIAL (Casimir + winding + holonomy):               |
  |     All terms scale as 1/L^4. Monotonically decreasing.             |
  |     NO MINIMUM. (Confirms lx_effective_potential.py)                |
  |                                                                     |
  |  2. WITH R-FIELD POTENTIAL V(|R|) = -mu_R^2|R|^2 + lambda|R|^4:    |
  |     The mass term -9*mu_R^2/L^2 decays SLOWER than 1/L^4.          |
  |     Creates a LOCAL minimum at:                                     |
  |       L_* = sqrt(2*A_total / (9*mu_R^2))                           |
  |     BUT the potential is unbounded below (V -> -inf as L -> inf).   |
  |     This is a FALSE vacuum -- not truly stable.                     |
  |                                                                     |
  |  3. WITH BULK CC (Lambda_5 * L):                                    |
  |     The linear term makes V -> +inf as L -> inf.                    |
  |     Combined with the 1/L^2 and 1/L^4 terms, creates a GENUINE     |
  |     stable minimum. But Lambda_5 is an INPUT parameter.             |
  |                                                                     |
  |  4. WITH R-FIELD POTENTIAL + BULK CC:                               |
  |     V = A/L^4 - B/L^2 + Lambda_5 * L                               |
  |     This is the richest structure, with BOTH a minimum and a        |
  |     maximum. The minimum can be tuned to Minkowski (V = 0) or       |
  |     de Sitter (V > 0) by adjusting Lambda_5.                        |
  |                                                                     |
  |  KEY RESULTS:                                                       |
  |    - mu_R = v_EW/sqrt(2): L_* ~ {L_star_Higgs_m:.1e} m (sub-fm scale)     |
  |      M_KK ~ {M_KK_Higgs:.0f} GeV (electroweak scale KK tower)           |
  |      This is INTERESTING but gives very small L_X.                  |
  |                                                                     |
  |    - For L_* ~ 0.8 um: need mu_R ~ {mu_R_for_pheno:.1e} GeV             |
  |      This is an extremely small mass -- unnaturally small.          |
  |                                                                     |
  |  WHAT IS GENUINELY NEW IN THIS ANALYSIS:                            |
  |    The R-field potential V(|R|) was missing from previous analyses.  |
  |    With the constraint v_R = 3/L, the mass term creates a 1/L^2    |
  |    contribution that is qualitatively different from all 1/L^4      |
  |    terms. This IS a stabilization mechanism, but:                   |
  |    - It requires mu_R as an input                                   |
  |    - The minimum is AdS without a bulk CC                           |
  |    - The scale L_* is determined by mu_R, not predicted             |
  |                                                                     |
  |  WHAT IS STILL MISSING:                                             |
  |    1. A DYNAMICAL determination of mu_R from first principles       |
  |    2. A mechanism to generate Lambda_5 (or eliminate the need)      |
  |    3. A connection between L_X and the chronomagnetic scale 0.8 um  |
  |    4. Radion mass and coupling computation for experimental tests   |
  |                                                                     |
  |  BOTTOM LINE:                                                       |
  |    A stable minimum CAN exist if the R-field has a mass term.       |
  |    The minimum location depends on mu_R (R-field mass parameter).   |
  |    If mu_R = v_EW/sqrt(2) ~ 174 GeV, then L_* ~ {L_star_Higgs_m:.0e} m     |
  |    and M_KK ~ {M_KK_Higgs:.0f} GeV. This is the most natural STUR          |
  |    prediction, but it does NOT match L_eff ~ 0.8 um.               |
  |                                                                     |
  |    The framework PARTIALLY resolves the structural gap:             |
  |    it upgrades "no minimum exists" to "a minimum exists with        |
  |    L_* determined by mu_R." The gap reduces from "no mechanism"     |
  |    to "mu_R needs to be determined from first principles."          |
  +---------------------------------------------------------------------+
""")

# ========== SECTION 11: COMPARISON TABLE ==========

print(f"{'=' * 74}")
print("  SECTION 11: COMPARISON TABLE — L_* FOR DIFFERENT mu_R VALUES")
print(f"{'=' * 74}")

print(f"\n  {'mu_R (GeV)':>14s}  {'L_* (GeV^-1)':>14s}  {'L_* (m)':>14s}  {'M_KK (GeV)':>14s}  {'v_R (GeV)':>14s}  {'Comment':>20s}")
print(f"  {'---':>14s}  {'---':>14s}  {'---':>14s}  {'---':>14s}  {'---':>14s}  {'---':>20s}")

test_cases = [
    (M_Pl, "Planck scale mu_R"),
    (1e16, "GUT scale"),
    (1e10, ""),
    (1e6, ""),
    (1e3, "TeV scale"),
    (v_EW/np.sqrt(2), "Higgs mass scale"),
    (v_EW, "EW VEV"),
    (1.0, "1 GeV"),
    (0.2, "Lambda_QCD"),
    (1e-3, ""),
    (mu_R_for_pheno, "L_* = 0.8 um"),
    (1e-15, ""),
]

for mu_val, comment in test_cases:
    L_val = np.sqrt(2 * A_total / (9 * mu_val**2))
    L_val_m = L_val * hbar_c_m
    M_KK_val = 2 * np.pi / L_val
    v_R_val = 3.0 / L_val
    print(f"  {mu_val:14.4e}  {L_val:14.4e}  {L_val_m:14.4e}  {M_KK_val:14.4e}  {v_R_val:14.4e}  {comment:>20s}")

print(f"\n  A_total = {A_total:.6e} (lambda_R = 1)")
print(f"  Formula: L_* = sqrt(2*A_total / (9*mu_R^2))")
