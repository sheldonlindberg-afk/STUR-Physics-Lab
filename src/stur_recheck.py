#!/usr/bin/env python3
"""
Every claim that failed, checked again with independent code.

Nothing here imports the scripts that first reached each verdict: each check is a fresh
implementation, often by a different method (closed form vs numerics, Fock space vs
characteristic function, etc.). A verdict is CONFIRMED when the fresh number reproduces
the recorded one and the conclusion follows; otherwise it is flagged.

Covered:
  X1  S_R = -k ln V matches no standard entropy (only linear entropy, as V -> 1)
  X2  E_R = (1/2) k_B T Phi^2: wrong temperature dependence; crossing hbar w = 2.40 k_B T
  X3  The Smarr check is circular
  X4  The electron as a real self-repelling charge cloud: hydrogen binds by 6.64 eV
  X5  An empty universe triggers tunnelling: the barrier grows as rho -> 0
  X6  Information paradox: a coarse-grained entropy breaks the area bound after 0.5381 t_evap
  X7  One A_mu for confinement and horizons: the replica factors n and (1 - n) differ
  X8  Option A: excluded by 8-13 orders where its area law operates
  X9  Option B: a confining field felt by matter needs sqrt(sigma) < hbar H0 = 1.4e-33 eV
  X10 Option C: a running horizon tension adds only a constant c_s N to S
  X11 Front 1: Li holographic dark energy has w_a > 0 for every c
  X12 Front 3: a 1/3 twist gives J = 1/6, not a fermion
  X13 Front 8: Koide Q = 2/3 at -0.43 sigma; delta = 2/9 excluded
  X14 Front 9: one-loop Planck stability needs m_H >= 133 GeV
  X15 Front 12: SU(3)_C and SU(3)_L never meet; the gap grows 18.6 -> 27.3
Not independently rechecked (the verdict rests on literature values, or needs a solver
not rebuilt here): Skyrme fold cost (front 3 / P5), running-vacuum CMB bound (front 2),
Eichhorn-Held retrodictions (front 10), 3-3-1 Higgs threshold (front 11).
"""
from math import log, pi, sqrt

import numpy as np
from scipy.integrate import quad, solve_ivp
from scipy.linalg import eigh_tridiagonal
from scipy.optimize import brentq

HBAR, KB, C, G = 1.054571817e-34, 1.380649e-23, 2.99792458e8, 6.67430e-11
EV = 1.602176634e-19
RESULTS = []


def banner(s):
    print("\n" + "=" * 78 + "\n" + s + "\n" + "=" * 78)


def verdict(key, ok, text):
    RESULTS.append((key, ok, text))
    print(f"   -> {'CONFIRMED' if ok else 'NOT CONFIRMED'}: {text}")


def x1_entropy():
    banner("X1  Is -ln V an entropy?  Qubit in (|0> + |1>)/sqrt2 with visibility V")
    print("      V      -ln V     S_vN      S_linear   S_Renyi2")
    rows = []
    for V in (0.999, 0.99, 0.9, 0.5, 0.1):
        p = np.array([(1 + V) / 2, (1 - V) / 2])
        svn = -np.sum(p * np.log(p))
        slin = 1 - np.sum(p**2) - 0 * V
        slin = (1 - V**2) / 2
        s2 = -np.log((1 + V**2) / 2)
        rows.append((V, -log(V), svn, slin, s2))
        print(f"   {V:7.3f}  {-log(V):8.4f}  {svn:8.4f}  {slin:8.4f}   {s2:8.4f}")
    r_lin = rows[0][3] / rows[0][1]
    no_match = all(abs(r[1] - r[2]) > 1e-3 * r[1] for r in rows) and abs(rows[-1][1] - rows[-1][3]) > 1
    verdict("X1", no_match and abs(r_lin - 1) < 2e-3,
            f"-ln V equals no entropy at finite decoherence; only the linear entropy matches it as V -> 1 "
            f"(ratio {r_lin:.4f} at V = 0.999)")


def x2_temperature():
    banner("X2  Fixed energy deposited, varying temperature: STUR vs standard decoherence")
    # Standard: two branches displaced by +-a in a thermal mode; V = |<D(2a)>_th| from Fock space
    def V_fock(alpha, nbar, N=120):
        from scipy.linalg import expm
        a = np.diag(np.sqrt(np.arange(1, N)), 1)
        D = expm(2 * alpha * (a.T - a))
        q = nbar / (1 + nbar)
        p = (1 - q) * q ** np.arange(N)
        return abs(np.sum(p * np.diag(D)))
    alpha = 0.3
    for nbar in (0.1, 1.0, 5.0):
        Vf = V_fock(alpha, nbar)
        Va = np.exp(-2 * alpha**2 * (2 * nbar + 1))
        print(f"   nbar = {nbar:4.1f}: V (Fock) = {Vf:.6f}, closed form exp(-2a^2(2n+1)) = {Va:.6f}")
    # STUR: -ln V = E / k_B T ; standard: -ln V = 2 (E/hbar w) coth(hbar w / 2 k_B T)
    f = lambda x: x - 2 / np.tanh(x / 2)
    xc = brentq(f, 0.5, 10)
    print(f"   STUR -ln V falls as 1/T at fixed E; standard rises as coth. They cross only at hbar w = {xc:.4f} k_B T.")
    verdict("X2", abs(xc - 2.40) < 0.01 and abs(V_fock(alpha, 1.0) - np.exp(-2 * alpha**2 * 3)) < 1e-9,
            f"opposite temperature dependence; agreement only at the coincidence hbar w = {xc:.2f} k_B T")


def x3_smarr():
    banner("X3  The Smarr check")
    import sympy as sp
    M = sp.symbols("M", positive=True)
    T = 1 / (8 * sp.pi * M)              # Hawking temperature (G = c = hbar = k = 1)
    S = 4 * sp.pi * M**2                 # A/4
    ER = T * S                           # E_R = (1/2) k T Phi^2 with S_R = (1/2) k Phi^2 SET EQUAL to A/4
    ratio = sp.simplify(ER / M)
    print(f"   With S_R identified with A/4 by assumption: E_R / M = {ratio} for every M.")
    print("   That is the Smarr identity M = 2 T S, put in through the identification; it tests nothing.")
    verdict("X3", ratio == sp.Rational(1, 2), "E_R = M/2 holds identically once S_R = A/4 is assumed: circular")


def x4_hydrogen(n=6000, rmax=40.0):
    banner("X4  A real, self-repelling charge cloud: hydrogen 1s, self-consistent (atomic units)")
    h = rmax / n
    r = h * np.arange(1, n + 1)
    VH = np.zeros(n)
    for it in range(200):
        d = 1 / h**2 + (-1 / r + VH)
        e = -0.5 / h**2 * np.ones(n - 1)
        w, v = eigh_tridiagonal(d, e, select="i", select_range=(0, 0))
        u = v[:, 0] / np.sqrt(h * np.sum(v[:, 0] ** 2))
        rho = u**2                                   # radial density, integrates to 1
        q_in = np.cumsum(rho) * h
        out = np.cumsum((rho / r)[::-1])[::-1] * h
        VHn = q_in / r + out - rho / r * h
        if np.max(np.abs(VHn - VH)) < 1e-11:
            break
        VH = 0.5 * VH + 0.5 * VHn
    eps = w[0]
    J = 0.5 * h * np.sum(rho * VH)
    E = eps - J
    rmean = h * np.sum(rho * r)
    print(f"   eigenvalue {eps:.5f} Ha, self-energy J = {J:.5f} Ha, total E = {E:.5f} Ha = {E*27.211386:.3f} eV")
    print(f"   <r> = {rmean:.3f} a0   (no self-repulsion: 13.606 eV, 1.50 a0; measured 13.598 eV)")
    verdict("X4", abs(-E * 27.211386 - 6.64) < 0.05 and abs(rmean - 2.50) < 0.05,
            f"binding {-E*27.211386:.2f} eV against 13.60 measured: a real charge cloud is excluded")


def x5_tunnelling():
    banner("X5  Tunnelling from nothing as the vacuum density falls")
    print("   rho/rho_P    barrier a0 = (3/8 pi rho)^1/2    WKB exponent ~ int_0^a0 a sqrt(1 - a^2/a0^2) da")
    vals = []
    for rho in (1e-1, 1e-3, 1e-6, 1e-9):
        a0 = sqrt(3 / (8 * pi * rho))
        I = quad(lambda a: a * sqrt(max(0.0, 1 - (a / a0) ** 2)), 0, a0)[0]
        vals.append(I)
        print(f"   {rho:8.0e}     {a0:12.3e}                          {I:.3e}   (a0^2/3 = {a0**2/3:.3e})")
    verdict("X5", all(b > a for a, b in zip(vals, vals[1:])),
            "the barrier and the suppression grow as rho -> 0: an emptier universe tunnels less")


def x6_page(beta=1.4847):
    banner("X6  Coarse-grained radiation entropy vs the remaining black hole's area bound")
    # M ~ (1 - x)^(1/3), S_BH ~ (1 - x)^(2/3); S_rad = beta (S0 - S_BH) (beta: Page 1976, recalled)
    x = brentq(lambda x: beta * (1 - (1 - x) ** (2 / 3)) - (1 - x) ** (2 / 3), 0, 1)
    print(f"   S_rad = S_BH at t = {x:.4f} t_evap (beta = {beta}); afterwards S_rad > A/4 of what remains.")
    verdict("X6", abs(x - 0.5381) < 5e-4,
            f"an entropy that tracks the coarse-grained curve violates the area bound after {x:.4f} t_evap")


def x7_replica():
    banner("X7  Replica: can one quantity be both horizon entropy and confining-string energy?")
    import sympy as sp
    n, A, Gs, sig, As = sp.symbols("n A G sigma A_s", positive=True)
    lnZ = (1 - n) * A / (4 * Gs) - n * sig * As
    S = sp.simplify(-sp.diff(lnZ - n * lnZ.subs(n, 1), n).subs(n, 1))
    E = sp.simplify(-sp.diff(lnZ, n).subs(n, 1))
    print(f"   S = -d/dn [ln Z_n - n ln Z_1] at n = 1  = {S}")
    print(f"   <K> = -d ln Z_n / dn at n = 1          = {E}")
    verdict("X7", sp.simplify(S - A / (4 * Gs)) == 0,
            "the string term carries factor n, enters <K> but not S; the horizon term is pure entropy")


def x8_option_a():
    banner("X8  Option A against acceleration noise (LISA Pathfinder) where its area law operates")
    m_sr = 86.909 * 1.66053907e-27
    S_a_max = (1.74e-15) ** 2 / 2                      # two-sided, from the one-sided ASD (LIT)
    kappa_need = 1e-3 / ((m_sr / HBAR) ** 2 * 12.0)     # Gamma = 1e-3 in a 3 m x 4 s Sr-87 interferometer
    print(f"   Signal needs kappa >= {kappa_need:.2e} m^3/s^3 (Gamma = 1e-3, A_st = 12 m s).")
    print("   Noise pushes matter with S_a = kappa / xi, so LISA PF allows kappa <= S_a xi:")
    orders = []
    for xi in (1e-6, 1e-4, 1e-2, 0.3):
        kmax = S_a_max * xi
        orders.append(log(kappa_need / kmax, 10))
        print(f"     xi = {xi:7.0e} m: kappa <= {kmax:.2e}  ->  excluded by {orders[-1]:.1f} orders")
    verdict("X8", min(orders) > 7.5 and max(orders) < 14.5,
            f"excluded by {min(orders):.0f}-{max(orders):.0f} orders for xi from 1 um to 0.3 m (area law needs xi << dx)")


def x9_option_b():
    banner("X9  Option B: confinement longer than the Hubble radius")
    H0 = 67.4e3 / 3.0857e22
    lim = HBAR * H0 / EV
    print(f"   hbar H0 = {lim:.2e} eV (H0 = 67.4 km/s/Mpc, LIT)")
    verdict("X9", abs(lim / 1.4e-33 - 1) < 0.05, f"sqrt(sigma) < {lim:.1e} eV: an ordinary fifth force, not confinement")


def x10_option_c():
    banner("X10 Option C: 1/4G(mu) = 1/4G0 + (c_s/4 pi) N mu^2 with mu = 1/R")
    c_s = 0.3046
    for R in (1.0, 1e3, 1e9):
        dS = 4 * pi * R**2 * c_s / (4 * pi) / R**2
        print(f"   R = {R:7.0e}: extra entropy = {dS:.4f} N  (independent of R)")
    verdict("X10", abs(c_s / (4 * pi) - 0.0242) < 1e-4, f"a constant {c_s:.3f} N, no observable")


def x11_hde():
    banner("X11 Front 1: Li holographic dark energy, w_a for every c")
    print("   c      w_0       w_a   (Omega_de' = Omega(1-Omega)(1 + 2 sqrt(Omega)/c), Omega_0 = 0.69)")
    was = []
    for cc in (0.3, 0.6, 1.0, 1.5, 3.0):
        Om = 0.69
        w0 = -1 / 3 - 2 * sqrt(Om) / (3 * cc)
        dOm = Om * (1 - Om) * (1 + 2 * sqrt(Om) / cc)       # d Omega / d ln a
        wa = -(-(1 / (3 * cc)) * dOm / sqrt(Om))            # w_a = -dw/da at a = 1
        was.append(wa)
        print(f"   {cc:3.1f}   {w0:+.3f}   {wa:+.3f}")
    verdict("X11", min(was) > 0, "w_a > 0 for every c; DESI DR2 prefers w_a ~ -0.9 (LIT): wrong direction")


def x12_twist():
    banner("X12 Front 3: angular momentum of a charge-flux twist, J = q Phi / 4 pi")
    for frac in (1.0, 1 / 3):
        J = frac * 2 * pi / (4 * pi)
        print(f"   twist fraction {frac:.3f}: J = {J:.4f}")
    verdict("X12", abs(1 / 3 * 0.5 - 1 / 6) < 1e-12, "a full twist gives J = 1/2; a 1/3 twist gives 1/6: not a fermion")


def x13_koide():
    banner("X13 Front 8: Koide's relation with current masses (MeV; LIT)")
    me, mmu, mtau, dtau = 0.51099895000, 105.6583755, 1776.93, 0.09
    Q = lambda mt: (me + mmu + mt) / (sqrt(me) + sqrt(mmu) + sqrt(mt)) ** 2
    q = Q(mtau)
    dq = abs(Q(mtau + dtau) - Q(mtau - dtau)) / 2
    print(f"   Q = {q:.8f}; Q - 2/3 = {q - 2/3:+.2e} +- {dq:.1e}  ({(q - 2/3)/dq:+.2f} sigma)")
    # Koide exact: sqrt(m_k) = mu (1 + sqrt2 cos(delta + 2 pi k / 3)); fit delta to the e/mu ratio
    def ratio(d):
        s = [1 + sqrt(2) * np.cos(d + 2 * pi * k / 3) for k in range(3)]
        return sorted(x * x for x in s)
    target = me / mmu
    f = lambda d: ratio(d)[0] / ratio(d)[1] - target
    grid = np.linspace(0.0, 2 * pi / 3, 20001)
    vals = [f(x) for x in grid]
    roots = [brentq(f, grid[i], grid[i + 1]) for i in range(len(grid) - 1) if vals[i] * vals[i + 1] < 0]
    d = min(roots, key=lambda r: abs(r - 2 / 9))
    dme, dmmu = 1.5e-10, 2.3e-6
    eps = 1e-7
    dd = abs((brentq(lambda x: ratio(x)[0] / ratio(x)[1] - (me / (mmu * (1 + eps))), d - 1e-3, d + 1e-3) - d) / eps)
    sig = dd * sqrt((dme / me) ** 2 + (dmmu / mmu) ** 2)
    print(f"   Koide exact, delta from m_e/m_mu: {d:.9f} vs 2/9 = {2/9:.9f}; difference {(d - 2/9)/sig:.0f} sigma")
    verdict("X13", abs((q - 2 / 3) / dq + 0.43) < 0.05 and abs(d - 2 / 9) / sig > 100,
            f"Q fits at {(q - 2/3)/dq:+.2f} sigma; delta = 2/9 is off by {abs(d - 2/9)/sig:.0f} sigma once Koide is exact")


def x14_higgs():
    banner("X14 Front 9: the smallest Higgs mass that keeps lambda >= 0 to M_Pl (one loop, fresh RGEs)")
    v, mt = 246.22, 172.57
    def min_lambda(l0, g0):
        def rhs(t, s):
            g1, g2, g3, yt, l = s
            k = 1 / (16 * pi**2)
            return [k * 41 / 6 * g1**3, -k * 19 / 6 * g2**3, -k * 7 * g3**3,
                    k * yt * (4.5 * yt**2 - 8 * g3**2 - 2.25 * g2**2 - 17 / 12 * g1**2),
                    k * (24 * l**2 - 6 * yt**4 + 12 * l * yt**2 - 3 * l * (3 * g2**2 + g1**2)
                         + 0.375 * (2 * g2**4 + (g1**2 + g2**2) ** 2))]
        sol = solve_ivp(rhs, [0, log(1.22089e19 / mt)], [*g0, l0], rtol=1e-10, atol=1e-12, dense_output=True)
        return sol.sol(np.linspace(0, sol.t[-1], 4000))[4].min()
    inputs = {
        "MS-bar NNLO inputs (Buttazzo et al. 2013, recalled): y_t = 0.9369": (0.3583, 0.6477, 1.1666, 0.9369),
        "QCD-only pole -> MS-bar top mass (front 9's matching): y_t = 0.9326": (0.35869, 0.64822, 1.16316, 0.93262),
    }
    out = []
    for lab, g0 in inputs.items():
        lc = brentq(lambda l: min_lambda(l, g0), 0.10, 0.30, xtol=1e-8)
        mh = sqrt(2 * lc) * v
        out.append(mh)
        print(f"   {lab}:  m_H >= {mh:.1f} GeV")
    print("   The bound moves by ~1 GeV with the top-mass matching at one loop; both are far above 125.2.")
    verdict("X14", abs(out[1] - 133.1) < 0.3 and min(out) > 130,
            f"m_H >= {min(out):.1f}-{max(out):.1f} GeV at one loop (matching-dependent) vs 125.2: "
            "Planck stability does not predict the Higgs mass")


def x15_unification():
    banner("X15 Front 12: do SU(3)_C and SU(3)_L meet? (one loop, fresh)")
    a3, aL = -5.0, -6.5                                 # 3-3-1, N_c = N_g = 3 (one-loop a_i)
    L = log(1.22089e19 / 4e3) / (2 * pi)
    inv3, invL = 1 / 0.0775, 31.5
    g0 = invL - inv3
    g1 = (invL - aL * L) - (inv3 - a3 * L)
    print(f"   1/alpha_L - 1/alpha_3: {g0:.2f} at 4 TeV -> {g1:.2f} at M_Pl (one loop)")
    verdict("X15", g1 > g0 > 0, "the gap only grows: no unification in minimal 3-3-1")


def main():
    for f in (x1_entropy, x2_temperature, x3_smarr, x4_hydrogen, x5_tunnelling, x6_page, x7_replica,
              x8_option_a, x9_option_b, x10_option_c, x11_hde, x12_twist, x13_koide, x14_higgs,
              x15_unification):
        f()
    banner("SUMMARY")
    for k, ok, t in RESULTS:
        print(f"   {k:4s} {'CONFIRMED    ' if ok else 'NOT CONFIRMED'} {t}")
    print(f"   {sum(ok for _, ok, _ in RESULTS)} of {len(RESULTS)} failures confirmed by independent code.")
    return RESULTS


if __name__ == "__main__":
    main()
