# Stage 10o: the ultralight static-mass candidate (U0), and the ranking from computed inputs

**Script:** `scripts/genesis_v10o_u0_and_ranking.py` (4/4 gates pass; about 10 minutes)
**Date:** 2026-10-30
**Status:** U0 computed. The ranking now uses only computed results (Stages 10g–10o). No registered file was changed, and U0 is **not** pre-registered.

## U0: what it is

U0 is an R-phase with a small static mass m that rolls coherently after recombination. This is the standard ultralight axion-like birefringence mechanism.

- It was found by Stage 10j, which computed it only for c_γ = 3 and 8 and only at high ℓ.
- It uses c_γ = 6 with c_s = 0, an R-charge assignment that Stage 10i shows is allowed (no QCD pinning).
- Dynamics: θ'' + 3Hθ' + (m²/3) sin 3θ = 0 with |θ_i| ≤ π/3, using Stage 10j's equation and integrator.

## Gates

1. **Background:** 13.797 Gyr, matching the Stage 10b sources.
2. **c_γ scaling:** c_γ = 6 equals 2 × the exact c_γ = 3 result to 3×10⁻¹⁶°. This is checked on the history with the largest rotation (0.589°).
3. **Reproduction:** Stage 10j is reproduced at its own (m, θ_i) points to 3×10⁻⁵°.
4. **U0 reaches β_now** for 11 of the solved masses.

## Corrections found on the way

The first two runs failed their gates, and both causes were fixed before any U0 result was used.

- **Run 1: histories built per unit K.** These reached tens of degrees, where β_eff (an arcsin) saturates. The linearity gate missed it because it probed a frozen history.
- **Run 2: a sign bug.** The solve compared signed β with +0.277°, but the sign follows θ_i, which is free.

**Stage 10j's "plateau" was a sampling artifact.** For H₀ < m < H(z*), β depends on the field's phase today (m·t₀), so it oscillates with m. 10j's 22 mass points gave 0.20–0.22°. An 80-point scan shows:

| | Result |
|---|---|
| Maximum \|β_rec\|, c_γ = 3, θ_i = π/3 | **0.2876°** at m/H₀ = 13.3 |
| Fraction of masses reaching 0.277° | c_γ = 3: 3%; **c_γ = 6: 71%** |
| Physical ceiling (full swing 2π/3), c_γ = 3 | 0.418° |

So 10j's statement that "c_γ = 3 never reaches β_now" is wrong. It does, but only at specific masses.

## U0 predictions (c_γ = 6, β_rec = 0.277°)

| m [eV] | m/H₀ | θ_i [rad] | β_reio | ratio | Δβ |
|---|---|---|---|---|---|
| 9.6×10⁻³³ | 6.7 | 0.630 | 0.253° | 0.915 | −0.024° |
| 1.8×10⁻³² | 12.4 | 0.638 | 0.219° | 0.789 | −0.059° |
| 3.3×10⁻³² | 22.9 | 0.728 | 0.150° | 0.541 | −0.127° |
| 6.1×10⁻³² | 42.4 | 0.713 | 0.056° | 0.201 | −0.221° |
| ≥ 1.1×10⁻³¹ | ≥ 78 | ≈ 0.69 | ≈ 0.005° | ≈ 0.02 | ≈ −0.27° |

- **Field-size window: open for every solved mass.** The lower edge is f > 4.2×10¹² GeV, from ACT anisotropy, since the field is light during inflation. The upper edge is f < 8–9×10¹⁷ GeV, from the ULA density bound Ω h² ≤ 0.006 (Hlozek et al. 2015, PRD 91, 103512). The lightest mass lies below that bound's range.
- **High-ℓ shape: flat.** |β_eff(ℓ) − β_now| ≤ 0.0004° at ℓ = 50–1200, so U0 has no ℓ-shape signature.
- **The tomographic ratio measures m.** It runs from 0.92 for the lightest masses down to about 0.02 for m ≳ 10⁻³¹ eV. LiteBIRD's σ(Δβ) is 0.21° at r = 0.0035, so it can only weakly separate these values.

## Ranking (computed inputs only)

| Hypothesis | Computed status | Assumptions beyond STUR |
|---|---|---|
| **H0**: STUR as written | β ≈ 0 in every consistent reading (10i); 2.9–4.9σ from the measured β | none |
| C0: free U(1) rotation | **Excluded**: no f window for any β input (10g, 10k, 10n) | c_s = 0 charges; fermions pinned in X |
| M3a: log-time oscillation | **Not realisable** with Hubble friction: every mass law tested misses by ≥ 0.27° (10j). Its registered test stands as a test | c_s = 0; X-pinning; H1 dynamics |
| STUR-B: log-time rotation | Viable: f window 5.8×10⁷–2.8×10¹⁵ GeV (10n). Needs a ~150× suppression with no mechanism | c_s = 0; X-pinning; ξ𝕋\|R\|² with unpinned \|R\|; ~150× suppression |
| **U0**: ultralight static mass | **Viable**: m = 10⁻³²–4.5×10⁻³⁰ eV, θ_i ≈ 0.7 rad, wide f window | c_s = 0 (c_γ = 6 assignment); X-pinning; a free tiny mass m |

## Conclusion

**H0** is still the hypothesis that fits STUR's own mathematics best: no isotropic birefringence. Of the β ≠ 0 options, **U0 now ranks above STUR-B**. Both need c_s = 0 and fermions pinned in X. Beyond that:

- **U0** adds one free mass and uses standard dynamics with O(1) numbers.
- **STUR-B** adds a new coupling, an unpinned modulus and an unexplained ~150× suppression.

U0 has three weaknesses:

- STUR does not produce its mass. The repo's Higgs modulation, if pinned, gives m ≥ 6×10⁻¹⁶ GeV, which is 10²³–10²⁵ times heavier.
- The tomographic ratio depends on m, so U0 makes no single Δβ prediction.
- It has no ℓ-shape signature.

U0's testable content is therefore a nonzero, achromatic β with a flat β_eff(ℓ), plus a Δβ that maps to m.
