# GENESIS v6: Quantum Nucleation → Inflation → Reheating → BBN → CMB → BAO

**Document Type:** Review of an external real-physics pipeline (standard cosmology, not a
STUR mechanism)
**Status:** POSITIVE RESULT — broadly consistent with real published data, with one real,
quantified, honestly-reported tension
**Provenance:** This pipeline was built and run outside this repository (iteratively, across
several versions v1→v6, by/with another AI session per the user's own workflow) and handed
back here as a 46-page source listing (`genesis_pipeline_v6.pdf`) plus a run transcript
(`run_v6.pdf`). **This document reviews those two files; the pipeline was not independently
re-executed in this session.** It embeds several large literal data tables (PRIMAT 2023
nuclear rate tables, the DESI DR2 BAO covariance matrix, weak-rate thermal correction tables —
thousands of individual numbers) that cannot be reliably retyped from OCR'd page images without
real risk of a silent transcription error. Re-running the actual `.py` file (not a PDF of it)
is listed as the one open item that would upgrade this from "reviewed" to "independently
verified" — see §7.

---

## 0. What this is

A complete, standard-physics (non-speculative, non-STUR) account of the universe's first
~380,000 years, built in six stages, each stage's output feeding the next, confronted against
real published data at every step:

1. **Quantum nucleation** (Vilenkin tunneling) of a closed FRW universe from "nothing."
2. **Inflation** (Starobinsky R²), exact background + exact Mukhanov-Sasaki mode equations
   (no slow-roll shortcuts).
3. **Reheating**, computed self-consistently (not assumed) from a physically motivated decay
   channel (gravitational scalaron decay to Higgs pairs).
4. **BBN**, with the real PRIMAT 2023 nuclear rate tables and the full Pitrou et al. (2018)
   weak-rate treatment (Born + radiative corrections + finite nucleon mass + weak magnetism).
5. **Recombination → CMB acoustic scale**, cross-checked against an independent CLASS/HyRec
   2020 run.
6. **DESI DR2 BAO**, combined with the BBN-inferred baryon density, for an H0 determination
   using **no CMB anisotropy data at all**.
7. *(Optional, run when available)* **Full CMB power spectra** via CLASS against the real
   Planck 2018 plik-lite likelihood (615 bandpowers) and, when supplied, the real ACT DR6
   CMB-only likelihood.

Every comparison number below is read directly from the provided run transcript, not
recomputed or estimated.

---

## 1. Stage 1 — Vilenkin quantum tunneling nucleation

The WKB tunneling exponent is checked **two independent ways** (direct WKB integral, and a
numerically-solved Euclidean instanton) against the known analytic result, not just quoted:

| V | WKB (numeric) | analytic 24π²/V |
|---|---|---|
| 1e-2 | 2.368705e+04 | 2.368705e+04 |
| 1e-6 | 2.368705e+08 | 2.368705e+08 |
| 1e-10 | 2.368705e+12 | 2.368705e+12 |

Exact agreement at every scale tested.

---

## 2. Stage 2 — Starobinsky R² inflation vs. the quadratic model

Exact background + exact Mukhanov-Sasaki (no slow-roll approximation), normalized to the real
measured A_s = 2.100×10⁻⁹.

**Starobinsky R²** (V0 = 1.133×10⁻¹⁰ M⁴, 148.1 total e-folds from φ0=6.5):

| N* | n_s | pull vs Planck | pull vs P-ACT-LB | r |
|---|---|---|---|---|
| 50 | 0.9615 | −0.8σ | −3.8σ | 0.0043 (OK, r<0.036) |
| 55 | 0.9649 | −0.0σ | −2.8σ | 0.0035 (OK) |
| 60 | 0.9677 | +0.7σ | −1.9σ | 0.0030 (OK) |

**m²φ² (quadratic)** (V0 = 4.119×10⁻¹¹ M⁴, 72.8 total e-folds):

| N* | n_s | pull vs Planck | pull vs P-ACT-LB | r |
|---|---|---|---|---|
| 50 | 0.9597 | −1.2σ | −4.3σ | 0.1582 (**EXCLUDED**) |
| 55 | 0.9634 | −0.4σ | −3.2σ | 0.1440 (**EXCLUDED**) |
| 60 | 0.9664 | +0.4σ | −2.3σ | 0.1322 (**EXCLUDED**) |

Data: Planck18+BK18+BAO n_s = 0.9649±0.0042; P-ACT-LB (ACT DR6) n_s = 0.9743±0.0034; BK18
r < 0.036 (95%). **The calculation correctly discriminates a viable model (Starobinsky) from
an excluded one (quadratic) — the quadratic model fails the tensor bound at every N* tested.**

**Tunneling boundary condition genuinely matters.** At the Starobinsky plateau (V0 = 1.133e-10
M⁴ → H = 6.145×10⁻⁶ M, energy scale 7.94×10¹⁵ GeV):

| nucleate at φ | e-folds | ln P_tunnel(φ) − ln P_tunnel(plateau) | ln P_no-boundary(φ) − ln P_no-boundary(plateau) |
|---|---|---|---|
| 2.0 | 1.6 | −1.14×10¹² | +1.14×10¹² |
| 4.0 | 16.2 | −1.69×10¹¹ | +1.69×10¹¹ |
| 5.5 | 62.5 | −4.77×10¹⁰ | +4.77×10¹⁰ |
| 6.0 | 95.9 | −3.15×10¹⁰ | +3.15×10¹⁰ |
| 8.0 | 509.1 | −6.10×10⁹ | +6.10×10⁹ |
| 12.0 | 13489.3 | −2.32×10⁸ | +2.32×10⁸ |

Vilenkin tunneling weight grows toward the plateau top (favors long inflation); Hartle-Hawking
no-boundary weight favors the potential minimum (favors *no* inflation). **Which boundary
condition is physically correct is an open question in quantum cosmology — this is reported
as a consequence of choosing Vilenkin's, not a proof that inflation must occur.**

---

## 3. Stage 2.5 — Reheating computed, not assumed (the key new result)

N* was treated as a free choice (50–60) in earlier versions of this pipeline. v6 computes it
self-consistently from a two-fluid Boltzmann treatment of reheating, using w=0 — the
time-averaged equation of state the R² potential's scalaron actually has, oscillating about
its quadratic minimum (this is the model's own prediction, not a choice):

| Reheating scenario | T_reh | N* | n_s | pull vs Planck | pull vs P-ACT-LB |
|---|---|---|---|---|---|
| Higgs decay, ξ=0 (physically motivated rate) | 5.10×10⁹ GeV | 51.39 | 0.9625 | −0.6σ | −3.5σ |
| Instant reheating (max N* possible for w<1/3) | 2.25×10¹⁵ GeV | 55.72 | 0.9653 | +0.1σ | −2.6σ |
| T_reh = 4 MeV (BBN floor, min N*) | 4.00×10⁻³ GeV | 42.16 | 0.9546 | −2.5σ | −5.8σ |

A factor-4 change in the decay rate shifts N* by only ~0.2 — the result is not sensitive to
the exact coupling.

**P-ACT needs N* ≥ 59.5 (2σ), ≥ 66.7 (1σ), 75.7 (central). With w=0, N* is capped at 55.7
(the instant-reheating limit) — so Starobinsky + standard reheating stays ≥2.6σ below P-ACT
for ANY reheating temperature.** This is the pipeline's strongest, most falsifiable claim: it
isn't that a particular reheating choice happens to disagree with ACT — no choice of standard
(w=0) reheating temperature can reach it.

What *would* close the gap (checked explicitly, and flagged as **not what the R² potential
actually produces** — would require new physics, e.g. a kination/stiff phase):

| w (held constant) | T_reh | N* | n_s | pull vs P-ACT-LB |
|---|---|---|---|---|
| 0.33 | 4 MeV | 55.91 | 0.9655 | −2.6σ |
| 0.67 | 4 MeV | 64.12 | 0.9698 | −1.3σ |
| 1.00 | 4 MeV | 69.54 | 0.9721 | −0.7σ |

To be within 2σ of P-ACT with w=1 needs T_reh ≲ 1.8×10¹⁰ GeV; within 1σ needs T_reh ≲ 8.3 GeV.

**Tensor forecast for the model's own prediction (r=0.0040):** BICEP/Keck BK18 (current,
σ(r)~0.009) → 0.4σ, not yet decisive. Simons Observatory (ground, running now, goal
σ(r)~0.002) → would be 2.0σ. LiteBIRD (JAXA satellite, goal σ(r)~0.001, launch early 2030s)
→ would be 4.0σ. (CMB-S4 was cancelled by DOE/NSF in July 2025.) **A detection at
r~0.003–0.004 together with n_s~0.965 would strongly favor R²; r<0.001 would rule it out.**

---

## 4. Stage 3 — BBN with real nuclear rate tables (PRIMAT 2023)

Full Pitrou et al. (2018) weak-rate treatment: neutron-decay phase space with radiative +
finite-mass corrections gives λ₀ = 1.75476 (the plain Born value is 1.63609 — the corrections
are a genuine, large effect, correctly included). At the real Planck ω_b = 0.02237
(η₁₀=6.124), nucleon number is conserved to 10 decimal places.

| Quantity | Prediction | Real observed | Tension |
|---|---|---|---|
| Y_p | 0.24756 ± 0.00011 | 0.2453±0.0034 (Aver+21) | +0.7σ |
| Y_p | (same) | 0.2387±0.0036 (EMPRESS XV 2025) | +2.5σ |
| D/H | 2.4571×10⁻⁵ ± 2.64×10⁻⁷ | 2.527×10⁻⁵±3.00×10⁻⁷ (Cooke+18) | −1.7σ |
| ³He/H | 1.039×10⁻⁵ ± 1.3×10⁻⁷ | < 1.1×10⁻⁵±2.0×10⁻⁶ (Bania+02) | consistent |
| ⁷Li/H | 5.505×10⁻¹⁰ ± 1.8×10⁻¹¹ | 1.58×10⁻¹⁰±3.10×10⁻¹¹ (Sbordone+10) | **+10.9σ** |

The ⁷Li discrepancy is the real, famous **cosmological lithium problem** — widely attributed
to stellar depletion in old halo stars, not a BBN calculation error, and correctly *not* used
by standard practice (e.g. the PDG BBN review) to constrain the baryon density. Reported for
completeness, not papered over.

**Independent baryon density cross-check:** inverting this network's own D/H prediction gives
ω_b(BBN, D/H) = 0.02199 ± 0.00022, vs. ω_b(CMB, Planck 2018) = 0.02237 ± 0.00015 — a −1.5σ
difference between two independent probes (nuclear physics at t~3 min vs. acoustic physics at
t~380,000 yr), a known, modest feature of current nuclear rates, not hidden.

**Stage 3b (lepton asymmetry ξ_ν extension, properly judged by AIC/BIC, not just χ²):** adding
a free electron-neutrino chemical potential improves the fit (Δχ²=2.83 for 1 extra parameter,
ΔAIC=+0.83, ΔBIC=+1.44 — positive, but weak). Verdict: **weak evidence only**; ξ=0 is 1.7σ
from the best fit (ξ = +0.017±0.010). The two helium surveys disagree with each other by
~1.4σ, so no single Y_p can fit both — ξ_ν mostly relieves the EMPRESS pull at the cost of a
slightly lower D/H. Appropriately not oversold as a discovery.

---

## 5. Stage 4 — Recombination → CMB acoustic scale (with a self-caught, self-fixed bug)

Using Y_p = 0.2476 handed over from Stage 3, Planck 2018 best-fit ω_b, ω_c, H0:

**First pass (3-level hydrogen atom, Peebles/RECFAST v1.5):**

| Quantity | Pipeline | Planck 2018 | Pull |
|---|---|---|---|
| z* | 1090.47 | 1089.92±0.25 | +2.2σ |
| r* [Mpc] | 144.39 | 144.43±0.26 | −0.2σ |
| 100θ* | 1.04079 | 1.04110±0.00031 | −1.0σ |
| z_drag | 1060.43 | 1059.94±0.3 | +1.6σ |
| r_drag [Mpc] | 147.05 | 147.09±0.26 | −0.2σ |

**Cross-check with CLASS/HyRec 2020 (full multilevel atom, same Y_p):**

| Quantity | Pipeline | Planck 2018 | Pull |
|---|---|---|---|
| z* | 1089.99 | 1089.92±0.25 | +0.3σ |
| r* [Mpc] | 144.43 | 144.43±0.26 | −0.0σ |
| 100θ* | 1.04108 | 1.04110±0.00031 | −0.1σ |
| z_drag | 1060.00 | 1059.94±0.3 | +0.2σ |
| r_drag [Mpc] | 147.09 | 147.09±0.26 | −0.0σ |

**This is good scientific practice, not a cover-up**: the +0.5 offset in the 3-level-atom pass
was correctly diagnosed as the known limitation of that approximation, confirmed by running
the more accurate multilevel calculation, which removes it. The scorecard (§7) uses the
corrected (HyRec) values.

Planck compressed distance prior (Chen, Huang & Wang 2019): R = 1.7500 vs. 1.7502±00046 →
χ²=0.00 for 2 dof.

**CMB-inferred H0 from the measured acoustic angle θ* alone (ω_b, ω_c held fixed):
67.46 ± 0.10 km/s/Mpc** — vs. Planck's own full fit 67.36±0.54 (+0.2σ).

---

## 6. Stage 5 — DESI DR2 BAO + BBN → H0 with NO CMB anisotropy data

Combines 13 real DESI DR2 BAO measurements (full published covariance) with ω_b = 0.02199
±0.00022 from Stage 3's own deuterium inference and r_drag from Stage 4's own recombination
physics — a genuinely independent early-universe H0 determination that uses no CMB power
spectrum information at all.

**Best fit: H0 = 68.42 ± 0.43 km/s/Mpc, Ω_m = 0.2972 ± 0.0086, r_drag = 148.41 Mpc.**
Goodness of fit: χ² = 10.28 for 13 points − 2 parameters = 11 dof (good fit, no per-point
pull exceeding ~2σ).

| Comparison | Tension |
|---|---|
| vs. Planck CMB (67.36±0.54) | +1.5σ |
| vs. SH0ES (73.04±1.04) | **−4.1σ** |

**This independently reproduces the real Hubble tension a third way**: an early-universe
ruler built from nuclear physics (BBN, t~3 min) plus large-scale structure (BAO, t~billions of
years) — using *zero* CMB anisotropy information — lands next to the CMB value and far from
the distance-ladder value. Two independent early-universe routes agreeing with each other
and not with the ladder is exactly why the Hubble tension is taken seriously in the field.

Ω_m: DESI+BBN 0.2972±0.0086 vs. Planck 0.3153±0.0073 → −1.6σ (1D; DESI's own 2D analysis
quotes 2.3σ).

---

## 7. Stage 6 — Full CMB power spectra (CLASS + real Planck 2018 plik-lite likelihood)

Run with an actual compiled CLASS Boltzmann code, HyRec recombination, HMcode lensing,
against the real Planck 2018 plik-lite TT,TE,EE likelihood (615 bandpowers) plus a Gaussian
τ prior standing in for Planck's low-ℓ EE likelihood.

**Validation (everything free) against Planck's own published fit:**

| Parameter | This pipeline | Planck 2018 TT,TE,EE+lowE |
|---|---|---|
| ω_b | 0.02236±0.00015 | 0.02236±0.00015 |
| ω_c | 0.12015±0.00135 | 0.1202±0.0014 |
| n_s | 0.96561±0.00426 | 0.9649±0.0044 |
| τ | 0.05590±0.00822 | 0.0544±0.0073 |
| H0 | 67.32 | 67.27±0.60 |

**χ² scenario test — does fixing GENESIS's own predicted parameters hurt the fit to the real
Planck power spectrum?**

| Scenario | χ² | Δχ² | Tension | H0 |
|---|---|---|---|---|
| ΛCDM, all 6 free (baseline) | 587.41 | 0.00 | 0.0σ | 67.32 |
| n_s fixed to the R² prediction (0.9625) | 587.98 | 0.57 | 0.8σ | 67.01 |
| ω_b fixed to the BBN D/H value (0.02199) | 594.01 | 6.59 | 2.6σ | 66.24 |
| both fixed (full GENESIS early-universe prediction) | 594.17 | 6.75 | 2.1σ | 66.35 |

**The inflation prediction costs almost nothing against the real Planck spectrum (0.8σ)**;
the ω_b-from-BBN value costs more (2.6σ), consistent with the independently-noted 1.5σ BBN-CMB
ω_b tension from Stage 3 (treating a measured quantity as if it were exact, rather than with
its own error bar, is explicitly flagged as the reason this number reads larger than the
genuine statistical tension).

ACT DR6 was not run in the session that produced this transcript (needs the real
`dr6_data_cmbonly.fits` file from NASA LAMBDA — the pipeline explicitly refuses to run on a
bundled simulated test file if one is substituted, rather than silently using fake data).

---

## 8. Scorecard — read the way a referee would

**(A) Code validation** (same inputs as Planck's own published analysis — this tests the
software, not the physics):

| Quantity | Pipeline | Published | Pull |
|---|---|---|---|
| 100θ* | 1.04108 | Planck 2018: 1.0411±0.00031 | −0.1σ |
| z* | 1089.99 | 1089.92±0.25 | +0.3σ |
| r* [Mpc] | 144.43 | 144.43±0.26 | −0.0σ |
| z_drag | 1060.00 | 1059.94±0.3 | +0.2σ |
| r_drag [Mpc] | 147.09 | 147.09±0.26 | −0.0σ |
| H0 from measured θ* | 67.46 | 67.36±0.54 | +0.2σ |
| (R, ω_b) χ² | 0.00 | Planck compressed, 2 dof | — |
| Planck spectra fit: ω_b | 0.02236 | 0.02236±0.00015 | +0.0σ |
| Planck spectra fit: ω_c | 0.12015 | 0.1202±0.0014 | −0.0σ |
| Planck spectra fit: n_s | 0.96561 | 0.9649±0.0044 | +0.2σ |
| Planck spectra fit: H0 | 67.32 | 67.27±0.60 | +0.1σ |

**10 of 10 within 2σ.**

**(B) Physics tests** — GENESIS's genuine predictions, combined into one global χ² with
honest degrees of freedom, a p-value, and standard verdict thresholds (p≥0.05 consistent;
0.0027≤p<0.05 tension 2–3σ; p<0.0027 excluded >3σ):

| Data combination | χ² | dof | p-value | ~σ | Verdict |
|---|---|---|---|---|---|
| Core + Planck n_s | 19.09 | 15 | 0.21 | 1.3σ | **consistent** |
| Core + Planck n_s + ξ_ν | 16.26 | 14 | 0.298 | 1.0σ | consistent |
| Core + P-ACT-LB n_s | 30.80 | 15 | 0.00934 | 2.6σ | **tension** |
| Core + P-ACT-LB n_s + ξ_ν | 27.97 | 14 | 0.0143 | 2.4σ | tension |
| + ⁷Li + SH0ES (Planck n_s) | 152.29 | 17 | 8.7e-24 | 10.1σ | excluded >3σ |
| + ⁷Li + SH0ES (P-ACT-LB n_s) | 164.00 | 17 | 4.31e-26 | 10.6σ | excluded >3σ |

**Bottom line (direct from the pipeline's own output):**
- Core data with Planck's own n_s: χ²/dof = 19.1/15, p=0.21 → **GENESIS is consistent.**
- Core data with ACT's newer P-ACT-LB n_s: χ²/dof = 30.8/15, p=0.0093 → **in tension**; the
  driver is specifically the R² inflation prediction (−3.5σ vs. P-ACT-LB at the physically
  computed reheating N*). Decisive future tests: independent confirmation of n_s~0.974
  (Simons Observatory) and r~0.004 (LiteBIRD).
- Adding the lithium plateau or SH0ES as if they were clean primordial/early-universe
  measurements fails *any* standard ΛCDM cosmology, not something specific to this pipeline —
  they are the field's own open problems (stellar lithium depletion; the distance-ladder
  Hubble tension), shown for completeness, not used to inflate or deflate the real verdict.

---

## 9. Sources (as cited in the pipeline and run transcript)

- Planck Collaboration, *Planck 2018 results. VI. Cosmological parameters*
- Riess et al. 2022, *A Comprehensive Measurement of H0*, ApJL 934, L7 (SH0ES)
- DESI Collaboration 2025, arXiv:2503.14738 (DESI DR2 BAO)
- PRIMAT v0.2.2 (23 June 2023) nuclear rate tables, original measurements cited per reaction
  (Ando+2006, Moscoso+2021, Gómez Iñesta+2017, Serpico+2004, de Souza+2019, Descouvemont+2004,
  Iliadis+2016), as distributed in LINX (github.com/cgiovanetti/LINX, MIT licence)
- Pitrou et al. 2018, arXiv:1801.08023 (full weak n↔p rate treatment)
- Aver, Berg, Olive, Pogge, Salzer & Skillman 2021, JCAP 03, 027 (Y_p)
- EMPRESS XV 2025, arXiv:2506.24050 (Y_p, independent survey)
- Cooke, Pettini & Steidel 2018, ApJ 855, 102 (D/H)
- Bania, Rood & Balser 2002, Nature 415, 54 (³He/H upper bound)
- Sbordone et al. 2010, A&A 522, A26 (⁷Li/H, the Spite plateau / lithium problem)
- Chen, Huang & Wang 2019, JCAP 02, 028 (Planck compressed distance priors)
- Seager, Sasselov & Scott 1999 (RECFAST v1.5 calibration, the one hand-calibrated fudge
  factor in this pipeline, explicitly flagged as such)
- Louis et al. 2025 (ACT DR6, P-ACT-LB n_s)
- BICEP/Keck 2021, PRL 127, 151301 (BK18, r < 0.036 95% limit)
- CLASS (lesgourg/class_public), HyRec 2020 recombination, HMcode lensing
- heatherprince/planck-lite-py (Planck 2018 plik-lite re-implementation)
- ACT Collaboration DR6-ACT-lite (github.com/ACTCollaboration/DR6-ACT-lite)

---

## 10. Open items

1. **Independent re-execution from the real `.py` file, not this PDF review.** This document
   is built from reading a 46-page OCR'd source listing and a run transcript; several massive
   embedded literal data tables (PRIMAT rates, DESI covariance, weak-rate thermal corrections)
   were not retyped and re-run here because of real transcription-error risk. If the actual
   source file is made available, Stages 1–5 (pure numpy/scipy) should be directly runnable
   in a session like this one to independently confirm the numbers above; Stage 6 additionally
   needs a compiled CLASS, the real Planck plik-lite data directory, and (optionally) the real
   ACT DR6 `dr6_data_cmbonly.fits` file, none of which this session has confirmed it can fetch.
2. **The ACT tension is real, not resolved.** 2.6σ, specifically driven by the R² inflation
   n_s prediction under standard (w=0) reheating — not fixable by any reheating temperature
   choice within the model as built. Resolving it one way or the other needs new data (Simons
   Observatory n_s, LiteBIRD r), not a recalculation.
3. **No connection attempted to STUR's own framework.** This is a standalone, real-physics
   pipeline, reviewed on its own terms — like `QUARK_RESISTANCE_BOUNCE_COSMOLOGY.md`, it is
   not a STUR closure claim.

---

**Document Status:** Reviewed, not independently re-executed in this session. The pipeline's
own reported results are broadly consistent with real data (10/10 code-validation checks within
2σ; physics tests consistent with Planck's own n_s at p=0.21) and the one genuine tension found
(2.6σ with newer ACT data) is honestly attributed to a specific, falsifiable physical driver
rather than smoothed over — a meaningfully different outcome from the quark-torsion-bounce
exploration earlier in this project.
