# Chronomagnetic Geological Predictions — Exact Formula

**Document Type:** Numerical Predictions  
**Framework:** STUR v7.1 / Chronomagnetics (Lindberg et al.)  
**Date:** 2026-06-19  
**Status:** Honest recomputation; PDF table values corrected  

---

## Executive Summary

This document provides honest recomputation of chronomagnetic modulation values M(t) for
major geological and biological events using the exact formula derived in STUR. An important
discrepancy is disclosed: the values in Table 3 and Table 4 of the Chronomagnetics PDF
(Lindberg, Burkeen, Cyrek, Lockwood, LaMarche, Beaubier) do **not** match the formula as
stated. The exact computation is given here; the PDF tables require correction.

The genuine falsifiable predictions from Chronomagnetics are the **phase-lock epochs**: times
when M(t) = 1, i.e., when ω ln((t + t_c)/t₀) = π/2 + nπ for integer n. These are the
epochs of maximal chronomagnetic coherence and are the primary observational target.

---

## 1. The Exact Formula

The chronomagnetic modulation function is:

```
M(t) = |sin(ω · ln((t + t_c) / t₀))|
```

where:
- t is the lookback time (positive = past), in Ma (millions of years)
- ω = 2π² = 19.7392  [exact, from ∞₃ phase closure]
   (or ω_triangle = 2π/ln(3722/2705) = 19.6867, 0.27% difference)
- t_c is a phase offset calibration parameter (in Ma)
- t₀ is the reference epoch (in Ma)

**The PDF uses ω = ω_triangle = 19.6867.**

**Calibration:** The parameters t_c and t₀ must be fixed by at least one known phase-lock
epoch or by the present-day M value. The PDF appears to have used specific calibration values
that are not explicitly stated in the table, which is the source of the table-formula
discrepancy documented below.

For the computations in this document, we adopt:

```
ω = 19.6867   (triangle value, matching the PDF derivation)
t₀ = 1 Ma    (calibration epoch — smallest log-time unit)
t_c = 0       (no phase offset unless calibrated from data)
```

These are illustrative values for demonstrating the formula; the PDF's exact calibration
parameters are not recoverable from the published table without additional information.

---

## 2. Discrepancy Between PDF Tables and the Formula

### 2.1 K-Pg Boundary Check (t = 66 Ma)

PDF Table 3 claims: M(66 Ma) = 0.9882

Computing with the formula M(t) = |sin(ω × ln(t/t₀))| with t₀ = 1 Ma:

```
M(66) = |sin(19.6867 × ln(66))| = |sin(19.6867 × 4.1897)| = |sin(82.48)| = |sin(82.48 rad)|
```

82.48 rad = 82.48 − 13×2π = 82.48 − 81.68 = 0.80 rad

```
M(66) = |sin(0.80)| = 0.717
```

This gives M ≈ 0.72, not 0.9882 as stated in the PDF.

### 2.2 Present-Day Check (t = 0)

PDF Table 3 claims: M(0) = 0.9730

With t_c = 0 and any t₀ > 0, the formula gives M(0) = |sin(ω × ln(t_c/t₀))|, which
depends entirely on the phase offset t_c. With t_c = 0 the argument is ln(0) = −∞, which is
undefined. This indicates the PDF uses a non-zero t_c (a phase anchor).

### 2.3 Conclusion on the Discrepancy

The PDF table values (all M > 0.89, classified as "MAJOR") were computed with calibration
parameters (t_c, t₀ or equivalent) that are not stated in the publication. They cannot be
reproduced from the formula as written without those parameters.

**This is a documentation gap, not necessarily an error in the chronomagnetic framework.**
The framework predicts phase-lock epochs at M = 1; whether the major geological events fall
near those epochs is a testable prediction that depends on the calibration.

**Until the calibration parameters are published or independently determined, Table 3 and
Table 4 of the Chronomagnetics PDF should not be cited as quantitative predictions.**

---

## 3. Genuine Falsifiable Predictions: Phase-Lock Epochs

### 3.1 Phase-Lock Condition

Phase-lock occurs when M(t) = 1, i.e.:

```
ω × ln((t + t_c) / t₀) = π/2 + n × π     for n = 0, 1, 2, …
```

Equivalently:

```
(t + t_c) / t₀ = exp((π/2 + nπ) / ω) = exp((2n+1)π / (2ω))
```

For ω = 2π²:

```
(t + t_c) / t₀ = exp((2n+1) / (4π))
```

### 3.2 Log-Periodic Spacing

Consecutive phase-lock epochs are spaced by the chronomagnetic ratio:

```
t_{n+1} / t_n = exp(π / ω) = exp(1/(2π)) = e^{1/(2π)} = 1.1696   [exact, ω = 2π²]
               ≈ 1.1694                                             [ω = ω_triangle]
```

This means phase-lock epochs are spaced by a factor of ~1.17 in lookback time, i.e., each
epoch is about 17% further back than the previous one.

### 3.3 Predicted Phase-Lock Epochs (Relative Spacing)

Starting from a calibration epoch at t_ref (the most recent phase-lock), subsequent epochs
are at:

```
t_n = t_ref × (e^{1/(2π)})^n     (n = 1, 2, 3, …  for past epochs)
```

The spacing in log-time between consecutive phase-lock events is constant:

```
Δ(ln t) = π / ω = 1/(2π) = 0.15915     [exact]
```

This corresponds to ~15.9% of a decade in log-time between consecutive phase-lock epochs.

### 3.4 What Can Be Tested Without Calibration

Even without fixing t_c and t₀, the framework makes a **parameter-free prediction**:

> **Major coherence events should cluster at times forming a geometric sequence with ratio
> e^{1/(2π)} ≈ 1.1696.**

If major extinction events, magnetic reversals, and climate transitions are analyzed for
log-time clustering, the chronomagnetic prediction is that they should be spaced by factors
of ≈ 1.17 in lookback time. This is a falsifiable statistical prediction that does not
require knowing the absolute phase-lock epochs.

---

## 4. Sample Computation: Phase-Lock Windows Near the Present

Assuming the most recent phase-lock occurred N million years ago (unknown without calibration),
the next predicted phase-lock is N × 1.1696 Ma ago, the one before that was N / 1.1696 Ma
ago.

For reference: if we assume the Brunhes-Matuyama reversal (0.773 Ma) was near a phase-lock
epoch, the predicted spacing gives neighboring epochs at:

```
t_{prev} = 0.773 / 1.1696 = 0.661 Ma     (0.661 Ma ago)
t_{next} = 0.773 × 1.1696 = 0.904 Ma     (0.904 Ma ago)
t_{next+1} = 0.904 × 1.1696 = 1.058 Ma  (1.058 Ma ago)
```

These are predictions conditional on the Brunhes-Matuyama being a phase-lock epoch —
an assumption that requires verification.

---

## 5. Reconciliation with the PDF Tables

To reconcile the PDF Table 3 values with the formula, the following is needed:

1. **State the calibration parameters explicitly:** t_c and t₀ (or equivalent phase anchor)
2. **Verify each table entry** by computing M(t) = |sin(ω × ln((t + t_c)/t₀))| for each
   geological event
3. **Report actual M values** rather than rounding all events to M > 0.89 (which appears
   inconsistent with a formula that spans the full range 0 ≤ M ≤ 1)

Until this reconciliation is published, the honest statement is:

> The Chronomagnetics framework predicts log-periodic phase-lock epochs with spacing factor
> e^{1/(2π)} ≈ 1.17. Whether the specific geological events in Table 3 coincide with these
> epochs depends on the calibration parameters, which have not yet been published in
> reproducible form.

---

## 6. Status of Chronomagnetic Geological Predictions

| Prediction | Basis | Status |
|-----------|-------|--------|
| Log-periodic spacing e^{1/(2π)} ≈ 1.17 | ω = 2π² from phase closure | **Derived** |
| Discrete scale invariance M(λt) = M(t) | ω × ln(λ) = 2π | **Exact** |
| Phase-lock windows (M = 1) near reversals | Framework | **Testable with calibration** |
| Table 3 geological event values | PDF (not reproducible) | **Requires correction** |
| Future windows at 0.44, 3.05, 6.27 Ma | PDF Table 4 | **Requires calibration verification** |

---

## References

- `TRIANGLE_GENESIS_DERIVATION.md` — derivation of ω = 2π² and λ_chrono = e^{1/π}
- `DERIVATION_CHAIN_INFINITY.md` §2.3b — first-principles derivation of ω
- `scripts/Chronomagnetics.pdf` — original paper (Lindberg, Burkeen, Cyrek, Lockwood,
  LaMarche, Beaubier) — Tables 3 and 4 require calibration disclosure
- `scripts/chronomagnetics_closure.py` — numerical framework (PART 1, PART 4)

---

*This document provides an honest account of what the chronomagnetic framework predicts and
what requires further calibration disclosure. The core prediction — log-periodic phase-lock
spacing — is derived and falsifiable. The PDF table values are not reproducible without
the calibration parameters and should not be cited as quantitative predictions until those
parameters are published.*
