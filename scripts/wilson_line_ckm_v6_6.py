#!/usr/bin/env python3
"""
v6.6 — WILSON LINE PHASES FOR NONTRIVIAL CKM
==============================================
KEY INSIGHT: Pure Z₃ gives circulant Yukawa matrices → V_CKM = Identity.
Wilson line phases ω^q break this → nontrivial CKM.

The Z₃ orbifold has a background gauge field A₅ (Wilson line).
This multiplies Yukawa couplings by phase factors depending on gauge charges.
Up-type and down-type quarks have DIFFERENT hypercharges → DIFFERENT phases
→ Y_u and Y_d are NO LONGER simultaneously diagonalizable → V_CKM ≠ I.

This is a COMPUTATION, not a modification of the theory.
The Wilson line is a REQUIRED background on S¹/Z₃ — it's already in the framework.
"""

import numpy as np
from scipy.linalg import eigh, svd
from scipy.optimize import brentq, minimize

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
    psi0 = eigenvectors[:, 0]
    norm = np.sqrt(np.sum(psi0**2) * dtheta)
    psi0 /= norm
    if psi0[0] < 0:
        psi0 = -psi0
    theta_c = np.where(theta > np.pi, theta - 2*np.pi, theta)
    sigma = np.sqrt(np.sum(theta_c**2 * psi0**2 * dtheta))
    kappa = (2*np.pi/3) / sigma
    return eigenvalues[0], psi0, theta, dtheta, kappa, sigma

def pairwise_overlap(psi, theta, dtheta, shift):
    N = len(theta)
    n_shift = int(round(shift / (2*np.pi) * N)) % N
    psi_shifted = np.roll(psi, -n_shift)
    return np.sum(psi * psi_shifted) * dtheta

def triple_overlap_complex(psi_f, psi_H, theta, dtheta, shift_i, shift_j, phase=0):
    """Triple overlap with complex phase from Wilson line."""
    N = len(theta)
    ns_i = int(round(shift_i / (2*np.pi) * N)) % N
    ns_j = int(round(shift_j / (2*np.pi) * N)) % N
    psi_i = np.roll(psi_f, -ns_i)
    psi_j = np.roll(psi_f, -ns_j)
    return np.sum(psi_i * psi_H * psi_j) * dtheta * np.exp(1j * phase)

# ==============================================================================
#  FIND α_eff FOR λ = 0.225
# ==============================================================================
def overlap_target(alpha):
    _, psi, theta, dtheta, _, _ = solve_mathieu(alpha)
    return pairwise_overlap(psi, theta, dtheta, 2*np.pi/3) - 0.225

alpha_eff = brentq(overlap_target, 1.0, 10.0)
_, psi0, theta, dtheta, kappa0, _ = solve_mathieu(alpha_eff)

print("="*78)
print("  v6.6 — WILSON LINE CKM COMPUTATION")
print("="*78)
print(f"\n  α_eff = {alpha_eff:.4f}, λ = 0.225000")

# ==============================================================================
#  WILSON LINE PHASES
# ==============================================================================
print("\n" + "="*78)
print("  WILSON LINE PHASES ON S¹/Z₃")
print("="*78)

# On S¹/Z₃ orbifold, the Wilson line W = exp(i A₅ L) is valued in the gauge group.
# For the SM: W ∈ U(1)_Y × SU(2)_L × SU(3)_C
# The Z₃ constraint: W³ = 1 (since going around the circle 3 times = identity)
# So W = diag(ω^{q_i}) where ω = e^{2πi/3}

# The Wilson line generates DIFFERENT phases for particles with different hypercharge Y:
# Phase(f) = ω^{Y_f} when transported around the circle

# Hypercharges (SM convention):
# Q_L: Y = +1/6    → phase: ω^{1/6}
# u_R: Y = +2/3    → phase: ω^{2/3}
# d_R: Y = -1/3    → phase: ω^{-1/3}
# L:   Y = -1/2    → phase: ω^{-1/2}
# e_R: Y = -1      → phase: ω^{-1}
# H:   Y = +1/2    → phase: ω^{1/2}

# In the Yukawa coupling H Q_L u_R: total phase = ω^{1/2 + 1/6 + 2/3} = ω^{4/3}
# For H Q_L d_R: total phase = ω^{1/2 + 1/6 - 1/3} = ω^{1/3}
# For H L e_R: total phase = ω^{1/2 - 1/2 - 1} = ω^{-1}

# But this is the TOTAL phase — what matters is the phase at EACH site.
# The Wilson line wraps around the full circle.
# A fermion at site k (θ = 2πk/3) picks up phase ω^{Y_f × k}.

# So the Yukawa coupling Y_ij gets phase:
# ϕ_ij = 2π/3 × (Y_H × 0 + Y_Qi × k_i + Y_Rj × k_j)
# (Higgs at θ = 0 for simplicity)

# For FULL Wilson line parameterization:
# W = exp(i δ_W × A₅) where A₅ = diag(Y) in hypercharge direction
# The phase acquired by fermion at site k is:
# ϕ_f(k) = δ_W × Y_f × k × 2π/3

# δ_W is the Wilson line parameter (0 to 3, since ω³ = 1)

# KEY: the CKM comes from the DIFFERENCE in phases between up and down sectors
# because Y(u_R) ≠ Y(d_R).

omega = np.exp(2j * np.pi / 3)

# Wilson line parameter scan
print("\n  Scanning Wilson line parameter δ_W:")
print(f"  {'δ_W':>6s}  {'|V_us|':>8s}  {'|V_cb|':>8s}  {'|V_ub|':>8s}  {'m_t/m_c':>8s}  {'m_b/m_s':>8s}  {'m_c/m_u':>8s}  {'m_s/m_d':>8s}")
print("  " + "-"*80)

def build_yukawa_wilson(alpha_f, alpha_H, delta_W, Y_L, Y_R, k_L, k_R):
    """Build complex Yukawa matrix with Wilson line phases."""
    _, psi_f, th, dt, _, _ = solve_mathieu(alpha_f)
    _, psi_H, _, _, _, _ = solve_mathieu(alpha_H)
    N = len(th)

    Y = np.zeros((3, 3), dtype=complex)
    for i in range(3):
        for j in range(3):
            # Overlap (magnitude)
            shift_i = k_L[i] * 2*np.pi/3
            shift_j = k_R[j] * 2*np.pi/3
            ns_i = int(round(shift_i / (2*np.pi) * N)) % N
            ns_j = int(round(shift_j / (2*np.pi) * N)) % N
            psi_i = np.roll(psi_f, -ns_i)
            psi_j = np.roll(psi_f, -ns_j)
            O_ij = np.sum(psi_i * psi_H * psi_j) * dt

            # Wilson line phase
            # Phase from transporting L_i from 0 to site k_L[i] and R_j from 0 to site k_R[j]
            phase = delta_W * (Y_L * k_L[i] + Y_R * k_R[j]) * 2*np.pi/3
            Y[i, j] = O_ij * np.exp(1j * phase)

    return Y

# SM hypercharges
Y_QL = 1/6     # Q_L
Y_uR = 2/3     # u_R
Y_dR = -1/3    # d_R
Y_LL = -1/2    # L (lepton doublet)
Y_eR = -1      # e_R

k_gen = [0, 1, 2]  # generation sites

best_wilson_chi2 = 1e30
best_wilson_params = None

for alpha_H in [1.0, 2.0, 3.0, 5.0, 8.0, 12.0]:
    for delta_W in np.linspace(0.01, 2.99, 60):
        Y_u = build_yukawa_wilson(alpha_eff, alpha_H, delta_W, Y_QL, Y_uR, k_gen, k_gen)
        Y_d = build_yukawa_wilson(alpha_eff, alpha_H, delta_W, Y_QL, Y_dR, k_gen, k_gen)

        UuL, su, _ = svd(Y_u)
        UdL, sd, _ = svd(Y_d)

        su = sorted(su, reverse=True)
        sd = sorted(sd, reverse=True)

        V = np.abs(UuL.conj().T @ UdL)

        if su[1] < 1e-15 or sd[1] < 1e-15:
            continue

        r_tc = su[0] / su[1]
        r_cu = su[1] / max(su[2], 1e-30)
        r_bs = sd[0] / sd[1]
        r_sd = sd[1] / max(sd[2], 1e-30)

        chi2 = 0
        chi2 += ((V[0,1] - 0.225) / 0.01)**2
        chi2 += ((V[1,2] - 0.041) / 0.01)**2
        chi2 += ((V[0,2] - 0.004) / 0.002)**2

        if chi2 < best_wilson_chi2:
            best_wilson_chi2 = chi2
            best_wilson_params = (delta_W, alpha_H, V, su, sd, r_tc, r_cu, r_bs, r_sd)

        if abs(V[0,1] - 0.225) < 0.1 or chi2 < 200:
            print(f"  {delta_W:6.3f}  {V[0,1]:8.4f}  {V[1,2]:8.4f}  {V[0,2]:8.5f}  "
                  f"{r_tc:8.1f}  {r_bs:8.1f}  {r_cu:8.1f}  {r_sd:8.1f}  [α_H={alpha_H:.0f}]")

if best_wilson_params:
    dW, aH, V, su, sd, r_tc, r_cu, r_bs, r_sd = best_wilson_params
    print(f"\n  BEST WILSON LINE FIT (CKM χ² = {best_wilson_chi2:.1f}):")
    print(f"    δ_W = {dW:.4f}")
    print(f"    α_H = {aH:.1f}")
    print(f"    |V_CKM|:")
    for row in V:
        print(f"      [{row[0]:.5f}  {row[1]:.5f}  {row[2]:.5f}]")
    print(f"    m_t/m_c = {r_tc:.1f}, m_c/m_u = {r_cu:.1f}")
    print(f"    m_b/m_s = {r_bs:.1f}, m_s/m_d = {r_sd:.1f}")
else:
    print("  No Wilson line solution found.")

# ==============================================================================
#  COMBINED: WILSON LINE + FLAVON
# ==============================================================================
print("\n" + "="*78)
print("  COMBINED: WILSON LINE + FLAVON (Z₃ BREAKING)")
print("="*78)

def build_yukawa_full(alpha_f, alpha_H, delta_W, eps, Y_L, Y_R, k_L, k_R):
    """Build Yukawa with Wilson line phases AND flavon Z₃ breaking."""
    _, psi_f, th, dt, _, _ = solve_mathieu(alpha_f)
    _, psi_H, _, _, _, _ = solve_mathieu(alpha_H)
    N = len(th)

    Y = np.zeros((3, 3), dtype=complex)
    for i in range(3):
        for j in range(3):
            shift_i = k_L[i] * 2*np.pi/3
            shift_j = k_R[j] * 2*np.pi/3
            ns_i = int(round(shift_i / (2*np.pi) * N)) % N
            ns_j = int(round(shift_j / (2*np.pi) * N)) % N
            psi_i = np.roll(psi_f, -ns_i)
            psi_j = np.roll(psi_f, -ns_j)
            O_ij = np.sum(psi_i * psi_H * psi_j) * dt

            # Wilson line phase
            phase = delta_W * (Y_L * k_L[i] + Y_R * k_R[j]) * 2*np.pi/3

            # Flavon suppression
            n_phi = (3 - (k_L[i] + k_R[j]) % 3) % 3

            Y[i, j] = O_ij * eps**n_phi * np.exp(1j * phase)

    return Y

print("\n  Scanning (δ_W, ε, α_H) parameter space:")
print(f"  {'δ_W':>6s}  {'ε':>6s}  {'α_H':>5s}  {'|V_us|':>8s}  {'|V_cb|':>8s}  {'|V_ub|':>8s}  {'m_t/m_c':>8s}  {'m_b/m_s':>8s}")
print("  " + "-"*70)

best_full_chi2 = 1e30
best_full_params = None

for alpha_H in [2.0, 5.0, 10.0, 20.0]:
    for delta_W in np.linspace(0.1, 2.9, 30):
        for eps in [0.05, 0.10, 0.15, 0.20, 0.25, 0.30]:
            Y_u = build_yukawa_full(alpha_eff, alpha_H, delta_W, eps, Y_QL, Y_uR, k_gen, k_gen)
            Y_d = build_yukawa_full(alpha_eff, alpha_H, delta_W, eps, Y_QL, Y_dR, k_gen, k_gen)

            UuL, su, _ = svd(Y_u)
            UdL, sd, _ = svd(Y_d)
            su_s = sorted(su, reverse=True)
            sd_s = sorted(sd, reverse=True)
            V = np.abs(UuL.conj().T @ UdL)

            if su_s[1] < 1e-15 or sd_s[1] < 1e-15:
                continue

            r_tc = su_s[0] / su_s[1]
            r_bs = sd_s[0] / sd_s[1]

            chi2 = ((V[0,1] - 0.225)/0.005)**2 + ((V[1,2] - 0.041)/0.005)**2 + \
                   ((V[0,2] - 0.004)/0.001)**2 + ((r_tc - 271)/50)**2 + ((r_bs - 51)/10)**2

            if chi2 < best_full_chi2:
                best_full_chi2 = chi2
                best_full_params = (delta_W, eps, alpha_H, V, su_s, sd_s, r_tc, r_bs)

            if V[0,1] > 0.10 and chi2 < 500:
                print(f"  {delta_W:6.3f}  {eps:6.3f}  {alpha_H:5.1f}  {V[0,1]:8.4f}  {V[1,2]:8.4f}  "
                      f"{V[0,2]:8.5f}  {r_tc:8.1f}  {r_bs:8.1f}")

if best_full_params:
    dW, eps_f, aH, V, su, sd, r_tc, r_bs = best_full_params
    print(f"\n  BEST COMBINED FIT (χ² = {best_full_chi2:.1f}):")
    print(f"    δ_W = {dW:.4f}, ε = {eps_f:.4f}, α_H = {aH:.1f}")
    print(f"    |V_CKM|:")
    for row in V:
        print(f"      [{row[0]:.5f}  {row[1]:.5f}  {row[2]:.5f}]")
    print(f"    m_t/m_c = {r_tc:.1f} (obs: 271)")
    print(f"    m_b/m_s = {r_bs:.1f} (obs: 51)")

# ==============================================================================
#  ALTERNATIVE: CKM FROM Z₃ PHASE STRUCTURE WITHOUT WILSON LINE
# ==============================================================================
print("\n" + "="*78)
print("  ALTERNATIVE: CKM FROM Z₃ ROOT-OF-UNITY PHASES")
print("="*78)

# On S¹/Z₃, the wavefunctions at different sites carry Z₃ phases:
# ψ_k(θ) = ψ_0(θ - 2πk/3) × ω^k  where ω = e^{2πi/3}
# This is because the Z₃ orbifold identification includes both:
#   θ → θ + 2π/3  AND  ψ → ω ψ (boundary condition)
#
# With these phases, the Yukawa matrix becomes:
# Y_ij = ∫ ψ_i*(θ) H(θ) ψ_j(θ) dθ × ω^{k_i - k_j}

print("\n  Z₃ boundary condition: ψ_k → ω^k ψ_k under θ → θ+2π/3")
print("  This gives complex Yukawa entries:")

def build_yukawa_z3phase(alpha_f, alpha_H, k_L, k_R, phase_exp=1):
    """Yukawa with Z₃ boundary condition phases."""
    _, psi_f, th, dt, _, _ = solve_mathieu(alpha_f)
    _, psi_H, _, _, _, _ = solve_mathieu(alpha_H)
    N = len(th)

    Y = np.zeros((3, 3), dtype=complex)
    for i in range(3):
        for j in range(3):
            shift_i = k_L[i] * 2*np.pi/3
            shift_j = k_R[j] * 2*np.pi/3
            ns_i = int(round(shift_i / (2*np.pi) * N)) % N
            ns_j = int(round(shift_j / (2*np.pi) * N)) % N
            psi_i = np.roll(psi_f, -ns_i)
            psi_j = np.roll(psi_f, -ns_j)
            O_ij = np.sum(psi_i * psi_H * psi_j) * dt

            # Z₃ phase: ω^{(k_L[i]*p_L + k_R[j]*p_R)} where p = Z₃ charge of the representation
            # For Q_L: Z₃ charge p_Q = 1 (fundamental)
            # For u_R: Z₃ charge p_u (can differ)
            # The phase depends on the Z₃ representation under which each field transforms

            # If all fields transform as ω^k under Z₃:
            phase = omega**(phase_exp * (k_L[i] - k_R[j]))
            Y[i, j] = O_ij * phase

    return Y

# The Z₃ phase e^{2πi(k_i-k_j)/3} already breaks the circulant structure
# because it's ω^{k_i - k_j}, not ω^{k_i + k_j}

for alpha_H in [1.0, 3.0, 5.0, 10.0]:
    for p_u in range(3):
        for p_d in range(3):
            Y_u = build_yukawa_z3phase(alpha_eff, alpha_H, k_gen, k_gen, phase_exp=p_u)
            Y_d = build_yukawa_z3phase(alpha_eff, alpha_H, k_gen, k_gen, phase_exp=p_d)

            UuL, su, _ = svd(Y_u)
            UdL, sd, _ = svd(Y_d)
            V = np.abs(UuL.conj().T @ UdL)
            su_s = sorted(su, reverse=True)
            sd_s = sorted(sd, reverse=True)

            if su_s[1] > 1e-15 and sd_s[1] > 1e-15:
                r_tc = su_s[0] / su_s[1]
                r_bs = sd_s[0] / sd_s[1]
            else:
                r_tc = r_bs = 0

            # Only print if V is nontrivial
            if abs(V[0,1]) > 0.01:
                print(f"  α_H={alpha_H:.0f}, p_u={p_u}, p_d={p_d}: "
                      f"|V_us|={V[0,1]:.4f}, |V_cb|={V[1,2]:.4f}, |V_ub|={V[0,2]:.5f}, "
                      f"m_t/m_c={r_tc:.1f}, m_b/m_s={r_bs:.1f}")

# ==============================================================================
#  DIFFERENT APPROACH: NON-DEGENERATE Z₃ SITES
# ==============================================================================
print("\n" + "="*78)
print("  NON-DEGENERATE SITES: θ₁ ≠ 2π/3, θ₂ ≠ 4π/3")
print("="*78)

# If the Z₃ is softly broken so sites are at θ = 0, 2π/3 + δ₁, 4π/3 + δ₂:
# All overlaps become different → CKM ≠ Identity

def build_yukawa_shifted(alpha_f, alpha_H, positions_L, positions_R):
    """Yukawa with non-degenerate site positions."""
    _, psi_f, th, dt, _, _ = solve_mathieu(alpha_f)
    _, psi_H, _, _, _, _ = solve_mathieu(alpha_H)
    N = len(th)

    Y = np.zeros((3, 3))
    for i in range(3):
        for j in range(3):
            ns_i = int(round(positions_L[i] / (2*np.pi) * N)) % N
            ns_j = int(round(positions_R[j] / (2*np.pi) * N)) % N
            psi_i = np.roll(psi_f, -ns_i)
            psi_j = np.roll(psi_f, -ns_j)
            Y[i, j] = np.sum(psi_i * psi_H * psi_j) * dt

    return Y

print("\n  Scanning site displacement δ:")
print(f"  {'δ₁':>6s}  {'δ₂':>6s}  {'|V_us|':>8s}  {'|V_cb|':>8s}  {'|V_ub|':>8s}  {'m_t/m_c':>8s}  {'m_b/m_s':>8s}")
print("  " + "-"*65)

best_shift_chi2 = 1e30
best_shift_params = None

for alpha_H_u in [5.0]:
    for alpha_H_d in [2.0]:
        for d1 in np.linspace(-0.5, 0.5, 21):
            for d2 in np.linspace(-0.5, 0.5, 21):
                pos_L = [0, 2*np.pi/3, 4*np.pi/3]
                pos_uR = [0, 2*np.pi/3 + d1, 4*np.pi/3 + d2]
                pos_dR = [0, 2*np.pi/3 - d1, 4*np.pi/3 - d2]  # opposite shift

                Y_u = build_yukawa_shifted(alpha_eff, alpha_H_u, pos_L, pos_uR)
                Y_d = build_yukawa_shifted(alpha_eff, alpha_H_d, pos_L, pos_dR)

                UuL, su, _ = svd(Y_u)
                UdL, sd, _ = svd(Y_d)
                V = np.abs(UuL.T @ UdL)
                su_s = sorted(su, reverse=True)
                sd_s = sorted(sd, reverse=True)

                if su_s[1] < 1e-15 or sd_s[1] < 1e-15:
                    continue

                r_tc = su_s[0] / su_s[1]
                r_bs = sd_s[0] / sd_s[1]

                chi2_ckm = ((V[0,1] - 0.225)/0.01)**2 + ((V[1,2] - 0.041)/0.01)**2

                if chi2_ckm < best_shift_chi2:
                    best_shift_chi2 = chi2_ckm
                    best_shift_params = (d1, d2, V, r_tc, r_bs, su_s, sd_s)

                if V[0,1] > 0.05 and V[0,1] < 0.5:
                    print(f"  {d1:6.3f}  {d2:6.3f}  {V[0,1]:8.4f}  {V[1,2]:8.4f}  {V[0,2]:8.5f}  "
                          f"{r_tc:8.1f}  {r_bs:8.1f}")

if best_shift_params:
    d1, d2, V, r_tc, r_bs, su, sd = best_shift_params
    print(f"\n  BEST SHIFTED SITES FIT (CKM χ² = {best_shift_chi2:.1f}):")
    print(f"    δ₁ = {d1:.4f}, δ₂ = {d2:.4f}")
    print(f"    |V_CKM|:")
    for row in V:
        print(f"      [{row[0]:.5f}  {row[1]:.5f}  {row[2]:.5f}]")
    print(f"    m_t/m_c = {r_tc:.1f} (obs: 271)")
    print(f"    m_b/m_s = {r_bs:.1f} (obs: 51)")

# ==============================================================================
#  FINAL: OPTIMIZED FULL MODEL WITH SHIFTED SITES
# ==============================================================================
print("\n" + "="*78)
print("  OPTIMIZED FULL MODEL")
print("="*78)

def full_model_chi2(params):
    alpha_f, alpha_H_u, alpha_H_d, alpha_H_l, d1, d2 = params
    if alpha_f < 0.5 or alpha_f > 20:
        return 1e10
    if any(a < 0.1 or a > 50 for a in [alpha_H_u, alpha_H_d, alpha_H_l]):
        return 1e10

    pos_L = [0, 2*np.pi/3, 4*np.pi/3]
    pos_uR = [0, 2*np.pi/3 + d1, 4*np.pi/3 + d2]
    pos_dR = [0, 2*np.pi/3 - d1, 4*np.pi/3 - d2]
    pos_eR = [0, 2*np.pi/3, 4*np.pi/3]  # leptons unshifted

    try:
        Y_u = build_yukawa_shifted(alpha_f, alpha_H_u, pos_L, pos_uR)
        Y_d = build_yukawa_shifted(alpha_f, alpha_H_d, pos_L, pos_dR)
        Y_e = build_yukawa_shifted(alpha_f, alpha_H_l, pos_L, pos_eR)
    except:
        return 1e10

    UuL, su, _ = svd(Y_u)
    UdL, sd, _ = svd(Y_d)
    _, se, _ = svd(Y_e)

    su = sorted(su, reverse=True)
    sd = sorted(sd, reverse=True)
    se = sorted(se, reverse=True)

    V = np.abs(UuL.T @ UdL)

    if su[1] < 1e-15 or sd[1] < 1e-15 or se[1] < 1e-15:
        return 1e10

    chi2 = 0
    chi2 += ((su[0]/su[1] - 271)/30)**2
    chi2 += ((sd[0]/sd[1] - 51)/10)**2
    chi2 += ((se[0]/se[1] - 16.8)/2)**2
    chi2 += ((V[0,1] - 0.225)/0.005)**2
    chi2 += ((V[1,2] - 0.041)/0.005)**2
    chi2 += ((V[0,2] - 0.004)/0.001)**2
    return chi2

best_opt_chi2 = 1e30
best_opt_params = None

for af in [3.0, 4.8, 6.0, 8.0]:
    for aHu in [3.0, 5.0, 10.0]:
        for aHd in [1.0, 2.0, 5.0]:
            for d1_start in [-0.3, 0.0, 0.3]:
                x0 = [af, aHu, aHd, 1.0, d1_start, -d1_start]
                try:
                    result = minimize(full_model_chi2, x0, method='Nelder-Mead',
                                    options={'maxiter': 3000, 'fatol': 0.1})
                    if result.fun < best_opt_chi2:
                        best_opt_chi2 = result.fun
                        best_opt_params = result.x
                except:
                    pass

if best_opt_params is not None:
    af, aHu, aHd, aHl, d1, d2 = best_opt_params
    print(f"\n  OPTIMIZED (χ² = {best_opt_chi2:.2f}, 6 params for 6 observables → 0 d.o.f.):")
    print(f"    α_eff = {af:.4f}")
    print(f"    α_H(up) = {aHu:.4f}")
    print(f"    α_H(down) = {aHd:.4f}")
    print(f"    α_H(lepton) = {aHl:.4f}")
    print(f"    δ₁ = {d1:.4f} (site shift)")
    print(f"    δ₂ = {d2:.4f} (site shift)")

    pos_L = [0, 2*np.pi/3, 4*np.pi/3]
    pos_uR = [0, 2*np.pi/3 + d1, 4*np.pi/3 + d2]
    pos_dR = [0, 2*np.pi/3 - d1, 4*np.pi/3 - d2]

    Y_u = build_yukawa_shifted(af, aHu, pos_L, pos_uR)
    Y_d = build_yukawa_shifted(af, aHd, pos_L, pos_dR)
    Y_e = build_yukawa_shifted(af, aHl, pos_L, [0, 2*np.pi/3, 4*np.pi/3])

    UuL, su, _ = svd(Y_u)
    UdL, sd, _ = svd(Y_d)
    _, se, _ = svd(Y_e)
    su = sorted(su, reverse=True)
    sd = sorted(sd, reverse=True)
    se = sorted(se, reverse=True)
    V = np.abs(UuL.T @ UdL)

    _, psi_opt, th_opt, dt_opt, kappa_opt, _ = solve_mathieu(af)
    lam_opt = pairwise_overlap(psi_opt, th_opt, dt_opt, 2*np.pi/3)

    print(f"\n    λ (Cabibbo from overlap) = {lam_opt:.6f}")
    print(f"    κ = {kappa_opt:.4f}")

    print(f"\n    Mass ratios:")
    print(f"      m_t/m_c = {su[0]/su[1]:.1f}  (obs: 271)")
    print(f"      m_b/m_s = {sd[0]/sd[1]:.1f}  (obs: 51)")
    print(f"      m_τ/m_μ = {se[0]/se[1]:.1f}  (obs: 16.8)")

    print(f"\n    |V_CKM|:")
    for row in V:
        print(f"      [{row[0]:.5f}  {row[1]:.5f}  {row[2]:.5f}]")
    print(f"    Observed:")
    print(f"      [0.97373  0.22500  0.00382]")
    print(f"      [0.22486  0.97335  0.04090]")
    print(f"      [0.00857  0.04020  0.99912]")

    # Check: does this predict m_c/m_u and m_s/m_d? (not fitted)
    if su[2] > 0 and sd[2] > 0:
        print(f"\n    PREDICTIONS (not fitted):")
        print(f"      m_c/m_u = {su[1]/su[2]:.1f}  (obs: 477)")
        print(f"      m_s/m_d = {sd[1]/sd[2]:.1f}  (obs: 20)")
        print(f"      m_μ/m_e = {se[1]/se[2]:.1f}  (obs: 207)")
    else:
        print(f"\n    m_u, m_d predict zero (Z₃ degeneracy not broken by site shift alone)")

# ==============================================================================
#  SUMMARY
# ==============================================================================
print("\n" + "="*78)
print("  v6.6 SUMMARY")
print("="*78)
print("""
  APPROACHES TESTED:
  1. Wilson line phases (hypercharge-dependent) → CKM entries computed
  2. Wilson line + flavon (Z₃ breaking) → CKM + mass splitting
  3. Z₃ root-of-unity phases → tested all phase combinations
  4. Non-degenerate site positions → CKM from geometric misalignment
  5. Optimized full model → best fit to masses + CKM simultaneously

  The results above determine whether the Z₃ framework can reproduce
  the SM flavor structure with a tractable number of parameters.
""")
