# Round 9 preregistration: can STUR-ROLL calculate the Cabibbo angle?

Committed **before** any round-9 calculation. Results go in
[`REFINEMENT_R9.md`](REFINEMENT_R9.md). The same ground rules as round 8
apply: the core is frozen, modules are conditional, no fitting to the
target, parameter accounting, and a no-go is a valid outcome.

> **In plain terms.** The Cabibbo angle measures how strongly quarks of
> neighbouring generations mix; its sine is 0.2250 &plusmn; 0.0007. STUR-ROLL was not
> built to explain it. We test the only two ways it could: a symmetry that
> fixes the angle exactly, or the shape of the extra dimension setting how
> much quark wavefunctions overlap. We write down now what would count as
> success. We expect neither to succeed; the point is to find out properly.

**Target.** |V_us| = 0.2250 &plusmn; 0.0007 (PDG 2024 &dagger;). Secondary, reported
but not used for the verdict: |V_cb| &asymp; 0.041, |V_ub| &asymp; 0.0037.

## Module 9A: an angle fixed by STUR-ROLL's discrete symmetries

**What is available.** STUR-ROLL's discrete structures are: the orbifold
parity of S&sup1;/Z&#8322;; the brane angle at &vartheta; = &pi;, which acts on a field of
&vartheta;-charge q as (&minus;1)^q (R6); and the Z&#8326; centre of the Standard Model
gauge group (R3.2). No other discrete symmetry may be added.

**Method.** Enumerate every assignment of these charges to three quark
generations that is consistent with chiral zero modes. For each, find the
allowed Yukawa textures. Test, with random O(1) couplings, whether |V_us| is
fixed by the symmetry (independent of the couplings) or varies continuously.

**Outcomes.**
- **Pass** if some allowed assignment fixes |V_us| to a value, which is then
  compared to 0.2250 at 3&sigma;.
- **No-go** if no assignment fixes |V_us| (it is either exactly 0 or 1, or
  continuously variable).

## Module 9B: the angle from wavefunction overlaps (bulk quarks)

**Added assumptions.**

| | Statement |
|---|---|
| D-9B1 | Quarks propagate in the bulk of S&sup1;/Z&#8322; with orbifold-odd (kink) masses, giving chiral zero modes with profiles e^(&minus;c y). They are neutral under U(1)_B, as R2.2 requires. Yukawas live on the y = 0 brane: Y_ij = y_ij F_Qi F_qj, with F the zero-mode value at y = 0. |
| D-9B2 | The 5D Yukawas y_ij are anarchic: independent complex numbers with \|y\| log-uniform in [1/3, 3] and uniform phases. |
| D-9B3 (symmetric) | Doublet and down-type singlet of each generation share a profile: F_Qi = F_di. Without this, F_Q1/F_Q2 is a free ratio and V_us is unconstrained; that case is reported but has no prediction to test. |

**Inputs (not predictions).** The six quark masses. Only ratios matter for
the mixing; the ratio m_d/m_s &asymp; 0.050 (scale-independent under QCD) is
the one that sets V_us. Values used: m_u, m_c, m_t, m_d, m_s, m_b at M_Z
(MS-bar, approximate &dagger;).

**Method.** For each of 20,000 anarchic samples, solve for the profiles F
so that the Yukawa eigenvalues reproduce the six masses exactly, then
compute the CKM matrix. Report the distribution of |V_us|.

**Outcomes.**
- **Sharp pass** if the central 68% interval contains 0.2250 **and** its
  half-width is at most 30% of the median.
- **Consistent, not predictive** if the central 68% interval contains
  0.2250 but is wider than that.
- **No-go** if 0.2250 lies outside the central 95% interval.

**What would be STUR-specific.** Nothing in 9B uses &theta;, k or &vartheta;
except that quarks must be U(1)_B-neutral and the Standard Model sits at
y = 0. The module therefore tests whether STUR-ROLL's geometry adds anything
to generic extra-dimensional flavour. A "consistent, not predictive" result
would be reported as exactly that.

## What changes in the main documents

- A pass in either module: `HYPOTHESIS.md` gains a conditional flavour
  prediction with its assumptions listed.
- Otherwise: one line in `HYPOTHESIS.md`, "STUR-ROLL does not predict quark
  mixing", linking to the result.

&dagger; Standard values; the conclusions depend only on |V_us| to ~1% and on
m_d/m_s to ~10%.
