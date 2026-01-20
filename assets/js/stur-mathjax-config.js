/**
 * STUR MathJax Configuration
 * Shared MathJax setup with physics domain color macros
 *
 * Include BEFORE MathJax:
 * <script src="../assets/js/stur-mathjax-config.js"></script>
 * <script async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js"></script>
 *
 * === PHYSICS DOMAIN COLOR CODING ===
 * Use these macros in your equations:
 *   \Diff{...}  - Green (#4ade80)  - Diffusion/Kinetic terms
 *   \Pot{...}   - Pink (#f472b6)   - Potential/Relaxation
 *   \XCRM{...}  - Gold (#fbbf24)   - XCRM coupling
 *   \Tor{...}   - Blue (#60a5fa)   - Torsion/Gravity
 *   \Quant{...} - Violet (#a78bfa) - Quantum corrections
 *   \Matt{...}  - Cyan (#22d3ee)   - Matter sector
 *
 * Example:
 *   S = \int [\Diff{\frac{1}{2}(\nabla R)^2} - \Pot{V(R)} + \XCRM{\chi R \partial_X R}]
 */

window.MathJax = {
  tex: {
    inlineMath: [['\\(', '\\)']],
    displayMath: [['\\[', '\\]']],
    processEscapes: true,
    macros: {
      // ============================================================
      // PHYSICS DOMAIN COLOR MACROS
      // ============================================================
      // Diffusion - Green (#4ade80) - Kinetic terms, gradient energy
      Diff: ['\\color{#4ade80}{#1}', 1],

      // Potential - Pink (#f472b6) - Relaxation potential V(R)
      Pot: ['\\color{#f472b6}{#1}', 1],

      // XCRM - Gold (#fbbf24) - X-Cross Resistance Mechanism coupling
      XCRM: ['\\color{#fbbf24}{#1}', 1],

      // Torsion - Blue (#60a5fa) - Gravity, teleparallel torsion
      Tor: ['\\color{#60a5fa}{#1}', 1],

      // Quantum - Violet (#a78bfa) - Loop corrections, holonomy
      Quant: ['\\color{#a78bfa}{#1}', 1],

      // Matter - Cyan (#22d3ee) - Standard Model matter sector
      Matt: ['\\color{#22d3ee}{#1}', 1],

      // ============================================================
      // COMMON SYMBOL MACROS
      // ============================================================
      Rcal: '\\mathcal{R}',
      Mcal: '\\mathcal{M}',
      Lcal: '\\mathcal{L}',
      Tcal: '\\mathcal{T}',
      Hcal: '\\mathcal{H}',
      Ocal: '\\mathcal{O}',
      Fcal: '\\mathcal{F}',
      Dcal: '\\mathcal{D}',

      // Bold symbols
      bR: '\\mathbf{R}',
      bx: '\\mathbf{x}',

      // Common physics notation
      dd: '\\mathrm{d}',
      ee: '\\mathrm{e}',
      ii: '\\mathrm{i}',

      // STUR-specific
      Rbg: 'R_{\\rm bg}',
      lcoh: '\\ell_{\\rm coh}',
      Lx: 'L_X',
      sigR: '\\sigma_R',
      PhiR: '\\Phi_R',

      // Operators
      Tr: '\\operatorname{Tr}',
      diag: '\\operatorname{diag}',
      sgn: '\\operatorname{sgn}'
    }
  },
  svg: {
    fontCache: 'global'
  },
  options: {
    // Disable context menu to prevent broken button rendering
    enableMenu: false,
    // Disable assistive MathML which renders as broken buttons
    enableAssistiveMml: false,
    // Disable speech text generation
    enableSpeech: false,
    // Disable exploration features
    enableExplorer: false
  }
};
