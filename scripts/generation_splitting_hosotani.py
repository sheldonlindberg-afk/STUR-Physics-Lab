#!/usr/bin/env python3
"""
Generation Splitting from Hosotani Mechanism on S¹/Z₃
=====================================================

PROBLEM: Z₃ symmetry forces 1st and 2nd generation to be degenerate.
         The helix phase exp(±iθ/3) gives zero up-down splitting.
         Need a PHYSICAL mechanism to break these degeneracies.

SOLUTION: The Hosotani mechanism (Wilson line VEV on S¹) provides both:
  1. Up-down splitting via different U(1)_Y charges
  2. Generation splitting via Wilson line phases at Z₃ fixed points

PHYSICS:
  On S¹/Z₃ with a Wilson line ⟨A₅⟩ = v_W, fermions with different
  hypercharges Y feel different effective potentials:

    V_eff(θ; Y) = α(1 - cos(θ - θ₀)) + Y·v_W·θ/(2π)

  The Wilson line creates a LINEAR tilt in the periodic potential.
  This shifts the localization center by δθ ∝ Y·v_W/α and changes
  the effective mass through modified overlap integrals.

  At the three Z₃ fixed points θ_k = 2πk/3, the Wilson line
  phases are:
    W_k = exp(i·Y·v_W·2πk/3)

  These are DIFFERENT for k=0,1,2, breaking Z₃ → nothing.

  The mass eigenvalues become:
    m_k ∝ exp(-κ²/4) × |1 + 2cos(2πk/3 + Y·v_W·2π/3)|

  For three generations with k=0,1,2, this gives DIFFERENT masses.

This script computes the EXACT spectrum by solving the Mathieu equation
with a Wilson line tilt for each fermion species.

Author: Claude (v5.2 computation)
"""

import numpy as np
from scipy.linalg import eigh
from scipy.optimize import minimize_scalar

# Parameters
N_BASIS = 40   # Fourier modes for Hamiltonian
N_THETA = 2000 # Grid points
DTHETA = 2 * np.pi / N_THETA

# ============================================================
# PART 1: Mathieu equation with Wilson line
# ============================================================

def solve_mathieu_wilson(alpha, wilson_phase, n_states=6):
    """
    Solve: -f''(θ) + α(1 - cos θ)f(θ) + w·θ/(2π) f(θ) = ε f(θ)

    on S¹ with periodic BCs, where w = wilson_phase.

    The Wilson line adds a CONSTANT gauge field A₅ = w/(2πR).
    For a charged fermion, this shifts the momentum:
      p → p - Y·A₅

    In the Fourier basis |m⟩ = exp(imθ)/√(2π):
      H_{mm'} = (m - w/(2π))² δ_{mm'} + α δ_{mm'} - (α/2)(δ_{m,m'+1} + δ_{m,m'-1})

    Actually, the proper way: the Wilson line for a fermion with charge Y
    on S¹ shifts the KK momenta: m → m + Y·⟨A₅⟩·R.

    Let's define ξ = Y·⟨A₅⟩·R as the dimensionless Wilson line parameter.
    Then the Hamiltonian in Fourier basis is:

      H_{mm'} = (m + ξ)² δ_{mm'} + α[δ_{mm'} - (1/2)(δ_{m,m'+1} + δ_{m,m'-1})]
    """
    n = N_BASIS
    dim = 2*n + 1
    H = np.zeros((dim, dim))

    xi = wilson_phase  # dimensionless shift

    for i, m in enumerate(range(-n, n+1)):
        # Kinetic + Wilson line shift
        H[i, i] = (m + xi)**2 + alpha
        # Cosine potential
        for j, mp in enumerate(range(-n, n+1)):
            if mp == m + 1 or mp == m - 1:
                H[i, j] -= alpha / 2

    evals, evecs = eigh(H)

    # Convert to position-space wavefunctions
    theta = np.linspace(0, 2*np.pi, N_THETA, endpoint=False)
    psi_grid = np.zeros((n_states, N_THETA), dtype=complex)

    for k in range(n_states):
        for i, m in enumerate(range(-n, n+1)):
            psi_grid[k] += evecs[i, k] * np.exp(1j * m * theta) / np.sqrt(2*np.pi)

    # Normalize
    for k in range(n_states):
        norm = np.sqrt(np.trapezoid(np.abs(psi_grid[k])**2, theta))
        psi_grid[k] /= norm

    return evals[:n_states], psi_grid, theta


def compute_overlap(psi1, psi2, theta):
    """Compute overlap integral ⟨ψ₁|ψ₂⟩."""
    return np.trapezoid(np.conj(psi1) * psi2, theta)


def compute_yukawa_matrix(alpha, xi_u, xi_d, higgs_profile=None):
    """
    Compute the 3×3 Yukawa matrix Y_{ij} for up-type or down-type quarks.

    The three generations correspond to the three lowest-energy states
    of the Mathieu equation on S¹/Z₃.

    On S¹/Z₃, states must satisfy ψ(θ + 2π/3) = ω^k ψ(θ) for k=0,1,2.
    This means the Fourier modes are restricted to m ≡ k (mod 3).

    The Wilson line ξ depends on the fermion species (through hypercharge Y).
    """
    # Solve for up-type with ξ_u
    evals_u, psi_u, theta = solve_mathieu_wilson(alpha, xi_u, n_states=6)
    # Solve for down-type with ξ_d
    evals_d, psi_d, theta_d = solve_mathieu_wilson(alpha, xi_d, n_states=6)

    return evals_u, evals_d, psi_u, psi_d, theta


# ============================================================
# PART 2: Z₃ orbifold projection
# ============================================================

def solve_z3_sector(alpha, xi, sector_k, n_states=3):
    """
    Solve the Mathieu equation restricted to Z₃ sector k.

    On S¹/Z₃, the orbifold projection requires:
      ψ(θ + 2π/3) = ω^k ψ(θ),  ω = e^{2πi/3}

    This restricts Fourier modes to m ≡ k (mod 3).

    In the restricted basis |m⟩ with m = k, k±3, k±6, ...:
      H_{mm'} = (m + ξ)² δ_{mm'} + α δ_{mm'} - (α/2)(δ_{m,m'+1} + δ_{m,m'-1})

    But wait — the cosine couples m to m±1, which are in DIFFERENT Z₃ sectors.
    So on the orbifold, we need to be more careful.

    The Z₃ projection onto sector k selects:
      |ψ_k⟩ = (1/3)Σ_{n=0}^{2} ω^{-kn} T^n |ψ⟩

    where T is the translation by 2π/3.

    More practically: solve the full problem on S¹, then project.
    The Z₃ eigenvalues are the eigenvalues of the translation operator
    T: ψ(θ) → ψ(θ + 2π/3) restricted to each sector.
    """
    n = N_BASIS
    dim = 2*n + 1
    H = np.zeros((dim, dim), dtype=complex)

    for i, m in enumerate(range(-n, n+1)):
        H[i, i] = (m + xi)**2 + alpha
        for j, mp in enumerate(range(-n, n+1)):
            if mp == m + 1 or mp == m - 1:
                H[i, j] -= alpha / 2

    # Also build the Z₃ translation operator T in Fourier basis
    # T|m⟩ = exp(i·m·2π/3)|m⟩
    omega = np.exp(2j * np.pi / 3)
    T = np.zeros((dim, dim), dtype=complex)
    for i, m in enumerate(range(-n, n+1)):
        T[i, i] = np.exp(1j * m * 2 * np.pi / 3)

    # Z₃ projector onto sector k: P_k = (1/3)(I + ω^{-k}T + ω^{-2k}T²)
    I = np.eye(dim, dtype=complex)
    T2 = T @ T
    omega_k = omega**(-sector_k)
    P_k = (I + omega_k * T + omega_k**2 * T2) / 3.0

    # Project Hamiltonian: H_k = P_k H P_k
    H_k = P_k @ H @ P_k

    # Diagonalize in the projected subspace
    evals_full, evecs_full = eigh(H_k)

    # The projected space has dim/3 non-zero eigenvalues
    # Filter out the zero eigenvalues (from the null space of P_k)
    # Check which eigenvectors are in the image of P_k
    good_indices = []
    for i in range(dim):
        # Check if this eigenvector is in the image of P_k
        v = evecs_full[:, i]
        Pv = P_k @ v
        overlap = np.abs(np.vdot(v, Pv))
        if overlap > 0.5:  # In the projected subspace
            good_indices.append(i)

    sector_evals = evals_full[good_indices[:n_states]]
    sector_evecs = evecs_full[:, good_indices[:n_states]]

    # Convert to position space
    theta = np.linspace(0, 2*np.pi, N_THETA, endpoint=False)
    psi_grid = np.zeros((n_states, N_THETA), dtype=complex)

    for k_idx in range(min(n_states, len(sector_evals))):
        for i, m in enumerate(range(-n, n+1)):
            psi_grid[k_idx] += sector_evecs[i, k_idx] * np.exp(1j * m * theta) / np.sqrt(2*np.pi)
        norm = np.sqrt(np.trapezoid(np.abs(psi_grid[k_idx])**2, theta))
        if norm > 1e-10:
            psi_grid[k_idx] /= norm

    return sector_evals, psi_grid, theta


# ============================================================
# PART 3: Mass matrix from overlaps
# ============================================================

def compute_mass_matrix(alpha, xi_up, xi_down):
    """
    Compute the 3×3 mass matrices for up-type and down-type quarks.

    Each generation corresponds to a Z₃ sector k = 0, 1, 2.
    The mass comes from the overlap of the up-type wavefunction in
    sector k_L with the down-type (or same-type) in sector k_R,
    mediated by the Higgs profile.

    For diagonal masses (same generation):
      m_k ∝ ⟨ψ_k^L | H(θ) | ψ_k^R⟩

    where H(θ) is the Higgs profile (localized or constant on S¹).
    """
    # Get wavefunctions in each Z₃ sector
    up_sectors = []
    down_sectors = []

    for k in range(3):
        evals_u, psi_u, theta = solve_z3_sector(alpha, xi_up, k, n_states=1)
        evals_d, psi_d, _ = solve_z3_sector(alpha, xi_down, k, n_states=1)
        up_sectors.append((evals_u[0], psi_u[0]))
        down_sectors.append((evals_d[0], psi_d[0]))

    # Mass matrix: M_{ij} = ⟨up_i | down_j⟩ (overlap integral)
    M = np.zeros((3, 3), dtype=complex)
    for i in range(3):
        for j in range(3):
            M[i, j] = compute_overlap(up_sectors[i][1], down_sectors[j][1], theta)

    return M, up_sectors, down_sectors, theta


# ============================================================
# PART 4: SM hypercharges and Wilson line
# ============================================================

# SM fermion hypercharges (Y = Q - T₃)
Y_Q_L = 1/6    # Left-handed quark doublet
Y_u_R = 2/3    # Right-handed up-type
Y_d_R = -1/3   # Right-handed down-type
Y_L_L = -1/2   # Left-handed lepton doublet
Y_e_R = -1     # Right-handed charged lepton
Y_nu_R = 0     # Right-handed neutrino (if exists)

# SU(3) color: quarks also feel the color Wilson line
# For SU(3), the Wilson line at Z₃ fixed points gives phases:
#   W_color = diag(ω, ω², 1) where ω = e^{2πi/3}
# This means the three colors at each fixed point get different shifts.

def compute_full_spectrum(alpha, v_wilson):
    """
    Compute the full fermion mass spectrum on S¹/Z₃ with Wilson line.

    The Wilson line parameter v_W enters through ξ = Y · v_W for each fermion.

    For the SU(3) color Wilson line at Z₃ fixed points:
      The holonomy W = diag(e^{i2π/3}, e^{i4π/3}, 1) in SU(3)
      gives additional phases to each color.

    The TOTAL Wilson line shift for a quark of color c and hypercharge Y is:
      ξ = Y · v_W + (color phase_c) / (2π)

    For the three colors: phase_c = 0, 2π/3, 4π/3
    """
    print("="*70)
    print(f"FULL SPECTRUM: α = {alpha:.3f}, v_Wilson = {v_wilson:.4f}")
    print("="*70)

    # Quark masses: need to diagonalize 3×3 matrix in generation space
    # For each quark type (u, d), there are 3 generations × 3 colors

    # But let's first do the simpler calculation:
    # Each generation corresponds to Z₃ sector k = 0, 1, 2
    # The Wilson line shift for sector k is ξ + k·(something)

    # Actually, the key physics is:
    # On S¹/Z₃, the Wilson line ⟨A₅⟩ = v_W gives a shift ξ = Y·v_W
    # The Z₃ sectors at the three fixed points experience:
    #   ξ_k = Y·v_W + k·(color contribution)

    # For a SINGLE color (simplest case first):
    print("\n--- Single-color spectrum (no color Wilson line) ---")

    for fermion_name, Y_L, Y_R in [
        ("up quark", Y_Q_L, Y_u_R),
        ("down quark", Y_Q_L, Y_d_R),
        ("charged lepton", Y_L_L, Y_e_R),
        ("neutrino", Y_L_L, Y_nu_R),
    ]:
        xi_L = Y_L * v_wilson
        xi_R = Y_R * v_wilson

        print(f"\n  {fermion_name}: Y_L = {Y_L:.3f}, Y_R = {Y_R:.3f}")
        print(f"    ξ_L = {xi_L:.4f}, ξ_R = {xi_R:.4f}")

        # Get Z₃ sector energies for left and right
        masses_diag = []
        for k in range(3):
            evals_L, psi_L, theta = solve_z3_sector(alpha, xi_L, k, n_states=1)
            evals_R, psi_R, _ = solve_z3_sector(alpha, xi_R, k, n_states=1)

            # Diagonal mass: overlap between L and R in same sector
            overlap = np.abs(compute_overlap(psi_L[0], psi_R[0], theta))

            # The physical mass is proportional to v_EW × Yukawa
            # Yukawa ∝ overlap × (phase factor from Wilson line)
            # Phase factor: exp(i·(ξ_L - ξ_R)·2πk/3) from Wilson line at fixed point k
            wilson_phase = np.exp(1j * (xi_L - xi_R) * 2 * np.pi * k / 3)

            mass_k = overlap  # proportional to mass
            masses_diag.append(mass_k)

            print(f"    Sector k={k}: E_L = {evals_L[0]:.4f}, E_R = {evals_R[0]:.4f}, "
                  f"|overlap| = {overlap:.6f}")

        masses_arr = np.array(masses_diag)
        if masses_arr[0] > 1e-10:
            ratios = masses_arr / masses_arr[0]
            print(f"    Mass ratios (k=0:1:2): {ratios[0]:.4f} : {ratios[1]:.4f} : {ratios[2]:.4f}")

    # Now with color Wilson line
    print("\n\n--- Including SU(3) color Wilson line ---")
    print("  Color phases at Z₃ fixed points: 0, 2π/3, 4π/3")

    omega = np.exp(2j * np.pi / 3)
    color_phases = [0, 2*np.pi/3, 4*np.pi/3]

    for fermion_name, Y_L, Y_R in [
        ("up quark", Y_Q_L, Y_u_R),
        ("down quark", Y_Q_L, Y_d_R),
    ]:
        print(f"\n  {fermion_name}:")

        # 3 generations × 3 colors = 9 states
        # But physically, color is summed over (confined)
        # The effective mass for generation k is the color-averaged overlap

        for k in range(3):
            color_masses = []
            for c, phi_c in enumerate(color_phases):
                # Total shift: hypercharge Wilson + color Wilson
                xi_L_c = Y_L * v_wilson + phi_c / (2*np.pi)
                xi_R_c = Y_R * v_wilson + phi_c / (2*np.pi)

                evals_L, psi_L, theta = solve_z3_sector(alpha, xi_L_c, k, n_states=1)
                evals_R, psi_R, _ = solve_z3_sector(alpha, xi_R_c, k, n_states=1)

                overlap = np.abs(compute_overlap(psi_L[0], psi_R[0], theta))
                color_masses.append(overlap)

            avg_mass = np.mean(color_masses)
            print(f"    Gen {k}: color masses = [{color_masses[0]:.6f}, "
                  f"{color_masses[1]:.6f}, {color_masses[2]:.6f}], "
                  f"avg = {avg_mass:.6f}")

    return


# ============================================================
# PART 5: Effective potential approach — what actually works
# ============================================================

def effective_mass_splitting(alpha_eff):
    """
    The correct approach to generation splitting:

    On S¹/Z₃, the three FIXED POINTS are at θ = 0, 2π/3, 4π/3.
    Fermions localized at each fixed point form one generation.

    The Z₃ symmetry is broken by:
    1. The SU(3) color Wilson line (Hosotani mechanism)
    2. The U(1)_Y Wilson line
    3. The Higgs VEV profile on S¹

    The key insight: the Wilson line ⟨A₅⟩ for SU(2)_L is the Higgs
    mechanism in 5D. The Higgs VEV v = ⟨A₅⟩ × (2πR) gives:

      ξ = Y × v / (2πR × M_KK) = Y × v × L / (2π)

    For v·L = 3 (Z₃ quantization):
      ξ = Y × 3 / (2π) = Y × 0.477
    """
    print("\n" + "="*70)
    print("EFFECTIVE MASS SPLITTING FROM WILSON LINE")
    print("="*70)

    # v·L = 3 quantization gives ξ = Y × 3/(2π)
    v_L = 3.0  # Z₃ quantization condition

    print(f"\nUsing v·L = {v_L} (Z₃ quantization)")
    print(f"Wilson line parameter: ξ = Y × {v_L/(2*np.pi):.4f}")

    # Effective Wilson line shifts for each SM fermion
    fermions = {
        'u_L': (Y_Q_L, v_L/(2*np.pi)),
        'u_R': (Y_u_R, v_L/(2*np.pi)),
        'd_L': (Y_Q_L, v_L/(2*np.pi)),
        'd_R': (Y_d_R, v_L/(2*np.pi)),
        'e_L': (Y_L_L, v_L/(2*np.pi)),
        'e_R': (Y_e_R, v_L/(2*np.pi)),
    }

    print(f"\nWilson line shifts ξ = Y × {v_L/(2*np.pi):.4f}:")
    for name, (Y, scale) in fermions.items():
        xi = Y * scale
        print(f"  {name}: Y = {Y:+.3f}, ξ = {xi:+.4f}")

    # Now solve for each fermion type in each Z₃ sector
    print(f"\nSolving Mathieu equation at α_eff = {alpha_eff:.3f}")
    print("-"*70)

    results = {}

    for fermion_type, (Y_left, Y_right, label) in {
        'up': (Y_Q_L, Y_u_R, 'Up-type quarks'),
        'down': (Y_Q_L, Y_d_R, 'Down-type quarks'),
        'lepton': (Y_L_L, Y_e_R, 'Charged leptons'),
    }.items():
        xi_L = Y_left * v_L / (2*np.pi)
        xi_R = Y_right * v_L / (2*np.pi)

        print(f"\n{label}: ξ_L = {xi_L:.4f}, ξ_R = {xi_R:.4f}")

        sector_masses = []
        for k in range(3):
            # Solve in each Z₃ sector
            evals_L, psi_L, theta = solve_z3_sector(alpha_eff, xi_L, k, n_states=1)
            evals_R, psi_R, _ = solve_z3_sector(alpha_eff, xi_R, k, n_states=1)

            # Effective Yukawa: overlap of L and R wavefunctions
            overlap = compute_overlap(psi_L[0], psi_R[0], theta)
            mass_proxy = np.abs(overlap)

            # Energy difference between sectors (contributes to mass via KK mixing)
            E_avg = (evals_L[0] + evals_R[0]) / 2

            sector_masses.append({
                'k': k,
                'E_L': evals_L[0],
                'E_R': evals_R[0],
                'overlap': overlap,
                'mass': mass_proxy,
            })

            print(f"  k={k}: E_L={evals_L[0]:.6f}, E_R={evals_R[0]:.6f}, "
                  f"|Y|={mass_proxy:.6f}, phase={np.angle(overlap)*180/np.pi:.2f}°")

        masses = np.array([s['mass'] for s in sector_masses])
        if np.max(masses) > 1e-10:
            # Sort by mass (heaviest = 3rd gen)
            idx = np.argsort(masses)[::-1]
            m3, m2, m1 = masses[idx[0]], masses[idx[1]], masses[idx[2]]

            print(f"\n  Sorted masses: m₃={m3:.6f}, m₂={m2:.6f}, m₁={m1:.6f}")
            if m1 > 1e-15:
                print(f"  Ratios: m₃/m₂ = {m3/m2:.4f}, m₂/m₁ = {m2/m1:.4f}, m₃/m₁ = {m3/m1:.4f}")
            else:
                print(f"  Ratios: m₃/m₂ = {m3/m2:.4f}, m₁ ≈ 0")

            results[fermion_type] = {
                'masses': masses[idx],
                'sectors': [sector_masses[i] for i in idx]
            }
        else:
            print("  All overlaps near zero — check parameters")

    return results


# ============================================================
# PART 6: Scan Wilson line strength
# ============================================================

def scan_wilson_strength():
    """
    Scan the Wilson line strength to find what gives realistic mass ratios.

    We need:
      m_b/m_s ≈ 53     (3rd/2nd gen down quarks)
      m_t/m_c ≈ 277    (3rd/2nd gen up quarks)
      m_τ/m_μ ≈ 16.8   (3rd/2nd gen leptons)
      m_s/m_d ≈ 20     (2nd/1st gen down quarks)
      m_c/m_u ≈ 590    (2nd/1st gen up quarks)
      m_μ/m_e ≈ 207    (2nd/1st gen leptons)
    """
    print("\n" + "="*70)
    print("SCANNING WILSON LINE STRENGTH")
    print("="*70)

    alpha_eff = 1.480  # computed value

    # The Wilson line on S¹/Z₃ is quantized: v_W = n/(3R) for integer n
    # But the Hosotani VEV can take continuous values within each topological sector

    # Try different effective v·L values
    for v_L in [0.5, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 9.0]:
        print(f"\n{'='*50}")
        print(f"  v·L = {v_L}")
        print(f"{'='*50}")

        for fermion_type, Y_left, Y_right, label in [
            ('up', Y_Q_L, Y_u_R, 'Up quarks'),
            ('down', Y_Q_L, Y_d_R, 'Down quarks'),
            ('lepton', Y_L_L, Y_e_R, 'Leptons'),
        ]:
            xi_L = Y_left * v_L / (2*np.pi)
            xi_R = Y_right * v_L / (2*np.pi)

            masses = []
            for k in range(3):
                evals_L, psi_L, theta = solve_z3_sector(alpha_eff, xi_L, k, n_states=1)
                evals_R, psi_R, _ = solve_z3_sector(alpha_eff, xi_R, k, n_states=1)
                overlap = np.abs(compute_overlap(psi_L[0], psi_R[0], theta))
                masses.append(overlap)

            masses = np.sort(masses)[::-1]
            if masses[-1] > 1e-15:
                r32 = masses[0]/masses[1]
                r21 = masses[1]/masses[2]
                print(f"  {label:12s}: m₃/m₂ = {r32:8.3f}, m₂/m₁ = {r21:8.3f}")
            else:
                print(f"  {label:12s}: m₃/m₂ = {masses[0]/max(masses[1],1e-20):8.3f}, m₁ ≈ 0")


# ============================================================
# PART 7: The actual physical mechanism — intergeneration mixing
# ============================================================

def intergeneration_yukawa(alpha_eff):
    """
    The REAL mass hierarchy comes from the YUKAWA MATRIX structure.

    On S¹/Z₃, the three generations have wavefunctions ψ_k(θ) centered
    at θ_k = 2πk/3. The Yukawa coupling to the Higgs is:

      Y_{ij} = g₅ ∫ dθ ψ_Li(θ) H(θ) ψ_Rj(θ)

    If the Higgs is localized at θ = 0 (the k=0 fixed point), then:
      Y_{00} ~ 1 (3rd generation, at the Higgs location)
      Y_{11} ~ exp(-κ²/4) (2nd generation, one step away)
      Y_{22} ~ exp(-κ²/4) (1st generation, one step away)
      Y_{01} ~ exp(-κ²/16) (off-diagonal)

    THIS is why 2nd and 1st gen are degenerate! They're both one
    step away from the Higgs.

    To BREAK this degeneracy, we need the Higgs to NOT be at a fixed point,
    or we need the two non-Higgs fixed points to be distinguishable.

    The Wilson line does this: with ξ ≠ 0, the wavefunctions at the
    three fixed points are SHIFTED by different amounts:
      θ_0 → θ_0 + δ₀
      θ_1 → θ_1 + δ₁
      θ_2 → θ_2 + δ₂

    where δ_k depends on the Wilson line phase at fixed point k.
    """
    print("\n" + "="*70)
    print("YUKAWA MATRIX WITH LOCALIZED HIGGS")
    print("="*70)

    # Solve for the three generation wavefunctions
    # The Higgs is localized at θ = 0

    # Step 1: Get wavefunctions localized at each fixed point
    evals, psi, theta = solve_mathieu_wilson(alpha_eff, 0.0, n_states=1)
    psi_0 = psi[0]  # Ground state centered at θ = 0

    # Wavefunctions at other fixed points: shift by 2π/3, 4π/3
    shift_1 = int(round(N_THETA / 3))
    shift_2 = int(round(2 * N_THETA / 3))

    psi_1 = np.roll(psi_0, shift_1)  # Centered at 2π/3
    psi_2 = np.roll(psi_0, shift_2)  # Centered at 4π/3

    # Higgs profile: localized at θ = 0
    sigma_H = 0.862  # Same localization as fermions (at α_eff = 1.480)
    H_profile = np.exp(-(theta - np.pi)**2 / (2 * sigma_H**2))
    # Actually, need to be careful with periodicity
    # Use the periodic Gaussian
    H_profile = np.zeros(N_THETA)
    for n_wrap in range(-2, 3):
        H_profile += np.exp(-(theta + 2*np.pi*n_wrap)**2 / (2 * sigma_H**2))
    H_norm = np.sqrt(np.trapezoid(H_profile**2, theta))
    H_profile /= H_norm

    # Compute Yukawa matrix
    gen_psi = [psi_0, psi_1, psi_2]

    print(f"\nα_eff = {alpha_eff:.3f}, σ = {sigma_H:.3f} rad")
    print(f"Higgs localized at θ = 0\n")

    Y = np.zeros((3, 3), dtype=complex)
    for i in range(3):
        for j in range(3):
            Y[i, j] = np.trapezoid(np.conj(gen_psi[i]) * H_profile * gen_psi[j], theta)

    print("Yukawa matrix |Y_{ij}|:")
    for i in range(3):
        row = "  "
        for j in range(3):
            row += f"{np.abs(Y[i,j]):10.6f} "
        print(row)

    # Diagonalize Y†Y to get mass eigenvalues
    YdY = np.conj(Y.T) @ Y
    eigenvalues = np.sort(np.real(np.linalg.eigvalsh(YdY)))[::-1]
    mass_eigenvalues = np.sqrt(np.maximum(eigenvalues, 0))

    print(f"\nMass eigenvalues (√(Y†Y)): {mass_eigenvalues}")
    if mass_eigenvalues[-1] > 1e-15:
        print(f"Ratios: m₃/m₂ = {mass_eigenvalues[0]/mass_eigenvalues[1]:.4f}, "
              f"m₂/m₁ = {mass_eigenvalues[1]/mass_eigenvalues[2]:.4f}")

    # Now with Wilson line: shift each generation differently
    print("\n--- With Wilson line (v·L = 3) ---")

    v_L = 3.0
    # The Wilson line shifts each FERMION differently based on hypercharge
    # For up-type quarks:
    for fermion_type, Y_left, Y_right, label in [
        ('up', Y_Q_L, Y_u_R, 'Up quarks'),
        ('down', Y_Q_L, Y_d_R, 'Down quarks'),
        ('lepton', Y_L_L, Y_e_R, 'Leptons'),
    ]:
        xi_L = Y_left * v_L / (2*np.pi)
        xi_R = Y_right * v_L / (2*np.pi)
        delta_xi = xi_L - xi_R  # The relevant Wilson line difference

        print(f"\n  {label}: Δξ = ξ_L - ξ_R = {delta_xi:.4f}")

        # The Wilson line phase at each fixed point modifies the Yukawa:
        # Y_{ij}^{Wilson} = Y_{ij} × exp(i·Δξ·(θ_i + θ_j)/2)
        # This is an approximation; let's do it properly.

        # Get LEFT and RIGHT wavefunctions with Wilson line
        evals_L, psi_L_0, _ = solve_mathieu_wilson(alpha_eff, xi_L, n_states=1)
        evals_R, psi_R_0, _ = solve_mathieu_wilson(alpha_eff, xi_R, n_states=1)

        # Shift to three fixed points
        psi_L = [psi_L_0[0], np.roll(psi_L_0[0], shift_1), np.roll(psi_L_0[0], shift_2)]
        psi_R = [psi_R_0[0], np.roll(psi_R_0[0], shift_1), np.roll(psi_R_0[0], shift_2)]

        # Yukawa matrix with Higgs at θ = 0
        Y_mat = np.zeros((3, 3), dtype=complex)
        for i in range(3):
            for j in range(3):
                Y_mat[i, j] = np.trapezoid(np.conj(psi_L[i]) * H_profile * psi_R[j], theta)

        # Diagonalize
        YdY = np.conj(Y_mat.T) @ Y_mat
        eigenvalues = np.sort(np.real(np.linalg.eigvalsh(YdY)))[::-1]
        mass_ev = np.sqrt(np.maximum(eigenvalues, 0))

        print(f"  Mass eigenvalues: {mass_ev}")
        if mass_ev[1] > 1e-15:
            print(f"  m₃/m₂ = {mass_ev[0]/mass_ev[1]:.2f}, ", end="")
        if mass_ev[2] > 1e-15:
            print(f"m₂/m₁ = {mass_ev[1]/mass_ev[2]:.4f}")
        else:
            print(f"m₁ ≈ 0")

    return


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    alpha_eff = 1.480  # From rigorous calculation

    print("="*70)
    print("GENERATION SPLITTING FROM HOSOTANI MECHANISM ON S¹/Z₃")
    print("="*70)
    print(f"\nInput: α_eff = {alpha_eff}")
    print(f"Observed mass ratios needed:")
    print(f"  Up quarks:   m_t/m_c ≈ 136,  m_c/m_u ≈ 590")
    print(f"  Down quarks: m_b/m_s ≈ 45,   m_s/m_d ≈ 20")
    print(f"  Leptons:     m_τ/m_μ ≈ 16.8, m_μ/m_e ≈ 207")

    # Part 5: Effective mass splitting
    results = effective_mass_splitting(alpha_eff)

    # Part 6: Scan Wilson line
    scan_wilson_strength()

    # Part 7: Yukawa matrix with localized Higgs
    intergeneration_yukawa(alpha_eff)

    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    print("""
The computation above tests whether the Hosotani mechanism (Wilson line
VEV on S¹/Z₃) can produce realistic fermion mass hierarchies.

Key questions answered:
1. Does the Wilson line break Z₃ degeneracy between generations?
2. Does it produce realistic mass ratios?
3. Does the up-down splitting emerge?
""")
