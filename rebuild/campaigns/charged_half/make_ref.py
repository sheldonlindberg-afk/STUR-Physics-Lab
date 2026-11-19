import sys, json, math
sys.dont_write_bytecode = True
from multiprocessing import Pool
import reference_solver as S
pts = []
for g in (-0.1, -0.0365, -0.0073, 0.0073, 0.05, 0.12):
    for j, w in ((0.5, 0.02), (0.5, 0.15), (0.5, 0.6), (1.5, 0.12), (1.5, 0.5), (2.5, 0.35), (3.5, 0.8)):
        pts.append((j, w, g))
pts += [(0.5, 0.002, 0.05), (0.5, 0.004, 0.0365), (1.5, 0.01, 0.12), (0.5, 0.03, -0.12)]   # w below or near g/2 (horizon frequency of either sign)
def job(p):
    return [list(p), S.gamma(p[0], p[1], p[2], rmax_w=6000.0, rtol=1e-13)]
if __name__ == "__main__":
    with Pool(4) as pool:
        res = pool.map(job, pts)
    json.dump(res, open("reference_gamma.json", "w"))
    print(len(res), min(r[1] for r in res), max(r[1] for r in res))
