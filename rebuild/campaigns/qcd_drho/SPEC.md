# SPEC: the O(alpha_s) QCD correction to the rho parameter from the top-bottom doublet

*Postulates and conventions only. Nothing here is the answer.*

Units: ħ = c = 1. The electroweak symmetry-breaking sector enters only through the weak currents; this is the *gaugeless limit* at leading order in G_F m_t².

## 1. The theory (postulates)

* A weak doublet of quarks (t, b) in the fundamental representation of SU(N) colour (N_C colours, Casimir C_F = (N_C² − 1)/(2 N_C); the numbers N_C = 3, C_F = 4/3 are the physical case, but keep N_C and C_F general), coupled to the
  gluon field with the QCD coupling g_s, α_s = g_s²/4π, in Feynman gauge (the result is gauge independent: say why). The top has mass m_t, the bottom is massless. Left-handed doublet, right-handed singlets;
  both quarks get their mass from the Yukawa coupling to the Higgs doublet, so the quark masses are the only source of weak-isospin breaking.
* The weak interaction is the coupling of the three SU(2)_L gauge fields to the left-handed currents J^a_μ = q̄ γ_μ P_L (τ^a/2) q, a = 1, 2, 3, with coupling g and gauge-boson masses M_W² = g² v²/4 for W^{1,2} and, with the
  hypercharge coupling switched off, M_Z² c² → M_W² for W³ (gaugeless limit: g, g' → 0 at fixed v, i.e. work to leading order in the electroweak couplings and in G_F m_t² = m_t²/(√2 v²), neglecting terms suppressed by M_{W,Z}²/m_t²).

## 2. The quantity (definition)

Let Σ_W(q²) and Σ_Z(q²) be the transverse self-energies of the charged and neutral gauge bosons from the quark loops (with QCD corrections), defined by the dressed propagator −i g^{μν}/(q² − M² + Σ_T(q²)) (positive Σ lowers the effective mass²).
The low-energy ratio of the neutral- to the charged-current strength is ρ = 1 + Δρ with

    Δρ = Σ_Z(0)/M_Z² − Σ_W(0)/M_W²       (the Z and W of the gaugeless limit, M_Z² c² = M_W²).

Everything is evaluated at q² = 0. Regularize dimensionally in d = 4 − 2ε; the result must be finite once the quark mass is renormalized. Two schemes for the top mass are requested: the **pole** mass m_t (the pole of the full top propagator) and the
**MS-bar mass at the scale μ**, m̄_t(μ). Δρ is a physical quantity (it does not depend on μ or the scheme when all orders are kept); at fixed order, with the leading term written in terms of the mass of the stated scheme, the correction changes.

Write Δρ = Δρ₀(m) [1 + c(scheme, C_F, μ/m) · α_s/π] where Δρ₀(m) is the one-loop (α_s⁰) value with the top mass m of the stated scheme, and c is the O(α_s) coefficient.

## 3. Exports (exact signatures in campaign.py)

`delta_rho_oneloop(m, GF, NC)` → the one-loop Δρ₀ of the doublet with the massless bottom, in terms of G_F = 1/(√2 v²).
`qcd_coeff(scheme, CF, mu_over_m)` → the coefficient c; `scheme` is "pole" (then `mu_over_m` is ignored) or "msbar" (m̄_t(μ), mu_over_m is μ divided by the mass m̄_t(μ) itself).
`delta_rho_qcd(m, GF, NC, CF, alphas, scheme, mu_over_m)` → Δρ₀(m)(1 + c α_s/π).

## 4. Conventions for numerics

Report the two-loop vacuum integrals you use and how every pole (UV subdivergence, mass counterterm) cancels; the relation between the pole and the MS-bar mass at this order; the colour-factor dependence; and the independent route you used to check the number.
