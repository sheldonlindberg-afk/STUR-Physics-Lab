# DERIVATION: stage `toolkit` (build 2026-11-b)

Postulates: SPEC.md section 1 ("toolkit") and section 0 (layers). The stage is pure mathematics:
no measured input is used, nothing is quoted. Every export is `derived`. The only convention
is SPEC section 1: *the Hessian step h is absolute and the same in every coordinate*.

Written before the code. Each export: (a) what it rests on, (b) derivation, (c) closed form,
(d) the independent second route used in `toolkit.py`'s `__main__` self-check.

---------------------------------------------------------------------------------------------
## 1. `eigvalsh(A)`: Jacobi eigenvalue method

**Rests on:** the spectral theorem for a real symmetric A (A = Q D Q^T, Q orthogonal), and
invariance of the spectrum under A -> J^T A J for orthogonal J.

**Derivation.** Take a plane rotation J in the (p,q) plane, c = cos t, s = sin t, with
J_pp = J_qq = c, J_pq = s, J_qp = -s. For A' = J^T A J:

    a'_pq = (c^2 - s^2) a_pq + c s (a_pp - a_qq).

Demand a'_pq = 0. With t = tan t and theta = (a_qq - a_pp) / (2 a_pq):

    cot 2t = (c^2 - s^2)/(2cs) = theta   =>   t^2 + 2 theta t - 1 = 0
    t = -theta +- sqrt(theta^2 + 1).

Choose the root of smaller modulus (|t| <= 1, rotation angle <= pi/4), written without
cancellation as

    t = sgn(theta) / (|theta| + sqrt(theta^2 + 1)),   c = 1/sqrt(1 + t^2),   s = t c.

Updates (using a'_pq = 0 to eliminate, tau = s/(1+c)):

    a'_pp = a_pp - t a_pq,     a'_qq = a_qq + t a_pq,     a'_pq = 0,
    a'_rp = a_rp - s (a_rq + tau a_rp),   a'_rq = a_rq + s (a_rp - tau a_rq)   (r != p,q).

Check of a'_pp: a'_pp = c^2 a_pp - 2cs a_pq + s^2 a_qq; substitute a_qq - a_pp = 2 theta a_pq
= a_pq (c^2 - s^2)/(cs): a'_pp = a_pp + s^2 (a_qq - a_pp) - 2cs a_pq
= a_pp + a_pq [ s(c^2 - s^2)/c - 2cs ] = a_pp - a_pq (s/c)(s^2 + c^2) = a_pp - t a_pq.  OK.

**Convergence.** The Frobenius norm is invariant, and the rotation only mixes rows/columns
p,q, so sum of squares of the off-diagonal entries S = sum_{i != j} a_ij^2 obeys

    S' = S - 2 a_pq^2

(strictly decreasing). Cyclic sweeps over all p<q converge (quadratically, asymptotically) to
a diagonal matrix whose diagonal is the spectrum. Stop when S is zero to rounding relative to
the Frobenius norm; return the diagonal sorted ascending.

**Closed form:** none for general n (it is an iteration); for n = 2 one rotation is exact:
lambda = (a+d)/2 +- sqrt(((a-d)/2)^2 + b^2).

**Second route.** (i) The 2x2 closed form above. (ii) Invariants that never use the rotation
formula: sum(lambda) = tr A, sum(lambda^2) = tr A^2 = ||A||_F^2, and the characteristic
polynomial det(A - lambda I) evaluated by Gaussian elimination must vanish at each returned
eigenvalue (relative to the product scale). (iii) A matrix with a known spectrum: the
second-difference matrix tridiag(-1, 2, -1) of size n has lambda_k = 2 - 2 cos(k pi/(n+1)),
which follows from the eigenvectors sin(j k pi/(n+1)) and the sine addition formula.

---------------------------------------------------------------------------------------------
## 2. `hessian(f, x, h=1e-4)`: central differences

**Rests on:** Taylor's theorem; SPEC section 1 convention (absolute h, same in every coordinate).

**Derivation.** Expand f about x with e_i the unit vectors, d_i = partial_i.

Diagonal:  f(x +- h e_i) = f +- h d_i f + (h^2/2) d_i^2 f +- (h^3/6) d_i^3 f + (h^4/24) d_i^4 f + ...

    H_ii = [ f(x + h e_i) - 2 f(x) + f(x - h e_i) ] / h^2  =  d_i^2 f + (h^2/12) d_i^4 f + O(h^4).

Off-diagonal: with f(s1, s2) = f(x + s1 h e_i + s2 h e_j), all terms even in either sign cancel
in the combination f(+,+) - f(+,-) - f(-,+) + f(-,-), leaving 4 h^2 d_i d_j f + O(h^4):

    H_ij = [ f(++) - f(+-) - f(-+) + f(--) ] / (4 h^2)
         = d_i d_j f + (h^2/6)(d_i^3 d_j + d_i d_j^3) f + O(h^4).

The formula is symmetric under i <-> j, so compute i < j and mirror.

**Error budget.** Truncation O(h^2 f''''); rounding ~ eps |f| / h^2. At h = 1e-4 and
f = O(1): truncation ~ 1e-8, rounding ~ 1e-8. **Exact (up to rounding) for polynomials of
degree <= 3**, because both error terms contain fourth derivatives.

**Second route.** (i) A quadratic form f = x^T M x / 2 + b.x has Hessian exactly M
(sym. part); a cubic has an analytic Hessian. (ii) Independent numerical method: Richardson
extrapolation (4 H(h) - H(2h))/3 cancels the h^2 term; and for a rational f the diagonal
second derivative is obtained exactly from nested dual numbers / the exact first derivative
(section 3) differenced once, which shares no formula with the second-difference stencil.

---------------------------------------------------------------------------------------------
## 3. `exact_derivative(f, x)`: forward-mode dual numbers over Fraction

**Rests on:** the algebra Q[eps]/(eps^2). For any rational function f with f regular at a,
f(a + b eps) = f(a) + f'(a) b eps (Taylor's theorem truncates exactly because eps^2 = 0).

**Derivation of the arithmetic.** Elements (a, a') = a + a' eps, a, a' in Q.

    (a + a' eps) +- (b + b' eps) = (a +- b) + (a' +- b') eps
    (a + a' eps)(b + b' eps)     = ab + (a' b + a b') eps                     [eps^2 = 0]
    1/(b + b' eps)               = (1/b)(1 - (b'/b) eps)                      [b != 0]
    (a + a' eps)/(b + b' eps)    = a/b + ((a' b - a b')/b^2) eps
    (a + a' eps)^n               = a^n + n a^(n-1) a' eps                     [n integer, by induction;
                                                                               n<0 via the reciprocal]

These are the sum, product (Leibniz), quotient and power rules. By induction on the
expression tree of f, f((x, 1)) = (f(x), f'(x)). All arithmetic is in `fractions.Fraction`, so
the result is exact. Constants (int, Fraction) embed as (c, 0). If f returns a plain number
(a constant function), the derivative is 0.

**Closed form:** f'(x) = eps-coefficient of f(x + eps).

**Second route.** (i) Hand differentiation of test functions with the quotient rule, in exact
Fractions. (ii) An independent exact method that uses no differentiation rules at all:
polynomial interpolation. For a polynomial of degree <= 4 the 5-point stencil
[f(x-2h) - 8 f(x-h) + 8 f(x+h) - f(x+2h)]/(12h) is exact in rational arithmetic (its error
term is h^4 f^(5)/30); for a general rational f, the symmetric quotient
[f(x+h) - f(x-h)]/(2h) in exact Fractions with h = 10^-k converges as h^2.

---------------------------------------------------------------------------------------------
## 4. `bisect(f, a, b, iters=200)`

**Rests on:** the intermediate value theorem: f continuous, f(a) f(b) < 0 => a root in (a,b).

**Derivation.** Keep a bracket [lo, hi] with sign f(lo) != sign f(hi). m = (lo+hi)/2; if
f(m) = 0 return m; else replace the endpoint whose sign equals sign f(m). Invariant: the
bracket contains a root; width_k = (b-a)/2^k. In binary floating point the width stops halving
after ~53 + log2((b-a)/|root|) steps, when m coincides with an endpoint; iterating up to
`iters` (default 200) therefore reaches the last-bit bracket. Return the midpoint.
If f(a) = 0 or f(b) = 0 return that endpoint; if f(a) f(b) > 0 raise ValueError (precondition
violated; no silent answer).

**Closed form:** |error| <= (b-a)/2^(iters+1) until rounding.

**Second route.** Roots known in closed form (x^2 = 2); and a different numerical method,
Newton's iteration x <- x - f/f' with f' from `exact_derivative`-style analytic slope, which
shares nothing with bracketing.

---------------------------------------------------------------------------------------------
## 5. `golden_max(f, a, b, iters=200)`

**Rests on:** unimodality: f strictly increasing left of x*, strictly decreasing right of it.
Then for a < c < d < b: f(c) < f(d) => x* in [c, b]; f(c) >= f(d) => x* in [a, d].

**Derivation of the ratio.** Place interior points symmetrically, c = b - rho (b-a),
d = a + rho (b-a), 1/2 < rho < 1. After discarding [a,c) the new interval [c,b] has length
rho (b-a) and the surviving point d should be the new *left* interior point:

    d = b - rho * rho (b-a)   <=>   a + rho(b-a) = b - rho^2 (b-a)   <=>   rho^2 + rho - 1 = 0
    rho = (sqrt(5) - 1)/2    (the inverse golden ratio; computed, not typed).

(The mirror case gives the same equation.) One new function evaluation per step; the bracket
shrinks by rho each step: width_k = rho^k (b-a).

**Accuracy limit.** Near a smooth maximum f(x) ~ f* - (1/2)|f''|(x-x*)^2, so points closer
than ~ sqrt(eps |f*|/|f''|) are indistinguishable in floating point: the abscissa is good to
~1e-8 relative, not 1e-16. The iteration stops early when the two interior points coincide.
Returns the bracket midpoint.

**Second route.** (i) Closed-form maximizers (vertex of a parabola; x e^{-x} at x = 1).
(ii) A different method: the maximizer is the root of f', found with `bisect` on the analytic
derivative.

---------------------------------------------------------------------------------------------
## 6. `trapezoid(ys, dx)`

**Rests on:** piecewise-linear interpolation between equally spaced samples y_0..y_{N}.

**Derivation.** On one panel the linear interpolant integrates to dx (y_i + y_{i+1})/2. Sum:

    T = dx [ (y_0 + y_N)/2 + sum_{i=1}^{N-1} y_i ].

Error (Euler-Maclaurin): T - I = (dx^2/12) [f'(b) - f'(a)] + O(dx^4). Fewer than two samples
span no interval: T = 0. The interior sum uses `math.fsum` (exactly rounded sum) so the result
does not depend on the order of accumulation.

**Second route.** (i) Exact for linear integrands; for int_0^pi sin = 2 the leading error is
(dx^2/12)(cos pi - cos 0) = -dx^2/6, so the *size* of the error is itself predicted. (ii) A
different rule on the same samples: Simpson = (4 T(dx) - T(2 dx))/3 (Richardson), error
O(dx^4).

---------------------------------------------------------------------------------------------
## 7. `levi_civita(p)`

**Rests on:** the sign homomorphism S_n -> {+1,-1}; sgn of a k-cycle is (-1)^(k-1).

**Derivation.** If p is not a bijection of {0..n-1} (a repeated index), the totally
antisymmetric symbol vanishes: return 0. Otherwise decompose p into disjoint cycles; a cycle of
length k is a product of k-1 transpositions, so

    sgn(p) = (-1)^(n - #cycles).

Returned as a Python int (exact).

**Second route.** Count inversions: sgn(p) = (-1)^(#{i<j : p_i > p_j}) (each adjacent swap in
a bubble sort changes the inversion count by exactly 1). Checked against the cycle formula
over every permutation of n <= 5, together with sum over S_n of sgn = 0 (n >= 2) and the
determinant identity det(A) = sum_p sgn(p) prod_i A[i][p_i] against Gaussian elimination.

---------------------------------------------------------------------------------------------
## Not derived / open items

Nothing in this stage is quoted or left underived. Choices where the contract is silent are
listed in QUESTIONS.md (return value at the end of bisection/golden section; behaviour on
invalid brackets; trapezoid with < 2 samples; integer type returned by `levi_civita`).
