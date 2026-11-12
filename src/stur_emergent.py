#!/usr/bin/env python3
"""
The question turned around: gravity as a CONSEQUENCE of the quantum level, not a field
that acts on quantum particles from outside.

Already in the repository (KNOWN, computed in stur_unification.py U3):
  the vacuum's entanglement entropy obeys an area law, S = 0.3046 (R/a)^2 per scalar
  field, and Jacobson's argument (1995) turns delta S = delta<K> on every local horizon
  into Einstein's equations, with 1/(4 G hbar) = the entanglement entropy per area.
  TEGR (TEGR.md) is then the field theory that comes out.

What this file asks: IF gravity comes from the quantum level, what does that predict for
the diamond experiment? There are two ways a long-range field can be a consequence of a
quantum medium, and they predict opposite things.

  K1  Newton's G from vacuum entanglement: the cutoff the area law needs.
  K2  COLLECTIVE (like phonons): a 1/r force that emerges from a quantum lattice.
      Two probes, each in two places, coupled only to the medium. Exact dynamics.
      The medium follows each branch, so the probes entangle (lambda = 1). Slow switching
      leaves no record in the medium; sudden switching leaves phonons = which-path info.
  K3  STATISTICAL (like temperature): the field follows the AVERAGE of the quantum level
      (lambda = 0). For that to be consistent the average must be produced by intrinsic
      noise / collapse (Diosi-Penrose type). Its rate for the diamond design.
  K4  The two signatures the experiment measures, and what each would mean.
Labels: KNOWN, FOLLOWS, CHECK, LIT, ANALOG (a lattice model of the mechanism, not gravity).
"""
import numpy as np
import scipy.sparse as sps
import scipy.sparse.linalg as spla

import stur_gravity_entanglement as ge

G, C, HBAR = 6.67430e-11, 2.99792458e8, 1.054571817e-34
L_P = np.sqrt(HBAR * G / C**3)
C_AREA = 0.3046            # computed in stur_unification.py U3 (Srednicki method), per scalar
M_CARBON = 12 * 1.66053907e-27
DONADI_R0 = 0.54e-10       # LIT: Donadi et al., Nat. Phys. 17, 74 (2021): DP smearing R0 > 0.54 A


def banner(s):
    print("\n" + "=" * 78 + "\n" + s + "\n" + "=" * 78)


# --------------------------------------------------------------------------- K1
def cutoff_for_G(n_fields, c_area=C_AREA):
    """Jacobson: S = A / (4 G hbar) per unit area on every horizon. Entanglement: S = N c
    (R/a)^2 = N c A / (4 pi a^2). Equal  ->  a = l_P sqrt(N c / pi)."""
    return L_P * np.sqrt(n_fields * c_area / np.pi)


# --------------------------------------------------------------------------- K2
def laplacian_3d(L):
    """Lattice -Laplacian on an L^3 cube, Dirichlet walls (spacing 1)."""
    e = np.ones(L)
    D = sps.diags([-e[:-1], 2 * e, -e[:-1]], [-1, 0, 1])
    I = sps.identity(L)
    return (sps.kron(sps.kron(D, I), I) + sps.kron(sps.kron(I, D), I) + sps.kron(sps.kron(I, I), D)).tocsc()


def idx(L, x, y, z):
    return (x * L + y) * L + z


def green_profile(L=81, r_ref=12, rs=(2, 3, 4, 6, 8)):
    """Static response G = K^-1 of the quantum medium to a point source at the centre.
    The walls add a nearly constant offset near the centre, so the force law is tested
    through potential DIFFERENCES: G(r) - G(r_ref) vs (1/r - 1/r_ref) / (4 pi)."""
    K = laplacian_3d(L)
    c = L // 2
    src = np.zeros(L**3)
    src[idx(L, c, c, c)] = 1.0
    Gc, info = spla.cg(K, src, rtol=1e-12, maxiter=5000)
    assert info == 0
    ref = Gc[idx(L, c + r_ref, c, c)]
    return [(r, Gc[idx(L, c + r, c, c)] - ref, (1 / r - 1 / r_ref) / (4 * np.pi)) for r in rs]


def medium_modes(L):
    K = laplacian_3d(L).toarray()
    w2, U = np.linalg.eigh(K)
    return np.sqrt(w2), U


def probe_sites(L, sep=6, split=2):
    """Parallel geometry: A at x = c - sep/2, B at x = c + sep/2; branches at y = c -+ split/2."""
    c = L // 2
    A = [idx(L, c - sep // 2, c - split // 2, c), idx(L, c - sep // 2, c + split // 2, c)]
    B = [idx(L, c + sep // 2, c - split // 2, c), idx(L, c + sep // 2, c + split // 2, c)]
    return A, B


def envelope(t, t_ramp, t_hold, sudden=False):
    if sudden:
        return np.where((t >= 0) & (t <= t_hold), 1.0, 0.0)
    total = t_hold + 2 * t_ramp
    up = np.clip(t / t_ramp, 0, 1)
    dn = np.clip((total - t) / t_ramp, 0, 1)
    s = lambda u: np.sin(np.pi * u / 2) ** 2
    return np.minimum(s(up), s(dn))


def medium_evolution(L=14, g=1.9, t_ramp=40.0, t_hold=120.0, sudden=False, nt=6000, mean_field=False):
    """Exact evolution of the quantum medium (all normal modes) driven by the two probes.
    H = sum_k w_k a_k^+ a_k + h(t) sum_k f_k(config) (a_k + a_k^+),
    f_k = g sum_probes u_k(site) / sqrt(2 w_k).  For each of the 4 branch configurations:
      displacement alpha_k = -i int f h(t') e^{i w t'} dt'   (interaction picture, end of run)
      phase        Phi     = +int dt int_{t'<t} f^2 h(t) h(t') sin(w (t - t'))  (state e^{i Phi})
    mean_field=True: the medium is driven by the AVERAGE source (each probe's two sites
    with weight 1/2) and each probe feels the field of that average (lambda = 0).
    Returns the 4x4 reduced probe state, the medium overlaps and the entangling phase."""
    w, U = medium_modes(L)
    A, B = probe_sites(L)
    total = t_hold + 2 * t_ramp if not sudden else t_hold
    t = np.linspace(0, total, nt)
    dt = t[1] - t[0]
    h = envelope(t, t_ramp, t_hold, sudden)
    # time integrals per mode
    eiw = np.exp(1j * np.outer(w, t))                              # (modes, nt)
    I1 = (eiw * h).sum(axis=1) * dt                                 # int h e^{iwt}
    # Phi kernel: int dt h(t) int_0^t h(t') sin(w(t-t')) dt' = Im[ int h(t) e^{iwt} conj(int_0^t h e^{iwt'}) ]
    cum = np.cumsum(eiw * h, axis=1) * dt
    K2 = (np.imag(eiw * h * np.conj(cum))).sum(axis=1) * dt
    configs = [(i, j) for i in range(2) for j in range(2)]
    u = lambda site: U[site, :] / np.sqrt(2 * w)
    if not mean_field:
        f = {c: g * (u(A[c[0]]) + u(B[c[1]])) for c in configs}
        alpha = {c: -1j * f[c] * I1 for c in configs}
        Phi = {c: (f[c] ** 2 * K2).sum() for c in configs}            # second-order Magnus phase
    else:
        # field sourced by the averaged probes; each branch couples to that classical field
        fbar = g * 0.5 * (u(A[0]) + u(A[1]) + u(B[0]) + u(B[1]))
        alpha = {c: -1j * fbar * I1 for c in configs}               # same medium state for all branches
        # energy of branch (i, j) in the mean field: cross terms with the OTHER probe's average only
        fA = {i: g * u(A[i]) for i in range(2)}
        fB = {j: g * u(B[j]) for j in range(2)}
        fBbar = 0.5 * (fB[0] + fB[1])
        fAbar = 0.5 * (fA[0] + fA[1])
        Phi = {(i, j): 2 * ((fA[i] * fBbar + fAbar * fB[j]) * K2).sum() for (i, j) in configs}
    # reduced probe state: rho_{c,c'} = 1/4 <alpha_c'|alpha_c> e^{i(Phi_c - Phi_c')}
    rho = np.zeros((4, 4), complex)
    for a, ca in enumerate(configs):
        for b, cb in enumerate(configs):
            d = alpha[ca] - alpha[cb]
            ov = np.exp(-0.5 * np.sum(np.abs(d) ** 2) + 1j * np.imag(np.sum(np.conj(alpha[cb]) * alpha[ca])))
            rho[a, b] = 0.25 * ov * np.exp(1j * (Phi[ca] - Phi[cb]))
    ph = np.array([[Phi[(0, 0)], Phi[(0, 1)]], [Phi[(1, 0)], Phi[(1, 1)]]])
    dphi = ph[0, 0] + ph[1, 1] - ph[0, 1] - ph[1, 0]
    # which-path record left in the medium: overlap of medium states for A's two branches
    record = abs(np.exp(-0.5 * np.sum(np.abs(alpha[(0, 0)] - alpha[(1, 0)]) ** 2)))
    # static prediction: cross energy -g^2 G(a, b) for each branch pair, so the entangling
    # phase is g^2 tau_eff [G(A0,B0)+G(A1,B1)-G(A0,B1)-G(A1,B0)], tau_eff = int h^2 dt
    Gm = (U / w**2) @ U.T
    tau_eff = (h**2).sum() * dt
    static = g**2 * tau_eff * (Gm[A[0], B[0]] + Gm[A[1], B[1]] - Gm[A[0], B[1]] - Gm[A[1], B[0]]) \
        if not mean_field else 0.0
    return dict(rho=rho, dphi=dphi, static=static, record=record, neg=ge.negativity(rho))


# --------------------------------------------------------------------------- K3
def dp_rate(m, R, d):
    """Diosi-Penrose: Gamma = (G / 2 hbar) int int (rho1 - rho2)(x)(rho1 - rho2)(y) / |x - y|
    for a uniform sphere displaced by d >= 2R: = (G m^2 / hbar)(6/(5R) - 1/d).
    (Conventions differ by a factor 2 between Diosi and Penrose.)"""
    return G * m**2 / HBAR * (6 / (5 * R) - 1 / d)


def dp_crystal_extra(m, R0=DONADI_R0):
    """Extra DP rate from the lumpiness of the crystal: each carbon nucleus smeared over R0,
    N = m / m_C nuclei, each adding (G m_C^2 / hbar)(6 / (5 R0))."""
    return (m / M_CARBON) * G * M_CARBON**2 / HBAR * 6 / (5 * R0)


def main():
    banner("K1  Newton's G as a consequence of vacuum entanglement (Jacobson + area law)")
    print(f"   Area law per scalar field (stur_unification.py U3): S = {C_AREA} (R/a)^2")
    for N in (1, 10, 100, 1000):
        print(f"   N = {N:4d} quantum fields: G comes out right if the cutoff a = {cutoff_for_G(N)/L_P:.3f} l_P")
    print("   FOLLOWS: the strength of gravity is fixed by how much the quantum vacuum is")
    print("   entangled, counted down to a cutoff of order the Planck length. On this reading")
    print("   the Planck length is where the counting stops (where the numbers break down),")
    print("   not where reality does: it is the spacing of whatever the quantum level is made of.")

    banner("K2  COLLECTIVE: a 1/r force that emerges from a quantum medium (ANALOG, exact)")
    print("   Medium: a 3D lattice of coupled quantum oscillators (the 'quantum level').")
    print("   Static response to a point source (81^3 lattice), potential relative to r = 12,")
    print("   vs the 1/r law of Newton (and Coulomb):")
    for r, Gl, Gc in green_profile():
        print(f"     r = {r}: lattice {Gl:.5f}   (1/r - 1/12)/(4 pi) {Gc:.5f}   ratio {Gl/Gc:.4f}")
    print("   Two probes, each in two places, coupled ONLY to the medium (14^3 lattice, all")
    print("   2744 modes, exact):")
    print("   switching                     entangling phase   static 1/r prediction   negativity   which-path record in medium")
    for label, kw in [("slow (adiabatic)", {}), ("sudden", {"sudden": True}),
                      ("slow, MEAN-FIELD medium", {"mean_field": True})]:
        r = medium_evolution(**kw)
        print(f"   {label:28s}  {r['dphi']:+16.4f}   {r['static']:+20.4f}   {r['neg']:10.4f}"
              f"   {1 - r['record']:.1e}")
    print("   FOLLOWS: a field that is a consequence of a quantum medium follows EACH branch")
    print("   of its sources. The probes entangle through it, with the phase of the emergent")
    print("   1/r law to 0.3% (lambda = 1). Slow switching leaves the medium in its vacuum: no")
    print("   record, full entanglement. Sudden switching leaves phonons that carry which-path")
    print("   information, and here that record is enough to destroy the entanglement (the")
    print("   analogue of TEGR.md E6, where gravity's record is 1e-59 gravitons). Only by")
    print("   replacing the medium with its average (mean field) does the entanglement vanish.")
    print("   LIT: this is how trapped-ion quantum gates work: the ions' collective motion, a")
    print("   field emerging from the ions themselves, entangles them (Molmer-Sorensen 1999).")

    banner("K3  STATISTICAL: gravity follows the AVERAGE of the quantum level (lambda = 0)")
    import stur_gravity_full as GF
    A = GF.design_a()
    m, R = A["m"], A["R"]                                   # design A
    print("   An average is only well defined if something produces it: intrinsic noise or")
    print("   collapse. The parameter-free version is Diosi-Penrose (gravity-induced collapse).")
    for d in (250e-6, A["dx"]):
        Gm = dp_rate(m, R, d)
        print(f"   Diamond {m:.3e} kg, R = {R*1e6:.3f} um, split {d*1e6:.0f} um:  DP rate {Gm:.0f} /s"
              f"  -> superposition lifetime {1e3/Gm:.1f} ms (x2 by convention)")
    print(f"   Crystal lumpiness (nuclei smeared over R0 = {DONADI_R0*1e10:.2f} A, LIT bound): extra"
          f" {dp_crystal_extra(m):.1e} /s (negligible)")
    print("   Design A needs 3.2 s of coherence. Under DP the superposition is gone ~500x sooner.")
    print("   LIT: Donadi et al. 2021 excluded the simplest DP (R0 < 0.54 A) from the absence of")
    print("   the radiation it predicts; versions with larger R0 survive and are tested here.")

    banner("K4  What the experiment measures, read the right way round")
    print("   If gravity is a consequence of the quantum level, the question is WHICH kind:")
    print("   gravity is ...                 two diamonds entangle?   ONE diamond keeps its 3 s superposition?")
    print("   collective (phonon-like)       yes  (lambda = 1)        yes")
    print("   statistical (average + noise)  no   (lambda = 0)        no: DP-type collapse in ~6 ms")
    print("   FOLLOWS: the second column needs only ONE diamond. A single-diamond interferometer")
    print("   at design A's mass and split already tells the two apart, before any entanglement")
    print("   run. The two-diamond witness then confirms the collective reading.")
    print("   Your picture (all things, gravity included, are consequences of the quantum level)")
    print("   does not need gravity to be 'quantized' separately: a field that emerges from")
    print("   quantum constituents is automatically in two places when they are (K2). That is")
    print("   the lambda = 1 prediction, reached from the quantum side.")


if __name__ == "__main__":
    main()
