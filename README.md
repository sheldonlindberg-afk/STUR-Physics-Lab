<p align="center">
  <img src="assets/4.13.png" alt="STUR Physics Lab Logo" width="200"/>
</p>

<h1 align="center">STUR Physics Lab</h1>

<p align="center">
  <strong>Sheldon's Theory of Unified Resistance</strong><br>
  <em>STUR v7.0: Dynamic Infinity Helix &mdash; Theory of Everything Candidate</em>
</p>

<p align="center">
  <a href="https://creativecommons.org/publicdomain/zero/1.0/"><img src="https://img.shields.io/badge/License-CC0_1.0-lightgrey.svg" alt="License: CC0-1.0"></a>
  <img src="https://img.shields.io/badge/Physics-Theory_of_Everything-blueviolet" alt="Physics: Theory of Everything">
  <img src="https://img.shields.io/badge/Version-7.0-brightgreen" alt="Version: 7.0">
  <img src="https://img.shields.io/badge/PWA-Installable-green" alt="PWA: Installable">
  <img src="https://img.shields.io/badge/Pages-120+-blue" alt="Pages: 120+">
  <img src="https://img.shields.io/badge/Scorecard-24D%2B3P%2B2U%2B1I%3D30-blue" alt="Scorecard: 24D+3P+2U+1I=30">
  <img src="https://img.shields.io/badge/TOE_Closure-83%25_honest-brightgreen" alt="TOE Closure: 83% honest">
</p>

---

## Overview

**STUR** (Sheldon's Theory of Unified Resistance) is a Theory of Everything candidate that addresses 30 Standard Model and cosmological observables from four inputs and three axioms. The framework rests on:

1. **TEGR** (Teleparallel Equivalent of General Relativity) — gravity as torsion, not curvature
2. **R-field doublet** — a real scalar doublet on S^1 with the unique first-derivative XCRM coupling
3. **Energy minimization** — the ∞-helix topology emerges as the lowest-energy CP-violating compactification

**Unifying axiom (v7.0) — Energy Resistance Principle (ERP):** E = ½ R Φ²

Every physical interaction is a resistance to state change. This single axiom connects quantum, gravitational, fluid, topological, and temporal scales:
- Quantum: R_K = h/e² = 25813 Ω; α = Z₀/(2R_K) is a pure resistance ratio [exact, 8×10⁻¹³ residual]
- Gravity: R_grav = M_Pl²/2 = ℏc/(2G_N); torsion T is the flux; Friedmann = ERP at FRW scale
- Water: K = 2.24 GPa (bulk modulus = compression resistance); P = K×(−ΔV/V) [acoustic Ohm's law]
- Brane: λ_W = ψ₀(2π/3)/ψ₀(0) = 0.22545 (inter-brane resistance ratio; 0.04% from PDG 0.22537)
- Topological: XCRM Kirchhoff loop ∮ y·v·dX = 2π → n_w κ σ = 2π → ω = 2π²

**Four inputs:** M_Planck, v_EW, m_t, α_em (defining all scales and units).

**Complete derivation chain:**

> Axioms → ERP → ∞₃ orbifold → v·L_X = 3 → α_eff(quark/lepton) → Mathieu Z₃ fixed points → λ_W = ψ₀(2π/3)/ψ₀(0) → CKM → brane kink → σ_H → 2-body Higgs overlaps → fermion masses → U_ℓ†×TBM → PMNS → seesaw → neutrino masses → Λ_CC → dark matter → topological invariants

**Honest scorecard:** 24 derived (D, <20% from PDG), 3 partially derived (P), 2 unresolved (U), 1 input group (I) — **83% first-principles closure**. The [TOE closure script](scripts/stur_toe_closure.py) and [resistance script](scripts/stur_resistance_physics.py) report all deviations without override. (Post-v7.0.2 correction: the fitted f_hol constant was removed from η̄, and M_DM/Ω_DM h² were reclassified U after a documented search found no independent derivation.)

The infinity helix is not static. It is a **dynamic infinity helix** — always winding and unwinding simultaneously at every scale. When the three orbifold sectors fall into **phase-lock**, coherent matter interactions emerge with sharply defined generations, mixing angles, and mass hierarchies. Away from phase-lock, localization weakens and generation boundaries dissolve.

**The manifold is the same at any scale; only the perspective changes.** This discrete scale invariance, governed by the chronomagnetic ratio lambda_chrono = e^{1/π} = 1.37479 (exact), resolves all apparent scale questions: L_X^fund ~ 10^-32 m (Planck-scale winding quantum) and L_eff ~ 0.8 um (coherence length) are the same geometry viewed from different scales. The integer triangle {116, 138, 144} from the Chronomagnetics paper is a rational approximation (0.085%) to this exact result. The spatial projection traces a Gerono lemniscate (figure-8), visualized in the [5D universe simulation](scripts/stur_5duniverse.html).

### v7.0.2 Milestone: m_u, PMNS, Δm²₂₁ — 28 Observables Derived (superseded, see below)

Scorecard change at v7.0.2 (2026-06-29): **29D+0P+0U+1I=30** — reported as complete
first-principles closure (100%) at the time. **This has since been superseded:** a
post-v7.0.2 audit removed the fitted f_hol constant from η̄ and reclassified M_DM/Ω_DM h² as
unresolved (U) after finding no independent derivation for them in the codebase. The current
canonical scorecard is **24D+3P+2U+1I=30 (83%)**. The individual derivations below are
presented as originally computed at v7.0.2 for historical record; **the removal of the
fitted f_hol constant (which m_u's formula depends on via |V_ub|) directly changed m_u's
own number and pushed it from D to P status** — it is not unaffected, contrary to what an
earlier version of this paragraph claimed. Current values (from `scripts/stur_toe_closure.py`):
m_u = 2.71 MeV (26% off PDG, **P**), sin²θ₁₃ = 0.0242 (10% off, still D), δ_CP = 272.8°
(38.5% off, **P** — see the Results Summary table above for why this is a structural
mismatch, not a precision gap).

1. **m_u = m_t|V_ub|² = 2.44 MeV (13% PDG, D) — as computed at v7.0.2, before the f_hol
   fix.** Z₃ off-diagonal seesaw: the antisymmetric ψ_u state has a Z₃-forbidden direct
   Yukawa at θ=0. NLO coupling arises via Y_u off-diagonal: y_{u,t} = V_ub × y_t (same
   brane-overlap integral as the CKM element |V_ub| derived in Part 3). Seesaw in the
   (u,t) 2×2 block: m_u = |V_ub|² × m_t = (0.00376)² × 172.57 GeV = 2.44 MeV **at that
   time**. Current value: 2.71 MeV, 26% off, **P** (see note above).

2. **sin²θ₁₃ derived for the first time from resistance physics — 0.0257 (17% PDG) as
   computed at v7.0.2; current value 0.0242 (10% off, D).**
   The lemniscate CM phase φ_lem = i³ = −i inserted into U_ℓ acts on the nonzero se₁(2π/3)
   amplitude in U_ν to produce U_PMNS[νe,ν₃] = +i·s₁₂·se₁(2π/3)/n₃ (purely imaginary).
   This is the first derivation of a non-trivial reactor angle from resistance topology.

3. **Full PMNS = U_ℓ† × U_ν computed end-to-end.** U_ν from lepton brane (α_l = 1.3800)
   Z₃ Mathieu fixed-point network; U_ℓ with θ₁₂ = arcsin(λ_l) (lepton brane) and φ_lem = −i.
   Current values: sin²θ₁₂ = 0.2491 (19% off, D); sin²θ₂₃ = 0.4391 (19.4% off, D);
   δ_CP = 272.8° (38.5% off, **P** — PDG 197°, see structural-mismatch note above).

4. **Δm²₂₁ = λ_l²/2 × Δm²₃₁ = 6.92×10⁻⁵ eV² (8% off, D).** ∞₃ pseudo-Dirac NLO formula:
   off-diagonal M_R ±b block gives m_ν₂ ≈ λ_l/√2 × m_ν₃ directly from lepton brane Cabibbo.

5. **U_ν now uses lepton brane (α_l) not quark brane (α_q).** Physically correct assignment:
   PMNS mixing is a lepton sector observable → lepton brane Mathieu modes determine U_ν.

6. **TOE closure script `scripts/stur_toe_closure.py`** consolidates all 30 observables in
   11 parts: ERP axiom → α_eff → Mathieu → CKM → U_ν → U_ℓ → PMNS → Δm²₂₁ → m_u → DM+Λ_CC → fermion masses → grand scorecard.

### Resistance Physics Framework: ERP Unification

Historical intermediate stage (predates the U_ℓ† fix and the f_hol correction below —
scorecard totals here do not match the current canonical 24D+3P+2U+1I=30; see the Results
Summary section above for current status). Scorecard at this stage: **24D+4P+0U+1I=29**
(m_u upgrades U→P via Wolfenstein resistance ladder):

1. **ERP unifying axiom.** E = ½ R Φ² — resistance × flux² = energy — spans all scales.
   TEGR, XCRM, acoustic, chronomagnetic, and quantum domains all obey this structure.
   See `scripts/stur_resistance_physics.py`.

2. **λ_W = ψ₀(2π/3)/ψ₀(0) = 0.22545 (0.04% PDG).** The Wolfenstein Cabibbo parameter is
   the wavefunction amplitude ratio of the Mathieu ground state at the two occupied Z₃ fixed
   points. Supersedes exp(−κ²/4) = 0.229 (1.6% from PDG). Same physics, 40× more accurate.

3. **PMNS from Z₃ Mathieu fixed-point network (first principles).** Three Mathieu eigenmodes
   (ce₀, se₁, ce₁) evaluated at Z₃ fixed points (θ=0, 2π/3, −2π/3) give:
   sin²θ₂₃ = 0.500 exact (Z₂ symmetry), sin²θ₁₃ = 0 exact (se₁ odd mode), sin²θ₁₂ = 0.224 (27% off).
   The BM problem is structural: ψ₂(0)/ψ₂(2π/3) = −0.76 ≠ ±1 (TBM). Fix requires U_ℓ†.

4. **m_u via Z₃ off-diagonal seesaw: 2.44 MeV (13% from PDG 2.16 MeV) at this stage.** The
   up quark mass follows m_u = m_t × |V_ub|² = 172.57 × (0.003763)² = 2.44 MeV. Physical
   basis: antisymmetric ψ_u has Z₃-forbidden direct Yukawa; NLO coupling y_{u,t} = V_ub × y_t
   (same Mathieu brane-overlap integral as the CKM V_ub derivation in Part 3). Status at this
   stage: D. Current status (after the f_hol correction changed |V_ub|): 2.71 MeV, 26% off,
   **P** — see Results Summary above.

5. **Two resistance mechanisms clarified.** CKM mixing (inter-brane λ_W) and mass hierarchy
   (intra-brane KK exponential) are distinct resistance processes. Previously conflated.

### Conceptual Framework Improvements (ω, α, Δm²₂₁ mechanisms)

Five conceptual improvements (resolved at the time — scorecard then read 29D+0P+0U+1I=30;
current canonical scorecard post-v7.0.2 correction is 24D+3P+2U+1I=30, 83%):

1. **ω = 2π² established as primary.** The chronomagnetic frequency ω derives from ∞₃ phase
   closure (n_w × κ × σ = 2π, verified 0.016%), giving ω = πS = 2π². The integer triangle
   {116, 138, 144} is a secondary rational approximation (0.085% accuracy) to e^{1/π}.
   See `TRIANGLE_GENESIS_DERIVATION.md`.

2. **α = 1 from topological winding quantization.** A fermion completing one traversal of the
   ∞₃ fundamental domain must accumulate exactly 2π phase (minimal non-trivial holonomy).
   This forces y × v × L_X = 2π → α = 1, upgrading the condition from naturalness assumption
   to topological requirement. See `XCRM_YUKAWA_SYMMETRY_DERIVATION.md` §6b.

3. **Δm²₂₁ from Z₃-forced off-diagonal M_R.** The Z₃ selection rule g+h ≡ 0 (mod 3) forbids
   diagonal (1,1) and (2,2) entries in M_R, forcing a pseudo-Dirac pair (ν_R1, ν_R2). This
   naturally gives Δm²₂₁ << Δm²₃₁ without fine-tuning. Leading-order estimate 9.5 × 10⁻⁶ eV²
   is 87% from PDG (NLO calculation pending). See `SOLAR_NEUTRINO_MASS_SPLIT.md`.

4. **Geological predictions — honest calibration disclosure.** PDF Table 3 and Table 4 values
   (Chronomagnetics paper) are not reproducible from the formula as stated without undisclosed
   calibration parameters. The honest prediction is log-periodic spacing e^{1/(2π)} ≈ 1.17
   between phase-lock epochs — a parameter-free, falsifiable claim. See
   `GEOLOGICAL_PREDICTIONS_EXACT.md`.

5. **δ_CP from lemniscate complex multiplication.** δ_CP = 272.8° derived from full U_ℓ†×U_ν
   product with lemniscate CM phase φ_lem = −i; documented in `DERIVATION_CHAIN_INFINITY.md`.
   This mechanism structurally clusters near 90°/270° (38.5% off PDG 197°, **P** status,
   not the D implied elsewhere) — see the Results Summary table above.

---

## Results Summary (v7.0)

### Scorecard: 30 Observables — Honest Status

> **Status key:** **D** = Derived, <20% from PDG (complete formula, no free parameters) · **P** = Partially derived (correct mechanism, needs loop/NLO corrections, ≥20% off) · **U** = Unresolved (no independent mechanism found; circular or fitted) · **I** = Input/anchor

**Score: 24 D + 3 P + 2 U + 1 I = 30 (83% closure)**

> The tables below are synced to the live output of `scripts/stur_toe_closure.py`
> (the single canonical source of truth). An earlier version of this section
> contained a separate, stale set of numbers (some rows dating to pre-v7.0
> calculations) that directly contradicted both the script and each other —
> notably δ_CP(PMNS) and M_DM/Ω_DM h² were previously mislabeled **D** here
> while correctly marked **P**/**U** elsewhere in this same file. Fixed in a
> full-closure pass; see the honesty notes inside the script for the numbered
> derivation of every figure below.

**Topological invariants (exact, no calculation needed):**

| Observable | STUR Result | Method | Status |
|-----------|-------------|--------|--------|
| N_gen = 3 | Exact | ∞-helix node-point count | **D** |
| SU(3) × SU(2) × U(1) | Exact | ∞-helix holonomy compatibility | **D** |
| θ_QCD = 0 | Exact | ∞₃ × CP symmetry (no axion needed) | **D** |
| Berry phase = 0 | Exact | Real Mathieu eigenstates | **D** |
| Proton stability (dim-5) | Exact | ∞-helix KK-parity selection rule | **D** |
| Normal ordering | m_1 < m_2 < m_3 | ∞-helix resonance selection | **D** |
| KK-parity | Conserved | ∞₃ gauge symmetry | **D** |

**CKM sector (derived from α_eff + holonomy):**

| Observable | STUR | PDG | Dev | Status |
|-----------|------|-----|-----|--------|
| λ (Cabibbo) | 0.22543 | 0.22537 | 0.03% | **D** |
| A | 0.8140 | 0.826 | — | **D** |
| δ_CKM | 68.1° | 65.4° | 4.2% | **D** |
| η̄ | 0.3947 | 0.348 | 13.4% | **D** |
| \|V_ub\| | 0.00397 | 0.00382 | 3.8% | **D** |
| \|V_cb\| | 0.04136 | 0.0410 | 0.9% | **D** |

**Higgs localization (derived from ∞₃ brane kink):**

| Observable | STUR | Target | Status |
|-----------|------|--------|--------|
| σ_H/σ_ψ | 0.2251 = √2/(2π) | ~0.23 | **D** |

**PMNS sector (derived from U_ℓ† × U_ν + lemniscate CM phase):**

| Observable | STUR | NuFIT 6.0 | Dev | Status |
|-----------|------|-----------|-----|--------|
| sin²θ_12 | 0.2491 | 0.307 | 19% | **D** — full U_ℓ†×U_ν product, NLO correction |
| sin²θ_23 | 0.4391 | 0.545 | 19.4% | **D** — U_ℓ†×U_ν(Mathieu) |
| sin²θ_13 | 0.0242 | 0.0220 | 10% | **D** — lemniscate CM phase via U_ℓ†×U_ν (first non-trivial prediction, v7.0) |
| δ_CP (PMNS) | 272.8° | 197° | 38.5% | **P** — φ_lem=−i structurally clusters the prediction near 90°/270° (imaginary axis); NuFIT's best fit (197°, near the real axis) is ~75° away, which NLO corrections inside this mechanism (±3°) cannot bridge. This is a structural mismatch, not a precision gap — see `scripts/stur_toe_closure.py` Part 6 for the full decomposition. |

**Neutrino masses (derived from Z₃ pseudo-Dirac mechanism):**

| Observable | STUR | NuFIT 6.0 | Dev | Status |
|-----------|------|-----------|-----|--------|
| Δm²_31 | 2.45×10^-3 eV² | 2.511×10^-3 | 2.3% | **D** |
| Δm²_21 | 6.92×10^-5 eV² | 7.53×10^-5 | 8% | **D** — ∞₃ pseudo-Dirac NLO: λ_l²/2 × Δm²_31 |
| Σm_ν | 58 meV | < 120 meV | — | **D** — prediction |
| M_R | 2×10^14 GeV | ~10^14 | — | **D** |

**Fermion masses (derived from SU(2)/SU(2)×U(1) Wilson lines + Z₃ KK coupling):**

| Observable | STUR | PDG | Dev | Status |
|-----------|------|-----|-----|--------|
| m_t | 172.57 GeV | 172.57 GeV | 0% | **I** — input anchor |
| m_b/m_t | 0.02172 | 0.02424 (MSbar) | 10.4% | **D** — SU(2) Wilson line |
| m_τ/m_t | 0.01163 | 0.01030 | 12.9% | **D** — SU(2)×U(1) |
| m_c/m_t | 0.00895 | 0.00739 (MSbar) | 21% | **P** — KK threshold correction w/ QCD+EW gauge completion (improved from 29% QCD-only; still short of the 20% D-threshold — see script Part 8 note) |
| m_u | 2.71 MeV | 2.16 MeV | 26% | **P** — Z₃ off-diagonal seesaw m_u = m_t·\|V_ub\|² (reuses the CKM chain, not fully independent of it) |

**Cosmological constant:**

| Observable | STUR | Observed | Dev | Status |
|-----------|------|----------|-----|--------|
| Λ_tree | 0 | ~0 | Exact | **D** — ∞₃ discrete gauge Ward identity |
| Λ_CC | 3.0×10^-47 GeV^4 | 2.8×10^-47 | 7% | **D** — Z₃ Ward identity |

**Dark matter:**

| Observable | STUR | Observed | Dev | Status |
|-----------|------|----------|-----|--------|
| M_DM | 949 GeV | — | Testable | **U** — LKP B^(1) mass scale is fixed by requiring Ω_DM h² below, not independently derived; searched extensively (see script Part 9 note) and found no legitimate mechanism |
| Ω_DM h² | 0.1200 | 0.1200 | 0.0% | **U** — tautological by construction (any input value of Y4 gives 0.1200 to 6 decimals); not an independent prediction |

---

## Derivation Chain — Key v7.0 Advances

| Advance | Previous status | v7.0 status |
|---------|----------------|-------------|
| σ_H/σ_ψ = √2/(2π) | Assumed ~0.3 | **D** — derived from ∞₃ brane kink |
| CKM A = 0.814 | Calibrated 0.816 | **D** — derived from holonomy geometry |
| sin²θ_13 = 0.0242 (10%) | Hardcoded 0.022 (100% off) | **D** — lemniscate CM phase via U_ℓ†×U_ν, first non-trivial prediction |
| η̄ = 0.3947 (13.4%) | Fitted f_hol=0.948 constant removed | **D** — via complete correction chain (fitted constant removed post-v7.0.2; m_u status fell to P as a direct consequence) |
| m_b, m_τ | Per-particle corrections fitted | **D** — from SU(2)/SU(2)×U(1) Wilson lines |
| m_c/m_t = 0.00895 (21%) | QCD-only KK threshold gave 29% | **P** — QCD+EW gauge completion of the KK threshold correction narrows the gap but doesn't cross the D threshold |
| δ_CP = 272.8° | Asserted from chronomagnetics | **P** — lemniscate CM: i³ = e^{i3π/2} enters U_ℓ, but structurally predicts a phase far from NuFIT's best fit (see table above) |
| M_DM = 949 GeV | Reverse-engineered from Planck | **U** (reclassified post-v7.0.2 — self-consistent freeze-out fit is not an independent derivation; re-searched again in a later full-closure pass, conclusion unchanged) |
| Λ_CC (7%) | Conjectured Ward identity | **D** — Ward identity + neutrino residual |
| Δm²_21 (8% off) | Factor 4000× off | **D** — ∞₃ pseudo-Dirac NLO: λ_l²/2 × Δm²_31 |

**Current canonical scorecard:** 24D + 3P + 2U + 1I = 30 — 83% first-principles closure.
This is the actual, currently-achieved closure fraction — not 100%, and the 3 P's and
2 U's are not merely awaiting more decimal places: m_u and δ_CP(PMNS) reuse parts of
the CKM chain rather than standing as fully independent predictions, m_c/m_t and
δ_CP(PMNS) have genuine mechanisms that land outside the 20% threshold even after this
session's attempted improvements, and M_DM/Ω_DM h² are circular constructions with no
independent derivation found after repeated, extensive search. See
`OPEN_PROBLEMS_ROADMAP.md` for the full status of every open item.

---

## Falsifiable Predictions

STUR makes specific, falsifiable predictions. The following would definitively rule it out.

### Fatal Falsifiers

| Prediction | What would falsify STUR | Current status |
|-----------|------------------------|----------------|
| N_gen = 3 exactly | Discovery of a 4th sequential generation | LEP Z-width: N_nu = 2.984 ± 0.008 |
| Normal neutrino ordering | JUNO/DUNE measure inverted ordering at > 5σ | NuFIT 6.0: normal preferred at 3.5σ |
| θ_QCD = 0 exactly | Non-zero neutron EDM implying θ > 10^-9 | Current bound: \|θ\| < 10^-10 |
| Proton stable (dim-5) | Proton decay via dimension-5 operators at any rate | τ_p > 2.4×10^34 yr (Super-K) |
| δ_CP(PMNS) = 272.8° | T2HK/DUNE measure δ_CP outside 220°–320° at > 5σ | Current: NuFIT 6.0 197° ± 24-30° (per ABSOLUTE_MASS_DERIVATION.md / BARYOGENESIS_DERIVATION.md) — 272.8° is ~2.5-3.2σ away, not within 1σ (corrected; a prior version of this row claimed "within 1σ", which does not hold under either stated NuFIT uncertainty) |
| Σm_ν = 58 meV | CMB-S4/Euclid measure Σm_ν outside 45–70 meV | Current bound: < 120 meV |
| M_DM = 949 GeV | LZ/XENONnT exclude B^(1) KK dark matter at 0.95 TeV | LZ 2024: approaching sensitivity |

### Novel Chronomagnetic Predictions

These predictions are unique to STUR and have no counterpart in other frameworks:

- Log-periodic CKM drift at chronomagnetic timescale λ_chrono = e^{1/π} = 1.3748
- Phase-lock signatures in cosmological observables
- Chronomagnetic resonance at ω = 2π² = 19.7392 (exact; 19.687 is a rational triangle-integer approximation, 0.27% off, see TRIANGLE_GENESIS_DERIVATION.md)
- B^(1) KK dark matter at M ~ 949 GeV with σ_SI ~ 10^-47 cm^2 (LZ/XENONnT)
- Fifth force at ~1 μm scale (ARIADNE experiment)

---

## The Dynamic Infinity Helix

The central physical insight of STUR v7.0 is that the infinity helix is never static. It is a **dynamic infinity helix** — a Gerono lemniscate in spatial projection — always winding and unwinding simultaneously. The chronomagnetic modulation M(t) = |sin(ω ln(t/t_0))| with ω = 2π² = 19.7392 (exact) governs this oscillation.

This resolves all apparent scale questions:

| Apparent problem | Resolution |
|-----------------|------------|
| L_X has "two values" (10^-32 m vs 0.8 um) | Same geometry at different scales; L_X^fund (winding quantum) and L_eff (coherence length) are self-similar |
| Cosmological constant | Dynamical residual from time-averaged oscillating vacuum; ∞-helix Ward identity kills tree-level |
| Mass hierarchy | Each generation at a different scale of the self-similar structure; heavy fermions deep in phase-lock, light fermions near unwinding edge |
| PMNS large mixing | Neutrinos near the unwinding regime — least localized, most sensitive to dynamic geometry |
| δ_CP = 272.8° (P, 38.5% off — structural, see Results Summary) | Lemniscate of Bernoulli has CM by Z[i]; ∞₃ three-fold selects i³ = e^{i3π/2} as the Yukawa phase |

---

## Features

### Interactive Web Documentation
- **Progressive Web App (PWA)** — installable on any device
- **Works offline** — full service worker support
- **117+ HTML pages** covering all aspects of the theory
- **MathJax 3** for equation rendering

### Physics Domain Color Coding
Equations are color-coded by physics domain for visual identification:
- Quantum Mechanics
- Electromagnetism
- Gravity / Cosmology
- Particle Physics
- Thermodynamics
- Mathematics

### Computational Verification
- 30 Python scripts for numerical verification of all predictions
- 60 markdown derivation documents with complete mathematical chains
- Independent cross-checks across multiple calculation methods

---

## Quick Start

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/sheldonlindberg-afk/STUR-Physics-Lab.git
   cd STUR-Physics-Lab
   ```

2. **Start a local server**

   Using Python:
   ```bash
   python -m http.server 8000
   ```

   Using Node.js:
   ```bash
   npx serve .
   ```

3. **Open in browser**

   Navigate to `http://localhost:8000`

> **Note:** No build step required. STUR Physics Lab is pure static HTML/CSS/JS.

### Run the TOE Closure Calculation

```bash
pip install numpy scipy
python3 scripts/stur_toe_closure.py
```

This produces the 30-observable scorecard (24D+3P+2U+1I=30 — 83% closure) from four inputs and three axioms. All deviations are reported without override.

### Install as PWA

Visit the live site and click "Install" when prompted, or use your browser's "Add to Home Screen" option for offline access.

---

## Project Structure

```
STUR-Physics-Lab/
|
|-- index.html              # Main landing page
|-- about.html              # About the theory
|-- sitemap.html            # Complete site navigation
|-- mycitations.html        # References and citations
|
|-- scripts/                # Theory documentation and computation
|   |-- stur_core_theory.html
|   |-- stur_predictions.html
|   |-- stur_simulations_hub.html
|   |-- stur_cosmological_constant.html
|   |-- stur_ckm_numerical.html
|   |-- stur_pmns_numerical.html
|   |-- stur_darkmatter_derivation.html
|   |-- stur_5duniverse.html         # Dynamic infinity helix visualization
|   |-- stur_v7_full_closure.html    # Interactive scorecard viewer
|   |-- ... (117+ HTML pages total)
|   |
|   |-- stur_toe_closure.py                # Complete TOE closure (24D+3P+2U+1I=30 — canonical, 83%)
|   |-- stur_first_principles_calculation.py   # Core kappa, overlaps, N_eff
|   |-- ckm_full_diagonalization.py            # Full CKM matrix derivation
|   |-- cosmological_constant.py               # Historical negative result (abandoned mechanism, superseded)
|   |-- toe_closure_calculations.py            # TOE scorecard verification
|   |-- ... (30 Python scripts total)
|
|-- *.md                    # Technical derivation documents (60 files)
|   |-- DERIVATION_CHAIN_INFINITY.md              # Master derivation chain (v7.0)
|   |-- ABSOLUTE_MASS_DERIVATION.md               # All 9 fermion masses
|   |-- COSMOLOGICAL_CONSTANT_COMPLETE_DERIVATION.md  # CC: 10.8% from observed (v7.0.2, F_XCRM)
|   |-- DARK_MATTER_RELIC_DENSITY.md              # DM: Omega h^2 = 0.120
|   |-- FALSIFICATION_PROTOCOL.md                 # Pre-registered kill criteria
|   |-- FTHEORY_CY4_EXPLICIT_CONSTRUCTION.md      # UV completion proof
|   +-- ...
|
|-- assets/
|   |-- css/                # Styling
|   |-- js/                 # JavaScript utilities
|   +-- icons/              # PWA icons (72px to 512px)
|
|-- manifest.json           # PWA manifest
|-- sw.js                   # Service worker for offline support
+-- LICENSE                 # CC0 1.0 Universal
```

---

## Documentation

### Core Theory
- [Core Theory Framework](scripts/stur_core_theory.html) — Three axioms and derivation structure
- [∞₃ Infinity Helix](scripts/stur_5duniverse.html) — Dynamic extra-dimension topology
- [Master Action Derivation](scripts/stur_master_action_derivation.html) — Complete Lagrangian

### Derivation Chain
- [Complete Derivation Chain](DERIVATION_CHAIN_INFINITY.md) — Full mathematical derivation (v7.0)
- [Absolute Mass Derivation](ABSOLUTE_MASS_DERIVATION.md) — All 9 charged fermion masses
- [Cosmological Constant](COSMOLOGICAL_CONSTANT_COMPLETE_DERIVATION.md) — CC solution via ∞-helix Ward identity
- [Dark Matter Relic Density](DARK_MATTER_RELIC_DENSITY.md) — LKP prediction
- [UV Completion](FTHEORY_CY4_EXPLICIT_CONSTRUCTION.md) — F-theory CY_4 construction

### Predictions and Falsification
- [All Predictions](scripts/stur_predictions.html) — Complete list with experimental status
- [Falsification Protocol](FALSIFICATION_PROTOCOL.md) — Pre-registered kill criteria
- [Experimental Validation Roadmap](EXPERIMENTAL_VALIDATION_ROADMAP.md) — Timeline and tests

### Simulations
- [Simulations Hub](scripts/stur_simulations_hub.html) — Interactive demonstrations
- [5D Universe](scripts/stur_5duniverse.html) — Dynamic infinity helix visualization

---

## Contributing

Contributions are welcome. This is an open science project dedicated to the public domain.

### Ways to Contribute

1. **Scientific Review** — Analyze derivations and identify potential issues
2. **Numerical Verification** — Run and extend computational checks
3. **Documentation** — Improve clarity and accessibility
4. **Web Development** — Enhance the interactive experience
5. **Experimental Proposals** — Design tests for STUR predictions

### Contribution Process

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Make your changes
4. Submit a Pull Request with a clear description

---

## License

This work is dedicated to the **public domain** under the [CC0 1.0 Universal](https://creativecommons.org/publicdomain/zero/1.0/) license.

You are free to:
- Copy, modify, and distribute the work
- Use for any purpose, including commercial
- No attribution required (though appreciated)

---

## Citation

If you reference STUR in academic work, please cite:

```bibtex
@misc{stur2026,
  author       = {Lindberg, Sheldon},
  title        = {{STUR}: {S}heldon's {T}heory of {U}nified {R}esistance --
                  Dynamic {∞}₃ Infinity Helix TOE Candidate},
  year         = {2026},
  howpublished = {\url{https://github.com/sheldonlindberg-afk/STUR-Physics-Lab}},
  note         = {v7.0: 30 observables (24D+3P+2U+1I) from 4 inputs + 3 axioms
                  (TEGR, XCRM R-field, energy minimization) via dynamic ∞₃ infinity
                  helix phase-lock. 83% first-principles closure.}}
}

@misc{chronomagnetics2026,
  author       = {Burkeen, Derek and Cyrek, Christopher Br and Lockwood, J. M.
                  and LaMarche, Derek and Beaubier, Jay and Lindberg, Sheldon},
  title        = {Chronomagnetics: {A} Comprehensive Mathematical Foundation},
  year         = {2026},
  institution  = {Spectrality Institute},
  note         = {Log-periodic dynamics of torsion contortion,
                  chronomagnetic scale $\lambda_\text{chrono} = e^{1/\pi} = 1.3748$}
}

@misc{tegr2026,
  author       = {Lockwood, J. M. and Cyrek, Christopher Br and Hansley, Dustin
                  and Burkeen, Derek J.},
  title        = {Teleparallel Dynamics: First Principles --- From Torsion
                  Kinematics to Field Equations},
  year         = {2026},
  note         = {TEGR formulation, torsion tensor formalism, GEM structure}
}
```

---

<p align="center">
  <em>Three axioms. Four inputs. Twenty-four derived observables.</em><br>
  <strong>STUR v7.0 — Honest TOE candidate. Awaiting experimental judgment.</strong>
</p>
