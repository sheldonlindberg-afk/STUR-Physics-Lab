# 3-3-1 from a triangle: an attempt at the 19 parameters from geometry

*Can one fixed geometry give the 3-3-1 gauge group, three generations, and the measured
couplings, masses and mixing? Every step is computed, and every failure is kept. Companion to
[WHY.md](WHY.md), which sorts the 19 parameters by what is known. Independent work, not peer
reviewed.*

Run it: `python3 src/triangle_orbifold.py` (about 10 s; output in
[results/triangle/output.txt](results/triangle/output.txt)). Pinned by
[`tests/test_triangle_orbifold.py`](tests/test_triangle_orbifold.py).

---

## The result in one paragraph

Take a six-dimensional SU(6) gauge theory whose two extra dimensions form a flat triangle
with three corners. The geometry has no free parameter. It gives the 3-3-1 gauge group and
every 3-3-1 fermion charge, three generations, one heavy generation when the Higgs sits at a
corner, and a quark mixing matrix close to the identity. It does not give the numbers.
Unification of the couplings fails with the minimal particle content, by a factor of 3.6 in
α_s. No symmetric Higgs potential produces the mass hierarchy. The mixing angles come out 30
to 60 times too small. Where the construction can be made to fit, it is by adding inputs:
extra matter with one fitted mass for unification, and two corner strengths per sector for the
masses. **None of the 19 parameters is derived.** The tally in [WHY.md](WHY.md) is unchanged.

## How to read the labels

| Label | Meaning |
|---|---|
| CHECK | Exact or numerical mathematics, verified in the script. |
| MODEL | This repository's construction on published ingredients. |
| FAILS | A prediction of the construction that the measurements exclude. |
| FIT | Inputs chosen to match measurements. It shows a fit exists; it predicts nothing by itself. |
| EMPIRICAL | A numerical regularity with no derivation here. |

## The geometry

The torus with complex structure τ = e^{2πi/3}, divided by a rotation of 120°. This is two
equilateral triangles glued along their edges, with three corners where the rotation has a
fixed point. The rotation is a symmetry of the torus only for this τ, so the shape is fixed.
What remains free is discrete: the gauge twist and the integer magnetic flux.

## Gauge sector

### G1. The twist leaves 3-3-1 (CHECK)

A rotation by 120° can act on the SU(6) gauge field as P = diag(1, 1, 1, ω, ω, ω). The
generators that commute with P number 17 = 8 + 8 + 1: SU(3) × SU(3) × U(1). Of the four
Z₃ twists of SU(6), this is the only one that leaves that group.

Every left-handed fermion of this repository's β = −1/√3 model
([`src/m331_standalone.py`](src/m331_standalone.py)) is a piece of an SU(6) representation:

| Fermion | (colour, SU(3)_L, X) | SU(6) representation |
|---|---|---|
| lepton triplets | (1, 3, −1/3) | 6̄ |
| charged lepton singlets | (1, 1, 1) | 20 |
| third quark family | (3, 3, 1/3) | 20 |
| first two quark families | (3, 3, 0) | 15 |
| u-type singlets | (3, 1, −2/3) | 15 |
| d-type singlets | (3, 1, 1/3) | 6̄ |

The family that anomaly cancellation forces to differ sits in a different representation
from the other two. That 3-3-1 fits in SU(6) is known [1]; the check against this
repository's charges is done here in exact fractions.

### G2. The couplings where SU(6) is restored (CHECK)

The embedding fixes g₃ = g_L and g_X² = (3/4) g². With the 3-3-1 matching
1/g_Y² = β²/g² + 1/g_X² this is **sin²θ_W = 3/8** at the orbifold scale, the same value as
in SU(5).

### G3. Minimal content fails (FAILS)

The two electroweak couplings fix the scale M_c where they meet; the strong coupling is then
a prediction. Boundary values and coefficients are those of `src/m331_standalone.py`
(a_X = 26/3, b_L = 13/2, as in [NOTE_331.md](NOTE_331.md)).

| Content, μ₃₃₁ | M_c | α_s(M_Z) predicted |
|---|---|---|
| minimal, 4 TeV, one loop | 1.5×10¹⁰ GeV | 0.0326 |
| minimal, 4 TeV, two loops | 1.4×10¹⁰ GeV | 0.0325 |
| plus the orbifold's own scalar, two loops | 7.6×10⁹ GeV | 0.0326 |
| minimal, 10⁵ GeV, two loops | 3.7×10¹⁰ GeV | 0.0354 |
| minimal, 10¹¹ GeV, two loops | 2.5×10¹² GeV | 0.0581 |
| measured | | 0.1180 |

"The orbifold's own scalar" is the (3, 3̄) part of the gauge field along the extra
dimensions, the one scalar the geometry supplies without a choice. It does not help. Raising
the 3-3-1 scale does not help either.

### G4. What would fit (FIT)

Extra multiplets at μ₃₃₁, taken from the 3-3-1 pieces of the SU(6) representations 6, 15,
20, 21 and 35: 22 candidates, up to four at once. Required: the three couplings meet, and the
unified scale is high enough for the proton (τ(p → e⁺π⁰) > 2.4×10³⁴ yr [4], with the
lifetime estimated as M_c⁴/(α_U² m_p⁵), good to an order of magnitude).

- Five sets pass a one-loop screen. Four survive at two loops. **None lands within 0.003 of
  the measured α_s(M_Z) at two loops with every mass at μ₃₃₁.**
- The smallest set that brackets the measurement is three SU(3)_L-octet fermions and one
  real colour-octet scalar: α_s(M_Z) = 0.109 at one loop and 0.133 at two.
- Freeing one mass, the common mass M₈ of the three octet fermions, and fixing it by
  α_s(M_Z): **M₈ = 7.1 TeV, M_c = 1.1×10¹⁶ GeV, 1/α_U = 32.7, proton lifetime about
  5×10³⁵ yr.**

This is one input fitted to one number, so it is not a prediction of α_s. What it does
predict, if taken seriously, is new SU(3)_L-octet fermions near 7 TeV and a proton lifetime
about 20 times the current limit, with an order-of-magnitude error. Two-loop gauge terms
only; Yukawa terms and threshold corrections at M_c are not included, and the one-to-two-loop
shift (0.109 to 0.133) shows how large such corrections are here.

## Flavour sector

Charged fermions in M units of magnetic flux on a torus have M zero modes, and a Yukawa
coupling is the overlap integral of three of them [2]. On the orbifold the modes are sorted
by their Z₃ eigenvalue [3]. All integrals are done numerically in the script; the rotation,
the reflection and the corner translation act as unitary matrices to 10⁻¹⁴.

### T1. Three generations (CHECK)

| Flux | Modes with Z₃ eigenvalue 1, ω, ω² |
|---|---|
| 2 | 1, 0, 1 |
| 4 | 1, 2, 1 |
| 6 | **3**, 2, 1 |
| 8 | 3, 2, 3 |
| 10 | 3, 4, 3 |
| 12 | 5, 4, 3 |

Flux 6 has exactly three invariant modes. Under the translation that carries one corner to
the next they have charges 0, 1, 2: they are permuted exactly like the three corners. The
Higgs that couples two flux-6 fermions has flux 12 and five invariant modes, with charges
0, 1, 1, 2, 2. Only even flux is used; odd flux needs extra boundary phases.

### T2. The fully symmetric Higgs (FAILS)

One Higgs direction keeps every symmetry of the triangle, and it is unique. It gives masses
1 : 0.7937 : 0.7937 (the ratio is 2^(−1/3)). Measured, from the Yukawa couplings at M_Z used
in WHY.md: up-type 1 : 3.7×10⁻³ : 7.3×10⁻⁶, down-type 1 : 1.9×10⁻² : 9.5×10⁻⁴.

### T3. A Higgs at a point gives one massive generation (CHECK)

If the Higgs is concentrated at a point p of the triangle, the Yukawa matrix is
Y_ab = L_a(p) R_b(p). It has rank one: exactly one massive generation. Verified at generic
points to 10⁻¹⁴. A Higgs made of lumps at the three corners gives three masses in the ratio
of the lump weights.

### T4. The Higgs potential does not put it there (FAILS)

- **Local quartic alone.** The direction that minimises ∫|Φ|⁴ at fixed norm is the
  triangular vortex lattice: the minimum is 1.1596, equal to the value for one flux quantum
  per cell computed separately on the same lattice. It gives masses 1 : 1 : 0, the wrong
  pattern. The corner-concentrated Higgs has the value 6.0000: it is the maximum.
- **Fermion loops.** They lower the quartic in proportion to Σm⁴, which favours one heavy
  generation. Scanning their strength up to the point where the corner state itself would
  become unstable, the vacuum stays spread out (masses 1 : 0.89 : 0.54 at 90% of that
  strength) and the potential becomes unbounded below before the Higgs concentrates.

### T5. A light Higgs from unequal corners (MODEL, with a FIT; the mixing FAILS)

If the Higgs is far lighter than the compactification scale, the quartic is irrelevant to
its direction: the light Higgs is the lowest state of the Higgs mass matrix, and the other
four modes stay at the compactification scale. That agrees with one Standard-Model-like
Higgs and nothing else nearby.

Suppose mass terms of strengths k₁ > k₂ > k₃ sit at the corners; orbifold fixed points
generically carry such terms. The light Higgs then sits on the strongest corner and leaks
onto the others by an amount set by one geometric number, the overlap of two Higgs corner
states, **g = 0.00212**:

| Corner strengths | Masses |
|---|---|
| 1, 1, 1 | 1 : 0.79 : 0.79 |
| 1, 0.9, 0.5 | 1 : 1.9×10⁻² : 2.1×10⁻³ |
| 1, 0.5, 0.25 | 1 : 2.1×10⁻³ : 7.0×10⁻⁴ |

So strengths that differ by factors of order one give hierarchies of 10⁻² to 10⁻³. Fitted
to the four measured ratios, the strengths are (1, 0.636, 0.0035) for the up-type Higgs and
(1, 0.899, 0.307) for the down-type. The down sector needs nothing unusual; the up quark
needs one corner almost switched off.

With the masses fitted, the mixing matrix is a prediction, set by the overlap 0.0797 of the
fermion corner states:

| | Predicted | Measured |
|---|---|---|
| \|V_us\| | 0.0038 | 0.22501 |
| \|V_cb\| | 0.0012 | 0.04183 |
| \|V_tb\| | 1.00000 | 0.999118 |

The matrix is close to the identity, as measured, but the angles are 30 to 60 times too
small, and there is no CP violation. The up-type and down-type Higgs are treated as
independent directions here; the row structure of the 3-3-1 Yukawa terms (WHY.md, W9) is not
imposed.

### T6. The triangle form of a spectrum (EMPIRICAL)

A mass matrix unchanged by rotating the triangle is circulant, and its eigenvalues have the
form √m_k = a(1 + r cos(θ + 2πk/3)). Any three masses fit this with some (a, r, θ); the
content is in the values.

| | r/√2 | θ |
|---|---|---|
| charged leptons (pole masses) | 1.00000 | 0.22222 |
| up quarks (Yukawas at M_Z) | 1.2895 | 0.0518 |
| down quarks (Yukawas at M_Z) | 1.1151 | 0.1001 |

r = √2 is Koide's relation (WHY.md, W8; history in [5]). For the leptons θ equals 2/9 to
five digits. Neither is derived here, the quarks follow no simple value, and WHY.md records
that the lepton relation holds for pole masses and not for running masses.

## What this adds to the ledger

| Parameter | What the triangle gives |
|---|---|
| gauge group and charges | 3-3-1 and all its fermion charges, from one twist (G1). Not one of the 19. |
| number of generations | Three, at flux 6 (T1). Not one of the 19; the flux is a discrete choice. |
| sin²θ_W, α_s | 3/8 at the orbifold scale; fails with minimal content, fits with extra matter and one fitted mass (G3, G4). |
| quark masses | One heavy generation for a Higgs at a corner; the hierarchy needs two inputs per sector (T3, T5). |
| mixing angles | Close to the identity; sizes wrong by 30 to 60 (T5). |
| CP phase, θ̄, v, λ, lepton masses | Not addressed, apart from the empirical T6. |

## What would turn this into a prediction

The corner strengths are inputs. They would become outputs if a discrete Wilson line made
the three corners inequivalent and the loop-generated corner terms were computed; that is one
discrete choice for all four strength ratios. It has not been done, and it could fail. The
mixing would still need a reason for the up-type and down-type Higgs to sit differently.

## Sources

1. F. F. Deppisch, C. Hati, S. Patra, U. Sarkar and J. W. F. Valle, "331 Models and Grand
   Unification: From Minimal SU(5) to Minimal SU(6)",
   [arXiv:1608.05334](https://arxiv.org/abs/1608.05334).
2. D. Cremades, L. E. Ibáñez and F. Marchesano, "Computing Yukawa Couplings from Magnetized
   Extra Dimensions", JHEP 05 (2004) 079,
   [arXiv:hep-th/0404229](https://arxiv.org/abs/hep-th/0404229).
3. H. Abe, T. Kobayashi and H. Ohki, "Magnetized orbifold models", JHEP 09 (2008) 043,
   [arXiv:0806.4748](https://arxiv.org/abs/0806.4748).
4. Super-Kamiokande Collaboration (A. Takenaka et al.), "Search for proton decay via
   p → e⁺π⁰ and p → μ⁺π⁰ with an enlarged fiducial volume in Super-Kamiokande I-IV",
   Phys. Rev. D 102, 112011 (2020), [arXiv:2010.16098](https://arxiv.org/abs/2010.16098).
5. A. Rivero and A. Gsponer, "The strange formula of Dr. Koide",
   [arXiv:hep-ph/0505220](https://arxiv.org/abs/hep-ph/0505220).

Titles, authors and the proton-lifetime limit were read from the arXiv records on
2026-11-15. The formulas of [2] and [3] were not copied: the zero-mode wavefunction is the
one quoted in the script, and every overlap, mode count and symmetry property is recomputed
there.
