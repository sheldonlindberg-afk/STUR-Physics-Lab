# GENESIS v10 Stage 10n: Field-Normalization Bounds by Calculation

**Script:** `scripts/genesis_v10n_field_bounds.py` (about 15 min; **23/24 gates pass**, and the one failure is reported below)
**Date:** 2026-10-29
**Replaces:** the argued steps in `docs/GENESIS_V10D_FIELD_CONSTRAINTS.md` (the isocurvature hand estimate, the generic early-dark-energy fractions, and the A_CB units that had been inferred), and the C0 window in `scripts/genesis_v10g_hypothesis_ranking.py`.

Each bound below comes from a computation, using each hypothesis's own dynamics:

| Hypothesis | Dynamics used | c_γ |
|---|---|---|
| C0 | θ̇ = q/a³, normalized to β_now through the visibility function | 3 |
| M3a (registered) | θ = A₀ sin(ω ln t + δ), A₀ = 1.435–2.931 rad | 3 |
| STUR-B, Part C | complex W with ξ𝕋\|W\|², W″ + 3HW′ + 6ξH²W = 0, ξ = 146.2, \|W\| unpinned, f ≡ \|W(today)\| | 0.0201 |
| STUR-B-A2 (comparison only) | pre-registered rotation at constant f, θ̇ = ω/t | 0.0201 |

## [13] Bound conventions

- **ACT DR6 A_CB.** The search snippet of Eq. (7) in arXiv:2608.27458 gives C_L^αα = A_CB · 2π/[L(L+1)] × 10⁻⁴ rad², with A_CB < 0.15 at 95%. Some later papers quote it in deg² instead.
  - The convention is fixed by calculation. ACT's own quoted g < 4.9×10⁻²/H_I follows from the rad² reading (4.87×10⁻²/H_I, a 0.6% match) and not from deg² (8.5×10⁻⁴/H_I). Both gates pass.
  - The bound used in genesis_v10d and v10g, 0.15×10⁻⁴ rad², is therefore correct. No anisotropy bound changes.
  - arxiv.org was unreachable from this container (DNS), so the definition comes from search excerpts, cross-checked by the g consistency test.
- **Electron b₀.** The Kostelecký–Russell tables (arXiv:0801.0287) could not be opened. Searches give electron b̃ bounds of about 10⁻²⁹ GeV (Eöt-Wash re-analysis), with 5×10⁻³⁰ GeV in Heckel et al. 2006 (hep-ph/0606218).
  - M3a's b₀ ≤ 4.4×10⁻⁴¹ GeV (genesis_v10d) is about 10¹¹ below that.
  - The conclusion "no constraint" stands, but the specific b₀ table entry remains unconfirmed.

## [11] Energy-density history in CAMB

**Method.**
- **Representation.** Λ plus the component is folded into a tabulated w(a). It runs as a c_s² = 1 `DarkEnergyFluid`, or through PPF where the table crosses w = −1.
- **Lensing.** Linear lensing is used in every run, for consistency.
- **Fisher setup.** A Planck-like Fisher forecast uses TT/TE/EE over ℓ = 30–2500 (33/70 μK′, 7.3′, f_sky = 0.6, τ prior 0.007). It is marginalized over the six ΛCDM parameters and gives the 95% (1.96σ) bound on s = (f/M)².

**Gates.**
- The forecast reproduces Planck 2018: σ(n_s), σ(ω_b) and σ(H₀) are 0.95, 1.00 and 1.19× the Planck values.
- A fluid with ΔN_eff = 0.3 reproduces CAMB's own N_eff + 0.3 in θ* to 1.7×10⁻⁴.
- Derivatives are linear to better than 5%.

**Results.**

| Component | CMB bound | BBN bound (\|ΔN_eff\| < 0.3 / < 1) | Previously (v10d, generic EDE fraction) |
|---|---|---|---|
| M3a, A₀ = 1.435 | f < 1.23×10¹⁶ GeV (Ω_θ(z*) < 0.97%) | 2.3 / 4.3×10¹⁶ | 1.4×10¹⁶ |
| M3a, A₀ = 2.931 | f < 6.0×10¹⁵ | 1.1 / 2.1×10¹⁶ | 6.9×10¹⁵ |
| STUR-B-A2 | f < 1.77×10¹⁶ | 3.3 / 6.1×10¹⁶ | 2.0×10¹⁶ |
| C0 | negligible (at the BBN bound, Ω_θ(z*) = 3×10⁻¹⁶) | **5.15 / 9.4×10¹⁰** | 5.15×10¹⁰ (v10g) |

Marginalizing over ΛCDM weakens the tracker constraint by a factor of 4.2. The computed tracker limit, Ω_θ(z*) < 0.97%, happens to match the generic ~1% used in v10d. The edges move by 10–14%.

### STUR-B (Part C): a result the earlier argument missed

From the minisuperspace action (sympy-gated), the Friedmann equation is 3(M² + ξ|W|²)H² = |Ẇ|²/2 + ρ.

- **In an exact power-law era nothing changes.** For any constant friction the circular mode has |r|² = 6ξ exactly (sympy gate). The kinetic energy then cancels the ξ|W|² term identically, and H is unchanged.
- **The real background is not exactly power-law, so a residual survives.** The residual D = (H²/H²_std − 1)/x² plateaus through the radiation era at **D ≈ −1.3×10⁴ (z ~ 10⁵) to −1.8×10⁴ (BBN)**. It is converged to under 2% across rtol for a ≥ 10⁻⁷, and it is single-signed (H² is lowered).
- **An earlier gate in this script was wrong.** It treated the BBN value as numerical noise. The tolerance scan shows it is a physical plateau, and that gate was replaced.
- **BBN bound:** |ΔN_eff| = 1.1×10⁵ x², so **f < 3.95×10¹⁵ GeV**.
- **CMB bound:** f < 2.8×10¹⁵ GeV (spline template through PPF) to 4.5×10¹⁵ GeV (smooth degree-2 envelope through the fluid). The 39% spread is a template and dark-energy-model systematic. The window uses the conservative 2.8×10¹⁵.
- **Sensitivity to a counter-rotating admixture.** The registered STUR-B has ε = 0. An admixture of 10⁻³ (10⁻²) tightens BBN to f < 4.5×10¹² (1.4×10¹²) GeV.
- **Ġ/G today** (assuming local G_eff = 1/F, which is not derived for scalar-torsion gravity): with lunar laser ranging Ġ/G = (0.7 ± 3.8)×10⁻¹³ yr⁻¹, f < 1.4×10¹⁶ GeV. This is not binding.

## [10] Inflationary fluctuations and isocurvature

- **Mode functions in de Sitter.**
  - The massless mode freezes at (H/2π)², to 10⁻⁴ (gate).
  - With M3a's H²-scaled restoring mass m = 1.5ωH, and with Part C's m² = 6ξH² (both μ = 29.6), superhorizon power decays as a⁻³ (gate), down to about 10⁻⁷³ (H/2π)² after 55 e-folds.
  - In those cases there is **no anisotropic-birefringence and no isocurvature bound**. M3a's "light during inflation" case from v10d holds only if the restoring force is absent during inflation.
- **Shift-symmetric light histories (C0, STUR-B-A2).**
  - ρ depends on θ̇ only, and the computed superhorizon S scales as k² (ratio 3.999 for k → 2k, gate). It vanishes on superhorizon scales.
  - At STUR-B-A2's lower window edge, P_iso ~ 8×10⁻³⁵, negligible.
  - This replaces v10d's "no first-order energy perturbation" argument with a computation.
- **M3a, light case.**
  - The registered equation gives δρ/ρ = 2δθ/A₀ exactly (computed).
  - Treating the tracker as CDM-like in matter domination, with δθ = H_I/(2πf) and the Planck uncorrelated-CDI bound P_iso < 8.7×10⁻¹¹ (Planck 2015, k = 0.05 Mpc⁻¹; the Planck 2018 uncorrelated value was not found), gives f < 4.8×10¹⁶ (A₀ min) and 2.3×10¹⁶ (A₀ max).
  - This is weaker than the CMB energy bound, consistent with v10d's hand estimate of 3–6×10¹⁶.
  - The CDM-like mapping is an approximation: the tracker has w = 1/3 in the radiation era.

## Windows (f in GeV; upper edges at |ΔN_eff| < 0.3; lower edges from ACT anisotropy if light, otherwise NGC 1275 at 8×10⁻¹³ GeV⁻¹)

| Hypothesis | f_min | f_max | Window | Change vs v10d / v10g |
|---|---|---|---|---|
| C0 | 2.1×10¹² (anisotropy) | 5.15×10¹⁰ (BBN); 9.4×10¹⁰ at \|ΔN\| < 1 | **EMPTY** (gap ×22–41) | confirmed; also empty at \|ΔN\| < 1 |
| M3a, heavy during inflation (H²-scaled restoring force) | 8.7×10⁹ | 6.0×10¹⁵ – 1.23×10¹⁶ (CMB, by A₀) | **OPEN** | upper edge −13% (CMB Fisher replaces generic EDE) |
| M3a, light during inflation | 2.1×10¹² | same | **OPEN** | same; isocurvature computed, not binding |
| STUR-B, Part C | 5.8×10⁷ (NGC 1275) | 2.8×10¹⁵ (CMB, PPF; 3.95×10¹⁵ BBN) | **OPEN** | **new**: heavy during inflation, so no anisotropy lower edge. Upper edge from the computed H² residual; ε = 10⁻² would cut it to 1.4×10¹² |
| STUR-B-A2 (constant f, comparison) | 1.4×10¹⁰ | 1.77×10¹⁶ | OPEN | upper edge −12% |

**Gate that failed.** PPF and the c_s² = 1 fluid differ by 11% in f on the same tracker (1.37 vs 1.23×10¹⁶ GeV). The 5% threshold was set in advance and has not been changed. This is a dark-energy-perturbation modelling systematic. It affects only the Part C CMB number, which needs PPF; that number is quoted as a range for this reason.

## Remaining caveats

- **Bounds not confirmed from source:** the BBN threshold |ΔN_eff| < 0.3 (BBN+BK18 analysis; 1.0 conservative, Mangano & Serpico 2011) and the Planck 2015 isocurvature value.
- **Part C is computed on its minisuperspace background only.** Perturbation-level effects of the large effective Planck-mass shift ξx²|W|² at early times are not computed.
- **Fisher, not a likelihood.** All results are Fisher forecasts at the Planck-like noise level, not likelihood fits to Planck data.

Sources:
- [ACT DR6 anisotropic birefringence](https://arxiv.org/pdf/2608.27458)
- [BICEP/Keck XVII](https://arxiv.org/pdf/1705.02523)
- [Kostelecký & Russell tables](https://arxiv.org/pdf/0801.0287)
- [Heckel et al. 2006](https://arxiv.org/pdf/hep-ph/0606218)
- [LLR Ġ/G review](https://arxiv.org/pdf/2002.00095)
- [isocurvature bound quoted in arXiv:1806.06056](https://arxiv.org/pdf/1806.06056)
- [BBN N_eff (Mangano & Serpico)](https://arxiv.org/pdf/1103.1261)
- [BBN+BK18 ΔN_eff](https://arxiv.org/pdf/2210.14159)
