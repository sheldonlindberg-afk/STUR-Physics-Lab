# Stage 10i: pinning and anomaly claims, computed

**Script:** `scripts/genesis_v10i_pinning_anomalies.py`. It runs in about 25 s, and all 12 gates pass.
**Purpose:** replace four arguments from Stages 10f/10g with calculations.

## Inputs and their status

- **χ(0)^{1/4} = 75.5(5) MeV:** verified (Grilli di Cortona et al. 2016, arXiv:1511.02867; also quoted in arXiv:1812.01008).
- **High-temperature exponent b of χ(T) ∝ T^−b:** not verified. It is scanned over b = 6.68–8.16.
- **T_c = 150 MeV and a piecewise g\*:** approximations. They move the relic abundance by O(1). They do not affect the β bounds, which use ρ ≤ ρ_DM or ρ ≤ ρ_crit directly.

**Check on the relic solver:** misalignment with θ_QCD,i = 1 gives Ω h² ≈ 0.08–0.11 at f ≈ 5×10¹² GeV (f_a = f/6). That is consistent with the standard QCD-axion window.

## 1. Reading A (c_γ = 8, c_s = 3): **confirmed**

The R-phase is a QCD axion, with θ_QCD,eff = 6θ.

- **Misalignment.** The equation of motion with χ(T) was solved for 24 (f, b) cases. Each case is integrated to m/H = 300 and then continued with WKB to today.
- **Rotating today is impossible.** Still rotating over the barrier today needs ρ ≥ 2χ₀ = 6.5×10⁻⁵ GeV⁴, which is 1.8×10⁴² ρ_crit.
- **Trapped fields have a tiny amplitude.** With ρ ≤ ρ_DM, θ_amp(0) ≤ 1.3×10⁻²² for any f. At recombination the amplitude is ≤ 4.6×10⁻¹⁸.
- **The oscillation averages out.** Even the slowest case, f = M_Pl with m = 4.3×10³ s⁻¹, is suppressed by the CAMB visibility average to ≤ 1.1×10⁻¹⁶. That bound is computed by integrating by parts.

**Result:** |β| ≤ 7×10⁻²³ deg for any f and any initial condition, against 0.277° observed.

## 2. A QCD potential pins both STUR-B and M3a: **confirmed (c_s = 0 is required for both)**

- **The QCD frequency dominates.** For f ≤ M_Pl, m_QCD t/ω ≥ 2.6×10¹⁵ at recombination (≥ 10²⁰ today). The QCD mass overwhelms the log-time frequency.
- **STUR-B cannot keep rotating.** Its rotation energy, at the required rate ω_eff = 0.132 per unit ln t, is ≤ 4.4×10⁻⁴⁴ of the QCD barrier.
- **Neither amplitude fits.** A trapped field with ρ ≤ ρ_crit has amplitude ≤ 2.5×10⁻²² rad. M3a needs A₀ ≈ 1.4–2.9 rad (or 0.5–1.1 rad with c_γ = 8), and STUR-B needs about 1.4 rad of winding.

An earlier draft of this script used a windowed-signal demonstration. It was removed because the pure log-time signal already averages to 3×10⁻⁵ over the visibility window, so the demonstration could not isolate the effect of pinning.

## 3. Reading B: **modified — the earlier "X = 1 for every species" is refuted for the repo's own potential**

The repo's localization potential is α(1 − cos(u + θ − φ_g)) on the circle. The script solves its ground state for each θ and computes the 4D mass phase arg m₄(θ) with m₄ = ∫ψ² e^{i(u+θ)}.

| Case | X_f = d arg m₄/dθ (quark α = 1.48) | E₀(θ) variation |
|---|---|---|
| repo potential only (comoving) | **0.000000** (10⁻¹²) | 2×10⁻¹¹ (flat) |
| + X-fixed Higgs modulation, ε_H = 0.40 | 0.184 | flat at tree level |
| + X-fixed pinning, η = 1 / 10 / 100 | 0.373 / 0.972 / 0.998 | 0.02–0.07 |

Lepton values (α = 1.38) agree to within 0.01.

- **The zero-mode shift is an exact flat direction.** With the repo's own potential the fermions move with the phase, no 4D mass phase rotates, and **c_γ = c_s = 0 exactly**.
- **X_f → 1 needs pinning in X**, which the repo does not supply. Its Z₃ action X → X + L/3 has no fixed points (the minimum shift is L/3). The Master Action's S¹/Z₂ requirement that R be Z₂-even is violated by the winding background: max |R(X) − R(−X)|/v = 2.
- **An X-fixed Higgs modulation** would give X_f ≈ 0.18, so c_γ ≈ 1.5. But the same modulation also breaks the flat direction and gives the phase a static mass (see 10f).

## 4. Charge enumeration: **modified — the "forces c_γ = 8, c_s = 3 / leptons only" claim is refuted**

- **R-Yukawas alone** (s = ±1 per coupling, which the Z₃ structure allows): full flavor mixing still allows generation-dependent signs, carried by the right-handed charges (residual 6×10⁻¹⁶). Over all 512 assignments, c_s = 0 occurs with c_γ ∈ {−6, −4, −2, 0, 2, 4, 6}. For example, s_u = −s_d with s_e = s_u gives c_γ = 6, c_s = 0. **Quarks can carry R-charge without a color anomaly.**
- **R-Yukawas plus the repo's Higgs-overlap Yukawas**, with U(1)_R exact: invariance forces s_u = −X_H and s_d = s_e = X_H, which gives **c_γ = c_s = 0**. A Higgs neutral under U(1)_R is inconsistent: U(1)_R is then explicitly broken and the phase is not a Goldstone.

## What this changes

| Earlier claim (10f/10g) | Computed outcome |
|---|---|
| Reading A gives β ≈ 0 | **Confirmed**: \|β\| ≤ 7×10⁻²³ deg |
| c_s ≠ 0 pins STUR-B and M3a | **Confirmed**: amplitude cap 2.5×10⁻²² rad |
| Reading B: θ only relocalizes fermions, c_γ = 0 | **Confirmed** (X_f = 10⁻¹²). This is the repo's own case |
| Generation index cannot cancel; X = 1 forces c_γ = 8, c_s = 3; M3a needs leptons-only charges | **Refuted.** c_s = 0 with c_γ ≠ 0 is allowed by R-Yukawas alone. With the Higgs Yukawas, c_γ = c_s = 0 |

**Net result:** every consistent reading of the repo's fermion sector gives β ≈ 0 (H0). Reading A gives a pinned QCD axion; reading B gives an exact flat direction with no anomaly; and with both Yukawa structures U(1)_R is anomaly-free.

A β ≠ 0 hypothesis needs both of the following:

- an X-fixed pinning of the fermion positions, which the repo does not have;
- R-Yukawas whose charges are not tied to the Higgs Yukawas, for example s_u = −s_d.

Under those conditions **quarks may be R-charged**, so M3a's H2 can be restated as "c_s = 0 assignment" rather than "leptons only".
