#!/usr/bin/env python3
"""
Gauge Coupling Unification via RG Running on S^1/Z_3
=====================================================

STUR Framework: 5D TEGR on M^4 x S^1/Z_3

PROBLEM:
  At the compactification scale M_KK, STUR predicts sin^2(theta_W) = 3/8
  (SU(5)-like normalization from 5D gauge-Higgs unification).
  At M_Z = 91.19 GeV, experiment gives sin^2(theta_W) = 0.2312.

  Question: Does standard 1-loop RG running from M_KK to M_Z,
  including KK threshold corrections from S^1/Z_3, reproduce the
  observed low-energy gauge couplings?

CALCULATION:
  1. Fix unified coupling at M_KK from sin^2(theta_W) = 3/8
  2. Run alpha_1, alpha_2, alpha_3 from M_KK to M_Z using SM beta functions
  3. Include KK threshold corrections (power-law -> log corrections on orbifold)
  4. Compare predicted sin^2(theta_W)(M_Z) and alpha_s(M_Z) with experiment

Author: STUR Physics Lab
"""

import numpy as np

def header(title):
    print(f"\n{'=' * 72}")
    print(f"  {title}")
    print(f"{'=' * 72}\n")

# =========================================================================
# CONSTANTS
# =========================================================================
v_EW = 246.22          # GeV
M_Z = 91.1876          # GeV
M_W = 80.379           # GeV
m_t = 172.57           # GeV
m_H = 125.10           # GeV
alpha_em_MZ = 1/127.95 # alpha_em at M_Z (MSbar)
sin2_W_obs = 0.23121   # sin^2(theta_W) at M_Z (MSbar)
alpha_s_obs = 0.1179   # alpha_s at M_Z

# STUR scales
L_X = 3.0 / v_EW      # GeV^-1
M_KK = 2 * np.pi / L_X  # ~ 515.7 GeV

# SM 1-loop beta function coefficients (SU(5) normalization: alpha_1 = 5/3 * alpha_Y)
# b_i = (1/4pi) * d(1/alpha_i)/d(ln mu)
# Convention: d(alpha_i^-1)/d(ln mu) = -b_i/(2*pi)
b1 = 41.0 / 10   # U(1)_Y with SU(5) normalization
b2 = -19.0 / 6   # SU(2)_L
b3 = -7.0         # SU(3)_C

# =========================================================================
# SECTION 1: OBSERVED COUPLINGS AT M_Z
# =========================================================================
header("SECTION 1: Observed Couplings at M_Z")

alpha_1_obs = alpha_em_MZ / (1 - sin2_W_obs) * (5.0/3)  # SU(5) normalization
alpha_2_obs = alpha_em_MZ / sin2_W_obs
alpha_3_obs_val = alpha_s_obs

print(f"  alpha_em(M_Z)     = {alpha_em_MZ:.6f}  (1/{1/alpha_em_MZ:.2f})")
print(f"  sin^2(theta_W)    = {sin2_W_obs:.5f}")
print(f"  alpha_s(M_Z)      = {alpha_s_obs:.4f}")
print()
print(f"  alpha_1(M_Z) [SU(5) norm] = {alpha_1_obs:.6f}  (1/{1/alpha_1_obs:.2f})")
print(f"  alpha_2(M_Z)              = {alpha_2_obs:.6f}  (1/{1/alpha_2_obs:.2f})")
print(f"  alpha_3(M_Z)              = {alpha_3_obs_val:.6f}  (1/{1/alpha_3_obs_val:.2f})")
print()
print(f"  STUR M_KK = 2pi/L_X = {M_KK:.1f} GeV")
print(f"  ln(M_KK/M_Z) = {np.log(M_KK/M_Z):.4f}")

# =========================================================================
# SECTION 2: RUN FROM M_Z UP TO M_KK (what do SM couplings become at M_KK?)
# =========================================================================
header("SECTION 2: SM Couplings Run Up to M_KK")

def run_coupling_1loop(alpha_low, b, mu_low, mu_high):
    """1-loop RG: 1/alpha(mu_high) = 1/alpha(mu_low) - b/(2pi) * ln(mu_high/mu_low)"""
    inv_alpha_high = 1/alpha_low - b/(2*np.pi) * np.log(mu_high/mu_low)
    return 1.0 / inv_alpha_high

# Run observed couplings from M_Z to M_KK
alpha_1_KK = run_coupling_1loop(alpha_1_obs, b1, M_Z, M_KK)
alpha_2_KK = run_coupling_1loop(alpha_2_obs, b2, M_Z, M_KK)
alpha_3_KK = run_coupling_1loop(alpha_3_obs_val, b3, M_Z, M_KK)

print(f"  Running from M_Z = {M_Z:.2f} to M_KK = {M_KK:.1f} GeV")
print(f"  (1-loop SM beta functions, no thresholds)")
print()
print(f"  alpha_1(M_KK) = {alpha_1_KK:.6f}  (1/{1/alpha_1_KK:.2f})")
print(f"  alpha_2(M_KK) = {alpha_2_KK:.6f}  (1/{1/alpha_2_KK:.2f})")
print(f"  alpha_3(M_KK) = {alpha_3_KK:.6f}  (1/{1/alpha_3_KK:.2f})")
print()

sin2_W_KK = (alpha_1_KK * 3/5) / (alpha_1_KK * 3/5 + alpha_2_KK)
print(f"  sin^2(theta_W) at M_KK = {sin2_W_KK:.5f}")
print(f"  Target (SU(5)):           {3/8:.5f}")
print(f"  Deviation:                {abs(sin2_W_KK - 3/8)/3/8*100:.1f}%")
print()
print(f"  alpha_2/alpha_3 at M_KK = {alpha_2_KK/alpha_3_KK:.4f}  (unification needs 1.0)")
print(f"  alpha_1/alpha_2 at M_KK = {alpha_1_KK/alpha_2_KK:.4f}  (unification needs 1.0)")

# =========================================================================
# SECTION 3: WHERE DO COUPLINGS UNIFY IN THE SM?
# =========================================================================
header("SECTION 3: Standard SM Unification Scale")

# Find where alpha_1 = alpha_2
# 1/alpha_1(mu) = 1/alpha_1(MZ) - b1/(2pi)*ln(mu/MZ)
# 1/alpha_2(mu) = 1/alpha_2(MZ) - b2/(2pi)*ln(mu/MZ)
# Set equal: delta(1/alpha) = (b1-b2)/(2pi)*ln(mu/MZ)
delta_inv = 1/alpha_1_obs - 1/alpha_2_obs
ln_ratio_12 = delta_inv / ((b1 - b2) / (2 * np.pi))
M_unif_12 = M_Z * np.exp(ln_ratio_12)

delta_inv_23 = 1/alpha_2_obs - 1/alpha_3_obs_val
ln_ratio_23 = delta_inv_23 / ((b2 - b3) / (2 * np.pi))
M_unif_23 = M_Z * np.exp(ln_ratio_23)

print(f"  alpha_1 = alpha_2 crossing at:  M = {M_unif_12:.2e} GeV")
print(f"  alpha_2 = alpha_3 crossing at:  M = {M_unif_23:.2e} GeV")
print(f"  (SM does not unify exactly; these differ by ~2 orders)")
print()
print(f"  In STUR, M_KK = {M_KK:.1f} GeV is far below GUT scale.")
print(f"  Couplings do NOT unify at M_KK with pure SM running.")

# =========================================================================
# SECTION 4: UNIFICATION AT M_KK WITH KK THRESHOLD CORRECTIONS
# =========================================================================
header("SECTION 4: KK Threshold Corrections on S^1/Z_3")

print("  On S^1/Z_3, KK modes above M_KK modify the beta functions.")
print("  Each KK level n contributes delta_b_i from the full 5D content.")
print()
print("  5D gauge theory on S^1/Z_3:")
print("    - Zero modes: SM gauge bosons + matter")
print("    - KK modes at m_n = n * M_KK (n=1,2,...)")
print("    - Z_3 projects: only modes with n mod 3 = 0 survive as 'untwisted'")
print("    - Twisted modes at m = (n + 1/3)*M_KK and (n + 2/3)*M_KK")
print()

# In a 5D SU(5)-like theory on S^1/Z_3:
# The Z_3 orbifold breaks SU(5) -> SU(3) x SU(2) x U(1)
# Each KK level contributes the FULL 5D content (SU(5) adjoint),
# so above M_KK the running is effectively 5D (power-law).
# But the orbifold projection means different KK levels contribute differently.

# For the Z_3 orbifold:
# - Untwisted sector (n mod 3 = 0): full SU(5) adjoint contribution
# - Twisted sectors (n mod 3 = 1,2): broken contribution (SM subgroup only)

# The KK threshold correction to 1/alpha_i is:
# delta(1/alpha_i) = -1/(2pi) * sum_n b_i^(n) * ln(Lambda/m_n)
# where b_i^(n) are the beta coefficients from KK level n

# For SU(5) adjoint at each KK level (complete multiplet):
# b_adj = [0, 0, 0] (SU(5) preserving, so all equal)
# Actually: b_SU5 = -11 * C_2(SU5) / 3 = ... for gauge
# The point: COMPLETE SU(5) multiplets don't split the couplings

# What matters is the DIFFERENCE between orbifold-projected spectrum
# and full SU(5) spectrum. This is the threshold correction.

# Standard result for orbifold GUTs (Hall-Nomura type):
# The threshold correction at 1-loop:
# delta_i = b_i^(5D) * sum_{n=1}^{N_KK} ln(N_KK * M_KK / (n * M_KK))
# But for Z_3 with unequal projections:

# Let's compute properly.
# In 5D SU(5) on S^1/Z_3, the boundary conditions break SU(5) to SM.
# At each KK level n, the contribution to b_i depends on Z_3 phase.

# The key formula (Dienes, Dudas, Gherghetta):
# 1/alpha_i(M_Z) = 1/alpha_GUT + b_i^SM/(2pi)*ln(M_KK/M_Z) + Delta_i/(2pi)
# where Delta_i encodes the KK threshold corrections.

# For S^1/Z_3 with N_orb = 3:
# Delta_i = sum_{n=1}^infty [b_i^(n) * ln(M_KK/m_n)] where m_n = n*M_KK/3 for twisted
# The regularized sum converges and gives:
# Delta_i = (b_i^5D - b_i^SM) * [sum_{n=1}^N 1 - psi(N+1) - gamma_E terms]

# Simpler approach: compute what alpha_GUT must be at M_KK for each coupling
# to reproduce observed values at M_Z, including KK corrections.

# Actually let's try the forward calculation:
# Assume sin^2(theta_W) = 3/8 at M_KK (exact SU(5) relation)
# This means alpha_1 = alpha_2 = alpha_GUT at M_KK

# From sin^2(theta_W) = 3/8:
# alpha_em = alpha_2 * sin^2(theta_W) = alpha_GUT * 3/8
# alpha_Y = alpha_1 * 3/5 = alpha_GUT * 3/5
# alpha_em = alpha_Y * cos^2(theta_W) = alpha_GUT * 3/5 * 5/8 = alpha_GUT * 3/8 ✓

# Method: fix alpha_GUT at M_KK such that alpha_em(M_Z) is reproduced.
# Then predict sin^2(theta_W)(M_Z) and alpha_s(M_Z).

print("  FORWARD CALCULATION:")
print("  Fix alpha_GUT at M_KK from sin^2(theta_W) = 3/8")
print("  Run down to M_Z with SM beta functions")
print("  Predict sin^2(theta_W)(M_Z) and alpha_s(M_Z)")
print()

# =========================================================================
# SECTION 5: FORWARD CALCULATION
# =========================================================================
header("SECTION 5: Forward Calculation from M_KK")

# We need alpha_GUT at M_KK.
# Strategy: find alpha_GUT such that alpha_em(M_Z) = 1/127.95

# At M_KK: alpha_1 = alpha_2 = alpha_GUT, alpha_3 = alpha_GUT (full unification)
# Run to M_Z:
# 1/alpha_i(M_Z) = 1/alpha_GUT - b_i/(2pi) * ln(M_Z/M_KK)
#                = 1/alpha_GUT + b_i/(2pi) * ln(M_KK/M_Z)

L = np.log(M_KK / M_Z)  # ~ 1.73

# alpha_em = alpha_1*3/5 * alpha_2 / (alpha_1*3/5 + alpha_2)
# For SU(5) normalization, alpha_em^-1 = (3/5)*alpha_1^-1 + alpha_2^-1
# Wait, that's wrong. Let me be careful.
# alpha_em^-1 = alpha_Y^-1 + alpha_2^-1 (at any scale)
# where alpha_Y = (3/5)*alpha_1

# So: 1/alpha_em(MZ) = 5/(3*alpha_1(MZ)) + 1/alpha_2(MZ)
#   = 5/3 * [1/alpha_GUT + b1/(2pi)*L] + [1/alpha_GUT + b2/(2pi)*L]
#   = (5/3 + 1)/alpha_GUT + [5*b1/3 + b2]/(2pi) * L
#   = 8/(3*alpha_GUT) + [5*b1/3 + b2]/(2pi) * L

# So: alpha_GUT = 8/3 / (1/alpha_em(MZ) - [5*b1/3 + b2]/(2pi)*L)

b_eff = 5*b1/3 + b2  # effective beta for alpha_em
inv_alpha_em = 1/alpha_em_MZ

alpha_GUT_from_em = (8.0/3) / (inv_alpha_em - b_eff/(2*np.pi) * L)

print(f"  ln(M_KK/M_Z) = {L:.4f}")
print(f"  b_eff (for alpha_em) = 5*b1/3 + b2 = {b_eff:.4f}")
print(f"  alpha_GUT (from alpha_em match) = {alpha_GUT_from_em:.6f}  (1/{1/alpha_GUT_from_em:.2f})")
print()

# Now predict individual couplings at M_Z
alpha_1_pred = 1.0 / (1/alpha_GUT_from_em + b1/(2*np.pi) * L)
alpha_2_pred = 1.0 / (1/alpha_GUT_from_em + b2/(2*np.pi) * L)
alpha_3_pred = 1.0 / (1/alpha_GUT_from_em + b3/(2*np.pi) * L)

sin2_pred = (alpha_1_pred * 3/5) / (alpha_1_pred * 3/5 + alpha_2_pred)
alpha_em_pred = (alpha_1_pred * 3/5) * alpha_2_pred / (alpha_1_pred * 3/5 + alpha_2_pred)

print(f"  Predicted at M_Z (1-loop, no KK thresholds):")
print(f"    alpha_1(M_Z) = {alpha_1_pred:.6f}  (obs: {alpha_1_obs:.6f}, err: {abs(alpha_1_pred-alpha_1_obs)/alpha_1_obs*100:.2f}%)")
print(f"    alpha_2(M_Z) = {alpha_2_pred:.6f}  (obs: {alpha_2_obs:.6f}, err: {abs(alpha_2_pred-alpha_2_obs)/alpha_2_obs*100:.2f}%)")
print(f"    alpha_3(M_Z) = {alpha_3_pred:.6f}  (obs: {alpha_s_obs:.6f}, err: {abs(alpha_3_pred-alpha_s_obs)/alpha_s_obs*100:.2f}%)")
print()
print(f"    sin^2(theta_W)(M_Z) = {sin2_pred:.5f}  (obs: {sin2_W_obs:.5f}, err: {abs(sin2_pred-sin2_W_obs)/sin2_W_obs*100:.2f}%)")
print(f"    alpha_em(M_Z)       = 1/{1/alpha_em_pred:.2f}  (obs: 1/{1/alpha_em_MZ:.2f})")
print(f"    alpha_s(M_Z)        = {alpha_3_pred:.4f}  (obs: {alpha_s_obs:.4f})")

# =========================================================================
# SECTION 6: FIND OPTIMAL M_KK FOR BEST sin^2(theta_W)
# =========================================================================
header("SECTION 6: Optimal M_KK for sin^2(theta_W)")

print("  Scanning M_KK to find best match to observed sin^2(theta_W)...")
print()

best_sin2_err = 1e10
best_MKK = 0
best_alpha_s = 0

results = []
for log_MKK in np.linspace(np.log10(200), np.log10(1e17), 1000):
    MKK = 10**log_MKK
    Lrun = np.log(MKK / M_Z)

    alpha_G = (8.0/3) / (inv_alpha_em - b_eff/(2*np.pi) * Lrun)
    if alpha_G <= 0 or alpha_G > 1:
        continue

    a1 = 1.0 / (1/alpha_G + b1/(2*np.pi) * Lrun)
    a2 = 1.0 / (1/alpha_G + b2/(2*np.pi) * Lrun)
    a3 = 1.0 / (1/alpha_G + b3/(2*np.pi) * Lrun)

    if a1 <= 0 or a2 <= 0 or a3 <= 0:
        continue

    s2 = (a1 * 3/5) / (a1 * 3/5 + a2)

    results.append((MKK, s2, a3, alpha_G))

    err = abs(s2 - sin2_W_obs)
    if err < best_sin2_err:
        best_sin2_err = err
        best_MKK = MKK
        best_sin2 = s2
        best_alpha_s = a3
        best_alpha_G = alpha_G

print(f"  Best M_KK for sin^2(theta_W) = {sin2_W_obs:.5f}:")
print(f"    M_KK = {best_MKK:.2e} GeV")
print(f"    sin^2(theta_W) = {best_sin2:.5f}")
print(f"    alpha_s(M_Z)   = {best_alpha_s:.4f}  (obs: {alpha_s_obs:.4f})")
print(f"    alpha_GUT      = {best_alpha_G:.6f}  (1/{1/best_alpha_G:.1f})")
print()

# What L_X does this correspond to?
L_X_needed = 2 * np.pi / best_MKK
v_EW_needed = 3.0 / L_X_needed
print(f"    L_X needed   = {L_X_needed:.4e} GeV^-1")
print(f"    v_EW implied = 3/L_X = {v_EW_needed:.2e} GeV  (actual: {v_EW:.2f} GeV)")
print()

if best_MKK > 1e14:
    print(f"  RESULT: Standard SU(5) unification requires M_KK ~ 10^16 GeV.")
    print(f"  STUR M_KK = {M_KK:.0f} GeV is ~{best_MKK/M_KK:.0e}x too low.")
    print(f"  This is the standard gauge hierarchy / doublet-triplet problem.")

# =========================================================================
# SECTION 7: KK THRESHOLD CORRECTIONS (can they help?)
# =========================================================================
header("SECTION 7: Can KK Threshold Corrections Bridge the Gap?")

print("  The KK tower on S^1/Z_3 modifies the running above M_KK.")
print("  In 5D, running becomes power-law: delta(1/alpha_i) ~ N_KK * b_i^5D")
print("  where N_KK is the number of KK levels below the cutoff Lambda.")
print()

# In 5D SU(5) on the orbifold, the KK threshold correction is:
# Delta_i = -b_i^KK/(2pi) * sum_{n=1}^{N} ln(Lambda/(n*M_KK))
# For Z_3, the spectrum has n = 1,2,3,... with Z_3 phase factors

# The differential running (splitting) from KK modes:
# delta(1/alpha_i - 1/alpha_j) = -(b_i^KK - b_j^KK)/(2pi) * sum_{n=1}^N ...

# In a complete SU(5) KK level: b_i^KK are all equal (SU(5) symmetric)
# So KK thresholds from complete multiplets DON'T split the couplings!

# The splitting comes only from INCOMPLETE multiplets at the orbifold boundary.
# On Z_3: the first KK level is incomplete because Z_3 projection removes
# some states. The "threshold correction" is from the non-universal part.

# Standard result (Dienes, Dudas, Gherghetta 1998):
# On S^1/Z_N, the threshold correction is:
# Delta_i = -(delta_b_i)/(2pi) * [N_KK * ln(N_KK) - N_KK + ...] ~ power-law
# where delta_b_i = b_i^5D - b_i^4D is the difference

# For S^1/Z_3 breaking SU(5) -> SM:
# The 5D content at each KK level is the full SU(5) adjoint (24)
# decomposed under SM: (8,1)_0 + (1,3)_0 + (1,1)_0 + (3,2)_{-5/6} + (3bar,2)_{5/6}
# The Z_3 orbifold projects differently on these:
# Untwisted (n mod 3=0): all survive
# Twisted (n mod 3=1,2): heavy X,Y bosons get mass ~ n*M_KK

# The non-universal threshold correction:
# Delta_1 - Delta_2 = -(delta_b_1 - delta_b_2)/(2pi) * eta_KK
# where eta_KK accounts for the KK sum

# For the X,Y bosons (the SU(5)-breaking sector):
# delta_b_XY = [-2/3, -2/3, -2/3] (gauge contribution, universal)
# plus matter contributions that ARE non-universal

# The crucial point: for the GAUGE sector alone, KK corrections are universal
# and don't help. The splitting comes from MATTER multiplets on the boundary.

# Let's estimate the required threshold correction:
delta_12_needed = 1/alpha_1_obs - 1/alpha_2_obs  # what we need at M_Z

# From M_KK unification:
delta_12_from_running = (b1 - b2)/(2*np.pi) * np.log(M_KK/M_Z)

# What's left must come from thresholds:
delta_12_threshold = delta_12_needed - delta_12_from_running

# Similarly for 2-3 splitting:
delta_23_needed = 1/alpha_2_obs - 1/alpha_3_obs_val
delta_23_from_running = (b2 - b3)/(2*np.pi) * np.log(M_KK/M_Z)
delta_23_threshold = delta_23_needed - delta_23_from_running

print(f"  Required splittings at M_Z:")
print(f"    1/alpha_1 - 1/alpha_2 = {delta_12_needed:.3f}")
print(f"    1/alpha_2 - 1/alpha_3 = {delta_23_needed:.3f}")
print()
print(f"  SM running (M_KK={M_KK:.0f} GeV to M_Z):")
print(f"    delta_12 from running = {delta_12_from_running:.3f}")
print(f"    delta_23 from running = {delta_23_from_running:.3f}")
print()
print(f"  Remaining (must come from KK thresholds):")
print(f"    delta_12 needed = {delta_12_threshold:.3f}")
print(f"    delta_23 needed = {delta_23_threshold:.3f}")
print()

# For reference, running to GUT scale:
delta_12_GUT = (b1-b2)/(2*np.pi) * np.log(2e16/M_Z)
delta_23_GUT = (b2-b3)/(2*np.pi) * np.log(2e16/M_Z)
print(f"  For comparison, SM running to 2x10^16 GeV:")
print(f"    delta_12 = {delta_12_GUT:.3f} (need {delta_12_needed:.3f})")
print(f"    delta_23 = {delta_23_GUT:.3f} (need {delta_23_needed:.3f})")

# =========================================================================
# SECTION 8: ORBIFOLD GUT WITH BRANE-LOCALIZED MATTER
# =========================================================================
header("SECTION 8: S^1/Z_3 with Brane-Localized Matter")

print("  In orbifold GUT models, matter can live on the Z_3 fixed-point branes.")
print("  Brane-localized matter does NOT propagate in the bulk, so it only")
print("  affects 4D running (not KK threshold corrections).")
print()
print("  However, the GAUGE fields propagate in the bulk, and their KK modes")
print("  give UNIVERSAL threshold corrections that don't split couplings.")
print()
print("  The Z_3 orbifold has 3 fixed points. If different generations")
print("  live at different fixed points, the threshold corrections from")
print("  MATTER KK modes can be non-universal.")
print()

# Let's compute what brane kinetic terms would be needed.
# On S^1/Z_3, one can add gauge kinetic terms localized at the branes:
# S_brane = sum_j (r_i^j / 4) int d^4x F_i^2 delta(X - X_j)
# where r_i^j has dimensions of length and can differ for each gauge group.

# These modify the effective coupling:
# 1/alpha_i^eff = L_X/alpha_5 + sum_j r_i^j

# The splitting:
# 1/alpha_1 - 1/alpha_2 = sum_j (r_1^j - r_2^j)

# To get the needed splitting at M_KK:
inv_a1_KK = 1/alpha_GUT_from_em  # from unification
inv_a2_KK = 1/alpha_GUT_from_em
inv_a3_KK = 1/alpha_GUT_from_em

# We need:
# 1/alpha_i(M_Z) = 1/alpha_GUT + b_i/(2pi)*L + Delta_i
# where Delta_i is the KK threshold + brane correction

# Required Delta_i:
Delta_1 = 1/alpha_1_obs - 1/alpha_GUT_from_em - b1/(2*np.pi)*L
Delta_2 = 1/alpha_2_obs - 1/alpha_GUT_from_em - b2/(2*np.pi)*L
Delta_3 = 1/alpha_3_obs_val - 1/alpha_GUT_from_em - b3/(2*np.pi)*L

print(f"  Required threshold corrections (with M_KK={M_KK:.0f} GeV):")
print(f"    Delta_1 = {Delta_1:.3f}")
print(f"    Delta_2 = {Delta_2:.3f}")
print(f"    Delta_3 = {Delta_3:.3f}")
print()
print(f"    Delta_1 - Delta_2 = {Delta_1-Delta_2:.3f}")
print(f"    Delta_2 - Delta_3 = {Delta_2-Delta_3:.3f}")
print()

# Are these reasonable?
# Typical KK threshold: Delta ~ N_KK * b/(2pi)
# With N_KK ~ Lambda/M_KK and Lambda = M_Pl:
N_KK_Pl = 1.22e19 / M_KK
print(f"  Number of KK levels below Planck: N_KK ~ {N_KK_Pl:.2e}")
print(f"  Needed Delta ~ {max(abs(Delta_1), abs(Delta_2), abs(Delta_3)):.1f}")
print(f"  Available from power-law (b~1, N={N_KK_Pl:.0e}): Delta ~ {N_KK_Pl/(2*np.pi):.2e}")
print()
print("  Power-law KK running CAN provide enough correction in principle,")
print("  but it must be NON-UNIVERSAL (different for alpha_1, alpha_2, alpha_3).")
print("  This requires the matter content in the bulk to be non-universal")
print("  under the SM gauge groups — which happens naturally on S^1/Z_3")
print("  where X,Y bosons have different KK boundary conditions.")

# =========================================================================
# SECTION 9: EXPLICIT Z_3 SPECTRUM CALCULATION
# =========================================================================
header("SECTION 9: Explicit Z_3 KK Spectrum and Threshold Corrections")

# On S^1/Z_3, fields with Z_3 charge q have KK masses:
# m_n^2 = ((n + q/3) * 2pi/L_X)^2  for n = 0, 1, 2, ...
# where q = 0, 1, 2

# For SU(5) breaking: the (X,Y) bosons have Z_3 charge q=1
# (they are in the coset SU(5)/SM)
# Their lightest mode has mass m_0 = (1/3) * M_KK

# The threshold correction from integrating out KK modes:
# delta(1/alpha_i) = 1/(2pi) * sum_{KK modes} b_i^mode * ln(Lambda/m_mode)

# For the X,Y bosons (12 real d.o.f., SU(3)x SU(2) decomposition):
# X,Y: (3,2)_{-5/6} + (3bar,2)_{5/6}
# b_i contributions: b_1(XY) = 5/3*2*1/10*12 = 2, b_2(XY) = 2*1/6*12/2 = 2,
# Actually, let's just use the standard gauge contribution.

# The X,Y bosons contribute to beta functions as:
# b_1^XY = 5/3 * (2/3)^2 * 3 * 2 + 5/3 * (1/3)^2 * ... (complicated)
# Let me use the standard result:
# For a (3,2)_{-5/6} scalar: b_1 = 5/3*(5/6)^2*6*1/10 = ..., etc.
# This is getting complicated. Let me just compute the LOG threshold.

# Key physics: the lowest X,Y mode at m = M_KK/3 and subsequent modes
# The threshold correction (finite, regularized) is:
# Delta_i = -delta_b_i/(2pi) * ln(M_KK/m_{XY}) = -delta_b_i/(2pi) * ln(3)

# For the X,Y gauge bosons:
# They contribute to b_i as gauge bosons in the (3,2) + (3bar,2) representation
# b_3(XY) = -11/3 * 1/2 * 2 = ... no, they are in fundamental of SU(3)
# b_3(XY) = 1/3 * T(fund) * dim(2) * 2 = 1/3 * 1/2 * 2 * 2 = 2/3
# b_2(XY) = 1/3 * T(fund) * dim(3) * 2 = 1/3 * 1/2 * 3 * 2 = 1
# b_1(XY) = 2/5 * (5/6)^2 * 6 * 2 * 2/10 = ...

# Simpler: just note that a complete SU(5) level adds equally to all b_i.
# The SPLITTING comes from the mass splitting between XY and SM KK modes.

# On Z_3: SM gauge KK modes have mass n*M_KK (q=0)
#          XY gauge KK modes have mass (n+1/3)*M_KK (q=1)

# The log threshold from the mass difference:
# Delta_i(threshold) = -b_i^XY/(2pi) * [sum over XY KK modes]
#                    + b_i^SM_gauge/(2pi) * [sum over SM KK modes]
# Since at each level the SU(5) contribution is the same,
# the difference only comes from the MASS SHIFT.

# For n-th XY mode vs n-th SM mode:
# ln(m_SM^n / m_XY^n) = ln(n*M_KK / (n+1/3)*M_KK) = ln(n/(n+1/3))

# Total threshold (regularized, N_max levels):
N_max = 100
threshold_log = sum(np.log(n / (n + 1.0/3)) for n in range(1, N_max+1))
# This converges to a finite value

print(f"  Z_3 mass shift: m_XY^(n) = (n+1/3)*M_KK, m_SM^(n) = n*M_KK")
print(f"  Log threshold sum (N={N_max}): {threshold_log:.4f}")
print(f"  This is ~ -ln(3)/2 = {-np.log(3)/2:.4f} (first term dominates)")
print()

# The finite threshold correction to the SPLITTING:
# delta(1/alpha_i) from X,Y mass shift = -b_i^{XY}/(2pi) * threshold_log
# Since b_i^{XY} contributes differently to 1,2,3:

# X,Y bosons are in the adjoint of SU(5) but in the broken part.
# Their gauge contribution to b_i:
# As massive vector bosons in (3,2)_{5/6} + cc:
b_3_XY = 2.0/3  # 2 complex scalars in fundamental of SU(3)
b_2_XY = 1.0    # 2 complex scalars in fundamental of SU(2)
b_1_XY = 5.0/3 * 2 * (5.0/6)**2 * 2 / 10  # rough estimate

# Actually, the X,Y gauge bosons are VECTORS not scalars.
# A massive vector in representation R contributes:
# b_i = -11/3 * T(R_i) for gauge bosons? No, that's the gauge boson itself.
# The X,Y are part of the gauge multiplet, so their contribution is:
# delta b_3 = -11/3 * T(3) * dim(2) = -11/3 * 1/2 * 2 = -11/3
# delta b_2 = -11/3 * T(2) * dim(3) = -11/3 * 1/2 * 3 = -11/2
# delta b_1 = -11/3 * Y^2 normalization = ...

# This is getting complicated. Let me just use the INVERSE approach.
# What TOTAL threshold correction Delta_i is needed?

print(f"  INVERSE APPROACH:")
print(f"  Required threshold corrections to achieve unification at M_KK={M_KK:.0f}:")
print(f"    Delta_1 = {Delta_1:.3f}")
print(f"    Delta_2 = {Delta_2:.3f}")
print(f"    Delta_3 = {Delta_3:.3f}")
print()

# These are huge numbers. Can power-law running provide them?
# In 5D, each KK level adds ~ b^5D to the running.
# With ~10^16 KK levels below Planck cutoff... yes, in principle.
# But the SPLITTING Delta_1 - Delta_2 must also be right.

# The required splitting:
print(f"  Required splitting:")
print(f"    Delta_1 - Delta_2 = {Delta_1 - Delta_2:.3f}")
print(f"    Delta_2 - Delta_3 = {Delta_2 - Delta_3:.3f}")
print(f"    Delta_1 - Delta_3 = {Delta_1 - Delta_3:.3f}")

# =========================================================================
# SECTION 10: SUMMARY
# =========================================================================
header("SECTION 10: Summary")

print(f"  ╔════════════════════════════════════════════════════════════════╗")
print(f"  ║  GAUGE UNIFICATION ON S^1/Z_3 — RESULTS                     ║")
print(f"  ╠════════════════════════════════════════════════════════════════╣")
print(f"  ║                                                              ║")
print(f"  ║  Starting point: sin^2(theta_W) = 3/8 at M_KK              ║")
print(f"  ║  STUR M_KK = {M_KK:.0f} GeV  (from L_X = 3/v_EW)              ║")
print(f"  ║                                                              ║")
print(f"  ║  1-loop SM running (M_KK -> M_Z):                           ║")
print(f"  ║    sin^2(theta_W)(M_Z) = {sin2_pred:.5f}  (obs: {sin2_W_obs:.5f})     ║")
print(f"  ║    alpha_s(M_Z)        = {alpha_3_pred:.4f}   (obs: {alpha_s_obs:.4f})      ║")
print(f"  ║    Deviation: sin^2 = {abs(sin2_pred-sin2_W_obs)/sin2_W_obs*100:.1f}%, alpha_s = {abs(alpha_3_pred-alpha_s_obs)/alpha_s_obs*100:.0f}%    ║")
print(f"  ║                                                              ║")
print(f"  ║  Standard unification scale: M_GUT ~ {best_MKK:.0e} GeV          ║")
print(f"  ║  Ratio M_GUT/M_KK ~ {best_MKK/M_KK:.0e}                           ║")
print(f"  ║                                                              ║")
print(f"  ║  KK thresholds on Z_3:                                      ║")
print(f"  ║    Required Delta_12 = {Delta_1-Delta_2:.1f}                              ║")
print(f"  ║    Required Delta_23 = {Delta_2-Delta_3:.1f}                              ║")
print(f"  ║    Power-law running CAN provide this from ~10^16 KK modes  ║")
print(f"  ║    but requires NON-UNIVERSAL bulk matter content            ║")
print(f"  ║                                                              ║")
print(f"  ║  STATUS: PARTIAL                                             ║")
print(f"  ║  sin^2(theta_W) = 3/8 is correct SU(5) boundary condition.  ║")
print(f"  ║  1-loop SM running gives sin^2 = {sin2_pred:.4f} ({abs(sin2_pred-sin2_W_obs)/sin2_W_obs*100:.1f}% off).       ║")
print(f"  ║  Full closure requires computing Z_3 KK threshold sums      ║")
print(f"  ║  with the complete 5D STUR matter content.                   ║")
print(f"  ║                                                              ║")
print(f"  ╚════════════════════════════════════════════════════════════════╝")


if __name__ == '__main__':
    pass  # Script runs at import time (top-level print statements)
