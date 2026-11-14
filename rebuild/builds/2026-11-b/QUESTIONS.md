# QUESTIONS: build 2026-11-b

## Stage `toolkit`

No missing inputs; nothing quoted. Points where SPEC.md / contract.py are silent, and the choice made:

1. **`bisect` / `golden_max` return value.** Contract says "a root" / "the maximizer" but not which point of the
   final bracket. Resolved: return the bracket midpoint; iteration stops early once the bracket reaches
   floating-point resolution (so `iters=200` is an upper bound). Builds may differ at the 1e-16 (bisect) or
   ~1e-8 relative (golden section, limited by sqrt(machine epsilon) near a smooth maximum) level.
2. **`bisect` with an invalid bracket.** Contract requires f(a) f(b) < 0. Resolved: an endpoint that is exactly a
   root is returned; same-sign endpoints raise `ValueError` rather than return a silent non-root.
3. **`golden_max` on ties** (f(c) == f(d)): keeps the left sub-interval [a, d]. Irrelevant for strictly unimodal f.
4. **`trapezoid` with fewer than 2 samples:** returns 0.0 (no interval). Result is coerced to `float`, so
   Fraction samples are accepted but complex samples are not (contract says `-> float`).
5. **`eigvalsh` input symmetry:** the matrix is symmetrized, (A + A^T)/2, before iteration; a genuinely
   non-symmetric input is outside the contract and is not detected.
6. **`hessian` step:** per SPEC section 1 h is absolute and identical in all coordinates; no rescaling by |x|.
   Off-diagonal entries use the four-point stencil (4 evaluations each), diagonal the three-point one.
7. **`exact_derivative` scope:** the contract lists + - * / and rational constants; integer powers (`**`, including
   negative) are also supported since they are repeated * and /. Float constants inside f are rejected
   (TypeError) rather than silently made inexact. A constant f (returns a plain number) gives Fraction(0).
8. **`levi_civita` on non-permutations:** any input that is not a bijection of 0..n-1 (repeated *or*
   out-of-range index) returns 0; the contract only mentions repeats.

## Stage `gauge331`

No missing inputs; nothing quoted. Ambiguities and the choice made:

1. **Antitriplet component order.** SPEC says the antitriplet's first two charges are (Q_u, Q_d) "in some
   order". Since -T3 reverses the doublet, the order is (Q_d, Q_u); X_a = Q_u - 1/2 + b.
2. **Lepton X_L.** SPEC states X_L (-1/3, -2/3). The code derives it from "electron = T3 = -1/2 member with
   charge -1" (X_L = -1/2 - b) and `__main__` shows it equals the stated values; the stated values are not typed in.
3. **`quark_charges` for even N_c.** n_A = (1+N_c)/2 is not an integer; the function still returns the rational
   continuation (N_c+1)/(2N_c), (1-N_c)/(2N_c) rather than raising. Only odd N_c is physical.
4. **`doublet_charge_pairs` at N_c = 1.** N_g - n_A = 0 triplet quark families; multiplets with zero multiplicity
   are skipped (the returned set is unchanged, as antitriplets give the same pair).
5. **Sign/phase of the covariant derivative.** Not specified; irrelevant, since M2 is quadratic in g_A T_A.
6. **`neutral_masses` selection.** Returns the two largest eigenvalues of the 3x3 block (the photon's zero is
   dropped by position, not by a threshold). For w/v >~ 1e4 the light eigenvalue from the Jacobi solver loses
   relative accuracy ~ eps * (w/v)^2 (seen as 4e-9 at w = 4e6); the closed form (T, P) in `__main__` does not.
7. **G_F matching.** G_F/sqrt2 = g^2/(8 M_W^2) is used as the tree-level definition of G_F, not derived from a
   muon-decay amplitude; tagged `derived` on that basis since the contract fixes the formula.
8. **`photon_direction` normalization.** Unnormalized, chosen so that sum_A n_A g_A T_A = Q exactly
   (n_3 = 1/g, n_8 = beta/g, n_9 = 1/g_X); then |n|^2 = 1/e^2.

## Stage `chiral`

No missing inputs. `chpt_mpi` is quoted (allowed); everything else is derived. Ambiguities and the choice made:

1. **`goldstone_count` zero threshold.** "Zero mode" of a numerical Hessian needs a tolerance. Resolved: step
   h = 1e-4 v (caller scales h, SPEC section 1), count |e| < 1e-6 max|e|; the stencil's truncation error on the
   quartic is lam h^2/2, i.e. 2.5e-9 of the sigma mass^2. Needs lam > 0, v > 0 (v = 0 has no broken symmetry and
   the scaled step would vanish).
2. **Which vacuum direction.** SPEC names phi = (sigma, pi) but not the vacuum; O(4) makes all equivalent, taken
   as (v, 0, 0, 0).
3. **`sigma_model_vacuum` returns m_pi^2 = H/sigma0**, not lam (sigma0^2 - v^2). Identical at the exact root
   (stationarity), but H/sigma0 has no cancellation at small H; builds using the other form may differ at
   ~1e-16/(H/(lam v^3)) relative. sigma0 is the bisection root (bracket midpoint at float resolution).
4. **Sign of H.** For H < 0 the vacuum is returned at sigma0 < 0 (reflection), m_pi^2 unchanged; for H = 0,
   (v, 0). SPEC only considers H > 0.
5. **GMOR "f_pi = <sigma>".** Used exactly (m_pi^2 = H/sigma0 is exact in the model), so `gmor_mpi` =
   sqrt(mq_sum cond13^3)/f_pi with physical f_pi; no chiral-limit correction.
6. **`chpt_mpi` when the bracket is negative:** raises ValueError (no clipping).
7. **`tensor_identity_residual` at q = 0:** qhat undefined; returns 0.0 (both sides vanish).
8. **Goldberger-Treiman provenance:** tagged `derived` (PCAC pole argument, DERIVATION section 7). The pion-pole
   dominance and smoothness of g_A(q^2) are PCAC assumptions; the overall sign convention is not tracked (modulus only).
9. **Lint note:** the self-check could not use m = 1.3 as a test mass because 1.3 coincides with an entry of
   inputs.py (GW_M2 error); 1.5 is used instead. No effect on exports.

## Stage `casimir`

No missing inputs. `cp_energy` rests on the quoted fluctuation formula (allowed); everything else is derived.
Ambiguities and the choice made:

1. **Gravity in the safe-gap criterion.** SPEC section 4 says "gravity phase" without giving the potential, and
   this stage may not import `graviton` (a later stage). Resolved: U_G = -G m^2/r (inputs.G_NEWTON) is assumed
   here; it is derived from graviton exchange only in stage `graviton`. blind/checks.py uses the same form.
2. **"Smallest gap".** The phase ratio is C/(G m^2) sum_{j=0..6} gap^-(6-j) d^-j, strictly decreasing in the gap,
   so the safe set is [g*, oo) and the smallest safe gap is the unique root. The bracket is derived
   (g0 < g* < 7^(1/6) g0, g0 = (C/(fraction G m^2))^(1/6)), widened by 1e-9 relative; bisection runs to float
   resolution. The ratio is evaluated in the factored form (no cancellation), not from differences of energies.
3. **Geometric validity not enforced.** gap >= 2R (no overlap) and gap >> R (point dipoles, retarded regime,
   constant alpha) are not imposed; for an extreme `fraction` the returned root could be unphysical. At the
   baseline gap/R is about 206.
4. **tau.** Cancels identically; accepted and required positive, otherwise unused. m <= 0, tau <= 0 or
   fraction <= 0 raise ValueError.
5. **`sphere_K` types.** float eps -> float; anything else (int, Fraction) is converted with Fraction(eps) and
   returns a Fraction. eps = -2 (no static solution) raises ZeroDivisionError.
6. **`green_tensor` at r = 0** raises ValueError; entries are floats. Sign convention as SPEC states
   (G = (k^2 delta - dd) e^(-kr)/r; at k = 0, (delta - 3nn)/r^3).
7. **`cp_integral` normalization.** Taken literally from the contract: int (1/2) r^6 Tr[G.G] du, so that
   U = -(hbar c/pi) I alpha1 alpha2/r^7.
8. **Lint note:** the self-check's sample count is written 4 * 10 ** 4 because integer literals above 10000 are
   rejected. No effect on exports.

## Stage `graviton`

No missing inputs; nothing quoted. Ambiguities and the choice made:

1. **Units of the stress tensors in the exchange.** SPEC gives the amplitude only as "proportional to T2.P.T1".
   The normalization is derived as U = -(1/2)(16 pi G)(T2.P.T1) yukawa(r, 0) (coupling h T/2 times the field
   equation's source strength). The code uses unit rest-frame tensors (1,0,0,0) times m1 m2, i.e. c cancels
   analytically (T^00 = m c^2, G -> G/c^4) and inputs.C_LIGHT is never read. Motion corrections O(v^2/c^2) to
   the stress tensors (v ~ 1e-3 m/s) and retardation are dropped: the potential is the static one.
2. **`ramp_profile` with ramp = 0.** SPEC's formula divides by ramp. Resolved as the limit: s = 1 on [0, T],
   0 outside. For ramp > 0, t outside [0, T] gives 0 through the clamp.
3. **`ramp_profile` boundaries.** "t < ramp" uses the opening branch, ramp <= t <= ramp + hold returns exactly 1,
   later t the closing branch; the pieces agree at the joints, so the choice of closed/open ends is immaterial.
4. **Return type of `ramp_profile`.** Returns int 0/1 at exact endpoints and in the hold, float elsewhere
   (contract says "float in [0, 1]"; values compare equal).
5. **Trapezoid sampling.** t_i = T i/(n-1), i = 0..n-1, spacing T/(n-1); the hold/ramp joints are generally not
   on the grid. The integrand is assembled as [-2U(gap) + 2U(d_cross)] per sample (energies in J), integrated
   by toolkit.trapezoid and divided by hbar at the end. A build that factors G m^2/hbar out of the sum
   differs at the 1e-15 relative level. Trapezoid error at n = 4001 for design A is ~1e-11 relative (vs Simpson).
6. **`tpt` with non-Fraction entries.** Ints are promoted to Fraction (result Fraction); floats pass through and
   give a float. The contract only specifies Fractions.
7. **`point_mass_metric` units.** "GM/(c^2 r)" with h_mn having lower indices and signature (-,+,+,+), so
   g_00 = -1 + h00 GM/(c^2 r); the sign convention h00 > 0 follows from eta_00 = -1 and is what the blind check
   expects.

## Stage `desitter`

No missing inputs; nothing quoted. Ambiguities and the choice made:

1. **`mm_coupling` normalization.** The contract defines it as l^2/lP^2 and that is what is returned
   (= 3/(Lambda lP^2)). The coefficient N of the action N int eps F^F that reproduces Einstein-Hilbert is
   N = -l^2/(64 pi G) (hbar = c = 1), i.e. -(1/(64 pi)) l^2/lP^2 (DERIVATION section 7); the factor
   -1/(64 pi) is NOT included in the export.
2. **Meaning of Lambda.** SPEC section 6 does not state the Einstein equation with a cosmological constant.
   Lambda is taken as the constant in the Einstein-Hilbert form e(R - 2 Lambda), to which the
   MacDowell-Mansouri action reduces with Lambda = 3/l^2; hence l = sqrt(3/Lambda). Cross-check: R = 12/l^2
   = 4 Lambda. This standard definition is the one assumption beyond the SPEC.
3. **Units and normalization of the residuals.** `curvature_split_residual` and `ds_curvature_max` return
   maxima over COORDINATE components (mu, nu), not frame components, in G = c = 1; F^{a4} is the coefficient
   of J_a4, i.e. T^a/l (it includes the 1/l). `ds_curvature_max` takes the max over all 5x5 matrix entries of
   F_{mu nu} (the matrix entry [a][b] is F^a_b; |F^a_b| = |F^{ab}|).
4. **How the residual is a real test.** F = dA + [A, A] is built from 5x5 matrices with a NUMERICAL derivative
   (5-point stencil, h = 1e-3, relative in r, halved until the stencil stays in f > 0), while R^{ab} uses the
   ANALYTIC derivatives of omega (needs f''). The residual is therefore stencil noise (~1e-12), not identically
   zero. A point closer to a horizon than the stencil can resolve gives a larger residual.
5. **`unbroken_generators`** lists the basis generators J_AB that annihilate V, as the contract says; it does not
   compute the full stabilizer subalgebra (linear combinations) for a V off the coordinate axes. Zero test:
   |J V| <= 1e-12 max|V|. Returns (A, B) in lexicographic order.
6. **`spin_connection` domain.** f(r) <= 0 raises ValueError (the diagonal tetrad is real only in the static
   region). Entries are floats; f and fp are callables of r.
7. **`action_coefficients` where R = 0.** cR = (eps R e e)/(e R) is undefined for a Ricci-flat geometry
   (l -> infinity); on SdS R = 12/l^2 > 0. Not guarded.
8. **Sign conventions.** F_{mu nu} = d_mu A_nu - d_nu A_mu + [A_mu, A_nu]; a 2-form is (1/2) R_{mu nu} dx^mu ^
   dx^nu. With eps_0123 = +1 and the component read on dt^dr^dtheta^dphi, (cR, cV) come out positive; the
   tetrad determinant e = r^2 sin(theta) is used with its sign (no absolute value).

## Stage `blackholes`

No missing inputs. Quoted (all on the stage's list): `qnm_220`, `invert_220` (Berti-Cardoso-Will 2006 fit),
`hawking_K`. Ambiguities and the choice made:

1. **`killing_kappa` is evaluated at r0, not extrapolated to the horizon.** The scalar -(nabla xi)^2/2 is
   regular through the horizon and equals f'(r0)^2/4 at the sample radius; the function returns its square
   root at r0 (for Schwarzschild M/r0^2, i.e. (1/4M)(1 + d)^-2 at r0 = 2M(1 + d)). It therefore differs from
   the horizon value by O(d). `h` is the step of the central difference of the metric in r; the theta
   difference uses a fixed step 1e-6 at theta = 1 rad (these components do not enter kappa).
2. **`kerr_first_law`: status of S, T, Omega, J.** SPEC section 7 lists them as quoted (Bardeen-Carter-Hawking)
   but the export is not on `quoted_allowed`. Resolved: PROVENANCE says `derived`, meaning the *identities*
   (first law, Smarr) are derived from the SPEC's formulas; the formulas themselves are postulates, not
   re-derived from the Kerr metric (which is not in the SPEC). pi and a = sqrt(pq) cancel exactly:
   T dS = (p - q) d(p^2 + pq)/(4 (p^2 + pq)), Omega dJ = d(J^2)/(2 M (p^2 + pq)); the latter is the finite
   limit at q = 0. (dp, dq) is a direction: the residual is linear in it. Differentials are taken by
   `toolkit.exact_derivative`.
3. **`kerr_area_km2`: same status.** The formula is stated by the SPEC; it is shown to follow from the SPEC's
   Kerr data (A = 4S = 4 pi (p^2 + a^2) = 8 pi M r_+). That A = 4S (hbar = G = 1) and the Kerr metric's
   horizon 2-geometry are standard but not in the SPEC. |chi| > 1 raises ValueError.
4. **`sds_horizons` edge cases.** Returns None when the maximum of f is negative; if it is exactly 0.0 in
   floating point the double root (r0, r0) is returned; M <= 0 or l <= 0 raises ValueError (pure de Sitter,
   M = 0, has only r_c = l and is not handled).
5. **`euclidean_cone_ratio`.** eps may be negative (cosmological horizon; the static side is r < r_c). The
   proper radius uses a 200-node trapezoid rule in u, r = rh + eps u^2; accuracy ~1e-7 for eps << rh, ~2e-6
   for eps ~ rh/4. `rh` is taken on trust (not re-solved); f <= 0 inside the interval raises ValueError.
6. **`photon_sphere`, `isco`: "numerically".** Golden-section search finds a smooth extremum only to
   ~1e-8 relative, at the crossbuild tolerance. Resolved: photon sphere = `toolkit.golden_max`, then polished by
   `toolkit.bisect` on the exact slope (`toolkit.exact_derivative`); ISCO = `toolkit.bisect` on the exact
   symmetric difference of L^2(r) = -f'/(f/r^2)' (h = 1e-9, exact Fractions). No closed form is used in the
   code; the closed forms (3, sqrt 27; 6, 12, 8/9) appear only in the self-check. `isco` returns
   E2 = E^2 (energy per unit mass squared) and L2 = L^2 in units of M^2.
7. **`qnm_220` / `invert_220` units and frames.** The mass in `qnm_220` is the detector-frame mass;
   frequency = omega/(2 pi) in Hz, damping = omega/(2Q) in 1/s; `invert_220` takes them in the same units and
   returns M_det/(1 + z). The inversion is algebraic (chi = 1 - ((Q - q1)/q2)^(1/q3)); a Q outside the fit's
   range raises ValueError. Error tuples in `inputs` (F220, G220, THETA_G_*) are read as (value, lower, upper).
8. **`shadow_uas`.** Uses inputs.GM_SUN and inputs.PARSEC; radian -> microarcsecond = (180/pi) 3600 1e6.
9. **Self-check, Sgr A\*.** "The measured theta_g is the mean of the two theta_g values" is read as: the
   stellar-dynamics theta_g compared with the EHT's THETA_G_SGRA is (theta_g(VLTI) + theta_g(Keck))/2, and the
   pull is (that - EHT)/sigma_EHT with the EHT error on the side facing it. If the SPEC meant the opposite
   roles, the pull's denominator changes (no export is affected).
10. **Self-check, area theorem.** Component spins are not in `inputs`; the final area is compared with the
    largest possible initial area (both components non-spinning).

## Stage `links`

No missing inputs. Quoted: only the pi0 anomaly amplitude (allowed). Ambiguities and the choice made:

1. **`neutrality_per_nucleon`: what carries the charge.** The SPEC gives the ratio k Q^2/(G m^2) only.
   Resolved: both diamonds carry the same net charge Q; vacuum Coulomb law (no EPS_DIAMOND factor; induced
   dipoles are rung 3's background); nucleon count = m / inputs.U_AMU; the result is |Q|/(e N) at
   Coulomb = GAP_FRACTION x gravity, i.e. (u/e) sqrt(F G/k). If the charges were meant unequal, or the count to
   use inputs.M_N, the number changes by an O(1) factor.
2. **`g_window` when p3 <= p5.** The contract assumes pole_5 < pole_3. Resolved: always return
   ((mpl/p3)^2, (mpl/p5)^2) unclipped; lo >= hi then signals an empty window. p3, p5 and mpl must share units
   (GeV with inputs.POLES_331).
3. **`pi0_width_eV` units and conventions.** fpi and mpi in GeV, result x 1e9 to eV; f_pi is the ~92 MeV
   convention (inputs.F_PI); the amplitude multiplies eps^{mu nu rho sigma} e1*_mu k1_nu e2*_rho k2_sigma with
   no extra factor; identical-photon factor 1/2 included. Result: Gamma = A^2 m^3/(64 pi). Provenance is
   declared `quoted` (amplitude), with the polarization sum and phase space derived.
4. **`planck_mass_GeV` conversion.** J -> GeV uses inputs.E_CH (read at call time) for any (G, hbar, c).
5. **`matter_charges` X_L.** Taken from the SPEC's stated values (-1/3, -2/3), not solved from Q_e = -1, so
   q_e = -1 is a test of them. "Reverse" for the neutron = ((Nc-1)/2 u, (Nc+1)/2 d). Returned order
   (q_p, q_n, q_e, Q_nu) with the neutrino = component 1, the electron = component 2.
6. **`schwarzschild_radius`.** Mass in kg, radius in metres, 2 G m/c^2 with inputs.G_NEWTON, C_LIGHT.

## Provenance notes (M5 rule)

SPEC section 0 (last paragraph): a `derived` export that rests on a quoted export names it, with the word
"quoted". Three notes were extended (note text only; no code, value or provenance kind changed; all three
stay `derived`, none is on a `quoted_allowed` list):

1. **`casimir.casimir_safe_gap`** rests on the quoted `cp_energy`: the Casimir strength C in the phase ratio is
   the coefficient of the quoted Casimir-Polder formula (the private `_cp_coefficient` that `cp_energy` divides
   by r^7). The root-finding and the geometry are derived.
2. **`graviton.design_phase`** rests on the quoted `casimir.cp_energy` through `casimir.casimir_safe_gap` (the
   gap at which the phase is evaluated). The gravitational phase at a given gap is derived.
3. **`links.planck_bh_kT_GeV`** rests on the quoted `blackholes.hawking_K` (Hawking 1975). Only the Planck mass
   and the unit conversion are derived here.

## Stage `running` (SPEC section 9)

Nothing could not be derived; nothing is quoted (`inputs.POLES_331` is not used by this stage).
Interpretation points and how they were resolved (DERIVATION_running.md section 6):

1. **Colour multiplicity of the singlet partners.** "Each electrically charged fermion component ... has one
   singlet partner": resolved as one partner per component per copy of the multiplet, so a quark component's
   partner comes in N_c colours and once per family (like u^c, d^c). Supported by the exact anomaly sums
   ([SU(3)_C]^2 U(1)_X, gravitational, [U(1)_X]^3), which vanish only with this counting.
2. **Scalars.** Only the three complex scalar triplets of section 2, colour singlets, no singlet partners.
   Their X charges are section 2's postulates, entered as exact thirds.
3. **Lepton X.** Solved from the electron charge -1 (T3 = -1/2 component) with `gauge331.triplet_charges`, not
   copied from the SPEC's (-1/3, -2/3); the two agree exactly. The antitriplet's first two components come out
   as (Q_d, Q_u) (the only consistent order).
4. **The theory below MU_331 is always the 3-colour, 3-generation Standard Model**, also for
   `landau_pole(5, variant)`: `couplings_at` takes no N_c. So 1/alpha_X(MU_331) is N_c- and variant-independent
   (1/alpha_X = 1/alpha_Y - beta^2/alpha_2, beta^2 = 1/3), and N_c and the variant enter only through b_X.
5. **`landau_pole` is the scale of alpha_X = 1** (SPEC's definition), not of 1/alpha_X = 0, which is a factor
   exp(2 pi/b_X) higher. It raises ValueError if alpha_X >= 1 already at MU_331.
6. **`matching_331` raises ValueError** when the matching has no real g_X (1/alpha_Y <= beta^2/alpha_2).
7. **Even N_c** gives a non-integer number of antitriplet families; not rejected, b stays an exact Fraction.
