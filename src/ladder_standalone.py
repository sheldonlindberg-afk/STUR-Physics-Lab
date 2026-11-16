#!/usr/bin/env python3
"""
The symmetry-breaking ladder, from 3-3-1 to the two-diamond gravity experiment.
A single-file, standard-library-only reproduction of SYMMETRY_LADDER.md.

HOW TO RUN
    Paste this whole file into any Python 3.8+ runner (a terminal, an online
    interpreter, Jupyter, Pyodide, or an AI assistant's code tool) and run it.
    No packages to install: it uses only the Python standard library.
    It runs in a few seconds. It exits with status 1 if any check fails, so scripts and
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
              with the G of the diamond experiment; the selection holds for G down to 8.2x
              weaker at the reference spectrum, 1.6x weaker at the worst point of the
              threshold scan (Landau poles from src/m331_three_loop.py, carried as numbers).
              Black holes (rung 6 -> 4 and link 3): the diamond's Schwarzschild radius is a
              millionth of the Planck length; a Planck-mass black hole has k_B T = M_Pl/8 pi.
      More    Links added later, derived here without sympy (src/ladder_links.py L10e, L11-L22): the
              de Sitter horizon's entropy 3 pi/Lambda and its first law; the seesaw neutrino scale and
              its 1/w scaling (the Yukawas stay free); the first post-Newtonian correction to the
              entangling phase (-1.4e-23 rad); the cosmological constant against each rung's vacuum
              energy; Leaver's quasinormal modes, Schwarzschild and Kerr, and the ringdown fit against them; the ABJ anomaly
              coefficient from gamma matrices; the rho parameter's top-bottom loop and M_W; and
              Hawking's Planck spectrum from the Bogoliubov coefficients.
    Inputs are measured values (PDG 2024, FLAG 2024, CODATA 2018, Planck 2018; for rung 6 the EHT,
    stellar dynamics and LVK). What is not derived, by
    anyone: why the inputs have their values, and how gravity unifies with the others.

SOURCE
    Repository: https://github.com/sheldonlindberg-afk/STUR-Physics-Lab
    Notes:      SYMMETRY_LADDER.md
    This file condenses src/m331_breaking.py, chiral_breaking.py, casimir_diamonds.py,
    graviton_exchange.py, macdowell_mansouri.py, black_holes.py and ladder_links.py (the sympy ones
    re-derived here with numbers and exact fractions);
    tests/test_ladder_standalone.py checks
    that it agrees with them. Independent work, not peer reviewed. License: CC0 1.0.
"""
from fractions import Fraction as F
from itertools import permutations
from math import cos, exp, factorial, log, pi, sin, sqrt
import cmath
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
MZ_MEAS = 91.1880             # GeV, PDG 2024
ALPHA_MZ_INV = 127.930        # 1/alpha_em(M_Z), MS-bar, PDG 2024
S2_MZ = 0.23129               # sin^2 theta_W(M_Z), MS-bar, PDG 2024
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
POLES_331 = {"+1/sqrt3": (3.49103e19, 5.15600e11), "-1/sqrt3": (2.28969e29, 1.12580e15)}
# The same poles over the 72-point threshold scan of NOTE_331.md 3a (r_J, r_S, M_V, light
# doublets): the lowest N_c = 3 pole and the highest N_c = 5 pole, i.e. the narrowest window.
# Computed by src/ladder_links.py L3e; tests/test_ladder_standalone.py checks them against it.
POLES_331_SCAN = {"+1/sqrt3": (1.54027e19, 2.69119e12), "-1/sqrt3": (1.51351e29, 4.25661e15)}

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
    check("with rung 4's G the 3-3-1 selection keeps N_c = 3 and excludes N_c = 5; it would fail for G 8.2x weaker",
          all(lo < 1 < hi for lo, hi in win.values()) and abs(1 / win["+1/sqrt3"][0] / 8.18 - 1) < 0.01,
          "pinned", f"got windows {', '.join(f'{lo:.3g}-{hi:.2g}' for lo, hi in win.values())},"
          " pinned 0.12 (8.2x weaker) as the narrow side. The poles come from src/m331_three_loop.py")
    # L3e: the reference spectrum is one point. Over the threshold scan the window narrows.
    wscan = {}
    for v, (p3, p5) in POLES_331_SCAN.items():
        wscan[v] = ((mpl / p3) ** 2, (mpl / p5) ** 2)
        print(f"   beta = {v:8s}, worst over the threshold scan: N_c = 3 pole {p3 / mpl:.3g} M_Pl, N_c = 5 pole"
              f" {p5 / mpl:.2g} M_Pl -> holds for {wscan[v][0]:.2g} < G/G_meas < {wscan[v][1]:.2g}")
    check("over the threshold scan the selection still holds at the measured G, but would fail for G 1.6x weaker",
          all(lo < 1 < hi for lo, hi in wscan.values()) and abs(1 / wscan["+1/sqrt3"][0] / 1.592 - 1) < 0.01,
          "pinned", f"got windows {', '.join(f'{lo:.3g}-{hi:.2g}' for lo, hi in wscan.values())},"
          " pinned 0.63 (1.6x weaker) as the narrow side, at M_V = 2 TeV, r_J = 0.5, r_S = 1/3 and two light"
          " doublets. The 8.2x above is the reference spectrum's margin, not the model's. Gravity's own term in the"
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


# ----------------------------------------------------------------------------------------
# MORE LINKS (src/ladder_links.py L10e, L11-L22), standard library only
# ----------------------------------------------------------------------------------------
M_H_GEV, M_T_GEV, M_B_GEV = 125.20, 172.57, 4.18      # PDG 2024
MW_MEAS = 80.3692                                     # GeV, PDG 2024 average
DR_W_HAT, RHO_HAT = 0.06937, 1.01016                  # PDG 2024: MS-bar Delta r_W and rho-hat (bosonic loops included)
DALPHA_LEP_3LOOP, DALPHA_HAD_5 = 0.031497686, 0.02783       # Steinhauser 1998 (three loops); PDG 2024
NUFIT_DM21, NUFIT_DM31 = 7.49e-5, 2.513e-3            # eV^2, NuFIT 6.0, normal ordering
SUM_NU_PLANCK = 0.12                                  # eV, Planck 2018
M_E_EV = 0.51099895e6
EV = 1.602176634e-19


def design_a():
    """Design A as rung 4 builds it: m, dx, hold, ramp, gap."""
    return (geomspace(1e-16, 1e-12, 25)[13], geomspace(10e-6, 3e-3, 25)[18], geomspace(0.05, 20, 25)[2],
            geomspace(0.05, 5, 17)[12], casimir_safe_gap())


def branch_integral(fn, n=4001):
    """Entangling combination of int fn(r, v1y, v2y, nx, ny) dt over design A's branch pairs
    (A_i at (0, s_i y), B_j at (gap, s_j y)); returns (sum phi00 + phi11 - phi01 - phi10)."""
    m, dx, hold, ramp, gap = design_a()
    total = hold + 2 * ramp
    dt = total / (n - 1)
    ts = [total * i / (n - 1) for i in range(n)]
    ys = [0.5 * dx * ramp_profile(t, hold, ramp) for t in ts]
    vy = [(ys[min(i + 1, n - 1)] - ys[max(i - 1, 0)]) / (ts[min(i + 1, n - 1)] - ts[max(i - 1, 0)]) for i in range(n)]
    out = 0.0
    for si in (1, -1):
        for sj in (1, -1):
            vals = []
            for i in range(n):
                dyy = (sj - si) * ys[i]
                r = sqrt(gap * gap + dyy * dyy)
                vals.append(fn(m, r, si * vy[i], sj * vy[i], gap / r, dyy / r))
            integral = dt * (sum(vals) - 0.5 * (vals[0] + vals[-1]))
            out += (1 if si == sj else -1) * integral
    return out


def cgamma(z):
    """Gamma(z) for complex z, Lanczos (g = 7, 9 terms)."""
    c = (0.99999999999980993, 676.5203681218851, -1259.1392167224028, 771.32342877765313, -176.61502916214059,
         12.507343278686905, -0.13857109526572012, 9.9843695780195716e-6, 1.5056327351493116e-7)
    if z.real < 0.5:
        return pi / (cmath.sin(pi * z) * cgamma(1 - z))
    z -= 1
    x = c[0] + sum(c[i] / (z + i) for i in range(1, 9))
    t = z + 7.5
    return sqrt(2 * pi) * t ** (z + 0.5) * cmath.exp(-t) * x


def leaver(n, l=2, guess=None):
    """M omega of the gravitational l-mode, n-th overtone, from Leaver's continued fraction (2M = 1)."""
    eps = 3
    def cond(w, N=300):
        rho = -1j * w
        al = lambda k: k * k + (2 * rho + 2) * k + 2 * rho + 1
        be = lambda k: -(2 * k * k + (8 * rho + 2) * k + 8 * rho**2 + 4 * rho + l * (l + 1) - eps)
        ga = lambda k: k * k + 4 * rho * k + 4 * rho**2 - eps - 1
        R = 0
        for k in range(N - 1, n - 1, -1):
            R = al(k) * ga(k + 1) / (be(k + 1) - R)
        fwd = 0
        for k in range(1, n + 1):
            fwd = al(k - 1) * ga(k) / (be(k - 1) - fwd)
        return be(n) - fwd - R
    a, b = (guess or {0: 0.74 - 0.18j, 1: 0.69 - 0.55j}[n]), (guess or {0: 0.74 - 0.18j, 1: 0.69 - 0.55j}[n]) + 0.01
    fa, fb = cond(a), cond(b)
    for _ in range(60):
        if fb == fa:
            break
        a, b, fa = b, b - fb * (b - a) / (fb - fa), fb
        fb = cond(b)
        if abs(b - a) < 1e-14:
            break
    return b / 2


def gamma_matrices():
    """Euclidean 4x4 gamma matrices from Pauli matrices (complex lists)."""
    s1, s2, s3 = [[0, 1], [1, 0]], [[0, -1j], [1j, 0]], [[1, 0], [0, -1]]
    one = [[1, 0], [0, 1]]
    k = lambda A, B: [[A[i // 2][j // 2] * B[i % 2][j % 2] for j in range(4)] for i in range(4)]
    return [k(s2, s1), k(s2, s2), k(s2, s3), k(s1, one)]


def mm(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(4)) for j in range(4)] for i in range(4)]


def seesaw_light(mD, M):
    return 2 * mD**2 / (M + sqrt(M * M + 4 * mD**2))


KERR_BCW_TABLE = {0.0: (.3737, .0890), 0.1: (.3870, .0887), 0.2: (.4021, .0883), 0.3: (.4195, .0877),
                  0.4: (.4398, .0869), 0.5: (.4641, .0856), 0.6: (.4940, .0838), 0.7: (.5326, .0808),
                  0.8: (.5860, .0756), 0.9: (.6716, .0649), 0.98: (.8254, .0386)}   # BCW 2006, Table II


def kerr_conditions(w, A, chi, m=2, s=-2, N=300):
    """Leaver's radial and angular continued-fraction conditions for the n = 0 Kerr mode (2M = 1)."""
    a = chi / 2
    b = sqrt(1 - 4 * a * a)
    k1, k2 = abs(m - s) / 2, abs(m + s) / 2
    q = w / 2 - m * a
    c0 = 1 - s - 1j * w - 2j * q / b
    c1 = -4 + 2j * w * (2 + b) + 4j * q / b
    c2 = s + 3 - 3j * w - 2j * q / b
    c3 = w * w * (4 + 2 * b - a * a) - 2 * a * m * w - s - 1 + (2 + b) * 1j * w - A + (4 * w + 2j) * q / b
    c4 = s + 1 - 2 * w * w - (2 * s + 3) * 1j * w - (4 * w + 2j) * q / b
    al = lambda k: k * k + (c0 + 1) * k + c0
    be = lambda k: -2 * k * k + (c1 + 2) * k + c3
    ga = lambda k: k * k + (c2 - 3) * k + c4 - c2 + 2
    R = 0
    for k in range(N - 1, -1, -1):
        R = al(k) * ga(k + 1) / (be(k + 1) - R)
    aw = a * w
    alt = lambda k: -2 * (k + 1) * (k + 2 * k1 + 1)
    bet = lambda k: (k * (k - 1) + 2 * k * (k1 + k2 + 1 - 2 * aw)
                     - (2 * aw * (2 * k1 + s + 1) - (k1 + k2) * (k1 + k2 + 1)) - (aw * aw + s * (s + 1) + A))
    gat = lambda k: 2 * aw * (k + k1 + k2 + s)
    Rt = 0
    for k in range(N - 1, 0, -1):
        Rt = alt(k - 1) * gat(k) / (bet(k) - Rt)
    return be(0) - R, bet(0) - Rt


def kerr_solve(chi, guess):
    x = list(guess)
    for _ in range(60):
        f = lambda v: kerr_conditions(v[0], v[1], chi)
        F0 = f(x)
        J = []
        for j in range(2):
            xp = list(x)
            xp[j] += 1e-7
            Fp = f(xp)
            J.append([(Fp[i] - F0[i]) / 1e-7 for i in range(2)])
        det = J[0][0] * J[1][1] - J[1][0] * J[0][1]
        d0 = (F0[0] * J[1][1] - F0[1] * J[1][0]) / det
        d1 = (F0[1] * J[0][0] - F0[0] * J[0][1]) / det
        x[0] -= d0
        x[1] -= d1
        if abs(d0) + abs(d1) < 1e-13:
            break
    return x


_KERR_GRID = {}


def kerr_grid():
    if not _KERR_GRID:
        x = kerr_solve(0.0, [2 * leaver(0), 4 + 0j])
        _KERR_GRID[0.0] = tuple(x)
        for i in range(1, 40):
            x = kerr_solve(i * 0.025, x)
            _KERR_GRID[round(i * 0.025, 4)] = tuple(x)
    return _KERR_GRID


def kerr_FQ_w(chi):
    g = kerr_grid()
    k = min(g, key=lambda c: abs(c - chi))
    return kerr_solve(chi, list(g[k]))[0] / 2


def kerr_FQ(chi):
    w = kerr_FQ_w(chi)
    return w.real, w.real / (-2 * w.imag)


def invert_220_exact(freq, damp, z):
    Q = pi * freq / damp
    lo, hi = 0.0, 0.95
    for _ in range(50):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if kerr_FQ(mid)[1] < Q else (lo, mid)
    chi = (lo + hi) / 2
    return kerr_FQ(chi)[0] / (2 * pi * freq * GM_SUN / C_LIGHT**3) / (1 + z), chi



def links_more():
    banner("MORE LINKS  Rung 5 -> 6, rung 1 -> data, rung 4 -> 5 and 6 (src/ladder_links.py L10e, L11-L22)")
    plain("further places where one rung feeds another: the de Sitter horizon's entropy, the neutrino-mass scale, the first relativistic correction to the experiment's phase (far too small to see), the cosmological constant against each rung's vacuum energy, and three results the earlier rungs had quoted: the ringdown fit, the anomaly coefficient and Hawking's Planck spectrum.")
    l = 1.0
    # L11: the de Sitter horizon
    f0 = lambda r: 1 - r * r / l**2
    kappa = killing_kappa(f0, l - 1e-6 * l, 1e-8 * l)
    Lam = 3 / l**2
    A_ = 4 * pi * l**2
    ratio_3 = (A_ / 4) / (pi / Lam)
    Ssi = 3 * pi / (LAMBDA_SI * (HBAR * G_NEWTON / C_LIGHT**3))
    ell = sqrt(3 / LAMBDA_SI)
    T_dS = HBAR * C_LIGHT / (2 * pi * K_B * ell)
    check("L11a de Sitter's horizon r = l has kappa = 1/l from rung 6's Killing definition; A = 4 pi l^2 = 12 pi/Lambda,"
          " so S = A/4 = 3 pi/Lambda, three times pi/Lambda (the form pi c^3/(G hbar Lambda))",
          abs(kappa * l - 1) < 1e-5 and abs(A_ - 12 * pi / Lam) < 1e-12 and abs(ratio_3 - 3) < 1e-12)
    check("L11d at the measured Lambda: l = 1.65e26 m, S_dS = 3.26e122 k_B, T_dS = 2.2e-30 K",
          abs(Ssi / 3.263e122 - 1) < 1e-3 and abs(T_dS / 2.21e-30 - 1) < 1e-2 and abs(ell / 1.647e26 - 1) < 1e-3,
          "pinned", f"got S = {Ssi:.4e}, T = {T_dS:.3e} K, l = {ell:.4e} m, pinned 3.263e122, 2.21e-30, 1.647e26")
    res = 0.0
    for r_ in (0.3, 0.7, 0.9, 1.1):                      # SdS horizons of 2M = r(1 - r^2/l^2) at those radii
        Mh = lambda x: x * (1 - x * x / l**2) / 2
        h = 1e-5
        dM = (Mh(r_ + h) - Mh(r_ - h)) / (2 * h)
        fm = lambda x: 1 - 2 * Mh(r_) / x - x * x / l**2
        fp = (fm(r_ + h) - fm(r_ - h)) / (2 * h)
        res = max(res, abs(dM - fp / (4 * pi) * 2 * pi * r_))
    check("L11b the first law dM = (f'(r_h)/4 pi) dS holds at both Schwarzschild-de Sitter horizons (dM = T dS at the"
          " black hole's, dM = -T dS at the cosmological one)", res < 1e-8, "math", f"largest residual {res:.1e}")
    worst, k_max = 0.0, 200
    for k in range(1, k_max):
        hz = sds_horizons((k / k_max) / sqrt(27), l)
        worst = max(worst, hz[0]**2 + hz[1]**2)
    check("L11c de Sitter maximizes the entropy: (S_bh + S_c)/S_dS < 1 for every black hole the universe allows,"
          " r_b^2 + r_c^2 + (r_b + r_c)^2 = 2 l^2", worst < 1 and abs(worst - 0.998077) < 1e-5, "pinned", f"got {worst:.6f}")
    # L10e
    lam_r = lambda r, Lm: 1 / sqrt(1 - r * r / l**2)
    ok = all(abs(lam_r(r_, 0) - (1 + r_ * r_ / (2 * l**2))) < 0.5 * r_**4 / l**4 * 1.5 for r_ in (0.01, 0.05, 0.1))
    m, dx, hold, ramp, gap = design_a()
    ell2 = 3 / LAMBDA_SI
    dn = G_NEWTON * m * m / HBAR * branch_integral(lambda m_, r, v1, v2, nx, ny: 1 / r)
    dc = G_NEWTON * m * m / HBAR * branch_integral(lambda m_, r, v1, v2, nx, ny: r / (2 * ell2))
    check("L10e a test mass at distance r from M has U = -GMm/(r sqrt(1 - r^2/l^2)): a relative correction (r/l)^2/2,"
          " symmetric in the two masses; it shifts design A's phase by -1.9e-60 of itself",
          ok and abs(dc / dn / -1.92e-60 - 1) < 0.03, "pinned", f"got {dc / dn:.3e}")
    # L12: neutrino mass
    qm, qp = triplet_charges(F(-1, 3), "-1/sqrt3"), triplet_charges(F(-2, 3), "+1/sqrt3")
    check("L12a rung 1's lepton triplet: (nu, e, N) with N neutral for beta = -1/sqrt3, (nu, e, E-) with E charged for +1/sqrt3",
          qm == [0, -1, 0] and qp == [0, -1, -1])
    mD, Mh_ = 3.0e-3, 1.0
    ev = sorted(jacobi_eigenvalues([[0, mD], [mD, Mh_]]), key=abs)
    prod_ok = abs(ev[0] * ev[1] + mD**2) < 1e-12
    mu_, Lm_, mD2 = 1e-6, 1.0, 0.02
    ev3 = sorted(jacobi_eigenvalues([[0, mD2, 0], [mD2, 0, Lm_], [0, Lm_, mu_]]), key=abs)
    inv_ok = abs(abs(ev3[0]) / (mu_ * mD2**2 / (mD2**2 + Lm_**2)) - 1) < 1e-4
    check("L12b seesaw [[0, m_D],[m_D, M]]: the eigenvalues multiply to -m_D^2, so m_light = m_D^2/m_heavy; the inverse"
          " seesaw gives mu m_D^2/(m_D^2 + Lambda^2); at fixed Yukawas m_light goes as 1/w exactly",
          prod_ok and inv_ok and abs(abs(ev[0]) - seesaw_light(mD, Mh_)) < 1e-12, "math", f"product residual {abs(ev[0] * ev[1] + mD**2):.1e}")
    g_ = sqrt(4 * pi / ALPHA_MZ_INV / S2_MZ)
    w_ = 2 * 4e3 / g_
    v_ = (sqrt(2) * G_F) ** -0.5
    M_R = w_ / sqrt(2) * 1e9
    yD = sqrt(2 * sqrt(NUFIT_DM31) * M_R) / (v_ * 1e9)
    ye = sqrt(2) * M_E_EV / (v_ * 1e9)
    lt = lambda wv, yd=yD: seesaw_light(yd * v_ * 1e9 / sqrt(2), wv * 1e9 / sqrt(2))
    slope = log10_ratio(lt(10 * w_), lt(w_))
    s_min = sqrt(NUFIT_DM21) + sqrt(NUFIT_DM31)
    check("L12c-d with M_V = 4 TeV (w = 12.3 TeV): 0.05 eV needs y_D = 3.8e-6, 1.3x the electron's (a free Yukawa, not a"
          " prediction); the minimal mass sum 0.059 eV is inside Planck's 0.12 eV",
          abs(w_ / 12275.8 - 1) < 1e-4 and abs(yD / 3.789e-6 - 1) < 2e-3 and abs(yD / ye - 1.2909) < 2e-3
          and abs(slope + 1) < 1e-9 and s_min < SUM_NU_PLANCK, "pinned", f"got w = {w_:.1f} GeV, y_D = {yD:.3e}, slope {slope:.6f}, sum {s_min:.4f} eV")
    # L13: first post-Newtonian correction
    def lag(t, r_=10.0, v_=0.3):
        U = 1 / r_
        geo = -1 / t * sqrt(1 - 2 * t * U + 2 * t**2 * U**2 - (1 + 2 * t * U) * t * v_**2)
        eih = -1 / t + v_**2 / 2 + U + t * (v_**4 / 8 + 1.5 * U * v_**2 - U**2 / 2)
        return geo - eih
    r_t = lag(0.02) / lag(0.01)
    check("L13a the EIH test-mass limit (3/2 v^2 and G^2 terms) agrees with the geodesic Lagrangian of harmonic-coordinate"
          " Schwarzschild to 1/c^2: the difference scales as 1/c^4", 3.6 < r_t < 4.4, "math", f"difference ratio at t and 2t: {r_t:.3f} (4 expected)")
    c2 = C_LIGHT**2
    pn = G_NEWTON * m * m / HBAR * branch_integral(
        lambda m_, r, v1, v2, nx, ny: (1.5 * (v1**2 + v2**2) - 3.5 * v1 * v2 - 0.5 * (ny * v1) * (ny * v2)) / (r * c2))
    g2 = -G_NEWTON**2 * m**3 / (HBAR * c2) * branch_integral(lambda m_, r, v1, v2, nx, ny: 1 / r**2)
    check("L13b design A's entangling phase: the velocity terms of the 1PN correction shift it by -1.4e-23 rad of 2.19"
          " (relative -6.6e-24 ~ -(v/c)^2), the G^2 term by -1.8e-37 rad: nowhere near measurable",
          abs(dn - 2.1868) < 1e-3
          and abs(pn / -1.442e-23 - 1) < 0.02 and abs(g2 / -1.785e-37 - 1) < 0.02, "pinned", f"got {pn:.3e} rad and {g2:.3e} rad")
    # L14: Bekenstein
    Mbh = 1e30
    Rbh = 2 * G_NEWTON * Mbh / c2
    bek_bh = 2 * pi * Rbh * Mbh * C_LIGHT / HBAR
    holo_bh = 4 * pi * Rbh**2 / (4 * G_NEWTON * HBAR / C_LIGHT**3)
    Rd = diamond_radius(m)
    bek_d = 2 * pi * Rd * m * C_LIGHT / HBAR
    holo_d = 4 * pi * Rd**2 / (4 * G_NEWTON * HBAR / C_LIGHT**3)
    atoms = m / (12 * U_AMU)
    check("L14 a Schwarzschild black hole saturates the Bekenstein bound 2 pi R E/(hbar c) = A/4 l_P^2 exactly; design A's"
          " diamond (7.4e11 atoms) is far below its bound 2.6e23 and the holographic bound 1.2e58 (k_B)",
          abs(bek_bh / holo_bh - 1) < 1e-12 and abs(bek_d / 2.620e23 - 1) < 2e-3 and abs(holo_d / 1.201e58 - 1) < 2e-3 and bek_d > 1e3 * atoms,
          "pinned", f"got bound {bek_d:.3e}, holographic {holo_d:.3e}, atoms {atoms:.3e}")
    # L15: the cosmological constant against each rung's vacuum energy
    rho_L = LAMBDA_SI * C_LIGHT**4 / (8 * pi * G_NEWTON)
    rho_Pl = C_LIGHT**7 / (HBAR * G_NEWTON**2)
    rho_ev4 = rho_L * (HBAR * C_LIGHT) ** 3 / EV**4
    mpl_ev = sqrt(HBAR * C_LIGHT / G_NEWTON) * c2 / EV
    ratios = [(92.07e6 * 134.9768e6) ** 2 / rho_ev4, ((M_H_GEV * 1e9) ** 2 * (v_ * 1e9) ** 2 / 8) / rho_ev4,
              (w_ * 1e9) ** 4 / rho_ev4, mpl_ev**4 / rho_ev4]
    check("L15a S_dS = (3/8) rho_Planck/rho_Lambda exactly, with rho_Lambda = Lambda c^4/8 pi G and rho_Pl = c^7/(hbar G^2)",
          abs(Ssi / (3 / 8 * rho_Pl / rho_L) - 1) < 1e-12)
    check("L15b rho_Lambda^(1/4) = 2.25 meV; rung 2's chiral vacuum energy f_pi^2 m_pi^2 is 6e42, rung 1's Higgs minimum"
          " m_h^2 v^2/8 5e54, the 3-3-1 scale w^4 9e62 (an order of magnitude) and M_Pl^4 9e122 times larger: the"
          " cosmological-constant problem, quantified and not solved",
          abs(rho_ev4**0.25 / 2.248e-3 - 1) < 2e-3 and abs(ratios[0] / 6.05e42 - 1) < 5e-3 and abs(ratios[1] / 4.65e54 - 1) < 5e-3
          and abs(ratios[2] / 8.89e62 - 1) < 5e-3 and abs(ratios[3] / (8 * Ssi / 3) - 1) < 1e-3, "pinned",
          "ratios " + ", ".join(f"{x:.2e}" for x in ratios))
    # L16: quasinormal modes
    w0, w1 = leaver(0), leaver(1)
    fit_r = BCW_220[0] + BCW_220[1]
    fit_q = BCW_220[3] + BCW_220[4]
    check("L16a Leaver's continued fraction for Schwarzschild: M omega = 0.373672 - 0.088962 i (l = 2, n = 0) and"
          " 0.346711 - 0.273915 i (n = 1)", abs(w0 - (0.373672 - 0.088962j)) < 2e-6 and abs(w1 - (0.346711 - 0.273915j)) < 2e-6,
          "pinned", f"got {w0:.6f} and {w1:.6f}")
    check("L16b the Berti-Cardoso-Will fit at chi = 0 is 1.4% low in frequency and 0.9% high in Q (L20 covers the spin"
          " dependence at chi ~ 0.7, which GW250114 uses)",
          abs(fit_r / w0.real - 1 + 0.014) < 1e-3 and abs(fit_q / (w0.real / (-2 * w0.imag)) - 1 - 0.009) < 1e-3, "pinned",
          f"got {100 * (fit_r / w0.real - 1):+.2f}% and {100 * (fit_q / (w0.real / (-2 * w0.imag)) - 1):+.2f}%")
    # L20: Kerr quasinormal modes
    worst = max(max(abs(kerr_FQ_w(c).real - re), abs(-kerr_FQ_w(c).imag - im)) for c, (re, im) in KERR_BCW_TABLE.items())
    check("L20a Teukolsky's radial equation (s = -2) with Leaver's recurrence, coupled through the separation constant to the"
          " spheroidal equation's, reproduces Berti-Cardoso-Will's Table II (l = m = 2, n = 0, chi = 0 to 0.98) to 6e-5",
          worst < 6e-5, "data", f"largest difference {worst:.1e}; the table is quoted to 4 digits, so half a unit in the last place is 5e-5")
    ef = eq = 0.0
    for i in range(100):
        c = i * 0.01
        Fx, Qx = kerr_FQ(c)
        ef = max(ef, abs((BCW_220[0] + BCW_220[1] * (1 - c) ** BCW_220[2]) / Fx - 1))
        eq = max(eq, abs((BCW_220[3] + BCW_220[4] * (1 - c) ** BCW_220[5]) / Qx - 1))
    check("L20b the fit against the exact modes over chi = 0 to 0.99: largest errors 1.85% (F) and 0.88% (Q), the maxima BCW state",
          abs(ef - 0.0185) < 5e-4 and abs(eq - 0.0088) < 5e-4, "data", f"got {100 * ef:.2f}% and {100 * eq:.2f}%")
    mf, chif = invert_220_exact(F220[0], G220[0], GW_Z[0])
    a_f = kerr_area_km2(mf, chif)
    corners = [kerr_area_km2(*invert_220_exact(f, g, z)) for f in (F220[0] - F220[1], F220[0] + F220[2])
               for g in (G220[0] - G220[1], G220[0] + G220[2]) for z in (GW_Z[0] - GW_Z[1], GW_Z[0] + GW_Z[1])]
    a_init_max = kerr_area_km2(GW_M1[0] + GW_M1[2], 0) + kerr_area_km2(GW_M2[0] + GW_M2[2], 0)
    check("L20c GW250114's ringdown inverted with the exact Kerr modes: M_f = 66.48 Msun, chi_f = 0.744, final area 4.04e5 km^2;"
          " at the least favourable corner 3.36e5 km^2 against the initial 2.52e5: the area law does not rest on the fit's error",
          abs(mf - 66.48) < 0.02 and abs(chif - 0.7444) < 5e-4 and abs(a_f / 4.039e5 - 1) < 1e-3
          and min(corners) > a_init_max and abs(min(corners) / 3.360e5 - 1) < 2e-3, "pinned",
          f"got M_f = {mf:.2f}, chi_f = {chif:.4f}, area {a_f:.4g} km^2, worst corner {min(corners):.4g}, initial {a_init_max:.4g}")
    # L21: the retarded Casimir-Polder step, in an exactly solvable retarded model
    M_, mu_, g_, w0_ = 40, 0.3, 0.45, 1.0
    def lat_green(xi, d):
        return sum(cos(2 * pi * p_ * d / M_) / (xi * xi + mu_**2 + 4 * sin(pi * p_ / M_) ** 2) for p_ in range(M_)) / M_
    def e0(r):
        V = [[0.0] * (M_ + 2) for _ in range(M_ + 2)]
        for j in range(M_):
            V[j][j] = 2 + mu_**2
            V[j][(j + 1) % M_] = V[(j + 1) % M_][j] = -1.0
        V[M_][M_] = V[M_ + 1][M_ + 1] = w0_**2
        V[M_][0] = V[0][M_] = g_
        V[M_ + 1][r] = V[r][M_ + 1] = g_
        return 0.5 * sum(sqrt(x) for x in jacobi_eigenvalues(V))
    def lndet(r, retarded, n=1600):
        def f(xi):
            a = xi * xi + w0_**2
            return log(1 - (g_ * g_ * lat_green(xi if retarded else 0.0, r) / (a - g_ * g_ * lat_green(xi, 0))) ** 2)
        h = 1.0 / n                                   # xi = t/(1 - t), dxi = dt/(1 - t)^2
        tot = 0.0
        for k in range(n):
            t = k * h
            wgt = 1 if k in (0,) else (4 if k % 2 else 2)
            tot += wgt * f(t / (1 - t)) / (1 - t) ** 2
        tot += 0.0                                    # the integrand vanishes at t = 1
        return tot * h / 3 / (2 * pi)
    r_far = M_ // 2
    ex0, fo0, st0 = e0(r_far), lndet(r_far, True), lndet(r_far, False)
    rows = [(r, e0(r) - ex0, lndet(r, True) - fo0, lndet(r, False) - st0) for r in (3, 6)]
    check("L21a retarded Casimir-Polder: in a solvable model (two oscillators and a propagating field on a ring) the energy from"
          " the normal modes of the whole system equals (1/2 pi) int dxi ln[1 - (g^2 G12(xi, r) alpha_d)^2] with the retarded"
          " Green function, while the static (instantaneous) kernel is off by a factor of 3; P2's Green tensor carries the same"
          " algebra to the electromagnetic case (the dyadic case is not diagonalized here)",
          all(abs(fo / ex - 1) < 1e-6 for _, ex, fo, _ in rows) and abs(rows[0][3] / rows[0][1] - 3) < 1.0 and abs(rows[0][3] / rows[0][1] - 1) > 1,
          "math", "r = %d: normal modes %.6e, ln det %.6e, static %.6e" % (rows[0][0], rows[0][1], rows[0][2], rows[0][3]))
    x_cp = ((EPS_DIAMOND - 1) / (EPS_DIAMOND + 2)) * diamond_radius(m)**3 / gap**3
    check("L21c at design A's gap alpha G ~ K R^3/r^3 = 1e-7, so the second-order Casimir-Polder term is exact to 1e-14",
          5e-8 < x_cp < 2e-7 and x_cp**2 < 1e-13, "math", f"got {x_cp:.2e}")
    # L17: the ABJ anomaly
    gam = gamma_matrices()
    id4 = [[1 if i == j else 0 for j in range(4)] for i in range(4)]
    cliff = all(abs(sum(abs(mm(gam[a], gam[b])[i][j] + mm(gam[b], gam[a])[i][j] - (2 if a == b else 0) * id4[i][j])
                        for i in range(4) for j in range(4))) < 1e-12 for a in range(4) for b in range(4))
    g5 = mm(mm(gam[0], gam[1]), mm(gam[2], gam[3]))
    sig = lambda a, b: [[0.5j * (mm(gam[a], gam[b])[i][j] - mm(gam[b], gam[a])[i][j]) for j in range(4)] for i in range(4)]
    lam, holds = None, True
    for a, b, c_, d in ((a, b, c_, d) for a in range(4) for b in range(4) for c_ in range(4) for d in range(4)):
        P = mm(mm(g5, sig(a, b)), sig(c_, d))
        tr = sum(P[i][i] for i in range(4))
        e = eps4([a, b, c_, d])
        if e == 0:
            holds &= abs(tr) < 1e-12
        else:
            lam = tr / e if lam is None else lam
            holds &= abs(tr - lam * e) < 1e-12
    check("L17a Fujikawa's Jacobian with explicit gamma matrices: tr[gamma5 sigma_mn sigma_rs] = -4 eps_mnrs for all 256 index sets"
          " (the sign is gamma5's orientation), so the divergence is e^2 eps F F/(16 pi^2) in magnitude",
          cliff and holds and abs(abs(lam) - 4) < 1e-12 and abs(abs((1 / (16 * pi**2)) * (1 / 8) * lam) * 32 * pi**2 - 1) < 1e-12)
    Bf, Ef = F(3, 7), F(5, 11)
    Fm = [[0] * 4 for _ in range(4)]
    Fm[0][1], Fm[1][0], Fm[2][3], Fm[3][2] = Bf, -Bf, Ef, -Ef
    epsFF = sum(eps4([a, b, c_, d]) * Fm[a][b] * Fm[c_][d] for a, b, c_, d in permutations(range(4)))
    check("L17b a second route: each chirality's lowest Landau level is a 1+1 Weyl fermion, d n5/dt = 2 (eB/2 pi)(eE/2 pi);"
          " with eps F F = 8 F12 F34 it is the same number as the Jacobian's (e^2/32 pi^2) x 2 eps F F",
          epsFF == 8 * Bf * Ef and abs(2 / (32 * pi**2) * float(epsFF) - 2 * float(Bf) * float(Ef) / (4 * pi**2)) < 1e-15)
    ok = True
    for Nc, Qu, Qd, alpha in ((3, 2 / 3, -1 / 3, 1 / 137.036), (5, 3 / 5, -2 / 5, 1 / 137.036)):
        e2 = 4 * pi * alpha
        amp = Nc * (Qu**2 - Qd**2) / 2 * e2 / (16 * pi**2) * 8                 # per 1/f_pi
        ok &= abs(amp / (alpha * Nc * (Qu**2 - Qd**2) / pi) - 1) < 1e-12
    check("L17c matching to PCAC: the anomaly's amplitude is alpha N_c (Q_u^2 - Q_d^2)/(pi f_pi), the coefficient the pi0 width"
          " (links above) took as given; the PCAC step and Adler-Bardeen stay quoted", ok)
    # L18: the rho parameter
    def drho_loop(eps, s2, mt=M_T_GEV, mb=M_B_GEV):
        D = 1 / eps
        A0 = lambda m_: m_**2 * (D + 1 - log(m_**2))
        B0 = lambda m1, m2: D + 1 - (m1**2 * log(m1**2) - m2**2 * log(m2**2)) / (m1**2 - m2**2)
        B0e = lambda m_: D - log(m_**2)
        fac = -0.5 * (1 - eps) / (1 - eps / 2)
        LLn = lambda m1, m2: 2 * fac * (A0(m2) + m1**2 * B0(m1, m2))
        LLe = lambda m_: 2 * fac * (A0(m_) + m_**2 * B0e(m_))
        LRn = lambda m_: 2 * m_**2 * B0e(m_)
        Z = lambda m_, Q, T3: (T3 - Q * s2) ** 2 * LLe(m_) + (Q * s2) ** 2 * LLe(m_) - 2 * (T3 - Q * s2) * Q * s2 * LRn(m_)
        ward = 2 * LLe(mt) + 2 * LRn(mt)
        return 4 * (Z(mt, 2 / 3, 0.5) + Z(mb, -1 / 3, -0.5)) - 2 * LLn(mt, mb), ward
    Fclosed = M_T_GEV**2 + M_B_GEV**2 - 2 * M_T_GEV**2 * M_B_GEV**2 / (M_T_GEV**2 - M_B_GEV**2) * log(M_T_GEV**2 / M_B_GEV**2)
    t1, w1_ = drho_loop(1e-6, 0.2)
    t2, _ = drho_loop(1e-6, 0.3)
    check("L18a the W and Z self-energies from the t-b loop in dimensional regularization: the vector Ward identity holds,"
          " Delta rho has no 1/eps pole and no s^2 dependence, and equals N_c G_F/(8 sqrt2 pi^2) [m_t^2 + m_b^2 - 2 m_t^2 m_b^2"
          " ln(m_t^2/m_b^2)/(m_t^2 - m_b^2)]", abs(t1 / Fclosed - 1) < 1e-4 and abs(t1 - t2) < 1e-2 * Fclosed * 1e-2
          and abs(w1_) < 1e-4 * Fclosed, "math", f"loop/closed - 1 = {t1 / Fclosed - 1:.1e} at eps = 1e-6")
    drho = 3 * G_F * Fclosed / (8 * sqrt(2) * pi**2)
    A_w = pi * ALPHA_0 / (sqrt(2) * G_F)
    dal = DALPHA_LEP_3LOOP + DALPHA_HAD_5
    def solve(use_dal, use_top, use_h, rest=0.0):
        MW = 80.4
        for _ in range(200):
            c2s2 = MW**2 / (MZ_MEAS**2 - MW**2)
            dH = 3 * G_F * MW**2 / (8 * sqrt(2) * pi**2) * log(M_H_GEV**2 / MW**2) if use_h else 0.0
            dr = (dal if use_dal else 0.0) - (c2s2 * drho if use_top else 0.0) + dH + rest
            MW = sqrt(MZ_MEAS**2 / 2 * (1 + sqrt(1 - 4 * A_w / (1 - dr) / MZ_MEAS**2)))
        return MW
    steps = [solve(0, 0, 0), solve(1, 0, 0), solve(1, 1, 0), solve(1, 1, 1)]
    lo, hi = -0.05, 0.05
    for _ in range(80):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if solve(1, 1, 1, mid) > MW_MEAS else (lo, mid)
    check("L18b-c Delta rho = 9.26e-3; M_W from G_F, alpha(0), M_Z: tree 80.94, + Delta alpha 79.96, + top loop 80.53, + Higgs log"
          " 80.50 GeV against 80.37 measured; the remainder Delta r = 0.007 is not computed here (B7's MS-bar +0.35% is not closed)",
          abs(drho / 9.256e-3 - 1) < 2e-3 and abs(steps[0] - 80.939) < 2e-3 and abs(steps[1] - 79.961) < 2e-3
          and abs(steps[2] - 80.526) < 2e-3 and abs(steps[3] - 80.495) < 3e-3 and abs((lo + hi) / 2 - 0.0071) < 3e-4,
          "pinned", "steps " + ", ".join(f"{x:.3f}" for x in steps) + f", remainder {(lo + hi) / 2:+.4f}")
    # L22: B7's +0.35% on M_Z through the MS-bar relations
    alh = 1 / ALPHA_MZ_INV
    A0 = sqrt(pi * ALPHA_0 / (sqrt(2) * G_F))
    dr0 = 1 - ALPHA_0 / alh
    tree_ = sqrt(pi * alh / (sqrt(2) * G_F) / (S2_MZ * (1 - S2_MZ)))
    pred_ = A0 / (sqrt(S2_MZ * (1 - S2_MZ)) * sqrt((1 - DR_W_HAT) * RHO_HAT))
    pred1 = A0 / (sqrt(S2_MZ * (1 - S2_MZ)) * sqrt((1 - DR_W_HAT) * (1 + drho)))
    check("L22 B7's tree M_Z = A0/[s c (1 - Dr0)^(1/2)] against M_Z = A0/[s c ((1 - Dr_W) rho-hat)^(1/2)] (PDG's MS-bar relations):"
          " M_Z^2/tree^2 = (1 - Dr0)/[(1 - Dr_W) rho-hat] gives 91.1879 GeV and the -0.348% gap; L18's one-loop rho is 91% of"
          " rho-hat - 1 and gives 91.229 GeV; Dr_W - Dr0 = 0.0029 and the bosonic 9% are not derived",
          abs(pred_ - MZ_MEAS) < 2e-3 and abs(pred_ / tree_ - MZ_MEAS / tree_) < 5e-5 and abs(drho / (RHO_HAT - 1) - 0.912) < 2e-3
          and abs(pred1 - 91.229) < 2e-3, "data", f"got {pred_:.4f} GeV (measured {MZ_MEAS}), tree {tree_:.3f}, one-loop rho gives {pred1:.3f}")
    # L19: Hawking radiation as radiation
    import cmath
    y, Om = 0.7, 1.3
    s_ = 0.6 + 0.9j
    n_pts, lo_t, hi_t = 40000, -40.0, 6.0
    h_ = (hi_t - lo_t) / n_pts
    fn = lambda t: cmath.exp(1j * y * t - s_ * cmath.exp(t) + t)
    simpson = h_ / 3 * (fn(lo_t) + fn(hi_t) + sum((4 if k % 2 else 2) * fn(lo_t + k * h_) for k in range(1, n_pts)))
    closed = cgamma(1 + 1j * y) * s_ ** (-1 - 1j * y)
    gam2 = abs(cgamma(1 + 1j * y)) ** 2 - pi * y / (exp(pi * y) - exp(-pi * y)) * 2
    mod = lambda sgn: abs(cgamma(1 + 1j * y) * (sgn * 1j * Om) ** (-1 - 1j * y))
    rat = (mod(-1) / mod(+1)) ** 2
    check("L19a the Klein-Gordon overlaps of the outgoing modes e^(-i w u), u = -(1/kappa) ln(-kappa U), with the vacuum of"
          " the regular coordinate U reduce to Gamma(1 + i w/kappa)(+-i Omega)^(-1-i w/kappa) (the integral and"
          " |Gamma(1+iy)|^2 = pi y/sinh(pi y) checked numerically); |beta/alpha|^2 = e^(-2 pi w/kappa)",
          abs(simpson - closed) < 1e-8 and abs(gam2) < 1e-12 and abs(rat / exp(-2 * pi * y) - 1) < 1e-10, "math",
          f"integral difference {abs(simpson - closed):.1e}, ratio {rat:.10f} vs {exp(-2 * pi * y):.10f}")
    ok = True
    for y_, Om_ in ((0.7, 1.3), (1.9, 0.4), (0.2, 5.0)):
        g2_ = abs(cgamma(1 + 1j * y_)) ** 2
        A2 = exp(pi * y_) * g2_ / (4 * pi**2 * y_ * Om_)               # w = y kappa, kappa = 1
        B2 = exp(-pi * y_) * g2_ / (4 * pi**2 * y_ * Om_)
        ok &= abs((A2 - B2) * 2 * pi * Om_ - 1) < 1e-10 and abs(B2 / (A2 - B2) * (exp(2 * pi * y_) - 1) - 1) < 1e-10
    check("L19b unitarity |alpha|^2 - |beta|^2 = 1/(2 pi kappa Omega) and the mean number n = |beta|^2/(|alpha|^2 - |beta|^2) ="
          " 1/(e^(2 pi w/kappa) - 1): Planck's law at k_B T = hbar kappa/2 pi, as emission, for every Omega", ok)
    zeta2 = sum(1 / k**2 for k in range(1, 200001))
    flux = zeta2 / (2 * pi)                                              # (1/2 pi) int w n dw, T = 1
    check("L19c the energy flux of one massless 1+1 field is pi T^2/12, the one-dimensional Stefan-Boltzmann law (the 3+1"
          " grey-body factors behind the mass-loss rate stay quoted: Carr et al.)", abs(flux / (pi / 12) - 1) < 1e-5)


def log10_ratio(a, b):
    from math import log10
    return log10(a / b)



def main():
    t0 = time.time()
    for rung in (rung1, rung2, rung3, rung4, rung5, rung6, links, links_more):
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
    print("   Nine more links follow: de Sitter's horizon has entropy 3 pi/Lambda = pi x 3/(G Lambda), 3.3e122, and"
          " is the maximum;")
    print("   rung 1's breaking scale gives a seesaw neutrino mass scaling as 1/w, with the Yukawas left free; the")
    print("   first post-Newtonian correction to the experiment's phase is 1e-23 rad; the cosmological constant is")
    print("   the Planck vacuum energy divided by 8 S_dS/3 and is not explained; and the ringdown fit, the ABJ")
    print("   anomaly coefficient, the rho parameter's top loop and Hawking's Planck spectrum, quoted until now,")
    print("   are derived (the M_Z correction beyond the top loop and the microstates")
    print("   of S_dS are not).")
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
