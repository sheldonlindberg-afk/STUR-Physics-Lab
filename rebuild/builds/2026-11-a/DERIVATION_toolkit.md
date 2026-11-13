# DERIVATION: toolkit (SPEC.md section 1)

The toolkit has no physics postulates; it rests on SPEC.md section 1 ("standard library only;
Jacobi eigenvalue solver, central-difference Hessian, forward-mode dual numbers over
`fractions.Fraction`, bisection, golden-section search, trapezoid rule, permutation parity")
and on the signatures in `contract.py`. It reads nothing from `inputs.py`. The only numbers
in the code are structural (0, 1, 2, 4, 1/2, sweep limits, the default step 1e-4 fixed by the
contract); machine epsilon is obtained at run time as `math.ulp(1.0)`.

Notation: eps = 2^-52 (unit roundoff u = eps/2), ||A||_F the Frobenius norm.

---

## 1. `eigvalsh(A)`: cyclic Jacobi

**Method.** For a real symmetric n x n matrix A, repeatedly apply plane rotations
A <- J^T A J, J = J(p, q, theta), each chosen to annihilate one off-diagonal pair a_pq = a_qp.

Restricted to the (p, q) plane, with c = cos theta, s = sin theta,

    [a'_pp a'_pq]   [c -s][a_pp a_pq][ c s]
    [a'_pq a'_qq] = [s  c][a_pq a_qq][-s c]

and a'_pq = (c^2 - s^2) a_pq + cs (a_pp - a_qq). Setting a'_pq = 0 gives
cot 2theta = (a_qq - a_pp)/(2 a_pq) =: tau. With t = tan theta, t^2 + 2 tau t - 1 = 0, and we take
the root of smaller modulus (|theta| <= pi/4, which guarantees convergence):

    t = sign(tau) / (|tau| + sqrt(1 + tau^2))      (sign(0) := +1),
    c = 1/sqrt(1 + t^2),  s = t c.

For |tau| so large that tau^2 overflows we use t = 1/(2 tau) (the leading term). The updates
are written in Rutishauser's stable form, with tau_r = s/(1 + c):

    a'_pp = a_pp - t a_pq,   a'_qq = a_qq + t a_pq,   a'_pq = 0,
    a'_rp = a_rp - s (a_rq + tau_r a_rp),   a'_rq = a_rq + s (a_rp - tau_r a_rq)   (r != p, q).

These follow from expanding the rotation and using the defining equation for t: e.g.
a'_pp = c^2 a_pp - 2cs a_pq + s^2 a_qq = a_pp - t a_pq once t^2 + 2 tau t = 1 is used.

**Why it is correct.** The orthogonal similarity preserves eigenvalues and ||A||_F, and each
rotation moves exactly 2 a_pq^2 of off-diagonal weight onto the diagonal:
off(A')^2 = off(A)^2 - 2 a_pq^2. Over a full cyclic sweep this gives (asymptotically)
quadratic convergence of off(A) -> 0 (Henrici; Forsythe-Henrici for |theta| <= pi/4). When
off(A) = 0 the diagonal is the spectrum; we return it sorted ascending.

**Stopping rule (robust to wide dynamic range).** Within a sweep, an element is set to zero
without rotating if it is negligible next to *both* diagonal entries it couples:
|a_pp| + 100|a_pq| == |a_pp| and |a_qq| + 100|a_pq| == |a_qq| in floating point (Rutishauser).
Additionally an element with |a_pq| <= u^2 * ||A||_F (below anything that can change any
eigenvalue at the backward-error level, eps ||A||) is set to zero; this makes exact zero
modes, whose diagonal entries tend to 0, stop rotating instead of chasing denormals. The
iteration stops when a sweep finds every off-diagonal element negligible (or after 100
sweeps, far beyond the ~6-10 that convergence needs; non-convergence raises).

**Error behaviour.** Each rotation is backward stable: the computed matrix is an exact
orthogonal similarity of A + E, ||E|| = O(eps ||A||) per sweep. By Weyl's inequality every
computed eigenvalue is within O(n eps ||A||) of the exact one. Therefore an exact zero mode
of a 9x9 matrix comes out at |lambda| <~ 10 eps max|lambda| ~ 1e-15 relative, below the
required 1e-12 regardless of how small the other nonzero eigenvalues are. (Jacobi is in
addition known to give small eigenvalues to high *relative* accuracy for scaled-diagonally-
dominant matrices — Demmel-Veselic — which the Rutishauser threshold preserves, since it
only discards a_pq that is negligible relative to the *local* diagonal entries, not to
||A||.) Caveat: for a matrix that is *not* graded (a rotated one), a nonzero eigenvalue
far below eps ||A|| is only determined to absolute accuracy ~eps ||A||; the self-check
shows a 1e-15-relative eigenvalue coming out at ~1e-15 with O(1) relative error, exactly as
Weyl predicts. Zero-mode *detection* (|lambda| < 1e-12 max) is unaffected. Input is symmetrized as (A + A^T)/2 and converted to float; a non-square input raises.

**Second route.** (i) Trace and Frobenius invariants: sum lambda = tr A, sum lambda^2 =
||A||_F^2. (ii) For each computed lambda, det(A - lambda I) by Gaussian elimination with
partial pivoting changes sign across lambda +/- delta (Sylvester inertia count: the number
of negative pivots of LDL^T of A - sigma I equals the number of eigenvalues below sigma).
(iii) Known spectra: rotated diag(1,2,3,4); a 9x9 rotated diag with entries spanning 1e-15..1
plus exact zeros; the graded matrix diag(10^k) with small couplings.

---

## 2. `hessian(f, x, h=1e-4)`: central differences

**Method.** Taylor expand f(x + a e_i + b e_j) to fourth order. Then

    H_ii ~ [f(x + h e_i) - 2 f(x) + f(x - h e_i)] / h^2
         = f_ii + (h^2/12) f_iiii + O(h^4),
    H_ij ~ [f(++) - f(+-) - f(-+) + f(--)] / (4 h^2),  (+- means x + h e_i - h e_j, etc.)
         = f_ij + (h^2/6)(f_iiij + f_ijjj) + O(h^4).

The odd-order terms cancel by the symmetry of the stencils. H_ji is set equal to H_ij, so
the result is exactly symmetric (needed for `eigvalsh`). Cost 1 + 2n + 4 n(n-1)/2 calls.

**Error behaviour.** Truncation O(h^2 f^(4)); roundoff O(eps |f| / h^2). At the default
h = 1e-4 that is ~1e-8 |f^(4)| + ~1e-8 |f|, consistent with the blind check's 1e-5. The
self-check confirms both: Richardson ratio err(h)/err(h/2) = 4.000 for e^x sin y at
h = 1e-2, and at h = 1e-4 the cubic test is off by ~3e-7 on H_yy = 12, which is the roundoff
term eps |f| / h^2 ~ 2e-16 * 9 / 1e-8 (the truncation term is zero for a cubic). The
step h is absolute (contract signature); callers whose coordinates are not O(1) must pass
an appropriate h. For polynomials of degree <= 3 the truncation error vanishes identically.

**Second route.** Richardson: compute with h and h/2; the difference must shrink by ~4
(second order). Also exact comparison on a cubic, whose Hessian is known in closed form,
and comparison with `exact_derivative` applied twice through dual numbers on a rational f.

---

## 3. `exact_derivative(f, x)`: forward-mode dual numbers over Fraction

**Method.** Work in the ring Q[e]/(e^2): a dual number a + b e with a, b in Q (Fractions).
For any rational function f built from + - * /, f(x + e) = f(x) + f'(x) e exactly, because the
ring operations encode the differentiation rules:

    (a + b e) + (c + d e) = (a + c) + (b + d) e                     (sum rule)
    (a + b e)(c + d e)    = ac + (ad + bc) e        (e^2 = 0)        (product rule)
    1/(c + d e)           = 1/c - (d/c^2) e         (c != 0)        (from (c + d e)(1/c - d e/c^2) = 1)
    (a + b e)/(c + d e)   = a/c + (bc - ad)/c^2 e                    (quotient rule)
    (a + b e)^n           = a^n + n a^(n-1) b e     (integer n, incl. n <= 0, a != 0 if n < 0)

Constants (int, Fraction) embed as c + 0 e. Every reflected form is implemented
(c + X, c - X, c * X, c / X, -X, +X), so `1/x`, `2 - x`, `Fraction(1,3) * x` all work.
By induction on the expression tree, the e-part of the result equals the derivative of the
expression at x. All arithmetic is in `fractions.Fraction`, so the result is exact; it is
returned as a `Fraction` (a constant f gives Fraction(0)).

Floats are rejected (TypeError): mixing a float in would silently destroy exactness, which
is the whole point of this export. Division by a dual whose real part is 0 raises
ZeroDivisionError (f is not defined there). Comparisons (<, ==, ...) act on the real part, so
piecewise-defined f differentiate correctly away from branch points.

**Error behaviour.** None: the result is exact (no truncation, no roundoff).

**Second route.** Exact symmetric difference quotients in Fraction arithmetic,
D(h) = [f(x+h) - f(x-h)]/(2h) = f'(x) + f'''(x) h^2/6 + ..., with h = 10^-k: |D(h) - f'| must
fall by ~100 per k. Also the closed-form quotient rule for the blind check's
(x^3 + 1)/(x - 3) at x = 2: f' = [3x^2(x-3) - (x^3+1)]/(x-3)^2 = -21.

---

## 4. `bisect(f, a, b, iters=200)`

**Method.** With f(a) f(b) < 0 and f continuous, the intermediate value theorem guarantees a
root in [a, b]. Take m = a + (b - a)/2; keep the half on which f changes sign. If f hits 0
exactly at an endpoint or midpoint, return that point. Stop after `iters` halvings or when m
equals an endpoint in floating point (the bracket is then two adjacent doubles).

**Error behaviour.** After k steps the bracket has width (b - a)/2^k; the returned midpoint
is within half of that of a root. 200 steps exhaust double precision for any bracket
(2^-200 << eps), so the result is accurate to ~1 ulp of the root (limited only by the
accuracy of the sign of f near the root). No sign change raises ValueError.

**Second route.** Newton's iteration (or the closed form) on test functions, e.g. x^2 - 2
on [0, 2] vs sqrt(2); and the residual |f(r)| ~ |f'(r)| ulp(r).

---

## 5. `golden_max(f, a, b, iters=200)`

**Method.** Golden-section search for the maximizer of a unimodal f. Interior points
c = b - r(b - a), d = a + r(b - a), r = (sqrt5 - 1)/2 (root of r^2 + r - 1 = 0, computed).
If f(c) >= f(d) the maximizer lies in [a, d] (unimodality), else in [c, b]. Because
r^2 = 1 - r, the surviving interior point is exactly one of the new interior points, so each
step costs one evaluation and shrinks the bracket by r ~ 0.618. Return the midpoint of the
final bracket. Stop early when the bracket no longer shrinks in floating point.

**Error behaviour.** Bracket width (b - a) r^k (r^200 ~ 1e-42, i.e. exhausted). The true
limit is the flatness of f at the max: comparisons of f(c), f(d) are meaningless once
|f(c) - f(d)| ~ eps |f|, i.e. |x - x*| ~ sqrt(2 eps |f(x*)| / |f''(x*)|). For a maximum with
f(x*) = 0 this is tiny; in general expect ~sqrt(eps) ~ 1e-8 relative.

**Second route.** Bisection on a central-difference derivative f'(x) ~ [f(x+h)-f(x-h)]/2h,
whose root is the maximizer (and is not limited by sqrt(eps) in the same way); and closed
forms, e.g. -(x - 0.3)^2.

---

## 6. `trapezoid(ys, dx)`

**Method.** Integrating the piecewise-linear interpolant of equally spaced samples:
I = dx [y_0/2 + y_1 + ... + y_(n-1) + y_n/2]. Summed with `math.fsum` (correctly rounded sum).
Fewer than two samples give 0.

**Error behaviour.** Euler-Maclaurin: I - int = (dx^2/12)[f'(b) - f'(a)] - (dx^4/720)[f'''(b) -
f'''(a)] + ..., so O(dx^2) in general, and spectrally accurate for smooth periodic integrands
over a period. For int_0^pi sin with n = 2001: error ~ (pi/2000)^2/12 * 2 ~ 4e-7.

**Second route.** Richardson/Romberg: (4 T(dx/2) - T(dx))/3 is Simpson's rule, O(dx^4); the
difference T(dx) - T(dx/2) must shrink by ~4 per halving; closed forms (int sin = 2,
polynomials of degree <= 1 integrated exactly).

---

## 7. `levi_civita(p)`

**Method.** For p a sequence of n integers: if any entry repeats or lies outside 0..n-1,
return 0 (the Levi-Civita symbol vanishes on repeated indices). Otherwise p is a permutation;
decompose it into disjoint cycles. A cycle of length L is a product of L - 1 transpositions,
so sign(p) = (-1)^(n - #cycles).

**Error behaviour.** Exact integer arithmetic.

**Second route.** Count inversions #{i < j : p_i > p_j}; sign = (-1)^inversions. Verified
for all permutations of 0..4 in the self-check, plus multiplicativity sign(p o q) = sign(p)
sign(q).

---

## Things not derived / judgement calls

None of the toolkit rests on a quoted result. Judgement calls are listed in QUESTIONS.md
(absolute Hessian step, rejection of floats in dual numbers, input symmetrization).
