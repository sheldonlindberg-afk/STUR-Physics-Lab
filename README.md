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
extended notes: [NOTE_331.md](NOTE_331.md); the note's own page: [paper/README.md](paper/README.md))

In SU(3)_C × SU(3)_L × U(1)_X models, keep the number of colours N_c general, take no
generation or neutrino number from experiment, and require every gauge coupling to stay
perturbative to the Planck scale.

Exact (algebra, no measured input):
- Anomaly cancellation fixes the quark charges for every N_c, and the SU(3)_L anomaly makes
  N_g a multiple of N_c (N_c odd) or 2N_c (N_c even).
- Baryons are fermions with integer charge if and only if N_c is odd.

Numerical (running from the measured couplings):
- SU(3)_L running excludes N_c ≥ 7, and U(1)_X running excludes N_c = 5.
- Every N_g > N_c is excluded too, except N_c = 2 with N_g = 4 for β = −1/√3. A colourless
  N_c = 1 also passes.
- In coupling space the regions are nested: wherever any odd N_c ≥ 3 survives, N_c = 3
  does. No choice of couplings selects 5 or 7 instead
  ([`src/m331_coupling_map.py`](src/m331_coupling_map.py)).

So one input about colour is needed. As an observation: a colour force exists and baryons
are fermions of integer charge (N_c odd, at least 3). Asymptotic freedom of colour then
follows. As an axiom instead: colour is non-abelian and asymptotically free. Either way,
only **N_c = N_g = 3** survives, with quark charges ⅔ and −⅓. The selection holds:
- at two loops, including two-loop Yukawa terms, and at three loops in the gauge and
  matter sector;
- with one-loop threshold matching across the heavy spectrum;
- for 3-3-1 scales of 2–30 TeV;
- in both variants β = ±1/√3 (for β = +1/√3, only if its heavy charged leptons are above
  about 0.65 TeV; see below).

Every β-function coefficient is derived twice here, from tabulated group invariants and from
explicit generator matrices ([`src/m331_matrix_check.py`](src/m331_matrix_check.py)), and
agrees exactly, to three loops, with the external package PyR@TE 3
([`tools/pyrate_crosscheck.py`](tools/pyrate_crosscheck.py)).

Requiring the scalar sector to stay perturbative to M_Pl then bounds the exotic quarks
below 1.4–1.8 M_V.
A recast of the ATLAS 13 TeV, 139 fb⁻¹ dilepton search puts the Z′ above 4.6–5.2 TeV for
β = +1/√3 and 4.0–5.0 TeV for β = −1/√3, depending on its decays
([`src/m331_zprime_recast.py`](src/m331_zprime_recast.py); validated against ATLAS's own
Z′_ψ and Z′_χ limits, using the official HEPData tables, and reproduced independently with
Pythia 8).

**Conditions:**
- the 3-3-1 framework;
- the framework's scope: β = ±1/√3 with leptons in triplets. The flipped 3-3-1 model, with a
  lepton sextet, has a different anomaly relation and is not covered
  ([NOTE_331.md §1](NOTE_331.md));
- one input about colour, as above: baryons like ours (N_c odd, at least 3), or a
  non-abelian, asymptotically free colour group ([NOTE_331.md §2](NOTE_331.md));
- Planck-scale perturbativity;
- the measured TeV-scale electroweak couplings, which are an input, not a prediction.
  In the β = +1/√3 variant there is no comfortable margin. At α = 1 (three loops), N_c = 3
  reaches M_Pl only if the heavy charged leptons are heavier than 0.65 ± 0.13 TeV with M_V
  at its LHC bound (1.09 TeV at M_V = 10 TeV; Yukawa couplings run with the gauge couplings).
  A stricter criterion asks for more: about 3 TeV at α = 0.5. Lighter ones are not yet excluded by the
  LHC, and they push N_c = 3 below M_Pl too
  ([`src/m331_margin.py`](src/m331_margin.py); [NOTE_331.md §3e](NOTE_331.md)).
  The condition is on the three leptons' geometric-mean mass. Run 2 allows it down to
  0.24 TeV, so the LHC has not tested it. The HL-LHC reaches it only about at the threshold
  ([`src/m331_heavy_lepton.py`](src/m331_heavy_lepton.py), cross-checked against Pythia 8
  and reproducing ATLAS's own singlet limits; [NOTE_331.md §3f](NOTE_331.md)).

**Run it in one paste.** [`src/m331_standalone.py`](src/m331_standalone.py) reproduces the
whole selection in a single file that uses only the Python standard library: charges and
anomalies for general N_c, N_g = N_c, the selection without asymptotic freedom, the Standard Model calibration, SU(3)_L and two-loop
U(1)_X running with Yukawas, one-loop thresholds across the heavy spectrum, the
β = +1/√3 heavy-lepton condition against mass floors, and the R-ratio cross-check. Copy it (the [website](https://sheldonlindberg-afk.github.io/STUR-Physics-Lab/#run331)
has a one-click **Copy Python script** button; on GitHub use *Copy raw file*) and paste it
into any Python 3.8+ runner, notebook or AI assistant's code tool. It runs in about 15 s
and ends with 28 PASS/FAIL checks against the numbers pinned here
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

## The forces in one chain

**[FORCE_CHAIN.md](FORCE_CHAIN.md)** runs the forces as one simulation (`src/force_chain.py`,
about 7 s): unification, the photon, weak to strong, the strong force, electromagnetism and
gravity in the lab, gravity as a broken gauge theory, and black holes, which evaporate back
through every force to the Planck mass the chain started from. Each stage uses earlier
stages' outputs, and each measured input is marked where it enters.

Seven branches leave the chain where its values meet a measurement it did not use
(`src/chain_branches.py`): the W mass from the running of α and the top quark (80.47 GeV
against 80.37); the electron's magnetic moment, inverted to the α the chain starts from; the
weak mixing angle at zero momentum (0.23873 against 0.2382 ± 0.0011); the neutron lifetime
(880.6 ± 1.6 s against 878.4 ± 0.5); primordial helium, which needs all four forces (0.241
against 0.245 ± 0.003); how sharply that helium pins the neutron–proton mass difference; and
the masses at which cold matter collapses, two pure numbers times M_Pl³/m_N² (1.456 and
0.710 M☉).

`src/chain_first_principles.py` is the same chain as one copy-paste file (standard library only,
about 1 s), built on the blind first-principles rebuild: derived values replace outside numbers
wherever a stage derives them, and all eight comparisons with measurements are within 2σ.
Its ninth step asks why the measured inputs have their values: **[WHY.md](WHY.md)** sorts the
Standard Model's 19 parameters by what is known (11 unexplained, 3 related by established
physics, 2 empirical regularities, 3 conjectured), tests each published explanation against
data, and works out what the 3-3-1 structure does and does not give for quark flavour. None of
the 19 is derived.
`src/first_principles_standalone.py` is that rebuild's ten stages alone.

## For students: the symmetry-breaking ladder

**[SYMMETRY_LADDER.md](SYMMETRY_LADDER.md)** follows the forces down in energy, from the 3-3-1
scale to the two diamonds, with every step derived and checked in code:
- 3-3-1 → Standard Model → electromagnetism: the photon, the hypercharge matching and the
  W, Z, Z′ masses, from the gauge-boson mass matrix;
- chiral symmetry breaking: pions, the GMOR relation and the nuclear force, and the pion
  mass at O(p⁴) in chiral perturbation theory (132.6 ± 3.8 MeV against 135.0);
- the Casimir–Polder force between the diamonds, from electrostatics and the dipole field,
  at finite temperature (negligible at the design's 0.15 K), and the electric dipoles that
  exceed the design's bound by orders of magnitude (measured on silica, modelled for patches);
- one-graviton exchange: Newton's law and the experiment's 2.19 rad phase;
- gravity as a broken de Sitter gauge theory (MacDowell–Mansouri), a reformulation of GR;
- black holes, gravity's strong-field end rather than a symmetry breaking: the Hawking
  temperature fixed by the smoothness of Euclidean time, the first law in exact fractions,
  the largest black hole the measured Λ allows, and the EHT shadows of M87* and Sgr A* and
  GW250114's area increase against the data (Hawking radiation itself is unmeasured);
- twenty-six links across the rungs (see SYMMETRY_LADDER.md). **Neutral matter:** q_p + q_e is exactly the 3-3-1 (or
  Standard Model) mixed anomaly, and the diamond experiment needs it below 2.8×10⁻¹⁹ e per
  nucleon; the measured limit, 10⁻²¹ e, is 280× tighter. **π⁰ → γγ:** rung 1's charges and the measured f_π
  give 7.79 eV, against PrimEx's 7.80 ± 0.12 eV, for any N_c. **The Planck mass:** the 3-3-1
  selection's cutoff is √(ħc/G) with the diamond experiment's G; the selection would survive
  G 8.2× weaker or 10¹⁴× stronger at the reference spectrum, and G 1.6× weaker at the
  worst point of the threshold scan. **Black holes:** the diamond's Schwarzschild radius is a
  millionth of the Planck length, and a Planck-mass black hole has k_BT = M_Pl c²/8π.

Gravity is not part of the gauge chain; the page says where each derivation stops.

**Run it in one paste.** [`src/ladder_standalone.py`](src/ladder_standalone.py) reproduces all
six rungs and twenty-one links in a single file that uses only the Python standard library. Copy it (the
[website](https://sheldonlindberg-afk.github.io/STUR-Physics-Lab/#runchain) has a one-click
**Copy Python script** button) and paste it into any Python 3.8+ runner, notebook or AI
assistant's code tool. It runs in a few seconds and ends with 102 PASS/FAIL checks
([expected output](results/ladder/standalone.txt)). Each check is tagged **math** (an identity
verified by computation), **data** (against a measurement, with the tolerance and its reason
printed) or **pinned** (a number this repository derives, guarding against changes), and the
script exits with status 1 if any check fails.

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
python3 src/short_range_gravity.py  # design A against a Yukawa term in Newton's law, ~4 s
python3 src/m331_exact.py           # the 3-3-1 selection, both variants
python3 src/m331_three_loop.py       # three-loop gauge running and the criterion, ~70 s
python3 src/m331_margin.py           # the beta = +1/sqrt3 margin against mass floors, ~2 min
python3 src/m331_matrix_check.py     # the beta-function coefficients again, from explicit matrices, ~2 s
python3 src/m331_coupling_map.py     # the selection as a map of coupling space, ~2.5 min
python3 src/m331_heavy_lepton.py     # its heavy leptons vs the LHC and HL-LHC, ~5 s
python3 src/m331_gravity_fixed_point.py  # gravity above M_Pl (asymptotic safety) and the 3-3-1 couplings, ~70 s
python3 src/force_chain.py           # the forces in one chain, with its seven branches, ~7 s
python3 src/chain_branches.py        # the branches alone, with their sensitivities, ~15 s
python3 src/ladder_standalone.py     # the whole ladder, one file, no dependencies, ~1 s
python3 src/m331_rho_bound.py        # rho from 3-3-1 Z-Z' mixing vs the global fit and the LHC, ~7 s
python3 src/m331_zpole.py            # the LEP/SLD Z-pole fit of the mixing, validated on E6 Z', ~30 s
python3 src/m331_breaking.py         # the ladder, rungs 1-6: also chiral_breaking, casimir_diamonds,
                                    # graviton_exchange, macdowell_mansouri, black_holes (each a few seconds)
python3 src/ladder_links.py          # links across the rungs: neutral matter, pi0 -> gamma gamma, M_Pl, ~2 s
python3 src/m331_standalone.py      # the whole 3-3-1 chain, one file, no dependencies, ~15 s
python3 src/why_parameters.py        # the 19 parameters: explanations tested, 3-3-1 flavour, ~3 s
python3 tools/dependency_map.py    # regenerate DEPENDENCIES.md after changing a script, ~1 s
python -m pytest tests -q           # every number pinned (354 tests)
```

Each script writes its reference output to `results/`, and CI checks every number on
each push.

## Layout

```
paper/                    the 3-3-1 note: PDF, LaTeX source, and its own README (start there)
notebooks/                study notebooks with exercises
NOTE_331.md               the 3-3-1 note with extended detail on each check
NOVELTY.md                literature search: what is new, what was already known
NOTE_TEGR.md              the frame in teleparallel gravity and black-hole entropy
FORCE_CHAIN.md            the forces as one chain, from 3-3-1 into black holes and back
WHY.md                    why these inputs? the 19 parameters, explanations tested, sources
SYMMETRY_LADDER.md        symmetry breaking from 3-3-1 to the diamond experiment, derived
FIRST_PRINCIPLES.md       how to rebuild the ladder from first principles
rebuild/                  protocol and harness for a blind AI rebuild of the ladder
DEPENDENCIES.md           generated map: which script feeds which, and every shared constant
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
