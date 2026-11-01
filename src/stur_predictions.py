#!/usr/bin/env python3
"""
Unification search, step 5: how much room is there for a STUR prediction?

Take STUR's physical picture literally - spacetime is the environment that records
which-path information - but with STANDARD gravity (no new structure).  In the
unified equation the environment enters only through its modular Hamiltonian; a
thermal graviton bath at temperature T gives (FDT + dimensional analysis; same form
as Blencowe, PRL 111, 021302 (2013), O(1) prefactor c0 NOT fixed here):

    Gamma_rate = c0 * (k_B T / hbar) * (Delta E / E_P)^2

Delta E = energy difference between the two arms (largest when the arms differ in
internal state, as in clock-transition interferometers such as MAGIS-100 / AION).
Then: the enhancement F a new STUR coupling would need to reach a visibility
sensitivity dV over an interrogation time t.
"""
import numpy as np

hbar, kB, c, G = 1.054571817e-34, 1.380649e-23, 2.99792458e8, 6.67430e-11
EP = np.sqrt(hbar * c**5 / G)                     # J
h = 2 * np.pi * hbar


def banner(s):
    print("\n" + "=" * 78 + "\n" + s + "\n" + "=" * 78)


def main():
    banner("P1  Standard-gravity 'spacetime environment' for an atom interferometer")
    dE_clock = h * c / 698.4e-9                    # Sr-87 clock transition energy
    hbark = hbar * 2 * np.pi / 698.4e-9
    dE_kin = 100 * hbark * 10.0                    # 100 hbar k momentum difference at ~10 m/s
    print(f"E_P = {EP:.4e} J")
    print(f"Delta E (arms in different clock states, Sr 698 nm) = {dE_clock:.3e} J")
    print(f"Delta E (kinetic, 100 hbar k at 10 m/s)            = {dE_kin:.3e} J")
    H0 = 67.4e3 / 3.0857e22
    baths = {
        "cosmic graviton background (LIT prediction, unobserved)": 0.905,
        "de Sitter horizon, T = hbar H/(2 pi kB)": hbar * H0 * np.sqrt(0.685) / (2 * np.pi * kB),
        "Unruh temperature of a lab held at g = 9.81": hbar * 9.81 / (2 * np.pi * c * kB),
        "deliberately absurd: T = 300 K graviton bath": 300.0,
    }
    t, dV = 1.0, 1e-3                              # interrogation time (s), visibility sensitivity (assumed)
    print(f"\nInterrogation time t = {t} s; assumed visibility sensitivity dV = {dV} (parameter, not a MAGIS spec)")
    for name, T in baths.items():
        g = (kB * T / hbar) * (dE_clock / EP) ** 2 * t
        print(f"  {name:55s} T = {T:9.3e} K   Gamma = {g:.2e}   enhancement needed F = {dV/g:.1e}")
    print("\n  -> with standard gravity, spacetime-as-environment decoherence needs an enhancement")
    print("     F ~ 10^41 (graviton background) to 10^71 (de Sitter); even a 300 K graviton bath")
    print("     needs 10^39. A STUR signal at MAGIS/AION needs new structure, not GR.")

    banner("P2  Lab-testable consequences of the unified equation (all STANDARD physics)")
    print("  (a) V = <(-1)^{Delta N}> (visibility = parity of exchanged quanta): testable with a")
    print("      qubit + cavity mode, measuring photon-number parity of the cavity (standard).")
    print("  (b) Entanglement Hamiltonian = local, distance-weighted energy (BW): already measured")
    print("      by entanglement-Hamiltonian tomography in quantum simulators (LIT: Kokail et al. 2021).")
    print("  (c) Confining string: entropy length-independent, modular energy ~ sigma x area:")
    print("      testable in Rydberg / trapped-ion simulators of confining Ising chains (standard).")
    print("  None of these distinguishes STUR from standard physics.")


if __name__ == "__main__":
    main()
