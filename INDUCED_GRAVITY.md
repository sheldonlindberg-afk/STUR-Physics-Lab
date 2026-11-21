# Newton's constant induced by stage 1's own matter

*Whether G is induced by the 3-3-1 fields of the merged simulation's stage 1, cut off at the one
scale stage 1 already has, the U(1)_X Landau pole. Independent work, not peer reviewed.*

Run it: `python3 src/induced_gravity.py` (standard library only, under a second; output in
[results/induced_gravity/output.txt](results/induced_gravity/output.txt)). Pinned by
[`tests/test_induced_gravity.py`](tests/test_induced_gravity.py).

## The result in one paragraph

Gravity's gauge group is not derived from stage 1 ([GRAVIGUT_NOGO.md](GRAVIGUT_NOGO.md)), so
this asks the other question: is G induced by stage 1's own matter, as Sakharov proposed?
Counting stage 1's 17 gauge vectors, 69 Weyl fermions and 18 real scalars, and cutting off
at the U(1)_X pole (2.9–4.4 M_Pl), gives **M_Pl between 0.47 and 3.1 times its measured value**.
So G comes out at 0.10–4.6 times the measured value, with no input from gravity at all. The
other variant, whose pole lies 10¹⁰ M_Pl up, fails. So does N_c = 5, which would induce
M_Pl ≈ 10¹² GeV. This is a MODEL result: an order-of-magnitude prediction of G that rests on
Sakharov's assumptions, listed below.

## The formula (LIT)

Sakharov's induced gravity at one loop, with a proper-time cutoff κ and no tree-level term.
In the standard convention (G > 0 attractive, Euclidean action −(1/16πG)∫√g R), a boson's
W = ½ ln det D = −½∫_{1/κ²}^∞ (dt/t) Tr e^{−tD} contains −(κ²/32π²)∫√g a₁, with a₁ = k₁R. So

**1/G = (1/2π) str[k₁] κ²,  M_Pl² = str[k₁] κ²/(2π),  str[k₁] = N_S(1/6 − ξ) + N_W/6 − 2N_V/3.**

| Field | k₁ | Into str[k₁] |
|---|---|---|
| real scalar, coupling ξ to R | 1/6 − ξ | +(1/6 − ξ) |
| Weyl fermion | −1/6 | +1/6 (fermions enter str with a minus sign) |
| massless gauge vector, ghosts included | −2/3 | −2/3 |

Sources:
- The species coefficients: M. Visser, Mod. Phys. Lett. A17 (2002) 977,
  [arXiv:gr-qc/0204062](https://arxiv.org/abs/gr-qc/0204062), Table I. They agree with the
  general a₂ = tr(E + R/6) of D. Vassilevich, Phys. Rept. 388 (2003) 279,
  [arXiv:hep-th/0306138](https://arxiv.org/abs/hep-th/0306138).
- The scalar formula, verbatim: F. Larsen and F. Wilczek, Nucl. Phys. B458 (1996) 249,
  [arXiv:hep-th/9506066](https://arxiv.org/abs/hep-th/9506066), sec. 3.3,
  1/G_ren = 1/G_bare + (1/2π)(1/6 − ξ)/ε².
- The positive scalar and Dirac terms: S. Solodukhin, Living Rev. Rel. 14 (2011) 8,
  [arXiv:1104.3712](https://arxiv.org/abs/1104.3712), eqs. (115), (137), (141).
- Gauge fields: Kabat's contact term enters the black-hole entropy, not entanglement entropy
  ([arXiv:hep-th/9503016](https://arxiv.org/abs/hep-th/9503016), abstract). It does not change
  the vector's heat-kernel contribution to 1/G.

So scalars and fermions induce positive G and gauge vectors negative: positive G needs the
matter to outweigh the vectors.

## The inputs, all from stage 1 (CHECK)

| | β = +1/√3 (selected) | β = −1/√3 |
|---|---|---|
| N_V (8 + 8 + 1 generators) | 17 | 17 |
| N_W, from `running._fields_331` | 69 | 66 |
| N_S (three complex triplets) | 18 | 18 |
| U(1)_X pole, one loop (stage `running`) | 5.34×10¹⁹ GeV = 4.37 M_Pl | 4.5×10²⁹ GeV |
| U(1)_X pole, three loops (`inputs.POLES_331`) | 3.49×10¹⁹ GeV = 2.86 M_Pl | 2.3×10²⁹ GeV |

ξ is not fixed by stage 1, so the two values with a structural reason are used: ξ = 0
(minimal) and ξ = 1/6 (conformal). The graviton's own loop is not included.

## The test and its result

The conditions were fixed before computing:
- ξ is 0 or 1/6;
- pass if str[k₁] > 0 and the cutoff the measured G needs is within a factor of 3 of the
  selected variant's pole (one- or three-loop);
- the other variant must fail, or the test would not discriminate.

The overall sign of the relation was corrected after a first computation, from the sources
above. The conditions were not changed.

| Selected β = +1/√3 | str[k₁] | κ needed | / 1-loop pole | / 3-loop pole | In band [1/3, 3] |
|---|---|---|---|---|---|
| ξ = 0 | +19/6 | 1.41 M_Pl | 0.32 | 0.49 | yes (3-loop pole) |
| ξ = 1/6 | +1/6 | 6.14 M_Pl | 1.40 | 2.15 | yes (both) |

β = −1/√3: ξ = 0 needs a cutoff 10⁻¹⁰ of its pole, and ξ = 1/6 gives str[k₁] = −1/3, no
positive G. **Verdict: PASS (prediction), and the test discriminates between the variants.**

**What it predicts.** M_Pl = pole · √(str[k₁]/2π):

| ξ | 1-loop pole | 3-loop pole |
|---|---|---|
| 0 | M_Pl = 3.10 × measured (G = 0.10 ×) | 2.03 × (G = 0.24 ×) |
| 1/6 | 0.71 × (G = 1.97 ×) | 0.47 × (G = 4.61 ×) |

It also closes stage 1 on itself. Because str[k₁] < 2π, the induced M_Pl lies below the
N_c = 3 pole, which is the condition stage 1 uses to select N_c = 3.

## What it does not do

- **It predicts an order of magnitude, not a value.** The spread comes from ξ and from the 1- vs
  3-loop pole. Most of the content is two facts: the selected variant's pole lies at 3–4 M_Pl,
  and its fermions outweigh its vectors. The other variant shows that the first fact is not
  automatic.
- **Sakharov's assumptions stay assumptions:** no tree-level 1/G₀; a proper-time cutoff
  identified with a Landau pole, which is a criterion (α_X = 1), not a physical scale; no
  graviton loop.
- **The cosmological constant is not solved.** The same loop induces a vacuum energy with
  str[1] = N_S + 2N_V − 2N_W = −86, of order κ⁴: about 10¹²² times the measured value.
- **Beyond the test:** the N_c = 5 content at its own pole (7.3×10¹¹ GeV) would induce
  M_Pl ≈ 9×10¹¹ GeV, 10⁻⁷ of the measured value. Of the two, only N_c = 3 reproduces G.

**Status for the chain:** a MODEL result worth a blind rebuild. Its next gates are an
independent build of the induced coefficient and a verifier check of the sign. If it passes
them, it is a candidate stage 0, with the measured G as a branch with a pull.
