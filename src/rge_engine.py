#!/usr/bin/env python3
"""
General one-loop RGEs for quartic and Yukawa couplings (real scalars, two-component fermions).

LIT recalled: Machacek & Vaughn, NPB 222, 83; 236, 221; 249, 70 (1983-85); Luo, Wang, Xiao,
PRD 67, 065019 (2003). With kappa = 1/2 (Weyl fermions), Theta^A = g_A theta^A:

  (4pi)^2 beta(lambda_abcd) = Lambda2 - 8 kappa H + 3 A + LambdaY - 3 LambdaS
      Lambda2_abcd = lambda_abef lambda_efcd + (2 more channels)
      A_abcd       = {Th^A,Th^B}_ab {Th^A,Th^B}_cd + (2 more channels)
      H_abcd       = (1/4) sum over the 24 orderings of Re Tr(Y^a Y^b+ Y^c Y^d+)
      LambdaY      = sum over legs of Y2(S) lambda,   Y2(S)_ab = 2 kappa Re Tr(Y^a+ Y^b)
      LambdaS      = sum over legs of C2(S) lambda,   C2(S) = Th^A Th^A
  (4pi)^2 beta(Y^a) = 1/2 [Y2(F)^T Y^a + Y^a Y2(F)] + 2 Y^b Y^a+ Y^b + Y^b Y2(S)_ba
                      - 3 [C2(F) Y^a + Y^a C2(F)],    Y2(F) = Y^b+ Y^b

Scalars: complex multiplets are stored as real components (x, y), z = (x + i y)/sqrt2.
The engine is checked against the Standard Model (check_sm).
"""
from itertools import permutations
from math import pi, sqrt

import numpy as np

KAPPA = 0.5


def real_generator(t):
    """Complex Hermitian generator t on z -> Hermitian theta on (x, y), with delta phi = i theta phi."""
    tR, tI = t.real, t.imag
    M = np.block([[-tI, -tR], [tR, -tI]])
    return -1j * M


def gell_mann():
    l = np.zeros((8, 3, 3), complex)
    l[0][0, 1] = l[0][1, 0] = 1
    l[1][0, 1], l[1][1, 0] = -1j, 1j
    l[2][0, 0], l[2][1, 1] = 1, -1
    l[3][0, 2] = l[3][2, 0] = 1
    l[4][0, 2], l[4][2, 0] = -1j, 1j
    l[5][1, 2] = l[5][2, 1] = 1
    l[6][1, 2], l[6][2, 1] = -1j, 1j
    l[7][0, 0] = l[7][1, 1] = 1 / sqrt(3)
    l[7][2, 2] = -2 / sqrt(3)
    return l / 2


def su2_gens():
    s = np.zeros((3, 2, 2), complex)
    s[0][0, 1] = s[0][1, 0] = 0.5
    s[1][0, 1], s[1][1, 0] = -0.5j, 0.5j
    s[2][0, 0], s[2][1, 1] = 0.5, -0.5
    return s


class Scalars:
    """Complex multiplets -> real fields. Each multiplet: (dim, list of (group, gens) )."""

    def __init__(self, multiplets):
        self.blocks = []
        n = 0
        for dim in multiplets:
            self.blocks.append((n, dim))
            n += 2 * dim
        self.n = n

    def idx(self, m, k):
        """Real indices (x, y) of component k of multiplet m."""
        n0, dim = self.blocks[m]
        return n0 + k, n0 + dim + k

    def embed(self, m, t):
        """Embed a complex generator t (dim x dim) of multiplet m into the full real space."""
        n0, dim = self.blocks[m]
        T = np.zeros((self.n, self.n), complex)
        T[n0:n0 + 2 * dim, n0:n0 + 2 * dim] = real_generator(t)
        return T

    def bilinear(self, mi, mj, part):
        """S with (1/2) phi^T S phi = Re or Im of Phi_i^dag Phi_j."""
        S = np.zeros((self.n, self.n))
        dim = self.blocks[mi][1]
        for k in range(dim):
            xi, yi = self.idx(mi, k)
            xj, yj = self.idx(mj, k)
            if part == "re":
                for a, b in ((xi, xj), (yi, yj)):
                    S[a, b] += 0.5; S[b, a] += 0.5
            else:
                for a, b, s in ((xi, yj, 0.5), (yi, xj, -0.5)):
                    S[a, b] += s; S[b, a] += s
        return S


def quartic_tensor(S1, S2):
    """lambda_abcd = d^4 [ (1/2 phi S1 phi)(1/2 phi S2 phi) ]: sum over the 6 splits of S1 S2."""
    t = (np.einsum("ab,cd->abcd", S1, S2) + np.einsum("ac,bd->abcd", S1, S2)
         + np.einsum("ad,bc->abcd", S1, S2))
    t2 = (np.einsum("ab,cd->abcd", S2, S1) + np.einsum("ac,bd->abcd", S2, S1)
          + np.einsum("ad,bc->abcd", S2, S1))
    return t + t2


def channels(M, n):
    """Given X_{ab,cd} as an (n^2, n^2) matrix, return X_abcd + X_acbd + X_adbc as a tensor."""
    T = M.reshape(n, n, n, n)
    return T + T.transpose(0, 2, 1, 3) + T.transpose(0, 2, 3, 1)


def beta_quartic(lam, Th, Y):
    """lam (n,n,n,n); Th list of (n,n) Hermitian gauge matrices with couplings included;
    Y (n, f, f) complex symmetric Yukawa matrices. Returns (4 pi)^2 beta."""
    n = lam.shape[0]
    L = lam.reshape(n * n, n * n)
    lam2 = channels(L @ L, n)
    K = []
    for A in Th:
        for B in Th:
            K.append((A @ B + B @ A).reshape(-1))
    K = np.array(K)
    Aten = channels((K.T @ K).real, n)
    C2S = sum(T @ T for T in Th).real if Th else np.zeros((n, n))
    legs = lambda X: (np.einsum("ae,ebcd->abcd", X, lam) + np.einsum("be,aecd->abcd", X, lam)
                      + np.einsum("ce,abed->abcd", X, lam) + np.einsum("de,abce->abcd", X, lam))
    out = lam2 + 3 * Aten - 3 * legs(C2S)
    if Y is not None:
        Yd = np.conj(np.transpose(Y, (0, 2, 1)))
        Y2S = 2 * KAPPA * np.einsum("aij,bji->ab", Yd, Y).real
        f = Y.shape[1]
        P = np.einsum("aij,bjk->abik", Y, Yd).reshape(n * n, f, f)            # Y^a Y^b+
        tr = (P.reshape(n * n, f * f) @ P.transpose(0, 2, 1).reshape(n * n, f * f).T)
        tr = tr.real.reshape(n, n, n, n)                                       # Re Tr(Y^a Y^b+ Y^c Y^d+)
        H = np.zeros_like(tr)
        for p in permutations(range(4)):
            H += tr.transpose(p)
        H /= 4
        out += legs(Y2S) - 8 * KAPPA * H
    return out


def beta_yukawa(Y, C2F, n_scalar):
    """(4 pi)^2 beta(Y^a); C2F (f, f) real diagonal fermion Casimir with couplings."""
    Yd = np.conj(np.transpose(Y, (0, 2, 1)))
    Y2F = np.einsum("bij,bjk->ik", Yd, Y)
    Y2S = 2 * KAPPA * np.einsum("aij,bji->ab", Yd, Y).real
    out = 0.5 * (np.einsum("ji,ajk->aik", Y2F, Y) + np.einsum("aij,jk->aik", Y, Y2F))
    out += 2 * np.einsum("bij,ajk,bkl->ail", Y, Yd, Y)
    out += np.einsum("bij,ba->aij", Y, Y2S)
    out -= 3 * (np.einsum("ij,ajk->aik", C2F, Y) + np.einsum("aij,jk->aik", Y, C2F))
    return out


def project(tensor, basis):
    """Least-squares coefficients of tensor in the span of basis tensors; returns (coef, residual)."""
    B = np.array([b.reshape(-1) for b in basis]).T
    c, *_ = np.linalg.lstsq(B, tensor.reshape(-1), rcond=None)
    res = np.linalg.norm(B @ c - tensor.reshape(-1)) / max(np.linalg.norm(tensor), 1e-300)
    return c, res


# ---------------------------------------------------------------- Standard Model check
def sm_setup(g1, g2, yt, Nc=3):
    """H = (1, 2, 1/2); fermions: Q (2 x Nc, Y = 1/6), t^c (Nc, Y = -2/3). g1 non-GUT."""
    sc = Scalars([2])
    Th = [g2 * sc.embed(0, s) for s in su2_gens()] + [g1 * sc.embed(0, 0.5 * np.eye(2))]
    nf = 3 * Nc
    Y = np.zeros((sc.n, nf, nf), complex)
    # y_t eps_ij H_i Q_j t^c  (Q_j index j*Nc + alpha, t^c index 2Nc + alpha)
    eps = np.array([[0, 1], [-1, 0]])
    for i in range(2):
        xi, yi = sc.idx(0, i)
        for j in range(2):
            if eps[i, j] == 0:
                continue
            for al in range(Nc):
                q, tc = j * Nc + al, 2 * Nc + al
                for a, f in ((xi, 1 / sqrt(2)), (yi, 1j / sqrt(2))):
                    Y[a, q, tc] += eps[i, j] * yt * f
                    Y[a, tc, q] += eps[i, j] * yt * f
    return sc, Th, Y


def check_sm(lam=0.13, g1=0.36, g2=0.65, g3=1.16, yt=0.94):
    sc, Th, Y = sm_setup(g1, g2, yt)
    S = sc.bilinear(0, 0, "re")                              # H^dag H = (1/2) phi^T S phi
    T = quartic_tensor(S, S)                                 # lambda (H^dag H)^2 -> lambda * T
    b, res = project(beta_quartic(lam * T, Th, Y), [T])
    expected = (24 * lam**2 - 6 * yt**4 + 12 * lam * yt**2 - 3 * lam * (3 * g2**2 + g1**2)
                + 3 / 8 * (2 * g2**4 + (g2**2 + g1**2) ** 2))
    Nc = 3
    C2 = np.zeros(3 * Nc)
    CF = 4 / 3
    C2[:2 * Nc] = CF * g3**2 + 0.75 * g2**2 + g1**2 / 36
    C2[2 * Nc:] = CF * g3**2 + 4 / 9 * g1**2
    bY = beta_yukawa(Y, np.diag(C2), sc.n)
    cy, resy = project(bY, [Y])
    expected_y = yt * (4.5 * yt**2 - 8 * g3**2 - 9 / 4 * g2**2 - 17 / 12 * g1**2)
    return b[0], expected, res, cy[0] * yt, expected_y, resy
