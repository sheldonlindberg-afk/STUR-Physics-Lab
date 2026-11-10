#!/usr/bin/env python3
"""
Gravity in TEGR (the Teleparallel Equivalent of General Relativity), applied to the
double slit / gravity-entanglement chain of MEASUREMENT.md and GRAVITY_ENTANGLEMENT.md.

TEGR (KNOWN; Einstein 1928, Moller 1961, Hayashi-Shirafuji 1979, Aldrovandi-Pereira 2013):
  gravity is a gauge field of the TRANSLATION group. The field is the tetrad e^a_mu, its
  potential B^a_mu = e^a_mu - delta^a_mu, its field strength is TORSION
      T^a_{mu nu} = d_mu e^a_nu - d_nu e^a_mu + w^a_{b mu} e^b_nu - w^a_{b nu} e^b_mu,
  with a flat (pure-gauge) spin connection w. Curvature is zero; there is no curved
  spacetime, only a force field, like electromagnetism.
  Lagrangian  L = (e / 16 pi G) T_scalar  (sign fixed below by Newton's law), with
      T_scalar = 1/4 T^{rmn} T_{rmn} + 1/2 T^{rmn} T_{nmr} - T^r_{rm} T^{n m}_n.

  E1  The identity T = -R + B (B a total divergence): same field equations as GR. CHECK.
  E2  Newton's law from the TEGR Lagrangian, coefficient included. CHECK.
  E3  Black-hole entropy from the TEGR action: boundary flux at infinity gives A/4. CHECK.
  E4  The gravitational phase is a TEGR holonomy. The two-mass phase phi = G m^2 tau/(hbar r)
      comes out of field + matter bookkeeping: the FIELD's own action is branch-dependent.
  E5  STUR open problem P2 (which connection is A_mu?): the translational potential as a
      candidate, scored on R1-R5.
  E6  Does gravity's own field record which path? Graviton emission during the split
      (the gravitational version of the surface decoherence in T5).
  E7  What TEGR changes for the experiment.
Labels: KNOWN, FOLLOWS, CHECK (computed here), LIT, PROPOSAL.
"""
import numpy as np
import sympy as sp

G_SI, C_SI, HBAR_SI = 6.67430e-11, 2.99792458e8, 1.054571817e-34


def banner(s):
    print("\n" + "=" * 78 + "\n" + s + "\n" + "=" * 78)


# --------------------------------------------------------------------------- core
def torsion_parts(E, X, eta, omega=None, simp=False):
    """Return (T_scalar, B_divergence, metric, inverse metric, e) for tetrad E[a, mu].
    simp=True simplifies each torsion component (fast for small closed-form tetrads)."""
    S = sp.simplify if simp else (lambda q: q)
    n = len(X)
    E = sp.Matrix(E)
    Einv = E.inv()                                  # Einv[mu, a] = e_a^mu
    g = (E.T * eta * E).applyfunc(S)
    ginv = g.inv().applyfunc(S)
    if omega is None:
        omega = [[[0] * n for _ in range(n)] for _ in range(n)]
    Ta = [[[sp.diff(E[a, nu], X[mu]) - sp.diff(E[a, mu], X[nu])
            + sum(omega[a][b][mu] * E[b, nu] - omega[a][b][nu] * E[b, mu] for b in range(n))
            for nu in range(n)] for mu in range(n)] for a in range(n)]
    T = [[[S(sum(Einv[r, a] * Ta[a][mu][nu] for a in range(n))) for nu in range(n)]
          for mu in range(n)] for r in range(n)]
    TL = [[[sum(g[r, s] * T[s][m][v] for s in range(n)) for v in range(n)] for m in range(n)]
          for r in range(n)]
    Tup = [[[sum(ginv[m, a] * ginv[v, b] * T[r][a][b] for a in range(n) for b in range(n))
             for v in range(n)] for m in range(n)] for r in range(n)]
    s1 = sum(Tup[r][m][v] * TL[r][m][v] for r in range(n) for m in range(n) for v in range(n))
    s2 = sum(Tup[r][m][v] * TL[v][m][r] for r in range(n) for m in range(n) for v in range(n))
    Tv = [sum(T[r][r][m] for r in range(n)) for m in range(n)]           # T^r_{r mu}
    Tvu = [sum(ginv[m, k] * Tv[k] for k in range(n)) for m in range(n)]
    s3 = sum(Tv[m] * Tvu[m] for m in range(n))
    Tsc = S(sp.Rational(1, 4) * s1 + sp.Rational(1, 2) * s2 - s3)
    e = S(E.det())                                  # orientation chosen so that det > 0
    B = 2 / e * sum(sp.diff(e * Tvu[m], X[m]) for m in range(n))
    torsion_parts.last_vector = Tvu                 # T^mu (torsion vector, index up)
    return Tsc, B, g, ginv, e


def ricci_scalar(g, ginv, X):
    n = len(X)
    Gam = [[[sum(ginv[a, d] * (sp.diff(g[d, b], X[c]) + sp.diff(g[d, c], X[b]) - sp.diff(g[b, c], X[d]))
                 for d in range(n)) / 2 for c in range(n)] for b in range(n)] for a in range(n)]

    def Ric(b, c):
        return sum(sp.diff(Gam[a][b][c], X[a]) - sp.diff(Gam[a][b][a], X[c])
                   + sum(Gam[a][a][d] * Gam[d][b][c] - Gam[a][c][d] * Gam[d][b][a] for d in range(n))
                   for a in range(n))
    return sum(ginv[b, c] * Ric(b, c) for b in range(n) for c in range(n))


# --------------------------------------------------------------------------- E1
def identity_check(points=3, seed=7):
    """T + R - B at random points for a non-trivial static, non-diagonal-in-space tetrad."""
    t, x, y, z = sp.symbols("t x y z", real=True)
    X = [t, x, y, z]
    eta = sp.diag(-1, 1, 1, 1)
    A = sp.sin(x) * y / 3 + z**2 / 7
    Bf = sp.cos(y) * x / 5 + x * z / 11
    E = sp.Matrix([[sp.exp(A), 0, 0, 0],
                   [0, sp.exp(Bf), z / 13, 0],
                   [0, 0, sp.exp(Bf), 0],
                   [0, 0, 0, sp.exp(-Bf)]])
    T, B, g, ginv, e = torsion_parts(E, X, eta)
    R = ricci_scalar(g, ginv, X)
    rng = np.random.default_rng(seed)
    out = []
    for _ in range(points):
        pt = {t: 0, x: sp.Rational(int(rng.integers(-9, 10)), 7),
              y: sp.Rational(int(rng.integers(-9, 10)), 5), z: sp.Rational(int(rng.integers(-9, 10)), 3)}
        out.append((float(sp.N((T + R - B).subs(pt), 30)), float(sp.N(T.subs(pt), 15)),
                    float(sp.N(R.subs(pt), 15))))
    return out


# --------------------------------------------------------------------------- E2
def newtonian_lagrangian():
    """Second-order part of e*T for e^0 = e^{Phi} dt, e^i = e^{-Psi} dx^i (static)."""
    t, x, y, z, eps = sp.symbols("t x y z epsilon", real=True)
    X = [t, x, y, z]
    P = sp.Function("Phi")(x, y, z)
    Q = sp.Function("Psi")(x, y, z)
    E = sp.diag(sp.exp(eps * P), sp.exp(-eps * Q), sp.exp(-eps * Q), sp.exp(-eps * Q))
    T, B, g, ginv, e = torsion_parts(E, X, sp.diag(-1, 1, 1, 1))
    eT = sp.expand(sp.exp(eps * P - 3 * eps * Q) * T)          # e = e^{Phi - 3 Psi}
    L2 = sp.expand(sp.diff(eT, eps, 2).subs(eps, 0) / 2)
    return L2, (x, y, z), P, Q


def grad_form(L2, X, P, Q):
    """Write L2 as a (grad Phi)^2 + b (grad Phi . grad Psi) + c (grad Psi)^2."""
    a = sum(L2.coeff(sp.diff(P, v), 2) for v in X) / 3
    c = sum(L2.coeff(sp.diff(Q, v), 2) for v in X) / 3
    b = sum(sp.expand(L2).coeff(sp.diff(P, v)).coeff(sp.diff(Q, v)) for v in X) / 3
    return sp.nsimplify(a), sp.nsimplify(b), sp.nsimplify(c)


# --------------------------------------------------------------------------- E3
def schwarzschild_tegr_action():
    """Euclidean Schwarzschild, G = 1. Diagonal spherical tetrad, flat spin connection of
    the same tetrad at M = 0 (the Krssak-Pereira reference prescription). In vacuum R = 0,
    so e T = e B = 2 d_mu(e T^mu): the action is a pure boundary flux,
        I_E = (1/16 pi) int e T = (beta / 16 pi) * 4 pi * [2 e T^r / sin(theta)]_{2M}^{inf}.
    Returns (reference torsion scalar, e T^r / sin theta, I from infinity, I from the tip, M)."""
    tau, r, th, ph, M = sp.symbols("tau r theta phi M", positive=True)
    X = [tau, r, th, ph]
    f = 1 - 2 * M / r
    E = sp.diag(sp.sqrt(f), 1 / sp.sqrt(f), r, r * sp.sin(th))
    Eref = sp.diag(1, 1, r, r * sp.sin(th))
    n = 4
    w = [[[0] * n for _ in range(n)] for _ in range(n)]
    # flat-space spin connection of Eref (frame indices 1=r, 2=theta, 3=phi), antisymmetric
    w[2][1][2], w[1][2][2] = 1, -1
    w[3][1][3], w[1][3][3] = sp.sin(th), -sp.sin(th)
    w[3][2][3], w[2][3][3] = sp.cos(th), -sp.cos(th)
    eta = sp.eye(4)
    Tref, *_ = torsion_parts(Eref, X, eta, w, simp=True)
    T, B, g, ginv, e = torsion_parts(E, X, eta, w, simp=True)
    flux = sp.simplify(e * torsion_parts.last_vector[1] / sp.sin(th))
    beta = 8 * sp.pi * M
    pref = beta * 4 * sp.pi * 2 / (16 * sp.pi)
    I_inf = sp.simplify(pref * sp.limit(flux, r, sp.oo))
    I_tip = sp.simplify(-pref * sp.limit(flux, r, 2 * M, "+"))
    return sp.simplify(Tref), flux, I_inf, I_tip, M


# --------------------------------------------------------------------------- E4
def two_mass_bookkeeping(m1, m2, r):
    """Newtonian limit of TEGR (E2): L = -(1/8 pi G)(grad Phi)^2 - rho Phi.
    Cross terms for two point masses: field part and matter part (exact integrals)."""
    field = -G_SI * m1 * m2 / r                  # -(1/4piG) int grad Phi1 . grad Phi2 = -G m1 m2 / r
    matter = 2 * G_SI * m1 * m2 / r              # -m1 Phi2(x1) - m2 Phi1(x2)
    return field, matter, field + matter         # total L = -U = +G m1 m2 / r


# --------------------------------------------------------------------------- E6
def graviton_count(m, dx, t_ramp, t_hold):
    """Quadrupole emission (KNOWN, P = G/(5c^5) <dddot Q_ij dddot Q_ij>) of ONE branch of a
    diamond moving dx/2 along z with a smooth minimum-jerk ramp, open-hold-close.
    Third derivative taken analytically. Returns energy (J) and graviton number at w = 2 pi / t_r."""
    u = sp.symbols("u", real=True)
    s = 10 * u**3 - 15 * u**4 + 6 * u**5
    zz = (sp.Rational(1, 2) * dx * s) ** 2          # z^2 as a function of u = t / t_r
    d3 = sp.diff(zz, u, 3) / t_ramp**3              # d^3(z^2)/dt^3
    one_ramp = float(sp.integrate(d3**2, (u, 0, 1))) * t_ramp
    E = G_SI / (5 * C_SI**5) * (2 / 3) * m**2 * (2 * one_ramp)   # open + close, hold radiates 0
    w = 2 * np.pi / t_ramp
    return E, E / (HBAR_SI * w)


def main():
    banner("E1  Identity: T_scalar = -R + B, B a total divergence (CHECK)")
    for d, T, R in identity_check():
        print(f"   T = {T:+.6e}   R = {R:+.6e}   T + R - B = {d:+.1e}")
    print("   FOLLOWS: e T and -e R differ by a divergence, so TEGR and GR have identical")
    print("   field equations. Every prediction of GRAVITY_ENTANGLEMENT.md is unchanged.")

    banner("E2  Newton's law from the TEGR Lagrangian (CHECK, coefficients exact)")
    L2, Xs, P, Q = newtonian_lagrangian()
    a, b, c = grad_form(L2, Xs, P, Q)
    print(f"   e^0 = e^Phi dt, e^i = e^-Psi dx^i:  (e T)_2 = {a} (grad Phi)^2 {int(b):+d} grad Phi.grad Psi"
          f" {int(c):+d} (grad Psi)^2  (+ divergence)")
    print("   Lagrangian L = -(e T)/(16 pi G) - rho Phi (sign fixed by attraction). Varying:")
    print("     d/dPsi : laplacian(Psi) = laplacian(Phi)         ->  Psi = Phi")
    print("     d/dPhi : laplacian(Psi) = 4 pi G rho             ->  Newton, coefficient 1")
    print("   (check: with Psi = Phi, (e T)_2 = 2 (grad Phi)^2, so L = -(1/8 pi G)(grad Phi)^2 - rho Phi.)")

    banner("E3  Black-hole entropy from the TEGR action (CHECK)")
    Tref, flux, I_inf, I_tip, M = schwarzschild_tegr_action()
    print(f"   Reference tetrad torsion scalar with this spin connection: {Tref}  (must be 0)")
    print(f"   R = 0, so the action is a boundary flux. e T^r / sin(theta) = {flux}")
    print(f"   Flux at infinity:          I_inf = {I_inf}   (GR with Gibbons-Hawking + subtraction: beta M / 2 = 4 pi M^2)")
    print(f"   Flux at the horizon tip:   I_tip = {I_tip}")
    S = sp.simplify(8 * sp.pi * M**2 - I_inf)
    print(f"   With the horizon regular (as GR assumes): S = beta M - I_inf = {S} = A/4"
          f" (A = 16 pi M^2): {sp.simplify(S - 4*sp.pi*M**2) == 0}")
    print("   FOLLOWS: the flux at infinity alone gives GR's answer, with no boundary term or")
    print("   background subtraction added by hand. The diagonal frame does not rotate around")
    print("   the Euclidean horizon, which is singular there and adds an equal flux at the tip.")
    print("   No single flat frame is regular at both ends: a frame regular at the tip needs a")
    print("   rotation k dtau, and then the flux at infinity diverges (CHECK in the tests).")
    print("   So TEGR gives A/4 with the same input as GR (a smooth horizon), not with less.")

    banner("E4  The gravitational phase as a TEGR holonomy; the FIELD's own share")
    print("   A mass on a worldline picks up phase -(m c / hbar) int e^0_mu dx^mu: the")
    print("   holonomy of the translational potential B^0_0 = Phi / c^2 (KNOWN; COW 1975,")
    print("   gravitational Aharonov-Bohm: Overstreet et al., Science 375, 226 (2022)).")
    m, r = 1.5e-14, 181.2e-6
    fld, mat, tot = two_mass_bookkeeping(m, m, r)
    print(f"   Two diamonds (1.5e-14 kg, 181 um): matter part {mat:+.3e} J, field part"
          f" {fld:+.3e} J, total L = {tot:+.3e} J = G m^2 / r")
    print("   FOLLOWS: the matter coupling alone would give 2 G m^2 / r; the gravitational FIELD's")
    print("   own action gives -G m^2 / r, and the net is the familiar G m^2 / r. The field term")
    print("   is not optional: without it the phase is doubled. For it to depend on the branch")
    print("   pair, the field configuration itself must be in two places.")
    print("   So in TEGR language: lambda = 1 means the torsion field is in two places, exactly")
    print("   as the electron's EM field is (T5). lambda = 0 means one torsion field.")

    banner("E5  STUR open problem P2: is TEGR's translational potential the connection A_mu?")
    print("   Candidate: A_mu = (m c / hbar) B^0_mu  (Phi_R = its holonomy around the two paths)")
    print("   R1 holonomy of a gauge connection        YES  (translation gauge group, abelian at linear order)")
    print("   R2 Gaussian noise                        YES  for the free linear field; noise ~ (l_P/L)^2 (P2: 2.6e-70)")
    print("   R3 area law at the QCD scale             NO   massless -> perimeter law, same as EM (P2)")
    print("   R4 horizon entropy A / 4 l_P^2           YES  E3, as in GR (smooth horizon assumed)")
    print("   R5 couples to a neutral atom             YES  every mass; COW phase 1.58e8 rad in MAGIS (P2)")
    print("   FOLLOWS: 4 of 5. It is the first candidate in P2 meeting R1, R4 and R5 at full")
    print("   strength (the Levi-Civita spin connection couples to atoms only as a 1e-14 boost).")
    print("   It fails R3 for the same reason EM does. With Gaussian noise in this A_mu, the")
    print("   visibility formula V = exp(-1/2 <Phi_R^2>) is exactly Option A's model, whose")
    print("   area-law version is excluded (OPTION_A.md); its standard (graviton) version is")
    print("   too small to see. So TEGR names STUR's connection, and leaves the QCD end open.")

    banner("E6  Does gravity's own field record which path? (gravitational version of T5)")
    for m_, dx, tr, th in [(1.5e-14, 721e-6, 1.58, 0.08), (1e-14, 250e-6, 0.73, 2.5)]:
        E, N = graviton_count(m_, dx, tr, th)
        print(f"   m = {m_:.1e} kg, dx = {dx*1e6:.0f} um, ramps {tr} s: radiated {E:.1e} J,"
              f" gravitons emitted {N:.1e}")
    print("   FOLLOWS: no graviton carries which-path information away, so the field does not")
    print("   decohere the diamond (KNOWN in outline: Belenchia et al., PRD 98, 126009 (2018)).")
    print("   The which-path record is the static (Coulomb-like) torsion field, bound to the")
    print("   source, and it is undone when the paths recombine. For EM the decoherence in T5")
    print("   needed a nearby SURFACE; gravity has no conductors (no negative mass), so it has")
    print("   no analogue of that surface and cannot be screened.")

    banner("E7  What TEGR changes for the experiment")
    print("   Predictions: nothing. T = -R + B (E1), so lambda = 1 vs lambda = 0, the phases,")
    print("   the noise budget and the design (GRAVITY_ENTANGLEMENT.md) are all unchanged.")
    print("   What it changes is the reading:")
    print("    - gravity is a gauge FORCE field (torsion) on flat spacetime, the same structure")
    print("      as electromagnetism. The split-vs-amplitude question becomes the SAME question")
    print("      for both fields. EM answers lambda = 1 (T5); TEGR's linear theory is an abelian")
    print("      gauge theory like EM, which makes lambda = 1 the structural expectation.")
    print("      (Expectation, not proof: the experiment still decides.)")
    print("    - the field's own action is part of the entangling phase (E4).")
    print("    - STUR's A_mu gets a name (E5): 4 of 5 requirements met.")
    print("   Not used: f(T) and other modified teleparallel theories, which DO change")
    print("   predictions but add new structure.")


if __name__ == "__main__":
    main()
