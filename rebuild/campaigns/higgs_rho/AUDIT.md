# AUDIT: campaign higgs_rho (Higgs-mass dependence of the one-loop rho parameter), builds a and b

Auditor (red team). I edited nothing in the repository or in the builds. All scripts are in this directory. They ran on
copies of the build modules (`copies/a`, `copies/b`) with bytecode writing off. The mutants are in `mutants/`, and the
gate wrote its `gate_report.json` only inside those directories.

Paths: SPEC/campaign/oracle in `/home/user/STUR-Physics-Lab/rebuild/campaigns/higgs_rho/`.
Build a is `.../scratchpad/room-higgs_rho-a/builds/higgs_rho-a/`, build b is `.../scratchpad/room-higgs_rho-b/builds/higgs_rho-b/`.

## 0. Bottom line

Both builds are physically correct. I derived the Feynman rules myself and the diagram set is complete. I evaluated
the diagrams by a route that uses no Passarino–Veltman reduction and no 1/d tensor trick, and it agrees with both
builds to 0 ulp in double precision. This holds for rho_higgs_rel and for the raw self-energies, over mH = 10…5000 GeV,
ξ = 0.3, 1, 4 and μ = 17, MW, 3.7 MW. A second route of my own (4D Euclidean radial integration) agrees as well.

The gate plus the oracle, however, cannot tell the correct finite function from a wrong one. Seven of my ten
modules pass the full verifier gate: the correct control M0 and six wrong mutants. The wrong ones include a typed-in
heavy-Higgs asymptotic formula (2.6× off at 125 GeV), leading-order heavy-mass PV functions (87% off at 125 GeV) and a
gauge-dependent result.

## 1. Physics, independently of the builders

### 1.1 Feynman rules

`vertices.py` expands |DΦ|² in sympy. The fields are commuting symbols and each ∂_μF is a symbol (output in
`vertices_out.txt`). With c real, these are all the monomials that contain H:

| term in L | coefficient | Feynman rule (incoming momenta, ∂ → −ip) |
|---|---|---|
| H W⁺W⁻ | g²v/2 = g M_W | i g M_W g^{μν} |
| H Z Z | g²v/(4c²) | i (g/c) M_Z g^{μν} (×2 for ZZ) |
| H² W⁺W⁻ | g²/4 | i g²/2 g^{μν} |
| H² Z Z | g²/(8c²) | i g²/(2c²) g^{μν} |
| W⁻(H∂φ⁺ − φ⁺∂H), W⁺(H∂φ⁻ − φ⁻∂H) | +ig/2, −ig/2 | ±i(g/2)(p_φ − p_H)^μ |
| Z(H∂φ⁰ − φ⁰∂H) | g/(2c) | (g/2c)(p_φ − p_H)^μ |
| H φ^± W^∓ Z, H φ^± W^∓ A (quartic) | −g²s²/(2c), g² s/2 | (not used, see 1.2) |
| H Z ∂H, Z ∂H | 0 | none |

There is no H W Z, H W γ, H γγ or H Z γ vertex at tree level. The R_ξ functions F^± = ∂·W^± ∓ iξM_Wφ^± and
F_Z = ∂·Z − ξM_Zφ⁰ contain no H. They cancel the V–∂φ mixing and give the Goldstones the mass² ξM_V². The gauge
propagator is −i[g − (1−ξ)kk/(k² − ξM²)]/(k² − M²). For the W, the product of the two derivative vertices in the
H-φ loop is (i g k^μ)(i g k^ν) = −g² k^μk^ν. For the Z it is (κk^μ)(−κk^ν) = −κ²k^μk^ν. These are identical with
κ = g → g/c, which is the structural fact both builds use.

### 1.2 Completeness of the diagram set

A one-loop 1PI two-point function of W⁺W⁻ (or ZZ) is either two cubic vertices joined by two propagators, or one
quartic vertex closed on one propagator. With at least one H line, the candidates are:

* **Cubic vertices:** V–V–H (H-V loop) and V–φ–H (H-Goldstone loop). A loop with H plus a photon or a Z would need
  H W γ or H W Z: none exists. A loop with H plus W for the Z would need H Z W: none exists.
* **Quartic vertices:** the loop must close two conjugate fields of one vertex. H²VV gives the H seagull.
  H φ W Z and H φ W A have no conjugate pair (and the wrong external legs), and no H–φ mixed propagator exists.
* **Ghosts:** ghosts appear only bilinearly. A ghost loop on two external V's uses two V-c̄-c vertices and contains no
  H. The H c̄c (∝ ξ) vertex enters only H tadpoles.
* **Photon:** no γ-H coupling. Π_γZ gets no H contribution, because H and φ⁰ are neutral.

So the set is complete: seagull, H-V and H-φ for each of W and Z, plus tadpoles. Both builds use exactly this set
(a DERIVATION §2, §4; b DERIVATION §1–2). **Low:** neither build writes out the exclusion of mixed W–Z/W–γ loops,
and both lists of "H-containing terms" omit the quartic H φ W Z / H φ W A terms (a DERIVATION:19–22, b DERIVATION:8–15).

### 1.3 Tadpoles

An H tadpole enters only through HVV with coupling 2M_V²/v (from M_V²(1 + H/v)²). So Π^tad_VV/M_V² = 2⟨H⟩/v is
the same for W and Z and cancels in Δρ. This holds for any ξ (the ξ-dependent tadpole value is common to both).
Both builds state this correctly (a §2, b DERIVATION:47).

### 1.4 Exact ξ independence

H-V diagram: (1−ξ)M²/((k²−M²)(k²−ξM²)) = 1/(k²−M²) − 1/(k²−ξM²). So
16π²Π_c/κ² = −[M²B0(m_H,M) − B00(m_H,M) + B00(m_H,√ξM)]. The last term cancels 16π²Π_b/κ² = +B00(m_H,√ξM) exactly,
for each V separately. I checked this numerically per diagram at mH = 400 GeV, M = M_Z (`compare_out.txt`). The
H-φ and H-V parts move with ξ by ±(2783 to 13753) GeV². Their sum stays 35829.8683073737 for ξ = 0.3, 1, 4.

Build b keeps ξ explicit. Its F (b `higgs_rho.py`:31–38) reduces algebraically to 4·16π²h of build a, via
(1−ξ)M²·g[ξM², M², m²] = L2(M², m²) − L2(ξM², m²), so the ξ-dependent pieces collapse to L2(M², m²) + (m² + M²)/2.

### 1.5 Independent evaluation (`indep.py`, `compare.py`, `asym.py`)

* **Route I (exact-d Feynman parameters).** Each diagram uses ∫ℓ^μℓ^ν/(ℓ²−Δ)^n in exact d, with MS-bar Δ_UV dropped:
  * A0 = m²(1 − ln m²/μ²)
  * B0 = −∫ln Δ
  * C2 (the k k two-propagator coefficient) = ½∫Δ(1 − ln Δ)
  * C3 (the three-propagator coefficient) = ½∫_simplex(−ln Δ)

  This route has no PV reduction, no k k → g k²/d step and no ξ cancellation imposed. Result: rho_higgs_rel and
  self_energy_W/Z equal both builds with relative difference **0.0** (maximum over the grid) in double precision.
* **Route II (4D Euclidean radial integral).** I wrote my own integrand of the double difference
  [I(mH,W) − I(mH,Z)] − [I(W,W) − I(W,Z)], in which polynomial scheme differences cancel. It agrees with route I
  to 0.0 for ξ = 0.3, 1, 4.
* **Large-mH constant, analytic.** The M-dependent part of 16π²h is ¾M² ln(m_H²/μ²) − (5/8)M² + o(1). That gives
  rho_rel → B ln(mH²/MW²) + C with C = 9.53900888e-4 (inputs MW = 80.38, MZ = 91.19, α = 1/128). The numerical value
  at mH = 1e6 MW is 9.539007e-4, which converges correctly.

Reference values (ξ-independent, μ-independent):

| mH [GeV] | 10 | 50 | 125 | 200 | 300 | 1000 | 5000 |
|---|---|---|---|---|---|---|---|
| rho_higgs_rel | 2.670871522e-4 | 1.375766683e-4 | −2.052058478e-4 | −5.151967285e-4 | −8.533394666e-4 | −2.111424485e-3 | −4.006329408e-3 |

**No difference was found, however small.**

## 2. Mutants: what the gate and oracle let through

`make_mutants.py` writes each mutant as the correct closed form with exactly one plausible error. I ran
`gate.py <dir> --mode verifier --campaign … --oracle …/oracle.py --timeout 900` on each. The summary is in
`gate_summary.txt` and each full gate output is in `mutants/*/gate_stdout.txt`.

| mutant | error | verifier gate | how wrong |
|---|---|---|---|
| M0_control_correct | none (control) | PASS | — |
| **M1_no_seagull** | H²VV seagull dropped | **PASS** | rho_rel exact; Π_WW(125) 15.80 vs 14.53 GeV² |
| **M1b_double_seagull** | seagull symmetry factor ½ forgotten | **PASS** | rho_rel exact; Π wrong |
| **M2_no_1overd** | finite ε·(1/ε) part of B00 dropped (k k → g k²/4) | **PASS** | rho_rel exact; Π_WW(125) 6.83 vs 14.53 |
| **M3_long_sign** | sign of the (1−ξ)kk/(k²−ξM²) propagator term flipped | **PASS** | exact at ξ = 1, gauge-dependent elsewhere: rho_rel(125, ξ = 4) = −8.69e-5 vs −2.05e-4 |
| M4_B0_equal_mass | B0(0;m,m) = 1 − ln m² (A0/m²) | FAIL (custodial) | constant offset not ∝ s² |
| **M5_heavy_higgs_only** | Δρ = B ln(mH²/MW²) recited for all mH | **PASS** | rho_rel(125) −5.30e-4 vs −2.05e-4 (2.6×); C = 0 (3.5e-18) vs 9.54e-4 |
| **M6_heavy_mass_PV** | B0, B00 replaced by their leading heavy-mass forms (poles exact) | **PASS** | rho_rel(125) −2.68e-5 vs −2.05e-4 (−87%); C = 5.03e-4 vs 9.54e-4 |
| K1_control_divdiff | B0 divided difference over a instead of a−b | FAIL (μ) | control |
| K2_control_hphi_sign | sign of the H-φ bubble flipped | FAIL (slope, oracle) | control |

Why they survive:

* Every blind check passes for any smooth h(M) whose ln mH² coefficient is ¾M² and whose pole is mH-independent:
  * b_reference_zero is automatic;
  * b_custodial (campaign.py:38–48) holds for any smooth h;
  * b_sign_and_size checks monotonicity only;
  * b_difference_consistent checks internal consistency only.
* b_mu_independent (campaign.py:22–29) loops over ξ but compares only μ values. Nothing compares rho_rel across ξ at
  finite mH.
* The oracle's xi_check (oracle.py:29–31) tests log_coefficient, which both builds (and every mutant) compute
  analytically without using ξ, so the check is vacuous.
* Any term in h that is independent of M or of mH drops out of rho_rel identically. That includes the seagull, the 1/d
  term and M²-constants. So rho_rel is structurally blind to those errors, and the raw self-energy exports are never
  checked against anything.

Proposed checks (`proposed_checks.py`, run by `run_proposed.py`, output in `run_proposed_out.txt`). They use the
independent reference values above.

| check | tolerance | a | b | kills |
|---|---|---|---|---|
| finite_function_check: rho_rel at mH = 10, 50, 125, 200, 300, 1000, 5000 | 1e-9 rel | PASS (0) | PASS (0) | M5, M6 (and M4, K1, K2) |
| xi_finite_check: rho_rel at mH = 50, 300, 1000; ξ = 0.3, 4, 25; μ = MW, 3.7MW | 1e-9 rel | PASS | PASS | M3 |
| constant_check: rho_rel(1e6 MW) − B ln, vs C_INF = 9.53900888e-4 | 1e-5 rel | PASS | PASS | M5, M6 |
| raw_self_energy_check: Π_WW, Π_ZZ at 3 (mH, ξ, μ) points (needs SPEC to pin CDR, see 4) | 1e-9 rel | PASS | PASS | M1, M1b, M2, M3 |
| landau_check: ξ = 0 | 1e-9 rel | PASS | **FAIL (nan)** | (finding L1) |

## 3. Hidden answers and provenance

* **Build b (5 Bash calls, about 4 min, no scratch work in the room except `tmp/cust.py`, a custodial probe).** The
  DERIVATION does not recite a known closed form. The standard heavy-Higgs expression (with its constant) and the
  Veltman-style functions appear nowhere. b's runtime formula is its own ξ-explicit divided-difference form
  (b `higgs_rho.py`:31–38), which I showed equals a's only after a non-trivial algebraic collapse.

  Every step is stated as an intermediate result: vertices; each diagram as an integral expression; the poles (−3M²,
  mH- and ξ-independent); the 4/d bookkeeping; the asymptotics (4 − (1−ξ) − ξ = 3). I re-derived each one and all
  are correct. The working, however, is "expanded by hand" with no shown algebra.

  Two assertions are not derived:
  * **b DERIVATION:39** says the W vertices are "g k^μ and g k^ν" and the Z vertices "−g_Z k, g_Z k", with "same
    overall sign". As written the two products have opposite signs; the true W vertices are i g k^μ and i g k^ν.
    "Checked against scalar QED" is not shown.
  * **b DERIVATION:66–67** admits that the relative sign of the vertex products "was fixed by hand and cross-checked
    by the ξ-independence". Part of the sign is therefore fixed by a consistency requirement, not derived. It is
    correct (K2 shows a wrong sign breaks the slope), but it is not derived. **Low/medium.**

  The ghost argument (b DERIVATION:20–21) is garbled, though its conclusion is right.

  Second routes (b `higgs_rho.py`:73–114; I ran `__main__` and it passes): exact-d at ε = 1e-12, Feynman-parameter
  quadrature of B0 and K, a ξ scan and a μ scan. These check only the evaluation of b's integrals, not the Feynman
  rules or the diagram assembly.
* **Build a.** It has sympy vertex extraction (room `tmp/vertices.py`; I read it, and it matches mine) and an
  explicit diagram-by-diagram derivation (a §4). Its second route (a `higgs_rho.py`:86–104, a DERIVATION §6(i)) is a
  direct Euclidean integration with explicit R_ξ propagators. That route does test the assembly and the ξ
  cancellation; I re-ran it and it agrees to 12 printed digits. a's B (a:71–75) is checked against a sympy limit in
  `__main__`.

  **Low:** the vertex table (a DERIVATION:39) gives the W–φ–H rule as ±(g/2)(p_φ − p_H), missing the factor i. The
  diagram in §4(b) is computed only for the real (Z-like) coupling and carried to W by the "κ" argument. That is
  valid for the product, but it is not shown for the W.
* **PROVENANCE vs code.**
  * a:78–83: the notes match. `self_energy_*` ignore xi, which matches the "xi cancels" note.
  * b:5–10: the notes match.
  * In both builds `log_coefficient` is a hand-typed analytic expression from the DERIVATION's asymptotics
    (a:75, b:70), not computed from the loop functions at run time. That is accurate as "derived" (by hand), and a
    verifies it in code. b's expression 3α(MW² − MZ²)/(16π s² MW²) is the target −3α/(16πc²) in disguise. It is
    legitimately derived in b §3, but the lint cannot see such forms.

## 4. Independence

The exact agreement (0.0) is algebraic, not coincidental. b's F ≡ 4·16π²h_a identically (1.4), and both evaluate it at
50 digits and round to float, so the doubles coincide. Both builds follow the conventions that SPEC pins:
M²(eff) = M² + Π, the 1PI sum = iΠg^{μν}, ½Π_ZZZ², MS-bar, and k k → g k²/d with the ε/ε piece kept. My route I
uses none of their reduction steps (no PV, no 1/d trick, exact-d tensor formula) and reproduces the raw Π exactly.
So the shared convention is the correct reading of SPEC, not a shared mistake.

The routes differ in substance:
* a cancels ξ analytically, and its code has no ξ;
* b keeps ξ in code;
* a's Euclidean check tests the assembly;
* b's checks test only the integrals.

What is common to both, and to me, is the Lagrangian in SPEC and the standard vertex derivation, which I checked
mechanically.

SPEC ambiguities:
* **Medium.** SPEC:29 says "d = 4 − 2ε, MS-bar" but does not say whether the k^μk^ν → g^{μν}k²/d reduction (CDR) or a
  4-dimensional g^{μν}k²/4 (DRED-like) is meant. The two differ in raw Π by κ²(mH² + M²)/(8·16π²). That is exactly
  mutant M2: Π_WW(125) = 6.83 vs 14.53 GeV². The difference cancels in rho_rel.
* MS vs MS-bar, or e^{γε}(4π)^{−ε} vs Γ(1+ε)(4π)^{−ε}, differ only at O(ε²): no one-loop effect.
* Including the tadpoles would change raw Π (in a ξ-dependent way), but SPEC excludes them.
* The sign of Π and the Z normalisation are pinned.

So rho_higgs_rel is unambiguous. The raw self-energies are unambiguous only once CDR is stated, which a raw oracle
would need.

## 5. Isolation

* Both transcript audits are CLEAN (`builds/{a,b}/isolation_audit.txt`).
* The build files contain no literature terms: grep for Veltman, Peskin, Takeuchi, screening, PDG, G_F, "known",
  "standard", "textbook" and the canary found nothing. The physics vocabulary is first-principles.
* Process note (low): campaign.py was replaced during a's build (a DERIVATION:140–144; ACCEPTED.md class R) after b
  reported the custodial-check bug. A file in a's room therefore changed in response to b's work. The change touched
  only a blind check, and a states that nothing in the build changed as a result, which is consistent with the code.
* Nothing in either build suggests knowledge from outside the room.

## 6. Findings by severity

**High**
* **H1: the gate plus oracle verify only the large-mH logarithm.** Six wrong mutants pass the full verifier gate
  (M1, M1b, M2, M3, M5, M6), including:
  * a recited asymptotic formula (2.6× off at 125 GeV);
  * leading-order PV functions (−87% at 125 GeV);
  * a gauge-dependent rho_rel (−58% at ξ = 4).

  The causes:
  * no finite-function reference;
  * no ξ test of rho_rel (campaign.py:22–29 compares only μ);
  * the vacuous oracle xi_check (oracle.py:29–31);
  * raw self-energies never checked.

  This is a defect of the campaign, not of either build. **For these two builds it is closed by my two independent
  routes (§1.5, 0 ulp).** For future builds it stays open until `proposed_checks.py` (or equivalent) is adopted.

**Medium**
* M1: the self_energy_W/Z exports are unverifiable as the campaign stands. SPEC:29 does not pin CDR vs 4D tensor
  reduction (a 2× difference in Π), and rho_rel is blind to the seagull and the 1/d term.
* M2: b's DERIVATION is terse. Its Feynman rules were done in-head with no shown algebra, and the H-φ vertex-product
  sign was partly fixed by demanding ξ-independence (b DERIVATION:39, 66–67). It is correct but under-derived.

**Low**
* L1: build b returns nan in Landau gauge ξ = 0 (b `higgs_rho.py`:36–38, log(0) in the divided difference with node
  ξM² = 0). ξ = 1e-30 works. Build a is fine.
* L2: a's vertex table omits the factor i on the W–φ–H rule (a DERIVATION:39).
* L3: both builds' lists of H terms omit the quartic H φ W Z / H φ W A vertices, and neither explicitly excludes mixed
  W–Z/W–γ loops (the exclusion is correct; my sympy confirms that no H W Z or H W γ vertex exists).
* L4: b's ghost paragraph is garbled (b DERIVATION:20–21).
* L5: `log_coefficient` is hand-typed in both builds. It is correct and derived in the DERIVATION, but it is the form
  the lint cannot see.
* L6: process: campaign.py changed during a's build in response to b (§5).

## 7. Verdict

**ACCEPT the result** (both builds). rho_higgs_rel(mH) as tabulated in §1.5:
* the large-mH form is B ln(mH²/MW²) + C, with B = −3α/(16πc²) = −6.001224e-4 and C = 9.539009e-4;
* the result is exactly ξ-independent and μ-independent;
* the raw MS-bar (CDR) self-energies are as in `proposed_checks.PI_REF`.

Both builds are physically correct and agree with my independent exact-d Feynman-parameter and Euclidean routes to the
last bit. The only high-severity finding (H1) concerns the gate and oracle, and it is closed for these builds by §1.5,
not by the gate pass.

Before this campaign's gate is reused:
1. Add finite_function_check, xi_finite_check and constant_check to the oracle.
2. Pin CDR in SPEC §2 and add raw_self_energy_check.
3. Drop or fix the vacuous xi_check.
4. Ask b to handle ξ = 0 and to show its vertex signs.

## Files (all in this directory)

* `indep.py` (routes I and II), `compare.py` → `compare_out.txt`
* `vertices.py` → `vertices_out.txt`
* `refvalues.py` → `refvalues_out.txt`, `asym.py` → `asym_out.txt`
* `make_mutants.py`, `mutants/*` (each with `higgs_rho.py`, `DERIVATION.md`, `gate_stdout.txt`, `gate_report.json`),
  `gate_summary.txt`
* `proposed_checks.py`, `run_proposed.py` → `run_proposed_out.txt`
