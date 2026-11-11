#!/usr/bin/env python3
"""
Does ONE known equation govern measurement, the vacuum and horizons?  Candidate (KNOWN pieces only):

    D(rho || sigma) = Delta<K_sigma> - Delta S >= 0,   K_sigma = -ln sigma      (U1)
    first law:  delta S = delta <K_sigma>  at first order                       (U1')
    visibility of a which-path record:  V = < (-1)^{Delta N} >                  (U2)

Sector-specific input is ONLY the modular Hamiltonian K_sigma:
    thermal bath          K = H / k_B T                      (decoherence, thermo)
    Rindler / horizon     K = 2 pi x boost  (Bisognano-Wichmann; the 2 pi holonomy of P4)
    QCD flux tube         K unknown in closed form          <- the gap

Sections
  U2  parity identity for which-path records (Fock-space check)
  U1  free-fermion lattice: (a) modular Hamiltonian = 2 pi x local boost (BW/CHM)
                            (b) first law and positivity of D for a boundary excitation
                            (c) local Clausius form  dS = sum_x dE(x) / T_loc(x)
  U3  entanglement area law (Srednicki): horizon tension = (species) x c / cutoff^2
  U4  the QCD gap stated as a computable target
numpy + scipy + mpmath.
"""
import numpy as np
import mpmath as mp
from scipy.linalg import expm, eigh

LBL = {"K": "KNOWN", "F": "FOLLOWS", "C": "CHECK"}


def banner(s):
    print("\n" + "=" * 78 + "\n" + s + "\n" + "=" * 78)


# ---------------------------------------------------------------------------
def U2_parity():
    banner("U2  Visibility = parity of exchanged quanta:  V = <(-1)^{Delta N}>")
    print("Exact for linear coupling to bosons, any bath state diagonal in Fock basis")
    print("(algebra: D(a)^dag Pi D(a) = Pi D(2a); FOLLOWS, literature not checked).")
    rng = np.random.default_rng(3)
    worst = 0.0
    for al, T in [(0.3, 0.05), (0.6, 2.0), (1.1, 0.7)]:
        N = 300
        a = np.diag(np.sqrt(np.arange(1, N)), 1)
        for kind in ["thermal", "random diagonal"]:
            if kind == "thermal":
                p = np.exp(-np.arange(N) / T)
            else:
                p = np.zeros(N); p[:25] = rng.random(25)
            p /= p.sum()
            D = expm(al * (a.T - a))
            P = np.abs(D) ** 2
            dn = np.arange(N)[:, None] - np.arange(N)[None, :]
            par = np.sum(P * p[None, :] * (-1.0) ** dn)
            V = np.trace(D @ D @ np.diag(p)).real
            worst = max(worst, abs(par - V))
            tl = f"T={T:4.2f}" if kind == "thermal" else "      "
            print(f"   alpha={al:.1f} {kind:16s} {tl}:  <(-1)^dN> = {par:+.12f}   V = {V:+.12f}")
    print(f"   max |difference| = {worst:.1e}   CHECK")
    print("   Same object as a free-field Wilson loop <0|D(alpha)|0>: abelian W(C) is the")
    print("   visibility of a charge interferometer around C (KNOWN). For Gaussian noise")
    print("   -ln V = 2 Var(N_exch): the phase variance counts exchanged quanta.")
    return worst


# ---------------------------------------------------------------------------
def C_inf(idx, dps=None):
    """Half-filled infinite tight-binding chain (hopping 1, k_F = pi/2, v_F = 2):
    C_ij = sin(pi(i-j)/2)/(pi(i-j)), C_ii = 1/2.  Float64, or mpmath if dps given."""
    idx = list(idx)
    if dps is None:
        d = np.subtract.outer(idx, idx).astype(float)
        with np.errstate(invalid="ignore", divide="ignore"):
            C = np.where(d == 0, 0.5, np.sin(np.pi * d / 2) / (np.pi * d))
        return C
    mp.mp.dps = dps
    n = len(idx)
    M = mp.matrix(n, n)
    for a in range(n):
        for b in range(n):
            d = idx[a] - idx[b]
            M[a, b] = mp.mpf(1) / 2 if d == 0 else mp.sin(mp.pi * d / 2) / (mp.pi * d)
    return M


def modular_h(L, dps):
    """h = ln((1 - C_A)/C_A) for a block of L sites, computed fully in high precision."""
    M = C_inf(range(L), dps)
    E, Q = mp.eigsy(M)
    lam = [mp.log((1 - E[k]) / E[k]) for k in range(L)]
    out = np.zeros((L, L))
    for i in range(L):
        for j in range(i, L):
            out[i, j] = out[j, i] = float(mp.fsum(Q[i, k] * lam[k] * Q[j, k] for k in range(L)))
    return out


def S_gauss(CA):
    ev = np.clip(eigh(CA, eigvals_only=True), 1e-300, 1 - 1e-16)
    ev = ev[(ev > 1e-14) & (ev < 1 - 1e-14)]
    return float(-np.sum(ev * np.log(ev) + (1 - ev) * np.log(1 - ev)))


def S_gauss_c(CA):
    ev = np.clip(np.linalg.eigvalsh(CA), 1e-300, 1 - 1e-16)
    ev = ev[(ev > 1e-14) & (ev < 1 - 1e-14)]
    return float(-np.sum(ev * np.log(ev) + (1 - ev) * np.log(1 - ev)))


def U1_lattice():
    banner("U1  Free-fermion chain: one equation for horizon-type entanglement")
    vF = 2.0
    print("(a) Modular Hamiltonian of a block of L sites vs 2 pi x local boost (CHM/BW, KNOWN).")
    print("    Prediction (continuum): h_(x-1,x) = -(2 pi/v_F) x (L-x)/L,  2 pi/v_F = pi")
    res = {}
    for L in [20, 40, 60]:
        h = modular_h(L, dps=30 + 2 * L)
        x = np.arange(1, L)
        beta = x * (L - x) / L
        ratio = -np.diag(h, 1) / beta
        lr = np.max(np.abs(np.triu(h, 2))) / np.max(np.abs(np.diag(h, 1)))
        # continuum velocity carried by ALL hoppings: v_eff(x) = sum_r r sin(k_F r) (-h_{x, x+r})
        def veff(c):
            return sum(-r * np.sin(np.pi * r / 2) * h[c - (r + 1) // 2, c - (r + 1) // 2 + r]
                       for r in range(1, L, 2) if c - (r + 1) // 2 >= 0 and c - (r + 1) // 2 + r < L)
        c0, c1 = L // 2, L // 4
        eff0 = veff(c0) / (c0 * (L - c0) / L)
        eff1 = veff(c1) / ((c1 - 0.5) * (L - c1 + 0.5) / L)
        res[L] = (h, eff0)
        print(f"    L={L:3d}: nearest-neighbour only {ratio[L//2-1]:.4f};  all hoppings, centre {eff0:.5f},"
              f" x=L/4 {eff1:.5f}   (pi = {np.pi:.5f});  |longer|/|nn| = {lr:.3f}")
    print("    -> the 2 pi of the Euclidean horizon (P4) is the slope of the modular Hamiltonian:")
    print("       K = 2 pi x (boost-weighted energy). Lattice CHECK (finite-L corrections shrink).")

    print("\n(b) First law and positivity on a ring (N = 202, half filling, closed shell), L = 40")
    print("    excitation: rotate a filled wavepacket at the cut into an empty one by angle eps")
    N, nf, L = 202, 101, 40
    m = np.arange(-(nf - 1) // 2, (nf - 1) // 2 + 1)
    orb = np.exp(1j * np.outer(np.arange(N), 2 * np.pi * m / N)) / np.sqrt(N)
    C = orb @ orb.conj().T                               # exact projector
    mp.mp.dps = 120
    Mm = mp.matrix(L, L)
    for a_ in range(L):
        for b_ in range(L):
            d = a_ - b_
            Mm[a_, b_] = mp.mpf(nf) / N if d == 0 else mp.sin(mp.pi * nf * d / N) / (N * mp.sin(mp.pi * d / N))
    E, Q = mp.eigsy(Mm)
    lam = [mp.log((1 - E[k]) / E[k]) for k in range(L)]
    h = np.array([[float(mp.fsum(Q[i_, k] * lam[k] * Q[j_, k] for k in range(L))) for j_ in range(L)]
                  for i_ in range(L)])
    xs = np.arange(N)
    u = np.exp(-((xs - L) ** 2) / (2 * 3.0**2)) * np.exp(1j * 0.6 * xs)   # packet on the cut
    pa = C @ u; pa /= np.linalg.norm(pa)
    pb = u - C @ u; pb /= np.linalg.norm(pb)
    CA0 = C[:L, :L]
    S0 = S_gauss_c(CA0)
    rows = []
    for eps in [0.2, 0.1, 0.05, 0.025]:
        q = np.cos(eps) * pa + np.sin(eps) * pb
        C1 = C - np.outer(pa, pa.conj()) + np.outer(q, q.conj())
        CA1 = C1[:L, :L]
        dS = S_gauss_c(CA1) - S0
        dK = float(np.real(np.sum(h * (CA1 - CA0).T)))
        rows.append((eps, dS, dK, C1))
        print(f"    eps={eps:6.3f}:  dS = {dS:+.6e}   d<K> = {dK:+.6e}   dS/d<K> = {dS/dK:.5f}"
              f"   D = {dK-dS:.3e}   D/eps^2 = {(dK-dS)/eps**2:.5f}")
    e_ = np.array([r[0] for r in rows]); S_ = np.array([r[1] for r in rows]); K_ = np.array([r[2] for r in rows])
    X = np.c_[e_, e_**2]
    aS = np.linalg.lstsq(X, S_, rcond=None)[0]; aK = np.linalg.lstsq(X, K_, rcond=None)[0]
    print(f"    first-order slopes (fit a eps + b eps^2):  dS: {aS[0]:.5f}   d<K>: {aK[0]:.5f}"
          f"   ratio {aS[0]/aK[0]:.5f}")
    print("    -> first order: dS = d<K> (first law); difference D >= 0 is pure eps^2. CHECK")

    print("\n(c) Local Clausius form  dS = sum_x dE(x)/T_loc(x),  T_loc(x) = v_F/(2 pi beta(x))  (ring CHM)")
    vF = 2 * np.sin(np.pi * nf / N)
    eps, dS, dK, C1 = rows[-1]
    x = np.arange(1, L)
    beta = (N / np.pi) * np.sin(np.pi * x / N) * np.sin(np.pi * (L - x) / N) / np.sin(np.pi * L / N)
    dE = -2 * np.real(np.array([C1[xx - 1, xx] - C[xx - 1, xx] for xx in x]))
    clausius = float(np.sum(2 * np.pi * beta / vF * dE))
    print(f"    eps={eps}: sum dE/T_loc = {clausius:+.6e}   exact d<K> = {dK:+.6e}"
          f"   ratio = {clausius/dK:.5f}")
    print("    -> the Unruh-weighted local energy IS the modular energy (lattice, 0.0x %),")
    print("       and by (b) its first-order change equals dS.")
    print("    -> a global E = T S is the integrated, global-T caricature of THIS local law;")
    print("       the temperature is the local Unruh-type T_loc(x), not one global T.")
    return res, rows, clausius / dK, aS[0] / aK[0]


# ---------------------------------------------------------------------------
def srednicki(N=60, n=30, lmax=4000):
    S = 0.0
    for l in range(lmax + 1):
        j = np.arange(1, N + 1, dtype=float)
        K = np.diag(l * (l + 1) / j**2 + ((j + 0.5) ** 2 + (j - 0.5) ** 2) / j**2)
        K[0, 0] = 9 / 4 + l * (l + 1)
        off = -((j[:-1] + 0.5) ** 2) / (j[:-1] * j[1:])
        K += np.diag(off, 1) + np.diag(off, -1)
        w, v = eigh(K)
        X = 0.5 * (v / np.sqrt(w)) @ v.T
        P = 0.5 * (v * np.sqrt(w)) @ v.T
        nu = np.sqrt(np.clip(eigh(X[:n, :n] @ P[:n, :n], eigvals_only=True), 0.25, None))
        nu = nu[nu > 0.5 + 1e-12]
        s = np.sum((nu + .5) * np.log(nu + .5) - (nu - .5) * np.log(nu - .5))
        S += (2 * l + 1) * s
        if l > 50 and (2 * l + 1) * s < 1e-9:
            break
    return S


def U3_area():
    banner("U3  Entanglement entropy of a free scalar across a sphere (Srednicki 1993)")
    Rs, Ss = [], []
    for n in [10, 14, 18, 22, 26]:
        S = srednicki(N=2 * n + 30, n=n)
        R = n + 0.5
        Rs.append(R); Ss.append(S)
        print(f"   R/a = {R:5.1f}:  S = {S:9.4f}   S/(R/a)^2 = {S/R**2:.4f}")
    Rs, Ss = np.array(Rs), np.array(Ss)
    coef = np.polyfit(Rs, Ss / Rs**2, 1)            # S/R^2 = k + m/R  (allow subleading)
    k = np.polyfit(1 / Rs, Ss / Rs**2, 1)[1]
    s_area = k / (4 * np.pi)
    print(f"   extrapolated S = {k:.4f} (R/a)^2  (LIT Srednicki 0.30)  ->  S = {s_area:.5f} A/a^2")
    print(f"   Bekenstein-Hawking A/4lP^2 needs a = lP x sqrt(4 x {s_area:.4f}) = {np.sqrt(4*s_area):.3f} lP,")
    print(f"   or N_species = 1/(4 x {s_area:.4f}) = {1/(4*s_area):.1f} scalars at cutoff a = lP")
    print("   KNOWN (Susskind-Uglum 1994): this cutoff dependence is exactly the renormalisation")
    print("   of 1/G; the horizon 'tension' runs as  1/(4G(mu)) = 1/(4G_0) + c N_species mu^2.")
    print("   -> the known sigma(mu) for the HORIZON sector, with c computed above.")
    return k, s_area


def U4_gap():
    banner("U4  The QCD sector: where the candidate does not (yet) close")
    print("Abelian/free fields: W(C) = <D(alpha)> -> perimeter law (P2), fits U2 exactly.")
    print("Confining SU(3): area law is non-perturbative; no closed-form K is known for a")
    print("region pierced by a flux tube. The precise target that would complete U1+U2:")
    print("   compute the modular Hamiltonian / entanglement of a region cut by a confining")
    print("   string and check whether sigma_QCD appears as its boost-weighted energy,")
    print("   i.e. whether  dS_string = 2 pi sum beta(x) dE_string(x)  with E_string = sigma L.")
    print("Testable toy (next step): 2+1D compact U(1) or Z2 lattice gauge theory - confining,")
    print("small enough for exact diagonalisation.")


def main():
    w = U2_parity()
    res, rows, cl, fl = U1_lattice()
    k, s = U3_area()
    U4_gap()
    return dict(parity_err=w, rows=rows, clausius=cl, first_law=fl, sred=k, s_area=s,
                mid=res[60][1])


if __name__ == "__main__":
    main()
