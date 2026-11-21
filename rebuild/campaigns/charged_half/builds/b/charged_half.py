"""Emission of a charged massless spin-1/2 particle from a Schwarzschild hole with fluctuating charge.
See DERIVATION.md.  Units G=c=hbar=k_B=M=1, T=1/(8 pi)."""
import math
import functools
import numpy as np
from scipy.integrate import solve_ivp

PROVENANCE = {
    "transmission": ("derived", "Dirac radial system (SPEC S1) integrated from the horizon in y=ln(r-2); exact 1/r series for the log-Coulomb asymptotics; Gamma=1/|A_in|^2"),
    "rates": ("derived", "Gauss-Legendre thermal integral of Gamma_j(w;g_gb) n_F(w;g_mu); ln Gamma Chebyshev-interpolated in g"),
    "charge_distribution": ("derived", "birth-death chain detailed balance pi(n+1)/pi(n)=up(n)/down(n+1), SPEC S3"),
    "weight_ratio": ("derived", "<P>/P(0,0) with the stationary distribution"),
    "energy_ratio": ("derived", "(<P>/<N>)/(P0/N0)"),
}

TEMP = 1.0 / (8.0 * math.pi)
CFG = dict(rtol=1e-12, y0=-32.0, rfac=30.0, rk=4.0, w_lo=1e-3, w_hi=1.7, nodes=8, jmax=9.5, gm=0.25, ng=15,
           edges=(1e-3, 0.0025, 0.005, 0.01, 0.02, 0.04, 0.08, 0.16, 0.3, 0.5, 0.8, 1.2, 1.7))


# ---------------------------------------------------------------- asymptotic series
def _series(om, g, kap, x):
    """P, Q=s*q of the incoming asymptotic solution e^{-i phi}(P,Q), arrays om,g; scalar kap, x. Returns P,Q,smallest term.
    The series is asymptotic. All terms are generated until every element has passed its smallest term (or reached 1e-19),
    then each is summed up to its own optimal truncation, defined on the envelope max(t_m, t_{m-1}) so that accidental
    early dips of individual terms (e.g. g ~ 0 where low orders nearly vanish) never truncate it prematurely."""
    om = np.asarray(om, dtype=complex)
    g = np.asarray(g, dtype=complex)
    p1 = np.ones_like(om)
    c1 = np.zeros_like(om)
    c2 = np.zeros_like(om)
    xm = 1.0
    pt, ct, tt = [], [], []
    for m in range(1, 600):
        cm = (kap * p1 + (m - 1) * c1 - (2 * m - 3) * c2 - 2j * g * c1) / (-2j * om)
        pm = -kap * cm / m
        xm *= x
        t = np.maximum(abs(pm), abs(cm)) * xm
        pt.append(pm * xm)
        ct.append(cm * xm)
        tt.append(t)
        p1, c2, c1 = pm, c1, cm
        if m >= 12:
            T = np.array(tt)
            env = np.maximum(T[1:], T[:-1])                  # env[k] = max(t_{k+2}, t_{k+1})  (1-based orders)
            emin = env.min(axis=0)
            if np.all((env[-1] > 1e6 * np.maximum(emin, 1e-300)) | (emin < 1e-19)) and m >= 20:
                break
    T = np.array(tt)
    env = np.maximum(T[1:], T[:-1])
    conv = env < 1e-19
    kstar = np.where(conv.any(axis=0), conv.argmax(axis=0), env.argmin(axis=0))      # index into env
    last = kstar + 2                                          # include orders 1..last (1-based)
    idx = np.arange(1, len(tt) + 1)[:, None]
    use = idx <= last[None, :]
    P = 1.0 + np.sum(np.where(use, np.array(pt), 0), axis=0)
    q = np.sum(np.where(use, np.array(ct), 0), axis=0)
    return P, np.sqrt(1 - 2 * x) * q, env.min(axis=0)


# ---------------------------------------------------------------- batched Gamma
def _gamma_batch(j, w, g, R=None, rtol=None, y0=None, full=False):
    """Gamma_j(w_i; g_i) for arrays w, g (one batch, common matching radius)."""
    w = np.atleast_1d(np.asarray(w, dtype=float))
    g = np.atleast_1d(np.asarray(g, dtype=float)) * np.ones_like(w)
    rtol = CFG["rtol"] if rtol is None else rtol
    y0 = CFG["y0"] if y0 is None else y0
    kap = j + 0.5
    if R is None:
        R = max(60.0, (CFG["rfac"] + CFG["rk"] * kap * kap) / w.min())
    B = w.size
    r0 = 2.0 + math.exp(y0)
    rs0 = r0 + 2.0 * (y0 - math.log(2.0))
    wh = w - g / 2.0
    Rp0 = np.exp(-1j * wh * rs0)
    Wh0 = kap * math.sqrt(math.exp(y0) / r0) / r0
    Rm0 = Rp0 * Wh0 / (0.25 - 2j * wh)
    u0 = np.concatenate([Rp0, Rm0])

    def rhs(y, u):
        r = 2.0 + math.exp(y)
        W = kap * math.sqrt(math.exp(y) / r) / r
        wt = w - g / r
        Rp, Rm = u[:B], u[B:]
        return np.concatenate([r * (-1j * wt * Rp + W * Rm), r * (1j * wt * Rm + W * Rp)])

    sol = solve_ivp(rhs, [y0, math.log(R - 2.0)], u0, method="DOP853", rtol=rtol, atol=1e-40)
    Rp, Rm = sol.y[:B, -1], sol.y[B:, -1]
    x = 1.0 / R
    P, Q, t1 = _series(w, g, kap, x)
    Pt, Qt, t2 = _series(-w, -g, kap, x)
    phi = w * (R + 2.0 * math.log(R / 2.0 - 1.0)) - g * math.log(R - 2.0)
    ein, eout = np.exp(-1j * phi), np.exp(1j * phi)
    a11, a12, a21, a22 = ein * P, eout * Qt, ein * Q, eout * Pt
    det = a11 * a22 - a12 * a21
    Ain = (a22 * Rp - a12 * Rm) / det
    Aout = (-a21 * Rp + a11 * Rm) / det
    gam = 1.0 / abs(Ain) ** 2
    if full:
        return dict(gamma=gam, gamma2=1 - abs(Aout) ** 2 / abs(Ain) ** 2, J=abs(Rm) ** 2 - abs(Rp) ** 2, terms=np.maximum(t1, t2), nfev=sol.nfev)
    return gam


def transmission(j, w, g):
    """Gamma_j(w; g): absorption probability of the partial wave j (SPEC S2)."""
    return float(_gamma_batch(float(j), [float(w)], [float(g)])[0])


# ---------------------------------------------------------------- grey-body grid
def _nodes():
    xg, wg = np.polynomial.legendre.leggauss(CFG["nodes"])
    ws, wts = [], []
    e = CFG["edges"]
    for a, b in zip(e[:-1], e[1:]):
        ws.append(0.5 * (b - a) * xg + 0.5 * (b + a))
        wts.append(0.5 * (b - a) * wg)
    ws.append(np.array([CFG["w_lo"]]))                      # last column: w_lo, used only for the analytic tail
    wts.append(np.array([0.0]))
    return ws, wts


def _cheb(gm, ng):
    k = np.arange(ng)
    return gm * np.cos(np.pi * (2 * k + 1) / (2 * ng))


@functools.lru_cache(maxsize=None)
def _table(gm):
    """ln Gamma_j(w_i; g_k) on panels x j x Chebyshev nodes of [-gm, gm]."""
    ws, wts = _nodes()
    gk = _cheb(gm, CFG["ng"])
    js = [0.5 + i for i in range(int(round(CFG["jmax"] - 0.5)) + 1)]
    out = np.empty((len(js), sum(len(a) for a in ws), len(gk)))
    for ji, j in enumerate(js):
        col = 0
        for wp in ws:
            W = np.repeat(wp, len(gk))
            G = np.tile(gk, len(wp))
            gam = _gamma_batch(j, W, G).reshape(len(wp), len(gk))
            out[ji, col:col + len(wp), :] = np.log(np.maximum(gam, 1e-300))
            col += len(wp)
    return np.concatenate(ws), np.concatenate(wts), np.array(js), gk, out


def _gm_for(g):
    gm = CFG["gm"]
    while abs(g) > gm:
        gm *= 2.0
    return gm


def _gamma_grid(g):
    """Gamma_j(w_i; g) for all j, w_i by barycentric Chebyshev interpolation of ln Gamma."""
    gm = _gm_for(g)
    ws, wts, js, gk, tab = _table(gm)
    ng = len(gk)
    k = np.arange(ng)
    bw = (-1.0) ** k * np.sin(np.pi * (2 * k + 1) / (2 * ng))
    d = g - gk
    hit = np.nonzero(d == 0.0)[0]
    if hit.size:
        lg = tab[:, :, hit[0]]
    else:
        c = bw / d
        lg = tab @ (c / c.sum())
    return ws, wts, js, np.exp(lg)


@functools.lru_cache(maxsize=None)
def _rates_cached(gb, gmu):
    ws, wts, js, gam = _gamma_grid(gb)
    gam_lo, ws, wts, gam = gam[:, -1], ws[:-1], wts[:-1], gam[:, :-1]
    x = (ws - gmu / 2.0) / TEMP
    nf = 0.5 * (1.0 - np.tanh(0.5 * x))                    # 1/(e^x+1), stable
    deg = (2 * js + 1)[:, None]
    N = float(np.sum(deg * gam * nf * wts) / (2 * math.pi))
    P = float(np.sum(deg * gam * nf * wts * ws) / (2 * math.pi))
    # analytic low-frequency tail below w_lo:  Gamma ~ Gamma(w_lo) (w/w_lo)^(2j+1)
    wl = CFG["w_lo"]
    nfl = 0.5 * (1.0 - math.tanh(0.5 * (0.5 * wl - gmu / 2.0) / TEMP))
    Nt = np.sum((2 * js + 1) * gam_lo * wl / (2 * js + 2)) * nfl / (2 * math.pi)
    Pt = np.sum((2 * js + 1) * gam_lo * wl * wl / (2 * js + 3)) * nfl / (2 * math.pi)
    return N + float(Nt), P + float(Pt)


def rates(g_gb, g_mu):
    """(N, P): number rate and power per helicity state with grey-body coupling g_gb, chemical potential coupling g_mu."""
    return _rates_cached(round(float(g_gb), 14), round(float(g_mu), 14))


# ---------------------------------------------------------------- charge process
def _nr(rule, q, n):
    return {"before": n, "mid": n - q / 2.0, "after": n - q}[rule]


def _up(alpha, rule, n):          # electron emission: q = -1
    return rates(alpha * (-1) * _nr(rule[0], -1, n), alpha * (-1) * _nr(rule[1], -1, n))[0]


def _down(alpha, rule, n):        # positron emission: q = +1
    return rates(alpha * _nr(rule[0], 1, n), alpha * _nr(rule[1], 1, n))[0]


@functools.lru_cache(maxsize=None)
def _dist(alpha, rule):
    lw = [0.0]                                              # ln pi(n)/pi(0), n >= 0
    n = 0
    while True:
        lw.append(lw[-1] + math.log(_up(alpha, rule, n)) - math.log(_down(alpha, rule, n + 1)))
        n += 1
        tot = sum(math.exp(v) for v in lw)
        if (lw[-1] < lw[-2] and math.exp(lw[-1]) < 1e-17 * tot) or n > 2000:
            break
    w = np.exp(np.array(lw))
    full = np.concatenate([w[:0:-1], w])                    # n = -nmax..nmax (mirror symmetry)
    full /= full.sum()
    ns = np.arange(-(len(w) - 1), len(w))
    keep = full >= 1e-14
    full = full[keep] / full[keep].sum()
    return {int(a): float(b) for a, b in zip(ns[keep], full)}


def charge_distribution(alpha, rule=("after", "after")):
    """Stationary distribution {n: pi(n)} of the charge birth-death process."""
    return dict(_dist(float(alpha), tuple(rule)))


def _averages(alpha, rule):
    pi = _dist(float(alpha), tuple(rule))
    P = N = 0.0
    for n, p in pi.items():
        ne, pe = rates(alpha * (-1) * _nr(rule[0], -1, n), alpha * (-1) * _nr(rule[1], -1, n)), \
                 rates(alpha * _nr(rule[0], 1, n), alpha * _nr(rule[1], 1, n))
        N += p * (ne[0] + pe[0]) / 2.0
        P += p * (ne[1] + pe[1]) / 2.0
    return N, P


def weight_ratio(alpha, rule=("after", "after")):
    """<P>/P(0,0)."""
    return _averages(float(alpha), tuple(rule))[1] / rates(0.0, 0.0)[1]


def energy_ratio(alpha, rule=("after", "after")):
    """(<P>/<N>) / (P(0,0)/N(0,0))."""
    N, P = _averages(float(alpha), tuple(rule))
    N0, P0 = rates(0.0, 0.0)
    return (P / N) / (P0 / N0)


def _gamma_schrodinger(j, w, rmax_wr=5e3):
    """Second route (g = 0): Chandrasekhar real equation Z'' + (w^2 - W^2 - W')Z = 0 for Z = R_+ + R_-, integrated in r*
    (r(r*) from the Lambert W function, LSODA), matched to WKB plane waves at large r. Gamma = omega/|c_-|^2."""
    from scipy.special import lambertw
    from scipy.integrate import solve_ivp as ivp
    kap = j + 0.5

    def r_of(rs):
        if rs < 40.0:
            return 2.0 + 2.0 * float(np.real(lambertw(math.exp(rs / 2.0 - 1.0))))
        r = rs
        for _ in range(60):                                 # r = r* - 2 ln(r/2 - 1)
            r = rs - 2.0 * math.log(r / 2.0 - 1.0)
        return r

    def Wf(rs):
        r = r_of(rs)
        return kap * math.sqrt(1.0 - 2.0 / r) / r, r

    def V(rs):
        W, r = Wf(rs)
        f = 1.0 - 2.0 / r
        # dW/dr* = f dW/dr, W = kap sqrt(f)/r:  dW/dr = kap (f'/(2 sqrt f) / r - sqrt f / r^2), f' = 2/r^2
        dWdr = kap * ((1.0 / r ** 2) / math.sqrt(f) / r - math.sqrt(f) / r ** 2)
        return W * W + f * dWdr

    rs0 = -60.0
    wv = w
    cW = Wf(rs0)[0] / (0.25 - 2j * wv)                      # near-horizon R_- = c W R_+  (first-order correction)
    e0 = np.exp(-1j * wv * rs0)
    Z0 = np.array([e0 * (1 + cW), e0 * (-1j * wv + cW * (0.25 - 1j * wv))])
    R = max(60.0, rmax_wr / w)
    rs1 = R + 2.0 * math.log(R / 2.0 - 1.0)
    y0 = np.array([Z0[0].real, Z0[1].real, Z0[0].imag, Z0[1].imag])       # LSODA is real-only: (Re Z, Re Z', Im Z, Im Z')
    sol = ivp(lambda t, z: [z[1], -(wv * wv - V(t)) * z[0], z[3], -(wv * wv - V(t)) * z[2]], [rs0, rs1], y0, method="LSODA", rtol=1e-11, atol=1e-30)
    Z, dZ = sol.y[0, -1] + 1j * sol.y[2, -1], sol.y[1, -1] + 1j * sol.y[3, -1]
    h = 1e-3 * R
    k2 = lambda t: wv * wv - V(t)
    k = math.sqrt(k2(rs1))
    dk = (math.sqrt(k2(rs1 + h)) - math.sqrt(k2(rs1 - h))) / (2 * h)
    # Z = (c_- e^{-iS} + c_+ e^{iS})/sqrt(k);  Z' = [(-ik - k'/2k) c_- e^{-iS} + (ik - k'/2k) c_+ e^{iS}]/sqrt(k)
    u, v = Z * math.sqrt(k), dZ * math.sqrt(k) + 0.5 * dk / k * Z * math.sqrt(k)
    cm = 0.5 * (u + 1j * v / k)           # c_- e^{-iS}
    return wv / abs(cm) ** 2


def _stationary_nullvector(alpha, rule, pi):
    """Second route for pi: null vector of the generator matrix on the support of pi."""
    from scipy.linalg import null_space
    ns = sorted(pi)
    idx = {n: i for i, n in enumerate(ns)}
    L = np.zeros((len(ns), len(ns)))
    for n in ns:
        if n + 1 in idx:
            u = _up(alpha, rule, n)
            L[idx[n + 1], idx[n]] += u
            L[idx[n], idx[n]] -= u
        if n - 1 in idx:
            d = _down(alpha, rule, n)
            L[idx[n - 1], idx[n]] += d
            L[idx[n], idx[n]] -= d
    v = null_space(L)[:, 0]
    v = v / v.sum()
    return max(abs(v[idx[n]] - pi[n]) for n in ns)


if __name__ == "__main__":
    from scipy.integrate import quad
    A = 1.0 / 137.035999084
    print("== second route (a): Gamma(g=0), Schrodinger/WKB route vs Dirac-series route")
    for j, w in ((0.5, 0.05), (0.5, 0.3), (1.5, 0.2), (2.5, 0.6), (4.5, 1.0)):
        a, b = transmission(j, w, 0.0), _gamma_schrodinger(j, w)
        print(f"  j={j} w={w}: Dirac {a:.9g}  Schrodinger {b:.9g}  rel diff {abs(a / b - 1):.1e}")
    print("== flux conservation, Gamma two ways, matching-radius / tolerance variation (g != 0)")
    for j, w, g in ((0.5, 0.05, 0.1), (1.5, 0.2, -0.1), (3.5, 0.5, 0.1)):
        d = _gamma_batch(j, [w], [g], full=True)
        d2 = _gamma_batch(j, [w], [g], full=True, R=2.0 * (30 + 4 * (j + .5) ** 2) / w, rtol=1e-12, y0=-40.0)
        print(f"  j={j} w={w} g={g}: 1/|Ain|^2={d['gamma'][0]:.10g}  1-|Aout|^2/|Ain|^2={d['gamma2'][0]:.10g}  J={d['J'][0]:.10f}"
              f"  [2R, rtol 1e-12, y0=-40: {d2['gamma'][0]:.10g}, rel {abs(d['gamma'][0] / d2['gamma'][0] - 1):.1e}]  series term {d['terms'][0]:.1e}")
    print("== second route (c): thermal integral by quad vs Gauss-Legendre grid (g=0, j=1/2,3/2,5/2)")
    ws, wts, js, gam = _gamma_grid(0.0)
    for ji in (0, 1, 2):
        j = js[ji]
        qN = quad(lambda w: (2 * j + 1) * transmission(j, w, 0.0) / (math.exp(w / TEMP) + 1) / (2 * math.pi), 1e-3, 1.7, points=[0.02, 0.1, 0.3, 0.6], limit=200, epsabs=0, epsrel=1e-10)[0]
        nf = 1 / (np.exp(ws[:-1] / TEMP) + 1)
        gN = float(np.sum((2 * j + 1) * gam[ji, :-1] * nf * wts[:-1]) / (2 * math.pi))
        print(f"  j={j}: quad {qN:.10e}  GL {gN:.10e}  rel {abs(qN / gN - 1):.1e}")
    N0, P0 = rates(0.0, 0.0)
    print(f"== neutral: N = {N0:.8e}  P = {P0:.8e}")
    print("== results at alpha = 1/137.036 (second-route pi check: max |pi_nullvector - pi_detailed_balance|)")
    for r1 in ("before", "mid", "after"):
        for r2 in ("before", "mid", "after"):
            rule = (r1, r2)
            pi = charge_distribution(A, rule)
            print(f"  rule {rule}: weight_ratio = {weight_ratio(A, rule):.10f}  energy_ratio = {energy_ratio(A, rule):.10f}"
                  f"  nmax = {max(pi)}  var(n) = {sum(p * n * n for n, p in pi.items()):.4f}  nullvec diff = {_stationary_nullvector(A, rule, pi):.1e}")
