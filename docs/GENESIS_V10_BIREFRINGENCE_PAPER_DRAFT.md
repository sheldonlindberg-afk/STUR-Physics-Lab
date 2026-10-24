# Pre-registered birefringence tests of two bridge hypotheses from a teleparallel scalar-doublet model

**Sheldon Lindberg**

*Draft, 2026-10-23. Not submitted. Prepared with AI assistance (Claude, Anthropic): the computations, audits and text were produced in an AI-assisted session and have not yet been independently reviewed. Items marked [PENDING: …] await results from parallel work. All references were checked against bibliographic records (2026-10-24); [3]'s journal is inferred from its DOI.*

---

## Abstract

We pre-register predictions for isotropic cosmic birefringence from two hypotheses motivated by STUR. STUR is a five-dimensional teleparallel model with a real scalar doublet R = |R| e^{iφ}.

Neither hypothesis is derived from the STUR action, and we show three results that make this explicit:

1. **The action forbids log-time accrual.** Its exact U(1) symmetry fixes a³|R|²φ̇ as a constant, so the phase cannot build up linearly in log-time.
2. **A no-fit derivation is already excluded.** Using the model's own chiral Yukawa (anomaly coefficient c_γ = 8) and its log-periodic rate ω = 2π², the predicted rotation is β ≈ 110°. Observation gives β ≈ 0.3°, so this is excluded by hundreds of σ.
3. **The model's inflationary r is not a model output.** Neither tensor-to-scalar ratio associated with it follows from the action without fitting.

We therefore register two explicitly assumption-based hypotheses:

- **STUR-B.** The phase accrues linearly in log-time, with one amplitude κ fitted to the measured β.
- **STUR-M3a.** The phase oscillates, θ = A₀ sin(2π² ln t + δ), and only leptons carry R-charge.

**Method.** We use exact CAMB E-mode sources with the rotation applied at emission, and Fisher forecasts with the instrumental polarization-angle miscalibration marginalized.

**STUR-B predictions.**
- β_reio/β_rec = 0.231 and Δβ = −0.213 ± 0.044°.
- At the assumed tensor amplitude r = 0.0035, LiteBIRD's calibration-free σ(Δβ) is 0.21°, four times the commonly quoted 0.05°. The reason is that primordial B-modes add irreducible variance at ℓ ≲ 10. The tomographic test is therefore weak (1.0σ).

**STUR-M3a predictions.**
- β_reio/β_rec ≈ 1, so there is no tomographic signal.
- The high-ℓ angle is ℓ-dependent. For the median phase it declines (0.277° → about 0.17° by ℓ ≈ 2500); across all admissible phases β_eff(ℓ = 3000) spans 0.079–0.568°, so some phases rise instead.
- A flat rotation would be rejected at 2.5–6.3σ by a Simons Observatory-like survey and 8–26σ by a CMB-S4-like survey. LiteBIRD gives 0.4–0.6σ.

All predictions are hashed and time-stamped before the relevant data are released.

---

## 1. Introduction

A parity-violating coupling of a pseudoscalar field φ to photons, L ⊃ (g/4) φ F F̃, rotates the plane of linear polarization by β = (g/2)Δφ along the photon's path [S. M. Carroll, G. B. Field & R. Jackiw, Phys. Rev. D 41, 1231 (1990); D. Harari & P. Sikivie, Phys. Lett. B 289, 67 (1992)]. In the CMB, an isotropic β converts E-modes to B-modes:

C_ℓ^EB = ½ sin 4β (C_ℓ^EE − C_ℓ^BB).

The leading systematic is an instrumental miscalibration α of the polarization angle, which this formula cannot separate from β.

**Current measurements.** Using Galactic foreground emission to calibrate α, Minami & Komatsu reported β = 0.35 ± 0.14° from Planck 2018 [1]. Eskilt & Komatsu reported β = 0.342 (+0.094/−0.091)° from WMAP and Planck combined, with no evidence of frequency dependence over 23–353 GHz [2]. The pre-registrations below use β_now = 0.277 ± 0.057° (4.8σ), from Eskilt's joint analysis of ACT and Planck [5]. That analysis uses its reported instrumental priors; its ACT-only reproduction gives 0.207 ± 0.073°, and a dust-mitigation robustness test excludes β = 0 at only 3.5σ (see §8). The ACT collaboration's own DR6 EB analysis reports a rotation of 0.20 ± 0.08° [6].

**Tomography.** The reionization bump (ℓ ≲ 10) and the recombination peaks probe the rotation accumulated since z ≈ 8 and z ≈ 1100 respectively. Their difference Δβ = β_reio − β_rec is immune to α. Sherwin & Namikawa forecast σ(Δβ) ≈ 0.05° for LiteBIRD-class experiments [3]. LiteBIRD's own forecasts for isotropic birefringence are given in [4].

**This paper.** We take a model with an angular degree of freedom, test whether birefringence follows from it, find that it does not, and then register two clearly labeled bridge hypotheses with full forecasts. We consider the negative results as important as the predictions.

## 2. The model, and what is and is not derived

STUR's Master Action on M⁴ × S¹ [repo: `scripts/stur_master_action_derivation.html`, eq. 2.5] is

S = ∫d⁵x √−g [ ½|∇R|² − V(|R|) + χ|R|²∂_Xφ + α|R|𝕋 + L_matter ],

where:
- V = λ/4 (|R|² − v²)²;
- 𝕋 is the teleparallel torsion scalar;
- R = |R|e^{iφ} is a real doublet.

The fermions couple to R through L_Y = −y(ψ̄_L R₁ ψ_R + ψ̄_L R₂ γ⁵ ψ_R + h.c.) = −y|R| ψ̄ e^{iγ⁵φ} ψ [repo: `ALPHA_PARAMETER_DERIVATION.md` §1.2]. This is a chiral, axion-like coupling.

The model also describes a log-periodic "chronomagnetic" mode with frequency ω = 2π² in ln t. It is governed by the equation W'' + W'/t + (ω/t)²W = 0 [repo: `DERIVATION_CHAIN_INFINITY.md` §2.3b].

**Not derived from the action:**
- a photon coupling φ F F̃;
- any source for the phase φ;
- the restoring term (ω/t)²;
- an R² inflaton.

Section 3 makes each of these precise.

## 3. No-go results

### 3.1 U(1) symmetry forbids log-time accrual

Every term of S is invariant under φ → φ + const. For constant |R| the χ term is a total derivative, and α|R|𝕋 depends only on |R|.

Reduce to the homogeneous FRW zero mode, φ = kX + θ(t), with 𝕋 = −6H². Then θ is cyclic and d/dt(a³|R|²θ̇) = 0.

Log-time accrual means θ̇ = w/t. Substituting with |R| = v and a ∝ tᵖ gives d p_θ/dt = v²w(3p − 1)t^{3p−2}. This vanishes only for p = 1/3, a stiff era that is not realized after BBN. The sympy check is in `genesis_v10_sturb_action_audit.py`.

With the action taken literally, θ̇ ∝ a⁻³: the rotation is effectively complete before reionization (β_reio/β_rec ≈ 0.02).

### 3.2 The chronomagnetic equation is not the FRW zero-mode equation

A zero mode in FRW has friction 3H, which is 2/t in matter domination. The repo's equation has 1/t, which corresponds to a ∝ t^{1/3}. With the correct friction, the solution is W = t^{−1/2} sin(√(ω² − ¼) ln t).

The restoring term is also not in the action. It corresponds to a non-minimal coupling ξ𝕋|R|².

### 3.3 No-fit β from the model's own ingredients

The chiral rotation ψ → e^{−iγ⁵θ/2}ψ generates, through the ABJ anomaly, the photon term θ N_c Q² (α/4π) F F̃ per Dirac fermion. Over three generations this gives:
- photon coefficient **c_γ = Σ N_c Q² = 8**;
- color coefficient c_s = 3.

Combined with a phase rotating at ω = 2π² per unit ln t, the phase advances by Δφ = 207.7 rad since recombination. The predicted rotation is then

β = c_γ α Δφ / 2π = 110.6°.

This is 19.7° when reduced modulo 90°, as an EB estimator would see it. The implications:
- **B-modes:** C_ℓ^BB/C_ℓ^EE ≈ 0.40.
- **Strong CP:** θ_QCD would roll by 1246 rad.

| Fermion content | c_γ | β | EB-equivalent | C^BB/C^EE | Tension |
|---|---|---|---|---|---|
| all charged fermions | 8 | 110.6° | 19.7° | 0.40 | 340σ |
| leptons only | 3 | 41.5° | 41.1° | 0.98 | 717σ |
| one charged lepton | 1 | 13.8° | 13.7° | 0.21 | 236σ |

The rotation is averaged over the visibility function, and depolarization is negligible. Matching the observed β would need the phase to rotate about 400× slower than ω, for which the model provides no mechanism (`genesis_v10_beta_from_action.py`).

### 3.4 The tensor-to-scalar ratio

Two tensor ratios are associated with the model; neither is an output of the action.

- **r = 0.0035.** This is Starobinsky R² at N* = 55. The STUR action is linear in 𝕋 and contains no R² term, so this value is an imported assumption.
- **r = 0.0139.** This comes from the repo's chaotic inflation with extra friction β_H = 3 + 2π. It rescales ε at fixed N, but the friction also stretches N(R). Done consistently, the result is r = 24/(β_H N) = 0.043 at N = 60. Numerical integration confirms this, and the standard-friction limit reproduces 8/N. That value exceeds the BICEP/Keck bound r < 0.036 [BICEP/Keck Collaboration, P. A. R. Ade et al., Phys. Rev. Lett. 127, 151301 (2021), arXiv:2110.00483]. The model's n_s = 1 − 2/N is unaffected (`genesis_v10_r_from_action.py`).

**Theory gaps** (`scripts/genesis_v10f_theory_gaps.py`). None is closed. (a) The Yukawa phase potential and the Z₃ twisted boundary condition leave the phase zero mode exactly flat; the potentials that do exist are static and give a fixed-frequency oscillation, not sin(ω ln t), which averages out of the CMB; a log-time form needs an H²-coupling such as ξ𝕋|R|², absent from the action. (b) The repo localizes quarks with the same R-Yukawa as leptons, so quarks carry R-charge: c_γ = 8, c_s = 3. M3a with these charges needs A₀ = 0.54–1.10 rad and makes θ_QCD oscillate by 3.2–6.6 rad, violating the neutron-EDM bound by ~10¹⁰. **M3a's assumption H2 therefore conflicts with the repo's own fermion localization.** (c) The background of inflation driven by |R| itself is parameter-free (ε_H = 15/(10N + 15) ≈ 0.024 at N = 60), but n_s and r cannot yet be computed: non-minimally coupled teleparallel scalars can lack linear scalar perturbations unless their coupling functions satisfy a special relation (Raatikainen & Räsänen, JCAP 12 (2019) 021), not shown for STUR.

## 4. Two bridge hypotheses

**STUR-B** (registered in Stages 10 and 10b):
- **A1.** β = κΦ_R: the photon angle tracks the accumulated R-phase.
- **A2.** dβ/d ln t = κ[1 + ε cos(2πu/ln λ + phase)], with ε = 0 as the baseline.
- **A3.** The rotation is isotropic and achromatic.
- **A4.** t_c ≪ t_rec.

κ is fitted to β_now.

**STUR-M3a** (registered in Stage 10c):
- **H1.** θ(t) = A₀ sin(2π² ln(t/t₀) + δ), with constant amplitude. This reads the repo's equation literally and requires a restoring force that explicitly breaks the action's U(1).
- **H2.** Only leptons carry R-charge, so c_γ = 3 and c_s = 0. This keeps θ_QCD = 0.
- **H3.** β = (c_γ α/2π)[θ(t₀) − θ(t_emit)].

**Rules fixed before computing:**
- A₀ ≤ 3 rad.
- A₀ is solved for each phase δ so that the exact EB-weighted high-ℓ angle (ℓ = 50–1500) equals β_now.
- The predictions are the full ranges over all admissible δ, with no selection afterwards.

Both hypotheses take the GENESIS R² value r = 0.0035 for the B-mode variance.

## 5. Methods

**Sources.** We take E-mode sources S_E(k, η) from the CAMB 2.0.5 Boltzmann hierarchy, with the Planck 2018 ΛCDM parameters (τ = 0.0544). The scalar sources come from a scalar-only run; enabling tensors in the same run returns sources that fail the C_ℓ^EE check.

**Rotation at emission.**

Δ_E,ℓ = N_ℓ ∫dη S_E cos 2β(η) j_ℓ(k(η₀ − η)),
Δ_B,ℓ = N_ℓ ∫dη S_E sin 2β(η) j_ℓ(k(η₀ − η)),

with N_ℓ = √((ℓ+2)!/(ℓ−2)!), and β_eff(ℓ) = ¼ arcsin(2C_ℓ^EB / C_ℓ^EE).

Grids:
- **Low ℓ (2–40):** 800 log-spaced k up to 0.03 Mpc⁻¹, and the full conformal-time history.
- **High ℓ:** linear k (Δk = 2×10⁻⁴), with η = 150–800 Mpc.

**Calibration.** κ, and A₀ for M3a, are set so that the EB-information-weighted β_eff over ℓ = 50–1500 equals β_now.

**Forecasts.** We use the C_ℓ^EB Fisher matrix with Gaussian variance ((C^EE + N)(C^BB + N))/((2ℓ+1) f_sky), including lensed and tensor B-modes. The miscalibration template 2α(C^EE − C^BB) is marginalized. Competing histories are compared by Δχ² with free amplitude and free α.

**Gates.** All passed:
- C_ℓ^EE matches CAMB to 2.2×10⁻³ at ℓ ≤ 40 and 3.0×10⁻² at ℓ ≤ 1500 (4×10⁻⁴ on the extended ℓ ≤ 3000 grid);
- a constant β is returned at every ℓ to 3×10⁻¹⁶;
- the age matches Planck 2018;
- the M3a amplitude solution is linear to 4×10⁻⁵°;
- the ℓ-shape forecast reproduces the registered curves to 6×10⁻⁵°.

## 6. Predictions

| | STUR-B (Stage 10b) | STUR-M3a (Stage 10c) |
|---|---|---|
| Fitted | κ = 0.02674 ± 0.00550° per unit ln t | A₀ = 1.44–2.93 rad, δ = 0.52–2.62 rad (49/144 phases) |
| β_reio/β_rec | 0.231 (0.225–0.259 over ε, phase, t_c, τ, reionization width) | 0.983–1.093 (1.05–1.07 over τ, reionization width) |
| Δβ | −0.213 ± 0.044° | −0.005 to +0.026° |
| High-ℓ β_eff(ℓ) | flat, 0.273–0.282° | ℓ-dependent: median phase 0.277° (ℓ≈135) → 0.237° (1536) → 0.169° (2499); at ℓ = 3000, 0.079–0.568° across phases |
| Frequency dependence | none | none |
| QCD axion | — | none (c_s = 0) |

For reference, Stage 10 (STUR-B with a simplified line-of-sight calculation) gave a ratio of 0.213 and Δβ = −0.218°. The full-Boltzmann result shifts Δβ by 0.005°.

## 7. Forecasts

**7.1 LiteBIRD tomography is limited by the model's own tensors.** σ(Δβ), with f_sky = 0.6, 2.2 μK-arcmin noise, a 30′ beam and α marginalized, as a function of r:

| r | σ(Δβ) | STUR-B Δβ significance |
|---|---|---|
| 0 | 0.078° | 2.7σ |
| 0.001 | 0.142° | 1.5σ |
| 0.0035 | 0.211° | 1.0σ |
| 0.0139 | 0.352° | 0.6σ |

At r = 0 our σ(Δβ) is consistent with [3] after scaling for sky fraction. At r = 0.0035, the competing histories differ from STUR-B by:
- late-only rotation or miscalibration: 1.0σ;
- early-only rotation: 0.2σ;
- ln a accrual: 0.0σ.

If M3a is true, STUR-B is disfavored at only 0.3σ. **The Δβ test is a consistency check, not a decisive test.**

**7.2 M3a's ℓ-shape is calibration-free and is decisive from the ground.** The table gives the significance at which a flat rotation with a free angle is rejected if M3a is true, over all admissible phases (min / median / max). Instrument parameters are approximate.

| Experiment | M3a | STUR-B control |
|---|---|---|
| LiteBIRD (ℓ ≤ 1000) | 0.35 / 0.38 / 0.60σ | 1.0σ |
| ACT DR6-like (18 μK′, ℓ 300–3000) | 1.0 / 1.2 / 2.1σ | 0.1σ |
| SO LAT-like (8 μK′) | 2.5 / 3.2 / 6.3σ | 0.2σ |
| CMB-S4-like (2 μK′) | 8.1 / 11.3 / 25.9σ | 0.6σ |

**7.3 Tests that decide both hypotheses:**
- an absolutely calibrated β ≠ 0 at high ℓ;
- achromaticity across frequency bands;
- for GENESIS R², detection of r = 0.0035 (about 3.5σ at LiteBIRD; r < 0.001 excludes it).

**Field normalization** (`scripts/genesis_v10d_field_constraints.py`). The decay constant f of the R-phase is not fixed by STUR, whose two VEVs (3/L_X ≈ 0.74 eV and ≈ 2×10¹⁶ GeV) are mutually inconsistent and both excluded for M3a (the first by the photon coupling, the second by an energy fraction Ω ≈ 0.02–0.085). Treating f as free, the allowed windows are: STUR-B with c_γ = 8, none (θ_QCD rolls); STUR-B with c_γ = 0.02, 1.4×10¹⁰–2.0×10¹⁶ GeV; M3a, from 2.1×10¹² GeV (light during inflation) or 8.7×10⁹ GeV (heavy) up to 6.9×10¹⁵ GeV. The upper edges come from early-dark-energy fractions (literature range 0.0036–0.021, not tracker-specific); the lower edges from ACT DR6 anisotropic birefringence or the NGC 1275 photon-coupling bound. The lepton CPT-odd coupling is ~10¹⁰ below laboratory reach.
**Anisotropic birefringence.** If the phase is light during inflation (H_I = 1.47×10¹³ GeV for r = 0.0035), δθ ≈ H_I/2πf gives a scale-invariant rotation spectrum; ACT DR6's A_CB < 0.15×10⁻⁴ rad² (95%) then sets the lower edge of f quoted above. (The A_CB unit convention was inferred from the paper's own conversion, matching to 2%, not read from its definition.)

## 8. Limitations

1. **Input robustness.** Every calibration depends on β_now = 0.277 ± 0.057° [5]. That value rests on the analysis's instrumental priors. With dust mitigation the detection drops to 3.5σ, and the ACT-only values are lower (0.207 ± 0.073° [5]; 0.20 ± 0.08° [6]). Because κ and A₀ scale linearly with β_now, a lower true β rescales the STUR-B and M3a amplitudes but not the predicted shapes (ratios, ℓ-dependence).
2. **Calibration weighting.** The M3a amplitude is fixed with LiteBIRD-like weights over ℓ = 50–1500. The measured β_now comes from ACT+Planck, which weight ℓ up to about 3000, where M3a's β_eff departs from flat. At the registered A₀, an ACT DR6+Planck-like analysis would measure β = 0.260–0.266° rather than 0.277° (−0.29 to −0.19σ of β_now; approximate noise models). This is recorded as a known limitation in the Stage 10c2 addendum; the registered predictions are not altered. STUR-B is unaffected because its curve is flat.
3. **Systematics not modelled:** lensing remapping of the EB pattern, foreground residuals, ℓ-dependent instrumental EB such as beam ellipticity, and the expected Faraday rotation used to judge achromaticity. Quantified in `scripts/genesis_v10e_systematics.py`. (a) Lensing, computed by lensing the rotated ξ₋ = EE − BB + 2iEB (gated: constant rotation preserved to 2×10⁻¹⁵), reduces the M3a shape significance by 5–12% (median SO-like 3.0σ, S4-like 10.5σ). (b) An ℓ-dependent instrumental polarization-angle drift of about 0.07–0.10° between ℓ ≈ 300 and 2500 is largely degenerate with M3a's shape; marginalizing it lowers the medians to 1.3σ (SO-like) and 5.1σ (S4-like). The shape test is decisive only if the ℓ-dependence of the angle calibration is known to ≲ 0.02°. Dust EB (∝ ℓ^−2.42) costs at most 12%. (c) For |RM| ≤ 10 rad m⁻², Faraday rotation differs by ≤ 0.010° across 68–235 GHz, below LiteBIRD's σ(β) ≈ 0.02°; the achromaticity criterion is |β_F| < 0.032° at 40 GHz in a fit β(ν) = β₀ + β_F (ν/40 GHz)⁻².
4. **Approximate instruments.** Noise, beam and sky fractions are approximate, and the forecasts are Gaussian Fisher estimates.
5. **Theory.** Neither hypothesis is derived. STUR-B's κ is fitted. M3a needs an explicit U(1) breaking and a lepton-only charge assignment. Neither r value is a model output.
6. **Pre-registration scope.** M3a's registered curves extend only to ℓ = 1500, while its strongest signature lies at ℓ = 1500–3000. Done: Stage 10c2 addendum, SHA-256 `425eb65fd2371baee762ca77893ea472107b2c90bcacbc128e70b6bb12eaa308`, registering the ℓ ≤ 3000 curves of all 49 phases and the shape-test criterion.
7. **Review.** None of this has been independently reviewed.

## 9. Pre-registration and verification

| File | SHA-256 of file | Code SHA-256 stored inside |
|---|---|---|
| `scripts/genesis V10 preregistration` (Stage 10, STUR-B) | `c05406dd94c6ea596166a9e2121e895975ca4fb7e06e579cf42092f95d265bb3` | `11dd1aaf…6248091e` (`scripts/genesis V10 Light Bird`) |
| `scripts/genesis_v10b_preregistration.json` (Stage 10b, STUR-B) | `8dde755844ca7c2416a6618f4565bce815ea3fd8d9e9268492e509ebb2663018` | `2430061b…6de838` (`scripts/genesis_v10b_boltzmann.py`) |
| `scripts/genesis_v10c_m3a_preregistration.json` (Stage 10c, M3a) | `d3008ee624930ae356f4cfe3c89f331d7cbae8628346c895a4dba37f44224638` | `2a4a990c…6007cbf5` (`scripts/genesis_v10c_m3a.py`) |

**To verify:**
1. Run `sha256sum <file>` on each pre-registration file and compare with the table.
2. Check that the `code_sha256` field inside each JSON equals `sha256sum` of the named script.
3. Rerunning a script regenerates every field except `generated_utc`. Stage 10 was confirmed to reproduce byte-for-byte apart from that field.

Time-stamp: [PENDING: independent time-stamp — merge to the default branch and/or Zenodo/OSF DOI, recorded before ACT/SO/LiteBIRD release binned β(ℓ)]

## 10. Reproducibility

**Scripts** (all in `scripts/`):

| Script | Purpose | Runtime |
|---|---|---|
| `genesis V10 Light Bird` | Stage 10 | ~40 s |
| `genesis_v10b_boltzmann.py` | Stage 10b | ~10 min |
| `genesis_v10c_m3a.py` | Stage 10c | ~10 min |
| `genesis_v10c_m3a_lshape.py` | ℓ-shape forecast | ~10 min |
| `genesis_v10_sturb_action_audit.py` | §3.1–3.2 | — |
| `genesis_v10_beta_from_action.py` | §3.3 | — |
| `genesis_v10_r_from_action.py` | §3.4 | — |
| `genesis_v10_phase_suppression.py` | M1–M3 search | — |

**Versions used:** Python 3.13, CAMB 2.0.5, NumPy 2.5.3, SciPy 1.18.1, SymPy 1.14.0. Pinned in `scripts/requirements-genesis.txt`.

## References

[1] Y. Minami and E. Komatsu, "New Extraction of the Cosmic Birefringence from the Planck 2018 Polarization Data," Phys. Rev. Lett. 125, 221301 (2020), arXiv:2011.11254.
[2] J. R. Eskilt and E. Komatsu, "Improved Constraints on Cosmic Birefringence from the WMAP and Planck Cosmic Microwave Background Polarization Data," Phys. Rev. D 106, 063503 (2022), arXiv:2205.13962.
[3] B. D. Sherwin and T. Namikawa, "Cosmic birefringence tomography and calibration-independence with reionization signals in the CMB", arXiv:2108.09287 (2021); DOI 10.1093/mnras/stac3146 (MNRAS).
[4] LiteBIRD Collaboration, "LiteBIRD Science Goals and Forecasts: constraining isotropic cosmic birefringence," arXiv:2503.22322.
[5] J. R. Eskilt, "Cosmic birefringence from a joint analysis of ACT and Planck," arXiv:2608.06480; Phys. Rev. D 114, 043553 (2026).
[6] P. Diego-Palazuelos and E. Komatsu, "Cosmic Birefringence from the Atacama Cosmology Telescope Data Release 6", arXiv:2509.13654 (2025): β = 0.215 ± 0.074° (2.9σ); it quotes the ACT collaboration's EB rotation angle 0.20 ± 0.08° from T. Louis et al. (ACT), "DR6 Power Spectra, Likelihoods and ΛCDM Parameters", arXiv:2503.14452, JCAP (2025).
[7] A. Lewis, A. Challinor and A. Lasenby, "Efficient computation of CMB anisotropies in closed FRW models", ApJ 538, 473 (2000), arXiv:astro-ph/9911177 (CAMB).
