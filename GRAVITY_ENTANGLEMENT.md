# Gravity-induced entanglement: is gravity's field split, or in two places?

Reproduce: `python3 src/stur_gravity_entanglement.py` (under 1 s). The full output is
in `results/gravity_entanglement/output.txt`, and `tests/test_gravity_entanglement.py`
pins the numbers. Labels: KNOWN, FOLLOWS, LIT, PROPOSAL.

Gravity here is **TEGR's torsion field** ([TEGR.md](TEGR.md)). At these masses and
distances its phases are exactly the weak-field G m²/r used below. They are recomputed
from the TEGR field energy in `src/stur_tegr_gr.py` (agreement 6×10⁻¹⁶ rad; the next
order is 10⁻²⁴). Only TEGR and ordinary electromagnetism are used. Nothing exotic.

This continues [MEASUREMENT.md](MEASUREMENT.md) §T5. For the electron, the charge
and its field are in two places as an *amplitude*, not as e/2 + e/2. This report
asks the same question about gravity.

## The experiment (LIT: Bose et al. 2017; Marletto & Vedral 2017)

Two micro-diamonds (m = 10⁻¹⁴ kg, radius 0.88 µm) are each put into a superposition of
two places 250 µm apart. The nearest branches are 200 µm apart, and the two masses are
held for 2.5 s. Nothing acts between them except gravity. At the end, the experiment
checks whether the two masses are entangled.

## The equation

Each pair of branches (i of mass A, j of mass B) sits at distance r_ij and picks up
the ordinary Newtonian phase

```
φ_ij = G m² τ / (ħ r_ij)                                          (KNOWN)
```

The two pictures of gravity's field differ in one number, λ (PROPOSAL):

```
φ_ij(λ) = λ · φ_ij  +  (1 − λ) · φ_ij^mean-field
Δφ(λ)   = φ₀₀ + φ₁₁ − φ₀₁ − φ₁₀  =  λ · Δφ                          (FOLLOWS)
concurrence = |sin(λ Δφ / 2)|
```

- **λ = 1:** gravity's field is in two places as an amplitude, like the electron's
  field in T5. The four phases don't factor apart, so the masses become **entangled**.
- **λ = 0:** gravity's field is one classical average, the "split field". Each mass
  feels the other's averaged pull. All phases are local, the state stays a product,
  and there is **no entanglement at any mass, gap or time**. Tests check this to 10⁻¹².

So the experiment measures λ directly.

## Results

**Baseline phases (G1)**

| Geometry | Branch distances (µm) | Entangling phase Δφ | Concurrence |
|---|---|---|---|
| Linear (Bose et al.) | 450, 700, 200, 450 | −0.314 rad | 0.156 |
| Parallel (Chevalier et al. 2020) | 200, 320, 320, 200 | **+0.594 rad** | **0.293** |

The parallel arrangement gives nearly twice the entanglement for the same closest
approach.

**Split versus amplitude (G2, parallel).** The witness is designed for the λ = 1
prediction; ⟨W⟩ < 0 proves entanglement.

| λ | Δφ (rad) | Witness ⟨W⟩ | Runs needed (3σ) |
|---|---|---|---|
| 1.00 | 0.594 | −0.146 | 433 |
| 0.50 | 0.297 | −0.074 | 1,811 |
| 0.25 | 0.148 | −0.037 | 7,324 |
| 0 (split field) | 0 | 0 | never |

**Dephasing budget (G3).** Any process that records which branch a diamond is in
dephases it. The entanglement is gone entirely at γτ = 0.289, so the total dephasing
rate must be below **0.12 /s per diamond**.

- **Gas collisions, derived** (H5b). For a split much larger than the body and than the
  gas wavelength, every collision resolves the branches, so the rate is the collision
  rate, n⟨v⟩σ_tot. Here σ_tot = 2πR² is the exact quantum hard-sphere cross-section,
  checked by partial waves (2.0096 πR² at kR = 3000; kR ≈ 4000 for N₂ at 0.15 K).
- **The interpolation used before** (Romero-Isart 2011, eq. 27) gives 4.19× more. It
  extends the long-wavelength coefficient into this regime with a Gaussian.
- **At the published target** of 10⁻¹⁵ Pa (N₂) and 0.15 K, the collision rate is
  0.025 /s (γτ = 0.06), a fifth of the budget.
- At 10⁻¹³ Pa it is 20× too high. The vacuum is still a hard requirement, but no longer
  the one that decides the design.

**Electromagnetic background (G4).** The two neutral diamonds also attract through the
Casimir–Polder force, which falls off as 1/r⁷. At a 200 µm gap, its entangling phase is
6% of gravity's. Keeping it below 10% needs a gap above 181 µm. It is a known EM term,
calculated and subtracted.

**Self-gravity of one split mass (G5).** For the electron, the split picture failed
partly because the two halves repel each other (T5). A split diamond's halves would
attract, but over 2.5 s they move together by only 3×10⁻¹⁷ m. That is far too small to
see. For gravity, the self-interaction route is closed, and entanglement is the only test.

**How well λ can be measured (G6, parallel)**

| Dephasing γτ | 10⁴ runs | 10⁵ runs | 10⁶ runs | Floor (infinite runs) |
|---|---|---|---|---|
| 0 | λ > 0.21 | 0.068 | 0.021 | 0 |
| 0.05 | 0.40 | 0.24 | 0.19 | 0.17 |
| 0.10 | 0.59 | 0.42 | 0.36 | 0.34 |

Dephasing sets a hard floor. A weak entangling phase is erased completely, so below
the floor no number of runs helps. Δφ grows as m²τ: a 3× lighter diamond gives a
phase 11× smaller (0.053 rad at 3×10⁻¹⁵ kg).

## Verdict

- **Split field (λ = 0):** no gravitational entanglement, ever. This is a sharp,
  falsifiable prediction that uses no exotic physics.
- **Amplitude (λ = 1):** Δφ = 0.59 rad for the parallel baseline, which can be
  detected in about 433 runs.
- **Electromagnetism** already behaves as λ = 1 (T5; Sonnentag & Hasselbach 2007).
- **Gravity:** λ has not been measured.

λ is the one quantity here that an experiment under construction can measure and that
existing data leave open.
- **Within the theory,** λ = 1 is derived, CONDITIONALLY: it requires a statistical
  gravity smeared at the entanglement cutoff, and Markovian dynamics
  ([COLLECTIVE.md](COLLECTIVE.md)).
- **It isn't distinctive.** λ = 1 is also what perturbative quantum gravity predicts, so
  a positive witness rules out classical gravity without singling out this theory.
- **Intermediate λ is a phenomenological scale, not a dynamics.** The interpolation
  φ_ij(λ) doesn't define a consistent theory for 0 < λ < 1. It measures how much of the
  entangling phase is present. Results from either branch of this test go back into
[WALL.md](WALL.md).

Everything this section left out is modelled in the next one.

## The full model (`src/stur_gravity_full.py`)

Reproduce: `python3 src/stur_gravity_full.py` (about 15 s). Output in
`results/gravity_entanglement/full_output.txt`; `tests/test_gravity_full.py` pins it.
New ASSUMPTION inputs: 5 s overhead per run; at least 30 runs per measurement setting;
Im[(ε−1)/(ε+2)] = 0.01 for diamond (scanned over 10⁻³–10⁻¹); field gradient 10⁶ T/m (LIT, Bose et al.).

**H0. The Casimir-safe gap is the same for every mass: 181 µm.** Casimir goes as
R⁶/r⁷, and gravity as m²/r ∝ R⁶/r, so their ratio doesn't depend on the mass. Lighter
diamonds can't be moved closer to make up for their weaker pull.

**H1. Split and recombine.** Integrating the phase along real opening and closing
paths *adds* entangling phase, because the branches are already partly open during
the ramps: +18% for 0.5 s ramps. But it also adds time for every noise source to act.

**H2. Heat radiation.** At 0.15 K the thermal wavelength is 15 mm, much larger than the
superposition. Scattering of thermal photons is negligible (10⁻¹⁵ /s). What matters is
the diamond's own thermal emission. With a third of the budget given to it, the
diamond's **internal temperature must stay below about 1 K** (0.7–1.5 K over the Im K
scan). The diamond can't be held by absorbed laser light for the whole sequence.

**H3. Vibration (acceleration) noise.** A diamond in two places is an extremely
sensitive accelerometer: 6×10¹⁶ rad per m/s².

| Noise type | Phase that cuts entanglement to 10% | Acceleration noise allowed |
|---|---|---|
| Independent per diamond | 0.71 rad | 2.7×10⁻¹⁷ m s⁻²/√Hz |
| Common to both | 1.32 rad | 5.0×10⁻¹⁷ m s⁻²/√Hz |

LISA Pathfinder, the quietest free-falling test mass ever flown, reached 1.7×10⁻¹⁵
(LIT). The requirement is 35–65× below that. Shared noise is tolerated better
(it leaves the |01⟩–|10⟩ coherence intact), but it still has to be measured and
subtracted, or cancelled by the design.

**H4. The split itself.** A single electron spin (an NV centre) has to push the whole
diamond apart. With a 10⁶ T/m gradient, a 10⁻¹⁴ kg diamond opens only 116 µm in a
0.5 s ramp. Mass × separation is fixed by the ramp time, so heavier diamonds split
less, and the whole sequence must fit inside the spin's coherence time.

**H5. Full design search.** The search covers 25 masses × 25 separations × 25 hold
times × 17 ramp times, with every noise source on. The gap is set by Casimir, and the
split is limited by H4. Each design is scored by wall-clock time to a 3σ witness.

| Scenario | Best design | Result |
|---|---|---|
All with the derived gas rate (H5b). The previous, interpolated rate is shown for
comparison.

| Scenario | Best design | Result | With the old interpolated rate |
|---|---|---|---|
| A: 10⁻¹⁵ Pa N₂, 0.15 K, no vibration, unlimited spin coherence | 6.8×10⁻¹⁴ kg, Δx = 53 µm, ramps 2×0.89 s, hold 0.47 s, Δφ = 1.51 rad | **270 runs, 0.5 h** | 565 runs, 1.3 h |
| A′: as A, leftover gas is helium | 2.2×10⁻¹⁴ kg, Δx = 279 µm, Δφ = 1.85 rad | **270 runs, 0.6 h** | no design works |
| B: A + spin coherence 1.6 s | 1.5×10⁻¹⁴ kg, Δx = 137 µm, Δφ = 0.24 rad | 12,570 runs, 22.9 h | no design works |
| C: A + internal temperature 4 K | — | no design works | no design works |
| D: A + 10⁻¹⁴ Pa | — | no design works | no design works |
| E: A + LISA Pathfinder vibration | — | no design works | no design works |

**Design A** (1.5×10⁻¹⁴ kg, Δx = 721 µm, 3.24 s) is the reference geometry used across
the repository. With the derived gas rate its gas collisions use γτ = 0.105 (it was
0.44), and it reaches a 3σ witness in **270 runs (0.6 h)**. That is the protocol minimum
of 30 runs per setting, so gas no longer limits it. Almost all of its entangling phase
builds up during the ramps.

The fastest design (A, 53 µm) is heavier than design A, so it is 2×10⁹ times beyond
today's largest superposed mass, against 4×10⁸ for design A.

**Requirements, each varied alone**

| Requirement | Others at target (A) | Others ideal (10⁻¹⁷ Pa) |
|---|---|---|
| Internal temperature | < 1.89 K (was 1.19) | < 2.45 K |
| Spin coherence | > 1.38 s (was 2.1) | > 0.8 s |
| Vibration (acceleration noise) | < 3.1×10⁻¹⁷ m s⁻²/√Hz (was 1.3×10⁻¹⁷) | < 4.6×10⁻¹⁷ |
| Vacuum (others ideal) | N₂ < 7.6×10⁻¹⁵ Pa, He < 2.9×10⁻¹⁵ Pa (were 1.8×10⁻¹⁵, 6.9×10⁻¹⁶) | |

**H6. EM forces that can fake a positive result.** Noise can't create entanglement;
it can only hide it. But electromagnetic *interactions* between the diamonds can
create it:

- **Net charge:** one electron's worth of charge on each design-A diamond gives an
  entangling phase **1.6×10¹⁰× gravity's** (7×10⁸× for the fastest design). Both diamonds must carry exactly zero net charge.
  Levitated microspheres have been discharged to zero (LIT: Moore, Rider & Gratta 2014).
- **Permanent dipoles:** each must be < 4.5×10⁻²⁹ C·m (2.8×10⁻⁴ e·µm) to keep EM below
  10% of gravity. Otherwise a conducting shield goes between the diamonds (LIT: van de
  Kamp et al. 2020).
- **Controls:** run with the shield in place, with deliberately charged diamonds, and
  at several gaps. Gravity falls as 1/r and a dipole as 1/r³, so their dependence on
  the gap tells them apart.

## What comes out

| Requirement | Needed | State of the art (LIT) |
|---|---|---|
| Mass in a spatial superposition | 1.5×10⁻¹⁴ kg (design A) | 4×10⁻²³ kg (Fein et al. 2019): **4×10⁸× short** |
| Superposition size | 721 µm (design A) | |
| Vacuum | < 8×10⁻¹⁵ Pa (N₂), < 3×10⁻¹⁵ Pa (He) | reached only in cryogenic systems |
| Spin coherence | > 1.4 s | ~1 s (NV, cryogenic, with dynamical decoupling) |
| Internal temperature | < 1.9 K | micro-diamonds heat up under trapping light |
| Vibration (acceleration noise) | < 3.1×10⁻¹⁷ m s⁻²/√Hz | 1.7×10⁻¹⁵ (LISA Pathfinder): **~57× short** |
| Charge / dipoles | exactly 0 / < 4×10⁻²⁹ C·m, or a shield | zero charge demonstrated |

1. **Nothing in the physics forbids the test.** At the published targets, design A
   settles λ = 0 against λ = 1 in 270 runs (0.6 h), the protocol minimum. With the
   derived gas rate there is now room: helium as the leftover gas still allows a design
   (270 runs). A 10× worse vacuum still does not.
2. **λ = 0 (split field) predicts exactly zero gravitational entanglement.** A positive
   witness can't come from noise. It could come from EM, which is why H6's controls
   are part of the prediction.
3. **How finely λ can be pinned down** is set by dephasing. With 10⁶ runs, the fastest
   design reaches λ > 0.28 (it was 0.44). At 10⁻¹⁷ Pa it reaches λ > 0.017.
4. **What stands between the question and its answer is engineering, not theory.** The
   requirements must all be met at once, and the largest gaps are the mass in
   superposition (8½ orders of magnitude) and the vibration noise (about 1¾ orders).

Caveats: the gas rate is now derived (H5b). It assumes hard-sphere collisions;
van der Waals capture at 0.15 K reaches only a few nm beyond the surface, negligible
next to R. The mean-field (λ = 0) model is the Schrödinger–Newton picture.
Without added noise, that picture is a nonlinear quantum theory with known
consistency problems. Consistent classical-gravity models add extra decoherence,
which would make λ = 0 even easier to tell apart from λ = 1. That extra decoherence
isn't modelled here.
