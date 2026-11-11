#!/usr/bin/env python3
"""Independent cross-check of the Z' recast with Pythia 8's own Z' process.

Pythia's NewGaugeBoson:ffbar2gmZZprime (gmZmode = 3: Z' alone, no gamma/Z interference) with
its default PDF (NNPDF2.3 QCD+QED LO), its own width calculation and full Breit-Wigner, at
sqrt(s) = 13 TeV. Shares nothing with src/m331_zprime_recast.py except the Z' couplings.

Pythia's couplings: L = (g / 4 c_W) fbar gamma^mu (v - a gamma5) f Z'_mu, so in units of g/c_W
    v = 2 (g_L + g_R),   a = 2 (g_L - g_R)   (SM Z: v_d = -0.693, a_d = -1).

For each model and mass, sigma(pp -> Z' -> e+ e-) is computed; its ratio to Z'_SSM times the
ATLAS SSM prediction, against the HEPData limit, gives the mass limit independently.

Usage:  python3 tools/pythia_crosscheck.py      (needs pythia8mc; about a minute)
Writes: results/m331/zprime/pythia_crosscheck.json
"""
import json, os, sys
from math import sqrt
import pythia8mc

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, os.path.join(ROOT, "src"))
import m331_zprime_recast as Z

OUT = os.path.join(ROOT, "results", "m331", "zprime", "pythia_crosscheck.json")
MASSES = [4000.0, 4500.0, 5000.0, 5500.0]
NAMES = {0: {"d": "d", "u": "u", "e": "e", "nu": "nue"},
         1: {"d": "s", "u": "c", "e": "mu", "nu": "numu"},
         2: {"d": "b", "u": "t", "e": "tau", "nu": "nutau"}}


def sigma(gens, M, n=20000):
    py = pythia8mc.Pythia("", False)
    for line in ("Beams:eCM = 13000.", "NewGaugeBoson:ffbar2gmZZprime = on", "Zprime:gmZmode = 3",
                 "Zprime:universality = off", "Zprime:coup2WW = 0.", f"32:m0 = {M}",
                 f"32:mMin = {0.5 * M}", f"32:mMax = {1.5 * M}", "32:onMode = off", "32:onIfAny = 11",
                 "PartonLevel:all = off", "HadronLevel:all = off", "ProcessLevel:resonanceDecays = on",
                 "Next:numberCount = 0", "Random:setSeed = on", "Random:seed = 12345"):
        py.readString(line)
    for g, names in NAMES.items():
        for f, pn in names.items():
            c = gens[g][f if f != "nu" else "nu"]
            gl, gr = c["L"], c.get("R", 0.0)
            py.readString(f"Zprime:v{pn} = {2 * (gl + gr)}")
            py.readString(f"Zprime:a{pn} = {2 * (gl - gr)}")
    py.init()
    for _ in range(n):
        py.next()
    return py.infoPython().sigmaGen() * 1e12, py.infoPython().sigmaErr() * 1e12, \
        py.particleData.mWidth(32) / M          # fb, fb, Gamma/M


def main():
    s2 = Z.S2_SSM          # Pythia's own normalisation of g / c_W; same scheme for every model
    models = {"SSM": Z.model_couplings("SSM", s2=s2),
              "331+A": Z.model_couplings("331", beta=1 / sqrt(3), first_gen_rep="3b", s2=s2),
              "331+B": Z.model_couplings("331", beta=1 / sqrt(3), first_gen_rep="3", s2=s2),
              "331-A": Z.model_couplings("331", beta=-1 / sqrt(3), first_gen_rep="3b", s2=s2)}
    out = {"s2": s2, "masses": MASSES, "models": {}}
    for name, gens in models.items():
        out["models"][name] = [sigma(gens, M) for M in MASSES]
        print(name, [(round(a, 4), round(c * 100, 2)) for a, b, c in out["models"][name]])
    json.dump(out, open(OUT, "w"), indent=1)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
