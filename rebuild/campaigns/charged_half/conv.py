import sys, math, numpy as np
sys.dont_write_bytecode = True
from multiprocessing import Pool
import reference_solver as S
from chain import gam_interp, w, js, wu, T, deg
# (a) g interpolation: direct solves at off-node g
def job(a):
    j, ww, g, rm = a
    return S.gamma(j, ww, g, rmax_w=rm)
pts = [(0.5, w[5], 0.037, 3000.0), (0.5, w[20], -0.071, 3000.0), (1.5, w[30], 0.113, 3000.0), (2.5, w[40], -0.019, 3000.0), (0.5, w[2], 0.09, 3000.0),
       (0.5, w[20], -0.071, 9000.0), (1.5, w[30], 0.113, 9000.0)]
if __name__ == "__main__":
    with Pool(4) as p:
        res = p.map(job, pts)
    for (j, ww, g, rm), v in zip(pts, res):
        i = js.index(j) if hasattr(js, 'index') else list(js).index(j); k = list(w).index(ww)
        print(f"j={j} w={ww:.4f} g={g} rmax_w={rm}: direct {v:.10f}  interp {gam_interp(g)[i, k]:.10f}  rel {abs(gam_interp(g)[i,k]/v-1):.1e}")
