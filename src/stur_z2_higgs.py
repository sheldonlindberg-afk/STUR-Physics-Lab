#!/usr/bin/env python3
"""
Unification search, step 3b: Z2 gauge-Higgs model, heavy DYNAMICAL charges.

Why: with static charges (an earlier static-charge version) the string state and the vacuum lie in
different Gauss-law superselection sectors of region A, so D(string||vac) is
infinite and <K> cannot be compared.  Making the quark a heavy dynamical particle
puts both states in one Hilbert space.

Model (KNOWN, Fradkin-Shenker 1979), unitary gauge (matter absorbed into links):
  H = - sum_p B_p - h sum_l X_l - J sum_l Z_l - sum_v G_v A_v,   A_v = prod_{l at v} X_l
  A_v = -1 means a matter charge at v (cost 2 G_v).  Heavy quarks: G_v > 0 large;
  the two quark sites get G_v -> -G_q (charge pinned there).  The flux between them
  is a dynamical string (plaquette term B_p makes it fluctuate).
Geometry: ladder Lx x 1 plaquettes (exact diagonalisation in the X basis).
Test: is the exact modular energy d<K> = Tr[(rho - rho_vac) K], K = -ln rho_vac,
distance-weighted energy (Bisognano-Wichmann structure)  d<K> ~ c * sum_A dist * dE ?
If so, the FULL string energy (an operator here) enters <K>.  And does dS saturate?
"""
import numpy as np
from scipy.sparse.linalg import LinearOperator, eigsh


def banner(s):
    print("\n" + "=" * 78 + "\n" + s + "\n" + "=" * 78)


class Ladder:
    def __init__(self, Lx, h, J, G, cut):
        self.Lx, self.h, self.J, self.cut = Lx, h, J, cut
        links, mid = [], []
        for j in (0, 1):
            for i in range(Lx):
                links.append(((i, j), (i + 1, j))); mid.append(i + 0.5)
        for i in range(Lx + 1):
            links.append(((i, 0), (i, 1))); mid.append(float(i))
        self.links, self.mid = links, np.array(mid)
        self.E = len(links)
        idx = {l: k for k, l in enumerate(links)}
        self.verts = [(i, j) for i in range(Lx + 1) for j in (0, 1)]
        self.star = [sum(1 << k for k, l in enumerate(links) if v in l) for v in self.verts]
        self.plaq = [(1 << idx[((i, 0), (i + 1, 0))]) | (1 << idx[((i, 1), (i + 1, 1))]) |
                     (1 << idx[((i, 0), (i, 1))]) | (1 << idx[((i + 1, 0), (i + 1, 1))]) for i in range(Lx)]
        self.st = np.arange(2**self.E, dtype=np.int64)
        self.bits = ((self.st[:, None] >> np.arange(self.E)) & 1).astype(np.int8)
        self.par = np.stack([(np.bitwise_count(self.st & m) & 1) if hasattr(np, "bitwise_count")
                             else np.array([bin(int(s) & m).count("1") & 1 for s in self.st])
                             for m in self.star], 1).astype(np.int8)          # 1 = charge at v
        self.G = G
        self.inA = self.mid < cut
        self.wA = np.int64(1) << np.arange(self.inA.sum(), dtype=np.int64)
        self.wB = np.int64(1) << np.arange((~self.inA).sum(), dtype=np.int64)
        self.vx = np.array([v[0] for v in self.verts], float)

    def ground(self, Gv):
        X = 1 - 2 * self.bits.astype(float)
        A = 1 - 2 * self.par.astype(float)
        diag = -self.h * X.sum(1) - A @ Gv
        st, masks = self.st, self.plaq + [1 << k for k in range(self.E)]
        coef = [1.0] * len(self.plaq) + [self.J] * self.E

        def mv(v):
            v = v.ravel()
            out = diag * v
            for m, c in zip(masks, coef):
                out -= c * v[st ^ m]
            return out
        E, vec = eigsh(LinearOperator((len(st), len(st)), matvec=mv, dtype=float), k=1, which="SA", tol=1e-12)
        psi = vec[:, 0]
        return E[0], psi * np.sign(psi[np.argmax(abs(psi))])

    def local_energy(self, psi, Gv):
        p2 = psi**2
        st = self.st
        eX = -self.h * (p2 @ (1 - 2 * self.bits.astype(float)))
        eZ = np.array([-self.J * (psi @ psi[st ^ (1 << k)]) for k in range(self.E)])
        eB = np.array([-(psi @ psi[st ^ m]) for m in self.plaq])
        eA = -Gv * (p2 @ (1 - 2 * self.par.astype(float)))
        pos = np.r_[self.mid, self.mid, np.arange(self.Lx) + 0.5, self.vx]
        return pos, np.r_[eX, eZ, eB, eA]

    def M(self, psi):
        kA = (self.bits[:, self.inA].astype(np.int64) * self.wA).sum(1)
        kB = (self.bits[:, ~self.inA].astype(np.int64) * self.wB).sum(1)
        M = np.zeros((2 ** self.inA.sum(), 2 ** (~self.inA).sum()))
        M[kA, kB] = psi
        return M


def run(Lx=6, h=0.8, J=0.3, Gm=2.0, Gq=2.0, xb=5, ells=(1, 2, 3, 4), verbose=True):
    cut = 3.25
    G0 = np.full(2 * (Lx + 1), Gm)
    lad = Ladder(Lx, h, J, G0, cut)
    vid = {v: k for k, v in enumerate(lad.verts)}
    E0, p0 = lad.ground(G0)
    U, sv, _ = np.linalg.svd(lad.M(p0), full_matrices=False)
    keep = sv > 1e-15 * sv[0]
    Uk, Kev = U[:, keep], -2 * np.log(sv[keep])
    ent = lambda s: float(-np.sum(s[s > 1e-8] ** 2 * np.log(s[s > 1e-8] ** 2)))
    S0, K0 = ent(sv), float(np.sum(Kev * sv[keep] ** 2))
    pos, e0 = lad.local_energy(p0, G0)
    sel = pos < cut
    dist = cut - pos
    if verbose:
        print(f"Lx={Lx} ladder, h={h}, J={J}, G={Gm}, quark G=-{Gq}: dim {2**lad.E}, "
              f"resolved modes {keep.sum()}/{len(sv)}, max K {Kev.max():.1f}")
    rows = []
    for ell in ells:
        xa = 4 - ell
        Gv = G0.copy(); Gv[vid[(xa, 0)]] = -Gq; Gv[vid[(xb, 0)]] = -Gq
        E, p = lad.ground(Gv)
        M = lad.M(p)
        s = np.linalg.svd(M, compute_uv=False)
        rho = M @ M.T
        Pr = Uk.T @ rho @ Uk
        leak = 1 - float(np.trace(Pr))
        dS = ent(s) - S0
        dK = float(np.sum(Kev * np.diag(Pr))) - K0
        _, e = lad.local_energy(p, Gv)
        _, eop = lad.local_energy(p, G0)          # vacuum operators on the string state
        wde = float(np.sum((dist * (eop - e0))[sel]))
        nterm = len(pos) - len(lad.vx)                 # last len(vx) entries are matter-mass terms
        isq = np.zeros(len(pos), bool); isq[nterm:] = True
        wq = float(np.sum((dist * (eop - e0))[sel & isq]))
        ws = wde - wq
        nq = float(p**2 @ lad.par[:, vid[(xa, 0)]])
        rows.append(dict(ell=ell, dE=E - E0, dS=dS, dK=dK, wdE=wde, wq=wq, ws=ws, leak=leak, nq=nq))
        if verbose:
            print(f"  ell={ell}: dE={E-E0:7.4f}  <n_quark>={nq:.3f}  dS={dS:+.4f}  d<K>={dK:8.4f}"
                  f"  sum d*dE={wde:7.3f} (string {ws/wde*100:4.1f}%)  d<K>/sum={dK/wde:6.3f}  leak {leak:.0e}")
    dE = np.array([r["dE"] for r in rows])
    sigma = np.polyfit(list(ells), dE, 1)[0]
    if verbose:
        print(f"  string tension from dE(ell): {sigma:.4f} per link")
    return sigma, rows


def main():
    banner("Z2  Z2 gauge-Higgs ladder: heavy dynamical quark, dynamical flux tube")
    print("d<K> exact (K = -ln rho_vac, SVD-resolved to K ~ 69; 'leak' = weight beyond that,")
    print("so d<K> is a LOWER bound when leak is not small).  'string %' = share of the")
    print("distance-weighted energy carried by flux/plaquette/hopping terms (vs quark mass).")
    out = {}
    for h in [0.8, 1.0, 1.2]:
        sig, rows = run(h=h, Gq=6.0)
        r23 = [r["dK"] / r["wdE"] for r in rows if r["ell"] in (2, 3)]
        dS = [r["dS"] for r in rows]
        print(f"  dS increments: " + ", ".join(f"{b-a:+.4f}" for a, b in zip(dS, dS[1:]))
              + f";  d<K>/sum at ell=2,3: {r23[0]:.3f}, {r23[1]:.3f}")
        r2, r3 = [r for r in rows if r["ell"] == 2][0], [r for r in rows if r["ell"] == 3][0]
        cq, cs = np.linalg.solve([[r2["wq"], r2["ws"]], [r3["wq"], r3["ws"]]], [r2["dK"], r3["dK"]])
        print(f"  separate weights from ell=2,3 (exactly determined, no error bar):"
              f"  quark c_q = {cq:.2f},  string c_s = {cs:.2f}   (1+1D bare string: 0)")
        out[h] = (sig, rows, cq, cs)
    print("\nEntanglement-Hamiltonian tomography was tried and is ill-posed at this size:")
    print("only ~20 modes have K < 40 (gapped vacuum), fewer than the ~37 fit parameters.")
    return out


def eh_tomography(Lx=6, h=0.8, J=0.3, Gm=2.0, kmax=40.0, verbose=True):
    """Fit the exact vacuum modular Hamiltonian on its well-resolved subspace (K < kmax)
    as K ~ c0 + sum_t beta_t O_t over every local term O_t lying wholly inside A.
    Bisognano-Wichmann predicts beta_t = (2 pi / v) * coupling_t * dist_t for ALL term
    types (electric X, matter hopping Z, plaquette B, matter mass A_v)."""
    cut = 3.25
    G0 = np.full(2 * (Lx + 1), Gm)
    lad = Ladder(Lx, h, J, G0, cut)
    E0, p0 = lad.ground(G0)
    U, sv, _ = np.linalg.svd(lad.M(p0), full_matrices=False)
    Kev = -2 * np.log(np.clip(sv, 1e-300, None))
    good = Kev < kmax
    Ug, Kg = U[:, good], Kev[good]
    Alinks = np.where(lad.inA)[0]
    pos_of = {k: i for i, k in enumerate(Alinks)}
    nA = len(Alinks)
    dimA = 2**nA
    cfg = np.arange(dimA)
    bitsA = (cfg[:, None] >> np.arange(nA)) & 1
    ops, lab, dist, coup = [], [], [], []
    for k in Alinks:                                   # electric X_l (diagonal)
        ops.append(np.diag(1 - 2 * bitsA[:, pos_of[k]]).astype(float)); lab.append("X")
        dist.append(cut - lad.mid[k]); coup.append(h)
    for k in Alinks:                                   # matter hopping Z_l (flip one link)
        O = np.zeros((dimA, dimA)); O[cfg, cfg ^ (1 << pos_of[k])] = 1
        ops.append(O); lab.append("Z"); dist.append(cut - lad.mid[k]); coup.append(J)
    for i, m in enumerate(lad.plaq):                   # plaquettes wholly in A
        ks = [k for k in range(lad.E) if (m >> k) & 1]
        if all(lad.inA[k] for k in ks):
            mm = sum(1 << pos_of[k] for k in ks)
            O = np.zeros((dimA, dimA)); O[cfg, cfg ^ mm] = 1
            ops.append(O); lab.append("B"); dist.append(cut - (i + 0.5)); coup.append(1.0)
    for v, sm in zip(lad.verts, lad.star):             # stars wholly in A
        ks = [k for k in range(lad.E) if (sm >> k) & 1]
        if all(lad.inA[k] for k in ks):
            par = np.zeros(dimA, int)
            for k in ks:
                par ^= bitsA[:, pos_of[k]]
            ops.append(np.diag(1 - 2 * par).astype(float)); lab.append("A"); dist.append(cut - v[0]); coup.append(Gm)
    # project everything to the resolved subspace and solve least squares
    P = lambda O: Ug.T @ O @ Ug
    cols = [np.eye(len(Kg)).ravel()] + [P(O).ravel() for O in ops]
    Xmat = np.array(cols).T
    coef, *_ = np.linalg.lstsq(Xmat, np.diag(Kg).ravel(), rcond=None)
    resid = np.linalg.norm(Xmat @ coef - np.diag(Kg).ravel()) / np.linalg.norm(np.diag(Kg).ravel())
    beta = coef[1:]
    lab, dist, coup = np.array(lab), np.array(dist), np.array(coup)
    if verbose:
        print(f"EH tomography h={h}: resolved modes {good.sum()}/{dimA} (K<{kmax}),"
              f" relative residual {resid:.3f}")
        for t in ["X", "Z", "B", "A"]:
            s_ = lab == t
            if s_.any():
                r = -beta[s_] / coup[s_]               # K = -sum beta*coupling*O  ->  local inverse T
                order = np.argsort(dist[s_])
                print(f"   {t}: dist " + " ".join(f"{d:4.2f}" for d in dist[s_][order]))
                print(f"      beta/coupling " + " ".join(f"{x:6.2f}" for x in r[order]))
    return lab, dist, coup, beta, resid


if __name__ == "__main__":
    main()
