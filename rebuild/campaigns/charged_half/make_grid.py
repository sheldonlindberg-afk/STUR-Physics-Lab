import sys, json, math, numpy as np
sys.dont_write_bytecode = True
from multiprocessing import Pool
import reference_solver as S

T = 1 / (8 * math.pi)
GMAX = 0.12
NG = 7
gnodes = GMAX * np.cos(np.pi * (2 * np.arange(NG) + 1) / (2 * NG))           # Chebyshev nodes
js = [k + 0.5 for k in range(10)]
panels = [(0.0, 4.0, 16), (4.0, 12.0, 16), (12.0, 36.0, 16)]
u, wu = [], []
for a, b, n in panels:
    x, w = np.polynomial.legendre.leggauss(n)
    u += list(0.5 * (b - a) * x + 0.5 * (b + a)); wu += list(0.5 * (b - a) * w)
u, wu = np.array(u), np.array(wu)
wgrid = T * u


def job(args):
    ig, ij, iw = args
    return ig, ij, iw, S.gamma(js[ij], float(wgrid[iw]) , float(gnodes[ig]))


if __name__ == "__main__":
    tasks = [(ig, ij, iw) for ig in range(NG) for ij in range(len(js)) for iw in range(len(wgrid))]
    out = np.zeros((NG, len(js), len(wgrid)))
    with Pool(4) as p:
        for k, (ig, ij, iw, v) in enumerate(p.imap_unordered(job, tasks, chunksize=8)):
            out[ig, ij, iw] = v
    np.savez("grid.npz", gnodes=gnodes, js=js, w=wgrid, wu=wu * T, gamma=out)
    print("done")
