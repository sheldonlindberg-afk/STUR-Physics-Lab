"""Pins tools/dependency_map.py and DEPENDENCIES.md: the page is current, every script has a
topic, and no copied value differs from its source without a stated reason."""
import os, sys
ROOT = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, os.path.join(ROOT, "tools"))
import dependency_map as D

BUILT = D.build()


def test_every_script_has_a_topic():
    info, vals, rows, missing, stale = BUILT
    assert not missing and not stale, (missing, stale)


def test_no_copy_drifts_from_its_source():
    info, vals, rows, missing, stale = BUILT
    drift = [(k, o["module"], o["line"], o["value"]) for k, r in rows.items() for o in r if o["status"] == "DRIFT"]
    assert not drift, drift


def test_derived_values_match_their_sources():
    info, vals, rows, missing, stale = BUILT
    assert abs(vals["M_Pl"] / 1.22089e19 - 1) < 1e-5            # sqrt(hbar c / G) = the 3-3-1 cutoff
    assert abs(vals["v"] - 246.22) < 0.01
    assert abs(vals["MZp_MV"] - 1.225) < 1e-3 and abs(vals["s2TeV"] - 0.2504) < 1e-4
    assert abs(vals["A_m"] / 1.4678e-14 - 1) < 1e-4 and abs(vals["A_dphi"] - 2.1868) < 1e-4
    assert vals["c_s"] == 0.3046


def test_every_catalogued_quantity_is_found():
    info, vals, rows, missing, stale = BUILT
    unused = [k for k, r in rows.items() if not r]
    assert not unused, unused


def test_page_is_current():
    text = D.report(*BUILT)
    assert open(D.OUT, encoding="utf8").read() == text, "run python3 tools/dependency_map.py"
