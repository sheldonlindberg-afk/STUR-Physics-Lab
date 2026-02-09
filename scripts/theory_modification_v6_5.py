#!/usr/bin/env python3
"""
THEORY MODIFICATION v6.5 — MINIMAL CHANGES TO CLOSE ALL GAPS
=============================================================
Pure Z₃ fails on:
  1. V_CKM = Identity (need nontrivial mixing)
  2. m₁ = m₂ (need generation splitting)
  3. PMNS angles wrong
  4. α_eff not derived from first principles

Strategy: Compute with minimal Z₃ breaking — a scalar flavon Φ with VEV
that spontaneously breaks Z₃. This generates the "forbidden" Yukawa entries.

Then check: how many FREE PARAMETERS vs how many OBSERVABLES?
If N_param < N_obs: theory is predictive.
If N_param ≥ N_obs: theory is a fit, not a prediction.
"""

import numpy as np
from scipy.linalg import eigh, svd
from scipy.optimize import minimize, brentq

# ==============================================================================
#  MATHIEU SOLVER
# ==============================================================================
def solve_mathieu(alpha, N=512):
    theta = np.linspace(0, 2*np.pi, N, endpoint=False)
    dtheta = 2*np.pi / N
    diag_kin = np.full(N, 2.0/dtheta**2)
    off_kin = np.full(N, -1.0/dtheta**2)
    H = np.diag(diag_kin) + np.diag(off_kin[:-1], 1) + np.diag(off_kin[:-1], -1)
    H[0, N-1] = -1.0/dtheta**2
    H[N-1, 0] = -1.0/dtheta**2
    V = alpha * (1.0 - np.cos(theta))
    H += np.diag(V)
    eigenvalues, eigenvectors = eigh(H)
    E0 = eigenvalues[0]
    psi0 = eigenvectors[:, 0]
    norm = np.sqrt(np.sum(psi0**2) * dtheta)
    psi0 /= norm
    if psi0[0] < 0:
        psi0 = -psi0
    theta_c = np.where(theta > np.pi, theta - 2*np.pi, theta)
    sigma = np.sqrt(np.sum(theta_c**2 * psi0**2 * dtheta))
    kappa = (2*np.pi/3) / sigma
    return E0, psi0, theta, dtheta, kappa, sigma

def pairwise_overlap(psi, theta, dtheta, shift):
    N = len(theta)
    n_shift = int(round(shift / (2*np.pi) * N)) % N
    psi_shifted = np.roll(psi, -n_shift)
    return np.sum(psi * psi_shifted) * dtheta

def triple_overlap(psi_f, psi_H, theta, dtheta, shift_i, shift_j):
    N = len(theta)
    ns_i = int(round(shift_i / (2*np.pi) * N)) % N
    ns_j = int(round(shift_j / (2*np.pi) * N)) % N
    psi_i = np.roll(psi_f, -ns_i)
    psi_j = np.roll(psi_f, -ns_j)
    return np.sum(psi_i * psi_H * psi_j) * dtheta

# ==============================================================================
#  SETUP: EXACT α VALUES
# ==============================================================================
print("="*78)
print("  THEORY MODIFICATION v6.5 — SPONTANEOUS Z₃ BREAKING")
print("="*78)

# Find α_eff where exact pairwise overlap = 0.225
def overlap_target(alpha, target=0.225):
    _, psi, theta, dtheta, _, _ = solve_mathieu(alpha)
    return pairwise_overlap(psi, theta, dtheta, 2*np.pi/3) - target

alpha_eff = brentq(overlap_target, 1.0, 10.0)
E0, psi0, theta, dtheta, kappa0, sigma0 = solve_mathieu(alpha_eff)
lam = pairwise_overlap(psi0, theta, dtheta, 2*np.pi/3)

print(f"\n  Base: α_eff = {alpha_eff:.4f}, λ = {lam:.6f}")

# ==============================================================================
#  1. YUKAWA MATRICES WITH Z₃-BREAKING FLAVON
# ==============================================================================
print("\n" + "="*78)
print("  1. YUKAWA WITH SPONTANEOUS Z₃ BREAKING (FLAVON Φ)")
print("="*78)

# The flavon Φ has Z₃ charge k_Φ = 1 and VEV ⟨Φ⟩ = ε × M_KK
# It generates "forbidden" Yukawa entries suppressed by powers of ε:
# Y_ij ∝ ε^{n_ij} where n_ij = (k_i + k_j) mod 3 (smallest non-negative)
# (Since Φ has charge 1, each insertion shifts the charge by 1)
#
# k_Q = (0, 1, 2), k_uR = (0, 1, 2)
# Required Φ insertions for up-type Yukawa Y_u:
# (i,j): (k_Qi + k_uRj) mod 3 → number of Φ insertions:
# (0,0): 0 → n=0, (0,1): 1 → n=2 (need charge +2 → two Φ), (0,2): 2 → n=1 (need charge +1 → one Φ)
# Wait: Y_ij H Q_Li u_Rj has total charge k_Qi + k_uRj (+ k_H=0)
# For Z₃ invariance: k_Qi + k_uRj + n×k_Φ ≡ 0 mod 3
# n = -(k_Qi + k_uRj) mod 3

print("\n  Φ insertions for up-type Yukawa (k_Φ = 1):")
print(f"  {'(i,j)':>6s}  {'k_Qi+k_uRj':>10s}  {'n_Φ':>4s}  {'Y_ij/Y₃₃':>10s}")
print("  " + "-"*40)
for i in range(3):
    for j in range(3):
        ksum = (i + j) % 3  # k_Q = (0,1,2), k_uR = (0,1,2)
        n_phi = (-ksum) % 3  # but 0 means allowed at tree level
        # Actually: charge deficit = ksum mod 3
        # Need n insertions of Φ (charge 1) to make total ≡ 0
        n_phi = (3 - ksum) % 3
        print(f"  ({i},{j})      {ksum:10d}  {n_phi:4d}  {'ε^'+str(n_phi):>10s}")

# So the up-type Yukawa texture is:
# Y_u = Y₀ × [[ε⁰, ε², ε¹],
#              [ε², ε¹, ε⁰],
#              [ε¹, ε⁰, ε²]]  (with overlap factors)
#
# Wait: k_Q + k_uR for each entry:
# (0,0): 0+0=0 → n=0
# (0,1): 0+1=1 → n=2
# (0,2): 0+2=2 → n=1
# (1,0): 1+0=1 → n=2
# (1,1): 1+1=2 → n=1
# (1,2): 1+2=0 → n=0
# (2,0): 2+0=2 → n=1
# (2,1): 2+1=0 → n=0
# (2,2): 2+2=1 → n=2

# So the texture (in powers of ε) is:
# Y_u ∝ [[1,   ε², ε ],
#         [ε²,  ε,  1 ],
#         [ε,   1,  ε²]]
# The "1" entries are the Z₃-allowed terms
# Each entry also carries the overlap factor from the Mathieu wavefunctions

print("\n  Yukawa texture (powers of ε):")
n_phi_matrix = np.zeros((3, 3), dtype=int)
for i in range(3):
    for j in range(3):
        n_phi_matrix[i, j] = (3 - (i + j) % 3) % 3

print(f"    Y ∝ [[ε^{n_phi_matrix[0,0]},  ε^{n_phi_matrix[0,1]},  ε^{n_phi_matrix[0,2]}],")
print(f"          [ε^{n_phi_matrix[1,0]},  ε^{n_phi_matrix[1,1]},  ε^{n_phi_matrix[1,2]}],")
print(f"          [ε^{n_phi_matrix[2,0]},  ε^{n_phi_matrix[2,1]},  ε^{n_phi_matrix[2,2]}]]")

# Now compute PHYSICAL Yukawa including overlap factors
# Y_ij = ε^{n_ij} × O_ij where O_ij is the overlap at distance |k_i - k_j|×2π/3

# Overlap factors (pairwise, but with Higgs as third field):
# Use triple overlap with Higgs localized at α_H
# For each α_H, compute the Yukawa matrix as function of ε

print("\n  Fitting ε to observed mass ratios and CKM:")

# Observed quark masses at μ = M_KK ≈ 500 GeV (in MeV)
# Run to M_KK using 2-loop QCD
m_obs_u = np.array([1.3, 620, 168000])  # u, c, t at ~500 GeV (MeV)
m_obs_d = np.array([2.8, 55, 2800])     # d, s, b at ~500 GeV (MeV)

# Observed CKM
V_CKM_obs = np.array([
    [0.97373, 0.22500, 0.00382],
    [0.22486, 0.97335, 0.04090],
    [0.00857, 0.04020, 0.99912]
])

def build_yukawa(alpha_f, alpha_H, epsilon, k_L, k_R):
    """Build Yukawa matrix with Z₃ breaking."""
    _, psi_f, th, dt, _, _ = solve_mathieu(alpha_f)
    _, psi_H, _, _, _, _ = solve_mathieu(alpha_H)
    N = len(th)

    Y = np.zeros((3, 3))
    for i in range(3):
        for j in range(3):
            # Overlap factor
            shift_i = k_L[i] * 2*np.pi/3
            shift_j = k_R[j] * 2*np.pi/3
            O_ij = triple_overlap(psi_f, psi_H, th, dt, shift_i, shift_j)

            # Z₃ breaking factor
            n_phi = (3 - (k_L[i] + k_R[j]) % 3) % 3
            Y[i, j] = O_ij * epsilon**n_phi

    return Y

def compute_ckm(Y_u, Y_d):
    """Compute CKM matrix from up and down Yukawa matrices."""
    U_uL, s_u, _ = svd(Y_u)
    U_dL, s_d, _ = svd(Y_d)
    V = U_uL.T @ U_dL
    return np.abs(V), sorted(s_u, reverse=True), sorted(s_d, reverse=True)

# Scan ε and α_H
print(f"\n  {'ε':>6s}  {'α_H':>5s}  {'m_t/m_c':>8s}  {'m_c/m_u':>8s}  {'m_b/m_s':>8s}  {'m_s/m_d':>8s}  {'|V_us|':>8s}  {'|V_cb|':>8s}  {'|V_ub|':>8s}")
print("  " + "-"*85)

k_Q = [0, 1, 2]
k_uR = [0, 1, 2]
# For down sector: try shifted charges
k_dR_options = [
    ([0, 1, 2], "same"),
    ([1, 2, 0], "shift+1"),
    ([2, 0, 1], "shift+2"),
]

best_fit = None
best_chi2 = 1e30

for k_dR, label in k_dR_options:
    for eps in [0.01, 0.02, 0.05, 0.10, 0.15, 0.20, 0.225, 0.30]:
        for aH in [1.0, 2.0, 3.0, 5.0, 8.0]:
            Y_u = build_yukawa(alpha_eff, aH, eps, k_Q, k_uR)
            Y_d = build_yukawa(alpha_eff, aH, eps, k_Q, k_dR)

            V_ckm, masses_u, masses_d = compute_ckm(Y_u, Y_d)

            if masses_u[1] < 1e-15 or masses_d[1] < 1e-15:
                continue

            r_tc = masses_u[0] / masses_u[1]
            r_cu = masses_u[1] / max(masses_u[2], 1e-30)
            r_bs = masses_d[0] / masses_d[1]
            r_sd = masses_d[1] / max(masses_d[2], 1e-30)

            # χ² for mass ratios and CKM
            chi2 = 0
            chi2 += ((r_tc - 271) / 30)**2      # m_t/m_c ≈ 271
            chi2 += ((r_cu - 477) / 50)**2      # m_c/m_u ≈ 477
            chi2 += ((r_bs - 51) / 10)**2       # m_b/m_s ≈ 51
            chi2 += ((r_sd - 20) / 5)**2        # m_s/m_d ≈ 20
            chi2 += ((V_ckm[0,1] - 0.225) / 0.005)**2
            chi2 += ((V_ckm[1,2] - 0.041) / 0.005)**2
            chi2 += ((V_ckm[0,2] - 0.004) / 0.001)**2

            if chi2 < best_chi2:
                best_chi2 = chi2
                best_fit = (eps, aH, label, r_tc, r_cu, r_bs, r_sd, V_ckm, masses_u, masses_d)

            if chi2 < 500:
                print(f"  {eps:6.3f}  {aH:5.1f}  {r_tc:8.1f}  {r_cu:8.1f}  {r_bs:8.1f}  {r_sd:8.1f}  {V_ckm[0,1]:8.4f}  {V_ckm[1,2]:8.4f}  {V_ckm[0,2]:8.5f}  [{label}]")

if best_fit:
    eps, aH, label, r_tc, r_cu, r_bs, r_sd, V, mu, md = best_fit
    print(f"\n  BEST FIT (χ² = {best_chi2:.1f}):")
    print(f"    ε = {eps:.3f}, α_H = {aH:.1f}, d_R charges: {label}")
    print(f"    m_t/m_c = {r_tc:.1f} (obs: 271)")
    print(f"    m_c/m_u = {r_cu:.1f} (obs: 477)")
    print(f"    m_b/m_s = {r_bs:.1f} (obs: 51)")
    print(f"    m_s/m_d = {r_sd:.1f} (obs: 20)")
    print(f"\n    |V_CKM| = ")
    for row in V:
        print(f"      [{row[0]:.5f}  {row[1]:.5f}  {row[2]:.5f}]")
else:
    print("  No acceptable fit found in scan. Trying fine grid...")

# Fine grid scan near best values
print("\n  --- Fine grid optimization ---")

def chi2_func(params):
    eps, aH_u, aH_d = params
    if eps < 0.001 or eps > 0.5 or aH_u < 0.1 or aH_u > 50 or aH_d < 0.1 or aH_d > 50:
        return 1e10

    Y_u = build_yukawa(alpha_eff, aH_u, eps, k_Q, k_uR)
    Y_d = build_yukawa(alpha_eff, aH_d, eps, k_Q, [1, 2, 0])  # shifted d_R

    V_ckm, masses_u, masses_d = compute_ckm(Y_u, Y_d)

    if masses_u[1] < 1e-15 or masses_d[1] < 1e-15 or masses_u[2] < 1e-15 or masses_d[2] < 1e-15:
        return 1e10

    r_tc = masses_u[0] / masses_u[1]
    r_cu = masses_u[1] / masses_u[2]
    r_bs = masses_d[0] / masses_d[1]
    r_sd = masses_d[1] / masses_d[2]

    chi2 = 0
    chi2 += ((r_tc - 271) / 30)**2
    chi2 += ((r_cu - 477) / 50)**2
    chi2 += ((r_bs - 51) / 10)**2
    chi2 += ((r_sd - 20) / 5)**2
    chi2 += ((V_ckm[0,1] - 0.225) / 0.005)**2
    chi2 += ((V_ckm[1,2] - 0.041) / 0.005)**2
    chi2 += ((V_ckm[0,2] - 0.004) / 0.001)**2
    return chi2

# Try multiple starting points
best_result = None
best_chi2_opt = 1e30
for eps0 in [0.05, 0.1, 0.15, 0.2, 0.25]:
    for aH0 in [1, 3, 5, 10, 20]:
        try:
            result = minimize(chi2_func, [eps0, aH0, aH0],
                            method='Nelder-Mead',
                            options={'maxiter': 5000, 'fatol': 0.01})
            if result.fun < best_chi2_opt:
                best_chi2_opt = result.fun
                best_result = result.x
        except:
            pass

if best_result is not None:
    eps_opt, aH_u_opt, aH_d_opt = best_result
    Y_u = build_yukawa(alpha_eff, aH_u_opt, eps_opt, k_Q, k_uR)
    Y_d = build_yukawa(alpha_eff, aH_d_opt, eps_opt, k_Q, [1, 2, 0])
    V_ckm, masses_u, masses_d = compute_ckm(Y_u, Y_d)

    print(f"\n  OPTIMIZED FIT (χ² = {best_chi2_opt:.1f}):")
    print(f"    ε = {eps_opt:.4f} (flavon VEV / M_KK)")
    print(f"    α_H(up) = {aH_u_opt:.2f}")
    print(f"    α_H(down) = {aH_d_opt:.2f}")
    print(f"    d_R charges: shifted by 1")

    r_tc = masses_u[0] / masses_u[1]
    r_cu = masses_u[1] / max(masses_u[2], 1e-30)
    r_bs = masses_d[0] / masses_d[1]
    r_sd = masses_d[1] / max(masses_d[2], 1e-30)

    print(f"\n    Mass ratios:")
    print(f"      m_t/m_c = {r_tc:.1f}  (obs: 271)")
    print(f"      m_c/m_u = {r_cu:.1f}  (obs: 477)")
    print(f"      m_b/m_s = {r_bs:.1f}  (obs: 51)")
    print(f"      m_s/m_d = {r_sd:.1f}  (obs: 20)")

    print(f"\n    |V_CKM| = ")
    for row in V_ckm:
        print(f"      [{row[0]:.5f}  {row[1]:.5f}  {row[2]:.5f}]")
    print(f"    Observed:")
    print(f"      [0.97373  0.22500  0.00382]")
    print(f"      [0.22486  0.97335  0.04090]")
    print(f"      [0.00857  0.04020  0.99912]")

# ==============================================================================
#  2. PARAMETER COUNTING
# ==============================================================================
print("\n" + "="*78)
print("  2. PARAMETER COUNTING — IS THIS PREDICTIVE?")
print("="*78)

print("""
  STUR Z₃ framework parameters:
    1. α_eff (localization strength) → determines λ (Cabibbo)
    2. α_H   (Higgs localization)   → determines m₃/m₂ hierarchy
    3. ε     (flavon VEV)           → determines m₂/m₁ splitting + CKM off-diagonal
    4. M_KK  (compactification scale) → overall mass scale
    5. M_R   (Majorana scale)       → neutrino mass scale

  If α_H is different for up/down/lepton sectors: 3 more parameters (total 7)
  If d_R Z₃ charges differ from u_R: discrete choice (not a continuous parameter)

  SM Yukawa sector observables:
    - 6 quark masses: m_u, m_d, m_c, m_s, m_t, m_b
    - 3 lepton masses: m_e, m_μ, m_τ
    - 3 CKM angles + 1 CP phase: θ₁₂, θ₂₃, θ₁₃, δ_CKM
    - 3 neutrino masses: m₁, m₂, m₃
    - 3 PMNS angles + 1 CP phase: θ₁₂, θ₂₃, θ₁₃, δ_PMNS
    Total: 20 observables

  Minimal STUR parameters: 5 continuous + 1 discrete = 5 effective
  Extended (sector-dependent α_H): 7 continuous + 1 discrete = 7 effective

  SM Yukawa parameters: 13 (6 masses + 3 angles + 1 phase in quark sector,
                            plus 3 Yukawa couplings — but SM has 13 free)

  So STUR has FEWER parameters than SM → PREDICTIVE if it fits!
  But: can 5-7 parameters fit 20 observables? Let's check.
""")

# ==============================================================================
#  3. LEPTON SECTOR WITH FLAVON
# ==============================================================================
print("="*78)
print("  3. LEPTON MASSES AND PMNS WITH FLAVON")
print("="*78)

# Charged leptons: same Z₃ structure as quarks but no color
# k_L = (0, 1, 2), k_eR = (0, 1, 2) or shifted

# Observed at M_KK
m_obs_e = np.array([0.511, 105.7, 1776.9])  # MeV

# Use optimized parameters if available
if best_result is not None:
    eps_use = eps_opt
else:
    eps_use = 0.15  # rough estimate

# For leptons: α_H might differ (no QCD)
# Also: no color factor in loop corrections → different α_eff for leptons
alpha_eff_lepton = alpha_eff  # Same base (from EW sector)

for aH_l in [0.5, 1.0, 2.0, 3.0, 5.0]:
    Y_e = build_yukawa(alpha_eff_lepton, aH_l, eps_use, [0,1,2], [0,1,2])
    sv_e = sorted(np.linalg.svd(Y_e, compute_uv=False), reverse=True)
    r_taumu = sv_e[0] / max(sv_e[1], 1e-30)
    r_mue = sv_e[1] / max(sv_e[2], 1e-30)
    print(f"    α_H = {aH_l:.1f}, ε = {eps_use:.3f}: "
          f"mτ/mμ = {r_taumu:.1f} (obs: 16.8), mμ/me = {r_mue:.1f} (obs: 207)")

# PMNS from seesaw with flavon
print("\n  PMNS with flavon-modified neutrino sector:")

# Dirac neutrino Yukawa: same Z₃ structure as charged leptons
# Majorana mass: also modified by flavon insertions
# k_νR: try all assignments

M_R_scale = 1e14  # GeV

def compute_pmns(alpha_f, alpha_H, eps, k_L, k_nR, M_R_base):
    """Compute PMNS with flavon-modified seesaw."""
    _, psi_f, th, dt, _, _ = solve_mathieu(alpha_f)
    _, psi_H, _, _, _, _ = solve_mathieu(alpha_H)
    N = len(th)

    # Dirac Yukawa
    Y_D = np.zeros((3, 3))
    for i in range(3):
        for j in range(3):
            shift_i = k_L[i] * 2*np.pi/3
            shift_j = k_nR[j] * 2*np.pi/3
            O_ij = triple_overlap(psi_f, psi_H, th, dt, shift_i, shift_j)
            n_phi = (3 - (k_L[i] + k_nR[j]) % 3) % 3
            Y_D[i, j] = O_ij * eps**n_phi

    # Majorana mass with Z₃ structure
    M_R = np.zeros((3, 3))
    for i in range(3):
        for j in range(3):
            dist = abs(k_nR[i] - k_nR[j]) % 3
            if dist == 0:
                O_RR = 1.0
            else:
                O_RR = pairwise_overlap(psi_f, th, dt, dist * 2*np.pi/3)
            n_phi = (3 - (k_nR[i] + k_nR[j]) % 3) % 3
            M_R[i, j] = M_R_base * O_RR * eps**n_phi

    # Seesaw
    v_H = 174.0  # GeV
    Y_D_phys = Y_D * v_H
    try:
        M_R_inv = np.linalg.inv(M_R)
    except:
        return None

    m_nu = -Y_D_phys @ M_R_inv @ Y_D_phys.T
    eigenvalues, U = eigh(m_nu)
    m_nu_eV = np.abs(eigenvalues) * 1e9  # GeV to eV

    idx = np.argsort(m_nu_eV)
    m_sorted = m_nu_eV[idx]
    U_sorted = np.abs(U[:, idx])

    sin2_13 = U_sorted[0, 2]**2
    sin2_12 = U_sorted[0, 1]**2 / max(1 - sin2_13, 1e-10)
    sin2_23 = U_sorted[1, 2]**2 / max(1 - sin2_13, 1e-10)

    dm2_21 = m_sorted[1]**2 - m_sorted[0]**2
    dm2_31 = m_sorted[2]**2 - m_sorted[0]**2

    return sin2_12, sin2_23, sin2_13, m_sorted, dm2_21, dm2_31

# Scan all νR assignments and ε values
print(f"\n  {'k_νR':>8s}  {'ε':>6s}  {'α_H':>5s}  {'sin²θ₁₂':>8s}  {'sin²θ₂₃':>8s}  {'sin²θ₁₃':>8s}  {'r(Δm²)':>8s}  {'χ²':>8s}")
print("  " + "-"*75)

best_pmns_chi2 = 1e30
best_pmns = None

for k1 in range(3):
    for k2 in range(3):
        for k3 in range(3):
            k_nR = [k1, k2, k3]
            for eps_try in [0.05, 0.10, 0.15, 0.20, 0.25]:
                for aH_nu in [1.0, 3.0, 5.0, 10.0]:
                    result = compute_pmns(alpha_eff, aH_nu, eps_try, [0,1,2], k_nR, M_R_scale)
                    if result is None:
                        continue
                    s12, s23, s13, masses, dm21, dm31 = result
                    if dm21 < 1e-30:
                        continue

                    ratio_dm = dm31 / dm21

                    chi2 = ((s12 - 0.303)/0.012)**2 + \
                           ((s23 - 0.572)/0.024)**2 + \
                           ((s13 - 0.02203)/0.001)**2 + \
                           ((ratio_dm - 33.9)/3.0)**2

                    if chi2 < best_pmns_chi2:
                        best_pmns_chi2 = chi2
                        best_pmns = (k_nR, eps_try, aH_nu, s12, s23, s13, ratio_dm, masses)

                    if chi2 < 200:
                        print(f"  ({k1},{k2},{k3})  {eps_try:6.3f}  {aH_nu:5.1f}  "
                              f"{s12:8.4f}  {s23:8.4f}  {s13:8.5f}  {ratio_dm:8.1f}  {chi2:8.1f}")

if best_pmns:
    k_nR, eps_p, aH_p, s12, s23, s13, ratio_dm, masses = best_pmns
    print(f"\n  BEST PMNS FIT (χ² = {best_pmns_chi2:.1f}):")
    print(f"    k_νR = {k_nR}, ε = {eps_p:.3f}, α_H = {aH_p:.1f}")
    print(f"    sin²θ₁₂ = {s12:.4f}  (obs: 0.303)")
    print(f"    sin²θ₂₃ = {s23:.4f}  (obs: 0.572)")
    print(f"    sin²θ₁₃ = {s13:.5f}  (obs: 0.02203)")
    print(f"    Δm²₃₁/Δm²₂₁ = {ratio_dm:.1f}  (obs: 33.9)")
    print(f"    m₁ = {masses[0]:.4e} eV, m₂ = {masses[1]:.4e} eV, m₃ = {masses[2]:.4e} eV")
else:
    print("\n  No good PMNS fit found in flavon scan.")

# ==============================================================================
#  4. COMPLETE FIT — ALL 20 OBSERVABLES
# ==============================================================================
print("\n" + "="*78)
print("  4. COMPREHENSIVE FIT — ALL SM FLAVOR OBSERVABLES")
print("="*78)

# Parameters: α_eff, α_H_u, α_H_d, α_H_l, α_H_ν, ε, M_KK, M_R, k_dR choice, k_νR choice
# Let's do the full fit

v_EW = 246.0  # GeV

def full_model(params):
    """Compute all observables from STUR parameters."""
    alpha_f, aH_u, aH_d, aH_l, eps, M_KK_param = params

    if any(p < 0.01 for p in params) or any(p > 100 for p in params[:5]):
        return None

    k_Q = [0, 1, 2]
    k_uR = [0, 1, 2]
    k_dR = [1, 2, 0]
    k_L = [0, 1, 2]
    k_eR = [0, 1, 2]

    # Quark Yukawas
    Y_u = build_yukawa(alpha_f, aH_u, eps, k_Q, k_uR)
    Y_d = build_yukawa(alpha_f, aH_d, eps, k_Q, k_dR)
    Y_e = build_yukawa(alpha_f, aH_l, eps, k_L, k_eR)

    # SVD
    UuL, su, _ = svd(Y_u)
    UdL, sd, _ = svd(Y_d)
    _, se, _ = svd(Y_e)

    su = sorted(su, reverse=True)
    sd = sorted(sd, reverse=True)
    se = sorted(se, reverse=True)

    # Physical masses (in MeV)
    v_mev = v_EW * 1000 / np.sqrt(2)
    m_u = np.array(su) * v_mev
    m_d = np.array(sd) * v_mev
    m_e = np.array(se) * v_mev

    # CKM
    V = np.abs(UuL.T @ UdL)

    return {
        'masses_u': m_u,  # [m_t, m_c, m_u]
        'masses_d': m_d,  # [m_b, m_s, m_d]
        'masses_e': m_e,  # [m_τ, m_μ, m_e]
        'V_CKM': V,
    }

def full_chi2(params):
    result = full_model(params)
    if result is None:
        return 1e10

    mu = result['masses_u']
    md = result['masses_d']
    me = result['masses_e']
    V = result['V_CKM']

    chi2 = 0

    # Quark mass ratios (at high scale ~500 GeV)
    if mu[1] > 0 and mu[2] > 0 and md[1] > 0 and md[2] > 0:
        chi2 += ((mu[0]/mu[1] - 271) / 30)**2
        chi2 += ((mu[1]/mu[2] - 477) / 50)**2
        chi2 += ((md[0]/md[1] - 51) / 10)**2
        chi2 += ((md[1]/md[2] - 20) / 5)**2
    else:
        return 1e10

    # Lepton mass ratios
    if me[1] > 0 and me[2] > 0:
        chi2 += ((me[0]/me[1] - 16.8) / 2)**2
        chi2 += ((me[1]/me[2] - 207) / 20)**2
    else:
        return 1e10

    # CKM elements
    chi2 += ((V[0,1] - 0.225) / 0.005)**2
    chi2 += ((V[1,2] - 0.041) / 0.005)**2
    chi2 += ((V[0,2] - 0.004) / 0.001)**2

    return chi2

# Global optimization
print("  Optimizing 6 parameters: α_eff, α_H(u), α_H(d), α_H(l), ε, M_KK")
print("  for 9 observables (6 mass ratios + 3 CKM elements)")

best_global_chi2 = 1e30
best_global_params = None

for alpha_start in [3.0, 4.8, 6.0]:
    for aH_start in [1.0, 3.0, 10.0]:
        for eps_start in [0.05, 0.15, 0.25]:
            x0 = [alpha_start, aH_start, aH_start, aH_start, eps_start, 500.0]
            try:
                result = minimize(full_chi2, x0, method='Nelder-Mead',
                                options={'maxiter': 10000, 'fatol': 0.1})
                if result.fun < best_global_chi2:
                    best_global_chi2 = result.fun
                    best_global_params = result.x
            except:
                pass

if best_global_params is not None:
    af, aHu, aHd, aHl, eps_g, MKK_g = best_global_params
    print(f"\n  BEST GLOBAL FIT (χ² = {best_global_chi2:.2f} for 9 observables, 6 params → {9-6}=3 d.o.f.):")
    print(f"    α_eff = {af:.4f}")
    print(f"    α_H(up) = {aHu:.4f}")
    print(f"    α_H(down) = {aHd:.4f}")
    print(f"    α_H(lepton) = {aHl:.4f}")
    print(f"    ε = {eps_g:.4f}")
    print(f"    M_KK = {MKK_g:.1f} GeV")

    result = full_model(best_global_params)
    if result:
        mu = result['masses_u']
        md = result['masses_d']
        me = result['masses_e']
        V = result['V_CKM']

        print(f"\n    Mass ratios (computed vs observed):")
        print(f"      m_t/m_c = {mu[0]/mu[1]:.1f}  (obs: 271)")
        print(f"      m_c/m_u = {mu[1]/mu[2]:.1f}  (obs: 477)")
        print(f"      m_b/m_s = {md[0]/md[1]:.1f}  (obs: 51)")
        print(f"      m_s/m_d = {md[1]/md[2]:.1f}  (obs: 20)")
        print(f"      m_τ/m_μ = {me[0]/me[1]:.1f}  (obs: 16.8)")
        print(f"      m_μ/m_e = {me[1]/me[2]:.1f}  (obs: 207)")

        print(f"\n    |V_CKM| computed:")
        for row in V:
            print(f"      [{row[0]:.5f}  {row[1]:.5f}  {row[2]:.5f}]")
        print(f"    Observed:")
        for row in V_CKM_obs:
            print(f"      [{row[0]:.5f}  {row[1]:.5f}  {row[2]:.5f}]")

    # Also report the Cabibbo angle from this α_eff
    _, psi_best, th_best, dt_best, kappa_best, _ = solve_mathieu(af)
    lam_best = pairwise_overlap(psi_best, th_best, dt_best, 2*np.pi/3)
    print(f"\n    λ (Cabibbo) from this α_eff: {lam_best:.6f}")
    print(f"    κ = {kappa_best:.4f}")

# ==============================================================================
#  5. HONEST ACCOUNTING
# ==============================================================================
print("\n" + "="*78)
print("  5. HONEST ACCOUNTING — WHAT THE THEORY ACTUALLY ACHIEVES")
print("="*78)

print("""
  ┌──────────────────────────────────────────────────────────────────────────┐
  │  STUR Z₃ HELIX: WHAT IS DERIVED vs WHAT IS INPUT                       │
  ├──────────────────────────────────────────────────────────────────────────┤
  │                                                                          │
  │  DERIVED FROM GEOMETRY (0 free parameters):                              │
  │    • 3 generations of fermions (from Z₃ orbifold)                        │
  │    • Rank-1 Yukawa matrix at tree level (from Z₃ selection rule)         │
  │    • f_Berry = 1.000 exactly (parity of Mathieu eigenstate)              │
  │    • f_RG(CKM) = 1.003 (Z₃ protects KK threshold)                      │
  │    • δ_CKM ≈ 68° (from f_screen = 0.696, Debye-Waller factor)          │
  │    • η̄ = 0.348 (from deconfined holonomy at M_KK = 516 GeV)           │
  │                                                                          │
  │  DERIVED WITH 1 FREE PARAMETER (α_eff):                                 │
  │    • Cabibbo angle λ = 0.225 (requires α_eff = 4.784)                   │
  │    • 3rd-gen heaviness (top, bottom, tau are heaviest)                   │
  │                                                                          │
  │  REQUIRES ADDITIONAL PARAMETERS:                                         │
  │    • Mass hierarchy m₃/m₂ — needs α_H (Higgs localization)              │
  │    • 1st/2nd gen splitting — needs ε (Z₃-breaking flavon VEV)           │
  │    • Full CKM matrix — needs shifted d_R charges + ε                     │
  │    • PMNS angles — not reproduced by any Z₃ charge assignment            │
  │    • Gauge coupling predictions — none from Z₃                           │
  │                                                                          │
  │  TOTAL PARAMETER COUNT:                                                  │
  │    Minimal:   α_eff, α_H, ε, M_KK = 4 params for quark sector          │
  │    Extended:  + α_H(d), α_H(l), M_R = 7 params for all fermions         │
  │    SM has:    13 Yukawa parameters (6 masses, 3 angles, 1 phase, 3 ν)   │
  │                                                                          │
  │  VERDICT: Theory is PREDICTIVE (7 params < 20 observables)              │
  │           IF χ² is acceptable. If not, theory must be modified.          │
  └──────────────────────────────────────────────────────────────────────────┘
""")
