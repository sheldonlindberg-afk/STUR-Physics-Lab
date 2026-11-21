# Red-team audit: ferm_se (fermion-loop one-loop Σ_AA, Σ_AZ, Σ_ZZ, Σ_W; 't Hooft-Feynman gauge, MS-bar)

In the repository I wrote only this file and `audit_proposed_checks.py`. All scratch work is in
`S = /tmp/claude-0/-home-user-STUR-Physics-Lab/6f003c51-fc14-5da0-833a-45f53d6397be/scratchpad/audit-ferm_se`:
* `derive.py` / `derive.log`: the independent sympy derivation (§1);
* `indep.py`, `compare.py` / `compare.log` / `compare.json`: the independent numerics and the 75-point comparison (§2);
* `make_mutants.py`, `mutants/<name>/`, `mutants2/<name>/`: the mutants of build a, each with `gate_stdout.txt`, `gate_report.json` and `proposed_out.txt` (§3);
* `checks_a.log`, `checks_b.log`, `checks_ref.log`: the proposed checks run on both builds and on the reference.

The builds were run from copies in `S/copies/{a,b}`, so nothing was written into `builds/`. Each verifier gate run takes about 6 minutes, almost all of it in the reference.

Classes, as in the sibling audits: **B** = a defect in a build. **R** = a SPEC wording or ambiguity issue that should be revised. **C** = an oracle or check gap, or a caveat. **N** = a note or a positive result.

## 0. Verdict

* **Both builds are correct.** I found no B finding.
  * My own derivation from the SPEC Lagrangian gives the same integrand as both builds, symbolically (difference exactly 0).
  * My own dispersion-relation numerics agree with build a, build b and the oracle reference to ≤ 9·10⁻¹⁵ at 75 points.
* **The oracle reference is right, including the two places where it departs from the printed Denner formula.**
  * The sign flip of Σ^AZ follows from the SPEC's photon convention.
  * The general-I3 axial term 3 I3²/(s²c²) replaces Denner's 3/(4s²c²). I derived it independently: (g_L − g_R)² = I3²/(s²c²).
* **The gate is weak outside the window it samples.** 7 of my 24 wrong mutants pass the full verifier gate. The 5 proposed checks kill all 7 and pass both builds.
* **The oracle is over-strict at exact zeros** (C1). A roundoff-sized control is rejected.

## 1. Independent derivation (`S/derive.py`, sympy)

**Couplings.** I expanded ψ̄γ^μ(g W^a T^a + g' Y B)ψ with W3, B solved from Z = cW3 − sB, A = sW3 + cB, and W1, W2 solved from W± = (W1 ∓ iW2)/√2. With T3 = I3, Y = Q − I3 on the left-handed component and T3 = 0, Y = Q on the right-handed one, sympy gives:
* photon: e Q for both chiralities;
* Z: e(I3 − s²Q)/(sc) for L and −e sQ/c for R, so **g_L − g_R = I3/(sc) for any I3**;
* W: ū γ^μ P_L d W⁺ with g/√2 = e/(√2 s), and no right-handed coupling.

The photon and Z vertices have the same overall sign, +ie, under the SPEC's rotation. So Σ^AZ ∝ +Q(g_L + g_R). This is opposite to Denner's convention, which confirms the oracle's flip.

**Sign of Σ.** The tree vertex function is −i g(k² − M²). Adding the amputated 1PI sum iΠ g gives −i g(k² − M² − Π_T). So Σ = −Π, entry by entry, including the A–Z entry, which matches the SPEC's Γ^{VV'} wording.

**Trace and loop integral.** I wrote my own recursive d-dimensional trace (Tr 1 = 4) and pushed the chiral projectors to the right. The γ5 remainder is ε^{μνρσ}q_ρ q'_σ, which is antisymmetric and integrates to ε(μ,ν,k,k) = 0. The rest of the chain:
* Feynman parameter x on the m2 line, q = l − xk;
* symmetric integration in d dimensions (l^μ l^ν → g l²/d);
* exact-d Γ-function master integrals, expanded in ε with all O(ε) × pole terms kept;
* MS-bar.

The result is

  Σ_T = N (α/4π) · 2 ∫₀¹ dx [−ln(Δ/μ²)] { G₊[2x(1−x)k² − (1−x)m1² − x m2²] + G₋ m1 m2 },  Δ = (1−x)m1² + x m2² − x(1−x)k²,

with G₊ = a_L b_L + a_R b_R and G₋ = a_L b_R + a_R b_L. Specific results:
* **Agreement with the builds.** My integrand minus the builds' integrand (build a route 2, build b) is exactly 0.
* **No rational remainder.** The L-independent part integrates to 0. Build b's claim of "no finite rational remainder" is therefore true in the Feynman-parameter form. In build a's PV form, the same content appears as the (m1² + m2² − k²/3)/6 term of B00, so the two statements are consistent.
* **UV coefficient.** dΣ/d ln μ² = N(α/4π)[G₊(2k²/3 − m1² − m2²) + 2G₋ m1 m2]. This matches build a's statement.

**The four self-energies:**
* **AA:** G₊ = G₋ = 2Q².
* **AZ:** G₊ = G₋ = Q(g_L + g_R).
* **ZZ:** G₊ = g_L² + g_R², G₋ = 2 g_L g_R, so G₊ − G₋ = (g_L − g_R)² = I3²/(s²c²). Rewriting −2(G₊ − G₋)m²B0 in Denner's bracket gives −(α/4π)(2/3)·3 I3²/(s²c²) m² B0. **This is exactly the corrected reference term.** Denner's 3/(4s²c²) is its |I3| = ½ case, and the uncorrected reference would have rejected correct builds on the oracle's "odd" set (I3 = 3/2).
* **W:** G₊ = 1/(2s²) times w, G₋ = 0.
* **Ward identity:** G₊ = G₋ whenever one vertex is the photon, so Σ^AA(0) = Σ^AZ(0) = 0 for every m.

**Neutrino and Q = 0.** For Q = 0, g_R = −sQ/c = 0 identically. Therefore:
* a massless neutrino (L only) and a massive Q = 0 Dirac fermion with a sterile ν_R both get G₊ = g_L² and G₋ = 0;
* the "right-handed absent" rule needs no special code;
* build b's explicit `zr = 0` for m = Q = 0 is redundant but harmless.

**W weight.** The two W vertices give |V|², and the colour trace gives N_C, so w = N_C|V|². Both builds multiply by w and add no further N_C. This is correct.

**γ5 scheme.** I ran the same chain in Breitenlohner–Maison/'t Hooft–Veltman, with 4-dim external indices and the naive γ^μ P vertex. It differs from NDR by a finite rational term:

  Σ_HV − Σ_NDR = N(α/4π)(a_L − a_R)(b_L − b_R)(k² − 3m1² − 3m2²)/3.

The pole is unchanged. The shift is zero for AA and AZ but not for ZZ or W (see R1).

## 2. Independent numerics (`S/indep.py`, `S/compare.py`)

**Method.** A twice-subtracted dispersion relation:
* **Imaginary part:** from the on-shell (Cutkosky) trace with the Lorentz-invariant transverse projection,
  Im Σ = N(α/4)(λ^{1/2}/s)(1/3)[G₊(2s − m1² − m2² − (m1² − m2²)²/s) + 6G₋ m1 m2].
  Its normalisation is fixed by the massless limit Im Σ = π dΣ/d ln μ². It reproduces the vector β(3 − β²)/2 and axial β³ shapes.
* **Real part:** Re Σ(s) = Σ(s0) + (s − s0)Σ'(s0) + (s − s0)²/π · PV∫ Im Σ(s')/((s' − s0)²(s' − s)) ds', in mpmath at 30 digits.
* **Subtraction constants:** plain quadrature at one spacelike point s0 ≤ −1000 GeV².
* **Independence:** no B0, no closed-form logs, and no code from the builds or the reference.

**Coverage: 75 points**, listed in `compare.log`:
* k² = −10⁵, −1000, 0, 10⁻¹²;
* exact thresholds 4m_t², (m_t + m_b)² and 4·91² (W), and the thresholds ×(1 ± 10⁻⁶);
* the pseudo-threshold (m_t − m_b)², and k² = 10⁷ and 1.1·10⁸;
* masses 10⁻⁶ and 10⁴ GeV, a 10⁻⁶ against 10⁴ GeV doublet, and up↔down reversed doublets;
* unusual charges and weights: (300, Q = 1, I3 = 3/2, N = 2), (20, 0.3, −1), (5, −1/3, +1, 3), (0, −2/3, −1/2, 5), a massive Q = 0 neutrino (50 GeV) and a fully sterile fermion;
* μ = 1, 3, 20, 45 and 10⁴ GeV, and three (M_W, M_Z, α) sets.

**Result:** the worst relative deviation is 9.1·10⁻¹⁵ for build a, 9.1·10⁻¹⁵ for build b and 2.6·10⁻⁹ for the reference.
* The only reference deviations above 10⁻¹² are at k² = 0. There the reference evaluates at k² = 10⁻¹⁸ instead of 0, and the differences are α·10⁻¹⁸-sized absolute.
* The reference flip −f_AZ agrees with my own couplings. This confirms the Σ^AZ sign independently.

**What is and is not independent:**
* **The reference** is the orchestrator's transcription of a published formula (Denner, Fortschr. Phys. 41 (1993), App. B). It is not a derivation, and it was edited during this campaign (the I3 term, see `git diff`). The builds' derivations were done blind, and my derivation and numerics share no code with either.
* **What my work shares with the builds** is only the physics. The Feynman-parameter integrand is mathematically the same one (that is the claim being tested), and my subtraction constants use it at one Euclidean point.
* **What is independent:** the timelike, threshold and real-part behaviour and the whole k² dependence come from the cut and the dispersion integral. The couplings come from my own symbolic expansion of the Lagrangian.

## 3. Mutants of build a

Each mutant is one exact text substitution of `builds/a/ferm_se.py`. Each was run with `python3 gate.py --mode verifier --campaign ferm_se --oracle ferm_se/oracle.py --timeout 7000 <dir>` from `campaigns/`.

| Mutant | Error | Gate | Killed by | Proposed check that kills it |
|---|---|---|---|---|
| M01 | Σ^AZ sign flipped (Denner's photon convention) | FAIL | grid, μ, mass scan, above-thr | table, asymptotics |
| M02 | ZZ axial mass term dropped (G₋ = G₊) | FAIL | all five oracle checks | table |
| M03 | ZZ axial term with Denner's 1/(4s²c²), i.e. \|I3\| = ½ | FAIL | **grid only** (the single I3 = 3/2 fermion of the "odd" set) | table |
| M04 | AA with \|Q\| instead of Q² | FAIL | grid, μ, above-thr, own-precision | table, slope, asymptotics |
| M05 | colour factor missing in AZ | FAIL | grid, μ, above-thr | table, asymptotics |
| **M06** | 10⁻³ error only for 1.5 < k²/4m² < 4 (neutral loops) | **PASS** | – | `audit_table` |
| **M07** | μ clipped at 10⁴ GeV | **PASS** | – | `audit_table`, `audit_mu_log_linear` |
| M08 | masses < 10⁻⁴ GeV set to 0 | FAIL | **mass scan only, one point** (m = 10⁻⁶, k² = 3.6·10⁻¹², dev 1.3·10⁻⁶) | table, slope |
| M09 | working precision 16 digits | FAIL | blind continuity, grid, μ, mass scan, own-precision | table, μ-linearity |
| M10 | \|k²\| < 10⁻⁶ treated as k² = 0 | FAIL | **mass scan only, one point** (as M08) | table, slope |
| **M10b** | \|k²\| < 10⁻¹³ treated as k² = 0 | **PASS** | – | `audit_photon_slope_at_zero` |
| M11 | extra N_C = 3 in Σ_W when w > 1.5 | FAIL | grid, μ, above-thr, own-precision | table, asymptotics |
| **M12** | Q = 0 fermions treated as massless ("neutrino") | **PASS** | – | `audit_table` (massive Q = 0 points) |
| M13 | O(ε) rational term of B00 dropped | FAIL | blind Ward, all five oracle checks | table, slope, asymptotics |
| M13b | only its −k²/3 part dropped (Ward still exact) | FAIL | grid, μ, mass scan, above-thr, own-precision | table, slope, asymptotics |
| M14 | 'tHV/BM γ5 shift (G₊ − G₋)(k² − 3m1² − 3m2²)/3 | FAIL | grid, μ, mass scan, above-thr, own-precision | table, asymptotics |
| M15 | Σ_W sign flipped | FAIL | all five oracle checks | table, asymptotics |
| M16 | N_C inferred from the charge (3 if fractional) | FAIL | **grid only** ("odd" set, N = 2 and 5) | table |
| **M17** | at \|disc\| < 10⁻¹² B² (exact threshold) k² nudged by 10⁻⁶ | **PASS** | – | `audit_table` (exact thresholds) |
| M18 | ln μ² replaced by ln(μ M_W) | FAIL | blind Ward, grid, μ | table |
| M19 | ZZ axial mass term with the wrong sign | FAIL | all five oracle checks | table |
| **M20** | AA replaced by the massless form for k² < −10⁵ | **PASS** | – | `audit_table` (k² = −10⁶, −10⁸) |
| M21 | W k² = 0 branch wrong when m_up > m_down | FAIL | grid, μ, own-precision | table |
| **M22** | sets the global `mp.dps = 40` at import (violates SPEC §4) | **PASS** | – | `audit_global_precision` |
| C01 | CONTROL, not wrong: Σ^AA(0) and Σ^AZ(0) = 10⁻¹⁵ α M_W² (roundoff) | FAIL | grid, μ, mass scan, own-precision | **wrongly rejected** (C1); passes all proposed checks |

**Totals:**
* 24 genuinely wrong mutants. The gate kills 17, and **7 survive**: M06, M07, M10b, M12, M17, M20 and M22.
* **No survivor is an error at the benchmark point.** Each is a parameter region the oracle does not sample, or a rule it does not enforce.
* **The blind tier kills only 3** (M09, M13, M18). Every other kill comes from the oracle tier.
* **All 7 survivors fail `audit_proposed_checks.py`.**
* **Build a and build b pass all 5 proposed checks** (`checks_a.log`, `checks_b.log`). The worst values are 1.9·10⁻¹² (table), 1.4·10⁻¹⁴ (slope), 1·10⁻¹⁶ (μ-linearity) and 5·10⁻¹⁰ (asymptotics, which is O(m²/k²)), and the precision is untouched.
* **The control C01 passes the proposed checks.**

## 4. Findings

| # | Class | Finding |
|---|---|---|
| R1 | R | **γ5 scheme not named.** SPEC §2 says to "treat the trace of the chiral projectors so that the transverse part is unambiguous". Both builds and the oracle use an anticommuting γ5 (NDR). A builder using BM/'tHV with the naive γ^μP vertex gets the extra finite term N(α/4π)(a_L−a_R)(b_L−b_R)(k² − 3m1² − 3m2²)/3 in Σ_ZZ and Σ_W. Its μ dependence is still linear in k² and the Ward identity is still exact, so the blind tier cannot tell (M14 passes the blind tier). **Fix:** say "anticommuting γ5 (NDR)". |
| R2 | R | **"Σ_T is analytic at k² = 0" is false for m = 0.** A massless loop gives c k²(5/3 − ln(−k²/μ²)). It is continuous with limit 0, but Σ'(0) diverges logarithmically. **Fix:** "Σ_T is continuous at k² → 0 (analytic if every mass in the loop is non-zero)". |
| R3 | R | **The oracle tests fermions the SPEC does not postulate.** SPEC §1 puts the left-handed component in a *doublet* with a Yukawa mass, so \|I3\| = ½. The oracle's "odd" set uses I3 = 3/2, and (91, Q = 0, I3 = 0). The natural extension (T3 = I3, Y = Q − I3) is what both builds and the corrected reference implement, and §1 confirms it is the coupling-level answer. **Fix:** state "I3 is the T3 of the left-handed component, any value". |
| C1 | C | **The oracle is over-strict at exact zeros.** `_dev` uses the floor 10⁻⁹ α M_W² together with the tolerance 10⁻⁹. Where the reference is 0 (Σ^AA(0), Σ^AZ(0)), a build must therefore return \|Σ\| ≲ 5·10⁻¹⁷ GeV². The roundoff-sized control C01 (10⁻¹⁵ α M_W², 1000× below the blind Ward tolerance) is rejected by four oracle checks. Both builds pass only because they work at 50 or 120 digits. **Fix:** as in bos_se, an absolute floor of 10⁻³ α M_W² in `_dev`. |
| C2 | C | **Coverage gaps.** None of the following is sampled: the neutral window 1.5–4 × threshold; exact thresholds; k² < −5 M_W² (except −2000 and −3000); μ > 10⁴ GeV; massive Q = 0 fermions; 0 < \|k²\| < 10⁻¹² GeV²; the global precision rule of SPEC §4. M08 and M10 are each killed by one mass-scan point. M03 (the uncorrected I3 term) and M16 are each killed only by the "odd" set. Each gap has a proposed check (§3). |
| C3 | C | **The reference stands in k² = 10⁻¹⁸ for k² = 0.** That is not small next to m² once m ≲ 10⁻⁶ GeV. At Σ_W(0) with (10⁻⁶, 2·10⁻⁶) GeV it is off by 1.3·10⁻⁷ relative, and it fails that one point of `audit_table` (`checks_ref.log`), while both builds are exact. This is harmless inside the oracle's floors, but the reference should take the k² → 0 limit analytically (or use k² ≪ min m²) before any oracle point is added there. |
| C4 | C | **The blind tier is weak** (3 of 24 kills). Three reference-free checks could move into `campaign.BLIND` without leaking the result: `audit_mu_log_linear`, `audit_global_precision` and `audit_photon_slope_at_zero` (textbook charge renormalisation). |
| N1 | N | **Independent confirmation of all four self-energies,** including the Σ^AZ sign, the general-I3 axial term, the absence of a rational remainder in NDR, the neutrino and Q = 0 handling, and the W weight (§§1–2). |
| N2 | N | **Prose slips in the builds; the code is unaffected.** Build a's DERIVATION writes (g_L − g_R)² = I3²/(s²c²) "= 1/(4s²c²)", which is the \|I3\| = ½ case, though its code is general. Build b's DERIVATION §4(b) has a garbled B0 expression. Neither affects the code. Both builds keep their precision local (`workdps`). |

## 5. Not verified

* Gauge-parameter independence: not applicable, because the fermion loop has no gauge propagator inside it.
* The full fermionic Δr.
* Masses below 10⁻⁶ GeV.
* The builds' DERIVATION prose beyond the points above.
