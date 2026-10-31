# Refinement round 3

Date: 2026-10-31. Script: [`src/checks/r3_nucleation.py`](../src/checks/r3_nucleation.py) (runs in under 1 s).
Labels in square brackets refer to [`REFERENCES.md`](REFERENCES.md).

| # | Item (from the R2 list) | Outcome |
|---|---|---|
| R3.1 | Planck reionization-tomography bound | **Partly done.** The result is null [N4.4], but its numerical value could not be retrieved (full text blocked). STUR-ROLL's maximum is computed below; nothing is excluded. |
| R3.2 | The Z&#8326; global-structure caveat | **Resolved, by a commitment.** STUR-ROLL adopts the minimal [SU(3)&times;SU(2)&times;U(1)]/Z&#8326; group. Then k &isin; &Zopf; follows from [N2.1], and the model predicts no colour-singlet fractionally charged states. |
| R3.3 | The nucleation phase | **Done.** There is a window for H_nuc for every allowed f. A tensor-mode consequence follows, and a sharp corner opens if the phase is R&sup2; inflation. |
| R3.4 | Full-text verification of † references | **Blocked.** arxiv.org and journals.aps.org are still refused by the session's network policy. One more abstract was confirmed ([N4.4] is published as PRD 111, 023501). |
| R3.5 | The missing companion scripts | **Blocked.** These need the author's files. |

## R3.1 Reionization-era anisotropy against Planck PR4

Namikawa [N4.4] (*Phys. Rev. D* **111**, 023501, 2025) constrains anisotropic
birefringence generated at reionization using Planck PR4. The abstract
reports a power spectrum "consistent with null"; the numerical bound is in
the full text, which could not be reached.

STUR-ROLL's reionization-era signal is bounded from above by its own
structure. The largest possible rotation difference across the sky is &alpha;, so
D_L &le; (&alpha;/2)&sup2; &asymp; 1.3&times;10&#8315;&#8309; rad&sup2;. In the random-domain models of R2.4 it is at
most about 4.5&times;10&#8315;&#8310; rad&sup2;, concentrated at &ell; &lesssim; 10. The models with a large
signal need opposite-sign domains inside the last-scattering volume. Those
are rare: R2.1 puts the probability of a wall in our Hubble volume at 0.1&ndash;0.2.

**Status:** this remains consistent with the abstract-level result. A
quantitative comparison needs the PR4 bandpowers.

## R3.2 The Z&#8326; caveat: resolved by adopting the minimal gauge group

Reece [N2.1] shows that with the minimal Standard Model gauge group
[SU(3)&times;SU(2)&times;U(1)]/Z&#8326;, an axion's photon Chern&ndash;Simons coupling has a
fractional part that is a multiple of 1/3, **determined by its gluon
coupling** (abstract). The &theta; of STUR-ROLL has no gluon coupling, because &psi;
is colourless and the SM is B-neutral, so the fractional part vanishes and
**k_eff &isin; &Zopf;**. This agrees with R2.2's orbifold result
k_eff = &kappa; + &frac12; sgn M, and the half-integer bare level is consistent with it.

**What this commits STUR-ROLL to:** the Z&#8326; quotient is equivalent to the
statement that every colour-singlet state has an integer electric charge. So
the UV completion must contain **no fractionally charged colourless
particles**, which is consistent with all searches so far. Without the
quotient, fractional photon couplings become possible (R2.2 estimated a 1/9
ladder; this has not been verified) and the integer prediction is lost.

## R3.3 The nucleation phase

**Constraints on H_nuc** (all inputs from earlier rounds):

- **Lower bound.** H_nuc &gt; H_c = 15.06/L, so that &theta; starts at its minimum
  [R2.2]. With 1/L &ge; 0.88 TeV [R2.3], H_nuc &gt; 1.3&times;10&#8308; GeV.
- **Upper bound.** H_nuc &lt; 2&pi;f(0.03&pi;)/&radic;N, which keeps &beta; within 3% of &alpha;/2
  after N e-folds of random walk [R2.4].
- **Tensor modes.** r &lt; 0.036 (BICEP/Keck) gives H &lt; 4.7&times;10&sup1;&sup3; GeV. This never
  binds before the seed condition does.

| f [GeV] | N | H_nuc range [GeV] | maximum r |
|---|---|---|---|
| 2.9&times;10&#8313; | 60 | 1.3&times;10&#8308; &ndash; 2.2&times;10&#8312; | 8&times;10&#8315;&sup1;&sup3; |
| 10&sup1;&sup2; | 60 | 1.3&times;10&#8308; &ndash; 7.6&times;10&sup1;&#8304; | 10&#8315;&#8311; |
| 10&sup1;&#8308; | 60 | 1.3&times;10&#8308; &ndash; 7.6&times;10&sup1;&sup2; | 10&#8315;&sup3; |
| 3.5&times;10&sup1;&#8308; | 60 | 1.3&times;10&#8308; &ndash; 2.7&times;10&sup1;&sup3; | 1.2&times;10&#8315;&sup2; |
| any allowed f | 10&#8310; | the window stays open | &mdash; |

**Consequence 1: an inflation-scale prediction.** STUR-ROLL requires
**r &lesssim; 10&#8315;&sup3; unless f &gtrsim; 10&sup1;&#8308; GeV**. If LiteBIRD detects r &gtrsim; 2&times;10&#8315;&sup3;, f is
forced into the top decade of its window. This links the two LiteBIRD
observables, r and &beta;.

**Consequence 2: the R&sup2; corner.** The archived GENESIS pipeline used R&sup2;
(Starobinsky) inflation. If that is the nucleation phase (r &asymp; 0.003&ndash;0.0035,
H &asymp; 1.4&times;10&sup1;&sup3; GeV at the pivot scale):

- f &gt; 1.8&ndash;1.9&times;10&sup1;&#8308; GeV for N = 60 (rising as &radic;N), which reproduces R2.4's
  conditional bound independently;
- the domain-wall bound f &le; &radic;(10&sup1;&#8312; eV&sup3;/8m) then gives **m &lesssim; 3&ndash;4&times;10&#8315;&sup3;&#8304; eV**;
- combined with the &alpha;/2 window from R2.1 (m &gtrsim; 2&times;10&#8315;&sup3;&sup1; eV), this confines the
  sector to **2&times;10&#8315;&sup3;&sup1; &lesssim; m &lesssim; 3&times;10&#8315;&sup3;&#8304; eV and f &asymp; 2&ndash;8&times;10&sup1;&#8308; GeV**.

The prediction set in this corner is r &asymp; 0.003,
&Delta;&beta; &isin; [&minus;0.21&deg;, &minus;0.15&deg;] and |&beta;| = &alpha;/2. **All three are LiteBIRD observables.**

**Caveat.** H during R&sup2; inflation is larger before the pivot scale exits
the horizon. Using the pivot value underestimates the early random walk, so
these bounds on f are lower limits. A longer pre-pivot phase tightens them,
and N &gtrsim; 1000 at the pivot value of H would close the corner.

## Open after round 3

1. **Get the full texts** of [N4.4] (the PR4 bandpowers) and the † items. This
   needs arxiv.org allowed in the environment's network settings.
2. **Get the companion scripts** (`class_check.py` and the others) from the author.
3. **Decide whether the nucleation phase is R&sup2; inflation.** If it is, compute
   the exact &int;H(N)&sup2;dN random walk through Starobinsky inflation, not just the
   pivot value.
