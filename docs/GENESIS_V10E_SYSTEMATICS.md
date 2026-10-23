# GENESIS v10 Stage 10e: Systematics for the STUR-B and STUR-M3a Tests

**Script:** `scripts/genesis_v10e_systematics.py` (5/5 gates pass). The first run takes about 10 minutes; reruns with `--cache` take seconds.
**Scope:** the three effects that `scripts/genesis_v10c_m3a_lshape.py` did not model, and what they do to the tests both hypotheses rely on.
**Registered files:** imported only, never modified, so every pre-registration code hash remains valid.

## (a) Lensing of an ℓ-dependent rotation

**Method.** Birefringence rotates the polarization at emission, so it acts on the *unlensed* E/B fields; lensing then remaps Q/U. In the curved-sky correlation-function method ([Challinor & Lewis 2005](https://arxiv.org/abs/astro-ph/0502425), `camb.correlations`), lensing acts linearly, with real kernels, on

- ξ₊ ↔ C^EE + C^BB
- ξ₋ ↔ C^EE − C^BB + 2i C^EB.

The imaginary part of ξ₋ therefore transforms exactly like its real part:

  C̃^EB = L₋[C^EB],  C̃^EE − C̃^BB = L₋[C^EE − C^BB].

L₋[X] is obtained by lensing an input with EE = X and BB = 0, then taking lensed EE − lensed BB.

**Gates.**
- L₋[C^EE] reproduces CAMB's own lensed EE − BB to 6.4×10⁻⁴ over ℓ = 30–3000.
- A constant rotation stays a constant rotation after lensing, to 2×10⁻¹⁵.
- The unlensed construction reproduces the lshape forecast's medians to 0.3%.

**Result.** The table gives the significance at which a flat rotation with a free angle is rejected if M3a is true (min / median / max over the 49 registered phases). The STUR-B column is a control.

| Experiment | Without lensing (lshape) | **Lensed** | STUR-B, lensed |
|---|---|---|---|
| LiteBIRD | 0.35 / 0.38 / 0.60σ | **0.35 / 0.38 / 0.59σ** | 1.01σ |
| ACT DR6-like | 1.01 / 1.19 / 2.13σ | **0.98 / 1.14 / 2.03σ** | 0.10σ |
| Simons Obs. LAT-like | 2.54 / 3.18 / 6.32σ | **2.38 / 3.03 / 6.03σ** | 0.23σ |
| CMB-S4-like | 8.11 / 11.31 / 25.94σ | **7.11 / 10.49 / 24.65σ** | 0.61σ |

Lensing smooths the decline and costs 5–12% of the significance. The CMB-S4-like worst case falls from 8.1σ to 7.1σ. The conclusions of the lshape forecast stand. Inputs above ℓ = 3000 are held at their ℓ = 3000 value, and the lensing input is band-limited at ℓ = 4000.

## (b) ℓ-dependent instrumental EB and foreground EB

Both are treated as nuisance templates that are fitted together with the flat rotation:

- **Beam-like drift of the effective polarization angle:** α(ℓ) = a·ℓ(ℓ+1)/2500². This is the small-ℓθ form of a cross-polar or beam-width mismatch.
- **Dust EB:** C^EB_dust = ρ C^EE_dust, with C^EE_dust ∝ ℓ^−2.42 (the shape only).

| Experiment | M3a, beam drift marginalized | M3a, dust EB marginalized | Drift that mimics M3a, a(ℓ = 2500) |
|---|---|---|---|
| LiteBIRD | 0.16 / 0.24 / 0.57σ | 0.34 / 0.37 / 0.59σ | −0.16° |
| ACT DR6-like | 0.29 / 0.47 / 1.14σ | 0.89 / 1.10 / 2.03σ | −0.11° |
| Simons Obs. LAT-like | **0.86 / 1.30 / 3.27σ** | 2.21 / 2.93 / 5.94σ | **−0.10°** |
| CMB-S4-like | **3.58 / 5.06 / 12.15σ** | 6.64 / 9.18 / 19.47σ | **−0.07°** |

**Instrumental.** A smooth drift in the effective angle calibration of about **0.07–0.10° between ℓ ≈ 300 and 2500** is largely degenerate with M3a's decline.
- When the drift is marginalized, Simons Observatory drops from 3.0σ to 1.3σ (median), and CMB-S4 drops from 10.5σ to 5.1σ (median; 3.6σ worst phase).
- That drift size is the same order as published detector-polarization-angle systematics. ACT optical modelling puts them at the tenth-of-a-degree scale ([arXiv:2403.00763](https://arxiv.org/html/2403.00763v2)). A CMB-S4 systematics talk lists a birefringence calibration systematic above 0.1° ([Verges 2024, unrefereed](https://cosmology.lbl.gov/talks/Verges_24.pdf)). SO finds that cross-polar beams raise EB mainly at high ℓ ([arXiv:2503.01791](https://arxiv.org/pdf/2503.01791)). Beam rotation also mixes E and B, which sets a floor on the bias ([arXiv:0903.1116](https://arxiv.org/pdf/0903.1116)).
- **Threshold:** the M3a shape test is decisive only if the *ℓ-dependence* of the angle calibration is known to ≲ 0.02° over ℓ = 300–2500, not just its mean. That is about 1/4 of the mimicking drift.

**Dust.** A falling C^EE_dust shape is nearly orthogonal to M3a's decline: marginalizing it costs at most about 12% of the significance. The mimicking amplitudes are therefore not meaningful, and dust EB is not a credible impostor for the decline. Dust EB itself has not been measured. It is modelled through filament misalignment, with |r^TB| of order 10⁻² ([Clark et al. 2021](https://arxiv.org/pdf/2408.06214); [arXiv:2205.13962](https://arxiv.org/pdf/2205.13962) fits dust EB amplitudes jointly with β, finding them consistent with zero). It matters for the *absolute* β, not for the shape test.

## (c) Faraday rotation and the achromaticity criterion

Rotation angle = RM·λ². Galactic RM at high latitude:
- median 0.0 ± 0.5 rad/m² toward the north Galactic pole and +6.3 ± 0.7 rad/m² toward the south ([Mitra et al. 2010](https://web3.arxiv.org/abs/1003.4519));
- scatter about 9 rad/m² ([Akahori et al. 2013](https://arxiv.org/pdf/1303.1595)).

| Band [GHz] | RM = 1 | RM = 6.3 | RM = 10 rad/m² | PMF rms, B = 4.4 nG |
|---|---|---|---|---|
| 40 | 0.0032° | 0.020° | 0.032° | 4.0° |
| 68 | 0.0011° | 0.0070° | 0.011° | 1.4° |
| 100 | 0.0005° | 0.0032° | 0.0052° | 0.63° |
| 140 | 0.0003° | 0.0017° | 0.0026° | 0.32° |
| 235 | 0.0001° | 0.0006° | 0.0009° | 0.11° |
| 402 | 0.00003° | 0.0002° | 0.0003° | 0.039° |

The script prints all 15 bands. Only the 40-GHz range edge and the 195–402 GHz centers are confirmed against sources. The intermediate centers are the standard LiteBIRD baseline but are unverified here ([arXiv:2302.05228](https://arxiv.org/abs/2302.05228)).

**Primordial magnetic fields.** These are stochastic with zero mean, so they add *anisotropic* rotation, not isotropic β.
- Rotation rms ≈ 1.6° B_nG (ν/30 GHz)⁻². This is a review's rescaling ([arXiv:astro-ph/0601570](https://arxiv.org/pdf/astro-ph/0601570)) of [Kosowsky & Loeb 1996](https://ar5iv.arxiv.org/html/astro-ph/9601055), whose own figure is about 1° at 30 GHz for 1 nG.
- Field limit: B₁Mpc < 4.4 nG ([Planck 2015 XIX](https://web3.arxiv.org/abs/1502.01594)).

**Quantitative criterion** (both STUR-B and M3a predict an achromatic β):
- Fit β(ν) = β₀ + β_F (ν/40 GHz)⁻².
- A ν⁻² term with |β_F| ≤ 0.032° (|RM_eff| ≤ 10 rad/m²) is Faraday-compatible. Anything larger, after subtracting a Galactic RM map, or any non-ν⁻² frequency dependence, excludes the achromatic hypotheses.
- Between the CMB channels (68–235 GHz), Galactic Faraday rotation can account for at most **0.010°**. A larger difference, beyond 3σ_combined, cannot be attributed to Faraday rotation. The gate confirms that 0.010° is below LiteBIRD's σ(β) of 0.02°.

## Not covered

- Anisotropic-birefringence constraints from PMFs, or from fluctuations of the R-phase (separate gap item).
- Component-separation residuals beyond the dust-EB template.
- Non-smooth instrumental ℓ-dependence (for example sidelobes).
