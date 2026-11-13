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
