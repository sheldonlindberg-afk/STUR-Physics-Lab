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
| D0 | Start: quantum mechanics (with the Born rule) and N local quantum fields with spacing a | Assumed | — |
| D1 | The vacuum's entanglement across any surface obeys an area law: S = 0.3047 (R/a)² per field | Srednicki's method, R/a = 10.5–18.5, extrapolated | CHECK (LIT 0.30) |
| D2 | The vacuum is thermal to every accelerated observer: K = 2π × boost energy, T = ħg/(2πck_B) | Lattice modular Hamiltonian: 0.99969, 0.99992, 0.99997 of 2π at L = 20, 40, 60 | CHECK |
| D3 | Clausius (δQ = TδS) on every local horizon gives Einstein's equations, with 1/(4Għ) = entanglement per area | Jacobson 1995 | LIT, not recomputed |
| D4 | The same equations from the TEGR action (c⁴/16πG)∫eT: gravity is torsion on flat spacetime | T = −R + divergence, residual 10⁻¹⁶⁸ | CHECK |
| D5 | Static solution: Schwarzschild, uniquely. Weak field: Ψ = Φ, ∇²Φ = 4πGρ | TEGR field equations solved symbolically | CHECK |
| D6 | In a superposition each branch sources its own field: the equation above | What D0 implies for a field made of the quantum level. Exact in the lattice analog: phase 0.6064 vs 1/r law 0.6046, record 2×10⁻⁶ | FOLLOWS + analog |

## What comes out of it (D7)

| | Consequence | Number |
|---|---|---|
| (a) | **Double slit with a detector:** V = \|⟨E₁\|E₂⟩\|. No observer is needed, only a record | D² + V² = 1.000000 at every detector strength |
| (b) | **The electron's own field** is in both branches. In free space it leaves no record. Near a surface, image charges record the path and the fringes fade | LIT: Sonnentag & Hasselbach 2007. A literally split charge is excluded (MEASUREMENT.md) |
| (c) | **One mass, gravity's own record:** \|⟨E₁\|E₂⟩_grav\| = e^(−N/2) | N = 1.4×10⁻⁵⁹ gravitons: gravity keeps no record |
| (d) | **Two masses:** the action difference alone entangles them | 0.594 rad; concurrence 0.293. Best design: 565 runs, 1.3 h (GRAVITY_ENTANGLEMENT.md) |
| (e) | **Classical limit** (one branch, many particles) | Perihelion 42.98″/century; light bending 1.7512″; γ = 1; GPS +38.54 µs/day |
| (f) | **If gravity were only an average** (not D6): no entanglement in (d), and intrinsic collapse is needed | Diósi–Penrose: 170 /s, so one diamond's superposition lasts ~6 ms instead of > 3 s |

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
  entanglement. Gravity then joins the other fields in |Eᵢ⟩ (D6).

## What was put in, and what was not derived (D8)

- **Put in:** quantum mechanics with the Born rule; N local fields; the spacing a.
- **Computed:** c_s, the Unruh/modular structure, the TEGR identity, Schwarzschild and
  Newton, and every number in D7.
- **From the literature:** Jacobson's step D3.
- **Not derived:**
  - the value of G (the measured G fixes only a²/N: a = 0.31 ℓ_P for one field, 3.1 ℓ_P
    for a hundred);
  - the Born rule;
  - the particle content (the Standard Model).
- **The one physical claim beyond textbook physics:** D6 applies to gravity. That is,
  gravity emerges *collectively* from the quantum level, as phonons do in a crystal, and
  not as a statistical average. It is tested by (c) and (d), and (f) is what failure
  would look like.
- **Status:** every ingredient is published physics. The chain, the λ framing and the
  computed checks are this project's. The equation contains no adjustable parameter
  beyond the measured G.
