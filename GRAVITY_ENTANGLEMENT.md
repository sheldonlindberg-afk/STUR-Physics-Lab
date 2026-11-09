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

Not modelled: blackbody decoherence, trap and acceleration noise, and the
splitting and recombining stages (the branches are held at fixed distances for
the full τ). Each of these makes the dephasing budget tighter, never looser.
