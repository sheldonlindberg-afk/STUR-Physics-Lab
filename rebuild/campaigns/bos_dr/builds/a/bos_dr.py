"""Bosonic part of the one-loop on-shell Delta r of muon decay (SPEC.md); see DERIVATION.md.

Structure
* a small d-dimensional Dirac engine and a zero-external-momentum loop-integral reducer (partial fractions in q^2,
  MS-bar with the O(eps) x pole pieces kept) -- DERIVATION sections 2-3;
* the vertex (Z exchange, W-gamma and W-Z triangles), lepton LSZ, W-gamma / W-Z box and Fermi-theory QED pieces,
  built from the doublet coupling matrices derived from the Lagrangian -- section 4 (sympy, lazily, cached);
* the on-shell assembly with the provided bos_se self-energies -- section 6; the M_H dependence is evaluated with my own
  Higgs-diagram formulas at a locally raised mpmath precision -- section 7.
"""
import math
import functools
import itertools

import numpy as np
import sympy as sp
import mpmath as mp

import bos_se

# ------------------------------------------------------------------------------------------------------------------
# symbols
# ------------------------------------------------------------------------------------------------------------------
d = sp.Symbol("d")
P = sp.Symbol("P")                                   # 1/eps (UV pole marker), d = 4 - 2 eps
x = sp.Symbol("x")                                   # q^2
g, c = sp.symbols("g c", positive=True)
s = sp.sqrt(1 - c**2)
mW2, mZ2, lam2 = sp.symbols("mW2 mZ2 lam2", positive=True)
LW, LZ, LL = sp.symbols("L_W L_Z L_lam")             # ln(m^2/mu^2)
LOGS = {mW2: LW, mZ2: LZ, lam2: LL}


# ------------------------------------------------------------------------------------------------------------------
# d-dimensional gamma contraction (DERIVATION section 3)
# ------------------------------------------------------------------------------------------------------------------
def contract(string):
    """Contract all repeated Lorentz indices of a product of gamma matrices; returns {free-index tuple: coeff(d)}."""
    string = tuple(string)
    for i, a in enumerate(string):
        if a in string[i + 1:]:
            j = string.index(a, i + 1)
            break
    else:
        return {string: sp.Integer(1)}
    out = {}

    def add(dct, f):
        for k, v in dct.items():
            out[k] = sp.expand(out.get(k, 0) + f * v)
    if j == i + 1:
        add(contract(string[:i] + string[j + 1:]), d)
        return out
    # gamma^b gamma_a = 2 g^{b a} - gamma_a gamma^b ; g^{b a} renames the partner of a (at i) into b
    b = string[j - 1]
    renamed = string[:i] + (b,) + string[i + 1:j - 1] + string[j + 1:]
    add(contract(renamed), 2)
    add(contract(string[:j - 1] + (a, b) + string[j + 1:]), -1)
    return out


def coeff_of(string, free):
    return sp.factor(contract(string).get(tuple(free), 0))


@functools.lru_cache(None)
def dirac():
    """Dirac coefficients (functions of d) of DERIVATION section 3."""
    cV = coeff_of(["r", "s", "a", "s", "r"], ["a"]) / d                          # gamma^r qs gamma^a qs gamma_r / q^2
    rpr = coeff_of(["r", "p", "r"], ["p"])                                         # gamma^r ps gamma_r
    # Sigma: gamma^r (ps+qs) gamma_r/(p+q)^2 -> rpr [ps/q^2 - (2/d) ps q^2/q^4]  (both reduce to 1/(q^2 (q^2-M^2)))
    cS = sp.factor(rpr * (1 - sp.Integer(2) / d))
    # non-abelian: gamma^r qs gamma^s [g_ar q_s - 2 g_rs q_a + g_sa q_r]
    cNA = sp.factor(coeff_of(["a", "t", "t"], ["a"]) / d - 2 * coeff_of(["r", "a", "r"], ["a"]) / d
                    + coeff_of(["t", "t", "a"], ["a"]) / d)
    return cV, cS, cNA


# explicit 4x4 matrices (checks and the d = 4 box algebra)
def _gammas():
    I2, Z2 = np.eye(2), np.zeros((2, 2))
    sx = np.array([[0, 1], [1, 0]], complex)
    sy = np.array([[0, -1j], [1j, 0]], complex)
    sz = np.array([[1, 0], [0, -1]], complex)
    g0 = np.block([[Z2, I2], [I2, Z2]]).astype(complex)
    gs = [np.block([[Z2, si], [-si, Z2]]) for si in (sx, sy, sz)]
    G = [g0] + gs
    g5 = 1j * G[0] @ G[1] @ G[2] @ G[3]
    return G, g5, np.diag([1.0, -1.0, -1.0, -1.0])


@functools.lru_cache(None)
def box_fierz(order1, order2):
    """K with  sum (gamma-string1 P_L) x (gamma-string2 P_L) = K gamma^a P_L x gamma_a P_L  (d = 4, explicit matrices).
    order = permutation of ('a','s','r') giving the index order of the three gammas."""
    G, g5, eta = _gammas()
    PL = (np.eye(4) - g5) / 2
    lo = [G[m] for m in range(4)]
    up = [eta[m, m] * G[m] for m in range(4)]                       # gamma_mu
    lhs = np.zeros((16, 16), complex)
    for ia, isg, ir in itertools.product(range(4), repeat=3):
        idx = {"a": ia, "s": isg, "r": ir}
        A = np.eye(4, dtype=complex)
        B = np.eye(4, dtype=complex)
        for t in order1:
            A = A @ lo[idx[t]]
        for t in order2:
            B = B @ up[idx[t]]
        lhs += np.kron(A @ PL, B @ PL)
    t0 = sum(np.kron(lo[m] @ PL, up[m] @ PL) for m in range(4))
    K = np.vdot(t0.ravel(), lhs.ravel()) / np.vdot(t0.ravel(), t0.ravel())
    assert np.allclose(lhs, K * t0)
    return float(K.real)


# ------------------------------------------------------------------------------------------------------------------
# loop integrals at zero external momentum (DERIVATION section 2): result = fin + P * res
# ------------------------------------------------------------------------------------------------------------------
def _T(k, m2):
    """int_n 1/(q^2-m^2)^k as (fin, res)."""
    L = LOGS[m2]
    if k == 1:
        return m2 * (1 - L), m2
    if k == 2:
        return -L, sp.Integer(1)
    return (-1)**k * sp.factorial(k - 3) / sp.factorial(k - 1) * m2**(2 - k), sp.Integer(0)


@functools.lru_cache(None)
def integ(n, props):
    """int_n (q^2)^n / prod_i (q^2 - m_i^2)^{k_i}, props = ((m2, k), ...) with m2 = 0 for a massless line."""
    expr = x**n / sp.Mul(*[(x - m)**k for m, k in props])
    fin, res = sp.Integer(0), sp.Integer(0)
    for term in sp.Add.make_args(sp.apart(sp.together(expr), x)):
        num, den = sp.fraction(sp.together(term))
        if not den.has(x):
            continue                                                  # polynomial in q^2: scaleless
        facs = [(f, k) for f, k in sp.factor_list(den)[1] if f.has(x)]
        assert len(facs) == 1, term
        f, k = facs[0]
        pl = sp.Poly(f, x)
        assert pl.degree() == 1
        m = sp.simplify(-pl.all_coeffs()[1] / pl.all_coeffs()[0])
        coef = sp.simplify(term * (x - m)**k)
        assert not coef.has(x)
        if m == 0:
            assert k == 1, ("IR divergent massless pole", term)       # only lambda regulates the IR
            continue
        tf, tr = _T(k, m)
        fin += coef * tf
        res += coef * tr
    return sp.simplify(fin), sp.simplify(res)


def ms(cd, I):
    """c(d) * (fin + res/eps) -> fin + P*res with the O(eps) x pole piece (d = 4 - 2 eps)."""
    fin, res = I
    c4 = cd.subs(d, 4) if isinstance(cd, sp.Basic) else cd
    c1 = sp.diff(cd, d).subs(d, 4) if isinstance(cd, sp.Basic) else 0
    return c4 * fin - 2 * c1 * res + P * c4 * res


def props(*pairs):
    acc = {}
    for m, k in pairs:
        acc[m] = acc.get(m, 0) + k
    return tuple(sorted(acc.items(), key=lambda t: str(t[0])))


# ------------------------------------------------------------------------------------------------------------------
# couplings (DERIVATION section 1)
# ------------------------------------------------------------------------------------------------------------------
T1 = sp.Matrix([[0, 1], [1, 0]]) / 2
T2 = sp.Matrix([[0, -sp.I], [sp.I, 0]]) / 2
T3 = sp.Matrix([[1, 0], [0, -1]]) / 2
Y = -sp.eye(2) / 2
Q = T3 + Y
e = g * s
G = {"W1": g * T1, "W2": g * T2, "Z": (g / c) * (T3 - s**2 * Q), "A": e * Q}
GR = {"Z": -(g / c) * s**2 * Q, "A": e * Q}                  # right-handed (only the charged entry is physical)
MASS = {"W1": mW2, "W2": mW2, "Z": mZ2, "A": lam2}
IDX = {"W1": 1, "W2": 2, "Z": 3, "A": 3}
KAP = {"W1": 1, "W2": 1, "Z": c, "A": s}
BOSONS = ("W1", "W2", "Z", "A")
TA = {"W1": T1, "W2": T2}


def lam3(a, X, Yb):
    return g * sp.LeviCivita(IDX[a], IDX[X], IDX[Yb]) * KAP[a] * KAP[X] * KAP[Yb]


def F_ex(X):                         # type (a): exchange of X between the two legs (units 1/16pi^2)
    cV = dirac()[0]
    return ms(cV, integ(1, props((0, 2), (MASS[X], 1))))


def F_NA(X, Yb):                     # type (b): triangle with the triple vertex
    cNA = dirac()[2]
    return ms(cNA, integ(1, props((0, 1), (MASS[X], 1), (MASS[Yb], 1))))


def F_S(X):                          # Sigma_L coefficient per unit coupling^2
    cS = dirac()[1]
    return ms(cS, integ(1, props((0, 2), (MASS[X], 1))))


def vertex_matrix(ext):
    """Doublet matrix M^ext (multiplying i gamma P_L, units 1/16pi^2) of the one-loop vertex, external boson ext."""
    M = sp.zeros(2, 2)
    for X in BOSONS:
        M += G[X] * G[ext] * G[X] * F_ex(X)
    for X, Yb in itertools.product(BOSONS, repeat=2):
        l3 = lam3(ext, X, Yb)
        if l3 != 0:
            M += -sp.I * l3 * G[X] * G[Yb] * F_NA(X, Yb)
    return M.applyfunc(sp.expand)


def sigma_L(f):
    """Sigma_L of the left-handed doublet member f (0 = neutrino, 1 = charged lepton), units 1/16pi^2."""
    return sp.expand(sum((G[X] * G[X])[f, f] * F_S(X) for X in BOSONS))


def _final(expr):
    """Impose M_Z^2 = M_W^2/c^2, take lambda -> 0 after checking that ln(lambda) drops; returns (fin, pole, IRcoef)."""
    expr = sp.expand(expr)
    pole = sp.simplify(expr.coeff(P))
    fin = expr.subs(P, 0)
    fin = sp.expand(fin.subs({mZ2: mW2 / c**2, LZ: LW - sp.log(c**2)}))
    ir = sp.simplify(fin.coeff(LL).subs(lam2, 0))
    fin = sp.simplify(sp.expand(fin.subs(LL, 0)).subs(lam2, 0))
    pole = sp.simplify(pole.subs(mZ2, mW2 / c**2).subs(lam2, 0))
    return fin, pole, ir


@functools.lru_cache(None)
def derive_vb():
    """delta_VB(mu) = vertices + boxes + LSZ - Fermi QED (units 1/16pi^2): dict of pieces (fin, pole, IR coeff)."""
    out = {}
    norm = sum(g**2 * TA[a][0, 1] * TA[a][1, 0] for a in TA)                 # tree, real basis
    Ma = {a: vertex_matrix(a) for a in TA}
    d1 = sum(Ma[a][0, 1] * g * TA[a][1, 0] for a in TA) / norm
    d2 = sum(g * TA[a][0, 1] * Ma[a][1, 0] for a in TA) / norm
    lsz = sigma_L(0) + sigma_L(1)                       # 4 legs x 1/2 (mu, nu_mu, e, nu_e; two identical doublets)
    # boxes (d = 4 algebra): line 1 element (nu, l), line 2 element (l, nu)
    line1 = {"Vmu": (lambda a, V: (G[a] * G[V])[0, 1], -1, ("a", "s", "r")),
             "Vnu": (lambda a, V: (G[V] * G[a])[0, 1], +1, ("r", "s", "a"))}
    line2 = {"Ve": (lambda a, V: (G[V] * G[a])[1, 0], -1, ("r", "s", "a")),
             "Vnue": (lambda a, V: (G[a] * G[V])[1, 0], +1, ("a", "s", "r"))}
    box = 0
    for V in ("Z", "A"):
        I = integ(1, props((0, 2), (MASS[V], 1), (mW2, 1)))
        assert sp.simplify(I[1]) == 0                    # UV finite
        for (f1, s1, o1), (f2, s2, o2) in itertools.product(line1.values(), line2.values()):
            K = sp.nsimplify(box_fierz(o1, o2)) / 4      # q^mu q^nu -> q^2 g^{mu nu}/4
            cpl = sum(f1(a, V) * f2(a, V) for a in TA) / norm
            box += -mW2 * cpl * s1 * s2 * K * I[0]
    # WW "box": the doublet algebra gives no allowed charge flow
    ww = sum((G[a] * G[b])[0, 1] * (G[a] * G[b])[1, 0] + (G[a] * G[b])[0, 1] * (G[b] * G[a])[1, 0]
             for a in TA for b in TA)
    assert sp.simplify(ww) == 0
    # Fermi theory, charge-retention form [e gamma P_L mu][nu_mu gamma P_L nu_e]: photon vertex + LSZ of mu and e
    fermi_vertex = e**2 * F_ex("A")
    fermi_lsz = e**2 * F_S("A")                         # 2 legs x 1/2
    fermi = sp.expand(fermi_vertex + fermi_lsz)
    out["vertex1"] = _final(d1)
    out["vertex2"] = _final(d2)
    out["lsz"] = _final(lsz)
    out["box"] = _final(box)
    out["fermi_vertex"] = _final(fermi_vertex)
    out["fermi_lsz"] = _final(fermi_lsz)
    out["fermi"] = _final(fermi)
    tot = sp.expand(d1 + d2 + lsz + box - fermi)
    out["total"] = _final(tot)
    return out


@functools.lru_cache(None)
def derive_ward():
    """Thomson-limit photon coupling: predicted Sigma^AZ(0)/M_Z^2 (units 1/16pi^2) from neutrino neutrality, and the
    left - right universality residue for the charged lepton (must vanish)."""
    MA = vertex_matrix("A")
    sAZ = sp.Symbol("sAZ")
    resid_nu = MA[0, 0] + G["Z"][0, 0] * sAZ
    pred = sp.solve(sp.expand(resid_nu), sAZ)[0]
    left_l = MA[1, 1] + sigma_L(1) * G["A"][1, 1] + G["Z"][1, 1] * pred
    right_l = GR["Z"][1, 1] * pred
    return _final(pred), _final(sp.expand(left_l - right_l))


@functools.lru_cache(None)
def _vb_func():
    fin = derive_vb()["total"][0]
    return sp.lambdify((g, c, LW), fin, modules="mpmath")


def delta_vb_mu(MW, MZ, alpha, mu):
    """delta_VB in MS-bar at the scale mu (vertices + boxes + LSZ - Fermi QED), dimensionless."""
    with mp.workdps(30):
        cm = mp.mpf(MW) / mp.mpf(MZ)
        g2 = 4 * mp.pi * mp.mpf(alpha) / (1 - cm**2)
        val = _vb_func()(mp.sqrt(g2), cm, mp.log(mp.mpf(MW)**2 / mp.mpf(mu)**2)) / (16 * mp.pi**2)
        return float(val)


def delta_vb(MW, MZ, alpha):
    """Vertex + box + lepton LSZ contribution after the Fermi-theory QED subtraction (SPEC 4), = delta_VB(mu = M_W)."""
    return delta_vb_mu(MW, MZ, alpha, MW)


# ------------------------------------------------------------------------------------------------------------------
# self-energy assembly (DERIVATION section 6)
# ------------------------------------------------------------------------------------------------------------------
def _sigma_aa_prime(MW, MZ, MH, alpha, mu):
    h = 1e-3 * MW * MW
    f = lambda k2: bos_se.sigma_AA(k2, MW, MZ, MH, alpha, mu)
    D = lambda hh: (f(hh) - f(-hh)) / (2 * hh)
    return (4 * D(h) - D(2 * h)) / 3


def se_part_bos_se(MW, MZ, MH, alpha, mu):
    """2 delta e/e - delta s^2/s^2 + (Sigma^W(0) - delta M_W^2)/M_W^2 from the bos_se exports (doubles)."""
    c2 = (MW / MZ)**2
    s2 = 1 - c2
    cw, sw = math.sqrt(c2), math.sqrt(s2)
    aap = _sigma_aa_prime(MW, MZ, MH, alpha, mu)
    az0 = bos_se.sigma_AZ(0, MW, MZ, MH, alpha, mu)
    zz = bos_se.sigma_ZZ(MZ * MZ, MW, MZ, MH, alpha, mu)
    w0 = bos_se.sigma_W(0, MW, MZ, MH, alpha, mu)
    ww = bos_se.sigma_W(MW * MW, MW, MZ, MH, alpha, mu)
    return (aap + 2 * (sw / cw) * az0 / MZ**2 - (c2 / s2) * (zz / MZ**2 - ww / MW**2) + (w0 - ww) / MW**2)


# ---- Higgs-boson diagrams (M_H dependence at high precision; DERIVATION section 7) ----
def _J(r):
    """int_0^1 ln(x - r) dx, real part for real r."""
    if isinstance(r, mp.mpc):
        return (1 - r) * mp.log(1 - r) + r * mp.log(-r) - 1
    t1 = (1 - r) * mp.log(abs(1 - r)) if r != 1 else mp.mpf(0)
    t2 = r * mp.log(abs(r)) if r != 0 else mp.mpf(0)
    return t1 + t2 - 1


def _b0(k2, a, b, mu2):
    """MS-bar finite Re B0(k^2; m1^2 = a, m2^2 = b) = -int_0^1 ln[(x a + (1-x) b - x(1-x) k^2)/mu^2] dx."""
    if k2 == 0:
        if a == b:
            return -mp.log(a / mu2)
        return 1 - (a * mp.log(a / mu2) - b * mp.log(b / mu2)) / (a - b)
    B = a - b - k2
    disc = B * B - 4 * k2 * b
    if disc >= 0:
        sq = mp.sqrt(disc)
        qv = -(B + (1 if B >= 0 else -1) * sq) / 2
        x1, x2 = qv / k2, b / qv
        tot = mp.log(abs(k2)) + _J(x1) + _J(x2)
    else:
        x1 = mp.mpc(-B, mp.sqrt(-disc)) / (2 * k2)
        tot = mp.log(abs(k2)) + 2 * mp.re(_J(x1))
    return -(tot - mp.log(mu2))


def _a0(a, mu2):
    return a * (1 - mp.log(a / mu2))


def _b00(k2, m1, m2, mu2):
    """finite part of B00 for D1 = q^2 - m1, D2 = (q+k)^2 - m2 (m's are masses squared)."""
    B0 = _b0(k2, m1, m2, mu2)
    if k2 == 0:
        return (_a0(m2, mu2) + m1 * B0) / 4 + (m1 + m2) / 8
    f = k2 + m1 - m2
    B1 = (_a0(m1, mu2) - _a0(m2, mu2) - f * B0) / (2 * k2)
    return (_a0(m2, mu2) + 2 * m1 * B0 + f * B1) / 6 + (3 * m1 + 3 * m2 - k2) / 18


def _sigma_higgs(k2, M2, MH2, g2, mu2):
    """Higgs-boson diagrams of Sigma^W_T (M2 = M_W^2); Sigma^ZZ_T = this(M2 = M_Z^2)/c^2."""
    return g2 * (M2 * _b0(k2, M2, MH2, mu2) - _b00(k2, MH2, M2, mu2) + _a0(MH2, mu2) / 4) / (16 * mp.pi**2)


def _dps(*m):
    """B00 holds terms ~ M_H^4/k^2 and B0 terms ~ (M_H^2/k^2) ln that cancel down to ln M_H: keep 6 digits per decade
    of the mass ratio on top of 30."""
    r = max(m) / min(m)
    return 30 + 6 * int(math.ceil(math.log10(max(r, 10.0))))


def dr_higgs(MW, MZ, MH, alpha, mu):
    """Higgs-diagram part of the self-energy brackets of Delta r (mpf at the current precision)."""
    mw, mz, mh, mu_ = (mp.mpf(v) for v in (MW, MZ, MH, mu))
    cm2 = (mw / mz)**2
    s2 = 1 - cm2
    g2 = 4 * mp.pi * mp.mpf(alpha) / s2
    W = lambda k2: _sigma_higgs(k2, mw**2, mh**2, g2, mu_**2)
    Zf = lambda k2: _sigma_higgs(k2, mz**2, mh**2, g2, mu_**2) / cm2
    w0, ww, zz = W(mp.mpf(0)), W(mw**2), Zf(mz**2)
    return -(cm2 / s2) * (zz / mz**2 - ww / mw**2) + (w0 - ww) / mw**2


def delta_r_bos(MW, MZ, MH, alpha):
    """Delta r_bos: bosonic part of the one-loop on-shell Delta r (SPEC 3). Evaluated at mu = M_W (mu cancels)."""
    mu = MW
    mh_ref = MW
    rest = se_part_bos_se(MW, MZ, mh_ref, alpha, mu)
    with mp.workdps(_dps(MW, MZ, MH)):
        dh = dr_higgs(MW, MZ, MH, alpha, mu) - dr_higgs(MW, MZ, mh_ref, alpha, mu)
        dh = float(dh)
    return rest + dh + delta_vb_mu(MW, MZ, alpha, mu)


PROVENANCE = {
    "delta_r_bos": ("derived", "on-shell assembly 2de/e - ds^2/s^2 + (Sigma_W(0)-dMW^2)/MW^2 + delta_VB with bos_se "
                               "self-energies; M_H dependence from my Higgs diagrams at local mp precision"),
    "delta_vb": ("derived", "vertex (Z, W-gamma, W-Z) + boxes (WZ, W-gamma) + lepton LSZ - Fermi QED (=0), "
                            "'t Hooft-Feynman gauge, MS-bar at mu = M_W, lambda -> 0"),
}


# ------------------------------------------------------------------------------------------------------------------
# second routes and checks (DERIVATION section 8)
# ------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    MWv, MZv, MHv, AL = 80.38, 91.19, 125.0, 1 / 128.0
    cv, sv2 = MWv / MZv, 1 - (MWv / MZv)**2
    cV, cS, cNA = dirac()
    print("Dirac coefficients: cV =", cV, " cS =", cS, " cNA =", cNA)
    # d = 4 engine vs explicit matrices
    Gm, g5, eta = _gammas()
    lo = Gm
    up = [eta[m, m] * Gm[m] for m in range(4)]
    for a_ in range(4):
        lhs = sum(up[r] @ lo[s_] @ lo[a_] @ up[s_] @ lo[r] for r in range(4) for s_ in range(4))
        assert np.allclose(lhs, float(cV.subs(d, 4) * 4) * lo[a_])
    print("engine (d=4) == explicit matrices; box Fierz K(same) =", box_fierz(("a", "s", "r"), ("a", "s", "r")),
          " K(reversed) =", box_fierz(("a", "s", "r"), ("r", "s", "a")))
    res = derive_vb()
    for k, (fin, pole, ir) in res.items():
        print(f"  {k:13s} pole/(16pi^2) = {pole}   ln(lambda^2) coeff = {ir}\n      fin = {sp.simplify(fin)}")
    hand = g**2 * (6 + (7 - 4 * s**2) / (2 * s**2) * sp.log(c**2))
    print("route 1: sympy total at mu=M_W minus hand closed form =",
          sp.simplify(res["total"][0].subs(LW, 0) - hand))
    print("         total - (hand - 4 g^2 L_W) =", sp.simplify(res["total"][0] - hand + 4 * g**2 * LW))
    print("delta_vb =", delta_vb(MWv, MZv, AL),
          " hand =", AL / (4 * math.pi * sv2) * (6 + (7 - 4 * sv2) / (2 * sv2) * math.log(cv**2)))
    pred, resid = derive_ward()
    print("Ward: predicted Sigma^AZ(0)/MZ^2 (x16pi^2) =", sp.simplify(pred[0]), " pole", pred[1],
          "; charged-lepton L-R residue =", sp.simplify(resid[0]), resid[1])
    pf = sp.lambdify((g, c, LW), pred[0])
    for mu in (MWv, 300.0, 10.0):
        g2v = 4 * math.pi * AL / sv2
        print(f"   mu={mu}: bos_se Sigma^AZ(0) = {bos_se.sigma_AZ(0, MWv, MZv, MHv, AL, mu):.15e}  predicted = "
              f"{pf(math.sqrt(g2v), cv, math.log(MWv**2 / mu**2)) * MZv**2 / (16 * math.pi**2):.15e}")
    print("route 2 (UV, mu independence of the full sum):")
    for mu in (MWv, 300.0, 10.0, 2000.0):
        tot = se_part_bos_se(MWv, MZv, MHv, AL, mu) + delta_vb_mu(MWv, MZv, AL, mu)
        print(f"   mu = {mu:7.2f}: Delta r_bos = {tot:.15f}")
    print("Higgs part vs bos_se (pure-bos_se assembly vs hybrid):")
    for mh in (1.0, 10.0, 125.0, 1000.0, 1e4):
        pure = se_part_bos_se(MWv, MZv, mh, AL, MWv) + delta_vb(MWv, MZv, AL)
        print(f"   MH = {mh:8g}: pure {pure:.15f}  hybrid {delta_r_bos(MWv, MZv, mh, AL):.15f}")
    print("Sigma_AA(0) =", bos_se.sigma_AA(0, MWv, MZv, MHv, AL, MWv))
    with mp.workdps(60):                         # closed-form B0 vs direct Feynman-parameter quadrature
        for k2, a_, b_ in ((MWv**2, MWv**2, 1e20), (MZv**2, MZv**2, 1.0), (MWv**2, MWv**2, MWv**2)):
            k2, a_, b_ = mp.mpf(k2), mp.mpf(a_), mp.mpf(b_)
            q = -mp.quad(lambda t: mp.log(t * a_ + (1 - t) * b_ - t * (1 - t) * k2), [0, mp.mpf(1) / 2, 1])
            print(f"   B0 closed form - quadrature (k2={float(k2):.4g}, m2^2={float(b_):.3g}): "
                  f"{float(_b0(k2, a_, b_, mp.mpf(1)) - q):.2e}")
    B = 11 * AL / (48 * math.pi * sv2)
    for h1 in (1e3, 1e8, 1e12):
        f1, f2 = delta_r_bos(MWv, MZv, h1 * MWv, AL), delta_r_bos(MWv, MZv, 10 * h1 * MWv, AL)
        print(f"   slope at MH ~ {h1:g} MW: {(f2 - f1) / math.log(100.0) / B:.10f} x 11 alpha/(48 pi s^2)")
    print("Delta r_bos(MH = 125) =", delta_r_bos(MWv, MZv, MHv, AL), "; MH = 1e14:", delta_r_bos(MWv, MZv, 1e14, AL))
