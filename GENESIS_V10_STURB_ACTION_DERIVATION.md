# Can STUR-B Be Derived from the STUR Master Action?

**Document Type:** Derivation audit
**Framework:** STUR v7.0 Master Action + GENESIS v10 Stage 10 (`scripts/genesis V10 Light Bird`)
**Date:** 2026-10-22
**Status:** NOT DERIVED from the Master Action as written (no-go shown). DERIVABLE from a minimal, CP-even two-term extension, with three open costs.
**Script:** `scripts/genesis_v10_sturb_action_audit.py` (runs in ~8 s; reuses the pre-registration's own background and LOS code)

---

## Summary

The GENESIS v10 pre-registration rests on two bridge assumptions:

- **A1:** β = κ Φ_R. The photon polarization angle follows the R-field phase.
- **A2:** dβ/d ln t = κ [1 + ε cos(…)]. The phase accrues linearly in log-time.

The outcome of the audit, assumption by assumption:

| Requirement | In the Master Action? | What it takes |
|---|---|---|
| A1: parity-odd photon coupling | No: there is no φ F F̃ term | Anomaly-induced term c_γ (α/4π) φ F F̃ from R-charged chiral fermions in the Yukawa coupling −y ψ̄ R ψ. It is CP-even, so ∞₃×CP allows it. |
| A2: log-time accrual | **No: forbidden by the action's own U(1)** | A non-minimal coupling (ξ/2) 𝕋 \|R\|² plus an unpinned, rotating doublet mode |

With that extension the derived accrual law is φ ∝ √(6ξ) ln a (log of the **scale factor**), not ln t. LiteBIRD cannot tell the two apart: the LOS ratio β_reio/β_rec moves from 0.213 to 0.234, and Δβ moves from −0.218° to −0.212°, which is 0.1σ.

## 1. The Master Action has a U(1) that forbids log-time accrual (Part A)

S = ∫d⁵x √−g [ ½|∇R|² − V(|R|) + χ|R|²∂_Xφ + α|R|𝕋 + L_matter ],  R = |R| e^{iφ}

Every term is invariant under φ → φ + const:

- the kinetic term and V(|R|) are U(1)-symmetric by construction;
- for constant |R|, χ|R|²∂_Xφ is a total derivative (it only counts the winding);
- α|R|𝕋 depends only on |R|.

Reduce to the homogeneous FRW zero mode, φ(t, X) = kX + θ(t), with 𝕋 = −6H². Then θ is cyclic and

  d/dt ( a³ |R|² θ̇ ) = 0  ⇒  θ̇ = Q / (v² a³)  (for |R| = v).

Log-time accrual needs θ̇ = w/t. Substituting with a ∝ tᵖ gives d p_θ/dt = v² w (3p − 1) t^{3p−2}. That vanishes only for p = 1/3, a stiff, kination-like era that is never realized after BBN. The sympy check is in the script.

**Consequence.** If the Master Action is taken literally and a photon coupling is added, essentially all of the rotation happens before reionization. The ratio is ≈ 0.000 and Δβ ≈ −β_rec.

## 2. The repo's Cauchy-Euler equation is not the FRW zero-mode equation (Part B)

`DERIVATION_CHAIN_INFINITY.md` §2.3b states, for matter domination:

  W'' + (1/t) W' + (ω/t)² W = 0  ⇒  W = sin(ω ln t/t₀)

Three problems with it:

1. **The friction term.** A zero mode in FRW has friction 3H = 3p/t, which is **2/t** in matter domination. With 2/t the solution is W = t^{−1/2} sin(√(ω² − ¼) ln t). The repo's 1/t corresponds to p = 1/3.
2. **The restoring term.** (ω/t)² ∝ H² is a non-minimal coupling ξ𝕋|R|². It does not appear in the Master Action, which has the non-analytic α|R|𝕋 instead.
3. **The interpretation.** W is a real amplitude. Its oscillation phase ω ln t is not the R-field angle φ. Only a *complex* (rotating) doublet mode converts it into φ.

There is also a small inconsistency inside the pre-registration itself. It uses ln λ = ln(3722/2705) = 0.31916, while the v7.0 exact value is 1/π = 0.31831. This has no effect at ε = 0.

## 3. The minimal extension that does give A1 and A2 (Part C)

  L_B = (ξ/2) 𝕋 |R|² + c_γ (α/4π) φ F F̃

**CP.** |R|²𝕋 is CP-even. φ is odd (R → R*), and F F̃ is odd, so φ F F̃ is even. Both terms therefore respect the ∞₃×CP symmetry that STUR uses for θ_QCD = 0. The *sign* of β is set spontaneously by the sign of the Noether charge Q, so STUR does not predict the sign. The obvious alternative, a derivative coupling ∂_μφ T^μ (which gives φ ∝ ln a), is CP-odd and therefore excluded by STUR's own symmetry.

**Dynamics.** For an unpinned complex mode, Ẅ + 3HẆ + 6ξH²W = 0. In a power-law era this gives

  W = t^{−(3p−1)/2} e^{iΩ_p ln t},  Ω_p² = 6ξp² − (3p−1)²/4.

The setup and numerical solution:

- **Fixing ξ.** Setting the matter-era rate equal to the chronomagnetic ω = 2π² gives **ξ = 146.2**.
- **Solving.** The equation was integrated exactly on the Planck 2018 background, from a = 10⁻⁶ to today.
- **Solver check.** It matches the local WKB rate to 2×10⁻⁵.

What the solution shows:

- **dφ/d ln a is era-independent** at 29.6 (≈ √(6ξ)) in the radiation era, the matter era and today. The rate per unit ln t is not: 14.8 in the radiation era and 19.7 in the matter era.
- **|R| decays as t^{−1/2}** in the matter era.
- **The ε of A2 arises naturally** from the elliptical part of the mode, but at **twice** the rotation frequency, not once as A2 assumes. The radiation-to-matter transition leaves only ε ~ 3×10⁻⁴.

## 4. Predictions on the pre-registration's LOS machinery (Part D)

All cases are normalized to β_rec = 0.277 ± 0.057°. LiteBIRD's σ(Δβ) is 0.05°.

| Accrual law | β_reio/β_rec | Δβ | vs 0 | vs pre-registered | c_γ needed |
|---|---|---|---|---|---|
| C0 Master Action (U(1), \|R\| = v) | 0.000 | −0.277° | 3.7σ | 0.8σ | free (Q) |
| C1 STUR-B as pre-registered (ln t) | 0.213 | −0.218° | 3.2σ | 0.0σ | 0.020 |
| **C2 derived: ξ𝕋\|R\|² rotating mode** | **0.234** | **−0.212°** | 3.2σ | 0.1σ | 0.020 |
| C3 ∂φ·T^μ (ln a, CP-odd, excluded) | 0.234 | −0.212° | 3.2σ | 0.1σ | free (g) |

What this means for the falsification criteria:

- **The Δβ test does separate STUR-B from late-only rotation or calibration error** (ratio 1, Δβ = 0) at 3.2σ.
- **It does not separate STUR-B from the Master Action as written** (ratio ≈ 0): the two are only 0.8σ apart. The pre-registered criterion "Δβ differs from −0.218° by > 3σ" can therefore exclude late-time rotation, but not early-only rotation.
- **The ln t vs ln a distinction is unobservable** at LiteBIRD precision. Updating the pre-registration to the derived law (C2) changes the headline Δβ by 0.006°.

## 5. Open costs of the extension (why this is not yet "derived from STUR")

1. **c_γ ≈ 0.020 is unnatural.** The chiral rotation gives c_γ = Σ X_f N_c Q_f² over R-charged Dirac fermions, so the smallest natural value is 1 (one charged lepton). At c_γ = 1 and phase rate ω, β_rec ≈ 14°, which is excluded. Either the phase rotates about 50× slower than ω, or the photon coupling is suppressed by a mechanism not yet identified. *(Corrected 2026-10-22: an earlier version said c_γ = E/2, smallest value 1/2, β ≈ 7°, 25×.)* STUR's own Yukawa gives c_γ = 8; see the addendum "β from the action, nothing fitted".
2. **|R| ∝ t^{−1/2} contradicts the pinned vacuum |R| = v**, which `stur_master_action_derivation.html` uses for Λ_tree = 0. The rotating mode must be a separate light doublet (for example a KK or winding mode), not the vacuum R itself. That identification is not derived.
3. **The rotating mode must have no color anomaly.** If the R-charged fermions carried color, φ G G̃ would make θ_QCD roll by about 200 rad since recombination, in conflict with the nEDM bound and with STUR's own "no axion" prediction (`stur_strong_cp_solution.html`). Only leptons, or color-vectorlike fermions, may carry R-charge.
4. **ξ ≈ 146 is a large non-minimal coupling.** Its origin in the TEGR-XCRM reduction is not derived either. The literature analogue is "teleparallel dark energy" (ξ𝕋φ²).

## 6. Related inconsistency found while reading the repo

The pre-registration's tensor prediction (GENESIS R², r = 0.0035 at N* = 55) disagrees with the repo's own canonical D-status value r_eff = 0.0139 from `scripts/stur_inflation.py`, which is chaotic inflation with XCRM torsion friction. At LiteBIRD's σ(r) ≈ 0.001 these differ by roughly 10σ. The project needs to choose one before the pre-registration hash is posted.

## Recommendation

Keep the A1 and A2 status in the pre-registration as "bridge hypothesis; not derived from the STUR action". That label is accurate. Two optional upgrades:

- record the C2 law (ratio 0.234, Δβ = −0.212 ± 0.044°) as the action-motivated variant, together with the extension L_B written above;
- add C0 (ratio ≈ 0) to the competing-explanations list, noting that LiteBIRD separates it from STUR-B at only about 0.8σ.

---

## Addendum (2026-10-22): Stage 10b full-Boltzmann run and the inflation decision

**Decision:** the pre-registration commits to **GENESIS R² inflation, r = 0.0035** (N* = 55). The r_eff = 0.0139 of `scripts/stur_inflation.py` is not used in this pre-registration.

`scripts/genesis_v10b_boltzmann.py` (Stage 10b) replaces Stage 10's simplified reionization line-of-sight calculation with exact CAMB 2.0.5 E-mode sources. All 5 of its validation checks pass. Pre-registration file: `scripts/genesis_v10b_preregistration.json`, SHA-256 `8dde755844ca7c2416a6618f4565bce815ea3fd8d9e9268492e509ebb2663018`. The Stage 10 file is unchanged; both stand.

| Quantity | Stage 10 (simplified) | Stage 10b (full Boltzmann) |
|---|---|---|
| κ [deg per unit ln t] | 0.02632 | 0.02674 ± 0.00550 |
| β_reio/β_rec | 0.213 | **0.231** (0.225–0.259 across ε, phase, t_c, τ, reionization width) |
| Δβ | −0.218 ± 0.045° | **−0.213 ± 0.044°** |
| LiteBIRD σ(Δβ) | 0.05° (quoted) | **0.211° (computed, at r = 0.0035)** |

**Why the computed σ(Δβ) is 4× the quoted value.** The quoted 0.05° (Sherwin & Namikawa 2021) assumes no primordial B-modes. GENESIS's own tensors add irreducible variance at ℓ = 2–10, exactly where β_reio is measured. The computed σ(Δβ) is 0.078° at r = 0, 0.142° at r = 0.001, 0.211° at r = 0.0035, and 0.352° at r = 0.0139.

**What LiteBIRD can decide, at r = 0.0035:**
- **Tensors:** r = 0.0035 at about 3.5σ. A measurement of r < 0.001 excludes GENESIS.
- **Overall rotation:** κ ≠ 0 from high-ℓ β. Sensitivity is 41σ with the angle calibration known, so in practice LiteBIRD's ~0.02° absolute calibration sets the limit.
- **Achromaticity:** β must be the same across all frequency bands.

**What it cannot decide:** whether the rotation builds up with log-time. With the calibration angle marginalized, the STUR-B Δβ is a 1.0σ signal. Late-only rotation or miscalibration sits 1.0σ away, early-only rotation 0.2σ, and accrual in ln a instead of ln t 0.0σ. The Δβ criterion is therefore stored as a consistency check, not a decisive test.

---

## Addendum (2026-10-22): β from the action, nothing fitted

`scripts/genesis_v10_beta_from_action.py` computes β with no free parameter. Every input comes from STUR:

- **c_γ.** STUR's fermion coupling (`ALPHA_PARAMETER_DERIVATION.md` §1.2) is L_Y = −y(ψ̄_L R₁ ψ_R + ψ̄_L R₂ γ⁵ ψ_R + h.c.) = −y|R| ψ̄ e^{iγ⁵φ} ψ. This is a chiral, axion-like coupling for every charged fermion. Removing the phase by a chiral rotation gives, through the ABJ anomaly, **c_γ = Σ N_c Q_f² = 8** over three generations, and a color coefficient **c_s = 3**.
- **Δφ.** The only log-time rate in STUR is the chronomagnetic **ω = 2π²**. That gives Δφ = ω ln(t₀/t*) = 207.7 rad since recombination.

| Fermion content | c_γ | Predicted β | EB-equivalent (mod 90°) | C_BB/C_EE | vs observed 0.277 ± 0.057° |
|---|---|---|---|---|---|
| **STUR Yukawa, all charged fermions** | **8** | **110.6°** | **19.7°** | **0.40** | **340σ** |
| leptons only | 3 | 41.5° | 41.1° | 0.98 | 717σ |
| one generation | 8/3 | 36.9° | 36.6° | 0.92 | 636σ |
| one charged lepton | 1 | 13.8° | 13.7° | 0.21 | 236σ |

The calculation averages the rotation over the recombination visibility function. Depolarization is negligible, with polarization fraction ≥ 0.997.

**Result.** The prediction derived from STUR's own ingredients is excluded by existing data:

1. **The angle is far too large.** β is about 400× too large, 340σ away from the measured value.
2. **It would make large B-modes.** Rotating E-modes into B-modes would give C_BB ≈ 0.4 C_EE, while observations require less than about 1%.
3. **It conflicts with STUR's strong-CP solution.** The same rotation would make θ_QCD roll by 1246 rad. That contradicts the neutron EDM bound and STUR's own claim of no axion.

Matching 0.277° would need the phase to rotate about 400× slower than ω (with c_γ = 8). The repo contains no mechanism for that. The Master Action as written (φ̇ = Q/v²a³) leaves Δφ set by an initial condition, so it makes no β prediction at all.

**Implication for the pre-registration.** The status "bridge hypothesis; not derived from the STUR action" in both pre-registration files remains accurate. In fact it is now stronger: the direct derivation from STUR's own ingredients gives a β that is already excluded. A STUR-based birefringence prediction needs a new element: either a reason the R-phase rotates about 400× slower than ω today, or a reason the anomaly coefficient is suppressed. That element must also remove the color anomaly.

---

## Addendum (2026-10-22): no-fit check of r, and a search for a suppression mechanism

### r (`scripts/genesis_v10_r_from_action.py`)

- **r = 0.0035 (pre-registered) is not a STUR output.** It assumes Starobinsky R² inflation. The STUR action has no R² (or 𝕋²) term, and f(𝕋) gravity does not propagate a scalaron.
- **`stur_inflation.py`'s r = 0.0139 is a calculation slip.** It rescales ε at fixed N. But its own friction β_H = 3 + 2π also stretches N(R). Done consistently, its model gives **r = 24/(β_H N) = 0.043** at N = 60 (0.047 at N = 55). Numerical integration confirms this, and the β_H = 3 limit reproduces 8/N. That value is above the BICEP/Keck bound of 0.036, so the model is excluded. Its n_s = 1 − 2/N claim is correct.

### Suppression search (`scripts/genesis_v10_phase_suppression.py`)

Only mechanisms built from structure already in the repo were tested. No numerical ratio was searched for to produce the required factor of about 400.

| Mechanism | c_γ | c_s | Result |
|---|---|---|---|
| M1: Z₃ generation R-charges sum to zero | 0 | 0 | β = 0 exactly. Strong-CP safe, but 4.9σ from the measured 0.277° |
| M2: only leptons carry R-charge | 3 | 0 | Rotation at ω gives β = 41°, excluded |
| M3: the R-phase **oscillates**, θ = A sin(ω ln t + δ), leptons only | 3 | 0 | Bounded excursion of order A instead of 207 rad: see below |

**M3(a), the repo's own equation (friction 1/t, constant amplitude):**

- **Amplitude.** β_now = 0.277° is reproduced with **A₀ = 1.45–2.72 rad**, an O(1) amplitude. The pre-set naturalness gate (A₀ ≤ 1 rad) still fails, and the threshold was fixed before the run.
- **Sign.** Only today's phases δ ≈ 0.5–2.1 rad give a positive β, so the measured sign of β selects the phase.
- **What it predicts.** The oscillating part averages out across each visibility window. Every photon then carries the same angle K·A₀ sin δ, so **β_reio/β_rec = 1.01–1.06 and Δβ = +0.004 to +0.016°**.

**M3(b), FRW friction (amplitude ∝ t^(−1/2)):**

- **Depolarization.** The amplitude at recombination is about 192× larger than today, so most phases depolarize the CMB heavily (polarization fraction 0.07–0.92).
- **Surviving phases.** Those that keep polarization above about 98.7% need A₀ ≈ 0.13–0.18 rad and give **ratio ≈ 0.01 to −0.08** (early-only-like).

**Conclusion.** The only STUR-internal mechanism that gives a natural size (M3a) predicts **no tomographic difference**, ratio ≈ 1. That is the opposite of STUR-B's pre-registered 0.231, and at LiteBIRD it is indistinguishable from late-time rotation or miscalibration. No mechanism found in the repo reproduces log-time accrual (ratio ≈ 0.23) with natural parameters.

M3 also has two requirements of its own:

1. A restoring force on the R-phase. This explicitly breaks the Master Action's U(1), as Part A shows.
2. R-charges for leptons only.

Neither is derived in the repo.

---

## Addendum (2026-10-22): STUR-M3a pre-registered alongside STUR-B (Stage 10c)

`scripts/genesis_v10c_m3a.py` produces `scripts/genesis_v10c_m3a_preregistration.json`, SHA-256 `d3008ee624930ae356f4cfe3c89f331d7cbae8628346c895a4dba37f44224638`. It records both STUR-B hashes. None of the three files replaces another.

**Hypothesis.**
- θ(t) = A₀ sin(2π² ln(t/t₀) + δ), with constant amplitude.
- Only leptons carry R-charge, so c_γ = 3 and c_s = 0.
- β = (c_γ α/2π)[θ(t₀) − θ(t_emit)].

**Rules fixed before computing.**
- A₀ ≤ 3 rad.
- A₀ is solved per phase so that the exact EB-weighted high-ℓ angle equals β_now.
- The predictions are the full ranges over all admissible phases.

**Admissible solutions.** 49 of 144 phases qualify: δ = 0.52–2.62 rad, with A₀ = 1.44–2.93 rad. Both gates pass.

| Prediction | STUR-M3a | STUR-B (Stage 10b) |
|---|---|---|
| β_reio/β_rec | 0.983 – 1.093 (τ ±1σ, reionization width: 1.05–1.07) | 0.231 |
| Δβ | −0.005 to +0.026° | −0.213 ± 0.044° |
| High-ℓ β_eff(ℓ) | ℓ-dependent, up to 0.07° from β_now (stored per phase) | flat (0.273–0.280°) |
| Depolarization at recombination | < 10⁻⁴ | negligible |
| Frequency dependence | none | none |
| QCD axion | none (c_s = 0 required) | not addressed |

**What LiteBIRD can and cannot decide** (Δβ, angle calibration marginalized, r = 0.0035):
- If STUR-B is true, M3a is disfavored at **1.0σ**.
- If M3a is true, STUR-B is disfavored at only 0.3σ.
- M3a vs miscalibration: 0.35σ.
- Δβ therefore cannot separate the two hypotheses decisively.

What does decide:
- an absolute high-ℓ β ≠ 0 (both hypotheses need this);
- achromaticity across frequency bands;
- the ℓ-structure of β_eff, which needs a dedicated forecast;
- no QCD axion, for M3a.
