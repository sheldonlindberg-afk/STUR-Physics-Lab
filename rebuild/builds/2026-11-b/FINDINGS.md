# Verifier findings: build 2026-11-b

Verifier session, 2026-11-13. Followed `rebuild/prompts/verifier.md`. *Subagents can't write in the
repository, so the orchestrator wrote this file from the verifier's report, after re-running the
three harness commands below and seeing the same RESULT lines.*

The verifier read `ORCHESTRATOR_LOG_2026-11-b.md` and build a's FINDINGS.md first. Nothing in `src/`
or the build was edited. Third routes: sympy and mpmath at 30-40 digits.

## Harness results (verbatim RESULT lines)

| Command | RESULT line |
|---|---|
| `python3 rebuild/harness.py rebuild/builds/2026-11-b --mode verifier --ledger` | `RESULT: ALL GATES PASS` (every stage PASS; oracle 1+18+7+6+5+10+21+8 = 76/76) |
| `... 2026-11-b --mode verifier --compare rebuild/_selftest/reference_build` | `crossbuild 17/18`, `FAIL chiral.sigma_model_vacuum: max rel diff 1.03e-06`, `RESULT: FAILURES (see above)` |
| `... 2026-11-a --mode verifier --compare rebuild/builds/2026-11-b` | `crossbuild 18/18`, `RESULT: ALL GATES PASS` |

LEDGER.md: 58 derived, 0 input, 7 quoted. All 7 quoted exports are on their `quoted_allowed` lists.

## Class counts

| B | R | C | N |
|---|---|---|---|
| **0** | **0** | **7** | **7** |

No class R finding survived a third route. In F1, N2 and N3 the reference is the less precise side.

## Findings table

| # | Check | Class | Evidence | Action |
|---|---|---|---|---|
| F1 | probe `chiral.sigma_model_vacuum(1.7, 0.9, 0.03)`, 1.03e-6 vs rtol 1e-8: the only harness failure | **N** (build a's F1 applies; the reference is the less precise side) | sympy: σ₀ = 0.91070161535992360530, m_π² = 0.032941634772596212040. Build b: σ₀ to 1 ulp, m_π² rel err 1.6e-16. Reference: +1.029e-6 (the 2λh² of the 2h diagonal at `src:386`). A SPEC-literal 3-point diagonal at h = 1e-4 gives +2.55e-7, so no correct build can pass this probe. a/b agree to 1.44e-12 by different routes (a: Richardson Hessian; b: the stationarity identity H/σ₀). | As in build a: the owner decides on the `src` `hessian()` fix, or the probe compares with H/σ₀. |
| N2 | probe `blackholes.isco()` (b vs ref 4.77e-9, rtol 1e-8); oracle "ISCO 6M" (rtol 2e-4) | **N** (applies) | Build b returns (6.0, 12.0, 0.888888888888889), exact to rounding. Build a: 6.000000000006. Reference adapter: 6.0000000286. The pass margin against the reference is still 2x. | Compare the probe with the closed form, or tighten the adapter. Tighten the oracle rtol to 1e-8. |
| N3 | oracle safe-gap / 2.1868 rad pins | **N** (applies; the reference grid) | Build b gap = 181.10727825727617 µm, 7e-16 from mpmath. design_phase = 2.187786760330193, 9.6e-12 from mpmath 2.187786760309 (the SPEC-fixed n = 4001 trapezoid). The reference grid point is 181.16092 µm (+2.96e-4), with phase 2.1868 (−4.5e-4). SPEC §4 says "not on a coarse grid". | Owner's call (open since build a): bisect in `src` `casimir_safe_gap()` and re-pin 181.107 µm / 2.1878 rad, or annotate the pin as "first grid point". |
| N4 | oracle "Planck-mass black hole k_B T" | **N** (applies; oracle rounding) | The oracle compares with 1.22089e19/(8π), 1.05e-7 low. Build b is ~1e-16 from mpmath. | Optional: compare with the full-precision M_Pl/(8π). |
| N5 | oracle "neutrality needed: 2.82e-19 e per nucleon (pinned)", rtol 2e-3 | **N** (new; pin rounding, small margin) | mpmath 2.8243652699202e-19; build b ~1e-16 from it. The 3-digit pin is 1.548e-3 low, so the pass margin is only 1.3x (same for build a). | Re-pin as 2.8244e-19 with rtol 1e-6, so a convention change (C5) can't hide in the rounding. |
| N6 | probe `desitter.ricci_scalar(0.2, 5.0, ...)` (a-b and b-ref 3.23e-11, rtol 1e-8); oracle Ricci checks (rtol 1e-7) | **N** (a pass that is not independent; for information) | Build b is exact (0.48000000000000004, from an analytic dω table checked against finite differences). Build a and the reference adapter both give 0.4799999999844744: the same central difference h = 1e-5 of the same ω table. Their mutual agreement is not independent evidence; build b is the independent route. | None required. |
| N7 | oracle "Euclidean section smooth at period 2π/(f'/2)" (rtol 1e-5); the log's "200 trapezoid nodes" item | **N** (adequate; quantified) | Build b ratio 1 − 9.94e-8. The exact ratio at ε = 1e-7 r_b is 1 − 7.99e-8 (the physical O(ε) term). Truncation error of the 200-node rule is 1.0e-12; the rest is rounding near the float root. Total error is 100x inside the rtol. Build a: −4.64e-7. | None. |
| C1 | oracle "eps R^e^e = 2 e R"; new Ricci gate | **C** (build a's C1; resolved for curvature) | Build b passes the three Ricci = 12/ℓ² checks exactly. Its `ricci_scalar` contracts the same R array as `action_coefficients`, so the curvature itself is gated. cR = 2 remains an ε-identity, acceptable as a sign-convention probe. | None beyond build a's resolution. |
| C2 | provenance kinds | **C** (applies; deferred to the auditor) | `kerr_first_law`, `kerr_area_km2` and `planck_bh_kT_GeV` are "derived" but rest on quoted formulas; `pi0_width_from_rungs` is "quoted". Same pattern as build a. | Build a's proposed SPEC §0 rule, still open. |
| C3 | `desitter.ell_from_lambda`, pins ℓ = 1.647e26 m and coupling 1.04e122 | **C** (SPEC gap, flagged by the builder) | SPEC §6 never defines Λ. Builds a and b and src all take Λ as the constant in e(R − 2Λ), and agree. Under the other common reading, e(R − Λ), ℓ changes by √2 and the pins fail. | SPEC §6: "Λ is the cosmological constant of the Einstein-Hilbert action (1/16πG)∫e(R − 2Λ), i.e. G_μν + Λg_μν = 0. `ell_from_lambda` is the ℓ for which the MacDowell-Mansouri action reduces to that form." |
| C4 | oracle "Killing κ_b, κ_c" and "Schwarzschild κ = 1/4M" (rtol 1e-5) | **C** (convention; all three agree) | `killing_kappa` returns κ at the sample point, with no extrapolation, in builds a and b and `src:857` (a/b agree bit for bit). The oracle's ~2e-6 deviation is its own sample offset; the finite-difference error is only ~5e-9. Margin 4x. | SPEC §7: "`killing_kappa(f, r0, h)` returns κ evaluated at r0 itself". Oracle: compare with \|f′(r₀)\|/2 at rtol 1e-7, which tests the Christoffels rather than the offset. |
| C5 | `links.neutrality_per_nucleon` (pinned 2.82e-19) | **C** (SPEC gap) | SPEC gives only the ratio kQ²/(Gm²). Builds a and b and `src:1115-1117` all assume equal net charges, vacuum Coulomb, nucleon count m/u and fraction = GAP_FRACTION. Alternatives fail the pin: m/m_p gives +0.73%; k/ε_r gives a factor √5.7. | SPEC §8: "Both diamonds carry the same net charge Q = ε e (m/u), u = `inputs.U_AMU`; the Coulomb potential is the vacuum kQ²/r, k = `inputs.K_COUL`; the bound is \|φ_C\| ≤ GAP_FRACTION·\|φ_G\|." |
| C6 | `casimir.casimir_safe_gap` | **C** (SPEC gap, flagged by the builder) | SPEC §4 says "gravity phase" without the potential, and casimir can't import graviton. Builds a and b, src and the blind check all use −Gm²/r. | SPEC §4: "The gravity phase uses U_G = −G m²/r with `inputs.G_NEWTON` (rung 4 derives this; rung 3 assumes it)." |
| C7 | oracle "m_π² = H/⟨σ⟩ at the vacuum" (two cases, rtol 1e-5) | **C** (can't fail for build b) | Build b's `sigma_model_vacuum` returns H/σ₀ by construction (`chiral.py:72`). The Hessian appears only in the derivation and self-check, so the PROVENANCE note "from the Hessian" overstates the code. No oracle check tests σ₀ itself; only the crossbuild probe does (b matches sympy to 1 ulp). | Oracle: compare σ₀ with the reference's cubic root, and m_π² with λ(σ₀_ref² − v²). Or SPEC §3: say whether m_π² must come from the mass matrix or may use the vacuum condition. |

## Probe triage (18 probes; max rel diff a-b / b-ref)

| Probe | a-b | b-ref | Verdict |
|---|---|---|---|
| gauge331.mass_matrix | 1.8e-16 | 1.8e-16 | Same construction from Gell-Mann matrices. |
| gauge331.neutral_masses | 3.3e-16 | 1.2e-14 | eigvalsh on the 3x3 block; second routes differ. |
| gauge331.quark_charges | 0 | 0 | Same affine-anomaly route. |
| chiral.chpt_mpi | 0 | 0 | Quoted formula. |
| chiral.sigma_model_vacuum | 1.4e-12 | **1.03e-6 FAIL** | F1 (N); C7. |
| casimir.cp_integral | 0 | 0 | 23/4 in both by the same closed route, implemented differently. |
| casimir.casimir_safe_gap | 7.5e-16 | 3.0e-16 | Same equation and bracket; mpmath confirms. |
| graviton.entangling_phase | 0 | 2.4e-16 | SPEC-fixed formula and trapezoid. |
| graviton.design_phase | 1.4e-15 | 0 | Same; N3 for the pin. |
| desitter.action_coefficients | 2.2e-16 | 1.0e-15 | ε-identity (C1). |
| desitter.ricci_scalar | 3.2e-11 | 3.2e-11 | N6: b exact; a and the reference share one stencil. |
| blackholes.sds_horizons | 0 | 0 | All bisect to the correctly rounded roots. |
| blackholes.isco | 1.0e-12 | 4.8e-9 | N2. |
| blackholes.kerr_first_law | 0 | 0 | Exact Fractions; identical route in a and b. |
| links.pi0_width_eV | 0 | 2.3e-16 | Polarization sum computed with levi_civita in both. |
| blackholes.kappa_from_spin_connection | 1.4e-16 | 1.8e-16 | At the SPEC offset. |
| links.matter_charges | 0 | 0 | Exact, via rung 1. |
| links.planck_bh_kT_GeV | 0 | 0 | Via `hawking_K` (N4). |

## Independence: build a vs build b routes

The SPEC and contract channel most derivations into one route. Most a/b agreements are therefore
"same derivation, independently implemented", and the third routes (sympy, mpmath, literature) carry
the evidential weight. The genuinely different routes are:
- chiral m_π² (a: Richardson Hessian; b: stationarity identity), agreeing to 1.4e-12;
- desitter's Ricci scalar (a: finite-difference dω; b: analytic dω);
- blackholes' cone-ratio quadrature and Nariai mass (a bisects 1 − 3x²; b uses the analytic ℓ/√27).

Shared routes: the toolkit algorithms (SPEC §1), gauge331's photon direction and 1/e² (the same closed
form), casimir's 23/4 route, graviton's SPEC-fixed phase, desitter's ε contractions and Λ convention
(C3), blackholes' horizons, κ, orbits and Kerr algebra, and links' conventions (C5).

## Provenance spot-check (build b code)

- **Verified as claimed:** `quark_charges`, `cp_integral` (no 23/4 literal), `casimir_safe_gap`,
  `photon_sphere` and `isco` (no closed forms on the code path), `ricci_scalar`, the polarization sum,
  `kappa_from_spin_connection`.
- **Honest but typed rather than computed:** `photon_direction`, `ell_from_lambda` (√(3/Λ) typed after
  derivation; build a computes the 3 as cV/(4cR)), `nariai_mass_kg` (ℓ/√27), the phase-space factor.
- **Overstated:** the `sigma_model_vacuum` note (C7).
- **C2 pattern:** `kerr_first_law`, `kerr_area_km2`, `planck_bh_kT_GeV`.

## Feedback to the builder

No class B findings, so there is no build-error feedback. C3 to C7 reach a future build only as SPEC or
oracle changes, without numbers.

## Class R issue notes

None. F1: sympy shows imprecision at `src/ladder_standalone.py:386`, not an error in the physics. N3:
mpmath shows the pins describe the grid point at `src/ladder_standalone.py:573`. N2: the adapter's
search tolerance.

## Addendum 2026-11-14: weak, running, and the derived f_pi (P2)

Scope: the stages `weak` and `running`, `chiral.chpt_mpi_from_rungs`, `links.pi0_width_from_rungs`
and `links.g_window_from_rungs`. Verified at commit 8cb2f5f by a separate verifier session.

### Runs

| Command | Result |
|---|---|
| `python3 rebuild/harness.py rebuild/builds/2026-11-b --mode verifier --ledger` | exit 0, `ALL GATES PASS`, 10 stages; weak oracle 2/2, running oracle 15/15, chiral 8/8, links 10/10; LEDGER.md unchanged (66 derived, 0 input, 8 quoted) |
| `... 2026-11-a --mode verifier --compare rebuild/builds/2026-11-b` | `crossbuild 25/25` |
| `python3 rebuild/chain_compare.py rebuild/builds/2026-11-b` | 22/22 overlaps agree |
| `pytest tests/test_rebuild_harness.py tests/test_chain_vs_rebuild.py tests/test_force_chain.py` | 51 passed |
| mutant: build a's `b_331` with b_X × 11/10 and × 9/10 (copies in the verifier's scratch directory) | builder gate for `running` **passes** (blind 4/4); verifier mode fails 7 and 9 oracle checks |

There is no oracle failure to triage. The findings below come from the third route and from
passes that are not independent evidence.

### Third route

Script: [`rebuild/verify/third_route_weak_running.py`](../../verify/third_route_weak_running.py)
(with `third_route_compare.py` beside it; `cleanroom.py` does not export that directory). It imports sympy, mpmath and `rebuild/inputs.py` only; nothing from
`src/` or the builds. What it does:

- **Width:** spin sum of |ū p̸(1−γ₅)v|² with sympy's Dirac matrices in the (+,−,−,−) metric (the
  builds use (−,+,+,+)), without the Dirac-equation shortcut, times the two-body phase space. The
  difference from G_F²V²f²m_l²m_π(1−m_l²/m_π²)²/8π simplifies to 0.
- **Coefficients:** C₂(G) from structure constants of explicit generators; Q_u, Q_d and every X
  solved in sympy from Q_e = −1, Q_u − Q_d = 1 and the [SU(3)_L]²U(1)_X anomaly; Tr X², Tr t_a t_a
  and the colour index summed over the full field list, in exact rationals.
- **Matching:** (1/g, β/g, 1/g_X) is a null vector of the 9×9 gauge mass matrix built from the three
  scalar triplets with a vev in every neutral component, so 1/e² = (1+β²)/g_L² + 1/g_X² and
  1/α_X = 1/α_Y − 1/(3α₂) for both variants.
- **Poles:** the closed form μ₀ exp(2π(1/α_X(μ₀) − 1)/b_X) at 40 digits, and an RK4 integration of
  dg/dt = b g³/16π² to g² = 4π (agrees to 3e-11 to 1e-9).

| Quantity | Third route | Build a | Build b | src | Rel. diff a / b / src |
|---|---|---|---|---|---|
| f_π (GeV) | 0.1305673867958 | 0.1305673867958 | 0.1305673867958 | 0.1305673868307 | 2e-16 / 2e-16 / 2.7e-10 |
| π⁰ → γγ width (eV) | 7.741747842662 | 7.741747842662 | 7.741747842662 | 7.741747838517 | 2e-16 / 2e-16 / 5.4e-10 |
| O(p⁴) m_π (GeV) | 0.1322937502541 | 0.1322937502541 | 0.1322937502541 | 0.1322937502204 | 2e-16 / 2e-16 / 2.6e-10 |
| (b_Y, b_2), Standard Model | (41/6, −19/6) | same | same | same | exact |
| b_X, β = −1/√3, N_c = 1, 3, 5, 7, 9 | 22/9, 26/3, 58/3, 310/9, 54 | same | same | same | exact |
| b_X, β = +1/√3, N_c = 1, 3, 5, 7, 9 | 46/9, 14, 82/3, 406/9, 202/3 | same | same | same | exact |
| b_L, N_c = 1, 3, 5, 7, 9 (both variants) | −59/6, −13/2, −1/2, 49/6, 39/2 | same | same | same | exact |
| b_colour, N_c = 1, 3, 5, 7, 9 | −11/3, −5, −25/3, −35/3, −15 | not exported | not exported | same | exact |
| 1/α_X(4 TeV), both variants | 83.73067915954 | 83.73067915954 | 83.73067915954 | (oracle's formula, same) | 2e-16 / 0 / n/a |
| pole, −1/√3, N_c = 3 (GeV) | 4.470102320411e29 | 4.470102320411e29 | 4.470102320411e29 | 4.470102323237e29 | 9e-15 / 5e-15 / 6.3e-10 |
| pole, −1/√3, N_c = 5 (GeV) | 1.900487709629e15 | 1.900487709629e15 | 1.900487709629e15 | 1.900487721366e15 | 5e-15 / 2e-15 / 6.2e-9 |
| pole, +1/√3, N_c = 3 (GeV) | 5.335458672202e19 | 5.335458672202e19 | 5.335458672202e19 | 5.335458698767e19 | 6e-15 / 1e-15 / 5.0e-9 |
| pole, +1/√3, N_c = 5 (GeV) | 7.265467765571e11 | 7.265467765571e11 | 7.265467765571e11 | 7.265467793774e11 | 4e-15 / 3e-16 / 3.9e-9 |
| pole, N_c = 1 and 7, both variants | 9.015e95, 1.4326e10; 5.900e47, 4.0402e8 | same to 7e-14 | same to 1e-14 | not run | |
| G window, −1/√3 (lo, hi) | (7.459646300603e-22, 4.126891334166e7) | same to 2e-14 | same to 9e-15 | (7.459646291e-22, 4.126891283e7) | src 1.3e-9, 1.2e-8 |
| G window, +1/√3 (lo, hi) | (0.05236120636051, 2.82374843825e14) | same to 1e-14 | same to 2e-15 | (0.0523612058391, 2.823748416e14) | src 1.0e-8, 7.8e-9 |

Closed forms found by the third route: b_X = (5N_c² + 8N_c + 9)/9 for β = −1/√3 and
(5N_c² + 20N_c + 21)/9 for β = +1/√3 (fitted at N_c = 1, 3, 5, 7; hold at 9 and 11);
b_L = −21/2 + N_c(N_c+1)/3. One-loop over quoted three-loop poles: 1.952 and 1.688 (−1/√3),
1.528 and 1.409 (+1/√3). M_Pl = 1.22089013e19 GeV.

### Findings (this addendum)

| # | Check | Class | Evidence | Action |
|---|---|---|---|---|
| X-N1 | oracle "f_pi from G_F and pi -> mu nu" (rtol 1e-8), and through it the π⁰ width and O(p⁴) mass | **N** | Build and third route agree to 2e-16; `src/ladder_links.py:338` differs by 2.7e-10 because it types ħ = 6.582119569e-25 GeV s, while the build forms `HBAR/E_CH` from the 10-digit CODATA ħ. The exact SI value is 6.58211956951e-25, 3.1e-10 above the build's and 3.9e-11 above src's. The effect is 5.4e-10 on the width and 2.6e-10 on the mass. | None. Tolerances 1e-8 and 1e-5 are adequate. |
| X-N2 | oracle "one-loop pole equals src's one-loop running" (rtol 1e-6) and "G window from the one-loop poles" (1e-5) | **N** (the reference is the less precise side) | src integrates dg/dt numerically (`solve_ivp`, rtol 1e-9) and is 6e-10 to 6.2e-9 above the closed form; the builds match the 40-digit closed form to 7e-14 or better. | None needed. The oracle could compare with the closed form at 1e-12. |
| X-C1 | SPEC §9 singlet counting ("one per copy of the multiplet", fixed in de2fce7 after both builders chose it) | **C**, closed; **not** a shared mistake | The reading is forced by gauge-anomaly cancellation. With it, X³, grav²X, [SU(3)_L]²X, [SU(N_c)]²X, [SU(3)_L]³ and [SU(N_c)]³ all vanish for N_c = 1…9, both variants. Colourless singlets give b_X = 50/9 (−) and 94/9 (+) at N_c = 3 and leave X³, grav²X, [SU(N_c)]²X and [SU(N_c)]³ non-zero. Singlets not repeated per family give 6 and 28/3 and are also anomalous. src's `m331_exact.MODELS` has the same content. Neutral singlets carry X = 0, so "neutral components have none" cannot change any b. | None. SPEC could add the reason: "this is the counting for which the gauge anomalies cancel". |
| X-C2 | SPEC §9 "the Standard Model below the 3-3-1 scale is the 3-colour one for every N_c" (same commit) | **C** (convention; build, reference and SPEC agree) | It is a choice about a counterfactual. If the N_c = 5 pole were instead matched from a 5-colour, 5-generation Standard Model with the same M_Z boundary (b_Y = 85/6, b_2 = 17/6), it would be 6.70e14 GeV instead of 1.90e15 (−1/√3) and 3.47e11 instead of 7.27e11 (+1/√3). The N_c = 3 selection is unchanged. | None. The reading is stated in SPEC; quote the N_c = 5 poles as holding under it. |
| X-C3 | `landau_pole`: "α_X = 1" and the N_c = 3 selection | **C** (SPEC-fixed criterion; a result that is true but narrow for +1/√3) | The scale where 1/α_X = 0 is 2.06×, 1.38× (−1/√3) and 1.57×, 1.26× (+1/√3) higher; the selection survives. For +1/√3 the one-loop N_c = 3 pole is only 4.37 × M_Pl (2.86 × at three loops): a b_X 4.1% larger (14.58 instead of 14) puts it at M_Pl. For −1/√3 the margin is 68% in b_X. | Owner: wherever the one-loop N_c = 3 selection is quoted for +1/√3, state the margin. |
| X-C4 | blind check "one-loop coefficients exact; b_X > 0 and grows with N_c" | **C** (test gap; the oracle covers it) | b_X scaled by 11/10 or 9/10 passes the whole builder gate for `running`: the blind tier tests only type, sign and monotonicity, and the pole check uses the build's own b_X. Verifier mode catches both (exact comparison with src's content, poles, and for × 11/10 the +1/√3 selection). | Auditor: add a blind check that fixes the value without stating it, e.g. b_X + β²(b_L + 11) equals the hypercharge sum (2/3)ΣY² + (1/3)ΣY² over the same content with Y = Q − T₃ from rung 1; and keep a b_X-scaling mutant in `tests/test_rebuild_harness.py`. |
| X-C5 | f_π: the radiative correction, and the digits quoted | **C** (SPEC-fixed route; all three agree) | SPEC §10, both builds and src use Γ_measured = Γ_tree(1 + 0.0176) with the same G_F, V_ud, masses and width, so the oracle pass confirms the formula and inversion, not the correction. Without the correction f_π would be 131.711 MeV (+0.876%). The inputs' errors (δ ± 0.0021, V_ud ± 0.00032) give ±0.135 and ±0.043 MeV, so 130.5674 MeV is reproducible to 2.7e-10 but physically 130.57 ± 0.14 MeV; likewise the π⁰ width is 7.742 ± 0.017 eV. src returns this error; the builds' export does not. | None for the builds. Quote f_π with its error where it is used as a physical result. |

### Independence of the two builds on the new stages

- **Same SPEC-fixed route:** the master formula for b, the field content and singlet counting, the
  matching 1/α_X = 1/α_Y − β²/α₂ (both solve rung 1's `inv_e2`, which hard-codes the closed form, as
  noted earlier), the closed-form pole, the V−A amplitude with the Dirac-equation reduction, the
  trace, and the inversion by f² scaling. f_π is bit-identical in a and b for that reason. The
  three `_from_rungs` exports are compositions of existing exports.
- **Independent:** the code that enumerates the content (a: per-triplet loop with a closed-form
  check in N_c; b: a field list, a closed form and the anomaly sums); the antitriplet-X solve; the
  second routes (a: explicit 4×4 trace and Gaussian-smeared phase space, bisection for the pole;
  b: explicit spinors and a numerical phase-space integral, RK4 in α, log-form window edges).
- The third route above is independent of both and of src in all of these.

### Answers asked of this verification

- **Could a b_X wrong by about 10% pass?** The blind tier: yes (X-C4, shown by mutants). The
  oracle: no; it compares b_331 exactly for N_c = 1, 3, 5, 7 against src's field content, and the
  third route confirms that content exactly.
- **Is the shared singlet-counting reading correct?** Yes, physically: it is the anomaly-free one
  (X-C1). It was a SPEC gap (class C), now closed, not a shared mistake.
- **ACCEPTED.md addendum numbers:** all confirmed. f_π = 130.5674 MeV (130.56739); src to 2.7e-10
  ("3e-10" is right as a rounding); π⁰ width 7.7417 eV (7.78550 with the lattice input); O(p⁴) mass
  132.29 MeV (132.294; 132.649 with the lattice input); poles 5.335e19 and 7.265e11 GeV (+1/√3),
  4.470e29 and 1.900e15 GeV (−1/√3); ratios to three loops 1.41 to 1.95. Not wrong, but stated
  without qualification: the digits of f_π (X-C5) and the +1/√3 selection margin (X-C3).

### Not verified here

- The PDG text behind `GAMMA_PI_MUNU`, `DELTA_PI` and `V_UD` (values taken from `rebuild/inputs.py`;
  no network access was used). The verifier's recollection that PDG quotes f_π|V_ud| ≈ 127.13 MeV
  matches the third route's 127.130 MeV but was not checked against the source.
- The quoted three-loop `POLES_331` were not recomputed; only the ratios to them.
- No comparison with published 3-3-1 β coefficients; the check is the explicit trace computation.

### Updated class counts

This addendum: B 0, R 0, C 5, N 2.

| | B | R | C | N |
|---|---|---|---|---|
| Earlier stages | 0 | 0 | 7 | 7 |
| This addendum | 0 | 0 | 5 | 2 |
| **Total** | **0** | **0** | **12** | **9** |

No class R finding: on every quantity of the extension the reference agrees with the third route
exactly (coefficients) or to 6.2e-9 or better (numbers), and where it differs it is the less
precise side (X-N2). No class B finding, so there is no feedback to the builders.
