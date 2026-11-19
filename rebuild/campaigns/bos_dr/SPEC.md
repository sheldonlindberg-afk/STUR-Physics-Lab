# SPEC: the bosonic part of the on-shell Delta r of muon decay at one loop

*Postulates and conventions only. Nothing here is the answer.*

Units: ħ = c = 1. This is the second stage after `bos_se`: the **provided module `bos_se`** (in the same directory as your build; its exports are described below) gives the
bosonic one-loop gauge-boson self-energies of the theory below; you do not re-derive them. Everything else is yours to derive.

## 1. The theory (postulates)

The SU(2)_L × U(1)_Y theory with a Higgs doublet (hypercharge 1/2), massless leptons ℓ, ν_ℓ (left-handed doublets, right-handed singlets of the charged leptons), W^± = (W¹ ∓ iW²)/√2,
Z = c W³ − s B, A = s W³ + c B, c = g/√(g²+g'²), e = g s, covariant derivative D_μ = ∂_μ − i g W^a_μ T^a − i g' Y B_μ. Charged-lepton hypercharge Y = −1/2 (doublet), charge Q = T³ + Y.
't Hooft–Feynman gauge (ξ = 1) with the Faddeev–Popov ghosts and Goldstones of the first stage. Derive every vertex, including the fermion couplings (the Z and photon couplings of the
leptons, the W coupling g/(2√2) γ^μ(1−γ⁵)), from the Lagrangian.

## 2. The provided module

`bos_se.sigma_AA, sigma_AZ, sigma_ZZ, sigma_W(k2, MW, MZ, MH, alpha, mu)` return the bosonic transverse self-energies Σ^{VV'}_T(k²) (GeV²): the dressed transverse propagator is −i g^{μν}/(k² − M_V² + Σ_T(k²)), the
photon–Z mixing enters the inverse propagator matrix as +Σ^{AZ}_T; MS-bar at the scale μ (a mass), tadpoles excluded, fermion loops excluded, real parts, k² = 0 means the limit. Using them is allowed and expected; you may
differentiate numerically, e.g. for Σ'_AA(0). Everything else in this SPEC (the renormalization, the vertex, box and external-leg diagrams, the assembly) you derive.

## 3. The observable (definition)

Inputs: M_W, M_Z (pole masses; hence c² = M_W²/M_Z², s² = 1 − c²), M_H, α = e²/4π with e the charge in the Thomson limit (renormalized so that the photon couples to a charged particle with
strength e at zero photon momentum, with the photon–Z mixing at zero momentum accounted for), all on-shell. The Fermi constant G_F is defined from the muon-decay amplitude at zero momentum
transfer in the limit of massless leptons, including the one-loop electroweak corrections but **excluding the QED corrections of the Fermi model**, i.e. subtracting the one-loop photonic correction of the
four-fermion effective theory (the real and virtual infrared divergences cancel in the sum; use a photon mass λ → 0 and show the cancellation). Δr is then the first-order relative correction defined by

    M_W² (1 − M_W²/M_Z²) = (π α / (√2 G_F)) (1 + Δr).

The task: the **bosonic part** Δr_bos of Δr, namely everything except the diagrams whose only non-gauge-boson internal lines are a closed fermion loop on a vector-boson propagator (the fermion-loop
self-energies, vacuum polarization of the photon, and the like, which are not part of this campaign). Δr_bos includes the bosonic self-energies, the mixing, the vertex corrections, the box diagrams, the lepton
wave-function renormalization and the renormalization constants of the on-shell scheme. It is UV finite and gauge-parameter independent. Derive how each piece enters (which diagrams, which counterterms) and
report the decomposition in DERIVATION.md.

## 4. Exports (exact signatures in campaign.py)

`delta_r_bos(MW, MZ, MH, alpha)` → Δr_bos, dimensionless, first order in α. The MS-bar scale cancels; the exports take no μ.
`delta_vb(MW, MZ, alpha)` → the one-loop vertex + box + lepton-wave-function contribution to the relative correction of the muon-decay amplitude (after the Fermi-theory QED subtraction), as it enters Δr_bos in your
decomposition; for definiteness take the 't Hooft–Feynman-gauge diagrams of section 3 with the on-shell W–ℓ–ν coupling counterterm *not* included (it belongs to the renormalization pieces).

## 5. Conventions for numerics

State which counterterms enter and why, how the infrared divergence cancels, the UV check, how the self-energies of the provided module are used (including k² = 0 limits), and the accuracy. Keep any
high-precision setting local.
