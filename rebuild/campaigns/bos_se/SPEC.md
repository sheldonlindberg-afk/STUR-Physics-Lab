# SPEC: the bosonic one-loop gauge-boson self-energies of the electroweak theory, 't Hooft-Feynman gauge

*Postulates and conventions only. Nothing here is the answer.*

Units: ħ = c = 1. This is the first stage of the on-shell Delta r of muon decay: the self-energies of γ, Z, W that come from loops of
**bosons only** (gauge bosons, Goldstone bosons, the Higgs boson, ghosts). Loops with a fermion are excluded entirely.

## 1. The theory (postulates)

* SU(2)_L × U(1)_Y gauge theory with couplings g, g', gauge fields W^a_μ, B_μ with the non-Abelian field strength (triple and quartic gauge
  couplings), a Higgs doublet Φ = (φ⁺, (v + H + iχ)/√2) of hypercharge 1/2, D_μΦ = (∂_μ − i g W^a_μ τ^a/2 − i g' B_μ/2)Φ and
  V = −μ²Φ†Φ + λ(Φ†Φ)², at its minimum Φ = (0, v/√2). W^± = (W¹ ∓ iW²)/√2, Z = c W³ − s B, A = s W³ + c B, c = g/√(g²+g'²), e = g s.
  Derive M_W, M_Z (M_W = c M_Z), the Higgs mass M_H and every coupling you need (gauge, Goldstone, Higgs, ghost vertices) from the Lagrangian; do not assume them.
* Gauge fixing: the 't Hooft-Feynman gauge (R_ξ with ξ = 1 for W^±, Z and the photon), chosen so that the gauge-boson–Goldstone mass mixing cancels; the Goldstones
  φ^±, χ have mass² M_W², M_Z² and the gauge-boson propagators are −i g^{μν}/(k² − M²). Faddeev–Popov ghosts for all four gauge fields with the BRST-consistent
  couplings to the Higgs and the Goldstones: they contribute to the diagrams below.
* The inputs are the tree-level parameters M_W, M_Z, M_H and α = e²/4π, with c² = M_W²/M_Z², s² = 1 − c². At one loop no renormalization of the parameters inside
  the loops is needed.

## 2. The quantities (definition)

For V, V' ∈ {A, Z} or V = V' = W, the transverse part Σ^{VV'}_T(k²) of the one-loop 1PI two-point function is defined by the dressed transverse propagator
−i g^{μν}/(k² − M_V² + Σ_T(k²)) (for the A–Z mixing: the transverse mixing term −i g^{μν} Σ^{AZ}_T(k²) in the inverse propagator matrix; positive Σ lowers the
effective mass² M² − Σ). Σ^{AA}, Σ^{AZ}: M_A = 0. Include **all** one-loop 1PI diagrams with at least one boson, ghost or scalar in the loop and no fermion: gauge-boson
bubbles with triple vertices, Goldstone and Higgs bubbles, mixed gauge–scalar bubbles, ghost loops and every quartic-vertex tadpole-type loop (the "seagull" diagrams on
a boson line). **Exclude** the diagrams with a one-point Higgs tadpole attached (they are cancelled by the tadpole counterterm). Regularize in d = 4 − 2ε (conventional
dimensional regularization: d-dimensional loop momentum, g^μ_μ = d, the O(ε) part of every d-dependent coefficient kept against the 1/ε pole) and subtract the
pole in the MS-bar scheme at the scale μ (a mass argument): μ^{2ε} multiplies the measure and Δ = 1/ε − γ_E + ln 4π is dropped.

Below every threshold the self-energies are real. At or above a threshold return the real part. The loops with a photon are infrared-regular at the arguments below:
take the photon mass λ → 0 inside the loop functions (the limit exists). k² = 0 is allowed and means the limit k² → 0 (the Σ_T are analytic there).

## 3. Exports (exact signatures in campaign.py)

`sigma_AA(k2, MW, MZ, MH, alpha, mu)`, `sigma_AZ(...)`, `sigma_ZZ(...)`, `sigma_W(...)`: the bosonic Σ^{AA}_T, Σ^{AZ}_T, Σ^{ZZ}_T, Σ^{W}_T at k² (GeV²), masses in GeV, α = e²/4π, MS-bar scale μ in GeV.

## 4. Conventions for numerics

State the scalar integrals you use and how every pole cancels or is subtracted; state how thresholds, k² = 0 and very large M_H are handled; keep any high-precision
setting local to the exports (do not change a global precision). Say what you checked: the photon Ward identity, the μ dependence, the UV pole coefficient.
