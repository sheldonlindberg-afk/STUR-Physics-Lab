# Gravity as a consequence of the quantum level

Reproduce: `python3 src/stur_emergent.py` (about 12 s). The full output is in
`results/emergent/output.txt`, and `tests/test_emergent.py` pins the numbers.
Labels: KNOWN, FOLLOWS, CHECK, LIT, ANALOG (a lattice model of the mechanism, not
gravity itself).

## The question, turned around

The earlier reports asked whether gravity, acting on a quantum particle, behaves
quantum-mechanically. That puts gravity outside, acting on the quantum world. The
other way round: **everything, gravity included, is a consequence of what happens at
the quantum level.** Then the question isn't "is gravity quantum?" but "*what kind*
of consequence is gravity?" Each answer makes a definite prediction for the
diamond experiment.

## K1. Newton's G from the quantum vacuum (KNOWN; coefficient computed earlier)

- The vacuum's entanglement entropy across any surface obeys an area law:
  S = 0.3046 (R/a)² per quantum field (`stur_unification.py` U3, Srednicki's method).
- Jacobson (1995) showed that δS = δ⟨K⟩ on every local horizon *is* Einstein's
  equation, with 1/(4Għ) equal to the entanglement per unit area. [TEGR.md](TEGR.md)
  is the field theory that results.

Matching the two fixes the cutoff a, the spacing at which the quantum level's
entanglement stops being counted:

| Number of quantum fields | Cutoff that gives the observed G |
|---|---|
| 1 | 0.31 ℓ_P |
| 10 | 0.98 ℓ_P |
| 100 | 3.1 ℓ_P |
| 1000 | 9.8 ℓ_P |

On this reading the Planck length is where the counting stops, "where the numbers
break down", and not where reality breaks down.

## Two ways a field can be a consequence of a quantum medium

**K2. Collective, like phonons (ANALOG, exact).** The medium is a 3D lattice of
coupled quantum oscillators, standing in for "the quantum level".

- **A 1/r force emerges.** The lattice's static response to a point source follows
  Newton's (and Coulomb's) 1/r law away from the lattice scale. Relative to r = 12 on
  an 81³ lattice, lattice/continuum = 1.09, 1.05, 1.03, 1.014, 1.009 at r = 2, 3, 4, 6, 8.
- **Two probes, each in two places, coupled only to the medium.** I computed the exact
  dynamics of all 2,744 modes of a 14³ lattice:

| Switching | Entangling phase | Static 1/r prediction | Entanglement (negativity) | Which-path record left in the medium |
|---|---|---|---|---|
| Slow | 0.606 rad | 0.605 rad | **0.149** | 2×10⁻⁶ |
| Sudden | 0.498 rad | 0.484 rad | **0** | 0.31 |
| Slow, medium replaced by its average | 0 | — | **0** | 0 |

- A field that emerges from a quantum medium follows **each branch** of its sources.
  The probes entangle through it, with the phase of the emergent 1/r law to 0.3%.
  That is λ = 1.
- When the probes are moved slowly, the medium returns to its vacuum and keeps no
  record. When they are moved suddenly, leftover phonons record which path was taken,
  and that destroys the entanglement. For gravity the corresponding record is 10⁻⁵⁹
  gravitons ([TEGR.md](TEGR.md) E6), so gravity is deep in the slow regime.
- This isn't hypothetical: trapped-ion quantum gates entangle ions through their own
  collective motion, a field that emerges from the ions themselves (LIT:
  Mølmer–Sørensen 1999).

**K3. Statistical, like temperature.** Here the field follows the *average* of the
quantum level, which is λ = 0. An average is only well defined if something produces
it: intrinsic noise or collapse. The parameter-free version is Diósi–Penrose
gravity-induced collapse:

| Diamond (1.5×10⁻¹⁴ kg, R = 1.007 µm) | DP collapse rate | Superposition lifetime |
|---|---|---|
| split 250 µm | 169 /s | 5.9 ms |
| split 721 µm (design A) | 170 /s | 5.9 ms |

The lifetime is uncertain by a factor of 2, depending on the convention used.
Lumpiness of the crystal (nuclei smeared over R₀ ≥ 0.54 Å) adds only 4×10⁻⁶ /s. Design
A needs 3.2 s of coherence, so under DP the superposition is gone about 550× sooner.
The simplest DP (R₀ < 0.54 Å) is already excluded by the absence of the radiation it
predicts (LIT: Donadi et al. 2021). Versions with larger R₀ survive, and this
experiment tests them.

## K4. What the experiment measures, read the right way round

| Gravity is … | Do two diamonds entangle? | Does one diamond keep its 3 s superposition? |
|---|---|---|
| collective (phonon-like) | **yes** (λ = 1) | **yes** |
| statistical (average + noise) | **no** (λ = 0) | **no**: DP-type collapse in ~6 ms |

The right-hand column needs only **one** diamond. A single-diamond interferometer at
design A's mass and split already tells the two apart, before any entanglement run.
The two-diamond witness then confirms the collective reading.

## What this means for the picture

If all things, gravity included, are consequences of the quantum level, gravity
doesn't need to be "quantized" as a separate step. A field that emerges from quantum
constituents is automatically in two places when they are (K2). That is the λ = 1
prediction, reached from the quantum side rather than imposed on gravity from
outside. The one way out is for gravity to be a statistical average. That requires
intrinsic collapse, which has its own, faster signature (K3).

**Limits of K2:** it is an analog. It shows that the mechanism (an emergent 1/r field
following each branch) is generic and exact for a quantum medium. It doesn't show
that gravity's medium is of this kind. That is what the experiment decides.
