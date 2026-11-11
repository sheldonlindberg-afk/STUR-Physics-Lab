"""Holds the current documents to the computations and to each other.

Fails if a superseded claim returns, if a number shared between documents drifts
from the script that computes it, if a document link breaks, or if the stated test
count goes stale. The archive is not checked.
"""
import glob, os, re, sys
ROOT = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, os.path.join(ROOT, "src"))

CURRENT = ["README.md", "DERIVATION.md", "PREDICTIONS.md", "COLLECTIVE.md", "OPPENHEIM.md",
           "EMERGENT.md", "GRAVITY_ENTANGLEMENT.md", "TEGR.md", "MEASUREMENT.md", "BORN.md",
           "WALL.md", "NOTE_331.md", "REPORT.md", "CONSISTENCY.md", "RECHECK.md", "NOVELTY.md", "index.html", "technical.html", "llms.txt", "CITATION.cff"]


def read(name):
    return open(os.path.join(ROOT, name), encoding="utf8").read()


def test_point_nucleus_heating_only_quoted_as_superseded():
    pat = re.compile(r"10⁶⁰|10⁵⁶|1e60|1e56|10<sup>60|10<sup>56")
    qualifiers = ("point", "earlier", "artefact", "old ", "it gave", "0.51 W/kg")
    bad = [(n, l.strip()[:90]) for n in CURRENT for l in read(n).splitlines()
           if pat.search(l) and not any(q in l for q in qualifiers)]
    assert not bad, bad


def test_d6_is_never_presented_as_unconditional():
    forbidden = ["derived, not assumed", "| FOLLOWS + analog |", "FOLLOWS under R₀ = a",
                 'tag ok">derived</span><span class="c">A statistical',
                 "and it now follows from D1–D3 instead of being added to them"]
    hits = [(n, f) for n in CURRENT for f in forbidden if f in read(n)]
    assert not hits, hits
    assert "CONDITIONAL" in read("DERIVATION.md") and "CONDITIONAL" in read("REPORT.md")
    for n in ("README.md", "DERIVATION.md", "PREDICTIONS.md", "COLLECTIVE.md", "OPPENHEIM.md"):
        assert re.search(r"perturbative\s+(\(effective-field-theory\)\s+)?quantum\s+gravity", read(n), re.I), n


def test_gravity_bounds_never_claimed_as_new():
    """NOVELTY.md §3: P2-P5 are worked examples within existing literature."""
    forbidden = ["The new result there is a shape-free", "shape-free bound (STUR)"]
    hits = [(n, f) for n in CURRENT for f in forbidden if f in read(n)]
    assert not hits, hits
    assert "not new" in read("OPPENHEIM.md")
    assert "not a new result" in read("REPORT.md") and "not new results" in read("llms.txt")


def test_shared_numbers_match_their_computation():
    import stur_oppenheim as O, stur_thermo_gravity as T
    h = T.heating_per_kg_nuclei(T.cutoff(1))
    assert f"{h:.1f}" == "0.5" and f"{h / T.EARTH_W_PER_KG:.0e}" == "6e+10"
    for n in ("README.md", "DERIVATION.md", "PREDICTIONS.md", "COLLECTIVE.md", "EMERGENT.md"):
        assert ("0.5 W" in read(n) or "0.51 W" in read(n)) and "6×10¹⁰" in read(n), n
    B = O.joint_bound(O.D_A)
    assert f"{(2 * B / O.GAMMA_BUDGET) ** 0.5:.1e}" == "1.3e-12"
    for n in ("README.md", "PREDICTIONS.md", "OPPENHEIM.md"):
        assert "1.3×10⁻¹²" in read(n), n
    import stur_gravity_full as Fg
    assert round(Fg.LPF_ASD / O.ASD_REQ) in (56, 57)               # LISA Pathfinder vs requirement
    for n in ("README.md", "PREDICTIONS.md", "GRAVITY_ENTANGLEMENT.md", "WALL.md"):
        assert "57" in read(n), n
    assert Fg.GAS_MODEL == "kinetic"                                   # derived, not interpolated
    full = read("results/gravity_entanglement/full_output.txt")
    dphi = float(re.search(r"dphi = (\d+\.\d+) rad", full).group(1))
    assert "565 -> 270 runs" in full and f"{dphi:.2f}" == "1.51"
    for n in ("README.md", "DERIVATION.md", "PREDICTIONS.md", "index.html", "technical.html"):
        assert "270 runs" in read(n) or "270 (0.6 h)" in read(n), n
        assert "2.19" in read(n), n
    yuk = read("results/unifying_search/331_yukawa.txt")
    assert "0.2663" in yuk and "0.0662 < s^2 < 0.0742" in yuk
    assert "0.266" in read("NOTE_331.md") and "0.066" in read("NOTE_331.md")


def test_document_links_resolve():
    missing = []
    for n in CURRENT:
        for target in re.findall(r"\]\(([A-Za-z0-9_\-./]+\.(?:md|pdf))(?:#[^)]*)?\)", read(n)):
            if not os.path.exists(os.path.join(ROOT, target)):
                missing.append((n, target))
    assert not missing, missing


def test_stated_test_count_is_current():
    count = sum(len(re.findall(r"^def test_", open(f).read(), re.M))
                for f in glob.glob(os.path.join(ROOT, "tests", "test_*.py")))
    for n in ("README.md", "REPORT.md"):
        stated = {int(x) for x in re.findall(r"\((\d+) tests", read(n))}
        assert stated == {count}, (n, stated, count)
