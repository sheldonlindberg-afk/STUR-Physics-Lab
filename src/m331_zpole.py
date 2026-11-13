#!/usr/bin/env python3
"""
The Z-pole observables and the 3-3-1 scale: the full tree-level electroweak-precision test of
Z-Z' mixing, validated on the E6 Z' bosons, against the LHC Z' search.

src/m331_rho_bound.py used rho alone. Z-Z' mixing also changes the Z's couplings to every
fermion, at the same order (v/w)^2. This module fits both effects to the LEP/SLD Z-pole data.

Inputs (LIT; results/m331/zpole/zpole_inputs.json, each number with its table):
  measured: LEP/SLD, Phys. Rept. 427 (2006) 257, arXiv:hep-ex/0509008 (Table 2.13, the
  lineshape with lepton universality; Tables 5.10-5.11, heavy flavour), plus A_l (LEP, SLD)
  and sin^2 theta_eff (Q_FB, Tevatron) as in Gfitter; correlations as published.
  SM predictions: Gfitter, Eur. Phys. J. C 78 (2018) 675, arXiv:1803.01853, Table 1 (full
  fit), with their parametric errors added in quadrature. 14 observables; M_Z is an input,
  M_W is not used (src/m331_rho_bound.py treats rho with the global fit).

Method (MODEL: tree level, linear around the SM). With alpha, G_F and M_Z fixed, a Z-Z' mixing
angle theta and a shift rho = M_W^2 / (c^2 M_Z^2) change the Z couplings to
    G_f = (1 + drho/2) (T3 - (s^2 + ds^2) Q) + theta g'_f,    ds^2 = -s^2 c^2 / (c^2 - s^2) drho,
with g'_f the Z' coupling in units of g/c_W (src/m331_zprime_recast.py, the same functions the
LHC recast uses) and s^2 = 0.23153. Each observable is computed at tree level (QCD factor
1 + alpha_s/pi on quarks) with and without new physics, and the difference is added to
Gfitter's SM value.

Z1  The fit's SM baseline: chi^2_SM = 14.2 for 14 observables; A0,b_FB (pull -2.3) gives
    4.6 of it, SLD's A_l (+2.0) another 4.0. (CHECK)
Z2  Validation on the E6 Z'_chi and Z'_psi (Erler, Langacker, Munir and Rojas, JHEP 08 (2009)
    017, arXiv:0906.2435, Tables 4-5: 95% CL ranges of sin theta_ZZ'):
        Z'_chi, rho_0 = 1 (drho >= 0, M_Z' free):  here [-0.0015, +0.0008],  theirs [-0.0016, +0.0006]
        Z'_psi, rho_0 = 1:                         here [-0.0022, +0.0008],  theirs [-0.0018, +0.0009]
        Z'_psi, rho_0 free:                        here [-0.0022, +0.0008],  theirs [-0.0018, +0.0010]
    The asymmetry is reproduced in both models; every edge is within 0.0004 of theirs and
    the widths within 12%. Their fit has more data (more Z-pole observables, M_W, low-energy
    measurements) and floats M_H and alpha_s; fixing rho does not close the Z'_psi gap, so it
    is the data set, not rho. Since theta goes as 1/w^2 here, 12% in theta is about 6% in w.
    (CHECK; LIT)
Z3  3-3-1 mixing from rung 1's mass matrix (src/m331_breaking.py), exactly diagonalized:
        theta = (v/w)(sin^2 a0 - sin^2 a) M_Z/M_Z',   rho - 1 = (v/w)^2 (sin^2 a - sin^2 a0)^2,
    agreeing with the exact eigenvectors to < 0.5%, sign included, at v/w = 0.04. The Z'
    direction reproduces g331 of the LHC recast exactly. The same sin^2 a0 cancels both:
    at a = a0 the Z is the SM Z at this order. (CHECK)
Z4  The bound on w. Delta chi^2 = 3.84 against the best fit in w, at every a, for the odd
    quark generation (the one in the SU(3)_L triplet) being the first, second or third, with
    and without A0,b_FB. Worst case over a and generations:
        with A0,b_FB:     beta = +1/sqrt3: w > 7.5 TeV      beta = -1/sqrt3: w > 7.6 TeV
        without A0,b_FB:  w > 6.0 TeV and 6.4 TeV
    The odd generation moves it by at most 0.3 TeV. The LHC Z' recast gives w > 11.9 and
    10.3 TeV for every a (src/m331_rho_bound.py R3). So the Z pole is stronger than rho
    alone (5.8 TeV at best) but still below the LHC: by 1.6x (beta = +1/sqrt3) and 1.4x
    (-1/sqrt3) in w with A0,b_FB, 2.0x and 1.6x without. Near a = a0 both effects vanish
    together and the Z pole gives almost nothing. (CHECK; MODEL)
    No significant preference for mixing: the best 3-3-1 point improves chi^2 by 0.5
    (+1/sqrt3) and 1.0 (-1/sqrt3), or 2.9 and 2.1 without A0,b_FB (at w ~ 5-6 TeV, driven by
    SLD's A_l), for two extra parameters. (CHECK)
Z5  What is left out (FOLLOWS). Tree level only: loop contributions to T (the scalars, see
    src/m331_rho_bound.py R5) are not included. Correlated SM parametric errors are treated as
    independent. The Z' exchange itself is out of phase with the resonant Z and negligible at
    the pole. Low-energy parity violation and flavour-changing Z' couplings are separate tests
    and not used.
Labels: CHECK, MODEL, LIT, FOLLOWS.
"""
import json
import math
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import m331_breaking as B
import m331_rho_bound as R
import m331_zprime_recast as ZR

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = json.load(open(os.path.join(HERE, "..", "results", "m331", "zpole", "zpole_inputs.json")))
OBS = DATA["observables"]
NAMES = list(OBS)
S2 = 0.23153                       # sin^2 theta_eff (Gfitter): the base of the tree-level couplings
AS = DATA["alpha_s"]
DCHI = 3.84                        # 95% CL, one parameter
VARIANTS = ("+1/sqrt3", "-1/sqrt3")
GENS = (0, 1, 2)                   # the odd quark generation: 0 = first, 1 = second, 2 = third
LEPTON_FLAV = ("e", "mu", "tau")
UP, DOWN = ("u", "c", "t"), ("d", "s", "b")


def banner(s):
    print("\n" + "=" * 78 + "\n" + s + "\n" + "=" * 78)


# --------------------------------------------------------------------------- data, chi^2
def covariance(names=NAMES):
    idx = {n: i for i, n in enumerate(names)}
    C = np.zeros((len(names), len(names)))
    for i, n in enumerate(names):
        C[i, i] = OBS[n]["meas"][1] ** 2 + OBS[n]["sm"][1] ** 2
    for block in DATA["correlations"].values():
        o, m = block["order"], block["matrix"]
        for a in range(len(o)):
            for b in range(len(o)):
                if a != b and o[a] in idx and o[b] in idx:
                    C[idx[o[a]], idx[o[b]]] = m[a][b] * OBS[o[a]]["meas"][1] * OBS[o[b]]["meas"][1]
    return C


_CINV = {}


def chi2(shifts, names=NAMES):
    """shifts: {name: prediction - SM}."""
    key = tuple(names)
    if key not in _CINV:
        _CINV[key] = np.linalg.inv(covariance(names))
    d = np.array([OBS[n]["meas"][0] - OBS[n]["sm"][0] - shifts.get(n, 0.0) for n in names])
    return float(d @ _CINV[key] @ d)


def names_without(*drop):
    return [n for n in NAMES if n not in drop]


# --------------------------------------------------------------------------- tree level
def sm_fields():
    """(flavour, colours, T3_L, Q) for the Z-pole final states; generation index per flavour."""
    out = []
    for gi in range(3):
        out.append(("nu" + str(gi), 1, 0.5, 0.0, gi, "nuL"))
        out.append((LEPTON_FLAV[gi], 1, -0.5, -1.0, gi, "e"))
        if gi < 2:
            out.append((UP[gi], 3, 0.5, 2 / 3, gi, "u"))
        out.append((DOWN[gi], 3, -0.5, -1 / 3, gi, "d"))
    return out


def couplings(theta=0.0, drho=0.0, zp=None):
    """{flavour: (Nc, G_L, G_R)}; zp(kind, gen, chir) -> Z' coupling in units of g/c_W."""
    ds2 = -S2 * (1 - S2) / (1 - 2 * S2) * drho
    s2 = S2 + ds2
    norm = 1 + drho / 2
    out = {}
    for fl, nc, T3, Q, gi, kind in sm_fields():
        GL = norm * (T3 - s2 * Q)
        GR = norm * (-s2 * Q)
        if zp is not None and theta:
            GL += theta * zp(kind, gi, "L")
            GR += theta * zp(kind, gi, "R") if kind != "nuL" else 0.0
        if kind == "nuL":
            GR = 0.0
        out[fl] = (nc, GL, GR)
    return out


def observables(c):
    """Tree-level Z-pole pseudo-observables from the couplings (massless fermions)."""
    qcd = 1 + AS / math.pi
    G = {fl: nc * (gl**2 + gr**2) * (qcd if nc == 3 else 1.0) for fl, (nc, gl, gr) in c.items()}
    A = {fl: (gl**2 - gr**2) / (gl**2 + gr**2) for fl, (nc, gl, gr) in c.items()}
    k = B.G_F * B.MZ_MEAS**3 / (3 * math.sqrt(2) * math.pi)            # G_F M_Z^3 / (3 sqrt2 pi)
    had = G["u"] + G["c"] + G["d"] + G["s"] + G["b"]
    lep = G["e"]
    tot = had + G["e"] + G["mu"] + G["tau"] + G["nu0"] + G["nu1"] + G["nu2"]
    gev_to_nb = 0.3893794e6
    s2l = 0.25 * (1 - (c["e"][1] + c["e"][2]) / (c["e"][1] - c["e"][2]))
    return {
        "GammaZ": k * tot,
        "sigma_had": 12 * math.pi * G["e"] * had / (B.MZ_MEAS**2 * tot**2) * gev_to_nb,
        "R_l": had / lep,
        "AFB_l": 0.75 * A["e"] ** 2,
        "A_l_LEP": A["e"], "A_l_SLD": A["e"],
        "s2eff_QFB": s2l, "s2eff_Tevt": s2l,
        "R_b": G["b"] / had, "R_c": G["c"] / had,
        "AFB_b": 0.75 * A["e"] * A["b"], "AFB_c": 0.75 * A["e"] * A["c"],
        "A_b": A["b"], "A_c": A["c"],
    }


REL = ("GammaZ", "sigma_had", "R_l", "R_b", "R_c")      # shifted multiplicatively


def shifts(theta=0.0, drho=0.0, zp=None):
    o0, o1 = observables(couplings()), observables(couplings(theta, drho, zp))
    return {n: (OBS[n]["sm"][0] * (o1[n] / o0[n] - 1) if n in REL else o1[n] - o0[n]) for n in NAMES}


# --------------------------------------------------------------------------- Z2: E6
def zp_e6(model):
    field = {("nuL", "L"): "nuL", ("e", "L"): "eL", ("e", "R"): "eR",
             ("u", "L"): "uL", ("u", "R"): "uR", ("d", "L"): "dL", ("d", "R"): "dR"}
    return lambda kind, gi, ch: ZR.gE6(model, field[(kind, ch)], S2)


def chi2_e6(theta, model, rho_mode, names=NAMES):
    """rho_mode: 'one' (rho_0 = 1, M_Z' free: drho = theta^2 (M_Z'^2/M_Z^2 - 1) >= 0, profiled),
    'free' (drho profiled freely)."""
    zp = zp_e6(model)
    grid = np.linspace(0, 3e-3, 61) if rho_mode == "one" else np.linspace(-1.5e-3, 3e-3, 91)
    vals = [chi2(shifts(theta, d, zp), names) for d in grid]
    i = int(np.argmin(vals))
    lo, hi = grid[max(i - 1, 0)], grid[min(i + 1, len(grid) - 1)]
    for _ in range(40):                                 # golden refinement of the profile
        m1, m2 = lo + 0.382 * (hi - lo), lo + 0.618 * (hi - lo)
        if chi2(shifts(theta, m1, zp), names) < chi2(shifts(theta, m2, zp), names):
            hi = m2
        else:
            lo = m1
    return chi2(shifts(theta, 0.5 * (lo + hi), zp), names)


def interval(f, lo=-6e-3, hi=6e-3, n=241):
    """95% CL range (low, high) of a one-parameter profile chi^2 f(x)."""
    xs = np.linspace(lo, hi, n)
    ys = np.array([f(x) for x in xs])
    cut = ys.min() + DCHI
    inside = np.where(ys <= cut)[0]
    i0, i1 = inside[0], inside[-1]

    def edge(out, inn):                 # bisect between a point outside and one inside
        for _ in range(40):
            m = 0.5 * (out + inn)
            out, inn = (out, m) if f(m) <= cut else (m, inn)
        return 0.5 * (out + inn)
    return edge(xs[i0 - 1], xs[i0]), edge(xs[i1 + 1], xs[i1])


def e6_ranges():
    out = {}
    for model, mode in (("chi", "one"), ("psi", "one"), ("psi", "free")):
        f = lambda t, m=model, r=mode: chi2_e6(t, m, r)
        out[(model, mode)] = interval(f)
    return out


# --------------------------------------------------------------------------- Z3: 3-3-1 mixing
def lagrangian_couplings(variant, s2=S2):
    beta = float(B.beta_value(variant))
    e = math.sqrt(4 * math.pi / 127.95)
    g, gY = e / math.sqrt(s2), e / math.sqrt(1 - s2)
    gX = 1 / math.sqrt(1 / gY**2 - beta**2 / g**2)
    return beta, g, gY, gX


def exact_mixing(variant, w, a, v=None):
    """theta, rho - 1 and M_Z1, M_Z2 from the exact (W3, W8, B) mass matrix of rung 1."""
    v = R.v_ew() if v is None else v
    beta, g, gY, gX = lagrangian_couplings(variant)
    M = B.mass_matrix(variant)
    num = np.array(M.subs({B.g: g, B.gX: gX, B.w: w, B.v1: v * math.cos(a), B.v2: v * math.sin(a)}).evalf(),
                   float)[np.ix_([2, 7, 8], [2, 7, 8])]
    ev, U = np.linalg.eigh(num)
    nY = np.array([0, beta / g, 1 / gX]); nY /= np.linalg.norm(nY)
    nZ0 = np.array([math.sqrt(1 - S2), 0, 0]) - math.sqrt(S2) * nY
    nZp = np.array([0, 1 / gX, -beta / g]); nZp /= np.linalg.norm(nZp)
    u = U[:, 1] * np.sign(U[:, 1] @ nZ0)
    MW2 = g**2 * v**2 / 4
    return float(u @ nZp), MW2 / ((1 - S2) * ev[1]) - 1, math.sqrt(ev[1]), math.sqrt(ev[2]), (g, gX, nZp)


def mixing(variant, w, sin2a):
    """Leading order in v/w: theta and rho - 1 (Z3)."""
    v = R.v_ew()
    beta, g, gY, gX = lagrangian_couplings(variant)
    s0 = float(R.sin2_a0_symbolic(variant, gX**2 / g**2))
    mzp = math.sqrt((g**2 + beta**2 * gX**2) / 3) * w
    return (v / w) * (s0 - sin2a) * B.MZ_MEAS / mzp, (v / w) ** 2 * (sin2a - s0) ** 2


def zp_331(variant, odd_gen):
    beta = float(B.beta_value(variant))
    Y = {("nuL", "L"): -0.5, ("e", "L"): -0.5, ("e", "R"): -1.0,
         ("u", "L"): 1 / 6, ("u", "R"): 2 / 3, ("d", "L"): 1 / 6, ("d", "R"): -1 / 3}

    def f(kind, gi, ch):
        if ch == "R":
            rep = None
        elif kind in ("nuL", "e"):
            rep = "3"
        else:
            rep = "3" if gi == odd_gen else "3b"
        return ZR.g331(ZR.t8(rep), Y[(kind, ch)], beta, S2)
    return f


# --------------------------------------------------------------------------- Z4: the bound on w
def chi2_331(variant, w, sin2a, odd_gen, names=NAMES):
    th, dr = mixing(variant, w, sin2a)
    return chi2(shifts(th, dr, zp_331(variant, odd_gen)), names)


def w_bound(variant, sin2a, odd_gen, names=NAMES, w_lo=500.0, w_hi=1e5):
    """Smallest w with chi^2(w) <= min_w chi^2 + 3.84 (chi^2 -> chi^2_SM as w -> infinity)."""
    ws = np.geomspace(w_lo, w_hi, 120)
    ys = np.array([chi2_331(variant, w, sin2a, odd_gen, names) for w in ws])
    best = min(ys.min(), chi2({}, names))
    bad = np.where(ys > best + DCHI)[0]
    if bad.size == 0:
        return 0.0
    i = bad[-1]
    if i == len(ws) - 1:
        return np.inf
    a, b = ws[i], ws[i + 1]
    for _ in range(40):
        m = math.sqrt(a * b)
        a, b = (m, b) if chi2_331(variant, m, sin2a, odd_gen, names) > best + DCHI else (a, m)
    return math.sqrt(a * b)


SIN2A = np.linspace(0.0, 1.0, 41)


def best_fit(variant, names=NAMES):
    """(chi^2_SM - chi^2_min, w, sin^2 a, odd generation) over a grid of the 3-3-1 parameters."""
    best = (np.inf,)
    for s in SIN2A:
        for gen in GENS:
            for w in np.geomspace(500.0, 1e5, 150):
                c = chi2_331(variant, w, s, gen, names)
                if c < best[0]:
                    best = (c, w, s, gen)
    return (chi2({}, names) - best[0],) + best[1:]


def w_bounds(variant, names=NAMES):
    """{odd_gen: [w_bound at each sin^2 a]}."""
    return {gen: [w_bound(variant, s, gen, names) for s in SIN2A] for gen in GENS}


def worst(bounds):
    return max(max(v) for v in bounds.values())


# --------------------------------------------------------------------------- main
def main():
    banner("Z1  SM baseline (LIT: LEP/SLD measurements, Gfitter SM predictions)")
    pulls = {n: (OBS[n]["meas"][0] - OBS[n]["sm"][0]) / math.hypot(OBS[n]["meas"][1], OBS[n]["sm"][1]) for n in NAMES}
    print(f"   chi^2_SM = {chi2({}):.1f} for {len(NAMES)} observables;  without A0,b_FB: "
          f"{chi2({}, names_without('AFB_b')):.1f} for {len(NAMES) - 1}")
    print("   pulls: " + ", ".join(f"{n} {p:+.1f}" for n, p in pulls.items()))

    banner("Z2  Validation: E6 Z'_chi, Z'_psi against Erler et al. 2009 (95% CL, sin theta_ZZ')")
    val = DATA["validation"]
    for (model, mode), (lo, hi) in e6_ranges().items():
        ref = val[f"{model}_rho1" if mode == "one" else f"{model}_rhofree"]
        print(f"   Z'_{model}, rho_0 {'= 1' if mode == 'one' else 'free'}: here [{lo:+.4f}, {hi:+.4f}],"
              f"  theirs [{ref[0]:+.4f}, {ref[1]:+.4f}]")

    banner("Z3  3-3-1 mixing: leading order against exact diagonalization (v/w = 0.04)")
    for v in VARIANTS:
        for a in (0.2, 0.7, 1.3):
            th, dr, *_ = exact_mixing(v, R.v_ew() / 0.04, a)
            th0, dr0 = mixing(v, R.v_ew() / 0.04, math.sin(a) ** 2)
            print(f"   beta = {v}, a = {a}: theta {th:+.4e} (formula {th0:+.4e}),  rho - 1 {dr:.4e} ({dr0:.4e})")

    banner("Z4  Lower bound on w (95% CL) from the Z pole, worst over a; LHC for comparison")
    for v in VARIANTS:
        wl = R.w_from_zprime(v)[0]
        for label, names in (("all", NAMES), ("no A0,b_FB", names_without("AFB_b"))):
            bd = w_bounds(v, names)
            per = ", ".join(f"odd gen {g + 1}: {max(bd[g]) / 1e3:.1f}" for g in GENS)
            print(f"   beta = {v}, {label:10s}: worst {worst(bd) / 1e3:.1f} TeV ({per});  LHC {wl / 1e3:.1f} TeV")
        for label, names in (("all", NAMES), ("no A0,b_FB", names_without("AFB_b"))):
            dc, w, s, gen = best_fit(v, names)
            print(f"      best 3-3-1 point ({label}): chi^2 lower by {dc:.1f} at w = {w / 1e3:.1f} TeV, "
                  f"sin^2 a = {s:.3f}, odd gen {gen + 1}")
        bd = w_bounds(v)
        print(f"      vs sin^2 a (odd gen 3): " + ", ".join(
            f"{s:.2f}: {bd[2][i] / 1e3:.1f}" for i, s in enumerate(SIN2A) if i % 5 == 0) + " TeV")


if __name__ == "__main__":
    main()
