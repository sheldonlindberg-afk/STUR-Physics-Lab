# Pre-registration: is G induced by stage 1's own matter, cut off at its Landau pole?

*Written before the calculation, so that the pass and fail conditions can't be moved to fit the
result. Independent work, not peer reviewed. Status: **registered, not yet computed.***

## The hypothesis (MODEL)

Gravity is not unified with 3-3-1 ([GRAVIGUT_NOGO.md](GRAVIGUT_NOGO.md)). Instead Newton's
constant is induced, as Sakharov proposed: it is the one-loop response of stage 1's own
fields to curvature, cut off at the one scale stage 1 already has, the U(1)_X Landau pole.
If this holds, the chain's one gravitational input, the measured G, becomes a prediction from
stage 1. Stage 1 already uses M_Pl to select N_c = 3, so the two together would form a
self-consistency condition. If it fails, the hypothesis is dropped.

## The formula (LIT, quoted, not derived here)

M. Visser, "Sakharov's induced gravity: a modern perspective", Mod. Phys. Lett. A17 (2002)
977, [arXiv:gr-qc/0204062](https://arxiv.org/abs/gr-qc/0204062), read from the v1 HTML:

- proper-time cutoff κ, eq. (7); heat-kernel expansion, eq. (8); a₁ = k₁R − m², eqs. (13)–(14);
- eq. (21): **1/G = 1/G₀ − (1/2π) str[k₁] κ² + UV finite**, where str = Tr[(−)^F] (eq. 12):
  fermions enter with a minus sign;
- Table I, per species (bare traces; the minus sign for fermions comes from str):

| Field | k₁ | Into str[k₁] |
|---|---|---|
| real scalar, coupling ξ to R | 1/6 − ξ | +(1/6 − ξ) |
| Weyl fermion | −1/6 | +1/6 |
| massless gauge vector, ghosts included | −2/3 | −2/3 |

Cross-check: these agree with the general a₂ = tr(E + R/6) of D. Vassilevich, Phys. Rept.
388 (2003) 279, [arXiv:hep-th/0306138](https://arxiv.org/abs/hep-th/0306138), for a scalar
(E = −ξR), the squared Dirac operator (E = −R/4) and a Feynman-gauge vector with two ghosts.
The Vassilevich table itself was read only in summary. The cross-check is arithmetic done here.

With Sakharov's assumption 1/G₀ = 0 (Visser, Sec. 4), and with M_Pl² = ħc/G in natural units:

**M_Pl² = −str[k₁] κ² / (2π).**   So a positive G **requires str[k₁] < 0**: gauge vectors must
outweigh scalars and fermions.

## The inputs, all from stage 1 (CHECK, computed from the merged simulation's functions)

- N_V: generators of SU(3)_C × SU(3)_L × U(1)_X = 8 + 8 + 1 = 17.
- N_W: left-handed Weyl components from `running._fields_331` (66 for β = −1/√3, 69 for
  β = +1/√3; [GRAVIGUT_NOGO.md](GRAVIGUT_NOGO.md) N2).
- N_S: real scalar components of the three triplets in `running._fields_331` (18).
- κ: the U(1)_X Landau pole of the selected variant, β = +1/√3 (stage 1 selects N_c = 3 with
  it). One loop with α_X = 1 gives 5.335×10¹⁹ GeV (stage `running`). Three loops gives
  3.49×10¹⁹ GeV (`inputs.POLES_331`).
- Not included: the graviton's own loop (Sakharov's gravity is not quantized), and the
  scalars' coupling ξ, which stage 1 does not fix.

## What will be computed

1. str[k₁] = N_S (1/6 − ξ) + N_W/6 − 2N_V/3, for both variants, at ξ = 0 (minimal) and
   ξ = 1/6 (conformal), the only two values with a structural reason.
2. Where str[k₁] < 0: κ_needed = M_Pl √(2π/(−str[k₁])), against the pole.
3. The ξ that would be needed for each variant, reported as a fit, not a prediction.

## Pass and fail, fixed now

The comparison κ ↔ Landau pole carries O(1) uncertainty from three sources:
- the proper-time cutoff is not a pole;
- α_X = 1 is a criterion, not a sharp scale;
- the one-loop and three-loop poles differ by a factor of 1.5.

So the band is generous, but closed:

| Outcome | Condition |
|---|---|
| **PASS (prediction)** | β = +1/√3, ξ = 0 or ξ = 1/6: str[k₁] < 0 **and** κ_needed / pole ∈ [1/3, 3] for the one- or three-loop pole |
| **CONDITIONAL (fit)** | the same holds only for some other ξ. Then ξ is a new parameter traded for G: no net prediction. Recorded, not claimed |
| **FAIL** | str[k₁] ≥ 0 at both structural ξ values (wrong-sign or infinite G), or κ_needed outside the band |
| **Variant test** | β = −1/√3, whose pole is 10¹⁰ M_Pl above, must fail the band. If it passed, the test would not discriminate |

Known reasons the result can't be stronger than MODEL, stated now:
- Visser's Sec. 5 notes that one-loop finiteness needs str(1) = str(m²) = str(m⁴) = 0,
  which no known spectrum satisfies. The cutoff version used here is the original Sakharov
  form, which Visser calls attractive but of doubtful predictive power (Sec. 4).
- The sign of the vector contribution is the subtle point in the literature: the gauge-field
  "contact term", Kabat, [arXiv:hep-th/9503016](https://arxiv.org/abs/hep-th/9503016). It
  was not read for this registration. A pass would have to survive it before being claimed.
- The overall sign convention of eq. (21) was checked against Visser's own statement in
  eq. (29), str[k₁] ≈ −1 giving positive 1/G, and not re-derived.

## Disclosure

A rough tally was made while reading the sources, before this registration was written.
It suggested that the selected variant's sign is marginal (close to zero at ξ = 1/6). The
conditions above were chosen for the physics reasons stated, not adjusted to that tally. The
structural ξ values and the factor-3 band are the natural choices, and the variant test
was added so that a pass could not be trivial.
