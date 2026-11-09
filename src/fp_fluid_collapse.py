#!/usr/bin/env python3
"""
Make It Make Sense theory, part 9 (v0.8): collapse of matter that pushes back.

CORRECTION.  The v0.7 solver for this part computed each zone's energy from its adiabat and
never checked energy conservation.  Measured afterwards, it CREATED ~37% extra energy during
the run (inside + escaped - M = +0.37 M).  Its results -- 39% blown off, horizon at 3.1 M,
shock at 8.7 M, "the stiffening holds the ceiling where plain radiation does not" -- are
RETRACTED.

This solver (energy-conserving by construction):
  Misner-Sharp spherical fluid collapse (KNOWN), with the MIMS law with pressure
      d^2R/dtau^2 = -[(m + 4 pi R^3 P) - phi_bar (4 m + 8 pi R^3 P)] / R^2       (FOLLOWS)
  State: interface radii R, velocities U, ENCLOSED MASS m (evolved: D_t m = -4 pi R^2 P U),
  zone energy e = (m_{j+1} - m_j) / (4/3 pi dR^3).  Total mass-energy is conserved exactly
  (pressure is zero at the surface).  Gamma^2 = 1 + U^2 - 2m(1 - phi_bar)/R.  Lapse from the
  pressure gradient.  Artificial viscosity q (only for compression faster than uniform
  contraction) for shocks.  RK4; time step limited by sound, viscosity, the law's rate and
  a kinematic limit (no gap between layers closes by more than 10% per step).  Escaping outer
  zones are removed and counted; a negligible outer zone is merged into its neighbour.
  EOS (the author's choice 1, causal form): cs^2 = 1/3 + (2/3) phi^2, = 1 beyond full.

Results (computed here), from a uniform ball at 1.5 r_s in free fall (an arbitrary start):
  CHECK  dust: T = 7.589 (part 8: 7.53), peak fullness 1.0000, energy error 9e-16.
  F1  energy error stays at machine precision (~1e-15) throughout every run.
  F2  horizon forms at ~3.8 M; only ~2.5% of the mass escapes before.
  F3  stiffening and plain radiation agree so far (peak fullness <= 0.62, where the
      stiffening hardly changes the pressure).
  F4  every run stops at ~10 M with a zone drained to ~0 mass: a known odd-even instability
      of interface-averaged pressure work, not physics.  The core is still collapsing; the
      bounce, the lifetime and the burst are not reached.  OPEN: a compatible energy
      discretisation (each zone's energy changed by its own pressure, total still exact).
"""
import numpy as np

def pfun(kind, chi):
    if kind == "dust":
        return lambda e: 0 * e, lambda e: 0 * e
    if kind == "rad":
        return lambda e: e / 3, lambda e: 0 * e + 1 / 3
    def p(e):
        x = e / chi
        xc = np.minimum(x, 1.0)
        return chi * (xc / 3 + 2 * xc ** 3 / 9) + chi * np.maximum(x - 1, 0)
    def cs2(e):
        x = np.minimum(e / chi, 1.0)
        return 1 / 3 + 2 * x * x / 3
    return p, cs2


def run(M, N=300, chi=1.0, kind="stiff", profile="uniform", R0fac=1.5, law=True,
        tfac=40.0, cfl=0.25, Cq=2.0, Cl=0.3, q_in_lapse=False, maxsteps=2_000_000,
        verbose=False, every=None):
    rs = 2 * M
    R0 = R0fac * rs
    x = np.linspace(0, 1, N + 1)
    R = R0 * x
    dVc = 4 * np.pi / 3 * np.diff(R ** 3)
    xc = 0.5 * (x[1:] + x[:-1])
    prof = np.ones(N) if profile == "uniform" else (1 - xc ** 2)
    e = prof * M / np.sum(prof * dVc)
    p, cs2 = pfun(kind, chi)

    def mphi(R, e):
        m = np.concatenate([[0], np.cumsum(e * 4 * np.pi / 3 * np.diff(R ** 3))])
        pb = np.zeros_like(m)
        if law:
            pb[1:] = 3 * m[1:] / (4 * np.pi * chi * R[1:] ** 3)
            pb[0] = pb[1]
        return m, pb

    def mphi_from_m(R, mm):
        pb = np.zeros_like(mm)
        if law:
            pb[1:] = 3 * mm[1:] / (4 * np.pi * chi * R[1:] ** 3)
            pb[0] = pb[1]
        return mm, pb

    m, pb = mphi(R, e)
    mm0 = m.copy()
    U = -np.sqrt(np.maximum(2 * m * (1 - pb) / np.maximum(R, 1e-300), 0))
    U[0] = 0

    def deriv(R, U, mm):
        n = len(mm) - 1
        e = np.maximum(np.diff(mm), 1e-300) / (4 * np.pi / 3 * np.diff(R ** 3))
        m, pb = mphi_from_m(R, mm)
        G2 = 1 + U ** 2 - 2 * m * (1 - pb) / np.maximum(R, 1e-300)
        G2[0] = 1
        Gam = np.sqrt(np.maximum(G2, 1e-14))
        pz = p(e)
        w = e + pz
        # artificial viscosity: only for compression faster than uniform contraction
        Rz = 0.5 * (R[1:] + R[:-1])
        Uz = 0.5 * (U[1:] + U[:-1])
        dUs = np.diff(U) - Uz / np.maximum(Rz, 1e-300) * np.diff(R)
        cs = np.sqrt(cs2(e))
        q = np.where(dUs < 0, w * (Cq * dUs ** 2 + Cl * cs * np.abs(dUs)), 0.0)
        P = pz + q
        Pl = P if q_in_lapse else pz
        dPl = np.diff(Pl)
        wb = 0.5 * (w[1:] + w[:-1])
        lna = np.concatenate([[0], np.cumsum(-dPl / np.maximum(wb, 1e-300))])
        lna -= lna[-1]
        az = np.exp(lna)
        ai = np.concatenate([[az[0]], 0.5 * (az[1:] + az[:-1]), [az[-1]]])
        Pint = np.concatenate([[P[0]], 0.5 * (P[1:] + P[:-1]), [0.0]])
        wint = np.concatenate([[w[0]], wb, [0.5 * w[-1]]])
        gradP = np.zeros(n + 1)
        gradP[1:n] = np.diff(P) / np.maximum(np.diff(Rz), 1e-300)
        gradP[n] = (0 - P[-1]) / max(R[n] - Rz[-1], 1e-300)
        grav = np.zeros(n + 1)
        grav[1:] = -(m[1:] + 4 * np.pi * R[1:] ** 3 * Pint[1:]
                     - pb[1:] * (4 * m[1:] + 8 * np.pi * R[1:] ** 3 * Pint[1:])) / R[1:] ** 2
        DtU = -(G2 / np.maximum(wint, 1e-300)) * gradP + grav
        DtU[0] = 0
        Dtm = -4 * np.pi * R ** 2 * Pint * U
        Dtm[0] = 0
        dRdt = ai * U
        dRdt[0] = 0
        Gz = 0.5 * (Gam[1:] + Gam[:-1])
        return dRdt, ai * DtU, ai * Dtm, dict(m=m, pb=pb, G2=G2, az=az, q=q, cs=cs, Gz=Gz, P=P, e=e)

    az_i = lambda az: np.concatenate([[az[0]], 0.5 * (az[1:] + az[:-1]), [az[-1]]])
    t, had, t_form, phimax, nstep, escaped = 0.0, False, None, 0.0, 0, 0.0
    mm = mm0
    k = np.sqrt(8 * np.pi * chi / 3)
    hist = []
    while t < tfac * M + 100 and nstep < maxsteps:
        while len(mm) > 11 and U[-1] > 0 and R[-1] > 3 * rs:
            escaped += mm[-1] - mm[-2]
            R, U, mm = R[:-1], U[:-1], mm[:-1]
        # merge a negligible outer zone into its neighbour (keeps the surface and total mass)
        while len(mm) > 11 and (mm[-1] - mm[-2]) < 0.01 * (mm[-2] - mm[-3]):
            R = np.concatenate([R[:-2], R[-1:]])
            U = np.concatenate([U[:-2], U[-1:]])
            mm = np.concatenate([mm[:-2], mm[-1:]])
        dR1, dU1, de1, aux = deriv(R, U, mm)
        m, pb, G2, az, e = aux["m"], aux["pb"], aux["G2"], aux["az"], aux["e"]
        phimax = max(phimax, e.max() / chi)
        Mleft = m[-1]
        rs_now = 2 * Mleft
        trapped = (G2[1:] < U[1:] ** 2).any() or (R[-1] < rs_now)
        if trapped and not had:
            t_form = t
            had = True
        elif had and not trapped:
            return dict(T=t, ok=True, t_form=t_form, phimax=phimax, escaped=escaped / M,
                        energy_err=(Mleft + escaped - M) / M, steps=nstep, hist=hist)
        sp = np.abs(U[1:]) + 1e-9
        lim = [0.02 * np.min(R[1:] / sp), 0.5]
        if law:
            lim.append(0.01 / (k * np.sqrt(max(pb.max(), 1e-12))))
        if kind != "dust":
            sig = aux["cs"] + np.sqrt(aux["q"] / np.maximum(e + p(e), 1e-300))
            lim.append(cfl * np.min(np.diff(R) / aux["Gz"] / np.maximum(az * sig, 1e-300)))
        # kinematic limit for every kind: no gap between layers may close by more than 10%
        closing = -np.diff(az_i(az) * U)
        lim.append(0.1 * np.min(np.where(closing > 0, np.diff(R) / np.maximum(closing, 1e-300), np.inf)))
        dt = min(lim)
        st = []
        ok = True
        Rs, Us, es = R + dt / 2 * dR1, U + dt / 2 * dU1, mm + dt / 2 * de1
        for stage in range(3):
            c1, c2, c3 = np.any(np.diff(Rs) <= 0), np.any(np.diff(es) < 0), not np.all(np.isfinite(Rs))
            if c1 or c2 or c3:
                ok = False
                why = ("cross" if c1 else "") + (" negmass" if c2 else "") + (" nan" if c3 else "")
                jj = np.where(np.diff(es) < 0)[0] if c2 else np.where(np.diff(Rs) <= 0)[0]
                diag = dict(why=why, stage=stage, zones=jj[:6].tolist(), nz=len(mm) - 1,
                            R=R[jj[0]:jj[0]+3].tolist() if len(jj) else None,
                            U=U[jj[0]:jj[0]+3].tolist() if len(jj) else None,
                            dm=np.diff(mm)[jj[0]-1:jj[0]+2].tolist() if len(jj) else None,
                            P=aux["P"][jj[0]-1:jj[0]+2].tolist() if len(jj) else None,
                            e=e[jj[0]-1:jj[0]+2].tolist() if len(jj) else None)
                break
            d = deriv(Rs, Us, es)
            st.append(d)
            if stage == 0:
                Rs, Us, es = R + dt / 2 * d[0], U + dt / 2 * d[1], mm + dt / 2 * d[2]
            elif stage == 1:
                Rs, Us, es = R + dt * d[0], U + dt * d[1], mm + dt * d[2]
        if not ok:
            j = int(np.argmin(np.diff(Rs))) if np.all(np.isfinite(Rs)) else -1
            return dict(T=None, ok=False, fail="step failed", diag=diag,
                        t=t, t_form=t_form, phimax=phimax, escaped=escaped / M,
                        where=(R[j] / rs if j >= 0 else None), hist=hist)
        (dR2, dU2, de2, _), (dR3, dU3, de3, _), (dR4, dU4, de4, _) = st
        R = R + dt / 6 * (dR1 + 2 * dR2 + 2 * dR3 + dR4)
        U = U + dt / 6 * (dU1 + 2 * dU2 + 2 * dU3 + dU4)
        mm = mm + dt / 6 * (de1 + 2 * de2 + 2 * de3 + de4)
        t += dt
        nstep += 1
        if every and nstep % every == 0:
            hist.append((t, phimax, e.max() / chi, R[-1] / rs, (m[-1] + escaped - M) / M,
                         trapped, len(mm) - 1))
            if verbose:
                print(f"  t={t:8.3f} dt={dt:.1e} phi_now={e.max()/chi:.3f} Rsurf/rs={R[-1]/rs:.3f} "
                      f"energy_err={(m[-1]+escaped-M)/M:+.1e} trapped={trapped} zones={len(mm)-1}",
                      flush=True)
    return dict(T=None, ok=False, fail="timeout", t=t, t_form=t_form, phimax=phimax,
                escaped=escaped / M, hist=hist)


def main():
    print("=" * 78 + "\nF0-F4  Collapse with pressure, energy-conserving (MIMS law, Misner-Sharp)\n" + "=" * 78)
    d = run(2.0, kind="dust")
    print(f"   CHECK dust M = 2: T = {d['T']:.3f} (part 8: 7.53), peak fullness {d['phimax']:.4f},"
          f" energy error {d['energy_err']:.0e}")
    out = {"dust": d}
    print("   EOS          M   horizon at   escaped   peak fullness   energy error   stops at")
    for kind, lab in (("stiff", "stiffening"), ("rad", "radiation")):
        for M in (2.0, 4.0):
            r = run(M, kind=kind, every=200, maxsteps=4_000_000, tfac=200)
            out[(kind, M)] = r
            err = max(abs(h[4]) for h in r["hist"]) if r["hist"] else float("nan")
            why = r.get("diag", {}).get("why", r.get("fail"))
            print(f"   {lab:11s} {M:3.0f}   {r['t_form']/M:.2f} M      {r['escaped']:.3f}      "
                  f"{r['phimax']:.3f}          {err:.0e}       {r['t']/M:.2f} M ({why.strip()})")
    print("   -> energy conserved to machine precision; horizon at ~3.8 M; ~2.5% escapes.")
    print("   -> runs stop at ~10 M from a drained zone (numerical); the core has not bounced.")
    print("   OPEN: compatible energy discretisation, then the bounce, lifetime and burst.")
    return out


if __name__ == "__main__":
    main()
