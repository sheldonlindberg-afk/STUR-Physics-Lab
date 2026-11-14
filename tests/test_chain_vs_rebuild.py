"""The force chain (src/force_chain.py) against every accepted rebuild of the ladder.

Where the two overlap, the build's export called with the chain's own arguments must agree to
rounding, and the build's own headline value must agree with the chain's or differ only for a
recorded cause inside its recorded band (rebuild/chain_compare.py, KNOWN). A change on either
side, src/ or an accepted build, shows up here.
"""
import os
import shutil
import sys
import textwrap

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REBUILD = os.path.join(ROOT, "rebuild")
sys.path.insert(0, REBUILD)

import chain_compare  # noqa: E402

ACCEPTED = sorted(d for d in os.listdir(os.path.join(REBUILD, "builds"))
                  if os.path.exists(os.path.join(REBUILD, "builds", d, "ACCEPTED.md")))


@pytest.fixture(scope="module")
def chain():
    return chain_compare.chain_values()


@pytest.mark.parametrize("build_id", ACCEPTED)
def test_chain_and_accepted_build_agree(chain, build_id):
    rows = chain_compare.compare(os.path.join(REBUILD, "builds", build_id), chain)
    assert all(ok for *_, ok, _ in rows), chain_compare.summarize(rows)


def test_every_known_difference_is_used(chain):
    # a KNOWN entry no comparison uses would silently excuse nothing; keep the table honest
    rows = chain_compare.compare(os.path.join(REBUILD, "builds", ACCEPTED[-1]), chain)
    labels = {r[0] for r in rows}
    assert set(chain_compare.KNOWN) <= labels, set(chain_compare.KNOWN) - labels


def test_a_wrong_build_is_caught(chain, tmp_path):
    # the pi0 width a factor 2 off: the same-arguments comparison must fail, and nothing else
    src = os.path.join(REBUILD, "builds", ACCEPTED[-1])
    d = tmp_path / "mutant"
    shutil.copytree(src, d)
    with open(d / "links.py", "a") as fh:
        fh.write("\n" + textwrap.dedent("""
            _w = pi0_width_eV
            def pi0_width_eV(*a):
                return 2 * _w(*a)
        """))
    rows = chain_compare.compare(str(d), chain)
    fails = [r[0] for r in rows if not r[5]]
    assert fails == ["pi0 width with the chain's alpha(0), f_pi and charges",
                     "pi0 width: chain vs the build's pi0_width_from_rungs"], fails


def test_chain_compare_never_enters_a_clean_room():
    import cleanroom
    assert "chain_compare.py" in cleanroom.FORBIDDEN_IN_ROOM
    assert "chain_compare.py" not in cleanroom.ALLOWED
