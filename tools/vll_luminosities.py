#!/usr/bin/env python3
"""q-qbar parton luminosities dL/dtau at sqrt(s) = 13 TeV for continuum Drell-Yan pair
production (src/m331_heavy_lepton.py), on a log grid of sqrt(s_hat) from 150 GeV to 7 TeV:

    dL_q/dtau = int_tau^1 dx/x [f_q(x) f_qbar(tau/x) + f_qbar(x) f_q(tau/x)],  mu_F = sqrt(s_hat)

for q = d, u, s, c, b, with the LHAPDF grids that ship with Pythia 8 (NNPDF3.1 NNLO luxQED
and PDF4LHC21, central members), read through pythia8mc.LHAGrid1, as in
tools/parton_luminosities.py.

Writes results/m331/vll/lumi_dy_13TeV.json. Needs pythia8mc; not needed to run the module.
"""
import json, os
import numpy as np
import pythia8mc

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
OUT = os.path.join(ROOT, "results", "m331", "vll", "lumi_dy_13TeV.json")
PDFDIR = "/usr/local/share/Pythia8/pdfdata/"
SETS = ["NNPDF31_nnlo_as_0118_luxqed_0000.dat", "PDF4LHC21_mc_0000.dat"]
SQRTS = 13000.0
MHAT = np.exp(np.linspace(np.log(150.0), np.log(7000.0), 97))
FLAV = {"d": 1, "u": 2, "s": 3, "c": 4, "b": 5}


def lumi(pdf, q, M, n=1500):
    tau = (M / SQRTS) ** 2
    lx = np.linspace(np.log(tau), 0.0, n)
    x = np.exp(lx)
    Q2 = M * M
    xq = np.array([pdf.xf(q, v, Q2) for v in x]); xqb = np.array([pdf.xf(-q, v, Q2) for v in x])
    xq2 = np.array([pdf.xf(q, tau / v, Q2) for v in x]); xqb2 = np.array([pdf.xf(-q, tau / v, Q2) for v in x])
    return float(np.trapezoid((xq * xqb2 + xqb * xq2) / tau, lx))


def main():
    out = {"sqrt_s_GeV": SQRTS, "scale": "mu_F = sqrt(s_hat)", "mhat_GeV": MHAT.tolist(), "sets": {}}
    for s in SETS:
        pdf = pythia8mc.LHAGrid1(2212, s, PDFDIR)
        out["sets"][s] = {k: [lumi(pdf, q, M) for M in MHAT] for k, q in FLAV.items()}
        print(s, "done")
    json.dump(out, open(OUT, "w"))
    print("wrote", OUT)


if __name__ == "__main__":
    main()
