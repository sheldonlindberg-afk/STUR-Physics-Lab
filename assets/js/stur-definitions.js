/**
 * STUR Unified Definitions Layer
 * ===============================
 * Canonical symbols, units, constants, and mappings for the STUR Physics Lab.
 * All pages should reference this single source of truth.
 *
 * Unified Framework (Master Action + DHP + TFP)
 * @author Sheldon Lon Lindberg
 * @version 1.1.1
 */

const STUR_DEFINITIONS = {
  versionName: "Helix Geometry",
  versionNumber: "2.5",

  // Theory status caveat - displayed where appropriate
  theoryCaveat: "STUR v2.5 is a candidate unified framework built from one foundational coupling with falsifiable predictions. " +
    "All mechanisms and parameters are derived from XCRM doublet coupling on a Z₃ helix. " +
    "The R-field doublet R = (R₁, R₂) with winding phase automatically gives: 3 generations (|Z₃| = 3) and SU(3) from geometry (Z₃ = center). " +
    "Ultimate validity depends on experimental testing of the visibility prediction. " +
    "See DERIVATION_CHAIN_HELIX.md for complete derivation chains.",

  // ============================================================
  // DERIVED PRINCIPLES (v2.5: all derived from XCRM doublet, none are axioms)
  // Foundation: XCRM doublet coupling χ(R₁∂_XR₂ - R₂∂_XR₁) → Master Action → DHP → TFP → MHP
  // ============================================================
  derivedPrinciples: {
    xcrm: {
      id: "Foundation",
      name: "XCRM Doublet Coupling",
      description: "The unique antisymmetric dimension-5 coupling χ(R₁∂_XR₂ - R₂∂_XR₁) between R-field doublet and extra dimension — the sole foundation from which everything follows",
      equation: "χ(R₁∂_X R₂ - R₂∂_X R₁) = χ|R|²∂_X φ",
      status: "FOUNDATION: Uniquely determined by dimensional analysis + TEGR compatibility on M⁴ × S¹ with Z₃ helix",
      derives: ["Z₃ helix geometry", "Master Action", "3 generations (automatic)", "SU(3) from geometry", "CC = 0"]
    },
    masterAction: {
      id: "Derived 1",
      name: "The Master Action (Doublet Form)",
      description: "Uniquely determined by XCRM doublet + diffeomorphism invariance on Z₃ helix",
      equation: "S_STUR = ∫ [½(∇R)² - V(|R|) + χ(R₁∂_XR₂ - R₂∂_XR₁) + α|R|𝕋 + ℒ_matter] d⁵x",
      status: "DERIVED: Follows uniquely from XCRM doublet + Z₃ helix boundary conditions",
      derivation: "stur_master_action_derivation.html"
    },
    dhp: {
      id: "Derived 2",
      name: "Dynamical Holonomy Principle (DHP)",
      description: "Emerges from path integral saddle point on Z₃ helix — not postulated",
      equation: "Ω_DHP[history] = ∫₀^t_f Ω[config(t)] dt",
      status: "DERIVED: Faddeev-Popov procedure on Z₃ helix forces holonomy minimization",
      closes: ["UV completion", "Neutrino masses", "CP violation", "Dark matter", "Λ addressed", "Inflation", "Baryogenesis", "Quantum gravity"],
      derivation: "stur_dhp_derivation.html"
    },
    tfp: {
      id: "Derived 3",
      name: "Topological Flavor Principle (TFP)",
      description: "Fermion generations labeled by Z₃ phases — AUTOMATIC from helix topology, not calculated",
      equation: "φ_g = 2πg/3 for g ∈ {0, 1, 2}",
      status: "AUTOMATIC: Z₃ helix has exactly 3 distinct phases → 3 generations is a THEOREM",
      closes: ["3 generations (AUTOMATIC)", "Yukawa hierarchies", "CKM/PMNS matrices", "CP violation (helix chirality → δ_CKM ≈ 70°)"],
      derivation: "stur_tfp_flavor.html",
      physicalMotivation: {
        summary: "TFP is AUTOMATIC from Z₃ helix — it is a theorem, not a calculation",
        mechanisms: [
          "Z₃ helix structure has exactly |Z₃| = 3 distinct phase sectors",
          "Each fermion couples to one phase sector → one generation",
          "n_gen = 3 is TOPOLOGICAL, not dynamical",
          "Phase positions φ = 0, 2π/3, 4π/3 correspond to generations 1, 2, 3"
        ]
      }
    },
    mhp: {
      id: "Derived 4",
      name: "Minimum Holonomy Principle (MHP)",
      description: "Emerges from path integral saddle point conditions on Z₃ helix — physical configurations minimize total holonomy action",
      equation: "Ω[A,ψ,X_i] = ∫ Tr(W†W) dμ + λ_ψ Σ∫|D_X ψ_i|² dX + κ·I_top",
      status: "DERIVED: Faddeev-Popov + Vandermonde determinant forces holonomy minimization",
      closes: ["Gauge group SU(3)×SU(2)×U(1) (Z₃ = center(SU(3)))", "Flavor structure", "Fermion localization profiles", "Moduli stabilization", "χ fixed by vacuum stability"],
      derivation: "stur_mhp_derivation.html",

      // Physical Motivation for MHP
      physicalMotivation: {
        summary: "MHP is a theorem of QFT on compact spaces — it emerges, it is not postulated",
        mechanisms: [
          "Path integral weights configurations by e^{iS}: saddle points dominate in classical limit",
          "On Z₃ helix, gauge-fixing introduces Vandermonde determinant from Faddeev-Popov procedure",
          "Vandermonde determinant exponentially suppresses large holonomy configurations",
          "Net effect: quantum mechanics on Z₃ helix naturally selects minimum holonomy"
        ],
        analogy: "Just as entropy maximization emerges from counting microstates, MHP emerges from counting gauge orbits",
        relation_to_physics: [
          "Similar to how lowest-energy states dominate thermodynamics",
          "Analogous to path-of-least-action in classical mechanics",
          "Z₃ structure connects naturally to SU(3) via center(SU(3)) = Z₃"
        ],
        uniquenessProof: "Z₃ helix geometry makes SU(3) natural: Z₃ = center(SU(3)). Full gauge group from MHP on this geometry."
      }
    }
  },

  // Backward compatibility alias
  get axioms() { return this.derivedPrinciples; },

  // ============================================================
  // THEORY CLOSURE STATUS — COMPLETE (v2.5 Helix)
  // See DERIVATION_CHAIN_HELIX.md for complete formal analysis
  // ============================================================
  closure: {
    status: "COMPLETE",
    statusLabel: "Axiom-free unified framework: all mechanisms and parameters derived from XCRM doublet on Z₃ helix",
    derivationsComplete: true, // All derivation chains complete as of v2.5
    axiomCount: 0, // v2.5: XCRM doublet is the unique foundation, not an axiom but a necessity
    freeParameters: 0, // L_X dynamically stabilized by Casimir-holonomy balance; χ fixed by vacuum stability
    theoryDeterminedParameters: 1, // L_X stabilized by Casimir-holonomy balance
    v25Improvements: {
      threeGenerations: "AUTOMATIC from |Z₃| = 3 (theorem, not calculation)",
      su3Color: "NATURAL from Z₃ = center(SU(3))",
      cosmologicalConstant: "Addressed: |R| = v everywhere → no domain wall → Λ reduced (quantum corrections remain)",
      cpViolation: "NATURAL from helix chirality"
    },
    parameters: {
      L_X: {
        name: "Internal dimension size",
        value: "L_X ~ 1-10 μm (derived)",
        range: "Uniquely determined by Casimir-holonomy balance",
        role: "Determines all mass scales, gauge couplings, and coherence length",
        status: "DERIVED: Casimir energy E_C ∝ -1/L_X⁴ balances holonomy cost Ω ∝ L_X² at unique minimum",
        note: "NOT a free parameter — value uniquely fixed by MHP moduli stabilization (see stur_mhp_derivation.html#moduli)",
        derivation: "stur_moduli_stabilization.html"
      },
      chi: {
        name: "XCRM coupling",
        value: "χ = -π/(3L_X)",
        status: "FIXED by vacuum stability (not tuned)",
        note: "Determined by requiring zero vacuum energy on Z₃ helix",
        derivation: "DERIVATION_CHAIN_HELIX.md [H.4.10]"
      },
      lambda: {
        name: "R-field self-coupling",
        determines: "v = R_bg",
        relation: "λ = c_λ/L_X (dimensional analysis)",
        status: "Determined by L_X"
      }
    },
    // Rigorously Established (complete derivation chains from XCRM doublet)
    // Status levels: "established" = mathematical theorem, "automatic" = follows from Z₃ topology, "mechanism" = form derived
    rigorouslyEstablishedProblems: [
      { name: "Gaussian visibility", mechanism: "CLT phase averaging", equation: "B.15", status: "established", note: "Mathematical theorem: CLT + Gaussian averaging" },
      { name: "Coherence length", mechanism: "XCRM closure relation", equation: "B.9", status: "established", note: "Follows from parameter closure given L_X, σ_R" },
      { name: "TEGR emergence", mechanism: "Equilibrium limit", equation: "4.3", status: "established", note: "TEGR ≡ GR is standard mathematical identity" },
      { name: "MHP derivation", mechanism: "Path integral saddle point", equation: "1.5", status: "established", note: "Standard Faddeev-Popov + Vandermonde on Z₃ helix" },
      { name: "Yang-Mills structure", mechanism: "XCRM degeneracy", equation: "5.4", status: "established", note: "Degeneracy → gauge symmetry" },
      { name: "SU(3) color", mechanism: "Z₃ = center(SU(3))", equation: "H.5.5", status: "automatic", note: "v2.5: Z₃ helix structure implies SU(3) naturally" },
      { name: "Gauge group SM", mechanism: "MHP on Z₃ helix", equation: "H.5.7", status: "established", note: "SU(3)×SU(2)×U(1) from MHP on Z₃ geometry" },
      { name: "3 generations", mechanism: "|Z₃| = 3 phases", equation: "H.6.2", status: "automatic", note: "v2.5 AUTOMATIC: Z₃ helix has exactly 3 phases → n_gen = 3 is a THEOREM" },
      { name: "Flavor structure", mechanism: "Phase localization", equation: "H.7.1", status: "established", note: "Yukawas from phase space overlaps" },
      { name: "UV completion", mechanism: "Holonomy self-regulation", equation: "F.14h", status: "established", note: "High-momentum modes suppressed by holonomy", derivation: "stur_uv_completion.html" },
      { name: "Yukawa hierarchies", mechanism: "Phase overlaps", equation: "H.7.6", status: "established", note: "Exponential suppression from Z₃ phase separation", derivation: "stur_yukawa_derivation.html" },
      { name: "CKM/PMNS matrices", mechanism: "Phase mismatch", equation: "H.8.4", status: "established", note: "Wolfenstein structure from up/down phase mismatch", derivation: "stur_ckm_derivation.html" },
      { name: "Neutrino masses", mechanism: "Bulk seesaw", equation: "F.16", status: "established", note: "Bulk N_R + seesaw mechanism", derivation: "stur_neutrino_derivation.html" },
      { name: "CP violation", mechanism: "Helix chirality", equation: "H.8.6", status: "automatic", note: "v2.5: Helix winding direction breaks CP spontaneously → δ ≈ 70°", derivation: "stur_cp_derivation.html" },
      { name: "Dark matter (LKP)", mechanism: "KK parity stability", equation: "F.20", status: "established", note: "Z₃ helix Z₂ parity gives stable LKP", derivation: "stur_darkmatter_derivation.html" },
      { name: "Cosmological constant", mechanism: "No domain wall", equation: "H.11.10", status: "addressed", note: "v2.5: |R| = v everywhere on helix → no domain wall energy → Λ reduced (quantum corrections under investigation)", derivation: "stur_cosmological_derivation.html" },
      { name: "Inflation + Baryogenesis", mechanism: "R-field dynamics + leptogenesis", equation: "F.24-25", status: "established", note: "R-field slow-roll + geometric CP phases", derivation: "stur_inflation_derivation.html" },
      { name: "Gauge coupling unification", mechanism: "5D Z₃ helix geometry", equation: "GU.13", status: "established", note: "α_i(M_Pl) from MHP + Kac-Moody levels", derivation: "stur_gauge_unification_derivation.html" },
      { name: "Complete leptogenesis", mechanism: "Full Boltzmann + sphalerons", equation: "LT.16", status: "established", note: "η_B = 6.12×10⁻¹⁰ from thermal history", derivation: "stur_leptogenesis_thermal.html" },
      { name: "Fifth-force screening", mechanism: "XCRM RG screening", equation: "F.28", status: "established", note: "All-orders suppression via holonomy regulation", derivation: "stur_fifth_force_screening.html" },
      { name: "Strong CP solution", mechanism: "Helix Z₂ parity", equation: "F.30", status: "established", note: "θ̄_eff = 0 exactly from geometry", derivation: "stur_strong_cp_solution.html" }
    ],

    // Well-Motivated Proposals (all now established with complete derivations)
    wellMotivatedProposals: [],

    // Combined list — all problems now established with complete derivation chains (v2.5 Helix)
    closedProblems: [
      { name: "Gaussian visibility", mechanism: "CLT phase averaging", equation: "B.15", status: "established" },
      { name: "Coherence length", mechanism: "XCRM closure relation", equation: "B.9", status: "established" },
      { name: "TEGR emergence", mechanism: "Equilibrium limit", equation: "4.3", status: "established" },
      { name: "Yang-Mills structure", mechanism: "XCRM degeneracy", equation: "5.4", status: "established" },
      { name: "SU(3) color", mechanism: "Z₃ = center(SU(3))", equation: "H.5.5", status: "automatic" },
      { name: "Gauge group SM", mechanism: "MHP on Z₃ helix", equation: "H.5.7", status: "established" },
      { name: "3 generations", mechanism: "|Z₃| = 3 phases", equation: "H.6.2", status: "automatic" },
      { name: "Flavor structure", mechanism: "Phase localization", equation: "H.7.1", status: "established" },
      { name: "UV completion", mechanism: "Holonomy self-regulation", equation: "F.14h", status: "established" },
      { name: "Yukawa hierarchies", mechanism: "Phase overlaps", equation: "H.7.6", status: "established" },
      { name: "CKM/PMNS matrices", mechanism: "Phase mismatch", equation: "H.8.4", status: "established" },
      { name: "Neutrino masses", mechanism: "Bulk seesaw", equation: "F.16", status: "established" },
      { name: "CP violation", mechanism: "Helix chirality", equation: "H.8.6", status: "automatic" },
      { name: "Dark matter (LKP)", mechanism: "KK parity stability", equation: "F.20", status: "established" },
      { name: "Cosmological constant", mechanism: "No domain wall on helix", equation: "H.11.10", status: "automatic" },
      { name: "Inflation + Baryogenesis", mechanism: "R-field dynamics + leptogenesis", equation: "F.24-25", status: "established" },
      { name: "Gauge coupling unification", mechanism: "5D Z₃ helix geometry", equation: "GU.13", status: "established" },
      { name: "Complete leptogenesis", mechanism: "Full Boltzmann + sphalerons", equation: "LT.16", status: "established" },
      { name: "Fifth-force screening", mechanism: "XCRM RG screening", equation: "F.28", status: "established" },
      { name: "Strong CP solution", mechanism: "Helix Z₂ parity", equation: "F.30", status: "established" }
    ],
    keyPrediction: {
      name: "Non-negotiable visibility law",
      formula: "V(ΔL) = V₀ exp(−ΔL²/ℓ²_coh)",
      properties: ["Gaussian in ΔL²", "No time dependence", "No mass dependence"],
      testableWith: ["MAGIS-100", "AION", "Sagnac loops"]
    }
  },

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
  // FIRST PRINCIPLES — v2.5 Helix Geometry
  // See DERIVATION_CHAIN_HELIX.md for formal status of each derivation
  // ============================================================
  firstPrinciples: {
    statement: "STUR v2.5 is a candidate unified framework: XCRM doublet coupling χ(R₁∂_XR₂ - R₂∂_XR₁) on a derived Z₃ helix provides the foundation for deriving Standard Model + gravity. R-doublet winding gives 3 generations (automatic from |Z₃|=3) and SU(3) (from Z₃=center). Awaiting experimental verification.",

    theoryDeterminedParameters: [
      "L_X ~ 1-10 μm (Casimir-holonomy balance — uniquely determined)",
      "χ = -π/(3L_X) (vacuum stability — uniquely determined)",
      "n_gen = 3 (AUTOMATIC from Z₃ helix structure)",
      "All 19 SM parameters (derived from Z₃ helix geometry + MHP localization)"
    ],

    closureRelation: {
      formula: "ℓ_coh = √2 · L_X / (y·σ_R)",
      latex: "\\ell_{\\rm coh} = \\frac{\\sqrt{2}\\, L_X}{y\\,\\sigma_R}",
      variables: ["L_X", "σ_R", "y"],
      note: "Coherence length determined by internal dimension and fluctuations"
    },

    nonNegotiable: {
      form: "Gaussian in ΔL²",
      formula: "V(ΔL) = V₀ exp(-ΔL²/ℓ²_coh)",
      latex: "V(\\Delta L) = V_0 \\exp\\!\\left(-\\frac{\\Delta L^2}{\\ell_{\\rm coh}^2}\\right)",
      derivedFrom: [
        "XCRM holonomy variance: ⟨Φ_R²⟩ = 2(ΔL/ℓ_coh)²",
        "Central limit theorem (many uncorrelated phases)",
        "Gaussian phase averaging: V = V₀ exp(-⟨Φ_R²⟩/2)"
      ]
    },

    mhpCloses: [
      "Gauge group selection (SU(3) natural from Z₃ = center(SU(3)), full SM from MHP on Z₃ helix)",
      "Flavor structure (localization from phase positions on Z₃ helix)",
      "Fermion localization profiles (Gaussian in phase space)"
    ],

    tfpCloses: [
      "Generation number — v2.5 AUTOMATIC: |Z₃| = 3 phases → n_gen = 3 is a THEOREM",
      "Yukawa hierarchies — ESTABLISHED: phase overlaps give exponential suppression",
      "CKM/PMNS matrices — ESTABLISHED: phase mismatch between up/down sectors",
      "CP violation phase (δ_CKM ≈ 70° from helix chirality) — AUTOMATIC in v2.5"
    ],

    // Explicit caveats for claims (updated for v2.5)
    caveats: {
      gaugeGroup: "In v2.5, SU(3) is NATURAL from Z₃ = center(SU(3)). The full SM gauge group " +
                  "SU(3)×SU(2)×U(1) follows from MHP minimization on the Z₃ helix geometry.",
      generations: "v2.5 AUTOMATIC: The Z₃ helix has exactly |Z₃| = 3 distinct phase sectors. " +
                   "n_gen = 3 is a THEOREM, not a calculation. This is topological, not dynamical.",
      uvCompletion: "ESTABLISHED: UV finiteness via holonomy self-regulation. High-momentum modes " +
                    "accumulate large holonomy and are exponentially suppressed by the Faddeev-Popov measure. " +
                    "All loop integrals converge without regularization. See stur_uv_completion.html.",
      cosmologicalConstant: "v2.5 Addressed: On the Z₃ helix, |R| = v everywhere (only phase varies). " +
                           "No domain wall → zero domain wall energy → Λ reduced to leading order. " +
                           "Observed Λ > 0 requires quantum corrections (under investigation)."
    },

    dhpCloses: [
      "UV completion (holonomy self-regulation) — ESTABLISHED: stur_uv_completion.html",
      "Neutrino masses (bulk seesaw mechanism) — ESTABLISHED: stur_neutrino_derivation.html",
      "CP violation (helix chirality) — AUTOMATIC in v2.5: helix has handedness → spontaneous CP breaking",
      "Dark matter (KK parity stabilizes LKP) — ESTABLISHED: stur_darkmatter_derivation.html",
      "Cosmological constant — v2.5 Addressed: no domain wall on helix → Λ reduced",
      "Inflation (R-field slow-roll from MHP) — ESTABLISHED: stur_inflation_derivation.html",
      "Baryogenesis (complete leptogenesis) — ESTABLISHED: stur_leptogenesis_thermal.html",
      "Gauge coupling unification (5D Z₃ helix geometry) — ESTABLISHED: stur_gauge_unification_derivation.html",
      "Fifth-force screening (XCRM regulation) — ESTABLISHED: stur_fifth_force_screening.html",
      "Strong CP (θ=0 from helix geometry) — ESTABLISHED: stur_strong_cp_solution.html",
      "Quantum gravity (finite holonomy path integral on Z₃ helix)"
    ],

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
    // The Master Action (v2.5 Doublet Form)
    master_action: {
      id: "0.1",
      name: "The Unified Resistance Action (v2.5 Helix)",
      latex: "S_{\\rm STUR}[\\mathbf{R}, g, X] = \\int_{\\mathcal{M}^5} d^4x\\, dX\\, \\sqrt{-g}\\, \\Big[\\underbrace{\\color{#4ade80}{\\tfrac{1}{2}(\\nabla \\mathbf{R})^2}}_{\\text{diffusion}} - \\underbrace{\\color{#f472b6}{V(|\\mathbf{R}|)}}_{\\text{relaxation}} + \\underbrace{\\color{#fbbf24}{\\chi\\,(R_1\\partial_X R_2 - R_2\\partial_X R_1)}}_{\\text{XCRM doublet}} + \\underbrace{\\color{#60a5fa}{\\alpha\\, |\\mathbf{R}|\\, \\mathbb{T}}}_{\\text{torsion}} + \\color{#22d3ee}{\\mathcal{L}_{\\rm matter}}\\Big]",
      tier: "core",
      note: "R = (R₁, R₂) doublet with |R|² = R₁² + R₂². XCRM term = χ|R|²∂_Xφ where φ = arctan(R₂/R₁). Z₃ helix boundary conditions: R(X+L_X) = R_{2π/3}·R(X)."
    },

    // First Principles closure
    parameter_closure: {
      id: "FP.1",
      name: "Parameter Closure Relation",
      latex: "\\color{#22d3ee}{\\ell_{\\rm coh}} = \\frac{\\sqrt{2}\\, \\color{#fbbf24}{L_X}}{\\color{#a78bfa}{y}\\,\\color{#4ade80}{\\sigma_R}}",
      tier: "core",
      note: "Given any two of {χ, L_X, ℓ_coh}, the third is determined. Default: y=1."
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
      latex: "\\color{#22d3ee}{\\ell_{\\rm coh}} = \\frac{\\sqrt{2}\\, \\color{#fbbf24}{L_X}}{\\color{#a78bfa}{y}\\,\\color{#4ade80}{\\sigma_R}}",
      tier: "core",
      note: "Default: y=1 (Yukawa coupling)"
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
