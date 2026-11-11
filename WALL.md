# Where the STUR program stands: we've hit the wall

Every route has now been pushed until it stopped. This page records what stands,
what failed, and why each remaining route is blocked. Each line points to the
code and report that support it.

## What stands (known physics, written as one equation)

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

## The open route: is gravity's field split, or in two places?

| Claim | Status | Where |
|---|---|---|
| A real EM charge "pulled into two places" | excluded: self-repulsion in flight, and a nearby surface erases the fringes | MEASUREMENT.md T5 |
| Gravity's field: amplitude (λ = 1) vs one averaged field (λ = 0) | **open; measurable.** λ = 0 predicts zero entanglement. Design A at the published targets needs 270 runs (derived gas rate); the binding gaps are mass in superposition (×4×10⁸) and vibration noise (×57 below LISA Pathfinder) | GRAVITY_ENTANGLEMENT.md |
| Gravity is TEGR (torsion gauge field on flat spacetime) | GR falls out: Schwarzschild as the unique static solution, perihelion 42.98″, light bending 1.7512″, γ = 1, GPS +38.54 µs/day; the experiment's phases are TEGR's to 6×10⁻¹⁶ rad. Names STUR's A_μ on the gravity side (4 of 5 requirements) | TEGR.md |
| Gravity as a consequence of the quantum level | G fixed by vacuum entanglement (cutoff 0.31 ℓ_P per field). Collective (phonon-like) emergence: field follows each branch, λ = 1 (lattice analog: 1/r law and entanglement exact). Statistical emergence would need at least Diósi–Penrose noise, which at the cutoff heats matter at 0.5 W/kg (6×10¹⁰ × the Earth's heat flow): so gravity is collective, **if** the smearing is the cutoff and the dynamics Markovian. One diamond kept for 3.24 s tests the rest; Oppenheim's classical gravity is squeezed by the same diamond (Γ·S_a bound). λ = 1 is also perturbative quantum gravity's prediction | EMERGENT.md, COLLECTIVE.md, OPPENHEIM.md |
| The equation from the quantum level up | ρᵢⱼ = ρᵢⱼ(0)⟨Eⱼ\|Eᵢ⟩e^{i(Sᵢ−Sⱼ)/ħ}, with gravity's TEGR action in Sᵢ and G from vacuum entanglement. Collective emergence of gravity (λ = 1) derived from D1–D3 (COLLECTIVE.md); predictions in PREDICTIONS.md | DERIVATION.md |

## The walls

1. **Data wall.** Option A survives only in a corner at ξ ≈ Earth's radius:
   Γ ≈ 2×10⁻³ for 3 m × 4 s arms. Closing it needs the published LIGO
   acceleration spectrum and geophysical bounds. `arxiv.org` is now reachable from the
   project's environment, but the corner still rests on an estimate. Even if it survived, its form
   (Γ ∝ Δx²) is generic gravity-gradient noise, not STUR.
2. **Compute wall.** The equal-weights test needs DMRG at large system size. It
   would only confirm Bisognano–Wichmann, which is already a theorem.
3. **The real wall: no free parameter.** The unified equation is fixed entirely by
   known quantum field theory. Every STUR-specific addition tried (A, B, C) either
   conflicts with existing experiments or has no observable. A new prediction
   needs a **new idea**: structure that produces a measurable deviation and is
   not already excluded. That can't come from reorganizing what's here.

## The 3-3-1 thread: where it stopped (fronts 7–7g)

Every assumption of the N_c = N_g = 3 selection that can be computed has been computed:
- the exact charges;
- two-loop gauge running;
- two-loop Yukawa terms;
- one-loop threshold matching (checked by matching-scale independence to 10⁻⁹);
- no-Yukawa bounds;
- the cutoff window (7.2×10¹⁵ – 1.4×10¹⁹ GeV);
- Witten's anomaly, now shown redundant;
- the scalar sector's own consistency to M_Pl.

The selection survives all of them. What is left is three walls:

1. **Conceptual.** The selection takes the measured TeV-scale couplings as input. For
   β = −1/√3, N_c = 5 survives in a narrow band of weak angle about three times below
   ours. No computation inside the framework removes this. It would need a principle
   fixing the couplings, and front 12 shows 3-3-1 has none (no gauge unification).
2. **Data.** The framework predicts a Z′ at 1.225 M_V, bilepton gauge bosons, and, if it
   is to stay consistent to M_Pl, exotic quarks below 1.4–1.8 M_V with the top's doublet
   carrying most of the vev. Colliders decide.
3. **Refinement only.** Two-loop quartic RGEs, one-loop Higgs matching and a full
   (non-random) map of the surviving scalar region would reshape the allowed corner. They
   can't restore N_c = 5, which fails in the gauge sector alone.

## The gravity thread: where it stopped

Computed:
- the decoherence floor for every continuous, Markovian classical gravity (the
  Tilloy–Diósi floor, which is also Oppenheim's trade-off once minimized);
- the shape-free one-particle bound (P3);
- the kernel-free bound Γ·S_a ≥ (F_LR/M)²/8, which covers every Markovian
  classical–quantum gravity, discrete jump models included (P5). It applies Oppenheim et
  al.'s own appendix-B trade-off, so it is not new as a principle;
- the finite-nucleus heating, which corrects the old 10⁶⁰ W/kg to 0.5 W/kg.

What is left:

1. **Theory wall: non-Markovian classical gravity.** No positivity theorem plays the
   role of the trade-off for classical fields with memory, so no bound of this kind can
   be derived for them. It would take a new theorem.
2. **Experiment wall.** Every decisive test needs a ~10⁻¹⁴ kg diamond held coherent
   across about its own radius (P5) or across 721 µm (P3, two diamonds). That is 4×10⁸
   times the largest mass yet put in superposition. Engineering decides; these notes
   don't.
3. **Distinctiveness wall.** A positive result confirms λ = 1, which perturbative
   quantum gravity also predicts. Distinguishing this framework from standard physics
   would need a new mechanism (an option D-type idea), not more computation.

## What would move it

- **For the corner:** allow `arxiv.org` in the environment's network settings,
  then close or confirm the Earth-scale corner of option A.
- **For a new prediction:** propose a new mechanism. I'll test it the same way:
  label it, compute it, confront it with the strongest bound, and give its
  MAGIS/AION signal.
- **To publish:** write STUR up as the synthesis above (option D).
