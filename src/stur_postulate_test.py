#!/usr/bin/env python3
"""
STUR open problem #1: test the postulate  S_R = -k_B ln(V/V0) = 1/2 k_B Phi_R^2
and its Landauer corollary  E_R = 1/2 k_B T Phi_R^2  against standard decoherence
theory.

Writing Gamma = -ln(V/V0) = 1/2 Phi_R^2, the postulate says
    (P1)  S/k_B   = Gamma                (visibility loss is entropy)
    (P2)  E_exch  = k_B T Gamma           (energy exchanged with the environment)
so at fixed E_exch, Gamma = E_exch/(k_B T): a colder interferometer loses more.

Models (all KNOWN PHYSICS, no STUR input):
  A. Pure-dephasing spin-boson, Ohmic J(w) = eta w exp(-w/wc), product initial
     state rho_S (x) rho_beta.  Solved exactly (analytic) and cross-checked by an
     independent truncated-Fock simulation with a few discrete modes.
  B. Caldeira-Leggett free particle in a two-branch superposition |+dx/2>+|-dx/2>.
     B1: recoilless (heavy-particle) limit - exactly model A with sigma_z -> 2x/dx.
     B2: high-T Markovian CL master equation, including the particle's motion.

Units: the analytic part of A uses hbar = k_B = 1 with frequencies in units of
wc; B2 uses SI.  Everything printed is computed here.

numpy + scipy required; matplotlib optional (plots are skipped without it).
"""
import os
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq
from scipy.linalg import eigh, expm

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "results", "postulate_test")

# SI constants (CODATA 2018 exact / recommended)
hbar = 1.054571817e-34
kB = 1.380649e-23
amu = 1.66053906660e-27


def banner(s):
    print("\n" + "=" * 74 + "\n" + s + "\n" + "=" * 74)


# ---------------------------------------------------------------------------
# A. Pure-dephasing spin-boson: exact formulas
#   H = Σ w_k b_k†b_k + sigma_z Σ g_k (b_k + b_k†)      (hbar = 1; H_S = w0 σz/2
#   commutes with everything and drops out)
#   Branch s = ±1 displaces mode k by  alpha_k(t) = s g_k (e^{-i w t} - 1)/w.
#   Coherence:   |rho01(t)/rho01(0)| = exp(-Gamma),
#       Gamma(t) = Σ 4 g_k^2 (1 - cos w_k t)/w_k^2 * coth(beta w_k / 2)
#   Bath energy: dE_B(t) = Σ w_k |alpha_k|^2 = Σ 2 g_k^2 (1 - cos w_k t)/w_k
#   (independent of T and of s);  <H_int> changes by -dE_B;  <H_S> constant.
#   Mode by mode:  Gamma_k = dE_k / [ k_B T * x_k tanh x_k ],  x_k = hbar w_k/(2 k_B T)
# ---------------------------------------------------------------------------
def gamma_k_over_E(x):
    """Gamma per unit energy for one mode, in units of 1/(k_B T): 1/(x tanh x)."""
    return 1.0 / (x * np.tanh(x))


def x_star():
    """Mode at which standard theory and the postulate agree: x tanh x = 1."""
    return brentq(lambda x: x * np.tanh(x) - 1.0, 0.1, 5.0)


def J_ohmic(w, eta=1.0, wc=1.0):
    return eta * w * np.exp(-w / wc)


def Gamma_ohmic(t, T, eta=1.0, wc=1.0, vacuum=True):
    """Exact decoherence function. vacuum=False keeps only the thermal part
    (coth - 1), i.e. subtracts the T=0 piece that includes reversible dressing."""
    def f(w):
        c = 1.0 / np.tanh(w / (2 * T)) if T > 0 else 1.0
        if not vacuum:
            c -= 1.0
        return 4 * J_ohmic(w, eta, wc) / w**2 * (1 - np.cos(w * t)) * c
    # split range for the oscillatory integrand
    edges = np.concatenate([[0], np.linspace(0, 60 * wc, 400)[1:]])
    return sum(quad(f, a, b, limit=200)[0] for a, b in zip(edges[:-1], edges[1:]))


def dEB_ohmic(t, eta=1.0, wc=1.0):
    """Bath energy change (T-independent). Closed form for Ohmic-exponential:
    2 eta ∫ e^{-w/wc}(1-cos wt) dw = 2 eta wc [1 - 1/(1+(wc t)^2)]."""
    return 2 * eta * wc * (1 - 1 / (1 + (wc * t) ** 2))


def S_qubit(Gamma):
    """von Neumann entropy (nats) of an equal-weight qubit with |rho01| = e^{-Gamma}/2."""
    c = np.exp(-np.asarray(Gamma, float))
    p = np.clip(np.stack([(1 + c) / 2, (1 - c) / 2]), 1e-300, 1)
    return -(p * np.log(p)).sum(0)


# ---------------------------------------------------------------------------
# A'. Independent check: qubit + N discrete modes, truncated Fock space.
#     Does not use any of the formulas above.
# ---------------------------------------------------------------------------
def vn(rho):
    ev = np.clip(eigh(rho, eigvals_only=True), 0, None)
    ev = ev[ev > 1e-14]
    return float(-(ev * np.log(ev)).sum())


def simulate(ws, gs, T, t, nmax=30):
    a = np.diag(np.sqrt(np.arange(1, nmax)), 1)
    n = a.T @ a
    I = np.eye(nmax)
    # per-mode thermal state and branch propagators
    rho_m, Up, Um, Hb = [], [], [], []
    for w, g in zip(ws, gs):
        p = np.exp(-w * np.arange(nmax) / T)
        p /= p.sum()
        rho_m.append(np.diag(p))
        Up.append(expm(-1j * t * (w * n + g * (a + a.T))))
        Um.append(expm(-1j * t * (w * n - g * (a + a.T))))
        Hb.append(w * n)

    def kron_all(ms):
        out = np.array([[1.0 + 0j]])
        for m in ms:
            out = np.kron(out, m)
        return out

    rb = kron_all(rho_m)
    U_p, U_m = kron_all(Up), kron_all(Um)
    HB = sum(kron_all([Hb[j] if j == k else I for j in range(len(ws))])
             for k in range(len(ws)))
    rp = U_p @ rb @ U_p.conj().T          # bath record if qubit is |0>
    rm = U_m @ rb @ U_m.conj().T          # bath record if qubit is |1>
    coh = np.trace(U_m.conj().T @ U_p @ rb)   # rho01(t)/rho01(0)
    V = abs(coh)
    rhoS = 0.5 * np.array([[1, coh], [np.conj(coh), 1]])
    rhoB = 0.5 * (rp + rm)
    dEB = float(np.real(np.trace(HB @ rhoB) - np.trace(HB @ rb)))
    S_S, S_B0, S_Bt = vn(rhoS), vn(rb), vn(rhoB)
    # Uhlmann fidelity between the two bath records
    ev, vec = eigh(rp)
    sq = vec @ np.diag(np.sqrt(np.clip(ev, 0, None))) @ vec.conj().T
    F = float(np.sum(np.sqrt(np.clip(eigh(sq @ rm @ sq, eigvals_only=True), 0, None))))
    # relative entropy D(rhoB(t) || rho_beta)
    lb = np.diag(np.log(np.clip(np.real(np.diag(rb)), 1e-300, None)))  # rb diagonal
    evB, vB = eigh(rhoB)
    evB = np.clip(evB, 1e-300, None)
    logB = vB @ np.diag(np.log(evB)) @ vB.conj().T
    D = float(np.real(np.trace(rhoB @ (logB - lb))))
    return dict(Gamma=-np.log(V), dEB=dEB, S_S=S_S, dS_B=S_Bt - S_B0,
                I=S_S + S_Bt - S_B0, Sigma=S_S + dEB / T, D=D, F=F)


def analytic_discrete(ws, gs, T, t):
    ws, gs = np.asarray(ws), np.asarray(gs)
    G = np.sum(4 * gs**2 * (1 - np.cos(ws * t)) / ws**2 / np.tanh(ws / (2 * T)))
    E = np.sum(2 * gs**2 * (1 - np.cos(ws * t)) / ws)
    return G, E


# ---------------------------------------------------------------------------
# B2. Caldeira-Leggett high-T master equation (SI)
#   drho/dt = -i/hbar[H,rho] - i gam/hbar [x,{p,rho}] - (2 m gam kB T/hbar^2)[x,[x,rho]]
#   => off-diagonal rho(x,x') decays at rate D (x-x')^2/hbar^2, D = 2 m gam kB T
#   => d<E_kin>/dt = -4 gam <E_kin> + 2 gam kB T   (gross in-flow 2 gam kB T)
# ---------------------------------------------------------------------------
def cl_numbers(m, dx, T, gam, t, E0=None):
    D = 2 * m * gam * kB * T
    Gamma = D * dx**2 * t / hbar**2
    Ein = 2 * gam * kB * T * t                       # heat in from the noise
    if E0 is None:
        E0 = 0.5 * kB * T                            # particle starts thermalised
    Eeq = 0.5 * kB * T
    Enet = (E0 - Eeq) * (np.exp(-4 * gam * t) - 1)   # net kinetic-energy change
    lam = hbar / np.sqrt(m * kB * T)
    return dict(Gamma=Gamma, E_post=kB * T * Gamma, E_in=Ein, E_net=Enet, lam=lam)


# ---------------------------------------------------------------------------
def main(make_plots=True):
    results = {}

    banner("A0  Single bosonic mode: where can the postulate hold?")
    xs = x_star()
    results["x_star"] = xs
    print(f"Standard:  Gamma_k = dE_k / (k_B T * x tanh x),  x = hbar w / (2 k_B T)")
    print(f"Postulate: Gamma   = dE   / (k_B T)")
    print(f"Equal only when x tanh x = 1  ->  x* = {xs:.6f},  hbar w* = {2*xs:.6f} k_B T")
    for x in [0.01, 0.1, 0.5, xs, 2.0, 5.0]:
        print(f"  hbar w/k_B T = {2*x:7.3f}   Gamma_std/Gamma_post = {gamma_k_over_E(x):10.4f}")
    print("High T (x<<1): Gamma_k -> 4 dE_k k_B T/(hbar w)^2  [grows with T at fixed dE]")
    print("Low  T (x>>1): Gamma_k -> 2 dE_k/(hbar w)          [T-independent]")

    banner("A1  Exact model vs independent Fock-space simulation (hbar=k_B=1)")
    ws, gs = [0.7, 1.3], [0.25, 0.35]
    rows = []
    for T in [0.3, 1.0, 3.0]:
        for t in [0.8, 2.0]:
            r = simulate(ws, gs, T, t, nmax=30 if T < 2 else 40)
            Ga, Ea = analytic_discrete(ws, gs, T, t)
            rows.append((T, t, r, Ga, Ea))
            print(f"T={T:3.1f} t={t:3.1f}  Gamma sim/an = {r['Gamma']:.6f}/{Ga:.6f}   "
                  f"dE_B sim/an = {r['dEB']:.6f}/{Ea:.6f}")
    results["sim_rows"] = rows
    print("\nSame runs - entropies (nats) vs postulate P1 (S/k_B = Gamma) and P2 (E = T Gamma):")
    print("  T    t   Gamma   S_sys   dS_bath  I(S:B)  Sigma=dS+bQ  -lnF   dE_B   T*Gamma")
    for T, t, r, Ga, Ea in rows:
        print(f"{T:4.1f} {t:4.1f} {r['Gamma']:7.4f} {r['S_S']:7.4f} {r['dS_B']:8.4f} "
              f"{r['I']:7.4f} {r['Sigma']:10.4f} {-np.log(r['F']):7.4f} {r['dEB']:7.4f} {T*r['Gamma']:8.4f}")
    err = max(abs(r["Sigma"] - (r["I"] + r["D"])) for _, _, r, _, _ in rows)
    print(f"Consistency check (Esposito-Lindenberg-Van den Broeck): Sigma = I + D(rho_B||rho_beta);"
          f" max |diff| = {err:.1e}")
    results["esposito_err"] = err
    r0 = simulate(ws, gs, 0.02, 2.0, nmax=30)
    results["fid_T0"] = (r0["Gamma"], -np.log(r0["F"]))
    print(f"T -> 0 (T=0.02, t=2): Gamma = {r0['Gamma']:.6f}, -ln F(bath records) = {-np.log(r0['F']):.6f}"
          f"  [equal for pure records: V = |<chi_0|chi_1>|, Englert distinguishability - not an entropy]")

    banner("A2  Ohmic bath, eta = 0.05, wc = 1: time dependence at fixed T")
    eta = 0.05
    for T in [0.1, 1.0, 10.0]:
        print(f"T = {T}")
        for t in [1, 10, 100, 1000]:
            G = Gamma_ohmic(t, T, eta)
            E = dEB_ohmic(t, eta)
            print(f"   t={t:5d}  Gamma={G:9.4f}  dE_B={E:.5f}  "
                  f"(k_BT Gamma)/dE_B = {T*G/E:9.3f}   S_sys/Gamma = {S_qubit(G)/G:.4f}")
    print("dE_B saturates at 2 eta wc; Gamma grows ~ 4 pi eta T t at long times: no fixed ratio.")

    banner("A3  Fixed energy exchanged: Gamma vs T (eta=0.05, wc t = 3, dE_B fixed)")
    t0 = 3.0
    E0 = dEB_ohmic(t0, eta)
    Ts = np.logspace(-2, 1.5, 36)
    G_full = np.array([Gamma_ohmic(t0, T, eta) for T in Ts])
    G_th = np.array([Gamma_ohmic(t0, T, eta, vacuum=False) for T in Ts])
    G_post = E0 / Ts
    results.update(Ts=Ts, G_full=G_full, G_th=G_th, G_post=G_post, E0=E0)
    print(f"dE_B = {E0:.5f} (hbar wc), identical at every T")
    for i in range(0, len(Ts), 5):
        print(f"  k_BT/hbar wc = {Ts[i]:8.4f}   Gamma_std = {G_full[i]:9.4f}   "
              f"Gamma_std(thermal only) = {G_th[i]:9.4f}   Gamma_postulate = {G_post[i]:10.4f}")
    slope = lambda y: np.polyfit(np.log(Ts[-8:]), np.log(y[-8:]), 1)[0]
    slope_lo = lambda y: np.polyfit(np.log(Ts[:6]), np.log(y[:6]), 1)[0]
    print(f"log-log slope d ln Gamma/d ln T, high T:  standard {slope(G_full):+.3f}, postulate {slope(G_post):+.3f}")
    print(f"log-log slope d ln Gamma/d ln T, low  T:  standard {slope_lo(G_full):+.3f}, "
          f"thermal-only {slope_lo(G_th):+.3f}, postulate {slope_lo(G_post):+.3f}")
    cross = Ts[np.argmin(abs(np.log(G_full / G_post)))]
    print(f"Curves cross once, near k_BT = {cross:.3f} hbar wc (a coincidence point, not an identity)")
    results["cross"] = cross

    banner("B1  Caldeira-Leggett, recoilless limit = model A with sigma_z -> 2x/dx")
    print("Same Gaussian influence functional; J_eff(w) = (m gam dx^2/(2 pi hbar)) w e^{-w/wc}.")
    print("All conclusions of A1-A3 carry over unchanged (Gamma ∝ T at fixed bath energy).")

    banner("B2  Caldeira-Leggett high-T master equation, Rb-87 atom, SI units")
    m = 86.909 * amu
    dx, gam, t = 1e-6, 1.0, 1e-3
    print(f"m = {m:.4e} kg, dx = {dx} m, gam = {gam} s^-1, t = {t} s")
    print("  T [K]     lam_th [m]   Gamma      E_post=k_BT*Gamma [J]  E_in(gross) [J]  "
          "E_net [J]  E_post/E_in")
    cl_rows = []
    for T in [1e-9, 1e-7, 1e-5, 1e-3, 1.0, 300.0]:
        r = cl_numbers(m, dx, T, gam, t)
        cl_rows.append((T, r))
        print(f"  {T:8.1e}  {r['lam']:10.3e}  {r['Gamma']:10.3e}  {r['E_post']:12.3e}  "
              f"{r['E_in']:15.3e}  {r['E_net']:9.1e}  {r['E_post']/r['E_in']:10.3e}")
    print("E_post/E_in = (dx/lam_th)^2 identically; Gamma/E_in = m dx^2/hbar^2 (T-independent).")
    print("A thermalised particle has E_net = 0 yet decoheres: postulate P2 would require Gamma = 0.")
    results["cl_rows"] = cl_rows

    if make_plots:
        try:
            plots(results, eta)
        except ImportError:
            print("\n(matplotlib not installed - plots skipped)")
    return results


def plots(R, eta):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    os.makedirs(OUT, exist_ok=True)
    C1, C2, C3, INK, MUTED = "#2a78d6", "#eb6834", "#1baf7a", "#0b0b0b", "#52514e"
    plt.rcParams.update({"font.size": 10, "axes.edgecolor": MUTED, "axes.labelcolor": INK,
                         "xtick.color": MUTED, "ytick.color": MUTED, "axes.grid": True,
                         "grid.color": "#e4e3df", "grid.linewidth": 0.6,
                         "axes.spines.top": False, "axes.spines.right": False,
                         "lines.linewidth": 2, "figure.facecolor": "#fcfcfb",
                         "axes.facecolor": "#fcfcfb", "savefig.facecolor": "#fcfcfb"})

    # 1. Gamma vs T at fixed energy
    fig, ax = plt.subplots(figsize=(6.4, 4.2))
    ax.loglog(R["Ts"], R["G_post"], color=C2, label="STUR postulate  Γ = ΔE/k_BT")
    ax.loglog(R["Ts"], R["G_full"], color=C1, label="Spin-boson, exact")
    ax.loglog(R["Ts"], R["G_th"], color=C3, ls="--", label="Spin-boson, thermal part only")
    ax.set_xlabel("k_B T / ħω_c")
    ax.set_ylabel("Visibility loss  Γ = −ln V")
    ax.set_title(f"Fixed bath energy ΔE_B = {R['E0']:.4f} ħω_c (Ohmic, η={eta}, ω_c t=3)",
                 fontsize=10, color=INK, loc="left")
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "gamma_vs_T_fixed_energy.png"), dpi=150)
    plt.close(fig)

    # 2. single-mode ratio
    x = np.logspace(-2, 1, 400)
    fig, ax = plt.subplots(figsize=(6.4, 4.2))
    ax.loglog(2 * x, gamma_k_over_E(x), color=C1, label="Standard: 1/(x tanh x)")
    ax.axhline(1, color=C2, label="STUR postulate: 1")
    ax.axvline(2 * R["x_star"], color=MUTED, lw=1, ls=":")
    ax.annotate(f"ħω = {2*R['x_star']:.2f} k_BT", (2 * R["x_star"] * 1.1, 30), color=MUTED)
    ax.set_xlabel("ħω / k_B T  (mode frequency)")
    ax.set_ylabel("Γ per unit energy  ×  k_B T")
    ax.set_title("One bosonic mode: visibility lost per unit energy given to it",
                 fontsize=10, color=INK, loc="left")
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "single_mode_ratio.png"), dpi=150)
    plt.close(fig)

    # 3. entropy vs Gamma
    G = np.logspace(-3, 1.5, 300)
    fig, ax = plt.subplots(figsize=(6.4, 4.2))
    ax.loglog(G, G, color=C2, label="STUR postulate  S/k_B = Γ")
    ax.loglog(G, S_qubit(G), color=C1, label="Qubit von Neumann entropy")
    ax.axhline(np.log(2), color=MUTED, lw=1, ls=":")
    ax.annotate("ln 2", (G[0] * 1.5, np.log(2) * 1.15), color=MUTED)
    ax.set_xlabel("Γ = −ln V")
    ax.set_ylabel("Entropy / k_B")
    ax.set_title("Entropy recorded vs visibility lost", fontsize=10, color=INK, loc="left")
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "entropy_vs_gamma.png"), dpi=150)
    plt.close(fig)
    print("\nPlots written to results/postulate_test/")


if __name__ == "__main__":
    main()
