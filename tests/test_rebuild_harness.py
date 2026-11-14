"""The rebuild harness must pass a correct build and catch broken or dishonest ones.

A gatekeeper that has never been seen to fail proves nothing, so each tier is shown failing
on a planted defect: a hard-coded answer, wrong physics, a forbidden import, a magic number,
a mislabelled provenance.
"""
import os
import shutil
import sys
import textwrap

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REBUILD = os.path.join(ROOT, "rebuild")
REF = os.path.join(REBUILD, "_selftest", "reference_build")
sys.path.insert(0, REBUILD)

import contract  # noqa: E402
import harness   # noqa: E402


def _statuses(rep):
    return {k: v["status"] for k, v in rep["stages"].items()}


@pytest.fixture(scope="module")
def reference_report():
    return harness.run(REF, mode="verifier", lint=False)


def test_reference_passes_every_tier(reference_report):
    assert reference_report["ok"], harness.summarize(reference_report)
    assert set(_statuses(reference_report).values()) == {"pass"}


def test_every_stage_has_blind_and_oracle_checks(reference_report):
    for name, rec in reference_report["stages"].items():
        assert rec["blind"], name
        assert rec["oracle"], name


def _mutant(tmp_path, stage, extra):
    """A copy of the reference build with `extra` appended to one stage module."""
    d = tmp_path / "mutant"
    shutil.copytree(REF, d)
    with open(d / f"{stage}.py", "a") as fh:
        fh.write("\n" + textwrap.dedent(extra))
    return str(d)


def test_hardcoded_phase_is_caught(tmp_path):
    d = _mutant(tmp_path, "graviton", """
        def entangling_phase(m, dx, hold, ramp, gap, n=4001):
            return 2.1868
    """)
    rep = harness.run(d, mode="builder", lint=False)
    assert _statuses(rep)["graviton"] == "fail"
    assert _statuses(rep)["links"].startswith("blocked")          # the gate holds later stages


def test_wrong_physics_is_caught_by_blind_checks(tmp_path):
    # Forget the 1/2 in the trace reversal: light would bend as much as a mass.
    d = _mutant(tmp_path, "graviton", """
        from fractions import Fraction as _F
        def tpt(T1, T2):
            eta = (-1, 1, 1, 1)
            return sum(_F(T1[a]) * T2[a] for a in range(4)) - sum(eta[a] * T1[a] for a in range(4)) * sum(eta[a] * T2[a] for a in range(4))
    """)
    rep = harness.run(d, mode="builder", lint=False)
    assert _statuses(rep)["graviton"] == "fail"


def test_wrong_charges_are_caught(tmp_path):
    d = _mutant(tmp_path, "gauge331", """
        from fractions import Fraction as _F
        def quark_charges(Nc):
            return _F(2, 3), _F(-1, 3)        # the N_c = 3 values typed in for every N_c
    """)
    rep = harness.run(d, mode="builder", lint=False)
    assert _statuses(rep)["gauge331"] == "fail"


def test_cached_input_is_caught_by_sensitivity(tmp_path):
    d = _mutant(tmp_path, "blackholes", """
        import inputs as _i
        _G = _i.G_NEWTON                      # read once at import: mutations can't reach it
        def nariai_mass_kg(Lam):
            return _i.C_LIGHT ** 2 / (3 * _G * Lam ** 0.5)
    """)
    rep = harness.run(d, mode="builder", lint=False)
    fails = [l for l, ok, _ in rep["stages"]["blackholes"]["sensitivity"] if not ok]
    assert fails == ["Nariai mass reads G"]


def test_oracle_catches_what_blind_checks_cannot(tmp_path):
    # Right shape, wrong normalization: the pi0 width a factor 2 off passes every scaling law.
    d = _mutant(tmp_path, "links", """
        _w = pi0_width_eV
        def pi0_width_eV(*a):
            return 2 * _w(*a)
    """)
    assert harness.run(d, mode="builder", lint=False)["ok"]
    rep = harness.run(d, mode="verifier", lint=False)
    fails = [l for l, ok, _ in rep["stages"]["links"]["oracle"] if not ok]
    assert fails == ["pi0 width 7.785 eV", "pi0 width from rung 1's charges and the weak decay's f_pi: 7.7417 eV (force chain)"]


def test_quoted_provenance_where_derivation_required(tmp_path):
    d = _mutant(tmp_path, "casimir", """
        PROVENANCE = dict(PROVENANCE, cp_integral=("quoted", "Casimir and Polder 1948"))
    """)
    rep = harness.run(d, mode="builder", lint=False)
    assert _statuses(rep)["casimir"] == "fail"


def test_missing_export_fails_contract(tmp_path):
    d = _mutant(tmp_path, "desitter", "del ell_from_lambda\n")
    rep = harness.run(d, mode="builder", lint=False)
    assert _statuses(rep)["desitter"] == "fail"


def _lint(tmp_path, stage, code):
    p = tmp_path / f"{contract.stage(stage)['module']}.py"
    p.write_text(textwrap.dedent(code))
    return {l: (ok, d) for l, ok, d in harness.tier_lint(contract.stage(stage), str(p))}


def test_lint_accepts_clean_code(tmp_path):
    res = _lint(tmp_path, "graviton", """
        import inputs
        from math import sqrt, pi
        from fractions import Fraction
        import toolkit, chiral
        def f(m, r):
            return inputs.G_NEWTON * m / r * 0.5 + 1e-12 * 2.0
    """)
    assert all(ok for ok, _ in res.values()), res


@pytest.mark.parametrize("code,label", [
    ("import numpy\n", "imports: standard library, inputs, earlier stages only"),
    ("import links\n", "imports: standard library, inputs, earlier stages only"),      # a LATER stage
    ("from inputs import G_NEWTON\n", "imports: standard library, inputs, earlier stages only"),
    ("x = open('src/ladder_standalone.py').read()\n", "no file access, exec or eval"),
    ("x = 'see ladder_standalone'\n", "no reference to the oracle or src/"),
    ("phase = 2.1868\n", "no typed-in physical numbers (take them from inputs.py or compute them)"),
    ("G = 6.6743e-11\n", "no typed-in physical numbers (take them from inputs.py or compute them)"),
    ("eps = 5.7\n", "no typed-in physical numbers (take them from inputs.py or compute them)"),
    ("rho = 3510\n", "no typed-in physical numbers (take them from inputs.py or compute them)"),
])
def test_lint_rejects(tmp_path, code, label):
    res = _lint(tmp_path, "graviton", code)
    assert not res[label][0], res


def test_crossbuild_agrees_with_itself():
    res = harness.tier_crossbuild(REF, REF)
    assert res and all(ok for _, ok, _ in res), res


ACCEPTED = sorted(d for d in (os.listdir(os.path.join(REBUILD, "builds")) if os.path.isdir(os.path.join(REBUILD, "builds")) else [])
                  if os.path.exists(os.path.join(REBUILD, "builds", d, "ACCEPTED.md")))


@pytest.mark.parametrize("build_id", ACCEPTED)
def test_accepted_builds_stay_green(build_id):
    """Every accepted AI build keeps passing every tier, so drift in either the build's
    environment or the reference shows up in CI."""
    rep = harness.run(os.path.join(REBUILD, "builds", build_id), mode="verifier")
    assert rep["ok"], harness.summarize(rep)


def test_disconnected_rung_is_caught(tmp_path):
    # Rung 4 recomputes 1/r privately instead of using rung 2's exchange transform: right
    # numbers, no connection. Only the connections tier sees it.
    d = _mutant(tmp_path, "graviton", """
        import inputs as _i
        from math import sqrt as _sq
        def entangling_phase(m, dx, hold, ramp, gap, n=4001):
            total = hold + 2 * ramp
            ys = [2 * (1 / gap - 1 / _sq(gap * gap + (dx * ramp_profile(total * i / (n - 1), hold, ramp)) ** 2))
                  for i in range(n)]
            return _i.G_NEWTON * m * m / _i.HBAR * total / (n - 1) * (sum(ys) - (ys[0] + ys[-1]) / 2)
    """)
    rep = harness.run(d, mode="verifier", lint=False)
    g = rep["stages"]["graviton"]
    assert all(ok for _, ok, _ in g["blind"]) and all(ok for _, ok, _ in g["oracle"])     # numbers are right
    assert [l for l, ok, _ in g["connections"] if not ok] == \
        ["L-2to4: graviton.entangling_phase uses chiral.yukawa, toolkit.trapezoid"]


def test_every_connection_is_exercised(reference_report):
    seen = {l.split(":")[0] for rec in reference_report["stages"].values() for l, _, _ in rec.get("connections", [])}
    assert seen == {c["id"] for c in contract.CONNECTIONS}


def test_lint_rejects_from_stage_import(tmp_path):
    res = _lint(tmp_path, "graviton", "from toolkit import trapezoid\n")
    assert not res["imports: standard library, inputs, earlier stages only"][0]


# Leaks 3 and 4 of build 2026-11-a: closed forms moved from the blind checks to the oracle.
# Each mutant below has the right properties (passes the builder gate) and the wrong closed form.
def test_wrong_charge_normalization_needs_the_oracle(tmp_path):
    d = _mutant(tmp_path, "gauge331", """
        _ie2 = inv_e2
        def inv_e2(variant, g, gX):
            return 1.01 * _ie2(variant, g, gX)    # still homogeneous, still above 1/g^2 and 1/gX^2
    """)
    rep = harness.run(d, mode="builder", lint=False)
    assert rep["stages"]["gauge331"]["status"] == "pass"     # rung 1's own tier can't see it
    # downstream, stage running's matching (through inv_e2) does: the rungs check each other
    assert [l for l, ok, _ in rep["stages"]["running"]["blind"] if not ok] == \
        ["matching keeps g_L = g_2 and rung 1's photon coupling"]
    rep = harness.run(d, mode="verifier", lint=False)
    fails = [l for l, ok, _ in rep["stages"]["gauge331"]["oracle"] if not ok]
    assert fails == ["-1/sqrt3: 1/e^2 = (1 + beta^2)/g^2 + 1/gX^2", "+1/sqrt3: 1/e^2 = (1 + beta^2)/g^2 + 1/gX^2"]


def test_wrong_kappa_normalization_needs_the_oracle(tmp_path):
    # kappa doubled everywhere, and the Euclidean ratio redefined to match: self-consistent, wrong
    d = _mutant(tmp_path, "blackholes", """
        _kk, _ks, _ec = killing_kappa, kappa_from_spin_connection, euclidean_cone_ratio
        def killing_kappa(f, r0, h):
            return 2 * _kk(f, r0, h)
        def kappa_from_spin_connection(M, l):
            return tuple(2 * k for k in _ks(M, l))
        def euclidean_cone_ratio(f, rh, beta, eps):
            return _ec(f, rh, 2 * beta, eps)
    """)
    rep = harness.run(d, mode="builder", lint=False)
    assert [l for l, ok, _ in rep["stages"]["blackholes"]["blind"] if not ok] == []
    rep = harness.run(d, mode="verifier", lint=False)
    fails = {l for l, ok, _ in rep["stages"]["blackholes"]["oracle"] if not ok}
    assert {"Killing kappa_b = f'(r_b)/2", "Killing kappa_c = -f'(r_c)/2", "Euclidean section smooth at period 2 pi/(f'/2)"} <= fails


def test_wrong_lambda_relation_needs_the_oracle(tmp_path):
    d = _mutant(tmp_path, "desitter", """
        def ell_from_lambda(Lam):
            return (2 / Lam) ** 0.5               # the right scaling, the wrong coefficient
    """)
    rep = harness.run(d, mode="builder", lint=False)
    assert [l for l, ok, _ in rep["stages"]["desitter"]["sensitivity"] if not ok] == []
    rep = harness.run(d, mode="verifier", lint=False)
    fails = [l for l, ok, _ in rep["stages"]["desitter"]["oracle"] if not ok]
    assert "Lambda l^2 = 3" in fails


def test_wrong_pion_mass_needs_the_oracle(tmp_path):
    d = _mutant(tmp_path, "chiral", """
        _sv = sigma_model_vacuum
        def sigma_model_vacuum(lam, v, H):
            s0, m2 = _sv(lam, v, H)
            return s0, 1.01 * m2                  # still positive and linear in H
    """)
    rep = harness.run(d, mode="builder", lint=False)
    assert [l for l, ok, _ in rep["stages"]["chiral"]["blind"] if not ok] == []
    rep = harness.run(d, mode="verifier", lint=False)
    fails = [l for l, ok, _ in rep["stages"]["chiral"]["oracle"] if not ok]
    assert len(fails) == 2 and all(l.startswith("m_pi^2 = H/<sigma>") for l in fails)


def test_wrong_curvature_is_caught(tmp_path):
    # C1 of build 2026-11-a: cR = 2 is an epsilon identity and can't see R^ab. A curvature with the
    # omega ^ omega term dropped (R = d omega only) must now fail.
    d = _mutant(tmp_path, "desitter", """
        import _ref as _r
        def ricci_scalar(M, l, x):
            f, fp = _r._sds(M, l)
            return _r.ricci_scalar(M, l, x) - 2 * (1 - f(x[1])) / x[1] ** 2     # wrong: angular omega^omega terms dropped
    """)
    rep = harness.run(d, mode="verifier", lint=False)
    assert [l for l, ok, _ in rep["stages"]["desitter"]["blind"] if not ok] == \
        ["ricci_scalar is the contraction of d omega + omega ^ omega; R ~ 1/length^2"]
    assert all(not ok for l, ok, _ in rep["stages"]["desitter"]["oracle"] if l.startswith("Ricci scalar"))


# Audit of builds 2026-11-a and 2026-11-b (AUDIT.md): each mutant below passed every tier before
# the audit's checks, and must now fail.
_WRONG_TETRAD = """
    import math as _m
    def spin_connection(x, f, fp):
        t, r, th, ph = x
        sf = _m.sqrt(f(r))
        E = [[0.0] * 4 for _ in range(4)]
        E[0][0], E[1][1], E[2][2], E[3][3] = sf, 1 / sf, r, {E33}
        w = [[[0.0] * 4 for _ in range(4)] for _ in range(4)]
        w[0][1][0] = w[1][0][0] = fp(r) / 2
        w[2][1][2], w[1][2][2] = sf, -sf
        w[3][1][3], w[1][3][3] = {W31}, -({W31})
        w[3][2][3] = {W32}
        w[2][3][3] = -w[3][2][3]
        return E, w
    def ricci_scalar(M, l, x, h=1e-5):              # made consistent with the wrong omega, so ricci_two_routes passes
        f = lambda r: 1 - 2 * M / r - r * r / l**2
        fp = lambda r: 2 * M / r**2 - 2 * r / l**2
        E, w = spin_connection(x, f, fp)
        dw = []
        for mu in range(4):
            p, q = list(x), list(x)
            p[mu] += h
            q[mu] -= h
            a, b = spin_connection(p, f, fp)[1], spin_connection(q, f, fp)[1]
            dw.append([[[(a[i][j][n] - b[i][j][n]) / (2 * h) for n in range(4)] for j in range(4)] for i in range(4)])
        return sum((dw[a][a][b][b] - dw[b][a][b][a] + sum(w[a][c][a] * w[c][b][b] - w[a][c][b] * w[c][b][a] for c in range(4)))
                   / (E[a][a] * E[b][b]) * (-1 if b == 0 else 1) for a in range(4) for b in range(4))
"""


def test_wrong_tetrad_is_caught_by_blind_checks(tmp_path):
    # e^3 = r dphi instead of r sin(theta) dphi, with omega torsion-free FOR THAT tetrad and ricci_scalar
    # consistent with it: the torsion and ricci_two_routes checks pass; the metric and flatness checks don't
    d = _mutant(tmp_path, "desitter", _WRONG_TETRAD.format(E33="r", W31="sf", W32="0.0"))
    rep = harness.run(d, mode="builder", lint=False)
    fails = [l for l, ok, _ in rep["stages"]["desitter"]["blind"] if not ok]
    assert "tetrad reproduces -f dt^2 + dr^2/f + r^2 dOmega^2 at random points" in fails
    assert "de Sitter F = 0 built from the build's spin_connection and so41_generator" in fails
    assert "spin connection is torsion-free and metric (omega_ab = -omega_ba)" not in fails


def test_omega_tuned_to_the_torsion_point_is_caught(tmp_path):
    # omega^3_2 = cos(1.1): right at the torsion check's theta, wrong d/dtheta (a branch on the test's argument)
    d = _mutant(tmp_path, "desitter", _WRONG_TETRAD.format(E33="r * _m.sin(th)", W31="sf * _m.sin(th)", W32="_m.cos(1.1)"))
    rep = harness.run(d, mode="builder", lint=False)
    assert [l for l, ok, _ in rep["stages"]["desitter"]["blind"] if not ok] == \
        ["de Sitter F = 0 built from the build's spin_connection and so41_generator"]


def test_pi0_mass_dependence_is_caught(tmp_path):
    # right at the physical pion mass (so the oracle's 7.785 eV passes), wrong power of m
    d = _mutant(tmp_path, "links", """
        import inputs as _i
        _w0 = pi0_width_eV
        def pi0_width_eV(alpha, fpi, mpi, Nc, Qu, Qd):
            return _w0(alpha, fpi, mpi, Nc, Qu, Qd) * mpi / _i.M_PI0
    """)
    rep = harness.run(d, mode="verifier", lint=False)
    assert all(ok for _, ok, _ in rep["stages"]["links"]["oracle"])
    assert [l for l, ok, _ in rep["stages"]["links"]["blind"] if not ok] == ["pi0 width ~ A^2 m^3 (dimensional analysis)"]


def test_point_mass_metric_normalization_is_caught_blind(tmp_path):
    # gamma = 1 but the wrong normalization: the old PPN check passed it, only the oracle saw it
    d = _mutant(tmp_path, "graviton", """
        from fractions import Fraction as _F
        def point_mass_metric():
            return _F(1), _F(1)
    """)
    rep = harness.run(d, mode="builder", lint=False)
    assert [l for l, ok, _ in rep["stages"]["graviton"]["blind"] if not ok] == \
        ["point-mass metric = 16 pi G Y P.tau (field equation and tpt agree)"]


def test_hidden_quoted_dependency_is_caught(tmp_path):
    # C2 of build 2026-11-a: 'derived' on top of a quoted export, without saying so
    d = _mutant(tmp_path, "links", """
        import inputs as _i
        import blackholes
        def planck_bh_kT_GeV():
            mpl = planck_mass_GeV(_i.G_NEWTON, _i.HBAR, _i.C_LIGHT)
            return _i.K_B * blackholes.hawking_K(mpl * 1e9 * _i.E_CH / _i.C_LIGHT**2) / _i.E_CH / 1e9
    """)
    rep = harness.run(d, mode="builder", lint=False)
    assert [l for l, ok, _ in rep["stages"]["links"]["contract"] if not ok] == \
        ["PROVENANCE[planck_bh_kT_GeV] names its quoted dependencies"]


# Stages running (one-loop 3-3-1 Landau poles) and weak (f_pi from G_F): each mutant is a plausible
# wrong implementation that must fail.
def test_wrong_field_content_needs_the_oracle(tmp_path):
    # b_X 10% low (a forgotten singlet, say): still exact, positive and growing with N_c, and the pole
    # is still where that b_X runs to 1, so every blind check passes
    d = _mutant(tmp_path, "running", """
        from fractions import Fraction as _F
        _b = b_331
        def b_331(Nc, variant):
            bX, bL = _b(Nc, variant)
            return bX * _F(9, 10), bL
    """)
    rep = harness.run(d, mode="verifier", lint=False)
    assert [l for l, ok, _ in rep["stages"]["running"]["blind"] if not ok] == []
    fails = [l for l, ok, _ in rep["stages"]["running"]["oracle"] if not ok]
    assert "+1/sqrt3: b_331 equals src's field content (N_c = 1, 3, 5, 7, 9, 11)" in fails
    assert "+1/sqrt3: one-loop pole, N_c = 3, equals src's one-loop running" in fails


def test_wrong_matching_is_caught_blind(tmp_path):
    # beta^2 = 1 in the matching instead of rung 1's photon coupling
    d = _mutant(tmp_path, "running", """
        def matching_331(mu, variant):
            aY, a2 = couplings_at(mu)
            return aY - a2, a2
    """)
    rep = harness.run(d, mode="builder", lint=False)
    assert "matching keeps g_L = g_2 and rung 1's photon coupling" in \
        [l for l, ok, _ in rep["stages"]["running"]["blind"] if not ok]


def test_missing_helicity_suppression_is_caught_blind(tmp_path):
    d = _mutant(tmp_path, "weak", """
        from math import pi as _pi
        def pion_decay_width(fpi, GF, Vud, m_l, m_pi):
            return GF**2 * Vud**2 * fpi**2 * m_pi**3 * (1 - m_l**2 / m_pi**2) ** 2 / (8 * _pi)
    """)
    rep = harness.run(d, mode="builder", lint=False)
    assert [l for l, ok, _ in rep["stages"]["weak"]["blind"] if not ok] == \
        [_FPI_ANCHOR, "helicity suppression and phase-space closure"]


_FPI_ANCHOR = "f_pi/sqrt2 within 2% of the lattice inputs.F_PI (convention and normalization)"


def test_wrong_width_normalization_is_caught_blind(tmp_path):
    # twice the width: every scaling law and the round trip still hold (f_pi is read off the same formula).
    # Before the P4 addendum only the oracle saw it; now f_pi misses the lattice value by 1/sqrt2.
    d = _mutant(tmp_path, "weak", """
        _w = pion_decay_width
        def pion_decay_width(*a):
            return 2 * _w(*a)
    """)
    rep = harness.run(d, mode="verifier", lint=False)
    assert [l for l, ok, _ in rep["stages"]["weak"]["blind"] if not ok] == [_FPI_ANCHOR]
    assert len([l for l, ok, _ in rep["stages"]["weak"]["oracle"] if not ok]) == 2


def test_pi0_with_the_input_fpi_is_caught(tmp_path):
    d = _mutant(tmp_path, "links", """
        import inputs as _i
        import gauge331 as _g
        import weak as _wk
        def pi0_width_from_rungs():
            _wk.fpi_from_pion_decay()                 # called, but its value thrown away for the input F_PI
            Qu, Qd = _g.quark_charges(3)
            return pi0_width_eV(_i.ALPHA_0, _i.F_PI, _i.M_PI0, 3, Qu, Qd)
    """)
    rep = harness.run(d, mode="builder", lint=False)
    assert [l for l, ok, _ in rep["stages"]["links"]["blind"] if not ok] == \
        ["pi0 width from rung 1's charges and stage weak's f_pi"]


def test_chpt_with_the_input_fpi_is_caught(tmp_path):
    d = _mutant(tmp_path, "chiral", """
        import inputs as _i
        import weak as _wk
        def chpt_mpi_from_rungs():
            _wk.fpi_from_pion_decay()                 # called, but the lattice input used instead
            return chpt_mpi(_i.M_UD_FLAG, _i.COND_13, _i.FPI_OVER_F, _i.LBAR3, _i.F_PI)
    """)
    rep = harness.run(d, mode="builder", lint=False)
    assert [l for l, ok, _ in rep["stages"]["chiral"]["blind"] if not ok] == ["O(p^4) pion mass with stage weak's f_pi"]


# ------------------------------------------------------------------------------------------
# P4 addendum (2026-11-14): mutants of stages weak and running, and of the derived-f_pi hand-off, that
# passed the builder gate (some of them every tier) before the checks named here were added.
ACCEPTED = [os.path.join(REBUILD, "builds", b) for b in ("2026-11-a", "2026-11-b")]


def _fails(rep, stage, tier):
    return [l for l, ok, _ in rep["stages"][stage].get(tier, []) if not ok]


def _moved(stage, label):
    assert label in harness.PERTURBED[stage][1]
    return f"with its inputs moved: {label}"


@pytest.mark.parametrize("build", ACCEPTED)
def test_accepted_builds_pass_the_addendum_checks(build):
    if not os.path.isdir(build):
        pytest.skip("build not present")
    rep = harness.run(build, mode="verifier")
    assert rep["ok"], harness.summarize(rep)
    for stage in harness.PERTURBED:
        assert len([1 for l, _, _ in rep["stages"][stage]["sensitivity"] if l.startswith("with its inputs moved")]) == \
            len(harness.PERTURBED[stage][1])


def test_fpi_in_the_92_MeV_convention_is_caught_blind(tmp_path):
    # the width written with F = f/sqrt2 (so 4 pi instead of 8 pi): fpi_from_pion_decay returns ~92 MeV
    d = _mutant(tmp_path, "weak", """
        _w = pion_decay_width
        def pion_decay_width(f, *a):
            return _w(f * 2 ** 0.5, *a)
    """)
    rep = harness.run(d, mode="builder", lint=False)
    assert _fails(rep, "weak", "blind") == [_FPI_ANCHOR]


def test_inputs_cached_or_typed_in_fpi_are_caught(tmp_path):
    # DELTA_PI typed as a Fraction (the lint sees two small integers and passes it on the accepted builds) and V_UD read at import: right at the
    # published inputs, so the round trip and the oracle passed
    d = _mutant(tmp_path, "weak", """
        import math as _m, inputs as _i
        from fractions import Fraction as _F
        _V = _i.V_UD
        def fpi_from_pion_decay():
            g = _i.GAMMA_PI_MUNU * _i.HBAR / (_i.E_CH * 1e9) / (1 + float(_F(176, 10000)))
            return _m.sqrt(g / pion_decay_width(1.0, _i.G_F, _V, _i.M_MU, _i.M_PIC))
    """)
    rep = harness.run(d, mode="verifier", lint=False)
    assert _fails(rep, "weak", "blind") == [] and _fails(rep, "weak", "oracle") == []
    assert _fails(rep, "weak", "sensitivity") == [_moved("weak", "f_pi reproduces the measured width")]


def test_width_wrong_outside_the_old_oracle_range_is_caught(tmp_path):
    # right for 0.07 < m_l/m_pi < 0.72 at m_pi = 0.14, the only region the oracle sampled
    d = _mutant(tmp_path, "weak", """
        _w = pion_decay_width
        def pion_decay_width(f, GF, Vud, ml, mp):
            return _w(f, GF, Vud, ml, mp) * (1.5 if 0.001 < ml / mp < 0.05 else 1)
    """)
    rep = harness.run(d, mode="verifier", lint=False)
    assert _fails(rep, "weak", "blind") == []
    assert len(_fails(rep, "weak", "oracle")) == 1


def test_bL_errors_are_caught_blind(tmp_path):
    # b_L with the adjoint Casimir of SU(2), and a b_L that depends on the variant: b_X untouched, so the
    # old blind checks (which never looked at b_L) passed both
    d = _mutant(tmp_path, "running", """
        from fractions import Fraction as _F
        _b = b_331
        def b_331(Nc, variant):
            bX, bL = _b(Nc, variant)
            return bX, bL + _F(11, 3)
    """)
    rep = harness.run(d, mode="builder", lint=False)
    assert _fails(rep, "running", "blind") == ["b_L(N_c = 3) and b_2 share their fermion sum (decoupling)"]
    d = _mutant(tmp_path / "v", "running", """
        from fractions import Fraction as _F
        _b = b_331
        def b_331(Nc, variant):
            bX, bL = _b(Nc, variant)
            return bX, bL + (_F(1, 6) if variant.startswith("+") else 0)
    """)
    rep = harness.run(d, mode="builder", lint=False)
    assert _fails(rep, "running", "blind") == ["b_L is the same in both variants",
                                               "b_L(N_c = 3) and b_2 share their fermion sum (decoupling)"]


def test_sm_without_the_higgs_is_caught_blind(tmp_path):
    d = _mutant(tmp_path, "running", """
        from fractions import Fraction as _F
        _sm = sm_coefficients
        def sm_coefficients():
            y, w = _sm()
            return y - _F(1, 6), w - _F(1, 6)
    """)
    rep = harness.run(d, mode="builder", lint=False)
    assert _fails(rep, "running", "blind") == ["b_L(N_c = 3) and b_2 share their fermion sum (decoupling)"]


def test_pole_tuned_to_the_tested_colours_is_caught(tmp_path):
    # a branch on an untested argument: N_c = 7 was probed by no tier
    d = _mutant(tmp_path, "running", """
        _lp = landau_pole
        def landau_pole(Nc, variant):
            return _lp(Nc, variant) * (2 if Nc == 7 else 1)
    """)
    rep = harness.run(d, mode="verifier", lint=False)
    assert _fails(rep, "running", "blind") == ["landau_pole is where the matched alpha_X runs to 1"]
    assert len(_fails(rep, "running", "oracle")) == 2


def test_bX_wrong_beyond_the_tested_colours_is_caught_by_the_oracle(tmp_path):
    d = _mutant(tmp_path, "running", """
        from fractions import Fraction as _F
        _b = b_331
        def b_331(Nc, variant):
            bX, bL = _b(Nc, variant)
            return (bX * _F(9, 10) if Nc >= 9 else bX), bL
    """)
    rep = harness.run(d, mode="verifier", lint=False)
    assert len(_fails(rep, "running", "oracle")) == 2


def test_pole_with_a_typed_scale_and_cached_MZ_are_caught(tmp_path):
    # the 3-3-1 scale typed as 4e3 in the pole's prefactor (one significant digit: the lint allows it; the
    # matching still reads MU_331, so the old sensitivity check saw the pole move), and M_Z read at import
    d = _mutant(tmp_path, "running", """
        import math as _m, inputs as _i
        def landau_pole(Nc, variant):
            a = matching_331(_i.MU_331, variant)[0]
            return 4e3 * _m.exp(2 * _m.pi * (a - 1) / float(b_331(Nc, variant)[0]))
    """)
    rep = harness.run(d, mode="verifier", lint=False)
    assert _fails(rep, "running", "blind") == [] and _fails(rep, "running", "oracle") == []
    assert _fails(rep, "running", "sensitivity") == [_moved("running", "landau_pole is where the matched alpha_X runs to 1")]
    d = _mutant(tmp_path / "mz", "running", """
        import math as _m, inputs as _i
        _MZ = _i.MZ_MEAS
        def couplings_at(mu):
            bY, b2 = sm_coefficients()
            t = _m.log(mu / _MZ) / (2 * _m.pi)
            return (1 - _i.S2_MZ) * _i.ALPHA_MZ_INV - float(bY) * t, _i.S2_MZ * _i.ALPHA_MZ_INV - float(b2) * t
    """)
    rep = harness.run(d, mode="verifier", lint=False)
    assert _fails(rep, "running", "blind") == [] and _fails(rep, "running", "oracle") == []
    assert _fails(rep, "running", "sensitivity") == \
        [_moved("running", "Standard Model running: SPEC's boundary and the b-slopes")]


def test_derived_fpi_cached_at_import_downstream_is_caught(tmp_path):
    # chiral keeps stage weak's f_pi from import time, and still calls weak (the spy is satisfied)
    d = _mutant(tmp_path, "chiral", """
        import inputs as _i
        import weak as _wk
        _F92 = _wk.fpi_from_pion_decay() / 2 ** 0.5
        def chpt_mpi_from_rungs():
            _wk.fpi_from_pion_decay()
            return chpt_mpi(_i.M_UD_FLAG, _i.COND_13, _i.FPI_OVER_F, _i.LBAR3, _F92)
    """)
    rep = harness.run(d, mode="verifier", lint=False)
    assert _fails(rep, "chiral", "blind") == [] and _fails(rep, "chiral", "oracle") == []
    assert _fails(rep, "chiral", "connections") == []
    assert _fails(rep, "chiral", "sensitivity") == [_moved("chiral", "O(p^4) pion mass with stage weak's f_pi")]


def test_links_hand_offs_with_cached_inputs_are_caught(tmp_path):
    d = _mutant(tmp_path, "links", """
        import inputs as _i
        import gauge331 as _g
        import running as _r
        import weak as _wk
        _AL, _GN = _i.ALPHA_0, _i.G_NEWTON
        _P = {v: (_r.landau_pole(3, v), _r.landau_pole(5, v)) for v in ("-1/sqrt3", "+1/sqrt3")}
        def pi0_width_from_rungs():
            Qu, Qd = _g.quark_charges(3)
            return pi0_width_eV(_AL, _wk.fpi_from_pion_decay() / 2 ** 0.5, _i.M_PI0, 3, Qu, Qd)
        def g_window_from_rungs(variant):
            _r.landau_pole(3, variant)
            return g_window(*_P[variant], planck_mass_GeV(_GN, _i.HBAR, _i.C_LIGHT))
    """)
    rep = harness.run(d, mode="verifier", lint=False)
    assert _fails(rep, "links", "blind") == [] and _fails(rep, "links", "oracle") == []
    assert _fails(rep, "links", "connections") == []
    assert _fails(rep, "links", "sensitivity") == [_moved("links", "pi0 width from rung 1's charges and stage weak's f_pi"),
                                                   _moved("links", "G window from the one-loop poles of stage running")]


def test_window_from_the_quoted_poles_is_caught(tmp_path):
    # g_window_from_rungs calls running.landau_pole (the spy is satisfied) and returns the three-loop window
    d = _mutant(tmp_path, "links", """
        import inputs as _i
        import running as _r
        def g_window_from_rungs(variant):
            _r.landau_pole(3, variant); _r.landau_pole(5, variant)
            q3, q5 = _i.POLES_331[variant]
            return g_window(q3, q5, planck_mass_GeV(_i.G_NEWTON, _i.HBAR, _i.C_LIGHT))
    """)
    rep = harness.run(d, mode="verifier", lint=False)
    assert _fails(rep, "links", "connections") == []
    assert _fails(rep, "links", "blind") == ["G window from the one-loop poles of stage running"]
    assert len(_fails(rep, "links", "oracle")) == 2


def test_report_json_has_real_booleans(tmp_path):
    # the oracle compares with numpy floats; a numpy.bool_ was written to the report as the string "False"
    import json
    d = _mutant(tmp_path, "links", """
        import inputs as _i
        def g_window_from_rungs(variant):
            q3, q5 = _i.POLES_331[variant]
            return g_window(q3, q5, planck_mass_GeV(_i.G_NEWTON, _i.HBAR, _i.C_LIGHT))
    """)
    rep = json.loads(json.dumps(harness.run(d, mode="verifier", lint=False), default=str))
    for rec in rep["stages"].values():
        for tier in ("contract", "blind", "sensitivity", "connections", "oracle"):
            assert all(isinstance(ok, bool) for _, ok, _ in rec.get(tier, []))
