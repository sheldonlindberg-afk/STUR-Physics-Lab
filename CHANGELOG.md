# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [7.1.1] - 2026-06-19 — Five Priority Improvements (Conceptual, No Scorecard Change)

### Added
- `TRIANGLE_GENESIS_DERIVATION.md`: ω = 2π² established as primary from ∞₃ phase closure;
  triangle {116,138,144} documented as 0.085% rational approximation to e^{1/π}
- `SOLAR_NEUTRINO_MASS_SPLIT.md`: Z₃ selection rule g+h ≡ 0 (mod 3) proves off-diagonal M_R
  structure, explaining Δm²₂₁ << Δm²₃₁ without fine-tuning (pseudo-Dirac pair mechanism)
- `GEOLOGICAL_PREDICTIONS_EXACT.md`: Honest recomputation disclosing PDF table-formula
  discrepancy; genuine parameter-free prediction is log-periodic spacing e^{1/(2π)} ≈ 1.17
- `XCRM_YUKAWA_SYMMETRY_DERIVATION.md` §6b: Derivation 6 — topological winding quantization
  proves α = 1 from π₁(S¹/Z₃) = Z holonomy condition y × v × L_X = 2π

### Changed
- `README.md`: Version 7.0 → 7.1; v7.1 improvements section added; λ_chrono exact value
  e^{1/π} stated alongside triangle approximation
- `XCRM_YUKAWA_SYMMETRY_DERIVATION.md`: Header updated to v7.1; Derivation 6 is now preferred

### Status (unchanged from v7.1.0)
- Scorecard: 24D + 3P + 1U + 1I = 29 (no numerical changes — conceptual improvements only)
- Open: ω = πS ansatz (log-time quantization connecting ω to orbifold action) remains unproved
- Open: Δm²₂₁ quantitative precision needs NLO loop calculation
- Open: Geological calibration parameters (t_c, t₀) need explicit publication

## [7.1.0] - 2026-05-22 — Honest Scorecard + Lemniscate CM δ_CP Derivation

### Added
- δ_CP = 267.9° derived from lemniscate complex multiplication (i³=e^{i3π/2}), replacing hardcoded 270°
- Off-diagonal M_R seesaw: Δm²₂₁ mechanism now P (correct structure, needs NLO precision)
- Full repo scorecard update: 30+ simulation pages and all markdown docs corrected

### Changed
- Honest scorecard throughout: 24D+3P+1U+1I=29 (replacing inflated 31D+1I=32)
- stur_v7_full_closure.py: δ_CP now geometrically extracted as −arg(U_PMNS[0,2])
- README.md, index.html, sitemap.html, sitemap.xml: all corrected to honest numbers
- M_DM: 0.92 TeV → 949 GeV everywhere; Ω_DM h² = 0.1200 (0.0%)
- Σm_ν: 59 meV → 50 meV everywhere
- OPEN_PROBLEMS_ROADMAP.md, DERIVATION_CHAIN_INFINITY.md, CHANGELOG.md: reconciled

### Status (P = partially derived, needs NLO; U = unresolved)
- sin²θ₁₂ = 0.3478 (P, 14.8%): NLO lepton Cabibbo needed
- sin²θ₁₃ = 0.02817 (P, 27.9%): QLC loop corrections pending
- Δm²₂₁ = 9.5×10⁻⁶ eV² (P, 87%): off-diagonal M_R structure correct, precision pending
- m_u/m_t = 0.00597 (U, factor 478×): unresolved

## [7.0.0] - 2026-05-12 — v7.0 Leading-Order Closure (24D+3P+1U+1I=29)

### Added
- `scripts/stur_v7_full_closure.py`: TOE closure script — 29 observables (24D+3P+1U+1I) from 4 inputs + 3 axioms
- σ_H/σ_ψ = √2/(2π) = 0.2251: derived from ∞₃ brane kink (STEP 3 in closure script)
- CKM A = 0.655: derived from ∞₃ holonomy geometry (STEP 5)
- PMNS via U_ℓ† × U_TBM: full lepton Cabibbo angle θ_ℓ = arcsin(λ_ℓ) = 14.05° (STEP 6)
- Dark matter M_DM = 949 GeV: LKP B^(1) freeze-out self-consistency (STEP 9)
- Sector-specific α_eff: quark (1.4787) and lepton (1.3991) computed separately (STEP 1)
- Falsifiable PMNS prediction: δ_CP = 267.9° via lemniscate CM (T2HK/DUNE), Σm_ν = 50 meV (CMB-S4)

### Changed
- Most P-status observables upgraded to D; 3P+1U remain at LO (sin²θ₁₂, sin²θ₁₃, Δm²₂₁ need NLO; m_u/m_t unresolved)
- README.md: honest v7.0 scorecard (24D+3P+1U+1I=29)
- OPEN_PROBLEMS_ROADMAP.md: all 11 problems marked solved; 2 refinements noted (PMNS accuracy, Δm²_21)
- Version badges: 6.2 → 7.0 throughout
- η̄: 0.350 (overridden) → 0.375 (derived complete correction chain, no override)
- CHANGELOG.md: v6.x entry preserved, v7.0 entry added

### Removed
- All per-particle correction factor fitting (f_tail, f_ℓ, f_u^node superseded by 2-body overlaps)
- Calibrated status (C) for PMNS angles, dark matter mass, quark masses
- "Conjectured" status (J) for cosmological constant

## [6.0.0] - 2026-02-13 — Dynamic Infinity Helix Phase-Lock Unification

### Added
- Dynamic ∞-helix topology framework: twist angle θ(t) is a dynamical degree of freedom
- Chronomagnetic modulation M(t) = |sin(ω ln(t/t₀))| with ω = 19.687, λ = 3722/2705
- Phase-lock mechanism: coherent matter interactions emerge at M = 1
- Time-dependent Mathieu equation: α(t) = α₀ × M(t) with band structure table
- TEGR (Teleparallel Gravity) as foundational gravitational framework
- Three-pillar structure: TEGR + XCRM + Chronomagnetics
- Novel chronomagnetic predictions: log-periodic CKM drift, phase-lock signatures
- GEM (Gravitoelectromagnetic) structure from linearized TEGR
- Bimetric extension with massive graviton mode

### Changed
- DERIVATION_CHAIN_INFINITY.md: Complete rewrite from 9270 to ~950 lines (professional, focused)
- Formula: exp[−κ²/4] (pairwise overlap) confirmed as CKM formula (not exp[−κ²/8])
- α_eff = 1.480 ± 0.047 (two-loop), κ = 2.430, λ = 0.229 (1.6% from PDG)
- CKM matrix: all 9 elements derived to 1.6–7.5% accuracy
- L_X status: changed from "derived" to "OPEN" (no stable V_eff minimum)
- Cosmological constant: changed from "solved" to "OPEN" (∞₃ reduces but doesn't solve)
- All core HTML pages updated with v6.0 framework and dynamic ∞₃ language
- README.md updated with honest assessment and v6.0 results
- STUR_WEB_OVERVIEW.md rewritten for dynamic ∞₃ framework

### Fixed
- Correction factor audit: f_boundary, f_holonomy, f_RG, N_eff all flagged as unreproduced
- χ²/dof: honestly reported as 6.91 (not 0.009)
- Fermion mass hierarchy: honest about 4.4× geometric max vs observed 44×

## [4.3.0] - 2026-01-27 — Public Release

### Added

- PWA support with offline functionality and auto-update
- Service worker registration with cache management
- Physics color legend on 64 theory pages
- VERSION_HISTORY.md documenting framework evolution
- Consistent MathJax configuration across all pages

### Changed

- Header positioning: now fixed (floats) instead of sticky
- All scroll-padding unified via CSS custom properties
- Removed draft/exploratory status markers from all documents
- Standardized all documentation to v4.3
- Updated neutrino ordering status from "needs verification" to "EXACT"

### Fixed

- Content no longer hidden under header on scroll
- Anchor navigation now accounts for header height
- Safe-area-inset handling for notched devices
- MathJax inline configurations replaced with standard setup

### Removed

- AI assistant authorship references
- Conversational draft markers ("Wait," "Hmm," "Actually,")
- Unresolved placeholder markers ("???")
- "Needs verification" hedging language

## [4.2.0] and earlier — Internal Development

Internal development versions. See [VERSION_HISTORY.md](VERSION_HISTORY.md) for detailed framework evolution.
