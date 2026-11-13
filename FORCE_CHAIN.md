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
