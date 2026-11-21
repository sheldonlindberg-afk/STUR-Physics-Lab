"""Bosonic one-loop transverse self-energies of gamma, Z, W in the 't Hooft-Feynman gauge (SPEC.md).

Derivation (see DERIVATION.md): the Lagrangian of SPEC section 1 is written in real mass-basis component fields,
every vertex is extracted from it mechanically (all leg permutations, d -> -i p), the one-loop 1PI two-point
functions are summed with the real-field symmetry factors, contracted with g_{mu nu} and k_mu k_nu, reduced to
A0 / B0 in d dimensions, the O(eps) parts of the d-dependent coefficients are kept against the pole (MS-bar), and
B0(k^2) is split as B0(0) + k^2 Bbar(k^2) so that the k^2 -> 0 limit is manifest.

The symbolic derivation runs once (lazily, cached) with sympy; the numerics use mpmath with a precision set locally
inside each export (mp.workdps).
"""
import itertools
import math

import mpmath as mp
import sympy as sp

# --------------------------------------------------------------------------------------------------------------
# symbols
# --------------------------------------------------------------------------------------------------------------
g, cw = sp.symbols("g c_w", positive=True)
MW, MH = sp.symbols("M_W M_H", positive=True)
kk, qq, qk = sp.symbols("kk qq qk")
dd = sp.Symbol("d")
sw = sp.sqrt(1 - cw**2)
MZ = MW / cw
xi = sp.Integer(1)                      # 't Hooft-Feynman gauge
v = 2 * MW / g                          # M_W = g v / 2 (checked in _check_tree)
gp = g * sw / cw                        # g' = g s / c  (c = g / sqrt(g^2 + g'^2))

MASS2 = {"W": MW**2, "Z": MZ**2, "H": MH**2, "0": sp.Integer(0)}
LOG = {m: sp.Symbol("L_" + m) for m in ("W", "Z", "H")}           # L_m = ln(m^2/mu^2)

VNAMES = ("W1", "W2", "Z", "A")
SNAMES = ("phi1", "phi2", "H", "chi")
GNAMES = ("uW1", "uW2", "uZ", "uA")


# --------------------------------------------------------------------------------------------------------------
# group theory in the real mass basis (DERIVATION sections 1-2)
# --------------------------------------------------------------------------------------------------------------
def _group():
    eps = sp.LeviCivita
    # gauge basis a = 0,1,2 (W^1,2,3), 3 (B); f^{abc} = g eps^{abc}
    f_gauge = [[[g * eps(a, b, c) if max(a, b, c) < 3 else 0 for c in range(4)] for b in range(4)] for a in range(4)]
    tau = [sp.Matrix([[0, 1], [1, 0]]), sp.Matrix([[0, -sp.I], [sp.I, 0]]), sp.Matrix([[1, 0], [0, -1]])]
    gens = [(g / 2, t) for t in tau] + [(gp / 2, sp.eye(2))]       # T^a = coupling x numeric matrix

    def realify(Mc):                 # complex 2x2 map on z_j = (phi_{2j-1} + i phi_{2j})/sqrt2 -> real 4x4
        R = sp.zeros(4, 4)
        for i in range(2):
            for j in range(2):
                re, im = sp.re(Mc[i, j]), sp.im(Mc[i, j])
                R[2 * i, 2 * j], R[2 * i, 2 * j + 1] = re, -im
                R[2 * i + 1, 2 * j], R[2 * i + 1, 2 * j + 1] = im, re
        return R

    th_gauge = [cpl * realify(-sp.I * t) for cpl, t in gens]
    for t in th_gauge:
        assert sp.simplify(t + t.T) == sp.zeros(4, 4)
    # real scalar components (phi1, phi2, phi3, phi4) = (phi1, phi2, v + H, chi): reorder to (phi1, phi2, H, chi): identity
    # rotation W^gauge_a = O[a, alpha] V_alpha, V = (W1, W2, Z, A)
    O = sp.Matrix([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, cw, sw], [0, 0, -sw, cw]])
    assert sp.simplify(O.T * O) == sp.eye(4)
    f = [[[sp.simplify(sum(O[a, al] * O[b, be] * O[c, ga] * f_gauge[a][b][c]
                           for a in range(4) for b in range(4) for c in range(4)))
           for ga in range(4)] for be in range(4)] for al in range(4)]
    th = [sp.simplify(sum((O[a, al] * th_gauge[a] for a in range(4)), sp.zeros(4, 4))) for al in range(4)]
    u = sp.Matrix([0, 0, v, 0])
    return f, th, u


# --------------------------------------------------------------------------------------------------------------
# Lagrangian as monomials with explicit labels.  factor = (kind, label, lorentz_index or None, derivative_index or None)
# --------------------------------------------------------------------------------------------------------------
def _ren(pieces, ren):
    out = []
    for c, facs in pieces:
        out.append((c, [(k, l, ren.get(li, li), ren.get(di, di)) for (k, l, li, di) in facs]))
    return out


def _mul(A, B, pref=1):
    out = []
    for ca, fa in A:
        for cb, fb in B:
            c = sp.expand(pref * ca * cb)
            if c != 0:
                out.append((c, fa + fb))
    return out


def _lagrangian():
    f, th, u = _group()
    L = []
    # Yang-Mills  -1/4 F^a_{mn} F^{a mn}
    for a in range(4):
        F = [(sp.Integer(1), [("V", a, "n", "m")]), (sp.Integer(-1), [("V", a, "m", "n")])]
        for b in range(4):
            for c in range(4):
                if f[a][b][c] != 0:
                    F.append((f[a][b][c], [("V", b, "m", None), ("V", c, "n", None)]))
        L += _mul(F, F, sp.Rational(-1, 4))
    # scalar kinetic 1/2 (D phi)_i . (D phi)_i, D phi = d eta + theta^a V^a (u + eta)
    for i in range(4):
        D = [(sp.Integer(1), [("S", i, None, "m")])]
        for a in range(4):
            tu = sp.expand((th[a] * u)[i])
            if tu != 0:
                D.append((tu, [("V", a, "m", None)]))
            for j in range(4):
                if th[a][i, j] != 0:
                    D.append((th[a][i, j], [("V", a, "m", None), ("S", j, None, None)]))
        L += _mul(D, D, sp.Rational(1, 2))
    # gauge fixing -1/(2 xi) F^a F^a, F^a = d.V^a - xi eta^T theta^a u
    for a in range(4):
        F = [(sp.Integer(1), [("V", a, "m", "m")])]
        tu = th[a] * u
        for i in range(4):
            if tu[i] != 0:
                F.append((-xi * tu[i], [("S", i, None, None)]))
        L += _mul(F, _ren(F, {"m": "n"}), -1 / (2 * xi))
    # Faddeev-Popov: d cbar^a . d c^a + (d^m cbar^a) f^{abc} V^b_m c^c - xi cbar^a c^b (theta^b (u+eta)).(theta^a u)
    for a in range(4):
        L.append((sp.Integer(1), [("cb", a, None, "m"), ("c", a, None, "m")]))
        for b in range(4):
            for c in range(4):
                if f[a][b][c] != 0:
                    L.append((f[a][b][c], [("cb", a, None, "m"), ("V", b, "m", None), ("c", c, None, None)]))
            m2 = sp.expand(((th[b] * u).T * (th[a] * u))[0])
            if m2 != 0:
                L.append((-xi * m2, [("cb", a, None, None), ("c", b, None, None)]))
            for i in range(4):
                for j in range(4):
                    cij = sp.expand(th[b][i, j] * (th[a] * u)[i])
                    if cij != 0:
                        L.append((-xi * cij, [("cb", a, None, None), ("c", b, None, None), ("S", j, None, None)]))
    # Higgs potential: only its quadratic part enters (cubic/quartic scalar couplings only feed excluded tadpoles)
    lam = MH**2 / (2 * v**2)
    mu2 = lam * v**2
    eta = sp.symbols("e0:4")
    phi = sp.Matrix([eta[0], eta[1], v + eta[2], eta[3]])
    pp = sp.Rational(1, 2) * (phi.T * phi)[0]
    Vpot = sp.expand(-mu2 * pp + lam * pp**2)
    for i in range(4):
        assert sp.simplify(sp.diff(Vpot, eta[i]).subs({e: 0 for e in eta})) == 0     # minimum: no tadpole at tree level
        for j in range(i, 4):
            h = sp.simplify(sp.diff(Vpot, eta[i], eta[j]).subs({e: 0 for e in eta}))
            if h != 0:
                fac = sp.Rational(1, 2) if i == j else 1
                L.append((-fac * h, [("S", i, None, None), ("S", j, None, None)]))
    return L, (f, th, u)


# --------------------------------------------------------------------------------------------------------------
# tensor algebra: term = (coeff, atoms), atoms ('g', i, j) | ('p', vec, i)
# --------------------------------------------------------------------------------------------------------------
DOT = {("k", "k"): kk, ("q", "q"): qq, ("k", "q"): qk, ("q", "k"): qk}


def _contract(term):
    c, atoms = term
    atoms = list(atoms)
    changed = True
    while changed:
        changed = False
        for n, at in enumerate(atoms):
            if at[0] == "g" and at[1] == at[2]:
                c = c * dd
                atoms.pop(n)
                changed = True
                break
        if changed:
            continue
        pos = {}
        for n, at in enumerate(atoms):
            for idx in (at[1:] if at[0] == "g" else at[2:]):
                pos.setdefault(idx, []).append(n)
        for idx, ns in pos.items():
            if len(ns) == 2:
                n1, n2 = ns
                A1, A2 = atoms[n1], atoms[n2]
                if A1[0] == "g" or A2[0] == "g":
                    if A1[0] != "g":
                        n1, n2, A1, A2 = n2, n1, A2, A1
                    other = A1[2] if A1[1] == idx else A1[1]
                    if A2[0] == "g":
                        new = ("g",) + tuple(other if x == idx else x for x in A2[1:])
                    else:
                        new = ("p", A2[1], other)
                    atoms[n2] = new
                    atoms.pop(n1)
                else:
                    c = c * DOT[(A1[1], A2[1])]
                    for n in sorted((n1, n2), reverse=True):
                        atoms.pop(n)
                changed = True
                break
            assert len(ns) <= 2, "index used more than twice"
    return (c, tuple(atoms))


def _tmul(A, B):
    return [(ca * cb, fa + fb) for ca, fa in A for cb, fb in B]


_fresh = itertools.count()


def _vertex(groups, legs):
    """i x (sum over leg -> factor assignments) of the monomials with exactly the legs' field content."""
    key = tuple(sorted((l[0], l[1]) for l in legs))
    out = []
    for coeff, facs in groups.get(key, []):
        names = {}
        for (_, _, li, di) in facs:
            for x in (li, di):
                if x is not None and x not in names:
                    names[x] = "_t%d" % next(_fresh)
        for perm in itertools.permutations(range(len(legs))):
            ok = all((facs[n][0], facs[n][1]) == (legs[perm[n]][0], legs[perm[n]][1]) for n in range(len(facs)))
            if not ok:
                continue
            terms = [(sp.I * coeff, ())]
            for n, (kind, lab, li, di) in enumerate(facs):
                leg = legs[perm[n]]
                if li is not None:
                    terms = _tmul(terms, [(1, (("g", names[li], leg[2]),))])
                if di is not None:
                    terms = _tmul(terms, [(-sp.I * cmom, (("p", vec, names[di]),)) for vec, cmom in leg[3].items()])
            out += terms
    return [_contract(t) for t in out]


def _scalar(terms):
    tot = 0
    for c, atoms in terms:
        t = _contract((c, atoms))
        assert not t[1], t
        tot += t[0]
    return sp.expand(tot)


# --------------------------------------------------------------------------------------------------------------
# loop reduction (DERIVATION section 5).  X-symbols: A0_m, B0_{m1 m2}
# --------------------------------------------------------------------------------------------------------------
def _A0(m):
    return sp.Integer(0) if m == "0" else sp.Symbol("A0_" + m)


def _B0(m1, m2):
    a, b = sorted((m1, m2))
    return sp.Symbol("B0_" + a + b)


def _reduce(N, m1, m2):
    """I[N] for N polynomial in qq, qk (q-degree <= 2), D1 = q^2 - m1^2, D2 = (q-k)^2 - m2^2."""
    P = sp.Poly(sp.expand(N), qq, qk)
    a1, a2, B = _A0(m1), _A0(m2), _B0(m1, m2)
    M1, M2 = MASS2[m1], MASS2[m2]
    fk = kk + M1 - M2
    Iqk = (a2 - a1 + fk * B) / 2
    table = {(0, 0): B, (0, 1): Iqk, (1, 0): a2 + M1 * B, (0, 2): (kk * a2 + fk * Iqk) / 2}
    out = 0
    for (eq, ek), c in P.terms():
        assert (eq, ek) in table, ("q-degree too high", eq, ek)
        out += c * table[(eq, ek)]
    return sp.expand(out)


# --------------------------------------------------------------------------------------------------------------
# diagrams (DERIVATION section 4)
# --------------------------------------------------------------------------------------------------------------
def _setup():
    L, grp = _lagrangian()
    groups = {}
    for c, facs in L:
        groups.setdefault(tuple(sorted((x[0], x[1]) for x in facs)), []).append((c, facs))
    return groups, grp


def _masses(groups):
    """Read every mass from the quadratic Lagrangian and check the propagator forms of DERIVATION section 2."""
    p = {"k": 1}
    mp_ = {"k": -1}
    out = {}
    for kind, names in (("V", VNAMES), ("S", SNAMES)):
        for a in range(4):
            for b in range(4):
                legs = [(kind, a, "mu", p), (kind, b, "nu", mp_)]
                G = _vertex(groups, legs)
                if kind == "V":
                    Gg = _scalar(_tmul(G, [(1, (("g", "mu", "nu"),))]))
                    Gk = _scalar(_tmul(G, [(1, (("p", "k", "mu"), ("p", "k", "nu")))]))
                    # Feynman gauge: Gamma = -i g (k^2 - M^2): g-contraction -i d (k^2-M^2), kk-contraction -i k^2 (k^2-M^2)
                    if a != b:
                        assert sp.simplify(Gg) == 0 and sp.simplify(Gk) == 0
                    else:
                        M2 = sp.simplify(kk + Gg / (sp.I * dd))
                        assert sp.simplify(Gk - kk * Gg / dd) == 0
                        out[("V", a)] = sp.simplify(M2)
                else:
                    Gs = _scalar(G)
                    if a != b:
                        assert sp.simplify(Gs) == 0
                    else:
                        out[("S", a)] = sp.simplify(kk - Gs / sp.I)
            # V-S mixing must vanish (gauge-fixing cancels it)
    for a in range(4):
        for i in range(4):
            G = _vertex(groups, [("V", a, "mu", p), ("S", i, None, mp_)])
            Gk = _scalar(_tmul(G, [(1, (("p", "k", "mu"),))]))
            assert sp.simplify(Gk) == 0, ("V-S mixing survives", a, i)
    for a in range(4):
        for b in range(4):
            G = _scalar(_vertex(groups, [("cb", a, None, p), ("c", b, None, mp_)]))
            if a != b:
                assert sp.simplify(G) == 0
            else:
                out[("G", a)] = sp.simplify(kk - G / sp.I)
    return out


def _mass_label(m2):
    for lab, val in MASS2.items():
        if sp.simplify(m2 - val) == 0:
            return lab
    raise ValueError(m2)


def _diagrams(groups, mlab, a, b, want_long=False, raw=None):
    """Pi_T (and optionally Pi_L) for external V^a (in, k) -> V^b (out) as sums of c(d) x {A0, B0} / (16 pi^2)."""
    K, Km = {"k": 1}, {"k": -1}
    bos = [("V", i) for i in range(4)] + [("S", i) for i in range(4)]
    idx = {}
    Pg = 0      # g_{mu nu} Pi^{mu nu} * 16 pi^2
    Pk = 0      # k_mu k_nu Pi^{mu nu} * 16 pi^2
    proj_g = [(1, (("g", "mu", "nu"),))]
    proj_k = [(1, (("p", "k", "mu"), ("p", "k", "nu")))]

    def prop(kind, i1, i2):
        return [(-sp.I, (("g", i1, i2),))] if kind == "V" else [(sp.I, ())]

    # bosonic bubbles (1/2) sum_{c,d}
    for (kc, c), (kd, d) in itertools.product(bos, bos):
        l1 = [("V", a, "mu", K), (kc, c, "r1", {"q": -1}), (kd, d, "s1", {"q": 1, "k": -1})]
        l2 = [("V", b, "nu", Km), (kc, c, "r2", {"q": 1}), (kd, d, "s2", {"q": -1, "k": 1})]
        V1 = _vertex(groups, l1)
        if not V1:
            continue
        V2 = _vertex(groups, l2)
        if not V2:
            continue
        T = _tmul(_tmul(_tmul(V1, V2), prop(kc, "r1", "r2")), prop(kd, "s1", "s2"))
        m1, m2 = mlab[(kc, c)], mlab[(kd, d)]
        Ng, Nk = sp.Rational(1, 2) * _scalar(_tmul(T, proj_g)), sp.Rational(1, 2) * _scalar(_tmul(T, proj_k))
        if raw is not None:
            raw.append(("bubble", (kc, c), (kd, d), m1, m2, Ng, Nk))
        Pg += _reduce(Ng, m1, m2)
        Pk += _reduce(Nk, m1, m2)
    # ghost loops: - sum_{x,y}, line x: cbar at vertex 1, c at vertex 2
    for x, y in itertools.product(range(4), range(4)):
        V1 = _vertex(groups, [("V", a, "mu", K), ("cb", x, None, {"q": -1}), ("c", y, None, {"q": 1, "k": -1})])
        if not V1:
            continue
        V2 = _vertex(groups, [("V", b, "nu", Km), ("c", x, None, {"q": 1}), ("cb", y, None, {"q": -1, "k": 1})])
        if not V2:
            continue
        T = _tmul(_tmul(V1, V2), [(sp.I * sp.I, ())])
        m1, m2 = mlab[("G", x)], mlab[("G", y)]
        Ng, Nk = -_scalar(_tmul(T, proj_g)), -_scalar(_tmul(T, proj_k))
        if raw is not None:
            raw.append(("ghost", ("G", x), ("G", y), m1, m2, Ng, Nk))
        Pg += _reduce(Ng, m1, m2)
        Pk += _reduce(Nk, m1, m2)
    # seagulls (1/2) sum_c
    for (kc, c) in bos:
        legs = [("V", a, "mu", K), ("V", b, "nu", Km), (kc, c, "r1", {"q": 1}), (kc, c, "r2", {"q": -1})]
        V4 = _vertex(groups, legs)
        if not V4:
            continue
        T = _tmul(V4, prop(kc, "r1", "r2"))
        Ns = []
        for proj, acc in ((proj_g, "g"), (proj_k, "k")):
            N = _scalar(_tmul(T, proj))
            Ns.append(sp.Rational(1, 2) * N)
            assert not (N.has(qq) or N.has(qk)), "seagull numerator depends on q"
            val = sp.Rational(1, 2) * N * _A0(mlab[(kc, c)])
            if acc == "g":
                Pg += val
            else:
                Pk += val
        if raw is not None:
            raw.append(("seagull", (kc, c), None, mlab[(kc, c)], None, Ns[0], Ns[1]))
    Pg, Pk = sp.expand(Pg), sp.expand(Pk)
    PiT = sp.expand((Pg - Pk / kk) / (dd - 1))
    PiL = sp.expand(Pk / kk)
    return (PiT, PiL) if want_long else PiT


# --------------------------------------------------------------------------------------------------------------
# O(eps), MS-bar, Bbar (DERIVATION sections 5-6)
# --------------------------------------------------------------------------------------------------------------
def _xsyms(expr):
    return sorted([s for s in expr.free_symbols if s.name.startswith(("A0_", "B0_"))], key=lambda s: s.name)


def _res(X):
    return MASS2[X.name[3:]] if X.name.startswith("A0_") else sp.Integer(1)


def _fin(X):
    if X.name.startswith("A0_"):
        m = X.name[3:]
        return MASS2[m] * (1 - LOG[m])
    return sp.Symbol("B0f_" + X.name[3:])


def _eps_expand(Pi):
    """Pi = sum_j c_j(d) X_j  ->  (finite MS-bar part, pole coefficient)."""
    Pi = sp.expand(Pi)
    Xs = _xsyms(Pi)
    rest = sp.simplify(Pi.subs({X: 0 for X in Xs}))
    assert rest == 0, rest
    fin, pole = 0, 0
    for X in Xs:
        c = sp.together(Pi.coeff(X))
        c4 = c.subs(dd, 4)
        c1 = -2 * sp.diff(c, dd).subs(dd, 4)
        fin += c4 * _fin(X) + c1 * _res(X)
        pole += c4 * _res(X)
    return sp.expand(fin), sp.expand(pole)


def _b0zero(name):
    """finite B0(0, m1, m2) from the A0's (DERIVATION section 6)."""
    m1, m2 = name[0], name[1]
    if m1 == m2:
        return -LOG[m1]
    if m1 == "0":
        return 1 - LOG[m2]
    if m2 == "0":
        return 1 - LOG[m1]
    a, b = MASS2[m1], MASS2[m2]
    return (a * (1 - LOG[m1]) - b * (1 - LOG[m2])) / (a - b)


def _to_bbar(fin):
    subs = {}
    for s in fin.free_symbols:
        if s.name.startswith("B0f_"):
            nm = s.name[4:]
            subs[s] = _b0zero(nm) + kk * sp.Symbol("Bb_" + nm)
    e = sp.expand(fin.subs(subs))
    gens = sorted([s for s in e.free_symbols if s.name.startswith(("Bb_", "L_"))], key=lambda s: s.name)
    P = sp.Poly(e, *gens)
    out = 0
    for mon, c in P.terms():
        c = sp.factor(sp.cancel(sp.together(c)))
        num, den = sp.fraction(c)
        assert not den.has(kk), ("1/k^2 survives", mon, c)
        out += c * sp.Mul(*[gg**ee for gg, ee in zip(gens, mon)])
    return out


def _numeric_form(fin):
    """fin with B0f -> B0z + k^2 Bbar; the k^-2 part is shown to vanish once B0z is written out, and dropped.
    B0z = finite B0(0, m1, m2) stays a symbol so that degenerate masses (M_H = M_W, ...) need no special case."""
    subs, explicit = {}, {}
    for s_ in fin.free_symbols:
        if s_.name.startswith("B0f_"):
            nm = s_.name[4:]
            z = sp.Symbol("B0z_" + nm)
            subs[s_] = z + kk * sp.Symbol("Bb_" + nm)
            explicit[z] = _b0zero(nm)
    e = sp.expand(fin.subs(subs))
    low, reg = 0, 0
    for term in sp.Add.make_args(e):
        p_ = term.as_powers_dict().get(kk, 0)
        assert p_ >= -1, term
        if p_ == -1:
            low += term
        else:
            reg += term
    assert sp.simplify(sp.expand(low * kk).subs(explicit)) == 0, "the 1/k^2 terms do not cancel"
    return reg


_CACHE = {}


def _derive():
    if "res" in _CACHE:
        return _CACHE["res"]
    groups, grp = _setup()
    ms = _masses(groups)
    mlab = {}
    for (kind, i), m2 in ms.items():
        mlab[(kind, i)] = _mass_label(m2)
    res = {"mlab": mlab}
    for name, (a, b) in (("AA", (3, 3)), ("AZ", (3, 2)), ("ZZ", (2, 2)), ("W", (0, 0))):
        PiT = _diagrams(groups, mlab, a, b)
        fin, pole = _eps_expand(PiT)
        # Sigma_T = -Pi_T, overall 1/(16 pi^2)
        sig_fin = -fin
        sig_pole = -pole
        res[name] = {"bfin": sp.expand(sig_fin), "pole": sp.expand(sig_pole), "bbar": _to_bbar(sp.expand(sig_fin)),
                     "num": _numeric_form(sp.expand(sig_fin))}
    _CACHE["res"] = res
    _CACHE["groups"] = groups
    return res


# --------------------------------------------------------------------------------------------------------------
# numerics
# --------------------------------------------------------------------------------------------------------------
def _re_b0fin(k2, a, b, mu2):
    """Re B0^fin(k^2; a = m1^2, b = m2^2) = -int_0^1 ln|x a + (1-x) b - x(1-x) k^2| / mu^2 dx (current mp precision)."""
    if k2 == 0:
        if a == b:
            return -mp.log(a / mu2)
        if a == 0 or b == 0:
            return 1 - mp.log((a + b) / mu2)
        return 1 - (a * mp.log(a / mu2) - b * mp.log(b / mu2)) / (a - b)
    # f(x) = k2 x^2 + (a - b - k2) x + b = k2 (x - x1)(x - x2)
    B = a - b - k2
    disc = B * B - 4 * k2 * b

    def J(r):                                  # int_0^1 ln(x - r) dx (complex r) or ln|x - r| (real r)
        if isinstance(r, mp.mpc):
            return (1 - r) * mp.log(1 - r) + r * mp.log(-r) - 1
        t1 = (1 - r) * mp.log(abs(1 - r)) if r != 1 else mp.mpf(0)
        t2 = r * mp.log(abs(r)) if r != 0 else mp.mpf(0)
        return t1 + t2 - 1

    if disc >= 0:
        sq = mp.sqrt(disc)
        # stable roots
        qv = -(B + mp.sign(B) * sq) / 2 if B != 0 else -sq / 2
        if qv == 0:
            x1 = x2 = mp.mpf(0)
        else:
            x1 = qv / k2
            x2 = b / qv
        tot = mp.log(abs(k2)) + J(x1) + J(x2)
    else:
        sq = mp.sqrt(-disc)
        x1 = mp.mpc(-B, sq) / (2 * k2)
        tot = mp.log(abs(k2)) + 2 * mp.re(J(x1))
    return -(tot - mp.log(mu2))


def _bbar(k2, a, b):
    """Re (B0(k^2) - B0(0)) / k^2, with the exact k^2 -> 0 limit B0'(0)."""
    if k2 == 0:
        if a == b:
            return 1 / (6 * a)
        if a == 0 or b == 0:
            return 1 / (2 * (a + b))
        return (a * a - b * b - 2 * a * b * mp.log(a / b)) / (2 * (a - b) ** 3)
    mu2 = max(a, b, abs(k2))
    return (_re_b0fin(k2, a, b, mu2) - _re_b0fin(0, a, b, mu2)) / k2


_LAMB = {}


def _lamb(name):
    if name not in _LAMB:
        expr = _derive()[name]["num"]
        syms = sorted(expr.free_symbols, key=lambda s: s.name)
        _LAMB[name] = (syms, sp.lambdify(syms, expr, modules="mpmath"))
    return _LAMB[name]


def _dps(k2, mw, mz, mh, mu):
    vals = [mw * mw, mz * mz, mh * mh, mu * mu] + ([abs(k2)] if k2 != 0 else [])
    vals = [x for x in vals if x > 0]
    r = max(vals) / min(vals)
    return 40 + 3 * int(math.ceil(math.log10(max(r, 10.0))))


def _evaluate(name, k2, mw_, mz_, mh_, alpha, mu):
    syms, fn = _lamb(name)
    with mp.workdps(_dps(k2, mw_, mz_, mh_, mu)):
        k2m, mwm, mzm, mhm, mum = (mp.mpf(k2), mp.mpf(mw_), mp.mpf(mz_), mp.mpf(mh_), mp.mpf(mu))
        c = mwm / mzm
        s2 = 1 - c * c
        g2 = 4 * mp.pi * mp.mpf(alpha) / s2
        m2 = {"W": mwm**2, "Z": mzm**2, "H": mhm**2, "0": mp.mpf(0)}
        vals = []
        for s in syms:
            n = s.name
            if n == "kk":
                vals.append(k2m)
            elif n == "M_W":
                vals.append(mwm)
            elif n == "M_H":
                vals.append(mhm)
            elif n == "c_w":
                vals.append(c)
            elif n == "g":
                vals.append(mp.sqrt(g2))
            elif n.startswith("L_"):
                vals.append(mp.log(m2[n[2:]] / mum**2))
            elif n.startswith("Bb_"):
                vals.append(_bbar(k2m, m2[n[3]], m2[n[4]]))
            elif n.startswith("B0z_"):
                vals.append(_re_b0fin(0, m2[n[4]], m2[n[5]], mum**2))
            else:
                raise ValueError(n)
        val = fn(*vals) / (16 * mp.pi**2)
        return float(mp.re(val))


def sigma_AA(k2, MW, MZ, MH, alpha, mu):
    """Bosonic transverse photon self-energy Sigma^AA_T(k^2) (GeV^2)."""
    return _evaluate("AA", k2, MW, MZ, MH, alpha, mu)


def sigma_AZ(k2, MW, MZ, MH, alpha, mu):
    """Bosonic transverse photon-Z mixing Sigma^AZ_T(k^2) (GeV^2)."""
    return _evaluate("AZ", k2, MW, MZ, MH, alpha, mu)


def sigma_ZZ(k2, MW, MZ, MH, alpha, mu):
    """Bosonic transverse Z self-energy Sigma^ZZ_T(k^2) (GeV^2)."""
    return _evaluate("ZZ", k2, MW, MZ, MH, alpha, mu)


def sigma_W(k2, MW, MZ, MH, alpha, mu):
    """Bosonic transverse W self-energy Sigma^W_T(k^2) (GeV^2)."""
    return _evaluate("W", k2, MW, MZ, MH, alpha, mu)


_NOTE = ("one-loop bosonic 1PI diagrams derived from the SPEC Lagrangian by the in-module vertex extractor, "
         "d-dim reduction to A0/B0 with O(eps) kept, MS-bar, Sigma_T = -Pi_T")
PROVENANCE = {
    "sigma_AA": ("derived", _NOTE),
    "sigma_AZ": ("derived", _NOTE),
    "sigma_ZZ": ("derived", _NOTE),
    "sigma_W": ("derived", _NOTE),
}


# --------------------------------------------------------------------------------------------------------------
# second routes (DERIVATION section 7); run with `python3 bos_se.py`
# --------------------------------------------------------------------------------------------------------------
def _canon(terms):
    out = {}
    for c, atoms in terms:
        key = tuple(sorted(("g",) + tuple(sorted(a[1:])) if a[0] == "g" else a for a in atoms))
        out[key] = sp.expand(out.get(key, 0) + c)
    return {k: v for k, v in out.items() if sp.simplify(v) != 0}


def _same(t1, t2):
    a, b = _canon(t1), _canon(t2)
    keys = set(a) | set(b)
    return all(sp.simplify(a.get(k, 0) - b.get(k, 0)) == 0 for k in keys)


def _check_rules():
    """Compare the extracted vertices with the hand-derived rules of DERIVATION section 3."""
    groups, (f, th, u) = _setup()
    P = [{"p1": 1}, {"p2": 1}, {"p3": 1}, {"p4": 1}]
    n = 0

    def G(i, j):
        return (sp.Integer(1), (("g", i, j),))

    def p(v_, i, c=1):
        return (c, (("p", v_, i),))
    for a, b, c in itertools.product(range(4), repeat=3):
        V = _vertex(groups, [("V", a, "m", P[0]), ("V", b, "n", P[1]), ("V", c, "r", P[2])])
        F = f[a][b][c]
        hand = []
        for (i1, i2, i3, q1, q2) in (("m", "n", "r", "p1", "p2"), ("n", "r", "m", "p2", "p3"), ("r", "m", "n", "p3", "p1")):
            hand += [(F, (("g", i1, i2), ("p", q1, i3))), (-F, (("g", i1, i2), ("p", q2, i3)))]
        assert _same(V, hand), ("VVV", a, b, c)
        n += 1
    for a, b, c, d_ in itertools.combinations_with_replacement(range(4), 4):
        V = _vertex(groups, [("V", a, "m", P[0]), ("V", b, "n", P[1]), ("V", c, "r", P[2]), ("V", d_, "s", P[3])])
        hand = []
        for e in range(4):
            t1 = f[a][b][e] * f[c][d_][e]
            t2 = f[a][c][e] * f[b][d_][e]
            t3 = f[a][d_][e] * f[b][c][e]
            hand += [(-sp.I * t1, (("g", "m", "r"), ("g", "n", "s"))), (sp.I * t1, (("g", "m", "s"), ("g", "n", "r"))),
                     (-sp.I * t2, (("g", "m", "n"), ("g", "r", "s"))), (sp.I * t2, (("g", "m", "s"), ("g", "n", "r"))),
                     (-sp.I * t3, (("g", "m", "n"), ("g", "r", "s"))), (sp.I * t3, (("g", "m", "r"), ("g", "n", "s")))]
        assert _same(V, hand), ("VVVV", a, b, c, d_)
        n += 1
    for a in range(4):
        for i, j in itertools.product(range(4), repeat=2):
            V = _vertex(groups, [("V", a, "m", P[0]), ("S", i, None, P[1]), ("S", j, None, P[2])])
            hand = [(th[a][i, j], (("p", "p2", "m"),)), (-th[a][i, j], (("p", "p3", "m"),))]
            assert _same(V, hand), ("VSS", a, i, j)
            n += 1
        for b in range(4):
            anti = -(th[a] * th[b] + th[b] * th[a]) / 2
            Kab = anti * u
            for i in range(4):
                V = _vertex(groups, [("V", a, "m", P[0]), ("V", b, "n", P[1]), ("S", i, None, P[2])])
                assert _same(V, [(2 * sp.I * Kab[i], (("g", "m", "n"),))]), ("VVS", a, b, i)
                for j in range(4):
                    V = _vertex(groups, [("V", a, "m", P[0]), ("V", b, "n", P[1]), ("S", i, None, P[2]), ("S", j, None, P[3])])
                    assert _same(V, [(2 * sp.I * anti[i, j], (("g", "m", "n"),))]), ("VVSS", a, b, i, j)
                    n += 2
            for c in range(4):
                V = _vertex(groups, [("cb", a, None, P[0]), ("V", b, "m", P[1]), ("c", c, None, P[2])])
                assert _same(V, [(f[a][b][c], (("p", "p1", "m"),))]), ("ghost", a, b, c)
                n += 1
    return n


def _check_symbolic():
    groups = _setup()[0]
    mlab = {k: _mass_label(m2) for k, m2 in _masses(groups).items()}
    out = {}
    # photon longitudinal part vanishes identically
    PiT, PiL = _diagrams(groups, mlab, 3, 3, want_long=True)
    finL, poleL = _eps_expand(PiL) if _xsyms(PiL) else (0, 0)
    out["AA longitudinal (fin, pole)"] = (sp.simplify(_numeric_form(sp.expand(finL)) if finL != 0 else 0), sp.simplify(poleL))
    # W1 W1 = W2 W2, W1 W2 = 0
    p11 = _diagrams(groups, mlab, 0, 0)
    out["W2W2 - W1W1"] = sp.simplify(_diagrams(groups, mlab, 1, 1) - p11)
    out["W1W2"] = sp.simplify(_diagrams(groups, mlab, 0, 1))
    # custodial limit g' -> 0
    r = _derive()
    sub = {cw: 1}
    zz = r["ZZ"]["bfin"].subs(sub)
    w = r["W"]["bfin"].subs(sub)
    ren = {sp.Symbol("B0f_WZ"): sp.Symbol("B0f_WW"), sp.Symbol("B0f_HZ"): sp.Symbol("B0f_HW"), LOG["Z"]: LOG["W"]}
    out["custodial ZZ - W at g' = 0"] = sp.simplify(sp.expand(zz.subs(ren) - w.subs(ren)))
    out["AZ at g' = 0"] = sp.simplify(r["AZ"]["bfin"].subs(sub))
    return out


def _feynman_parameter_route(name, k2, mw_, mz_, mh_, alpha, mu, dps=30):
    """Independent loop integration: q = l + x k, angular average, Feynman-parameter integrals done numerically."""
    ab = {"AA": (3, 3), "AZ": (3, 2), "ZZ": (2, 2), "W": (0, 0)}[name]
    groups = _setup()[0]
    mlab = {k: _mass_label(m2) for k, m2 in _masses(groups).items()}
    raw = []
    _diagrams(groups, mlab, ab[0], ab[1], raw=raw)
    x, ll, lk, DU, LD = sp.symbols("x ll lk DU LD")     # DU = Delta_UV, LD = ln(Delta/mu^2)
    Dl = sp.Symbol("Delta")
    tot_x, tot_c = 0, 0
    deltas = []
    for kind, _, _, m1, m2, Ng, Nk in raw:
        if kind == "seagull":
            c = (Ng - Nk / kk) / (dd - 1)
            M2 = MASS2[m1]
            if M2 != 0:
                tot_c += c.subs(dd, 4) * M2 * (1 - LOG[m1]) - 2 * sp.diff(c, dd).subs(dd, 4) * M2
            continue
        M1, M2 = MASS2[m1], MASS2[m2]
        delta = x * M2 + (1 - x) * M1 - x * (1 - x) * kk
        deltas.append(delta)
        vals = []
        for N in (Ng, Nk):
            e = sp.expand(N.subs({qq: ll + 2 * x * lk + x**2 * kk, qk: lk + x * kk}, simultaneous=True))
            Pl = sp.Poly(e, lk)
            avg = 0
            for (pw,), cc in Pl.terms():
                assert pw <= 2
                if pw == 0:
                    avg += cc
                elif pw == 2:
                    avg += cc * ll * kk / dd
            Pll = sp.Poly(sp.expand(avg), ll)
            assert Pll.degree() <= 1
            n0, n1 = Pll.coeff_monomial(1), Pll.coeff_monomial(ll)
            # int 1/(l^2-D)^2 -> (DU - LD);  int l^2/(l^2-D)^2 -> (d/2) D (DU + 1 - LD)
            vals.append((n0, n1 * dd / 2))
        a_ = (vals[0][0] - vals[1][0] / kk) / (dd - 1)
        b_ = (vals[0][1] - vals[1][1] / kk) / (dd - 1)
        fin = (a_.subs(dd, 4) * (-LD) - 2 * sp.diff(a_, dd).subs(dd, 4)
               + b_.subs(dd, 4) * Dl * (1 - LD) - 2 * sp.diff(b_, dd).subs(dd, 4) * Dl)
        tot_x += fin.subs(Dl, delta).subs(LD, sp.log(sp.Abs(delta)) - sp.Symbol("lnmu2"))     # real part
    with mp.workdps(dps):
        c = mp.mpf(mw_) / mz_
        g2 = 4 * mp.pi * alpha / (1 - c * c)
        num = {g: mp.sqrt(g2), cw: c, MW: mp.mpf(mw_), MH: mp.mpf(mh_), kk: mp.mpf(k2), sp.Symbol("lnmu2"): mp.log(mp.mpf(mu)**2)}
        for m in ("W", "Z", "H"):
            num[LOG[m]] = mp.log({"W": mp.mpf(mw_), "Z": mp.mpf(mz_), "H": mp.mpf(mh_)}[m]**2 / mp.mpf(mu)**2)
        fx = sp.lambdify([x], tot_x.subs(num), modules="mpmath")
        const = sp.N(tot_c.subs(num), dps) if tot_c != 0 else 0
        pts = {mp.mpf(0), mp.mpf(1) / 2, mp.mpf(1)}
        for dl in deltas:                                  # split the x-range at the zeros of Delta (thresholds)
            c2, c1, c0 = [mp.mpf(str(sp.N(cf, dps))) for cf in sp.Poly(dl.subs(num), x).all_coeffs()]
            disc = c1 * c1 - 4 * c2 * c0
            if c2 != 0 and disc > 0:
                for rt in ((-c1 + mp.sqrt(disc)) / (2 * c2), (-c1 - mp.sqrt(disc)) / (2 * c2)):
                    if mp.mpf(10)**(-20) < rt < 1 - mp.mpf(10)**(-20):
                        pts.add(rt)
        val = mp.quad(fx, sorted(pts)) + mp.mpf(str(const))
        return float(-val / (16 * mp.pi**2))


if __name__ == "__main__":
    print("Feynman rules extracted from the Lagrangian = hand rules (DERIVATION 3):", _check_rules(), "vertex cases agree")
    for kname, val in _check_symbolic().items():
        print(f"{kname}: {val}")
    r = _derive()
    for nm in ("AA", "AZ", "ZZ", "W"):
        print(f"UV pole of Sigma^{nm} (coefficient of Delta, x 16 pi^2): {sp.factor(r[nm]['pole'])}")
    MWv, MZv, MHv, AL = 80.38, 91.19, 125.0, 1 / 128.0
    print("\nmain route (PV reduction, closed form)  vs  second route (Feynman parameters, numerical x-integral)")
    for nm, fn in (("AA", sigma_AA), ("AZ", sigma_AZ), ("ZZ", sigma_ZZ), ("W", sigma_W)):
        for k2 in (-3.0 * MWv**2, -0.7 * MWv**2, 0.4 * MWv**2):
            a_ = fn(k2, MWv, MZv, MHv, AL, 1.7 * MWv)
            b_ = _feynman_parameter_route(nm, k2, MWv, MZv, MHv, AL, 1.7 * MWv)
            print(f"  Sigma^{nm}({k2:+.1f}) = {a_:+.12e}   {b_:+.12e}   rel diff {abs(a_ - b_) / max(abs(a_), 1e-30):.1e}")
    print("\nmu dependence vs UV pole: d Sigma / d ln mu^2 (numerical) vs pole coefficient / 16 pi^2")
    for nm, fn in (("AA", sigma_AA), ("AZ", sigma_AZ), ("ZZ", sigma_ZZ), ("W", sigma_W)):
        k2 = 0.3 * MWv**2
        h = 1e-4
        der = (fn(k2, MWv, MZv, MHv, AL, MWv * math.exp(h / 2)) - fn(k2, MWv, MZv, MHv, AL, MWv * math.exp(-h / 2))) / (2 * h)
        cc = MWv / MZv
        pole = float(r[nm]["pole"].subs({g: math.sqrt(4 * math.pi * AL / (1 - cc * cc)), cw: cc, MW: MWv, MH: MHv, kk: k2})) / (16 * math.pi**2)
        print(f"  {nm}: {der:+.10e}  {pole:+.10e}")
    print("\nlarge and small M_H, thresholds:")
    for mh in (1.0, 125.0, 1e6, 1e14):
        print(f"  M_H = {mh:g}: W(0) = {sigma_W(0.0, MWv, MZv, mh, AL, MWv):+.10e}  ZZ(MZ^2) = {sigma_ZZ(MZv**2, MWv, MZv, mh, AL, MWv):+.10e}"
              f"  W(1e-7) = {sigma_W(1e-7, MWv, MZv, mh, AL, MWv):+.10e}")
