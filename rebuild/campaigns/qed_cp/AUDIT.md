# AUDIT: campaign qed_cp (Casimir–Polder by fourth-order perturbation theory), builds a and b

Auditor (red team). I edited nothing in the repository or in the builds. Every script below lives in this directory
and ran on copies of the builds (`copies/a`, `copies/b`) with bytecode writing off, so the builds' own
`gate_report.json` and `__pycache__` were not touched.

Paths: SPEC/campaign/oracle in `/home/user/STUR-Physics-Lab/rebuild/campaigns/qed_cp/`;
build a = `.../room-qed_cp-a/builds/qed_cp-a/`; build b = `.../room-qed_cp-b/builds/qed_cp-b/` (scratchpad).

## 0. What I verified independently (not just re-ran)

| Item | How | Result |
|---|---|---|
| 12 time orderings and their energy-denominator sum Σ₁₂ | my own enumeration: all 4! orderings of {A_k, A_q, B_k, B_q}, halved for the k↔q relabelling (`check_identities.py`, `check_numerics.py`) | equals build a's `_sigma12_symbolic` exactly (sympy), equals a's closed form (DERIVATION a §3, general a≠b) exactly, equals the k↔q-symmetrised version of build b's `_diagram_sum` to 4e-16 (b's own S is deliberately not symmetric; it relies on the symmetric numerator, which is valid) |
| a's identity (2) Σ₁₂ = (8/π)∫du ab·kq/[(a²+u²)(b²+u²)(k²+u²)(q²+u²)] | my mpmath quadrature at 5 random (a,b,k,q) spread over 4 decades; also re-ran a's `_check_identity` | relative error ≤ 3e-29; a's symbolic residual is exactly 0 |
| angular average τ_ij (a: P, P+Q; b: B, A) | direct θ-quadrature of both the transverse (xx) and longitudinal (zz) components at x = 0.7, 2.3, 9.1 (`check_b_and_tau.py`) | 10 digits, both builds. (Build a's own `__main__` checks only the zz component.) |
| mode-sum prefactor (2πk/V)·V/(2π)³·4πk² = k³/π, overall sign −d⁴/π² | by hand | correct in both |
| b's hand-transcribed S decomposition (`qed_cp.py` b:76–78) against its own sympy enumeration | numerically at 3 points | exact |
| final U(r) | a vs b vs a high-precision (mpmath) evaluation of the oracle's integral, ρ = rω₀ from 1e-6 to 1e8 (`check_numerics.py`, `check_far.py`) | a/b agree to ≤ 4e-16 for 1e-4 ≤ ρ ≤ 1e4; both agree with the careful reference to ~1e-15 |
| the ε→0 regularisation | §4 below (`regulators.py`, `regulators2.py`) | three different smooth regulators give the same limit; a sharp cut-off has none |

Conclusion of §0: the physics in both builds is right, and the chain RS → 12 diagrams → eq.(1) → (a: identity (2) →
eq.(3)) / (b: Laplace trick → E₁ functions → s-integral) checks out step by step. The findings below concern
provenance wording, the independence claim, and above all how weak the gate is.

## 1. Provenance honesty

Neither build has a lookup table, caching, a lint-dodging constant, or an argument-dependent branch that changes the
mathematics. a's `ρ ≥ 1` switch (a `qed_cp.py:39–51`) and b's r-dependent breakpoints (b:79) only change the
quadrature, and the two forms agree to 1e-14 at ρ = 1. C and D come from the derived polynomial / Laplace transforms,
never typed in (a:59–67, b:98–111). Specific points:

* **a, `cp_energy` (a:54–56, PROVENANCE a:71).** The code that runs is exactly the one-dimensional integral (3).
  It is literally the oracle's Green-tensor formula: (1/π)e^{−2x}p(x) = (1/2π)·Tr G·G·r⁶, with the same p. The
  12-diagram enumeration and identity (2) live only in `_sigma12_symbolic` / `_check_identity` (a:80–104), which only
  `__main__` calls. So the note "4th-order RS over 12 … diagrams" describes the derivation, not anything the code
  computes. The hand-typed parts of the runtime path are the prefactor −1/π and α(iu)²/α₀² = (1+t²)⁻². Everything
  else in p(x) is derived symbolically from M = (π/2)(−∇²δ+∂∂)e^{−ur}/r (a:16–26). I re-derived both typed parts and
  they are correct. **Medium:** to the gate, build a is byte-for-byte indistinguishable from mutant M1 (the banned
  formula typed in). Only a reader of DERIVATION + `__main__` can tell them apart.
* **b, `cp_energy` (b:68–87, PROVENANCE b:8).** The diagram enumeration is not on the runtime path either: the
  decomposition f1 = 2k/(a(a+k)²), f2 = 6/(a+k)², f4 = 4a/(a+k)² is hand-transcribed into `_u` (b:77–78). I checked the
  transcription and it is exact. **Low.**
* **b, `near_coefficient`/`far_coefficient` notes** match the code (sympy Abel limit and Laplace transforms). The limits
  S → 2/(akq) and S → 4/(a²(k+q)) are taken by hand in DERIVATION b §3, not in code. They are correct. **Low.**
* **a, `near_coefficient` note** "cross-checked by London route": the London route exists only in `__main__` (a:136–139). It is accurate as a note. **Info.**

### The "fit" of identity (2) in build a (SPEC §2)

The right-hand side of (2), an α(iu)-shaped product with the prefactor 8/π, was **posited and then verified**. It was
not constructed from Σ₁₂. DERIVATION a §3 calls it "derived", but no step shows how the form or the 8/π was found.
It is the classic Casimir–Polder / Craig–Thirunamachandran denominator identity, so it was most likely recalled from
the literature (or guessed with the target formula in mind), not discovered.

The verification is still a complete proof, and I checked it two ways. First, the sum of upper-half-plane residues
equals Σ₁₂ identically in (a, b, k, q), and a's own check gives residual 0. Second, my quadrature at random points
agrees to 1e-29. The normalisation 8/π is fixed by that exact algebra, not by any comparison with the answer. The
identity is a statement about the 12 time-ordered denominators only. It contains no field propagator, so using it
does not assume the Green-tensor formula, and SPEC §2's ban is honoured in substance.

What a then does in §4 is to *derive* the imaginary-frequency Green tensor, (u²δ+∂∂)e^{−ur}/r, as the Fourier
transform of the mode sum. That is exactly the content the campaign wanted re-derived. **Finding (low, wording):**
"derived" should read "posited, then proved by residues (literature identity)".

## 2. Derivation vs code mismatches

Build a:
1. DERIVATION a §3 (line 65) says identity (2) was checked "numerically at random points". No such code exists; only
   the symbolic residue check (a:98–104) does. Low. (I did the numerical check myself: it holds.)
2. DERIVATION a §6(d) (line 111) says "quad with tightened tolerances / alternative variable agree to ~1e-12". The code
   (a:152–154) only compares the t-form with the s-form at ρ = 1, so there is no tolerance-refinement study. SPEC §4
   asks for one. Low.
3. Numerical defect outside the gate's range: the t-form (a:45–51) returns J/(3π/4) = 0.99958 for ρ ≤ 1e-8 (with a
   QUADPACK roundoff warning). The near-zone result is wrong there by 4e-4. It is correct (2e-13) at ρ = 1e-6. Low.
4. DERIVATION a §6(b) claims the direct double integral at ρ = 2 agrees to 3e-4. `__main__` does compute it
   (a:146–150); see the addendum for my rerun.
5. Everything else matches: (1) ↔ `_U_double` (a:107–126), Σ₁₂ ↔ `_sigma12_symbolic`, p(x) ↔ `_p_coeffs`, the
   limits ↔ `far_/near_coefficient`.

Build b:
1. DERIVATION b §4(ii) (line 56) says "Gaussian-damped e^{−eps(k+q)}". The damping is exponential (Abel), not
   Gaussian. Low (wording).
2. DERIVATION b line 57–58 claims the result is "justified by the result being independent of eps-shape". The code
   only ever uses exponential damping, so nothing in b supports that claim. My §4 test does: it holds. Low–medium.
3. DERIVATION b §1 line 21: "E4 = sum V V V /(…)" has a V missing (typo). Low.
4. Fixed 45-digit precision (b:13) loses accuracy at very large ρ because of the 1/r³ cancellations: 1e-8 relative at
   ρ = 1e6 and 3e-6 at 1e8. Fine inside the gate's range. Low.
5. Second route: `_brute` with second Richardson at ρ = 1 gives −0.651534 vs main −0.651266 (4e-4). That is a weak but
   genuine check of the Abel definition (my rerun of b `__main__`).

## 3. Independence

* **Methods.** Up to eq.(1), the routes are the same textbook set-up: the same 12 orderings, the same numerator
  d⁴k³q³Tr[τ(kr)τ(qr)]/π², the same τ and the same Abel prescription. They differ only in the reduction of the
  double integral:
  * a uses a contour/residue identity and lands on imaginary frequency, then does a 1-D QUADPACK integral.
  * b uses 1/(k+q) = ∫ds e^{−(k+q)s} (a real Laplace / "imaginary-time" variable), with closed-form one-photon
    integrals in E₁ of the complex argument s − ir at 45 digits, then a tanh-sinh s-integral.

  These are genuinely different reductions and different numerics. So the 4e-16 agreement proves that **the two
  reductions of eq.(1) are equivalent and both converged**. It proves nothing about eq.(1) itself, because that is
  shared. I checked the shared upstream separately (§0), and the oracle (a different, linear-response route from the
  literature) also tests it. Caveat: the 4e-16 agreement says the two *programs* are correct implementations. Only the
  oracle and my §0 checks speak to whether eq.(1) is the right physics.
* **Build a vs the oracle is not independent at the last step.** a's runtime formula *is* the oracle formula. Their
  agreement (0.0000 %) tests a's quadrature, plus the claim that a's derivation ends at the literature formula. It is
  not a numerical cross-check. The independent evidence for a is the derivation itself (verified here) and a's §6(b)
  direct integral.
* **Could either builder have seen the other's or the oracle's formula?** The clean rooms are not isolated:
  * Both rooms sit in the same scratchpad, on the same filesystem as the repository.
  * The repository's `src/casimir_diamonds.py:18–23` contains Tr G·G = 2e^{−2u}(3+6u+5u²+2u³+u⁴)/r⁶ and 23/4 verbatim.
  * Timestamps: b's DERIVATION and code were written at 23:25–23:26. a first imported campaign.py at 23:30 and wrote
    its files at 23:40. So b's build was readable throughout a's work.

  I found no trace of copying. a's route is not b's, and a's p(x) is computed, not typed. But "blind" rests on agent
  compliance, not on enforcement. **Medium (process).**

## 4. The Abel limit and the exchange of integration order

* **What is conditionally convergent.** k³τ(kr)·S grows like k·sin kr, so eq.(1) does not converge as a Lebesgue
  integral. For any ε > 0, a product regulator φ(εk)φ(εq) with φ decaying makes every integral absolutely
  convergent. Fubini then justifies every exchange (identity (2) ↔ k, q in a; s ↔ k, q in b). The only non-trivial
  step is ε → 0 at fixed r > 0, taken inside the u- (or s-) integral.
* **Test (`regulators2.py`).** U_ε for three regulators, reduced exactly with identity (2):
  * Abel e^{−εk}: the builds' choice.
  * Gaussian e^{−ε²k²}.
  * A hydrogen-like dipole form factor (1+ε²k²)⁻⁴: the physically motivated one, since finite atomic size is what
    really regulates the dipole approximation.

  | ρ = rω₀ | regulator | U_ε/U−1 at ε = 0.08, 0.04, 0.02, 0.01 |
  |---|---|---|
  | 1 | Abel | −2.5e−1, −1.3e−1, −6.6e−2, −3.3e−2 (linear in ε) |
  | 1 | Gauss | +5.6e−3, +1.4e−3, +3.5e−4, +8.6e−5 (∝ ε²) |
  | 1 | form factor | −7.2e−3, +5.6e−3, +1.4e−3, +3.5e−4 (∝ ε²) |
  | 5 | Abel / Gauss / f.f. | −5.9e−3 / +1.6e−5 / +6.3e−5 at ε = 0.01 |
  | 0.1 | Gauss | −5.5e−2 → +1.8e−4 at ε = 0.02 → 0.01 (needs ε ≪ r) |

  All three tend to the builds' U. The approach is O(ε/r) for Abel and O(ε²/r²) for the even regulators.
* **Sharp cut-off.** Even the near-zone one-photon integral ∫₀^Λ x²A(x)dx has no limit: it oscillates as
  π − 2cos Λ (values 1.14π, 0.44π, 0.39π, 1.18π at Λ ≈ 100, 1000, 1001, 3000). So "a physically different
  regularisation" can change the answer only by being non-smooth, and a sharp cut-off is not physical: real atoms
  have smooth form factors.
* **Justification.** For r > 0 the one-photon integrals are Fourier transforms of functions with polynomial growth
  and an asymptotic expansion in 1/k. Their regulated values converge to the same distributional limit for every
  regulator with φ(0) = 1 that is smooth and rapidly decaying. Corrections are O((ε/r)^n), which for a real atom
  means O(a_Bohr/r): beyond the dipole approximation and outside the model.

  Contact (δ⊥) terms contribute only at r = 0. The r-independent fourth-order and renormalisation terms carry no
  e^{ik·r} phase. Neither build proves dominated convergence for exchanging ε → 0 with the outer integral, but the
  numerics above and the two builds' direct double integrals (a: 3e-4, b: 4e-4) confirm it.

  **Verdict: justified at the level of rigor appropriate here. Low.**

## 5. Weak checks and mutants

Mutants are in `mutants/<name>/qed_cp.py`. Each was run with
`python3 gate.py <dir> --mode verifier --campaign …/qed_cp --oracle …/qed_cp/oracle.py`; the output is in
`mutants/<name>/gate_stdout.txt`.

| Mutant | What is wrong | Gate (verifier + oracle) |
|---|---|---|
| **M1 banned_route** | the Green-tensor / imaginary-frequency formula typed in; `return 23/(4*math.pi)`, `return 3/4`; PROVENANCE "derived" | **PASSES (23/23)** |
| **M2 asymptotic_switch** | exact core, but pure −Cα₀²/r⁷ for ρ > 20 and pure London for ρ < 0.05. Error 1.3 % at ρ = 20.5, 0.6 % at 30, 7e-4 at 0.049 | **PASSES** |
| M3 two_pole_alpha | wrong atom: a two-pole α(iu) with the same α₀ and the same London coefficient (0.3–1 % crossover error) | killed by oracle crossover at ρ = 0.5, 1, 3, 20 |
| **M4 systematic_1e-4** | U off by 1.5e-4 everywhere, C and D by 0.9e-4 (an under-converged ε-extrapolation like a's own §6b) | **PASSES** |
| **M5 probe_fitted_trace** | wrong polarisation trace p(x): extra x²…x⁸ terms with p(0) and the far moment unchanged. Error 1.0 % peaking at ρ ≈ 5.6, ~1e-13 at the five oracle points | **PASSES** (a 2 % version is killed by the monotonicity check) |
| **M6 alpha_w0_cubed** | spurious dependence on the second dimensionless group α₀ω₀³: U × (1 + 0.3(x−1)(x−3)) | **PASSES** (wrong by any amount wherever α₀ω₀³ ∉ {1, 3}) |

Per check, a wrong implementation that survives it:
* `b_negative` (campaign.py:16): any attractive function. M2–M6 all survive it.
* `b_alpha_squared` (:21): a single point at ω₀ = 1, so M6 survives.
* `b_dimensions` (:26): one λ at one point. It only enforces dimensional homogeneity. By dimensional analysis
  U = α₀²ω₀⁷F(rω₀, α₀ω₀³), so the dependence on α₀ω₀³ is unconstrained, and M6 survives.
* `b_slopes` (:37): the slope tolerance is ±0.1, so anything with U ∝ r^{−6±0.1} at ρ = 1e-2 survives (M2, M3, M5).
* `b_limits_agree` (:43): only self-consistency at 2e-3. M2 passes trivially, M4 too.
* `b_crossover_monotone` (:52): kills large-amplitude M5 but not 1 %.
* Oracle coefficients at 1e-4 (oracle.py:23–24): M4 survives with 0.9e-4.
* Oracle crossover (oracle.py:26): 5 fixed points, all at ω₀ = α₀ = 1, tolerance 2e-4. M2, M4, M5 and M6 survive.
  There is no probe between 3 and 20 or between 20 and the far-limit check at 1e4.
* Nothing in the gate can detect M1. The lint (gate.py:67–72) inspects only float literals with ≥ 3 significant
  digits within 1 % of LINT_TARGETS. The integer expressions 23/(4π) and 3/4 pass, and 0.75 is not even a lint target.

Proposed new checks, implemented in `proposed_checks.py` (output in `proposed_checks_output.txt`). Builds a and b
**pass all five**.

| Check | Kind | Kills |
|---|---|---|
| `B_far_approach`: (1 − Ur⁷/C) > 0 and scales as ρ⁻² (ratio of the deficits at ρ = 100, 200 is 4 ± 0.1) | blind (no target value) | M2, M4 |
| `B_near_approach`: (1 − Ur⁶/(Dω₀)) > 0 and scales as ρ² at ρ = 0.01, 0.02 | blind | M2, M4, M5 |
| `B_alpha_everywhere`: U/α₀² independent of α₀ at ω₀ = 0.37, r = 5.1 for α₀ = 0.1, 2, 7 | blind | M6 |
| `O_dense`: 12 log-random ρ ∈ [1e-2, 1e3], random ω₀, α₀ ∈ [0.1, 10], tolerance 1e-6, against a **fixed** reference | oracle | M2, M3, M4, M5, M6 |
| `O_coeff_tight`: C, D to 1e-8 | oracle | M4 |

Notes on these checks:
* The near ratio is 3.94 because the next term is ρ³ log ρ. Use ρ = 0.005 and 0.01 for more margin.
* `O_dense` should get a fresh seed each verifier run, so the probe points cannot be fitted the way M5 fits the
  current five.

For **M1** no numerical check is possible, because the banned formula is the right answer. My proposal:
1. Add exports for intermediate objects that the gate checks against its own brute force:
   * `diagram_sum(k, q, wA, wB)` against the gate's own enumeration of time orderings;
   * `regulated_double_integral(r, w0, eps)` (eq.(1) with e^{−ε(k+q)} at finite ε, e.g. ε r = 0.2) against a 2-D
     quadrature in the gate. U_ε at finite ε is not given by the Green-tensor formula, so a copied formula cannot
     produce it.
2. Keep the auditor's reading of DERIVATION as the real defence.
3. Add `3/4`, `0.75` and the integer patterns `23/(4*pi)` / `23/4` to the lint (an AST check for BinOp of int literals).

### Oracle bug found (class R)

`oracle.reference` (oracle.py:13–15) uses `quad` on [0, ∞) with no breakpoints and the decay scale 1/r. It loses
accuracy for ρ beyond ~30: −4.4e-5 at ρ = 50, +6.9e-3 at 200, −9 % at 1e3, garbage (×1e12) at 1e4, and 0 beyond.
The current probes (≤ 20) are unaffected, but the reference cannot be used to extend the crossover check. The fix is
the variable s = ξr with breakpoints, or mpmath, as in `proposed_checks.ref`. **Medium.**

## 6. Findings by severity

**High**
* H1 (gate/process, not the builds): the gate cannot enforce SPEC §2. M1, the banned Green-tensor formula with
  copied closed forms, passes every tier, and build a's runtime code is that formula. For builds a and b this
  finding is **closed by this audit**: I verified each step of both derivation chains independently (§0, §1).
  It stays open for any future build until the intermediate-object checks of §5 exist.

**Medium**
* M-1: four surviving numerical mutants (M2, M4, M5, M6) show that the blind and oracle tiers probe too few points,
  only at ω₀ = α₀ = 1, with loose tolerances. Per README P4, each becomes a new check (§5 table).
* M-2: `oracle.reference` is inaccurate for ρ ≳ 30 (class R).
* M-3: the clean rooms are not isolated from each other or from the repository (which holds the target formula). b
  was complete before a started. There is no evidence of leakage, but the independence is not enforced.
* M-4: a's PROVENANCE "derived via 12 diagrams" describes the derivation, not the runtime code. The runtime code is
  the Green-tensor formula.
* L-M: b's claim of "independent of eps-shape" was never tested in b (I tested it: true).

**Low**
* a: identity (2) described as "derived" when it was posited and proved. DERIVATION claims checks that the code does
  not contain: "numerically at random points" and "tightened tolerances". The near zone is wrong by 4e-4 for
  ρ ≤ 1e-8.
* b: "Gaussian" for exponential damping; a typo in the E4 formula; precision loss at ρ ≥ 1e6; the S decomposition is
  hand-transcribed into `_u`.
* The Abel step is not proved to the level of dominated convergence, but it is justified physically and confirmed
  numerically for three regulators.

## 7. Verdict

**ACCEPT** both builds as correct, independently derived implementations of the fourth-order Casimir–Polder result:
* U(r) at all separations;
* C = 23/(4π);
* D = 3/4.

There is no open high-severity finding against either build: H1 is a gate weakness that I closed for these two
builds by checking their derivations by hand and with independent code.

The acceptance is **conditional on the README P4 follow-up** before the gate is trusted for anything else:
* add the five checks in `proposed_checks.py` (fresh seed for `O_dense`);
* fix `oracle.reference` for large ρ;
* add the intermediate-object exports (or an equivalent manual-audit requirement) that would kill M1;
* correct the wording issues in both DERIVATION files.

## Addendum: rerun of the builds' own second routes (on copies)

See `b_main_output.txt` and `a_main_output.txt`.

* **Build a.** The identity residual is 0, the count is 12 and p = [3, 6, 5, 2, 1]. The London D = 0.75 and the
  s-form and t-form J(1) agree to 14 digits. The direct eq.(1), extrapolated in ε at ρ = 2, gives −8.279308e−3 against
  eq.(3)'s −8.276692e−3, a difference of 3.2e−4. This reproduces DERIVATION a §6(b) exactly.
* **Build b.** S has 12 diagrams. The u values are unchanged at doubled precision. The 2-D brute force with second
  Richardson gives −0.651534 at ρ = 1 against the main route's −0.651266, a difference of 4.1e−4.
* Both direct routes are independent of the reduction steps (identity (2) in a, the Laplace trick in b). They confirm
  the Abel-defined eq.(1) only at the 3–4e−4 level. My `regulators2.py` confirms it at ≲1e−4 for three regulators.
* After my runs the builds' `qed_cp.py` md5 sums are unchanged (a 81f9fe8f…, b d9b2c08a…), and no files were added
  to the build directories.
