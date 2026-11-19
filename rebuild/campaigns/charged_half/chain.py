import sys, math, numpy as np
sys.dont_write_bytecode = True
T = 1 / (8 * math.pi)
D = np.load("grid.npz")
gn, js, w, wu, G = D["gnodes"], D["js"], D["w"], D["wu"], D["gamma"]
deg = 2 * js + 1


def gam_interp(g):
    """Chebyshev-node polynomial interpolation of Gamma(g) at every (j, w)."""
    out = np.zeros(G.shape[1:])
    n = len(gn)
    for k in range(n):
        lk = 1.0
        for m in range(n):
            if m != k:
                lk *= (g - gn[m]) / (gn[k] - gn[m])
        out += lk * G[k]
    return out


def rates(g):
    Gm = gam_interp(g)
    nf = 1 / (np.exp((w - g / 2) / T) + 1)
    Nn = np.sum(deg[:, None] * Gm * nf[None, :] * wu[None, :]) / (2 * math.pi)
    Pp = np.sum(deg[:, None] * Gm * (w * nf)[None, :] * wu[None, :]) / (2 * math.pi)
    return Nn, Pp


def chain(alpha, nmax=20):
    N = {n: rates(alpha * n)[0] for n in range(-nmax - 1, nmax + 2)}
    logpi = {0: 0.0}
    for n in range(1, nmax + 1):                       # pi(n)/pi(n-1) = N(e- emission at n-1: g = -alpha(n-1)) / N(e+ emission at n: g = +alpha n)
        logpi[n] = logpi[n - 1] + math.log(N[-(n - 1)] / N[n])
    for n in range(-1, -nmax - 1, -1):
        logpi[n] = logpi[n + 1] + math.log(N[-n - 1 + 0] / N[n]) if False else logpi[n + 1] + math.log(N[n + 1] / N[-n])  # symmetric check below
    return logpi


if __name__ == "__main__":
    al = 1 / 137.035999084
    N0, P0 = rates(0.0)
    print("N(0), P(0)", N0, P0, " (greybody P_1/2 = 4.09165e-5)")
    for g in (0.0, 0.0073, -0.0073, 0.05, -0.05, 0.1, -0.1):
        n_, p_ = rates(g); print("g", g, "N/N0", n_ / N0, "P/P0", p_ / P0)
    # birth-death chain: up rate (n -> n+1) = N(-alpha n) [electron], down rate (n -> n-1) = N(+alpha n) [positron]
    nmax = 25
    up = {n: rates(-al * n)[0] for n in range(-nmax, nmax + 1)}
    dn = {n: rates(+al * n)[0] for n in range(-nmax, nmax + 1)}
    lp = {0: 0.0}
    for n in range(1, nmax + 1):
        lp[n] = lp[n - 1] + math.log(up[n - 1] / dn[n])
    for n in range(-1, -nmax - 1, -1):
        lp[n] = lp[n + 1] + math.log(dn[n + 1] / up[n])
    pi = {n: math.exp(v) for n, v in lp.items()}
    Z = sum(pi.values()); pi = {n: v / Z for n, v in pi.items()}
    print("pi(0..5)", [round(pi[n], 4) for n in range(6)], "pi(nmax)", pi[nmax], "<n^2>", sum(n * n * v for n, v in pi.items()))
    Pav = sum(pi[n] * (rates(-al * n)[1] + rates(al * n)[1]) / 2 for n in pi)
    Nav = sum(pi[n] * (rates(-al * n)[0] + rates(al * n)[0]) / 2 for n in pi)
    print("weight ratio <P>/P0 =", Pav / P0, " ; 0.142/0.147 =", 0.142 / 0.147)
    print("energy ratio =", (Pav / Nav) / (P0 / N0), " ; 4.18/4.22 =", 4.18 / 4.22)
