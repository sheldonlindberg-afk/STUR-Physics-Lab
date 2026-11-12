#!/usr/bin/env python3
"""
Where the entropy sits in TEGR: Noether charges, the corner term and the frame.

TEGR's Lagrangian is GR's plus a total derivative, L_TEGR = L_GR + d(alpha), with
alpha^mu = (1/8 pi) e T^mu (G = 1; see stur_tegr E1 and E3b). Two Lagrangians that differ
by d(alpha) have the same bulk symplectic structure but Noether charges that differ by a
corner term, Q_TEGR = Q_GR + iota_xi alpha (Iyer-Wald 1994; for formulations of gravity in
general, Freidel-Geiller-Pranzetti arXiv:2006.12527). This module computes both sides for
static spherical metrics ds^2 = -f dt^2 + dr^2/f + r^2 dOmega^2 (any f), and asks how the
answer depends on the flat spin connection, which in TEGR encodes the choice of frame.

Every flat connection here is built as omega = Lambda^-1 d Lambda (pure gauge) and its
curvature is checked to vanish.

  K1  The TEGR Noether charge for xi = d_t, computed directly from L_TEGR = -e T / 16 pi
      (no superpotential convention assumed): Q_TEGR(r) = r (sqrt f - f) = N E_BY, the lapse
      times the Brown-York quasilocal energy E_BY = r (1 - sqrt f); the TEGR momentum
      Pi_0^{tr} integrates to E_BY itself. -> M (ADM) at infinity, -> 0 at the horizon.
      KNOWN: Maluf's TEGR gravitational energy is E_BY; the Noether charge gives the ADM
      mass (Hammad et al., arXiv:1912.08811). (CHECK)
  K2  GR's Iyer-Wald charge: Q_GR(r) = r^2 f'/4; at the bifurcation surface kappa A/(8 pi),
      i.e. the Wald entropy (2 pi / kappa) Q = A/4. KNOWN. (CHECK)
  K3  Q_GR - Q_TEGR is exactly the corner term from alpha (the torsion flux of E3b). At the
      bifurcation surface it is all of kappa A / 8 pi: with the static frame, the whole
      Wald entropy sits in the corner term, none in TEGR's Noether charge. (CHECK)
  K4  The frame boosted along the Killing flow (regular at the bifurcation surface):
      flat; the diffeomorphism charge is unchanged; the compensating local boost adds a
      volume term kappa r (1/sqrt f - 1) per unit radius, which vanishes as the region
      shrinks to the horizon and diverges linearly at infinity. (CHECK)
  K5  Euclidean: the frame winding at rate k around the time circle. Flat. The tip term of
      the action is (A/4)(1 + k/kappa): A/4 for the non-rotating frame (E3b) and 0 for
      the frame regular at the tip (k = -kappa); then the flux at infinity diverges
      (it is finite, M, only for k = 0).
      The connection in the earlier E3 test (k d tau added to the static reference) is NOT
      flat; this replaces it. (CHECK)
Labels: KNOWN, CHECK (computed here).
"""
import sympy as sp

import stur_tegr

t, r, th, ph = sp.symbols("t r theta phi", real=True)
X = [t, r, th, ph]
N4 = 4


def banner(s):
    print("\n" + "=" * 78 + "\n" + s + "\n" + "=" * 78)


# --------------------------------------------------------------------------- tools
def spherical_rotation():
    """Lambda_A: spherical legs (r, theta, phi) -> Cartesian legs. Its pure-gauge connection
    is the reference connection of stur_tegr E3."""
    rh = [sp.sin(th) * sp.cos(ph), sp.sin(th) * sp.sin(ph), sp.cos(th)]
    thh = [sp.cos(th) * sp.cos(ph), sp.cos(th) * sp.sin(ph), -sp.sin(th)]
    phh = [-sp.sin(ph), sp.cos(ph), 0]
    L = sp.eye(4)
    for i in range(3):
        L[i + 1, 1], L[i + 1, 2], L[i + 1, 3] = rh[i], thh[i], phh[i]
    return L


def boost(rate, euclidean=False):
    """Boost (Lorentzian) or rotation (Euclidean) of legs 0, 1 by angle rate * t."""
    B = sp.eye(4)
    if euclidean:
        B[0, 0] = B[1, 1] = sp.cos(rate * t)
        B[0, 1], B[1, 0] = -sp.sin(rate * t), sp.sin(rate * t)
    else:
        B[0, 0] = B[1, 1] = sp.cosh(rate * t)
        B[0, 1] = B[1, 0] = sp.sinh(rate * t)
    return B


def pure_gauge(L):
    """omega^a_{b mu} = (Lambda^-1 d_mu Lambda)^a_b, indexed omega[a][b][mu] as in stur_tegr."""
    Li = sp.simplify(L.inv())
    d = [sp.simplify(Li * sp.diff(L, X[m])) for m in range(N4)]
    return [[[d[m][a, b] for m in range(N4)] for b in range(N4)] for a in range(N4)]


def curvature(w):
    """Nonzero components R^a_{b mu nu} of omega."""
    out = {}
    for a in range(N4):
        for b in range(N4):
            for m in range(N4):
                for v in range(m + 1, N4):
                    R = (sp.diff(w[a][b][v], X[m]) - sp.diff(w[a][b][m], X[v])
                         + sum(w[a][c][m] * w[c][b][v] - w[a][c][v] * w[c][b][m] for c in range(N4)))
                    R = sp.simplify(R)
                    if R != 0:
                        out[(a, b, m, v)] = R
    return out


def at_t0(w):
    return [[[sp.simplify(w[a][b][m].subs(t, 0)) for m in range(N4)] for b in range(N4)] for a in range(N4)]


def momentum(E, eta, w, pairs=((0, 1),)):
    """Pi_a^{mu nu} = dL / d(d_mu e^a_nu) for L = -e T / 16 pi, by differentiating the
    torsion scalar with respect to independent torsion components."""
    n = N4
    S = [[[sp.Symbol(f"S_{a}{m}{v}") for v in range(n)] for m in range(n)] for a in range(n)]
    Einv, g = E.inv(), E.T * eta * E
    gi, e = g.inv(), E.det()
    T = [[[sum(Einv[q, a] * S[a][m][v] for a in range(n)) for v in range(n)] for m in range(n)] for q in range(n)]
    TL = [[[sum(g[q, s] * T[s][m][v] for s in range(n)) for v in range(n)] for m in range(n)] for q in range(n)]
    Tup = [[[sum(gi[m, a] * gi[v, b] * T[q][a][b] for a in range(n) for b in range(n))
             for v in range(n)] for m in range(n)] for q in range(n)]
    s1 = sum(Tup[a][b][c] * TL[a][b][c] for a in range(n) for b in range(n) for c in range(n))
    s2 = sum(Tup[a][b][c] * TL[c][b][a] for a in range(n) for b in range(n) for c in range(n))
    Tv = [sum(T[a][a][m] for a in range(n)) for m in range(n)]
    s3 = sum(Tv[m] * sum(gi[m, k] * Tv[k] for k in range(n)) for m in range(n))
    L = -e * (sp.Rational(1, 4) * s1 + sp.Rational(1, 2) * s2 - s3) / (16 * sp.pi)
    Ta = [[[sp.diff(E[a, v], X[m]) - sp.diff(E[a, m], X[v])
            + sum(w[a][b][m] * E[b, v] - w[a][b][v] * E[b, m] for b in range(n))
            for v in range(n)] for m in range(n)] for a in range(n)]
    sub = {S[a][m][v]: Ta[a][m][v] for a in range(n) for m in range(n) for v in range(n)}
    return {(m, v): [(sp.diff(L, S[a][m][v]) - sp.diff(L, S[a][v][m])).subs(sub) for a in range(n)]
            for (m, v) in pairs}


def sphere(expr):
    return sp.simplify(sp.integrate(sp.integrate(expr, (th, 0, sp.pi)), (ph, 0, 2 * sp.pi)))


def static_tetrad(f):
    return sp.diag(sp.sqrt(f), 1 / sp.sqrt(f), r, r * sp.sin(th))


# --------------------------------------------------------------------------- K1-K3
def charges_static():
    """K1-K3 for general f. Returns a dict of exact expressions in f(r)."""
    f = sp.Function("f")(r)
    E, eta = static_tetrad(f), sp.diag(-1, 1, 1, 1)
    w = pure_gauge(spherical_rotation())
    Pi = momentum(E, eta, w)[(0, 1)]
    Q_tegr = sphere(sum(Pi[a] * E[a, 0] for a in range(N4)))         # xi^a = e^a_t
    Pi0 = sphere(Pi[0])
    # GR Iyer-Wald: Q = (1/16 pi) oint sqrt(-g) (nabla^r xi^t - nabla^t xi^r)
    g = sp.diag(-f, 1 / f, r**2, r**2 * sp.sin(th)**2)
    gi = g.inv()
    xi_low = [g[m, 0] for m in range(N4)]
    Gam = [[[sum(gi[a, d] * (sp.diff(g[d, b], X[c]) + sp.diff(g[d, c], X[b]) - sp.diff(g[b, c], X[d]))
                 for d in range(N4)) / 2 for c in range(N4)] for b in range(N4)] for a in range(N4)]
    cov = [[sp.diff(xi_low[nu], X[mu]) - sum(Gam[l][mu][nu] * xi_low[l] for l in range(N4))
            for nu in range(N4)] for mu in range(N4)]                  # nabla_mu xi_nu
    up = lambda mu, nu: sum(gi[mu, a] * gi[nu, b] * cov[a][b] for a in range(N4) for b in range(N4))
    Q_gr = sphere(sp.sqrt(-g.det()) * (up(1, 0) - up(0, 1)) / (16 * sp.pi))
    flux, fF, rr = stur_tegr.static_flux_general()
    corner = sp.simplify((-flux / 2).subs(rr, r))    # iota_xi alpha on the sphere: -(4 pi / 8 pi) flux
    return {"Q_tegr": Q_tegr, "Pi0": Pi0, "Q_gr": Q_gr, "corner": corner,
            "diff": sp.simplify(Q_gr - Q_tegr - corner), "f": f}


def limits_schwarzschild_rn(res):
    """Evaluate K1-K3 at infinity and at the outer horizon for Reissner-Nordstrom
    (Q = 0 is Schwarzschild)."""
    rp, rm = sp.symbols("r_p r_m", positive=True)
    fRN = (1 - rp / r) * (1 - rm / r)
    M = (rp + rm) / 2
    kappa = (rp - rm) / (2 * rp**2)
    ev = lambda key, where: sp.simplify(sp.limit(res[key].subs(res["f"], fRN).doit(), r, where,
                                                 "+" if where != sp.oo else "-"))
    return {"Q_tegr_inf": ev("Q_tegr", sp.oo), "Q_tegr_hor": ev("Q_tegr", rp),
            "Q_gr_inf": ev("Q_gr", sp.oo), "Q_gr_hor": ev("Q_gr", rp),
            "corner_hor": ev("corner", rp), "M": M, "kappaA8pi": sp.simplify(kappa * 4 * sp.pi * rp**2 / (8 * sp.pi)),
            "wald_gr": sp.simplify(2 * sp.pi / kappa * ev("Q_gr", rp)), "area_quarter": sp.pi * rp**2}


# --------------------------------------------------------------------------- K4
def boosted_frame():
    """Lorentzian frame Lambda_A B(kappa t), regular at the bifurcation surface."""
    kap = sp.Symbol("kappa", positive=True)
    w = pure_gauge(spherical_rotation() * boost(kap))
    flat = curvature(w) == {}
    w0 = at_t0(w)
    f = sp.Function("f")(r)
    E, eta = static_tetrad(f), sp.diag(-1, 1, 1, 1)
    P = momentum(E, eta, w0, pairs=((0, 0), (0, 1), (0, 2), (0, 3)))
    Q = sphere(sum(P[(0, 1)][a] * E[a, 0] for a in range(N4)))
    lam = sp.zeros(4)
    for a in range(N4):
        for b in range(N4):
            lam[a, b] = w0[a][b][0]                                    # iota_xi omega
    lam_sph = lam.subs({th: 0, ph: 0})                                 # its (0,1) boost part
    Jt = sphere(sum(P[(0, v)][a] * lam[a, b] * E[b, v] for a in range(N4) for b in range(N4) for v in range(N4)))
    return {"flat": flat, "Q": Q, "J_volume": Jt, "kappa": kap, "f": f, "lam01": lam_sph[0, 1]}


# --------------------------------------------------------------------------- K5
def euclidean_winding():
    """Euclidean static metric with the frame winding at rate k around the time circle:
    Lambda = Lambda_A R(k tau). k = 0 is the frame of stur_tegr E3. Returns the flux
    e T^r / sin(theta) for general f (it depends on tau when k != 0)."""
    k = sp.Symbol("k", real=True)
    w = pure_gauge(spherical_rotation() * boost(k, euclidean=True))
    flat = curvature(w) == {}
    f = sp.Function("f")(r)
    E = static_tetrad(f)
    stur_tegr.torsion_parts(E, X, sp.eye(4), w, simp=True)
    e = E.det()
    flux = sp.simplify(e * stur_tegr.torsion_parts.last_vector[1] / sp.sin(th))
    # the old E3 test connection: static reference + k d tau, not pure gauge
    w_old = pure_gauge(spherical_rotation())
    w_old[0][1][0], w_old[1][0][0] = k, -k
    old_curv = curvature(w_old)
    return {"flat": flat, "flux": flux, "k": k, "f": f, "old_curvature": old_curv}


def winding_tip_term(res):
    """Schwarzschild, f = 1 - 2M/r: the tip term I_tip = -(beta/2) flux(r+) in units of
    A/4, the winding rate that makes the tip regular, and the flux at infinity for k = 0
    and for that rate (at tau = 0)."""
    M = sp.Symbol("M", positive=True)
    k = res["k"]
    fl = sp.simplify(res["flux"].subs(res["f"], 1 - 2 * M / r).doit())
    beta = 8 * sp.pi * M
    I_tip = sp.simplify(-beta / 2 * sp.limit(fl, r, 2 * M, "+"))
    ratio = sp.simplify(I_tip / (4 * sp.pi * M**2))
    k_reg = sp.solve(sp.Eq(ratio, 0), k)
    inf0 = sp.limit(fl.subs(k, 0), r, sp.oo)
    infk = sp.limit(fl.subs(k, k_reg[0]).subs(t, 0), r, sp.oo)
    return {"ratio": ratio, "regular_k": k_reg, "flux_inf_k0": inf0, "flux_inf_regular": infk, "M": M}


# --------------------------------------------------------------------------- main
def main():
    banner("K1  TEGR Noether charge for xi = d_t, from L_TEGR directly (CHECK)")
    res = charges_static()
    lim = limits_schwarzschild_rn(res)
    print(f"   Static frame, any f:   Q_TEGR(r) = {res['Q_tegr']}")
    print(f"   TEGR momentum:         oint Pi_0^(tr) = {res['Pi0']}   (Brown-York energy r(1 - sqrt f))")
    print("   So Q_TEGR = N E_BY with lapse N = sqrt f. KNOWN: Maluf's TEGR energy is E_BY.")
    print(f"   Reissner-Nordstrom: Q_TEGR(oo) = {lim['Q_tegr_inf']} = M: {sp.simplify(lim['Q_tegr_inf'] - lim['M']) == 0}"
          f"   (ADM mass);   Q_TEGR(r+) = {lim['Q_tegr_hor']}")

    banner("K2  GR's Iyer-Wald charge (CHECK)")
    print(f"   Q_GR(r) = {res['Q_gr']}")
    print(f"   RN: Q_GR(oo) = {lim['Q_gr_inf']}  (Komar's M/2);   Q_GR(r+) = {lim['Q_gr_hor']}"
          f" = kappa A / 8 pi: {sp.simplify(lim['Q_gr_hor'] - lim['kappaA8pi']) == 0}")
    print(f"   Wald entropy (2 pi / kappa) Q_GR(r+) = {lim['wald_gr']} = A/4:"
          f" {sp.simplify(lim['wald_gr'] - lim['area_quarter']) == 0}")

    banner("K3  The difference is the corner term iota_xi alpha (CHECK)")
    print(f"   Corner term from alpha = (1/8 pi) e T^mu (E3b flux): {res['corner']}")
    print(f"   Q_GR - Q_TEGR - corner = {res['diff']}  (two independent routes agree)")
    print(f"   At the bifurcation surface the corner term is {lim['corner_hor']} = kappa A / 8 pi:"
          f" {sp.simplify(lim['corner_hor'] - lim['kappaA8pi']) == 0}")
    print("   FOLLOWS: with the static frame, TEGR's Noether charge vanishes at the bifurcation")
    print("   surface and the whole Wald entropy is in the corner term. The bulk theories are")
    print("   the same; where the entropy is booked is not.")

    banner("K4  The frame regular at the bifurcation surface (Lorentzian boost, CHECK)")
    b = boosted_frame()
    print(f"   omega = (Lambda_A B(kappa t))^-1 d(...): flat = {b['flat']}")
    print(f"   Diffeomorphism charge: {b['Q']}  (unchanged; kappa drops out)")
    print(f"   Compensating boost lambda = iota_xi omega (01 component {b['lam01']}); its current, per")
    print(f"   unit radius: {b['J_volume']}")
    print("   This is integrable at the horizon (it vanishes as the region shrinks to it) and")
    print("   grows linearly at infinity, where the boosted frame keeps boosting.")
    print("   OPEN: whether the first-law variation of this Lorentz sector carries kappa dS")
    print("   at the bifurcation surface is not computed here.")

    banner("K5  Euclidean: the frame winding around the time circle (CHECK)")
    e5 = euclidean_winding()
    tip = winding_tip_term(e5)
    print(f"   omega = (Lambda_A R(k tau))^-1 d(...); k = 0 is the E3 frame. Flat = {e5['flat']}")
    print(f"   Schwarzschild tip term / (A/4) = {tip['ratio']}  (kappa = 1/4M: = 1 + k/kappa)")
    print(f"   Flux at infinity: k = 0 -> {tip['flux_inf_k0']} (E3: I = beta M / 2);"
          f"  tip-regular k = {tip['regular_k'][0]} = -kappa -> {tip['flux_inf_regular']}")
    print(f"   The earlier E3 test connection (static reference + k d tau) has curvature"
          f" {len(e5['old_curvature'])} components != 0, e.g. R^0_2(tau,theta) ="
          f" {e5['old_curvature'].get((0, 2, 0, 2))}: not flat, so not TEGR. Replaced by this check.")
    print("   FOLLOWS: A/4 sits at the tip for the non-rotating frame, and nowhere at the tip")
    print("   for the regular frame, which then pays at infinity. The frame (the flat")
    print("   connection) decides where the entropy is booked: edge-mode-type data.")


if __name__ == "__main__":
    main()
