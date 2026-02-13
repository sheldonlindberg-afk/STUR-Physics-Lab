<p align="center">
  <img src="assets/4.13.png" alt="STUR Physics Lab Logo" width="200"/>
</p>

<h1 align="center">STUR Physics Lab</h1>

<p align="center">
  <strong>Sheldon's Theory of Unified Resistance</strong><br>
  <em>Dynamic Z₃ Phase-Lock Unification — Theory of Everything Candidate</em>
</p>

<p align="center">
  <a href="https://creativecommons.org/publicdomain/zero/1.0/"><img src="https://img.shields.io/badge/License-CC0_1.0-lightgrey.svg" alt="License: CC0-1.0"></a>
  <img src="https://img.shields.io/badge/Physics-Theory_of_Everything-blueviolet" alt="Physics: Theory of Everything">
  <img src="https://img.shields.io/badge/Version-6.0-brightgreen" alt="Version: 6.0">
  <img src="https://img.shields.io/badge/PWA-Installable-green" alt="PWA: Installable">
  <img src="https://img.shields.io/badge/Pages-114+-blue" alt="Pages: 114+">
  <img src="https://img.shields.io/badge/Cabibbo_Angle-1.6%25-brightgreen" alt="Cabibbo Angle: 1.6%">
  <img src="https://img.shields.io/badge/CKM_Matrix-Derived-orange" alt="CKM Matrix: Derived">
</p>

---

## Overview

**STUR** (Sheldon's Theory of Unified Resistance) is a Theory of Everything candidate built on three pillars: **TEGR** (torsion gravity), the **XCRM** coupling (unique R-field torsion term), and **Chronomagnetics** (log-periodic phase dynamics). The framework derives Standard Model structure from a dynamically oscillating **Z₃ orbifold** on M⁴ × S¹.

The Z₃ helix is not static — the twist angle continuously winds and unwinds on a chronomagnetic cycle. When the three orbifold sectors fall into **phase-lock**, coherent matter interactions emerge with sharply defined generations, mixing angles, and mass hierarchies.

**Key results (v6.0, all derived from first principles):**

- **N_gen = 3** — topological (Z₃ fixed-point count)
- **Cabibbo angle λ = 0.229** — 1.6% from PDG (exp[−κ²/4] pairwise overlap)
- **Full CKM matrix** — 9 elements derived to 1.6–7.5% accuracy
- **CP violation δ_CKM = 68.3°** — from helix chirality (4.4% from measurement)
- **θ_QCD = 0** — automatic from Z₃ × CP symmetry (no axion needed)
- **Berry phase = 0** — verified exactly
- **m_τ/m_μ = 17.0** — 1% from observed (brane Yukawa hierarchy)

**Open problems:** L_X stabilization, absolute fermion masses, cosmological constant.

---

## Features

### Dynamic Z₃ Phase-Lock Framework (v6.0)
- TEGR torsion gravity → R-field doublet → XCRM unique coupling → Z₃ orbifold → Phase-lock
- Chronomagnetic modulation M(t) = |sin(ω ln(t/t₀))| with ω = 19.687
- Phase-locked CKM matrix: Cabibbo angle λ = exp[−κ²/4] = 0.229
- Three generations from Z₃ topology; SU(3)×SU(2)×U(1) from holonomy

### Interactive Web Documentation
- **Progressive Web App (PWA)** - installable on any device
- **Works offline** - full service worker support
- **114+ HTML pages** covering all aspects of the theory
- **MathJax 3** for beautiful equation rendering

### Physics Domain Color Coding
Equations are color-coded by physics domain for easy identification:
- Quantum Mechanics
- Electromagnetism
- Gravity/Cosmology
- Particle Physics
- Thermodynamics
- Mathematics

### Computational Verification
- Python scripts for numerical verification of predictions
- Boundary correction calculations
- Parameter derivation analysis

---

## Quick Start

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/STUR-Physics-Lab.git
   cd STUR-Physics-Lab
   ```

2. **Start a local server**

   Using Python:
   ```bash
   python -m http.server 8000
   ```

   Using Node.js:
   ```bash
   npx serve .
   ```

   Using PHP:
   ```bash
   php -S localhost:8000
   ```

3. **Open in browser**

   Navigate to `http://localhost:8000`

> **Note:** No build step required - STUR Physics Lab is pure static HTML/CSS/JS.

### Install as PWA

Visit the live site and click "Install" when prompted, or use your browser's "Add to Home Screen" option for offline access.

---

## Project Structure

```
STUR-Physics-Lab/
|
|-- index.html              # Main landing page
|-- about.html              # About the theory
|-- sitemap.html            # Complete site navigation
|-- mycitations.html        # References and citations
|
|-- scripts/                # Theory documentation (110 HTML pages)
|   |-- stur_core_theory.html
|   |-- stur_predictions.html
|   |-- stur_simulations_hub.html
|   |-- stur_cosmological_constant.html
|   |-- stur_ckm_derivation.html
|   |-- ... (105+ more pages)
|
|-- assets/
|   |-- css/                # Styling
|   |   |-- stur-core.css       # Core styles
|   |   |-- stur-glass.css      # Glassmorphism effects
|   |   |-- stur-theory.css     # Theory page styles
|   |   |-- stur-icons.css      # Icon styles
|   |   +-- stur-index.css      # Index page styles
|   |-- js/                 # JavaScript utilities
|   +-- icons/              # PWA icons (72px to 512px)
|
|-- *.md                    # Technical derivation documents (28 files)
|   |-- DERIVATION_CHAIN_HELIX.md
|   |-- COSMOLOGICAL_CONSTANT_NEUTRINO_DERIVATION.md
|   |-- ALPHA_PARAMETER_DERIVATION.md
|   +-- ...
|
|-- *.py                    # Computational verification scripts
|-- manifest.json           # PWA manifest
|-- sw.js                   # Service worker for offline support
+-- LICENSE                 # CC0 1.0 Universal
```

---

## Key Predictions

### Quantitative Results (v6.0)

| Observable | STUR Prediction | Measurement | Deviation |
|-----------|----------------|-------------|-----------|
| **Cabibbo angle λ** | 0.229 ± 0.008 | 0.22500 ± 0.00067 | **1.6%** |
| **η̄ (CP violation)** | 0.350 ± 0.029 | 0.348 ± 0.010 | **0.5%** |
| **δ_CKM** | 68.3° | 65.4° | **4.4%** |
| **N_gen** | 3 (exact) | 2.984 ± 0.008 | **Exact** |
| **θ_QCD** | 0 (exact) | < 10⁻¹⁰ | **Exact** |
| **m_τ/m_μ** | 17.0 | 16.8 | **1%** |

### Kill Criteria

| Prediction | What would falsify STUR |
|-----------|------------------------|
| N_gen = 3 exactly | Discovery of sequential 4th generation |
| θ_QCD = 0 exactly | Neutron EDM > 10⁻²⁸ e·cm |
| Z₃ KK structure | Non-Z₃ KK graviton spectrum |
| Proton stable (dim-5) | Proton decay via dim-5 operators |

### Chronomagnetic Predictions (Novel)

- Log-periodic CKM drift at λ_chrono = 3722/2705 timescale
- Phase-lock signatures in cosmological observables
- Chronomagnetic resonance at ω ≈ 19.687

---

## Documentation

### Core Theory
- [Core Theory Framework](scripts/stur_core_theory.html) - The three axioms and derivation structure
- [Z_3 Helix Geometry](scripts/stur_5duniverse.html) - Extra dimension topology
- [Generation Structure](scripts/stur_generations.html) - Why exactly 3 generations

### Predictions
- [All Predictions](scripts/stur_predictions.html) - Complete list with experimental status
- [Cosmological Constant](scripts/stur_cosmological_constant.html) - CC derivation and solution

### Technical Derivations
- [Complete Derivation Chain](DERIVATION_CHAIN_HELIX.md) - Full mathematical derivation
- [Alpha Parameter](ALPHA_PARAMETER_DERIVATION.md) - Fine structure constant
- [Neutrino & CC](COSMOLOGICAL_CONSTANT_NEUTRINO_DERIVATION.md) - Neutrino mass and cosmological constant

### Simulations
- [Simulations Hub](scripts/stur_simulations_hub.html) - Interactive demonstrations

---

## Contributing

Contributions are welcome! This is an open science project dedicated to the public domain.

### Ways to Contribute

1. **Scientific Review** - Analyze derivations and identify potential issues
2. **Numerical Verification** - Run and extend computational checks
3. **Documentation** - Improve clarity and accessibility
4. **Web Development** - Enhance the interactive experience
5. **Experimental Proposals** - Design tests for predictions

### Contribution Process

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Make your changes
4. Submit a Pull Request with a clear description

---

## License

This work is dedicated to the **public domain** under the [CC0 1.0 Universal](https://creativecommons.org/publicdomain/zero/1.0/) license.

You are free to:
- Copy, modify, and distribute the work
- Use for any purpose, including commercial
- No attribution required (though appreciated)

---

## Citation

If you reference STUR in academic work, please cite:

```bibtex
@misc{stur2025,
  author       = {Lindberg, Sheldon},
  title        = {{STUR}: {S}heldon's {T}heory of {U}nified {R}esistance --
                  Dynamic {Z}_3 Phase-Lock Unification},
  year         = {2025},
  howpublished = {\url{https://github.com/sheldonlindberg-afk/STUR-Physics-Lab}},
  note         = {TOE candidate: CKM matrix derived to 1.6\% from dynamic Z₃
                  orbifold phase-lock on TEGR torsion gravity}
}
```

---

<p align="center">
  <em>Science advances by proposing falsifiable theories.</em><br>
  <strong>STUR awaits experimental judgment.</strong>
</p>
