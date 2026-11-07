"""Pins the 'room for STUR' numbers in src/stur_predictions.py."""
import numpy as np
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import stur_predictions as P


def test_enhancement_needed_for_graviton_background():
    dE = P.h * P.c / 698.4e-9
    g = (P.kB * 0.905 / P.hbar) * (dE / P.EP) ** 2
    assert 3.5e41 < 1e-3 / g < 4.5e41
