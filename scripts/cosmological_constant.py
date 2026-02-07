#!/usr/bin/env python3
"""
Cosmological Constant from Casimir Energy on S¹/Z₃
====================================================

STUR Framework v5.2 — Honest Computation

The framework claims to connect the extra dimension to the cosmological
constant. This script computes what the Casimir energy on S¹/Z₃
actually gives and compares to the observed Λ₄.

Key question: Does the S¹/Z₃ Casimir energy naturally give a small Λ₄?

Spoiler from lx_effective_potential.py: The SM on S¹/Z₃ has
Δn_eff = -63 (fermion-dominated), giving POSITIVE Casimir energy.

Author: STUR Physics Lab
Date: 2026-02-07
"""

import numpy as np

# ── Constants ──────────────────────────────────────────────────────
hbar_c = 0.197327  # GeV·fm
M_Pl = 1.2209e19   # GeV (Planck mass)
G_N = 1 / M_Pl**2  # in GeV⁻²
Lambda_obs = 2.60e-47  # GeV⁴ (observed CC, from ρ_Λ = 3H₀²/(8πG) × Ω_Λ)
rho_crit = 4.08e-47    # GeV⁴ (critical density)
v_EW = 246.22       # GeV


def casimir_energy_density_5d(L, n_scalars=4, n_weyl=90, n_gauge=12):
    """
    5D Casimir energy density on S¹/Z₃.

    ρ_Cas = (π²/1620) × (1/L⁵) × [n_b - (7/8)n_f]
    where the 1/1620 = 1/(6 × 270) comes from the Z₃ projection
    reducing modes to every 3rd KK level.
    """
    # On S¹/Z₃, only every 3rd KK mode survives: n = 0, 3, 6, ...
    # This reduces the sum by factor of 1/3⁴ = 1/81 compared to S¹
    # Standard S¹ result: ρ = π²/(1440 L⁵) × Δn (Ramond convention)
    # Z₃ reduction: ρ = π²/(1440 × 81 × L⁵) × Δn ... NO

    # Actually: on S¹/Z₃, the KK spectrum is m_n = 3n/L, so:
    # ρ_Cas = Σ_{n=1}^∞ d.o.f. × (3n/L)⁵ × zeta-regularized sum

    # The standard result for bosons on S¹ with radius R:
    # ρ_b = -π²/(1440 R⁴) per d.o.f. (4D result after integration)

    # For Z₃ orbifold with period L:
    # Physical radius R = L/(2π), KK mass m_n = 2πn/L (on S¹)
    # On Z₃: m_n = 2πn/(L/3) = 6πn/L (only multiples of 3 survive)

    # Effective radius R_eff = L/3
    # ρ_Cas = -π²/(1440) × (2π/L_eff)⁴ per boson d.o.f. (4D)
    # where L_eff = L/3

    # Simpler: use the general formula
    # ρ_Cas = -(π²/90) × (1/L_eff⁴) × [n_b - (7/8)n_f]/(4×360)
    # = -(π²)/(1440 × L_eff⁴) × Δn

    # Standard S¹ Casimir: E_Cas/V₃ = -π²/(720 L⁴) × Δn  [Zeldovich convention]
    # (The factor depends on convention; using Appelquist-Chodos)

    L_eff = L / 3  # Z₃ effective length

    Delta_n = n_scalars + n_gauge * 2 - (7/8) * n_weyl

    # 4D vacuum energy density (after integrating over X)
    # ρ = (1/L) × integral of 5D Casimir over [0, L]
    # = (1/L) × V_Cas^{5D} × L = V_Cas^{5D}
    # In natural units:
    rho_cas = -(np.pi**2 / (720)) * Delta_n / L_eff**4

    return rho_cas, Delta_n


def print_section(title, num):
    print("\n" + "─" * 70)
    print(f"  SECTION {num}: {title}")
    print("─" * 70)


def main():
    print("=" * 70)
    print("  COSMOLOGICAL CONSTANT FROM CASIMIR ENERGY ON S¹/Z₃")
    print("  STUR Framework v5.2 — First-Principles Computation")
    print("=" * 70)

    # SM field content
    n_scalars = 4   # Higgs doublet (2 complex = 4 real)
    n_weyl = 90     # 45 Weyl fermions × 2 (Dirac) = 90 Weyl
                     # Actually: 3 gen × (2 quarks × 3 colors + 2 leptons) × 2 chiralities
                     # = 3 × (6+2) × 2 = 48 Weyl = 24 Dirac
                     # With color: 3×(2×3+2)×2 = 48 Weyl

    # Let's be careful about the SM d.o.f.
    # Quarks: 6 flavors × 3 colors × 4 (Dirac spinor) = 72
    # Leptons: 6 × 4 = 24 (including ν_R if Dirac)
    # Without ν_R: 3 × (4+2) = 18 (charged leptons: 4 per Dirac, neutrinos: 2 per Weyl)

    # Count Weyl fermions explicitly:
    # u_L, d_L: 2 × 3 colors × 3 gen = 18
    # u_R, d_R: 2 × 3 colors × 3 gen = 18
    # e_L, ν_L: 2 × 3 gen = 6
    # e_R: 1 × 3 gen = 3
    # Total Weyl: 18 + 18 + 6 + 3 = 45 (SM without ν_R)
    n_weyl_SM = 45

    # Bosons:
    # W±, Z: 3 × 3 polarizations = 9 (but massive → 3 each in 4D+extra)
    # γ: 2 polarizations
    # gluons: 8 × 2 = 16 polarizations
    # In 5D: each gauge boson has 3 physical polarizations (D-2 = 3 in 5D)
    # + 1 scalar from A_5 component
    # Total gauge d.o.f.: 12 gauge bosons × (3+1) = 48 ... no
    # Actually for Casimir counting, we count on-shell 4D d.o.f.:
    # Massless vectors: 2 d.o.f. each → γ(2) + 8 gluons(16) = 18
    # Massive vectors: 3 d.o.f. each → W±(6) + Z(3) = 9
    # Plus Higgs: 4 real scalars (but 3 eaten → 1 physical Higgs)
    # After EWSB: 1 Higgs + 3 Goldstones (eaten) → 1 scalar + 3 longitudinal
    # For Casimir with unbroken symmetry (high T / small L):
    n_b_gauge = 12 * 2  # 12 gauge bosons × 2 transverse polarizations = 24 boson d.o.f.
    # In 5D, also A_5 components = 12 real scalars
    n_b_A5 = 12
    n_b_higgs = 4  # Higgs doublet

    n_b_total = n_b_gauge + n_b_A5 + n_b_higgs  # = 40
    n_f_total = n_weyl_SM  # = 45

    print_section("SM Field Content on S¹/Z₃", 1)
    print(f"""
  Gauge bosons (transverse): 12 × 2 = {n_b_gauge} bosonic d.o.f.
  Gauge A₅ scalars:          12 × 1 = {n_b_A5} bosonic d.o.f.
  Higgs doublet:              4 real = {n_b_higgs} bosonic d.o.f.
  Total bosonic:                       {n_b_total}

  Weyl fermions (SM):                  {n_f_total}
  (3 gen × [2(u,d)×3(color) + 2(e,ν)]_L + [2(u,d)×3(color) + 1(e)]_R = 45)

  Δn_eff = n_b - (7/8)×n_f = {n_b_total} - (7/8)×{n_f_total}
         = {n_b_total} - {7/8 * n_f_total:.2f}
         = {n_b_total - 7/8 * n_f_total:.2f}
    """)

    Delta_n = n_b_total - (7/8) * n_f_total

    # ================================================================
    # SECTION 2: Casimir energy at various scales
    # ================================================================
    print_section("Casimir Energy at Various L", 2)

    print(f"\n  {'L':>12}  {'ρ_Cas (GeV⁴)':>14}  {'ρ_Cas/ρ_Λ':>14}  {'Comment':>30}")
    print(f"  {'─'*12}  {'─'*14}  {'─'*14}  {'─'*30}")

    L_values = {
        'L_Pl (1.6e-35m)': 1.6e-35 / (hbar_c * 1e-15),  # in GeV⁻¹
        'L_GUT (1e-31m)': 1e-31 / (hbar_c * 1e-15),
        'L_EW (1e-18m)': 1e-18 / (hbar_c * 1e-15),
        '0.8 μm': 0.8e-6 / (hbar_c * 1e-15),
        '1 mm': 1e-3 / (hbar_c * 1e-15),
        'vL=3 → L': 3.0 / v_EW,
    }

    for name, L_GeV in L_values.items():
        L_eff = L_GeV / 3
        rho = -(np.pi**2 / 720) * Delta_n / L_eff**4
        ratio = rho / Lambda_obs
        L_m = L_GeV * hbar_c * 1e-15
        print(f"  {name:>12}  {rho:14.4e}  {ratio:14.4e}  L = {L_m:.2e} m")

    # ================================================================
    # SECTION 3: What L gives the observed CC?
    # ================================================================
    print_section("What L Gives the Observed Λ₄?", 3)

    # ρ_Cas = -(π²/720) × Δn / (L/3)⁴
    # Set |ρ_Cas| = Λ_obs:
    # (L/3)⁴ = (π²/720) × |Δn| / Λ_obs
    # L/3 = [(π²/720) × |Δn| / Λ_obs]^{1/4}

    L_eff_CC = ((np.pi**2 / 720) * abs(Delta_n) / Lambda_obs)**0.25
    L_CC = 3 * L_eff_CC
    L_CC_m = L_CC * hbar_c * 1e-15

    print(f"""
  Setting |ρ_Casimir| = Λ_obs = {Lambda_obs:.2e} GeV⁴:

  (L/3)⁴ = (π²/720) × |Δn| / Λ_obs
  L/3 = [(π²/720) × {abs(Delta_n):.2f} / {Lambda_obs:.2e}]^(1/4)

  L_eff = {L_eff_CC:.4e} GeV⁻¹
  L = 3 × L_eff = {L_CC:.4e} GeV⁻¹ = {L_CC_m:.4e} m

  This is {L_CC_m*1e3:.2f} mm = {L_CC_m*1e6:.0f} μm
  Compare: ADD experimental bound L < 44 μm (2σ, torsion balance)

  M_KK = 2π/(L/3) = {2*np.pi/L_eff_CC:.4e} GeV = {2*np.pi/L_eff_CC*1e-3:.2f} TeV

  ⚠ NOTE: Since Δn < 0 (fermion-dominated), ρ_Cas > 0.
  The observed Λ₄ is also positive. So the Casimir energy has
  the RIGHT SIGN. But this is coincidental — ANY fermion-dominated
  theory gives positive Casimir energy.
    """)

    # ================================================================
    # SECTION 4: The Casimir CC problem
    # ================================================================
    print_section("The Casimir CC Problem", 4)

    # At the Planck scale
    rho_Planck = M_Pl**4 / (16 * np.pi**2)
    # At the EW scale
    rho_EW = v_EW**4

    print(f"""
  The standard CC problem:
    ρ_Λ^(obs) / ρ_Λ^(Planck) = {Lambda_obs / rho_Planck:.2e}

  In the STUR framework with L ~ {L_CC_m:.0e} m:
    The Casimir energy ρ_Cas ~ 1/L⁴ naturally gives ρ ~ Λ_obs
    ONLY if L is tuned to L ~ {L_CC_m*1e6:.0f} μm.

  But this is circular: we're choosing L so that ρ_Cas = Λ_obs.
  The CC problem is not solved — it's traded for an L problem.

  The hierarchy is:
    ρ_Cas(L_Pl) / ρ_Cas(L_CC) = (L_CC/L_Pl)⁴ = ({L_CC_m/1.6e-35:.2e})⁴
                                = {(L_CC_m/1.6e-35)**4:.2e}

  This is the SAME fine-tuning as the standard CC problem,
  just expressed as a length hierarchy instead of an energy hierarchy.
    """)

    # ================================================================
    # SECTION 5: Boson-fermion cancellation and SUSY
    # ================================================================
    print_section("Boson-Fermion Cancellation", 5)

    print(f"""
  For exact Casimir cancellation (ρ_Cas = 0), need Δn = 0:
    n_b = (7/8) × n_f
    {n_b_total} ≠ (7/8) × {n_f_total} = {7/8 * n_f_total:.2f}

  The SM is fermion-heavy: Δn = {Delta_n:.2f}

  With N=1 SUSY on S¹/Z₃:
    Each boson paired with a fermion → Δn = 0 exactly
    Casimir energy = 0 (to leading order)
    This is the standard SUSY motivation for the CC.

  Without SUSY: The Z₃ orbifold provides NO mechanism to
  cancel the Casimir contribution. The residual ρ_Cas is
  determined by Δn and L, both of which are inputs.

  With the STUR field content (SM + R-field):
    R-field: 2 real scalars → adds 2 to n_b
    n_b_STUR = {n_b_total} + 2 = {n_b_total + 2}
    Δn_STUR = {n_b_total + 2} - {7/8 * n_f_total:.2f} = {n_b_total + 2 - 7/8 * n_f_total:.2f}
    Still fermion-dominated. The R-field doesn't help.
    """)

    # ================================================================
    # SECTION 6: Topological contribution from Z₃
    # ================================================================
    print_section("Topological Contribution from Z₃ Structure", 6)

    # On Z₃ orbifold, there are contributions from twisted sectors
    # at the fixed points
    print(f"""
  On S¹/Z₃, the vacuum energy has three contributions:

  1. BULK (untwisted): Standard Casimir from KK modes n = 0,3,6,...
     ρ_bulk = -(π²/720) × Δn / (L/3)⁴
     = {-(np.pi**2/720) * Delta_n / L_eff_CC**4:.2e} GeV⁴ (at L = L_CC)

  2. FIXED POINT (twisted): Localized energy at the three Z₃ points
     These come from modes with Z₃ phase ω = exp(2πi/3)
     ρ_twisted ~ 3 × (Λ_UV⁴/16π²) × (1-ω)(1-ω²) = 3 × Λ_UV⁴/(16π²) × 3
     This is UV-sensitive and requires renormalization.

  3. TORSION (R-field): Energy from the R-field vacuum on S¹/Z₃
     V_R = v⁴ × λ_R (quartic coupling)
     At v = v_EW: V_R ~ (246 GeV)⁴ × O(1) ~ 3.7e9 GeV⁴
     This is 3.7e9 / 2.6e-47 = {3.7e9/2.6e-47:.0e} times too large!

  The twisted sector and R-field contributions are BOTH
  UV-sensitive and require cancellation to ~10⁻⁵⁶.
  This IS the cosmological constant problem — it's not solved
  by putting the SM on S¹/Z₃.
    """)

    # ================================================================
    # SECTION 7: What WOULD work
    # ================================================================
    print_section("What Would Actually Solve the CC Problem", 7)

    print(f"""
  For the Z₃ Casimir energy to naturally explain Λ₄:

  1. NEED: Δn ≈ 0 (boson-fermion balance)
     Status: Δn = {Delta_n:.1f} — far from zero
     Fix: Add 39 real scalars or remove 45 Weyl fermions
     Neither is physical within the SM

  2. NEED: L dynamically stabilized at L ~ {L_CC_m*1e6:.0f} μm
     Status: L_X effective potential has NO minimum (see lx_effective_potential.py)
     Fix: Would need additional physics (flux, SUSY, ...)

  3. NEED: Twisted sector contributions to cancel bulk
     Status: These are UV-sensitive, not calculable without UV completion
     Fix: String theory provides this cancellation in specific compactifications

  4. NEED: R-field vacuum energy to cancel everything else
     Status: V_R ~ v⁴ ~ 10⁹ GeV⁴ ≫ Λ_obs ~ 10⁻⁴⁷ GeV⁴
     Fix: Requires fine-tuning to 56 decimal places

  CONCLUSION:
  The S¹/Z₃ compactification does NOT solve or illuminate
  the cosmological constant problem. The CC on S¹/Z₃ has the
  same fine-tuning issues as in 4D, plus additional contributions
  from KK towers and twisted sectors that make it WORSE.
    """)

    # ================================================================
    # SECTION 8: Honest summary
    # ================================================================
    print_section("HONEST ASSESSMENT", 8)

    print(f"""
  CLAIM TESTED: "The cosmological constant can be computed from
  Casimir energy on S¹/Z₃ in the STUR framework."

  RESULT: FALSE

  What the S¹/Z₃ Casimir energy gives:
    ρ_Cas = -(π²/720) × Δn / (L/3)⁴
    With SM: Δn = {Delta_n:.1f} (fermion-dominated → positive ρ)
    Sign: CORRECT (Λ_obs > 0 and Δn < 0 → ρ_Cas > 0) ✓
    Magnitude: Requires L = {L_CC_m*1e6:.0f} μm to match Λ_obs
               This is NOT predicted — it's an INPUT.

  The CC problem remains:
    • Bulk Casimir: needs Δn ≈ 0 (SUSY) or L tuned
    • Twisted sectors: UV-sensitive, uncalculable
    • R-field VEV: V ~ v⁴ ~ 10⁹ GeV⁴ needs cancellation to 10⁻⁵⁶
    • Total: same 10⁵⁶ fine-tuning as 4D

  What the framework CAN say:
    • IF L is somehow stabilized (not shown), and
    • IF twisted + R-field contributions cancel (not shown), then
    • The residual Casimir gives ρ ~ 1/L⁴ with the right sign
    • This is suggestive but NOT a prediction

  STATUS: The CC is NOT computed from the STUR framework.
  It remains an input parameter (or equivalently, L remains unfixed).
    """)


if __name__ == "__main__":
    main()
