"""Pins front 13: timescape vs flat LCDM on Pantheon+ (official standardization)."""
import os, sys
import numpy as np
import pytest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import god_eq_timescape as T


def test_timescape_distance_checks():
    f = 0.695
    b, t0 = T.ts_params(f)
    from scipy.integrate import quad
    num = quad(lambda t: 1 / (T.ts_gamma(t, b) * t ** (2 / 3)), 0.05, t0, epsabs=1e-13)[0]
    assert abs(T.ts_F(t0, b) - T.ts_F(0.05, b) - num) < 1e-10      # closed form F
    assert abs(T.ts_z(t0, f)) < 1e-12
    H0, q0 = T.ts_dressed_metric_H_q(f)
    assert abs(H0 - T.ts_H0_dressed(f)) < 1e-8
    q0_lit = -(1 - f) * (8 * f**3 + 39 * f**2 - 12 * f - 8) / (4 + f + 4 * f * f) ** 2
    assert abs(q0 - q0_lit) < 1e-6                                 # Wiltshire q0
    q0DL, slope = T.q0_from_DL(lambda z: T.ts_DL(np.array([z]), f, n=20000)[0])
    assert abs(slope - 1 / T.ts_H0_dressed(f)) < 1e-4              # D_L ~ z / H0_dressed
    assert q0DL < 0 and q0 < 0                                     # apparent acceleration


def test_lcdm_q0():
    q0, slope = T.q0_from_DL(lambda z: T.lcdm_DL(np.array([z]), 0.3, n=20000)[0])
    assert abs(slope - 1) < 1e-4 and abs(q0 + 0.55) < 3e-3


@pytest.fixture(scope="module")
def data():
    try:
        return T.load_pantheon()
    except Exception as e:                                        # offline: skip
        pytest.skip(f"Pantheon+ data unavailable: {e}")


def test_pantheon_lcdm_reference_and_timescape(data):
    col, C = data
    L = T.Likelihood(col, C, 0.01, "zHD")
    assert L.N == 1580
    gOm, gfv = np.linspace(0.05, 0.7, 651), np.linspace(0.3, 0.97, 671)
    Om, sOm, chiL, lnZL = T.fit_1d(gOm, L.scan(T.lcdm_DL, gOm), T.PRIOR_OM)
    fv, sfv, chiT, lnZT = T.fit_1d(gfv, L.scan(T.ts_DL, gfv), T.PRIOR_FV)
    assert abs(Om - 0.334) < 0.005 and abs(sOm - 0.018) < 0.002  # Brout et al. 2022
    assert 4.5 < chiT - chiL < 6.0                                # LCDM mildly preferred
    assert -4.5 < lnZT - lnZL < -3.5
    assert abs(fv - 0.853) < 0.01
    assert L.chi2(T.eds_DL(L.z)) - chiL > 600                     # smooth matter-only fails
