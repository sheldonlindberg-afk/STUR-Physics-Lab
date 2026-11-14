#!/usr/bin/env python3
"""Verifier's third route for the 2026-11-14 extension (stages weak, running; derived f_pi in chiral/links).

Independent of src/ and of the builds: imports only sympy, mpmath and rebuild/inputs.py (measured numbers).
Usage: python3 rebuild/verify/third_route_weak_running.py   -> prints a table and writes third_route.json
next to this script.
"""
import importlib.util
import json
import os
import sys

import mpmath as mp
import sympy as sp

mp.mp.dps = 40
REPO = sys.argv[1] if len(sys.argv) > 1 else os.path.abspath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
spec = importlib.util.spec_from_file_location("inputs", os.path.join(REPO, "rebuild", "inputs.py"))
I = importlib.util.module_from_spec(spec)
spec.loader.exec_module(I)
R = sp.Rational
OUT = {}


def M(x):
    """A float literal from inputs.py as the exact decimal it was typed as."""
    return mp.mpf(repr(x))


# =====================================================================================================
# 1. pi -> l nu from the V-A Lagrangian: trace with sympy's gamma matrices in the (+,-,-,-) metric
#    (the builds use (-,+,+,+)), phase space done by hand in closed form.
# =====================================================================================================
def weak_width_symbolic():
    from sympy.physics.matrices import mgamma
    from sympy import Matrix, eye, sqrt, simplify, symbols, pi
    GF, V, f, ml, mpi = symbols("G_F V f m_l m_pi", positive=True)
    g = [mgamma(i) for i in range(4)]                     # Dirac rep, {g^m, g^n} = 2 eta^{mn}, eta = (+,-,-,-)
    g5 = sp.I * g[0] * g[1] * g[2] * g[3]
    eta = [1, -1, -1, -1]
    slash = lambda p: sum((eta[i] * p[i] * g[i] for i in range(4)), sp.zeros(4))
    # pion at rest; lepton momentum k along z, antineutrino q opposite
    ks = (mpi**2 - ml**2) / (2 * mpi)
    El = (mpi**2 + ml**2) / (2 * mpi)        # = sqrt(ks^2 + ml^2); energy conservation El + ks = mpi
    assert simplify(El**2 - ks**2 - ml**2) == 0 and simplify(El + ks - mpi) == 0
    k = [El, 0, 0, ks]
    q = [ks, 0, 0, -ks]
    p = [k[i] + q[i] for i in range(4)]
    # M = (G_F/sqrt2) V f * ubar(k) pslash (1 - g5) v(q)   (phase irrelevant); NO Dirac-equation shortcut
    G = slash(p) * (eye(4) - g5)
    Gbar = g[0] * G.H * g[0]
    # sum_s u ubar = kslash + m ; sum_s v vbar = qslash (massless)
    tr = (G * slash(q) * Gbar * (slash(k) + ml * eye(4))).trace()
    tr = simplify(tr)
    msq = simplify((GF**2 / 2) * V**2 * f**2 * tr)
    # two-body phase space: Gamma = |k*| / (8 pi m_pi^2) * sum|M|^2
    width = simplify(msq * ks / (8 * pi * mpi**2))
    textbook = GF**2 * V**2 * f**2 * ml**2 * mpi * (1 - ml**2 / mpi**2) ** 2 / (8 * pi)
    return simplify(width - textbook), simplify(tr), (GF, V, f, ml, mpi), width


resid, trace, syms, width_expr = weak_width_symbolic()
print("== 1. weak ==")
print(" spin trace (sympy, (+,-,-,-), no Dirac-eq shortcut):", sp.factor(trace))
print(" width - G_F^2 V^2 f^2 m_l^2 m_pi (1 - m_l^2/m_pi^2)^2 / (8 pi)  =", resid)
OUT["weak_width_residual_symbolic"] = str(resid)

hbar_GeV_s = M(I.HBAR) / (M(I.E_CH) * mp.mpf(10) ** 9)
hbar_exact = mp.mpf("6.62607015e-34") / (2 * mp.pi) / (mp.mpf("1.602176634e-19") * mp.mpf(10) ** 9)   # SI-2019 exact h, e
gam_tree = M(I.GAMMA_PI_MUNU) * hbar_GeV_s / (1 + M(I.DELTA_PI))
GF, Vud, mmu, mpic = M(I.G_F), M(I.V_UD), M(I.M_MU), M(I.M_PIC)


def fpi_from(gam, V=Vud):
    return mp.sqrt(8 * mp.pi * gam / (GF**2 * V**2 * mmu**2 * mpic * (1 - mmu**2 / mpic**2) ** 2))


fpi = fpi_from(gam_tree)
fpi_no_rc = fpi_from(M(I.GAMMA_PI_MUNU) * hbar_GeV_s)
fpi_hexact = fpi_from(M(I.GAMMA_PI_MUNU) * hbar_exact / (1 + M(I.DELTA_PI)))
fpi_src_hbar = fpi_from(M(I.GAMMA_PI_MUNU) * mp.mpf("6.582119569e-25") / (1 + M(I.DELTA_PI)))
err_delta = fpi * mp.mpf("0.0021") / (2 * (1 + M(I.DELTA_PI)))        # PDG delta_pi error 0.0021
err_vud = fpi * mp.mpf("0.00032") / Vud                                # PDG |V_ud| error
print(" hbar (GeV s) from inputs HBAR/E_CH:", mp.nstr(hbar_GeV_s, 15), "; exact SI h/(2 pi e):", mp.nstr(hbar_exact, 15))
print(" f_pi (GeV), delta_pi = 0.0176 removed :", mp.nstr(fpi, 16))
print(" f_pi with the 10-digit hbar 6.582119569e-25:", mp.nstr(fpi_src_hbar, 16), " rel", mp.nstr(fpi_src_hbar / fpi - 1, 3))
print(" f_pi with exact SI hbar               :", mp.nstr(fpi_hexact, 16), " rel", mp.nstr(fpi_hexact / fpi - 1, 3))
print(" f_pi with NO radiative correction     :", mp.nstr(fpi_no_rc, 10), " (+%s%%)" % mp.nstr(100 * (fpi_no_rc / fpi - 1), 4))
print(" f_pi |V_ud|                           :", mp.nstr(fpi * Vud, 10))
print(" physical error: delta_pi +-0.0021 -> +-%s MeV; V_ud +-0.00032 -> +-%s MeV"
      % (mp.nstr(err_delta * 1e3, 3), mp.nstr(err_vud * 1e3, 3)))
OUT.update(fpi=mp.nstr(fpi, 17), fpi_no_rc=mp.nstr(fpi_no_rc, 12), fpi_err_delta_MeV=mp.nstr(err_delta * 1e3, 4),
           fpi_err_vud_MeV=mp.nstr(err_vud * 1e3, 4))

# =====================================================================================================
# 2. One-loop coefficients from explicit generator matrices (traces), sympy exact
# =====================================================================================================
print("== 2. beta coefficients ==")


def su_n_generators(n):
    """Generalised Gell-Mann matrices / 2: Tr(t_a t_b) = delta_ab / 2."""
    gens = []
    for i in range(n):
        for j in range(i + 1, n):
            s = sp.zeros(n)
            s[i, j] = s[j, i] = R(1, 2)
            gens.append(s)
            a = sp.zeros(n)
            a[i, j], a[j, i] = -sp.I / 2, sp.I / 2
            gens.append(a)
    for l in range(1, n):
        d = sp.zeros(n)
        for i in range(l):
            d[i, i] = 1
        d[l, l] = -l
        gens.append(d / sp.sqrt(2 * l * (l + 1)))
    return gens


T3L = su_n_generators(3)
# order produced: (01 s, 01 a, 02 s, 02 a, 12 s, 12 a, diag1 = T3, diag2 = T8)
T3_, T8_ = T3L[6], T3L[7]
assert T3_ == sp.diag(R(1, 2), -R(1, 2), 0) and sp.simplify(T8_ - sp.diag(1, 1, -2) / (2 * sp.sqrt(3))) == sp.zeros(3)


def adjoint_casimir(gens):
    """C2(G) from the structure constants: f_acd f_bcd = C2 delta_ab, evaluated for a = b = 0."""
    n = len(gens)
    tot = 0
    for c in range(n):
        for d in range(n):
            comm = gens[0] * gens[c] - gens[c] * gens[0]
            f = sp.simplify(-2 * sp.I * (comm * gens[d]).trace())      # f_{0cd}
            tot += f * f
    return sp.nsimplify(sp.simplify(tot))


C2_SU3 = adjoint_casimir(T3L)
C2_SU2 = adjoint_casimir(su_n_generators(2))
print(" adjoint Casimirs from structure constants: SU(2)", C2_SU2, " SU(3)", C2_SU3)


def charges(X, beta, anti=False):
    sgn = -1 if anti else 1                       # antitriplet: -t^*; T3, T8 are real diagonal
    Q = sgn * (T3_ + beta * T8_) + X * sp.eye(3)
    return [sp.nsimplify(sp.simplify(Q[i, i])) for i in range(3)]


def quark_charges(Nc, beta):
    """Q_u - Q_d = 1 and cancellation of the [SU(3)_L]^2 U(1)_X anomaly with Q_e = -1."""
    Qu, Qd, XL, Xt, Xa = sp.symbols("Qu Qd XL Xt Xa")
    Ng, nA = Nc, sp.Rational(1 + Nc, 2)
    nT = Ng - nA
    eqs = [sp.Eq(charges(XL, beta)[1], -1),                       # electron
           sp.Eq(charges(Xt, beta)[0], Qu), sp.Eq(charges(Xt, beta)[1], Qd),
           sp.Eq(charges(Xa, beta, True)[1], Qu),                 # antitriplet: (Q_d, Q_u) order (T3 flips)
           sp.Eq(Ng * XL + Nc * nT * Xt + Nc * nA * Xa, 0)]       # sum of X over SU(3)_L (anti)triplets, T(3)=T(3bar)
    sol = sp.solve(eqs, [Qu, Qd, XL, Xt, Xa], dict=True)
    assert len(sol) == 1
    s = sol[0]
    assert sp.simplify(charges(s[Xa], beta, True)[0] - s[Qd]) == 0
    return s[Qu], s[Qd], s[XL], s[Xt], s[Xa]


SCALARS = {-1: (R(-1, 3), R(2, 3), R(-1, 3)), +1: (R(1, 3), R(1, 3), R(-2, 3))}     # SPEC section 2 postulate


def field_content(Nc, sign, singlet_colour=True, singlet_per_family=True):
    """Weyl multiplets: dict(mult, L in {'3','3b','1'}, colour dim, X). Singlets: X = -Q for each charged component."""
    beta = sign / sp.sqrt(3)
    Qu, Qd, XL, Xt, Xa = quark_charges(Nc, beta)
    Ng, nA = Nc, sp.Rational(1 + Nc, 2)
    nT = Ng - nA
    trip = [(Ng, "3", 1, XL), (nT, "3", Nc, Xt), (nA, "3b", Nc, Xa)]
    f = []
    for mult, rep, col, X in trip:
        f.append(dict(mult=mult, L=rep, col=col, X=X, cbar=False))
        for q in charges(X, beta, rep == "3b"):
            if q != 0:
                f.append(dict(mult=mult if singlet_per_family else 1, L="1",
                              col=col if singlet_colour else 1, X=-q, cbar=col > 1 and singlet_colour))
    s = [dict(mult=1, L="3", col=1, X=X) for X in SCALARS[sign]]
    return f, s, (Qu, Qd, XL, Xt, Xa)


def traces(fields, Nc):
    """Explicit traces over the full reducible representation: Tr X^2, Tr t_1 t_1 (SU(3)_L), colour index."""
    trX = trL = trC = 0
    t1 = T3L[0]
    for F in fields:
        dL = 1 if F["L"] == "1" else 3
        tL = sp.zeros(1) if F["L"] == "1" else (t1 if F["L"] == "3" else -t1.conjugate())
        trX += F["mult"] * F["col"] * dL * F["X"] ** 2
        trL += F["mult"] * F["col"] * (tL * tL).trace()
        trC += F["mult"] * dL * (R(1, 2) if F["col"] > 1 else 0)
    return sp.nsimplify(trX), sp.nsimplify(trL), sp.nsimplify(trC)


def b_331(Nc, sign, **kw):
    f, s, _ = field_content(Nc, sign, **kw)
    fX, fL, fC = traces(f, Nc)
    sX, sL, sC = traces(s, Nc)
    bX = R(2, 3) * fX + R(1, 3) * sX
    bL = -R(11, 3) * C2_SU3 + R(2, 3) * fL + R(1, 3) * sL
    bC = -R(11, 3) * Nc + R(2, 3) * fC + R(1, 3) * sC
    return bX, bL, bC


def anomalies(Nc, sign, **kw):
    f, _, _ = field_content(Nc, sign, **kw)
    dim = lambda F: (1 if F["L"] == "1" else 3) * F["col"]
    sgnL = {"3": 1, "3b": -1, "1": 0}
    return {"X^3": sum(F["mult"] * dim(F) * F["X"] ** 3 for F in f),
            "grav^2 X": sum(F["mult"] * dim(F) * F["X"] for F in f),
            "SU3L^2 X": sum(F["mult"] * F["col"] * F["X"] for F in f if F["L"] != "1"),
            "SUNc^2 X": sum(F["mult"] * (1 if F["L"] == "1" else 3) * F["X"] for F in f if F["col"] > 1),
            "SU3L^3": sum(F["mult"] * F["col"] * sgnL[F["L"]] for F in f),
            "SUNc^3": sum(F["mult"] * (1 if F["L"] == "1" else 3) * (-1 if F["cbar"] else 1) for F in f if F["col"] > 1)}


def sm_coefficients(Ng=3, Nc=3):
    """b_Y, b_2 by explicit sums (hypercharges from Q = T3 + Y with the quark charges for N_c colours)."""
    Qu, Qd = R(Nc + 1, 2 * Nc), R(1 - Nc, 2 * Nc)
    YQ = Qu - R(1, 2)
    ferm = [(Ng * Nc, 2, YQ), (Ng * Nc, 1, -Qu), (Ng * Nc, 1, -Qd), (Ng, 2, R(-1, 2)), (Ng, 1, R(1))]
    bY = R(2, 3) * sum(m * d * y**2 for m, d, y in ferm) + R(1, 3) * 2 * R(1, 4)
    b2 = -R(11, 3) * C2_SU2 + R(2, 3) * sum(m * R(1, 2) for m, d, y in ferm if d == 2) + R(1, 3) * R(1, 2)
    return bY, b2


bY, b2 = sm_coefficients()
print(" SM: b_Y, b_2 =", bY, b2, "  (N_c = N_g = 5 counterfactual:", sm_coefficients(5, 5), ")")
OUT["sm"] = [str(bY), str(b2)]
OUT["b_331"] = {}
for sign, name in ((-1, "-1/sqrt3"), (+1, "+1/sqrt3")):
    for Nc in (1, 3, 5, 7, 9):
        bX, bL, bC = b_331(Nc, sign)
        an = anomalies(Nc, sign)
        Qu, Qd, XL, Xt, Xa = field_content(Nc, sign)[2]
        OUT["b_331"][f"{name}|{Nc}"] = [str(bX), str(bL), str(bC)]
        print(f" {name} Nc={Nc}: Qu,Qd={Qu},{Qd} XL,Xt,Xa={XL},{Xt},{Xa}  b_X={bX}  b_L={bL}  b_c={bC}  anomalies all zero:",
              all(sp.simplify(v) == 0 for v in an.values()))
# closed forms in N_c (fit and verify)
N = sp.symbols("N")
for sign, name in ((-1, "-1/sqrt3"), (+1, "+1/sqrt3")):
    pts = [(Nc, b_331(Nc, sign)[0]) for Nc in (1, 3, 5, 7, 9, 11)]
    poly = sp.factor(sp.interpolate(pts[:4], N))
    ok = all(sp.simplify(poly.subs(N, n) - v) == 0 for n, v in pts)
    print(f" {name}: b_X(N_c) = {poly}  (cubic through N_c = 1,3,5,7; holds at 9, 11: {ok})")
    OUT[f"bX_poly|{name}"] = str(poly)

print(" -- alternative singlet-counting readings (N_c = 3) --")
for sign, name in ((-1, "-1/sqrt3"), (+1, "+1/sqrt3")):
    for label, kw in (("one per copy, coloured (SPEC)", {}),
                      ("colourless singlets", dict(singlet_colour=False)),
                      ("one per component type, not per family", dict(singlet_per_family=False))):
        bX = b_331(3, sign, **kw)[0]
        an = {k: v for k, v in anomalies(3, sign, **kw).items() if sp.simplify(v) != 0}
        print(f"   {name} {label}: b_X = {bX}; non-zero anomalies: {an if an else 'none'}")
        OUT[f"reading|{name}|{label}"] = [str(bX), {k: str(v) for k, v in an.items()}]

# =====================================================================================================
# 3. Matching: photon as the null vector of the gauge-boson mass matrix (sympy), then the poles (mpmath)
# =====================================================================================================
print("== 3. matching and poles ==")


def inv_e2_symbolic(sign):
    g, gX, v1, v2, w = sp.symbols("g g_X v1 v2 w", positive=True)
    beta = sign / sp.sqrt(3)
    gens = [g * t for t in T3L]
    M2 = sp.zeros(9)
    for X in SCALARS[sign]:
        q = charges(X, beta)
        neutral = [i for i in range(3) if q[i] == 0]
        # generic vev in every neutral component (a superset of SPEC's assignment)
        vev = sp.zeros(3, 1)
        for i, s in zip(neutral, sp.symbols(f"a{len(neutral)}_0:3", positive=True)):
            vev[i] = s
        G = gens + [gX * X * sp.eye(3)]
        for a in range(9):
            for b in range(9):
                M2[a, b] += ((G[a] * vev).H * (G[b] * vev))[0] + ((G[b] * vev).H * (G[a] * vev))[0]
    # photon candidate: e Q = e (T3 + beta T8 + X) -> components (e/g, e beta/g, e/gX) along (W3, W8, B)
    n = sp.zeros(9, 1)
    n[6], n[7], n[8] = 1 / g, beta / g, 1 / gX
    null = sp.simplify(M2 * n)
    inv_e2 = sp.simplify((n.T * n)[0])
    return null == sp.zeros(9, 1), inv_e2


for sign, name in ((-1, "-1/sqrt3"), (+1, "+1/sqrt3")):
    ok, ie2 = inv_e2_symbolic(sign)
    print(f" {name}: (1/g, beta/g, 1/g_X) is a null vector of the mass matrix for any neutral vevs: {ok};  1/e^2 = {ie2}")
    OUT[f"inv_e2|{name}"] = str(ie2)

mz, ainv, s2, mu0 = M(I.MZ_MEAS), M(I.ALPHA_MZ_INV), M(I.S2_MZ), M(I.MU_331)


def boundary(mu, bY_=bY, b2_=b2):
    t = mp.log(mu / mz) / (2 * mp.pi)
    aY = (1 - s2) * ainv - mp.mpf(bY_.p) / bY_.q * t
    a2 = s2 * ainv - mp.mpf(b2_.p) / b2_.q * t
    # 1/e^2 = 1/g_Y^2 + 1/g_2^2 (SM) = (1 + beta^2)/g_L^2 + 1/g_X^2 (3-3-1), g_L = g_2, beta^2 = 1/3
    return aY, a2, aY - a2 / 3


aY0, a20, aX0 = boundary(mu0)
print(" 1/alpha_Y, 1/alpha_2, 1/alpha_X at MU_331:", mp.nstr(aY0, 17), mp.nstr(a20, 17), mp.nstr(aX0, 17))
OUT["boundary"] = [mp.nstr(aY0, 17), mp.nstr(a20, 17), mp.nstr(aX0, 17)]
mpl = mp.sqrt(M(I.HBAR) * M(I.C_LIGHT) ** 5 / M(I.G_NEWTON)) / (M(I.E_CH) * mp.mpf(10) ** 9)
print(" M_Pl = sqrt(hbar c^5/G) =", mp.nstr(mpl, 12), "GeV")
OUT["mpl"] = mp.nstr(mpl, 17)


def pole(bX, aX=aX0, target=1):
    return mu0 * mp.exp(2 * mp.pi * (aX - target) / (mp.mpf(bX.p) / bX.q))


def pole_ode(bX):
    """Independent numerical route: RK4 on dg/dt = b g^3/(16 pi^2), stop at g^2 = 4 pi (alpha_X = 1)."""
    b = mp.mpf(bX.p) / bX.q
    g = mp.sqrt(4 * mp.pi / aX0)
    gc = mp.sqrt(4 * mp.pi)
    f = lambda y: b * y**3 / (16 * mp.pi**2)
    t, h = mp.mpf(0), mp.mpf("0.01")
    while True:
        k1 = f(g); k2 = f(g + h * k1 / 2); k3 = f(g + h * k2 / 2); k4 = f(g + h * k3)
        gn = g + h * (k1 + 2 * k2 + 2 * k3 + k4) / 6
        if gn >= gc:
            if h < mp.mpf("1e-12"):
                return mu0 * mp.exp(t + h * (gc - g) / (gn - g))
            h /= 10
            continue
        g, t = gn, t + h


OUT["poles"] = {}
for sign, name in ((-1, "-1/sqrt3"), (+1, "+1/sqrt3")):
    q3, q5 = I.POLES_331[name]
    for Nc in (1, 3, 5, 7):
        bX = b_331(Nc, sign)[0]
        p = pole(bX)
        true_pole = pole(bX, target=0)
        extra = ""
        if Nc in (3, 5):
            ode = pole_ode(bX)
            q = q3 if Nc == 3 else q5
            extra = f"  RK4 rel {mp.nstr(ode / p - 1, 3)};  / three-loop quoted = {mp.nstr(p / M(q), 5)}"
        print(f" {name} Nc={Nc}: b_X={bX}  alpha_X=1 at {mp.nstr(p, 13)} GeV  (1/alpha_X=0 at {mp.nstr(true_pole, 5)};"
              f" pole/M_Pl = {mp.nstr(p / mpl, 5)}){extra}")
        OUT["poles"][f"{name}|{Nc}"] = mp.nstr(p, 17)
    p3, p5 = pole(b_331(3, sign)[0]), pole(b_331(5, sign)[0])
    lo, hi = (mpl / p3) ** 2, (mpl / p5) ** 2
    print(f" {name}: N_c=3 selected (p5 < M_Pl < p3): {p5 < mpl < p3};  G window (lo, hi) = ({mp.nstr(lo, 13)}, {mp.nstr(hi, 13)})")
    OUT[f"g_window|{name}"] = [mp.nstr(lo, 17), mp.nstr(hi, 17)]
    # robustness of the selection
    b3 = b_331(3, sign)[0]
    bcrit = 2 * mp.pi * (aX0 - 1) / mp.log(mpl / mu0)
    print(f"   b_X at which the N_c=3 pole would sit at M_Pl: {mp.nstr(bcrit, 8)} = b_X(3) x {mp.nstr(bcrit / (mp.mpf(b3.p) / b3.q), 6)};"
          f"  b_X(5)/that = {mp.nstr((mp.mpf(b_331(5, sign)[0].p) / b_331(5, sign)[0].q) / bcrit, 5)}")
    OUT[f"bcrit|{name}"] = mp.nstr(bcrit, 12)
    for fac in ("0.9", "1.1"):
        pp3 = pole(b3 * R(fac)); pp5 = pole(b_331(5, sign)[0] * R(fac))
        print(f"   b_X x {fac}: poles {mp.nstr(pp3, 5)}, {mp.nstr(pp5, 5)} GeV; selection holds: {pp5 < mpl < pp3}")
    # the other reading of 'the SM below': an N_c = N_g = 5 Standard Model below MU_331 for the N_c = 5 pole
    aX5 = boundary(mu0, *sm_coefficients(5, 5))[2]
    print(f"   N_c=5 pole if the theory below MU_331 also had 5 colours and generations (same M_Z boundary): "
          f"{mp.nstr(pole(b_331(5, sign)[0], aX5), 6)} GeV (SPEC reading: {mp.nstr(p5, 6)})")
    OUT[f"pole5_altSM|{name}"] = mp.nstr(pole(b_331(5, sign)[0], aX5), 12)
    # alternative singlet readings
    for label, kw in (("colourless singlets", dict(singlet_colour=False)),
                      ("not per family", dict(singlet_per_family=False))):
        a3, a5 = pole(b_331(3, sign, **kw)[0]), pole(b_331(5, sign, **kw)[0])
        print(f"   reading '{label}': poles {mp.nstr(a3, 5)}, {mp.nstr(a5, 5)} GeV; selection holds: {a5 < mpl < a3}")

# =====================================================================================================
# 4. pi0 -> gamma gamma and the O(p^4) pion mass at the derived f_pi
# =====================================================================================================
print("== 4. pi0 width, O(p^4) pion mass ==")
alpha0, mpi0 = mp.mpf(1) / mp.mpf("137.035999084"), M(I.M_PI0)
assert abs(alpha0 - mp.mpf(I.ALPHA_0)) < 1e-18
Qu3, Qd3 = quark_charges(3, -1 / sp.sqrt(3))[:2]
anom = 3 * (Qu3**2 - Qd3**2)
F92 = fpi / mp.sqrt(2)


def pi0_width(F):                  # Gamma = alpha^2 m^3 [N_c (Q_u^2 - Q_d^2)]^2 / (64 pi^3 F^2), F ~ 92 MeV
    return alpha0**2 * mpi0**3 * mp.mpf(int(anom)) ** 2 / (64 * mp.pi**3 * F**2) * mp.mpf(10) ** 9


def chpt(F92_):                    # M^2 = 2 m Sigma/F^2, F = F_pi/(F_pi/F); M_pi^2 = M^2 (1 - M^2 lbar3/(32 pi^2 F^2))
    Fc = F92_ / M(I.FPI_OVER_F)
    M2 = 2 * M(I.M_UD_FLAG) * M(I.COND_13) ** 3 / Fc**2
    return mp.sqrt(M2 * (1 - M2 * M(I.LBAR3) / (32 * mp.pi**2 * Fc**2)))


F_lat = mp.mpf("0.1302") / mp.sqrt(2)
w, w_lat = pi0_width(F92), pi0_width(F_lat)
m4, m4_lat = chpt(F92), chpt(F_lat)
print(" N_c (Q_u^2 - Q_d^2) =", anom, "; F = f_pi/sqrt2 =", mp.nstr(F92, 12))
print(" pi0 width (eV): derived f_pi", mp.nstr(w, 14), "; lattice 130.2/sqrt2:", mp.nstr(w_lat, 10),
      "; +-%s eV from delta_pi" % mp.nstr(w * 2 * err_delta / fpi, 3))
print(" O(p^4) m_pi (GeV): derived f_pi", mp.nstr(m4, 14), "; lattice:", mp.nstr(m4_lat, 10))
print(" pulls: pi0 width vs PrimEx %s +- %s: %s sigma" % (I.GAMMA_PI0, mp.nstr(I.GAMMA_PI0_ERR, 3),
                                                        mp.nstr((w - M(I.GAMMA_PI0)) / mp.mpf(I.GAMMA_PI0_ERR), 3)))
OUT.update(pi0_width=mp.nstr(w, 17), chpt_mpi=mp.nstr(m4, 17), pi0_width_lattice=mp.nstr(w_lat, 12),
           chpt_mpi_lattice=mp.nstr(m4_lat, 12))

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "third_route.json"), "w") as fh:
    json.dump(OUT, fh, indent=1)
