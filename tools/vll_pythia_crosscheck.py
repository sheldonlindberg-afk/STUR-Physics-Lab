#!/usr/bin/env python3
"""Independent check of the pair cross section in src/m331_heavy_lepton.py with Pythia 8.

Pythia's NewGaugeBoson:ffbar2gmZZprime with Zprime:gmZmode = 0 gives q qbar -> gamma*/Z/Z' ->
F Fbar with full interference. F is Pythia's fourth-generation tau' (id 17), which couples to
the Z as an SU(2) doublet member; its Z' couplings and those of every quark are set to the
3-3-1 (beta = +1/sqrt3) values of src/m331_zprime_recast.py. The module's own code is run in
the same 'doublet' mode, with the same PDF (NNPDF3.1 luxQED), alpha_em(M_Z), sin^2 theta_W,
Z and Z' widths, and compared. Zprime:universality must be off: with it on (the default)
Pythia copies the first-generation couplings to the b quark and the electron's to the tau'.

Writes results/m331/vll/pythia_crosscheck.json. Needs pythia8mc; not needed to run the module.
"""
import json, os, sys
import pythia8mc

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, os.path.join(ROOT, "src"))
import m331_heavy_lepton as H

OUT = os.path.join(ROOT, "results", "m331", "vll", "pythia_crosscheck.json")
POINTS = [(200.0, 4600.0), (400.0, 4600.0), (800.0, 4600.0), (400.0, 1500.0), (600.0, 1500.0)]
NEV = 20000


def run(mF, MZp):
    p = pythia8mc.Pythia("", False)
    cf = H.pythia_couplings()
    for s in ["Beams:eCM = 13000", "NewGaugeBoson:ffbar2gmZZprime = on", "Zprime:gmZmode = 0",
              "Zprime:coup2gen4 = on", "Zprime:universality = off", f"17:m0 = {mF}", f"32:m0 = {MZp}", "32:onMode = off",
              "32:onIfAny = 17", f"PhaseSpace:mHatMin = {2 * mF + 0.1}", "PhaseSpace:mHatMax = 13000",
              "PDF:pSet = LHAGrid1:NNPDF31_nnlo_as_0118_luxqed_0000.dat", "SigmaProcess:alphaEMorder = -1",
              f"StandardModel:sin2thetaW = {H.S2_MZ}", f"StandardModel:sin2thetaWbar = {H.S2_MZ}",
              "PartonLevel:all = off", "HadronLevel:all = off", "ProcessLevel:resonanceDecays = off", "Next:numberShowEvent = 0", "Next:numberShowInfo = 0", "Next:numberShowProcess = 0",
              "Next:numberCount = 0", "Random:setSeed = on", "Random:seed = 7"] + cf:
        p.readString(s)
    p.init()
    for _ in range(NEV):
        p.next()
    return (p.infoPython().sigmaGen() * 1e12, p.infoPython().sigmaErr() * 1e12,   # mb -> fb
            p.particleData.mWidth(23), p.particleData.mWidth(32))


def main():
    rows = []
    for mF, MZp in POINTS:
        sig, err, gZ, gZp = run(mF, MZp)
        mine = H.sigma_pair(mF, MZp=MZp, mode="doublet", widths=(gZ, gZp), aem=H.AEM_MZ)
        rows.append(dict(mF=mF, MZp=MZp, pythia_fb=sig, pythia_err_fb=err, module_fb=mine, GammaZ=gZ, GammaZp=gZp))
        print(f"m_F = {mF:5.0f}  M_Z' = {MZp:5.0f}: Pythia {sig:.4g} +- {err:.2g} fb, module {mine:.4g} fb,"
              f" ratio {mine / sig:.4f}  (Gamma_Z' = {gZp:.1f} GeV)")
    json.dump(rows, open(OUT, "w"), indent=1)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
