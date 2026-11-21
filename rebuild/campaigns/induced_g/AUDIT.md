# Red-team audit: induced_g (Sakharov's one-loop 1/G, proper-time cutoff)

In the repository I wrote only this file and `audit_proposed_checks.py`. All scratch work is in
`S = /tmp/claude-0/-home-user-STUR-Physics-Lab/56536ebd-3031-5fab-abbd-ab2797e8167a/scratchpad/audit-ig`:
* `casimir_esu.py` / `casimir_esu.log`: the independent sign route (§1);
* `regulator_dependence.py` / `regulator_dependence.log`: the same mode sums with energy cutoffs (§1d);
* `make_mutants.py`, `mutants/<name>/` (each holds `induced_g.py`, a copy of build a's `DERIVATION.md`, `DESCRIPTION.txt`,
  `gate_builder.txt`, `gate_verifier.txt`, `proposed_out.txt`), `run_gates.sh`, `gates.log`, `proposed.log` (§3);
* `copies/{a,b}`: the builds were gated from copies, because the gate writes `gate_report.json` into the build directory;
* `checks_a.log`, `checks_b.log`: the proposed checks on both builds.

Nothing was written into `builds/`, `oracle.py`, `campaign.py` or `SPEC.md`.

Class labels follow `../README.md` / `../PROTOCOL.md`: **B** = builder bug, **R** = reference or oracle bug (here: coverage
gaps; no oracle value is wrong), **C** = SPEC issue, **N** = numerical. (The nucleon_pol audit used a different lettering; this one
follows the campaign README.)

## 0. Verdict

* **The result is established within the SPEC:**

  1/G = (κ²/2π) [ n_s (1/6 − ξ) + n_w/6 − 2 n_v/3 ]  (d = 4),

  with k₁ = 1/6 − ξ (scalar), −2^⌊d/2⌋/12 (Dirac), half of that for Weyl, (d − 6)/6 (vector without ghosts) and (d − 8)/6
  (vector with its two ghosts).
* **Independent sign.** My route uses the canonical zero-point energy on the Einstein static universe R × S³ (§1). It uses no b₁
  formula, no determinants for statistics, and no ghosts: transverse photons only, and the Dirac sea for fermions. It gives the same
  three numbers, +1/6 for a minimal scalar, +1/6 for a Weyl fermion and −2/3 for a gauge vector, analytically and to 10⁻⁹ numerically.
* **The claim "minimally coupled scalars and fermions induce positive G, gauge vectors negative" is right in the SPEC's
  conventions.** That is W = −ln Z, S_grav = −(1/16πG)∫√g R with R > 0 on spheres, and the proper-time cutoff.
* **The sign is a property of the regulator, not of the fields alone.** The relative weights 1 : 1 : −4 (scalar : Weyl : vector) are
  universal for a common regulator. The overall sign is not: with a positive energy cutoff on the same mode sums, every sign flips
  (§1d, C2).
* **Both builds are correct. Neither has a code defect.** There are two documentation findings (B1, B2).
* **Mutants.** 30 mutants of build a: 28 wrong, 1 equivalent (M23), and 1 that types in the correct closed form (M28).
  * The original gate kills 20 of the 28 wrong ones. The builder tier alone kills 5.
  * **8 wrong mutants survive both gates** (M07, M13, M14, M15, M19, M20, M21, M26). All 8 die on the new checks in
    `audit_proposed_checks.py`, and so do the 20 that the gate kills.
  * M28 dies only on a heuristic check. Both real builds pass all 7 new checks.

## 1. Independent derivation of the sign: zero-point energy on R × S³ (task 1)

### (a) Route

**Geometry.** S¹_β × S³_a with β → ∞. This is a different manifold from the builds' S⁴: a product, not Einstein, with
Ric = diag(0, 2/a², 2/a², 2/a²) and R = 6/a² > 0. Then:
* ∫√g R = β · 2π²a³ · 6/a² = 12π²βa;
* S_grav = −(3π/4) βa/G.

**Effective action.** As β → ∞, Z → e^{−βE₀}, so W = −ln Z = βE₀(a), with E₀ the vacuum (zero-point) energy. Matching the
term linear in a gives

  **1/G = −(4/3π) × [coefficient of a in E₀]**.

A positive 1/G therefore means that the vacuum energy has a *negative* κ²a term.

**The SPEC regulator, reduced to modes.**
* On S¹ × S³: Tr e^{−tD} = β (4πt)^{−1/2} Σ_modes e^{−tω²}, where the ω² are the spatial eigenvalues of D.
* So the SPEC's boson rule W = −½∫_{1/κ²}^∞ (dt/t) Tr e^{−tD} becomes E₀ = Σ f(ω), with

  f(ω) = −(1/4√π) ∫_{1/κ²}^∞ dt t^{−3/2} e^{−tω²} = −κ/(2√π) + ω/2 + O(ω²/κ).

  This is the canonical +ω/2 per bosonic mode, which checks the SPEC's boson determinant sign against the Hamiltonian.
* A fermion has f → −f, which is −ω/2 per mode (the Dirac sea). That is the SPEC's Z = det D̸ again.

**Field content: the canonical physical modes, with no ghosts and no Lichnerowicz or Weitzenböck formula.**

| Field | Frequency ω | Number of modes |
|---|---|---|
| Scalar, −∇² + ξR | ω² = [l(l+2) + 6ξ]/a² | (l+1)², l ≥ 0 |
| Weyl fermion | ω = (n + 3/2)/a | 2(n+1)(n+2): particles and antiparticles, one helicity, from the S³ Dirac spectrum ±(n+3/2)/a with degeneracy (n+1)(n+2) per sign |
| Maxwell field in Coulomb gauge | ω = (n+1)/a | 2n(n+2), n ≥ 1: transverse (coexact) photons only, with n = 1 the 6 Killing vectors of S³ |

### (b) Analytic evaluation

Use s = t/a². For even summands, the Poisson / Euler–Maclaurin sums are exact up to e^{−π²/s}:

Σ_{ν≥1} ν² e^{−sν²} = √π/(4s^{3/2}),  Σ_{ν≥1} e^{−sν²} = √π/(2√s) − ½,  Σ_{ν∈ℕ+½} e^{−sν²} = √π/(2√s).

The s^{−1/2} = a t^{−1/2} term gives ∫_{1/κ²}^∞ dt t^{−2} = κ², so it is the κ²a term.

| Field | Mode sum (s^{−1/2} part) | κ²a term of E₀ | 1/G per κ² | K = 2π/(Gκ²) |
|---|---|---|---|---|
| scalar | Σ ν² e^{−s(ν²−1+6ξ)} → (1−6ξ)√π/4 | −(1−6ξ)/16 | (1−6ξ)/(12π) | **1/6 − ξ** |
| Weyl | −Σ_{ν∈ℕ+½} 2(ν²−¼) e^{−sν²} → +√π/4 (with the fermion sign) | −1/16 | 1/(12π) | **+1/6** |
| photon | Σ_{ν≥1} 2(ν²−1) e^{−sν²} → −√π | +1/4 | −1/(3π) | **−2/3** |

For the photon, the constant +1 of the sum gives an a-independent κ¹ term (a missing zero mode). It does not touch κ²a.

### (c) Numerical check (`casimir_esu.py`)

I summed the exact mode sums with the closed-form f(ω) = −(ω/2√π)[e^{−x}/√x − √π erfc √x], x = ω²/κ², then fitted in two ways.

**Fit in κ at a = 1**, with basis κ⁴, κ², κ, ln κ, 1, κ⁻², κ⁻⁴:

| Field | K from E₀ | Reference |
|---|---|---|
| scalar, ξ = 0 | +0.1666666665 | 1/6 |
| scalar, ξ = 0.4 | −0.2333333337 | 1/6 − 0.4 |
| scalar, ξ = 1 | −0.83333341 | 1/6 − 1 |
| Weyl | +0.1666666665 | 1/6 |
| photon | −0.6666666664 | −2/3 |

**Fit in a at κ = 30.** The a¹ coefficients give K = +0.16666668, +0.16666665 and −0.66666665.

**Agreement with the builds.** Each value equals the builds' `inv_G` per species to 10⁻⁹. This is the new check
`audit_einstein_universe_route`.

**The route also fixes the ghost count.** Write the Feynman-gauge vector on R × S³ mode by mode:
* A₀ is a minimal scalar on S³, because Ric₀₀ = 0;
* the exact 1-forms carry the scalar spectrum with l ≥ 1;
* the two ghosts are minimal scalars.

So A₀ + exact − 2 ghosts = −(one constant mode), and the Feynman-gauge operator with two ghosts equals the transverse photons alone
(up to a zero mode that only gives a κ¹ term). One ghost (M02) leaves an extra +1/6, and my route rejects it.

### (d) What fixes the sign: the regulator (`regulator_dependence.py`)

**General regulator.** For ln det D → −∫(dt/t) ρ(κ²t) Tr e^{−tD}, the κ² term is proportional to b₁ × ∫₀^∞ du ρ(u)/u². For the
proper-time cutoff ρ = θ(u − 1), so the integral is +1.

**Energy cutoff instead.** I regulated the *canonical* sum directly as Σ ±(ω/2) F(ω/κ), with F ≥ 0, on the same modes:

| Regulator | scalar (ξ = 0) | Weyl | photon |
|---|---|---|---|
| proper time (SPEC) | +1/6 | +1/6 | −2/3 |
| Gaussian F = e^{−x²} | −1/3 | −1/3 | +4/3 |
| exponential F = e^{−x} | −2/3 | −2/3 | +8/3 |

The ratios are universal and the sign is not. Equivalently, a positive energy cutoff corresponds to a ρ with ∫ρ/u² < 0.

**Consequence.** "Scalars and fermions induce G > 0, vectors G < 0" is a theorem of the SPEC's postulates, including the regulator.
It is not a regulator-independent physical statement:
* dimensional regularisation has no κ² term at all;
* Pauli–Villars gives either sign, depending on the regulator masses.

So the SPEC's sentence "its sign … follows from the conventions above" is true only because the conventions include the proper-time
cutoff (C2).

### (e) What is independent and what is shared

**Independent of the builds:**
* the manifold: a non-Einstein product, with R coming from S³ only;
* Lorentzian-time canonical quantisation, with statistics from ±ω/2, not from det^{∓½};
* Coulomb-gauge physical photons, with no Feynman gauge and no ghosts;
* no heat-kernel b₁ formula, no Lichnerowicz and no Weitzenböck identity;
* all of the code.

**Shared with the SPEC and the builds:**
* the proper-time regulator (necessarily);
* the form of S_grav and the R > 0 convention;
* the standard S³ spectra;
* prior knowledge: I knew the literature numbers.

## 2. Review of the two derivations (task 1)

### Checks that both builds pass

**Sign chain (W = −ln Z).**

| Field | Z | W | ln Z per heat trace |
|---|---|---|---|
| Real boson | det^{−½} | +½ ln det = −½∫(dt/t) Tr | +½ |
| Dirac | det D̸ = det(D̸²)^{½} | −½ ln det D̸² = +½∫(dt/t) Tr | −½ |
| Ghosts (one complex Grassmann pair c, c̄ with −∇²) | det(−∇²)^{+1} | | −1, i.e. minus two real minimal scalars |

* The fermion row holds up to a phase (−1)^{N/2} from the ±λ pairs, which does not touch the R term. Neither build mentions it.
* Weyl is half of Dirac, as the SPEC says.

**Endomorphisms.**

| Field | Operator | E |
|---|---|---|
| Scalar | −∇² + ξR | −ξR |
| Dirac | D̸² = −∇² + R/4 (Lichnerowicz) | −R/4 |
| Vector, Feynman gauge | −∇²A_m + R_m^n A_n, which is the Hodge Laplacian (dδ + δd) by Weitzenböck, not the Bochner −∇² | −Ric, so tr E = −R and tr 1 = d |

* Since b₁ depends only on tr E, E = −(R/d)g would give the same k₁. That is the equivalent mutant M23. My R × S³ route has
  Ric ≠ (R/4)g, and it agrees.
* The ghosts are −∇² with no ξ. The FP operator comes from ∇·A, so the matter ξ does not enter. Both builds do this.

**b₁ = tr(E + R/6)**, in the R > 0 convention. Both builds confirm it from exact S⁴ spectra. I checked their S⁴ data:
* scalar l(l+3), degeneracy (2l+3)(l+1)(l+2)/6;
* Dirac ±(n+2), degeneracy 4·C(n+3,3) per sign;
* coexact 1-forms (l+1)(l+2), degeneracy l(l+3)(2l+3)/2 (10 at l = 1);
* exact 1-forms with the scalar spectrum for l ≥ 1.

All are correct.

**Matching.**
* W ⊃ −(κ²/32π²) K ∫√g R, using ∫_{1/κ²}^∞ t^{−2} dt = κ² and (4π)^{−2}.
* Equating this to −(1/16πG)∫√g R gives 1/G = κ²K/2π.
* On the unit S⁴, ∫√g R = 32π², so S_grav = −2π/G, which is build a's −B/(2π).

### Build a

* Complete. Its W(κ) route uses the same statistics postulate as its analytic chain, so it tests the matching arithmetic, the
  regulator integral and the S⁴ volume rather than the statistics postulates. That is all the SPEC asks.
* **B1 (prose only).** §2 says the vector operator comes "from −∇ⁿF_{nm} + ∇_m∇ⁿA_n". The Feynman gauge-fixing term contributes
  **−**∇_m∇·A, which cancels the ∇^n∇_m A_n piece after commuting it as ∇_m∇·A + R_m^n A_n. With "+", the operator would be
  −∇² + Ric + 2∇∇·, which is not Laplace type. The stated result −∇² + Ric is right, and so is the code.
* The fit in §7 at ξ = 0.5 differs from the formula by 2·10⁻⁸ (N2).

### Build b

* Correct, and its analytic chain is the same as build a's.
* **B2 (gap / loose prose).** The "radius route" of DERIVATION §5 is not carried out.
  * The sentence "has constant term −(1/2) b₁ V/(16π²) = −S_part*… printed and compared" is unfinished.
  * The code's "W(a) … ⇒ 1/G > 0" lines print the sign of `inv_G` itself, which is circular.
  * So build b's independent second route checks k₁, including the sign of E, but **not** the statistics and matching signs. The
    sign of 1/G in build b rests on the analytic chain alone.
  * The chain is correct (build a's W route and my §1 both confirm it), so this is a documentation gap with no code effect.
* QUESTIONS records an initial Dirac degeneracy slip (4C vs 8C), corrected. That is honest, and the fix is right.

## 3. Mutants of build a (task 2)

Each mutant is an exact text substitution of `builds/a/induced_g.py` (`S/make_mutants.py`). Each was gated with
`python3 gate.py <dir> --mode builder --campaign induced_g` and
`python3 gate.py <dir> --mode verifier --campaign induced_g --oracle induced_g/oracle.py`, run from `campaigns/`, and then with
`python3 induced_g/audit_proposed_checks.py <dir>`.

Tiers:
* **Bl** is the builder gate (the blind checks). Contract and lint never fired.
* **Or** is the verifier oracle.
* **New** lists the proposed checks: `k1wide`, `xionly`, `weylodd`, `invGwide`, `mpl0`, `ESU` (the §1 route) and `usesk1`.

| Mutant | Error | Builder gate | Verifier gate | Killed by (gate) | Killed by (new checks) |
|---|---|---|---|---|---|
| M01 | overall sign of 1/G | PASS | FAIL | Or: signs, 1/G, stage 1 | invGwide, mpl0, ESU |
| M02 | ghosts counted once (one real ghost) | PASS | FAIL | Or: k1, 1/G, stage 1 | k1wide, invGwide, mpl0, ESU |
| M03 | ghosts with boson sign | PASS | FAIL | Or: k1, signs, 1/G, stage 1 | k1wide, invGwide, mpl0, ESU |
| M04 | Bochner −∇² instead of Hodge (E = 0) | PASS | FAIL | Or: k1, signs, 1/G, stage 1 | k1wide, invGwide, mpl0, ESU |
| M05 | Weyl = Dirac | FAIL | FAIL | Bl: spinor/Weyl; Or | k1wide, invGwide, mpl0, ESU |
| M06 | spinor dimension 2^(d/2), so non-integer for odd d | PASS | FAIL | Or: k1 (d = 3, 5) | k1wide |
| **M07** | **matter ξ applied to the ghosts in k1** | PASS | **PASS** | – | xionly |
| M08 | ξ on the ghosts, in k1 and in inv_G | PASS | FAIL | Or: 1/G, stage 1 | xionly, invGwide, mpl0 |
| M09 | vector k1 d-independent (d = 4) | PASS | FAIL | Or: k1 (the blind "linear in d" accepts a constant) | k1wide |
| M10 | κ instead of κ² | FAIL | FAIL | Bl: scaling; Or | invGwide, mpl0 |
| M11 | 4π instead of 2π | PASS | FAIL | Or: 1/G, stage 1 | invGwide, mpl0, ESU |
| M12 | mpl = √\|1/G\| | FAIL | FAIL | Bl: mpl; Or: stage 1 | mpl0 |
| **M13** | **ξ clamped to ≥ 0 in inv_G** | PASS | **PASS** | – | invGwide, mpl0 |
| **M14** | **\|ξ\| in inv_G** | PASS | **PASS** | – | invGwide, mpl0 |
| **M15** | **mpl returns 0.0 (not None) at 1/G = 0** | PASS | **PASS** | – | mpl0 |
| M16 | fermions with boson statistics in inv_G | PASS | FAIL | Or: signs, 1/G, stage 1 | invGwide, mpl0, ESU |
| M17 | Lichnerowicz sign, E = +R/4 | PASS | FAIL | Or: k1, signs, 1/G, stage 1 | k1wide, invGwide, mpl0, ESU |
| M18 | Weitzenböck sign, E = +Ric | PASS | FAIL | Or: k1, signs, 1/G, stage 1 | k1wide, invGwide, mpl0, ESU |
| **M19** | **ξ applied to the spinor operator in k1** | PASS | **PASS** | – | xionly |
| **M20** | **spinor dimension halved for d > 10** | PASS | **PASS** | – | k1wide |
| **M21** | **Weyl silently defined in odd d** | PASS | **PASS** | – | weylodd |
| M22 | tr 1 = d − 2 and ghosts as well (double subtraction) | PASS | FAIL | Or: k1, 1/G, stage 1 | k1wide, invGwide, mpl0, ESU |
| *M23* | E = −(R/d)g for the vector (*equivalent*: same trace) | *PASS* | *PASS* | – | – (correctly passes) |
| M24 | mpl returns 1/G (no square root) | FAIL | FAIL | Bl: mpl; Or: stage 1 | mpl0 |
| M25 | 1/G clamped at ≥ 0 | FAIL | FAIL | Bl: additivity; Or | invGwide, ESU |
| **M26** | **ξ clamped to [−½, ½] in the scalar k1** | PASS | **PASS** | – | k1wide, invGwide, mpl0 |
| M27 | conformal ghosts −∇² + R/6 (ghost part 0) | PASS | FAIL | Or: k1, 1/G, stage 1 | k1wide, invGwide, mpl0, ESU |
| *M28* | closed form typed into inv_G (*correct values*, not derived) | *PASS* | *PASS* | – | usesk1 (heuristic) |
| M29 | odd-d Dirac with 2^⌈d/2⌉ | PASS | FAIL | Or: k1 | k1wide |
| M30 | inv_G uses k1(vector) at d = 5 | PASS | FAIL | Or: 1/G, stage 1 | invGwide, mpl0, ESU |

**Totals**
* There are 30 mutants: 28 wrong, 1 equivalent (M23) and 1 correct-valued typed-in (M28).
* **The gate kills 20 of the 28 wrong mutants.**
  * The builder tier kills 5: M05, M10, M12, M24, M25.
  * The other 15 die only on the oracle.
* **8 wrong mutants survive both gates: M07, M13, M14, M15, M19, M20, M21, M26.** Each is wrong only where the oracle does not
  sample.
* **All 28 wrong mutants fail `audit_proposed_checks.py`**, and so does M28 (on the heuristic check).
* M23 passes, as an equivalent mutant must.
* **Both builds pass all 7 proposed checks** (`checks_a.log`, `checks_b.log`; worst 4·10⁻¹⁶, and 1.6·10⁻⁹ for the fitted ESU route).
* Every mutant that changes a d = 4 per-species value (M01–M05, M11, M16–M18, M22, M25, M27, M30) is also killed by the
  independent ESU route on its own.
* The ghost-count error M02 survives the oracle's *sign* check (a vector with one ghost still gives a negative 1/G). The oracle's
  value checks and the ESU route kill it.

## 4. New checks (task 3; `audit_proposed_checks.py`, `CHECKS = [(label, fn)]`, fn(module) → (ok, detail))

| Check | Closes | What it tests |
|---|---|---|
| `audit_k1_wide` | M20, M26 (and M06, M09, M29) | k₁ for every kind at d = 1…26 and the scalar at ξ = −10³…10³, against tr(E + R/6); the oracle stops at d = 10, \|ξ\| ≤ 0.4 |
| `audit_xi_only_in_scalar` | M07, M19 | k₁ of dirac, weyl, vector and vector_no_ghosts is independent of ξ; the oracle calls non-scalar kinds only at ξ = 0 |
| `audit_weyl_odd_d_rejected` | M21 | k1('weyl', odd d) raises or returns None/NaN (SPEC: even d only) |
| `audit_inv_G_wide` | M13, M14 | 5760 points, κ from 10⁻³ to 10¹⁹, counts 0…1000, ξ < 0 with n_s > 0 (the oracle's only ξ < 0 point has n_s = 0), plus exact linearity in ξ and in each count (reference-free) |
| `audit_mpl_boundary` | M15 | mpl is None at 1/G = 0 exactly (no fields; conformal scalars only) and for 1/G < 0, √ for 1/G > 0, including ξ < 0 |
| `audit_einstein_universe_route` | independent anchor | per-species 1/G against §1, computed live (about 0.1 s) |
| `audit_inv_G_uses_k1` | M28 | heuristic: inv_G's body calls k1; evadable, so the transcript audit remains the guard |

## 5. Findings and class counts

**B (builder): 2, documentation only, no code defect.**
* **B1.** Build a §2 has the wrong sign of the gauge-fixing term in prose; the stated result is right.
* **B2.** Build b's second route does not test the statistics or matching signs. Its "radius route" is unfinished prose plus a
  circular print. The sign is confirmed independently here.

**R (reference / oracle): 3, all coverage gaps. No oracle value is wrong.**
* I re-derived every `ref_k1` and `ref_inv_G` value. The stage-1 number also checks:
  √[(3 + 11.5 − 34/3)/(2π)] · 5.3355·10¹⁹ = 3.788·10¹⁹, and at ξ = 1/6 with 66 Weyl, 1/G = −κ²/(6π) < 0.
* The Larsen–Wilczek, Vassilevich, Solodukhin and Visser citations were not re-read here (no network). The values agree with §1.
* **R1.** Sampling gaps: d ≤ 10; ξ only on the scalar kind; ξ < 0 only with n_s = 0; no Weyl at odd d; mpl never at 1/G = 0.
  These let M07, M13–M15, M19–M21 and M26 through. Fix: adopt `audit_proposed_checks.CHECKS` into the gate's oracle (or blind)
  tier.
* **R2.** The blind check "vector k₁ linear in d" accepts a d-independent constant (M09). Fix: also require a nonzero slope (blind:
  it follows from tr 1 = d, which the check label already states).
* **R3.** `LINT_EXACT` (1/(2π), ±2/3) cannot see `kappa**2/(2*math.pi)*(n_s*(1/6 - xi) + n_w/6 - 2*n_v/3)`, because `_fold` only
  folds constant subtrees (M28). Same issue as nucleon_pol C2. The heuristic `audit_inv_G_uses_k1` is a partial guard.

**C (SPEC): 4.**
* **C1.** "Faddeev–Popov ghosts, which are Grassmann scalars" gives no count and no operator. Both builds chose one complex pair
  c, c̄ with −∇², which is standard and is confirmed by §1c (the only choice that leaves the transverse photons). Wording fix: "one
  complex Grassmann ghost pair with operator −∇² (no ξ)".
* **C2.** The sign of 1/G is fixed by the regulator, not by the field content (§1d). With a positive energy cutoff on the canonical
  zero-point sum, all three signs flip; in dimensional regularisation there is no κ² term. The SPEC should say that "the sign
  follows from the conventions" *because* the convention includes the proper-time cutoff, and every downstream use of "matter
  induces attractive gravity" should carry that qualifier.
* **C3.** The meaning of the `xi` argument of k1 for non-scalar kinds is unspecified. Both builds ignore it, which is right because
  the ghosts' and spinors' operators have no ξ. The SPEC should say so; `audit_xi_only_in_scalar` enforces it.
* **C4.** The behaviour of k1('weyl', odd d) is unspecified ("even d only"). Both builds raise ValueError. The SPEC should say "raise".

**N (numerical): 3.**
* **N1.** Exact cancellations in floats.
  * At n_s = 4, n_v = 1 (or 1 scalar, 3 Weyl, 1 vector), 1/G is exactly 0. Build a returns 0.0 and build b returns −1.8·10⁻¹⁷ κ².
  * Both return mpl = None, but a rounding to +10⁻¹⁷ would return 4·10⁻⁹ κ. This is harmless, and the cross-build difference is
    10⁻¹⁷.
  * A tolerance in mpl (or Fraction arithmetic in inv_G) would make it deterministic.
* **N2.** Build a's W-route fit at ξ = 0.5 differs by 2·10⁻⁸. This is a fitting residual.
* **N3.** M23 is an equivalent mutant: b₁ sees only tr E.

## 6. Limits of the result (what "established within the SPEC" does not cover)

* **Regulator.** The κ² coefficient, including its sign, belongs to the proper-time cutoff (§1d, C2). Other regulators rescale the
  value by a factor and can flip the sign (energy cutoffs give −2× and −4× here). The universal content is the b₁-weighted
  combination
  Σ (±) k₁ = n_s(1/6 − ξ) + n_w/6 − 2n_v/3,
  together with the logarithmic (b₂) terms.
* **Same cutoff for all fields** (SPEC). Different κ per species would change the relative weights. A physical cutoff, for example
  from a UV completion, need not be common.
* **No tree-level term.** With a bare 1/G₀ the result is only the renormalisation δ(1/G).
* **No graviton loop.** The metric is classical. Graviton and graviton-ghost contributions to b₁ are not included.
* **Massless fields.** Masses m ≪ κ change only finite terms, but in induced-gravity models with Σ m² ln m² constraints (for
  example Frolov–Fursaev–Zelnikov), those finite terms *are* the answer. They are outside this SPEC.
* **d = 4 only for inv_G.** k₁(d) is general.
* **Gauge fields: Kabat's contact term (entropy vs 1/G).**
  * On a cone (black-hole entanglement entropy), the vector's area term from its d − 2 = 2 physical polarisations is
    +2/6 = +1/3, like two scalars. The −tr Ric (= −1) piece of k₁ = 2/6 − 1 = −2/3 appears there as Kabat's contact term,
    localised at the tip.
  * The induced 1/G computed here on smooth manifolds includes that piece as an ordinary bulk term. My §1 route obtains −2/3 from
    the physical transverse photons alone on a smooth R × S³, so the negative vector contribution to 1/G is not a ghost artefact
    and not a contact-term ambiguity.
  * What fails for vectors is the statement "entanglement entropy = A/4G_induced" without the contact term. Neither the SPEC nor
    the builds use that statement.
* **Non-abelian vectors.** One generator counts as one abelian vector at one loop, as the SPEC says. Interactions are not included.

## 7. Reproduce

```
cd rebuild/campaigns
python3 S/make_mutants.py && S/run_gates.sh            # gates.log
for d in S/mutants/* S/copies/a S/copies/b; do python3 -B induced_g/audit_proposed_checks.py $d; done
python3 S/casimir_esu.py; python3 S/regulator_dependence.py     # (run from S)
```
