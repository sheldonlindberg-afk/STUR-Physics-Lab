#!/usr/bin/env python3
"""
3-3-1 from geometry: SU(6) on the triangle T^2/Z_3, and what it gives of the 19 parameters.

An attempt, with every failure kept. The geometry is one flat triangle: the torus with
complex structure tau = exp(2 pi i/3), divided by a rotation of 120 degrees. It is two
equilateral triangles glued along their edges, with three corners (the fixed points). The Z_3
rotation exists only for this tau, so the shape has no free parameter.

Every row is one of
    CHECK      exact or numerical mathematics, verified here;
    MODEL      this script's construction on published ingredients;
    FAILS      a prediction of the construction that the measurements exclude;
    FIT        inputs chosen to match measurements: an existence statement, not a prediction.

Gauge sector
G1  The twist P = diag(1,1,1,w,w,w) on SU(6) leaves SU(3) x SU(3) x U(1): 3-3-1. (CHECK)
    Every 3-3-1 fermion of src/m331_standalone.py (beta = -1/sqrt3), the odd quark family
    included, is a piece of the SU(6) representations 6bar, 15 and 20. (CHECK)
    (LIT: 3-3-1 inside SU(6) is known: Deppisch, Hati, Patra, Sarkar and Valle, "331 Models and
    Grand Unification: From Minimal SU(5) to Minimal SU(6)", arXiv:1608.05334.)
G2  The embedding fixes g_3 = g_L and g_X^2 = (3/4) g^2 at the orbifold scale, so
    sin^2 theta_W = 3/8 there. (CHECK)
G3  With the minimal 3-3-1 content this fails: the two electroweak couplings meet near
    1e10 GeV, and the strong coupling predicted from that point is far below 0.118. The one
    scalar the orbifold itself supplies, the (3, 3bar) part of the extra-dimensional gauge
    field, does not rescue it. (FAILS; one and two loops)
G4  Which extra matter at the 3-3-1 scale would make it fit? Pieces of the SU(6)
    representations 6, 15, 20, 21 and 35, up to four multiplets, with the unified scale high
    enough for the proton. No set fits at two loops with every mass at mu_331; the smallest
    set that brackets the measurement fits once one mass is freed (LIT: tau(p -> e+ pi0) > 2.4e34 yr, Super-Kamiokande,
    Phys. Rev. D 102, 112011 (2020), arXiv:2010.16098; the lifetime here is the dimensional
    estimate M^4/(alpha^2 m_p^5), good to an order of magnitude). (FIT)

Flavour sector (zero modes in magnetic flux: Cremades, Ibanez and Marchesano, JHEP 05 (2004)
079, arXiv:hep-th/0404229; on orbifolds: Abe, Kobayashi and Ohki, JHEP 09 (2008) 043,
arXiv:0806.4748). Fermion zero modes in M units of flux are
    psi^{j,M}(z) = N exp(i pi M z Im z / Im tau) theta[j/M, 0](M z, M tau),   j = 0..M-1,
and a Yukawa coupling is the overlap integral of three of them. All integrals are done here.
T1  Z_3 content of the zero modes. Flux 6 has exactly three invariant modes: three
    generations. They are permuted like the three corners of the triangle. (CHECK)
T2  The one Higgs direction with the full symmetry of the triangle gives masses
    1 : 0.794 : 0.794. (FAILS)
T3  A Higgs concentrated at a point p gives the Yukawa matrix L_a(p) R_b(p): rank one, one
    massive generation. (CHECK)
T4  The Higgs potential. The local quartic alone is minimised by the triangular vortex
    lattice (Abrikosov's parameter, recomputed from one flux quantum per cell), which gives
    masses 1 : 1 : 0. A corner-concentrated Higgs is its maximum. Fermion loops, which lower
    the quartic in proportion to sum m^4, do not move the vacuum to a corner before the
    potential turns over. (FAILS)
T5  A light Higgs. If the Higgs is far lighter than the compactification scale, its direction
    is the lowest state of the Higgs mass matrix and the other four modes stay heavy. With
    mass terms of strengths k_1 > k_2 > k_3 at the corners the leak onto the weaker corners is
    set by one number, the overlap g of two Higgs corner states. (MODEL)
    Corner strengths fitted to the four quark mass ratios (FIT); the mixing matrix that
    follows is a prediction, and it is 30 to 60 times too small. (FAILS)
T6  The triangle form of a mass spectrum, sqrt(m_k) = a (1 + r cos(theta + 2 pi k/3)), is what
    a rotation-symmetric (circulant) matrix has. For the charged leptons r = sqrt2 is Koide's
    relation (src/why_parameters.py, W8; history: Rivero and Gsponer, arXiv:hep-ph/0505220).
    Evaluated for leptons and quarks. (EMPIRICAL: a regularity, not derived here)

numpy + scipy. About 10 s.
"""
import os
import sys
from fractions import Fraction as F
from itertools import combinations, combinations_with_replacement
from math import exp, log, pi, sqrt

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq, least_squares, minimize

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import m331_standalone as E
import ladder_links as LL
import why_parameters as W

M_PROTON = 0.93827208816                 # GeV, PDG 2024 (AUDIT.md)
TAU_P_LIMIT = 2.4e34                     # yr, p -> e+ pi0, Super-Kamiokande, arXiv:2010.16098
YEAR_S = 3.156e7
VARIANT = "-1/sqrt3"


def banner(s):
    print("\n" + "=" * 96 + "\n" + s + "\n" + "=" * 96)


# =========================================================================================
# Gauge sector
# =========================================================================================
TWIST = (0, 0, 0, 1, 1, 1)               # Z_3 charges of P on the fundamental of SU(6)


def surviving_generators(p=TWIST):
    """Number of SU(6) generators commuting with the twist: E_ab survives if p_a = p_b mod 3."""
    return sum(1 for a in range(6) for b in range(6) if a != b and (p[a] - p[b]) % 3 == 0) + 5


def all_twists():
    """Every Z_3 twist of SU(6) up to ordering, with the number of surviving generators."""
    out = {}
    for n0 in range(7):
        for n1 in range(7 - n0):
            n2 = 6 - n0 - n1
            if (n1 + 2 * n2) % 3:                                   # det P = 1
                continue
            key = tuple(sorted((n0, n1, n2), reverse=True))
            out[key] = sum(n * n for n in key) - 1
    return out


X_FUND = [F(-1, 3)] * 3 + [F(1, 3)] * 3      # X on the 6: colour indices, then SU(3)_L indices
_REP = {0: 1, 1: 3, 2: -3, 3: 1}             # antisymmetric power of a 3: 1, 3, 3bar, 1


def fragments(name):
    """3-3-1 content of an SU(6) representation: {(colour, L, X): 1}; 3bar is written -3."""
    out = {}
    if name in ("6", "6bar", "15", "20"):
        k = {"6": 1, "6bar": 1, "15": 2, "20": 3}[name]
        for idx in combinations(range(6), k):
            nc = sum(1 for i in idx if i < 3)
            key = (_REP[nc], _REP[k - nc], sum(X_FUND[i] for i in idx))
            out[key] = 1
        if name == "6bar":
            out = {(-c if abs(c) == 3 else c, -l if abs(l) == 3 else l, -x): 1 for c, l, x in out}
    elif name == "21":                       # symmetric square
        out = {(6, 1, F(-2, 3)): 1, (1, 6, F(2, 3)): 1, (3, 3, F(0)): 1}
    elif name == "35":                       # adjoint
        out = {(8, 1, F(0)): 1, (1, 8, F(0)): 1, (1, 1, F(0)): 1, (3, -3, F(-2, 3)): 1, (-3, 3, F(2, 3)): 1}
    return out


def dimension(frags):
    return sum(abs(c) * abs(l) for c, l, _ in frags)


def embedding():
    """Each left-handed fermion of the beta = -1/sqrt3 model, and the SU(6) representation holding it.
    The model lists (multiplicity, (None, dim_L, dim_colour), X) without the triplet/antitriplet sign,
    so the match is on dimensions and X."""
    gs, ferm, scal, _ = E.model(3, VARIANT)
    have = {}
    for rep in ("6bar", "15", "20"):
        for c, l, x in fragments(rep):
            have.setdefault((abs(l), abs(c), x), rep)
    return [(mult, dims[1], dims[2], q, have.get((dims[1], dims[2], q))) for mult, dims, q in ferm]


def sin2_at_orbifold():
    """g_X^2/g^2 and sin^2 theta_W where SU(6) is restored. X = c T_X with T_X the canonically
    normalised generator diag(1,1,1,-1,-1,-1)/sqrt12; 1/g_Y^2 = beta^2/g^2 + 1/g_X^2, beta^2 = 1/3."""
    c2 = sum(x * x for x in X_FUND) / F(1, 2)
    gx2 = 1 / c2
    inv_gy2 = F(1, 3) + 1 / gx2
    return gx2, (1 / inv_gy2) / (1 + 1 / inv_gy2)


class Group(E.Group):
    """src/m331_standalone.Group with the sextet and octet of SU(3) added."""

    def T(self, d):
        if self.N == 3 and d == 8:
            return F(3)
        return super().T(d)

    def C2(self, d, charge=None):
        if self.N == 3 and d == 8:
            return F(3)
        if self.N == 3 and d == 6:
            return F(10, 3)
        return super().C2(d, charge)


GROUPS = [Group("X"), Group("SU3L", 3), Group("SU3c", 3)]

# extra multiplets: (label, kind, dim_L, dim_colour, X). kind: "complex" scalar, "real" scalar,
# "weyl" fermion (real representation), "dirac" (a vector-like pair of Weyl fermions).
ORBIFOLD_SCALAR = ("scalar (3,3bar) X=2/3 from the gauge field", "complex", 3, 3, F(2, 3))


def candidates():
    seen, out = set(), []
    for rep in ("6", "15", "20", "21", "35"):
        for c, l, x in fragments(rep):
            key = (abs(l), abs(c), abs(x))
            if key in seen or (abs(c) == 1 and abs(l) == 1):
                continue
            seen.add(key)
            tag = f"({abs(c)},{abs(l)}) X={abs(x)}"
            if x == 0 and abs(c) * abs(l) == 8:
                out += [(f"Weyl fermion {tag}", "weyl", abs(l), abs(c), abs(x)),
                        (f"real scalar {tag}", "real", abs(l), abs(c), abs(x))]
            else:
                out += [(f"vector-like fermion {tag}", "dirac", abs(l), abs(c), abs(x)),
                        (f"scalar {tag}", "complex", abs(l), abs(c), abs(x))]
    return out


_COEFF = {}


def coeffs(extra=()):
    """Exact one- and two-loop gauge coefficients (order X, SU(3)_L, colour), in the convention
    of src/m331_standalone.coefficients, for the minimal model plus extra multiplets."""
    key = tuple(sorted(e[0] for e in extra))
    if key not in _COEFF:
        _, ferm, scal, _ = E.model(3, VARIANT)
        ferm, scal = list(ferm), list(scal)
        for _, kind, dl, dc, x in extra:
            dims = (None, dl, dc)
            if kind == "weyl":
                ferm.append((1, dims, x))
            elif kind == "dirac":
                ferm += [(1, dims, x), (1, dims, -x)]
            elif kind == "complex":
                scal.append((1, dims, x))
            else:
                scal.append((F(1, 2), dims, x))
        a, b = E.coefficients(GROUPS, ferm, scal)
        _COEFF[key] = (np.array([float(v) for v in a]), np.array([[float(v) for v in r] for r in b]))
    return _COEFF[key]


NORM = np.array([0.75, 1.0, 1.0])            # (3/4)/alpha_X, 1/alpha_L, 1/alpha_3 are equal in SU(6)


def run(ainv0, mu0, mu1, extra=(), loops=2):
    """Inverse couplings (X, L, 3) from mu0 to mu1. d(1/alpha_i)/dln mu = -a_i/2pi - b_ij alpha_j/8pi^2."""
    a, b = coeffs(extra)
    if loops == 1:
        return np.array(ainv0) - a * log(mu1 / mu0) / (2 * pi)
    f = lambda t, y: -a / (2 * pi) - (b @ (1 / y)) / (8 * pi**2)
    sol = solve_ivp(f, (0.0, log(mu1 / mu0)), np.array(ainv0, float), rtol=1e-9, atol=1e-11)
    return sol.y[:, -1]


def run_staged(ainv0, mu0, mu1, extra=(), staged=(), loops=2):
    """run(), with further multiplets entering at their own masses: staged = ((field, mass), ...)."""
    y, mu, active = np.array(ainv0, float), mu0, list(extra)
    for field, mass in sorted(staged, key=lambda t: t[1]):
        if mass >= mu1:
            break
        if mass > mu:
            y, mu = run(y, mu, mass, tuple(active), loops), mass
        active.append(field)
    return run(y, mu, mu1, tuple(active), loops)


def unify(extra=(), mu331=E.MU331, loops=2, staged=()):
    """Use the two electroweak couplings to fix the orbifold scale, then predict the strong one.
    Returns dict(Mc, ainv_U, a3_pred (1/alpha_3 at mu331), alpha_s_MZ, tau_p in years) or None when
    the electroweak couplings do not meet below the Planck mass or a coupling blows up first.
    staged: multiplets that enter above mu331, as ((field, mass), ...)."""
    aX, aL, a3m = E.boundary(mu331)

    def gap(lnr, a3):
        y = run_staged([aX, aL, a3], mu331, mu331 * exp(lnr), extra, staged, loops)
        return (y * NORM)[0] - y[1], y

    def meet(a3):
        top = log(E.M_PLANCK / mu331)
        try:
            if gap(top, a3)[0] > 0:
                return None
            lnr = brentq(lambda s: gap(s, a3)[0], 0.0, top, xtol=1e-10)
        except (ValueError, FloatingPointError):
            return None
        return lnr, gap(lnr, a3)[1]

    def miss(a3):
        m = meet(a3)
        return None if m is None else m[1][2] - m[1][1]

    grid = np.linspace(2.0, 90.0, 23)
    vals = [miss(g) for g in grid]
    a3p = None
    for g0, g1, v0, v1 in zip(grid, grid[1:], vals, vals[1:]):
        if v0 is not None and v1 is not None and v0 * v1 <= 0:
            a3p = brentq(miss, g0, g1, xtol=1e-9)
            break
    if a3p is None:
        return None
    lnr, y = meet(a3p)
    Mc, aU = mu331 * exp(lnr), y[1]
    if not np.all(np.isfinite(y)) or aU <= 1:
        return None
    alpha_s = 1 / (1 / E.ALPHA_S_MZ + (a3p - a3m))
    tau = Mc**4 * aU**2 / M_PROTON**5 * LL.HBAR_GEV_S / YEAR_S
    return dict(Mc=Mc, ainv_U=aU, a3_pred=a3p, a3_meas=a3m, alpha_s_MZ=alpha_s, tau_p=tau)


ALPHA_S_TOL = 0.003                      # |alpha_s(M_Z) - measured| counted as a fit (thresholds are unknown)


def completion_search(max_fields=4, tol=3.0, mu331=E.MU331):
    """One-loop screen over sets of up to max_fields extra multiplets.
    Kept: the three couplings meet within tol in 1/alpha_3, and the estimated proton lifetime passes."""
    cand = candidates()
    a0, _ = coeffs(())
    da = [coeffs((c,))[0] - a0 for c in cand]
    aX, aL, a3 = E.boundary(mu331)
    start = np.array([aX, aL, a3]) * NORM
    found = []
    for k in range(1, max_fields + 1):
        for combo in combinations_with_replacement(range(len(cand)), k):
            a = a0 + sum(da[i] for i in combo)
            slope = -a * NORM / (2 * pi)                      # per unit ln mu, normalised
            if slope[0] >= slope[1]:
                continue
            lnr = (start[0] - start[1]) / (slope[1] - slope[0])
            if not 0 < lnr < log(E.M_PLANCK / mu331):
                continue
            aU = start[1] + slope[1] * lnr
            d3 = (start[2] + slope[2] * lnr) - aU
            Mc = mu331 * exp(lnr)
            if aU <= 1 or abs(d3) > tol:
                continue
            tau = Mc**4 * aU**2 / M_PROTON**5 * LL.HBAR_GEV_S / YEAR_S
            if tau < TAU_P_LIMIT:
                continue
            found.append((k, abs(d3), combo))
    found.sort()
    return cand, found


def completions(max_fields=4):
    """The screened sets run at two loops, ordered by the distance of the predicted alpha_s(M_Z)
    from the measured one. Returns (candidates, number screened, [(extra, one-loop, two-loop)])."""
    cand, found = completion_search(max_fields)
    out = []
    for k, d3, combo in found:
        extra = tuple(cand[i] for i in combo)
        u1, u2 = unify(extra, loops=1), unify(extra, loops=2)
        if u1 is None or u2 is None or u2["tau_p"] < TAU_P_LIMIT:
            continue
        out.append((extra, u1, u2))
    out.sort(key=lambda t: (abs(t[2]["alpha_s_MZ"] - E.ALPHA_S_MZ), len(t[0])))
    return cand, len(found), out


def best_completion_with_one_mass():
    """The smallest set that brackets the measured alpha_s: one real colour-octet scalar at mu_331
    and three SU(3)_L-octet Weyl fermions at a common mass M_8, which is then fixed by alpha_s(M_Z).
    One input fitted to one number; M_c and the proton lifetime follow."""
    cand = {c[0]: c for c in candidates()}
    scalar, octet = cand["real scalar (8,1) X=0"], cand["Weyl fermion (1,8) X=0"]
    u = lambda m8: unify((scalar,), loops=2, staged=((octet, m8),) * 3)
    f = lambda lm: u(exp(lm))["alpha_s_MZ"] - E.ALPHA_S_MZ
    lo, hi = log(E.MU331), log(1e3 * E.MU331)
    if f(lo) * f(hi) > 0:
        return None
    m8 = exp(brentq(f, lo, hi, xtol=1e-8))
    return m8, u(m8)


# =========================================================================================
# Flavour sector: the magnetised triangle
# =========================================================================================
TAU = np.exp(2j * np.pi / 3)
OM = TAU
AREA = TAU.imag
CORNERS = (0j, (2 + TAU) / 3, 2 * (2 + TAU) / 3)
N_GRID = 96
_x = (np.arange(N_GRID) + 0.5) / N_GRID
_X, _Y = np.meshgrid(_x, _x, indexing="ij")
Z = _X + TAU * _Y
DA = AREA / N_GRID**2


def psi_raw(j, M, z):
    """Unnormalised zero mode j of flux M at the points z."""
    z = np.asarray(z, complex)
    out = np.zeros(z.shape, complex)
    for l in range(-8, 9):
        a = j / M + l
        out += np.exp(1j * np.pi * a * a * M * TAU + 2j * np.pi * a * M * z)
    return np.exp(1j * np.pi * M * z * z.imag / TAU.imag) * out


_FULL, _SECT = {}, {}


def full(M):
    """Normalised modes on the grid, and the matrices of the rotation z -> w z, the corner
    translation z -> z + (2+tau)/3 (with its gauge phase) and the reflection z -> -z."""
    if M not in _FULL:
        P = np.array([psi_raw(j, M, Z) for j in range(M)])
        nrm = np.sqrt((abs(P)**2).sum(axis=(1, 2)) * DA)
        P = P / nrm[:, None, None]
        op = lambda f: np.einsum("iab,jab->ij", P.conj(),
                                 np.array([f(j) for j in range(M)]) / nrm[:, None, None]) * DA
        R = op(lambda j: psi_raw(j, M, OM * Z))
        Pm = op(lambda j: psi_raw(j, M, -Z))
        w = CORNERS[1]
        T = op(lambda j: np.exp(-1j * np.pi * M * (np.conj(w) * Z).imag / TAU.imag) * psi_raw(j, M, Z + w))
        _FULL[M] = dict(grid=P, nrm=nrm, R=R, T=T, P=Pm)
    return _FULL[M]


def sector(M, k):
    """The zero modes of flux M with Z_3 eigenvalue w^k: values on the grid, an evaluator at any
    point, and the translation and reflection restricted to them."""
    if (M, k) not in _SECT:
        f = full(M)
        wv, V = np.linalg.eig(f["R"])
        sel = [i for i in range(M) if abs(wv[i] - OM**k) < 1e-6]
        Q = np.linalg.qr(V[:, sel])[0] if sel else np.zeros((M, 0), complex)
        nrm = f["nrm"]
        at = lambda p: np.array([sum(Q[j, a] * psi_raw(j, M, [p])[0] / nrm[j] for j in range(M))
                                 for a in range(Q.shape[1])])
        _SECT[(M, k)] = dict(grid=np.einsum("ja,jxy->axy", Q, f["grid"]), at=at, n=Q.shape[1],
                             T=Q.conj().T @ f["T"] @ Q, P=Q.conj().T @ f["P"] @ Q)
    return _SECT[(M, k)]


def unitarity_error(M):
    """Largest deviation from unitarity of the rotation and reflection, and of the corner translation
    where it is a symmetry (flux divisible by 3)."""
    f = full(M)
    return max(abs(f[k] @ f[k].conj().T - np.eye(M)).max() for k in (("R", "T", "P") if M % 3 == 0 else ("R", "P")))


def zero_mode_table(fluxes=(2, 4, 6, 8, 10, 12)):
    return {M: tuple(sector(M, k)["n"] for k in range(3)) for M in fluxes}


def corner_charges(M, k):
    """Charges (0, 1 or 2) of the modes under the corner translation: its eigenvalues are w^q."""
    ev = np.linalg.eigvals(sector(M, k)["T"])
    assert np.allclose(abs(ev), 1, atol=1e-8) and np.allclose(ev**3, 1, atol=1e-7)
    return sorted(int(round(np.angle(e) / (2 * np.pi / 3))) % 3 for e in ev)


M_GEN, M_HIGGS = 6, 12                        # flux of the fermions and of the Higgs (6 + 6)
_Y = {}


def yukawa_tensor():
    """Y[a,b,c] = Int L_a R_b conj(H_c): three invariant modes of flux 6 twice, five of flux 12."""
    if "Y" not in _Y:
        L, H = sector(M_GEN, 0)["grid"], sector(M_HIGGS, 0)["grid"]
        _Y["Y"] = np.einsum("axy,bxy,cxy->abc", L, L, H.conj()) * DA
    return _Y["Y"]


def masses(h):
    """Singular values of the Yukawa matrix for the Higgs Phi = sum_c h_c H_c, heaviest = 1."""
    s = np.linalg.svd(yukawa_tensor() @ np.conj(h), compute_uv=False)
    return s / s[0]


def symmetric_higgs():
    """The Higgs direction unchanged by the corner translation; it is unique and reflection-even."""
    S = sector(M_HIGGS, 0)
    ev, V = np.linalg.eig(S["T"])
    sel = [i for i in range(S["n"]) if abs(ev[i] - 1) < 1e-6]
    assert len(sel) == 1
    h = V[:, sel[0]]
    return h / np.linalg.norm(h), float(np.real(np.vdot(h, S["P"] @ h) / np.vdot(h, h)))


def point_higgs(p):
    """The Higgs concentrated at p (the reproducing kernel: h_c = conj(H_c(p)))."""
    return np.conj(sector(M_HIGGS, 0)["at"](p))


def point_higgs_check(p=0.137 + 0.291 * TAU):
    L = sector(M_GEN, 0)["at"](p)
    M = yukawa_tensor() @ np.conj(point_higgs(p))
    return masses(point_higgs(p)), float(abs(M - np.outer(L, L)).max())


def quartic_tensor():
    if "B" not in _Y:
        H = sector(M_HIGGS, 0)["grid"].reshape(5, -1)
        D = np.einsum("ax,bx->abx", H.conj(), H)
        _Y["B"] = AREA * np.einsum("abx,cdx->abcd", D, D) * DA
    return _Y["B"]


def B(h):
    """Area * Int |Phi|^4 / (Int |Phi|^2)^2: 1 for a uniform |Phi|, larger when concentrated."""
    r = np.einsum("a,b->ab", np.conj(h), h)
    return float(np.real(np.einsum("ab,cd,abcd->", r, r, quartic_tensor())) / np.real(np.vdot(h, h))**2)


def abrikosov():
    """The same ratio for one flux quantum on this lattice: the triangular vortex lattice."""
    p = abs(psi_raw(0, 1, Z))**2
    return float(AREA * (p * p).sum() * DA / (p.sum() * DA)**2)


def loop_term(h):
    """sum m_i^4 for a unit Higgs direction: what fermion loops subtract from the quartic."""
    s = np.linalg.svd(yukawa_tensor() @ np.conj(h) / np.linalg.norm(h), compute_uv=False)
    return float((s**4).sum())


_c = lambda p: p[:5] + 1j * p[5:]


def _starts(n, seed):
    rng = np.random.default_rng(seed)
    hk = point_higgs(CORNERS[0])
    return [rng.normal(size=10) for _ in range(n)] + \
           [np.concatenate([hk.real, hk.imag]) + 0.05 * rng.normal(size=10) for _ in range(3)]


def vacuum(xi=0.0, n=10, seed=11):
    """Direction minimising the effective quartic B - xi * loop_term. Returns (h, value)."""
    best = None
    for p0 in _starts(n, seed):
        r = minimize(lambda p: B(_c(p)) - xi * loop_term(_c(p)), p0, method="BFGS", options=dict(gtol=1e-9))
        if best is None or r.fun < best.fun:
            best = r
    h = _c(best.x)
    return h / np.linalg.norm(h), float(best.fun)


def corner_numbers():
    """K = |H(p)|^2 at a corner (= flux/area), g = overlap of two Higgs corner states,
    and the same overlap for the fermions."""
    Hc = np.array([sector(M_HIGGS, 0)["at"](c) for c in CORNERS])
    Lc = np.array([sector(M_GEN, 0)["at"](c) for c in CORNERS])
    GH, GL = Hc @ Hc.conj().T, Lc @ Lc.conj().T
    return dict(K=GH[0, 0].real, g=abs(GH[0, 1]) / GH[0, 0].real, kappa_L=abs(GL[0, 1]) / GL[0, 0].real, Hc=Hc)


def light_higgs(k):
    """Lowest state of the Higgs mass matrix m^2 - sum_i k_i |K_i><K_i| (corner strengths k_i).
    Returns the mass ratios, the left-handed rotation (lightest first) and the heavier eigenvalues."""
    Hc = corner_numbers()["Hc"]
    O = sum(ki * np.outer(Hc[i].conj(), Hc[i]) for i, ki in enumerate(k))
    ev, V = np.linalg.eigh(O)
    U, s, _ = np.linalg.svd(yukawa_tensor() @ np.conj(V[:, -1]))
    return s / s[0], U[:, ::-1], ev[::-1] / ev[-1]


def quark_targets():
    y = W.YUK_MZ
    return np.array([y["c"] / y["t"], y["u"] / y["t"]]), np.array([y["s"] / y["b"], y["d"] / y["b"]])


def fit_corner_strengths(target):
    k = lambda x: [1.0, 1 / (1 + np.exp(x[0])), 1 / (1 + np.exp(x[1]))]
    r = least_squares(lambda x: np.log(light_higgs(k(x))[0][1:] / target), [0.0, 3.0], xtol=1e-14)
    return k(r.x), float(abs(r.fun).max())


def mixing():
    """|V_us|, |V_cb|, |V_tb| once the corner strengths are fitted to the mass ratios."""
    tu, td = quark_targets()
    ku, eu = fit_corner_strengths(tu)
    kd, ed = fit_corner_strengths(td)
    V = abs(light_higgs(ku)[1].conj().T @ light_higgs(kd)[1])
    return dict(ku=ku, kd=kd, resid=max(eu, ed), Vus=V[0, 1], Vcb=V[1, 2], Vtb=V[2, 2])


def triangle_form(m):
    """(r, theta) with sqrt(m_k) = a (1 + r cos(theta + 2 pi k/3)); Koide's relation is r = sqrt2."""
    s = np.sqrt(np.array(m, float))
    z = (s * np.exp(-2j * np.pi * np.arange(3) / 3)).sum() / 3
    th = np.angle(z) % (2 * np.pi / 3)
    return 2 * abs(z) / s.mean(), min(th, 2 * np.pi / 3 - th)


# =========================================================================================
def describe(extra):
    names = {}
    for e in extra:
        names[e[0]] = names.get(e[0], 0) + 1
    return ", ".join(f"{n} x {k}" for k, n in names.items())


def main():
    banner("G1  SU(6) on the triangle: the twist diag(1,1,1,w,w,w) leaves 3-3-1 (CHECK)")
    print(f"   surviving generators: {surviving_generators()} = 8 + 8 + 1")
    for mult, n in sorted(all_twists().items(), key=lambda t: -t[1]):
        print(f"   eigenvalue multiplicities {mult}: {n} generators" + ({(3, 3, 0): "   <- SU(3) x SU(3) x U(1)", (4, 1, 1): "   (SU(4) x U(1)^2)", (2, 2, 2): "   (SU(2)^3 x U(1)^2)", (6, 0, 0): "   (SU(6))"}[mult]))
    print("   SU(6) representation holding each left-handed fermion of the beta = -1/sqrt3 model:")
    for mult, dl, dc, q, rep in embedding():
        print(f"      {mult} x (colour {dc}, SU(3)_L {dl}, X = {str(q):>4s})   in {rep}")
    print("   (LIT: 3-3-1 inside SU(6): Deppisch, Hati, Patra, Sarkar and Valle, arXiv:1608.05334.)")

    banner("G2  The couplings where SU(6) is restored (CHECK)")
    gx2, s2 = sin2_at_orbifold()
    print(f"   g_3 = g_L,  g_X^2/g^2 = {gx2},  sin^2 theta_W = {s2}")

    banner("G3  Minimal 3-3-1 content: the strong coupling predicted from the electroweak pair (FAILS)")
    aX, aL, a3 = E.boundary(E.MU331)
    print(f"   at mu_331 = {E.MU331:.0f} GeV: (3/4)/alpha_X = {0.75 * aX:.2f}, 1/alpha_L = {aL:.2f}, 1/alpha_3 = {a3:.2f}")
    for label, extra in (("minimal content", ()), ("plus the orbifold's own scalar", (ORBIFOLD_SCALAR,))):
        for loops in (1, 2):
            u = unify(extra, loops=loops)
            print(f"   {label:31s} {loops} loop: M_c = {u['Mc']:.2e} GeV, 1/alpha_U = {u['ainv_U']:.1f}, "
                  f"alpha_s(M_Z) = {u['alpha_s_MZ']:.4f} (measured {E.ALPHA_S_MZ})")
    for mu in (1e5, 1e8, 1e11):
        u = unify((), mu331=mu, loops=2)
        print(f"   minimal content, mu_331 = {mu:.0e} GeV, 2 loop: M_c = {u['Mc']:.2e} GeV, alpha_s(M_Z) = {u['alpha_s_MZ']:.4f}")

    banner("G4  Extra matter at mu_331 that would make the three couplings meet (FIT)")
    cand, n_screen, sols = completions()
    good = [t for t in sols if abs(t[2]["alpha_s_MZ"] - E.ALPHA_S_MZ) < ALPHA_S_TOL]
    print(f"   {len(cand)} candidate multiplets from the SU(6) representations 6, 15, 20, 21, 35; up to 4 at once")
    print(f"   passing the one-loop screen with the proton safe: {n_screen}; surviving at two loops: {len(sols)}; "
          f"within {ALPHA_S_TOL} of the measured alpha_s(M_Z) at two loops: {len(good)}")
    for extra, u1, u2 in sols[:5]:
        print(f"   {describe(extra)}")
        print(f"      alpha_s(M_Z) = {u1['alpha_s_MZ']:.4f} (1 loop), {u2['alpha_s_MZ']:.4f} (2 loop; measured {E.ALPHA_S_MZ}); "
              f"M_c = {u2['Mc']:.1e} GeV, 1/alpha_U = {u2['ainv_U']:.1f}, proton lifetime ~ {u2['tau_p']:.0e} yr")
    b = best_completion_with_one_mass()
    if b:
        m8, u = b
        print("   the first set with the three octet fermions at their own mass M_8, fixed by alpha_s(M_Z) (one input, one number):")
        print(f"      M_8 = {m8:.2e} GeV  ->  M_c = {u['Mc']:.2e} GeV, 1/alpha_U = {u['ainv_U']:.1f}, proton lifetime ~ {u['tau_p']:.0e} yr")
    print(f"   proton-lifetime limit used: {TAU_P_LIMIT:.1e} yr; the estimate M_c^4/(alpha_U^2 m_p^5) is good to an order of magnitude.")
    print("   Two-loop gauge terms only; Yukawa terms and threshold corrections at M_c are not included.")

    banner("T1  Zero modes on the triangle and their Z_3 charges (CHECK)")
    for M, n in zero_mode_table().items():
        print(f"   flux {M:2d}: {n} modes with eigenvalue (1, w, w^2);  rotation, translation, reflection unitary to {unitarity_error(M):.0e}")
    print(f"   three generations = the invariant modes of flux {M_GEN}; corner-translation charges {corner_charges(M_GEN, 0)}")
    print(f"   Higgs = the {sector(M_HIGGS, 0)['n']} invariant modes of flux {M_HIGGS}; charges {corner_charges(M_HIGGS, 0)}")

    banner("T2  The fully symmetric Higgs (FAILS)")
    h0, par = symmetric_higgs()
    tu, td = quark_targets()
    print(f"   unique invariant direction, reflection eigenvalue {par:+.0f}: masses 1 : {masses(h0)[1]:.4f} : {masses(h0)[2]:.4f}"
          f"   (2^(-1/3) = {2 ** (-1 / 3):.4f})")
    print(f"   measured (Yukawas at M_Z): up 1 : {tu[0]:.2e} : {tu[1]:.2e};  down 1 : {td[0]:.2e} : {td[1]:.2e}")

    banner("T3  A Higgs concentrated at a point gives one massive generation (CHECK)")
    s, err = point_higgs_check()
    print(f"   at a generic point: masses 1 : {s[1]:.1e} : {s[2]:.1e};  |Y - L(p) L(p)^T| = {err:.0e}")

    banner("T4  The Higgs potential on the triangle (FAILS)")
    hv, bmin = vacuum(0.0)
    hk = point_higgs(CORNERS[0])
    print(f"   quartic alone: minimum B = {bmin:.4f} (one vortex per cell on this lattice: {abrikosov():.4f}); "
          f"masses 1 : {masses(hv)[1]:.3f} : {masses(hv)[2]:.0e}")
    print(f"   corner-concentrated Higgs: B = {B(hk):.4f}, sum m^4 = {loop_term(hk):.3f}; stable only below xi_c = {B(hk) / loop_term(hk):.4f}")
    xc = B(hk) / loop_term(hk)
    for x in (0.5, 0.9, 0.99):
        h, gmin = vacuum(x * xc)
        print(f"   fermion loops at xi = {x:.2f} xi_c: effective quartic {gmin:+.3f} (corner: {B(hk) - x * xc * loop_term(hk):+.3f}); "
              f"masses 1 : {masses(h)[1]:.3f} : {masses(h)[2]:.3f}" + ("   <- unbounded below" if gmin < 0 else ""))

    banner("T5  A light Higgs from unequal corners (MODEL; strengths are a FIT; mixing FAILS)")
    cn = corner_numbers()
    print(f"   Higgs at a corner: |H|^2 = {cn['K']:.4f} (flux/area = {M_HIGGS / AREA:.4f});  overlap of two corner states g = {cn['g']:.5f}")
    print(f"   fermion corner states: overlap = {cn['kappa_L']:.5f}")
    for k in ([1, 1, 1], [1, 0.9, 0.5], [1, 0.5, 0.25]):
        s, _, ev = light_higgs(k)
        print(f"   corner strengths {k}: masses 1 : {s[1]:.2e} : {s[2]:.2e};  next Higgs modes at {ev[1]:.3f}, {ev[2]:.3f} of the lightest")
    m = mixing()
    print(f"   fitted to the mass ratios (residual {m['resid']:.0e}): up {np.round(m['ku'], 5).tolist()}, down {np.round(m['kd'], 5).tolist()}")
    print(f"   predicted |V_us| = {m['Vus']:.4f} (measured {W.V_US}), |V_cb| = {m['Vcb']:.4f} (measured {W.V_CB}), |V_tb| = {m['Vtb']:.5f} ({W.V_TB})")

    banner("T6  The triangle form sqrt(m_k) = a (1 + r cos(theta + 2 pi k/3)) (EMPIRICAL)")
    y = W.YUK_MZ
    for name, ms in (("charged leptons (pole masses)", (LL.M_EL, LL.M_MU, LL.M_TAU)),
                     ("up quarks (Yukawas at M_Z)", (y["u"], y["c"], y["t"])),
                     ("down quarks (Yukawas at M_Z)", (y["d"], y["s"], y["b"]))):
        r, th = triangle_form(ms)
        print(f"   {name:30s} r/sqrt2 = {r / sqrt(2):.5f},  theta = {th:.5f}")
    print(f"   Koide's ratio for the leptons (src/why_parameters.py): {W.koide()[0]:.6f} (2/3 = 0.666667); 2/9 = {2 / 9:.5f}")

    banner("Summary")
    print("   Follows from the geometry: the 3-3-1 gauge group and charges; three generations; one heavy generation")
    print("   when the Higgs sits at a corner; a mixing matrix close to the identity.")
    print("   Fails: unification with minimal content; any symmetric Higgs potential (no hierarchy); the size of the mixing.")
    print("   Fitted, not predicted: the extra matter for unification; the corner strengths. None of the 19 is derived.")


if __name__ == "__main__":
    main()
