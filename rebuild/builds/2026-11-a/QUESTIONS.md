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
