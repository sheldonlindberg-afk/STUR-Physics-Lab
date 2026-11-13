"""Pins src/force_chain.py: the forces in one chain, each stage using earlier stages' outputs."""
import contextlib, io, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import force_chain as FC

ROOT = os.path.join(os.path.dirname(__file__), "..")
_OUT = io.StringIO()
with contextlib.redirect_stdout(_OUT):
    LEDGER, INPUTS = FC.run()
LEDGER = [list(r) for r in LEDGER]
VALUES = {name: value for name, value, _, _ in LEDGER}


def test_every_stage_after_the_first_uses_an_earlier_stage():
    n = len(FC.STAGES)
    for st in range(2, n + 1):
        sources = {made for _, _, made, used in LEDGER if st in used}
        assert sources and min(sources) < st, st
    for _, _, made, used in LEDGER:
        assert all(u > made for u in used)


def test_each_stage_hands_something_on_or_is_final():
    final = {"pi0 width", "m_pi O(p^4)", "neutrality needed", "end temperature", "Sgr A* T_H"}
    for name, _, made, used in LEDGER:
        assert used or name in final, name


def test_the_numbers_the_stages_pass():
    assert abs(VALUES["M_Pl"] / 1.22089e19 - 1) < 1e-5
    assert abs(1 / VALUES["alpha(0)"] - 137.035999) < 1e-5
    assert abs(VALUES["f_pi"] * 1e3 - 130.57) < 0.01
    assert abs(VALUES["pi0 width"] - 7.742) < 2e-3
    assert abs(VALUES["neutrality needed"] / 2.82e-19 - 1) < 3e-3
    assert abs(VALUES["phase"] - 2.1868) < 1e-3
    assert abs(VALUES["end temperature"] / (VALUES["M_Pl"] / (8 * 3.141592653589793)) - 1) < 1e-6


def test_measured_inputs_are_declared_where_they_enter():
    names = {name for _, name, _, _ in INPUTS}
    for n in ("G", "1/alpha-hat(M_Z)", "G_F", "Delta alpha_had", "Gamma(pi -> mu nu)", "Lambda",
              "diamond permittivity", "M_V floor", "cryostat T"):
        assert n in names, n


def test_no_rung_vocabulary_and_reference_output():
    out = _OUT.getvalue()
    full = io.StringIO()
    with contextlib.redirect_stdout(full):
        FC.main()
    text = full.getvalue()
    assert "rung" not in text.lower() and "link 3" not in text.lower()
    assert text == open(os.path.join(ROOT, "results", "force_chain.txt")).read()
