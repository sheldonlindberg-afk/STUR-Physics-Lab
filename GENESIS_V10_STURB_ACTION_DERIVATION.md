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

1. **c_γ ≈ 0.020 is unnatural.** Anomaly matching gives c_γ = E/2, with E = Σ X_f N_c Q_f², so the smallest natural value is 1/2. At c_γ = 1/2 and phase rate ω, β_rec ≈ 7°, which is excluded. Either the phase rotates about 25× slower than ω, or the photon coupling is suppressed by a mechanism not yet identified.
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
