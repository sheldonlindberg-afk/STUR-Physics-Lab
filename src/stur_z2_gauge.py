#!/usr/bin/env python3
"""
Unification search, step 3: 2+1D Z2 lattice gauge theory, where the flux tube is
a DYNAMICAL field (unlike 1+1D).  Question: does the full string energy enter the
modular energy <K> (Bisognano-Wichmann distance weighting) while the entropy S
stays independent of string length?

Model (KNOWN, Wegner 1971; Kogut 1979):  H = - sum_p B_p - h sum_l X_l
  B_p = product of Z around plaquette p,  X_l = electric field on link l,
  Gauss law  prod_{l at v} X_l = -1 at static charges, +1 elsewhere.
  Confining for h > h_c ~ 0.33 (dual to the 2D transverse-field Ising model).

Exact method: gauge-invariant states <-> plaquette configurations tau (duality).
In the electric basis, link value e_l = s_l XOR tau(p1) XOR tau(p2) (outside = 0),
s = reference string between the charges.  So H = -sum_p tau^x_p - h sum_l (-1)^{e_l}.
The state is mapped back to physical link configurations and rho_A is the partial
trace over links in B (extended-Hilbert-space definition, includes the boundary
electric flux).  K = -ln rho_A(vacuum), resolved by SVD.
"""
import os
import numpy as np
from scipy.sparse.linalg import LinearOperator, eigsh

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "z2_gauge")


def banner(s):
    print("\n" + "=" * 78 + "\n" + s + "\n" + "=" * 78)


class Z2Strip:
    def __init__(self, Lx, Ly, h, cut):
        self.Lx, self.Ly, self.h, self.cut = Lx, Ly, h, cut
        self.F = Lx * Ly
        pid = lambda i, j: i * Ly + j if (0 <= i < Lx and 0 <= j < Ly) else -1
        links = []                       # (kind, x, y, midpoint_x, plaquette1, plaquette2)
        for j in range(Ly + 1):          # horizontal links (i,j)-(i+1,j)
            for i in range(Lx):
                links.append(("h", i, j, i + 0.5, pid(i, j - 1), pid(i, j)))
        for i in range(Lx + 1):          # vertical links (i,j)-(i,j+1)
            for j in range(Ly):
                links.append(("v", i, j, float(i), pid(i - 1, j), pid(i, j)))
        self.links = links
        self.states = np.arange(2**self.F, dtype=np.int64)
        bits = ((self.states[:, None] >> np.arange(self.F)) & 1).astype(np.int8)
        zero = np.zeros(len(self.states), np.int8)
        self.tau_e = np.stack([(bits[:, a] if a >= 0 else zero) ^ (bits[:, b] if b >= 0 else zero)
                               for (_, _, _, _, a, b) in links], 1)       # e_l without string
        self.inA = np.array([L[3] < cut for L in links])
        self.plaq_x = np.array([i + 0.5 for i in range(Lx) for j in range(Ly)])

    def string(self, xa, xb, y):
        s = np.zeros(len(self.links), np.int8)
        for k, (kind, i, j, *_rest) in enumerate(self.links):
            if kind == "h" and j == y and xa <= i < xb:
                s[k] = 1
        return s

    def ground(self, s):
        e = self.tau_e ^ s[None, :]
        diag = -self.h * np.sum(1 - 2 * e.astype(np.int64), 1).astype(float)
        masks = [1 << p for p in range(self.F)]
        st = self.states

        def mv(v):
            v = v.ravel()
            out = diag * v
            for m in masks:
                out -= v[st ^ m]
            return out
        op = LinearOperator((len(st), len(st)), matvec=mv, dtype=float)
        E, vec = eigsh(op, k=1, which="SA", tol=1e-12)
        psi = vec[:, 0]
        return E[0], psi * np.sign(psi[np.argmax(abs(psi))]), e

    def local_energy(self, psi, e):
        """<-h X_l> per link (at link midpoint) and <-B_p> per plaquette (at centre)."""
        p2 = psi**2
        eX = -self.h * (p2 @ (1 - 2 * e.astype(float)))
        st = self.states
        eB = np.array([-(psi @ psi[st ^ (1 << p)]) for p in range(self.F)])
        pos = np.r_[[L[3] for L in self.links], self.plaq_x]
        return pos, np.r_[eX, eB]

    def keys(self, e):
        w = (np.int64(1) << np.arange(e.shape[1], dtype=np.int64))
        kA = (e[:, self.inA].astype(np.int64) * w[: self.inA.sum()]).sum(1)
        kB = (e[:, ~self.inA].astype(np.int64) * w[: (~self.inA).sum()]).sum(1)
        return kA, kB


def matrix(kA, kB, psi, Aindex):
    ia = np.array([Aindex[k] for k in kA])
    ub, ib = np.unique(kB, return_inverse=True)
    M = np.zeros((len(Aindex), len(ub)))
    M[ia, ib] = psi
    return M


def run(Lx=6, Ly=3, h=0.5, y=1, xb=5, ells=(1, 2, 3, 4), verbose=True):
    cut = 3.25                                   # A: vertical links x<=3, horizontal midpoints <=2.5
    m = Z2Strip(Lx, Ly, h, cut)
    zero = np.zeros(len(m.links), np.int8)
    E0, p0, e0 = m.ground(zero)
    states = [(None, E0, p0, e0)]
    for ell in ells:
        xa = 4 - ell
        s = m.string(xa, xb, y)
        E, p, e = m.ground(s)
        states.append((ell, E, p, e))
    # common A-configuration index
    allA = np.unique(np.concatenate([m.keys(st[3])[0] for st in states]))
    Aindex = {k: i for i, k in enumerate(allA)}
    kA0, kB0 = m.keys(e0)
    M0 = matrix(kA0, kB0, p0, Aindex)
    U, sv, _ = np.linalg.svd(M0, full_matrices=False)
    keep = sv > 1e-15 * sv[0]
    Uk, Kev = U[:, keep], -2 * np.log(sv[keep])
    S0 = float(-np.sum(sv[sv > 1e-8] ** 2 * np.log(sv[sv > 1e-8] ** 2)))
    K0 = float(np.sum(Kev * sv[keep] ** 2))
    pos, en0 = m.local_energy(p0, e0)
    sel = pos < cut
    dist = cut - pos
    rows = []
    if verbose:
        print(f"Lx={Lx} Ly={Ly} h={h}: dim {2**m.F}, A-configs {len(allA)}, resolved modes {keep.sum()}, max K {Kev.max():.1f}")
    for ell, E, p, e in states[1:]:
        kA, kB = m.keys(e)
        M = matrix(kA, kB, p, Aindex)
        s = np.linalg.svd(M, compute_uv=False)
        s = s[s > 1e-8]
        dS = float(-np.sum(s**2 * np.log(s**2))) - S0
        rho = M @ M.T
        Pr = Uk.T @ rho @ Uk
        leak = 1 - float(np.trace(Pr))
        dK = float(np.sum(Kev * np.diag(Pr))) - K0
        _, en = m.local_energy(p, e)
        wde = float(np.sum((dist * (en - en0))[sel]))
        rows.append(dict(ell=ell, dE=E - E0, dS=dS, dK=dK, D=dK - dS, wdE=wde, leak=leak))
        if verbose:
            print(f"  ell={ell}: dE={E-E0:7.4f}  dS={dS:+.4f}  d<K>={dK:8.4f}  D={dK-dS:8.4f}"
                  f"  sum d*dE={wde:8.4f}  d<K>/sum={dK/wde:7.3f}  leak {leak:.0e}")
    dE = np.array([r["dE"] for r in rows])
    sigma = np.polyfit(list(ells), dE, 1)[0]
    if verbose:
        print(f"  string tension from dE(ell): sigma = {sigma:.4f} per link (strong-coupling 2h = {2*h})")
    return sigma, rows


def main():
    banner("Z1  2+1D Z2 gauge theory, STATIC charges: dynamical flux tube crossing the cut")
    out = {}
    for h in [1.0, 0.5]:
        sigma, rows = run(h=h)
        dS = np.array([r["dS"] for r in rows])
        print(f"  dS increments: " + ", ".join(f"{b-a:+.4f}" for a, b in zip(dS, dS[1:])) + "  (saturates)")
        print("  leak = 1 for ell >= 2: a static charge at an INTERIOR vertex of A is a Gauss-law")
        print("  superselection label of rho_A, so supp(rho_string) and supp(rho_vac) are disjoint and")
        print("  D(string||vac) = infinity. d<K> is undefined there (values printed are meaningless).")
        print("  -> use heavy DYNAMICAL charges instead: stur_z2_higgs.py")
        out[h] = (sigma, rows)
    return out


if __name__ == "__main__":
    main()
