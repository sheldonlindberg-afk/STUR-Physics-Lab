"""Pins the option B / C wall numbers."""
import numpy as np


def test_confinement_scale_and_constant_entropy_shift():
    hbar, c, eV = 1.054571817e-34, 2.99792458e8, 1.602176634e-19
    RH = c / (67.4e3 / 3.0857e22)
    assert abs(hbar * c / RH / eV - 1.44e-33) < 0.02e-33
    assert abs(4 * np.pi * 0.02424 - 0.3046) < 1e-3
