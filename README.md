<p align="center">
  <img src="assets/logo.svg" alt="" width="120"/>
</p>

<h1 align="center">Gravity and the Quantum: Worked Examples</h1>

<p align="center">
  <strong>Reproducible worked examples at the gravity–quantum interface, for physics students and physicists, plus one research note.</strong><br>
  Every number comes from a script in <code>src/</code> and is pinned by a test that runs on every commit.<br>
  Independent work, not peer reviewed.
</p>

<p align="center">
  <a href="https://github.com/sheldonlindberg-afk/STUR-Physics-Lab/actions/workflows/tests.yml"><img src="https://github.com/sheldonlindberg-afk/STUR-Physics-Lab/actions/workflows/tests.yml/badge.svg" alt="Tests"></a>
  <a href="https://creativecommons.org/publicdomain/zero/1.0/"><img src="https://img.shields.io/badge/License-CC0_1.0-lightgrey.svg" alt="License: CC0-1.0"></a>
</p>

<p align="center">
  <a href="paper/note331.pdf"><strong>3-3-1 note (PDF)</strong></a>
  &nbsp;&middot;&nbsp; <a href="notebooks/">Notebooks</a>
  &nbsp;&middot;&nbsp; <a href="https://sheldonlindberg-afk.github.io/STUR-Physics-Lab/">Website</a>
  &nbsp;&middot;&nbsp; <a href="https://sheldonlindberg-afk.github.io/STUR-Physics-Lab/technical.html">Research notes</a>
</p>

---

## For researchers: three colours and three generations in 3-3-1 models

**[paper/note331.pdf](paper/note331.pdf)** (LaTeX: [paper/note331.tex](paper/note331.tex);
extended notes: [NOTE_331.md](NOTE_331.md))

In SU(3)_C × SU(3)_L × U(1)_X models, keep the number of colours N_c general, take no
generation or neutrino number from experiment, and require every gauge coupling to stay
perturbative to the Planck scale.

- The SU(3)_L anomaly plus asymptotic freedom of colour force N_c to be odd and N_g = N_c.
  Witten's global anomaly then holds automatically.
- SU(3)_L running excludes N_c ≥ 7.
- U(1)_X running excludes N_c = 5.

Only **N_c = N_g = 3** survives, with quark charges ⅔ and −⅓. The selection holds:
- at two loops, including two-loop Yukawa terms, and at three loops in the gauge and
  matter sector;
- with one-loop threshold matching across the heavy spectrum;
- for 3-3-1 scales of 2–30 TeV;
- in both variants β = ±1/√3 (for β = +1/√3, only if its heavy charged leptons are above
  about 0.6 TeV; see below).

Requiring the scalar sector to stay perturbative to M_Pl then bounds the exotic quarks
below 1.4–1.8 M_V.
A recast of the ATLAS 13 TeV, 139 fb⁻¹ dilepton search puts the Z′ above 4.6–5.2 TeV for
β = +1/√3 and 4.0–5.0 TeV for β = −1/√3, depending on its decays
([`src/m331_zprime_recast.py`](src/m331_zprime_recast.py); validated against ATLAS's own
Z′_ψ and Z′_χ limits, using the official HEPData tables, and reproduced independently with
Pythia 8).

**Conditions:**
- the 3-3-1 framework;
- Planck-scale perturbativity;
- the measured TeV-scale electroweak couplings, which are an input, not a prediction.
  In the β = +1/√3 variant there is no comfortable margin. At α = 1 (three loops), N_c = 3
  reaches M_Pl only if the heavy charged leptons are heavier than 0.56 ± 0.11 TeV with M_V
  at its LHC bound (0.96 TeV at M_V = 10 TeV). Lighter ones are not yet excluded by the
  LHC, and they push N_c = 3 below M_Pl too
  ([`src/m331_margin.py`](src/m331_margin.py); [NOTE_331.md §3e](NOTE_331.md)).

**Run it in one paste.** [`src/m331_standalone.py`](src/m331_standalone.py) reproduces the
whole selection in a single file that uses only the Python standard library: charges and
anomalies for general N_c, N_g = N_c, the Standard Model calibration, SU(3)_L and two-loop
U(1)_X running with Yukawas, one-loop thresholds across the heavy spectrum, and the
R-ratio cross-check. Copy it (the [website](https://sheldonlindberg-afk.github.io/STUR-Physics-Lab/#run331)
has a one-click **Copy Python script** button; on GitHub use *Copy raw file*) and paste it
into any Python 3.8+ runner, notebook or AI assistant's code tool. It runs in about 15 s
and ends with 20 PASS/FAIL checks against the numbers pinned here
([expected output](results/m331/standalone.txt)).

The closest prior work is Doff & Pisano (2000). The literature search is in
[NOVELTY.md](NOVELTY.md). Comments from 3-3-1 experts are welcome; please
[open an issue](https://github.com/sheldonlindberg-afk/STUR-Physics-Lab/issues).

## For researchers: the frame in teleparallel gravity and black-hole entropy

**[NOTE_TEGR.md](NOTE_TEGR.md)** (literature map: [QUANTUM_TEGR.md](QUANTUM_TEGR.md))

Teleparallel gravity (TEGR) equals GR up to a boundary term, plus one extra variable, the
local Lorentz frame. The note asks whether that frame contributes to black-hole entropy.

- **Classically, it changes where the entropy is booked, not the first law.** TEGR's
  Noether charge vanishes at the bifurcation surface, and the Wald entropy sits in the
  corner term instead. δM = TδS + ΦδQ comes out as in GR for every frame.
- **The frame's corner phase space is a Lorentz orbit through the dual area bivector over
  8πG,** for any metric. Its charges close into so(3,1), and its normal boost is conjugate
  to area/8πG.
- **Quantized, it gives a group-dependent logarithm** (1, 5 or 9 × ln a), not the area law
  and not Sen's universal 77/45. So the frame must be gauge in the measure, and TEGR's
  black-hole entropy is GR's.

All of it is computed by `src/stur_tegr_corner.py`, `src/stur_tegr_frame.py` and
`src/stur_tegr_logs.py`, and pinned by tests.

## For students: the symmetry-breaking ladder

**[SYMMETRY_LADDER.md](SYMMETRY_LADDER.md)** follows the forces down in energy, from the 3-3-1
scale to the two diamonds, with every step derived and checked in code:
- 3-3-1 → Standard Model → electromagnetism: the photon, the hypercharge matching and the
  W, Z, Z′ masses, from the gauge-boson mass matrix;
- chiral symmetry breaking: pions, the GMOR relation and the nuclear force;
- the Casimir–Polder force between the diamonds, from electrostatics and the dipole field;
- one-graviton exchange: Newton's law and the experiment's 2.19 rad phase;
- gravity as a broken de Sitter gauge theory (MacDowell–Mansouri), a reformulation of GR.

Gravity is not part of the gauge chain; the page says where each derivation stops.

**Run it in one paste.** [`src/ladder_standalone.py`](src/ladder_standalone.py) reproduces all
five rungs in a single file that uses only the Python standard library. Copy it (the
[website](https://sheldonlindberg-afk.github.io/STUR-Physics-Lab/#runladder) has a one-click
**Copy Python script** button) and paste it into any Python 3.8+ runner, notebook or AI
assistant's code tool. It runs in a few seconds and ends with 37 PASS/FAIL checks
([expected output](results/ladder/standalone.txt)).

## For students: notebooks with exercises

| Notebook | What it works out | Prerequisites |
|---|---|---|
| [01 TEGR and the classic tests](notebooks/01_tegr_classic_tests.ipynb) | Tetrad field equations → Schwarzschild; perihelion 42.98″/century, light bending 1.7512″, γ = 1, GPS +38.54 µs/day, all from geodesic integrals | Carroll ch. 1–5 |
| [02 Complementarity and decoherence](notebooks/02_complementarity_and_decoherence.ipynb) | Englert's V² + D² = 1; a thermal which-path environment, −ln V = 2 Var(ΔN) | Density matrices |
| [03 Gravity-mediated entanglement](notebooks/03_gravity_mediated_entanglement.ipynb) | Bose–Marletto–Vedral branch phases, concurrence, gas decoherence | Two-qubit entanglement |
| [04 The area law](notebooks/04_area_law.ipynb) | Srednicki's S ≈ 0.30 (R/a)² | Gaussian states |
| [05 Teleparallel gravity in 3D](notebooks/05_teleparallel_3d_quantum.ipynb) | 3D quantum gravity (Ponzano–Regge): exact 6j symbols, their Regge-action limit, the 2–3 move | Notebook 01; SU(2) recoupling |

Outputs are saved, so the notebooks read on GitHub, and CI re-runs them on every commit.

## The worked examples

Each piece is labelled by status. **Established** means published and tested;
**recomputed** means it is reproduced here in code; **conditional** means it holds only
under stated assumptions.

| Topic | Result | Status | Report |
|---|---|---|---|
| Teleparallel gravity | Schwarzschild is the unique static spherical solution of the TEGR field equations; GR's classic tests from its geodesics | Established; recomputed | [TEGR.md](TEGR.md) |
| Which-path records | V = \|⟨E₁\|E₂⟩\|, D² + V² = 1 | Established (Englert 1996); recomputed | [MEASUREMENT.md](MEASUREMENT.md) |
| Born rule | p = \|c\|² by envariance, Gleason-type additivity, no-signalling and branch frequencies | Published arguments reproduced; each assumes locality or non-contextuality | [BORN.md](BORN.md) |
| Area law, Unruh | S = 0.3046 (R/a)² per scalar; K = 2π × boost on a lattice | Established (Srednicki; Bisognano–Wichmann); recomputed | [DERIVATION.md](DERIVATION.md) |
| Jacobson's argument | Clausius on local horizons gives Einstein's equations, with 1/4Għ = entanglement per area | Hypothesis; algebra re-checked, premise assumed; relates G to unknowns, does not predict it | [DERIVATION.md](DERIVATION.md) |
| Two-diamond (BMV) design | Δφ = 2.19 rad; 270 runs (0.6 h) at the published targets, which need 4×10⁸ × today's largest superposed mass and vibration noise 57× below LISA Pathfinder | Worked example | [GRAVITY_ENTANGLEMENT.md](GRAVITY_ENTANGLEMENT.md) |
| Classical–quantum gravity | Oppenheim's decoherence–diffusion trade-off, minimized, is the Diósi–Penrose floor; a coherent diamond implies CQ acceleration noise ≥ 1.3×10⁻¹² m s⁻²/√Hz | Worked example within existing literature, not new | [OPPENHEIM.md](OPPENHEIM.md) |
| Smeared Markovian classical gravity | At R₀ = a it heats matter at 0.5 W/kg, 6×10¹⁰ × the Earth's heat flow | Conditional: **only under R₀ = a and Markovian dynamics** | [COLLECTIVE.md](COLLECTIVE.md) |
| Trapped-ion visibility | −ln V = 2 Var(ΔN); contrast 0.787 → 0.111 from n̄ = 0.1 to 5 | Worked example; novelty unchecked | [PREDICTIONS.md](PREDICTIONS.md) |

The experimental consequences, with requirements and sources, are in
[PREDICTIONS.md](PREDICTIONS.md). A positive two-diamond result (gravity follows each
branch, λ = 1) is also what perturbative quantum gravity predicts, so it would rule out
classical gravity, not single out anything here.

### One equation for the bookkeeping

The research notes ([DERIVATION.md](DERIVATION.md), [technical.html](technical.html))
collect these pieces in one place:

```
ρᵢⱼ(t) = ρᵢⱼ(0) · ⟨Eⱼ|Eᵢ⟩ · e^{i(Sᵢ − Sⱼ)/ħ}
Sᵢ = S_matter[i] + S_EM[i] + (c⁴/16πG) ∫ eᵢ T[eᵢ] d⁴x        gravity's TEGR action
```

This is standard decoherence with branch-dependent phases; it is not a new theory. Its
use is practical: every decoherence channel, gravity's own field included, enters as one
factor of the record overlap ⟨Eⱼ|Eᵢ⟩, so the channels are tallied and compared on the
same footing in one calculation.

## Reproduce

```bash
pip install -r requirements.txt pytest
python3 src/stur_tegr_gr.py         # GR's classic tests from TEGR, ~10 s
python3 src/stur_tegr_corner.py     # TEGR vs GR Noether charges and the first law, ~60 s
python3 src/stur_tegr_frame.py      # the frame at a corner: boost conjugate to area/8piG; Lorentz closure, ~15 s
python3 src/stur_tegr_logs.py       # frame edge logs vs Sen's universal log correction, ~1 s
python3 src/stur_tegr3d.py          # 3D: Ponzano-Regge 6j asymptotics and the 2-3 move, ~3 s
python3 src/stur_derivation.py      # the whole chain, ~30 s
python3 src/stur_gravity_full.py    # the two-diamond design search, ~15 s
python3 src/m331_exact.py           # the 3-3-1 selection, both variants
python3 src/m331_three_loop.py       # three-loop gauge running and the criterion, ~70 s
python3 src/m331_margin.py           # the beta = +1/sqrt3 margin against mass floors, ~50 s
python3 src/ladder_standalone.py     # the whole ladder, one file, no dependencies, ~1 s
python3 src/m331_breaking.py         # the ladder, rungs 1-5: also chiral_breaking, casimir_diamonds,
                                    # graviton_exchange, macdowell_mansouri (each a few seconds)
python3 src/m331_standalone.py      # the whole 3-3-1 chain, one file, no dependencies, ~15 s
python -m pytest tests -q           # every number pinned (143 tests)
```

Each script writes its reference output to `results/`, and CI checks every number on
each push.

## Layout

```
paper/                    the 3-3-1 note: PDF and LaTeX source
notebooks/                study notebooks with exercises
NOTE_331.md               the 3-3-1 note with extended detail on each check
NOVELTY.md                literature search: what is new, what was already known
NOTE_TEGR.md              the frame in teleparallel gravity and black-hole entropy
SYMMETRY_LADDER.md        symmetry breaking from 3-3-1 to the diamond experiment, derived
QUANTUM_TEGR.md           literature map for quantum teleparallel gravity
TEGR.md, MEASUREMENT.md, BORN.md, DERIVATION.md, GRAVITY_ENTANGLEMENT.md,
OPPENHEIM.md, COLLECTIVE.md, EMERGENT.md, PREDICTIONS.md
                          the worked examples, one report each
src/                      one script per report; outputs in results/
tests/                    regression tests
index.html, technical.html  the website (GitHub Pages)
```

Script names keep the `stur_` prefix of the project's former working title.
Earlier exploratory material, superseded by the work above, is preserved in git
history at commit [`d6baab6`](https://github.com/sheldonlindberg-afk/STUR-Physics-Lab/tree/d6baab6).

## License

CC0 1.0. See [LICENSE](LICENSE).
