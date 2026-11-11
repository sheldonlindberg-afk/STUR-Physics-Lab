#!/usr/bin/env python3
"""q-qbar parton luminosities for Drell-Yan production of a heavy resonance at sqrt(s) = 13 TeV.

    L_q(tau) = int_tau^1 dx/x [f_q(x) f_qbar(tau/x) + f_qbar(x) f_q(tau/x)],  tau = M^2/s,  mu = M

for q = d, u, s, c, b, evaluated with the LHAPDF grids that ship with Pythia 8
(NNPDF3.1 NNLO luxQED and PDF4LHC21, central members), read through pythia8mc.LHAGrid1.

Usage:  python3 tools/parton_luminosities.py
Writes: results/m331/zprime/lumi_13TeV.json
Needs:  pythia8mc (pip install pythia8mc). Not needed to run the recast itself.
"""
import json, os
import numpy as np
import pythia8mc

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
OUT = os.path.join(ROOT, "results", "m331", "zprime", "lumi_13TeV.json")
PDFDIR = "/usr/local/share/Pythia8/pdfdata/"
SETS = ["NNPDF31_nnlo_as_0118_luxqed_0000.dat", "PDF4LHC21_mc_0000.dat"]
SQRTS = 13000.0
MASSES = np.arange(1500.0, 6501.0, 50.0)
FLAV = {"d": 1, "u": 2, "s": 3, "c": 4, "b": 5}


def lumi(pdf, q, M, n=4000):
    tau = (M / SQRTS) ** 2
    lx = np.linspace(np.log(tau), 0.0, n)
    x = np.exp(lx)
    Q2 = M * M
    xq = np.array([pdf.xf(q, v, Q2) for v in x]); xqb = np.array([pdf.xf(-q, v, Q2) for v in x])
    xq2 = np.array([pdf.xf(q, tau / v, Q2) for v in x]); xqb2 = np.array([pdf.xf(-q, tau / v, Q2) for v in x])
    # f(x) f(tau/x) = xf(x) xf(tau/x) / tau ; dx/x = d ln x
    integrand = (xq * xqb2 + xqb * xq2) / tau
    return float(np.trapezoid(integrand, lx))


def main():
    out = {"sqrt_s_GeV": SQRTS, "scale": "mu_F = M", "masses_GeV": MASSES.tolist(), "sets": {}}
    for s in SETS:
        pdf = pythia8mc.LHAGrid1(2212, s, PDFDIR)
        out["sets"][s] = {k: [lumi(pdf, q, M) for M in MASSES] for k, q in FLAV.items()}
        print(s, "u/d at 4 TeV:", out["sets"][s]["u"][50] / out["sets"][s]["d"][50])
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump(out, open(OUT, "w"))
    print("wrote", OUT)


if __name__ == "__main__":
    main()
