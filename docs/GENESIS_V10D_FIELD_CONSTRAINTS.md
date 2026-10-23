# GENESIS v10 Stage 10d: Field-Normalization Constraints on STUR-B and STUR-M3a

**Script:** `scripts/genesis_v10d_field_constraints.py` (runs in under 1 s; 4/4 gates pass)
**Date:** 2026-10-23
**Scope:** Gap-list items 6 (field normalization f) and 7 (anisotropic birefringence).

## Why f matters

Both hypotheses are written in terms of the dimensionless R-phase θ. The physical field is a = fθ. The decay constant f sets three things: the field's energy density, its photon coupling g = c_γ α/(π f), and its inflationary fluctuations.

**STUR does not fix f.** The repo gives two incompatible R-field VEVs:

- v = 3/L_X with L_X = 0.8 μm, about 0.74 eV (`ABSOLUTE_MASS_DERIVATION.md`)
- v_R ≈ M_GUT ≈ 2×10¹⁶ GeV (`COMPLETE_CORRECTIONS_AND_RESOLUTIONS.md`)

f is therefore treated as free, and both repo values are evaluated.

## Constraints

**(a) Energy density.** The model energy density is ρ = f² W²/(2t²), with W = ω_eff for STUR-B and W = A₀ω for M3a. It is compared against early-dark-energy fractions: about 1% at z ~ 100–1000 and about 2.6% in the radiation era, both at 2σ (arXiv:2107.11065).

**(b) Photon coupling.**
- CAST: g < 0.66×10⁻¹⁰ GeV⁻¹ (95%, arXiv:1705.02290).
- Chandra NGC 1275 / H1821+643: g < 6.3–8.0×10⁻¹³ GeV⁻¹ (99.7%, m ≲ 10⁻¹² eV; Reynolds et al. 2020).
- The field's mass today is about ω/t₀ ~ 10⁻³² eV, so both bounds apply.

**(c) Lepton derivative coupling.** b₀ = θ̇/2 does not depend on f.

**(d) Anisotropic birefringence.** For a field that is light during inflation, δβ = g H_I/(4π). Here H_I = 1.47×10¹³ GeV, from the GENESIS value r = 0.0035.
- ACT DR6: A_CB < 0.15×10⁻⁴ rad² (95%, arXiv:2608.27458). Its quoted g < 4.9×10⁻²/H_I was checked against this to 2%.
- SPT-3G B-modes: A_CB < 1.2×10⁻⁴ (arXiv:2510.07928).

**(e) Color anomaly.** Any c_s ≠ 0 makes θ_QCD roll.

| Hypothesis | Energy density: f < | NGC 1275: f > | ACT DR6 anisotropy: f > | Allowed f |
|---|---|---|---|---|
| STUR-B, c_γ = 8 (ω_eff = ω/399) | 8×10¹⁸ GeV | 2.3×10¹⁰ | 5.6×10¹² | **none.** θ_QCD rolls 3.1 rad (c_s = 3), for every f |
| STUR-B, c_γ = 0.02 (rate ω) | 2.0×10¹⁶ | 5.8×10⁷ | 1.4×10¹⁰ | **1.4×10¹⁰ – 2.0×10¹⁶ GeV** |
| STUR-M3a, c_γ = 3, light during inflation | 6.9×10¹⁵ – 1.4×10¹⁶ (by A₀) | 8.7×10⁹ | 2.1×10¹² | **2.1×10¹² – 6.9×10¹⁵ GeV** |
| STUR-M3a, heavy during inflation | same | 8.7×10⁹ | n/a | **8.7×10⁹ – 6.9×10¹⁵ GeV** |

### Lepton CPT-odd coupling

For M3a, b₀ ≤ 4.4×10⁻⁴¹ GeV today. That is roughly 10 orders of magnitude below laboratory sensitivity (~10⁻³¹ GeV scale; see the caveat below). It gives no constraint on any f.

### STUR's own f values

- **f = 0.74 eV (L_X = 0.8 μm)** gives g ≈ 10⁷ GeV⁻¹ for M3a. It is excluded by about 19 orders of magnitude for every hypothesis.
- **f = v_R ≈ 2×10¹⁶ GeV:**
  - M3a: Ω ≈ 0.085 at the largest A₀ (0.02 at the smallest), above the ~1% bound. Excluded.
  - STUR-B with c_γ = 0.02: Ω = 0.0099, right at the bound.
  - STUR-B with c_γ = 8: allowed by energy density, but excluded by (e).

### Strongest constraints

- **Lower edge of f:** ACT DR6 anisotropic birefringence, if the field is light during inflation; otherwise the NGC 1275 photon coupling.
- **Upper edge of f:** the early-dark-energy fraction.

### Isocurvature

A rough hand estimate for M3a (light case; not computed in the script) gives f ≲ 3–6×10¹⁶ GeV, weaker than the energy-density bound. The estimate treats the field's energy perturbation as CDM-like isocurvature, which is only approximate for a tracking component. STUR-B's phase shifts carry no first-order energy perturbation.

## Caveats and numbers not independently verified

- **Lepton b₀ bound.** The ~10⁻³¹ GeV scale is order-of-magnitude only. The search did not return the specific electron b₀/b_J table entries (Kostelecký & Russell, arXiv:0801.0287, Tables D6–D9). The conclusion holds by a margin of about 10¹⁰.
- **Early-dark-energy fractions.** These come from a fixed-sound-speed parametrization (arXiv:2107.11065; the Planck 2013 constant-Ω_e bound was < 0.010). No tracker-specific bound was found. Bounds depend on the likelihood used, and other values in the literature range from 0.0036 to 0.021.
- **NGC 1275 bound.** This is a 99.7% limit that depends on the cluster magnetic-field model. CAST (95%) is a robust but much weaker fallback: f > 1.1×10⁸ GeV for M3a.
- **ACT DR6 A_CB units.** The 10⁻⁴ rad² units were inferred from the paper's own conversion g < 4.9×10⁻²/H_I, not read from its definition.
- **Shared assumptions.** Each hypothesis's ρ ∝ 1/t² scaling is taken from its own equation of motion. The STUR-B rotation and the M3a restoring force are phenomenological and not derived from the Master Action. The "heavy during inflation" case for M3a assumes its restoring mass, of order ωH, also applies during inflation.
