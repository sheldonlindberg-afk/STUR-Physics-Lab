# Red-team audit: bos_se (bosonic one-loop Σ_AA, Σ_AZ, Σ_ZZ, Σ_W; 't Hooft-Feynman gauge, MS-bar, CDR)

Auditor's scratch work is in `.../scratchpad/audit-bos_se/`: `indep.py` is the independent derivation, `run2.py` to `run5.py` are the checks, `mutants/` holds the 20 mutant directories and their gate logs, and `checks_*.log` are the runs of the proposed checks.
I read and ran the code of builds a and b and the reference. Everything independent below uses none of their code and none of the reference's formulas.

Classes: **B** = a defect in a build. **R** = a SPEC ambiguity, where a correct build could legitimately resolve something differently. **C** = an oracle or check gap. **N** = a note or a positive result.

## 1. Independent verification of the result (task 1)

**Route.** I did my own derivation of the full Σ_W and Σ_ZZ, and also of Σ_AA and Σ_AZ, in exact d:
* I wrote my own small Lorentz-tensor contractor with symbolic d.
* I wrote my own Passarino-Veltman reduction to A0 and B0. Symmetric integration is done in d dimensions, and the O(ε) part of every d-dependent coefficient is multiplied against the pole.
* I wrote my own Re B0 by Feynman-parameter quadrature.
* The Feynman rules are my own hand rules, in the SPEC's field conventions:
  * D = ∂ − i e Q A − i (g/c)(T3 − s²Q) Z
  * W±φ∓V couplings M_W (a⁺_V + a⁰_V)
  * quartic terms from −¼F², derived explicitly
  * the ghost loop with its −1
  * symmetry factors ½ for identical neutral fields in seagulls

The diagram classes are:
* VV bubbles
* ghost loops, two orientations each
* VS bubbles: (γφ), (Zφ), (WH), (Zφ)×2, (ZH)
* SS bubbles: (φH), (φχ), (φ⁺φ⁻), (χH)
* seagulls: WWWW, WWZZ, WWAZ, WWHH, WWχχ, WWφφ, and the ZZ, AA and AZ analogues

**Calibration of the machinery against textbook results:**
* The massless gauge-plus-ghost loop gives Π_T = (3d−2)/(d−1) k² B0. That is 5/3 B0 + 1/9 per C_A, the known 5/3 L + 31/9.
* k·Π·k = 0, so the massless result is transverse.
* The complex-scalar loop gives −(1/3)(B0 + 2/3), the known 8/9.

**Result: agreement.** My Σ_AA, Σ_AZ, Σ_ZZ and Σ_W agree with the reference, and with both builds, to the last double-precision bit (relative difference 0.0) at 8 points:
* k² = −5 M_W², −1000, 0.3 M_W², M_W², M_Z², 2.5 (M_W+M_Z)², 5·10⁴ (with M_H = 10⁴ GeV) and −10⁸ GeV²
* three mass and μ sets, including M_W = 75 and M_Z = 91.19 GeV

They also agree at the exact thresholds 4M_W², (M_W+M_Z)², (M_W+M_H)², (M_Z+M_H)² and 4M_Z². In particular:
* **Signs:** both the overall sign Σ = −Π and the sign of Σ_AZ in the SPEC's photon-field convention are confirmed independently. My Σ_AZ equals −Σ_AZ(Denner), which confirms the oracle's sign flip.
* **Rational terms:** the rational (non-log) terms of Σ_W and Σ_ZZ are confirmed, including the M_W² and M_Z² rational terms, which the oracle docstring says were previously "checked only by the builds agreeing with the oracle".

**Two further identities that are independent of everything.** Both builds pass both of them; they are in `audit_proposed_checks.py`.
* **Large-|k²| asymptotics.** At k² = −10¹² against the massless textbook coefficients (SU(2) gauge plus doublet, and the hypercharge scalar part), the relative agreement is 9·10⁻⁹. The deviation falls off like M²/k², as it should.
* **Custodial limit g' → 0 at fixed g.** Σ_ZZ − Σ_W = O(s²) is observed: 2.2·10⁻⁷ at s² = 10⁻⁷. Σ_AZ = O(s) is also observed.

**What this does not cover:**
* My vertex magnitudes are textbook values that I re-derived by hand. They are not an automated extraction from the Lagrangian, and the builds' extraction was automated. One rule I first recalled with the wrong sign: the W⁺W⁺W⁻W⁻ quartic vertex. I caught it by deriving it explicitly in the real basis, which shows that recalled rules are a real risk.
* I did not re-check the full Δr. The orchestrator's statement that the bosonic Δr is UV finite and μ independent is unverified by me.

## 2. SPEC review (task 2)

| # | Class | Finding |
|---|---|---|
| R1 | R | **Literal reading of the Σ_AZ sign.** SPEC §2 defines the diagonal entries by the propagator −i g/(k² − M² + Σ). The literal inverse of that is +i g (k² − M² + Σ). SPEC then puts "−i g^{μν} Σ^{AZ}_T in the inverse propagator matrix". Read literally, against the diagonal entries, this makes Σ_AZ(SPEC) = −(the same-sign convention as the diagonal), which is the opposite of what the oracle pins. The oracle's choice is right only if "inverse propagator matrix" is read as Denner's vertex function Γ = −i g (k² − M² + Σ). Build a noticed this (QUESTIONS 1) and chose the vertex-function reading; build b chose the same without comment. **Fix:** replace the phrase with "the two-point vertex function Γ^{VV'}_{μν} = −i g_{μν}[(k² − M_V²)δ_{VV'} + Σ^{VV'}_T] + (longitudinal)". |
| R2 | N | **Photon-field sign.** SPEC §1 pins D = ∂ − i g W τ/2 − i g' B/2 and A = sW3 + cB. Together these fix the sign of Σ_AZ, and the oracle's flip relative to Denner follows from the SPEC text. I verified this independently (section 1). |
| R3 | N | **Sign of Σ.** It is unambiguous: the propagator plus "positive Σ lowers M²" give Σ = −Π for the diagonal entries. |
| R4 | N | **Tadpoles.** The exclusion is clear: only Higgs one-point insertions are excluded, and the seagulls are kept. The Goldstone masses are ξM² at the tree minimum, so no ambiguity remains. |
| R5 | N | **d-dimensional rules.** CDR, g^μ_μ = d, and the O(ε) × pole rule are stated. The MS-bar normalisation is equivalent to A0 = m²(Δ + 1 − ln m²/μ²), and the differences between MS-bar variants are O(ε) at one loop. |
| R6 | N | **k² = 0, thresholds, real parts and λ → 0.** All are clearly stated. No B0' or IR pole appears in these functions. |
| R7 | C | SPEC gives no range for M_H, μ or c_W, but the oracle tests only M_H in [1, 10⁹] at 8 points, μ in [1, 10⁴], and three values of c_W. A correct build has no reason to be limited, so this is harmless for correct builds and is only a coverage gap (section 3). |
| R8 | C | SPEC §4 says "keep any high-precision setting local", but nothing enforces it. `own_precision_check` reloads the module at dps = 15 and never checks that dps is still 15 afterwards (mutant M13 survives). |
| C1 | C | **Oracle over-strict at exact zeros of the reference.** `_dev` uses the floor 1e-9 α M_W² together with the tolerance 1e-9. At Σ_AA(0) (always zero) and at Σ_AZ(0) for μ = M_W (B0(0, M_W, M_W) = 0), this demands \|Σ\| < 5·10⁻¹⁷ GeV², which is about 10⁻¹⁸ α M_W². A correct build that sums diagrams in double precision leaves roundoff of about 10⁻¹⁵ to 10⁻¹⁴ α M_W² and is rejected, while it passes the blind Ward check (< 10⁻¹²). Control mutant M14 (Σ_AA(0) = 10⁻¹⁵ α M_W²) fails `grid_check` and `mu_check`. Both builds pass only because they evaluate at 50 or more digits. **Fix:** use the absolute floor 1e-3 α M_W² in `_dev`, which with the 1e-9 tolerance means 10⁻¹² α M_W² absolute (`grid_check_absfloor`), and do the same in `mu_check`. |

## 3. Mutants (task 3)

All mutants are build b with one export overridden by an appended wrapper, `bos_se.py` plus `DERIVATION.md`. Each was run with `python3 gate.py --mode verifier --campaign bos_se --oracle bos_se/oracle.py <dir>`. **No mutant failed the blind tier.** Every kill came from the oracle tier.

| Mutant | Error | Gate | Killed by (oracle) | Proposed check that kills it |
|---|---|---|---|---|
| M01 | Σ_W rational term + k²/(9 s²) | FAIL | grid, high-k², M_H, μ | – |
| M02 | Σ_W without the (u±, u^Z) ghost loops | FAIL | grid, high-k², M_H, μ, own precision | – |
| M03 | Σ_W φ⁺φ⁻ seagull with g²/4 instead of g²/2 | FAIL | grid, high-k², M_H, μ, own precision | – |
| M03b | Σ_ZZ φφ seagull with (c² − s²) instead of (c² − s²)² | FAIL | grid, high-k², M_H, μ | – |
| M04 | sign of the (W, H) bubble flipped only for M_H > 10³ GeV | FAIL | M_H (5·10³ point), own precision | – |
| M05 | Σ_W + M_H²/(120 s²) only for M_H > 10⁵ GeV | FAIL | M_H, own precision | – |
| **M05b** | the same, only for 1.5·10⁵ < M_H < 9·10⁵ GeV | **PASS** | – | `dense_higgs_mass` |
| M06 | Σ_ZZ wrong k² rational term only for k² < 0 | FAIL | grid, μ | – |
| **M06b** | the same, only for k² < −5·10⁴ GeV² | **PASS** | – | `asymptotic_spacelike` (reference-free) |
| M07 | O(ε) part of (d − 1) in the WWWW seagull dropped | FAIL | all five | – |
| M08 | Σ_ZZ with μ² → μ M_W (exact at μ = M_W) | FAIL | grid, μ | – |
| M09 | Σ_AZ sign flipped (Denner's photon convention) | FAIL | grid, high-k², μ | `asymptotic_spacelike` also kills it |
| M10 | all four with Σ = +Π | FAIL | all five | – |
| M11 | Σ_AA × 1.001 (Ward identity still exact) | FAIL | grid, high-k², μ | – |
| **M12** | Σ_W 1% wrong above the W-H threshold, only for M_H > 200 GeV | **PASS** | – | `heavy_higgs_above_threshold` |
| **M13** | sets the global `mp.dps = 40` at import (violates SPEC §4) | **PASS** | – | `global_precision_untouched` (reference-free) |
| M14 | CONTROL, not wrong: Σ_AA(0) = 10⁻¹⁵ α M_W² (roundoff) | FAIL | grid, μ | wrongly rejected; passes `grid_check_absfloor` (C1) |
| **M15** | Σ_W wrong constant only for μ > 2·10⁴ GeV | **PASS** | – | `wide_mu` |
| M16 | c_W hard-coded to 80.38/91.19 in Σ_ZZ | FAIL | grid | – |
| **M17** | Σ_ZZ Goldstone-seagull error proportional to (c² − c₁²)(c² − c₂²)(c² − c₃²), which vanishes at the three oracle c_W values | **PASS** | – | `custodial_limit` (reference-free), `mass_ratio_off_sm` |

**Totals:**
* 19 mutants are genuinely wrong. The oracle kills 13 of them, and 6 survive: M05b, M06b, M12, M13, M15 and M17.
* Every survivor is a parameter region the oracle does not sample, or a SPEC rule it does not enforce. None is an error at the benchmark point.
* All 6 survivors are killed by the checks in `audit_proposed_checks.py`.
* The checks pass both builds: build a and build b pass all 8. The worst deviations are 8.8·10⁻⁹ (asymptotic), 2.2·10⁻⁷ (custodial, which is O(s²) as required) and 1.4·10⁻¹⁴ (dense M_H). The others are 0.
* The control M14 shows the over-strictness in C1.

## 4. Findings summary

* **B:** none. I found no defect in either build.
* **R1:** the SPEC text about the inverse propagator for Σ_AZ contradicts the oracle's sign under a literal reading, and needs rewording. Both builds and the oracle use the vertex-function reading, which my independent derivation from the SPEC's field definitions also supports under the Σ = −Π convention.
* **C1:** the oracle is over-strict at exact zeros of the reference (Σ_AA(0), and Σ_AZ(0) at μ = M_W). It could reject a correct double-precision build.
* **C2, coverage gaps** (each with a proposed check):
  * large spacelike k² (the oracle goes down only to −5 M_W²)
  * windows in M_H between the oracle's points
  * above-threshold values only at M_H = 125 GeV
  * μ only in [1, 10⁴] GeV
  * only three values of c_W, with no custodial or off-SM test
  * the "local precision" rule of SPEC §4 is not enforced
* **C3:** the blind tier kills none of the 19 wrong mutants. This is expected for a blind tier, but two reference-free checks are strong and could be moved into `campaign.BLIND` without leaking the answer: the custodial limit and the large-k² textbook asymptotics. Moving the asymptotic check would reveal the leading k² ln coefficients, which are textbook values anyway.
* **N:** independent exact-d confirmation of all four self-energies, including the signs and rational terms of Σ_W and Σ_ZZ and the sign convention of Σ_AZ (section 1).

## 5. Verdicts

* **Build a: PASS.** It is correct, as checked by my independent derivation, the textbook asymptotics, the custodial limit and the six reference-based extended checks. It keeps its precision local.
* **Build b: PASS.** The same holds for build b: bit-identical results to build a and the reference at every point I sampled. It keeps its precision local.

**Not verified:**
* the builds' DERIVATION.md prose beyond spot reading
* M_H > 10⁹ GeV, except through the oracle's own-precision points at 10¹⁰ and 10¹⁴ GeV
* the full on-shell Δr
* gauge-parameter independence, which is not applicable: the result is defined in Feynman gauge only
