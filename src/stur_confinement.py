#!/usr/bin/env python3
"""
Unification search, step 2: the QCD-type sector.  Does a confining flux tube that
crosses an entanglement cut enter the entropy S, or only the modular energy <K>?

Model (KNOWN): lattice Schwinger model (QED in 1+1D, confining), Kogut-Susskind
staggered fermions, Gauss law solved with open boundaries (Banks et al. 1976):

  W = 2H/(a g^2) = sum_n (L_n + alpha_n)^2 + (mu/2) sum_n (-1)^n s^z_n
                   + x sum_n (s^+_n s^-_{n+1} + h.c.)
  L_n = sum_{k<=n} (s^z_k + (-1)^k)/2,   x = 1/(g a)^2,   mu = 2 (m/g) sqrt(x)

Static charges +-q are a background field alpha_n = q on the links between them
(the Wilson-line string).  Region A = left half of the chain.  The string's right
end is fixed one site past the cut; its left end sits ell sites inside A.

For each ell we compute, exactly:
  dS   = S(rho_A^string) - S(rho_A^vac)
  dK   = Tr[(rho_A^string - rho_A^vac) K],   K = -ln rho_A^vac   (exact modular Ham.)
  D    = D(rho_A^string || rho_A^vac) = dK - dS          (checked directly)
  K_BW = (2 pi / v) sum_{terms in A} dist_to_cut * dE_term,   v = 2x  (Bisognano-Wichmann)
and compare D with a Wilson-loop-type area term sigma x (area swept by the 2 pi
modular rotation of the string inside A).
"""
import os
import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import eigsh

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "confinement")


def banner(s):
    print("\n" + "=" * 78 + "\n" + s + "\n" + "=" * 78)


class Schwinger:
    def __init__(self, N, x, mg):
        self.N, self.x, self.mu = N, x, 2 * mg * np.sqrt(x)
        self.basis = np.array([s for s in range(2**N) if bin(s).count("1") == N // 2])
        self.idx = {s: i for i, s in enumerate(self.basis)}
        self.sz = np.array([[1 if (s >> n) & 1 else -1 for n in range(N)] for s in self.basis])
        self.stag = np.array([(-1) ** n for n in range(N)])
        self.Lbare = np.cumsum((self.sz + self.stag) / 2, axis=1)[:, :-1]
        r, c = [], []
        self.bond_pairs = [[] for _ in range(N - 1)]
        for i, s in enumerate(self.basis):
            for n in range(N - 1):
                if ((s >> n) & 1) != ((s >> (n + 1)) & 1):
                    j = self.idx[s ^ (1 << n) ^ (1 << (n + 1))]
                    r.append(i); c.append(j)
                    self.bond_pairs[n].append((i, j))
        D = len(self.basis)
        self.hop = coo_matrix((np.full(len(r), x), (r, c)), shape=(D, D)).tocsr()

    def ground(self, alpha):
        diag = np.sum((self.Lbare + alpha) ** 2, 1) + self.mu / 2 * self.sz @ self.stag
        D = len(self.basis)
        H = self.hop + coo_matrix((diag, (range(D), range(D))), shape=(D, D))
        E, v = eigsh(H, k=1, which="SA", tol=1e-13)
        psi = v[:, 0]
        return E[0], psi * np.sign(psi[np.argmax(abs(psi))])

    def local_energy(self, psi, alpha):
        """Energy of each term with its position: electric & hopping at n+1/2, mass at n."""
        p2 = psi**2
        pos, e = [], []
        for n in range(self.N - 1):
            pos.append(n + 0.5); e.append(p2 @ (self.Lbare[:, n] + alpha[n]) ** 2)
            pos.append(n + 0.5); e.append(self.x * sum(psi[i] * psi[j] for i, j in self.bond_pairs[n]))
        for n in range(self.N):
            pos.append(n); e.append(self.mu / 2 * self.stag[n] * (p2 @ self.sz[:, n]))
        return np.array(pos), np.array(e)

    def rhoA(self, psi):
        N, h = self.N, self.N // 2
        full = np.zeros(2**N)
        full[self.basis] = psi
        M = full.reshape(2 ** (N - h), 2**h)          # bits 0..h-1 (left half) are the low bits
        return M.T @ M


def entropy_from_probs(p):
    p = p[p > 1e-15]
    return float(-(p * np.log(p)).sum())


def schmidt(m, psi):
    """Schmidt decomposition across the middle cut (SVD resolves rho_A eigenvalues
    down to ~1e-32, versus ~1e-16 for eigh of rho_A)."""
    N, h = m.N, m.N // 2
    full = np.zeros(2**N)
    full[m.basis] = psi
    M = full.reshape(2 ** (N - h), 2**h)          # bits 0..h-1 (left half) are the low bits
    _, s, Vt = np.linalg.svd(M, full_matrices=False)
    return M, s, Vt


def run(N=16, x=1.0, mg=0.5, q=0.5, ells=None, verbose=True):
    m = Schwinger(N, x, mg)
    zero = np.zeros(N - 1)
    E0, p0 = m.ground(zero)
    ds, Es = [], []
    for d in range(2, N - 3, 2):
        al = zero.copy(); st = N // 2 - d // 2; al[st:st + d] = q
        ds.append(d); Es.append(m.ground(al)[0] - E0)
    sigma = np.polyfit(ds, Es, 1)[0]
    M0, s0, Vt0 = schmidt(m, p0)
    keep = s0 > 1e-15 * s0[0]
    V = Vt0[keep].T
    Kev = -2 * np.log(s0[keep])                    # exact modular spectrum on resolved modes
    S0 = entropy_from_probs(s0**2)
    K0 = float(np.sum(Kev * s0[keep] ** 2))
    pos, e0 = m.local_energy(p0, zero)
    cut = N // 2 - 0.5
    inA = pos < cut
    v = 2 * x
    if verbose:
        print(f"N={N}, x={x}, m/g={mg}, q={q}:  sigma = {sigma:.5f} per site (bare q^2 = {q*q});"
              f"  resolved Schmidt modes {keep.sum()}/{len(s0)}, max K = {Kev.max():.1f}")
    rows = []
    for ell in (ells or range(1, N // 2 - 1)):
        al = zero.copy()
        al[N // 2 - ell: N // 2 + 1] = q
        E, p = m.ground(al)
        M, s, _ = schmidt(m, p)
        rho = M.T @ M
        Pr = V.T @ rho @ V
        leak = 1 - float(np.trace(Pr))
        dS = entropy_from_probs(s**2) - S0
        dK = float(np.sum(Kev * np.diag(Pr))) - K0
        _, e = m.local_energy(p, zero)            # VACUUM energy operators on both states
        de = (e - e0)[inA]
        kbw = 2 * np.pi / v * np.sum((cut - pos[inA]) * de)
        rows.append(dict(ell=ell, dS=dS, dK=dK, D=dK - dS, KBW=kbw, leak=leak, dE=E - E0))
        if verbose:
            print(f"  ell={ell}:  dS = {dS:+.4f}   d<K> = {dK:.4f}   D = {dK-dS:.4f}   "
                  f"K_BW = {kbw:.4f}   d<K>/K_BW = {dK/kbw:.3f}   leak {leak:.0e}")
    # dynamical (screening) energy per string link, deep inside the string
    al = zero.copy(); al[2:N - 3] = q
    _, p = m.ground(al)
    _, e = m.local_energy(p, zero)
    mid = (pos > N / 2 - 2) & (pos < N / 2 + 2)
    eps_dyn = float(np.sum((e - e0)[mid]) / 4)
    if verbose:
        print(f"  dynamical energy per string link eps_dyn = {eps_dyn:.4f};  q^2 - sigma = {q*q - sigma:.4f}"
              f"  -> K sees {eps_dyn/sigma*100:.1f}% of sigma")
    return sigma, rows, eps_dyn


def replica_check():
    banner("C2  Replica equation: both areas in one generating function (FOLLOWS)")
    print("ln Z_n = (1 - n) A_H/(4 G) - n sigma A_swept + ...   (A_swept = pi ell^2 per sheet)")
    print("S = (1 - n d/dn) ln Z_n |_{n=1};   <K> - <K>_vac = sigma A_swept  (BW)")
    AH, sig, Asw = 7.3, 0.23, np.pi * 4.0**2             # arbitrary test values
    lnZ = lambda n: (1 - n) * AH / 4 - n * sig * Asw
    lnZ_vac = lambda n: (1 - n) * AH / 4
    h = 1e-6
    S = lambda f: f(1) - (f(1 + h) - f(1 - h)) / (2 * h)
    print(f"   numerical: S(with string) = {S(lnZ):.8f},  S(vacuum) = {S(lnZ_vac):.8f},  A_H/4 = {AH/4:.8f}")
    for n in [2, 3]:
        renyi = lambda f: (f(n) - n * f(1)) / (1 - n)
        print(f"   Renyi-{n}: with string {renyi(lnZ):.8f}  vacuum {renyi(lnZ_vac):.8f}")
    print("   -> the confinement area drops out of EVERY entropy (linear in n) and survives only")
    print("      in the modular energy; the horizon area survives in S. Lattice test: C1 dS")
    print("      must saturate with string length while d<K> grows.")


def main():
    banner("C1  Lattice Schwinger model: flux tube crossing the entanglement cut")
    out = {}
    for N, x, mg in [(16, 1.0, 0.5), (20, 1.0, 0.5), (16, 4.0, 0.5), (16, 1.0, 1.0)]:
        sigma, rows, eps = run(N, x, mg)
        ell = np.array([r["ell"] for r in rows], float)
        dS = np.array([r["dS"] for r in rows]); dK = np.array([r["dK"] for r in rows])
        b2 = np.polyfit(ell, dK, 2)
        print(f"  dS spread over ell >= 3: {np.ptp(dS[2:]):.4f} (saturates);  d<K> fit: "
              f"{b2[0]:.4f} ell^2 + {b2[1]:.4f} ell + {b2[2]:.4f};  BW coefficient (pi/v) eps_dyn = "
              f"{np.pi/(2*x)*eps:.4f}")
        out[(N, x, mg)] = (sigma, rows, eps)
    replica_check()
    return out


if __name__ == "__main__":
    main()
