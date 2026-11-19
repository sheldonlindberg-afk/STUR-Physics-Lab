"""Orchestrator's reference chain for the charged spin-1/2 campaign (HIDDEN). Grey-body grid from make_grid.py (reference_solver.py, an independent amplitude-variable solver
validated at g = 0 against the accepted greybody references to 2e-7); Gamma(g) by Chebyshev-node interpolation (about 1e-5 relative), the rest by quadrature."""
import math, os
import numpy as np

T = 1 / (8 * math.pi)
_D = np.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), "grid.npz"))
gn, js, w, wu, G = _D["gnodes"], _D["js"], _D["w"], _D["wu"], _D["gamma"]
deg = 2 * js + 1


def gam(g):
    out = np.zeros(G.shape[1:])
    n = len(gn)
    for k in range(n):
        lk = 1.0
        for m in range(n):
            if m != k:
                lk *= (g - gn[m]) / (gn[k] - gn[m])
        out += lk * G[k]
    return out


def rates(g_gb, g_mu):
    Gm = gam(g_gb)
    nf = 1 / (np.exp((w - g_mu / 2) / T) + 1)
    N = np.sum(deg[:, None] * Gm * nf[None, :] * wu[None, :]) / (2 * math.pi)
    P = np.sum(deg[:, None] * Gm * (w * nf)[None, :] * wu[None, :]) / (2 * math.pi)
    return float(N), float(P)


def _n_eff(rule, q, n):
    return {"before": n, "after": n - q, "mid": n - q / 2}[rule]


def chain(alpha, rule=("after", "after"), nmax=30):
    up = {n: rates(alpha * -1 * _n_eff(rule[0], -1, n), alpha * -1 * _n_eff(rule[1], -1, n)) for n in range(-nmax, nmax + 1)}
    dn = {n: rates(alpha * _n_eff(rule[0], +1, n), alpha * _n_eff(rule[1], +1, n)) for n in range(-nmax, nmax + 1)}
    lp = {0: 0.0}
    for n in range(1, nmax + 1):
        lp[n] = lp[n - 1] + math.log(up[n - 1][0] / dn[n][0])
    for n in range(-1, -nmax - 1, -1):
        lp[n] = lp[n + 1] + math.log(dn[n + 1][0] / up[n][0])
    pi = {n: math.exp(v) for n, v in lp.items()}
    Z = sum(pi.values())
    pi = {n: v / Z for n, v in pi.items()}
    P = sum(pi[n] * (up[n][1] + dn[n][1]) / 2 for n in pi)
    Nn = sum(pi[n] * (up[n][0] + dn[n][0]) / 2 for n in pi)
    return pi, P, Nn


def weight_ratio(alpha, rule=("after", "after")):
    N0, P0 = rates(0.0, 0.0)
    pi, P, Nn = chain(alpha, rule)
    return P / P0, (P / Nn) / (P0 / N0), pi
