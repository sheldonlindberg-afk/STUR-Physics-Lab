# GENESIS v10 Stage 10j: R-phase mass dynamics, computed instead of argued

**Script:** `scripts/genesis_v10j_mass_dynamics.py`. It runs in about 20 minutes, and all 10 gates pass. It uses the Stage 10b CAMB sources and transfers, which it imports without modifying.

Two claims in the earlier write-ups had been argued rather than computed:
- **Claim 5:** a static cos 3θ mass makes the oscillation average out of the CMB.
- **Claim 6:** M3a's log-time form needs a mass that scales as 1/t.

This document replaces both with calculations. Neither original claim survives unchanged.

## Claim 5: static cos 3θ mass

**Setup.**
- The potential is V = (m²f²/9)(1 − cos 3θ), with field range |θ| ≤ π/3.
- The field equation θ̈ + 3Hθ̇ + (m²/3) sin 3θ = 0 is solved on the Planck background, starting frozen at θ_i ≤ π/3.
- The rotation is β = K[θ(t₀) − θ(t)], with K = c_γα/2π, and it is fed through exact CAMB EB transfers at ℓ = 50–1200 using the Stage 10c LiteBIRD weights.
- For m t₀ > 3×10⁴ the WKB form is used. Its emission term is the visibility Fourier transform at m. Its today term is averaged over T_obs = 5 yr. Its amplitude is capped by ρ_θ ≤ ρ_DM at f = 2.1×10¹² GeV.

**Gates.**
- A frozen field (m t₀ = 0.3) gives 0.0009°.
- θ·a^(3/2) is constant at late times to 2×10⁻⁵.
- At the overlap, WKB gives 0.202° and the ODE gives 0.209°, which agree to within 3%.

| m [GeV] | m/H(z*) | max\|β\|, c_γ = 3 | max\|β\|, c_γ = 8 |
|---|---|---|---|
| 4.5×10⁻⁴³ (≈ 0.3 H₀) | 1×10⁻⁵ | 0.0009° | 0.002° |
| 7×10⁻⁴² | 2×10⁻⁴ | 0.17° | 0.46° |
| 3.6×10⁻⁴¹ | 1×10⁻³ | **0.22°** (maximum) | 0.59° |
| 10⁻⁴⁰ – 4.5×10⁻³⁸ | 3×10⁻³ – 1.4 | 0.20–0.21° (plateau) | 0.54–0.56° |
| 1.8×10⁻³⁵ | ~500 | 5×10⁻⁶° | 1.5×10⁻⁵° |
| 6×10⁻¹⁶ (claimed floor) | 2×10²² | 6×10⁻²³° | 1.6×10⁻²²° |

**Verdict: modified.**
- **At the claimed floor, confirmed.** At m ≥ 6×10⁻¹⁶ GeV (ε_H = 0.1) the rotation is 10⁻²²°, so it averages out. Suppression already sets in for m ≳ 10 H(z*).
- **Not true for every static mass.** For H₀ ≲ m ≲ H(z*) the field rolls coherently after recombination, and β reaches a plateau that is not averaged out.
  - **c_γ = 3** (leptons only, as c_s = 0 requires): the maximum is **0.22°**, so β_now = 0.277 ± 0.057° is **not reached** at |θ_i| ≤ π/3. The shortfall is only about 1σ.
  - **c_γ = 8:** β_now is reachable for **m = 7×10⁻⁴² – 3.3×10⁻³⁷ GeV**. But c_γ = 8 comes with c_s = 3, which makes the field a QCD axion.
- **Fine-tuning required.** Such light masses need ε_H far below the critical value computed in `genesis_v10f_theory_gaps.py`, where m < H(z*) requires a tiny ε_H.
- **Limitations.** The energy check is at the smallest allowed f against ρ_DM, which is generous. The reionization (low-ℓ) angle was not computed in this branch.
- **Consequence.** A static-mass, ultralight R-phase is a β ≠ 0 option that the Stage 10g ranking did not list. With c_γ = 3 it falls about 1σ short of β_now.

## Claim 6: which mode equation gives M3a's form?

**Setup.**
- The mode equation in u = ln t is θ_uu + F θ_u + Ω²θ = 0.
- Every case is integrated backwards from today with θ and θ_u equal to the registered M3a solution: median phase δ = 1.5708 rad, and A₀ = 1.4352 rad recovered exactly from the stored curve, since the curve is linear in A₀ to 1×10⁻⁶.
- Each case is compared with the registered curves through exact CAMB transfers.

| Case | A(t*)/A(t₀) | ⟨dφ/d ln t⟩ | β_high | max\|Δβ_eff(ℓ)\| vs registered |
|---|---|---|---|---|
| (iii) repo Cauchy-Euler (F = 0, Ω = ω) | 1.000 | 19.71 | 0.277° | 7.5×10⁻⁶° |
| (iv) m = ω/t, FRW friction | 186 | 19.71 | −0.334° | 1.83° |
| (ii) ξ𝕋 coupling, ξ = 36 / 146.2 / 400 | 224 / 237 / 235 | 9.9 / 19.7 / 32.6 | −0.49° / −0.05° / 0.01° | 4.17° / 0.38° / 0.27° |
| (i) static mass, m t₀ = ω, 3ω, 10ω | 2–3×10⁴ | 1.8 / 5.7 / 18.8 | ≈ 0° | 3.98° / 1.58° / 0.28° |

**Gates.**
- (iii) reproduces the registered curve to 7.5×10⁻⁶°, with constant amplitude and frequency ω.
- (iv) has a matter-era amplitude slope of −0.479, against −1/2 from the indicial equation.
- The best FRW-friction case deviates by 0.27°, which is as large as the signal itself.

**Verdict: refuted as stated.**
- **A 1/t mass is not enough.** It gives the right log-time frequency, but with FRW friction 3H the amplitude grows about 186× ≈ (t₀/t*)^(1/2) back to recombination. The rotation history then has nothing in common with M3a's.
- **The ξ𝕋 coupling and static masses fail too**, by 0.27–4°.
- **Only the repo's F = 0 equation reproduces M3a.** That equation is not the FRW equation of motion: it needs 1/t friction, i.e. a ∝ t^(1/3).
- **Consequence.** M3a's H1 is not realisable by any of these mass laws in FRW cosmology. That is a stronger negative than the earlier argument, which said only "needs a mass ∝ 1/t".
