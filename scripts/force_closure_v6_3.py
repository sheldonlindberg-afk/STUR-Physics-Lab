#!/usr/bin/env python3
"""
STUR Force Closure v6.3
========================
COMPUTE closure for every remaining gap. No descriptions of failure.

Gap A: α_H too small (0.15 vs need 3.7-168) — compute brane-localized Higgs profile
Gap B: PMNS angles wrong — compute with DIFFERENT neutrino Z₃ charges
Gap C: α_eff 1.39 vs 1.50 — compute with resummed KK tower
Gap D: Gauge coupling mismatch — compute with Z₃ Wilson line breaking
"""
import numpy as np
from scipy.optimize import brentq
from scipy.linalg import svd

def solve_mathieu(alpha, N=512):
    L = 2*np.pi; dth = L/N
    theta = np.linspace(-np.pi + dth/2, np.pi - dth/2, N)
    V = alpha*(1 - np.cos(theta))
    H = np.diag(2.0/dth**2 + V)
    od = -1.0/dth**2 * np.ones(N-1)
    H += np.diag(od, 1) + np.diag(od, -1)
    H[0, N-1] = -1.0/dth**2; H[N-1, 0] = -1.0/dth**2
    ev, evec = np.linalg.eigh(H)
    psi = evec[:, 0]; psi /= np.sqrt(np.sum(psi**2)*dth)
    if psi[N//2] < 0: psi = -psi
    sigma = np.sqrt(np.sum(psi**2 * theta**2 * dth))
    kappa = (2*np.pi/3)/sigma
    return ev[0], psi, theta, sigma, kappa, dth

def get_psis(alpha, N=512):
    L = 2*np.pi; dth = L/N
    theta = np.linspace(-np.pi + dth/2, np.pi - dth/2, N)
    psis = []
    for off in [0, 2*np.pi/3, -2*np.pi/3]:
        V = alpha*(1 - np.cos(theta - off))
        H = np.diag(2.0/dth**2 + V)
        od = -1.0/dth**2 * np.ones(N-1)
        H += np.diag(od, 1) + np.diag(od, -1)
        H[0, N-1] = -1.0/dth**2; H[N-1, 0] = -1.0/dth**2
        ev, evec = np.linalg.eigh(H)
        p = evec[:, 0]; p /= np.sqrt(np.sum(p**2)*dth)
        idx = np.argmin(np.abs(theta - off))
        if p[idx] < 0: p = -p
        psis.append(p)
    return theta, dth, psis

M_KK = 516.0; v_EW = 246.22; alpha_f = 1.48

print("="*78)
print("  FORCE CLOSURE v6.3 — COMPUTE EVERYTHING")
print("="*78)

# =================================================================
# GAP A: α_H — BRANE-LOCALIZED HIGGS (DELTA FUNCTION LIMIT)
# =================================================================
print("\n" + "="*78)
print("  GAP A: α_H — THE HIGGS IS BRANE-LOCALIZED (DELTA FUNCTION)")
print("="*78)

# KEY INSIGHT: On S¹/Z₃, the Higgs is localized at the orbifold
# FIXED POINT θ=0 by the orbifold projection. It doesn't need a
# potential — the Z₃ identification FORCES it to be at θ=0.
# In the δ-function limit: h(θ) = δ(θ)
# Then Y_{ij} = ψ_i(0) × ψ_j(0) (brane Yukawa)

E0, psi0, theta, sigma, kappa, dth = solve_mathieu(alpha_f)
_, _, psis = get_psis(alpha_f)

# Brane Yukawa: Y_{ij} = ψ_i(0) × ψ_j(0)
# Find index closest to θ=0
idx0 = np.argmin(np.abs(theta))
brane_vals = [p[idx0] for p in psis]

Y_brane = np.zeros((3,3))
for i in range(3):
    for j in range(3):
        Y_brane[i,j] = brane_vals[i] * brane_vals[j]

sv_brane = np.linalg.svd(Y_brane, compute_uv=False)
sv_brane = sorted(sv_brane, reverse=True)

print(f"\n  Brane-localized Yukawa: Y_ij = ψ_i(0) × ψ_j(0)")
print(f"  ψ₃(0) = {brane_vals[0]:.6f}  (gen 3 at θ=0)")
print(f"  ψ₂(0) = {brane_vals[1]:.6f}  (gen 2 at θ=2π/3)")
print(f"  ψ₁(0) = {brane_vals[2]:.6f}  (gen 1 at θ=-2π/3)")
print(f"\n  Singular values: {sv_brane[0]:.6f}, {sv_brane[1]:.6e}, {sv_brane[2]:.6e}")
print(f"  Rank = 1 (as expected for outer product)")

# The δ-function Higgs gives a RANK-1 Yukawa → only m₃ ≠ 0.
# To get m₂, need Z₃ selection rule (off-diagonal coupling).
# Full brane structure with Z₃ charges:
# Y₀₀ = ψ₃(0)² (tree, allowed)
# Y₁₂ = ψ₂(0)·ψ₁(0) (tree, Z₃ allowed)
# Y₁₁ = 0 (Z₃ forbidden)
# Mass eigenvalues: m₃ = |Y₀₀|, m₂ = |Y₁₂|, m₁ = 0

Y00 = brane_vals[0]**2
Y12 = brane_vals[1] * brane_vals[2]

ratio_32 = Y00 / Y12
print(f"\n  Z₃ selection rule structure:")
print(f"    Y₀₀ = ψ₃(0)² = {Y00:.6f}")
print(f"    Y₁₂ = ψ₂(0)·ψ₁(0) = {Y12:.6f}")
print(f"    m₃/m₂ = Y₀₀/Y₁₂ = {ratio_32:.1f}")
print(f"    This equals ψ₃(0)²/[ψ₂(0)·ψ₁(0)] = exp(κ²/2) = {np.exp(kappa**2/2):.1f}")

# Now: different sectors have different α_eff due to RG running
# α_eff(μ) = α_base × (1 + c₃·α_s(μ)/π + c₂·α₂(μ)/π + c₁·α₁(μ)/π)
alpha_base = 1.48

# QCD coupling at various scales
def alpha_s_running(mu):
    """One-loop QCD running."""
    b0 = 7.0  # (11 - 2/3 × 6)
    if mu <= 0.5: return 1.0  # Non-perturbative cap
    return 0.1180 / (1 + 0.1180 * b0/(2*np.pi) * np.log(mu/91.2))

# Effective α for each quark at its mass scale
# c₃ = 4C_F/3 for the dominant QCD vertex correction
c3 = 4*4/3/3  # = 16/9

print(f"\n  {'Fermion':>10s}  {'μ (GeV)':>10s}  {'α_s(μ)':>8s}  {'α_eff(μ)':>10s}  {'κ(μ)':>8s}  {'m₃/m₂':>8s}  {'Obs ratio':>10s}")
print(f"  " + "─"*75)

fermion_data = [
    ('top',     172.57, 172.57/1.273),
    ('bottom',  4.183,  4.183/0.0935),
    ('tau',     1.777,  1.777/0.1057),
]

for name, mu, obs_ratio in fermion_data:
    a_s = alpha_s_running(mu)
    if name == 'tau':
        a_eff = alpha_base  # No QCD for leptons
    else:
        a_eff = alpha_base * (1 + c3 * a_s / np.pi)

    _, p, th, sig, kap, dt = solve_mathieu(a_eff)
    _, _, ps = get_psis(a_eff)
    idx_0 = np.argmin(np.abs(th))
    bv = [pp[idx_0] for pp in ps]
    r32 = bv[0]**2 / (bv[1]*bv[2])
    print(f"  {name:>10s}  {mu:10.3f}  {a_s:8.4f}  {a_eff:10.4f}  {kap:8.4f}  {r32:8.1f}  {obs_ratio:10.1f}")

# Higher-order: include EW corrections for top
print(f"\n  --- Including EW + 2-loop QCD ---")
alpha_2 = 0.034
c2 = 3/4  # SU(2) C_F

for name, mu, obs_ratio in fermion_data:
    a_s = alpha_s_running(mu)
    a_s2 = a_s**2  # Two-loop
    if name == 'tau':
        a_eff = alpha_base * (1 + c2*alpha_2/np.pi)
    else:
        a_eff = alpha_base * (1 + c3*a_s/np.pi + c3**2*a_s2/(np.pi**2) + c2*alpha_2/np.pi)

    _, p, th, sig, kap, dt = solve_mathieu(a_eff)
    _, _, ps = get_psis(a_eff)
    idx_0 = np.argmin(np.abs(th))
    bv = [pp[idx_0] for pp in ps]
    r32 = bv[0]**2 / (bv[1]*bv[2])
    print(f"  {name:>10s}  α_eff={a_eff:.4f}  κ={kap:.4f}  m₃/m₂={r32:.1f}  (obs: {obs_ratio:.1f})")

# =================================================================
# GAP B: PMNS — USE DIFFERENT Z₃ CHARGES FOR NEUTRINOS
# =================================================================
print("\n" + "="*78)
print("  GAP B: PMNS — COMPUTE WITH DIFFERENT NEUTRINO Z₃ CHARGES")
print("="*78)

# The problem with the naive seesaw: charged leptons and neutrinos
# have the SAME Z₃ structure → U_PMNS ≈ I (no mixing).
# Solution: neutrino right-handed fields have DIFFERENT Z₃ charges.
# If ν_R charges are (1, 2, 0) instead of (0, 1, 2):
# M_R matrix has DIFFERENT structure → misalignment → large mixing.

# Charged lepton mass matrix (diagonal in Z₃ basis):
alpha_ell = 1.48
_, _, psis_ell = get_psis(alpha_ell)
E0_e, psi_e, theta_e, _, _, dth_e = solve_mathieu(alpha_ell)
idx0_e = np.argmin(np.abs(theta_e))

Y_ell_diag = np.array([psis_ell[i][idx0_e]**2 for i in range(3)])
U_ell = np.eye(3)  # Already diagonal in Z₃ basis

# Neutrino: Different Z₃ charge assignment
# ν_R charges: (1, 0, 2) — SHIFTED by one unit
# This means M_R^{ij} ≠ 0 only if (k_νR_i + k_νR_j) ≡ 0 mod 3
# With (1, 0, 2): allowed entries are M_{00}=(1+1≡2, forbidden),
# M_{01}=(1+0≡1, forbidden), M_{02}=(1+2≡0, allowed!),
# M_{11}=(0+0≡0, allowed), M_{12}=(0+2≡2, forbidden),
# M_{22}=(2+2≡1, forbidden)
# So: M_R = [[0, 0, M₀₂], [0, M₁₁, 0], [M₂₀, 0, 0]]

# This is a CYCLIC permutation-like structure!
# With brane localization:
# ν_R₀ at θ=2π/3 (charge 1), ν_R₁ at θ=0 (charge 0), ν_R₂ at θ=-2π/3 (charge 2)

# M_R values from brane localization
M_R_scale = 1e14  # GeV (seesaw scale)
# M₁₁ = ψ_νR₁(0)² × M_R_scale (gen 1 of νR at brane)
# M₀₂ = ψ_νR₀(0) × ψ_νR₂(0) × M_R_scale

_, _, psis_nuR = get_psis(alpha_ell)
# But νR are at DIFFERENT positions due to shifted charges:
# νR₀ at 2π/3, νR₁ at 0, νR₂ at -2π/3 (same as leptons, just labeled differently)

# Actually, the key is the MISMATCH between L and R assignments.
# Let L = (0, 1, 2) as usual, νR = (1, 0, 2).
# Then the Dirac Yukawa Y_D^{ij} has selection rule:
# k_L_i + k_νR_j + k_H ≡ 0 mod 3
# With k_H = 0: k_L_i + k_νR_j ≡ 0 mod 3

# Y_D selection:
# (i,j): k_L + k_νR mod 3
# (0,0): 0+1=1 → forbidden
# (0,1): 0+0=0 → ALLOWED
# (0,2): 0+2=2 → forbidden
# (1,0): 1+1=2 → forbidden
# (1,1): 1+0=1 → forbidden
# (1,2): 1+2=0 → ALLOWED
# (2,0): 2+1=0 → ALLOWED
# (2,1): 2+0=2 → forbidden
# (2,2): 2+2=1 → forbidden

# Y_D = [[0, y₀₁, 0], [0, 0, y₁₂], [y₂₀, 0, 0]]
# This is a CYCLIC PERMUTATION matrix!

y_D = 1e-6  # Dirac Yukawa magnitude
Y_D = np.zeros((3,3))
# Y_01 = ψ_L₀(brane) × ψ_νR₁(brane) (both near brane)
# Y_12 = ψ_L₁(brane) × ψ_νR₂(brane) (both away from brane)
# Y_20 = ψ_L₂(brane) × ψ_νR₀(brane) (both away from brane)
Y_D[0,1] = psis_ell[0][idx0_e] * psis_nuR[0][idx0_e] * y_D  # L₀ × νR₁ (both near θ=0)
Y_D[1,2] = psis_ell[1][idx0_e] * psis_nuR[2][idx0_e] * y_D  # L₁ × νR₂
Y_D[2,0] = psis_ell[2][idx0_e] * psis_nuR[1][idx0_e] * y_D  # L₂ × νR₀

print(f"  Neutrino Dirac Yukawa (cyclic from Z₃ charge shift):")
print(f"    Y_D₀₁ = {Y_D[0,1]/y_D:.6f} × y_D")
print(f"    Y_D₁₂ = {Y_D[1,2]/y_D:.6f} × y_D")
print(f"    Y_D₂₀ = {Y_D[2,0]/y_D:.6f} × y_D")

# M_R matrix (Z₃ charges (1,0,2)):
# Allowed: (0,2), (1,1), (2,0)
M11 = M_R_scale * psis_nuR[0][idx0_e]**2  # νR₁ at brane
M02 = M_R_scale * psis_nuR[1][idx0_e] * psis_nuR[2][idx0_e]  # νR₀ × νR₂ (away)
M_R = np.zeros((3,3))
M_R[1,1] = M11
M_R[0,2] = M02; M_R[2,0] = M02

print(f"\n  Majorana mass matrix:")
print(f"    M₁₁ = {M11:.3e} GeV")
print(f"    M₀₂ = M₂₀ = {M02:.3e} GeV")

# Seesaw: m_ν = -Y_D^T M_R⁻¹ Y_D v²
try:
    M_R_inv = np.linalg.inv(M_R)
    m_nu = -v_EW**2 * Y_D.T @ M_R_inv @ Y_D

    # Diagonalize
    evals_nu, evecs_nu = np.linalg.eigh(m_nu)
    idx_sort = np.argsort(np.abs(evals_nu))
    evals_nu = evals_nu[idx_sort]
    evecs_nu = evecs_nu[:, idx_sort]

    print(f"\n  Neutrino masses:")
    for i in range(3):
        print(f"    m_{i+1} = {np.abs(evals_nu[i])*1e9:.6f} eV")

    # PMNS = U_ell† × U_ν (U_ell = I since ell is diagonal)
    U_PMNS = evecs_nu

    print(f"\n  |U_PMNS|:")
    for i in range(3):
        row = "    "
        for j in range(3):
            row += f"{np.abs(U_PMNS[i,j]):8.4f}  "
        print(row)

    # Extract angles
    s13_sq = np.abs(U_PMNS[0,2])**2
    c13_sq = 1 - s13_sq
    s12_sq = np.abs(U_PMNS[0,1])**2 / c13_sq if c13_sq > 0 else 0
    s23_sq = np.abs(U_PMNS[1,2])**2 / c13_sq if c13_sq > 0 else 0

    print(f"\n  PMNS angles:")
    print(f"    sin²θ₁₂ = {s12_sq:.4f}  (obs: 0.303)")
    print(f"    sin²θ₂₃ = {s23_sq:.4f}  (obs: 0.572)")
    print(f"    sin²θ₁₃ = {s13_sq:.5f}  (obs: 0.02203)")

    # Tune y_D for correct mass scale
    dm31_obs = 2.511e-3  # eV²
    m3_sq_computed = evals_nu[2]**2 * 1e18  # convert GeV² to eV²
    if m3_sq_computed > 0:
        scale_factor = np.sqrt(dm31_obs / m3_sq_computed)
        y_D_corrected = y_D * np.sqrt(scale_factor)
        print(f"\n  Mass scale calibration:")
        print(f"    y_D needed = {y_D_corrected:.3e}")

        # Recompute with correct y_D
        Y_D2 = Y_D * scale_factor
        m_nu2 = -v_EW**2 * Y_D2.T @ M_R_inv @ Y_D2
        evals2, evecs2 = np.linalg.eigh(m_nu2)
        idx2 = np.argsort(np.abs(evals2))
        evals2 = evals2[idx2]

        dm21 = (evals2[1]**2 - evals2[0]**2) * 1e18
        dm31 = (evals2[2]**2 - evals2[0]**2) * 1e18
        print(f"    Δm²₂₁ = {dm21:.3e} eV²  (obs: 7.41e-5)")
        print(f"    Δm²₃₁ = {dm31:.3e} eV²  (obs: 2.511e-3)")
        if dm21 != 0:
            print(f"    Ratio Δm²₃₁/Δm²₂₁ = {dm31/dm21:.1f}  (obs: 33.9)")

except np.linalg.LinAlgError:
    print("  M_R is singular — trying pseudoinverse")
    M_R_inv = np.linalg.pinv(M_R)
    m_nu = -v_EW**2 * Y_D.T @ M_R_inv @ Y_D
    evals_nu, evecs_nu = np.linalg.eigh(m_nu)
    print(f"  Eigenvalues: {evals_nu}")

# =================================================================
# GAP C: α_eff — RESUMMED KK TOWER
# =================================================================
print("\n" + "="*78)
print("  GAP C: α_eff — RESUMMED KK TOWER (EXACT SUM)")
print("="*78)

# The one-loop CW potential from the full KK tower:
# V_CW(θ) = -1/(64π⁶L⁴) Σ_n Σ_flavors 1/n⁵ cos(n·θ) × (-1)^F
# The EXACT sum can be done using the polylogarithm:
# Σ 1/n⁵ cos(nθ) = Re[Li₅(e^{iθ})]

# But we need the CURVATURE at θ=0:
# V''(0) = 1/(64π⁶L⁴) Σ_n Σ_f n²/n⁵ = 1/(64π⁶L⁴) × N_eff × ζ(3)
# where N_eff counts the effective d.o.f.

# SM fermion contribution (with Z₃ phases):
# Each fermion flavor contributes:
# δα = -(7/8) × 1/(4π²) × Σ_n cos(n·θ_Z3)/n³
# With θ_Z3 = 2πk/3 for Z₃ charge k:

# Exact sum of the potential curvature from all SM fields
zeta3 = 1.202056903  # ζ(3)

# Z₃ charge assignments for SM fermions (generation index → Z₃ charge)
# Q_L: (0, 1, 2), u_R: (0, 1, 2), d_R: (1, 2, 0), L_L: (0, 1, 2), e_R: (0, 1, 2), ν_R: (1, 0, 2)
# For each fermion, the contribution to V''(0) depends on its Z₃ charge k:
# f(k) = Σ_n cos(2πnk/3)/n³

def kk_sum_cos(k, N_max=1000):
    """Compute Σ_{n=1}^{N_max} cos(2πnk/3)/n³"""
    s = 0
    for n in range(1, N_max+1):
        s += np.cos(2*np.pi*n*k/3) / n**3
    return s

f0 = kk_sum_cos(0)  # = ζ(3) = 1.202
f1 = kk_sum_cos(1)
f2 = kk_sum_cos(2)

print(f"\n  KK sums: f(0) = {f0:.6f} [= ζ(3) = {zeta3:.6f}]")
print(f"           f(1) = {f1:.6f}")
print(f"           f(2) = {f2:.6f}")

# Total contribution from SM fermions to α_eff:
# Count: per generation, 15 Weyl fermions (quarks + leptons, without νR)
# or 16 with νR.
# Each with Z₃ charge k contributes f(k) to the sum.

# Gen 0 (k=0): Q_L(3×2=6), u_R(3), e_R(1) = 10 fermions, charge 0
# Gen 1 (k=1): Q_L(6), u_R(3), e_R(1) = 10, charge 1
# Gen 2 (k=2): Q_L(6), u_R(3), e_R(1) = 10, charge 2
# Plus d_R: gen 0 at k=1, gen 1 at k=2, gen 2 at k=0 → 3+3+3=9
# Plus L_L: gen 0 at k=0, gen 1 at k=1, gen 2 at k=2 → 2+2+2=6
# Plus ν_R: gen 0 at k=1, gen 1 at k=0, gen 2 at k=2 → 1+1+1=3

n_f_k0 = 10 + 3 + 2 + 1  # gen 0 fermions + d_R(gen2) + L_L(gen0) + νR(gen1) at k=0
n_f_k1 = 10 + 3 + 2 + 1  # gen 1 fermions + d_R(gen0) + L_L(gen1) + νR(gen0)
n_f_k2 = 10 + 3 + 2 + 1  # gen 2 fermions + d_R(gen1) + L_L(gen2) + νR(gen2)

delta_alpha_KK_exact = -(7/8) / (4*np.pi**2) * (n_f_k0*f0 + n_f_k1*f1 + n_f_k2*f2)
print(f"\n  Fermion KK contribution to α:")
print(f"    n_f(k=0) = {n_f_k0}, n_f(k=1) = {n_f_k1}, n_f(k=2) = {n_f_k2}")
print(f"    δα_KK = -(7/8)/(4π²) × Σ n_f(k)×f(k) = {delta_alpha_KK_exact:.6f}")

# Bosonic contribution (gauge + Higgs):
# Gauge: 24 bosonic d.o.f. at k=0 (singlet under Z₃)
# Higgs: 4 real scalars at k=0
n_b_k0 = 24 + 4 + 2  # gauge + Higgs + R-field
delta_alpha_KK_boson = 1/(4*np.pi**2) * n_b_k0 * f0
print(f"    Bosonic: n_b(k=0) = {n_b_k0}")
print(f"    δα_KK(boson) = +1/(4π²) × n_b × f(0) = {delta_alpha_KK_boson:.6f}")

delta_alpha_total = delta_alpha_KK_boson + delta_alpha_KK_exact
print(f"    Total δα_KK = {delta_alpha_total:.6f}")

alpha_eff_resummed = 1.0 * (1 + delta_alpha_total) * 1.072 * 1.076
E0r, _, _, sigr, kapr, _ = solve_mathieu(alpha_eff_resummed)
lamr = np.exp(-kapr**2/4)

print(f"\n  α_eff (resummed KK) = {alpha_eff_resummed:.4f}")
print(f"  κ = {kapr:.4f}, λ = exp(-κ²/4) = {lamr:.5f}")
print(f"  Target λ = 0.22500, deviation = {(lamr/0.225-1)*100:+.1f}%")

# =================================================================
# GAP D: GAUGE COUPLINGS — ORBIFOLD GUT BREAKING
# =================================================================
print("\n" + "="*78)
print("  GAP D: sin²θ_W FROM ORBIFOLD GUT BREAKING")
print("="*78)

# In a Z₃ orbifold GUT: SU(5) → SU(3)×SU(2)×U(1) at M_KK
# The orbifold boundary conditions MODIFY the tree-level relation.
# sin²θ_W = 3/8 at M_GUT, then runs down.

# With M_KK = 516 GeV and standard SU(5) embedding:
b1_SM = 41.0/10; b2_SM = -19.0/6; b3_SM = -7.0
M_Z = 91.2

# sin²θ_W at M_KK from GUT boundary condition:
# At the Z₃ orbifold: sin²θ_W(M_KK) = 3/8 + corrections
# KK threshold correction:
# Δsin²θ_W = -(3α/(20π)) × Σ_n [b₁^(n) - (5/3)b₂^(n)] × ln(m_n/M_KK)
# For Z₃: each KK level contributes differently

# SM running from M_KK to M_Z:
t_down = np.log(M_KK/M_Z)

# Start with sin²θ_W(M_KK) = 3/8 = 0.375 (SU(5) boundary)
# Then add threshold corrections and run down
sin2_W_GUT = 3.0/8

# Threshold correction from Z₃ orbifold:
# The X,Y bosons of SU(5) get mass M_KK from the orbifold
# Their contribution shifts sin²θ_W:
# Δ = (α/(6π)) × [12×5/3 - 8] × ln(M_GUT/M_KK) (X,Y boson contribution)
# For M_GUT = M_KK (orbifold GUT): this is zero
# But there's a finite threshold from the split multiplets:
delta_sin2_orbifold = -(0.034/(6*np.pi)) * (12*5/3 - 8) * np.log(M_KK/M_Z) * 0  # Zero at M_KK=M_GUT

# One-loop running from M_KK down to M_Z:
# sin²θ_W(M_Z) = sin²θ_W(M_KK) + (α/4π) × (b₁-5/3·b₂) × t
alpha_em_MKK = 1.0/127.0
delta_running = alpha_em_MKK/(4*np.pi) * (b1_SM - 5.0/3*b2_SM) * t_down

sin2_W_pred = sin2_W_GUT + delta_running
print(f"  SU(5) orbifold GUT on S¹/Z₃:")
print(f"    sin²θ_W(M_GUT) = 3/8 = {sin2_W_GUT:.4f}")
print(f"    Running M_KK→M_Z: Δ = {delta_running:+.4f}")
print(f"    sin²θ_W(M_Z) = {sin2_W_pred:.4f}")
print(f"    Observed: 0.23121")
print(f"    Deviation: {(sin2_W_pred/0.23121-1)*100:+.1f}%")

# The problem: starting at 3/8 and running only 1.73 decades is not enough.
# Need: sin²θ_W drops from 3/8=0.375 to 0.231 over 17 decades (M_GUT=10¹⁶).
# With M_KK=516, only 1.73 decades → drops to ~0.365.

# RESOLUTION: The Z₃ orbifold does NOT have SU(5) at M_KK.
# Instead, it has SU(3)×SU(2)×U(1) at ALL scales, with Z₃ relating them.
# The prediction is: α₁⁻¹ : α₂⁻¹ : α₃⁻¹ ratios at M_KK from Z₃ structure.

# Z₃ orbifold prediction: the RATIO of couplings at M_KK
# is determined by the Z₃ HOLONOMY acting on each gauge factor.
# For Z₃ ⊂ SU(3): the holonomy contributes differently to each coupling.
# sin²θ_W = (α₁/(α₁+α₂)) × 3/5 at the Z₃ scale

# Using SM running values at M_KK:
alpha1_MKK = (5.0/3) * (1.0/127.951) / (1 - (5.0/3)*(1.0/127.951)*b1_SM*t_down/(2*np.pi))
alpha2_MKK = 0.0338 / (1 - 0.0338*b2_SM*t_down/(2*np.pi))
alpha3_MKK = 0.1180 / (1 - 0.1180*b3_SM*t_down/(2*np.pi))

sin2_W_SM = alpha1_MKK / (alpha1_MKK + (5.0/3)*alpha2_MKK)
print(f"\n  SM running to M_KK = 516 GeV:")
print(f"    sin²θ_W(M_KK) = {sin2_W_SM:.5f}")
print(f"    This is just SM running — no new prediction from Z₃.")

# α_s prediction: from the Z₃ constraint on the KK spectrum
# At the orbifold fixed points, there's a relation:
# α₃(M_KK) = α₂(M_KK) × C₃/C₂ where C_i are Casimir factors
# For Z₃: C₃/C₂ = 3/2 (from Z₃ embedding in SU(3) vs SU(2))
alpha3_Z3_pred = alpha2_MKK * 3.0/2
alpha_s_Z3_pred = alpha3_Z3_pred  # At M_KK

# Run back to M_Z
t_up = t_down
alpha_s_MZ_pred = alpha3_Z3_pred / (1 + alpha3_Z3_pred * b3_SM * t_up / (2*np.pi))

print(f"\n  Z₃ Casimir ratio prediction:")
print(f"    α₃(M_KK) = (3/2)×α₂(M_KK) = {alpha3_Z3_pred:.4f}")
print(f"    Running to M_Z: α_s(M_Z) = {alpha_s_MZ_pred:.4f}")
print(f"    Observed: α_s(M_Z) = 0.1180")
print(f"    Deviation: {(alpha_s_MZ_pred/0.1180-1)*100:+.1f}%")

# =================================================================
# SUMMARY
# =================================================================
print("\n" + "="*78)
print("  v6.3 FORCE CLOSURE SUMMARY")
print("="*78)

print(f"""
  ┌──────────────────────────────────────────────────────────────────────┐
  │  COMPUTED RESULTS (no words, just numbers)                          │
  ├──────────────────────────────────────────────────────────────────────┤
  │                                                                      │
  │  MASS HIERARCHY (brane-localized Higgs, RG-enhanced α):             │
  │    Top sector:   α_eff = {alpha_f*(1+c3*0.108/np.pi):.3f}  m₃/m₂ = computed above       │
  │    Bottom sector: α_eff = {alpha_f*(1+c3*0.215/np.pi):.3f}  m₃/m₂ = computed above      │
  │    Tau sector:    α_eff = {alpha_f*(1+0.75*0.034/np.pi):.3f}  m₃/m₂ = computed above     │
  │                                                                      │
  │  PMNS (cyclic Z₃ charge shift for νR):                              │
  │    sin²θ₁₂ = {s12_sq:.4f}  (obs 0.303)                              │
  │    sin²θ₂₃ = {s23_sq:.4f}  (obs 0.572)                              │
  │    sin²θ₁₃ = {s13_sq:.5f}  (obs 0.02203)                           │
  │                                                                      │
  │  α_eff (resummed KK):                                               │
  │    α_eff = {alpha_eff_resummed:.4f}  →  λ = {lamr:.5f} (obs 0.225)              │
  │                                                                      │
  │  GAUGE (Z₃ Casimir ratio):                                          │
  │    α_s(M_Z) = {alpha_s_MZ_pred:.4f}  (obs 0.1180, {(alpha_s_MZ_pred/0.1180-1)*100:+.1f}%)              │
  │    sin²θ_W stays SM — no new Z₃ prediction at M_KK = 516            │
  └──────────────────────────────────────────────────────────────────────┘
""")
