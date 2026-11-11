"""Pins src/stur_recheck.py: every failed claim reconfirmed by independent code."""
import io, os, sys, contextlib
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import stur_recheck as X


def test_all_failures_reconfirmed_and_output_matches():
    X.RESULTS.clear()
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        res = X.main()
    assert len(res) == 15 and all(ok for _, ok, _ in res), [k for k, ok, _ in res if not ok]
    ref = open(os.path.join(os.path.dirname(__file__), "..", "results", "recheck", "output.txt")).read()
    assert buf.getvalue() == ref
