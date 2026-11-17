# AUDIT: campaign greybody (Hawking power per degree of freedom, Schwarzschild), builds a and b

Auditor (red team). I edited nothing in the repository or in the builds. All scripts below are in this directory.
They ran on copies of the builds (`copies/a`, `copies/b`) with bytecode writing off. Mutants are in `mutants/<name>/`,
each with its verifier-gate output (`gate_stdout.txt`, `gate_report.json`) and the proposed-check output (`proposed_out.txt`).

Paths:
* SPEC, campaign and oracle: `/home/user/STUR-Physics-Lab/rebuild/campaigns/greybody/`.
* a = `.../scratchpad/room-greybody-a/builds/greybody-a/greybody.py` (Opus).
* b = `.../scratchpad/room-greybody-b/builds/greybody-b/greybody.py` (Sonnet).

## 0. What I verified independently (not just re-ran)

| Item | How | Result |
|---|---|---|
| Fermion potential | by hand: dW/dr = k[f_r/(2√f r) − √f/r²] = −k(1−3/r)/(r²√f), so dW/dr* = k√f(3/r − 1)/r² | a:39,49 (V₊ = W² + dW/dr*) and b:64 with σ = −1 (V = W² − dW/dr*, i.e. a's V₋) are both correct. Γ(V₊) = Γ(V₋) to 1e-11 (a `main_out.txt`, my `fermion_loww.py`) |
| Far-field recurrence | own derivation: ψ_ε = e^{iεωr*}u gives (f u_r)_r + 2iεω u_r − (V/f)u = 0, then collect r^{−n−2} | **2iεω(n+1)a_{n+1} = n(n+1)a_n − 2(n²−1)a_{n−1} − Σ_{p=2}^{n+2} v_p a_{n+2−p}**. Matches a:77,89–94 including its R-scaled form. Matches b:41–46 after m = n+1, since (m−1)²−1 = m(m−2). The f^{−1/2} coefficients C(2m,m)/2^m (a:58–65, b:23–29) are right |
| Horizon BC | ψ = e^{−iωr*}(1 + c f), c(κ_h² − 2iωκ_h) = V₁ with κ_h = 1/2 | a's c = V₁/(1/4 − iω) (a:120–124) is right. For fermions V ≈ σk√f/8, so the leading correction is O(√f), not O(f) (see §5) |
| Γ = 1/\|A_in\|² | Wronskian flux argument | right in both. The 2×2 matching (a:148–156, b:88–100) is right |
| SPEC §3 assembly | read line by line | right in both: T = 1/(8π) (a:14, b:14); FD sign (a:202, b:151); 1/(2π) (a:220,223, b:152); (2j+1) and j ≥ s (a:177,187,220; b:121,131,152) |
| **Γ itself, by a different route** | `indep.py`: no asymptotic series. Local first-order WKB projection at R = 2000/ω, A ∝ [(ik − k'/2k)ψ − ψ']/(2ik) with k = √(ω² − V), and its own horizon start (O(√f) fermion correction included). `compare_gamma.py`: 132 points, s ∈ {0, ½, 1, 2}, j = s, s+1, s+3, ω = 0.001…2.4 | a vs mine: ≤ 3e-9 for all bosons; fermions ≤ 1e-9 for ω ≥ 0.02 and ~1e-7 at ω ≤ 0.005. b vs a: ≤ 1e-8 for bosons, **up to 1.4e-4 for fermions** (§5) |
| **P_s, by a different route** | `indep_power.py`: own Γ, own quadrature (8 panels, 20 Gauss nodes, ω ≤ 2.6), j summed to 1e-11 | 7.43868693871e-5, 4.09165271219e-5, 1.68192739347e-5, 1.91836996439e-6. a agrees to 1.6e-11, 1.4e-11, 3.8e-10, 9.6e-10. b agrees to 1.5e-9, 2.5e-8, 2.3e-8, 3.4e-7 |
| Exact low-frequency coefficients | Page 1976 / Starobinsky for a = 0: bosons Γ → 4C²(2ω)^{2l+2}; fermions Γ → C²(2ω)^{2l+1}; C = (l−s)!(l+s)!/((2l)!(2l+1)!!). Richardson-extrapolated from ω = 0.001, 0.002 | 8 cases (s,l) = (0,0),(0,1),(½,½),(½,3/2),(1,1),(1,2),(2,2),(2,3): both builds within 3e-4 (the residual is the ω² term) |
| Oracle unit | ħc⁴/G² = 1.9123e29 g³/s, so UNIT = 2.7925e-4 | oracle.py:6 is right |

**Conclusion of §0.** Both builds solve the SPEC correctly. P_s is now known to about 1e-9 from two routes that share
only the SPEC postulates: a's series matching and my series-free WKB projection. The findings below concern how
little the gate itself proves, and some inaccurate claims.

## 1. Provenance honesty and hidden answers

* **No lookup tables, no answer-like literals, no argument-dependent branches** in either build.
  * I grepped both for the gate's probe arguments (0.005, 0.2, 0.37, 1.0, …). The only constants are numerical
    knobs: r*_min = −80, R rules, node counts, panel edges.
  * The R and d0 rules (a:104–106; b:70–73) are smooth functions of (j, ω).
  * The near-horizon and asymptotic parts use the SPEC potentials only.
* **Caching.** `functools.lru_cache` on Γ and on P (a:160,231; b:104,156) is plain memoisation.
  * It does mean `b_convergence_independent_of_call` (campaign.py:62) is satisfied by the cache, whatever the numerics
    do. A noisy implementation would pass it. **Low**, weak check.
* **a clips Γ (a:163, `min(1.0, …)`).** PROVENANCE a:20 does not mention it, and DERIVATION a §1 says
  "Γ ∈ [0, 1] automatically".
  * It is active: 126 of the 3886 Γ evaluations in a's power grid return exactly 1.0 (`record_grid.py`, `grid_a.json`,
    `offline_mutants.py`). The unclipped values are 1 + O(1e-10), from the ODE tolerance.
  * The numerical effect is nil. But the clip blinds the gate's only bound check, `b_range` (campaign.py:18), for build a.
  * **Low.**
* **PROVENANCE notes otherwise match the code**, both builds. b:11 and a:22 describe the quadrature that actually runs.
* **Documentation drift in b.**
  * The j cut is "Γ_j < 1e-14" in DERIVATION b step 4 but 1e-15 in the code (b:125,143).
  * The series truncation is "< 1e-17" in the DERIVATION but 1e-19 in the code (b:49).
  * **Low.**

## 2. Derivation vs code, SPEC conformance

* Everything in the §0 table conforms to SPEC §§1–3 in both builds.
* **b's transmission accepts non-physical arguments (b:110–118).**
  * There is no guard for j < s: Γ(1, 0, 0.3) = 1.000000000025, and Γ(2, 1, ·) and Γ(0.5, 0, ·) return values.
  * There is no guard for ω ≤ 0: ω = 0 raises ZeroDivisionError, and ω < 0 returns Γ(|ω|).
  * a returns 0 for these (a:170–173).
  * The SPEC exports only physical j, and the sums never call these arguments. **Low.**
* **a's DERIVATION §5 low-ω derivation is only a sketch.** It does not reach the general-spin coefficients that §0 shows
  are reproduced. It is used only as a check, as a says. **Info.**

## 3. Independence

* **a and b are the same method.**
  * Both integrate outward from an ingoing horizon state.
  * Both match at finite R to the same 1/r asymptotic series (one in r^{−n} with R-scaling, one in x = 1/r).
  * Both use DOP853 at rtol 1e-11 and Gauss–Legendre panels in ω.
  * They differ in implementation: near-horizon variable (a: r* with Lambert-W start, then r; b: t = ln(r−2) throughout),
    sign of the fermion partner, R rule, stopping rule for the series, and node count.
  * So a–b agreement (1e-8 on bosons) tests the implementations, not the method. A shared conceptual error in the series
    matching would not have shown up.
* **My route closes that gap.**
  * It replaces the series with a WKB projection and uses a different horizon start and quadrature.
  * It agrees with a to ~1e-9 on Γ and on every P_s.
  * What all three share is the SPEC itself (potentials, flux definition, emission formula). Only the literature oracle
    tests that, and to about 1% it does.
* **Could the builders have seen other answers?**
  * The rooms are on the same filesystem as the repository. The repository holds 0.267/0.147/0.060/0.007 and 5.34e25
    in `src/black_holes.py`, `src/ladder_links.py` and others.
  * The orchestrator's own integration, `scratchpad/orch/gb_check.py`, was written at 23:17. That is before both rooms
    were exported (23:21), and it was world-readable. It contains a working Γ solver and a P loop.
  * b's code (23:58) was written after a's (23:31), and a's build was readable then.
  * The disk is mounted `relatime`, so atime cannot show reads.
  * I found no trace of copying. b's code is structurally different from a's and from gb_check.py, and each fixed the
    exact-zero bug differently (a: three consecutive negligible terms; b: pairwise max).
  * Blindness still rests on compliance, as in qed_cp. **Medium (process).**

### Can the oracle tell a right normalisation from a wrong one?

The two-route reference is P = 7.4386869e-5, 4.0916527e-5, 1.6819274e-5, 1.9183700e-6. Measured against it:

| s | oracle target | target vs reference | window the oracle accepts (relative to the reference) |
|---|---|---|---|
| 0 | 0.267·UNIT = 7.4560e-5 | +0.23% | −1.27% … +1.73% |
| ½ | 0.147·UNIT = 4.1050e-5 | +0.33% | −1.18% … +1.83% |
| 1 | 0.060·UNIT = 1.6755e-5 | −0.38% | −2.36% … +1.62% |
| 2 | Page 3.84e-6/2 = 1.9200e-6 | +0.09% | −5.9% … +6.1% |

* **A factor 1.05 on spin 2 passes.** M1b and M4 below do it with +4.5% and +4.6%.
* **A factor 1.015 on spin 1 passes.**
* **The ratio check checks no spin-2 ratio.** Its label says "0.026 (2)", but the lambda at oracle.py:23 tests only
  p[1]/p[0] and p[2]/p[0]. It also uses absolute tolerance 0.02, which is ±3.6% on 0.551 and ±8.9% on 0.225. Mutant M1
  (P_2 wrong by −69%) **passes** the ratio check.
* **The Γ point check** (oracle.py:24) uses the orchestrator's crude solver: plane-wave projection with no 1/r
  correction (gb_check.py:26). I confirm the values: 0.908938 and 0.129974. But the tolerance of 1e-3 is about 0.8% on
  Γ(1,1). **Low.**

**Sharper targets (proposed):**
1. **Self-consistent two-route reference.** P_s above at 1e-5 tolerance (`O_power_precise`). Also Γ at 40 stratified
   points from `indep.py` at 1e-4 (`O_gamma_dense`, `reference.json`).
2. **Exact low-frequency coefficients for every spin.** This is blind and analytic (`B_lowfreq_coeff`). It is the
   sharpest probe of the spin-dependent 1/r³ term.
3. **Page 1976 (PRD 13, 198) three-digit values.** Recalled from memory, so the orchestrator should check them against
   the paper:
   * photons 3.37e-5 for two helicities; both builds give 3.364e-5 (−0.18%);
   * gravitons 3.84e-6; both builds give 3.837e-6 (−0.08%);
   * total 2.011e-4 for 4 neutrino species + photons + gravitons; both builds give 4P_½ + 2P_1 + 2P_2 = 2.0114e-4 (+0.02%).

   As 0.3% targets these would already tighten spin 1 and spin 2 by a factor of 7 to 20.

## 4. Weak checks and mutants

All mutants are build a's file with one edit (`make_mutants.py`, plus `M0` and `M1b` built inline). Each was run with
`python3 gate.py mutants/<name> --mode verifier --campaign …/greybody --oracle …/greybody/oracle.py --timeout 1500`
(`run_gates.sh`).

| Mutant | What is wrong | Verifier gate | Killed by the proposed checks (`proposed_checks.py`) |
|---|---|---|---|
| **M0_lookup** | power_per_dof returns literature weights × 5.34e25/(ħc⁴/G²) typed as a dict. PROVENANCE still says "derived". Lint passes because no literal is within 1% of a target | **PASSES** | B_power_assembly (+2e-3), O_power_precise |
| M1_kappa_1ms | 1/r³ term 2(1−s) instead of 2(1−s²): identical for s = 0, 1 | all blind checks pass (slopes 6.11); killed by oracle spin 2 (−69%); **the ratio check passes** | B_lowfreq_coeff (−0.85), O_gamma_dense, O_power_precise |
| **M1b_kappa2_2p5pct** | spin-2 1/r³ coefficient −6.15 instead of −6 (2.5%). Limits and slopes preserved | **PASSES** (P_2 +4.51%) | B_lowfreq_coeff (+8.1e-2 at (2,2)), O_gamma_dense, O_power_precise |
| M2_fd_as_be | Bose–Einstein occupation for the fermion | killed by oracle spin ½ (+5.04%) and ratio | B_power_assembly, O_power_precise |
| **M3_two_waves** | partial-wave sum in P truncated after two waves (absorption_sum untouched) | **PASSES** (P_0 −0.26%) | B_power_assembly, O_power_precise |
| **M4_gamma_bump** | Γ → Γ^{1−0.15·exp(−((ω−0.45)/0.1)²)}: stays in [0,1], monotone, exact at low and high ω and at the oracle's ω = 0.2 probe | **PASSES** (P_2 +4.57%, P_1 +0.85%) | O_gamma_dense (up to 130% at ω ≈ 0.45), O_power_precise |
| **M5_T_typo** | T = 1/25.1 instead of 1/(8π) (+0.13%) | **PASSES** (+0.3 … +1.2%) | B_power_assembly, O_power_precise |
| **M6_tail_2j** | degeneracy 2j instead of 2j+1 for j ≥ s+2, in P only | **PASSES** (−0.05%) | B_power_assembly, O_power_precise |

**Six of eight mutants survive the full verifier gate. All eight are killed by the proposed checks.** Builds a and b
pass all four proposed checks. b passes O_gamma_dense at 1e-4 (worst 2.1e-5) but fails it at 1e-6 because of its
fermion error (§5).

Per existing check, a wrong implementation that survives it:
* `b_range` (campaign.py:17): any Γ clipped into [0,1]. Build a clips, so the check cannot see a's Γ > 1.
* `b_low_scalar` (:22): an ±8% window on Γ_00/ω² at a single ω. Any s = 0 error < 4%, and any spin ≠ 0 error at all.
  The exact coefficients for all spins (B_lowfreq_coeff, tolerance 2e-3) close this.
* `b_slopes` (:27): exponents only, at ±0.25. M1 and M1b survive it.
* `b_geometric` (:37): ω = 1 only, ±12%, and spin 2 is not tested. It is blind to everything at ω < 1, where the power is.
* `b_monotone` (:46): lowest wave, 6 points. M4 survives.
* `b_order` (:53): ordering only. Every mutant survives.
* `b_convergence_independent_of_call` (:58): satisfied by any cache.
* Oracle power (oracle.py:14–17): the windows in §3. M1b, M3, M4, M5 and M6 survive. The tolerances are set by
  1–2-digit literature weights.
* Oracle ratio (oracle.py:22–23): no spin-2 term, and absolute tolerance.
* Oracle Γ (oracle.py:24–25): two points at the same ω, 1e-3. M4 survives because its bump vanishes at 0.2.

Proposed checks, as code in `proposed_checks.py`, with the same (ok, detail) shape as `campaign.BLIND`:
* `B_lowfreq_coeff` (blind): kills M1, M1b and any wrong spin-dependent potential term. It runs in under a second.
* `B_power_assembly` (blind): the gate recomputes P_s from `m.transmission` with its own quadrature, occupation and
  (2j+1). Tolerance 1e-5. It kills M0, M2, M3, M5 and M6, and any lookup that does not equal the build's own integral.
  It costs about 3–10 minutes per build.
* `O_gamma_dense` (oracle): 40 jittered points (s; j = s, s+1; ω ≈ 0.07…0.6) against `reference.json`. Tolerance 1e-4.
  It kills M1, M1b and M4. The seed should be refreshed per verifier run.
* `O_power_precise` (oracle): the two-route P_s at 1e-5. It kills all eight.

**Limit.** A build that types in the correct high-precision P_s and also has a correct Γ passes everything,
B_power_assembly included, because its typed numbers equal its own integral. As in qed_cp, the gate cannot enforce a
route. Only reading DERIVATION and the code can.

## 5. Numerical honesty

* **Γ > 1.**
  * All three solvers give 1 + O(1e-10) where Γ is saturated. b at (1,1,1.2) gives 1 + 5e-11, and at ω = 2.4 gives
    1 + 8e-11. Mine gives 1 + 2e-11.
  * a hides this with the clip (§1). b reports it honestly (b QUESTIONS.md).
  * Harmless. **Low.**
* **b's fermion boundary condition (b:73–77).**
  * b starts at d0 = 1e-8·min(1,ω)² with ψ = e^{−iωr*}, Φ = −iωψ, and no correction term.
  * DERIVATION b step 1 bounds the error by "O(V/w) ~ d0/w". That holds for bosons (V ∝ f). For fermions V ∝ √f, so
    the error is O(k√d0), relative to a horizon correction d ≈ 2k/(1 − 8iω).
  * Measured, b vs a and vs my independent solver: 3e-5 for (½, ½, 0.02), 6.6e-5 for (½, 3/2, 0.02), 1.4e-4 for
    (½, 7/2, 0.02). Setting d0fac = 1e-14 removes it, down to 1e-9 (`fermion_loww_out.txt`).
  * b's own convergence test (b:171–172) moves d0 only at a boson point (2,2,0.05), so it could not see this. b's
    QUESTIONS claim "σ = ±1 agrees to ~4e-11" is true but irrelevant, because both signs share the same start error.
  * Effect on P_½: 2.5e-8, because the errors change sign across ω ≈ 0.15. The exported `transmission(0.5, j, ω)` is
    still wrong at the 1e-4 level. **Medium (claim versus reality; no effect on the result).**
* **a's fermion start at very low ω.**
  * r*_min = −80 with no √f correction leaves a ~1e-7 relative error at ω ≤ 0.005: (½, ½, 0.002) moves −9.7e-8 when
    r*_min = −160. My solver, x0 = 1e-12 with the √f correction, agrees with the −160 value.
  * a's DERIVATION §9 claims r*_min doubling moves Γ by ≤ 4e-10. That was tested only at (½, 3/2, 0.3).
  * Negligible for P. **Low.**
* **b's convergence evidence.**
  * DERIVATION b "(b)" promises R, d0, rtol, GL nodes ×2, j cutoff and ω_max varied, with P moving < 1e-6.
  * The code (b:171–177) does one Γ point for R/d0/rtol, and one pair of P configurations: nodes 12 → 16 (×1.33, not ×2),
    ω_max 2.4 → 2.8, cut 1e-15 → 1e-17, all changed at once.
  * That single comparison moved P_2 by 3.5e-7. This is in fact b's true error: −3.4e-7 against the two-route reference.
  * So the < 1e-6 claim happens to hold, which I verified independently, but b did not demonstrate it as SPEC §5 asks
    ("changing each by a factor of 2"). **Low–medium.**
* **a's convergence evidence.** Each knob was changed separately and doubled (a `main_out.txt`), plus a scipy.quad route.
  It is consistent with my 1e-9 cross-check. a's claimed tolerance of 1e-8 on P_s holds.
* **The exact-zero coefficient bug.**
  * For bosons, a_{n+1} = {[n(n+1) − L]a_n − 2(n² − s²)a_{n−1}}/(2iεω(n+1)). This vanishes exactly at n = j = s, so
    a₁ = 0 for (0,0), a₂ = 0 for (1,1) and a₃ = 0 for (2,2).
  * The zeros are isolated. If a_{n+1} = 0, then a_{n+2} = −2((n+1)² − s²)a_n/(…) ≠ 0.
  * So a's "three consecutive negligible terms" (a:98–100) and b's "pairwise max" (b:49–53) are both sufficient.
  * Checked numerically: (1,1) and (2,2) agree with my series-free solver to ≤ 8e-10 at every ω.
* **Low frequency (ω ≤ 0.005).**
  * Bosons: a, b and mine agree to ≤ 1.5e-11 at ω = 0.001, 0.002 and 0.005. Γ_00/ω² = 16.1024, 16.2079, 16.5405.
  * Fermions: as above, a 1e-7 and b 1e-5.
  * The exact ω → 0 coefficients are reproduced for 8 (s,l) by both builds (§0).
  * The gate's own low-frequency test is a ±8% window (campaign.py:22).

## 6. Findings by severity

**High**
* **H1: the verifier cannot distinguish wrong results at the few-% level.** Six of eight mutants pass the full verifier
  gate. They include:
  * a 2.5% error in the spin-2 potential (P_2 +4.5%, M1b);
  * a smooth distortion of Γ at ω ≈ 0.45 (P_2 +4.6%, P_1 +0.9%, M4);
  * a wrong T (+0.13%, M5);
  * a truncated or mis-weighted j-sum (M3, M6);
  * a typed-in literature answer (M0).

  The spin-2 window is ±6%. The "ratio" check, despite its label, tests no spin-2 ratio (oracle.py:23), and lets
  P_2 off by −69% through (M1).

  This is a defect of the campaign's checks, not of either build. **For these two builds it is closed by my independent
  two-route recomputation** (P_s to ~1e-9, Γ to ~1e-9). For any future build it stays open until the checks in
  `proposed_checks.py` (or equivalent) are adopted.

**Medium**
* M1: b's fermion Γ is wrong by up to 1.4e-4 relative at low ω. The cause is its BC start (b:73–77), whose error bound in
  the DERIVATION is wrong for fermions and which b's checks did not exercise. The effect on P_½ is 2.5e-8.
* M2: process, as in qed_cp. The literature weights in the repository and the orchestrator's working solver
  (`scratchpad/orch/gb_check.py`, 23:17) were readable from both rooms, and b's build ran after a's was on disk.
  I found no evidence of use.

**Low**
* L1: a clips Γ to 1 (a:163), undocumented and contrary to DERIVATION §1. It is harmless, but it blinds `b_range`.
* L2: b's convergence demonstration is one combined configuration change, not the factor-2-per-knob study it claims
  and SPEC §5 asks for. Its true error (3.4e-7 on P_2) is within its claim.
* L3: a's fermion Γ at ω ≤ 0.005 is accurate to 1e-7, not the 1e-10 implied by DERIVATION §9.
* L4: b's transmission has no guard for j < s or ω ≤ 0 (ω = 0 crashes).
* L5: drift between b's documentation and code (j cut, series cut, "×2 nodes").
* L6: the determinism check is satisfied by any cache. The oracle Γ check has 1e-3 tolerance at a single ω, from a
  crude reference whose values I confirm.

## 7. Verdict

**ACCEPT the result** (both builds):

P_s = 7.43869e-5, 4.09165e-5, 1.68193e-5, 1.91837e-6 (units 1/M², per degree of freedom).

Both builds are physically correct and numerically converged, confirmed by an independent series-free route to ~1e-9.
They also match Page's three-digit values within rounding. The only high-severity finding (H1) concerns the gate and
oracle. It is closed for these builds by §0, not by the gate pass, which on its own proves far less than it seems.

Before this campaign's gate is reused:
1. Add `B_lowfreq_coeff` and `B_power_assembly` to `campaign.BLIND`.
2. Replace the oracle's power targets with the two-route values at 1e-5 (`O_power_precise`), and add `O_gamma_dense`.
3. Fix the ratio check to include spin 2, or drop it.
4. Ask a to document the clip and b to fix its fermion BC start.

## Files

* `indep.py`: independent Γ solver.
* `compare_gamma.py` → `compare_gamma_out.txt`.
* `fermion_loww.py` → `fermion_loww_out.txt`.
* `indep_power.py` → `indep_power_*.json`.
* `record_grid.py` → `grid_a.json`; `offline_mutants.py`.
* `make_mutants.py`, `run_gates.sh`, `mutants/*`.
* `proposed_checks.py`, `make_reference.py` → `reference.json`; `run_proposed.py`, `run_all_proposed.sh`.
