# SPEC: gauge-parameter independence of the Higgs-mass dependence of the W-mass prediction (Delta r) at one loop

*Postulates and conventions only. Nothing here is the answer.*

Units: ħ = c = 1. Same bosonic electroweak theory as the higgs_rho campaign, in the R_ξ gauge with one parameter ξ ≥ 0 for all three gauge sectors (gauge-boson propagator
−i[g^{μν} − (1−ξ)k^μk^ν/(k² − ξM²)]/(k² − M²), Goldstone mass² ξM_V²; gauge-fixing chosen so the W–φ and Z–φ mass mixing cancels; the Landau gauge ξ = 0 must be accepted). Ghosts: say why they
do or do not contribute to the Higgs-containing two-point functions. Fermions and QCD are omitted: only Higgs-containing loops carry
m_H dependence, and the Higgs does not couple to the massless fermions of muon decay (so no Higgs vertex or box diagrams exist at one loop).

## 1. The theory (postulates)

* SU(2)_L × U(1)_Y with couplings g, g', Higgs doublet Φ = (φ⁺, (v + H + iφ⁰)/√2), hypercharge 1/2, D_μΦ = (∂_μ − i g W^a_μ τ^a/2 − i g' B_μ/2)Φ,
  V = −μ²Φ†Φ + λ(Φ†Φ)², at its minimum Φ = (0, v/√2). W^± = (W¹ ∓ iW²)/√2, Z = c W³ − s B, A = s W³ + c B, c = g/√(g²+g'²), e = g s.
  Derive M_W, M_Z (M_W = c M_Z), m_H and the Goldstone and Higgs couplings from the Lagrangian; do not assume them.
* Inputs: M_W, M_Z (pole masses; hence c² = M_W²/M_Z² and s² = 1 − c², the on-shell mixing angle), α = e²/4π and m_H the variable.

## 2. The self-energies (definition)

The one-loop 1PI two-point function of a massive vector V = W, Z has the form i[Π_VV(q²) g^{μν} + Π^L_VV(q²) q^μq^ν]. Only the g^{μν} part
Π_VV(q²) matters here: the effective mass² of the vector is M_V² + Π_VV(q²) (pole mass: at q² = M_V²). Keep the diagrams that contain a Higgs boson
H: H with a gauge boson, H with a Goldstone, and the quartic seagull loop with H; drop the tadpoles (they shift Π_WW/M_W² and Π_ZZ/M_Z² by the same
amount; check this, and say how it enters the observable below). Regularize in d = 4 − 2ε (conventional dimensional regularization, tensor reduction
k^μk^ν → g^{μν}k²/d with the O(ε) part of 1/d kept against the 1/ε pole) and subtract in MS-bar at the scale μ: μ^{2ε} multiplies the measure and
Δ = 1/ε − γ_E + ln 4π is dropped. For q² below every threshold (q² < (m_H + M_V)²) Π_VV is real.

## 3. The observable (definition)

The Fermi constant of muon decay is defined at zero momentum from the W exchange, with the tree-level relation G_F/√2 = g²/(8 M_W²) corrected by
the effective mass at q² = 0 (the 1PI vertex and box corrections have no Higgs-dependent part, as stated above). The weak coupling g and
the mixing angle are tied to the inputs through the on-shell definitions: M_W and M_Z are pole masses and s² ≡ 1 − M_W²/M_Z² *at the order considered*; the
electric charge e is not renormalized by Higgs loops (the photon self-energy and γ–Z mixing carry no Higgs-containing diagram at this order). From the
measured G_F, α and M_Z the model predicts M_W through

    M_W² s² = π α / (√2 G_F) / (1 − Δr)        (Sirlin's Δr)

so the Higgs dependence of the M_W prediction is the Higgs part of Δr. Derive Δr_H in terms of the self-energies of section 2. You must
carry the relation between the bare g, s_0² and the on-shell quantities through the one-loop shifts of the pole masses; this is the part of the task.
Report the m_H dependence as Δr_H(m_H) − Δr_H(M_W) (the reference mass m_H = M_W removes the scheme-dependent constants, and the polynomial terms of the
renormalization).

## 4. Exports (exact signatures in campaign.py)

* `sigma_W(q2, mH, MW, MZ, alpha, xi, mu)` → the MS-bar g^{μν} coefficient Π_WW(q²) from the Higgs-containing diagrams.
* `sigma_Z(q2, mH, MW, MZ, alpha, xi, mu)` → the same for Π_ZZ(q²).
* `delta_r_higgs_rel(mH, MW, MZ, alpha, xi, mu)` → Δr_H(m_H) − Δr_H(m_H = M_W), dimensionless.
* `log_coefficient(MW, MZ, alpha, xi)` → B = lim_{m_H→∞} [Δr_H(m_H) − Δr_H(M_W)] / ln(m_H²/M_W²), from the large-m_H expansion of your own integrals.

## 5. The question

Compute everything for general ξ, including the q^μq^ν and ξ-dependent parts of the gauge propagator and the Goldstone loops with mass² ξM². Report whether
the Higgs-dependent Delta r_H(m_H) − Delta r_H(M_W) depends on ξ, and why (or why not). Do not assume the answer. Pi_VV(q²) is the g^{μν} coefficient of the
sum of Higgs-containing 1PI diagrams; with ξ ≠ 1 the pole-mass relation needs care: say how the pole position and the q^μq^ν pieces enter.

## 6. Conventions for numerics

State the integrals you use (Feynman parameters, Passarino–Veltman, ...), how the poles cancel, how thresholds are avoided, and the accuracy of every export. State what
you checked: μ-independence of the physical combination, the q² → 0 limit, the large-m_H behaviour.
