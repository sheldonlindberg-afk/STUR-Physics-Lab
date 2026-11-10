# Oppenheim's classical gravity, and what one levitated particle decides

Reproduce: `python3 src/stur_oppenheim.py` (about 2 s). The full output is in
`results/oppenheim/output.txt`, and `tests/test_oppenheim.py` pins it. Labels: KNOWN,
FOLLOWS, CHECK, LIT, STUR (a result of this project).

## Why this page exists

[COLLECTIVE.md](COLLECTIVE.md) argues that gravity's field follows each branch because a
*statistical* gravity would carry noise. That argument left two gaps:

1. **The strongest current alternative was never addressed.** Oppenheim's
   postquantum classical gravity keeps the metric classical, couples it to quantum matter
   through a completely positive Markovian map, and pays for it with a
   **decoherence–diffusion trade-off** (LIT, retrieved: Oppenheim, Sparaciari, Šoda,
   Weller-Davies, arXiv:2203.01982, Nat. Commun. 14, 7910 (2023)). It is the leading
   classical-gravity model, and the main thing a λ = 1 experiment has to beat.
2. **The smearing length was fixed by identification.** COLLECTIVE sets R₀ equal to the
   entanglement cutoff a. Nothing forces a statistical gravity to make that choice.

This page works through Oppenheim's trade-off with the repository's conventions, finds
what it predicts for one particle, and corrects one number in COLLECTIVE.md on the way.

## The trade-off (LIT, with the constant checked)

Oppenheim et al.'s eq. (29): the coefficients of any completely positive classical–quantum
(CQ) master equation obey the matrix-kernel inequality [[2D₂, D₁], [D₁, D₀]] ⪰ 0.

- D₀ is the decoherence kernel of the mass density.
- D₁ is the back-reaction. In the Newtonian limit, D₁ = −½ on each side (their eq. 38).
- D₂ is the diffusion. It appears as a random mass J that sources the potential,
  ∇²Φ = 4πG(m + J), with ⟨JJ⟩ = 2D₂ δ(t − t′) (their eqs. 39–41).

Per Fourier mode of the mass density, in this page's notation:

```
D₀(q) · S_J(q)  ≥  g(q)² / 4          S_J = 2D₂,   g = smearing of the source (g = 1: local)
```

**P1 (CHECK).** The constant ¼ was checked on a qubit that drives one classical variable.
I computed the CQ state exactly and tested positivity, |ρ₀₁(z)|² ≤ ρ₀₀(z)ρ₁₁(z), at every z:

| D₀·D_var / (α²/4) | min over z of (ρ₀₀ρ₁₁ − \|ρ₀₁\|²)/ρ₀₀ρ₁₁ |
|---|---|
| 0.90 | −0.105 (not a state) |
| 0.99 | −0.010 (not a state) |
| 1.00 | 0 |
| 1.01 | +0.010 |

Continuous measurement of the mass density, with the record fed back as the potential,
lands exactly on the bound (ratio 1.000000). The trade-off is the price of letting a
classical field learn where quantum matter is.

## P2. If matter feels the noisy potential, the floor is Diósi–Penrose (FOLLOWS)

In Oppenheim's Newtonian limit, matter couples to the classical potential through
H_I = ∫Φ m (their eq. 35). The random mass J therefore jitters Φ, and that jitter
dephases the matter too. Per mode, the total decoherence is:

```
D₀ + K² S_J / ħ²   ≥   2K √(D₀ S_J) / ħ   ≥   K g / ħ,        K = 4πG / q²
```

That is the Diósi–Penrose kernel at every q (grid check to 2×10⁻¹⁶). It is exactly the
Tilloy–Diósi minimum of `src/stur_thermo_gravity.py` Q1.

**So Oppenheim's continuous class is inside COLLECTIVE.md's argument.** This holds for
models that are continuous, Markovian and translation-invariant, with Gaussian noise.
For the design-A diamond (1.5×10⁻¹⁴ kg, split 721 µm), such a gravity decoheres it at
≥ 169.5 /s unless the source is smeared over R₀ > 455 µm. The inverse-square law holds
down to 52 µm, which rules out that much smearing.

## P3. One particle measured two ways: a shape-free bound (STUR)

P2 needs one step beyond the trade-off itself: the noisy potential has to act back on
the matter. To drop even that step, use only the trade-off together with the force the
noise exerts, F = −∫m∇Φ (Oppenheim et al.'s eq. 42). Write:

- Γ for the decoherence rate of a split Δx;
- S_a for the white acceleration noise of the same particle (two-sided).

By Cauchy–Schwarz, for every pair of kernels the trade-off allows:

```
Γ(Δx) · S_a  ≥  (M²/4) · I(Δx)²,
I = ∫ d³q/(2π)³ (4πG/q²) |F(q)|² |q_z| √(1 − cos q_zΔx)
```

F(q) is the particle's normalized mass form factor. The bound is tight: a saturating pair
of kernels reaches it to 10⁻⁶, and random kernels on or above the trade-off line never
beat it (tests). It doesn't depend on the kernels' shapes, ranges or anisotropy. Only
the smearing g(q) of the source enters. For a split much larger than the body,
I → (2√2 G/π²R²)·(9/4) for a uniform sphere.

**Design-A diamond** (R = 1.007 µm, split 721 µm), with Γ held to the experiment's own
dephasing budget of 0.12 /s:

| Source smearing R₀ | Γ·S_a ≥ (m²/s⁴) | Acceleration noise CQ gravity must produce (one-sided) | ÷ design-A requirement (1.3×10⁻¹⁷) |
|---|---|---|---|
| local, or 0.54 Å | 1.01×10⁻²⁵ | 1.3×10⁻¹² m s⁻²/√Hz | 1.0×10⁵ |
| 1 µm | 3.5×10⁻²⁷ | 2.4×10⁻¹³ | 1.9×10⁴ |
| 10 µm | 5.1×10⁻³¹ | 2.9×10⁻¹⁵ | 2.3×10² |
| 52 µm | 7.4×10⁻³⁴ | 1.1×10⁻¹⁶ | 8.6 |

- The ratio stays above 1 up to R₀ = **157 µm**. That's three times beyond the largest
  smearing the inverse-square law allows (52 µm).
- **The falsifiable number:** a design-A diamond that stays coherent within its budget,
  and whose own acceleration noise meets the design requirement, excludes **every**
  continuous Markovian CQ gravity, whatever its kernels. The conditions are the same as
  in P2, but without P2's back-action step. Gravitational entanglement isn't needed.
- A uniform sphere was used for F(q). Real nuclei only add to I, so the bound is
  conservative.

## P4. Small splits: the minimum heating of matter, and a correction (FOLLOWS)

For Δx ≪ R, decoherence becomes momentum diffusion, and the trade-off becomes a heating
floor for the centre of mass:

```
d⟨p_z²⟩/dt  ≥  (4π/3) ħ G M² ∫ρ̂² d³x        (ρ̂: the normalized mass density, smeared by R₀)
```

Applied to each nucleus, which is a uniform sphere of radius 1.2 A^⅓ fm:

| | Internal heating, local coupling |
|---|---|
| Diamond | 0.51 W/kg |
| Silica | 0.31 W/kg |
| The Earth's internal heat flow (LIT, recalled) | 7.9×10⁻¹² W/kg |

**Local continuous CQ gravity is excluded by a factor of 4×10¹⁰.** This agrees with
Oppenheim et al.'s own remark that continuous models with noise everywhere are ruled out.
The radiation bound already demands R₀ ≥ 0.54 Å (LIT: Donadi et al. 2021).

**Correction to COLLECTIVE.md.**
- **What was wrong.** The heating formula ħG/(4√π R₀³) treats nuclei as points. At
  R₀ = a it gave 10⁵⁶–10⁶⁰ W/kg, which was quoted in the README and elsewhere. Real
  nuclei are about 10⁻¹⁵ m across, so below that size the nucleus, not R₀, sets the
  smearing, and the true figure at R₀ = a is **0.5 W/kg**.
- **Why the conclusion stands.** That is still 6×10¹⁰ times the heat any matter shows,
  and the same noise is excluded by the radiation bound.
- **Where it is fixed.** `src/stur_thermo_gravity.py` Q3 now prints both numbers. The
  two formulas agree to 10⁻⁴ once R₀ ≫ 1 fm.

**Heating can't reach the allowed models.** At R₀ = 0.54 Å the centre-of-mass floor for
a 100 nm silica sphere in a 50 kHz trap is 3×10⁻¹² phonons/s, which is unmeasurable.
For the R₀ still allowed, the deciding test is coherence at a large split (P2, P3).

## What this means for the theory

| Gravity is … | Γ (one diamond, 721 µm) | Its own acceleration noise | Two diamonds entangle? |
|---|---|---|---|
| collective (this theory; also perturbative quantum gravity) | 0 | 0 | yes, Δφ = 2.19 rad |
| continuous Markovian CQ (Oppenheim), any kernels, R₀ ≤ 157 µm | Γ·S_a ≥ bound above | ≥ 1.3×10⁻¹² m s⁻²/√Hz if Γ ≤ 0.12 /s | no |
| the same, with matter feeling the noisy potential (P2) | ≥ 169.5 /s for R₀ ≲ 0.1 µm | — | no |

**What is and isn't new.**
- **Known physics:** the trade-off (Oppenheim et al.); its Diósi–Penrose floor once the
  noise acts back (Tilloy–Diósi 2016; Oppenheim et al.'s appendix D.2 notes that the DP
  kernel saturates it).
- **This project's:**
  - the shape-free one-particle product bound Γ·S_a ≥ (M²/4)I², and its numbers for
    design A;
  - the finite-nucleus heating floor, and the correction to COLLECTIVE.md.

  I didn't find either in the papers I read. That isn't proof of novelty.
- **What a positive result would not show.** A coherent, quiet diamond rules out CQ
  gravity, but it confirms λ = 1, and λ = 1 is also ordinary perturbative quantum
  gravity's prediction. It doesn't single out this theory.

**Scope.**
- The bound covers continuous Markovian models with translation-invariant Gaussian
  kernels.
- It doesn't cover:
  - discrete (jump) CQ models whose noise sits only where the mass is (Oppenheim et al.'s
    eq. 46, which they find not yet ruled out);
  - kernels tied to the Earth's background potential;
  - non-Markovian classical gravity.
- The Earth's heat-flow figure is recalled, not retrieved.
- The 50 kHz trap frequency is an assumption.
