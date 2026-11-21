#!/usr/bin/env python3
"""
Is Newton's constant induced by stage 1's own matter, cut off at its U(1)_X Landau pole?

The test registered in INDUCED_GRAVITY_PREREG.md, computed as registered. Sakharov's induced
gravity at one loop with a proper-time cutoff kappa and no tree-level term, with the species
coefficients of M. Visser, Mod. Phys. Lett. A17 (2002) 977, arXiv:gr-qc/0204062, Table I (LIT):
    str[k1] = N_S (1/6 - xi) + N_W / 6 - 2 N_V / 3,
real scalars with coupling xi to R, Weyl fermions (k1 = -1/6, entering str with a minus sign),
massless gauge vectors with their ghosts (k1 = -2/3).
THE SIGN. The registration took 1/G = -(1/2 pi) str[k1] kappa^2 from Visser's eq. (21). That
sign is wrong in the standard convention (G > 0 attractive, Euclidean action -(1/16 pi G) int R):
W = (1/2) ln det D = -(1/2) int dt/t Tr exp(-tD) gives W > -(kappa^2/32 pi^2) int a1, so
    1/G = +(1/2 pi) str[k1] kappa^2,      M_Pl^2 = +str[k1] kappa^2 / (2 pi),
in agreement with F. Larsen and F. Wilczek, Nucl. Phys. B458 (1996) 249, arXiv:hep-th/9506066,
sec. 3.3 (1/G_ren = 1/G_bare + (1/2 pi)(1/6 - xi)/eps^2 for a scalar), and S. Solodukhin,
Living Rev. Rel. 14 (2011) 8, arXiv:1104.3712, eqs. (115), (137), (141) (scalars and Dirac
fermions positive). Both are computed below: I2-I5 as registered (wrong sign), I6 corrected.

I1  The species counts, from stage 1 (CHECK): N_V = 17 generators; N_W and N_S from the blind
    build's running._fields_331.
I2  str[k1] at the two structural values xi = 0 (minimal) and xi = 1/6 (conformal), both variants.
I3  Where str[k1] < 0: the cutoff needed to give the measured M_Pl, against the one-loop and
    three-loop Landau poles; the band of the registration is [1/3, 3].
I4  The xi that would be needed, reported as a fit.
I5  The verdict, by the registration's table, with the registered (wrong) sign.
I6  The same table with the corrected sign. Nothing else changed: same xi values, band, variant test.
I7  What the corrected relation predicts: M_Pl, and G, from stage 1 alone (MODEL).
I8  Not registered, reported for what it is: the cosmological constant the same loop induces,
    and the N_c = 5 content at its own pole.
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
BAND = (Fraction(1, 3), Fraction(3))       # registered


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


def str_k1(variant, xi):
    n_v, n_w, n_s = counts(variant)
    xi = Fraction(xi)
    return n_s * (K1["scalar"] - xi) - n_w * K1["weyl"] + n_v * K1["vector"]


def xi_for(variant, target_str):
    """The xi at which str[k1] equals target_str."""
    n_v, n_w, n_s = counts(variant)
    return Fraction(1, 6) + (str_k1(variant, 0) - Fraction(1, 6) * n_s - target_str) / n_s


def poles(variant):
    return {"one loop": running.landau_pole(3, variant), "three loops": inputs.POLES_331[variant][0]}


def mpl():
    return links.planck_mass_GeV(inputs.G_NEWTON, inputs.HBAR, inputs.C_LIGHT)


def kappa_needed(s, sign=-1):
    """kappa giving the measured M_Pl, for sign * str[k1] = s > 0 (sign = -1: as registered; +1: corrected)."""
    return mpl() * math.sqrt(2 * math.pi / (sign * float(s)))


def str_for_kappa(kappa, sign=-1):
    """str[k1] that a cutoff kappa needs: sign * 2 pi (M_Pl/kappa)^2."""
    return sign * 2 * math.pi * (mpl() / kappa) ** 2


def verdict(variant, sign=-1):
    rows = []
    for xi in (Fraction(0), Fraction(1, 6)):
        s = str_k1(variant, xi)
        if sign * s <= 0:
            rows.append((xi, s, None, False))
            continue
        k = kappa_needed(s, sign)
        ratios = {name: k / p for name, p in poles(variant).items()}
        ok = any(float(BAND[0]) <= r <= float(BAND[1]) for r in ratios.values())
        rows.append((xi, s, ratios, ok))
    return rows


def mpl_induced(variant, xi, pole):
    """Corrected relation: M_Pl = pole sqrt(str[k1] / 2 pi), or None if str[k1] <= 0."""
    s = str_k1(variant, xi)
    return pole * math.sqrt(float(s) / (2 * math.pi)) if s > 0 else None


def str_k0(variant, Nc=3):
    """str of the heat-kernel a0 (degrees of freedom, bosons minus fermions): the kappa^4 term."""
    n_v, n_w, n_s = counts(variant, Nc)
    return n_s + 2 * n_v - 2 * n_w


def counts_nc(variant, Nc):
    n_v = (Nc * Nc - 1) + 8 + 1
    n_w = n_s = 0
    for kind, mult, dim, _ in running._fields_331(Nc, variant):
        if kind == "weyl":
            n_w += int(mult) * dim
        else:
            n_s += 2 * int(mult) * dim
    return n_v, n_w, n_s


def table(sign):
    sel = verdict(SELECTED, sign)
    other = [v for v in VARIANTS if v != SELECTED][0]
    passed = any(ok for *_, ok in sel)
    other_passes = any(ok for *_, ok in verdict(other, sign))
    if passed and not other_passes:
        out = "PASS (prediction)"
    elif passed:
        out = "PASS for both variants: the test does not discriminate"
    else:
        out = "FAIL at the structural xi values; CONDITIONAL (fit) only, see I4"
    return sel, other, other_passes, out


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
        for xi in (Fraction(0), Fraction(1, 6)):
            s = str_k1(var, xi)
            res[("str", var, xi)] = s
            print(f"   beta = {var:8s}, xi = {str(xi):3s}: str[k1] = {str(s):6s} = {float(s):+.4f}"
                  f"  ->  1/G {'> 0' if s < 0 else '<= 0: no positive G'}")

    banner("I3  The cutoff the measured G needs, against the U(1)_X pole")
    print(f"   M_Pl = {M:.5e} GeV; band of the registration: kappa_needed / pole in [1/3, 3]")
    for var in VARIANTS:
        for name, p in poles(var).items():
            print(f"   beta = {var:8s} {name:11s} pole {p:.4e} GeV = {p / M:.3g} M_Pl:"
                  f" a cutoff there needs str[k1] = {str_for_kappa(p):+.3g}")
        for xi, s, ratios, ok in verdict(var):
            if ratios is None:
                print(f"      xi = {str(xi):3s}: no positive G")
            else:
                print(f"      xi = {str(xi):3s}: kappa_needed = {kappa_needed(s):.3e} GeV;"
                      + "; ".join(f" / {n} pole = {r:.3g}" for n, r in ratios.items()) + f"  -> in band: {ok}")
        res[("verdict", var)] = verdict(var)

    banner("I4  The xi a fit would need (CONDITIONAL: xi is then a new parameter traded for G)")
    for var in VARIANTS:
        for name, p in poles(var).items():
            need = Fraction(str_for_kappa(p)).limit_denominator(10 ** 9)
            x = xi_for(var, need)
            lo = xi_for(var, Fraction(str_for_kappa(p / float(BAND[0]))).limit_denominator(10 ** 9))
            hi = xi_for(var, Fraction(str_for_kappa(p / float(BAND[1]))).limit_denominator(10 ** 9))
            res[("xi_fit", var, name)] = float(x)
            print(f"   beta = {var:8s}, {name:11s}: xi = {float(x):.4f} (band: {float(min(lo, hi)):.4f} to"
                  f" {float(max(lo, hi)):.4f})")

    banner("I5  Verdict, by the registered table, with the registered sign (shown to be wrong in I6)")
    sel, other, other_passes, out = table(-1)
    res["verdict"] = out
    for xi, s, ratios, ok in sel:
        why = "str[k1] >= 0: wrong-sign or infinite G" if ratios is None else ("in band" if ok else "outside the band")
        print(f"   selected beta = {SELECTED}, xi = {xi}: {why}")
    print(f"   the other variant (beta = {other}) passes the band: {other_passes}")
    print(f"   VERDICT (registered sign): {out}")

    banner("I6  Corrected sign, 1/G = +(1/2 pi) str[k1] kappa^2: the registered table otherwise unchanged")
    for var in VARIANTS:
        for xi, s, ratios, ok in verdict(var, +1):
            if ratios is None:
                print(f"   beta = {var:8s}, xi = {str(xi):3s}: str[k1] = {float(s):+.4f}: no positive G")
            else:
                print(f"   beta = {var:8s}, xi = {str(xi):3s}: str[k1] = {float(s):+.4f}, kappa_needed ="
                      f" {kappa_needed(s, +1) / M:.3f} M_Pl;" + ";".join(f" / {n} pole = {r:.3g}" for n, r in ratios.items())
                      + f"  -> in band: {ok}")
        res[("verdict_corrected", var)] = verdict(var, +1)
    sel, other, other_passes, out = table(+1)
    res["verdict_corrected"] = out
    print(f"   VERDICT (corrected sign): {out}")
    print("   Caveat: the sign was corrected after the registered computation, from the literature above;")
    print("   the pass comes from that correction and carries less weight than a pass as first registered.")

    banner("I7  What it predicts: M_Pl = pole sqrt(str[k1]/2 pi) for the selected variant (MODEL)")
    preds = []
    for xi in (Fraction(0), Fraction(1, 6)):
        for name, p in poles(SELECTED).items():
            m = mpl_induced(SELECTED, xi, p)
            preds.append(m)
            print(f"   xi = {str(xi):3s}, {name:11s} pole: M_Pl = {m:.3e} GeV = {m / M:.2f} x measured;"
                  f" G = {(M / m) ** 2:.2f} x measured")
    res["mpl_range"] = (min(preds) / M, max(preds) / M)
    print(f"   range: M_Pl {min(preds) / M:.2f} to {max(preds) / M:.2f} x measured, G {(M / max(preds)) ** 2:.2f} to"
          f" {(M / min(preds)) ** 2:.1f} x measured: an order-of-magnitude prediction of G from stage 1 alone")
    print("   and the selection of N_c = 3 stays consistent: M_Pl = pole_3 sqrt(str/2 pi) < pole_3 because str < 2 pi")

    banner("I8  Not registered: the cosmological term, and N_c = 5")
    for var in VARIANTS:
        k0 = str_k0(var)
        res[("str_k0", var)] = k0
        print(f"   beta = {var:8s}: str[1] = N_S + 2 N_V - 2 N_W = {k0}: the same loop induces a vacuum energy of order"
              f" str[1] kappa^4/(32 pi^2) ~ (10^19 GeV)^4, 10^122 times the measured one. Not solved here")
    n5 = counts_nc(SELECTED, 5)
    s5 = n5[2] * Fraction(1, 6) + Fraction(n5[1], 6) - Fraction(2, 3) * n5[0]
    p5 = running.landau_pole(5, SELECTED)
    m5 = p5 * math.sqrt(float(s5) / (2 * math.pi)) if s5 > 0 else None
    res["nc5"] = (n5, s5, m5)
    print(f"   N_c = 5, beta = {SELECTED}: N_V, N_W, N_S = {n5}, str[k1](xi=0) = {float(s5):+.3f}, pole {p5:.2e} GeV:"
          + (f" induced M_Pl = {m5:.2e} GeV = {m5 / M:.1e} x measured" if m5 else " no positive G"))
    return res


if __name__ == "__main__":
    main()
