# The forces in one chain

[`src/force_chain.py`](src/force_chain.py) follows the forces in order, from the 3-3-1
gauge theory down to the diamond experiment's gravity and on into black holes, which then
evaporate back up through every force. Each stage is a function that takes values earlier
stages returned and returns new ones. A ledger records every hand-off, and
[`tests/test_force_chain.py`](tests/test_force_chain.py) checks that each stage after the
first uses an earlier stage's output and that nothing is retyped in between. Output:
[`results/force_chain.txt`](results/force_chain.txt); about 7 s.

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

## Branches: where the chain meets a measurement it did not use

Seven branches leave the chain ([`src/chain_branches.py`](src/chain_branches.py); output
[`results/branches/output.txt`](results/branches/output.txt)). Each takes values the chain
already carries, adds the inputs named, and ends at a number that has been measured. They
are numbered by the stage they follow, and the ledger records their hand-offs like any other.

| Branch | Takes from the chain | Result | Measured | Inputs entering here |
|---|---|---|---|---|
| 2a The W mass | G_F (stage 1), α(0) (stage 2) | Tree level 80.94 GeV; with stage 2's running of α 79.96; with the top quark's loop **80.47 GeV** | 80.369 ± 0.013 GeV | M_Z, m_t |
| 2b The electron's magnetic moment | α(0) (stage 2) | The measured moment, inverted through the five-loop QED series: **1/α = 137.035999166** | published 137.035999166(15); stage 2 has 137.035999 | the series' coefficients, a_e |
| 2c The weak mixing angle at zero momentum | the running of α by sector (stage 2) | Leptons pull it toward ¼, quarks toward 21/44: 0.23129 at M_Z → **0.23873** | 0.2382 ± 0.0011 at 157 MeV (Qweak); full calculation 0.23873 ± 0.00005 | sin²θ_W(M_Z) |
| 3a The neutron lifetime | G_F (stage 1), \|V_ud\| (stage 3) | Phase space computed from m_n − m_p; tree level 913 s; with the quoted radiative corrections **880.6 ± 1.6 s** | 878.4 ± 0.5 s | g_A, m_n − m_p, the radiative corrections |
| 4a Primordial helium | M_Pl (stage 1), α(0) (stage 2), the lifetime (3a) | 16.0% neutrons at weak freeze-out, 12.0% left when deuterium burns at 71 keV: **Y_p = 0.241** | 0.245 ± 0.003 | baryon density, deuteron binding, two nuclear cross sections |
| 4b The neutron–proton mass difference | G_F, \|V_ud\|, M_Pl, α(0), the lifetime (3a), Y_p (4a) | Not derived: lattice QCD + QED gives 2.52 − 1.00 = 1.51 ± 0.28 MeV. Computed: **dY_p/dδ = −0.61 per MeV**; at the lattice's central value the lifetime would be 332 s and Y_p 0.117 | 1.2933 MeV | the lattice result |
| 7a When matter collapses | M_Pl and G (stage 1) | M_Pl³/m_n² = 1.85 M☉. Electrons hold up 3.098/μ_e² of it (**1.456 M☉** for carbon); free neutrons in general relativity 0.384 of it (**0.710 M☉**) | heaviest neutron star 2.08 ± 0.07 M☉ | the Sun's GM, nucleon masses |

What each one connects:

- **2a** closes most of a gap the chain already admitted: its tree-level electroweak masses
  miss by far more than the measurement's error. Stage 2's running of α alone overshoots
  (−0.5%); the top quark's loop brings it back to +0.13%. The remaining bosonic and
  two-loop terms are not computed, so the comparison is printed, not claimed. With the
  complete correction quoted from the PDG (Δr = 0.03685) the same relation gives 80.355 GeV.
- **2b** shows where the chain's α comes from. It is a return trip, not a test: the
  α̂(M_Z) that stage 1 takes as input was itself obtained from α(0), and α(0) is measured
  best by the electron's magnetic moment. The branch inverts that measurement through the
  QED series and recovers the published value to all its digits. Coming down from M_Z,
  stage 2 can only fix 1/α to ± 0.009, because of the hadronic input; the electron's moment
  is 600,000 times more precise.
- **2c** uses stage 2's loops a second time. The fermion loops that make α run also mix
  the photon with the Z, so the weak mixing angle runs: each sector pulls it toward
  λ = Σ N_c Q T₃ / (2 Σ N_c Q²), which is ¼ for leptons, 21/44 for five quarks and ⅜ for
  all fermions together, the unified value. The one-loop result lands on the full
  calculation and within 0.5σ of the measurement, which sees the 3.2% rise at 6σ. The
  model: one loop, the hadronic mixing weighted by quark charges, the W loop left out.
- **3a** is the weak force acting on the strong force's bound state. The only strong-force
  input is g_A; the error is dominated by it, and the result sits 1.3σ above the measurement.
- **4a** needs all four forces. Gravity (stage 1's Planck mass) sets how fast the universe
  expands; the weak force (3a's lifetime) sets when neutrons stop converting and how fast
  they decay; the strong force (the deuteron's binding) sets when deuterium survives; and
  electromagnetism (stage 2's α) sets the barrier it must cross to burn. With G 10% larger
  the helium fraction would be 0.249.
- **4b** is the one input 3a and 4a both lean on hardest. The chain does not derive it:
  lattice QCD + QED finds that the down quark's extra mass makes the neutron 2.5 MeV
  heavier and electromagnetism makes the proton 1.0 MeV heavier, leaving 1.5 ± 0.3 MeV.
  What the branch computes is the leverage. A 1% change in the difference changes the
  lifetime by 6.7% and the helium fraction by 0.008, so the measured helium fixes it to
  ± 5 keV where the lattice reaches ± 280 keV. With electromagnetism alone the proton
  would be the heavier particle and hydrogen would not be stable.
- **7a** joins the two ends of the chain. The same G that stage 6's diamonds measure, and
  the nucleon mass that stage 4 traces to QCD field energy, fix the mass at which matter can
  no longer hold itself up: two pure numbers, both integrated here, times M_Pl³/m_N². The
  heaviest neutron star measured is 2.9 times the free-neutron limit, so stage 4's nuclear
  force, not Pauli pressure, carries it. Stage 8's black holes are 45 times above the limit.

Three of these carry a model, named where it enters. Branch 2a keeps only the two leading
pieces of the electroweak correction, and branch 2c only the one-loop fermion terms. Branch
4a uses a minimal reaction network: n + p ↔ D + γ
and D + D, with every fusion taken to end in helium-4. It leaves twice the measured
deuterium, because it has no D + p → ³He, and its helium moves by less than 0.002 when
either nuclear cross section is doubled or halved. Full nucleosynthesis codes give 0.247.

The branches are not part of the first-principles file below: that file is assembled from
the blind rebuild, which has no stages for them.

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
  [GRAVIGUT_NOGO.md](GRAVIGUT_NOGO.md) shows why it cannot be: no breaking of stage 1 leaves
  gravity's non-compact group, and no orthogonal graviGUT parent holds stage 1's chiral fermions.

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
| Gravity's scale | M_Pl 0.47–3.1 × measured | the one-loop induced G of stage 1's own fields, cut off at its U(1)_X pole ([INDUCED_GRAVITY.md](INDUCED_GRAVITY.md); blind campaign `induced_g`) |

| Derived, against its measurement | Pull |
|---|---|
| Pion mass at O(p⁴), against the neutral pion | −0.71σ |
| π⁰ → γγ width, 7.742 eV against 7.802 ± 0.117 | −0.51σ |
| The same width with the derived pion mass, 7.29 ± 0.62 eV | −0.81σ |
| Pion–nucleon coupling (Goldberger–Treiman), 12.97 against 13.1 ± 0.1 | −1.30σ |
| M87* and Sgr A* angular sizes against the EHT | −0.40σ, +0.16σ |
| GW250114's ringdown frequency and damping rate | +0.33σ, +0.59σ |

All eight are within 2σ (χ² = 3.76; they are not independent, since several share f_π), and
all 40 identity and hand-off checks pass. The three `[model]` checks pass too: the measured G
lies in the band stage 1 induces, and neither the other variant nor N_c = 5 can induce it.
Three limits apply:

- **The measured inputs stay measured.** G's digits (its scale is now a check, not an input;
  downstream steps need its digits), the couplings at M_Z, G_F, the pion's decay rate,
  the lattice constants and Λ are not derived by any stage. The 3-3-1 scale and the ratio of
  the two electroweak vacuum values are choices.
- **Tree-level M_Z is 0.35% above the measured value**, far outside the measurement's error.
  The chain has no loop corrections, so this comparison is printed but not counted in the fit.
- **Three parts of the chain above have no blind stage**: running α down to zero momentum
  (α(0) is an input here), the nucleon's mass budget with the pion's electromagnetic
  splitting, and the species-by-species evaporation sequence.

**Step 9: why these inputs?** The merged simulation ends with a ninth step that is different
in kind. It is not from the blind build. It asks why the measured inputs have their values:
the Standard Model's 19 parameters, the published attempts to explain them, and quark flavour
in 3-3-1, restated with the standard library from [`src/why_parameters.py`](src/why_parameters.py).
Its comparisons are tagged `[conj]` (rests on a named conjecture) or `[emp]` (an empirical
regularity) and stay outside the fit and the verdict; ten of the 40 checks are its identities.
The explanation, results and sources are in [WHY.md](WHY.md).

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
