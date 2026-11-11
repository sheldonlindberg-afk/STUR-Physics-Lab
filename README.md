<p align="center">
  <img src="assets/4.13.png" alt="STUR Physics Lab logo" width="160"/>
</p>

<h1 align="center">STUR: Measurement and Gravity from the Quantum Level Up</h1>

<p align="center">
  <strong>One equation for the double slit, measurement and gravity, built from known quantum physics. Gravity's strength comes from vacuum entanglement, and its field follows each branch of a superposition. That is also what standard quantum gravity predicts, so the experiments below test classical gravity, not this theory alone.</strong>
</p>

<p align="center">
  <a href="https://github.com/sheldonlindberg-afk/STUR-Physics-Lab/actions/workflows/tests.yml"><img src="https://github.com/sheldonlindberg-afk/STUR-Physics-Lab/actions/workflows/tests.yml/badge.svg" alt="Tests"></a>
  <a href="https://creativecommons.org/publicdomain/zero/1.0/"><img src="https://img.shields.io/badge/License-CC0_1.0-lightgrey.svg" alt="License: CC0-1.0"></a>
</p>

<p align="center">
  <a href="https://sheldonlindberg-afk.github.io/STUR-Physics-Lab/"><strong>Open the interactive site &rarr;</strong></a>
  &nbsp;&middot;&nbsp; <a href="DERIVATION.md">Derivation</a>
  &nbsp;&middot;&nbsp; <a href="PREDICTIONS.md">Predictions</a>
</p>

---

## The equation

```
ρᵢⱼ(t) = ρᵢⱼ(0) · ⟨Eⱼ|Eᵢ⟩ · e^{i(Sᵢ − Sⱼ)/ħ}

Sᵢ = S_matter[i] + S_EM[i] + (c⁴/16πG) ∫ eᵢ T[eᵢ] d⁴x        gravity as TEGR torsion
G  = π a² c³ / (N c_s ħ),   c_s = 0.3046                     from vacuum entanglement
p  = |c|²                                                    derived
```

- **The branches:** a system in a superposition carries, in each branch, its own
  configuration of every field it sources. That includes detectors, light, its own
  electric field, and gravity's tetrad eᵢ.
- **The overlap ⟨Eⱼ|Eᵢ⟩:** how far the fields have kept a record of which branch
  happened. That is what makes outcomes definite. No observer is needed.
- **The phase:** the difference in action between branches, including the
  gravitational field's own action.
- **The strength of gravity, G:** how entangled the quantum vacuum is per unit area.

## The derivation

| Step | Result | Report |
|---|---|---|
| Born rule | p = \|c\|², from unitarity with locality or non-contextuality | [BORN.md](BORN.md) |
| Area law | The vacuum's entanglement across any surface: S = 0.3046 (R/a)² per field | [UNIFICATION.md](UNIFICATION.md) |
| Unruh / modular structure | The vacuum is thermal to every accelerated observer: K = 2π × boost | [UNIFICATION.md](UNIFICATION.md) |
| Field equations | Clausius on every local horizon gives Einstein's equations (Jacobson), with 1/4Għ = entanglement per area | [DERIVATION.md](DERIVATION.md) |
| Gravity as torsion | The TEGR action gives the same equations; Schwarzschild is the unique static solution | [TEGR.md](TEGR.md) |
| Gravity follows each branch (conditional) | A Markovian statistical gravity smeared at the entanglement cutoff would heat matter at 0.5 W/kg, 6×10¹⁰ × the Earth's heat flow. Derived **under R₀ = a and Markovian dynamics**, not unconditionally | [COLLECTIVE.md](COLLECTIVE.md) |
| Classical gravity's trade-off | Oppenheim's decoherence–diffusion bound, minimized, is the Diósi–Penrose floor. One particle obeys Γ·S_a ≥ (M²/4)I² for any kernels | [OPPENHEIM.md](OPPENHEIM.md) |
| Measurement | V = \|⟨E₁\|E₂⟩\|; the electron's field is in both branches as an amplitude | [MEASUREMENT.md](MEASUREMENT.md) |

The only measured input is G. It fixes the ratio a²/N of the cutoff to the number of
fields: a = 0.31 ℓ_P for one field and 3.1 ℓ_P for a hundred. The coefficient 0.3046
depends on the lattice regularization, so the G formula doesn't predict G.

## Where this stands

- **A synthesis of known physics.** Every ingredient is published physics: decoherence,
  the Born rule (Zurek, Gleason), Jacobson's thermodynamic gravity, and TEGR. The
  combination and the computed checks are this project's.
- **Gravity following each branch (λ = 1) is derived only conditionally.** The argument
  assumes a statistical gravity is smeared at the entanglement cutoff (R₀ = a) and is
  Markovian. With a larger R₀ put in by hand, or memory in the dynamics, experiment
  decides ([COLLECTIVE.md](COLLECTIVE.md), [OPPENHEIM.md](OPPENHEIM.md)).
- **Confirming λ = 1 wouldn't single this theory out.** Perturbative quantum gravity
  predicts the same thing. The diamond experiments rule classical gravity in or out,
  Oppenheim's model included. Only a null result would be new physics.
- **The diamond experiments are far off.** They need 4×10⁸ times today's largest mass in
  superposition, and vibration noise about 57 times below LISA Pathfinder.
- **This project's own results:**
  - none on the classical-gravity side: the bounds in [OPPENHEIM.md](OPPENHEIM.md) are worked examples within a systematic literature (Fabiano et al. 2026; Angeli et al. 2025; see [NOVELTY.md](NOVELTY.md));
  - the identity −ln V = 2 Var(ΔN);
  - a conditional particle-physics result: in 3-3-1 models, perturbativity to the
    Planck scale selects 3 colours = 3 generations ([NOTE_331.md](NOTE_331.md)). It is
    independent of the measurement–gravity equation: the two threads share a method, not
    a derivation.
- **Open tensions,** and what was checked: [CONSISTENCY.md](CONSISTENCY.md).
- **Derived now, rechecked, or underivable:** [RECHECK.md](RECHECK.md). Every failed
  claim has been reconfirmed by independent code (15 of 15). The gas-collision rate and
  Jacobson's step are now derived.

## What it predicts

| Prediction | Number | Experiment |
|---|---|---|
| Two diamonds entangle through gravity alone (also perturbative quantum gravity's prediction) | Δφ = 2.19 rad; 270 runs (0.6 h) at the published targets, which need 4×10⁸ × today's largest superposed mass | Levitated-diamond interferometry ([GRAVITY_ENTANGLEMENT.md](GRAVITY_ENTANGLEMENT.md)) |
| One diamond keeps its superposition | Full coherence for 3.24 s; any Markovian statistical gravity with smearing ≤ 52 µm leaves ≤ 1.3% | Single-diamond interferometry ([COLLECTIVE.md](COLLECTIVE.md)) |
| Classical (Oppenheim) gravity is squeezed by one particle | Coherent at 0.12 /s ⇒ CQ acceleration noise ≥ 1.3×10⁻¹² m s⁻²/√Hz, 4×10⁴ × design A's requirement | Same diamond plus its accelerometry ([OPPENHEIM.md](OPPENHEIM.md)) |
| Every CQ gravity, discrete ones included (Oppenheim et al.'s kernel-free trade-off, applied to a small split) | Coherent at 0.12 /s across a split of one radius ⇒ CQ acceleration noise ≥ 6.7×10⁻¹³ m s⁻²/√Hz | One diamond, small split ([OPPENHEIM.md](OPPENHEIM.md) P5) |
| Gravity keeps no record of one mass | 1.4×10⁻⁵⁹ gravitons emitted per split | — ([TEGR.md](TEGR.md)) |
| The classical limit is general relativity | Perihelion 42.98″/century, light bending 1.7512″, γ = 1, GPS +38.54 µs/day | Observed |
| Visibility loss counts quanta, so heat destroys more of it | −ln V = 2 Var(ΔN); contrast 0.787 → 0.111 from n̄ = 0.1 to 5 | One trapped ion (`src/stur_lab_test.py`) |
| A confining string's entropy saturates while its modular energy grows | — | Rydberg-atom and trapped-ion simulators ([CONFINEMENT.md](CONFINEMENT.md)) |

Full list, with requirements and sources: [PREDICTIONS.md](PREDICTIONS.md).

## Reproduce

```bash
pip install -r requirements.txt pytest
python3 src/stur_derivation.py      # the whole chain, ~30 s
python3 src/stur_thermo_gravity.py  # why gravity follows each branch, ~6 s
python3 src/stur_gravity_full.py    # the two-diamond design search, ~15 s
python3 src/stur_oppenheim.py       # classical (Oppenheim) gravity's trade-off, ~2 s
python -m pytest tests -q           # every number pinned (121 tests)
```

Each script writes its reference output to `results/`, and CI checks every number on
each push.

## Layout

```
index.html                the plain-language home page (GitHub Pages), TEGR first
technical.html            the full technical record, with the interactive calculators
assets/                   styles, scripts, icons and the social preview card
DERIVATION.md             the equation, step by step
PREDICTIONS.md            every prediction, with numbers and experiments
COLLECTIVE.md             why gravity's field follows each branch (conditions stated)
OPPENHEIM.md              classical-quantum gravity's trade-off, and a one-particle bound
NOTE_331.md               standalone note: 3 colours = 3 generations from 3-3-1 running
CONSISTENCY.md            what was checked, what was fixed, and the tensions that remain
RECHECK.md                derived now / failed and rechecked / cannot be derived, with reasons
NOVELTY.md                literature search: what is new, what was already known
BORN.md, MEASUREMENT.md, TEGR.md, GRAVITY_ENTANGLEMENT.md, EMERGENT.md
                          the supporting reports
src/                      one script per report; outputs in results/
tests/                    regression tests
REPORT.md                 development record: the route from the original STUR
                          equation to this theory, including the wider search for a
                          unifying equation (GOD_EQUATION.md, UNIFICATION.md, ...)
archive/                  earlier versions, kept for the record
```

## Archive

Earlier versions are preserved:

- [`archive/resistance-equation/`](archive/resistance-equation/): the original STUR
  resistance equation that this work grew out of, with its derivation record
  ([PDF](docs/STUR_Resistance_Equation_Derivation_Record.pdf)) and `src/stur_verify.py`.
- [`archive/stur-roll/`](archive/stur-roll/): **STUR-ROLL** (cosmic birefringence,
  |β| = α/2 = 0.2091°), with its site, docs, code and tests (still run in CI).
- [`archive/v7-toe/`](archive/v7-toe/) and [`archive/genesis-v10-stur-b/`](archive/genesis-v10-stur-b/):
  older material. See [`archive/README.md`](archive/README.md).

## License

CC0 1.0. See [LICENSE](LICENSE).
