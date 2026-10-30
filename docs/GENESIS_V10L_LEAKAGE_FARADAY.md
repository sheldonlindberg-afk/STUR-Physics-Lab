# GENESIS v10 Stage 10l: T→P leakage in the EB+TB test, and PMF Faraday rotation

**Script:** `scripts/genesis_v10l_leakage_faraday.py`. All 11 gates pass. Runtime is about 35 min, mostly the Part 2 Monte Carlo.
**Input:** the Stage 10h caches (`curves.npz` and `curves_tb.npz`) from the corrected final run, with STUR-B at the registered κ.
**Replaces two argued claims with calculations:**
- **Claim 8.** The drift-robust EB+TB test "remains vulnerable to T→P leakage and beam ellipticity".
- **Claim 12.** "PMF Faraday rotation is zero-mean, so it only adds anisotropy".

No registered file is modified.

## Part 1: T→P leakage and beam ellipticity

**Model.** This is the harmonic leakage-beam model ACT DR6 uses ([arXiv:2503.14452](https://arxiv.org/pdf/2503.14452)): E_obs = E + g_E T and B_obs = B + g_B T. To first order:
- EB gains g_B·TE + g_E·TB.
- TB gains g_B·TT.

**Consequences:**
- g_B adds the template [TE, TT] to [EB, TB]. That is a different direction from the angle α's [EE, TE].
- g_E enters [EB, TB] only through g_E × TB_signal.

The ℓ-shape of g_B was modelled several ways: free at every ℓ, free per bin, the HHZ parametric forms, and binned with a calibration prior. The HHZ forms are monopole (constant), dipole (∝ ℓ) and quadrupole / differential ellipticity (∝ ℓ²), after Hu, Hedman & Zaldarriaga 2003.

**Gates:**
- With leakage off, the script reproduces `genesis_v10h.tbeb_dchi2` to 6×10⁻¹⁴σ for all phases, and the Stage 10h (d) table to 0.005.
- A constant rotation is still absorbed (residual 2×10⁻⁸ of the raw χ).
- The g_E term is linear in g_E.

**Flat rotation rejected if M3a is true** (min / median / max over the 49 phases, in σ):

| Treatment of g_B (T→B leakage) | SO-like | S4-like |
|---|---|---|
| none (Stage 10h (d)) | 1.14 / 1.74 / 4.27 | 4.18 / 6.48 / 16.53 |
| **free at every ℓ** | **0.00 / 0.00 / 0.00** | **0.00 / 0.00 / 0.00** |
| free per bin, Δℓ = 50 | 0.18 / 0.27 / 0.66 | 0.72 / 0.99 / 2.33 |
| free per bin, Δℓ = 200 | 0.46 / 0.82 / 2.22 | 1.70 / 2.92 / 7.91 |
| free per bin, Δℓ = 500 | 0.70 / 1.04 / 2.60 | 2.70 / 3.79 / 9.18 |
| one constant amplitude (= HHZ monopole) | 1.11 / 1.68 / 4.24 | 4.02 / 6.16 / 15.92 |
| HHZ dipole | 1.07 / 1.57 / 3.91 | 3.93 / 5.58 / 13.66 |
| HHZ quadrupole / ellipticity | 1.11 / 1.45 / 3.22 | 4.13 / 5.07 / 10.65 |
| HHZ all three | 0.83 / 1.10 / 2.37 | 2.98 / 3.88 / 8.28 |
| Δℓ = 200 bins, prior σ_g = 0.3% | 0.49 / 0.84 / 2.29 | 1.71 / 2.94 / 7.94 |
| Δℓ = 200 bins, prior σ_g = 0.03% | 0.81 / 1.28 / 3.42 | 2.20 / 3.52 / 9.44 |

**Leakage that fakes M3a** (S4-like, ℓ = 300–3000):
- An exact per-ℓ g_B with **rms 0.019%** (median phase; 0.012–0.049% across phases) and maximum |g_B| = 0.065% reproduces M3a completely.
- The best-fit HHZ amplitudes at ℓ = 2500 for the median phase are 0.0016% (monopole), 0.0070% (dipole) and 0.015% (quadrupole / ellipticity), up to 0.048% across phases.
- For scale, the ACT DR6 residual leakage is about 0.3%, a power-spectrum-level figure that varies by array-band.

**Calibration needed** (Δℓ = 200 bins):
- **S4-like, median phase:** reaching 5σ needs the leakage known to **σ_g ≤ 0.0087%**, about 35× better than the ACT residual level.
- **The other cases** (SO-like at 3σ, and S4-like at 5σ for every phase) cannot be reached even with perfect leakage knowledge. Without leakage these tests already sit below those levels: SO-like median 1.74σ, S4-like worst phase 4.18σ.

**Null information** (S4-like, constant leakage, ΛCDM fixed):
- **TE** constrains g_E to 0.0088%. It carries no first-order g_B information.
- **BB** sees g_B only at second order, g_B² TT, which is detectable only for |g_B| > 0.029%. That is above the faking amplitude.
- **TB/EB** cannot separate g_B from the signal. With g_B free per ℓ, the [EB, TB] 2-vector is absorbed completely.

**g_E (T→E).**
- At 0.3%, the g_E·TB_signal term is itself a spurious non-flat signal of 0.58σ for S4 at the median phase. That is 9% of M3a's 6.48σ (14% at most).
- At three times the TE-limited level (0.026%) it is 0.05σ, or 0.8% of M3a. TE-based calibration of g_E removes it.

**Conclusion (claim 8).**
- T→B leakage defeats the joint EB+TB test unless the shape of g_B(ℓ) is constrained. Free per ℓ, it absorbs M3a completely; at the realistic Δℓ = 200 binning, the S4-like median falls from 6.48σ to 2.92σ.
- The leakage amplitude that fakes M3a is about 0.02%, roughly 15× below today's ACT residual level of 0.3%.
- The internal spectra cannot fix this: TE carries no first-order g_B information, and BB sees g_B only above 0.029%.
- An external leakage calibration (planet or beam maps) of g_B(ℓ) at the ≲ 0.01% level is a precondition for the M3a shape test.

## Part 2: primordial-magnetic-field Faraday rotation (Monte Carlo)

**Setup:**
- **Rotation:** α(n̂) = C′λ₀² ∫ w(χ) B₀(χn̂)·n̂ dχ, from RM = 0.812 rad m⁻² per (cm⁻³ μG pc) with comoving B₀.
- **Weight:** w = τ̇ × (fraction already emitted), from CAMB. The rotation-weighted τ is 0.950 for recombination and 0.053 for reionization.
- **Field:** a sum of 1200 transverse Fourier modes (k·e = 0), normalized to B₁Mpc = 4.4 nG, the Planck 2015 XIX power-spectrum bound.
- **Monopole:** computed per mode with the exact angular integral.
- **Anisotropic rms:** the exact line-of-sight transform on 800 directions, using a 0.1 Mpc recombination grid. The reionization grid covers only the modes it resolves; the gate shows |W(|k·n| ≥ 0.05 Mpc⁻¹)|/W(0) = 3.4×10⁻⁴.
- **Density modulation:** an n_e term (δ_e rms 10⁻³), the only route by which a monopole can arise (∮ n_e B·dA ≠ 0).

**Gates:**
- A uniform field through the line-of-sight machinery matches C′λ²B cos θ τ_eff to 3.5×10⁻¹¹.
- The divergence-free monopole is below 10⁻¹² of the rms.
- The estimator detects a monopole when ∇·B ≠ 0.
- The monopole at 40 GHz is below 0.032°.

**Results at 30 GHz, B₁Mpc = 4.4 nG** (in degrees):

| Spectrum | Anisotropic rms: pointwise | 30′ beam | 1.4′ beam | Monopole, ∇·B = 0 | Monopole with n_e modulation |
|---|---|---|---|---|---|
| n_B = −2.9 (nearly scale-invariant) | 4.53 | 3.56 | 4.39 | 5×10⁻¹⁷ | −2.7×10⁻⁵ |
| n_B = +2, cutoff 1 Mpc⁻¹ | 2.24 | 1.1×10⁻³ | 0.55 | 2×10⁻²² | 4×10⁻⁸ |
| n_B = +2, cutoff 10 Mpc⁻¹ | 94 (sub-arcsecond structure) | 5×10⁻⁴ | 0.23 | 6×10⁻²¹ | 7×10⁻⁹ |

**Normalization check.** The scale-invariant case gives 0.81° rms per nG at 30 GHz (30′ beam). The literature quotes about 1–1.6° per nG (Kosowsky & Loeb 1996); I did not verify that figure.

**Frequency dependence (α ∝ ν⁻²).** The worst-case monopole is 1.5×10⁻⁵° at 40 GHz and 1.5×10⁻⁷° at 402 GHz. The 30′ anisotropic rms for n_B = −2.9 runs from 2.0° at 40 GHz to 0.020° at 402 GHz.

**Conclusion (claim 12): confirmed by calculation.**
- A divergence-free PMF gives an exactly zero isotropic rotation: ∮ B·dA = 0 on every shell.
- The only nonzero monopole comes from n_e modulation. It is at most 1.5×10⁻⁵° at 40 GHz, more than 2000× below the 0.032° achromaticity threshold.
- PMFs at the Planck bound contribute large anisotropic rotation: 2° rms at 40 GHz for a nearly scale-invariant field. They do not contribute an isotropic β.

**Caveats:**
- The δ_e = 10⁻³ modulation amplitude is an assumption. The monopole scales linearly with it.
- The blue-spectrum cutoffs are a scan, not a damping-scale calculation.
- The intermediate LiteBIRD band centers are unverified. The ν⁻² scaling is exact.

Sources: [ACT DR6 power spectra, arXiv:2503.14452](https://arxiv.org/pdf/2503.14452); Planck 2015 XIX, *Constraints on primordial magnetic fields* ([record](https://aaltodoc.aalto.fi/items/9a13f02d-c267-42f6-9cc7-4febbd097907)).
