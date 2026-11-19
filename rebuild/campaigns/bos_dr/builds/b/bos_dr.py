"""Bosonic part of the on-shell Delta r of muon decay at one loop (see DERIVATION.md).

Delta r_bos = Sigma'_AA(0) + 2 (s/c) Sigma_AZ(0)/MZ^2 - (c^2/s^2)[Sigma_ZZ(MZ^2)/MZ^2 - Sigma_W(MW^2)/MW^2]
              + [Sigma_W(0) - Sigma_W(MW^2)]/MW^2 + delta_V,
delta_V = 2 (vertex + 1/2 wave function of the lepton and neutrino) + boxes (Feynman gauge, zero external momenta,
photon mass lambda, Fermi-theory QED subtraction = 0 at zero momentum in charge-retention order).
All masses in GeV; the MS-bar scale is set to MW inside (it cancels between the Sigma's and delta_V).
"""
import math

import mpmath as mp

import bos_se

_PI = math.pi


def _s2c2(MW, MZ):
    c2 = (MW / MZ) ** 2
    return 1.0 - c2, c2


def _dv_pieces(MW, MZ, alpha, mu, lam):
    """Finite (MS-bar, pole Delta dropped) pieces of delta_V in units of 1/(16 pi^2), as a dict; mp precision local."""
    with mp.workdps(40):
        MW, MZ, alpha, mu, lam = (mp.mpf(x) for x in (MW, MZ, alpha, mu, lam))
        c2 = (MW / MZ) ** 2
        s2 = 1 - c2
        c, s = mp.sqrt(c2), mp.sqrt(s2)
        g2 = 4 * mp.pi * alpha / s2
        g = mp.sqrt(g2)
        e2 = g2 * s2
        LW, LZ, Ll = mp.log(MW**2 / mu**2), mp.log(MZ**2 / mu**2), mp.log(lam**2 / mu**2)
        half = mp.mpf(1) / 2
        gL = (g / c) * (s2 - half)           # Z coupling of the left-handed charged lepton
        gn = g / (2 * c)                     # Z coupling of the neutrino
        b0WZ = 1 + (c2 * LW - LZ) / s2       # B0(0; MW, MZ) without the pole
        b0Wg = 1 - LW                        # B0(0; MW, 0) without the pole
        # vertex diagrams, relative to the tree vertex (O(eps) of the d-dim Dirac algebra kept)
        vD = gn * gL * (1 - LZ - mp.mpf(3) / 2)                     # Z between lepton and neutrino leg
        vA1Z = -g * c * gL * (3 * b0WZ - half)                      # Z on the lepton leg, WWZ vertex
        vA2 = g * c * gn * (3 * b0WZ - half)                        # Z on the neutrino leg, WWZ vertex
        vA1g = g2 * s2 * (3 * b0Wg - half)                          # photon on the lepton leg, WWgamma vertex
        # wave-function constants delta Z = -G, G = q^2 (Delta - ln(m^2/mu^2) - 1/2)
        G = lambda L: -L - half
        dZl = -(e2 * G(Ll) + gL**2 * G(LZ) + g2 / 2 * G(LW))
        dZn = -(gn**2 * G(LZ) + g2 / 2 * G(LW))
        # boxes (Z: four topologies, photon: mu-e)
        SZ = gL**2 - 8 * gL * gn + gn**2
        boxZ = -SZ * (c2 / s2) * (LW - LZ)
        boxg = -e2 * (Ll - LW)
        vert = 2 * (vD + vA1Z + vA2 + vA1g)
        wfn = dZl + dZn
        return {"vertex": vert, "wfn": wfn, "box_Z": boxZ, "box_gamma": boxg,
                "total": (vert + wfn + boxZ + boxg) / (16 * mp.pi**2)}   # lambda terms: wfn (+e2 Ll) and box (-e2 Ll) cancel


_EXPORT = {"AA": bos_se.sigma_AA, "AZ": bos_se.sigma_AZ, "ZZ": bos_se.sigma_ZZ, "W": bos_se.sigma_W}


def _higgs_part(kind, k2, MW, MZ, MH, alpha, mu):
    """Higgs-mass dependent part of Sigma_W (kind 'W') or Sigma_ZZ ('Z') in the 't Hooft-Feynman gauge (DERIVATION 9):
    (g_V^2/16 pi^2) [ M_V^2 B0(k2;M_V,M_H) - 1/2 Bt(k2;M_V,M_H) + 1/4 A0(M_H) ], MS-bar, g_V^2 = g^2 (W) or g^2/c^2 (Z),
    Bt = int_0^1 dx D_x (1 - ln D_x/mu^2), D_x = (1-x) M_V^2 + x M_H^2 - x(1-x) k2.  Needs the caller's mp.workdps."""
    c2 = (mp.mpf(MW) / MZ) ** 2
    g2 = 4 * mp.pi * mp.mpf(alpha) / (1 - c2)
    M2 = mp.mpf(MW if kind == "W" else MZ) ** 2
    pref = g2 if kind == "W" else g2 / c2
    H2, k2, mu2 = mp.mpf(MH) ** 2, mp.mpf(k2), mp.mpf(mu) ** 2
    pts = [mp.mpf(0)] + [mp.mpf(10) ** (-j) for j in range(40, 0, -2)] + [mp.mpf(1)]
    lnD = lambda x: mp.log(((1 - x) * M2 + x * H2 - x * (1 - x) * k2) / mu2)
    B0 = -mp.quad(lnD, pts)
    Bt = mp.quad(lambda x: (lambda L: mp.exp(L) * mu2 * (1 - L))(lnD(x)), pts)
    A0 = H2 * (1 - mp.log(H2 / mu2))
    return pref * (M2 * B0 - Bt / 2 + A0 / 4) / (16 * mp.pi**2)


def _sig(name, k2, MW, MZ, MH, alpha, mu):
    """Sigma(k2; M_H) as an mpf. The documented exports return floats; for M_H >> M_W they carry ~M_H^2 pieces that
    cancel in Delta r_bos and a float would round the answer away. So the exports are called only at a moderate
    reference mass M_H0 = M_W (no cancellation problem), and the M_H dependence (Higgs diagrams only, DERIVATION 9) is
    added exactly in mpmath: Sigma(M_H) = Sigma_export(M_H0) + [F(M_H) - F(M_H0)]. Sigma_AA, Sigma_AZ have no Higgs part."""
    ref = _EXPORT[name](float(k2), float(MW), float(MZ), float(MW), float(alpha), float(mu))
    val = mp.mpf(ref)
    if name in ("W", "ZZ"):
        kind = "W" if name == "W" else "Z"
        val += _higgs_part(kind, k2, MW, MZ, MH, alpha, mu) - _higgs_part(kind, k2, MW, MZ, MW, alpha, mu)
    return val


def _sigma_aa_prime0(MW, MZ, MH, alpha, mu):
    """Sigma'_AA(0) = lim Sigma_AA(k2)/k2 (Sigma_AA(0)=0), by Neville extrapolation of Sigma_AA(h)/h to h -> 0 (mp)."""
    hs = [mp.mpf(MW) ** 2 * mp.mpf(4) / 1000 * j for j in (1, 2, 3, 4, 5, 6)]
    P = [_sig("AA", h, MW, MZ, MH, alpha, mu) / h for h in hs]
    n = len(hs)
    for m in range(1, n):
        for i in range(n - m):
            P[i] = (hs[i + m] * P[i] - hs[i] * P[i + 1]) / (hs[i + m] - hs[i])
    return P[0]


def _sigma_terms(MW, MZ, MH, alpha, mu):
    """The Sigma part of Delta r (mp): returns (dAA, az, zz, w, w0) = Sigma'_AA(0), Sigma_AZ(0)/MZ^2,
    Sigma_ZZ(MZ^2)/MZ^2, Sigma_W(MW^2)/MW^2, Sigma_W(0)/MW^2."""
    MW2, MZ2 = mp.mpf(MW) ** 2, mp.mpf(MZ) ** 2
    return (_sigma_aa_prime0(MW, MZ, MH, alpha, mu),
            _sig("AZ", 0, MW, MZ, MH, alpha, mu) / MZ2,
            _sig("ZZ", MZ2, MW, MZ, MH, alpha, mu) / MZ2,
            _sig("W", MW2, MW, MZ, MH, alpha, mu) / MW2,
            _sig("W", 0, MW, MZ, MH, alpha, mu) / MW2)


def _prec(MW, MZ, MH):
    return 60 + 3 * int(math.ceil(math.log10(max(MH / MW, MW / MH, 10.0)))) * 2


def delta_vb(MW, MZ, alpha):
    """Finite, scale-free vertex + box + lepton wave-function contribution (DERIVATION section 8)."""
    MW, MZ = float(MW), float(MZ)
    s2, c2 = _s2c2(MW, MZ)
    mu, lam = MW, 1e-6 * MW
    with mp.workdps(60):
        loops = _dv_pieces(MW, MZ, alpha, mu, lam)["total"]
        az = _sig("AZ", 0, MW, MZ, MW, alpha, mu) / mp.mpf(MZ) ** 2   # photon-Z mixing carried by the charge relation
        return float(loops + 2 * az / mp.sqrt(mp.mpf(s2) * mp.mpf(c2)))


def delta_r_bos(MW, MZ, MH, alpha):
    MW, MZ, MH = float(MW), float(MZ), float(MH)
    with mp.workdps(_prec(MW, MZ, MH)):
        s2 = 1 - (mp.mpf(MW) / MZ) ** 2
        c2 = 1 - s2
        s, c = mp.sqrt(s2), mp.sqrt(c2)
        mu = MW
        dAA, az, zz, w, w0 = _sigma_terms(MW, MZ, MH, alpha, mu)
        sig = dAA + 2 * (s / c) * az - (c2 / s2) * (zz - w) + (w0 - w)
        dv = _dv_pieces(MW, MZ, alpha, mu, 1e-6 * MW)["total"]
        return float(sig + dv)


PROVENANCE = {
    "delta_r_bos": ("derived", "bare-parameter assembly: Sigma terms from bos_se + diagrammatic delta_V (DERIVATION sections 2-8)"),
    "delta_vb": ("derived", "Feynman-gauge vertices, boxes, lepton wave functions at zero momentum, Fermi QED subtraction, charge-mixing term"),
}


if __name__ == "__main__":
    MWv, MZv, MHv, al = 80.38, 91.19, 125.0, 1 / 128.0
    s2, c2 = _s2c2(MWv, MZv)
    print("Delta r_bos(MH=125) =", delta_r_bos(MWv, MZv, MHv, al))
    print("delta_vb            =", delta_vb(MWv, MZv, al))
    # second route 1: closed form of the diagram sum (sympy-simplified in DERIVATION section 8)
    g2 = 4 * math.pi * al / s2
    closed = g2 / (16 * math.pi**2) * (6 + (7 - 4 * s2) / (2 * s2) * math.log(c2))
    print("closed form of delta_vb    =", closed)
    # second route 2: lambda independence (IR cancellation wave function vs box)
    for lam in (1e-2, 1e-5, 1e-9):
        print("lambda =", lam, "delta_V(mu=MW) =", float(_dv_pieces(MWv, MZv, al, MWv, lam * MWv)["total"]))
    # second route 3: mu independence of the full sum (Sigma's at mu vs delta_V at mu)
    s, c = math.sqrt(s2), math.sqrt(c2)
    for mu in (30.0, 80.38, 500.0):
        with mp.workdps(60):
            h, az, zz, w, w0 = _sigma_terms(MWv, MZv, MHv, al, mu)
            sig = h + 2 * (s / c) * az - (c2 / s2) * (zz - w) + (w0 - w)
            print("mu =", mu, "total =", float(sig + _dv_pieces(MWv, MZv, al, mu, 1e-6 * MWv)["total"]))
    # second route 4: Denner-type grouping  Sigma(-2c/s) + delta_vb
    with mp.workdps(60):
        h, az, zz, w, w0 = _sigma_terms(MWv, MZv, MHv, al, MWv)
        print("Sigma(-2c/s) + delta_vb =", float(h - 2 * (c / s) * az - (c2 / s2) * (zz - w) + (w0 - w)) + delta_vb(MWv, MZv, al))
    # second route 5: large-MH behaviour, slope in ln MH^2 -> 11 alpha/(48 pi s^2)
    f = lambda mh: delta_r_bos(MWv, MZv, mh, al)
    print("slope at MH=1e13..1e14:", (f(1e14) - f(1e13)) / math.log(10.0 ** 2), " expected", 11 * al / (48 * math.pi * s2))
