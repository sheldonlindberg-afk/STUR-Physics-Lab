<p align="center">
  <img src="assets/4.13.png" alt="STUR Physics Lab logo" width="160"/>
</p>

<h1 align="center">STUR: Measurement and Gravity from the Quantum Level Up</h1>

<p align="center">
  <strong>One equation for the double slit, measurement and gravity, derived from quantum fields. Gravity's strength comes from vacuum entanglement, its field follows each branch of a superposition, and two diamonds will show it.</strong>
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
| Gravity follows each branch | A statistical gravity at the entanglement cutoff would heat matter at 10⁶⁰ W/kg | [COLLECTIVE.md](COLLECTIVE.md) |
| Measurement | V = \|⟨E₁\|E₂⟩\|; the electron's field is in both branches as an amplitude | [MEASUREMENT.md](MEASUREMENT.md) |

The only measured input is G. It fixes the ratio a²/N of the cutoff to the number of
fields: a = 0.31 ℓ_P for one field and 3.1 ℓ_P for a hundred.

## What it predicts

| Prediction | Number | Experiment |
|---|---|---|
| Two diamonds entangle through gravity alone | Δφ = 2.19 rad; 565 runs (1.3 h) at the published targets | Levitated-diamond interferometry ([GRAVITY_ENTANGLEMENT.md](GRAVITY_ENTANGLEMENT.md)) |
| One diamond keeps its superposition | Full coherence for 3.24 s; any statistical gravity leaves ≤ 1.3% | Single-diamond interferometry ([COLLECTIVE.md](COLLECTIVE.md)) |
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
python -m pytest tests -q           # every number pinned (90 tests)
```

Each script writes its reference output to `results/`, and CI checks every number on
each push.

## Layout

```
index.html, assets/       the site (GitHub Pages)
DERIVATION.md             the equation, step by step
PREDICTIONS.md            every prediction, with numbers and experiments
COLLECTIVE.md             why gravity's field follows each branch
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
