"""Cross-build comparison of the gauge-dependent classes SE and VBW (campaign dr_xi): run from the campaigns directory, python3 dr_xi/cross_build.py"""
import importlib.util as iu, os
H = os.path.dirname(os.path.abspath(__file__))
def L(k):
    sp = iu.spec_from_file_location("d" + k, os.path.join(H, "builds", k, "dr_xi.py")); m = iu.module_from_spec(sp); sp.loader.exec_module(m); return m
a, b = L("a"), L("b")
worst = 0.0
for p in [(80.38, 91.19, 125.0, 1 / 128), (75., 91.19, 300., 1 / 130), (85., 91.19, 1000., 1 / 129)]:
    for xi in (1e-3, 0.3, 1.0, 4.0, 25.0, 1000.0):
        for mu in (30.0, p[0], 900.0):
            sa, sb = a.delta_r_se(p[0], p[1], p[2], p[3], xi, mu), b.delta_r_se(p[0], p[1], p[2], p[3], xi, mu)
            va, vb = a.delta_r_vbw(p[0], p[1], p[3], xi, mu), b.delta_r_vbw(p[0], p[1], p[3], xi, mu)
            worst = max(worst, abs(sa - sb) / (abs(sa) + 1e-6), abs(va - vb) / (abs(va) + 1e-6))
print(f"SE and VBW of the two builds, xi > 0, three points x six xi x three mu: worst relative difference {worst:.1e}")
for p in [(80.38, 91.19, 125.0, 1 / 128)]:
    print("xi = 0 (Landau, IR pole subtracted in MS-bar by each builder; the convention differs):", a.delta_r_se(*p[:4], 0.0, p[0]) - b.delta_r_se(*p[:4], 0.0, p[0]))
