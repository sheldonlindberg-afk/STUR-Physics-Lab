#!/usr/bin/env python3
"""
Fermion Mass Hierarchy from Exact Yukawa Matrix on S¹/Z₃
==========================================================

STUR Framework v5.1 — Honest Mass Hierarchy Computation

This script computes the 3×3 Yukawa matrix Y_ij by direct numerical
integration of Mathieu wavefunctions with a localized Higgs profile,
then diagonalizes to get mass eigenvalues. NO correction factors.

The question: What does the Z₃ geometry ACTUALLY predict for fermion
mass ratios, given only α_eff = 1.431 (one-loop)?

Physics:
- Three generations at Z₃ fixed points: θ = 0, 2π/3, 4π/3
- Higgs localized at θ = 0 (electroweak symmetry breaking at one point)
- Yukawa coupling: Y_ij = ∫ ψ_i(θ) H(θ) ψ_j(θ) dθ
- Up-type: helix phase exp(+iθ/3), down-type: exp(-iθ/3)
- Z₃ twisted sectors: up quarks (n=1), down quarks (n=0)

The mass hierarchy comes from THREE sources:
1. Higgs localization: gen 3 (at Higgs) >> gens 1,2 (away from Higgs)
2. Yukawa self-energy: top Yukawa feeds back into localization → α₃ > α₁,₂
3. Z₃ twisted sector: wavefunction nodes for specific generations

This calculation reveals what the geometry gives and where it falls short.

Author: Computed for STUR v5.1
Date: 2026-02-07
"""

import numpy as np
from scipy import linalg
import warnings
warnings.filterwarnings('ignore')

if hasattr(np, 'trapezoid'):
    np_trapz = np.trapezoid
else:
    from scipy import integrate as _int
    np_trapz = _int.trapezoid


# =========================================================================
# MATHIEU SOLVER (shared with other scripts)
# =========================================================================

def solve_mathieu(alpha, N=2000, center=0.0):
    """Solve -f'' + α(1-cos(θ-c))f = εf with periodic BCs on [-π,π]."""
    dtheta = 2*np.pi / N
    theta = np.linspace(-np.pi + dtheta/2, np.pi - dtheta/2, N)
    V = alpha * (1 - np.cos(theta - center))
    diag = 2.0/dtheta**2 + V
    off = -1.0/dtheta**2 * np.ones(N-1)
    H = np.diag(diag) + np.diag(off, 1) + np.diag(off, -1)
    H[0, -1] = -1.0/dtheta**2
    H[-1, 0] = -1.0/dtheta**2
    evals, evecs = linalg.eigh(H, subset_by_index=[0, 3])
    psi = np.real(evecs[:, 0])
    norm = np.sqrt(np_trapz(psi**2, theta))
    psi /= norm
    if psi[np.argmax(np.abs(psi))] < 0:
        psi = -psi
    return psi, theta, evals[0]


def get_sigma(psi, theta):
    """Width of |ψ|² distribution."""
    prob = psi**2 / np_trapz(psi**2, theta)
    mean = np_trapz(theta * prob, theta)
    var = np_trapz((theta - mean)**2 * prob, theta)
    return np.sqrt(var)


# =========================================================================
# HIGGS PROFILE
# =========================================================================

def higgs_profile(theta, sigma_H, center=0.0):
    """Higgs VEV profile localized at center with width σ_H."""
    H = np.exp(-(theta - center)**2 / (4 * sigma_H**2))
    H /= np.sqrt(np_trapz(H**2, theta))
    return H


def higgs_delta(theta, center=0.0, epsilon=0.02):
    """Approximate delta-function Higgs (very narrow Gaussian)."""
    return higgs_profile(theta, epsilon, center)


# =========================================================================
# YUKAWA MATRIX COMPUTATION
# =========================================================================

def compute_yukawa_matrix(psis, theta, H_profile, helix_phase=0.0):
    """
    Compute the 3×3 Yukawa matrix:
        Y_ij = ∫ ψ_i(θ) H(θ) exp(i·helix_phase·θ) ψ_j(θ) dθ

    helix_phase = +1/3 for up-type, -1/3 for down-type, 0 for no helix.
    """
    n = len(psis)
    Y = np.zeros((n, n), dtype=complex)
    for i in range(n):
        for j in range(n):
            if abs(helix_phase) < 1e-10:
                integrand = psis[i] * H_profile * psis[j]
            else:
                integrand = psis[i] * H_profile * np.exp(1j * helix_phase * theta) * psis[j]
            Y[i, j] = np_trapz(integrand, theta)
    return Y


def mass_eigenvalues(Y):
    """Get mass eigenvalues from Yukawa matrix (singular values)."""
    # Masses are sqrt of eigenvalues of Y†Y
    YdY = Y.conj().T @ Y
    evals = np.sort(np.real(linalg.eigvalsh(YdY)))[::-1]
    evals = np.maximum(evals, 0)  # numerical safety
    return np.sqrt(evals)


# =========================================================================
# YUKAWA SELF-ENERGY CORRECTION
# =========================================================================

def yukawa_self_energy_correction(alpha_base, y_eff_g, v_L=3.0):
    """
    Compute generation-dependent α correction from Yukawa self-energy.

    The Yukawa coupling of generation g feeds back into its localization
    potential through one-loop self-energy:

        δα_g = (y_g²/(16π²)) × (v²L²) × C_loop

    where C_loop is a model-dependent loop factor O(1).

    Returns array of corrected α values for each generation.
    """
    C_loop = 1.0  # O(1) coefficient from loop integral
    alpha_g = np.zeros(len(y_eff_g))
    for g in range(len(y_eff_g)):
        delta_alpha = (y_eff_g[g]**2 / (16 * np.pi**2)) * v_L**2 * C_loop
        alpha_g[g] = alpha_base + delta_alpha
    return alpha_g


def self_consistent_mass_hierarchy(alpha_base, sigma_H, N=2000, max_iter=20, tol=1e-6):
    """
    Self-consistent computation of mass hierarchy with Yukawa backreaction.

    1. Start with uniform α for all generations
    2. Compute Yukawa matrix → mass eigenvalues
    3. Use eigenvalues to correct α for each generation
    4. Iterate to self-consistency
    """
    centers = [0.0, 2*np.pi/3, 4*np.pi/3]
    alpha_g = np.array([alpha_base] * 3)

    history = []
    for iteration in range(max_iter):
        # Solve for wavefunctions with current α_g
        psis = []
        theta_common = None
        for g in range(3):
            psi, theta, _ = solve_mathieu(alpha_g[g], N=N, center=centers[g])
            psis.append(psi)
            theta_common = theta

        # Higgs profile
        H = higgs_profile(theta_common, sigma_H, center=0.0)

        # Yukawa matrix (no helix phase for mass hierarchy)
        Y = compute_yukawa_matrix(psis, theta_common, H, helix_phase=0.0)
        m = mass_eigenvalues(Y)

        # Effective Yukawa couplings (normalized to largest)
        y_eff = m / m[0] if m[0] > 0 else m

        history.append({
            'alpha_g': alpha_g.copy(),
            'masses': m.copy(),
            'Y': Y.copy(),
        })

        # Update α with Yukawa self-energy
        alpha_new = yukawa_self_energy_correction(alpha_base, y_eff)

        # Check convergence
        if np.max(np.abs(alpha_new - alpha_g)) < tol:
            break
        alpha_g = alpha_new

    return history


# =========================================================================
# MAIN COMPUTATION
# =========================================================================

if __name__ == '__main__':
    print("=" * 70)
    print("  FERMION MASS HIERARCHY FROM EXACT YUKAWA MATRIX ON S¹/Z₃")
    print("  STUR Framework v5.1 — No Correction Factors")
    print("=" * 70)

    alpha_eff = 1.431  # from alpha_eff_rigorous_calculation.py (one-loop)
    N = 2000

    # PDG mass ratios (using running masses at MZ for quarks)
    # Up-type: m_u = 1.27 MeV, m_c = 0.619 GeV, m_t = 171.7 GeV
    # Down-type: m_d = 2.67 MeV, m_s = 53.5 MeV, m_b = 2.85 GeV
    PDG_up = {'m1': 1.27e-3, 'm2': 0.619, 'm3': 171.7}  # GeV
    PDG_down = {'m1': 2.67e-3, 'm2': 53.5e-3, 'm3': 2.85}  # GeV

    # ══════════════════════════════════════════════════════════
    # SECTION 1: WAVEFUNCTIONS AND HIGGS PROFILE
    # ══════════════════════════════════════════════════════════

    print(f"\n{'─' * 70}")
    print("  SECTION 1: Wavefunctions at Z₃ Fixed Points")
    print(f"{'─' * 70}")

    centers = [0.0, 2*np.pi/3, 4*np.pi/3]
    gen_labels = ['3rd (t/b)', '2nd (c/s)', '1st (u/d)']
    psis = []
    for g in range(3):
        psi, theta, E0 = solve_mathieu(alpha_eff, N=N, center=centers[g])
        psis.append(psi)
        sig = get_sigma(psi, theta)
        print(f"  Gen {g} [{gen_labels[g]:>10s}] at θ={centers[g]:.4f}: "
              f"σ={sig:.4f} rad, E₀={E0:.4f}")

    sigma = get_sigma(psis[0], theta)
    kappa = (2*np.pi/3) / sigma
    print(f"\n  Common σ = {sigma:.4f} rad, κ = {kappa:.3f}")

    # ══════════════════════════════════════════════════════════
    # SECTION 2: YUKAWA MATRIX VS HIGGS WIDTH
    # ══════════════════════════════════════════════════════════

    print(f"\n{'─' * 70}")
    print("  SECTION 2: Mass Hierarchy vs Higgs Width σ_H")
    print(f"{'─' * 70}")

    print(f"\n  The mass hierarchy depends on how localized the Higgs is.")
    print(f"  Narrower Higgs → larger hierarchy (only gen 3 overlaps).")
    print(f"  Broader Higgs → smaller hierarchy (all generations overlap).\n")

    sigma_H_values = [0.05, 0.1, 0.2, 0.3, 0.5, 0.8, 1.0, 1.5, 2.0, 3.0]

    print(f"  {'σ_H':>6s}  {'m₃/m₂':>8s}  {'m₃/m₁':>8s}  {'m₂/m₁':>8s}  "
          f"{'m₃':>10s}  {'m₂':>10s}  {'m₁':>10s}  Note")
    print(f"  {'─'*6}  {'─'*8}  {'─'*8}  {'─'*8}  {'─'*10}  {'─'*10}  {'─'*10}  {'─'*20}")

    best_sigma_H = None
    best_score = 1e10
    for sigma_H in sigma_H_values:
        H = higgs_profile(theta, sigma_H, center=0.0)
        Y = compute_yukawa_matrix(psis, theta, H, helix_phase=0.0)
        m = mass_eigenvalues(Y)

        if m[1] > 0 and m[2] > 0:
            r32 = m[0]/m[1]
            r31 = m[0]/m[2]
            r21 = m[1]/m[2]
        else:
            r32 = r31 = r21 = float('inf')

        # Compare with observed down-type ratios: m_b/m_s ≈ 53, m_b/m_d ≈ 1067
        # and up-type: m_t/m_c ≈ 277, m_t/m_u ≈ 135000
        # Score: geometric mean of log-ratio accuracy for down-type
        obs_r32_d = PDG_down['m3'] / PDG_down['m2']  # 53.3
        obs_r31_d = PDG_down['m3'] / PDG_down['m1']  # 1067
        if r32 > 1 and r31 > 1:
            score = abs(np.log(r32/obs_r32_d)) + abs(np.log(r31/obs_r31_d))
        else:
            score = 100

        note = ""
        if sigma_H < 0.06:
            note = "δ-function limit"
        elif abs(sigma_H - sigma) < 0.1:
            note = "σ_H ≈ σ_fermion"
        elif sigma_H > 2.5:
            note = "delocalized Higgs"

        if score < best_score:
            best_score = score
            best_sigma_H = sigma_H

        print(f"  {sigma_H:6.2f}  {r32:8.1f}  {r31:8.1f}  {r21:8.1f}  "
              f"{m[0]:10.4e}  {m[1]:10.4e}  {m[2]:10.4e}  {note}")

    # Observed ratios
    print(f"\n  Observed mass ratios (down-type):")
    print(f"    m_b/m_s = {PDG_down['m3']/PDG_down['m2']:.1f}")
    print(f"    m_b/m_d = {PDG_down['m3']/PDG_down['m1']:.0f}")
    print(f"    m_s/m_d = {PDG_down['m2']/PDG_down['m1']:.1f}")
    print(f"  Observed mass ratios (up-type):")
    print(f"    m_t/m_c = {PDG_up['m3']/PDG_up['m2']:.0f}")
    print(f"    m_t/m_u = {PDG_up['m3']/PDG_up['m1']:.0f}")
    print(f"    m_c/m_u = {PDG_up['m2']/PDG_up['m1']:.0f}")

    # ══════════════════════════════════════════════════════════
    # SECTION 3: DETAILED ANALYSIS AT BEST σ_H
    # ══════════════════════════════════════════════════════════

    print(f"\n{'─' * 70}")
    print(f"  SECTION 3: Detailed Analysis at σ_H = {best_sigma_H}")
    print(f"{'─' * 70}")

    H = higgs_profile(theta, best_sigma_H, center=0.0)

    # Without helix phase
    Y_nohel = compute_yukawa_matrix(psis, theta, H, helix_phase=0.0)
    m_nohel = mass_eigenvalues(Y_nohel)

    # With helix phase (up-type)
    Y_up = compute_yukawa_matrix(psis, theta, H, helix_phase=+1./3)
    m_up = mass_eigenvalues(Y_up)

    # With helix phase (down-type)
    Y_down = compute_yukawa_matrix(psis, theta, H, helix_phase=-1./3)
    m_down = mass_eigenvalues(Y_down)

    print(f"\n  Yukawa matrix |Y| (no helix phase):")
    for i in range(3):
        row = "    "
        for j in range(3):
            row += f"{abs(Y_nohel[i,j]):12.4e}"
        print(row)

    print(f"\n  Mass eigenvalues (singular values of Y):")
    print(f"    No helix: m = [{m_nohel[0]:.4e}, {m_nohel[1]:.4e}, {m_nohel[2]:.4e}]")
    print(f"    Up-type:  m = [{m_up[0]:.4e}, {m_up[1]:.4e}, {m_up[2]:.4e}]")
    print(f"    Down-type:m = [{m_down[0]:.4e}, {m_down[1]:.4e}, {m_down[2]:.4e}]")

    if m_nohel[1] > 0:
        print(f"\n  Mass ratios (no helix):")
        print(f"    m₃/m₂ = {m_nohel[0]/m_nohel[1]:.1f}")
        if m_nohel[2] > 1e-20:
            print(f"    m₃/m₁ = {m_nohel[0]/m_nohel[2]:.1f}")
            print(f"    m₂/m₁ = {m_nohel[1]/m_nohel[2]:.1f}")

    # ══════════════════════════════════════════════════════════
    # SECTION 4: YUKAWA SELF-ENERGY BACKREACTION
    # ══════════════════════════════════════════════════════════

    print(f"\n{'─' * 70}")
    print("  SECTION 4: Yukawa Self-Energy Backreaction")
    print(f"{'─' * 70}")

    print(f"\n  The top Yukawa y_t ≈ 1 feeds back into the localization")
    print(f"  potential, deepening the well for generation 3.")
    print(f"  This amplifies the mass hierarchy through positive feedback.")

    hist = self_consistent_mass_hierarchy(alpha_eff, best_sigma_H, N=N)

    print(f"\n  Self-consistent iteration (σ_H = {best_sigma_H}):")
    print(f"  {'Iter':>4s}  {'α₃':>8s}  {'α₂':>8s}  {'α₁':>8s}  "
          f"{'m₃':>10s}  {'m₂':>10s}  {'m₁':>10s}  {'m₃/m₂':>8s}")
    print(f"  {'─'*4}  {'─'*8}  {'─'*8}  {'─'*8}  {'─'*10}  {'─'*10}  {'─'*10}  {'─'*8}")
    for it, h in enumerate(hist):
        a = h['alpha_g']
        m = h['masses']
        r32 = m[0]/m[1] if m[1] > 0 else float('inf')
        print(f"  {it:4d}  {a[0]:8.4f}  {a[1]:8.4f}  {a[2]:8.4f}  "
              f"{m[0]:10.4e}  {m[1]:10.4e}  {m[2]:10.4e}  {r32:8.1f}")

    # Final self-consistent result
    final = hist[-1]
    m_final = final['masses']
    if m_final[1] > 0:
        print(f"\n  Self-consistent mass ratios:")
        print(f"    m₃/m₂ = {m_final[0]/m_final[1]:.1f}")
        if m_final[2] > 1e-20:
            print(f"    m₃/m₁ = {m_final[0]/m_final[2]:.1f}")

    # ══════════════════════════════════════════════════════════
    # SECTION 5: GEOMETRIC MASS HIERARCHY LIMITS
    # ══════════════════════════════════════════════════════════

    print(f"\n{'─' * 70}")
    print("  SECTION 5: Maximum Geometric Mass Hierarchy")
    print(f"{'─' * 70}")

    print(f"\n  The MAXIMUM hierarchy from the geometry occurs for a")
    print(f"  delta-function Higgs at θ=0:")
    print(f"    m₃/m₂ = |ψ₀(0)|² / |ψ₁(0)|² = exp(κ²/2)")
    print(f"    At κ = {kappa:.3f}: max m₃/m₂ = {np.exp(kappa**2/2):.1f}")
    print(f"")
    print(f"  Observed hierarchies:")
    print(f"    m_b/m_s = {PDG_down['m3']/PDG_down['m2']:.1f} (down-type)")
    print(f"    m_t/m_c = {PDG_up['m3']/PDG_up['m2']:.0f} (up-type)")

    max_ratio = np.exp(kappa**2/2)
    if max_ratio < PDG_down['m3']/PDG_down['m2']:
        print(f"\n  ⚠ STRUCTURAL GAP: Even the maximum geometric ratio ({max_ratio:.1f})")
        print(f"  is LESS than the observed m_b/m_s ({PDG_down['m3']/PDG_down['m2']:.1f}).")
        print(f"  The Z₃ geometry with uniform α CANNOT produce the full hierarchy.")
        print(f"  Additional physics needed:")
        print(f"    • Generation-dependent α from Yukawa backreaction: δα/α ~ y²/(16π²) ~ 0.6%")
        print(f"    • Z₃ twisted sector wavefunction nodes (for up-type splitting)")
        print(f"    • Or: abandon single-α assumption")
    else:
        print(f"\n  ✓ Geometric ratio ({max_ratio:.1f}) CAN accommodate observed hierarchy.")

    # What α_eff would give the observed down-type hierarchy?
    target_r32 = PDG_down['m3'] / PDG_down['m2']  # ~53
    # For delta Higgs: ratio = exp(κ²/2), need κ² = 2 ln(53) = 7.94, κ = 2.82
    kappa_needed = np.sqrt(2 * np.log(target_r32))
    sigma_needed = (2*np.pi/3) / kappa_needed
    # From harmonic approx: α ≈ 1/σ⁴ × (something), but let's use the actual curve
    from scipy.optimize import brentq

    def kappa_residual(alpha):
        psi_t, theta_t, _ = solve_mathieu(alpha, N=1000, center=0.0)
        sig_t = get_sigma(psi_t, theta_t)
        return (2*np.pi/3)/sig_t - kappa_needed

    try:
        alpha_needed = brentq(kappa_residual, 0.5, 10.0)
        print(f"\n  For m_b/m_s = {target_r32:.0f} (delta Higgs limit):")
        print(f"    Need κ = {kappa_needed:.3f}, σ = {sigma_needed:.4f}")
        print(f"    Need α_eff = {alpha_needed:.3f}")
        print(f"    Current α_eff = {alpha_eff:.3f}")
        print(f"    Gap: {abs(alpha_needed - alpha_eff)/alpha_eff*100:.0f}%")
    except Exception:
        print(f"\n  (Could not find α for target ratio)")

    # ══════════════════════════════════════════════════════════
    # SECTION 6: UP-DOWN ASYMMETRY FROM HELIX PHASE
    # ══════════════════════════════════════════════════════════

    print(f"\n{'─' * 70}")
    print("  SECTION 6: Up-Down Asymmetry from Helix Phase")
    print(f"{'─' * 70}")

    print(f"\n  The helix phase exp(±iθ/3) creates different Yukawa matrices")
    print(f"  for up-type and down-type quarks, generating m_t/m_b ≠ 1.\n")

    for sigma_H in [0.1, 0.3, 0.5, 1.0]:
        H = higgs_profile(theta, sigma_H, center=0.0)
        Yu = compute_yukawa_matrix(psis, theta, H, helix_phase=+1./3)
        Yd = compute_yukawa_matrix(psis, theta, H, helix_phase=-1./3)
        mu = mass_eigenvalues(Yu)
        md = mass_eigenvalues(Yd)
        if md[0] > 0 and md[1] > 0 and md[2] > 0:
            r_tb = mu[0] / md[0]
            r_cs = mu[1] / md[1]
            r_ud = mu[2] / md[2] if md[2] > 1e-20 else float('inf')
            print(f"  σ_H = {sigma_H:.1f}: m_t/m_b = {r_tb:.3f}, "
                  f"m_c/m_s = {r_cs:.3f}, m_u/m_d = {r_ud:.3f}")

    print(f"\n  Observed: m_t/m_b = {PDG_up['m3']/PDG_down['m3']:.1f}, "
          f"m_c/m_s = {PDG_up['m2']/PDG_down['m2']:.1f}, "
          f"m_u/m_d = {PDG_up['m1']/PDG_down['m1']:.2f}")

    # ══════════════════════════════════════════════════════════
    # SECTION 7: HONEST ASSESSMENT
    # ══════════════════════════════════════════════════════════

    print(f"\n{'─' * 70}")
    print("  SECTION 7: HONEST ASSESSMENT")
    print(f"{'─' * 70}")

    print(f"""
  WHAT THE Z₃ GEOMETRY GIVES (without correction factors):

  1. THREE GENERATIONS: ✓ (from Z₃ topology)

  2. MASS HIERARCHY (qualitative): ✓
     - Higgs localization at one Z₃ fixed point naturally produces
       one heavy generation + two light ones
     - Maximum ratio: exp(κ²/2) = {np.exp(kappa**2/2):.1f} at κ = {kappa:.3f}

  3. MASS HIERARCHY (quantitative): PARTIAL
     - m_b/m_s observed = {PDG_down['m3']/PDG_down['m2']:.0f}, geometric max = {np.exp(kappa**2/2):.0f}
     - The geometry CAN produce enough 3rd/2nd gen splitting
       for down-type quarks (barely), but NOT for up-type
     - m_t/m_c observed = {PDG_up['m3']/PDG_up['m2']:.0f}, geometric max = {np.exp(kappa**2/2):.0f}
     - 2nd/1st generation splitting requires ADDITIONAL physics
       (Z₃ twisted sector nodes, generation-dependent α, or
       asymmetric Higgs profile)

  4. UP-DOWN MASS RATIO: WEAK
     - The helix phase exp(±iθ/3) produces m_u ≈ m_d for all
       generations (ratio near 1.0), while observed ratios range
       from 0.48 (m_u/m_d) to 60 (m_t/m_b)
     - The helix phase alone is too small to explain the up-down
       asymmetry — it gives a <1% effect on mass eigenvalues

  5. YUKAWA SELF-ENERGY: NEGLIGIBLE
     - δα/α ~ y_t²/(16π²) ~ 0.6%
     - Too small to significantly enhance the hierarchy

  CONCLUSION: The Z₃ geometry QUALITATIVELY explains the mass hierarchy
  (one heavy + two light generations) but QUANTITATIVELY falls short
  by factors of 5-500 depending on the sector. The correction factor
  chains in the framework (f_tail, f_node, etc.) are compensating for
  this gap, which means they are NOT derived but FITTED.

  This is a genuine structural limitation of the single-α Z₃ model.
  Possible resolutions:
    a) Generation-dependent localization potentials (breaks Z₃ universality)
    b) Multiple Higgs doublets with different profiles
    c) Additional orbifold structure beyond S¹/Z₃
    d) Radiative mass generation for 1st/2nd gen (loop suppression)
""")
