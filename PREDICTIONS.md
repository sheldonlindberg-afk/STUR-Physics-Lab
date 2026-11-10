# Predictions

Each prediction below follows from the equation of [DERIVATION.md](DERIVATION.md):

```
ρᵢⱼ(t) = ρᵢⱼ(0) · ⟨Eⱼ|Eᵢ⟩ · e^{i(Sᵢ − Sⱼ)/ħ},
Sᵢ = S_matter[i] + S_EM[i] + (c⁴/16πG) ∫ eᵢ T[eᵢ] d⁴x,   G = πa²c³/(N c_s ħ)
```

Every number is computed by the script named next to it and pinned by `tests/`.

## Gravity

**1. Two masses become entangled through gravity alone.** Gravity's field follows each
branch ([COLLECTIVE.md](COLLECTIVE.md)). Two diamonds, each held in two places, pick up
the entangling phase of their own torsion field.

| Design | Mass | Split | Phase Δφ | Runs to a 3σ witness |
|---|---|---|---|---|
| Baseline (parallel) | 10⁻¹⁴ kg | 250 µm, 2.5 s | 0.594 rad | 433 |
| Design A | 1.5×10⁻¹⁴ kg | 721 µm, 3.24 s | **2.19 rad** | **565 (1.3 h)** |

Requirements: vacuum below 1.8×10⁻¹⁵ Pa, internal temperature below 1.2 K, spin
coherence above 2.1 s, acceleration noise below 1.3×10⁻¹⁷ m s⁻²/√Hz, zero net charge.
Source: `src/stur_gravity_full.py`, [GRAVITY_ENTANGLEMENT.md](GRAVITY_ENTANGLEMENT.md).

**2. One mass keeps its superposition.** A design-A diamond held in two places keeps
its full coherence for 3.24 s: gravity adds no decoherence of its own. Any gravity that
was a statistical average would leave at most 1.3% coherence (at 52 µm smearing, the
largest Newton's law allows), and 10⁻²³⁹ at the radiation bound. This is the first
experiment to run, since it needs one diamond, not two. Source:
`src/stur_thermo_gravity.py`.

**3. Gravity heats nothing.** Ordinary matter receives no heating from gravitational
noise. A statistical gravity at the theory's own cutoff would deliver 10⁵⁶–10⁶⁰ W/kg.
Source: `src/stur_thermo_gravity.py`.

**4. Gravity keeps no record of a single mass.** Splitting a design-A diamond emits
1.4×10⁻⁵⁹ gravitons, so gravity never reveals which branch happened. Source:
`src/stur_tegr.py`, [TEGR.md](TEGR.md) E6.

**5. The classical limit is general relativity.** From the TEGR solution:

| Test | Prediction | Measured |
|---|---|---|
| Mercury's perihelion | 42.98″/century | 42.98″ |
| Light bending at the solar limb | 1.7512″ | γ = 0.99983 ± 0.00045 |
| PPN γ | 1 | 1 + (2.1 ± 2.3)×10⁻⁵ |
| GPS clock offset | +38.54 µs/day | 38.6 |

Source: `src/stur_tegr_gr.py`.

## Measurement

**6. Visibility is the record overlap.** V = |⟨E₁|E₂⟩| and D² + V² = 1 at every detector
strength. No observer is needed. Electron fringes fade near a surface because image
charges record the path, as Sonnentag & Hasselbach observed (2007). Source:
`src/stur_measurement.py`.

**7. Visibility loss counts quanta, so heat destroys more of it.** For a spin given a
state-dependent kick ±α on a motional mode at temperature T:

```
−ln V = 2 Var(ΔN) = 2⟨ΔN⟩ coth(ħω / 2k_BT)
```

At fixed energy deposited, the loss *grows* with temperature. One trapped ion shows it.
With |α|² = 0.1, going from n̄ = 0.1 to n̄ = 5 lowers the spin contrast from 0.787 to
**0.111**, and sideband spectroscopy before and after gives Var(ΔN) directly.
Source: `src/stur_lab_test.py` (Fock space, to 7.5×10⁻¹¹).

**8. Probabilities are |amplitude|².** Any other power fails to sum to 1 or lets one
side of an entangled pair signal to the other. Source: `src/stur_born.py`,
[BORN.md](BORN.md).

## Confinement

**9. A confining string's entanglement entropy stops growing while its modular energy
grows with its length.** This can be measured in Rydberg-atom and trapped-ion
simulators. Source: `src/stur_confinement.py`, `src/stur_z2_higgs.py`.

## What sets the numbers

The only measured input is G. It fixes the ratio a²/N of the entanglement cutoff to the
number of fields: a = 0.31 ℓ_P for one field and 3.1 ℓ_P for a hundred. The particle
content is taken from the Standard Model.
