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
