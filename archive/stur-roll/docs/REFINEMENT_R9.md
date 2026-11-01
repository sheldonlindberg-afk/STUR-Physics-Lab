# Refinement round 9: can STUR-ROLL calculate the Cabibbo angle?

Date: 2026-10-31. Preregistration: [`R9_PREREGISTRATION.md`](R9_PREREGISTRATION.md)
(committed before any calculation). Script:
[`src/checks/r9_cabibbo.py`](../src/checks/r9_cabibbo.py); captured output:
[`results/r9_cabibbo_output.txt`](../results/r9_cabibbo_output.txt).

> **In plain terms.** No. STUR-ROLL's symmetries cannot tell the three quark
> generations apart, so they cannot fix how much the generations mix. Letting
> the quarks spread into the extra dimension gives a mixing angle that
> *can* land on the measured value, but it lands anywhere between about 0.15
> and 0.6, so hitting 0.225 is not a prediction. The one version narrow enough
> to test also gets the other two mixing angles wrong. Like the old archive
> claim, any "derivation" of the Cabibbo angle here would need a knob set to
> the answer.

## Bottom line

| Module | Verdict | Why |
|---|---|---|
| **9A** angle fixed by a discrete symmetry | **no-go** | Bulk quarks must carry even brane-angle charge to keep chiral zero modes, so every symmetry STUR-ROLL has acts identically on all three generations. Brane-localised quarks can differ, but abelian Z&#8322; charges only ever leave \|V_us\| continuous (104 of 1024 assignments) or pin it to 0 (8); none fixes a value in between. |
| **9B** angle from wavefunction overlaps | **consistent, not predictive** | With anarchic O(1) 5D Yukawas and profiles solved to reproduce the six quark masses, \|V_us\| has median 0.31 and 68% range 0.15&ndash;0.62. The observed 0.2250 sits at the 32nd percentile, but the band's half-width is 75% of the median (a sharp pass needed &le; 30%). |

**STUR-ROLL does not predict quark mixing.**

## Module 9A in detail

- **Bulk quarks.** A chiral zero mode needs the same orbifold parity at both
  branes. The brane angle at &vartheta; = &pi; multiplies the parity at y = 0 by
  (&minus;1)^q, so an odd-q quark loses its zero mode (its lightest state moves
  to the KK scale). Chiral quarks therefore have q even, and &vartheta; acts as +1
  on all of them. The orbifold parity is fixed by chirality and the Z&#8326;
  centre is part of the gauge group; both are the same for every generation.
  All nine Yukawa entries are allowed in each sector, and nothing fixes an
  angle.
- **Brane-localised quarks.** These escape the zero-mode condition, so
  (&minus;1)^q can differ between generations. Of the 2&#185;&#8304; = 1024 assignments of
  q &isin; {0, 1} to Q_i, u_i, d_i and the Higgs, 912 leave some quark massless,
  104 leave \|V_us\| continuously variable, and 8 pin it to exactly 0. This
  is the general rule for abelian charges: they make texture zeros, never
  a specific non-trivial angle.

## Module 9B in detail

Quarks in the bulk with kink masses have zero-mode profiles e^(&minus;cy); the
brane Yukawa is Y_ij = y_ij F_Qi F_qj. Under D-9B3 (F_Qi = F_di) the masses fix
the profiles, and the leading estimate is \|V_us\| &asymp; F_Q1/F_Q2 &asymp;
&radic;(m_d/m_s) = 0.224, the Gatto&ndash;Sartori&ndash;Tonin relation. The O(1)
anarchic couplings then spread it:

| | median | 68% | 95% | observed | percentile |
|---|---|---|---|---|---|
| \|V_us\| | 0.31 | 0.15&ndash;0.62 | 0.06&ndash;0.90 | 0.2250 | 32nd |
| \|V_cb\| | 0.16 | 0.07&ndash;0.35 | 0.03&ndash;0.65 | 0.041 | 5.5th |
| \|V_ub\| | 0.044 | 0.018&ndash;0.096 | 0.0065&ndash;0.18 | 0.0037 | **0.8th** |

19,265 of 20,000 samples converged; the 735 that did not were excluded.

**The secondary angles (reported, not used for the verdict, as
preregistered).** The symmetric profiles that make \|V_us\| testable also
predict \|V_cb\| ~ &radic;(m_s/m_b) and \|V_ub\| ~ &radic;(m_d/m_b), both too large.
The observed \|V_ub\| lies below the model's 95% band. So the only version of
9B narrow enough to test is itself disfavoured by the third mixing angle.

**Without D-9B3** the ratio F_Q1/F_Q2 is not fixed by the masses, and
\|V_us\| simply tracks it (median 0.022, 0.074, 0.215 for F_Q1/F_Q2 = 0.015,
0.05, 0.15). That version can fit any Cabibbo angle and predicts none.

## What this means

- STUR-ROLL's predictive power comes from one place: a whole-number coupling
  and a half-turn roll, acting on a field that does not touch the quarks. It
  has nothing comparable for flavour.
- Generic extra-dimensional flavour reproduces the *pattern* of quark
  mixing (small angles, a hierarchy) but not the *value* of the Cabibbo
  angle. That is a known feature of the approach, confirmed here for
  STUR-ROLL's geometry.
- A future flavour module would need a genuinely new ingredient, such as a
  non-abelian flavour symmetry that could fix angles. That is outside
  STUR-ROLL and would be a separate hypothesis, preregistered on its own.
