#!/usr/bin/env python3
"""
Gravity-induced entanglement (Bose et al., PRL 119, 240401 (2017); Marletto & Vedral,
PRL 119, 240402 (2017)). Gravity is TEGR's torsion field; at these scales its phases are
the weak-field ones below, recomputed from the TEGR field energy in stur_tegr_gr.py
(F3-F4, agreement 6e-16 rad; next order 1e-24).

Two masses m, each put into a two-path superposition of size dx, held for a time tau.
Only gravity acts between them. The question is the gravitational version of T5 in
stur_measurement.py: is gravity's field in two places as an AMPLITUDE, or as one
classical average (a "split" field)?

  Q (amplitude, lambda = 1): each branch pair (i, j) picks up its own phase
        phi_ij = G m^2 tau / (hbar r_ij)                               (KNOWN)
     The four phases do not factor, so the masses become entangled.
  C (split / mean field, lambda = 0): each mass feels the AVERAGE field of the other,
        phi_i^A = sum_j p_j G m^2 tau / (hbar r_ij)
     These are local phases only: the state stays a product. Concurrence is exactly 0.
  Interpolation (PROPOSAL, the one free parameter): a fraction lambda of the interaction
     acts as an amplitude and (1 - lambda) as the mean field. Entanglement grows with
     lambda, so the experiment MEASURES lambda.

Also modelled: dephasing (gas collisions), the Casimir-Polder background that sets the
closest allowed approach, the mean-field self-gravity of one split mass (the analogue of
T5's self-repulsion), and the number of runs needed to see the entanglement witness.
Labels: KNOWN, FOLLOWS, LIT (input taken from the literature), PROPOSAL.
"""
import numpy as np

G = 6.67430e-11
HBAR = 1.054571817e-34
C = 2.99792458e8
KB = 1.380649e-23
RHO_DIAMOND = 3510.0
EPS_DIAMOND = 5.7
M_N2 = 28 * 1.66053907e-27

# LIT: Bose et al. 2017 baseline
BASE = dict(m=1e-14, dx=250e-6, gap=200e-6, tau=2.5)

I2 = np.eye(2)
SX = np.array([[0, 1], [1, 0]], complex)
SY = np.array([[0, -1j], [1j, 0]], complex)
SZ = np.diag([1.0 + 0j, -1.0])


def banner(s):
    print("\n" + "=" * 78 + "\n" + s + "\n" + "=" * 78)


def radius(m):
    return (3 * m / (4 * np.pi * RHO_DIAMOND)) ** (1 / 3)


def branch_distances(dx, gap, geometry="linear"):
    """r[i, j]: distance between branch i of mass A and branch j of mass B.
    linear:   A_L A_R ... B_L B_R on one line; nearest branches are `gap` apart.
    parallel: both superpositions perpendicular to the line joining them, `gap` apart."""
    if geometry == "linear":
        xa = np.array([0.0, dx])
        xb = np.array([dx + gap, 2 * dx + gap])
        return np.abs(xa[:, None] - xb[None, :])
    ya = np.array([0.0, dx])
    yb = np.array([0.0, dx])
    return np.sqrt(gap**2 + (ya[:, None] - yb[None, :]) ** 2)


def phases(m, dx, gap, tau, geometry="linear", lam=1.0):
    """4 branch phases. lam = 1: amplitude (Q). lam = 0: mean field (C)."""
    phi = G * m**2 * tau / (HBAR * branch_distances(dx, gap, geometry))
    mean_A = phi.mean(axis=1, keepdims=True)    # A's branch i feels B's averaged field
    mean_B = phi.mean(axis=0, keepdims=True)
    mf = mean_A + mean_B - phi.mean()           # mean-field energy, no double counting
    return lam * phi + (1 - lam) * mf


def entangling_phase(ph):
    return ph[0, 0] + ph[1, 1] - ph[0, 1] - ph[1, 0]


def state(ph, gamma_tau=0.0):
    """Density matrix: (1/2) sum e^{-i phi_ij}|ij>, with each mass dephased by e^{-gamma tau}."""
    psi = 0.5 * np.exp(-1j * ph).ravel()
    rho = np.outer(psi, psi.conj())
    idx = [(i, j) for i in range(2) for j in range(2)]
    for a, (i, j) in enumerate(idx):
        for b, (k, l) in enumerate(idx):
            rho[a, b] *= np.exp(-gamma_tau * ((i != k) + (j != l)))
    return rho


def concurrence_pure(ph):
    return abs(np.sin(entangling_phase(ph) / 2))


def negativity(rho):
    r = rho.reshape(2, 2, 2, 2).transpose(0, 3, 2, 1).reshape(4, 4)   # partial transpose on B
    ev = np.linalg.eigvalsh(r)
    return float(-ev[ev < 0].sum())


def partial_transpose(rho):
    return rho.reshape(2, 2, 2, 2).transpose(0, 3, 2, 1).reshape(4, 4)


def witness_for(rho_design):
    """Optimal PPT witness for the state the experiment is DESIGNED for:
    W = (|v><v|)^{T_B}, v the most negative eigenvector of rho_design^{T_B}.
    <W> < 0 certifies entanglement; <W> >= 0 for every separable state (KNOWN)."""
    ev, vec = np.linalg.eigh(partial_transpose(rho_design))
    v = vec[:, 0]
    return partial_transpose(np.outer(v, v.conj()))


PAULIS = [I2, SX, SY, SZ]


def witness_stats(W, rho, runs):
    """<W> and its standard error when `runs` are split over the 9 local settings
    (sigma_a x sigma_b, a, b in {x, y, z}); each correlator has outcomes +-1."""
    mean = float(np.real(np.trace(rho @ W)))
    var = 0.0
    for k in range(1, 4):
        for l in range(1, 4):
            P = np.kron(PAULIS[k], PAULIS[l])
            c = np.real(np.trace(W @ P)) / 4
            e = np.real(np.trace(rho @ P))
            var += c**2 * (1 - e**2) / (runs / 9)
    # single-site terms are read off the same settings; bounded by the same variance budget
    for k in range(1, 4):
        for P in (np.kron(PAULIS[k], I2), np.kron(I2, PAULIS[k])):
            c = np.real(np.trace(W @ P)) / 4
            e = np.real(np.trace(rho @ P))
            var += c**2 * (1 - e**2) / (runs / 3)
    return mean, np.sqrt(var)


def runs_for_witness(W, rho, sigma=3.0):
    """Runs needed for <W> < 0 at `sigma` standard errors (sd scales as 1/sqrt(N))."""
    mean, sd1 = witness_stats(W, rho, 1.0)
    if mean >= -1e-12:                     # separable within rounding: never certified
        return np.inf
    return float(np.ceil((sigma * sd1 / mean) ** 2))


def gas_decoherence_rate(m, P, T, m_gas=None):
    """DERIVED (src/stur_gravity_full.py H5b): for dx much larger than the body and the gas
    wavelength, every collision resolves the superposition, so the rate is the collision rate
        Gamma = n <v> sigma_tot = (P/kT) sqrt(8kT/(pi m_gas)) 2 pi R^2
    with the quantum hard-sphere cross-section 2 pi R^2 (kR ~ 4000 here). The interpolation
    used before (LIT: Romero-Isart, PRA 84, 052121 (2011), eq. 27) gives 4.19x more.
    N2 assumed as the residual gas."""
    mg = M_N2 if m_gas is None else m_gas
    return P / (KB * T) * np.sqrt(8 * KB * T / (np.pi * mg)) * 2 * np.pi * radius(m) ** 2


def casimir_energy(m, r):
    """KNOWN (Casimir-Polder, retarded, r >> R):  U = -(23 hbar c / 4 pi) R^6 / r^7 * K^2,
    with K = (eps - 1)/(eps + 2)."""
    R = radius(m)
    K = (EPS_DIAMOND - 1) / (EPS_DIAMOND + 2)
    return -(23 * HBAR * C / (4 * np.pi)) * R**6 / r**7 * K**2


def casimir_vs_gravity_gap(m, dx, tau, geometry="linear"):
    """Smallest gap at which the Casimir entangling phase is <= 10% of gravity's."""
    for gap in np.geomspace(1e-6, 1e-3, 4000):
        r = branch_distances(dx, gap, geometry)
        phc = -casimir_energy(m, r) * tau / HBAR
        if abs(entangling_phase(phc)) <= 0.1 * abs(entangling_phase(phases(m, dx, gap, tau, geometry))):
            return gap
    return np.nan


def self_gravity_shift(m, dx, tau):
    """FOLLOWS: in the split-field (mean-field) picture, the two halves of ONE mass attract
    each other (gravitational analogue of T5's self-repulsion). Each half (m/2) feels the
    other half's pull G (m/2) / dx^2. Relative displacement after tau."""
    a = G * (m / 2) / dx**2
    return 2 * 0.5 * a * tau**2          # both halves move toward each other


def lambda_resolution(runs, sigma=3.0, geometry="parallel", gamma_tau=0.0, **kw):
    """Smallest lambda whose witness (designed for lambda = 1) is negative at `sigma`
    with `runs` runs. Bisection: entanglement is monotonic in lambda here."""
    W = witness_for(state(phases(geometry=geometry, lam=1.0, **kw), gamma_tau))

    def ok(lam):
        rho = state(phases(geometry=geometry, lam=lam, **kw), gamma_tau)
        return runs_for_witness(W, rho, sigma) <= runs
    if not ok(1.0):
        return np.nan
    lo, hi = 0.0, 1.0
    for _ in range(40):
        mid = 0.5 * (lo + hi)
        lo, hi = (lo, mid) if ok(mid) else (mid, hi)
    return hi


def lambda_floor(gamma_tau, geometry="parallel", **kw):
    """Smallest lambda with any entanglement left after dephasing (infinite runs)."""
    for lam in np.linspace(0, 1, 10001):
        if negativity(state(phases(geometry=geometry, lam=lam, **kw), gamma_tau)) > 1e-12:
            return lam
    return np.nan


def main():
    b = BASE
    banner("G1  Baseline (LIT: Bose et al. 2017): m = 1e-14 kg, dx = 250 um, gap = 200 um, tau = 2.5 s")
    print(f"   Diamond radius R = {radius(b['m'])*1e6:.2f} um")
    for geo in ("linear", "parallel"):
        r = branch_distances(b["dx"], b["gap"], geo)
        ph = phases(**b, geometry=geo)
        dphi = entangling_phase(ph)
        print(f"   {geo:8s}: branch distances (um) {np.round(r.ravel()*1e6,1)}")
        print(f"             phases (rad) {np.round(ph.ravel(),4)}")
        print(f"             entangling phase dphi = {dphi:+.4f} rad, concurrence = {concurrence_pure(ph):.4f}")

    banner("G2  The two pictures of gravity's field, same masses, same geometry")
    print("   lambda = 1: field in two places as an amplitude (standard quantum gravity at")
    print("               Newtonian order). lambda = 0: one classical averaged field.")
    print("   Witness W is designed for the lambda = 1 prediction and applied to each case.")
    print("   lambda   dphi (rad)   concurrence   negativity   witness <W>   runs (3 sigma)")
    for geo in ("linear", "parallel"):
        print(f"   [{geo}]")
        W = witness_for(state(phases(**b, geometry=geo)))
        for lam in (1.0, 0.75, 0.5, 0.25, 0.0):
            ph = phases(**b, geometry=geo, lam=lam)
            rho = state(ph)
            w = np.real(np.trace(rho @ W))
            n = runs_for_witness(W, rho)
            print(f"   {lam:5.2f}   {entangling_phase(ph):+10.4f}   {concurrence_pure(ph):11.4f}"
                  f"   {negativity(rho):10.4f}   {w:+11.4f}   {f'{n:.0f}' if np.isfinite(n) else 'never':>14}")
    print("   FOLLOWS: the entangling phase is exactly lambda * dphi. With lambda = 0 every")
    print("   phase is local and the state stays a product: no entanglement, ever.")

    banner("G3  Dephasing: how quiet must the experiment be?")
    geo = "parallel"
    ph = phases(**b, geometry=geo)
    print("   gamma*tau   negativity   witness <W>   runs for 3 sigma")
    gt_max = None
    for gt in (0.0, 0.01, 0.05, 0.1, 0.2, 0.3, 0.5):
        rho = state(ph, gt)
        W = witness_for(rho)
        w = np.real(np.trace(rho @ W))
        n = runs_for_witness(W, rho)
        print(f"   {gt:9.2f}   {negativity(rho):10.4f}   {w:+11.4f}   {f'{n:.0f}' if np.isfinite(n) else 'never':>16}")
    for gt in np.linspace(0, 1, 2001):
        if negativity(state(ph, gt)) <= 1e-12:
            gt_max = gt
            break
    print(f"   Entanglement is gone at gamma*tau = {gt_max:.3f}"
          f"  -> total dephasing rate < {gt_max/b['tau']:.3f} /s per mass")
    for P, T in [(1e-15, 0.15), (1e-13, 0.15), (1e-10, 4.0)]:
        Gm = gas_decoherence_rate(b["m"], P, T)
        print(f"   Gas at P = {P:.0e} Pa, T = {T} K: Gamma = {Gm:.2e} /s,"
              f" Gamma*tau = {Gm*b['tau']:.2e}")
    print("   (Order-of-magnitude estimate, N2 assumed.) Even the LIT target of 1e-15 Pa and")
    print("   0.15 K (Bose et al.) uses most of the budget; blackbody emission and scattering,")
    print("   and trap noise, must fit in what is left.")

    banner("G4  The Casimir background (KNOWN EM between the two diamonds)")
    for geo in ("linear", "parallel"):
        g10 = casimir_vs_gravity_gap(b["m"], b["dx"], b["tau"], geo)
        r = branch_distances(b["dx"], b["gap"], geo)
        phc = -casimir_energy(b["m"], r) * b["tau"] / HBAR
        ratio = abs(entangling_phase(phc) / entangling_phase(phases(**b, geometry=geo)))
        print(f"   {geo:8s}: at gap 200 um, Casimir/gravity entangling phase = {ratio:.1e};"
              f" Casimir < 10% of gravity needs gap > {g10*1e6:.0f} um")
    print("   Casimir falls as 1/r^7 against gravity's 1/r, so a modest gap removes it, and")
    print("   what remains is a known, calculable EM term to subtract.")

    banner("G5  Self-gravity of one split mass (the gravity version of T5)")
    s = self_gravity_shift(b["m"], b["dx"], b["tau"])
    print(f"   Split-field picture: halves of one diamond attract across dx = 250 um.")
    print(f"   Relative displacement after 2.5 s: {s:.2e} m  (an atomic nucleus is ~1e-15 m)")
    print("   FOLLOWS: unlike the electron's e/2 + e/2 repulsion in T5, a split mass's")
    print("   self-pull is far too weak to see. So for gravity, the self-interaction route is")
    print("   closed and the entanglement test is the only one.")

    banner("G6  What the experiment measures: lambda, and the scaling with mass")
    print("   Smallest lambda told apart from 0 (split field) at 3 sigma, parallel geometry:")
    print("   gamma*tau     1e4 runs   1e5 runs   1e6 runs   floor (infinite runs)")
    for gt in (0.0, 0.05, 0.1):
        r = [lambda_resolution(n, geometry="parallel", gamma_tau=gt, **b) for n in (1e4, 1e5, 1e6)]
        print(f"   {gt:9.2f}   {r[0]:8.3f}   {r[1]:8.3f}   {r[2]:8.3f}   {lambda_floor(gt, **b):10.3f}")
    print("   FOLLOWS: dephasing sets a hard floor. A weak entangling phase is erased")
    print("   completely, so below the floor no number of runs helps.")
    print("   mass (kg)   dphi parallel (rad)   at gap 200 um, dx 250 um, tau 2.5 s")
    for m in (1e-15, 3e-15, 1e-14, 3e-14):
        ph = phases(m, b["dx"], b["gap"], b["tau"], "parallel")
        print(f"   {m:9.0e}   {entangling_phase(ph):+19.4f}")
    print("   dphi grows as m^2 tau: halving the mass needs four times the coherence time.")

    banner("VERDICT")
    print("   The 'split field' picture (lambda = 0) makes a sharp prediction: NO gravitational")
    print("   entanglement at any mass, gap or time. Standard quantum gravity at Newtonian order")
    ph = phases(**b, geometry="parallel")
    print(f"   (lambda = 1) predicts dphi = {entangling_phase(ph):.2f} rad for the parallel baseline:"
          f" ~{runs_for_witness(witness_for(state(ph)), state(ph)):.0f} runs at 3 sigma.")
    print("   The experiment measures lambda directly: a single number with no exotic physics,")
    print("   only Newton's 1/r and the two pictures of what a field does when its source is in")
    print("   two places. For EM, experiment already shows lambda = 1 behaviour (T5, Sonnentag & Hasselbach).")
    print("   For gravity, nobody knows yet.")


if __name__ == "__main__":
    main()
