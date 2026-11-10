#!/usr/bin/env python3
"""
The Born rule, derived from the quantum level instead of assumed.

DERIVATION.md D0 assumed "probability = |amplitude|^2". Here it is replaced by weaker,
physical assumptions, and |c|^2 is derived four ways. Each is computed.

Assumed instead (A1-A3):
  A1  Unitary quantum mechanics with tensor products (the equation of DERIVATION.md).
  A2  Locality: what can be learned about a system S cannot be changed by acting only
      on a separate system E (no-signaling).
  A3  An outcome's probability depends only on the state and on that outcome
      (not on what else was measured with it: non-contextuality).

  B1  Envariance (Zurek 2003, 2005): from A1 + A2, equal amplitudes give equal
      probabilities; fine-graining with the environment then gives p = |c|^2 for every
      rational |c|^2, and continuity for the rest. Any other rule contradicts itself.
  B2  Additivity (Gleason-type, from A3): if p = F(|<e|psi>|^2) in every basis, the
      probabilities of a complete set must add to 1. Only F(x) = x does that.
  B3  No-signaling (from A2): with any rule F(x) = x^q, q != 1, Bob's statistics change
      when Alice changes her measurement far away: a faster-than-light telegraph.
  B4  Frequencies (Hartle 1968; Farhi-Goldstone-Gutmann 1989): in N repeats, the total
      weight of branches whose frequency differs from |c|^2 goes to zero.
Labels: KNOWN, FOLLOWS, CHECK, LIT.
"""
import numpy as np
from math import comb, log

RNG = np.random.default_rng(20261110)


def banner(s):
    print("\n" + "=" * 78 + "\n" + s + "\n" + "=" * 78)


# --------------------------------------------------------------------------- B1
def ket(d, i):
    v = np.zeros(d, complex)
    v[i] = 1
    return v


def envariance_equal():
    """|psi> = (|0>|e0> + |1>|e1>)/sqrt2. Swap on S, then the counter-swap on E only.
    Also an arbitrary phase on S, undone by the opposite phase on E."""
    psi = (np.kron(ket(2, 0), ket(2, 0)) + np.kron(ket(2, 1), ket(2, 1))) / np.sqrt(2)
    X = np.array([[0, 1], [1, 0]], complex)
    I = np.eye(2)
    after_S = np.kron(X, I) @ psi
    restored = np.kron(I, X) @ after_S
    ph = 0.731
    P = np.diag([1, np.exp(1j * ph)])
    restored_ph = np.kron(I, P.conj()) @ (np.kron(P, I) @ psi)
    return np.linalg.norm(after_S - psi), np.linalg.norm(restored - psi), np.linalg.norm(restored_ph - psi)


def complete_unitary(cols):
    """Unitary whose first columns are the given orthonormal vectors."""
    d = cols.shape[0]
    M = np.hstack([cols, RNG.normal(size=(d, d - cols.shape[1])) + 0j])
    Q, R = np.linalg.qr(M)
    Q[:, : cols.shape[1]] = cols
    return Q


def fine_grain(m, M):
    """|psi> = sqrt(m/M)|0>|e0> + sqrt((M-m)/M)|1>|e1>, environment of dimension M.
    A unitary on E alone maps |e0> -> sum_{k<m} |k>/sqrt(m), |e1> -> sum_{k>=m} |k>/sqrt(M-m).
    Returns: the fine-grained amplitudes (should all be 1/sqrt(M)), the largest residual of
    envariance for swapping any two fine-grained branches (undone on E only), and p0."""
    a0, a1 = np.sqrt(m / M), np.sqrt((M - m) / M)
    e0, e1 = ket(M, 0), ket(M, 1)
    psi = a0 * np.kron(ket(2, 0), e0) + a1 * np.kron(ket(2, 1), e1)
    f0 = np.zeros(M, complex); f0[:m] = 1 / np.sqrt(m)
    f1 = np.zeros(M, complex); f1[m:] = 1 / np.sqrt(M - m)
    # unitary U with U e0 = f0, U e1 = f1
    W = complete_unitary(np.stack([f0, f1], axis=1))
    V = complete_unitary(np.stack([e0, e1], axis=1))
    U = W @ V.conj().T
    psi_f = np.kron(np.eye(2), U) @ psi
    amp = psi_f.reshape(2, M)
    # each fine-grained branch k: system label s(k) = 0 for k < m, 1 otherwise
    nz = np.abs(amp)[np.abs(amp) > 1e-12]
    # envariance of a swap between branches k and l: relabel the joint state as sum_k |k>_{SC}|k>_E
    # (the system's record plus an ancilla C carrying k). A swap k<->l on SC is undone by k<->l on E.
    joint = np.zeros((M, M), complex)
    for k in range(M):
        joint[k, k] = amp[0 if k < m else 1, k]
    worst = 0.0
    for k in range(M):
        for l in range(k + 1, M):
            Pm = np.eye(M); Pm[[k, l]] = Pm[[l, k]]
            swapped = Pm @ joint             # act on SC
            back = swapped @ Pm.T            # counter-swap on E
            worst = max(worst, np.linalg.norm(back - joint))
    p0 = m / M                               # m equiprobable fine-grained branches carry outcome 0
    return nz, worst, p0, a0**2


def rival_rule_inconsistency(m, M, q):
    """A rule p ~ |c|^(2q). Coarse amplitudes give p0 = x^q / (x^q + (1-x)^q), x = m/M.
    Fine-grained (same physical state, after a unitary on E only), every branch has |c|^2 = 1/M,
    so the same rule gives p0 = m/M. They must agree."""
    x = m / M
    coarse = x**q / (x**q + (1 - x) ** q)
    return coarse, x


# --------------------------------------------------------------------------- B2
def random_basis(d):
    Z = RNG.normal(size=(d, d)) + 1j * RNG.normal(size=(d, d))
    Q, _ = np.linalg.qr(Z)
    return Q


def additivity_violation(q, d=3, trials=20000):
    """max over random bases and states of |sum_k F(|<e_k|psi>|^2) - 1| for F(x) = x^q."""
    worst = 0.0
    for _ in range(trials):
        psi = RNG.normal(size=d) + 1j * RNG.normal(size=d)
        psi /= np.linalg.norm(psi)
        B = random_basis(d)
        x = np.abs(B.conj().T @ psi) ** 2
        worst = max(worst, abs(np.sum(x**q) - 1))
    return worst


# --------------------------------------------------------------------------- B3
def bob_marginal(psi, theta_A, theta_B, q):
    """Two qubits. Alice measures along angle theta_A (real basis), Bob along theta_B.
    Joint 'probabilities' from the rule F(x) = x^q, normalised over the four outcomes.
    Returns Bob's P(+)."""
    def basis(t):
        return [np.array([np.cos(t / 2), np.sin(t / 2)]), np.array([-np.sin(t / 2), np.cos(t / 2)])]
    A, B = basis(theta_A), basis(theta_B)
    P = np.array([[abs(np.kron(a, b).conj() @ psi) ** (2 * q) for b in B] for a in A])
    P /= P.sum()
    return P[:, 0].sum()


def signaling(q, trials=400):
    """Largest change in Bob's P(+) when only Alice's setting changes."""
    worst = 0.0
    for _ in range(trials):
        psi = RNG.normal(size=4) + 1j * RNG.normal(size=4)
        psi /= np.linalg.norm(psi)
        tB = RNG.uniform(0, 2 * np.pi)
        p1 = bob_marginal(psi, 0.0, tB, q)
        p2 = bob_marginal(psi, RNG.uniform(0, 2 * np.pi), tB, q)
        worst = max(worst, abs(p1 - p2))
    return worst


# --------------------------------------------------------------------------- B4
def atypical_weight(N, p, eps=0.05):
    """Total squared norm of the branches of (sqrt(p)|0> + sqrt(1-p)|1>)^N whose fraction of
    0s differs from p by more than eps. Exact (log-space binomial)."""
    tot = 0.0
    for k in range(N + 1):
        if abs(k / N - p) > eps:
            lw = log(comb(N, k)) + (k * log(p) if k else 0) + ((N - k) * log(1 - p) if N - k else 0)
            tot += np.exp(lw)
    return tot


def main():
    banner("B1  Envariance: from locality (A2) to equal, then |c|^2, probabilities (CHECK)")
    a, b_, c_ = envariance_equal()
    print(f"   |psi> = (|0>|e0> + |1>|e1>)/sqrt2.  Swap on S changes the state by {a:.3f};")
    print(f"   the counter-swap on E alone restores it to {b_:.1e}. A phase on S, undone on E: {c_:.1e}.")
    print("   A2: acting on E cannot change S's probabilities. The swap on S exchanges p0 and p1,")
    print("   yet E alone undoes it. So p0 = p1 = 1/2, and phases do not matter.")
    print("   Unequal amplitudes, fine-grained by a unitary on E only:")
    print("     m/M      |c0|^2    fine-grained amplitudes        swap residual   p0 (counting)")
    for m, M in [(1, 3), (2, 5), (3, 7), (5, 8)]:
        nz, worst, p0, c2 = fine_grain(m, M)
        print(f"     {m}/{M}   {c2:.6f}   all {nz.min():.6f}-{nz.max():.6f} (1/sqrt(M) = {1/np.sqrt(M):.6f})"
              f"   {worst:.1e}        {p0:.6f}")
    print("   FOLLOWS: p0 = m/M = |c0|^2 for every rational value, and by continuity for all.")
    print("   Any other rule disagrees with itself on the SAME state (coarse vs fine-grained):")
    for q in (0.5, 2.0):
        coarse, fine = rival_rule_inconsistency(2, 5, q)
        print(f"     p ~ |c|^{2*q:g}: coarse p0 = {coarse:.4f}, fine-grained p0 = {fine:.4f}")

    banner("B2  Additivity (A3): probabilities of a complete set must add to 1 (CHECK, dim 3)")
    for q in (0.5, 0.9, 1.0, 1.1, 2.0):
        print(f"   F(x) = x^{q:<3}: largest |sum - 1| over 20,000 random states and bases = {additivity_violation(q):.2e}")
    print("   FOLLOWS: only F(x) = x is additive (for continuous F this is Cauchy's equation).")
    print("   LIT: Gleason (1957): in dimension >= 3, EVERY non-contextual probability assignment")
    print("   to measurement outcomes is p = Tr(rho P): the Born rule, mixed states included.")

    banner("B3  No-signaling (A2): any other rule is a faster-than-light telegraph (CHECK)")
    for q in (0.5, 0.9, 1.0, 1.1, 2.0):
        print(f"   F(x) = x^{q:<3}: largest change in Bob's P(+) when only Alice's setting changes = {signaling(q):.2e}")
    print("   FOLLOWS: with |c|^2, Bob sees nothing of Alice's choice; with any other power he")
    print("   does, instantly. This is the 'instant reaction, but no message' of MEASUREMENT.md T4:")
    print("   the Born rule is exactly what makes the stretched-object picture safe.")

    banner("B4  Frequencies: the weight of the 'wrong-frequency' branches goes to zero (CHECK)")
    p = 2 / 5
    for N in (10, 100, 1000, 10000):
        print(f"   N = {N:5d} repeats, |c0|^2 = 0.4: weight of branches with |f - 0.4| > 0.05 = {atypical_weight(N, p):.2e}")
    print("   FOLLOWS: almost all of the state sits on branches where the observed frequency is")
    print("   |c|^2. (This step reads small weight as negligible, so on its own it is not free of")
    print("   the rule it derives; B1-B3 do not need that reading.)")

    banner("VERDICT")
    print("   The Born rule is no longer an input. It follows from unitarity + locality (B1, B3)")
    print("   or from unitarity + non-contextuality (B2, Gleason), and B4 shows the frequencies.")
    print("   What remains assumed: A1-A3, and that outcomes are records (rho_ij of DERIVATION.md).")
    print("   LIT caveat: envariance assumes that probabilities exist and depend only on the state;")
    print("   that step is debated (Schlosshauer & Fine 2005). B2 and B3 do not rely on it.")


if __name__ == "__main__":
    main()
