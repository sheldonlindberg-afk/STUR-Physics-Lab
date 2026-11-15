"""Pins src/m331_matrix_check.py: the beta-function coefficients from explicit generator matrices."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import numpy as np
import m331_matrix_check as M
import m331_exact as E


def test_generators_and_adjoint_casimir():
    for N in (2, 3, 5):
        g = M.su_generators(N)
        assert np.allclose([[np.trace(a @ b) for b in g] for a in g], np.eye(N * N - 1) / 2)
        assert abs(M.adjoint_casimir(g) - N) < 1e-10


def test_standard_model_from_matrices():
    a, b, top = M.sm()
    assert np.allclose(a, [41 / 10, -19 / 6, -7])
    assert np.allclose(b, [[199 / 50, 27 / 10, 44 / 5], [9 / 10, 35 / 6, 12], [11 / 10, 9 / 2, -26]])
    assert np.allclose(top, [17 / 10, 3 / 2, 2])


def test_331_coefficients_agree_with_the_tabulated_route():
    for v in E.MODELS:
        for Nc, Ng in ((3, 3), (5, 5), (2, 4)):
            dg, dy = M.compare(Nc, v, Ng)
            assert dg < 1e-10 and dy < 1e-10


def test_a_wrong_yukawa_is_caught():
    import pytest
    from fractions import Fraction as F
    with pytest.raises(AssertionError):                    # no scalar of the needed charge
        M.yukawa((3, 3), ((None, 3, 3), F(1, 3)), ((None, 1, 3), F(-2, 3)), [F(5, 3)])
