"""The oracle: differential comparison of a build against the reference implementation.

VERIFIER ONLY. A builder must not read this file, src/, tests/, results/ or the repository's
.md pages for the stage it is building. Otherwise the rebuild is no longer independent and
proves nothing.

Two kinds of comparison:
  * differential: the build and src/ladder_standalone.py are called on the SAME arguments,
    including random ones, and must agree (the build may be more precise, never less);
  * pinned: headline numbers the repository publishes, which the build must reproduce
    from inputs.py.
A disagreement is a FINDING, not automatically a build error: the reference can be wrong too.
The verifier triages every one (rebuild/prompts/verifier.md).
"""
import importlib.util
import os
import random
from fractions import Fraction as F
from math import pi, sqrt

HERE = os.path.dirname(os.path.abspath(__file__))
REF_PATH = os.path.join(HERE, "..", "src", "ladder_standalone.py")


def load_reference():
    spec = importlib.util.spec_from_file_location("_ladder_reference", REF_PATH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _rel(a, b):
    return abs(a - b) / max(abs(b), 1e-300)


def _cmp(label, got, want, rtol, note=""):
    ok = got is not None and _rel(got, want) <= rtol
    return (label, ok, f"build {got!r} vs reference {want!r} (rtol {rtol:g}){'; ' + note if note else ''}")


def _run(items):
    out = []
    for label, thunk in items:
        try:
            out.extend(thunk())
        except Exception as e:
            out.append((label, False, f"raised {type(e).__name__}: {e}"))
    return out


# ------------------------------------------------------------------------------------------
def toolkit(m, L):
    t = m["toolkit"]
    def eig():
        rng = random.Random(7)
        A = [[rng.uniform(-1, 1) for _ in range(6)] for _ in range(6)]
        A = [[A[i][j] + A[j][i] for j in range(6)] for i in range(6)]
        a, b = t.eigvalsh(A), L.jacobi_eigenvalues(A)
        return [("eigenvalues agree with reference Jacobi", max(abs(x - y) for x, y in zip(a, b)) < 1e-10, f"{a}")]
    return _run([("eig", eig)])


def gauge331(m, L):
    G = m["gauge331"]
    out = []
    rng = random.Random(11)
    for var in ("-1/sqrt3", "+1/sqrt3"):
        def mm(var=var):
            worst = 0.0
            for _ in range(5):
                args = (rng.uniform(0.3, 1), rng.uniform(0.3, 1.2), rng.uniform(500, 9000), rng.uniform(10, 200), rng.uniform(10, 200))
                A, B = G.mass_matrix(var, *args), L.mass_matrix(var, *args)
                sc = max(abs(B[i][j]) for i in range(9) for j in range(9))
                worst = max(worst, max(abs(A[i][j] - B[i][j]) for i in range(9) for j in range(9)) / sc)
            return [(f"{var}: mass matrix equals reference on 5 random points", worst < 1e-12, f"max rel diff {worst:.1e}")]

        def charges(var=var):
            ok = True
            for Nc in (3, 5, 7):
                ferm, _, Qu, Qd = L.model(Nc, var)
                ok &= tuple(G.quark_charges(Nc)) == (Qu, Qd)
                for X in (F(-1, 3), F(2, 3), F(1, 6)):
                    ok &= list(G.triplet_charges(X, var)) == L.triplet_charges(X, var)
                    ok &= list(G.triplet_charges(X, var, True)) == L.triplet_charges(X, var, True)
            return [(f"{var}: charges equal reference exactly", ok, "")]
        def closed(var=var):
            # closed-form derivation results, moved here from the blind checks (leak 3, build 2026-11-a)
            g, gX, w, v1, v2 = 0.652, 0.79, 4000.0, 150.0, 190.0
            beta = (-1 if var.startswith("-") else 1) / sqrt(3)
            n = G.photon_direction(var, g, gX)
            want = [0, 0, 1 / g, 0, 0, 0, 0, beta / g, 1 / gX]
            cos = abs(sum(a * b for a, b in zip(n, want))) / (sqrt(sum(x * x for x in n)) * sqrt(sum(x * x for x in want)))
            M = G.mass_matrix(var, g, gX, w, v1, v2)
            v2s = v1 * v1 + v2 * v2
            mw2 = (M[0][0] + M[1][1]) / 2
            MZ2, MZp2 = G.neutral_masses(var, g, gX, w, v1, v2)
            gY2 = 1 / (beta**2 / g**2 + 1 / gX**2)
            eps = v2s / w**2
            cw2 = g * g / (g * g + gY2)
            rho = lambda W: (lambda A: (A[0][0] + A[1][1]) / 2)(G.mass_matrix(var, g, gX, W, v1, v2)) / \
                (G.neutral_masses(var, g, gX, W, v1, v2)[0] * cw2)
            r1, r2 = rho(w), rho(2 * w)
            return [(f"{var}: photon along Q = T3 + beta T8 + X", abs(cos - 1) < 1e-12, f"cos {cos}"),
                    _cmp(f"{var}: 1/e^2 = (1 + beta^2)/g^2 + 1/gX^2", G.inv_e2(var, g, gX), (1 + beta**2) / g**2 + 1 / gX**2, 1e-12),
                    _cmp(f"{var}: M_W^2 = g^2 v^2/4", mw2, g * g * v2s / 4, 1e-12),
                    _cmp(f"{var}: M_Z^2 = (g^2 + gY^2) v^2/4 at leading order", MZ2, (g * g + gY2) * v2s / 4, 5 * eps),
                    _cmp(f"{var}: M_Z'^2 = (g^2 + beta^2 gX^2) w^2/3 at leading order", MZp2, (g * g + beta**2 * gX**2) * w * w / 3, 5 * eps),
                    (f"{var}: rho >= 1 and rho - 1 ~ (v/w)^2", r1 > 1 and 3.9 < (r1 - 1) / (r2 - 1) < 4.1, f"rho - 1 = {r1 - 1:.3e}")]
        out += _run([("mm", mm), ("charges", charges), ("closed", closed)])

    def data():
        v = G.vev_from_GF(L.G_F)
        mz = G.mz_tree(L.G_F, L.ALPHA_MZ_INV, L.S2_MZ)
        return [_cmp("v from G_F = 246.22 GeV", v, 246.22, 4e-5),
                _cmp("tree-level M_Z = 91.51 GeV (measured 91.19; +0.35% is the loop correction)",
                     mz, sqrt(pi / L.ALPHA_MZ_INV / (sqrt(2) * L.G_F) / (L.S2_MZ * (1 - L.S2_MZ))), 1e-12)]
    return out + _run([("data", data)])


def chiral(m, L):
    C = m["chiral"]
    def vals():
        r = [_cmp("GMOR pion mass 127.6 MeV", C.gmor_mpi(L.MU_PLUS_MD, L.COND_13, L.F_PI),
                  sqrt(L.MU_PLUS_MD * L.COND_13**3) / L.F_PI, 1e-12)]
        Fc = L.F_PI / L.FPI_OVER_F
        M2 = 2 * L.M_UD_FLAG * L.COND_13**3 / Fc**2
        ref = sqrt(M2 * (1 - M2 / (32 * pi * pi * Fc * Fc) * L.LBAR3))
        r.append(_cmp("O(p^4) pion mass 132.6 MeV", C.chpt_mpi(L.M_UD_FLAG, L.COND_13, L.FPI_OVER_F, L.LBAR3, L.F_PI), ref, 1e-12))
        r.append(_cmp("nuclear range 1/m_pi = 1.414 fm (via yukawa decay length)",
                      -1 / ((__import__("math").log(C.yukawa(1.01, L.M_PIC / L.HBARC_GEV_FM) * 1.01)
                             - __import__("math").log(C.yukawa(1.0, L.M_PIC / L.HBARC_GEV_FM) * 1.0)) / 0.01),
                      L.HBARC_GEV_FM / L.M_PIC, 1e-9))
        for lam, v, H in ((2.0, 1.0, 0.05), (1.0, 2.0, 0.01)):
            s0, mpi2 = C.sigma_model_vacuum(lam, v, H)
            r.append(_cmp(f"m_pi^2 = H/<sigma> at the vacuum (lambda {lam}, v {v}, H {H})", mpi2, H / s0, 1e-5))
        LL = _src("ladder_links")
        Fw = LL.fpi_from_weak()[1] / sqrt(2) / L.FPI_OVER_F
        M2w = 2 * L.M_UD_FLAG * L.COND_13**3 / Fw**2
        r.append(_cmp("O(p^4) pion mass from the weak decay's f_pi: 132.29 MeV (force chain stage 4)", C.chpt_mpi_from_rungs(),
                      sqrt(M2w * (1 - M2w / (32 * pi * pi * Fw * Fw) * L.LBAR3)), 1e-8))
        r.append(_cmp("Goldberger-Treiman g_piNN = 13.01", C.goldberger_treiman(L.G_A, L.M_N, L.F_PI), L.G_A * L.M_N / L.F_PI, 1e-12))
        r.append(_cmp("Yukawa normalization", C.yukawa(0.7, 1.3), __import__("math").exp(-1.3 * 0.7) / (4 * pi * 0.7), 1e-12))
        return r
    return _run([("vals", vals)])


def casimir(m, L):
    P = m["casimir"]
    def vals():
        r = [("sphere K = (eps-1)/(eps+2) exactly", P.sphere_K(F(57, 10)) == F(47, 77), f"{P.sphere_K(F(57, 10))}"),
             ("fluctuation integral = 23/4 exactly", P.cp_integral() == F(23, 4), f"{P.cp_integral()}")]
        g1, g2 = P.green_tensor(0.37, -0.29, 0.41, 1.7), L.green(0.37, -0.29, 0.41, 1.7)
        r.append(("Green tensor equals reference", max(abs(g1[i][j] - g2[i][j]) for i in range(3) for j in range(3)) < 1e-12, ""))
        mA, rr = L.geomspace(1e-16, 1e-12, 25)[13], 200e-6
        R = P.diamond_radius(mA)
        K = (L.EPS_DIAMOND - 1) / (L.EPS_DIAMOND + 2)
        Uc = P.cp_energy(R, R, K, K, rr)
        Ug = -L.G_NEWTON * mA * mA / rr
        r.append(_cmp("Casimir/gravity at 200 um, design A = 2.335e-2 (pinned)", Uc / Ug, 2.335e-2, 1e-2))
        r.append(_cmp("Casimir energy equals reference formula", Uc,
                      -23 / (4 * pi) * L.HBAR * L.C_LIGHT * (K * L.diamond_radius(mA) ** 3) ** 2 / rr**7, 1e-10))
        gap = P.casimir_safe_gap(1e-14, 250e-6, 2.5, 0.1)
        ref_grid = L.casimir_safe_gap()
        step = (1e3) ** (1 / 3999) - 1
        r.append(("safe gap: build's root lies within one reference grid step below 181.16 um",
                  ref_grid * (1 - 1.01 * step) <= gap <= ref_grid * (1 + 1e-6),
                  f"build {gap * 1e6:.4f} um, reference grid point {ref_grid * 1e6:.4f} um (grid step {step * 100:.2f}%)"))
        return r
    return _run([("vals", vals)])


def graviton(m, L):
    Gr = m["graviton"]
    def vals():
        r = [("h00 = hii = 2 (units GM/c^2 r)", tuple(Gr.point_mass_metric()) == (2, 2), f"{Gr.point_mass_metric()}"),
             ("static masses: T.P.T = m1 m2 / 2", Gr.tpt((F(1), 0, 0, 0), (F(1), 0, 0, 0)) == F(1, 2), "")]
        ok = all(abs(Gr.ramp_profile(t, 0.3, 0.7) - L.ramp_profile(t, 0.3, 0.7)) < 1e-14 for t in [0.017 * k for k in range(100)])
        r.append(("branch profile equals reference", ok, ""))
        gap = L.casimir_safe_gap()                                  # same gap as the reference, isolating the phase
        mA, dx = L.geomspace(1e-16, 1e-12, 25)[13], L.geomspace(10e-6, 3e-3, 25)[18]
        hold, ramp = L.geomspace(0.05, 20, 25)[2], L.geomspace(0.05, 5, 17)[12]
        r.append(_cmp("design A entangling phase = 2.1868 rad (pinned), at the reference gap",
                      Gr.entangling_phase(mA, dx, hold, ramp, gap), 2.1868, 5e-4))
        r.append(_cmp("design_phase at the build's own Casimir root: within the reference grid's 0.17% of 2.1868",
                      Gr.design_phase(), 2.1868, 3e-3, "the reference picks the first point of a 4000-point log grid"))
        return r
    return _run([("vals", vals)])


def desitter(m, L):
    D = m["desitter"]
    def vals():
        ok = all(D.so41_generator(A, B) == L.J(A, B) for A in range(5) for B in range(5))
        xs, f, fp = [0.2, 2.3, 1.1, 0.4], (lambda r: 1 - 0.6 / r - r * r / 49), (lambda r: 0.6 / r**2 - 2 * r / 49)
        (E1, w1), (E2, w2) = D.spin_connection(xs, f, fp), L.tetrad_and_spin(xs, f, fp)
        sc = max(abs(E1[a][m] - E2[a][m]) for a in range(4) for m in range(4)) + \
            max(abs(w1[a][b][m] - w2[a][b][m]) for a in range(4) for b in range(4) for m in range(4))
        rng = random.Random(23)
        for _ in range(4):
            M_, l_ = rng.uniform(0.05, 0.4), rng.uniform(6.0, 12.0)
            p_ = [rng.uniform(-1, 1), rng.uniform(1.5, 3.0), rng.uniform(0.3, 2.8), rng.uniform(0, 6)]
            f_ = lambda r, M_=M_, l_=l_: 1 - 2 * M_ / r - r * r / l_**2
            fp_ = lambda r, M_=M_, l_=l_: 2 * M_ / r**2 - 2 * r / l_**2
            (Ea, wa), (Eb, wb) = D.spin_connection(p_, f_, fp_), L.tetrad_and_spin(p_, f_, fp_)
            sc = max(sc, max(abs(Ea[a][m] - Eb[a][m]) for a in range(4) for m in range(4)) +
                     max(abs(wa[a][b][m] - wb[a][b][m]) for a in range(4) for b in range(4) for m in range(4)))
        cR, cV = D.action_coefficients(0.3, 7.0, [0.2, 2.3, 1.1, 0.4])
        return [("so(4,1) generators equal reference", ok, ""),
                ("tetrad and spin connection equal reference at 5 points (index convention included)", sc < 1e-12, f"diff {sc:.1e}"),
                _cmp("eps R^e^e = 2 e R", cR, 2.0, 1e-6), _cmp("eps e^e^e^e = 24 e", cV, 24.0, 1e-9),
                *[_cmp(f"Ricci scalar of SdS = 12/l^2 (M {M_}, l {l_})", D.ricci_scalar(M_, l_, p_), 12 / l_**2, 1e-7)
                  for M_, l_, p_ in ((0.3, 7.0, [0.2, 2.3, 1.1, 0.4]), (0.0, 4.0, [0.0, 1.7, 0.5, 2.0]),
                                     (0.1, 11.0, [0.0, 3.1, 0.7, 1.2]))],
                _cmp("Lambda l^2 = 3", 1.7e-52 * D.ell_from_lambda(1.7e-52) ** 2, 3.0, 1e-12),
                _cmp("measured Lambda: l = 1.647e26 m (pinned)", D.ell_from_lambda(L.LAMBDA_SI), 1.647e26, 1e-3),
                _cmp("MacDowell-Mansouri coupling 1.04e122 (pinned)", D.mm_coupling(L.LAMBDA_SI, L.L_PLANCK), 1.04e122, 1e-2)]
    return _run([("vals", vals)])


def blackholes(m, L):
    B = m["blackholes"]
    def vals():
        r = []
        rb, rc = B.sds_horizons(1.0, 9.0)
        Rb, Rc = L.sds_horizons(1.0, 9.0)
        r += [_cmp("SdS black-hole horizon", rb, Rb, 1e-12), _cmp("SdS cosmological horizon", rc, Rc, 1e-12)]
        kb, kc = B.kappa_from_spin_connection(1.0, 9.0)
        fp = lambda x: 2 / x**2 - 2 * x / 81
        r += [_cmp("kappa_b from rung 5 = f'(r_b)/2", kb, fp(Rb) / 2, 1e-7), _cmp("kappa_c from rung 5", kc, -fp(Rc) / 2, 1e-7)]
        f9 = lambda x: 1 - 2 / x - x * x / 81
        r += [_cmp("Killing kappa_b = f'(r_b)/2", B.killing_kappa(f9, Rb * (1 + 1e-6), 1e-8 * Rb), fp(Rb) / 2, 1e-5),
              _cmp("Killing kappa_c = -f'(r_c)/2", B.killing_kappa(f9, Rc * (1 - 1e-6), 1e-8 * Rc), -fp(Rc) / 2, 1e-5),
              _cmp("Euclidean section smooth at period 2 pi/(f'/2)",
                   B.euclidean_cone_ratio(f9, Rb, 2 * pi / (fp(Rb) / 2), 1e-7 * Rb), 1.0, 1e-5)]
        r.append(_cmp("Schwarzschild kappa = 1/4M", B.killing_kappa(lambda x: 1 - 2 / x, 2.0 + 2e-6, 2e-8), 0.25, 1e-5))
        rp, bc = B.photon_sphere()
        r += [_cmp("photon sphere 3M", rp, 3.0, 1e-7), _cmp("shadow radius sqrt(27) M", bc, sqrt(27), 1e-10)]
        ri, L2, E2 = B.isco()
        r += [_cmp("ISCO 6M", ri, 6.0, 2e-4), _cmp("ISCO L^2 = 12", L2, 12.0, 1e-6), _cmp("ISCO E^2 = 8/9", E2, 8 / 9, 1e-6)]
        r.append(_cmp("largest black hole 4.269e52 kg (pinned)", B.nariai_mass_kg(L.LAMBDA_SI), 4.269e52, 1e-3))
        r.append(_cmp("M87* shadow from stellar mass", B.shadow_uas(L.M87_STARS[0], L.M87_STARS[2]),
                      L.shadow_uas(L.M87_STARS[0], L.M87_STARS[2]), 1e-12))
        mf, chi = B.invert_220(L.F220[0], L.G220[0], L.GW_Z[0])
        Mf, Chi = L.invert_220(L.F220[0], L.G220[0], L.GW_Z[0])
        r += [_cmp("GW250114 ringdown remnant mass", mf, Mf, 1e-10), _cmp("GW250114 ringdown spin", chi, Chi, 1e-10)]
        r.append(_cmp("GW250114 final area", B.kerr_area_km2(mf, chi), L.kerr_area_km2(Mf, Chi), 1e-10))
        f2, g2 = B.qnm_220((1 + L.GW_Z[0]) * L.GW_MF, L.GW_CHIF)
        F2, G2 = L.qnm_220((1 + L.GW_Z[0]) * L.GW_MF, L.GW_CHIF)
        r += [_cmp("220 frequency from the full-signal remnant", f2, F2, 1e-12), _cmp("220 damping", g2, G2, 1e-12)]
        r.append(_cmp("Hawking temperature of GW250114's remnant", B.hawking_K(L.GW_MF * L.GM_SUN / L.G_NEWTON),
                      L.hawking_K(L.GW_MF * L.GM_SUN / L.G_NEWTON), 1e-12))
        return r
    return _run([("vals", vals)])


def links(m, L):
    Lk = m["links"]
    def vals():
        mA = L.geomspace(1e-16, 1e-12, 25)[13]
        mpl = Lk.planck_mass_GeV(L.G_NEWTON, L.HBAR, L.C_LIGHT)
        lo, _ = Lk.g_window(*L.POLES_331["+1/sqrt3"], mpl)
        T3, M_ = _src("m331_three_loop"), _src("m331_margin")
        gw = []
        for var in ("-1/sqrt3", "+1/sqrt3"):
            p3 = T3.pole(3, var, MV=4e3, loops=1, thresholds=False, yukawas=False, gmax=M_.ALPHA1)
            p5 = T3.pole(5, var, MV=4e3, loops=1, thresholds=False, yukawas=False, gmax=M_.ALPHA1)
            got, want = Lk.g_window_from_rungs(var), ((mpl / p3) ** 2, (mpl / p5) ** 2)
            gw.append(_cmp(f"{var}: G window from the one-loop poles", got[0], want[0], 1e-5))
            gw[-1] = (gw[-1][0], gw[-1][1] and _rel(got[1], want[1]) < 1e-5, gw[-1][2])
        return gw + [_cmp("neutrality needed: 2.82e-19 e per nucleon (pinned)", Lk.neutrality_per_nucleon(mA), 2.82e-19, 2e-3),
                _cmp("pi0 width 7.785 eV", Lk.pi0_width_eV(L.ALPHA_0, L.F_PI, L.M_PI0, 3, F(2, 3), F(-1, 3)), 7.785, 3e-4),
                _cmp("Planck mass 1.22089e19 GeV (pinned)", mpl, 1.22089e19, 1e-6),
                _cmp("G window lower edge: fails for G 8.18x weaker (pinned)", 1 / lo, 8.18, 1e-2),
                _cmp("design A Schwarzschild radius 2.180e-41 m (pinned)", Lk.schwarzschild_radius(mA), 2.180e-41, 1e-3),
                _cmp("pi0 width from rung 1's charges and the weak decay's f_pi: 7.7417 eV (force chain)",
                     Lk.pi0_width_from_rungs(), 7.74175, 1e-5),
                _cmp("Planck-mass black hole k_B T = 4.86e17 GeV", Lk.planck_bh_kT_GeV(), 1.22089e19 / (8 * pi), 1e-6),
                ("rung 1's matter charges (1, 0, -1, 0)", tuple(Lk.matter_charges(3, "+1/sqrt3")) == (1, 0, -1, 0), "")]
    return _run([("vals", vals)])


def _src(name):
    """A src/ module by name (verifier only): the 3-3-1 running and the weak decay live there."""
    import sys
    d = os.path.join(HERE, "..", "src")
    if d not in sys.path:
        sys.path.insert(0, d)
    return importlib.import_module(name)


def running(m, L):
    R = m["running"]

    def coeffs():
        E = _src("m331_exact")
        out = [("SM one-loop coefficients (b_Y, b_2) = (41/6, -19/6)", tuple(R.sm_coefficients()) == (F(41, 6), F(-19, 6)),
                f"{R.sm_coefficients()}")]
        for var in ("-1/sqrt3", "+1/sqrt3"):
            bad = []
            for Nc in (1, 3, 5, 7):
                a, _ = E.coefficients(*E.MODELS[var](Nc)[:3])
                if tuple(R.b_331(Nc, var)) != (a[0], a[1]):
                    bad.append((Nc, R.b_331(Nc, var), (a[0], a[1])))
            out.append((f"{var}: b_331 equals src's field content (N_c = 1, 3, 5, 7)", not bad, f"{bad}" if bad else "exact"))
        return out

    def boundary():
        from math import log
        out = []
        s2, ainv, mz = L.S2_MZ, L.ALPHA_MZ_INV, 91.188
        t = log(4e3 / mz) / (2 * pi)
        aY, a2 = (1 - s2) * ainv - 41 / 6 * t, s2 * ainv + 19 / 6 * t
        y, w = R.couplings_at(4e3)
        out += [_cmp("1/alpha_Y(4 TeV), one loop", y, aY, 1e-12), _cmp("1/alpha_2(4 TeV), one loop", w, a2, 1e-12)]
        for var in ("-1/sqrt3", "+1/sqrt3"):
            out.append(_cmp(f"{var}: 1/alpha_X(4 TeV) = 1/alpha_Y - beta^2/alpha_2", R.matching_331(4e3, var)[0], aY - a2 / 3, 1e-12))
        return out

    def poles():
        T3, M = _src("m331_three_loop"), _src("m331_margin")
        out = []
        mpl = 1.22089e19
        for var in ("-1/sqrt3", "+1/sqrt3"):
            p3, p5 = R.landau_pole(3, var), R.landau_pole(5, var)
            for Nc, p in ((3, p3), (5, p5)):
                ref = T3.pole(Nc, var, MV=4e3, loops=1, thresholds=False, yukawas=False, gmax=M.ALPHA1)
                out.append(_cmp(f"{var}: one-loop pole, N_c = {Nc}, equals src's one-loop running", p, ref, 1e-6,
                                "src integrates the same one-loop equation numerically"))
            out.append((f"{var}: the one-loop poles select N_c = 3 (pole_5 < M_Pl < pole_3)", p5 < mpl < p3,
                        f"pole_3 = {p3:.3e}, pole_5 = {p5:.3e} GeV"))
            q3, q5 = L.POLES_331[var] if hasattr(L, "POLES_331") else __import__("inputs").POLES_331[var]
            out.append((f"{var}: one loop within a factor 1.3-2.1 of three loops (pinned)",
                        1.3 < p3 / q3 < 2.1 and 1.3 < p5 / q5 < 2.1, f"{p3 / q3:.3f}, {p5 / q5:.3f}"))
        return out
    return _run([("coeffs", coeffs), ("boundary", boundary), ("poles", poles)])


def weak(m, L):
    W = m["weak"]

    def vals():
        LL = _src("ladder_links")
        rng = random.Random(91)
        worst = 0.0
        for _ in range(5):
            f, GF, V, ml, mp = rng.uniform(0.05, 0.2), rng.uniform(5e-6, 2e-5), rng.uniform(0.9, 1), rng.uniform(0.01, 0.1), 0.14
            want = GF**2 * V**2 * f**2 * ml**2 * mp * (1 - ml**2 / mp**2) ** 2 / (8 * pi)
            worst = max(worst, abs(W.pion_decay_width(f, GF, V, ml, mp) / want - 1))
        return [("pion_decay_width = G_F^2 |V_ud|^2 f^2 m_l^2 m_pi (1 - m_l^2/m_pi^2)^2 / 8 pi (5 random points)",
                 worst < 1e-12, f"max rel diff {worst:.1e}"),
                _cmp("f_pi from G_F and pi -> mu nu = 130.57 MeV (src/ladder_links.fpi_from_weak, force chain stage 3)",
                     W.fpi_from_pion_decay(), LL.fpi_from_weak()[1], 1e-8, "hbar in GeV s from HBAR/E_CH vs src's constant")]
    return _run([("vals", vals)])


BY_STAGE = {"toolkit": toolkit, "gauge331": gauge331, "chiral": chiral, "casimir": casimir,
            "graviton": graviton, "desitter": desitter, "blackholes": blackholes, "running": running,
            "weak": weak, "links": links}
