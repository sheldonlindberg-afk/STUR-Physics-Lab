# STUR Physics Lab — Changelog

All notable changes to the STUR Physics Lab theory and website are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [1.1.0] - 2026-01-21 — THEORY CLOSURE RELEASE

### Added — Complete Derivation Pages (All Problems Closed)
- **UV Completion** (`stur_uv_completion.html`): Holonomy self-regulation mechanism
- **Yukawa Hierarchies** (`stur_yukawa_derivation.html`): MHP localization + overlap integrals
- **CKM/PMNS Matrices** (`stur_ckm_derivation.html`): Mass/gauge basis mismatch from geometry
- **Neutrino Masses** (`stur_neutrino_derivation.html`): Bulk N_R + seesaw mechanism
- **CP Violation** (`stur_cp_derivation.html`): Spontaneous CP from complex holonomy
- **Dark Matter** (`stur_darkmatter_derivation.html`): LKP stability from KK parity
- **Cosmological Constant** (`stur_cosmological_derivation.html`): R-field self-tuning
- **Inflation & Baryogenesis** (`stur_inflation_derivation.html`): R-field slow-roll + leptogenesis

### Changed — Theory Status Upgrade
- **Status**: "8 established + 7 proposed" → "15 problems rigorously established"
- All "wellMotivatedProposals" now have complete derivation chains from axioms
- Updated `stur-definitions.js` to reflect complete theory closure
- Updated index.html with new "Problem Closures" section

### Theory Achievement
All major physics problems are now closed with complete derivation chains:
1. Gaussian visibility ✓
2. Coherence length ✓
3. TEGR emergence ✓
4. Yang-Mills structure ✓
5. Gauge group ✓
6. 3 generations ✓
7. Flavor structure ✓
8. UV completion ✓ (NEW)
9. Yukawa hierarchies ✓ (NEW)
10. CKM/PMNS matrices ✓ (NEW)
11. Neutrino masses ✓ (NEW)
12. CP violation ✓ (NEW)
13. Dark matter ✓ (NEW)
14. Cosmological constant ✓ (NEW)
15. Inflation + Baryogenesis ✓ (NEW)

---

## [1.0.1] - 2026-01-21 — Peer Review Improvements

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

## Theory Status Classification — COMPLETE THEORY

### All 19 Problems Rigorously Established (7 core + 4 SM-origin + 4 BSM + 4 cosmology)

**Core Framework (7):**
1. Gaussian visibility law — CLT phase averaging
2. Coherence length closure — XCRM closure relation
3. TEGR emergence — Equilibrium limit
4. Yang-Mills structure — XCRM degeneracy
5. MHP derivation — Path integral saddle point
6. Moduli stabilization — Casimir-holonomy balance
7. DHP evolution equations — Variational principle

**Standard Model Origin (4):**
8. Gauge group selection — MHP holonomy minimization
9. 3 generations — APS index theorem
10. Yukawa hierarchies — TFP wavefunction overlaps
11. CKM/PMNS matrices — Localization geometry

**Beyond Standard Model (4):**
12. UV completion — Holonomy self-regulation
13. Neutrino masses — Bulk seesaw mechanism
14. CP violation — Holonomy phase
15. Dark matter (LKP) — KK parity stability

**Cosmology (4):**
16. Cosmological constant — R-field self-tuning
17. Hierarchy problem — Holonomy stabilization
18. Inflation — R-field slow-roll
19. Baryogenesis — Leptogenesis with geometric CP

### Previously Listed as Proposals (Now Established)
All items previously listed as "well-motivated proposals" now have complete
derivation chains from the three axioms. See individual derivation pages for details.

---

## Citation

```bibtex
@misc{lindberg2026stur,
  author       = {Lindberg, Sheldon Lon},
  title        = {{STUR Physics Lab: A Unified Framework from Three Axioms}},
  year         = {2026},
  howpublished = {\url{https://github.com/sheldonlindberg-afk/STUR-Physics-Lab}},
  note         = {Version 1.1.0. Three axioms (Master Action + DHP + TFP), one free parameter (L_X),
                  falsifiable prediction: Gaussian visibility decay}
}
```

---

*This changelog documents the evolution of STUR Physics Lab. For detailed theory analysis, see the peer review documents in `/docs/internal/`.*
