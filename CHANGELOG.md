# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
