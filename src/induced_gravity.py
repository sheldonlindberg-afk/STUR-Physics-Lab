#!/usr/bin/env python3
"""
Is Newton's constant induced by stage 1's own matter, cut off at its U(1)_X Landau pole?

The test of INDUCED_GRAVITY.md. Sakharov's induced gravity at one loop, with a proper-time
cutoff kappa and no tree-level term. In the standard convention (G > 0 attractive, Euclidean
action -(1/16 pi G) int sqrt(g) R), W = (1/2) ln det D = -(1/2) int_{1/kappa^2} dt/t Tr exp(-tD)
contains -(kappa^2/32 pi^2) int sqrt(g) a1, so
    1/G = (1/2 pi) str[k1] kappa^2,     M_Pl^2 = str[k1] kappa^2 / (2 pi),
    str[k1] = N_S (1/6 - xi) + N_W / 6 - 2 N_V / 3,
for real scalars with coupling xi to R, Weyl fermions and massless gauge vectors with their
ghosts. LIT: the species coefficients are M. Visser's, Mod. Phys. Lett. A17 (2002) 977,
arXiv:gr-qc/0204062, Table I. The scalar formula is that of F. Larsen and F. Wilczek, Nucl. Phys.
B458 (1996) 249, arXiv:hep-th/9506066, sec. 3.3; the positive scalar and Dirac terms are those of
S. Solodukhin, Living Rev. Rel. 14 (2011) 8, arXiv:1104.3712, eqs. (115), (137), (141).

I1  The species counts, from stage 1 (CHECK): N_V = 17 generators; N_W and N_S from the blind
    build's running._fields_331.
I2  str[k1] at the two structural values xi = 0 (minimal) and xi = 1/6 (conformal), both variants.
I3  The cutoff the measured M_Pl needs, against the one-loop and three-loop Landau poles; the
    band fixed before computing is [1/3, 3].
I4  The verdict, by the table fixed before computing.
I5  What it predicts: M_Pl, and G, from stage 1 alone (MODEL).
I6  Beyond the test: the cosmological constant the same loop induces, and the N_c = 5 content.
Labels: CHECK (computed), LIT (quoted), MODEL (the hypothesis).
Standard library only. Under a second.
"""
import math
import os
import sys
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import chain_first_principles as CFP

inputs, running, links, gauge331 = CFP.inputs, CFP.running, CFP.links, CFP.gauge331
VARIANTS = gauge331.VARIANTS
SELECTED = "+1/sqrt3"                      # the variant stage 1 selects N_c = 3 with
K1 = {"scalar": Fraction(1, 6), "weyl": Fraction(-1, 6), "vector": Fraction(-2, 3)}   # Visser Table I
BAND = (Fraction(1, 3), Fraction(3))       # fixed before computing
XIS = (Fraction(0), Fraction(1, 6))


def banner(s):
    print("\n" + "=" * 78 + "\n" + s + "\n" + "=" * 78)


def counts(variant, Nc=3):
    """(N_V, N_W, N_S) above the 3-3-1 scale: gauge generators of SU(N_c) x SU(3)_L x U(1)_X, left-handed Weyl
    components and real scalar components of stage 1's field list."""
    n_v = (Nc * Nc - 1) + 8 + 1
    n_w = n_s = 0
    for kind, mult, dim, _ in running._fields_331(Nc, variant):
        if kind == "weyl":
            n_w += int(mult) * dim
        else:
            n_s += 2 * int(mult) * dim          # complex triplets: two real components each
    return n_v, n_w, n_s


def str_k1(variant, xi, Nc=3):
    """sum over species of k1, fermions with a minus sign (Weyl k1 = -1/6 enters as +1/6)."""
    n_v, n_w, n_s = counts(variant, Nc)
    return n_s * (K1["scalar"] - Fraction(xi)) - n_w * K1["weyl"] + n_v * K1["vector"]


def str_k0(variant, Nc=3):
    """str of the heat-kernel a0 (degrees of freedom, bosons minus fermions): the kappa^4 term."""
    n_v, n_w, n_s = counts(variant, Nc)
    return n_s + 2 * n_v - 2 * n_w


def poles(variant):
    return {"one loop": running.landau_pole(3, variant), "three loops": inputs.POLES_331[variant][0]}


def mpl():
    return links.planck_mass_GeV(inputs.G_NEWTON, inputs.HBAR, inputs.C_LIGHT)


def kappa_needed(s):
    """The cutoff giving the measured M_Pl, for str[k1] = s > 0."""
    return mpl() * math.sqrt(2 * math.pi / float(s))


def str_for_kappa(kappa):
    """str[k1] that a cutoff kappa needs: 2 pi (M_Pl/kappa)^2."""
    return 2 * math.pi * (mpl() / kappa) ** 2


def mpl_induced(variant, xi, pole, Nc=3):
    """M_Pl = pole sqrt(str[k1] / 2 pi), or None if str[k1] <= 0."""
    s = str_k1(variant, xi, Nc)
    return pole * math.sqrt(float(s) / (2 * math.pi)) if s > 0 else None


def verdict(variant):
    """Per structural xi: (xi, str[k1], {pole: kappa_needed/pole} or None, in band)."""
    rows = []
    for xi in XIS:
        s = str_k1(variant, xi)
        if s <= 0:
            rows.append((xi, s, None, False))
            continue
        ratios = {name: kappa_needed(s) / p for name, p in poles(variant).items()}
        rows.append((xi, s, ratios, any(float(BAND[0]) <= r <= float(BAND[1]) for r in ratios.values())))
    return rows


def table():
    other = [v for v in VARIANTS if v != SELECTED][0]
    passed = any(ok for *_, ok in verdict(SELECTED))
    other_passes = any(ok for *_, ok in verdict(other))
    if passed and not other_passes:
        return other, other_passes, "PASS (prediction)"
    if passed:
        return other, other_passes, "PASS for both variants: the test does not discriminate"
    return other, other_passes, "FAIL at the structural xi values"


def main():
    res = {}
    M = mpl()
    banner("I1  Species above the 3-3-1 scale, from stage 1")
    for var in VARIANTS:
        res[("counts", var)] = counts(var)
        n_v, n_w, n_s = counts(var)
        print(f"   beta = {var:8s}: N_V = {n_v} vectors, N_W = {n_w} Weyl fermions, N_S = {n_s} real scalars")
    print("   (graviton loop not included: Sakharov's gravity is not quantized)")

    banner("I2  str[k1] = N_S (1/6 - xi) + N_W/6 - 2 N_V/3   [LIT coefficients, Visser Table I]")
    for var in VARIANTS:
        for xi in XIS:
            s = str_k1(var, xi)
            res[("str", var, xi)] = s
            print(f"   beta = {var:8s}, xi = {str(xi):3s}: str[k1] = {str(s):6s} = {float(s):+.4f}"
                  f"  ->  1/G {'> 0' if s > 0 else '<= 0: no positive G'}")

    banner("I3  The cutoff the measured G needs, against the U(1)_X pole")
    print(f"   M_Pl = {M:.5e} GeV; band fixed before computing: kappa_needed / pole in [1/3, 3]")
    for var in VARIANTS:
        for name, p in poles(var).items():
            print(f"   beta = {var:8s} {name:11s} pole {p:.4e} GeV = {p / M:.3g} M_Pl:"
                  f" a cutoff there needs str[k1] = {str_for_kappa(p):.3g}")
        for xi, s, ratios, ok in verdict(var):
            if ratios is None:
                print(f"      xi = {str(xi):3s}: no positive G")
            else:
                print(f"      xi = {str(xi):3s}: kappa_needed = {kappa_needed(s) / M:.3f} M_Pl;"
                      + ";".join(f" / {n} pole = {r:.3g}" for n, r in ratios.items()) + f"  -> in band: {ok}")
        res[("verdict", var)] = verdict(var)

    banner("I4  Verdict")
    other, other_passes, out = table()
    res["verdict"] = out
    for xi, s, ratios, ok in verdict(SELECTED):
        print(f"   selected beta = {SELECTED}, xi = {xi}: " + ("no positive G" if ratios is None else
                                                              ("in band" if ok else "outside the band")))
    print(f"   the other variant (beta = {other}) passes the band: {other_passes}")
    print(f"   VERDICT: {out}")

    banner("I5  What it predicts: M_Pl = pole sqrt(str[k1]/2 pi) for the selected variant (MODEL)")
    preds = []
    for xi in XIS:
        for name, p in poles(SELECTED).items():
            m = mpl_induced(SELECTED, xi, p)
            preds.append(m)
            print(f"   xi = {str(xi):3s}, {name:11s} pole: M_Pl = {m:.3e} GeV = {m / M:.2f} x measured;"
                  f" G = {(M / m) ** 2:.2f} x measured")
    res["mpl_range"] = (min(preds) / M, max(preds) / M)
    print(f"   range: M_Pl {min(preds) / M:.2f} to {max(preds) / M:.2f} x measured, G {(M / max(preds)) ** 2:.2f} to"
          f" {(M / min(preds)) ** 2:.1f} x measured: an order-of-magnitude prediction of G from stage 1 alone")
    print("   and the selection of N_c = 3 stays consistent: M_Pl = pole_3 sqrt(str/2 pi) < pole_3 because str < 2 pi")

    banner("I6  Beyond the test: the cosmological term, and N_c = 5")
    for var in VARIANTS:
        k0 = str_k0(var)
        res[("str_k0", var)] = k0
        print(f"   beta = {var:8s}: str[1] = N_S + 2 N_V - 2 N_W = {k0}: the same loop induces a vacuum energy of order"
              f" str[1] kappa^4/(32 pi^2) ~ (10^19 GeV)^4, 10^122 times the measured one. Not solved here")
    n5 = counts(SELECTED, 5)
    s5 = str_k1(SELECTED, 0, 5)
    p5 = running.landau_pole(5, SELECTED)
    m5 = mpl_induced(SELECTED, 0, p5, 5)
    res["nc5"] = (n5, s5, m5)
    print(f"   N_c = 5, beta = {SELECTED}: N_V, N_W, N_S = {n5}, str[k1](xi=0) = {float(s5):+.3f}, pole {p5:.2e} GeV:"
          + (f" induced M_Pl = {m5:.2e} GeV = {m5 / M:.1e} x measured" if m5 else " no positive G"))
    return res


if __name__ == "__main__":
    main()
