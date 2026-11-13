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
    assert fails == ["pi0 width 7.785 eV", "pi0 width from rung 1's charges 7.785 eV"]


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
    assert harness.run(d, mode="builder", lint=False)["ok"]
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
