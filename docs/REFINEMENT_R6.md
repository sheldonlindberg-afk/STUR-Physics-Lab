# Refinement round 6: the brane angle fixes the twist at exactly &pi;

Date: 2026-10-31. Script: [`src/checks/r6_brane_angle.py`](../src/checks/r6_brane_angle.py) (about 3 s).

**Outcome.** Round 5's brane field is replaced with an angle &vartheta;. That makes the twist
**exactly &pi; by symmetry**, removes the brane domain-wall and isocurvature
problems, and turns the late-time hilltop into a consequence of the
Lagrangian. **The initial-condition coincidence identified in the review is
removed.** What remains are two discrete choices, listed in section 5.

## 1. The term

On the y = 0 brane (where R2.2 allows &psi; couplings):

L&#8320; &sup; &frac12; f_&vartheta;&sup2; (&part;&vartheta;)&sup2; &minus; V(&vartheta;) &minus; &vartheta; (q_&psi; J^y_&psi; + q_&phi; J^y_&phi;),  with J^y = the y-component of each field's number current.

- **&vartheta; is an angle.** &vartheta; &rarr; &vartheta; + 2&pi; must be a symmetry, so q_&psi; and q_&phi; are integers. The
  term is a localized holonomy for &psi;-number and &phi;-number.
- **&vartheta; is odd under the orbifold parity.** The y-currents are odd, so &vartheta; &rarr; &minus;&vartheta;
  is required for invariance.

## 2. The key fact: the parity-symmetric points of an angle are 0 and &pi;

Since &minus;&pi; &equiv; &pi;, the reflection &vartheta; &rarr; &minus;&vartheta; leaves **two** values unchanged: 0 and &pi;.
Consequences:

- **Any parity-symmetric periodic potential is stationary at exactly 0 and &pi;.**
  Checked on 2000 random potentials: |V&prime;| &le; 2&times;10&#8315;&sup1;&#8309;. Quantum corrections respect
  the orbifold parity, so they cannot move these points. The &psi;-loop
  contribution is itself even, and tiny (&lesssim; 10&#8315;&sup1;&sup3; eV&#8308;).
- **When the brane settles at &pi;, the twist is &delta; = &pi; exactly, with no parameter
  to tune.** This happens in about a quarter of random potentials. In the
  rest the minimum is at 0, or at a symmetric pair &plusmn;v&#8320; that would break the
  parity.
- **&vartheta; = &pi; does not break the orbifold parity.** It is the other symmetric
  state, so there are no &plusmn;v brane domain walls, unlike round 5's &Sigma;.

## 3. What &vartheta; = &pi; does: a fermion-parity defect

At &vartheta; = &pi;, a field of charge q picks up (&minus;1)^q at the brane. Which charge
choices make &theta; = 0 a hilltop at late times (fermion-dominated)?

| q_&psi; | q_&phi; | &theta; = 0 at &vartheta; = &pi; |
|---|---|---|
| even | any | minimum |
| **odd** | **even** | **hilltop** |
| odd | odd | hilltop (but this also flips the scalar's twist) |

The choice is **q_&psi; odd, q_&phi; even** (minimal: q_&psi; = 1, q_&phi; = 0). Then &vartheta; = &pi; is a
**localized fermion-parity defect for &psi;**. It turns the antiperiodic spin
structure that a smooth birth imposes into the **periodic** one that the
original `stur_final.py` assumed.

So the late-time hilltop of `stur_final.py` is no longer an assumption that
conflicts with the birth. It is **the end state of a brane transition**.

## 4. The sequence, start to finish

1. **Birth (smooth, untwisted).** The positivity theorem (R5) requires
   &vartheta; = 0 and &theta; = 0. This is forced by the geometry, whatever V(&vartheta;) is.
2. **The brane twists.** &vartheta; = 0 is a maximum of V. For m_&vartheta; &gtrsim; 2H, &vartheta; rolls to &pi;
   within about 4&ndash;26 e-folds (for m_&vartheta; ~ H it takes 50&ndash;90). The direction of the
   roll is fixed while the universe is still about one Hubble patch. Any walls
   formed in the first few e-folds are inflated beyond our horizon if
   inflation lasts longer than about 60 + N_twist e-folds. Because &vartheta; is
   heavier than H, it has no super-horizon fluctuations and so produces no
   isocurvature. **Both problems that sank round 4's dark-matter branch are
   absent here.**
3. **&theta; during inflation.** &theta;'s potential is negligible, so it random-walks
   away from its exact birth value, reaching &theta;_i &asymp; s&#8320;&radic;N with s&#8320; = H/2&pi;f (R2.4).
4. **Late times.** With &psi; effectively periodic, &theta; = 0 is the hilltop. &theta; rolls
   to &pi; at z ~ 4&ndash;300 and rotates the CMB polarization by &beta;.

| s&#8320; = H/2&pi;f | &theta;_i (N = 60) | &beta;_rec | &beta; / (&alpha;/2) |
|---|---|---|---|
| 10&#8315;&#8308; | 7.7&times;10&#8315;&#8308; | 0.2094&deg; | 1.002 |
| 10&#8315;&sup3; | 7.7&times;10&#8315;&sup3; | 0.2081&deg; | 0.995 |
| 10&#8315;&sup2; | 7.7&times;10&#8315;&sup2; | 0.2043&deg; | 0.977 |

(m_&theta; = 10&#8315;&sup3;&#8304; eV.) **&beta; = &alpha;/2 to better than 1% for H_nuc &lesssim; 6&times;10&#8315;&sup3; f, and to 3%
for s&#8320; up to 10&#8315;&sup2;.**

## 5. What is left

**Two discrete choices remain. Neither is a continuous tuning.**
- The sign of V(&vartheta;): the minimum is at &pi;, not 0. This is a discrete choice, like k = 1.
- The charges: q_&psi; odd and q_&phi; even.

**Conditions:**
- **m_&vartheta; &gtrsim; 2H_nuc**, for a prompt and coherent twist;
- **total inflation &gtrsim; 60 + N_twist e-folds**;
- **H_nuc &lesssim; 0.08 f**, already required by R2.4/R3.3.

**Comparison with the review's concern.** "&beta; = &alpha;/2 holds only if &theta; starts
on the hilltop (about 3% likely)" is resolved. &theta; starts at its exact birth
value, and the hilltop is placed there by symmetry. Compared with Lee et al.
[3], STUR-ROLL now supplies UV origins for **both** of their assumptions: c_&gamma; = 1
(the level) and the hilltop start (birth plus brane twist).

**Still open:**
1. **The origin of &vartheta;.** It is a new brane degree of freedom. It may be the
   phase of a brane scalar, or a remnant of the orbifold's own twisted sector.
   Its scale (m_&vartheta; &gtrsim; 2H_nuc &ge; 2.6&times;10&#8308; GeV) makes it invisible at colliders,
   since it couples only to the bulk &psi; current.
2. **The smooth-birth assumption itself.** Everything here assumes the universe
   nucleates with a contractible fifth dimension, as you proposed. This is now
   a load-bearing premise and should be stated as an axiom.
3. **Dark matter and dark energy** are still not explained (R5).
