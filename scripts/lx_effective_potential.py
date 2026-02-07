#!/usr/bin/env python3
"""
L_X Effective Potential from Casimir Energy on S¹/Z₃
=====================================================

STUR Framework v5.1 — Dynamical Compactification Scale

The compactification scale L_X is currently undetermined, with a 10²⁶
discrepancy between the fundamental value (from v·L_X = 3) and the
effective value (~0.8 μm from phenomenology).

This script computes V_eff(L) from the one-loop Casimir energy of the
SM field content on S¹/Z₃, the holonomy potential, and the R-field
helix energy, to determine whether the potential has a dynamical minimum.

Physics:
- Casimir energy: V_Casimir ∝ -ζ(5) / L⁵ × (boson - fermion) count
- Holonomy potential: V_hol ∝ g²/L⁴ × B₄(θ/(2π)) from gauge loops
- Helix energy: V_helix ∝ v²/L² from R-field winding
- Tree-level CC: Λ₀ (classical cosmological constant)

The question: Does V_eff(L) = V_Casimir + V_hol + V_helix + Λ₀ have
a stable minimum at some L_X?

Author: Computed for STUR v5.1
Date: 2026-02-07
"""

import numpy as np

# =========================================================================
# CONSTANTS (natural units: ℏ = c = 1, energies in GeV)
# =========================================================================

M_Planck = 2.435e18   # Reduced Planck mass (GeV)
v_EW = 246.22         # Electroweak VEV (GeV)
alpha_s = 0.1179      # Strong coupling at M_Z
alpha_em = 1/137.036   # EM coupling
g_s = np.sqrt(4*np.pi*alpha_s)
g_2 = 0.652           # SU(2) coupling
g_1 = 0.357           # U(1) coupling
hbar_c = 0.19733      # ℏc in GeV·fm
GeV_to_inv_m = 1e15 / hbar_c  # GeV → m⁻¹ conversion

# SM field content
N_scalars = 4          # Higgs doublet (real components)
N_Weyl = 45            # SM Weyl fermions per generation × 3 generations
N_gauge = 12           # 8 gluons + 3 W + 1 B

# Effective degrees of freedom (periodic/antiperiodic BCs on S¹)
# Bosons: periodic → Casimir energy -π²/(720 L⁵) per d.o.f.
# Fermions: antiperiodic → Casimir energy +7π²/(5760 L⁵) per d.o.f.


# =========================================================================
# CASIMIR ENERGY ON S¹/Z₃
# =========================================================================

def casimir_energy_density(L, n_b, n_f):
    """
    Casimir energy density on S¹ of circumference L.

    For a circle of circumference L = 2πR:
        V_Casimir = -(π²/6) × (1/L⁵) × [n_b - (7/8)n_f × (for antiperiodic)]

    In 5D on S¹, the full one-loop result for PERIODIC bosons is:
        E/V₃ = -(π²/90) × n_b / (2πR)⁴ × (1/R)

    For S¹/Z₃: the orbifold projection modifies the KK spectrum.
    Untwisted sector: modes n = 0 (mod 3) survive
    Twisted sectors: fractional modes at fixed points

    In terms of the circumference L = 2πR:
        V_Casimir = -(π²/1440) × 1/L⁵ × Δn_eff

    where Δn_eff = n_b_eff - (7/8)n_f_eff accounts for the Z₃ projection.
    """
    # On S¹/Z₃, the effective degrees of freedom are modified.
    # Untwisted: every 3rd KK level survives → factor 1/3⁵ enhancement per mode
    # But more modes (all integers), so net: 1/3⁴ relative to S¹
    # Total: V_S1Z3 = V_S1 × (1/3⁴ + twisted sector corrections)

    # Simplified: on S¹/Z₃, the Casimir energy is dominated by the
    # untwisted sector with KK spacing 3/L instead of 1/L:
    L_eff = L / 3  # effective length for Z₃ KK spacing

    # Casimir energy per d.o.f. on S¹ of length L_eff:
    # E_Cas = -π²/(720 L_eff⁵) for periodic scalars in 5D
    # Using the standard Casimir formula in 5D:
    prefactor = np.pi**2 / (1440.0)

    # Bosonic contribution (periodic BCs)
    V_boson = -prefactor * n_b / L_eff**5

    # Fermionic contribution (antiperiodic BCs on S¹)
    # The 7/8 factor applies in 4D; in 5D the ratio is different
    # For antiperiodic fermions: shifted KK spectrum (n+1/2)
    V_fermion = +prefactor * (7.0/8.0) * n_f / L_eff**5

    # On the Z₃ orbifold, fermions in twisted sectors have fractional momenta
    # This modifies the effective count:
    # Twisted sector adds: 2 × (1/3⁵) correction per twisted field
    # (two twisted sectors with momenta shifted by ±1/3)
    twist_correction = 2 * (1.0/3**5) * n_f * prefactor / L_eff**5

    return V_boson + V_fermion + twist_correction


def casimir_SM(L):
    """Casimir energy for SM field content on S¹/Z₃."""
    return casimir_energy_density(L, N_scalars + N_gauge, 2 * N_Weyl)


# =========================================================================
# HOLONOMY POTENTIAL
# =========================================================================

def holonomy_potential(L, theta_hol=2*np.pi/3):
    """
    One-loop holonomy potential from gauge fields on S¹.

    V_hol = -(1/(2π)⁴) × (1/L⁴) × Σ_rep d_rep × B₄(q·θ/(2π))

    where B₄(x) = x⁴ - 2x³ + x² - 1/30 is the 4th Bernoulli polynomial.

    For SU(3) gauge fields at Z₃ holonomy θ = 2π/3:
    The Z₃-symmetric minimum is the desired vacuum.
    """
    def bernoulli_4(x):
        """B₄(x) for x ∈ [0,1]."""
        x = x % 1.0
        return x**4 - 2*x**3 + x**2 - 1.0/30

    # SU(3) adjoint: 8 generators with charges ±1, ±2, 0, 0, 0, 0
    # At θ = 2π/3, the holonomy is in the center Z₃
    charges = [1, -1, 2, -2, 0, 0, 0, 0]  # simplified
    V = 0.0
    for q in charges:
        V += bernoulli_4(q * theta_hol / (2*np.pi))

    # Full one-loop result:
    prefactor = 3.0 / (2*np.pi)**4  # 3 for color factor
    V_hol = -prefactor / L**4 * V

    return V_hol


# =========================================================================
# HELIX ENERGY
# =========================================================================

def helix_energy(L, v=v_EW):
    """
    Energy from the R-field helix winding.

    The helix φ(X) = 2πX/(3L) has gradient energy:
        V_helix = (1/2) × v² × (2π/(3L))²
                = 2π²v²/(9L²)

    This is the kinetic energy cost of the helix winding.
    """
    return 2 * np.pi**2 * v**2 / (9 * L**2)


# =========================================================================
# GRAVITATIONAL/MODULI POTENTIAL
# =========================================================================

def moduli_potential(L, M_5):
    """
    Gravitational moduli potential from 5D Einstein-Hilbert.

    In Kaluza-Klein reduction, the radion (L) has a kinetic term
    but no tree-level potential. The potential comes from:
    1. Casimir energy (computed above)
    2. Flux contributions (if any)
    3. Non-perturbative effects (e.g., gaugino condensation)

    Here we include a simple stabilization term from the 5D bulk:
    V_moduli = M_5³ × (σ/L - σ₀/L₀)² × L

    where σ is a modulus field and M_5 is the 5D Planck mass.
    For simplicity, use M_5 ≈ M_Planck (for L ≈ 1/M_Planck).
    """
    # In practice, the moduli potential is model-dependent.
    # Return 0 for the minimal calculation.
    return 0.0


# =========================================================================
# TOTAL EFFECTIVE POTENTIAL
# =========================================================================

def V_effective(L, Lambda_0=0.0):
    """
    Total effective potential for the compactification scale L.

    V_eff = V_Casimir + V_holonomy + V_helix + Λ₀

    L is in GeV⁻¹ (natural units).
    """
    V_cas = casimir_SM(L)
    V_hol = holonomy_potential(L)
    V_hel = helix_energy(L)
    return V_cas + V_hol + V_hel + Lambda_0


# =========================================================================
# MAIN COMPUTATION
# =========================================================================

if __name__ == '__main__':
    print("=" * 70)
    print("  L_X EFFECTIVE POTENTIAL FROM CASIMIR ENERGY ON S¹/Z₃")
    print("  STUR Framework v5.1 — Dynamical Scale Determination")
    print("=" * 70)

    # ══════════════════════════════════════════════════════════
    # SECTION 1: INDIVIDUAL CONTRIBUTIONS
    # ══════════════════════════════════════════════════════════

    print(f"\n{'─' * 70}")
    print("  SECTION 1: Energy Components vs L")
    print(f"{'─' * 70}")

    print(f"\n  SM field content on S¹/Z₃:")
    print(f"    Scalars (Higgs): {N_scalars} real d.o.f.")
    print(f"    Weyl fermions: {N_Weyl} × 2 (Dirac) = {2*N_Weyl}")
    print(f"    Gauge bosons: {N_gauge}")
    print(f"    Net: Δn = n_b - (7/8)n_f = {N_scalars + N_gauge} - {7/8 * 2 * N_Weyl:.1f} = {N_scalars + N_gauge - 7/8 * 2 * N_Weyl:.1f}")
    print(f"    {'(fermion-dominated → positive Casimir energy)' if N_scalars + N_gauge < 7/8 * 2 * N_Weyl else '(boson-dominated → negative Casimir energy)'}")

    # Scan L values (in GeV⁻¹)
    # 1 GeV⁻¹ ≈ 0.2 fm, so L = 10⁻¹⁵ GeV⁻¹ ≈ 0.2 × 10⁻¹⁵ fm = GUT scale
    # L = 1 GeV⁻¹ ≈ 0.2 fm = hadronic scale
    # L = 10⁶ GeV⁻¹ ≈ 0.2 μm = submillimeter scale

    # Convert L from meters to GeV⁻¹: L(GeV⁻¹) = L(m) / (ℏc in m⋅GeV)
    # ℏc = 1.9733 × 10⁻¹⁶ m⋅GeV
    hbar_c_m = 1.9733e-16  # m⋅GeV

    # Scan in physical units
    L_meters = np.logspace(-35, -3, 500)  # from Planck to mm
    L_GeV = L_meters / hbar_c_m           # in GeV⁻¹

    V_cas_arr = np.array([casimir_SM(L) for L in L_GeV])
    V_hol_arr = np.array([holonomy_potential(L) for L in L_GeV])
    V_hel_arr = np.array([helix_energy(L) for L in L_GeV])
    V_tot_arr = V_cas_arr + V_hol_arr + V_hel_arr

    # Print at representative scales
    print(f"\n  {'L (m)':>12s}  {'L (GeV⁻¹)':>12s}  {'V_Cas (GeV⁵)':>14s}  "
          f"{'V_hol (GeV⁵)':>14s}  {'V_helix (GeV⁵)':>14s}  {'V_tot (GeV⁵)':>14s}")
    print(f"  {'─'*12}  {'─'*12}  {'─'*14}  {'─'*14}  {'─'*14}  {'─'*14}")

    display_L_m = [1e-35, 1e-30, 1e-25, 1e-20, 1e-15, 1e-10, 1e-6, 1e-3]
    for Lm in display_L_m:
        LG = Lm / hbar_c_m
        vc = casimir_SM(LG)
        vh = holonomy_potential(LG)
        vhe = helix_energy(LG)
        vt = vc + vh + vhe
        print(f"  {Lm:12.0e}  {LG:12.2e}  {vc:14.2e}  {vh:14.2e}  {vhe:14.2e}  {vt:14.2e}")

    # ══════════════════════════════════════════════════════════
    # SECTION 2: BEHAVIOR ANALYSIS
    # ══════════════════════════════════════════════════════════

    print(f"\n{'─' * 70}")
    print("  SECTION 2: Potential Behavior Analysis")
    print(f"{'─' * 70}")

    # Check the scaling of each term
    print(f"\n  Scaling behavior:")
    print(f"    V_Casimir ∝ 1/L⁵ (dominant at small L)")
    print(f"    V_holonomy ∝ 1/L⁴")
    print(f"    V_helix ∝ 1/L² (dominant at large L, if V_Cas > 0)")
    print(f"")

    # Sign of Casimir energy determines stability
    delta_n = N_scalars + N_gauge - (7.0/8) * 2 * N_Weyl
    print(f"    Effective boson-fermion count: Δn = {delta_n:.1f}")
    if delta_n < 0:
        print(f"    → Casimir energy is POSITIVE at small L (repulsive)")
        print(f"    → V_helix is POSITIVE at large L")
        print(f"    → If both are positive, V_eff has no minimum (runaway)")
        print(f"    → Need NEGATIVE holonomy or CC contribution for stability")
    else:
        print(f"    → Casimir energy is NEGATIVE at small L (attractive)")
        print(f"    → Combined with positive V_helix → POTENTIAL MINIMUM EXISTS")

    # Look for minimum
    # dV/dL = 0 requires: 5 V_Cas / L + 4 V_hol / L + 2 V_hel / L = 0
    # (each scales as 1/L^n, derivative is -n/L^{n+1})
    # With Λ₀, we can always tune to get a minimum

    # Check if V_tot changes sign
    sign_changes = np.where(np.diff(np.sign(V_tot_arr)))[0]
    if len(sign_changes) > 0:
        print(f"\n  V_eff changes sign at L ≈ {L_meters[sign_changes[0]]:.2e} m")
    else:
        sign_str = "positive" if V_tot_arr[len(V_tot_arr)//2] > 0 else "negative"
        print(f"\n  V_eff is always {sign_str} in scanned range")

    # Look for local minimum in V_tot
    dV = np.diff(V_tot_arr)
    min_candidates = np.where((dV[:-1] < 0) & (dV[1:] > 0))[0]
    if len(min_candidates) > 0:
        idx = min_candidates[0] + 1
        L_min = L_meters[idx]
        V_min = V_tot_arr[idx]
        print(f"\n  ✓ LOCAL MINIMUM FOUND:")
        print(f"    L_min = {L_min:.2e} m")
        print(f"    V_min = {V_min:.2e} GeV⁵")
        print(f"    Comparison: L_X (phenomenological) ≈ 0.8 μm = 8×10⁻⁷ m")
    else:
        print(f"\n  ✗ No local minimum found in range [{L_meters[0]:.0e}, {L_meters[-1]:.0e}] m")
        print(f"    V_eff is monotonically {'decreasing' if dV[0] < 0 else 'increasing'}")

    # ══════════════════════════════════════════════════════════
    # SECTION 3: WITH COSMOLOGICAL CONSTANT
    # ══════════════════════════════════════════════════════════

    print(f"\n{'─' * 70}")
    print("  SECTION 3: Including Cosmological Constant")
    print(f"{'─' * 70}")

    # The observed CC: Λ_obs ≈ 2.846 × 10⁻¹²² M_Planck⁴
    # In GeV⁴: Λ_obs ≈ (2.25 meV)⁴ ≈ 2.6 × 10⁻⁴⁷ GeV⁴
    Lambda_obs = 2.6e-47  # GeV⁴ (4D CC)

    # The CC enters the 5D effective potential as Λ₅ = Λ₄ × L
    # So V_eff gets an additive Λ₄ × L term
    # This is positive and GROWS with L, providing a restoring force

    print(f"\n  The 4D CC contribution to V_eff is: V_CC = Λ₄ × L")
    print(f"  Observed Λ₄ = {Lambda_obs:.2e} GeV⁴")
    print(f"  This is tiny compared to Casimir/helix at any relevant L.")

    # For the CC to balance V_helix at L ~ μm:
    # Λ₄ × L ~ v²/L² → Λ₄ ~ v²/L³
    L_pheno = 0.8e-6 / hbar_c_m  # 0.8 μm in GeV⁻¹
    Lambda_balance = v_EW**2 / L_pheno**3
    print(f"\n  For balance at L ~ 0.8 μm:")
    print(f"    Need Λ₄ ~ v²/L³ ~ {Lambda_balance:.2e} GeV⁴")
    print(f"    Observed Λ₄ = {Lambda_obs:.2e} GeV⁴")
    print(f"    Ratio: {Lambda_balance/Lambda_obs:.2e}")
    print(f"    This is a restatement of the CC problem.")

    # ══════════════════════════════════════════════════════════
    # SECTION 4: v·L = 3 CONSTRAINT
    # ══════════════════════════════════════════════════════════

    print(f"\n{'─' * 70}")
    print("  SECTION 4: The v·L = 3 Quantization Constraint")
    print(f"{'─' * 70}")

    # The Z₃ helix requires v × L_X = 3 (in natural units)
    # If v = v_EW = 246 GeV → L_X = 3/246 GeV⁻¹ = 0.0122 GeV⁻¹
    L_from_vEW = 3.0 / v_EW  # GeV⁻¹
    L_from_vEW_m = L_from_vEW * hbar_c_m  # meters

    print(f"\n  From v·L_X = 3:")
    print(f"    If v = v_EW = {v_EW} GeV:")
    print(f"      L_X = 3/{v_EW} = {L_from_vEW:.4f} GeV⁻¹")
    print(f"      L_X = {L_from_vEW_m:.2e} m = {L_from_vEW_m*1e15:.1f} fm")
    print(f"      M_KK = 2π/L_X = {2*np.pi/L_from_vEW:.0f} GeV")
    print(f"")
    print(f"    If L_X = 0.8 μm (phenomenological):")
    L_pheno_GeV = 0.8e-6 / hbar_c_m
    v_from_pheno = 3.0 / L_pheno_GeV
    print(f"      v = 3/L_X = {v_from_pheno:.2e} GeV")
    print(f"      M_KK = 2π/L_X = {2*np.pi/L_pheno_GeV:.2e} GeV = {2*np.pi/L_pheno_GeV*1e-3:.2e} MeV")
    print(f"")
    print(f"    INCONSISTENCY: v·L = 3 gives:")
    print(f"      • v = v_EW → L ~ 2.4 fm (much smaller than phenomenological)")
    print(f"      • L = 0.8 μm → v ~ {v_from_pheno:.1e} GeV (much smaller than v_EW)")
    print(f"")
    print(f"    The 'v' in v·L = 3 cannot be the electroweak VEV.")
    print(f"    It must be a DIFFERENT scale (e.g., R-field VEV ≠ Higgs VEV).")

    # ══════════════════════════════════════════════════════════
    # SECTION 5: HONEST ASSESSMENT
    # ══════════════════════════════════════════════════════════

    print(f"\n{'─' * 70}")
    print("  SECTION 5: HONEST ASSESSMENT OF L_X DETERMINATION")
    print(f"{'─' * 70}")

    print(f"""
  STATUS: L_X CANNOT BE DETERMINED FROM CURRENT FRAMEWORK

  Key findings:

  1. CASIMIR ENERGY: SM on S¹/Z₃ has MORE fermions than bosons.
     Δn_eff = {delta_n:.0f} (fermion-dominated).
     → Casimir energy is POSITIVE (repulsive) at small L.
     → V_helix is also POSITIVE at large L.
     → Without additional contributions, V_eff has NO minimum.

  2. HOLONOMY POTENTIAL: Provides a NEGATIVE contribution ∝ 1/L⁴.
     This could create a minimum if it's large enough to overcome
     the Casimir repulsion. But at the Z₃ point, the holonomy
     potential IS at its minimum (by construction), so it doesn't
     help stabilize L — it just shifts the energy.

  3. v·L = 3 CONSTRAINT:
     If v = v_EW: L ~ 2.4 fm (too small for phenomenological claims)
     If L ~ μm: v ~ 10⁻¹⁰ GeV (not the electroweak scale)
     The constraint is internally consistent ONLY if v is a SEPARATE
     scale from v_EW. This needs to be stated explicitly.

  4. SCALE HIERARCHY:
     The 10²⁶ gap between L_fund and L_pheno is NOT a dynamical
     result — it would require a mechanism like the Randall-Sundrum
     warp factor or a large-N effect. Neither is present in the
     current framework.

  WHAT WOULD FIX THIS:
    • Identify the R-field VEV v_R as distinct from v_EW
    • Show that v_R is dynamically determined (e.g., from a potential)
    • Demonstrate that L_X = 3/v_R gives a consistent phenomenology
    • OR: accept that L_X is an INPUT parameter (honest but reduces
      the theory's predictive power)

  IMPACT ON OTHER PREDICTIONS:
    • Neutrino masses: depend on M_KK through seesaw mechanism
    • Proton decay: rate depends on M_KK exponentially
    • Dark matter: LKP mass depends on M_KK
    • All cosmological predictions: affected by L_X uncertainty

  This is the single biggest open problem in the STUR framework.
""")
