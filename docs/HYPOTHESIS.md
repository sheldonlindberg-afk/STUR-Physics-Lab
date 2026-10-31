# STUR-ROLL: the hypothesis

Sheldon Lindberg, 2026. This is the current statement after refinement rounds
1&ndash;7. Each claim links to the round that established it; references are in
[`REFERENCES.md`](REFERENCES.md) and terms are defined in
[`GLOSSARY.md`](GLOSSARY.md). The original computation,
[`src/stur_final.py`](../src/stur_final.py), is kept exactly as uploaded; its
outdated statements are listed in [`STATUS.md`](STATUS.md).

> **In plain terms.** Light from the early universe is slightly polarized:
> its electric field prefers one direction. Recent measurements suggest that,
> on its 13.8-billion-year trip to us, that direction has been turned by about
> a fifth of a degree. STUR-ROLL says the turn is not a free number. It comes
> from a hidden field that, after the universe cooled, rolled exactly halfway
> around a circle. Half a turn of that field rotates light by exactly half the
> fine-structure constant, &alpha;/2 = 0.2091&deg;. Nothing is adjusted to get
> this number; it follows from whole numbers and symmetry.

## The claim

STUR-ROLL adds to Lambda-CDM one sector that predicts the isotropic CMB
birefringence angle:

    |beta| = k alpha / 2,   k = 1   ->   0.2091 deg   (computed 0.2080-0.2094 deg)

There is no continuous fitted parameter and no initial-condition coincidence.

- **Scope.** Gravity is general relativity, written in its teleparallel form
  (TEGR), so STUR-ROLL passes every GR precision test by construction. Dark
  matter and dark energy are those of Lambda-CDM (see "What STUR-ROLL does not
  explain").
- **Observable footprint.** The new sector carries &lesssim; 2&times;10&#8315;&#8309;
  of the matter energy (R2.1). It shows up only through &beta;, through a
  possible heavy partner of the photon at the edge of LHC reach (R2.3), and
  through a link to the primordial gravitational-wave ratio r (R3.3).
- **Relation to prior work.** The observable is the c_&gamma; = 1 case of the
  hilltop-axion birefringence of Lee, Murai, Takahashi & Yin [3]. STUR-ROLL's
  contribution is a **derivation of both of their assumptions** from a
  five-dimensional theory: c_&gamma; = 1, and the hilltop start.

## Axioms and inputs

| | Statement | Status |
|---|---|---|
| **A1 Smooth birth** | The universe nucleates through a smooth geometry in which the fifth dimension (S&sup1;/Z&#8322;) closes off. In the quotient this is a half-disc, and the two branes are the ends of one brane. | **axiom** (R5, R6) |
| **A2 Gauge structure** | A Z&#8322;-odd U(1)_B in the bulk with holonomy &theta; = &oint;B_y; bulk hypercharge; SM gauge group [SU(3)&times;SU(2)&times;U(1)]/Z&#8326;. | **choice** (R2.2, R2.3, R3.2) |
| **A3 Matter** | A charge-1 vectorlike bulk lepton pair &psi; with masses (M, &minus;M); a B-charged scalar &phi;; an orbifold-odd brane angle &vartheta; at y = 0. | **choice** (R2.2, R6) |
| **Discrete choices** | k = 1 (minimal level); V(&vartheta;) has its minimum at &pi;; &vartheta;-charges q_&psi; odd, q_&phi; even. | discrete, no tuning |
| **Gravity** | Quadratic Poincar&eacute; gauge theory with TEGR as its GR limit. Torsion plays **no role** in the mechanism (R5). | consistent |

> **In plain terms.** There is one assumption about how the universe began
> (A1), a few choices of which particles exist (A2, A3), and three
> yes-or-no switches. None of them is a dial that could be turned to fit the
> data.

The full Lagrangian, with the parity table, is in
[`REFINEMENT_R5.md`](REFINEMENT_R5.md) &sect;1; the brane term is in
[`REFINEMENT_R6.md`](REFINEMENT_R6.md) &sect;1.

## The derived chain

Each step has a technical statement and a plain-language reading.

**1. Birth fixes the starting values (A1).** For a smooth birth the holonomies
around the closing dimension are trivial: **&theta; = 0 and &vartheta; = 0
exactly**. Any other value costs Euclidean action ~&theta;&sup2;/g&#8324;&sup2;,
and across the allowed parameter space g&#8324; = 1/(fL) lies between about
10&#8315;&sup1;&sup2; and 5&times;10&#8315;&sup3; (R7 A4), so the cost is at least
~4&times;10&#8308;&theta;&sup2;.
*Plainly:* a universe that begins smoothly cannot begin with the hidden field
twisted; the untwisted start is enormously favoured.

**2. At birth that point is the minimum (positivity theorem, R5).** With the
boundary conditions a smooth birth imposes (bosons periodic, fermions
antiperiodic), Z(&theta;) = Tr[e^{&minus;LH}e^{i&theta;Q}] has positive weights,
so |Z(&theta;)| &le; Z(0) and E(&theta;) &ge; E(0) to all orders. Brane terms
that respect the orbifold parity cannot change this (20,000 random cases, 0
violations).
*Plainly:* at the start, the field sits at the bottom of a valley, and no
amount of quantum fluctuation can make that spot anything but a valley.

**3. The coupling to light is quantised (R1.1, R2.2, R3.2).** The 5D
Chern&ndash;Simons term gives L = (k&alpha;/4&pi;)&theta;FF&#771; with
k_eff = &kappa; + &frac12; sgn M &isin; &Zopf;. The bare level &kappa; &isin;
&Zopf; + &frac12; comes from the parity anomaly; the Z&#8326; structure and the
colourless &psi; make k an integer. The fermion tower gives
&Phi;(&pi;) &minus; &Phi;(0) = (&pi;/2) sgn M exactly, for every MR, so a roll
&Delta;&theta; = &pi; gives **&beta; = k&alpha;/2 exactly**.
*Plainly:* how strongly the hidden field turns light comes in whole-number
steps, like electric charge. The smallest non-zero step gives &alpha;/2 for
half a turn.

**4. The brane twists (R6).** &vartheta; = 0 is a maximum of V(&vartheta;). The
orbifold parity (&vartheta; &rarr; &minus;&vartheta;) fixes the stationary
points at exactly 0 and &pi;, so &vartheta; rolls to **exactly &pi;**. For
m_&vartheta; &gtrsim; 2H_nuc this takes 4&ndash;26 e-folds and happens
coherently, giving no walls and no isocurvature. With q_&psi; odd and q_&phi;
even, &vartheta; = &pi; is a **fermion-parity defect**: &psi; becomes
effectively periodic.
*Plainly:* a switch on the boundary of the extra dimension flips, and symmetry
forces it to land exactly at "fully flipped". That flip changes how the
fermions feel the extra dimension.

**5. Inflation (R2.4, R3.3).** &theta;'s potential is about 10&#8315;&#8312;&#8311;
of H&sup2;, so &theta; random-walks to |&theta;_i| &asymp; s&#8320;&radic;N, with
s&#8320; = H_nuc/2&pi;f. Keeping &beta; within 3% (1%) of &alpha;/2 needs
s&#8320;&radic;N &lesssim; 0.094 (0.031), i.e. H_nuc &lesssim; 0.076 f for N = 60.
*Plainly:* during inflation the field jiggles a little. As long as inflation
was not too violent, it stays close enough to its starting point.

**6. The late-time hilltop (stur_final step 4).** With &psi; periodic and
fermion-dominated, the one-loop Wilson-line potential is
V = m&sup2;f&sup2;(1 + cos &theta;), so &theta; = 0 is now a hilltop. The mass
obeys m&sup2;f&sup2; ~ e^(&minus;M_fL)/L&#8308;; its magnitude is an input.
*Plainly:* because of the flip in step 4, the old valley floor is now a
hilltop, and the field is still sitting on it.

**7. The roll (stur_final step 5, R2.1).** &theta; rolls from &theta;_i to
&plusmn;&pi; at z &asymp; 4&ndash;300, after the CMB was emitted, giving
**&beta;_rec = 0.2081&ndash;0.2094&deg;** for s&#8320; = 10&#8315;&#8308;&ndash;10&#8315;&sup3;
(R6 &sect;4).
*Plainly:* somewhere between about 3 million and 1.5 billion years after the
Big Bang (the CMB was released at 380,000 years), the field rolls off the
hilltop and settles half a turn away. Light that left
before the roll arrives rotated by &alpha;/2.

**The sign of &beta; (corrected in R7 A1).** V(&theta;) is even, so the hilltop
is symmetric: each region rolls toward the sign of its own &theta;_i, and the
brane twist does not choose the direction. Because &theta; &asymp; 0 at every
recombination emission point, &beta;_rec = (&alpha;/2&pi;)(&theta;_obs &minus;
&theta;_emit) takes **one sign over our whole sky**, set by &theta; in our own
region. Distant regions can carry the opposite sign; that is the origin of the
patchy reionization signal (R2.4).

> **Superseded parts of the original chain.** `stur_final.py` derived
> &theta; = 0 at nucleation from the scalar dominating the de Sitter potential.
> That cannot hold &theta;, whose curvature is about 10&#8315;&#8312;&#8311; of H&sup2;.
> Steps 1&ndash;2 replace it. `stur_final.py` also assumed periodic fermions;
> step 4 now derives this.

## Constraints and consistency

| Quantity | Allowed range | Source |
|---|---|---|
| &theta; mass m | 2&times;10&#8315;&sup3;&sup1; &lesssim; m &lesssim; 10&#8315;&sup2;&#8312; eV (for &alpha;/2 within 3%) | R2.1 |
| decay constant f | 2.9&times;10&#8313; GeV (Chandra) to &radic;(10&sup1;&#8312; eV&sup3;/8m) (domain walls) | section C, R1.2 |
| 1/L | 0.8&ndash;1.0 TeV &lesssim; 1/L &lt; f/197 (KK hypercharge M&#8321; = 2&pi;/L &gt; 5.1&ndash;5.5 TeV; nucleation window) | R2.3, R7 A3 |
| &psi; mass | M_f &gtrsim; 1.2&times;10&#8309; GeV (beyond colliders) | R2.3, R7 A5 |
| H_nuc | 15/L &lt; H_nuc &lt; 0.6 f/&radic;N | R3.3 |
| m_&vartheta; | &gtrsim; 2H_nuc &ge; 2.6&times;10&#8308; GeV | R6 |
| energy in &theta; | &lesssim; 2&times;10&#8315;&#8309; of matter (release at H &asymp; m/19.5) | R2.1 |
| weak gravity conjecture (U(1)_B) | satisfied for all allowed f | R1.5 |
| anisotropy | recombination: isotropic; reionization: patchy, rms &le; 0.2&deg;, within A_CB &lt; 0.15 | R2.4 |
| &beta; today | unobservably slow time dependence (period ~10&#8312; yr) | R2.4 |

## Predictions (all testable by LiteBIRD)

1. **|&beta;| = &alpha;/2 = 0.209&deg;** (computed 0.208&ndash;0.209&deg;).
2. **Tomography:** &Delta;&beta; = &beta;_reio &minus; &beta;_rec &isin;
   [&minus;0.209&deg;, &minus;0.146&deg;] if our reionization shell lies in one
   domain, widening to **[&minus;0.209&deg;, &minus;0.122&deg;]** for the
   expected opposite-domain fraction (&le; 0.085 at N_extra &ge; 60). That is
   2.4&ndash;4.2&sigma; from zero at LiteBIRD (R2.1, R7 A2). A miscalibration or
   a late (dark-energy-like) roll gives &Delta;&beta; &asymp; 0.
3. **Bound on the low-to-high-&ell; difference:** |&beta;(low &ell;) &minus;
   &beta;(high &ell;)| &le; &alpha;/2. This is calibration-free.
4. **No anisotropic birefringence at recombination** (R2.4).
5. **Tensor ratio:** r &lesssim; 10&#8315;&sup3; unless f &gtrsim; 10&sup1;&#8308; GeV.
   If the nucleation phase is R&sup2; inflation: r &asymp; 0.003 with
   2&times;10&#8315;&sup3;&sup1; &lesssim; m &lesssim; 3&times;10&#8315;&sup3;&#8304; eV and
   f &asymp; 2&ndash;8&times;10&sup1;&#8308; GeV (R3.3).
6. **Colliders:** a KK hypercharge boson near 6 TeV, with 4&ndash;5&times; the
   SSM dilepton rate, appears only at the 1/L &asymp; 1 TeV edge (R2.3).
7. **No fractionally charged colour-singlet particles** (from the Z&#8326;
   choice, R3.2).

What these would mean for physics if confirmed is in
[`IMPLICATIONS.md`](IMPLICATIONS.md).

## What STUR-ROLL does not explain

- **Dark matter.** The sector has no stable particle. B_&mu; is Z&#8322;-odd, so
  there is no 4D B charge. &psi; decays through brane mixing at y = 0 (R2.2),
  and &phi; through the analogous brane couplings. &vartheta; sits at its
  minimum after inflation. &theta; contributes &lesssim; 2&times;10&#8315;&#8309;.
  **Dark matter is the Lambda-CDM component.**
- **Dark energy.** No field in the sector can play the role: a field that light
  could not trigger the roll (R4 &sect;C), and torsion gives no twist (R5).
  **Dark energy is the cosmological constant.**

## Caveat

The &beta; measurements rely on calibrating the polarization angle against
Galactic foregrounds. The ACT+Planck and ACT DR6 authors call the signal a
hint, and a systematic would remove the test. Tomography (prediction 2) is
the calibration-independent check.
