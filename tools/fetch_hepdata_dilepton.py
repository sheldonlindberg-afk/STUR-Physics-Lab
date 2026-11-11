#!/usr/bin/env python3
"""Official ATLAS dilepton limits from HEPData (ins1725190, doi:10.17182/hepdata.88425.v1).

ATLAS, Phys. Lett. B 796 (2019) 68, arXiv:1903.06248: observed and expected 95% CL limits on
the fiducial sigma x B(X -> ll, one flavour), combined ee + mumu, for relative widths
0, 0.5, 1.2, 3, 6 and 10% (tables t4/t5). The Z'_SSM prediction is not tabulated directly;
it is reconstructed as (observed 3%-width limit) / (table t9: observed limit / SSM
cross-section, 139 fb^-1 entry).

Units: the tables label the limits "pb", but the values are the femtobarn numbers quoted in
the paper (3.6 fb at 250 GeV, 0.014 fb at 6 TeV for zero width). Stored here in fb.

Usage:  curl -L -o hepdata_ins1725190.tar.gz https://www.hepdata.net/download/submission/ins1725190/1/csv
        python3 tools/fetch_hepdata_dilepton.py hepdata_ins1725190.tar.gz
Writes: results/m331/zprime/atlas_1903.06248_hepdata.json
"""
import csv, json, os, sys, tarfile
import numpy as np

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
OUT = os.path.join(ROOT, "results", "m331", "zprime", "atlas_1903.06248_hepdata.json")
FILES = {"obs": "Observeddileptoncross-sectionlimits.csv", "exp": "Expecteddileptoncross-sectionlimits.csv",
         "ratio": "RatioofobservedlimitstoSSMcrosssection.csv"}


def blocks(text):
    out, meta, rows, hdr = [], {}, [], None
    for line in text.splitlines():
        if line.startswith("#:"):
            if rows:
                out.append((dict(meta), hdr, rows)); meta, rows, hdr = {}, [], None
            k, _, v = line[3:].partition(",")
            if ":" in k and not v:
                k, _, v = k.partition(":")
            meta[k.strip()] = v.strip()
        elif not line.strip():
            continue
        elif hdr is None:
            hdr = line
        else:
            r = next(csv.reader([line]))
            if "-" not in [x.strip() for x in r]:
                rows.append([float(x) for x in r])
    if rows:
        out.append((dict(meta), hdr, rows))
    return out


def main(archive):
    tar = tarfile.open(archive, mode="r:gz")
    text = {k: tar.extractfile(next(m for m in tar.getmembers() if m.name.endswith(f))).read().decode()
            for k, f in FILES.items()}
    curves = {}
    for kind in ("obs", "exp"):
        for meta, hdr, rows in blocks(text[kind]):
            assert meta["LUMINOSITY [fb$^{-1}$]"] == "139" and "Mass [GeV]" in hdr
            curves[f"{kind}_{float(meta['RELATIVE WIDTH [%]'])}"] = rows
    ratio = [np.array(r) for m, h, r in blocks(text["ratio"]) if m.get("EE LUMINOSITY [fb$^{-1}$]") == "139"][0]
    o3 = np.array(curves["obs_3.0"])
    m = ratio[:, 0] * 1000
    ssm = np.exp(np.interp(m, o3[:, 0], np.log(o3[:, 1]))) / ratio[:, 1]
    curves["model_SSM"] = [[float(a), float(b)] for a, b in zip(m, ssm)]
    data = {"source": "ATLAS, PLB 796 (2019) 68, arXiv:1903.06248; HEPData ins1725190 v1, "
                      "doi:10.17182/hepdata.88425.v1 (tables t4, t5, t9)",
            "quantity": "95% CL upper limit on fiducial sigma x B(X -> ll, single flavour) [fb]; model_SSM "
                        "reconstructed as obs_3.0 / (t9 ratio, 139 fb^-1)",
            "units_note": "HEPData labels these limits pb; the values equal the fb numbers in the paper text",
            "curves": curves}
    json.dump(data, open(OUT, "w"))
    print("wrote", OUT, sorted(curves))


if __name__ == "__main__":
    main(sys.argv[1])
