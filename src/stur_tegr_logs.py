#!/usr/bin/env python3
"""
Does TEGR's frame change the logarithmic correction to black-hole entropy?

stur_tegr_frame Q5-Q8: TEGR's frame at a corner is a Lorentz coadjoint orbit with radius
the area density / 8 pi G. Quantized as a group (Q7), its Plancherel density grows
linearly and adds a logarithm, not the area law. This module compares that logarithm
with the universal one-loop result.

Benchmarks (quoted, LIT):
  Sen, arXiv:1205.0971 (JHEP 04 (2013) 156), eqs. (1.2), (1.5): for Schwarzschild in
    D = 4, in the ensemble of rotation-singlet states per unit mass interval,
        Delta S_singlet = (C_local - 3) ln a,
        C_local = (2 n_S - 26 n_V + 7 n_F - (233/2) n_{3/2} + 424) / 90,
    a the size parameter (A ~ a^2). Pure gravity: (212/45 - 3) ln a = (77/45) ln a.
    The coefficient is the integrated trace anomaly plus zero modes; it depends on the
    massless field content and is independent of the ultraviolet completion.
  Sen, same paper, section 4: SU(2) loop quantum gravity gives -2 ln a in that ensemble.
  Varrin, arXiv:2610.37750, eqs. (4.20)-(4.24): edge entropy 2 <ln mu(k)> plus the Shannon
    term, k = A / 16 pi G; the edge logarithm is 2 ln k.
  David and Mukherjee, arXiv:2201.06043: the graviton's edge sectors across a sphere in
    flat space give a log coefficient -16/3, equal to the edge character of the massless
    spin-2 field. (A flat-space entanglement benchmark, not a black-hole ensemble.)

Computed here (CHECK):
  L1  The logarithm of Varrin-type edge counting, 2 <ln mu(k)>, for the groups the frame
      could be quantized with. The label k is proportional to A in each case:
        SO(1,1), the normal boost alone (spherical reduction): flat measure, mu = 1;
        SL(2,R) = so(2,1) (Q7): mu = k tanh(pi k)  (Varrin eq. 4.14);
        SL(2,C) = so(3,1), simple principal series (n = 0, rho): mu ~ rho^2
          (Gelfand-Naimark Plancherel density (n^2 + rho^2): dm = |mu + i lambda|^2 dmu dlambda,
           LIT: arXiv:2403.17180, section on the classical complex case);
        and, for comparison, Varrin's causal semigroup SL+(2,R): mu = k sinh(2 pi k).
      Coefficient of ln a fitted from A = 1e4 to 1e8, after removing any area term.
  L2  Conversion to Sen's ensemble (exact): k = A / 16 pi = M^2, so at a fixed mass window
      the width in k is 2 M dM, and the Shannon term adds +1 x ln a. This is the same
      conversion Sen uses for loop quantum gravity.
  L3  The comparison table, all in Sen's ensemble (coefficient of ln a).
FOLLOWS: edge counting gives 1, 5 or 9 depending on the group, against Sen's 77/45 for
pure gravity (1.42 with the photon). None depends on the matter content, as Sen's must.
The frame's logarithm is construction-dependent and is not the universal one.
Since TEGR and GR have the same one-loop bulk determinants, the universal coefficient is
the same in both, provided the frame is treated as gauge in the path-integral measure.
Counting the frame's orbit states as physical would shift it. Labels: LIT, CHECK, FOLLOWS.
"""
from fractions import Fraction as Fr

import mpmath as mp


def banner(s):
    print("\n" + "=" * 78 + "\n" + s + "\n" + "=" * 78)


def sen_c_local(nS=0, nV=0, nF=0, n32=0):
    """Sen eq. (1.2), uncharged black holes in D = 4."""
    return (Fr(2 * nS - 26 * nV + 7 * nF) - Fr(233, 2) * n32 + 424) / 90


def sen_singlet(nS=0, nV=0, nF=0, n32=0):
    """Sen eq. (1.5), D = 4, uncharged: C_local - (D - 2) N_R / 2 with N_R = 3."""
    return sen_c_local(nS, nV, nF, n32) - 3


SEN_LQG_SU2 = Fr(-2)                        # Sen section 4, eq. (4.3)
DAVID_MUKHERJEE_GRAVITON_EDGE = Fr(-16, 3)  # flat-space sphere, coefficient of log(R/eps)


def edge_term(area, measure):
    """2 ln mu(k*) at k* = A / 16 pi (G = 1), minus the area term A/4 for the semigroup."""
    k = mp.mpf(area) / (16 * mp.pi)
    if measure == "SO(1,1)":
        return mp.mpf(0)
    if measure == "SL(2,R)":
        return 2 * mp.log(k * mp.tanh(mp.pi * k))
    if measure == "SL(2,C)":
        return 2 * mp.log(k ** 2)
    if measure == "semigroup":
        return 2 * mp.log(k * mp.sinh(2 * mp.pi * k)) - mp.mpf(area) / 4
    raise ValueError(measure)


def log_coefficient(measure, areas=(1e4, 1e5, 1e6, 1e7, 1e8)):
    """Fitted coefficient of ln a (A ~ a^2, so ln A = 2 ln a) of the edge term."""
    mp.mp.dps = 40
    xs = [mp.log(mp.sqrt(mp.mpf(A))) for A in areas]          # ln a
    ys = [edge_term(A, measure) for A in areas]
    n = len(xs)
    xb, yb = sum(xs) / n, sum(ys) / n
    slope = sum((x - xb) * (y - yb) for x, y in zip(xs, ys)) / sum((x - xb) ** 2 for x in xs)
    return slope


SHANNON_SHIFT = 1      # L2: ln(width in k) = ln(2 M dM) = ln a + const, a = 2M


def comparison():
    edge = {m: log_coefficient(m) for m in ("SO(1,1)", "SL(2,R)", "SL(2,C)", "semigroup")}
    table = {
        "Sen, pure gravity (universal)": float(sen_singlet()),
        "Sen, gravity + photon (the massless fields at BH scales)": float(sen_singlet(nV=1)),
        "SU(2) loop quantum gravity (Sen sec. 4)": float(SEN_LQG_SU2),
        "Edge counting, SO(1,1) boost only (spherical reduction)": float(edge["SO(1,1)"] + SHANNON_SHIFT),
        "Edge counting, SL(2,R) (Q7)": float(edge["SL(2,R)"] + SHANNON_SHIFT),
        "Edge counting, SL(2,C) simple series (frame's full orbit)": float(edge["SL(2,C)"] + SHANNON_SHIFT),
        "Edge counting, causal semigroup (Varrin)": float(edge["semigroup"] + SHANNON_SHIFT),
    }
    return table, edge


def main():
    banner("Benchmarks (LIT)")
    print(f"   Sen C_local, pure gravity: {sen_c_local()} = 212/45; singlet ensemble: {sen_singlet()} = 77/45")
    print(f"   Sen, SU(2) loop quantum gravity, same ensemble: {SEN_LQG_SU2}")
    print(f"   David-Mukherjee, graviton edge sectors (flat sphere, log R/eps): {DAVID_MUKHERJEE_GRAVITON_EDGE}")

    banner("L1-L2  Edge-counting logarithms, converted to Sen's ensemble (CHECK)")
    table, edge = comparison()
    for m, v in edge.items():
        print(f"   Edge term 2 <ln mu>, {m:9s}: {mp.nstr(v, 8)} x ln a")
    print(f"   Shannon term at a fixed mass window (exact): +{SHANNON_SHIFT} x ln a")

    banner("L3  Coefficient of ln a, all in Sen's singlet ensemble")
    for k, v in table.items():
        print(f"   {k:62s} {v:+.4f}")
    print("   Edge counting gives 1, 5 or 9 depending on the group; Sen's universal value is")
    print("   77/45 = 1.711 for pure gravity, 64/45 = 1.422 with the photon, and depends on the")
    print("   massless fields. None of the edge countings does. The frame's log is not it.")
    print("   FOLLOWS: Sen's coefficient comes from one-loop bulk determinants and zero modes,")
    print("   the same in TEGR and GR. It stays the same only if the frame is gauge in the")
    print("   measure; counting the frame's orbit states as physical would add to it.")


if __name__ == "__main__":
    main()
