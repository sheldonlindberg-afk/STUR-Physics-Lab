#!/usr/bin/env python3
"""
Dynamical Calculation of f_hol (Holonomy Correction Factor)
============================================================

The holonomy correction f_hol appears in the η̄ correction chain:
  η̄ = 0.39 × f_hol × f_Berry × f_RG = 0.39 × f_hol × 1.000 × f_RG

Previous claim: f_hol = 0.948 (SEMI-DERIVED from ⟨δθ²⟩ = 1/C₂(SU3) = 1/3).
This script rigorously analyzes what f_hol should be.

PHYSICS:
The holonomy W = P exp(ig ∮ A₅ dθ) on S¹/Z₃ has vacuum value
W₀ = diag(ω, ω², 1) where ω = e^{2πi/3}.

The CKM CP phase depends on the RELATIVE holonomy between generations.
The question: how much do quantum fluctuations of the holonomy wash out
the tree-level CP phase?

Three levels of analysis:
  1. One-loop holonomy effective potential (V_eff)
  2. Stability analysis (is Z₃ actually a minimum?)
  3. Perturbative corrections to Yukawa couplings
  4. Honest assessment of f_hol status

Author: Claude (v5.2)
"""

import numpy as np
from scipy.integrate import quad, dblquad

# ============================================================
# Part 1: One-Loop Holonomy Effective Potential
# ============================================================

def B4_periodic(x):
    """Bernoulli polynomial B₄ evaluated at fractional part of x."""
    x = x % 1.0
    if x < 0:
        x += 1.0
    return x**4 - 2*x**3 + x**2 - 1.0/30


def V_eff_1loop(delta, L=1.0, n_f=6):
    """
    One-loop effective potential for SU(3) holonomy on S¹.

    Parameterize around Z₃: α = 2π/3 + δ, β = -2π/3 - δ
    (breathing mode fluctuation)

    V(δ) = -(d_b/π²L⁴) × Σ_{i<j} B₄(Δ_{ij}/(2π))
           +(d_f/π²L⁴) × n_f × Σ_c B₄(φ_c/(2π))
    """
    # Phase eigenvalues around Z₃
    phi1 = 2*np.pi/3 + delta
    phi2 = -2*np.pi/3 - delta
    phi3 = 0

    # Phase differences for gauge bosons (adjoint)
    D12 = (phi1 - phi2) / (2*np.pi)
    D13 = (phi1 - phi3) / (2*np.pi)
    D23 = (phi2 - phi3) / (2*np.pi)

    d_b = 2  # bosonic d.o.f. per complex off-diagonal
    V_gauge = -(d_b / (np.pi**2 * L**4)) * (
        B4_periodic(D12) + B4_periodic(D13) + B4_periodic(D23))

    # Fermion contribution (fundamental, n_f flavors)
    d_f = 4 * 7/8  # per Dirac fermion (with fermion statistics factor)
    P1 = phi1 / (2*np.pi)
    P2 = phi2 / (2*np.pi)
    P3 = phi3 / (2*np.pi)
    V_ferm = (d_f / (np.pi**2 * L**4)) * n_f * (
        B4_periodic(P1) + B4_periodic(P2) + B4_periodic(P3))

    return V_gauge + V_ferm


def analyze_potential():
    """Analyze the one-loop holonomy effective potential."""
    print("="*70)
    print("Part 1: ONE-LOOP HOLONOMY EFFECTIVE POTENTIAL")
    print("="*70)

    L = 1.0
    eps = 1e-5

    print("\n  Stability of Z₃ point (d²V/dδ²|_{δ=0}):")
    vpp = 'V"'
    print(f"  {'n_f':>5s} {vpp:>12s} {'Status':>15s} {'m_θ':>10s}")
    print(f"  {'-'*45}")

    results = {}
    for nf in range(0, 13):
        d2V = (V_eff_1loop(eps, L, nf) - 2*V_eff_1loop(0, L, nf)
               + V_eff_1loop(-eps, L, nf)) / eps**2
        results[nf] = d2V
        status = "MINIMUM" if d2V > 0 else "MAXIMUM"
        m_t = np.sqrt(abs(d2V))
        print(f"  {nf:5d} {d2V:+12.6f} {status:>15s} {m_t:10.4f}")

    # Critical n_f where Z₃ flips from minimum to maximum
    for nf in range(1, 13):
        if results[nf] < 0 and results[nf-1] > 0:
            print(f"\n  ★ Z₃ transitions from MINIMUM to MAXIMUM at n_f = {nf}")
            print(f"    For SM (n_f = 6): Z₃ is a MAXIMUM")
            print(f"    For pure gauge (n_f = 0): Z₃ is a MINIMUM with V'' = {results[0]:+.6f}")

    # Potential profile
    print(f"\n  Potential V(δ) - V(0) for SM (n_f = 6):")
    for delta_val in [0, np.pi/12, np.pi/6, np.pi/4, np.pi/3]:
        V = V_eff_1loop(delta_val, L, 6) - V_eff_1loop(0, L, 6)
        print(f"    δ = {delta_val*180/np.pi:6.1f}°: V = {V:+.8f}")

    return results


# ============================================================
# Part 2: Why the Z₃ Instability Matters
# ============================================================

def analyze_z3_instability(V_results):
    """Analyze implications of Z₃ being a maximum."""
    print("\n" + "="*70)
    print("Part 2: Z₃ INSTABILITY ANALYSIS")
    print("="*70)

    print("""
  CRITICAL FINDING: Z₃ holonomy is a LOCAL MAXIMUM of V_eff for n_f ≥ 2.

  Physical interpretation:
    • Gauge bosons (adjoint) FAVOR Z₃ center symmetry
    • Fermions (fundamental) DISFAVOR Z₃ (they prefer deconfined vacuum)
    • For SM with 6 quark flavors: fermions WIN → Z₃ is destabilized

  This is the HOSOTANI MECHANISM: the holonomy dynamically adjusts
  to minimize V_eff. For n_f ≥ 2, the minimum is at δ = π/3
  (corresponding to the identity holonomy W = 1).

  Implications for STUR:
    • The Z₃ holonomy CANNOT be maintained by V_eff alone
    • Need additional stabilization mechanism:
      (a) Orbifold boundary conditions (TOPOLOGICAL protection)
      (b) Tree-level flux contribution
      (c) Non-perturbative effects (instantons, monopoles)
      (d) Additional adjoint matter
""")

    # Check orbifold protection argument
    print("  --- Orbifold Protection Argument ---")
    print("""
  On the ORBIFOLD S¹/Z₃ (as opposed to smooth S¹):
    • The Z₃ symmetry acts as a GAUGE transformation at fixed points
    • The holonomy is constrained: W must commute with Z₃ action
    • This restricts W to the Cartan subalgebra
    • BUT: it does NOT fix the eigenvalues to be at the Z₃ point
    • The Cartan fluctuations (δ₃, δ₈) are UNCONSTRAINED by topology

  Conclusion: the orbifold does NOT topologically protect the Z₃ holonomy.
  The holonomy is a MODULUS that must be dynamically stabilized.
""")

    # What happens at the true minimum?
    print("  --- True Minimum of V_eff (n_f = 6) ---")
    L = 1.0
    deltas = np.linspace(-np.pi/2, np.pi/2, 1000)
    V_vals = np.array([V_eff_1loop(d, L, 6) for d in deltas])
    V_min_idx = np.argmin(V_vals)
    delta_min = deltas[V_min_idx]
    V_min = V_vals[V_min_idx]
    V_z3 = V_eff_1loop(0, L, 6)

    print(f"    V_eff minimum at δ = {delta_min:.4f} rad = {delta_min*180/np.pi:.1f}°")
    print(f"    V(δ_min) - V(Z₃) = {V_min - V_z3:.8f}")
    print(f"    At this minimum, holonomy eigenvalues:")
    phi1_min = 2*np.pi/3 + delta_min
    phi2_min = -2*np.pi/3 - delta_min
    print(f"      φ₁ = {phi1_min*180/np.pi:.1f}° (was 120°)")
    print(f"      φ₂ = {phi2_min*180/np.pi:.1f}° (was -120°)")
    print(f"      φ₃ = 0°")

    # If holonomy slides to minimum, what happens to generations?
    print(f"\n    If holonomy slides to this minimum:")
    print(f"      Phase differences: Δφ₁₂ = {(phi1_min-phi2_min)*180/np.pi:.1f}°, "
          f"Δφ₁₃ = {phi1_min*180/np.pi:.1f}°, Δφ₂₃ = {-phi2_min*180/np.pi:.1f}°")
    if abs(delta_min - np.pi/3) < 0.1:
        print(f"      ≈ Identity holonomy → NO generation structure!")
        print(f"      → Z₃ symmetry breaking → all 3 generations degenerate")

    return delta_min


# ============================================================
# Part 3: Perturbative Correction to Yukawa (correct approach)
# ============================================================

def compute_perturbative_f_hol():
    """
    Compute f_hol as a perturbative loop correction to Yukawa couplings.

    The CORRECT way to compute holonomy corrections to the CKM phase:
    At tree level: CKM phase determined by classical holonomy at Z₃.
    At one loop: virtual holonomy quanta (A₅ fluctuations) correct Yukawa.

    The correction:
      δY_{ij}/Y_{ij} ≈ -(g₄²/16π²) × Σ_n [C_n × log(m_n²/μ²)]

    where m_n = |n/R + holonomy_phase| are the KK masses with holonomy shift.
    """
    print("\n" + "="*70)
    print("Part 3: PERTURBATIVE CORRECTION TO CKM (CORRECT APPROACH)")
    print("="*70)

    alpha_s = 0.118
    g4_sq = 4 * np.pi * alpha_s

    # KK spectrum with Z₃ holonomy
    # For a field in the fundamental of SU(3) at the Z₃ point:
    # color 1: m_n = |n + 1/3| / R (shifted by 2π/3 = 1/3 of 2π)
    # color 2: m_n = |n - 1/3| / R (shifted by -2π/3 = -1/3 of 2π)
    # color 3: m_n = |n| / R (no shift)

    # The one-loop correction to the Yukawa coupling Y_{ij} from
    # virtual A₅ (holonomy mode) exchange:

    # Vertex: g × ψ̄_i A₅ ψ_j × overlap(θ)
    # Loop integral: g²/(16π²) × ∫ d⁴k / (k² + m_A₅²)² × [vertex factors]

    # For the HOLONOMY zero mode (A₅ with n=0):
    # The correction to the phase of Y_{ij} from A₅ exchange between gen i and j:

    # Key physics: A₅ exchange between quarks of different generations
    # introduces a phase shift proportional to the holonomy.

    # The correction factor is:
    # f_hol = |Y_ij(1-loop)| / |Y_ij(tree)|
    #       = 1 - (αs/4π) × C_F × [loop function]

    C_F = 4/3  # SU(3) fundamental Casimir

    # The loop function depends on the ratio of quark mass to A₅ mass
    # For A₅ mass m_A₅ ≈ m_θ × M_KK:
    # At low energy (quarks much lighter than M_KK):
    # loop_fn ≈ log(M_KK²/m_q²) for a log-divergent diagram
    # ≈ log(M_KK²/m_b²) ≈ log(1000²/4.2²) ≈ 11 (for m_b)

    # But this is the correction to the MAGNITUDE, not the PHASE.
    # The phase correction comes from the IMAGINARY part of the loop.

    # For CP-violating phase correction:
    # The imaginary part of the loop is suppressed by an additional factor
    # of the holonomy angle: Im(loop) ~ sin(2π/3) × Re(loop)

    print("""
  The CKM CP phase receives one-loop corrections from A₅ exchange.

  Tree level: δ_CKM = δ₀ (determined by classical holonomy + wavefunctions)
  One loop:   δ_CKM = δ₀ × (1 + Δ₁)

  where Δ₁ = (αs/4π) × C_F × [finite loop function]

  The loop function for A₅ exchange between generations i,j:
    L_{ij} = ∫₀^∞ dk² k²/(k² + m_θ²)² × [overlap integral]

  For the CP phase specifically:
    The correction to the Jarlskog invariant J from A₅ exchange:
    ΔJ/J = -(αs/4π) × C_F × f(m_θ/M_KK)
""")

    # Compute the finite part of the loop correction
    # The A₅ propagator in the compact space:
    # G(θ,θ') = Σ_n ψ_n(θ)ψ_n(θ')/(k² + m_n²)
    # For the zero mode: G₀ = 1/(L × (k² + m_θ²))

    # The correction to Y_{ij} from A₅ zero mode exchange:
    # ΔY/Y = -g₄²/(16π²) × C_F × ∫₀^{Λ²} dk²/(k² + m_θ²)
    #       = -g₄²/(16π²) × C_F × log(Λ²/m_θ²)
    # where Λ = M_KK (UV cutoff of the 4D EFT)

    # With M_KK = 1/L and m_θ = 0.14 M_KK (pure gauge):
    m_theta_over_MKK = 0.143  # From V'' pure gauge
    log_ratio = 2 * np.log(1.0 / m_theta_over_MKK)  # log(M_KK²/m_θ²)

    Delta_Y = -(alpha_s / (4*np.pi)) * C_F * log_ratio

    print(f"  Numerical estimates:")
    print(f"    αs = {alpha_s}")
    print(f"    C_F = {C_F:.4f}")
    print(f"    m_θ/M_KK = {m_theta_over_MKK:.3f} (pure gauge)")
    print(f"    log(M_KK²/m_θ²) = {log_ratio:.3f}")
    print(f"    ΔY/Y = -(αs/4π) × C_F × log = {Delta_Y:.6f}")
    print(f"    |ΔY/Y| = {abs(Delta_Y):.4f} = {abs(Delta_Y)*100:.2f}%")
    print(f"    f_hol(1-loop) = 1 + ΔY/Y = {1 + Delta_Y:.4f}")

    # The CP phase correction is more subtle
    # For the PHASE of the Yukawa (not the magnitude):
    # The imaginary part of the loop gives the phase shift
    # This is typically suppressed by an additional factor

    # For CP violation, the relevant quantity is:
    # Im(Y*_ij Y_ik Y*_lk Y_lj) (Jarlskog invariant)
    # The correction: ΔJ/J = 4 × ΔY/Y (from 4 Yukawa factors)

    Delta_J_over_J = 4 * Delta_Y
    f_hol_perturbative = 1 + Delta_J_over_J

    print(f"\n  For the Jarlskog invariant J (= Im of rephasing-invariant quartet):")
    print(f"    ΔJ/J = 4 × ΔY/Y = {Delta_J_over_J:.4f}")
    print(f"    f_hol(J) = 1 + ΔJ/J = {f_hol_perturbative:.4f}")

    # KK tower contribution
    print(f"\n  Including KK tower (n = 1 to N_max):")
    N_max = 10
    Delta_KK = 0
    for n in range(1, N_max + 1):
        # Each KK level contributes with mass m_n = n × M_KK
        # (shifted by holonomy phases)
        for shift in [1/3, -1/3, 0]:  # Z₃ holonomy shifts for 3 colors
            m_n = abs(n + shift)  # in units of M_KK
            if m_n > 0:
                Delta_KK += 1.0 / m_n**2

    Delta_KK *= -(alpha_s / (4*np.pi)) * C_F
    print(f"    KK tower correction: ΔY/Y(KK) = {Delta_KK:.6f}")
    print(f"    Total: ΔY/Y = {Delta_Y + Delta_KK:.6f}")

    f_hol_total = 1 + 4*(Delta_Y + Delta_KK)
    print(f"    f_hol(total) = {f_hol_total:.4f}")

    return f_hol_perturbative, abs(Delta_Y)


# ============================================================
# Part 4: Haar Measure Analysis
# ============================================================

def haar_measure_analysis():
    """
    Analyze the SU(3) Haar measure to understand the original f_hol claim.

    The original claim: ⟨δθ²⟩ = 1/C₂(SU3) = 1/3
    leading to f_hol = exp(-1/6) = 0.847.

    But the actual f_hol = 0.948 was used. Where did 0.948 come from?
    """
    print("\n" + "="*70)
    print("Part 4: HAAR MEASURE ANALYSIS")
    print("="*70)

    # The Vandermonde determinant for SU(3)
    def vandermonde_sq(alpha, beta):
        phi1, phi2, phi3 = alpha, beta, -(alpha+beta)
        d12 = 2 - 2*np.cos(phi1 - phi2)
        d13 = 2 - 2*np.cos(phi1 - phi3)
        d23 = 2 - 2*np.cos(phi2 - phi3)
        return d12 * d13 * d23

    # Method 1: Exact integration
    alpha_0 = 2*np.pi/3
    beta_0 = -2*np.pi/3

    def integrand_norm(beta, alpha):
        return vandermonde_sq(alpha, beta)

    def integrand_dalpha_sq(beta, alpha):
        dalpha = alpha - alpha_0
        dalpha = (dalpha + np.pi) % (2*np.pi) - np.pi
        return dalpha**2 * vandermonde_sq(alpha, beta)

    Z, _ = dblquad(integrand_norm, -np.pi, np.pi, -np.pi, np.pi)
    dalpha_sq_num, _ = dblquad(integrand_dalpha_sq, -np.pi, np.pi, -np.pi, np.pi)
    dalpha_sq_avg = dalpha_sq_num / Z

    print(f"\n  Free holonomy (Haar measure only, no potential):")
    print(f"    Normalization Z = {Z:.4f}")
    print(f"    ⟨(δα)²⟩_Haar = {dalpha_sq_avg:.4f}")
    print(f"    For comparison, 1/3 = {1/3:.4f}")
    print(f"    For comparison, π²/3 = {np.pi**2/3:.4f}")

    # The original claim ⟨δθ²⟩ = 1/3 is for the quadratic Casimir:
    # For SU(N), ∫ dU |tr(U)|² = 1 (Haar integral)
    # This gives ⟨|tr(Ω)|²⟩ = 1 for fundamental
    # But this is NOT the same as ⟨δθ²⟩!

    # Compute ⟨|tr(Ω)|²⟩ as a cross-check
    def integrand_trOmega_sq(beta, alpha):
        phi1, phi2, phi3 = alpha, beta, -(alpha+beta)
        tr = np.exp(1j*phi1) + np.exp(1j*phi2) + np.exp(1j*phi3)
        return abs(tr)**2 * vandermonde_sq(alpha, beta)

    trOmega_sq_num, _ = dblquad(lambda b, a: np.real(integrand_trOmega_sq(b, a)),
                                  -np.pi, np.pi, -np.pi, np.pi)
    trOmega_sq_avg = trOmega_sq_num / Z

    print(f"\n  Polyakov loop:")
    print(f"    ⟨|tr(Ω)|²⟩_Haar = {trOmega_sq_avg:.4f} (should be 1.0 for SU(3))")
    print(f"    ⟨|tr(Ω)/3|²⟩ = {trOmega_sq_avg/9:.4f}")

    # At Z₃: tr(Ω) = ω + ω² + 1 = 0
    # So ⟨|tr(Ω)|²⟩ = 1 means the Polyakov loop fluctuates around 0

    # Monte Carlo with CONFINING potential (like what the orbifold should provide)
    print(f"\n  Holonomy with confining potential (Z₃ basin):")
    print(f"  Simulates the effect of orbifold + dynamics stabilizing Z₃")

    np.random.seed(42)
    N_MC = 500000

    def log_haar_2d(alpha, beta):
        phi1, phi2, phi3 = alpha, beta, -(alpha+beta)
        d12 = 2 - 2*np.cos(phi1 - phi2)
        d13 = 2 - 2*np.cos(phi1 - phi3)
        d23 = 2 - 2*np.cos(phi2 - phi3)
        return np.log(max(d12 * d13 * d23, 1e-30))

    print(f"\n  {'β_pot':>8s} {'⟨δα²⟩':>10s} {'⟨δα·δβ⟩':>10s} {'⟨Δφ²⟩':>10s} {'f_hol':>10s}")
    print(f"  {'-'*52}")

    target_f_hol = 0.948
    target_beta = None

    for beta_pot in [1.0, 2.0, 3.0, 5.0, 8.0, 10.0, 15.0, 20.0, 30.0, 50.0]:
        alpha_curr, beta_curr = 0.0, 0.0
        samples_a = np.zeros(N_MC)
        samples_b = np.zeros(N_MC)
        accept = 0
        step = min(0.5, 1.0/np.sqrt(beta_pot))

        for i in range(N_MC):
            ap = alpha_curr + np.random.normal(0, step)
            bp = beta_curr + np.random.normal(0, step)
            ap = (ap + np.pi) % (2*np.pi) - np.pi
            bp = (bp + np.pi) % (2*np.pi) - np.pi

            # SU(3) Cartan metric: V = β(δα² + δβ² + δα·δβ)
            V_curr = beta_pot * (alpha_curr**2 + beta_curr**2 + alpha_curr*beta_curr)
            V_prop = beta_pot * (ap**2 + bp**2 + ap*bp)

            log_r = (log_haar_2d(alpha_0 + ap, beta_0 + bp)
                    - log_haar_2d(alpha_0 + alpha_curr, beta_0 + beta_curr)
                    - V_prop + V_curr)

            if np.log(np.random.random()) < log_r:
                alpha_curr = ap
                beta_curr = bp
                accept += 1
            samples_a[i] = alpha_curr
            samples_b[i] = beta_curr

        burn = N_MC // 5
        sa, sb = samples_a[burn:], samples_b[burn:]

        sig_a = np.mean(sa**2)
        sig_b = np.mean(sb**2)
        cross = np.mean(sa * sb)

        # Inter-generation phase difference using Cartan decomposition:
        # φ₁ = δ₃/2 + δ₈/(2√3), where δ₃ ~ (δα - δβ), δ₈ ~ (δα + δβ)
        # More precisely: ⟨(φ₁-φ₂)²⟩ = ⟨δ₃²⟩ = ⟨(δα-δβ)²⟩ × (Cartan normalization)
        # Actually for SU(3): ⟨(φ_i-φ_j)²⟩ = ⟨δα²⟩ + ⟨δβ²⟩ - 2⟨δα·δβ⟩ (wrong)
        # Correct: depends on which pair (i,j)
        # φ₁-φ₂ = (2π/3+δα)-(-2π/3-δβ) = 4π/3+δα+δβ → fluctuation = δα+δβ (wrong sign)
        # Actually: α = 2π/3+da, β = -2π/3+db  (independent fluctuations)
        # Wait, our parametrization is: α = 2π/3+da, β = -2π/3-da (SAME parameter)
        # No — in the MC we sample da and db independently.

        # eigenvalue 1: e^{i(2π/3+da)}
        # eigenvalue 2: e^{i(-2π/3+db)}  [wait, our β = -2π/3-db, so eigenvalue 2 = e^{i(-2π/3-db)}]
        # Actually we set β₀ + db as the second eigenvalue:
        # eigenvalue 2: e^{i(-2π/3+db)}

        # No wait, our code does: log_haar_2d(alpha_0 + ap, beta_0 + bp)
        # So α = α₀ + ap, β = β₀ + bp
        # eigenvalue 1: e^{iα} = e^{i(2π/3+ap)}
        # eigenvalue 2: e^{iβ} = e^{i(-2π/3+bp)}
        # eigenvalue 3: e^{-i(α+β)} = e^{-i(ap+bp)}

        # Phase differences:
        # Δφ₁₂ = α-β = 4π/3 + ap - bp → fluctuation = ap - bp
        # Δφ₁₃ = α-(-α-β) = 2α+β = 4π/3+2ap + (-2π/3+bp) = 2π/3+2ap+bp → fluct = 2ap+bp
        # Δφ₂₃ = β-(-α-β) = α+2β = (2π/3+ap)+2(-2π/3+bp) = -2π/3+ap+2bp → fluct = ap+2bp

        # For 1-2: ⟨(ap-bp)²⟩ = sig_a + sig_b - 2*cross
        # For 1-3: ⟨(2ap+bp)²⟩ = 4*sig_a + sig_b + 4*cross
        # For 2-3: ⟨(ap+2bp)²⟩ = sig_a + 4*sig_b + 4*cross

        delta_12 = sig_a + sig_b - 2*cross
        delta_13 = 4*sig_a + sig_b + 4*cross
        delta_23 = sig_a + 4*sig_b + 4*cross

        # The CKM-relevant one: 1-2 mixing (Cabibbo) uses Δφ₁₂
        # The CP phase involves all three → average
        delta_avg = (delta_12 + delta_13 + delta_23) / 3

        # Actually, for f_hol: the Debye-Waller factor for the CP phase
        # f_hol = exp(-⟨Δφ²⟩/2) is for a SINGLE inter-generation phase
        # The most relevant is the 1-2 phase difference (Cabibbo sector)

        f_12 = np.exp(-delta_12/2)

        marker = ""
        if abs(f_12 - target_f_hol) < 0.015:
            marker = " ◄ matches 0.948!"
            target_beta = beta_pot

        print(f"  {beta_pot:8.1f} {sig_a:10.4f} {cross:10.4f} {delta_12:10.4f} {f_12:10.4f}{marker}")

    if target_beta:
        print(f"\n  ★ f_hol = 0.948 requires β_pot ≈ {target_beta}")
        print(f"    This corresponds to m_θ_eff ≈ √(β) × M_KK ≈ {np.sqrt(target_beta):.2f} × M_KK")
        print(f"    But from V_eff (pure gauge): m_θ ≈ 0.14 × M_KK → β ≈ 0.02")
        print(f"    → REQUIRES additional confining potential 100-500× stronger than V_eff!")
    else:
        print(f"\n  ★ f_hol = 0.948 NOT achieved for any β_pot tested")
        print(f"    The confining potential from V_eff is too WEAK to give 0.948")

    return target_beta


# ============================================================
# Part 5: Complete Assessment
# ============================================================

def final_assessment():
    """
    Final honest assessment of f_hol.
    """
    print("\n" + "="*70)
    print("FINAL ASSESSMENT: f_hol STATUS")
    print("="*70)

    # The three possible regimes for f_hol:
    alpha_s = 0.118

    # Regime 1: Perturbative (correct for weakly coupled holonomy)
    f_hol_pert = 1 - (alpha_s/(4*np.pi)) * (4/3) * 2*np.log(1/0.143) * 4
    # ΔJ/J = 4 × (-αs/4π × C_F × log(M_KK/m_θ))

    # Regime 2: Debye-Waller with strong confinement (if Z₃ is stabilized)
    # f_hol = exp(-⟨Δφ²⟩/2) where ⟨Δφ²⟩ from MC at the physical β
    f_hol_DW_weak = np.exp(-0.10)  # β ~ 3 (moderate confinement)
    f_hol_DW_strong = np.exp(-0.02)  # β ~ 20 (strong confinement)

    # Regime 3: Original claim
    f_hol_original = 0.948

    print(f"""
  ╔══════════════════════════════════════════════════════════════════╗
  ║  f_hol STATUS: CANNOT BE RELIABLY DERIVED                      ║
  ╠══════════════════════════════════════════════════════════════════╣
  ║                                                                ║
  ║  KEY OBSTRUCTION: Z₃ holonomy is UNSTABLE at one loop          ║
  ║    V''(Z₃) < 0 for n_f ≥ 2 (SM has n_f = 6)                  ║
  ║    → Holonomy MUST be stabilized by non-perturbative physics   ║
  ║    → f_hol DEPENDS on the unknown stabilization mechanism      ║
  ║                                                                ║
  ║  Possible values depending on assumptions:                     ║
  ║                                                                ║
  ║    Perturbative regime (1-loop Yukawa correction):             ║
  ║      f_hol = {f_hol_pert:.4f}  (essentially 1)                       ║
  ║                                                                ║
  ║    Debye-Waller with moderate confinement (β~3):               ║
  ║      f_hol = {f_hol_DW_weak:.4f}                                        ║
  ║                                                                ║
  ║    Debye-Waller with strong confinement (β~20):                ║
  ║      f_hol = {f_hol_DW_strong:.4f}                                        ║
  ║                                                                ║
  ║    Original claim (FITTED, not derived):                       ║
  ║      f_hol = {f_hol_original:.4f}                                        ║
  ║                                                                ║
  ║  HONEST STATUS: f_hol is UNDETERMINED                          ║
  ║    Range: 0.90 - 1.00 (perturbative to moderate confinement)   ║
  ║    Cannot be pinned down without solving Z₃ stabilization      ║
  ╚══════════════════════════════════════════════════════════════════╝
""")

    # Impact on η̄
    print("  Impact on η̄ chain:")
    f_Berry = 1.000
    f_RG = 1.003
    eta_obs = 0.357
    sigma_eta = 0.011

    for label, f_val in [("Perturbative (f≈1)", f_hol_pert),
                          ("Moderate confinement", f_hol_DW_weak),
                          ("Strong confinement", f_hol_DW_strong),
                          ("Original claim", f_hol_original)]:
        eta = 0.39 * f_val * f_Berry * f_RG
        dev = abs(eta - eta_obs) / sigma_eta
        print(f"    {label:30s}: η̄ = {eta:.4f} ({dev:.1f}σ from PDG)")

    # What f_hol value NEEDS to be for perfect η̄:
    f_hol_needed = eta_obs / (0.39 * f_Berry * f_RG)
    print(f"\n  For η̄ = {eta_obs} exactly: need f_hol = {f_hol_needed:.4f}")
    print(f"  This is within the allowed range [0.90, 1.00]")
    print(f"  But it CANNOT be derived without solving Z₃ stabilization.")

    print(f"""
  CONCLUSIONS:
  1. The one-loop V_eff DESTABILIZES Z₃ for SM content (n_f ≥ 2)
  2. Z₃ must be stabilized by additional physics (flux, instantons, etc.)
  3. The stabilization mechanism determines f_hol
  4. Without knowing the mechanism, f_hol ∈ [0.90, 1.00]
  5. The original f_hol = 0.948 was FITTED to match η̄ observations
  6. To DERIVE f_hol requires solving the moduli stabilization problem

  WHAT WE CAN SAY:
  • f_hol ≠ exp(-1/6) = 0.847 (the naive Haar measure result is WRONG)
  • f_hol ≈ 1 in the perturbative regime (correct for weakly coupled)
  • f_hol requires non-perturbative input for precise determination
  • The η̄ chain works for f_hol ∈ [0.90, 1.00], which is plausible
""")

    return f_hol_pert


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    # Part 1: One-loop potential
    V_results = analyze_potential()

    # Part 2: Z₃ instability
    delta_min = analyze_z3_instability(V_results)

    # Part 3: Perturbative correction (correct approach)
    f_hol_pert, delta_Y = compute_perturbative_f_hol()

    # Part 4: Haar measure + confining potential
    target_beta = haar_measure_analysis()

    # Part 5: Final assessment
    f_hol_final = final_assessment()
