# The forces in one chain

[`src/force_chain.py`](src/force_chain.py) follows the forces in order, from the 3-3-1
gauge theory down to the diamond experiment's gravity and on into black holes, which then
evaporate back up through every force. Each stage is a function that takes values earlier
stages returned and returns new ones. A ledger records every hand-off, and
[`tests/test_force_chain.py`](tests/test_force_chain.py) checks that each stage after the
first uses an earlier stage's output and that nothing is retyped in between. Output:
[`results/force_chain.txt`](results/force_chain.txt); about 3 s.

```bash
python3 src/force_chain.py
```

## The stages

| Stage | What happens | Uses | Gives | Measured input entering here |
|---|---|---|---|---|
| 1 Unification | SU(3)_C × SU(3)_L × U(1)_X breaks to the Standard Model and then to electromagnetism. Anomalies fix the quark charges (2/3, −1/3 at N_c = 3) and make matter exactly neutral; the Landau poles select N_c = 3 against the Planck mass (2.86 M_Pl vs 4×10⁻⁸ M_Pl for N_c = 5) | — | charges, q_p + q_e = 0, M_Pl, G, G_F, α̂(M_Z), M_V | G; 1/α̂(M_Z), G_F; the Z′ floor |
| 2 Electroweak to the photon | The same coupling run to zero momentum: leptons computed, hadrons measured, scheme converted. 1/α(0) = **137.035999** | α̂(M_Z) | α(0) | Δα_had |
| 3 Weak to strong | G_F and the pion's weak decay give **f_π = 130.57 MeV** | G_F | f_π | Γ(π → μν), δ_π, \|V_ud\| |
| 4 The strong force | Chiral symmetry breaking: π⁰ → γγ = **7.742 eV** (PrimEx 7.802 ± 0.117), the O(p⁴) pion mass 132.3 MeV, the electromagnetic π⁺–π⁰ splitting, the nuclear force's 1.41 fm range, and the nucleon's mass: **91% QCD field energy** | charges, N_c, α(0), f_π | mass budget | lattice constants, σ-terms; m_ρ, m_a₁ |
| 5 Electromagnetism in the lab | Exact neutrality, and with α(0) the experiment's requirement, < 2.82×10⁻¹⁹ e per nucleon; the Casimir–Polder gap, 181.2 µm | q_p + q_e, α(0), G | gap | diamond's permittivity |
| 6 Gravity in the lab | One-graviton exchange: design A's entangling phase, **2.187 rad**; 1.99 rad without the u and d quarks' masses | G, gap, mass budget | phase, mass, cryostat temperature | the cryostat temperature (a design choice) |
| 7 Gravity as a broken gauge theory | SO(4,1) → SO(3,1) (MacDowell–Mansouri): l = 1.65×10²⁶ m, coupling 10¹²²; the Λ term cancels in the entangling phase; the field equations give Schwarzschild–de Sitter | G, phase | l, f(r) | Λ |
| 8 Black holes | Surface gravity from the gauge theory's spin connection; Sgr A*'s Hawking temperature from stage 7's f(r) (Λ changes it by 2×10⁻³²); the EHT shadows and GW250114's area law; then an evaporating hole's temperature passes the cryostat, the CMB, electrons, pions, the QCD crossover, the W and Z, the electroweak crossover, the 3-3-1 scale, and ends at stage 1's Planck mass | l, f(r), G, M_Pl, M_V, cryostat temperature, mass | — | EHT, stellar-orbit and LVK data (in `src/black_holes.py`) |

## What closes and what doesn't

The chain closes on itself: stage 1's Planck mass, set by the G the diamonds measure in
stage 6, is where stage 8's evaporating black hole ends. And the same particles that stage 1
breaks into are what stage 8's black hole emits, in reverse order.

Each place a measured number enters is marked. Not derived anywhere in the chain:

- the values of those inputs (the couplings, masses, Λ, diamond's permittivity);
- why the scales are so far apart;
- gravity's unification with the gauge forces. Stage 7 is an equivalent rewriting of general
  relativity with Λ, in the same broken-symmetry language as stage 1. It is not derived from
  stage 1, and the step from 6 to 7 is a change of language, not of physics.

Three steps carry a model, named where they occur: the ρ + a₁ saturation of the pion
splitting (27% above the measured value), the switch-on rule for each species in the
evaporating black hole, and the order-of-magnitude bound on Λ's mass–mass correction.

## Where the derivations are

The chain calls the repository's derivations instead of repeating them:
the 3-3-1 sector in `src/m331_*.py` ([NOTE_331.md](NOTE_331.md)); the strong force in
`src/chiral_breaking.py`; Casimir–Polder in `src/casimir_diamonds.py`; graviton exchange in
`src/graviton_exchange.py`; MacDowell–Mansouri in `src/macdowell_mansouri.py`; black holes in
`src/black_holes.py`; the hand-offs in `src/ladder_links.py`, whose results are tabulated
step by step in [SYMMETRY_LADDER.md](SYMMETRY_LADDER.md). Every literature value is
checked in [AUDIT.md](AUDIT.md).

## The same chain on first principles, in one file

[`src/chain_first_principles.py`](src/chain_first_principles.py) runs the chain again on a
different footing. Its formulas don't come from the modules above. They come from blind build
`2026-11-b` ([rebuild/PROTOCOL.md](rebuild/PROTOCOL.md)), written by AI sessions that saw only
the postulates, the function signatures and the measured inputs. The file embeds that
build's ten stages unchanged, needs only the Python standard library, and runs in about a
second, so it can be pasted into any Python runner. Output:
[`results/chain_first_principles.txt`](results/chain_first_principles.txt).

```bash
python3 src/chain_first_principles.py
```

Wherever the chain could take a number from outside and a stage derives it, the derived
number is used, and every result that has a measurement is then compared with it:

| Not put in | Derived value | From |
|---|---|---|
| Quark charges | 2/3, −1/3 | anomaly cancellation |
| Number of colours | 3 | the one-loop Landau poles against the Planck mass |
| f_π | 130.567 MeV | G_F and the pion's weak decay, in place of the lattice value |
| m_π | 132.3 ± 3.8 MeV | O(p⁴) chiral perturbation theory with that f_π (the formula is quoted) |
| Gap between the diamonds | 181.11 µm | the Casimir–Polder force |

| Derived, against its measurement | Pull |
|---|---|
| Pion mass at O(p⁴), against the neutral pion | −0.71σ |
| π⁰ → γγ width, 7.742 eV against 7.802 ± 0.117 | −0.51σ |
| The same width with the derived pion mass, 7.29 ± 0.62 eV | −0.81σ |
| Pion–nucleon coupling (Goldberger–Treiman), 12.97 against 13.1 ± 0.1 | −1.30σ |
| M87* and Sgr A* angular sizes against the EHT | −0.40σ, +0.16σ |
| GW250114's ringdown frequency and damping rate | +0.33σ, +0.59σ |

All eight are within 2σ (χ² = 3.76; they are not independent, since several share f_π), and
all 28 identity and hand-off checks pass. Three limits apply:

- **The measured inputs stay measured.** G, the couplings at M_Z, G_F, the pion's decay rate,
  the lattice constants and Λ are not derived by any stage. The 3-3-1 scale and the ratio of
  the two electroweak vacuum values are choices.
- **Tree-level M_Z is 0.35% above the measured value**, far outside the measurement's error.
  The chain has no loop corrections, so this comparison is printed but not counted in the fit.
- **Three parts of the chain above have no blind stage**: running α down to zero momentum
  (α(0) is an input here), the nucleon's mass budget with the pion's electromagnetic
  splitting, and the species-by-species evaporation sequence.

[`src/first_principles_standalone.py`](src/first_principles_standalone.py) is the ten stages
alone, without the chain: 74 functions, 66 derived in the build and 8 quoted, each printed
with how it was obtained
([`results/first_principles_standalone.txt`](results/first_principles_standalone.txt)).

Both files are generated by [`tools/build_chain_standalone.py`](tools/build_chain_standalone.py)
from `rebuild/inputs.py`, the build's modules and a driver
([`tools/chain_driver.py`](tools/chain_driver.py), [`tools/stages_driver.py`](tools/stages_driver.py));
[`tests/test_chain_first_principles.py`](tests/test_chain_first_principles.py) checks that they
are current, that the embedded stages give the build's numbers exactly, and that the chain's values
agree with `src/force_chain.py` where the two overlap.
