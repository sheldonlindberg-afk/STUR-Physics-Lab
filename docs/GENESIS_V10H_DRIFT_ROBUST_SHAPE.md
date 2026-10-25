# Stage 10h: a drift-robust test of STUR-M3a's ℓ-dependent β_eff

**Script:** `scripts/genesis_v10h_drift_robust_shape.py` (10/10 gates pass). The first run takes about 37 minutes. Reruns with `--cache` reuse the β_eff curves, and the T/E transfers via `<cache>_tb.npz`.
**Builds on:** Stage 10e (`genesis_v10e_systematics.py`), imported only. No registered file is modified.

## The problem

Stage 10e found that a beam-like drift of the effective polarization angle, α(ℓ) = a ℓ(ℓ+1)/2500², at about 0.1° between ℓ ≈ 300 and 2500, is largely degenerate with M3a's ℓ-dependent β_eff(ℓ). It cuts the SO-like median significance from 3.0σ to 1.3σ.

## Why most strategies cannot help

If every channel has a **free** drift amplitude, a cosmological shape common to all channels is reproduced exactly by equal drifts. The null models are nested: free per-channel drifts contain the equal-drift case. Splitting into channels with same-shaped drift templates therefore cannot raise the significance, and one gate checks exactly that. Only three things can break the degeneracy:

1. drift templates whose shape differs between channels;
2. priors on the drift amplitude, from an external calibrator;
3. an observable in which a rotation at emission and an instrumental angle act differently.

The third exists: **TB versus EB.**
- **An instrumental angle α(ℓ)** rotates the observed Q/U, so TE → TB and EE → EB rotate by the same α(ℓ).
- **A rotation at emission** rotates the E-mode *sources*, so TB is weighted by Δ_T·Δ_E and EB by Δ_E².
- **The consequence:** a rotation that varies in time across the recombination window gives β_TB(ℓ) ≠ β_EB(ℓ). No pure angle drift of any ℓ-shape can produce that difference.

## Method

- **Truth and null model.** The truth is M3a, for all 49 admissible phases with their registered A₀. The null model is a constant rotation plus nuisances.
- **Strategies (a)–(c).** Lensed EB as in Stage 10e. Same-sky joint covariance: shared cosmic variance, independent noise. Each channel gets its own α_c (free) and drift a_c, either free or with a Gaussian prior σ_a, in degrees of angle at ℓ = 2500.
- **Drift templates:**
  - quadratic, ℓ(ℓ+1)/2500²;
  - beam-shaped, 1 − exp(−ℓ(ℓ+1)σ_c²), with σ_c = FWHM_c/√(8 ln 2).
- **Strategy (d).** Unlensed EB and TB from exact CAMB T- and E-sources. An **independent angle α(ℓ) is fitted at every multipole**, using the full 2×2 EB/TB covariance (Cov(EB,TB) = C_TE·C_BB/ν). What remains is what no common angle can absorb.
- **Instruments.** SO LAT bands at 93, 145 and 225 GHz (2.2′, 1.4′, 1.0′), with noise in the ratio 8.2 : 8.9 : 21 μK′ ([arXiv:2405.01621](https://arxiv.org/pdf/2405.01621)). They are rescaled so the combination equals the 8 μK′ SO-like level of earlier stages. S4-like is the same, scaled to 2 μK′. ACT DR6-like is 18 μK′. All use f_sky = 0.4 and ℓ = 300–3000, and all are approximate.

**Gates.**
- Reproduces the Stage 10e single-instrument medians exactly: 3.03/1.30σ for SO and 10.49/5.06σ for S4, without and with drift.
- Free same-shape band drifts give ≤ the combined significance.
- A prior σ_a → 0 recovers the no-drift result.
- C_TT matches CAMB to 8×10⁻⁴, and C_TE to 3×10⁻⁴.
- A constant rotation gives EB = ½ sin 4β·EE and TB = sin 2β·TE to 7×10⁻¹⁵, and zero TB/EB inconsistency (< 0.01σ for S4).
- The re-solved A₀ reproduces the cached curves to 10⁻¹⁶°.

## Results

The flat rotation is rejected at these significances (min / median / max over the 49 phases):

| Strategy | SO-like | S4-like |
|---|---|---|
| EB, one channel, no drift (Stage 10e) | 2.38 / 3.03 / 6.03 | 7.11 / 10.49 / 24.65 |
| EB, one channel, free quadratic drift (10e baseline) | 0.86 / 1.30 / 3.27 | 3.58 / 5.06 / 12.15 |
| (b) 3 bands, free quadratic drifts | 0.70 / 1.11 / 2.74 | — |
| (b) 3 bands, free beam-shaped drifts | 0.65 / 1.09 / 2.71 | 2.90 / 4.44 / 11.54 |
| (a) + ACT DR6, free drifts | 0.91 / 1.39 / 3.44 | — |
| (a) + SO SAT (ℓ ≤ 300), free drifts | 0.86 / 1.30 / 3.27 | — |
| (a) SO LAT + S4, free drifts | — | 3.61 / 5.13 / 12.28 |
| (c) prior σ_a = 0.20° | 1.00 / 1.39 / 3.27 | 3.62 / 5.09 / 12.16 |
| (c) prior σ_a = 0.08° | 1.42 / 1.76 / 3.40 | 3.80 / 5.12 / 12.18 |
| (c) prior σ_a = 0.02° | 2.22 / 2.73 / 5.38 | 5.38 / 6.58 / 12.52 |
| **(d) EB + TB, free angle at every ℓ** | **1.14 / 1.74 / 4.27** | **4.18 / 6.48 / 16.53** |
| (d) with a toy TT foreground residual (D_ℓ = 10 μK² at ℓ = 3000) | 1.11 / 1.69 / 4.20 | 4.01 / 6.17 / 16.02 |
| (d) ACT DR6-like | 0.45 / 0.69 / 1.68 | |

**Calibration-prior width needed** (strategy c, quadratic drift):
- **SO-like, 3σ:** σ_a ≤ **0.007°** at the median phase. At the least favorable phase, 3σ is never reached, even with the drift fixed at zero, where the maximum is 2.38σ.
- **S4-like, 5σ:** no prior is needed at the median phase, which is already 5.06σ with the drift free. Every phase reaches 5σ only for σ_a ≤ **0.022°**.

For comparison, current angle-calibration precision is:
- Tau A: 0.33° measured;
- the SO requirement: 0.2° ([arXiv:2011.02449](https://arxiv.org/pdf/2011.02449));
- an expected systematic of 0.08° for SO's sparse wire grid ([arXiv:2512.19102](https://arxiv.org/html/2512.19102v1)).

These figures describe the *constant* angle. I found no published precision for its ℓ-dependence.

**STUR-B under the same treatment.**
- STUR-B's own TB/EB inconsistency is 0.05σ (ACT), 0.11σ (SO) and 0.33σ (S4): a consistent null.
- M3a against STUR-B plus a free angle at every ℓ: SO 1.18 / 1.74 / 4.19σ, S4 4.27 / 6.39 / 16.28σ.
- In lensed EB with drift, M3a against STUR-B plus α plus drift: SO 0.63 / 1.16 / 3.24σ, S4 2.72 / 4.49 / 11.94σ.
- STUR-B against a flat rotation plus drift: 0.14σ (SO) and 0.36σ (S4). Its high-ℓ curve is effectively flat.

So the drift treatment does not merge STUR-B into M3a. The two stay as separable as M3a is from a flat rotation.

## Conclusions

1. **More instruments or frequency bands do not help** while each one has a free drift. Beam-shaped templates differ too little between 1.0′ and 2.2′ to break the degeneracy; the significance falls slightly because the extra nuisances absorb a little more.
2. **A calibration prior on the ℓ-dependence of the angle works, but SO would need ≲ 0.007°.** That is roughly 10× better than any published calibrator, all of which constrain only the constant angle. For S4 the median phase needs no prior, but the least favorable phase needs σ_a ≤ 0.022°.
3. **The EB+TB test (d) is drift-proof.** It absorbs an instrumental angle of any ℓ-shape exactly, and it still detects M3a at **4.2–16.5σ for S4-like across every admissible phase**, and 1.1–4.3σ for SO-like. It is the only strategy here that is decisive for every phase without an external calibration of the angle's ℓ-dependence. Its remaining vulnerability is **leakage that is not a pure angle rotation**: T→P leakage and beam ellipticity can create TB and EB patterns of their own. These must be controlled with T–P cross-correlation nulls, such as stacking TB on bright sources and comparing TT×TB with TT×EB.

## Proposed falsification criterion (drift-robust)

Using the joint EB+TB power spectra over ℓ = 300–3000, fit an independent polarization-angle parameter in every multipole bin. This absorbs any instrumental angle drift and any constant rotation. Then compute the residual TB/EB inconsistency D² (Δχ² of the common-angle fit), after T→P and ellipticity leakage have been bounded by null tests.

- **STUR-M3a is excluded** if D² is consistent with zero, while the forecast for *every* stored admissible phase exceeds 3σ for that dataset (a CMB-S4-class survey: minimum 4.2σ).
- **STUR-M3a is supported** only if D² is significantly nonzero *and* its ℓ-pattern is consistent, within 3σ, with the stored TB/EB residual of at least one admissible phase.
- With SO-like sensitivity (median 1.7σ), the test is informative but not decisive. A null result there disfavors only the most favorable phases.

STUR-B is not tested by this criterion: it predicts D² ≈ 0, at most 0.33σ for S4.

## Not modelled

- Lensing in (d). In EB it cost 5–12%, and a similar reduction is expected here.
- Partial sky overlap between instruments.
- Temperature foregrounds beyond the stated toy residual.
- Leakage systematics that are not angle rotations.
- Noise levels, which are approximate.

## Corrected during this work

- The first run built STUR-B at κ = 1° per unit ln t, giving β ≈ 10° at recombination. That made the small-angle angle template fail and produced a spurious 48–122σ TB/EB "signal" for the STUR-B control. STUR-B is now built at the registered Stage 10b κ = 0.02674°. M3a results were unaffected.
- The first version of the band-splitting gate asserted equality with the combined channel. It is now the logically correct inequality (≤), because the null models are nested.
