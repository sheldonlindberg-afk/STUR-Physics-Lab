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
