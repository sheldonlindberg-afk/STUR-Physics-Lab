# The bookkeeping equation: known physics, step by step

*Research notes, not peer reviewed. Labels mark what is established physics, what is computed here, and what holds only under stated assumptions.*

This page writes known physics (decoherence, the Born-rule arguments, Jacobson's
thermodynamic argument and TEGR) as one equation. It is a synthesis, not a new theory.

Reproduce: `python3 src/stur_derivation.py` (about 30 s). The full output is in
`results/derivation/output.txt`, and `tests/test_derivation.py` pins it. Every number
below is recomputed by that script from the modules it names.

## The equation

```
|Ψ⟩ = Σᵢ cᵢ |i⟩_matter |Eᵢ⟩_fields e^{iSᵢ/ħ}

Sᵢ  = S_matter[i] + S_EM[i] + (c⁴/16πG) ∫ eᵢ T[eᵢ] d⁴x        (TEGR: gravity as torsion)
G   = π a² c³ / (N c_s ħ),   c_s = 0.3046                     (Jacobson's hypothesis)

ρᵢⱼ(t) = ρᵢⱼ(0) · ⟨Eⱼ|Eᵢ⟩ · e^{i(Sᵢ − Sⱼ)/ħ}
```

In words:
- **The branches:** a system in a superposition carries, in each branch i, its own
  configuration of every field it sources. That includes detectors, light, its own
  electric field and, if gravity is quantum, gravity's tetrad eᵢ.
- **The overlap ⟨Eⱼ|Eᵢ⟩:** how far the fields keep a record of which branch happened.
  When it goes to zero the branches no longer interfere (decoherence). Why one outcome
  is then seen is a question of interpretation that the equation doesn't settle.
- **The phase:** the difference in action between branches, including the gravitational
  field's own action.
- **The G line:** if Jacobson's argument holds, G is tied to how much the quantum vacuum
  is entangled per unit area. It relates G to unknowns (a²/N) and doesn't predict it.

## The steps

| Step | Result | How | Status |
|---|---|---|---|
| D0 | Start: unitary quantum mechanics, locality (no-signaling), non-contextual probabilities, and N local quantum fields with spacing a | Assumed | — |
| DB | **The Born rule:** probability = \|amplitude\|² | Published arguments reproduced: envariance (fine-graining gives p = m/M exactly); only F(x) = x is additive (10⁻¹⁵); any other power signals faster than light; wrong-frequency branches carry weight 2×10⁻²⁴ at N = 10⁴ ([BORN.md](BORN.md)) | CHECK; the arguments' assumptions are debated |
| D1 | The vacuum's entanglement across any surface obeys an area law: S = 0.3047 (R/a)² per field (0.3046 from the longer R/a = 10.5–26.5 run in `src/stur_unification.py`; the equation uses 0.3046) | Srednicki's method, R/a = 10.5–18.5, extrapolated | KNOWN; CHECK (LIT 0.30) |
| D2 | The vacuum is thermal to every accelerated observer: K = 2π × boost energy, T = ħg/(2πck_B) | Lattice modular Hamiltonian: 0.99969, 0.99992, 0.99997 of 2π at L = 20, 40, 60 | KNOWN (Bisognano–Wichmann, Unruh); CHECK |
| D3 | If Clausius (δQ = TδS) holds on every local horizon, Einstein's equations follow, with 1/(4Għ) = entanglement per area | Jacobson 1995, re-checked step by step in `src/stur_jacobson.py`: Raychaudhuri (exact on FRW with general a(t)), the null-vector lemma X_kk = 0 ⇒ X ∝ g (one free parameter left), and the contracted Bianchi identity (exact on a general time-dependent spherical metric) | HYPOTHESIS: the algebra is checked; the premise (local equilibrium on every local horizon) is assumed |
| D4 | The same equations from the TEGR action (c⁴/16πG)∫eT: gravity written as torsion on flat spacetime | T = −R + divergence, residual ≤ 10⁻¹⁶⁵ at random points | KNOWN; CHECK |
| D5 | Static solution: Schwarzschild, uniquely. Weak field: Ψ = Φ, ∇²Φ = 4πGρ | TEGR field equations solved symbolically | KNOWN; CHECK |
| D6 | In a superposition each branch sources its own gravitational field: the equation above | Open experimentally. Argued here only under two assumptions: a Markovian statistical gravity coarse-grained at the cutoff a would heat matter at 0.5 W/kg, 6×10¹⁰ times the Earth's heat flow ([COLLECTIVE.md](COLLECTIVE.md), [OPPENHEIM.md](OPPENHEIM.md)). Lattice analog: phase 0.6064 vs 1/r law 0.6046, record 2×10⁻⁶ | **CONDITIONAL** (R₀ = a, Markovian) + analog |

## What D6 rests on

Jacobson's step gives Einstein's equation as an equation of state, which is
semiclassical. Taken by itself it points, if anywhere, toward an averaged field
(λ = 0), not toward D6. So D6 needs an argument of its own, and the one here has four
steps:

1. A statistical gravity, a classical average of the quantum level, must carry noise in
   order to respond to quantum matter (Diósi; Tilloy & Diósi).
2. The least noise any Markovian model can carry is the Diósi–Penrose kernel 4πG/ħq²,
   smeared over a length R₀. This holds for Oppenheim's classical–quantum gravity as
   well ([OPPENHEIM.md](OPPENHEIM.md) P2).
3. **Assume R₀ equals the cutoff a.** The motivation: an equation of state is
   coarse-grained where its degrees of freedom are counted, and D1–D3 contain no other
   length. This is an assumption, not a theorem.
4. Then the noise heats every kilogram of matter by about 0.5 W (the nuclei's own size
   limits it). That is 6×10¹⁰ times the Earth's heat flow, which rules such a model out.

**What escapes the argument.**
- A statistical gravity with a larger R₀ put in by hand survives it. One diamond would
  test that, for R₀ up to 448 µm (COLLECTIVE §4; OPPENHEIM P3).
- Non-Markovian classical gravity is not covered at all.
- The systematic treatment of classical gravity's minimal noise is in the literature
  (Fabiano et al. 2026; Angeli et al. 2025; see [NOVELTY.md](NOVELTY.md)). The
  calculation here is a worked example within it.

So D6 holds **under R₀ = a and Markovian dynamics** only. Its label is CONDITIONAL.

**How D3 and D6 fit together.** Jacobson's step (D3) is usually stated for the averaged
stress energy ⟨T_μν⟩, which is the semiclassical form. If D6 holds, it is applied inside
each branch instead:
- the vacuum's entanglement per area (D1) is the same in every branch;
- so each branch's local horizons obey the same Clausius relation, with that branch's
  own T_μν;
- each branch then satisfies Einstein's equation with its own source, which is what the
  equation's Sᵢ uses.

This is an interpretation of D3, not a recomputation. It is also exactly where a
statistical (λ = 0) reading would differ. (An earlier version quoted 10⁵⁶–10⁶⁰ W/kg for
step 4. That figure treats nuclei as points; see OPPENHEIM.md P4.)

## What the equation gives (D7)

Items (a), (b) and (e) are standard physics recomputed. Items (c), (d), (f) and (g)
are worked examples; (d) and (f) assume gravity follows each branch.

| | Consequence | Number |
|---|---|---|
| (a) | **Double slit with a detector:** V = \|⟨E₁\|E₂⟩\|. No observer is needed, only a record | D² + V² = 1.000000 at every detector strength |
| (b) | **The electron's own field** is in both branches. In free space it leaves no record. Near a surface, image charges record the path and the fringes fade | LIT: Sonnentag & Hasselbach 2007. A literally split charge is excluded (MEASUREMENT.md) |
| (c) | **One mass, gravity's own record:** \|⟨E₁\|E₂⟩_grav\| = e^(−N/2) | N = 1.3×10⁻⁵⁹ gravitons: gravity keeps essentially no record |
| (d) | **Two masses:** if gravity follows each branch, the action difference alone entangles them | Baseline (10⁻¹⁴ kg, 2.5 s): 0.594 rad, concurrence 0.293. Design A (1.5×10⁻¹⁴ kg): 2.19 rad, 270 runs, 0.6 h (GRAVITY_ENTANGLEMENT.md) |
| (e) | **Classical limit** (one branch, many particles) | Perihelion 42.98″/century; light bending 1.7512″; γ = 1; GPS +38.54 µs/day |
| (f) | **One mass keeps its superposition** if gravity follows each branch | A design-A diamond stays fully coherent for 3.24 s. A Markovian statistical gravity would leave ≤ 1.5% for any smearing allowed by Newton's law, and 10⁻²³¹ at the radiation bound (COLLECTIVE.md) |
| (g) | **Classical gravity's squeeze (Oppenheim):** one particle measured two ways | Γ·S_a ≥ (M²/4)I² for any kernels; a coherent, quiet design-A diamond needs CQ noise 10⁵× above its own requirement (OPPENHEIM.md). A worked example, not a new result |

## Where the starting ideas ended up

The project began from four informal ideas. Here is what known physics says about each.

- **"Measuring creates what we see."** Interference between outcomes disappears when the
  fields hold a record (⟨Eⱼ|Eᵢ⟩ → 0), whether or not anyone looks. Decoherence doesn't
  by itself say why one outcome is seen.
- **"The electron is an EM cloud, not just a probability."** Its field is in both
  branches, as part of |Eᵢ⟩. But it is there as an amplitude, not as a charge split in
  half: a split charge repels itself and is excluded.
- **"Entanglement is one thing stretched across space."** That is the joint state of
  matter and its fields, branch by branch. It gives the full quantum correlations, and
  it cannot send signals.
- **"Gravity is a consequence of the quantum level."** Not established. Jacobson's
  argument (D3) ties G to vacuum entanglement if its premise holds. Whether gravity then
  joins the other fields in |Eᵢ⟩ (D6) is open; the argument here for it depends on the
  smearing being the cutoff and on Markovian dynamics (COLLECTIVE.md).

## What was put in, and what was not derived (D8)

- **Put in:** unitary quantum mechanics; locality and non-contextuality; N local fields;
  the spacing a.
- **Computed here:** the published Born-rule arguments (DB), c_s, the Unruh/modular
  structure, the TEGR identity, Schwarzschild and Newton, and every number in D7.
- **Re-checked from the literature:** Jacobson's step D3 (`src/stur_jacobson.py`). Its
  premise, local equilibrium on every local horizon with the area term as the only
  entropy change, is assumed.
- **Not derived:**
  - the value of G (the measured G fixes only a²/N: a = 0.31 ℓ_P for one field, 3.1 ℓ_P
    for a hundred);
  - the particle content (the Standard Model);
  - the entanglement reading of G for gauge fields. For gauge fields the area-law
    coefficient includes a contact term that isn't entanglement of the field's physical
    modes (Kabat, Nucl. Phys. B 453, 281 (1995), [hep-th/9503016](https://arxiv.org/abs/hep-th/9503016)). So G = πa²c³/(N c_s ħ) is cleanest for N scalars
    or fermions. For the Standard Model's gauge fields, identifying 1/4Għ with
    entanglement alone is not settled, and c_s depends on the regulator in any case.
- **Whether gravity follows each branch is open.** The argument here (D6) holds only if a
  Markovian statistical gravity is smeared at the same cutoff that fixes G. With a
  larger smearing, or non-Markovian dynamics, it doesn't apply, and experiment decides.
- **λ = 1 doesn't single out these notes.** Perturbative (effective-field-theory) quantum
  gravity predicts the same thing. A positive result in (d) or (f) would rule out
  classical gravity, Oppenheim's included, but it wouldn't confirm these notes over
  standard physics. Only a null result would be new physics.
- **Every ingredient is published physics.** The way it is put together and the computed
  checks are this project's. The equation contains no adjustable parameter beyond the
  measured G. Every testable number, with requirements: [PREDICTIONS.md](PREDICTIONS.md).
