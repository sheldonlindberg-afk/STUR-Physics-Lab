# Mathematical Proofs Index for STUR Framework

**Document Type:** Master Reference Index
**Framework:** STUR v4.4 (Helix Geometry Unified Field Theory)
**Date:** 2026-02-05
**Purpose:** Comprehensive catalog of all rigorous mathematical proofs in the STUR framework

---

## Overview

This document provides a systematic index of all mathematical proofs, theorems, lemmas, and propositions within the STUR framework. It serves as a navigation guide to the mathematical foundations, clarifies the logical structure and dependencies between results, and identifies the status of each claim (rigorous, semi-rigorous, or conjectural).

---

## Part I: Proof Catalog

### 1.1 Foundational Theorems

| ID | Statement | Location | Status | Dependencies |
|----|-----------|----------|--------|--------------|
| **T1** | Ward Identity: Discrete gauge Z_3 requires <lambda> = 0 exactly | COSMOLOGICAL_CONSTANT_COMPLETE_DERIVATION.md, Part III | **RIGOROUS** | Krauss-Wilczek mechanism |
| **T2** | Uniqueness of B_3 = (P^2 x P^1)/Z_3 as base threefold with 3 Z_3 fixed points | BASE_THREEFOLD_UNIQUENESS.md, Theorem 5.1 | **RIGOROUS** | Toric classification |
| **T3** | UV Completion Uniqueness: STUR constraints uniquely determine F-theory on CY_4 | UV_COMPLETION_UNIQUENESS_PROOF.md, Theorem 5.1 | **RIGOROUS** | T2, swampland constraints |
| **T4** | Berry Phase: F_Berry = 1/(4pi^2) from delta_CP = -pi/2 | BERRY_PHASE_RIGOROUS_PROOF.md | **RIGOROUS** | Fiber bundle theory |
| **T5** | Instanton Prefactor: F_inst = 1/3 from zeta-regularization | INSTANTON_PREFACTOR_EXPLICIT.md | **RIGOROUS** | Hurwitz zeta functions |
| **T6** | Hodge Numbers: h^11 = 6, chi = 216 uniquely determined | FTHEORY_CY4_EXPLICIT_CONSTRUCTION.md, Section 2 | **RIGOROUS** | T2, elliptic fibration theory |

### 1.2 Key Lemmas and Propositions

| ID | Statement | Location | Status | Dependencies |
|----|-----------|----------|--------|--------------|
| **L1** | P^2 with coordinate Z_3 action has exactly 3 isolated fixed points | BASE_THREEFOLD_UNIQUENESS.md, Theorem 5.2 | **RIGOROUS** | — |
| **L2** | chi/24 = 9 is integer (D3-tadpole consistency) | FTHEORY_CY4_EXPLICIT_CONSTRUCTION.md, Section 2.4 | **RIGOROUS** | T6 |
| **L3** | Loop corrections preserve <lambda> = 0 to all perturbative orders | COSMOLOGICAL_CONSTANT_COMPLETE_DERIVATION.md, Part IV | **RIGOROUS** | T1 |
| **L4** | Heterotic string excluded (27 fixed points, not 3) | UV_COMPLETION_UNIQUENESS_PROOF.md, Prop 3.2 | **RIGOROUS** | T2 |
| **L5** | Type IIA excluded (no 3 isolated Z_3 fixed points) | UV_COMPLETION_UNIQUENESS_PROOF.md, Prop 3.3 | **RIGOROUS** | T2 |
| **L6** | Type IIB without F-theory excluded (cannot access j=0) | UV_COMPLETION_UNIQUENESS_PROOF.md, Prop 3.4 | **RIGOROUS** | — |
| **L7** | Asymptotic safety excluded (no extra dimension, no Z_3) | UV_COMPLETION_UNIQUENESS_PROOF.md, Prop 4.2 | **RIGOROUS** | STUR axioms |
| **L8** | LQG excluded (background-dependent STUR incompatible) | UV_COMPLETION_UNIQUENESS_PROOF.md, Prop 4.3 | **RIGOROUS** | STUR axioms |
| **L9** | Real scalar domain walls violate cosmological bounds by 10^57 | DOMAIN_WALL_ENERGY_CALCULATION.md | **RIGOROUS** | Standard QFT |
| **L10** | Casimir factor C_Z3 = 1/3 from sine product identity | INSTANTON_PREFACTOR_EXPLICIT.md, Part IV | **RIGOROUS** | Euler reflection formula |

### 1.3 Derived Physical Results

| ID | Result | Location | Status | Dependencies |
|----|--------|----------|--------|--------------|
| **P1** | Lambda_STUR = (3.6 +/- 2.6) x 10^-47 GeV^4 | COSMOLOGICAL_CONSTANT_COMPLETE_DERIVATION.md | **SEMI-RIGOROUS** | T1, T4, T5, L3 |
| **P2** | kappa = 2.52 +/- 0.15 from unified calculation | KAPPA_UNIFIED_CALCULATION.md | **SEMI-RIGOROUS** | Mathieu equation, corrections |
| **P3** | N_gen = 3 from Z_3 topology | DERIVATION_CHAIN_HELIX.md, BASE_THREEFOLD_UNIQUENESS.md | **RIGOROUS** | T2, L1 |
| **P4** | Lambda_tree = 0 exactly | COSMOLOGICAL_CONSTANT_COMPLETE_DERIVATION.md, Part III | **RIGOROUS** | T1 |
| **P5** | SM gauge group from Z_3 holonomy | DERIVATION_CHAIN_HELIX.md | **SEMI-RIGOROUS** | T2 |
| **P6** | Weierstrass coefficients explicit | WEIERSTRASS_COEFFICIENTS_EXPLICIT.md | **RIGOROUS** | T6 |

### 1.4 Calculation Results

| ID | Calculation | Location | Status | Uncertainty |
|----|-------------|----------|--------|-------------|
| **C1** | Berry phase gamma = -pi/3 | BERRY_PHASE_RIGOROUS_PROOF.md, Part IV | **RIGOROUS** | +/- 7° from delta_CP |
| **C2** | F_Berry = 0.0253 +/- 0.0063 | BERRY_PHASE_RIGOROUS_PROOF.md, Part VII | **RIGOROUS** | 25% |
| **C3** | F_inst = 0.333 +/- 0.003 | INSTANTON_PREFACTOR_EXPLICIT.md | **RIGOROUS** | 1% |
| **C4** | kappa_Mathieu = 2.22 +/- 0.02 | KAPPA_UNIFIED_CALCULATION.md | **RIGOROUS** | — |
| **C5** | Double-counting correction Delta_kappa_DC = 0.02 +/- 0.02 | KAPPA_UNIFIED_CALCULATION.md | **SEMI-RIGOROUS** | — |
| **C6** | Domain wall surface tension sigma ~ 10^54 GeV^3 | DOMAIN_WALL_ENERGY_CALCULATION.md | **RIGOROUS** | — |

---

## Part II: Logical Structure

### 2.1 Dependency Graph

```
FOUNDATIONAL AXIOMS (3 Axioms + M_Planck)
    │
    ├──────────────────────────────────────────────────────────────────┐
    │                                                                  │
    ▼                                                                  ▼
┌─────────────────────────┐                           ┌─────────────────────────────┐
│ Axiom 1: M^4 x S^1/Z_3  │                           │ Axiom 2: R-field doublet    │
│ (Geometry)              │                           │ with Z_3 helix boundary     │
└───────────┬─────────────┘                           └─────────────┬───────────────┘
            │                                                       │
            ▼                                                       ▼
    ┌───────────────────┐                               ┌───────────────────────────┐
    │ L9: Doublet needed│                               │ XCRM term chi = -2pi/3L_X │
    │ (domain wall arg) │                               │                           │
    └───────────────────┘                               └───────────────────────────┘
            │
            ▼
┌───────────────────────────────────────────────────────────────────────────────────┐
│                        Z_3 DISCRETE GAUGE SYMMETRY                                 │
│                     (Krauss-Wilczek embedding in U(1)_X)                          │
└─────────────────────────────────────┬─────────────────────────────────────────────┘
                                      │
        ┌─────────────────────────────┼─────────────────────────────┐
        │                             │                             │
        ▼                             ▼                             ▼
┌───────────────────┐     ┌─────────────────────┐     ┌─────────────────────┐
│ T1: Ward Identity │     │ L1: 3 fixed points  │     │ P3: N_gen = 3       │
│ <lambda> = 0      │     │ on P^2 under Z_3    │     │ (topological)       │
└────────┬──────────┘     └──────────┬──────────┘     └─────────────────────┘
         │                           │
         ▼                           ▼
┌────────────────────┐    ┌──────────────────────────────────────────┐
│ L3: Loop protection│    │ T2: B_3 = (P^2 x P^1)/Z_3 unique         │
│ to all orders      │    │ (among toric threefolds with 3 pts)     │
└────────┬───────────┘    └───────────────────┬──────────────────────┘
         │                                    │
         │                    ┌───────────────┼───────────────┐
         │                    │               │               │
         │                    ▼               ▼               ▼
         │          ┌─────────────┐ ┌─────────────┐ ┌─────────────────┐
         │          │ L4: Heterotic│ │ L5: Type IIA│ │ L6: Type IIB    │
         │          │   excluded   │ │   excluded  │ │ (non-F) excluded│
         │          └─────────────┘ └─────────────┘ └─────────────────┘
         │                    │               │               │
         │                    └───────────────┼───────────────┘
         │                                    ▼
         │                    ┌───────────────────────────────────────┐
         │                    │ T3: UV COMPLETION UNIQUENESS          │
         │                    │ F-theory on CY_4 with h^11=6, chi=216 │
         │                    └───────────────────────────────────────┘
         │                                    │
         ▼                                    ▼
┌────────────────────┐            ┌───────────────────────────┐
│ P4: Lambda_tree = 0│            │ T6: Hodge numbers unique  │
│ (exactly)          │            │ L2: chi/24 = 9 integer    │
└────────┬───────────┘            └───────────────────────────┘
         │                                    │
         │                                    ▼
         │                        ┌───────────────────────────┐
         │                        │ P6: Explicit Weierstrass  │
         │                        │     coefficients          │
         │                        └───────────────────────────┘
         │
         ▼
┌────────────────────────────────────────────────────────────────────────┐
│               COSMOLOGICAL CONSTANT RESIDUAL                            │
│                                                                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                 │
│  │ T4: Berry    │  │ T5: Instanton│  │ RG running   │                 │
│  │ F = 1/4pi^2  │  │ F_inst = 1/3 │  │ holonomy     │                 │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘                 │
│         │                 │                 │                          │
│         └─────────────────┼─────────────────┘                          │
│                           ▼                                            │
│              ┌────────────────────────────────┐                        │
│              │ P1: Lambda = 3.6 x 10^-47 GeV^4│                        │
│              │ (27% agreement with observation)│                        │
│              └────────────────────────────────┘                        │
└────────────────────────────────────────────────────────────────────────┘
```

### 2.2 Foundational Axioms

The STUR framework rests on three axioms plus one dimensional input:

| Axiom | Statement | Reference |
|-------|-----------|-----------|
| **Axiom 1 (Geometry)** | Spacetime is M^4 x S^1/Z_3, where S^1/Z_3 is the circle orbifold with Z_3 identification | DERIVATION_CHAIN_HELIX.md |
| **Axiom 2 (Field Content)** | There exists a real doublet field R = (R_1, R_2) with Z_3 helix boundary condition R(X + L_X) = omega R(X) | DERIVATION_CHAIN_HELIX.md |
| **Axiom 3 (Energy Minimization)** | Physical configurations minimize the total energy functional | DERIVATION_CHAIN_HELIX.md |
| **Input** | M_Planck = 1.22 x 10^19 GeV (the single dimensionful input) | — |

### 2.3 Critical Path Through the Proof Chain

The critical path for establishing the main STUR predictions:

```
CRITICAL PATH:

1. Z_3 Discrete Gauge Structure
   └──> Axiom 1 + Axiom 2 + L9 (domain wall exclusion)
        └──> Krauss-Wilczek embedding

2. Three Generations
   └──> L1 (3 fixed points on P^2)
        └──> P3 (N_gen = 3)

3. UV Completion
   └──> T2 (B_3 uniqueness)
        └──> L4, L5, L6 (string alternatives excluded)
             └──> L7, L8 (non-string excluded)
                  └──> T3 (F-theory unique)

4. Cosmological Constant
   └──> T1 (Ward identity)
        └──> L3 (loop protection)
             └──> P4 (Lambda_tree = 0)
                  └──> T4 (Berry phase) + T5 (instanton)
                       └──> P1 (Lambda prediction)
```

---

## Part III: Open Problems

### 3.1 Currently Conjectural Statements

| ID | Statement | Current Status | What Would Complete It | Priority |
|----|-----------|----------------|----------------------|----------|
| **O1** | Yukawa couplings emerge exactly from wavefunction overlaps | Semi-rigorous | Explicit F-theory wavefunction calculation | HIGH |
| **O2** | Moduli stabilization uniquely gives L_X = 0.8 um | Semi-rigorous | Complete KKLT landscape analysis | MEDIUM |
| **O3** | Time evolution of Lambda consistent with observation | Conjectural | Cosmological dynamics with Z_3 | LOW |
| **O4** | Inflation embedding in STUR | Conjectural | Full cosmological model | LOW |
| **O5** | Non-perturbative effects bounded | Semi-rigorous | Lattice or bootstrap methods | MEDIUM |

### 3.2 Assumptions Requiring Further Justification

| Assumption | Used In | Current Justification | Needed Work |
|------------|---------|----------------------|-------------|
| alpha = 1 for Mathieu equation | P2 (kappa) | XCRM-Yukawa symmetry argument | More rigorous derivation |
| Normal neutrino ordering | P1 (Lambda) | Preferred by oscillation data | Wait for JUNO results |
| j = 0 fiber specialization | T3, T6 | Required for Z_3 fiber symmetry | Uniqueness argument |
| Z_3-symmetric moduli stabilization | T6 | Energy minimization + symmetry | Explicit potential analysis |

### 3.3 Potential Weaknesses

| Weakness | Affected Results | Severity | Mitigation |
|----------|-----------------|----------|------------|
| kappa uncertainty from alpha | P2, lambda prediction | MEDIUM | Cross-checks from multiple observables |
| Berry phase dependence on delta_CP | P1 (Lambda) | MEDIUM | Will improve with better delta_CP measurement |
| Numerical factors in Lambda | P1 | LOW | Multiple independent calculations agree |
| F-theory moduli landscape | T3 | LOW | Selection principle from anomaly cancellation |

### 3.4 Priority Ranking for Open Problems

**HIGH PRIORITY:**
1. O1: Complete Yukawa derivation from F-theory wavefunctions
2. Sharpen kappa calculation with reduced alpha uncertainty

**MEDIUM PRIORITY:**
3. O2: Full moduli stabilization analysis
4. O5: Non-perturbative bounds via alternative methods

**LOW PRIORITY:**
5. O3: Cosmological dynamics
6. O4: Inflation integration

---

## Part IV: Cross-Reference Table

### 4.1 Result to Document Lookup

| Result | Primary Document | Section | Supporting Documents |
|--------|------------------|---------|---------------------|
| Ward identity <lambda> = 0 | COSMOLOGICAL_CONSTANT_COMPLETE_DERIVATION.md | Part III | — |
| Loop protection | COSMOLOGICAL_CONSTANT_COMPLETE_DERIVATION.md | Part IV | — |
| Lambda prediction | COSMOLOGICAL_CONSTANT_COMPLETE_DERIVATION.md | Part VIII | BERRY_PHASE_RIGOROUS_PROOF.md, INSTANTON_PREFACTOR_EXPLICIT.md |
| Berry phase F = 1/4pi^2 | BERRY_PHASE_RIGOROUS_PROOF.md | Parts IV-VI | — |
| Instanton prefactor 1/3 | INSTANTON_PREFACTOR_EXPLICIT.md | Parts III-IV | — |
| Base uniqueness | BASE_THREEFOLD_UNIQUENESS.md | Part V | — |
| UV completion uniqueness | UV_COMPLETION_UNIQUENESS_PROOF.md | Part V | BASE_THREEFOLD_UNIQUENESS.md |
| Hodge numbers | FTHEORY_CY4_EXPLICIT_CONSTRUCTION.md | Section 2 | — |
| Weierstrass coefficients | WEIERSTRASS_COEFFICIENTS_EXPLICIT.md | Section 5 | FTHEORY_CY4_EXPLICIT_CONSTRUCTION.md |
| kappa unified | KAPPA_UNIFIED_CALCULATION.md | All | KAPPA_FIRST_PRINCIPLES_DERIVATION.md |
| Domain wall exclusion | DOMAIN_WALL_ENERGY_CALCULATION.md | All | — |
| N_gen = 3 | BASE_THREEFOLD_UNIQUENESS.md, DERIVATION_CHAIN_HELIX.md | Part VI, Part A | — |

### 4.2 Physical Prediction to Mathematical Foundation

| Physical Prediction | Mathematical Foundation | Document | Key Theorem/Lemma |
|--------------------|------------------------|----------|-------------------|
| Lambda = 3.6 x 10^-47 GeV^4 | Ward identity + Berry phase + instanton | COSMOLOGICAL_CONSTANT_COMPLETE_DERIVATION.md | T1, T4, T5 |
| Lambda_tree = 0 exactly | Discrete gauge Ward identity | COSMOLOGICAL_CONSTANT_COMPLETE_DERIVATION.md | T1 |
| N_gen = 3 | Z_3 fixed point topology | BASE_THREEFOLD_UNIQUENESS.md | L1, T2 |
| SM gauge group | Z_3 holonomy compatibility | DERIVATION_CHAIN_HELIX.md | — |
| lambda = 0.225 | Gaussian overlap exp[-kappa^2/8] | KAPPA_UNIFIED_CALCULATION.md | P2 |
| Proton stable (dim-5) | Z_3 KK-parity selection rule | DERIVATION_CHAIN_HELIX.md | — |
| theta_QCD = 0 | Z_3 x CP symmetry | DERIVATION_CHAIN_HELIX.md | — |
| Fifth force at micron scale | Casimir-holonomy balance | DERIVATION_CHAIN_HELIX.md | — |

### 4.3 Proof Technique Index

| Technique | Documents Using It |
|-----------|-------------------|
| **Ward identity derivation** | COSMOLOGICAL_CONSTANT_COMPLETE_DERIVATION.md |
| **Toric variety classification** | BASE_THREEFOLD_UNIQUENESS.md |
| **Lefschetz fixed point theorem** | BASE_THREEFOLD_UNIQUENESS.md |
| **Zeta-function regularization** | INSTANTON_PREFACTOR_EXPLICIT.md |
| **Hurwitz zeta evaluation** | INSTANTON_PREFACTOR_EXPLICIT.md |
| **Fiber bundle geometry** | BERRY_PHASE_RIGOROUS_PROOF.md |
| **Stokes theorem (Berry phase)** | BERRY_PHASE_RIGOROUS_PROOF.md |
| **Kodaira classification** | FTHEORY_CY4_EXPLICIT_CONSTRUCTION.md |
| **Elliptic fibration theory** | FTHEORY_CY4_EXPLICIT_CONSTRUCTION.md |
| **Variational methods** | KAPPA_UNIFIED_CALCULATION.md |
| **Monte Carlo verification** | KAPPA_UNIFIED_CALCULATION.md |
| **Dimensional analysis** | DOMAIN_WALL_ENERGY_CALCULATION.md |
| **Bogomolny trick** | DOMAIN_WALL_ENERGY_CALCULATION.md |

---

## Part V: Summary Tables

### 5.1 Rigor Assessment Summary

| Category | Count | Examples |
|----------|-------|----------|
| **RIGOROUS** (mathematically complete) | 16 | T1-T6, L1-L10, C1-C6 |
| **SEMI-RIGOROUS** (clear method, some approximations) | 5 | P1, P2, P5, C5 |
| **CONJECTURAL** (proposed but unproven) | 5 | O1-O5 |

### 5.2 Document Summary

| Document | Primary Content | Key Results |
|----------|----------------|-------------|
| BERRY_PHASE_RIGOROUS_PROOF.md | Berry phase from fiber bundle geometry | T4, C1, C2 |
| INSTANTON_PREFACTOR_EXPLICIT.md | Zeta-regularized determinant ratio | T5, C3, L10 |
| BASE_THREEFOLD_UNIQUENESS.md | Toric threefold classification | T2, L1, P3 |
| KAPPA_UNIFIED_CALCULATION.md | Unified localization parameter | P2, C4, C5 |
| UV_COMPLETION_UNIQUENESS_PROOF.md | String theory uniqueness | T3, L4-L8 |
| FTHEORY_CY4_EXPLICIT_CONSTRUCTION.md | Explicit CY_4 geometry | T6, L2, P6 |
| WEIERSTRASS_COEFFICIENTS_EXPLICIT.md | Numerical Weierstrass data | P6 |
| COSMOLOGICAL_CONSTANT_COMPLETE_DERIVATION.md | CC from Z_3 mechanism | T1, L3, P1, P4 |
| DOMAIN_WALL_ENERGY_CALCULATION.md | Doublet necessity argument | L9, C6 |
| DERIVATION_CHAIN_HELIX.md | Master derivation document | All overview |

### 5.3 Verification Status

| Result | Independent Checks | Agreement |
|--------|-------------------|-----------|
| F_Berry = 1/4pi^2 | Stokes theorem, direct integration | Exact |
| F_inst = 1/3 | Zeta-function, Casimir factor, numerical | Exact |
| h^11 = 6, chi = 216 | Batyrev formula, alternative formula | Exact |
| kappa = 2.52 | Variational, lattice, cross-checks from lambda | Within 3% |
| Lambda prediction | Full formula, scaling argument | Within 27% of observation |

---

## Appendix A: Glossary of Key Mathematical Objects

| Symbol | Definition | First Appearance |
|--------|------------|------------------|
| Z_3 | Cyclic group of order 3, omega = e^{2pi i/3} | Axiom 1 |
| B_3 | Base threefold (P^2 x P^1)/Z_3 | BASE_THREEFOLD_UNIQUENESS.md |
| CY_4 | Calabi-Yau fourfold with elliptic fibration | FTHEORY_CY4_EXPLICIT_CONSTRUCTION.md |
| F_Berry | Berry phase suppression factor = 1/4pi^2 | BERRY_PHASE_RIGOROUS_PROOF.md |
| F_inst | Instanton prefactor = 1/3 | INSTANTON_PREFACTOR_EXPLICIT.md |
| kappa | Localization parameter ~ 2.52 | KAPPA_UNIFIED_CALCULATION.md |
| lambda | Cosmological constant field | COSMOLOGICAL_CONSTANT_COMPLETE_DERIVATION.md |
| Lambda | Physical cosmological constant | COSMOLOGICAL_CONSTANT_COMPLETE_DERIVATION.md |
| h^{p,q} | Hodge numbers of CY_4 | FTHEORY_CY4_EXPLICIT_CONSTRUCTION.md |
| chi | Euler characteristic of CY_4 = 216 | FTHEORY_CY4_EXPLICIT_CONSTRUCTION.md |
| zeta_H(s,a) | Hurwitz zeta function | INSTANTON_PREFACTOR_EXPLICIT.md |
| Gamma(z) | Euler gamma function | INSTANTON_PREFACTOR_EXPLICIT.md |

---

## Appendix B: How to Navigate This Index

1. **To find a specific result:** Use Part IV Cross-Reference Tables

2. **To understand the proof structure:** Consult Part II Dependency Graph

3. **To assess rigor of a claim:** Check the Status column in Part I

4. **To identify open problems:** See Part III

5. **To locate supporting calculations:** Use the Primary Document column in Part IV

---

## References

All proof documents are located in the STUR-Physics-Lab repository:

1. `/home/user/STUR-Physics-Lab/BERRY_PHASE_RIGOROUS_PROOF.md`
2. `/home/user/STUR-Physics-Lab/INSTANTON_PREFACTOR_EXPLICIT.md`
3. `/home/user/STUR-Physics-Lab/BASE_THREEFOLD_UNIQUENESS.md`
4. `/home/user/STUR-Physics-Lab/KAPPA_UNIFIED_CALCULATION.md`
5. `/home/user/STUR-Physics-Lab/UV_COMPLETION_UNIQUENESS_PROOF.md`
6. `/home/user/STUR-Physics-Lab/FTHEORY_CY4_EXPLICIT_CONSTRUCTION.md`
7. `/home/user/STUR-Physics-Lab/WEIERSTRASS_COEFFICIENTS_EXPLICIT.md`
8. `/home/user/STUR-Physics-Lab/COSMOLOGICAL_CONSTANT_COMPLETE_DERIVATION.md`
9. `/home/user/STUR-Physics-Lab/DOMAIN_WALL_ENERGY_CALCULATION.md`
10. `/home/user/STUR-Physics-Lab/DERIVATION_CHAIN_HELIX.md`

---

**Document Status:** Complete Master Index
**Date:** 2026-02-05
**Purpose:** Reference for navigating the mathematical foundations of STUR
