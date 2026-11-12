#!/usr/bin/env python3
"""Fetch the LHC singlet vector-like-lepton limits used by src/m331_heavy_lepton.py.

  ATLAS, JHEP 05 (2025) 075, arXiv:2411.07143 (140 fb^-1), HEPData ins2847252 v1:
    Figure 9a  singlet e partner:  theory sigma, expected and observed 95% CL limits
    Figure 9c  singlet mu partner: same
  CMS, inclusive nonresonant multilepton search, arXiv:2202.08676 (138 fb^-1),
    HEPData ins2034279 v1, table "Singlet VLL limit": singlet tau partner, expected and
    observed 95% CL limits on sigma x B.

Writes results/m331/vll/hepdata_vll.json. Needs curl and network access; not needed to run the module.
"""
import csv, io, json, os, subprocess, urllib.parse

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
OUT = os.path.join(ROOT, "results", "m331", "vll", "hepdata_vll.json")
TABLES = {"e": ("ins2847252", "Figure 9a"), "mu": ("ins2847252", "Figure 9c"), "tau": ("ins2034279", "Singlet VLL limit")}


def blocks(rec, name):
    url = f"https://www.hepdata.net/download/table/{rec}/{urllib.parse.quote(name)}/1/csv"
    text = subprocess.run(["curl", "-sS", "-L", "-m", "60", url], check=True, capture_output=True, text=True).stdout
    out, cur, head = [], None, None
    for line in text.splitlines():
        row = next(csv.reader(io.StringIO(line))) if line.strip() else []
        if row and "GeV" in row[0]:                      # a new table block: its column header
            if cur:
                out.append((head, cur))
            head, cur = row, []
            continue
        try:
            vals = [float(x) for x in row[:2]]
        except ValueError:
            continue                                     # description or metadata line
        if cur is not None and len(vals) == 2:
            cur.append(vals)
    if cur:
        out.append((head, cur))
    return url, out


def main():
    res = {}
    for fl, (rec, name) in TABLES.items():
        url, bl = blocks(rec, name)
        d = {"source": url}
        for head, rows in bl:
            h = head[1].lower()
            key = "theory" if "theory" in h else "obs" if "observed" in h else "exp" if ("expected" in h and "only" not in h) else None
            if key and key not in d:
                d[key] = rows
        res[fl] = d
        print(fl, {k: len(v) for k, v in d.items() if k != "source"})
    json.dump(res, open(OUT, "w"), indent=1)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
