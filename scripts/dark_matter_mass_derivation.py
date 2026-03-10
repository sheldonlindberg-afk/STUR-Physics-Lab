#!/usr/bin/env python3
"""
DARK MATTER MASS DERIVATION — RESOLVING THE 8.4× DISCREPANCY
=============================================================

STUR Framework: Dark Matter from S¹/∞₃ Compactification

THE PROBLEM:
  - Holonomy calculation gives M_DM ≈ 7.7 TeV
  - Matching Planck Ω_DM h² = 0.120 requires M_DM ≈ 0.92 TeV
  - Factor of 8.4× discrepancy

THIS SCRIPT:
  a. Computes the KK spectrum on S¹/∞₃ for the R-field
  b. Identifies the lightest ∞₃-odd mode (DM candidate)
  c. Computes its mass from the KK scale + holonomy corrections
  d. Computes the relic density via WIMP freeze-out
  e. Finds the self-consistent M_DM that gives Ω h² = 0.120
  f. Systematically explores whether the 8× gap can be resolved

Physical constants:
  M_Pl = 1.22e19 GeV, v_EW = 246.22 GeV, Ω_DM h² = 0.1200 ± 0.0012

Author: STUR Physics Lab — Dark Matter Sector
Date: 2026-03-10
"""

import numpy as np
from scipy.optimize import brentq
import warnings
warnings.filterwarnings('ignore')

# ═══════════════════════════════════════════════════════════════════════════
# PHYSICAL CONSTANTS
# ═══════════════════════════════════════════════════════════════════════════
M_Pl = 1.2209e19          # GeV (Planck mass)
v_EW = 246.22             # GeV (Higgs VEV)
alpha_em = 1 / 137.036    # Fine structure constant
sin2_W = 0.2312           # sin²θ_W at M_Z
g_Y = np.sqrt(4 * np.pi * alpha_em / (1 - sin2_W))  # U(1)_Y coupling
g_2 = np.sqrt(4 * np.pi * alpha_em / sin2_W)        # SU(2)_L coupling
alpha_s_MZ = 0.1179       # Strong coupling at M_Z
hbar_c = 1.9733e-16       # GeV·m (conversion factor)
G_F = 1.1664e-5           # GeV⁻² (Fermi constant)

# Observed
Omega_DM_obs = 0.1200     # Planck 2018 central value
sigma_Omega = 0.0012      # Planck 1σ uncertainty

# SM degrees of freedom at various temperatures
g_star_full = 106.75      # All SM DOF active


def header(title):
    print(f"\n{'═' * 72}")
    print(f"  {title}")
    print(f"{'═' * 72}\n")


# ═══════════════════════════════════════════════════════════════════════════
# PART 1: KK SPECTRUM ON S¹/∞₃ FOR THE R-FIELD
# ═══════════════════════════════════════════════════════════════════════════
header("PART 1: KK Spectrum on S¹/∞₃")

print("  Geometry: M⁴ × S¹/Z₃ where Z₃ acts as X → X + L_X/3")
print("  The R-field Φ(x,X) expands in KK modes on the orbifold:")
print("    Φ(x,X) = Σ_n φ^(n)(x) · exp(2πi n X / L_X)")
print()
print("  Under Z₃: X → X + L_X/3")
print("    φ^(n) → ω^n φ^(n),  where ω = exp(2πi/3)")
print()
print("  Z₃ charges:")
print("    n mod 3 = 0: charge 0 (Z₃-even, SM sector)")
print("    n mod 3 = 1: charge 1 (Z₃-odd)")
print("    n mod 3 = 2: charge 2 (Z₃-odd)")
print()

# STUR claims two characteristic scales:
# 1. Fundamental: L_X^fund ~ 10⁻³² m → 1/L_X ~ 10¹⁶ GeV (GUT scale)
# 2. Effective:   L_eff ~ 0.8 μm    → 1/L_eff ~ 0.25 eV

# The fundamental KK scale
L_X_fund_m = 1e-32         # m
M_KK_fund = 2 * np.pi * hbar_c / L_X_fund_m   # GeV
print(f"  Fundamental scale: L_X = {L_X_fund_m:.0e} m")
print(f"    → M_KK = 2π/L_X = {M_KK_fund:.2e} GeV  (GUT scale — far too heavy for DM)")

# The effective scale
L_eff_m = 0.8e-6            # m
L_eff_GeV_inv = L_eff_m / hbar_c   # GeV⁻¹
M_KK_eff = 2 * np.pi / L_eff_GeV_inv  # GeV
print(f"\n  Effective scale: L_eff = {L_eff_m:.1e} m = 0.8 μm")
print(f"    → M_KK = 2π/L_eff = {M_KK_eff:.3e} GeV = {M_KK_eff:.3f} eV")
print(f"    (sub-eV — far too light for WIMP DM)")

# The "holonomy mass" that was previously claimed
# M_DM = 3/L_eff (with holonomy corrections)
M_DM_holonomy_naive = 3.0 / L_eff_GeV_inv  # GeV
print(f"\n  Previous 'holonomy mass' M_DM = 3/L_eff = {M_DM_holonomy_naive:.3e} GeV")
print(f"    = {M_DM_holonomy_naive*1e9:.2f} neV — this is nonsensical for a WIMP!")

# KK spectrum for modes n = 1..10
print(f"\n  KK spectrum (first 10 modes) at fundamental scale:")
print(f"  {'n':>4s}  {'Z₃ charge':>10s}  {'m_n (GeV)':>14s}  {'Role':>20s}")
print(f"  {'─'*4}  {'─'*10}  {'─'*14}  {'─'*20}")
for n in range(0, 11):
    z3_charge = n % 3
    m_n = n * M_KK_fund / (2 * np.pi) * (2 * np.pi)  # n/L_X
    # Actually m_n = n * (2π/L_X) / (2π) = n/L_X ... no, standard KK: m_n = n/R
    m_n = n / (L_X_fund_m / hbar_c)  # n/L_X in GeV
    role = "SM" if z3_charge == 0 else f"Z₃-odd (q={z3_charge})"
    if n == 0:
        role = "SM (zero mode)"
    elif n == 1:
        role += " ← DM candidate"
    print(f"  {n:>4d}  {z3_charge:>10d}  {m_n:>14.3e}  {role:>20s}")


# ═══════════════════════════════════════════════════════════════════════════
# PART 2: THE HOLONOMY MASS CALCULATION (REPRODUCING THE 7.7 TEV CLAIM)
# ═══════════════════════════════════════════════════════════════════════════
header("PART 2: Reproducing the Holonomy Mass Calculation")

print("  The DARK_MATTER_RELIC_DENSITY.md document calculates:")
print("    M_LKP² = M_KK² + Δm²_hol")
print()
print("  where the holonomy contribution is:")
print("    Δm²_hol ~ (g_Y² / 16π²) × v² × f_hol(κ)")
print("    f_hol(κ) ~ κ⁴ × exp(κ²/2)")
print("    κ = 2.52 (localization parameter)")
print()

kappa = 2.52
f_hol_kappa = kappa**4 * np.exp(kappa**2 / 2)
Delta_m2_hol = (g_Y**2 / (16 * np.pi**2)) * v_EW**2 * f_hol_kappa

M_DM_holonomy = np.sqrt(abs(Delta_m2_hol))

print(f"  κ = {kappa}")
print(f"  f_hol(κ) = κ⁴ exp(κ²/2) = {f_hol_kappa:.2e}")
print(f"  g_Y = {g_Y:.4f}")
print(f"  Δm²_hol = (g_Y²/16π²) × v² × f_hol = {Delta_m2_hol:.3e} GeV²")
print(f"  M_DM(holonomy) = √(Δm²_hol) = {M_DM_holonomy:.0f} GeV = {M_DM_holonomy/1e3:.2f} TeV")

# Check: the document claims ~7.7 TeV
# Let's see what values reproduce 7.7 TeV
M_target_hol = 7700  # GeV
print(f"\n  Target: M_DM ≈ 7.7 TeV = 7700 GeV")
print(f"  Our calculation: M_DM = {M_DM_holonomy:.0f} GeV = {M_DM_holonomy/1e3:.2f} TeV")
print(f"\n  NOTE: The g_Y²/16π² formula gives only ~210 GeV.")
print(f"  The 7.7 TeV claim in DARK_MATTER_RELIC_DENSITY.md uses:")
print(f"    Δm²_hol ~ (0.36²/158) × 246² × 1.2×10⁶")
print(f"  The factor '1.2×10⁶' is claimed to be f_hol(κ), but our")
print(f"  calculation gives f_hol(2.52) = {f_hol_kappa:.0f}, not 1.2×10⁶.")
print(f"  This 1243× inflation factor is NOT justified in the document.")

# Alternative form from the document text:
# Δm²_hol ~ (0.36² / 158) × (246 GeV)² × 1.2 × 10⁶
Delta_m2_alt = (0.36**2 / 158) * 246**2 * 1.2e6
M_DM_alt = np.sqrt(Delta_m2_alt)
print(f"\n  Alternative (from document text):")
print(f"    Δm²_hol ~ (0.36²/158) × 246² × 1.2×10⁶ = {Delta_m2_alt:.2e} GeV²")
print(f"    M_DM = {M_DM_alt:.0f} GeV = {M_DM_alt/1e3:.1f} TeV")

# Use the larger of the two as "the holonomy prediction"
M_DM_hol = max(M_DM_holonomy, M_DM_alt)
print(f"\n  ═══════════════════════════════════════════════")
print(f"  HOLONOMY PREDICTION: M_DM = {M_DM_hol:.0f} GeV = {M_DM_hol/1e3:.1f} TeV")
print(f"  ═══════════════════════════════════════════════")


# ═══════════════════════════════════════════════════════════════════════════
# PART 3: Z₃-CHARGED MASS SPECTRUM WITH HOLONOMY SPLITTING
# ═══════════════════════════════════════════════════════════════════════════
header("PART 3: Z₃-Charged Mass Spectrum with Holonomy Splitting")

print("  On S¹/Z₃, the Z₃-charged modes get mass contributions:")
print("    m_n² = (n/R)² + v_R² · f(holonomy)")
print()
print("  For the R-field with VEV v_R and topological constraint v·L_X = 3:")

# The topological constraint
v_R_times_L_X = 3.0  # dimensionless

# If we use fundamental scale:
v_R_fund = v_R_times_L_X / (L_X_fund_m / hbar_c)  # GeV
print(f"  v_R (fundamental) = 3/L_X = {v_R_fund:.2e} GeV  (~ M_GUT)")

# The Z₃ orbifold splits the KK tower:
# For n = 3k (Z₃-even): m_n = n/R (no extra holonomy contribution)
# For n = 3k+1 or 3k+2 (Z₃-odd): m_n² = (n/R)² + Δm²_hol

# At fundamental scale, the Z₃-odd DM candidate (n=1):
m_1_fund = np.sqrt((1 / (L_X_fund_m / hbar_c))**2 + Delta_m2_hol)
print(f"\n  n=1 mode at fundamental scale:")
print(f"    m₁² = (1/L_X)² + Δm²_hol")
print(f"    1/L_X = {1/(L_X_fund_m/hbar_c):.2e} GeV")
print(f"    Δm_hol = {M_DM_holonomy:.0f} GeV")
print(f"    m₁ ≈ 1/L_X = {m_1_fund:.2e} GeV  (dominated by KK mass)")
print(f"    → Fundamental scale makes DM candidate a GUT-scale particle!")

print(f"\n  ─── KEY INSIGHT ───")
print(f"  The holonomy mass Δm_hol ~ {M_DM_holonomy/1e3:.1f} TeV is a")
print(f"  SPLITTING between Z₃-even and Z₃-odd modes at the SAME KK level,")
print(f"  not the total mass of the DM candidate.")
print(f"  The total mass is dominated by whichever scale sets 1/L_X.")


# ═══════════════════════════════════════════════════════════════════════════
# PART 4: RELIC DENSITY CALCULATION
# ═══════════════════════════════════════════════════════════════════════════
header("PART 4: WIMP Relic Density — Full Calculation")

# Hypercharge assignments for SM fermions
# Y = Q - T₃ (in SM normalization where Y = Q - T₃)
# But in the hypercharge convention Y_f (where Q = T₃ + Y):
# u_R: Y = 2/3, d_R: Y = -1/3, e_R: Y = -1, ν_R: Y = 0
# Q_L: Y = 1/6, L_L: Y = -1/2

# The Y⁴ sum for the annihilation cross section B^(1) B^(1) → ff̄
# counts hypercharge fourth powers weighted by color:
# Σ_f N_c Y_f⁴

# Right-handed fermions (3 generations):
Y4_uR = 3 * (2/3)**4 * 3     # 3 gens × Y⁴ × N_c
Y4_dR = 3 * (1/3)**4 * 3     # 3 gens × Y⁴ × N_c
Y4_eR = 3 * (1)**4 * 1       # 3 gens × Y⁴ × N_c=1
# Left-handed doublets (3 generations):
Y4_QL = 3 * (1/6)**4 * 3 * 2   # 3 gens × Y⁴ × N_c × (u+d)
Y4_LL = 3 * (1/2)**4 * 1 * 2   # 3 gens × Y⁴ × N_c=1 × (ν+e)

Y4_sum = Y4_uR + Y4_dR + Y4_eR + Y4_QL + Y4_LL

print(f"  Annihilation: B^(1) B^(1) → ff̄  (s-channel hypercharge exchange)")
print(f"  Σ_f N_c Y_f⁴ contributions:")
print(f"    u_R: 3 × (2/3)⁴ × 3 = {Y4_uR:.4f}")
print(f"    d_R: 3 × (1/3)⁴ × 3 = {Y4_dR:.4f}")
print(f"    e_R: 3 × (1)⁴ × 1   = {Y4_eR:.4f}")
print(f"    Q_L: 3 × (1/6)⁴ × 6 = {Y4_QL:.4f}")
print(f"    L_L: 3 × (1/2)⁴ × 2 = {Y4_LL:.4f}")
print(f"    Total: Σ N_c Y⁴ = {Y4_sum:.4f}")

# Annihilation cross section for vector boson DM (KK B^(1))
# ⟨σv⟩ = g_Y⁴ × Σ(N_c Y_f⁴) / (16π M²)
# This is the s-wave piece (velocity-independent part)

def sigma_v_annihilation(M_DM, g_Y_val, Y4, include_coann=False):
    """B^(1) B^(1) → ff̄ annihilation cross section in GeV⁻²."""
    sigma_v = g_Y_val**4 * Y4 / (16 * np.pi * M_DM**2)
    if include_coann:
        sigma_v *= 1.0  # We'll handle coannihilation separately
    return sigma_v

def sigma_v_to_cm3_s(sigma_v_GeV2):
    """Convert from GeV⁻² to cm³/s."""
    # 1 GeV⁻² = 0.389 × 10⁻²⁷ cm²
    # ⟨σv⟩ in cm³/s: multiply by c ≈ 3×10¹⁰ cm/s... but natural units already have c=1
    # In natural units: 1 GeV⁻² = 1.17 × 10⁻¹⁷ cm² (for cross sections)
    # But ⟨σv⟩ has dimensions of volume/time: 1 GeV⁻² = hbar c × (hbar c / hbar) = ...
    # Properly: 1 GeV⁻² = (hbar c)² / (hbar × GeV) × something
    # Standard: 1 pb = 2.568 × 10⁻⁹ GeV⁻²  →  1 GeV⁻² = 3.894 × 10⁸ pb
    # And ⟨σv⟩ in natural units: 1 GeV⁻² = 1.17 × 10⁻¹⁷ cm² × c
    # → 1 GeV⁻² = 1.17e-17 × 3e10 cm³/s ... no.
    # Correct: 1 GeV⁻² (in σv units) = (0.197 fm)² × c
    # = (0.197e-13 cm)² × 3e10 cm/s = 3.88e-27 × 3e10 = 1.16e-16 cm³/s ... too large.
    # Standard reference: ⟨σv⟩_thermal ≈ 3×10⁻²⁶ cm³/s corresponds to ~1 pb = 2.57e-9 GeV⁻²
    # So: 1 GeV⁻² = 3e-26 / 2.57e-9 cm³/s = 1.17e-17 cm³/s
    # Wait, let's be more careful:
    # 1 pb = 10⁻³⁶ cm²; 1 pb = 2.568e-9 GeV⁻²
    # ⟨σv⟩: if we quote σv in pb (cross section × velocity, with v~c=1 in natural units)
    # then σv [cm³/s] = σ [cm²] × v [cm/s] ≈ σ [cm²] × c [cm/s]
    # Actually in natural units σv has dimensions of length² = 1/energy² (in natural units)
    # Converting: 1 GeV⁻² = (ℏc)² [in cm] = (1.97e-14 cm)² = 3.89e-28 cm²
    # For σv: multiply by c: 3.89e-28 × 3e10 = 1.17e-17 cm³/s
    return sigma_v_GeV2 * 1.17e-17  # cm³/s


# Freeze-out calculation
def compute_x_f(M_DM, sigma_v_val, g_eff_dof=2, g_star=106.75):
    """Iteratively compute freeze-out parameter x_f = M/T_f."""
    # x_f = ln[0.038 × (g_eff/√g_*) × M_Pl × M × ⟨σv⟩] - 0.5 ln(x_f)
    # Iterate starting from x_f = 25
    x = 25.0
    for _ in range(20):
        arg = 0.038 * (g_eff_dof / np.sqrt(g_star)) * M_Pl * M_DM * sigma_v_val
        if arg > 0:
            x_new = np.log(arg) - 0.5 * np.log(x)
            x = x_new
        if x < 1:
            x = 1
    return x


def relic_density(M_DM, sigma_v_val, x_f, g_star=106.75):
    """Compute Ω h² from standard Lee-Weinberg formula."""
    # Ω h² = 1.07 × 10⁹ × x_f / (M_Pl × √g_* × ⟨σv⟩) [GeV⁻¹ units]
    # where M_Pl is in GeV and ⟨σv⟩ is in GeV⁻²
    return 1.07e9 * x_f / (M_Pl * np.sqrt(g_star) * sigma_v_val)


# ═══════════════════════════════════════════════════════════════════════════
# PART 4a: RELIC DENSITY FOR M_DM = 7.7 TeV (HOLONOMY PREDICTION)
# ═══════════════════════════════════════════════════════════════════════════
header("PART 4a: Relic Density at Holonomy-Predicted Mass")

M_hol = M_DM_hol  # ~ 7.7 TeV
sv_hol = sigma_v_annihilation(M_hol, g_Y, Y4_sum)
xf_hol = compute_x_f(M_hol, sv_hol)
Omega_hol = relic_density(M_hol, sv_hol, xf_hol)
sv_hol_cm3s = sigma_v_to_cm3_s(sv_hol)

print(f"  M_DM = {M_hol:.0f} GeV = {M_hol/1e3:.1f} TeV (holonomy prediction)")
print(f"  ⟨σv⟩ = {sv_hol:.3e} GeV⁻²  = {sv_hol_cm3s:.3e} cm³/s")
print(f"  x_f = {xf_hol:.1f}  (T_f = {M_hol/xf_hol:.0f} GeV)")
print(f"  Ω_DM h² = {Omega_hol:.3f}")
print(f"  Planck:   Ω_DM h² = {Omega_DM_obs}")
print(f"  Ratio: Ω_predicted / Ω_observed = {Omega_hol/Omega_DM_obs:.1f}")
print()
print(f"  RESULT: At M_DM = {M_hol/1e3:.1f} TeV, B^(1) is OVERPRODUCED")
print(f"  by a factor of {Omega_hol/Omega_DM_obs:.1f}×.")
print(f"  The cross section is too small (∝ 1/M²), so freeze-out happens")
print(f"  too early, leaving too many relics.")


# ═══════════════════════════════════════════════════════════════════════════
# PART 4b: RELIC DENSITY FOR M_DM = 0.92 TeV (FITTED VALUE)
# ═══════════════════════════════════════════════════════════════════════════
header("PART 4b: Relic Density at Fitted Mass")

M_fit = 920.0  # GeV
sv_fit = sigma_v_annihilation(M_fit, g_Y, Y4_sum)
xf_fit = compute_x_f(M_fit, sv_fit)
Omega_fit = relic_density(M_fit, sv_fit, xf_fit)
sv_fit_cm3s = sigma_v_to_cm3_s(sv_fit)

print(f"  M_DM = {M_fit:.0f} GeV = {M_fit/1e3:.2f} TeV (fitted to Planck)")
print(f"  ⟨σv⟩ = {sv_fit:.3e} GeV⁻²  = {sv_fit_cm3s:.3e} cm³/s")
print(f"  x_f = {xf_fit:.1f}  (T_f = {M_fit/xf_fit:.0f} GeV)")
print(f"  Ω_DM h² = {Omega_fit:.3f}")
print(f"  Planck:   Ω_DM h² = {Omega_DM_obs}")
print(f"  Deviation: {abs(Omega_fit - Omega_DM_obs)/sigma_Omega:.1f}σ")


# ═══════════════════════════════════════════════════════════════════════════
# PART 4c: FIND SELF-CONSISTENT M_DM FOR Ω h² = 0.120
# ═══════════════════════════════════════════════════════════════════════════
header("PART 4c: Self-Consistent M_DM for Ω h² = 0.120")

def Omega_of_M(M_DM):
    """Relic density as a function of DM mass (no coannihilation)."""
    sv = sigma_v_annihilation(M_DM, g_Y, Y4_sum)
    xf = compute_x_f(M_DM, sv)
    return relic_density(M_DM, sv, xf)

# Scan masses
M_scan = np.logspace(2, 5, 500)  # 100 GeV to 100 TeV
Omega_scan = np.array([Omega_of_M(M) for M in M_scan])

# Find M where Ω = 0.120
# Ω is monotonically increasing with M (∝ M² roughly)
# Find the crossing
try:
    M_self_consistent = brentq(lambda M: Omega_of_M(M) - 0.120, 100, 1e5)
except:
    M_self_consistent = None

if M_self_consistent:
    sv_sc = sigma_v_annihilation(M_self_consistent, g_Y, Y4_sum)
    xf_sc = compute_x_f(M_self_consistent, sv_sc)
    Omega_sc = Omega_of_M(M_self_consistent)
    print(f"  Self-consistent solution (B^(1) only, no coannihilation):")
    print(f"    M_DM = {M_self_consistent:.0f} GeV = {M_self_consistent/1e3:.3f} TeV")
    print(f"    ⟨σv⟩ = {sv_sc:.3e} GeV⁻²")
    print(f"    x_f = {xf_sc:.1f}")
    print(f"    Ω h² = {Omega_sc:.4f}")
else:
    print(f"  No self-consistent solution found in [100 GeV, 100 TeV]")

# With coannihilation
def Omega_of_M_coann(M_DM, f_coann=1.9):
    """Relic density including coannihilation enhancement factor."""
    sv = sigma_v_annihilation(M_DM, g_Y, Y4_sum) * f_coann
    xf = compute_x_f(M_DM, sv)
    return relic_density(M_DM, sv, xf)

try:
    M_sc_coann = brentq(lambda M: Omega_of_M_coann(M) - 0.120, 100, 1e5)
except:
    M_sc_coann = None

if M_sc_coann:
    sv_c = sigma_v_annihilation(M_sc_coann, g_Y, Y4_sum) * 1.9
    xf_c = compute_x_f(M_sc_coann, sv_c)
    print(f"\n  With coannihilation (f_coann = 1.9):")
    print(f"    M_DM = {M_sc_coann:.0f} GeV = {M_sc_coann/1e3:.3f} TeV")
    print(f"    ⟨σv⟩_eff = {sv_c:.3e} GeV⁻²")
    print(f"    x_f = {xf_c:.1f}")
    print(f"    Ω h² = {Omega_of_M_coann(M_sc_coann):.4f}")

print(f"\n  ═══════════════════════════════════════════════════════════════")
print(f"  DISCREPANCY:")
print(f"    Holonomy prediction:  M_DM = {M_DM_hol:.0f} GeV = {M_DM_hol/1e3:.1f} TeV")
if M_self_consistent:
    print(f"    Relic-consistent:     M_DM = {M_self_consistent:.0f} GeV = {M_self_consistent/1e3:.3f} TeV")
    print(f"    Ratio: {M_DM_hol/M_self_consistent:.1f}×")
if M_sc_coann:
    print(f"    Relic (w/ coann):     M_DM = {M_sc_coann:.0f} GeV = {M_sc_coann/1e3:.3f} TeV")
    print(f"    Ratio: {M_DM_hol/M_sc_coann:.1f}×")
print(f"  ═══════════════════════════════════════════════════════════════")


# ═══════════════════════════════════════════════════════════════════════════
# PART 5: SYSTEMATIC EXPLORATION OF RESOLUTION MECHANISMS
# ═══════════════════════════════════════════════════════════════════════════
header("PART 5: Can the 8× Discrepancy Be Resolved?")

# ═══════════════════════════════════════════════
# Mechanism 1: Coannihilation effects
# ═══════════════════════════════════════════════
print("  ─── MECHANISM 1: Coannihilation Effects ───")
print()
print("  In UED-type models, the KK spectrum is nearly degenerate.")
print("  Coannihilation with KK leptons/quarks increases σ_eff.")
print()
print("  The coannihilation enhancement factor f_coann:")
print("    f_coann = σ_eff / σ(B^(1)B^(1))")
print()

# Scan over coannihilation factors needed to make M_hol work
f_needed = None
try:
    def Omega_hol_coann(f):
        sv = sigma_v_annihilation(M_hol, g_Y, Y4_sum) * f
        xf = compute_x_f(M_hol, sv)
        return relic_density(M_hol, sv, xf)

    f_needed = brentq(lambda f: Omega_hol_coann(f) - 0.120, 1, 1000)
except:
    # If relic density at f=1000 is still too high, report
    Omega_at_f1000 = Omega_hol_coann(1000)
    print(f"  Even with f_coann = 1000: Ω h² = {Omega_at_f1000:.3f}")

if f_needed:
    print(f"  To get Ω h² = 0.120 at M_DM = {M_hol/1e3:.1f} TeV:")
    print(f"    f_coann needed = {f_needed:.1f}")
    print()
    print(f"  Typical UED coannihilation: f_coann ~ 1.5 - 3")
    print(f"  Required: f_coann = {f_needed:.1f}")
    if f_needed > 5:
        print(f"  → INSUFFICIENT: f_coann = {f_needed:.1f} is far beyond realistic")
        print(f"    coannihilation in any known extra-dimension model.")
        print(f"    The largest values in mUED are f ~ 3-5.")
    else:
        print(f"  → POTENTIALLY VIABLE with strong coannihilation.")
else:
    print(f"  → Cannot resolve the discrepancy via coannihilation alone.")

# ═══════════════════════════════════════════════
# Mechanism 2: Sommerfeld Enhancement
# ═══════════════════════════════════════════════
print()
print("  ─── MECHANISM 2: Sommerfeld Enhancement ───")
print()
print("  For non-relativistic DM, long-range forces enhance σv:")
print("    S = (πα/v) / (1 - exp(-πα/v))")
print("  At freeze-out: v ~ 1/√x_f ~ 0.2")
print()

alpha_Y = g_Y**2 / (4 * np.pi)
v_fo = 1.0 / np.sqrt(xf_hol)  # typical velocity at freeze-out
S_sommerfeld = (np.pi * alpha_Y / v_fo) / (1 - np.exp(-np.pi * alpha_Y / v_fo))

print(f"  α_Y = g_Y²/4π = {alpha_Y:.4f}")
print(f"  v at freeze-out = 1/√x_f = {v_fo:.3f}")
print(f"  Sommerfeld factor S = {S_sommerfeld:.3f}")
print(f"  Enhancement: only {S_sommerfeld:.1f}× (negligible for weak-scale α)")
print(f"  → INSUFFICIENT: Sommerfeld enhancement is {S_sommerfeld:.2f}×,")
print(f"    need {f_needed:.0f}× to close the gap." if f_needed else "    far from sufficient.")

# ═══════════════════════════════════════════════
# Mechanism 3: Non-thermal production
# ═══════════════════════════════════════════════
print()
print("  ─── MECHANISM 3: Non-Thermal Production ───")
print()
print("  If DM was never in thermal equilibrium, the relic density")
print("  depends on the production mechanism, not on ⟨σv⟩.")
print()
print("  Option A: Freeze-in (FIMP)")
print("    Ω h² ∝ ⟨σv⟩ × M_Pl / M_DM")
print("    Works for very weakly coupled particles (y ~ 10⁻¹²)")
print("    B^(1) has full hypercharge coupling → NOT a FIMP.")
print("    → INCOMPATIBLE with LKP identity.")
print()
print("  Option B: Late decay of heavier particle")
print("    If a heavier Z₃-odd state decays to the LKP after")
print("    freeze-out of the heavier state:")
print("    Ω_LKP = (M_LKP / M_heavy) × Ω_heavy")
print(f"    Need: M_LKP/M_heavy × Ω_heavy = 0.120")
print(f"    If M_heavy = {M_hol/1e3:.1f} TeV and Ω_heavy = {Omega_hol:.1f}:")
print(f"    Then M_LKP = 0.120/Omega_hol × M_heavy = {0.120/Omega_hol * M_hol:.0f} GeV")
print(f"    This gives a LOWER mass, but it's the heavy state mass that's")
print(f"    set by holonomy — the light state mass is ad hoc.")
print(f"    → DOES NOT RESOLVE the fundamental mismatch.")
print()
print("  Option C: Dilution by late entropy injection")
print("    If entropy is injected after freeze-out (e.g., from")
print("    moduli decay), the DM abundance is diluted:")
print("    Ω_final = Ω_thermal / D,  D = entropy dilution factor")
print(f"    Need: D = Ω_hol / Ω_obs = {Omega_hol/Omega_DM_obs:.1f}")
print(f"    → POSSIBLE in principle, but introduces NEW physics")
print(f"      (moduli fields, late decay) not present in STUR's three axioms.")
print(f"      This would be an ad hoc fix, not a derivation.")

# ═══════════════════════════════════════════════
# Mechanism 4: Different DM candidate
# ═══════════════════════════════════════════════
print()
print("  ─── MECHANISM 4: Different DM Candidate ───")
print()
print("  Could the DM be something other than B^(1)?")
print()
print("  Option A: Lightest twisted-sector state")
print("    On S¹/Z₃, twisted sector states live at fixed points.")
print("    Their masses are set by the orbifold geometry, not KK scale.")
print("    PROBLEM: Twisted states typically have string-scale masses")
print("    (~ M_Pl), far too heavy for DM.")
print("    → NOT VIABLE without additional structure.")
print()
print("  Option B: R-field scalar (KK scalar instead of vector)")
print("    The R-field itself (scalar) has KK modes.")
print("    The lightest Z₃-odd scalar has a mass that depends on")
print("    the R-field potential, not just 1/L_X.")
print("    Mass: m_scalar² = (1/L_X)² + λ v_R² + Δm²_hol")
print("    The self-coupling λ is a free parameter in the R-sector.")
print()

# If DM is a scalar with adjustable potential:
# We need M_scalar ~ 0.92 TeV but holonomy gives the KK vector at 7.7 TeV
# The scalar could be lighter if λ v_R² partially cancels Δm²_hol
# But this is fine-tuning
print("    For the scalar mass to be ~0.92 TeV while the vector is ~7.7 TeV:")
print("    Need: m_scalar²/m_vector² ~ (0.92/7.7)² ~ 0.014")
print("    This requires ~99% cancellation in the scalar mass → FINE-TUNING")
print("    → NOT NATURAL")
print()
print("  Option C: Hidden sector DM (not from KK tower)")
print("    If there's a hidden sector with its own DM candidate,")
print("    the mass is set by hidden-sector dynamics.")
print("    But this introduces new parameters beyond the three axioms.")
print("    → ABANDONS the 'everything from 3 axioms' claim.")

# ═══════════════════════════════════════════════
# Mechanism 5: Correcting the holonomy calculation
# ═══════════════════════════════════════════════
print()
print("  ─── MECHANISM 5: Is the Holonomy Calculation Wrong? ───")
print()
print("  The holonomy mass comes from:")
print("    Δm²_hol = (g_Y²/16π²) × v² × f_hol(κ)")
print(f"    f_hol(κ) = κ⁴ exp(κ²/2) = {f_hol_kappa:.1f} for κ = {kappa}")
print()
print("  The exponential factor exp(κ²/2) grows VERY fast:")
for k in [1.0, 1.5, 2.0, 2.52, 3.0]:
    fh = k**4 * np.exp(k**2 / 2)
    m_pred = np.sqrt((g_Y**2 / (16 * np.pi**2)) * v_EW**2 * fh)
    print(f"    κ = {k:.2f}: f_hol = {fh:>10.1f}  →  M_DM = {m_pred:>8.0f} GeV = {m_pred/1e3:>6.2f} TeV")

# What κ gives 0.92 TeV?
M_target = 920.0  # GeV
f_hol_needed = (M_target**2 * 16 * np.pi**2) / (g_Y**2 * v_EW**2)
print(f"\n  For M_DM = 920 GeV: need f_hol = {f_hol_needed:.1f}")

# Solve κ⁴ exp(κ²/2) = f_hol_needed
# This requires numerical solution
try:
    kappa_needed = brentq(lambda k: k**4 * np.exp(k**2/2) - f_hol_needed, 0.1, 10)
    print(f"  → κ = {kappa_needed:.3f}")
    print(f"  vs κ = {kappa} (used in holonomy calculation)")
    print(f"  Ratio: {kappa/kappa_needed:.2f}× — only a {(kappa/kappa_needed - 1)*100:.0f}% change in κ")
    print(f"  BUT: κ is derived from the localization of wavefunctions on the")
    print(f"  orbifold, and is NOT a free parameter. Changing κ from {kappa} to")
    print(f"  {kappa_needed:.2f} would require a different orbifold geometry.")
except:
    print(f"  Cannot find κ that gives f_hol = {f_hol_needed:.1f}")

print()
print("  CRITICAL POINT: The f_hol(κ) formula itself is suspect.")
print("  It comes from a one-loop radiative correction to the KK mass,")
print("  analogous to UED boundary-localized terms. The factor κ⁴ exp(κ²/2)")
print("  grows so steeply that small changes in κ have enormous effects.")
print("  The derivation of κ = 2.52 should be checked rigorously.")


# ═══════════════════════════════════════════════════════════════════════════
# PART 6: WHAT DETERMINES M_DM IN STUR?
# ═══════════════════════════════════════════════════════════════════════════
header("PART 6: What Actually Determines M_DM in STUR?")

print("  The dark matter mass in STUR depends on:")
print()
print("  1. KK SCALE (1/L_X):")
print(f"     At fundamental scale: 1/L_X ~ {1/(L_X_fund_m/hbar_c):.1e} GeV (GUT)")
print(f"     At effective scale:   1/L_eff ~ {1/L_eff_GeV_inv:.2e} GeV (sub-eV)")
print(f"     NEITHER gives TeV-scale DM directly.")
print()
print("  2. HOLONOMY SPLITTING:")
print(f"     Δm_hol = {M_DM_holonomy:.0f} GeV = {M_DM_holonomy/1e3:.1f} TeV")
print(f"     This gives the Z₃-odd/even mass SPLITTING, not the absolute mass.")
print(f"     At fundamental scale, this splitting is negligible vs 1/L_X ~ 10¹⁶ GeV.")
print(f"     At effective scale, the splitting DOMINATES over 1/L_eff ~ 0.25 eV.")
print()
print("  3. THE REAL ISSUE:")
print("     STUR has TWO compactification scales and no clear mechanism")
print("     for selecting which one determines the DM mass:")
print(f"     • L_X^fund ~ 10⁻³² m: gives DM at GUT scale (too heavy)")
print(f"     • L_eff ~ 0.8 μm: gives DM at sub-eV scale (too light)")
print(f"     • Holonomy 'correction': gives DM at ~{M_DM_holonomy/1e3:.1f} TeV")
print(f"       but only when applied to the sub-eV base mass")
print()
print("  4. THE CIRCULAR LOGIC:")
print("     The '7.7 TeV holonomy mass' was obtained by computing a")
print("     one-loop radiative correction to the KK mass, using the")
print("     Higgs VEV v = 246 GeV and a localization parameter κ = 2.52.")
print("     The holonomy 'form factor' f_hol(κ) = κ⁴ exp(κ²/2) blows up")
print("     exponentially, making the correction LARGER than the base mass.")
print("     This signals a BREAKDOWN of perturbation theory:")
print("     when the 'correction' exceeds the 'base', the expansion is invalid.")


# ═══════════════════════════════════════════════════════════════════════════
# PART 7: HONEST ASSESSMENT
# ═══════════════════════════════════════════════════════════════════════════
header("PART 7: Honest Assessment — Can the Mismatch Be Resolved?")

print("  ╔══════════════════════════════════════════════════════════════════╗")
print("  ║               DARK MATTER MASS: HONEST STATUS                  ║")
print("  ╠══════════════════════════════════════════════════════════════════╣")
print("  ║                                                                ║")
print("  ║  Holonomy prediction:   M_DM ≈ {:<6.1f} TeV                    ║".format(M_DM_hol/1e3))
if M_self_consistent:
    print("  ║  Planck-consistent:     M_DM ≈ {:<6.3f} TeV                    ║".format(M_self_consistent/1e3))
print("  ║  Discrepancy:           {:<5.1f}×                                ║".format(M_DM_hol/M_self_consistent if M_self_consistent else 0))
print("  ║                                                                ║")
print("  ║  MECHANISM ANALYSIS:                                           ║")
print("  ║  1. Coannihilation:     Need f={:<4.0f} (max realistic ~3-5)    ║".format(f_needed if f_needed else 0))
print("  ║  2. Sommerfeld:         Factor {:<5.2f}× (negligible)           ║".format(S_sommerfeld))
print("  ║  3. Non-thermal:        Introduces ad hoc parameters           ║")
print("  ║  4. Different candidate: Requires fine-tuning or new sector    ║")
print("  ║  5. Wrong holonomy calc: Perturbation theory breakdown         ║")
print("  ║                                                                ║")
print("  ║  NONE of these mechanisms can naturally bridge the 8× gap.     ║")
print("  ║                                                                ║")
print("  ╚══════════════════════════════════════════════════════════════════╝")

print()
print("  DIAGNOSIS:")
print()
print("  The fundamental problem is that STUR does not have a UNIQUE")
print("  compactification scale that gives TeV-scale dark matter.")
print()
print("  1. The 'holonomy mass' of ~7.7 TeV is computed from a radiative")
print("     correction formula that uses κ = 2.52, derived from wavefunction")
print("     localization. But f_hol = κ⁴ exp(κ²/2) ~ 1090 is so large that")
print("     the 'correction' dominates over the base mass. This means:")
print("     → The perturbative calculation is unreliable")
print("     → The true mass requires non-perturbative treatment")
print()
print("  2. The relic-density-consistent mass of ~0.92 TeV was obtained by")
print("     INVERTING the freeze-out formula: given Ω h² = 0.120, what M")
print("     gives the right abundance? This is NOT a prediction — it's a")
print("     constraint FROM observation that STUR must satisfy.")
print()
print("  3. To actually PREDICT M_DM from first principles, STUR needs:")
print("     a) A definite compactification radius R = L_X/(2π)")
print("     b) A definite holonomy background (Wilson line VEV)")
print("     c) A self-consistent calculation where Δm_hol ≪ m_KK")
print("        (perturbative regime) or a non-perturbative treatment")
print()
print("  4. The 8.4× mismatch cannot be resolved by any of the standard")
print("     mechanisms (coannihilation, Sommerfeld, non-thermal production)")
print("     because the required enhancement factors are too large to be")
print("     physical in a weakly-coupled WIMP scenario.")

print()
print("  ═══════════════════════════════════════════════════════════════")
print("  CONCLUSION:")
print("  ═══════════════════════════════════════════════════════════════")
print("  The dark matter mass M_DM = 0.92 TeV is NOT derivable from")
print("  STUR's three axioms. It is a FITTED parameter, reverse-")
print("  engineered from the Planck measurement of Ω_DM h² = 0.120.")
print()
print("  The holonomy calculation giving 7.7 TeV is itself unreliable")
print("  because f_hol(κ) ≫ 1 signals perturbation theory breakdown.")
print("  Even if we trust it, no standard mechanism can reduce 7.7 TeV")
print("  to 0.92 TeV without introducing ad hoc ingredients.")
print()
print("  WHAT'S FUNDAMENTALLY WRONG:")
print("  STUR lacks a mechanism to SET the compactification radius at a")
print("  scale that yields TeV-mass KK modes. The Casimir-holonomy balance")
print("  gives L_eff ~ 0.8 μm (sub-eV KK modes), and the fundamental scale")
print("  gives L_X ~ 10⁻³² m (GUT-scale KK modes). The TeV scale does not")
print("  emerge naturally from either.")
print()
print("  STATUS: M_DM = UNRESOLVED (fitted, not derived)")
print("          Ω_DM h² = TAUTOLOGICAL (follows from fitted M_DM)")
print("  ═══════════════════════════════════════════════════════════════")


# ═══════════════════════════════════════════════════════════════════════════
# PART 8: NUMERICAL SUMMARY TABLE
# ═══════════════════════════════════════════════════════════════════════════
header("PART 8: Numerical Summary")

print(f"  {'Quantity':<35s}  {'Value':>15s}  {'Comment'}")
print(f"  {'─'*35}  {'─'*15}  {'─'*40}")
print(f"  {'g_Y (hypercharge coupling)':<35s}  {g_Y:>15.4f}  {'at M_Z scale'}")
print(f"  {'Σ N_c Y_f⁴':<35s}  {Y4_sum:>15.4f}  {'SM fermion sum'}")
print(f"  {'κ (localization parameter)':<35s}  {kappa:>15.2f}  {'from orbifold geometry'}")
print(f"  {'f_hol(κ) = κ⁴ exp(κ²/2)':<35s}  {f_hol_kappa:>15.1f}  {'holonomy form factor'}")
print(f"  {'M_DM (holonomy)':<35s}  {M_DM_hol:>12.0f} GeV  {f'{M_DM_hol/1e3:.1f} TeV'}")
if M_self_consistent:
    print(f"  {'M_DM (relic, no coann)':<35s}  {M_self_consistent:>12.0f} GeV  {f'{M_self_consistent/1e3:.3f} TeV, for Ω=0.120'}")
if M_sc_coann:
    print(f"  {'M_DM (relic, f_coann=1.9)':<35s}  {M_sc_coann:>12.0f} GeV  {f'{M_sc_coann/1e3:.3f} TeV, for Ω=0.120'}")
print(f"  {'Discrepancy ratio':<35s}  {M_DM_hol/M_self_consistent if M_self_consistent else 0:>15.1f}  {'holonomy / relic-consistent'}")
print(f"  {'Ω h² at M_hol = {:.1f} TeV'.format(M_DM_hol/1e3):<35s}  {Omega_hol:>15.2f}  {'vs observed 0.120'}")
print(f"  {'Overproduction factor':<35s}  {Omega_hol/Omega_DM_obs:>15.1f}  {'Ω_predicted / Ω_observed'}")
print(f"  {'f_coann needed at M_hol':<35s}  {f_needed:>15.0f}  {'vs realistic max ~3-5'}" if f_needed else "")
print(f"  {'Sommerfeld enhancement':<35s}  {S_sommerfeld:>15.2f}  {'negligible for α_Y ~ 0.01'}")
if M_self_consistent:
    print(f"  {'κ needed for 920 GeV':<35s}  {kappa_needed:>15.3f}  {f'vs derived κ = {kappa}'}")
print()
print("  Script complete. The 8.4× discrepancy is UNRESOLVED.")
print("  M_DM remains a fitted parameter in the STUR framework.")
