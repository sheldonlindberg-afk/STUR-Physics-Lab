# Complete Derivation of the eta-bar Correction Chain

**Document Type:** Theoretical Physics Derivation
**Framework:** STUR v4.3 (∞₃ Helix Geometry)
**Version:** 1.0
**Date:** 2026-01-25
**Purpose:** Derive the three correction factors connecting eta-bar_base = 0.39 to eta-bar_obs = 0.348

---

## Executive Summary

The STUR framework predicts the CP-violating Wolfenstein parameter eta-bar from ∞₃ helix geometry. The base calculation from helix chirality gives:

```
eta-bar_base = 0.39
```

However, PDG 2024 reports:

```
eta-bar_obs = 0.348 +/- 0.010
```

This document derives the complete correction chain:

```
eta-bar = sin(delta_CKM) x 0.424 x f_hol x f_Berry x f_RG
        = sin(delta_CKM) x 0.424 x 1.000 x 1.000 x 1.003
        = 0.3947
```

Agreement: 13.4% deviation from PDG 2024 (eta-bar_obs = 0.348 +/- 0.010) — Grade D.

**v6.0 RESOLUTION (2026-07-18):** The self-contradiction flagged in prior audits of
this document (f_hol = 0.948 simultaneously labeled "derived" in §2, "conditionally
derived" in §7.3, and "FITTED" in the closing status block) has been resolved by
**removing the override**. The canonical prediction script previously hard-coded
f_hol = 0.948 as a fitted constant chosen to pull eta-bar toward the PDG value. That
override has been deleted. Every dynamical calculation actually carried out in this
document and in HOLONOMY_AVERAGING_DERIVATION.md — the one-loop effective potential,
and every non-fitted attempt in the companion document — agrees that f_hol ≈ 1.000
(the ∞₃ holonomy vacuum is destabilized for n_f ≥ 2, so no fluctuation suppression
survives). The canonical script now uses the honest value **f_hol = 1.000**, and the
chain gives **eta-bar = 0.3947**, a 13.4% deviation from the observed 0.348 (Grade D,
not the sub-1σ "acceptable" result previously reported using the fitted 0.948). This
is an honest downgrade, not a new error: it removes a fitted correction that had been
dressed up as a derivation. See §2 and §7 below, both updated to reflect this.

**Formal status of the remaining factors (v5.4, unaffected by the f_hol resolution):**
- f_RG = 1.003 ± 0.001: **PROVED** — QCD KK threshold cancels in CKM by flavor
  universality (gluon corrections are generation-blind). Only A₅ exchange (+0.3%)
  survives. CKM angle running bounded to < 0.001%. See f_RG_formal_proof.py.
- f_hol = 1.000: **HONEST VALUE (v6.0)** — the confined-phase "derivation" below
  (Schur orthogonality → Cartan decomposition → C_ud = exp(-1/6) → f_hol = 0.948)
  requires an unproven confinement assumption; the one-loop effective potential
  actually destabilizes the ∞₃ vacuum for n_f ≥ 2, and every dynamical calculation
  that does not assume confinement gives ≈1.000 (no suppression). f_hol = 0.948 is
  therefore removed as a fitted number, not a derived one.

**v5.3 UPDATE:** f_RG corrected from 0.970 to 1.003. The previous -3% KK threshold
was WRONG — it violates ∞₃ symmetry. Rigorous computation in f_RG_kk_threshold.py
shows: KK threshold = 0 (∞₃ protection), CKM running < 10⁻⁵, EW matching = +0.3%.
Without f_hol (honest): η̄ = 0.391 ± 0.030 → 1.4σ from PDG (still consistent).

**v5.2 UPDATE:** f_Berry = 1.000 exactly (NOT 0.975). Berry phase vanishes
for real Mathieu ground states: ⟨p⟩ = 0 by parity, Bargmann invariant = 0
for real wavefunctions. See scripts/berry_phase_exact.py for proof.

---

## Table of Contents

1. Base Calculation Review
2. Factor 0.948: Holonomy Correction to CP Phase
3. Factor 0.975: Berry Phase Correction
4. Factor 1.003: RG Running Correction (v5.3 corrected from 0.970)
5. Combined Result and Uncertainty Analysis
6. Physical Interpretation

---

## 1. Base Calculation Review

### 1.1 Origin of eta-bar from Helix Chirality

In the STUR ∞₃ helix framework, CP violation arises from the spontaneous breaking of CP symmetry by the helix vacuum configuration:

```
R-field doublet: R = (R_1, R_2) = v(cos(phi), sin(phi))

Helix vacuum: phi(X) = 2pi X / (3 L_X)

Under CP: phi -> -phi

Since phi_vac != 0, CP is spontaneously broken.
```

### 1.2 The CKM Phase delta

The CKM CP-violating phase delta_CKM emerges from the geometric structure. The base calculation (Derivation D in DERIVATION_CHAIN_INFINITY.md) gives:

```
delta_CKM = theta_chi + delta_tb x f_screen
          = 26.57 deg + 60 deg x 0.696
          = 68.3 deg  (was 66.8 deg with undetermined f_screen = 0.67)
```

where:
- theta_chi = arctan(1/2) = 26.57 deg (helix chirality phase)
- delta_tb = pi/3 = 60 deg (holonomy interference for t->b transition)
- f_screen = 0.696 ± 0.006 (Debye-Waller screening, DERIVED in v5.1
  from |⟨ψ₀|e^{iθ}|ψ₀⟩| at α_eff = 1.480; see f_screen_first_principles.py)

### 1.3 Base eta-bar Calculation

From the unitarity triangle geometry:

```
eta-bar = sin(gamma) x R_t

where:
- gamma ~ delta_CKM ~ 67 deg (angle of unitarity triangle)
- R_t = |V_td V_tb*| / |V_cd V_cb*| ~ 0.85 (side ratio)
```

Direct calculation:

```
eta-bar_base = sin(67 deg) x 0.424
            = 0.921 x 0.424
            = 0.39
```

---

### 1.4 First-Principles Derivation of R_t

The quantity R_t = |V_td V_tb*| / |V_cd V_cb*| can be calculated from the helix geometry.

**Step 1: CKM Elements from Overlap Integrals**

From the infinity helix, the CKM matrix elements are:

```
V_ij = ∫ ψ_ui*(φ) ψ_dj(φ) dφ × (phase factors)
```

For generations separated by Δn sectors on the helix:

```
|V_ij| ∝ exp[-κ² Δn² / 8] × f_boundary
```

**Step 2: Individual Elements**

```
V_ud: Δn = 0 → |V_ud| = 1 - λ²/2 ≈ 0.974
V_cd: Δn = 1 → |V_cd| = λ = exp[-κ²/8] × f_corr ≈ 0.225
V_td: Δn = 2 → |V_td| = A λ³ (1-ρ̄-iη̄) → |V_td| ≈ A λ³ √[(1-ρ̄)² + η̄²]
V_tb: Δn = 0 → |V_tb| ≈ 1
V_cb: Δn = 1 → |V_cb| = A λ² ≈ 0.041
```

**Step 3: Geometric Calculation of A**

The parameter A comes from the ratio of overlap integrals:

```
A = |V_cb| / λ² = (Y_23 / Y_12) / λ

From helix geometry with κ = 2.5:
Y_23 / Y_12 = exp[-κ²(2² - 1²)/8] / exp[-κ²/8]
            = exp[-3κ²/8]
            = exp[-2.34]
            = 0.096

But this assumes uniform localization. With generation-dependent enhancement:
A = 0.096 × (κ_eff/κ)² = 0.096 × (1.3)² × 2.1 = 0.81  [ARITHMETIC ERROR]
```

**Correction:** 0.096 × 1.69 × 2.1 = 0.3407, not 0.81 (verified independently). The
document's stated result of 0.81 is the value needed to reproduce the target
|V_cb| = A λ² ≈ 0.041; the correctly-multiplied 0.3407 does not. This is a genuine,
unresolved arithmetic inconsistency: the "×2.1 enhancement" factor was evidently
chosen to land on A ≈ 0.81 rather than derived, and even that stated target does not
follow from the arithmetic shown. Downstream steps in this section continue to use
A = 0.81 (matching the phenomenological |V_cb|), so this error is flagged here rather
than propagated as a fix.

**Step 4: Geometric Calculation of |V_td|**

```
|V_td| = |V_us V_cb| × |1 - ρ̄ - iη̄|
       = λ × A λ² × √[(1-ρ̄)² + η̄²]
       = A λ³ × √[(1-ρ̄)² + η̄²]
```

From helix geometry, ρ̄ and η̄ are determined by the phase structure:

```
ρ̄ = cos(δ_CKM) × (overlap_ratio)
η̄ = sin(δ_CKM) × (overlap_ratio)

where overlap_ratio = |V_ub V_cb*| / |V_ud V_cd*| × (1/Aλ²)
```

**Step 5: R_t Calculation**

```
R_t = |V_td V_tb*| / |V_cd V_cb*|
    = |V_td| / (|V_cd| × |V_cb|)
    = A λ³ √[(1-ρ̄)² + η̄²] / (λ × A λ²)
    = √[(1-ρ̄)² + η̄²]
```

From the helix phase geometry with δ_CKM = 66.8° [STALE — §1.2 above updates
δ_CKM to 68.3°; this section was never recomputed with the updated value. Using
68.3°: sin(68.3°) = 0.9291 vs. sin(66.8°) = 0.9186 used below, a ~1% difference that
propagates into R_t, η̄_base, and every downstream number in this section. Flagged,
not silently recomputed here — see the v6.0 resolution note in the Executive
Summary, which uses the updated 68.3° value for the canonical result.]:

```
ρ̄_geom = 0.17  (from cos component of phase)
η̄_geom = 0.39  (from sin component of phase)

R_t = √[(1-0.17)² + (0.39)²]
    = √[0.689 + 0.152]
    = √0.841
    = 0.917
```

**Step 6: Corrected η̄ Formula**

The standard Wolfenstein formula η̄ = sin(γ) × R_t uses a different parameterization.

In the helix framework, using the geometric R_t:

```
η̄_base = sin(δ_CKM) × (η̄_geom / R_t)
       = sin(66.8°) × (0.39 / 0.917)
       = 0.921 × 0.425
       = 0.391 ≈ 0.39
```

Alternatively, directly from the phase:

```
η̄ = Im(V_ud V_ub* V_cd* V_cb) / (A² λ⁶)

From helix: Im(phase product) = sin(δ_CKM) × A² λ⁶ × f_overlap
          = sin(66.8°) × (0.81)² × (0.225)⁶ × 0.65
          = 0.921 × 0.656 × 1.29×10⁻⁴ × 0.65
          = 5.07 × 10⁻⁵

η̄ = 5.07×10⁻⁵ / (0.656 × 1.29×10⁻⁴) = 5.07e-5 / 8.46e-5 = 0.599  [NOT 0.39]
```

**Correction:** the division as shown gives 0.599, not 0.39 — the "✓" in the original
was not a verified checksum. This alternative route to η̄_base does not actually
reproduce the 0.39 obtained in Step 6 above; the two derivations of the same quantity
disagree by roughly 50% once independently checked. Kept here unresolved rather than
papered over; it does not affect the headline chain, which is built on the Step 6
value.

---

This derivation shows η̄_base = 0.39 follows from the helix geometry with δ_CKM = 66.8° derived in Section 1.2.

This is 12% above the observed value. The following three corrections reduce it to the experimental value.

---

## 2. Factor 0.948: Holonomy Correction to CP Phase [SUPERSEDED — v6.0]

> **This section is retained for historical/audit transparency only.** The
> f_hol = 0.948 result derived below rests on an unproven confinement assumption
> (§7.3 admits: "not proved from first principles — one-loop V_eff destabilizes ∞₃
> for n_f ≥ 2"). Every dynamical calculation that does not assume confinement gives
> f_hol ≈ 1.000. The canonical script has been corrected to use f_hol = 1.000; the
> derivation below should be read as "what f_hol would be IF the unproven confinement
> assumption held," not as the value actually used in the current eta-bar prediction.

### 2.1 Physical Origin

The holonomy W = exp(i theta) around the compact dimension X fluctuates around its ∞₃ vacuum value theta_0 = 2pi/3. These quantum fluctuations affect the CP-violating phase.

### 2.2 Holonomy Fluctuation Variance

From HOLONOMY_AVERAGING_DERIVATION.md, the holonomy phase variance is:

```
<delta-theta^2> = [1/(m_theta L_X)^2] / C_2(SU(3))
```

where:
- m_theta ~ 0.1-0.15 M_KK (holonomy mass, loop suppressed)
- L_X ~ 1/M_KK (compact dimension size)
- C_2(SU(3)) = 3 (quadratic Casimir of SU(3))

### 2.3 Detailed Derivation of <delta-theta^2> = 1/3

**Step 1: Holonomy effective potential**

The one-loop effective potential from KK modes:

```
V_KK(theta) = -(pi^2/L_X^4) x (1/90) x sum_i (+/-1) d_i B_4(q_i theta/2pi)
```

where B_4(x) = x^4 - 2x^3 + x^2 - 1/30 is the 4th Bernoulli polynomial.

**Step 2: Holonomy mass from potential curvature**

```
m_theta^2 = d^2 V_eff/d theta^2 |_{theta_0}
          ~ (4 pi^2 / L_X^2) x g_s^2 x C_2(SU(3))
          ~ M_KK^2 x (0.1)^2 x 3
```

Therefore: m_theta ~ 0.17 M_KK

**Step 3: Quantum fluctuations**

The zero-mode variance from the harmonic oscillator ground state:

```
<delta-theta^2>_naive = 1/(2 m_theta L_X)
                      = 1/(2 x 0.17 x 2pi)
                      ~ 0.47 rad^2
```

**Step 4: SU(3) gauge constraint**

Physical states must be gauge-invariant. The Haar measure projection reduces fluctuations:

```
<delta-theta^2>_phys = <delta-theta^2>_naive / C_2(SU(3))
                     = 0.47 / 3
                     = 0.16 rad^2
```

**Alternative derivation using SU(3) path integral:**

The holonomy path integral with Haar measure:

```
Z = integral dtheta |Delta(theta)|^2 exp(-S_eff[theta])

|Delta(theta)|^2 ~ sin^2(theta/2) sin^2(theta/2 + pi/3) sin^2(theta/2 - pi/3)
```

This gives:

```
<delta-theta^2> = 1 / C_2(SU(3)) = 1/3 rad^2
```

### 2.4 Effect on CP Phase

The CP phase delta involves the interference of holonomy phases from different quark sectors. The effective CP phase is:

```
delta_eff = delta_base x <cos(delta-theta)>
```

For Gaussian fluctuations:

```
<cos(delta-theta)> = exp(-<delta-theta^2>/2)
                   = exp(-1/6)
                   = exp(-0.167)
                   = 0.846
```

However, this applies to the FULL phase. For eta-bar, which involves sin(delta), the correction is smaller because:

```
<sin(delta + delta-theta)> = sin(delta) x <cos(delta-theta)> + cos(delta) x <sin(delta-theta)>
                           = sin(delta) x exp(-<delta-theta^2>/2)  [since <sin(delta-theta)> = 0]
```

### 2.5 Correlation Between Generations

The relevant fluctuations for the CP-violating observable are CORRELATED between the u and d quark sectors. The differential variance:

```
<(delta-theta_u - delta-theta_d)^2> = 2 <delta-theta^2> x (1 - C_ud)
```

where C_ud is the correlation coefficient.

For quarks in the same SU(2)_L doublet:

```
C_ud = exp(-|phi_u - phi_d| / xi)
     = exp(-pi/3 / 2pi)  [for pi/3 separation and correlation length xi ~ 2pi]
     = exp(-1/6)
     = 0.846
```

Therefore:

```
<(delta-theta_u - delta-theta_d)^2> = 2 x (1/3) x (1 - 0.846)
                                    = 0.667 x 0.154
                                    = 0.103 rad^2
```

### 2.6 Holonomy Correction Factor

The holonomy correction to eta-bar:

```
f_hol = exp(-<(delta-theta_u - delta-theta_d)^2> / 2)
      = exp(-0.103/2)
      = exp(-0.052)
      = 0.949

Rounded: f_hol = 0.948 +/- 0.010
```

### 2.7 Summary Box: Factor 0.948

```
+------------------------------------------------------------------+
|  HOLONOMY CORRECTION FACTOR: f_hol = 0.948                       |
|                                                                  |
|  Physical origin: Quantum fluctuations of Wilson line around     |
|                   the compact dimension X                        |
|                                                                  |
|  Key calculation:                                                |
|    <delta-theta^2> = 1/C_2(SU(3)) = 1/3 rad^2                   |
|                                                                  |
|  Correlated fluctuation for CKM:                                 |
|    <(delta-theta_u - delta-theta_d)^2> = 0.103 rad^2            |
|                                                                  |
|  Correction factor:                                              |
|    f_hol = exp(-0.103/2) = 0.948                                |
|                                                                  |
|  Connection to ∞₃: The factor 1/3 comes from C_2(SU(3)) = 3,    |
|                    which is intimately connected to the ∞₃       |
|                    center of SU(3) color.                        |
+------------------------------------------------------------------+
```

---

## 3. Factor 1.000: Berry Phase Correction (ELIMINATED — v5.2)

**v5.2 UPDATE:** Exact computation proves f_Berry = 1.000, not 0.975.
The Berry phase vanishes identically for real Mathieu ground states.
See scripts/berry_phase_exact.py for the complete proof.

The original derivation below is INCORRECT — retained for historical reference
with corrections noted.

### 3.1 Physical Origin (INCORRECT — see v5.2 note above)

Fermions localized at different phases on the ∞₃ helix acquire Berry (geometric) phases when transported around the compact dimension. This modifies the effective CP-violating phase.

### 3.2 Berry Connection

For a fermion with wavefunction psi(phi) localized at phi_0 on the helix:

```
psi(phi) = N exp[-(phi - phi_0)^2 / (4 sigma^2)]
```

The Berry connection is:

```
A_phi = i <psi | d/d phi | psi>
```

### 3.3 Calculation of Berry Connection

For a Gaussian profile centered at phi_0:

```
<psi | d/d phi | psi> = integral d phi |psi|^2 x [-(phi - phi_0) / (2 sigma^2)]
                      = 0  (by symmetry around phi_0)
```

The Berry connection for a SINGLE fermion vanishes. However, the RELATIVE Berry phase between different fermion species is non-zero.

### 3.4 Relative Berry Phase for CKM

The CKM matrix involves the interference between up-type and down-type quark mass eigenstates. The Berry phase accumulated in the CKM element V_ij comes from the OVERLAP region between generations i and j.

Consider the Berry phase for the off-diagonal CKM element V_ub (which dominates the CP violation through eta-bar):

```
gamma_Berry = arg(<u | d/d phi | d> x <d | d/d phi | s> x <s | d/d phi | u>)
```

This is the geometric phase from the CLOSED LOOP: u -> d -> s -> u on the ∞₃ helix.

### 3.5 Explicit Calculation

For Gaussian profiles at phi_u = 0, phi_d = 2pi/3, phi_s = 4pi/3:

**Step 1: Adjacent overlaps**

```
<u | d/d phi | d> = integral d phi psi_u*(phi) (d/d phi) psi_d(phi)
```

Using psi_g(phi) = N exp[-(phi - phi_g)^2 / (4 sigma^2)]:

```
<u | d/d phi | d> = integral d phi [N exp(-(phi)^2/(4sigma^2))] x [N exp(-(phi-2pi/3)^2/(4sigma^2)) x (-(phi-2pi/3)/(2sigma^2))]

= -(pi/3) / (2 sigma^2) x exp[-(2pi/3)^2 / (8 sigma^2)] x (normalization)
```

For sigma = (2pi/3)/kappa with kappa = 2.5:

```
sigma = 2pi/7.5 = 0.838 rad

(2pi/3)^2 / (8 sigma^2) = (2.094)^2 / (8 x 0.702) = 4.38/5.62 = 0.78

exp(-0.78) = 0.458
```

**Step 2: Total Berry phase**

The three adjacent overlaps contribute:

```
gamma_Berry = 3 x arg[-(pi/3)/(2 sigma^2) x 0.458 x (phase factors)]
```

The phase factors from the ∞₃ structure:

```
e^{i x 0} x e^{i x 2pi/3} x e^{i x 4pi/3} = e^{i(0 + 2pi/3 + 4pi/3)} = e^{i x 2pi} = 1
```

**Step 3: Net Berry phase contribution**

The Berry phase contributes a phase shift to the CKM phase:

```
Delta-delta_Berry = gamma_Berry = 3 x arctan[Im/Re]
```

From numerical integration with the helix parameters:

```
gamma_Berry = -0.05 rad = -2.9 deg
```

### 3.6 Effect on eta-bar

The Berry phase shifts the effective CP phase:

```
delta_eff = delta_base + gamma_Berry = 67 deg - 2.9 deg = 64.1 deg
```

The effect on eta-bar:

```
eta-bar_Berry / eta-bar_base = sin(64.1 deg) / sin(67 deg)
                             = 0.899 / 0.921
                             = 0.976
```

Alternatively, treating as a multiplicative correction to the amplitude:

```
f_Berry = exp(gamma_Berry x cot(delta))
        = exp(-0.05 x cot(67 deg))
        = exp(-0.05 x 0.424)
        = exp(-0.021)
        = 0.979
```

Taking the average of these two approaches:

```
f_Berry = 0.975 +/- 0.005  ← INCORRECT (v5.2: f_Berry = 1.000 exactly)
```

**v5.2 CORRECTION:** Both approaches above use approximate Gaussian profiles.
Exact computation with Mathieu eigenstates shows the Berry phase is identically
zero because the ground states are real (even parity). See scripts/berry_phase_exact.py.

### 3.7 Alternative Derivation: Adiabatic Transport

When a fermion is adiabatically transported around the ∞₃ helix, it acquires a geometric phase:

```
gamma_adiabatic = integral_0^{2pi} A_phi d phi
```

For the helix configuration with R-field:

```
R(X) = v(cos(2pi X/(3 L_X)), sin(2pi X/(3 L_X)))
```

The connection induced on the fermion:

```
A_phi = (1/2) x (Y_L - Y_R) x (d phi / d X) x X
      = (1/2) x Delta-Y x (2pi / 3)
```

For the difference in hypercharge between left and right components:

```
Delta-Y = Y_L - Y_R = 1/6 - 2/3 = -1/2  (for up quarks)
Delta-Y = Y_L - Y_R = 1/6 - (-1/3) = 1/2  (for down quarks)
```

The relative Berry phase:

```
gamma_{u-d} = (1/2) x (1/2 - (-1/2)) x (2pi/3) = pi/3 x 1/2 = pi/6 = 30 deg
```

After screening by wavefunction overlap:

```
gamma_{u-d,eff} = gamma_{u-d} x f_overlap
               = 30 deg x 0.1
               = 3 deg
```

This is consistent with our previous estimate of ~3 deg.

### 3.8 Summary Box: Factor 1.000 (CORRECTED v5.2)

```
+------------------------------------------------------------------+
|  BERRY PHASE CORRECTION FACTOR: f_Berry = 1.000 (EXACT)          |
|                                                                  |
|  v5.2 CORRECTION: The Berry phase VANISHES for real Mathieu      |
|  ground states. The original claim of f_Berry = 0.975 was        |
|  incorrect.                                                      |
|                                                                  |
|  PROOF (three independent methods):                              |
|                                                                  |
|  1. Abelian Berry phase:                                         |
|     A = i⟨ψ|∂_λ|ψ⟩ = 0 because Mathieu ground states at θ₀=0  |
|     are real (even parity), so ⟨p⟩ = 0 exactly.                 |
|                                                                  |
|  2. Bargmann invariant:                                          |
|     γ_B = arg(⟨ψ₁|ψ₂⟩⟨ψ₂|ψ₃⟩⟨ψ₃|ψ₁⟩) = 0                   |
|     because all overlaps ⟨ψ_i|ψ_j⟩ are real for real ψ.         |
|                                                                  |
|  3. Numerical verification:                                      |
|     Abelian phase = 3.3×10⁻¹⁴ (machine zero)                   |
|     Bargmann arg = 0.0000° (exactly zero)                        |
|                                                                  |
|  IMPACT ON η̄ (version history):                                 |
|     v5.1: η̄ = 0.39 × 0.948 × 0.975 × 0.970 = 0.350 (0.09σ)    |
|     v5.2: η̄ = 0.39 × 0.948 × 1.000 × 0.970 = 0.359 (1.1σ)     |
|     v5.3: η̄ = 0.39 × 0.948 × 1.000 × 1.003 = 0.371 (0.75σ)    |
|     v6.0: η̄ = eta_base × 1.000 × 1.000 × 1.003 = 0.3947       |
|           (13.4% dev.) — f_hol=0.948 fitted override REMOVED   |
|           in v6.0; this row is the current canonical value      |
|                                                                  |
|  See: scripts/berry_phase_exact.py                               |
+------------------------------------------------------------------+
```

---

## 4. Factor 1.003: RG Running Correction (v5.3 corrected from 0.970)

### 4.1 Physical Origin

The CKM parameters are scale-dependent quantities. The helix calculation gives values at the KK scale M_KK, but observations are made at M_Z. The RG running from M_KK to M_Z modifies eta-bar.

### 4.2 Scale Hierarchy

```
M_KK = hbar c / L_X ~ 0.2 eV  (for L_X ~ 1 micron)

But effective flavor physics scale: M_KK^eff ~ v_EW = 246 GeV

Observation scale: M_Z = 91.2 GeV

GUT scale: M_GUT ~ 10^16 GeV
```

The relevant running is from the electroweak scale to M_Z, with threshold corrections at the KK scale.

### 4.3 Beta Function for CP Phase

The one-loop beta function for the CKM phase delta is:

```
d delta / d ln(mu) = (1 / 16 pi^2) x [y_t^2 - y_b^2] x sin(2 delta) x f(s_ij)
```

where f(s_ij) is a function of the mixing angles.

### 4.4 Detailed RG Calculation

**Step 1: Running of Yukawa couplings**

The top Yukawa dominates:

```
y_t(mu) = y_t(M_Z) x [1 + (3 y_t^2 / 16 pi^2) x ln(mu/M_Z)]^{-1}
```

At M_Z: y_t ~ 1.0

**Step 2: Running of eta-bar**

The parameter eta-bar = A^2 lambda^6 eta runs because A, lambda, and eta all run.

```
d eta-bar / d ln(mu) = eta-bar x [2 (d ln A / d ln mu) + 6 (d ln lambda / d ln mu) + (d ln eta / d ln mu)]
```

**Step 3: Individual running contributions**

From the Yukawa RG equations:

```
d ln lambda / d ln mu = (y_t^2 + y_b^2) / (32 pi^2) ~ 0.002 per e-fold

d ln A / d ln mu = -(y_t^2 - y_c^2) / (32 pi^2) ~ -0.002 per e-fold

d ln eta / d ln mu = (y_t^2 sin^2 delta) / (16 pi^2) ~ 0.003 per e-fold
```

**Step 4: Integration from M_GUT to M_Z**

Number of e-folds: ln(M_GUT/M_Z) ~ ln(10^16/10^2) ~ 32

```
Delta ln eta-bar = [2(-0.002) + 6(0.002) + 0.003] x 32 / 2  [factor 1/2 for average]
                 = [0.011] x 16
                 = 0.18
```

This gives:

```
eta-bar(M_Z) / eta-bar(M_GUT) = exp(-0.18) = 0.84
```

Wait - this is too large. The issue is that most of the running cancels between different contributions.

### 4.5 More Careful Analysis

The dominant effect is the running of the CP PHASE delta, not the full eta-bar:

```
d delta / d ln(mu) = -(y_t^2 - y_b^2) / (16 pi^2) x J / (c_12^2 c_13^2 c_23^2 s_13 sin delta)
```

For the SM:

```
d delta / d ln(mu) ~ -0.001 rad per e-fold
```

From M_KK^eff to M_Z (about 1 e-fold):

```
Delta-delta = -0.001 rad = -0.06 deg
```

This is TINY. The larger effect comes from **threshold corrections** at the KK scale.

### 4.6 KK Threshold Corrections

At the KK scale, integrating out KK modes shifts the effective CP phase:

```
delta_{threshold} = sum_n (delta_n / n^2) x exp(-n M_KK L_X)
```

For the first few KK modes:

```
delta_{threshold} ~ delta_0 x [1/1 + 1/4 + 1/9 + ...] x damping
                  ~ delta_0 x 1.64 x 0.02
                  ~ 0.033 delta_0
```

This gives a 3% shift in the CP phase.

### 4.7 Combined RG Effect

**Contribution 1: Phase running** (-0.1%)
**Contribution 2: KK threshold** (-3%)
**Contribution 3: Electroweak matching** (-0.5%)

Total:

```
eta-bar(M_Z) / eta-bar(M_KK) = 1 - 0.001 - 0.03 - 0.005
                             = 0.964
```

Adding uncertainty: f_RG = 1.003 +/- 0.003

**v5.3 CORRECTION:** The above estimate of 0.964 was WRONG. Rigorous computation
in f_RG_kk_threshold.py shows:
  - KK threshold correction = 0 (∞₃ symmetry protection, exact)
  - CKM angle running = negligible (< 10⁻⁵)
  - EW matching = +0.3% (A₅ exchange in box diagrams)
  - TOTAL: f_RG = 1.003 ± 0.003
The previous -3% KK threshold assumed non-universal corrections that violate
∞₃ symmetry. The ∞₃ charge assignment forces F_n(k) = Σ_c ω^{kc} log(m_n(c)/M_KK) = 0
for k ≢ 0 mod 3, so the CP-phase-relevant part vanishes exactly.

### 4.8 Alternative: Direct eta-bar Running

From the literature [Antusch et al., JHEP 0503 (2005) 024], the running of Wolfenstein parameters in the SM:

```
eta-bar(M_Z) / eta-bar(M_GUT) = 1.00 - 0.03(y_t^2/0.5) ~ 0.97
```

This confirms our estimate.

### 4.9 Summary Box: Factor 1.003 (v5.3 corrected)

```
+------------------------------------------------------------------+
|  RG RUNNING CORRECTION FACTOR: f_RG = 1.003 (v5.3)              |
|                                                                  |
|  Previous value: 0.970 (WRONG — see correction below)            |
|                                                                  |
|  Physical origin: Scale dependence of CKM parameters             |
|                   from M_KK to M_Z                               |
|                                                                  |
|  Rigorous computation (f_RG_kk_threshold.py):                    |
|    - KK threshold: 0% (∞₃ symmetry protection — EXACT)          |
|      F_n(k) = Σ_c ω^{kc} log(m_n(c)/M_KK) = 0 for k≢0 mod 3   |
|    - CKM angle running: < 10⁻⁵ (negligible)                     |
|    - EW matching: +0.3% (A₅ exchange in box diagrams)            |
|                                                                  |
|  Result:                                                         |
|    eta-bar(M_Z) / eta-bar(M_KK) = 1.003 +/- 0.003               |
|                                                                  |
|  Why old value was wrong:                                        |
|    The -3% "KK threshold" assumed non-universal corrections      |
|    to the CP phase from KK modes. But ∞₃ symmetry forces        |
|    these corrections to vanish for CP-odd observables.           |
+------------------------------------------------------------------+
```

---

## 5. Combined Result and Uncertainty Analysis

### 5.1 The Complete Correction Chain (v6.0 — f_hol override removed)

```
eta-bar_corrected = eta-bar_base x f_hol x f_Berry x f_RG
                  = 0.3947/1.003 x 1.000 x 1.000 x 1.003   [eta-bar_base ~ 0.3934,
                                                             see Executive Summary]
```

Step by step:

```
Step 1: eta-bar_base x 1.000 = eta-bar_base  (f_hol honest value, v6.0 — was 0.948 FITTED)
Step 2: x 1.000 = unchanged                  (Berry phase — NO correction, v5.2)
Step 3: x 1.003 = 0.3947                     (RG running — v5.3 corrected)
```

**v6.0 note:** the previous "Step 1: 0.39 x 0.948 = 0.370" is removed. f_hol = 0.948
was a fitted number (see §2 superseded banner and §7.3); the canonical script now
uses f_hol = 1.000, which is what every non-fitted dynamical calculation actually
gives.

### 5.2 Uncertainty Propagation

Individual uncertainties:

```
eta-bar_base: ~0.393 +/- 0.02 (5%)
f_hol:        1.000, exact (v6.0 — no longer a fitted parameter with its own error bar)
f_Berry:      1.000 +/- 0.000 (0%, exact — v5.2)
f_RG:         1.003 +/- 0.003 (0.3%) — v5.3 corrected
```

Combined relative uncertainty:

```
sigma_rel^2 = (0.05)^2 + (0.000)^2 + (0.000)^2 + (0.003)^2
            = 0.0025 + 0.000 + 0.000 + 0.000009
            = 0.002509

sigma_rel = 0.0501 = 5.0%
```

(v6.0 correction: the previous line used (0.015)^2 for the f_RG term, which
contradicted the f_RG uncertainty stated one line above it, 0.003. That mismatch is
fixed here; f_hol no longer carries a separate fitted uncertainty since it is not a
fitted parameter in v6.0.)

Absolute uncertainty:

```
sigma_abs = 0.3947 x 0.0501 = 0.0198 ~ 0.02
```

### 5.3 Final Result (v6.0 — honest, f_hol override removed)

```
+==================================================================+
|                                                                  |
|   FINAL RESULT: eta-bar = 0.3947 +/- 0.020  (v6.0)              |
|                                                                  |
|   Observed (PDG 2024): eta-bar = 0.348 +/- 0.010                |
|                                                                  |
|   Deviation (%): |0.3947 - 0.348| / 0.348 = 13.4%               |
|   Deviation (sigma): |0.3947-0.348| / sqrt(0.020^2+0.010^2)     |
|            = 0.0467 / 0.0224 = 2.1 sigma                        |
|                                                                  |
|   GRADE: D (13.4% deviation) — this is the honest result after  |
|   removing the f_hol = 0.948 fitted override.                   |
|                                                                  |
|   v5.2 NOTE: f_Berry correction eliminated (was 0.975, now 1.000)|
|   v5.3 NOTE: f_RG corrected from 0.970 to 1.003                 |
|     (KK threshold = 0 by ∞₃ symmetry; EW matching +0.3%)        |
|   v6.0 NOTE: f_hol override (0.948, fitted) REMOVED. Honest     |
|     value f_hol = 1.000 used throughout. Previously reported    |
|     values of 0.371/0.75sigma (with fitted f_hol) and 0.359     |
|     (stale v5.2 central value) are both superseded.             |
|                                                                  |
+==================================================================+
```

### 5.4 Decomposition Table

| Factor | Value | Uncertainty | Physical Origin |
|--------|-------|-------------|-----------------|
| eta-bar_base | ~0.393 | +/- 0.02 | Helix chirality + unitarity triangle |
| f_hol | **1.000** | **exact (v6.0)** | **Honest value — 0.948 fitted override removed; §2 kept for history only** |
| f_Berry | **1.000** | **exact** | **ELIMINATED (v5.2): Berry phase = 0 for real ψ** |
| f_RG | 1.003 | +/- 0.003 | RG running: KK=0 (∞₃ protection), EW +0.3% (v5.3) |
| **eta-bar_final** | **0.3947** | **+/- 0.020** | Combined result (v6.0: f_hol override removed) |

---

## 6. Physical Interpretation

### 6.1 Why the Corrections Reduce eta-bar (v6.0 update)

With both f_Berry and f_hol now equal to 1.000, only ONE correction factor
survives:

1. **Holonomy fluctuations (f_hol = 1.000, v6.0)**: The confined-phase "derivation"
   in §2 (which gave 0.948) is superseded — it depends on an unproven confinement
   assumption that the document's own §7.3 admits is contradicted by the one-loop
   effective potential (∞₃ destabilized for n_f ≥ 2). Every dynamical calculation
   that does not assume confinement gives f_hol ≈ 1.000, i.e. no suppression.

2. **Berry phase (1.000 — ELIMINATED v5.2)**: Exact computation shows the Berry phase vanishes for real Mathieu ground states. The Abelian Berry connection A = i⟨ψ|∂_λ|ψ⟩ = 0 by parity, and the Bargmann invariant is zero for real wavefunctions. This correction no longer contributes.

3. **RG running (1.003)**: v5.3 correction — the RG effect is negligible. KK threshold corrections vanish by ∞₃ symmetry. The only surviving effect is +0.3% from A₅ exchange in EW matching. Previous claim of 0.970 (top Yukawa driving η̄ down) was incorrect for the CKM CP phase.

### 6.2 Connection to the ∞₃ Structure

**f_hol = 1.000 (v6.0, honest value):**
- No suppression of the base prediction survives once the confinement assumption
  (needed for the 0.948 figure) is dropped.
- The §2 calculation showing <delta-theta^2> = 1/3 → f_hol = 0.948 remains an
  interesting IF-confined result, but is not used in the canonical prediction.
- The ∞₃ center of SU(3) may still be physically relevant to holonomy dynamics;
  what changed is only that the associated numerical suppression factor is not
  established, so it is not used to adjust the prediction.

**f_Berry = 1.000 (ELIMINATED v5.2):**
- Berry phase was expected from transport around the ∞₃ structure
- However, real Mathieu ground states have identically zero Berry phase
- This is because ψ(-θ) = ψ(θ) (even parity) → ⟨ψ|∂/∂θ|ψ⟩ = 0
- The Bargmann invariant also vanishes: all overlaps ⟨ψ_i|ψ_j⟩ ∈ ℝ

**f_RG = 1.003 (v5.3 corrected from 0.970):**
- KK threshold corrections VANISH by ∞₃ symmetry protection (exact)
- Only surviving effect: +0.3% from A₅ exchange in EW box diagrams
- Previous -3% KK threshold was incorrect (violated ∞₃ symmetry)
- See f_RG_kk_threshold.py for rigorous derivation

### 6.3 Falsification Criteria

The correction chain makes specific predictions that can falsify STUR:

1. **If improved measurements give eta-bar far from 0.3947:**
   The correction factors would need to change by more than 2 sigma.

2. **If the holonomy variance is found to differ from 1/3:**
   This would indicate SU(3) is not the relevant gauge group for the holonomy, falsifying the ∞₃-SU(3) connection.

3. **If Berry phase measurements in analogous systems give different values:**
   The geometric phase calculation could be tested in condensed matter analogs.

### 6.4 Comparison with Other Approaches

| Approach | eta-bar prediction | Fitting required |
|----------|-------------------|------------------|
| SM (fitted) | 0.348 (input) | Yes (eta-bar is fitted) |
| STUR base | ~0.393 | No |
| STUR corrected (v6.0, honest) | 0.3947 +/- 0.020 | No (f_hol override removed) |

STUR calculates eta-bar from first principles, but the v6.0 honest result deviates
from the observed value by 13.4% (Grade D), not the sub-1σ agreement previously
reported using the fitted f_hol = 0.948.

---

## 7. Conclusion

### 7.1 Summary of Derivations (v6.0)

We have derived three correction factors that modify the base STUR prediction for eta-bar:

1. **f_hol = 1.000 (v6.0, honest value)**: The confined-phase "derivation" in §2
   giving 0.948 depends on an assumption (∞₃ center symmetry preservation) that the
   document's own dynamical calculation contradicts (one-loop V_eff destabilizes ∞₃
   for n_f ≥ 2). With no dynamical mechanism established, f_hol = 1.000 (no
   suppression) is the honest value, and the previous 0.948 has been removed as a
   fitted override rather than a derived result.

2. **f_Berry = 1.000 (ELIMINATED v5.2)**: Exact computation proves the Berry phase vanishes for real Mathieu ground states. See scripts/berry_phase_exact.py.

3. **f_RG = 1.003** (v5.3 corrected from 0.970): From rigorous computation in f_RG_kk_threshold.py. KK threshold = 0 (∞₃ symmetry protection), EW matching = +0.3%. Previous -3% KK threshold was WRONG.

### 7.2 Final Result (v6.0 — resolved)

```
eta-bar = eta-bar_base x 1.000 x 1.000 x 1.003 = 0.3947

Observed: eta-bar = 0.348 +/- 0.010

Deviation: 13.4% (2.1 sigma using propagated theory uncertainty +/- 0.020) — Grade D
```

### 7.3 Significance (v6.0 — resolution of prior self-contradiction)

**This document previously carried an unresolved internal contradiction**, flagged by
independent audit: §2 presented f_hol = 0.948 as a confident multi-step "derivation,"
the v5.4 banner called it "CONDITIONALLY DERIVED," and the closing status block (this
section, prior revision) simultaneously called the same number "FITTED — not
derived" and noted that "all dynamical approaches give ≈1.000." That contradiction is
now resolved: **the fitted override has been removed.** The canonical script uses
f_hol = 1.000, consistent with every dynamical calculation that does not assume
confinement. The result is an honest downgrade of the eta-bar prediction from 0.371
(0.75σ, using the fitted 0.948) to 0.3947 (13.4% deviation, Grade D, using the honest
1.000) — a real change in the framework's reported closure, not merely a corrected
label.

The surviving, non-fitted corrections are:
- f_hol = 1.000 (v6.0 honest value — not fitted, not suppressed)
- RG running effects (f_RG = 1.003, DERIVED — v5.3, unaffected by this resolution)

**Formal status (v6.0):**
- f_RG = 1.003 ± 0.001: **PROVED** (f_RG_formal_proof.py). QCD KK threshold cancels in
  CKM by flavor universality — gluon corrections are generation-blind. Only A₅ exchange
  survives (+0.3%). CKM running bounded to < 0.001% (Jarlskog elements run by < 10⁻⁵).
- f_hol = 1.000: **HONEST VALUE, v6.0** — the confined-phase route to 0.948 in §2
  (f_hol_confined_derivation.py) requires an assumption (center symmetry preserved)
  that this document's own one-loop effective potential contradicts for n_f ≥ 2.
  f_hol = 0.948 is therefore a fitted number, not a derived one, and is no longer
  used in the canonical prediction.
- f_Berry = 1.000: **PROVED** (berry_phase_exact.py). Berry phase vanishes identically
  for real Mathieu eigenstates.

**Final eta-bar (v6.0): 0.3947, 13.4% deviation from PDG (Grade D).**

---

---

## 8. Cross-Reference: Wavefunction Tail Correction (f_tail)

### 8.1 Note on f_tail and η̄

The unified wavefunction tail correction factor f_tail primarily affects quantities that depend directly on inter-generation wavefunction overlaps, such as the Cabibbo angle λ. The η̄ parameter, being derived from the CP-violating phase δ_CKM and geometric factors, does **not receive a direct f_tail correction**.

**Why f_tail does not directly affect η̄:**

1. The base η̄ calculation (Section 1) depends on sin(δ_CKM) and the unitarity triangle geometry
2. The correction factors f_hol, f_Berry, and f_RG modify the phase and running, not the overlap integrals
3. The tail correction f_tail ≈ 1.019 addresses wavefunction normalization in overlap regions, which enters λ but not the CP phase itself

### 8.2 Indirect Effects

While f_tail does not directly modify η̄, there is an indirect connection through the CKM parameterization:

```
η̄ = η (1 - λ²/2)

where η = A λ² η̄_base × (correction factors)
```

If λ is corrected by f_tail, there is a small (~0.1%) indirect effect on η̄ through the (1 - λ²/2) factor. This is well within the 5.3% uncertainty on η̄ and does not change the excellent agreement with observation.

### 8.3 Summary

| Correction | Affects λ? | Affects η̄? | Reason |
|------------|------------|-------------|--------|
| f_tail     | **Yes** (directly) | No (negligible indirect) | Overlap integral correction |
| f_hol      | Yes | **Yes** | Phase fluctuations |
| f_Berry    | Yes | **Yes** | Geometric phase |
| f_RG       | Yes | **Yes** | Scale running |

---

## References

1. HOLONOMY_AVERAGING_DERIVATION.md - Complete holonomy variance derivation
2. DERIVATION_CHAIN_INFINITY.md - Base eta-bar calculation and ∞₃ framework
3. PDG 2024 - Experimental values for CKM parameters
4. Hosotani, Y. (1983) - Dynamical gauge symmetry breaking
5. Berry, M.V. (1984) - Quantal phase factors
6. Antusch et al., JHEP 0503 (2005) 024 - RG running of CKM parameters
---

**Document Status:** Updated v6.0 — f_hol fitted override (0.948) REMOVED; resolved
in favor of the honest dynamical value f_hol = 1.000. This closes the three-way
self-contradiction ("derived" in §2 / "conditionally derived" in the v5.4 banner /
"FITTED" in the prior version of this footer) that earlier audits flagged: the
document now states, consistently throughout, that f_hol = 0.948 is a fitted number
that has been removed, not a derived result that survives alongside a fitted label.
**Key Result:** eta-bar = 0.3947, deviating 13.4% from PDG 0.348 (Grade D)
**f_RG = 1.003 ± 0.001 PROVED** (flavor universality + A₅ exchange, f_RG_formal_proof.py)
**f_hol = 1.000 HONEST VALUE (v6.0)** — 0.948 was fitted, not derived, and is removed;
  the confined-phase route to 0.948 requires an assumption this document's own
  one-loop calculation contradicts (∞₃ destabilized for n_f ≥ 2)
**f_Berry ELIMINATED** — Berry phase vanishes for real Mathieu eigenstates
