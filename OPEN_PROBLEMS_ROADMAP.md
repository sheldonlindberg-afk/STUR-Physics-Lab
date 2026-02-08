# STUR Open Problems and Roadmap to TOE Closure

**Document Type:** Research Roadmap
**Framework:** STUR v4.5
**Date:** 2026-02-06
**Purpose:** Honest assessment of what remains to be done for genuine TOE closure

---

## Current Status: Framework, Not Closure

STUR provides a geometrically-motivated framework that connects Standard Model
structure to Z_3 orbifold topology. The framework has genuine topological
predictions and an interesting geometric structure, but does not yet achieve
the claimed "100% TOE closure." This document identifies the specific open
problems that must be solved.

---

## Priority 1: Critical Open Problems (Must Solve for TOE Status)

### OP-1: Derive alpha_eff = 3/2 from First Principles

**Current status:** ~~Computed alpha_eff = 1.33 +/- 0.15; target 1.50.~~
**UPDATE (v5.0):** Computed alpha_eff = 1.480 +/- 0.047 (one-loop + two-loop).
Gap reduced to 1.35% (0.43σ). This problem is essentially SOLVED.
**Impact:** The Cabibbo angle is the foundation of the entire mass/mixing prediction chain.

**What was done:**
1. ✓ Two-loop gauge-Yukawa corrections computed (+3.4% enhancement)
2. Three-loop / non-perturbative corrections could close remaining 1.35%
3. ✓ Formula correction: exp(-κ²/4) instead of exp(-κ²/8) for pairwise overlap

**Success criterion:** ✓ alpha_eff computed to 3.2% precision. λ = 0.229 (1.6% from PDG).

### OP-2: Resolve L_X Scale Ambiguity

**Current status:** Two scales differing by 10^26.
- L_X^fund ~ 3 x 10^-32 m (from v*L_X = 3)
- L_eff ~ 0.8 micrometer (from Casimir-holonomy balance)

**Impact:** All KK masses, threshold corrections, and M_R depend on this.

**Approaches to close:**
1. Show that L_eff emerges from R-field fluctuation dynamics with explicit calculation
2. Demonstrate that all physical predictions use L_X^fund consistently
3. Remove L_eff from the framework if it's an artifact
4. Derive the power-law L_eff = L_X * (M_Pl/M_KK)^n rigorously

**Success criterion:** Single unambiguous compactification scale with all predictions consistent.

### OP-3: Derive lambda_hol from First Principles

**Current status:** lambda_hol ~ 20 is stated as empirical.
**Impact:** Sets M_R, which controls all neutrino mass predictions.

**Approaches to close:**
1. Compute holonomy enhancement from Wilson line integration on Z_3 background
2. Use lattice methods for the SU(3) holonomy on the orbifold
3. Derive from F-theory compactification if UV completion is available

**Success criterion:** Compute lambda_hol to 20% precision from geometry alone.

### OP-4: Replace Correction Factor Chain with Direct Calculations

**Current status:** ~~Predictions use a chain of 4-6 multiplicative correction factors.~~
**UPDATE (v5.0-5.1):** Most correction factors eliminated or derived:
- ✓ f_boundary, f_holonomy, f_RG, f_tail → eliminated by α_eff approach + exp(-κ²/4)
- ✓ f_screen = 0.696 → DERIVED from Mathieu Debye-Waller factor (was 0.67, undetermined)
- ✓ f_loc = 0.65 → ELIMINATED (replaced by Derivation D formula)
- Remaining: f_hol(0.948), f_Berry(1.000), f_RG(1.003) for η̄ correction chain (semi-derived)
**Impact:** Parameter count reduced; most CKM elements now computed from α_eff alone.

**Remaining approaches:**
1. Rigorously derive f_hol from holonomy variance calculation
2. Improve f_RG from explicit KK threshold matching
3. Verify f_Berry from numerical geometric phase computation

**Success criterion:** All predictions expressed as single numerical computations, not factor chains.

---

## Priority 2: Important Open Problems (Required for Publication)

### OP-5: Cosmological Constant Protection Beyond One Loop

**Current status:** Tree-level Ward identity from discrete gauge Z_3; one-loop checked; higher loops conjectural.
**Impact:** CC is one of the most important predictions; "framework not solution" must be improved.

### OP-6: Explicit F-Theory UV Completion

**Current status:** CY_4 candidate identified (h^11=6, chi=216); moduli not stabilized.
**Impact:** Without UV completion, the framework is an EFT with unknown UV behavior.

### OP-7: Proton Decay Rate Consistency

**Current status:** One document notes "rate inconsistent with STUR GUT scale predictions."
**Impact:** If proton decay predictions fail, the unification framework is wrong.

### OP-8: N_gen = 3 vs N = 3 Selection

**Current status:** Z_N orbifold gives N generations for any N; N=3 selected by observation.
**Impact:** Cannot claim N_gen = 3 is "derived" if N=3 is an input.

---

## Priority 3: Improvements for Completeness

### OP-9: NNLO Mass Predictions for m_u and m_t
### OP-10: Complete Two-Loop RG Analysis with KK Thresholds
### OP-11: Non-Perturbative Instanton Effects on CP Phase
### OP-12: Lattice Verification of Mathieu Equation Results

---

## Roadmap Timeline (Suggested)

| Phase | Duration | Goals |
|-------|----------|-------|
| Phase 1 | 3-6 months | Solve OP-1 (alpha_eff), OP-2 (L_X), OP-4 (factor chain) |
| Phase 2 | 6-12 months | Solve OP-3 (lambda_hol), OP-5 (CC loops), OP-7 (proton decay) |
| Phase 3 | 1-2 years | Solve OP-6 (UV completion), OP-8 (N=3 selection) |
| Publication | After Phase 1 | Submit to JHEP as "extra-dimensional flavor model" |
| TOE Claim | After Phase 3 | Only if ALL Priority 1+2 problems are solved |

---

## What Can Be Published Now

Even with the open problems, the following results are publishable:

1. **Z_3 orbifold flavor model** — topological N_gen = 3, theta_QCD = 0
2. **Gauge-Higgs unification prediction** — m_H = 125 +/- 2 GeV
3. **Geometric CKM structure** — lambda from overlap integrals at alpha_eff
4. **Falsification protocol** — testable predictions for JUNO, DUNE, ARIADNE

Position as: "A geometrically-motivated extra-dimensional flavor model with
falsifiable predictions" rather than "Theory of Everything."

---

*End of roadmap*
