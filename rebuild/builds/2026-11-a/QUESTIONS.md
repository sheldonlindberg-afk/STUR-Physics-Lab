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
