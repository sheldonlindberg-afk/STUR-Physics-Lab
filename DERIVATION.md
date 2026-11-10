# The equation, from the quantum level up

Reproduce: `python3 src/stur_derivation.py` (about 30 s). The full output is in
`results/derivation/output.txt`, and `tests/test_derivation.py` pins it. Every number
below is recomputed by that script from the modules it names.

## The equation

```
|Ψ⟩ = Σᵢ cᵢ |i⟩_matter |Eᵢ⟩_fields e^{iSᵢ/ħ}

Sᵢ  = S_matter[i] + S_EM[i] + (c⁴/16πG) ∫ eᵢ T[eᵢ] d⁴x        (TEGR: gravity as torsion)
G   = π a² c³ / (N c_s ħ),   c_s = 0.3046                     (from vacuum entanglement)

ρᵢⱼ(t) = ρᵢⱼ(0) · ⟨Eⱼ|Eᵢ⟩ · e^{i(Sᵢ − Sⱼ)/ħ}
```

In words:
- **The branches:** a system in a superposition carries, in each branch i, its own
  configuration of every field it sources. That includes detectors, light, its own
  electric field, and gravity's tetrad eᵢ.
- **The overlap ⟨Eⱼ|Eᵢ⟩:** how far the fields keep a record of which branch happened.
  This is what makes outcomes definite.
- **The phase:** the difference in action between branches, including the gravitational
  field's own action.
- **The strength of gravity, G:** a property of the quantum vacuum, namely how much it is
  entangled per unit area.

## The derivation

| Step | Result | How | Check |
|---|---|---|---|
| D0 | Start: unitary quantum mechanics, locality (no-signaling), non-contextual probabilities, and N local quantum fields with spacing a | Assumed | — |
| DB | **The Born rule:** probability = \|amplitude\|² | Envariance (fine-graining gives p = m/M exactly); only F(x) = x is additive (10⁻¹⁵); any other power signals faster than light; wrong-frequency branches carry weight 2×10⁻²⁴ at N = 10⁴ ([BORN.md](BORN.md)) | CHECK |
| D1 | The vacuum's entanglement across any surface obeys an area law: S = 0.3047 (R/a)² per field (0.3046 from the longer R/a = 10.5–26.5 run in UNIFICATION.md; the equation uses 0.3046) | Srednicki's method, R/a = 10.5–18.5, extrapolated | CHECK (LIT 0.30) |
| D2 | The vacuum is thermal to every accelerated observer: K = 2π × boost energy, T = ħg/(2πck_B) | Lattice modular Hamiltonian: 0.99969, 0.99992, 0.99997 of 2π at L = 20, 40, 60 | CHECK |
| D3 | Clausius (δQ = TδS) on every local horizon gives Einstein's equations, with 1/(4Għ) = entanglement per area | Jacobson 1995 | LIT, not recomputed |
| D4 | The same equations from the TEGR action (c⁴/16πG)∫eT: gravity is torsion on flat spacetime | T = −R + divergence, residual ≤ 10⁻¹⁶⁵ at random points | CHECK |
| D5 | Static solution: Schwarzschild, uniquely. Weak field: Ψ = Φ, ∇²Φ = 4πGρ | TEGR field equations solved symbolically | CHECK |
| D6 | In a superposition each branch sources its own field: the equation above | A Markovian statistical gravity coarse-grained at the cutoff a would heat matter at 0.5 W/kg, 6×10¹⁰ times the Earth's heat flow, so gravity is collective ([COLLECTIVE.md](COLLECTIVE.md), [OPPENHEIM.md](OPPENHEIM.md)). Lattice analog: phase 0.6064 vs 1/r law 0.6046, record 2×10⁻⁶ | **FOLLOWS under R₀ = a, Markovian** (+ analog) |

**When D6 follows from D1–D3, and when it doesn't.** Jacobson's step gives Einstein's
equation as an equation of state, which is semiclassical. Taken by itself it points, if
anywhere, toward an averaged field (λ = 0), not toward D6.

The argument for D6 runs as follows:

1. A statistical gravity, a classical average of the quantum level, must carry noise in
   order to respond to quantum matter.
2. The least noise any Markovian model can carry is the Diósi–Penrose kernel 4πG/ħq²,
   smeared over a length R₀. This holds for Oppenheim's classical–quantum gravity as
   well ([OPPENHEIM.md](OPPENHEIM.md) P2).
3. **Identify R₀ with the cutoff a.** An equation of state is coarse-grained where its
   degrees of freedom are counted, and D1–D3 contain no other length.
4. Then the noise heats every kilogram of matter by about 0.5 W (the nuclei's own size
   limits it). That is 6×10¹⁰ times the Earth's heat flow, so gravity's field is
   collective: it follows each branch of its sources, as sound follows the atoms of a
   crystal ([COLLECTIVE.md](COLLECTIVE.md)).

**Step 3 is an identification, not a theorem.**
- A statistical gravity can put in a larger R₀ by hand, and then it survives this
  argument. One diamond tests it, for R₀ up to 455 µm (COLLECTIVE §4; OPPENHEIM P3).
- Non-Markovian classical gravity is not covered at all.

So D6 is derived **under R₀ = a and Markovian dynamics**, not unconditionally. (An
earlier version quoted 10⁵⁶–10⁶⁰ W/kg for step 4. That figure treats nuclei as points;
see OPPENHEIM.md P4.)

## What comes out of it (D7)

| | Consequence | Number |
|---|---|---|
| (a) | **Double slit with a detector:** V = \|⟨E₁\|E₂⟩\|. No observer is needed, only a record | D² + V² = 1.000000 at every detector strength |
| (b) | **The electron's own field** is in both branches. In free space it leaves no record. Near a surface, image charges record the path and the fringes fade | LIT: Sonnentag & Hasselbach 2007. A literally split charge is excluded (MEASUREMENT.md) |
| (c) | **One mass, gravity's own record:** \|⟨E₁\|E₂⟩_grav\| = e^(−N/2) | N = 1.4×10⁻⁵⁹ gravitons: gravity keeps no record |
| (d) | **Two masses:** the action difference alone entangles them | Baseline (10⁻¹⁴ kg, 2.5 s): 0.594 rad, concurrence 0.293. Best design A (1.5×10⁻¹⁴ kg): 2.19 rad, 565 runs, 1.3 h (GRAVITY_ENTANGLEMENT.md) |
| (e) | **Classical limit** (one branch, many particles) | Perihelion 42.98″/century; light bending 1.7512″; γ = 1; GPS +38.54 µs/day |
| (f) | **One mass keeps its superposition:** gravity adds no decoherence | A design-A diamond stays fully coherent for 3.24 s. A statistical gravity would leave ≤ 1.3% for any smearing allowed by Newton's law, and 10⁻²³⁹ at the radiation bound (COLLECTIVE.md) |
| (g) | **Classical gravity's squeeze (Oppenheim):** one particle measured two ways | Γ·S_a ≥ (M²/4)I² for any kernels; a coherent, quiet design-A diamond needs CQ noise 10⁵× above its own requirement (OPPENHEIM.md) |

## How your three starting ideas sit in the equation

- **"Measuring creates what we see."** That is the factor ⟨Eⱼ|Eᵢ⟩ → 0. A definite
  outcome appears when the fields hold a record, whether or not anyone looks.
- **"The electron is an EM cloud, not just a probability."** Its field *is* in both
  branches, as part of |Eᵢ⟩. But it is in two places as an amplitude, not as a charge
  split in half, since a split charge repels itself and is excluded.
- **"Entanglement is one thing stretched across space."** That is the joint state: matter
  and its fields, branch by branch, one object. It gives the full quantum correlations,
  and it cannot send signals.
- **"Gravity is a consequence of the quantum level."** That is D1–D3: G comes from vacuum
  entanglement. Gravity then joins the other fields in |Eᵢ⟩ (D6), and it has to: an
  averaged gravity smeared at the theory's own cutoff would heat all matter
  (COLLECTIVE.md). That conclusion depends on the smearing being the cutoff.

## What was put in, and what was not derived (D8)

- **Put in:** unitary quantum mechanics; locality and non-contextuality; N local fields; the spacing a.
- **Computed:** the Born rule (DB), c_s, the Unruh/modular structure, the TEGR identity,
  Schwarzschild and Newton, and every number in D7.
- **From the literature:** Jacobson's step D3.
- **Not derived:**
  - the value of G (the measured G fixes only a²/N: a = 0.31 ℓ_P for one field, 3.1 ℓ_P
    for a hundred);
  - the particle content (the Standard Model).
- **Gravity's character is derived, but only conditionally:** its field follows each
  branch (D6), because a Markovian statistical gravity smeared at the same cutoff that
  fixes G would heat ordinary matter 6×10¹⁰ times faster than observed. With a larger
  smearing put in by hand, or non-Markovian dynamics, the argument doesn't apply, and
  experiment decides.
- **λ = 1 doesn't single this theory out.** Perturbative (effective-field-theory) quantum
  gravity predicts the same thing. A positive result in (d) or (f) would rule out
  classical gravity, Oppenheim's included, but it wouldn't confirm this framework over
  standard physics. Only a null result would be new physics.
- **Every ingredient is published physics.** The chain, the derivation of D6, the λ
  framing and the computed checks are this project's. The equation contains no
  adjustable parameter beyond the measured G. All predictions, with numbers:
  [PREDICTIONS.md](PREDICTIONS.md).
