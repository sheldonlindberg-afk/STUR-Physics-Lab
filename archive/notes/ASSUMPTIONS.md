# Every assumption behind the postulate test, varied, with all matches found

Reproduce: `python3 src/stur_assumption_scan.py` (about 45 s). The full output is
in `results/assumption_scan/output.txt`, and `tests/test_assumption_scan.py`
pins the matches. Every number below is taken from that output. This report
extends [POSTULATE_TEST.md](POSTULATE_TEST.md).

Notation. Γ ≡ −ln(V/V₀) = ½Φ_R². The postulate and its corollary say:
- **P1:** S/k_B = Γ (visibility loss is entropy);
- **P2:** E_exchanged = k_B T Γ.

Each agreement found is classified as one of:
- **IDENTITY:** holds to numerical precision over the whole grid;
- **LIMIT:** holds only asymptotically;
- **COINCIDENCE:** holds only on a line in parameter space;
- **NONE:** never holds in the range scanned.

## 1. The assumption register

| # | Assumption | Where it enters | How it was varied | Result |
|---|---|---|---|---|
| A1 | Phase noise is Gaussian, so −ln V = ½⟨Φ²⟩ | Postulate chain | Spin bath (non-Gaussian), 3 / 30 / 300 spins | **LIMIT.** Error is 93% for 3 spins, where −ln V isn't even monotonic in time; 16% for 30; 2.1% for 300. Holds only for large baths (central limit theorem). KNOWN. |
| A2 | −k_B ln V is an entropy (P1) | STUR POSTULATE | 8 standard entropies and divergences, plus 2 extra measures | No standard entropy matches Γ (§2). |
| A3 | Landauer as an equality: E = k_BT·S | Corollary P2 | Esposito's identity | **The form E = k_BT·S is exactly right, but only with a different S** (§3). |
| A4 | "Energy exchanged" | P2 | System, bath, rms heat, free energy, erasure cost, net and gross flows | No candidate equals k_BTΓ (§3). |
| A5 | T is the bath temperature | P2 | Noise temperature, required temperature | The temperature that would make P2 hold *falls* as the bath heats up (§3). |
| A6 | The Smarr check supports P2 | Consistency check | Energy actually radiated | **Fails.** E_R = T_H S_BH = 0.500 Mc², but the hole radiates 1.000 Mc² (§6). |
| B1 | Bath is bosonic and linearly coupled | Test model | Ising spin bath | Γ > 0 with **exactly zero** energy exchanged anywhere (caveat in §5). |
| B2 | Bath is in a thermal state | Test model | The vacuum floor | For a thermal bath, or any classical mixture of coherent states, Γ_k ≥ 2⟨Q_k⟩/ħω_k. P2 is **impossible** for any mode with ħω < 2k_BT. Squeezed baths not tested. |
| B3 | Bath and qubit start uncorrelated | Test model | Bath pre-equilibrated to qubit state \|0⟩; vacuum part subtracted | Same Γ and same ⟨Q⟩ (derived in §7). Subtracting the vacuum part changes only the low-T end. |
| B4 | Ohmic spectrum (s = 1) | Test model | s = 0.5, 1, 2, 3, with ω_c t from 0.3 to 100 and k_BT/ħω_c from 0.01 to 30 | Only 0.4–2.5% of the grid lies within 10% of P2. At fixed energy, the slope d ln Γ/d ln T is +1.00 at high T for every s (postulate: −1). |
| B5 | Pure dephasing (no energy leaves the system) | Test model | Qubit that relaxes in a thermal bath (generalized amplitude damping) | Matches only on a line (COINCIDENCE). The crossing moves to a different place (§4). |
| B6 | Markov Caldeira–Leggett model | Part 1 | Exact recoilless version | Same verdict. |
| B7 | Environment is a bath, not scattered particles | Test model | Rayleigh scattering of thermal photons | P2 is off by ×6.97 (energy passing through) or by about 10⁻¹¹ (energy deposited). |
| B8 | Environment is ordinary matter, not spacetime | Everything | Can't be varied without open problem #2 | Stated as a requirement (§8). |

## 2. Entropy candidates for P1 (one mode, 48 values of T and coupling)

The simulation agrees with Γ = 2α²coth(ħω/2k_BT) to within 8.6×10⁻⁷.

| Candidate X | Range of X/Γ | Class |
|---|---|---|
| von Neumann entropy of the system | 0.027 – 3.6 | COINCIDENCE (2.1% of the grid) |
| Rényi-2 entropy of the system (−ln purity) | 0.027 – 0.998 | **LIMIT Γ → 0** (0.993–0.998 for Γ < 0.02); can never exceed ln 2 |
| Bath entropy change (= Holevo χ of the records) | 0.0053 – 3.6 | COINCIDENCE |
| Mutual information I(S:B) | 0.032 – 7.2 | COINCIDENCE |
| Entropy production ΔS_S + Q/T | 0.033 – 13.6 | NONE |
| D(ρ_B‖ρ_β) | 2×10⁻⁶ – 9.7 | NONE |
| −ln Uhlmann fidelity of the records | 0.006 – 1.000 | **LIMIT T → 0** (exactly 1.000000), and a **bound** −ln F ≤ Γ. KNOWN (Englert; Uhlmann). |
| Petz Rényi-½ divergence of the records | 0.012 – 4 | NONE |
| Relative entropy of one record from the thermal state | 0.006 – 10 | COINCIDENCE |
| **2 Var(Q_k)/(ħω_k)²** (spread in the number of quanta exchanged) | **1.000 – 1.000** | **IDENTITY** |

**The one exact match:** for each bath mode, at every T, **Γ_k = 2 Var(Q_k)/(ħω_k)²**. Q here is the heat
measured by recording the bath's energy before and after. In words: visibility
loss counts the *spread* in the number of quanta exchanged. It is not an energy
divided by k_BT, and it is not an entropy.

I derived and checked this here. It follows directly from the standard model,
and I expect it is already in the literature on heat statistics in dephasing,
but I have not searched for a reference. **So P1 has no exact match.** It holds
only in two limits: weak decoherence (Rényi-2 entropy) and zero temperature
(record fidelity).

## 3. Energy and temperature candidates for P2

| E / (k_B T* Γ) | Range | Class |
|---|---|---|
| ΔE of the system (pure dephasing) | 0 | NONE |
| ⟨Q⟩ = ΔE of the bath, T* = T | 0.006 – 10 | COINCIDENCE, on the line ħω = **2.399357 k_BT** |
| rms heat √Var Q, T* = T | 0.022 – 224 | COINCIDENCE |
| Bath free-energy gain T·D | 2×10⁻⁶ – 9.7 | NONE |
| Landauer cost of erasing the qubit–bath correlation, T·I | 0.032 – 7.2 | COINCIDENCE |
| ⟨Q⟩ with T* = noise temperature (ħω/2)coth(ħω/2k_BT) | 0.006 – 1.000 | LIMIT T → 0 |

If both the energy *and* the entropy are swapped for standard quantities, there
are exact matches:

| Identity | Range | Status |
|---|---|---|
| **⟨Q⟩ = k_BT · D(record‖ρ_β)** | 1.000 – 1.000 | **IDENTITY. KNOWN** (Esposito, Lindenberg & Van den Broeck 2010) |
| ⟨Q⟩ = ¼ k_BT · D(record₀‖record₁) | 0.25 – 0.25 | IDENTITY (the same fact, for Gaussian states) |
| ⟨Q_k⟩ = k_B T_noise,k · (−ln F_k) | 1.000 – 1.000 | IDENTITY for each mode. FOLLOWS from the known fidelity of Gaussian states. |
| ⟨Q⟩ = k_BT · (−ln F) | 1.002 – 1.008 for T ≥ 3.2 ħω | LIMIT T → ∞ (holds for many modes too) |

**The key result.** The structure "energy = k_BT × entropy of the
environment's record" is exactly right, and it is KNOWN physics: the entropy is
the relative entropy of the record from the bath's thermal state. STUR's P2
replaces that relative entropy with Γ. For each mode, the two differ by a factor
of exactly 1/(x tanh x), with x = ħω/2k_BT. That factor is the whole
disagreement.

- **No temperature fixes it.** The value that would make ⟨Q⟩ = k_BT*Γ is
  T* = (ħω/2)tanh(ħω/2k_BT); the formula was checked to 8.6×10⁻⁷. That value
  never exceeds ħω/2 and *falls* as the bath gets hotter, so it is not a
  temperature any thermometer would read.
- **Vacuum floor.** Γ_k/(2⟨Q_k⟩/ħω_k) = coth ≥ 1 everywhere on the grid (minimum
  1.000000). P2 needs Γ_k = ⟨Q_k⟩/k_BT, which is below that floor whenever
  ħω < 2k_BT. So P2 is forbidden there, not just wrong.

## 4. A system that really loses energy (generalized amplitude damping)

| E / (k_BT Γ) | Class |
|---|---|
| Net change in system energy | COINCIDENCE. At short times it tends to x tanh(x/2), which equals 1 only at ħω₀ = **1.543405 k_BT** |
| Gross energy in plus out | COINCIDENCE, at ħω₀ = **1 k_BT** |
| Gross *number of quanta* exchanged / Γ | **LIMIT t → 0**: 0.99995 – 0.999999. Γ equals the number of quantum jumps. KNOWN (quantum trajectories) |

The crossing point depends on the model: 2.40 k_BT for pure dephasing, 1.54 k_BT
here, 1 k_BT for gross energy. So these crossings are coincidences, not a hidden
law.

What the models share is §2's identity in another form: **Γ counts quanta, not
energy divided by k_BT.**

## 5. Non-Gaussian bath, and scattering

**Ising spin bath.** Every term in the Hamiltonian commutes, so the energies of
the system, the bath and the interaction are each exactly conserved. Yet Γ > 0:
decoherence happens with zero energy exchanged anywhere.

Caveat: the bath state here is a classical mixture, so this dephasing can be
undone by a spin echo. If STUR restricts P1 to irreversible decoherence, this
counterexample drops out, but the bosonic results don't.

**Thermal photons, saturated regime.** Each scattered photon fully reveals the
path, so Γ = N_scattered. The mean scattered photon has energy
7ζ(8)/ζ(7) k_BT = **6.9703 k_BT**, so P2 fails by ×6.97 if E counts the energy
passing through. For Rb-87, the energy actually deposited by recoil is only
1.8×10⁻¹¹ k_BTΓ at 300 K and 2.4×10⁻¹³ at 4 K.

## 6. The Smarr check

T_H S_BH = **0.500000 Mc²**, but the energy a black hole actually radiates is
∫T_H dS_BH = **1.000000 Mc²**. If E_R means energy exchanged with the
environment, the black-hole case gives ½, not 1.

So the check that passed confirms the Smarr relation Mc² = 2TS, an identity
about the hole itself. It does not confirm P2. For comparison, quasi-static
blackbody radiation would carry 4/3 S_BH of entropy.

## 7. Derivation for B3 (FOLLOWS)

Suppose the bath starts in equilibrium with the qubit's state |1⟩, displaced
by +g/ω.

- Branch |1⟩ stays put.
- Branch |0⟩ circles around −g/ω: α₀(t) = −g/ω + (2g/ω)e^(−iωt).
- The two branches are separated by (2g/ω)(e^(−iωt) − 1), the same as for an
  uncorrelated start. So Γ is unchanged.
- The average bath energy is ½·(g²/ω)(|2e^(−iωt) − 1|² − 1) = (2g²/ω)(1 − cos ωt),
  also unchanged.

## 8. Summary of all matches

| Match | Class | Status |
|---|---|---|
| Γ_k = 2 Var(Q_k)/(ħω_k)² | IDENTITY | FOLLOWS (derived here; literature not checked) |
| ⟨Q⟩ = k_BT · D(record‖thermal) | IDENTITY | KNOWN |
| ⟨Q_k⟩ = k_B T_noise · (−ln F_k) | IDENTITY (each mode) | FOLLOWS |
| −ln V = ½⟨Φ²⟩ | LIMIT (large bath) | KNOWN |
| Γ = −ln F of the records | LIMIT T → 0; otherwise −ln F ≤ Γ | KNOWN |
| ⟨Q⟩ = k_BT(−ln F) | LIMIT T → ∞ | FOLLOWS |
| S₂(system) = Γ | LIMIT Γ → 0 | FOLLOWS (trivial) |
| Γ = number of quantum jumps | LIMIT t → 0 | KNOWN |
| **P1 itself** | at best a LIMIT (Γ → 0 or T → 0) | — |
| **P2 itself** | COINCIDENCE at ħω = 2.40 / 1.54 / 1.00 k_BT depending on model; 0.4–2.5% of the scanned grid; never for photon scattering | — |

**The verdict is unchanged: standard decoherence theory contradicts the postulate.**

The scan does pin down where it goes wrong. "Energy = k_BT × entropy of the
environment's record" is standard physics. The STUR-specific step, **taking
that entropy to be −k_B ln V**, is the step that fails. The two differ by
x tanh x for each mode, and visibility loss instead counts the spread in quanta
exchanged.

Every number above assumes an ordinary environment. For spacetime as the
environment (B8), STUR would need either noise that breaks the
fluctuation–dissipation theorem, or coupling only at the crossing frequency.
Both are new assumptions, and neither can be tested until A_μ is fixed (open
problem #2).

**Option (not developed, needs your go-ahead):** redefine
S_R ≡ k_B D(spacetime record‖equilibrium). Then P2 becomes known physics.
But Φ_R² would no longer be the visibility loss, so the Gaussian-Wilson-loop
link (item 1 of the equation) and the area-law bound (item 4) would have to be
redone.
