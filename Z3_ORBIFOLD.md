# The Z3 orbifold engine against the 19 parameters

*A first attempt at explaining the Standard Model's free parameters from one geometry, run
as proposed and checked number by number. It is an attempt and an explanation, not a claim.
Companion to [WHY.md](WHY.md), which sorts the same 19 parameters by what is known.
Independent work, not peer reviewed.*

Run it: `python3 src/z3_orbifold_audit.py` (about 3 s; output in
[results/z3_orbifold/output.txt](results/z3_orbifold/output.txt)). The engine itself is
[`src/z3_orbifold_engine.py`](src/z3_orbifold_engine.py), kept exactly as proposed. Pinned by
[`tests/test_z3_orbifold.py`](tests/test_z3_orbifold.py).

---

## The result in one paragraph

The numbers do not align yet. The engine speaks about 7 of the 19 parameters: four quark
mass ratios and three mixing angles. All seven miss the measured values by 2 to 5 orders of
magnitude. The quark mixing it prints (0.0029 and 0.0068) is a rounding error in its own
matrix routine; the true values are near 0.00001. It forces an eighth parameter, the
CP-violating phase, to zero, against a measured 1.147 rad. Two parameters are typed in, and
nine are not addressed. Two things hold up. The mechanism is sound: changing one hand-set
number from 1.8 to 0.50 brings every output within about one order of magnitude. And the
three-colour selection agrees with this repository's exact calculation. The geometry does
not yet do the explaining, because the outputs follow from six hand-chosen numbers, not
from the stabilised radius.

## What the engine does

1. **A radius.** A potential V(R) = −a/R⁴ + 0.42/R⁶ + 0.18 R², with a Casimir-type
   coefficient a, has a minimum at R\*.
2. **Three bulk masses per sector.** M_i = √V″(R\*) × (2, 4/3, 2/3) × 1.8/R\* × tilt, with
   tilt 1.05 for up-type and 0.92 for down-type quarks.
3. **Yukawa matrices.** Each generation sits at one of three fixed points with profile
   exp(−M R d). The Higgs sits at the third fixed point with profile exp(−8 R d). Overlaps
   give the matrices; off-diagonal entries are multiplied by |cos| of a phase difference.
4. **Three colours.** A two-loop running of the 3-3-1 couplings from 4 TeV excludes 5 and 7
   colours by a pole below the Planck mass.

## The ledger

| Label | Meaning |
|---|---|
| OUTPUT | The engine gives a number that can be compared. |
| FIXED | The engine's construction forces a value. |
| INPUT | The engine uses the measured value. |
| SILENT | The engine says nothing. |

| Parameter | Label | What the engine says |
|---|---|---|
| α_s | SILENT | Section 4 counts colours. It does not give the coupling. |
| α_QED | INPUT | 1/125.7 at 4 TeV is typed into section 4. |
| α_W (sin²θ_W) | INPUT | 0.2504 at 4 TeV is typed into section 4. |
| v | SILENT | R\* is a pure number. No unit of mass enters. |
| λ (Higgs mass) | SILENT | The Higgs is a fixed profile with no potential. |
| m_t, m_b | SILENT | Each matrix is divided by its largest entry, so y_t = y_b = 1 by construction. |
| m_c, m_u, m_s, m_d | OUTPUT | As ratios to m_t and m_b. |
| m_τ, m_μ, m_e | SILENT | No lepton sector. |
| θ₁₂, θ₂₃, θ₁₃ | OUTPUT | From the two left rotations. |
| δ | FIXED | Both matrices are real, so there is no CP violation. |
| θ̄ | SILENT | The matrices are real by the \|cos\| rule. That is a choice, not a mechanism. |

Tally: 7 OUTPUT, 1 FIXED, 2 INPUT, 9 SILENT.

## Z4. The seven outputs against the measured values

Yukawa couplings at M_Z from eq. (2.4) of [1]; mixing angles and phase from eq. (12.28) of
[2]. The engine's values are computed with numpy's SVD (see Z3).

| Quantity | Engine | Measured | Miss (orders of magnitude) |
|---|---|---|---|
| y_c / y_t | 1.1×10⁻⁷ | 3.7×10⁻³ | −4.5 |
| y_u / y_t | 7.3×10⁻⁸ | 7.3×10⁻⁶ | −2.0 |
| y_s / y_b | 1.7×10⁻⁷ | 1.9×10⁻² | −5.1 |
| y_d / y_b | 8.7×10⁻⁸ | 9.4×10⁻⁴ | −4.0 |
| sin θ₁₂ | 1.1×10⁻⁵ | 0.225 | −4.3 |
| sin θ₂₃ | 1.3×10⁻⁵ | 0.042 | −3.5 |
| sin θ₁₃ | 1.7×10⁻⁷ | 0.0037 | −4.3 |
| δ | 0 | 1.147 rad | n/a |

The root-mean-square miss is 4.07 orders of magnitude. The pattern is also wrong, not only
the size: the two light generations come out nearly equal (y_c/y_u = 1.5 against a measured
506; y_s/y_d = 2.0 against 19.9). The reason is that the Higgs sits on the third
generation's fixed point, so the other two are both far from it and both strongly
suppressed.

## Z3. The printed mixing matrix is a numerical artefact

The engine gets its left rotation as U = Y V / s, with singular values s near 10⁻⁷ taken
from Y^T Y. Rounding errors of order 10⁻¹⁶ in Y^T Y become errors of order 10⁻³ in U. The
engine's U is not orthogonal: U^T U differs from the identity by 3.9×10⁻³. The entries
0.0029 and 0.0068 it prints are that error. An orthogonal matrix would have equal entries
in those two places, and numpy's SVD gives 1.07×10⁻⁵ for both. The singular values
themselves agree with numpy to 1 part in 10⁵, so the mass ratios the engine prints are
correct.

## Z1 and Z2. What the geometry supplies

- **The minimum is real.** The exact root of dV/dR is R\* = 1.04771 with V″ = 5.63145. The
  engine's grid of 2000 points gives 1.04730 and 5.65331, close enough.
- **V(R\*) = +0.138 is positive**, so the potential leaves a vacuum energy of order one in
  its own units.
- **The radius cancels.** The profiles are exp(−M R d) and M is proportional to 1/R\*, so
  the product M R\* does not depend on R\*. Rebuilding the engine's matrices from M R and
  8 R alone reproduces them to 3×10⁻²¹.
- **Two numbers reach the Yukawas:** √V″(R\*) = 2.378 and 8 R\* = 8.378. Each is multiplied
  by a hand-chosen constant (1.8 and 8.0), so the potential's contribution cannot be
  separated from the choice of those constants.
- **The twist factors are 2, 4/3, 2/3.** The docstring names the Z3 eigenvalues (0, 1, 2)/3,
  but the code does not use them.

The flavour chain holds 16 hand-chosen numbers (listed in the script's output, Z0). They
reach the seven outputs as six effective dials: scale × tilt for each sector, the Higgs
exponent, and three phase offsets.

## Z5. Sensitivity

Because the outputs are exponentials of the dials, small changes move them a long way. A
10% increase in the bulk-mass scale lowers sin θ₁₂ by 1.7 orders of magnitude. A 10%
increase in the Higgs exponent lowers each mass ratio by 0.6 to 0.7 orders of magnitude. A
prediction from this mechanism needs its exponents fixed to about 1%.

## Z6. Can the structure align at all?

**One dial.** Lowering the bulk-mass scale from 4.28 to 1.19 (the geometric factor from 1.8
to 0.50), with everything else as given, brings the root-mean-square miss from 4.07 to 0.69
orders of magnitude. The worst output is then y_u/y_t, 1.2 orders too large.

**Six dials.** A random search with local refinement over the six effective dials finds a
miss of 0.42 orders of magnitude, a factor 2.7 per output. The exponents M R are then
between 0.6 and 2.7, against 2.6 to 9.0 in the engine as given. This is a best-found value,
not a proven optimum.

So exponential localisation does produce hierarchies of the measured size from numbers of
order one. That is the known result of Arkani-Hamed and Schmaltz [3]. It is not yet an
explanation here, because six dials are tuned to seven outputs and the fit is still off by
a factor of about 3.

## Z7. The three-colour selection

| N_c | b_X engine / exact | b_L engine / exact | b_XX engine / exact | b_LL engine / exact |
|---|---|---|---|---|
| 3 | 9.33 / 8.67 | −6.50 / −6.50 | 10.7 / 14.2 | −32.0 / −15.0 |
| 5 | 20.00 / 19.33 | −0.50 / −0.50 | 23.0 / 24.5 | 124.0 / 99.0 |
| 7 | 35.11 / 34.44 | 8.17 / 8.17 | 40.4 / 37.7 | 349.3 / 263.7 |

"Exact" is [`src/m331_exact.py`](src/m331_exact.py), whose machinery reproduces the Standard
Model's known coefficients. The engine's one-loop SU(3)_L coefficient is exact. Its U(1)_X
coefficient is 2/3 too large at every N_c. Its two-loop terms are approximations (the
U(1)_X one is 1.15 times the one-loop coefficient). Its inputs at 4 TeV, 125.7 and 0.2504,
match this repository's one-loop running (125.7 and 0.2505).

The verdict does not depend on any of this:

| N_c | Engine | Engine, one loop only | Exact coefficients | `src/m331_exact.py` |
|---|---|---|---|---|
| 3 | survives | survives | survives | survives |
| 5 | 7.4×10¹⁴ GeV | 8.3×10¹⁴ GeV | 1.8×10¹⁵ GeV | 1.3×10¹⁵ GeV |
| 7 | 1.1×10¹⁰ GeV | 1.1×10¹⁰ GeV | 1.4×10¹⁰ GeV | 9.7×10⁹ GeV |

This part is a restatement of [NOTE_331.md](NOTE_331.md), not a new result, and it carries
that note's limits (the β = +1/√3 variant and the mass floors discussed there). Section 4
does not use R\*, V″ or the bulk masses. Nothing links the orbifold to the 3-3-1 running.

## What this means for the unification attempt

- **What worked.** The mechanism reaches the right orders of magnitude with exponents near
  1 (Z6). The colour selection is robust (Z7). The potential has a real minimum (Z1).
- **What failed.** Every output as given (Z4). The printed mixing matrix (Z3). CP
  violation, which is absent by construction.
- **What is missing before it can explain anything.**
  1. A derivation of the constants 1.8, 8.0, 1.05, 0.92 and the three phase offsets, or
     fewer of them than outputs.
  2. Complex phases, so that δ can be non-zero. The Z3 phases e^(2πik/3) are a natural
     candidate; the \|cos\| rule discards them.
  3. A Higgs position that does not coincide with one generation, so that the two light
     generations split.
  4. A scale. The potential has no unit, so v, the Higgs mass and every absolute mass are
     out of reach.
  5. A lepton sector, and a link between the geometry and the gauge couplings.
- **A stable SVD.** Any next version should decompose Y directly (one-sided Jacobi, or
  numpy), not Y^T Y.

## Limits

- The audit tests the engine's numbers. It does not test whether a Z3 orbifold with these
  ingredients exists as a consistent field theory; the potential and the bulk-mass formula
  are taken as given.
- The six-dial fit is a search from one random seed. Another seed gives a miss between
  about 0.35 and 0.42.
- The measured Yukawas are at M_Z. The engine names no scale; running to another scale
  changes the ratios by tens of percent, far less than the misses.
- The labels in the ledger are this repository's judgement.

## Sources

1. S. Antusch, K. Hinze and S. Saad, [arXiv:2510.01312](https://arxiv.org/abs/2510.01312), eq. (2.4), as used in [WHY.md](WHY.md).
2. PDG 2024, review "CKM quark-mixing matrix", eq. (12.28), [pdg.lbl.gov](https://pdg.lbl.gov/2024/reviews/rpp2024-rev-ckm-matrix.pdf). The values of sin θ₁₃ and δ were typed from memory of that review and not re-read for this audit.
3. N. Arkani-Hamed and M. Schmaltz, Phys. Rev. D 61, 033005 (2000), [arXiv:hep-ph/9903417](https://arxiv.org/abs/hep-ph/9903417). Cited for the mechanism; not re-read for this audit.
