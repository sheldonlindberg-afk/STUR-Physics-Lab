#!/usr/bin/env python3
"""Digitise the combined-dilepton limits of ATLAS, PLB 796 (2019) 68, arXiv:1903.06248, Fig. 3.

The figures are vector PDFs in the arXiv source (https://arxiv.org/e-print/1903.06248).
Each curve is read from its drawing path; the axes are calibrated from the tick labels and
the mass axis is anchored to the stated scan range, 250-6000 GeV.

Usage:  python3 tools/digitize_atlas_dilepton.py <dir with fig_03a.pdf, fig_03b.pdf>
Writes: results/m331/zprime/atlas_1903.06248_fig3.json
Needs:  pymupdf (pip install pymupdf). Not needed to run the recast itself.
"""
import json, os, sys
import numpy as np
import pymupdf

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
OUT = os.path.join(ROOT, "results", "m331", "zprime", "atlas_1903.06248_fig3.json")

# (colour, dash pattern) -> curve name, per figure; colours from the figure legends
NAMES = {
    "fig_03a.pdf": {("0.0,0.0,0.0", "[] 0"): "obs_0.0", ("0.0,0.0,0.0", "[ 5 5 ] 0"): "exp_0.0",
                    ("1.0,0.0,1.0", "[] 0"): "obs_3.0", ("1.0,0.0,1.0", "[ 3 3 ] 0"): "exp_3.0",
                    ("1.0,0.0,0.0", "[] 0"): "obs_10.0", ("1.0,0.0,0.0", "[ 1 2 ] 0"): "exp_10.0",
                    ("0.0,0.0,1.0", "[] 0"): "model_SSM"},
    "fig_03b.pdf": {("0.0,0.0,0.0", "[] 0"): "obs_0.5", ("0.0,0.0,0.0", "[ 5 5 ] 0"): "exp_0.5",
                    ("1.0,0.0,1.0", "[] 0"): "obs_1.2", ("1.0,0.0,1.0", "[ 3 3 ] 0"): "exp_1.2",
                    ("1.0,0.0,0.0", "[] 0"): "obs_6.0", ("1.0,0.0,0.0", "[ 1 2 ] 0"): "exp_6.0",
                    ("0.0,0.0,1.0", "[] 0"): "model_psi", ("0.0,0.0,1.0", "[ 3 3 ] 0"): "model_chi"},
}


def digitise(path, names):
    pg = pymupdf.open(path)[0]
    xs, ys = {}, {}
    for b in pg.get_text("dict")["blocks"]:
        for l in b.get("lines", []):
            for s in l["spans"]:
                t = s["text"].strip(); x0, y0, x1, y1 = s["bbox"]
                if t in ("1000", "2000", "3000", "4000", "5000", "6000") and s["size"] > 15:
                    xs[int(t)] = (y0 + y1) / 2
                if t in ("10", "1") and s["size"] > 15 and y0 > 470:
                    ys.setdefault(t, []).append((x0 + x1) / 2)
    m = np.array(sorted(xs))
    am, bm = np.polyfit([xs[k] for k in m], m, 1)
    tens = sorted(ys["10"], reverse=True)              # 1e-2, 1e-1, 1e1 in drawing order
    pts = [(tens[0], -2), (tens[1], -1), (ys["1"][0], 0), (tens[2], 1)]
    ay, by = np.polyfit([p[0] for p in pts], [p[1] for p in pts], 1)
    raw = {}
    for d in pg.get_drawings():
        if round(d.get("width") or 0, 2) != 1.5 or len(d["items"]) < 30:
            continue
        key = (",".join(f"{c:.1f}" for c in d["color"]), d.get("dashes"))
        if key not in names:
            continue
        p = sorted({(am * P.y + bm, ay * P.x + by) for it in d["items"] if it[0] == "l" for P in it[1:3]})
        raw[names[key]] = np.array(p)
    # anchor the mass axis: limits are scanned from 250 to 6000 GeV (paper, Section 7)
    lim = [v for k, v in raw.items() if k.startswith("obs_")]
    lo = min(v[:, 0].min() for v in lim); hi = max(v[:, 0].max() for v in lim)
    fix = lambda mm: 250 + (mm - lo) * 5750 / (hi - lo)
    return {k: [[round(float(fix(a)), 1), round(float(10 ** b), 6)] for a, b in v] for k, v in raw.items()}


def main(src):
    data = {"source": "ATLAS, Phys. Lett. B 796 (2019) 68, arXiv:1903.06248, Fig. 3 (combined ee+mumu)",
            "quantity": "95% CL upper limit on fiducial sigma x B(X -> ll, single flavour) [fb]; "
                        "model_* are ATLAS's fiducial predictions",
            "keys": "obs_/exp_<relative width in %>, model_<SSM|psi|chi>; rows are [mass GeV, fb]",
            "curves": {}}
    for f, names in NAMES.items():
        data["curves"].update(digitise(os.path.join(src, f), names))
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump(data, open(OUT, "w"), indent=0)
    print("wrote", OUT, sorted(data["curves"]))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else ".")
