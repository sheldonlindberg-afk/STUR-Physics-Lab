"""The force chain on its two back ends: src/ and every accepted blind rebuild of the ladder.

src/force_chain.py run(build=<dir>) takes each hand-off the build derives from the build, called with
the chain's own earlier hand-offs. Both back ends must give the same chain: the same values handed
between the same stages, equal to rounding except where a cause is recorded in BANDS.
"""
import contextlib
import io
import os
import sys

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REBUILD = os.path.join(ROOT, "rebuild")
sys.path.insert(0, os.path.join(ROOT, "src"))

import force_chain as FC  # noqa: E402

BUILDS = sorted(d for d in os.listdir(os.path.join(REBUILD, "builds"))
                if os.path.exists(os.path.join(REBUILD, "builds", d, "ACCEPTED.md")))

# hand-off -> (lowest, highest relative difference build vs src, cause). Anything not listed: <= 1e-12.
BANDS = {
    "alpha(0)": (9e-8, 1.3e-7, "src takes the leptons' three-loop Delta alpha from the literature; the build computes"
                               " the one-loop part itself (today's masses and M_Z) and adds the quoted higher loops"),
    "pi0 width": (1.8e-7, 2.6e-7, "alpha(0) squared, from the row above"),
    "f_pi": (0.0, 1e-9, "hbar in GeV s: the build forms HBAR/E_CH, src types the constant"),
    "m_pi O(p^4)": (0.0, 1e-9, "f_pi, from the row above"),
    "neutrality needed": (4e-8, 7e-8, "alpha(0) to the power -1/2, from the first row"),
    "gap": (2.9e-4, 3.0e-4, "src returns the first point of a 4000-point grid above the root; the build bisects"
                            " to the root (rebuild FINDINGS N3)"),
    "phase": (4.4e-4, 4.6e-4, "the gap, from the row above"),
    "Sgr A* T_H": (0.0, 1e-12, "Lambda's shift, 2e-32, is below double precision"),
    "end temperature": (0.0, 1e-9, "the Planck mass through the build's Hawking formula"),
}


def _run(build=None):
    with contextlib.redirect_stdout(io.StringIO()):
        ledger, inputs = FC.run(build)
    return [(n, v, made, tuple(used)) for n, v, made, used in ledger], [(st, n) for st, n, _, _ in inputs]


@pytest.fixture(scope="module")
def on_src():
    return _run()


def _rel(a, b):
    return abs(a - b) / abs(b)


@pytest.mark.parametrize("build_id", BUILDS)
def test_both_back_ends_give_the_same_chain(on_src, build_id):
    led_s, in_s = on_src
    led_b, in_b = _run(os.path.join(REBUILD, "builds", build_id))
    assert [(n, made, used) for n, _, made, used in led_b] == [(n, made, used) for n, _, made, used in led_s]
    assert in_b == in_s                                   # the same measured inputs enter at the same stages
    bad = []
    for (name, vs, _, _), (_, vb, _, _) in zip(led_s, led_b):
        if isinstance(vs, (int, float)) and not isinstance(vs, bool) and vs != 0:
            lo, hi, _ = BANDS.get(name, (0.0, 1e-12, ""))
            if not lo <= _rel(float(vb), float(vs)) <= hi:
                bad.append((name, vs, vb, _rel(float(vb), float(vs)), (lo, hi)))
        elif vs != vb:
            bad.append((name, vs, vb))
    assert not bad, bad


def test_every_band_names_a_hand_off(on_src):
    assert set(BANDS) <= {n for n, *_ in on_src[0]}


def test_the_src_back_end_is_left_as_it_was(on_src):
    # after a build run the switch is off again, and the default run reproduces the published output
    if BUILDS:
        _run(os.path.join(REBUILD, "builds", BUILDS[0]))
    assert FC.BUILD is None
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        FC.main()
    assert out.getvalue() == open(os.path.join(ROOT, "results", "force_chain.txt")).read()


def test_a_wrong_build_changes_the_chain(on_src, tmp_path):
    # a build whose Planck mass is 1% off: the hand-off M_Pl, and nothing upstream of it, moves
    import shutil
    import textwrap
    if not BUILDS:
        pytest.skip("no accepted build")
    d = tmp_path / "mutant"
    shutil.copytree(os.path.join(REBUILD, "builds", BUILDS[-1]), d)
    with open(d / "links.py", "a") as fh:
        fh.write("\n" + textwrap.dedent("""
            _pm = planck_mass_GeV
            def planck_mass_GeV(G, hbar, c):
                return 1.01 * _pm(G, hbar, c)
        """))
    led_b, _ = _run(str(d))
    vs = {n: v for n, v, *_ in on_src[0]}
    vb = {n: v for n, v, *_ in led_b}
    assert abs(vb["M_Pl"] / vs["M_Pl"] - 1.01) < 1e-9
    assert abs(vb["end temperature"] / vs["end temperature"] - 1) > 5e-3
    assert vb["G"] == vs["G"] and vb["Q_u"] == vs["Q_u"]
