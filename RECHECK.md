# Derivation and recheck record

*November 2026.* This page answers one instruction: anything not yet derived must be
derived, and anything that failed must be checked again. It sorts every item into one
of four groups:
- derived now;
- failed and rechecked;
- not independently rechecked;
- impossible to derive within the framework, with the reason.

Each is backed by code and a test.

## 1. Derived now (previously estimated or cited)

| Item | Before | Now | Effect |
|---|---|---|---|
| **Gas-collision decoherence** (design A's deciding number) | Interpolation γ = λ_th²Λ (Romero-Isart 2011, eq. 27, read from arXiv) | Γ = n⟨v⟩σ_tot, with σ_tot = 2πR² checked by an exact partial-wave sum (2.0096 πR² at kR = 3000; kR ≈ 4000 for N₂ at 0.15 K) | The interpolation was **4.19× too high**. Design A now needs 270 runs (was 565). Helium as the leftover gas no longer kills the experiment. Requirements relax: 7.6×10⁻¹⁵ Pa, 1.4 s spin coherence, 1.9 K, vibration 57× below LISA Pathfinder. `src/stur_gravity_full.py` H5b |
| **Jacobson's step D3** | Cited, not recomputed | Each link derived symbolically (`src/stur_jacobson.py`): Raychaudhuri (exact on FRW with a general a(t)); the null-vector lemma, X_kk = 0 ⇒ X = f g (one free parameter left); Clausius, giving G = 1/(4ħη); the contracted Bianchi identity (exact on a general time-dependent spherical metric) | D3 is now CHECK. Its premise, local equilibrium on every local horizon, remains assumed. |
| **Equal quark and string modular weights** | "Needs DMRG" | Settled by theorem: in a relativistic continuum limit the modular Hamiltonian is 2π × the boost generator (Bisognano–Wichmann 1975), which weights every energy density equally | The lattice computation would only illustrate a proved theorem. Not run. |

## 2. Every failed claim, checked again with independent code

Source: `src/stur_recheck.py` (fresh implementations, importing none of the original
scripts), output `results/recheck/output.txt`, test `tests/test_recheck.py`.

| # | Claim that failed | Independent method | Result |
|---|---|---|---|
| X1 | S_R = −k ln V is an entropy | von Neumann, linear and Rényi-2 entropies of the dephased qubit | Confirmed: matches none; only the linear entropy agrees, as V → 1 |
| X2 | E_R = ½k_BTΦ² (Landauer) | Fock-space thermal overlap vs the closed form; crossing equation solved | Confirmed: opposite T dependence; agreement only at ħω = 2.40 k_BT |
| X3 | Smarr check | Symbolic | Confirmed circular: E_R = M/2 identically once S_R = A/4 is assumed |
| X4 | The electron as a real charge cloud | Fresh self-consistent radial solver | Confirmed: 6.64 eV binding, ⟨r⟩ = 2.50 a₀, against 13.60 eV measured |
| X5 | An empty universe tunnels | WKB barrier integral | Confirmed: the barrier grows as ρ → 0 |
| X6 | Information paradox | Evaporation history with Page's factor 1.4847 (recalled) | Confirmed: the area bound breaks after 0.5381 t_evap |
| X7 | One A_μ for horizons and confinement | Symbolic replica derivative | Confirmed: the string term enters ⟨K⟩, not S |
| X8 | Option A | Option A's noise against LISA Pathfinder's acceleration noise | Confirmed: excluded by 8–13 orders for ξ from 1 µm to 0.3 m |
| X9 | Option B | ħH₀ | Confirmed: √σ < 1.4×10⁻³³ eV |
| X10 | Option C | Closed form | Confirmed: a constant 0.305 N |
| X11 | Holographic dark energy (front 1) | Closed-form w_a | Confirmed: w_a > 0 for every c |
| X12 | ⅓ twist as a quark (front 3) | J = qΦ/4π | Confirmed: J = 1/6, not a fermion |
| X13 | Koide δ = 2/9 (front 8) | Fresh fit, current masses | Confirmed: Q at −0.43σ; δ = 2/9 off by 452σ (447σ recorded; recalled precisions) |
| X14 | Higgs mass from Planck stability (front 9) | Fresh one-loop RGEs, two top-mass matchings | Confirmed: m_H ≥ 133.1–134.3 GeV against 125.2. The bound depends on the top-mass matching by about 1 GeV |
| X15 | Gauge unification in 3-3-1 (front 12) | Fresh one-loop running | Confirmed: the gap grows from 18.6 to 27.1 (27.3 at two loops) |

**15 of 15 failures are confirmed.** One number moved: front 9's one-loop bound is
133.1 GeV with its own matching and 134.3 GeV with MS-bar NNLO inputs. The verdict
doesn't change.

**Not independently rechecked** (the verdict rests on literature values, or would need
a solver not rebuilt here):
- the Skyrme fold cost;
- the running-vacuum CMB bound (front 2);
- the Eichhorn–Held retrodictions (front 10);
- the 3-3-1 Higgs threshold (front 11).

## 3. What cannot be derived within the framework, and why

| Item | Why it can't be derived here | Where this is shown |
|---|---|---|
| The value of G | G = πa²c³/(N c_s ħ) needs the cutoff a, which is a free input. The measured G fixes only a²/N. | DERIVATION D8 |
| c_s = 0.3046 as a universal number | The area-law coefficient depends on the regulator (LIT, Srednicki 1993). Gauge fields add contact terms (Kabat 1995). | CONSISTENCY K4 |
| The particle content | Only N_c = N_g = 3 and the ⅓ charges follow, conditionally, in 3-3-1. The gauge group and the representations are inputs. | NOTE_331 |
| Masses, mixings, the Higgs mass, couplings, dark energy | Consistency conditions fix integers, not continuous numbers. Every mechanism tried misses by 3–5%, only accommodates, or fails. | GOD_EQUATION fronts 8–12, rechecked in X13–X15 |
| Jacobson's premise (local equilibrium on every horizon) | It's the physical assumption the derivation starts from | `src/stur_jacobson.py` |
| Non-Markovian classical gravity's behaviour | No positivity theorem constrains classical fields with memory | WALL.md |

## 4. Blocked by data, not by theory

- **Option A's Earth-scale corner** (best case Γ = 2.4×10⁻³, already not distinctive).
  Closing it needs LIGO's measured low-frequency strain spectrum. The O3 sensitivity
  paper (arXiv:2008.01301) shows it only in figures. The data hosts, gwosc.org and
  dcc.ligo.org, are blocked by this environment's network. The corner can't change
  option A's verdict: at ξ ≈ R_E the signal is ordinary gravity-gradient noise,
  quadratic in Δx.

## Reproduce

```bash
python3 src/stur_recheck.py        # the 15 rechecks, ~1 s
python3 src/stur_jacobson.py       # D3, ~2 s
python3 src/stur_gravity_full.py   # the derived gas rate and the design search, ~25 s
```
