"""toolkit: numerical and exact building blocks shared by every later stage.

Derivations, error behaviour and second routes: DERIVATION_toolkit.md (SPEC.md section 1).
Standard library only; reads nothing from inputs.py (there is nothing physical here).
"""
import math
from fractions import Fraction

PROVENANCE = {
    "eigvalsh": ("derived", "cyclic Jacobi rotations, t = sgn(tau)/(|tau|+sqrt(1+tau^2)), tau = cot 2theta ="
                            " (a_qq-a_pp)/(2a_pq), Rutishauser updates; off(A)^2 drops by 2a_pq^2 per rotation;"
                            " negligibility test relative to local diagonal; backward stable, errors O(n eps ||A||)"),
    "hessian": ("derived", "central differences from 4th-order Taylor expansion: H_ii = (f+ - 2f0 + f-)/h^2,"
                           " H_ij = (f++ - f+- - f-+ + f--)/(4h^2), odd orders cancel, error O(h^2), symmetric"),
    "exact_derivative": ("derived", "forward-mode dual numbers a + b e, e^2 = 0, over Fraction: ring operations"
                                    " encode sum/product/quotient rules, so f(x+e) = f(x) + f'(x) e exactly"),
    "bisect": ("derived", "intermediate value theorem; halve the sign-change bracket; width (b-a)/2^k,"
                          " stops when the bracket is two adjacent doubles"),
    "golden_max": ("derived", "golden-section search, r = (sqrt5-1)/2 solves r^2 + r - 1 = 0 so one interior"
                              " point is reused; unimodality keeps the maximizer in the bracket; width (b-a) r^k"),
    "trapezoid": ("derived", "integral of the piecewise-linear interpolant, dx[y0/2 + y1 + ... + yn/2],"
                             " Euler-Maclaurin error O(dx^2); fsum for the sum"),
    "levi_civita": ("derived", "0 on repeated/out-of-range index, else sign = (-1)^(n - number of cycles),"
                               " each L-cycle being L-1 transpositions"),
}

_EPS = math.ulp(1.0)          # machine epsilon, 2^-52, obtained at run time


# ------------------------------------------------------------------------------------------
# 1. eigenvalues of a real symmetric matrix: cyclic Jacobi
# ------------------------------------------------------------------------------------------
def eigvalsh(A, max_sweeps=100):
    """Eigenvalues of a real symmetric matrix (list of lists), ascending."""
    n = len(A)
    if any(len(row) != n for row in A):
        raise ValueError("eigvalsh needs a square matrix")
    a = [[float(A[i][j] + A[j][i]) / 2 for j in range(n)] for i in range(n)]   # symmetrize
    if n == 0:
        return []
    fro = math.sqrt(math.fsum(a[i][j] ** 2 for i in range(n) for j in range(n)))
    if fro == 0.0:
        return [0.0] * n
    floor = (_EPS / 2) ** 2 * fro          # below any backward-error-level change of the spectrum
    for _ in range(max_sweeps):
        rotated = False
        for p in range(n - 1):
            for q in range(p + 1, n):
                apq = a[p][q]
                if apq == 0.0:
                    continue
                app, aqq = a[p][p], a[q][q]
                g = 10 * 10 * abs(apq)
                if (abs(app) + g == abs(app) and abs(aqq) + g == abs(aqq)) or abs(apq) <= floor:
                    a[p][q] = a[q][p] = 0.0      # negligible next to both coupled diagonal entries
                    continue
                rotated = True
                tau = (aqq - app) / (2 * apq)
                if abs(tau) > 1 / _EPS:          # tau^2 would swamp the 1 (or overflow)
                    t = 1 / (2 * tau)
                else:
                    t = (1.0 if tau >= 0 else -1.0) / (abs(tau) + math.sqrt(1 + tau * tau))
                c = 1 / math.sqrt(1 + t * t)
                s = t * c
                tr = s / (1 + c)
                a[p][p] = app - t * apq
                a[q][q] = aqq + t * apq
                a[p][q] = a[q][p] = 0.0
                for r in range(n):
                    if r == p or r == q:
                        continue
                    arp, arq = a[r][p], a[r][q]
                    nrp = arp - s * (arq + tr * arp)
                    nrq = arq + s * (arp - tr * arq)
                    a[r][p] = a[p][r] = nrp
                    a[r][q] = a[q][r] = nrq
        if not rotated:
            return sorted(a[i][i] for i in range(n))
    raise ArithmeticError("Jacobi did not converge")


# ------------------------------------------------------------------------------------------
# 2. central-difference Hessian
# ------------------------------------------------------------------------------------------
def hessian(f, x, h=1e-4):
    """Central-difference Hessian of f: R^n -> R at x (absolute step h)."""
    x = [float(v) for v in x]
    n = len(x)

    def at(*shifts):
        y = list(x)
        for i, d in shifts:
            y[i] += d
        return f(y)

    f0 = f(list(x))
    H = [[0.0] * n for _ in range(n)]
    for i in range(n):
        H[i][i] = (at((i, h)) - 2 * f0 + at((i, -h))) / (h * h)
        for j in range(i):
            v = (at((i, h), (j, h)) - at((i, h), (j, -h)) - at((i, -h), (j, h)) + at((i, -h), (j, -h))) / (4 * h * h)
            H[i][j] = H[j][i] = v
    return H


# ------------------------------------------------------------------------------------------
# 3. exact derivative: forward-mode dual numbers over Fraction
# ------------------------------------------------------------------------------------------
def _exact(c):
    if isinstance(c, bool) or isinstance(c, float) or isinstance(c, complex):
        raise TypeError(f"exact_derivative: {type(c).__name__} constant {c!r} would destroy exactness;"
                        " use int or Fraction")
    if isinstance(c, (int, Fraction)):
        return Fraction(c)
    return None


class Dual:
    """a + b e with e^2 = 0, a and b Fractions."""
    __slots__ = ("a", "b")
    __hash__ = None

    def __init__(self, a, b=0):
        self.a, self.b = Fraction(a), Fraction(b)

    @staticmethod
    def _lift(o):
        if isinstance(o, Dual):
            return o
        c = _exact(o)
        return None if c is None else Dual(c, 0)

    def __add__(self, o):
        o = self._lift(o)
        return NotImplemented if o is None else Dual(self.a + o.a, self.b + o.b)
    __radd__ = __add__

    def __sub__(self, o):
        o = self._lift(o)
        return NotImplemented if o is None else Dual(self.a - o.a, self.b - o.b)

    def __rsub__(self, o):
        o = self._lift(o)
        return NotImplemented if o is None else Dual(o.a - self.a, o.b - self.b)

    def __mul__(self, o):
        o = self._lift(o)
        return NotImplemented if o is None else Dual(self.a * o.a, self.a * o.b + self.b * o.a)
    __rmul__ = __mul__

    def __truediv__(self, o):
        o = self._lift(o)
        if o is None:
            return NotImplemented
        if o.a == 0:
            raise ZeroDivisionError("dual division by a number with zero real part")
        return Dual(self.a / o.a, (self.b * o.a - self.a * o.b) / (o.a * o.a))

    def __rtruediv__(self, o):
        o = self._lift(o)
        return NotImplemented if o is None else o.__truediv__(self)

    def __neg__(self):
        return Dual(-self.a, -self.b)

    def __pos__(self):
        return Dual(self.a, self.b)

    def __pow__(self, n):
        if isinstance(n, Fraction) and n.denominator == 1:
            n = n.numerator
        if isinstance(n, bool) or not isinstance(n, int):
            raise TypeError("dual power needs an integer exponent")
        if n == 0:
            return Dual(1, 0)
        if n < 0:
            return Dual(1, 0) / (self ** (-n))
        return Dual(self.a ** n, n * self.a ** (n - 1) * self.b)

    # comparisons act on the real part (piecewise f, away from branch points)
    def _cmp(self, o):
        o = self._lift(o)
        if o is None:
            raise TypeError("cannot compare a dual number with a non-exact value")
        return self.a, o.a

    def __eq__(self, o):
        x, y = self._cmp(o)
        return x == y

    def __lt__(self, o):
        x, y = self._cmp(o)
        return x < y

    def __le__(self, o):
        x, y = self._cmp(o)
        return x <= y

    def __gt__(self, o):
        x, y = self._cmp(o)
        return x > y

    def __ge__(self, o):
        x, y = self._cmp(o)
        return x >= y

    def __repr__(self):
        return f"Dual({self.a}, {self.b})"


def exact_derivative(f, x):
    """f'(x) exactly, as a Fraction, for f built from + - * / (and integer powers) of x and
    rational constants."""
    x = _exact(x)
    if x is None:
        raise TypeError("exact_derivative needs x as an int or Fraction")
    y = f(Dual(x, 1))
    if isinstance(y, Dual):
        return y.b
    if _exact(y) is not None:
        return Fraction(0)                 # f does not depend on x
    raise TypeError(f"f returned {type(y).__name__}, not a dual/rational number")


# ------------------------------------------------------------------------------------------
# 4. bisection
# ------------------------------------------------------------------------------------------
def bisect(f, a, b, iters=200):
    """A root of f in [a, b], given f(a) f(b) < 0."""
    a, b = float(a), float(b)
    fa, fb = f(a), f(b)
    if fa == 0:
        return a
    if fb == 0:
        return b
    if (fa > 0) == (fb > 0):
        raise ValueError(f"bisect: no sign change on [{a}, {b}] (f = {fa}, {fb})")
    for _ in range(iters):
        m = a + (b - a) / 2
        if m == a or m == b:
            break
        fm = f(m)
        if fm == 0:
            return m
        if (fm > 0) == (fa > 0):
            a, fa = m, fm
        else:
            b, fb = m, fm
    return a + (b - a) / 2


# ------------------------------------------------------------------------------------------
# 5. golden-section maximization
# ------------------------------------------------------------------------------------------
def golden_max(f, a, b, iters=200):
    """The maximizer of a unimodal f on [a, b]."""
    a, b = float(a), float(b)
    if a > b:
        a, b = b, a
    r = (math.sqrt(5) - 1) / 2
    c, d = b - r * (b - a), a + r * (b - a)
    fc, fd = f(c), f(d)
    for _ in range(iters):
        if fc >= fd:                       # maximizer in [a, d]; old c becomes new d
            b, d, fd = d, c, fc
            c = b - r * (b - a)
            if not (a < c < d) and b - a <= 4 * _EPS * max(abs(a), abs(b), 1.0):
                break
            fc = f(c)
        else:                              # maximizer in [c, b]; old d becomes new c
            a, c, fc = c, d, fd
            d = a + r * (b - a)
            if not (c < d < b) and b - a <= 4 * _EPS * max(abs(a), abs(b), 1.0):
                break
            fd = f(d)
    return a + (b - a) / 2


# ------------------------------------------------------------------------------------------
# 6. trapezoid rule
# ------------------------------------------------------------------------------------------
def trapezoid(ys, dx):
    """Trapezoid rule over equally spaced samples ys with spacing dx."""
    ys = list(ys)
    if len(ys) < 2:
        return 0.0
    return dx * (math.fsum(ys[1:-1]) + (ys[0] + ys[-1]) / 2)


# ------------------------------------------------------------------------------------------
# 7. permutation parity / Levi-Civita symbol
# ------------------------------------------------------------------------------------------
def levi_civita(p):
    """Sign of the permutation p of 0..n-1; 0 if an index repeats (or is out of range)."""
    p = list(p)
    n = len(p)
    if sorted(p) != list(range(n)):
        return 0
    seen, cycles = [False] * n, 0
    for i in range(n):
        if not seen[i]:
            cycles += 1
            j = i
            while not seen[j]:
                seen[j] = True
                j = p[j]
    return -1 if (n - cycles) % 2 else 1


# ------------------------------------------------------------------------------------------
# self-check by the second routes of DERIVATION_toolkit.md
# ------------------------------------------------------------------------------------------
if __name__ == "__main__":
    import itertools
    import random

    rng = random.Random(7)

    def orth(n):
        Q = [[rng.gauss(0, 1) for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(i):
                d = sum(Q[i][k] * Q[j][k] for k in range(n))
                Q[i] = [Q[i][k] - d * Q[j][k] for k in range(n)]
            nr = math.sqrt(sum(v * v for v in Q[i]))
            Q[i] = [v / nr for v in Q[i]]
        return Q

    def rotate(D):
        n = len(D)
        Q = orth(n)
        return [[math.fsum(Q[k][i] * D[k] * Q[k][j] for k in range(n)) for j in range(n)] for i in range(n)]

    def neg_pivots(A, sigma):
        """Sylvester inertia: number of eigenvalues below sigma, from LDL^T-like elimination."""
        n = len(A)
        M = [[A[i][j] - (sigma if i == j else 0) for j in range(n)] for i in range(n)]
        cnt = 0
        for k in range(n):
            piv = M[k][k] if M[k][k] != 0 else 1e-300
            cnt += piv < 0
            for i in range(k + 1, n):
                m = M[i][k] / piv
                for j in range(k + 1, n):
                    M[i][j] -= m * M[k][j]
        return cnt

    print("eigvalsh")
    D = [1.0, 2.0, 3.0, 4.0]
    A = rotate(D)
    ev = eigvalsh(A)
    print("  rotated diag(1..4):", ev, " trace", math.fsum(ev), "vs", math.fsum(A[i][i] for i in range(4)))
    D9 = [0.0, 0.0, 0.0, 10.0 ** -15, 10.0 ** -9, 10.0 ** -4, 0.5, 1.0, 1.0]
    A9 = rotate([d * 10.0 ** 7 for d in D9])
    ev9 = eigvalsh(A9)
    big = max(abs(v) for v in ev9)
    print("  9x9 with 3 exact zeros, span 1e-15..1 (x1e7): zero modes / max =",
          [abs(v) / big for v in ev9[:3]])
    print("  sum lam^2 vs ||A||_F^2:", math.fsum(v * v for v in ev9),
          math.fsum(A9[i][j] ** 2 for i in range(9) for j in range(9)))
    print("  computed spectrum / 1e7:", [v / 10.0 ** 7 for v in ev9])
    print("  inertia counts at midpoints between distinct eigenvalues 4|5, 5|6, 6|7:",
          [neg_pivots(A9, (ev9[i] + ev9[i + 1]) / 2) for i in range(4, 7)], "(want [5, 6, 7])")
    print("  (eigenvalues far below eps*||A|| are fixed only in absolute terms, ~1e-16 * max)")
    G = [[10.0 ** (2 * i) if i == j else 10.0 ** (i + j - 1) * 0.1 for j in range(5)] for i in range(5)]
    print("  graded diag(10^2i) + small couplings:", eigvalsh(G))

    print("hessian")
    f = lambda v: v[0] ** 2 + 3 * v[0] * v[1] + v[1] ** 3
    print("  cubic at (0.5, 2):", hessian(f, [0.5, 2.0]), " exact [[2,3],[3,12]]")
    g = lambda v: math.exp(v[0]) * math.sin(v[1])
    H1, H2 = hessian(g, [0.3, 0.7], 1e-2), hessian(g, [0.3, 0.7], 5e-3)
    ex = [[math.exp(0.3) * math.sin(0.7), math.exp(0.3) * math.cos(0.7)],
          [math.exp(0.3) * math.cos(0.7), -math.exp(0.3) * math.sin(0.7)]]
    e1 = max(abs(H1[i][j] - ex[i][j]) for i in range(2) for j in range(2))
    e2 = max(abs(H2[i][j] - ex[i][j]) for i in range(2) for j in range(2))
    print(f"  Richardson e^x sin y: err(h) / err(h/2) = {e1 / e2:.3f} (want ~4)")

    print("exact_derivative")
    fr = lambda x: (x * x * x + 1) / (x - 3)
    d = exact_derivative(fr, Fraction(2))
    print("  (x^3+1)/(x-3) at 2:", d, " quotient rule:", Fraction(3 * 4 * (2 - 3) - 9, (2 - 3) ** 2))
    x0 = Fraction(2)
    for k in (2, 4, 6):
        h = Fraction(1, 10 ** k)
        dq = (fr(x0 + h) - fr(x0 - h)) / (2 * h)
        print(f"  exact difference quotient h = 1e-{k}: error = {float(dq - d):.3e}")
    fx = lambda x: 1 / x + (2 - x) * Fraction(1, 3) - x ** -2 + 5 / (1 - x * x) - (x - 1) / x
    xx = Fraction(3, 7)
    want = -1 / xx ** 2 - Fraction(1, 3) + 2 / xx ** 3 + 5 * 2 * xx / (1 - xx * xx) ** 2 - 1 / xx ** 2
    print("  reflected ops 1/x, 2-x, x^-2, 5/(1-x^2), (x-1)/x at 3/7:", exact_derivative(fx, xx), "==", want,
          exact_derivative(fx, xx) == want)

    print("bisect / golden_max")
    r = bisect(lambda x: x * x - 2, 0.0, 2.0)
    print("  sqrt2:", r, " error", r - math.sqrt(2), " residual", r * r - 2)
    gm = golden_max(lambda x: -(x - 0.3) ** 2, -1.0, 2.0)
    fq = lambda x: math.sin(x) * math.exp(-x)
    gm2 = golden_max(fq, 0.0, 2.0)
    br = bisect(lambda x: (fq(x + 1e-6) - fq(x - 1e-6)), 0.1, 1.5)
    print("  -(x-0.3)^2:", gm, "; sin(x)e^-x:", gm2, " vs root of f':", br, " vs pi/4:", math.pi / 4)

    print("trapezoid")
    for n in (501, 1001, 2001):
        ys = [math.sin(math.pi * i / (n - 1)) for i in range(n)]
        T = trapezoid(ys, math.pi / (n - 1))
        print(f"  n = {n}: int sin = {T:.12f}, error = {T - 2:.3e}  (dx^2/6 = {(math.pi / (n - 1)) ** 2 / 6:.3e})")
    print("  linear exact:", trapezoid([1 + 3 * i * 0.1 for i in range(11)], 0.1), "(want 2.5)")

    print("levi_civita")
    ok = True
    perms = list(itertools.permutations(range(5)))
    for p in perms:
        inv = sum(p[i] > p[j] for i in range(5) for j in range(i + 1, 5))
        ok &= levi_civita(p) == (-1) ** inv
    for _ in range(50):
        p, q = rng.choice(perms), rng.choice(perms)
        ok &= levi_civita([p[q[i]] for i in range(5)]) == levi_civita(p) * levi_civita(q)
    print("  cycles vs inversions, multiplicativity over S_5:", ok, "; repeated index:", levi_civita([0, 0, 2, 3]))
