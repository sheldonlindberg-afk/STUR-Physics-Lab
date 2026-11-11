<p align="center">
  <img src="assets/4.13.png" alt="STUR Physics Lab logo" width="160"/>
</p>

<h1 align="center">STUR Physics Lab: Gravity and the Quantum</h1>

<p align="center">
  <strong>A science-education project. A plain-language guide to gravity, quantum physics and measurement, plus the author's research notes. Established physics, worked examples and open questions are labelled separately, and every number is reproduced by open code. Independent work, not peer reviewed.</strong>
</p>

<p align="center">
  <a href="https://github.com/sheldonlindberg-afk/STUR-Physics-Lab/actions/workflows/tests.yml"><img src="https://github.com/sheldonlindberg-afk/STUR-Physics-Lab/actions/workflows/tests.yml/badge.svg" alt="Tests"></a>
  <a href="https://creativecommons.org/publicdomain/zero/1.0/"><img src="https://img.shields.io/badge/License-CC0_1.0-lightgrey.svg" alt="License: CC0-1.0"></a>
</p>

<p align="center">
  <a href="https://sheldonlindberg-afk.github.io/STUR-Physics-Lab/"><strong>Open the guide &rarr;</strong></a>
  &nbsp;&middot;&nbsp; <a href="https://sheldonlindberg-afk.github.io/STUR-Physics-Lab/technical.html">Research notes</a>
  &nbsp;&middot;&nbsp; <a href="NOTE_331.md">3-3-1 note</a>
</p>

---

## What's here

- **The guide** ([site](https://sheldonlindberg-afk.github.io/STUR-Physics-Lab/), `index.html`). For
  students, teachers and anyone curious:
  - Einstein's gravity told as a twist instead of a curve (teleparallel gravity, TEGR),
    with GR's classic tests recomputed;
  - the open question of whether gravity is quantum, and the two-diamond experiment
    that could decide it;
  - the research idea that gravity is tied to the entanglement of empty space;
  - decoherence: why records, not observers, erase interference;
  - common quantum myths, and what mainstream physics actually says.
- **Research notes** (`technical.html` and the `.md` reports below). Known physics of
  measurement and gravity, organised into one bookkeeping equation and recomputed in
  code. A synthesis, not a new theory.
- **A standalone particle-physics note** ([NOTE_331.md](NOTE_331.md)): in 3-3-1 models,
  requiring every coupling to stay perturbative to the Planck scale selects 3 colours =
  3 generations. Conditional, and the one candidate original result here; an expert
  reading is still needed ([NOVELTY.md](NOVELTY.md)).

## The bookkeeping equation (research notes)

```
ρᵢⱼ(t) = ρᵢⱼ(0) · ⟨Eⱼ|Eᵢ⟩ · e^{i(Sᵢ − Sⱼ)/ħ}

Sᵢ = S_matter[i] + S_EM[i] + (c⁴/16πG) ∫ eᵢ T[eᵢ] d⁴x        gravity as TEGR torsion
G  = π a² c³ / (N c_s ħ),   c_s = 0.3046                     Jacobson's hypothesis
p  = |c|²                                                    Born rule (Gleason, Zurek)
```

This writes known physics in one place; it is not a new theory.

- **The branches:** a system in a superposition carries, in each branch, its own
  configuration of every field it sources: detectors, light, its own electric field
  and, if gravity is quantum, gravity's tetrad eᵢ.
- **The overlap ⟨Eⱼ|Eᵢ⟩:** how far the fields have kept a record of which branch
  happened. This is decoherence: it removes interference without any observer. Why one
  outcome is seen is a question of interpretation that it leaves open.
- **The phase:** the difference in action between branches, including the
  gravitational field's own action.
- **The G line:** Jacobson's (1995) argument ties G to vacuum entanglement per area,
  assuming local equilibrium on every horizon. That premise is not established, and the
  formula relates G to unknowns (a²/N); it doesn't predict G.

## The steps, and their status

| Step | Result | Status | Report |
|---|---|---|---|
| Born rule | p = \|c\|² | Published arguments (Zurek, Gleason, no-signalling) reproduced; each assumes locality or non-contextuality; still debated | [BORN.md](BORN.md) |
| Area law | The vacuum's entanglement across any surface: S = 0.3046 (R/a)² per field | Established (Srednicki); recomputed | [UNIFICATION.md](UNIFICATION.md) |
| Unruh / modular structure | The vacuum is thermal to every accelerated observer: K = 2π × boost | Established (Bisognano–Wichmann); checked on a lattice | [UNIFICATION.md](UNIFICATION.md) |
| Field equations | Clausius on every local horizon gives Einstein's equations, with 1/4Għ = entanglement per area | Jacobson's hypothesis; algebra re-checked, premise assumed | [DERIVATION.md](DERIVATION.md) |
| Gravity as torsion | The TEGR action gives the same equations; Schwarzschild is the unique static solution | Established; recomputed | [TEGR.md](TEGR.md) |
| Gravity follows each branch | A Markovian statistical gravity smeared at the entanglement cutoff would heat matter at 0.5 W/kg, 6×10¹⁰ × the Earth's heat flow | Conditional: holds **only under R₀ = a and Markovian dynamics**. Experiment decides | [COLLECTIVE.md](COLLECTIVE.md) |
| Classical gravity's trade-off | Oppenheim's decoherence–diffusion bound, minimized, is the Diósi–Penrose floor. One particle obeys Γ·S_a ≥ (M²/4)I² for any kernels | Worked example within existing literature, not new | [OPPENHEIM.md](OPPENHEIM.md) |
| Measurement | V = \|⟨E₁\|E₂⟩\| | Established (Englert 1996); recomputed | [MEASUREMENT.md](MEASUREMENT.md) |

## Where this stands

- **A synthesis of known physics.** Every ingredient is published physics: decoherence,
  the Born-rule arguments (Zurek, Gleason), Jacobson's thermodynamic gravity, and TEGR.
  The combination and the computed checks are this project's.
- **Whether gravity follows each branch (λ = 1) is open.** The argument here works only
  under two stated assumptions: a statistical gravity smeared at the entanglement cutoff
  (R₀ = a), with Markovian dynamics. With a larger R₀ or memory in the dynamics,
  experiment decides ([COLLECTIVE.md](COLLECTIVE.md), [OPPENHEIM.md](OPPENHEIM.md)).
- **Confirming λ = 1 wouldn't single out these notes.** Perturbative quantum gravity
  predicts the same thing. The diamond experiments rule classical gravity in or out,
  Oppenheim's model included.
- **The diamond experiments are far off.** They need 4×10⁸ times today's largest mass in
  superposition, and vibration noise about 57 times below LISA Pathfinder.
- **What might be new:** only the 3-3-1 selection in [NOTE_331.md](NOTE_331.md), and it
  is conditional and unreviewed. The classical-gravity bounds in
  [OPPENHEIM.md](OPPENHEIM.md) are worked examples within a systematic literature
  (Fabiano et al. 2026; Angeli et al. 2025; see [NOVELTY.md](NOVELTY.md)). The trapped-ion
  identity −ln V = 2 Var(ΔN) is a worked example whose novelty hasn't been checked.
- **Open tensions,** and what was checked: [CONSISTENCY.md](CONSISTENCY.md).
- **Derived, rechecked, or underivable:** [RECHECK.md](RECHECK.md). Every failed
  claim has been reconfirmed by independent code (15 of 15).

## What experiments could check

| Prediction | Number | Experiment |
|---|---|---|
| If gravity is quantum, two diamonds entangle through gravity alone (perturbative quantum gravity's prediction) | Δφ = 2.19 rad; 270 runs (0.6 h) at the published targets, which need 4×10⁸ × today's largest superposed mass | Levitated-diamond interferometry ([GRAVITY_ENTANGLEMENT.md](GRAVITY_ENTANGLEMENT.md)) |
| If gravity follows each branch, one diamond keeps its superposition | Full coherence for 3.24 s; any Markovian statistical gravity with smearing ≤ 52 µm leaves ≤ 1.3% | Single-diamond interferometry ([COLLECTIVE.md](COLLECTIVE.md)) |
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
index.html                the plain-language guide (GitHub Pages)
technical.html            the research notes, with the interactive calculators
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
                          equation to these notes, including the wider search for a
                          unifying equation (UNIFYING_SEARCH.md, UNIFICATION.md, ...)
archive/                  earlier versions, kept for the record
```

## Archive

Earlier, superseded versions are kept for the record. They are not maintained, and their
claims are not endorsed by the current work:

- [`archive/resistance-equation/`](archive/resistance-equation/): the original STUR
  resistance equation that this work grew out of, with its derivation record
  ([PDF](docs/STUR_Resistance_Equation_Derivation_Record.pdf)) and `src/stur_verify.py`.
- [`archive/stur-roll/`](archive/stur-roll/): **STUR-ROLL** (cosmic birefringence,
  |β| = α/2 = 0.2091°), with its site, docs, code and tests (still run in CI).
- [`archive/v7-toe/`](archive/v7-toe/) and [`archive/genesis-v10-stur-b/`](archive/genesis-v10-stur-b/):
  older material. See [`archive/README.md`](archive/README.md).

## License

CC0 1.0. See [LICENSE](LICENSE).
