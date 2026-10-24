# Scorecard re-score, 2026-10-24

**Result:** 23D + 3P + 3U + 1I = 30, 79% closure → **11D + 7P + 10U + 2I = 30, 39% closure (11D / 28 non-input rows).**

The canonical scorecard is `scripts/stur_toe_closure.py`, Part 11. It now prints the previous and the new status for every row, with the reason for each change.

## Rules

| Status | Meaning |
|---|---|
| **D** | Computed from the stated inputs, with no fitted or hard-coded constant specific to that observable, and not contradicted by another script or page in the repo. It must also stay within 20% of observation when the repo's own computed f_KK = 1.2401 replaces the hard-coded f_KK = 1.286. |
| **P** | Partial: contains an unexplained factor, or is more than 20% off. |
| **U** | Not derived, an input in disguise, no measured counterpart, or contradicted elsewhere in the repo. |
| **I** | Declared input. |

**Why f_KK is tested.** `stur_toe_closure.py:150` hard-codes f_KK = 1.286, citing "Burkeen et al.", which could not be checked. The repo's own `alpha_eff_rigorous_calculation.py` computes f_KK = 1.2401, which `rg_enhanced_mass_hierarchy.py:131` also uses. The full sensitivity run, rerunning Part 11 with 1.2401, gives:

- λ_W = 0.23332 (3.5% off, was 0.03%), still D;
- sin²θ₂₃ 20.1%, m_τ/m_t 20.7%, both over 20%;
- m_c/m_t 34% and m_u 50%, both already P;
- Δm²₂₁ 2%.

To reproduce, replace `f_KK     = 1.286` with `f_KK     = 1.2401` in a copy of the script and run it.

## Row by row

| # | Observable | Previous | New | Evidence | Reason |
|---|---|---|---|---|---|
| 1 | N_gen = 3 | D | D | `stur_toe_closure.py` Part 11 | Topological count; nothing in the repo contradicts it |
| 2 | Gauge group | D | **P** | `scripts/stur_maxwell_equations.html:84` | SM selection via MHP is asserted; the gauge field's origin is "not separately derived" |
| 3 | θ_QCD = 0 | D | **U** | `scripts/stur_strong_cp_solution.html:432`; `docs/GENESIS_V10F_THEORY_GAPS.md` | The repo's own radiative estimate, θ_eff ≈ 8.6×10⁻⁸, is about 860× the nEDM bound of 10⁻¹⁰. The R-phase also carries a color anomaly, c_s = 3 |
| 4 | Berry phase = 0 | D | **U** | `BERRY_PHASE_RIGOROUS_PROOF.md:19` | No measured counterpart; the repo elsewhere uses a nonzero Berry phase, γ = −π/3 |
| 5 | Proton stable | D | D | Part 11; README predictions | Consistent with τ_p bounds |
| 6 | Normal ordering | D | D | Part 11 | Prediction; current data mildly prefer normal ordering. Not yet decisive (JUNO) |
| 7 | KK-parity | D | **U** | Part 11 ("observed —"); commit `73a36ae` | No measured counterpart; the mechanism was since renamed KK-triality |
| 8 | α = Z₀/(2R_K) | D | **I** | `stur_toe_closure.py:63` | Definitional identity (Z₀ = μ₀c, R_K = h/e²) on α_em, one of the four declared inputs |
| 9 | λ_Cabibbo | D | D | `stur_toe_closure.py:182` | 0.03% with f_KK = 1.286; 3.5% with the computed 1.2401. The headline precision rests on the hard-coded constant |
| 10 | δ_CKM | D | D | `stur_toe_closure.py:216` | 4.2% (3.6% with the computed f_KK) |
| 11 | η̄ | D | D | `stur_toe_closure.py:229` | 13.4% (13.1%). Fitted f_hol already removed. The 0.424 overlap ratio and the e^(−1/6) holonomy factor have derivations in the repo, though `f_hol_*` scripts give competing values |
| 12 | \|V_ub\| | D | D | `stur_toe_closure.py:233` | 3.8% |
| 13 | \|V_cb\| | D | D | `stur_toe_closure.py:234` | 0.9% |
| 14 | sin²θ₁₃ | D | D | `stur_toe_closure.py:375` | 10% (16% with the computed f_KK) |
| 15 | sin²θ₂₃ | D | **P** | `stur_toe_closure.py:377` | 19.4% only with the hard-coded f_KK; 20.1% with 1.2401 |
| 16 | δ_CP(PMNS) | P | P | `stur_toe_closure.py:378` | 38.5% |
| 17 | Δm²₃₁ | D | **U** | `stur_toe_closure.py:447-456` | Hard-coded anchor √(2.453×10⁻³) eV²; M_R0 cancels. The script's own honesty note says so |
| 18 | M_DM | U | U | Part 9 note | Fixed by requiring Ω_DM h² = 0.12 |
| 19 | Ω_DM h² | U | U | Part 9 note | Tautological |
| 20 | M_R | D | **U** | `stur_toe_closure.py:445` | M_R0 = 3·1.5·√3·1.2·2.1×10¹³ GeV, a product of unexplained constants; "~10¹⁴" is not a measurement |
| 21 | Λ_CC | D | **U** | `stur_toe_closure.py:680-690`; `BERRY_PHASE_RIGOROUS_PROOF.md:6`; `cosmological_constant.py:356` | Built on the hard-coded neutrino masses (to the 4th power) and the fitted F_Berry = 1/(4π²); `cosmological_constant.py` states "The CC is NOT computed from the STUR framework" |
| 22 | m_b/m_t | D | D | `stur_toe_closure.py:711` | 10.4% (0.7% with the computed f_KK) |
| 23 | m_τ/m_t | D | **P** | `stur_toe_closure.py:717` | 12.9% only with the hard-coded f_KK; 20.7% with 1.2401 |
| 24 | m_c/m_t | P | P | `stur_toe_closure.py:548` | 21% (34% with the computed f_KK); also depends on the unexplained M_R0 through ln(M_R0/m_t) |
| 25 | ω = 2π² | D | **U** | `stur_toe_closure.py:185-188`; `DERIVATION_CHAIN_INFINITY.md:644` | Tautology: κ_q ≡ (2π/3)/σ_q, so 3κ_qσ_q = 2π identically; ω = πS is a stated ansatz. The "observed" value is its own prediction |
| 26 | r | U | U | `genesis_v10_r_from_action.py` | 0.043, excluded |
| 27 | sin²θ₁₂ | D | D | `stur_toe_closure.py:376` | 19% (17.5% with the computed f_KK) |
| 28 | Δm²₂₁ | D | **P** | `stur_toe_closure.py:466` | The ratio λ_l²/2 is derived; the absolute scale is inherited from the hard-coded Δm²₃₁ |
| 29 | m_u | P | P | `stur_toe_closure.py:567` | 26% (50% with the computed f_KK) |
| 30 | M_Pl, v, m_t, α | I | I | — | Declared inputs |

## Not changed, but noted

- **The CKM chain's e^(−1/6) and the (1 + π/4) Gerono factor** have stated derivations in the repo. The `f_hol` family of scripts disagree about the holonomy factor (0.948 fitted, 0.846 from geometry, "undetermined"). Rows 10–13 stay D because the canonical chain uses the repo-supported f_hol = 1.000.
- **Normal ordering and proton stability** are predictions consistent with current data, not precision measurements.
- **R-charged quarks make the R-phase a QCD axion.** The theory-gap analysis shows quarks carry R-charge (c_s = 3). That sharpens row 3: a QCD axion would relax θ dynamically, which contradicts the repo's "no axion" claim. Resolving it is a theory question, not a scoring one.
