"""Blind checks: properties a correct build must have, with NO reference answers.

The builder may read and run these. They test identities, limits, symmetries, internal
consistency between two routes, and scaling laws. Scaling laws catch hard-coded answers: a
function that returns a typed constant can't scale correctly when its arguments change.

Each stage function takes {module_name: module} for the build and returns a list of
(label, ok, detail) tuples.
"""
import random
from fractions import Fraction as F
from math import isfinite, pi, sqrt


def _rel(a, b):
    return abs(a - b) / max(abs(b), 1e-300)


def _safe(fn, *a, **k):
    try:
        return fn(*a, **k), None
    except Exception as e:                     # a crash is a failed check, not a harness error
        return None, f"{type(e).__name__}: {e}"


def run_safely(checks):
    """Wrap each check thunk so an exception becomes a failure with its message."""
    out = []
    for label, thunk in checks:
        try:
            ok, detail = thunk()
        except Exception as e:
            ok, detail = False, f"raised {type(e).__name__}: {e}"
        out.append((label, bool(ok), detail))
    return out


# ------------------------------------------------------------------------------------------
def toolkit(m):
    t = m["toolkit"]
    rng = random.Random(1)

    def eig():
        # a random rotation of diag(1, 2, 3, 4)
        n = 4
        Q = [[rng.gauss(0, 1) for _ in range(n)] for _ in range(n)]
        for i in range(n):                                         # Gram-Schmidt
            for j in range(i):
                d = sum(Q[i][k] * Q[j][k] for k in range(n))
                Q[i] = [Q[i][k] - d * Q[j][k] for k in range(n)]
            nr = sqrt(sum(x * x for x in Q[i]))
            Q[i] = [x / nr for x in Q[i]]
        D = [1.0, 2.0, 3.0, 4.0]
        A = [[sum(Q[k][i] * D[k] * Q[k][j] for k in range(n)) for j in range(n)] for i in range(n)]
        ev = t.eigvalsh(A)
        return max(abs(a - b) for a, b in zip(ev, D)) < 1e-10, f"got {ev}"

    def hess():
        H = t.hessian(lambda x: x[0] ** 2 + 3 * x[0] * x[1] + x[1] ** 3, [0.5, 2.0])
        want = [[2, 3], [3, 12]]
        return max(abs(H[i][j] - want[i][j]) for i in range(2) for j in range(2)) < 1e-5, f"got {H}"

    def exact():
        d = t.exact_derivative(lambda x: (x * x * x + 1) / (x - 3), F(2))
        want = F(3 * 4 * (2 - 3) - (8 + 1), (2 - 3) ** 2)
        return d == want and isinstance(d, F), f"got {d!r}, want {want!r}"

    def roots():
        r = t.bisect(lambda x: x * x - 2, 0.0, 2.0)
        g = t.golden_max(lambda x: -(x - 0.3) ** 2, -1.0, 2.0)
        return abs(r - sqrt(2)) < 1e-12 and abs(g - 0.3) < 1e-7, f"bisect {r}, golden {g}"

    def trap():
        n = 2001
        ys = [__import__("math").sin(pi * i / (n - 1)) for i in range(n)]
        v = t.trapezoid(ys, pi / (n - 1))
        return abs(v - 2) < 1e-6, f"int sin = {v}"

    def eps():
        ok = t.levi_civita([0, 1, 2, 3]) == 1 and t.levi_civita([1, 0, 2, 3]) == -1
        ok &= t.levi_civita([0, 0, 2, 3]) == 0 and t.levi_civita([3, 2, 1, 0]) == 1
        return ok, ""

    return run_safely([("Jacobi eigenvalues of a rotated diag(1,2,3,4)", eig),
                       ("central-difference Hessian of x^2 + 3xy + y^3", hess),
                       ("exact rational derivative by dual numbers", exact),
                       ("bisection and golden section", roots),
                       ("trapezoid rule, int_0^pi sin = 2", trap),
                       ("permutation parity", eps)])


# ------------------------------------------------------------------------------------------
def gauge331(m):
    G, t = m["gauge331"], m["toolkit"]
    g, gX, w, v1, v2 = 0.652, 0.79, 4000.0, 150.0, 190.0
    beta = {"-1/sqrt3": -1 / sqrt(3), "+1/sqrt3": 1 / sqrt(3)}
    checks = []
    for var in ("-1/sqrt3", "+1/sqrt3"):
        def zero_mode(var=var):
            M = G.mass_matrix(var, g, gX, w, v1, v2)
            ev = t.eigvalsh(M)
            sc = max(abs(x) for x in ev)
            nz = sum(abs(x) < 1e-12 * sc for x in ev)
            n = G.photon_direction(var, g, gX)
            res = max(abs(sum(M[i][k] * n[k] for k in range(9))) for i in range(9))
            return nz == 1 and res < 1e-9 * sc, f"{nz} zero eigenvalues, |M n| = {res:.2e}"

        def photon_form(var=var):
            # properties only: the photon is neutral (it lies in the Cartan directions 2, 7, 8),
            # it is massless for ANY vevs, and e is homogeneous of degree 1 in the couplings
            # and weaker than either coupling alone
            n = G.photon_direction(var, g, gX)
            nn = sqrt(sum(x * x for x in n))
            off = max(abs(n[k]) for k in (0, 1, 3, 4, 5, 6)) / nn
            rng = random.Random(5)
            worst = 0.0
            for _ in range(3):
                M = G.mass_matrix(var, g, gX, rng.uniform(500, 9000), rng.uniform(10, 200), rng.uniform(10, 200))
                sc = max(abs(M[i][j]) for i in range(9) for j in range(9))
                worst = max(worst, max(abs(sum(M[i][k] * n[k] for k in range(9))) for i in range(9)) / (sc * nn))
            ie2 = G.inv_e2(var, g, gX)
            hom = _rel(G.inv_e2(var, 2 * g, 2 * gX), ie2 / 4)
            return off < 1e-12 and worst < 1e-12 and hom < 1e-12 and ie2 > 1 / g**2 and ie2 > 1 / gX**2, \
                f"charged components {off:.1e}, |M n| on random vevs {worst:.1e}, homogeneity {hom:.1e}"

        def step1(var=var):
            M0 = G.mass_matrix(var, g, gX, w, 0.0, 0.0)
            ev = t.eigvalsh(M0)
            nz = sum(abs(x) < 1e-12 * max(ev) for x in ev)
            return nz == 4, f"{nz} massless states with v = 0 (SU(2) x U(1)_Y needs 4)"

        def masses(var=var):
            # properties only: neutral_masses are eigenvalues of mass_matrix; the W mass does not
            # depend on w and scales as v^2; M_Z decouples from w and M_Z' grows as w^2
            M = G.mass_matrix(var, g, gX, w, v1, v2)
            ev = t.eigvalsh(M)
            MZ2, MZp2 = G.neutral_masses(var, g, gX, w, v1, v2)
            sc = max(abs(x) for x in ev)
            ok = all(min(abs(x - y) for x in ev) < 1e-9 * sc for y in (MZ2, MZp2)) and 0 < MZ2 < MZp2
            mw = lambda W, a, b: (lambda A: (A[0][0] + A[1][1]) / 2)(G.mass_matrix(var, g, gX, W, a, b))
            ok &= _rel(mw(2 * w, v1, v2), mw(w, v1, v2)) < 1e-12 and _rel(mw(w, 2 * v1, 2 * v2), 4 * mw(w, v1, v2)) < 1e-12
            z = [G.neutral_masses(var, g, gX, W, v1, v2) for W in (w, 2 * w, 4 * w)]
            eps = (v1 * v1 + v2 * v2) / w**2
            ok &= _rel(z[1][0], z[2][0]) < 5 * eps and _rel(z[1][1], 4 * z[0][1]) < 5 * eps and _rel(z[2][1], 4 * z[1][1]) < 5 * eps
            return ok, f"M_Z^2 {MZ2:.4g}, M_Z'^2 {MZp2:.4g}; scaling in w and v"

        def rho_scaling(var=var):
            # M_W^2/M_Z^2 approaches its w -> infinity value from above, with corrections ~ (v/w)^2
            def r(W):
                M = G.mass_matrix(var, g, gX, W, v1, v2)
                return (M[0][0] + M[1][1]) / 2 / G.neutral_masses(var, g, gX, W, v1, v2)[0]
            r1, r2, r4 = r(w), r(2 * w), r(4 * w)
            q = (r1 - r2) / (r2 - r4)
            return r1 > r2 > r4 and 3.9 < q < 4.1, f"M_W^2/M_Z^2 decreasing in w, successive-difference ratio {q:.3f}"

        def doublets(var=var):
            ok, bad = True, []
            for Nc in (3, 5, 7):
                Qu, Qd = G.quark_charges(Nc)
                pairs = G.doublet_charge_pairs(Nc, var)
                ok &= pairs == {frozenset({F(0), F(-1)}), frozenset({Qu, Qd})}
                if not ok:
                    bad.append((Nc, pairs))
            return ok, f"{bad}" if bad else "leptons (0, -1), quarks (Q_u, Q_d) for N_c = 3, 5, 7"

        checks += [(f"{var}: exactly one massless boson, along photon_direction", zero_mode),
                   (f"{var}: photon is neutral, massless for any vevs; e homogeneous", photon_form),
                   (f"{var}: four massless states after step 1", step1),
                   (f"{var}: W, Z, Z' masses are eigenvalues with the right v and w scaling", masses),
                   (f"{var}: M_W^2/M_Z^2 falls to its limit as (v/w)^2", rho_scaling),
                   (f"{var}: doublet charges for N_c = 3, 5, 7", doublets)]

    def charges():
        ok = True
        for Nc in range(1, 12, 2):
            Qu, Qd = G.quark_charges(Nc)
            ok &= isinstance(Qu, F) and Qu - Qd == 1
            ok &= F(Nc + 1, 2) * Qu + F(Nc - 1, 2) * Qd == 1          # proton charge 1
        Qu3, Qd3 = G.quark_charges(3)
        return ok, f"N_c = 3: ({Qu3}, {Qd3})"

    def neutral_vevs():
        ok = True
        for var in ("-1/sqrt3", "+1/sqrt3"):
            for X in (F(-1, 3), F(2, 3), F(1, 3), F(-2, 3)):
                q = G.triplet_charges(X, var)
                qa = G.triplet_charges(X, var, anti=True)
                ok &= q[0] - q[1] == 1 and qa[1] - qa[0] == 1 and sum(q) == 3 * X and sum(qa) == 3 * X
        return ok, "Q traceless part, antitriplet sign"

    def gf_scaling():
        v1_, v2_ = G.vev_from_GF(1e-5), G.vev_from_GF(4e-5)
        z1, z2 = G.mz_tree(1e-5, 128.0, 0.23), G.mz_tree(1e-5, 4 * 128.0, 0.23)
        return _rel(v1_ / v2_, 2) < 1e-12 and _rel(z1 / z2, 2) < 1e-12, "v ~ G_F^-1/2, M_Z ~ alpha^1/2"

    checks += [("anomaly-derived quark charges: Q_u - Q_d = 1 and q_p = 1 for odd N_c", charges),
               ("triplet charges: T3 spacing and trace 3X, antitriplet reversed", neutral_vevs),
               ("v ~ G_F^-1/2 and M_Z ~ alpha^1/2 (scaling, no constants)", gf_scaling)]
    return run_safely(checks)


# ------------------------------------------------------------------------------------------
def chiral(m):
    C = m["chiral"]

    def gold():
        n4 = C.goldstone_count(2.0, 1.0)
        n4b = C.goldstone_count(0.7, 3.0)
        return n4 == 3 and n4b == 3, f"{n4}, {n4b} zero modes"

    def gmor_form():
        ok = True
        for lam, v, H in ((2.0, 1.0, 0.05), (1.0, 2.0, 0.01)):
            s0, mpi2 = C.sigma_model_vacuum(lam, v, H)
            ok &= abs(lam * s0 * (s0 * s0 - v * v) - H) < 1e-10 and mpi2 > 0
            # Goldstone limit: m_pi^2 vanishes linearly as the explicit breaking H goes to 0
            a, b = C.sigma_model_vacuum(lam, v, 1e-2 * H)[1], C.sigma_model_vacuum(lam, v, 2e-2 * H)[1]
            ok &= _rel(b / a, 2) < 1e-3
        return ok, "true vacuum; m_pi^2 > 0 and linear in H as H -> 0"

    def gmor_scaling():
        a, b = C.gmor_mpi(1e-3, 0.3, 0.09), C.gmor_mpi(4e-3, 0.3, 0.09)
        c = C.gmor_mpi(1e-3, 0.3, 0.18)
        return _rel(b / a, 2) < 1e-12 and _rel(a / c, 2) < 1e-12, "m_pi ~ sqrt(m_q)/f_pi"

    def chpt_limit():
        # lbar3 = 0 must reduce to leading order with F = f_pi/(F_pi/F)
        lo = C.chpt_mpi(3e-3, 0.27, 1.06, 0.0, 0.092)
        want = sqrt(2 * 3e-3 * 0.27**3) / (0.092 / 1.06)
        hi = C.chpt_mpi(3e-3, 0.27, 1.06, 3.0, 0.092)
        return _rel(lo, want) < 1e-12 and hi < lo, f"lbar3 = 0 -> {lo}, LO {want}; lbar3 > 0 lowers it"

    def yuk():
        mm = 1.3
        h = 1e-4
        worst = 0.0
        for r in (0.3, 0.9, 2.1):
            V = lambda x: C.yukawa(x, mm)
            lap = (V(r + h) * (r + h) - 2 * V(r) * r + V(r - h) * (r - h)) / (h * h) / r
            worst = max(worst, abs(lap - mm * mm * V(r)) / (mm * mm * V(r)))
        e = 1e-4
        flux = -4 * pi * e * e * (C.yukawa(e + 1e-7, mm) - C.yukawa(e - 1e-7, mm)) / 2e-7
        return worst < 1e-5 and abs(flux - 1) < 1e-3, f"(lap - m^2)V residual {worst:.1e}, flux {flux:.5f}"

    def newton_limit():
        return _rel(C.yukawa(2.0, 0.0), 1 / (8 * pi)) < 1e-12, "m = 0 gives 1/(4 pi r)"

    def tens():
        rng = random.Random(3)
        worst = max(C.tensor_identity_residual([rng.uniform(-2, 2) for _ in range(3)]) for _ in range(5))
        return worst < 1e-12, f"residual {worst:.1e}"

    def gt():
        a, b = C.goldberger_treiman(1.27, 0.94, 0.092), C.goldberger_treiman(2 * 1.27, 0.94, 0.092)
        return _rel(b / a, 2) < 1e-12, "linear in g_A"

    return run_safely([("O(4) -> O(3): three Goldstone pions", gold),
                       ("sigma model: vacuum, and m_pi^2 linear in H (Goldstone limit)", gmor_form),
                       ("GMOR scaling", gmor_scaling),
                       ("ChPT reduces to leading order at lbar3 = 0", chpt_limit),
                       ("Yukawa solves (lap - m^2)V = -delta with unit flux", yuk),
                       ("Yukawa at m = 0 is Coulomb/Newton", newton_limit),
                       ("one-pion-exchange tensor identity", tens),
                       ("Goldberger-Treiman scaling", gt)])


# ------------------------------------------------------------------------------------------
def casimir(m):
    P = m["casimir"]

    def sphere():
        K = P.sphere_K(F(57, 10))
        ok = isinstance(K, F) and P.sphere_K(F(1)) == 0
        ok &= P.sphere_K(F(10 ** 9)) < 1 and P.sphere_K(F(10 ** 9)) > F(999, 1000)    # conductor limit
        return ok, f"K(5.7) exact Fraction; K(1) = 0; conductor limit -> 1"

    def wave_eq():
        pt, k, h = (0.37, -0.29, 0.41), 1.7, 1e-3
        G0 = P.green_tensor(*pt, k)
        def lap(i, j, hs):
            tot = 0.0
            for d in range(3):
                p1, p2 = list(pt), list(pt)
                p1[d] += hs
                p2[d] -= hs
                tot += (P.green_tensor(*p1, k)[i][j] - 2 * G0[i][j] + P.green_tensor(*p2, k)[i][j]) / (hs * hs)
            return tot
        sc = max(abs(G0[i][j]) for i in range(3) for j in range(3))
        worst = max(abs((4 * lap(i, j, h / 2) - lap(i, j, h)) / 3 - k * k * G0[i][j]) / (k * k * sc)
                    for i in range(3) for j in range(3))
        return worst < 1e-6, f"(lap - k^2) G residual {worst:.1e}"

    def static_limit():
        G0 = P.green_tensor(0.0, 0.0, 2.0, 0.0)          # k = 0: the static dipole field
        return abs(G0[0][0] - 1 / 8) < 1e-12 and abs(G0[2][2] + 2 / 8) < 1e-12, f"{G0[0][0]}, {G0[2][2]}"

    def integral_exact():
        I = P.cp_integral()
        return isinstance(I, F), f"{I!r} (a Fraction; its value is checked by the oracle)"

    def r7():
        a, b = P.cp_energy(1e-6, 1e-6, 0.6, 0.6, 1e-4), P.cp_energy(1e-6, 1e-6, 0.6, 0.6, 2e-4)
        c = P.cp_energy(2e-6, 1e-6, 0.6, 0.6, 1e-4)
        return a < 0 and _rel(a / b, 128) < 1e-12 and _rel(c / a, 8) < 1e-12, "U < 0, ~ R1^3 / r^7"

    def radius():
        return _rel(P.diamond_radius(8.0) / P.diamond_radius(1.0), 2) < 1e-12, "R ~ m^(1/3)"

    def gap_mass_free():
        a = P.casimir_safe_gap(1e-14, 250e-6, 2.5, 0.1)
        b = P.casimir_safe_gap(1e-13, 250e-6, 2.5, 0.1)
        c = P.casimir_safe_gap(1e-14, 250e-6, 9.0, 0.1)
        return _rel(a, b) < 1e-5 and _rel(a, c) < 1e-5, f"gap independent of mass and time: {a:.6e}, {b:.6e}, {c:.6e}"

    def gap_is_root():
        from inputs import G_NEWTON, HBAR
        m_, dx, tau, fr = 1e-14, 250e-6, 2.5, 0.1
        gp = P.casimir_safe_gap(m_, dx, tau, fr)
        R = P.diamond_radius(m_)
        K = P.sphere_K(5.7)
        def ratio(gap):
            d = sqrt(gap * gap + dx * dx)
            gr = 2 * G_NEWTON * m_ * m_ * (1 / gap - 1 / d)
            cs = 2 * (-P.cp_energy(R, R, K, K, gap) + P.cp_energy(R, R, K, K, d))
            return abs(cs) / abs(gr)
        return abs(ratio(gp) - fr) < 1e-4 * fr, f"Casimir/gravity at the gap = {ratio(gp):.7f}"

    return run_safely([("dielectric sphere K: exact, K(1) = 0, conductor limit", sphere),
                       ("Green tensor solves the imaginary-frequency wave equation", wave_eq),
                       ("Green tensor at k = 0 is the static dipole field", static_limit),
                       ("fluctuation integral is exact", integral_exact),
                       ("Casimir-Polder scaling R^3 R^3 / r^7, attractive", r7),
                       ("diamond radius ~ m^(1/3)", radius),
                       ("safe gap independent of mass and time", gap_mass_free),
                       ("safe gap is the root of Casimir = fraction x gravity", gap_is_root)])


# ------------------------------------------------------------------------------------------
def graviton(m):
    Gr = m["graviton"]

    def ppn():
        h00, hii = Gr.point_mass_metric()
        return isinstance(h00, F) and hii == h00 and h00 > 0, f"h00 = {h00}, hii = {hii} (gamma = hii/h00)"

    def light():
        T, Tph = (F(1), 0, 0, 0), (F(1), 0, 0, F(1))
        r = Gr.tpt(T, Tph) / Gr.tpt(T, T)
        return r == 2, f"photon/mass coupling ratio {r}"

    def symmetric():
        A, B = (F(3), F(1), F(2), F(5)), (F(2), F(7), F(1), F(1))
        return Gr.tpt(A, B) == Gr.tpt(B, A), "T2.P.T1 symmetric"

    def profile():
        ok = Gr.ramp_profile(0.0, 1.0, 2.0) == 0 and Gr.ramp_profile(2.5, 1.0, 2.0) == 1
        ok &= abs(Gr.ramp_profile(1.0, 1.0, 2.0) - 0.5) < 1e-12 and abs(Gr.ramp_profile(5.0, 1.0, 2.0)) < 1e-12
        return ok, "0 at start, 1/2 mid-ramp, 1 in hold, 0 at end"

    def scaling():
        args = (1e-14, 5e-4, 0.1, 1.0, 2e-4)
        a = Gr.entangling_phase(*args)
        b = Gr.entangling_phase(2e-14, *args[1:])
        return a > 0 and _rel(b / a, 4) < 1e-12, f"phase ~ m^2: {a:.4g} -> {b:.4g}"

    def hold_linear():
        p = lambda hold: Gr.entangling_phase(1e-14, 5e-4, hold, 1.0, 2e-4)
        d1, d2 = p(1.0) - p(0.5), p(1.5) - p(1.0)
        return _rel(d1, d2) < 1e-3, "phase grows linearly with hold time"

    def g_dependence():
        import inputs
        a = Gr.entangling_phase(1e-14, 5e-4, 0.1, 1.0, 2e-4)
        old = inputs.G_NEWTON
        try:
            inputs.G_NEWTON = 3 * old
            b = Gr.entangling_phase(1e-14, 5e-4, 0.1, 1.0, 2e-4)
        finally:
            inputs.G_NEWTON = old
        return _rel(b / a, 3) < 1e-12, "phase ~ G, read from inputs at call time (not cached)"

    def design():
        import inputs
        gap = m["casimir"].casimir_safe_gap(inputs.GAP_BASELINE_MASS, inputs.GAP_BASELINE_DX,
                                            inputs.GAP_BASELINE_TAU, inputs.GAP_FRACTION)
        a = Gr.design_phase()
        b = Gr.entangling_phase(inputs.DESIGN_A_MASS, inputs.DESIGN_A_DX, inputs.DESIGN_A_HOLD, inputs.DESIGN_A_RAMP, gap)
        old = inputs.EPS_DIAMOND
        try:
            inputs.EPS_DIAMOND = 3.0                  # weaker Casimir -> smaller gap -> larger phase
            c = Gr.design_phase()
        finally:
            inputs.EPS_DIAMOND = old
        return _rel(a, b) < 1e-12 and c > a, f"design phase {a:.5g} at casimir's gap; with eps = 3: {c:.5g}"

    def newton_from_yukawa():
        # the phase must be the m = 0 exchange potential: compare with an explicit 1/r integral
        import inputs
        args = (1e-14, 5e-4, 0.1, 1.0, 2e-4)
        total, n = 0.1 + 2.0, 4001
        ys = []
        for i in range(n):
            y = 0.5 * 5e-4 * Gr.ramp_profile(total * i / (n - 1), 0.1, 1.0)
            ys.append(2 * (1 / 2e-4 - 1 / sqrt(4e-8 + 4 * y * y)))
        want = inputs.G_NEWTON * 1e-28 / inputs.HBAR * total / (n - 1) * (sum(ys) - (ys[0] + ys[-1]) / 2)
        return _rel(Gr.entangling_phase(*args), want) < 1e-9, "phase = (G m^2/hbar) int [1/d] dt for 1/r"

    return run_safely([("design phase = entangling phase at casimir's safe gap, and responds to it", design),
                       ("the exchange potential is 1/r (Newton) along the branches", newton_from_yukawa),
                       ("linearized point mass: PPN gamma = 1", ppn),
                       ("light couples twice as strongly", light),
                       ("graviton contraction symmetric", symmetric),
                       ("branch profile shape", profile),
                       ("entangling phase ~ m^2", scaling),
                       ("entangling phase linear in hold time", hold_linear),
                       ("entangling phase ~ G (inputs read at call time)", g_dependence)])


# ------------------------------------------------------------------------------------------
def desitter(m):
    D = m["desitter"]
    x = [0.2, 2.3, 1.1, 0.4]

    def algebra():
        J = D.so41_generator
        ok = True
        for a in range(4):
            for b in range(4):
                Pa, Pb = J(a, 4), J(b, 4)
                cm = [[sum(Pa[i][k] * Pb[k][j] - Pb[i][k] * Pa[k][j] for k in range(5)) for j in range(5)] for i in range(5)]
                Jab = J(a, b)
                ok &= all(abs(cm[i][j] + Jab[i][j]) < 1e-12 for i in range(5) for j in range(5))
        return ok, "[P_a, P_b] = -J_ab (l = 1)"

    def breaking():
        st = D.unbroken_generators([0, 0, 0, 0, 1])
        return len(st) == 6 and all(B < 4 for _, B in st), f"{len(st)} unbroken"

    def split():
        r = D.curvature_split_residual(0.3, 7.0, x)
        r2 = D.curvature_split_residual(0.1, 11.0, [0.0, 3.1, 0.7, 1.2])
        return r < 1e-6 and r2 < 1e-6, f"residuals {r:.1e}, {r2:.1e}"

    def vacuum():
        return D.ds_curvature_max(7.0, x) < 1e-6, "de Sitter is flat as an SO(4,1) connection"

    def coefficients():
        cR, cV = D.action_coefficients(0.3, 7.0, x)
        cR2, cV2 = D.action_coefficients(0.1, 4.0, [0.0, 1.7, 0.5, 2.0])
        return abs(cR - cR2) < 1e-5 and abs(cV - cV2) < 1e-8 and abs(cV - round(cV)) < 1e-8, \
            f"geometry-independent: ({cR:.6f}, {cV:.6f}) and ({cR2:.6f}, {cV2:.6f})"

    def scal():
        a, b = D.ell_from_lambda(1e-52), D.ell_from_lambda(4e-52)
        c, d = D.mm_coupling(1e-52, 1e-35), D.mm_coupling(2e-52, 1e-35)
        return _rel(a / b, 2) < 1e-12 and _rel(c / d, 2) < 1e-12, "l ~ Lambda^-1/2, coupling ~ 1/Lambda"

    def torsion():
        f = lambda r: 1 - 0.6 / r - r * r / 49
        fp = lambda r: 0.6 / r**2 - 2 * r / 49
        E, w = D.spin_connection(x, f, fp)
        h, worst = 1e-6, 0.0
        for a in range(4):
            for mu in range(4):
                for nu in range(mu + 1, 4):
                    def de(p, q):
                        xp, xm = list(x), list(x)
                        xp[p] += h
                        xm[p] -= h
                        return (D.spin_connection(xp, f, fp)[0][a][q] - D.spin_connection(xm, f, fp)[0][a][q]) / (2 * h)
                    we = sum(w[a][b][mu] * E[b][nu] - w[a][b][nu] * E[b][mu] for b in range(4))
                    worst = max(worst, abs(de(mu, nu) - de(nu, mu) + we))
        eta = (-1, 1, 1, 1)
        anti = max(abs(w[a][b][mu] * eta[a] + w[b][a][mu] * eta[b]) for a in range(4) for b in range(4) for mu in range(4))
        return worst < 1e-7 and anti < 1e-12, f"torsion {worst:.1e}; omega_ab antisymmetric {anti:.1e}"

    def ricci_two_routes():
        # property, not value: ricci_scalar must equal the contraction of R = d omega + omega ^ omega,
        # built here by finite differences of the build's own spin_connection; and R ~ 1/length^2
        eta = (-1, 1, 1, 1)
        worst = 0.0
        for M, l, p in ((0.3, 7.0, x), (0.1, 11.0, [0.0, 3.1, 0.7, 1.2])):
            f = lambda r, M=M, l=l: 1 - 2 * M / r - r * r / l**2
            fp = lambda r, M=M, l=l: 2 * M / r**2 - 2 * r / l**2
            E, w = D.spin_connection(p, f, fp)
            h = 1e-5
            dw = []
            for mu in range(4):
                pp, pm = list(p), list(p)
                pp[mu] += h
                pm[mu] -= h
                wp, wm = D.spin_connection(pp, f, fp)[1], D.spin_connection(pm, f, fp)[1]
                dw.append([[[(wp[a][b][nu] - wm[a][b][nu]) / (2 * h) for nu in range(4)] for b in range(4)] for a in range(4)])
            inv = [[0.0] * 4 for _ in range(4)]                  # E_a^mu: the inverse of the (diagonal) tetrad
            for a in range(4):
                inv[a][a] = 1 / E[a][a]
            R = 0.0
            for a in range(4):
                for b in range(4):
                    for mu in range(4):
                        for nu in range(4):
                            Rab = dw[mu][a][b][nu] - dw[nu][a][b][mu] + sum(
                                w[a][c][mu] * w[c][b][nu] - w[a][c][nu] * w[c][b][mu] for c in range(4))
                            R += Rab * inv[a][mu] * inv[b][nu] * eta[b]
            worst = max(worst, abs(D.ricci_scalar(M, l, p) - R) / max(abs(R), 1e-300))
        s1, s2 = D.ricci_scalar(0.3, 7.0, x), D.ricci_scalar(0.6, 14.0, [2 * y if i == 1 else y for i, y in enumerate(x)])
        return worst < 1e-6 and _rel(s1 / s2, 4) < 1e-6, f"ricci_scalar vs d omega + omega^omega: {worst:.1e}; scaling {s1 / s2:.6f}"

    return run_safely([("ricci_scalar is the contraction of d omega + omega ^ omega; R ~ 1/length^2", ricci_two_routes),
                       ("spin connection is torsion-free and metric (omega_ab = -omega_ba)", torsion),
                       ("so(4,1) translations close on Lorentz", algebra),
                       ("de Sitter vector leaves 6 Lorentz generators", breaking),
                       ("F = R - e^e/l^2 and torsion-free on SdS", split),
                       ("de Sitter vacuum F = 0", vacuum),
                       ("action coefficients are geometry independent", coefficients),
                       ("l and coupling scaling with Lambda", scal)])


# ------------------------------------------------------------------------------------------
def blackholes(m):
    B = m["blackholes"]

    def horizons():
        rb, rc = B.sds_horizons(1.0, 9.0)
        f = lambda r: 1 - 2 / r - r * r / 81
        none = B.sds_horizons(1.0, 5.0)
        return abs(f(rb)) < 1e-12 and abs(f(rc)) < 1e-12 and 2 < rb < rc and none is None, f"{rb}, {rc}; beyond Nariai {none}"

    def kappa_scaling():
        # properties only: kappa is positive, scales as 1/M for Schwarzschild, and does not
        # depend on where the near-horizon sample is taken
        k = lambda M, d: B.killing_kappa(lambda r: 1 - 2 * M / r, 2 * M * (1 + d), 1e-8 * M)
        k1, k2, k1b = k(1.0, 1e-6), k(3.0, 1e-6), k(1.0, 1e-5)
        return k1 > 0 and _rel(k1 / k2, 3) < 1e-5 and _rel(k1, k1b) < 1e-4, f"kappa(M=1) {k1:.6f}, ratio to M=3 {k1 / k2:.6f}"

    def euclid():
        # the Euclidean section is smooth at the period 2 pi/kappa, kappa being the build's own
        # Killing kappa, and conical at any other period
        l = 9.0
        f = lambda r: 1 - 2 / r - r * r / l**2
        rb, _ = B.sds_horizons(1.0, l)
        kb = B.killing_kappa(f, rb * (1 + 1e-6), 1e-8 * rb)
        good = B.euclidean_cone_ratio(f, rb, 2 * pi / kb, 1e-7 * rb)
        bad = B.euclidean_cone_ratio(f, rb, 1.3 * 2 * pi / kb, 1e-7 * rb)
        return abs(good - 1) < 1e-5 and abs(bad - 1) > 0.1, f"smooth {good:.7f}; wrong period {bad:.4f}"

    def first_law():
        rng = random.Random(6)
        ok = True
        for k in range(30):
            p = F(rng.randint(1, 400), rng.randint(1, 40))
            q = F(0) if k < 5 else p * F(rng.randint(0, 99), 100)
            for dp, dq in ((1, 0), (0, 1), (2, -3)):
                a, s = B.kerr_first_law(p, q, dp, dq)
                ok &= a == 0 and s == 0
        return ok, "dM = T dS + Omega dJ and Smarr, exact"

    def first_law_detects():
        # a wrong direction must not be silently accepted: the residual is a function of (dp, dq)
        a, _ = B.kerr_first_law(F(5), F(2), 1, 0)
        return isinstance(a, F), "returns an exact Fraction"

    def orbits():
        r, b = B.photon_sphere()
        ri, L2, E2 = B.isco()
        f = lambda x: 1 - 2 / x
        ok = _rel(b, 1 / sqrt(f(r) / r**2)) < 1e-10                 # b is the potential at its peak
        ok &= ri > r and L2 > 0 and 0 < E2 < 1
        return ok, f"photon sphere {r:.6f}, b {b:.6f}; ISCO {ri:.4f}"

    def scalings():
        ok = _rel(B.shadow_uas(2e6, 8000.0) / B.shadow_uas(1e6, 8000.0), 2) < 1e-12
        ok &= _rel(B.shadow_uas(1e6, 4000.0) / B.shadow_uas(1e6, 8000.0), 2) < 1e-12
        ok &= _rel(B.kerr_area_km2(20.0, 0.0) / B.kerr_area_km2(10.0, 0.0), 4) < 1e-12
        ok &= _rel(B.kerr_area_km2(10.0, 1.0) / B.kerr_area_km2(10.0, 0.0), 0.5) < 1e-12
        ok &= _rel(B.hawking_K(2.0) / B.hawking_K(1.0), 0.5) < 1e-12
        ok &= _rel(B.nariai_mass_kg(4e-52) / B.nariai_mass_kg(1e-52), 0.5) < 1e-12
        return ok, "shadow ~ M/D, area ~ M^2, extremal = half, T ~ 1/M, Nariai ~ Lambda^-1/2"

    def qnm_roundtrip():
        f, g = B.qnm_220(70.0, 0.7)
        mm, chi = B.invert_220(f, g, 0.1)
        return _rel(mm * 1.1, 70.0) < 1e-9 and abs(chi - 0.7) < 1e-9, f"round trip M {mm * 1.1}, chi {chi}"

    def kappa_rung5():
        f = lambda r: 1 - 2 / r - r * r / 81
        rb, rc = B.sds_horizons(1.0, 9.0)
        kb, kc = B.kappa_from_spin_connection(1.0, 9.0)
        Kb = B.killing_kappa(f, rb * (1 + 1e-6), 1e-8 * rb)
        Kc = B.killing_kappa(f, rc * (1 - 1e-6), 1e-8 * rc)
        return _rel(kb, Kb) < 1e-5 and _rel(kc, Kc) < 1e-5, f"spin connection {kb:.6f}, {kc:.6f}; Killing {Kb:.6f}, {Kc:.6f}"

    def nariai_vs_ell():
        # property, not formula: at the returned mass the two horizons must merge (f = f' = 0
        # at one radius) for the de Sitter radius rung 5 gives
        D = m["desitter"]
        import inputs
        Lam = 2e-52
        M = B.nariai_mass_kg(Lam) * inputs.G_NEWTON / inputs.C_LIGHT**2       # geometric units (m)
        l = D.ell_from_lambda(Lam)
        f = lambda r: 1 - 2 * M / r - r * r / l**2
        fp = lambda r: 2 * M / r**2 - 2 * r / l**2
        r0 = m["toolkit"].bisect(fp, M, l)                                     # where f' = 0
        return abs(f(r0)) < 1e-9 and B.sds_horizons(M, l * (1 + 1e-6)) is not None and \
            B.sds_horizons(M, l * (1 - 1e-6)) is None, f"f at f' = 0: {f(r0):.1e}; horizons exist just below the bound only"

    return run_safely([("kappa from rung 5's spin connection equals the Killing kappa", kappa_rung5),
                       ("largest black hole from rung 5's de Sitter radius", nariai_vs_ell),
                       ("SdS horizons and the Nariai bound", horizons),
                       ("Killing kappa > 0, ~ 1/M, independent of the sample point", kappa_scaling),
                       ("Euclidean section smooth at period 2 pi/kappa (own kappa) only", euclid),
                       ("Kerr first law and Smarr, exact", first_law),
                       ("first-law residual is exact", first_law_detects),
                       ("photon sphere and ISCO consistency", orbits),
                       ("black-hole scaling laws", scalings),
                       ("QNM forward and inverse agree", qnm_roundtrip)])


# ------------------------------------------------------------------------------------------
def links(m):
    Lk, G = m["links"], m["gauge331"]

    def anomaly():
        rng = random.Random(331)
        ok = True
        for _ in range(100):
            Nc = rng.choice((3, 5, 7, 9, 11))
            b, XL, Xt = (F(rng.randint(-60, 60), rng.randint(1, 30)) for _ in range(3))
            ok &= Lk.qp_qe_minus_anomaly(Nc, b, XL, Xt) == 0
        return ok, "q_p + q_e = anomaly/N_g for 100 random rational models"

    def neutral_size_free():
        a, b = Lk.neutrality_per_nucleon(1e-14), Lk.neutrality_per_nucleon(1e-12)
        return _rel(a, b) < 1e-12 and a > 0, "independent of diamond mass"

    def pi0():
        ok = True
        for Nc in (1, 3, 5, 7):
            Qu, Qd = G.quark_charges(Nc)
            ok &= Nc * (Qu * Qu - Qd * Qd) == 1
        w1 = Lk.pi0_width_eV(0.0073, 0.092, 0.135, 3, F(2, 3), F(-1, 3))
        w2 = Lk.pi0_width_eV(2 * 0.0073, 0.092, 0.135, 3, F(2, 3), F(-1, 3))
        w3 = Lk.pi0_width_eV(0.0073, 0.092, 0.135, 5, F(2, 3), F(-1, 3))
        return ok and _rel(w2 / w1, 4) < 1e-12 and _rel(w3 / w1, (5 / 3) ** 2) < 1e-12, "N_c(Q_u^2 - Q_d^2) = 1; ~ alpha^2 N_c^2"

    def mpl():
        # property, not formula: at the window's edges M_Pl(x G) equals the poles
        a, b = Lk.planck_mass_GeV(6.6e-11, 1e-34, 3e8), Lk.planck_mass_GeV(4 * 6.6e-11, 1e-34, 3e8)
        lo, hi = Lk.g_window(4e19, 5e11, a)
        e1 = Lk.planck_mass_GeV(lo * 6.6e-11, 1e-34, 3e8) / 4e19
        e2 = Lk.planck_mass_GeV(hi * 6.6e-11, 1e-34, 3e8) / 5e11
        return _rel(a / b, 2) < 1e-12 and lo < hi and abs(e1 - 1) < 1e-12 and abs(e2 - 1) < 1e-12, \
            "M_Pl ~ G^-1/2; M_Pl(x G) hits each pole at the window's edges"

    def rs():
        return _rel(Lk.schwarzschild_radius(2.0) / Lk.schwarzschild_radius(1.0), 2) < 1e-12, "linear in m"

    def matter():
        ok = all(tuple(Lk.matter_charges(Nc, v)) == (1, 0, -1, 0) for Nc in (3, 5, 7) for v in ("-1/sqrt3", "+1/sqrt3"))
        return ok, "q_p = 1, q_n = 0, q_e = -1, Q_nu = 0 from rung 1, both variants, N_c = 3, 5, 7"

    def pi0_rungs():
        import inputs
        Qu, Qd = G.quark_charges(3)
        a = Lk.pi0_width_from_rungs()
        b = Lk.pi0_width_eV(inputs.ALPHA_0, inputs.F_PI, inputs.M_PI0, 3, Qu, Qd)
        return _rel(a, b) < 1e-12, f"{a:.4f} eV"

    def planck_bh():
        # property, not formula: it must be rung 6's temperature at link 3's mass, and scale as 1/M
        import inputs
        kT = Lk.planck_bh_kT_GeV()
        mpl_kg = Lk.planck_mass_GeV(inputs.G_NEWTON, inputs.HBAR, inputs.C_LIGHT) * 1e9 * inputs.E_CH / inputs.C_LIGHT**2
        want = inputs.K_B * m["blackholes"].hawking_K(mpl_kg) / inputs.E_CH / 1e9
        return _rel(kT, want) < 1e-12 and kT > 0, f"k_B T_H(M_Pl) = {kT:.4e} GeV"

    return run_safely([("rung 1's charges make matter neutral", matter),
                       ("pi0 width from rung 1's charges", pi0_rungs),
                       ("Planck-mass black hole: rung 6's temperature at link 3's mass", planck_bh),
                       ("neutral matter is an anomaly identity", anomaly),
                       ("neutrality requirement independent of size", neutral_size_free),
                       ("pi0: anomaly factor 1 for all N_c, width scaling", pi0),
                       ("Planck mass scaling and G window", mpl),
                       ("Schwarzschild radius linear in mass", rs)])


BY_STAGE = {"toolkit": toolkit, "gauge331": gauge331, "chiral": chiral, "casimir": casimir,
            "graviton": graviton, "desitter": desitter, "blackholes": blackholes, "links": links}
