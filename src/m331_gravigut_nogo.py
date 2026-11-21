#!/usr/bin/env python3
"""
Can stage 1's 3-3-1 gauge theory and stage 7's gravity gauge theory come from one group?

Stage 1 of the merged simulation (src/chain_first_principles.py) is SU(3)_C x SU(3)_L x U(1)_X
with the fermions of the blind build's stage `running` (_fields_331). Stage 7 is gravity as a
broken SO(1,4) gauge theory (MacDowell-Mansouri). This script asks whether a derivation of
the second from the first exists, and answers with theorems and an exhaustive scan.

N1  Breaking cannot do it (CHECK). Breaking leaves a subgroup. Every subalgebra of a compact
    Lie algebra is compact (negative-definite trace form), and so(1,4) has 4 generators with
    tr(X X) > 0 in its defining representation (the three boosts and the time translation, all
    non-compact). So so(1,4), and so(1,3) with its boosts, is not a subalgebra of su(3)+su(3)+u(1).
N2  Stage 1's fermions (CHECK). 66 left-handed Weyl components for beta = -1/sqrt3, 69 for
    +1/sqrt3, and the three families are not copies of one representation: one quark family is
    an SU(3)_L triplet, two are antitriplets, and the anomaly cancels only across all three.
    So the template of the SO(10) graviGUTs, one family in one spinor, cannot apply: the whole
    chiral content has to come from one representation (or come with mirror partners).
N3  The graviGUT route (LIT + CHECK). Nesti and Percacci (PRD 81, 025010 (2010),
    arXiv:0909.4537) and Konitopoulos, Roumelioti and Zoupanos (Fortschr. Phys. 2023,
    arXiv:2309.15892; conformal and (A)dS version arXiv:2403.17511) put the Lorentz (or de
    Sitter) group and an internal SO(N) in SO(p, q) and break it to their product, with the
    fermions in one Majorana-Weyl spinor. A Majorana-Weyl spinor exists for p - q = 0 mod 8
    (standard; their SO(3,11) and SO(1,17) are of this kind), so with signature (1, 3 + N) the
    internal SO(N) needs N = 6 mod 8. Then SU(3)_C x SU(3)_L acts on the vector of SO(N) as
    V = R + conj(R) plus real pieces. Proved and checked by scan here:
      (a) a zero weight in V (a singlet, an adjoint) makes the two halves of the spinor equal
          under SU(3) x SU(3): no chirality;
      (b) with no zero weight, conj(Lambda^k R) = Lambda^(d-k) R (d = dim R), so the spinor is
          chiral only if d is odd;
      (c) representations without a zero weight have non-zero triality, so d = 0 mod 3.
    With N = 2d = 6 mod 8: d = 3 mod 12, and both SU(3)s act faithfully only from d = 15.
N4  The scan (CHECK). Every embedding at d = 15 (SO(30), the smallest allowed) and at d = 9
    (SO(18), no Majorana condition, so every fermion comes twice): none has stage 1's chiral content. Each one
    that is chiral carries chiral colour sextets, 15-plets and other exotics, at least 49
    multiplets at d = 15; they cannot be paired off and given mass, and they would destroy
    stage 1's Landau-pole selection of N_c = 3. The minimal embedding (SO(12), SO(14) via
    6 = (3,1) + (1,3)) is vectorlike: every (3,3) comes with a (3bar,3bar).
N5  Supersymmetry (LIT + CHECK, counting only). The Haag-Lopuszanski-Sohnius theorem leaves
    supersymmetry as the one way to mix spacetime and internal symmetry. N = 8 supergravity's
    SU(8) contains SU(3) x SU(3) x U(1) (8 = (3,1) + (1,3) + 1 + 1), but it has 56 spin-1/2
    states: fewer than stage 1's 66 or 69.
Not covered: non-orthogonal parents (exceptional real forms other than E8, for which Distler
and Garibaldi, Commun. Math. Phys. 298, 419 (2010), arXiv:0905.2658, prove that no real form
holds gravity and chiral matter together), supergroups beyond the count of N5, and
Kaluza-Klein constructions.
Labels: CHECK (computed here), LIT (quoted).
Standard library only. About 5 s.
"""
import itertools
import os
import sys
from collections import Counter
from fractions import Fraction
from functools import lru_cache

_CFP = globals().get("CFP")                     # an embedded copy (src/gravity_from_331.py) is handed CFP
if _CFP is None:                                # as a repository script: the merged simulation's blind-build stages
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import chain_first_principles as _CFP

gauge331, running = _CFP.gauge331, _CFP.running
VARIANTS = gauge331.VARIANTS


def banner(s):
    print("\n" + "=" * 78 + "\n" + s + "\n" + "=" * 78)


# ------------------------------------------------------------------------------------- N1
def so14_trace_signs():
    """tr(X X) for the 10 generators M_ij of so(1,4) in its defining representation, metric
    diag(-1, 1, 1, 1, 1): (M_ij)^a_b = delta^a_i eta_jb - delta^a_j eta_ib."""
    eta = [-1, 1, 1, 1, 1]
    signs = []
    for i, j in itertools.combinations(range(5), 2):
        X = [[0] * 5 for _ in range(5)]
        X[i][j], X[j][i] = eta[j], -eta[i]
        tr = sum(X[a][b] * X[b][a] for a in range(5) for b in range(5))
        signs.append(((i, j), tr))
    return signs


# ------------------------------------------------------------------------------------- N2
def conj(r):
    return {"1": "1", "3": "3b", "3b": "3"}[r]


def stage1_content(variant):
    """Left-handed Weyl multiplets (colour, SU(3)_L, X) -> number, from stage 1's running._fermion_triplets
    (leptons first, then the quark triplet and antitriplet families) and gauge331.triplet_charges."""
    out = Counter()
    rows = running._fermion_triplets(3, variant)
    for k, (mult, X, anti) in enumerate(rows):
        quark = k > 0
        fam = int(mult // 3) if quark else int(mult)
        col = "3" if quark else "1"
        out[(col, "3b" if anti else "3", X)] += fam
        for q in gauge331.triplet_charges(X, variant, anti=anti):
            if q != 0:
                out[(conj(col), "1", -q)] += fam
    return out


def weyl_components(content):
    d = {"1": 1, "3": 3, "3b": 3}
    return sum(n * d[c] * d[l] for (c, l, _), n in content.items())


def quark_families(variant):
    """The SU(3)_L representation of each quark family, from the stage's family split."""
    Ng, nA, nT = gauge331._families(3)
    return ["3"] * int(nT) + ["3b"] * int(nA)


# ------------------------------------------------------------------------------------- SU(3) characters
W3 = ((1, 0), (-1, 1), (0, -1))
W3B = tuple((-a, -b) for a, b in W3)


def _sym(p, W):
    c = Counter()
    for combo in itertools.combinations_with_replacement(range(3), p):
        c[(sum(W[i][0] for i in combo), sum(W[i][1] for i in combo))] += 1
    return c


@lru_cache(maxsize=None)
def char(p, q):
    """Weights (Dynkin basis) of the SU(3) irrep (p, q): Sym^p 3 x Sym^q 3bar minus its trace."""
    def prod(a, b):
        c = Counter()
        for x, m in a.items():
            for y, n in b.items():
                c[(x[0] + y[0], x[1] + y[1])] += m * n
        return c
    c = prod(_sym(p, W3), _sym(q, W3B))
    if p and q:
        c = c - prod(_sym(p - 1, W3), _sym(q - 1, W3B))
    return tuple(sorted(c.items()))


def weights(R):
    (c, l) = R
    return [wc + wl for wc, a in char(*c) for _ in range(a) for wl, b in char(*l) for _ in range(b)]


def cj(r):
    return (r[1], r[0])


def spinor(pieces, zero_pairs=0):
    """The two Weyl halves of the SO(2 sum dim R) spinor for V = sum (R + conj R) [+ zero_pairs
    zero-weight pairs], as characters of SU(3) x SU(3). Weights are stored doubled."""
    cur = Counter({((0, 0, 0, 0), 0): 1})
    for p in (w for R in pieces for w in weights(R)):
        nxt = Counter()
        for (w, par), m in cur.items():
            nxt[(tuple(a + b for a, b in zip(w, p)), par)] += m
            nxt[(tuple(a - b for a, b in zip(w, p)), par ^ 1)] += m
        cur = nxt
    half = [Counter(), Counter()]
    for (w, par), m in cur.items():
        half[par][w] += m
    if zero_pairs:                      # a zero-weight pair flips the chirality without changing the weight
        tot = half[0] + half[1]
        half = [Counter({k: v * 2 ** (zero_pairs - 1) for k, v in tot.items()})] * 2
    return half


def decompose(ch):
    """Irreps ((p,q)_C, (p,q)_L) -> multiplicity, by peeling off highest weights."""
    ch = Counter({k: v for k, v in ch.items() if v})
    irr = Counter()
    while ch:
        hw = max(ch, key=lambda w: 1e6 * (w[0] + w[1] + 0.01 * w[0]) + (w[2] + w[3] + 0.01 * w[2]))
        m = ch[hw]
        c, l = (hw[0] // 2, hw[1] // 2), (hw[2] // 2, hw[3] // 2)
        irr[(c, l)] += m
        for wc, a in char(*c):
            for wl, b in char(*l):
                k = (2 * wc[0], 2 * wc[1], 2 * wl[0], 2 * wl[1])
                ch[k] -= m * a * b
                if ch[k] < 0:
                    raise ArithmeticError("not a character")
                if ch[k] == 0:
                    del ch[k]
    return irr


def chiral_index(irr):
    """n(R) - n(conj R) for every R with a positive excess: empty means vectorlike."""
    return {k: irr[k] - irr[(cj(k[0]), cj(k[1]))] for k in irr if irr[k] > irr[(cj(k[0]), cj(k[1]))]}


NAME = {"1": (0, 0), "3": (1, 0), "3b": (0, 1)}


def stage1_index(variant):
    """Stage 1's chiral index under SU(3)_C x SU(3)_L alone."""
    irr = Counter()
    for (c, l, _), n in stage1_content(variant).items():
        irr[(NAME[c], NAME[l])] += n
    return chiral_index(irr)


# ------------------------------------------------------------------------------------- N3, N4
def no_zero_weight_irreps(dmax):
    out, seen = [], set()
    for c in ((0, 0), (1, 0), (2, 0), (2, 1), (4, 0)):
        for l in ((0, 0), (1, 0), (0, 1), (2, 0), (0, 2), (2, 1), (1, 2), (4, 0), (0, 4)):
            R = (c, l)
            w = weights(R)
            key = frozenset([R, (cj(c), cj(l))])
            if len(w) <= dmax and all(any(x) for x in w) and key not in seen:
                seen.add(key)
                out.append((len(w), R))
    return out


def embeddings(d):
    """Every V = R + conj R with dim R = d, no zero weight, both SU(3)s acting; the relative
    orientation of the pieces matters, the overall one does not."""
    base = no_zero_weight_irreps(d)
    res = []

    def rec(start, left, acc):
        if left == 0:
            res.append(list(acc))
            return
        for i in range(start, len(base)):
            if base[i][0] <= left:
                rec(i, left - base[i][0], acc + [base[i][1]])
    rec(0, d, [])
    seen = set()
    for pc in res:
        if not (any(R[0] != (0, 0) for R in pc) and any(R[1] != (0, 0) for R in pc)):
            continue
        for signs in itertools.product((0, 1), repeat=len(pc) - 1):
            P = [pc[0]] + [R if s == 0 else (cj(R[0]), cj(R[1])) for R, s in zip(pc[1:], signs)]
            key = tuple(sorted(P))
            if key not in seen:
                seen.add(key)
                yield P


SMALL = {(0, 0), (1, 0), (0, 1)}


def scan(d, targets):
    """For every embedding at this d and both halves: does the chiral index equal a target?
    Returns (embeddings, chiral halves, matches, fewest exotic chiral multiplets, that embedding)."""
    n = chiral = 0
    matches, best = [], None
    for P in embeddings(d):
        n += 1
        for half in spinor(P):
            idx = chiral_index(decompose(half))
            if idx:
                chiral += 1
                exotic = sum(v for (c, l), v in idx.items() if c not in SMALL or l not in SMALL)
                if best is None or exotic < best[0]:
                    best = (exotic, P)
            if any(idx == t for t in targets):
                matches.append(P)
    return n, chiral, matches, best


def majorana_weyl(p, q):
    return (p - q) % 8 == 0


def allowed_d(dmax=40):
    """d = dim R with: d odd (b), d = 0 mod 3 (c), and 2d = 6 mod 8 (Majorana-Weyl in SO(1, 3 + 2d))."""
    return [d for d in range(1, dmax + 1) if d % 2 == 1 and d % 3 == 0 and majorana_weyl(1, 3 + 2 * d)]


# ------------------------------------------------------------------------------------- main
def main():
    res = {}
    banner("N1  Breaking 3-3-1 cannot leave gravity's group")
    s = so14_trace_signs()
    pos = [g for g, t in s if t > 0]
    neg = [g for g, t in s if t < 0]
    res["so14"] = (len(pos), len(neg))
    print(f"   so(1,4), defining representation: tr(X X) > 0 for {len(pos)} generators {pos},"
          f" < 0 for {len(neg)}")
    print("   su(3)+su(3)+u(1) is compact: tr(X X) <= 0 on all of it and on every subalgebra.")
    print("   So so(1,4) (and its so(1,3)) is not a subalgebra: no breaking of stage 1 leaves it.  [CHECK]")

    banner("N2  Stage 1's fermions")
    for var in VARIANTS:
        c = stage1_content(var)
        res[("weyl", var)] = weyl_components(c)
        res[("index", var)] = stage1_index(var)
        print(f"   beta = {var}: {weyl_components(c)} left-handed Weyl components;"
              f" quark families in SU(3)_L: {quark_families(var)}")
        print("      " + ", ".join(f"({a},{b}){'+' if x >= 0 else ''}{x}: {n}" for (a, b, x), n in sorted(c.items())))
        print(f"      chiral index under SU(3)_C x SU(3)_L: {stage1_index(var)}")
    print("   The families are not copies of one representation: the content must come whole, from one")
    print("   representation, or with mirror partners.  [CHECK]")

    banner("N3  The graviGUT conditions, checked")
    h0, h1 = spinor([((1, 0), (0, 0))])
    res["so6"] = (dict(decompose(h0)), dict(decompose(h1)))
    print(f"   sanity, SO(6) > SU(3): the two Weyl spinors are {dict(decompose(h0))} and {dict(decompose(h1))}"
          " (4 = 3 + 1, chiral)")
    mini = [chiral_index(decompose(h)) for h in spinor([((1, 0), (0, 0)), ((0, 0), (1, 0))], zero_pairs=1)]
    mini12 = [chiral_index(decompose(h)) for h in spinor([((1, 0), (0, 0)), ((0, 0), (1, 0))])]
    res["minimal"] = (mini12, mini)
    print(f"   (a)+(b), the minimal embedding 6 = (3,1) + (1,3): SO(12) index {mini12}, SO(14) index {mini}: vectorlike")
    even = [chiral_index(decompose(h)) for h in spinor([((1, 0), (0, 0)), ((0, 0), (1, 0)), ((1, 0), (1, 0)),
                                                        ((1, 0), (0, 0))])]
    res["even_d"] = even
    print(f"   (b), an even d = 18 example V = (3,1)+(1,3)+(3,3)+(3,1): index {even}: vectorlike")
    ad = allowed_d()
    res["allowed_d"] = ad
    print(f"   d odd, d = 0 mod 3 and Majorana-Weyl in SO(1, 3 + 2d): d = {ad} -> smallest SO(N) with N = {2 * ad[0]}"
          f" ({2 * ad[0]} needs one SU(3) only; both act faithfully from d = {ad[1]}, SO({2 * ad[1]}))  [CHECK]")

    banner("N4  Every embedding at d = 15 (SO(30)) and d = 9 (SO(18), doubled fermions)")
    targets = []
    for var in VARIANTS:
        t = res[("index", var)]
        targets += [t, {(cj(a), cj(b)): v for (a, b), v in t.items()}]
    # d = 9 has no Majorana-Weyl spinor: the left-handed content is two copies of one half, so
    # the question is whether one half carries stage 1's chiral index (the second copy would be extra)
    for d, tg in ((15, targets), (9, targets)):
        n, chiral, matches, best = scan(d, tg)
        res[("scan", d)] = (n, chiral, len(matches), best[0] if best else None)
        print(f"   d = {d:2d}: {n} embeddings, {chiral} chiral halves, {len(matches)} with stage 1's chiral content;"
              f" fewest exotic chiral multiplets {best[0] if best else '-'} (V = {best[1] if best else '-'})  [CHECK]")

    banner("N5  Supersymmetry, counting only")
    n8 = len(list(itertools.combinations(range(8), 3)))
    res["n8"] = n8
    print(f"   N = 8 supergravity: spin-1/2 in the 3-index antisymmetric of SU(8): {n8} states, against stage 1's"
          f" {res[('weyl', '-1/sqrt3')]} and {res[('weyl', '+1/sqrt3')]}  [CHECK; LIT for the multiplet]")

    banner("Summary")
    print("   No breaking of stage 1 gives gravity's gauge group (N1), and no orthogonal parent with one")
    print("   Majorana-Weyl spinor holds stage 1's chiral fermions without chiral exotics (N3, N4). Within these")
    print("   classes there is no derivation of stage 7 from stage 1. Open: non-orthogonal parents, supergroups")
    print("   beyond N5's count, Kaluza-Klein.")
    return res


if __name__ == "__main__":
    main()
