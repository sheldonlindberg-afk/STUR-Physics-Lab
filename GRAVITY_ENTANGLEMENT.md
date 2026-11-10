# Gravity-induced entanglement: is gravity's field split, or in two places?

Reproduce: `python3 src/stur_gravity_entanglement.py` (under 1 s). The full output is
in `results/gravity_entanglement/output.txt`, and `tests/test_gravity_entanglement.py`
pins the numbers. Labels: KNOWN, FOLLOWS, LIT, PROPOSAL. Only Newtonian gravity
(G m²/r) and ordinary electromagnetism are used. Nothing exotic.

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

- Gas collisions are an order-of-magnitude estimate, assuming nitrogen as the leftover gas.
- At the published target of 10⁻¹⁵ Pa and 0.15 K, the collision rate is about 0.1 /s
  (γτ ≈ 0.26). That uses most of the budget by itself.
- At 10⁻¹³ Pa the collision rate is 100× too high.

The vacuum is the hardest requirement in the experiment.

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

This is the first STUR quantity in this repository that is a free parameter of
known physics, that an experiment under construction can measure, and that is not
already excluded. Results from either branch of this test go back into
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
| A: 10⁻¹⁵ Pa N₂, 0.15 K, no vibration, unlimited spin coherence | 1.5×10⁻¹⁴ kg, Δx = 721 µm, ramps 2×1.58 s, hold 0.08 s, Δφ = 2.19 rad | **565 runs, 1.3 h** |
| A′: as A, leftover gas is helium | — | **no design works** |
| B: A + spin coherence 1.6 s | — | no design works |
| C: A + internal temperature 4 K | — | no design works |
| D: A + 10⁻¹⁴ Pa | — | no design works |
| E: A + LISA Pathfinder vibration | — | no design works |

In design A, gas collisions use γτ = 0.44 of a 0.80 budget. Almost all of the
entangling phase builds up during the ramps.

**Requirements, each varied alone**

| Requirement | Others at target (A) | Others ideal (10⁻¹⁷ Pa) |
|---|---|---|
| Internal temperature | < 1.19 K | < 2.4 K |
| Spin coherence | > 2.1 s | > 0.8 s |
| Vibration (acceleration noise) | < 1.3×10⁻¹⁷ m s⁻²/√Hz | < 4.4×10⁻¹⁷ |
| Vacuum (others ideal) | N₂ < 1.8×10⁻¹⁵ Pa, He < 6.9×10⁻¹⁶ Pa | |

**H6. EM forces that can fake a positive result.** Noise can't create entanglement;
it can only hide it. But electromagnetic *interactions* between the diamonds can
create it:

- **Net charge:** one electron's worth of charge on each diamond gives an entangling
  phase **1.6×10¹⁰× gravity's**. Both diamonds must carry exactly zero net charge.
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
| Mass in a spatial superposition | 1.5×10⁻¹⁴ kg | 4×10⁻²³ kg (Fein et al. 2019): **4×10⁸× short** |
| Superposition size | 721 µm | |
| Vacuum | < 2×10⁻¹⁵ Pa (N₂), < 7×10⁻¹⁶ Pa (He) | reached only in cryogenic systems |
| Spin coherence | > 2.1 s | ~1 s (NV, cryogenic, with dynamical decoupling) |
| Internal temperature | < 1.2 K | micro-diamonds heat up under trapping light |
| Vibration (acceleration noise) | < 1.3×10⁻¹⁷ m s⁻²/√Hz | 1.7×10⁻¹⁵ (LISA Pathfinder): **~140× short** |
| Charge / dipoles | exactly 0 / < 4×10⁻²⁹ C·m, or a shield | zero charge demonstrated |

1. **Nothing in the physics forbids the test.** At the published targets, the best
   design settles λ = 0 against λ = 1 in about 565 runs (1.3 h of running). But it sits
   on the edge: with helium as the leftover gas, or a 10× worse vacuum, no design works.
2. **λ = 0 (split field) predicts exactly zero gravitational entanglement.** A positive
   witness can't come from noise. It could come from EM, which is why H6's controls
   are part of the prediction.
3. **How finely λ can be pinned down** is set by dephasing. With 10⁶ runs, design A
   reaches λ > 0.44. At 10⁻¹⁷ Pa it reaches λ > 0.028.
4. **What stands between the question and its answer is engineering, not theory.** The
   requirements must all be met at once, and the largest gaps are the mass in
   superposition (8½ orders of magnitude) and the vibration noise (about 2 orders).

Caveats: the gas formula is an order-of-magnitude estimate, and the outcome of design
A hinges on it. The mean-field (λ = 0) model is the Schrödinger–Newton picture.
Without added noise, that picture is a nonlinear quantum theory with known
consistency problems. Consistent classical-gravity models add extra decoherence,
which would make λ = 0 even easier to tell apart from λ = 1. That extra decoherence
isn't modelled here.
