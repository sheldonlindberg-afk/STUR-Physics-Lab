# GENESIS v10 Stage 10k: sensitivity of the predictions to the β input

**Script:** `scripts/genesis_v10k_beta_input_sensitivity.py` (`--cache DIR` reuses the transfers; the cold run takes about 70 minutes, mostly the T+E transfers)
**Status:** a sensitivity analysis, **not** a pre-registration. The registered files are imported, never modified, and their predictions stand as registered.
**Purpose:** to replace the argued statement "a lower β only rescales the amplitudes; the shapes are unchanged" with a computation.

## Inputs

| Label | β [deg] | Source |
|---|---|---|
| registered | 0.277 ± 0.057 | ACT+Planck joint, arXiv:2608.06480 |
| dust-mitigated | 0.277 ± 0.079 | same value at its 3.5σ dust-robust significance |
| ACT DR6 alone | 0.215 ± 0.074 | arXiv:2509.13654 |

## Method

Within each hypothesis, only the amplitude depends on the input:

- **STUR-B:** κ.
- **M3a:** A₀(δ), solved per phase by the registered rule. That rule requires A₀ ≤ 3 rad and takes the EB-weighted angle over ℓ = 50–1500.

The transfers are computed once per unit amplitude. **Linearity in the amplitude was gated, not assumed**, using exact transfers at the solved amplitudes. Every hypothesis was also gated against its registered numbers at the registered input.

## Gates (12/13 pass)

| Gate | Result |
|---|---|
| STUR-B: registered row reproduces Stage 10b κ, ratio, Δβ, σ(Δβ) and competitor Δχ² | PASS |
| **STUR-B linearity: exact-κ ratio equals the rescaled ratio, to 10⁻³** | **FAIL, 2.5×10⁻³** (see below) |
| M3a: registered row has 49 phases and A₀ = 1.4352–2.9311 rad (Stage 10c) | PASS |
| M3a: per-unit × A₀ reproduces the stored Stage 10c curves | PASS, 6×10⁻⁵° |
| M3a linearity: exact transfers at the solved A₀ equal per-unit × A₀ | PASS, 4.8×10⁻⁵° (5 cases) |
| M3a: β_eff(3000) range reproduces Stage 10c2 | PASS |
| M3a: ratio and Δβ ranges reproduce Stage 10c | PASS |
| EB+TB: a constant rotation gives zero inconsistency | PASS |
| EB+TB: estimator homogeneity (exact probe vs A₀ × per-unit) | PASS (4.6609 vs 4.6611) |
| EB+TB: registered row reproduces Stage 10h min/median/max | PASS (max deviation 0.005) |
| f-windows: `window()` reproduces Stage 10d's printed windows | PASS |
| C0: registered row reproduces Stage 10g | PASS |

**The failed gate is a finding.** Stage 10b built STUR-B at κ = 1° per unit ln t (β ≈ 10° at recombination) and rescaled the result. An exact build at each input's κ (~0.02–0.03°) gives a ratio that differs by 2.5×10⁻³ relative. That is about 1.5×10⁻⁴° in β_reio, far below σ(Δβ) = 0.044°. The 10⁻³ threshold was set before the run and is kept.

## Results

### STUR-B

| Input | κ [deg/ln t] | ratio | Δβ [deg] | LiteBIRD σ(Δβ) | LiteBIRD signal | Δχ² early-only | Δχ² late-only |
|---|---|---|---|---|---|---|---|
| registered | 0.02674 ± 0.00550 | 0.2308 | −0.2131 ± 0.0438 | 0.2114° | 1.01σ | 0.037 | 1.016 |
| dust-mitigated | 0.02674 ± 0.00764 | 0.2308 | −0.2131 ± 0.0609 | 0.2114° | 1.01σ | 0.037 | 1.016 |
| ACT alone | 0.02076 ± 0.00714 | 0.2308 | −0.1654 ± 0.0569 | 0.2114° | 0.78σ | 0.022 | 0.612 |

These quantities do not change with the input, to the precision shown:

- the ratio (relative change 2×10⁻¹⁶);
- Δβ/β;
- LiteBIRD's absolute σ(Δβ) (3.5×10⁻⁵).

The κ, Δβ and the detection significance scale with β. The Δχ² against competing histories scales as β². The dust-mitigated input changes only the uncertainties.

### M3a

| Input | admissible phases | δ [rad] | A₀ [rad] | ratio | Δβ [deg] | β_eff(3000) [deg] |
|---|---|---|---|---|---|---|
| registered | 49 | 0.524–2.618 | 1.435–2.931 | 0.983–1.093 | −0.0048 to +0.0258 | 0.079–0.568 |
| dust-mitigated | 49 | 0.524–2.618 | 1.435–2.931 | 0.983–1.093 | −0.0048 to +0.0258 | 0.079–0.568 |
| ACT alone | **55** | **0.393–2.749** | 1.114–2.997 | **0.962–1.116** | −0.0082 to +0.0249 | **−0.010 to 0.519** |

**The shapes are not unchanged for M3a.** A lower β lowers every phase's required A₀, so the A₀ ≤ 3 rad cap admits **6 more phases** (δ = 0.393–2.749 overall). Their shapes differ:

- the ratio range widens to 0.962–1.116;
- at one new phase, β_eff(ℓ = 3000) **changes sign** (−0.010°).

Each phase's own shape is invariant: it is linear in A₀, which the gate confirms. The *set* of predicted shapes is not.

### Drift-robust joint EB+TB (Stage 10h estimator, unlensed)

| Input | SO-like min / median / max | S4-like min / median / max |
|---|---|---|
| registered | 1.14 / 1.74 / 4.27σ | 4.18 / 6.48 / 16.53σ |
| dust-mitigated | 1.14 / 1.74 / 4.27σ | 4.18 / 6.48 / 16.53σ |
| ACT alone | 0.89 / 1.45 / 4.48σ | **3.24** / 5.49 / 17.11σ |

With the ACT-only input, the worst-phase S4-like significance falls from 4.18σ to 3.24σ. Smaller amplitudes and the newly admitted phases together cause the drop. The maximum rises, because the new phases include more strongly ℓ-dependent ones. The proposed criterion ("every admissible phase above 3σ at S4-class") **still holds**, with less margin.

### f windows (Stage 10d / 10g formulas)

| Input | C0 (lower / upper) | STUR-B (c_γ ≈ 0.02) | M3a light | M3a heavy |
|---|---|---|---|---|
| registered | 2.1e12 / 5.1e10 GeV: **none** | [1.4e10, 2.0e16] | [2.1e12, 6.9e15] | [8.7e9, 6.9e15] |
| dust-mitigated | same | same | same | same |
| ACT alone | 2.1e12 / 6.6e10: **none** | [1.1e10, 2.0e16] | [2.1e12, 6.7e15] | [8.7e9, 6.7e15] |

**C0 stays excluded for every input.** With the lower β its BBN upper bound rises only to 6.6×10¹⁰ GeV, still a factor of about 32 below the anisotropy lower bound.

## Verdict on the argued claim

"A lower β only rescales the amplitudes; the shapes are unchanged":

- **Holds for STUR-B.** The ratio, Δβ/β and LiteBIRD's σ(Δβ) are invariant to 10⁻¹⁶–10⁻⁵.
- **Fails for M3a.** The A₀ ≤ 3 rad cap makes the admissible-phase set depend on β: 49 → 55 phases at β = 0.215°, a wider ratio range, a sign change of β_eff(3000) for one phase, and S4-like worst-case EB+TB down from 4.18σ to 3.24σ.
- **The dust-mitigated input changes only the uncertainties**, in both hypotheses.
