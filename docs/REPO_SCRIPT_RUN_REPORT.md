# Repo script run report (pre-GENESIS-v10 scripts)

**Date:** 2026-10-23
**Scope:** every `scripts/*.py` except `genesis_v10*.py` and `genesis V10 Light Bird` (33 scripts), plus the browser test suite in `tests/`.
**Environment:** Python 3.13, NumPy 2.5.3, SciPy 1.18.1; 4 CPU cores; `MPLBACKEND=Agg`.
**Method:** Scripts were run unmodified and nothing was fixed.

- **Pass 1:** 6 in parallel, 300 s timeout each.
- **Pass 2:** the 16 pass-1 timeouts were rerun 4 at a time, with single-threaded BLAS and a 900 s timeout.

The pass-1 timeouts were caused by BLAS thread oversubscription on 4 cores: every timed-out script had stopped mid-calculation, not hung, and 15 of 16 finished in pass 2.

**Result:** 32 ok, 0 crashed, 1 timeout (`alpha_eff_rigorous_calculation.py`, still running at 900 s). Only `stur_numerical_verification.py` has real pass/fail self-tests; it passes 10/10. Most scripts print a status label or scorecard instead.

## Results

| Script | Status | Runtime | Key outputs | Issues |
|---|---|---|---|---|
| alpha_eff_rigorous_calculation.py | **timeout** (300 s and 900 s) | >900 s | stops in "FACTOR 1: twisted sector enhancement" | too slow to verify |
| berry_phase_exact.py | ok (pass 2) | 253 s | "f_Berry = 0.975 is NOT DERIVED — it is FITTED" | conflicts with f_Berry = 1.000 "PROVED" (f_hol_confined_derivation.py) and 1/(4π²) (BERRY_PHASE_RIGOROUS_PROOF.md) |
| brane_yukawa_hierarchy.py | ok | 3 s | m_t/m_b ~ 10–40 (obs 41); "EXACT mass values: cannot be derived without fitting" | contradicts the README's "<2%" masses |
| chronomagnetics_closure.py | ok (pass 2) | 314 s | scale "FITTED — not derivable"; 6 derived + 5 partial (older scorecard) | old scorecard |
| ckm_full_diagonalization.py | ok (pass 2) | 269 s | f_hol = 0.846 "from geometry", f_screen = 0.6956 | f_hol value conflicts with f_hol_dynamical.py |
| cosmological_constant.py | ok | 0.2 s | "STATUS: The CC is NOT computed from the STUR framework" | **contradicts README Λ_CC = D (7–10.8%)** |
| f_RG_formal_proof.py | ok | 1.7 s | f_RG = 1.0029 "PROVED"; old 0.970 wrong | — |
| f_RG_kk_threshold.py | ok | 1.6 s | f_RG = 1.0026 | consistent with above |
| f_hol_confined_derivation.py | ok | 1.8 s | f_hol = 0.948 "conditionally derived"; f_Berry = 1.000 "PROVED" | f_Berry conflict (see berry_phase_exact) |
| f_hol_dynamical.py | ok (pass 2) | 72 s | "f_hol is UNDETERMINED"; 0.948 was FITTED; 0.847 Haar is WRONG | conflicts with ckm_full_diagonalization / stur_first_principles_calculation (0.846) |
| f_hol_phase_correction.py | ok | 1.6 s | "HONEST STATUS: f_hol is FITTED (0.948)" | — |
| f_screen_first_principles.py | ok (pass 2) | 83 s | f_screen "NOW DERIVED" | — |
| fermion_mass_hierarchy.py | ok (pass 2) | 18 s | geometry "QUALITATIVELY explains"; masses "NOT derived but FITTED" | contradicts README masses |
| five_open_problems_closure.py | ok (pass 2) | 3 s | scorecard 8 D + 23 P | old scorecard |
| generation_splitting_hosotani.py | ok (pass 2) | 4 s | v·L scan tables | no conclusion printed |
| infinity_helix_dynamics.py | ok | 290 s | ⟨M⟩ = 0.636, \|δθ\|_rms = 0.83° | uses λ = 3722/2705, not the v7.0 e^{1/π} |
| lx_effective_potential.py | ok | 1.7 s | "accept that L_X is an INPUT parameter… single biggest open problem" | **contradicts "L_X ≈ 0.8 μm (derived)"** |
| lx_flux_stabilization.py | ok | 11 s | "L_X remains an input parameter with moderate fine-tuning" | same |
| mass_spectrum_full.py | ok | 80 s | max 3rd/2nd mass ratio ~19 vs needed 45–136; "falls short of the full hierarchy" | contradicts README masses |
| rank1_yukawa_mass_spectrum.py | ok | 19 s | m₂/m₁ ~ π/α_s ~ 10–30; absolute scale unfixed | — |
| rg_enhanced_mass_hierarchy.py | ok | 130 s | κ enhancement factor 1.188 | — |
| stur_first_principles_calculation.py | ok (pass 2) | 218 s | f_holonomy = 0.846 (Haar) | f_hol conflict |
| stur_inflation.py | ok | 3 s | r_eff = 0.0139 [D], n_s = 0.9667 | r is a slip: consistent value 0.043, excluded (see genesis_v10_r_from_action.py) |
| stur_numerical_verification.py | ok (pass 2) | 35 s | **Tests passed 10/10**; κ = 2.433 ± 0.062 | only script with real unit tests |
| stur_paper_bridge_closure.py | ok | 233 s | 6 derived + 6 partial + 16 calibrated + 1 input = 29 | old scorecard |
| stur_refinement_v7.py | ok | 300 s | CKM A = 0.6545 (21%), Δm²₂₁ ~ 10⁻³⁵ eV², δ_CP 270°; points to a "31D+1I=32" scorecard | values superseded; 31D+1I=32 appears nowhere else |
| stur_resistance_physics.py | ok (pass 2) | 11 s | ERP tables | — |
| stur_toe_closure.py (canonical) | ok (pass 2) | 34 s | **24 D + 3 P + 2 U + 1 I = 30, 83%** (matches README); λ_W = 0.22543; Λ_CC D 7%; Δm²₃₁ D 2.3% | Δm²₃₁ is hard-coded (finding 2); Λ_CC D contradicts cosmological_constant.py |
| stur_v71_closure.py | ok (pass 2) | 18 s | 24 D + 3 P (29 incl. input); m_u half-cell gives 188 MeV (U) | — |
| stur_v7_full_closure.py | ok (pass 2) | 25 s | "24D + 3P + 1U + 1I = 29"; "strongest: λ (1.6%), Δm²₃₁ (0.4%)" | 29 vs 30 observables; λ 1.6% vs canonical 0.03%; Δm²₃₁ hard-coded |
| three_pillar_toe_closure.py | ok | 211 s | 8 D + 17 P + 2 C + 2 U + 1 I = 30 (v6.3); λ = 0.22787 "D" | m_u = 806 MeV, m_e = 8.3 MeV, Δm²₃₁ = 2.2×10⁻¹⁰ labelled **P** |
| toe_closure_calculations.py | ok (pass 2) | 98 s | "12/26 parameters derived = 46%"; "~65% derived" | yet another closure figure |
| toe_closure_first_principles.py | ok | 191 s | λ = 0.22870 (Partial); PMNS and Δm² rows "Calibrated" (exact matches) | — |

**Browser tests** (`tests/stur-tests.js`, run headless in Node 22 with a stub `window`, loading `assets/js/stur-version.js` first as `tests/index.html` does): **31 passed, 3 failed**.

1. **"Gaussian Visibility: Always positive"** (`tests/stur-tests.js:98-101`). exp(−900) underflows to 0 in float64. This is a test bug, not physics.
2. **"Theory Status: 3 axioms"** (`:130`) expects 3, but `assets/js/stur-version.js:23` sets `axiomCount: 1`.
3. **"Version: Axiom-free status (v2.4)"** (`:359`) expects 0.

Tests 2 and 3 contradict each other, so no value of `axiomCount` can pass both. The site metadata also prints "v2.4 | Axiom-Free" (`stur-version.js:357-358`), while the README describes v7.0 with 3 axioms.

## Findings

1. **Λ_CC and L_X are listed as derived, but the repo's own scripts say they are not.**
   - `cosmological_constant.py` concludes "The CC is NOT computed from the STUR framework. It remains an input parameter".
   - `lx_effective_potential.py` and `lx_flux_stabilization.py` both conclude L_X is an input parameter, "the single biggest open problem".
   - The canonical scorecard still counts Λ_CC as D (7%) (`stur_toe_closure.py` output, scorecard row Λ_CC). README and `stur_master_action_derivation.html` §4 present L_X ≈ 0.8 μm as derived from M_Pl.

2. **Δm²₃₁ is hard-coded, but scored as derived.**
   - `stur_toe_closure.py:456` sets `m_nu3_atm = np.sqrt(2.453e-3)`, and its own note at lines 447–455 says M_R0 cancels. So the "2.3% from PDG" is the gap between a literature constant and PDG.
   - `README.md:226` lists it as D, and `stur_v7_full_closure.py` calls Δm²₃₁ a "strongest prediction" (0.4%).
   - Δm²₂₁ (= λ_l²/2 × Δm²₃₁) and Σm_ν inherit this anchor.

3. **The correction factors have mutually contradictory values and statuses across scripts.**
   - **f_hol:** 0.948 FITTED (`f_hol_phase_correction.py`, `f_hol_dynamical.py`); 0.846 "from geometry" (`ckm_full_diagonalization.py`, `stur_first_principles_calculation.py`); "UNDETERMINED, Haar 0.847 is WRONG" (`f_hol_dynamical.py`).
   - **f_Berry:** 0.975 FITTED (`berry_phase_exact.py`); 1.000 "PROVED" (`f_hol_confined_derivation.py`); 1/(4π²) (`BERRY_PHASE_RIGOROUS_PROOF.md`, itself flagged fitted).
   - Separately, `stur_toe_closure.py:445` defines an unrelated `f_hol = 3*1.5*np.sqrt(3)*1.2*2.1`, a product of unexplained constants that sets the M_R scale.

4. **The fermion-mass claims are not supported by the mass scripts.**
   - The README says most charged-fermion masses are derived to <2%.
   - `mass_spectrum_full.py`: maximum 3rd/2nd-generation ratio ~19, "falls short of the full hierarchy".
   - `fermion_mass_hierarchy.py`: masses "NOT derived but FITTED".
   - `brane_yukawa_hierarchy.py`: "EXACT mass values: cannot be derived without fitting corrections".
   - `three_pillar_toe_closure.py` labels m_u = 806 MeV (PDG 2.16), m_e = 8.3 MeV and Δm²₃₁ = 2.2×10⁻¹⁰ as **P**.

5. **Many incompatible scorecards are shipped as runnable scripts.**
   - 24 D + 3 P + 2 U + 1 I = 30 (canonical, `stur_toe_closure.py`)
   - 24 D + 3 P + 1 U + 1 I = 29 (`stur_v7_full_closure.py`)
   - "31D+1I=32" (`stur_refinement_v7.py`)
   - 8 D + 17 P + 2 C + 2 U + 1 I (`three_pillar_toe_closure.py`)
   - 8 D + 23 P (`five_open_problems_closure.py`)
   - 6 + 6 + 16 calibrated (`stur_paper_bridge_closure.py`)
   - "12/26 = 46%" (`toe_closure_calculations.py`)
   - Cabibbo λ appears as 0.22543 (canonical), 0.22787 "D" (three_pillar), and 0.22870 "Partial" (toe_closure_first_principles).
   - Nothing marks which scripts are superseded.

**Also noted:**
- `stur_inflation.py`'s r_eff = 0.0139 is a slow-roll slip; the consistent value is 0.043, excluded by BICEP/Keck (see `genesis_v10_r_from_action.py`).
- `infinity_helix_dynamics.py` still uses λ = 3722/2705 rather than e^{1/π}.
- `alpha_eff_rigorous_calculation.py` could not be verified within 900 s.
