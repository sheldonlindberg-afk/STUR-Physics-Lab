# Where the STUR program stands: we've hit the wall

Every route has now been pushed until it stopped. This page records what stands,
what failed, and why each remaining route is blocked. Each line points to the
code and report that support it.

## What stands (known physics, unified in one equation)

**ln Zₙ = (1 − n) · A_H/4Għ − n · σ · A_swept + …**

This is the replica generating function with holonomy 2πn. The same first law,
δS = δ⟨K⟩ (equivalently D = Δ⟨K⟩ − ΔS ≥ 0), governs every sector below.

| Sector | Result | Evidence |
|---|---|---|
| Horizons | S = A/4G is linear in the holonomy | P4 (exact); OPEN_PROBLEMS.md |
| Decoherence and thermodynamics | ⟨Q⟩ = k_BT · D(record‖thermal); visibility = parity of exchanged quanta, V = ⟨(−1)^ΔN⟩ | ASSUMPTIONS.md; UNIFICATION.md U2, exact to 10⁻¹⁶ |
| Local horizon thermodynamics | dS = Σ dE(x)/T_loc(x), with a local Unruh-type temperature | UNIFICATION.md U1, lattice 0.9997 |
| Confinement | the string area enters the modular energy, not the entropy | CONFINEMENT.md (1+1D), Z2_GAUGE.md (2+1D) |
| Running horizon tension | 1/4G(μ) = 1/4G₀ + 0.0242 N μ² | UNIFICATION.md U3 |

**Status:** this is a synthesis. Every ingredient is published physics; the
combined statement and the lattice tests are this project's.

## What failed (STUR-specific claims, each computed)

| Claim | Failure | Where |
|---|---|---|
| S_R = −k_B ln V | matches no standard entropy; contradicts the area bound after the Page time | POSTULATE_TEST.md, ASSUMPTIONS.md, OPEN_PROBLEMS.md P7 |
| E_R = ½k_BTΦ² (Landauer) | Landauer applies to erasure, not dephasing; the T-scaling is the wrong sign | POSTULATE_TEST.md |
| Smarr check | circular: it reproduces an identity that was put in | user's correction; OPEN_PROBLEMS.md P4 |
| One A_μ and one σ(μ) | the two areas carry factors n vs (1 − n); energy density vs entropy density | OPEN_PROBLEMS.md P2–P3, CONFINEMENT.md |
| Quarks as folds | folds are baryons; a B = ⅓ fold costs 0.18 E_P | OPEN_PROBLEMS.md P5 |
| An empty universe triggers tunnelling | the barrier rises as density falls | OPEN_PROBLEMS.md P6 |
| **Option A:** spacetime records which-path information with an area law | excluded by 8–13 orders of magnitude (LISA Pathfinder, GW detectors) wherever the area law operates | OPTION_A.md |
| **Option B:** a confining field coupled to atoms | confinement must be longer than the Hubble radius (√σ < 1.4×10⁻³³ eV). What's left is an ordinary fifth force (MICROSCOPE): Γ ≈ 10⁻⁵⁸ | `src/stur_walls.py` |
| **Option C:** a scale-dependent horizon tension | ΔS = 4πcN is a constant (0.3 k_B per scalar); T_H unchanged; no observable | `src/stur_walls.py` |

## The walls

1. **Data wall.** Option A survives only in a corner at ξ ≈ Earth's radius:
   Γ ≈ 2×10⁻³ for 3 m × 4 s arms. Closing it needs the published LIGO
   acceleration spectrum and geophysical bounds. This session's network blocks
   `arxiv.org`, so the corner rests on an estimate. Even if it survived, its form
   (Γ ∝ Δx²) is generic gravity-gradient noise, not STUR.
2. **Compute wall.** The equal-weights test needs DMRG at large system size. It
   would only confirm Bisognano–Wichmann, which is already a theorem.
3. **The real wall: no free parameter.** The unified equation is fixed entirely by
   known quantum field theory. Every STUR-specific addition tried (A, B, C) either
   conflicts with existing experiments or has no observable. A new prediction
   needs a **new idea**: structure that produces a measurable deviation and is
   not already excluded. That can't come from reorganizing what's here.

## What would move it

- **For the corner:** allow `arxiv.org` in the environment's network settings,
  then close or confirm the Earth-scale corner of option A.
- **For a new prediction:** propose a new mechanism. I'll test it the same way:
  label it, compute it, confront it with the strongest bound, and give its
  MAGIS/AION signal.
- **To publish:** write STUR up as the synthesis above (option D).
