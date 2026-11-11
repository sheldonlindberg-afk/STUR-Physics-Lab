#!/usr/bin/env python3
"""
Unifying-equation search, front 7g: does the 3-3-1 scalar sector itself survive to the Planck scale?

The selection of N_c = 3 asks that the theory stay perturbative up to M_Pl, and so far
only the gauge couplings were followed. If the scalar quartics or the Yukawas of
3-3-1 at N_c = 3 blew up, or the potential became unbounded below, before M_Pl, the
model would fail its own test. This computes it.

Content (N_c = 3, third generation in the quark triplet, other two in anti-triplets):
  scalars   three complex SU(3)_L triplets = 18 real fields, with their X charges;
  potential the 9 quartics allowed with a discrete symmetry separating the two triplets
            of equal X (needed in both variants):
              sum_i l_i (Phi_i+ Phi_i)^2 + sum_{i<j} l_ij (Phi_i+ Phi_i)(Phi_j+ Phi_j)
              + sum_{i<j} l'_ij |Phi_i+ Phi_j|^2;
  Yukawas   the top (triplet quark Q3 with t^c) and every exotic quark (Q3 with T^c or J^c;
            the anti-triplets with D^c or J'^c) and, for beta = +1/sqrt3, the heavy leptons,
            all exotics sharing one y_J.
One-loop quartic and Yukawa RGEs from src/rge_engine.py (checked against the SM), two-loop
gauge running from front 7b/7d. The beta functions are extracted as exact polynomials.

S1  CHECKS: the 9-term basis is closed under the RGEs (residual), the quartic tensor is
    gauge invariant, the polynomial fit is exact.
S2  The SM alone: lambda_SM(mu) from m_t to M_Pl (one loop). It turns negative well below
    M_Pl: the SM is metastable, which is known, and the 3-3-1 sector inherits the question.
S3  Random search over the 3-3-1 quartics at M_V = 4 TeV, with tan(beta) and y_J free and
    the light-Higgs quartic matched to the SM value (tree-level decoupling):
      lambda_SM = l_a c^4 + l_b s^2... (formula in light_higgs_quartic)
    Fractions that stay perturbative (|l| < 4 pi, y < sqrt(4 pi)) and bounded below up to M_Pl.
"""
import os
import sys
from math import log, pi, sqrt

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import minimize

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rge_engine as R
import m331_exact as E
import m331_yukawa as Y
import m331_threshold as T

M_PLANCK = E.M_PLANCK
MV = 4e3
NC = 3
CF = (NC**2 - 1) / (2 * NC)

# variant data: scalar X charges; roles; fermion X charges
VARIANTS = {
    "-1/sqrt3": dict(X=[-1 / 3, 2 / 3, -1 / 3], top=0, other=1, chi=2,
                     XQ3=1 / 3, Xtc=-2 / 3, XQ3ex=-2 / 3, XQa=0.0, XQaex=1 / 3, leptons=False),
    "+1/sqrt3": dict(X=[1 / 3, 1 / 3, -2 / 3], top=2, other=0, chi=1,
                     XQ3=0.0, Xtc=-2 / 3, XQ3ex=1 / 3, XQa=1 / 3, XQaex=-2 / 3, leptons=True),
}
PAIRS = [(0, 1), (0, 2), (1, 2)]
NAMES = ["l1", "l2", "l3", "l12", "l13", "l23", "l'12", "l'13", "l'23"]


def banner(s):
    print("\n" + "=" * 78 + "\n" + s + "\n" + "=" * 78)


class Model:
    def __init__(self, variant):
        self.v = variant
        d = VARIANTS[variant]
        self.d = d
        self.sc = R.Scalars([3, 3, 3])
        n = self.sc.n
        gm = R.gell_mann()
        self.ThL = [sum(self.sc.embed(m, gm[A]) for m in range(3)) for A in range(8)]
        self.ThX = sum(self.sc.embed(m, d["X"][m] * np.eye(3)) for m in range(3))
        # quartic basis
        N = [self.sc.bilinear(i, i, "re") for i in range(3)]
        basis = [R.quartic_tensor(N[i], N[i]) for i in range(3)]
        basis += [R.quartic_tensor(N[i], N[j]) for i, j in PAIRS]
        for i, j in PAIRS:
            Re_, Im_ = self.sc.bilinear(i, j, "re"), self.sc.bilinear(i, j, "im")
            basis.append(R.quartic_tensor(Re_, Re_) + R.quartic_tensor(Im_, Im_))
        self.basis = basis
        self.Nmat, self.pairs_RI = N, [(self.sc.bilinear(i, j, "re"), self.sc.bilinear(i, j, "im"))
                                       for i, j in PAIRS]
        self.build_fermions()

    def build_fermions(self):
        d, sc = self.d, self.sc
        f = []                                   # (label, C2 pieces: (colour, triplet, X))
        def add(label, n, col, trip, X):
            start = len(f)
            for _ in range(n):
                f.append((label, col, trip, X))
            return start
        q3 = add("Q3", 3 * NC, True, True, d["XQ3"])
        tc = add("tc", NC, True, False, d["Xtc"])
        q3e = add("Q3ex", NC, True, False, d["XQ3ex"])
        qa = [add("Qa", 3 * NC, True, True, d["XQa"]) for _ in range(2)]
        qae = [add("Qaex", NC, True, False, d["XQaex"]) for _ in range(2)]
        lep, lepe = [], []
        if d["leptons"]:
            lep = [add("L", 3, False, True, -2 / 3) for _ in range(3)]
            lepe = [add("Ec", 1, False, False, 1.0) for _ in range(3)]
        self.f = f
        nf = len(f)
        self.Ytop = np.zeros((sc.n, nf, nf), complex)
        self.Yex3 = np.zeros((sc.n, nf, nf), complex)
        self.Yexa = np.zeros((sc.n, nf, nf), complex)
        self.Yexl = np.zeros((sc.n, nf, nf), complex)

        def couple(Yt, phi, conj, trip_start, sing_start, ncol):
            for k in range(3):
                x, y = sc.idx(phi, k)
                for al in range(ncol):
                    i, j = trip_start + k * ncol + al, sing_start + al
                    for a, w in ((x, 1 / sqrt(2)), (y, (-1j if conj else 1j) / sqrt(2))):
                        Yt[a, i, j] += w
                        Yt[a, j, i] += w
        couple(self.Ytop, d["top"], True, q3, tc, NC)
        couple(self.Yex3, d["chi"], True, q3, q3e, NC)
        for s0, e0 in zip(qa, qae):
            couple(self.Yexa, d["chi"], False, s0, e0, NC)
        for s0, e0 in zip(lep, lepe):
            couple(self.Yexl, d["chi"], True, s0, e0, 1)
        self.Ys = [self.Ytop, self.Yex3, self.Yexa] + ([self.Yexl] if d["leptons"] else [])
        self.ynames = ["y_t", "y_J3", "y_Ja", "y_E"][:len(self.Ys)]
        self.K = len(self.Ys)

    def C2F(self, gX, gL, g3):
        c = [(CF * g3**2 if col else 0) + (4 / 3 * gL**2 if trip else 0) + gX**2 * X**2
             for _, col, trip, X in self.f]
        return np.diag(c)

    def theta(self, gX, gL):
        return [gL * t for t in self.ThL] + [gX * self.ThX]

    def lam_tensor(self, l):
        return sum(c * b for c, b in zip(l, self.basis))

    def yuk(self, ys):
        return sum(y * Yk for y, Yk in zip(ys, self.Ys))

    def beta_lam_exact(self, l, gX, gL, ys):
        b = R.beta_quartic(self.lam_tensor(l), self.theta(gX, gL), self.yuk(ys))
        return R.project(b, self.basis)

    def beta_y_exact(self, gX, gL, g3, ys):
        b = R.beta_yukawa(self.yuk(ys), self.C2F(gX, gL, g3), self.sc.n)
        return R.project(b, self.Ys)

    def mono_l(self, l, u):
        nu = len(u)
        return np.concatenate([[l[i] * l[j] for i in range(9) for j in range(i, 9)],
                               [l[i] * u[k] for i in range(9) for k in range(nu)],
                               [u[k] * u[m] for k in range(nu) for m in range(k, nu)]])

    def cached_fit(self):
        """Load the fitted coefficients if cached (results/m331/), else fit and save."""
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "m331",
                            f"331_scalar_coeffs_{'minus' if self.v[0] == '-' else 'plus'}.npz")
        if os.path.exists(path):
            z = np.load(path)
            self.coef_l, self.cy = z["coef_l"], z["cy"]
            return tuple(z["checks"])
        checks = self.fit()
        np.savez(path, coef_l=self.coef_l, cy=self.cy, checks=np.array(checks))
        return checks

    def fit(self, seed=0):
        """Exact polynomial form of the betas, by least squares on random points."""
        rng = np.random.default_rng(seed)
        nu = 2 + self.K
        n_mono = 45 + 9 * nu + nu * (nu + 1) // 2
        rows, rhs, worst_close = [], [], 0.0
        for _ in range(int(1.4 * n_mono)):
            l = rng.uniform(-1, 1, 9)
            gX, gL = rng.uniform(0.2, 1.2, 2)
            ys = rng.uniform(0.2, 1.2, self.K)
            u = np.concatenate([[gX**2, gL**2], ys**2])
            c, res = self.beta_lam_exact(l, gX, gL, ys)
            worst_close = max(worst_close, res)
            rows.append(self.mono_l(l, u)); rhs.append(c)
        A, B = np.array(rows), np.array(rhs)
        self.coef_l = np.linalg.lstsq(A, B, rcond=None)[0]
        fit_res = np.abs(A @ self.coef_l - B).max()
        # Yukawas: beta_k / y_k linear in (y_1^2 .. y_K^2, gX^2, gL^2, g3^2)
        rows, rhs, worst_y = [], [], 0.0
        for _ in range(3 * (self.K + 3)):
            gX, gL, g3 = rng.uniform(0.2, 1.2, 3)
            ys = rng.uniform(0.2, 1.2, self.K)
            c, res = self.beta_y_exact(gX, gL, g3, ys)
            worst_y = max(worst_y, res)
            rows.append(np.concatenate([ys**2, [gX**2, gL**2, g3**2]])); rhs.append(c.real / ys)
        A, B = np.array(rows), np.array(rhs)
        self.cy = np.linalg.lstsq(A, B, rcond=None)[0]           # (K+3, K)
        yfit = np.abs(A @ self.cy - B).max()
        return worst_close, fit_res, worst_y, yfit

    def gauge_invariance(self, seed=1):
        l = np.random.default_rng(seed).uniform(-1, 1, 9)
        lam = self.lam_tensor(l)
        worst = 0.0
        for Tg in self.theta(1.0, 1.0):
            d = (np.einsum("ae,ebcd->abcd", Tg, lam) + np.einsum("be,aecd->abcd", Tg, lam)
                 + np.einsum("ce,abed->abcd", Tg, lam) + np.einsum("de,abce->abcd", Tg, lam))
            worst = max(worst, np.abs(d).max())
        return worst / np.abs(lam).max()

    # ------------------------------------------------------------ fast pieces
    def beta_l(self, l, gX, gL, ys):
        u = np.concatenate([[gX**2, gL**2], np.asarray(ys)**2])
        return self.mono_l(l, u) @ self.coef_l

    def gauge_yukawa_coeffs(self):
        """Two-loop gauge Yukawa coefficients per structure (per y^2), from front 7d's formula."""
        gs, ferm, scal, (Xt, Xa, Qu, Qd, Ng, nA) = E.MODELS[self.v](NC)
        F = Y.F
        nt = 3 * NC
        top = Y.yukawa_coeff(gs, ((None, 3, NC), Xt), ((None, 1, NC), -Qu), nt)
        if self.v == "-1/sqrt3":
            e3 = Y.yukawa_coeff(gs, ((None, 3, NC), Xt), ((None, 1, NC), -Qu), nt)
            ea = Y.yukawa_coeff(gs, ((None, 3, NC), Xa), ((None, 1, NC), -Qd), nt)
        else:
            e3 = Y.yukawa_coeff(gs, ((None, 3, NC), Xt), ((None, 1, NC), -Qd), nt)
            ea = Y.yukawa_coeff(gs, ((None, 3, NC), Xa), ((None, 1, NC), -Qu), nt)
        cols = [top, e3, [nA * x for x in ea]]
        if self.v == "+1/sqrt3":
            lep = Y.yukawa_coeff(gs, ((None, 3, 1), F(-2, 3)), ((None, 1, 1), F(1)), 3)
            cols.append([Ng * x for x in lep])
        return np.array([[float(x) for x in c] for c in cols]).T      # (3 gauge, K)

    def V(self, phi, l):
        N = [0.5 * phi @ M @ phi for M in self.Nmat]
        v = l[0] * N[0]**2 + l[1] * N[1]**2 + l[2] * N[2]**2
        for k, (i, j) in enumerate(PAIRS):
            Rr, Ii = self.pairs_RI[k]
            r, im = 0.5 * phi @ Rr @ phi, 0.5 * phi @ Ii @ phi
            v += l[3 + k] * N[i] * N[j] + l[6 + k] * (r * r + im * im)
        return v

    def bounded_below(self, l, rng, starts=5):
        f = lambda p: self.V(p / np.linalg.norm(p), l)
        best = np.inf
        for _ in range(starts):
            r = minimize(f, rng.normal(size=18), method="L-BFGS-B", options={"maxiter": 400})
            best = min(best, r.fun)
        return best > -1e-9, best


def light_higgs_quartic(l, m, c2):
    """Tree-level decoupling (v_chi >> v): the light Higgs h = c h_top + s h_other.
    Exchange terms vanish because the two doublet vevs sit in different triplet components;
    the heavy chi radial mode is integrated out."""
    d = VARIANTS[m.v]
    a, b, x = d["top"], d["other"], d["chi"]
    lij = lambda i, j: l[3 + PAIRS.index(tuple(sorted((i, j))))]
    s2 = 1 - c2
    return l[a] * c2**2 + l[b] * s2**2 + lij(a, b) * c2 * s2 - (lij(a, x) * c2 + lij(b, x) * s2) ** 2 / (4 * l[x])


def sm_running(mu_end, n=400):
    """One-loop SM from m_t (MS-bar inputs recalled: Buttazzo et al. 2013) to mu_end."""
    g1, g2, g3, yt, lam = 0.3583, 0.6477, 1.1666, 0.9369, 0.12604

    def rhs(t, s):
        g1, g2, g3, yt, lam = s
        k = 1 / (16 * pi**2)
        return [k * 41 / 6 * g1**3, -k * 19 / 6 * g2**3, -k * 7 * g3**3,
                k * yt * (4.5 * yt**2 - 8 * g3**2 - 9 / 4 * g2**2 - 17 / 12 * g1**2),
                k * (24 * lam**2 - 6 * yt**4 + 12 * lam * yt**2 - 3 * lam * (3 * g2**2 + g1**2)
                     + 3 / 8 * (2 * g2**4 + (g2**2 + g1**2) ** 2))]
    return solve_ivp(rhs, [0, log(mu_end / 172.57)], [g1, g2, g3, yt, lam], rtol=1e-9,
                     dense_output=True, max_step=0.2)


def run_331(m, l0, yt0, yJ0, g0, mu0=MV, n_check=8, rng=None, pert_first=False):
    """Run (g, y, l) from mu0 to M_Pl. Returns dict with perturbativity and stability verdicts."""
    gs, ferm, scal, _ = E.MODELS[m.v](NC)
    a, b = E.coefficients(gs, ferm, scal)
    a = np.array([float(x) for x in a]); b = np.array([[float(x) for x in r] for r in b])
    cg = m.gauge_yukawa_coeffs()
    k = 1 / (16 * pi**2)
    K = m.K

    def rhs(t, s):
        g = s[:3]; ys = s[3:3 + K]; l = s[3 + K:]
        dg = g**3 * k * (a + (b @ g**2 - cg @ ys**2) * k)
        v = np.concatenate([ys**2, g**2])
        dy = k * ys * (v @ m.cy)
        dl = k * m.beta_l(l, g[0], g[1], ys)
        return np.concatenate([dg, dy, dl])

    def blow(t, s):
        return min(4 * pi - np.abs(s[3 + K:]).max(), sqrt(4 * pi) - np.abs(s[3:3 + K]).max(),
                   4 * pi - s[:3].max())
    blow.terminal = True
    tend = log(M_PLANCK / mu0)
    ys0 = np.array([yt0] + [yJ0] * (K - 1))
    sol = solve_ivp(rhs, [0, tend], np.concatenate([g0, ys0, l0]), events=blow,
                    rtol=1e-8, atol=1e-10, dense_output=True, max_step=0.5)
    pert = sol.t[-1] >= tend - 1e-9
    stable, where = True, None
    tmax = sol.t[-1]
    if not pert and pert_first:
        n_check = 0
        stable = None
    for tt in np.linspace(0, tmax, n_check):
        l = sol.sol(tt)[3 + K:]
        ok, _ = m.bounded_below(l, rng)
        if not ok:
            stable, where = False, mu0 * np.exp(tt)
            break
    return dict(pert=pert, mu_fail=None if pert else mu0 * np.exp(sol.t[-1]), stable=stable,
                mu_unstable=where, l_end=sol.sol(tmax)[3 + K:], y_end=sol.sol(tmax)[3:3 + K])


PRIORS = {"wide": dict(li=(0.02, 2.0), lij=(-1.0, 3.0), lp=(-2.0, 2.0), yJ=(0.2, 1.5)),
          "small": dict(li=(0.01, 0.4), lij=(-0.3, 0.6), lp=(-0.4, 0.4), yJ=(0.1, 0.8)),
          "tight": dict(li=(0.005, 0.25), lij=(-0.15, 0.4), lp=(-0.3, 0.3), yJ=(0.05, 0.6))}


def yJ_max(m, yt0, g0):
    """Largest common exotic Yukawa at M_V for which gauge + Yukawas stay perturbative to M_Pl.
    Exact at one loop: the quartics do not feed back into gauge or Yukawa running."""
    from scipy.optimize import brentq
    f = lambda y: 1.0 if run_331(m, np.zeros(9), yt0, y, np.asarray(g0), n_check=0,
                                 pert_first=True)["pert"] else -1.0
    lo, hi = 0.05, 2.0
    if f(hi) > 0:
        return hi
    for _ in range(30):
        mid = 0.5 * (lo + hi)
        lo, hi = (mid, hi) if f(mid) > 0 else (lo, mid)
    return 0.5 * (lo + hi)


def sample(m, rng, lam_sm, yt_sm, g0, n=300, prior="small"):
    """Random quartics at M_V matched to lambda_SM; counts outcomes."""
    P = PRIORS[prior]
    out = dict(tried=0, viable=0, pert=0, stable=0, both=0, example=None, fail_scales=[])
    d = VARIANTS[m.v]
    a = d["top"]
    while out["viable"] < n and out["tried"] < 40 * n:
        out["tried"] += 1
        l = np.zeros(9)
        l[[0, 1, 2]] = rng.uniform(*P["li"], 3)
        l[3:6] = rng.uniform(*P["lij"], 3)
        l[6:9] = rng.uniform(*P["lp"], 3)
        c2 = rng.uniform(0.1, 0.9)
        l[a] = 0.0
        rest = light_higgs_quartic(l, m, c2)                 # with l_top = 0
        l[a] = (lam_sm - rest) / c2**2
        if not (0 < l[a] < P["li"][1]):
            continue
        if not m.bounded_below(l, rng, starts=3)[0]:
            continue
        yt = yt_sm / sqrt(c2)
        yJ = rng.uniform(*P["yJ"])
        if yt > 1.5:
            continue
        out["viable"] += 1
        r = run_331(m, l, yt, yJ, g0, rng=rng, pert_first=True)
        out["pert"] += r["pert"]
        out["stable"] += bool(r["stable"])
        if r["pert"] and r["stable"]:
            out["both"] += 1
            out.setdefault("survivors", []).append((l.copy(), c2, yt, yJ, r["l_end"]))
            if out["example"] is None:
                out["example"] = (l.copy(), c2, yt, yJ, r["l_end"])
        elif not r["pert"]:
            out["fail_scales"].append(r["mu_fail"])
        if r["stable"] is False:
            out.setdefault("unstable_scales", []).append(r["mu_unstable"])
    return out


def main(n_samples=250, seed=11):
    res = {}
    banner("S1  CHECKS")
    models = {}
    for v in VARIANTS:
        m = Model(v)
        close, fitres, closey, yfit = m.cached_fit()
        gi = m.gauge_invariance()
        models[v] = m
        res[(v, "checks")] = (close, fitres, closey, yfit, gi)
        print(f"   beta = {v:8s}: basis closure residual {close:.1e}; Yukawa-structure closure {closey:.1e};")
        print(f"                    polynomial fit max error {fitres:.1e} (Yukawa {yfit:.1e}); gauge invariance {gi:.1e}")
        lab = m.ynames + ["gX", "gL", "g3"]
        for kk, nm in enumerate(m.ynames):
            print(f"                    16pi^2 beta({nm})/{nm} = " + " ".join(
                f"{m.cy[i, kk]:+.3f} {lab[i]}^2" for i in range(len(lab)) if abs(m.cy[i, kk]) > 1e-9))
    sm = R.check_sm()
    print(f"   engine vs SM (exact formulas): beta_lambda {sm[0]:.6f} vs {sm[1]:.6f}; beta_yt {sm[3].real:.6f} vs {sm[4]:.6f}")

    banner("S2  The Standard Model alone")
    sol = sm_running(M_PLANCK)
    ts = np.linspace(0, sol.t[-1], 4000)
    lam = sol.sol(ts)[4]
    i0 = np.argmax(lam < 0)
    mu0 = 172.57 * np.exp(ts[i0]) if lam.min() < 0 else None
    res["sm_cross"] = mu0
    print(f"   lambda(m_t) = 0.1260 -> lambda(4 TeV) = {sol.sol(log(MV/172.57))[4]:.4f}; one-loop lambda turns negative at"
          f" {mu0:.1e} GeV;  lambda(M_Pl) = {lam[-1]:+.3f}")
    print("   (LIT recalled: at NNLO the crossing is ~1e10-1e11 GeV and the SM is metastable, not unstable.)")
    lam_sm = float(sol.sol(log(MV / 172.57))[4])
    yt_sm = float(sol.sol(log(MV / 172.57))[3])

    banner("S3  Gauge + Yukawas alone: the largest exotic Yukawa (exact at one loop)")
    gauge0 = {}
    for v, m in models.items():
        ainv, _, _ = Y.boundary(MV, lam=tuple(T.lambdas(T.heavy_spectrum(NC, v, MV), MV)))
        gauge0[v] = np.sqrt(4 * pi / ainv)
        gL = gauge0[v][1]
        for c2 in (0.9, 0.5):
            ym = yJ_max(m, yt_sm / sqrt(c2), gauge0[v])
            res[(v, "yJmax", c2)] = ym
            print(f"   beta = {v:8s}, top-doublet vev fraction c^2 = {c2}: y_J(4 TeV) < {ym:.3f}"
                  f"  ->  m_exotic < {sqrt(2)*ym/gL:.2f} M_V")

    banner("S4  The full scalar sector from 4 TeV to the Planck scale (N_c = 3)")
    print(f"   matched at M_V = 4 TeV: lambda_SM = {lam_sm:.4f}, y_t(SM) = {yt_sm:.4f}; tan(beta) free (c^2 in [0.1, 0.9]);")
    print("   the top-doublet quartic is solved from lambda_SM; the vacuum must be bounded below at 4 TeV.")
    print("   Survive = every quartic |l| < 4 pi, every Yukawa < sqrt(4 pi) and the potential bounded below,")
    print("   checked at 8 scales up to M_Pl.")
    for prior in ("wide", "small", "tight"):
        P = PRIORS[prior]
        print(f"   prior '{prior}': l_i in {P['li']}, l_ij in {P['lij']}, l'_ij in {P['lp']}, y_J in {P['yJ']}")
    rng = np.random.default_rng(seed)
    for v, m in models.items():
        for prior, n in (("wide", 60), ("small", n_samples), ("tight", n_samples)):
            o = sample(m, rng, lam_sm, yt_sm, gauge0[v], n=n, prior=prior)
            res[(v, prior)] = o
            fs = np.array(o["fail_scales"]) if o["fail_scales"] else None
            print(f"   beta = {v:8s} {prior:5s}: {o['viable']:3d} viable; perturbative {o['pert']:3d}; "
                  f"perturbative and stable {o['both']:3d} ({100*o['both']/max(o['viable'],1):.0f}%)"
                  + (f"; failures at {np.median(fs):.0e} GeV (median)" if fs is not None else ""))
        surv = res[(v, "tight")].get("survivors", []) + res[(v, "small")].get("survivors", [])
        if surv:
            yJs = np.array([x[3] for x in surv]); c2s = np.array([x[1] for x in surv])
            lmax = max(np.abs(x[0]).max() for x in surv)
            ltop = np.array([x[4][VARIANTS[v]["top"]] for x in surv])
            res[(v, "surv")] = (len(surv), yJs.max(), c2s.min(), c2s.max(), lmax, ltop.min())
            print(f"        survivors: y_J(4 TeV) up to {yJs.max():.2f}; c^2 from {c2s.min():.2f} to {c2s.max():.2f};"
                  f" largest |l(4 TeV)| {lmax:.2f}; top-doublet quartic at M_Pl >= {ltop.min():+.3f}")
            l, c2, yt, yJ, le = surv[0]
            print(f"        example: c^2 = {c2:.2f}, y_t = {yt:.3f}, y_J = {yJ:.3f}")
            print("          at 4 TeV : " + " ".join(f"{n_}={x:+.3f}" for n_, x in zip(NAMES, l)))
            print("          at M_Pl  : " + " ".join(f"{n_}={x:+.3f}" for n_, x in zip(NAMES, le)))
            res[(v, "example")] = surv[0]
    return res


if __name__ == "__main__":
    main()
