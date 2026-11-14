#!/usr/bin/env python3
"""
The Z3 orbifold engine against the Standard Model's 19 parameters: an audit.

src/z3_orbifold_engine.py is kept exactly as it was proposed. It is an attempt at an
explanation, not a claim: a Casimir-type potential fixes a radius, the radius fixes three
bulk masses, exponentially localised profiles give the quark Yukawa matrices, and a 3-3-1
running selects three colours. This script runs it, goes through the 19 parameters one by
one, and compares every number the engine gives with the measured value. Labels:
    OUTPUT   the engine gives a number that can be compared;
    FIXED    the engine's construction forces a value;
    INPUT    the engine uses the measured value;
    SILENT   the engine says nothing.

Z0  The engine as given, and every hand-chosen number in it (the dials).
Z1  The stabilised radius: exact minimum against the engine's grid minimum.
Z2  What the geometry supplies: the radius cancels from the fermion profiles; the potential
    enters the Yukawas through sqrt(V''(R*)) and 8 R* only.
Z3  CHECK of the engine's SVD against numpy's. The engine divides Y V by singular values of
    order 1e-7 obtained from Y^T Y, and its left rotation is not orthogonal.
Z4  The seven outputs against the measured values (Yukawas at M_Z: Antusch, Hinze and Saad,
    arXiv:2510.01312, eq. (2.4), as in src/why_parameters.py; mixing angles and phase: PDG
    2024 CKM review, eq. (12.28)).
Z5  Sensitivity: decades of change in each output per 10% change of a dial.
Z6  Can the structure align at all? One dial refitted, then all six effective dials.
    (MODEL: the mechanism is that of Arkani-Hamed and Schmaltz, Phys. Rev. D 61, 033005
    (2000), arXiv:hep-ph/9903417: hierarchies from overlaps of localised wave functions.)
Z7  The engine's 3-3-1 section against this repository's exact coefficients
    (src/m331_exact.py).
Z8  The ledger of 19 and the tally.
"""
import contextlib
import io
import math
import os
import sys

import numpy as np
from scipy.optimize import brentq, minimize, minimize_scalar

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import m331_exact as E
import why_parameters as W
import z3_orbifold_engine as Z

FP = np.array([0.0, 2 * np.pi / 3, 4 * np.pi / 3])          # the three fixed points
TWIST = np.array([2.0, 4.0 / 3.0, 2.0 / 3.0])               # the engine's (3 - i)/1.5
PHASES_DOWN = (0.15, 0.03, -0.02)                           # the engine's down-sector offsets

# Measured. Yukawas at M_Z (W.YUK_MZ); PDG 2024 CKM review, eq. (12.28)
S12, S23 = W.S12, W.V_CB                                     # s23 = |V_cb| to 1 part in 1e5
S13, DELTA = 0.003732, 1.147
OUTPUTS = ("y_c/y_t", "y_u/y_t", "y_s/y_b", "y_d/y_b", "sin theta_12", "sin theta_23", "sin theta_13")
MEASURED = np.array([W.YUK_MZ["c"] / W.YUK_MZ["t"], W.YUK_MZ["u"] / W.YUK_MZ["t"],
                     W.YUK_MZ["s"] / W.YUK_MZ["b"], W.YUK_MZ["d"] / W.YUK_MZ["b"], S12, S23, S13])

# Every number in the engine's flavour chain that is chosen by hand: (dial, value, where).
DIALS = [
    ("n_b", "12", "potential: bosonic degrees of freedom"),
    ("n_f", "12", "potential: fermionic degrees of freedom"),
    ("fermion weight", "0.65", "potential: n_b - 0.65 n_f"),
    ("zeta factor", "80/81", "potential: Casimir coefficient"),
    ("flux_c", "0.42", "potential: 1/R^6 term"),
    ("bulk_c", "0.18", "potential: R^2 term"),
    ("twist pattern", "(3 - i)/1.5", "bulk masses: 2, 4/3, 2/3"),
    ("geometric factor", "1.8", "bulk masses: 1.8/R*"),
    ("tilt, up", "1.05", "bulk masses"),
    ("tilt, down", "0.92", "bulk masses"),
    ("Higgs width", "8.0", "Higgs profile exp(-8 R* d)"),
    ("Higgs site", "third fixed point", "Higgs profile"),
    ("phase offset 1", "0.15", "down sector"),
    ("phase offset 2", "0.03", "down sector"),
    ("phase offset 3", "-0.02", "down sector"),
    ("off-diagonal rule", "|cos(phase difference)|", "Yukawa matrix"),
]

# (parameter, label, what the engine says)
LEDGER = [
    ("alpha_s", "SILENT", "section 4 counts colours; it does not give the coupling"),
    ("alpha_QED", "INPUT", "1/125.7 at 4 TeV is typed into section 4"),
    ("alpha_W (sin^2 theta_W)", "INPUT", "0.2504 at 4 TeV is typed into section 4"),
    ("v (electroweak scale)", "SILENT", "R* is a pure number; no unit of mass enters"),
    ("lambda (Higgs mass)", "SILENT", "the Higgs is a fixed profile, with no potential"),
    ("m_t", "SILENT", "each Yukawa matrix is divided by its largest entry"),
    ("m_b", "SILENT", "the same normalisation makes y_b/y_t = 1 by construction"),
    ("m_c", "OUTPUT", "y_c/y_t"),
    ("m_s", "OUTPUT", "y_s/y_b"),
    ("m_d", "OUTPUT", "y_d/y_b"),
    ("m_u", "OUTPUT", "y_u/y_t"),
    ("m_tau", "SILENT", "no lepton sector"),
    ("m_mu", "SILENT", "no lepton sector"),
    ("m_e", "SILENT", "no lepton sector"),
    ("theta_12 (Cabibbo)", "OUTPUT", "from U_up^T U_down"),
    ("theta_23", "OUTPUT", "from U_up^T U_down"),
    ("theta_13", "OUTPUT", "from U_up^T U_down"),
    ("delta_CKM", "FIXED", "both matrices are real, so the phase is 0 or pi and J = 0"),
    ("theta-bar", "SILENT", "real matrices by the |cos| rule; no mechanism"),
]
CLASSES = ("OUTPUT", "FIXED", "INPUT", "SILENT")


def banner(s):
    print("\n" + "=" * 78 + "\n" + s + "\n" + "=" * 78)


def tally():
    return {c: sum(1 for r in LEDGER if r[1] == c) for c in CLASSES}


# ------------------------------------------------------------------------------ Z0
def engine_output():
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        Z.main()
    return buf.getvalue()


def engine_chain():
    """The engine's own numbers, by its own functions: R*, V'', the two matrices, its SVD."""
    R, V, Vpp = Z.stabilize_radius()
    Mu = [Z.dynamical_bulk_masses(R, Vpp, i, "up") for i in range(3)]
    Md = [Z.dynamical_bulk_masses(R, Vpp, i, "down") for i in range(3)]
    Yu = Z.build_yukawa_matrix(R, Mu, Mu, list(FP))
    Yd = Z.build_yukawa_matrix(R, Md, Md, [f + p for f, p in zip(FP, PHASES_DOWN)])
    return R, V, Vpp, Mu, Md, Yu, Yd


# ------------------------------------------------------------------------------ Z1
def casimir_coefficient(n_b=12, n_f=12, weight=0.65):
    return (80.0 / 81.0) * (math.pi**2 / 90.0) * (n_b - weight * n_f)


def exact_minimum(flux_c=0.42, bulk_c=0.18, **kw):
    """Root of dV/dR for V = -a/R^4 + flux_c/R^6 + bulk_c R^2, and V'' there."""
    a = casimir_coefficient(**kw)
    dV = lambda r: 4 * a / r**5 - 6 * flux_c / r**7 + 2 * bulk_c * r
    R = brentq(dV, 0.5, 3.0, xtol=1e-14)
    return R, -20 * a / R**6 + 42 * flux_c / R**8 + 2 * bulk_c


# ------------------------------------------------------------------------------ Z2
def yukawa(c, w, phases, n=2000):
    """The engine's Yukawa matrix in terms of the products that matter: c_i = M_i R (fermion
    exponents) and w = 8 R (Higgs exponent). The radius itself drops out."""
    y = np.arange(n) * 2 * np.pi / n
    d = np.abs(y[None, :] - FP[:, None])
    d = np.minimum(d, 2 * np.pi - d)
    psi = np.exp(-np.asarray(c)[:, None] * d)
    psi /= np.sqrt((psi**2).sum(1))[:, None]
    h = np.exp(-w * d[2])
    h /= np.sqrt((h**2).sum())
    Y = (psi[:, None, :] * psi[None, :, :] * h).sum(2)
    ph = np.abs(np.cos(np.asarray(phases)[:, None] - np.asarray(phases)[None, :]))
    np.fill_diagonal(ph, 1.0)
    Y = Y * ph
    return Y / np.abs(Y).max()


def default_dials():
    """The six effective dials at the engine's values: s = sqrt(V'') x 1.8, the two tilts,
    w = 8 R*, and the three phase offsets."""
    R, _, Vpp = Z.stabilize_radius()
    return [math.sqrt(Vpp) * 1.8, 1.05, 0.92, 8.0 * R, *PHASES_DOWN]


def matrices(x, n=2000):
    s, tu, td, w = x[:4]
    return yukawa(s * tu * TWIST, w, FP, n), yukawa(s * td * TWIST, w, FP + np.asarray(x[4:7]), n)


def observables(x, n=2000):
    """The seven outputs: four Yukawa ratios and three mixing angles (numpy SVD)."""
    Yu, Yd = matrices(x, n)
    Uu, su, _ = np.linalg.svd(Yu)
    Ud, sd, _ = np.linalg.svd(Yd)
    V = np.abs(Uu.T @ Ud)                       # rows (t, c, u), columns (b, s, d)
    s13 = V[2, 0]
    c13 = math.sqrt(max(1 - s13**2, 1e-300))
    return np.array([su[1] / su[0], su[2] / su[0], sd[1] / sd[0], sd[2] / sd[0],
                     V[2, 1] / c13, V[1, 0] / c13, s13])


def decades(x, n=2000):
    return np.log10(np.maximum(observables(x, n), 1e-300) / MEASURED)


def rms_decades(x, n=2000):
    if min(x[:4]) <= 0:
        return 99.0
    return float(np.sqrt(np.mean(decades(x, n)**2)))


def radius_cancels():
    """Largest change in either engine matrix when R is doubled at fixed M R and fixed
    Higgs exponent."""
    R, _, Vpp, Mu, Md, Yu, Yd = engine_chain()
    out = 0.0
    for M, ph, Y in ((Mu, list(FP), Yu), (Md, [f + p for f, p in zip(FP, PHASES_DOWN)], Yd)):
        c = [m * R for m in M]
        out = max(out, np.abs(np.array(Y) - yukawa(c, 8.0 * R, ph)).max())
    return out


# ------------------------------------------------------------------------------ Z3
def svd_check():
    """The engine's Jacobi SVD against numpy's on the engine's own matrices."""
    _, _, _, _, _, Yu, Yd = engine_chain()
    su, Uu, _ = Z.svd_3x3(Yu)
    sd, Ud, _ = Z.svd_3x3(Yd)
    Uu, Ud = np.array(Uu), np.array(Ud)
    orth = max(np.abs(Uu.T @ Uu - np.eye(3)).max(), np.abs(Ud.T @ Ud - np.eye(3)).max())
    V_engine = np.abs(Uu.T @ Ud)
    V_numpy = np.abs(np.linalg.svd(np.array(Yu))[0].T @ np.linalg.svd(np.array(Yd))[0])
    s_err = max(abs(a / b - 1) for a, b in zip(su + sd, list(np.linalg.svd(np.array(Yu))[1])
                                               + list(np.linalg.svd(np.array(Yd))[1])))
    return orth, V_engine, V_numpy, s_err


# ------------------------------------------------------------------------------ Z5
def sensitivity(step=0.10):
    """Change of each output, in decades, when one effective dial is raised by 10%."""
    x0 = default_dials()
    base = np.log10(observables(x0))
    rows = []
    for k, name in ((0, "bulk-mass scale (sqrt(V'') x 1.8)"), (3, "Higgs exponent (8 R*)"),
                    (1, "tilt, up"), (2, "tilt, down")):
        x = list(x0)
        x[k] *= 1 + step
        rows.append((name, np.log10(observables(x)) - base))
    return rows


# ------------------------------------------------------------------------------ Z6
def one_dial_fit():
    x0 = default_dials()
    r = minimize_scalar(lambda s: rms_decades([s] + x0[1:]), bounds=(0.3, 3.0), method="bounded",
                        options={"xatol": 1e-6})
    return r.x, r.fun, decades([r.x] + x0[1:])


def six_dial_fit(samples=3000, seed=7):
    """Random search over the six effective dials, then a local refinement. The scale and
    the tilts enter only as the two products scale x tilt, so the six are: those two, the
    Higgs exponent, and the three phase offsets. Seven outputs, six dials."""
    full = lambda z: [1.0, *z]
    rng = np.random.default_rng(seed)
    best = (99.0, None)
    for _ in range(samples):
        z = [rng.uniform(0.2, 6), rng.uniform(0.2, 6), rng.uniform(0.3, 20), *rng.uniform(-1, 1, 3)]
        m = rms_decades(full(z), 400)
        if m < best[0]:
            best = (m, z)
    r = minimize(lambda z: rms_decades(full(z), 400), best[1], method="Nelder-Mead",
                 options={"maxiter": 4000, "xatol": 1e-6, "fatol": 1e-8})
    x = full(r.x)
    return x, rms_decades(x), decades(x)


# ------------------------------------------------------------------------------ Z7
def engine_coefficients(Nc):
    """The one- and two-loop coefficients typed into the engine's run_331_selection."""
    F = Z.Fraction
    Ng, Qu, Qd = Nc, F(Nc + 1, 2 * Nc), F(1 - Nc, 2 * Nc)
    bL = F(-21, 2) + F(Nc * (Nc + 1), 3)
    bX = F(2, 3) * (Ng * (3 * F(-1, 3)**2 + 1)
                    + Nc * (Ng - F(Nc + 1, 2)) * (3 * (Qu - F(1, 3))**2 + Qu**2 + Qd**2 + (Qu - 1)**2)
                    + Nc * F(Nc + 1, 2) * (3 * (Qd + F(1, 3))**2 + Qd**2 + Qu**2 + (Qd + 1)**2)
                    ) + F(1, 3) * 3 * (F(-1, 3)**2 + F(2, 3)**2 + F(-1, 3)**2)
    return float(bX), float(bL), float(bX) * 1.15, -136.0 + (26.0 / 3.0) * Nc * (Nc + 1)


def exact_coefficients(Nc):
    """The same four numbers from src/m331_exact.py: a_X, a_L, b_XX, b_LL."""
    a, b = E.coefficients(*E.model_331(Nc)[:3])
    return float(a[0]), float(a[1]), float(b[0][0]), float(b[1][1])


def euler_pole(bX, bL, bXX, bLL, ainv=125.7, s2=0.2504, steps=2000):
    """The engine's integration (explicit Euler, pole when a coupling reaches alpha = 1)."""
    t_max = math.log(1.2209e19 / 4.0e3)
    aL = 1.0 / (s2 * ainv)
    aX = 1.0 / ((1.0 - s2) * ainv - s2 * ainv / 3.0)
    dt = t_max / steps
    for k in range(steps):
        daL = bL / (2 * math.pi) * aL**2 + bLL / (8 * math.pi**2) * aL**3
        daX = bX / (2 * math.pi) * aX**2 + bXX / (8 * math.pi**2) * aX**3
        aL += daL * dt
        aX += daX * dt
        if aL >= 1.0 or aX >= 1.0:
            return 4.0e3 * math.exp(k * dt)
    return None


def inputs_at_4tev():
    """This repository's one-loop values of 1/alpha_em and sin^2 theta_W at 4 TeV."""
    L0 = math.log(4.0e3 / E.MZ) / (2 * math.pi)
    aY = (1 - E.s2) * E.ainv - 41 / 6 * L0
    a2 = E.s2 * E.ainv + 19 / 6 * L0
    return aY + a2, a2 / (aY + a2)


# ------------------------------------------------------------------------------ main
def fmt(v):
    return f"{v:.2e}" if v < 1e-2 else f"{v:.4f}"


def main():
    banner("Z0  The engine as given")
    print(engine_output().rstrip())
    print(f"\n   Hand-chosen numbers in the flavour chain: {len(DIALS)}")
    for name, val, where in DIALS:
        print(f"     {name:18s} {val:26s} {where}")
    print("   Section 4 adds four more: 125.7, 0.2504, 4 TeV, and the two-loop factor 1.15.")

    banner("Z1  The stabilised radius")
    Rg, Vg, Vppg = Z.stabilize_radius()
    Rx, Vppx = exact_minimum()
    print(f"   engine (grid of 2000):  R* = {Rg:.5f}   V'' = {Vppg:.5f}")
    print(f"   exact root of dV/dR:    R* = {Rx:.5f}   V'' = {Vppx:.5f}")
    print(f"   The minimum is real and interior. V(R*) = {Vg:+.4f} is positive.")
    print("   R* is a pure number: no unit of length or mass enters the potential.")

    banner("Z2  What the geometry supplies")
    print("   Profiles are exp(-M R d) with M proportional to 1/R, so R cancels:")
    print(f"   engine matrices against the same matrices from M R and 8 R alone: "
          f"largest difference {radius_cancels():.1e}")
    x0 = default_dials()
    print(f"   The potential enters through two numbers: sqrt(V''(R*)) = {math.sqrt(Vppg):.4f} and "
          f"8 R* = {x0[3]:.4f}.")
    print(f"   Exponents M_i R, up:   {', '.join(f'{x0[0] * 1.05 * t:.3f}' for t in TWIST)}")
    print(f"   Exponents M_i R, down: {', '.join(f'{x0[0] * 0.92 * t:.3f}' for t in TWIST)}")
    print("   The twist factors are 2, 4/3, 2/3. The docstring's eigenvalues (0, 1, 2)/3 are not used.")

    banner("Z3  CHECK: the engine's SVD against numpy's")
    orth, Ve, Vn, s_err = svd_check()
    print(f"   singular values agree to {s_err:.1e} (relative)")
    print(f"   engine's left rotation: largest entry of U^T U - 1 = {orth:.1e}  (numpy: 1e-16)")
    print("   |V| from the engine's SVD            |V| from numpy's SVD")
    for a, b in zip(Ve, Vn):
        print("     [" + ", ".join(f"{x:.2e}" for x in a) + "]   [" + ", ".join(f"{x:.2e}" for x in b) + "]")
    print("   The engine's 0.0029 and 0.0068 are rounding error divided by singular values of 1e-7.")
    print(f"   An orthogonal matrix has equal entries there; numpy gives {Vn[1, 2]:.1e} for both.")

    banner("Z4  The seven outputs against the measured values")
    obs = observables(x0)
    dec = decades(x0)
    print("   quantity         engine      measured    engine/measured   decades")
    for nme, o, m, d in zip(OUTPUTS, obs, MEASURED, dec):
        print(f"   {nme:14s}  {o:9.2e}   {m:9.2e}   {o / m:12.1e}      {d:+.2f}")
    print(f"   root-mean-square miss: {rms_decades(x0):.2f} decades")
    print(f"   y_c/y_u: engine {obs[0] / obs[1]:.2f}, measured {MEASURED[0] / MEASURED[1]:.0f}.   "
          f"y_s/y_d: engine {obs[2] / obs[3]:.2f}, measured {MEASURED[2] / MEASURED[3]:.1f}.")
    print(f"   delta_CKM: engine 0 (real matrices), measured {DELTA} rad.")

    banner("Z5  Sensitivity: decades of change per +10% in one dial")
    print("   dial                               " + "  ".join(f"{n.replace('sin ', ''):>8s}" for n in OUTPUTS))
    for name, d in sensitivity():
        print(f"   {name:34s} " + "  ".join(f"{v:+8.2f}" for v in d))

    banner("Z6  Can the structure align at all?")
    s1, m1, d1 = one_dial_fit()
    print(f"   One dial. Bulk-mass scale {x0[0]:.3f} -> {s1:.3f} (geometric factor 1.8 -> "
          f"{1.8 * s1 / x0[0]:.2f}), all else as given:")
    print(f"     rms miss {rms_decades(x0):.2f} -> {m1:.2f} decades;  per output: "
          + ", ".join(f"{v:+.2f}" for v in d1))
    x6, m6, d6 = six_dial_fit()
    print("   Six dials (scale x tilt for up and down, Higgs exponent, three phases) for seven outputs:")
    print(f"     scale x tilt {x6[1]:.2f} (up), {x6[2]:.2f} (down), Higgs exponent {x6[3]:.2f}, "
          f"phases {x6[4]:+.2f}, {x6[5]:+.2f}, {x6[6]:+.2f}")
    print(f"     best found: rms miss {m6:.2f} decades (a factor {10**m6:.1f});  per output: "
          + ", ".join(f"{v:+.2f}" for v in d6))
    lo, hi = min(x6[1], x6[2]) * TWIST[2], max(x6[1], x6[2]) * TWIST[0]
    print("   Localised profiles reach the right orders of magnitude when the exponents M R are")
    print(f"   {lo:.1f} to {hi:.1f} instead of {x0[0] * 0.92 * TWIST[2]:.1f} to {x0[0] * 1.05 * TWIST[0]:.1f}. "
          "They do so with six dials for seven outputs.")

    banner("Z7  The engine's 3-3-1 section against src/m331_exact.py")
    print("   N_c   b_X engine/exact    b_L engine/exact    b_XX engine/exact    b_LL engine/exact")
    for Nc in (3, 5, 7):
        e, x = engine_coefficients(Nc), exact_coefficients(Nc)
        print(f"   {Nc}     {e[0]:7.2f} / {x[0]:7.2f}   {e[1]:7.2f} / {x[1]:7.2f}   "
              f"{e[2]:8.1f} / {x[2]:8.1f}   {e[3]:8.1f} / {x[3]:8.1f}")
    ainv4, s24 = inputs_at_4tev()
    print(f"   inputs at 4 TeV: engine 1/alpha = 125.7, sin^2 = 0.2504;  one-loop running here: "
          f"{ainv4:.1f}, {s24:.4f}")
    print("   pole below M_Pl (engine's integrator; 'none' = survives):")
    print("   N_c   engine coefficients   one loop only   exact coefficients   src/m331_exact.py")
    for Nc in (3, 5, 7):
        e, x = engine_coefficients(Nc), exact_coefficients(Nc)
        ref = E.run_two_loop(Nc)[0]
        cells = [euler_pole(*e), euler_pole(e[0], e[1], 0.0, 0.0), euler_pole(*x),
                 ref if ref is not None and ref < E.M_PLANCK else None]
        print(f"   {Nc}     " + "   ".join(f"{'none' if c is None else f'{c:.1e} GeV':>17s}" for c in cells))
    print("   Section 4 does not use R*, V'' or the bulk masses. It is independent of sections 1-3.")

    banner("Z8  The ledger of 19")
    for name, label, what in LEDGER:
        print(f"   {name:26s} {label:7s} {what}")
    t = tally()
    print("\n   " + ", ".join(f"{c}: {t[c]}" for c in CLASSES))
    print(f"   {t['OUTPUT']} outputs from {len(DIALS)} hand-chosen numbers (6 effective). "
          f"As given, the closest of the {t['OUTPUT']} is a factor "
          f"{10**np.abs(decades(default_dials())).min():.0f} from its measured value.")


if __name__ == "__main__":
    main()
