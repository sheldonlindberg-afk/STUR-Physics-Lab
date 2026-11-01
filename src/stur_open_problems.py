#!/usr/bin/env python3
"""
STUR open problems #2-#7, tested against known physics.

  P2  Which connection is A_mu?            (requirements matrix + computed checks)
  P3  sigma(mu)                             (what the 38 orders are; one candidate flow)
  P4  QCD loop area vs horizon area         (Euclidean gravity: how area enters)
  P5  Quark quantum numbers from folds      (Skyrme quantisation; fractional folds)
  P6  Bounce density rho_c, barrier R(rho)  (holographic bound on the Hubble sphere)
  P7  Information paradox                   (Page curve vs the STUR entropy)

Labels used in the printout:  KNOWN, FOLLOWS, STUR, CHECK, LIT (literature input,
not recomputed here).  numpy + scipy required; matplotlib optional.
"""
import os
import numpy as np
from scipy.integrate import solve_ivp, quad
from scipy.optimize import brentq
from scipy.special import erf

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "results", "open_problems")

# CODATA 2018
c, G, hbar, kB = 2.99792458e8, 6.67430e-11, 1.054571817e-34, 1.380649e-23
eV = 1.602176634e-19
GeV = 1e9 * eV
Msun = 1.98847e30
amu = 1.66053906660e-27
lP = np.sqrt(hbar * G / c**3)
EP_GeV = np.sqrt(hbar * c**5 / G) / GeV                 # Planck energy
hbarc_GeVm = hbar * c / GeV                            # GeV * m
rhoP = c**7 / (hbar * G**2)                            # Planck energy density, J/m^3


def banner(s):
    print("\n" + "=" * 78 + "\n" + s + "\n" + "=" * 78)


# ===========================================================================
# P2  Which connection?
# ===========================================================================
def wilson_u1_square(L, a, e2, h=None):
    """Free Euclidean 4D U(1): <Phi^2> = e^2 ∮∮ dx.dy D(x-y), D = 1/(4 pi^2 (r^2+a^2))."""
    h = h or a / 2
    n = int(round(L / h))
    s = (np.arange(n) + 0.5) * h
    pts, tan = [], []
    for (x0, y0, tx, ty) in [(0, 0, 1, 0), (L, 0, 0, 1), (L, L, -1, 0), (0, L, 0, -1)]:
        pts.append(np.c_[x0 + tx * s, y0 + ty * s])
        tan.append(np.tile([tx, ty], (n, 1)))
    P, T = np.vstack(pts), np.vstack(tan)
    r2 = ((P[:, None, :] - P[None, :, :]) ** 2).sum(-1)
    return e2 * h * h * np.sum((T @ T.T) / (4 * np.pi**2 * (r2 + a * a)))


def immirzi():
    j = np.arange(1, 4000) / 2
    gm = brentq(lambda g: np.sum((2 * j + 1) * np.exp(-2 * np.pi * g * np.sqrt(j * (j + 1)))) - 1, .05, 1)
    me = brentq(lambda g: np.sum(2 * np.exp(-2 * np.pi * g * np.sqrt(j * (j + 1)))) - 1, .05, 1)
    return np.log(2) / (np.pi * np.sqrt(3)), me, gm


def P2():
    banner("P2  Which connection is A_mu?  Requirements R1-R5 tested per candidate")
    print("R1 holonomy of a gauge connection   R2 Gaussian (V = exp(-<Phi^2>/2))")
    print("R3 area law at the QCD scale        R4 horizon entropy A/4lP^2")
    print("R5 couples to a neutral-atom interferometer (needed for any lab test)")

    print("\n[R3 for U(1) in 4D]  free Maxwell, square loops, e^2 = 4 pi alpha, cutoff a:")
    e2 = 4 * np.pi / 137.035999
    Ls = np.array([10, 20, 40, 80, 160.0])
    W = np.array([wilson_u1_square(L, 1.0, e2) for L in Ls])
    for L, w in zip(Ls, W):
        print(f"   L/a = {L:5.0f}   <Phi^2> = {w:.5f}   <Phi^2>/(4L) = {w/(4*L):.6f}   <Phi^2>/L^2 = {w/L**2:.2e}")
    X = np.c_[Ls**2, 4 * Ls, np.log(Ls), np.ones_like(Ls)]
    coef = np.linalg.lstsq(X, W, rcond=None)[0]
    print(f"   fit <Phi^2> = A*L^2 + p*(4L) + k ln L + c:  A = {coef[0]:.2e}, p = {coef[1]:.5f}, k = {coef[2]:.4f}")
    print("   -> perimeter law (A consistent with 0). KNOWN. U(1) in 4D fails R3.")

    print("\n[R3 mechanism]  Gaussian field strength with correlation length xi (stochastic vacuum):")
    print("   <Phi^2> = C0 g(L)^2, g = xi^2[(L/xi) sqrt(pi) erf(L/xi) + exp(-L^2/xi^2) - 1]")
    for Lx in [0.1, 1, 10, 100]:
        g = Lx * np.sqrt(np.pi) * erf(Lx) + np.exp(-Lx**2) - 1
        print(f"   L/xi = {Lx:6.1f}   <Phi^2>/(C0 pi xi^2 L^2) = {g**2/(np.pi*Lx**2):.4f}")
    print("   -> area law with sigma = (pi/2) C0 xi^2 iff field strength has a FINITE correlation")
    print("      length (a mass gap). KNOWN. Massless fields (photon, graviton) do not.")

    print("\n[R4]  Horizon entropy from a connection: loop quantum gravity, SU(2) Ashtekar-Barbero")
    g_abck, g_me, g_gm = immirzi()
    print(f"   Immirzi parameter fixed BY DEMANDING S = A/4lP^2:  ABCK {g_abck:.6f},"
          f"  Meissner {g_me:.6f},  Ghosh-Mitra {g_gm:.6f}  (LIT values reproduced)")
    print("   -> R4 is met only by fitting gamma to the answer; 1/4 is input, not output.")

    print("\n[R5]  Phases for a Rb-87 interferometer, MAGIS-like (T = 1 s, k_eff = 4 pi/780 nm):")
    keff, g0, T = 4 * np.pi / 780e-9, 9.81, 1.0
    print(f"   gravity (metric, mass-dependent) COW phase k g T^2  = {keff*g0*T**2:.3e} rad   KNOWN")
    Rz = 2 * 3.986004e14 / (6.371e6) ** 3 / c**2
    dz = 1.0
    print(f"   spin-connection holonomy: Riemann R_0z0z = {Rz:.2e} m^-2, area c T dz (dz = {dz} m)"
          f" -> boost angle {Rz*c*T*dz:.1e}")
    print(f"   vacuum graviton fluctuation scale (lP/L)^2 at L = 1 m = {(lP/1.0)**2:.1e}  (dimensional)")
    print("   U(1) EM and SU(3) colour: atom is neutral and a colour singlet -> 0 at tree level")

    print("\n   Matrix (P pass / F fail / - n.a.):")
    print("   candidate                 R1  R2  R3  R4  R5")
    print("   U(1) electromagnetism     P   P   F   F   F")
    print("   SU(3) colour              P   ~*  P   F   F      (*approx.: Casimir scaling, LIT lattice)")
    print("   spin connection (LC)      P   F   F   P** P(tiny)  (**Euclidean holonomy gives A/4lP^2")
    print("                                                     exactly, but LINEAR in Phi: see P4)")
    print("   Ashtekar-Barbero SU(2)    P   F   F   P(fit) F")
    print("   new field                 must be confining at 1 fm AND couple to neutral atoms:")
    print("                             specifying it is new structure - not done here.")
    print("   VERDICT: no known connection meets R1-R5. The QCD end needs a massive (gapped)")
    print("   colour field; the horizon end needs gravity. One A_mu with one sigma(mu) = P3.")
    return g_me


# ===========================================================================
# P3  sigma(mu)
# ===========================================================================
def alpha_s_run(mu_to, mu0=91.1876, a0=0.1180, thresholds=(1.27, 4.18, 172.69)):
    """2-loop MSbar running with continuous matching at the quark masses."""
    def nf(mu):
        return 3 + sum(mu > m for m in thresholds)

    def rhs(lnmu2, a):
        n = nf(np.exp(lnmu2 / 2))
        b0, b1 = 11 - 2 * n / 3, 102 - 38 * n / 3
        return -(b0 / (4 * np.pi)) * a**2 - (b1 / (16 * np.pi**2)) * a**3
    sol = solve_ivp(rhs, [2 * np.log(mu0), 2 * np.log(mu_to)], [a0], rtol=1e-10, atol=1e-14,
                    max_step=0.5)
    return sol.y[0, -1]


def P3():
    banner("P3  sigma(mu): what the 38 orders are, and one honest candidate flow")
    sQ = 0.44**2 / hbarc_GeVm**2
    sP = 1 / (4 * lP**2)
    print(f"sigma_Planck/sigma_QCD = {sP/sQ:.4e};  (E_P/(2 x 0.44 GeV))^2 = {(EP_GeV/0.88)**2:.4e}  CHECK")
    print("Dimensionless tension sigma/mu^2 at each end's own scale:")
    print(f"   QCD:    sigma/(0.44 GeV)^2 = 1        (circular: mu was chosen as sqrt(sigma))")
    print(f"   Planck: sigma/E_P^2        = {sP*lP**2:.4f}")
    print("   -> the 1.9e38 is (E_P/sqrt(sigma_QCD))^2: dimensional analysis, not a flow.")
    print("   Any sigma = c mu^2 spans it; beta(sigma) = 2 sigma is engineering dimension (FOLLOWS).")

    print("\nThe hierarchy itself is KNOWN physics (dimensional transmutation). 2-loop SM running:")
    for mu in [1.777, 10, 91.1876, 1e3, 1e10, EP_GeV]:
        print(f"   alpha_s({mu:10.4g} GeV) = {alpha_s_run(mu):.5f}")
    aP = alpha_s_run(EP_GeV)

    print("\nCandidate flow (KNOWN definition): the Creutz ratio chi(mu) = static force at r = 1/mu")
    print("   chi(mu) = C_F alpha_s(mu) mu^2 + sigma_QCD     (leading order, C_F = 4/3)")
    print("   Gravity analogue between energy-mu quanta at r = 1/mu:  mu^4 / E_P^2")
    CF = 4 / 3
    chiP = CF * aP + 1.0                              # in units of E_P^2
    print(f"   at mu = E_P:  QCD part C_F alpha_s = {CF*aP:.4f} E_P^2;  gravity part = 1 E_P^2")
    print(f"   required sigma_Planck = 0.25 E_P^2.  QCD alone short by x{0.25/(CF*aP):.1f};"
          f" QCD+gravity over by x{chiP/0.25:.2f}")
    print(f"   QCD alone would need alpha_s(E_P) = 3/16 = 0.1875 (SM gives {aP:.4f})")
    print("   VERDICT: no known running quantity lands on 1/(4 lP^2). sigma(mu) not derived;")
    print("   the area tension that falls out of known forces is O(1) x mu^2 at every scale.")
    return aP


# ===========================================================================
# P4  Are the two areas the same kind?
# ===========================================================================
def P4():
    banner("P4  QCD Wilson-loop area vs horizon area (Euclidean gravity)")
    print("QCD: -ln<W> = sigma x (area of the surface the loop BOUNDS), quadratic in Phi.")
    print("Gravity: Euclidean Schwarzschild; the loop is the thermal circle at the horizon.")
    print("   holonomy of the spin connection around it = kappa * beta (must be 2 pi: no cone)")
    for M in [1e-3, 1.0, 4e6, 1e11]:
        m = M * Msun
        kappa = c**4 / (4 * G * m)                        # surface gravity (m s^-2)
        TH = hbar * c**3 / (8 * np.pi * G * m * kB)
        beta_len = hbar * c / (kB * TH)                   # thermal circle length, m
        print(f"   M = {M:7.1e} Msun   holonomy kappa beta_len / c^2 = {kappa*beta_len/c**2/np.pi:.10f} pi")
    print("Replica/conical method (KNOWN: Susskind-Uglum, BTZ 1994): holonomy 2 pi n gives")
    print("   ln Z_n  contains  (1 - n) * 2 pi * A / (8 pi G hbar)  ->  S = -d/dn[ln Z_n - n ln Z_1]|_{n=1}")
    A = 16 * np.pi * (G * Msun / c**2) ** 2
    lnZ = lambda n: (1 - n) * 2 * np.pi * A / (8 * np.pi * lP**2)
    d = 1e-6
    S = -((lnZ(1 + d) - (1 + d) * lnZ(1)) - (lnZ(1 - d) - (1 - d) * lnZ(1))) / (2 * d)
    print(f"   numerical: S / (A/4lP^2) = {S/(A/(4*lP**2)):.10f}   CHECK")
    print("Two structural differences (FOLLOWS):")
    print("   (1) Gravity: ln Z is LINEAR in the holonomy, coefficient A/8 pi G (Aharonov-Bohm-like).")
    print("       QCD:     ln W is QUADRATIC in the phase fluctuation, coefficient sigma.")
    print("   (2) Horizon area is TRANSVERSE to the loop's plane: the loop LINKS the horizon")
    print("       (a codimension-2 surface), like an AB loop around a flux tube.")
    print("       The QCD area is the area the loop SPANS.")
    print("   VERDICT: in 4D GR + QCD they are different kinds of area (spanned vs linked).")
    print("   Known exception: AdS/CFT, where Wilson loops (string worldsheet, tension 1/2 pi alpha')")
    print("   and entropies (Ryu-Takayanagi surface, tension 1/4G) are both bulk minimal surfaces;")
    print("   in a 4D bulk both are 2-surfaces. Requires Lambda < 0; our universe has Lambda > 0.")


# ===========================================================================
# P5  Quark quantum numbers from folds (Skyrme)
# ===========================================================================
def skyrme_profile(R=20.0, r0=1e-4):
    """B=1 hedgehog by boundary-value solve of the field equation, with the exact
    massless tail F = k/r^2 imposed at R (R F' + 2F = 0) and integrated analytically
    beyond R. (A hard cutoff F(R) = 0 underestimates the moment of inertia by ~3%.)"""
    from scipy.integrate import solve_bvp

    def f(r, y):
        F, P = y
        s2, s2F = np.sin(F) ** 2, np.sin(2 * F)
        return np.vstack([P, (2 * s2F * (1 - P * P) + 2 * s2 * s2F / r**2 - 4 * r * P)
                          / (2 * r * r + 4 * s2)])
    bc = lambda ya, yb: np.array([ya[0] - np.pi, R * yb[1] + 2 * yb[0]])
    r = np.geomspace(r0, R, 2000)
    sol = solve_bvp(f, bc, r, np.vstack([np.pi * np.exp(-r), -np.pi * np.exp(-r)]),
                    tol=1e-9, max_nodes=10**6)
    rr = np.geomspace(r0, R, 400001)
    F, P = sol.sol(rr)
    s2 = np.sin(F) ** 2
    E = 4 * np.pi * np.trapezoid(rr * rr * P * P + 2 * s2 * (P * P + 1) + s2 * s2 / rr**2, rr)
    Lt = 8 * np.trapezoid(rr * rr * s2 * (1 + P * P + s2 / rr**2), rr)
    k = F[-1] * R**2
    return E + 8 * np.pi * k * k / R**3, Lt + 8 * k * k / R


def P5():
    banner("P5  Quantum numbers of folds (Skyrme model, rigid-rotor quantisation)")
    E, Lt = skyrme_profile()
    a = E / 4                       # M = a F_pi / e
    b = 2 * np.pi / 3 * Lt          # Lambda = b / (e^3 F_pi)
    print(f"E/(12 pi^2) = {E/(12*np.pi**2):.6f} (LIT 1.2314);  M = {a:.3f} F_pi/e (LIT ANW 36.5)")
    print(f"Lambda = (2 pi/3) Lt/(e^3 F_pi), Lt = {Lt:.3f} (LIT ANW 50.9)")
    MN, MD = 938.9, 1232.0
    invL = (MD - MN) * 8 / 12       # 1/Lambda in MeV
    M0 = MN - 3 / 8 * invL
    e = (b * invL * a / M0) ** 0.25
    Fpi = M0 * e / a
    print(f"Fit to N(939), Delta(1232): M0 = {M0:.1f} MeV, e = {e:.3f}, F_pi = {Fpi:.1f} MeV"
          f"  (LIT ANW: 5.45, 129; measured F_pi = 186 MeV in this convention)")
    print("Quantised B=1 states: J = I = 1/2, 3/2, ...  Charge Q = I3 + B/2 (KNOWN, ANW 1983):")
    for I in [0.5, 1.5]:
        print(f"   I = J = {I}:  Q = " + ", ".join(f"{I3 + 0.5:+.0f}" for I3 in np.arange(I, -I - 1, -1)))
    print("Spin-1/2 needs the WZW term: J = N_c B / 2 mod 1 (KNOWN, Witten 1983).")
    print("   -> fermionic folds REQUIRE N_c = 3 colours as input: circular for deriving quarks.")
    print("\nCan a fold carry B = 1/3?  Hedgehog with f(0) = theta: B = (2 theta - sin 2 theta)/(2 pi)")
    th = brentq(lambda t: (2 * t - np.sin(2 * t)) / (2 * np.pi) - 1 / 3, 0.1, 3.1)
    from fractions import Fraction as Fr
    qs = [Fr(1, 2) + Fr(1, 6), Fr(-1, 2) + Fr(1, 6)]
    print(f"   B = 1/3 at theta = {th:.6f} rad. Then Q = I3 + B/2 = {qs[0]}, {qs[1]} for I = 1/2"
          " (the u, d charges - but only because B = 1/3 was put in)")
    print("   but the field is singular at r = 0; Skyrme-term energy with core cutoff eps:")
    for eps in [1e-1, 1e-2, 1e-3, 1e-4]:
        f = lambda r: th * np.exp(-r)
        Ec = 4 * np.pi * quad(lambda r: np.sin(f(r)) ** 4 / r**2, eps, 30, limit=400, points=[eps * 10])[0]
        print(f"   eps = {eps:7.0e}:  E_core = {Ec:12.2f}   eps*E_core = {eps*Ec:.4f}"
              f"  (-> 4 pi sin^4 theta = {4*np.pi*np.sin(th)**4:.4f})")
    eps_P = lP / (2 * hbarc_GeVm / (e * Fpi * 1e-3))          # lP in Skyrme length units 2/(e F_pi)
    E_GeV = (Fpi * 1e-3 / (4 * e)) * 4 * np.pi * np.sin(th) ** 4 / eps_P
    print(f"   Planck cutoff (eps = lP): E_core = {E_GeV:.2e} GeV = {E_GeV/EP_GeV:.3f} E_P"
          "   vs quark masses ~ 0.002-173 GeV")
    print("   VERDICT: folds give baryons (B, J, I, Q all integer-B; N and Delta reproduced),")
    print("   not quarks. Fractional folds have Planck-scale core energy, and colour, flavour")
    print("   and 3 generations do not appear at all.")


# ===========================================================================
# P6  Bounce density and barrier in terms of Phi_R
# ===========================================================================
def P6(gamma):
    banner("P6  Bounce density rho_c and barrier R(rho) in terms of Phi_R")
    print("Flat FRW, H^2 = 8 pi G rho/(3 c^2); Hubble sphere A = 4 pi (c/H)^2; line 4: Phi_max^2 = A/(2 lP^2)")
    for rho in [1e-9 * rhoP, 1e-60 * rhoP, 1e-120 * rhoP]:
        H = np.sqrt(8 * np.pi * G * rho / (3 * c**2))
        Phi2 = 4 * np.pi * (c / H) ** 2 / (2 * lP**2)
        print(f"   rho/rho_P = {rho/rhoP:7.0e}:  Phi_max^2 = {Phi2:.6e},  3 rho_P/(4 rho) = {0.75*rhoP/rho:.6e}")
    print("   -> Phi_max^2(rho) = 3 rho_P / (4 rho)          (FOLLOWS, exact)")
    rc = np.sqrt(3) / (32 * np.pi**2 * gamma**3)
    print(f"LQC bounce (KNOWN within LQC): rho_c = sqrt(3)/(32 pi^2 gamma^3) rho_P = {rc:.4f} rho_P (gamma = {gamma:.6f})")
    print(f"   in STUR variables: rho_c = 3 rho_P/(4 Phi_c^2) with Phi_c^2 = {0.75/rc:.4f}")
    print("   -> the bounce is where the Hubble sphere holds Phi^2 ~ 2. Phi_c is set by gamma, not by STUR.")
    print("Creation from nothing (no parent vacuum = KNOWN, Vilenkin 1982): P ~ exp(-/+ S_dS),")
    print("   S_dS = 3 rho_P/(8 rho)  =>  R(rho) = 1/2 Phi_max^2(rho) = 3 rho_P/(8 rho)   [STUR identification]")
    print(f"   R(rho_c) = {0.375/rc:.4f}  (barrier gone at the bounce; FOLLOWS)")
    H0 = 67.4e3 / 3.0857e22
    OL = 0.685
    rL = 3 * (H0 * np.sqrt(OL)) ** 2 * c**2 / (8 * np.pi * G)
    print(f"   today's vacuum: rho_L/rho_P = {rL/rhoP:.3e},  R = S_dS/k_B = {0.375*rhoP/rL:.3e}")
    print("   dR/drho < 0: the EMPTIER the universe, the HIGHER the Vilenkin barrier.")
    print("   (Hartle-Hawking sign: exp(+S) favours empty dS - creation, not a trigger.)")
    print("   VERDICT: rho_c and R(rho) can be written in Phi_R (above), but only by renaming")
    print("   LQC and Vilenkin. 'Emptiness triggers tunnelling' is opposite to Vilenkin and")
    print("   is not a trigger in Hartle-Hawking. rho_c (dense) and the trigger (empty)")
    print(f"   are {rc*rhoP/rL:.1e} apart in density: they cannot be the same event.")
    return rL


# ===========================================================================
# P7  Information paradox
# ===========================================================================
def P7(rL, make_plots=True):
    banner("P7  Information paradox: Page curve vs the STUR entropy")
    r = 1.4847                       # LIT: Page 2013, dS_rad/(-dS_BH) for 4D Schwarzschild emission
    mP = np.sqrt(r / (1 + r))
    tP = 1 - mP**3
    print(f"Coarse radiation entropy per unit BH entropy lost: {r} (LIT, Page 2013)")
    print(f"Page point: M/M0 = sqrt(r/(1+r)) = {mP:.4f};  t_Page/t_evap = {tP:.4f}  (LIT 0.5381)  CHECK")
    print("Unitarity (KNOWN): S_fine(rad) = min(r (S0 - S_BH), S_BH)   [Page curve; islands 2019]")
    print("STUR: S_R = 1/2 Phi_R^2 = -ln V.  From POSTULATE_TEST: for Gaussian baths -ln V is")
    print("   monotone and unbounded -> it behaves like the COARSE curve r (S0 - S_BH).")
    print("   Line 4 caps it at A(t)/4lP^2 = S_BH(t).  Violation after the Page time:")
    for f in [0.6, 0.8, 0.95, 0.999]:
        m = (1 - f) ** (1 / 3)
        coarse, cap = r * (1 - m**2), m**2
        print(f"   t/t_evap = {f:5.3f}:  coarse S_R/S0 = {coarse:.4f}   bound S_BH/S0 = {cap:.4f}"
              f"   {'VIOLATED' if coarse > cap else 'ok'}")
    print("   -> postulate (line 2) + bound (line 4) contradict each other after t_Page,")
    print("      unless Phi_R^2 is a fine-grained entropy - which ASSUMPTIONS.md shows it is not.")
    S_dS = 0.375 * rhoP / rL
    print(f"\nBackground picture: 'universe ends with almost no information'. Final dS horizon")
    print(f"   entropy = {S_dS:.2e} k_B (computed above). Coarse entropy only grows (2nd law);")
    print("   fine-grained entropy of a closed unitary universe is constant (KNOWN).")
    print("   -> 'almost no information' is false (coarse) or always true (fine): never a trigger.")
    print("   VERDICT: STUR as written reproduces Hawking's paradox, not its resolution.")
    if make_plots:
        try:
            import matplotlib
            matplotlib.use("Agg")
            import matplotlib.pyplot as plt
            os.makedirs(OUT, exist_ok=True)
            t = np.linspace(0, 1, 500)
            m = (1 - t) ** (1 / 3)
            fig, ax = plt.subplots(figsize=(6.4, 4.2))
            fig.patch.set_facecolor("#fcfcfb"); ax.set_facecolor("#fcfcfb")
            ax.plot(t, r * (1 - m**2), color="#eb6834", lw=2, label="STUR S_R (behaves as coarse, monotone)")
            ax.plot(t, m**2, color="#52514e", lw=1.2, ls=":", label="Bound S_BH(t) = A(t)/4ℓ_P²")
            ax.plot(t, np.minimum(r * (1 - m**2), m**2), color="#2a78d6", lw=2, label="Page curve (unitarity)")
            ax.axvline(tP, color="#52514e", lw=0.8)
            ax.annotate(f"t_Page = {tP:.3f}", (tP + 0.01, 1.35), color="#52514e")
            ax.set_xlabel("t / t_evap"); ax.set_ylabel("Entropy / S_BH(0)")
            ax.set_title("Evaporating black hole: radiation entropy", loc="left", fontsize=10)
            ax.grid(color="#e4e3df", lw=0.6)
            for sp in ["top", "right"]:
                ax.spines[sp].set_visible(False)
            ax.legend(frameon=False, fontsize=9)
            fig.tight_layout()
            fig.savefig(os.path.join(OUT, "page_curve.png"), dpi=150)
            plt.close(fig)
            print("\nPlot written to results/open_problems/")
        except ImportError:
            print("\n(matplotlib not installed - plot skipped)")


def main(make_plots=True):
    gamma = P2()
    P3()
    P4()
    P5()
    rL = P6(gamma)
    P7(rL, make_plots)


if __name__ == "__main__":
    main()
