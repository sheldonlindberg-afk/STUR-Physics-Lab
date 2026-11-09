#!/usr/bin/env python3
"""
Make It Make Sense theory, part 8: the mass-conserving, angle-rule collapse.

Part 7 showed the ceiling P1 forces the shock's one-turn phase slip to be counted as an
ANGLE, and that a solver must conserve mass, not the winding.  The standard way to do both:
follow each mass layer individually and let layers pass through each other (dust does not
collide).  Each layer's phase evolves continuously; no jump between neighbours is counted.

  Each layer i (mass M/N, areal radius R_i) obeys the theory's law with the mass inside it
  at that moment (FOLLOWS from part 1; exact GR for dust away from the ceiling, and its
  thin-shell limit is the Israel junction condition):
        d^2 R_i / dtau^2 = -(G m_i / R_i^2) (1 - 4 phi_i),   phi_i = 3 m_i / (4 pi rho_max R_i^3)
  Start: marginally bound free fall, dR/dtau = -sqrt(2m/R (1 - phi)).
  Horizon: some radius with 2 m(R)/R (1 - phi(R)) > 1 (trapped or anti-trapped).

Results (computed here):
  E1  Lifetime T = 3.8 M (uniform star) and 3.2 M (centrally concentrated), in Planck
      units, i.e. PROPORTIONAL TO M: a solar-mass hole re-expands after ~2e-5 s.  Observed
      black holes last billions of years, so under this rule the re-expansion cannot come
      back into OUR region: it must open into a new one (a white hole beyond the hole).
      LIT (recalled): bounces inside black holes opening new expanding regions were
      proposed with torsion by Poplawski (2010) -- the same teleparallel/torsion family.
  E2  P1 fails again: where layers cross, the local fullness spikes without bound
      (caustics).  With part 7: dust cannot respect P1 under EITHER rule.
      FOLLOWS: P1 requires matter that resists compression near full -- "pure matter at 1"
      must carry pressure.  The theory needs an equation of state p(phi): OPEN.
"""
import numpy as np


def banner(s):
    print("\n" + "=" * 78 + "\n" + s + "\n" + "=" * 78)


def init(M, N, profile, R0, chi):
    x = np.linspace(0, 1, 20001)
    rho = np.ones_like(x) if profile == "uniform" else (1 - x ** 2)
    f = rho * x * x
    mc = np.concatenate([[0], np.cumsum(0.5 * (f[1:] + f[:-1]) * np.diff(x))])
    mc /= mc[-1]
    q = (np.arange(N) + 0.5) / N
    r = R0 * np.interp(q, mc, x)
    m = M * q
    v = -np.sqrt(2 * m / r * np.clip(1 - 3 * m / (4 * np.pi * chi * r ** 3), 0, None))
    return r, v


def accel(r, M, N, chi):
    order = np.argsort(r)
    menc = np.empty(N)
    menc[order] = M / N * (np.arange(N) + 0.5)
    phib = 3 * menc / (4 * np.pi * chi * r ** 3)
    return -(menc / r ** 2) * (1 - 4 * phib), phib


def local_fullness(r, M, N, chi):
    """Fullness of each zone between neighbouring layers (first zone holds half a layer)."""
    rs = np.sort(r)
    dmz = np.full(N, M / N)
    dmz[0] = 0.5 * M / N
    vol = 4 * np.pi / 3 * np.diff(np.concatenate([[0], rs ** 3]))
    return dmz / (chi * np.maximum(vol, 1e-300))


def run(M, N=400, profile="conc", R0fac=1.5, chi=1.0, tfac=12.0, ngrid=4000):
    rs = 2 * M
    r, v = init(M, N, profile, R0fac * rs, chi)
    k = np.sqrt(8 * np.pi * chi / 3)
    t, had, phmax, ncross = 0.0, False, 0.0, 0
    prev = np.argsort(r)
    f = lambda r, v: (v, accel(r, M, N, chi)[0])
    Rg = np.linspace(1e-3, 1.2 * rs, ngrid)
    while t < tfac * M + 50:
        _, phib = accel(r, M, N, chi)
        dt = 0.02 * min(np.min(r / np.maximum(np.abs(v), 1e-9)),
                        np.min(1 / (k * np.sqrt(np.maximum(phib, 1e-12)))), 1.0)
        k1r, k1v = f(r, v)
        k2r, k2v = f(r + dt / 2 * k1r, v + dt / 2 * k1v)
        k3r, k3v = f(r + dt / 2 * k2r, v + dt / 2 * k2v)
        k4r, k4v = f(r + dt * k3r, v + dt * k3v)
        r = np.abs(r + dt / 6 * (k1r + 2 * k2r + 2 * k3r + k4r))
        v = v + dt / 6 * (k1v + 2 * k2v + 2 * k3v + k4v)
        t += dt
        o = np.argsort(r)
        ncross += int((o != prev).any())
        prev = o
        phmax = max(phmax, local_fullness(r, M, N, chi).max())
        ms = M / N * (np.arange(N) + 1)
        mg = np.interp(Rg, r[o], ms, left=0, right=M)
        if (2 * mg / Rg * (1 - 3 * mg / (4 * np.pi * chi * Rg ** 3)) > 1).any():
            had = True
        elif had:
            return dict(T=t, phmax=phmax, ncross=ncross)
    return dict(T=None, phmax=phmax, ncross=ncross)


def main():
    G, c, hbar = 6.67430e-11, 2.99792458e8, 1.054571817e-34
    t_P, m_P = np.sqrt(hbar * G / c ** 5), np.sqrt(hbar * c / G)
    banner("E1-E2  Layers that pass through each other (mass-conserving, angle rule)")
    print("   star            M (m_P)   lifetime T   T/M     max local fullness   steps with crossings")
    rows = {}
    for prof in ("uniform", "conc"):
        for M in (2.0, 4.0, 8.0):
            r = run(M, profile=prof)
            rows[(prof, M)] = r
            lab = "uniform" if prof == "uniform" else "concentrated"
            print(f"   {lab:13s}  {M:6.1f}    {r['T']:8.2f}    {r['T']/M:5.3f}    "
                  f"{r['phmax']:14.1f}         {r['ncross']}")
    for prof in ("uniform", "conc"):
        tm = rows[(prof, 8.0)]["T"] / 8.0
        print(f"   {prof:8s}: solar-mass lifetime {tm*(1.98892e30/m_P)*t_P:.1e} s")
    print("   -> T is proportional to M, not M^2.  Observed black holes last billions of years,")
    print("      so under this rule the bounce cannot re-emerge into OUR region: it must open a")
    print("      new one beyond the hole (cf. Poplawski's torsion bounces, recalled).")
    print("   -> uniform star: peak local fullness 1 at the bounce (P1 exactly saturated).")
    print("   -> concentrated star: layers cross and the local fullness spikes (caustics,")
    print("      unbounded in the continuum): P1 fails.  With part 7, dust breaks P1 under")
    print("      either rule, so P1 requires pressure: the theory needs p(phi).  OPEN.")
    return rows


if __name__ == "__main__":
    main()
