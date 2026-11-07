"""Pins the 2+1D Z2 gauge-Higgs results (small ladder, fast)."""
import os, sys
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import stur_z2_higgs as Z


def test_dynamical_string_enters_modular_energy():
    sigma, rows = Z.run(Lx=5, h=0.8, Gq=6.0, xb=5, ells=(1, 2, 3), verbose=False)
    assert abs(sigma - 1.408) < 0.01                        # confining string
    assert all(r["nq"] > 0.99 for r in rows)                # quark stays pinned
    dS = [r["dS"] for r in rows]
    assert dS[2] - dS[1] < 0.6 * (dS[1] - dS[0])            # entropy saturates (ratio 0.53 here)
    r2, r3 = rows[1], rows[2]
    cq, cs = np.linalg.solve([[r2["wq"], r2["ws"]], [r3["wq"], r3["ws"]]], [r2["dK"], r3["dK"]])
    assert cs > 1.0 and cq > 1.0                            # K weights the string energy (1+1D: 0)
