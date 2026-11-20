# SPEC: the fermion-loop one-loop self-energies of the electroweak gauge bosons, 't Hooft-Feynman gauge

*Postulates and conventions only. Nothing here is the answer.*

Units: ħ = c = 1. This is the fermionic counterpart of the bosonic self-energies: the transverse self-energies of γ, Z, W that come from **loops of fermions only**.
All boson, Goldstone and ghost loops are excluded entirely.

## 1. The theory (postulates)

* SU(2)_L × U(1)_Y with couplings g, g', gauge fields W^a_μ, B_μ, covariant derivative D_μ = ∂_μ − i g W^a_μ T^a − i g' Y B_μ, W^± = (W¹ ∓ iW²)/√2,
  Z = c W³ − s B, A = s W³ + c B, c = g/√(g²+g'²) = M_W/M_Z, e = g s, α = e²/4π, s² = 1 − c², Q = I₃ + Y.
  The gauge bosons have the tree-level masses M_W, M_Z (a Higgs doublet gives them, you do not need the Higgs sector except for the next bullet); gauge fixing is the 't Hooft-Feynman gauge,
  so every gauge-boson propagator is −i g^{μν}/(k² − M²) (the k^μ k^ν part does not contribute to the transverse part).
* Matter content: each Dirac fermion f has a left-handed component in an SU(2) doublet with weak isospin I₃ (the T³ of that component: any value, not only ±½) (and a right-handed SU(2) singlet of the same electric charge Q) and gets
  its mass m from a Yukawa coupling to the Higgs doublet. A fermion given as (m = 0, Q = 0, I₃ = ½) is a neutrino: left-handed only, no right-handed partner.
  The charged-current W^± couples left-handed doublet partners (u, d) of the same weight; quarks carry N_C colours and a CKM matrix enters only through the weights given below.
  Derive every coupling (vector and axial couplings of f to γ and Z, the W coupling) from the Lagrangian; do not assume them.
* Inputs: M_W, M_Z, α and the fermion data below. No renormalization of the parameters inside the loops is needed at one loop.

## 2. The quantities (definition)

For V, V' ∈ {A, Z} or V = V' = W, the transverse part Σ^{VV'}_T(k²) of the one-loop 1PI two-point function is defined by the dressed transverse propagator
−i g^{μν}/(k² − M_V² + Σ_T(k²)) (for the A–Z mixing: the transverse vertex function, the quadratic term of the effective action, is Γ^{VV'}_{μν} = −i g_{μν}[(k² − M_V²)δ_{VV'} + Σ^{VV'}_T(k²)],
so the A–Z entry is −i g_{μν} Σ^{AZ}_T; positive Σ lowers the effective mass² M² − Σ). Include the fermion bubble diagrams only: γγ, γZ, ZZ (each fermion, both chiralities, mass insertions
included) and WW (each doublet (u, d) with weight w). Regularize in d = 4 − 2ε (d-dimensional loop momentum and γ-algebra, the O(ε) parts of d-dependent coefficients kept against the 1/ε pole;
use an anticommuting γ5 (naive dimensional regularization, NDR); the 't Hooft–Veltman scheme differs by finite terms and is not asked for) and subtract the pole in MS-bar at the scale μ: μ^{2ε} multiplies the measure and Δ = 1/ε − γ_E + ln 4π is dropped.

Below every threshold the self-energies are real; at or above one return the real part. m = 0 and k² = 0 are allowed (the limit k² → 0: Σ_T is continuous there; for massless loops its derivative is not, so the exports are asked for values, not slopes, at k² = 0).

## 3. Exports (exact signatures in campaign.py)

`fermions` is a tuple of (m, Q, I3, NC) per Dirac fermion (colours counted by NC, not repeated); `doublets` is a tuple of (m_up, m_down, w) with w = N_C |V_ud|² the weight of that W^± → f f' loop (leptons: w = 1).
`sigma_AA(k2, fermions, MW, MZ, alpha, mu)`, `sigma_AZ(...)`, `sigma_ZZ(...)`: fermionic Σ^{AA}_T, Σ^{AZ}_T, Σ^{ZZ}_T at k² (GeV²), masses in GeV;
`sigma_W(k2, doublets, MW, MZ, alpha, mu)`: fermionic Σ^{W}_T.

## 4. Conventions for numerics

State the scalar integrals you use and how the pole cancels or is subtracted; state how thresholds (k² above 4m², (m_u + m_d)²), k² = 0, m = 0, and very different masses in one loop (m_t against m_ν = 0) are handled; keep
any high-precision setting local to the exports (do not change a global precision). Say what you checked: the photon Ward identity, the μ dependence, the UV pole coefficient, and the limit of a heavy fermion.
