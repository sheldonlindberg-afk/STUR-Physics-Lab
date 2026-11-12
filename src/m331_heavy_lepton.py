#!/usr/bin/env python3
"""
The heavy charged leptons of the beta = +1/sqrt3 model against the LHC (NOTE_331.md, section 3f).

Section 3e found that in this variant N_c = 3 reaches M_Pl at alpha = 1 only if the heavy
charged leptons E are heavy enough (m_E >= 0.56 +- 0.11 TeV with M_V at its LHC bound).
This module asks what the LHC already says about E, and what the HL-LHC can say.

E is the third member of the lepton triplet (nu, e, E^-), with E^c an SU(3)_L singlet: both
chiralities are SU(2)_L singlets with Y = Q = -1. Below M_V it is a vector-like singlet
lepton, the benchmark the LHC searches use. It mixes with the ordinary leptons through the
allowed Yukawas (L chi* e^c and L rho* E^c type terms; e^c and E^c carry the same charges),
so it decays promptly to W nu, Z l, h l, and the search that applies depends on which
flavour it mixes with. There are three E, one per generation.

H1  CHECK: the partonic cross section q qbar -> gamma*/Z/Z' -> F Fbar for a massive F with
    general chiral couplings reproduces the QED result (4 pi alpha^2/3s) beta (3 - beta^2)/2
    and, massless, 4 pi alpha^2 Q^2/(9 s).
H2  CHECK: the hadronic cross section against Pythia 8 (ffbar2gmZZprime, full interference,
    same PDF and couplings, tau' in its doublet mode): results/m331/vll/pythia_crosscheck.json
    from tools/vll_pythia_crosscheck.py.
H3  The singlet benchmark at LO against the theory curve ATLAS uses (arXiv:2411.07143):
    ATLAS's curve is 22% below LO at 150 GeV and 19% above at 800 GeV; we do not reproduce
    its normalisation and use only ratios. The 3-3-1 E is normalised to ATLAS's curve times
    sigma_LO(3-3-1) / sigma_LO(singlet). The Z' (4.6 TeV) interferes constructively: +2% at
    400 GeV, +6% at 600 GeV, +16% at 800 GeV.
H4  Mass limits per flavour (observed, expected): e and mu partners (ATLAS, 140 fb^-1,
    HEPData ins2847252), tau partners (CMS, 138 fb^-1, HEPData ins2034279). Each search
    assumes the singlet benchmark's branching ratios.
H5  The RG condition is on the geometric mean. The threshold correction depends on
    sum_i ln(m_Ei / mu), so three non-degenerate E act like three degenerate ones at
    (m_E1 m_E2 m_E3)^(1/3) (checked against the full running). With each E mixing with one
    flavour, the lightest spectrum the LHC allows has a geometric mean of ~0.23 TeV, below
    the 0.56 TeV the selection needs: the LHC has not tested the condition.
H6  HL-LHC (3 ab^-1, 13 TeV cross sections; 14 TeV would help further): expected limits
    scaled by sqrt(L0/L) (background-limited) and by L0/L (background-free), the two ends.
H7  The condition itself moves: with no Z' at the HL-LHC the Z' floor (same recast, same
    scaling) rises, M_V with it, and so does m_E*.
"""
import json
import os
from functools import lru_cache
import sys
from math import log, pi, sqrt

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import m331_zprime_recast as Z

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "results", "m331", "vll")
LUMI = json.load(open(os.path.join(DATA, "lumi_dy_13TeV.json")))
HEP = json.load(open(os.path.join(DATA, "hepdata_vll.json")))
SETS = {"NNPDF3.1": "NNPDF31_nnlo_as_0118_luxqed_0000.dat", "PDF4LHC21": "PDF4LHC21_mc_0000.dat"}

S2_MZ = 0.23122                        # MS-bar at M_Z (Z couplings)
AEM_MZ = 0.00781751                    # Pythia's alpha_em(M_Z), used for the Pythia comparison
AEM = 1 / 127.95                       # as in the rest of the repo
MZ, GZ = 91.1876, 2.4952
BETA = 1 / sqrt(3)
SQRTS = 13000.0
GEV2_TO_FB = 0.3894e12                 # (hbar c)^2 in GeV^2 fb
L_RUN2 = {"e": 140.0, "mu": 140.0, "tau": 138.0}


def banner(s):
    print("\n" + "=" * 78 + "\n" + s + "\n" + "=" * 78)


# ---------------------------------------------------------------- couplings ----------
def couplings(mode="singlet", MZp=4600.0, widths=None):
    """Bosons as (mass, width, {quark flavour: (gL, gR)}, (gL_F, gR_F)), couplings in units of e.
    mode: 'singlet' (E: SU(2) singlet, Y = -1), 'doublet' (T3 = -1/2: Pythia's tau', for H2),
    'singlet_noZp' (the LHC benchmark: gamma and Z only)."""
    sw, cw = sqrt(S2_MZ), sqrt(1 - S2_MZ)
    gz = 1 / (sw * cw)
    q = {"u": (2 / 3, 0.5), "d": (-1 / 3, -0.5), "s": (-1 / 3, -0.5), "c": (2 / 3, 0.5), "b": (-1 / 3, -0.5)}
    QF, T3F = -1.0, (-0.5 if mode == "doublet" else 0.0)
    gamma = (0.0, 0.0, {k: (Q, Q) for k, (Q, T3) in q.items()}, (QF, QF))
    zq = {k: (gz * (T3 - Q * S2_MZ), gz * (-Q * S2_MZ)) for k, (Q, T3) in q.items()}
    gZw, gZpw = (GZ, None) if widths is None else widths
    zb = (MZ, gZw, zq, (gz * (T3F - QF * S2_MZ), gz * (-QF * S2_MZ)))
    if mode == "singlet_noZp":
        return [gamma, zb]
    gens = Z.model_couplings("331", beta=BETA, s2=Z.S2_TEV)
    fl = {"d": (0, "d"), "u": (0, "u"), "s": (1, "d"), "c": (1, "u"), "b": (2, "d")}
    zpq = {k: (gz * gens[g][f]["L"], gz * gens[g][f]["R"]) for k, (g, f) in fl.items()}
    E = [x for x in Z.exotic_couplings(BETA, Z.S2_TEV) if x[0] == "E"][0]
    zpF = (gz * E[2], gz * E[3])
    if gZpw is None:
        ex = Z.exotic_couplings(BETA, Z.S2_TEV) + Z.scalar_couplings(BETA, Z.S2_TEV)
        sm, exw, _, _ = Z.widths(gens, Z.S2_TEV, ex)
        gZpw = (sm + exw) * MZp
    return [gamma, zb, (MZp, gZpw, zpq, zpF)]


def pythia_couplings(MZp=4600.0):
    """Pythia's Zprime:v_f, a_f (v = 2(gL + gR), a = 2(gL - gR) in units of g/c_W) for the
    3-3-1 Z', with the E couplings on the tau' (tools/vll_pythia_crosscheck.py)."""
    gens = Z.model_couplings("331", beta=BETA, s2=Z.S2_TEV)
    out = []
    names = [("d", "u", "e", "nue"), ("s", "c", "mu", "numu"), ("b", "t", "tau", "nutau")]
    for g, (dn, up, l, nu) in enumerate(names):
        for nm, f in ((dn, "d"), (up, "u"), (l, "e"), (nu, "nu")):
            gL, gR = gens[g][f]["L"], gens[g][f]["R"]
            out += [f"Zprime:v{nm} = {2 * (gL + gR):.8f}", f"Zprime:a{nm} = {2 * (gL - gR):.8f}"]
    E = [x for x in Z.exotic_couplings(BETA, Z.S2_TEV) if x[0] == "E"][0]
    out += [f"Zprime:vtauPrime = {2 * (E[2] + E[3]):.8f}", f"Zprime:atauPrime = {2 * (E[2] - E[3]):.8f}"]
    return out


# ---------------------------------------------------------------- cross sections -----
def sigma_hat(shat, m, qf, bosons, aem=AEM):
    """q qbar -> F Fbar (colour-singlet F), averaged over initial spins and colours, GeV^-2.
    Helicity amplitudes with A_ab = sum_i g_q^a g_F^b e^2 / (s - M_i^2 + i M_i Gamma_i):
      opposite F helicities: (1 +- c)^2 |A1 (1 +- b) + A2 (1 -+ b)|^2 / 4
      equal F helicities:    2 (1 - b^2) (1 - c^2) |A1 + A2|^2 / 4
    with (A1, A2) = (A_LL, A_LR) for a left-handed quark and (A_RR, A_RL) for a right-handed one.
    shat may be an array."""
    sh = np.atleast_1d(np.asarray(shat, float))
    ok = sh > 4 * m * m
    b = np.sqrt(np.where(ok, 1 - 4 * m * m / np.where(ok, sh, 1.0), 0.0))
    e2 = 4 * pi * aem
    A = {a + f: sum(gq[qf][a == "R"] * gF[f == "R"] * e2 / (sh - M * M + 1j * M * W) for M, W, gq, gF in bosons)
         for a in "LR" for f in "LR"}
    tot = np.zeros_like(sh)
    for A1, A2 in ((A["LL"], A["LR"]), (A["RR"], A["RL"])):
        tot += 8 / 3 * (np.abs(A1 * (1 + b) + A2 * (1 - b)) ** 2 + np.abs(A1 * (1 - b) + A2 * (1 + b)) ** 2) / 4
        tot += 2 * (1 - b * b) * 4 / 3 * np.abs(A1 + A2) ** 2 / 4
    out = np.where(ok, b / (32 * pi * sh) * sh**2 * tot / 12, 0.0)
    return out if np.ndim(shat) else float(out[0])


def _lumi(pdfset):
    mh = np.array(LUMI["mhat_GeV"])
    tab = LUMI["sets"][SETS[pdfset]]
    return lambda q, M: np.exp(np.interp(np.log(M), np.log(mh), np.log(np.array(tab[q]))))


def sigma_pair(m, MZp=4600.0, mode="singlet", pdfset="NNPDF3.1", widths=None, aem=AEM, n=3000):
    """sigma(p p -> F Fbar) at 13 TeV in fb (LO): sum_q int dtau dL_q/dtau sigma_hat(tau s)."""
    bos = couplings(mode, MZp, widths)
    L = _lumi(pdfset)
    lo, hi = log(2 * m * 1.000001), log(7000.0)
    lm = np.linspace(lo, hi, n)
    if mode != "singlet_noZp" and 2 * m < MZp:            # resolve the Z' peak
        W = bos[-1][1]
        lm = np.union1d(lm, np.log(np.linspace(MZp - 8 * W, MZp + 8 * W, 801)))
    M = np.exp(lm)
    tot = np.zeros_like(M)
    for q in "duscb":
        tot += L(q, M) * sigma_hat(M * M, m, q, bos, aem)
    # dtau = 2 M^2 dlnM / s
    return float(np.trapezoid(tot * 2 * M * M / SQRTS**2, lm)) * GEV2_TO_FB


# ---------------------------------------------------------------- data ---------------
def _curve(rows):
    a = np.array(rows)
    return lambda m: float(np.exp(np.interp(m, a[:, 0], np.log(a[:, 1]))))


def theory_atlas(m):
    return _curve(HEP["e"]["theory"])(m) * 1e3            # fb; same curve for e and mu


@lru_cache(maxsize=None)
def z_ratio(m, MZp=4600.0):
    """sigma_LO(3-3-1 E, gamma + Z + Z') / sigma_LO(singlet benchmark, gamma + Z)."""
    return sigma_pair(m, MZp, "singlet") / sigma_pair(m, MZp, "singlet_noZp")


def sigma_331(m, MZp=4600.0, flavour="e", K=1.0):
    """The 3-3-1 E pair cross section in fb. For e and mu: ATLAS's singlet curve times the
    model ratio (H3), so the normalisation is the one ATLAS's limit was set against. For tau,
    whose CMS limit is on sigma x B with CMS's own normalisation, the LO cross section with
    the 3-3-1 Z' times K (K = 1.0-1.2 brackets the NLO QCD correction)."""
    m = round(float(m), 3)
    if flavour == "tau":
        return K * sigma_pair(m, MZp, "singlet")
    return theory_atlas(m) * z_ratio(m, MZp)


def mass_limit(flavour, kind="obs", scale=1.0, MZp=4600.0, K=1.0):
    """Excluded mass window (lowest, highest excluded m in GeV) where sigma_331 > limit x scale,
    over the range the published limit covers; (None, None) if nothing is excluded. With
    scale < 1 (projections) the upper edge may run past the last published point: it is then
    capped there and flagged by the caller."""
    from scipy.optimize import brentq
    rows = np.array(HEP[flavour][kind])
    lim = _curve(HEP[flavour][kind])
    f = lambda x: log(sigma_331(x, MZp, flavour, K) / (lim(x) * 1e3 * scale))
    ms = np.linspace(rows[:, 0].min(), rows[:, 0].max(), 37)
    v = [f(x) for x in ms]
    ex = [i for i, y in enumerate(v) if y > 0]
    if not ex:
        return None, None
    i0, i1 = ex[0], ex[-1]
    lo = ms[i0] if i0 == 0 else brentq(f, ms[i0 - 1], ms[i0], xtol=0.5)
    hi = ms[i1] if i1 == len(ms) - 1 else brentq(f, ms[i1], ms[i1 + 1], xtol=0.5)
    return lo, hi


# ---------------------------------------------------------------- RG link ------------
def geometric_mean_check():
    """H5: three non-degenerate E vs degenerate at their geometric mean (alpha = 1, 3 loops)."""
    import m331_margin as M
    trip = (320.0, 400.0, 100.0)
    gm = float(np.prod(trip)) ** (1 / 3)
    p3 = M.pole(**dict(M.FLOORS, mE=trip)) / M.M_PLANCK
    p1 = M.pole(**dict(M.FLOORS, mE=gm)) / M.M_PLANCK
    return trip, gm, p3, p1


LEP = 100.0                            # LEP2 limit on heavy charged leptons, GeV (approximate)
MSTAR = (561.0, 113.0)                 # section 3e: m_E* at M_V = 3.755 TeV, alpha = 1, three loops


def geo(xs):
    return float(np.prod(np.asarray(xs, float))) ** (1 / len(xs))


def run2_limits():
    """{flavour: {K: ((obs lo, obs hi), (exp lo, exp hi))}}."""
    out = {}
    for fl in ("e", "mu", "tau"):
        Ks = (1.0, 1.2) if fl == "tau" else (1.0,)
        out[fl] = {K: (mass_limit(fl, "obs", K=K), mass_limit(fl, "exp", K=K)) for K in Ks}
    return out


def lightest_allowed(out):
    """Lightest m_E allowed per flavour by Run 2: just above the observed excluded window when it
    starts at the search's first point, else the LEP limit (taking K = 1.2 for tau)."""
    res = []
    for fl in ("e", "mu", "tau"):
        lo, hi = out[fl][max(out[fl])][0]
        first = np.array(HEP[fl]["obs"])[:, 0].min()
        res.append(hi if (lo is not None and lo <= first + 1) else LEP)
    return res


def hl_reach():
    """Expected 3 ab^-1 reach per flavour: (mass, capped) for sqrt(L0/L) and L0/L scaling."""
    res = {}
    for fl in ("e", "mu", "tau"):
        L0, K = L_RUN2[fl], (1.2 if fl == "tau" else 1.0)
        mx = np.array(HEP[fl]["exp"])[:, 0].max()
        r = []
        for sc in (sqrt(L0 / 3000), L0 / 3000):
            hi = mass_limit(fl, "exp", scale=sc, K=K)[1]
            r.append((hi if hi else LEP, bool(hi and hi >= mx - 1)))
        res[fl] = tuple(r)
    return res


def zprime_reach(scale=1.0, kind="exp"):
    """The Z' bound (TeV-scale, GeV) from the recast of src/m331_zprime_recast.py with the ATLAS
    limit scaled by `scale`, all exotic and scalar channels open (the conservative case)."""
    gens = Z.model_couplings("331", beta=BETA, s2=Z.S2_TEV)
    ex = Z.exotic_couplings(BETA, Z.S2_TEV) + Z.scalar_couplings(BETA, Z.S2_TEV)
    _, w, _, pred = Z.recast(gens, Z.S2_TEV, ex, kind=kind)
    ms = np.arange(2000.0, 6001.0, 1.0)
    excl = pred(ms) > Z.limit_at_width(ms, w, kind) * scale
    return float(ms[np.nonzero(excl)[0][-1]])


def hl_threshold():
    """H7: m_E* (alpha = 1, three loops) with M_V at the projected HL-LHC Z' floor (sqrt(L)
    scaling, all channels open), with and without Yukawas. M_V = M_Z' / 1.225 as in section 3a."""
    import m331_margin as M
    mz = zprime_reach(sqrt(139.0 / 3000))
    MV = mz / 1.225
    return mz, MV, M.mE_critical(MV=MV), M.mE_critical(MV=MV, yukawas=False)


def main():
    banner("H1  CHECK: partonic cross section against QED (photon only)")
    bos = [(0.0, 0.0, {"u": (1.0, 1.0)}, (1.0, 1.0))]
    for m, s in ((0.0, 1e6), (300.0, 1e6), (480.0, 1e6)):
        b = sqrt(1 - 4 * m * m / s)
        mine = sigma_hat(s, m, "u", bos) * 3          # undo the 1/3 colour average for the QED form
        ref = 4 * pi * AEM**2 / (3 * s) * b * (3 - b * b) / 2
        print(f"   sqrt(s) = 1 TeV, m = {m:3.0f} GeV: module / QED = {mine / ref:.12f}")

    banner("H2  CHECK: hadronic cross section against Pythia 8 (tau' doublet mode, 3-3-1 Z')")
    pc = json.load(open(os.path.join(DATA, "pythia_crosscheck.json")))
    for r in pc:
        mine = sigma_pair(r["mF"], MZp=r["MZp"], mode="doublet", widths=(r["GammaZ"], r["GammaZp"]), aem=AEM_MZ)
        print(f"   m_F = {r['mF']:4.0f} GeV, M_Z' = {r['MZp'] / 1e3:.1f} TeV: Pythia {r['pythia_fb']:.4g} +- "
              f"{r['pythia_err_fb']:.2g} fb, module {mine:.4g} fb, ratio {mine / r['pythia_fb']:.4f}")

    banner("H3  The singlet benchmark at LO vs ATLAS's theory curve; the Z' effect")
    for m in (150.0, 200.0, 300.0, 400.0, 500.0, 600.0, 800.0):
        s0 = sigma_pair(m, mode="singlet_noZp")
        s1 = sigma_pair(m, mode="singlet")
        s1p = sigma_pair(m, mode="singlet_noZp", pdfset="PDF4LHC21")
        print(f"   m = {m:4.0f} GeV: LO {s0:8.4g} fb (PDF4LHC21 {s1p / s0:.3f}x), ATLAS {theory_atlas(m):8.4g} fb,"
              f" K = {theory_atlas(m) / s0:.3f};  with Z' (4.6 TeV): x{s1 / s0:.4f}")

    banner("H4  Run-2 mass limits on the 3-3-1 E, by the flavour it mixes with")
    out = run2_limits()
    for fl, lab in (("e", "e  "), ("mu", "mu "), ("tau", "tau")):
        for K, (o, e) in out[fl].items():
            ks = "" if fl != "tau" else f" (K = {K:.1f})"
            so = f"{o[0]:.0f}-{o[1]:.0f} GeV" if o[0] else "nothing"
            se = f"{e[0]:.0f}-{e[1]:.0f} GeV" if e[0] else "nothing"
            print(f"   E mixing with {lab}{ks}: excluded {so} observed, {se} expected")
    print(f"   Below each search's first mass point (150 GeV for e, mu; 100 GeV for tau) LEP's")
    print(f"   ~{LEP:.0f} GeV applies. A tau-mixed E is allowed down to the LEP limit.")

    banner("H5  The RG condition is on the geometric mean of the three m_E")
    trip, gm, p3, p1 = geometric_mean_check()
    print(f"   m_E = {trip} GeV: pole {p3:.4f} M_Pl;  degenerate at the geometric mean {gm:.0f} GeV: {p1:.4f} M_Pl")
    low = lightest_allowed(out)
    print(f"   lightest Run-2-allowed set, one E per flavour: (e, mu, tau) = ({low[0]:.0f}, {low[1]:.0f},"
          f" {low[2]:.0f}) GeV, geometric mean {geo(low):.0f} GeV")
    print(f"   if all three mix with tau: geometric mean {LEP:.0f} GeV")
    print(f"   the selection needs >= {MSTAR[0]:.0f} +- {MSTAR[1]:.0f} GeV (M_V = 3.755 TeV): the LHC has not tested it.")

    banner("H6  HL-LHC, 3 ab^-1 (13 TeV cross sections): expected reach per flavour")
    res = hl_reach()
    for fl in ("e", "mu", "tau"):
        (a, ca), (b, cb) = res[fl]
        cap = lambda c: " (capped: past the last published point)" if c else ""
        print(f"   {fl:3s}: {a:.0f} GeV{cap(ca)} background-limited, {b:.0f} GeV{cap(cb)} background-free")
    ga = geo([res[f][0][0] for f in ("e", "mu", "tau")])
    gb = geo([res[f][1][0] for f in ("e", "mu", "tau")])
    print(f"   geometric mean of the reach, one E per flavour: {ga:.0f} to {gb:.0f} GeV, against m_E* ="
          f" {MSTAR[0]:.0f} +- {MSTAR[1]:.0f} GeV")
    print("   The tau-mixed E sets the pace: its reach is the weakest of the three.")

    banner("H7  The target moves: m_E* with M_V at the projected HL-LHC Z' floor")
    mz, MV, a, b = hl_threshold()
    print(f"   Z' expected reach at 3 ab^-1 (sqrt(L) scaling, all channels open): {mz / 1e3:.2f} TeV"
          f" (Run 2 expected {zprime_reach() / 1e3:.2f} TeV)")
    print(f"   -> M_V >= {MV / 1e3:.2f} TeV;  m_E* = {a:.0f} GeV with Yukawas, {b:.0f} GeV without"
          f" (+-20% truncation, section 3e)")
    print(f"   HL-LHC geometric-mean reach {ga:.0f}-{gb:.0f} GeV vs this m_E*: the HL-LHC reaches the")
    print("   threshold, but covers its uncertainty band only with the optimistic scaling, and only")
    print("   if each E mixes with a different flavour (all tau-mixed: reach "
          f"{res['tau'][0][0]:.0f}-{res['tau'][1][0]:.0f} GeV).")


if __name__ == "__main__":
    main()
