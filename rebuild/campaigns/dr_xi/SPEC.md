# SPEC: gauge-parameter independence of the whole bosonic one-loop Delta r (general R_xi gauge)

*Postulates and conventions only. Nothing here is the answer.*

Units: ħ = c = 1. In earlier work the bosonic one-loop Δr of muon decay was assembled in the 't Hooft–Feynman gauge (ξ = 1). Here you derive it in the **general R_ξ gauge** (one parameter ξ ≥ 0 for all
four gauge fields), from scratch, **with no module provided**: self-energies, photon–Z mixing, the on-shell renormalization, the vertex corrections, the boxes and the lepton wave-function renormalization, each
with its full ξ dependence. The sum is a physical quantity and must not depend on ξ; the individual classes do.

## 1. The theory (postulates)

* SU(2)_L × U(1)_Y with couplings g, g', a Higgs doublet Φ = (φ⁺, (v + H + iχ)/√2) of hypercharge 1/2, D_μ = ∂_μ − i g W^a_μ T^a − i g' Y B_μ, V = −μ²Φ†Φ + λ(Φ†Φ)², at its minimum.
  W^± = (W¹ ∓ iW²)/√2, Z = c W³ − s B, A = s W³ + c B, c = g/√(g²+g'²), e = g s. Massless leptons ℓ, ν_ℓ (left-handed doublets, right-handed charged singlets); no other fermion couples (the
  fermion-loop self-energies are excluded, as in the bosonic Δr). Derive every vertex, mass and coupling (gauge, Goldstone, Higgs, ghost, fermion) from the Lagrangian.
* R_ξ gauge fixing with one ξ for W^±, Z and the photon: gauge-boson propagator −i[g^{μν} − (1 − ξ) k^μk^ν/(k² − ξ M²)]/(k² − M²) (M = M_W, M_Z, and 0 for the photon, where the denominator is
  k² and the ξ term is −(1−ξ) k^μk^ν/k²), Goldstone mass² ξ M_W², ξ M_Z², gauge fixing chosen so that the gauge–Goldstone mass mixing cancels, Faddeev–Popov ghosts with masses² ξM². The Landau gauge ξ = 0 and
  large ξ must be accepted. The photon's ξ is the same ξ.
* Tadpoles: the Higgs one-point diagrams are cancelled by the tadpole counterterm and are not included. Say, in DERIVATION.md, why that leaves the gauge-independent total unchanged.
* Inputs (all on-shell): the pole masses M_W, M_Z, the Higgs mass M_H, and α = e²/4π with e the Thomson-limit charge; s² = 1 − M_W²/M_Z². The Fermi constant G_F is defined from the muon-decay amplitude at zero momentum
  transfer with massless leptons, including the one-loop electroweak corrections but **excluding the QED corrections of the Fermi model** (subtract the one-loop photonic correction of the four-fermion theory;
  the infrared divergences, real and virtual, cancel with a photon mass λ → 0). Δr is the first-order relative correction in M_W²(1 − M_W²/M_Z²) = (πα/(√2 G_F))(1 + Δr).

## 2. The quantities

Regularize in d = 4 − 2ε (d-dimensional loop momentum, g^μ_μ = d, the O(ε) parts of d-dependent coefficients kept against the 1/ε pole) and subtract in MS-bar at the scale μ for the intermediate pieces below.
Below every threshold the quantities are real; at or above, return the real part. Report in DERIVATION.md which diagrams belong to each class and the renormalization constants used.

* **Class SE**: everything in Δr that comes from the gauge-boson two-point functions: the transverse self-energies of γ, Z, W, the photon–Z mixing (including its value at zero momentum), the on-shell
  renormalization of the masses, the weak mixing angle and the charge, and the shift of G_F that they induce. (The fermion-loop self-energies are not part of this campaign.)
* **Class VBW**: the 1PI vertex corrections of the W^± ℓ ν_ℓ coupling, the box diagrams, the lepton wave-function renormalization, and the Fermi-theory subtraction. It is UV divergent and μ dependent by itself.
  It does *not* contain the photon–Z mixing piece (that is in SE).
* The total Δr_bos = SE + VBW is UV finite, μ independent and ξ independent.

**Landau gauge, ξ = 0 exactly (clarification added after the audit).** The classes SE and VBW are separately infrared divergent at ξ = 0 and diverge like ±(3/4)(α/4π) ln ξ as ξ → 0⁺; the total is finite and ξ independent. At ξ = 0 their *values* therefore
depend on how the infrared pole is subtracted, a convention this SPEC does not fix: state yours (the two accepted builds differ by the constant (1/8)(α/4π), equal and opposite in the two classes). Only ξ > 0 values of the classes are compared between builds.

## 3. Exports (exact signatures in campaign.py)

`delta_r_se(MW, MZ, MH, alpha, xi, mu)`: class SE, MS-bar at μ.
`delta_r_vbw(MW, MZ, alpha, xi, mu)`: class VBW, MS-bar at μ (it does not depend on M_H).
`delta_r_bos_xi(MW, MZ, MH, alpha, xi)`: the total, first order in α, dimensionless (no μ).
Masses in GeV. M_H ranges from 1 GeV to above 10¹⁰ GeV.

## 4. The question

Compute everything for general ξ. In DERIVATION.md state the structure of the ξ dependence: which pieces (self-energy, mixing, vertex, box, wave function) are ξ dependent and how they cancel; report, as a check
of your own, the total at ξ = 0, 1 and a large ξ. Keep any high-precision setting local to the exports. If you cannot make the total ξ independent, say so plainly rather than adjusting a term.
