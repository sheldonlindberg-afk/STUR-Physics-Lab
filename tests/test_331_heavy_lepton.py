"""Pins src/m331_heavy_lepton.py: the beta = +1/sqrt3 heavy leptons against LHC searches."""
import json, os, sys
from math import pi, sqrt
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import m331_heavy_lepton as H


def test_partonic_qed_massive():
    bos = [(0.0, 0.0, {"u": (1.0, 1.0)}, (1.0, 1.0))]
    for m in (0.0, 300.0, 480.0):
        b = sqrt(1 - 4 * m * m / 1e6)
        ref = 4 * pi * H.AEM**2 / 3e6 * b * (3 - b * b) / 2
        assert abs(H.sigma_hat(1e6, m, "u", bos) * 3 / ref - 1) < 1e-12


def test_pythia_crosscheck():
    for r in json.load(open(os.path.join(H.DATA, "pythia_crosscheck.json"))):
        mine = H.sigma_pair(r["mF"], MZp=r["MZp"], mode="doublet", widths=(r["GammaZ"], r["GammaZp"]), aem=H.AEM_MZ)
        assert abs(mine / r["pythia_fb"] - 1) < 0.02          # Pythia MC error ~0.5%


def test_reproduces_atlas_singlet_limits():
    # ATLAS quotes 320 GeV (e) and 400 GeV (mu); the 3-3-1 Z' adds ~1% here
    assert abs(H.mass_limit("e", "obs")[1] - 321) < 5
    assert abs(H.mass_limit("mu", "obs")[1] - 404) < 5


def test_tau_window():
    lo, hi = H.mass_limit("tau", "obs", K=1.0)
    assert 115 < lo < 130 and 155 < hi < 175                 # CMS quotes 125-150 GeV


def test_geometric_mean_and_untested():
    trip, gm, p3, p1 = H.geometric_mean_check()
    assert abs(p3 - p1) < 1e-3
    low = H.lightest_allowed(H.run2_limits())
    assert abs(H.geo(low) - 235) < 5 and H.geo(low) < H.MSTAR[0] - H.MSTAR[1]


def test_hl_lhc():
    res = H.hl_reach()
    assert abs(res["e"][0][0] - 735) < 10 and abs(res["tau"][0][0] - 455) < 10
    mz, MV, a, b = H.hl_threshold()
    assert abs(mz - 5500) < 20 and abs(a - 621) < 8
