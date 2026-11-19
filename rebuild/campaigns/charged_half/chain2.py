import sys, math, numpy as np
sys.dont_write_bytecode = True
from chain import rates, T, gam_interp, w, wu, deg
al = 1 / 137.035999084
N0, P0 = rates(0.0)

def rates2(gG, gC):
    """Gamma at coupling gG, occupation at chemical coupling gC."""
    Gm = gam_interp(gG)
    nf = 1 / (np.exp((w - gC / 2) / T) + 1)
    return (np.sum(deg[:, None] * Gm * nf[None, :] * wu[None, :]) / (2 * math.pi), np.sum(deg[:, None] * Gm * (w * nf)[None, :] * wu[None, :]) / (2 * math.pi))

def run(rule):
    # electron (q=-1): n -> n+1, positron (q=+1): n -> n-1
    def gG(q, n):
        na = n - q                                         # hole charge after emission
        nmid = n - q / 2
        return {"before": al * q * n, "after": al * q * na}[rule[0]]
    def gC(q, n):
        na = n - q; nmid = n - q / 2
        return {"before": al * q * n, "after": al * q * na, "mid": al * q * nmid}[rule[1]]
    nmax = 30
    up = {n: rates2(gG(-1, n), gC(-1, n)) for n in range(-nmax, nmax + 1)}
    dn = {n: rates2(gG(+1, n), gC(+1, n)) for n in range(-nmax, nmax + 1)}
    lp = {0: 0.0}
    for n in range(1, nmax + 1): lp[n] = lp[n - 1] + math.log(up[n - 1][0] / dn[n][0])
    for n in range(-1, -nmax - 1, -1): lp[n] = lp[n + 1] + math.log(dn[n + 1][0] / up[n][0])
    pi = {n: math.exp(v) for n, v in lp.items()}; Z = sum(pi.values()); pi = {n: v / Z for n, v in pi.items()}
    Pav = sum(pi[n] * (up[n][1] + dn[n][1]) / 2 for n in pi); Nav = sum(pi[n] * (up[n][0] + dn[n][0]) / 2 for n in pi)
    n2 = sum(n * n * v for n, v in pi.items()); mean = sum(n * v for n, v in pi.items())
    return Pav / P0, (Pav / Nav) / (P0 / N0), n2, mean

for rule in (("before", "before"), ("after", "after"), ("after", "mid"), ("after", "before"), ("before", "after"), ("mid" if False else "after", "after")):
    r = run(rule)
    print(rule, "weight ratio %.5f  energy ratio %.5f  <n^2> %.3f  <n> %.3f" % r)
print("literature: weight", 0.142 / 0.147, " energy", 4.18 / 4.22)
