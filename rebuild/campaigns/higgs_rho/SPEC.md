# SPEC: the Higgs-mass dependence of the rho parameter at one loop

*Postulates and conventions only. Nothing here is the answer.*

Units: ħ = c = 1. Only the bosonic electroweak sector with the Higgs doublet is needed: fermions and QCD are omitted, because the
quantity below depends on the Higgs mass only through Higgs-containing loops.

## 1. The theory (postulates)

* Gauge group SU(2)_L × U(1)_Y with fields W^a_μ (a = 1, 2, 3), B_μ and couplings g, g'. Higgs doublet Φ = (φ⁺, (v + H + iφ⁰)/√2) with
  hypercharge 1/2, D_μΦ = (∂_μ − i g W^a_μ τ^a/2 − i g' B_μ/2)Φ and potential V = −μ²Φ†Φ + λ(Φ†Φ)², at its minimum Φ = (0, v/√2).
* Mass eigenstates: W^±_μ = (W¹_μ ∓ iW²_μ)/√2, Z_μ = c W³_μ − s B_μ, A_μ = s W³_μ + c B_μ with c = g/√(g² + g'²), s² = 1 − c², and
  e = g s. Derive M_W, M_Z (M_W = c M_Z), the Higgs mass m_H and the Goldstone couplings from the Lagrangian; do not assume them.
* R_ξ gauge, one parameter ξ for all three gauge sectors, with gauge-fixing functions chosen so that the W⁺–φ⁻ and Z–φ⁰ mass mixing
  cancels at tree level and the Goldstone and unphysical gauge-boson modes have mass² ξ M_W² and ξ M_Z². Ghosts need not be included for
  the diagrams of section 2 (say why in DERIVATION.md).

## 2. The observable (definition)

Treat M_W, M_Z (hence c, s) and α = e²/4π as inputs and m_H as the variable. At zero momentum the one-loop 1PI two-point functions
give effective masses: the one-loop effective action contains M_W²(eff) W⁺_μW^{−μ} and ½ M_Z²(eff) Z_μZ^μ with
M_V²(eff) = M_V² + Π_VV(0), Π_VV(0) being the g^{μν} coefficient at q = 0 (the q^μ q^ν terms vanish there). Keep only the diagrams that contain a Higgs
boson H (loops with H and a gauge boson, with H and a Goldstone, and the quartic seagull loops with H); drop the
tadpole diagrams (they shift both Π_WW/M_W² and Π_ZZ/M_Z² by the same amount, so they cancel in the ratio below; confirm this in
your derivation). The rho parameter is ρ = M_W²(eff)/(c² M_Z²(eff)), so at one loop

    Δρ = Π_WW(0)/M_W² − Π_ZZ(0)/M_Z² .

Regularize in d = 4 − 2ε dimensions and subtract the pole in the MS-bar scheme at the scale μ (a length⁻¹ argument).

## 3. Exports (exact signatures in campaign.py)

* `self_energy_W(mH, MW, MZ, alpha, xi, mu)` → the MS-bar Π_WW(0) from the Higgs-containing diagrams.
* `self_energy_Z(mH, MW, MZ, alpha, xi, mu)` → the same for Π_ZZ(0).
* `rho_higgs_rel(mH, MW, MZ, alpha, xi, mu)` → Δρ(m_H) − Δρ(m_H = M_W), from the two functions above (this difference is the
  quantity that is physical and finite).
* `log_coefficient(MW, MZ, alpha, xi)` → B = lim_{m_H→∞} Δρ(m_H)/ln(m_H²/M_W²), derived analytically from the large-m_H expansion of your loop integrals.

## 4. Conventions for numerics

State the Passarino–Veltman (or other) integrals you use, how the poles cancel, and the accuracy of every export. Say what you checked
about the independence of the result from μ, and from the gauge parameter.
