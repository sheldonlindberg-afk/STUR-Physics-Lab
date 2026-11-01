#!/usr/bin/env python3
"""
STUR open problem #1, part 2: list every assumption behind the postulate test,
vary each one, and search for any choice under which standard physics
reproduces the postulate

    (P1)  S / k_B = Gamma,            Gamma = -ln(V/V0) = 1/2 Phi_R^2
    (P2)  E_exchanged = k_B T Gamma

Every agreement found is classified:
    IDENTITY     holds to numerical precision over the whole scanned grid
    LIMIT        holds only asymptotically (T -> 0, T -> inf, t -> 0, ...)
    COINCIDENCE  holds only on a line/surface in parameter space
    NONE         never holds in the scanned range

Sections
  S1  Gaussian-noise assumption (V = exp(-1/2<phi^2>)): spin bath.
  S2  Entropy candidates for P1 (one bosonic mode, exact Fock-space numerics).
  S3  Energy and temperature candidates for P2 (same grid).
  S4  Spectral exponent s, time and initial-state convention (Ohmic family).
  S5  Dissipative qubit (energy really leaves the system): generalised
      amplitude damping.
  S6  Scattering decoherence by thermal photons (Joos-Zeh, saturated regime).
  S7  The black-hole consistency check: E_R = T_H S_BH vs energy actually radiated.

hbar = k_B = 1 in S1-S5 (mode frequency w = 1 unless stated); SI in S6-S7.
numpy + scipy required; matplotlib optional.
"""
import os
import numpy as np
from scipy.linalg import eigh, expm
from scipy.optimize import brentq
from scipy.special import zeta, gamma as Gfn

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "results", "assumption_scan")
REL_TOL_IDENTITY = 1e-6
MATCH_BAND = np.log(1.1)          # "match" = within 10 %


def banner(s):
    print("\n" + "=" * 78 + "\n" + s + "\n" + "=" * 78)


def classify(ratio, label, extra=""):
    """ratio = candidate / postulate quantity on a grid (array)."""
    r = np.asarray(ratio, float)
    lr = np.log(r[np.isfinite(r) & (r > 0)])
    if lr.size == 0:
        verdict = "NONE (candidate is zero or undefined)"
    elif lr.max() - lr.min() < REL_TOL_IDENTITY and abs(lr.mean()) < REL_TOL_IDENTITY:
        verdict = "IDENTITY"
    elif lr.max() - lr.min() < REL_TOL_IDENTITY:
        verdict = f"IDENTITY up to constant factor {np.exp(lr.mean()):.6g}"
    else:
        frac = np.mean(np.abs(lr) < MATCH_BAND)
        verdict = ("NONE in range" if frac == 0 else
                   f"COINCIDENCE ({100*frac:.1f}% of grid within 10%)")
    print(f"  {label:<44s} ratio range [{r.min():9.3g}, {r.max():9.3g}]  -> {verdict} {extra}")
    return verdict


# ---------------------------------------------------------------------------
# Single bosonic mode helpers (hbar = k_B = w = 1)
# ---------------------------------------------------------------------------
def vn(rho):
    ev = eigh(rho, eigvals_only=True)
    ev = ev[ev > 1e-15]
    return float(-(ev * np.log(ev)).sum())


def msqrt(rho):
    ev, v = eigh(rho)
    return v @ np.diag(np.sqrt(np.clip(ev, 0, None))) @ v.conj().T


def mlog(rho):
    ev, v = eigh(rho)
    return v @ np.diag(np.log(np.clip(ev, 1e-300, None))) @ v.conj().T


def one_mode(alpha2, T, N=None):
    """Pure dephasing of an equal-weight qubit by one mode at temperature T.
    Branch s displaces the mode by s*alpha (alpha real, alpha2 = alpha^2 = mean
    quanta added per branch).  Returns every candidate quantity."""
    nbar = 1 / np.expm1(1 / T)
    if N is None:
        N = int(max(60, 30 * (nbar + 1) + 12 * alpha2 + 40))
    al = np.sqrt(alpha2)
    a = np.diag(np.sqrt(np.arange(1, N)), 1)
    n = np.arange(N)
    p = np.exp(-n / T)
    p /= p.sum()
    rb = np.diag(p)
    D = expm(al * (a.T - a))                       # D(alpha)
    rp, rm = D @ rb @ D.T, D.T @ rb @ D            # bath records
    c = np.trace(D @ D @ rb)                       # Tr D(2 alpha) rho_beta
    Gam = -np.log(abs(c))
    rS = 0.5 * np.array([[1, c], [c, 1]])
    rB = 0.5 * (rp + rm)
    S_beta, S_B, S_S = vn(rb), vn(rB), vn(rS)
    Q = float(np.trace(np.diag(n) @ rB) - (n * p).sum())
    # two-point-measurement heat statistics (exact, from |<m|D|n>|^2)
    P = np.abs(D) ** 2
    dn = n[:, None] - n[None, :]
    w = P * p[None, :]
    VarQ = float((w * dn**2).sum() - (w * dn).sum() ** 2)
    sq = msqrt(rp)
    F = float(np.sum(np.sqrt(np.clip(eigh(sq @ rm @ sq, eigvals_only=True), 0, None))))
    petz_half = float(-2 * np.log(np.trace(msqrt(rp) @ msqrt(rm)).real))
    logp = -n / T - np.log(np.sum(np.exp(-n / T)))      # analytic, no underflow
    relent = lambda r: float(np.trace(r @ mlog(r)).real - np.real(np.diag(r)) @ logp)
    Drel = relent(rB)                              # D(rho_B || rho_beta)
    # records are unitary images of rho_beta, so S(record) = S(rho_beta) and
    # ln(record1) = D^T ln(rho_beta) D exactly: no matrix log of near-pure states
    plogp = float(p @ logp)
    D_rec = plogp - float(np.real(np.diag(rp)) @ logp)          # D(record0 || rho_beta)
    D_pm = plogp - float(np.trace(rp @ (D.T @ np.diag(logp) @ D)).real)  # D(record0||record1)
    return dict(Gamma=Gam, Gamma_an=2 * alpha2 / np.tanh(1 / (2 * T)), nbar=nbar,
                S_S=S_S, S2_S=-np.log(np.trace(rS @ rS).real), dS_B=S_B - S_beta,
                I=S_S + S_B - S_beta, Sigma=S_S + Q / T, D=Drel, mlnF=-np.log(F),
                petz=petz_half, D_rec=D_rec, D_pm=D_pm, Q=Q, VarQ=VarQ, T=T, a2=alpha2,
                Teff=0.5 / np.tanh(1 / (2 * T)))


# ---------------------------------------------------------------------------
def S1_gaussian():
    banner("S1  Assumption: Gaussian phase noise.  Test: central spin + Ising spin bath")
    print("H = sigma_z * sum_k c_k tau_z^k + sum_k h tau_z^k.  Every term commutes:")
    print("system, bath and interaction energies are each EXACTLY conserved.")
    rng = np.random.default_rng(1)
    for Nb in [3, 30, 300]:
        c = rng.uniform(0.5, 1.5, Nb) / np.sqrt(Nb)
        beta_h = 0.3                                   # thermal polarisation tanh(beta h)
        m = np.tanh(beta_h)
        ts = np.linspace(0.05, 3, 60)
        # exact: <e^{i phi}> = prod_k [cos(2 c_k t) + i m sin(2 c_k t)]
        V = np.abs(np.prod(np.cos(2 * np.outer(ts, c)) + 1j * m * np.sin(2 * np.outer(ts, c)), 1))
        G = -np.log(np.clip(V, 1e-300, None))
        half_var = 0.5 * (1 - m**2) * (2 * np.outer(ts, c)) ** 2 @ np.ones(Nb)   # 1/2 Var(phi)
        dev = np.max(np.abs(G - half_var) / half_var)
        mono = np.all(np.diff(G) > 0)
        print(f"  N_bath = {Nb:4d}: max |(-lnV) - 1/2 Var(phi)| / (1/2 Var) = {dev:8.3f};"
              f"  -ln V monotone in t: {mono}")
    print("  Energy exchanged with any subsystem = 0 exactly, yet Gamma > 0:")
    print("  P2 (E = k_B T Gamma > 0) fails for every T > 0.  [Caveat: bath state is")
    print("  diagonal, so this dephasing is echo-reversible; a STUR restriction to")
    print("  irreversible decoherence would exclude it.]")


def S2_S3_one_mode():
    banner("S2  Assumption: 'entropy' in P1.  One mode, grid of T and quanta per branch")
    Ts = np.array([0.05, 0.1, 0.2, 0.4, 0.8, 1.6, 3.2, 6.4])
    a2s = np.array([0.002, 0.01, 0.05, 0.2, 0.5, 1.0])
    rows = [one_mode(a2, T) for T in Ts for a2 in a2s]
    G = np.array([r["Gamma"] for r in rows])
    err = max(abs(r["Gamma"] - r["Gamma_an"]) / r["Gamma_an"] for r in rows)
    print(f"  Fock numerics vs Gamma = 2 alpha^2 coth(w/2T): max rel. error {err:.1e}")
    get = lambda k: np.array([r[k] for r in rows])
    out = {}
    print("  candidate X                                  X/Gamma over grid")
    for k, lab in [("S_S", "von Neumann entropy, system"),
                   ("S2_S", "Renyi-2 entropy, system (-ln purity)"),
                   ("dS_B", "bath entropy change = Holevo chi of records"),
                   ("I", "mutual information I(S:B)"),
                   ("Sigma", "entropy production dS_S + Q/T"),
                   ("D", "D(rho_B || rho_beta) = bath free energy / T"),
                   ("mlnF", "-ln Uhlmann fidelity of records"),
                   ("petz", "Petz Renyi-1/2 divergence of records")]:
        out[k] = classify(get(k) / G, lab)
    # limits for fidelity
    lowT = [r for r in rows if r["T"] == Ts[0]]
    print(f"  -ln F / Gamma at T = {Ts[0]}: "
          + ", ".join(f"{r['mlnF']/r['Gamma']:.6f}" for r in lowT)
          + "   -> LIMIT T->0 (pure records: V = |<chi0|chi1>|, KNOWN)")
    print(f"  max over grid of (-ln F)/Gamma = {np.max(get('mlnF')/G):.6f}  (<= 1: Uhlmann bound, KNOWN)")
    out["D_rec"] = classify(get("D_rec") / G, "D(record || thermal state)")
    small = [r for r in rows if r["Gamma"] < 0.02]
    print(f"  Renyi-2 / Gamma for the {len(small)} points with Gamma < 0.02: "
          f"[{min(r['S2_S']/r['Gamma'] for r in small):.4f}, {max(r['S2_S']/r['Gamma'] for r in small):.4f}]"
          "  -> LIMIT Gamma->0: S_2 = ln2 - ln(1+V^2) = Gamma - Gamma^2 + ... (FOLLOWS, trivial)")
    print(f"  ...but S_2 <= ln 2 = {np.log(2):.4f} while Gamma is unbounded: fails once Gamma ~ 0.1")
    out["quanta"] = classify(2 * get("VarQ") / G,
                             "2 Var(Q)/(hbar w)^2  [TPM heat fluctuation]",
                             "<- new-to-this-project, model-exact")

    banner("S3  Assumptions: 'energy exchanged' and 'temperature' in P2 (same grid)")
    print("  candidate E / (k_B T* Gamma)")
    T = get("T")
    for E, lab in [(np.zeros_like(G), "dE_system (pure dephasing)"),
                   (get("Q"), "<Q> = dE_bath (= -dE_int)"),
                   (np.sqrt(get("VarQ")), "rms heat sqrt(Var Q)"),
                   (T * get("D"), "bath free-energy gain T D"),
                   (T * get("I"), "Landauer cost to erase S-B correlation T I")]:
        with np.errstate(divide="ignore", invalid="ignore"):
            out["E:" + lab] = classify(E / (T * G), lab + ",  T* = T_bath")
    Teff = get("Teff")
    out["E:Teff"] = classify(get("Q") / (Teff * G), "<Q>, T* = noise temp (hw/2)coth(hw/2T)")
    print("  --- keep E = <Q>, but replace the entropy -ln V by other record measures ---")
    out["P2:D_rec"] = classify(get("Q") / (T * get("D_rec")),
                               "<Q> / (k_B T D(record||rho_beta))", "<- KNOWN (Esposito et al. 2010)")
    out["P2:D_pm"] = classify(get("Q") / (T * get("D_pm")),
                              "<Q> / (k_B T D(record0||record1))", "<- = 1/4: same identity, Gaussian")
    out["P2:Fnoise"] = classify(get("Q") / (Teff * get("mlnF")),
                                "<Q> / (k_B T_noise (-ln F))", "<- FOLLOWS (Gaussian fidelity)")
    hiT = np.array([r["Q"] / (r["T"] * r["mlnF"]) for r in rows if r["T"] >= 3.2])
    print(f"  <Q> / (k_B T (-ln F)) for T >= 3.2 hbar w: [{hiT.min():.4f}, {hiT.max():.4f}]  -> LIMIT T->inf")
    print(f"  Quantum floor: min over grid of Gamma / (2<Q>/hbar w) = "
          f"{np.min(G / (2 * get('Q'))):.6f}  (= coth >= 1; vacuum bound)")
    print("    => P2 needs Gamma_k = <Q_k>/k_BT, below this floor whenever hbar w < 2 k_B T:")
    print("       impossible there for any thermal or coherent-mixture bath state.")
    Treq = get("Q") / G
    print(f"  Temperature that WOULD make <Q> = k_B T* Gamma: T* = (hbar w/2) tanh(hbar w/2T);"
          f" check max rel err {np.max(abs(Treq - 0.5*np.tanh(0.5/T))/Treq):.1e}")
    print("    -> T* <= hbar w/2 always; T* -> hbar w/2 (T->0), -> (hbar w)^2/(4T) (T->inf):")
    print("       it FALLS as the bath gets hotter. No thermometer reads this.")
    xs = brentq(lambda x: x * np.tanh(x) - 1, 0.1, 5)
    print(f"  <Q> = k_B T Gamma exactly on the line hbar w = {2*xs:.6f} k_B T (COINCIDENCE).")
    return rows, out


# ---------------------------------------------------------------------------
# S4: Ohmic family J = eta w^s wc^{1-s} e^{-w/wc}; vectorised integrals
# ---------------------------------------------------------------------------
_u = np.linspace(1e-6, np.sqrt(60.0), 120001)        # w = u^2 (handles w->0)
_w = _u**2
_dw = 2 * _u * np.gradient(_u)


def gamma_E(s, T, t, eta=0.05, thermal_only=False):
    J = eta * _w**s * np.exp(-_w)
    cth = 1 / np.tanh(_w / (2 * T)) - (1.0 if thermal_only else 0.0)
    oc = 1 - np.cos(_w * t)
    G = np.sum(4 * J / _w**2 * oc * cth * _dw)
    E = np.sum(2 * J / _w * oc * _dw)
    return G, E


def S4_spectrum():
    banner("S4  Assumptions: spectral exponent s, time t, initial-state convention")
    Ts = np.logspace(-2, 1.5, 36)
    ts = np.logspace(-0.5, 2, 26)
    maps = {}
    for s in [0.5, 1.0, 2.0, 3.0]:
        for th in [False, True]:
            R = np.empty((len(ts), len(Ts)))
            for i, t in enumerate(ts):
                for j, T in enumerate(Ts):
                    G, E = gamma_E(s, T, t, thermal_only=th)
                    R[i, j] = T * G / E                    # k_B T Gamma / dE_B
            maps[(s, th)] = R
            frac = np.mean(np.abs(np.log(R)) < MATCH_BAND)
            # slope in T at fixed energy (energy is T-independent) at mid time
            i0 = len(ts) // 2
            sl_hi = np.polyfit(np.log(Ts[-8:]), np.log(R[i0, -8:] / Ts[-8:]), 1)[0]
            sl_lo = np.polyfit(np.log(Ts[:6]), np.log(R[i0, :6] / Ts[:6]), 1)[0]
            print(f"  s={s:3.1f} {'thermal-only' if th else 'full        '}  "
                  f"grid within 10% of P2: {100*frac:5.1f}%   d lnGamma/d lnT at fixed E: "
                  f"low T {sl_lo:+.2f}, high T {sl_hi:+.2f}   (postulate -1)")
    G, E = gamma_E(1.0, 1.0, 3.0)
    print(f"  integrator check vs quad (s=1,T=1,t=3): Gamma={G:.5f} (quad: 1.06740), "
          f"dE={E:.5f} (closed form 0.09000)")
    print("  Product vs equilibrated-|0> initial state: same relative displacement, so")
    print("  Gamma and <Q> are identical (shown analytically in POSTULATE/ASSUMPTIONS docs).")
    return Ts, ts, maps


# ---------------------------------------------------------------------------
def S5_gad():
    banner("S5  Assumption: pure dephasing.  Dissipative qubit (GAD, Markov, hbar w0 = x k_B T)")
    print("  Gamma(t) = gam (2n+1) t / 2;  p_e(t) = p_eq + (1/2 - p_eq) e^{-gam(2n+1)t}")
    out = {}
    xs = np.logspace(-1.5, 1.5, 61)
    taus = np.logspace(-4, 0.5, 46)                   # gam t
    Rnet, Rgross, Rq = [], [], []
    for x in xs:
        n = 1 / np.expm1(x)
        k = 2 * n + 1
        peq = n / k
        for tau in taus:
            Gam = k * tau / 2
            pe = peq + (0.5 - peq) * np.exp(-k * tau)
            Enet = x * abs(pe - 0.5)                  # units of k_B T
            # gross quanta: integral of gam[(n+1)p_e + n p_g] = gam[n + p_e]
            Ngross = n * tau + peq * tau + (0.5 - peq) * (1 - np.exp(-k * tau)) / k
            Rnet.append(Enet / Gam)
            Rgross.append(x * Ngross / Gam)
            Rq.append(Ngross / Gam)
    Rnet, Rgross, Rq = map(np.array, (Rnet, Rgross, Rq))
    out["net"] = classify(Rnet, "|dE_S| net / (k_B T Gamma)")
    out["gross"] = classify(Rgross, "gross energy in+out / (k_B T Gamma)")
    out["quanta"] = classify(Rq, "gross quanta exchanged / Gamma")
    short = Rq.reshape(len(xs), len(taus))[:, 0]
    print(f"  gross quanta / Gamma at gam t = 1e-4, all x: [{short.min():.6f}, {short.max():.6f}]"
          "  -> LIMIT t->0: Gamma = number of quantum jumps (KNOWN, quantum trajectories)")
    xstar = brentq(lambda x: x * np.tanh(x / 2) - 1, 0.1, 10)
    print(f"  short-time net:   |dE_S|/(k_BT Gamma) -> x tanh(x/2); = 1 at hbar w0 = {xstar:.6f} k_B T")
    print(f"  short-time gross: E/(k_BT Gamma) -> x;          = 1 at hbar w0 = 1 k_B T")
    print("  Same coth (fluctuation-dissipation) factor as pure dephasing, but a different")
    print("  prefactor, so the crossing moves (2.40 -> 1.54 k_BT): it is model-dependent.")
    return out


def S6_photons():
    banner("S6  Thermal-photon scattering decoherence (Rayleigh, saturated: dx >> photon wavelength)")
    print("  Each scattered photon carries full which-path information: Gamma = N_scattered.")
    r = 8 * zeta(8) * Gfn(8) / (zeta(7) * Gfn(7)) / 8      # <hbar w> / k_B T for flux*w^4 weighting
    print(f"  Mean scattered-photon energy  <hbar w> = 7 zeta(8)/zeta(7) k_B T = {r:.4f} k_B T")
    hbar, kB, c, amu, eV = 1.054571817e-34, 1.380649e-23, 2.99792458e8, 1.66053906660e-27, 1.602176634e-19
    M = 86.909 * amu
    for T in [300.0, 4.0]:
        # mean recoil energy per scattering, isotropic: <(hbar dk)^2>/2M with <dk^2> = 2k^2
        k2 = (kB * T / (hbar * c)) ** 2 * Gfn(9) * zeta(9) / (Gfn(7) * zeta(7))
        Erec = hbar**2 * 2 * k2 / (2 * M)
        print(f"  T={T:6.1f} K, Rb-87:  energy passed through / (k_B T Gamma) = {r:.3f};"
              f"  energy deposited (recoil) / (k_B T Gamma) = {Erec/(kB*T):.3e}")
    print("  P2 with 'energy passed through': off by x7 (NONE). With energy deposited: off by ~1e-11.")
    return r


def S7_blackhole():
    banner("S7  The passed consistency check: is T_H S_BH the energy exchanged?")
    G, c, hbar, kB, Ms = 6.67430e-11, 2.99792458e8, 1.054571817e-34, 1.380649e-23, 1.98847e30
    M = Ms
    TH = lambda m: hbar * c**3 / (8 * np.pi * G * m * kB)
    SBH = lambda m: 4 * np.pi * G * m**2 * kB / (hbar * c)
    ms = np.linspace(1e-9, 1, 200001) * M
    dS = 8 * np.pi * G * ms * kB / (hbar * c)            # dS_BH/dm, analytic
    W = np.trapezoid(TH(ms) * dS, ms) if hasattr(np, "trapezoid") else np.trapz(TH(ms) * dS, ms)
    print(f"  E_R = T_H S_BH                 = {TH(M)*SBH(M)/(M*c**2):.6f} Mc^2   (Smarr: the record's check)")
    print(f"  energy radiated  int T_H dS_BH = {W/(M*c**2):.6f} Mc^2   (first law; all of M is exchanged)")
    print(f"  entropy carried by quasi-static blackbody radiation = 4/3 S_BH = {4/3:.6f} S_BH")
    print("  If E_R is 'energy exchanged with the environment', the black-hole case gives 1/2,")
    print("  not 1: the Smarr check verifies M = 2 T S (a virial identity), not P2.")


# ---------------------------------------------------------------------------
def plots(Ts, ts, maps):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.colors import LinearSegmentedColormap, TwoSlopeNorm
    os.makedirs(OUT, exist_ok=True)
    INK, MUTED = "#0b0b0b", "#52514e"
    cmap = LinearSegmentedColormap.from_list("div", ["#2a78d6", "#e4e3df", "#eb6834"])
    plt.rcParams.update({"font.size": 9, "axes.edgecolor": MUTED, "xtick.color": MUTED,
                         "ytick.color": MUTED, "figure.facecolor": "#fcfcfb",
                         "savefig.facecolor": "#fcfcfb"})
    fig, axs = plt.subplots(2, 4, figsize=(12, 5.6), sharex=True, sharey=True)
    norm = TwoSlopeNorm(vmin=-4, vcenter=0, vmax=4)
    for col, s in enumerate([0.5, 1.0, 2.0, 3.0]):
        for row, th in enumerate([False, True]):
            ax = axs[row, col]
            L = np.log10(maps[(s, th)])
            im = ax.pcolormesh(Ts, ts, L, cmap=cmap, norm=norm, shading="auto")
            ax.contour(Ts, ts, L, levels=[0], colors=INK, linewidths=1.5)
            ax.set_xscale("log"); ax.set_yscale("log")
            ax.set_title(f"s = {s}, {'thermal part' if th else 'full'}", fontsize=9,
                         color=INK, loc="left")
            if row == 1: ax.set_xlabel("k_B T / ħω_c")
            if col == 0: ax.set_ylabel("ω_c t")
    cb = fig.colorbar(im, ax=axs, shrink=0.8)
    cb.set_label("log₁₀ [ k_B T Γ / ΔE_B ]   (0 = postulate holds)")
    fig.suptitle("Where standard dephasing matches the STUR postulate (black line); "
                 "orange: postulate under-predicts Γ, blue: over-predicts",
                 fontsize=10, color=INK, x=0.02, ha="left")
    fig.savefig(os.path.join(OUT, "match_map_spectral_family.png"), dpi=140)
    plt.close(fig)
    print("\nPlot written to results/assumption_scan/")


def main(make_plots=True):
    S1_gaussian()
    rows, out23 = S2_S3_one_mode()
    Ts, ts, maps = S4_spectrum()
    out5 = S5_gad()
    S6_photons()
    S7_blackhole()
    if make_plots:
        try:
            plots(Ts, ts, maps)
        except ImportError:
            print("\n(matplotlib not installed - plot skipped)")
    return dict(rows=rows, out23=out23, maps=maps, out5=out5)


if __name__ == "__main__":
    main()
