#!/usr/bin/env python3
"""
Make It Make Sense theory, part 9: collapse of matter that pushes back (the author's choice 1).

Equation of state (NEW, causal form of "radiation that stiffens near full"):
    sound speed^2 = 1/3 + (2/3) phi^2  (phi = e / rho_max <= 1),  = 1 beyond.
    Ordinary radiation (p = e/3) at low fullness; the speed of sound reaches c exactly at
    full.  (A pressure growing without limit would need sound faster than light.)

Gravity: the MIMS law with pressure.  For a uniform region, H^2 = (8 pi/3) e (1 - phi) and
energy conservation give exactly
    d^2R/dtau^2 = -[(m + 4 pi R^3 p) - phi_bar (4 m + 8 pi R^3 p)] / R^2       (FOLLOWS)
(dust: part 8's law; no ceiling: GR).  Used layer by layer with the mean fullness phi_bar
(as in part 8) inside the Misner-Sharp equations (KNOWN: GR spherical fluid collapse):
lapse from the pressure gradient, Gamma^2 = 1 + U^2 - 2m(1 - phi_bar)/R solved to
convergence, energy from each zone's adiabat (algebraic, no drift), RK4 in time.

Setup: a uniform ball at 1.5 r_s in marginally bound free fall (an arbitrary start, not a
model of how primordial holes form).  Outer zones that escape (moving out, beyond 3 r_s)
are removed and counted as escaped; spherical symmetry means this cannot affect the inside.

Results (computed here):
  CHECK  dust: T = 7.59 (part 8: 7.53), peak fullness 1.0000.
  F1  ~39% of the mass is blown off by radiation pressure before the horizon forms
      (same for M = 2, 4 and for both equations of state; it depends on the start).
  F2  horizon at ~3.1 M; plain radiation overshoots the ceiling (peak 7.7 at M = 2), the
      stiffening holds it (peak 0.72) -- up to the shock.
  F3  at ~8.7 M infalling outer layers form a SHOCK near 0.3 r_s, before the core reaches
      full.  This solver follows smooth flow only: the bounce, the lifetime and the burst
      need a shock-capturing method.  OPEN.
"""
import numpy as np

def make_eos(kind, chi):
    if kind == "dust":
        return (lambda e: 0 * e), None
    if kind == "rad":
        p = lambda e: e / 3
    else:  # causal stiffening: cs^2 = 1/3 + (2/3) phi^2, = 1 beyond phi = 1
        def p(e):
            x = e / chi
            xc = np.minimum(x, 1.0)
            return chi * (xc / 3 + 2 * xc ** 3 / 9) + chi * np.maximum(x - 1, 0)
    # adiabat: d ln n = de / (e + p)
    eg = np.logspace(-14, 2, 40001) * chi
    f = 1 / (eg + p(eg))
    lnn = np.concatenate([[0], np.cumsum(0.5 * (f[1:] + f[:-1]) * np.diff(eg))])
    lnn += np.log(eg[0])   # e ~ n^(4/3)-like normalisation at the low end; any constant works
    e_of_lnn = lambda L: np.exp(np.interp(L, lnn, np.log(eg)))
    lnn_of_e = lambda e: np.interp(np.log(e), np.log(eg), lnn)
    return p, (e_of_lnn, lnn_of_e)


def run(M, N=300, chi=1.0, kind="stiff", profile="uniform", R0fac=1.5, law=True,
        tfac=40.0, cfl=0.2, maxsteps=3_000_000, verbose=False):
    rs = 2 * M
    R0 = R0fac * rs
    x = np.linspace(0, 1, N + 1)
    R = R0 * x
    dVc = 4 * np.pi / 3 * np.diff(R ** 3)
    xc = 0.5 * (x[1:] + x[:-1])
    prof = np.ones(N) if profile == "uniform" else (1 - xc ** 2)
    e0 = prof * M / np.sum(prof * dVc)
    p, ad = make_eos(kind, chi)
    m0 = np.concatenate([[0], np.cumsum(e0 * dVc)])
    phib0 = np.zeros(N + 1)
    if law:
        phib0[1:] = 3 * m0[1:] / (4 * np.pi * chi * R[1:] ** 3)
    U = -np.sqrt(np.maximum(2 * m0 * (1 - phib0) / np.maximum(R, 1e-300), 0))
    # conserved per-zone "number": dust -> rest mass; fluid -> n from adiabat (Gamma = 1 at t=0)
    if kind == "dust":
        dmu = e0 * dVc
    else:
        dmu = np.exp(ad[1](e0)) * dVc

    def state(R, U):
        N = len(R) - 1
        dV = 4 * np.pi / 3 * np.diff(R ** 3)
        # Gamma from the constraint needs m, which needs e, which needs Gamma: iterate twice
        Gz = np.ones(N) if not hasattr(state, "Gprev") or len(state.Gprev) != N else state.Gprev.copy()
        for it in range(200):
            n = dmu[:N] * Gz / dV
            e = n if kind == "dust" else ad[0](np.log(n))
            m = np.concatenate([[0], np.cumsum(e * dV)])
            pb = np.zeros(N + 1)
            if law:
                pb[1:] = 3 * m[1:] / (4 * np.pi * chi * R[1:] ** 3)
            G2 = 1 + U ** 2 - 2 * m * (1 - pb) / np.maximum(R, 1e-300)
            G2[0] = 1
            Gi = np.sqrt(np.maximum(G2, 1e-12))
            Gnew = 0.5 * (Gi[1:] + Gi[:-1])
            err = np.max(np.abs(Gnew - Gz) / np.maximum(Gnew, 1e-6))
            Gz = 0.5 * Gz + 0.5 * Gnew
            if err < 1e-11:
                break
        state.Gprev = Gz.copy()
        state.err = err
        return e, m, pb, G2, Gz, dV

    def deriv(R, U):
        N = len(R) - 1
        e, m, pb, G2, Gz, dV = state(R, U)
        pz = p(e)
        w = e + pz
        Rz = 0.5 * (R[1:] + R[:-1])
        dP = np.diff(pz)
        wb = 0.5 * (w[1:] + w[:-1])
        lna = np.concatenate([[0], np.cumsum(-dP / np.maximum(wb, 1e-300))])
        lna -= lna[-1]
        az = np.exp(lna)
        ai = np.concatenate([[az[0]], 0.5 * (az[1:] + az[:-1]), [az[-1]]])
        pint = np.concatenate([[pz[0]], 0.5 * (pz[1:] + pz[:-1]), [0.0]])
        wint = np.concatenate([[w[0]], wb, [0.5 * w[-1]]])
        gradP = np.zeros(N + 1)
        gradP[1:N] = dP / np.maximum(np.diff(Rz), 1e-300)
        gradP[N] = (0 - pz[-1]) / max(R[N] - Rz[-1], 1e-300)
        grav = np.zeros(N + 1)
        grav[1:] = -(m[1:] + 4 * np.pi * R[1:] ** 3 * pint[1:]
                     - pb[1:] * (4 * m[1:] + 8 * np.pi * R[1:] ** 3 * pint[1:])) / R[1:] ** 2
        DtU = -(G2 / np.maximum(wint, 1e-300)) * gradP + grav
        DtU[0] = 0
        dR = ai * U
        dR[0] = 0
        return dR, ai * DtU, (e, m, pb, G2, Gz, dV, az, pz)

    k = np.sqrt(8 * np.pi * chi / 3)
    t, had, phimax, nstep, t_form = 0.0, False, 0.0, 0, None
    escaped = 0.0
    while t < tfac * M + 100 and nstep < maxsteps:
        N = len(R) - 1
        # remove an outer zone that is escaping: moving out, beyond 3 r_s, not trapped
        while N > 10 and U[-1] > 0 and R[-1] > 3 * rs:
            dVo = 4 * np.pi / 3 * (R[-1] ** 3 - R[-2] ** 3)
            e_o = state(R, U)[0][-1]
            escaped += e_o * dVo
            R, U, dmu = R[:-1], U[:-1], dmu[:-1]
            N -= 1
        rs_now = 2 * (M - escaped)
        dR1, dU1, aux = deriv(R, U)
        e, m, pb, G2, Gz, dV, az, pz = aux
        if not (np.all(np.isfinite(R)) and np.all(np.isfinite(U)) and np.all(np.isfinite(e))):
            bad = np.where(~np.isfinite(e))[0]
            return dict(T=None, ok=False, fail=f"NaN at t = {t:.3f}, zones {bad[:4]} of {N}",
                        t=t, phimax=phimax, steps=nstep, t_form=t_form, escaped=escaped / M)
        phimax = max(phimax, e.max() / chi)
        trapped = (G2[1:] < U[1:] ** 2).any() or (R[-1] < rs_now)
        if trapped:
            if not had:
                t_form = t
            had = True
        elif had:
            return dict(T=t, phimax=phimax, Rsurf=R[-1] / rs, steps=nstep, ok=True, t_form=t_form,
                        escaped=escaped / M, zones_left=N)
        cs = 0.0 if kind == "dust" else 1.0
        lim = [0.02 * np.min(R[1:] / np.maximum(np.abs(U[1:]), 1e-9)), 0.5]
        if law:
            lim.append(0.01 / (k * np.sqrt(max(pb.max(), 1e-12))))
        if kind != "dust":
            lim.append(cfl * np.min(np.diff(R) / Gz / np.maximum(az, 1e-300)))
        dt = min(lim)
        Rmid = R + dt / 2 * dR1
        if np.any(np.diff(Rmid) <= 0):
            j = np.where(np.diff(Rmid) <= 0)[0][0]
            return dict(T=None, ok=False, fail="shock", t=t, shock_R=R[j] / rs, shock_zone=j,
                        zones=N, phimax=phimax, escaped=escaped / M, t_form=t_form, e_shock=e[j] / chi)
        dR2, dU2, _ = deriv(Rmid, U + dt / 2 * dU1)
        dR3, dU3, _ = deriv(R + dt / 2 * dR2, U + dt / 2 * dU2)
        dR4, dU4, _ = deriv(R + dt * dR3, U + dt * dU3)
        Rn = R + dt / 6 * (dR1 + 2 * dR2 + 2 * dR3 + dR4)
        Un = U + dt / 6 * (dU1 + 2 * dU2 + 2 * dU3 + dU4)
        if not (np.all(np.isfinite(Rn)) and np.all(np.isfinite(Un))):
            jb = np.where(~(np.isfinite(Rn) & np.isfinite(Un)))[0]
            st = [np.all(np.isfinite(x)) for x in (dR1, dU1, dR2, dU2, dR3, dU3, dR4, dU4)]
            return dict(T=None, ok=False, fail=f"non-finite step at t={t:.3f}: interfaces {jb[:5]} of {N}; finite stages {st}; Rsurf {R[-1]:.3f} Usurf {U[-1]:.3f} rs_now {rs_now:.3f}; e_min {e.min():.2e}; Gamma solve err {state.err:.1e}",
                        t=t, phimax=phimax, escaped=escaped / M, t_form=t_form)
        if np.any(np.diff(Rn) <= 0):
            j = np.where(np.diff(Rn) <= 0)[0][0]
            return dict(T=None, ok=False, fail="shock", t=t, shock_R=R[j] / rs, shock_zone=j,
                        zones=N, phimax=phimax, escaped=escaped / M, t_form=t_form, e_shock=e[j] / chi)
        R, U = Rn, Un
        t += dt
        nstep += 1
        if verbose and nstep % 20000 == 0:
            print(f"  t={t:.3f} dt={dt:.1e} Rsurf/rs={R[-1]/rs:.3f} phimax={phimax:.3f}", flush=True)
        if verbose and nstep % 200 == 0:
            print(f"  step {nstep} t={t:.3f} dt={dt:.1e} Rsurf/rs={R[-1]/rs:.3f} Usurf={U[-1]:+.3f} "
                  f"Rin={R[1]:.2e} e_c={e[0]:.2e} trapped={trapped} lapse_c={az[0]:.2e}", flush=True)
    return dict(T=None, ok=False, fail="timeout", t=t, phimax=phimax, Rsurf=R[-1] / rs, steps=nstep,
                t_form=t_form, escaped=escaped / M)


def main():
    print("=" * 78 + "\nF0-F3  Collapse with pressure (MIMS law, Misner-Sharp, RK4)\n" + "=" * 78)
    d = run(2.0, kind="dust")
    print(f"   CHECK dust M = 2: T = {d['T']:.2f} (part 8: 7.53), peak fullness {d['phimax']:.4f}")
    out = {"dust": d}
    print("   EOS        M    horizon at   escaped   peak fullness   ends with")
    for kind, lab in (("stiff", "stiffening"), ("rad", "radiation")):
        for M in (2.0, 4.0):
            r = run(M, kind=kind, maxsteps=300000)
            out[(kind, M)] = r
            end = (f"shock at t = {r['t']:.2f} ({r['t']/M:.2f} M), R = {r['shock_R']:.2f} r_s"
                   if r.get("fail") == "shock" else f"stop at t = {r['t']:.2f} ({r['t']/M:.2f} M): "
                   "non-finite step (layers crossing inside a sub-step)")
            tf = r.get("t_form")
            print(f"   {lab:10s} {M:3.0f}   {tf if tf is None else round(tf/M, 2)} M     "
                  f"{r['escaped']:.3f}     {r['phimax']:7.3f}        {end}")
    print("   -> radiation pressure blows ~39% off; the stiffening holds the ceiling where plain")
    print("      radiation does not; a shock forms at ~8.7 M before the core is full.")
    print("   OPEN: shock capturing, to follow the bounce, the lifetime and the burst.")
    return out


if __name__ == "__main__":
    main()
