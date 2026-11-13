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
