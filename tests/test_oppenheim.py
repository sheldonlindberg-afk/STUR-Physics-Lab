"""Pins src/stur_oppenheim.py: Oppenheim's decoherence-diffusion trade-off for gravity."""
import io, os, sys, contextlib
import numpy as np
from scipy.integrate import quad
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import stur_oppenheim as O


def test_qubit_tradeoff_constant():
    assert O.qubit_positivity(0.99) < -0.009          # below the bound: not positive
    assert O.qubit_positivity(1.01) > 0.009
    assert abs(O.qubit_positivity(1.0)) < 1e-12        # on the bound
    D0, Dv, ratio, mdet = O.qubit_measurement_feedback()
    assert abs(ratio - 1) < 1e-6 and abs(mdet) < 1e-15  # measurement + feedback saturates it


def test_backaction_floor_is_diosi_penrose():
    for q in (1e2, 1e9, 1e14):
        v, d = O.min_total_over_D0(q)
        assert abs(v - 1) < 1e-5 and abs(d - 1) < 3e-3


def test_h_abs_exact():
    for k in (1e-3, 0.3, 5.0, 37.2, 123.4):
        ref = quad(lambda u: u * abs(np.sin(k * u)), 0, 1, limit=4000, epsabs=1e-13)[0]
        assert abs(O.h_abs(np.array([k]))[0] - ref) < 1e-8
    assert abs(O.h_abs(np.array([1e6]))[0] - 1 / np.pi) < 1e-5


def test_joint_bound_value_and_limit():
    I = O.I_joint(O.D_A)
    assert abs(I / O.I_split_limit(O.R_A) - 1) < 2e-3
    assert abs(O.joint_bound(O.D_A) / 1.0132e-25 - 1) < 2e-3
    assert 0.95e-4 < O.r0_where_bound_meets_requirement() < 1.05e-4


def test_joint_bound_holds_for_random_kernels_and_is_tight():
    rng = np.random.default_rng(1)
    dx, R, M = 50e-6, 1e-6, 1e-14
    # saturating kernels (Cauchy-Schwarz equality), on the trade-off line D0 S_J = 1/4
    def sat(q, u):
        K = 4 * np.pi * O.G / q**2
        w1 = M**2 * (1 - np.cos(q * u * dx)) + 1e-300
        w2 = (q * u) ** 2 * K**2 + 1e-300
        return 0.5 * np.sqrt(w2 / w1)
    g, s, b, _ = O.grid_gamma_Sa(sat, lambda q, u: 1 / (4 * sat(q, u)), dx, M, R)
    assert abs(g * s / b - 1) < 1e-6
    for _ in range(5):
        amp = 10 ** rng.uniform(-30, 10)
        slope = rng.uniform(-3, 3)
        D0 = lambda q, u: amp * (q * R) ** slope * (1.5 + np.cos(3 * u))
        SJ = lambda q, u: (1 + rng.uniform(0, 2)) / (4 * D0(q, u))
        g, s, b, _ = O.grid_gamma_Sa(D0, SJ, dx, M, R)
        assert g * s >= b * (1 - 1e-9)


def test_heating_floors():
    assert 0.45 < O.internal_heating_per_kg(O.DIAMOND) < 0.55
    assert abs(O.internal_heating_per_kg(O.DIAMOND, O.cutoff(1)) /
               O.internal_heating_per_kg(O.DIAMOND) - 1) < 1e-3
    assert O.internal_heating_per_kg(O.SILICA) / O.EARTH_W_PER_KG > 1e10
    # agrees with the point-nucleus formula once R0 >> 1 fm
    import stur_thermo_gravity as T
    assert abs(O.internal_heating_per_kg(O.DIAMOND, O.R0_DONADI) / T.heating_per_kg(O.R0_DONADI) - 1) < 1e-6


def test_reference_output_matches():
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        O.main()
    ref = open(os.path.join(os.path.dirname(__file__), "..", "results", "oppenheim", "output.txt")).read()
    assert buf.getvalue() == ref


def test_kernel_free_bound_any_cq_model():
    worst, sat = O.operator_check(trials=60)
    assert worst >= 1 - 1e-9 and abs(sat - 1) < 1e-9
    for x in (0.5, 1.0, 1.5, 2.0, 5.0):
        assert abs(O.sphere_force_closed(x * O.R_A) / O.sphere_force_fourier(x * O.R_A) - 1) < 1e-4
    assert abs(O.sphere_force_closed(O.R_A) / (O.G * O.M_A**2 / O.R_A**2) - 0.46875) < 1e-12
    asd = (2 * O.general_bound(O.R_A) / O.GAMMA_BUDGET) ** 0.5
    assert abs(asd / 6.68e-13 - 1) < 5e-3
