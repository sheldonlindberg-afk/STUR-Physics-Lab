#!/usr/bin/env python3
"""
The symmetry-breaking ladder, from 3-3-1 to the two-diamond gravity experiment.
A single-file, standard-library-only reproduction of SYMMETRY_LADDER.md.

HOW TO RUN
    Paste this whole file into any Python 3.8+ runner (a terminal, an online
    interpreter, Jupyter, Pyodide, or an AI assistant's code tool) and run it.
    No packages to install: it uses only the Python standard library.
    It runs in about a second. It exits with status 1 if any check fails, so scripts and
    CI can rely on the exit code as well as the printed verdict.

READING THE CHECKS
    Every check is tagged with what it tests:
      [math]    an identity or derivation, verified by exact or numerical computation;
                no measurement is involved, so it can only fail if the algebra is wrong.
      [data]    a computed value against a measurement. The tolerance and the reason
                for it are printed on the next line.
      [pinned]  a number this repository derives (for example the experiment's 2.19 rad
                phase), checked against the value pinned in the repository. It catches
                changes; it is not, by itself, evidence that the physics is right.
    [model] marks a check made inside a simplified stand-in model, not the full theory.

FOR AI ASSISTANTS
    Execute the file as-is and report the printed results. Every rung ends with
    PASS/FAIL checks against the numbers pinned in the source repository, and the last
    lines give the overall verdict. Explain the physics from the section headers and the
    comments; do not change the inputs unless the user asks to.

WHAT IT COMPUTES
    The forces followed down in energy. At each threshold a symmetry breaks and the forces
    separate; gravity is not part of the chain and sits beside it at every scale.
      Rung 1  3-3-1 -> Standard Model -> electromagnetism: the gauge-boson mass matrix from
              the scalar vacuum values; the photon, hypercharge, W, Z, Z', bileptons, rho,
              and every fermion's electric charge for any number of colours.
      Rung 2  The strong force: chiral symmetry breaking in the linear sigma model (a
              MODEL of QCD's low-energy structure): pions, the GMOR relation, the Yukawa
              form and tensor structure of the nuclear force, Goldberger-Treiman; and the
              pion mass at O(p^4) in chiral perturbation theory, QCD's own effective
              theory, with lattice low-energy constants (derived in src/chiral_breaking.py).
      Rung 3  Electromagnetism, the experiment's background: the Casimir-Polder force
              between the diamonds, from electrostatics and the dipole field.
      Rung 4  Gravity to the experiment: linearized GR, one-graviton exchange (Newton's
              law, light's factor 2), and the 2.19 rad entangling phase of design A.
      Rung 5  Gravity as a broken gauge theory: MacDowell-Mansouri (1977), de Sitter
              SO(4,1) broken to Lorentz SO(3,1): an equivalent REFORMULATION of GR + Lambda.
      Rung 6  Black holes: not a symmetry breaking, but gravity's strong-field end, and the
              first formula with hbar, G, c and k_B together. Surface gravity from rung 5's
              spin connection; the temperature fixed by the smoothness of Euclidean time;
              the first law and Smarr in exact fractions; Schwarzschild-de Sitter's two
              horizons and the Nariai limit with the measured Lambda; photon sphere, shadow
              and ISCO; the EHT shadows of M87* and Sgr A*; GW250114's area increase and
              ringdown. Hawking radiation itself is not measured.
      Links   Where one rung feeds another. Neutral matter (rung 1 -> 4): q_p + q_e is an
              anomaly of rung 1, and the experiment needs it below 2.8e-19 e per nucleon.
              pi0 -> gamma gamma (rung 1 -> 2): rung 1's charges and rung 2's f_pi give the
              measured width (f_pi is a measured input; the test is the anomaly normalization).
              The Planck mass (rung 4 -> 1): the 3-3-1 selection's cutoff is sqrt(hbar c / G),
              with the G of the diamond experiment; the selection holds for G down to 8.4x
              weaker at the reference spectrum, 1.6x weaker at the worst point of the
              threshold scan (Landau poles from src/m331_three_loop.py, carried as numbers).
              Black holes (rung 6 -> 4 and link 3): the diamond's Schwarzschild radius is a
              millionth of the Planck length; a Planck-mass black hole has k_B T = M_Pl/8 pi.
    Inputs are measured values (PDG 2024, FLAG 2024, CODATA 2018, Planck 2018; for rung 6 the EHT,
    stellar dynamics and LVK). What is not derived, by
    anyone: why the inputs have their values, and how gravity unifies with the others.

SOURCE
    Repository: https://github.com/sheldonlindberg-afk/STUR-Physics-Lab
    Notes:      SYMMETRY_LADDER.md
    This file condenses src/m331_breaking.py, chiral_breaking.py, casimir_diamonds.py,
    graviton_exchange.py, macdowell_mansouri.py, black_holes.py and ladder_links.py;
    tests/test_ladder_standalone.py checks
    that it agrees with them. Independent work, not peer reviewed. License: CC0 1.0.
"""
from fractions import Fraction as F
from itertools import permutations
from math import cos, exp, factorial, pi, sin, sqrt
import random
import textwrap
import time

# ----------------------------------------------------------------------------------------
# Inputs (PDG 2024, FLAG 2024, CODATA 2018, Planck 2018)
# CODATA 2018 is kept to match the rest of the repository. CODATA 2022 changes alpha,
# 1/(4 pi eps0) and the atomic mass unit only in the 9th-10th digit (G, hbar, c, e are
# unchanged), which moves no printed result.
# ----------------------------------------------------------------------------------------
G_F = 1.1663788e-5            # GeV^-2, Fermi constant
MZ_MEAS = 91.1876             # GeV
ALPHA_MZ_INV = 127.951        # 1/alpha_em(M_Z), MS-bar
S2_MZ = 0.23122               # sin^2 theta_W(M_Z), MS-bar
MU_PLUS_MD = 2.16e-3 + 4.70e-3   # GeV, m_u + m_d, MS-bar 2 GeV
MU_PLUS_MD_ERR = sqrt(0.07e-3**2 + 0.07e-3**2)   # GeV, PDG 2024: m_u, m_d each +- 0.07 MeV
F_PI = 0.1302 / sqrt(2)       # GeV, f_pi = 92.1 MeV
COND_13 = 0.272               # GeV, |<qbar q>|^(1/3), lattice (FLAG), MS-bar 2 GeV
COND_13_ERR = 0.005           # GeV, FLAG 19 average (N_f = 2+1), restated in FLAG 21; FLAG 2024 omits LECs
M_PI0, M_PIC = 0.1349768, 0.13957039
# N_f = 2+1 lattice inputs for the O(p^4) pion mass (src/chiral_breaking.py S7): m_ud from
# FLAG 2024 (arXiv:2411.04268); F_pi/F and lbar_3 the FLAG 19 averages restated in FLAG 21
M_UD_FLAG, M_UD_FLAG_ERR = 3.364e-3, 0.041e-3   # GeV, (m_u + m_d)/2, MS-bar 2 GeV
FPI_OVER_F, FPI_OVER_F_ERR = 1.062, 0.007
LBAR3, LBAR3_ERR = 3.07, 0.64
G_A, M_N = 1.2754, 0.9389187  # nucleon axial coupling; average nucleon mass (GeV)
G_PINN_EMP = 13.1             # charged pi-N coupling: g_c^2/4pi = 13.69 +- 0.12 +- 0.15 (GMO sum rule;
G_PINN_ERR = 0.1              # Baru et al., Nucl. Phys. A 872, 69 (2011), eq. 9.13), so g = 13.12 +- 0.09
HBARC_GEV_FM = 0.1973269804
G_NEWTON = 6.67430e-11        # m^3 kg^-1 s^-2
HBAR = 1.054571817e-34        # J s
C_LIGHT = 2.99792458e8        # m/s
EPS_DIAMOND = 5.7             # static permittivity of diamond
RHO_DIAMOND = 3510.0          # kg/m^3
LAMBDA_SI = 1.1056e-52        # m^-2, Planck 2018 (TT,TE,EE+lowE+lensing+BAO): 3 H0^2 Omega_L / c^2 with H0 = 67.66, Omega_L = 0.6889
#   (A&A 641, A6 (2020), Table 2). Planck quotes Lambda = (4.24 +- 0.11)e-66 eV^2 = 1.089e-52 m^-2 without BAO.
L_PLANCK = 1.616255e-35       # m
# Landau poles of the 3-3-1 running in GeV (N_c = 3, N_c = 5), at the reference spectrum:
# M_V = 4 TeV, Yukawas and thresholds on, alpha = 1, three loops. Computed by
# src/m331_three_loop.py (too heavy to repeat here); tests/test_ladder_standalone.py checks
# them against that module. They are the repository's numbers, so their check is pinned.
POLES_331 = {"+1/sqrt3": (3.53147e19, 5.18629e11), "-1/sqrt3": (2.33273e29, 1.13517e15)}
# The same poles over the 72-point threshold scan of NOTE_331.md 3a (r_J, r_S, M_V, light
# doublets): the lowest N_c = 3 pole and the highest N_c = 5 pole, i.e. the narrowest window.
# Computed by src/ladder_links.py L3e; tests/test_ladder_standalone.py checks them against it.
POLES_331_SCAN = {"+1/sqrt3": (1.55807e19, 2.70740e12), "-1/sqrt3": (1.54193e29, 4.29258e15)}

CHECKS = []
KINDS = ("math", "data", "pinned")


def banner(s):
    print("\n" + "=" * 78 + "\n" + s + "\n" + "=" * 78)


def plain(text):
    """A plain-language summary of a rung, for readers who are not specialists."""
    print(textwrap.fill("In plain words: " + text, 90, initial_indent="   ", subsequent_indent="   ") + "\n")


def check(label, ok, kind="math", note=None, model=False):
    """Record one check. kind: 'math', 'data' or 'pinned' (see READING THE CHECKS).
    note: what was compared and why the tolerance is what it is, printed under the check."""
    assert kind in KINDS
    CHECKS.append((label, bool(ok), kind))
    tag = f"[{kind}]" + (" [model]" if model else "")
    print(f"   [{'PASS' if ok else 'FAIL'}] {tag:15s} {label}")
    if note:
        print(textwrap.fill(note, 90, initial_indent=" " * 10, subsequent_indent=" " * 10))


# ----------------------------------------------------------------------------------------
# Small linear algebra (lists of lists)
# ----------------------------------------------------------------------------------------
def zeros(n, m=None):
    return [[0] * (m or n) for _ in range(n)]


def eye(n):
    return [[1 if i == j else 0 for j in range(n)] for i in range(n)]


def mat_mul(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]


def mat_add(A, B, s=1):
    return [[A[i][j] + s * B[i][j] for j in range(len(A[0]))] for i in range(len(A))]


def mat_scale(A, s):
    return [[s * x for x in row] for row in A]


def comm(A, B):
    return mat_add(mat_mul(A, B), mat_mul(B, A), -1)


def mat_vec(A, v):
    return [sum(A[i][k] * v[k] for k in range(len(v))) for i in range(len(A))]


def jacobi_eigenvalues(A, tol=1e-14, sweeps=100):
    """Eigenvalues of a real symmetric matrix by cyclic Jacobi rotations."""
    a = [row[:] for row in A]
    n = len(a)
    for _ in range(sweeps):
        off = sum(a[i][j] ** 2 for i in range(n) for j in range(n) if i != j)
        if off < tol**2 * (1 + sum(a[i][i] ** 2 for i in range(n))):
            break
        for p in range(n):
            for q in range(p + 1, n):
                if abs(a[p][q]) < 1e-300:
                    continue
                th = (a[q][q] - a[p][p]) / (2 * a[p][q])
                t = (1 if th >= 0 else -1) / (abs(th) + sqrt(th * th + 1))
                c = 1 / sqrt(t * t + 1)
                s = t * c
                for k in range(n):
                    akp, akq = a[k][p], a[k][q]
                    a[k][p], a[k][q] = c * akp - s * akq, s * akp + c * akq
                for k in range(n):
                    apk, aqk = a[p][k], a[q][k]
                    a[p][k], a[q][k] = c * apk - s * aqk, s * apk + c * aqk
    return sorted(a[i][i] for i in range(n))


# ----------------------------------------------------------------------------------------
# RUNG 1: 3-3-1 -> Standard Model -> electromagnetism
# ----------------------------------------------------------------------------------------
def gell_mann_halves():
    """T^a = lambda^a / 2 as 3x3 complex matrices."""
    l = [zeros(3) for _ in range(8)]
    l[0][0][1] = l[0][1][0] = 1
    l[1][0][1], l[1][1][0] = -1j, 1j
    l[2][0][0], l[2][1][1] = 1, -1
    l[3][0][2] = l[3][2][0] = 1
    l[4][0][2], l[4][2][0] = -1j, 1j
    l[5][1][2] = l[5][2][1] = 1
    l[6][1][2], l[6][2][1] = -1j, 1j
    l[7] = [[1 / sqrt(3), 0, 0], [0, 1 / sqrt(3), 0], [0, 0, -2 / sqrt(3)]]
    return [mat_scale(m, 0.5) for m in l]


T8_TIMES_BETA = {"-1/sqrt3": (F(-1, 6), F(-1, 6), F(1, 3)), "+1/sqrt3": (F(1, 6), F(1, 6), F(-1, 3))}
T3_DIAG = (F(1, 2), F(-1, 2), F(0))
BETA = {"-1/sqrt3": -1 / sqrt(3), "+1/sqrt3": 1 / sqrt(3)}


def model(Nc, variant):
    """Fermions (multiplicity, SU(3)_L dim, colour dim, X, is_antitriplet) and the scalar
    triplets' X charges, as in src/m331_exact.py."""
    Qu, Qd = F(Nc + 1, 2 * Nc), F(1 - Nc, 2 * Nc)
    Ng, nA = Nc, (1 + Nc) // 2
    if variant == "-1/sqrt3":
        Xt, Xa = Qu - F(1, 3), Qd + F(1, 3)
        ferm = [(Ng, 3, 1, F(-1, 3), False), (Ng, 1, 1, F(1), False),
                (Ng - nA, 3, Nc, Xt, False), (nA, 3, Nc, Xa, True),
                (Ng, 1, Nc, -Qu, False), (Ng, 1, Nc, -Qd, False),
                (Ng - nA, 1, Nc, -Qu, False), (nA, 1, Nc, -Qd, False)]
        scal = [F(-1, 3), F(2, 3), F(-1, 3)]
    else:
        Xt, Xa = Qu - F(2, 3), Qd + F(2, 3)
        ferm = [(Ng, 3, 1, F(-2, 3), False), (Ng, 1, 1, F(1), False), (Ng, 1, 1, F(1), False),
                (Ng - nA, 3, Nc, Xt, False), (nA, 3, Nc, Xa, True),
                (Ng, 1, Nc, -Qu, False), (Ng, 1, Nc, -Qd, False),
                (Ng - nA, 1, Nc, -Qd, False), (nA, 1, Nc, -Qu, False)]
        scal = [F(1, 3), F(1, 3), F(-2, 3)]
    return ferm, scal, Qu, Qd


def triplet_charges(X, variant, anti=False):
    b = T8_TIMES_BETA[variant]
    sgn = -1 if anti else 1
    return [sgn * (T3_DIAG[k] + b[k]) + X for k in range(3)]


def vev_layout(variant):
    """Each scalar triplet's neutral components (exact), and where its vev sits: the first
    triplet neutral in component 3 takes w; the others take v1, v2."""
    _, scal, _, _ = model(3, variant)
    out, chi_done = [], False
    for X in scal:
        q = triplet_charges(X, variant)
        neutral = [k for k in range(3) if q[k] == 0]
        if 2 in neutral and not chi_done:
            out.append((X, 2, "w", neutral))
            chi_done = True
        else:
            out.append((X, [k for k in neutral if k != 2][0], None, neutral))
    names = iter(("v1", "v2"))
    return [(X, k, n if n else next(names), neu) for X, k, n, neu in out]


def mass_matrix(variant, g, gX, w, v1, v2):
    T = gell_mann_halves()
    vals = {"w": w, "v1": v1, "v2": v2}
    cs = [g] * 8 + [gX]
    M = zeros(9)
    for X, k, name, _ in vev_layout(variant):
        phi = [0, 0, 0]
        phi[k] = vals[name] / sqrt(2)
        gens = T + [mat_scale(eye(3), float(X))]
        for A in range(9):
            for B in range(9):
                anti = mat_add(mat_mul(gens[A], gens[B]), mat_mul(gens[B], gens[A]))
                val = sum(phi[i].conjugate() * anti[i][j] * phi[j] if isinstance(phi[i], complex) else phi[i] * anti[i][j] * phi[j]
                          for i in range(3) for j in range(3))
                M[A][B] += cs[A] * cs[B] * complex(val).real
    return M


def rung1():
    banner("RUNG 1  3-3-1 -> Standard Model -> electromagnetism (gauge-boson mass matrix)")
    plain("one larger force splits, in two steps, into the weak force and electromagnetism. The checks confirm that exactly one force carrier stays massless (the photon, which carries light) and that the W and Z particles get the right masses.")
    g, gX, w = 0.652, 0.79, 4000.0
    print(f"   Example values g = {g}, g_X = {gX}, w = {w / 1e3:.0f} TeV, v1, v2 = 150, 190 GeV: the checks below are")
    print("   identities that hold for any values, so no Z' or bilepton mass is predicted here.")
    for variant in ("-1/sqrt3", "+1/sqrt3"):
        beta = BETA[variant]
        print(f"   beta = {variant}")
        lay = vev_layout(variant)
        for X, k, name, neu in lay:
            print(f"     triplet X = {str(X):5s}: Q = 0 in components {[c + 1 for c in neu]}; vev {name} in component {k + 1}")
        v1, v2 = 150.0, 190.0
        M = mass_matrix(variant, g, gX, w, v1, v2)
        ev = jacobi_eigenvalues(M)
        scale = max(abs(x) for x in ev)
        nzero = sum(abs(x) < 1e-12 * scale for x in ev)
        check(f"{variant}: the 9x9 mass matrix has exactly one zero eigenvalue (8 massive bosons)", nzero == 1)
        nQ = [0, 0, 1 / g, 0, 0, 0, 0, beta / g, 1 / gX]
        res = max(abs(x) for x in mat_vec(M, nQ))
        check(f"{variant}: the massless state is the gauge field of Q = T3 + beta T8 + X", res < 1e-9 * scale)
        einv2 = sum(x * x for x in nQ)
        M0 = mass_matrix(variant, g, gX, w, 0.0, 0.0)
        ev0 = jacobi_eigenvalues(M0)
        nzero0 = sum(abs(x) < 1e-12 * max(abs(y) for y in ev0) for x in ev0)
        nY = [0] * 7 + [beta / g, 1 / gX]
        gYinv2 = sum(x * x for x in nY)
        check(f"{variant}: after step 1 alone, 4 massless states; Y = beta T8 + X is massless and "
              f"1/g_Y^2 = beta^2/g^2 + 1/g_X^2 (the matching condition)",
              nzero0 == 4 and max(abs(x) for x in mat_vec(M0, nY)) < 1e-9 * max(ev0)
              and abs(einv2 - (1 / g**2 + gYinv2)) < 1e-12)
        gY2 = 1 / gYinv2
        v2s = v1 * v1 + v2 * v2
        mw2 = (M[0][0] + M[1][1]) / 2
        check(f"{variant}: M_W^2 = g^2 v^2/4 and bilepton masses g^2 (w^2 + v_i^2)/4",
              abs(mw2 / (g * g * v2s / 4) - 1) < 1e-12
              and all(abs(x / y - 1) < 1e-12 for x, y in zip(sorted([M[3][3], M[5][5]]),
                                                            sorted(g * g * (w * w + v * v) / 4 for v in (v1, v2)))))
        neutral = [[M[i][j] for j in (2, 7, 8)] for i in (2, 7, 8)]
        nev = jacobi_eigenvalues(neutral)
        lamZ, lamZp = nev[1], nev[2]
        eps = (v2s / w**2)
        check(f"{variant}: M_Z^2 -> (g^2 + g_Y^2) v^2/4 and M_Z'^2 -> (g^2 + beta^2 g_X^2) w^2/3 (to O(v^2/w^2))",
              abs(lamZ / ((g * g + gY2) * v2s / 4) - 1) < 5 * eps and abs(lamZp / ((g * g + beta**2 * gX**2) * w**2 / 3) - 1) < 5 * eps)
        s2 = 0.23
        tX2 = s2 / (1 - (1 + beta**2) * s2)
        gx_s2 = sqrt(s2 * g * g / (1 - s2 - beta**2 * s2))
        ratio2 = ((g * g + beta**2 * gx_s2**2) / 3) / (g * g / 4)
        check(f"{variant}: M_Z'/M_V = sqrt(4/3 (1 + beta^2 t_X^2)), t_X^2 = s2/(1 - (1+beta^2) s2) (derived)",
              abs(ratio2 - 4 / 3 * (1 + beta**2 * tX2)) < 1e-12)
        cw2 = g * g / (g * g + gY2)
        rho = mw2 / (lamZ * cw2)
        M2 = mass_matrix(variant, g, gX, 2 * w, v1, v2)
        nev2 = jacobi_eigenvalues([[M2[i][j] for j in (2, 7, 8)] for i in (2, 7, 8)])
        rho2 = (M2[0][0] + M2[1][1]) / 2 / (nev2[1] * cw2)
        check(f"{variant}: rho = M_W^2/(M_Z^2 cos^2 theta_W) >= 1, with rho - 1 ~ (v/w)^2 (Z-Z' mixing)",
              rho > 1 and 3.9 < (rho - 1) / (rho2 - 1) < 4.1)
        ok = True
        for Nc in (3, 5, 7):
            ferm, _, Qu, Qd = model(Nc, variant)
            for mult, dL, dC, X, anti in ferm:
                if dL == 3:
                    q = triplet_charges(X, variant, anti)
                    ok &= set(q[:2]) == ({F(0), F(-1)} if dC == 1 else {Qu, Qd})
        check(f"{variant}: every SU(2)_L doublet has charges (Q_u, Q_d) = ((N_c+1)/2N_c, (1-N_c)/2N_c) "
              "or (0, -1), for N_c = 3, 5, 7", ok)
        print(f"     1/e^2 = (1 + beta^2)/g^2 + 1/g_X^2; rho - 1 = {rho - 1:.3e} at v/w = {sqrt(v2s) / w:.3f}")
    v = (sqrt(2) * G_F) ** -0.5
    mz = sqrt(pi / ALPHA_MZ_INV / (sqrt(2) * G_F) / (S2_MZ * (1 - S2_MZ)))
    print(f"   v = (sqrt2 G_F)^(-1/2) = {v:.2f} GeV; tree-level M_Z = {mz:.2f} GeV vs measured {MZ_MEAS}"
          f" ({100 * (mz / MZ_MEAS - 1):+.2f}%, the radiative correction, not derived)")
    check("v = 246.22 GeV from G_F, and tree-level M_Z within 0.5% of the measurement",
          abs(v - 246.22) < 0.01 and abs(mz / MZ_MEAS - 1) < 0.005, "data",
          f"got M_Z = {mz:.2f} GeV vs {MZ_MEAS} GeV ({100 * (mz / MZ_MEAS - 1):+.2f}%). Tolerance 0.5%: this is tree"
          " level, and the loop corrections it omits are each of order alpha/pi = 0.25%")


# ----------------------------------------------------------------------------------------
# RUNG 2: the strong force (linear sigma model: a MODEL)
# ----------------------------------------------------------------------------------------
def sigma_potential(lam, v, H, phi):
    p2 = sum(x * x for x in phi)
    return lam / 4 * (p2 - v * v) ** 2 - H * phi[0]


def hessian(fun, x, h=1e-4):
    n = len(x)
    Hm = zeros(n)
    for i in range(n):
        for j in range(n):
            def f(di, dj):
                y = list(x)
                y[i] += di
                y[j] += dj
                return fun(y)
            Hm[i][j] = (f(h, h) - f(h, -h) - f(-h, h) + f(-h, -h)) / (4 * h * h)
    return Hm


def pauli():
    return [[[0, 1], [1, 0]], [[0, -1j], [1j, 0]], [[1, 0], [0, -1]]]


def kron(A, B):
    return [[A[i // 2][j // 2] * B[i % 2][j % 2] for j in range(4)] for i in range(4)]


def rung2():
    banner("RUNG 2  The strong force: chiral symmetry breaking (MODEL: linear sigma model)")
    plain("when a symmetry of the strong force breaks, light particles called pions appear. Exchanging pions between protons and neutrons is what holds atomic nuclei together. Some checks here use a simplified stand-in for the strong force, and they are marked [model].")
    lam, v = 2.0, 1.0
    Hm = hessian(lambda p: sigma_potential(lam, v, 0.0, p), [v, 0, 0, 0])
    ev = jacobi_eigenvalues(Hm)
    nz = sum(abs(x) < 1e-6 for x in ev)
    check("massless quarks: the vacuum breaks O(4) -> O(3), leaving exactly 3 Goldstone pions (6 - 3)",
          nz == 3 and abs(ev[-1] - 2 * lam * v * v) < 1e-4, model=True)
    H = 0.05
    s0 = v
    for _ in range(60):                                    # vacuum: lam s0 (s0^2 - v^2) = H
        s0 -= (lam * s0 * (s0 * s0 - v * v) - H) / (lam * (3 * s0 * s0 - v * v))
    mpi2 = hessian(lambda p: sigma_potential(lam, v, H, p), [s0, 0, 0, 0])[1][1]
    check("quark masses: m_pi^2 = H/<sigma>, f_pi = <sigma>, so m_pi^2 f_pi^2 = H f_pi (the GMOR form)",
          abs(mpi2 - H / s0) < 1e-6, model=True)
    mpi = sqrt(MU_PLUS_MD * COND_13**3) / F_PI
    print(f"   GMOR: m_pi = sqrt((m_u + m_d)|<qbar q>|)/f_pi = {mpi * 1e3:.1f} MeV;"
          f" measured {M_PI0 * 1e3:.1f} MeV ({100 * (mpi / M_PI0 - 1):+.1f}%, higher-order chiral terms)")
    dmpi = 0.5 * sqrt((MU_PLUS_MD_ERR / MU_PLUS_MD) ** 2 + (3 * COND_13_ERR / COND_13) ** 2)
    check("GMOR with measured quark masses, f_pi and the lattice condensate: m_pi = 127.6 MeV (within 8% of 135)",
          abs(mpi - 0.1276) < 1e-3 and abs(mpi / M_PI0 - 1) < 0.08, "data",
          f"got {mpi * 1e3:.1f} +- {dmpi * mpi * 1e3:.1f} MeV (inputs, {100 * dmpi:.1f}%) vs {M_PI0 * 1e3:.1f} MeV."
          " Tolerance 8%: GMOR is leading order with f_pi standing in for the chiral-limit F; the next check"
          " does it at O(p^4)")
    # chiral perturbation theory at O(p^4): M^2 = 2 m_ud Sigma / F^2, M_pi^2 = M^2 [1 - M^2 lbar_3 / (32 pi^2 F^2)]
    def mpi4(mud, c13, r, l3):
        Fc = F_PI / r
        M2 = 2 * mud * c13**3 / Fc**2
        return sqrt(M2 * (1 - M2 / (32 * pi * pi * Fc * Fc) * l3))
    c4 = [M_UD_FLAG, COND_13, FPI_OVER_F, LBAR3]
    m4 = mpi4(*c4)
    dm4 = 0.0
    for i, e in enumerate((M_UD_FLAG_ERR, COND_13_ERR, FPI_OVER_F_ERR, LBAR3_ERR)):
        up = list(c4)
        up[i] += e
        dm4 += (mpi4(*up) - m4) ** 2
    dm4 = sqrt(dm4)
    print(f"   O(p^4) chiral perturbation theory, FLAG inputs: m_pi = {m4 * 1e3:.1f} +- {dm4 * 1e3:.1f} MeV")
    check("the pion mass at O(p^4) in chiral perturbation theory: 132.6 MeV, within 2 sigma of 135.0",
          abs(m4 - 0.1326) < 1e-3 and abs(m4 - M_PI0) < 2 * dm4, "data",
          f"got {m4 * 1e3:.1f} +- {dm4 * 1e3:.1f} MeV vs {M_PI0 * 1e3:.1f} MeV ({(m4 - M_PI0) / dm4:+.1f} sigma)."
          " Not the sigma model: QCD's effective theory, whose one-loop chiral log src/chiral_breaking.py S6"
          " derives in two parametrizations; lbar_3, F_pi/F and the condensate are FLAG 19/21 averages, m_ud is FLAG 2024's."
          " The uncertainty is mostly the condensate")
    m = 1.3
    V = lambda r: exp(-m * r) / (4 * pi * r)
    rs = [0.3, 0.9, 2.1]
    hh = 1e-4
    lap = [(V(r + hh) * (r + hh) - 2 * V(r) * r + V(r - hh) * (r - hh)) / (hh * hh) / r for r in rs]
    flux = -4 * pi * (1e-4) ** 2 * (V(1e-4 + 1e-7) - V(1e-4 - 1e-7)) / 2e-7
    check("exchange of a mass-m particle: V = e^(-m r)/(4 pi r) solves (lap - m^2) V = 0 with unit flux"
          " (the Fourier transform of 1/(q^2 + m^2): the Yukawa potential)",
          max(abs(lp - m * m * V(r)) / (m * m * V(r)) for lp, r in zip(lap, rs)) < 1e-5 and abs(flux - 1) < 1e-3)
    rng = HBARC_GEV_FM / M_PIC
    print(f"   Range of the nuclear force 1/m_pi = {rng:.3f} fm")
    S = pauli()
    rnd = random.Random(3)
    q = [rnd.uniform(-2, 2) for _ in range(3)]
    q2 = sum(x * x for x in q)
    sq = [[sum(q[i] * S[i][a][b] for i in range(3)) for b in range(2)] for a in range(2)]
    qh = [x / sqrt(q2) for x in q]
    sqh = [[sum(qh[i] * S[i][a][b] for i in range(3)) for b in range(2)] for a in range(2)]
    s1s2 = [[sum(kron(S[i], S[i])[a][b] for i in range(3)) for b in range(4)] for a in range(4)]
    S12 = mat_add(mat_scale(kron(sqh, sqh), 3), s1s2, -1)
    lhs = kron(sq, sq)
    rhs = mat_scale(mat_add(s1s2, S12), q2 / 3)
    check("one-pion exchange: (s1.q)(s2.q) = (q^2/3)[s1.s2 + S12]: central and tensor nuclear forces, and range 1.414 fm",
          max(abs(lhs[a][b] - rhs[a][b]) for a in range(4) for b in range(4)) < 1e-12 and abs(rng - 1.414) < 1e-3)
    gpinn = G_A * M_N / F_PI
    print(f"   Goldberger-Treiman: g_piNN = g_A M_N / f_pi = {gpinn:.2f}; empirical {G_PINN_EMP} +- {G_PINN_ERR}")
    eps_chi = (M_PIC / (4 * pi * F_PI)) ** 2
    check("Goldberger-Treiman from chiral symmetry: g_piNN = 13.01, within 2% of the empirical value",
          abs(gpinn / G_PINN_EMP - 1) < 0.02, "data",
          f"got {gpinn:.2f} vs {G_PINN_EMP} +- {G_PINN_ERR} ({100 * (gpinn / G_PINN_EMP - 1):+.1f}%). Tolerance 2%:"
          f" the Goldberger-Treiman discrepancy is a next-order chiral correction, of order"
          f" (m_pi/4 pi f_pi)^2 = {100 * eps_chi:.1f}%")


# ----------------------------------------------------------------------------------------
# RUNG 3: Casimir-Polder between the diamonds
# ----------------------------------------------------------------------------------------
def diamond_radius(m):
    return (3 * m / (4 * pi * RHO_DIAMOND)) ** (1 / 3)


def green(x, y, z, k):
    r = sqrt(x * x + y * y + z * z)
    u = k * r
    X = (x, y, z)
    return [[exp(-u) / r**3 * ((1 + u + u * u) * (i == j) - (3 + 3 * u + u * u) * X[i] * X[j] / r**2)
             for j in range(3)] for i in range(3)]


def rung3():
    banner("RUNG 3  Electromagnetism, the experiment's background: Casimir-Polder")
    plain("two electrically neutral diamonds still attract slightly, through quantum fluctuations of the electromagnetic field. The experiment must keep this pull well below gravity, which sets how close the diamonds may come.")
    eps = F(57, 10)
    # inside A r cos(th), outside -E0 r cos(th) + B cos(th)/r^2 (R = E0 = 1): continuity and eps-flux
    # A = -1 + B ; eps A = -1 - 2B  ->  B = (eps - 1)/(eps + 2)
    B = (eps - 1) / (eps + 2)
    A = -1 + B
    check("dielectric sphere, from Laplace's equation: alpha/(4 pi eps0) = K R^3, K = (eps-1)/(eps+2)",
          eps * A == -1 - 2 * B and B == (eps - 1) / (eps + 2))
    pt, k, h = (0.37, -0.29, 0.41), 1.7, 1e-3
    Gc = green(*pt, k)
    worst = 0.0
    def lap_fd(i, j, hs):
        tot = 0.0
        for d in range(3):
            p1, p2 = list(pt), list(pt)
            p1[d] += hs
            p2[d] -= hs
            tot += (green(*p1, k)[i][j] - 2 * Gc[i][j] + green(*p2, k)[i][j]) / (hs * hs)
        return tot
    scale = max(abs(Gc[i][j]) for i in range(3) for j in range(3))
    for i in range(3):
        for j in range(3):
            lap = (4 * lap_fd(i, j, h / 2) - lap_fd(i, j, h)) / 3        # Richardson: O(h^4)
            worst = max(worst, abs(lap - k * k * Gc[i][j]) / (k * k * scale))
    r = sqrt(sum(x * x for x in pt))
    u = k * r
    tr = sum(Gc[i][j] * Gc[j][i] for i in range(3) for j in range(3))
    target = 2 * exp(-2 * u) * (3 + 6 * u + 5 * u**2 + 2 * u**3 + u**4) / r**6
    check("dipole Green tensor at imaginary frequency solves (lap - xi^2/c^2) G = 0, and "
          "Tr G.G = 2 e^(-2u)(3 + 6u + 5u^2 + 2u^3 + u^4)/r^6", worst < 1e-6 and abs(tr / target - 1) < 1e-12)
    coeffs = (3, 6, 5, 2, 1)
    I = sum(F(c) * F(factorial(n), 2 ** (n + 1)) for n, c in enumerate(coeffs))
    check("the fluctuation integral int_0^oo e^(-2u)(3 + 6u + 5u^2 + 2u^3 + u^4) du = 23/4 exactly,"
          " so U = -(23/4 pi) hbar c alpha1 alpha2 / r^7 (Casimir-Polder)", I == F(23, 4))
    m, rr = geomspace(1e-16, 1e-12, 25)[13], 200e-6          # design A's mass (rung 4)
    R = diamond_radius(m)
    K = (EPS_DIAMOND - 1) / (EPS_DIAMOND + 2)
    Uc = -float(I) / pi * HBAR * C_LIGHT * (K * R**3) ** 2 / rr**7
    Ug = -G_NEWTON * m * m / rr
    print(f"   design A, m = {m:.3e} kg (R = {R * 1e6:.2f} um), r = 200 um: Casimir {Uc:.3e} J, gravity {Ug:.3e} J, ratio {Uc / Ug:.2e}")
    check("at 200 um Casimir is 2.3% of gravity, and both scale as R^6, so the safe gap is mass-independent",
          abs(Uc / Ug - 2.335e-2) < 2e-4, "pinned", f"got {Uc / Ug:.4e}, pinned 2.335e-2 +- 2e-4")


# ----------------------------------------------------------------------------------------
# RUNG 4: gravity to the experiment
# ----------------------------------------------------------------------------------------
ETA4 = (-1, 1, 1, 1)


def tpt(T1, T2):
    """T2.P.T1 with P = (eta eta + eta eta - eta eta)/2 (diagonal T's, exact)."""
    full = sum(F(ETA4[a] ** 2) * T1[a] * T2[a] for a in range(4))
    tr = lambda T: sum(ETA4[a] * T[a] for a in range(4))
    return (2 * full - tr(T1) * tr(T2)) / 2


def ramp_profile(t, hold, ramp):
    def up(x):
        x = min(max(x, 0.0), 1.0)
        return 2 * x * x if x < 0.5 else 1 - 2 * (1 - x) ** 2
    total = hold + 2 * ramp
    if t < ramp:
        return up(t / ramp)
    if t > ramp + hold:
        return up((total - t) / ramp)
    return 1.0


def geomspace(a, b, n):
    return [a * (b / a) ** (k / (n - 1)) for k in range(n)]


def casimir_safe_gap():
    """Smallest gap where Casimir's entangling phase is <= 10% of gravity's (parallel geometry,
    the repository's baseline m = 1e-14 kg, dx = 250 um, tau = 2.5 s)."""
    m, dx, tau = 1e-14, 250e-6, 2.5
    R = diamond_radius(m)
    K = (EPS_DIAMOND - 1) / (EPS_DIAMOND + 2)
    for gap in geomspace(1e-6, 1e-3, 4000):
        r = [[gap, sqrt(gap * gap + dx * dx)], [sqrt(gap * gap + dx * dx), gap]]
        ent = lambda f: f(r[0][0]) + f(r[1][1]) - f(r[0][1]) - f(r[1][0])
        grav = ent(lambda x: G_NEWTON * m * m * tau / (HBAR * x))
        cas = ent(lambda x: (23 * HBAR * C_LIGHT / (4 * pi)) * R**6 / x**7 * K**2 * tau / HBAR)
        if abs(cas) <= 0.1 * abs(grav):
            return gap
    return float("nan")


def rung4():
    banner("RUNG 4  Gravity to the diamond experiment (linearized GR, one-graviton exchange)")
    plain("treating gravity as the exchange of gravitons reproduces Newton's law and gives the quantum phase, 2.19 radians, that the two-diamond experiment would measure.")
    hbar00 = F(4)                                          # in units of GM/r
    trace = ETA4[0] * hbar00
    h00 = hbar00 - F(ETA4[0]) * trace / 2
    hii = 0 - F(ETA4[1]) * trace / 2
    check("linearized GR, point mass: h_00 = h_ii = 2GM/r, so Phi = -GM/r and PPN gamma = 1",
          h00 == 2 and hii == 2 and -h00 / 2 == -1 and hii / h00 == 1)
    T1, T2, Tph = (F(1), 0, 0, 0), (F(1), 0, 0, 0), (F(1), 0, 0, F(1))
    check("one-graviton exchange: T2.P.T1 = m1 m2 / 2, U(q) = -4 pi G m1 m2/q^2 -> U(r) = -G m1 m2 / r"
          " (rung 2's transform at m = 0)", tpt(T1, T2) == F(1, 2))
    check("a photon couples twice as strongly as a static mass of the same energy: light bends 4GM/(c^2 b)",
          tpt(T1, Tph) / tpt(T1, T2) == 2)
    m = geomspace(1e-16, 1e-12, 25)[13]
    dx = geomspace(10e-6, 3e-3, 25)[18]
    hold = geomspace(0.05, 20, 25)[2]
    ramp = geomspace(0.05, 5, 17)[12]
    gap = casimir_safe_gap()
    n = 4001
    total = hold + 2 * ramp
    ts = [total * i / (n - 1) for i in range(n)]
    integrand = []
    for t in ts:
        y = 0.5 * dx * ramp_profile(t, hold, ramp)
        integrand.append(2 * (1 / gap - 1 / sqrt(gap * gap + (2 * y) ** 2)))
    dt = total / (n - 1)
    integral = dt * (sum(integrand) - 0.5 * (integrand[0] + integrand[-1]))
    dphi = G_NEWTON * m * m / HBAR * integral
    print(f"   Casimir-safe gap {gap * 1e6:.2f} um; design A: m = {m:.4e} kg, dx = {dx * 1e6:.1f} um,"
          f" hold {hold:.4f} s, ramps 2 x {ramp:.4f} s")
    print(f"   Entangling phase Delta phi = phi_LL + phi_RR - phi_LR - phi_RL = {dphi:.4f} rad")
    check("design A's entangling phase from the graviton-exchange potential: 2.19 rad",
          abs(dphi - 2.1868) < 1e-3 and abs(gap - 181.16e-6) < 0.1e-6, "pinned",
          f"got {dphi:.4f} rad and gap {gap * 1e6:.2f} um, pinned 2.1868 rad and 181.16 um")


# ----------------------------------------------------------------------------------------
# RUNG 5: MacDowell-Mansouri, SO(4,1) -> SO(3,1)
# ----------------------------------------------------------------------------------------
ETA5 = (-1, 1, 1, 1, 1)


def J(A, B):
    return [[(1 if C == A else 0) * (ETA5[B] if D == B else 0) - (1 if C == B else 0) * (ETA5[A] if D == A else 0)
             for D in range(5)] for C in range(5)]


def tetrad_and_spin(x, f, fp):
    """Static spherical metric -f dt^2 + dr^2/f + r^2 dOmega^2: tetrad e^a_mu and the
    Levi-Civita spin connection omega^a_{b mu} (checked torsion-free below)."""
    t, r, th, ph = x
    sf = sqrt(f(r))
    E = [[sf, 0, 0, 0], [0, 1 / sf, 0, 0], [0, 0, r, 0], [0, 0, 0, r * sin(th)]]
    w = [[[0.0] * 4 for _ in range(4)] for _ in range(4)]   # w[a][b][mu]
    w[0][1][0] = w[1][0][0] = fp(r) / 2
    w[2][1][2], w[1][2][2] = sf, -sf
    w[3][1][3], w[1][3][3] = sf * sin(th), -sf * sin(th)
    w[3][2][3], w[2][3][3] = cos(th), -cos(th)
    return E, w


def connection(x, f, fp, l, with_e=True):
    E, w = tetrad_and_spin(x, f, fp)
    As = []
    for mu in range(4):
        A = [[0.0] * 5 for _ in range(5)]
        for a in range(4):
            for b in range(4):
                A[a][b] = w[a][b][mu]
        if with_e:
            for a in range(4):
                Ja4 = J(a, 4)
                for C in range(5):
                    for D in range(5):
                        A[C][D] += E[a][mu] / l * Ja4[C][D]
        As.append(A)
    return As


def curvature(x, f, fp, l, with_e=True, h=1e-5):
    A0 = connection(x, f, fp, l, with_e)
    dA = []
    for m in range(4):
        xp, xm = list(x), list(x)
        xp[m] += h
        xm[m] -= h
        Ap, Am = connection(xp, f, fp, l, with_e), connection(xm, f, fp, l, with_e)
        dA.append([mat_scale(mat_add(Ap[n], Am[n], -1), 1 / (2 * h)) for n in range(4)])
    return [[mat_add(mat_add(dA[m][n], dA[n][m], -1), comm(A0[m], A0[n])) for n in range(4)] for m in range(4)]


def eps4(p):
    if len(set(p)) < 4:
        return 0
    s = 1
    for i in range(4):
        for j in range(i + 1, 4):
            if p[i] > p[j]:
                s = -s
    return s


def wedge(X, Y):
    """eps_abcd X^ab ^ Y^cd, coefficient of dt dr dth dph."""
    tot = 0.0
    for a, b, c, d in permutations(range(4)):
        ea = eps4([a, b, c, d])
        for m, n, p, q in permutations(range(4)):
            tot += ea * eps4([m, n, p, q]) * X[a][b][m][n] * Y[c][d][p][q]
    return tot / 4


def rung5():
    banner("RUNG 5  Gravity as a broken gauge theory: MacDowell-Mansouri (an equivalent REFORMULATION)")
    plain("Einstein's gravity can be rewritten in the same broken-symmetry language as the other forces. This is a rewriting, not a new theory. Fed the measured dark energy, it lands on a famous open puzzle: why that number is about 10^122 times smaller than natural.")
    P = [J(a, 4) for a in range(4)]                        # translations, l = 1
    alg = all(comm(P[a], P[b]) == [[-ETA5[4] * x for x in row] for row in J(a, b)] for a in range(4) for b in range(4))
    V = [0, 0, 0, 0, 1]
    gens = [(A, B) for A in range(5) for B in range(A + 1, 5)]
    stab = [(A, B) for A, B in gens if mat_vec(J(A, B), V) == [0] * 5]
    check("so(4,1) = so(3,1) + 4 translations, [P_a, P_b] ~ J_ab / l^2; the de Sitter vector V = l e_4"
          " leaves the 6 Lorentz generators unbroken and breaks 4 (the tetrad: D V^a = e^a)",
          alg and len(stab) == 6 and all(B < 4 for _, B in stab))
    M_, l = 0.3, 7.0
    f_sds = lambda r: 1 - 2 * M_ / r - r * r / l**2
    fp_sds = lambda r: 2 * M_ / r**2 - 2 * r / l**2
    x = [0.2, 2.3, 1.1, 0.4]
    E, w = tetrad_and_spin(x, f_sds, fp_sds)
    hh = 1e-6
    tors = 0.0                                             # de^a + w^a_b e^b = 0
    for a in range(4):
        for m in range(4):
            for n in range(m + 1, 4):
                def e_at(mu, nu):
                    xp, xm = list(x), list(x)
                    xp[mu] += hh
                    xm[mu] -= hh
                    return (tetrad_and_spin(xp, f_sds, fp_sds)[0][a][nu] - tetrad_and_spin(xm, f_sds, fp_sds)[0][a][nu]) / (2 * hh)
                de = e_at(m, n) - e_at(n, m)
                we = sum(w[a][b][m] * E[b][n] - w[a][b][n] * E[b][m] for b in range(4))
                tors = max(tors, abs(de + we))
    Fm = curvature(x, f_sds, fp_sds, l, True)
    Rm = curvature(x, f_sds, fp_sds, l, False)
    split, torsion_block = 0.0, 0.0
    for m in range(4):
        for n in range(4):
            for a in range(4):
                for b in range(4):
                    ee = (E[a][m] * E[b][n] - E[a][n] * E[b][m]) * ETA4[b]
                    split = max(split, abs(Fm[m][n][a][b] - Rm[m][n][a][b] + ee / l**2))
                torsion_block = max(torsion_block, abs(Fm[m][n][a][4]))
    check("on a real spacetime (Schwarzschild-de Sitter): the spin connection is torsion-free, "
          "F^ab = R^ab - e^a^e^b / l^2 and F^a4 = T^a/l = 0", tors < 1e-7 and split < 1e-7 and torsion_block < 1e-7)
    f_ds = lambda r: 1 - r * r / l**2
    fp_ds = lambda r: -2 * r / l**2
    Fds = curvature(x, f_ds, fp_ds, l, True)
    check("the vacuum: de Sitter space of radius l is the flat SO(4,1) connection, F = 0, so Lambda = 3/l^2",
          max(abs(Fds[m][n][i][j]) for m in range(4) for n in range(4) for i in range(5) for j in range(5)) < 1e-7)
    Einv = [[0.0] * 4 for _ in range(4)]                   # e_a^mu (diagonal tetrad)
    for a in range(4):
        Einv[a][a] = 1 / E[a][a]
    ricF = max(abs(sum(Fm[m][n][a][b] * ETA4[b] * Einv[b][n] for b in range(4) for n in range(4)))
               for a in range(4) for m in range(4))
    f_s = lambda r: 1 - 2 * M_ / r
    fp_s = lambda r: 2 * M_ / r**2
    Fs = curvature(x, f_s, fp_s, l, True)
    Es, _ = tetrad_and_spin(x, f_s, fp_s)
    ricFs = max(abs(sum(Fs[m][n][a][b] * ETA4[b] / Es[b][n] for b in range(4) for n in range(4) if Es[b][n] != 0))
                for a in range(4) for m in range(4))
    check("field equations: the Ricci contraction of F vanishes for Schwarzschild-de Sitter (G + Lambda g = 0,"
          " Lambda = 3/l^2) and not for Schwarzschild without Lambda", ricF < 1e-6 and ricFs > 1e-3)
    Rup = [[[[Rm[m][n][a][b] * ETA4[b] for n in range(4)] for m in range(4)] for b in range(4)] for a in range(4)]
    EE = [[[[E[a][m] * E[b][n] - E[a][n] * E[b][m] for n in range(4)] for m in range(4)] for b in range(4)] for a in range(4)]
    e_det = E[0][0] * E[1][1] * E[2][2] * E[3][3]
    Rs = sum(Rm[m][n][a][b] * ETA4[b] * Einv[a][m] * Einv[b][n] for m in range(4) for n in range(4) for a in range(4) for b in range(4))
    cR = wedge(Rup, EE) / (e_det * Rs)
    cV = wedge(EE, EE) / e_det
    s = -1
    Lam = -(s**2 * cV) / (2 * (2 * s) * cR)                 # in units of 1/l^2
    print(f"   eps R^e^e = {cR:.6f} e R;  eps e^e^e^e = {cV:.6f} e;  Ricci scalar {Rs:.6f} (12/l^2 = {12 / l**2:.6f})")
    check("the action eps F^F = Euler + (2s/l^2) 2 e R + (1/l^4) 24 e gives e (R - 2 Lambda) with Lambda = 3/l^2;"
          " 1/(16 pi G) fixes N = -3/(64 pi G Lambda)", abs(cR - 2) < 1e-6 and abs(cV - 24) < 1e-9 and abs(Lam - 3) < 1e-6)
    ell = sqrt(3 / LAMBDA_SI)
    coup = 3 / (L_PLANCK**2 * LAMBDA_SI)
    print(f"   Measured Lambda: l = sqrt(3/Lambda) = {ell:.3e} m; MacDowell-Mansouri coupling 3/(G Lambda) = {coup:.2e} (Planck units)")
    check("the measured Lambda gives l = 1.65e26 m and a coupling of 1e122: the cosmological-constant problem",
          abs(ell / 1.647e26 - 1) < 1e-3 and abs(coup / 1.04e122 - 1) < 0.01, "pinned",
          f"got l = {ell:.4e} m and {coup:.3e}, pinned 1.647e26 m and 1.04e122")


# ----------------------------------------------------------------------------------------
# RUNG 6: black holes, the strong-field end of gravity's column (src/black_holes.py)
# ----------------------------------------------------------------------------------------
K_B = 1.380649e-23            # J/K
GM_SUN = 1.3271244e20         # m^3 s^-2, IAU 2015 nominal (Resolution B3; Prsa et al., arXiv:1510.07674)
PARSEC = 3.0856775814913673e16
UAS = pi / (180 * 3600e6)     # one micro-arcsecond in radians
# EHT ring diameters (uas, 68%): M87* (EHT 2019, ApJL 875, L1), Sgr A* (EHT 2022, ApJL 930, L12)
RING_M87, RING_SGRA = (42.0, 3.0), (51.8, 2.3)
# The EHT's theta_g = GM/(c^2 D) (uas; value, error below, error above), from the ring with
# alpha = d/theta_g calibrated on GRMHD images, the calibration's spread included (same
# papers; M87*: Paper VI, ApJL 875, L6). alpha = 11.1 and 10.8, against the shadow's 10.4.
THETA_G_M87, THETA_G_SGRA = (3.8, 0.4, 0.4), (4.8, 0.7, 1.4)   # EHT 2019 Paper VI; EHT 2022 Paper I, Table 1
# Masses and distances measured without the EHT. M87*: stellar dynamics (Gebhardt et al.,
# ApJ 729, 119 (2011)), (6.6 +- 0.4)e9 Msun at an assumed 17.9 Mpc; M/D does not depend on
# the distance assumed. Sgr A*: stellar orbits, GRAVITY 2022 and Keck 2019 (Msun, pc).
M87_STARS = (6.6e9, 0.4e9, 17.9e6)
SGRA_VLTI, SGRA_KECK = (4.297e6, 8277.0), (3.975e6, 7959.0)   # Keck: Do et al. 2019, Table 1, R0 = 7.959 kpc
# GW250114 (LVK, PRL 135, 111403 (2025)): component masses (Msun, +-90%), full-signal
# remnant, redshift; the ringdown-only 220 fit (redshifted f, damping rate, Hz). The spin
# bound chi_1,2 <= 0.26 is not needed: spin 0 gives the largest initial area.
GW_M1, GW_M2 = (33.6, 0.8, 1.2), (32.2, 1.3, 0.8)
GW_MF, GW_CHIF, GW_Z = 62.7, 0.68, (0.09, 0.01)
F220, G220 = (247.0, 6.0, 6.0), (221.0, 32.0, 39.0)
BCW_220 = (1.5251, -1.1568, 0.1292, 0.7000, 1.4187, -0.4990)   # Berti, Cardoso, Will (2006)


class Dual:
    """a + b eps with eps^2 = 0, over exact Fractions: exact derivatives of rational functions."""
    def __init__(self, a, b=0):
        self.a, self.b = F(a), F(b)

    def _w(self, o):
        return o if isinstance(o, Dual) else Dual(o)

    def __add__(self, o):
        o = self._w(o)
        return Dual(self.a + o.a, self.b + o.b)
    __radd__ = __add__

    def __sub__(self, o):
        o = self._w(o)
        return Dual(self.a - o.a, self.b - o.b)

    def __rsub__(self, o):
        return self._w(o) - self

    def __mul__(self, o):
        o = self._w(o)
        return Dual(self.a * o.a, self.a * o.b + self.b * o.a)
    __rmul__ = __mul__

    def __truediv__(self, o):
        o = self._w(o)
        return Dual(self.a / o.a, (self.b * o.a - self.a * o.b) / (o.a * o.a))


def kerr_first_law(p, q):
    """Kerr in its horizon radii r+ = p, r- = q (G = c = 1): M = (p+q)/2, a^2 = pq,
    S = pi (p^2 + a^2), T = (p - q)/(4 pi (p^2 + a^2)), Omega = a/(p^2 + a^2), J = M a
    (horizon quantities LIT: Bardeen-Carter-Hawking 1973). pi cancels in T dS and T S, and
    Omega dJ = (a^2 dM + M d(a^2)/2)/(p^2 + a^2) needs only a^2, so everything is rational.
    p, q are Duals; returns dM - T dS - Omega dJ (the eps part) and M - 2TS - 2 Omega J."""
    m, a2 = (p + q) / 2, p * q
    s_pi = p * p + a2                                        # S / pi
    t_pi = (p - q).a / (4 * s_pi.a)                          # pi T
    first = m.b - t_pi * s_pi.b - (a2.a * m.b + m.a * a2.b / 2) / s_pi.a
    smarr = m.a - 2 * t_pi * s_pi.a - 2 * m.a * a2.a / s_pi.a
    return first, smarr


def sds_horizons(M_, l):
    """Black-hole and cosmological horizons of f = 1 - 2M/r - r^2/l^2, by bisection."""
    Fn = lambda x: x - 2 * M_ - x**3 / l**2
    rm = l / sqrt(3)
    def bis(a, b):
        for _ in range(200):
            m = (a + b) / 2
            a, b = (m, b) if (Fn(a) > 0) == (Fn(m) > 0) else (a, m)
        return (a + b) / 2
    return (bis(2 * M_, rm), bis(rm, l)) if Fn(rm) > 0 else None


def killing_kappa(f, r0, h):
    """Surface gravity from the Killing vector xi = d/dt: kappa^2 = -1/2 (nabla_mu xi_nu)
    (nabla^mu xi^nu), at radius r0. The Christoffel symbols come from central differences
    of the metric diag(-f, 1/f, r^2, r^2 sin^2 th) alone: f, never f', and not the tetrad."""
    x0 = [0.0, r0, 1.0, 0.0]
    gfun = lambda x: [-f(x[1]), 1 / f(x[1]), x[1] ** 2, (x[1] * sin(x[2])) ** 2]
    g0, dg = gfun(x0), []                                        # dg[c][a] = d_c g_aa
    for c in range(4):
        xp, xm = list(x0), list(x0)
        xp[c] += h
        xm[c] -= h
        gp, gm = gfun(xp), gfun(xm)
        dg.append([(gp[a] - gm[a]) / (2 * h) for a in range(4)])
    def gam(a, b, c):                                            # Gamma^a_bc, diagonal metric
        return ((dg[b][a] if a == c else 0) + (dg[c][a] if a == b else 0) - (dg[a][b] if b == c else 0)) / (2 * g0[a])
    D = [[(dg[m][0] if n == 0 else 0) - gam(0, m, n) * g0[0] for n in range(4)] for m in range(4)]
    return sqrt(-sum(D[m][n] ** 2 / (g0[m] * g0[n]) for m in range(4) for n in range(4)) / 2)


def euclidean_cone(f, rh, beta, eps):
    """Circumference over 2 pi x proper radius of the Euclidean (tau, r) circle at r_h + eps,
    for a tau-period beta: 1 if the plane is smooth there, otherwise a cone.
    rho = int dr/sqrt(f), with r = r_h + u^2 so the integrand is finite; the midpoint rule
    never evaluates the endpoint, so this uses f only."""
    n = 400
    h, s = sqrt(abs(eps)) / n, (1 if eps > 0 else -1)
    rho = h * sum(2 * u / sqrt(abs(f(rh + s * u * u))) for u in ((k + 0.5) * h for k in range(n)))
    return beta * sqrt(abs(f(rh + eps))) / (2 * pi * rho)


def golden_max(fn, a, b, it=200):
    g = (sqrt(5) - 1) / 2
    for _ in range(it):
        c, d = b - g * (b - a), a + g * (b - a)
        a, b = (a, d) if fn(c) > fn(d) else (c, b)
    return (a + b) / 2


def shadow_uas(m_sun, d_pc):
    """Schwarzschild shadow diameter 2 sqrt(27) GM/(c^2 D), micro-arcseconds."""
    return 2 * sqrt(27) * m_sun * GM_SUN / C_LIGHT**2 / (d_pc * PARSEC) / UAS


def theta_g_pull(pred, pred_rel_err, meas):
    """(measured - predicted)/sigma, with the measured error on the side facing the prediction."""
    val, lo, hi = meas
    return (val - pred) / sqrt((hi if pred > val else lo) ** 2 + (pred * pred_rel_err) ** 2)


def kerr_area_km2(m_sun, chi):
    rg = m_sun * GM_SUN / C_LIGHT**2 / 1e3
    return 8 * pi * rg * rg * (1 + sqrt(1 - chi * chi))


def qnm_220(m_det_sun, chi):
    f1, f2, f3, q1, q2, q3 = BCW_220
    omega = (f1 + f2 * (1 - chi) ** f3) / (m_det_sun * GM_SUN / C_LIGHT**3)
    return omega / (2 * pi), omega / (2 * (q1 + q2 * (1 - chi) ** q3))


def invert_220(freq, damp, z):
    """Remnant mass (source frame) and spin from the 220 frequency and damping rate alone."""
    f1, f2, f3, q1, q2, q3 = BCW_220
    chi = 1 - ((pi * freq / damp - q1) / q2) ** (1 / q3)
    m_det = (f1 + f2 * (1 - chi) ** f3) / (2 * pi * freq * GM_SUN / C_LIGHT**3)
    return m_det / (1 + z), chi


def hawking_K(m_kg):
    return HBAR * C_LIGHT**3 / (8 * pi * G_NEWTON * m_kg * K_B)


def rung6():
    banner("RUNG 6  Black holes: the strong-field end of gravity's column (not a symmetry breaking)")
    plain("a black hole is not a place where a symmetry breaks, so this is not a new step down the chain. It is gravity at its strongest, and the first formula here that needs quantum physics, gravity, relativity and heat at once: the Hawking temperature. The geometry fixes that temperature, and telescopes and gravitational waves test the geometry. Hawking radiation itself has never been measured.")
    # H1: kappa from the Killing vector d/dt, on both Schwarzschild-de Sitter horizons. The
    # Christoffels come from the metric (f only); f'/2 is computed only to compare. The
    # invariant is evaluated just on the static side of each horizon (offset 1e-6 r_h).
    M_, l = 1.0, 9.0                                       # 27 M^2/l^2 = 1/3
    f = lambda r: 1 - 2 * M_ / r - r * r / l**2
    fp = lambda r: 2 * M_ / r**2 - 2 * r / l**2
    rb, rc = sds_horizons(M_, l)
    kap = [killing_kappa(f, rh + side * 1e-6 * rh, 1e-8 * rh) for rh, side in ((rb, 1), (rc, -1))]
    k_schw = killing_kappa(lambda r: 1 - 2 / r, 2.0 + 2e-6, 2e-8)
    # cross-check: rung 5's spin connection (validated there by its torsion-free check)
    _, w = tetrad_and_spin([0.0, rb + 1e-9, 1.0, 0.0], f, fp)
    print(f"   SdS (M = 1, l = 9): horizons r_b = {rb:.6f}, r_c = {rc:.6f}; Killing kappa = {kap[0]:.6f}, {kap[1]:.6f}"
          f" (|f'|/2 = {fp(rb) / 2:.6f}, {-fp(rc) / 2:.6f}; rung 5's omega^0_(1t) = {w[0][1][0]:.6f})."
          f" Schwarzschild: kappa = {k_schw:.7f} = 1/(4M)")
    check("horizon f(r_h) = 0 and surface gravity from the Killing vector d/dt, kappa^2 = -(nabla xi)^2/2,"
          " equal to |f'(r_h)|/2 on both SdS horizons and 1/(4M) for Schwarzschild; T_H = hbar c kappa/(2 pi k_B)",
          abs(f(rb)) < 1e-12 and abs(f(rc)) < 1e-12 and abs(kap[0] / (fp(rb) / 2) - 1) < 1e-5
          and abs(kap[1] / (-fp(rc) / 2) - 1) < 1e-5 and abs(k_schw / 0.25 - 1) < 1e-5)
    # H2: the Euclidean section is smooth only for tau-period 2 pi / kappa. rho comes from f
    # alone. The ratio is linear in the period, so a period 10% off would prove nothing; the
    # discriminating case is a period from a different f: Schwarzschild's 8 pi M, ignoring Lambda.
    ratios = [euclidean_cone(f, rh, 2 * pi / k, s * 1e-7 * rh) for rh, k, s in zip((rb, rc), kap, (1, -1))]
    wrong = euclidean_cone(f, rb, 8 * pi * M_, 1e-7 * rb)
    print(f"   circumference/(2 pi rho) near each horizon: {ratios[0]:.7f}, {ratios[1]:.7f} for beta = 2 pi/kappa;"
          f" {wrong:.4f} at the SdS black-hole horizon for Schwarzschild's period 8 pi M (a cone)")
    check("Euclidean time: the (tau, r) plane is smooth at a horizon only if tau has period 2 pi/kappa, so"
          " T = kappa/2 pi is fixed by the geometry; the two SdS horizons need different periods, and"
          " Schwarzschild's period leaves a cone in SdS",
          all(abs(x - 1) < 1e-5 for x in ratios) and abs(kap[0] / kap[1] - 1) > 0.5 and abs(wrong - 1) > 0.1)
    # H3: first law and Smarr, exact (Kerr; q = 0 is Schwarzschild: dM = T dS, M = 2TS)
    rng, ok = random.Random(6), True
    for k in range(60):
        p = F(rng.randint(1, 400), rng.randint(1, 40))
        q = F(0) if k < 10 else p * F(rng.randint(0, 99), 100)
        for dp, dq in ((1, 0), (0, 1)):
            first, smarr = kerr_first_law(Dual(p, dp), Dual(q, dq))
            ok &= first == 0 and smarr == 0
    check("black-hole thermodynamics with S = A/4 l_P^2, in exact fractions: dM = T dS + Omega dJ and"
          " M = 2TS + 2 Omega J for Kerr; dM = T dS and M = 2TS for Schwarzschild (60 random horizons)", ok)
    # H4: Nariai limit, exactly and as a limit of the two temperatures
    Mq = F(5, 7)
    fN = lambda r: 1 - 2 * Mq / r - r * r / (27 * Mq * Mq)
    fpN = lambda r: 2 * Mq / r**2 - 2 * r / (27 * Mq * Mq)
    exact = fN(3 * Mq) == 0 and fpN(3 * Mq) == 0 and 9 * Mq * Mq * (F(3) / (27 * Mq * Mq)) == 1
    lim = []
    for x in (0.9, 0.99, 0.9999):
        lx = sqrt(27 / x)
        b, c = sds_horizons(1.0, lx)
        lim.append((b, c, (2 / b**2 - 2 * b / lx**2) / 2, -(2 / c**2 - 2 * c / lx**2) / 2))
    print("   27M^2/l^2 -> 1: " + "; ".join(f"r = {b:.3f}, {c:.3f}, kappa = {kb:.4f}, {kc:.4f}" for b, c, kb, kc in lim))
    check("Schwarzschild-de Sitter: the two horizons and their temperatures merge at the Nariai limit,"
          " f = f' = 0 at r = 3M when 9 G^2 M^2 Lambda = c^4 (exact); beyond it there is no static region",
          exact and abs(lim[-1][0] - 3) < 0.02 and abs(lim[-1][1] - 3) < 0.02 and lim[-1][2] < 0.002
          and lim[-1][3] < 0.002 and sds_horizons(1.0, sqrt(27 / 1.01)) is None)
    m_n = C_LIGHT**2 / (3 * G_NEWTON * sqrt(LAMBDA_SI))
    print(f"   rung 5's measured Lambda: the largest black hole is M = c^2/(3 G sqrt(Lambda)) = {m_n:.3e} kg"
          f" = {m_n * G_NEWTON / GM_SUN:.2e} M_sun, horizon at 1/sqrt(Lambda) = {1 / sqrt(LAMBDA_SI):.2e} m")
    check("with rung 5's Lambda, the largest black hole the universe allows: 4.27e52 kg = 2.1e22 solar masses",
          abs(m_n / 4.269e52 - 1) < 1e-3, "pinned", f"got {m_n:.4e} kg, pinned 4.269e52 kg")
    # H5: geodesics from the effective potentials (M = 1), found numerically
    rph = golden_max(lambda r: (1 - 2 / r) / r**2, 2.01, 20)
    bc = 1 / sqrt((1 - 2 / rph) / rph**2)
    check("photons: the potential f/r^2 peaks at the photon sphere r = 3GM/c^2; the critical impact"
          " parameter, the shadow radius seen from far away, is sqrt(27) GM/c^2",
          abs(rph - 3) < 1e-7 and abs(bc - sqrt(27)) < 1e-10)
    dV = lambda r, L2: 2 / r**2 * (1 + L2 / r**2) - (1 - 2 / r) * 2 * L2 / r**3
    # Circular orbits exist where dV/dr = 0; they exist iff min_r dV/dr <= 0. Bisect on L^2.
    min_dV = lambda L2: golden_max(lambda r: -dV(r, L2), 4, 9)      # the dip of dV/dr near 6M
    lo, hi = 10.0, 14.0
    for _ in range(60):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if dV(min_dV(mid), mid) > 0 else (lo, mid)
    r_isco = min_dV(hi)                                    # where the two orbits merge
    E2 = (1 - 2 / r_isco) * (1 + hi / r_isco**2)
    print(f"   photon sphere r = {rph:.8f} M, shadow radius {bc:.8f} M; ISCO r = {r_isco:.5f} M,"
          f" L^2 = {hi:.6f} M^2, E^2 = {E2:.6f}")
    check("massive particles: circular orbits exist for L^2 >= 12 (GM/c)^2; at that minimum the stable and"
          " unstable orbits merge at the innermost stable circular orbit, r = 6GM/c^2, with E^2 = 8/9",
          abs(hi - 12) < 1e-6 and abs(r_isco - 6) < 1e-3 and abs(E2 - 8 / 9) < 1e-6)
    # H6: Event Horizon Telescope. The EHT measures a ring, not the shadow, and converts it to
    # theta_g = GM/(c^2 D) with a GRMHD-calibrated alpha = ring/theta_g; that conversion is the
    # ring-to-shadow correction, and its spread is in the EHT's error. Compare theta_g.
    k = 2 * sqrt(27)                                       # shadow diameter / theta_g
    p87 = shadow_uas(M87_STARS[0], M87_STARS[2])
    z87 = theta_g_pull(p87 / k, M87_STARS[1] / M87_STARS[0], THETA_G_M87)
    gas = shadow_uas(3.5e9, M87_STARS[2]) / k
    check("M87*: theta_g = GM/(c^2 D) from the stellar-dynamics mass is 3.64 uas (shadow 37.8 uas); the EHT's,"
          " from its 42 +- 3 uas ring, is 3.8 +- 0.4 uas", abs(z87) < 2, "data",
          f"got {p87 / k:.2f} uas, {z87:+.2f} sigma (shadow {p87:.1f} uas). Tolerance 2 sigma: the EHT's error, which"
          f" holds the ring (7%) and its GRMHD calibration alpha = {RING_M87[0] / THETA_G_M87[0]:.1f} against the"
          " Schwarzschild shadow's 10.4, and the mass (6%; the distance cancels in M/D). The gas-dynamics mass"
          f" (3.5e9) would give {gas:.2f} uas, {theta_g_pull(gas, 0, THETA_G_M87):+.1f} sigma, excluded")
    pv, pk = shadow_uas(*SGRA_VLTI), shadow_uas(*SGRA_KECK)
    pS = (pv + pk) / 2
    zS = theta_g_pull(pS / k, abs(pv - pk) / pS, THETA_G_SGRA)
    check("Sgr A*: theta_g from the stellar-orbit mass and distance is 5.03 uas (shadow 52.2 uas); the EHT's,"
          " from its 51.8 +- 2.3 uas ring, is 4.8 (-0.7 +1.4) uas", abs(zS) < 2, "data",
          f"got {pS / k:.2f} uas (GRAVITY {pv / k:.2f}, Keck {pk / k:.2f}), {zS:+.2f} sigma. Tolerance 2 sigma: the EHT's"
          f" upper error (alpha = {RING_SGRA[0] / THETA_G_SGRA[0]:.1f}, calibration included) and the GRAVITY-Keck"
          " spread in M/D (4%)")
    # H7: GW250114. The final area comes from the ringdown alone, not the full-signal fit,
    # which assumes GR and obeys the area law by construction.
    z, dz = GW_Z
    a_i = kerr_area_km2(GW_M1[0], 0) + kerr_area_km2(GW_M2[0], 0)
    a_i_max = kerr_area_km2(GW_M1[0] + GW_M1[2], 0) + kerr_area_km2(GW_M2[0] + GW_M2[2], 0)
    mf, chif = invert_220(F220[0], G220[0], z)
    a_f = kerr_area_km2(mf, chif)
    a_f_min = min(kerr_area_km2(*invert_220(fq, gq, zq)) for fq in (F220[0] - F220[1], F220[0] + F220[2])
                  for gq in (G220[0] - G220[1], G220[0] + G220[2]) for zq in (z - dz, z + dz))
    print(f"   GW250114 ringdown alone: M_f = {mf:.1f} M_sun, chi_f = {chif:.2f}. Areas (A = 8 pi (GM/c^2)^2 (1 +"
          f" sqrt(1 - chi^2))): initial {a_i:,.0f} km^2, final {a_f:,.0f} km^2")
    check("GW250114, Hawking's area law: final area 4.1e5 km^2 > initial 2.4e5 km^2, from the published"
          " masses and the ringdown-only fit", a_f_min > a_i_max, "data",
          f"least favourable corners of the published 90% ranges: initial {a_i_max:,.0f} km^2 (spins 0, which"
          f" maximizes it), final {a_f_min:,.0f} km^2; a heuristic, not a bound, as the area need not be monotonic"
          " in (f, gamma). The collaboration finds A_f > A_i at > 4 sigma at all analysis points (arXiv:2509.08054)")
    f220, g220 = qnm_220((1 + z) * GW_MF, GW_CHIF)
    check("GW250114: the full-signal remnant predicts a 220 mode at 249 Hz, damping 244 Hz; the ringdown"
          " alone measures 247 +- 6 Hz and 221 (-32 +39) Hz",
          abs(f220 - F220[0]) < 2 * F220[1] and G220[0] - 2 * G220[1] < g220 < G220[0] + 2 * G220[2], "data",
          f"got {f220:.1f} Hz and {g220:.0f} Hz. Tolerance: twice the published 90% intervals; the fit formula is"
          " good to a few per cent, and z = 0.09 +- 0.01 moves f by 1%")
    print(f"   Hawking temperature of the remnant: {hawking_K(GW_MF * GM_SUN / G_NEWTON):.1e} K, far below the"
          " 2.7 K microwave background: unmeasured")


# ----------------------------------------------------------------------------------------
# LINKS between the rungs (src/ladder_links.py)
# ----------------------------------------------------------------------------------------
U_AMU = 1.66053906660e-27     # kg; carbon-12: 12 u for 12 nucleons
K_COUL = 8.9875517923e9       # 1/(4 pi eps0)
E_CH = 1.602176634e-19        # C
ALPHA_0 = 1 / 137.035999084   # alpha at q^2 = 0 (real photons)
EPS_PE_BOUND = 1e-21          # |q_p + q_e|/e, Bressi et al., PRA 83, 052101 (2011); same for q_n
GAMMA_PI0 = (7.802, sqrt(0.052**2 + 0.105**2))   # eV, PrimEx-I+II, Larin et al., Science 368, 506 (2020)


def baryons(Qu, Qd, Nc):
    """The N_c-quark proton ((N_c+1)/2 u, (N_c-1)/2 d) and neutron (the reverse)."""
    up, dn = F(Nc + 1, 2), F(Nc - 1, 2)
    return up * Qu + dn * Qd, dn * Qu + up * Qd


def parity(p):
    p, s = list(p), 1
    for i in range(len(p)):
        while p[i] != i:
            j = p[i]
            p[i], p[j] = p[j], p[i]
            s = -s
    return s


def links():
    banner("LINKS  Where one rung's output is another rung's input")
    plain("places where one rung's result is needed by another. For example, the diamond experiment needs matter to be electrically neutral to extreme precision, and rung 1 explains why it is exactly neutral.")
    # L1a: q_p + q_e is the [SU(3)_L]^2 U(1)_X anomaly, for any beta, N_c and X charges.
    # b = beta/(2 sqrt3) enters linearly, so exact random rationals test the identity.
    rng, ok = random.Random(331), True
    for _ in range(200):
        Nc = rng.choice((3, 5, 7, 9, 11))
        b, XL, Xt = (F(rng.randint(-60, 60), rng.randint(1, 30)) for _ in range(3))
        Xa = Xt + 2 * b                                   # u, d the same in triplet and anti-triplet
        Qu, Qd = F(1, 2) + b + Xt, F(-1, 2) + b + Xt
        ok &= (F(1, 2) - b + Xa, F(-1, 2) - b + Xa) == (Qu, Qd)
        Qnu, Qe = F(1, 2) + b + XL, F(-1, 2) + b + XL
        Ng, n = Nc, F(Nc * (1 + Nc), 2 * Nc)              # SU(3)_L^3: N_g(1 + N_c) = 2 n N_c
        anomaly = Ng * XL + Nc * ((Ng - n) * Xt + n * Xa)
        qp, qn = baryons(Qu, Qd, Nc)
        ok &= qp + Qe == anomaly / Ng and qn + Qnu == qp + Qe
    check("neutral matter is an anomaly: q_p + q_e = [SU(3)_L]^2 U(1)_X / N_g and q_n + Q_nu = q_p + q_e,"
          " for any beta, N_c, X (200 exact random cases)", ok)
    # L1b: rung 1's charges
    ok = True
    for variant in ("-1/sqrt3", "+1/sqrt3"):
        for Nc in (3, 5, 7):
            ferm, _, Qu, Qd = model(Nc, variant)
            lep = triplet_charges(ferm[0][3], variant)
            qp, qn = baryons(Qu, Qd, Nc)
            ok &= (qp, qn, lep[1], lep[0]) == (1, 0, -1, 0)
    check("rung 1's charges: q_p = 1, q_n = 0, q_e = -1, Q_nu = 0 exactly, both variants, N_c = 3, 5, 7", ok)
    # L1c-d: design A
    m = geomspace(1e-16, 1e-12, 25)[13]
    nucleons = m / U_AMU
    one_e = K_COUL * E_CH**2 / (G_NEWTON * m * m)        # same 1/r, same trajectories: exact ratio
    delta_max = sqrt(0.1 * G_NEWTON / K_COUL) * m / E_CH / nucleons
    margin = delta_max / EPS_PE_BOUND
    print(f"   Design A ({nucleons:.3e} nucleons): one stray electron each = {one_e:.2e} x gravity's phase;")
    print(f"   Coulomb < 10% of gravity needs < {delta_max:.2e} e per nucleon, for any diamond size")
    print(f"   Measured: |q_p + q_e|, |q_n| < 1e-21 e -> margin {margin:.0f}; that residual totals"
          f" {EPS_PE_BOUND * nucleons:.1e} e per diamond, below one electron, so discharging cannot reach it")
    check("design A: one electron = 1.6e10 x gravity (as H6); neutrality needed to 2.8e-19 e per nucleon,"
          " a margin of 282 over the measured bound",
          abs(one_e / 1.60e10 - 1) < 0.01 and abs(delta_max / 2.82e-19 - 1) < 2e-3 and abs(margin / 282 - 1) < 2e-3,
          "pinned", f"got {one_e:.3e}, {delta_max:.3e} e and {margin:.1f}, pinned 1.60e10, 2.82e-19 e and 282")
    check("measured neutrality (1e-21 e) is tighter than design A needs; rung 1 makes it exact",
          margin > 1, "data",
          f"got margin {margin:.0f}. Passes if the measured bound is tighter than the requirement"
          " (margin > 1), nothing more; the value is pinned in the check above")
    # L2: pi0 -> gamma gamma
    factors = [Nc * (F(Nc + 1, 2 * Nc) ** 2 - F(1 - Nc, 2 * Nc) ** 2) for Nc in range(1, 12)]
    check("pi0 -> gamma gamma: N_c (Q_u^2 - Q_d^2) = 1 for every N_c with rung 1's charges", set(factors) == {1})
    mpi = 1.0                                             # |M|^2 in units of A^2 m^4
    k1, k2 = (mpi / 2, 0, 0, mpi / 2), (mpi / 2, 0, 0, -mpi / 2)
    low = lambda v: (v[0], -v[1], -v[2], -v[3])
    msq = 0.0
    for e1 in ((0, 1, 0, 0), (0, 0, 1, 0)):
        for e2 in ((0, 1, 0, 0), (0, 0, 1, 0)):
            vs = (low(e1), low(e2), low(k1), low(k2))
            M = sum(parity(p) * vs[0][p[0]] * vs[1][p[1]] * vs[2][p[2]] * vs[3][p[3]] for p in permutations(range(4)))
            msq += M * M
    A = ALPHA_0 / (pi * F_PI)
    width = 0.5 * (M_PI0 / 2) / (8 * pi * M_PI0**2) * msq * A**2 * M_PI0**4 * 1e9    # eV
    pull = (width - GAMMA_PI0[0]) / GAMMA_PI0[1]
    print(f"   sum |M|^2 = {msq:.3f} A^2 m^4 -> Gamma = A^2 m^3/(64 pi) = {width:.3f} eV"
          f"  (PrimEx-I+II {GAMMA_PI0[0]} +- {GAMMA_PI0[1]:.3f} eV, {pull:+.1f} sigma)")
    print(f"   f_pi = {F_PI * 1e3:.2f} MeV is a measured input (PDG), not derived by rung 2. What the match tests")
    print("   is the anomaly normalization N_c (Q_u^2 - Q_d^2) = 1 that rung 1's charges give.")
    print("   With the charges held at 2/3, -1/3 the width would scale as (N_c/3)^2; with rung 1's it")
    print("   cannot select N_c, the R-ratio does (src/m331_why_three.py W6).")
    check("pi0 width from rung 1's charges and the measured f_pi: 7.79 eV, within 2 sigma of PrimEx",
          abs(msq - 0.5) < 1e-12 and abs(width - 7.785) < 2e-3 and abs(pull) < 2, "data",
          f"got {width:.3f} eV vs {GAMMA_PI0[0]} +- {GAMMA_PI0[1]:.3f} eV ({pull:+.1f} sigma). Tolerance 2 sigma,"
          " the usual standard. This is leading order (the anomaly alone); next-order"
          " corrections of a few percent are not included")
    # L3: the 3-3-1 selection's cutoff is sqrt(hbar c / G), with rung 4's G
    mpl = sqrt(HBAR * C_LIGHT / G_NEWTON) * C_LIGHT**2 / E_CH / 1e9
    print(f"   M_Pl = sqrt(hbar c / G) from rung 4's G = {mpl:.6e} GeV: the cutoff the 3-3-1 selection runs to")
    check("the 3-3-1 cutoff is rung 4's gravity: sqrt(hbar c / G) = 1.22089e19 GeV",
          abs(mpl / 1.22089e19 - 1) < 1e-6, "pinned", f"got {mpl:.6e} GeV, pinned 1.22089e19 GeV")
    # L3b: what the selection needs from G. It keeps N_c = 3 and excludes N_c = 5 while
    # pole_5 < M_Pl < pole_3. G -> x G moves M_Pl by x^(-1/2), so it holds for
    # (M_Pl/pole_3)^2 < x < (M_Pl/pole_5)^2, with M_Pl from rung 4's G.
    win = {}
    for v, (p3, p5) in POLES_331.items():
        win[v] = ((mpl / p3) ** 2, (mpl / p5) ** 2)
        print(f"   beta = {v:8s}: N_c = 3 pole {p3 / mpl:.3g} M_Pl, N_c = 5 pole {p5 / mpl:.2g} M_Pl"
              f" -> holds for {win[v][0]:.2g} < G/G_meas < {win[v][1]:.2g}")
    print("   G is measured to 2.2e-5 (CODATA 2018). The assumption: G does not run between the")
    print("   laboratory and 10^19 GeV (corrections ~ (E/M_Pl)^2; many hidden light species would break it).")
    check("with rung 4's G the 3-3-1 selection keeps N_c = 3 and excludes N_c = 5; it would fail for G 8.4x weaker",
          all(lo < 1 < hi for lo, hi in win.values()) and abs(1 / win["+1/sqrt3"][0] / 8.37 - 1) < 0.01,
          "pinned", f"got windows {', '.join(f'{lo:.3g}-{hi:.2g}' for lo, hi in win.values())},"
          " pinned 0.12 (8.4x weaker) as the narrow side. The poles come from src/m331_three_loop.py")
    # L3e: the reference spectrum is one point. Over the threshold scan the window narrows.
    wscan = {}
    for v, (p3, p5) in POLES_331_SCAN.items():
        wscan[v] = ((mpl / p3) ** 2, (mpl / p5) ** 2)
        print(f"   beta = {v:8s}, worst over the threshold scan: N_c = 3 pole {p3 / mpl:.3g} M_Pl, N_c = 5 pole"
              f" {p5 / mpl:.2g} M_Pl -> holds for {wscan[v][0]:.2g} < G/G_meas < {wscan[v][1]:.2g}")
    check("over the threshold scan the selection still holds at the measured G, but would fail for G 1.6x weaker",
          all(lo < 1 < hi for lo, hi in wscan.values()) and abs(1 / wscan["+1/sqrt3"][0] / 1.629 - 1) < 0.01,
          "pinned", f"got windows {', '.join(f'{lo:.3g}-{hi:.2g}' for lo, hi in wscan.values())},"
          " pinned 0.61 (1.6x weaker) as the narrow side, at M_V = 2 TeV, r_J = 0.5, r_S = 1/3 and two light"
          " doublets. The 8.4x above is the reference spectrum's margin, not the model's. Gravity's own term in the"
          " running moves these poles by 3% or less (src/ladder_links.py L3f)")
    # L4: rung 6 -> rung 4. Design A's diamond as a black hole.
    rs = 2 * G_NEWTON * m / C_LIGHT**2
    print(f"   Design A's diamond ({m:.3e} kg): Schwarzschild radius 2Gm/c^2 = {rs:.2e} m = {rs / L_PLANCK:.2e} l_P,"
          f" {rs / diamond_radius(m):.0e} of its own radius")
    check("design A's diamond has a Schwarzschild radius of 2.2e-41 m, a millionth of the Planck length:"
          " the experiment's gravity is that weak", abs(rs / 2.180e-41 - 1) < 1e-3 and abs(rs / L_PLANCK / 1.349e-6 - 1) < 1e-3,
          "pinned", f"got {rs:.4e} m = {rs / L_PLANCK:.4e} l_P, pinned 2.180e-41 m and 1.349e-6 l_P")
    # L5: rung 6 -> link 3. A black hole of one Planck mass.
    m_pl = sqrt(HBAR * C_LIGHT / G_NEWTON)
    kT = K_B * hawking_K(m_pl) / E_CH / 1e9
    rs_pl = 2 * G_NEWTON * m_pl / C_LIGHT**2 / sqrt(HBAR * G_NEWTON / C_LIGHT**3)
    print(f"   A black hole of one Planck mass: k_B T_H = {kT:.3e} GeV = M_Pl c^2 / 8 pi; radius {rs_pl:.4f} l_P."
          " At that size the semiclassical formula is no longer trusted")
    check("a black hole of one Planck mass has k_B T_H = M_Pl c^2/(8 pi) = 4.86e17 GeV, 1/(8 pi) of the"
          " 3-3-1 cutoff, and a radius of 2 Planck lengths", abs(kT * 8 * pi / mpl - 1) < 1e-12 and abs(rs_pl - 2) < 1e-12)


def main():
    t0 = time.time()
    for rung in (rung1, rung2, rung3, rung4, rung5, rung6, links):
        rung()
    banner("VERDICT")
    n_ok = sum(ok for _, ok, _ in CHECKS)
    print("   3-3-1 breaks to the Standard Model and then to electromagnetism: the photon, hypercharge,")
    print("   W, Z and Z' follow from the vacuum values. Chiral symmetry breaking gives the pions and the")
    print("   nuclear force. Electromagnetism, never broken, leaves the Casimir-Polder background between")
    print("   the diamonds. Gravity sits beside the chain: one-graviton exchange gives Newton's law and the")
    print("   experiment's 2.19 rad phase, and MacDowell-Mansouri writes GR + Lambda as SO(4,1) broken")
    print("   to Lorentz. Black holes are gravity's strong-field end: the geometry fixes their temperature,")
    print("   and the EHT shadows and GW250114's area increase test that geometry; Hawking radiation itself")
    print("   is unmeasured, and whether information is lost is open.")
    print("   Five links run across the gauge chain and gravity: rung 1's anomalies make matter neutral, which")
    print("   the diamond experiment needs to 2.8e-19 e per nucleon; its charges with rung 2's f_pi give")
    print("   the measured pi0 -> gamma gamma width; the 3-3-1 cutoff, M_Pl, is rung 4's G, which")
    print("   the selection needs within a factor 8.4 (it is measured to 2e-5); rung 6 puts the diamond's")
    print("   Schwarzschild radius at a millionth of the Planck length; and a black hole of one Planck")
    print("   mass has k_B T_H = M_Pl c^2/8 pi, 1/(8 pi) of the 3-3-1 cutoff, where the formula is no")
    print("   longer trusted. Inputs")
    print("   are measured; gravity's unification with the other forces is not derived. Rung 2's")
    print("   pion counting uses the linear sigma model, a stand-in for QCD, and rung 5 rewrites GR")
    print("   rather than going beyond it.")
    by_kind = ", ".join(f"{sum(k == kind for _, _, k in CHECKS)} {kind}" for kind in KINDS)
    print(f"\n   Checks passed: {n_ok}/{len(CHECKS)}   ({by_kind}; {time.time() - t0:.2f} s)")
    for label, ok, _ in CHECKS:
        if not ok:
            print(f"   FAILED: {label}")
    print("   ALL CHECKS PASS" if n_ok == len(CHECKS) else "   SOME CHECKS FAILED")
    return n_ok == len(CHECKS)


if __name__ == "__main__":
    if not main():
        raise SystemExit(1)       # a non-zero exit status, so CI and scripts see the failure
