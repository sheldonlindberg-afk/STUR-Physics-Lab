# QUESTIONS / resolved ambiguities: build 2026-11-a

## toolkit

1. **Hessian step is absolute.** `hessian(f, x, h=1e-4)` uses the same absolute step h in every
   coordinate (the contract gives a single scalar h). Callers whose coordinates are far from
   O(1) (e.g. vevs in GeV ~ 1e2..1e4, or fields in physical units) must pass a suitable h
   themselves; the optimum is h ~ (eps |f| / |f''''|)^(1/4). No per-coordinate rescaling is done.
2. **Floats rejected in `exact_derivative`.** The contract says f uses rational constants. A
   float constant (or float x) raises TypeError instead of being converted, since silently
   mixing floats would make the "exact" result inexact. Integer powers x**n (n any int,
   including negative, or an integral Fraction) are supported as repeated products;
   non-integer powers raise TypeError. Comparisons act on the real part.
3. **`eigvalsh` symmetrizes its input** as (A + A^T)/2 and converts entries to float (Fractions
   allowed). Exact zero modes come out at ~1e-16 of the largest |eigenvalue|; nonzero
   eigenvalues far below eps*||A|| are only accurate in absolute terms (~eps*||A||) unless the
   matrix is graded/diagonally dominant.
4. **`bisect` returns an exact zero immediately** if f vanishes at an endpoint or midpoint, and
   raises ValueError when f(a) f(b) > 0. `golden_max` accepts a > b by swapping.
5. `levi_civita` returns 0 for any sequence that is not a permutation of 0..n-1 (repeats or
   out-of-range entries), extending "0 if repeated index".

## gauge331

1. **"Remaining neutral component".** For beta = -1/sqrt3 the third scalar (X = -1/3) is neutral
   in components 1 AND 3. I read "each other triplet takes its remaining neutral component" as
   "its neutral component other than component 3 (the w slot)", which is unique in both variants.
   Result (both variants): w in phi1 comp 3, v1 in phi2 comp 2, v2 in phi3 comp 1. The code raises
   if the rule does not single out exactly one component.
2. **Antitriplet X.** `triplet_charges(X, variant, anti=True)` takes X as the antitriplet's own
   U(1)_X charge (X is not conjugated); only T3, T8 flip sign: Q = (-1/2 - b + X, 1/2 - b + X, 2b + X).
   With this, the antitriplet's first two components are (Q_d, Q_u), so X_a = X_t + 2b (matches SPEC section 8).
3. **X_L derived, not read.** The lepton-triplet X is derived from Q_e = -1 (X_L = -1/2 - b); it
   reproduces SPEC's listed -1/3 and -2/3. quark_charges(Nc) has no variant argument; it solves the
   anomaly for both variants and asserts the same answer (b cancels identically).
4. **N_c = 1** is accepted (n_A = 1, no quark triplets); even N_c raises ValueError.
5. **neutral_masses** drops the eigenvalue of smallest modulus (the photon) from the 3x3
   (W3, W8, B) block, which decouples exactly from W1,2,4..7 for these vev patterns.
6. The scalar X charges are SPEC postulates written as small Fractions in the code (selected by the
   sign of b); no measured number is used in this stage (G_F, alpha, s^2 are function arguments).

## casimir

1. **Gravity potential inside `casimir_safe_gap`.** contract lists casimir's dependencies as toolkit
   only, so the gravity phase here uses U_g = -G m^2/r directly (inputs.G_NEWTON at call time). It is
   identical to -4 pi G m^2 chiral.yukawa(r, 0) (the ladder's rung 2 -> 4 derivation, which is done
   and connection-checked in stage graviton) and to the blind check's form. Not imported from
   chiral to keep within the declared dependency list.
2. **"Casimir phase <= fraction x gravity phase"** is read with absolute values of both entangling
   phases (both are positive in the parallel geometry since both potentials are attractive and
   monotone). The ratio is proved strictly decreasing in the gap (geometric-sum identity, see
   DERIVATION_casimir.md section 6), so "smallest gap" = the unique root.
3. **Both diamonds equal**: same m, R = diamond_radius(m), K = sphere_K(inputs.EPS_DIAMOND) (float eps
   gives a float K by the same exact elimination). Static alpha for all xi, as SPEC says.
4. **cp_energy units**: R in m, K dimensionless, r in m, returns J; alpha_i = K_i R_i^3 (the
   4 pi eps0 is absorbed by P3's convention). Only the fluctuation formula is quoted; the
   reduction to -(hbar c/pi) I K1 K2 R1^3 R2^3/r^7 and I itself are derived.
5. **sphere_K for int eps** is promoted to Fraction (exact); float eps stays float.

## graviton

1. **Clamp in the profile.** SPEC's "up(x) ... (clamped to [0, 1])" is applied to the argument x
   before up (and therefore also bounds the output). Without clamping x, up(x < 0) = 2x^2 > 0 would
   re-open the branches for t > T or t < 0. Inside [0, T] the two readings agree.
2. **Hold boundaries.** s = 1 for ramp <= t <= ramp + hold (closed interval); up is continuous there
   (up(1) = 1), so the choice does not affect values.
3. **Matter coupling normalization.** SPEC gives the amplitude only "proportional to" T2.P.T1. The
   absolute normalization U(q) = -8 pi G T2.P.T1/q^2 is fixed by P1 (the field equation with 16 pi G)
   and the standard coupling (1/2) h_{mu nu} T^{mu nu}; with tpt = 1/2 for static masses this gives
   -4 pi G m1 m2/q^2, i.e. U = -4 pi G m1 m2 chiral.yukawa(r, 0), the SPEC connection. It is cross-checked
   by the position-space route U = -(1/2) m2 c^2 h00.
4. **Photon stress tensor** taken as T^00 = T^33 = E (null dust along z), as the blind check's (1,0,0,1).
5. **Equal masses.** entangling_phase(m, ...) uses m1 = m2 = m; branch separation 2y = dx s(t), so dx
   is the full branch separation during the hold (consistent with casimir's d_LR = sqrt(gap^2 + dx^2)).
6. design_phase uses the default n = 4001 (as the blind check's comparison does).

## desitter

1. **Epsilon sign convention for (cR, cV).** The contract does not fix the sign of eps_abcd. I take the
   plain permutation symbol (toolkit.levi_civita) for the LOWERED Lorentz symbol, eps_{0123} = +1, and
   eps~^{0123} = +1 for the coordinate density (4-form component on dt^dr^dth^dph). This gives
   (cR, cV) = (2, 24). The opposite convention (eps^{0123} = +1, lowered with eta) flips both to (-2, -24);
   the ratio cV/(4 cR) = 3 = Lambda l^2 is convention independent. Flagged for the cross-build comparison.
2. **"e R" normalization.** e = det(e^a_mu) (positive for the diagonal tetrad), R = R^{ab}_{mu nu} E_a^mu E_b^nu.
   cR is the ratio of the two literal contractions at the given geometry (numerically 2 to ~1e-15).
3. **so(4,1) components of F.** F = sum_{A<B} F^{AB} J_AB (equivalently (1/2) F^{AB} J_AB over all A, B), so
   F^{ab} = F^a_c eta^{cb} (Lorentz block) and F^{a4} = (F)^a_4. With this normalization F^{a4} = T^a/l
   exactly as SPEC states.
4. **mm_coupling** is returned as the positive ratio l^2/lP^2 = 3/(lP^2 Lambda) per the contract; the MM
   prefactor N itself is -l^2/(32 pi G cR) (sign set by the overall action sign), not exported.
5. **ell_from_lambda** uses the exact Fraction coefficients (from levi_civita contractions alone) rather than
   the finite-difference geometric ones, so it is exact (sensitivity tier requires 1e-12); action_coefficients
   is the geometric route and agrees to ~1e-15.

## blackholes

1. **Kerr first law with irrational a.** a = sqrt(pq) is not rational, so Omega and J are never formed.
   Only the quoted BCH S, T, Omega, J enter, through the exact rational combinations
   T dS = (T pi) d(S/pi), Omega J = a^2 M/(p^2 + a^2) and Omega dJ = (Omega/2J) d(J^2) = d(J^2)/(2M(p^2+a^2)),
   with directional derivatives along (dp, dq) by toolkit.exact_derivative. At q = 0 (Schwarzschild) along dq,
   dJ itself diverges but Omega dJ has the finite limit this formula gives; I take that limit as the meaning
   of the residual there (the blind check's q = 0 cases).
2. **Nariai degenerate point.** sds_horizons returns None when max f <= 0, including the exact Nariai
   double root (no static region). The bound is strict: horizons exist iff 27 M^2 < l^2.
3. **kappa_from_spin_connection needs fp.** desitter.spin_connection takes (f, fp). I pass fp as the exact
   derivative of the postulated rational f (toolkit.exact_derivative at Fraction(r), Fraction(M), Fraction(l)),
   not a hand-typed f'. The Killing route (killing_kappa) uses finite differences of f only, as SPEC requires.
4. **killing_kappa theta.** The metric is built at theta = pi/3 (generic); kappa is theta independent.
5. **Euclidean ratio endpoint.** After r = rh + u^2 the integrand is smooth and even in u but 0/0 at u = 0
   with f only; its endpoint value is extrapolated from two interior samples, (4g(du) - g(2du))/3. n = 401 samples.
6. **ISCO definition.** "The L^2 at which circular orbits first exist" = min over r > r_ph of
   L^2(r) = -f'/(f/r^2)' (V' linear in L^2), exact derivatives at Fraction(r). r_isco is polished with an
   exact symmetric difference (eta = 1e-6, bias ~1e-12 relative). E^2 = V(r_isco; L^2).
7. **Kerr area route.** r+ is solved by bisection of r^2 - 2r + chi^2 (horizons p, q with p + q = 2M, pq = a^2)
   and A = 4 pi (r+^2 + a^2) = 4 S_BCH; SPEC's 8 pi M^2 (1 + sqrt(1 - chi^2)) is the identity check.
   Marked derived; it leans on the horizon-area formula 4 pi (r+^2 + a^2) (equivalently the quoted S = A/4).
8. **Self-check conventions.** "Pull" = (prediction - measured)/sigma_meas with sigma on the side facing
   the prediction; the M87* theta_g also shows the prediction's own 1-sigma from the stellar mass error.
   Sgr A*: "average of VLTI and Keck" is taken as the mean of the two theta_g = GM/(c^2 D) values (not
   mean mass over mean distance; these differ slightly). GW250114: initial area uses central component
   masses at chi = 0; final area uses invert_220 of the central (F220, G220) at z = GW_Z[0]; the self-check
   also prints the range of A_final over the 1-sigma (f, gamma) box (a crude spread, not a posterior).
9. **qnm units.** The damping rate omega/(2Q) is in s^-1 (contract says "Hz"); the frequency is omega/(2 pi).
