# What experiments could check

*Research notes, not peer reviewed. Labels mark what is established physics, what is computed here, and what holds only under stated assumptions.*

Each item below is what the bookkeeping equation of [DERIVATION.md](DERIVATION.md) gives.
Most are also what standard physics predicts. The gravity items assume gravity follows
each branch, which is an open experimental question:

```
ρᵢⱼ(t) = ρᵢⱼ(0) · ⟨Eⱼ|Eᵢ⟩ · e^{i(Sᵢ − Sⱼ)/ħ},
Sᵢ = S_matter[i] + S_EM[i] + (c⁴/16πG) ∫ eᵢ T[eᵢ] d⁴x,   G = πa²c³/(N c_s ħ)
```

Every number is computed by the script named next to it and pinned by `tests/`.

## Gravity

**1. Two masses become entangled through gravity alone,** if gravity's field follows
each branch, as perturbative quantum gravity predicts ([COLLECTIVE.md](COLLECTIVE.md)
argues for it under stated assumptions). Two diamonds, each held in two places, pick up
the entangling phase of their own torsion field.

| Design | Mass | Split | Phase Δφ | Runs to a 3σ witness |
|---|---|---|---|---|
| Baseline (parallel) | 10⁻¹⁴ kg | 250 µm, 2.5 s | 0.594 rad | 433 |
| Design A | 1.5×10⁻¹⁴ kg | 721 µm, 3.24 s | **2.19 rad** | **270 (0.6 h)** |

Requirements, with the derived gas-collision rate: vacuum below 7.6×10⁻¹⁵ Pa (N₂),
internal temperature below 1.9 K, spin coherence above 1.4 s, acceleration noise below
3.1×10⁻¹⁷ m s⁻²/√Hz, zero net charge. The earlier interpolated rate was 4.19× higher,
and gave 565 runs.
Source: `src/stur_gravity_full.py`, [GRAVITY_ENTANGLEMENT.md](GRAVITY_ENTANGLEMENT.md).

**2. One mass keeps its superposition.** A design-A diamond held in two places keeps
its full coherence for 3.24 s: gravity adds no decoherence of its own. Any Markovian
statistical gravity would leave at most 1.3% coherence (at 52 µm smearing, the
largest Newton's law allows), and 10⁻²³⁹ at the radiation bound. This is the first
experiment to run, since it needs one diamond, not two. Source:
`src/stur_thermo_gravity.py`.

**3. Gravity heats nothing.** Ordinary matter receives no heating from gravitational
noise. A Markovian statistical gravity smeared at the theory's own cutoff would deliver
0.5 W/kg, limited by the size of the nuclei. That is 6×10¹⁰ times the Earth's heat flow.
(An earlier version said 10⁵⁶–10⁶⁰ W/kg, a point-nucleus artefact.) Source:
`src/stur_thermo_gravity.py`, `src/stur_oppenheim.py`.

**3′. Classical (Oppenheim) gravity is squeezed by one particle.** The trade-off between
decoherence and diffusion bounds one particle's decoherence rate Γ times its acceleration
noise S_a: Γ·S_a ≥ (M²/4)I², for every allowed pair of kernels. Suppose a design-A
diamond keeps its coherence within the experiment's 0.12 /s budget. Then a classical
gravity must shake it with at least 1.3×10⁻¹² m s⁻²/√Hz, which is 4×10⁴ times the
noise the experiment already requires. This holds for every source smearing up to
100 µm.
Source: `src/stur_oppenheim.py`, [OPPENHEIM.md](OPPENHEIM.md).

**3″. Every classical–quantum gravity, discrete models included, is squeezed by a small
split.** Oppenheim et al.'s kernel-free observational trade-off (their appendix B.4),
applied with the body's force response as the test function, gives Γ·S_a ≥ (F_LR/M)²/8, where F_LR is the pull between the branches. The pull is largest at a split of
one radius. A design-A diamond coherent at 0.12 /s across 1 µm requires any classical
gravity to shake it with at least 6.7×10⁻¹³ m s⁻²/√Hz. Source: `src/stur_oppenheim.py`
P5.

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

## What a result would and would not show

- **None of predictions 1–8 distinguishes this theory from standard physics.**
  - Predictions 1–4 (λ = 1) are also what perturbative quantum gravity predicts. A
    positive result rules out classical gravity (Diósi–Penrose, Tilloy–Diósi,
    Oppenheim's continuous models). It doesn't confirm this framework over standard
    physics. Only a null result would be new physics.
  - Predictions 5–8 are general relativity and standard quantum mechanics.
- **Prediction 7 is cheap and decisive against the original STUR postulate.** That
  postulate predicts the opposite temperature dependence. Prediction 7 can't come out
  in STUR's favour.
- **The diamond experiments are far beyond current reach.** They need a mass in
  superposition 4×10⁸ times the current record, and vibration noise about 57 times
  below LISA Pathfinder ([GRAVITY_ENTANGLEMENT.md](GRAVITY_ENTANGLEMENT.md)).
- **This project's own results, as distinct from synthesis of known physics:**
  - (the bounds 3′ and 3″ are worked examples within a systematic literature: Fabiano et
    al. 2026, Angeli et al. 2025; NOVELTY.md);
  - the exact identity −ln V = 2 Var(ΔN) behind 7;
  - the conditional particle-physics result N_c = N_g = 3 ([NOTE_331.md](NOTE_331.md)).

## What sets the numbers

The only measured input is G. It fixes the ratio a²/N of the entanglement cutoff to the
number of fields: a = 0.31 ℓ_P for one field and 3.1 ℓ_P for a hundred. The particle
content is taken from the Standard Model.
