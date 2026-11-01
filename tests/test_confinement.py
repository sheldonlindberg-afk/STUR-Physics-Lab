"""Pins the confinement / replica results of src/stur_confinement.py (small chain)."""
import os, sys
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import stur_confinement as C


def test_string_enters_modular_energy_not_entropy():
    sigma, rows, eps = C.run(12, 1.0, 0.5, ells=[1, 2, 3, 4], verbose=False)
    assert abs(sigma - 0.230) < 2e-3                       # confining, screened below q^2 = 0.25
    dS = [r["dS"] for r in rows]; dK = [r["dK"] for r in rows]
    assert abs(dS[3] - dS[2]) < 2e-3                         # entropy saturates
    assert dK[3] / dK[0] > 3.5                               # modular energy keeps growing
    for r in rows[2:]:
        assert abs(r["dK"] / r["KBW"] - 1) < 0.03            # Bisognano-Wichmann on the lattice
        assert r["D"] > 0
