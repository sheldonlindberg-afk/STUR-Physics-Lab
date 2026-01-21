# STUR Physics Lab — Changelog

All notable changes to the STUR Physics Lab theory and website are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [Unreleased]

### Added
- Comprehensive peer review document (`PEER_REVIEW_MOBILE_SITE_2026.md`)
- External CSS file for index page styles (`stur-index.css`)
- Skip-to-content accessibility link
- Improved keyboard focus visibility
- BibTeX citation format support
- Version history/changelog (this file)
- Performance hints (`will-change`, reduced motion support)
- `aria-hidden` attributes on decorative elements

### Changed
- Moderated "Complete Theory" claims with appropriate caveats
- Added caveat for gauge group uniqueness claim
- Improved MHP physical motivation documentation
- Optimized backdrop-filter for low-end devices
- Extracted ~550 lines of inline CSS from index.html to external file

### Fixed
- Keyboard focus visibility for accessibility
- Missing aria-hidden on decorative icons

---

## [1.0.0] - 2026-01-21

### Theory Foundation
- **Master Action** (Axiom 1): Complete specification of the unified resistance action
  - Diffusion term: ½(∇R)²
  - Relaxation potential: V(R) = (λ/4)(R² - v²)²
  - XCRM coupling: χR∂ₓR
  - Torsion coupling: αR𝕋
  - Matter Lagrangian: ℒ_matter

- **Dynamic Holonomy Principle** (Axiom 2): Universe evolves along minimum integrated holonomy path
  - Closes: UV completion, neutrino masses, CP violation, dark matter, Λ problem, inflation, baryogenesis

- **Minimum Holonomy Principle** (Derived): Path integral saddle point condition
  - Derived from Faddeev-Popov procedure
  - Closes: Gauge group, generations, flavor structure, Yukawa hierarchies

### Key Predictions
- **Primary Prediction**: Gaussian visibility decay
  - Formula: V(ΔL) = V₀ exp(−ΔL²/ℓ²_coh)
  - Properties: No time dependence, no mass dependence
  - Testable with: MAGIS-100, AION, Sagnac loops

### Falsification Criteria
- Theory falsified if:
  - Visibility is oscillatory (sinusoidal)
  - Visibility depends on time
  - Visibility depends on particle mass at fixed shot time
  - Functional form deviates from Gaussian in ΔL²

### Website Features
- 59+ theory pages covering all aspects of STUR
- Interactive sandbox for mathematical verification
- Mobile-first responsive design
- iOS-26 inspired glassmorphic aesthetics
- Physics domain color-coding system
- MathJax rendering with custom macros

### Documentation
- Complete Technical Appendix with mathematical derivations
- Glossary of STUR-specific terminology
- Learning resources and prerequisites
- Multiple peer review documents

---

## Version Numbering

- **Major version** (X.0.0): Fundamental changes to axioms or primary predictions
- **Minor version** (0.X.0): New derivations, pages, or significant documentation
- **Patch version** (0.0.X): Bug fixes, typos, minor clarifications

---

## Theory Status Classification

### Rigorously Established (7)
1. Gaussian visibility law
2. Coherence length closure
3. TEGR emergence
4. Yang-Mills structure
5. Gauge group selection
6. 3 generations (APS index)
7. Flavor structure

### Well-Motivated Proposals (8)
1. Yukawa hierarchies
2. CKM/PMNS matrices
3. UV completion
4. Neutrino masses
5. CP violation
6. Dark matter (KK parity)
7. Cosmological constant
8. Inflation & baryogenesis

---

## Citation

```bibtex
@misc{lindberg2026stur,
  author       = {Lindberg, Sheldon Lon},
  title        = {{STUR Physics Lab: A Unified Framework from Two Axioms}},
  year         = {2026},
  howpublished = {\url{https://github.com/sheldonlindberg-afk/STUR-Physics-Lab}},
  note         = {Version 1.0.0. Two axioms (Master Action + DHP), one free parameter (L_X),
                  falsifiable prediction: Gaussian visibility decay}
}
```

---

*This changelog documents the evolution of STUR Physics Lab. For detailed theory analysis, see the peer review documents in `/docs/internal/`.*
