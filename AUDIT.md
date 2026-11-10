# Consistency audit and testable predictions

*November 2026.* This audit read every current report (REPORT, DERIVATION, BORN,
EMERGENT, MEASUREMENT, GRAVITY_ENTANGLEMENT, TEGR, WALL, ASSUMPTIONS, UNIFICATION) and
the public files (README, `index.html`, `quantum.html`, `llms.txt`, `CITATION.cff`)
against each other and against the computed outputs in `results/`. The archive was not
audited. The test suite passes (86 tests).

It asks two questions:
1. Does the work contradict itself?
2. Does it make new predictions that are easy to test?

## 1. Contradictions found, and how each was fixed

| # | Where | Contradiction | Fix |
|---|---|---|---|
| C1 | DERIVATION D3 → D6 | **The main logical gap.** D6 (each branch sources its own gravitational field, λ = 1) was labelled FOLLOWS. But D3, Jacobson's argument, gives Einstein's equation as an equation of state for ⟨T_μν⟩. That is the semiclassical, mean-field equation, the λ = 0 picture of EMERGENT K3. So the chain's own source for G points, if anywhere, toward the picture D6 rejects. D8 also called D6 "the one claim beyond textbook physics", so the same step was labelled both derived and assumed. | D6 is now labelled ASSUMED, with a caveat that D1–D3 fix the *value* of G but not whether the field follows each branch. The same note is in EMERGENT K1/K3, the derivation script's output and `quantum.html`. |
| C2 | EMERGENT K4, DERIVATION D7(f), WALL, `quantum.html` | These said a single diamond held for 3 s "tells the two pictures apart". It tests Diósi–Penrose specifically. Other consistent classical-gravity models set the noise differently, so λ = 0 doesn't imply a 6 ms lifetime. | Reworded everywhere: one diamond tests DP; only the two-diamond witness measures λ. |
| C3 | DERIVATION D8, WALL, `quantum.html` | λ = 1 was presented as the framework's distinguishing claim. It is also what perturbative (effective-field-theory) quantum gravity predicts, so a positive result wouldn't single out this work. | Stated explicitly: only a null result (λ = 0) would be new physics. |
| C4 | README, `index.html`, `llms.txt`, `CITATION.cff` | These still presented S_R = ½k_BΦ_R² as untested and the Smarr check as passed. REPORT §1 records both as failed or circular, and REPORT §8 flagged the files as needing correction. | README rewritten around the current status; the original equation is kept in a collapsed "superseded" block. `index.html` has a status banner and corrected labels. `llms.txt` and `CITATION.cff` are corrected. |
| C5 | README open problem 1 | It asked for the postulate to be tested, which ASSUMPTIONS.md had already done: standard theory contradicts it. | Replaced with the current list of open questions and tests. |
| C6 | DERIVATION D1 vs README, EMERGENT, UNIFICATION | c_s = 0.3047 vs 0.3046. These are two extrapolations (R/a up to 18.5 vs 26.5), not an error. | Both values and their sources are now stated. |
| C7 | DERIVATION D4 vs TEGR E1 | Residual 10⁻¹⁶⁸ vs 10⁻¹⁶⁵. These are different random points. | Stated as ≤ 10⁻¹⁶⁵. |
| C8 | Derivation script, D3 | It cited "first law, 0.9997". 0.99969 is the local Clausius ratio; the first-law slope ratio is 0.99907 (UNIFICATION §2). | Both numbers are now printed, with their labels. |
| C9 | DERIVATION D7(d) | One cell put the baseline phase (0.594 rad at 10⁻¹⁴ kg) next to design A's run count (565 runs, which goes with 2.19 rad at 1.5×10⁻¹⁴ kg). | The two designs are now separated. |
| C10 | REPORT | It said 43 tests; there are 86. | Updated. |

**Not fixable by editing:** the PDF derivation record (`docs/`) still shows the original
claims. It is marked superseded in the README and on the site.

## 2. Spot checks that came out consistent

I recomputed each of these independently of the scripts:

- **G = πa²c³/(N c_s ħ):** follows from N·c_s·A/(4πa²) = A/(4ℓ_P²). For N = 1,
  a = √(c_s/π) ℓ_P = 0.311 ℓ_P; for N = 100, 3.11 ℓ_P.
- **Diósi–Penrose rate:** E_G = (6/5)Gm²/R for split ≫ R. For 1.5×10⁻¹⁴ kg and
  R = 1.007 µm this gives 170 /s. The radii (0.88 and 1.007 µm) match diamond density.
  The nuclear-granularity term (7.5×10¹¹ carbon atoms, R₀ = 0.54 Å) gives 4×10⁻⁶ /s,
  matching EMERGENT K3.
- **Negativity:** 0.149 = ½ sin(0.606/2), consistent with concurrence |sin(Δφ/2)|.
- **Dephasing budget:** 0.289 / 2.5 s = 0.116 /s, matching the stated 0.12 /s.
- **Modular slopes in D2:** 3.14061, 3.14135 and 3.14148 divided by π give 0.99969,
  0.99992 and 0.99997.
- **The crossing point ħω = 2.3994 k_BT** (ASSUMPTIONS §3) is reproduced from scratch by
  `src/stur_lab_test.py`.

## 3. Tensions that remain (stated, not resolved)

- **c_s depends on the regulator.** The area-law coefficient 0.3046 belongs to one
  lattice regularization, and only a²/N is fixed by the measured G. So the number in the
  headline G formula carries no predictive content. That is consistent with D8 ("the
  value of G is not derived"), but its four-digit precision shouldn't be read as a
  prediction.
- **λ = 0 is a family of models, not one model.** Mean-field gravity without noise
  (Schrödinger–Newton) is a nonlinear theory with known consistency problems. Consistent
  versions add noise whose size depends on the model. GRAVITY_ENTANGLEMENT already notes
  this; C2 above was the place where it had been forgotten.
- **Envariance** assumes probabilities exist and depend only on the state (BORN.md
  caveat). B2 and B3 don't rely on that step.

## 4. Testable predictions: an honest ranking

| Prediction | Comes from | New? | How easy to test | What it decides |
|---|---|---|---|---|
| **At fixed energy deposited, visibility loss *rises* with temperature:** −ln V = 2⟨ΔN⟩coth(ħω/2k_BT). STUR's P2 says it *falls* as 1/T. | ASSUMPTIONS §3; `src/stur_lab_test.py` | No: standard QM | **Easy.** One trapped ion, a spin-dependent kick, two motional temperatures. Existing technique. | Rules out P2. With \|α\|² = 0.1, going from n̄ = 0.1 to n̄ = 5 drops the contrast from 0.787 to 0.111. P2 predicts a rise to 0.982. |
| **Γ = 2 Var(ΔN):** visibility loss equals twice the variance of the number of quanta exchanged | ASSUMPTIONS §2 | No: it follows from standard QM. This exact statement may be unpublished; the literature hasn't been checked. | **Easy.** Same ion run, with sideband spectroscopy of the phonon number before and after. | Confirms that visibility counts quanta, not entropy. Checked to 7.5×10⁻¹¹ in Fock space. |
| V = ⟨(−1)^ΔN⟩ (parity of exchanged quanta) | UNIFICATION U2 | No | Easy. Cavity or trapped-ion parity measurement. | Confirms the decoherence sector of the unified equation. |
| A confining string's entropy saturates while its modular energy grows with length | CONFINEMENT, Z2_GAUGE | No | Moderate. Rydberg or trapped-ion simulators. | Confirms the confinement sector. |
| One 1.5×10⁻¹⁴ kg diamond lives 5.9 ms under Diósi–Penrose | EMERGENT K3 | No (DP's own prediction) | Hard: 4×10⁸ beyond today's largest superposed mass | Tests DP |
| Two diamonds entangle (λ = 1) | DERIVATION D6 | **Only a null result would be new** | Very hard: the mass gap above, and vibration noise about 140× below LISA Pathfinder | Collective vs averaged gravity |

**Bottom line.** The work, as it now stands, contains no contradiction left
unaddressed. But it also makes **no prediction that is both new and easy to test**. That
follows from its structure: everything that survived is built from known physics, so its
predictions are those of known physics. The easy tests above are worth doing because
they are cheap and decisive against the original STUR postulate. They can't come out in
STUR's favour.

A new, testable prediction needs one new quantity that changes a measurable number.
Options A–C added such quantities, and each was excluded or turned out unobservable
(WALL.md). One direction not yet tried, which would need your decision because it adds
new structure: take Jacobson's thermodynamic reading of gravity (D3) literally as
λ = 0, and derive the noise it implies from the same entanglement-per-area that fixes G.
If that fixed a decoherence rate with no free parameter, levitated-nanoparticle
experiments, which are far easier than the two-diamond test, could check it.

## Reproduce

```bash
python3 src/stur_lab_test.py      # the trapped-ion kill test; output in results/lab_test/
python -m pytest tests -q         # 86 tests
```
