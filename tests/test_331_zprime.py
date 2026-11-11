"""Pins src/m331_zprime_recast.py: the ATLAS 139 fb^-1 dilepton recast for the beta = +-1/sqrt3 Z'."""
import os, sys
from math import sqrt
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import m331_zprime_recast as Z


def test_couplings_match_known_forms():
    s2 = 0.23
    gv = (Z.g331(Z.t8("3"), -0.5, -1 / sqrt(3), s2) + Z.g331(0, -1, -1 / sqrt(3), s2)) / 2
    assert abs(gv - (1 - 4 * s2) / (4 * sqrt(3 - 4 * s2))) < 1e-12


def test_benchmark_widths_match_atlas():
    for model, w in (("SSM", 3.0), ("psi", 0.5), ("chi", 1.2)):
        g, *_ = Z.widths(Z.model_couplings(model, s2=Z.S2_SSM), Z.S2_SSM)
        assert abs(100 * g - w) / w < 0.1, model


def test_digitised_curves_match_quoted_values():
    assert abs(Z.curve("obs_0.0", 6000.0) / 0.014 - 1) < 0.06
    assert abs(Z.curve("obs_10.0", 250.0) / 13.1 - 1) < 0.03
    assert abs(Z.mass_limit(lambda M: Z.curve("model_SSM", M), 3.0) - 5100) < 50


def test_method_reproduces_psi_and_chi_limits():
    for model, m in (("psi", 4500), ("chi", 4800)):
        lim, *_ = Z.recast(Z.model_couplings(model, s2=Z.S2_SSM), Z.S2_SSM, pdfset="PDF4LHC21")
        assert abs(lim - m) < 60, (model, lim)


def test_beta_plus_limits():
    gens = Z.model_couplings("331", beta=1 / sqrt(3), first_gen_rep="3b", s2=Z.S2_TEV)
    lo, width, br, _ = Z.recast(gens, Z.S2_TEV)
    assert 5150 < lo < 5250 and abs(width - 1.68) < 0.02
    lo_ex, *_ = Z.recast(gens, Z.S2_TEV, Z.exotic_couplings(1 / sqrt(3), Z.S2_TEV))
    assert 4850 < lo_ex < 4950
    out = open(os.path.join(os.path.dirname(__file__), "..", "results", "m331", "zprime_recast.txt")).read()
    assert "beta = +1/sqrt3: M_Z' > 5.0-5.2 TeV (SM decays only); > 4.7-4.9 TeV" in out or \
           "beta = +1/sqrt3: M_Z' > 5.0-5.2 TeV (SM decays only); > 4.6-4.9 TeV" in out


def test_hepdata_inputs_and_digitisation():
    assert abs(Z.curve("obs_0.0", 250.0) - 3.573) < 0.01            # HEPData t4, zero width
    assert abs(Z.DIG_OFFSET - 1) < 0.04                             # digitisation within 4%


def test_omissions_are_small():
    gens = Z.model_couplings("331", beta=1 / sqrt(3), first_gen_rep="3b", s2=Z.S2_TEV)
    ex = tuple(Z.exotic_couplings(1 / sqrt(3), Z.S2_TEV)) + tuple(Z.scalar_couplings(1 / sqrt(3), Z.S2_TEV))
    lo, width, *_ = Z.recast(gens, Z.S2_TEV, ex)
    assert 4780 < lo < 4880 and width < 4.0                        # every scalar open too
    g, *_ = Z.widths(Z.model_couplings("331", beta=1 / sqrt(3), s2=Z.S2_SSM), Z.S2_SSM)
    r = Z.lineshape(Z.model_couplings("331", beta=1 / sqrt(3), s2=Z.S2_SSM), 5000.0, g)
    assert abs(r[0.10]) < 0.05                                     # interference within +-10% M


def test_pythia_reproduction():
    for name, (lp, lm) in Z.Z8_pythia().items():
        assert abs(lp - lm) < 60, name
