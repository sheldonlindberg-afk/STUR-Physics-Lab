# STUR Documentation Issues Registry

**Document Type:** Issue Tracking
**Framework:** STUR v4.4
**Date:** 2026-02-04
**Purpose:** Catalog all documentation inconsistencies, circular reasoning, and incomplete derivations

---

## Issue Classification

- **[SIGN]** Sign convention inconsistency
- **[SCALE]** L_X scale ambiguity
- **[CIRCULAR]** Potential circular reasoning
- **[VERSION]** Version reference inconsistency
- **[NOTATION]** Symbol/notation inconsistency
- **[INCOMPLETE]** Derivation incomplete or missing
- **[FITTED]** Parameter appears fitted rather than derived
- **[CONFLICT]** Conflicting statements across documents

---

## Part I: Sign Convention Issues

### Issue SIGN-001: chi Sign Not Consistently Documented

**Severity:** Medium
**Status:** Needs standardization

**Locations:**
- XCRM_YUKAWA_SYMMETRY_DERIVATION.md:567 - States chi = -2pi/(3*L_X) (correct)
- VLX_QUANTIZATION_DERIVATION.md:157 - States k = -chi (consistent)
- DERIVATION_CHAIN_HELIX.md:588 - States d_X phi = -chi (correct)
- HIGH_PRECISION_PREDICTIONS.md:426 - "With sign from helix chirality (left-handed)" (unclear)
- STUR_PAPER_DRAFT.md:351 - "The sign of chi (XCRM coupling)" listed as potential issue

**Issue:** While most documents use chi < 0, some use |chi| without noting the sign. The STUR_PAPER_DRAFT.md explicitly lists "sign of chi" as a potential issue, indicating awareness but no resolution.

**Recommendation:** Add explicit statement "chi = -2pi/(3*L_X) < 0 (negative by convention)" wherever chi is defined.

---

### Issue SIGN-002: CKM Phase Value Discrepancy

**Severity:** High
**Status:** Conflicting values

**Locations:**
- DERIVATION_CHAIN_HELIX.md:1844-1847 - Calculates delta_CKM = 2*arctan(eta/rho) = 132 degrees
- DERIVATION_CHAIN_HELIX.md:1847 - States "Observed: delta_CKM = (67 +/- 4) degrees"
- ETA_BAR_CORRECTION_CHAIN.md:172 - Uses delta_CKM = 66.8 degrees

**Issue:** The calculated value (132 deg) is exactly 2x the observed value (67 deg). This is the well-known convention difference between gamma = 2*arctan(eta/rho) and the PDG convention.

**Recommendation:** Clarify that 2*arctan(eta/rho) is NOT delta_CKM but rather a related quantity. The physical CKM phase gamma ~ 67 degrees should be used consistently.

---

### Issue SIGN-003: Casimir Energy Sign Confusion

**Severity:** Medium
**Status:** Explanatory text needed

**Locations:**
- LX_CASIMIR_HOLONOMY_DERIVATION.md:84-85 - "Bosons POSITIVE, Fermions NEGATIVE"
- LX_CASIMIR_HOLONOMY_DERIVATION.md:359 - "Wait - this gives a negative result! Let me recheck..."
- LX_CASIMIR_HOLONOMY_DERIVATION.md:383 - "Both derivatives are negative - energy decreases..."
- CORRECTION_FACTORS_COMPLETE.md:300 - "Wait - negative energy doesn't mean repulsive"
- TOPOLOGICAL_NCRIT_DERIVATION.md:240 - "The negative N_eff indicates repulsive Casimir force"

**Issue:** Multiple documents show confusion between:
- Negative N_eff (from fermion dominance)
- Negative energy (vacuum energy contribution)
- Repulsive vs attractive forces (sign of force derivative)

**Recommendation:** Add clear physical interpretation section: "N_eff < 0 means fermion-dominated, which creates energy that DECREASES as L_X INCREASES (repulsive = pushes walls apart)."

---

## Part II: L_X Scale Ambiguity Issues

### Issue SCALE-001: Fundamental vs Effective Scale Conflation

**Severity:** Critical
**Status:** Partially resolved (two-scale interpretation), needs consistent application

**Locations Using ~10^-32 m:**
- LX_SCALE_HIERARCHY_RESOLUTION.md:16 - "~3 x 10^-32 m"
- COMPLETE_CORRECTIONS_AND_RESOLUTIONS.md:140 - "~3 x 10^-32 m"
- CORRECTION_FACTORS_COMPLETE.md:365 - "3 x 10^-32 m"
- TOPOLOGICAL_NCRIT_DERIVATION.md:313 - "~6 x 10^-32 m"
- DERIVATION_CHAIN_HELIX.md:4862 - "10^-32 m"
- STUR_PAPER_DRAFT.md:384 - "~10^-32 m"

**Locations Using ~0.8 micrometer:**
- FTHEORY_CY4_EXPLICIT_CONSTRUCTION.md:20,910,933,1154,1180 - "0.8 micrometer"
- HIGH_PRECISION_PREDICTIONS.md:761,867-869,1398-1411 - "0.79 micrometer" or "0.8 micrometer"
- DERIVATION_CHAIN_HELIX.md:168,179,2077,6817 - "0.8 micrometer"
- SCALE_UNIFICATION_ANALYSIS.md:16,73,89,197,255,313 - "0.8 micrometer"
- STUR_PAPER_DRAFT.md:345,385 - "~0.8 micrometer" or "~1 micrometer"

**Issue:** Many documents use "L_X" without specifying which scale. Some documents mention both scales in different sections without clear distinction.

**Specific conflicts:**
- STUR_PAPER_DRAFT.md:353 - Lists "The L_X scale (10^-32 m vs. micrometer)" as explicit open issue
- STUR_PAPER_DRAFT.md:384-385 - Lists BOTH scales on consecutive lines without reconciliation
- DERIVATION_CHAIN_HELIX.md:4860-4877 - Contains explicit warning about "25-order-of-magnitude discrepancy"

**Recommendation:** Always use L_X^fund or L_X^eff to disambiguate. Add "(fundamental)" or "(Casimir)" qualifier in all documents.

---

### Issue SCALE-002: M_KK Scale Inconsistency

**Severity:** High
**Status:** Depends on which L_X is used

**Locations:**
- HIGH_PRECISION_PREDICTIONS.md:764 - M_KK = 1/L_X ~ 0.25 eV (for L_X ~ 0.8 micrometer)
- COMPLETE_CORRECTIONS_AND_RESOLUTIONS.md:158-159 - M_KK ~ pi/L_X ~ 10^16 GeV (for L_X ~ 10^-32 m)
- COSMOLOGICAL_CONSTANT_COMPLETE_DERIVATION.md:708 - M_KK ~ 0.25 meV (for L_X ~ 0.8 micrometer)

**Issue:** M_KK differs by ~25 orders of magnitude depending on which L_X is used.

**Recommendation:** Define M_KK^fund = 1/L_X^fund ~ 10^16 GeV and M_KK^eff = 1/L_X^eff ~ 0.25 eV explicitly.

---

## Part III: Circular Reasoning Issues

### Issue CIRCULAR-001: f_boundary = 0.65 Derivation Failure

**Severity:** Critical
**Status:** Admitted circular/fitted

**Locations:**
- BOUNDARY_CORRECTION_DERIVATION.md:297 - "The boundary correction factor of **0.65 cannot be derived** from simple Gaussian overlap truncation"
- BOUNDARY_CORRECTION_DERIVATION.md:314 - "The 0.65 may be a **fitting parameter** chosen to give the correct final lambda"
- BOUNDARY_FACTOR_RESOLUTION.md:292 - States f_boundary is "NOT derived from first principles in this or any other STUR document"
- BOUNDARY_FACTOR_RESOLUTION.md:306 - "Note: This 'verification' is circular - f_Z3 = 0.42 was obtained..."
- CORRECTION_FACTORS_COMPLETE.md:96-97 - "0.62 is close to the previously used 0.65 by construction, as both are chosen to produce the correct Cabibbo angle"

**Issue:** Despite claims that "all correction factors are derived from first principles" (DERIVATION_CHAIN_HELIX.md:91), f_boundary = 0.65 (or f_sector = 0.62) appears to be fitted to reproduce the observed Cabibbo angle.

**Recommendation:** Honest acknowledgment required. Either:
1. Derive f_boundary rigorously from specified assumptions, OR
2. Label as "phenomenological parameter with geometric motivation"

---

### Issue CIRCULAR-002: PMNS Form Factor f = 5.83 Fitted

**Severity:** High
**Status:** Contradictory claims

**Locations:**
- DERIVATION_CHAIN_HELIX.md:4001 - "CRITICAL HONESTY: The form lambda^2/(1-lambda^2/2) x f was chosen to highlight connection to CKM, but the function f-tilde ~ 5.83 is effectively fitted"
- DERIVATION_CHAIN_HELIX.md:4165 - "Fitted value: f chosen to reproduce sin^2(theta_12) = 0.303"
- HIGH_PRECISION_PREDICTIONS.md:1567 - "f = 5.83 (derived from TBM x seesaw corrections)"
- HIGH_PRECISION_PREDICTIONS.md:1614 - "PMNS Form Factors (ALL DERIVED, not fitted)"

**Issue:** DERIVATION_CHAIN_HELIX.md explicitly admits f is "effectively fitted" at lines 4001 and 4165. Yet HIGH_PRECISION_PREDICTIONS.md claims it is "derived" (line 1567) and states "ALL DERIVED, not fitted" (line 1614).

**Recommendation:** Reconcile these statements. If f = 5.83 is derived from TBM x seesaw, show the calculation. If it is fitted, acknowledge this.

---

### Issue CIRCULAR-003: kappa = 2.5 vs kappa = 2.52

**Severity:** Medium
**Status:** Gap acknowledged but glossed over

**Locations:**
- KAPPA_HIGHER_ORDER_CORRECTIONS.md:16 - "kappa_0 = 2.22 +/- 0.15" (from Mathieu)
- KAPPA_HIGHER_ORDER_CORRECTIONS.md:19 - "phenomenologically requires kappa = 2.5"
- KAPPA_HIGHER_ORDER_CORRECTIONS.md:24 - "Delta_kappa = kappa_total - kappa_0 = 2.5 - 2.22 = +0.28"
- Various documents use kappa = 2.5 or kappa = 2.52 interchangeably

**Issue:** The base Mathieu equation gives kappa_0 = 2.22. The final value 2.52 requires +0.30 of corrections, which are computed in KAPPA_HIGHER_ORDER_CORRECTIONS.md but with significant uncertainty. Some documents still use kappa = 2.5 exactly (no uncertainty).

**Recommendation:** Use kappa = 2.52 +/- 0.16 consistently and propagate uncertainty.

---

### Issue CIRCULAR-004: M_R Hierarchy Adjustment

**Severity:** High
**Status:** Admitted adjustment to match data

**Locations:**
- ABSOLUTE_MASS_DERIVATION.md:1190-1192 - "5.6 Adjustment of M_R: To match observed neutrino masses, we need M_R adjustment"
- ABSOLUTE_MASS_DERIVATION.md:1208 - "The STUR prediction with this adjusted M_R"
- HIGH_PRECISION_PREDICTIONS.md:1511 - "M_R seesaw scale | PMNS, delta_CP | 20% | From holonomy"
- STUR_PAPER_DRAFT.md:252 - "M_R hierarchy derived from Z_3 kink phases"
- STUR_PAPER_DRAFT.md:406 - "M_R hierarchy... now derived from Z_3 geometry"

**Issue:** ABSOLUTE_MASS_DERIVATION.md explicitly states M_R is "adjusted" to match neutrino masses. Yet other documents claim M_R hierarchy is "derived."

**Recommendation:** Clarify: Is M_R derived from Z_3 kink phases (how?), or adjusted to match neutrino data?

---

### Issue CIRCULAR-005: alpha = 1 "Natural Coupling"

**Severity:** Medium
**Status:** Convenience assumption

**Locations:**
- NUMERICAL_VERIFICATION_REPORT.md:194 - "For alpha = 1.0 (natural coupling)"
- ALPHA_PARAMETER_DERIVATION.md:447-453 - Physical motivation for sigma ~ 2pi/3 implies alpha ~ 1

**Issue:** The choice alpha = 1 is called "natural" but is essentially an O(1) choice that happens to give the right kappa. DERIVATION_CHAIN_HELIX.md:8038 admits this: "The first-principles calculation reveals that the STUR framework's Cabibbo angle... using any fitted correction factors."

**Recommendation:** Either derive alpha = 1 from first principles or acknowledge it as a natural-value assumption.

---

## Part IV: Version Inconsistency Issues

### Issue VERSION-001: Mixed Version References

**Severity:** Medium
**Status:** Needs systematic update

**Documents referencing v4.4:**
- COMPLETE_CORRECTIONS_AND_RESOLUTIONS.md:4
- COSMOLOGICAL_CONSTANT_COMPLETE_DERIVATION.md:4
- COSMOLOGICAL_CONSTANT_NEUTRINO_DERIVATION.md:4
- FTHEORY_CY4_EXPLICIT_CONSTRUCTION.md:4

**Documents referencing v4.3:**
- Most other documents (14+ files)

**Documents referencing older versions:**
- ALPHA_PARAMETER_DERIVATION.md:916 - "STUR Framework v3.6"
- KAPPA_HIGHER_ORDER_CORRECTIONS.md:1949 - "STUR Framework v3.6"
- BOUNDARY_CORRECTION_DERIVATION.md:370 - "STUR Framework v3.5"
- KAPPA_FIRST_PRINCIPLES_DERIVATION.md:947 - "STUR Framework v3.5"
- TOPOLOGICAL_NCRIT_DERIVATION.md:493 - "STUR Framework v3.8"

**Document referencing future version:**
- STUR_WEB_OVERVIEW.md:255 - "STUR v5.0" (ahead of current!)

**Issue:** VERSION_HISTORY.md states "Current Version: v4.3" but multiple documents reference v4.4, and one references v5.0.

**Recommendation:**
1. Update VERSION_HISTORY.md to acknowledge v4.4
2. Update all internal references in v3.x documents
3. Clarify whether v5.0 in web overview is intentional (future) or error

---

### Issue VERSION-002: CHANGELOG vs VERSION_HISTORY Discrepancy

**Severity:** Low
**Status:** Minor inconsistency

**Locations:**
- CHANGELOG.md:8 - "[4.3.0] - 2026-01-27 - Public Release"
- VERSION_HISTORY.md:3 - "Current Version: v4.3 (2026-01-27)"

**Issue:** CHANGELOG follows semver (4.3.0) while VERSION_HISTORY uses v4.3. Minor but should be consistent.

**Recommendation:** Standardize on either "v4.x" or "4.x.0" format.

---

## Part V: Notation Inconsistency Issues

### Issue NOTATION-001: alpha Used for Multiple Purposes

**Severity:** Medium
**Status:** Unavoidable but needs context

**Locations:**
- ALPHA_PARAMETER_DERIVATION.md - alpha = (y*v*L_X/2pi)^2 (localization)
- NUMERICAL_VERIFICATION_REPORT.md:262 - alpha_s(M_Z) (strong coupling)
- LX_SCALE_HIERARCHY_RESOLUTION.md:320-328 - alpha (fifth force coupling)
- Various - alpha_em (fine structure constant)

**Issue:** Greek letter alpha is heavily overloaded in physics. In STUR, it primarily means localization strength, but other standard meanings also appear.

**Recommendation:** Use alpha_loc for localization, alpha_s for strong, alpha_em for EM, alpha_fifth for fifth force.

---

### Issue NOTATION-002: sigma Width vs sigma Uncertainty

**Severity:** Low
**Status:** Context-dependent but confusing

**Locations:**
- Throughout - sigma = (2pi/3)/kappa (Gaussian width in radians)
- NUMERICAL_VERIFICATION_REPORT.md and others - "within 1 sigma" (statistical uncertainty)
- COMPLETE_CORRECTIONS_AND_RESOLUTIONS.md:114 - "within 1.5 sigma" (statistical)

**Issue:** sigma is used both for Gaussian width parameter and statistical uncertainty.

**Recommendation:** Use sigma_G or sigma_loc for Gaussian width; use "1-sigma" or "sigma_stat" for uncertainties.

---

### Issue NOTATION-003: theta Overloading

**Severity:** Low
**Status:** Standard physics issue

**Locations:**
- theta_12, theta_23, theta_13 - PMNS mixing angles
- theta_W - Weinberg angle
- theta - holonomy phase
- theta_Cabibbo - Cabibbo angle
- theta - generic phase coordinate

**Issue:** theta appears in many contexts. While conventional in physics, can cause confusion in STUR-specific discussions.

**Recommendation:** Always subscript theta when used: theta_PMNS, theta_hol, etc.

---

## Part VI: Incomplete Derivation Issues

### Issue INCOMPLETE-001: f_sector Modeling Dependence

**Severity:** Medium
**Status:** Acknowledged but not resolved

**Locations:**
- CORRECTION_FACTORS_COMPLETE.md:455 - "f_sector = 0.62: Approximately derived from sector confinement probability; modeling choices affect the precise value"

**Issue:** The derivation of f_sector depends on modeling choices not fully specified.

**Recommendation:** Document the specific model assumptions and their effect on the final value.

---

### Issue INCOMPLETE-002: Electroweak Scale v Derivation

**Severity:** High
**Status:** Explicitly marked as incomplete

**Locations:**
- ABSOLUTE_MASS_DERIVATION.md:591 - "v = 246.22 GeV CANNOT currently be derived from first principles"
- ABSOLUTE_MASS_DERIVATION.md:597 - "If top Yukawa y_t is derived from localization"
- DERIVATION_CHAIN_HELIX.md:3371 - Claims v emerges dynamically from radiative corrections

**Issue:** ABSOLUTE_MASS_DERIVATION.md explicitly states v cannot be derived, while DERIVATION_CHAIN_HELIX.md claims it "emerges dynamically." The derivation chain requires M_Planck as input.

**Recommendation:** Clarify: v is CONSTRAINED given M_Planck, not derived from nothing.

---

### Issue INCOMPLETE-003: M_Planck Input Acknowledged

**Severity:** High (fundamental)
**Status:** Acknowledged correctly

**Locations:**
- MPLANCK_DERIVATION_ANALYSIS.md:411 - "M_Planck cannot be derived from pure mathematics"
- MPLANCK_DERIVATION_ANALYSIS.md:162 - "This is circular: you need to know M_KK to run couplings to M_KK"
- DERIVATION_CHAIN_HELIX.md:7 - "All Standard Model parameters derived from three axioms plus M_Planck"

**Issue:** M_Planck must remain an input. This is correctly acknowledged but sometimes obscured by claims of "deriving all parameters from first principles."

**Recommendation:** Always include "...plus M_Planck" when claiming derivation from first principles.

---

### Issue INCOMPLETE-004: Topological N=3 Circularity Concern

**Severity:** Medium
**Status:** Acknowledged as potential issue

**Locations:**
- TOPOLOGICAL_NCRIT_DERIVATION.md:29-36 - "1.2 The Circularity Issue: A potential circularity is... To break this circularity, we need physics arguments that select Z_3 independently of observation"

**Issue:** The document explicitly acknowledges potential circularity in deriving N=3 generations.

**Recommendation:** The document addresses this but the resolution should be prominently summarized.

---

## Part VII: Conflicting Statement Issues

### Issue CONFLICT-001: "Zero Free Parameters" vs "Three External Inputs"

**Severity:** High
**Status:** Contradictory claims

**Locations:**
- SCALE_UNIFICATION_ANALYSIS.md:12 - "STUR v3.7 claims 'zero free parameters' but lists three 'external inputs'"
- Various documents claim "all parameters derived" while others list inputs

**Issue:** Depending on the document, STUR has:
- 0 free parameters
- 1 input (M_Planck)
- 3 inputs (M_Planck, v, alpha_em)
- 4 inputs (various lists)

**Recommendation:** Standardize on "1 dimensional input (M_Planck) plus mathematical constants and SM particle content."

---

### Issue CONFLICT-002: Derivation Status Disagreement

**Severity:** High
**Status:** Internal contradiction

**Multiple documents claim parameters are "DERIVED" while others show they are fitted:

| Parameter | Claimed DERIVED | Admitted FITTED/ADJUSTED |
|-----------|-----------------|--------------------------|
| f_boundary | DERIVATION_CHAIN_HELIX.md:107 | BOUNDARY_FACTOR_RESOLUTION.md:292 |
| f = 5.83 | HIGH_PRECISION_PREDICTIONS.md:1614 | DERIVATION_CHAIN_HELIX.md:4001,4165 |
| M_R hierarchy | STUR_PAPER_DRAFT.md:252,406 | ABSOLUTE_MASS_DERIVATION.md:1190-1192 |

**Recommendation:** Create authoritative derivation status table (see STUR_NOTATION_CONVENTIONS.md Section 5).

---

## Part VIII: Open Issues Requiring Further Work

### OPEN-001: String Theory Embedding Not Explicit

**Status:** Partially addressed in FTHEORY_CY4_EXPLICIT_CONSTRUCTION.md

The F-theory UV completion is now more explicit with:
- Specific CY_4 construction
- chi = 216, chi/24 = 9 (integer)
- Hodge numbers h^11 = 6, h^21 = 3, h^31 = 25

Remaining gaps:
- Explicit flux configuration verification
- Moduli stabilization numerical details
- D3-brane position selection principle

---

### OPEN-002: Non-Perturbative Effects Estimated

**Locations:**
- COMPLETE_CORRECTIONS_AND_RESOLUTIONS.md:688 - "Non-perturbative effects estimated, not calculated"

These include:
- Instanton corrections
- Strong CP resolution
- Gaugino condensation contributions

---

### OPEN-003: Lattice Validation Needed

**Locations:**
- NUMERICAL_VERIFICATION_REPORT.md:365 - "Lattice Validation: Perform lattice QFT calculations to independently validate the correction factors"

Specific needs:
- f_boundary verification
- f_tail verification
- kappa from lattice 5D QFT

---

### OPEN-004: Two-Scale Reconciliation Physics

**Status:** Interpretation given, physical mechanism unclear

The two scales are:
- L_X^fund ~ 10^-32 m (from v*L_X = 3 with v ~ M_GUT)
- L_X^eff ~ 0.8 micrometer (from Casimir-holonomy)

COMPLETE_CORRECTIONS_AND_RESOLUTIONS.md:191-196 gives:
- "This requires n ~ 2.5" for anomalous dimension
- "For d=5 and appropriate mass, this gives the required hierarchy"

But the "appropriate mass" and full mechanism are not specified.

---

## Summary Statistics

| Category | Count | Critical | High | Medium | Low |
|----------|-------|----------|------|--------|-----|
| SIGN | 3 | 0 | 1 | 2 | 0 |
| SCALE | 2 | 1 | 1 | 0 | 0 |
| CIRCULAR | 5 | 1 | 3 | 1 | 0 |
| VERSION | 2 | 0 | 0 | 1 | 1 |
| NOTATION | 3 | 0 | 0 | 1 | 2 |
| INCOMPLETE | 4 | 0 | 2 | 2 | 0 |
| CONFLICT | 2 | 0 | 2 | 0 | 0 |
| **TOTAL** | **21** | **2** | **9** | **7** | **3** |

---

## Recommended Priority Actions

1. **CRITICAL:** Resolve f_boundary derivation (CIRCULAR-001)
2. **CRITICAL:** Standardize L_X scale usage (SCALE-001)
3. **HIGH:** Reconcile f=5.83 derivation claims (CIRCULAR-002)
4. **HIGH:** Clarify M_R derivation vs adjustment (CIRCULAR-004)
5. **HIGH:** Update version references systematically (VERSION-001)
6. **HIGH:** Reconcile "zero parameters" claims (CONFLICT-001)
7. **MEDIUM:** Standardize chi sign documentation (SIGN-001)
8. **MEDIUM:** Clarify Casimir energy signs (SIGN-003)
9. **MEDIUM:** Add kappa uncertainty throughout (CIRCULAR-003)
10. **MEDIUM:** Document f_sector model dependence (INCOMPLETE-001)

---

**Document Status:** COMPLETE AUDIT
**Auditor:** Documentation review process
**Last Updated:** 2026-02-04
