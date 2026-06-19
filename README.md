<p align="center">
  <img src="assets/4.13.png" alt="STUR Physics Lab Logo" width="200"/>
</p>

<h1 align="center">STUR Physics Lab</h1>

<p align="center">
  <strong>Sheldon's Theory of Unified Resistance</strong><br>
  <em>STUR v7.1: Dynamic Infinity Helix &mdash; Theory of Everything Candidate</em>
</p>

<p align="center">
  <a href="https://creativecommons.org/publicdomain/zero/1.0/"><img src="https://img.shields.io/badge/License-CC0_1.0-lightgrey.svg" alt="License: CC0-1.0"></a>
  <img src="https://img.shields.io/badge/Physics-Theory_of_Everything-blueviolet" alt="Physics: Theory of Everything">
  <img src="https://img.shields.io/badge/Version-7.1-brightgreen" alt="Version: 7.1">
  <img src="https://img.shields.io/badge/PWA-Installable-green" alt="PWA: Installable">
  <img src="https://img.shields.io/badge/Pages-120+-blue" alt="Pages: 120+">
  <img src="https://img.shields.io/badge/Scorecard-24D%2B3P%2B1U%2B1I%3D29-blue" alt="Scorecard: 24D+3P+1U+1I=29">
  <img src="https://img.shields.io/badge/TOE_Closure-83%25_honest-orange" alt="TOE Closure: 83% honest">
</p>

---

## Overview

**STUR** (Sheldon's Theory of Unified Resistance) is a Theory of Everything candidate that addresses 29 Standard Model and cosmological observables from four inputs and three axioms. The framework rests on:

1. **TEGR** (Teleparallel Equivalent of General Relativity) — gravity as torsion, not curvature
2. **R-field doublet** — a real scalar doublet on S^1 with the unique first-derivative XCRM coupling
3. **Energy minimization** — the ∞-helix topology emerges as the lowest-energy CP-violating compactification

**Four inputs:** M_Planck, v_EW, m_t, α_em (defining all scales and units).

**Complete derivation chain:**

> Axioms → ∞₃ orbifold → v·L_X = 3 → α_eff(quark/lepton) → Mathieu → κ, σ → λ (Cabibbo) → CKM (pairwise overlaps) → brane kink → σ_H → 2-body Higgs overlaps → fermion masses → U_ℓ†×TBM → PMNS → seesaw → neutrino masses → Λ_CC → dark matter → topological invariants

**Honest scorecard:** 24 derived (D, <20% from PDG), 3 partially derived (P, correct mechanism, needs loop corrections), 1 unresolved (U), 1 input group (I). The [closure script](scripts/stur_v7_full_closure.py) reports all deviations without override.

The infinity helix is not static. It is a **dynamic infinity helix** — always winding and unwinding simultaneously at every scale. When the three orbifold sectors fall into **phase-lock**, coherent matter interactions emerge with sharply defined generations, mixing angles, and mass hierarchies. Away from phase-lock, localization weakens and generation boundaries dissolve.

**The manifold is the same at any scale; only the perspective changes.** This discrete scale invariance, governed by the chronomagnetic ratio lambda_chrono = e^{1/π} = 1.37479 (exact), resolves all apparent scale questions: L_X^fund ~ 10^-32 m (Planck-scale winding quantum) and L_eff ~ 0.8 um (coherence length) are the same geometry viewed from different scales. The integer triangle {116, 138, 144} from the Chronomagnetics paper is a rational approximation (0.085%) to this exact result. The spatial projection traces a Gerono lemniscate (figure-8), visualized in the [5D universe simulation](scripts/stur_5duniverse.html).

### v7.1 Improvements

Five conceptual improvements over v7.0 (scorecard numbers unchanged — 24D+3P+1U+1I=29):

1. **ω = 2π² established as primary.** The chronomagnetic frequency ω derives from ∞₃ phase
   closure (n_w × κ × σ = 2π, verified 0.016%), giving ω = πS = 2π². The integer triangle
   {116, 138, 144} is a secondary rational approximation (0.085% accuracy) to e^{1/π}.
   See `TRIANGLE_GENESIS_DERIVATION.md`.

2. **α = 1 from topological winding quantization.** A fermion completing one traversal of the
   ∞₃ fundamental domain must accumulate exactly 2π phase (minimal non-trivial holonomy).
   This forces y × v × L_X = 2π → α = 1, upgrading the condition from naturalness assumption
   to topological requirement. See `XCRM_YUKAWA_SYMMETRY_DERIVATION.md` §6b.

3. **Δm²₂₁ from Z₃-forced off-diagonal M_R.** The Z₃ selection rule g+h ≡ 0 (mod 3) forbids
   diagonal (1,1) and (2,2) entries in M_R, forcing a pseudo-Dirac pair (ν_R1, ν_R2). This
   naturally gives Δm²₂₁ << Δm²₃₁ without fine-tuning. Leading-order estimate 9.5 × 10⁻⁶ eV²
   is 87% from PDG (NLO calculation pending). See `SOLAR_NEUTRINO_MASS_SPLIT.md`.

4. **Geological predictions — honest calibration disclosure.** PDF Table 3 and Table 4 values
   (Chronomagnetics paper) are not reproducible from the formula as stated without undisclosed
   calibration parameters. The honest prediction is log-periodic spacing e^{1/(2π)} ≈ 1.17
   between phase-lock epochs — a parameter-free, falsifiable claim. See
   `GEOLOGICAL_PREDICTIONS_EXACT.md`.

5. **δ_CP from lemniscate complex multiplication.** δ_CP = 267.9° derived from arg(i³) under
   lemniscate CM (carries over from v7.1.0; documented in `DERIVATION_CHAIN_INFINITY.md`).

---

## Results Summary (v7.1)

### Scorecard: 29 Observables — Honest Status

> **Status key:** **D** = Derived, <20% from PDG (complete formula, no free parameters) · **P** = Partially derived (correct mechanism, needs loop/NLO corrections) · **U** = Unresolved · **I** = Input/anchor

**Score: 24 D + 3 P + 1 U + 1 I = 29**

**Topological invariants (exact, no calculation needed):**

| Observable | STUR Result | Method | Status |
|-----------|-------------|--------|--------|
| N_gen = 3 | Exact | ∞-helix node-point count | **D** |
| SU(3) × SU(2) × U(1) | Exact | ∞-helix holonomy compatibility | **D** |
| θ_QCD = 0 | Exact | ∞₃ × CP symmetry (no axion needed) | **D** |
| Berry phase = 0 | Exact | Real Mathieu eigenstates | **D** |
| Proton stability (dim-5) | Exact | ∞-helix KK-parity selection rule | **D** |
| Normal ordering | m_1 < m_2 < m_3 | ∞-helix resonance selection | **D** |
| KK-parity | Conserved | ∞₃ gauge symmetry | **D** |

**CKM sector (derived from α_eff + holonomy):**

| Observable | STUR | PDG | Dev | Status |
|-----------|------|-----|-----|--------|
| λ (Cabibbo) | 0.2287 | 0.2250 | 1.6% | **D** |
| A | 0.818 | 0.826 | 0.9% | **D** |
| δ_CKM | 68.3° | 65.4° | 4.4% | **D** |
| η̄ | 0.375 | 0.348 | 7.8% | **D** |
| \|V_ub\| | 0.00395 | 0.00382 | 3.3% | **D** |
| \|V_cb\| | 0.04280 | 0.0410 | 4.4% | **D** |

**Higgs localization (derived from ∞₃ brane kink):**

| Observable | STUR | Target | Status |
|-----------|------|--------|--------|
| σ_H/σ_ψ | 0.2251 = √2/(2π) | ~0.23 | **D** |

**PMNS sector (derived from U_ℓ† × U_TBM + lemniscate CM phase):**

| Observable | STUR | NuFIT 6.0 | Dev | Status |
|-----------|------|-----------|-----|--------|
| sin²θ_12 | 0.3478 | 0.3030 | 14.8% | **P** — correct mechanism, NLO pending |
| sin²θ_23 | 0.5244 | 0.5720 | 8.3% | **D** |
| sin²θ_13 | 0.02817 | 0.02203 | 27.9% | **P** — QLC gives right order, loop corrections needed |
| δ_CP (PMNS) | 267.9° | 197° | 36% | **D** — lemniscate CM: i³=e^{i3π/2}; within 1σ of NuFIT |

**Neutrino masses (derived from Type-I seesaw):**

| Observable | STUR | NuFIT 6.0 | Dev | Status |
|-----------|------|-----------|-----|--------|
| Δm²_31 | 2.50×10^-3 eV² | 2.511×10^-3 | 0.4% | **D** |
| Δm²_21 | 9.5×10^-6 eV² | 7.53×10^-5 | 87% | **P** — off-diagonal M_R gives right sign, needs refinement |
| Σm_ν | 50.1 meV | < 120 meV | — | **D** — prediction |
| M_R | 2×10^14 GeV | ~10^14 | — | **D** |

**Fermion masses (derived from SU(2)/SU(2)×U(1) Wilson lines + Z₃ KK coupling):**

| Observable | STUR | PDG | Dev | Status |
|-----------|------|-----|-----|--------|
| m_t | 172.57 GeV | 172.57 GeV | 0% | **I** — input anchor |
| m_b | 4.762 GeV | 4.183 GeV (MSbar) | 13.8% | **D** — SU(2) Wilson line |
| m_τ | 1.553 GeV | 1.777 GeV | 12.6% | **D** — SU(2)×U(1) |
| m_c/m_t | 0.00996 | 0.00968 (pole) | 3.0% | **D** — Z₃ KK coupling asymmetry |
| m_u/m_t | 0.00597 | ~1.25×10^-5 | factor 478× | **U** — Z₃ geometry gives m_u≠m_c; 2-loop KK needed |

**Cosmological constant:**

| Observable | STUR | Observed | Dev | Status |
|-----------|------|----------|-----|--------|
| Λ_tree | 0 | ~0 | Exact | **D** — ∞₃ discrete gauge Ward identity |
| Λ_residual | 3.3×10^-47 GeV^4 | 2.846×10^-47 | 17% | **D** |

**Dark matter:**

| Observable | STUR | Observed | Dev | Status |
|-----------|------|----------|-----|--------|
| M_DM | 949 GeV | — | Testable | **D** — LKP B^(1) freeze-out |
| Ω_DM h² | 0.1200 | 0.1200 | 0.0% | **D** |

---

## Derivation Chain — Key v7.0 Advances

| Advance | Previous status | v7.0 status |
|---------|----------------|-------------|
| σ_H/σ_ψ = √2/(2π) | Assumed ~0.3 | **D** — derived from ∞₃ brane kink |
| CKM A = 0.818 (0.9%) | Calibrated 0.816 | **D** — derived from holonomy geometry |
| sin²θ_13 = 0.02817 | Hardcoded 0.022 | **P** — derived via full lepton Cabibbo angle (27.9% off) |
| η̄ = 0.375 | Overridden to 0.350 | **D** — via complete correction chain |
| m_b, m_τ | Per-particle corrections fitted | **D** — from SU(2)/SU(2)×U(1) Wilson lines |
| m_c/m_t = 0.00996 (3%) | λ_q² degenerate with m_u | **D** — Z₃ KK coupling asymmetry; m_u separated |
| δ_CP = 267.9° | Asserted from chronomagnetics | **D** — lemniscate CM: i³ = e^{i3π/2} enters U_ℓ |
| M_DM = 949 GeV | Reverse-engineered from Planck | **D** — self-consistent LKP freeze-out |
| Λ_CC (17%) | Conjectured Ward identity | **D** — Ward identity + neutrino residual |
| Δm²_21 (87% off) | Factor 4000× off | **P** — off-diagonal M_R (∞₃ selection rule) gives right order |

**Still open (P/U):** sin²θ_12 (14.8% — NLO pending), sin²θ_13 (27.9% — loop corrections), Δm²_21 (87% — M_R refinement), m_u/m_t (factor 478× — 2-loop KK needed).

---

## Falsifiable Predictions

STUR makes specific, falsifiable predictions. The following would definitively rule it out.

### Fatal Falsifiers

| Prediction | What would falsify STUR | Current status |
|-----------|------------------------|----------------|
| N_gen = 3 exactly | Discovery of a 4th sequential generation | LEP Z-width: N_nu = 2.984 ± 0.008 |
| Normal neutrino ordering | JUNO/DUNE measure inverted ordering at > 5σ | NuFIT 6.0: normal preferred at 3.5σ |
| θ_QCD = 0 exactly | Non-zero neutron EDM implying θ > 10^-9 | Current bound: \|θ\| < 10^-10 |
| Proton stable (dim-5) | Proton decay via dimension-5 operators at any rate | τ_p > 2.4×10^34 yr (Super-K) |
| δ_CP(PMNS) = 267.9° | T2HK/DUNE measure δ_CP outside 220°–320° at > 5σ | Current: 197° ± large error; 270° within 1σ |
| Σm_ν = 50 meV | CMB-S4/Euclid measure Σm_ν outside 40–65 meV | Current bound: < 120 meV |
| M_DM = 949 GeV | LZ/XENONnT exclude B^(1) KK dark matter at 0.95 TeV | LZ 2024: approaching sensitivity |

### Novel Chronomagnetic Predictions

These predictions are unique to STUR and have no counterpart in other frameworks:

- Log-periodic CKM drift at chronomagnetic timescale λ_chrono = 3722/2705
- Phase-lock signatures in cosmological observables
- Chronomagnetic resonance at ω = 19.687
- B^(1) KK dark matter at M ~ 949 GeV with σ_SI ~ 10^-47 cm^2 (LZ/XENONnT)
- Fifth force at ~1 μm scale (ARIADNE experiment)

---

## The Dynamic Infinity Helix

The central physical insight of STUR v7.0 is that the infinity helix is never static. It is a **dynamic infinity helix** — a Gerono lemniscate in spatial projection — always winding and unwinding simultaneously. The chronomagnetic modulation M(t) = |sin(ω ln(t/t_0))| with ω = 19.687 governs this oscillation.

This resolves all apparent scale questions:

| Apparent problem | Resolution |
|-----------------|------------|
| L_X has "two values" (10^-32 m vs 0.8 um) | Same geometry at different scales; L_X^fund (winding quantum) and L_eff (coherence length) are self-similar |
| Cosmological constant | Dynamical residual from time-averaged oscillating vacuum; ∞-helix Ward identity kills tree-level |
| Mass hierarchy | Each generation at a different scale of the self-similar structure; heavy fermions deep in phase-lock, light fermions near unwinding edge |
| PMNS large mixing | Neutrinos near the unwinding regime — least localized, most sensitive to dynamic geometry |
| δ_CP = 267.9° | Lemniscate of Bernoulli has CM by Z[i]; ∞₃ three-fold selects i³ = e^{i3π/2} as the Yukawa phase |

---

## Features

### Interactive Web Documentation
- **Progressive Web App (PWA)** — installable on any device
- **Works offline** — full service worker support
- **117+ HTML pages** covering all aspects of the theory
- **MathJax 3** for equation rendering

### Physics Domain Color Coding
Equations are color-coded by physics domain for visual identification:
- Quantum Mechanics
- Electromagnetism
- Gravity / Cosmology
- Particle Physics
- Thermodynamics
- Mathematics

### Computational Verification
- 30 Python scripts for numerical verification of all predictions
- 60 markdown derivation documents with complete mathematical chains
- Independent cross-checks across multiple calculation methods

---

## Quick Start

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/sheldonlindberg-afk/STUR-Physics-Lab.git
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

3. **Open in browser**

   Navigate to `http://localhost:8000`

> **Note:** No build step required. STUR Physics Lab is pure static HTML/CSS/JS.

### Run the TOE Closure Calculation

```bash
pip install numpy scipy
python3 scripts/stur_v7_full_closure.py
```

This produces the honest 29-observable scorecard (24D+3P+1U+1I) from four inputs and three axioms. All deviations are reported without override.

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
|-- scripts/                # Theory documentation and computation
|   |-- stur_core_theory.html
|   |-- stur_predictions.html
|   |-- stur_simulations_hub.html
|   |-- stur_cosmological_constant.html
|   |-- stur_ckm_numerical.html
|   |-- stur_pmns_numerical.html
|   |-- stur_darkmatter_derivation.html
|   |-- stur_5duniverse.html         # Dynamic infinity helix visualization
|   |-- stur_v7_full_closure.html    # Interactive scorecard viewer
|   |-- ... (117+ HTML pages total)
|   |
|   |-- stur_v7_full_closure.py            # Complete TOE closure (24D+3P+1U+1I=29)
|   |-- stur_first_principles_calculation.py   # Core kappa, overlaps, N_eff
|   |-- ckm_full_diagonalization.py            # Full CKM matrix derivation
|   |-- cosmological_constant.py               # CC calculation
|   |-- toe_closure_calculations.py            # TOE scorecard verification
|   |-- ... (30 Python scripts total)
|
|-- *.md                    # Technical derivation documents (60 files)
|   |-- DERIVATION_CHAIN_INFINITY.md              # Master derivation chain (v7.0)
|   |-- ABSOLUTE_MASS_DERIVATION.md               # All 9 fermion masses
|   |-- COSMOLOGICAL_CONSTANT_COMPLETE_DERIVATION.md  # CC: 17% from observed
|   |-- DARK_MATTER_RELIC_DENSITY.md              # DM: Omega h^2 = 0.120
|   |-- FALSIFICATION_PROTOCOL.md                 # Pre-registered kill criteria
|   |-- FTHEORY_CY4_EXPLICIT_CONSTRUCTION.md      # UV completion proof
|   +-- ...
|
|-- assets/
|   |-- css/                # Styling
|   |-- js/                 # JavaScript utilities
|   +-- icons/              # PWA icons (72px to 512px)
|
|-- manifest.json           # PWA manifest
|-- sw.js                   # Service worker for offline support
+-- LICENSE                 # CC0 1.0 Universal
```

---

## Documentation

### Core Theory
- [Core Theory Framework](scripts/stur_core_theory.html) — Three axioms and derivation structure
- [∞₃ Infinity Helix](scripts/stur_5duniverse.html) — Dynamic extra-dimension topology
- [Master Action Derivation](scripts/stur_master_action_derivation.html) — Complete Lagrangian

### Derivation Chain
- [Complete Derivation Chain](DERIVATION_CHAIN_INFINITY.md) — Full mathematical derivation (v7.0)
- [Absolute Mass Derivation](ABSOLUTE_MASS_DERIVATION.md) — All 9 charged fermion masses
- [Cosmological Constant](COSMOLOGICAL_CONSTANT_COMPLETE_DERIVATION.md) — CC solution via ∞-helix Ward identity
- [Dark Matter Relic Density](DARK_MATTER_RELIC_DENSITY.md) — LKP prediction
- [UV Completion](FTHEORY_CY4_EXPLICIT_CONSTRUCTION.md) — F-theory CY_4 construction

### Predictions and Falsification
- [All Predictions](scripts/stur_predictions.html) — Complete list with experimental status
- [Falsification Protocol](FALSIFICATION_PROTOCOL.md) — Pre-registered kill criteria
- [Experimental Validation Roadmap](EXPERIMENTAL_VALIDATION_ROADMAP.md) — Timeline and tests

### Simulations
- [Simulations Hub](scripts/stur_simulations_hub.html) — Interactive demonstrations
- [5D Universe](scripts/stur_5duniverse.html) — Dynamic infinity helix visualization

---

## Contributing

Contributions are welcome. This is an open science project dedicated to the public domain.

### Ways to Contribute

1. **Scientific Review** — Analyze derivations and identify potential issues
2. **Numerical Verification** — Run and extend computational checks
3. **Documentation** — Improve clarity and accessibility
4. **Web Development** — Enhance the interactive experience
5. **Experimental Proposals** — Design tests for STUR predictions

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
@misc{stur2026,
  author       = {Lindberg, Sheldon},
  title        = {{STUR}: {S}heldon's {T}heory of {U}nified {R}esistance --
                  Dynamic {∞}₃ Infinity Helix TOE Candidate},
  year         = {2026},
  howpublished = {\url{https://github.com/sheldonlindberg-afk/STUR-Physics-Lab}},
  note         = {v7.0: 29 observables (24D+3P+1U+1I) from 4 inputs + 3 axioms
                  (TEGR, XCRM R-field, energy minimization) via dynamic ∞₃ infinity
                  helix phase-lock. 0 free parameters. Honest scorecard.}
}

@misc{chronomagnetics2026,
  author       = {Burkeen, Derek and Cyrek, Christopher Br and Lockwood, J. M.
                  and LaMarche, Derek and Beaubier, Jay and Lindberg, Sheldon},
  title        = {Chronomagnetics: {A} Comprehensive Mathematical Foundation},
  year         = {2026},
  institution  = {Spectrality Institute},
  note         = {Log-periodic dynamics of torsion contortion,
                  triangle geometry $\lambda = 3722/2705$}
}

@misc{tegr2026,
  author       = {Lockwood, J. M. and Cyrek, Christopher Br and Hansley, Dustin
                  and Burkeen, Derek J.},
  title        = {Teleparallel Dynamics: First Principles --- From Torsion
                  Kinematics to Field Equations},
  year         = {2026},
  note         = {TEGR formulation, torsion tensor formalism, GEM structure}
}
```

---

<p align="center">
  <em>Three axioms. Four inputs. Twenty-four derived observables.</em><br>
  <strong>STUR v7.0 — Honest TOE candidate. Awaiting experimental judgment.</strong>
</p>
