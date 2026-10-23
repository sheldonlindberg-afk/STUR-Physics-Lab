# GENESIS v10 Stage 10f: Can STUR's Own Structure Close the Theory Gaps?

**Document Type:** Derivation audit
**Date:** 2026-10-23
**Script:** `scripts/genesis_v10f_theory_gaps.py` (about 1 min; 8 gates, of which 1 is a numerical check and the FAILs are results)
**Rule:** every mechanism comes from a term already in the STUR action or the repo's own constructions, and is computed. No constants were combined to hit a target number.

## Summary

| Gap | Result | Key number |
|---|---|---|
| (a) Restoring force for the R-phase (M3a's H1) | **Not closed** | The Yukawa and Z₃ structure give V(θ) = 0 exactly. The static potentials that do exist give m_θ ≥ 6×10⁻¹⁶ GeV ≈ 2×10²² H(z*) (ε_H = 0.1, f ≤ M_Pl), a constant-frequency oscillation, not sin(ω ln t) |
| (b) Leptons-only R-charge (M3a's H2) | **Not closed; contradicted** | Quark localization needs R-charged quarks, so c_γ = 8 and c_s = 3. M3a with these charges makes θ_QCD oscillate by 3.2–6.6 rad (nEDM bound: 10⁻¹⁰) |
| (c) Inflation from the action's own scalar \|R\| | **Partially closed** | Parameter-free background ε_H = 15/(10N + 15) = 0.024 at N = 60. No defensible n_s or r: scalar-torsion scalar perturbations are not established |

## (a) Restoring force

- **Fermion phase potential** y²v²(1 − cos(φ − φ_g)) (`ALPHA_PARAMETER_DERIVATION.md` §1.3). Shifting the zero mode θ only moves every localized fermion by ΔX = −θ/k. All Yukawas are L–R overlaps, and every species moves together, so no mass and no energy depends on θ. This is an exact flat direction, the diagonal of U(1) × X-translations.
- **Z₃ twisted boundary condition.** It fixes the winding, k L_X = 2π/3. A constant phase shift preserves it.
- **Higgs Z₃ modulation** H(φ) = H₀[1 + ε_H cos 3φ] (`ABSOLUTE_MASS_DERIVATION.md` §2.2), if pinned to the coordinate:
  - It breaks the X-shift and gives m_f(θ) = m_f0[1 + ε_eff cos 3θ], with ε_eff = 0.035 ε_H.
  - The top-dominated Coleman-Weinberg potential is about (3/4π²) m_t⁴ ε_eff cos 3θ. Its amplitude is not calculable, because the scale μ needs a cos 3θ counterterm.
  - For f ≤ M_Pl, m_θ < H(z*) would require ε_H < 2×10⁻⁴⁶.
  - The mass is constant. θ then oscillates as a^(−3/2) cos(mt), and the oscillation averages out of every CMB visibility window.
  - Log-periodicity would need m(t) = ω/t, but m·t changes by a factor of 3.7×10⁴ between recombination and today.
- **QCD anomaly** (c_s = 3). This makes θ a QCD axion with a constant mass, and H2 removes it in any case.
- **Literal reading of the Yukawa.** ψ̄_L(R₁ + R₂γ⁵)ψ_R equals ψ̄_L(R₁ + R₂)ψ_R, because γ⁵ψ_R = ψ_R. Read this way it breaks U(1) explicitly: there is a tree-level potential and **no** chiral phase, so c_γ = 0 and there is no birefringence at all. The document's own V_ferm uses the phase, so the intended coupling is ψ̄(R₁ + iγ⁵R₂)ψ, and that is the reading used elsewhere.

A mass that falls as 1/t needs a coupling to H², such as ξ𝕋|R|², which is not in the Master Action.

## (b) Leptons-only R-charge

`stur_toe_closure.py` Part 2 localizes **both** the quark brane (α_q, which gives λ_W and the CKM matrix) and the lepton brane (α_l, which gives the PMNS matrix). The Mathieu potential α(1 − cos θ) used for both is the R-Yukawa phase potential. An R-neutral quark would not localize, and the CKM and mass derivations would fail.

The generation index enters as a *position*, φ_g = 2πg/3, not as a charge. So X = 1 for every species, and the 1 + ω + ω² cancellation does not act on R-charges. This forces c_γ = 8 and c_s = 3.

M3a with c_γ = 8 would need A₀ = 0.54–1.10 rad, which is more natural than the registered range. But θ_QCD,eff = 6θ would then oscillate with an amplitude of 3.2–6.6 rad.

## (c) Inflation from |R| with F(|R|)𝕋, F = 2α|R|

The mini-superspace variation (sympy) gives:

- the constraint **3FH² = φ̇²/2 + V**, with no H·Ḟ term, unlike F·R;
- the scalar equation **φ̈ + 3Hφ̇ + V′ + 3F′H² = 0**.

Slow roll for φ ≫ v, with V ≈ λφ⁴/4:

- H² = λφ³/(24α) and ε_H = 15α/φ;
- dN = −dφ/(10α) and φ_end = 15α;
- so **ε_H(N) = 15/(10N + 15)**, independent of α and λ. Numerical integration of the exact background gives 0.0248, against 0.0244 at N = 60.

Inflation on this branch needs φ* ≈ α(10N + 15) ≫ v. Since today M_Pl² = 2αv, that means v/α ≪ about 600. The repo does not fix α and v separately.

**Perturbations.** Raatikainen & Räsänen ([arXiv:1910.03488](https://arxiv.org/pdf/1910.03488), JCAP 12 (2019) 021) show that a teleparallel theory with a non-minimally coupled scalar has no linear scalar perturbations unless its coupling functions F (to 𝕋), G (torsion vector × ∂φ) and P satisfy a particular relation. STUR has F = 2α|R|, G = 0 and P = 0. I could not verify whether that combination meets the relation, because the full text was not reachable. The metric-equivalent choice needs G ∝ F′, which STUR does not have.

So n_s and r are **not computable defensibly** from the Master Action. If scalar perturbations do exist, the scale-free background means n_s and r would depend on N alone. That would be a sharp, parameter-free prediction, and it justifies doing the full scalar-torsion perturbation calculation.

Related literature: [Gonzalez-Espinoza et al., arXiv:1904.08068](https://web3.arxiv.org/pdf/1904.08068v1); [Fomin et al., arXiv:2407.14542](https://arxiv.org/html/2407.14542v3); [review, arXiv:2106.13793](https://arxiv.org/pdf/2106.13793).
