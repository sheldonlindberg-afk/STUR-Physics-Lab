#!/usr/bin/env python3
"""
Unification search, step 4: equal weights for quark and string in the modular
Hamiltonian, tested where an exact lattice benchmark exists.

Model (KNOWN): Ising chain with transverse field J and longitudinal field h,
    H = -G sum_i s_i X_i X_{i+1} - J sum_i Z_i - h sum_i X_i      (open, N sites)
Ordered phase J < G: domain walls (kinks) are the 'quarks'; h > 0 confines them
with string tension sigma = 2 h m_s (McCoy-Wu 1978); near J = G the continuum
limit is the Ising field theory in a magnetic field (relativistic, v = 2J).
Static quarks: two bonds with s_i = -1 pin kinks there; the spins between them
are reversed and cost 2 h m_s per site - an OPERATOR energy (-h X), unlike 1+1D QED.

Exact benchmark (KNOWN; Baxter CTM, Itoyama-Thacker 1987, Peschel et al. 1999):
for h = 0 and a half-infinite chain, rho_A = exp(-eps * sum_j (distance_j) h_j)/Z,
  eps = pi K(k') / K(k),  k = J/G,  k' = sqrt(1-k^2)
i.e. Bisognano-Wichmann holds EXACTLY on the lattice with slope eps, the same for
every term.  (eps -> 2 pi / v x lattice spacing as J -> G.)

Test: d<K> = Tr[(rho_A - rho_A^vac) K],  K = -ln rho_A^vac (exact, SVD-resolved)
versus  eps * sum_{terms in A} distance * dE   (vacuum operators), for growing
string length ell and for h = 0 (no string) and h > 0 (string carries a growing
share of the energy).  Equal weights <=> the ratio stays = 1 as the share grows.

RESULT (recorded honestly): INCONCLUSIVE at exact-diagonalisation scale (N <= 18).
The kink is itself a Z2 'charge': the string state flips the magnetisation AT the
cut, which the vacuum rarely does, so d<K> is dominated by a large constant
(~15-30 already at ell = 1) and 2-30% of the weight sits beyond the SVD-resolved
modes (K > 69).  dS also grows near the open edge instead of saturating.  The
equal-weight question needs DMRG at large N with high-precision Schmidt spectra.
"""
import numpy as np
from scipy.sparse.linalg import LinearOperator, eigsh
from scipy.special import ellipk


def banner(s):
    print("\n" + "=" * 78 + "\n" + s + "\n" + "=" * 78)


def eps_ctm(J, G):
    k = J / G
    return np.pi * ellipk(1 - k * k) / ellipk(k * k)     # scipy ellipk takes m = k^2


class Chain:
    def __init__(self, N):
        self.N = N
        self.st = np.arange(2**N, dtype=np.int64)
        self.x = 1 - 2 * ((self.st[:, None] >> np.arange(N)) & 1).astype(np.int8)   # X eigenvalues

    def ground(self, G, J, h, s):
        x = self.x.astype(float)
        diag = -G * np.sum(s[None, :] * x[:, :-1] * x[:, 1:], 1) - h * x.sum(1)
        st, masks = self.st, [1 << i for i in range(self.N)]

        def mv(v):
            v = v.ravel()
            out = diag * v
            for m in masks:
                out -= J * v[st ^ m]
            return out
        E, vec = eigsh(LinearOperator((len(st), len(st)), matvec=mv, dtype=float), k=1, which="SA", tol=1e-13)
        psi = vec[:, 0]
        return E[0], psi * np.sign(psi @ np.ones(len(psi)) + 1e-300)

    def local(self, psi, G, J, h):
        """vacuum-operator energies: bonds (-G XX) at i+1/2, sites (-J Z - h X) at i."""
        p2 = psi**2
        x = self.x.astype(float)
        eb = -G * (p2 @ (x[:, :-1] * x[:, 1:]))
        ez = np.array([-J * (psi @ psi[self.st ^ (1 << i)]) for i in range(self.N)])
        ex = -h * (p2 @ x)
        pos = np.r_[np.arange(self.N - 1) + 0.5, np.arange(self.N), np.arange(self.N)]
        kind = np.r_[["XX"] * (self.N - 1), ["Z"] * self.N, ["X"] * self.N]
        return pos, kind, np.r_[eb, ez, ex]

    def M(self, psi):
        L = self.N // 2
        return psi.reshape(2 ** (self.N - L), 2**L)        # low bits = left half (sites 0..L-1)


def run(N=20, G=1.0, J=0.5, h=0.0, ells=(1, 2, 3, 4, 5, 6), verbose=True):
    ch = Chain(N)
    L = N // 2
    cut = L - 0.5
    s0 = np.ones(N - 1)
    E0, p0 = ch.ground(G, J, h, s0)
    U, sv, _ = np.linalg.svd(ch.M(p0), full_matrices=False)
    keep = sv > 1e-15 * sv[0]
    Uk, Kev = U[:, keep], -2 * np.log(sv[keep])
    ent = lambda s: float(-np.sum(s[s > 1e-8] ** 2 * np.log(s[s > 1e-8] ** 2)))
    S0, K0 = ent(sv), float(np.sum(Kev * sv[keep] ** 2))
    pos, kind, e0 = ch.local(p0, G, J, h)
    inA = pos < cut
    d = cut - pos
    eps = eps_ctm(J, G)
    rows = []
    if verbose:
        print(f"N={N} G={G} J={J} h={h}: eps_CTM = {eps:.5f} (2pi/v = {2*np.pi/(2*J):.4f}),"
              f" resolved modes {keep.sum()}/{len(sv)}")
    for ell in ells:
        s = s0.copy()
        s[L - 1 - ell] = -1          # kink in A, ell bonds from the cut bond
        s[L + 1] = -1                # kink in B, fixed
        E, p = ch.ground(G, J, h, s)
        M = ch.M(p)
        rho = M.T @ M
        Pr = Uk.T @ rho @ Uk
        leak = 1 - float(np.trace(Pr))
        sv1 = np.linalg.svd(M, compute_uv=False)
        dS = ent(sv1) - S0
        dK = float(np.sum(Kev * np.diag(Pr))) - K0
        _, _, e = ch.local(p, G, J, h)
        de = (e - e0)
        W = float(np.sum((d * de)[inA]))
        Ws = float(np.sum((d * de)[inA & (kind == "X")]))          # string (longitudinal field) part
        rows.append(dict(ell=ell, dE=E - E0, dS=dS, dK=dK, W=W, Ws=Ws, leak=leak))
        if verbose:
            print(f"  ell={ell}: dE={E-E0:7.4f}  dS={dS:+.4f}  d<K>={dK:8.4f}  eps*sum d dE={eps*W:8.4f}"
                  f"  ratio={dK/(eps*W):.4f}  string share {Ws/W*100:5.1f}%  leak {leak:.0e}")
    return eps, rows


def main():
    banner("I1  Confining Ising chain: are quark and string weighted equally in K?  (INCONCLUSIVE)")
    for J, h in [(0.85, 0.05), (0.9, 0.05), (0.95, 0.05), (0.95, 0.02)]:
        run(N=18, J=J, h=h)
    print("\nleak = 2e-3 ... 3e-1: d<K> not resolved; the ratio to eps*sum d dE is not meaningful.")


if __name__ == "__main__":
    main()
