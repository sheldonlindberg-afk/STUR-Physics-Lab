# Red-team audit: dr_xi (gauge-parameter independence of the bosonic one-loop Δr, general R_ξ)

In the repository I wrote only this file and `audit_proposed_checks.py`. All scratch work is in
`S = /tmp/claude-0/-home-user-STUR-Physics-Lab/6f003c51-fc14-5da0-833a-45f53d6397be/scratchpad/audit-dr_xi`:
* `indep_se.py`: the independent derivation of the gauge-boson self-energies in R_ξ (§1). `t1.py` is the ξ = 1 check against Denner, `t2.py` the component check, `compare.py` / `compare.log` / `compare.json` the 45-point comparison with both builds, and `extreme.py` / `extreme.log` the run at ξ = 10⁻¹² … 10⁸.
* `landau.py` / `landau.log`: the Landau-gauge analysis (§2).
* `make_mutants.py`, `run_gates.sh`, `mutants/<name>/` (each with `gate_stdout.txt`, `gate_report.json`, `proposed_out.txt`), `gates.log`: the mutants (§3).
* `gen_table.py` → `tables.py`: the tables in `audit_proposed_checks.py`. `checks_a.log` and `checks_b.log` are the runs of the proposed checks on both builds.

The builds were run from copies in `S/copies/{a,b}`. Nothing was written into `builds/`, `oracle.py` or `reference_denner.py`.

Classes, as in the sibling audits: **B** = defect in a build. **R** = SPEC ambiguity (a correct build could resolve it differently). **C** = oracle/check gap or caveat. **N** = note or positive result.

## 0. Verdict

* **Both builds are correct where the SPEC defines the answer. I found no B finding.**
* **Class SE is confirmed independently.** My own derivation agrees with build a to 0 (bit-identical floats) and with build b to ≤ 3.3·10⁻¹⁵ relative. That covers 49 points with ξ = 10⁻¹² … 10⁶, μ = 30 … 5000 GeV, M_H = 1 … 10⁴ GeV and five (M_W, M_Z) pairs. The SE structure the builders claimed is confirmed too.
* **Class VBW is only checked through gauge independence, not by an independent derivation.** VBW(ξ) − VBW(1) = −[SE(ξ) − SE(1)] holds in both builds to ≤ 2.5·10⁻¹⁵ at 45 points. Combined with the oracle's total, this fixes VBW. It is not an independent computation of vertex + box + wave function (§1d).
* **The gate cannot see how Δr is split between the classes (C1).** 10 of my 19 wrong mutants of build a pass the full verifier gate:
  * 9 of them move a piece between SE and VBW;
  * 1 is wrong only for 0 < ξ < 0.1.

  The 5 proposed checks kill all 10, and both builds pass them.
* **The Landau-gauge class values are a convention the SPEC does not fix (R1).** The builds differ there by exactly (1/8)(α/4π) = 7.7712·10⁻⁵. I derived both conventions from one photon-mass computation, and the total is unaffected.

## 1. Independent derivation of class SE (task 1)

### (a) Method (`indep_se.py`; no code shared with the builds)

**Lagrangian and fields.**
* Real basis: gauge fields (W1, W2, Z, A) and a real scalar 4-vector φ, with D φ = ∂φ + θ^a A^a φ.
* θ^a is the real 4×4 image of −i g τ^a/2 and −i g′Y. The rotation W3 = cZ + sA, B = −sZ + cA is the SPEC's.
* The structure constants come numerically from [θ^a, θ^b] = f^{abc} θ^c.
* Goldstones lie along F_a = θ^a v, and the Higgs along v.

**Vertices.** I derived them by hand from ½(Dφ)² − ¼F² − (1/2ξ)(∂·A − ξ F_a·h)² + c̄^a δG^a c^b. Momenta are incoming, and V3 has the form f^{abc}[g(k1−k2) + …]. The other vertices are:
* VSS: (p_i − p_j) θ^a_ij;
* VVS: i g (X_ab + X_ba), with X_ab = F_aᵀθ^b;
* VVSS: i g (S_ij + S_ji);
* VVVV: brute-force sum over the 24 slot assignments;
* ghost: f^{dba} q_μ, with loop factor −1.

The photon carries the SPEC's R_ξ propagator with a tiny mass λ (λ²/M_W² = 10⁻³² … 10⁻⁵⁰), extrapolated to λ → 0. The builds use a massless dimensionally regulated photon in SE, so this is a different IR route.

**Diagrams.** VV, VS, SS and ghost bubbles plus the VVVV and VVSS seagulls, with no tadpoles. Every vector line is split into simple poles, g/(k² − M²) and ∓kk/M²·[1/(k² − M²) − 1/(k² − ξM²)].

**Reduction and renormalization.**
* My own index contractor gives the d-dimensional numerators.
* The exact reduction to A0 and B0 uses k² = D1 + m1² and k·p = (D1 − D2 + m1² − m2² + p²)/2. No PV tensor coefficients or IBP are needed.
* MS-bar keeps the O(ε) of c(d): c(d)·A0 → c(4)A0_fin − 2c′(4)m².
* Re B0 comes from a closed form through the roots, with a stable series for distant roots.

**Evaluation points.** Σ(0) uses the g/d contraction at p = 0. Σ′_AA(0) uses a Richardson central difference at p² = ±10⁻¹², ±2·10⁻¹² M_W². The working precision is 80–100 digits.

### (b) Validation at ξ = 1 against an external anchor

Σ_W, Σ_ZZ, Σ_AA and Σ_AZ at k² = M_W², M_Z², 3000 and −5000 GeV² agree with Denner's appendix B (`reference_denner.py`) to all 15 printed digits (`t1.py`).
* Σ_AZ has the opposite sign, as it must under the SPEC's photon convention (same finding as ferm_se).
* Σ_AA(0) and Σ_AZ(0) at ξ = 1, μ = M_W vanish to 10⁻⁸⁰.

At ξ = 1 the agreement at general k² tests every vertex and diagram class. At general ξ only the propagators change, because no gauge-sector vertex depends on ξ in linear R_ξ (the ghost–scalar ξ couplings enter only the excluded tadpoles).

### (c) The ξ dependence of SE (gate point M_W = 80.38, M_Z = 91.19, M_H = 125 GeV, α = 1/128, μ = M_W)

* **δZ_e is ξ-independent.** δZ_e = ½Σ′_AA(0) + (s/c)Σ_AZ(0)/M_Z² = −2.072329988176·10⁻⁴ at every ξ: across the 45 points it changes by ≤ 10⁻⁴² from ξ = 1. Σ′_AA(0) and Σ_AZ(0) separately depend strongly on ξ (for example, at ξ = 4 they are −4.51·10⁻³ and +3.82·10⁻³·M_Z²).
* **The mixing-angle combination is ξ-independent.** Σ_W(M_W²)/M_W² − Σ_Z(M_Z²)/M_Z² = −2.762262592697·10⁻³ at every ξ, to ≤ 10⁻³⁹. Σ_W(M_W²)/M_W² and Σ_Z(M_Z²)/M_Z² separately shift by the same function of ξ, the tadpole-like shift (table, 4th column).
* **So all of SE's ξ dependence sits in [Σ_W(0) − Σ_W(M_W²)]/M_W².** In my table that term carries the whole of SE(ξ) − SE(1): the other two pieces change by < 10⁻³⁹.

| ξ | Σ_W(0)/M_W² | Σ_W(M_W²)/M_W² | common shift of Σ_V(M_V²)/M_V² (W, Z) | SE(ξ) − SE(1), auditor | VBW(ξ) − VBW(1), build a | build b |
|---|---|---|---|---|---|---|
| 10⁻⁶ | 6.923297952e-4 | −1.091203903e-2 | −2.0642544e-3, −2.0642544e-3 | 4.362510002892e-3 | −4.362510002892e-3 | −4.362510002892e-3 |
| 10⁻³ | −2.503312098e-3 | −1.089418534e-2 | −2.046400708e-3, same | 1.14901441727e-3 | −1.149014417270e-3 | −1.149014417270e-3 |
| 0.3 | −3.171713822e-3 | −9.465429242e-3 | −6.176446097e-4, same | −9.481434055027e-4 | 9.481434055027e-4 | 9.481434055027e-4 |
| 4 | 2.486219669e-3 | −1.535687319e-2 | −6.509088555e-3, same | 1.060123403129e-2 | −1.060123403129e-2 | −1.060123403129e-2 |
| 25 | 1.942200971e-2 | −1.436362529e-1 | −1.347884683e-1, same | 1.558164037974e-1 | −1.558164037974e-1 | −1.558164037974e-1 |
| 1000 | 6.959770474e-1 | −1.376973927e+1 | −1.376089149e+1, same | 1.445847446025e+1 | −1.445847446025e+1 | −1.445847446025e+1 |

**Comparison with the builds.**
* **45 points** (`compare.log`): 7 (M_W, M_Z, M_H, α) sets × ξ ∈ {10⁻⁶, 10⁻³, 0.05, 0.3, 2, 4, 25, 1000} × μ ∈ {30, M_W, 900, 5000}. The absolute SE agrees with build a to 0 and with build b to ≤ 1.7·10⁻¹⁵.
* **4 more points** (`extreme.log`): ξ = 10⁻¹², 10⁻⁹, 10⁴, 10⁶, 10⁸. These agree to ≤ 3.3·10⁻¹⁵.
* **λ dependence.** My values change by ≤ 10⁻¹⁴ relative between λ/M_W = 10⁻¹² and 10⁻¹⁶. The residual is the O(λ) term build b mentions, so SE is IR finite for every ξ > 0. My λ route and the builds' dimensional route agree.

### (d) Class VBW: NOT independently derived

I did not compute the vertex, box and wave-function diagrams myself. What I checked follows from gauge independence:
* VBW_build(ξ) − VBW_build(1) = −[SE_mine(ξ) − SE_mine(1)] in both builds, to ≤ 2.5·10⁻¹⁵ at 45 points.
* `audit_vbw_table` checks VBW against Denner's total minus my SE at 49 points.

Because my SE is independent and the physical total is ξ-independent, this does pin VBW: any VBW error would have to show up in the total, which the oracle checks. But it is not a second derivation of VBW. In particular, it says nothing about how VBW itself is split into vertex, box and wave function.

There is one partly independent piece of evidence on the lepton side. Mutants m05 and m06 put the photon (ξ_A = 1), or the whole Z sector (ξ_Z = 1, with the χ and u_Z masses), back into Feynman gauge while the rest stays at ξ. Build a's total then stays exactly ξ-independent and equal to Denner (both pass the full gate). This is the separate ξ_A, ξ_Z independence a correct R_ξ computation must have. It exercises build a's vertex, box and wave-function code with the photon and Z gauge parameters varied separately (**N2**).

## 2. Landau gauge and the IR treatment (task 2)

**Why the classes diverge as ξ → 0+.** In Σ_W(0) the soft photon pairs with the massless-in-the-limit Goldstone (γ–W–φ coupling) and with the ξ-pole of the W propagator (mass² ξM_W²). This gives a ln(ξM_W²) IR logarithm, which the W–γ box cancels in VBW. I found numerically (`landau.log`):
* **The slope is −(3/4)(α/4π).** dSE/d ln ξ = −(3/4)(α/4π)·(1 + O(ξ)): the ratio is −0.749643, −0.7499944 and −0.74999992 for the pairs (10⁻⁴, 10⁻⁶), (10⁻⁶, 10⁻⁸) and (10⁻⁸, 10⁻¹⁰).
* **The regulators correspond as λ² ↔ ξM_W², with no extra constant.** Exactly at ξ = 0 with photon mass λ, SE(0; λ) = C0(μ) − (3/4)(α/4π) ln(λ²/μ²) + O(λ), with C0 λ-independent to 10⁻¹⁸. Then SE(ξ → 0+) = C0(μ) − (3/4)(α/4π) ln(ξM_W²/μ²) + o(1). I checked this at μ = 30, M_W and 900 GeV to all digits.
* **The class values at ξ = 0 therefore depend on how the IR log is removed.** dZ_e and the mixing combination stay ξ-independent at ξ = 0. Only W0M carries the log.

**The two conventions.**
* **Build b** replaces ln(λ²/μ²) → 1, so SE_b(0) = C0 − (3/4)(α/4π)·1. My λ computation with that rule reproduces build b's SE(0) to 1.5·10⁻¹⁷ at μ = 30, M_W and 900 GeV.
* **Build a** uses massless Goldstones with dimensional IR regularization and drops the 1/ε_IR pole together with the UV pole. Its SE(0) equals C0 − (3/4)(α/4π)·(5/6) at all 9 (point, μ) pairs I tested.
* **The difference** is the rational O(ε)×1/ε_IR term from the d-dependent coefficient of the IR-divergent integral. It comes to SE_a(0) − SE_b(0) = +(1/8)(α/4π) exactly: 0.12500000000 (±3·10⁻¹⁴) in units of α/4π at three μ and three (M_W, M_Z), and VBW has the opposite sign. This is the cross-build 7.771237·10⁻⁵.

Both builds have SE(0) + VBW(0) equal to the ξ > 0 total, so the total is unaffected. **R1:** the SPEC asks for the classes "at ξ = 0" but they are IR divergent there, so their value is a convention. The SPEC should either pick one (for example "the ξ → 0+ log removed with ln(ξM_W²/μ²) → 0", which in my variables is SE(0) = C0) or require the classes only for ξ > 0.

**The builders' "(3/2) α/4π" statement and the photon-mass definition.**
* **What build a says.** A massless, dimensionally regulated photon in all lepton diagrams, with 4d Fierz for the finite box structures, would shift the total by exactly (3/2)α/4π (0.0042975 → 0.0033650).
* **I did not recompute the boxes, so the number "3/2" is unverified by me (C2).**
* **The mechanism is plausible.** An IR pole multiplying an evanescent (O(ε)) Dirac structure leaves a rational remainder. In a consistent dimensional treatment, the Fermi-theory subtraction (scaleless, hence "zero") would have to be evaluated with the same d-dimensional Dirac algebra, and its 1/ε_UV − 1/ε_IR structure would remove the remainder. So the shift reflects an inconsistent mix of schemes, not a physical ambiguity of Δr.
* **The photon-mass route is the right physical definition here.** The SPEC prescribes it ("the infrared divergences … cancel with a photon mass λ → 0"). It is also the Sirlin definition of G_F via the charge-retention Fermi-theory QED correction, which is finite and regulator independent.
* **What the ξ = 1 agreement with Denner (≤ 10⁻¹⁵) shows.**
  * It does show that the builds' VBW + Fermi-subtraction convention is the one behind Denner's δ_VB = α/(4πs²)[6 + (7 − 4s²)/(2s²) ln c²], i.e. the standard literature Δr.
  * It does not show that the ξ ≠ 1 classes are right: that needs §1.
  * It does not verify Denner's δ_VB independently. The reference is a transcription, independently re-derived only in the bos_dr audit.
  * It does not test the (3/2) claim.

## 3. Mutants of build a (task 3)

All mutants were run through `python3 gate.py --mode verifier --campaign dr_xi --oracle dr_xi/oracle.py <dir>` from `rebuild/campaigns` (`gates.log`, `mutants/*/gate_stdout.txt`), then through `audit_proposed_checks.py` (`mutants/*/proposed_out.txt`). I wrote 21 mutants: 19 wrong and 2 equivalent.

| Mutant | What it changes | Gate | Proposed checks |
|---|---|---|---|
| m01_comp_f_xi | +f to SE, −f to VBW, f = 2(α/4π)(ξ−1)/(1+ξ) | **PASS** | killed (SE table, VBW table, Landau) |
| m02_comp_small_xi | the same with f = (α/4π) ξ ln ξ, only for 0 < ξ < 0.1 | **PASS** | killed (SE table, VBW table) |
| m03_comp_mu | compensating f = (α/4π) ln(μ²/M_W²)(1 − 1/(1+ξ)) | **PASS** | killed (SE table, VBW table) |
| m04_AZ_moved_to_VBW | (2/sc)Σ_AZ(0)/M_Z² moved from SE to VBW (the other bookkeeping, QUESTIONS a1/b2) | **PASS** | killed (SE table, VBW table, Landau) |
| m05_photon_feynman_gauge | photon propagator at ξ_A = 1 in all diagrams | **PASS** | killed (SE table, VBW table, Landau, log slope) |
| m06_Z_feynman_gauge | Z propagator and the χ and u_Z masses at ξ_Z = 1 | **PASS** | killed (SE table, VBW table, Landau) |
| m07_landau_as_tiny_xi | ξ = 0 evaluated as ξ = 10⁻¹² in the class exports | **PASS** | killed (Landau: κ between −33 and −26, varying with the point) |
| m08_landau_ir_mu | at ξ = 0, a μ-dependent IR subtraction ±(3/4)(α/4π) ln(μ²/M_W²) | **PASS** | killed (Landau: κ varies with μ, from −4.3 to 2.8) |
| m09_landau_const | at ξ = 0, ±0.6 α/4π moved between the classes | **PASS** | killed (Landau: κ = 0.033) |
| m21_small_xi_branch | Σ_W(0) evaluated at 1.01ξ for 0 < ξ < 0.1 (a wrong small-ξ branch) | **PASS** | killed (SE table, total at extreme ξ) |
| m10_ghost_dropped | SE ghost loops dropped | FAIL | killed |
| m11_ghost_sign | ghost loop sign +1 | FAIL | killed |
| m12_chi_mass_MW | χ mass ξM_W² instead of ξM_Z² | FAIL | killed |
| m13_photon_box_dropped | W–γ box dropped | FAIL | killed |
| m14_Wxi_pole_sign_lepton | sign of the W ξ-pole term flipped in the lepton diagrams | FAIL | killed |
| m15_tadpole_masses_only | ξ-dependent tadpole added to Σ_V(M_V²) but not to Σ_W(0) | FAIL | killed |
| m17_small_mass_B0 | B0 small-mass shortcut (m² < 10⁻² p² → 0) | FAIL (only M_H = 1 GeV) | killed (SE table) |
| m18_mu_SE_only | SE evaluated at 1.01 μ | FAIL | killed |
| m19_low_precision | DPS 60 → 24 | FAIL | killed |
| m16_tadpole_consistent | tadpole added consistently to Σ_W(0), Σ_W(M_W²), Σ_Z(M_Z²) | PASS | passes: **equivalent** |
| m20_real_part_sign | Re B0 shifted above every threshold where both masses are < 0.05 p² | PASS | passes: **equivalent** |

**Survivors of the gate.** m01–m09 and m21: 10 wrong mutants. Every one of them is killed by at least one proposed check.

**m16 is equivalent.** It is the builders' tadpole argument made executable: a common k·M_V² in the W and Z self-energies cancels in Δr (**N3**).

**m20 is equivalent.** In build a's on-shell reduction, the coefficient of every B0(M_V²; ξM1², ξM2²) is exactly zero. The perturbed values (Σ_W at (ξM_W², ξM_Z²), Σ_Z at (ξM_W², ξM_W²)) are reached but change nothing. My code independently gives a zero coefficient for B0(M_Z²; ξM_W², ξM_W²) in Σ_Z (the shift is 10⁻⁷⁹). The unphysical thresholds at (√ξ M1 + √ξ M2)² < M_V² therefore do not enter the on-shell self-energies, so the "real part above unphysical thresholds" question of QUESTIONS a7/b5 is moot for these pairs (**N4**). The remaining unphysical threshold, photon + Goldstone in Σ_W(M_W²), sits at the endpoint x = 1. It is covered by the SE table at ξ = 10⁻¹² … 0.05.

## 4. Findings

* **C1 (main gap).** The oracle and blind checks constrain only the total and SE + VBW. Any f(ξ, μ) moved between the classes passes them: m01–m09 pass the gate. Only an independent SE closes this. `audit_se_table` is **independent**: my own Feynman rules, algebra and reduction, anchored to Denner at ξ = 1. `audit_vbw_table` is **not independent**: it is Denner's total minus my SE.
* **C2.** The ξ sampling of the oracle (0, 0.2, 1, 3, 25, 400) and of the blind checks (0 … 1000) has no point in 0 < ξ < 0.2 and none above 1000. m21 is wrong only for ξ < 0.1 and passes. `audit_total_extreme_xi` (reference-free) adds ξ = 10⁻⁹ … 0.05 and 10⁴ … 10⁶; both builds are exact there (worst 0.0, and ≤ 6·10⁻¹⁴ even at ξ = 10⁸). The (3/2) α/4π statement of build a is unverified by me (§2).
* **R1.** The class values at ξ = 0 are an IR convention: build a has κ = 5/6 and build b κ = 1, a difference of (1/8)α/4π. `audit_landau_convention` accepts any single constant κ in [½, 3/2] that is the same at every point and μ. That kills m07–m09 and both builds pass it, but no check can tell κ = 5/6 from κ = 1 until the SPEC fixes the convention.
* **N1.** The SE structure is confirmed independently: δZ_e ξ-independent, Σ_W/M_W² − Σ_Z/M_Z² on shell ξ-independent, a common tadpole-like shift, and all ξ dependence in [Σ_W(0) − Σ_W(M_W²)]/M_W². The Landau log is −(3/4)(α/4π) ln(ξM_W²/μ²), with exact correspondence to the photon-mass regulator.
* **N2.** Build a's total is also independent of ξ_A and of ξ_Z separately (m05, m06). Both builds are stable to ξ = 10⁸ and ξ = 10⁻¹².
* **N3, N4.** The tadpole argument and the vanishing of the on-shell unphysical-threshold B0 coefficients, as described in §3.

## 5. Proposed checks (`audit_proposed_checks.py`; `CHECKS = [(label, fn(module) -> (ok, msg))]`; `python3 audit_proposed_checks.py <build dir>`)

| Check | Independent? | Build a | Build b | Kills |
|---|---|---|---|---|
| `audit_se_table`: SE at 49 points, rel 10⁻¹⁰ | yes (auditor derivation) | 0.0 | 3.3e-15 | m01–m06, m21, and every SE-side error |
| `audit_vbw_table`: VBW = Denner − SE_auditor, rel 10⁻⁹ | no (gauge independence) | 7.4e-16 | 7.4e-16 | m01–m06 |
| `audit_total_extreme_xi`: total at ξ = 10⁻⁹ … 0.05, 10⁴ … 10⁶ | reference-free | 0.0 | 0.0 | m21 |
| `audit_landau_convention`: one κ, ½ ≤ κ ≤ 3/2 | the C0(μ) are independent; κ is a convention | κ = 0.8333333333 | κ = 1.0000000000 | m07, m08, m09 (and m01, m04, m05, m06) |
| `audit_landau_log_slope`: dSE/dln ξ → −(3/4)α/4π | reference-free, derived coefficient | 1.0e-7 | 1.0e-7 | m05 (and m10, m11) |

Both builds pass all 5 checks (`checks_a.log`, `checks_b.log`). Every wrong mutant fails at least one.
