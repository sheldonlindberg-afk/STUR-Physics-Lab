/**
 * STUR Unified Definitions Layer
 * ===============================
 * Canonical symbols, units, constants, and mappings for the STUR Physics Lab.
 * All pages should reference this single source of truth.
 *
 * @version 1.0.0
 * @author Sheldon Lon Lindberg
 */

const STUR_DEFINITIONS = {
  version: "9.2",

  // ============================================================
  // CORE CONSTANTS
  // ============================================================
  constants: {
    // Fundamental
    hbar: { value: 1.054571817e-34, unit: "J·s", name: "Reduced Planck constant" },
    c: { value: 299792458, unit: "m/s", name: "Speed of light" },
    G: { value: 6.67430e-11, unit: "m³/(kg·s²)", name: "Gravitational constant" },
    e: { value: 1.602176634e-19, unit: "C", name: "Elementary charge" },
    m_e: { value: 9.1093837015e-31, unit: "kg", name: "Electron mass" },
    epsilon_0: { value: 8.8541878128e-12, unit: "F/m", name: "Vacuum permittivity" },
    k_B: { value: 1.380649e-23, unit: "J/K", name: "Boltzmann constant" },

    // Derived Planck units
    l_P: { value: 1.616255e-35, unit: "m", name: "Planck length" },
    t_P: { value: 5.391247e-44, unit: "s", name: "Planck time" },
    m_P: { value: 2.176434e-8, unit: "kg", name: "Planck mass" },

    // STUR-specific
    alpha_fine: { value: 1/137.035999084, unit: "1", name: "Fine structure constant" },
    a_0: { value: 5.29177210903e-11, unit: "m", name: "Bohr radius" },

    // Chronomagnetics
    lambda_chrono: { value: 3722/2705, unit: "1", name: "Chronomagnetic ratio", approx: 1.376 },
    triangle_chrono: { a: 116, b: 138, c: 144, name: "Illustrative triangle" }
  },

  // ============================================================
  // CANONICAL SYMBOLS
  // ============================================================
  symbols: {
    // Primary field
    R: { latex: "R", name: "Resistance field", unit: "1", description: "Scalar resistance field R(x,t,X)" },
    R_bg: { latex: "R_{\\rm bg}", name: "Background resistance", unit: "1" },
    sigma_R: { latex: "\\sigma_R", name: "RMS resistance fluctuation", unit: "1" },

    // Coherence
    ell_coh: { latex: "\\ell_{\\rm coh}", name: "Coherence length", unit: "m" },
    L_X: { latex: "L_X", name: "X-dimension compactification scale", unit: "m" },

    // Holonomy
    Phi_R: { latex: "\\Phi_R", name: "Resistance holonomy", unit: "rad" },
    J_a: { latex: "\\mathsf{J}_a", name: "Holonomy current", unit: "m⁻¹" },

    // Visibility
    V: { latex: "V", name: "Visibility", unit: "1" },
    V_0: { latex: "V_0", name: "Maximum visibility", unit: "1" },
    Delta_L: { latex: "\\Delta L", name: "Arm separation", unit: "m" },

    // TEGR
    e_mu: { latex: "e^a{}_{\\mu}", name: "Tetrad/vierbein", unit: "1" },
    T_tensor: { latex: "T^a{}_{\\mu\\nu}", name: "Torsion tensor", unit: "m⁻¹" },
    K_tensor: { latex: "K^a{}_{bc}", name: "Contortion tensor", unit: "m⁻¹" },
    K_eff: { latex: "K_{\\rm eff}", name: "Effective contortion", unit: "m⁻¹" },
    T_scalar: { latex: "\\mathbb{T}", name: "Torsion scalar", unit: "m⁻²" },

    // Action terms
    D: { latex: "D", name: "Diffusion coefficient", unit: "m²/s" },
    chi: { latex: "\\chi", name: "XCRM coupling", unit: "1" },
    alpha: { latex: "\\alpha", name: "Torsion coupling", unit: "1" },
    Gamma: { latex: "\\Gamma", name: "Relaxation rate", unit: "s⁻¹" },

    // Chronomagnetics
    lambda: { latex: "\\lambda", name: "Log-periodic constant", unit: "1" },
    u_t: { latex: "u(t)", name: "Log-time coordinate", unit: "1" },
    M_u: { latex: "\\mathcal{M}(u)", name: "Modulation function", unit: "1" }
  },

  // ============================================================
  // FIRST PRINCIPLES (v9.2+)
  // ============================================================
  firstPrinciples: {
    statement: "STUR makes exactly one adjustable prediction—the coherence length ℓ_coh. Given any two of {χ, L_X, ℓ_coh}, the third is determined. The form of the visibility law V(ΔL) = V₀ exp(-ΔL²/ℓ²_coh) is not adjustable—it follows from Gaussian phase averaging of the XCRM holonomy.",

    singleParameter: "ℓ_coh",

    closureRelation: {
      formula: "ℓ_coh = √2 · L_X / σ_R",
      latex: "\\ell_{\\rm coh} = \\frac{\\sqrt{2}\\, L_X}{\\sigma_R}",
      variables: ["χ", "L_X", "ℓ_coh"],
      note: "Given any two, the third is determined"
    },

    nonNegotiable: {
      form: "Gaussian in ΔL²",
      formula: "V(ΔL) = V₀ exp(-ΔL²/ℓ²_coh)",
      latex: "V(\\Delta L) = V_0 \\exp\\!\\left(-\\frac{\\Delta L^2}{\\ell_{\\rm coh}^2}\\right)",
      derivedFrom: [
        "XCRM closure: ∂_X R = (R - R_bg)/L_X",
        "Central limit theorem (many uncorrelated phases)",
        "Holonomy-visibility relation: V = V₀ exp(-⟨Φ_R²⟩/2)"
      ]
    },

    falsifiedIf: [
      "Visibility is oscillatory (sinusoidal)",
      "Visibility depends on time (not just ΔL)",
      "Visibility depends on particle mass at fixed shot time",
      "Functional form deviates from Gaussian in ΔL²"
    ]
  },

  // ============================================================
  // CORE EQUATIONS (LaTeX)
  // ============================================================
  equations: {
    // The Master Action
    master_action: {
      id: "0.1",
      name: "The Unified Resistance Action",
      latex: "S_{\\rm STUR}[R, g, X] = \\int_{\\mathcal{M}^5} d^4x\\, dX\\, \\sqrt{-g}\\, \\Big[\\underbrace{\\color{#4ade80}{\\tfrac{1}{2}(\\nabla R)^2}}_{\\text{diffusion}} - \\underbrace{\\color{#f472b6}{V(R)}}_{\\text{relaxation}} + \\underbrace{\\color{#fbbf24}{\\chi\\, R\\,\\partial_X R}}_{\\text{XCRM}} + \\underbrace{\\color{#60a5fa}{\\alpha\\, R\\, \\mathbb{T}}}_{\\text{torsion}} + \\color{#22d3ee}{\\mathcal{L}_{\\rm matter}}\\Big]",
      tier: "core"
    },

    // First Principles closure
    parameter_closure: {
      id: "FP.1",
      name: "Parameter Closure Relation",
      latex: "\\color{#22d3ee}{\\ell_{\\rm coh}} = \\frac{\\sqrt{2}\\, \\color{#fbbf24}{L_X}}{\\color{#4ade80}{\\sigma_R}}",
      tier: "core",
      note: "Given any two of {χ, L_X, ℓ_coh}, the third is determined"
    },

    // Visibility (THE falsifiable prediction - NON-NEGOTIABLE FORM)
    visibility_gaussian: {
      id: "FP.2",
      name: "Non-Negotiable Visibility Law",
      latex: "\\color{#f472b6}{V(\\Delta L)} = V_0 \\exp\\!\\left(-\\frac{(\\color{#fb923c}{\\Delta L})^2}{\\color{#22d3ee}{\\ell_{\\rm coh}}^2}\\right)",
      tier: "falsifiable",
      is_primary_prediction: true,
      is_non_negotiable: true,
      note: "Form follows from Gaussian phase averaging—NOT adjustable"
    },

    // Coherence length (closure)
    coherence_length: {
      id: "5.3",
      name: "Coherence Length Closure",
      latex: "\\color{#22d3ee}{\\ell_{\\rm coh}} = \\frac{\\sqrt{2}\\, \\color{#fbbf24}{L_X}}{\\color{#4ade80}{\\sigma_R}}",
      tier: "core"
    },

    // Holonomy
    holonomy: {
      id: "5.1",
      name: "Resistance Holonomy",
      latex: "\\color{#c4b5fd}{\\Phi_R} = \\color{#c4b5fd}{\\oint_{\\mathcal{C}}} \\color{#fbbf24}{\\mathsf{J}_a}\\, dx^a",
      tier: "core"
    },

    // TEGR equivalence
    tegr_equivalence: {
      id: "3.2",
      name: "TEGR ≡ GR Equivalence",
      latex: "S_{\\rm TEGR} = \\frac{1}{16\\pi G} \\int d^4x\\, e\\, T = S_{\\rm EH} + \\text{boundary term}",
      tier: "core"
    },

    // Emergent 4D equation
    emergent_4d: {
      id: "3.4.7",
      name: "Emergent 4D Equation",
      latex: "\\partial_t \\bar R = \\color{#4ade80}{D\\nabla^2 \\bar R} \\color{#94a3b8}{-} \\color{#f472b6}{\\Gamma(\\bar R - R_{\\rm bg})} \\color{#94a3b8}{+} \\color{#22d3ee}{\\xi}",
      tier: "derived"
    },

    // Loop enhancement
    loop_enhancement: {
      id: "5.5",
      name: "Loop Enhancement (Area Scaling)",
      latex: "\\color{#c4b5fd}{\\langle \\Phi_R^2 \\rangle_{\\rm loop}} \\approx \\frac{\\color{#4ade80}{\\sigma_R^2}}{\\color{#fbbf24}{L_X^2}}\\, \\color{#fb923c}{A_{\\rm loop}}",
      tier: "derived"
    },

    // Chronomagnetics
    chrono_modulation: {
      id: "6.2",
      name: "Log-Periodic Modulation",
      latex: "\\color{#f472b6}{\\mathcal{M}(u)} = 1 + \\epsilon \\cos(2\\pi u / \\ln\\color{#fbbf24}{\\lambda}), \\quad \\color{#22d3ee}{u(t)} = \\ln\\big((t + t_c)/t_0\\big)",
      tier: "cosmological"
    }
  },

  // ============================================================
  // FALSIFICATION CRITERIA
  // ============================================================
  falsification: {
    // Primary discriminators
    stur_signature: {
      type: "Gaussian in ΔL²",
      scaling: "exp(−(ΔL/ℓ_coh)²)",
      control_variable: "Arm separation ΔL"
    },

    null_models: {
      collisional_decoherence: {
        type: "Exponential in time",
        scaling: "exp(−Γt)",
        control_variable: "Time, pressure"
      },
      uldm_coherent: {
        type: "Oscillatory",
        scaling: "cos(ωt)",
        control_variable: "Frequency"
      },
      standard_qm: {
        type: "No suppression",
        scaling: "V = V_0 (constant)",
        control_variable: "None"
      }
    },

    // Statistical thresholds
    frequentist: {
      threshold: "5σ",
      method: "Fit Gaussian vs null model"
    },
    bayesian: {
      decisive_support: 5,
      decisive_exclusion: -5,
      scale: "Jeffreys (Δln𝒵)"
    },

    // Falsification conditions
    falsified_if: [
      "Visibility shows oscillatory (sinusoidal) behavior",
      "Time-dependent suppression instead of ΔL-dependent",
      "Mass-dependent effects at fixed shot time",
      "Non-Gaussian functional form"
    ]
  },

  // ============================================================
  // EXPERIMENTAL PLATFORMS
  // ============================================================
  platforms: {
    magis_100: { baseline: "~100 m", test: "Long-baseline ΔL scan" },
    aion: { baseline: "~10–100 m", test: "Multi-baseline visibility" },
    sagnac_loops: { baseline: "~1–10 m", test: "Loop holonomy at ΔL = 0" },
    neutron_interferometry: { baseline: "~0.1 m", test: "Different systematics" }
  },

  // ============================================================
  // TIER COLORS (for title and section styling)
  // ============================================================
  tiers: {
    core: { color: "#4ade80", name: "Core Theory", class: "page-title-core" },
    falsifiable: { color: "#22d3ee", name: "Falsifiable", class: "page-title-falsifiable" },
    derived: { color: "#fbbf24", name: "Derived", class: "page-title-derived" },
    cosmological: { color: "#a78bfa", name: "Cosmological", class: "page-title-cosmological" },
    biological: { color: "#f472b6", name: "Biological", class: "page-title-biological" },
    exploratory: { color: "#64748b", name: "Exploratory", class: "page-title-exploratory" }
  },

  // ============================================================
  // EQUATION TERM COLORS
  // ============================================================
  termColors: {
    diffusion: { color: "#4ade80", name: "Diffusion", role: "Kinetic" },
    potential: { color: "#f472b6", name: "Potential", role: "Relaxation" },
    xcrm: { color: "#fbbf24", name: "XCRM", role: "X-Coupling" },
    torsion: { color: "#60a5fa", name: "Torsion", role: "Gravity" },
    matter: { color: "#22d3ee", name: "Matter", role: "Fields" },
    quantum: { color: "#a78bfa", name: "Quantum", role: "Loop corrections" },
    integral: { color: "#c4b5fd", name: "Integral", role: "Holonomy" },
    metric: { color: "#fb923c", name: "Metric", role: "Geometry" }
  }
};

/**
 * Helper function to render equation with color coding
 */
STUR_DEFINITIONS.renderEquation = function(eqId) {
  const eq = this.equations[eqId];
  if (!eq) return null;
  return {
    latex: eq.latex,
    label: `(${eq.id}) — ${eq.name}`,
    tier: eq.tier
  };
};

/**
 * Generate falsification harness HTML for a page
 */
STUR_DEFINITIONS.generateFalsificationHarness = function(config) {
  const { observable, nullModel, sturPrediction, metric, units } = config;
  return `
<div class="falsification-harness">
  <div class="harness-section">
    <h4>Observable</h4>
    <p>${observable}</p>
  </div>
  <div class="harness-section">
    <h4>Null Model (Standard Physics)</h4>
    <p>${nullModel}</p>
  </div>
  <div class="harness-section">
    <h4>STUR Prediction</h4>
    <p>${sturPrediction}</p>
  </div>
  <div class="harness-section">
    <h4>Falsification Metric</h4>
    <p>${metric} (${units})</p>
  </div>
</div>
  `;
};

/**
 * Export for use in pages
 */
if (typeof window !== 'undefined') {
  window.STUR_DEFINITIONS = STUR_DEFINITIONS;
}

if (typeof module !== 'undefined' && module.exports) {
  module.exports = STUR_DEFINITIONS;
}
