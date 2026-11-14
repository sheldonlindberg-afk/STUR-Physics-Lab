"""Stage `toolkit` (build 2026-11-b): the shared numerical and exact tools.

Pure mathematics, standard library only; no measured input is used and nothing is quoted.
Derivations: DERIVATION_toolkit.md (same directory), section numbers cited below.
"""
import itertools
import math
import random
from fractions import Fraction

PROVENANCE = {
    "eigvalsh": ("derived", "cyclic Jacobi method: plane rotations with t = sgn(theta)/(|theta| + sqrt(theta^2+1)),"
                            " theta = (a_qq - a_pp)/(2 a_pq), each zeroing one off-diagonal entry; off-diagonal"
                            " norm falls by 2 a_pq^2 per rotation (DERIVATION section 1)"),
    "hessian": ("derived", "Taylor expansion: second central difference on the diagonal, four-point cross stencil"
                           " off the diagonal, absolute step h equal in all coordinates, error O(h^2)"
                           " (DERIVATION section 2)"),
    "exact_derivative": ("derived", "forward-mode dual numbers a + a' eps with eps^2 = 0 over fractions.Fraction;"
                                    " sum, product, quotient and integer-power rules follow from the algebra"
                                    " (DERIVATION section 3)"),
    "bisect": ("derived", "intermediate value theorem: halve a sign-changing bracket until it reaches floating-point"
                          " resolution (DERIVATION section 4)"),
    "golden_max": ("derived", "golden-section search for a unimodal maximum; ratio rho solves rho^2 + rho - 1 = 0 so"
                              " one interior point is reused each step (DERIVATION section 5)"),
    "trapezoid": ("derived", "integral of the piecewise-linear interpolant: dx [(y_0 + y_N)/2 + interior sum]"
                             " (DERIVATION section 6)"),
    "levi_civita": ("derived", "sign of a permutation from its cycle decomposition, (-1)^(n - cycles); 0 if an"
                               " index repeats (DERIVATION section 7)"),
}


# ------------------------------------------------------------------------------------------
# 1. Jacobi eigenvalues
# ------------------------------------------------------------------------------------------
def eigvalsh(A):
    """Eigenvalues of a real symmetric matrix (list of lists), ascending, by cyclic Jacobi rotations."""
    n = len(A)
    # work on the symmetrized copy (protects against rounding-level asymmetry in the caller's matrix)
    a = [[(float(A[i][j]) + float(A[j][i])) / 2 for j in range(n)] for i in range(n)]
    if n == 0:
        return []
    for _sweep in range(100):
        off = math.sqrt(sum(a[i][j] ** 2 for i in range(n) for j in range(n) if i != j))
        tot = math.sqrt(sum(a[i][j] ** 2 for i in range(n) for j in range(n)))
        if off == 0.0 or off <= 1e-18 * tot:
            break
        for p in range(n - 1):
            for q in range(p + 1, n):
                apq = a[p][q]
                if apq == 0.0:
                    continue
                theta = (a[q][q] - a[p][p]) / (2 * apq)
                if math.isinf(theta):
                    t = 0.0
                else:
                    t = 1 / (abs(theta) + math.hypot(theta, 1))
                    if theta < 0:
                        t = -t
                c = 1 / math.sqrt(1 + t * t)
                s = t * c
                tau = s / (1 + c)
                a[p][p] -= t * apq
                a[q][q] += t * apq
                a[p][q] = a[q][p] = 0.0
                for r in range(n):
                    if r != p and r != q:
                        arp, arq = a[r][p], a[r][q]
                        a[r][p] = a[p][r] = arp - s * (arq + tau * arp)
                        a[r][q] = a[q][r] = arq + s * (arp - tau * arq)
    return sorted(a[i][i] for i in range(n))


# ------------------------------------------------------------------------------------------
# 2. central-difference Hessian
# ------------------------------------------------------------------------------------------
def hessian(f, x, h=1e-4):
    """Central-difference Hessian of f: R^n -> R at x. The step h is absolute, the same in every coordinate."""
    n = len(x)
    x0 = [float(v) for v in x]

    def at(shifts):
        y = list(x0)
        for i, s in shifts:
            y[i] += s * h
        return f(y)

    f0 = f(list(x0))
    H = [[0.0] * n for _ in range(n)]
    for i in range(n):
        H[i][i] = (at([(i, 1)]) - 2 * f0 + at([(i, -1)])) / (h * h)
        for j in range(i + 1, n):
            v = (at([(i, 1), (j, 1)]) - at([(i, 1), (j, -1)])
                 - at([(i, -1), (j, 1)]) + at([(i, -1), (j, -1)])) / (4 * h * h)
            H[i][j] = H[j][i] = v
    return H


# ------------------------------------------------------------------------------------------
# 3. dual numbers over Fraction
# ------------------------------------------------------------------------------------------
class Dual:
    """a + a' eps with eps^2 = 0, both parts exact Fractions."""
    __slots__ = ("val", "der")

    def __init__(self, val, der=0):
        self.val = Fraction(val)
        self.der = Fraction(der)

    @staticmethod
    def _lift(o):
        if isinstance(o, Dual):
            return o
        if isinstance(o, bool) or not isinstance(o, (int, Fraction)):
            return None
        return Dual(o)

    def __add__(self, o):
        o = Dual._lift(o)
        return NotImplemented if o is None else Dual(self.val + o.val, self.der + o.der)

    __radd__ = __add__

    def __sub__(self, o):
        o = Dual._lift(o)
        return NotImplemented if o is None else Dual(self.val - o.val, self.der - o.der)

    def __rsub__(self, o):
        o = Dual._lift(o)
        return NotImplemented if o is None else Dual(o.val - self.val, o.der - self.der)

    def __mul__(self, o):
        o = Dual._lift(o)
        return NotImplemented if o is None else Dual(self.val * o.val, self.der * o.val + self.val * o.der)

    __rmul__ = __mul__

    def __truediv__(self, o):
        o = Dual._lift(o)
        if o is None:
            return NotImplemented
        return Dual(self.val / o.val, (self.der * o.val - self.val * o.der) / (o.val * o.val))

    def __rtruediv__(self, o):
        o = Dual._lift(o)
        return NotImplemented if o is None else o.__truediv__(self)

    def __pow__(self, n):
        if isinstance(n, Fraction) and n.denominator == 1:
            n = n.numerator
        if isinstance(n, bool) or not isinstance(n, int):
            return NotImplemented
        if n == 0:
            return Dual(1)
        return Dual(self.val ** n, n * self.val ** (n - 1) * self.der)

    def __neg__(self):
        return Dual(-self.val, -self.der)

    def __pos__(self):
        return self

    def __repr__(self):
        return f"Dual({self.val!r}, {self.der!r})"


def exact_derivative(f, x):
    """f'(x) exactly (a Fraction), for f built from + - * / (and integer powers) and rational constants."""
    y = f(Dual(Fraction(x), 1))
    if isinstance(y, Dual):
        return y.der
    return Fraction(0)          # f ignored its argument: a constant


# ------------------------------------------------------------------------------------------
# 4. bisection
# ------------------------------------------------------------------------------------------
def bisect(f, a, b, iters=200):
    """A root of f in [a, b]; needs a sign change, f(a) f(b) < 0 (an endpoint root is returned as is)."""
    lo, hi = float(a), float(b)
    flo, fhi = f(lo), f(hi)
    if flo == 0:
        return lo
    if fhi == 0:
        return hi
    if (flo > 0) == (fhi > 0):
        raise ValueError("bisect: f(a) and f(b) must have opposite signs")
    for _ in range(iters):
        mid = lo + (hi - lo) / 2
        if mid == lo or mid == hi:
            break
        fm = f(mid)
        if fm == 0:
            return mid
        if (fm > 0) == (flo > 0):
            lo, flo = mid, fm
        else:
            hi = mid
    return lo + (hi - lo) / 2


# ------------------------------------------------------------------------------------------
# 5. golden-section maximum
# ------------------------------------------------------------------------------------------
def golden_max(f, a, b, iters=200):
    """The maximizer of a unimodal f on [a, b]."""
    rho = (math.sqrt(5) - 1) / 2                 # root of rho^2 + rho - 1 = 0
    lo, hi = float(a), float(b)
    c = hi - rho * (hi - lo)
    d = lo + rho * (hi - lo)
    fc, fd = f(c), f(d)
    for _ in range(iters):
        if not (lo < c < d < hi):
            break
        if fc < fd:                              # maximum in [c, hi]
            lo, c, fc = c, d, fd
            d = lo + rho * (hi - lo)
            fd = f(d)
        else:                                    # maximum in [lo, d]
            hi, d, fd = d, c, fc
            c = hi - rho * (hi - lo)
            fc = f(c)
    return lo + (hi - lo) / 2


# ------------------------------------------------------------------------------------------
# 6. trapezoid rule
# ------------------------------------------------------------------------------------------
def trapezoid(ys, dx):
    """Trapezoid rule over equally spaced samples ys with spacing dx."""
    ys = list(ys)
    if len(ys) < 2:
        return 0.0
    return float(dx * (math.fsum(ys[1:-1]) + (ys[0] + ys[-1]) / 2))


# ------------------------------------------------------------------------------------------
# 7. permutation sign
# ------------------------------------------------------------------------------------------
def levi_civita(p):
    """Sign of the permutation p of 0..n-1: +1 even, -1 odd, 0 if p is not a permutation (repeated index)."""
    p = list(p)
    n = len(p)
    if sorted(p) != list(range(n)):
        return 0
    seen = [False] * n
    cycles = 0
    for i in range(n):
        if not seen[i]:
            cycles += 1
            j = i
            while not seen[j]:
                seen[j] = True
                j = p[j]
    return -1 if (n - cycles) % 2 else 1


# ------------------------------------------------------------------------------------------
# self-check: the independent second routes of DERIVATION_toolkit.md
# ------------------------------------------------------------------------------------------
def _det(M):
    """Determinant by Gaussian elimination with partial pivoting (works for floats and Fractions)."""
    a = [list(r) for r in M]
    n = len(a)
    det = 1
    for k in range(n):
        piv = max(range(k, n), key=lambda r: abs(a[r][k]))
        if a[piv][k] == 0:
            return 0 * det
        if piv != k:
            a[k], a[piv] = a[piv], a[k]
            det = -det
        det = det * a[k][k]
        for r in range(k + 1, n):
            m = a[r][k] / a[k][k]
            for c in range(k, n):
                a[r][c] -= m * a[k][c]
    return det


if __name__ == "__main__":
    rng = random.Random(7)
    ok_all = True

    def show(label, main, second, ok):
        global ok_all
        ok_all = ok_all and bool(ok)
        print(f"[{'ok' if ok else 'FAIL'}] {label}\n       main   : {main}\n       second : {second}")

    # 1. eigvalsh ---------------------------------------------------------------------------
    a_, b_, d_ = 2.0, -0.7, 0.5
    ev = eigvalsh([[a_, b_], [b_, d_]])
    r_ = math.sqrt(((a_ - d_) / 2) ** 2 + b_ ** 2)
    cf = [(a_ + d_) / 2 - r_, (a_ + d_) / 2 + r_]
    show("eigvalsh 2x2 vs closed form", ev, cf, max(abs(x - y) for x, y in zip(ev, cf)) < 1e-14)

    n = 7
    T = [[2.0 if i == j else (-1.0 if abs(i - j) == 1 else 0.0) for j in range(n)] for i in range(n)]
    ev = eigvalsh(T)
    cf = sorted(2 - 2 * math.cos(k * math.pi / (n + 1)) for k in range(1, n + 1))
    show("eigvalsh tridiag(-1,2,-1) vs 2 - 2cos(k pi/(n+1))", ev, cf, max(abs(x - y) for x, y in zip(ev, cf)) < 1e-13)

    n = 6
    R = [[rng.gauss(0, 1) for _ in range(n)] for _ in range(n)]
    S = [[R[i][j] + R[j][i] for j in range(n)] for i in range(n)]
    ev = eigvalsh(S)
    tr, tr2 = sum(S[i][i] for i in range(n)), sum(S[i][j] ** 2 for i in range(n) for j in range(n))
    scale = max(abs(x) for x in ev)
    charpoly = max(abs(_det([[S[i][j] - (lam if i == j else 0.0) for j in range(n)] for i in range(n)]))
                   for lam in ev) / scale ** n
    show("eigvalsh random 6x6: invariants (trace, trace of square, det(A - lambda) = 0)",
         f"sum {sum(ev):.13f}  sum sq {sum(x * x for x in ev):.12f}",
         f"tr  {tr:.13f}  tr A^2 {tr2:.12f}  max |det(A - lambda I)|/scale^n = {charpoly:.1e}",
         abs(sum(ev) - tr) < 1e-12 and abs(sum(x * x for x in ev) - tr2) < 1e-11 and charpoly < 1e-12)

    # 2. hessian ----------------------------------------------------------------------------
    fq = lambda x: math.exp(x[0] * x[1]) + math.sin(x[2]) * x[0] ** 2 + x[1] / (1 + x[2] ** 2)
    x0 = [0.4, -0.3, 0.8]
    H = hessian(fq, x0)
    h_ = 1e-3
    H1, H2 = hessian(fq, x0, h_), hessian(fq, x0, 2 * h_)
    Rich = [[(4 * H1[i][j] - H2[i][j]) / 3 for j in range(3)] for i in range(3)]
    e_, s_, c_ = math.exp(x0[0] * x0[1]), math.sin(x0[2]), math.cos(x0[2])
    q_ = 1 + x0[2] ** 2
    An = [[x0[1] ** 2 * e_ + 2 * s_, (1 + x0[0] * x0[1]) * e_, 2 * x0[0] * c_],
          [(1 + x0[0] * x0[1]) * e_, x0[0] ** 2 * e_, -2 * x0[2] / q_ ** 2],
          [2 * x0[0] * c_, -2 * x0[2] / q_ ** 2, -s_ * x0[0] ** 2 + x0[1] * (8 * x0[2] ** 2 / q_ ** 3 - 2 / q_ ** 2)]]
    dR = max(abs(H[i][j] - Rich[i][j]) for i in range(3) for j in range(3))
    dA = max(abs(H[i][j] - An[i][j]) for i in range(3) for j in range(3))
    show("hessian vs Richardson-extrapolated stencil and analytic second derivatives",
         [[round(v, 7) for v in row] for row in H],
         f"Richardson max diff {dR:.1e}; analytic max diff {dA:.1e}", dR < 1e-6 and dA < 1e-6)

    # 3. exact_derivative -------------------------------------------------------------------
    poly = lambda x: 3 * x ** 4 - x ** 3 / 7 + 5 * x - 2
    xq, hq = Fraction(5, 3), Fraction(1, 11)
    d1 = exact_derivative(poly, xq)
    d2 = (poly(xq - 2 * hq) - 8 * poly(xq - hq) + 8 * poly(xq + hq) - poly(xq + 2 * hq)) / (12 * hq)
    show("exact_derivative of a quartic vs exact 5-point interpolation stencil (no derivative rules)",
         repr(d1), repr(d2), d1 == d2 and isinstance(d1, Fraction))
    rat = lambda x: (x * x - 1 / (x + 2)) / (1 + x ** 3) - 2 / x
    d1 = exact_derivative(rat, xq)
    u, up = xq * xq - 1 / (xq + 2), 2 * xq + 1 / (xq + 2) ** 2
    w, wp = 1 + xq ** 3, 3 * xq ** 2
    d2 = (up * w - u * wp) / w ** 2 + 2 / xq ** 2
    hq = Fraction(1, 10 ** 8)
    d3 = (rat(xq + hq) - rat(xq - hq)) / (2 * hq)
    show("exact_derivative of a rational function vs hand quotient rule and exact symmetric quotient",
         repr(d1), f"{d2!r}; symmetric quotient differs by {float(abs(d3 - d1)):.1e}",
         d1 == d2 and abs(d3 - d1) < Fraction(1, 10 ** 12))

    # 4. bisect -----------------------------------------------------------------------------
    g = lambda x: x ** 3 - 2 * x - 5
    r1 = bisect(g, 2.0, 3.0)
    xn = 2.0
    for _ in range(50):
        xn -= g(xn) / float(exact_derivative(g, Fraction(xn)))
    show("bisect root of x^3 - 2x - 5 vs Newton iteration (slope from exact_derivative)", r1, xn, abs(r1 - xn) < 1e-14)
    r1 = bisect(lambda x: math.cos(x) - x, 0.0, 1.0)
    xn = 1.0
    for _ in range(200):
        xn = math.cos(xn)
    show("bisect root of cos x = x vs fixed-point iteration", r1, xn, abs(r1 - xn) < 1e-14)

    # 5. golden_max -------------------------------------------------------------------------
    fm = lambda x: x * math.exp(-x)
    m1 = golden_max(fm, 0.0, 5.0)
    m2 = bisect(lambda x: (1 - x) * math.exp(-x), 0.0, 5.0)
    show("golden_max of x exp(-x) vs bisection on f' (and closed form 1)", m1, m2, abs(m1 - m2) < 1e-7)
    fm = lambda x: x ** 3 - 4 * x ** 4
    m1 = golden_max(fm, 0.0, 1.0)
    m2 = bisect(lambda x: float(exact_derivative(fm, Fraction(x))), 0.1, 1.0)
    show("golden_max of x^3 - 4x^4 vs bisection on the exact derivative", m1, m2, abs(m1 - m2) < 1e-7)

    # 6. trapezoid --------------------------------------------------------------------------
    N = 2001
    dx = math.pi / (N - 1)
    ys = [math.sin(i * dx) for i in range(N)]
    T1 = trapezoid(ys, dx)
    T2 = trapezoid(ys[::2], 2 * dx)
    simpson = (4 * T1 - T2) / 3
    show("trapezoid int_0^pi sin vs Simpson (Richardson) and the Euler-Maclaurin error -dx^2/6",
         f"{T1:.12f}  (error {T1 - 2:.4e})", f"{simpson:.12f}  (predicted error {-dx * dx / 6:.4e})",
         abs(simpson - 2) < 1e-11 and abs((T1 - 2) / (-dx * dx / 6) - 1) < 1e-5)
    ys = [3 * i * Fraction(1, 4) - 1 for i in range(9)]
    show("trapezoid of a linear integrand is exact", trapezoid(ys, 1 / 4), float(3 * 2 * 2 / 2 - 2),
         trapezoid(ys, 1 / 4) == 3 * 2 * 2 / 2 - 2)

    # 7. levi_civita ------------------------------------------------------------------------
    agree, total = True, 0
    for nn in range(1, 6):
        s = 0
        for p in itertools.permutations(range(nn)):
            inv = sum(1 for i in range(nn) for j in range(i + 1, nn) if p[i] > p[j])
            agree = agree and levi_civita(p) == (-1) ** inv
            s += levi_civita(p)
            total += 1
        agree = agree and (s == 0 or nn == 1)
    show("levi_civita (cycles) vs inversion count, all permutations n <= 5", f"{total} permutations", f"agree: {agree}",
         agree and levi_civita([2, 2, 0]) == 0 and isinstance(levi_civita([1, 0]), int))
    M = [[Fraction(rng.randint(-5, 5), rng.randint(1, 4)) for _ in range(4)] for _ in range(4)]
    leib = sum(levi_civita(p) * M[0][p[0]] * M[1][p[1]] * M[2][p[2]] * M[3][p[3]] for p in itertools.permutations(range(4)))
    show("Leibniz determinant with levi_civita vs Gaussian elimination (exact Fractions)", repr(leib), repr(_det(M)),
         leib == _det(M))

    print("\nSELF-CHECK:", "all second routes agree" if ok_all else "DISAGREEMENT")
