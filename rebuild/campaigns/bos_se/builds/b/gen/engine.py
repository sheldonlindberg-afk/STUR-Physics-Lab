import sys, itertools
sys.path.insert(0, 'tmp')
import sympy as sp
from vtx import *
from phys import phys, e, mh

d, kk, qq, qk, Del = sp.symbols('d kk qq qk Del')
PARTNER = {'A': 'A', 'Z': 'Z', 'H': 'H', 'chi': 'chi', 'Wp': 'Wm', 'Wm': 'Wp', 'php': 'phm', 'phm': 'php',
           'cp': 'cbm', 'cm': 'cbp', 'cbm': 'cp', 'cbp': 'cm', 'cZ': 'cbZ', 'cbZ': 'cZ', 'cA': 'cbA', 'cbA': 'cA'}
MTAG = {'A': '0', 'Z': 'Z', 'Wp': 'W', 'Wm': 'W', 'php': 'W', 'phm': 'W', 'chi': 'Z', 'H': 'H',
        'cp': 'W', 'cm': 'W', 'cbp': 'W', 'cbm': 'W', 'cZ': 'Z', 'cbZ': 'Z', 'cA': '0', 'cbA': '0'}
MSYM = {'0': sp.Integer(0), 'W': mw, 'Z': mz, 'H': mh}
BOS = ['A', 'Z', 'Wp', 'Wm', 'php', 'phm', 'chi', 'H']
GH = ['cp', 'cm', 'cZ', 'cA', 'cbp', 'cbm', 'cbZ', 'cbA']

A0f = {t: sp.Symbol('A0f_' + t) for t in 'WZH'}
def B0f(t1, t2):
    t1, t2 = sorted([t1, t2])
    return sp.Symbol('B0f_' + t1 + t2)
def A0(t):
    return 0 if t == '0' else MSYM[t]**2 * Del + A0f[t]
def B0(t1, t2):
    return Del + B0f(t1, t2)


def vterms(ops, moms, idx):
    """terms (coeff, [factors]) of vertex (coefficient in L) of ordered ops; moms[l]={'k':a,'q':b}; idx[l] index label"""
    vx = vertex(ops)
    out = []
    for desc, co in vx.items():
        tl = [(co, [])]
        for it in desc:
            new = []
            if it[0] == 'g':
                for (cf, fs) in tl:
                    new.append((cf, fs + [('g', idx[it[1]], idx[it[2]])]))
            elif it[0] == 'p':
                for (cf, fs) in tl:
                    for vec, a in moms[it[1]].items():
                        if a != 0:
                            new.append((cf * a, fs + [('p', vec, idx[it[2]])]))
            elif it[0] == 'pp':
                m1, m2 = moms[it[1]], moms[it[2]]
                a1, b1 = m1.get('k', 0), m1.get('q', 0)
                a2, b2 = m2.get('k', 0), m2.get('q', 0)
                sc_ = a1 * a2 * kk + (a1 * b2 + a2 * b1) * qk + b1 * b2 * qq
                for (cf, fs) in tl:
                    new.append((cf * sc_, fs))
            tl = new
        out += tl
    return out


def mult(t1, t2):
    return [(a * b, f1 + f2) for (a, f1) in t1 for (b, f2) in t2]


def contract(term, ext):
    """contract repeated indices (ext = set of free labels). returns (coeff, factors)"""
    cf, fs = term
    fs = list(fs)
    while True:
        cnt = {}
        for fi, f in enumerate(fs):
            for ix in f[1:] if f[0] == 'g' else (f[2],):
                cnt.setdefault(ix, []).append(fi)
        rep = [ix for ix, l in cnt.items() if len(l) == 2 or (len(l) == 1 and False)]
        # g(i,i)
        done = False
        for fi, f in enumerate(fs):
            if f[0] == 'g' and f[1] == f[2]:
                cf = cf * d
                fs.pop(fi)
                done = True
                break
        if done:
            continue
        cand = [ix for ix, l in cnt.items() if len(l) == 2 and ix not in ext]
        if not cand:
            break
        ix = cand[0]
        i1, i2 = cnt[ix]
        f1, f2 = fs[i1], fs[i2]
        if f1[0] == 'p' and f2[0] == 'p':
            a, b = f1[1], f2[1]
            if a == b == 'q':
                cf = cf * qq
            elif a == b == 'k':
                cf = cf * kk
            else:
                cf = cf * qk
            for j in sorted((i1, i2), reverse=True):
                fs.pop(j)
        else:
            if f1[0] == 'p':
                f1, f2 = f2, f1
                i1, i2 = i2, i1
            # f1 is g
            other = f1[2] if f1[1] == ix else f1[1]
            if f2[0] == 'g':
                new = ('g',) + tuple(other if y == ix else y for y in f2[1:])
            else:
                new = ('p', f2[1], other)
            for j in sorted((i1, i2), reverse=True):
                fs.pop(j)
            fs.append(new)
    return cf, fs


def A0_of(t): return A0(t)

def reduce_direct(terms, t1, t2):
    """g^{mu nu} coefficient of int terms/(D1 D2), PV-reduced (symbolic d, Del)."""
    m1, m2 = MSYM[t1], MSYM[t2]
    Sg = 0
    Sqq = 0
    for cf, fs in terms:
        cf, fs = contract((cf, fs), {'mu', 'nu'})
        if not fs:
            raise Exception('no external structure')
        if len(fs) == 1 and fs[0][0] == 'g':
            Sg += cf
        elif len(fs) == 2 and all(f[0] == 'p' for f in fs):
            vs = sorted(f[1] for f in fs)
            if vs == ['q', 'q']:
                Sqq += cf
        else:
            raise Exception(('structure', fs))
    f_ = kk + m1**2 - m2**2
    X1 = (A0(t1) - A0(t2) - f_ * B0(t1, t2)) / 2           # int qk
    X0 = B0(t1, t2)
    Xqq = A0(t2) + m1**2 * B0(t1, t2)
    B1 = X1 / kk
    B00 = (A0(t2) + 2 * m1**2 * B0(t1, t2) + f_ * B1) / (2 * (d - 1))
    Sg = sp.expand(Sg)
    P = sp.Poly(Sg, qq, qk)
    res = 0
    for (a, b), co in P.terms():
        if (a, b) == (0, 0): res += co * X0
        elif (a, b) == (1, 0): res += co * Xqq
        elif (a, b) == (0, 1): res += co * X1
        else: raise Exception(('degree', a, b))
    Pq = sp.Poly(sp.expand(Sqq), qq, qk)
    for (a, b), co in Pq.terms():
        assert (a, b) == (0, 0), 'qq with extra q'
        res += co * B00
    return res


def reduce_proj(terms_g, terms_kk, t1, t2):
    m1, m2 = MSYM[t1], MSYM[t2]
    f_ = kk + m1**2 - m2**2
    X1 = (A0(t1) - A0(t2) - f_ * B0(t1, t2)) / 2
    X0 = B0(t1, t2)
    Xqq = A0(t2) + m1**2 * B0(t1, t2)
    Xqk2 = (kk * A0(t2) - f_ * X1) / 2
    def integ(S):
        P = sp.Poly(sp.expand(S), qq, qk)
        r = 0
        for (a, b), co in P.terms():
            if (a, b) == (0, 0): r += co * X0
            elif (a, b) == (1, 0): r += co * Xqq
            elif (a, b) == (0, 1): r += co * X1
            elif (a, b) == (0, 2): r += co * Xqk2
            else: raise Exception(('degree', a, b))
        return r
    Tg = sum((contract(t, set())[0] for t in terms_g), 0)
    Tk = sum((contract(t, set())[0] for t in terms_kk), 0)
    return (integ(Tg) - integ(Tk) / kk) / (d - 1)


def finalize(E):
    """E linear in Del, A0f_*, B0f_*; returns (finite part dict {loopsymbol: coeff}, pole coefficient)"""
    E = sp.expand(E)
    syms = [x for x in E.free_symbols if x.name.startswith(('A0f', 'B0f'))]
    ep = sp.Symbol('ep')
    fin = {}
    for sy in syms:
        co = sp.together(E.coeff(sy)).subs(d, 4 - 2 * ep)
        fin[sy] = sp.simplify(co.subs(ep, 0))
    cD = sp.together(E.coeff(Del)).subs(d, 4 - 2 * ep)
    pole = sp.simplify(cD.subs(ep, 0))
    rest = sp.simplify(sp.diff(cD, ep).subs(ep, 0))
    # any term free of all of these
    resid = sp.expand(E - sum(E.coeff(sy) * sy for sy in syms) - E.coeff(Del) * Del)
    rest += sp.simplify(resid.subs(d, 4).subs(Del, 0)) if resid != 0 else 0
    return fin, pole, rest


def diagrams(X, Y, proj=False):
    """all diagrams of Sigma_{XY}; returns list of (label, expression) with expression in units 1/(16 pi^2)"""
    out = []
    idxX, idxY = 'mu', 'nu'
    # bubbles
    for ordered in itertools.product(BOS, BOS):
        a, b = ordered
        at, bt = PARTNER[a], PARTNER[b]
        V1 = vertex([X, a, b])
        if not V1: continue
        V2 = vertex([Y, at, bt])
        if not V2: continue
        isv = lambda o: OPS[o] == 'v'
        i1 = ['mu', 'a' if isv(a) else None, 'b' if isv(b) else None]
        i2 = ['nu', 'a' if isv(at) else None, 'b' if isv(bt) else None]
        m1 = [{'k': 1}, {'q': 1}, {'q': -1, 'k': -1}]
        m2 = [{'k': -1}, {'q': -1}, {'q': 1, 'k': 1}]
        T1 = vterms([X, a, b], m1, i1)
        T2 = vterms([Y, at, bt], m2, i2)
        terms = mult(T1, T2)
        ca = -1 if isv(a) else 1   # c_a / i
        cb = -1 if isv(b) else 1
        pref = sp.Rational(1, 2) * (sp.I * ca) * (sp.I * cb)
        ta, tb = MTAG[a], MTAG[b]
        if not proj:
            R = reduce_direct(terms, ta, tb)
        else:
            tg = [(cf, [(f if f[0] == 'g' or f[2] not in ('mu', 'nu') else ('p', f[1], 'x')) if False else f for f in fs]) for cf, fs in terms]
            # replace nu by mu (contract), then project
            def relabel(fs):
                r = []
                for f in fs:
                    if f[0] == 'g':
                        r.append(('g',) + tuple('mu' if y == 'nu' else y for y in f[1:]))
                    else:
                        r.append(('p', f[1], 'mu' if f[2] == 'nu' else f[2]))
                return r
            tg = [(cf, relabel(fs)) for cf, fs in terms]
            tk = [(cf, fs + [('p', 'k', 'mu'), ('p', 'k', 'nu')]) for cf, fs in terms]
            R = reduce_proj(tg, tk, ta, tb)
        out.append((f'{X}-{Y} bubble {a},{b}', pref * R))
    # ghost bubbles (no 1/2, sign handled: Sigma = +R/16pi^2)
    for a in [o for o in GH if o.startswith('cb')]:
        for b in [o for o in GH if not o.startswith('cb')]:
            V1 = vertex([X, a, b])
            if not V1: continue
            at, bt = PARTNER[a], PARTNER[b]
            V2 = vertex([Y, at, bt])
            if not V2: continue
            m1 = [{'k': 1}, {'q': 1}, {'q': -1, 'k': -1}]
            m2 = [{'k': -1}, {'q': -1}, {'q': 1, 'k': 1}]
            T1 = vterms([X, a, b], m1, ['mu', None, None])
            T2 = vterms([Y, at, bt], m2, ['nu', None, None])
            terms = mult(T1, T2)
            ta, tb = MTAG[a], MTAG[b]
            if not proj:
                R = reduce_direct(terms, ta, tb)
            else:
                def relabel(fs):
                    r = []
                    for f in fs:
                        if f[0] == 'g':
                            r.append(('g',) + tuple('mu' if y == 'nu' else y for y in f[1:]))
                        else:
                            r.append(('p', f[1], 'mu' if f[2] == 'nu' else f[2]))
                    return r
                tg = [(cf, relabel(fs)) for cf, fs in terms]
                tk = [(cf, fs + [('p', 'k', 'mu'), ('p', 'k', 'nu')]) for cf, fs in terms]
                R = reduce_proj(tg, tk, ta, tb)
            out.append((f'{X}-{Y} ghost {a},{b}', R))
    # seagulls
    for a in BOS:
        at = PARTNER[a]
        V4 = vertex([X, Y, a, at])
        if not V4: continue
        isv = OPS[a] == 'v'
        idx = ['mu', 'nu', 'a' if isv else None, 'a' if isv else None]
        moms = [{'k': 1}, {'k': -1}, {'q': 1}, {'q': -1}]
        terms = vterms([X, Y, a, at], moms, idx)
        tot = 0
        for t in terms:
            cf, fs = contract(t, {'mu', 'nu'})
            if len(fs) == 1 and fs[0][0] == 'g':
                tot += cf
            elif len(fs) == 0:
                raise Exception('?')
            else:
                raise Exception(('seag', fs))
        # Sigma = (1/2) * (-i c_a... ) : scalar +1/2, vector -1/2 times int L4/D -> A0
        sgn = sp.Rational(1, 2) * (-1 if isv else 1)
        out.append((f'{X}-{Y} seagull {a}', sgn * tot * A0(MTAG[a])))
    return out
